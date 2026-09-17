# Mercato

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, sign in as a
support agent, issue a refund larger than that agent's ceiling, and see it become an
approval request that a finance lead then approves, without hitting an error page.

A different stranger, signed in as that same support agent, must NOT be able to approve
their own request by any means, and must not be able to reach a second store's orders by
guessing an address. The approval cannot be faked inside the app: while a request waits, no
money may have moved and no ledger entry may exist for it, and after one approval the
refund must exist exactly once in the store's books even if the approve control is pressed
twice.

## Overview

Mercato is a multi-tenant commerce platform. A retail organisation signs up, builds a
catalog, stocks it across locations, connects sales channels, and from then on runs its
trade through Mercato: watching orders arrive from every channel, routing them to a
location, printing labels, taking money, handing money back, arguing a chargeback, running
a wholesale price list for a business buyer, and deciding which of its own staff may do
each of those things.

Four surfaces share one design system and nothing else. The **marketing storefront** is the
public, country-segmented site that sells the platform: a country home, a plan comparison,
roughly thirty product capability routes on one template, an enterprise surface with its
own chrome, a retail surface with its own, and an editorial index. The **merchant admin**
is the authenticated application the storefront sells. The **buyer surfaces** are what a
merchant's own customers touch: the merchant's online store, the hosted checkout, the
customer account area, the order status page and the point-of-sale terminal in a physical
shop. The **machine surface** is what third-party applications, sales channels and AI
shopping agents speak to.

The account here does not belong to a person. It belongs to a business, that business has
staff, and the staff are not equal. The person on the shop floor may take a return. The
person in the warehouse may correct the count of what is on the shelf, but only in their
own warehouse. The wholesale representative may see the companies assigned to them and no
others. None of them may quietly add themselves to the list of people allowed to do
somebody else's job. There is no owning user to scope a row to: every query is scoped to a
store, and separately filtered by what that member may see.

**The genuinely hard part is that a permitted action can be too large for the person
permitted to do it.** A refund is not allowed or denied; it is allowed up to an amount, and
above that amount it stops being a refund and becomes a proposal that waits for somebody
else. Nothing happens while it waits: no money moves, no stock is taken, no message is
sent, because a sent message cannot be unsent. It goes to whoever currently holds the right
job rather than to a named person, so a holiday does not stop the business. It refuses
self-approval. It chases, then widens the net, then quietly lapses and says so. And when it
is finally approved, it happens exactly once.

Mercato deliberately is not several things. It is not a shipping carrier, a card acquirer,
a bank, a tax authority or a mail vendor; each of those is modelled behind Mercato's own
contract with a documented fallback, and none is contacted. It does not build terminal
firmware or pair card readers. It has no native mobile application. It does not author
editorial content, only consume it. It is not a place where anyone deletes a merchant's
data as a side effect of anything else.

## User roles

Signup is closed. Accounts are seeded; there is no public registration for staff. A person
exists independently of any store, and a person may hold membership in more than one store.

Permissions are fine-grained, namespaced and separately grantable, and a role is a named
set of them. A role says which actions. A **constraint** says on which rows: which
locations, which markets, which channels, which assigned companies, which personal-data
fields, and, for a refund, up to what amount. Both are required. Most systems build the
first and forget the second, and then a business with two warehouses discovers that anyone
who may correct stock may correct it everywhere.

| Role | Can read | Can write | Cannot |
|---|---|---|---|
| `owner` | everything in the store | everything in the store, including the plan and the transfer of ownership | **nothing is denied, but every dangerous act is logged and, above a threshold, needs a second person** |
| `administrator` | everything in the store | everything except changing or cancelling the plan | **change the plan, cancel the plan, or transfer ownership** |
| `store_manager` | orders, products, inventory, customers, discounts, online store, analytics | the same, and may run a discount | **manage staff, edit payment settings, or edit the settlement instrument** |
| `merchandiser` | products, inventory, store content | products except their cost, and store content | **read or edit a product's cost, adjust stock, or read orders** |
| `fulfilment_operator` | orders, fulfilment, inventory at assigned locations | fulfil, hold, release, buy a label, adjust stock and receive returns, at assigned locations only | **adjust stock at a location they are not assigned to, or read a customer's payment details** |
| `support_agent` | orders, customers without their personal fields, returns | refund up to `500000` in minor units, approve a return, start a return | **exceed the refund ceiling, read a full payment instrument, or read a residential address** |
| `finance` | balances, payouts, disputes, settlement instrument, finance analytics | refund up to `20000000` in minor units, submit dispute evidence, manage the payout schedule, export orders | **manage staff, edit a posted ledger entry, or edit products** |
| `sales_representative` | assigned companies only, and their orders, quotes and price lists | create a draft order on an assigned company's behalf, and a discount within ceiling | **see a company they are not assigned to, or publish a wholesale price to the public store** |
| `retail_associate` | orders at the assigned location | ring a sale, take a payment, accept a return within policy, discount within ceiling | **discount beyond the ceiling, open the day's totals, or see another location's takings** |
| `retail_manager` | the associate set, plus the day's totals | the associate set, plus opening and closing the register, managing staff codes, and adjusting stock at assigned locations | **grant themselves a permission they do not already hold** |
| `analyst` | analytics, orders, products | nothing | **mutate anything, anywhere** |
| `auditor` | the audit record, and every resource | nothing | **write anything at all, enforced structurally rather than by convention** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `support_agent` session to any
`finance`-only endpoint must be rejected by the server (an unauthorized request is denied,
not served), leaving the protected state unchanged.

Four further rules bind every role above.

1. **Nobody may grant a permission they do not already hold.** A custom role may contain
   only permissions the granting actor holds, checked on the server, on every surface
   including the machine one.
2. **A denial says which of four things went wrong**: the actor lacks the permission, the
   plan does not include the capability, the region does not allow it, or nobody in this
   store may do it. Four different conversations, four different messages.
3. **A list filters by policy inside the query.** A row the actor may not see is absent and
   the stated result count reflects the absence. The interface never says twelve results and
   shows nine.
4. **A field the actor may not read is redacted at the boundary**, so it is masked in the
   interface, in every export and in every machine response alike, and it renders as a
   consistent mask rather than as an empty value that reads as none.

The permission vocabulary is closed, namespaced and separately grantable. `orders` carries
`read`, `create_draft`, `edit`, `cancel`, `capture_payment`, `refund`, `mark_paid`, `archive`
and `export`. `fulfilment` carries `read`, `fulfil`, `request_fulfilment`, `hold`, `release`,
`buy_label` and `cancel_fulfilment`. `returns` carries `read`, `approve`, `decline`, `receive`,
`restock` and `refund`. `products` carries `read`, `create`, `edit`, `delete`, `publish`,
`edit_cost`, `edit_price`, `export` and `import`. `inventory` carries `read`, `adjust`,
`transfer_create`, `transfer_receive` and `set_available`. `customers` carries `read`,
`read_pii`, `create`, `edit`, `delete`, `export` and `segment_manage`. `companies` carries
`read`, `read_assigned`, `create`, `edit`, `approve_request` and `assign_representative`.
`discounts` carries `read`, `create`, `edit`, `delete` and `exceed_ceiling`. `markets` carries
`read`, `create`, `edit`, `publish`, `manage_catalog`, `manage_price_list` and `manage_domain`.
`finances` carries `read_balance`, `read_payout`, `read_dispute`, `submit_evidence`,
`manage_payout_schedule`, `read_settlement_instrument` and `edit_settlement_instrument`.
`analytics` carries `read`, `read_finance`, `create_report` and `export`. `online_store`
carries `read`, `edit_theme`, `publish_theme`, `edit_content`, `manage_menu` and
`manage_domain`. `apps` carries `read`, `install`, `uninstall`, `manage_scopes` and
`read_credentials`. `automations` carries `read`, `create`, `edit`, `activate`, `deactivate`
and `run_manually`. `settings` carries `read`, `edit_general`, `edit_payments`,
`edit_shipping`, `edit_taxes`, `edit_locations`, `edit_checkout`, `edit_notifications` and
`edit_policies`. `staff` carries `read`, `invite`, `edit_permissions`, `remove` and
`manage_roles`. `plan` carries `read`, `change` and `cancel`. `audit` carries `read` and
`export`. `pos` carries `operate`, `open_close_register`, `discount_up_to_ceiling`,
`accept_return`, `read_daily_totals` and `manage_staff_pins`.

Two of those deserve comment. `customers.read_pii` is separate from `customers.read` so a
support agent can find an order without reading a residential address. `products.edit_cost` is
separate from `products.edit_price` because cost is margin data and a merchandiser is not
automatically entitled to it.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Store | Constraint |
|---|---|---|---|
| `owner@example.com` | `owner` | `Oakleaf and Co` | none |
| `manager@example.com` | `store_manager` | `Oakleaf and Co` | both locations |
| `support@example.com` | `support_agent` | `Oakleaf and Co` | refund ceiling `500000` |
| `finance@example.com` | `finance` | `Oakleaf and Co` | refund ceiling `20000000` |
| `mallard@example.com` | `store_manager` | `Modern Mallard` | both locations of that store |

`mallard@example.com` is a member of `Modern Mallard` and of no other store. Nothing
belonging to `Oakleaf and Co` is reachable from that session, by navigation, by address or
by identifier.
## Core features

### Refunds and the ceiling

This is the spine of the product and every other feature exists around it.

1. A refund is composed against a paid order. It may be by line, by amount or against
   shipping, and each produces its own entries.
2. A refund whose amount is at or below the acting member's refund ceiling executes
   immediately: the money moves, a balanced ledger transaction is written, the order's
   financial status advances to `partially_refunded` or `refunded`, and the order timeline
   carries a refund entry naming the actor and the instant.
3. **A refund whose amount is above the acting member's refund ceiling does not execute and
   is not rejected. It creates an approval request.** While that request is pending: no
   money has moved, no ledger transaction exists for it, the order's financial status is
   unchanged, and the order's timeline carries a request entry rather than a refund entry.
   `support@example.com` has a ceiling of `500000` in minor units; a refund of `3411200`
   against order `#2049` from that session creates a request and changes nothing else.
   `finance@example.com` has a ceiling of `20000000`; the same refund from that session
   executes at once.
4. The negative case: a `support_agent` session that calls the refund endpoint directly
   with an amount above the ceiling receives a denial of the immediate refund, gets a
   pending request instead, and the order row is untouched. A `support_agent` session that
   calls the approval-decision endpoint directly is rejected by the server as unauthorized,
   and the request stays pending.
5. Every refund attempt carries a client-supplied idempotency key, unique per store. A
   repeat with the same key returns the original result rather than performing a second
   refund.
6. The sum of non-failed refunds for a payment may never exceed the amount captured. Two
   refunds racing for the remaining balance produce one success and one explicit refusal
   stating the actual remaining amount, never two successes and never a negative remainder.
7. A refund that fails at the payment layer leaves its record in a pending state and
   retries with a widening gap. It never silently reverses, and it never writes ledger
   entries speculatively.
8. Restocking is a separate decision from refunding and is separately permitted, because
   the person who may authorise the money is not necessarily the person who may declare a
   returned item fit to sell.
9. A refund may draw on the original payment method, then a gift card or store credit, then
   a manual method recorded by staff. The order is configurable per merchant, is explicit,
   and is shown before confirmation.
10. A refund exceeding the store's available balance is permitted: the balance goes
    negative, a debit is raised against the merchant and the merchant is notified. Refusing
    it would make the merchant unable to serve their own customer.

### Approval requests

1. An approval request carries the proposed action and its full parameters, the requester,
   the reason, the permission required to decide it, the resolved approver scope, a state
   and an expiry.
2. **The proposed action has no side effect while the request is pending.** Doing it and
   reversing on rejection is the tempting implementation; it is wrong for money and
   impossible for a message.
3. The approver set is resolved from roles and constraints, never from a named individual,
   so that one person's absence does not block the business. It is resolved when the
   request is created and resolved again when it is decided.
4. **Self-approval is refused.** The requester may never appear in the approver set for
   their own request. A direct decision call from the requester's own session is rejected
   by the server and the request remains pending.
5. Request states are `pending`, `approved`, `declined`, `expired` and `executed`. A
   request that nobody answers lapses at its expiry, notifies, and remains auditable as
   lapsed rather than disappearing.
6. An unanswered request escalates to a wider approver set after an interval, before it
   expires.
7. **On approval the action executes exactly once.** The request carries the idempotency
   key the execution uses, so a double approval, a redelivered queue message and a timed-out
   downstream call all converge on one effect. Two approvers approving at the same instant
   produce one refund.
8. If the underlying resource changed materially between request and decision, the
   execution re-validates, refuses, and names what changed. It never executes against a
   stale proposal.
9. If the approver loses the deciding permission between their decision and the execution,
   the execution is refused and the request returns to pending with a notification.
10. An approver may delegate to another holder of the same permission for a bounded window,
    and the delegation is recorded.
11. The actions that route through approval: a refund above ceiling; a discount above
    ceiling; a business-buyer order above the review threshold; a price change beyond a
    configured percentage; a bulk operation above a size threshold; a change of payout
    instrument; and activating an automation that contains a money-moving action.
12. Request, every notification, every view, the decision, the executing effect and its
    outcome are linked by one correlation identifier.
13. At the point-of-sale terminal the same object is decided in seconds rather than hours: a
    manager enters a code on the same device and the action proceeds. The code identifies a
    person and that person is recorded as the approver; a shared override code is refused by
    design. It is unavailable when the terminal is offline, because there is nothing to
    check a code against.

### Auth

Staff sign in through the running identity provider `keycloak` at `AUTH_ISSUER_URL`, using
an authorization-code flow with proof key and the client credentials at `AUTH_CLIENT_ID`
and `AUTH_CLIENT_SECRET`. Signing in authenticates the **person**; selecting a store
authorizes a **membership**.

1. The session identifier is opaque and high-entropy, carried in a cookie that is secure,
   http-only, same-site lax, host-only and pathed at the root. The cookie carries no claim,
   no role and no store; the identifier resolves server-side.
2. **The store context lives on the server session.** No request names its store. A store
   identifier taken from a request parameter and trusted is the single most common way a
   system of this shape leaks between tenants, and it is forbidden here.
3. Passwords, where a person sets one, are hashed with a memory-hard function whose
   parameters are stored beside the record, have a minimum length of `8` with no composition
   rules, and are checked against a breached-password corpus.
4. A one-time sign-in link is single use, lives `15` minutes, is invalidated by use or by a
   newer link, and is bound to the requesting browser so a forwarded link cannot be used
   elsewhere.
5. A second factor is required for any member holding a dangerous permission and may be
   required of everyone by a store administrator. Recovery codes are issued once and stored
   hashed.
6. A person session idles out after `24` hours and expires absolutely after `30` days, both
   configurable downward. A dangerous action additionally requires a fresh authentication
   within `15` minutes.
7. The session identifier rotates on sign-in and on any privilege change. Multiple sessions
   are permitted, individually listable and individually revocable by the person and by a
   store administrator. Signing out revokes server-side, not merely by clearing the cookie.
8. Group claims from the issuer map to roles, per store or across stores. A mapped role is
   authoritative and cannot be edited in the admin. Losing a group claim removes the mapped
   role at the next assertion or the next lifecycle event, whichever is sooner. A scheduled
   comparison reports differences between issuer state and local state rather than silently
   applying them, because a failed synchronisation that silently removes everybody's access
   is worse than a drift report.
9. Deprovisioning a person at the issuer terminates every session and revokes every token
   held by that person within `60` seconds. This is a budget, not a nightly job.
10. An organisation may require federated sign-in, and when it does, password and one-time
    link sign-in are refused for its members. A small named set of members keeps a local
    credential for recovery; every use is logged at the highest severity and notifies every
    organisation administrator.
11. Every assertion is validated for signature against the issuer's published keys,
    audience, issuer, expiry and not-before within a configured clock skew, and is single use
    by assertion identifier. A repeat is rejected.
12. A buyer account is a different kind of principal entirely. A staff person and a buyer
    with the same address are unrelated: no shared session, no shared reset, no shared
    credential record.
13. Enumeration resistance: a sign-up with an address that already exists produces the same
    response as one with a new address, and the existing account is notified instead.

### Organisations, stores and tenancy

1. Four levels, always: an organisation holds stores; a store holds locations, markets,
   channels and memberships; a person holds memberships to stores and, separately, to
   organisations. An organisation with one store is not a special case, it is one with a
   single child.
2. Tenancy is enforced three times over: the store context resolves from the server session;
   every tenant-owned query carries a store predicate and one without it does not run; and a
   connection scoped to one store returns zero rows from another store's tables even when
   the application layer is bypassed entirely.
3. **An organisation administrator is not automatically a member of any store** and may not
   read store data by virtue of the organisation role alone. They may grant themselves a
   store membership, and that act is logged at high severity. The alternative, where the
   organisation role implies read access everywhere, means one compromised organisation
   account reads every store and the audit record cannot tell administration from access.
4. Creating a store is one transaction that also creates the default location, the default
   market, the online-store channel, the owning membership and a theme assignment. A store
   that exists without a location cannot hold stock, and that state is structurally
   forbidden.
5. A store handle is lowercase kebab, globally unique, and immutable after the first order.
   The currency defaults from the country and is changeable only before the first order.
   The timezone is a named zone, never an offset.
6. Store lifecycle states are `trial`, `active`, `past_due`, `frozen`, `paused`, `closed`
   and `archived`. **No lifecycle transition deletes merchant data as a side effect.** A
   frozen store's public shop returns a holding page while its admin stays readable and its
   billing stays actionable; its owner can still read and export their own records.
7. Deletion is a separate, explicit, delayed operation with its own confirmation, its own
   notification to the owner and its own audit entry.
8. Development and staging stores cannot take a live payment, cannot message an address that
   has not opted in, and cannot install an application holding a live credential. Their rows
   are marked as seeded so a report can exclude them. Transferring one to a merchant
   requires fresh consent for every installed application's scopes.
9. An operation spanning stores names the stores it touches; there is no implicit all
   stores. Each store in the scope is authorized independently, a store the actor may not
   read is omitted and the omission is reported rather than silently dropped, partial
   success is reported per store, and one organisation audit entry plus one per store share
   a correlation identifier.

### Catalog

1. A product is a merchandising object; a **variant** is the sellable one. Every price,
   stock-keeping unit, barcode and inventory level belongs to the variant, never to the
   product.
2. A product carries at most `3` options, each with an ordered value list. A variant's
   option value tuple is unique per product and its arity equals the product's option count.
   A variant carrying three option values on a two-option product is a corrupt row the
   database refuses rather than the application detecting later.
3. Four independent axes decide whether a shopper sees something: `status`, which is
   `draft`, `active` or `archived`; publication per channel, optionally at a future instant;
   publication per market; and membership of a catalog. A product may be `active`, published
   to the online store, unpublished from the point of sale, present in two of five markets,
   and in one business catalog at a different price. All four are queried on every buyer
   read.
4. A variant's price is integer minor units plus a currency code. A compare-at price must
   exceed the price where it is set, or the interface is claiming a discount that does not
   exist. Cost is optional and separately permitted, because cost is margin data and a
   merchandiser is not automatically entitled to it. A converted price is a stored, rounded
   record; rounding never happens at read time.
5. A collection is either a manual ordered membership list with a position per row, or
   rule-based over product fields, tags, price, stock and metafields with a sort order. A
   rule-based collection is materialised, not evaluated on read; a rule change enqueues a
   rebuild and the collection carries the instant of its last successful build so the
   interface can say it is catching up rather than appearing wrong.
6. Import validates the whole file before writing anything: one bad row reports that row and
   writes nothing, unless the merchant explicitly chooses partial mode. Rows match on
   stock-keeping unit or on an external identifier, never on title. Export is asynchronous,
   produces a durable artefact, notifies on completion and expires. A bulk edit previews
   before it commits, showing the affected count and a sample, and is one reversible
   operation for a bounded window recorded as a single audit entry.
7. Deleting a product that has orders is refused; it archives instead, because the orders
   referencing it must keep making sense in five years. Removing an option value that is in
   use is refused with the list of variants that would be orphaned. A duplicate
   stock-keeping unit is permitted with a warning, because merchants legitimately reuse
   them, and is unique only where the merchant opts in. A price of zero is permitted for a
   free gift; a negative price is refused. A product is refused above `2000` variants per
   product, with the option-set explosion named in the message.
8. Alternative text is required at publication for the primary media of a published product.
   It is a gate, not a nag.

### Inventory across locations

1. **An inventory level is a set of quantities, not one number**: `on_hand`, `committed`,
   `reserved`, `incoming`, `damaged`, `quality_control` and `safety_stock`. `on_hand` is what
   is physically present; `committed` is reserved against an unfulfilled order line; `reserved`
   is held by an open checkout; `incoming` is on a transfer not yet received; and the last
   three are held back from sale for a named reason. `available` is
   derived from them by subtraction and is never a writable column. Every production defect
   of the form "we sold five of the last one" traces to a system where somebody wrote
   `available`.
2. Every change is an append-only movement entry carrying the item, the location, which
   quantity moved, the delta, the resulting quantity, a reason from the closed set `sale`,
   `return`, `restock`, `correction`, `received`, `transfer_out`, `transfer_in`, `damaged`,
   `theft`, `promotion`, `sample`, `recount`, the causing object, the actor, an idempotency
   key where the cause is retryable, and a database-assigned instant.
3. The current level is a projection of that ledger, reconciled on a schedule. A discrepancy
   between projection and ledger raises an alert; it is never silently corrected.
4. Starting a checkout increases `reserved`; the reservation expires and is released by a
   sweeper, because a buyer who closes their browser tells nobody. Placing an order decreases
   `reserved` and increases `committed` in one transaction. Creating a fulfilment decreases
   `committed` and decreases `on_hand` in one transaction. Cancelling before fulfilment
   decreases `committed` and leaves `on_hand` untouched. Receiving a return increases
   `on_hand` into the quantity the restock decision names.
5. A variant's `inventory_policy` is `deny` or `continue`. Under `deny` the variant is
   unpurchasable at zero available, checked at cart add, at checkout start and again inside
   the order-placement transaction. **Only the third check is authoritative**; the first two
   are a courtesy so the buyer finds out early. Under `continue` the order is created with a
   backorder flag and the fulfilment is held until stock arrives.
6. **Two orders for the last unit, placed at the same instant, produce exactly one success
   and one explicit out-of-stock refusal naming the short line and the shortfall.** Stock
   never goes negative through this path, and the losing request leaves no partial state: no
   orphaned row, no quantity left committed.
7. Deactivating a location holding stock is refused until the stock is transferred or
   written off, and the message states the quantity. Silently zeroing it is shrinkage nobody
   can explain.
8. A transfer carries an origin, a destination, a state from `draft`, `pending`,
   `in_transit`, `partially_received`, `received` and `cancelled`, an expected arrival and
   its lines. Receiving is partial and repeatable, each receipt writing its own entries.
   Over-receipt is permitted with a warning and recorded as such, because refusing it makes
   people lie to the system.
9. A correction that would make `on_hand` negative is permitted, because reality sometimes
   is, but it is flagged and reported. An untracked variant has an undefined `available`
   rather than zero and is always purchasable, and the interface distinguishes not tracked
   from none left.
10. A terminal and the online store read the same levels. There is no separate retail stock
    table. A terminal may query another location's availability read-only and may raise a
    transfer request, but may not move another location's stock.
11. Stock adjusted at a location outside the actor's constraint is denied, and that location
    does not appear in the picker at all.

### Orders

1. **Financial status and fulfilment status are two independent axes and never collapse into
   one.** Financial status is `pending`, `authorized`, `partially_paid`, `paid`,
   `partially_refunded`, `refunded` or `voided`. Fulfilment status is `unfulfilled`,
   `partially_fulfilled`, `fulfilled`, `on_hold`, `scheduled` or `in_progress`. `paid` with
   `unfulfilled` is the most common state in any real store and a single-status model cannot
   express it.
2. **Every order line stores its own snapshot** of the product title, the variant title, the
   stock-keeping unit, the price, the tax lines, the discount allocation and the weight,
   alongside a reference to the variant which every read path must tolerate being absent.
   This is correctness, not speed: the price the buyer paid must survive a price change, a
   rename, an option restructure and an archival.
3. An order carries a sequential number per store and an opaque identifier, its channel, its
   market, its buyer and, where it is a business order, the company and company location,
   its money in minor units, its two statuses and a separate cancellation state, snapshotted
   billing and shipping addresses, its attribution, its risk score and level, and its
   timestamps.
4. Staff may edit an order before it ships: add a line, remove an unfulfilled line, change a
   quantity, add a discount, change shipping. **An edit computes a delta**: a positive delta
   is an additional charge requiring the buyer's authorization, a negative delta is a refund
   and therefore obeys the ceiling rule above. Quantity changes move `committed` in the same
   transaction. Fulfilled lines are immutable; removing one is a return.
5. Two staff editing one order at once: the second is refused with a message naming what
   changed underneath them. The two edits are never blended into something neither of them
   meant.
6. A draft order is an order not yet placed: a quote, a phone order, a wholesale order built
   by a representative. It is priced from the buyer's catalog and price list, may carry a
   manual line for something not in the catalog, reserves nothing until it is sent for
   payment, expires after a configured window and releases any reservation, and retains its
   own identifier after conversion so the audit chain holds.
7. The order index is a queue-list with columns `Order`, `Date`, `Customer`, `Total`,
   `Payment status`, `Fulfillment status` and `Items`, plus any column the merchant adds.
   Filters cover status, date range, channel, location, market, tag, risk level, fulfilment
   location, delivery method and any metafield marked filterable. Sorting is offered only on
   indexed columns rather than offered and slow. Selecting across pages selects a query
   rather than a page, states the count, and re-evaluates at execution while reporting the
   difference.
8. Five metric tiles sit above the index, reading `Orders`, `Ordered items`,
   `Returned items`, `Fulfilled orders` and `Delivered orders`, each with a period
   comparison, under a period control defaulting to `30 days`.
9. Saved views are named, ordered sets of a filter expression, a sort, a column list and a
   page size. The shipped system views are `All`, `Unfulfilled`, `Unpaid`, `Open`, `Closed`,
   `Automations`, `Return requests` and `Local Delivery`; they may be duplicated but not
   deleted or renamed. A view belongs to a store and is personal or shared. The filter
   expression is a structured tree of field, operator and value rather than a raw query
   string, so it can be authorized field by field. A store holds `50` shared views and a
   person `50` personal views per index, and views beyond the visible tab width collapse
   into a disclosure rather than being truncated invisibly.
10. Every order carries an append-only timeline of state changes, payments, refunds,
    fulfilments, edits, notes, messages sent, automations that fired and application actions,
    each recording actor, instant and source. Staff notes and system events are visually
    distinct and separately filterable. The timeline is a projection of the audit record for
    that resource, not a second write path: two independent histories of one object disagree,
    and the one people read is the one that will be wrong.
11. A duplicate submission from a channel is deduplicated on that channel's own order
    identifier, which is unique per channel per store. An order arriving for an archived
    product is accepted, because the line snapshot carries everything needed.
12. Cancellation after partial fulfilment is permitted for the unfulfilled remainder only,
    with the refund calculated for that remainder. Payment captured with fulfilment
    permanently failed leaves the order open and proposes a refund; it never silently closes.
### Money, the ledger and payouts

1. **Every movement of value is one balanced transaction of two or more entries.** A
   transaction sums to zero per currency and the database refuses one that does not, so a
   programming mistake cannot quietly create money. Entries are never updated and never
   deleted; a correction is a reversing transaction that references its original.
2. **The ledger is the source of truth for every money figure shown anywhere.** A figure
   computed by adding up orders is a different number, and when the two appear on adjacent
   screens the difference becomes a support ticket and then a loss of trust.
3. Balances are held per store, per currency and per kind, with kinds `available`,
   `pending`, `reserved`, `disputed`, `fee`, `tax`, `rounding`, `in_transit`,
   `gift_card_liability` and `store_credit_liability`.
4. A payment moves through `created`, `requires_action`, `authorized`, `captured`,
   `failed`, `voided`, `refunded` or `partially_refunded`, and `disputed`. Authorization
   expiry is stored on the payment, per method and per country, and an expiring
   authorization enqueues either a capture or a void rather than simply lapsing.
5. Payment method classes: card, tokenised as a token plus brand plus last four plus expiry
   with network tokens preferred; device and browser wallets, delegated, where the platform
   receives a token and never a card number; bank redirect, asynchronous, where the order is
   created `pending` and settles on a signature-verified idempotent callback; the unified
   payments interface, asynchronous with a collect request that may be pending for minutes
   and must render an honest pending state rather than a spinner; instalments and pay-later,
   where the provider decides and the merchant is paid in full; bank debit for business
   buyers, where a mandate is stored, later charges reference it, and revocation is honoured
   within one business day; cash on delivery, an offline method creating a `pending` order
   under a configured fulfilment hold; gift card and store credit, a liability balance
   decremented only on successful capture; and manual or offline, recorded with a method
   label and a reference by a member holding the permission.
6. A stored instrument requires explicit buyer consent recorded with its text and version,
   stores only a token with a display remnant, is usable at checkout, on a draft order and
   when paying an invoice with each a separate staff-side authorization, carries the correct
   indicator when charged with no buyer present, and is removable by the buyer, which
   cancels any scheduled charge against it and notifies the merchant.
7. A dispute moves through `opened`, `evidence_due`, `submitted`, `won`, `lost` and
   `expired`. Funds move to the `disputed` balance the moment it opens. Evidence is stored
   field by field and saved continuously so a half-assembled case is never lost, and the
   deadline drives notifications at decreasing intervals.
8. The platform charges a fee when a merchant processes elsewhere. The rate comes from the
   store's plan entitlement and is versioned, so a historical order is rated at the rate in
   force then. It is computed on the order total at order creation and stored on the order,
   accrued to the `fee` balance, settled against the next bill, and **itemised per order**,
   because an unexplained percentage is the most common billing argument there is. A
   merchant using the built-in processor accrues none, and the interface says so rather than
   showing a zero line.
9. The merchant's own subscription bills monthly or annually per the plan, prorates
   immediately on upgrade and at the period boundary on downgrade with the interface saying
   when, accrues platform fees and application charges during the period, and produces one
   invoice per store per period or one consolidated per organisation where the organisation
   elects it. The invoice number is allocated from a per-store sequence inside the
   finalisation transaction, because a gap in an invoice sequence is a regulatory problem in
   several jurisdictions.
10. Dunning: a notice on the due instant; a notice and an admin banner at `3` days; a
    notice, a banner and the `past_due` state at `7` days; a final notice naming the freeze
    date at `14` days; the `frozen` state at `21` days. **No data is deleted at any step**,
    and capability suspension in `past_due` never includes reading or exporting the
    merchant's own data.
11. Risk is scored per payment before authorization where the method allows, producing a
    score, a level and a signal list. The merchant configures allow, review or cancel, sees
    the level and the signals rather than a raw model output, and may manually accept a
    cancelled order, which is recorded against the model's feedback. A review queue holds
    the authorization and stores its expiry so it cannot silently lapse.
12. A payout is a set of ledger transactions joined through a payout item table, so it
    reconciles exactly to the entries that made it, on a daily, weekly or monthly schedule
    with a cutoff in the store's timezone. The settlement instrument is versioned rather than
    edited, so a payout always names the instrument in force at its cutoff; a new one
    requires verification and a hold period, and changing it is a dangerous action. A failed
    payout returns funds to `available` with a failure code, notifies, and does not retry
    until the instrument is re-verified. A statement is downloadable per payout and matches
    the ledger exactly.
13. Presentment and settlement amounts are both stored with the rate and its timestamp, and
    are never recomputed at read time. A rounding remainder goes to a dedicated balance, never
    silently absorbed.
14. Capture after the authorization expired is refused with a specific error; a new
    authorization is required and the buyer must be involved.

### Fulfilment, shipping and delivery

1. One order can leave from more than one place, so an intermediate **fulfilment order**
   sits between the order and its shipments, each with its own lifecycle, assignee and
   permissions. Modelling fulfilment directly on the order makes split shipments
   inexpressible, which is why that shape gets rebuilt.
2. Routing is an ordered list of rules, each a filter over a candidate location set, run top
   to bottom with rule `n` receiving the output of rule `n-1`. A rule that would empty the
   set is skipped and the skip is recorded. Rule types: minimise splits, ranked preference,
   proximity to the destination, stock sufficiency, capability match, capacity, and blackout.
3. **Routing is deterministic and explains itself.** The same inputs always produce the same
   assignment, ties break on a stated key rather than on database ordering, and every
   fulfilment order records the rule trace that produced its assignment, so a merchant asking
   why a parcel shipped from the far warehouse gets an answer rather than a shrug. Routing
   runs once at order creation and again on demand when a human reassigns.
4. A third-party fulfilment service registers a callback and declares the locations it
   serves. Assignment sends a request the service accepts or rejects with a reason; a request
   with no response inside a stated window escalates to the merchant rather than retrying
   forever; a cancellation is a request the service may refuse if the parcel has left, and
   the interface models that refusal; tracking is pushed, validated and deduplicated by
   tracking number; every call carries a key and every callback is deduplicated.
5. Buying a label is a money-moving action: it debits the merchant and writes ledger
   entries. Voiding within the carrier's window writes a reversing transaction. A purchase
   that debits and then fails to produce a label reverses automatically and reports. Buying
   labels for a selection is a job reporting per-order success and failure individually.
6. The order status page is public, addressed by a signed token, and shows state, tracking,
   a delivery estimate and the merchant's branding. Carrier events are normalised to a common
   vocabulary; a raw carrier code is never shown to a buyer. A delivery exception surfaces to
   the merchant as a task, not only to the buyer as a message.
7. Local delivery is per location: zones by postal code or radius, a rate, a minimum order
   and a delivery window, matched against the buyer's address at checkout. Pickup is per
   location: an enabled flag, instructions, preparation time and per-line availability, with
   `ready_for_pickup` and `picked_up` as fulfilment states carrying their own notifications.
   A pickup order appears on that location's terminal as a task.
8. Every hold carries its reason and the member who set it, and is visible and filterable.
   Hold reasons: risk review, payment pending, business-buyer order review, an automation, a
   manual hold, and backorder. **A parcel sitting still with no visible reason is the defect
   this rule exists to prevent.** Releasing requires its own permission and is audited.
9. An order routed to a location that then goes offline offers reassignment as a task rather
   than moving silently, because stock is already committed at the original location. A
   fulfilment service reporting a shipment for a cancelled order is recorded, the order
   reopens with a note and a human is tasked; the event is never discarded.

### Returns and exchanges

1. A return is its own process, not a refund with extra steps. Its states are `requested`,
   `approved`, `declined`, `label_issued`, `in_transit`, `received`, `inspected`,
   `resolved`, `cancelled` and `expired`. `expired` exists because a buyer who requests a
   return and never sends it must release whatever was held, and must be told before it does.
2. **Eligibility is computed from the order's own delivery instant**, not from its creation
   instant and not from today minus a window. A parcel delivered late must not consume the
   buyer's return window.
3. Self-serve: the buyer opens the order status page, selects lines and quantities;
   eligibility runs against the merchant's policy including per-product exclusions and a
   final-sale flag; a reason is selected from the merchant's list with an optional note and,
   where required, a photograph; the request is auto-approved or queued for staff per policy;
   on approval a label is issued or instructions are shown; on receipt staff record condition
   and a restock decision; the refund or exchange then executes and obeys the ceiling rule.
4. Restock decisions are `restock_sellable`, which increases `on_hand` with reason `return`;
   `restock_damaged`, which increases `damaged`; `restock_quality_control`, which increases
   `quality_control` pending inspection; and `do_not_restock`, which moves no stock and
   records the loss.
5. An exchange is a return plus a new linked order, never an edit of the original. The delta
   is computed and charged or refunded or issued as store credit per policy. If the
   replacement becomes unavailable between request and approval the buyer is offered
   alternatives or a refund; it never silently becomes a refund.
6. A return requested for a line already returned is refused with the prior return
   referenced. A buyer returning more than they bought is refused at line level against the
   ordered quantity. A refund on a discounted line uses the discount allocation stored on the
   line, not the list price.
7. **A return received without a request is recorded as an unmatched receipt at the location
   and surfaced as a task. It is never discarded.**

### Customers, segments and business buyers

1. A customer carries identity, consent state per channel with its collected instant, text
   version and source, many addresses with one default, derived commerce aggregates, tax
   exemptions per jurisdiction, and an optional link to one or more companies. Personal
   fields sit behind their own permission and are redacted at the serialisation boundary, so
   a support agent without it sees a masked address in every surface, in exports and in
   machine responses alike.
2. A segment is a stored expression over customer fields, order aggregates, product
   affinity, location, tags, consent state and metafields, materialised on a schedule and on
   demand with its last-evaluated instant shown. Its size is reported before use and a
   segment below a floor is flagged when used for messaging, because a segment of three is
   usually a mistake. **Messaging a segment intersects it with consent state at send time,
   never at definition time**, so somebody who unsubscribed on Tuesday does not receive
   Wednesday's campaign built on Monday.
3. Business buying is three levels and collapsing it into a customer with a flag does not
   survive the first real trade account. A **company** carries a name, an external
   identifier, tax registrations, default payment terms, assigned catalogs and an assigned
   representative set. A **company location** carries its own addresses, its own tax
   registration, and overrides for payment terms, catalog and buyer experience. A **company
   contact** names a customer, the locations they may order for, a spending limit, and
   whether they may place orders or only draft them.
4. A representative assignment is a row linking a membership to a company with a granting
   actor, a granting instant and an optional expiry. It resolves to a predicate restricting
   company, order, quote and price-list reads to assigned companies, and it grants the right
   to draft an order on behalf of a contact, which records both the representative and the
   buyer contact as separate actors. Reassignment transfers future access and does not
   retroactively hide history the representative legitimately saw; the audit records the
   transfer. A representative with no assignments sees an empty state naming who assigns
   companies, not an error. **The same mechanism serves location assignment for fulfilment
   operators and retail staff: one table, one predicate builder, used three ways.**
5. Quantity rules are per variant per catalog, so different buyers get different rules for
   the same variant: a `minimum`, a `maximum` and an `increment`. They are enforced at the
   storefront's quantity control which snaps to valid values and explains why, at the cart,
   at the checkout, at the draft-order builder, and authoritatively inside the
   order-placement transaction. **The message always names the rule that applies**, because
   "invalid quantity" on a wholesale order for eleven cases of twelve is uninterpretable.
6. Bulk ordering offers a variant matrix on the product page, a grid of the first option
   against the second with a quantity field per cell showing per-variant price and
   availability; a separate order form listing the whole catalog with quantity fields,
   searchable, filterable, paginated, with the running total pinned; and an upload of a
   delimited file of stock-keeping units and quantities, validated whole and reporting
   unmatched rows before anything is added. A matrix of a thousand cells must stay responsive.
7. A buyer portal carries order history, reorder, quotes, invoices and their payment,
   addresses, contacts and the company's price list. The merchant defines buyer roles within
   a company: who may order, who may only draft, who may pay invoices, who may manage
   contacts. **A buyer role is evaluated by the same policy component as staff**, against a
   buyer principal. There is one policy engine, not two. A buyer role that would grant more
   than the merchant's own staff role is refused by the same escalation guard.
8. Payment terms are net windows or due on receipt, per company and overridable per company
   location, producing an invoice with a due instant. A deposit is a percentage or a fixed
   amount taken at checkout with the balance invoiced, leaving the order `partially_paid`.
9. **An order review gate** decides which orders need staff approval before fulfilment, from
   the total, the company, the contact, whether it is that company's first order, the credit
   exposure and any metafield. A gated order is created, stock is committed, and the
   fulfilment order is held with a business-review reason. Approval is by a member holding
   the permission; the decision, actor and instant are recorded and the buyer is notified.
   Credit exposure is the outstanding invoiced amount per company computed from the ledger,
   compared against a per-company limit; exceeding it triggers review regardless of other
   rules. Reducing the limit below current exposure gates new orders, leaves existing orders
   alone and notifies the merchant.
10. A tax number per company per jurisdiction is validated against that jurisdiction's
    service where one exists, with the response and instant stored, and a validated
    registration may zero-rate or reverse-charge per that jurisdiction's rules. A compliant
    invoice is generated at finalisation with a sequential number per store per jurisdiction
    and stored immutably. A validation outage does not block the order: the registration is
    marked unvalidated, standard tax applies, and the merchant is tasked.
11. A contact belonging to two companies is permitted; the ordering context is selected
    explicitly and shown at all times. Deleting a company with open orders is refused; it
    archives and the orders keep their snapshots. A quote holds its terms until expiry even
    if quantity rules change; a reorder is validated afresh.

### Markets, catalogs and price lists

1. A market is a named audience plus the settings that apply to it, of type `region`, `b2b`
   or `retail`, in state `draft`, `active` or `inactive`. Its membership is countries or
   subregions, or companies and company locations, or locations. It carries a currency and
   its rounding rule, a published language set with one primary, a domain or a path prefix,
   a catalog, a tax treatment and an optional theme override.
2. **Markets inherit, and inheritance is resolved rather than copied.** A setting resolves from the market, then its parent chain, then the
   store default, and the first explicit value wins. The interface shows, for every setting,
   whether it is set here or inherited and from where, and the count of overridden settings
   is what the market index displays beside each market. Chains are bounded at `4` levels;
   deeper is refused because both resolution cost and human comprehension fail. A parent
   reference is validated against the ancestor set on write, so a cycle is structurally
   impossible.
3. A catalog is a set of products with a price list, assignable to a market or to a set of
   companies and company locations, with an explicit product set or a rule or the whole
   catalog minus exclusions, published per channel. Creating one beyond the plan's cap is
   refused with the cap and the plan named.
4. A price list carries a percentage adjustment relative to the store price, per-variant
   fixed overrides that beat the adjustment, and per-variant volume breaks as an ordered set
   of minimum quantities and their prices. **Resolution order is company catalog, then market
   catalog, then store price, first match wins, and the resolution is recorded on the order
   line** so a price can be explained afterwards.
5. **Price resolution is one function**, used by the storefront, the cart, the checkout, the
   draft-order builder, the machine interface and the terminal. Six implementations of price
   resolution is six different prices, and the first anyone hears about it is a customer
   being charged one thing and shown another.
6. A view-as control pairs a country with a channel and renders the buyer surface as a buyer
   in that market would see it, **using the same resolution path as a real request**. A
   preview that is approximately right is worse than none, because people trust it. It never
   writes; carts created in preview are marked and excluded from analytics. It requires the
   market read permission, and previewing a business market additionally requires the company
   constraint to permit it.
7. A market may own a hostname, a subdomain or a path prefix. On the primary domain with no
   prefix, negotiate from the buyer's country signal and language and redirect; never vary a
   cached body. Every rendered route emits a canonical link and one alternate per published
   market and language. Changing a market's domain issues permanent redirects from the old
   form for a stated minimum period, because search ranking is the merchant's asset.
8. A country belongs to at most one region market per store; an overlap is refused at write
   time. A buyer whose country is in no market falls back to the store's primary market and
   the merchant is warned. A price-list entry whose variant no longer exists is retained and
   marked orphaned rather than deleted, so a restore does not lose the price. Two markets
   claiming one domain is refused. Deleting a parent while children exist is refused.

### Discounts, promotions and gift cards

1. Discount kinds: order percentage, order fixed, product percentage or fixed, buy-X-get-Y
   with a maximum uses per order, free shipping optionally capped, automatic where conditions
   match, and code-based with one code or a bulk-generated set.
2. Conditions are minimum subtotal, minimum quantity, customer segment, company, market,
   channel, first order only, product or collection membership, and a date window. They
   compose with an explicit conjunction; there is no implicit "and everything else".
3. **A discount is allocated across the lines it applies to and the allocation is stored on
   each line.** The allocation sums exactly to the discount amount and the residual smallest
   unit goes to a stated line by a stated rule, never lost. Allocating one hundred rupees
   across three lines by naive division loses a paisa, and a store running that promotion ten
   thousand times has books that do not balance. A refund uses the stored allocation, so
   refunding one of three discounted items returns the right amount. Taxes recompute after
   allocation.
4. Stacking. Each discount declares which classes it combines with. Product discounts apply, then
   order discounts, then shipping discounts. Promotional discounts stack on top of price-list
   prices rather than replacing them. A staff-created discount is bounded by the actor's
   discount ceiling, and above it becomes an approval request. Where two discounts of one
   class match and neither combines, the one giving the buyer the larger benefit wins and the
   choice is recorded.
5. **A code good for one use survives a thousand simultaneous attempts with exactly one
   redemption.** The other attempts receive an explicit exhausted message. Checking whether a
   code has been used and then marking it used are two steps, and four hundred people fit in
   the gap, so the total-uses limit must be settled in one indivisible step at the database.
6. Per-customer limits are enforced against the customer identity where one exists and
   against the checkout otherwise, with that weakness acknowledged. Bulk codes are generated
   asynchronously in batches with a stated ceiling. Codes that are not human-chosen are
   high-entropy, and code validation is rate-limited per network prefix.
7. A gift card is a code, a balance, a currency, an expiry where the jurisdiction permits
   one, and an issuing source. **Its outstanding balance is a liability on the ledger**:
   issuing one is a ledger transaction, not a row update. It decrements only on successful
   capture, so a failed capture leaves the balance intact and there is nothing to correct.
   Expiry writes a transaction releasing the liability rather than zeroing a column. Codes
   are stored hashed with a display remnant and lookup is rate-limited, because a gift card
   balance is cash. Store credit is the same mechanism with its own liability balance and no
   transferable code.
8. A discount whose condition stops being met after the cart changes is removed and the
   buyer is told which condition failed.
### Checkout and the buyer surface

1. Checkout is served from its own prefix, renders no merchant-authored template, and runs
   no merchant-supplied and no application-supplied code beside a payment field. It reads a
   cart snapshot rather than a live theme, so it survives a storefront failure, and it is
   optimised independently of any theme.
2. A checkout session is created from a cart, producing an immutable line snapshot plus a
   mutable buyer section. Its token in the address is treated as a credential: not logged,
   not leaked in a referrer, expired aggressively. It idles out after `1` hour and expires
   absolutely after `24`, and both release reservations. An abandoned checkout is recoverable
   by a signed single-use link valid for a configured window. The currency is fixed at
   creation from the market and never changes mid-checkout.
3. Steps are express, contact, delivery, delivery method, payment and, where the merchant
   enables it or a business rule requires it, review. **The address form is per country**:
   which fields exist, which are required, their labels, their order and their validation are
   per-country data, never a fixed set of fields with country-specific labels bolted on.
   India renders `Province` with its state list and a six-digit postal code; another country
   renders its own. Every field carries the correct autofill token. Autocomplete is a
   dismissible suggestion list that never overwrites a field the buyer has edited, and if the
   suggestion service is unavailable the form works as a plain form.
4. Stock is reserved while the checkout is open and released on completion, expiry or
   explicit abandonment; a sweeper releases expired reservations. If a reservation cannot be
   taken the buyer is told which line is short and by how much and is offered the available
   quantity. **The reservation is a courtesy; the order-placement transaction is the
   authority.**
5. Delivery options are shipping from the merchant's own rate table or from a carrier where
   the plan entitles it, pickup at locations with pickup enabled showing per-location
   availability of every line, and local delivery matched by zone. A carrier timeout falls
   back to the merchant's table, never to no options. Delivery dates are shown as dates
   rather than ranges where the merchant configures them.
6. The payment method set resolves from the market, the buyer's country, the currency, the
   amount and the merchant's configuration, in that order, and is presented in groups:
   express wallets, cards, bank-redirect methods, instalments, buy-now-pay-later, gift card
   and store credit, and offline methods. Card fields render inside an isolated frame served
   by the payment layer and the surrounding page never reads them. Every payment attempt
   carries an idempotency key; a double submit yields one charge.
7. Tax is calculated at the market and address level. The summary line reads
   `Estimated taxes` until the order is placed. Duties are shown where the market prepays
   them and otherwise stated as payable on delivery. A tax service timeout falls back to the
   merchant's own rates with the order flagged for review, never to zero.
8. Checkout branding is available on every plan from a constrained token set, along with
   which optional fields appear and their requirement level. Declared extension components at
   declared insertion points are a top-plan capability, sandboxed, with no access to payment
   fields and a hard timeout. **No extension may delay the submit path beyond its budget or
   prevent order placement**; one that exceeds its budget is disabled for that session and
   the session continues.
9. **Payment succeeded and order creation failed is the worst case in the system.** The
   payment is automatically voided or refunded, the buyer is told, and a reconciliation sweep
   finds any case that slipped through. It is never left to chance.
10. A buyer returning to a completed checkout gets the order status page; the checkout is
    not replayable. A duplicate submit produces one order. An invalid discount names its
    reason: expired, limit reached, not applicable to these items, minimum not met. A gift
    card that partly covers the total charges the remainder elsewhere and decrements only on
    successful capture of the whole. A session that expires mid-payment returns the buyer to
    a recoverable state with the cart intact.
11. **The whole checkout works as a sequence of plain form submissions with client scripting
    unavailable and with motion reduced.** On a payment surface that is the accessibility
    floor, not a fallback.

### Online store, themes and content

1. A theme is a store's name for a set of templates. A template is a page kind plus an
   ordered section list with per-section settings. A section is a reusable unit declaring its
   settings and its permitted block types. A block is a typed, ordered child of a section.
   The theme declares its own settings schema of colours, type, layout and per-section
   defaults. A theme's role is `main`, `unpublished` or `development`.
2. The editor is two panes: an outline tree and a live preview. Selecting in either selects
   in the other. **Reordering has a keyboard equivalent**, move up and move down as commands
   with announcements; drag-only reordering is an accessibility failure. The preview renders
   through the real storefront pipeline with unsaved changes applied, not a simulation.
   Changes stage and publish as one version; there is no partial live state. Every publish
   creates a restorable version with an actor and an instant. Two editors on one theme: the
   second is warned and may take over, which locks out the first with a message, because a
   silent overwrite loses an afternoon of work. A shareable expiring preview link needs no
   admin session, carries no admin capability and is excluded from indexing.
3. Content beyond the theme: pages with rich text; blogs and articles with author, tags and
   moderated comments where enabled; menus as named nested link trees referenced by themes;
   **metaobjects**, merchant-defined structured content types with typed fields referenced
   from templates, which is what lets a merchant add a size guide or care instructions as
   structured data rather than pasted markup; files; and redirects from path to path with a
   reason.
4. The rendering pipeline resolves hostname to store and market, resolves route to a
   template kind and a resource, authorizes publication state and market and catalog
   membership, resolves prices through the single resolver, renders template plus sections
   plus data on the server, and caches per market, per language, per currency and per
   publication state. **Personalisation happens only through declared client-side islands
   hydrating against a separate uncached endpoint, never by varying the cached document.** A
   cart badge, a recently-viewed list and a customer name are all islands. Varying the cached
   page by buyer destroys the cache and is the most common cause of a slow shop.
5. The storefront read interface is separate from the admin interface with its own credential
   class, exposes published resources only resolved through market and catalog, cannot
   express a query for an unpublished product, bounds query cost per request, and produces
   responses cacheable by their resolved key with no buyer identifier in the key.
6. Search-engine surface: one canonical per resource per market, with a product reachable
   through a collection canonicalising to the product; one alternate per published market and
   language; structured data for product, offer, breadcrumb, article and organisation emitted
   from the same data the page renders; sitemaps per market, paginated, regenerated on
   publication change; robots per market with unpublished markets and preview links excluded;
   and a permanent redirect on a handle change with the old handle reserved against reuse.
7. Headless rendering uses the same storefront read interface and nothing privileged. Its
   credential is public by nature, scoped to published market-resolved reads, rate-limited by
   cost, and incapable of any mutation beyond cart operations. The cart identifier is the
   credential for that cart. Checkout is handed off; a headless storefront does not implement
   it.
8. Publishing a theme referencing a deleted section is refused at publish with the template
   and the section named. **A section that fails at render renders nothing, the page renders,
   and the failure is logged with the section key and the route.** Removing a metaobject field
   while templates reference it is refused with the references listed.

### Sales channels and the agent surface

1. A channel carries a kind, a state, a credential reference, a configuration and the
   capabilities it supports. Kinds: online store, point of sale, social, marketplace, buyer
   application, assistant surface, and custom. Every order records its channel and the order
   index filters by it.
2. **A channel declares its capability set at registration and every surface derives its
   behaviour from that set.** The capabilities are `catalog_sync`, `order_ingest`,
   `checkout_here`, `checkout_there`, `inventory_sync`, `fulfilment_there` and
   `returns_there`. A hard-coded per-channel branch in the order pipeline is the defect this
   exists to prevent, and it is what makes the fourth channel unmaintainable.
3. Catalog and inventory push out; orders and returns come in. Synchronisation is
   event-driven from the outbox rather than a nightly sweep, with a scheduled full comparison
   per channel that **reports differences rather than blindly applying them**. Updates apply
   in order per resource; out-of-order delivery is detected by a monotonic version on the
   resource and the stale update is dropped. A channel that is slow or failing gets its own
   queue paused with an alert and does not consume the shared worker pool. A channel without
   `inventory_sync` simply does not receive those events.
4. Ingestion deduplicates on the channel's own order identifier, unique per channel per
   store. Products match by the channel's own reference and an unmatched line creates a
   custom line rather than rejecting the order. An order that settled on the channel arrives
   with its payment recorded as an external settlement, producing ledger entries describing
   money the platform never held. Stock is committed on arrival, and a channel that oversells
   against a stale catalog produces a backorder and an alert. Channel buyers may be anonymous
   and a customer record is created only where the channel supplies enough to make one
   meaningful.
5. The agent surface publishes a machine-readable catalog document per market carrying price,
   availability, variant structure and the merchant's policies, at a well-known path, cached.
6. **An agent is never taken at its word.** It must present both an agent credential and a
   buyer authorization. An agent credential alone may read a catalog and may not create an
   order. The agent either hands the buyer a completion surface or completes the purchase
   with a delegated payment credential the buyer has explicitly scoped; the platform never
   accepts a bare assertion that a buyer consented. Every agent-initiated order records the
   agent, the delegation, its scope and its expiry. A delegation that expires mid-checkout
   requires the buyer to finish directly.
7. The merchant stays in charge: per market and per channel they opt in, opt out, or opt in
   with a review gate. Agent traffic is rate-limited separately from storefront traffic,
   because a catalog crawl is a different load shape from a storefront visit. Agent-originated
   orders are attributed to their agent and the merchant can act on that. An agent whose
   orders are systematically cancelled or disputed is rate-limited, then suspended, per
   merchant and platform-wide, with an appeal path.
8. A channel credential revoked by the channel pauses synchronisation, notifies the merchant
   with a reconnect path, and retains queued events for a stated window. A product
   unpublished while an order is in flight on the channel: the order is accepted, because
   publication controls discovery and not acceptance. A cancellation for an already-fulfilled
   order is recorded, raises a task, and causes no automatic refund.

### Applications, extensions and the partner platform

1. An application declares its partner owner, its kind as public or custom, its requested
   scopes, its callback addresses, its event subscriptions, its extension declarations and
   its listing metadata. An installation is per store, never per organisation; installing
   across an organisation is a loop of individually consented installations.
2. Scopes mirror the permission vocabulary, split read and write. The consent surface lists
   every scope in plain language, grouped, with the dangerous ones separated and visually
   distinct. **An installation can never exceed the permissions of the member who installed
   it**, checked at install and re-checked when that member's permissions shrink. An
   application requesting a new scope after installation requires fresh consent from a member
   holding that permission; it can never silently gain capability on an update. Scopes
   covering personal data, order exports and payment data require an extra approval step and
   are separately audited. Uninstalling revokes credentials immediately and puts the
   application on the clock to delete the data it holds, with compliance tracked.
3. An installation token is opaque, rotatable with an overlap window and individually
   revocable, stored hashed with the plaintext shown once at issue and never again, bound to
   live or development and unable to cross, rate-limited per installation by cost, and
   attributed in the audit record as the application rather than as a generic system actor.
4. Extension points are five: a declared page or panel inside the admin shell, in an isolated
   frame that cannot read the admin session; a declared theme section a merchant can add in
   the editor, rendered on the server from the application's own template against a bounded
   data contract; a checkout extension on the top plan only; a buyer portal extension; and a
   declared tile on the retail surface under the same offline constraints as that surface.
5. **The sixth kind changes the architecture: a function.** A deterministic sandboxed
   computation the platform invokes inside its own pipeline to compute a discount, filter a
   delivery option, filter a payment method or rank a routing location. It gets no network
   access, no state between runs, and a hard instruction and time budget. **A function that
   exceeds its budget is skipped and the platform's default applies; it must never fail the
   checkout.** Functions are pure and their outputs are proposals the platform applies, so a
   function that mutates state is structurally impossible.
6. Isolation is structural. The host passes capabilities, not tokens: an extension needing to read an order receives a
   read function scoped to that order, not a credential. A content policy is declared per
   extension and enforced by the host, and the extension cannot widen it. An extension that
   fails renders its own error region and the host surface stays usable. Time and memory
   budgets apply per extension per render, and exceeding one disables the extension for the
   session and notifies the merchant.
7. Application billing is one-time, recurring with the merchant's own bill, or metered with a
   merchant-approved cap where a charge beyond the cap is refused rather than queued. Every
   model requires an explicit merchant approval surface showing the amount and the term. An
   unpaid application charge suspends the application, not the store.
8. Listing review precedes publication: scope justification, a data-handling declaration and
   a functional check. Automated checks cover callback reachability, signature verification
   and a scan for credentials committed into the extension bundle. Error rate, latency and
   rate-limit rejection are monitored per application, and one degrading the merchant
   experience is slowed with its partner notified. A compromised application is suspended
   platform-wide, its credentials revoked, and every affected merchant told what it could
   reach.
9. An installing member who loses their permissions freezes the installation's scopes: it
   keeps working but cannot escalate, and the store is notified. An application uninstalled
   while a job it started is running lets the job finish under a system principal, attributed
   to the application. Two applications writing the same metafield: the later write
   replaces the earlier one, both are shown in a conflict view, and the merchant is
   never left with a mystery. A development application on a live
   store is refused.

### Automations

1. A merchant-authored workflow is a node graph of a `trigger`, `condition` nodes with
   `Then` and `Otherwise` ports, and `action` nodes each with an `Output` port. A run
   executes the workflow version it started with, so editing a workflow does not change runs
   already in flight.
2. Triggers are resource events, a `Scheduled Time` trigger carrying a named timezone and a
   named schedule, a manual run against a selection from an index, or an event an installed
   application emits. **Named zones, never offsets**: a workflow scheduled at nine in the
   morning stays at nine across a daylight transition.
3. A condition evaluates a structured tree of field, operator and value over the triggering
   resource and anything prior steps fetched, with comparison, membership, presence, string
   match and date arithmetic relative to the run instant. **Both branches are always
   present**: a condition with only a `Then` silently discards the other case. Field access
   is subject to the workflow's effective permissions.
4. Actions are resource mutations, communications, invocations of an action an installed
   application declares, and control actions: wait until an instant or a duration, wait for a
   condition with a timeout, and branch on parallel outputs.
5. **A workflow runs with the intersection of the activating member's permissions and an
   explicit permission declaration on the workflow, and can never perform an action its
   activator could not perform directly.** If the activator's permissions shrink the workflow
   is suspended and the store is notified rather than silently downgraded mid-run. Activating
   one containing a money-moving action is a dangerous action.
6. Execution is at-least-once, so every action is idempotent or guarded by a key. Steps retry
   with a widening gap up to a ceiling, then the run fails with the step identified. Timeouts
   apply per step and per run and a run exceeding its ceiling fails visibly rather than
   hanging. The graph is acyclic and a workflow whose action re-triggers itself is stopped by
   a per-resource depth counter with an alert. Runs for one resource are serialised so two
   events for one order do not race. Runs are metered and a store exceeding its allowance is
   slowed with notice.
7. **Every workflow can be dry-run against historical data with no effects, reporting what it
   would have done.** That is what makes an automation safe to activate: nobody should have to
   find out what their automation does by watching it do it.
8. Shipped templates, each composing a trigger, a condition and two or three actions:
   `Capture payment if order is not high fraud risk` under `Risk`;
   `Get notified by email when product variant inventory is low` under
   `Inventory and Merch`; `Payment Reminder sent after due date` under
   `Orders, Payment Reminders`; `Cancel and restock high risk orders` under `Risk`;
   `Submit fulfillment request for paid orders that use a specified fulfillment service`
   under `Orders, Fulfillment`; and `Hide and republish products based on inventory level`
   under `Inventory and Merch`.

### Notifications

1. Five classes, and the separation is legal as well as architectural: transactional to a
   buyer, on the basis of the transaction, with no marketing content permitted inside it;
   marketing to a buyer, on explicit or implied consent per country; operational to a staff
   member, on their role and preferences; security to a staff member, never suppressible;
   and platform to a store's billing and technical contacts, never suppressible for billing
   and service matters. **A transactional template draws from a restricted block set that
   contains no promotional block**, because a receipt carrying a promotion becomes a marketing
   message in several jurisdictions.
2. A template exists per event per locale with a versioned merchant override, declares the
   fields it may use, and resolves its locale from the buyer's, then the market's primary
   language, then the store default. It previews with sample data at every locale and sends a
   test to a verified address. A merchant override that fails to render falls back to the
   platform default and alerts the merchant: a failed template never means an unsent
   transactional message.
3. Buyer notifications cover order confirmed, order edited naming what changed and the cost
   delta, payment failed or action required with a resume path, each fulfilment state,
   returns at approval and label and receipt and refund, abandoned checkout recovery as a
   capped marketing message, invoices and their due reminders, and account creation and
   sign-in codes.
4. Staff and merchant notifications cover an approval requested, reminded, escalated, decided
   or expired; a dangerous action performed, to the owner; a sign-in from a new device or a
   credential or factor change, to the person on every known channel; payouts paid, failed or
   instrument-changed, and disputes opened, due and decided, to finance-role holders; low
   stock, batched, to fulfilment-role holders; an integration failing or a delivery target
   disabled, to the store and the partner; a failed plan payment; and a completed or
   downloaded data export.
5. Double opt-in is required for every marketing subscription. **Unsubscribing is one click,
   needs no sign-in, has no confirmation step, and takes effect within seconds rather than at
   the next send.** A suppression list is global per store and honoured by every send path
   including applications and imports; an import that re-adds a suppressed address does not
   resurrect consent.
6. A merchant-owned sending domain is used only once its authentication records verify, and
   the verification state is visible and re-checked on a schedule. A hard bounce suppresses
   immediately; a complaint suppresses and records; rates are visible per store. Under
   pressure marketing is slowed ahead of transactional, so a customer waiting for confirmation
   that their money was taken is never behind forty thousand promotional messages. Every send
   carries a key derived from its event so a retried job does not send twice. Operational
   notifications batch on a short window, so a bulk import produces one summary rather than
   four thousand messages. Quiet hours are configurable per person for operational classes and
   never applied to security or transactional ones.
7. A message provider outage queues transactional messages with a stated maximum age, past
   which they surface in the admin as undelivered so a human can act.

### Analytics and exports

1. A fact is an immutable row derived from an event. Dimensions are time, channel, market,
   location, product, variant, collection, customer segment, company, staff, campaign, device
   and country. Measures are sales, orders, units, average order value, conversion, sessions,
   returns, refunds, gross margin where cost is known and permitted, fees and payouts. The
   grain is stated per report, because a report whose grain is ambiguous produces numbers
   nobody can reconcile.
2. **Every money measure reconciles exactly to the ledger for the same period and the same
   filter, and a scheduled comparison alerts on any difference beyond zero.** Not a tolerance:
   zero. Money reported and money recorded are the same money.
3. Every period boundary is computed in the store's named timezone. The default comparison is
   the immediately preceding period of the same length, aligned to the same weekday where the
   period is a multiple of a week. A period including today is labelled partial and never
   compared against a complete one without saying so. A retail location's day runs from
   register open to register close rather than midnight to midnight.
4. Register sessions record open and close instants, opening and closing float, expected and
   counted cash and the variance, per session and per associate, behind its own permission. A
   sale attributes to the location, the register, the associate and the day the session
   defines. **An offline sale attributes to the instant of sale, not the instant of
   synchronisation, and is flagged as having arrived late**, so a closed day's figures changing
   is explainable rather than an accusation.
5. Honesty rules: every surface states when its data was last updated; any approximate measure
   is labelled with its method named; session and visitor counts are approximate by nature and
   never presented beside exact money without distinction; the attribution model is stated on
   the report rather than one number presented as the number; **a measure with no data renders
   as no data, never as zero**; and a total under a filter says it is filtered.
6. Exports are always asynchronous. They require the analytics export permission and
   additionally the customer or order export permission where they contain those resources,
   and a personal-data export is a dangerous action. **Fields the actor may not read are
   absent from the artefact**, because an export is the most common way a field-level
   permission is bypassed. The artefact is signed, expiring and single-audience, and its
   download is audited with the actor and the address. The format is a delimited file with a
   documented schema and a header, plus a machine format. Completion notifies with the row
   count and the filter restated.
7. A refund in a later period than its order is reported on the instant the money moved, and
   order-level views show it against the order and say so. An order cancelled after its period
   closed restates the period visibly rather than silently. A store changing timezone records
   the change instant and reports spanning it say so; historical periods are not recomputed. A
   multi-currency store's totals are per currency and are never summed without an explicit,
   dated conversion. When the analytics store is behind, the freshness indicator says so and
   money surfaces fall back to the ledger, which is always current.

### Audit, consent and data governance

1. **Every mutation of a governed resource writes an audit entry in the same transaction as
   the mutation.** There is no path that writes without auditing. Every entry names a
   principal: a person, an application installation, or a named system process. There is no
   anonymous system actor.
2. An entry carries the organisation and, where applicable, the store; the actor type and
   identifier; the on-behalf-of actor where a representative acted for a buyer; the action
   from the closed vocabulary; the resource type and identifier; the changed fields only,
   before and after, with sensitive values reduced to a hash so a change is provable without
   the value being readable; the address, user agent and session; the correlation identifier
   shared with the request, the job, the event and any approval; a severity of informational,
   notable, dangerous or security; a database-assigned instant; and the previous entry's hash
   alongside its own.
3. **The record is append-only, enforced by database privilege rather than by convention, and
   hash-chained per organisation.** A verifier walks the chain and reports the position of the
   first break. The chain head is published to an append-only external store on a schedule so
   a whole-chain rewrite is detectable too. A detected break alerts at the highest severity
   and **the chain is not repaired, because a repaired chain proves nothing**. A merchant
   asking to delete audit entries is refused.
4. What is audited: authentication events; every denial of a dangerous action; every
   permission, role and membership change; every dangerous action; every money movement; every
   stock adjustment whose reason is not a sale; every price change; every export and every
   download of one; every access to sensitive personal fields; every application install,
   scope change and uninstall; every credential issue and revoke; every theme publish; every
   setting change; every approval request and decision; every workflow activation and every
   money-moving workflow action; every data-subject request and its fulfilment; and every
   break-glass sign-in. Ordinary reads are not audited, because auditing every read produces a
   record nobody can search, which is the same as no record.
5. A dangerous action requires, in addition to a permit: a fresh authentication within `15`
   minutes, an enrolled second factor, a confirmation naming the exact effect and its
   magnitude **whose confirming input is the resource's own identifier rather than the word
   yes**, an audit entry at high severity, and an asynchronous notification to the store owner.
   The dangerous set: editing permissions, removing a member, managing roles, changing or
   cancelling the plan, editing the settlement instrument, managing the payout schedule,
   editing payment settings, managing application scopes, exporting customers or orders or the
   audit record, deleting a product, activating a money-moving automation, and any refund above
   ceiling.
6. Every consent captures its purpose, its state, the exact text and its version, the instant,
   the source surface and the address. Purposes are separate: marketing email, marketing
   messaging, analytics, personalisation, and any purpose an application declares. Withdrawal
   is as easy as granting and propagates to every consumer including applications, which are
   notified. A consent record is producible on demand for a named subject and purpose. Where a
   jurisdiction requires opt-in, no purpose defaults to granted.
7. Every column is classified as not personal, personal, sensitive personal or payment, in the
   schema, machine-readable, and that classification is the source for redaction, export and
   retention. Sensitive personal and payment fields are encrypted at the field level under an
   organisation-scoped key held in the organisation's region. **Personal data never enters an
   application log, a trace attribute, an error report or an analytics event**, enforced by a
   redaction layer at the emit boundary plus a scanner in the build, because relying on
   discipline fails. Storefront attribution is discarded once an account exists.
8. Data region is chosen at organisation creation and is immutable. Every tenant row carries
   its region so a region predicate never needs a join. Personal data is processed and stored
   in its region; cross-region movement requires an explicit logged transfer with a lawful
   basis recorded. Keys and backups stay in region. Support access is region-scoped and
   separately audited. Aggregates leave the region only when non-identifying, and the
   aggregation is specified rather than assumed. A region migration is an export and a new
   organisation, not a setting.
9. Retention defaults: the event log `7` days; delivery attempts `30` days; sessions their
   absolute expiry plus `30` days; abandoned checkouts `90` days; customer personal data per
   merchant policy bounded by jurisdiction; order records per financial regulation, typically
   far longer than personal data; the audit record at least `1` year and typically `7`; and
   the ledger and invoices indefinitely. Records a regulation requires are retained with their
   personal fields anonymised rather than removed.
10. A data-subject request is one of access, portability, erasure, rectification or
    restriction, each with a stated window per jurisdiction, tracked, with escalation before
    breach. **Erasure covers the primary store, the analytics store, the search index, the
    cache, the event log and every backup restore path**, and propagates to every installed
    application holding the data with completion tracked and reported; an application that does
    not confirm is escalated and then suspended, and the merchant is told which one is holding
    data. A subject deleted from the primary store and present in the search index is not
    deleted. Erasure replaces personal fields with a stable non-identifying token so the
    commercial record still reconciles. **Restoring a backup replays the erasure log before the
    restore goes live**, as part of the restore procedure rather than as an afterthought. An
    erasure request for a subject with an open dispute is deferred with its lawful basis
    recorded and the subject is told when it will complete.
11. Records with a regulatory life of their own: a tax invoice, immutable once finalised and
    sequentially numbered per store per jurisdiction with no gaps; a credit note, treated the
    same, because a correction is a credit note and never an edited invoice; the ledger; and
    consent records, retained beyond the subject's other data because they are the proof that
    processing was lawful.

### The public storefront

1. The marketing storefront is country-segmented: the country is the first path element and
   is present on every route except the global root. A second language is a sibling path,
   never a query parameter and never a cookie-only switch. A trailing slash redirects
   permanently to the canonical form.
2. **Changing the country changes more than the language**: the prices, which plans exist,
   which capabilities are on sale there, which articles are in the library, how numbers are
   written, how dates are written, and which media plays behind the headline. The captured
   instance quotes rupees in Indian digit grouping, carries a fully translated sibling in
   Devanagari, and advertises `24/7 local chat support` as a plan line.
3. Resolution order: an explicit country segment in the path always wins and is never
   overridden by a header or a cookie; an explicit language suffix wins for language; on the
   global root only, negotiate from the request's country signal and accept-language header
   and issue a temporary redirect to the resolved storefront; a stored preference set by the
   visitor using the locale control is consulted only at that step; and if no storefront is
   published for the resolved country, serve the global root with the locale control opened
   pre-filtered to that country. **Negotiation never varies the response body at a cached
   path.**
4. Formatting: currency from the locale's own convention, never a symbol concatenated with a
   number formatted for another locale; the Indian grouping convention groups the lowest
   three digits and then every two above them; large numbers use the locale's convention,
   lakh and crore on the India storefront; dates use the locale's format, day then abbreviated
   month then four-digit year on the India storefront; percentages and multipliers render as
   written in the source copy, because they are claims rather than computed values; and the
   product supports right-to-left, with every directional icon mirrored and every inline
   offset expressed on the logical axis rather than as left and right.
5. **The plan lines are not marketing copy; they are entitlements the software enforces at
   write time with the plan named in the refusal.** `staff_seats` is enforced at invitation
   acceptance and at membership reactivation; `inventory_locations` at location creation;
   `b2b_catalogs` at catalog creation; `market_customisation` at a market setting override;
   `checkout_customisation` at extension installation on checkout; and
   `carrier_calculated_rates` at carrier configuration and at checkout rate resolution. `Up to
   5 staff accounts` means the back room refuses the sixth. **An entitlement reduction on
   downgrade never deletes data**: resources above the new cap become read-only, within a grace
   window, and the merchant chooses what to remove.
6. The plan comparison carries a billing toggle labelled `Pay yearly` that rewrites every
   price cell on the route. **Prices come from the server already worked out; the toggle
   selects among values already delivered and never computes one**, because a discount
   calculated in the browser is a discount somebody can edit. The toggle writes a query
   parameter so a shared link opens on the same term, both price strings are measured so the
   cell reserves the wider and nothing shifts, a plan not sold on a term renders `-` and its
   call to action becomes the sales path rather than a disabled control with no explanation,
   and the switch announces its state with the rewritten prices in a live region.
7. A capability route template serves roughly thirty routes and carries, in order: an eyebrow
   naming the capability, a hero with a heading and a body and one or two calls to action and
   one product graphic, an optional proof strip of three statistics or a logo wall, an optional
   sticky sub-navigation of two to four sub-topics, two to six alternating feature pairs, an
   optional dense feature grid, an optional tab set of customer evidence, optional questions,
   a closing conversion band, and a numbered footnote list matching every superscript marker
   above. **Every statistic carries a marker, every marker resolves to a footnote, every
   footnote links back, and a claim with a dangling marker does not ship.**
8. A small uppercase plan badge renders inline with a feature name and reads the lowest plan
   that includes it. **The badge and the comparison table read from the same entitlement
   source**, so a badge saying one thing and a table cell saying another is impossible by
   construction rather than by review.
9. A capability not sold in a country is handled in exactly one of three ways, recorded as
   data on the capability per country and never as a hard-coded country test inside a
   template: hidden, where the route is unlinked and answers not-found there; gated, where the
   route renders with an availability notice in place of its call to action; or waitlisted,
   where it renders with a notice and a registration form.
10. Conversion paths end in one of four surfaces: trial signup, a sales conversation, an
    application install, or a newsletter subscription. **A control that deep-links into the
    admin degrades to the trial signup when no session cookie is present and never reveals by
    its rendering whether a session exists**, because the storefront is cached per market and a
    per-visitor variation would either poison the cache or force it off. The retail route is
    the one route offering both paths at every conversion block, because a retail visitor is
    disproportionately likely to be an existing customer already.
11. Every storefront form obeys one validation model: validate on blur for a field the
    visitor has left and on submit for the whole form, never on every keystroke; once a field
    has shown an error, re-validate on input so the error clears as it is fixed; put the
    message beneath the field, associated with it, so it is announced when focus enters; say
    what is wrong and what to do, never `Invalid`; on a failed submit put a summary at the top
    listing each failed field as a link to it and move focus to the summary; enforce every rule
    again on the server, where the client copy is a convenience; **return every entered value,
    because losing a filled form is a defect**; disable the submit control and announce a busy
    state on submit; and carry a client-generated key on every submission so a double submit
    produces one record.
12. Anti-abuse on those forms: a token bucket per address and per network prefix; a challenge
    only after a suspicion threshold, never on the first attempt and never one that requires
    vision alone; an unattended decoy field that must remain empty, carrying an accessible
    label and removed from the tab order; a submission faster than a human floor treated as
    suspicious rather than rejected; and disposable addresses flagged for routing rather than
    silently rejected. **A form submitted by a bot is refused: either the decoy field is
    filled, or the same form is submitted repeatedly in quick succession.**
13. The editorial index is per country rather than translated from one source, which means an
    article is stored per locale rather than as one record with translations hung off it. It
    carries a slug unique per locale, a title, a standfirst, one primary topic, tags, an
    author, published and updated instants, a locale, a rich-text body, related articles and a
    derived cached reading time. An article withdrawn answers gone rather than not-found, with
    the topic index linked. A locale missing an article simply does not show it, and never
    renders it in another language without saying so.
14. Editorial search is scoped to editorial content and never returns product routes. **It
    works with client scripting unavailable**: the control is a form that submits to a results
    route, and suggestions in a listbox with arrow-key navigation and an announced result count
    are an enhancement on top. An empty result renders a heading, one sentence and the topic
    navigation, never a bare no-results.
15. **An unknown address renders the product's own not-found page** inside global chrome,
    with one heading, one sentence, a focusable search control, a way back, and the footer, and
    it answers not-found. It is never a bare framework error.
16. **Every internal link on every public route resolves.** A link that leads nowhere is a
    defect, and external links are out of scope for this rule because their health is somebody
    else's business.
17. A privacy page and a terms page are reachable from the footer of every page. The privacy
    page states what Mercato stores about a merchant and about a buyer and how long it is kept;
    the terms page is additionally linked from the signup form.
## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | Global root; negotiates and redirects to a country storefront | public |
| `/in` | Country home | public |
| `/in-hi` | Country home, second language, fully translated | public |
| `/in/pricing` | Plan comparison and the feature table | public |
| `/in/start` | Trial funnel, one control and no form | public |
| `/in/checkout` | Capability route | public |
| `/in/payments` | Capability route | public |
| `/in/orders` | Capability route | public |
| `/in/markets` | Capability route | public |
| `/in/flow` | Capability route, automations | public |
| `/in/pos` | Retail surface, its own chrome | public |
| `/in/enterprise` | Enterprise surface, its own chrome | public |
| `/in/plus/solutions/b2b-ecommerce` | Business-buyer surface, upmarket chrome | public |
| `/in/blog` | Editorial index, its own chrome and the only one with search | public |
| `/in/blog/topics/<topic>` | Editorial topic index | public |
| `/in/privacy` | Privacy page, linked from every footer | public |
| `/in/terms` | Terms page, linked from every footer and from signup | public |
| `/sitemap.xml` | Every public route | public |
| `/robots.txt` | Points at the sitemap | public |
| `/signin` | Starts the authorization-code flow at the issuer | public |
| `/store` | Store picker for a person holding more than one membership | any member |
| `/store/<store>/home` | Activity, today's tiles and the setup checklist | any member |
| `/store/<store>/orders` | Order queue-list, saved views, metric tiles | `orders.read` |
| `/store/<store>/orders/<id>` | Order detail, timeline, refund composer | `orders.read` |
| `/store/<store>/orders/drafts` | Draft orders and quotes | `orders.read` |
| `/store/<store>/orders/returns` | Return requests | `returns.read` |
| `/store/<store>/approvals` | Approval queue-list | any member; deciding needs the named permission |
| `/store/<store>/approvals/<id>` | One request, its parameters and its decision controls | as above |
| `/store/<store>/products` | Catalog index | `products.read` |
| `/store/<store>/products/<id>` | Product detail and variants | `products.read` |
| `/store/<store>/products/inventory` | Stock by location | `inventory.read` |
| `/store/<store>/products/transfers` | Inbound transfers | `inventory.read` |
| `/store/<store>/customers` | Customer index and segments | `customers.read` |
| `/store/<store>/customers/companies` | Companies, locations and contacts | `companies.read` |
| `/store/<store>/discounts` | Discounts and codes | `discounts.read` |
| `/store/<store>/markets` | Markets, catalogs, price lists, domains | `markets.read` |
| `/store/<store>/finances` | Balances, payouts, disputes, bills | `finances.read_balance` |
| `/store/<store>/analytics` | Reports and exports | `analytics.read` |
| `/store/<store>/online-store/themes` | Theme library and editor | `online_store.read` |
| `/store/<store>/apps` | Installed applications and their grants | `apps.read` |
| `/store/<store>/automations` | Workflow list, canvas and dry run | `automations.read` |
| `/store/<store>/settings/users` | Staff, roles, constraints and ceilings | `staff.read` |
| `/store/<store>/settings/audit` | Audit search | `audit.read` |
| `/org/<org>/stores` | Organisation store list | organisation member |
| `/org/<org>/users` | Identity configuration and group mapping | organisation administrator |
| `/org/<org>/audit` | Cross-store audit search | `audit.read` |
| `/shop/<store>` | A merchant's own buyer-facing store | public |
| `/shop/<store>/products/<handle>` | Buyer-facing product page | public |
| `/shop/<store>/cart` | Cart | public |
| `/shop/<store>/orders/<token>` | Order status and self-serve returns | signed token |
| `/checkout/<token>` | Hosted checkout, first step | checkout session |
| `/checkout/<token>/<step>` | Hosted checkout, a named step | checkout session |
| `/api/health` | Readiness | public |

### Entry and redirects

An unauthenticated request to any `/store/...` or `/org/...` route starts the
authorization-code flow and returns to the route that was asked for. A person with exactly
one active membership lands on that store's home; a person with more than one lands on
`/store`. Signing out revokes the session on the server and lands on `/in`. A token that
expires mid-action returns the actor to sign-in with the composed work preserved and
restores it afterwards. A request for a route the actor's role does not permit renders an
explanation naming the permission required and which roles in this store hold it, and the
navigation item for it is absent. A country segment with no published storefront resolves
to `/` with a temporary redirect and opens the locale control pre-filtered to that country.
An unknown address under a valid country renders Mercato's own not-found page inside global
chrome and answers not-found.

### Journeys

**A refund inside the ceiling.** Sign in as `support@example.com`. Open
`/store/oakleaf/orders`; the queue-list shows five orders. Open `#2050`, whose total is
`850900`. Choose the refund action; a panel slides over the order and the order's own
figures stay on screen. Enter `400000` and submit. The panel closes, an inline banner on
the order says the refund is done, the financial status reads `partially_refunded`, the
timeline carries a refund entry naming `support@example.com`, and the store's balance has
moved by that amount.

**A refund above the ceiling.** Sign in as `support@example.com`. Open
`/store/oakleaf/orders/2049`, total `3411200`. Choose the refund action and enter
`3411200`. Before submission the panel states that this is above the actor's ceiling of
`500000` and will be sent for approval. Submit. The result is a full-page confirmation
naming the request, its amount, the permission required to decide it and when it expires.
The order's financial status is still `paid`, the store's balance has not moved, and the
order timeline carries a request entry rather than a refund entry.

**Approving it.** Sign in as `finance@example.com`. Open `/store/oakleaf/approvals`. The
queue-list carries the pending request with its requester, its amount, its reason and its
expiry. Open it and approve. The result is a full-page confirmation. The refund now exists,
`#2049` reads `refunded`, the ledger carries one balanced transaction for it, and the
request records its decider and the instant. Approving a second time changes nothing and
creates no second refund.

**Self-approval refused.** Sign in as `support@example.com` and open the same request at
`/store/oakleaf/approvals/<id>`. The decision controls are present and disabled with the
reason available on focus, and a direct decision request from that session is rejected by
the server with the request left pending.

**Tenancy.** Sign in as `mallard@example.com`. `/store/oakleaf/orders` is not reachable and
`#2049` is not reachable by its identifier. The order index for `Modern Mallard` shows
`#3001` and nothing else, and the stated result count matches what is shown.

**A location-constrained adjustment.** Sign in as a member constrained to `Pune Warehouse`.
Open `/store/oakleaf/products/inventory`. The location picker offers `Pune Warehouse` and
does not offer `Delhi Flagship`, and a direct adjustment request naming `Delhi Flagship` is
refused with the level unchanged.

**A buyer buys.** Open `/shop/oakleaf`, add `Pauline` to the cart, open the cart, continue
to checkout. The address form renders India's own fields with a state list and a six-digit
postal code. Choose a delivery method, pay, and land on the order status page. Stock is
reserved while the checkout is open and committed when the order is placed.

### States

Every list has an empty state that names what to do next and offers the primary creating
action, and a separate filtered-to-empty state that names the active filters and offers to
clear them. Every page has a loading state: the shell renders at once with its navigation
and header while the content region shows a skeleton matching the page's shape. Denied is
four distinct messages: no permission, plan does not include it, region does not allow it,
nobody can. A degraded dependency replaces its own region with a retry control naming what
is unavailable while the rest of the page works, and the admin carries a system-state region
naming any capability currently running on a fallback. Offline, a page already loaded stays
readable from cache with a persistent banner and its mutating controls disabled with an
explanation. A long operation shows progress with a cancel control where cancelling is safe,
survives a reload and a sign-out, and notifies on completion. Errors never crash the app:
every error screen carries a copyable correlation identifier, says whether retrying can
succeed, and never shows a stack trace, an internal identifier or a hint that another tenant
exists.

## UI/UX notes

The north star is comprehension. Somebody arriving in the admin should be able to tell, in
the first moment and without reading anything twice, what needs doing today and who is
allowed to do it. Somebody arriving on the public site should understand that this is the
machinery a shop runs on.

Two registers share one token layer, and they are deliberately different. The admin is an
operational tool: quiet, dense but organised, restrained, built for scanning and repeated
action, with no oversized heroes and no editorial composition. The public storefront is
consumer and editorial: it may carry atmosphere, and the subject, which is the product
itself depicted at work, is the first thing seen. When the two disagree, whatever a merchant
does twenty times a day wins over whatever a visitor sees once.

The admin must support speed and repetition, so it takes density, large hit areas, stable
positions and minimal chrome. It must guide, so **each page leads with one clear primary
action, visually distinct from every secondary one**, and everything else is quieter. Where
money is being handed back it must reassure, so nothing moves while an amount is being
typed and the order's own figures stay on screen beside the field.

Colour carries meaning by role, never by decoration. The page ground on light is a
near-white neutral and on dark a near-black cool neutral, blue-green rather than truly
neutral. A card sits one step off its ground on either scheme and the two stay visibly
separate without a shadow. Ink is a near-black neutral; muted copy on light is a mid cool
neutral; secondary copy on dark is a light cool neutral and disabled is dimmer than it.
Rules are a near-white neutral on light and a low-strength near-white neutral on dark, with
a deep neutral where a rule must assert itself. The mark and anything that worked carry a
deep, soft teal. One accent, a light, vivid teal, appears in exactly three places and
nowhere else: the numerals of the closing numbered list, the eyebrow in the mega menu, and
the market status pill. Failure is a light, vivid red with a light, soft red as its tint.
Something still in progress is a near-white, muted teal. One wash, a near-white, muted
green, appears once. A state that is none of those three must not borrow any of them.

A second, saturated palette exists and belongs only to the payment product graphics: light
and mid vivid indigo, mid and light vivid blue, light vivid cyan, light and soft blue, light
soft indigo and deep soft indigo. Its saturation is what separates a depicted object from
the page it sits on, and it works because it is rationed. It must not leak into chrome.

Link states on the dark ground are a family of five and their ordering is deliberate: focus
is brighter than hover and active is dimmer than hover, so a keyboard user gets the
strongest contrast of the five rather than the weakest. The exact shades are yours, so long
as every role above stays separable and the three meaning-carrying colours are used for
nothing else.

One family carries the whole product: a variable grotesque on a `100 900` weight axis, in
one file, upright only, with no italic file loaded and `Helvetica, Arial, sans-serif` behind
it. Monospace is reserved for identifiers. Nine display and heading steps each carry their
own size, weight, line height and tracking as one group: `6rem` at `300` over `6.48rem`;
`4rem` at `330` over `4.32rem`; `3.5rem` at `330` over `3.78rem`; `2.75rem` at `330` over
`3.025rem`; `2.125rem` at `330` over `2.4225rem`; `1.75rem` at `360` over `2.1rem`;
`1.5rem` at `400` over `1.95rem`; `1.25rem` at `450` over `1.625rem`; `1rem` at `450` over
`1.4rem`. Three body steps and two control steps: `1.25rem` at `400` over `1.75rem`;
`1.125rem` at `400` over `1.575rem`; `0.875rem` at `420` over `1.2rem`; `1rem` at `550`
over `1.5rem`; `1.125rem` at `550` over `1.75rem`.

**The signature is the inversion**: display sizes are set below `400` and body at `400` or
above, so headlines read as drawn rather than typed over body copy that reads as ordinary.
Set the largest display step heavy and it is a different product however right everything
else is. Figures align in a column wherever amounts stack, which in this admin is most of it.

Spacing comes off one base unit and every gap is a multiple of it; the base unit is yours.
The gap between sections is roughly three times the gap beneath a heading and about halves
on a narrow screen. Corners soften in four steps from barely to noticeably, and the only
fully rounded shape is the pill, worn by circular icon buttons and by the primary action.
Elevation is split on purpose: the page is flat and the things depicted on it are not.
Chrome carries at most a hairline ring and a shallow ambient shadow; anything deeper belongs
to a depicted object.

Density is compact in the admin, so rows sit tight and a full queue fits one screen without
a warehouse operator scrolling for what should be in front of them. Density is spacious on
the storefront, where the subject needs room around it.

The admin's layout archetype is a sidebar shell: a bar across the top carrying the mark, a
centred search field with its shortcut hint, an assistant control, a notification control
and the actor's avatar; a collapsible navigation down the left whose collapsed state persists
per person per device; a sticky content header carrying the page title, a scope control and
the page's actions; and the page itself scrolling independently of the navigation. Inside
that shell, navigation is a breadcrumbed drill-down: every index drills into a detail, every
detail carries a trail back through its parents, and the graded path drills from the order
queue into an order, into a refund composed in a panel that slides over it, into a request.
The storefront ships four distinct chromes rather than one with a flag, because the four
carry different navigation trees, different primary actions and, in two cases, different
colour schemes; somebody arriving on the enterprise pages must never be shown the beginner's
menu.

Motion is described to the browser once and run by the browser, not redrawn by a script on
every frame, and that is the property most likely to be lost in a rebuild. Everything shares
three easings and one speed: around a fifth of a second, quick enough not to be waited for
and slow enough to be seen, easing off at the end rather than starting sharply, and nothing
uses a different speed to feel special. The named moments are the rotating headline that
finishes itself, the sibling dimming that fades a row back and lifts the item under the
pointer, the mega-menu group heading whose fade lags a beat behind its movement so it reads
as arriving rather than appearing, the link arrow that slides out from just before where it
belongs, the plus and minus that dissolve into each other on the same spot instead of
swapping, the chevron that flips rather than rotates so its stroke ends stay put, the thin
light travelling slowly around a card's border, the rule wiped in from the inline start, the
card that flips, the stack that leans, and the marquee whose speed is computed from its own
content length so a wall of four logos and a wall of forty travel alike. Only opacity,
transform, translate, scale, rotate, filter, clip path, mask and custom properties ever
animate; width, height, top, left, margin and padding never do. **Every one of those moments
has a reduced-motion twin**: decorative loops stop and their containers become scrollable
where content would be cut off, entrance reveals jump to their end state and are never
invisible and never mid-travel, scroll-linked transforms are removed with the end state
rendering at every position, autoplaying media does not autoplay and shows a poster with a
play control, and a cross-fade swaps instantly. A focus or hover colour change is retained,
because a colour change is not motion.

Accessibility is contract, not taste. Text and its background meet WCAG AA contrast, and so
do control boundaries, focus rings and any graphic carrying meaning. Every interaction has a
keyboard path, including reordering in the theme editor and connecting nodes on the workflow
canvas, and full keyboard navigation carries a visible focus ring that is never suppressed.
Touch targets are comfortably sized on the shorter axis. Icon-only controls carry a name
saying the action rather than the icon. Status, validity, required-ness and selection each
carry a second signal, so meaning is never carried by colour alone. Two places in this design
cost contrast and must be measured rather than assumed: the sibling dimming in the mega menu,
and the statement band's resting colour on a near-black ground.

Responsive behaviour holds at every width between the four tiers rather than only at them.
At the narrowest, one column and a four-column arrangement; then eight columns and
two-column cards; then twelve columns with the mega menu available; then twelve columns with
a wider gutter and full compositions; and above the widest, content caps and centres while
background compositions keep bleeding. Display sizes clamp continuously and body sizes do not
scale at all. Whether something responds to a pointer hovering is decided by whether the
device has a hover-capable pointer, not by how wide the viewport is: a tablet with a mouse is
wide and has one, a phone in landscape is wide and does not. The page never scrolls sideways
at any width, in any language, in either direction; wide content scrolls inside its own
container with its own softened edge. The layout survives text scaled to twice its size and
the page zoomed hard, reflowing to a single column with nothing lost.

What this must not look like: no page dominated by a single hue family with no second signal;
no decoration standing in for content; no marketing composition where the working interface
belongs; no admin index that reads as assembled rather than designed, which is what a dozen
separately built list pages produce. **Space over dividers. Comprehension over atmosphere in
the admin, atmosphere over density on the storefront. Stillness over feedback while money is
being decided.**
## Front-end specification

Everything in this section is front of house: how the product looks, moves, reads and is
laid out. Business rules live above.

### The two colour spaces

The token layer is authored in two colour spaces at once and that is the single most
consequential fact about it. Semantic tokens and hand-picked brand colours are declared
directly; the generated neutral ramps are declared in a perceptual space and the compositing
helpers mix in a perceptual space. The result is that a tint of a brand colour is
perceptually uniform rather than arithmetically uniform, which is why the dark surfaces stay
neutral as they lighten instead of drifting towards a dirty lilac.

Ship both forms of the neutral ramp, the direct one and the wide-gamut one, and **select
between them by capability, never by user agent string**. The two ramps are the same ramp
expressed twice and their steps correspond one to one.

The neutral ramp runs in nine steps from white through a near-white neutral, a lighter
near-white neutral, a near-white neutral rule, a light cool neutral, a mid cool neutral, a
darker mid cool neutral, a deep neutral and a near-black neutral, to black. Alongside it sit
a mid vivid blue, a light vivid teal for success, a light vivid orange, a light soft violet
and a mid vivid violet, a light vivid yellow, and two pale washes, a near-white muted green
and a near-white neutral green.

The roles the census establishes, and they are roles rather than swatches: white is the page
ground on light surfaces and all display type on dark heroes; black is the page ground on the
darkest sections and type on light surfaces; a near-white neutral is the rule on dark ground
and the hover terminus for muted navigation links; a ten-percent black scrim sits over hero
media; a light cool neutral is secondary copy on dark ground and the mega-menu description
colour; a mid cool neutral is a disabled link on dark ground; a near-white neutral is the
lightest section band; **a near-black cool neutral is what the dark sections actually sit on,
blue-green rather than neutral**; a deep neutral is the rule on light ground; a near-black
cool neutral is the card ground inside a dark section; a near-white neutral is the card
ground on light; a five-percent black hairline and a twenty-percent white rule carry the
pill-button border; a near-white neutral is the hairline rule on light; a deep soft teal is
the historic brand green, kept for the mark and for success; a mid vivid indigo belongs to
the wallet and instalment graphics; a mid cool neutral is muted copy on light; a
four-percent ink wash and a twenty-five-percent ink scrim exist; a ten-percent white is the
inner border on dark cards; **a light vivid teal is the accent**; a near-black neutral is
ink; a near-white neutral is the alternating band; a near-black neutral sits behind developer
graphics; a near-white muted teal is a product-graphic tint; a light soft red is the critical
tint and a light vivid red is critical itself; and a near-white neutral is the warm light
band.

Link states on the dark ground are declared as their own family of five: a light cool neutral
at rest, a near-white neutral on hover, a light cool neutral on active, white on focus, and a
mid cool neutral when disabled.

### Type

One family carries the whole site: a variable grotesque on a `100 900` axis in a single
file, upright only, with `Helvetica, Arial, sans-serif` behind it and the face swapping in
rather than blocking. Monospace appears in developer graphics and falls back to the system monospace stack,
`ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace`.

The nine display and heading steps and the five body and control steps are given in
`## UI/UX notes` with their sizes, weights and line heights. The named weights the axis makes
useful are `300` for light, `330` for the four largest headings, `400` for normal, `420` for
small body, `450` for medium, `550` for bold and `600` for semibold.

**The display sizes must be set at a weight below `400` and the body at `400` or above.** A
build that sets the second display step heavy produces a different site regardless of every
other value being right.

The measured render census confirms the scale is real rather than aspirational: the three
most-rendered pairs are a base size at normal weight, a small body size at its own slightly
heavier weight, and that same small size at normal weight. The largest display step also
appears one clamp step down, because display sizes clamp continuously.

Five secondary faces appear inside the theme-preview product graphic and nowhere in chrome,
purely to make the depicted storefront look unlike the site around it. Substitute any five
families that are mutually distinct in category: a condensed heavy display, a heavy sans, a
serif, a geometric sans and a monospace. The categories matter; the specific families do not.

### Space, radius, containers and grid

A spacing ramp of ten steps runs from a quarter of the base unit to forty times it. A gutter
and a page margin are their own tokens, as are the header height and the hero's top offset.
**Keep the hero offset as an expression rather than as a resolved figure**: it is the seam
where a taller chrome substitutes its own header height at run time, and resolving it removes
the seam.

Four radius steps run from barely softened to noticeably softened. Five container steps set
the measure limits rather than the page width. The measured radius census is a set of roles,
not a set of values: a fully rounded pill on circular icon buttons and the primary call to
action; one softening on cards, the floating media control and media frames; a smaller one on
badges, small chips and the wallet price pill; a larger one on mega-menu panels and video
frames; another on the desktop mega-menu containers; a small one on the product-card button
inside hero graphics; a large one on the radial glow ellipses; one on annotation callouts;
and three asymmetric ones, for developer cards sitting on the bottom edge of their section,
for section cards rising off the bottom of the viewport, and for panels anchored to the top
edge. **The fully rounded value is a pill rule, not a number to copy.**

The container is twelve columns above the third width tier, eight columns from the first, and
four below it, with the gutter widening at the large tier. The development overlays the
reference ships for each grid are evidence of the grid rather than a feature to build.

### Elevation, gradients and glows

Chrome carries at most a hairline ring and a shallow ambient shadow. Anything deeper belongs
to a depicted object: dark section cards carry a composited multi-layer shadow; a dark pill
carries a one-pixel top highlight inset, which is what stops it reading as a hole and must
survive; circular floating badges and tilted collage frames carry deep offset shadows;
desktop mega-menu panels carry a shallow one; the floating logo plate, the fixed assistant
launcher, small inline chips, rounded media frames, circular link buttons on dark ground and
the region selector each carry their own.

Three gradient families do all the work. A **scrim** lies over every hero video so display
type survives an arbitrary frame, and its first four tenths are untouched so the image still
reads. **Radial glows** light the dark payment and enterprise sections as absolutely
positioned ellipses, sized in container query units so they scale with their section rather
than the window, placed at container-relative offsets and at four low opacities. **Text
gradients**, clipped to text, sit on one heading step and light the developer section; their
odd angles and odd stop positions are art direction and must not be rounded. A conic sweep
lights the edge of a card and is the travelling light in the border glow. A section-level
dark wash is interpolated in a perceptual space, which is why its violet does not pass
through grey on its way to navy.

### Controls

Every control declares all of its state colours rather than letting any inherit. The state
axes are ground, which is light or dark; emphasis, which is primary, secondary or tertiary;
and interaction, which is rest, hover, focus, focus-visible, active and disabled. Each state
declares a text colour, a background colour, a border colour and a ring colour, so every
control carries twenty-four declared values. Geometry is a two-pixel border, the pill radius,
padding from its own tokens, and the control type step at bold weight.

**Focus is a two-pixel outline at a two-pixel offset, rendered on focus-visible only and
never suppressed.**

Controls transition colour, background colour, border colour and outline colour together on
the shared default easing, with a shorter variant for smaller controls. Nothing else on a
control moves.

### Colour scheme inversion

A section declares a scheme and every token inside it resolves against that scheme. **A
component must never test which scheme it is in; it consumes the scheme's tokens.** The
captured routes alternate schemes six to nine times each, and the whole retail route and the
whole business-buyer route invert relative to the home route.

### Iconography

Every icon is drawn from coordinates. **No icon file ships.** Icons are drawn inline at a
twenty-unit square box almost without exception, stroked with the current colour so the
surrounding token decides the colour, at a one-unit stroke width, sized by a class on the
element rather than by the box. Line icons are stroked and unfilled; solid icons are filled.
Every directional icon carries a right-to-left mirror rule, which is not optional because the
product publishes a right-to-left surface. Decorative icons are removed from the
accessibility tree and a labelled sibling carries the name.

The set: arrow right; chevron up, with down as the same path rotated; a heavier chevron down
on a larger box; check; close; a solid play triangle, rendered at three sizes with a slightly
heavier stroke in the largest; search, a circle plus a handle path; a solid globe on its own
larger box, reconstructed as a circle with two latitude arcs and one meridian; a tiny solid
caret on a wide short box; minus and plus as rectangles; an assistant sparkle painted twice,
once filled and once stroked, because the double paint is the icon's glow and must be kept as
two stacked paints; a speech bubble; analytics bars; an arrow into a box; a rocket; a
point-of-sale terminal; a small check; a rule; a card; a tag and pen; a large chat bubble on
its own box with each of its three paths drawn twice for the glow; a layered isometric cube
illustration of sixteen paths at a hairline stroke, alternating filled and unfilled; a
stacked-chevrons mark sized relative to its container; and a person-and-terminal illustration
of five paths at a heavier stroke.

The brand mark is a wordmark of four letterform paths plus a white backplate on a box wider
than it is tall, rendered smaller below the medium tier and larger above it. **Those
letterforms spell the reference's own name and must be replaced**: set `Mercato` in the
display family at bold weight with tight tracking, convert to outlines at the same box, and
place beside it a bag glyph built from one rounded rectangle and one semicircular handle arc,
filled in a deep soft teal.

Two icon behaviours are load-bearing. The **slide-out arrow** rests half a character before
where it belongs and fully transparent, and on the group's hover moves into place and becomes
opaque, sitting half a character after the text, aligned to the text baseline and sized in
ems so it scales with whatever type step it lands in. The **cross-fade toggle** puts the plus
and the minus at the same absolute centre at the same size, one opaque and one transparent,
and cross-fades them with a short delay rather than swapping; under reduced motion the
transition is removed and the swap is instant. The mega-menu chevron flips by scaling on the
vertical axis, on hover and on focus-within, never by a rotation, because a scale flip keeps
the stroke ends on the same pixels.

### Global chrome

The storefront ships **four distinct chromes** and which one a route wears is a property of
the route's audience. They must not be collapsed into one header with a variant flag.

| Chrome | Routes | Top-level navigation | Right-hand controls |
|---|---|---|---|
| Main | Country home, plan comparison, capability routes, trial funnel | `Why Mercato`, `Products`, `Pricing`, `Enterprise` | `Log in`, `Start for free` |
| Upmarket | Business-buyer solution routes | `Sell`, `Manage`, `Integrate`, `Migrate` | `Platform`, `Get in touch`, `Start for free` |
| Enterprise | The enterprise route and its children | `Solutions`, `Customers`, `Resources`, `Developers` | `Try Mercato`, `Get in touch` |
| Retail | Point-of-sale routes | `Point of Sale`, `Retail POS`, `Features`, `POS Pricing` | `Log in`, `Start for free` |
| Editorial | Blog and guides | `Blog`, `Find an Idea`, `Starting Up`, `Marketing`, `Latest`, `More` | search, `Log in`, `Start for free` |

The retail chrome's `Features` item carries children `Omnichannel selling`,
`Staff management` and `All features`. The editorial chrome's `More` disclosure carries
`Guides`, `The Mercato Podcast`, `Founder Stories`, `Ecommerce Business Tips`,
`See All topics` and `Enterprise Blog`. A platform switcher offers `Mercato` with
`Platform for entrepreneurs & SMBs`, `Plus` with
`A commerce solution for growing digital brands`, and `Enterprise` with
`Solutions for the world's largest brands`.

The main chrome renders white type on a transparent ground over a hero and on black once
scrolled. The upmarket and retail chromes render dark type on a light ground. **The
enterprise chrome is the only one that inverts on scroll**, from light type over its hero to
dark type on a light ground after it. Chrome is selected by route group at render time and is
part of the route's content document, so the header is correct in the first byte of markup.

The header is the full width, sticky at the top above all content, with the mark at the
inline start, the navigation centred in the remaining space and the controls at the inline
end. At scroll top on a hero route it is transparent with no rule; scrolled, it takes its
chrome's ground and one hairline rule beneath. With the mega menu open the ground goes solid
regardless of scroll position and the page behind dims. At small width with the panel open
the header keeps only the mark and the close control. Chrome is not printed; the mark prints
once at the top of the first page.

**The skip control is the first focusable element**, labelled `Skip to Content`, parked above
the top edge by a transform rather than by a clip or a negative margin, sliding down on focus
and honouring reduced motion. The transform is what keeps it in the accessibility tree and in
the tab order at all times.

The two content-bearing top-level items open a mega menu with three nesting levels, built on
hover and focus-within together so that **it is operable from the keyboard with no script at
all**. The level-one trigger widens its own hit target with a pseudo-element rather than by
changing layout. On hover of the row, every level-one label dims and the hovered one returns
to full, expressed as a group hover plus a self-hover override so the dimming survives the
pointer travelling between items. A level-two group heading is uppercase, tightly tracked, in
the accent teal, and at rest above the large tier it is transparent and lifted; on the
level-one item's hover or focus it becomes opaque and settles. **Its fade is delayed and its
movement is not**, so it has already begun to move before it becomes visible, which reads as
arriving rather than appearing. A level-three link row dims its siblings on the container's
hover, and its trailing arrow is transparent at rest and slides out on the row's hover,
mirrored under right-to-left; below the medium tier the arrow is always visible and sits
absolutely at the inline end.

The Products menu's level-two groups: `Build your website` carrying `Website Builder`,
`Themes`, `Domains`, `Customer Accounts` and `Wingman`; `Sell anywhere` carrying `Online`,
`AI Chats`, `Point of Sale`, `Bazaar app`, `Social & Marketplaces`, `Global`, `B2B` and
`Across Markets`; `Marketing & analytics` carrying `Advertising & Campaigns`,
`Email & Customer Chat`, `Discounts`, `Analytics` and `Test & Launch`; `Run your business`
carrying `Orders & Inventory`, `Shipping` and `Workflow Automation`; `Get paid` carrying
`Checkout` and `Payments`; `Customize & extend Mercato` carrying `Commerce for Agents` with
`Build with our agent tools`, `Mercato App Store` with `Largest commerce ecosystem`, and
`Mercato.dev` with `Dev docs, CLI, and more`; `Non-stop innovation` carrying
`Mercato Editions` with `150+ updates to Mercato, twice a year.`; and `Latest updates`
carrying `Agentic Storefronts`, `Campaign Autopilot` and `Mercato AI Toolkit for devs`.

The Why menu: `Get started fast` with `You could be selling by tomorrow.`;
`Switch to Mercato` with `Get more customers. Make more sales.`;
`Trusted by enterprise brands` with `No matter your size, complexity, or ambition.`; then a
group `Built into every store` carrying `World's best checkout` with
`Proven to convert better.` and `Wingman` with `Your commerce-obsessed AI assistant.`
Descriptions are a light cool neutral at the small step.

The footer is five columns, present and identical on every route: `Mercato` carrying
`What is Mercato?`, `Mercato Editions`, `Careers`, `Investors`, `Newsroom` and
`Sustainability`; `Ecosystem` carrying `Developer Docs`, `Theme Store`, `App Store`,
`Partners` and `Affiliates`; `Resources` carrying `Blog`, `Compare Mercato`, `Guides` and
`Courses`; `Support` carrying `Mercato Help Center`, `Community Forum`, `Hire a Partner` and
`Service Status`. The mark repeats at the inline start as a solid single-colour glyph, and
below the columns sit the locale control and the legal row, which carries the privacy and
terms links. Footer links transition colour on the shared easing.

Below the large tier the navigation collapses to one control rendered as the three-bar glyph;
the panel is full-screen, scrollable and enters from the inline end; level one becomes a
stack of full-width disclosure rows and level two a nested disclosure inside its parent row;
`Start for free` stays in the header at every width while `Log in` moves into the panel below
the medium tier; **the panel traps focus while open and returns it to the trigger on close**;
and body scroll is locked, with scroll chaining from inside the panel to the page behind it
prevented.

**Exactly one persistent floating control per route.** On the main chrome it is a small
rounded control at the bottom inline end carrying a looping muted poster with a play glyph
and the label `Why we build Mercato`, opening a modal player. On the upmarket and enterprise
chromes it is a circular chat launcher at the same position carrying the large chat glyph. It
must be reachable by keyboard, must be the last element in the tab order rather than an early
one, must not overlap the primary call to action at any width, and must be dismissible with
the dismissal holding for the session.

### The motion catalogue

Named keyframe sets, each carried by name because naming them in words is what gets them
built: `fade-in`; `pulse`; `spin`; `marquee`, with left-to-right and right-to-left variants;
`logo-group-marquee` and its reverse, which travel by their own width plus one gutter;
`move-phrase-in` and `move-phrase-in-last`, which slide a phrase in from the inline end and
**hold it at full opacity across the middle of the cycle**; `hero-card-grow` and
`hero-card-scroll`, which scale a depicted product card and lift it on desktop but not below
the medium tier, holding the same transform across part of the cycle;
`hero-card-scroll-md` as the unlifted variant; `globe-reveal`, which opens an ellipse clip
from nothing to beyond the frame; `wave-sweep` and `wave-sweep-mobile`, which animate the custom
properties `--wave-pos` and `--wave-height` that something downstream consumes as a mask
geometry; `pulse-mask`; `pulse-glow`,
which brightens and swells briefly at a fifth of the way through; `orbit-ripple-ring`;
`agentic-fade-in` and `agentic-pulse`; `checkout-feature-highlight`, which fades up, holds
near the end and fades out; `slide-gradient-bg` and `slide-gradient-window`;
`incentives-fill-background`; `apps-showcase-slide` and `apps-showcase-slide-reverse`, which
translate alternating rows in opposite directions by a shared custom property; and
`apps-showcase-tooltip-fade-in-up` with its sibling
`apps-showcase-tooltip-fade-in-up-motion-reduce`, which jumps to the end state instead of
travelling to it.

Three properties of that catalogue are requirements rather than trivia. **Custom properties
are animated, not positions**, which is what lets one running animation drive a mask, a
filter and a translate in step. **Every ambient animation has a reduced-motion twin.** And
**percentage keyframes carry holds**: the hold is the readable part of the animation, and an
implementation that interpolates straight through it plays the same motion and communicates
nothing.

The named effects: the **rotating headline**, a fixed phrase `Be the next` followed in turn by
`AI all-star`, `household name`, `solo-preneur`, `category creator`, `global empire`,
`store they line up for` and `big thing`, each word its own inline-block span, the container
clipped so words are cut off vertically and never horizontally, with a soft mask fading the
top and bottom quarters. The **border glow**, an element inset by a hairline at the section
radius running a long linear loop, masked by a two-layer mask that paints only the
one-pixel border ring, lit by the conic sweep. The **category underline**, which wipes a rule
in from the inline start with bleed below so the stroke is not clipped. The **card flip**,
which sets a perspective and preserves depth and gives its back face a half turn about the
vertical axis, with a companion fade-and-rise. The **tilted card stack**, whose lean comes
from a small perspective term and a translate. The **spotlight reveal**, an image layer
carrying a filter chain that recolours a greyscale source to a single hue without shipping a
second image; keep the chain intact, its intermediate steps are not redundant. The **mouse
spotlight**, the only effect requiring a pointer listener: two custom properties are written
on pointer move and a radial gradient consumes them, and the handler writes custom properties
rather than inline style strings and never reads layout on move.

Five marquee cycles were measured and the spread is the point: **a marquee's duration is
computed from its track's measured width divided by a constant speed and written into a
custom property**, so a wall of four logos and a wall of forty travel at the same speed.
Hard-code it and one of them races. Edges are treated with a mask rather than a fade overlay,
horizontally and vertically, because a mask works over any ground and an overlay only works
over a known one. Under reduced motion the container becomes horizontally scrollable and the
track wraps, so it becomes a list somebody can swipe rather than stopping with half a logo
cut off forever.

Motion budget: only opacity, transform, translate, scale, rotate, filter, clip path, mask and
custom properties animate; width, height, top, left, margin and padding never do, and the two
measured exceptions animate an absolutely positioned decorative layer inside a promoted
containing block and declare their promotion. Promotion is declared rather than guessed, and
the census skews towards opacity rather than transform because the dominant motion is a fade
of many small elements rather than a move of a few large ones. **No more than three infinite
animations run inside one viewport height.**

### Scroll

Scroll behaviour is driven by the engine, not by a scroll listener. Scroll-linked work is
budgeted per route rather than spread across all of them: the country home and the payments
route carry nearly all of it, and the plan comparison, the retail route and the editorial
index carry almost none. Do not spread the home page's technique across every route.

The enterprise route carries one **composed sequence** scrubbed against scroll position,
nine animations reading together as one piece: `bento-backdrop-zoom` and `bento-backdrop-blur`
on a backdrop that pushes forward and blurs as it leaves, overscanned top and bottom so the
zoom never reveals an edge; `bento-heading-in` and `bento-heading-out` on a heading that
arrives and then exits; `bento-fade-out`, `bento-phone-shrink` and `bento-phone-sink` on a
phone that fades, shrinks and sinks away; and `bento-card-rise` and `bento-cards-rise` on a
card grid that rises to replace it. The heading's display size is bound to the
large viewport height unit rather than to width, so the sequence occupies the same share of a
short laptop screen as of a tall monitor.

**Express that timeline declaratively so it can run off the main thread where the engine
supports it.** Where scroll-linked timelines are unsupported, fall back to an
intersection-triggered play of the same sequence at a fixed duration. Never fall back to a
scroll handler that writes styles per frame: that looks identical on a fast machine and
stutters badly on a three-year-old phone.

Scroll anchoring stays on, so content arriving late does not push the reading position.
Scroll chaining from a panel or dialog to the page behind it is prevented. Position restores
on back navigation, including into a route whose content arrives from the content service.
Capability routes carry a sticky in-page navigation offset by the header height so it never
overlaps the header. Snap is used on horizontal galleries only, never on the page. Landing on
a hash scrolls to the target with the header height subtracted and moves focus to it, and
under reduced motion hash entry jumps rather than gliding.

### Product graphics

Roughly half the storefront's visual weight is neither photography nor illustration. It is
animated, layered depictions of the product itself: an order list, a theme editor, a payment
sheet, a market picker, a workflow canvas. These are the most expensive things on the site to
build and the most valuable, because they are the only place a visitor sees the product
before signing up.

A product graphic is a composition of positioned layers, each one flat colour, type, an
inline vector or a procedurally generated placeholder. **None of them is a screenshot.** The
common structure is a ground, being a section with its own colour scheme plus radial glow
ellipses; a frame, being a rounded rectangle with a hairline ring; content, being type at the
smallest steps, rules and status chips; depth, being a tilt plus the deep shadow set; and
motion, being one infinite ambient loop plus one scroll-linked or entrance-linked move.

Rules for the engine: a graphic is data plus a layout, never a hand-positioned pile; its text
is real text in the accessibility tree or the composition carries a text alternative, because
a depicted order table is content and not decoration; **one ambient loop maximum per graphic**
and a second requires a reason; a graphic outside the viewport runs nothing, starts on
entering and stops on leaving; it must be legible and complete when still; every raster in it
is generated; and one that fails to initialise renders its still composition and never
renders a gap.

The **order-management graphic** depicts a top bar with the mark, a search field labelled
`Search` with the shortcut hint `Command K`, an assistant glyph, a bell and an initialled
avatar; a left navigation reading `Home`, `Orders` with children `Drafts`, `Shipping labels`
and `Abandoned checkouts`, then `Products`, `Customers`, `Marketing`, `Discounts`, `Content`,
`Markets`, `Finances`, `Analytics`, then a `Sales channels` group containing `Online Store`
and `Point of Sale`; a page header reading `Orders:` followed by a scope control reading
`All locations`; right-aligned `Export`, `More actions` and a filled `Create order`; a period
control reading `30 days`; five metric tiles reading `Orders 1,271` up `45%`,
`Ordered items 31` up `29%`, `Returned items 6` up `11%`, `Fulfilled orders 41` up `11%` and
`Delivered orders 22` up `45%`, each with a sparkline; a saved-view tab row reading `All`,
`Unfulfilled`, `Unpaid`, `Open`, `Closed`, `Automations`, `Return requests` and
`Local Delivery` with a `+` control; search, filter and sort controls; and a table with
columns `Order`, `Date`, `Customer`, `Total`, `Payment status`, `Fulfillment status` and
`Items`, carrying rows `#2050 Guy Hawkins ₹8,509`, `#2049 Floyd Miles ₹34,112`,
`#2048 Cody Fisher ₹8,509`, `#2047 Ralph Edwards ₹34,112` and `#2046 Theresa Webb ₹8,509`,
with comment and note glyphs and status chips reading `Paid`, `Payment pending`,
`Unfulfilled` and `On hold`. **Rows below the fold are drawn as grey skeleton bars**: the
graphic depicts its own loading state, which is both honest and a cheap way to imply depth.

The **theme-editor graphic** is two panes. The left outline pane lists `Home page`, then a
`Header` group containing `Header` and `Add section`, then a `Template` group containing an
`Image Banner` whose children are two text blocks reading `The Statement Sweater` and
`Classic shape, modern colors`, a `Buttons` block reading `Shop the collection`, and
`Add block`. Each row carries a type glyph. The right pane renders a merchant storefront: a
full-bleed photographic placeholder, a serif display heading over three lines, a subheading
and an outlined call to action.

Demo products depicted inside product graphics are named, so a reader can tell a depiction
from the real catalog: `Forest Knit Sweater`, `Lavender Knit Sweater`, `Deluxe Mixer`,
`Espresso Machine`, `Electric Kettle`, `Toasty Toaster` and `XT5 Gravel Bike`. Demo merchants
inside them are `Oakleaf and Co`, `Modern Mallard` and `Bean Bar`, at the demo hosts
`oakleaf.example` and `modernmallard.example`. Demo buyers are `Guy Hawkins`, `Floyd Miles`,
`Cody Fisher`, `Ralph Edwards` and `Theresa Webb`. Social and marketplace channels are named
by class as `Channel A` through `Channel H`, and assistant platforms as
`Assistant platform A`, `Assistant platform B` and `Assistant platform C`. Card schemes and
wallets are described by class rather than named: a global card scheme, a device wallet, a
browser wallet, an instalment provider and a bank-redirect method.

The **channel-graph graphic** is a centred mark with a radial tree of eight to ten channel
tiles below it, each a rounded square carrying a channel glyph, connected by hairline paths.
Alternating rows translate in opposite directions and per-tile tooltips rise as they fade in.
The application wall on the country home is the same technique at scale: three rows of tiles
in opposing directions with the rows behind dimmed and the front row at full strength.

The **payment surfaces** are three compositions on the darkest ground. An **orbit** of ten
ripple-ring ellipses each running a long linear infinite loop at staggered negative delays so
the ripples are evenly spaced, with six orbiting items around a centred badge, scroll-linked
as well as looped. A **symbol field** running a slow mask pulse, masked by a radial gradient
whose origin is deliberately off centre so the field does not read as a vignette. A **wallet
glass** of two stacked layers translating horizontally behind a seven-stop mask, with the
glass panel itself carrying a backdrop blur: **the seven-stop mask is the difference between
glass and a grey rectangle.** And a depicted **product card** carrying a price `₹17,640`, a
filled `Buy now` control and a line reading `4 payments of ₹4,410.00 with Quickpay`, growing
on entrance and scaling and lifting thereafter.

The **globe** is revealed by opening an ellipse clip from nothing to beyond the frame, and is
a dark sphere with a point-light field over land masses, a caption reading `175 COUNTRIES`
over `WITH MERCHANTS SELLING ON MERCATO`, and a starfield behind.

The **workflow canvas** is a node graph on white: a trigger node headed `Start when...` with
a body naming an event, a condition node headed `Check if...` with `Then` and `Otherwise`
ports, and action nodes headed `Do this...` each with an `Output` port and a `+` control.
Nodes are softly rounded cards with a rule between header and body; edges are orthogonal
paths with rounded corners in a blue stroke terminating in filled circles at each port. **Its
vocabulary is normative for the automations feature**: trigger, condition, then, otherwise,
action, output.

### The storefront routes

**The country home** is the longest route, eleven sections deep, and its section order is:
hero, with full-bleed motion background, the rotating headline and dual calls to action, dark
over media; a statement band, dark; a merchant storefront wall, dark; agent commerce, dark
with a green wash; sell more in more places, dark; merchant proof, dark; the assistant
section, violet; applications, dark navy; developer, dark navy; infrastructure, dark green;
and closing, dark fading to black.

The hero fills the viewport minus the header offset, carries full-bleed muted looping media
that autoplays only under no-preference, a scrim and a ten-percent black wash over the whole
frame, the headline at the largest display step in white, a two-line sub-headline at the base
body step reading `Dream big and build fast on Mercato. The world's best commerce platform.`,
a filled `Start for free` and an outlined control carrying the play glyph and the label
`Why we build Mercato`. At mobile width the headline wraps to three lines and the cycling
phrase renders inline rather than in a fixed-height clip, because a three-word phrase would
otherwise reserve three lines of empty space. The second-language variant carries different
hero footage entirely, not the same footage with different text.

The statement band is four clauses, each its own span:
`Sell everywhere people shop.`, `Online and in person.`, `Across AI and on social.`,
`Locally and globally.` At rest the first is white and the rest are a mid cool neutral;
pointing at a clause lifts it and drops the others, the same group-hover-plus-self-override
rule as the mega menu applied to running prose. **The clauses must read as one sentence with
no pointer at all, the clauses must be focusable, and the dimming must not drop below the
contrast floor.** The resting colour on a near-black ground sits at the edge of that floor
and must be verified rather than assumed.

The merchant wall renders twelve merchant host names as links over storefront thumbnails,
marqueeing horizontally: `northbeam.example`, `corvidsupply.example`, `velahome.example`,
`palegrove.example`, `ridgeline.example`, `halcyongoods.example`, `marrowandco.example`,
`oakleaf.example`, `modernmallard.example`, `beanbar.example`, `kaufhaus.example`,
`streamly.example`.

The agent section is headed `Your brand has entered the chat` over the body
`Get discovered across AI channels. Shoppers check out right in the chat. You don't lift a finger. All powered by `
followed by the inline link `Agentic Storefronts` and a full stop rendered as its own node,
which is a content-model detail worth reproducing: rich text is a sequence of nodes and the
punctuation after an inline link is one of them. Its graphic is three circular
assistant-platform badges overlapping at the inline start and a chat bubble reading
`I need a warm sweater in green. Under $200.` with a circular submit control over a blurred
product placeholder, fading up to partial opacity and then pulsing between partial and full.

`Sell more in more places` carries four sub-items: `Get a stunning store` with
` that's built to sell. Design fast with AI. Pick a prebuilt theme. Or go totally custom.`;
`Sell on every channel` with
`Put your products where shoppers search, shop, and scroll with ` and the link
`multichannel integration`; `Sell face to face` with
`Sell in person and keep online and in-store sales in sync with ` and the link `Mercato POS`;
and `Sell to 250M+ shoppers with Bazaar app`.

The proof section is three cards, each a photographic placeholder over a heading and a
two-sentence body: `Get started fast` with
`Jackie Prince launched Palegrove out of her home. Now it's a $4M+ business.`;
`Grow as big as you want` with
`Vela Home grew from a one-product shop into a cookware empire.`; and `Raise the bar` with
`Iconic toymaker Ridgeline sells direct to shoppers all around the world. All powered by Mercato.`
Below them, centred, an outlined control reading `Pick a plan that fits`.

The assistant section is headed `Meet your secret weapon, Wingman`. The applications section
is headed `Customize everything with apps` over
`The Mercato App Store has 21,000+ commerce apps for whatever specialized features your business might need.`
The developer section is headed `There's no better place for you to build` with the control
`Build apps`. The infrastructure section carries the globe, a checkout collage, the heading
`Rock steady. Blazing fast.`, the body
`Your Mercato store runs strong during your most epic product drops.`, and the quoted claim
that `Mercato Checkout` with `Quickpay`
`converts up to 50% higher than guest checkout and exposes your brand to hundreds of millions of buyers.`
with the footnote `Based on external study with a Big Three global consulting firm in April, 2023.`

The closing section is two overlapping photographic placeholders at the inline start, one
slightly rotated and offset, and at the inline end an ordered list of three steps separated by
hairline rules, each with its numeral in the accent teal at the small body step and its label
at a heading step: `01 Add your first product`, `02 Customize your store`,
`03 Set up payments`. Below it a filled control reading `Take your shot`. After eleven
sections of ambition, that plainness is the point.

Country-home states: media blocked or motion reduced renders the hero's first frame as a
generated still with the play control present; a partial content service may omit any
section, and the order of the remainder is preserved with no gap; on a slow connection
sections below the first render their still composition and ambient loops start only on
intersection; every hover-only affordance has a focus equivalent; and in print, hero media is
replaced by its still and ambient graphics render their end state.

**The plan comparison** is headed `You've got plans. Us too.` at a display step with the
sub-line `Try 3 days free, then ₹20/month for 3 months.`, the billing toggle labelled
`Pay yearly`, and four plan cards. `Basic` at `₹1,499/mo` for `For solo entrepreneurs` with
`Start for free`; `Grow` at `₹5,599/mo` for `For small teams` with `Start for free`;
`Advanced` at `₹22,680/mo` for `For global reach` with `Start for free`; and `Plus` at
`from ₹1,75,000/mo` for `For complex businesses` with `Try Plus`.

Feature lines per card, in order. `Basic`: `2% 3rd-party payment providers`;
`Built-in AI assistant`; `Millions of tokens`; `10 inventory locations`;
`24/7 local chat support`; `Earn up to ₹110,000 in credits`. `Grow`: `Everything in Basic`;
`1% 3rd-party payment providers`; `Up to 5 staff accounts`;
`Earn up to ₹170,000 in credits`. `Advanced`: `Everything in Grow`;
`0.6% 3rd-party payment providers`; `Enhanced 24/7 chat support`;
`Up to 15 staff accounts`; `Live 3rd-party shipping rates`; `Tailor your store by region`;
`Earn up to ₹230,000 in credits`. `Plus`: `Everything in Advanced`;
`0.2% 3rd-party payment providers`; `200 inventory locations`; `Unlimited staff accounts`;
`Priority 24/7 phone support`; `Unlimited B2B catalogs`; `Fully customizable checkout`.

Then a section headed `Always included` carrying capability cards:
`World's best checkout` with
`Get the checkout that converts 15% better on average than other platforms.`;
`Stunning store design` with
`Spin up your store from a simple prompt or with a pre-built template.`;
`Built-in assistant` with
`Wingman is your commerce-obsessed best friend, ready to help you sell.`; `24/7 support` with
`Our support staff and virtual Help Center assistant are here to help, day or night.`; and
`Every channel, one platform` with
`Show up where shoppers scroll and search with multichannel integration.` An assistant bubble
reads `Hi there!` and `How can I help?`

Then `Compare all features`, linked twice, opening the full comparison table with a sticky
header carrying the four plan names and their calls to action. Row groups are `Core
features`, `Hosting` and `Marketing`. Rows include `Earn 1% back on all sales`, reading
`Up to ₹110,000 INR`, `Up to ₹170,000 INR`, `Up to ₹230,000 INR` and `Up to ₹340,000 INR`;
`Online store`, reading `Full-featured` throughout; `Themes and templates`;
`Sell unlimited products`; `World's best-converting checkout`;
`Sell on social and marketplaces`; `Sell in AI chats`; `Mercato B2B`, reading
`Up to 3 catalogs` on the lower three and `Unlimited catalogs` on the top;
`Inventory management`; `Inventory locations`, reading `10`, `10`, `10` and `200`;
`Website builder`; `Millions of tokens`; `Wingman, AI assistant for commerce`;
`Unlimited web hosting`; `Custom domain name`; `Free SSL certificate`; `Unlimited contacts`;
`Create customer segments`; and `Create email campaigns`.

**An included cell renders as a filled circle carrying the check glyph in the accent teal and
carries the accessible name `Included`; a missing cell renders an explicit `Not included`
rather than emptiness.** Row labels carrying a dotted underline link to the capability route
that explains them. The yearly row reads `₹1,499 INR/mo`, `₹5,599 INR/mo`, `₹22,680 INR/mo`
and `-` for the top tier, which is not sold yearly self-serve.

The table renders five columns with a sticky header and full row labels at the widest tier;
four columns with a narrowed label column and horizontal scroll inside the table container
only at the middle tier; and at the narrowest, **a plan selector replaces the header and one
plan column shows at a time with the row labels fixed**, changed by swiping or by the
selector. The page body never scrolls horizontally at any width. A country with no self-serve
plans replaces the four cards with one card carrying the sales path and a line naming the
country. A withdrawn plan disappears from the table entirely rather than rendering as
unavailable. An unavailable currency falls back to the country's official currency, never to
another country's. If the price service is unreachable the last edge copy is served with its
age; if nothing is cached, the section renders a sales path and no numbers, never a zero and
never a dash without a reason.

**The capability template** serves roughly thirty routes. Six instances exist. `Checkout`
carries the eyebrow `Mercato Checkout`, the heading
`The best-converting checkout with Quickpay` hyphenated across a line break with a
non-breaking hyphen node, a body naming
`The world's highest-converting, customizable, one-click checkout` and claiming
`12% of US ecommerce`, a proof strip of `15%` `Higher conversion than the competition`,
`875M` `Global customers` and `5.5B` `Orders processed`, and a feature grid of nine:
`Express checkouts`, `Address auto-complete`, `In-store pickup`, `Location-based pricing`,
`Delivery dates`, `Local delivery`, `Local payment options`, `More ways to pay` and
`Tipping options`. Its wallet block claims `3x faster`, `50% higher conversion` and
`Hundreds of millions more customers`.

`Payments` carries the heading `Accept payments.` over `Expect growth.` as two separate
headings, the body `Mercato Payments is built in, so sales flow smoothly.`, the controls
`Activate payments` and `Start for free`, and six feature pairs: `Welcome every payment`,
`Sell more with Quickpay`, `Go local at checkout`, `Block fraud, not customers`,
`See the whole picture` and `Let AI do the selling`, with the statistics `250M+`, `130+`
currencies and `20%` fewer chargebacks. Its depicted analytics read
`Analytics: Sales by channel`, `Retail sales by POS location`, `Toronto $13.9K`, `New York`,
`London`, `Payouts: Total sales` and `$48,150`.

`Orders` carries the eyebrow `Order management and delivery`, the heading
`Fulfill orders faster from the platform you trust`, a sticky sub-navigation of
`Fulfill your orders`, `Manage your inventory` and `Process your returns` each with a
one-line description, and a feature grid of ten: `Order management`, `Order index`,
`Bulk fulfillment`, `Order editing`, `Manage subscriptions`, `Smart order routing`,
`Fulfillment automations`, `Custom saved views`, `Draft orders` and `Order analytics`. Its
customer-evidence tab set carries four merchant names, `Palegrove`, `Ridgeline`,
`Marrow and Co` and `Halcyon Goods`, each with a `Tools used` chip list drawn from
`Order management`, `Mercato Shipping`, `Fulfillment`, `Returns management`,
`Inventory management` and `Managed Markets`. Its routing graphic reads `Routing rules` over
`Use rules to determine how locations are selected to fulfil orders.` and
`Rules run from top to bottom, and each rule is applied to the results of the previous rule. The final result determines which locations fulfil the order.`,
showing `Minimize split` with `Check if any locations can fulfil the entire order.` and
`Use ranked locations` with `Choose locations in order of preference.`, plus an `Add rule`
control.

`Markets` carries the eyebrow `Mercato Markets`, the heading
`Get a store that flexes to fit every market`, the feature pairs
`Create markets in minutes` and `"View as" customers in each market`, a grid of six reading
`A tailor-made experience`, `Local languages and currencies`, `Optimized fulfillment`,
`Unique domains`, `The right look and feel` and `Select products and pricing` with the plan
badges `Advanced` and `Plus`, and three audience blocks, `Your target regions`,
`In-person shoppers` and `B2B buyers`, each with three bullets. Its depicted markets index
carries tabs `All`, `Regions`, `B2B` and `Retail`, entries `Europe` `2 customizations`,
`France` `3 customizations` and `Harrods` `2 customizations` with an `Active` status pill, and
a `View as` control pairing `United States` with `Online Store`.

`Automations` carries the eyebrow `Mercato Automations`, the heading
`Automate everything and get back to business`, the feature pairs
`Create custom ecommerce automations with no-code building blocks` and
`Tailored solutions. Limitless potential.` with four sub-topics, `Inventory management`,
`Fraud prevention`, `Loyalty and retention` and `Fulfillment management`, each linking to a
playbook, then `Plug-and-play templates, at the ready` over a six-card template gallery,
`Scheduled to fit your life`, and `Always on, so you don't have to be` with the statistics
`562M` `Workflows ran during end-of-year peak`, `1B+` `Decisions automated every month` and
`22k` `Unique jobs completed by Automations`.

A **plan badge** is a small uppercase chip rendered inline with a feature name reading the
lowest plan that includes it: `ADVANCED`, `PLUS`, and `NEW` as a recency badge on the same
component.

The **sticky sub-navigation** is offset by the header height, rendered as a vertical list at
the inline start above the large tier and as a horizontal scroller pinned under the header
below it, with a rule at the inline start of the active item and full-strength text while
inactive items sit at a mid cool neutral. Activating an item scrolls to its section with the
header offset subtracted and moves focus to the section heading, and **the active item follows
the section occupying the middle of the viewport, computed by intersection rather than by a
scroll handler**.

The **customer-evidence tab set** uses tabs that are merchant names, each panel carrying a
`Tools used` chip list, a pull-quote at a heading step, an attribution with the business name
in bold and the person's role, and a case-study card. It must be a real tab pattern: arrow
keys move between tabs, the panel is labelled by its tab, only the active tab is in the tab
order, and the panel is not removed from the accessibility tree while animating.

**The enterprise surface** is a separate surface rather than a template variant, with its own
navigation tree, its own primary call to action and its own floating control, because its
audience is a buying committee and the route's job is to produce a conversation rather than a
signup. Its sections are: a hero with full-bleed motion, the heading
`Enterprise commerce without compromise` at the largest display step, `Get in touch` with a
trailing arrow and `Try Mercato`; a marqueeing logo wall; `Results the board can't ignore`
with four counters; `Conversion so high it's almost cheating` over
`It's not cheating. It's math. Mercato Checkout converts up to 36% better than the competition.`;
the composed scroll sequence; a capability grid of five cards; comparison bars and a gauge; an
agent protocol section reading
`Pick the platform building the world's AI commerce infrastructure` over
`The open agent commerce protocol is an open standard that keeps your catalog and checkout working with every new wave of AI agents.`;
and a closing band reading `Make your next quarter one to remember`.

The four counters read `up to 36%` `better conversion`, `33%` `lower average TCO`, `20%`
`faster migration` and `300+` `new features a year`, each counting up from a zero state when
it enters the viewport. **The rest state is the visible text and the final value is carried
in a visually hidden sibling**, so the number a screen reader announces is the true number
rather than whatever the counter happens to be showing. Under reduced motion the counters
render their final value immediately.

The capability cards read `Sell in AI chats` with
`Let shoppers find products on leading AI platforms and check out fast with Agentic Storefronts.`;
`Move faster with AI built in` with
`Analyze data, generate content, and develop code in seconds with Wingman, Mercato's built-in AI assistant.`;
`250M+ high-intent buyers, only on Mercato` with
`Convert shoppers instantly with Quickpay's one-tap checkout, and add it fast without having to replatform.`;
`Cut costs, not ambitions` with
`Mercato's total cost of ownership is 33% better on average, so you can re-invest savings into growth.`;
and `Blink and your site's loaded` with
`Mercato sites render up to 2.4x faster than stores on other platforms and 1.8x faster on average. Even a 0.5s improvement in site speed can raise conversion.`

The comparison bars are a stacked chart drawn as rows rather than by a chart library:
Mercato's own bar is a full-width filled row in the accent teal carrying the mark, and below
it three rows each split into a filled portion labelled `1.4x faster than`,
`1.5x faster than` and `2.4x faster than` and an unfilled remainder carrying a chip naming
`Platform A`, `Platform B` and `Platform C`. Beside them a semicircular gauge drawn as one
stroked arc with a partial dash offset reads `17%` over `faster migration`, under
`Migrate fast, grow faster` and
`Independent research proves Mercato implementations are 20% faster compared to competitors.`
**Both are data**: the bar lengths derive from the values, the gauge's offset derives from
the percentage, and each carries a table alternative in the accessibility tree.

**The business-buyer route** wears the upmarket chrome and is headed
`Feels like DTC. Acts like B2B.` over
`Sell to businesses and consumers from one platform. Your business buyers get modern self-serve, and you get all the B2B features you need.`
Its feature grid is the strongest evidence in the whole source for what the admin must build,
and every item in it is a requirement stated above: `Customer-specific catalogs` badged
`PLUS`; `Quantity rules`; `Volume pricing`; `Site personalization by audience` badged
`ADVANCED` and `PLUS`; `Customizable buyer portal` badged `NEW`; `Custom B2B solutions`;
`Headless storefronts`; `Workflow automations`; `Company account requests`;
`Sales rep permissions`; `B2B-specific themes`; `Quick bulk ordering`; `Flexible checkout`;
`Vaulted credit cards`; `ACH payments` badged `NEW`; `VAT validation and invoices` badged
`NEW`; and `Custom discounts`. Its statistics read `Up to 33% more self-serve orders` over
`Within 12 months after adopting B2B on Mercato`, `$140.0Cr` over
`Invested into commerce innovation that scales with your business in 2024`, and
`Up to 36% lower total cost of ownership` over
`When compared to major competitors in North America`. Its testimonials are attributed to
`Kelly Marsden`, `Senior Vice President, Emerging Channels` at `Halcyon Goods`;
`Alex Bright`, `Managing Director and Co-Founder` at `Vela Home`; and `Amy Sanderson`,
`Co-Founder and Chief Operating Officer` at `Ridgeline`. Its depicted wholesale surface reads
`Show related products`, `You might also like`, `Wholesale catalog` `Active`,
`Volume pricing` with columns `Quantity` and `Price` and rows `Minimum 10 $3520.00`,
`Break 1 50 $3220.00` and `Break 2 100 $2950.00`, the product `XT5 Gravel Bike` at
`$2950 USD - $3520 USD`, the line `$3520 USD ea. Min. 10`, the control
`Add to cart $35,200 USD`, and `Payment terms` `Net 30`.

**The retail surface** wears its own light-scheme chrome and its own price list, because its
reader runs a physical shop and may not sell online at all. It is headed with the eyebrow
`POS System` over `The point of sale for every sale` and the body
`From first sale to full scale, today's best brands run on Mercato's POS system.`, with
`Start for free` and the line `Already have a Mercato store?` carrying the link
`Log in to set up Mercato POS`. Then `Powering retailers of every size` with three
photographic cards: `Single store` with
`Sell in store with integrated hardware, software, and built-in payments.`;
`Multiple stores` with
`Streamline operations with unified data, reporting, and inventory management.`; and
`On the go` with `Use wireless hardware to sell at pop-ups, markets, and more.` Then
`Everything you need` `in store, online, and beyond` over
`It's the power to sell in person backed by the power to sell online, all by the world's best commerce platform.`
with a three-tab set: `Back office` with
`One place to manage your business across all your locations, in person and online.`;
`POS software` with `POS software for smooth selling in store and at events.`; and
`Online sales` with
`The platform to sell everywhere else customers shop: online, on social media, and more.`
Then a feature grid, then five questions: `What is a POS (point of sale)?`,
`What are types of POS systems?`, `Which kind of businesses use Mercato Retail POS?`,
`What's the difference between Mercato and Mercato POS?` and
`Is Mercato POS available in my country?` Then a closing band reading
`Sell better with Mercato POS` with `Start free trial`.

**The presence of `Staff management` as a named navigation item on this surface and nowhere
else** is what makes in-person staffing its own permission domain.

Questions render as a **disclosure list, not an accordion that closes its siblings**. Each is
independently expandable, the trigger is a button carrying the question and the cross-fading
plus and minus glyphs, the panel is associated with its trigger, and the expanded state is
announced. **The answer text is in the document at first render, hidden by a style rule rather
than absent**, so search and in-page find both work.

**The editorial index** wears the only chrome carrying a search control. Its order is the
editorial navigation; a search control labelled `Search` opening a field with the placeholder
`Type something you're looking for`; a lead article with a topic label, a heading, a
standfirst and a byline; a conversion band folded into the feed reading
`Start your online business today. For free.` over
`Sign up for Mercato's free trial to access all of the tools and services you need to start, run, and grow your business.`
with `Start for free` and the line `Start free then enjoy 3 months for ₹20/month`; topic
columns of two to three articles each; and a dated `Latest` list with a `See all` link. Topics
are `Sell Online`, `Products to Sell`, `Podcasts`, `Starting Up`, `Backoffice`, `Marketing`,
`Latest` and `See all`. The seeded article records are
`10 Best Ecommerce Website Builders for Your Online Store (2024)` under `Sell Online`;
`10 Best Print on Demand Companies and Sites (2023)` and
`Why and How to Start Dropshipping in India as an eCommerce Business` under
`Products to Sell`; `Scarcity, Clout, and Michelin-Star Ambition` under `Podcasts`, dated
`27 Aug 2026`; `How To Build a Multivendor Marketplace in 6 Steps` under `Starting Up`, dated
`26 Aug 2026`; `8 Internal Controls Examples for Small Business Owners` under `Backoffice`,
dated `26 Aug 2026`; and `Email Open Rate Guide: How To Boost Email Opens` under `Marketing`,
dated `26 Aug 2026`. The India-specific headline is evidence that the archive is authored per
country rather than translated from one source. Dates render day first, abbreviated month, four-digit year. Suggestions
should settle within a short latency budget.

**The trial funnel** is almost bare and that is the signal: the entry is one control, not a
form. A composed hero puts the word `start` at the inline start and `today` at the inline end
of one line, with `Be selling by tomorrow` beneath and a single `Start for free`, behind them
a floating composition of a storefront and a phone. Then `Choose your design` over
`Start with a stunning prebuilt theme or describe what you want and generate a store with AI.`
and the theme-preview graphic. Its depicted storefront carries the navigation `New in`,
`Handbags`, `Jewelry`, `Accessories`, `Just landed`, `Most popular`, `Collections` and
`About`, the headings `The Elements of Style`, `Birds for every room`, `New this season` and
`Shop full collection`, product cards `Pauline` `Spotted in the wild` `₹11 226`, `Sanders`
`Cool and coastal` `₹13 304`, `Addie` `Warm and woodsy` `₹9 564`, `Sedgewick` `Lovable loon`
`₹14 972`, `Chip` `Limited-Edition Cardinal` `₹7 484` and `Carry` `Edition Cocoa Suede`
`₹59 869`, the lines `Hand-carved from Atlantic white cedar` and
`Painted with premium finishes`, and the counts `Handbags 42`, `Shoes 37` and
`Accessories 53`.

The depicted checkout inside the checkout capability route reads `Oakleaf and Co`,
`Express checkout options`, `Show more options`, `Contact`, `Have an account? Log in`,
`Email address or phone number`, `Email me with news and offers`, `Delivery`,
`Country/region`, `India`, `First name (optional)`, `Anu`, `Last name`, `Gupta`, `Address`,
`151, Rajouri Garden`, `Add apartment, suite, etc.`, `Province`, `West Delhi`, `Postal code`,
`110018`, `Shipping method`, `Discount code or gift card`, `Apply`, `Subtotal ₹18400`,
`Shipping ₹689.6`, `Estimated taxes ₹896.8`, `Total INR ₹19986.4`, the lines
`White kitchen chair` `Curved seat with beech wood legs` `₹6400` and `Side tables`
`Brown wooden side tables` `₹12000`, and the annotations `In store pick up`,
`Accept discounts and gift cards` and `Product recommendations`.

Conversion control labels, each appearing where it is listed: `Start for free` in the header
of every main-chrome route and repeated in body sections; `Log in` in the header;
`Start your free trial` in a capability hero; `Start free trial` on the retail and order
routes; `Try Plus` on the top plan tier only; `Get in touch` in enterprise chrome;
`Try Mercato` in enterprise chrome; `Activate payments` on the payments route;
`Get Automations` on the automations route; `Pick a plan that fits` on the country home;
`Take your shot` in its closing section; `Customize your markets` on the markets route;
`Log in to set up Point of Sale` on the retail route; and `Compare all features` twice in the
plan table, anchoring to the comparison table on the same route.

The locale control sits in the footer of every route, renders the current selection as a
country name and a language name, and opens a panel listing published countries grouped by
region with their published languages. **It works as a form with a submit control when
scripting is unavailable.** Selecting navigates to the target storefront's equivalent route
if published, and to that storefront's home if not, announcing the destination before
navigating because the whole page changes language. The selection is stored and consulted
only at the negotiation step.

### Route-level storefront states

A route not found renders the not-found page inside global chrome with one heading, one
sentence, a search control and the footer, never a bare framework error. **A section that
failed renders nothing while the page renders**, and the failure is logged with the section
key and the route. If the content service is unreachable, the last good edge copy is served
past its freshness window with a soft revalidation retry; if nothing is cached, the route
answers unavailable inside chrome. An empty editorial index renders a heading, one sentence
and the topic navigation, never a blank column. A plan unavailable in a country renders its
card with the price cell reading `Not available` and its call to action replaced by a link to
the sales conversation. A language not published never appears in the locale control for that
country: it is never offered and then broken. **With client scripting unavailable, content,
navigation and forms all function**: the mega menu falls back to a disclosure per top-level
item and the marquees render as static wrapped lists.

### Copy rules

Headings and controls are sentence case rather than title case; the measured exceptions are
the eyebrows, which are uppercase with loose tracking. Statistics use compact forms as
written: `250M+`, `1B+`, `22k`, `5.5B`, `875M`, `562M`, `21,000+`, `130+`, `175` and `300+`.
Contractions are used throughout, because the voice is contracted and informal and formalising
it changes the product's apparent audience, which is people running small shops. Every
statistic carries a footnote marker. **No typographic dash appears in any shipped string**;
where the source used one, a comma, a colon or a new sentence takes its place.

The second-language surface is a **full translation, not a partial one**. Every string above
has a Devanagari counterpart: the navigation, the hero headline, the body copy, the
sub-headline and both calls to action. The translation is authored rather than machine
generated for at least the chrome, the hero copy and every call to action, because a partially
translated storefront is worse than an untranslated one: the visitor cannot tell which parts
they can trust.

### Zero assets

**No binary asset ships.** No image, video, font file, icon file or vector document. Every
photograph, logo, texture and icon is produced by a generator, so the product can be built
from text alone and real media dropped in later without a code change.

Every generator obeys one contract. Its output is a pure function of a seed derived from the
resource identifier, so the same variant always yields the same placeholder. It is told the
box it must fill and fills it exactly, so no layout shift occurs. It runs at build time where
the content is static and at first request with a cache where it is not, never on every
render. Every generated image carries alternative text derived from its resource. It sits
behind one interface, so swapping in real media is a configuration change rather than a code
change. And **generated media is visually distinguishable from real photography on close
inspection**, because a placeholder that looks like a photograph ships to production by
accident.

The recipes. **Grain** is an inline fractal-noise filter used as a tiling overlay, desaturated
to remove the colour fringing turbulence produces by default, with a shallow alpha transfer
that keeps it a texture rather than a fog, applied as an overlay blend over dark sections at
very low opacity. **Hero and card photography** is a canvas gradient keyed by the seed: two
palette colours as a soft two-stop linear gradient at a seeded angle, overlaid with three
large blurred elliptical blobs at low opacity, then the grain, at the box's own aspect ratio.
**Product photography inside graphics** is a neutral ground with a centred rounded silhouette
derived from the product's type where one is known, filled with a seeded two-stop gradient,
with a soft contact shadow beneath. **Portraits are never generated as a face**: a circular
monogram of the initials at a heading step over a seeded ground. **Merchant storefront
thumbnails** are miniature compositions of a header bar, a hero block and a three-column
product row, drawn at the thumbnail's own scale so each reads as a website rather than as an
abstraction. **Small animated placeholders** are single-pixel transparent rasters generated at
runtime. **Application tile icons** are seeded rounded squares with a two-letter monogram.

**The globe** is the most expensive substitution and the one most likely to need adjustment: a
coarse coastline polygon set held as a compact coordinate list in source, covering the seven
continental land masses, is projected to a sphere in a canvas with a fixed tilt and rendered
once per size into an offscreen surface; the ocean is a radial gradient from a deep teal at
the limb to near-black at the centre of the far side and the land a slightly lighter fill with
no outline; merchant lights are placed by rejection sampling inside the land polygons,
weighted by a density field approximated as a few dozen two-dimensional blobs over the major
population centres, each accepted point rendering as a small dot in a warm amber with an
additive glow; a starfield of single-pixel points at low opacities sits behind; the reveal
animates the ellipse clip; and any rotation is a slow constant angular step redrawn at a
capped rate and stopped entirely under reduced motion. **Say plainly in the build that the
light distribution is a plausible reconstruction rather than the real one.**

**Fonts are named, not shipped**: choose a variable grotesque with the stated weight axis and
a licence permitting web use, with the stated fallback stack, metric-compatible enough that
the swap causes no layout shift, loaded with the face swapping in, preloaded and subset per
script, and with a separate subset for the Devanagari surface loaded only there.

**Marks** are outlines, not files: the wordmark set in the display family at bold weight with
tight tracking and converted to outlines; the glyph built from one rounded rectangle and one
semicircular handle arc; each customer logo-wall name set in a distinct family at a fixed cap
height and converted to outlines, so the wall reads as a set of different brands rather than
one repeated typeface. **Payment method marks are never reproduced**: each renders as a
rounded rectangle carrying a two-letter code and a description of its class. Channel marks
take the application-tile treatment.

**Vector animation payloads** are rebuilt as inline vector markup with the layers as sibling
groups, driven by the same scroll-linked mechanism as the composed sequence. The original's
easing between keyframes is not recoverable, so what is specified is a keyframe contract
inferred from sampled scroll positions, and it is marked as inferred.

**Hero motion backgrounds** are a generated canvas loop: three large blurred blobs from the
palette drifting on independent slow sinusoids at a capped frame rate, composited under the
scrim and the grain. Its first frame is generated as the poster and is what renders under
reduced motion, on a slow connection and in print.

Four things cannot be substituted and it is more honest to say so than to pretend: the
reference's filmed footage, whose emotional register the substitute does not carry; its
photographed merchants, without whom the proof section is a layout rather than an argument;
the exact easing inside the vector payloads; and the licensed display family, whose
replacement changes the voice more than any other single substitution.

### Component architecture

Primitives: button, link, icon, image, input, select, toggle, modal, accordion, card, heading
and message. Compositions: card grid, slideshow, stats cards, testimonial, section heading,
logo group, marquee, tab set and disclosure list. Sections: one per content section kind, each
self-contained, each wrapped in an error boundary and each declaring its own data contract.
Page layouts: one per route family. Hooks and utilities: focus trap, capability detection,
locale and region selection, colour scheme and formatting.

**A section knows nothing about the sections around it**, and the error boundary is the
enforcement of that. It is what makes the partial-render behaviour possible.

The admin is a shell, an index framework, a detail framework, an editor framework, form
primitives and a typed data layer. **The index framework is the highest-leverage component in
the admin**: it carries the table, saved views, filters, sort, bulk selection, pagination, and
the empty and denied states, written once and used by every index. Twelve indexes implemented
separately produce twelve different filter behaviours and twelve different empty states, which
is what makes an admin feel assembled rather than designed. The theme editor and the workflow
canvas share a selection model, an undo stack and a dirty-state model.

State: server state is cached query results with explicit invalidation on mutation and is
never mirrored into a client store; route state, which is filters, sort, scope, page and
selected tab, lives in the address so a view is shareable and the back button does the
sensible thing; ephemeral interface state is component-local; cross-cutting session state is a
small store of the actor, the store context, entitlements and feature flags; and draft state
is persisted per resource so a reload does not lose an unsaved edit, and cleared on a
successful save.

Undo: the theme editor and the workflow canvas keep a command stack of invertible commands
rather than a state snapshot, surviving a reload within the session. A bulk operation is one
reversible operation for a bounded window. **A destructive single action whose effect leaves
the system, such as a sent message, gets a confirmation rather than an undo**, because an undo
that restores a stored previous state cannot unsend a message and offering it teaches the
wrong model.

### Accessibility, in detail

The target is conformance across the standard's A and AA success criteria, plus the following.

Focus is visible as a two-pixel outline at a two-pixel offset on focus-visible, never removed,
meeting the non-text contrast floor against both the control and its surroundings. Focus order
follows reading order, and a visual reorder is accompanied by a source reorder rather than a
tab-index patch. Focus is never trapped except inside a modal or an open panel, where the trap
is intentional and escape releases it. Closing a panel, modal or menu returns focus to the
element that opened it. On navigation, focus moves to the main heading and the route change is
announced.

Keyboard paths: the mega menu opens by focus-within, moves within a group by arrow keys and
closes on escape returning focus; tab sets move by arrow keys with home and end jumping and
only the active tab in the tab order; disclosure lists toggle on enter and space and each is
independent; theme-editor reordering is command-based with announcements; table row selection
uses space to select and shift to extend, and a select-all control states what it selects; the
command surface moves by arrow keys, activates on enter and closes on escape; the terminal is
touch-first and every function is also reachable from an attached keyboard, because accessible
retail is a legal requirement in several of the markets this sells into; **and every drag has a
command equivalent, because a drag is never the only path**.

Names, roles and values: an icon-only control carries a name saying the action rather than the
icon, so `Close menu` and never `Cross`; a decorative icon is removed from the accessibility
tree; a status chip's status is text and colour is never its only carrier; the plan table's
inclusion glyph carries `Included` and a missing cell carries `Not included`; every form field
carries a persistent visible label and a placeholder is never the label; errors are associated
with their field and announced on focus; live regions carry asynchronous result counts, price
changes on the billing toggle, save confirmations and scope changes, polite by default and
assertive only for errors; and landmarks are one main, one banner, one contentinfo, with
navigation landmarks named where more than one exists.

Modals and panels trap focus, return it, close on escape, make the underlying page inert,
label the dialog by its heading and lock page scroll.

Contrast: body text at least `4.5:1` against its ground, large text at least `3:1`, and
control boundaries, focus rings and meaningful graphics at least `3:1`. Status, validity,
required-ness and selection each carry a second signal. High contrast mode is respected and
the design never depends on a background image to convey anything. **The two dimming patterns
must both be measured against the floor and adjusted if they fail.**

Announcements: the billing toggle announces the new term and that prices updated; a scope
change announces the new scope and the new result count; a filter announces the result count;
a save announces its confirmation with the resource named; a long operation announces its
start and its completion; and a validation failure announces the summary with focus moved to
it.

Tables use real table semantics with a header row and scoped headers; a grid of divisions is
not a table. In the comparison table the row headers are the feature names, the column headers
are the plan names, and every cell is programmatically associated with both. A sortable
column's sort state is announced and its control is a button inside the header. A wide table
scrolls inside its container and the container is focusable so a keyboard user can scroll it.
Where a table becomes cards, the association between label and value is preserved.

**Every chart carries an equivalent table in the accessibility tree, or a text summary stating
the same conclusion.** That covers the enterprise comparison bars and gauge, the admin metric
tiles and every report visualisation.

The two hardest surfaces are the theme editor and the workflow canvas. The outline pane is a
real tree: arrow keys move and expand, home and end jump, and type-ahead selects. Reordering
is command-based with announcements. **The workflow graph has a linear equivalent**: a list of
nodes with their connections, navigable and editable without a pointer. Selection is announced
with the selected node's type and position stated. The preview frame is reachable and its
content navigable, or it is marked as a preview and a text description of the change is
offered.

Layout survives `200%` text scaling and `400%` page zoom at a `1280px` viewport, reflowing to
a single column with no loss of content or function and no two-dimensional scrolling.

Testing coverage: automated checks on every route and every admin surface; the whole task list
performed without a pointer; at least two screen readers on the primary buyer flows and the
primary merchant flows; zoom and scaling; reduced motion on every route; and voice control,
which works only when a control's accessible name matches its visible label.

### Responsive, in detail

The primary width tiers are four, with a floor for very small devices and a handful of one-off
corrections for particular compositions that should stay one-off rather than being promoted
into the scale. Hover affordances are gated on pointer capability rather than on width.

Display sizes clamp continuously and body sizes do not scale at all; that pairing is the
design's signature. On the enterprise route the display size clamps against the large viewport
height unit rather than width, with a tightened line height, because the composed sequence has
to fit vertically.

At the narrowest tier: one column, a four-column arrangement, the narrow gutter, the collapsed
navigation, marquees at the same pixel speed as everywhere else, and the hero headline wrapping
to three lines. Between the first and second: eight columns, two-column card layouts, and the
sticky sub-navigation becoming a horizontal scroller. Between the second and third: twelve
columns at the narrow gutter, with the mega menu available. Between the third and fourth:
twelve columns at the wide gutter and full compositions. Above the fourth: content capped at
the container maximum and centred, with background compositions continuing to bleed.

Documents grow at mobile width, and the enterprise route grows twice as much as the country
home because its card grid reflows from a row into a column. Budget for that.

Admin and terminal at width: the admin keeps full navigation and full table columns at the
widest; collapses navigation to icons with labels on hover and focus at the next; turns
navigation into an overlay and drops tables to their primary columns with the rest in a
per-row disclosure at the next; and becomes a single column with tables as cards at the
narrowest. **Fulfilment surfaces are designed for small width first**: a picking list, a label
print and a stock adjustment must each be a one-handed operation. The terminal is fixed to its
device's form factor, with touch targets at least `44px` on the shorter axis, controls in the
lower half of the screen where a thumb reaches, and no hover-dependent affordance anywhere.
Buyer surfaces are small-width-first without qualification, because the majority of buyer
traffic in this market is mobile. **The mobile case is not a courtesy: a warehouse operator
picking parcels and a retail associate at a counter are both primary users and both are
holding a phone.**

Overflow: the page never scrolls horizontally at any width, in any language, in either
direction. Wide content, meaning tables, code blocks, wide graphics and marquees, each owns an
overflow container with its own scrollbar and its own edge mask. Long words wrap with an
explicit break rule, and the build is tested with a language whose words are longer than the
layout.

Compositions size their internal proportions in container query units rather than viewport
units, so a composition is reusable at any width without a breakpoint. **A composition sized in
viewport units is correct in exactly one layout.**

The testing matrix covers widths from very small to very large, a short laptop and a tall
monitor because display size binds to height on one route, hover-capable and coarse-touch and
keyboard-only pointers, both text directions, normal and doubled text scale, full and reduced
motion, and both light and dark section schemes rendered.
## Technical requirements

The application is server-rendered and progressively enhanced. Every route is produced on the
server and arrives as complete markup, so the browser receives a usable document on first
paint; scripting adds behaviour on top of a working page and is never what makes a page work.
The backend is **Django with its template layer**, serving the marketing storefront, the
merchant admin, the merchant storefront, the hosted checkout and the machine surface from one
process. The front end is **Alpine.js over those server-rendered templates**: the mega menu,
the disclosure lists, the slide-over refund composer, the command surface, the billing toggle,
the theme editor's outline pane and the workflow canvas are all enhancements over markup that
already carries the content.

Storage is **PostgreSQL**, reached at `DATABASE_URL`. Identity is **Keycloak**, reached at
`AUTH_ISSUER_URL` with the client credentials `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET`, and
it is the federated issuer this product's organisation-level sign-in requires. Read every host
and port from the environment and never hardcode one. **Both backing services are already
running and reachable at those variables. Do not download, install, compile or start a copy of
either.**

> Use only the libraries named here plus their direct dependencies. Do not introduce a second
> database, cache, queue, object store, identity provider or mail vendor - the only backing
> services available in this environment are `postgres` and `keycloak`, and reaching for
> anything else is a contract violation.

Authentication is an authorization-code flow with proof key against the issuer. The
application then holds its own opaque server session; the cookie carries no claim, no role and
no store. Buyer identity is a separate credential store with its own cookie and its own
audience. Machine callers present an installation token in a header, never in a query
parameter, because query parameters land in logs and referrers.

`GET /api/health` returns `200` once the app is ready.

**Six things are implemented exactly once and consumed by every surface**: the policy
decision, price resolution, money arithmetic, the tenancy predicate, the idempotency store and
the audit writer. Each of them implemented twice gives two different answers, and the second
one is always the wrong one in a way nobody notices for months.

Transport parses, validates shape and does nothing else. The application layer orchestrates a
use case, owns the transaction boundary, calls the policy component, and writes the audit
entry and the outbox row inside the same transaction as the state change. The domain is pure
and takes its clock by injection. Infrastructure sits behind interfaces the domain declares.
**No repository opens its own transaction**, because one that does makes composition
impossible and is the most common cause of partially applied writes.

The split into deployable units follows failure domain and change cadence rather than nouns: a
storefront renderer holding no merchant data; a merchant storefront renderer, the
highest-traffic surface by an order of magnitude; a checkout service with its own deploy
cadence; the admin application; a core service carrying catalog, inventory, orders,
fulfilment, customers, markets and discounts; a money service, separated because its failure
domain, its audit obligations and its change cadence all differ; an identity service,
separated because everything depends on it and nothing should depend on it deploying; a
delivery service for outbound events and messages; job runners, one pool per queue class; a
terminal service tolerating device offline behaviour; and an analytics pipeline. A service per
table is a distributed monolith with worse latency and the same coupling.

**The machine surface.** A graph interface serves the admin and storefront surfaces so a
client fetches exactly the fields it needs and the cost of a request is computable before it
runs; a resource interface serves webhooks, bulk operations and file handling, where a graph
adds nothing. Versions are dated, at least four supported concurrently and each for at least
twelve months, with a deprecation notice in the response headers for the oldest. Breaking
change happens only at a version boundary; removing a field, narrowing a type, adding a
required argument and changing an enumeration's meaning are all breaking. Identifiers are
opaque, globally unique, type-prefixed and sortable by creation, never a bare integer, because
a bare integer invites enumeration and reveals volume. **Pagination is cursor-based only**,
because offset pagination is incorrect under concurrent writes and expensive at depth. An
error carries a stable machine code, a human message, a path to the offending field and a
documented retryability flag. A nullable field documents what null means, and optional and
absent are distinguished from present and null. **An unknown field in a request is rejected
rather than ignored**, because silently ignoring a misspelled field means somebody thinks they
saved something they did not.

Three machine surfaces exist with different audiences and different trust, and conflating them
is how a public credential ends up reading customer records: the admin interface, for
applications acting for a merchant under a scoped installation token; the storefront
interface, for a merchant's own buyer-facing code including headless, under a public
credential limited to published data; and the partner interface, for a partner managing their
own applications, partner-scoped and never merchant-scoped. **The same policy component
authorizes all three; there is no separate machine-interface permission model.** A field the
credential's scopes do not cover is absent from the response rather than null, and requesting
it is an error naming the missing scope.

Validation happens in layers, and **every rule exists at the last layer that can express it**,
duplicated upward only for a better message. A rule that exists only in the interface layer is
a rule the background jobs, the imports and the automations do not obey. Shape, required-ness,
enumerations, formats, ranges and string lengths are rejected before any business logic runs.
Normalisation trims, folds case where the field is case-insensitive, and canonicalises
addresses and phone numbers. Semantic rules cross fields. Authorization follows. Database
constraints are the final layer and carry the balancing rule, the refund ceiling and the
variant option arity.

Field rules that must not be relaxed: money is an integer in minor units plus a currency, and
a request supplying a decimal is rejected rather than coerced; a quantity is a non-negative
integer and quantity zero means something different from absent, and both are expressible; an
email address is validated, normalised and never used as a primary key; a phone number is
stored canonically with its country and its display form derived; a timestamp on the wire
always carries a zone offset and a bare local time is rejected; a business date is a date plus
a named timezone and never an instant; free text is length-bounded, stored as text and escaped
at every output boundary by the renderer rather than at input; rich text is parsed to a
document tree at write, stored as that tree and rendered from it, never stored as unparsed
markup; and an identifier from another system is length-bounded, namespaced and never trusted
as unique on its own.

**Idempotency is required on every mutating operation that moves money, stock or a message**
and accepted on all others. The key is client-supplied, unique per store, and stored with the
request fingerprint and the response. A repeat with the same key and the same fingerprint
returns the stored response including its status. A repeat with the same key and a different
fingerprint is an error, because that means the sender has a defect and either guess would be
wrong. Keys are retained `7` days, longer than any client retry policy. A repeat arriving
while the first is still running waits, bounded, and then returns a retryable error rather
than executing twice.

Bulk operations submit a query or a mutation set, return an operation identifier, and produce
a durable result artefact fetched afterwards. One bulk operation per type per store runs at a
time and a second is rejected with the running one identified. Cancellation is supported with
partial results available. **Bulk work does not consume the interactive rate budget and
interactive requests are never starved by it.** The artefact expires and its address is signed
and single-audience.

**Rate limiting is cost-based, not request-based**, because one graph query can be a thousand
times more expensive than another and counting requests tells you nothing. The admin interface
uses a per-installation cost bucket refilling at a stated rate with a burst capacity, and a
query whose computed cost exceeds the bucket is rejected before execution with the cost and
the wait stated. The storefront interface is limited per credential and per network prefix with
a burst sized for a page load and a sustained rate sized for a crawler. Admin browser sessions
are limited per person, generously, shaped to catch a runaway client rather than a user.
Authentication is limited per address, per account and per network prefix with progressive
delay. The agent surface has its own budget separate from the storefront's. Bulk work is
governed by concurrency limits rather than rate limits. **Every rejection returns the limit,
the remaining budget, the reset instant and a retry-after**, because a rejection with no
guidance produces a client that retries in a tight loop, which is worse than the load it was
meant to prevent.

Caching has four layers. The edge holds rendered storefront documents, storefront read
responses, static assets and sitemaps, invalidated by key on publication events. The
application layer holds resolved settings, market resolution, entitlements, policy decisions
and price-list resolution, on a short lifetime plus event invalidation. The data layer holds
query results for hot read paths, keyed by version. The client holds static assets by content
hash and nothing else.

**The storefront cache key is store, market, language, currency, theme version, content
version, and device class only where the markup genuinely differs.** It never includes a buyer
identifier, a session, a cart or a customer segment. Everything that varies per buyer is an
island fetched separately. This is absolute because every violation of it is a storefront that
cannot be cached at all.

Invalidation is event-driven from the outbox and is idempotent: a product publish, unpublish,
price change or inventory-policy change invalidates that product's documents and the
collections containing it; a collection rebuild invalidates on completion rather than on rule
change; a theme publish invalidates the theme version component; a market setting change
invalidates that market; a content publish invalidates by content key; and inventory crossing
zero invalidates the product wherever the theme renders availability. **A missed invalidation
is bounded by a maximum stale age, so the worst case is stale rather than permanent.** When
the origin is slow, serve stale while revalidating; when it is down, serve stale beyond the
window up to a longer emergency window with the age surfaced in a response header; when
nothing is cached and the origin is down, render an error page in the merchant's branding
where that is cached and a plain one otherwise, never a framework stack trace. **Cart and
checkout are never cached** and must be fast without caching, which constrains their data
access to a small number of indexed reads.

Asynchronous work runs in separate queues with separate worker pools, sized independently:
`interactive` for work a person is waiting on, highest priority and tightest timeout; `money`
for payouts, billing, refunds and dunning, never sharing a pool with anything that can flood;
`delivery` for event delivery and channel synchronisation, isolated per target so one slow
target cannot block others; `bulk` for imports, exports and bulk edits, rate-limited per
store; and `maintenance` for reconciliation, retention and index rebuilds, lowest priority and
deferrable under load. **A single shared queue is the architecture that fails first**, because
one merchant importing a hundred thousand products delays every other merchant's order
confirmation.

Jobs survive a process death; a job held in memory is not a job. Delivery is at-least-once and
every handler is idempotent on the job's own identity. Ordering is not guaranteed globally,
and where it matters jobs for one resource are serialised on a key derived from that resource.
The visibility window is sized above the handler's timeout, or a job runs twice at once. After
a stated attempt ceiling a job moves to a dead-letter store with its full context and an alert
fires; **it is never dropped**, and dead-lettered jobs are inspectable and replayable
individually or in bulk after a fix. Queue depth and age are the primary alerting signals. Per
store, concurrency and throughput are capped per queue so one store cannot consume the pool,
weighted by plan but with a floor so no store is starved. A job's priority rises with its age.
Under sustained overload new bulk work is refused at submission with a clear message and a
retry-after rather than accepted and never run. Automation runs, bulk operations and event
deliveries are metered per store and visible to the merchant.

Scheduled and reconciliation work: release expired checkout reservations every minute; capture
or void authorizations approaching expiry every minute; initiate payouts at each store's
cutoff; bill subscriptions and run dunning daily in the store's timezone; compare the inventory
projection to its ledger hourly; **compare analytics money totals to the ledger hourly and
alert on any difference at all**; compare platform payment state to the processor hourly;
compare catalog and inventory per channel daily; compare issuer state to local memberships
daily; enforce retention daily; keep the search index fresh continuously with a daily full
check; and review the dead-letter store daily. **Every reconciliation job reports rather than
silently repairs**, except where a repair is provably safe and is itself written to the
ledger, in which case it still alerts.

Time semantics are the most common source of subtle defects in a system with stores in many
countries. Instants are stored with a zone in one canonical zone, database-assigned where the
database is the authority. A business date is a date plus the store's named timezone, never an
instant. Timezones are named zones from the region database, never offsets, because an offset
does not know about a daylight transition. Schedules are evaluated in the target's named zone.
**A schedule falling in a skipped local hour runs once at the next valid local instant, and one
falling in a repeated local hour runs once on the first occurrence**, deduplicated by the local
date and the schedule identity. A store timezone change is recorded with its instant and
historical periods are not recomputed. Every signed artefact tolerates a stated clock skew and
rejects outside it with a message naming skew as the cause, because the alternative is an hour
of undiagnosable failures.

Any operation exceeding `2` seconds produces a progress record with a state, a completion
fraction where computable and a result. Cancellation is offered where the operation is
cancellable and the interface states whether partial work stands. **A progress record survives
a page reload, a sign-out and a deploy.** Failure names what failed, how much succeeded, and
whether a retry is safe.

**Events are produced from an outbox row written in the same transaction as the state change.
Nothing publishes an event from a post-commit callback**, because that pattern loses events
whenever a process dies between the commit and the callback, which under load is often enough
to be a weekly incident and rare enough to be blamed on something else. A relay reads
unpublished rows in order, publishes them, and marks publication idempotently so a relay crash
republishes rather than losing. Consumers deduplicate on the event identifier. The relay's lag
is a primary alert.

An event carries an opaque sortable identifier; its store, organisation and environment; a
namespaced type from a closed vocabulary; the resource type and identifier; the payload at the
version the subscriber requested; the changed fields and their prior values for an update; the
instant the change happened rather than the instant the event was built; a monotonic sequence
per resource so a subscriber can detect and drop a stale delivery; the correlation identifier
of whatever caused it; and the actor.

A subscription names a target, an explicit list of types, an interface version, an optional
filter evaluated before delivery, and a per-subscription signing secret rotatable with an
overlap. **Wildcards are not offered**, because a wildcard subscription silently gains volume
when a new type ships. A subscription can only cover events the installation's scopes permit
reading, and a scope reduction disables it and notifies.

Delivery signs the raw body plus a timestamp, and **the subscriber verifies against the raw
bytes**, which the documentation says outright because verifying against a re-serialised body
is the most common integration failure. The timestamp is part of the signed material and
deliveries outside a stated window are rejected. Ordering is per resource and best-effort with
the sequence number as the authority; global ordering is not offered and the documentation
says so. Retries back off with jitter over `48` hours on a stated schedule. Success is any 2xx
inside a `5` second timeout. Failure classes are distinguished: a gone response disables the
subscription immediately and a client error does not retry beyond a small count. A target
failing consistently is paused with the merchant and partner notified, and a dead target does
not consume the delivery pool. **At-least-once is the guarantee and exactly-once is not
offered**, stated plainly rather than hidden, and subscribers are told to deduplicate on the
event identifier.

The event log retains `7` days, queryable by type, resource, instant and delivery outcome,
with every attempt recorded alongside its request headers, response status, truncated response
body, latency and next scheduled attempt. A merchant or partner may replay an event or a
range, and a replayed delivery is marked as such. **The merchant sees deliveries for their own
store, including failures, without needing the partner**, because a merchant unable to see why
an integration is failing is a support ticket the platform pays for. A payload larger than a
stated ceiling is truncated to identifiers with a fetch address and the truncation is flagged.
A resource deleted before delivery still delivers with its snapshot, because an event
describing a deletion whose payload is empty is useless. There is no backfill for a
subscription created after the event; a subscriber needing history uses a bulk read.

Every external system is specified by what it must survive rather than by which vendor fills
it: card acquiring and processing; alternative payment methods, each independently disableable;
bank payout rails; tax calculation; carrier rating and labels; carrier tracking; address
validation; the identity provider; message delivery; the content service; fulfilment services;
and sales channels. The shared rules: **every call has a timeout shorter than the caller's own
budget, and a call with no timeout is a defect**; retries apply only to idempotent operations
or ones carrying a key, backing off with jitter over a bounded attempt count and a stated total
window; a circuit opens per integration per store where the failure can be tenant-specific and
globally where it cannot, and an open circuit fails fast with its documented fallback; every
mutating outbound call carries a key derived from the platform's own operation identity, so a
retry is safe even when the platform never saw the first response; credentials are encrypted
with a key the application cannot export, rotated on a schedule and on suspicion, never logged
and never in a query parameter; tokens refresh ahead of expiry with a margin under a
single-flight guard so a herd of workers does not invalidate each other's refresh; every
inbound callback verifies a signature over the raw body plus a timestamp, rejects outside a
replay window and is idempotent on the sender's own identifier; clock skew tolerance is stated
per integration; the vendor version is pinned and a vendor's breaking change is caught by a
contract test in the build rather than by an incident; every integration has a development mode
bound to development stores; every call emits a span carrying the integration, the operation,
the outcome and the latency; and **only the fields an integration needs are sent**, so a
payment processor never receives a customer's order history.

The inbound callback pattern is specified once because it is the most common source of
correctness defects in a system of this shape: read the raw body and do not parse before
verifying; verify the signature over the raw bytes and the timestamp; reject outside the replay
window; deduplicate on the sender's event identifier, stored per integration; persist the raw
event and only then acknowledge with a success status; process asynchronously from the
persisted record; and **never let a processing failure turn into a non-acknowledgement**,
because the sender will retry forever and the queue is not the sender's problem to hold.

Five boundaries cannot be crossed in one transaction, and every correctness problem lives at
one of them: core service to money service; platform to payment processor; core service to
channel; platform to application; and terminal to platform. The consistency choice at each is
written down, because the failure mode of not writing it down is that different parts of the
build assume different answers. Order placement, its stock decrement and its ledger write for
one order are strongly consistent in one transaction, because overselling and unbalanced money
are both unacceptable. Payment capture against order state is eventual and reconciled hourly.
Catalog to storefront cache is eventual, bounded by the maximum stale age, because a briefly
stale price is recoverable and an uncacheable storefront is not. Inventory to channels is
eventual and reconciled daily, because the alternative is a distributed transaction with a
marketplace, which does not exist. Analytics to the ledger is eventual for non-money and exact
for money. **The audit entry and the action it records are strongly consistent in the same
transaction**, because an action without its audit entry is the one an attacker wants. The
search index trails the catalog by at most `5` seconds.

Where a business operation spans boundaries it is a saga with explicit compensations rather
than a distributed transaction, **and every compensation is itself idempotent, because a
compensation can fail and be retried too**. Placing an order reserves stock, authorizes
payment, creates the order, commits stock and captures or schedules capture; its compensation
voids the authorization and releases the reservation, and the order is never created in a half
state. A refund creates its record pending, calls the processor and writes the ledger entries
on confirmation; a failed call leaves it pending and retries rather than writing entries
speculatively. Buying a label debits, requests and stores, and a failure after the debit
reverses it. Fulfilling through a service reserves, requests and awaits acceptance, and a
rejection or a timeout releases the assignment and escalates. Installing an application
creates the installation, grants scopes, notifies the application and awaits its confirmation,
and no confirmation within a window uninstalls and reports.

**Graceful degradation is a design choice made once per dependency, not a reaction**, and
every degraded state is visible: the admin carries a system-state region naming any currently
degraded capability, and the storefront never silently renders less than it should without the
merchant being able to find out why. A failed search index falls back to a bounded database
search over title and stock-keeping unit with a banner saying results are limited, never an
empty list. A failed analytics store sends money surfaces to the ledger and marks non-money
surfaces stale. A failed tax service falls back to merchant rates with the order flagged. A
failed carrier rating falls back to the merchant's rate table. A failed address validator
leaves a plain form. A failed content service serves stale. A failed message provider queues
with a maximum age and then surfaces undelivered messages in the admin. A failing channel gets
its own queue paused with an alert while everything else continues. A failing application
renders an error region while the host surface works. A failing payment method's processor
disables that method at checkout with an explanation while the others stay. A failing
personalisation layer renders the unpersonalised page. **The primary database is the one
dependency with no degradation**, and the honest answer there is availability engineering
rather than a fallback.

A terminal that loses connectivity may sell within a configured floor against cached stock,
print a receipt and look up a cached product. **It may not perform any authorization-sensitive
action offline**: no return above a floor, no discount above a floor, no staff change, nothing
requiring an approval, and no read of another location. Its queue is durable on the device,
ordered, encrypted at rest, and has a maximum age after which the device refuses further
offline sales, showing how long it has left. On reconnect, transactions apply in order, each
idempotent on a device-generated key, and **a resulting negative level surfaces as a
discrepancy for a human rather than being silently clamped**. Revoking a device credential
stops its queue submitting and the queued transactions surface for manual reconciliation
rather than being dropped.

Release safety: schema changes expand, migrate and then contract, never making a destructive
change in the same release as the code that stops using the column; a deploy must be safe with
the previous version still running, because it will be, for minutes; feature flags exist per
store and per organisation with a kill switch and with flag state visible in the audit for
anything that changes behaviour; rollout is progressive by store cohort with automatic
rollback on a metric breach; contract tests fail the build on a change that breaks a supported
interface version; data backfills are resumable rate-limited jobs and never run inside a
deploy; and every release is rollback-safe or is gated behind a flag that is not.

Recovery targets: a recovery point of `5` minutes for transactional data and zero for the
ledger, achieved by synchronous replication of the money store; a recovery time of `1` hour
for the merchant storefront and checkout and `4` hours for the admin; continuous encrypted
in-region backups with restore rehearsed rather than assumed; **every restore replaying the
erasure log before going live**; a region failure failing the storefront and checkout over,
degrading the admin, and failing the money store over last and deliberately, because a
split-brain ledger is worse than an hour of downtime; and a status surface hosted
independently of the platform it reports on.

Observability answers three questions and every decision here serves one of them: is the
platform healthy; is one merchant's experience healthy; and what exactly happened in this one
incident. **The second is the one systems of this shape miss**, because a platform that is
healthy overall can be entirely broken for the one merchant whose channel integration died,
and that merchant is the one on the phone. Structured logs are one event per line carrying the
correlation identifier, the store, the actor and the outcome, and never a personal field.
Metrics are counters, histograms and gauges with a bounded label set, and **the store
identifier is never a metric label**, because per-store cardinality destroys a metrics store;
per-store observability comes from the event stream and from log queries instead. Traces are
distributed and sampled with every external call as a span. Profiles are continuous and
sampled on the storefront and checkout paths.

**One correlation identifier is generated at the edge and propagates through the request, the
transaction, the audit entry, the outbox row, the event, the job, the outbound call, the
approval and the log line**, so a single incident is one query against one identifier. It is
surfaced to the user on any error screen and in every error response, so a support
conversation begins with a reference rather than with "around three o'clock yesterday".

Some of this product's decisions are opaque unless deliberately explained, and each must be
inspectable by the merchant rather than only by the platform: why an order routed to a
location, from the routing trace; why a buyer sees a price, from the resolution recorded on the
order line; why an order is held, from the hold reason; why an action was refused, from the
policy decision's reason; why a message was not sent, from the suppression reason; why a
workflow did or did not fire, from the run's step log; why a delivery failed, from the attempt
log; and why a figure changed after the day closed, from the late-arrival flag. **A platform
that cannot answer these questions generates support load proportional to its own success.**

Objectives and alerts: merchant storefront and checkout availability at four nines, alerting on
error rate over a short window; checkout payment success rate held within a band of its own
trailing baseline rather than against an absolute threshold, because an absolute threshold
hides a processor degrading from ninety-eight percent to ninety-two; admin availability at
three nines and the machine interface between them; order placement latency within budget at
the 95th percentile; **outbox relay lag under `5` seconds, alerting loudly above `60`**; queue
age per class under a per-class target with the money and interactive queues paging; webhook
delivery success per target above `95%`; **ledger reconciliation exact, with any difference at
all paging somebody**; inventory reconciliation drift zero, with any drift raising a ticket
naming the item and the magnitude; audit chain integrity unbroken, with any break paging at the
highest severity; replica lag under a stated bound, above which replica reads shed to the
primary; and payout success rate within band. Every alert is actionable, has an owner and has a
runbook, because **an alert that fires routinely and is routinely ignored is worse than no
alert: it trains the ignoring**.

Per-merchant health has two faces: merchant-facing integration health per channel and per
application, delivery success, failing automations and degraded capabilities; and
platform-facing, a per-store health score composed of order success, checkout success,
delivery success and job backlog, alerting when a store crosses a threshold, so the platform
knows before the merchant calls.

An error shown to a person says what happened, whether it is theirs to fix and what to do
next; carries the copyable correlation identifier; leaks no stack trace, no internal identifier
beyond the correlation one and no hint that another tenant exists; states retryability, and
offers "try again" only where retrying can succeed; never loses what the user typed; and is
reported with the correlation identifier and without personal data.

**Performance budgets.** On the storefront at the 75th percentile on a mid-range device on a
slow connection: largest contentful paint `2.5s`; interaction to next paint `200ms`;
cumulative layout shift `0.1`; time to first byte `200ms` cached at the edge and `600ms`
uncached from the origin; initial compressed script `120KB` for the route excluding shared
runtime; initial compressed stylesheet `60KB`; one variable font file, subset, preloaded, with
a metric-compatible fallback so the swap causes no shift; and every image sized in the markup
so its box is reserved before the byte arrives. On the merchant storefront: largest contentful
paint `2.0s`, tighter than the marketing site because the buyer's intent is higher and the
bounce is more expensive; interaction to next paint `200ms`; uncached server render `300ms` at
the median; edge hit ratio above `90%` for anonymous traffic; `70KB` compressed client script
for a default theme; and **a per-store budget for third-party script with the offending
application named to the merchant when it is exceeded**, because a fast platform rendering a
theme carrying nine hundred kilobytes of somebody else's tracking is a slow shop and the
merchant has no other way to know who to blame. In the admin: shell paint `1.0s`; index first
row `1.5s`; index query `300ms` at the 95th percentile; detail page `1.2s`; command surface
first result `150ms` at the median; search freshness `5s` at the median after a write; and save
round trip `500ms` at the 95th percentile. In checkout: first step interactive `1.5s`; step
transition `400ms`; and payment submit to result `3s` at the 95th percentile excluding a buyer
authentication step.

Query discipline: no unbounded query, with every list carrying a server-enforced limit rather
than an offered one; no repeated per-row fetch, with batched loading for every association on
every list surface and a test that fails on a query-count regression; **authorization applied
inside the query rather than after the fetch**, which is a performance rule as well as a
correctness one; a covering index for every hot-path query with a plan regression failing the
build; read replicas permitted for index and report reads while any read inside a write
transaction and any read the same request will write from uses the primary; and bounded
monitored replica lag, with a surface reading after its own write reading the primary instead.

Client discipline: any list beyond `200` rows renders only what is on screen, and the wholesale
variant matrix does so without exception; code splitting is per route and per heavy component,
and the theme editor and the workflow canvas are never in the initial payload of anything
else; memoisation is applied where a measurement showed a problem rather than prophylactically;
no handler reads layout and then writes it inside a scroll or pointer handler; images below
the fold load lazily with an explicit box and the one above it loads eagerly and is preloaded;
and fonts are preloaded and subset per script, with the second-language surface loading its own
subset rather than a superset.

Volume targets the build must hold without a change of architecture: `1,000,000` products per
store; `2,000` variants per product; `250,000` orders per store per day at peak; `200`
locations per store; unbounded staff on the top plan; `100,000` companies per store;
`5,000,000` events per store per day; and `20,000` concurrent checkouts per store. Load testing
covers those targets including a peak-sale profile with a hundredfold spike over ten minutes.
Synthetic monitoring covers every budget per region continuously, alerting when the 75th
percentile crosses. Real user monitoring reports the same metrics segmented by market, device
class and theme. **A budget breach fails the build, because a budget that is routinely waived
is a budget that has been abandoned.**

**Security.** The assets an attacker wants are merchant money, directly stealable through
refunds, payouts and settlement-instrument changes; buyer payment credentials; buyer personal
data; merchant catalog and pricing, as competitive intelligence and as a lever for extortion;
staff sessions, which are the route to all of the above; application credentials, which are the
route to all of the above at scale across many merchants; and the storefront itself, for
defacement and for skimming injected into a checkout path.

The controls: three-layer tenancy with a generated test suite against a cross-tenant read; a
grantor who cannot grant what they do not hold, checked on the server, against privilege
escalation; enforcement in the service layer with the interface as a courtesy, against
authorization checked only in the interface; opaque identifiers plus a policy check on every
read and not merely on every list, against an insecure direct object reference; http-only,
secure, same-site cookies with rotation on privilege change and device-binding signals, against
session theft; same-site cookies plus an origin check plus a token on every state-changing
request, and **no state-changing request is ever a safe method**, against cross-site request
forgery; escaping at the render boundary by default, rich text stored as a parsed tree, a
content policy without inline execution, and merchant-supplied content treated as untrusted,
against cross-site scripting; sandboxed extensions under a content policy the extension cannot
widen, against script injection through an application; **checkout on its own prefix running no
merchant script, under the strictest content policy in the build, with integrity checks on its
own assets**, against card skimming; rate limiting, breached-password checks and a second
factor for dangerous permissions, against credential stuffing; identical responses for
existing and non-existing accounts, opaque identifiers and rate-limited lookups on gift-card
and discount codes, against enumeration; a signature over raw bytes plus a replay window,
against webhook forgery; a timestamp inside the signed material plus a nonce store, against
replay; dependencies pinned by hash, a generated bill of materials, provenance for build
artefacts and no post-install scripts in the build environment, against supply-chain
compromise; scoped, time-boxed, justified, region-limited and separately audited support
access, against insider access; cost-based limits, edge absorption and per-store fair share,
against denial of service; exports as dangerous actions with redaction, audit and expiring
artefacts, against exfiltration through exports; and content sniffed from bytes, processed out
of band, served from a separate origin with a download disposition and never executed, against
a malicious upload.

Payment data: **the platform's general services stay out of the card-data environment**. Only
the checkout payment layer touches a card and it hands back a token. No primary account number
is stored in any store, log, backup or analytics record, ever. Display is brand, last four and
expiry only. Transmission is to the processor only over a pinned, mutually authenticated
channel. The payment layer is network-segmented, separately deployed, separately
access-controlled and separately logged, and is penetration-tested independently at a stated
cadence with findings tracked to closure.

Secrets live in a managed store, never in source, never in an environment file committed
anywhere and never in a container image. They rotate on a schedule, on demand, and
automatically on suspicion, with an overlap window so rotation is not an outage. One secret
exists per purpose per environment, because a secret shared across environments means a
development compromise is a production compromise. Personal-data encryption keys are per
organisation, held in the organisation's region, and never exportable by the application. A
scanner runs in the build and over the repository history, and a hit fails the build and
triggers rotation.

Content policy: the storefront forbids inline execution with per-merchant allowances for
declared applications, generated rather than hand-maintained; checkout carries the strictest
policy with no merchant allowance at all; the admin is strict with extension frames on their
own origins; rich text renders from a parsed tree and an unknown node type renders as nothing
rather than as raw markup; and merchant-supplied templates render through an engine with no
arbitrary execution and a declared data contract.

Vulnerability management: continuous dependency scanning with a stated remediation window by
severity; static analysis on every change; scheduled dynamic scanning against every deployed
environment; annual penetration testing plus on major architectural change plus continuously on
the payment path; a published responsible-disclosure policy with a monitored channel and a
stated response time; and a written, rehearsed incident-response plan with a communication path
to merchants that does not depend on the affected system.

**No credential, API key or admin token appears in anything the browser downloads.** Every
response carries the standard security headers, including a strict transport policy and a
nosniff content-type policy. **Every public route carries its own title and description and no
two public routes share them.** A sitemap lists every public route and a robots file points at
the sitemap.

The schema is generated from the implementation and never hand-maintained, because a documented
field that does not exist is a defect class this eliminates. Every operation carries a runnable
example against a development store. The change log is machine-readable per version with every
addition, deprecation and removal. Contract tests run against every supported version on every
deploy. Deprecation telemetry is recorded per installation and per deprecated field, so a
version is retired on evidence rather than on a guess, and a client on a retiring version is
warned in headers, then by mail to the partner, then by an admin notice to affected merchants,
on a stated schedule.
## Data model

Ninety-four tables in fourteen groups. All timestamps are UTC.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
> data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
> written into `/app/USER_README.md` alongside each account so a grader can sign in.

### Conventions

A primary key is an opaque, sortable, type-prefixed identifier, unique across the platform,
which makes an identifier self-describing in a log and in a support conversation. Money is
always two columns, an integer in minor units and a currency code; never one column, never a
decimal type, never a float. Quantities are integers, and a fractional quantity where a
merchant sells by weight is a separate typed column with its unit. Timestamps are instants
with a zone, database-assigned; a local date is a date plus a named timezone. Soft deletion
exists only where a regulation requires retention or where a live storefront would break;
everywhere else deletion is deletion, because a soft-delete flag every query must remember is
a leak waiting to happen. Enumerations are database enumerations or check constraints, not
free strings. Foreign keys are declared with explicit delete behaviour, restricting by default
and cascading only where the child is meaningless alone. Nullability is explicit and a
nullable column carries a documented meaning for null. A metafield lives in one typed extension
table per owner type rather than in a document column, so it can be indexed, validated and
authorized.

**Every tenant-owned table carries three columns**: `store_id`, not null, a foreign key, and
the first column of every index that matters; `environment`, not null, `live` or
`development`, and part of every unique constraint; and `data_region`, not null, denormalised
from the organisation so a region predicate never needs a join. **A database connection whose
session is scoped to one store returns zero rows from every tenant-owned table populated only
for another store, even with the application layer bypassed entirely**, and a test generated
from the schema proves it so a new table cannot be added without being covered.

### Identity and access

`person` holds an email unique case-insensitively, a name, a locale and a status, and exists
independently of any store. `person_factor` holds a person, a type, an encrypted secret, a
confirmation instant and a last-used instant. `person_recovery_code` holds a person, a hash
and a consumption instant. `organisation` holds a name, a country, a data region, a retention
policy and a federation-required flag. `store` holds an organisation, a name, a globally
unique handle, a country, a currency, a timezone, a data region, a lifecycle state, a plan and
a creation instant. `membership` holds a person and a store with a status, an inviting actor,
an invitation instant, an acceptance instant and a source distinguishing invitation from
federated provisioning, unique on person and store. `org_membership` is distinct from it and
holds a person, an organisation, a role and a status. `role` holds a nullable store, a nullable
organisation, a name, a description and a built-in flag, where a null owner means a
platform-owned built-in role. `role_permission` holds a role and a permission.
`membership_role` holds a membership, a role, a granting actor and a granting instant.

`constraint_set` is the attribute layer and holds a membership, a refund ceiling in minor units
with its currency, a discount ceiling as a percentage with an absolute cap, a readable
personal-field set and a data region. `location_assignment` and `company_assignment` each hold
a membership, their target, a granting actor, a granting instant and an expiry, and
`company_assignment` additionally holds the role on that account. `grant` holds a membership, a
permission, its constraints, a justification, a requesting actor, an approving actor, a start
and an expiry, for time-boxed direct grants.

`session` holds a person, a nullable store, an environment, a creation instant, a last-seen
instant, an idle expiry, an absolute expiry, a step-up instant, an address, a user agent and a
revocation instant. Its identifier is opaque and it contains no claims.

`federation_config` holds an organisation, an issuer, a certificate, an enforcement flag, a
skew tolerance and the break-glass member set. `federation_claim_map` holds a federation
config, a claim, a value, a role and a nullable store. `assertion_replay` holds an issuer, an
assertion identifier and the instant it was seen, unique, retained longer than the skew
tolerance.

### Catalog

`product`, `product_tag`, `product_option`, `product_option_value`, `variant`,
`variant_option_value`, `inventory_item`, `media`, `collection`, `collection_product`,
`metafield_definition`, `metafield` and `publication`.

`product` holds a store, a title, a description document, a handle unique per store, a product
type, a vendor, a status, a template suffix and its instants. `variant` holds a product, a
stock-keeping unit, a barcode, a price in minor units with its currency, a compare-at amount, a
cost amount, a weight with its unit, a requires-shipping flag, a taxable flag, a tax code, a
position, an inventory policy and an inventory item. `variant_option_value` is unique on
variant and product option, **and the option value tuple is unique per product with an arity
equal to the product's option count**. `media` holds its owner, a kind, alternative text, a
position and a generated seed. `collection` holds a store, a title, a handle, a kind, a rule
document, a sort order, a publication instant and the instant of its last successful build.
`metafield_definition` holds a store, an owner type, a namespace, a key, a type, its
validations and its searchable and filterable flags. `publication` holds a product or
collection, a channel, a publication instant and an optional scheduled instant.

### Inventory

`location` holds a store, a name, a structured address, a fulfils-online-orders flag, a retail
flag, a pickup-enabled flag, pickup instructions and an active flag. `inventory_level` holds
an inventory item and a location with `on_hand`, `committed`, `reserved`, `incoming`,
`damaged`, `quality_control` and `safety_stock`, unique on item and location, **and
`available` is a generated column rather than a writable one**. `inventory_movement` is
append-only and holds the item, the location, which quantity moved, the delta, the resulting
quantity, a reason, the causing object's type and identifier, the actor, an idempotency key
and the instant it occurred. `transfer` holds a store, an origin, a destination, a state, an
expected arrival and a reference; `transfer_line` holds quantities ordered, received and
rejected. `reservation` holds a checkout, an inventory item, a location, a quantity and an
expiry, and is swept.

### Orders and fulfilment

`order` holds a store, a number per store, a channel, a market, a customer, an optional
company and company location, a currency and a presentment currency, a subtotal, a discount,
shipping, tax, duty, tip, total, paid, refunded and outstanding amounts, a financial status, a
fulfilment status, a cancellation instant and reason, a risk level, the membership that created
it, the contact it was created on behalf of, its instants, and a version carrying the
concurrency check. `order_line` holds the order, a nullable variant, snapshots of the product
title, the variant title and the stock-keeping unit, a quantity, a price in minor units, a
total discount in minor units, a discount allocation document, a tax lines document, a weight,
a requires-shipping flag and a fulfilable quantity. `order_address` holds the order, a kind,
structured fields and a country. `order_attribution` holds the order, a source, a landing
route, a referrer, a campaign, an agent and a delegation reference.

`draft_order` holds a store, a company, a contact, the creating membership, a state, an expiry,
totals and terms. `fulfilment_order` holds the order, a nullable assigned location, a nullable
fulfilment service, a state, a hold reason, a request instant and a routing trace document.
`fulfilment_order_line` holds a fulfilment order, an order line and a quantity. `fulfilment`
holds a fulfilment order, a state, a tracking company, a tracking number, a tracking address
and shipped and delivered instants.

`return` holds the order, a state, a request instant, a decision, its decider and instant, a
refund reference and an exchange order reference. `return_line` holds the return, an order
line, a quantity, a reason, a condition and a restock decision. `return_shipment` holds the
return, a label reference, tracking, a received instant, its receiver and a location.

### Money

`balance` holds a store, a currency and a kind, unique on the three. `ledger_transaction`
holds a store, a kind, an effective instant, a creation instant, a nullable idempotency key,
the source type and identifier, and a nullable reference to the transaction it reverses.
`ledger_entry` holds a transaction, a balance, a direction and an amount in minor units with
its currency. **`ledger_entry` rows are never updated and never deleted, enforced by the
privilege the application role holds rather than by convention, and a deferred constraint
asserts that a transaction's per-currency sum is zero at commit.** A reversal references its
original and a check prevents a reversal of its own reversal. A transaction with a source
exists once per idempotency key.

`payment` holds a store, a nullable order, an amount in minor units with its currency, a
presentment amount and currency, a captured amount, a status, a method class, an instrument
token, a brand, the last four digits, an expiry, a risk score, a risk level, an authorization
expiry, a processor reference, an idempotency key, and creation and capture instants.
`payment_pii` holds the cardholder name and billing address encrypted in a separate table, so
**the join itself is the authorization boundary**.

`refund` holds a payment, an amount in minor units with its currency, a reason, a status, a
nullable ledger transaction, a nullable approval request and an idempotency key, **under a
check constraint that the sum of non-failed refunds may not exceed the payment's captured
amount**. `dispute` holds a payment, a network reference that is unique, an amount, a reason, a
state, an evidence deadline, a submission instant, an outcome and a ledger transaction.
`dispute_evidence` is field-level so continuous saving is natural. `payout` holds a store, a
currency, an amount, a state, a cutoff instant, an arrival estimate, a settlement instrument
and a failure code, and `payout_item` joins it to the ledger transactions that made it.
`settlement_instrument` holds a store, a currency, an encrypted holder name, an encrypted
account number, encrypted routing details, the last four digits, a state, a verification
instant and an effective-from instant, and is versioned rather than edited. `platform_fee`
holds an order, a rate version, a basis amount, a fee amount and a ledger transaction, and
`fee_rate_version` holds a plan, a country, a rate and its effective window. `gift_card` holds
a store, a hashed code, the last four characters, a balance, a currency, an expiry, an issuing
source and a disable instant. `store_credit` holds a store, a customer, a balance and a
currency.

### Customers and business buyers

`customer`, `customer_pii`, `customer_consent`, `customer_address`, `segment`,
`segment_member`, `company`, `company_location`, `company_contact` and `company_credit`.

`customer_consent` holds a customer, a channel, a state, the instant it was collected, the
source, the text version and the address. `segment` holds a store, a name, an expression
document, a last-evaluated instant and a size, with `segment_member` materialised. `company`
holds a store, a name, an external identifier, a state, default payment terms, tax
registrations and a creation instant. `company_location` holds billing and shipping addresses
and overrides for payment terms, catalog and buyer settings. `company_contact` holds a company,
a customer, a role, a may-order flag, a may-draft-only flag, a spending limit in minor units
and the locations they may order for. `company_credit` holds a limit and a currency, with the
exposure derived from the ledger rather than stored independently.

### Markets and pricing

`market` holds a store, a name, a type, a state, a nullable parent market, a currency, a
rounding rule, a primary language and a tax treatment. `market_language`, `market_region`,
unique per store per country, `market_domain` and `market_setting`, which exists only where a
setting is overridden, so **the count of those rows is the customisation figure the market
index displays**. `catalog`, `catalog_company`, `catalog_product`, `price_list`,
`price_list_entry`, `price_break` and `quantity_rule`, the last holding a catalog, a variant, a
minimum, a maximum and an increment.

### Channels, applications and events

`channel` holds a store, a kind, a name, a state, its capability set, a configuration and a
credential reference. `channel_order_reference` holds a channel, an external order identifier
and an order, unique on channel and external identifier. `application` holds a partner, a name,
a kind, requested scopes, callbacks and extension declarations. `installation` holds an
application, a store, a state, the installing actor, the install instant and a credential hash.
`scope_grant`, `app_charge`, `event`, `outbox`, `subscription` and `delivery_attempt` complete
the group. `outbox` holds an aggregate type and identifier, a sequence, a payload and a
nullable publication instant.

### Workflow and approval

`workflow` holds a store, a name, a state, a version, its effective permissions, its creating
actor, its activating actor and the activation instant. `workflow_node` holds a workflow
version, a kind, a type and a configuration; `workflow_edge` holds the source node and port and
the target node; `workflow_run` holds a workflow version, the triggering event, a state and its
instants; `workflow_step` holds a run, a node, an input snapshot, an output, a state, an error
and an attempt count.

`approval_request` holds a store, the proposed action type, its full parameters, the requesting
membership, the reason, the permission required to decide it, the approver scope, a state, an
expiry, **an idempotency key** and a correlation identifier. `approval_decision` holds the
request, the deciding membership, the decision, a note and the decision instant.
`approval_delegation` holds the delegating and receiving memberships, the permission and its
window.

### Governance

`audit_entry` holds a nullable store, an organisation, an actor type and identifier, an action,
a resource type and identifier, the before and after of the changed fields only, an address, a
user agent, a correlation identifier, a severity, a database-assigned instant, **the previous
entry's hash and its own hash**. It is append-only. `consent_record`, `data_request`,
`retention_policy` and `encryption_key_ref` complete the group.

### Indexing and volume

Every tenant table is indexed on its store, its environment and its creation instant
descending, which is the universal index-page query. Orders additionally index on their two
statuses and creation instant for the default view and the saved views, on customer and
creation instant for customer history, and on market and on channel with creation instant for
the scoped views. An inventory level is unique on its item and location, which is the hot read
on every product page, and is additionally indexed on location and available for the low-stock
report and its automation trigger. Inventory movements are indexed for reconciliation and
ledger entries for balance computation, whose identifier ordering makes it a range scan. A
ledger transaction's idempotency key is unique per store where it is present. Variants are
indexed on their stock-keeping unit and on their barcode for the command surface and the
terminal. A price-list entry is unique on its price list and variant. Events are indexed for
the log and for ordering. Audit entries are indexed three ways, which are the three queries
anybody actually runs: by organisation and instant, by resource and instant, and by actor and
instant. A company assignment is indexed in both directions, which is the representative
predicate.

**No index on a nullable tenant column exists without the store identifier leading it, and no
query plan in production scans a tenant table without a store predicate**, the latter enforced
by a test rather than by review.

Events and delivery attempts are time-partitioned and dropped by partition on retention. Audit
entries are time-partitioned, retained long and never dropped without a governance decision.
Inventory movements and ledger entries are time-partitioned and never dropped. Orders and
their children are partitioned by store where a store's volume demands it, because the dominant
access is by store. Analytics facts live in their own store.

### Derived rather than stored

`available` on an inventory level. A customer's order count, total spent and first and last
order instants. A company's credit exposure. An article's reading time. A market's
customisation count. A balance, which is the sum of its ledger entries. A collection's
membership, where the collection is rule-based, materialised on rebuild rather than computed on
read. Every one of these is computed or materialised, never written by hand.

### Physical table names

Three physical table names are part of the contract rather than an implementation choice,
because the product's own reconciliation surfaces read them: `ledger_entry`,
`approval_request`, `inventory_level`. Create them under exactly those names. Every other
table above takes the name it is given here, and a framework's default prefixing is
turned off rather than accepted.

### Seed data

One organisation, `Northbeam Retail Group`, in data region `ap-south`.

Two stores, both in India, currency `inr`, timezone `Asia/Kolkata`: `Oakleaf and Co` with
handle `oakleaf`, and `Modern Mallard` with handle `modern-mallard`.

Five people, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Store | Refund ceiling |
|---|---|---|---|
| `owner@example.com` | `owner` | `Oakleaf and Co` | unbounded |
| `manager@example.com` | `store_manager` | `Oakleaf and Co` | none |
| `support@example.com` | `support_agent` | `Oakleaf and Co` | `500000` |
| `finance@example.com` | `finance` | `Oakleaf and Co` | `20000000` |
| `mallard@example.com` | `store_manager` | `Modern Mallard` | none |

Two locations on `Oakleaf and Co`: `Pune Warehouse`, which fulfils online orders, and
`Delhi Flagship`, which is retail with pickup enabled.

Six products on `Oakleaf and Co`, one variant each, priced in minor units: `Pauline` at
`1122600`, `Sanders` at `1330400`, `Addie` at `956400`, `Sedgewick` at `1497200`, `Chip` at
`748400` and `Carry` at `5986900`. Each holds `12` on hand at `Pune Warehouse` and `3` at
`Delhi Flagship`, except `Carry`, which holds `1` at `Pune Warehouse` and `0` at
`Delhi Flagship`, and is the boundary a contention check needs.

Five orders on `Oakleaf and Co`, every one `paid` and `unfulfilled`:

| Number | Customer | Total in minor units |
|---|---|---|
| `#2050` | `Guy Hawkins` | `850900` |
| `#2049` | `Floyd Miles` | `3411200` |
| `#2048` | `Cody Fisher` | `850900` |
| `#2047` | `Ralph Edwards` | `3411200` |
| `#2046` | `Theresa Webb` | `850900` |

One order on `Modern Mallard`, `#3001`, customer `Anu Gupta`, total `1998640`.

One company on `Oakleaf and Co`, `Halcyon Goods`, on payment terms `Net 30`, with one company
location and one company contact, and with no representative assigned at seed time.

`#2049` is the boundary the graded rule needs: `3411200` is above `support@example.com`'s
ceiling of `500000` and below `finance@example.com`'s of `20000000`, so a full refund of it is
a proposal from the first session and an execution from the second.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- **Multi-tenant, and tenancy is never a request parameter.** One organisation, two stores and
  five people are seeded; there is no public staff registration.
- **No native application, no desktop client, no browser extension.** One web application.
- **No terminal firmware, no card-reader pairing, no device provisioning.** The terminal is a
  client of the same contract and its admin-side surfaces exist; the device does not.
- **No editorial authoring back office.** Editorial content is consumed.
- **No real external service is contacted at run time.** Card acquiring, bank payout rails, tax
  calculation, carrier rating and tracking, address validation, message delivery, the content
  service and every sales channel are modelled behind this product's own contract with the
  documented fallback for each. No outbound network call is made while the app is running.
- **No second database, cache, queue, object store, identity provider or mail vendor.**
  `postgres` and `keycloak` are the only backing services.
- **No binary asset of any kind ships.** No image, video, font file, icon file or vector
  document. Every raster and every mark is generated.
- **No hard-coded host or port.** Every one is read from the environment.
- **No decimal or floating-point type anywhere on a money path**, in the database, in the
  interface or in a report.
- **No behaviour that depends on a hover-only affordance**, because a hover affordance is
  gated on pointer capability and a phone has none.
- **No page that scrolls horizontally**, at any width, in any language, in either direction.
- The app stays responsive at the stated volume targets, and remains correct rather than merely
  fast when two people reach the same last unit or the same single-use code at the same instant.

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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status": "ok"}` |
| `GET /api/stores` | none | a top-level JSON array of the stores the session's person is a member of, each with `id`, `handle` and `name` |
| `GET /api/orders` | `status`, `financial_status`, `fulfilment_status`, `location`, `cursor`, `limit` | a top-level JSON array of orders in the session's store, each with `id`, `number`, `customer_name`, `total_minor`, `currency`, `financial_status`, `fulfilment_status` and `item_count` |
| `GET /api/orders/{id}` | none | the order, with its lines, its addresses and its timeline |
| `POST /api/orders/{id}/refunds` | `amount_minor`, `currency`, `reason`, `restock`, `idempotency_key` | either the created refund, with `id`, `amount_minor`, `currency`, `status` and `ledger_transaction_id`, or, when the amount exceeds the actor's ceiling, the created approval request with `id`, `state` equal to `pending`, `action_type` equal to `order_refund`, `amount_minor`, `required_permission` and `expires_at` |
| `GET /api/approvals` | `state`, `cursor`, `limit` | a top-level JSON array of approval requests in the session's store, each with `id`, `action_type`, `amount_minor`, `currency`, `requested_by`, `state`, `required_permission` and `expires_at` |
| `GET /api/approvals/{id}` | none | the request, with its full proposed parameters and its decisions |
| `POST /api/approvals/{id}/decision` | `decision`, which is `approve` or `decline`, a `note`, and `idempotency_key` | the decided request, with `state`, `decided_by`, `decided_at` and, on approval, `executed_effect` naming the refund it produced |
| `GET /api/inventory` | `location`, `cursor`, `limit` | a top-level JSON array of inventory levels, each with `variant_id`, `sku`, `location_id`, `on_hand`, `committed`, `reserved` and `available` |
| `POST /api/inventory/adjustments` | `variant_id`, `location_id`, `quantity_name`, `delta`, `reason`, `idempotency_key` | the resulting level and the movement entry it wrote |
| `GET /api/products` | `status`, `cursor`, `limit` | a top-level JSON array of products with their variants |
| `GET /api/balances` | none | a top-level JSON array of balances for the session's store, each with `currency`, `kind` and `amount_minor` |
| `POST /api/checkouts` | `store`, `lines`, `idempotency_key` | the checkout session with its token and its reserved lines |
| `POST /api/checkouts/{token}/complete` | `payment_method`, `address`, `idempotency_key` | the placed order, or a rejection naming the short line |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call
returns the named resource or shape. **An invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success**, carrying a machine code, a
human message and the path to the offending field; the exact status is yours to choose from
the conventional ones. Bearer authorization is required on everything except login, health and
webhook receivers, which authenticate by signature rather than by a user token. Every mutating
endpoint accepts `idempotency_key` and every one that moves money, stock or a message requires
it.

### No mocks

`postgres` and `keycloak` are real services with real persisted state that this app does not
control. Any of the following is a contract violation however good the interface looks: an
in-memory list of orders or approvals that the app returns to itself; a session minted by the
app without the issuer having authenticated the person; a store context taken from a request
parameter and trusted; a hard-coded response standing in for a query; a balance computed by
adding up orders rather than read from its ledger entries; a refund that writes a row without a
balanced ledger transaction behind it; an approval whose execution writes the refund before the
decision; or an `available` quantity stored as a column somebody writes.

**The named provider is the fact - the app's UI and its own tables can only reflect what lives
in the provider, never substitute for it.**

## Definition of done

A support agent can refund a small amount on a paid order and see the money leave the store's
balance at once. Refunding more than that agent's ceiling instead creates an approval request
that moves nothing, and a finance lead approves it once and the refund exists exactly once. The
agent cannot approve their own request, and a member of one store sees nothing belonging to
another.
