# Checklist: Mercato

Items: 1389
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Unpinned values flagged: 10

Source of every item: `instruction.md`. Nothing here is derived from any
other file, because no other file existed when the extraction ran.

## C-OV Overview

- [ ] `C-OV-01` `capability` Mercato is a multi-tenant commerce platform serving four surfaces from one application. `src: Overview, instruction.md`
- [ ] `C-OV-02` `capability` A public marketing storefront sells the platform to a retail organisation. `src: Overview, instruction.md`
- [ ] `C-OV-03` `capability` An authenticated merchant admin is where an organisation runs its trade. `src: Overview, instruction.md`
- [ ] `C-OV-04` `capability` Buyer surfaces cover a merchant's online store, a hosted checkout, a customer account area, an order status page, a point-of-sale terminal. `src: Overview, instruction.md`
- [ ] `C-OV-05` `capability` A machine surface serves third-party applications, sales channels, shopping agents. `src: Overview, instruction.md`
- [ ] `C-OV-06` `constraint` The account belongs to a business rather than to a person, so no owning user scopes a row. `src: Overview, instruction.md`
- [ ] `C-OV-07` `constraint` Every query is scoped to a store, then filtered by what the acting member may see. `src: Overview, instruction.md`
- [ ] `C-OV-08` `capability` A permitted action can be too large for the person permitted to perform one, which turns the action into a proposal. `src: Overview, instruction.md`
- [ ] `C-OV-09` `constraint` Mercato does not build terminal firmware, pair card readers, ship a native application, author editorial content. `src: Overview, instruction.md`
- [ ] `C-OV-10` `constraint` No lifecycle transition deletes a merchant's data as a side effect of anything else. `src: Overview, instruction.md`

## C-RL User roles

- [ ] `C-RL-01` `role` Staff signup is closed, so accounts exist only as seeded records. `src: User roles, instruction.md`
- [ ] `C-RL-02` `role` A person exists independently of any store, with membership in more than one store permitted. `src: User roles, instruction.md`
- [ ] `C-RL-03` `role` A role names which actions a member may perform. `src: User roles, instruction.md`
- [ ] `C-RL-04` `role` A constraint names which rows a member may act on, covering locations, markets, channels, assigned companies, readable personal fields, a refund ceiling. `src: User roles, instruction.md`
- [ ] `C-RL-05` `role` The `owner` role grants everything in the store, plus the plan, plus the transfer of ownership. `src: User roles, instruction.md`
- [ ] `C-RL-06` `role` The `administrator` role grants everything except changing the plan, cancelling the plan, transferring ownership. `src: User roles, instruction.md`
- [ ] `C-RL-07` `role` The `store_manager` role denies managing staff, editing payment settings, editing the settlement instrument. `src: User roles, instruction.md`
- [ ] `C-RL-08` `role` The `merchandiser` role denies reading a product's cost, editing a product's cost, adjusting stock, reading orders. `src: User roles, instruction.md`
- [ ] `C-RL-09` `role` The `fulfilment_operator` role is constrained to assigned locations for fulfilment, for stock adjustment, for receiving returns. `src: User roles, instruction.md`
- [ ] `C-RL-10` `role` The `support_agent` role denies reading a full payment instrument, denies reading a residential address. `src: User roles, instruction.md`
- [ ] `C-RL-11` `literal` The `support_agent` refund ceiling is `500000` in minor units. `src: User roles, instruction.md`
- [ ] `C-RL-12` `literal` The `finance` refund ceiling is `20000000` in minor units. `src: User roles, instruction.md`
- [ ] `C-RL-13` `role` The `finance` role denies managing staff, editing a posted ledger entry, editing products. `src: User roles, instruction.md`
- [ ] `C-RL-14` `role` The `sales_representative` role sees only assigned companies, with their orders, quotes, price lists. `src: User roles, instruction.md`
- [ ] `C-RL-15` `role` The `retail_associate` role denies discounting beyond a ceiling, denies opening the day's totals, denies seeing another location's takings. `src: User roles, instruction.md`
- [ ] `C-RL-16` `role` The `retail_manager` role adds opening the register, closing the register, managing staff codes, adjusting stock at assigned locations. `src: User roles, instruction.md`
- [ ] `C-RL-17` `role` The `analyst` role mutates nothing anywhere. `src: User roles, instruction.md`
- [ ] `C-RL-18` `role` The `auditor` role reads the audit record plus every resource, with writing denied structurally. `src: User roles, instruction.md`
- [ ] `C-RL-19` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles, instruction.md`
- [ ] `C-RL-20` `contract` A direct API call from a `support_agent` session to a `finance`-only endpoint is rejected as unauthorized. `src: User roles, instruction.md`
- [ ] `C-RL-21` `contract` A rejected unauthorized call leaves the protected state unchanged. `src: User roles, instruction.md`
- [ ] `C-RL-22` `constraint` Nobody may grant a permission the granting actor does not already hold. `src: User roles, instruction.md`
- [ ] `C-RL-23` `constraint` The escalation guard is enforced server-side on every surface, the machine surface included. `src: User roles, instruction.md`
- [ ] `C-RL-24` `ui` A denial names which of four causes applies: missing permission, plan exclusion, region policy, nobody in the store. `src: User roles, instruction.md`
- [ ] `C-RL-25` `constraint` A list filters by policy inside the query, so a row the actor may not see is absent. `src: User roles, instruction.md`
- [ ] `C-RL-26` `constraint` A stated result count reflects rows removed by policy, never the unfiltered total. `src: User roles, instruction.md`
- [ ] `C-RL-27` `constraint` A field the actor may not read is redacted at the serialisation boundary. `src: User roles, instruction.md`
- [ ] `C-RL-28` `ui` A redacted field renders as a consistent mask rather than as an empty value. `src: User roles, instruction.md`
- [ ] `C-RL-29` `role` The `orders` namespace carries `read`, `create_draft`, `edit`, `cancel`, `capture_payment`, `refund`, `mark_paid`, `archive`, `export`. `src: User roles, instruction.md`
- [ ] `C-RL-30` `role` The `fulfilment` namespace carries `read`, `fulfil`, `request_fulfilment`, `hold`, `release`, `buy_label`, `cancel_fulfilment`. `src: User roles, instruction.md`
- [ ] `C-RL-31` `role` The `returns` namespace carries `read`, `approve`, `decline`, `receive`, `restock`, `refund`. `src: User roles, instruction.md`
- [ ] `C-RL-32` `role` The `products` namespace carries `read`, `create`, `edit`, `delete`, `publish`, `edit_cost`, `edit_price`, `export`, `import`. `src: User roles, instruction.md`
- [ ] `C-RL-33` `role` The `inventory` namespace carries `read`, `adjust`, `transfer_create`, `transfer_receive`, `set_available`. `src: User roles, instruction.md`
- [ ] `C-RL-34` `role` The `customers` namespace carries `read`, `read_pii`, `create`, `edit`, `delete`, `export`, `segment_manage`. `src: User roles, instruction.md`
- [ ] `C-RL-35` `role` The `companies` namespace carries `read`, `read_assigned`, `create`, `edit`, `approve_request`, `assign_representative`. `src: User roles, instruction.md`
- [ ] `C-RL-36` `role` The `discounts` namespace carries `read`, `create`, `edit`, `delete`, `exceed_ceiling`. `src: User roles, instruction.md`
- [ ] `C-RL-37` `role` The `markets` namespace carries `read`, `create`, `edit`, `publish`, `manage_catalog`, `manage_price_list`, `manage_domain`. `src: User roles, instruction.md`
- [ ] `C-RL-38` `role` The `finances` namespace carries `read_balance`, `read_payout`, `read_dispute`, `submit_evidence`, `manage_payout_schedule`, `read_settlement_instrument`, `edit_settlement_instrument`. `src: User roles, instruction.md`
- [ ] `C-RL-39` `role` The `analytics` namespace carries `read`, `read_finance`, `create_report`, `export`. `src: User roles, instruction.md`
- [ ] `C-RL-40` `role` The `online_store` namespace carries `read`, `edit_theme`, `publish_theme`, `edit_content`, `manage_menu`, `manage_domain`. `src: User roles, instruction.md`
- [ ] `C-RL-41` `role` The `apps` namespace carries `read`, `install`, `uninstall`, `manage_scopes`, `read_credentials`. `src: User roles, instruction.md`
- [ ] `C-RL-42` `role` The `automations` namespace carries `read`, `create`, `edit`, `activate`, `deactivate`, `run_manually`. `src: User roles, instruction.md`
- [ ] `C-RL-43` `role` The `settings` namespace carries `read`, `edit_general`, `edit_payments`, `edit_shipping`, `edit_taxes`, `edit_locations`, `edit_checkout`, `edit_notifications`, `edit_policies`. `src: User roles, instruction.md`
- [ ] `C-RL-44` `role` The `staff` namespace carries `read`, `invite`, `edit_permissions`, `remove`, `manage_roles`. `src: User roles, instruction.md`
- [ ] `C-RL-45` `role` The `plan` namespace carries `read`, `change`, `cancel`. `src: User roles, instruction.md`
- [ ] `C-RL-46` `role` The `audit` namespace carries `read`, `export`. `src: User roles, instruction.md`
- [ ] `C-RL-47` `role` The `pos` namespace carries `operate`, `open_close_register`, `discount_up_to_ceiling`, `accept_return`, `read_daily_totals`, `manage_staff_pins`. `src: User roles, instruction.md`
- [ ] `C-RL-48` `role` The permission `customers.read_pii` is separate from `customers.read`. `src: User roles, instruction.md`
- [ ] `C-RL-49` `role` The permission `products.edit_cost` is separate from `products.edit_price`. `src: User roles, instruction.md`
- [ ] `C-RL-50` `literal` The account `owner@example.com` holds the `owner` role on the first seeded store. `src: User roles, instruction.md`
- [ ] `C-RL-51` `literal` The account `manager@example.com` holds the `store_manager` role on the first seeded store. `src: User roles, instruction.md`
- [ ] `C-RL-52` `literal` The account `support@example.com` holds the `support_agent` role on the first seeded store. `src: User roles, instruction.md`
- [ ] `C-RL-53` `literal` The account `finance@example.com` holds the `finance` role on the first seeded store. `src: User roles, instruction.md`
- [ ] `C-RL-54` `literal` The account `mallard@example.com` holds the `store_manager` role on `Modern Mallard` only. `src: User roles, instruction.md`
- [ ] `C-RL-55` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, instruction.md`
- [ ] `C-RL-56` `constraint` Nothing belonging to the first seeded store is reachable from a `mallard@example.com` session by navigation. `src: User roles, instruction.md`
- [ ] `C-RL-57` `constraint` Nothing belonging to the first seeded store is reachable from a `mallard@example.com` session by address. `src: User roles, instruction.md`
- [ ] `C-RL-58` `constraint` Nothing belonging to the first seeded store is reachable from a `mallard@example.com` session by identifier. `src: User roles, instruction.md`

## C-CF Core features

- [ ] `C-CF-01` `capability` A refund is composed against a paid order. `src: Core features, instruction.md`
- [ ] `C-CF-02` `capability` A refund may be by line, by amount, against shipping, each producing its own entries. `src: Core features, instruction.md`
- [ ] `C-CF-03` `capability` A refund at or below the acting member's ceiling executes immediately. `src: Core features, instruction.md`
- [ ] `C-CF-04` `data` An executed refund moves money out of the store's balance. `src: Core features, instruction.md`
- [ ] `C-CF-05` `data` An executed refund writes one balanced ledger transaction. `src: Core features, instruction.md`
- [ ] `C-CF-06` `data` An executed refund advances the order's financial status to `partially_refunded` or to `refunded`. `src: Core features, instruction.md`
- [ ] `C-CF-07` `data` An executed refund appends a refund entry to the order timeline naming the acting member, naming the instant. `src: Core features, instruction.md`
- [ ] `C-CF-08` `capability` A refund above the acting member's ceiling neither executes nor is rejected: an approval request is created. `src: Core features, instruction.md`
- [ ] `C-CF-09` `constraint` A pending refund request has moved no money. `src: Core features, instruction.md`
- [ ] `C-CF-10` `constraint` A pending refund request has no ledger transaction for the proposed refund. `src: Core features, instruction.md`
- [ ] `C-CF-11` `constraint` A pending refund request leaves the order's financial status unchanged. `src: Core features, instruction.md`
- [ ] `C-CF-12` `data` A pending refund request appends a request entry to the order timeline rather than a refund entry. `src: Core features, instruction.md`
- [ ] `C-CF-13` `literal` A refund of `3411200` against order `#2049` from a `support@example.com` session creates a request. `src: Core features, instruction.md`
- [ ] `C-CF-14` `literal` A refund of `3411200` against order `#2049` from a `finance@example.com` session executes at once. `src: Core features, instruction.md`
- [ ] `C-CF-15` `contract` A `support_agent` session calling the refund endpoint above the ceiling receives a pending request rather than an immediate refund. `src: Core features, instruction.md`
- [ ] `C-CF-16` `contract` A `support_agent` session calling the refund endpoint above the ceiling leaves the order row untouched. `src: Core features, instruction.md`
- [ ] `C-CF-17` `contract` A `support_agent` session calling the approval-decision endpoint directly is rejected by the server as unauthorized. `src: Core features, instruction.md`
- [ ] `C-CF-18` `contract` A rejected decision call from the requester leaves the request pending. `src: Core features, instruction.md`
- [ ] `C-CF-19` `constraint` Every refund attempt carries a client-supplied idempotency key unique per store. `src: Core features, instruction.md`
- [ ] `C-CF-20` `constraint` A repeat refund with the same key returns the original result rather than refunding twice. `src: Core features, instruction.md`
- [ ] `C-CF-21` `constraint` The sum of non-failed refunds for a payment never exceeds the amount captured. `src: Core features, instruction.md`
- [ ] `C-CF-22` `constraint` Two refunds racing for the remaining balance produce one success plus one refusal stating the actual remaining amount. `src: Core features, instruction.md`
- [ ] `C-CF-23` `constraint` A refund that fails at the payment layer stays pending, retrying with a widening gap. `src: Core features, instruction.md`
- [ ] `C-CF-24` `constraint` A failing refund never writes ledger entries speculatively. `src: Core features, instruction.md`
- [ ] `C-CF-25` `role` Restocking is a separate decision from refunding, separately permitted. `src: Core features, instruction.md`
- [ ] `C-CF-26` `capability` A refund may draw on the original payment method, then a gift card or store credit, then a manual method. `src: Core features, instruction.md`
- [ ] `C-CF-27` `ui` The order in which a refund draws on sources is shown before confirmation. `src: Core features, instruction.md`
- [ ] `C-CF-28` `capability` A refund exceeding the store's available balance is permitted, taking the balance negative, raising a debit against the merchant. `src: Core features, instruction.md`
- [ ] `C-CF-29` `data` An approval request carries the proposed action plus the full parameters of the proposed action. `src: Core features, instruction.md`
- [ ] `C-CF-30` `data` An approval request carries the requester, the reason, the permission required to decide. `src: Core features, instruction.md`
- [ ] `C-CF-31` `data` An approval request carries the resolved approver scope, a state, an expiry. `src: Core features, instruction.md`
- [ ] `C-CF-32` `constraint` A pending request's proposed action has no side effect of any kind. `src: Core features, instruction.md`
- [ ] `C-CF-33` `constraint` The approver set resolves from roles plus constraints, never from a named individual. `src: Core features, instruction.md`
- [ ] `C-CF-34` `constraint` The approver set resolves when a request is created, then resolves again when a request is decided. `src: Core features, instruction.md`
- [ ] `C-CF-35` `constraint` The requester never appears in the approver set for the requester's own request. `src: Core features, instruction.md`
- [ ] `C-CF-36` `literal` Request states are `pending`, `approved`, `declined`, `expired`, `executed`. `src: Core features, instruction.md`
- [ ] `C-CF-37` `capability` A request nobody answers lapses at the expiry, notifies, remains auditable as lapsed. `src: Core features, instruction.md`
- [ ] `C-CF-38` `capability` An unanswered request escalates to a wider approver set after an interval, before the expiry. `src: Core features, instruction.md`
- [ ] `C-CF-39` `constraint` On approval the proposed action executes exactly once. `src: Core features, instruction.md`
- [ ] `C-CF-40` `constraint` The request carries the idempotency key the execution uses. `src: Core features, instruction.md`
- [ ] `C-CF-41` `constraint` A double approval, a redelivered queue message, a timed-out downstream call all converge on one effect. `src: Core features, instruction.md`
- [ ] `C-CF-42` `constraint` Two approvers approving at the same instant produce one refund. `src: Core features, instruction.md`
- [ ] `C-CF-43` `constraint` An execution re-validates against the underlying resource, refusing plus naming what changed if the resource moved. `src: Core features, instruction.md`
- [ ] `C-CF-44` `constraint` An approver losing the deciding permission before execution causes refusal, returning the request to pending with a notification. `src: Core features, instruction.md`
- [ ] `C-CF-45` `capability` An approver may delegate to another holder of the same permission for a bounded window, with the delegation recorded. `src: Core features, instruction.md`
- [ ] `C-CF-46` `capability` A refund above ceiling routes through approval. `src: Core features, instruction.md`
- [ ] `C-CF-47` `capability` A discount above ceiling routes through approval. `src: Core features, instruction.md`
- [ ] `C-CF-48` `capability` A business-buyer order above the review threshold routes through approval. `src: Core features, instruction.md`
- [ ] `C-CF-49` `capability` A price change beyond a configured percentage routes through approval. `src: Core features, instruction.md`
- [ ] `C-CF-50` `capability` A bulk operation above a size threshold routes through approval. `src: Core features, instruction.md`
- [ ] `C-CF-51` `capability` A change of payout instrument routes through approval. `src: Core features, instruction.md`
- [ ] `C-CF-52` `capability` Activating an automation containing a money-moving action routes through approval. `src: Core features, instruction.md`
- [ ] `C-CF-53` `data` The request, every notification, every view, the decision, the executing effect, the outcome share one correlation identifier. `src: Core features, instruction.md`
- [ ] `C-CF-54` `capability` At the terminal the same approval object is decided in seconds by a manager code entered on the same device. `src: Core features, instruction.md`
- [ ] `C-CF-55` `constraint` A terminal approving code identifies a person, so a shared override code is refused. `src: Core features, instruction.md`
- [ ] `C-CF-56` `constraint` Terminal approval is unavailable when the device is offline. `src: Core features, instruction.md`
- [ ] `C-CF-57` `contract` Staff sign in through the running identity provider `keycloak` at `AUTH_ISSUER_URL`. `src: Core features, instruction.md`
- [ ] `C-CF-58` `contract` Sign-in uses an authorization-code flow with proof key plus the credentials at `AUTH_CLIENT_ID`, `AUTH_CLIENT_SECRET`. `src: Core features, instruction.md`
- [ ] `C-CF-59` `capability` Signing in authenticates the person; selecting a store authorizes a membership. `src: Core features, instruction.md`
- [ ] `C-CF-60` `contract` The session identifier is opaque, high-entropy, carried in a secure http-only same-site host-only cookie pathed at the root. `src: Core features, instruction.md`
- [ ] `C-CF-61` `contract` The session cookie carries no claim, no role, no store, resolving server-side instead. `src: Core features, instruction.md`
- [ ] `C-CF-62` `constraint` The store context lives on the server session, so no request names the store. `src: Core features, instruction.md`
- [ ] `C-CF-63` `constraint` A store identifier taken from a request parameter is never trusted. `src: Core features, instruction.md`
- [ ] `C-CF-64` `constraint` A password is hashed with a memory-hard function whose parameters are stored beside the record. `src: Core features, instruction.md`
- [ ] `C-CF-65` `literal` A password has a minimum length of `8` with no composition rules. `src: Core features, instruction.md`
- [ ] `C-CF-66` `constraint` A password is checked against a breached-password corpus. `src: Core features, instruction.md`
- [ ] `C-CF-67` `literal` A one-time sign-in link lives `15` minutes, single use. `src: Core features, instruction.md`
- [ ] `C-CF-68` `constraint` A one-time sign-in link is invalidated by use or by a newer link. `src: Core features, instruction.md`
- [ ] `C-CF-69` `constraint` A one-time sign-in link is bound to the requesting browser, so a forwarded link cannot be used elsewhere. `src: Core features, instruction.md`
- [ ] `C-CF-70` `constraint` A second factor is required of any member holding a dangerous permission. `src: Core features, instruction.md`
- [ ] `C-CF-71` `capability` A store administrator may require a second factor of every member. `src: Core features, instruction.md`
- [ ] `C-CF-72` `constraint` Recovery codes are issued once, stored hashed. `src: Core features, instruction.md`
- [ ] `C-CF-73` `literal` A person session idles out after `24` hours, configurable downward. `src: Core features, instruction.md`
- [ ] `C-CF-74` `literal` A person session expires absolutely after `30` days, configurable downward. `src: Core features, instruction.md`
- [ ] `C-CF-75` `literal` A dangerous action requires a fresh authentication within `15` minutes. `src: Core features, instruction.md`
- [ ] `C-CF-76` `constraint` The session identifier rotates on sign-in. `src: Core features, instruction.md`
- [ ] `C-CF-77` `constraint` The session identifier rotates on any privilege change. `src: Core features, instruction.md`
- [ ] `C-CF-78` `capability` Multiple sessions are permitted, individually listable, individually revocable by the person. `src: Core features, instruction.md`
- [ ] `C-CF-79` `capability` A store administrator may revoke a member's individual session. `src: Core features, instruction.md`
- [ ] `C-CF-80` `contract` Signing out revokes the session server-side rather than merely clearing the cookie. `src: Core features, instruction.md`
- [ ] `C-CF-81` `capability` Group claims from the issuer map to roles, per store or across stores. `src: Core features, instruction.md`
- [ ] `C-CF-82` `constraint` A mapped role is authoritative, so editing a mapped role inside the admin is refused. `src: Core features, instruction.md`
- [ ] `C-CF-83` `constraint` Losing a group claim removes the mapped role at the next assertion or the next lifecycle event. `src: Core features, instruction.md`
- [ ] `C-CF-84` `capability` A scheduled comparison reports differences between issuer state, local state, rather than applying differences silently. `src: Core features, instruction.md`
- [ ] `C-CF-85` `literal` Deprovisioning a person at the issuer terminates every session, revokes every token, within `60` seconds. `src: Core features, instruction.md`
- [ ] `C-CF-86` `capability` An organisation may require federated sign-in, refusing password sign-in for members of the organisation. `src: Core features, instruction.md`
- [ ] `C-CF-87` `capability` A small named set of members keeps a local credential for recovery. `src: Core features, instruction.md`
- [ ] `C-CF-88` `constraint` Every break-glass sign-in is logged at the loudest level, notifying every organisation administrator. `src: Core features, instruction.md`
- [ ] `C-CF-89` `constraint` Every assertion is validated for signature, audience, issuer, expiry, not-before, within a configured clock skew. `src: Core features, instruction.md`
- [ ] `C-CF-90` `constraint` Every assertion is single use by assertion identifier, so a repeat is rejected. `src: Core features, instruction.md`
- [ ] `C-CF-91` `constraint` A buyer principal shares no session, no reset, no credential record with a staff principal. `src: Core features, instruction.md`
- [ ] `C-CF-92` `constraint` A sign-up with an existing address produces the same response as one with a new address. `src: Core features, instruction.md`
- [ ] `C-CF-93` `capability` An existing account is notified when somebody signs up with the same address. `src: Core features, instruction.md`
- [ ] `C-CF-94` `data` An organisation holds stores; a store holds locations, markets, channels, memberships. `src: Core features, instruction.md`
- [ ] `C-CF-95` `data` A person holds memberships to stores, separately to organisations. `src: Core features, instruction.md`
- [ ] `C-CF-96` `constraint` An organisation with one store is modelled as four levels rather than as a special case. `src: Core features, instruction.md`
- [ ] `C-CF-97` `constraint` Every tenant-owned query carries a store predicate, so one without a store predicate does not run. `src: Core features, instruction.md`
- [ ] `C-CF-98` `constraint` A connection scoped to one store returns zero rows from another store's tables with the application layer bypassed. `src: Core features, instruction.md`
- [ ] `C-CF-99` `constraint` An organisation administrator is not automatically a member of any store. `src: Core features, instruction.md`
- [ ] `C-CF-100` `constraint` An organisation administrator may not read store data by virtue of the organisation role alone. `src: Core features, instruction.md`
- [ ] `C-CF-101` `capability` An organisation administrator may grant themselves a store membership, logged at the loudest level. `src: Core features, instruction.md`
- [ ] `C-CF-102` `constraint` Creating a store is one transaction creating the default location, the default market, the online-store channel, the owning membership, a theme assignment. `src: Core features, instruction.md`
- [ ] `C-CF-103` `constraint` A store without a location is structurally forbidden. `src: Core features, instruction.md`
- [ ] `C-CF-104` `constraint` A store handle is lowercase kebab, globally unique, immutable after the first order. `src: Core features, instruction.md`
- [ ] `C-CF-105` `constraint` A store currency defaults from the country, changeable only before the first order. `src: Core features, instruction.md`
- [ ] `C-CF-106` `constraint` A store timezone is a named zone rather than an offset. `src: Core features, instruction.md`
- [ ] `C-CF-107` `literal` Store lifecycle states are `trial`, `active`, `past_due`, `frozen`, `paused`, `closed`, `archived`. `src: Core features, instruction.md`
- [ ] `C-CF-108` `constraint` A frozen store's public shop returns a holding page. `src: Core features, instruction.md`
- [ ] `C-CF-109` `constraint` A frozen store's admin stays readable, with billing actionable. `src: Core features, instruction.md`
- [ ] `C-CF-110` `constraint` A frozen store's owner can still read plus export the store's records. `src: Core features, instruction.md`
- [ ] `C-CF-111` `capability` Deletion is a separate explicit delayed operation with a confirmation, a notification to the owner, an audit entry. `src: Core features, instruction.md`
- [ ] `C-CF-112` `constraint` A development store cannot take a live payment. `src: Core features, instruction.md`
- [ ] `C-CF-113` `constraint` A development store cannot message an address that has not opted in. `src: Core features, instruction.md`
- [ ] `C-CF-114` `constraint` A development store cannot install an application holding a live credential. `src: Core features, instruction.md`
- [ ] `C-CF-115` `data` Development store rows are marked as seeded, so a report can exclude them. `src: Core features, instruction.md`
- [ ] `C-CF-116` `constraint` Transferring a development store to a merchant requires fresh consent for every installed application's scopes. `src: Core features, instruction.md`
- [ ] `C-CF-117` `constraint` A cross-store operation names the stores the operation touches, with no implicit all stores. `src: Core features, instruction.md`
- [ ] `C-CF-118` `constraint` Each store in a cross-store scope is authorized independently. `src: Core features, instruction.md`
- [ ] `C-CF-119` `constraint` A store the actor may not read is omitted from a cross-store operation, with the omission reported. `src: Core features, instruction.md`
- [ ] `C-CF-120` `capability` Partial success of a cross-store operation is reported per store. `src: Core features, instruction.md`
- [ ] `C-CF-121` `data` A cross-store operation writes one organisation audit entry plus one per store sharing a correlation identifier. `src: Core features, instruction.md`
- [ ] `C-CF-122` `data` A product is a merchandising object; a variant is the sellable object. `src: Core features, instruction.md`
- [ ] `C-CF-123` `data` Every price, stock-keeping unit, barcode, inventory level belongs to the variant rather than to the product. `src: Core features, instruction.md`
- [ ] `C-CF-124` `literal` A product carries at most `3` options. `src: Core features, instruction.md`
- [ ] `C-CF-125` `constraint` A variant's option value tuple is unique per product. `src: Core features, instruction.md`
- [ ] `C-CF-126` `constraint` A variant's option value tuple has an arity equal to the product's option count, refused by the database otherwise. `src: Core features, instruction.md`
- [ ] `C-CF-127` `literal` A product `status` is `draft`, `active`, or `archived`. `src: Core features, instruction.md`
- [ ] `C-CF-128` `data` Publication per channel is independent of status, optionally at a future instant. `src: Core features, instruction.md`
- [ ] `C-CF-129` `data` Publication per market is independent of publication per channel. `src: Core features, instruction.md`
- [ ] `C-CF-130` `data` Catalog membership is independent of every other publication axis. `src: Core features, instruction.md`
- [ ] `C-CF-131` `constraint` All four publication axes are resolved on every buyer read. `src: Core features, instruction.md`
- [ ] `C-CF-132` `constraint` A variant price is integer minor units plus a currency code. `src: Core features, instruction.md`
- [ ] `C-CF-133` `constraint` A compare-at price must exceed the price wherever a compare-at price is set. `src: Core features, instruction.md`
- [ ] `C-CF-134` `role` A variant cost is optional, separately permitted. `src: Core features, instruction.md`
- [ ] `C-CF-135` `constraint` A converted price is a stored rounded record, so rounding never happens at read time. `src: Core features, instruction.md`
- [ ] `C-CF-136` `capability` A manual collection is an ordered membership list with a position stored per row. `src: Core features, instruction.md`
- [ ] `C-CF-137` `capability` A rule-based collection matches over product fields, tags, price, stock, metafields, with a sort order. `src: Core features, instruction.md`
- [ ] `C-CF-138` `constraint` A rule-based collection is materialised rather than evaluated on read. `src: Core features, instruction.md`
- [ ] `C-CF-139` `data` A rule change enqueues a rebuild; the collection carries the instant of the last successful build. `src: Core features, instruction.md`
- [ ] `C-CF-140` `constraint` An import validates the whole file before writing anything. `src: Core features, instruction.md`
- [ ] `C-CF-141` `constraint` An import with one bad row reports the row plus writes nothing, unless partial mode was chosen explicitly. `src: Core features, instruction.md`
- [ ] `C-CF-142` `constraint` Import rows match on stock-keeping unit or on an external identifier, never on title. `src: Core features, instruction.md`
- [ ] `C-CF-143` `capability` An export runs asynchronously, produces a durable artefact, notifies on completion, expires. `src: Core features, instruction.md`
- [ ] `C-CF-144` `ui` A bulk edit previews before committing, showing the affected count plus a sample. `src: Core features, instruction.md`
- [ ] `C-CF-145` `capability` A bulk edit is one reversible operation for a bounded window recorded as a single audit entry. `src: Core features, instruction.md`
- [ ] `C-CF-146` `constraint` Deleting a product carrying orders is refused; the product archives instead. `src: Core features, instruction.md`
- [ ] `C-CF-147` `constraint` Removing an option value in use is refused with the list of variants that would be orphaned. `src: Core features, instruction.md`
- [ ] `C-CF-148` `capability` A duplicate stock-keeping unit is permitted with a warning, unique only where the merchant opts in. `src: Core features, instruction.md`
- [ ] `C-CF-149` `constraint` A price of zero is permitted; a negative price is refused. `src: Core features, instruction.md`
- [ ] `C-CF-150` `literal` A product is refused above `2000` variants per product, with the option-set explosion named in the message. `src: Core features, instruction.md`
- [ ] `C-CF-151` `constraint` Alternative text is required at publication for the primary media of a published product. `src: Core features, instruction.md`
- [ ] `C-CF-152` `literal` An inventory level carries `on_hand`, `committed`, `reserved`, `incoming`, `damaged`, `quality_control`, `safety_stock`. `src: Core features, instruction.md`
- [ ] `C-CF-153` `constraint` The quantity `available` is derived by subtraction, never a writable column. `src: Core features, instruction.md`
- [ ] `C-CF-154` `data` Every stock change is an append-only movement entry naming item, location, quantity moved, delta, resulting quantity. `src: Core features, instruction.md`
- [ ] `C-CF-155` `literal` A movement reason is one of `sale`, `return`, `restock`, `correction`, `received`, `transfer_out`, `transfer_in`, `damaged`, `theft`, `promotion`, `sample`, `recount`. `src: Core features, instruction.md`
- [ ] `C-CF-156` `data` Every movement entry names the causing object, the actor, an idempotency key where the cause is retryable, a database-assigned instant. `src: Core features, instruction.md`
- [ ] `C-CF-157` `constraint` The current level is a projection of the movement ledger, reconciled on a schedule. `src: Core features, instruction.md`
- [ ] `C-CF-158` `constraint` A discrepancy between projection, ledger raises an alert rather than a silent correction. `src: Core features, instruction.md`
- [ ] `C-CF-159` `constraint` Starting a checkout increases `reserved`. `src: Core features, instruction.md`
- [ ] `C-CF-160` `constraint` A reservation expires, then is released by a sweeper. `src: Core features, instruction.md`
- [ ] `C-CF-161` `constraint` Placing an order decreases `reserved` plus increases `committed` in one transaction. `src: Core features, instruction.md`
- [ ] `C-CF-162` `constraint` Creating a fulfilment decreases `committed` plus decreases `on_hand` in one transaction. `src: Core features, instruction.md`
- [ ] `C-CF-163` `constraint` Cancelling before fulfilment decreases `committed`, leaving `on_hand` untouched. `src: Core features, instruction.md`
- [ ] `C-CF-164` `constraint` Receiving a return increases `on_hand` into the quantity the restock decision names. `src: Core features, instruction.md`
- [ ] `C-CF-165` `literal` A variant `inventory_policy` is `deny` or `continue`. `src: Core features, instruction.md`
- [ ] `C-CF-166` `constraint` Under `deny` the variant is unpurchasable at zero available, checked at cart add, at checkout start, inside the placement transaction. `src: Core features, instruction.md`
- [ ] `C-CF-167` `constraint` Only the check inside the order-placement transaction is authoritative. `src: Core features, instruction.md`
- [ ] `C-CF-168` `capability` Under `continue` the order is created with a backorder flag, holding the fulfilment until stock arrives. `src: Core features, instruction.md`
- [ ] `C-CF-169` `constraint` Two orders for the last unit at the same instant produce exactly one success plus one explicit out-of-stock refusal. `src: Core features, instruction.md`
- [ ] `C-CF-170` `ui` An out-of-stock refusal names the short line plus the shortfall. `src: Core features, instruction.md`
- [ ] `C-CF-171` `constraint` Stock never goes negative through the ordering path. `src: Core features, instruction.md`
- [ ] `C-CF-172` `constraint` A losing placement request leaves no orphaned row, no quantity left committed. `src: Core features, instruction.md`
- [ ] `C-CF-173` `constraint` Deactivating a location holding stock is refused until the stock is transferred or written off. `src: Core features, instruction.md`
- [ ] `C-CF-174` `ui` A refusal to deactivate a location states the quantity still held there. `src: Core features, instruction.md`
- [ ] `C-CF-175` `literal` Transfer states are `draft`, `pending`, `in_transit`, `partially_received`, `received`, `cancelled`. `src: Core features, instruction.md`
- [ ] `C-CF-176` `capability` Receiving a transfer is partial, repeatable, each receipt writing its own movement entries. `src: Core features, instruction.md`
- [ ] `C-CF-177` `capability` Over-receipt is permitted with a warning, recorded as such. `src: Core features, instruction.md`
- [ ] `C-CF-178` `capability` A correction taking `on_hand` negative is permitted, flagged, reported. `src: Core features, instruction.md`
- [ ] `C-CF-179` `constraint` An untracked variant has an undefined `available` rather than zero, remaining always purchasable. `src: Core features, instruction.md`
- [ ] `C-CF-180` `ui` The interface distinguishes a variant that is not tracked from one with none left. `src: Core features, instruction.md`
- [ ] `C-CF-181` `constraint` A terminal, an online store read the same inventory levels, with no separate retail stock table. `src: Core features, instruction.md`
- [ ] `C-CF-182` `capability` A terminal may query another location's availability read-only, raising a transfer request rather than moving stock. `src: Core features, instruction.md`
- [ ] `C-CF-183` `constraint` Stock adjusted at a location outside the actor's constraint is denied. `src: Core features, instruction.md`
- [ ] `C-CF-184` `ui` A location outside the actor's constraint does not appear in the location picker. `src: Core features, instruction.md`
- [ ] `C-CF-185` `literal` Financial status is `pending`, `authorized`, `partially_paid`, `paid`, `partially_refunded`, `refunded`, or `voided`. `src: Core features, instruction.md`
- [ ] `C-CF-186` `literal` Fulfilment status is `unfulfilled`, `partially_fulfilled`, `fulfilled`, `on_hold`, `scheduled`, or `in_progress`. `src: Core features, instruction.md`
- [ ] `C-CF-187` `constraint` Financial status, fulfilment status never collapse into one field. `src: Core features, instruction.md`
- [ ] `C-CF-188` `data` An order line stores its own snapshot of product title, variant title, stock-keeping unit, price, tax lines, discount allocation, mass. `src: Core features, instruction.md`
- [ ] `C-CF-189` `constraint` An order line's variant reference may be absent, so every read path tolerates absence. `src: Core features, instruction.md`
- [ ] `C-CF-190` `data` An order carries a sequential number per store plus an opaque identifier. `src: Core features, instruction.md`
- [ ] `C-CF-191` `data` An order records channel, market, buyer, company where the order is a business order, money in minor units, addresses, attribution, risk level, timestamps. `src: Core features, instruction.md`
- [ ] `C-CF-192` `capability` Staff may edit an order before shipping: add a line, remove an unfulfilled line, change a quantity, add a discount, change shipping. `src: Core features, instruction.md`
- [ ] `C-CF-193` `constraint` An order edit computes a delta; a positive delta requires the buyer's authorization. `src: Core features, instruction.md`
- [ ] `C-CF-194` `constraint` A negative delta from an order edit is a refund, so the ceiling rule applies. `src: Core features, instruction.md`
- [ ] `C-CF-195` `constraint` A quantity change on an order moves `committed` in the same transaction. `src: Core features, instruction.md`
- [ ] `C-CF-196` `constraint` A fulfilled order line is immutable, so removing one is a return. `src: Core features, instruction.md`
- [ ] `C-CF-197` `constraint` Two staff editing one order: the second is refused with a message naming what changed underneath. `src: Core features, instruction.md`
- [ ] `C-CF-198` `constraint` Two simultaneous order edits are never blended together. `src: Core features, instruction.md`
- [ ] `C-CF-199` `capability` A draft order is priced from the buyer's catalog, from the buyer's price list. `src: Core features, instruction.md`
- [ ] `C-CF-200` `capability` A draft order may carry a manual line for something absent from the catalog. `src: Core features, instruction.md`
- [ ] `C-CF-201` `constraint` A draft order reserves nothing until sent for payment. `src: Core features, instruction.md`
- [ ] `C-CF-202` `capability` A draft order expires after a configured window, releasing any reservation. `src: Core features, instruction.md`
- [ ] `C-CF-203` `data` A draft order retains its own identifier after conversion, so the audit chain holds. `src: Core features, instruction.md`
- [ ] `C-CF-204` `ui` The order index carries columns `Order`, `Date`, `Customer`, `Total`, `Payment status`, `Fulfillment status`, `Items`. `src: Core features, instruction.md`
- [ ] `C-CF-205` `capability` Order filters cover status, date range, channel, location, market, tag, risk level, fulfilment location, delivery method, filterable metafields. `src: Core features, instruction.md`
- [ ] `C-CF-206` `constraint` Sorting is offered only on indexed columns. `src: Core features, instruction.md`
- [ ] `C-CF-207` `capability` Selecting across pages selects a query rather than a page, stating the count. `src: Core features, instruction.md`
- [ ] `C-CF-208` `constraint` A bulk action on a selected query re-evaluates the query at execution, reporting the difference. `src: Core features, instruction.md`
- [ ] `C-CF-209` `ui` Five metric tiles read `Orders`, `Ordered items`, `Returned items`, `Fulfilled orders`, `Delivered orders`, each with a period comparison. `src: Core features, instruction.md`
- [ ] `C-CF-210` `literal` The order index period control defaults to `30 days`. `src: Core features, instruction.md`
- [ ] `C-CF-211` `literal` The shipped system views are `All`, `Unfulfilled`, `Unpaid`, `Open`, `Closed`, `Automations`, `Return requests`, `Local Delivery`. `src: Core features, instruction.md`
- [ ] `C-CF-212` `constraint` A system view may be duplicated, never deleted, never renamed. `src: Core features, instruction.md`
- [ ] `C-CF-213` `data` A saved view is a named ordered set of a filter expression, a sort, a column list, a page size. `src: Core features, instruction.md`
- [ ] `C-CF-214` `constraint` A view's filter expression is a structured tree of field, operator, value rather than a raw query string. `src: Core features, instruction.md`
- [ ] `C-CF-215` `literal` A store holds `50` shared views per index; a person holds `50` personal views per index. `src: Core features, instruction.md`
- [ ] `C-CF-216` `ui` Views beyond the visible tab width collapse into a disclosure rather than truncating invisibly. `src: Core features, instruction.md`
- [ ] `C-CF-217` `data` Every order carries an append-only timeline of state changes, payments, refunds, fulfilments, edits, notes, messages, automations, application actions. `src: Core features, instruction.md`
- [ ] `C-CF-218` `data` Every timeline entry records actor, instant, source. `src: Core features, instruction.md`
- [ ] `C-CF-219` `ui` Staff notes, system events are visually distinct, separately filterable. `src: Core features, instruction.md`
- [ ] `C-CF-220` `constraint` The order timeline is a projection of the audit record rather than a second write path. `src: Core features, instruction.md`
- [ ] `C-CF-221` `constraint` A duplicate submission from a channel is deduplicated on that channel's own order identifier. `src: Core features, instruction.md`
- [ ] `C-CF-222` `capability` An order arriving for an archived product is accepted, because the line snapshot carries everything needed. `src: Core features, instruction.md`
- [ ] `C-CF-223` `capability` Cancellation after partial fulfilment is permitted for the unfulfilled remainder only. `src: Core features, instruction.md`
- [ ] `C-CF-224` `constraint` Payment captured with fulfilment permanently failed leaves the order open, proposing a refund. `src: Core features, instruction.md`
- [ ] `C-CF-225` `constraint` Every movement of value is one balanced transaction of two or more entries. `src: Core features, instruction.md`
- [ ] `C-CF-226` `constraint` A ledger transaction sums to zero per currency, refused by the database otherwise. `src: Core features, instruction.md`
- [ ] `C-CF-227` `constraint` A ledger entry is never updated, never deleted; a correction is a reversing transaction. `src: Core features, instruction.md`
- [ ] `C-CF-228` `constraint` The ledger is the source of truth for every money figure shown anywhere. `src: Core features, instruction.md`
- [ ] `C-CF-229` `constraint` A money figure is never computed by adding up orders. `src: Core features, instruction.md`
- [ ] `C-CF-230` `literal` Balance kinds are `available`, `pending`, `reserved`, `disputed`, `fee`, `tax`, `rounding`, `in_transit`, `gift_card_liability`, `store_credit_liability`. `src: Core features, instruction.md`
- [ ] `C-CF-231` `literal` Payment states are `created`, `requires_action`, `authorized`, `captured`, `failed`, `voided`, `refunded`, `partially_refunded`, `disputed`. `src: Core features, instruction.md`
- [ ] `C-CF-232` `data` Authorization expiry is stored on the payment per method, per country. `src: Core features, instruction.md`
- [ ] `C-CF-233` `constraint` An expiring authorization enqueues a capture or a void rather than lapsing without a record. `src: Core features, instruction.md`
- [ ] `C-CF-234` `capability` A card payment stores a token plus brand plus last four plus expiry, preferring a network token. `src: Core features, instruction.md`
- [ ] `C-CF-235` `constraint` A wallet payment delivers a token, so the platform never receives a card number. `src: Core features, instruction.md`
- [ ] `C-CF-236` `capability` A bank-redirect payment creates a `pending` order settling on a signature-verified idempotent callback. `src: Core features, instruction.md`
- [ ] `C-CF-237` `ui` A unified-payments-interface collect request renders an honest pending state rather than a spinner. `src: Core features, instruction.md`
- [ ] `C-CF-238` `capability` An instalment provider decides at checkout; the merchant is paid in full. `src: Core features, instruction.md`
- [ ] `C-CF-239` `capability` A bank-debit mandate is stored, referenced by later charges, revocable within one business day. `src: Core features, instruction.md`
- [ ] `C-CF-240` `capability` Cash on delivery creates a `pending` order under a configured fulfilment hold. `src: Core features, instruction.md`
- [ ] `C-CF-241` `constraint` A gift card or store credit balance decrements only on successful capture. `src: Core features, instruction.md`
- [ ] `C-CF-242` `role` A manual or offline payment is recorded with a method label plus a reference by a member holding the permission. `src: Core features, instruction.md`
- [ ] `C-CF-243` `constraint` Storing a payment instrument requires explicit buyer consent recorded with text, version. `src: Core features, instruction.md`
- [ ] `C-CF-244` `constraint` A stored instrument keeps a token only, with brand, last four, expiry as the display remnant. `src: Core features, instruction.md`
- [ ] `C-CF-245` `capability` A stored instrument is usable at checkout, on a draft order, when paying an invoice, each separately authorized. `src: Core features, instruction.md`
- [ ] `C-CF-246` `capability` Removing a stored instrument cancels any scheduled charge against the instrument, notifying the merchant. `src: Core features, instruction.md`
- [ ] `C-CF-247` `literal` Dispute states are `opened`, `evidence_due`, `submitted`, `won`, `lost`, `expired`. `src: Core features, instruction.md`
- [ ] `C-CF-248` `constraint` Funds move to the `disputed` balance the moment a dispute opens. `src: Core features, instruction.md`
- [ ] `C-CF-249` `capability` Dispute evidence is stored field by field, saved continuously. `src: Core features, instruction.md`
- [ ] `C-CF-250` `capability` A dispute deadline drives notifications at decreasing intervals. `src: Core features, instruction.md`
- [ ] `C-CF-251` `data` The platform fee rate comes from the store's plan entitlement, versioned so a historical order is rated at the rate then in force. `src: Core features, instruction.md`
- [ ] `C-CF-252` `data` The platform fee is computed on the order total at order creation, stored on the order, accrued to the `fee` balance. `src: Core features, instruction.md`
- [ ] `C-CF-253` `ui` The platform fee is itemised per order in the merchant's finance surface. `src: Core features, instruction.md`
- [ ] `C-CF-254` `ui` A merchant using the built-in processor sees a statement of no fee rather than a zero line. `src: Core features, instruction.md`
- [ ] `C-CF-255` `capability` The merchant's own subscription bills monthly or annually per the plan. `src: Core features, instruction.md`
- [ ] `C-CF-256` `constraint` An upgrade prorates immediately; a downgrade takes effect at the period boundary with the interface saying when. `src: Core features, instruction.md`
- [ ] `C-CF-257` `constraint` An invoice number is allocated from a per-store sequence inside the finalisation transaction. `src: Core features, instruction.md`
- [ ] `C-CF-258` `literal` Dunning notifies on the due instant, at `3` days, at `7` days with `past_due`, at `14` days with a final notice, at `21` days with `frozen`. `src: Core features, instruction.md`
- [ ] `C-CF-259` `constraint` No data is deleted at any dunning step. `src: Core features, instruction.md`
- [ ] `C-CF-260` `constraint` Capability suspension in `past_due` never includes reading or exporting the merchant's own data. `src: Core features, instruction.md`
- [ ] `C-CF-261` `capability` Risk is rated per payment before authorization where the method allows, producing a rating, a level, a signal list. `src: Core features, instruction.md`
- [ ] `C-CF-262` `capability` A merchant configures risk handling as allow, review, or cancel. `src: Core features, instruction.md`
- [ ] `C-CF-263` `ui` A merchant sees the risk level plus the signals rather than a raw model output. `src: Core features, instruction.md`
- [ ] `C-CF-264` `capability` A member holding the permission may manually accept a cancelled order, recorded against the model's feedback. `src: Core features, instruction.md`
- [ ] `C-CF-265` `constraint` A risk review queue holds the authorization, storing the authorization expiry so nothing lapses silently. `src: Core features, instruction.md`
- [ ] `C-CF-266` `data` A payout is a set of ledger transactions joined through a payout item table. `src: Core features, instruction.md`
- [ ] `C-CF-267` `capability` A payout schedule is daily, weekly, or monthly with a cutoff in the store's timezone. `src: Core features, instruction.md`
- [ ] `C-CF-268` `constraint` A settlement instrument is versioned rather than edited, so a payout names the instrument in force at its cutoff. `src: Core features, instruction.md`
- [ ] `C-CF-269` `constraint` A new settlement instrument requires verification plus a hold period. `src: Core features, instruction.md`
- [ ] `C-CF-270` `constraint` A failed payout returns funds to `available` with a failure code, notifying, without retrying until re-verification. `src: Core features, instruction.md`
- [ ] `C-CF-271` `capability` A payout statement is downloadable, itemised, matching the ledger exactly. `src: Core features, instruction.md`
- [ ] `C-CF-272` `data` Presentment amounts, settlement amounts are both stored with the rate plus the rate's timestamp. `src: Core features, instruction.md`
- [ ] `C-CF-273` `constraint` A rounding remainder goes to a dedicated balance rather than being absorbed silently. `src: Core features, instruction.md`
- [ ] `C-CF-274` `constraint` Capture after the authorization expired is refused with a specific error. `src: Core features, instruction.md`
- [ ] `C-CF-275` `data` A fulfilment order sits between the order, the shipments, each with its own lifecycle, assignee, permissions. `src: Core features, instruction.md`
- [ ] `C-CF-276` `capability` Routing is an ordered list of rules run top to bottom, each rule filtering the output of the previous rule. `src: Core features, instruction.md`
- [ ] `C-CF-277` `constraint` A routing rule that would empty the candidate set is skipped, with the skip recorded. `src: Core features, instruction.md`
- [ ] `C-CF-278` `capability` Routing rule types cover minimise splits, ranked preference, proximity, stock sufficiency, capability match, capacity, blackout. `src: Core features, instruction.md`
- [ ] `C-CF-279` `constraint` Routing is deterministic: the same inputs always produce the same assignment. `src: Core features, instruction.md`
- [ ] `C-CF-280` `constraint` A routing tie breaks on a stated key rather than on database ordering. `src: Core features, instruction.md`
- [ ] `C-CF-281` `data` Every fulfilment order records the rule trace that produced its assignment. `src: Core features, instruction.md`
- [ ] `C-CF-282` `constraint` Routing runs once at order creation, again on demand when a human reassigns. `src: Core features, instruction.md`
- [ ] `C-CF-283` `capability` A fulfilment service registers a callback, declaring the locations the service covers. `src: Core features, instruction.md`
- [ ] `C-CF-284` `capability` A fulfilment request is accepted or rejected with a reason by the service. `src: Core features, instruction.md`
- [ ] `C-CF-285` `constraint` A fulfilment request with no response inside a stated window escalates to the merchant. `src: Core features, instruction.md`
- [ ] `C-CF-286` `constraint` A fulfilment cancellation is a request the service may refuse once the parcel has left. `src: Core features, instruction.md`
- [ ] `C-CF-287` `constraint` Tracking pushed by a service is validated, deduplicated by tracking number. `src: Core features, instruction.md`
- [ ] `C-CF-288` `constraint` Buying a label debits the merchant plus writes ledger entries. `src: Core features, instruction.md`
- [ ] `C-CF-289` `constraint` Voiding a label inside the carrier's window writes a reversing transaction. `src: Core features, instruction.md`
- [ ] `C-CF-290` `constraint` A label purchase that debits without producing a label reverses automatically, then reports. `src: Core features, instruction.md`
- [ ] `C-CF-291` `capability` The order status page is public, addressed by a signed token, showing state, tracking, a delivery estimate, the merchant's branding. `src: Core features, instruction.md`
- [ ] `C-CF-292` `constraint` Carrier events are normalised to a common vocabulary, so a raw carrier code is never shown to a buyer. `src: Core features, instruction.md`
- [ ] `C-CF-293` `capability` A delivery exception surfaces to the merchant as a task rather than only to the buyer as a message. `src: Core features, instruction.md`
- [ ] `C-CF-294` `capability` Local delivery is per location with zones, a rate, a minimum order, a delivery window. `src: Core features, instruction.md`
- [ ] `C-CF-295` `capability` Pickup is per location with an enabled flag, instructions, preparation time, per-line availability. `src: Core features, instruction.md`
- [ ] `C-CF-296` `literal` Pickup adds the fulfilment states `ready_for_pickup`, `picked_up`, each with its own notification. `src: Core features, instruction.md`
- [ ] `C-CF-297` `capability` A pickup order appears on that location's terminal as a task. `src: Core features, instruction.md`
- [ ] `C-CF-298` `literal` Hold reasons cover risk review, payment pending, business-buyer order review, an automation, a manual hold, backorder. `src: Core features, instruction.md`
- [ ] `C-CF-299` `ui` Every hold carries its reason plus the member who set the hold, visible, filterable. `src: Core features, instruction.md`
- [ ] `C-CF-300` `role` Releasing a hold requires its own permission, audited. `src: Core features, instruction.md`
- [ ] `C-CF-301` `capability` An order routed to a location that goes offline offers reassignment as a task rather than moving silently. `src: Core features, instruction.md`
- [ ] `C-CF-302` `capability` A fulfilment service reporting a shipment for a cancelled order reopens the order with a note, tasking a human. `src: Core features, instruction.md`
- [ ] `C-CF-303` `literal` Return states are `requested`, `approved`, `declined`, `label_issued`, `in_transit`, `received`, `inspected`, `resolved`, `cancelled`, `expired`. `src: Core features, instruction.md`
- [ ] `C-CF-304` `constraint` Return eligibility is computed from the order's own delivery instant rather than from its creation instant. `src: Core features, instruction.md`
- [ ] `C-CF-305` `capability` A buyer selects lines, quantities on the order status page to open a return. `src: Core features, instruction.md`
- [ ] `C-CF-306` `constraint` Return eligibility runs against the merchant's policy, per-product exclusions, a final-sale flag. `src: Core features, instruction.md`
- [ ] `C-CF-307` `capability` A return reason comes from the merchant's list with an optional note, a photograph where required. `src: Core features, instruction.md`
- [ ] `C-CF-308` `capability` A return request is auto-approved or queued for staff per the merchant's policy. `src: Core features, instruction.md`
- [ ] `C-CF-309` `capability` On approval a return label is issued or return instructions are shown. `src: Core features, instruction.md`
- [ ] `C-CF-310` `capability` On receipt staff record the condition plus a restock decision. `src: Core features, instruction.md`
- [ ] `C-CF-311` `literal` Restock decisions are `restock_sellable`, `restock_damaged`, `restock_quality_control`, `do_not_restock`. `src: Core features, instruction.md`
- [ ] `C-CF-312` `data` An exchange is a return plus a new linked order, never an edit of the original. `src: Core features, instruction.md`
- [ ] `C-CF-313` `constraint` An exchange delta is charged, refunded, or issued as store credit per the merchant's policy. `src: Core features, instruction.md`
- [ ] `C-CF-314` `constraint` An unavailable replacement offers the buyer alternatives or a refund, never becoming a refund silently. `src: Core features, instruction.md`
- [ ] `C-CF-315` `constraint` A return requested for a line already returned is refused with the prior return referenced. `src: Core features, instruction.md`
- [ ] `C-CF-316` `constraint` A buyer returning more than the ordered quantity is refused at line level. `src: Core features, instruction.md`
- [ ] `C-CF-317` `constraint` A refund on a discounted line uses the discount allocation stored on the line rather than the list price. `src: Core features, instruction.md`
- [ ] `C-CF-318` `capability` A return received without a request is recorded as an unmatched receipt at the location, surfaced as a task. `src: Core features, instruction.md`
- [ ] `C-CF-319` `data` A customer carries identity, consent state per channel, addresses with one default, derived commerce aggregates, tax exemptions, company links. `src: Core features, instruction.md`
- [ ] `C-CF-320` `constraint` A customer's personal fields sit behind their own permission, redacted at the serialisation boundary. `src: Core features, instruction.md`
- [ ] `C-CF-321` `capability` A segment is a stored expression over customer fields, order aggregates, product affinity, location, tags, consent state, metafields. `src: Core features, instruction.md`
- [ ] `C-CF-322` `capability` A segment materialises on a schedule, on demand, showing its last-evaluated instant. `src: Core features, instruction.md`
- [ ] `C-CF-323` `ui` A segment's size is reported before use; a segment below a floor is flagged when used for messaging. `src: Core features, instruction.md`
- [ ] `C-CF-324` `constraint` Messaging a segment intersects the segment with consent state at send time rather than at definition time. `src: Core features, instruction.md`
- [ ] `C-CF-325` `data` A company carries a name, an external identifier, tax registrations, default payment terms, assigned catalogs, an assigned representative set. `src: Core features, instruction.md`
- [ ] `C-CF-326` `data` A company location carries its own addresses, its own tax registration, overrides for payment terms, catalog, buyer experience. `src: Core features, instruction.md`
- [ ] `C-CF-327` `data` A company contact names a customer, the locations the contact may order for, a spending limit, whether ordering or drafting only is permitted. `src: Core features, instruction.md`
- [ ] `C-CF-328` `data` A representative assignment links a membership to a company with a granting actor, a granting instant, an optional expiry. `src: Core features, instruction.md`
- [ ] `C-CF-329` `constraint` A representative assignment restricts company, order, quote, price-list reads to assigned companies. `src: Core features, instruction.md`
- [ ] `C-CF-330` `capability` A representative may draft an order on behalf of a contact, recording representative, buyer contact as separate actors. `src: Core features, instruction.md`
- [ ] `C-CF-331` `constraint` Reassigning a company transfers future access without retroactively hiding history, recording the transfer in the audit. `src: Core features, instruction.md`
- [ ] `C-CF-332` `ui` A representative with no assignments sees an empty state naming who assigns companies rather than an error. `src: Core features, instruction.md`
- [ ] `C-CF-333` `constraint` One assignment table plus one predicate builder serve company assignment, location assignment for fulfilment, location assignment for retail. `src: Core features, instruction.md`
- [ ] `C-CF-334` `literal` Quantity rules are a `minimum`, a `maximum`, an `increment`, per variant per catalog. `src: Core features, instruction.md`
- [ ] `C-CF-335` `constraint` Quantity rules are enforced at the storefront control, at the cart, at the checkout, at the draft-order builder, inside the placement transaction. `src: Core features, instruction.md`
- [ ] `C-CF-336` `ui` A quantity refusal names the rule that applies rather than reporting an invalid quantity. `src: Core features, instruction.md`
- [ ] `C-CF-337` `capability` A variant matrix on the product page shows the first option against the second with a quantity field per cell. `src: Core features, instruction.md`
- [ ] `C-CF-338` `capability` A separate order form lists the whole catalog with quantity fields, searchable, filterable, paginated, with the running total pinned. `src: Core features, instruction.md`
- [ ] `C-CF-339` `capability` A delimited upload of stock-keeping units plus quantities is validated whole, reporting unmatched rows before anything is added. `src: Core features, instruction.md`
- [ ] `C-CF-340` `constraint` A variant matrix of a thousand cells stays responsive. `src: Core features, instruction.md`
- [ ] `C-CF-341` `capability` A buyer portal carries order history, reorder, quotes, invoices with payment, addresses, contacts, the company's price list. `src: Core features, instruction.md`
- [ ] `C-CF-342` `capability` A merchant defines buyer roles within a company covering ordering, drafting, paying invoices, managing contacts. `src: Core features, instruction.md`
- [ ] `C-CF-343` `constraint` A buyer role is evaluated by the same policy component as staff, against a buyer principal. `src: Core features, instruction.md`
- [ ] `C-CF-344` `constraint` A buyer role granting more than the merchant's own staff role is refused by the escalation guard. `src: Core features, instruction.md`
- [ ] `C-CF-345` `capability` Payment terms are net windows or due on receipt, per company, overridable per company location. `src: Core features, instruction.md`
- [ ] `C-CF-346` `capability` A deposit is a percentage or a fixed amount taken at checkout, leaving the order `partially_paid` with the balance invoiced. `src: Core features, instruction.md`
- [ ] `C-CF-347` `capability` An order review gate decides which orders need staff approval before fulfilment. `src: Core features, instruction.md`
- [ ] `C-CF-348` `data` Review-gate inputs are the total, the company, the contact, whether the order is a first order, the credit exposure, any metafield. `src: Core features, instruction.md`
- [ ] `C-CF-349` `constraint` A gated order is created, stock is committed, the fulfilment order is held with a business-review reason. `src: Core features, instruction.md`
- [ ] `C-CF-350` `data` A review decision records the deciding member, the instant, notifying the buyer. `src: Core features, instruction.md`
- [ ] `C-CF-351` `data` Credit exposure is the outstanding invoiced amount per company computed from the ledger. `src: Core features, instruction.md`
- [ ] `C-CF-352` `constraint` Exceeding a per-company credit limit triggers review regardless of other rules. `src: Core features, instruction.md`
- [ ] `C-CF-353` `constraint` Reducing a credit limit below current exposure gates new orders, leaving existing orders alone. `src: Core features, instruction.md`
- [ ] `C-CF-354` `capability` A tax number per company per jurisdiction is validated against that jurisdiction's service where one exists. `src: Core features, instruction.md`
- [ ] `C-CF-355` `data` A tax validation response plus its instant are stored. `src: Core features, instruction.md`
- [ ] `C-CF-356` `capability` A validated registration may zero-rate or reverse-charge per that jurisdiction's rules. `src: Core features, instruction.md`
- [ ] `C-CF-357` `constraint` A compliant invoice is generated at finalisation, numbered sequentially per store per jurisdiction, stored immutably. `src: Core features, instruction.md`
- [ ] `C-CF-358` `constraint` A tax validation outage marks the registration unvalidated, applying standard tax, tasking the merchant. `src: Core features, instruction.md`
- [ ] `C-CF-359` `capability` A contact belonging to two companies is permitted, with the ordering context selected explicitly, shown at all times. `src: Core features, instruction.md`
- [ ] `C-CF-360` `constraint` Deleting a company with open orders is refused; the company archives. `src: Core features, instruction.md`
- [ ] `C-CF-361` `constraint` A quote holds its terms until expiry even where quantity rules change; a reorder is validated afresh. `src: Core features, instruction.md`
- [ ] `C-CF-362` `literal` A market has type `region`, `b2b`, or `retail`. `src: Core features, instruction.md`
- [ ] `C-CF-363` `literal` A market has state `draft`, `active`, or `inactive`. `src: Core features, instruction.md`
- [ ] `C-CF-364` `data` A market carries membership, a currency with a rounding rule, published languages with one primary, a domain or prefix, a catalog, a tax treatment, an optional theme override. `src: Core features, instruction.md`
- [ ] `C-CF-365` `constraint` A market setting resolves from the market, then the parent chain, then the store default, first explicit value winning. `src: Core features, instruction.md`
- [ ] `C-CF-366` `ui` The interface shows for every market setting whether the value is set here or inherited, naming the source. `src: Core features, instruction.md`
- [ ] `C-CF-367` `literal` A market inheritance chain is bounded at `4` levels, refused deeper. `src: Core features, instruction.md`
- [ ] `C-CF-368` `constraint` A market parent reference is validated against the ancestor set on write, so a cycle is impossible. `src: Core features, instruction.md`
- [ ] `C-CF-369` `capability` A catalog is a product set plus a price list, assignable to a market or to companies. `src: Core features, instruction.md`
- [ ] `C-CF-370` `constraint` Creating a catalog beyond the plan's cap is refused with the cap plus the plan named. `src: Core features, instruction.md`
- [ ] `C-CF-371` `capability` A price list carries a percentage adjustment, per-variant fixed overrides, per-variant volume breaks. `src: Core features, instruction.md`
- [ ] `C-CF-372` `constraint` A per-variant fixed override beats the percentage adjustment. `src: Core features, instruction.md`
- [ ] `C-CF-373` `constraint` Price resolution order is company catalog, then market catalog, then store price, first match winning. `src: Core features, instruction.md`
- [ ] `C-CF-374` `data` The price resolution is recorded on the order line, so a price can be explained afterwards. `src: Core features, instruction.md`
- [ ] `C-CF-375` `constraint` Price resolution is one function used by storefront, cart, checkout, draft-order builder, machine interface, terminal. `src: Core features, instruction.md`
- [ ] `C-CF-376` `capability` A view-as control pairs a country with a channel, rendering the buyer surface as that market's buyer would see. `src: Core features, instruction.md`
- [ ] `C-CF-377` `constraint` A view-as preview uses the same resolution path as a real request. `src: Core features, instruction.md`
- [ ] `C-CF-378` `constraint` A view-as preview never writes; carts created in preview are marked, excluded from analytics. `src: Core features, instruction.md`
- [ ] `C-CF-379` `capability` A market may own a hostname, a subdomain, or a path prefix. `src: Core features, instruction.md`
- [ ] `C-CF-380` `constraint` Negotiation on the primary domain with no prefix redirects rather than varying a cached body. `src: Core features, instruction.md`
- [ ] `C-CF-381` `constraint` Every rendered route emits a canonical link plus one alternate per published market per language. `src: Core features, instruction.md`
- [ ] `C-CF-382` `constraint` Changing a market's domain issues permanent redirects from the old form for a stated minimum period. `src: Core features, instruction.md`
- [ ] `C-CF-383` `constraint` A country belongs to at most one region market per store, refused at write time otherwise. `src: Core features, instruction.md`
- [ ] `C-CF-384` `capability` A buyer whose country is in no market falls back to the store's primary market, warning the merchant. `src: Core features, instruction.md`
- [ ] `C-CF-385` `constraint` A price-list entry whose variant no longer exists is retained, marked orphaned. `src: Core features, instruction.md`
- [ ] `C-CF-386` `constraint` Two markets claiming one domain is refused. `src: Core features, instruction.md`
- [ ] `C-CF-387` `constraint` Deleting a parent market that still has children is refused. `src: Core features, instruction.md`
- [ ] `C-CF-388` `capability` Discount kinds cover order percentage, order fixed, product percentage or fixed, buy-X-get-Y, free shipping, automatic, code-based. `src: Core features, instruction.md`
- [ ] `C-CF-389` `capability` Discount conditions cover minimum subtotal, minimum quantity, segment, company, market, channel, first order only, product or collection membership, a date window. `src: Core features, instruction.md`
- [ ] `C-CF-390` `constraint` Discount conditions compose with an explicit conjunction, with no implicit remainder. `src: Core features, instruction.md`
- [ ] `C-CF-391` `constraint` A discount is allocated across the lines the discount applies to, stored on each line. `src: Core features, instruction.md`
- [ ] `C-CF-392` `constraint` A discount allocation sums exactly to the discount amount. `src: Core features, instruction.md`
- [ ] `C-CF-393` `constraint` A residual smallest unit of a discount allocation goes to a stated line by a stated rule. `src: Core features, instruction.md`
- [ ] `C-CF-394` `constraint` Taxes recompute after discount allocation. `src: Core features, instruction.md`
- [ ] `C-CF-395` `constraint` Product discounts apply first, then order discounts, then shipping discounts. `src: Core features, instruction.md`
- [ ] `C-CF-396` `constraint` A promotional discount stacks on top of a price-list price rather than replacing one. `src: Core features, instruction.md`
- [ ] `C-CF-397` `constraint` A staff-created discount above the actor's discount ceiling becomes an approval request. `src: Core features, instruction.md`
- [ ] `C-CF-398` `constraint` Where two discounts of one class match without combining, the larger buyer benefit wins, with the choice recorded. `src: Core features, instruction.md`
- [ ] `C-CF-399` `constraint` A single-use code survives a thousand simultaneous attempts with exactly one redemption. `src: Core features, instruction.md`
- [ ] `C-CF-400` `ui` A losing attempt on an exhausted code receives an explicit exhausted message. `src: Core features, instruction.md`
- [ ] `C-CF-401` `constraint` A per-customer discount limit is enforced against the customer identity where one exists, against the checkout otherwise. `src: Core features, instruction.md`
- [ ] `C-CF-402` `capability` Bulk codes are generated asynchronously in batches with a stated ceiling per batch. `src: Core features, instruction.md`
- [ ] `C-CF-403` `constraint` A code not chosen by a human is high-entropy; code validation is rate-limited per network prefix. `src: Core features, instruction.md`
- [ ] `C-CF-404` `data` A gift card is a code, a balance, a currency, an expiry where permitted, an issuing source. `src: Core features, instruction.md`
- [ ] `C-CF-405` `constraint` Issuing a gift card is a ledger transaction against a liability balance rather than a row update. `src: Core features, instruction.md`
- [ ] `C-CF-406` `constraint` A gift card expiry writes a transaction releasing the liability rather than zeroing a column. `src: Core features, instruction.md`
- [ ] `C-CF-407` `constraint` A gift card code is stored hashed with a display remnant, with lookup rate-limited. `src: Core features, instruction.md`
- [ ] `C-CF-408` `constraint` Store credit uses the same mechanism as a gift card with its own liability balance, no transferable code. `src: Core features, instruction.md`
- [ ] `C-CF-409` `ui` A discount removed because the cart fell below a condition tells the buyer which condition failed. `src: Core features, instruction.md`
- [ ] `C-CF-410` `constraint` Checkout is served from its own prefix, rendering no merchant-authored template. `src: Core features, instruction.md`
- [ ] `C-CF-411` `constraint` Checkout runs no merchant-supplied code, no application-supplied code beside a payment field. `src: Core features, instruction.md`
- [ ] `C-CF-412` `constraint` Checkout reads a cart snapshot rather than a live theme. `src: Core features, instruction.md`
- [ ] `C-CF-413` `data` A checkout session carries an immutable line snapshot plus a mutable buyer section. `src: Core features, instruction.md`
- [ ] `C-CF-414` `constraint` A checkout token is treated as a credential: not logged, not leaked in a referrer, expired aggressively. `src: Core features, instruction.md`
- [ ] `C-CF-415` `literal` A checkout session idles out after `1` hour, expiring absolutely after `24`, both releasing reservations. `src: Core features, instruction.md`
- [ ] `C-CF-416` `capability` An abandoned checkout is recoverable by a signed single-use link valid for a configured window. `src: Core features, instruction.md`
- [ ] `C-CF-417` `constraint` A checkout currency is fixed at creation from the market, never changing mid-checkout. `src: Core features, instruction.md`
- [ ] `C-CF-418` `capability` Checkout steps are express, contact, delivery, delivery method, payment, then review where required. `src: Core features, instruction.md`
- [ ] `C-CF-419` `constraint` Which address fields exist, which are required, their labels, their order, their validation are per-country data. `src: Core features, instruction.md`
- [ ] `C-CF-420` `literal` India renders `Province` with its state list plus a six-digit postal code. `src: Core features, instruction.md`
- [ ] `C-CF-421` `constraint` Every address field carries the correct autofill token. `src: Core features, instruction.md`
- [ ] `C-CF-422` `constraint` Address autocomplete never overwrites a field the buyer has edited, remaining dismissible. `src: Core features, instruction.md`
- [ ] `C-CF-423` `constraint` An unavailable address suggestion service leaves the form working as a plain form. `src: Core features, instruction.md`
- [ ] `C-CF-424` `ui` A reservation that cannot be taken tells the buyer which line is short, by how much, offering the available quantity. `src: Core features, instruction.md`
- [ ] `C-CF-425` `capability` Delivery options are merchant rate table, carrier rates where entitled, pickup, local delivery. `src: Core features, instruction.md`
- [ ] `C-CF-426` `constraint` A carrier timeout falls back to the merchant's rate table rather than to no options. `src: Core features, instruction.md`
- [ ] `C-CF-427` `constraint` The payment method set resolves from market, buyer country, currency, amount, merchant configuration, in that order. `src: Core features, instruction.md`
- [ ] `C-CF-428` `ui` Payment methods are grouped as express wallets, cards, bank redirects, instalments, buy-now-pay-later, gift card or store credit, offline. `src: Core features, instruction.md`
- [ ] `C-CF-429` `constraint` Card fields render inside an isolated frame served by the payment layer. `src: Core features, instruction.md`
- [ ] `C-CF-430` `constraint` The page surrounding a card field never reads the card field. `src: Core features, instruction.md`
- [ ] `C-CF-431` `constraint` Every payment attempt carries an idempotency key, so a double submit yields one charge. `src: Core features, instruction.md`
- [ ] `C-CF-432` `literal` The checkout summary line reads `Estimated taxes` until the order is placed. `src: Core features, instruction.md`
- [ ] `C-CF-433` `constraint` A tax service timeout falls back to the merchant's own rates, flagging the order for review, never to zero. `src: Core features, instruction.md`
- [ ] `C-CF-434` `capability` Checkout branding from a constrained token set is available on every plan. `src: Core features, instruction.md`
- [ ] `C-CF-435` `role` Declared checkout extension components are a top-plan capability, sandboxed, with no access to payment fields. `src: Core features, instruction.md`
- [ ] `C-CF-436` `constraint` No extension may delay the checkout submit path beyond its budget or prevent order placement. `src: Core features, instruction.md`
- [ ] `C-CF-437` `constraint` An extension exceeding its budget is disabled for that session, with the session continuing. `src: Core features, instruction.md`
- [ ] `C-CF-438` `constraint` A payment that succeeded where order creation failed is automatically voided or refunded, telling the buyer. `src: Core features, instruction.md`
- [ ] `C-CF-439` `constraint` A reconciliation sweep finds any payment-without-order case that slipped through. `src: Core features, instruction.md`
- [ ] `C-CF-440` `capability` A buyer returning to a completed checkout gets the order status page, because a checkout is not replayable. `src: Core features, instruction.md`
- [ ] `C-CF-441` `ui` An invalid discount at checkout names its reason as expired, limit reached, not applicable, or minimum not met. `src: Core features, instruction.md`
- [ ] `C-CF-442` `constraint` A gift card partly covering a total charges the remainder elsewhere, decrementing only on successful capture of the whole. `src: Core features, instruction.md`
- [ ] `C-CF-443` `capability` A checkout session expiring mid-payment returns the buyer to a recoverable state with the cart intact. `src: Core features, instruction.md`
- [ ] `C-CF-444` `constraint` The whole checkout works as a sequence of plain form submissions with client scripting unavailable. `src: Core features, instruction.md`
- [ ] `C-CF-445` `data` A template is a page kind plus an ordered section list with per-section settings. `src: Core features, instruction.md`
- [ ] `C-CF-446` `data` A section declares its settings plus its permitted block types; a block is a typed ordered child. `src: Core features, instruction.md`
- [ ] `C-CF-447` `literal` A theme role is `main`, `unpublished`, or `development`. `src: Core features, instruction.md`
- [ ] `C-CF-448` `ui` The theme editor is two panes: an outline tree, a live preview, each selection mirroring the other. `src: Core features, instruction.md`
- [ ] `C-CF-449` `constraint` Theme reordering has a keyboard equivalent as move-up, move-down commands with announcements. `src: Core features, instruction.md`
- [ ] `C-CF-450` `constraint` The theme preview renders through the real storefront pipeline with unsaved changes applied. `src: Core features, instruction.md`
- [ ] `C-CF-451` `constraint` Theme changes stage, then publish as one version, so no partial live state exists. `src: Core features, instruction.md`
- [ ] `C-CF-452` `data` Every theme publish creates a restorable version with an actor plus an instant. `src: Core features, instruction.md`
- [ ] `C-CF-453` `constraint` A second theme editor is warned, may take over, locking out the first with a message. `src: Core features, instruction.md`
- [ ] `C-CF-454` `capability` A shareable expiring theme preview link needs no admin session, carries no admin capability, is excluded from indexing. `src: Core features, instruction.md`
- [ ] `C-CF-455` `capability` Content beyond the theme covers pages, blogs with moderated comments, menus, metaobjects, files, redirects. `src: Core features, instruction.md`
- [ ] `C-CF-456` `constraint` The rendering pipeline resolves store, market, then route, then authorizes publication, then resolves prices, then renders on the server. `src: Core features, instruction.md`
- [ ] `C-CF-457` `constraint` A rendered storefront document caches per market, per language, per currency, per publication state. `src: Core features, instruction.md`
- [ ] `C-CF-458` `constraint` Personalisation happens only through declared client-side islands against a separate uncached endpoint. `src: Core features, instruction.md`
- [ ] `C-CF-459` `constraint` A cached storefront document is never varied by buyer. `src: Core features, instruction.md`
- [ ] `C-CF-460` `constraint` The storefront read interface exposes published resources only, resolved through market, catalog. `src: Core features, instruction.md`
- [ ] `C-CF-461` `constraint` The storefront read interface cannot express a query for an unpublished product. `src: Core features, instruction.md`
- [ ] `C-CF-462` `constraint` A storefront read response's cache key never includes a buyer identifier. `src: Core features, instruction.md`
- [ ] `C-CF-463` `constraint` One canonical exists per resource per market, with a product reached through a collection canonicalising to the product. `src: Core features, instruction.md`
- [ ] `C-CF-464` `capability` Structured data for product, offer, breadcrumb, article, organisation is emitted from the same data the page renders. `src: Core features, instruction.md`
- [ ] `C-CF-465` `capability` Sitemaps are per market, paginated, regenerated on a publication change. `src: Core features, instruction.md`
- [ ] `C-CF-466` `constraint` Robots rules are per market, excluding unpublished markets, excluding preview links. `src: Core features, instruction.md`
- [ ] `C-CF-467` `constraint` A product handle change issues a permanent redirect, reserving the old handle against reuse. `src: Core features, instruction.md`
- [ ] `C-CF-468` `constraint` A headless storefront credential is scoped to published market-resolved reads plus cart operations. `src: Core features, instruction.md`
- [ ] `C-CF-469` `constraint` A headless storefront hands checkout off rather than implementing checkout. `src: Core features, instruction.md`
- [ ] `C-CF-470` `constraint` Publishing a theme referencing a deleted section is refused with the template plus the section named. `src: Core features, instruction.md`
- [ ] `C-CF-471` `constraint` A section failing at render renders nothing, with the page still rendering. `src: Core features, instruction.md`
- [ ] `C-CF-472` `data` A failed section is logged with the section key plus the route. `src: Core features, instruction.md`
- [ ] `C-CF-473` `constraint` Removing a metaobject field still referenced by templates is refused with the references listed. `src: Core features, instruction.md`
- [ ] `C-CF-474` `data` A channel carries a kind, a state, a credential reference, a configuration, a capability set. `src: Core features, instruction.md`
- [ ] `C-CF-475` `literal` Channel capabilities are `catalog_sync`, `order_ingest`, `checkout_here`, `checkout_there`, `inventory_sync`, `fulfilment_there`, `returns_there`. `src: Core features, instruction.md`
- [ ] `C-CF-476` `constraint` Every surface derives channel behaviour from the declared capability set rather than from a per-channel branch. `src: Core features, instruction.md`
- [ ] `C-CF-477` `constraint` Channel synchronisation is event-driven from the outbox rather than a nightly sweep. `src: Core features, instruction.md`
- [ ] `C-CF-478` `capability` A scheduled full comparison per channel reports differences rather than applying differences blindly. `src: Core features, instruction.md`
- [ ] `C-CF-479` `constraint` Channel updates apply in order per resource, with a stale update dropped by a monotonic version. `src: Core features, instruction.md`
- [ ] `C-CF-480` `constraint` A slow or failing channel has its own queue paused with an alert, without consuming the shared pool. `src: Core features, instruction.md`
- [ ] `C-CF-481` `constraint` Channel order ingestion deduplicates on the channel's own order identifier. `src: Core features, instruction.md`
- [ ] `C-CF-482` `constraint` An unmatched channel line creates a custom line rather than rejecting the order. `src: Core features, instruction.md`
- [ ] `C-CF-483` `data` An order settled on a channel arrives with its payment recorded as an external settlement. `src: Core features, instruction.md`
- [ ] `C-CF-484` `constraint` Stock is committed on channel order arrival; overselling against a stale catalog produces a backorder plus an alert. `src: Core features, instruction.md`
- [ ] `C-CF-485` `capability` The agent surface publishes a machine-readable catalog document per market at a well-known path, cached. `src: Core features, instruction.md`
- [ ] `C-CF-486` `constraint` An agent must present both an agent credential, a buyer authorization, to create an order. `src: Core features, instruction.md`
- [ ] `C-CF-487` `constraint` An agent credential alone may read a catalog, never create an order. `src: Core features, instruction.md`
- [ ] `C-CF-488` `constraint` The platform never accepts a bare assertion that a buyer consented to an agent purchase. `src: Core features, instruction.md`
- [ ] `C-CF-489` `data` Every agent-initiated order records the agent, the delegation, the delegation's scope, the delegation's expiry. `src: Core features, instruction.md`
- [ ] `C-CF-490` `constraint` A delegation expiring mid-checkout requires the buyer to finish directly. `src: Core features, instruction.md`
- [ ] `C-CF-491` `capability` A merchant opts in per market per channel, opts out, or opts in with a review gate. `src: Core features, instruction.md`
- [ ] `C-CF-492` `constraint` Agent traffic is rate-limited separately from storefront traffic. `src: Core features, instruction.md`
- [ ] `C-CF-493` `capability` An agent whose orders are systematically cancelled or disputed is rate-limited, then suspended, with an appeal path. `src: Core features, instruction.md`
- [ ] `C-CF-494` `capability` A revoked channel credential pauses synchronisation, notifying the merchant with a reconnect path. `src: Core features, instruction.md`
- [ ] `C-CF-495` `constraint` An order arriving for a product unpublished mid-flight is accepted, because publication controls discovery. `src: Core features, instruction.md`
- [ ] `C-CF-496` `data` An application declares its partner owner, its kind, its requested scopes, its callbacks, its subscriptions, its extensions, its listing metadata. `src: Core features, instruction.md`
- [ ] `C-CF-497` `constraint` An installation is per store, never per organisation. `src: Core features, instruction.md`
- [ ] `C-CF-498` `constraint` Application scopes mirror the permission vocabulary, split read from write. `src: Core features, instruction.md`
- [ ] `C-CF-499` `ui` The consent surface lists every scope in plain language, grouped, with dangerous scopes separated, visually distinct. `src: Core features, instruction.md`
- [ ] `C-CF-500` `constraint` An installation never exceeds the permissions of the member who installed the application. `src: Core features, instruction.md`
- [ ] `C-CF-501` `constraint` An installation's ceiling is re-checked when the installing member's permissions shrink. `src: Core features, instruction.md`
- [ ] `C-CF-502` `constraint` A new scope after installation requires fresh consent from a member holding that permission. `src: Core features, instruction.md`
- [ ] `C-CF-503` `constraint` Scopes covering personal data, order exports, payment data require an extra approval step, separately audited. `src: Core features, instruction.md`
- [ ] `C-CF-504` `constraint` Uninstalling revokes credentials immediately, enqueueing data deletion by the application with compliance tracked. `src: Core features, instruction.md`
- [ ] `C-CF-505` `constraint` An installation token is opaque, rotatable with an overlap window, individually revocable. `src: Core features, instruction.md`
- [ ] `C-CF-506` `constraint` An installation token is stored hashed, with the plaintext shown once at issue. `src: Core features, instruction.md`
- [ ] `C-CF-507` `constraint` An installation credential is bound to live or to development, unable to cross. `src: Core features, instruction.md`
- [ ] `C-CF-508` `data` Every mutation by an application records the installation, so the audit shows the application rather than a system actor. `src: Core features, instruction.md`
- [ ] `C-CF-509` `capability` Extension surfaces are an admin panel, a theme section, a checkout extension, a buyer portal extension, a terminal tile. `src: Core features, instruction.md`
- [ ] `C-CF-510` `constraint` An admin extension frame cannot read the admin session. `src: Core features, instruction.md`
- [ ] `C-CF-511` `constraint` A platform function is deterministic, sandboxed, with no network access, no state between runs, a hard budget. `src: Core features, instruction.md`
- [ ] `C-CF-512` `constraint` A function exceeding its budget is skipped, applying the platform default, never failing the checkout. `src: Core features, instruction.md`
- [ ] `C-CF-513` `constraint` A function is pure, so its output is a proposal the platform applies. `src: Core features, instruction.md`
- [ ] `C-CF-514` `constraint` The host passes a capability scoped to one resource rather than a credential. `src: Core features, instruction.md`
- [ ] `C-CF-515` `constraint` An extension content policy is declared per extension, enforced by the host, unwidenable by the extension. `src: Core features, instruction.md`
- [ ] `C-CF-516` `constraint` A failing extension renders its own error region, leaving the host surface usable. `src: Core features, instruction.md`
- [ ] `C-CF-517` `capability` Application billing is one-time, recurring with the merchant's bill, or metered under a merchant-approved cap. `src: Core features, instruction.md`
- [ ] `C-CF-518` `constraint` A metered application charge beyond the approved cap is refused rather than queued. `src: Core features, instruction.md`
- [ ] `C-CF-519` `constraint` An unpaid application charge suspends the application rather than the store. `src: Core features, instruction.md`
- [ ] `C-CF-520` `constraint` Listing review precedes publication, covering scope justification, a data-handling declaration, a functional check. `src: Core features, instruction.md`
- [ ] `C-CF-521` `capability` A compromised application is suspended platform-wide, its credentials revoked, with every affected merchant told what the application could reach. `src: Core features, instruction.md`
- [ ] `C-CF-522` `constraint` An installing member losing permissions freezes the installation's scopes, notifying the store. `src: Core features, instruction.md`
- [ ] `C-CF-523` `capability` An application uninstalled mid-job lets the job finish under a system principal, attributed to the application. `src: Core features, instruction.md`
- [ ] `C-CF-524` `ui` Two applications writing one metafield leave the later write in place, showing both in a conflict view. `src: Core features, instruction.md`
- [ ] `C-CF-525` `constraint` A development application on a live store is refused. `src: Core features, instruction.md`
- [ ] `C-CF-526` `data` A workflow is a node graph of a `trigger`, `condition` nodes with `Then`, `Otherwise` ports, `action` nodes each with an `Output` port. `src: Core features, instruction.md`
- [ ] `C-CF-527` `constraint` A workflow run executes the workflow version the run started with. `src: Core features, instruction.md`
- [ ] `C-CF-528` `capability` Workflow triggers are resource events, a `Scheduled Time` trigger with a named timezone, a manual run, an application event. `src: Core features, instruction.md`
- [ ] `C-CF-529` `constraint` A workflow schedule uses a named zone, so nine in the morning stays nine across a daylight transition. `src: Core features, instruction.md`
- [ ] `C-CF-530` `constraint` A workflow condition is a structured tree of field, operator, value over the triggering resource plus prior steps. `src: Core features, instruction.md`
- [ ] `C-CF-531` `constraint` Both workflow branches are always present, so no case is silently discarded. `src: Core features, instruction.md`
- [ ] `C-CF-532` `capability` Workflow actions are resource mutations, communications, application actions, control actions. `src: Core features, instruction.md`
- [ ] `C-CF-533` `constraint` A workflow runs with the intersection of the activator's permissions plus an explicit declaration on the workflow. `src: Core features, instruction.md`
- [ ] `C-CF-534` `constraint` A workflow can never perform an action the activator could not perform directly. `src: Core features, instruction.md`
- [ ] `C-CF-535` `constraint` A shrinking activator permission set suspends the workflow, notifying the store. `src: Core features, instruction.md`
- [ ] `C-CF-536` `constraint` Workflow execution is at-least-once, so every action is idempotent or guarded by a key. `src: Core features, instruction.md`
- [ ] `C-CF-537` `constraint` A workflow graph is acyclic; a self-retriggering workflow is stopped by a per-resource depth counter with an alert. `src: Core features, instruction.md`
- [ ] `C-CF-538` `constraint` Workflow runs for one resource are serialised, so two events for one order do not race. `src: Core features, instruction.md`
- [ ] `C-CF-539` `capability` Every workflow can be dry-run against historical data with no effects, reporting what would have happened. `src: Core features, instruction.md`
- [ ] `C-CF-540` `capability` Six automation templates ship, each composing a trigger, a condition, two or three actions, under the names the brief states. `src: Core features, instruction.md`
- [ ] `C-CF-541` `capability` Every shipped automation template carries a category label under the names the brief states. `src: Core features, instruction.md`
- [ ] `C-CF-542` `capability` Notification classes are transactional to a buyer, marketing to a buyer, operational to staff, security to staff, platform to a merchant. `src: Core features, instruction.md`
- [ ] `C-CF-543` `constraint` A transactional template draws from a restricted block set containing no promotional block. `src: Core features, instruction.md`
- [ ] `C-CF-544` `constraint` Security notifications, platform billing notifications are never suppressible. `src: Core features, instruction.md`
- [ ] `C-CF-545` `data` A template exists per event per locale with a versioned merchant override, declaring the fields the template may use. `src: Core features, instruction.md`
- [ ] `C-CF-546` `constraint` A template locale resolves from the buyer's locale, then the market's primary language, then the store default. `src: Core features, instruction.md`
- [ ] `C-CF-547` `constraint` A merchant override failing to render falls back to the platform default, alerting the merchant. `src: Core features, instruction.md`
- [ ] `C-CF-548` `constraint` Double opt-in is required for every marketing subscription. `src: Core features, instruction.md`
- [ ] `C-CF-549` `constraint` Unsubscribing is one click, needs no sign-in, has no confirmation step, takes effect within seconds. `src: Core features, instruction.md`
- [ ] `C-CF-550` `constraint` A suppression list is global per store, honoured by every send path. `src: Core features, instruction.md`
- [ ] `C-CF-551` `constraint` An import re-adding a suppressed address does not resurrect consent. `src: Core features, instruction.md`
- [ ] `C-CF-552` `constraint` A merchant sending domain is used only once its authentication records are confirmed. `src: Core features, instruction.md`
- [ ] `C-CF-553` `constraint` Under pressure marketing messages are slowed ahead of transactional ones. `src: Core features, instruction.md`
- [ ] `C-CF-554` `constraint` Every send carries a key derived from its event, so a retried job does not send twice. `src: Core features, instruction.md`
- [ ] `C-CF-555` `capability` Operational notifications batch on a short window, so a bulk import produces one summary. `src: Core features, instruction.md`
- [ ] `C-CF-556` `capability` Quiet hours are configurable per person for operational classes, never applied to security or transactional classes. `src: Core features, instruction.md`
- [ ] `C-CF-557` `constraint` A message provider outage queues transactional messages with a maximum age, then surfaces them as undelivered. `src: Core features, instruction.md`
- [ ] `C-CF-558` `data` An analytics fact is an immutable row derived from an event. `src: Core features, instruction.md`
- [ ] `C-CF-559` `data` Analytics dimensions cover time, channel, market, location, product, variant, collection, segment, company, staff, campaign, device, country. `src: Core features, instruction.md`
- [ ] `C-CF-560` `data` Analytics measures cover sales, orders, units, average order value, conversion, sessions, returns, refunds, margin, fees, payouts. `src: Core features, instruction.md`
- [ ] `C-CF-561` `constraint` A report states its grain. `src: Core features, instruction.md`
- [ ] `C-CF-562` `constraint` Every money measure reconciles exactly to the ledger for the same period, the same filter. `src: Core features, instruction.md`
- [ ] `C-CF-563` `constraint` A scheduled comparison alerts on any money difference beyond zero, with no tolerance. `src: Core features, instruction.md`
- [ ] `C-CF-564` `constraint` Every analytics period boundary is computed in the store's named timezone. `src: Core features, instruction.md`
- [ ] `C-CF-565` `constraint` A period that covers today is labelled partial, never compared against a complete one silently. `src: Core features, instruction.md`
- [ ] `C-CF-566` `constraint` A retail location's day runs from register open to register close rather than midnight to midnight. `src: Core features, instruction.md`
- [ ] `C-CF-567` `data` A register session records open, close instants, opening, closing float, expected, counted cash, the variance. `src: Core features, instruction.md`
- [ ] `C-CF-568` `role` Cash variance per session, per associate sits behind its own permission. `src: Core features, instruction.md`
- [ ] `C-CF-569` `constraint` An offline sale attributes to the instant of sale rather than the instant of synchronisation, flagged as late-arriving. `src: Core features, instruction.md`
- [ ] `C-CF-570` `ui` Every analytics surface states when its data was last updated. `src: Core features, instruction.md`
- [ ] `C-CF-571` `ui` Any approximate measure is labelled with its method named. `src: Core features, instruction.md`
- [ ] `C-CF-572` `ui` Session counts, visitor counts are never presented beside exact money without distinction. `src: Core features, instruction.md`
- [ ] `C-CF-573` `ui` A report states its attribution model rather than presenting one number as the number. `src: Core features, instruction.md`
- [ ] `C-CF-574` `ui` A measure with no data renders as no data rather than as zero. `src: Core features, instruction.md`
- [ ] `C-CF-575` `ui` A total under a filter states that the total is filtered. `src: Core features, instruction.md`
- [ ] `C-CF-576` `constraint` Exports are always asynchronous. `src: Core features, instruction.md`
- [ ] `C-CF-577` `role` A personal-data export is a dangerous action. `src: Core features, instruction.md`
- [ ] `C-CF-578` `constraint` Fields the acting member may not read are absent from an export artefact. `src: Core features, instruction.md`
- [ ] `C-CF-579` `constraint` An export artefact is signed, expiring, single-audience, with its download audited. `src: Core features, instruction.md`
- [ ] `C-CF-580` `capability` An export completion notifies with the row count plus the filter restated. `src: Core features, instruction.md`
- [ ] `C-CF-581` `constraint` A refund in a later period than its order is reported on the instant the money moved. `src: Core features, instruction.md`
- [ ] `C-CF-582` `constraint` An order cancelled after its period closed restates the period visibly. `src: Core features, instruction.md`
- [ ] `C-CF-583` `constraint` A multi-currency store's totals are per currency, never summed without an explicit dated conversion. `src: Core features, instruction.md`
- [ ] `C-CF-584` `constraint` Every mutation of a governed resource writes an audit entry in the same transaction as the mutation. `src: Core features, instruction.md`
- [ ] `C-CF-585` `constraint` Every audit entry names a principal, so no anonymous system actor exists. `src: Core features, instruction.md`
- [ ] `C-CF-586` `data` An audit entry carries actor, on-behalf-of actor, action, resource, changed fields before, after, address, user agent, session, correlation identifier, level, instant, two hashes. `src: Core features, instruction.md`
- [ ] `C-CF-587` `constraint` Sensitive values inside an audit entry are reduced to a hash. `src: Core features, instruction.md`
- [ ] `C-CF-588` `constraint` The audit record is append-only, enforced by database privilege rather than by convention. `src: Core features, instruction.md`
- [ ] `C-CF-589` `constraint` The audit record is hash-chained per organisation, so altering an old entry breaks every later hash. `src: Core features, instruction.md`
- [ ] `C-CF-590` `capability` A chain verifier reports the position of the first break. `src: Core features, instruction.md`
- [ ] `C-CF-591` `constraint` The audit chain head is published to an append-only external store on a schedule. `src: Core features, instruction.md`
- [ ] `C-CF-592` `constraint` A detected chain break is never repaired. `src: Core features, instruction.md`
- [ ] `C-CF-593` `constraint` A merchant asking to delete audit entries is refused. `src: Core features, instruction.md`
- [ ] `C-CF-594` `constraint` Ordinary reads are not audited; bulk reads, exports, sensitive personal reads are. `src: Core features, instruction.md`
- [ ] `C-CF-595` `constraint` A dangerous action requires a confirmation whose confirming input is the resource's own identifier. `src: Core features, instruction.md`
- [ ] `C-CF-596` `constraint` A dangerous action notifies the store owner asynchronously. `src: Core features, instruction.md`
- [ ] `C-CF-597` `data` Every consent captures purpose, state, exact text, text version, instant, source surface, address. `src: Core features, instruction.md`
- [ ] `C-CF-598` `capability` Consent purposes are separate for marketing email, marketing messaging, analytics, personalisation, plus any an application declares. `src: Core features, instruction.md`
- [ ] `C-CF-599` `constraint` Consent withdrawal is as easy as granting, propagating to every consumer with applications notified. `src: Core features, instruction.md`
- [ ] `C-CF-600` `constraint` Every column is classified as not personal, personal, sensitive personal, or payment, in the schema. `src: Core features, instruction.md`
- [ ] `C-CF-601` `constraint` Sensitive personal fields, payment fields are encrypted at the field level under an organisation-scoped key. `src: Core features, instruction.md`
- [ ] `C-CF-602` `constraint` Personal data never enters an application log, a trace attribute, an error report, an analytics event. `src: Core features, instruction.md`
- [ ] `C-CF-603` `constraint` Storefront attribution is discarded once an account exists. `src: Core features, instruction.md`
- [ ] `C-CF-604` `constraint` Data region is chosen at organisation creation, immutable afterwards. `src: Core features, instruction.md`
- [ ] `C-CF-605` `constraint` Cross-region movement of personal data requires an explicit logged transfer with a lawful basis recorded. `src: Core features, instruction.md`
- [ ] `C-CF-606` `literal` Retention defaults are `7` days for the event log, `30` days for delivery attempts, `90` days for abandoned checkouts, `1` year minimum for the audit record. `src: Core features, instruction.md`
- [ ] `C-CF-607` `constraint` A record a regulation requires is retained with its personal fields anonymised rather than removed. `src: Core features, instruction.md`
- [ ] `C-CF-608` `capability` A data-subject request is access, portability, erasure, rectification, or restriction, each with a tracked window. `src: Core features, instruction.md`
- [ ] `C-CF-609` `constraint` Erasure covers the primary store, the analytics store, the search index, the cache, the event log, every backup restore path. `src: Core features, instruction.md`
- [ ] `C-CF-610` `constraint` Erasure propagates to every installed application holding the data, with completion tracked, reported. `src: Core features, instruction.md`
- [ ] `C-CF-611` `constraint` An application not confirming erasure is escalated, then suspended, with the merchant told. `src: Core features, instruction.md`
- [ ] `C-CF-612` `constraint` Erasure replaces personal fields with a stable non-identifying token, so the commercial record still reconciles. `src: Core features, instruction.md`
- [ ] `C-CF-613` `constraint` Restoring a backup replays the erasure log before the restore goes live. `src: Core features, instruction.md`
- [ ] `C-CF-614` `constraint` A tax invoice is immutable once finalised, numbered sequentially per store per jurisdiction with no gaps. `src: Core features, instruction.md`
- [ ] `C-CF-615` `constraint` A correction to a finalised invoice is a credit note rather than an edited invoice. `src: Core features, instruction.md`
- [ ] `C-CF-616` `constraint` Consent records are retained beyond the subject's other data. `src: Core features, instruction.md`
- [ ] `C-CF-617` `constraint` The country segment is the first path element on every marketing route except the global root. `src: Core features, instruction.md`
- [ ] `C-CF-618` `constraint` A second language is a sibling path rather than a query parameter or a cookie-only switch. `src: Core features, instruction.md`
- [ ] `C-CF-619` `constraint` A trailing slash redirects permanently to the canonical form. `src: Core features, instruction.md`
- [ ] `C-CF-620` `capability` Changing the country changes prices, available plans, capability availability, editorial content, number format, date format, hero media. `src: Core features, instruction.md`
- [ ] `C-CF-621` `literal` The India storefront advertises `24/7 local chat support` as a plan line. `src: Core features, instruction.md`
- [ ] `C-CF-622` `constraint` An explicit country segment in the path always wins, never overridden by a header or a cookie. `src: Core features, instruction.md`
- [ ] `C-CF-623` `constraint` An explicit language suffix in the path wins for language. `src: Core features, instruction.md`
- [ ] `C-CF-624` `constraint` The global root negotiates from the country signal plus the accept-language header, issuing a temporary redirect. `src: Core features, instruction.md`
- [ ] `C-CF-625` `constraint` A stored locale preference is consulted only at the negotiation step. `src: Core features, instruction.md`
- [ ] `C-CF-626` `constraint` An unpublished country resolves to the global root with the locale control opened pre-filtered. `src: Core features, instruction.md`
- [ ] `C-CF-627` `constraint` Negotiation never varies the response body at a cached path. `src: Core features, instruction.md`
- [ ] `C-CF-628` `constraint` Currency renders from the locale's own convention rather than a symbol concatenated with a foreign format. `src: Core features, instruction.md`
- [ ] `C-CF-629` `constraint` The Indian grouping convention groups the lowest three digits, then every two above. `src: Core features, instruction.md`
- [ ] `C-CF-630` `capability` Large numbers use the locale's convention, lakh plus crore on the India storefront. `src: Core features, instruction.md`
- [ ] `C-CF-631` `constraint` Dates use the locale's format, day then abbreviated month then four-digit year on the India storefront. `src: Core features, instruction.md`
- [ ] `C-CF-632` `constraint` The product supports right-to-left, mirroring every directional icon, expressing every inline offset on the logical axis. `src: Core features, instruction.md`
- [ ] `C-CF-633` `constraint` A plan line is an entitlement enforced at write time with the plan named in the refusal. `src: Core features, instruction.md`
- [ ] `C-CF-634` `literal` The entitlement `staff_seats` is enforced at invitation acceptance, at membership reactivation. `src: Core features, instruction.md`
- [ ] `C-CF-635` `literal` The entitlement `inventory_locations` is enforced at location creation. `src: Core features, instruction.md`
- [ ] `C-CF-636` `literal` The entitlement `b2b_catalogs` is enforced at catalog creation. `src: Core features, instruction.md`
- [ ] `C-CF-637` `literal` The entitlement `market_customisation` is enforced at a market setting override. `src: Core features, instruction.md`
- [ ] `C-CF-638` `literal` The entitlement `checkout_customisation` is enforced at extension installation on checkout. `src: Core features, instruction.md`
- [ ] `C-CF-639` `literal` The entitlement `carrier_calculated_rates` is enforced at carrier configuration, at checkout rate resolution. `src: Core features, instruction.md`
- [ ] `C-CF-640` `constraint` An entitlement reduction on downgrade makes the excess read-only within a grace window, deleting nothing. `src: Core features, instruction.md`
- [ ] `C-CF-641` `literal` The plan comparison carries a billing toggle labelled `Pay yearly` rewriting every price cell. `src: Core features, instruction.md`
- [ ] `C-CF-642` `constraint` Prices come from the server already worked out, so the billing toggle never computes one. `src: Core features, instruction.md`
- [ ] `C-CF-643` `constraint` The billing toggle writes a query parameter, so a shared link opens on the same term. `src: Core features, instruction.md`
- [ ] `C-CF-644` `ui` A plan not sold on a term renders `-`, replacing its call to action with the sales path. `src: Core features, instruction.md`
- [ ] `C-CF-645` `ui` The billing toggle announces its state, with rewritten prices in a live region. `src: Core features, instruction.md`
- [ ] `C-CF-646` `constraint` Every marketing statistic carries a superscript marker resolving to a numbered footnote that links back. `src: Core features, instruction.md`
- [ ] `C-CF-647` `constraint` A claim with a dangling footnote marker does not ship. `src: Core features, instruction.md`
- [ ] `C-CF-648` `constraint` A plan badge reads the lowest plan carrying a feature, from the same entitlement source as the comparison table. `src: Core features, instruction.md`
- [ ] `C-CF-649` `capability` A capability not sold in a country is hidden, gated, or waitlisted, recorded as data per country. `src: Core features, instruction.md`
- [ ] `C-CF-650` `constraint` A country condition is never hard-coded inside a template. `src: Core features, instruction.md`
- [ ] `C-CF-651` `constraint` A control deep-linking into the admin degrades to the trial signup when no session cookie is present. `src: Core features, instruction.md`
- [ ] `C-CF-652` `constraint` A deep-linking control never reveals by its rendering whether a session exists. `src: Core features, instruction.md`
- [ ] `C-CF-653` `capability` The retail route offers both a trial path, an existing-account path, at every conversion block. `src: Core features, instruction.md`
- [ ] `C-CF-654` `constraint` A storefront form validates on blur for a field the visitor has left, on submit for the whole form. `src: Core features, instruction.md`
- [ ] `C-CF-655` `constraint` A field that has shown an error re-validates on input, so the error clears as the field is fixed. `src: Core features, instruction.md`
- [ ] `C-CF-656` `ui` A validation message sits beneath its field, associated with the field, announced when focus enters. `src: Core features, instruction.md`
- [ ] `C-CF-657` `ui` A validation message says what is wrong plus what to do rather than reading `Invalid`. `src: Core features, instruction.md`
- [ ] `C-CF-658` `ui` A failed submit puts a summary at the top listing each failed field as a link, moving focus to the summary. `src: Core features, instruction.md`
- [ ] `C-CF-659` `constraint` Every storefront validation rule is enforced again on the server. `src: Core features, instruction.md`
- [ ] `C-CF-660` `constraint` A failed submission returns every entered value. `src: Core features, instruction.md`
- [ ] `C-CF-661` `ui` A submit control disables plus announces a busy state on submit. `src: Core features, instruction.md`
- [ ] `C-CF-662` `constraint` Every storefront submission carries a client-generated key, so a double submit produces one record. `src: Core features, instruction.md`
- [ ] `C-CF-663` `constraint` Form anti-abuse uses a token bucket per address, per network prefix. `src: Core features, instruction.md`
- [ ] `C-CF-664` `constraint` A challenge is presented only after a suspicion threshold, never on the first attempt, never requiring vision alone. `src: Core features, instruction.md`
- [ ] `C-CF-665` `constraint` An unattended decoy field must remain empty, carrying an accessible label, removed from the tab order. `src: Core features, instruction.md`
- [ ] `C-CF-666` `constraint` A submission faster than a human floor is treated as suspicious rather than rejected. `src: Core features, instruction.md`
- [ ] `C-CF-667` `constraint` A disposable address is flagged for routing rather than silently rejected. `src: Core features, instruction.md`
- [ ] `C-CF-668` `constraint` A form submitted by a bot is refused, either by a filled decoy field or by repeated quick submission. `src: Core features, instruction.md`
- [ ] `C-CF-669` `data` An editorial article is stored per locale rather than as one record with translations hung off. `src: Core features, instruction.md`
- [ ] `C-CF-670` `data` An editorial article carries a slug unique per locale, a title, a standfirst, one primary topic, tags, an author, instants, a locale, a body, related articles, a derived reading time. `src: Core features, instruction.md`
- [ ] `C-CF-671` `constraint` A withdrawn article answers gone rather than not-found, linking the topic index. `src: Core features, instruction.md`
- [ ] `C-CF-672` `constraint` A locale missing an article never renders the article in another language without saying so. `src: Core features, instruction.md`
- [ ] `C-CF-673` `constraint` Editorial search is scoped to editorial content, never returning product routes. `src: Core features, instruction.md`
- [ ] `C-CF-674` `constraint` Editorial search works with client scripting unavailable, as a form submitting to a results route. `src: Core features, instruction.md`
- [ ] `C-CF-675` `ui` An empty editorial search result renders a heading, one sentence, the topic navigation. `src: Core features, instruction.md`
- [ ] `C-CF-676` `capability` An unknown address renders Mercato's own not-found page inside global chrome, answering not-found. `src: Core features, instruction.md`
- [ ] `C-CF-677` `ui` The not-found page carries one heading, one sentence, a focusable search control, a way back, the footer. `src: Core features, instruction.md`
- [ ] `C-CF-678` `constraint` Every internal link on every public route resolves. `src: Core features, instruction.md`
- [ ] `C-CF-679` `capability` A privacy page is reachable from the footer of every page, stating what Mercato stores plus how long. `src: Core features, instruction.md`
- [ ] `C-CF-680` `capability` A terms page is reachable from the footer of every page, linked additionally from the signup form. `src: Core features, instruction.md`

## C-UF User flow

- [ ] `C-UF-01` `contract` The route `/` serves the global root negotiating to a country storefront. `src: User flow, instruction.md`
- [ ] `C-UF-02` `contract` The route `/in` serves the country home. `src: User flow, instruction.md`
- [ ] `C-UF-03` `contract` The route `/in-hi` serves the country home in the second language, fully translated. `src: User flow, instruction.md`
- [ ] `C-UF-04` `contract` The route `/in/pricing` serves the plan comparison plus the feature table. `src: User flow, instruction.md`
- [ ] `C-UF-05` `contract` The route `/in/start` serves the trial funnel carrying one control, no form. `src: User flow, instruction.md`
- [ ] `C-UF-06` `contract` The route `/in/checkout` serves the checkout capability route. `src: User flow, instruction.md`
- [ ] `C-UF-07` `contract` The route `/in/payments` serves the payments capability route. `src: User flow, instruction.md`
- [ ] `C-UF-08` `contract` The route `/in/orders` serves the orders capability route. `src: User flow, instruction.md`
- [ ] `C-UF-09` `contract` The route `/in/markets` serves the markets capability route. `src: User flow, instruction.md`
- [ ] `C-UF-10` `contract` The route `/in/flow` serves the automations capability route. `src: User flow, instruction.md`
- [ ] `C-UF-11` `contract` The route `/in/pos` serves the retail surface wearing its own chrome. `src: User flow, instruction.md`
- [ ] `C-UF-12` `contract` The route `/in/enterprise` serves the enterprise surface wearing its own chrome. `src: User flow, instruction.md`
- [ ] `C-UF-13` `contract` The route `/in/plus/solutions/b2b-ecommerce` serves the business-buyer surface wearing the upmarket chrome. `src: User flow, instruction.md`
- [ ] `C-UF-14` `contract` The route `/in/blog` serves the editorial index, the only chrome carrying search. `src: User flow, instruction.md`
- [ ] `C-UF-15` `contract` The route `/in/blog/topics/<topic>` serves the editorial topic index. `src: User flow, instruction.md`
- [ ] `C-UF-16` `contract` The route `/in/privacy` serves the privacy page linked from every footer. `src: User flow, instruction.md`
- [ ] `C-UF-17` `contract` The route `/in/terms` serves the terms page linked from every footer. `src: User flow, instruction.md`
- [ ] `C-UF-18` `contract` The route `/sitemap.xml` serves the sitemap listing every public route. `src: User flow, instruction.md`
- [ ] `C-UF-19` `contract` The route `/robots.txt` serves the robots file pointing at the sitemap. `src: User flow, instruction.md`
- [ ] `C-UF-20` `contract` The route `/signin` serves the start of the authorization-code flow at the issuer. `src: User flow, instruction.md`
- [ ] `C-UF-21` `contract` The route `/store` serves the store picker for a person holding more than one membership. `src: User flow, instruction.md`
- [ ] `C-UF-22` `contract` The route `/store/<store>/home` serves the activity tiles plus the setup checklist. `src: User flow, instruction.md`
- [ ] `C-UF-23` `contract` The route `/store/<store>/orders` serves the order queue-list with saved views, metric tiles. `src: User flow, instruction.md`
- [ ] `C-UF-24` `contract` The route `/store/<store>/orders/<id>` serves the order detail, timeline, refund composer. `src: User flow, instruction.md`
- [ ] `C-UF-25` `contract` The route `/store/<store>/orders/drafts` serves the draft orders, quotes. `src: User flow, instruction.md`
- [ ] `C-UF-26` `contract` The route `/store/<store>/orders/returns` serves the return requests. `src: User flow, instruction.md`
- [ ] `C-UF-27` `contract` The route `/store/<store>/approvals` serves the approval queue-list. `src: User flow, instruction.md`
- [ ] `C-UF-28` `contract` The route `/store/<store>/approvals/<id>` serves the one request with its parameters, its decision controls. `src: User flow, instruction.md`
- [ ] `C-UF-29` `contract` The route `/store/<store>/products` serves the catalog index. `src: User flow, instruction.md`
- [ ] `C-UF-30` `contract` The route `/store/<store>/products/<id>` serves the product detail with variants. `src: User flow, instruction.md`
- [ ] `C-UF-31` `contract` The route `/store/<store>/products/inventory` serves the stock by location. `src: User flow, instruction.md`
- [ ] `C-UF-32` `contract` The route `/store/<store>/products/transfers` serves the inbound transfers. `src: User flow, instruction.md`
- [ ] `C-UF-33` `contract` The route `/store/<store>/customers` serves the customer index with segments. `src: User flow, instruction.md`
- [ ] `C-UF-34` `contract` The route `/store/<store>/customers/companies` serves the companies, locations, contacts. `src: User flow, instruction.md`
- [ ] `C-UF-35` `contract` The route `/store/<store>/discounts` serves the discounts, codes. `src: User flow, instruction.md`
- [ ] `C-UF-36` `contract` The route `/store/<store>/markets` serves the markets, catalogs, price lists, domains. `src: User flow, instruction.md`
- [ ] `C-UF-37` `contract` The route `/store/<store>/finances` serves the balances, payouts, disputes, bills. `src: User flow, instruction.md`
- [ ] `C-UF-38` `contract` The route `/store/<store>/analytics` serves the reports, exports. `src: User flow, instruction.md`
- [ ] `C-UF-39` `contract` The route `/store/<store>/online-store/themes` serves the theme library plus editor. `src: User flow, instruction.md`
- [ ] `C-UF-40` `contract` The route `/store/<store>/apps` serves the installed applications with their grants. `src: User flow, instruction.md`
- [ ] `C-UF-41` `contract` The route `/store/<store>/automations` serves the workflow list, canvas, dry run. `src: User flow, instruction.md`
- [ ] `C-UF-42` `contract` The route `/store/<store>/settings/users` serves the staff, roles, constraints, ceilings. `src: User flow, instruction.md`
- [ ] `C-UF-43` `contract` The route `/store/<store>/settings/audit` serves the audit search. `src: User flow, instruction.md`
- [ ] `C-UF-44` `contract` The route `/org/<org>/stores` serves the organisation store list. `src: User flow, instruction.md`
- [ ] `C-UF-45` `contract` The route `/org/<org>/users` serves the identity configuration plus group mapping. `src: User flow, instruction.md`
- [ ] `C-UF-46` `contract` The route `/org/<org>/audit` serves the cross-store audit search. `src: User flow, instruction.md`
- [ ] `C-UF-47` `contract` The route `/shop/<store>` serves the a merchant's own buyer-facing store. `src: User flow, instruction.md`
- [ ] `C-UF-48` `contract` The route `/shop/<store>/products/<handle>` serves the buyer-facing product page. `src: User flow, instruction.md`
- [ ] `C-UF-49` `contract` The route `/shop/<store>/cart` serves the cart. `src: User flow, instruction.md`
- [ ] `C-UF-50` `contract` The route `/shop/<store>/orders/<token>` serves the order status page plus self-serve returns. `src: User flow, instruction.md`
- [ ] `C-UF-51` `contract` The route `/checkout/<token>` serves the hosted checkout, first step. `src: User flow, instruction.md`
- [ ] `C-UF-52` `contract` The route `/checkout/<token>/<step>` serves the hosted checkout, a named step. `src: User flow, instruction.md`
- [ ] `C-UF-53` `contract` The route `/api/health` serves the readiness endpoint. `src: User flow, instruction.md`
- [ ] `C-UF-54` `capability` An unauthenticated request to an admin route starts the authorization-code flow, returning to the route asked for. `src: User flow, instruction.md`
- [ ] `C-UF-55` `capability` A person with exactly one active membership lands on that store's home after signing in. `src: User flow, instruction.md`
- [ ] `C-UF-56` `capability` A person with more than one membership lands on the store picker after signing in. `src: User flow, instruction.md`
- [ ] `C-UF-57` `contract` Signing out revokes the session on the server, landing on the country home. `src: User flow, instruction.md`
- [ ] `C-UF-58` `capability` A token expiring mid-action returns the actor to sign-in with the composed work preserved, restored afterwards. `src: User flow, instruction.md`
- [ ] `C-UF-59` `ui` A route the actor's role forbids renders an explanation naming the permission required, naming which roles hold one. `src: User flow, instruction.md`
- [ ] `C-UF-60` `ui` A navigation item for a forbidden route is absent. `src: User flow, instruction.md`
- [ ] `C-UF-61` `capability` A refund of `400000` against order `#2050` from a `support@example.com` session completes immediately. `src: User flow, instruction.md`
- [ ] `C-UF-62` `ui` A completed refund shows an inline banner on the order rather than a full-page confirmation. `src: User flow, instruction.md`
- [ ] `C-UF-63` `ui` The refund composer states before submission that an amount above the ceiling will be sent for approval. `src: User flow, instruction.md`
- [ ] `C-UF-64` `ui` Submitting an above-ceiling refund lands on a full-page confirmation naming the request, its amount, the permission required, its expiry. `src: User flow, instruction.md`
- [ ] `C-UF-65` `ui` The approval queue-list carries each pending request with its requester, its amount, its reason, its expiry. `src: User flow, instruction.md`
- [ ] `C-UF-66` `ui` An approval decision lands on a full-page confirmation. `src: User flow, instruction.md`
- [ ] `C-UF-67` `constraint` Approving one request twice creates no second refund. `src: User flow, instruction.md`
- [ ] `C-UF-68` `ui` Decision controls on the requester's own request are present, disabled, with the reason available on focus. `src: User flow, instruction.md`
- [ ] `C-UF-69` `constraint` A `mallard@example.com` session cannot reach order `#2049` by its identifier. `src: User flow, instruction.md`
- [ ] `C-UF-70` `constraint` The order index for `Modern Mallard` shows `#3001` alone, with the stated count matching. `src: User flow, instruction.md`
- [ ] `C-UF-71` `constraint` A member constrained to `Pune Warehouse` is refused a direct adjustment naming `Delhi Flagship`, with the level unchanged. `src: User flow, instruction.md`
- [ ] `C-UF-72` `capability` A buyer can add a product to a cart, open the cart, continue to checkout, pay, land on the order status page. `src: User flow, instruction.md`
- [ ] `C-UF-73` `ui` Every list carries an empty state naming what to do next, offering the primary creating action. `src: User flow, instruction.md`
- [ ] `C-UF-74` `ui` A filtered-to-empty state names the active filters, offering to clear them. `src: User flow, instruction.md`
- [ ] `C-UF-75` `ui` Every page carries a loading state where the shell renders at once, the content region showing a matching skeleton. `src: User flow, instruction.md`
- [ ] `C-UF-76` `ui` A degraded dependency replaces its own region with a retry control naming what is unavailable. `src: User flow, instruction.md`
- [ ] `C-UF-77` `ui` The admin carries a system-state region naming any capability currently running on a fallback. `src: User flow, instruction.md`
- [ ] `C-UF-78` `ui` An offline page already loaded stays readable from cache behind a persistent banner, with mutating controls disabled. `src: User flow, instruction.md`
- [ ] `C-UF-79` `ui` A long operation shows progress, offers cancelling where safe, survives a reload plus a sign-out, notifies on completion. `src: User flow, instruction.md`
- [ ] `C-UF-80` `ui` Every error screen carries a copyable correlation identifier, saying whether retrying can succeed. `src: User flow, instruction.md`
- [ ] `C-UF-81` `constraint` No error screen shows a stack trace, an internal identifier, or a hint that another tenant exists. `src: User flow, instruction.md`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The north star is comprehension: what needs doing today, who is allowed to do one, legible in the first moment. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-02` `ui` The admin reads as an operational tool: quiet, dense but organised, restrained, built for scanning. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-03` `ui` The admin carries no oversized hero, no editorial composition. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-04` `ui` The public storefront may carry atmosphere, with the depicted product seen first. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-05` `ui` Each page leads with one clear primary action, visually distinct from every secondary one. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-06` `ui` Nothing moves as a refund amount is typed, with the order's own figures beside the field. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-07` `ui` The page ground on light is a near-white neutral; on dark a near-black cool neutral reading blue-green. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-08` `ui` A card sits one step off its ground on either scheme, staying visibly separate without a shadow. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-09` `ui` Ink is a near-black neutral; muted copy on light is a mid cool neutral; secondary copy on dark is a light cool neutral. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-10` `ui` The mark plus anything that worked carry a deep, soft teal. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-11` `ui` One accent, a light vivid teal, appears in exactly three places: the closing numerals, the mega-menu eyebrow, the market status pill. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-12` `ui` Failure is a light vivid red with a light soft red as its tint. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-13` `ui` Something still in progress is a near-white muted teal; one near-white muted green wash appears once. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-14` `ui` A state that is neither failure, success, nor in progress borrows none of those three colours. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-15` `ui` The saturated payment palette of indigo, blue, cyan tones belongs to product graphics, never to chrome. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-16` `ui` Link focus on the dark ground is brighter than hover; link active is dimmer than hover. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-17` `ui` One variable grotesque family carries the whole product, upright only, with no italic file loaded. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-18` `ui` Display sizes are set lighter than body sizes, which is the design's signature inversion. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-19` `ui` Figures align in a column wherever amounts stack. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-20` `ui` Spacing comes off one base unit, with every gap a multiple of one. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-21` `ui` The gap between sections is roughly three times the gap beneath a heading, halving on a narrow screen. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-22` `ui` Corners soften in four steps, with the pill reserved for circular icon buttons plus the primary action. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-23` `ui` The page is flat; depth belongs to depicted objects rather than to chrome. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-24` `ui` Density is compact in the admin so a full queue fits one screen, spacious on the storefront. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-25` `ui` The admin shell is a top bar, a collapsible left navigation, a sticky content header, an independently scrolling page. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-26` `ui` The collapsed navigation state persists per person per device. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-27` `ui` Navigation inside the shell is a breadcrumbed drill-down from index to detail with a trail back through parents. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-28` `ui` The storefront ships four distinct chromes rather than one with a flag. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-29` `ui` Motion is described to the browser once rather than redrawn by a script on every frame. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-30` `ui` Everything shares three easings plus one speed, with nothing using a different speed to feel special. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-31` `ui` Every named motion moment has a reduced-motion twin that never leaves content invisible or mid-travel. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-32` `ui` Only opacity, transform, translate, scale, rotate, filter, clip path, mask, custom properties ever animate. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-33` `ui` A focus or hover colour change is retained under reduced motion, because a colour change is not motion. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-34` `ui` Text plus its background meet WCAG AA contrast, as do control boundaries, focus rings, meaningful graphics. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-35` `ui` Every interaction has a keyboard path, with full keyboard navigation carrying a visible focus ring. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-36` `ui` Touch targets are comfortably sized on the shorter axis. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-37` `ui` An icon-only control carries a name saying the action rather than the icon. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-38` `ui` Status, validity, required-ness, selection each carry a second signal beyond colour. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-39` `ui` The mega-menu sibling dimming, the statement band's resting colour are measured against the contrast floor. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-40` `ui` Responsive behaviour holds at every width between the four tiers rather than only at them. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-41` `ui` Hover response is decided by whether the device has a hover-capable pointer rather than by viewport width. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-42` `ui` The page never scrolls sideways at any width, in any language, in either direction. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-43` `ui` Wide content scrolls inside its own container with a softened edge. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-44` `ui` The layout survives doubled text scaling plus hard page zoom, reflowing to a single column. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-45` `ui` No page is dominated by a single hue family with no second signal. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-46` `ui` No decoration stands in for content. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-47` `ui` No marketing composition appears where the working interface belongs. `src: UI/UX notes, instruction.md`
- [ ] `C-UX-48` `ui` The stance is space over dividers, comprehension over atmosphere in the admin, stillness over feedback during a money decision. `src: UI/UX notes, instruction.md`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The neutral ramp ships in two forms, selected by capability rather than by user agent string. `src: Front-end specification, instruction.md`
- [ ] `C-FE-02` `ui` Generated neutral ramps are declared perceptually, so a tint stays perceptually uniform. `src: Front-end specification, instruction.md`
- [ ] `C-FE-03` `ui` Compositing helpers mix in a perceptual space rather than the ordinary one. `src: Front-end specification, instruction.md`
- [ ] `C-FE-04` `ui` White is the page ground on light surfaces plus all display type on dark heroes. `src: Front-end specification, instruction.md`
- [ ] `C-FE-05` `ui` Black is the page ground on the darkest sections plus type on light surfaces. `src: Front-end specification, instruction.md`
- [ ] `C-FE-06` `ui` A ten-percent black scrim sits over hero media. `src: Front-end specification, instruction.md`
- [ ] `C-FE-07` `ui` A twenty-percent white rule is the pill-button border. `src: Front-end specification, instruction.md`
- [ ] `C-FE-08` `ui` A ten-percent white is the inner border on dark cards. `src: Front-end specification, instruction.md`
- [ ] `C-FE-09` `ui` Link states on the dark ground are a family of five: rest, hover, active, focus, disabled. `src: Front-end specification, instruction.md`
- [ ] `C-FE-10` `ui` The variable grotesque runs a `100 900` axis in a single file with a named fallback stack. `src: Front-end specification, instruction.md`
- [ ] `C-FE-11` `ui` Monospace is reserved for identifiers, falling back to the system monospace stack. `src: Front-end specification, instruction.md`
- [ ] `C-FE-12` `ui` Nine display steps each carry their own size, line height, tracking as one group. `src: Front-end specification, instruction.md`
- [ ] `C-FE-13` `ui` Three body steps plus two control steps are carried exactly. `src: Front-end specification, instruction.md`
- [ ] `C-FE-14` `ui` Display sizes clamp continuously; body sizes do not scale at all. `src: Front-end specification, instruction.md`
- [ ] `C-FE-15` `ui` Five secondary faces appear inside the theme-preview graphic, never in chrome. `src: Front-end specification, instruction.md`
- [ ] `C-FE-16` `ui` A spacing ramp of ten steps runs from a quarter of the base unit upward. `src: Front-end specification, instruction.md`
- [ ] `C-FE-17` `ui` The hero offset stays an expression rather than a resolved figure, keeping the header-height seam. `src: Front-end specification, instruction.md`
- [ ] `C-FE-18` `ui` Four radius steps run from barely softened to noticeably softened. `src: Front-end specification, instruction.md`
- [ ] `C-FE-19` `ui` Five container steps set the measure limits rather than the page width. `src: Front-end specification, instruction.md`
- [ ] `C-FE-20` `ui` The fully rounded value is a pill rule rather than a number to copy. `src: Front-end specification, instruction.md`
- [ ] `C-FE-21` `ui` The container is twelve columns above the third tier, eight from the first, four below, with the gutter widening at the large tier. `src: Front-end specification, instruction.md`
- [ ] `C-FE-22` `ui` Chrome carries at most a hairline ring plus a shallow ambient shadow. `src: Front-end specification, instruction.md`
- [ ] `C-FE-23` `ui` A dark pill carries a one-pixel top highlight inset, so the pill does not read as a hole. `src: Front-end specification, instruction.md`
- [ ] `C-FE-24` `ui` A scrim leaves its first four tenths untouched, so the image still reads. `src: Front-end specification, instruction.md`
- [ ] `C-FE-25` `ui` Radial glows are sized in container query units, scaling with their section rather than the window. `src: Front-end specification, instruction.md`
- [ ] `C-FE-26` `ui` Text gradients keep their odd angles, their odd stop positions, unrounded. `src: Front-end specification, instruction.md`
- [ ] `C-FE-27` `ui` A conic sweep lights a card edge, driving the border glow. `src: Front-end specification, instruction.md`
- [ ] `C-FE-28` `ui` A section-level dark wash is interpolated perceptually, so its violet does not pass through grey. `src: Front-end specification, instruction.md`
- [ ] `C-FE-29` `ui` Every control declares all of its state colours rather than letting any inherit. `src: Front-end specification, instruction.md`
- [ ] `C-FE-30` `ui` Control state axes are ground, emphasis, interaction, each declaring text, background, border, ring. `src: Front-end specification, instruction.md`
- [ ] `C-FE-31` `ui` Focus is a two-pixel outline at a two-pixel offset on focus-visible, never suppressed. `src: Front-end specification, instruction.md`
- [ ] `C-FE-32` `ui` Controls transition colour, background colour, border colour, outline colour together on the shared easing. `src: Front-end specification, instruction.md`
- [ ] `C-FE-33` `ui` A section declares a colour scheme; every token inside resolves against that scheme. `src: Front-end specification, instruction.md`
- [ ] `C-FE-34` `ui` A component never tests which scheme the component is in, consuming the scheme's tokens instead. `src: Front-end specification, instruction.md`
- [ ] `C-FE-35` `ui` Every icon is drawn from coordinates, so no icon file ships. `src: Front-end specification, instruction.md`
- [ ] `C-FE-36` `ui` Icons are drawn at a twenty-unit square box, stroked with the current colour, sized by a class on the element. `src: Front-end specification, instruction.md`
- [ ] `C-FE-37` `ui` Every directional icon carries a right-to-left mirror rule. `src: Front-end specification, instruction.md`
- [ ] `C-FE-38` `ui` A decorative icon is removed from the accessibility tree, with a labelled sibling carrying the name. `src: Front-end specification, instruction.md`
- [ ] `C-FE-39` `ui` The icon set covers arrow, chevron, check, close, play, search, globe, caret, minus, plus, sparkle, speech bubble, analytics bars, rocket, terminal, rule, card, tag, chat bubble, cube, chevrons mark, person. `src: Front-end specification, instruction.md`
- [ ] `C-FE-40` `ui` The assistant sparkle is painted twice, once filled, once stroked, keeping the glow as two stacked paints. `src: Front-end specification, instruction.md`
- [ ] `C-FE-41` `ui` The brand wordmark is set in the display family, converted to outlines, beside a bag glyph of one rounded rectangle plus one handle arc. `src: Front-end specification, instruction.md`
- [ ] `C-FE-42` `ui` The inline link arrow rests just before where the arrow belongs, sliding into place on the group's hover, sized in ems. `src: Front-end specification, instruction.md`
- [ ] `C-FE-43` `ui` The plus, the minus occupy the same absolute centre, cross-fading rather than swapping. `src: Front-end specification, instruction.md`
- [ ] `C-FE-44` `ui` The mega-menu chevron flips by scaling on the vertical axis rather than rotating. `src: Front-end specification, instruction.md`
- [ ] `C-FE-45` `ui` The storefront ships main, upmarket, enterprise, retail, editorial chromes, each with its own navigation tree. `src: Front-end specification, instruction.md`
- [ ] `C-FE-46` `ui` The enterprise chrome is the only chrome inverting on scroll. `src: Front-end specification, instruction.md`
- [ ] `C-FE-47` `ui` Chrome is selected by route group at render time, correct in the first byte of markup. `src: Front-end specification, instruction.md`
- [ ] `C-FE-48` `ui` The skip control is the first focusable element, labelled `Skip to Content`, parked by a transform. `src: Front-end specification, instruction.md`
- [ ] `C-FE-49` `ui` The mega menu is operable from the keyboard with no script at all. `src: Front-end specification, instruction.md`
- [ ] `C-FE-50` `ui` A level-two group heading's fade is delayed behind its movement, so the heading reads as arriving. `src: Front-end specification, instruction.md`
- [ ] `C-FE-51` `ui` The footer carries five columns, present, identical on every route. `src: Front-end specification, instruction.md`
- [ ] `C-FE-52` `ui` Below the large tier an open panel traps focus, returning focus to the trigger on close. `src: Front-end specification, instruction.md`
- [ ] `C-FE-53` `ui` Body scroll is locked for an open small-width panel, with scroll chaining prevented. `src: Front-end specification, instruction.md`
- [ ] `C-FE-54` `ui` Exactly one persistent floating control appears per route. `src: Front-end specification, instruction.md`
- [ ] `C-FE-55` `ui` The floating control is the last element in the tab order, never overlapping the primary action, dismissible for the session. `src: Front-end specification, instruction.md`
- [ ] `C-FE-56` `ui` Custom properties are animated rather than positions, so one animation drives a mask, a filter, a translate in step. `src: Front-end specification, instruction.md`
- [ ] `C-FE-57` `ui` Percentage keyframes carry holds, because the hold is the readable part of an animation. `src: Front-end specification, instruction.md`
- [ ] `C-FE-58` `ui` The rotating headline is clipped vertically, never horizontally, with the top, bottom edges softened. `src: Front-end specification, instruction.md`
- [ ] `C-FE-59` `ui` The border glow is masked by a two-layer mask painting only the one-pixel border ring. `src: Front-end specification, instruction.md`
- [ ] `C-FE-60` `ui` The category underline wipes in from the inline start with bleed below, so the stroke is not clipped. `src: Front-end specification, instruction.md`
- [ ] `C-FE-61` `ui` The spotlight reveal keeps its filter chain intact, because the intermediate steps are not redundant. `src: Front-end specification, instruction.md`
- [ ] `C-FE-62` `ui` The mouse spotlight writes custom properties on pointer move rather than inline style strings. `src: Front-end specification, instruction.md`
- [ ] `C-FE-63` `ui` The mouse spotlight handler never reads layout on move. `src: Front-end specification, instruction.md`
- [ ] `C-FE-64` `ui` A marquee's duration is computed from its own track width divided by a constant speed. `src: Front-end specification, instruction.md`
- [ ] `C-FE-65` `ui` Marquee edges are treated with a mask rather than a fade overlay, because a mask works over any ground. `src: Front-end specification, instruction.md`
- [ ] `C-FE-66` `ui` Under reduced motion a marquee container becomes scrollable, with the track wrapping into a list. `src: Front-end specification, instruction.md`
- [ ] `C-FE-67` `ui` Width, height, top, left, margin, padding never animate. `src: Front-end specification, instruction.md`
- [ ] `C-FE-68` `ui` No more than three infinite animations run inside one viewport height. `src: Front-end specification, instruction.md`
- [ ] `C-FE-69` `ui` Scroll-linked work is budgeted per route rather than spread across every route. `src: Front-end specification, instruction.md`
- [ ] `C-FE-70` `ui` The enterprise composed sequence is expressed declaratively so the sequence can run off the main thread. `src: Front-end specification, instruction.md`
- [ ] `C-FE-71` `ui` Where scroll-linked timelines are unsupported the sequence falls back to an intersection-triggered play. `src: Front-end specification, instruction.md`
- [ ] `C-FE-72` `ui` The composed sequence never falls back to a scroll handler writing styles per frame. `src: Front-end specification, instruction.md`
- [ ] `C-FE-73` `ui` Scroll anchoring stays on, so content arriving late does not push the reading position. `src: Front-end specification, instruction.md`
- [ ] `C-FE-74` `ui` Scroll position restores on back navigation. `src: Front-end specification, instruction.md`
- [ ] `C-FE-75` `ui` A sticky sub-navigation is offset by the header height, never overlapping the header. `src: Front-end specification, instruction.md`
- [ ] `C-FE-76` `ui` Landing on a hash scrolls with the header height subtracted, moving focus to the target. `src: Front-end specification, instruction.md`
- [ ] `C-FE-77` `ui` Under reduced motion hash entry jumps rather than gliding. `src: Front-end specification, instruction.md`
- [ ] `C-FE-78` `ui` A product graphic is data plus a layout rather than a hand-positioned pile. `src: Front-end specification, instruction.md`
- [ ] `C-FE-79` `ui` A product graphic's text is real text in the accessibility tree, or the composition carries a text alternative. `src: Front-end specification, instruction.md`
- [ ] `C-FE-80` `ui` One ambient loop is the maximum per product graphic. `src: Front-end specification, instruction.md`
- [ ] `C-FE-81` `ui` A product graphic outside the viewport runs nothing, starting on entry, stopping on exit. `src: Front-end specification, instruction.md`
- [ ] `C-FE-82` `ui` A product graphic that fails to initialise renders its still composition rather than a gap. `src: Front-end specification, instruction.md`
- [ ] `C-FE-83` `ui` The order-management graphic draws its own loading state as skeleton rows below the fold. `src: Front-end specification, instruction.md`
- [ ] `C-FE-84` `ui` The wallet glass keeps its seven-stop mask, which is the difference between glass, a grey rectangle. `src: Front-end specification, instruction.md`
- [ ] `C-FE-85` `ui` The symbol field's mask origin sits off centre, so the field does not read as a vignette. `src: Front-end specification, instruction.md`
- [ ] `C-FE-86` `ui` The workflow canvas vocabulary of trigger, condition, then, otherwise, action, output is normative. `src: Front-end specification, instruction.md`
- [ ] `C-FE-87` `ui` The country home runs eleven sections in a fixed order from hero to closing. `src: Front-end specification, instruction.md`
- [ ] `C-FE-88` `ui` The statement band's four clauses read as one sentence with no pointer at all. `src: Front-end specification, instruction.md`
- [ ] `C-FE-89` `ui` The statement band's clauses are focusable. `src: Front-end specification, instruction.md`
- [ ] `C-FE-90` `ui` The closing section numbers three steps with the numerals in the accent teal. `src: Front-end specification, instruction.md`
- [ ] `C-FE-91` `ui` Media blocked or motion reduced renders the hero's first frame as a generated still with the play control present. `src: Front-end specification, instruction.md`
- [ ] `C-FE-92` `ui` A partial content service may omit any section, preserving the order of the remainder with no gap. `src: Front-end specification, instruction.md`
- [ ] `C-FE-93` `ui` Every hover-only affordance has a focus equivalent. `src: Front-end specification, instruction.md`
- [ ] `C-FE-94` `ui` In print, hero media is replaced by its still, with ambient graphics rendering their end state. `src: Front-end specification, instruction.md`
- [ ] `C-FE-95` `ui` An included comparison cell carries the accessible name `Included`; a missing cell renders `Not included`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-96` `ui` The comparison table becomes a one-plan-at-a-time view at the narrowest tier with row labels fixed. `src: Front-end specification, instruction.md`
- [ ] `C-FE-97` `ui` A withdrawn plan disappears from the table entirely rather than rendering as unavailable. `src: Front-end specification, instruction.md`
- [ ] `C-FE-98` `ui` An unavailable currency falls back to the country's official currency rather than another country's. `src: Front-end specification, instruction.md`
- [ ] `C-FE-99` `ui` An unreachable price service serves the last edge copy with its age, otherwise a sales path with no numbers. `src: Front-end specification, instruction.md`
- [ ] `C-FE-100` `ui` The capability template runs eyebrow, hero, optional proof, optional sub-navigation, feature pairs, optional grid, optional evidence, optional questions, closing band, footnotes. `src: Front-end specification, instruction.md`
- [ ] `C-FE-101` `ui` The sticky sub-navigation's active item follows the section occupying the middle of the viewport by intersection. `src: Front-end specification, instruction.md`
- [ ] `C-FE-102` `ui` The customer-evidence tab set is a real tab pattern with arrow-key movement, a labelled panel, one tab in the tab order. `src: Front-end specification, instruction.md`
- [ ] `C-FE-103` `ui` An animating evidence panel is not removed from the accessibility tree. `src: Front-end specification, instruction.md`
- [ ] `C-FE-104` `ui` The enterprise counters keep their final value in a visually hidden sibling, so the announced number is the true one. `src: Front-end specification, instruction.md`
- [ ] `C-FE-105` `ui` Under reduced motion the enterprise counters render their final value immediately. `src: Front-end specification, instruction.md`
- [ ] `C-FE-106` `ui` The comparison bars, the gauge are data, each carrying a table alternative in the accessibility tree. `src: Front-end specification, instruction.md`
- [ ] `C-FE-107` `ui` Questions render as a disclosure list rather than an accordion closing its siblings. `src: Front-end specification, instruction.md`
- [ ] `C-FE-108` `ui` A disclosure answer sits in the document at first render, hidden by a style rule rather than absent. `src: Front-end specification, instruction.md`
- [ ] `C-FE-109` `ui` The locale control works as a form with a submit control when scripting is unavailable. `src: Front-end specification, instruction.md`
- [ ] `C-FE-110` `ui` The locale control announces the destination before navigating. `src: Front-end specification, instruction.md`
- [ ] `C-FE-111` `ui` A language not published never appears in the locale control for that country. `src: Front-end specification, instruction.md`
- [ ] `C-FE-112` `ui` With client scripting unavailable the mega menu falls back to a disclosure per top-level item. `src: Front-end specification, instruction.md`
- [ ] `C-FE-113` `ui` With client scripting unavailable marquees render as static wrapped lists. `src: Front-end specification, instruction.md`
- [ ] `C-FE-114` `ui` Headings, controls are sentence case; eyebrows are uppercase with loose tracking. `src: Front-end specification, instruction.md`
- [ ] `C-FE-115` `ui` No typographic dash appears in any shipped string. `src: Front-end specification, instruction.md`
- [ ] `C-FE-116` `ui` The second-language surface is a full translation covering chrome, hero copy, every call to action. `src: Front-end specification, instruction.md`
- [ ] `C-FE-117` `ui` No binary asset of any kind ships. `src: Front-end specification, instruction.md`
- [ ] `C-FE-118` `ui` A generator's output is a pure function of a seed derived from the resource identifier. `src: Front-end specification, instruction.md`
- [ ] `C-FE-119` `ui` A generator fills the box the generator is given exactly, so no layout shift occurs. `src: Front-end specification, instruction.md`
- [ ] `C-FE-120` `ui` A generator runs at build time for static content, at first request with a cache otherwise. `src: Front-end specification, instruction.md`
- [ ] `C-FE-121` `ui` Every generated image carries alternative text derived from its resource. `src: Front-end specification, instruction.md`
- [ ] `C-FE-122` `ui` Generators sit behind one interface, so swapping in real media is a configuration change. `src: Front-end specification, instruction.md`
- [ ] `C-FE-123` `ui` Generated media is visually distinguishable from real photography on close inspection. `src: Front-end specification, instruction.md`
- [ ] `C-FE-124` `ui` Grain is an inline fractal-noise filter, desaturated, applied as an overlay at very low opacity. `src: Front-end specification, instruction.md`
- [ ] `C-FE-125` `ui` Portraits are never generated as a face, rendering a circular monogram instead. `src: Front-end specification, instruction.md`
- [ ] `C-FE-126` `ui` Merchant storefront thumbnails are miniature compositions reading as a website rather than an abstraction. `src: Front-end specification, instruction.md`
- [ ] `C-FE-127` `ui` The globe is projected from a coarse coastline polygon set held as a coordinate list in source. `src: Front-end specification, instruction.md`
- [ ] `C-FE-128` `ui` Globe merchant lights are placed by rejection sampling weighted by a density field. `src: Front-end specification, instruction.md`
- [ ] `C-FE-129` `ui` Any globe rotation stops entirely under reduced motion. `src: Front-end specification, instruction.md`
- [ ] `C-FE-130` `ui` Fonts are named rather than shipped, preloaded, subset per script. `src: Front-end specification, instruction.md`
- [ ] `C-FE-131` `ui` The second-language surface loads its own subset rather than a superset. `src: Front-end specification, instruction.md`
- [ ] `C-FE-132` `ui` Marks are outlines rather than files, with each logo-wall name set in a distinct family. `src: Front-end specification, instruction.md`
- [ ] `C-FE-133` `ui` Payment method marks are never reproduced, rendering as a rounded rectangle with a two-letter code. `src: Front-end specification, instruction.md`
- [ ] `C-FE-134` `ui` Hero motion backgrounds are a generated canvas loop whose first frame becomes the poster. `src: Front-end specification, instruction.md`
- [ ] `C-FE-135` `ui` Four things cannot be substituted: filmed footage, photographed merchants, payload easing, the licensed display family. `src: Front-end specification, instruction.md`
- [ ] `C-FE-136` `ui` Primitives cover button, link, icon, image, input, select, toggle, modal, accordion, card, heading, message. `src: Front-end specification, instruction.md`
- [ ] `C-FE-137` `ui` Compositions cover card grid, slideshow, stats cards, testimonial, section heading, logo group, marquee, tab set, disclosure list. `src: Front-end specification, instruction.md`
- [ ] `C-FE-138` `ui` A section knows nothing about its neighbouring sections, enforced by an error boundary. `src: Front-end specification, instruction.md`
- [ ] `C-FE-139` `ui` The index framework is written once, used by every admin index. `src: Front-end specification, instruction.md`
- [ ] `C-FE-140` `ui` Route state covering filters, sort, scope, page, selected tab lives in the address. `src: Front-end specification, instruction.md`
- [ ] `C-FE-141` `ui` Server state is cached query results with explicit invalidation, never mirrored into a client store. `src: Front-end specification, instruction.md`
- [ ] `C-FE-142` `ui` Draft state is persisted per resource, cleared on a successful save. `src: Front-end specification, instruction.md`
- [ ] `C-FE-143` `ui` The theme editor, the workflow canvas keep a command stack of invertible commands rather than a state snapshot. `src: Front-end specification, instruction.md`
- [ ] `C-FE-144` `ui` A destructive action whose effect leaves the system gets a confirmation rather than an undo. `src: Front-end specification, instruction.md`
- [ ] `C-FE-145` `ui` Focus order follows reading order, with a visual reorder accompanied by a source reorder. `src: Front-end specification, instruction.md`
- [ ] `C-FE-146` `ui` Focus is never trapped except inside a modal or an open panel, where escape releases the trap. `src: Front-end specification, instruction.md`
- [ ] `C-FE-147` `ui` On navigation focus moves to the main heading, with the route change announced. `src: Front-end specification, instruction.md`
- [ ] `C-FE-148` `ui` Tab sets move by arrow keys, jump by home, end, with only the active tab in the tab order. `src: Front-end specification, instruction.md`
- [ ] `C-FE-149` `ui` Table row selection uses space to select, shift to extend, with select-all stating the covered rows. `src: Front-end specification, instruction.md`
- [ ] `C-FE-150` `ui` The terminal is touch-first, with every function also reachable from an attached keyboard. `src: Front-end specification, instruction.md`
- [ ] `C-FE-151` `ui` Every drag has a command equivalent, so a drag is never the only path. `src: Front-end specification, instruction.md`
- [ ] `C-FE-152` `ui` Live regions carry asynchronous result counts, price changes, save confirmations, scope changes, polite by default. `src: Front-end specification, instruction.md`
- [ ] `C-FE-153` `ui` Landmarks are one main, one banner, one contentinfo, with navigation landmarks named where more than one exists. `src: Front-end specification, instruction.md`
- [ ] `C-FE-154` `ui` Modals trap focus, return focus, close on escape, make the underlying page inert, lock page scroll. `src: Front-end specification, instruction.md`
- [ ] `C-FE-155` `ui` Body text meets `4.5:1` against its ground; large text meets `3:1`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-156` `ui` Control boundaries, focus rings, meaningful graphics meet `3:1`. `src: Front-end specification, instruction.md`
- [ ] `C-FE-157` `ui` High contrast mode is respected, with the design never depending on a background image to convey anything. `src: Front-end specification, instruction.md`
- [ ] `C-FE-158` `ui` Tables use real table semantics with a header row plus scoped headers. `src: Front-end specification, instruction.md`
- [ ] `C-FE-159` `ui` A sortable column announces its sort state, with the control a button inside the header. `src: Front-end specification, instruction.md`
- [ ] `C-FE-160` `ui` A wide table's container is focusable, so a keyboard user can scroll one. `src: Front-end specification, instruction.md`
- [ ] `C-FE-161` `ui` Where a table becomes cards the association between label, value is preserved. `src: Front-end specification, instruction.md`
- [ ] `C-FE-162` `ui` Every chart carries an equivalent table in the accessibility tree or a text summary. `src: Front-end specification, instruction.md`
- [ ] `C-FE-163` `ui` The theme editor outline pane is a real tree with arrow movement, home, end jumps, type-ahead selection. `src: Front-end specification, instruction.md`
- [ ] `C-FE-164` `ui` The workflow graph has a linear equivalent navigable, editable without a pointer. `src: Front-end specification, instruction.md`
- [ ] `C-FE-165` `ui` Editor selection is announced with the selected node's type, position stated. `src: Front-end specification, instruction.md`
- [ ] `C-FE-166` `ui` Layout survives `200%` text scaling, `400%` page zoom at a `1280px` viewport. `src: Front-end specification, instruction.md`
- [ ] `C-FE-167` `ui` Voice control works because a control's accessible name matches its visible label. `src: Front-end specification, instruction.md`
- [ ] `C-FE-168` `ui` Fulfilment surfaces are designed small-width first, so picking, label printing, stock adjustment are one-handed. `src: Front-end specification, instruction.md`
- [ ] `C-FE-169` `ui` Terminal touch targets are at least `44px` on the shorter axis, with controls in the lower half of the screen. `src: Front-end specification, instruction.md`
- [ ] `C-FE-170` `ui` The terminal carries no hover-dependent affordance anywhere. `src: Front-end specification, instruction.md`
- [ ] `C-FE-171` `ui` Buyer surfaces are small-width first without qualification. `src: Front-end specification, instruction.md`
- [ ] `C-FE-172` `ui` Long words wrap with an explicit break rule. `src: Front-end specification, instruction.md`
- [ ] `C-FE-173` `ui` Compositions size their internal proportions in container query units rather than viewport units. `src: Front-end specification, instruction.md`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The application is server-rendered, progressively enhanced, so every route arrives as complete markup. `src: Technical requirements, instruction.md`
- [ ] `C-TR-02` `contract` Scripting adds behaviour on top of a working page rather than making the page work. `src: Technical requirements, instruction.md`
- [ ] `C-TR-03` `contract` The backend is Django with its template layer, serving every surface from one process. `src: Technical requirements, instruction.md`
- [ ] `C-TR-04` `contract` The front end is Alpine.js over server-rendered templates. `src: Technical requirements, instruction.md`
- [ ] `C-TR-05` `contract` Storage is PostgreSQL, reached at `DATABASE_URL`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-06` `contract` Identity is Keycloak, reached at `AUTH_ISSUER_URL` with `AUTH_CLIENT_ID`, `AUTH_CLIENT_SECRET`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-07` `contract` Every host, every port is read from the environment rather than hardcoded. `src: Technical requirements, instruction.md`
- [ ] `C-TR-08` `contract` Both backing services are already running, so neither is downloaded, installed, compiled, nor started. `src: Technical requirements, instruction.md`
- [ ] `C-TR-09` `constraint` Only the named libraries plus their direct dependencies are used. `src: Technical requirements, instruction.md`
- [ ] `C-TR-10` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements, instruction.md`
- [ ] `C-TR-11` `contract` Authentication is an authorization-code flow with proof key against the issuer. `src: Technical requirements, instruction.md`
- [ ] `C-TR-12` `contract` Machine callers present an installation token in a header rather than in a query parameter. `src: Technical requirements, instruction.md`
- [ ] `C-TR-13` `contract` The endpoint `GET /api/health` returns `200` once the app is ready. `src: Technical requirements, instruction.md`
- [ ] `C-TR-14` `constraint` Policy decision, price resolution, money arithmetic, the tenancy predicate, the idempotency store, the audit writer each exist exactly once. `src: Technical requirements, instruction.md`
- [ ] `C-TR-15` `constraint` Transport parses, validates shape, doing nothing else. `src: Technical requirements, instruction.md`
- [ ] `C-TR-16` `constraint` The application layer owns the transaction boundary, writing the audit entry plus the outbox row inside one transaction. `src: Technical requirements, instruction.md`
- [ ] `C-TR-17` `constraint` The domain layer is pure, taking its clock by injection. `src: Technical requirements, instruction.md`
- [ ] `C-TR-18` `constraint` No repository opens its own transaction. `src: Technical requirements, instruction.md`
- [ ] `C-TR-19` `constraint` Deployable units split by failure domain, by change cadence, rather than by noun. `src: Technical requirements, instruction.md`
- [ ] `C-TR-20` `contract` A graph interface serves the admin surface, the storefront surface; a resource interface serves webhooks, bulk operations, file handling. `src: Technical requirements, instruction.md`
- [ ] `C-TR-21` `contract` Interface versions are dated, at least four supported at once, each for at least twelve months. `src: Technical requirements, instruction.md`
- [ ] `C-TR-22` `contract` A deprecation notice appears in the response headers for the oldest supported version. `src: Technical requirements, instruction.md`
- [ ] `C-TR-23` `constraint` Removing a field, narrowing a type, adding a required argument, changing an enumeration's meaning are all breaking changes. `src: Technical requirements, instruction.md`
- [ ] `C-TR-24` `contract` Identifiers are opaque, globally unique, type-prefixed, sortable by creation, never a bare integer. `src: Technical requirements, instruction.md`
- [ ] `C-TR-25` `contract` Pagination is cursor-based only. `src: Technical requirements, instruction.md`
- [ ] `C-TR-26` `contract` An error carries a stable machine code, a human message, a path to the offending field, a retryability flag. `src: Technical requirements, instruction.md`
- [ ] `C-TR-27` `contract` An unknown field in a request is rejected rather than ignored. `src: Technical requirements, instruction.md`
- [ ] `C-TR-28` `contract` Three machine surfaces exist: admin under an installation token, storefront under a public credential, partner under a partner credential. `src: Technical requirements, instruction.md`
- [ ] `C-TR-29` `constraint` The same policy component authorizes all three machine surfaces. `src: Technical requirements, instruction.md`
- [ ] `C-TR-30` `constraint` A field outside the credential's scopes is absent from the response rather than null. `src: Technical requirements, instruction.md`
- [ ] `C-TR-31` `constraint` Every validation rule exists at the last layer able to express one, duplicated upward only for a better message. `src: Technical requirements, instruction.md`
- [ ] `C-TR-32` `constraint` Money on the wire is an integer in minor units plus a currency; a decimal is rejected rather than coerced. `src: Technical requirements, instruction.md`
- [ ] `C-TR-33` `constraint` A quantity is a non-negative integer, with zero distinct from absent. `src: Technical requirements, instruction.md`
- [ ] `C-TR-34` `constraint` An email address is validated, normalised, never used as a primary key. `src: Technical requirements, instruction.md`
- [ ] `C-TR-35` `constraint` A phone number is stored canonically with its country, with the display form derived. `src: Technical requirements, instruction.md`
- [ ] `C-TR-36` `constraint` A timestamp on the wire always carries a zone offset; a bare local time is rejected. `src: Technical requirements, instruction.md`
- [ ] `C-TR-37` `constraint` Free text is length-bounded, escaped at every output boundary by the renderer rather than at input. `src: Technical requirements, instruction.md`
- [ ] `C-TR-38` `constraint` Rich text is parsed to a document tree at write, stored as that tree, rendered from one. `src: Technical requirements, instruction.md`
- [ ] `C-TR-39` `constraint` An identifier from another system is length-bounded, namespaced, never trusted as unique alone. `src: Technical requirements, instruction.md`
- [ ] `C-TR-40` `constraint` Idempotency is required on every mutating operation moving money, stock, or a message. `src: Technical requirements, instruction.md`
- [ ] `C-TR-41` `constraint` A repeat with the same key plus the same fingerprint returns the stored response with its status. `src: Technical requirements, instruction.md`
- [ ] `C-TR-42` `constraint` A repeat with the same key plus a different fingerprint is an error. `src: Technical requirements, instruction.md`
- [ ] `C-TR-43` `literal` Idempotency keys are retained `7` days. `src: Technical requirements, instruction.md`
- [ ] `C-TR-44` `constraint` A repeat arriving before the first finishes waits, bounded, then returns a retryable error. `src: Technical requirements, instruction.md`
- [ ] `C-TR-45` `capability` A bulk operation returns an operation identifier, producing a durable result artefact fetched afterwards. `src: Technical requirements, instruction.md`
- [ ] `C-TR-46` `constraint` One bulk operation per type per store runs at a time, with a second rejected naming the running one. `src: Technical requirements, instruction.md`
- [ ] `C-TR-47` `constraint` Bulk work never consumes the interactive rate budget, so interactive requests are not starved. `src: Technical requirements, instruction.md`
- [ ] `C-TR-48` `constraint` Rate limiting is cost-based rather than request-based. `src: Technical requirements, instruction.md`
- [ ] `C-TR-49` `constraint` A query whose computed cost exceeds the bucket is rejected before execution with the cost, the wait stated. `src: Technical requirements, instruction.md`
- [ ] `C-TR-50` `constraint` Every rate rejection returns the limit, the remaining budget, the reset instant, a retry-after. `src: Technical requirements, instruction.md`
- [ ] `C-TR-51` `constraint` Caching has an edge layer, an application layer, a data layer, a client layer. `src: Technical requirements, instruction.md`
- [ ] `C-TR-52` `constraint` The storefront cache key is store, market, language, currency, theme version, content version, device class where markup differs. `src: Technical requirements, instruction.md`
- [ ] `C-TR-53` `constraint` The storefront cache key never includes a buyer identifier, a session, a cart, a segment. `src: Technical requirements, instruction.md`
- [ ] `C-TR-54` `constraint` Cache invalidation is event-driven from the outbox, idempotent. `src: Technical requirements, instruction.md`
- [ ] `C-TR-55` `constraint` A missed invalidation is bounded by a maximum stale age, so the worst case is stale rather than permanent. `src: Technical requirements, instruction.md`
- [ ] `C-TR-56` `capability` A slow origin serves stale during revalidation; a down origin serves stale up to a longer emergency window with the age in a header. `src: Technical requirements, instruction.md`
- [ ] `C-TR-57` `constraint` Cart, checkout are never cached, so both must be fast without caching. `src: Technical requirements, instruction.md`
- [ ] `C-TR-58` `literal` Queue classes are `interactive`, `money`, `delivery`, `bulk`, `maintenance`, each with its own worker pool. `src: Technical requirements, instruction.md`
- [ ] `C-TR-59` `constraint` A job survives a process death, so a job held in memory is not a job. `src: Technical requirements, instruction.md`
- [ ] `C-TR-60` `constraint` Job delivery is at-least-once, with every handler idempotent on the job's own identity. `src: Technical requirements, instruction.md`
- [ ] `C-TR-61` `constraint` Where job order matters, jobs for one resource are serialised on a key derived from that resource. `src: Technical requirements, instruction.md`
- [ ] `C-TR-62` `constraint` The visibility window is sized above the handler's timeout. `src: Technical requirements, instruction.md`
- [ ] `C-TR-63` `constraint` A job past its attempt ceiling moves to a dead-letter store with full context, raising an alert, never dropped. `src: Technical requirements, instruction.md`
- [ ] `C-TR-64` `capability` Dead-lettered jobs are inspectable, replayable individually or in bulk. `src: Technical requirements, instruction.md`
- [ ] `C-TR-65` `constraint` Per-store concurrency, throughput are capped per queue, weighted by plan with a floor so no store is starved. `src: Technical requirements, instruction.md`
- [ ] `C-TR-66` `constraint` A job's precedence rises with its age. `src: Technical requirements, instruction.md`
- [ ] `C-TR-67` `constraint` Under sustained overload new bulk work is refused at submission with a retry-after. `src: Technical requirements, instruction.md`
- [ ] `C-TR-68` `capability` Automation runs, bulk operations, event deliveries are metered per store, visible to the merchant. `src: Technical requirements, instruction.md`
- [ ] `C-TR-69` `capability` Scheduled work covers reservation sweeping, authorization expiry, payouts, billing, dunning, four reconciliations, retention, index freshness, dead-letter review. `src: Technical requirements, instruction.md`
- [ ] `C-TR-70` `constraint` Every reconciliation job reports rather than silently repairing. `src: Technical requirements, instruction.md`
- [ ] `C-TR-71` `constraint` Instants are stored with a zone in one canonical zone, database-assigned where the database is the authority. `src: Technical requirements, instruction.md`
- [ ] `C-TR-72` `constraint` A business date is a date plus the store's named timezone rather than an instant. `src: Technical requirements, instruction.md`
- [ ] `C-TR-73` `constraint` Timezones are named zones from the region database rather than offsets. `src: Technical requirements, instruction.md`
- [ ] `C-TR-74` `constraint` A schedule in a skipped local hour runs once at the next valid local instant. `src: Technical requirements, instruction.md`
- [ ] `C-TR-75` `constraint` A schedule in a repeated local hour runs once, on the first occurrence. `src: Technical requirements, instruction.md`
- [ ] `C-TR-76` `constraint` Every signed artefact tolerates a stated clock skew, rejecting outside one with skew named as the cause. `src: Technical requirements, instruction.md`
- [ ] `C-TR-77` `literal` Any operation exceeding `2` seconds produces a progress record with a state, a completion fraction where computable, a result. `src: Technical requirements, instruction.md`
- [ ] `C-TR-78` `constraint` A progress record survives a page reload, a sign-out, a deploy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-79` `constraint` Events are produced from an outbox row written in the same transaction as the state change. `src: Technical requirements, instruction.md`
- [ ] `C-TR-80` `constraint` Nothing publishes an event from a post-commit callback. `src: Technical requirements, instruction.md`
- [ ] `C-TR-81` `constraint` A relay reads unpublished outbox rows in order, marking publication idempotently. `src: Technical requirements, instruction.md`
- [ ] `C-TR-82` `data` An event carries an opaque sortable identifier, store, organisation, environment, a namespaced type, resource, payload, prior values, occurrence instant, a monotonic sequence, a correlation identifier, an actor. `src: Technical requirements, instruction.md`
- [ ] `C-TR-83` `data` A subscription names a target, an explicit type list, an interface version, an optional filter, a signing secret. `src: Technical requirements, instruction.md`
- [ ] `C-TR-84` `constraint` Wildcard subscriptions are not offered. `src: Technical requirements, instruction.md`
- [ ] `C-TR-85` `constraint` A subscription covers only events the installation's scopes permit reading. `src: Technical requirements, instruction.md`
- [ ] `C-TR-86` `constraint` Delivery signs the raw body plus a timestamp, with the subscriber verifying against the raw bytes. `src: Technical requirements, instruction.md`
- [ ] `C-TR-87` `constraint` Deliveries outside the stated replay window are rejected. `src: Technical requirements, instruction.md`
- [ ] `C-TR-88` `constraint` Delivery ordering is per resource, best-effort, with the sequence number as the authority. `src: Technical requirements, instruction.md`
- [ ] `C-TR-89` `literal` Delivery retries back off with jitter over `48` hours on a stated schedule. `src: Technical requirements, instruction.md`
- [ ] `C-TR-90` `literal` Delivery success is any 2xx inside a `5` second timeout. `src: Technical requirements, instruction.md`
- [ ] `C-TR-91` `constraint` A gone response disables a subscription immediately; a client error does not retry beyond a small count. `src: Technical requirements, instruction.md`
- [ ] `C-TR-92` `constraint` A consistently failing target is paused, notifying merchant, partner, without consuming the delivery pool. `src: Technical requirements, instruction.md`
- [ ] `C-TR-93` `contract` At-least-once is the delivery guarantee; exactly-once is not offered. `src: Technical requirements, instruction.md`
- [ ] `C-TR-94` `literal` The event log retains `7` days, queryable by type, resource, instant, delivery outcome. `src: Technical requirements, instruction.md`
- [ ] `C-TR-95` `data` Every delivery attempt is recorded with request headers, response status, a truncated body, latency, the next attempt. `src: Technical requirements, instruction.md`
- [ ] `C-TR-96` `capability` A merchant or a partner may replay an event or a range, with a replayed delivery marked as such. `src: Technical requirements, instruction.md`
- [ ] `C-TR-97` `capability` A merchant sees deliveries for their own store, failures included, without needing the partner. `src: Technical requirements, instruction.md`
- [ ] `C-TR-98` `constraint` An oversized payload is truncated to identifiers plus a fetch address, with the truncation flagged. `src: Technical requirements, instruction.md`
- [ ] `C-TR-99` `constraint` A resource deleted before delivery still delivers with its snapshot. `src: Technical requirements, instruction.md`
- [ ] `C-TR-100` `constraint` There is no backfill for a subscription created after an event. `src: Technical requirements, instruction.md`
- [ ] `C-TR-101` `constraint` Every external call carries a timeout shorter than the caller's own budget. `src: Technical requirements, instruction.md`
- [ ] `C-TR-102` `constraint` Retries apply only to idempotent operations or ones carrying a key, backing off with jitter over a bounded count. `src: Technical requirements, instruction.md`
- [ ] `C-TR-103` `constraint` A circuit opens per integration per store where failure is tenant-specific, globally where failure is not. `src: Technical requirements, instruction.md`
- [ ] `C-TR-104` `constraint` Every mutating outbound call carries a key derived from the platform's own operation identity. `src: Technical requirements, instruction.md`
- [ ] `C-TR-105` `constraint` Integration credentials are encrypted with a key the application cannot export, never logged, never in a query parameter. `src: Technical requirements, instruction.md`
- [ ] `C-TR-106` `constraint` Tokens refresh ahead of expiry under a single-flight guard. `src: Technical requirements, instruction.md`
- [ ] `C-TR-107` `constraint` Every inbound callback verifies a signature over the raw body plus a timestamp before parsing. `src: Technical requirements, instruction.md`
- [ ] `C-TR-108` `constraint` An inbound callback is deduplicated on the sender's own event identifier, stored per integration. `src: Technical requirements, instruction.md`
- [ ] `C-TR-109` `constraint` An inbound callback persists the raw event, then acknowledges, then processes asynchronously. `src: Technical requirements, instruction.md`
- [ ] `C-TR-110` `constraint` A processing failure never turns into a non-acknowledgement of an inbound callback. `src: Technical requirements, instruction.md`
- [ ] `C-TR-111` `constraint` Only the fields an integration needs are sent to one. `src: Technical requirements, instruction.md`
- [ ] `C-TR-112` `constraint` Order placement, its stock decrement, its ledger write are one strongly consistent transaction. `src: Technical requirements, instruction.md`
- [ ] `C-TR-113` `constraint` The audit entry, the action recorded are strongly consistent in the same transaction. `src: Technical requirements, instruction.md`
- [ ] `C-TR-114` `literal` The search index trails the catalog by at most `5` seconds. `src: Technical requirements, instruction.md`
- [ ] `C-TR-115` `constraint` A cross-boundary operation is a saga with explicit compensations rather than a distributed transaction. `src: Technical requirements, instruction.md`
- [ ] `C-TR-116` `constraint` Every compensation is itself idempotent. `src: Technical requirements, instruction.md`
- [ ] `C-TR-117` `constraint` A failed refund call leaves the refund pending, retrying, rather than writing ledger entries speculatively. `src: Technical requirements, instruction.md`
- [ ] `C-TR-118` `constraint` Every degraded state stays visible to the merchant for as long as the degradation lasts. `src: Technical requirements, instruction.md`
- [ ] `C-TR-119` `capability` A failed search index falls back to a bounded database search behind a banner rather than an empty list. `src: Technical requirements, instruction.md`
- [ ] `C-TR-120` `capability` A failed analytics store sends money surfaces to the ledger, marking non-money surfaces stale. `src: Technical requirements, instruction.md`
- [ ] `C-TR-121` `constraint` The primary database is the one dependency with no degradation. `src: Technical requirements, instruction.md`
- [ ] `C-TR-122` `constraint` An offline terminal may sell within a floor, print a receipt, look up a cached product. `src: Technical requirements, instruction.md`
- [ ] `C-TR-123` `constraint` An offline terminal performs no authorization-sensitive action of any kind. `src: Technical requirements, instruction.md`
- [ ] `C-TR-124` `constraint` An offline terminal queue is durable, ordered, encrypted at rest, with a maximum age. `src: Technical requirements, instruction.md`
- [ ] `C-TR-125` `constraint` A reconnecting terminal applies transactions in order, each idempotent on a device-generated key. `src: Technical requirements, instruction.md`
- [ ] `C-TR-126` `constraint` A resulting negative level after reconnect surfaces as a discrepancy rather than being clamped. `src: Technical requirements, instruction.md`
- [ ] `C-TR-127` `constraint` A revoked device credential stops its queue submitting, surfacing the queued transactions for reconciliation. `src: Technical requirements, instruction.md`
- [ ] `C-TR-128` `constraint` Schema changes expand, migrate, then contract across separate releases. `src: Technical requirements, instruction.md`
- [ ] `C-TR-129` `constraint` A deploy is safe with the previous version still running. `src: Technical requirements, instruction.md`
- [ ] `C-TR-130` `capability` Feature flags exist per store, per organisation, with a kill switch, with flag state visible in the audit. `src: Technical requirements, instruction.md`
- [ ] `C-TR-131` `capability` Rollout is progressive by store cohort with automatic rollback on a metric breach. `src: Technical requirements, instruction.md`
- [ ] `C-TR-132` `constraint` Data backfills are resumable rate-limited jobs, never run inside a deploy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-133` `literal` Recovery targets are `5` minutes for transactional data, zero for the ledger, `1` hour for storefront, `4` hours for the admin. `src: Technical requirements, instruction.md`
- [ ] `C-TR-134` `constraint` Backups are continuous, encrypted, in region, with restore rehearsed rather than assumed. `src: Technical requirements, instruction.md`
- [ ] `C-TR-135` `constraint` The money store fails over last, because a split-brain ledger is worse than an hour of downtime. `src: Technical requirements, instruction.md`
- [ ] `C-TR-136` `constraint` A status surface is hosted independently of the platform the surface reports on. `src: Technical requirements, instruction.md`
- [ ] `C-TR-137` `data` Structured logs are one event per line carrying correlation identifier, store, actor, outcome, never a personal field. `src: Technical requirements, instruction.md`
- [ ] `C-TR-138` `constraint` The store identifier is never a metric label. `src: Technical requirements, instruction.md`
- [ ] `C-TR-139` `constraint` One correlation identifier propagates through request, transaction, audit entry, outbox row, event, job, outbound call, approval, log line. `src: Technical requirements, instruction.md`
- [ ] `C-TR-140` `ui` The correlation identifier is surfaced on every error screen, in every error response. `src: Technical requirements, instruction.md`
- [ ] `C-TR-141` `capability` Explainability surfaces answer why an order routed, why a price applies, why an order is held, why an action was refused, why a message was not sent, why a workflow fired, why a delivery failed, why a closed figure changed. `src: Technical requirements, instruction.md`
- [ ] `C-TR-142` `literal` Outbox relay lag stays under `5` seconds, alerting loudly above `60`. `src: Technical requirements, instruction.md`
- [ ] `C-TR-143` `constraint` Ledger reconciliation is exact, with any difference at all paging somebody. `src: Technical requirements, instruction.md`
- [ ] `C-TR-144` `constraint` Inventory reconciliation drift is zero, with any drift raising a ticket naming item, magnitude. `src: Technical requirements, instruction.md`
- [ ] `C-TR-145` `constraint` Any audit chain break pages at the loudest level. `src: Technical requirements, instruction.md`
- [ ] `C-TR-146` `constraint` Every alert is actionable, has an owner, has a runbook. `src: Technical requirements, instruction.md`
- [ ] `C-TR-147` `capability` Per-merchant health covers integration health per channel, per application, delivery success, failing automations, degraded capabilities. `src: Technical requirements, instruction.md`
- [ ] `C-TR-148` `ui` An error shown to a person says what happened, whether the person can fix one, what to do next. `src: Technical requirements, instruction.md`
- [ ] `C-TR-149` `ui` An error states retryability, offering another attempt only where retrying can succeed. `src: Technical requirements, instruction.md`
- [ ] `C-TR-150` `constraint` An error never loses what the user typed. `src: Technical requirements, instruction.md`
- [ ] `C-TR-151` `literal` Storefront budgets are `2.5s` largest contentful paint, `200ms` interaction to next paint, `0.1` layout shift. `src: Technical requirements, instruction.md`
- [ ] `C-TR-152` `literal` Storefront byte budgets are `200ms` cached first byte, `600ms` uncached, `120KB` route script, `60KB` stylesheet. `src: Technical requirements, instruction.md`
- [ ] `C-TR-153` `literal` Merchant storefront budgets are `2.0s` largest contentful paint, `300ms` median server render, above `90%` edge hit ratio, `70KB` theme script. `src: Technical requirements, instruction.md`
- [ ] `C-TR-154` `capability` A per-store third-party script budget names the offending application to the merchant when exceeded. `src: Technical requirements, instruction.md`
- [ ] `C-TR-155` `literal` Admin budgets are `1.0s` shell paint, `1.5s` index first row, `300ms` index query, `1.2s` detail page, `150ms` command surface, `5s` search freshness, `500ms` save round trip. `src: Technical requirements, instruction.md`
- [ ] `C-TR-156` `literal` Checkout budgets are `1.5s` first step interactive, `400ms` step transition, `3s` payment submit to result. `src: Technical requirements, instruction.md`
- [ ] `C-TR-157` `constraint` Every list carries a server-enforced limit rather than an offered one. `src: Technical requirements, instruction.md`
- [ ] `C-TR-158` `constraint` Batched loading covers every association on every list surface. `src: Technical requirements, instruction.md`
- [ ] `C-TR-159` `constraint` Authorization is applied inside the query rather than after the fetch. `src: Technical requirements, instruction.md`
- [ ] `C-TR-160` `constraint` Every hot-path query has a covering index, with a plan regression failing the build. `src: Technical requirements, instruction.md`
- [ ] `C-TR-161` `constraint` A read inside a write transaction uses the primary rather than a replica. `src: Technical requirements, instruction.md`
- [ ] `C-TR-162` `constraint` A surface reading after its own write reads the primary. `src: Technical requirements, instruction.md`
- [ ] `C-TR-163` `literal` Any list beyond `200` rows renders only what is on screen. `src: Technical requirements, instruction.md`
- [ ] `C-TR-164` `constraint` The theme editor, the workflow canvas are never in the initial payload of anything else. `src: Technical requirements, instruction.md`
- [ ] `C-TR-165` `constraint` No handler reads layout then writes layout inside a scroll or pointer handler. `src: Technical requirements, instruction.md`
- [ ] `C-TR-166` `constraint` Images below the fold load lazily with an explicit box; the one above loads eagerly, preloaded. `src: Technical requirements, instruction.md`
- [ ] `C-TR-167` `literal` Volume targets are `1,000,000` products, `2,000` variants per product, `250,000` orders a day, `200` locations, `100,000` companies, `5,000,000` events a day, `20,000` concurrent checkouts. `src: Technical requirements, instruction.md`
- [ ] `C-TR-168` `constraint` A budget breach fails the build. `src: Technical requirements, instruction.md`
- [ ] `C-TR-169` `constraint` Tenancy is enforced three times over, with a generated suite covering the cross-tenant read. `src: Technical requirements, instruction.md`
- [ ] `C-TR-170` `constraint` No state-changing request is ever a safe method. `src: Technical requirements, instruction.md`
- [ ] `C-TR-171` `constraint` Checkout runs no merchant script under the strictest content policy in the build. `src: Technical requirements, instruction.md`
- [ ] `C-TR-172` `constraint` Responses for existing, non-existing accounts are identical, so enumeration is refused. `src: Technical requirements, instruction.md`
- [ ] `C-TR-173` `constraint` Dependencies are pinned by hash, with a generated bill of materials, provenance, no post-install scripts. `src: Technical requirements, instruction.md`
- [ ] `C-TR-174` `constraint` Support access is scoped, time-boxed, justified, region-limited, separately audited. `src: Technical requirements, instruction.md`
- [ ] `C-TR-175` `constraint` The platform's general services stay out of the card-data environment. `src: Technical requirements, instruction.md`
- [ ] `C-TR-176` `constraint` No primary account number is stored in any store, log, backup, or analytics record. `src: Technical requirements, instruction.md`
- [ ] `C-TR-177` `constraint` Card display is brand, last four, expiry only. `src: Technical requirements, instruction.md`
- [ ] `C-TR-178` `constraint` The payment layer is network-segmented, separately deployed, separately access-controlled, separately logged. `src: Technical requirements, instruction.md`
- [ ] `C-TR-179` `constraint` Secrets live in a managed store, never in source, never in a committed environment file, never in an image. `src: Technical requirements, instruction.md`
- [ ] `C-TR-180` `constraint` One secret exists per purpose per environment. `src: Technical requirements, instruction.md`
- [ ] `C-TR-181` `constraint` Personal-data encryption keys are per organisation, held in the organisation's region, never exportable. `src: Technical requirements, instruction.md`
- [ ] `C-TR-182` `constraint` A secret scanner runs in the build, over the repository history, failing the build plus triggering rotation on a hit. `src: Technical requirements, instruction.md`
- [ ] `C-TR-183` `constraint` Rich text renders from a parsed tree, with an unknown node type rendering as nothing. `src: Technical requirements, instruction.md`
- [ ] `C-TR-184` `constraint` Merchant-supplied templates render through an engine with no arbitrary execution plus a declared data contract. `src: Technical requirements, instruction.md`
- [ ] `C-TR-185` `capability` Vulnerability management covers dependency scanning, static analysis, dynamic scanning, penetration testing, disclosure, incident response. `src: Technical requirements, instruction.md`
- [ ] `C-TR-186` `constraint` No credential, API key, or admin token appears in anything the browser downloads. `src: Technical requirements, instruction.md`
- [ ] `C-TR-187` `constraint` Every response carries the standard security headers, a strict transport policy, a nosniff content-type policy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-188` `constraint` Every public route carries its own title plus its own description, with no two public routes sharing them. `src: Technical requirements, instruction.md`
- [ ] `C-TR-189` `contract` A sitemap lists every public route; a robots file names the sitemap. `src: Technical requirements, instruction.md`
- [ ] `C-TR-190` `constraint` The interface schema is generated from the implementation rather than hand-maintained. `src: Technical requirements, instruction.md`
- [ ] `C-TR-191` `capability` Every operation carries a runnable example against a development store. `src: Technical requirements, instruction.md`
- [ ] `C-TR-192` `capability` The change log is machine-readable per version with every addition, deprecation, removal. `src: Technical requirements, instruction.md`
- [ ] `C-TR-193` `constraint` Contract checks run against every supported version on every deploy. `src: Technical requirements, instruction.md`
- [ ] `C-TR-194` `capability` Deprecation telemetry is recorded per installation, per deprecated field. `src: Technical requirements, instruction.md`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds ninety-four tables in fourteen groups. `src: Data model, instruction.md`
- [ ] `C-DM-02` `data` All timestamps are UTC. `src: Data model, instruction.md`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`, written into `/app/USER_README.md` beside each account. `src: Data model, instruction.md`
- [ ] `C-DM-04` `constraint` A primary key is an opaque, sortable, type-prefixed identifier unique across the platform. `src: Data model, instruction.md`
- [ ] `C-DM-05` `constraint` Money is always two columns: an integer in minor units plus a currency code. `src: Data model, instruction.md`
- [ ] `C-DM-06` `constraint` No money column is a decimal type or a float. `src: Data model, instruction.md`
- [ ] `C-DM-07` `constraint` A fractional quantity is a separate typed column with its unit rather than a float in the quantity column. `src: Data model, instruction.md`
- [ ] `C-DM-08` `constraint` Soft deletion exists only where a regulation requires retention or a live storefront would break. `src: Data model, instruction.md`
- [ ] `C-DM-09` `constraint` Enumerations are database enumerations or check constraints rather than free strings. `src: Data model, instruction.md`
- [ ] `C-DM-10` `constraint` Foreign keys are declared with explicit delete behaviour, restricting by default. `src: Data model, instruction.md`
- [ ] `C-DM-11` `constraint` A nullable column carries a documented meaning for null. `src: Data model, instruction.md`
- [ ] `C-DM-12` `constraint` A metafield lives in one typed extension table per owner type rather than in a document column. `src: Data model, instruction.md`
- [ ] `C-DM-13` `literal` Every tenant-owned table carries `store_id`, `environment`, `data_region`, all not null. `src: Data model, instruction.md`
- [ ] `C-DM-14` `constraint` The store identifier leads every index that matters. `src: Data model, instruction.md`
- [ ] `C-DM-15` `literal` The column `environment` is `live` or `development`, part of every unique constraint. `src: Data model, instruction.md`
- [ ] `C-DM-16` `constraint` The data region is denormalised from the organisation, so a region predicate never needs a join. `src: Data model, instruction.md`
- [ ] `C-DM-17` `constraint` A connection scoped to one store returns zero rows from every tenant-owned table populated only for another. `src: Data model, instruction.md`
- [ ] `C-DM-18` `constraint` A schema-generated suite covers the cross-tenant read, so a new table cannot be added uncovered. `src: Data model, instruction.md`
- [ ] `C-DM-19` `data` Identity tables cover person, factors, recovery codes, organisation, store, membership, organisation membership, role, role permission, membership role. `src: Data model, instruction.md`
- [ ] `C-DM-20` `data` The constraint set holds a membership, a refund ceiling with its currency, a discount ceiling with a cap, a readable personal-field set, a data region. `src: Data model, instruction.md`
- [ ] `C-DM-21` `data` Assignment tables hold a membership, a target, a granting actor, a granting instant, an expiry. `src: Data model, instruction.md`
- [ ] `C-DM-22` `data` A session holds person, nullable store, environment, instants, address, user agent, revocation instant, with no claims. `src: Data model, instruction.md`
- [ ] `C-DM-23` `data` Federation tables hold the issuer configuration, the claim map, the assertion replay record. `src: Data model, instruction.md`
- [ ] `C-DM-24` `constraint` An assertion replay record is unique, retained longer than the skew tolerance. `src: Data model, instruction.md`
- [ ] `C-DM-25` `data` Catalog tables cover product, tag, option, option value, variant, variant option value, inventory item, media, collection, collection product, metafield definition, metafield, publication. `src: Data model, instruction.md`
- [ ] `C-DM-26` `data` A variant holds stock-keeping unit, barcode, price, compare-at, cost, mass, shipping flag, taxable flag, tax code, position, inventory policy, inventory item. `src: Data model, instruction.md`
- [ ] `C-DM-27` `constraint` A variant option value row is unique on variant plus product option. `src: Data model, instruction.md`
- [ ] `C-DM-28` `data` Inventory tables cover location, inventory level, inventory movement, transfer, transfer line, reservation. `src: Data model, instruction.md`
- [ ] `C-DM-29` `constraint` An inventory level is unique on item plus location. `src: Data model, instruction.md`
- [ ] `C-DM-30` `constraint` The quantity `available` is a generated column. `src: Data model, instruction.md`
- [ ] `C-DM-31` `constraint` The inventory movement table is append-only. `src: Data model, instruction.md`
- [ ] `C-DM-32` `data` Order tables cover order, order line, order address, order attribution, draft order, fulfilment order, fulfilment order line, fulfilment, return, return line, return shipment. `src: Data model, instruction.md`
- [ ] `C-DM-33` `data` An order carries a version column holding the concurrency check. `src: Data model, instruction.md`
- [ ] `C-DM-34` `data` An order line carries snapshots of product title, variant title, stock-keeping unit, alongside a nullable variant reference. `src: Data model, instruction.md`
- [ ] `C-DM-35` `data` A fulfilment order carries a routing trace document. `src: Data model, instruction.md`
- [ ] `C-DM-36` `data` Money tables cover balance, ledger transaction, ledger entry, payment, payment personal data, refund, dispute, dispute evidence, payout, payout item, settlement instrument, platform fee, fee rate version, gift card, store credit. `src: Data model, instruction.md`
- [ ] `C-DM-37` `constraint` A balance row is unique on store, currency, kind. `src: Data model, instruction.md`
- [ ] `C-DM-38` `constraint` A ledger entry is never updated, never deleted, enforced by the privilege the application role holds. `src: Data model, instruction.md`
- [ ] `C-DM-39` `constraint` A deferred constraint asserts a transaction's per-currency sum is zero at commit. `src: Data model, instruction.md`
- [ ] `C-DM-40` `constraint` A reversal references its original, with a check preventing a reversal of its own reversal. `src: Data model, instruction.md`
- [ ] `C-DM-41` `constraint` A ledger transaction with a source exists once per idempotency key. `src: Data model, instruction.md`
- [ ] `C-DM-42` `constraint` Payment personal data sits in a separate table, so the join is the authorization boundary. `src: Data model, instruction.md`
- [ ] `C-DM-43` `constraint` A check constraint holds the sum of non-failed refunds at or below the captured amount. `src: Data model, instruction.md`
- [ ] `C-DM-44` `constraint` A settlement instrument is versioned rather than edited. `src: Data model, instruction.md`
- [ ] `C-DM-45` `data` Customer tables cover customer, customer personal data, consent, address, segment, segment member, company, company location, company contact, company credit. `src: Data model, instruction.md`
- [ ] `C-DM-46` `data` Company credit exposure is derived from the ledger rather than stored independently. `src: Data model, instruction.md`
- [ ] `C-DM-47` `data` Market tables cover market, market language, market region, market domain, market setting, catalog, catalog company, catalog product, price list, price list entry, price break, quantity rule. `src: Data model, instruction.md`
- [ ] `C-DM-48` `constraint` A market region row is unique per store per country. `src: Data model, instruction.md`
- [ ] `C-DM-49` `data` A market setting row exists only where a setting is overridden, so the row count is the customisation figure. `src: Data model, instruction.md`
- [ ] `C-DM-50` `data` Channel tables cover channel, channel order reference, application, installation, scope grant, application charge, event, outbox, subscription, delivery attempt. `src: Data model, instruction.md`
- [ ] `C-DM-51` `constraint` A channel order reference is unique on channel plus external identifier. `src: Data model, instruction.md`
- [ ] `C-DM-52` `data` Workflow tables cover workflow, node, edge, run, step, approval request, approval decision, approval delegation. `src: Data model, instruction.md`
- [ ] `C-DM-53` `data` An approval request carries an idempotency key plus a correlation identifier. `src: Data model, instruction.md`
- [ ] `C-DM-54` `data` Governance tables cover audit entry, consent record, data request, retention policy, encryption key reference. `src: Data model, instruction.md`
- [ ] `C-DM-55` `data` An audit entry carries the previous entry's hash beside its own. `src: Data model, instruction.md`
- [ ] `C-DM-56` `constraint` Every tenant table is indexed on store, environment, creation instant descending. `src: Data model, instruction.md`
- [ ] `C-DM-57` `constraint` Orders are additionally indexed on the two statuses with creation instant, on customer, on market, on channel. `src: Data model, instruction.md`
- [ ] `C-DM-58` `constraint` Variants are indexed on stock-keeping unit, on barcode. `src: Data model, instruction.md`
- [ ] `C-DM-59` `constraint` A price-list entry is unique on price list plus variant. `src: Data model, instruction.md`
- [ ] `C-DM-60` `constraint` Audit entries are indexed by organisation, by resource, by actor, each with an instant. `src: Data model, instruction.md`
- [ ] `C-DM-61` `constraint` A company assignment is indexed in both directions. `src: Data model, instruction.md`
- [ ] `C-DM-62` `constraint` No index on a nullable tenant column exists without the store identifier leading one. `src: Data model, instruction.md`
- [ ] `C-DM-63` `constraint` No production query plan scans a tenant table without a store predicate. `src: Data model, instruction.md`
- [ ] `C-DM-64` `constraint` Events, delivery attempts are time-partitioned, dropped by partition on retention. `src: Data model, instruction.md`
- [ ] `C-DM-65` `constraint` Audit entries are time-partitioned, retained long, never dropped without a governance decision. `src: Data model, instruction.md`
- [ ] `C-DM-66` `constraint` Inventory movements, ledger entries are time-partitioned, never dropped. `src: Data model, instruction.md`
- [ ] `C-DM-67` `data` Derived values are the available quantity, customer aggregates, company exposure, reading time, market customisation count, a balance, rule-based collection membership. `src: Data model, instruction.md`
- [ ] `C-DM-68` `literal` The seeded organisation is `Northbeam Retail Group` in data region `ap-south`. `src: Data model, instruction.md`
- [ ] `C-DM-69` `literal` The first seeded store has handle `oakleaf`, currency `inr`, timezone `Asia/Kolkata`. `src: Data model, instruction.md`
- [ ] `C-DM-70` `literal` The seeded store `Modern Mallard` has handle `modern-mallard`, currency `inr`, timezone `Asia/Kolkata`. `src: Data model, instruction.md`
- [ ] `C-DM-71` `literal` The first seeded store's locations are `Pune Warehouse`, which fulfils online orders, plus `Delhi Flagship`, which is retail with pickup enabled. `src: Data model, instruction.md`
- [ ] `C-DM-72` `literal` The seeded products are `Pauline` at `1122600`, `Sanders` at `1330400`, `Addie` at `956400`. `src: Data model, instruction.md`
- [ ] `C-DM-73` `literal` The seeded products continue with `Sedgewick` at `1497200`, `Chip` at `748400`, `Carry` at `5986900`. `src: Data model, instruction.md`
- [ ] `C-DM-74` `literal` Each seeded product holds `12` on hand at `Pune Warehouse` plus `3` at `Delhi Flagship`, except `Carry`. `src: Data model, instruction.md`
- [ ] `C-DM-75` `literal` The product `Carry` holds `1` on hand at `Pune Warehouse` plus `0` at `Delhi Flagship`. `src: Data model, instruction.md`
- [ ] `C-DM-76` `literal` The seeded order `#2050` belongs to `Guy Hawkins` totalling `850900`. `src: Data model, instruction.md`
- [ ] `C-DM-77` `literal` The seeded order `#2049` belongs to `Floyd Miles` totalling `3411200`. `src: Data model, instruction.md`
- [ ] `C-DM-78` `literal` The seeded order `#2048` belongs to `Cody Fisher` totalling `850900`. `src: Data model, instruction.md`
- [ ] `C-DM-79` `literal` The seeded order `#2047` belongs to `Ralph Edwards` totalling `3411200`. `src: Data model, instruction.md`
- [ ] `C-DM-80` `literal` The seeded order `#2046` belongs to `Theresa Webb` totalling `850900`. `src: Data model, instruction.md`
- [ ] `C-DM-81` `constraint` Every order seeded on the first store starts `paid` plus `unfulfilled`. `src: Data model, instruction.md`
- [ ] `C-DM-82` `literal` The seeded order `#3001` belongs to `Modern Mallard`, customer `Anu Gupta`, totalling `1998640`. `src: Data model, instruction.md`
- [ ] `C-DM-83` `literal` The seeded company `Halcyon Goods` sits on payment terms `Net 30` with one location, one contact, no representative assigned. `src: Data model, instruction.md`
- [ ] `C-DM-84` `constraint` Seeding is idempotent, so restarting the app does not duplicate rows. `src: Data model, instruction.md`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product is multi-tenant, with tenancy never taken from a request parameter. `src: Constraints, instruction.md`
- [ ] `C-CN-02` `constraint` One organisation, two stores, five people are seeded, with no public staff registration. `src: Constraints, instruction.md`
- [ ] `C-CN-03` `constraint` There is no native application, no desktop client, no browser extension. `src: Constraints, instruction.md`
- [ ] `C-CN-04` `constraint` There is no terminal firmware, no card-reader pairing, no device provisioning. `src: Constraints, instruction.md`
- [ ] `C-CN-05` `constraint` There is no editorial authoring back office. `src: Constraints, instruction.md`
- [ ] `C-CN-06` `constraint` No real external service is contacted at run time. `src: Constraints, instruction.md`
- [ ] `C-CN-07` `constraint` No outbound network call is made at run time. `src: Constraints, instruction.md`
- [ ] `C-CN-08` `constraint` The only backing services are `postgres`, `keycloak`. `src: Constraints, instruction.md`
- [ ] `C-CN-09` `constraint` No binary asset of any kind ships with the build. `src: Constraints, instruction.md`
- [ ] `C-CN-10` `constraint` No host, no port is hard-coded anywhere. `src: Constraints, instruction.md`
- [ ] `C-CN-11` `constraint` No decimal or floating-point type appears anywhere on a money path. `src: Constraints, instruction.md`
- [ ] `C-CN-12` `constraint` No behaviour depends on a hover-only affordance. `src: Constraints, instruction.md`
- [ ] `C-CN-13` `constraint` No page scrolls horizontally at any width, in any language, in either direction. `src: Constraints, instruction.md`
- [ ] `C-CN-14` `constraint` The app stays responsive at the stated volume targets. `src: Constraints, instruction.md`
- [ ] `C-CN-15` `constraint` The app stays correct where two people reach the same last unit or the same single-use code at one instant. `src: Constraints, instruction.md`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app must be reachable at `APP_PUBLIC_URL`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, both read from the environment. `src: Deployment contract, instruction.md`
- [ ] `C-DC-03` `contract` The HTTP API is served on that same origin under the `/api` prefix. `src: Deployment contract, instruction.md`
- [ ] `C-DC-04` `contract` The endpoint `GET /api/health` returns `200` once ready. `src: Deployment contract, instruction.md`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, instruction.md`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty. `src: Deployment contract, instruction.md`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server rather than a dev server. `src: Deployment contract, instruction.md`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, never a child of the shell. `src: Deployment contract, instruction.md`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract, instruction.md`
- [ ] `C-DC-11` `contract` Named backing services are already running, so none is downloaded, installed, compiled, or started. `src: Deployment contract, instruction.md`
- [ ] `C-DC-12` `contract` Only the providers named in the brief are used, with no edge functions. `src: Deployment contract, instruction.md`
- [ ] `C-DC-13` `contract` There are no persistent volumes, no fixed container names, no custom networks. `src: Deployment contract, instruction.md`
- [ ] `C-DC-14` `contract` The endpoint `GET /api/stores` returns a top-level array of the session person's stores with `id`, `handle`, `name`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-15` `contract` The endpoint `GET /api/orders` returns a top-level array of orders in the session's store. `src: Deployment contract, instruction.md`
- [ ] `C-DC-16` `contract` An order summary carries `id`, `number`, `customer_name`, `total_minor`, `currency`, `financial_status`, `fulfilment_status`, `item_count`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-17` `contract` The endpoint `GET /api/orders/{id}` returns the order with its lines, its addresses, its timeline. `src: Deployment contract, instruction.md`
- [ ] `C-DC-18` `contract` The endpoint `POST /api/orders/{id}/refunds` accepts `amount_minor`, `currency`, `reason`, `restock`, `idempotency_key`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-19` `contract` A within-ceiling refund response carries `id`, `amount_minor`, `currency`, `status`, `ledger_transaction_id`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-20` `contract` An above-ceiling refund response carries the approval request with `state` equal to `pending`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-21` `contract` An above-ceiling refund response carries `action_type` equal to `order_refund`, plus `amount_minor`, `required_permission`, `expires_at`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-22` `contract` The endpoint `GET /api/approvals` returns a top-level array of approval requests in the session's store. `src: Deployment contract, instruction.md`
- [ ] `C-DC-23` `contract` An approval summary carries `id`, `action_type`, `amount_minor`, `currency`, `requested_by`, `state`, `required_permission`, `expires_at`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-24` `contract` The endpoint `GET /api/approvals/{id}` returns the request with its full proposed parameters, its decisions. `src: Deployment contract, instruction.md`
- [ ] `C-DC-25` `contract` The endpoint `POST /api/approvals/{id}/decision` accepts `decision`, a `note`, `idempotency_key`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-26` `contract` A decision response carries `state`, `decided_by`, `decided_at`, plus `executed_effect` on approval. `src: Deployment contract, instruction.md`
- [ ] `C-DC-27` `contract` The endpoint `GET /api/inventory` returns levels with `variant_id`, `sku`, `location_id`, `on_hand`, `committed`, `reserved`, `available`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-28` `contract` The endpoint `POST /api/inventory/adjustments` accepts `variant_id`, `location_id`, `quantity_name`, `delta`, `reason`, `idempotency_key`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-29` `contract` The endpoint `GET /api/products` returns a top-level array of products with their variants. `src: Deployment contract, instruction.md`
- [ ] `C-DC-30` `contract` The endpoint `GET /api/balances` returns balances with `currency`, `kind`, `amount_minor`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-31` `contract` The endpoint `POST /api/checkouts` accepts `store`, `lines`, `idempotency_key`, returning a session token with reserved lines. `src: Deployment contract, instruction.md`
- [ ] `C-DC-32` `contract` The endpoint `POST /api/checkouts/{token}/complete` accepts `payment_method`, `address`, `idempotency_key`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-33` `contract` Every list endpoint returns a top-level JSON array. `src: Deployment contract, instruction.md`
- [ ] `C-DC-34` `contract` An invalid or unauthorized call is rejected as a client error rather than a server error or a silent success. `src: Deployment contract, instruction.md`
- [ ] `C-DC-35` `contract` A rejection carries a machine code, a human message, the path to the offending field. `src: Deployment contract, instruction.md`
- [ ] `C-DC-36` `contract` Bearer authorization is required on everything except login, health, webhook receivers. `src: Deployment contract, instruction.md`
- [ ] `C-DC-37` `contract` A webhook receiver authenticates by signature rather than by a user token. `src: Deployment contract, instruction.md`
- [ ] `C-DC-38` `contract` Every mutating endpoint accepts `idempotency_key`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-39` `contract` Every endpoint moving money, stock, or a message requires `idempotency_key`. `src: Deployment contract, instruction.md`
- [ ] `C-DC-40` `constraint` An in-memory list of orders or approvals returned by the app to itself is a contract violation. `src: Deployment contract, instruction.md`
- [ ] `C-DC-41` `constraint` A session minted without the issuer having authenticated the person is a contract violation. `src: Deployment contract, instruction.md`
- [ ] `C-DC-42` `constraint` A store context taken from a request parameter is a contract violation. `src: Deployment contract, instruction.md`
- [ ] `C-DC-43` `constraint` A balance computed by adding up orders rather than read from ledger entries is a contract violation. `src: Deployment contract, instruction.md`
- [ ] `C-DC-44` `constraint` A refund row written without a balanced ledger transaction behind one is a contract violation. `src: Deployment contract, instruction.md`
- [ ] `C-DC-45` `constraint` An approval whose execution writes the refund before the decision is a contract violation. `src: Deployment contract, instruction.md`
- [ ] `C-DC-46` `constraint` An `available` quantity stored as a column somebody writes is a contract violation. `src: Deployment contract, instruction.md`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `support_agent` | the built-in role holding the small refund ceiling | `C-RL-11` |
| `500000` | the support-agent refund ceiling in minor units | `C-RL-11` |
| `finance` | the built-in role holding the larger refund ceiling | `C-RL-12` |
| `20000000` | the finance refund ceiling in minor units | `C-RL-12` |
| `owner@example.com` | the seeded owner account | `C-RL-50` |
| `owner` | the built-in role granting everything in a store | `C-RL-50` |
| `manager@example.com` | the seeded store-manager account | `C-RL-51` |
| `store_manager` | the built-in role for day-to-day trade | `C-RL-51` |
| `support@example.com` | the seeded support-agent account | `C-RL-52` |
| `finance@example.com` | the seeded finance account | `C-RL-53` |
| `mallard@example.com` | the seeded account whose only membership is the second store | `C-RL-54` |
| `Modern Mallard` | the seeded second store, the tenancy counterexample | `C-RL-54` |
| `deku-demo-pw-2026` | the password every seeded account signs in with | `C-RL-55` |
| `3411200` | the total of the boundary order in minor units | `C-CF-13` |
| `#2049` | the seeded order whose total sits between the two ceilings | `C-CF-13` |
| `pending` | a order financial status | `C-CF-36` |
| `approved` | a approval request state | `C-CF-36` |
| `declined` | a approval request state | `C-CF-36` |
| `expired` | a approval request state | `C-CF-36` |
| `executed` | a approval request state | `C-CF-36` |
| `8` | the minimum password length | `C-CF-65` |
| `15` | the step-up freshness window in minutes, also the one-time link lifetime | `C-CF-67` |
| `24` | the session idle window in hours, also the absolute checkout lifetime | `C-CF-73` |
| `30` | the absolute session window in days, also the delivery-attempt retention | `C-CF-74` |
| `60` | the deprovisioning budget in seconds, also the loud outbox-lag threshold | `C-CF-85` |
| `trial` | a store lifecycle state | `C-CF-107` |
| `active` | a store lifecycle state | `C-CF-107` |
| `past_due` | a store lifecycle state | `C-CF-107` |
| `frozen` | a store lifecycle state | `C-CF-107` |
| `paused` | a store lifecycle state | `C-CF-107` |
| `closed` | a store lifecycle state | `C-CF-107` |
| `archived` | a store lifecycle state | `C-CF-107` |
| `3` | the option cap per product, also the first dunning step in days | `C-CF-124` |
| `status` | a product field name | `C-CF-127` |
| `draft` | a product status value | `C-CF-127` |
| `2000` | the variant cap per product | `C-CF-150` |
| `on_hand` | a inventory quantity name | `C-CF-152` |
| `committed` | a inventory quantity name | `C-CF-152` |
| `reserved` | a inventory quantity name | `C-CF-152` |
| `incoming` | a inventory quantity name | `C-CF-152` |
| `damaged` | a inventory quantity name | `C-CF-152` |
| `quality_control` | a inventory quantity name | `C-CF-152` |
| `safety_stock` | a inventory quantity name | `C-CF-152` |
| `sale` | a stock movement reason | `C-CF-155` |
| `return` | a stock movement reason | `C-CF-155` |
| `restock` | a stock movement reason | `C-CF-155` |
| `correction` | a stock movement reason | `C-CF-155` |
| `received` | a stock movement reason | `C-CF-155` |
| `transfer_out` | a stock movement reason | `C-CF-155` |
| `transfer_in` | a stock movement reason | `C-CF-155` |
| `theft` | a stock movement reason | `C-CF-155` |
| `promotion` | a stock movement reason | `C-CF-155` |
| `sample` | a stock movement reason | `C-CF-155` |
| `recount` | a stock movement reason | `C-CF-155` |
| `inventory_policy` | a product field name | `C-CF-165` |
| `deny` | a inventory policy value | `C-CF-165` |
| `continue` | a inventory policy value | `C-CF-165` |
| `in_transit` | a transfer state | `C-CF-175` |
| `partially_received` | a transfer state | `C-CF-175` |
| `cancelled` | a transfer state | `C-CF-175` |
| `authorized` | a order financial status | `C-CF-185` |
| `partially_paid` | a order financial status | `C-CF-185` |
| `paid` | a order financial status | `C-CF-185` |
| `partially_refunded` | a order financial status | `C-CF-185` |
| `refunded` | a order financial status | `C-CF-185` |
| `voided` | a order financial status | `C-CF-185` |
| `unfulfilled` | a order fulfilment status | `C-CF-186` |
| `partially_fulfilled` | a order fulfilment status | `C-CF-186` |
| `fulfilled` | a order fulfilment status | `C-CF-186` |
| `on_hold` | a order fulfilment status | `C-CF-186` |
| `scheduled` | a order fulfilment status | `C-CF-186` |
| `in_progress` | a order fulfilment status | `C-CF-186` |
| `30 days` | the default period on the order index | `C-CF-210` |
| `All` | a shipped system view | `C-CF-211` |
| `Unfulfilled` | a shipped system view | `C-CF-211` |
| `Unpaid` | a shipped system view | `C-CF-211` |
| `Open` | a shipped system view | `C-CF-211` |
| `Closed` | a shipped system view | `C-CF-211` |
| `Automations` | a shipped system view | `C-CF-211` |
| `Return requests` | a shipped system view | `C-CF-211` |
| `Local Delivery` | a shipped system view | `C-CF-211` |
| `50` | the saved-view cap per index | `C-CF-215` |
| `available` | a inventory quantity name | `C-CF-230` |
| `disputed` | a balance kind | `C-CF-230` |
| `fee` | a balance kind | `C-CF-230` |
| `tax` | a balance kind | `C-CF-230` |
| `rounding` | a balance kind | `C-CF-230` |
| `gift_card_liability` | a balance kind | `C-CF-230` |
| `store_credit_liability` | a balance kind | `C-CF-230` |
| `created` | a payment state | `C-CF-231` |
| `requires_action` | a payment state | `C-CF-231` |
| `captured` | a payment state | `C-CF-231` |
| `failed` | a payment state | `C-CF-231` |
| `opened` | a dispute state | `C-CF-247` |
| `evidence_due` | a dispute state | `C-CF-247` |
| `submitted` | a dispute state | `C-CF-247` |
| `won` | a dispute state | `C-CF-247` |
| `lost` | a dispute state | `C-CF-247` |
| `7` | the event-log retention in days, also the idempotency-key retention | `C-CF-258` |
| `14` | a dunning step in days | `C-CF-258` |
| `21` | the dunning step at which a store freezes | `C-CF-258` |
| `ready_for_pickup` | a fulfilment state added by pickup | `C-CF-296` |
| `picked_up` | a fulfilment state added by pickup | `C-CF-296` |
| `requested` | a return state | `C-CF-303` |
| `label_issued` | a return state | `C-CF-303` |
| `inspected` | a return state | `C-CF-303` |
| `resolved` | a return state | `C-CF-303` |
| `restock_sellable` | a restock decision | `C-CF-311` |
| `restock_damaged` | a restock decision | `C-CF-311` |
| `restock_quality_control` | a restock decision | `C-CF-311` |
| `do_not_restock` | a restock decision | `C-CF-311` |
| `minimum` | a quantity rule field | `C-CF-334` |
| `maximum` | a quantity rule field | `C-CF-334` |
| `increment` | a quantity rule field | `C-CF-334` |
| `region` | a market type | `C-CF-362` |
| `b2b` | a market type | `C-CF-362` |
| `retail` | a market type | `C-CF-362` |
| `inactive` | a market state | `C-CF-363` |
| `4` | the market inheritance depth bound | `C-CF-367` |
| `1` | the checkout idle window in hours, also the audit retention floor in years | `C-CF-415` |
| `Province` | the address field label India renders | `C-CF-420` |
| `Estimated taxes` | the checkout summary line before the order is placed | `C-CF-432` |
| `main` | a theme role | `C-CF-447` |
| `unpublished` | a theme role | `C-CF-447` |
| `development` | an environment value, also a theme role | `C-CF-447` |
| `catalog_sync` | a channel capability | `C-CF-475` |
| `order_ingest` | a channel capability | `C-CF-475` |
| `checkout_here` | a channel capability | `C-CF-475` |
| `checkout_there` | a channel capability | `C-CF-475` |
| `inventory_sync` | a channel capability | `C-CF-475` |
| `fulfilment_there` | a channel capability | `C-CF-475` |
| `returns_there` | a channel capability | `C-CF-475` |
| `90` | the abandoned-checkout retention in days, also the edge hit-ratio floor | `C-CF-606` |
| `24/7 local chat support` | the support line the India plan table advertises | `C-CF-621` |
| `staff_seats` | a plan entitlement key | `C-CF-634` |
| `inventory_locations` | a plan entitlement key | `C-CF-635` |
| `b2b_catalogs` | a plan entitlement key | `C-CF-636` |
| `market_customisation` | a plan entitlement key | `C-CF-637` |
| `checkout_customisation` | a plan entitlement key | `C-CF-638` |
| `carrier_calculated_rates` | a plan entitlement key | `C-CF-639` |
| `Pay yearly` | the billing toggle label on the plan comparison | `C-CF-641` |
| `interactive` | a queue class | `C-TR-58` |
| `money` | a queue class | `C-TR-58` |
| `delivery` | a queue class | `C-TR-58` |
| `bulk` | a queue class | `C-TR-58` |
| `maintenance` | a queue class | `C-TR-58` |
| `2` | the progress-record threshold in seconds | `C-TR-77` |
| `48` | the webhook retry window in hours | `C-TR-89` |
| `5` | the search freshness bound in seconds, also the recovery point in minutes | `C-TR-90` |
| `2.5s` | the storefront largest-contentful-paint budget | `C-TR-151` |
| `200ms` | the interaction-to-next-paint budget | `C-TR-151` |
| `0.1` | the cumulative-layout-shift budget | `C-TR-151` |
| `600ms` | the uncached origin first-byte budget | `C-TR-152` |
| `120KB` | the storefront route script budget | `C-TR-152` |
| `60KB` | the storefront stylesheet budget | `C-TR-152` |
| `2.0s` | the merchant storefront largest-contentful-paint budget | `C-TR-153` |
| `300ms` | the median uncached server render budget | `C-TR-153` |
| `90%` | the edge hit-ratio floor for anonymous traffic | `C-TR-153` |
| `70KB` | the default theme client script budget | `C-TR-153` |
| `1.0s` | the admin shell paint budget | `C-TR-155` |
| `1.5s` | the admin index first-row budget, also checkout first-step interactive | `C-TR-155` |
| `1.2s` | the admin detail page budget | `C-TR-155` |
| `150ms` | the median command-surface first-result budget | `C-TR-155` |
| `5s` | the median search freshness budget after a write | `C-TR-155` |
| `500ms` | the save round-trip budget at the 95th percentile | `C-TR-155` |
| `400ms` | the checkout step transition budget | `C-TR-156` |
| `3s` | the payment submit-to-result budget at the 95th percentile | `C-TR-156` |
| `200` | the row count beyond which a list renders only what is on screen | `C-TR-163` |
| `1,000,000` | the products-per-store volume target | `C-TR-167` |
| `2,000` | the variants-per-product volume target | `C-TR-167` |
| `250,000` | the orders-per-store-per-day volume target | `C-TR-167` |
| `100,000` | the companies-per-store volume target | `C-TR-167` |
| `5,000,000` | the events-per-store-per-day volume target | `C-TR-167` |
| `20,000` | the concurrent-checkouts-per-store volume target | `C-TR-167` |
| `/app/USER_README.md` | the file the seeded logins are written into | `C-DM-03` |
| `store_id` | the tenant column leading every index that matters | `C-DM-13` |
| `environment` | the tenant column separating live rows from development rows | `C-DM-13` |
| `data_region` | the tenant column denormalised from the organisation | `C-DM-13` |
| `live` | an environment value | `C-DM-15` |
| `Northbeam Retail Group` | the seeded organisation | `C-DM-68` |
| `ap-south` | the seeded organisation's data region | `C-DM-68` |
| `oakleaf` | the handle of the first seeded store | `C-DM-69` |
| `inr` | the store currency | `C-DM-69` |
| `Asia/Kolkata` | the store timezone, a named zone | `C-DM-69` |
| `modern-mallard` | the handle of the second seeded store | `C-DM-70` |
| `Pune Warehouse` | the seeded location that fulfils online orders | `C-DM-71` |
| `Delhi Flagship` | the seeded retail location with pickup enabled | `C-DM-71` |
| `Pauline` | a seeded product | `C-DM-72` |
| `1122600` | a seeded variant price in minor units | `C-DM-72` |
| `Sanders` | a seeded product | `C-DM-72` |
| `1330400` | a seeded variant price in minor units | `C-DM-72` |
| `Addie` | a seeded product | `C-DM-72` |
| `956400` | a seeded variant price in minor units | `C-DM-72` |
| `Sedgewick` | a seeded product | `C-DM-73` |
| `1497200` | a seeded variant price in minor units | `C-DM-73` |
| `Chip` | a seeded product | `C-DM-73` |
| `748400` | a seeded variant price in minor units | `C-DM-73` |
| `Carry` | the seeded product stocked at the contention boundary | `C-DM-73` |
| `5986900` | a seeded variant price in minor units | `C-DM-73` |
| `12` | the seeded on-hand quantity at the warehouse | `C-DM-74` |
| `0` | the seeded on-hand quantity of the boundary product at the flagship | `C-DM-75` |
| `#2050` | a seeded order small enough to refund inside the ceiling | `C-DM-76` |
| `Guy Hawkins` | a seeded customer name | `C-DM-76` |
| `850900` | the total of the small seeded orders in minor units | `C-DM-76` |
| `Floyd Miles` | a seeded customer name | `C-DM-77` |
| `#2048` | a seeded order | `C-DM-78` |
| `Cody Fisher` | a seeded customer name | `C-DM-78` |
| `#2047` | a seeded order | `C-DM-79` |
| `Ralph Edwards` | a seeded customer name | `C-DM-79` |
| `#2046` | a seeded order | `C-DM-80` |
| `Theresa Webb` | a seeded customer name | `C-DM-80` |
| `#3001` | the seeded order belonging to the second store | `C-DM-82` |
| `Anu Gupta` | the seeded customer of the second store | `C-DM-82` |
| `1998640` | the total of the second store's order in minor units | `C-DM-82` |
| `Halcyon Goods` | the seeded company buying on terms | `C-DM-83` |
| `Net 30` | the seeded company's payment terms | `C-DM-83` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the base spacing unit every gap is a multiple of | `C-UX-20` |
| the exact shade of every colour role | `C-UX-07` |
| the exact easing curves shared across the product | `C-UX-30` |
| the exact width at which each responsive tier changes | `C-UX-40` |
| the exact radius of each of the four softening steps | `C-UX-22` |
| the variable grotesque family name | `C-UX-17` |
| the configured discount ceiling per role | `C-CF-207` |
| the configured approval expiry window | `C-CF-37` |
| the configured approval escalation interval | `C-CF-38` |
| the configured checkout reservation sweep interval | `C-CF-130` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 3 | 10 |
| User roles | 21 | 58 |
| Core features | 170 | 680 |
| User flow | 57 | 81 |
| UI and UX notes | 14 | 48 |
| Front-end specification | 71 | 173 |
| Technical requirements | 72 | 194 |
| Data model | 52 | 84 |
| Constraints | 2 | 15 |
| Deployment contract | 22 | 46 |

