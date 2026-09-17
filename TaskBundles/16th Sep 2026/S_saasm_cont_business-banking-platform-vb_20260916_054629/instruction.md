# Aurelia

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, read the home page, start an application from the email capture in the hero, work through the business details, the beneficial owners, the identity checks, the documents and the attestations, receive an approval, and sign in to find an operating account whose balance is the sum of balanced opening entries rather than a number somebody typed, all without hitting an error page. Three things in that sentence cannot be arranged inside the app's own screens. The formation document the applicant uploads must exist as a real object in MinIO under the key scheme pinned below, and the `2026-08` statement for `Meridian Operating` must be served from the object it was generated into rather than rebuilt on request: bytes on the app's own disk, a row in PostgreSQL holding a file, or a page that redraws a statement from the ledger each time somebody asks are each a contract violation however good the interface looks. A draft page and another organisation's statement must not be readable by a signed-out caller or by a member of a different organisation, by any address. And when fifty requests carrying one idempotency key arrive at once for the same payment, exactly one payment exists afterwards and all fifty callers receive the same response body.

## Overview

Aurelia is a marketing and documentation site for a business banking platform aimed at startups and small companies, and it is the platform that site sells. Both live on one origin. The site carries a product overview, pricing, seven product pages, three solutions pages, a resources library, a developer reference and a support library; the platform carries the ledger, accounts, payment rails, cards, spend controls with approvals, invoicing, compliance and the developer interface over all of it. A visitor ends by submitting an application that opens an account and provisions their organisation, and that submission is the seam between the two halves.

The product is not an ordinary web application with payments attached, and a build that treats it as one will be wrong in ways that are examinable rather than merely buggy. Aurelia does not hold deposits. Two chartered partner banks do, and Aurelia's ledger is a mirror of theirs. Every capability claim on the marketing surface carries a numbered footnote. Moving money, onboarding a company and keeping records are activities with deadlines that the system has to track rather than features it can ship late.

The regulatory frame is the reason this reads as it does, and it runs through every section below.

Five audiences, and the site is answerable to all of them. A founder opening an account, who came for what it is, what it costs and how fast. A finance operator, who came for controls, approvals and treasury. A developer, who came for the interface and the tooling. An accountant or bookkeeper, who came for statements, categorisation and exports. A compliance reviewer, who came for the disclosures and the partner banks. And a site editor, who writes and publishes everything the first five read.

What it deliberately is not. No real-time audio or video. No real partner-bank connection, card processor, card network, identity vendor, sanctions vendor, content host or measurement vendor: each is modelled inside this app against seeded data and operator actions. No card primary account numbers anywhere, ever. No mobile or desktop application. No second datastore, cache, queue, identity provider or mail vendor. No comments, no social features, no chat.

The genuinely hard part is that a balance is not a column. Every movement of value is a set of balanced, append-only entries, a balance is derived from them, an ACH payment that has settled can still be returned weeks later, and a card clearing routinely arrives for a different amount than the authorisation that preceded it. A system that cannot represent those three events has lost the money from its books and will not know why.

## User roles

Two roles live on the public site and six live inside a provisioned organisation. A role is read from the signed-in member's membership record and never from a request body, a query parameter or a header the caller controls.

| Role | Can do | Cannot do |
|---|---|---|
| Visitor | Read every published page, the pricing, the support library and the developer reference; start and complete an application | **Read a draft page, any statement, any document, any transaction or any organisation's data** |
| Editor | Write, edit and publish pages, support answers and guides; maintain the fee schedule and the footnote registry; read the page-view log | **Reach any organisation's accounts, payments, cards, statements or audit log, and move money by any route** |
| Owner | Everything inside their own organisation, including closing an account, changing approval policy, issuing and revoking tokens, and revoking an agent | **Reach another organisation's data, and approve a payment they themselves created** |
| Admin | Manage users and cards, add and edit recipients, create payments, approve within their limit | **Change approval policy, close an account, or approve a payment they themselves created** |
| Approver | Read everything in their organisation, approve or reject a payment at or below their own limit | **Create a payment and then approve it, approve above their limit, or change policy** |
| Initiator | Create payments and recipients, read their organisation's transactions | **Approve any payment, including their own; change policy; manage users or cards** |
| Bookkeeper | Read transactions and statements, categorise a posting, export, download a statement | **Move money by any route, create or approve a payment, add a recipient, or issue a card** |
| Card only | Use the card issued to them and read their own card transactions | **See another cardholder's transactions, see the organisation's accounts or payments, or move money by any route other than their own card** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from an Initiator session to any Approver-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create an account and start an application, and an application is what produces an organisation; joining an existing organisation is by invitation from its Owner or Admin.

Nine accounts are seeded, every one of them on the password named in `## Data model`. `editor@example.com` is Wren Ashby, the site editor. `reader@example.com` is Nell Okonjo, a signed-in reader of the support library who belongs to no organisation. Inside `Meridian Robotics`: `owner@example.com` is Priya Raman, the Owner; `admin@example.com` is Tom Vance, the Admin; `approver@example.com` is Ida Kemp, the Approver; `initiator@example.com` is Sam Oyelaran, the Initiator; `bookkeeper@example.com` is Grace Lindqvist, the Bookkeeper; `cardholder@example.com` is Milo Fenn, card only. Inside `Calder Textiles`: `owner2@example.com` is Bea Calder, its Owner.

## Core features

### Auth

Email and password are exchanged for a bearer token. Passwords are stored under a modern memory-hard password hash and never in any recoverable form. The client sends the token as a bearer credential on every API call; a server-rendered page reads the same token from an http-only cookie so that a page works before any script runs. Tokens expire, and an expired token returns the caller to the sign-in page with the pending work unwritten.

1. Signing in with a wrong password is refused, and the refusal does not say which of the two was wrong.
2. Signing out invalidates the token; a request replaying that token afterwards is denied.
3. Step-up re-authentication is a second, short-lived grant scoped to exactly one action, and it is required for: adding a recipient, the first payment to a recipient, changing approval policy, changing a recipient's payout details, adding a user, and any payment at or above `1000000` minor units. A recovery flow is never a way around it.
4. A step-up grant for one action never authorises another, and it expires.

### The persistent disclosure

This is not a footer credit and it must not be treated as one.

1. Every route where a banking capability is claimed carries the sentence `Aurelia is a fintech company, not an FDIC-insured bank. Banking services provided through Northgate Bank and Talbot National, Members FDIC.` exactly, letter for letter.
2. It is inside the document the server returns, so it is present in the first paint. A disclosure that depends on script is not a disclosure.
3. It is visible on the route's first screen without scrolling, because it corrects an impression the page has just created.
4. It is never inside a collapsed, dismissible or hidden element, and it is in the accessibility tree.
5. Its position is computed from the real heights of whatever chrome sits below it, so dismissing the announcement bar or the cookie bar re-seats it rather than leaving a gap, and no cookie bar, chat widget or announcement bar ever overlaps it or lets it scroll underneath.

### The footnote registry

One record per claim, and the marker and the footnote are produced from it together, so a claim cannot be published without its qualification. A build that renders the markers without the footnotes is worse than one that renders neither.

1. Every capability, rate, timing, cost and insurance claim carries a numbered marker that resolves to a footnote stating the condition, the qualification and a date.
2. The seeded registry has seven entries, and the marker number is the footnote's identity: `1` qualifies the word `banking`, `2` qualifies `instant`, `3` qualifies `free`, `4` qualifies `Get a credit card instantly`, `5` qualifies the deposit-insurance figure, `6` qualifies the yield rate, `7` qualifies the customer count.
3. A timing claim states whether it is typical or guaranteed and what delays it. A cost claim states what is free, what is not and on what condition. An insurance claim states which entity holds the deposits, through what mechanism, and the per-institution limit. A yield claim states the rate, the date it is as of, and that it varies. A credit claim states that approval is subject to underwriting.
4. Publishing a page that carries a marker with no matching registry entry is refused, and the page stays a draft.
5. A marker is a real reference: it is announced, it can be followed to its footnote and back, and it is never a decorative character sitting loose in the text.

### One fee source

1. Every fee exists once, as a record carrying a code, a name, an amount in integer minor units, its currency, its trigger, any waiver condition and an effective-from date.
2. The pricing page, the legal fee schedule at `/legal/fees` and every support answer that states a fee are all generated from that record. None of them stores its own copy of an amount.
3. The same fee read from `/pricing`, from `/legal/fees` and from the support answer that mentions it states the same amount and the same waiver condition.
4. An amount stated in one of those three places and not in the others is a defect, not a content difference, and the build refuses to publish it.
5. Rates carry the date they are as of.
6. The legal group is part of the product rather than boilerplate, and it is complete: the partner bank's deposit account agreement presented as theirs, Aurelia's own terms of service, a privacy notice carrying the disclosures the operating jurisdictions require, the insurance disclosure, the fee schedule, a statement of the partner banks' own terms, and a **complaint procedure carrying the regulator's contact route**.
7. None of those documents is transcribed from anywhere else. Another institution's deposit agreement is not text to copy, and a footnote that is not true of this product is worse than no footnote.

### The public site and its routes

1. Every public route returns a complete HTML document with its own title and its own description, and no two public routes share either. The title pattern is `Aurelia | Online Business Banking For Startups & Small Businesses`; the home route's title is `Online Business Banking For Startups, Small Businesses & Scaling Companies`; the developer reference's is `Full Banking API, Terminal-Native CLI & AI-Ready MCP Server | Aurelia`; the support library's is `FAQs | Pricing, Moving Your Money & More | Aurelia`.
2. An unknown address renders Aurelia's own not-found page and answers not-found. **No address ever renders the home page with a success status.** The seven campaign addresses `/as`, `/gs`, `/pb`, `/a/b`, `/a/i`, `/g/d` and `/wa` redirect permanently to a canonical destination instead.
3. Every internal link on every public route resolves to a route that exists and answers.
4. A sitemap lists every published public route, a robots file points at the sitemap, and the site serves a favicon and declares it in the document head.
5. The site records each page view with its route and the moment it happened, readable by the Editor and by nobody else. Nothing is sent to any outside address.
6. A first-time visitor is asked once about non-essential cookies in a bar anchored to the foot of the page, never a modal, with rejecting exactly as easy as accepting. The answer survives a reload, and the local page-view record is only written once the answer is yes.

### The support library

1. Answers are grouped by topic and open one at a time against their own measured height, so a long answer is never clipped and a short one never crawls.
2. Every answer has a stable anchor and is linkable, because support agents send links to answers.
3. It is server-rendered, and it is searchable with the search reflected in the address.
4. It carries structured data for question and answer pairs.
5. Any answer stating a fee or a timing is generated from the fee record, per the rule above.

### The developer reference

1. It is served at `/developers`, runs on the inverted ground, and is generated from the same schema the service validates against, so the published reference and the service cannot drift.
2. It lists exactly fifteen resources, each with its description, letter for letter: `cards` - `List debit and credit cards for an account`; `categories` - `List expense categories`; `credit` - `List credit accounts`; `customers` - `Create, update, and manage customers`; `events` - `List and inspect API events`; `invoices` - `Create, update, and manage invoices`; `org` - `View organization details`; `payments` - `Send money, request approvals, and transfer between accounts`; `recipients` - `Add, update, and manage payment recipients`; `safes` - `List and download SAFE agreements`; `statements` - `Download account statements as PDF`; `transactions` - `Search, update, and attach files to transactions`; `treasury` - `View treasury accounts`; `users` - `List and view organization team members`; `webhooks` - `Set up and manage webhook endpoints`.
3. It renders a worked request and the response that comes back, in a terminal panel. The request names an account, a recipient, an amount, a payment method, an external memo and an idempotency key. **The amount in the response is the amount in the request**: a published example whose request and response disagree by fifty cents is a defect in a payments product, not a rounding.
4. The worked response shows the six facts the contract actually carries: a caller-supplied idempotency key, an amount as a decimal string rather than a number, a currency travelling with that amount, prefixed and type-tagged identifiers, an opaque account identifier, and a status of `pendingApproval` proving a payment can exist in a non-terminal state awaiting a decision.
5. It carries the command-line section headed `Use the Aurelia CLI to run your finances from your terminal`, its three points and its `Install CLI` control, and it states that the tool authenticates with its own scoped credential rather than a copied session, prints a confirmation before any value-moving action unless told not to, and never prints a full credential.

### The editorial surface

1. The Editor writes pages, support answers and guides. A record in the `draft` state is **not readable by a signed-out caller and not readable by any signed-in caller who is not the Editor**, at its own address or at any other.
2. A draft appears in no sitemap, in no search result and in no internal link on a published page.
3. Publishing makes the record readable, gives it its own title and description, and adds it to the sitemap.
4. The Editor maintains the fee records and the footnote registry through the same surface.
5. Every form in this surface rejects invalid input inline, names the field that was wrong, and writes nothing when it refuses.

### The application

An account application is not a signup, and the requirements here are legal rather than aesthetic.

1. The flow is one address per step: an email capture, business identity, beneficial ownership, individual identity, documents, review, decision. The capture is one field and one control, and nothing is qualified prematurely.
2. Business identity records the legal name and the trading name as different things, the entity type, the formation jurisdiction, the registration number, the formation date, the registered and operating addresses as different things, the tax identifier, the nature of the business as a classification code, and the expected activity as volumes, counterparties and geographies. **Expected activity is the baseline the monitoring rules compare against**, so collecting it and never reading it is doing the paperwork and not the control.
3. Beneficial ownership identifies every natural person owning at or above the configured threshold, plus exactly one control person regardless of ownership. Ownership through an intermediate entity is traversed to the natural persons. The threshold and the traversal rules are configuration, and the ownership structure is stored as a graph rather than as a list of names.
4. Individual identity records, for each of those people, a name, a date of birth, an address and a government identifier, with a document check where risk requires it. **The evidence is stored, not only the verdict**: a stored `verified` with nothing behind it cannot be re-examined.
5. Documents are the formation documents, plus any further document a risk trigger demands. Their bytes live in the object store, never on the app's disk and never in a database column.
6. Every attestation and every disclosure is recorded with **the exact text that was shown**, stored alongside the acceptance and its moment, never a reference to a document that may later change.
7. The deposit agreement is presented as the partner bank's, not as Aurelia's.
8. The decision is approve, decline or refer for manual review. **Whether a decline states its specific reason is configured policy, not a fixed string**, because in some jurisdictions the law requires an adverse-action explanation and in others explaining would prejudice an investigation.
9. Approval provisions the organisation, opens one operating account at `Northgate Bank`, makes the applicant its Owner, and writes the opening postings. Nothing about that is a flag on a row: the account's balance is derived from those postings.

### The ledger

This is the decision everything else rests on.

1. Every movement of value is one or more **entries**, and entries come in balanced sets: within a single posting, debits equal credits, in one currency.
2. Entries are **append-only**. They are never updated and never deleted, and an attempt to do either as the application's own database user is refused by the database rather than merely absent from the code.
3. A correction is a new, opposing entry, never an edit.
4. **A balance is derived from entries and is never stored as a mutable authority.** It may be cached, and the cache is a projection that can be thrown away and rebuilt.
5. Every entry carries the identifier of what caused it: a payment, a card authorisation, a fee, an interest accrual, a return, a sweep.
6. Every posting carries an **effective date** and a **recorded-at instant**, and they differ: a back-dated correction has yesterday's effective date and today's recording.
7. The balance as at a past date is answerable and correct, because that is a question a bank must be able to answer.
8. Two hundred postings arriving at one account at the same instant leave a derived balance equal to the exact arithmetic sum, every time.
9. The ledger's accounts are not the customer's accounts. Several are internal: a customer deposit account per bank account, an in-transit account, fee income, interest expense, a card authorisation hold account, a returns and disputes suspense account, a partner-bank settlement account, an unmatched clearing account and a rounding residual account.
10. **A payment is never a single-entry decrement.** It is a movement from the customer's deposit account to in-transit, and later from in-transit to settlement. That two-stage structure is what makes a return, a failure and a reconciliation representable at all.

### Accounts, balances and holds

1. There are three kinds of account: operating, which carries the working balance; treasury or savings, which bears yield and may sweep; and credit, which is a liability. **A credit account's balance has the opposite sign to a deposit account's**, the list makes that unmistakable in its sign and its label, and no aggregate adds the two together.
2. **Every account has two balances and they are different numbers.** Current is the sum of all posted entries. Available is current minus live holds, minus pending debits, plus funds released by the availability policy.
3. Both are computed. The interface always labels which one it is showing. **Spending is authorised against available, never against current.** A deposit that has not cleared is in current and not in available.
4. A hold reserves value without posting a settled movement: a card authorisation, a pending outbound payment, a legal hold. **A hold is a posting to the hold account, not a flag**, so it is visible in the ledger.
5. Every hold has an expiry, and an expired hold is released by a posting made by a job, not lazily when somebody next reads the account. Advancing past a hold's expiry frees the funds without anything having read the hold first.
6. A hold's release and the settlement it becomes are linked, so the two are never double counted.
7. Interest accrues daily on the day's closing balance using the stated day-count convention, recorded as an entry in fractional minor units carried at higher precision. Capitalisation posts a rounded amount on a stated schedule. **Rounding differences accumulate to the residual ledger account and never disappear**: credited interest plus the residual equals the exactly computed total. The rate is versioned with effective dates, and a rate change mid-period splits the accrual.
8. The sweep program distributes deposits across the two partner banks. The per-bank exposure is tracked and reportable because insurance is per institution, the mechanics are disclosed including which entity holds what, sweep movements are ordinary ledger postings, and **the coverage figure shown on the site is derived from the actual allocation rather than asserted**. A stated figure the allocation does not support is a misrepresentation.

### Payment rails

The single most consequential fact here: these are not interchangeable transports. They differ in speed, finality, reversibility, operating window and cost, and one `send` method that hides the differences will be wrong about all five.

1. The rails and their properties: `internal` is instant, final, not reversible, always open. `ach` takes one to three banking days, is **not** final, is **reversible for days or months**, and runs on banking days against a cutoff. `wire` is same day, final, not reversible except as a request, and runs on banking days against an earlier cutoff. `realtime` completes in seconds, is **irrevocable**, and is open every hour of every day. `cheque` takes days to weeks, is not final, is reversible. `card` settles on clearing and is reversed only through a dispute.
2. **An ACH credit is never reported as complete on submission.** The status vocabulary distinguishes `submitted`, `settled` and `returned`.
3. Funds received by ACH are not immediately available, per the availability policy.
4. A return posts a reversing entry against the returns suspense account. **If the customer has already spent the money the account goes negative, and that is a real, expected, reportable state rather than an error.**
5. Return codes are stored, shown, and drive different behaviour: `account_closed` disables the recipient, `insufficient_funds` does not, and a `notification_of_change` corrects the counterparty's details without failing the payment.
6. A wire is irrevocable once sent, and **the interface says so before the control is pressed, not after**. A recall is a request to the receiving bank which may refuse, and it is never presented as a cancellation. Beneficiary details are validated as far as possible before submission because there is no undo.
7. Real-time payments are irrevocable on acceptance: no recall, no reversal, no chargeback. **There is no banking day on this rail**: a payment at two in the morning on a Sunday that is also a holiday is a normal event, and nothing keyed to a calendar, a batch window or an end-of-day process may gate it. The end-of-day process must handle a balance that moves while it runs, and the books still balance afterwards.
8. Because it is instant and irrevocable, the real-time rail carries **more** checking than the slow ones, not the same: confirmation of the payee, a lower velocity limit than the equivalent ACH payment, and step-up authentication on a first payment to a new recipient.
9. Cutoffs are stored as a local time plus a timezone identifier, never as an offset. The banking calendar is versioned data, loaded rather than written into the code, and it differs by rail. A payment submitted after cutoff is scheduled for the next banking day **and the interface states which date**. A payment scheduled for a non-banking day moves by a stated, configurable rule.
10. Incoming funds are subject to an availability policy stating how much is available immediately, how much on the next banking day, and what triggers an extended hold. Every hold placed under it is explainable to the customer with its reason and its release date.
11. The status vocabulary is rail-aware and its members are exactly `draft`, `pendingApproval`, `approved`, `scheduled`, `submitted`, `settled`, `failed`, `returned`, `cancelled` and `recallRequested`. **`settled` is not terminal: `returned` is reachable from it.** For the ACH rail, `settled` is not reachable until settlement is confirmed.

### Cards

1. Authorisation, clearing and settlement are different events. An authorisation asks whether funds exist and places a hold. A clearing is the merchant claiming the money, possibly days later. Settlement is the money moving.
2. **They are frequently for different amounts.** A restaurant tip clears for more than it authorised. A fuel pump authorises a nominal amount and clears the actual fill. A hotel or car hire authorises incrementally over days. A partial shipment produces several clearings against one authorisation. A cancelled order produces an authorisation that never clears.
3. An authorisation creates a hold, not a posting. A clearing posts the actual amount, releases the hold, and is linked to it.
4. **A clearing that exceeds its authorisation within the permitted margin is normal and must post.** Authorising `4000` minor units and clearing `4800` as a tip posts, releases the hold, and links the two so nothing is counted twice.
5. **A clearing may arrive with no matching authorisation** and must still post, into the unmatched clearing account for investigation, rather than being rejected.
6. An authorisation with no clearing expires on a timer that varies by merchant category, and the hold releases automatically. One expiry for every category either releases a hotel's hold too early or holds a restaurant's money for a week.
7. **The authorisation decision is synchronous and fast.** It is the lowest-latency path in the system, it depends on nothing that can be slow, and spend controls are evaluated inside it, so they have to be cheap to evaluate. Its behaviour when the policy store is unavailable is a declared decision, stand-in approve or decline, recorded as a risk decision rather than left as a default.
8. A dispute has a defined lifecycle: notification, provisional credit where required, evidence, representment, arbitration. **Provisional credit is a real posting** and it is reversed if the dispute is lost. The deadlines are legal, and a missed deadline forfeits the dispute, so the system tracks and surfaces them.
9. **A full card number never enters this system's storage or its logs.** The record holds a token and the last four digits and nothing else.

### Approvals, roles and spend controls

1. Approval policies are data: thresholds, rails, counterparty classes and roles, never code. A payment is evaluated against policy at creation and enters `pendingApproval` where the policy requires it.
2. The seeded policy is version `1`: a payment at or above `1000000` minor units requires `2` approvals, below that `1`.
3. **The initiator cannot approve their own payment**, whatever their role.
4. A payment records the policy version that governed it, and approval and rejection are recorded with the actor, the moment and any note.
5. **A payment whose amount or recipient is changed after approval returns to `pendingApproval`**, or approval means nothing.
6. Spend controls exist per card across five dimensions: amount per transaction, per day and per month; merchant category as an allow or block list; geography; time of day; and counterparty, where a first payment to a new recipient is treated differently. A control's evaluation is deterministic and fast, its decision is logged with the rule that fired, and **the cardholder can see which rule declined their transaction**.

### Compliance and screening

1. Every party is screened against a versioned sanctions list snapshot at onboarding: the business, every beneficial owner and the control person.
2. **Screening repeats on every list update, not only at onboarding.** A party clean against list version `2026-09-01` who appears in version `2026-09-15` has their account blocked and a review raised when that version is loaded.
3. **Payment counterparties are screened too**, not only account holders, and a payment to a listed counterparty is blocked before submission rather than after.
4. Matching is fuzzy and tuned for transliteration, name order and aliases. Exact matching is not screening.
5. A potential match blocks the activity and raises a review. It never warns and proceeds.
6. Every decision, including a dismissal, is recorded with the reviewer and the reason, and every decision names the list version it was made against so a past decision can be reproduced.
7. Transaction monitoring runs against the expected activity captured at onboarding, with rules that are versioned and can be replayed over historical postings before being activated, so nobody has to guess whether a new rule produces five alerts or fifty thousand. Alerts go to a queue with a defined disposition and a deadline the system tracks.
8. **Retention constrains deletion.** An erasure request restricts access and records the reconciliation of the two obligations; the ledger entries, the statements and the audit log survive it. A hard delete would destroy records the institution is required to keep.

### Reconciliation, statements and audit

1. Reconciliation runs daily against the partner bank's file. Every posting is matched to a bank record or becomes a break.
2. Breaks are typed as `timing`, `amount`, `missing` or `unexpected`, are aged, are assigned, and are worked by a person. **Nothing is auto-adjusted to match the bank**, because that destroys the evidence of whatever went wrong. A correction is a new posting with a reason code.
3. The run itself is a record, so "we reconciled on the fifteenth" is provable, and an unreconciled position beyond its threshold age escalates.
4. Where the platform's view and the bank's differ, the customer is shown the conservative figure, which is the lower of the two available balances, and the platform never reports a settled balance it cannot reconcile.
5. **A statement is generated once and stored, never rebuilt on request.** Requesting the same statement twice returns byte-identical content, including after a back-dated correcting entry has landed in that period; the correction appears in the next period or as an addendum. Statements are immutable and retained, and a correction is a new statement or an addendum, never an edit.
6. Categorisation is metadata and **never alters the ledger**. Exports are deterministic, state their basis and are reproducible.
7. Every state change, permission change, policy change and data access is recorded in an append-only, tamper-evident log: each entry carries the fingerprint of the entry before it and its own fingerprint covers every field including that one. Every entry names the actor, and **where the actor is an agent it names the agent and the human who authorised it**. Support access to a customer's record is logged with a reason. The log is queryable and exportable.

### The developer interface, events and agents

1. Every value-moving operation accepts a caller-supplied idempotency key, scoped to the organisation and the operation. A replay returns the **original response**, identical, including the original identifier and status. A replay carrying the same key with **different parameters is an error**, neither a new operation nor a silent replay. The key record is written in the same transaction as the effect, so the lookup and the write are atomic together and a retry cannot slip between them, and keys are retained for at least `24` hours.
2. Money is an integer in the currency's minor unit internally and a **decimal string** on the wire, with the currency travelling beside it. The exponent comes from a currency table. Nothing in a money path is a floating-point number.
3. Identifiers are prefixed and type-tagged: a payment request reads like `preq_01HX4T8A2M9V6RKP` and a recipient like `rcpt_4d82e1af`.
4. Tokens are scoped per resource and per action, with read granted separately from write. Payment-initiating scope is granted separately and is shown as such. Tokens are individually revocable and independently rotatable, and each records its last use and its scopes.
5. Every webhook is signed over the raw body with a timestamp inside the signed payload; the receiver verifies before parsing; replay is prevented by that timestamp plus a nonce inside a bounded window. **Delivery is at least once and ordering is not guaranteed**, both stated to the receiver, so every event carries a sequence and the resource's current state and the receiver acts on the carried state rather than on arrival order. Delivering `settled`, then `returned`, then `settled` again with their original timestamps leaves the payment `returned`. Delivering each of them twice changes nothing.
6. Failed deliveries retry with an increasing backoff and end in a dead-letter path, and the customer can replay events from the log, which is why `events` is a resource: every state change emits an immutable event, ordered per resource, queryable by resource, type and time.
7. Limits are per token and per organisation, documented, and stated in the response with what is left and when it resets. **Payment-initiating operations carry a separate and much lower limit than reads**: `120` read calls a minute against `10` payment-initiating calls a minute. A runaway loop on a read is a bill; a runaway loop on a payment is not.
8. The interface is versioned. A breaking change needs a new version, both run in parallel for a stated period, and the money representation and the status vocabulary are part of the contract, so adding a status is a breaking change.
9. **An agent may propose but not dispose.** Agent credentials are a separate kind, scoped, individually revocable and never a person's own token. Write scopes are granted per resource and per action rather than wholesale. **Every agent-initiated payment enters `pendingApproval` whatever its amount.** Each agent token carries its own velocity limits per transaction, per day and per counterparty. A payment to a new recipient always requires a human approval. Every agent action is attributed to both the agent and its authorising human, and a kill switch revokes the agent without disturbing that human's own access.

### Documents and the object store

1. Every stored document, statement and uploaded attachment lives in **MinIO**, the S3-compatible object store at `STORAGE_ENDPOINT` and `STORAGE_BUCKET`, reached with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. No bytes live on the app's filesystem and no bytes live in a database column.
2. The key scheme is `vault/{kind}/{owner_id}/{sha256_of_bytes}.{ext}`, where `kind` is one of `statement`, `formation`, `receipt` and `export`. A worked example: the `2026-08` statement for the operating account whose identifier is `1` is stored at `vault/statement/1/9f2ab1c4e7d0a5b8c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4.pdf`.
3. Protected content is served **only** through an authenticated streaming endpoint on this origin that checks the caller's membership and role before it reads the object. The bucket is never publicly readable and no pre-signed address is ever handed out.
4. A signed-out caller asking for a statement, a formation document or an export is denied. A member of one organisation asking for another organisation's object is denied, at the streaming endpoint and by any other address.
5. The digest in the key is the digest of the bytes, so the same bytes stored twice produce the same key and a statement's stored content is verifiable against it.

## User flow

The information architecture is one origin carrying four groups of addresses: the public site, the application, the authenticated product and the editorial surface.

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home: hero, feature stack, illustration panels, social proof, footer | public |
| `/pricing` | Every fee, generated from the fee record | public |
| `/products/accounts` | Operating and savings accounts | public |
| `/products/payments` | The rails and what they cost | public |
| `/products/cards` | Debit and credit cards | public |
| `/products/treasury` | Treasury, yield and sweep | public |
| `/products/spend-controls` | Controls and approvals | public |
| `/products/invoicing` | Invoicing | public |
| `/products/capital` | Credit and capital | public |
| `/solutions/stage`, `/solutions/sector`, `/solutions/role` | Solutions by company stage, sector and role | public |
| `/resources/blog`, `/resources/guides`, `/resources/customers` | The blog, the guides, customer stories | public |
| `/faq` | The support library | public |
| `/developers` | The developer reference | public |
| `/about/company`, `/about/careers`, `/about/security` | Company, careers, security | public |
| `/legal/terms`, `/legal/privacy`, `/legal/deposit-agreement`, `/legal/disclosures`, `/legal/fees`, `/legal/complaints`, `/legal/partner-banks` | The legal group | public |
| `/sitemap.xml`, `/robots.txt`, `/favicon.ico` | Sitemap, robots, favicon | public |
| `/apply` | Email capture | public |
| `/apply/business` | Business identity | applicant |
| `/apply/ownership` | Beneficial owners and the control person | applicant |
| `/apply/identity` | Individual identity for each of them | applicant |
| `/apply/documents` | Formation and risk-triggered documents | applicant |
| `/apply/review` | Attestations and the deposit agreement | applicant |
| `/apply/decision` | Approved, declined or referred | applicant |
| `/login`, `/logout` | Sign in and out | public |
| `/app` | Organisation overview: accounts, both balances, what needs attention | member |
| `/app/accounts`, `/app/accounts/<id>` | Accounts and one account's postings | member |
| `/app/transactions` | The transaction table, filterable, categorisable | member |
| `/app/payments`, `/app/payments/<id>` | The payment queue and one payment | member |
| `/app/payments/new` | Raise a payment | Owner, Admin, Initiator |
| `/app/approvals` | What is waiting on this member | Owner, Admin, Approver |
| `/app/recipients`, `/app/recipients/new` | Recipients and their screening state | Owner, Admin, Initiator |
| `/app/cards`, `/app/cards/<id>` | Cards, their controls and their transactions | member |
| `/app/treasury` | Treasury, yield, sweep and per-bank exposure | member |
| `/app/statements` | Statements, and the download that streams from the object store | member |
| `/app/reconciliation` | Runs and open breaks | Owner, Admin, Bookkeeper |
| `/app/audit` | The audit log | Owner |
| `/app/users` | Members and their roles | Owner, Admin |
| `/app/policies` | Approval policy and its versions | Owner |
| `/app/tokens` | Interface tokens and their scopes | Owner |
| `/app/agents` | Agent tokens, their limits and the kill switch | Owner |
| `/studio`, `/studio/pages`, `/studio/pages/new`, `/studio/pages/<id>`, `/studio/faq`, `/studio/fees`, `/studio/footnotes` | The editorial surface | Editor |
| `GET /api/health` | Readiness | public |

**Entry and redirects.** An unauthenticated request for any `/app` or `/studio` address goes to `/login` carrying the address that was asked for, and lands there once signed in. Signing in sends an organisation member to `/app` and the Editor to `/studio`. Signing out returns to `/` and the token stops working. A token that expires part way through an action returns the member to `/login` with nothing written. A member whose role does not reach a route is refused by the server, not merely shown a page without the link. The seven campaign addresses redirect permanently; every other unknown address renders the not-found page and answers not-found.

**Journeys.**

1. A visitor opens `/`, reads the headline and the qualified subhead, types an address into the hero capture and presses `Open account`. At `/apply/business` they give `Meridian Robotics` as the legal name with its entity type, jurisdiction, registration number, formation date, both addresses, tax identifier, classification and expected activity. At `/apply/ownership` they add two owners above the threshold and name one control person. At `/apply/identity` they give each person's details. At `/apply/documents` they upload a formation document, which lands in the object store at its key. At `/apply/review` they accept the deposit agreement and two attestations, and the exact text shown is stored with each acceptance. At `/apply/decision` the application is approved; the organisation exists, one operating account is open at `Northgate Bank`, and its balance is the sum of the balanced opening entries.
2. `initiator@example.com` opens `/app/payments/new`, picks `Meridian Operating`, picks the recipient `Jane Black`, enters an amount, picks the `ach` rail, adds an external memo and submits. The payment is `pendingApproval`. The same member's attempt to approve it is denied and the payment does not move. `approver@example.com` approves it from `/app/approvals`; it becomes `approved`, then `scheduled` for a stated date because the submission was after the ACH cutoff, then `submitted`, then `settled`.
3. An operator delivers a return for that payment five days after settlement with the code `insufficient_funds`. The payment moves from `settled` to `returned`, a reversing posting lands against the returns suspense account, and the operating account's current balance goes negative and is shown as a negative amount with its sign and its label.
4. A card authorisation for `4000` minor units at a restaurant places a hold, and `/app/cards/<id>` shows available lower than current. A clearing for `4800` posts, releases the hold and links to it. A second clearing arrives with no authorisation and posts to the unmatched clearing account.
5. `bookkeeper@example.com` opens `/app/transactions`, categorises a posting, opens `/app/statements` and downloads the `2026-08` statement, which streams from the object store. Every payment control is refused to them by the server.
6. A visitor opens `/faq`, searches, opens the answer about what a wire costs, follows its anchor, then opens `/pricing` and `/legal/fees` and finds the same amount in all three.
7. A visitor opens `/developers`, reads the fifteen resources and their descriptions, and reads the worked request and response whose amounts agree.
8. `editor@example.com` opens `/studio/pages/new`, writes a page and saves it as a draft. A signed-out request for its address is denied and it is in no sitemap. The Editor publishes it; it becomes readable and joins the sitemap.
9. An agent token creates a payment for a small amount. It enters `pendingApproval` regardless, the audit entry names both the agent and `owner@example.com` who authorised it, and the Owner revokes the agent from `/app/agents` without affecting their own access.
10. An operator loads the `2026-09-15` partner-bank file at `/app/reconciliation`. One record does not match. A typed, aged break is raised and assigned, and no posting is made automatically.
11. An operator loads sanctions list version `2026-09-15`. `Viktor Halberd`, previously clean, now matches. The recipient is blocked, a review is raised with the list version recorded, and a payment to that recipient is refused before submission.

**States.** Every list has an empty state naming what would fill it and what to do about it. Every surface that waits says it is waiting. An error never leaves a blank page. The not-found page carries the full chrome, a way back, a route to the support library and a route to a person, because somebody who cannot find a page may be in the middle of a problem with money. **The server-error page never tells a customer to try again.** It tells them to check their transaction list and gives them a route to a person, because a customer who retries a payment they cannot see the outcome of may pay twice.

## UI/UX notes

Somebody arriving at the public site should understand in the first moment that this is a bank for a company that does not want to visit a branch, and should feel that every claim on the page is one the company will stand behind. Somebody inside the product should feel that nothing is hidden and nothing is hurried. Those are the two things every later decision resolves against.

Two registers under one brand, and the tension is resolved by scoping rather than by splitting the difference. The public site is consumer and may carry atmosphere, with the subject itself seen first. The product behind the application is operational: quiet, dense but organised, built for scanning and for repeated action, carrying no oversized hero and no editorial composition anywhere inside it. Comprehension over atmosphere inside the product, and stillness over decoration wherever money moves. A page that is trying to reassure somebody while they authorise a wire has nothing moving on it.

Colour is named by role and by state rather than by hue, and that is the whole system rather than a preference. The page ground is a near-white cool neutral and raised surfaces are a plainer near-white neutral, and the two must stay visibly separate without a shadow being drawn between them. Ink is a deep cool neutral, one step darker again for emphasis, a mid cool neutral for subdued text, and a lighter mid cool neutral for unavailable content, which deliberately sits below the reading bar because it is unavailable. One brand colour, a light vivid blue, carries the primary surface, the primary text, the primary border and the focus ring, with a mid soft blue when it is pointed at and a darker one when it is pressed, and **it is the only thing on any page wearing it**. One further colour, a mid vivid magenta, means an error and appears nowhere else. A state that is neither of those two may not borrow either. The exact shades are yours, so long as those two rules hold.

Three properties make that a system rather than a list, and all three are required. Every role has an inverted twin, so a component drops onto a dark section with no conditional styling and the developer reference can run entirely inverted. Text and icon are parallel ladders with the same roles, addressable separately, so an icon can be tuned without moving text. And the pointed-at and pressed variants are roles of their own, so a component never computes its own hover colour. Change one role and every state that uses it follows.

Typography carries three roles. The interface and the reading text share one variable grotesque, and the interface weight is deliberately a shade heavier than the reading weight at the same size and the same colour, which is what separates the furniture from the content without changing either. The face must be a variable one with a weight axis, or that distinction collapses and the interface loses a layer of hierarchy. A transitional serif with a true italic appears in a handful of display headings and loads late or not at all. A monospace with tabular figures carries amounts, identifiers and code, because a column of money set in proportional digits looks like incompetence on a banking product. Figures line up in a column wherever amounts stack. No font binary is fetched: each role resolves to a face the reader already has installed, so nothing waits on a download and no line of type is briefly invisible.

Leading and tracking are proportions of the size rather than fixed measures, so optical spacing holds as the size changes. The exact families, the exact scale and the exact proportions are yours, so long as the two weights stay distinguishable in the rendered output and amounts stay aligned.

Corners are barely softened, and one small radius is almost the whole interface: the larger softenings are reserved for pills and for section containers, and the navigation trigger is the only fully rounded control. Space is one ladder of steps with named aliases for gaps, stacks and layout padding, and the gap between sections is a small multiple of the gap beneath a heading, roughly halving on a narrow screen. The grid divides evenly into halves, quarters and eighths and not into thirds, so anything three across is a deliberate exception rather than the grid's natural shape. Space over dividers: sections read as separate because of the room around them.

Elevation is extremely soft, because on a near-white interface a shadow's job is to separate rather than to lift. Depth otherwise comes from a small backdrop blur behind the navigation and behind the tiled composition, where each tile frosts what sits behind it. Layering uses a short disciplined set of stacking levels, one of them a long way behind everything for a purely decorative layer, and the navigation declares its own.

Motion is eased. Everything moves on one family of curves at one speed, quick enough not to be waited for and slow enough to be seen, easing off at the end rather than starting sharply, and nothing uses a different speed to feel special. The focus outline changes colour along with everything else rather than snapping while the rest glides. The moments worth naming, because a build that names none of them ships none of them: something entering rises a short distance while fading up, once, then stays arrived; something leaving fades while blurring slightly and something arriving fades while un-blurring, so a change reads as depth of field rather than as transparency; a panel opens with a slight backwards tilt from its top edge as though hinged rather than simply growing; a tab change fades while rising a very short distance; an answer opens against its own measured height rather than a guessed maximum; a ripple spreads and fades from the point of a press and is larger on a wide screen than on a phone; a fine grain drifts across a section ground; a card that has just arrived settles from slightly too large and slightly out of focus into place; a three-card stack crosses, its side cards fading out, passing behind the centre and fading back in on the opposite side; and one celebration only, reserved for a granted application, where notes fall the height of the page, spinning, each at its own transparency so the shower has depth. There is no blanket rule that animates everything, because such a rule quietly animates things nobody intended.

Under a reduced-motion preference every one of those is **replaced by an equivalent static affordance rather than frozen**. A frozen sliding row of names hides half of them, so it becomes a row the reader can scroll instead. The celebration does not run at all. Nothing is left part way. The entrance is the whole of the scroll behaviour and it is one moment repeated across most of the page: one short rise and one fade, arriving together. Scrolling is never taken over: there is no smooth-scroll layer, and every property scrubbed against scroll position is one that does not cause the page to lay out again.

Density is comfortable on the public site and compact inside the product, where a full payment queue and its filters sit on one screen without scrolling to find the controls. The layout archetype is a top navigation: the wordmark on the left, five items centred of which four open panels, and on the right a quiet sign-in control beside the filled primary action. That single pairing is the whole call-to-action hierarchy and it repeats in the hero. Inside the product the same top navigation carries the organisation, and the working surface is a table, because the transactions, the payment queue, the approvals, the ledger entries and the reconciliation breaks are all things somebody scans down a column. **Each page leads with one primary action, visually distinct from every secondary one**, and there is never a second thing competing with it.

A control here is specified by what it does in each of its states rather than by its dimensions. Resting, pointed at, pressed, focused and unavailable are all drawn, and an unavailable control says so by more than its colour. One main action style and one quieter alternative, the main one carrying the strongest contrast on the page. Escape closes any open panel and returns focus to the control that opened it. Destructive and irrevocable actions confirm first, and the irrevocability of a wire is stated before the control is pressed rather than after. Hover treatments are declared only where a pointer exists, and anything that reveals on hover is permanently revealed where there is none, so a tap on a phone never leaves a control stuck looking pressed.

Accessibility is contract and does not vary with any of the above. Body text and its background meet the WCAG AA contrast bar on the light ground and on the inverted one, and large display type meets the large-text bar; the disclosure sits over a generated scene, so it carries a scrim and is checked against the lightest point of what is beneath it rather than the average. One first-rank heading per route. The disclosure is in the accessibility tree and never inside anything collapsed or dismissible. Footnote markers are real references that are announced and can be followed to the footnote and back, never decorative characters, because somebody listening to the page otherwise hears a stray digit and has no route to the qualification, which on a regulated claim is a disclosure failure rather than an inconvenience. Accordions expose their expanded state and work from the keyboard. A visually-hidden idiom is used consistently and it hides labels rather than only spans, so every field carries a real label including the ones sighted readers never see. Unavailable text deliberately fails the contrast bar, and correctly so for disabled content, while white text on the primary surface passes it. Amounts are announced with their currency. Every control is reachable from the keyboard in reading order, and the ring marking the focused one is drawn differently from the pointed-at treatment. Icon-only controls carry a name saying what they do rather than what they depict. No interactive target is smaller than a comfortable fingertip. Every content image carries alternative text and every decorative one declares itself decorative.

The layout is mobile first across six ascending breakpoints, every rule written the same way round, and it holds at every width between them rather than only at the named ones. The widest tier does something deliberate on a very wide display rather than floating a centred column in space. There is exactly one exception to the ascending rule and it is kept: a viewport that is short rather than narrow suppresses the full-height treatment instead of squashing it, which is the laptop case where a full-height hero stops working. At a narrow viewport nothing overflows sideways and every navigation target stays reachable. Where the boundaries fall is yours, so long as the arrangement never breaks between them.

Five failures to design against, and each is a failure rather than a fashion. A page carried by one hue family with no second signal for meaning. Decoration occupying room that content should have. Marketing composition inside the product, where the working interface belongs. A ladder of drop shadows standing in for the soft separation described above. And a numbered marker published with no footnote behind it, which is worse than publishing neither.

## Technical requirements

The stack is fixed. The rendering model is a progressively enhanced multi-page application: every public address and every application step is a real address that returns a complete HTML document, and script adds behaviour to a page that already works without it rather than producing the page. The frontend is **vanilla progressive enhancement**: no client framework, no client-side router and no application shell. The backend is **Flask with Jinja templates**, which renders every document and serves the HTTP API on that same origin under the `/api` prefix. The datastore is **PostgreSQL** at `DATABASE_URL`. The object store is **MinIO** at `STORAGE_ENDPOINT` and `STORAGE_BUCKET`, reached with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The public origin and port are `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read every host, port and credential from the environment and never hardcode one. The backing services named in this brief are already running at those variables.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation.

Auth is app-implemented: email and password exchanged for a bearer token, passwords under a modern memory-hard password hash, tokens expiring, the same token carried in an http-only cookie so a server-rendered page is authorised before any script runs. `GET /api/health` returns `200` once the app is ready.

**The disclosure is in the first paint of every route where a banking capability is claimed.** It is rendered by the server into the document rather than added afterwards, because a page that makes a claim it has not yet qualified is making an unqualified claim for as long as that lasts.

**Every public route carries its own title and its own description, and no two public routes share either.** The site serves a favicon and declares it in the document head. A sitemap lists every published public route and a robots file points at it.

**Every internal link on every public route resolves.** A link to an address that does not answer is a defect the build catches rather than something a reader discovers.

Logs are structured, one line of JSON per request on standard output, carrying the method, the route, the status, the elapsed milliseconds and a request identifier generated at the edge of the request, and that identifier is returned in the body of every error response. **No amount, no account identifier, no card token, no credential and no document content is ever written to a log**, not even temporarily, because a log holding those is a second unmanaged copy of the record.

The reference for the interface is generated from the same schema the service validates requests against, so the published contract and the running service cannot disagree. Versioning is part of that contract: the money representation and the status vocabulary belong to the version, so adding a status is a breaking change for any client that switches exhaustively over it.

Determinism and reproducibility are requirements rather than qualities. Given the ledger and a date, every derived figure must be reproducible exactly: a balance, a statement, an interest accrual. That forbids any computation that depends on the current time, the current rate or the current configuration without recording which were used.

Limits exist on payment amount, on daily and monthly velocity per account and per counterparty, on card authorisation, on request rate, on upload size and on export size. Every one has a default, is configurable, and produces its own specific refusal rather than a generic one.

Published site content is produced by static generation with incremental revalidation: a published page is generated once and refreshed when its record changes, rather than composed again for every visitor.

The performance budgets are stated and are checked. The home route paints its first content quickly on a mid-range laptop over a throttled connection; the disclosure is inside that first paint, always, which is a compliance budget rather than a performance one; the home route's first visit transfers little; the script that runs before first paint is small; the type payload is small because it is subset and consolidated rather than served per route; and the scroll frame budget is sustained rather than met on average.

Analytics are local, are gated on the cookie answer, and never run before the disclosure has painted. No web font binary and no other binary asset is fetched at run time.

The app stays responsive with `250000` ledger entries in one organisation, `50000` postings on one account, `5000` transactions in one statement period and `2` organisations.

## Data model

Thirty-eight tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**Identity and access.** `account` holds `id`, `email` unique and compared case-insensitively, `display_name`, `password_hash`, `status` and `created_at`. `session` holds `id`, `account_id`, `token_hash`, `expires_at` and `created_at`. `organisation` holds `id`, `legal_name`, `trading_name`, `slug` unique, `entity_type`, `formation_jurisdiction`, `registration_number`, `formation_date`, `tax_identifier`, `business_classification`, `registered_address`, `operating_address`, `status` and `created_at`. `membership` holds `id`, `organisation_id`, `account_id`, `role` among `owner`, `admin`, `approver`, `initiator`, `bookkeeper` and `card_only`, and `spend_limit_minor`, unique on the organisation and the account together. `step_up` holds `id`, `account_id`, `action`, `granted_at` and `expires_at`.

**Content.** `page` holds `id`, `route` unique, `title`, `description`, `body`, `state` among `draft` and `published`, `published_at` and `editor_account_id`. `faq_entry` holds `id`, `anchor` unique, `question`, `answer`, `topic`, `fee_code` and `state`. `guide` holds `id`, `slug` unique, `title`, `body` and `state`. `footnote` holds `marker` unique, `claim_key` unique, `text`, `condition` and `as_of_date`. `claim` holds `id`, `key` unique, `surface` and `footnote_marker`. `fee` holds `id`, `code` unique, `name`, `amount_minor`, `currency`, `trigger`, `waiver_condition`, `effective_from` and `effective_to`. `page_view` holds `id`, `route` and `viewed_at`.

**Application.** `application` holds `id`, `email`, `organisation_id` which is absent until approval, `stage`, `decision`, `decision_reason_code`, `referred_at`, `decided_at` and `created_at`. `beneficial_owner` holds `id`, `application_id`, `parent_owner_id` which is absent for a direct owner, `kind` among `person` and `entity`, `legal_name`, `date_of_birth`, `address`, `government_identifier_last4`, `ownership_percent_basis_points` and `is_control_person`; the parent link is what makes the ownership a graph rather than a list. `identity_check` holds `id`, `beneficial_owner_id`, `vendor_reference`, `decision`, `evidence` and `checked_at`. `attestation` holds `id`, `application_id`, `account_id`, `text_shown` and `accepted_at`. `document` holds `id`, `organisation_id`, `kind`, `object_key`, `byte_size`, `digest` and `uploaded_at`.

**Ledger.** `ledger_account` holds `id`, `organisation_id` which is absent for an internal account, `class` among `customer_deposit`, `in_transit`, `fee_income`, `interest_expense`, `card_authorisation_hold`, `returns_suspense`, `partner_bank_settlement`, `unmatched_clearing` and `rounding_residual`, plus `currency`, `partner_bank` and `name`. `posting` holds `id`, `organisation_id`, `cause_kind`, `cause_id`, `effective_date`, `recorded_at` and `memo`. `entry` holds `id`, `posting_id`, `ledger_account_id`, `direction` among `debit` and `credit`, `amount_minor` and `currency`. `balance_cache` holds `ledger_account_id`, `as_of_date`, `current_minor` and `computed_at`, and is a **projection** that may be discarded and rebuilt at any moment. `hold` holds `id`, `ledger_account_id`, `cause_kind`, `cause_id`, `amount_minor`, `placed_at`, `expires_at` and `released_posting_id`. `interest_accrual` holds `id`, `ledger_account_id`, `accrual_date`, `rate_basis_points`, `day_count`, `amount_micro_minor` and `capitalised_posting_id`. `rate_version` holds `id`, `product`, `rate_basis_points`, `day_count` and `effective_from`.

**Accounts and money movement.** `bank_account` holds `id`, `organisation_id`, `kind` among `operating`, `treasury` and `credit`, `name`, `partner_bank`, `ledger_account_id` and `opened_at`. `recipient` holds `id`, `organisation_id`, `external_id` unique, `name`, `rail_details`, `screening_state` and `created_at`. `payment` holds `id`, `external_id` unique, `organisation_id`, `bank_account_id`, `recipient_id`, `amount_minor`, `currency`, `rail` among `internal`, `ach`, `wire`, `realtime`, `cheque` and `card`, `status` among `draft`, `pendingApproval`, `approved`, `scheduled`, `submitted`, `settled`, `failed`, `returned`, `cancelled` and `recallRequested`, plus `external_memo`, `idempotency_key`, `policy_version`, `scheduled_date`, `submitted_at`, `settled_at`, `returned_at`, `return_code` among `insufficient_funds`, `account_closed`, `unauthorised` and `notification_of_change`, `created_by_account_id` and `created_by_agent_id`. `payment_approval` holds `id`, `payment_id`, `approver_account_id`, `decision`, `note` and `decided_at`. `approval_policy` holds `id`, `organisation_id`, `version`, `threshold_minor`, `required_approvals`, `rails`, `counterparty_class` and `effective_from`. `banking_calendar` holds `id`, `rail`, `calendar_date`, `is_banking_day` and `version`. `cutoff` holds `id`, `rail`, `local_time`, `timezone` and `version`, where `timezone` is an identifier such as `America/New_York` and never an offset. `availability_policy` holds `id`, `rail`, `immediate_minor`, `next_day_minor` and `extended_hold_reason`.

**Cards.** `card` holds `id`, `organisation_id`, `account_id`, `bank_account_id`, `token`, `last_four`, `state` and `created_at`, and holds **no** primary account number. `card_authorisation` holds `id`, `card_id`, `amount_minor`, `merchant_category`, `merchant_name`, `hold_id`, `authorised_at`, `expires_at` and `state`. `card_clearing` holds `id`, `card_id`, `authorisation_id` which may be absent, `amount_minor`, `posting_id` and `cleared_at`. `spend_control` holds `id`, `card_id`, `dimension` among `amount`, `merchant_category`, `geography`, `time` and `counterparty`, plus `parameters` and `active`. `dispute` holds `id`, `card_clearing_id`, `state`, `opened_at`, `provisional_credit_posting_id` and `deadline_date`.

**Interface and records.** `api_token` holds `id`, `organisation_id`, `account_id`, `kind` among `user` and `agent`, `prefix`, `token_hash`, `scopes`, `authorising_account_id`, `velocity_per_transaction_minor`, `velocity_per_day_minor`, `velocity_per_counterparty_minor`, `last_used_at` and `revoked_at`. `idempotency_record` holds `id`, `organisation_id`, `operation`, `key`, `request_digest`, `response_body` and `created_at`, unique on the organisation, the operation and the key together. `event` holds `id`, `organisation_id`, `resource_kind`, `resource_id`, `sequence`, `type`, `state_snapshot` and `created_at`, where `sequence` rises by exactly one within a resource. `webhook_endpoint` holds `id`, `organisation_id`, `target_url`, `secret`, `state` and `failing_since`. `webhook_delivery` holds `id`, `webhook_endpoint_id`, `event_id`, `attempt`, `state` and `next_attempt_at`. `statement` holds `id`, `bank_account_id`, `period`, `object_key`, `digest`, `generated_at` and `addendum_of`. `reconciliation_run` holds `id`, `run_date`, `partner_bank`, `matched_count`, `break_count` and `completed_at`. `reconciliation_break` holds `id`, `reconciliation_run_id`, `kind` among `timing`, `amount`, `missing` and `unexpected`, plus `posting_id`, `bank_record_reference`, `amount_minor`, `assigned_to_account_id`, `opened_at` and `resolved_posting_id`. `sanctions_list_version` holds `id`, `version` and `published_at`; `sanctions_entry` holds `id`, `sanctions_list_version_id`, `name` and `aliases`; `screening_result` holds `id`, `subject_kind`, `subject_id`, `sanctions_list_version_id`, `outcome`, `reviewer_account_id`, `reason` and `decided_at`. `monitoring_rule` holds `id`, `version`, `expression` and `active`; `monitoring_alert` holds `id`, `monitoring_rule_id`, `organisation_id`, `subject_id`, `state`, `raised_at`, `disposition` and `due_date`. `audit_entry` holds `id`, `organisation_id`, `actor_account_id`, `actor_agent_id`, `action`, `target_kind`, `target_id`, `reason`, `prev_hash`, `hash` and `created_at`, where `hash` covers every other field including `prev_hash`. `category` holds `id`, `organisation_id` and `name`, and `transaction_category` pairs a posting with a category.

**Which values are derived rather than stored.** A ledger account's current balance is derived from its entries and `balance_cache` is only ever a projection of that derivation. An available balance is derived from the current balance, the live holds and the pending debits. A statement's figures are derived from the ledger as at the statement's close and are then fixed in the stored object. An interest capitalisation amount is derived from the accruals it covers. A page's readability is derived from its `state`. The stated deposit-insurance coverage is derived from the sweep allocation across the two partner banks and is never a stored assertion.

**Money.** Amounts are integers in the currency's minor unit. `$10.00` is `1000`, not `10.00` and not `10`. The exponent comes from a currency table, so it is `2` for `usd` and `0` for a currency with no minor unit. The stored currency code is lowercase, `usd`; the wire representation of an amount is a **decimal string** with an uppercase code beside it, so `1000` is carried as `"amount": "10.00"` with `"currency": "USD"`. No money value is ever a floating-point number, in storage, in transit or in a computation. Rounding is defined per operation and stated, and interest accrual rounds half to even.

**Invariants, as properties of the running system.** Every posting's debits equal its credits. No entry is ever updated or deleted, and an attempt as the application's own database user is refused by the database rather than merely absent from the code. A derived balance equals the exact sum of entries at the requested effective date, under concurrent postings as well as sequential ones. Available never counts a hold twice with the settlement it became. A payment reaches `returned` only from `settled`. One idempotency key within an organisation and operation yields exactly one effect and one stored response; the same key with a different request is refused. An event's sequence rises by exactly one within its resource. An audit entry's fingerprint covers the entry before it, so a rewritten row breaks the chain at that point. A statement's bytes are never rewritten. Credited interest plus the residual account equals the exactly computed total. The two organisations never read each other's rows by any address.

**Seed data.** Two organisations: `Meridian Robotics`, slug `meridian-robotics`, approved, with an operating account `Meridian Operating` at `Northgate Bank`, a treasury account `Meridian Treasury` at `Talbot National` and a credit account `Meridian Card`; and `Calder Textiles`, slug `calder-textiles`, approved, with one operating account `Calder Operating`. Nine accounts as named in `## User roles`. Two recipients on `Meridian Robotics`: `Jane Black` with external id `rcpt_4d82e1af` on the `ach` rail, screened clean against list version `2026-09-01`; and `Viktor Halberd` with external id `rcpt_9c11b7d3`, absent from list version `2026-09-01` and present in version `2026-09-15`. Seven fees effective from `2026-09-01`: `wire_outgoing_domestic` at `1500`, `wire_outgoing_international` at `2500`, `ach_outgoing` at `0`, `realtime_outgoing` at `0`, `cheque_outgoing` at `150`, `card_replacement` at `500` and `monthly_maintenance` at `0`, all in `usd`. Eight published pages and one draft page titled `Treasury sweep explained` at `/products/treasury-sweep`, which is not publicly readable. Six published support answers, of which the one anchored `what-does-a-wire-cost` states its amount from the `wire_outgoing_domestic` fee. Seven footnotes numbered `1` through `7` as listed in `## Core features`. One approval policy at version `1` with a threshold of `1000000` minor units and `2` required approvals above it. One rate version at `420` basis points, day count `365`, effective `2026-09-01`. A banking calendar for `2026` in which `2026-11-26` and `2026-12-25` are not banking days for `ach` and `wire` and every day is a banking day for `realtime`. Cutoffs of `16:30` for `ach` and `15:00` for `wire`, both in `America/New_York`. Card hold expiries by merchant category: `restaurant` after `2` days, `hotel` after `31` days, and `7` days otherwise. One statement for `Meridian Operating` for period `2026-08`, stored in the object store at its key. One partner-bank file for `2026-09-15` carrying one record that matches no posting. The site's stated application duration is `10` minutes, its stated yield rate is `4.20%` as of `2026-09-01`, its stated customer count is `200,000`, and its per-institution insured limit is `25000000` minor units, from which the coverage figure on the page is computed rather than typed.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual and structural detail that `## UI/UX notes` states as intent. Everything here is a requirement on what a reader sees, never a value to copy: no colour is given as a code, no space as a measurement, no type as a size and no motion as a timing.

### Modules

The component architecture is ten modules and two of them are unusual. The token layer; the surface state machine behind every interactive background; the accordion shared by the home rows and the support library; the mega-menu, in four instances; the disclosure module, which emits a marker and its footnote from one record; the entrance; the crossing card carousel; the grain overlay; the terminal panel on the developer reference; and the money display. The last two of those are described in their own sections below because each carries a rule the rest of the product depends on.

### The token layer

One token layer, defined once at the root and consumed everywhere. Colour is declared by **role and state** rather than by hue, and that is what makes it a system: there is no "light grey", there is the colour of a surface, the colour of a surface when it is pointed at, and the colour of a surface when it is pressed. The families are surfaces, text, icon, border, radius, spacing, type and easing.

Every role has an **inverted twin**, so a dark section is the same roles with the inverted variant applied rather than a second theme. Text and icon are declared as parallel ladders with identical roles so an icon can be tuned without moving text. Changing one role moves every state that uses it, and a component never computes a hover colour for itself.

### Palette, by role

Every colour below is a role with its family, tone and shade. No code appears anywhere in this build.

| Role | The colour |
|---|---|
| The default page surface | a near-white cool neutral |
| That surface, pointed at | one step deeper in the same neutral |
| That surface, pressed | a light cool neutral |
| An elevated surface | a near-white neutral, plainer than the ground |
| An elevated surface, pointed at and pressed | two steps of the same neutral, in order |
| An input surface | a near-white neutral, with plain white when pointed at and the page ground when unavailable |
| The inverted ground | a deep cool neutral |
| The primary surface, and the primary action | a light, vivid blue |
| The primary action, pointed at | a mid, soft blue |
| The primary action, pressed | a darker mid, soft blue |
| The primary action, unavailable | a mid cool neutral |
| An emphasised surface | the primary colour at three low strengths, for resting, pointed-at and pressed |
| A frosted surface | a cool neutral at three low strengths, in the same order |
| Default text and icon | a deep cool neutral |
| Emphasised text and icon | one step darker again |
| Subdued text and icon | a mid cool neutral |
| Unavailable text and icon | a lighter mid cool neutral |
| Primary text and icon | the brand blue |
| Error text, icon and border | a mid, vivid magenta |
| Text on the primary surface | plain white |
| Default, emphasised and subdued text inverted | a near-white neutral, a plainer near-white neutral, and a light cool neutral |
| Default, emphasised and subdued borders | a mid cool neutral, a deep cool neutral, and a light cool neutral |
| The primary border and the focus ring | the brand blue |
| The input and frosted borders | a cool neutral at a low strength |

The brand blue and the error magenta are the only two hues in the semantic layer. The ramps underneath are raw material and are never used directly. The scrim over the hero scene is a dark wash strongest at the foot and clearing by the top, which is what keeps the disclosure and the headline legible over it.

### Type

Three roles and no fourth.

- **Interface and reading.** One variable grotesque with a weight axis, at two weights that differ by a small amount on that axis. The heavier of the two carries interface chrome and the lighter carries reading text, at the same size and the same colour, and the difference is doing real work: it separates furniture from content without changing anything else. It is invisible unless looked for and its absence costs the interface a layer of hierarchy.
- **Display.** A transitional serif with a true italic, used in a handful of headings and nowhere else. It loads late or not at all.
- **Amounts and code.** Any freely licensed monospace with **tabular figures**, used for amounts, identifiers, keys and code, and for nothing else. Proportional digits make a column of money unreadable.

The reference's three commercially licensed families are not available and are not to be reproduced; each role is satisfied by a freely licensed equivalent or by a face the system already has. Type is subset and consolidated rather than served per route and per weight.

Each role ends in a face the reader's system already has, and no font binary is fetched, so there is no loading phase, no swap and no period of invisible text. Leading and tracking are proportions of the size so optical spacing holds as the size changes.

### Iconography

Every icon is drawn geometry rather than an image file or an icon font, which is what lets this build ship no binary. Icons inherit the icon ladder rather than the text ladder, which is why the two exist separately. Stroke weight is uniform across the whole set. The set is: a chevron in four rotations, a close mark, a search mark, an external-link mark, a check, a plus, a minus, an arrow in four rotations, a download mark, a filter mark, a calendar, a card, a bank, a person, a settings mark and a disclosure caret. An icon is decorative and hidden from assistive technology unless it is the only content of a control, in which case it carries a name saying what it does rather than what it depicts.

**Where a drawing carries internal clipping or blur references, those references are made unique per instance.** Two copies of the same drawing on one page that both declare the same internal identifier collide, and one of them renders wrong. It is the most common fault in exported artwork and it is cheap to prevent and slow to diagnose.

The wordmark is not artwork here. It is a small circular emblem of concentric rings drawn as strokes, beside the product name set in capitals at the light end of the weight axis with generous letterspacing. **The letterspacing is the identity**: a seven-letter word in light, widely spaced capitals beside a small circular emblem reads as an institution rather than as a startup, which for a product holding a company's money is the entire point. The letterspaced form is written `A U R E L I A`.

### Global chrome

**The announcement bar** sits above the header, carries a clock mark, the message `Real-time payments are here - instant, free, 24/7/365.` and a `Learn more` link, and is dismissible. Both `instant` and `free` in that sentence are product claims about a payment rail and carry their markers like any other claim.

**The header** sits below it, carrying the wordmark on the left, the five items `Products`, `Solutions`, `Resources`, `About` and `Pricing` centred, and on the right `Log in` as a bare control beside `Open account` as the filled primary. Four of the five items open panels. One hover treatment serves the whole navigation: the trigger's background fills with the brand colour at a low strength, the same everywhere.

Any layout computed against the height of the screen is computed against the **dynamic** viewport height minus the header, so a phone whose address bar slides away does not overflow.

**The mega-menus.** Four of the five navigation items open one. The panels are square across the top and rounded at the bottom, which is what makes them read as descending from the header rather than floating below it. They size themselves to their own content. Their inner content sits on its own rounded surface. Opening one is the hinged tilt described above; a closed panel is transparent rather than removed. They are keyboard-operable and expose their state.

**The footer** carries the product, solutions, resources and company groups, the legal group, the language control and the persistent disclosure.

**The cookie bar** is anchored to the foot of the page and is never a modal, because a modal on a financial product's landing page is both a conversion cost and, where an equally easy reject path is required, a compliance risk. Dismissing it re-seats the disclosure rather than leaving a gap, and a divider beside the disclosure fades out with it.

**The skip link** is the first focusable element in the document, is parked above the top of the viewport, becomes visible on focus and targets the main landmark.

### The disclosure and the footnote layer

The disclosure bar is carried on every route where a banking capability is claimed, sits at the foot of that route's first screen, is inside the document the server returned, and reads exactly:

`Aurelia is a fintech company, not an FDIC-insured bank. Banking services provided through Northgate Bank and Talbot National, Members FDIC.`

Its position is computed from the actual heights of whatever chrome sits below it, so it is never overlapped by the cookie bar, the announcement bar or anything else, and it never scrolls underneath one.

A claim and its marker are one component: it is given a claim key and it emits both the raised marker and the footnote entry, from one record, so a claim cannot be published without its qualification. The marker is a real reference. The footnote states the condition, the qualification and the date.

### The money display

One component displays an amount, and it is the one part of the site that shares a rule with the platform.

- It receives an integer minor amount and a currency, never a formatted string.
- It formats for the reader's locale and names the currency unambiguously.
- **It never performs arithmetic.** The moment the browser adds two amounts there are two calculators in the system and eventually they disagree about what somebody owes.
- It renders a negative amount explicitly and never by colour alone.
- It uses tabular figures, so a column of amounts lines up.

### The home page

The hero carries the headline `Radically different banking` set over a full-bleed generated scene with the type reversed over it, the subhead `Apply online in 10 minutes to experience banking¹ unlike anything that's come before.`, an email field labelled `Enter your email` with `Open account` inline inside it, `Launch demo` as the quieter alternative, and the disclosure at its foot over the image. **The inline capture is the conversion mechanism**: one field, one control, and everything else happens afterwards. Note that the marker in the subhead qualifies the word `banking` itself, which is exactly what the disclosure layer exists for.

Below it the feature stack is a two-column arrangement: a heading, a column of rows that expand one at a time with the first open, and an illustration panel beside them. The heading is `Get started fast. And never stop moving.`. The rows are `Apply online in 10 minutes` with the body `Free checking and savings accounts - no in-person visits or paperwork.`, then `Get a credit card instantly⁴`, then `Tackle banking tasks in seconds`. The closed rows show their titles separated by hairlines in the subdued border role, and the open row carries a dot in the primary colour.

The imagery is generated rather than photographed. The illustration panels are wide generated fields carrying a fine grain and a gradient scrim. **The grain is generated by the browser from a turbulence filter rather than being an image file**, which is a complete implementation that needs no substitution at all.

Then a customer logo row, a product tour, a comparison table, a testimonial carousel using the crossing three-card stack, a perks block, and the footer.

### The developer reference

It runs on the inverted ground, which is the first real use of the inverted twins and the proof they are a mechanism rather than a declaration. The headline is `Programmable finances for developers & agents`, the subhead is `Automate your financial operations with a full banking¹ API, terminal-native CLI, and AI-ready MCP server.`, the primary action is `Get your API token` and the quieter one is `Open account`.

Below it the resource index lists the fifteen resources and their descriptions, and a terminal panel renders a worked request and its response. The command-line block is headed `Use the Aurelia CLI to run your finances from your terminal` with the control `Install CLI` and three points: `Run Aurelia operations from your terminal, a script, or a CI pipeline`; `Human-readable output, structured for piping, scripting, and LLM consumption`; and `Write actions such as making payments, categorizing transactions, creating invoices, and uploading receipts`.

### The support library and the legal pages

The support library is accordion groups by topic sharing the home page's accordion. **Height animation measures the content rather than guessing it**: a fixed maximum either clips a long answer or makes a short one crawl open. Every answer has a stable anchor.

The legal pages carry the plain chrome on the light ground, body type on comfortable leading, and **no motion of any kind**, which is correct. The measure is capped so a line never runs far beyond a comfortable reading width at any screen size, because an uncapped legal document on a wide monitor is genuinely hard to read and is exactly the kind of document people give up on.

### The error pages

The not-found page is a designed page rather than an apology, and more people will see it than will see the legal set. It carries the full chrome, a display headline, a short body, and three routes out: the support library, the status page and a route to a person. It answers not-found.

The server-error page carries the title `500: Internal Server Error`. Its body **must not say to try again**. It says to check the transaction list and gives a route to a person, because on a payments product a customer who follows "please try again" may pay twice and cannot know whether they have.

### The application flow

One address per step, each reachable by its own address and each returning a complete document. The review step shows the exact text of every attestation and every disclosure on the page where it is accepted, because that exact text is what is stored. The decision step is the only place in the product where the celebration runs.

### The product surfaces

The working surface is a table: the transactions, the payment queue, the approvals queue, the ledger entries, the reconciliation breaks and the audit log. Every one of them shows an amount in the money display, aligns its figures, and states in its own header which balance a balance column is. A row's status is a word as well as a colour. A negative balance is shown with its sign and its label and is never rendered as an absence.

Raising a payment is a dedicated address rather than a panel over the queue, and so is adding a recipient, because both take a step-up grant and neither should be possible to lose by pressing Escape. Every outcome is an inline banner in the page the server returned, above the surface it changed, naming what happened and, where a date was chosen for the customer, which date.

### Copy

Every string below is pinned.

| Where | String |
|---|---|
| Home title | `Online Business Banking For Startups, Small Businesses & Scaling Companies` |
| Title pattern | `Aurelia \| Online Business Banking For Startups & Small Businesses` |
| Developer reference title | `Full Banking API, Terminal-Native CLI & AI-Ready MCP Server \| Aurelia` |
| Support library title | `FAQs \| Pricing, Moving Your Money & More \| Aurelia` |
| Server-error title | `500: Internal Server Error` |
| Wordmark | `A U R E L I A` |
| Announcement | `Real-time payments are here - instant, free, 24/7/365.` with `Learn more` |
| Navigation | `Products`, `Solutions`, `Resources`, `About`, `Pricing` |
| Right cluster | `Log in`, `Open account` |
| Persistent disclosure | `Aurelia is a fintech company, not an FDIC-insured bank. Banking services provided through Northgate Bank and Talbot National, Members FDIC.` |
| Hero headline | `Radically different banking` |
| Hero subhead | `Apply online in 10 minutes to experience banking¹ unlike anything that's come before.` |
| Hero field | `Enter your email` |
| Hero primary | `Open account` |
| Hero secondary | `Launch demo` |
| Feature heading | `Get started fast. And never stop moving.` |
| Feature one | `Apply online in 10 minutes` with `Free checking and savings accounts - no in-person visits or paperwork.` |
| Feature two | `Get a credit card instantly⁴` |
| Feature three | `Tackle banking tasks in seconds` |
| Developer headline | `Programmable finances for developers & agents` |
| Developer subhead | `Automate your financial operations with a full banking¹ API, terminal-native CLI, and AI-ready MCP server.` |
| Developer primary | `Get your API token` |
| Developer secondary | `Open account` |
| CLI heading | `Use the Aurelia CLI to run your finances from your terminal` |
| CLI control | `Install CLI` |
| CLI point one | `Run Aurelia operations from your terminal, a script, or a CI pipeline` |
| CLI point two | `Human-readable output, structured for piping, scripting, and LLM consumption` |
| CLI point three | `Write actions such as making payments, categorizing transactions, creating invoices, and uploading receipts` |
| Skip link | `Skip to main content` |

The disclosure sentence is reproduced exactly and is never rewritten for tone. The footnote text, the support answers and the legal documents are Aurelia's own to write: a qualification that is not true of this product is worse than no qualification, and another institution's deposit agreement is not text to copy.

## Constraints

- One product, two surfaces, one origin. No second origin for assets or for anything else.
- No real-time audio or video of any kind.
- No real partner-bank connection, card processor, card network, identity vendor, sanctions vendor, content host or measurement vendor. Each is modelled inside this app against seeded data and operator actions, and no request leaves this origin at run time.
- No card primary account numbers anywhere: not in storage, not in a log, not in a response. The record holds a token and the last four digits.
- No real money moves. Settlement, return, clearing, the partner-bank file and the sanctions list version are all operator actions inside the app.
- No mobile application and no desktop application; the download actions describe builds rather than serving them.
- No second database, cache, queue, object store, identity provider or mail vendor. No email is sent by this app and no mail server is available to it.
- No binary asset of any kind: no image file, no video file, no audio file, no font binary, no vector-animation file, no raster photography and no streaming media manifest. Every scene, every illustration, every grain field and the favicon are generated. The photographic hero the reference used would be a commissioned photograph; a generated atmospheric field stands in for it and holds the layout, and the difference is real and is accepted.
- No smooth-scroll layer, and no blanket rule that transitions every property.
- No comments, no likes, no messaging, no social graph and no third-party analytics.
- The app stays responsive with `250000` ledger entries in one organisation, `50000` postings on one account, `5000` transactions in one statement period and `2` organisations.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `display_name` | the account and a bearer token |
| `POST /api/auth/login` | `email`, `password` | a bearer token and its expiry |
| `POST /api/auth/step-up` | `password`, `action` | a short-lived grant scoped to that action |
| `POST /api/applications` | `email` | the application and its first stage |
| `PATCH /api/applications/<id>` | the stage's fields | the application at its next stage |
| `POST /api/applications/<id>/owners` | `legal_name`, `kind`, `parent_owner_id`, `ownership_percent_basis_points`, `is_control_person` | the ownership graph |
| `POST /api/applications/<id>/documents` | the document bytes and its `kind` | the stored object's key and digest |
| `POST /api/applications/<id>/attestations` | `text_shown` | the acceptance with its moment |
| `POST /api/applications/<id>/submit` | | the decision, and on approval the organisation and its opening account |
| `GET /api/org` | | the organisation's own details |
| `GET /api/accounts` | | a top-level JSON array of accounts, each with its current and available balances |
| `GET /api/accounts/<id>/balance` | `as_of` | the balances as at that effective date |
| `GET /api/transactions` | `account_id`, `from`, `to`, `cursor`, `limit` | a top-level JSON array of postings with their entries |
| `PATCH /api/transactions/<posting_id>` | `category_id` | the posting with its category, the ledger unchanged |
| `POST /api/payments` | `account_id`, `recipient_id`, `amount`, `currency`, `payment_method`, `external_memo`, and an `Idempotency-Key` header | the payment, with `status` and a decimal-string `amount` |
| `GET /api/payments` | `status`, `cursor`, `limit` | a top-level JSON array of payments |
| `POST /api/payments/<id>/approve` | `note` | the payment with its approval recorded, or a refusal |
| `POST /api/payments/<id>/reject` | `note` | the payment rejected |
| `PATCH /api/payments/<id>` | `amount` or `recipient_id` | the payment returned to `pendingApproval` |
| `POST /api/payments/<id>/recall` | | a recall request, never a cancellation |
| `GET /api/recipients` | | a top-level JSON array of recipients with their screening state |
| `POST /api/recipients` | `name`, `rail_details` | the recipient, subject to a step-up grant and to screening |
| `GET /api/cards` | | a top-level JSON array of cards, each with its token and last four digits |
| `POST /api/cards/<id>/authorisations` | `amount`, `merchant_category`, `merchant_name` | the decision and, when approved, the hold |
| `POST /api/cards/<id>/clearings` | `amount`, `authorisation_id` which may be absent | the posting, and the hold it released |
| `GET /api/treasury` | | the treasury accounts, the per-bank exposure and the derived coverage figure |
| `GET /api/statements` | | a top-level JSON array of statements with their periods |
| `GET /api/statements/<id>/content` | | the stored object streamed, for an entitled caller only |
| `GET /api/documents/<id>/content` | | the stored object streamed, for an entitled caller only |
| `GET /api/reconciliation` | `run_date` | the run, its counts and its open breaks |
| `GET /api/audit` | `cursor`, `limit` | a top-level JSON array of entries, each carrying its chain fingerprints |
| `GET /api/events` | `after`, `resource_kind`, `type` | the events after that sequence, with each resource's current state |
| `GET /api/fees` | | a top-level JSON array of fee records, the one source the site renders from |
| `POST /api/tokens` | `scopes`, `kind` | the token once, its prefix and its scopes |
| `DELETE /api/tokens/<id>` | | the token revoked |
| `POST /api/webhooks` | `target_url` | the endpoint and its signing secret once |
| `POST /api/hooks/partner-bank` | the partner-bank event, signed | accepted, acted on by carried state rather than arrival order |
| `GET /api/health` | | readiness |

Bearer auth is required on everything except signup, login, health, the application endpoints before approval, and the public site's own routes. The webhook receiver authenticates by signature and never by a member's token. A successful call returns the named resource or shape, and an invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success.

### No mocks

The object store is not simulated. Bytes on the app container's filesystem, a base64 column in PostgreSQL, a statement rebuilt from the ledger each time it is asked for, or a `{"stored": true}` the app returns to itself are each a contract violation however good the interface looks. The same holds for the datastore: rows held in a process rather than in PostgreSQL disappear when the app restarts, and a ledger assembled from a module-level list is not a ledger. **MinIO and PostgreSQL are the fact: this app's own screens and its own tables can only reflect what lives in them, never substitute for them.**

## Definition of done

A stranger can read the home page, apply, be approved, and sign in to an organisation whose operating account balance is the sum of balanced, append-only entries. An initiator's payment waits for somebody else to approve it, and editing its amount afterwards sends it back to waiting. An ACH credit that settled a week ago can still come back, and the account it came out of goes negative rather than the money vanishing. A statement downloaded twice is byte-identical, and it streams from the object store rather than being redrawn. Every claim on the site carries a marker that leads to a footnote, and the price of a wire is the same on the pricing page, in the fee schedule and in the support answer.
