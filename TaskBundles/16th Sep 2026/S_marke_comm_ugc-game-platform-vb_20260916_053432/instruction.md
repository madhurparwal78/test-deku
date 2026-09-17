# Kavora

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, sign up behind the age gate, buy a Kredz pack with real money, spend
those Kredz on an item another member published, and see the creator's balance
rise by the creator's share, without hitting an error page. A different stranger,
signed in as somebody else, must NOT be able to read that buyer's balance, that
creator's sales or that creator's payout requests by any means, including a
direct call to the API. The Kredz pack purchase cannot be faked inside the app:
the invoice must exist as a real record in `killbill` for the exact amount and
currency, and a confirmation the app returns to itself does not count.

## Overview

Kavora is a platform where the things people play and buy are made by other
people who use it. A visitor signs up behind an age gate, browses experiences and
marketplace items other members published, buys them with Kredz, the platform's
virtual currency, and the money flows back to whoever made the thing.

Two kinds of member share one account model. A player browses, buys and plays. A
creator is a player who has also published, and who is owed money. Everything a
member is allowed to do is decided by two things: who they are, and which age
band their stored date of birth resolves to today.

The genuinely hard part is the money. Balances are not a number that gets edited.
They are derived from an append-only log of entries, every economic operation
carries a caller-supplied idempotency key, and a correction is a new compensating
transaction rather than a repair to an old one. Two people buying the last thing
a balance can afford, at the same instant, must produce exactly one purchase.

The product deliberately is not: a place to run or render an experience, a chat
or messaging product, a social feed, a desktop creation tool, or a storefront for
anything except Kredz and the items members publish. Kavora Studio, the desktop
tool the platform is authored in, is named in the product and is not part of this
build.

Parts of this specification describe surfaces that were measured on a reference
product, and parts describe machinery that could only be specified. Build both;
the distinction is about where the requirements came from, not about how firm
they are.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `player` | Sign up, sign in by four routes, read the public catalogue and charts, search across four scopes, read **its own** balance, ledger, purchases, sessions and enrolled credentials, buy Kredz packs, buy items its age band allows, reserve a slot in an experience, appeal an enforcement action against it | **Cannot read another member's balance, ledger, purchases, sales or payout requests. Cannot publish an asset. Cannot request a payout. Cannot read or act on any creator route.** |
| `creator` | Everything a player can do, plus publish assets, edit and version **its own** items, read **its own** sales and split records, read its own payout eligibility and request a payout | **Cannot read or act on another creator's assets, items, sales or payouts. Cannot set its own split rate, approve its own moderation, or change its own eligibility.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `player` session
to any `creator`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged. The same
holds between two creators: one creator calling another creator's item, sale or
payout endpoint is denied, and the underlying row must not change.

A role is never read from a request body or a query parameter. Neither is an age
band: viewer context is derived server side from the session, and a client that
asserts its own band is ignored.

**Signup is open.** Anyone may create an account, and the age gate runs before
the account exists. These accounts are seeded for convenience and every one of
them uses the password `deku-demo-pw-2026`:

| Email | Username | Date of birth | Band today | Kredz | Role |
|---|---|---|---|---|---|
| `player@example.com` | `Nova Pilot` | `1996-03-11` | `adult` | `1000` | player |
| `player2@example.com` | `Tiny Comet` | `2016-05-04` | `child` | `500` | player |
| `player3@example.com` | `Edge Case` | `1999-07-22` | `adult` | `75` | player |
| `creator@example.com` | `Vale Studio` | `1990-01-15` | `adult` | `0` | creator |
| `creator2@example.com` | `Hollow Forge` | `1992-11-02` | `adult` | `0` | creator |

## Core features

### Auth

Email and password with bearer tokens, implemented by the app. `POST
/api/auth/signup` and `POST /api/auth/login` both take an `email` with a
`password` and answer with an `access_token`; every other call sends
`Authorization: Bearer <token>`. Passwords are stored hashed, never in
plain text. A token expires, and `POST /api/auth/logout` revokes one session.

1. Date of birth is collected **before any other account field** and is required.
   The signup body carries `date_of_birth` first, then `username`, then
   `email`, then `password`, then an optional `gender`. The visible identifier
   field accepts the account's email address.
2. The stored value is the **date of birth**. The age band is derived at read
   time and is never stored as the source of truth. Bands are `child` below `13`,
   `teen` from `13` to `17`, and `adult` from `18`. Those two thresholds are
   policy rows the app reads, not constants: move a threshold and every existing
   member's band reflects it immediately, with no row rewritten.
3. The band is calendar correct. Somebody whose birthday has not yet happened
   this year is a year younger than the year subtraction says, and somebody born
   on `29 February` resolves a correct band in a non-leap year. The comparison is
   made against server-side UTC today, so one member's birthday does not land on
   two different days for two visitors.
4. Changing a date of birth is a privileged operation that writes an audit record
   naming the old value, the new value, the actor and the reason. It is not a
   profile edit, and a member cannot do it to itself.
5. Four authentication routes exist, each independently enrollable and revocable
   through `/api/auth/credentials`: `password`, `one_time_code`, `device` and
   `handoff`. Revoking one leaves the other three able to authenticate. `device`
   is a passkey: the app issues a challenge, the device answers it, and no
   password is involved. `handoff` is the cross-device route, where a code shown
   on one device is confirmed on another.
6. A session is distinct from an identity. `GET /api/auth/sessions` lists the
   live sessions for the signed-in member. Revoking one session must not revoke
   the others; revoking the identity revokes all of them. A member signed in on
   several tabs sees the same signed-out state in all of them after signing out
   in one.
7. `POST /api/auth/one-time-code` takes an `email` and sends a six-digit code to
   that account's address and nowhere else. The message subject begins `Kavora
   sign-in code: ` followed by the account's username, so a code for `Nova Pilot`
   reads `Kavora sign-in code: Nova Pilot`, and the code itself is the first
   six-digit number in the body. `POST /api/auth/one-time-code/verify` takes the
   same `email` with the `code`, accepts the code once within `600` seconds, and
   answers with an `access_token`. A wrong code, a reused code or an
   expired code is refused and issues no session.
8. Capability discovery is anonymous. `GET /api/auth/metadata` answers, with no
   session, which of the four routes exist and which are offered right now. `GET
   /api/users/agreements` answers which agreements this visitor must accept. `GET
   /api/users/authenticated` is the one call about a specific member, and it is
   refused without a session. A surface that had to sign in before it could learn
   how to sign in would never render.
9. Account creation is gated against automated signup. The gate is first party:
   the signup form carries an unattended decoy field named `nickname_confirm`
   that a person never fills, and the same form submitted repeatedly in quick
   succession from one origin is refused. **The gate fails closed**: if its own check cannot complete, account
   creation is refused rather than waved through.
10. Password is at least `8` characters. A signup that fails any rule is rejected
    as invalid, names the field at fault, and writes no row.
11. Agreement text is fetched per visitor and per surface from
    `GET /api/users/agreements`, never embedded in the page. Acceptance is
    recorded with the agreement's version and locale, appended and never updated,
    so publishing a new version leaves the original acceptance record unchanged
    and still naming the old version. Whether a new version requires
    re-acceptance is a stored property of the agreement, not a code branch.
12. Account deletion cascades to an enumerated set of records and states which
    records survive: ledger entries and moderation decisions survive, because a
    ledger that can be edited is not a ledger, and the surviving rows carry no
    personal data.

### The Kredz ledger

Kredz are whole indivisible units. There is no fraction of a Kredz and no
floating point value anywhere on a monetary path.

1. Balances are **derived** from an append-only log of entries at
   `/api/economy/ledger`, never stored as a mutable number edited in place. `GET
   /api/economy/balance` returns the sum of the signed-in member's entries,
   computed at read time.
2. Every ledger entry belongs to a transaction, and the entries of one
   transaction sum to exactly `0`.
3. Every state-changing economic operation accepts a caller-supplied
   `idempotency_key` and is exactly-once with respect to it. The same key
   submitted a hundred times concurrently produces exactly one transaction and
   moves the balance once.
4. No `user` account balance is ever negative, including transiently. Fifty
   concurrent purchases against a balance that covers ten leave exactly ten
   succeeding, the balance at exactly `0`, and no moment at which it went below.
5. There are four transaction types with distinct entry shapes:
   `currency_purchase`, `item_purchase`, `creator_payout` and `refund`.
6. Every transaction records the actor, the reason and a `correlation_id` that
   travels with the operation across every route it touches.
7. The ledger is immutable. A correction is a new compensating transaction naming
   the original, never an edit and never a delete. After a refund the original
   transaction reads exactly as it did before and a new transaction sits beside
   it.
8. Account kinds are `user`, `creator`, `platform_fee`, `issuance` and
   `redemption`. Kredz enter the system only at `issuance` and leave only at
   `redemption`, so the total of all user, creator and platform balances always
   equals the total issued minus the total redeemed.
9. A purchase that fails leaves no partial state: no orphaned transaction, no
   entry without its partners, no balance moved halfway. A non-atomic
   multi-write that leaves half a transaction behind must never be observable:
   killing the process between two writes leaves the transaction wholly present
   or wholly absent.

### Buying Kredz

Three packs are sold for real money. Prices are integer minor units in `usd`.

| Pack code | Name | Kredz | Price |
|---|---|---|---|
| `starter-pack` | `Starter Pack` | `400` | `500` |
| `builder-pack` | `Builder Pack` | `1000` | `1000` |
| `studio-pack` | `Studio Pack` | `2400` | `2000` |

`$10.00` is `1000`, not `10.00` and not `10`.

1. `GET /api/economy/packs` lists the three packs. `POST
   /api/economy/purchases` buys one, carrying `pack_code` and
   `idempotency_key`.
2. Billing lives in `killbill`, the billing platform already running at
   `PAYMENTS_API_URL`. It is a billing platform and not a card processor: there
   is no card, no token and no decline. What exists there is accounts, catalogue
   plans and invoices.
3. Every `/1.0/kb/*` call carries HTTP Basic credentials read from
   `PAYMENTS_ADMIN_USER` and `PAYMENTS_ADMIN_PASSWORD`, the header
   `X-Killbill-ApiKey` read from `PAYMENTS_API_KEY`, and the header
   `X-Killbill-ApiSecret` read from `PAYMENTS_API_SECRET`. Writes also carry
   `X-Killbill-CreatedBy`. `GET /1.0/healthcheck` is the unauthenticated
   liveness call; `/1.0/kb/healthcheck` sits behind the tenant filter and answers
   unauthorized forever, so it can never be a health probe.
4. **Exactly one billing account exists per member**, identified by its
   `externalKey`, which is `kavora-` followed by the member's username in
   lowercase kebab-case. For `Nova Pilot` that is `kavora-nova-pilot`. The
   account is looked up with `GET /1.0/kb/accounts?externalKey=<key>`, which
   answers found when it exists and not found when it does not, and created with
   `POST /1.0/kb/accounts` carrying `name`, `externalKey`, `email`, `currency`
   and `country`. The external key is unique in the tenant, so a second attempt
   with the same key is refused by the store rather than by application code, and
   no second account appears in `GET /1.0/kb/accounts/pagination`.
5. **Exactly one invoice exists per completed pack purchase**, on that member's
   billing account, for the pack's price and currency, readable at
   `GET /1.0/kb/invoices/pagination`. Kill Bill reports an invoice `amount` as a
   decimal and its `currency` in upper case, so `1000` minor units reads as
   `10.00` and `USD` there. A purchase is complete only when that invoice exists;
   the app's own tables reflect what lives in the billing platform and never
   substitute for it.
6. A re-submitted purchase with the same `idempotency_key` produces no second
   invoice, no second Kill Bill account and no second Kredz credit.
7. On completion the app writes a `currency_purchase` transaction crediting the
   member's `user` account with the pack's Kredz and debiting `issuance` by the
   same amount, and sends a receipt.
8. The receipt is addressed to the buying member's email address, with no cc and
   no bcc. Its subject begins with `Kredz receipt: ` followed by the pack name,
   so a `Builder Pack` receipt reads `Kredz receipt: Builder Pack`. The body is
   not empty and names the pack, the Kredz credited and the price paid.
9. **The non-transition rule:** a marketplace item purchase, a payout, a refund
   and a refused pack purchase send no email at all. Only a completed pack
   purchase sends a receipt, and it sends exactly one.
10. `GET /api/economy/purchases` lists the signed-in member's own pack purchases
    with their invoice reference, and no other member's.

### The marketplace

Items are priced in Kredz by their creator. `GET /api/economy/items` lists the
catalogue; `GET /api/economy/items/{slug}` returns one; `POST
/api/economy/items/{slug}/purchase` buys it, carrying `idempotency_key`.

| Item slug | Name | Creator | Kredz | Minimum band |
|---|---|---|---|---|
| `aurora-visor` | `Aurora Visor` | `Vale Studio` | `75` | `child` |
| `nebula-glider` | `Nebula Glider` | `Vale Studio` | `250` | `child` |
| `copper-hoverboard` | `Copper Hoverboard` | `Hollow Forge` | `3` | `child` |
| `meridian-banner` | `Meridian Banner` | `Hollow Forge` | `1` | `child` |
| `vault-key` | `Vault Key` | `Vale Studio` | `400` | `teen` |

1. A purchase is **one** transaction with at least three entries: the buyer
   debited the gross, the creator credited the creator share, the platform fee
   account credited the platform share. They sum to `0`.
2. The split is configuration, versioned, and the version is written onto the
   sale. The seeded rate is version `1`, taking `30` of every `100` Kredz for the
   platform.
3. The split is computed in whole Kredz. **Compute the platform share by
   truncation and give the remainder to the creator.** One rule, applied
   everywhere, and creator share plus platform share always equals the gross
   exactly.

   | Gross | Platform share | Creator share |
   |---|---|---|
   | `75` | `22` | `53` |
   | `250` | `75` | `175` |
   | `3` | `0` | `3` |
   | `1` | `0` | `1` |
   | `400` | `120` | `280` |

   The `3` row is the one that disambiguates the rule: three Kredz split thirty
   to seventy is `0.9` and `2.1`, and both must become whole numbers that still
   sum to `3`.
4. A price change never applies retroactively. Changing an item's price after a
   sale leaves the completed sale's gross, shares and rate version exactly as
   they were, and a report regenerated after a rate change splits every past sale
   exactly as before.
5. Items are versioned and a purchase records the version bought. Publishing
   version two leaves version one resolvable and unchanged.
6. A purchase is refused, with nothing written, when: the buyer's balance is
   short; the buyer's derived age band is below the item's minimum band; the item
   is not in a published state; or the buyer is the item's own creator.
7. `player3@example.com` holds exactly `75` Kredz and `Aurora Visor` costs
   exactly `75`. Two simultaneous purchases of it from that account must not both
   succeed: exactly one wins, the other is refused, and the balance never goes
   below `0`.
8. `GET /api/economy/sales` returns the signed-in creator's own sales and nobody
   else's, each carrying `gross_kredz`, `creator_kredz`, `platform_kredz` and
   `rate_version`.

### Creator payouts

A payout converts a creator's Kredz balance to money owed, at a rate that is
versioned and recorded on the payout. It is a `creator_payout` transaction in the
same ledger, never a second money system with its own balance column.

1. `GET /api/economy/payouts/eligibility` returns six conditions, each separately
   true or false and each separately explainable: `age_band`,
   `identity_verified`, `tax_documents`, `minimum_balance`, `good_standing` and
   `region_supported`.
2. `POST /api/economy/payouts` requests a payout. A creator who is ineligible is
   refused with the **name of the condition that failed**, never an opaque
   refusal. `creator2@example.com` is seeded with `tax_documents` unmet, and its
   refusal names `tax_documents`.
3. A member below the `adult` band fails `age_band` and can never be paid.
4. The minimum balance is `100` Kredz.
5. A payout request that exceeds the creator's **derived** balance is refused and
   writes no ledger entry.
6. A settled payout's entries debit the creator account and credit `redemption`,
   and sum to `0`, so the system-wide total still equals issued minus redeemed.

### The creator publishing pipeline

Publishing runs through explicit stages. `POST /api/creator/assets` submits,
`GET /api/creator/assets` lists the signed-in creator's own assets, and `PATCH
/api/creator/assets/{id}` edits one.

1. The asset states are `uploading`, `uploaded`, `validating`,
   `pending_moderation`, `approved`, `deriving`, `published`, `rejected`,
   `unpublished` and `deleted`, and the only permitted moves between them are:

   | State | May move to |
   |---|---|
   | `uploading` | `uploaded`, `failed` |
   | `uploaded` | `validating`, `failed` |
   | `validating` | `pending_moderation`, `rejected`, `failed` |
   | `pending_moderation` | `approved`, `rejected` |
   | `approved` | `deriving` |
   | `deriving` | `published`, `failed` |
   | `published` | `pending_moderation`, `unpublished` |
   | `rejected` | `pending_moderation` |
   | `unpublished` | `published`, `deleted` |

   Any move not in that table is refused. A state is a closed set, not free text.
2. An asset is visible to nobody but its creator until it has passed every gate
   and reached `published`.
3. Upload, validation, moderation, derivation and publication are separate
   stages, each idempotent and independently retryable. Replaying a stage twice
   creates no duplicate record and does no duplicate work.
4. Validation runs before moderation, because it is cheap and mechanical. Five
   checks: a declared type that disagrees with the payload's own content is
   rejected; a size outside bounds is rejected; a structural integrity check
   rejects a malformed payload that would crash a renderer; a payload past its
   complexity bound is rejected because it is valid but too expensive to render;
   and a malware scan rejects the obvious, taking the industry test string
   `EICAR-STANDARD-ANTIVIRUS-TEST-FILE` as its known-bad marker. It never trusts a
   client-declared type or size, and it runs before the payload reaches any
   renderer.
5. **Editing a moderated field re-enters moderation.** Renaming a `published`
   asset returns it to `pending_moderation` and withdraws its derived imagery
   until it is approved again. Checking only on the way in is not checking.
6. A stage failure leaves the asset in a defined state with an operator-readable
   reason, never silently stuck.
7. Assets are versioned. Publishing a new version never mutates the old one.

### Derived preview imagery

Every asset carries preview imagery at three sizes, `small`, `medium` and
`large`. Deriving it is asynchronous, can fail, and can be re-run.

1. `GET /api/thumbnails/previews` answers **by asset and size** and returns a
   **state**, not only an address. The states are `pending`, `ready`,
   `unavailable` and `blocked`.
2. `pending` is a normal, expected, frequently returned answer. A client renders
   a defined placeholder for it and does not treat it as an error. An asset
   published a moment ago answers `pending`, and its page shows the placeholder
   rather than a broken image.
3. Derivation is idempotent per asset version and size: the same asset, version
   and size derived twice produces one record and does no second piece of work.
4. When an asset re-enters moderation its derived imagery is withdrawn and
   answers `blocked` until it is approved again.
5. Preview requests are batched: `GET /api/thumbnails/previews` accepts a list of
   asset ids and answers them in one response.
6. The preview itself is generated deterministically from a seed that is the
   asset id, its version and the size joined by colons, so `41:2:medium` always
   produces the same artwork on every load and every machine.

### Discovery, charts and the scoped search

1. One query resolves against four scopes from one input: `games`,
   `marketplace`, `communities` and `creator_store`. The visitor types first and
   chooses the scope afterwards. `GET /api/games/search` takes `q`, `scope`,
   `cursor` and `limit`.
2. Results are paginated **by cursor**, never by a numeric offset. The cursor is
   opaque and encodes both the sort position and the ranking version.
3. The sort key is stable and total: it always ends with a unique tiebreak, so
   two equally ranked rows never swap between two queries. Paging through a list
   whose scores are changing shows every row exactly once and skips none, and
   asking for a deep page costs no more than asking for an early one.
4. If the ranking version changes part way through paging, the cursor is either
   refused or continues consistently. It never silently mixes two versions.
5. Ranking inputs are enumerated, versioned, and the version is recorded on the
   response: engagement over a defined recent window of `30` days; retention, which
   distinguishes a genuinely good experience from a heavily promoted one;
   recency of publication as the new-content term; creator standing; and viewer
   locale as a weight.
6. **Age eligibility is a filter applied before ranking, never a weight.** A
   weight can be outranked; a filter cannot. `Deep Vault Heist` has a minimum
   band of `teen` and must not appear at any depth for `player2@example.com`,
   whose band is `child`.
7. A result page is never served to a viewer whose age band or locale differs
   from the viewer it was computed for.
8. An empty result is a defined state, distinguishable from a failure, and the
   page says so rather than showing nothing.
9. `GET /api/games/charts` returns the ranked experiences, under the same filter,
   cursor and tiebreak rules.
10. The default page `limit` is `20` and the server bounds it.

### Joining an experience

Joining an experience is realtime in the sense that matters here: a slot is
committed the instant it is promised. Joining is two phase, reserve a slot then
connect, and matchmaking chooses the instance.

| Experience slug | Name | Creator | Minimum band | Capacity | Occupied |
|---|---|---|---|---|---|
| `sky-forge-arena` | `Sky Forge Arena` | `Vale Studio` | `child` | `8` | `7` |
| `deep-vault-heist` | `Deep Vault Heist` | `Hollow Forge` | `teen` | `16` | `0` |
| `lantern-drift` | `Lantern Drift` | `Vale Studio` | `child` | `12` | `4` |

1. `POST /api/games/{slug}/join` selects an instance, **decrements its free slots
   at that moment**, and returns a reservation token with an expiry. Capacity is
   committed at reservation, not at connection, so matchmaking always knows how
   many people are already on their way. Counting connections instead of
   reservations sends a thundering herd of a thousand simultaneous joiners to
   one instance that still looks empty, and this must not happen.
2. A reservation lives for `120` seconds. If nobody connects, it is released
   automatically and its slot returns, exactly once.
3. `POST /api/games/reservations/{token}/connect` consumes the token, registers
   presence, and can never be consumed a second time.
4. `Sky Forge Arena` has exactly one free slot. Two simultaneous joins must not
   both succeed: exactly one reservation is issued, the other is refused, and the
   instance is never oversubscribed. Free slots never go below `0`.
5. Three ways to join, all through the same reservation: join a named instance,
   join a friend, or be placed automatically. Joining a friend whose instance is
   full is refused with the reason named and an offer of placement elsewhere.
6. Placement respects region, capacity, fill policy and the viewer's age band.
   An age-ineligible join is refused **at placement**, before any instance is
   contacted.
7. Presence is a lease, not a record. `POST /api/games/presence` refreshes it,
   and it expires after `60` seconds without a refresh. An instance killed
   without a clean shutdown leaves no member shown as present after the lease
   window.
8. Instance lifecycle is explicit: `requested`, `starting`, `ready`, `draining`,
   `terminated`.

### Safety, moderation and enforcement

1. Moderation is multi stage: an automated classification first, then a human
   review queue for anything the classifier does not decide confidently. Content
   waiting in that queue is visible to nobody but its creator.
2. Every moderation decision records the subject, the subject's version, the
   decision, the basis, the actor and the time, appended and never edited.
3. Enforcement is graduated and enumerated, not a single ban flag: `clear`,
   `warned`, `content_removed`, `capability_restricted`, `suspended` and
   `terminated`. Each state names exactly which capabilities it removes:
   `warned` is recorded and changes nothing; under `content_removed` one item is
   actioned and the account is unaffected; under `capability_restricted` named
   capabilities are suspended while the account stays usable. A
   `suspended` action carries an end time and lifts automatically when it passes;
   a suspension with no end is a termination nobody has taken responsibility for.
4. Every enforcement action is appealable, and an appeal is a state machine with
   its own audit trail: `submitted`, `in_review`, `upheld`, `overturned`. The
   appellant can see its own appeal and where it has reached. An appeal inbox
   with no states cannot be counted, aged or escalated, and is not what this
   product has.
5. Communication capability is derived from the age band and applied **server
   side**. `POST /api/users/messages` is the one route that carries a message
   between members, and a restricted member calling it straight, bypassing the
   interface, is refused. Filtering that lives in the interface is
   a suggestion, not a restriction.
6. Reporting is available to every member on every member-generated surface.
7. Retention and deletion obligations are enumerated per data class, each with a
   defined period, and deletion runs.

### Telemetry, localisation, flags and experiments

1. `POST /api/metrics/events` records four kinds of event: `authPageload` when an
   authentication surface renders, `pageHeartbeat` while a surface stays open,
   `userInteractions` when input activity occurs, and `batMissing` when an
   expected device-bound token is absent. Every event carries an application
   name, an event name, a context and a timestamp.
2. Liveness is sampled at escalating intervals, not a fixed one. Three tiers
   exist, `heartbeat1`, `heartbeat2` and `heartbeat3`. The observed contexts also
   include `mouse` for input activity, `hba` for the missing device token,
   `loginPage` and `passkeyLogin` for the login surface, `MultiverseSignupForm`
   for the signup wall, and `platformAuthenticatorSupport`, which reports whether
   the device can do a device-bound credential at all, so the product knows
   whether to offer `Quick Sign-in` before a visitor tries it.
3. Telemetry never blocks rendering and never fails a surface when the collector
   is unreachable, and it survives page unload.
4. **No event carries personal data.** Each event carries the current address,
   and any route whose address contains a member identifier is enumerated and has
   that identifier redacted before the event is emitted. `GET
   /api/metrics/page-views` records each page view with its route and timestamp
   and is readable by the member it belongs to.
5. No user-facing string is a literal in a component. Every string resolves from
   a namespaced bundle at `GET /api/locale/bundles/{namespace}`, and a surface
   loads only the namespaces it uses. The chrome's own strings live in the
   `navigation` namespace, so `GET /api/locale/bundles/navigation` answers the
   nav, the footer and the search scopes. `GET /api/locale/locales` lists the
   supported locales.
6. The active locale is part of the address, so a shared link lands in the same
   language the sharer saw. Every internal footer link carries it.
7. A missing key falls back through a defined chain and never renders the raw
   key. Bundles are versioned and cached separately from the application.
8. Plural and gender forms are expressible: a flat key-to-string map cannot
   express a language with more than two plural forms, and this one does. Text
   expansion is the other risk, and a non-latin locale left untested is where it
   lands: a pseudo-locale that runs a third longer than English overflows no
   card, at any width.
9. Feature flags and experiments are **two separate systems** with separate
   stores. The feature-flag service carries the internal codename `flagsvc` and
   the editorial content-bundle service carries the internal codename
   `bundlesvc`. `GET /api/flags` answers whether a capability is switched on for
   an application and a namespace; the same flag name may exist independently in
   two applications, and a surface fetches only its own namespace. `GET
   /api/flags/override-status` answers the per-user overrides layered on top of
   them. A flag is operational, changes without ceremony, and has no statistical
   meaning.
10. `GET /api/experiments/layers` answers which variant a unit is in. A **layer**
    is a set of mutually exclusive experiments: a unit belongs to at most one
    experiment per layer, so two experiments that would interfere can never both
    apply. Some layers assign by member, others by device, and the layer says
    which.
11. Experiment assignment is **deterministic**: a pure function of a stable
    identifier and the layer, computed identically everywhere, stable for the
    life of the experiment, and stored nowhere. The same member gets the same
    variant on two devices, and clearing a device's storage does not re-roll it.
12. `POST /api/experiments/exposures` records an exposure **at the moment the
    variant changes what the visitor sees**, not at the moment the assignment is
    fetched.
13. `GET /api/flags/prelude` is the client bootstrap call: one request returns
    the latest prelude a surface needs, its flags and its experiment
    assignments together, so nothing is fetched twice. Both resolve before first
    paint of the surface that depends on them, and both have a defined value
    when resolution fails. An anonymous caller gets a
    defined answer, and the surface renders a defined state from it. Which of the
    four authentication routes the login surface offers is decided by an
    experiment rather than being fixed.

### The public surfaces

1. `/` is the signup wall. It is the only surface without the full chrome: a bare
   wordmark and a single `Log In` action, because a visitor who has never signed
   in has nothing to navigate to.
2. `/login` is the login surface, carrying the full chrome and offering the
   authentication routes the experiment selects.
3. An unknown address renders the product's own **not-found** surface, with the
   full chrome so the visitor can navigate out, a heading reading `Something went
   wrong`, the code `404`, a vertical bar separator marked decorative so it is
   not announced, an explanation reading `Page not found`, and two actions
   reading `Back` and `Home`. It answers a not-found status, never a
   success status carrying not-found content, and it never redirects to the
   signup wall.
4. Every internal link on every public route resolves.
5. Every form rejects invalid input inline, names the field at fault, and writes
   nothing.
6. A privacy page at `/info/privacy`, reachable from the footer of every page,
   states what Kavora stores about a member, which records survive account
   deletion and for how long each data class is kept. A terms page at
   `/info/terms`, reachable from the same footer, carries the terms the agreement
   paragraph links to. An accessibility statement lives at `/info/accessibility`.
7. A `sitemap` at `/sitemap` lists every public route for a person, `/sitemap.xml`
   lists the same routes for a machine, and `/robots.txt` points at it.
8. Each page leads with one clear primary action, visually distinct from every
   secondary one.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the age-gated signup wall | anonymous |
| `/login` | the login surface, four routes | anonymous |
| `/charts` | ranked experience discovery | anonymous |
| `/marketplace` | the item catalogue | anonymous |
| `/marketplace/{slug}` | one item in the detail pane | anonymous |
| `/search` | scoped results, one scope at a time | anonymous |
| `/kredz` | balance, ledger and pack catalogue | player |
| `/kredz/packs/{code}` | one pack and its price | player |
| `/play/{slug}` | reserve a slot in a running instance | player |
| `/settings/sessions` | enrolled credentials and live sessions | player |
| `/create` | the creator dashboard | creator |
| `/create/new` | publish a new asset | creator |
| `/create/payouts` | payout eligibility and history | creator |
| `/info/privacy` | what the platform stores | anonymous |
| `/info/terms` | the terms a member agreed to | anonymous |
| `/info/accessibility` | the accessibility statement | anonymous |
| `/sitemap` | every public route, listed | anonymous |

**Entry and redirects.** An anonymous visitor asking for a protected route lands
on `/login` and continues to the route they asked for once signed in. A signed-in
visitor asking for `/` or `/login` lands on `/charts`. Signing out returns to `/`
and ends that session only, and every open tab of that session agrees within one
navigation. A token that expires part way through an action leaves the action
undone, says the session ended, and offers the login surface. A `player` asking
for a `creator` route is refused by the server and shown the not-found surface.
An unknown address renders the not-found surface.

**Journeys.**

1. Open `/`. The card asks Birthday first, as three selects placeheld `Month`,
   `Day` and `Year`. Enter a date, a username, a password, optionally a gender,
   read the agreement, press `Sign Up`. A toast confirms and `/charts` opens with
   the derived band already applied.
2. Open `/login` as `player@example.com`, press `Email Me a One-Time Code`, read
   the code from the message that arrives, enter it, and land on `/charts`.
3. Open `/kredz` as `player@example.com`. The balance reads `1000`. Open
   `/kredz/packs/builder-pack` and buy. The balance reads `2000`, the receipt
   arrives, and the purchase is listed with its invoice reference.
4. Open `/marketplace`, select `Aurora Visor` in the list. The detail pane shows
   `75` Kredz and `Vale Studio`. Press Buy. A toast confirms, the buyer's balance
   drops by `75`, and `Vale Studio` gains `53`.
5. Open `/create` as `creator@example.com`, press New, and `/create/new` opens.
   Name the asset, declare its type, paste its payload, publish. It moves through
   `validating` and `pending_moderation`, and its preview reads `pending`.
6. Select a `published` asset and rename it in the detail pane. It returns to
   `pending_moderation` and its preview reads `blocked`.
7. Open `/create/payouts` as `creator2@example.com`. Five conditions read met and
   `tax_documents` reads unmet. Press Request. The refusal names `tax_documents`
   and no ledger entry is written.
8. Type `vault` in the header search. The suggestions offer the same words `in
   Games`, `in Marketplace`, `in Communities` and `in Creator Store`. Choose
   Games. `/search` opens in that scope. Page forward twice; nothing repeats and
   nothing is skipped.
9. Open `/play/lantern-drift` as `player@example.com`. Eight slots are free.
   Press Play. A reservation is issued and the free count drops at once. Connect
   with the token and presence registers.
10. Open `/no-such-place`. The not-found surface renders with the full chrome and
    offers `Back` and `Home`.

**States.** Every list has an empty state that says what would fill it: no items,
no payouts, no sessions, no results for this query in this scope, no running
instance. Every page has a loading state, and a `pending` preview renders a
placeholder that stays visibly distinct from loaded content. Errors never crash
the application: a refused action leaves the page where it was, names the field
or the condition at fault, and writes nothing.

## UI/UX notes

The north star: a visitor understands in the first moment that everything here
was made by somebody else who uses it, and that the way in is to say how old they
are. The register is consumer with an operational spine. The catalogue and the
charts put the subject first and may carry atmosphere; the creator dashboard, the
payout ledger and the moderation queue read quiet and dense, built for scanning
and repeated action. The stance is subject over chrome on the public surfaces and
density over air on the creator ones, and a competing platform could rationally
hold the opposite.

**Everything is a token.** Every colour, size, radius, duration and easing
resolves from a named token, and no component carries a literal value. Two tokens
name the system from inside itself: the current design system is `Bedrock`, and a
token records that the previous system, `Ironworks`, exists and is not active.

Everything dimensional derives from one base interval, and the reading size is
two intervals. A reciprocal text-scale token holds line heights stable when a
visitor scales text up, so text that grows does not get leading that grows
faster. Six parallel scales share one vocabulary running none, xxsmall, xsmall,
small, medium, large, xlarge, xxlarge: gap, padding, gutter, margin, radius and
icon size, with separate scales for input and toggle control sizes. Radius runs
from square through a pill. Stroke is thin, standard, thick and thicker against a
stroke base of one. Controls take their height from the control scale, never from
padding plus line height, which is what keeps a text field and a select the same
height when their contents differ; every control on the signup form is one
height.

**Colour is named for the job it does.** Every interactive role resolves three
slots in one order, background then border then foreground, and a role with no
border resolves it to transparent rather than omitting it, so a component can
bind all three unconditionally. The roles are alert, emphasis, link, over-media,
soft-emphasis, standard, sub-emphasis, subtle and utility. Four families share
one naming convention: semantic roles as `--color-<role>-<variant>-<slot>`,
content weights as `--color-content-<weight>`, common uses as
`--color-common-<use>`, which is where the backdrop scrim and the shimmer live,
and the extended ramp as `--color-extended-<hue>-<step>`.

| Role | The colour |
|---|---|
| the primary action's background | a light, vivid blue, and the only thing on a page wearing it |
| the primary action's foreground | a near-white neutral |
| the colour that means something failed, and it appears nowhere else | a mid, vivid red, with a light, vivid red as its softer partner |
| the colour that means something succeeded | a mid, soft teal |
| default body content | a deep cool neutral |
| emphasised content | a deep neutral |
| muted content | a mid cool neutral |
| a link | a mid, vivid blue, distinct from the action blue |
| a subtle border | a deep cool neutral |
| the soft-emphasis foreground | a deep, soft blue |
| the deepest ground, and the raised card above it | a near-black neutral, then a deep cool neutral |
| a quiet rule or a disabled edge | a light cool neutral |
| a pale accent on artwork | a light, vivid blue |
| the backdrop behind a dialog | black at half opacity |
| the shimmer that says content has not arrived | a barely-there blue wash |

One token resolves through a colour-mixing function rather than a flat value: the
soft-emphasis background is the action blue mixed at three tenths into
transparency, and the mix is reproduced rather than flattened, because it
composites differently over the three colour modes. The exact shades are yours,
so long as each holds its role and its exclusivity rule and meets the contrast
bar in all three modes.

**Type.** A text family of several weights and a wider companion for display.
Name both as tokens with a fallback stack present on the target platforms, metric
compatible so the swap does not reflow, and let no component name a family.
Declare only the weights you actually use: the reference declared a text family
in seven weights and a display family in five, normal and italic for each, and
loaded four. There are eighteen roles, each resolving a font shorthand and a
letter spacing:

| Role | Weight | Size in base units | Line height | Letter spacing |
|---|---|---|---|---|
| display-large | 700 | 20 | 120% | -0.01em |
| display-medium | 700 | 14 | 120% | -0.01em |
| display-small | 700 | 10 | 120% | -0.01em |
| heading-large | 700 | 7 | 120% | -0.01em |
| heading-medium | 700 | 6 | 120% | -0.01em |
| heading-small | 700 | 5 | 120% | -0.01em |
| title-large | 700 | 4 | 140% | 0em |
| title-medium | 700 | 3.5 | 140% | 0em |
| title-small | 700 | 3 | 140% | 0em |
| label-large | 600 | 4 | 100% | 0em |
| label-medium | 600 | 3.5 | 100% | 0em |
| label-small | 600 | 3 | 100% | 0em |
| body-large | 400 | 4 | 140% | 0em |
| body-medium | 400 | 3.5 | 140% | 0em |
| body-small | 400 | 3 | 140% | 0em |
| caption-large | 600 | 3.5 | 140% | 0em |
| caption-medium | 600 | 3 | 140% | 0em |
| caption-small | 600 | 2.5 | 140% | 0em |

Four line heights exist and only four: 100%, 120%, 130% and 140%. Three letter
spacings exist: -0.01em, 0em and 0.01em. Display and heading roles pull their
letters slightly closer together; label roles take no leading at all, because a
label sits alone inside a control and any breathing room would decentre it.
Figures align wherever amounts stack: balances, prices, splits and payout rows.

**Icons.** Every icon is inline vector markup in the document, sized from the
icon scale, taking its colour from the current text colour, and carrying a name a
screen reader can announce. One copy of each mark. The reference delivered every
glyph as a background image behind an empty element instead: some encoded
directly into the stylesheet, including the wordmark, the search glyph and the
chevron on each date dropdown, and others fetched as separate vector files.
Neither mechanism is used here. A pale copy and a dark copy of the same geometry
shipped as two images is the thing this replaces, along with the request per
glyph and the missing accessible name that came with it.

**Motion.** Five easing characters and no others, one token each:
`--ease-linear` has no acceleration; `--ease-standard-in` leaves slowly and
arrives fast; `--ease-standard-out` leaves fast and settles slowly;
`--ease-expressive-in` anticipates, pulling back before it goes; and
`--ease-expressive-out` overshoots and settles back. The two expressive characters travel outside their
own start and end positions, so reserve them for something a visitor summoned
deliberately: a dialog, a sheet, a confirmation toast. Everything else uses the
calm pair.

There are five families of named animation, and every one of them must animate to
a consistent character across the whole product. A loading shimmer sweeps across
a placeholder at a slight skew. Sheet transitions pair an entrance and an exit for
four directions plus a fade, and a sheet travels a fraction further than its own
width so its shadow does not linger at the screen edge. A dialog pairs a backdrop
fade with a content scale that starts a fraction under full size, so it reads as
arriving rather than popping. Progress appears in four forms: a bar whose width
and offset move in stops, a rotating circle, a striped bar and a three-bar
loader. The utility family covers a rotation, a delayed fade, a chip entry that
scales in and a short downward slide that returns.

Every animation has a defined reduced-motion behaviour, and a visitor who has
asked for reduced motion gets it everywhere. The default is to hold the end state
and skip the transition. The loading shimmer is the one exception: it stops
moving and must stay visibly distinct from loaded content, because its whole job
is to say that something has not arrived yet. Durations are yours; the character
and the uniformity are not.

**Colour modes.** Three, from one token set, switchable without a reload: light,
dark, and an inverse palette that opposes whichever of the two is active, for a
surface that must contrast with the current mode rather than agree with it. A tooltip over artwork, a toast above the page
and a control resting on media all bind the over-media role, which holds a deep
neutral ground and a near-white neutral foreground whatever the mode is. One
mechanism only: the mode is set on the root element, every token resolves from
it, and components bind roles. There is no second forcing class anywhere, and no
mark ships in two colours.

**Chrome.** A header fixed to the top, dark, holding from left to right: the
square mark, four nav destinations reading `Charts`, `Marketplace`, `Create` and
`Kredz`, the search input with its submit glyph, and one right-hand action
reading `Sign Up`. The search suggestion menu offers the typed words against four
scopes suffixed `in Games`, `in Marketplace`, `in Communities` and `in Creator
Store`, and the visitor picks the scope after typing rather than before. A skip
link reading `Skip to Main Content` sits above the top edge and becomes visible
on focus; it is a genuine affordance and it survives. A footer holds ten items in
order: `About Us`, `Jobs`, `Newsroom`, `Parents`, `Buy Gift Cards`, `Help`,
`Terms`, `Accessibility`, `Privacy` and `Sitemap`, plus a language selector that
is a button rather than a link and opens the locale menu. The copyright line
names `Kavora Interactive` and the year, followed by a trademark notice. Hover is
one consistent lift in content weight, the same on every surface.

**The signup wall.** A generated tile field fills the section behind the card,
darkened by a radial scrim that is brighter at the centre than at the edges, so
the card sits in the brightest part of the field. The card is a raised near-black
panel holding a heading that reads `Sign up and start having fun!`, then four
fields in this order: Birthday as three selects placeheld `Month`, `Day` and
`Year`, with months `January` through `December` and days `01` through `31` zero
padded; `Username`, placeheld `Don't use your real name`; `Password`, placeheld
`At least 8 characters`, with a visibility toggle; and `Gender (optional)` as two
buttons inside one bordered box, each iconic and each still carrying a name. Both
of those placeholders are doing more than they look: one is a safety instruction
wearing the costume of a form hint, and the other states the rule before the
visitor can break it. Under every field sits an empty message slot, held open
before any error exists, so nothing below it moves when a message appears.
Reproduce that exactly. Below the fields, the agreement paragraph with its links
to `Terms of Use` and `Privacy Policy`, then the submit at full card width. Below
the card, a heading reading `Kavora on your device` and a row of eight storefront
pills, each a rounded outline with a small label above a larger name and a
generic inline glyph, carrying no third-party mark.

**The login surface.** A card carrying a heading that reads `Log in to Kavora`,
an identifier field and a password field whose labels are present and visually
hidden, a submit reading `Log In`, a recovery link reading `Forgot Password or
Username?`, a divider, then `Email Me a One-Time Code` and `Quick Sign-in`, then
a prompt reading `Don't have an account?` followed by `Sign Up`. One label
pattern across the whole product, and the visible label of the signup wall wins,
because a placeholder-only field loses its label the moment the visitor types.
The signup card and the login card take the same card token.

**The signed-in surfaces.** The marketplace, the charts, the creator dashboard
and the payout ledger are a split detail pane: the list holds the left, the
selected row opens on the right, and the list is never lost when a row is
inspected. Rows sit tight enough that a full page fits one screen. Publishing
takes its own address rather than a dialog, because it has a lifecycle a visitor
must be able to return to. Confirmations arrive as a toast bound to the
over-media role, and that toast is where the expressive-out character belongs.

**Responsive.** Five breakpoints, from the token set, and no second set anywhere;
the product must be responsive at every width between them, not only at the named
tiers. No horizontal overflow at any width from the narrowest upward. One copy of
every navigational element, never one hidden copy per end of the range, so no
invisible item sits in the focus path. Search stays reachable at every narrow
viewport, collapsing to an icon that expands rather than vanishing. Every
interactive target meets the minimum touch size at the two narrower widths. The
signup card holds its width at the two wider tiers and goes edge to edge at the
narrowest, and the footer wraps onto more rows as the window narrows, which is
why the header and the footer both change height as the window does.

**Accessibility.** Text meets WCAG AA contrast against its background, verified
per token pair in all three colour modes rather than by eye on a screenshot.
Keyboard navigation reaches every interactive element with a visible focus ring
against all three modes, in a focus order matching the visual order. Every
control carries a programmatic name, including the icon-only ones. Validation
errors are announced as well as rendered and are associated with their field.
Meaning is never carried by colour alone. Landmark structure, header, nav, main
and footer, is present on every surface. The age gate, three adjacent selects and
two icon buttons, is the hardest part of the product to operate without a pointer
and is fully operable by keyboard.

**Assets.** The build ships no binary. The background mosaic and the separate
vignette image the reference fetched beside it are folded into one declaration
and generated. The mosaic is a generated tile field: rounded rectangles at a four-by-three aspect, seeded sizes and slight
seeded rotations, overlapping by up to a fifth of their width and drawn back to
front, each filled with a two-stop gradient at a seeded angle, drawn from the
extended ramps and never from the action roles, so the artwork can never be
mistaken for something to click. Enough tiles to cover the widest breakpoint plus
a tile of bleed, no text and no representational imagery, and the same seed
produces the same artwork on every load and every machine. The eight storefront
badges are generated pills. The locale flag is replaced by the locale's language
tag set in the small label role, which is more accurate anyway, because a flag
names a country and the selector chooses a language.

**What this must not look like.** Not a page dominated by one hue family with no
second signal. Not decoration standing in for content. Not a marketing
composition where the working interface belongs. Not three generations of
component style coexisting on one screen.

## Front-end specification

This section carries the front-end detail that does not fit the notes above. It
is specification, not decoration.

**One component system, one token set.** The reference this product is drawn from
ran three generations of interface at once: a grid-and-component framework of the
mid twenty-tens, a first-party component library of the late twenty-tens, and a
current design system of some six hundred tokens, with two rival component
frameworks and a document manipulation library present as runtime globals on the
same page. That is evidence about the reference, not an instruction. Render every
surface from a single component system and a single token set, with one class
naming convention held throughout. The token vocabulary is the one thing worth
reusing from the reference: semantic role first, slot last.

**The information architecture.** Three public surfaces, one shared chrome, four
nav destinations and one scoped search: that is the whole navigable shape before
anyone signs in, and the module and component architecture follows it rather than
the other way round. One component system, one token set, one class naming
convention, one module system, one typography scale and one iconography
mechanism. The reference's own observed implementation, its coexisting runtime
globals and its published bundles, is informational evidence about how it grew
and is never a design to copy.

**The defects that are corrected rather than reproduced.** Twelve, and each one
is a requirement here: one interface generation instead of three; inline vector
icons with accessible names instead of background images; one colour-mode
mechanism on the root instead of two that disagree; one copy of each mark instead
of a pale one and a dark one; one control height on the signup form, taken from
the control scale, instead of three; one card token shared by the signup and
login cards instead of two unrostered greys; one navigation element instead of a
second hidden copy; search reachable at every width instead of absent at the
narrowest; the token breakpoints used everywhere instead of a second undeclared
set; one label pattern instead of two; one spelling of log-in; and `Page not
found` capitalised normally.

**Performance.** Three findings shape this. Fonts are the heaviest class the
reference ships, because it declares many more weights than it loads. The
background artwork is the heaviest single asset, on a surface whose whole job is
four fields and a button. Script count follows module count, which is what the
one-module-system rule above is for.

**Surface inventory.** Three surfaces carry the public chrome shape. The signup
wall replaces the nav with a bare wordmark and one action. The login surface and
the not-found surface both carry the full chrome, including the nav and the
search. Seven different unknown paths must resolve to one identical not-found
surface, not seven variants of one.

**The link graph.** The signup wall carries internal links to `/login`, to
`/info/terms` and `/info/privacy` inside the agreement paragraph, and, in the
footer, to `/info/about-us`, `/info/jobs`, `/info/blog`, `/info/parents`,
`/info/help`, `/info/terms`, `/info/accessibility`, `/info/privacy`,
`/giftcards` and `/sitemap`. Every footer link carries the active locale. The
only outbound links on the surface are the eight storefront pills.

**The four nav destinations** each lead somewhere real: `Charts` to ranked
experience discovery, `Marketplace` to the item catalogue, `Create` to the
creator surface, and `Kredz` to currency purchase.

**Machine-readable hooks.** The three birthday selects carry the stable
identifiers `MonthDropdown`, `DayDropdown` and `YearDropdown`, in that order, so
the age gate can be driven without a pointer. The search input, the search submit
and the skip link each carry a stable identifier of their own.

**Component states.** Every component defines its resting, pointed-at, pressed,
focused and unavailable states and how it behaves in each. Escape closes an open
overlay. A destructive action confirms first. An unavailable control is never
signalled by colour alone.

**Copy deck.** These strings are fixed and are resolved from locale bundles, not
written into components.

| Where | Copy |
|---|---|
| signup wall document title | `Kavora` |
| login document title | `Log in to Kavora` |
| not-found document title | `Kavora` |
| signup header action | `Log In` |
| signup card heading | `Sign up and start having fun!` |
| birthday label and placeholders | `Birthday`, then `Month`, `Day`, `Year` |
| month options | `January` through `December` |
| day options | `01` through `31`, zero padded |
| username label and placeholder | `Username`, `Don't use your real name` |
| password label and placeholder | `Password`, `At least 8 characters` |
| gender label | `Gender (optional)` |
| signup submit | `Sign Up` |
| device strip heading | `Kavora on your device` |
| login heading | `Log in to Kavora` |
| login hidden labels | `Username/Email/Phone`, `Password` |
| login submit | `Log In` |
| recovery link | `Forgot Password or Username?` |
| one-time code action | `Email Me a One-Time Code` |
| device credential action | `Quick Sign-in` |
| login signup prompt | `Don't have an account?` then `Sign Up` |
| nav | `Charts`, `Marketplace`, `Create`, `Kredz` |
| search scopes | `in Games`, `in Marketplace`, `in Communities`, `in Creator Store` |
| skip link | `Skip to Main Content` |
| header right action | `Sign Up` |
| footer | `About Us`, `Jobs`, `Newsroom`, `Parents`, `Buy Gift Cards`, `Help`, `Terms`, `Accessibility`, `Privacy`, `Sitemap` |
| locale selector current value | `English (United States)` |
| not-found heading, code, explanation | `Something went wrong`, `404`, `Page not found` |
| not-found actions | `Back`, `Home` |

The agreement paragraph is fetched rather than embedded, and for the default
locale and the signup surface it reads: `By clicking Sign Up, you are agreeing to
our Terms of Use (including arbitration) and acknowledge our Privacy Policy. If
you are under 18, you agree that your parent or guardian permits you to create
this account and agrees to our Terms of Use.`

Three inconsistencies in the source copy are corrected rather than reproduced:
log-in is spelled one way throughout, `Page not found` is capitalised normally,
and one label pattern is used on both forms.

**The zero-asset substitution guide.** No third-party wordmark, logo, trade
dress, artwork or experience title appears anywhere. No font file ships. Each
asset class the reference carried has a replacement here: the photographic mosaic
and its vignette become the generated tile field; the eight storefront badges
become generated pills; the encoded and fetched icon vectors become inline
vector; the locale flag becomes a language tag; and the one-pixel image beacon
used for telemetry becomes a transport that fetches no image and still survives
page unload.

**Cross-cutting.** These hold on every surface: one nav, one module system, one
breakpoint set; search reachable at every width and no horizontal overflow; a
programmatic name on every control and an age gate fully operable by keyboard;
contrast verified per token pair in all three modes; only the font weights used,
subset per locale, behind a metric-compatible fallback; the signup form painting
before the background artwork; no binary asset and a deterministic mosaic; and no
third-party mark anywhere.

## Technical requirements

Frontend: Remix, on React Router 7. Backend: Fastify on Node 20. The rendering
model is server-rendered HTML with interactive islands: the first paint of every
public route is HTML produced on the server, and the browser receives readable
markup before any script runs. Remix's production build is served by its own
production request handler mounted inside Fastify, and the JSON API is mounted on
the same Fastify instance under the `/api` prefix on the same origin.

Datastore: PostgreSQL, reached at `DATABASE_URL`. Billing: `killbill`, reached at
`PAYMENTS_API_URL` with `PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`,
`PAYMENTS_ADMIN_USER` and `PAYMENTS_ADMIN_PASSWORD`. Mail: Mailpit, a real SMTP
server, reached at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. The app
reads `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` from the environment and hardcodes
neither.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL, `killbill` and Mailpit, and reaching for anything else is a contract
violation.

Auth is app-implemented email and password with bearer tokens. Passwords are
hashed. A bearer token expires. A forgery token is issued per session, rotated,
required on every state-changing request and validated server side; it is a
separate concern from the idempotency key, because one stops a forged submission
and the other stops a duplicated one.

The product is specified as a set of independently addressed services rather than
one undifferentiated block. Carry that boundary as route prefixes on one origin,
each answering its own readiness: `/api/auth`, `/api/users`, `/api/economy`,
`/api/games`, `/api/thumbnails`, `/api/metrics`, `/api/locale` and
`/api/creator`. `GET /api/health` returns `200` once the whole application is
ready, including its database connection.

Logging is structured, and every line for an economic operation carries the
`correlation_id` that operation was given.

No credential, API key, admin token or **secret** of any kind appears in anything
the browser downloads: not in a script bundle, not in server-rendered markup, not
in a response body.

Every response carries security headers: a strict transport policy, a nosniff
content-type policy, a frame policy and a content-security policy.
Content-security violations are reported to `POST /api/metrics/csp` and are
readable for review.

Any surface showing a page of N items issues one metadata request and one imagery
request for that page, a count that does not grow with N. Only the font weights
actually used are fetched, subset to the character ranges the active locale
needs, and text is readable before font loading completes because the fallback is
metric compatible. The signup form reaches its first contentful paint without the
background artwork: the form is the product and the artwork is decoration.

Every response for an unknown path answers a not-found status. `/robots.txt`
points at `/sitemap.xml`, and `/sitemap.xml` lists every public route.

## Data model

Fourteen groups of table, described below. All timestamps are UTC.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
> fixture data, not a secret. Hash it as normal; the exact literal must work at
> login, and it must be written into `/app/USER_README.md` alongside each account
> so a grader can sign in.

**identities** - `id`, `username` unique, `email` unique, `password_hash`,
`date_of_birth`, `state` in `active`, `restricted`, `suspended`, `terminated`,
`created_at`. The age band is derived, never stored.

**age_policy** - `band`, `min_age_years`, `version`. Rows, not constants.

**date_of_birth_changes** - `identity_id`, `old_value`, `new_value`, `actor`,
`reason`, `changed_at`. Appended only.

**credentials** - `identity_id`, `kind` in `password`, `one_time_code`, `device`,
`handoff`, `enrolled_at`, `revoked_at`. A usable identity holds at least one
credential that is not revoked.

**sessions** - `identity_id`, `token_hash`, `issued_at`, `expires_at`,
`revoked_at`, `device_binding`. A session references exactly one identity and
never outlives it.

**agreements** and **agreement_acceptances** - `agreement_key`, `version`,
`locale`, `surface`, `body`, `requires_reacceptance`; and `identity_id`,
`agreement_key`, `version`, `accepted_at`, `locale`. An acceptance is unique on
identity plus key plus version and is appended, never updated.

**accounts** - `owner_id`, `owner_type`, `kind` in `user`, `creator`,
`platform_fee`, `issuance`, `redemption`.

**ledger_transactions** - `type`, `idempotency_key`, `correlation_id`, `actor`,
`reason`, `created_at`. The idempotency key is unique across the table.

**ledger_entries** - `transaction_id`, `account_id`, `amount` as a signed
integer, `created_at`. Derived, not stored: an account balance is the sum of its
entries, computed on read. These invariants hold at every instant, and the app
must be able to demonstrate them on demand:

- For every transaction, the sum of its entry amounts is exactly `0`.
- For every account, the balance equals the sum of its entries, with no
  exception and no cached divergence.
- No `user` account has a negative balance at any committed state.
- For any idempotency key, at most one transaction exists.
- The total of all user, creator and platform balances equals the total issued
  minus the total redeemed.
- No entry is ever updated or deleted after commit.

**currency_packs** and **billing_accounts** - `code`, `name`, `kredz`,
`price_minor`, `currency`; and `identity_id`, `external_key` unique,
`created_at`. The billing platform's own generated account identifier may be
stored, but the lookup is always by `external_key`.

**items**, **item_versions** and **split_rates** - `creator_id`, `slug` unique,
`name`, `version`, `price_kredz`, `state`, `min_band`; each version carrying its
own `name`, `price_kredz`, `payload_type` and `payload`; and `version`,
`platform_numerator`, `platform_denominator`, `effective_from`. A price is within
policy bounds. Publishing a version never mutates an earlier one.

**sales** - `item_id`, `item_version`, `buyer_id`, `gross_kredz`,
`creator_kredz`, `platform_kredz`, `rate_version`, `transaction_id`. Creator
share plus platform share equals gross, exactly, on every row.

**payout_requests** and **payout_eligibility** - `creator_id`, `amount_kredz`,
`rate_version`, `state` in `requested`, `settled`, `refused`,
`refused_condition`, `requested_at`, `settled_at`; and `creator_id`,
`condition`, `met`. An amount never exceeds the creator's derived balance.

**assets** and **asset_previews** - `creator_id`, `state`, `declared_type`,
`payload`, `size_bytes`, `failure_reason`, `created_at`, `updated_at`; and
`asset_id`, `asset_version`, `size` in `small`, `medium`, `large`, `state` in
`pending`, `ready`, `unavailable`, `blocked`, `seed`, `updated_at`. A preview is
unique on asset plus version plus size, which is what makes deriving it twice do
the work once.

**moderation_decisions**, **enforcement_actions** and **appeals** -
`subject_type`, `subject_id`, `subject_version`, `decision`, `basis`, `actor`,
`decided_at`; and `identity_id`, `state`, `capabilities_removed`, `ends_at`; and
`enforcement_action_id`, `state`, with an appended child row per transition. A
`suspended` enforcement row carries an `ends_at`.

**experiences**, **instances**, **reservations** and **presences** -
`creator_id`, `slug` unique, `name`, `min_band`, `engagement_30d`,
`retention_score`, `published_at`, `creator_standing`; and `experience_id`,
`region`, `capacity`, `free_slots`, `state`; and `instance_id`, `identity_id`,
`token_hash`, `issued_at`, `expires_at`, `consumed_at`, `released_at`; and
`identity_id`, `instance_id`, `refreshed_at`, `expires_at`. Free slots never go
below `0`, and a reservation token is consumed at most once. A presence row is a
lease with an expiry, not a durable record.

**ranking_versions**, **page_views** and **telemetry_events** - `version`,
`weights`, `window_days`, `effective_from`; and `route`, `identity_id`,
`viewed_at`; and `application`, `event`, `context`, `address`, `emitted_at`. A
stored telemetry address is redacted for any route that carries a member
identifier.

**locale_bundles**, **feature_flags**, **experiment_layers** and
**experiment_exposures** - `project`, `locale`, `namespace`, `body`, `version`;
and `application`, `namespace`, `key`, `enabled`, unique on the first three; and
`layer`, `assignment_unit`, `experiments`, `version`; and `layer`, `unit`,
`variant`, `exposed_at`.

**Seed data.** The five accounts of `## User roles`, with their dates of birth and
Kredz balances. The three packs, the five items and the three experiences of
`## Core features`. `Sky Forge Arena` is seeded with capacity `8` and `7` places
already taken, leaving exactly one free. `player3@example.com` is seeded with
exactly `75` Kredz. `creator2@example.com` is seeded with `tax_documents` unmet
and the other five conditions met. Split rate version `1` is seeded at `30` of
`100`. The age policy is seeded with `child` below `13`, `teen` from `13`, and
`adult` from `18`.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- Single tenant. There are no organisations, no teams and no shared workspaces.
- No chat, no direct messages, no comments, no likes and no social feed. The
  communication capability the age band governs is the right to be contacted at
  all, not a messaging product.
- Kavora Studio, the desktop creation tool, is named and is not built. Nothing in
  this build authors an experience; the platform lists, sells and reserves.
- The creator dashboard is a route inside this application, not a separate
  application on its own origin.
- The service boundary is carried as route prefixes on one origin. Nothing here
  deploys, scales or fails independently.
- No third-party bot-defence, error-reporting or analytics vendor. The bot gate
  is first party, and there are no outbound network calls at run time.
- No real settlement rails. A payout settles to a recorded request; no money
  leaves the system.
- No native application, no desktop client and no console client.
- No refunds initiated from the interface. The `refund` transaction type exists
  and is exercised by a compensating correction, not by a member-facing button.
- The app must stay responsive with `100000` ledger entries, `5000` items and
  `200` concurrent joins.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not
  be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `date_of_birth`, `username`, `email`, `password`, optional `gender` | the created member and an `access_token` |
| `POST /api/auth/login` | `email`, `password` | an `access_token` |
| `POST /api/auth/logout` | none | the revoked session |
| `GET /api/auth/metadata` | none | the authentication routes that exist and those offered |
| `POST /api/auth/one-time-code` | `email` | acceptance that a code was sent |
| `POST /api/auth/one-time-code/verify` | `email`, `code` | an `access_token` |
| `GET /api/auth/credentials` | none | a top-level array of the member's credentials |
| `GET /api/auth/sessions` | none | a top-level array of the member's live sessions |
| `GET /api/users/authenticated` | none | the signed-in member |
| `GET /api/users/agreements` | `surface`, `locale` | a top-level array of agreements to accept |
| `GET /api/economy/balance` | none | `balance_kredz`, derived |
| `GET /api/economy/ledger` | `cursor`, `limit` | a top-level array of the member's entries |
| `GET /api/economy/packs` | none | a top-level array of packs |
| `POST /api/economy/purchases` | `pack_code`, `idempotency_key` | the purchase and its invoice reference |
| `GET /api/economy/purchases` | none | a top-level array of the member's purchases |
| `GET /api/economy/items` | `cursor`, `limit` | a top-level array of items |
| `GET /api/economy/items/{slug}` | none | one item with its price and creator |
| `POST /api/economy/items/{slug}/purchase` | `idempotency_key` | the sale, with gross and both shares |
| `GET /api/economy/sales` | `cursor` | a top-level array of the creator's own sales |
| `GET /api/economy/payouts/eligibility` | none | the six conditions, each with its own outcome |
| `POST /api/economy/payouts` | `amount_kredz`, `idempotency_key` | the payout request, or the failing condition |
| `GET /api/economy/payouts` | none | a top-level array of the creator's payout requests |
| `POST /api/creator/assets` | `name`, `declared_type`, `payload` | the asset and its state |
| `GET /api/creator/assets` | `cursor` | a top-level array of the creator's own assets |
| `PATCH /api/creator/assets/{id}` | any moderated field | the asset and its new state |
| `GET /api/thumbnails/previews` | `asset_ids`, `size` | a top-level array of preview states |
| `GET /api/games/charts` | `cursor`, `limit` | a top-level array of ranked experiences |
| `GET /api/games/search` | `q`, `scope`, `cursor`, `limit` | a top-level array of results with the ranking version |
| `POST /api/games/{slug}/join` | optional `instance_id` or `friend` | a reservation token and its expiry |
| `POST /api/games/reservations/{token}/connect` | none | the registered presence |
| `POST /api/games/presence` | `instance_id` | the refreshed lease |
| `GET /api/flags` | `application`, `namespace` | the flags for that namespace |
| `GET /api/experiments/layers` | optional `layer` | the assigned variant per layer |
| `POST /api/experiments/exposures` | `layer`, `variant` | the recorded exposure |
| `POST /api/metrics/events` | `application`, `event`, `context`, `address` | the recorded event |
| `POST /api/metrics/csp` | a violation report | acceptance |
| `GET /api/metrics/page-views` | none | a top-level array of the member's page views |
| `GET /api/locale/locales` | none | a top-level array of supported locales |
| `GET /api/locale/bundles/{namespace}` | `locale` | the strings for that namespace |
| `POST /api/users/messages` | `to`, `body` | the delivered message, or a refusal |
| `GET /api/health` | none | readiness |

Bearer auth is required on everything except login, signup, health, the
capability-discovery calls and the public catalogue reads. A successful call
returns the named resource or shape. An invalid or unauthorized call is rejected
as a client error, never a `5xx` and never a silent success.

### No mocks

The named providers are the fact. Any of the following is a contract violation,
however good the interface looks: an in-memory array standing in for the ledger;
a hardcoded billing response the app returns to itself; a Kredz purchase recorded
in the app's own tables with no invoice in `killbill`; a receipt written to a log
instead of sent over SMTP to Mailpit; a second datastore holding balances beside
PostgreSQL. The app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A visitor can sign up behind the age gate, buy a Kredz pack, and spend those
Kredz on an item somebody else published, with the creator's share landing in the
creator's balance. Buying the same pack twice with one idempotency key charges
once and sends one receipt. Two people spending the last Kredz a balance holds
produce exactly one purchase, and a creator who cannot be paid is told which
condition failed.
