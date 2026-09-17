# Checklist: Kavora

Items: 220
Unpinned values flagged: 0
Sections present: Overview, User roles, Core features, User flow, UI and UX notes, Front-end specification, Technical requirements, Data model, Constraints, Deployment contract

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves players who browse a catalogue published by other members. `src: Overview`
- [ ] `C-OV-02` `capability` The product serves creators who publish to those players. `src: Overview`
- [ ] `C-OV-03` `capability` Balances are derived from an append-only log rather than edited in place. `src: Overview`
- [ ] `C-OV-04` `constraint` The product renders no experience, runs no chat, carries no social feed. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A `player` reads only its own balance. `src: User roles`
- [ ] `C-RL-02` `role` A `player` reads only its own purchase history. `src: User roles`
- [ ] `C-RL-03` `role` A `player` calling any creator endpoint is refused by the server. `src: User roles`
- [ ] `C-RL-04` `role` A `creator` reads only its own sales. `src: User roles`
- [ ] `C-RL-05` `role` A `creator` calling another creator's payout endpoint is refused by the server. `src: User roles`
- [ ] `C-RL-06` `role` A refused authorization leaves the protected row unchanged. `src: User roles`
- [ ] `C-RL-07` `role` A role is never taken from a request body. `src: User roles`
- [ ] `C-RL-08` `role` An age band is never taken from a request body. `src: User roles`
- [ ] `C-RL-09` `literal` Signup is open to anyone. `src: User roles`
- [ ] `C-RL-10` `literal` Seeded accounts sign in with `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-11` `literal` `player@example.com` is seeded with username `Nova Pilot`. `src: User roles`
- [ ] `C-RL-12` `literal` `player2@example.com` is seeded in the `child` band. `src: User roles`
- [ ] `C-RL-13` `literal` `player3@example.com` is seeded with a balance of exactly `75` Kredz. `src: User roles`
- [ ] `C-RL-14` `literal` `creator@example.com` is seeded with username `Vale Studio`. `src: User roles`
- [ ] `C-RL-15` `literal` `creator2@example.com` is seeded with username `Hollow Forge`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` `POST /api/auth/signup` returns an `access_token` for a valid submission. `src: Core features, Auth`
- [ ] `C-CF-02` `contract` `POST /api/auth/login` takes an `email` with a `password`. `src: Core features, Auth`
- [ ] `C-CF-03` `contract` `POST /api/auth/logout` revokes exactly one session. `src: Core features, Auth`
- [ ] `C-CF-04` `capability` Date of birth is the first field the signup body carries. `src: Core features, Auth`
- [ ] `C-CF-05` `data` The stored value is the date of birth rather than a derived band. `src: Core features, Auth`
- [ ] `C-CF-06` `capability` The age band is computed at read time from policy rows. `src: Core features, Auth`
- [ ] `C-CF-07` `literal` The `child` band covers ages below `13`. `src: Core features, Auth`
- [ ] `C-CF-08` `literal` The `adult` band covers ages from `18`. `src: Core features, Auth`
- [ ] `C-CF-09` `capability` A birthday still to come in the current year makes the member a year younger. `src: Core features, Auth`
- [ ] `C-CF-10` `capability` A date of birth of `29 February` resolves a correct band in a non-leap year. `src: Core features, Auth`
- [ ] `C-CF-11` `capability` The band comparison runs against server-side UTC today. `src: Core features, Auth`
- [ ] `C-CF-12` `literal` Four credential kinds enrol: `password`, `one_time_code`, `device`, `handoff`. `src: Core features, Auth`
- [ ] `C-CF-13` `capability` Revoking one credential leaves the other three able to authenticate. `src: Core features, Auth`
- [ ] `C-CF-14` `contract` `GET /api/auth/sessions` lists only the signed-in member's live sessions. `src: Core features, Auth`
- [ ] `C-CF-15` `capability` Revoking one session leaves the member's other sessions alive. `src: Core features, Auth`
- [ ] `C-CF-16` `contract` `POST /api/auth/one-time-code` sends a code to the account's own address. `src: Core features, Auth`
- [ ] `C-CF-17` `contract` A correct one-time code is accepted exactly once at the redemption endpoint. `src: Core features, Auth`
- [ ] `C-CF-18` `capability` A reused one-time code is refused with no session issued. `src: Core features, Auth`
- [ ] `C-CF-19` `contract` `GET /api/auth/metadata` answers with no session present. `src: Core features, Auth`
- [ ] `C-CF-20` `contract` `GET /api/users/agreements` answers with no session present. `src: Core features, Auth`
- [ ] `C-CF-21` `contract` `GET /api/users/authenticated` is refused without a session. `src: Core features, Auth`
- [ ] `C-CF-22` `capability` A signup carrying a filled decoy field is refused. `src: Core features, Auth`
- [ ] `C-CF-23` `capability` The same signup form submitted repeatedly in quick succession is refused. `src: Core features, Auth`
- [ ] `C-CF-24` `capability` The bot gate fails closed when the gate's own check cannot complete. `src: Core features, Auth`
- [ ] `C-CF-25` `literal` A password is at least `8` characters. `src: Core features, Auth`
- [ ] `C-CF-26` `capability` An invalid signup names the field at fault. `src: Core features, Auth`
- [ ] `C-CF-27` `capability` An invalid signup writes no row. `src: Core features, Auth`
- [ ] `C-CF-28` `data` An agreement acceptance records the agreement's version. `src: Core features, Auth`
- [ ] `C-CF-29` `contract` `GET /api/economy/balance` returns the sum of the member's own entries. `src: Core features, The Kredz ledger`
- [ ] `C-CF-30` `data` No stored balance column is edited in place. `src: Core features, The Kredz ledger`
- [ ] `C-CF-31` `data` The entries of one transaction sum to exactly `0`. `src: Core features, The Kredz ledger`
- [ ] `C-CF-32` `capability` One `idempotency_key` submitted a hundred times produces one transaction. `src: Core features, The Kredz ledger`
- [ ] `C-CF-33` `capability` Fifty concurrent purchases against a balance covering ten leave ten succeeding. `src: Core features, The Kredz ledger`
- [ ] `C-CF-34` `data` A `user` account balance never falls below `0`. `src: Core features, The Kredz ledger`
- [ ] `C-CF-35` `literal` Four transaction types exist: `currency_purchase`, `item_purchase`, `creator_payout`, `refund`. `src: Core features, The Kredz ledger`
- [ ] `C-CF-36` `literal` Five account kinds exist: `user`, `creator`, `platform_fee`, `issuance`, `redemption`. `src: Core features, The Kredz ledger`
- [ ] `C-CF-37` `data` User plus creator plus platform balances equal issued minus redeemed. `src: Core features, The Kredz ledger`
- [ ] `C-CF-38` `capability` A failed purchase leaves no orphaned transaction behind. `src: Core features, The Kredz ledger`
- [ ] `C-CF-39` `literal` `builder-pack` sells `1000` Kredz for `1000` minor units. `src: Core features, Buying Kredz`
- [ ] `C-CF-40` `literal` `starter-pack` sells `400` Kredz for `500` minor units. `src: Core features, Buying Kredz`
- [ ] `C-CF-41` `literal` `studio-pack` sells `2400` Kredz for `2000` minor units. `src: Core features, Buying Kredz`
- [ ] `C-CF-42` `contract` `GET /api/economy/packs` lists the three packs. `src: Core features, Buying Kredz`
- [ ] `C-CF-43` `contract` `POST /api/economy/purchases` buys one pack. `src: Core features, Buying Kredz`
- [ ] `C-CF-44` `literal` A member's billing account carries the external key `kavora-nova-pilot` for `Nova Pilot`. `src: Core features, Buying Kredz`
- [ ] `C-CF-45` `capability` Exactly one billing account exists per member in the billing platform. `src: Core features, Buying Kredz`
- [ ] `C-CF-46` `capability` Exactly one invoice exists per completed pack purchase. `src: Core features, Buying Kredz`
- [ ] `C-CF-47` `data` The invoice amount equals the pack's price in the pack's currency. `src: Core features, Buying Kredz`
- [ ] `C-CF-48` `capability` A re-submitted purchase creates no second invoice. `src: Core features, Buying Kredz`
- [ ] `C-CF-49` `data` A completed pack purchase credits the member's account with the pack's Kredz. `src: Core features, Buying Kredz`
- [ ] `C-CF-50` `literal` A receipt subject begins `Kredz receipt: ` followed by the pack name. `src: Core features, Buying Kredz`
- [ ] `C-CF-51` `contract` A receipt is addressed to the buying member with no cc. `src: Core features, Buying Kredz`
- [ ] `C-CF-52` `contract` A receipt body names the pack. `src: Core features, Buying Kredz`
- [ ] `C-CF-53` `constraint` A marketplace item purchase sends no email. `src: Core features, Buying Kredz`
- [ ] `C-CF-54` `constraint` A refused pack purchase sends no email. `src: Core features, Buying Kredz`
- [ ] `C-CF-55` `literal` `aurora-visor` is priced at `75` Kredz. `src: Core features, The marketplace`
- [ ] `C-CF-56` `literal` `copper-hoverboard` is priced at `3` Kredz. `src: Core features, The marketplace`
- [ ] `C-CF-57` `literal` `vault-key` carries a minimum band of `teen`. `src: Core features, The marketplace`
- [ ] `C-CF-58` `data` An item purchase is one transaction carrying at least three entries. `src: Core features, The marketplace`
- [ ] `C-CF-59` `literal` Split rate version `1` takes `30` of every `100` Kredz. `src: Core features, The marketplace`
- [ ] `C-CF-60` `data` The rate version is written onto the sale row. `src: Core features, The marketplace`
- [ ] `C-CF-61` `capability` The platform share is truncated. `src: Core features, The marketplace`
- [ ] `C-CF-62` `capability` The remainder of a split goes to the creator. `src: Core features, The marketplace`
- [ ] `C-CF-63` `literal` A gross of `75` splits into `22` for the platform. `src: Core features, The marketplace`
- [ ] `C-CF-64` `literal` A gross of `3` splits into `0` for the platform. `src: Core features, The marketplace`
- [ ] `C-CF-65` `data` Creator share plus platform share equals the gross on every sale row. `src: Core features, The marketplace`
- [ ] `C-CF-66` `capability` Changing an item's price leaves a completed sale unchanged. `src: Core features, The marketplace`
- [ ] `C-CF-67` `data` A purchase records the item version bought. `src: Core features, The marketplace`
- [ ] `C-CF-68` `capability` A purchase by a buyer whose balance is short is refused. `src: Core features, The marketplace`
- [ ] `C-CF-69` `capability` A purchase by a buyer below the item's minimum band is refused. `src: Core features, The marketplace`
- [ ] `C-CF-70` `capability` A creator buying its own item is refused. `src: Core features, The marketplace`
- [ ] `C-CF-71` `capability` Two simultaneous purchases of the last affordable item leave one succeeding. `src: Core features, The marketplace`
- [ ] `C-CF-72` `contract` `GET /api/economy/sales` returns only the signed-in creator's sales. `src: Core features, The marketplace`
- [ ] `C-CF-73` `literal` Six payout conditions exist: `age_band`, `identity_verified`, `tax_documents`, `minimum_balance`, `good_standing`, `region_supported`. `src: Core features, Creator payouts`
- [ ] `C-CF-74` `contract` `GET /api/economy/payouts/eligibility` returns each condition separately. `src: Core features, Creator payouts`
- [ ] `C-CF-75` `capability` An ineligible payout request names the failing condition. `src: Core features, Creator payouts`
- [ ] `C-CF-76` `literal` `creator2@example.com` fails `tax_documents`. `src: Core features, Creator payouts`
- [ ] `C-CF-77` `capability` A member below the `adult` band fails `age_band`. `src: Core features, Creator payouts`
- [ ] `C-CF-78` `literal` The minimum payout balance is `100` Kredz. `src: Core features, Creator payouts`
- [ ] `C-CF-79` `capability` A payout above the creator's derived balance is refused. `src: Core features, Creator payouts`
- [ ] `C-CF-80` `data` A refused payout writes no ledger entry. `src: Core features, Creator payouts`
- [ ] `C-CF-81` `data` A settled payout debits the creator account. `src: Core features, Creator payouts`
- [ ] `C-CF-82` `data` A settled payout credits `redemption`. `src: Core features, Creator payouts`
- [ ] `C-CF-83` `literal` Ten asset states exist, from `uploading` through `deleted`. `src: Core features, The creator publishing pipeline`
- [ ] `C-CF-84` `capability` A state move outside the permitted table is refused. `src: Core features, The creator publishing pipeline`
- [ ] `C-CF-85` `capability` Validation runs before moderation. `src: Core features, The creator publishing pipeline`
- [ ] `C-CF-86` `capability` A declared type disagreeing with the payload's content is refused. `src: Core features, The creator publishing pipeline`
- [ ] `C-CF-87` `capability` A payload carrying the malware marker is refused. `src: Core features, The creator publishing pipeline`
- [ ] `C-CF-88` `capability` Renaming a `published` asset returns the asset to `pending_moderation`. `src: Core features, The creator publishing pipeline`
- [ ] `C-CF-89` `data` Publishing a new asset version leaves the earlier version resolvable. `src: Core features, The creator publishing pipeline`
- [ ] `C-CF-90` `literal` Four preview states exist: `pending`, `ready`, `unavailable`, `blocked`. `src: Core features, Derived preview imagery`
- [ ] `C-CF-91` `contract` `GET /api/thumbnails/previews` answers by asset with a state. `src: Core features, Derived preview imagery`
- [ ] `C-CF-92` `capability` A freshly published asset answers `pending`. `src: Core features, Derived preview imagery`
- [ ] `C-CF-93` `capability` An asset re-entering moderation answers `blocked`. `src: Core features, Derived preview imagery`
- [ ] `C-CF-94` `contract` `GET /api/thumbnails/previews` answers a list of asset ids in one response. `src: Core features, Derived preview imagery`
- [ ] `C-CF-95` `literal` Four search scopes exist: `games`, `marketplace`, `communities`, `creator_store`. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-96` `contract` `GET /api/games/search` takes `q`, `scope`, `cursor`, `limit`. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-97` `capability` Paging uses an opaque cursor rather than a numeric offset. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-98` `capability` Paging a list whose ranking changes shows every row exactly once. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-99` `capability` Age eligibility filters before ranking rather than weighing against popularity. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-100` `literal` `deep-vault-heist` never appears for a viewer in the `child` band. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-101` `capability` An empty result is distinguishable from a failure. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-102` `literal` The default page `limit` is `20`. `src: Core features, Discovery, charts and the scoped search`
- [ ] `C-CF-103` `literal` `sky-forge-arena` is seeded with capacity `8` at `7` occupied. `src: Core features, Joining an experience`
- [ ] `C-CF-104` `contract` `POST /api/games/{slug}/join` returns a reservation token. `src: Core features, Joining an experience`
- [ ] `C-CF-105` `capability` Free slots drop at reservation rather than at connection. `src: Core features, Joining an experience`
- [ ] `C-CF-106` `literal` A reservation lives `120` seconds. `src: Core features, Joining an experience`
- [ ] `C-CF-107` `capability` A reservation token is consumed at most once. `src: Core features, Joining an experience`
- [ ] `C-CF-108` `capability` Two simultaneous joins against one free slot leave one reservation issued. `src: Core features, Joining an experience`
- [ ] `C-CF-109` `data` Free slots never fall below `0`. `src: Core features, Joining an experience`
- [ ] `C-CF-110` `capability` An age-ineligible join is refused before any instance is contacted. `src: Core features, Joining an experience`
- [ ] `C-CF-111` `literal` A presence lease expires after `60` seconds without a refresh. `src: Core features, Joining an experience`
- [ ] `C-CF-112` `capability` A restricted communication attempted straight against the API is refused. `src: Core features, Safety, moderation and enforcement`
- [ ] `C-CF-113` `literal` Four telemetry events exist: `authPageload`, `pageHeartbeat`, `userInteractions`, `batMissing`. `src: Core features, Telemetry, localisation, flags and experiments`
- [ ] `C-CF-114` `capability` A member identifier in a route is redacted before a telemetry event leaves. `src: Core features, Telemetry, localisation, flags and experiments`
- [ ] `C-CF-115` `constraint` No user-facing string is a literal inside a component. `src: Core features, Telemetry, localisation, flags and experiments`
- [ ] `C-CF-116` `contract` `GET /api/locale/bundles/{namespace}` returns one namespace's strings. `src: Core features, Telemetry, localisation, flags and experiments`
- [ ] `C-CF-117` `contract` `GET /api/flags` answers per application plus namespace. `src: Core features, Telemetry, localisation, flags and experiments`
- [ ] `C-CF-118` `capability` Experiment assignment is a pure function of a stable identifier plus the layer. `src: Core features, Telemetry, localisation, flags and experiments`
- [ ] `C-CF-119` `capability` An anonymous caller receives a defined flag answer. `src: Core features, Telemetry, localisation, flags and experiments`
- [ ] `C-CF-120` `ui` The signup wall replaces the nav with a bare wordmark. `src: Core features, The public surfaces`
- [ ] `C-CF-121` `ui` An unknown address renders the product's own not-found surface. `src: Core features, The public surfaces`
- [ ] `C-CF-122` `contract` An unknown address answers a not-found status. `src: Core features, The public surfaces`
- [ ] `C-CF-123` `ui` Every internal link on a public route resolves. `src: Core features, The public surfaces`
- [ ] `C-CF-124` `ui` An invalid form submission names the field at fault inline. `src: Core features, The public surfaces`
- [ ] `C-CF-125` `ui` A privacy page is reachable from the footer of every page. `src: Core features, The public surfaces`
- [ ] `C-CF-126` `ui` A terms page is reachable from the footer of every page. `src: Core features, The public surfaces`
- [ ] `C-CF-127` `contract` `/sitemap.xml` lists every public route. `src: Core features, The public surfaces`
- [ ] `C-CF-128` `contract` `/robots.txt` names the sitemap. `src: Core features, The public surfaces`
- [ ] `C-CF-129` `ui` Each page leads with one primary action distinct from every secondary one. `src: Core features, The public surfaces`

## C-UF User flow

- [ ] `C-UF-01` `ui` An anonymous visitor asking for a protected route lands on `/login`. `src: User flow`
- [ ] `C-UF-02` `ui` A signed-in visitor asking for `/` lands on `/charts`. `src: User flow`
- [ ] `C-UF-03` `ui` Signing out ends the signing-out session alone. `src: User flow`
- [ ] `C-UF-04` `ui` A player asking for a creator route sees the not-found surface. `src: User flow`
- [ ] `C-UF-05` `ui` The signup card asks Birthday before the username. `src: User flow`
- [ ] `C-UF-06` `ui` Buying `Builder Pack` as `Nova Pilot` moves the displayed balance to `2000`. `src: User flow`
- [ ] `C-UF-07` `ui` Buying `Aurora Visor` raises `Vale Studio` by `53` Kredz. `src: User flow`
- [ ] `C-UF-08` `ui` Publishing from `/create/new` shows the asset at `pending_moderation`. `src: User flow`
- [ ] `C-UF-09` `ui` Requesting a payout as `Hollow Forge` shows `tax_documents` unmet. `src: User flow`
- [ ] `C-UF-10` `ui` Typing in the header search offers four scopes after typing. `src: User flow`
- [ ] `C-UF-11` `ui` Joining `Lantern Drift` drops the free count at once. `src: User flow`
- [ ] `C-UF-12` `ui` Every list carries an empty state naming what would fill the list. `src: User flow`
- [ ] `C-UF-13` `ui` A `pending` preview renders a placeholder distinct from loaded content. `src: User flow`
- [ ] `C-UF-14` `ui` A refused action leaves the visitor on the same page. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every colour resolves from a named token rather than a literal value. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Every control on the signup form takes one height from the control scale. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The primary action wears a light, vivid blue worn by nothing else. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The failure colour is a mid, vivid red appearing nowhere else. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The success colour is a mid, soft teal. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Five easing characters govern every transition. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` A reduced-motion preference holds the end state. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` The loading shimmer stays visibly distinct from loaded content when held still. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` An empty message slot sits under every signup field before any error exists. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The header holds four nav destinations plus one right-hand action. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A skip link reading `Skip to Main Content` becomes visible on focus. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The footer holds ten items ending with `Sitemap`. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Search stays reachable at every narrow viewport. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` No horizontal overflow appears at any width. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Every interactive element carries a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` The age gate is fully operable by keyboard. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Seven unknown paths resolve to one identical not-found surface. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The signup card carries the heading copy pinned in the copy deck. `src: Front-end specification`
- [ ] `C-FE-03` `literal` The username placeholder reads `Don't use your real name`. `src: Front-end specification`
- [ ] `C-FE-04` `literal` The login heading reads `Log in to Kavora`. `src: Front-end specification`
- [ ] `C-FE-05` `literal` The not-found heading reads `Something went wrong`. `src: Front-end specification`
- [ ] `C-FE-06` `literal` The not-found explanation reads `Page not found`. `src: Front-end specification`
- [ ] `C-FE-07` `literal` The locale selector shows `English (United States)`. `src: Front-end specification`
- [ ] `C-FE-08` `constraint` No third-party wordmark appears anywhere. `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The JSON API is served under `/api` on the app's own origin. `src: Technical requirements`
- [ ] `C-TR-02` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-03` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-04` `contract` Every response carries a nosniff content-type security header. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Every response carries a strict transport security header. `src: Technical requirements`
- [ ] `C-TR-06` `capability` A page of N items issues one metadata request for the page. `src: Technical requirements`
- [ ] `C-TR-07` `constraint` No second datastore holds balances beside PostgreSQL. `src: Technical requirements`
- [ ] `C-TR-08` `constraint` No mail vendor stands in for Mailpit. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` A `sessions` row references exactly one identity. `src: Data model`
- [ ] `C-DM-02` `data` A `ledger_transactions` row carries a unique `idempotency_key`. `src: Data model`
- [ ] `C-DM-03` `data` A `ledger_entries` row is never updated after commit. `src: Data model`
- [ ] `C-DM-04` `data` A `billing_accounts` row carries a unique `external_key`. `src: Data model`
- [ ] `C-DM-05` `data` A `sales` row carries `gross_kredz`, `creator_kredz`, `platform_kredz`, `rate_version`. `src: Data model`
- [ ] `C-DM-06` `data` An `asset_previews` row is unique on asset plus version plus size. `src: Data model`
- [ ] `C-DM-07` `data` A `reservations` row carries an `expires_at`. `src: Data model`
- [ ] `C-DM-08` `data` A `presences` row carries an `expires_at`. `src: Data model`
- [ ] `C-DM-09` `data` Seeding the app twice creates no duplicate row. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No organisation, team or shared workspace exists. `src: Constraints`
- [ ] `C-CN-02` `constraint` No chat, comment or social feed exists. `src: Constraints`
- [ ] `C-CN-03` `constraint` The creator dashboard is a route inside the application. `src: Constraints`
- [ ] `C-CN-04` `constraint` No refund is initiated from the interface. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping reads `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix on the same origin. `src: Deployment contract`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200`. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-06` `contract` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-07` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract`
- [ ] `C-DC-08` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-09` `contract` An unauthorized call is rejected as a client error rather than a server error. `src: Deployment contract`
- [ ] `C-DC-10` `constraint` No in-memory array stands in for the ledger. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` No hardcoded billing response stands in for an invoice. `src: Deployment contract`
- [ ] `C-DC-12` `contract` Bearer auth is required on every route outside login, signup, health, the public catalogue reads. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No receipt written to a log stands in for a message sent over SMTP. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | pinned in the brief | `C-RL-10` |
| `player@example.com` | pinned in the brief | `C-RL-11` |
| `Nova Pilot` | pinned in the brief | `C-RL-11` |
| `player2@example.com` | pinned in the brief | `C-RL-12` |
| `child` | pinned in the brief | `C-RL-12` |
| `player3@example.com` | pinned in the brief | `C-RL-13` |
| `75` | pinned in the brief | `C-RL-13` |
| `creator@example.com` | pinned in the brief | `C-RL-14` |
| `Vale Studio` | pinned in the brief | `C-RL-14` |
| `creator2@example.com` | pinned in the brief | `C-RL-15` |
| `Hollow Forge` | pinned in the brief | `C-RL-15` |
| `13` | pinned in the brief | `C-CF-07` |
| `adult` | pinned in the brief | `C-CF-08` |
| `18` | pinned in the brief | `C-CF-08` |
| `password` | pinned in the brief | `C-CF-12` |
| `one_time_code` | pinned in the brief | `C-CF-12` |
| `device` | pinned in the brief | `C-CF-12` |
| `handoff` | pinned in the brief | `C-CF-12` |
| `8` | pinned in the brief | `C-CF-25` |
| `currency_purchase` | pinned in the brief | `C-CF-35` |
| `item_purchase` | pinned in the brief | `C-CF-35` |
| `creator_payout` | pinned in the brief | `C-CF-35` |
| `refund` | pinned in the brief | `C-CF-35` |
| `user` | pinned in the brief | `C-CF-36` |
| `creator` | pinned in the brief | `C-CF-36` |
| `platform_fee` | pinned in the brief | `C-CF-36` |
| `issuance` | pinned in the brief | `C-CF-36` |
| `redemption` | pinned in the brief | `C-CF-36` |
| `builder-pack` | pinned in the brief | `C-CF-39` |
| `1000` | pinned in the brief | `C-CF-39` |
| `starter-pack` | pinned in the brief | `C-CF-40` |
| `400` | pinned in the brief | `C-CF-40` |
| `500` | pinned in the brief | `C-CF-40` |
| `studio-pack` | pinned in the brief | `C-CF-41` |
| `2400` | pinned in the brief | `C-CF-41` |
| `2000` | pinned in the brief | `C-CF-41` |
| `kavora-nova-pilot` | pinned in the brief | `C-CF-44` |
| `Kredz receipt: ` | pinned in the brief | `C-CF-50` |
| `aurora-visor` | pinned in the brief | `C-CF-55` |
| `copper-hoverboard` | pinned in the brief | `C-CF-56` |
| `3` | pinned in the brief | `C-CF-56` |
| `vault-key` | pinned in the brief | `C-CF-57` |
| `teen` | pinned in the brief | `C-CF-57` |
| `1` | pinned in the brief | `C-CF-59` |
| `30` | pinned in the brief | `C-CF-59` |
| `100` | pinned in the brief | `C-CF-59` |
| `22` | pinned in the brief | `C-CF-63` |
| `0` | pinned in the brief | `C-CF-64` |
| `age_band` | pinned in the brief | `C-CF-73` |
| `identity_verified` | pinned in the brief | `C-CF-73` |
| `tax_documents` | pinned in the brief | `C-CF-73` |
| `minimum_balance` | pinned in the brief | `C-CF-73` |
| `good_standing` | pinned in the brief | `C-CF-73` |
| `region_supported` | pinned in the brief | `C-CF-73` |
| `uploading` | pinned in the brief | `C-CF-83` |
| `deleted` | pinned in the brief | `C-CF-83` |
| `pending` | pinned in the brief | `C-CF-90` |
| `ready` | pinned in the brief | `C-CF-90` |
| `unavailable` | pinned in the brief | `C-CF-90` |
| `blocked` | pinned in the brief | `C-CF-90` |
| `games` | pinned in the brief | `C-CF-95` |
| `marketplace` | pinned in the brief | `C-CF-95` |
| `communities` | pinned in the brief | `C-CF-95` |
| `creator_store` | pinned in the brief | `C-CF-95` |
| `deep-vault-heist` | pinned in the brief | `C-CF-100` |
| `limit` | pinned in the brief | `C-CF-102` |
| `20` | pinned in the brief | `C-CF-102` |
| `sky-forge-arena` | pinned in the brief | `C-CF-103` |
| `7` | pinned in the brief | `C-CF-103` |
| `120` | pinned in the brief | `C-CF-106` |
| `60` | pinned in the brief | `C-CF-111` |
| `authPageload` | pinned in the brief | `C-CF-113` |
| `pageHeartbeat` | pinned in the brief | `C-CF-113` |
| `userInteractions` | pinned in the brief | `C-CF-113` |
| `batMissing` | pinned in the brief | `C-CF-113` |
| `Don't use your real name` | pinned in the brief | `C-FE-03` |
| `Log in to Kavora` | pinned in the brief | `C-FE-04` |
| `Something went wrong` | pinned in the brief | `C-FE-05` |
| `Page not found` | pinned in the brief | `C-FE-06` |
| `English (United States)` | pinned in the brief | `C-FE-07` |
| `Sign up and start having fun!` | the signup card heading | `C-FE-02` |
| `Log In` | the signup header action | `C-FE-02` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 4 |
| User roles | 3 | 15 |
| Core features | 40 | 129 |
| User flow | 6 | 14 |
| UI and UX notes | 11 | 16 |
| Front-end specification | 2 | 8 |
| Technical requirements | 2 | 8 |
| Data model | 6 | 9 |
| Constraints | 1 | 4 |
| Deployment contract | 13 | 13 |

