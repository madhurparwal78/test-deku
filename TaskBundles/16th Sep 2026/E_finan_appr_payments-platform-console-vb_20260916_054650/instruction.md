# Nimbus Payments Platform Console

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, sign in as a
support operator of Northbeam Retail, attempt to refund a payment of two lakh rupees,
watch that attempt turn into a request that moves no money, sign in again as the finance
operator, approve it, and see the account's available balance fall by exactly that amount,
once, without hitting an error page. A different stranger signed in as the same support
operator must NOT be able to approve that request by any means, and must not be able to
read a single row belonging to Wellspring Studios. Neither guarantee can be arranged in the
interface: the refund must exist as a real row in PostgreSQL with matching ledger entries
that sum to zero, and a request that has been approved twice must still have produced
exactly one refund.

## Overview

Nimbus is a payments and financial infrastructure platform for businesses operating in
India. It is two surfaces joined at the hip, built and served as one application.

The regulatory posture implied by an India-specific storefront with per-country availability
is part of the product rather than a configuration constant: what a product costs, whether it
is sold at all, and how an amount is written are all properties of the country being served.

The **storefront** is the public half. It explains each product, quotes pricing in rupees,
publishes guides and customer stories, gates one product behind a country availability
badge, and routes a visitor to either a self-serve signup or a sales conversation. It is
readable by anyone who wanders in, it writes exactly one thing, and that one thing is a
sales lead.

The **console** is the authenticated half the storefront is selling. An organisation's team
members sign in, choose which organisation they are working as, and operate that
organisation's money: watching payments settle, refunding them, contesting disputes,
reviewing payouts, configuring webhook endpoints and API keys, and deciding which of their
own colleagues may do each of those things. Every console row exists in one of two
environments, `sandbox` or `live`, and the two never meet.

The account here is not a person. It is an organisation, and the staff of an organisation
are not equal. A support agent may hand back a small amount of money without asking anyone.
The same agent may not hand back two lakh rupees on their own, and the system does not
merely refuse: it turns the attempt into a **refund request** that a second person decides.
That is the genuinely hard part. Between the request being raised and the decision being
taken, **nothing at all happens**: no ledger entry, no reservation, no change to any
balance. A build that sets funds aside at request time hands any support agent a way to
freeze their employer's balance with no privilege beyond the one they already have.

What this deliberately is not: there is no card issuing, no lending, no carbon purchasing,
no connected accounts or marketplace money flows, no subscriptions, no invoices, no usage
meters, no query workspace, no exports, no federated single sign-on, no email and no
outbound webhook delivery. Endpoints are configured here; they are never called.

## User roles

Three roles, and a person may hold a membership in more than one organisation. Signup is
closed: accounts and memberships are seeded and there is no self-registration anywhere in
the console.

| Role | Can read | Can write |
|---|---|---|
| `support` | Payments, customers, disputes, refunds and approval requests of the organisations they are a member of, in both environments | Create a refund at or below their ceiling of `500000` paise; raise a refund request above it; withdraw a request they raised. **Cannot approve or reject any request, including their own. Cannot read or create API credentials. Cannot read or create webhook endpoints. Cannot read the audit log. Cannot change a member's role.** |
| `finance` | Everything `support` reads, plus balances, ledger entries and payouts | Create a refund of any amount; approve or reject a refund request another person raised. **Cannot approve a request they raised themselves. Cannot read or create API credentials. Cannot read or create webhook endpoints. Cannot change a member's role.** |
| `administrator` | Everything `finance` reads, plus members, roles, API credentials, webhook endpoints and the audit log | Invite a member, change a member's role, create and revoke an API credential, create and disable a webhook endpoint. **Cannot create a refund. Cannot approve or reject a refund request.** The person who decides who may move money does not move it. |
| anonymous visitor | Every storefront route | Submit the lead form, and nothing else. **Cannot reach any account data by any address.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `support` session to any
`finance`-only endpoint must be rejected by the server (an unauthorized request is denied,
not served), leaving the protected state unchanged.

Two further rules sit on top of the role, and both are about the particular thing in front
of the caller rather than the kind of person they are. A refund is permitted only when its
amount is at or below the caller's own ceiling. A request is approvable only by somebody
who is not the person who raised it. Where a permit rule and a deny rule both match, the
deny wins, every time.

Seeded accounts, all with the password `deku-demo-pw-2026`:

| Email | Name | Organisation | Role |
|---|---|---|---|
| `support@example.com` | Asha Rao | `northbeam` | `support` |
| `finance@example.com` | Kiran Mathew | `northbeam` and `wellspring` | `finance` |
| `admin@example.com` | Devika Nair | `northbeam` | `administrator` |
| `support2@example.com` | Damian Mueller | `wellspring` | `support` |

## Core features

### Auth and the account boundary

1. `POST /api/auth/login` takes `email` and `password`, checks them against the Keycloak
   realm named in `AUTH_REALM` at `AUTH_URL` using `AUTH_CLIENT_ID` and
   `AUTH_CLIENT_SECRET`, and returns a bearer `access_token` the client sends as
   `Authorization: Bearer <token>`. A wrong password is refused. An email that is not
   seeded is refused with the same response and no hint that the address is unknown.
2. The token is a ticket, not a badge of office. It carries nothing the server trusts about
   what the caller may do. Role, ceiling and membership are read from PostgreSQL on every
   single request, so a role changed now takes effect on the next request rather than when
   a token happens to expire.
3. `GET /api/me` returns the signed-in person and every membership they hold, each naming
   its organisation and role. A caller with no token is denied.
4. `GET /api/accounts` returns only the organisations the caller is a member of.
   `support@example.com` sees exactly one. `finance@example.com` sees exactly two.
5. Every console address carries its organisation as a path segment, and the organisation
   is resolved from that segment and re-authorised on every request. It is never taken from
   the session, from a cached context or from a value the client sends in a body. A member
   of `northbeam` asking for anything under `wellspring` is answered as though the record
   does not exist, because telling them it exists is itself a disclosure.
6. There is no signup endpoint, no password reset and no second identity provider anywhere
   in this application.

### Environments

7. Every console record carries an `environment` of `sandbox` or `live`. Reads take
   `?environment=sandbox` or `?environment=live`; when the parameter is absent the
   environment is `live`.
8. A read in one environment never returns a row from the other. Asking for the identifier
   of a `sandbox` payment while reading `live` is answered as not found, never as
   forbidden: answering forbidden confirms the record exists.
9. No operation reads from one environment and writes to the other.

### Payments

10. `GET /api/accounts/{account}/payments` returns a JSON array of that organisation's
    payments in the requested environment, newest first, walked with an opaque cursor
    rather than a page number. A payment carries `id`, `customer_name`, `amount_minor`,
    `currency`, `fee_minor`, `refunded_minor`, `status`, `instrument_brand`,
    `instrument_last_four` and `captured_at`.
11. `refunded_minor` is computed on read from the payment's non-failed refunds. It is never
    a stored running total that a second code path could forget to update.
12. `status` is one of `succeeded`, `partially_refunded`, `refunded` or `disputed`, spelled
    exactly.
13. `GET /api/accounts/{account}/payments/{payment_id}` returns one payment. An identifier
    from another organisation, or from the other environment, is answered as not found.

### Refunds, the ceiling, and the request

This is the spine of the product.

14. `POST /api/accounts/{account}/payments/{payment_id}/refunds` takes `amount_minor`,
    `currency` and `reason`, and carries an `Idempotency-Key` request header. The console
    generates that key when the refund composer is **rendered**, not when it is submitted,
    so a double-click, a retried request after a timeout and a browser back-and-resubmit
    are all one operation.
15. When `amount_minor` is at or below the caller's refund ceiling, the refund executes at
    once: a `refund` row is written, a ledger transaction debits `available` and credits
    `settlement` by exactly `amount_minor`, and the payment's status moves to
    `partially_refunded` or, when the whole captured amount is now refunded, `refunded`.
16. When `amount_minor` is above the caller's ceiling, **no refund is created**. The
    response is a rejection carrying the code `approval_required`, and the caller is offered
    the request path instead. The console shows the inline notice
    `This is above your refund limit of {amount}. Request approval instead.` with the
    caller's own ceiling rendered into it.
17. `POST /api/accounts/{account}/payments/{payment_id}/refund-requests` takes
    `amount_minor`, `currency`, `reason` and a `justification` that is mandatory and is
    shown to whoever decides it. It creates an `approval_request` in state
    `pending_approval` with `operation_class` of `refund_above_ceiling` and an `expires_at`
    of now plus the number of seconds in `REFUND_REQUEST_TTL_SEC`.
18. **A pending request holds nothing.** No refund row, no ledger entry, no reservation, no
    change to any balance, and no outbound call. Reading every balance of the organisation
    immediately after a request is raised must return exactly the same figures as reading
    them immediately before.
19. `GET /api/accounts/{account}/approval-requests` returns the organisation's requests,
    soonest to expire first, each carrying `id`, `payment_id`, `amount_minor`,
    `justification`, `state`, `requested_by`, `requested_at` and `expires_at`.
20. `POST /api/accounts/{account}/approval-requests/{id}/approve` takes an optional `note`.
    It is permitted only for a caller holding `finance` on that organisation who is **not**
    the person who raised it. A `support` caller is denied and the request's state is
    unchanged. The raiser is denied with the code `self_approval_forbidden` and the
    request's state is unchanged. In the console the approve control is **absent** on a
    request the viewer raised, not present and refusing.
21. An approval executes the refund under the idempotency key the request was created with,
    and moves the request to `executed`, recording `decided_by`, `decided_at` and the
    resulting `refund_id`. Approving an already-executed request counts once: it produces no
    second refund, no second ledger transaction and no second movement of the balance, and
    the caller is shown the outcome rather than an error.
21a. `POST /api/accounts/{account}/approval-requests/{id}/reject` takes a `note` that is
    mandatory, moves the request to `rejected`, and writes no refund.
21b. `POST /api/accounts/{account}/approval-requests/{id}/withdraw` moves a
    `pending_approval` request to `withdrawn`, and only the requester who raised it may
    call it. Anybody else is denied and the state is unchanged.
22. A request whose `expires_at` has passed is `expired` the next time it is read or acted
    upon. Approving an expired request is refused with the code `approval_expired` and
    writes no refund. There is no background job: expiry is computed when the row is
    looked at.
23. A refund of more than the payment's remaining refundable amount is refused with the code
    `amount_too_large`, and the message names the remainder. The remainder is the captured
    amount less the sum of that payment's non-failed refunds.
24. A refund of a payment whose status is `disputed` is refused with the code
    `payment_disputed`, at both the direct path and the request path, because refunding a
    disputed payment usually results in paying twice.
25. Concurrency and ordering, stated as what must hold rather than how to hold it.
    Two approvals of one request arriving at the same instant must not both take effect.
    Exactly one wins and writes the refund; the other is answered with the outcome of the
    first and writes nothing. The sum of non-failed refunds for a payment never exceeds
    that payment's captured amount, under simultaneous requests against the running system.
26. Replaying an `Idempotency-Key` with an identical body returns the stored response and
    creates nothing new. Replaying the same key with a different body is refused with the
    code `idempotency_conflict`. Keys are scoped to the organisation, the environment and
    the endpoint, and are retained twenty-four hours.
27. Every rejection above leaves the underlying rows byte-for-byte unchanged. A failed
    refund leaves no partial state: no orphan row, no half-written transaction, no balance
    moved and then moved back.

### Balances, the ledger and payouts

28. Money is an append-only, double-entry ledger. There is no balance column that is
    updated in place. A balance is the sum of its entries.
29. `GET /api/accounts/{account}/balances` returns one row per balance kind, each carrying
    `kind`, `currency` and `amount_minor`. The kinds are `available`, `pending`,
    `disputed`, `fee`, `in_transit` and `settlement`, spelled exactly.
30. For one organisation, one environment and one currency, the sum of `amount_minor` over
    every kind is exactly zero. It is zero after seeding, it is zero after a refund, and it
    is zero after an approval.
31. Each balance's `amount_minor` equals the sum of the signed `amount_minor` of its ledger
    entries. The two are never allowed to disagree; if they ever do, the entries are the
    truth and the balance is wrong.
32. `GET /api/accounts/{account}/ledger-entries` returns the entries, each carrying
    `ledger_transaction_id`, `balance_kind`, `currency`, `amount_minor` and `created_at`.
    The signed amounts of one transaction sum to exactly zero.
33. Amounts are integers in the currency's minor unit, which for `inr` is the paisa, and
    they always travel with their currency code. A floating-point number never carries an
    amount, at any layer, including in a response body.
34. `GET /api/accounts/{account}/payouts` returns payouts, each carrying `id`, `currency`,
    `amount_minor`, `status`, `method`, `cutoff_at`, `arrival_estimate` and
    `statement_descriptor`. `GET /api/accounts/{account}/payouts/{id}` additionally returns
    the ledger transactions composing it, and the payout's `amount_minor` equals the sum of
    their net amounts exactly. An operator reconciles a payout to the entry level without
    leaving the console; the absence of that view is why finance teams keep parallel
    spreadsheets.

### Disputes

35. `GET /api/accounts/{account}/disputes` returns disputes, each carrying `id`,
    `payment_id`, `amount_minor`, `fee_minor`, `reason`, `status` and `evidence_due_at`.
    `status` is one of `needs_response`, `under_review`, `won`, `lost` or `accepted`.
36. Opening a dispute moved its amount out of `available` into `disputed` and debited the
    dispute fee from `available` into `fee`. That is already true of the seed, and it is
    what makes the disputed payment unrefundable.
37. The dispute detail shows the time remaining before `evidence_due_at` as text as well as
    a countdown, because a deadline that exists only as an animation is a deadline a screen
    reader user does not have.

### The developer surface

38. `GET /api/accounts/{account}/api-keys` returns the organisation's credentials for the
    requested environment, each carrying `id`, `type`, `display_prefix`, `last_four`,
    `created_at` and `revoked_at`. **No response from this route ever carries a `secret`
    field**, and only an `administrator` may call it.
39. `POST /api/accounts/{account}/api-keys` takes a `type` of `publishable`, `secret` or
    `restricted` and returns the new credential **with its `secret` present exactly once**.
    The console shows it under the notice `Copy this now. It will not be shown again.` A
    secret value begins with `sk_live_` in `live` and `sk_sandbox_` in `sandbox`; a
    publishable value begins with `pk_live_` or `pk_sandbox_`. The prefix carries the
    environment so a value found somewhere public is identifiable at a glance.
40. Only a hash of the secret and a short display prefix are stored. A later reveal is
    impossible rather than gated: there is no route that returns it again.
41. `POST /api/accounts/{account}/api-keys/{id}/revoke` marks the credential revoked with a
    timestamp and a reason. A revoked credential is still listed, never deleted.
42. `GET` and `POST /api/accounts/{account}/webhook-endpoints` read and create delivery
    targets, each carrying `id`, `url`, `subscribed_types`, `state`, `failure_count` and
    `created_at`, and only an `administrator` may call either.
43. A delivery address is refused at configuration time when its scheme is not `https`, and
    when the host is a loopback name or address, a link-local address, a private range or
    the cloud metadata address. The refusal carries the code `endpoint_address_forbidden`
    and writes nothing. `https://hooks.northbeam.example/nimbus` is accepted;
    `http://127.0.0.1/hooks`, `https://localhost/hooks`, `https://10.0.0.7/hooks` and
    `https://169.254.169.254/latest` are each refused.
44. `subscribed_types` may contain only these event types, spelled exactly:
    `payment.succeeded`, `payment.disputed`, `refund.created`, `refund.failed`,
    `approval_request.created`, `approval_request.approved`,
    `approval_request.rejected`, `approval_request.expired`, `payout.paid`. An unknown type
    is refused and nothing is written.
45. `GET /api/accounts/{account}/events` returns the events the organisation has produced,
    each carrying `id`, `type`, `object_type`, `object_id` and `created_at`. An executed
    refund request produces an `approval_request.approved` event and a `refund.created`
    event. Nothing is delivered anywhere: this environment has no outbound network at
    runtime and the delivery log is out of scope.

### The audit log

46. Every mutation appends one audit record carrying `sequence`, `occurred_at`,
    `actor_type`, `actor_id`, `actor_display`, `action`, `resource_type`, `resource_id`,
    `request_id`, `prev_hash` and `hash`. The display name is written at the time of the
    action, so a removed member's actions stay attributable.
47. `sequence` starts at `1` for each organisation and increases by exactly one, with no
    gap. Each record's `hash` covers its own content and the previous record's `hash`, so
    altering one record breaks every hash after it. Re-computing the chain detects any
    altered or removed record, and that detectable modification is the whole point of
    storing the chain rather than computing it on read.
48. `GET /api/accounts/{account}/audit-records` returns the log, newest first, filterable by
    `actor_id` and by `action`. Only an `administrator` may read it.
49. The application can insert into the audit log and read it, and can do nothing else to
    it. There is no route anywhere in this application that edits or deletes an audit
    record; the capability does not exist to be misused.
50. The audit record and the business change it describes are written together. If the
    record cannot be written, the change does not happen.

### The storefront

51. The country home at `/in` is a sequence of full-width bands in this order: the hero;
    a customer logo strip; a solutions bento of unequal cards; a light statistics band of
    four figures; a global reach graphic; a case study with an image, three facts and an
    expandable list; a dedicated experts band; a customer quote beside a four-logo
    carousel; a dark developer band; a dark statistics band of three figures with gradient
    numerals; three integration-path cards; a startups programme card; an annual letter
    with editorial cards; a book of the week band; an events carousel; and the footer.
    The solutions bento is headed `Flexible solutions for every business model.` above
    `Grow your business with a comprehensive set of payments and financial tools, designed
    to work individually or together.`, and its first card reads
    `Accept and optimise payments globally, online and in person`. The light statistics
    band is headed `The backbone of global commerce`. The case study carries the facts
    `160 countries`, `11k+ locations globally` and
    `Products used Payments, Terminal, Connect, Guard and Nimbus Query`. The experts band
    is headed `Realise value faster with dedicated experts`. The developer band is headed
    `Reliable, extensible infrastructure for every stack.` above
    `Adapt Nimbus to your business needs with flexible integration options.` and carries
    two controls, `View developer docs` filled and `View Nimbus's code` outlined against
    the dark ground. The integration band is headed `Choose an integration path.` above
    `With AI-powered support, rich documentation, and built-in debugging tools, you can
    quickly get started with the best option for your business.` and offers a
    conversational path, a no-code path over a grid of twelve platform marks, and a code
    path. The annual letter band reads
    `Businesses on Nimbus generated US$1.9tn in 2025.` above
    `Our annual letter explores the trends defining the internet economy, including
    steeper growth for newer businesses, faster international expansion, stablecoin
    progress, agentic commerce, and more.` with a `Read the letter` control. The book band
    reads `Book of the week` above `Entrepreneurship starts with ideas.` An events
    carousel holding fewer items than fit centres them rather than scrolling or
    duplicating them to fill. A configured set of zero customer logos omits the strip
    entirely, and its band padding goes with it, rather than rendering it empty.
52. The hero carries an eyebrow reading `Global GDP running on Nimbus:` followed by a
    rolling counter, a lead sentence reading
    `Financial infrastructure to grow your revenue.`, a continuation reading
    `Accept payments, offer financial services and implement custom revenue models, from
    your first transaction to your billionth.`, and exactly one primary control reading
    `Request an invite`. The country home is the one route with a single call to action and
    no secondary.
53. The counter's value is served by the application, never animated up to a hard-coded
    target on the client. It never counts down. If the value cannot be resolved, the
    eyebrow renders the last known value; it must never render an empty box or a zero. A
    financial service showing a zero where a number belongs is not a cosmetic failure.
54. The four light statistics are `135+` `currencies and payment methods supported`,
    `US$1.9tn` `in payments volume processed in 2025`, `99.999%`
    `historical uptime for Nimbus services`, and `200m+`
    `active subscriptions managed on Nimbus Billing`. The three dark statistics are `500m+`
    `API requests per day`, `10k+` `API requests per second`, and `150k+`
    `transactions per minute`. Each carries a value, a unit, a caption and an as-of date,
    and the as-of date is in the markup even where it is not displayed, because a claim
    about payment volume without a period is a compliance problem.
55. The customer quote reads
    `"With Nimbus, we have a global technology partner to help our customers, from Canadian
    yoga studios to British boxing classes, keep growing and evolving in a new wellness
    world."` attributed to `Kiran Mathew,` `Lead Product Manager of Payments, Wellspring`,
    with a `Read the story` link. Where a quote has no linked story the link is omitted
    rather than rendered inert.
56. The three expandable case studies read
    `Northbeam consolidates $5 billion in online and in-store revenue onto Nimbus.`,
    `Shopfront powers online grocery delivery with Nimbus.` and
    `La Gazette improves local and international payments with Nimbus.` Expanding one opens
    a real dialog: focus moves into it, focus is trapped, Escape closes it, focus returns to
    the card, and the page behind does not scroll.
57. Customer logos belong to the customers. The build ships placeholder wordmarks set as
    text for `Northbeam`, `Corvid Motors`, `Basecoin`, `Lumen Search`, `Shopfront`,
    `Wellspring` and `Assurely`, and accepts real marks as geometry later.
58. Three product routes share one template that varies on exactly three axes: theme, which
    is light or dark; availability, which is available or gated; and the pair of calls to
    action. `/in/billing` is light and available and reads
    `Monetise faster with Nimbus Billing.` above
    `Manage pricing, reduce churn and grow revenue, on one platform.` with `Start now` and
    `Contact sales`. `/in/guard` is dark and available and reads
    `Stop fraud without stopping growth.` above
    `Nimbus Guard protects your revenue with AI powered by Nimbus's global network.`
    `/in/query` is gated and reads `Gain deeper insights faster with Nimbus Query` with
    `Try for free` and `Contact sales`.
59. The heading and its continuation are one paragraph in two colours, not two blocks.
    Setting them as two blocks changes where the lines break and shifts the route's whole
    vertical rhythm.
60. `/in/query` is not sold in India. Its sub-navigation carries the badge
    `Not available in your country` beside the product name; its primary control reads
    `Join the waitlist` instead of `Try for free` and resolves to the lead form with the
    product preselected and a flag recording that the visitor arrived from an unavailable
    market; and its pricing band renders a note in place of prices, never prices from
    another market. The route stays fully readable and fully indexed. The failure this
    prevents is a visitor completing a signup that verification would refuse three steps
    later.
61. Each product route's band order is: the sub-navigation; the hero with its running
    demonstration; a feature triptych; one deep-dive band per sub-navigation section; an
    integration band with a code sample; customer proof; three related products; a pricing
    summary; the calls to action again; the footer. A related-products band never links to
    the route it is on. A sub-navigation item whose section does not exist is not rendered:
    a link that scrolls nowhere is worse than a shorter bar.
62. The primary control is never a plain link. It carries the route's product identifier and
    the visitor's locale into the lead form as query state, so the form arrives with the
    product preselected and the country defaulted. Losing that state costs the visitor two
    steps of a regulated form, which is a defect rather than a cosmetic issue.
63. `/in/guides` and `/in/customer-stories` are filterable card indexes over three seeded
    items each, filterable by category and by product and sortable by newest, oldest and
    most read, with a text search that settles before it runs rather than firing on every
    keystroke. **Filter state lives in the address.** A filtered index is shareable,
    bookmarkable and indexable, and the back button steps through filter changes one at a
    time.
64. A filtered index with no results names each active filter, offers a control to clear
    each one individually, and shows the three most recent unfiltered items beneath. An
    unfiltered index is never empty; if it ever is, that is the library being broken rather
    than an empty state, and the route says so honestly.
65. Article bodies are built from structured content mapped to components, never from
    stored markup injected into the page. That is what keeps every article looking like the
    rest of the product and what stops an editorial author becoming a source of injected
    script.
66. `/in/pricing` quotes every product in rupees. Amounts render as a rupee sign, the
    integer rupee part grouped in the Indian style, a full stop, and exactly two digits.
    Indian grouping puts the last three digits together and then pairs: `20000000` paise
    renders `₹2,00,000.00`, `228000` renders `₹2,280.00`, `12345` renders `₹123.45`,
    `27226598` renders `₹2,72,265.98` and `123456789` renders `₹12,34,567.89`. Every
    default formatter gets this wrong unless it is told which country it is formatting for,
    and it is usually not told.
67. A visitor is never silently redirected away from an explicit country segment. Someone
    in another country opening `/in` sees the India route with a dismissible notice offering
    the switch. Silent geographic redirection breaks shared links and breaks indexing, and
    it is the single most complained-about behaviour of sites in this category.
68. The footer is the authoritative public route list and is rendered from the same route
    manifest the sitemap is generated from. It carries a locale control labelled
    `India (English)` and a copyright line reading `(c) 2026 Nimbus`. A route present in one
    list and absent from the other is a build failure, not a content mistake.
69. `POST /api/leads` is the only write path on the public half. It takes `work_email`,
    `full_name`, `company`, `country`, `company_website`, `annual_volume_band`,
    `products_of_interest`, `message`, `consent` and `company_fax`. `work_email`,
    `full_name`, `company`, `country` and `annual_volume_band` are required; `full_name` is
    one to one hundred characters, `company` is one to two hundred, and `message` is at most
    two thousand. `consent` defaults to off and is never pre-ticked.
70. `company_fax` is an unattended decoy. A submission that carries a non-empty
    `company_fax` is refused with the code `spam_suspected` and **writes no lead row**. A
    form submitted repeatedly in quick succession is refused the same way: a bot is a
    caller that fills the decoy, or one that submits the same form repeatedly faster than a
    person could type it. A second submission of identical values within a short window is
    deduplicated: it returns the first lead's identifier and creates no second row. No visual challenge is presented
    on a first attempt, because a challenge on a sales form costs more real leads than it
    blocks fake ones.
71. The lead form works with client scripting unavailable. It is a real form with a real
    action, and the enhancement adds inline validation and asynchronous submission. This is
    the storefront's only revenue-bearing path and it must not depend on a bundle a
    corporate proxy may strip.
72. Invalid input is rejected inline, beside the field, naming the field and saying what to
    do about it, and nothing is written. A network failure keeps every typed value, shows an
    inline message and offers a retry; it is never a whole-page error.
73. An unknown address renders the product's own not-found page, answers not found, and
    carries a way back: the exact copy `We cannot find that page.` and a link to `/in`. It
    is never a redirect and never a blank frame.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Locale landing, renders the India home with a switch offered | none |
| `/in` | Country home | none |
| `/in/billing` | Billing product overview, light, available | none |
| `/in/guard` | Fraud protection product overview, dark, available | none |
| `/in/query` | Analytics product overview, gated by availability | none |
| `/in/pricing` | Pricing in rupees | none |
| `/in/guides` | Guides index, filterable | none |
| `/in/guides/:slug` | Guide detail | none |
| `/in/customer-stories` | Customer stories index | none |
| `/in/customer-stories/:slug` | Customer story detail | none |
| `/in/privacy-and-terms` | What the product stores and for how long | none |
| `/in/contact-sales` | The lead form | none |
| `/sitemap.xml` | Every public route | none |
| `/robots.txt` | Points at the sitemap | none |
| `/signin` | Email and password | none |
| `/accounts` | Account chooser | any member |
| `/a/:account/home` | Balance summary and recent activity | any member |
| `/a/:account/payments` | Payment list beside a detail pane | any member |
| `/a/:account/payments/:id` | Payment detail | any member |
| `/a/:account/payments/:id/refund` | The refund composer, at its own address | `support` or `finance` |
| `/a/:account/approvals` | Approval queue beside a detail pane | any member |
| `/a/:account/approvals/:id` | Request detail and the decision controls | any member |
| `/a/:account/balances` | Balances, ledger entries and payouts | `finance` or `administrator` |
| `/a/:account/disputes` | Disputes | any member |
| `/a/:account/developers/keys` | API credentials | `administrator` |
| `/a/:account/developers/webhooks` | Delivery endpoints | `administrator` |
| `/a/:account/settings/team` | Members and roles | `administrator` |
| `/a/:account/audit` | The audit log | `administrator` |

**Entry and redirects.** An anonymous request for any `/a/...` address lands on `/signin`
carrying where it was going, and returns there once signed in. Signing in with exactly one
membership lands on that organisation's home; with more than one it lands on `/accounts`.
Signing out returns to `/signin`. A token that expires mid-action returns the caller to
`/signin` with the destination preserved and whatever they had typed in an open composer
still there. A member opening a route their role cannot read is told plainly and offered
the routes they can reach, and the rail never shows a group they hold nothing in. A member
opening an organisation they do not belong to is told it was not found.

**Journeys.**

1. *A visitor reaches sales.* Open `/in`. Read the hero. Open the products menu in the top
   bar and follow it to `/in/billing`. Press `Start now`. Land on `/in/contact-sales` with
   Billing already ticked under products of interest and India already chosen as the
   country. Fill in a work email, a name, a company and a volume band. Submit. Read a
   confirmation naming the next step and the expected response window.
2. *A gated product.* Open `/in/query`. See `Not available in your country` beside the
   product name in the sub-navigation. See the primary control read `Join the waitlist`.
   Scroll to the pricing band and see a note where prices would be.
3. *A refund inside the ceiling.* Sign in as `support@example.com`. Open
   `/a/northbeam/payments`. Select the Corvid Motors payment in the list; its detail fills
   the pane beside the list without the list losing its scroll position. Press Refund, land
   on `/a/northbeam/payments/pay_corvid_12345/refund`, enter the full refundable remainder,
   choose a reason, submit. An inline banner confirms the refund in the composer's own
   region, the payment now reads `refunded`, and `available` has fallen by `12345`.
4. *A refund above the ceiling becomes a request.* Sign in as `support@example.com`. Open
   the Kaufhaus payment and press Refund. Enter `20000000`. The composer shows
   `This is above your refund limit of ₹5,000.00. Request approval instead.` Write a
   justification under the prompt `Why is this needed? Approvers will read this.` Submit
   the request. The payment carries a pending badge, the approvals count in the rail rises
   by one, and every balance reads exactly what it read before.
5. *An approval.* Sign in as `finance@example.com` and choose Northbeam Retail. Open
   `/a/northbeam/approvals`. The queue is ordered by how soon each request expires and the
   banner reads `{count} requests need your decision. The oldest expires in {duration}.`
   Select the request; the detail pane shows the payment, the proposed change, the raiser,
   their ceiling and their justification. Approve. The request reads `executed`,
   `available` has fallen by `20000000`, and the audit log carries the decision.
6. *A denial.* Sign in as `support@example.com` and open `/a/northbeam/approvals`. The
   approve and reject controls are absent, not present and refusing. Calling the approve
   endpoint directly with this session is denied by the server and the request's state is
   unchanged.
7. *A credential.* Sign in as `admin@example.com`. Open `/a/northbeam/developers/keys`.
   Create a secret credential. Read its value once beneath
   `Copy this now. It will not be shown again.` Reload the route. Only the prefix and the
   last four remain and no route anywhere returns the value again.
8. *The audit trail.* Sign in as `admin@example.com`. Open `/a/northbeam/audit`. Filter by
   actor. Read the approval with its actor, action, target and time, and the hash linking
   it to the record before it.

**States.** Every list has an empty state naming what would appear there and the action
that creates the first one. Every filtered list that comes back empty names each active
filter with its own clear control. Every route has a loading state that reserves the space
the data will occupy, so nothing reflows when the data arrives. A refetch keeps the rows
already on screen, dims them, and swaps the new data in place without losing scroll
position. A partial failure shows the rows that loaded with an inline retry for the range
that did not, never a whole-page error. A list of money that is no longer current shows a
relative timestamp and a refresh control, because a list of money is never allowed to look
current when it is not. A column the viewer may not read is absent rather than masked, since
a masked column tells them a value exists. Errors never crash the route: every one is an
inline banner in the region that produced it, and the page keeps what was typed.

## UI/UX notes

The north star is comprehension. Somebody arriving on the storefront should understand
within one screen that this is financial infrastructure a business plugs its own shop into;
somebody opening the console should know at a glance which organisation they are working as
and whether the money in front of them is real. There is no mood to invent here beyond
that, and inventing one would be the same defect as inventing a colour.

Two registers share one system. The storefront is editorial and composed and may carry
atmosphere, because it is arguing a case. The console is operational: quiet, dense but
organised, built for scanning and repeated action, with no oversized heroes and no
decoration standing in for content. The console **adds density, never a second visual
language**. Comprehension over atmosphere in the console; space over dividers on the
storefront.

**Colour by role.** The page ground is a near-white neutral, and cards on it are a plainer,
lighter near-white neutral; the two must stay visibly separate without needing a dividing
rule. Alternating section bands are two further near-white neutrals, each a shade deeper
than the last. The dark band, used by the fraud-protection route and by the developer band
on the home route, is a deep, muted blue. Headings on light are a near-black cool neutral,
body copy is a mid cool neutral, and muted copy, captions and disabled text step lighter
through three further cool neutrals. Hairlines are near-white cool neutrals, four steps
from the faintest rule to the strong rule and the input border. The primary action wears a
light, vivid blue and is **the only thing on a page wearing it**; pressed it becomes a mid,
vivid blue and a hovered link settles on a mid, soft blue. Product graphics and icon fills
take a light, vivid indigo over a near-white cool neutral backplate. Three colours carry
meaning and appear nowhere else: a mid, vivid teal for something that worked, a mid, vivid
red for something that went wrong, and a light, vivid orange for something still in
progress; success text on a tint is a deep, soft green on a light, soft green backplate,
and an informational marker is a mid, vivid blue. A state that is none of the three must not
borrow any of them: a refunded row is deliberately a mid cool neutral, and a disputed row
takes the light, vivid magenta the display gradients also use. Those display gradients run
from a mid, vivid amber through a light, vivid violet and a light, soft violet into the
brand blue, with a mid, vivid orange at the warm end. The focus indicator is a light, vivid
blue. The exact shades are yours, so long as each role holds the relationship and the
exclusivity above.

**Type.** Headings and body carry real contrast in weight and size, chosen so a heading
reads as a title and body reads comfortably at arm's length. The weight scale is
deliberately light and must be reproduced: the light weight is `200`, ordinary body is
`300`, control labels and emphasis are `425`, and what this system calls bold is `500`. Type
it the conventional way and the whole product gains a stone. Display sizes scale
continuously with the width of the window while body sizes do not scale at all; that
mixture is the look. Figures line up in a column wherever amounts stack, in the console
tables and in every currency amount inside a demonstration.

**Shape, space and elevation.** Corners are barely softened: controls and inputs take the
smallest softening, cards one step more, and the only fully rounded shapes are the
call-to-action link and the decorative gradient blobs. Elevation is always two shadows
stacked, one wide and cool and one tight and neutral, both pulled inward at their edges so
they fade out instead of ringing the card; a single soft shadow reads as a sticker, and this
must read as an object sitting slightly above the page. Every gap is a multiple of one base
unit that is yours to choose, and the gap between bands is roughly three times the gap
beneath a heading and about halves on a narrow screen. That air is most of the reason the
reference looks costly, and trimming it is the fastest available way to make this look
cheap. Section dividers lean rather than sitting level, and the layout pads for the
vertical overshoot the lean introduces so the seams between bands do not show.

**Components and their states.** One main action style and one quieter alternative; the
main one carries the strongest contrast in the interface. Both have resting, pointed-at,
pressed, focused and unavailable states, and unavailable is never signalled by colour alone.
Escape closes any overlay; a destructive action confirms first and the confirmation lands
focus on the cancelling control rather than the confirming one. Hovering a link changes the
word, its underline and the arrow beside it at the same moment and at the same speed; a word
that changes colour while its underline lags reads as cheapness nobody can name. Hover
affordances are gated so a touch device never latches a hover after a tap, and every one of
them has an equivalent that does not need a pointer.

**Motion.** One character throughout: things leave quickly and arrive slowly, easing off at
the end rather than starting sharply, and every transition that changes colour takes the
same beat so a route never looks like several animations happening near each other. Nothing
uses a different speed to feel special. Exactly one element per product demonstration
overshoots and settles back; nothing else in the system bounces. A closing panel fades out
and only becomes untouchable at the very end, so a pointer crossing it does not fall through
mid-fade. Connector lines in the demonstrations genuinely draw themselves, each knowing its
own length, rather than being revealed by a sliding cover. Reduced motion is the **rest
state**, not a stripped variant: every reveal is authored so its finished frame is the
document's normal state and the movement is the addition, so a visitor who has asked for
less motion sees complete, still, correct pictures rather than blank rectangles. Loading is
honest: work with a countable unit gets a determinate bar, and only a genuinely unbounded
wait pulses.

**The console shell.** A fixed top bar carrying the wordmark, the organisation switcher, the
environment control, search and the profile, over a left rail of grouped navigation that
collapses to icons and remembers its state for that member across devices. Switching
organisation is a full navigation rather than a state swap, because a residual response from
one company rendered under another company's name is the worst thing this product can do. In
`sandbox` a tinted band runs the full width of the top bar and stays there, reading
`Sandbox. No real money moves here.`; in `live` there is no band, and the absence of the
band is the signal. The treatment marks the safe environment on purpose, because habits form
where actions are harmless. That control never collapses and is never behind a menu at any
width. A navigation group the member holds nothing in is absent rather than greyed out:
greying it tells an intruder what is worth attacking and tells an honest colleague, every
day, that they are not trusted.

**Density and the table.** One table serves every list route, in two densities chosen per
member per route, with rows sitting tight enough that a full queue fits one screen. Amounts
are right-aligned in lining figures with the currency mark quieter than the number, the
header is sticky, sortable columns announce their sort state, the whole row is the target,
and explicit controls live in a trailing overflow menu. Pages are walked with a cursor
rather than a page number. State is never carried by colour alone: every badge carries a
label **and** a shape, a filled circle for terminal success, a hollow circle for pending, a
square for failed and a diamond for disputed.

**Accessibility floors, which are contract rather than taste.** Body text meets a contrast
ratio of at least 4.5 to 1 against its ground and large text at least 3 to 1; control
boundaries, focus indicators and meaningful graphics meet at least 3 to 1. Interactive
targets are never smaller than 44 by 44, including a row in a dense list, with a clear gap
between adjacent targets. Full keyboard navigation reaches every control in visual order
with a visible focus indicator that is two rings, an outer in the focus blue and an inner in
a near-white, drawn as a shadow so it follows the corner radius and never removed. Every
icon-only control carries a name describing the action rather than the shape. Meaning is
never carried by colour alone anywhere. The page title is unique per route and names the
organisation and the environment in the console, so somebody who cannot see the band still
knows whether the refund they are about to issue is real.

**Responsive behaviour.** Three widths, phone, tablet, and laptop and above, with a fourth
step where the gutters grow and the measure does not, and the layout holds at every width
between them. On a phone the dense table becomes a list of cards showing the three things an
operator triages on and never scrolls sideways, the rail becomes a sheet, and the
storefront's demonstrations drop to still frames; nothing carrying a claim, a price or a
call to action is ever dropped. Text inputs never render below the size at which a phone
zooms on focus, because that zoom does not reverse. At double magnification everything works
with no sideways page scroll, which is why no component wraps text in a fixed height. Where
the viewport is narrower than the smallest named width the layout still holds rather than
clipping.

**What this must not look like.** Not a page dominated by a single hue family with no second
signal. Not decoration standing in for content. Not a marketing composition where the
working interface belongs, and not the reverse: the storefront is allowed to breathe and the
console is not. Nothing borrowed wholesale from a subject unrelated to money.

## Technical requirements

**Stack.** SolidJS with Vite for the browser, built to a production bundle at image build
time. Hono on Node 20 serves both that bundle and the JSON API from one process on the same
origin, with the API under the `/api` prefix. The browser receives an application shell and
fetches its data as JSON; every public route nevertheless serves its own title, description
and social preview in the delivered document, so a crawler and a link preview both see them
without running script. PostgreSQL is the record for everything the product owns, reached
with the connection string in `DATABASE_URL`. Keycloak is the record for who a person is
and what password they hold, reached at `AUTH_URL` with the realm in `AUTH_REALM` and the
client credentials in `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET`. Plain CSS or CSS modules.
Any charting, drawing or animation library that installs from an official package registry
at image build time is acceptable, as is hand-written code over the platform's own
animation, canvas and scroll interfaces.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and Keycloak, and reaching for
anything else is a contract violation. Both are **already running** and reachable at the
environment variables above; do not download, install, compile or start a copy of either.

**Configuration.** `DATABASE_URL`, `AUTH_URL`, `AUTH_REALM`, `AUTH_CLIENT_ID`,
`AUTH_CLIENT_SECRET`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT` and `REFUND_REQUEST_TTL_SEC` are
read from the environment. Never hardcode a host, a port or a duration.
`REFUND_REQUEST_TTL_SEC` is the lifetime of a refund request in seconds and its production
value is `86400`. The application must read it; a duration compiled into the application is
a contract violation.

**Authorization is a layer, not a scatter of checks.** One decision is made per request from
the caller, the action, the resource and the context, and it is made before the request body
is validated, so an unauthorised caller cannot probe validation behaviour. The same decision
governs a route, a list query, a field in a response and a mutation. A field the caller may
not read is absent from the response rather than null and rather than a redaction marker.
The client is never an enforcement point: the console hides what a member cannot use because
that is kinder, not because it is a control.

**Tenancy is a property of the query, not a filter applied afterwards.** No read reaches
storage without both an organisation predicate and an environment predicate, and both are
derived from the session and the route rather than from anything the client sends. An
organisation identifier accepted from a request body is the mechanism of every cross-tenant
read defect in products of this shape.

**The session is a bearer token, not a browser cookie.** There is no first-party cookie here,
so nothing is `HttpOnly`, nothing is `Secure`, nothing carries `SameSite=Lax` and nothing is
host-scoped to the console origin. The token is opaque, it is held by the client, and it is
presented on every call; the server re-reads what its holder may do on every request.

**Correlation.** One request identifier per inbound request, generated by the application,
carried into every log line and every audit record, and returned on every response including
every error. It is the first thing support asks for.

**Logging discipline.** Log lines are built from a named list of fields. No log line
serialises a whole object, and no password, token, secret, credential value or full
instrument number is ever written to a log. Structured logs go to standard output.

**Caching.** Reference data may be held in process behind a version key. Anything belonging
to an organisation is keyed by that organisation and that environment, taken from the
request context. An authorisation outcome is never cached, because a cached permit outlives
the revocation that should have ended it; what may be cached is the membership and role data
the decision reads, behind a version that moves whenever any of it changes. Invalidation is
a version bump on write rather than a deletion, because a deletion races with concurrent
reads and a stale read of money is not acceptable. There is no edge cache in front of this
application, so a storefront traffic spike reaches the origin directly; identical concurrent
renders of one route are single-flighted so the losers wait rather than each recomputing,
and no response is ever served single-flighted from a cache to a different organisation.

**Rate limiting.** Sign-in is limited per organisation and address together, so one noisy
tenant cannot lock out another. The algorithm is a token bucket with a stated burst, so a
legitimate spike succeeds and a sustained flood does not. A limited caller is told plainly,
with a retry interval, and is never silently dropped. Limits are counted per organisation
first, so one organisation exhausting its budget never slows another's payments.

**Collections.** Pagination is cursor-based with opaque cursors, forward and backward,
carrying a `has_more` flag. It is never offset-based: an offset page of a list that receives
new rows at the top silently skips rows. A cursor encodes the shape of the query it was
issued for, and a cursor presented against a different filter set is refused rather than
answered with the wrong page.

**Data-layer obligations.** No unbounded query anywhere. No list route issues one query per
row it returns. A mutation's own response reads the authoritative copy, so an operator never
sees their own change missing and never clicks a refund twice because the first appeared not
to happen. Ledger entries are the two rows that grow without bound and every read of them is
bounded by an organisation, an environment and a time range.

**Transport.** The scheme of every address this product accepts or serves is secure
transport only, the one exception being the container-internal address the environment
itself provides. No state-changing request is reachable by a safe method, anywhere. Every
response carries a strict transport policy, a content-type-options policy, a frame policy,
a content security policy without inline script, and a referrer policy that does not leak
paths. A request whose content type does not match its body is rejected rather than sniffed.
A parameter the endpoint does not recognise is rejected rather than ignored, because
ignoring it is friendlier for exactly one afternoon and then somebody ships an integration
believing it turned a setting on.

**Observability, and its limits here.** Observability in this build is one request identifier
and a line of structured logs per request, carrying the route, the status, the latency, the
organisation, the environment, the principal type and the decision outcome. There is no
metrics pipeline, no aggregate internal metrics behind authentication, no tracing, no
alerting, no stated service objectives, no declared degradation path per failing subsystem
and no incident process, because there is nothing external here to degrade. What the
companion specification calls an operational obligation is, in this build, a scope boundary
that is stated rather than silently dropped.

**Performance posture, continued.** The critical-path stylesheet is inlined and stays small
once compressed, a few kilobytes rather than tens of them. Route scripts are split per route
group so the two heaviest surfaces are never in the common bundle. Nothing on the storefront
depends on a third-party script, and removing the one analytics hook would change nothing a
visitor can see.

**Outbound safety.** This application makes no outbound network call at runtime. A webhook
address is validated at configuration time against the rules in `## Core features` and is
never fetched.

**Expiry without a scheduler.** There is no cron, no worker, no queue and no background job.
A refund request older than its lifetime is expired the next time it is read or acted upon.
Anyone observing state cannot tell that from a sweeper, and the product only owes the state.

**One money component.** A single component renders every amount in both halves of the
product. It takes an integer and a currency and nothing else, applies the Indian grouping,
applies lining figures and applies the sign convention. Every independently formatted amount
is a future inconsistency, and in a payments product an inconsistent amount is a support
ticket that opens "your system shows two different numbers".

**One writer for the ledger.** Ledger entries are written in exactly one place in the code
that every other path asks. The zero-sum property is enforceable in one place only if there
is one place.

**Performance posture.** No list query is unbounded; every list has a ceiling and is walked
by cursor. A payment list never counts the collection, because an exact count of a large,
actively written table is expensive and is wrong by the time it is read. The heavy storefront
demonstrations run only at the widest breakpoint, with a fine pointer, and only when the
visitor has not asked for reduced motion; that decision is made by the stylesheet before any
script runs, so a phone never pays for the desktop show. Fonts are preloaded with their
metrics overridden so nothing moves on the page when a face finishes loading.

**Static assets the crawlers and the sharers need.** The application serves `/favicon.ico`
and declares it in the document head of every route. It serves `/sitemap.xml` listing every
public route from the same manifest the footer renders, and `/robots.txt` naming that
sitemap with an absolute address. Every public route declares a social preview title, a
description and a preview image address that resolves, and no two public routes share a
title or a description.

## Data model

Fifteen tables. All timestamps are UTC. Every amount is an integer in the currency's minor
unit stored beside its currency code, in two columns, always together.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

### person
`id`, `email` unique, `display_name`, `created_at`. A person exists independently of any
organisation. No password lives here.

### account
`id` (the slug), `display_name`, `country`, `default_currency`, `verification_state`,
`restriction_reason` nullable, `timezone`, `created_at`. `verification_state` is one of
`draft`, `submitted`, `under_review`, `information_required`, `verified`, `restricted`,
`suspended` or `closed`. `restriction_reason` is null unless the state is `restricted`.

### membership
`id`, `person_id`, `account_id`, `role`, `refund_ceiling_minor` nullable, `created_at`.
Unique on the person and the account together. `role` is `support`, `finance` or
`administrator`. A null ceiling means no ceiling.

### payment
`id`, `account_id`, `environment`, `customer_name`, `amount_minor`, `currency`,
`fee_minor`, `status`, `instrument_brand`, `instrument_last_four`, `captured_at`,
`created_at`. `refunded_minor` is **derived on read**, never stored.

### refund
`id`, `account_id`, `environment`, `payment_id`, `amount_minor`, `currency`, `reason`,
`status`, `ledger_transaction_id`, `approval_request_id` nullable, `idempotency_key`,
`created_by`, `created_at`. `status` is `succeeded` or `failed`.

Invariant: for any payment, the sum of the `amount_minor` of its non-failed refunds is never
greater than that payment's `amount_minor`. Two refunds of the last refundable rupees
arriving at the same moment must not both succeed: exactly one is accepted, the other is
rejected, and the payment's refunded total never exceeds its captured amount. This must hold
under real simultaneous requests.

### approval_request
`id`, `account_id`, `environment`, `operation_class`, `payment_id`, `amount_minor`,
`currency`, `justification`, `state`, `requested_by`, `requested_at`, `expires_at`,
`decided_by` nullable, `decided_at` nullable, `decision_note` nullable, `refund_id`
nullable, `idempotency_key`. `state` is `pending_approval`, `executed`, `rejected`,
`expired`, `withdrawn` or `execution_failed`. `operation_class` is `refund_above_ceiling`.

Invariant: while a request is `pending_approval` it owns no refund row and no ledger entry.
Two approvals of one request arriving at the same moment produce exactly one refund: one is
accepted, the other observes the outcome of the first. `decided_by` is never equal to
`requested_by`.

### balance
`account_id`, `environment`, `currency`, `kind`, `amount_minor`. Unique on the four. `kind`
is `available`, `pending`, `disputed`, `fee`, `in_transit` or `settlement`.

Invariant: for one account, environment and currency, the sum of `amount_minor` across every
kind is exactly zero, at every moment an observer can read it. Each balance's
`amount_minor` equals the sum of the signed amounts of its ledger entries.

### ledger_transaction
`id`, `account_id`, `environment`, `kind`, `effective_at`, `created_at`, `source_type`,
`source_id`, `reverses_id` nullable. `kind` is `capture`, `refund`, `dispute_opened`,
`payout_created` or `payout_paid`.

### ledger_entry
`id`, `ledger_transaction_id`, `account_id`, `environment`, `balance_kind`, `currency`,
`amount_minor` signed, `created_at`. Never updated and never deleted; a correction is a new,
opposing transaction that references the original.

Invariant: the signed `amount_minor` of the entries of one transaction sum to exactly zero
per currency. The posting rules are: a capture of gross `G` with fee `F` debits `settlement`
by `G`, credits `available` by `G - F` and credits `fee` by `F`; a refund of `R` debits
`available` by `R` and credits `settlement` by `R`; a dispute opening for `D` with dispute
fee `X` debits `available` by `D + X`, credits `disputed` by `D` and credits `fee` by `X`; a
payout creation for `P` debits `available` by `P` and credits `in_transit` by `P`; a payout
payment for `P` debits `in_transit` by `P` and credits `settlement` by `P`.

### payout
`id`, `account_id`, `environment`, `currency`, `amount_minor`, `status`, `method`,
`cutoff_at`, `arrival_estimate`, `statement_descriptor`, `created_at`. `status` is
`pending`, `in_transit`, `paid` or `failed`.

### payout_item
`payout_id`, `ledger_transaction_id`. Invariant: a payout's `amount_minor` equals the sum of
the net amounts of the transactions it lists.

### dispute
`id`, `account_id`, `environment`, `payment_id`, `amount_minor`, `currency`, `reason`,
`fee_minor`, `status`, `evidence_due_at`, `created_at`. `status` is `needs_response`,
`under_review`, `won`, `lost` or `accepted`.

### api_credential
`id`, `account_id`, `environment`, `type`, `display_prefix`, `last_four`, `secret_hash`,
`created_by`, `created_at`, `revoked_at` nullable, `revoked_reason` nullable. `type` is
`publishable`, `secret` or `restricted`. The plaintext value exists only in the creation
response; nothing stores it.

### webhook_endpoint
`id`, `account_id`, `environment`, `url`, `subscribed_types`, `signing_secret_hash`,
`state`, `failure_count`, `created_by`, `created_at`, `disabled_at` nullable. `state` is
`enabled` or `disabled`.

### event
`id`, `account_id`, `environment`, `type`, `object_type`, `object_id`, `created_at`.

### audit_record
`id`, `account_id`, `environment`, `sequence`, `occurred_at`, `actor_type`, `actor_id`,
`actor_display`, `action`, `resource_type`, `resource_id`, `reason_code` nullable,
`request_id`, `prev_hash`, `hash`.

Invariant: `sequence` starts at `1` per account and increases by exactly one with no gap;
`hash` covers the record's content and `prev_hash`; the application inserts and reads and
does nothing else, and no route edits or deletes a record.

### idempotency_key
`account_id`, `environment`, `endpoint`, `key`, `request_fingerprint`, `response_status`,
`response_body`, `created_at`. Unique on the first four. Retained twenty-four hours.

### lead
`id`, `work_email`, `full_name`, `company`, `country`, `company_website` nullable,
`annual_volume_band`, `products_of_interest`, `message` nullable, `referring_route`,
`fingerprint`, `created_at`. Unique on `fingerprint`, which is derived from the work email,
the form version and a coarse time bucket.

### Seed data

**People and memberships.** `support@example.com` is Asha Rao, `support` on `northbeam`
with a ceiling of `500000`. `finance@example.com` is Kiran Mathew, `finance` on both
`northbeam` and `wellspring`, with no ceiling. `admin@example.com` is Devika Nair,
`administrator` on `northbeam`. `support2@example.com` is Damian Mueller, `support` on
`wellspring` with a ceiling of `500000`.

**Organisations.** `northbeam` is Northbeam Retail, India, `inr`, `verified`. `wellspring`
is Wellspring Studios, India, `inr`, `restricted`, with `restriction_reason` of
`settlement_instrument_unverified`.

**Payments on `northbeam` in `live`**, with the fee for each. The fee rule is two percent of
the captured amount, rounded half to even to the nearest paisa, plus `300` paise; the worked
example that disambiguates the rounding is `12345` paise, whose two percent is `246.9`,
which rounds to `247`, plus `300`, giving `547`.

| id | customer | amount | fee | status |
|---|---|---|---|---|
| `pay_beanbar_2280` | Bean Bar | `228000` | `4860` | `succeeded` |
| `pay_kaufhaus_200000` | Kaufhaus | `20000000` | `400300` | `succeeded` |
| `pay_northwind_75000` | Northwind Trading | `7500000` | `150300` | `succeeded` |
| `pay_streamly_4500` | Streamly | `450000` | `9300` | `succeeded` |
| `pay_corvid_12345` | Corvid Motors | `12345` | `547` | `succeeded` |
| `pay_plansmith_12500` | Plansmith | `1250000` | `25300` | `disputed` |

**Payment on `northbeam` in `sandbox`:** `pay_sandbox_beanbar_1000`, Bean Bar, `100000`,
fee `2300`, `succeeded`.

**Payment on `wellspring` in `live`:** `pay_lumen_7750`, Lumen Search, `775000`, fee
`15800`, `succeeded`.

**Dispute:** `dp_plansmith_0001` on `pay_plansmith_12500`, amount `1250000`, dispute fee
`150000`, reason `fraudulent`, status `needs_response`.

**Payout:** `po_northbeam_2231` on `northbeam` in `live`, amount `223140`, status `paid`,
method `bank_transfer`, statement descriptor `NIMBUS NORTHBEAM`, listing the capture
transaction of `pay_beanbar_2280`.

**Balances after seeding**, each row summing to exactly zero:

| account | environment | available | disputed | fee | in_transit | pending | settlement |
|---|---|---|---|---|---|---|---|
| `northbeam` | `live` | `27226598` | `1250000` | `740607` | `0` | `0` | `-29217205` |
| `northbeam` | `sandbox` | `97700` | `0` | `2300` | `0` | `0` | `-100000` |
| `wellspring` | `live` | `759200` | `0` | `15800` | `0` | `0` | `-775000` |

**Credentials:** `key_northbeam_live_01`, `secret`, display prefix `sk_live_`; and
`key_northbeam_sandbox_01`, `secret`, display prefix `sk_sandbox_`.

**Endpoint:** `whe_northbeam_live_01` at `https://hooks.northbeam.example/nimbus`,
subscribed to `payment.succeeded`, `refund.created` and `approval_request.approved`, state
`enabled`.

**Storefront content:** three guides and three customer stories, each with a title, a slug,
a category, a reading time and a published date; the four light statistics and the three
dark statistics named in `## Core features`; and one customer quote with its attribution.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

Everything here is appearance. Where a sentence also carries behaviour, the behaviour is
stated precisely and the appearance is stated as intent.

### The scaling rule

Display type is driven by a viewport scale factor that reaches unity at the width of a
laptop and falls proportionally below it, so a headline grows continuously with the window
rather than stepping at a breakpoint. Body type is not driven by it at all. The subtraction
that allows for a reserved scrollbar gutter stays in the expression even where the platform
reserves none, because that is what keeps the arithmetic identical between platforms that do
and do not.

### Layout and rhythm

A four-column measure inside a centred content width, with the gutters computed from the
window rather than fixed. Running copy is capped at three of the four columns, which is why
paragraphs stop short of the right edge while headings do not. The measure stops growing on
a very wide display and the gutters absorb the rest; that is the most conservative and most
correct decision in the system, and the one most often overridden by somebody with a large
monitor who thinks the page looks empty. Band padding above and below is generous and equal.

### Colour, continued

The console adds semantic aliases over the roles in `## UI/UX notes` and introduces no new
colour: succeeded takes the teal, pending the orange, failed the red, refunded the neutral,
disputed the magenta, blocked the deep, muted blue, the alternating table row the second
near-white band, the drawer the card ground with the large elevation step, and the row
separator the faintest hairline. A component that hard-codes a value cannot be re-themed for
a hosted page carrying a customer's own branding, so colour is always applied through its
role.

Three further roles exist only inside the demonstrations. A product-graphic accent, the
light vivid indigo, fills the icons and the small marks drawn inside a demonstration. An
alternate attention tone, a half-step from the in-progress orange, is used where two
pending states sit beside each other and must be told apart. And the progress bar's warm
terminus, the light vivid magenta, is the colour the bar reaches when it completes. None of
the three appears anywhere in the console.

### Typography, in full

Two families. The interface family is a variable grotesque; this build ships no licensed
face, so it declares the family it would use and falls back to `Helvetica Neue`, then
`Arial`, then the platform sans-serif, with ascent, descent and line gap overridden so
nothing reflows when a real face arrives. Code and tabular figures are set in
`SourceCodePro` at weight `500`, self-hosted and openly licensed. The whole specification is
complete and correct in the fallback stack alone; nothing here depends on the display face
existing.

The rendered scale, reproduced rather than idealised: `14px` for console-dense text and
footer text, `16px` for body copy, `18px` for a lead-in, `15px` for a control label, `13px`
for a footer link, `10px` for legal and eyebrow text, and `14px` for code. The code face's
line height is exactly twelve sevenths of its size; rounding it drifts code blocks out of
alignment with their line-number gutter.

### Radius, shadow and elevation

A five-step elevation scale, every step two layers: a wide cool shadow and a tight neutral
one, both with negative spread so they fade rather than halo. Each step reserves the space
its shadow occupies, so a card in a grid does not clip its shadow against its neighbour. A
shadow applied to a masked or non-rectangular shape is applied as a filter, not as a box
shadow, because a box shadow on a masked element shadows the box and not the mask. Radii
step from the barely-softened control through the card to the panel header that rounds only
the two corners meeting a flat edge below.

### Angles

Section dividers are sheared rather than level, at a shallow angle and at a steeper one, and
each shear carries a stored allowance for the vertical overshoot it introduces so a
component can pad for it without doing trigonometry while it renders. Ignore that allowance
and the seams between bands show.

### Stacking

Exactly four tiers and no others: local composition inside a component, fixed chrome, modal,
and decorative behind content. A component that needs to escape its tier uses a portal
rather than a larger number. The application root and the navigation content each open their
own stacking context, which is what lets local stacking restart inside a panel without
leaking out of it.

### Iconography

Every icon is geometry drawn in the page: not a font, not a file, not a sprite, and never
fetched. Icons inherit their colour from their container rather than carrying one, taking
either the current colour or a named role from the ink ramp. A stroked icon keeps its
`stroke-width` when its box is scaled; scaling the box without scaling the stroke is the
usual defect. The system set is the chevrons in four directions, a back caret,
the expanding caret pair that forms a link underline, the hover arrow in its open, closed
and clipped forms, the long arrow used in feature cards, the menu control, the cross in its
toggle and dismiss forms, the tick in a filled circle and in an outline circle, a download
arrow into a tray, a disclosure caret, an external-link box, a generic card mark, an
overflow ellipsis, the three browser window dots, a padlock, a globe for the locale control,
and the wordmark carrier.

Two of them are cleverer than they look. The menu control is four bars with two of them
coincident in the middle; opening it fades the outer pair and swings the coincident pair
apart about the shared centre into a cross, one shape with two meanings and no swap. The
hover arrow sits in a window deliberately too small for it with its shaft beginning outside
the left edge, which is what lets it slide in from nowhere rather than switching on; its
retraction does not travel at all, so it reads as retracting into the word.

Card scheme marks are other companies' trademarks and are not redrawn. A neutral placeholder
of exactly the right size stands in each slot, a hairline rounded rectangle carrying a
two-letter monogram in the code face, and the licensed marks drop in later.

### Chrome, in full

The top bar is fixed, full width, and the same height on both halves of the product. On the
storefront it sits transparent over a light hero, inherits the section ground over a dark
one, and fades in a blurred overlay once the route has scrolled, which is the only place in
the system where the chrome itself blurs what is behind it. Its five primary items are
`Products`, `Solutions`, `Developers` and `Resources` as disclosure buttons, then `Pricing`
as a plain link; `Sign in` sits at the right as a link with a trailing hover arrow and
`Contact sales` beyond it as a filled control with the same arrow. A hairline sits under the
bar on light routes, drawn as a fading element rather than a border so it softens at the
gutters.

The four disclosures open **one** shared panel that animates its height to whatever section
is active and cross-fades the contents, without the route behind reflowing and without the
scroll position changing. Moving between two open items must read as the drawer rearranging
itself, not as one drawer slamming and another opening. The panel is a disclosure and not a
dialog: focus is not trapped, tabbing past the last item closes it and continues into the
page, Escape closes it and returns focus to the trigger, a pointer opens it after a short
intent delay while a second open is immediate, and a keyboard opens it on activation only,
never on focus. Hover intent must survive a diagonal pointer path from the trigger into the
panel; a naive departure handler on the trigger closes the panel while the pointer crosses
the gap, and that is the single most common defect in a build of this component. The panel's
own footer band carries a soft radial highlight.

Below a phone width the five items collapse into one control and the panel becomes a
two-level drill-down: choosing a category slides the whole panel sideways to reveal that
category with a back control, the way a phone's own settings do, never an accordion
concertina. While it is open the page beneath does not scroll and the scroll position is
restored exactly on close, with the scrollbar gutter reserved so closing does not jump the
layout sideways.

Each product route carries a second sticky bar beneath the top bar: the product name on the
left with an availability badge where the product is gated, and the section links plus an
outbound documentation link carrying the external-link icon on the right. The documentation
link opens in the same tab, because opening a new one is the visitor's platform's decision
and not the page's. The active section is derived from what is actually on screen rather
than from the address fragment, so it stays correct when the visitor scrolls by hand. In-page
anchors carry scroll margin equal to the combined height of both fixed bars. On a phone the
right half collapses into a single toggle opening a sheet whose shadow escapes its clip on
three sides while its top edge stays flush with the bar. A route with fewer than two
sections renders the bar with the product name and the documentation link only, never with a
single lonely section link. A very long product name truncates to one line with an ellipsis
while the availability badge never truncates, never abbreviates and never wraps mid-word.

The footer is the tallest component in the system and sits on the second near-white band.
Five columns at desktop, two at tablet, and a single accordion on a phone. The columns are
the products, the solutions and developer destinations, the resources, the support links
with a trailing `Sign in`, and a bottom bar carrying a globe icon, the locale label
`India (English)`, the copyright line and a small solid mark at the far right. Footer text
is the `13px` size at the body weight in a mid cool neutral, and a column heading is the
body size at weight `500`.

### Hover, in full

Hovering a muted navigation link moves it from its mid cool neutral to the near-black cool
neutral, and the underline drawn beneath it and the caret pair beside it move at the same
moment and at the same speed, because they are separate elements and a build that transitions
only the element's own colour leaves the underline behind at the old value for the duration.
The quiet button variant changes its fill and its opacity together: the fill lightens while
the whole control becomes slightly more transparent, which lifts it over a light ground and
sinks it over a dark one. Doing only one of the two produces a visibly different control. A
link inside the navigation panel drops to a lower opacity instead. All of it is gated so a
touch device never latches a hover state after a tap.

### Motion, in full

One easing character governs everything: a fast departure and a long settle. A small number
of related curves exist for specific jobs, and no curve outside that set may be introduced,
because a build that needs a curve this system does not have is describing a motion this
product does not make. Colour, fill, stroke and opacity all share the house beat. Card
transforms are slightly slower. One long-travel transform is slower again. A closing panel
delays its loss of interactivity until its fade has finished, so panels never appear to
swallow clicks while they disappear. One collapsing region is stepped rather than
interpolated, in a single jump at the end of its window, because interpolating its height
would thrash layout.

Named moments, each carried as a moment rather than as a number: a plain fade; a fade that
rises a short distance and then stays arrived, whose terminal state keeps the element on its
own compositing layer because it will be scrubbed afterwards; a gradient border that turns
once, continuously, about its container's centre, with the centring inside the transform
because the element is larger than the box it turns in; a backplate tint that arrives to a
near-opaque value on a light ground and to a lighter one on a tinted ground; a line that
draws itself from its own measured length, which is why these lines cannot be reproduced by
animating a width; a marker that pops into place; and a bar that grows upward. Every one of
the last three is authored one-sided, with the finished state as the element's rest state,
which is what makes the reduced-motion experience correct rather than blank.

The hover arrow animates in over a very short beat, travelling a few units from the left
while it fades in, and animates out with no travel at all. The menu bars rotate to opposite
diagonals about their shared centre on a snappier curve than anything else in the system.
The navigation panel's height change uses a symmetric in-out curve while its contents
cross-fade on the standard one. A quiet ease-out governs the smallest state changes on quiet
controls, and a success checkmark arrives by being uncovered rather than by fading.

One sequence advances a registered integer frame index from zero to the frame count and
computes a position from it, which is frame-by-frame animation driven entirely by the style
engine with no script and no timer. The same idiom drives the text loader inside the code
demonstration, cycling a short set of braille glyphs through a pseudo-element's generated
content, which is why that graphic has a spinner without a spinner element.

Reduced motion is declared as the absence of motion rather than as its removal: animation is
declared inside a no-preference query so the document's default state is the finished state,
and the reduce query exists only to unwind the handful of effects that are load-bearing. The
heaviest demonstrations are gated three ways at once, on the widest breakpoint, on a fine
pointer and on no reduced-motion request, which is the performance strategy expressed as
stylesheet queries rather than as script.

### Scroll, in full

Scroll-driven elements satisfy five properties together, and a build satisfying four of them
feels wrong in a way that is hard to diagnose. They are bidirectional, so scrolling up
un-plays the effect and the state is a pure function of position rather than an event log.
They are idempotent at rest, so stopping mid-effect leaves a valid intermediate frame rather
than one that continues settling. They move only compositor properties, so no scroll handler
writes anything that triggers layout. They run off the main thread where the platform allows
a scroll-driven timeline, and read position once per frame otherwise, never inside the scroll
event itself. And under reduced motion every scrubbed element renders at its terminal frame.

Arriving at a deep anchor, or returning with a restored scroll position, initialises every
scrubbed element to the frame for that position before the first paint rather than starting
at zero and jumping. Scrolling past the last keyframe holds the terminal frame with no wrap
and no re-entry. An element that enters view already past its window renders its terminal
frame without animating. Resizing mid-effect recomputes the windows from the new geometry and
the current frame from the current position, never from the start. Magnifying the page well
past double disables scrubbing entirely and renders terminal frames. Printing renders
terminal frames.

Reveals are clips, not fades and not height animations: a hidden inset interpolated to a
revealed one on a single axis, so the movement reads as a card being uncovered from behind a
straight edge rather than as something a screen does. One clip form keeps its corners soft
while clipping; one is deliberately larger than its box on three sides so a shadow can
escape; one is negative horizontally so an address bar can bleed. A horizontally scrolling
row fades softly at both ends, and that soft edge belongs to the container rather than the
track, so it stays put while the track moves. A horizontal case-study carousel is a native
scroller with snap points rather than a transform-driven track, because a transform-driven
track loses the platform's momentum and its accessibility behaviour.

### The product demonstrations

Each is markup rather than media; no frame of one is a raster. Each carries no text that is
not also in the document, because its captions are read by search engines and by assistive
technology. Each runs only under the triple gate above and renders one still terminal frame
outside it. None blocks the first paint: the terminal frame is the served state and the
movement is added afterwards. Currency, language and payment-method set come from the
route's locale, and a visitor in India sees a rupee amount before they see anybody else's
money.

The reused primitive is a fake browser window containing a fake page, both entering over a
single linear beat and both settling at an opacity slightly below fully opaque. It never
becomes quite solid, and that is what keeps it reading as an illustration of a browser
rather than as a screenshot pasted onto the page. Its chrome is the three window dots and a
padlock, and its address block is clipped so a long address bleeds past the frame rather
than truncating. The demo addresses are `beanbar.example/checkout`,
`kaufhaus.example/checkout` and `streamly.example/checkout`, and the demo buyers are
`asha.rao@example.com`, `damian.mueller@example.com` and `taro.yamada@example.com`.

The billing hero is one authored timeline of about nineteen seconds driving roughly twenty
elements, with a single time origin shared by all of them. Three price cards rise and settle;
the left and right cards fold away while the centre one widens; usage rows and totals write
themselves into the widened card; the card becomes an invoice and a drawer slides in from
the right; a download control appears and the sequence holds. Built as twenty independent
animations of matching length it will drift, because the platform does not guarantee that
twenty animations started in the same frame share a start time, and by the third loop it
looks wrong. On a phone it collapses to two composite pieces and loops; on a wide screen it
runs once and holds.

The fraud demonstration is the densest, on a dark ground over a faint grid of thin lines. A
group of radiating path lines is transformed continuously while each line is independently
clipped, producing a fan growing outward from a centre. Connector curves are paths rather
than lines, because the same geometry is both the drawn line and the track the little arrows
travel along. One dash pattern marches by exactly its own period so the line never appears to
restart. A validation card pulses on a fixed cycle, a rotating gradient marks a working
state, a progress bar fills from a deep blue into a magenta, and a verdict fills in. Behind
all of it a very large, very soft glow, and a sub-pixel backdrop blur on the same element
that forces it onto its own compositing layer without visibly blurring anything, which is a
deliberate rasterisation hint rather than a mistake. Its labels are `Card testing`,
`Transaction fraud`, `Bot abuse`, `SCANNING...`, `BUILDING PAYMENT PROFILE...`,
`Payment analysis`, `Fraudulent dispute`, `Early fraud warning`, `Detection signals` and
`Pending`.

The code demonstration is set in the code face with a masked rather than bordered
line-number gutter, an elevated autocomplete list, a status line carrying a mode indicator, a
filename, a percentage and a line and column, and the braille loader described above. Its
syntax colours are four roles over the deep, muted blue ground: a keyword in the light,
vivid violet, a string in the light, vivid orange, an identifier in a near-white, and
punctuation in a light cool neutral. Its strings are `NORMAL`, `server.js` and
`Ready! Waiting for requests...`. It is not editable and is not focusable. The console's
real editor, if one is ever built, shares only the type and the colour roles with it.

The checkout demonstration rotates locales, showing `Pay Bean Bar`, then
`Kaufhaus bezahlen`, then a Japanese equivalent, with amounts of `US$5.46`, `EUR 26.89` and
`JP¥5,000`, a terminal prompt reading `Tap, insert or swipe to pay` in each language, line
items `Mocha Latte`, a loyalty discount, tax and a total, field labels `Email`,
`Payment method`, `Card` and `or`, and a `Continue` control. It also shows an instalment
option reading `Instalment plan` and a conversational path whose bubbles read
`Hi, I'm looking for a simple day cream with SPF?` and
`Sure, in that case, I'd recommend our pure glow cream!` beside a `Pure glow cream` product
card priced in rupees and a `Scan to pay` square.

Display numerals in the statistics rows are filled with a gradient running from amber
through violet into the brand blue, with each numeral showing a different slice of the same
ramp so the row reads as one continuous sweep rather than three identical rainbows. A
gradient numeral always applies a solid fallback colour first, so a platform that cannot clip
a gradient to text renders the numeral in the brand blue rather than in nothing. Invisible
text is the worst failure available on a route whose whole argument is its numbers.

### The dense table, in full

Two densities selectable per member per route, the comfortable one a little taller than the
compact one. Rows are the console-dense size at the body weight, with an eighteen-unit line
box, and the whole row navigates. Amounts are right-aligned in tabular figures with the
currency mark in a lighter cool neutral than the number. Even rows take the alternating
ground. The header is sticky and each sortable column carries a sort indicator that
announces its state. Selection is a leading checkbox column supporting a shift-click range,
and selecting everything matching a filter is visibly distinguished from selecting
everything visible. Beyond a couple of hundred rows the body is virtualised with honest
scrollbar proportions. A first load renders skeleton rows at the configured density and at
the exact expected count, so nothing reflows when the data lands.

### Zero-asset substitution

No image file, no photograph, no video, no icon file and no font file ships with this build.
Every graphic is drawn, and the substitution is procedural rather than a placeholder file.
What is being replaced, so nobody goes looking for it: the hero ribbon and its gradient
palette source; the bento card grounds; product and merchandise photography; card artwork
and its palette; the map dot field; the sprite sheet; the platform logo grid; the startups
programme card and its graphic background; the spacer; both typefaces; and every video.

Photographic and card imagery becomes deterministic procedural placeholders generated
from the identifier of the thing they stand for: a hash picks two stops from the palette, a
gradient runs between them at a hash-derived angle, two large soft highlights sit at
hash-derived positions, a generated grain texture is composited over it at low opacity, and a
single large soft shape gives the composition a focal point. The same story therefore always
gets the same picture, a grid of them looks composed rather than random, and their
alternative text is empty because they carry no information. A dot field is a generated point
set tested against a coarse landmass mask and drawn once to an offscreen surface rather than
once per frame. A matrix code is computed from its payment-link identifier and emitted as
rectangles with three nested-square registration marks and a quiet zone, not fetched as a
picture. Customer logos and partner marks are placeholder wordmarks set in the interface
family at weight `500` until real marks are supplied as geometry. A spacer image is replaced
by an explicit aspect-ratio box. The hero ribbon is a procedural three-layer reconstruction:
a broad conic sweep running orange through pink and violet into blue, rotated so its seam
falls outside the visible box; a repeating very-low-opacity light-and-dark banding at a
shallow angle composited so it reads as folded material catching light; and a large blur with
a radial mask dissolving one corner to nothing. The hero heading composites over it in a
blend that lets one piece of text read as near-black over the white part and luminous over
the saturated part, without two colour treatments and without a scrim.

## Constraints

- One organisation's data is never visible to another organisation's members, at any address,
  by any parameter, in either environment.
- No card issuing, no lending origination, no carbon removal purchasing, and no card artwork
  or issuing palette anywhere.
- No connected accounts, no platform relationships, no controller types, no multi-party money
  flows, no transfers between organisations, no destination or direct charges, no transfer
  reversals and no application fees.
- No subscriptions and no subscription items with a price, a quantity and a metered flag; no
  usage meters, no usage events, no aggregation of usage totals; no invoicing, no invoices,
  no invoice numbering sequence, no credit notes, no dunning attempt carrying an ordinal, a
  scheduled time and an attempted time, no revenue recovery,
  no instrument refresh, no recovery page, no catalogue of products and prices, no price
  tiers, no coupons and no tax rates.
- No query workspace and no assistant: no schema browser, no templates, no saved queries, no
  run history, and none of the Run, format, save and schedule controls. No reporting surface
  and no prebuilt reports,
  no scheduling at a daily, weekly or monthly frequency against an account-timezone anchor,
  no backfill, no long-running operations, no exports, no portability export in a documented
  format, and no downloadable file of any kind.
- No machine-facing service and therefore no machine principal construction: a credential is
  created, listed and revoked in the console, and no request is ever authenticated by one.
- No federated identity: no federation configuration carrying an issuer, a certificate, an
  enforced flag and a skew tolerance; no claim mapping; no assertion validated on issuer,
  audience, signature, expiry and not-before; no assertion replay store; no clock skew
  tolerance configurable downward; no `sso` administration and no `scim` provisioning
  scopes; no break-glass path; no second factor; no recovery codes issued once at
  second-factor enrolment, single-use and hashed, whose consumption is an audited event; no
  password reset; no signup and no self-service account creation.
- No notifications and no transactional messaging, and therefore no notification channel of
  any kind: no in-console notification centre, no
  email, no push, no digest aggregation of low-urgency events coalesced above a threshold
  when an extremely high volume arrives from one account, no per-member per-channel
  preferences, no quiet hours, no unsuppressable critical classes, no bounce or complaint
  handling, and no separate sending identity. Nothing is queued for mail, so nothing is
  unaffected by mail being unavailable: there is no mail here at all. Nobody is told that a
  dispute was received, that an approval is expiring, or that a requester's request needs a
  decision; those facts live in the console and the console is the truth.
- No outbound webhook delivery, no delivery attempt, no delivery log, no signature, no retry
  schedule and no replay. Webhook endpoints are configured and validated; nothing is ever
  sent to one.
- No onboarding or verification data capture: no business identity form, no representative
  attestation, no beneficial owners, no cumulative volume threshold requiring documentary
  evidence, no enhanced review by a human decision, no settlement instrument entry, no
  document upload and no file storage anywhere in the product.
- No careers route, no role list, no life and benefits band, and no job application.
- No risk scoring, no signals, no rule authoring, no backtesting, no shadow mode, no arming
  and no manual review queue. The fraud-protection product route describes the product; it
  does not operate it.
- No real payment rail, tax service, screening vendor, object store, key management service,
  content service, analytics vendor, consent vendor or tag manager. No integration carries a
  timeout and a budget, and none has a circuit breaker with a half-open probe, because there
  is no integration: no outbound network call is made at runtime, and no two providers can
  disagree, be recorded and be escalated to a human, so there is no automatic tie-break to
  forbid.
- No background job, no cron, no scheduler, no worker, no message queue, no outbox, no
  outbox relay elected as a singleton per partition, no recurring platform-wide job, no
  credential narrowing pass, no reconciliation job, no dead-letter store, no leader
  elected under a fenced lease, no long-running durable workflow with checkpoints for bulk
  operations, no chunked resumable backfill rate-limited against replica lag, no thumbnail
  or extraction derived in an isolated worker with no egress, and no chaos exercise over
  provider outage, replica lag, queue backlog, leader failover and clock skew whose
  observable behaviour is written down and then asserted.
- No read replica and therefore no replica lag, no freshness fail-over under a circuit
  breaker, and no isolated query capacity to saturate.
- No API versioning: no pinning an account permanently to the then-current version at first
  request, no per-request override header for testing an upgrade, and no deprecation window.
- No data residency, no per-tenant data encryption key or key alias, no field-level
  encryption, no key rotation, no erasure by key destruction, no pseudonym map, no retention
  schedule, no statutory retention class, no anti-money-laundering or know-your-customer
  programme, no subject rights and no restriction flag.
- No release or governance process reaches into the product: no automated accessibility run
  in a pipeline blocking merge, no secret scanned pre-commit and post-push and triaged, no
  backup rehearsed on a schedule where the rehearsal is the test, no reconciliation mismatch
  alert, no job queue age exceeding a per-class threshold, and no blameless post-incident
  review published internally and summarised to affected customers.
- No native application, no edge function and no server-side rendering framework beyond the
  one named in `## Technical requirements`.
- One currency, `inr`, and one locale, India in English. The locale control lists other
  locales and switching to one is out of scope; so is any right-to-left language, any
  zero-decimal currency and any currency conversion.
- The product must stay responsive with roughly ten thousand payments and one hundred
  thousand ledger entries per organisation per environment.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `200` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `person` |
| `GET /api/me` | none | `person` and its `memberships` array |
| `GET /api/accounts` | none | a top-level JSON array of accounts |
| `GET /api/accounts/{account}/payments` | `environment`, `cursor`, `limit`, `status` | a top-level JSON array of payments |
| `GET /api/accounts/{account}/payments/{id}` | `environment` | one payment |
| `POST /api/accounts/{account}/payments/{id}/refunds` | `amount_minor`, `currency`, `reason`; header `Idempotency-Key` | the created refund |
| `POST /api/accounts/{account}/payments/{id}/refund-requests` | `amount_minor`, `currency`, `reason`, `justification`; header `Idempotency-Key` | the created approval request |
| `GET /api/accounts/{account}/refunds` | `environment` | a top-level JSON array of refunds |
| `GET /api/accounts/{account}/approval-requests` | `environment`, `state` | a top-level JSON array of requests |
| `GET /api/accounts/{account}/approval-requests/{id}` | none | one request |
| `POST /api/accounts/{account}/approval-requests/{id}/approve` | `note` optional | the request, now `executed`, with its `refund_id` |
| `POST /api/accounts/{account}/approval-requests/{id}/reject` | `note` required | the request, now `rejected` |
| `POST /api/accounts/{account}/approval-requests/{id}/withdraw` | none | the request, now `withdrawn` |
| `GET /api/accounts/{account}/balances` | `environment` | a top-level JSON array of balances |
| `GET /api/accounts/{account}/ledger-entries` | `environment`, `cursor` | a top-level JSON array of entries |
| `GET /api/accounts/{account}/payouts` | `environment` | a top-level JSON array of payouts |
| `GET /api/accounts/{account}/payouts/{id}` | none | one payout with its `transactions` |
| `GET /api/accounts/{account}/disputes` | `environment` | a top-level JSON array of disputes |
| `GET /api/accounts/{account}/api-keys` | `environment` | a top-level JSON array, never carrying `secret` |
| `POST /api/accounts/{account}/api-keys` | `type`, `environment` | the credential, carrying `secret` exactly once |
| `POST /api/accounts/{account}/api-keys/{id}/revoke` | `reason` | the revoked credential |
| `GET /api/accounts/{account}/webhook-endpoints` | `environment` | a top-level JSON array of endpoints |
| `POST /api/accounts/{account}/webhook-endpoints` | `url`, `subscribed_types`, `environment` | the created endpoint |
| `GET /api/accounts/{account}/events` | `environment`, `type` | a top-level JSON array of events |
| `GET /api/accounts/{account}/members` | none | a top-level JSON array of memberships |
| `GET /api/accounts/{account}/audit-records` | `actor_id`, `action`, `cursor` | a top-level JSON array of records |
| `POST /api/leads` | the lead fields in `## Core features` | the created lead |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call
returns the named resource or shape. An invalid, unauthenticated or unauthorized call is
rejected as a client error, never as a server error and never as a silent success, and
carries a body of the shape
`{"error": {"type", "code", "message", "param", "request_id"}}` where `code` is the stable
machine-readable string this brief pins and `message` is for a person to read. Bearer auth
is required on everything under `/api/accounts` and on `/api/me`, and nowhere else.

**No mocks.** PostgreSQL is the fact for every record this product owns and Keycloak is the
fact for who a person is. An in-memory array of payments, a refund that exists only in
component state, a balance recomputed in the browser from a hard-coded starting figure, a
hand-written `{"status":"succeeded"}` the app returns to itself, an audit chain that is
recomputed on read rather than stored, or a seed that lives in a JavaScript file rather than
in the database are each a contract violation however good the interface looks. The named
provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A support operator can refund a small payment outright and watch the organisation's
available balance fall by exactly that amount. A larger refund becomes a request that moves
no money until a different person approves it, and approving it twice still hands back the
money once. A member of one organisation sees nothing belonging to another, in either
environment. Every amount reads in rupees under Indian grouping, and every balance still
sums to zero.
