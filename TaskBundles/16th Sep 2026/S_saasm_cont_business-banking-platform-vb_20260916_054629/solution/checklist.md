# Checklist: Aurelia

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 319
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves a marketing site for a business banking platform. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The product serves the banking platform the marketing site sells. `src: Overview para 1`
- [ ] `C-OV-03` `capability` A visitor ends by submitting an application that provisions an organisation. `src: Overview para 1`
- [ ] `C-OV-04` `constraint` One origin carries the site alongside the platform. `src: Overview para 1`
- [ ] `C-OV-05` `constraint` The product holds no deposits of its own. `src: Overview para 2`
- [ ] `C-OV-06` `capability` The ledger mirrors the partner banks' records. `src: Overview para 2`
- [ ] `C-OV-07` `constraint` The product carries no comments feature. `src: Overview para 4`
- [ ] `C-OV-08` `constraint` The product carries no chat feature. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A Visitor reads every published page without signing in. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A Visitor cannot read a draft page. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A Visitor cannot read any statement. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An Editor publishes pages, support answers, guides. `src: User roles table row 2`
- [ ] `C-RL-05` `role` An Editor cannot reach any organisation's accounts. `src: User roles table row 2`
- [ ] `C-RL-06` `role` An Owner changes approval policy inside their own organisation. `src: User roles table row 3`
- [ ] `C-RL-07` `role` An Owner cannot reach another organisation's data. `src: User roles table row 3`
- [ ] `C-RL-08` `role` An Admin cannot change approval policy. `src: User roles table row 4`
- [ ] `C-RL-09` `role` An Approver approves a payment at or below their own limit. `src: User roles table row 5`
- [ ] `C-RL-10` `role` An Initiator cannot approve any payment. `src: User roles table row 6`
- [ ] `C-RL-11` `role` A Bookkeeper reads transactions, categorises a posting, downloads a statement. `src: User roles table row 7`
- [ ] `C-RL-12` `role` A Bookkeeper cannot move money by any route. `src: User roles table row 7`
- [ ] `C-RL-13` `role` A Card only member cannot see another cardholder's transactions. `src: User roles table row 8`
- [ ] `C-RL-14` `role` The server rejects a lower role's direct call to a higher role's endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-15` `constraint` A rejected authorization leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-16` `capability` Signup is open to anyone. `src: User roles, signup paragraph`
- [ ] `C-RL-17` `literal` The seeded Owner of Meridian Robotics is `owner@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-18` `literal` The seeded Owner of Calder Textiles is `owner2@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-19` `literal` The seeded site editor is `editor@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-20` `literal` The seeded Initiator is `initiator@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-21` `literal` The seeded Approver is `approver@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-22` `literal` The seeded Bookkeeper is `bookkeeper@example.com`. `src: User roles, seeded accounts paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` A member exchanges an email address plus a password for a bearer token. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `constraint` The app stores a password under a memory-hard password hash. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `capability` The app refuses a sign-in carrying a wrong password. `src: Core features, Auth rule 1`
- [ ] `C-CF-04` `capability` The app denies a request replaying a token that was signed out. `src: Core features, Auth rule 2`
- [ ] `C-CF-05` `capability` A step-up grant is scoped to exactly one action. `src: Core features, Auth rule 3`
- [ ] `C-CF-06` `literal` A payment at or above `1000000` minor units requires a step-up grant. `src: Core features, Auth rule 3`
- [ ] `C-CF-07` `constraint` A step-up grant for one action never authorises another action. `src: Core features, Auth rule 4`
- [ ] `C-CF-08` `capability` Every route claiming a banking capability carries the persistent disclosure sentence verbatim. `src: Core features, disclosure rule 1`
- [ ] `C-CF-09` `constraint` The disclosure sits inside the document the server returns. `src: Core features, disclosure rule 2`
- [ ] `C-CF-10` `constraint` The disclosure is visible on the route's first screen without scrolling. `src: Core features, disclosure rule 3`
- [ ] `C-CF-11` `constraint` The disclosure never sits inside a collapsed element. `src: Core features, disclosure rule 4`
- [ ] `C-CF-12` `constraint` No cookie bar overlaps the disclosure. `src: Core features, disclosure rule 5`
- [ ] `C-CF-13` `capability` Every capability claim carries a numbered marker resolving to a footnote. `src: Core features, footnote rule 1`
- [ ] `C-CF-14` `literal` The seeded footnote registry holds markers `1` through `7`. `src: Core features, footnote rule 2`
- [ ] `C-CF-15` `capability` A footnote states a condition, a qualification, a date. `src: Core features, footnote rule 3`
- [ ] `C-CF-16` `constraint` The app refuses to publish a page whose marker has no registry entry. `src: Core features, footnote rule 4`
- [ ] `C-CF-17` `capability` A footnote marker is a reference a reader can follow to the footnote. `src: Core features, footnote rule 5`
- [ ] `C-CF-18` `data` Every fee exists once as a record carrying a code, an amount, a trigger. `src: Core features, fee rule 1`
- [ ] `C-CF-19` `capability` The pricing page renders its amounts from the fee record. `src: Core features, fee rule 2`
- [ ] `C-CF-20` `capability` The legal fee schedule renders its amounts from the fee record. `src: Core features, fee rule 2`
- [ ] `C-CF-21` `capability` A fee-stating support answer renders its amount from the fee record. `src: Core features, fee rule 2`
- [ ] `C-CF-22` `constraint` The same fee reads identically on the pricing page, the fee schedule, the support answer. `src: Core features, fee rule 3`
- [ ] `C-CF-23` `capability` Every public route returns a document carrying a title plus a description. `src: Core features, public site rule 1`
- [ ] `C-CF-24` `constraint` No two public routes share a title. `src: Core features, public site rule 1`
- [ ] `C-CF-25` `capability` An unknown address renders the product's own not-found page. `src: Core features, public site rule 2`
- [ ] `C-CF-26` `constraint` No address renders the home page with a success status. `src: Core features, public site rule 2`
- [ ] `C-CF-27` `capability` The seven campaign addresses redirect permanently to a canonical destination. `src: Core features, public site rule 2`
- [ ] `C-CF-28` `constraint` Every internal link on a public route resolves to a route that answers. `src: Core features, public site rule 3`
- [ ] `C-CF-29` `capability` A sitemap lists every published public route. `src: Core features, public site rule 4`
- [ ] `C-CF-30` `capability` The site serves a favicon declared in the document head. `src: Core features, public site rule 4`
- [ ] `C-CF-31` `capability` The site records each page view with a route plus a moment. `src: Core features, public site rule 5`
- [ ] `C-CF-32` `role` Only the Editor reads the page-view record. `src: Core features, public site rule 5`
- [ ] `C-CF-33` `capability` A first-time visitor is asked once about non-essential cookies. `src: Core features, public site rule 6`
- [ ] `C-CF-34` `constraint` The cookie answer survives a reload. `src: Core features, public site rule 6`
- [ ] `C-CF-35` `capability` A support answer opens against a measured height. `src: Core features, support library rule 1`
- [ ] `C-CF-36` `capability` Every support answer carries a stable anchor a reader can link to. `src: Core features, support library rule 2`
- [ ] `C-CF-37` `capability` The support library reflects a search in the address. `src: Core features, support library rule 3`
- [ ] `C-CF-38` `capability` The support library carries structured data for question pairs. `src: Core features, support library rule 4`
- [ ] `C-CF-39` `literal` The developer reference is served at `/developers`. `src: Core features, developer reference rule 1`
- [ ] `C-CF-40` `capability` The developer reference is generated from the schema the service validates against. `src: Core features, developer reference rule 1`
- [ ] `C-CF-41` `literal` The developer reference lists the fifteen resources from `cards` to `webhooks`. `src: Core features, developer reference rule 2`
- [ ] `C-CF-42` `constraint` The worked response states the amount the worked request states. `src: Core features, developer reference rule 3`
- [ ] `C-CF-43` `capability` The worked response shows a caller-supplied idempotency key. `src: Core features, developer reference rule 4`
- [ ] `C-CF-44` `ui` The developer reference carries the command-line section plus three statements. `src: Core features, developer reference rule 5`
- [ ] `C-CF-45` `constraint` A draft record is not readable by a signed-out caller. `src: Core features, editorial rule 1`
- [ ] `C-CF-46` `constraint` A draft record appears in no sitemap. `src: Core features, editorial rule 2`
- [ ] `C-CF-47` `capability` Publishing a record makes the record readable, adds the route to the sitemap. `src: Core features, editorial rule 3`
- [ ] `C-CF-48` `capability` An editorial form rejects invalid input inline, naming the field. `src: Core features, editorial rule 5`
- [ ] `C-CF-49` `constraint` A refused editorial form writes nothing. `src: Core features, editorial rule 5`
- [ ] `C-CF-50` `capability` The application flow gives one address per step. `src: Core features, application rule 1`
- [ ] `C-CF-51` `data` Business identity records a legal name separately from a trading name. `src: Core features, application rule 2`
- [ ] `C-CF-52` `data` Business identity records expected activity as the monitoring baseline. `src: Core features, application rule 2`
- [ ] `C-CF-53` `data` Beneficial ownership identifies exactly one control person. `src: Core features, application rule 3`
- [ ] `C-CF-54` `data` Ownership through an intermediate entity is traversed to the natural persons. `src: Core features, application rule 3`
- [ ] `C-CF-55` `data` Identity verification stores the evidence rather than only a verdict. `src: Core features, application rule 4`
- [ ] `C-CF-56` `constraint` An uploaded document's bytes live in the object store. `src: Core features, application rule 5`
- [ ] `C-CF-57` `data` An attestation is recorded with the exact text shown at acceptance. `src: Core features, application rule 6`
- [ ] `C-CF-58` `ui` The deposit agreement is presented as the partner bank's document. `src: Core features, application rule 7`
- [ ] `C-CF-59` `capability` An application decision is approve, decline, or refer. `src: Core features, application rule 8`
- [ ] `C-CF-60` `constraint` Whether a decline states a reason is configured policy. `src: Core features, application rule 8`
- [ ] `C-CF-61` `capability` Approval provisions an organisation, opens one operating account. `src: Core features, application rule 9`
- [ ] `C-CF-62` `data` Every movement of value is a set of balanced entries. `src: Core features, ledger rule 1`
- [ ] `C-CF-63` `constraint` The database refuses an update against a ledger entry. `src: Core features, ledger rule 2`
- [ ] `C-CF-64` `constraint` The database refuses a delete against a ledger entry. `src: Core features, ledger rule 2`
- [ ] `C-CF-65` `capability` A correction is a new opposing entry. `src: Core features, ledger rule 3`
- [ ] `C-CF-66` `constraint` A balance is derived from entries rather than stored as an authority. `src: Core features, ledger rule 4`
- [ ] `C-CF-67` `data` Every entry carries the identifier of the cause behind the entry. `src: Core features, ledger rule 5`
- [ ] `C-CF-68` `data` Every posting carries an effective date separate from a recorded-at instant. `src: Core features, ledger rule 6`
- [ ] `C-CF-69` `capability` The app answers a balance as at a past date. `src: Core features, ledger rule 7`
- [ ] `C-CF-70` `constraint` Concurrent postings to one account leave the derived balance equal to the exact sum. `src: Core features, ledger rule 8`
- [ ] `C-CF-71` `data` The ledger carries internal accounts for in-transit value, returns suspense, unmatched clearing. `src: Core features, ledger rule 9`
- [ ] `C-CF-72` `constraint` A payment moves value through an in-transit account rather than decrementing once. `src: Core features, ledger rule 10`
- [ ] `C-CF-73` `data` An account is operating, treasury, or credit. `src: Core features, accounts rule 1`
- [ ] `C-CF-74` `ui` A credit balance carries the opposite sign to a deposit balance. `src: Core features, accounts rule 1`
- [ ] `C-CF-75` `data` Every account carries a current balance separate from an available balance. `src: Core features, accounts rule 2`
- [ ] `C-CF-76` `constraint` Spending is authorised against the available balance. `src: Core features, accounts rule 3`
- [ ] `C-CF-77` `ui` The interface labels which balance the interface is showing. `src: Core features, accounts rule 3`
- [ ] `C-CF-78` `data` A hold is a posting to the hold account rather than a flag. `src: Core features, accounts rule 4`
- [ ] `C-CF-79` `capability` An expired hold is released by a posting made by a job. `src: Core features, accounts rule 5`
- [ ] `C-CF-80` `constraint` A hold's release is linked to the settlement the hold became. `src: Core features, accounts rule 6`
- [ ] `C-CF-81` `capability` Interest accrues daily on the day's closing balance. `src: Core features, accounts rule 7`
- [ ] `C-CF-82` `constraint` Interest rounding residue accumulates to the residual ledger account. `src: Core features, accounts rule 7`
- [ ] `C-CF-83` `capability` The sweep distributes deposits across the two partner banks. `src: Core features, accounts rule 8`
- [ ] `C-CF-84` `constraint` The coverage figure shown is derived from the allocation rather than asserted. `src: Core features, accounts rule 8`
- [ ] `C-CF-85` `data` The app carries six rails from `internal` to `card`. `src: Core features, rails rule 1`
- [ ] `C-CF-86` `constraint` An ACH credit is never reported complete on submission. `src: Core features, rails rule 2`
- [ ] `C-CF-87` `capability` A return posts a reversing entry against the returns suspense account. `src: Core features, rails rule 4`
- [ ] `C-CF-88` `capability` An account goes negative after a return whose funds were spent. `src: Core features, rails rule 4`
- [ ] `C-CF-89` `capability` A return code drives different behaviour per code. `src: Core features, rails rule 5`
- [ ] `C-CF-90` `ui` The interface states a wire's irreversibility before the control is pressed. `src: Core features, rails rule 6`
- [ ] `C-CF-91` `constraint` A recall is presented as a request rather than a cancellation. `src: Core features, rails rule 6`
- [ ] `C-CF-92` `constraint` No banking calendar gates a real-time payment. `src: Core features, rails rule 7`
- [ ] `C-CF-93` `constraint` A first real-time payment to a new recipient requires step-up authentication. `src: Core features, rails rule 8`
- [ ] `C-CF-94` `data` A cutoff is stored as a local time plus a timezone identifier. `src: Core features, rails rule 9`
- [ ] `C-CF-95` `ui` The interface states the date a post-cutoff payment is scheduled for. `src: Core features, rails rule 9`
- [ ] `C-CF-96` `capability` Incoming funds follow a stated availability policy. `src: Core features, rails rule 10`
- [ ] `C-CF-97` `literal` The payment status vocabulary runs from `draft` to `recallRequested`. `src: Core features, rails rule 11`
- [ ] `C-CF-98` `constraint` The status `returned` is reachable from the status `settled`. `src: Core features, rails rule 11`
- [ ] `C-CF-99` `capability` A card authorisation creates a hold rather than a posting. `src: Core features, cards rule 3`
- [ ] `C-CF-100` `capability` A clearing exceeding a permitted margin over the authorisation posts. `src: Core features, cards rule 4`
- [ ] `C-CF-101` `capability` A clearing with no authorisation posts to the unmatched clearing account. `src: Core features, cards rule 5`
- [ ] `C-CF-102` `capability` An authorisation expires on a timer that varies by merchant category. `src: Core features, cards rule 6`
- [ ] `C-CF-103` `constraint` The card authorisation decision depends on nothing slow. `src: Core features, cards rule 7`
- [ ] `C-CF-104` `capability` A dispute posts a provisional credit that reverses on a loss. `src: Core features, cards rule 8`
- [ ] `C-CF-105` `constraint` No card primary account number enters storage. `src: Core features, cards rule 9`
- [ ] `C-CF-106` `data` An approval policy is data carrying a threshold plus a required count. `src: Core features, approvals rule 1`
- [ ] `C-CF-107` `constraint` An initiator cannot approve their own payment. `src: Core features, approvals rule 3`
- [ ] `C-CF-108` `data` A payment records the policy version that governed the payment. `src: Core features, approvals rule 4`
- [ ] `C-CF-109` `capability` A payment edited after approval returns to `pendingApproval`. `src: Core features, approvals rule 5`
- [ ] `C-CF-110` `capability` A spend control names the rule that declined a card transaction. `src: Core features, approvals rule 6`
- [ ] `C-CF-111` `capability` Every party is screened against a versioned sanctions snapshot. `src: Core features, compliance rule 1`
- [ ] `C-CF-112` `capability` Loading a new list version blocks a party newly matching. `src: Core features, compliance rule 2`
- [ ] `C-CF-113` `capability` A payment to a listed counterparty is blocked before submission. `src: Core features, compliance rule 3`
- [ ] `C-CF-114` `constraint` A potential match blocks the activity rather than warning. `src: Core features, compliance rule 5`
- [ ] `C-CF-115` `data` A screening decision records the reviewer, the reason, the list version. `src: Core features, compliance rule 6`
- [ ] `C-CF-116` `capability` An erasure request restricts access, preserving the ledger. `src: Core features, compliance rule 8`
- [ ] `C-CF-117` `capability` Reconciliation matches every posting to a bank record or raises a break. `src: Core features, records rule 1`
- [ ] `C-CF-118` `constraint` Reconciliation makes no automatic posting to match the bank. `src: Core features, records rule 2`
- [ ] `C-CF-119` `capability` A statement is generated once, stored, returned byte-identical on a second request. `src: Core features, records rule 5`
- [ ] `C-CF-120` `constraint` Categorisation never alters the ledger. `src: Core features, records rule 6`
- [ ] `C-CF-121` `data` An audit entry carries the fingerprint of the entry before. `src: Core features, records rule 7`
- [ ] `C-CF-122` `data` An agent action names the agent plus the authorising human. `src: Core features, records rule 7`
- [ ] `C-CF-123` `capability` A replayed idempotency key returns the original response. `src: Core features, interface rule 1`
- [ ] `C-CF-124` `capability` The same idempotency key carrying different parameters is an error. `src: Core features, interface rule 1`
- [ ] `C-CF-125` `data` An amount travels on the wire as a decimal string beside a currency. `src: Core features, interface rule 2`
- [ ] `C-CF-126` `data` An identifier is prefixed by a type tag. `src: Core features, interface rule 3`
- [ ] `C-CF-127` `capability` A webhook is signed over the raw body with a timestamp inside the payload. `src: Core features, interface rule 5`
- [ ] `C-CF-128` `constraint` Out-of-order webhook delivery leaves the correct final state. `src: Core features, interface rule 5`
- [ ] `C-CF-129` `capability` The event log is queryable by resource, type, time. `src: Core features, interface rule 6`
- [ ] `C-CF-130` `literal` The read limit is `120` calls a minute against `10` payment-initiating calls. `src: Core features, interface rule 7`
- [ ] `C-CF-131` `constraint` An agent-initiated payment enters `pendingApproval` whatever the amount. `src: Core features, interface rule 9`
- [ ] `C-CF-132` `capability` Revoking an agent leaves the authorising human's own access working. `src: Core features, interface rule 9`
- [ ] `C-CF-133` `literal` A stored object's key follows the scheme `vault/{kind}/{owner_id}/{sha256_of_bytes}.{ext}`. `src: Core features, documents rule 2`
- [ ] `C-CF-134` `constraint` Protected content is served only through an authenticated streaming endpoint. `src: Core features, documents rule 3`
- [ ] `C-CF-135` `constraint` A signed-out caller asking for a statement is denied. `src: Core features, documents rule 4`
- [ ] `C-CF-136` `constraint` A member of one organisation cannot read another organisation's object. `src: Core features, documents rule 4`
- [ ] `C-CF-137` `capability` The legal group carries a complaint procedure naming a regulator route. `src: Core features, fee rule 6`

## C-UF User flow

- [ ] `C-UF-01` `capability` The route table's every public address answers. `src: User flow route table`
- [ ] `C-UF-02` `capability` An unauthenticated request for a product address goes to `/login`. `src: User flow, entry paragraph`
- [ ] `C-UF-03` `capability` Signing in sends an organisation member to `/app`. `src: User flow, entry paragraph`
- [ ] `C-UF-04` `capability` Signing in sends the Editor to `/studio`. `src: User flow, entry paragraph`
- [ ] `C-UF-05` `capability` Signing out stops the token working. `src: User flow, entry paragraph`
- [ ] `C-UF-06` `capability` A visitor completes the application from the hero capture to a decision. `src: User flow journey 1`
- [ ] `C-UF-07` `capability` An approver moves a pending payment to approved. `src: User flow journey 2`
- [ ] `C-UF-08` `capability` A returned payment leaves the operating account negative. `src: User flow journey 3`
- [ ] `C-UF-09` `capability` A card clearing larger than the authorisation releases the linked hold. `src: User flow journey 4`
- [ ] `C-UF-10` `capability` A bookkeeper downloads a statement streamed from the object store. `src: User flow journey 5`
- [ ] `C-UF-11` `capability` A reader finds one wire amount across the three fee surfaces. `src: User flow journey 6`
- [ ] `C-UF-12` `capability` An editor publishes a draft, making the draft readable. `src: User flow journey 8`
- [ ] `C-UF-13` `capability` An owner revokes an agent without losing their own access. `src: User flow journey 9`
- [ ] `C-UF-14` `capability` Loading a partner-bank file raises a typed break. `src: User flow journey 10`
- [ ] `C-UF-15` `capability` Loading a sanctions version blocks a recipient newly matching. `src: User flow journey 11`
- [ ] `C-UF-16` `ui` Every list carries an empty state naming what would fill the list. `src: User flow, states paragraph`
- [ ] `C-UF-17` `constraint` The server-error page never tells a customer to try again. `src: User flow, states paragraph`
- [ ] `C-UF-18` `ui` The not-found page carries a route to the support library. `src: User flow, states paragraph`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The public site may carry atmosphere with the subject seen first. `src: UI/UX notes para 2`
- [ ] `C-UX-02` `ui` The product surfaces read quiet, dense, organised for scanning. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` Nothing moves on a page where money is being authorised. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` The page ground stays visibly separate from a raised surface without a shadow. `src: UI/UX notes para 3`
- [ ] `C-UX-05` `ui` One brand colour carries the primary action alone. `src: UI/UX notes para 3`
- [ ] `C-UX-06` `ui` One further colour means an error, appearing nowhere else. `src: UI/UX notes para 3`
- [ ] `C-UX-07` `ui` Every colour role carries an inverted twin. `src: UI/UX notes para 4`
- [ ] `C-UX-08` `ui` Text roles sit in a ladder parallel to icon roles. `src: UI/UX notes para 4`
- [ ] `C-UX-09` `ui` Interface type sits a shade heavier on the variable axis than reading type. `src: UI/UX notes para 5`
- [ ] `C-UX-10` `ui` A monospace with tabular figures carries every amount. `src: UI/UX notes para 5`
- [ ] `C-UX-11` `constraint` No font binary is fetched at run time. `src: UI/UX notes para 5`
- [ ] `C-UX-12` `ui` One small corner softening carries almost the whole interface. `src: UI/UX notes para 7`
- [ ] `C-UX-13` `ui` Elevation stays soft enough to separate rather than lift. `src: UI/UX notes para 8`
- [ ] `C-UX-14` `ui` Everything moves on one family of curves at one speed. `src: UI/UX notes para 9`
- [ ] `C-UX-15` `ui` The focus outline changes colour along with everything else. `src: UI/UX notes para 9`
- [ ] `C-UX-16` `ui` A celebration runs only on a granted application. `src: UI/UX notes para 9`
- [ ] `C-UX-17` `ui` A reduced-motion preference replaces a movement with a static affordance. `src: UI/UX notes para 10`
- [ ] `C-UX-18` `constraint` No smooth-scroll layer takes over scrolling. `src: UI/UX notes para 10`
- [ ] `C-UX-19` `ui` The layout archetype is a top navigation carrying five centred items. `src: UI/UX notes para 11`
- [ ] `C-UX-20` `ui` Each page leads with one primary action distinct from every secondary one. `src: UI/UX notes para 11`
- [ ] `C-UX-21` `ui` A control carries resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes para 12`
- [ ] `C-UX-22` `constraint` Unavailable is never signalled by colour alone. `src: UI/UX notes para 12`
- [ ] `C-UX-23` `ui` Escape closes an open panel, returning focus to the opening control. `src: UI/UX notes para 12`
- [ ] `C-UX-24` `ui` Body text meets the WCAG AA contrast bar on both grounds. `src: UI/UX notes para 13`
- [ ] `C-UX-25` `ui` Each route carries one first-rank heading. `src: UI/UX notes para 13`
- [ ] `C-UX-26` `ui` Keyboard navigation reaches every control with a visible focus ring. `src: UI/UX notes para 13`
- [ ] `C-UX-27` `ui` An icon-only control carries a name saying what the control does. `src: UI/UX notes para 13`
- [ ] `C-UX-28` `ui` Every content image carries alternative text. `src: UI/UX notes para 13`
- [ ] `C-UX-29` `ui` The layout is mobile first across six ascending breakpoints. `src: UI/UX notes para 14`
- [ ] `C-UX-30` `ui` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes para 14`
- [ ] `C-UX-31` `ui` A short viewport suppresses the full-height treatment. `src: UI/UX notes para 14`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Every public address returns a complete HTML document from the server. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The datastore is PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The object store is MinIO reached at `STORAGE_ENDPOINT`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `constraint` No second datastore is introduced. `src: Technical requirements para 2`
- [ ] `C-TR-05` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements para 3`
- [ ] `C-TR-06` `constraint` The disclosure paints in the first paint of every claiming route. `src: Technical requirements para 4`
- [ ] `C-TR-07` `constraint` No two public routes share a description. `src: Technical requirements para 5`
- [ ] `C-TR-08` `contract` A robots file names the sitemap. `src: Technical requirements para 5`
- [ ] `C-TR-09` `constraint` Every internal link on a public route resolves. `src: Technical requirements para 6`
- [ ] `C-TR-10` `contract` Logs are one line of JSON per request carrying a request identifier. `src: Technical requirements para 7`
- [ ] `C-TR-11` `constraint` No amount is written to a log. `src: Technical requirements para 7`
- [ ] `C-TR-12` `constraint` No credential is written to a log. `src: Technical requirements para 7`
- [ ] `C-TR-13` `capability` Published content is produced once, refreshed when the record changes. `src: Technical requirements para 9`
- [ ] `C-TR-14` `constraint` Every derived figure is reproducible from the ledger plus a date. `src: Technical requirements para 11`
- [ ] `C-TR-15` `capability` Every limit carries a default, producing a specific refusal. `src: Technical requirements para 12`
- [ ] `C-TR-16` `constraint` Analytics never run before the disclosure has painted. `src: Technical requirements para 13`
- [ ] `C-TR-17` `constraint` No binary asset is fetched at run time. `src: Technical requirements para 13`
- [ ] `C-TR-18` `constraint` The app stays responsive at the stated data volumes. `src: Technical requirements para 14`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-02` `contract` The seeded credentials are written into `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` A membership carries a role among the six named roles. `src: Data model, identity paragraph`
- [ ] `C-DM-04` `data` A page carries a state among `draft` plus `published`. `src: Data model, content paragraph`
- [ ] `C-DM-05` `data` A footnote carries a marker, a claim key, an as-of date. `src: Data model, content paragraph`
- [ ] `C-DM-06` `data` A fee carries a code, an amount in minor units, an effective-from date. `src: Data model, content paragraph`
- [ ] `C-DM-07` `data` A beneficial owner carries a parent owner link making the ownership a graph. `src: Data model, application paragraph`
- [ ] `C-DM-08` `data` An entry carries a direction among `debit` plus `credit`. `src: Data model, ledger paragraph`
- [ ] `C-DM-09` `data` The balance cache is a projection that may be discarded. `src: Data model, ledger paragraph`
- [ ] `C-DM-10` `data` A payment carries a rail among the six named rails. `src: Data model, money movement paragraph`
- [ ] `C-DM-11` `data` A cutoff carries a timezone identifier rather than an offset. `src: Data model, money movement paragraph`
- [ ] `C-DM-12` `data` A card record holds a token plus the last four digits. `src: Data model, cards paragraph`
- [ ] `C-DM-13` `data` An idempotency record is unique on the organisation, the operation, the key. `src: Data model, interface paragraph`
- [ ] `C-DM-14` `data` An event sequence rises by exactly one within a resource. `src: Data model, interface paragraph`
- [ ] `C-DM-15` `data` A reconciliation break carries a kind among the four named kinds. `src: Data model, interface paragraph`
- [ ] `C-DM-16` `data` An amount is an integer in the currency's minor unit. `src: Data model, money paragraph`
- [ ] `C-DM-17` `constraint` No money value is a floating-point number. `src: Data model, money paragraph`
- [ ] `C-DM-18` `literal` The stored currency code is `usd` against the wire code `USD`. `src: Data model, money paragraph`
- [ ] `C-DM-19` `constraint` Every posting's debits equal the posting's credits. `src: Data model, invariants paragraph`
- [ ] `C-DM-20` `constraint` Neither organisation reads the other organisation's rows. `src: Data model, invariants paragraph`
- [ ] `C-DM-21` `literal` The seeded organisations are `Meridian Robotics` plus `Calder Textiles`. `src: Data model, seed paragraph`
- [ ] `C-DM-22` `literal` The seeded clean recipient is `Jane Black` carrying `rcpt_4d82e1af`. `src: Data model, seed paragraph`
- [ ] `C-DM-23` `literal` The seeded recipient `Viktor Halberd` appears in list version `2026-09-15`. `src: Data model, seed paragraph`
- [ ] `C-DM-24` `literal` The seeded domestic wire fee is `1500` minor units. `src: Data model, seed paragraph`
- [ ] `C-DM-25` `literal` The seeded draft page is `Treasury sweep explained`. `src: Data model, seed paragraph`
- [ ] `C-DM-26` `literal` The seeded statement covers period `2026-08` for `Meridian Operating`. `src: Data model, seed paragraph`
- [ ] `C-DM-27` `literal` The stated application duration is `10` minutes. `src: Data model, seed paragraph`
- [ ] `C-DM-28` `literal` The stated yield rate is `4.20%` as of `2026-09-01`. `src: Data model, seed paragraph`
- [ ] `C-DM-29` `constraint` Seeding is idempotent across a restart. `src: Data model, closing line`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` One token layer is defined at the root, consumed everywhere. `src: Front-end specification, token layer`
- [ ] `C-FE-02` `ui` A component never computes a hover colour for the component. `src: Front-end specification, token layer`
- [ ] `C-FE-03` `ui` No colour code appears anywhere in the build. `src: Front-end specification, palette`
- [ ] `C-FE-04` `ui` The hero scrim keeps the disclosure legible over the scene. `src: Front-end specification, palette`
- [ ] `C-FE-05` `ui` Three type roles exist, no fourth. `src: Front-end specification, type`
- [ ] `C-FE-06` `ui` Every icon is drawn geometry rather than an image file. `src: Front-end specification, iconography`
- [ ] `C-FE-07` `ui` An internal drawing reference is made unique per instance. `src: Front-end specification, iconography`
- [ ] `C-FE-08` `literal` The wordmark is set as `A U R E L I A`. `src: Front-end specification, iconography`
- [ ] `C-FE-09` `literal` The announcement bar carries `Real-time payments are here - instant, free, 24/7/365.` `src: Front-end specification, global chrome`
- [ ] `C-FE-10` `literal` The header carries the five items from `Products` to `Pricing`. `src: Front-end specification, global chrome`
- [ ] `C-FE-11` `ui` A mega-menu panel descends from the header rather than floating below. `src: Front-end specification, global chrome`
- [ ] `C-FE-12` `ui` The cookie bar is anchored to the foot, never a modal. `src: Front-end specification, global chrome`
- [ ] `C-FE-13` `literal` The skip link reads `Skip to main content` as the first focusable element. `src: Front-end specification, global chrome`
- [ ] `C-FE-14` `ui` The money display receives a minor amount plus a currency. `src: Front-end specification, money display`
- [ ] `C-FE-15` `constraint` The money display performs no arithmetic. `src: Front-end specification, money display`
- [ ] `C-FE-16` `ui` A negative amount renders explicitly rather than by colour alone. `src: Front-end specification, money display`
- [ ] `C-FE-17` `literal` The hero headline reads `Radically different banking`. `src: Front-end specification, home page`
- [ ] `C-FE-18` `literal` The hero capture field reads `Enter your email` beside `Open account`. `src: Front-end specification, home page`
- [ ] `C-FE-19` `ui` The feature stack carries the pinned heading above the three expanding rows. `src: Front-end specification, home page`
- [ ] `C-FE-20` `ui` The illustration grain is generated by the browser rather than fetched. `src: Front-end specification, home page`
- [ ] `C-FE-21` `literal` The developer headline reads `Programmable finances for developers & agents`. `src: Front-end specification, developer reference`
- [ ] `C-FE-22` `literal` The command-line control reads `Install CLI`. `src: Front-end specification, developer reference`
- [ ] `C-FE-23` `ui` The legal pages carry no motion of any kind. `src: Front-end specification, legal pages`
- [ ] `C-FE-24` `ui` The legal measure is capped at a comfortable reading width. `src: Front-end specification, legal pages`
- [ ] `C-FE-25` `literal` The server-error page carries the title `500: Internal Server Error`. `src: Front-end specification, error pages`
- [ ] `C-FE-26` `ui` The working surface for transactions is a table. `src: Front-end specification, product surfaces`
- [ ] `C-FE-27` `ui` Raising a payment is a dedicated address rather than a panel. `src: Front-end specification, product surfaces`
- [ ] `C-FE-28` `ui` An outcome is an inline banner above the surface the outcome changed. `src: Front-end specification, product surfaces`
- [ ] `C-FE-29` `constraint` The disclosure sentence is never rewritten for tone. `src: Front-end specification, copy`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One origin serves both surfaces. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` No real-time audio of any kind is carried. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` No request leaves the origin at run time. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` No card primary account number appears in a response. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` Settlement is an operator action inside the app. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` No mobile application is served. `src: Constraints bullet 6`
- [ ] `C-CN-07` `constraint` No email is sent by the app. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` No image file ships with the build. `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` No blanket rule transitions every property. `src: Constraints bullet 9`
- [ ] `C-CN-10` `constraint` No social graph is carried. `src: Constraints bullet 10`
- [ ] `C-CN-11` `constraint` The app stays responsive at two organisations. `src: Constraints bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200`. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` The `.browser_screenshots/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` The `.downloads/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` A production build is served behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `contract` No copy of a backing service is downloaded or started. `src: Deployment contract bullet 10`
- [ ] `C-DC-13` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes table`
- [ ] `C-DC-14` `contract` An invalid or unauthorized call is rejected as a client error. `src: Deployment contract, API shapes closing paragraph`
- [ ] `C-DC-15` `constraint` The object store is the only home for uploaded bytes. `src: Deployment contract, No mocks`
- [ ] `C-DC-16` `constraint` Rows live in PostgreSQL rather than in a process. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-DM-01 | Data model, password paragraph |
| `owner@example.com` | seeded Owner of Meridian Robotics | C-RL-17 | User roles, seeded accounts |
| `owner2@example.com` | seeded Owner of Calder Textiles | C-RL-18 | User roles, seeded accounts |
| `editor@example.com` | seeded site editor | C-RL-19 | User roles, seeded accounts |
| `initiator@example.com` | seeded Initiator | C-RL-20 | User roles, seeded accounts |
| `approver@example.com` | seeded Approver | C-RL-21 | User roles, seeded accounts |
| `bookkeeper@example.com` | seeded Bookkeeper | C-RL-22 | User roles, seeded accounts |
| `1000000` | step-up threshold in minor units | C-CF-06 | Core features, Auth rule 3 |
| `Aurelia is a fintech company, not an FDIC-insured bank. Banking services provided through Northgate Bank and Talbot National, Members FDIC.` | the persistent disclosure | C-CF-08 | Core features, disclosure rule 1 |
| `1` | first footnote marker | C-CF-14 | Core features, footnote rule 2 |
| `7` | last footnote marker | C-CF-14 | Core features, footnote rule 2 |
| `/developers` | the developer reference route | C-CF-39 | Core features, developer reference rule 1 |
| `cards` | first resource in the index | C-CF-41 | Core features, developer reference rule 2 |
| `webhooks` | last resource in the index | C-CF-41 | Core features, developer reference rule 2 |
| `internal` | first payment rail | C-CF-85 | Core features, rails rule 1 |
| `card` | last payment rail | C-CF-85 | Core features, rails rule 1 |
| `draft` | first payment status | C-CF-97 | Core features, rails rule 11 |
| `recallRequested` | last payment status | C-CF-97 | Core features, rails rule 11 |
| `120` | read calls per minute per token | C-CF-130 | Core features, interface rule 7 |
| `10` | payment-initiating calls per minute per token | C-CF-130 | Core features, interface rule 7 |
| `vault/{kind}/{owner_id}/{sha256_of_bytes}.{ext}` | the object key scheme | C-CF-133 | Core features, documents rule 2 |
| `/app/USER_README.md` | credential file path | C-DM-02 | Data model, password paragraph |
| `usd` | stored currency code | C-DM-18 | Data model, money paragraph |
| `USD` | wire currency code | C-DM-18 | Data model, money paragraph |
| `Meridian Robotics` | seeded organisation one | C-DM-21 | Data model, seed paragraph |
| `Calder Textiles` | seeded organisation two | C-DM-21 | Data model, seed paragraph |
| `Jane Black` | seeded clean recipient | C-DM-22 | Data model, seed paragraph |
| `rcpt_4d82e1af` | seeded clean recipient external id | C-DM-22 | Data model, seed paragraph |
| `Viktor Halberd` | seeded recipient newly listed | C-DM-23 | Data model, seed paragraph |
| `2026-09-15` | sanctions list version that lists Viktor Halberd | C-DM-23 | Data model, seed paragraph |
| `1500` | domestic wire fee in minor units | C-DM-24 | Data model, seed paragraph |
| `Treasury sweep explained` | the seeded draft page title | C-DM-25 | Data model, seed paragraph |
| `2026-08` | the seeded statement period | C-DM-26 | Data model, seed paragraph |
| `Meridian Operating` | the seeded operating account | C-DM-26 | Data model, seed paragraph |
| `4.20%` | the stated yield rate | C-DM-28 | Data model, seed paragraph |
| `2026-09-01` | the yield rate as-of date | C-DM-28 | Data model, seed paragraph |
| `A U R E L I A` | the letterspaced wordmark | C-FE-08 | Front-end specification, iconography |
| `Real-time payments are here - instant, free, 24/7/365.` | the announcement copy | C-FE-09 | Front-end specification, global chrome |
| `Products` | first navigation item | C-FE-10 | Front-end specification, global chrome |
| `Pricing` | last navigation item | C-FE-10 | Front-end specification, global chrome |
| `Skip to main content` | the skip link copy | C-FE-13 | Front-end specification, global chrome |
| `Radically different banking` | the hero headline | C-FE-17 | Front-end specification, home page |
| `Enter your email` | the hero field label | C-FE-18 | Front-end specification, home page |
| `Open account` | the hero primary action | C-FE-18 | Front-end specification, home page |
| `Get started fast. And never stop moving.` | the feature heading | C-FE-19 | Front-end specification, home page |
| `Programmable finances for developers & agents` | the developer headline | C-FE-21 | Front-end specification, developer reference |
| `Install CLI` | the command-line control | C-FE-22 | Front-end specification, developer reference |
| `500: Internal Server Error` | the server-error title | C-FE-25 | Front-end specification, error pages |
| `APP_PUBLIC_URL` | the public origin variable | C-DC-01 | Deployment contract bullet 1 |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | C-DC-02 | Deployment contract bullet 1 |
| `/api` | the API prefix | C-DC-03 | Deployment contract bullet 2 |
| `GET /api/health` | the health route | C-DC-04 | Deployment contract bullet 3 |
| `200` | the health status | C-DC-04 | Deployment contract bullet 3 |
| `.browser_screenshots/` | reserved directory | C-DC-07 | Deployment contract bullet 6 |
| `.downloads/` | reserved directory | C-DC-08 | Deployment contract bullet 6 |
| `0.0.0.0` | the bind address | C-DC-11 | Deployment contract bullet 9 |
| `DATABASE_URL` | the datastore variable | C-TR-02 | Technical requirements para 1 |
| `STORAGE_ENDPOINT` | the object store variable | C-TR-03 | Technical requirements para 1 |
| `pendingApproval` | the awaiting-decision status | C-CF-109 | Core features, approvals rule 5 |
| `debit` | one entry direction | C-DM-08 | Data model, ledger paragraph |
| `credit` | the other entry direction | C-DM-08 | Data model, ledger paragraph |
| `published` | the readable page state | C-DM-04 | Data model, content paragraph |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the permitted margin a clearing may exceed its authorisation by | C-CF-100 | named as a scheme rule with no figure given |
| the ownership threshold for a beneficial owner | C-CF-53 | named as configuration with no figure given |
| the six ascending responsive tiers | C-UX-29 | the count is pinned, the widths are the builder's |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 8 | 8 |
| User roles | 20 | 22 |
| Core features | 120 | 137 |
| User flow | 16 | 18 |
| UI and UX notes | 28 | 31 |
| Technical requirements | 16 | 18 |
| Data model | 26 | 29 |
| Front-end specification | 26 | 29 |
| Constraints | 11 | 11 |
| Deployment contract | 15 | 16 |
