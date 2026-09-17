# Checklist: Quarro

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 424
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` Quarro serves a public site for an infinite-canvas creative workspace on one origin. `src: Overview para 1`
- [ ] `C-OV-02` `capability` One subscription reaches every image, video, audio or language model in the manifest. `src: Overview para 1`
- [ ] `C-OV-03` `capability` Work is built as a graph of nodes joined by wires on a canvas. `src: Overview para 1`
- [ ] `C-OV-04` `contract` The signed-in workspace carries studios, canvases, runs, credits, plans, teammates plus deliveries. `src: Overview para 2`
- [ ] `C-OV-05` `constraint` Every output is generated inside the app from the prompt plus the model. `src: Overview para 4`
- [ ] `C-OV-06` `constraint` No card is collected anywhere in the product. `src: Overview para 4`
- [ ] `C-OV-07` `constraint` A generated asset is readable only by the studio that made the asset or by a client holding a live delivery. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A creator signs up without an invitation. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A creator belongs to exactly one studio as owner or member. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A studio creator runs nodes spending the studio's credits. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A studio member reads every output the studio generated. `src: User roles table row 1`
- [ ] `C-RL-05` `role` Only the studio owner chooses the plan. `src: User roles table row 1`
- [ ] `C-RL-06` `role` Only the studio owner buys credit packs. `src: User roles table row 1`
- [ ] `C-RL-07` `role` Only the studio owner invites teammates. `src: User roles table row 1`
- [ ] `C-RL-08` `role` The app denies a creator any read, edit or run inside another studio. `src: User roles table row 1`
- [ ] `C-RL-09` `role` The app denies a creator another studio's output. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A client reads the deliveries addressed to the client's own email. `src: User roles table row 2`
- [ ] `C-RL-11` `role` A client streams a delivered output until the delivery is revoked. `src: User roles table row 2`
- [ ] `C-RL-12` `role` The app denies a client an output whose delivery was revoked. `src: User roles table row 2`
- [ ] `C-RL-13` `role` The app denies a client canvas creation, node runs, bench runs, subscriptions or credit purchases. `src: User roles table row 2`
- [ ] `C-RL-14` `role` A client cannot join a studio. `src: User roles table row 2`
- [ ] `C-RL-15` `role` A direct API call from a client session to a creator-only endpoint is denied with the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-16` `role` A role named in a request body grants nothing. `src: User roles, authorization paragraph`
- [ ] `C-RL-17` `role` A studio or membership named in a request body grants nothing. `src: User roles, authorization paragraph`
- [ ] `C-RL-18` `literal` Sign-up accepts an `account_type` of `creator` or `client`, defaulting to `creator`. `src: User roles, signup paragraph`
- [ ] `C-RL-19` `constraint` Any other account type is refused as invalid with no account created. `src: User roles, signup paragraph`
- [ ] `C-RL-20` `literal` The app seeds `creator@example.com`, named `Noa Lindqvist`, as owner of `Northlight Studio`. `src: User roles, seeded accounts row 1`
- [ ] `C-RL-21` `literal` The app seeds `creator2@example.com`, named `Rafael Moura`, as owner of `Saltmarsh Cut`. `src: User roles, seeded accounts row 2`
- [ ] `C-RL-22` `literal` The app seeds `creator3@example.com`, named `Aiko Tanaka`, as a member of `Northlight Studio`. `src: User roles, seeded accounts row 3`
- [ ] `C-RL-23` `literal` The app seeds `client@example.com`, named `Jonas Weber`, as a client with no studio. `src: User roles, seeded accounts row 4`

## C-CF Core features

- [ ] `C-CF-01` `literal` The password `deku-demo-pw-2026` works at login for every seeded account. `src: Core features rule 1`
- [ ] `C-CF-02` `contract` `POST /api/auth/login` returns `access_token` with a user carrying `role`. `src: Core features rule 1`
- [ ] `C-CF-03` `constraint` A wrong password gets the same refusal as an unknown address. `src: Core features rule 1`
- [ ] `C-CF-04` `constraint` Sign-up refuses a password under ten characters, naming the field. `src: Core features rule 2`
- [ ] `C-CF-05` `constraint` Sign-up refuses a malformed email with nothing stored. `src: Core features rule 2`
- [ ] `C-CF-06` `constraint` Sign-up refuses a display name that is empty or longer than sixty characters. `src: Core features rule 2`
- [ ] `C-CF-07` `constraint` A second sign-up with an address in use is refused as a conflict. `src: Core features rule 2`
- [ ] `C-CF-08` `literal` A creator sign-up opens a studio named like `Mina Park's studio` on the `free` plan. `src: Core features rule 3`
- [ ] `C-CF-09` `data` A new studio receives `500` trial credits once. `src: Core features rule 3`
- [ ] `C-CF-10` `capability` A sign-up for an invited address joins the inviting studio with no trial grant. `src: Core features rule 3`
- [ ] `C-CF-11` `contract` `GET /api/auth/me` reports the role, the studio name plus the membership. `src: Core features rule 4`
- [ ] `C-CF-12` `ui` The sign-in form carries labelled `Email` plus `Password` fields with a `Sign in` action. `src: Core features rule 5`
- [ ] `C-CF-13` `ui` The sign-up form offers `I make work` or `I receive work`. `src: Core features rule 5`
- [ ] `C-CF-14` `ui` The sign-up form submits with `Create account`. `src: Core features rule 5`
- [ ] `C-CF-15` `contract` `GET /api/v1/workspace` returns plan, balance, seat limit, members plus pending invitations. `src: Core features rule 7`
- [ ] `C-CF-16` `role` The app denies a client the studio route. `src: Core features rule 7`
- [ ] `C-CF-17` `literal` Plan codes run `free`, `creator`, `growth`, `professional`, `enterprise` in order. `src: Core features rule 8`
- [ ] `C-CF-18` `literal` An invitation from a one-seat plan is refused with `limit_reached`. `src: Core features rule 9`
- [ ] `C-CF-19` `constraint` Inviting an address that already has an account is refused as a conflict. `src: Core features rule 9`
- [ ] `C-CF-20` `constraint` Inviting one address twice is refused as a conflict. `src: Core features rule 9`
- [ ] `C-CF-21` `capability` A pending invitation is listed until the address signs up. `src: Core features rule 9`
- [ ] `C-CF-22` `contract` `GET /api/v1/credits` returns `balance` plus entries newest first. `src: Core features rule 10`
- [ ] `C-CF-23` `data` A studio balance equals the sum of the studio's credit entries. `src: Core features rule 10`
- [ ] `C-CF-24` `data` Subscribing to `creator` monthly records `2000` with a grant of 20,000 credits. `src: Core features rule 11`
- [ ] `C-CF-25` `data` Subscribing to `creator` annual records `20400`. `src: Core features rule 11`
- [ ] `C-CF-26` `data` Subscribing to `professional` `110k` annual records `111600`. `src: Core features rule 11`
- [ ] `C-CF-27` `data` Subscribing to `professional` `300k` monthly records `30000` with a grant of 300,000 credits. `src: Core features rule 11`
- [ ] `C-CF-28` `data` A repeated subscription with the same `Idempotency-Key` writes no second billing event or grant. `src: Core features rule 11`
- [ ] `C-CF-29` `constraint` Subscribing to Enterprise or Free through the subscription route is refused as invalid. `src: Core features rule 11`
- [ ] `C-CF-30` `constraint` Subscribing to Professional with no `credit_option` is refused as invalid. `src: Core features rule 11`
- [ ] `C-CF-31` `literal` Credit packs on the free plan are refused with `plan_required`. `src: Core features rule 12`
- [ ] `C-CF-32` `data` Each credit pack adds 1,000 credits for `1000` in minor units, once per key. `src: Core features rule 12`
- [ ] `C-CF-33` `literal` A plan below the studio's member count is refused with `limit_reached`. `src: Core features rule 12`
- [ ] `C-CF-34` `contract` `GET /api/v1/billing-events` lists events newest first for the owner. `src: Core features rule 13`
- [ ] `C-CF-35` `role` The app denies a member the billing events. `src: Core features rule 13`
- [ ] `C-CF-36` `ui` Subscribing ends on a full-page confirmation reading `You are on Growth.` for Growth. `src: Core features rule 14`
- [ ] `C-CF-37` `ui` The subscription confirmation names the credits added, in the form `50,000 credits were added to Northlight Studio.` `src: Core features rule 14`
- [ ] `C-CF-38` `ui` Buying packs ends on the confirmation route reading like `3 credit packs added for $30.` `src: Core features rule 14`
- [ ] `C-CF-39` `constraint` A canvas name is one to eighty characters, unique within the studio. `src: Core features rule 15`
- [ ] `C-CF-40` `contract` Each canvas row carries `last_run_at` beside the node count. `src: Core features rule 15`
- [ ] `C-CF-41` `data` A node rank is one with no inputs, otherwise one more than the highest input rank. `src: Core features rule 16`
- [ ] `C-CF-42` `literal` The `auto` model resolves to `grain-4-turbo` for images. `src: Core features rule 17`
- [ ] `C-CF-43` `literal` The `auto` model resolves to `drift-1-6` for video. `src: Core features rule 17`
- [ ] `C-CF-44` `literal` The `auto` model resolves to `quill-3-mini` for text. `src: Core features rule 17`
- [ ] `C-CF-45` `contract` A new node's `node_key` is the title in lowercase hyphenated words, made unique within the canvas by a numeric suffix. `src: Core features rule 17`
- [ ] `C-CF-46` `data` A never-run node is not stale, skipped by a rerun unless marked stale. `src: Core features rule 23`
- [ ] `C-CF-47` `capability` The `auto` model resolves to the fast audio model for audio. `src: Core features rule 17`
- [ ] `C-CF-48` `constraint` A node aspect ratio outside the model's list is refused as invalid. `src: Core features rule 17`
- [ ] `C-CF-49` `constraint` A node edit carrying an older revision is refused as a conflict. `src: Core features rule 18`
- [ ] `C-CF-50` `data` Two node edits from the same revision admit exactly one winner. `src: Core features rule 18`
- [ ] `C-CF-51` `data` A prompt edit marks the edited node plus every downstream node stale. `src: Core features rule 18`
- [ ] `C-CF-52` `data` Marking a node stale leaves the node's `revision` unchanged. `src: Core features rule 18`
- [ ] `C-CF-53` `data` A title or position edit marks nothing stale. `src: Core features rule 18`
- [ ] `C-CF-54` `constraint` A self wire is refused as invalid. `src: Core features rule 19`
- [ ] `C-CF-55` `constraint` A wire closing a loop is refused as invalid. `src: Core features rule 19`
- [ ] `C-CF-56` `constraint` A duplicate wire is refused as invalid. `src: Core features rule 19`
- [ ] `C-CF-57` `constraint` A wire between two canvases is refused as invalid. `src: Core features rule 19`
- [ ] `C-CF-58` `data` Adding or removing a wire marks the receiving node plus the nodes after the receiving node stale. `src: Core features rule 19`
- [ ] `C-CF-59` `constraint` A node whose inputs lack a current output is refused as a conflict. `src: Core features rule 20`
- [ ] `C-CF-60` `data` A run charges the current rate for the node's kind with one `run` entry. `src: Core features rule 20`
- [ ] `C-CF-61` `data` A repeated run with the same key charges once. `src: Core features rule 20`
- [ ] `C-CF-62` `data` A successful run clears the node's stale mark. `src: Core features rule 20`
- [ ] `C-CF-63` `data` Running a current node again charges again, reusing the same output key. `src: Core features rule 20`
- [ ] `C-CF-64` `contract` A run on a degraded model returns the failed run as a success response, never a refusal. `src: Core features rule 22`
- [ ] `C-CF-65` `literal` A run the balance cannot cover is refused with `insufficient_credits`. `src: Core features rule 21`
- [ ] `C-CF-66` `data` Two runs racing for credits that cover one admit exactly one success. `src: Core features rule 21`
- [ ] `C-CF-67` `data` A run on a degraded model fails with no charge. `src: Core features rule 22`
- [ ] `C-CF-68` `ui` A failed canvas node says so inside the node. `src: Core features rule 22`
- [ ] `C-CF-69` `data` A rerun regenerates only stale nodes in rank order. `src: Core features rule 23`
- [ ] `C-CF-70` `data` A rerun the balance cannot cover is refused before any node runs. `src: Core features rule 23`
- [ ] `C-CF-71` `data` Identical node inputs produce byte-identical output. `src: Core features rule 24`
- [ ] `C-CF-72` `data` A changed prompt produces different output bytes. `src: Core features rule 24`
- [ ] `C-CF-73` `contract` An image output is stored as `image/png` with a shape matching the node aspect. `src: Core features rule 24`
- [ ] `C-CF-74` `contract` A video output is stored as `image/svg+xml` with a four-second loop. `src: Core features rule 24`
- [ ] `C-CF-75` `contract` An audio output is stored as `audio/wav` lasting about two seconds. `src: Core features rule 24`
- [ ] `C-CF-76` `contract` A text output is stored as `text/plain; charset=utf-8` quoting the prompt. `src: Core features rule 24`
- [ ] `C-CF-77` `ui` A new canvas is created from an inline row at the top of the canvases table. `src: Core features rule 25`
- [ ] `C-CF-78` `literal` Output keys follow `outputs/{workspace_id}/{node_id}/{sha256_of_bytes}.{ext}` in the MinIO bucket. `src: Core features rule 26`
- [ ] `C-CF-79` `data` An output row exists once per object key. `src: Core features rule 27`
- [ ] `C-CF-80` `contract` `GET /api/v1/assets/{asset_id}/content` streams the stored bytes with the stored content type. `src: Core features rule 28`
- [ ] `C-CF-81` `constraint` No response issues a public or time-limited link into the bucket. `src: Core features rule 28`
- [ ] `C-CF-82` `role` The app denies an anonymous caller any output. `src: Core features rule 29`
- [ ] `C-CF-83` `contract` `POST /api/v1/deliveries` creates a delivery in state `delivered`. `src: Core features rule 30`
- [ ] `C-CF-84` `capability` A delivery may go to an address with no account yet. `src: Core features rule 30`
- [ ] `C-CF-85` `constraint` A malformed client address is refused as invalid. `src: Core features rule 30`
- [ ] `C-CF-86` `constraint` A delivery note longer than two hundred characters is refused. `src: Core features rule 30`
- [ ] `C-CF-87` `role` The app refuses a delivery of another studio's output as not found. `src: Core features rule 30`
- [ ] `C-CF-88` `ui` Delivering ends on a full-page confirmation reading `Delivered to client@example.com.` with the used address. `src: Core features rule 30`
- [ ] `C-CF-89` `contract` A client's delivery list carries `studio_name` for live deliveries addressed to that client. `src: Core features rule 31`
- [ ] `C-CF-90` `data` Revoking moves a delivery to `revoked`. `src: Core features rule 32`
- [ ] `C-CF-91` `data` A second revoke changes nothing. `src: Core features rule 32`
- [ ] `C-CF-92` `role` The app denies another studio a revoke on a Northlight delivery. `src: Core features rule 32`
- [ ] `C-CF-93` `contract` `GET /api/v1/models` returns manifest fields with `credit_cost` from the current rates. `src: Core features rule 33`
- [ ] `C-CF-94` `literal` The manifest lists twenty-two models in pinned order, from `halcyon-2-1` to `parley-2`. `src: Core features rule 34`
- [ ] `C-CF-95` `literal` `lumen-preview` is a degraded model. `src: Core features rule 34`
- [ ] `C-CF-96` `literal` `driftwood-beta` is a degraded model. `src: Core features rule 34`
- [ ] `C-CF-97` `literal` Image models cap at `2048 x 2048`. `src: Core features rule 34`
- [ ] `C-CF-98` `literal` Image models list `4:5`, `16:9`, `1:1`; video models list `16:9`, `9:16`; audio models cap at `30` seconds. `src: Core features rule 34`
- [ ] `C-CF-99` `literal` Video models cap at `1920 x 1080` for ten seconds. `src: Core features rule 34`
- [ ] `C-CF-100` `ui` The roster groups every model under `Image`, `Video`, `Audio` or `Text` headings with name plus vendor. `src: Core features rule 35`
- [ ] `C-CF-101` `ui` The roster offers a `Let Ivo choose` action beside the routing lead. `src: Core features rule 35`
- [ ] `C-CF-102` `ui` The roster's `Let Ivo choose` action opens a new canvas node set to `auto`. `src: Core features rule 35`
- [ ] `C-CF-103` `capability` Every manifest model has a page one segment deep at the model slug. `src: Core features rule 36`
- [ ] `C-CF-104` `literal` The Halcyon 2.1 page reads `Creator buys 277 standard runs a month`. `src: Core features rule 36`
- [ ] `C-CF-105` `literal` Video, audio plus text model pages read `20`, `500` plus `5000` standard runs. `src: Core features rule 36`
- [ ] `C-CF-106` `ui` A model page links at least three models of the same output kind. `src: Core features rule 36`
- [ ] `C-CF-107` `literal` A model page gallery shows at least four items marked `data-sample`. `src: Core features rule 36`
- [ ] `C-CF-108` `ui` A model page offers `Try on the canvas` beside `Compare on the bench`. `src: Core features rule 36`
- [ ] `C-CF-109` `ui` A timed sample on a model page stays still until the visitor asks for playback. `src: Core features rule 36`
- [ ] `C-CF-110` `literal` A model page root carries `data-output-kind` for the model's kind. `src: Core features rule 36`
- [ ] `C-CF-111` `contract` `GET /api/v1/plans` returns prices, credits, seats plus computed yields in plan order. `src: Core features rule 37`
- [ ] `C-CF-112` `data` Enterprise prices, credits plus yields are null. `src: Core features rule 37`
- [ ] `C-CF-113` `literal` The Free plan descriptor reads `Try every model on the canvas`. `src: Core features rule 37`
- [ ] `C-CF-114` `literal` The Creator plan descriptor reads `Deliver client work every week`. `src: Core features rule 37`
- [ ] `C-CF-115` `literal` The Growth plan descriptor reads `Scale a busy solo practice fast`. `src: Core features rule 37`
- [ ] `C-CF-116` `literal` The Professional plan descriptor reads `Run a studio on one shared canvas`. `src: Core features rule 37`
- [ ] `C-CF-117` `capability` The Enterprise plan carries the fifth pinned descriptor. `src: Core features rule 37`
- [ ] `C-CF-118` `data` Yields divide credits by the current standard image or video cost, rounded down. `src: Core features rule 38`
- [ ] `C-CF-119` `literal` The pricing route is headed `One plan, every model.` over `Credits that follow the work.` `src: Front-end specification, route: pricing`
- [ ] `C-CF-120` `literal` The forecaster is headed `How many credits does your work need?` `src: Front-end specification, route: pricing`
- [ ] `C-CF-121` `literal` The pricing page shows `277 images or 20 videos` for Creator. `src: Core features rule 38`
- [ ] `C-CF-122` `literal` The pricing page shows `694 images or 50 videos` for Growth. `src: Core features rule 38`
- [ ] `C-CF-123` `literal` The pricing page shows `1,527 images or 110 videos` for Professional at 110K. `src: Core features rule 38`
- [ ] `C-CF-124` `literal` The Free card shows `Limited trial`; the Enterprise card shows `Custom`. `src: Core features rule 38`
- [ ] `C-CF-125` `literal` The billing toggle reads `Monthly` or `Annual` beside the chip `Save up to 15%`. `src: Core features rule 39`
- [ ] `C-CF-126` `ui` Annual mode shows the annual price beside the struck monthly price on each paid card. `src: Core features rule 39`
- [ ] `C-CF-127` `literal` The pricing root carries `data-billing-period` of `monthly` or `annual`. `src: Core features rule 39`
- [ ] `C-CF-128` `ui` The Professional stepper between `110K` or `300K` updates price, credits plus both yields together. `src: Core features rule 40`
- [ ] `C-CF-129` `literal` The Professional card carries `data-credit-option` of `110k` or `300k`. `src: Core features rule 40`
- [ ] `C-CF-130` `contract` `GET /api/v1/rates` returns the current version `2026-09`. `src: Core features rule 41`
- [ ] `C-CF-131` `contract` Version `2026-06` reads as retired. `src: Core features rule 41`
- [ ] `C-CF-132` `ui` The forecaster with no rows shows an empty track with no total. `src: Core features rule 42`
- [ ] `C-CF-133` `data` Forecast quantities round to two significant figures, half up, so `437` becomes `440`. `src: Core features rule 42`
- [ ] `C-CF-134` `constraint` A forecast with seven rows is refused. `src: Core features rule 43`
- [ ] `C-CF-135` `constraint` A forecast quantity outside ten to five thousand is refused. `src: Core features rule 43`
- [ ] `C-CF-136` `constraint` A forecast naming an unknown kind, tier or version is refused. `src: Core features rule 43`
- [ ] `C-CF-137` `data` 400 standard images with 30 standard videos total `58,800`, recommend `professional` at `110k`, overflow `9000` over `growth`. `src: Core features rule 44`
- [ ] `C-CF-138` `data` 100 standard images total `7,200`, recommending `creator` with overflow `7000` over `free`. `src: Core features rule 44`
- [ ] `C-CF-139` `data` 3000 high images total `432,000`, recommend `enterprise`, name `professional` at `300k` below, overflow `132000`. `src: Core features rule 44`
- [ ] `C-CF-140` `data` A forecast under a retired version stays stale until recomputed. `src: Core features rule 45`
- [ ] `C-CF-141` `literal` A stale forecast keeps the recommended card, offering `Recompute`. `src: Core features rule 45`
- [ ] `C-CF-142` `capability` The address `/pricing?forecast={id}` opens a saved forecast in the forecaster. `src: Core features rule 45`
- [ ] `C-CF-143` `literal` Exactly one plan card carries `data-glow` of `on`, the Professional card with no forecast. `src: Core features rule 46`
- [ ] `C-CF-144` `ui` The glow moves from one plan card to the next instead of jumping. `src: Core features rule 46`
- [ ] `C-CF-145` `literal` Each plan card carries `data-plan` with the plan code. `src: Core features rule 46`
- [ ] `C-CF-146` `literal` The comparison table groups rows under `Creative tools`, `Support` or the usage-limits heading. `src: Core features rule 47`
- [ ] `C-CF-147` `literal` The comparison table carries the rows `Monthly credits`, `Additional credit packs`, `All models`, `Unlimited seats`. `src: Core features rule 47`
- [ ] `C-CF-148` `literal` The comparison table carries `Custom agent skills`, `Multiplayer canvas`, `Community support`, `Dedicated success manager`. `src: Core features rule 47`
- [ ] `C-CF-149` `capability` The comparison table carries the queue ordering row plus the email support row. `src: Core features rule 47`
- [ ] `C-CF-150` `literal` Comparison cells read `500 once`, `$10 per 1,000 credits` or `110,000 to 300,000` where pinned. `src: Core features rule 47`
- [ ] `C-CF-151` `contract` `GET /api/v1/replay/graphs` lists five graphs from `advertising` to `branding`. `src: Core features rule 48`
- [ ] `C-CF-152` `constraint` Every replay graph is acyclic, at most twelve nodes, one model per node. `src: Core features rule 48`
- [ ] `C-CF-153` `constraint` Replay image or video nodes are framed at `4:5` or `16:9` alone. `src: Core features rule 48`
- [ ] `C-CF-154` `literal` The advertising graph carries eight nodes over five ranks from `product-mockup` to `movie-cut-1`. `src: Core features rule 49`
- [ ] `C-CF-155` `literal` The replay graph carries `data-graph-key`; each node carries `data-node-key` with a `data-node-state`. `src: Core features rule 49`
- [ ] `C-CF-156` `ui` Stepping advances one rank at a time with a readout like `Rank 2 of 5`. `src: Core features rule 50`
- [ ] `C-CF-157` `ui` The replay transport offers `Play`, `Pause`, `Step forward`, `Step back` plus a scrub track. `src: Core features rule 50`
- [ ] `C-CF-158` `ui` An opened node shows prompt, model, credit cost plus generation time. `src: Core features rule 50`
- [ ] `C-CF-159` `ui` An opened node offers `Apply prompt` beside `Rerun graph`. `src: Core features rule 50`
- [ ] `C-CF-160` `ui` Applying a prompt marks the node plus downstream nodes stale before any rerun. `src: Core features rule 51`
- [ ] `C-CF-161` `ui` The replay's `Rerun graph` regenerates only the stale nodes, in rank order. `src: Core features rule 51`
- [ ] `C-CF-162` `data` A default prompt regeneration is a `cache` hit with `nearby` false. `src: Core features rule 52`
- [ ] `C-CF-163` `data` An edited prompt falls back to a deterministic `curated` variant. `src: Core features rule 52`
- [ ] `C-CF-164` `ui` A curated node shows `Showing a nearby result`. `src: Core features rule 52`
- [ ] `C-CF-165` `constraint` A regeneration naming a model of another kind is refused as invalid. `src: Core features rule 52`
- [ ] `C-CF-166` `literal` A lower generation token is refused with `stale_generation`. `src: Core features rule 53`
- [ ] `C-CF-167` `data` Repeating the accepted generation token returns the same result. `src: Core features rule 53`
- [ ] `C-CF-168` `data` Past `30` reruns per session per hour, a regeneration degrades to curated with `rate_limited` true. `src: Core features rule 54`
- [ ] `C-CF-169` `ui` A reloaded replay keeps the edited prompts plus stale marks. `src: Core features rule 55`
- [ ] `C-CF-170` `data` A session claim creates `My first canvas` once, carrying overrides plus stale marks. `src: Core features rule 55`
- [ ] `C-CF-171` `data` Claimed nodes carry tier `standard` at revision one. `src: Core features rule 55`
- [ ] `C-CF-172` `literal` A second claimed session is named `My first canvas 2`. `src: Core features rule 55`
- [ ] `C-CF-173` `ui` Signing up after playing lands on the canvas the visitor was playing with. `src: Core features rule 55`
- [ ] `C-CF-174` `ui` Submitting the hero capsule scrolls to the graph showing the typed brief. `src: Core features rule 56`
- [ ] `C-CF-175` `role` The app refuses a bench run without a creator session. `src: Core features rule 57`
- [ ] `C-CF-176` `ui` Selecting a fifth bench model flashes the earliest chip instead of adding the fifth. `src: Core features rule 57`
- [ ] `C-CF-177` `literal` Each bench chip carries `data-chip-state` of `rest`, `active` or `rejected`. `src: Core features rule 57`
- [ ] `C-CF-178` `constraint` A bench run needs two to four distinct known models. `src: Core features rule 58`
- [ ] `C-CF-179` `constraint` A bench brief is one to four hundred characters. `src: Core features rule 58`
- [ ] `C-CF-180` `data` A replayed bench key returns the same run. `src: Core features rule 58`
- [ ] `C-CF-181` `literal` A bench run costing more than the balance is refused with `insufficient_credits`. `src: Core features rule 58`
- [ ] `C-CF-182` `data` Bench frames land on independent schedules by latency band. `src: Core features rule 59`
- [ ] `C-CF-183` `literal` `lumen-preview` fails at once with `Engine unavailable`. `src: Core features rule 59`
- [ ] `C-CF-184` `literal` `driftwood-beta` becomes `timed_out` once the thirty-second deadline passes. `src: Core features rule 59`
- [ ] `C-CF-185` `data` A completed run charges each succeeded frame the model's standard rate. `src: Core features rule 60`
- [ ] `C-CF-186` `data` A failed frame costs nothing. `src: Core features rule 60`
- [ ] `C-CF-187` `data` Two failed frames void the run with nothing charged. `src: Core features rule 60`
- [ ] `C-CF-188` `role` The app denies a creator of another studio any read, retry or pick on a bench run. `src: Core features rule 60`
- [ ] `C-CF-189` `data` A retried failed frame is charged only when the retry succeeds. `src: Core features rule 61`
- [ ] `C-CF-190` `literal` A voided bench run shows the two-failure cancellation line. `src: Core features rule 60`
- [ ] `C-CF-191` `literal` A failed frame holds its place with a retry action for the model. `src: Core features rule 60`
- [ ] `C-CF-192` `constraint` Retrying a succeeded frame is refused as a conflict. `src: Core features rule 61`
- [ ] `C-CF-193` `constraint` Retrying a frame on a voided run is refused as a conflict. `src: Core features rule 61`
- [ ] `C-CF-194` `constraint` A pick needs two succeeded frames on the run. `src: Core features rule 62`
- [ ] `C-CF-195` `constraint` Picking a model that did not succeed is refused as invalid. `src: Core features rule 62`
- [ ] `C-CF-196` `constraint` A second pick on one run is refused as a conflict. `src: Core features rule 62`
- [ ] `C-CF-197` `data` A bench run writes nothing to the object store. `src: Core features rule 63`
- [ ] `C-CF-198` `data` Win rates list only model pairs with at least `200` runs. `src: Core features rule 63`
- [ ] `C-CF-199` `literal` The hero headline stacks two pinned lines above the prompt capsule. `src: Core features rule 64`
- [ ] `C-CF-200` `literal` The hero capsule reads `Describe what you want to make` with a round `Start the replay` control. `src: Core features rule 64`
- [ ] `C-CF-201` `literal` The hero lead names one canvas, one subscription plus every model, ending on Ivo choosing. `src: Core features rule 64`
- [ ] `C-CF-202` `literal` The audience grid shows five panels from `Agencies` to `Go-to-market`. `src: Core features rule 65`
- [ ] `C-CF-203` `literal` The Agencies panel carries the chip `Campaign variants`; Go-to-market carries `Launch films`. `src: Core features rule 65`
- [ ] `C-CF-204` `literal` The announcement `Vesper 3 is now on Quarro.` carries a canvas action. `src: Core features rule 66`
- [ ] `C-CF-205` `ui` Pressing `Dismiss announcement` keeps the bar dismissed across reloads. `src: Core features rule 66`
- [ ] `C-CF-206` `literal` The enterprise route opens with `Your studio, one canvas.` `src: Core features rule 67`
- [ ] `C-CF-207` `ui` The enterprise route carries `Platform`, `Controls` plus `Support` tabs. `src: Core features rule 67`
- [ ] `C-CF-208` `ui` Five enterprise capability cards each end in `Book a call`. `src: Core features rule 67`
- [ ] `C-CF-209` `literal` The enterprise capability cards read `Collaborative canvas`, `Agent connector`, `Brand kits`, `Chat-tool creation`, `Shared asset library`. `src: Core features rule 67`
- [ ] `C-CF-210` `data` A valid enterprise lead is stored once. `src: Core features rule 68`
- [ ] `C-CF-211` `data` A newsletter lead with only an email is stored once. `src: Core features rule 68`
- [ ] `C-CF-212` `constraint` An invalid lead is refused, storing nothing. `src: Core features rule 68`
- [ ] `C-CF-213` `ui` A malformed work email in the booking form shows an inline error beside the field. `src: Core features rule 68`
- [ ] `C-CF-214` `ui` The footer capture `Get model launches in your inbox` accepts a valid address. `src: Core features rule 68`
- [ ] `C-CF-215` `literal` Four desktop releases are listed at version `2.4.0`. `src: Core features rule 69`
- [ ] `C-CF-216` `literal` The releases carry `Download for macOS (Apple silicon)`, `Download for macOS (Intel)`, `Download for Windows`, `Download for Linux`. `src: Core features rule 69`
- [ ] `C-CF-217` `literal` The desktop route is headed `Quarro for your desktop.` `src: Core features rule 69`
- [ ] `C-CF-218` `literal` The desktop route root carries `data-primary-platform` for the detected system. `src: Core features rule 69`
- [ ] `C-CF-219` `ui` The desktop route offers the detected platform's download first with the rest quieter. `src: Core features rule 69`
- [ ] `C-CF-220` `ui` The desktop route names `Watch a folder`, `Capture anything on screen`, `Queue runs offline`. `src: Core features rule 69`
- [ ] `C-CF-221` `literal` The manifesto route is headed `Made by hand, at the speed of thought.` `src: Core features rule 70`
- [ ] `C-CF-222` `ui` The manifesto essay closes on the hand-drawn signature. `src: Core features rule 70`
- [ ] `C-CF-223` `literal` The blog headline stacks `Field notes, guides` over `and model comparisons.` `src: Core features rule 71`
- [ ] `C-CF-224` `contract` `GET /api/v1/posts` filters by `category` with a `sort` order. `src: Core features rule 71`
- [ ] `C-CF-225` `contract` `GET /api/v1/posts` returns twelve posts per page with `X-Next-Cursor` when more remain. `src: Core features rule 71`
- [ ] `C-CF-226` `contract` `GET /api/v1/posts/{slug}` returns one post with the `body`. `src: Core features rule 71`
- [ ] `C-CF-227` `capability` Each blog post has a page at `/blog/{slug}`. `src: Core features rule 71`
- [ ] `C-CF-228` `ui` Each blog card shows the date, then the reading time, then the title, twelve cards per page. `src: Core features rule 71`
- [ ] `C-CF-229` `ui` A cold load of a filtered blog address restores the filtered view. `src: Core features rule 71`
- [ ] `C-CF-230` `ui` The about route carries the four vignettes, eight people, five roles plus eight investors. `src: Core features rule 72`
- [ ] `C-CF-231` `literal` The people grid names `Ines Carvalho`, `Tomas Reyes`, `Hana Okafor`, `Luca Brandt`, `Mira Solberg`, `Dev Anand`, `Clara Voss`, `Sami Haddad`. `src: Core features rule 72`
- [ ] `C-CF-232` `literal` The open roles read `Senior Graphics Engineer`, `Product Designer, Canvas`, `Model Partnerships Lead`, `Staff Backend Engineer, Billing`, `Community Producer`. `src: Core features rule 72`
- [ ] `C-CF-233` `literal` The investors are `Amara Whitfield`, `Kenji Morrow`, `Sofia Brennan`, `Owen Castell`, `Lena Hartmann`, `Marcus Obi`, `Yara Lindgren`, `Theo Marchetti`. `src: Core features rule 72`
- [ ] `C-CF-234` `literal` The office sits in `Porto`, in the `Bonfim` district. `src: Core features rule 72`
- [ ] `C-CF-235` `capability` A privacy page at `/privacy` is linked from the footer of every page. `src: Core features rule 73`
- [ ] `C-CF-236` `literal` The privacy page names `privacy@quarro.dev` for removal requests. `src: Core features rule 73`
- [ ] `C-CF-237` `capability` The footer links `/terms` beside `/acceptable-use`. `src: Core features rule 73`
- [ ] `C-CF-238` `capability` The site serves a favicon declared in every page head. `src: Core features rule 74`
- [ ] `C-CF-239` `literal` Every public route declares `og:title` plus an `og:image` that resolves. `src: Core features rule 75`
- [ ] `C-CF-240` `capability` No two public routes share a title or a description. `src: Core features rule 75`
- [ ] `C-CF-241` `capability` Every internal link on every public route resolves. `src: Core features rule 76`
- [ ] `C-CF-242` `capability` External footer links open in a new tab. `src: Core features rule 76`
- [ ] `C-CF-243` `capability` An unknown address answers not-found with the product's own page, keeping the header plus footer. `src: Core features rule 77`
- [ ] `C-CF-244` `literal` The not-found page shows a single not-on-the-canvas line with a `Back to home` action. `src: Core features rule 77`

## C-UF User flow

- [ ] `C-UF-01` `capability` Every listed public route answers. `src: User flow, routes table`
- [ ] `C-UF-02` `capability` An anonymous visitor to a signed-in route lands on `/sign-in`. `src: User flow, entry and redirects`
- [ ] `C-UF-03` `ui` Signing in returns a visitor to the remembered address. `src: User flow, entry and redirects`
- [ ] `C-UF-04` `ui` Signing in lands a client on `/deliveries`. `src: User flow, entry and redirects`
- [ ] `C-UF-05` `ui` A client reaching `/canvases`, `/account/billing` or `/account/team` is sent to `/deliveries`. `src: User flow, entry and redirects`
- [ ] `C-UF-06` `ui` A member opening the billing route sees a read-only view naming the owner. `src: User flow, entry and redirects`
- [ ] `C-UF-07` `ui` Signing in lands a creator on `/canvases`. `src: User flow, entry and redirects`
- [ ] `C-UF-08` `ui` The header's `Sign out` action returns a signed-in visitor to the home page. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `ui` Running Product Mockup settles the output into the node with the header balance dropping from `500`. `src: User flow, journeys`
- [ ] `C-UF-10` `ui` The first successful bench frame to land is `Grain 4 Turbo`. `src: User flow, journeys`
- [ ] `C-UF-11` `ui` The bench journey records a pick of `Vesper 3` on the row. `src: User flow, journeys`
- [ ] `C-UF-12` `ui` Signed in as `creator2@example.com`, the canvases table lists `Trailer Cut` without `Citrus Launch`. `src: User flow, journeys`
- [ ] `C-UF-13` `ui` The forecast journey reaches `58,800` with the overflow over Growth stated as `$90`. `src: User flow, journeys`
- [ ] `C-UF-14` `ui` An invited address signs up into `Northlight Studio` seeing `Citrus Launch` in the table. `src: User flow, journeys`
- [ ] `C-UF-15` `ui` The client journey lists deliveries under `Work delivered to you` then opens each output. `src: User flow, journeys`
- [ ] `C-UF-16` `ui` A contended save names the changed node inline with a `Reload node` action. `src: User flow, journeys`
- [ ] `C-UF-17` `ui` The blog address `/blog?category=comparisons&sort=oldest` shows four cards oldest first. `src: User flow, journeys`
- [ ] `C-UF-18` `literal` An empty canvases table reads `No canvases yet. Name one above to start.` `src: User flow, states`
- [ ] `C-UF-19` `literal` A client with nothing delivered reads `Nothing has been delivered to you yet.` `src: User flow, states`
- [ ] `C-UF-20` `ui` A bench frame awaiting a result holds a skeleton at the model's aspect. `src: User flow, states`
- [ ] `C-UF-21` `ui` A regenerating replay node shows the node's elapsed time. `src: User flow, states`
- [ ] `C-UF-22` `ui` A refused action names the reason inline beside the control. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The home page shows finished work within the first screen, public routes reading as creative marketing. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The signed-in routes read as a quiet dense tool with no editorial composition. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` Every public page leads with one primary action, everything else visibly quieter. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` The billing route stays still during a price decision. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `capability` Body text meets a contrast of at least 4.5 to 1. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-06` `capability` Header touch targets measure at least 44 by 44 CSS pixels. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-07` `capability` Every icon-only control carries an accessible label. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-08` `capability` Every content image carries alternative text. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-09` `ui` The focus ring stays visible over live three-dimensional content on both grounds. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-10` `ui` Arrow keys move the replay scrub by one rank; Enter expands a node. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-11` `ui` The node graph exposes an ordered list of ranks naming title, model plus kind. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-12` `ui` Most sections sit on the near-black ground with near-white type. `src: UI/UX notes, grounds`
- [ ] `C-UX-13` `ui` Card faces float on the dark ground as the brightest near-white. `src: UI/UX notes, palette by role`
- [ ] `C-UX-14` `ui` The vermilion accent covers under eight percent of any frame, never a section ground. `src: UI/UX notes, the accent`
- [ ] `C-UX-15` `ui` The pale amber appears only on the sign-in control with one enterprise chip. `src: UI/UX notes, the accent`
- [ ] `C-UX-16` `ui` The indigo-to-blue gradient appears on exactly one action. `src: UI/UX notes, the accent`
- [ ] `C-UX-17` `ui` Failure, success or in-progress each carry one exclusive colour in the signed-in tool. `src: UI/UX notes, meaning colours`
- [ ] `C-UX-18` `ui` A stale node shows by desaturation. `src: UI/UX notes, meaning colours`
- [ ] `C-UX-19` `ui` Headlines use a display serif with a true italic. `src: UI/UX notes, type`
- [ ] `C-UX-20` `ui` Model names, vendor names plus credit figures use a monospace face. `src: UI/UX notes, type`
- [ ] `C-UX-21` `ui` Section tags use a geometric sans as small-caps labels. `src: UI/UX notes, type`
- [ ] `C-UX-22` `ui` Nested corners stay concentric, the inner corner derived from the outer. `src: UI/UX notes, shape`
- [ ] `C-UX-23` `ui` Pills stay pills on non-square elements, never ellipses. `src: UI/UX notes, shape`
- [ ] `C-UX-24` `ui` Signed-in tables are compact so a studio's canvas list fits one screen. `src: UI/UX notes, density and spacing`
- [ ] `C-UX-25` `ui` Every panel closes on Escape. `src: UI/UX notes, components behave`
- [ ] `C-UX-26` `ui` Every destructive action asks once, naming the target. `src: UI/UX notes, components behave`
- [ ] `C-UX-27` `ui` Blocks fade into place with a hard decelerate over about half a second. `src: UI/UX notes, motion is eased`
- [ ] `C-UX-28` `ui` Only node cards entering on the canvas overshoot then settle. `src: UI/UX notes, motion is eased`
- [ ] `C-UX-29` `ui` A film grain drifts over the dark grounds as two layers at different speeds. `src: UI/UX notes, motion is eased`
- [ ] `C-UX-30` `ui` A pulse crosses each accent wire then rests for half the cycle. `src: UI/UX notes, motion is eased`
- [ ] `C-UX-31` `ui` Forward arrows shrink away then redraw in place, never sliding. `src: UI/UX notes, motion is eased`
- [ ] `C-UX-32` `ui` Under reduced motion the replay scrub moves in whole ranks with a readout. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-33` `capability` At a narrow viewport no public page overflows sideways. `src: UI/UX notes, responsive`
- [ ] `C-UX-34` `ui` A tap on a touch screen leaves no control stuck in the pointed-at state. `src: UI/UX notes, responsive`
- [ ] `C-UX-35` `ui` On a narrow screen the comparison table scrolls sideways with a pinned first column. `src: UI/UX notes, responsive`
- [ ] `C-UX-36` `ui` On a narrow screen the replay graph becomes a vertical list, one rank per screen. `src: UI/UX notes, responsive`
- [ ] `C-UX-37` `constraint` The word `seamless` appears nowhere in the product copy. `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-38` `ui` Generated work fills the corridor, the showcase plus the galleries instead of abstract shapes. `src: UI/UX notes, what it must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements para 1`
- [ ] `C-TR-02` `capability` The server returns each public route's title, description, preview tags plus favicon in the HTML. `src: Technical requirements, what the browser receives`
- [ ] `C-TR-03` `contract` Errors use one envelope with `code`, `message` plus `correlation_id` matching `X-Correlation-Id`. `src: Technical requirements, API conventions`
- [ ] `C-TR-04` `contract` Product endpoints carry the version in the path under `/api/v1/`. `src: Technical requirements, API conventions`
- [ ] `C-TR-05` `constraint` Every refusal is a client error, never a server error. `src: Technical requirements, API conventions`
- [ ] `C-TR-06` `constraint` A run without an `Idempotency-Key` header is refused as invalid. `src: Technical requirements, retries and races`
- [ ] `C-TR-07` `constraint` Reusing an `Idempotency-Key` with a different body is refused as a conflict, writing nothing. `src: Technical requirements, retries and races`
- [ ] `C-TR-08` `data` Racing runs resolve to exactly one success. `src: Technical requirements, retries and races`
- [ ] `C-TR-09` `data` Racing edits resolve to exactly one accepted edit. `src: Technical requirements, retries and races`
- [ ] `C-TR-10` `ui` One persistent three-dimensional canvas sits behind every public route, fading in after the first frame. `src: Technical requirements, the three render systems`
- [ ] `C-TR-11` `capability` A reduced-motion visitor gets the static tier with the reduced track. `src: Technical requirements, the degradation ladder`
- [ ] `C-TR-12` `capability` The document element carries `data-gl-tier` plus `data-motion` values. `src: Technical requirements, the degradation ladder`
- [ ] `C-TR-13` `capability` Sound starts `off` on a first visit, shown by `data-sound`. `src: Technical requirements, sound`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026`, hashed. `src: Data model, password paragraph`
- [ ] `C-DM-02` `data` `app_user` holds `email` unique across the product. `src: Data model, app_user`
- [ ] `C-DM-03` `data` `generation_run` holds at most one run per studio plus idempotency key. `src: Data model, generation_run`
- [ ] `C-DM-04` `data` `asset` holds `object_key` unique across the product. `src: Data model, generation_run`
- [ ] `C-DM-05` `data` `billing_event` holds at most one event per studio plus idempotency key. `src: Data model, credit_entry`
- [ ] `C-DM-06` `data` `delivery` records `revoked_at` on revocation. `src: Data model, delivery`
- [ ] `C-DM-07` `data` `bench_run` keeps the idempotency key with no reference to the person who ran the bench. `src: Data model, bench_run`
- [ ] `C-DM-08` `data` `lead` stores `source` with the lead `email`. `src: Data model, blog_post`
- [ ] `C-DM-09` `literal` `Northlight Studio` opens on `professional` with a ledger balance of `108,596`. `src: Data model, seed data`
- [ ] `C-DM-10` `literal` `Saltmarsh Cut` opens on `creator` with `20,000` credits. `src: Data model, seed data`
- [ ] `C-DM-11` `literal` `Citrus Launch` carries the eight advertising nodes, each run once with an output in the bucket. `src: Data model, seed data`
- [ ] `C-DM-12` `literal` `Autumn Lookbook` carries five never-run nodes. `src: Data model, seed data`
- [ ] `C-DM-13` `literal` `Trailer Cut` carries five never-run nodes. `src: Data model, seed data`
- [ ] `C-DM-14` `literal` The seeded delivery of `OOH Billboard` to `client@example.com` carries `Billboard for sign-off`. `src: Data model, seed data`
- [ ] `C-DM-15` `literal` Fourteen blog posts are seeded, newest `Quarro raises its Series A to build the one canvas`. `src: Data model, seed data`
- [ ] `C-DM-16` `data` Seeding is idempotent with every seeded row present once. `src: Data model, seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every mark is drawn inline, taking colour from the surrounding text. `src: Front-end specification, iconography`
- [ ] `C-FE-02` `ui` The wordmark is a symmetric ribbon pinched at a waist. `src: Front-end specification, iconography`
- [ ] `C-FE-03` `ui` A credit medallion coin sits beside every credit figure. `src: Front-end specification, iconography`
- [ ] `C-FE-04` `ui` The header floats as a capsule inset from the top-left with the wordmark plus the menu control. `src: Front-end specification, the chrome`
- [ ] `C-FE-05` `ui` A sound toggle with a small waveform sits beside the menu control. `src: Front-end specification, the chrome`
- [ ] `C-FE-06` `ui` The header shows a pale-yellow `Sign in` beside an accent `Start creating`. `src: Front-end specification, the chrome`
- [ ] `C-FE-07` `ui` `Sign in` drops from the header on a narrow screen. `src: Front-end specification, the chrome`
- [ ] `C-FE-08` `ui` Every control has stepped pixel corners that recolour with the control on hover. `src: Front-end specification, the chrome`
- [ ] `C-FE-09` `ui` The footer `Product` group lists `Web app` through `Agent connector` in order. `src: Front-end specification, the chrome`
- [ ] `C-FE-10` `literal` The footer carries the groups `Company`, `Resources` plus `Legal` with the line `Quarro, Porto`. `src: Front-end specification, the chrome`
- [ ] `C-FE-11` `ui` The plan glow breathes around one plan card without dimming at the middle of the breath. `src: Front-end specification, motion, in detail`
- [ ] `C-FE-12` `ui` The hero arrives once on load, fading in, settling from slightly larger. `src: Front-end specification, motion, in detail`
- [ ] `C-FE-13` `ui` Headings rise word by word from a clipped baseline with a capped stagger. `src: Front-end specification, the reveal and scroll system`
- [ ] `C-FE-14` `ui` Stills develop from soft grey into colour with focus on separate schedules. `src: Front-end specification, the reveal and scroll system`
- [ ] `C-FE-15` `ui` The glass medallion refracts the surrounding environment under directional, spot plus point lights. `src: Front-end specification, the three-dimensional layer`
- [ ] `C-FE-16` `ui` Credit medallions fall into a heap on the pricing route, more dropping at `300K`. `src: Front-end specification, the physics layer`
- [ ] `C-FE-17` `ui` The `Jingle` node shows a live waveform once sound is on. `src: Front-end specification, the sound layer`
- [ ] `C-FE-18` `ui` Cards carry a lift whose accent shadow strengthens when pointed at. `src: Front-end specification, the effects catalogue`
- [ ] `C-FE-19` `ui` A soft spotlight with a four-stop falloff follows a fine pointer. `src: Front-end specification, the effects catalogue`
- [ ] `C-FE-20` `ui` The Professional plan card carries a concave notch cut into the card. `src: Front-end specification, the effects catalogue`
- [ ] `C-FE-21` `ui` A faint dot grid lies on the dark ground beneath the grain. `src: Front-end specification, the effects catalogue`
- [ ] `C-FE-22` `ui` Each blog card's media carries a silhouette no other card shares. `src: Front-end specification, the effects catalogue`
- [ ] `C-FE-23` `ui` Enterprise tabs warm toward the accent when pointed at, never grey. `src: Front-end specification, hover states`
- [ ] `C-FE-24` `ui` A node card shows title, model attribution, an accent kind badge plus the output frame. `src: Front-end specification, the node showcase and replay canvas`
- [ ] `C-FE-25` `ui` Switching verticals cross-fades the graph without restarting the wire pulse. `src: Front-end specification, the node showcase and replay canvas`
- [ ] `C-FE-26` `ui` An opened node grows in place, pushing neighbours aside. `src: Front-end specification, the node showcase and replay canvas`
- [ ] `C-FE-27` `ui` The card corridor is a hallway of stills turned inward toward a central strip. `src: Front-end specification, route: home`
- [ ] `C-FE-28` `ui` The forecaster total counts toward the new figure with a medallion beside the total. `src: Front-end specification, route: pricing`
- [ ] `C-FE-29` `ui` A model page shows the gradient bar across the page under the name. `src: Front-end specification, route: models and model pages`
- [ ] `C-FE-30` `literal` The roster headline reads `Every model, one canvas.` `src: Front-end specification, route: models and model pages`
- [ ] `C-FE-31` `literal` The bench is headed `One brief. Up to four models.` with a `Run the comparison` action. `src: Front-end specification, route: bench`
- [ ] `C-FE-32` `ui` Bench frames show a running elapsed counter until the frame's result appears. `src: Front-end specification, route: bench`
- [ ] `C-FE-33` `literal` Each bench frame carries `data-frame-state` of `skeleton`, `settled` or `failed`. `src: Front-end specification, route: bench`
- [ ] `C-FE-34` `ui` Bench results appear as each lands, never as a batch. `src: Front-end specification, route: bench`
- [ ] `C-FE-35` `ui` The enterprise controls tab shows the `Northlight Studio` chip among three studio chips. `src: Front-end specification, route: enterprise`
- [ ] `C-FE-36` `ui` `Older posts` moves the blog to the next page of cards. `src: Front-end specification, route: blog`
- [ ] `C-FE-37` `ui` Blog filter changes re-run the card reveal in reading order. `src: Front-end specification, route: blog`
- [ ] `C-FE-38` `ui` About vignettes set the italic noun in the serif's true italic. `src: Front-end specification, route: about`
- [ ] `C-FE-39` `ui` The banded ground appears on wide screens; the organic blob replaces the band on narrow screens. `src: Front-end specification, route: about`
- [ ] `C-FE-40` `ui` The canvases table shows `Name`, `Nodes`, `Last run` plus `Credits spent` columns. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-41` `literal` Editor node elements carry `data-node-id` with a `data-node-state`. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-42` `ui` The billing page shows `Current plan` with `Credit balance` above a ledger table. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-43` `ui` The canvas toolbar offers `Add node` plus `Rerun stale nodes` beside the balance. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-44` `ui` The node panel carries `Title`, `Prompt`, `Model`, `Quality` plus `Aspect` fields. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-45` `ui` The node panel offers `Run node` plus `Deliver`. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-46` `ui` The team route offers `Invite a teammate` with a `Send invitation` action. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-47` `ui` A one-seat plan's team route replaces the invite field with a line naming `Professional`. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-48` `ui` The creator deliveries table shows `Output`, `Client`, `Sent` plus `State` columns. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-49` `literal` Delivery rows carry `data-delivery-state` of `delivered` or `revoked`. `src: Front-end specification, the signed-in tool`
- [ ] `C-FE-50` `ui` The creator deliveries table offers `Revoke` on each delivered row. `src: Front-end specification, the signed-in tool`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Studios are the only tenancy boundary, every read scoped to the caller's studio. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` No real company, product or person is named anywhere in the build. `src: Constraints para 2`
- [ ] `C-CN-03` `constraint` The documentation site appears as an external link only. `src: Constraints para 3`
- [ ] `C-CN-04` `constraint` Each download control resolves to the release record, with no installer shipped. `src: Constraints para 3`
- [ ] `C-CN-05` `constraint` The only backing services are PostgreSQL plus MinIO. `src: Constraints para 4`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-03` `contract` List endpoints return a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-04` `contract` A canvas write without a bearer token is refused as `unauthenticated`. `src: Deployment contract, API shapes`
- [ ] `C-DC-05` `constraint` Generated bytes live in the bucket, never on the app filesystem or in a database column. `src: Deployment contract, no mocks`
- [ ] `C-DC-06` `constraint` A run success always has an object in the bucket behind the output. `src: Deployment contract, no mocks`

## Pinned literals

| Value | Source | Item | Citation |
|---|---|---|---|
| `account_type` | pinned by the brief at the citation beside it | C-RL-18 | User roles, signup paragraph |
| `creator` | pinned by the brief at the citation beside it | C-RL-18 | User roles, signup paragraph |
| `client` | pinned by the brief at the citation beside it | C-RL-18 | User roles, signup paragraph |
| `creator@example.com` | pinned by the brief at the citation beside it | C-RL-20 | User roles, seeded accounts row 1 |
| `Noa Lindqvist` | pinned by the brief at the citation beside it | C-RL-20 | User roles, seeded accounts row 1 |
| `Northlight Studio` | pinned by the brief at the citation beside it | C-RL-20 | User roles, seeded accounts row 1 |
| `creator2@example.com` | pinned by the brief at the citation beside it | C-RL-21 | User roles, seeded accounts row 2 |
| `Rafael Moura` | pinned by the brief at the citation beside it | C-RL-21 | User roles, seeded accounts row 2 |
| `Saltmarsh Cut` | pinned by the brief at the citation beside it | C-RL-21 | User roles, seeded accounts row 2 |
| `creator3@example.com` | pinned by the brief at the citation beside it | C-RL-22 | User roles, seeded accounts row 3 |
| `Aiko Tanaka` | pinned by the brief at the citation beside it | C-RL-22 | User roles, seeded accounts row 3 |
| `Northlight Studio` | pinned by the brief at the citation beside it | C-RL-22 | User roles, seeded accounts row 3 |
| `client@example.com` | pinned by the brief at the citation beside it | C-RL-23 | User roles, seeded accounts row 4 |
| `Jonas Weber` | pinned by the brief at the citation beside it | C-RL-23 | User roles, seeded accounts row 4 |
| `deku-demo-pw-2026` | pinned by the brief at the citation beside it | C-CF-01 | Core features rule 1 |
| `Mina Park's studio` | pinned by the brief at the citation beside it | C-CF-08 | Core features rule 3 |
| `free` | pinned by the brief at the citation beside it | C-CF-08 | Core features rule 3 |
| `free` | pinned by the brief at the citation beside it | C-CF-17 | Core features rule 8 |
| `creator` | pinned by the brief at the citation beside it | C-CF-17 | Core features rule 8 |
| `growth` | pinned by the brief at the citation beside it | C-CF-17 | Core features rule 8 |
| `professional` | pinned by the brief at the citation beside it | C-CF-17 | Core features rule 8 |
| `enterprise` | pinned by the brief at the citation beside it | C-CF-17 | Core features rule 8 |
| `limit_reached` | pinned by the brief at the citation beside it | C-CF-18 | Core features rule 9 |
| `plan_required` | pinned by the brief at the citation beside it | C-CF-31 | Core features rule 12 |
| `limit_reached` | pinned by the brief at the citation beside it | C-CF-33 | Core features rule 12 |
| `auto` | pinned by the brief at the citation beside it | C-CF-42 | Core features rule 17 |
| `grain-4-turbo` | pinned by the brief at the citation beside it | C-CF-42 | Core features rule 17 |
| `auto` | pinned by the brief at the citation beside it | C-CF-43 | Core features rule 17 |
| `drift-1-6` | pinned by the brief at the citation beside it | C-CF-43 | Core features rule 17 |
| `auto` | pinned by the brief at the citation beside it | C-CF-44 | Core features rule 17 |
| `quill-3-mini` | pinned by the brief at the citation beside it | C-CF-44 | Core features rule 17 |
| `insufficient_credits` | pinned by the brief at the citation beside it | C-CF-65 | Core features rule 21 |
| `outputs/{workspace_id}/{node_id}/{sha256_of_bytes}.{ext}` | pinned by the brief at the citation beside it | C-CF-78 | Core features rule 26 |
| `halcyon-2-1` | pinned by the brief at the citation beside it | C-CF-94 | Core features rule 34 |
| `parley-2` | pinned by the brief at the citation beside it | C-CF-94 | Core features rule 34 |
| `lumen-preview` | pinned by the brief at the citation beside it | C-CF-95 | Core features rule 34 |
| `driftwood-beta` | pinned by the brief at the citation beside it | C-CF-96 | Core features rule 34 |
| `2048 x 2048` | pinned by the brief at the citation beside it | C-CF-97 | Core features rule 34 |
| `4:5` | pinned by the brief at the citation beside it | C-CF-98 | Core features rule 34 |
| `16:9` | pinned by the brief at the citation beside it | C-CF-98 | Core features rule 34 |
| `1:1` | pinned by the brief at the citation beside it | C-CF-98 | Core features rule 34 |
| `9:16` | pinned by the brief at the citation beside it | C-CF-98 | Core features rule 34 |
| `30` | pinned by the brief at the citation beside it | C-CF-98 | Core features rule 34 |
| `1920 x 1080` | pinned by the brief at the citation beside it | C-CF-99 | Core features rule 34 |
| `Creator buys 277 standard runs a month` | pinned by the brief at the citation beside it | C-CF-104 | Core features rule 36 |
| `20` | pinned by the brief at the citation beside it | C-CF-105 | Core features rule 36 |
| `500` | pinned by the brief at the citation beside it | C-CF-105 | Core features rule 36 |
| `5000` | pinned by the brief at the citation beside it | C-CF-105 | Core features rule 36 |
| `data-sample` | pinned by the brief at the citation beside it | C-CF-107 | Core features rule 36 |
| `data-output-kind` | pinned by the brief at the citation beside it | C-CF-110 | Core features rule 36 |
| `Try every model on the canvas` | pinned by the brief at the citation beside it | C-CF-113 | Core features rule 37 |
| `Deliver client work every week` | pinned by the brief at the citation beside it | C-CF-114 | Core features rule 37 |
| `Scale a busy solo practice fast` | pinned by the brief at the citation beside it | C-CF-115 | Core features rule 37 |
| `Run a studio on one shared canvas` | pinned by the brief at the citation beside it | C-CF-116 | Core features rule 37 |
| `One plan, every model.` | pinned by the brief at the citation beside it | C-CF-119 | Front-end specification, route: pricing |
| `Credits that follow the work.` | pinned by the brief at the citation beside it | C-CF-119 | Front-end specification, route: pricing |
| `How many credits does your work need?` | pinned by the brief at the citation beside it | C-CF-120 | Front-end specification, route: pricing |
| `277 images or 20 videos` | pinned by the brief at the citation beside it | C-CF-121 | Core features rule 38 |
| `694 images or 50 videos` | pinned by the brief at the citation beside it | C-CF-122 | Core features rule 38 |
| `1,527 images or 110 videos` | pinned by the brief at the citation beside it | C-CF-123 | Core features rule 38 |
| `Limited trial` | pinned by the brief at the citation beside it | C-CF-124 | Core features rule 38 |
| `Custom` | pinned by the brief at the citation beside it | C-CF-124 | Core features rule 38 |
| `Monthly` | pinned by the brief at the citation beside it | C-CF-125 | Core features rule 39 |
| `Annual` | pinned by the brief at the citation beside it | C-CF-125 | Core features rule 39 |
| `Save up to 15%` | pinned by the brief at the citation beside it | C-CF-125 | Core features rule 39 |
| `data-billing-period` | pinned by the brief at the citation beside it | C-CF-127 | Core features rule 39 |
| `monthly` | pinned by the brief at the citation beside it | C-CF-127 | Core features rule 39 |
| `annual` | pinned by the brief at the citation beside it | C-CF-127 | Core features rule 39 |
| `data-credit-option` | pinned by the brief at the citation beside it | C-CF-129 | Core features rule 40 |
| `110k` | pinned by the brief at the citation beside it | C-CF-129 | Core features rule 40 |
| `300k` | pinned by the brief at the citation beside it | C-CF-129 | Core features rule 40 |
| `Recompute` | pinned by the brief at the citation beside it | C-CF-141 | Core features rule 45 |
| `data-glow` | pinned by the brief at the citation beside it | C-CF-143 | Core features rule 46 |
| `on` | pinned by the brief at the citation beside it | C-CF-143 | Core features rule 46 |
| `data-plan` | pinned by the brief at the citation beside it | C-CF-145 | Core features rule 46 |
| `Creative tools` | pinned by the brief at the citation beside it | C-CF-146 | Core features rule 47 |
| `Support` | pinned by the brief at the citation beside it | C-CF-146 | Core features rule 47 |
| `Monthly credits` | pinned by the brief at the citation beside it | C-CF-147 | Core features rule 47 |
| `Additional credit packs` | pinned by the brief at the citation beside it | C-CF-147 | Core features rule 47 |
| `All models` | pinned by the brief at the citation beside it | C-CF-147 | Core features rule 47 |
| `Unlimited seats` | pinned by the brief at the citation beside it | C-CF-147 | Core features rule 47 |
| `Custom agent skills` | pinned by the brief at the citation beside it | C-CF-148 | Core features rule 47 |
| `Multiplayer canvas` | pinned by the brief at the citation beside it | C-CF-148 | Core features rule 47 |
| `Community support` | pinned by the brief at the citation beside it | C-CF-148 | Core features rule 47 |
| `Dedicated success manager` | pinned by the brief at the citation beside it | C-CF-148 | Core features rule 47 |
| `500 once` | pinned by the brief at the citation beside it | C-CF-150 | Core features rule 47 |
| `$10 per 1,000 credits` | pinned by the brief at the citation beside it | C-CF-150 | Core features rule 47 |
| `110,000 to 300,000` | pinned by the brief at the citation beside it | C-CF-150 | Core features rule 47 |
| `product-mockup` | pinned by the brief at the citation beside it | C-CF-154 | Core features rule 49 |
| `movie-cut-1` | pinned by the brief at the citation beside it | C-CF-154 | Core features rule 49 |
| `data-graph-key` | pinned by the brief at the citation beside it | C-CF-155 | Core features rule 49 |
| `data-node-key` | pinned by the brief at the citation beside it | C-CF-155 | Core features rule 49 |
| `data-node-state` | pinned by the brief at the citation beside it | C-CF-155 | Core features rule 49 |
| `stale_generation` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 53 |
| `My first canvas 2` | pinned by the brief at the citation beside it | C-CF-172 | Core features rule 55 |
| `data-chip-state` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 57 |
| `rest` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 57 |
| `active` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 57 |
| `rejected` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 57 |
| `insufficient_credits` | pinned by the brief at the citation beside it | C-CF-181 | Core features rule 58 |
| `lumen-preview` | pinned by the brief at the citation beside it | C-CF-183 | Core features rule 59 |
| `Engine unavailable` | pinned by the brief at the citation beside it | C-CF-183 | Core features rule 59 |
| `driftwood-beta` | pinned by the brief at the citation beside it | C-CF-184 | Core features rule 59 |
| `timed_out` | pinned by the brief at the citation beside it | C-CF-184 | Core features rule 59 |
| `Describe what you want to make` | pinned by the brief at the citation beside it | C-CF-200 | Core features rule 64 |
| `Start the replay` | pinned by the brief at the citation beside it | C-CF-200 | Core features rule 64 |
| `Agencies` | pinned by the brief at the citation beside it | C-CF-202 | Core features rule 65 |
| `Go-to-market` | pinned by the brief at the citation beside it | C-CF-202 | Core features rule 65 |
| `Campaign variants` | pinned by the brief at the citation beside it | C-CF-203 | Core features rule 65 |
| `Launch films` | pinned by the brief at the citation beside it | C-CF-203 | Core features rule 65 |
| `Vesper 3 is now on Quarro.` | pinned by the brief at the citation beside it | C-CF-204 | Core features rule 66 |
| `Your studio, one canvas.` | pinned by the brief at the citation beside it | C-CF-206 | Core features rule 67 |
| `Collaborative canvas` | pinned by the brief at the citation beside it | C-CF-209 | Core features rule 67 |
| `Agent connector` | pinned by the brief at the citation beside it | C-CF-209 | Core features rule 67 |
| `Brand kits` | pinned by the brief at the citation beside it | C-CF-209 | Core features rule 67 |
| `Chat-tool creation` | pinned by the brief at the citation beside it | C-CF-209 | Core features rule 67 |
| `Shared asset library` | pinned by the brief at the citation beside it | C-CF-209 | Core features rule 67 |
| `2.4.0` | pinned by the brief at the citation beside it | C-CF-215 | Core features rule 69 |
| `Download for macOS (Apple silicon)` | pinned by the brief at the citation beside it | C-CF-216 | Core features rule 69 |
| `Download for macOS (Intel)` | pinned by the brief at the citation beside it | C-CF-216 | Core features rule 69 |
| `Download for Windows` | pinned by the brief at the citation beside it | C-CF-216 | Core features rule 69 |
| `Download for Linux` | pinned by the brief at the citation beside it | C-CF-216 | Core features rule 69 |
| `Quarro for your desktop.` | pinned by the brief at the citation beside it | C-CF-217 | Core features rule 69 |
| `data-primary-platform` | pinned by the brief at the citation beside it | C-CF-218 | Core features rule 69 |
| `Made by hand, at the speed of thought.` | pinned by the brief at the citation beside it | C-CF-221 | Core features rule 70 |
| `Field notes, guides` | pinned by the brief at the citation beside it | C-CF-223 | Core features rule 71 |
| `and model comparisons.` | pinned by the brief at the citation beside it | C-CF-223 | Core features rule 71 |
| `Ines Carvalho` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Tomas Reyes` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Hana Okafor` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Luca Brandt` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Mira Solberg` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Dev Anand` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Clara Voss` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Sami Haddad` | pinned by the brief at the citation beside it | C-CF-231 | Core features rule 72 |
| `Senior Graphics Engineer` | pinned by the brief at the citation beside it | C-CF-232 | Core features rule 72 |
| `Product Designer, Canvas` | pinned by the brief at the citation beside it | C-CF-232 | Core features rule 72 |
| `Model Partnerships Lead` | pinned by the brief at the citation beside it | C-CF-232 | Core features rule 72 |
| `Staff Backend Engineer, Billing` | pinned by the brief at the citation beside it | C-CF-232 | Core features rule 72 |
| `Community Producer` | pinned by the brief at the citation beside it | C-CF-232 | Core features rule 72 |
| `Amara Whitfield` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Kenji Morrow` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Sofia Brennan` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Owen Castell` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Lena Hartmann` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Marcus Obi` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Yara Lindgren` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Theo Marchetti` | pinned by the brief at the citation beside it | C-CF-233 | Core features rule 72 |
| `Porto` | pinned by the brief at the citation beside it | C-CF-234 | Core features rule 72 |
| `Bonfim` | pinned by the brief at the citation beside it | C-CF-234 | Core features rule 72 |
| `privacy@quarro.dev` | pinned by the brief at the citation beside it | C-CF-236 | Core features rule 73 |
| `og:title` | pinned by the brief at the citation beside it | C-CF-239 | Core features rule 75 |
| `og:image` | pinned by the brief at the citation beside it | C-CF-239 | Core features rule 75 |
| `Back to home` | pinned by the brief at the citation beside it | C-CF-244 | Core features rule 77 |
| `No canvases yet. Name one above to start.` | pinned by the brief at the citation beside it | C-UF-18 | User flow, states |
| `Nothing has been delivered to you yet.` | pinned by the brief at the citation beside it | C-UF-19 | User flow, states |
| `deku-demo-pw-2026` | pinned by the brief at the citation beside it | C-DM-01 | Data model, password paragraph |
| `Northlight Studio` | pinned by the brief at the citation beside it | C-DM-09 | Data model, seed data |
| `professional` | pinned by the brief at the citation beside it | C-DM-09 | Data model, seed data |
| `108,596` | pinned by the brief at the citation beside it | C-DM-09 | Data model, seed data |
| `Saltmarsh Cut` | pinned by the brief at the citation beside it | C-DM-10 | Data model, seed data |
| `creator` | pinned by the brief at the citation beside it | C-DM-10 | Data model, seed data |
| `20,000` | pinned by the brief at the citation beside it | C-DM-10 | Data model, seed data |
| `Citrus Launch` | pinned by the brief at the citation beside it | C-DM-11 | Data model, seed data |
| `Autumn Lookbook` | pinned by the brief at the citation beside it | C-DM-12 | Data model, seed data |
| `Trailer Cut` | pinned by the brief at the citation beside it | C-DM-13 | Data model, seed data |
| `OOH Billboard` | pinned by the brief at the citation beside it | C-DM-14 | Data model, seed data |
| `client@example.com` | pinned by the brief at the citation beside it | C-DM-14 | Data model, seed data |
| `Billboard for sign-off` | pinned by the brief at the citation beside it | C-DM-14 | Data model, seed data |
| `Quarro raises its Series A to build the one canvas` | pinned by the brief at the citation beside it | C-DM-15 | Data model, seed data |
| `Company` | pinned by the brief at the citation beside it | C-FE-10 | Front-end specification, the chrome |
| `Resources` | pinned by the brief at the citation beside it | C-FE-10 | Front-end specification, the chrome |
| `Legal` | pinned by the brief at the citation beside it | C-FE-10 | Front-end specification, the chrome |
| `Quarro, Porto` | pinned by the brief at the citation beside it | C-FE-10 | Front-end specification, the chrome |
| `Every model, one canvas.` | pinned by the brief at the citation beside it | C-FE-30 | Front-end specification, route: models and model pages |
| `One brief. Up to four models.` | pinned by the brief at the citation beside it | C-FE-31 | Front-end specification, route: bench |
| `Run the comparison` | pinned by the brief at the citation beside it | C-FE-31 | Front-end specification, route: bench |
| `data-frame-state` | pinned by the brief at the citation beside it | C-FE-33 | Front-end specification, route: bench |
| `skeleton` | pinned by the brief at the citation beside it | C-FE-33 | Front-end specification, route: bench |
| `settled` | pinned by the brief at the citation beside it | C-FE-33 | Front-end specification, route: bench |
| `failed` | pinned by the brief at the citation beside it | C-FE-33 | Front-end specification, route: bench |
| `data-node-id` | pinned by the brief at the citation beside it | C-FE-41 | Front-end specification, the signed-in tool |
| `data-node-state` | pinned by the brief at the citation beside it | C-FE-41 | Front-end specification, the signed-in tool |
| `data-delivery-state` | pinned by the brief at the citation beside it | C-FE-49 | Front-end specification, the signed-in tool |
| `delivered` | pinned by the brief at the citation beside it | C-FE-49 | Front-end specification, the signed-in tool |
| `revoked` | pinned by the brief at the citation beside it | C-FE-49 | Front-end specification, the signed-in tool |
| `Sep 10, 2026` | pinned by the brief at the citation beside it | C-CF-228 | Core features rule 71 |
| `4 min read` | pinned by the brief at the citation beside it | C-CF-228 | Core features rule 71 |
| `One canvas, one subscription, every image, video, sound and language model worth using. Ivo picks one when you do not.` | pinned by the brief at the citation beside it | C-CF-201 | Core features rule 64 |
| `This page is not on the canvas.` | pinned by the brief at the citation beside it | C-CF-244 | Core features rule 77 |
| `This node changed since you opened it.` | pinned by the brief at the citation beside it | C-UF-16 | User flow, journeys |
| `Rates changed since this forecast.` | pinned by the brief at the citation beside it | C-CF-141 | Core features rule 45 |
| `Make it once.` | pinned by the brief at the citation beside it | C-CF-199 | Core features rule 64 |
| `Then make it everywhere.` | pinned by the brief at the citation beside it | C-CF-199 | Core features rule 64 |
| `Usage and limits` | pinned by the brief at the citation beside it | C-CF-146 | Core features rule 47 |
| `Two models failed, so this comparison was cancelled and nothing was charged.` | pinned by the brief at the citation beside it | C-CF-190 | Core features rule 60 |
| `Retry this model` | pinned by the brief at the citation beside it | C-CF-191 | Core features rule 60 |
| `Try it on the canvas` | pinned by the brief at the citation beside it | C-CF-204 | Core features rule 66 |
| `You do not have to choose. Describe what you want and Ivo routes the brief to the right model; every engine below is one click away when you do.` | pinned by the brief at the citation beside it | C-CF-101 | Core features rule 35 |
| `Bring the whole team and its rules` | pinned by the brief at the citation beside it | C-CF-117 | Core features rule 37 |
| `Field and Frame` | pinned by the brief at the citation beside it | C-FE-35 | Front-end specification, route: enterprise |
| `score-lite` | pinned by the brief at the citation beside it | C-CF-47 | Core features rule 17 |
| `Queue priority` | pinned by the brief at the citation beside it | C-CF-149 | Core features rule 47 |
| `Priority email support` | pinned by the brief at the citation beside it | C-CF-149 | Core features rule 47 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the briefs, wiring and models of the four non-advertising replay graphs | C-CF-152 | left to the builder inside the stated rules |
| the exact colour value behind every named role | C-UX-14 | carried as family, tone and shade rather than as a value |
| the gradient stop colours of each model | C-CF-93 | a count of six or seven is pinned, the colours are not |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 7 | 7 |
| User roles | 20 | 23 |
| Core features | 170 | 244 |
| User flow | 19 | 22 |
| UI and UX notes | 36 | 38 |
| Technical requirements | 10 | 13 |
| Data model | 15 | 16 |
| Front-end specification | 44 | 50 |
| Constraints | 5 | 5 |
| Deployment contract | 6 | 6 |

`## Definition of done` produces no items. Every clause in it restates an ask already
carried by `## Core features`, and a restatement folds into the item it restates.

Asks extracted and then withdrawn because no channel observes them reliably from outside the
running product without control over time, token expiry or the network: the framework and library names, the structured request log, the
absence of a second datastore, the performance budgets and frame-time figures, the
texture-memory and shader-compile budgets, the font loading behaviour, the absence of
committed binary files, the credential file at the app root, the reserved empty
directories, the process outliving the session, the loopback bind, the absence of edge
functions or persistent volumes, the table count, the ninety-day retention of bench
records, the thirty-day win-rate window, the one-day stale-forecast reload, and the
seven-day replay session lifetime, the absence of outbound email, the port 4173, the
production build, the absence of manual steps, the absence of outbound calls, the
token lifetime, the expired-token notice, the discard of older tokens, the day-old
recompute, the three-hundred-per-address limit, the touch-target floor beyond the header
(the forecaster slider handle at narrow widths among them), and the password reset. Each is a real requirement of the brief and none is
graded, so none appears here. Recorded rather than carried, per OPEN-DECISIONS D-H.
