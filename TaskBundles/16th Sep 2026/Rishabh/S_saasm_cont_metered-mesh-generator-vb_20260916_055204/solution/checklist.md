# Checklist: Voxelith

Items: 481
Unpinned values flagged: 3
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-BP, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product converts an uploaded photograph into a downloadable three-dimensional mesh. `src: Overview`
- [ ] `C-OV-02` `capability` The product converts a written prompt into a downloadable three-dimensional mesh. `src: Overview`
- [ ] `C-OV-03` `capability` A submitted conversion is a queued job carrying a visible state. `src: Overview`
- [ ] `C-OV-04` `constraint` A job still running when the page is refreshed remains running after the page returns. `src: Overview`
- [ ] `C-OV-05` `capability` A conversion is metered in credits granted monthly by plan. `src: Overview`
- [ ] `C-OV-06` `constraint` A job that fails costs the account no credit. `src: Overview`
- [ ] `C-OV-07` `constraint` Two jobs submitted against a balance with room for one resolve to one accepted job. `src: Overview`
- [ ] `C-OV-08` `data` A produced asset carries the licence granted by the plan held at the moment of creation. `src: Overview`
- [ ] `C-OV-09` `constraint` An asset made under the free plan remains openly licensed after the owning account upgrades. `src: Overview`
- [ ] `C-OV-10` `data` A produced asset carries a deletion date derived from the plan held at creation. `src: Overview`
- [ ] `C-OV-11` `constraint` Archiving an asset leaves the asset deletion date unchanged. `src: Overview`
- [ ] `C-OV-12` `capability` A visitor holding no account generates one model from the generator. `src: Overview`
- [ ] `C-OV-13` `constraint` The anonymous allowance is enforced on the server against a stored subject. `src: Overview`
- [ ] `C-OV-14` `capability` Work produced by an anonymous visitor moves into the account created by that visitor. `src: Overview`
- [ ] `C-OV-15` `capability` Three tools run wholly inside the browser under `/3d-tools`. `src: Overview`
- [ ] `C-OV-16` `constraint` A tool under `/3d-tools` uploads nothing. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` The stored role set is `creator`, `visitor`. `src: User roles`
- [ ] `C-RL-02` `role` An account holding `creator` owns a plan, a credit balance, a private asset library. `src: User roles`
- [ ] `C-RL-03` `role` A `visitor` holds no account. `src: User roles`
- [ ] `C-RL-04` `role` A `visitor` reaches the gallery, the pricing page, the three local tools, the legal pages. `src: User roles`
- [ ] `C-RL-05` `constraint` A `creator` cannot read an asset belonging to a second `creator`. `src: User roles`
- [ ] `C-RL-06` `constraint` A `creator` cannot download an asset belonging to a second `creator`. `src: User roles`
- [ ] `C-RL-07` `constraint` A `creator` cannot rename an asset belonging to a second `creator`. `src: User roles`
- [ ] `C-RL-08` `constraint` A `creator` cannot generate at a quality tier the held plan excludes. `src: User roles`
- [ ] `C-RL-09` `constraint` A `creator` cannot spend credit the account balance does not hold. `src: User roles`
- [ ] `C-RL-10` `constraint` A `visitor` cannot start a second anonymous generation. `src: User roles`
- [ ] `C-RL-11` `capability` Registration is open to anybody at `/sign-up`. `src: User roles`
- [ ] `C-RL-12` `contract` Ownership is enforced on the server on every asset read. `src: User roles`
- [ ] `C-RL-13` `contract` Ownership is enforced on the server on every stored object read. `src: User roles`
- [ ] `C-RL-14` `contract` An asset requested by a session belonging to a second account receives `404`. `src: User roles`
- [ ] `C-RL-15` `contract` A stored object requested by a session belonging to a second account receives `404`. `src: User roles`
- [ ] `C-RL-16` `contract` An asset requested with no session receives `401`. `src: User roles`
- [ ] `C-RL-17` `data` An account is deactivated rather than removed from storage. `src: User roles`
- [ ] `C-RL-18` `ui` Account deletion states what an open licence already granted cannot recall. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` A visitor registers at `/sign-up` with an email address, a password. `src: Core features 1`
- [ ] `C-CF-02` `capability` A registered account signing up lands on `/my-assets`. `src: Core features 1`
- [ ] `C-CF-03` `capability` A seeded account signs in at `/sign-in` with an email address, a password. `src: Core features 1`
- [ ] `C-CF-04` `contract` A sign-in carrying a wrong password receives `401`. `src: Core features 1`
- [ ] `C-CF-05` `contract` A sign-in failure message does not disclose which half of the pair was wrong. `src: Core features 1`
- [ ] `C-CF-06` `contract` A library endpoint called with no session receives `401`. `src: Core features 1`
- [ ] `C-CF-07` `literal` The stored quality tier keys are `fast`, `standard`, `pro`, `ultra`. `src: Core features 2`
- [ ] `C-CF-08` `literal` The tier `fast` stores octree resolution `196`, inference steps `20`, polygon ceiling `15000`, credit cost `2`. `src: Core features 2`
- [ ] `C-CF-09` `literal` The tier `standard` stores octree resolution `256`, inference steps `30`, polygon ceiling `30000`, credit cost `5`. `src: Core features 2`
- [ ] `C-CF-10` `literal` The tier `pro` stores octree resolution `384`, inference steps `40`, polygon ceiling `60000`, credit cost `10`. `src: Core features 2`
- [ ] `C-CF-11` `literal` The tier `ultra` stores octree resolution `512`, inference steps `50`, polygon ceiling `300000`, credit cost `20`. `src: Core features 2`
- [ ] `C-CF-12` `constraint` The generator control reads the stored tier table. `src: Core features 2`
- [ ] `C-CF-13` `constraint` The pricing page reads the stored tier table. `src: Core features 2`
- [ ] `C-CF-14` `literal` The maximum polygon ceiling published anywhere on the site is `300000`. `src: Core features 2`
- [ ] `C-CF-15` `contract` A write setting a tier outside the four stored keys receives `422`. `src: Core features 2`
- [ ] `C-CF-16` `data` A job records the octree resolution that produced the result. `src: Core features 2`
- [ ] `C-CF-17` `data` A job records the inference step count that produced the result. `src: Core features 2`
- [ ] `C-CF-18` `literal` The generator source mode is `image-to-3d` or `text-to-3d`. `src: Core features 3`
- [ ] `C-CF-19` `literal` The generator input mode is `single-image` or `multiple-images`. `src: Core features 3`
- [ ] `C-CF-20` `ui` The four quality tiers appear as a labelled radio group. `src: Core features 3`
- [ ] `C-CF-21` `ui` The generator carries a texture toggle. `src: Core features 3`
- [ ] `C-CF-22` `ui` The credit cost appears beside the generate control. `src: Core features 3`
- [ ] `C-CF-23` `constraint` The input mode `multiple-images` is available only at the tier `ultra`. `src: Core features 3`
- [ ] `C-CF-24` `constraint` The input mode `multiple-images` is available only to a paid plan. `src: Core features 3`
- [ ] `C-CF-25` `literal` The credit cost is the tier cost plus `5` when textures are on. `src: Core features 3`
- [ ] `C-CF-26` `literal` The credit cost rises by `10` when the input mode is `multiple-images`. `src: Core features 3`
- [ ] `C-CF-27` `literal` The default generator state costs `10` credits. `src: Core features 3`
- [ ] `C-CF-28` `ui` The displayed credit cost updates as a generator control changes. `src: Core features 3`
- [ ] `C-CF-29` `constraint` The credit cost charged equals the credit cost displayed at submission. `src: Core features 3`
- [ ] `C-CF-30` `constraint` An edit to the tier table after display does not change the credit cost charged. `src: Core features 3`
- [ ] `C-CF-31` `ui` The confirmation step names the licence the result carries before submission. `src: Core features 4`
- [ ] `C-CF-32` `literal` An asset created under the free plan carries the licence `CC-BY-4.0`. `src: Core features 4`
- [ ] `C-CF-33` `literal` An asset created by an anonymous visitor carries the licence `CC-BY-4.0`. `src: Core features 4`
- [ ] `C-CF-34` `literal` An asset created under a paid plan carries the licence `customer-owned`. `src: Core features 4`
- [ ] `C-CF-35` `ui` The generator accepts a source file through a file input. `src: Core features 5`
- [ ] `C-CF-36` `ui` The generator accepts a source file through a drop target. `src: Core features 5`
- [ ] `C-CF-37` `ui` The generator accepts a source file through a paste handler. `src: Core features 5`
- [ ] `C-CF-38` `literal` The accepted source formats are `JPG`, `PNG`, `WEBP`. `src: Core features 5`
- [ ] `C-CF-39` `contract` A source file outside the accepted formats is rejected inline with the found format named. `src: Core features 5`
- [ ] `C-CF-40` `constraint` A rejected source file is not stored. `src: Core features 5`
- [ ] `C-CF-41` `literal` A job state is one of `queued`, `processing`, `completed`, `failed`. `src: Core features 6`
- [ ] `C-CF-42` `capability` Submission returns a job in the state `queued`. `src: Core features 6`
- [ ] `C-CF-43` `ui` A running job shows a queue position or a named stage. `src: Core features 6`
- [ ] `C-CF-44` `constraint` A running job state survives a page reload. `src: Core features 6`
- [ ] `C-CF-45` `constraint` A single poller serves the whole document rather than one poller per open tab. `src: Core features 6`
- [ ] `C-CF-46` `data` Credit is reserved when a job starts. `src: Core features 6`
- [ ] `C-CF-47` `data` Credit is settled when a job ends. `src: Core features 6`
- [ ] `C-CF-48` `constraint` A job ending `failed` returns the reservation in full. `src: Core features 6`
- [ ] `C-CF-49` `ui` An account owning a job ending `failed` is told of the refund. `src: Core features 6`
- [ ] `C-CF-50` `constraint` The balance after a failed job equals the balance before the reservation. `src: Core features 6`
- [ ] `C-CF-51` `constraint` A second submission carrying an existing idempotency key produces one asset. `src: Core features 6`
- [ ] `C-CF-52` `constraint` A second submission carrying an existing idempotency key spends one reservation. `src: Core features 6`
- [ ] `C-CF-53` `contract` A second submission carrying an existing idempotency key answers with the existing job. `src: Core features 6`
- [ ] `C-CF-54` `contract` A submission whose cost exceeds the available balance receives `402`. `src: Core features 6`
- [ ] `C-CF-55` `constraint` A submission rejected for insufficient balance reserves nothing. `src: Core features 6`
- [ ] `C-CF-56` `contract` Of two submissions arriving together against a balance with room for one, the second receives `402`. `src: Core features 6`
- [ ] `C-CF-57` `constraint` The ledger after two simultaneous submissions against a balance with room for one shows one reservation. `src: Core features 6`
- [ ] `C-CF-58` `constraint` No readable balance value falls below zero. `src: Core features 6`
- [ ] `C-CF-59` `literal` The stored queue placement values are `limited`, `standard`, `higher`. `src: Core features 7`
- [ ] `C-CF-60` `data` A job records the queue placement drawn from the plan held at submission. `src: Core features 7`
- [ ] `C-CF-61` `constraint` An upgrade applied after submission does not advance a queued job. `src: Core features 7`
- [ ] `C-CF-62` `constraint` A downgrade applied after submission does not retard a queued job. `src: Core features 7`
- [ ] `C-CF-63` `constraint` A completed job produces exactly one asset. `src: Core features 8`
- [ ] `C-CF-64` `literal` An asset carries representations of kind `glb`, `obj`, `stl`, `texture-map`, `preview`. `src: Core features 8`
- [ ] `C-CF-65` `constraint` Downloading a second representation of one asset spends no further credit. `src: Core features 8`
- [ ] `C-CF-66` `constraint` Downloading a second representation of one asset creates no second library entry. `src: Core features 8`
- [ ] `C-CF-67` `data` Each download is recorded against the asset with the representation kind, the time. `src: Core features 8`
- [ ] `C-CF-68` `constraint` The download history of an asset is visible to the owning account alone. `src: Core features 8`
- [ ] `C-CF-69` `capability` An exported archive contains the mesh alongside a file stating the asset licence. `src: Core features 9`
- [ ] `C-CF-70` `constraint` An exported archive under `CC-BY-4.0` states the attribution requirement. `src: Core features 9`
- [ ] `C-CF-71` `data` An asset stores the plan under which the asset was created. `src: Core features 10`
- [ ] `C-CF-72` `constraint` An upgrade from the free plan to a paid plan does not relicense an existing asset. `src: Core features 10`
- [ ] `C-CF-73` `contract` A request changing a stored asset licence receives `409`. `src: Core features 10`
- [ ] `C-CF-74` `literal` The retention under the free plan is `7` days. `src: Core features 11`
- [ ] `C-CF-75` `literal` The retention under the plan `pro` is `180` days. `src: Core features 11`
- [ ] `C-CF-76` `literal` The plan `max` keeps an asset permanently. `src: Core features 11`
- [ ] `C-CF-77` `ui` An asset shows the deletion date. `src: Core features 11`
- [ ] `C-CF-78` `ui` A warning precedes the deletion of an asset. `src: Core features 11`
- [ ] `C-CF-79` `constraint` A downgrade does not shorten the deletion date of an existing asset. `src: Core features 11`
- [ ] `C-CF-80` `ui` The interface states the effect on existing deletion dates before a downgrade completes. `src: Core features 11`
- [ ] `C-CF-81` `constraint` An asset created after a downgrade carries the retention of the plan held after the downgrade. `src: Core features 11`
- [ ] `C-CF-82` `capability` The library at `/my-assets` is reachable behind a session. `src: Core features 12`
- [ ] `C-CF-83` `ui` The library filters by the statuses `completed`, `processing`, `failed`. `src: Core features 12`
- [ ] `C-CF-84` `ui` The library filters by any stored tag. `src: Core features 12`
- [ ] `C-CF-85` `ui` The library filters by the favourite flag. `src: Core features 12`
- [ ] `C-CF-86` `capability` An asset favourite flag is set, unset by the owning account. `src: Core features 12`
- [ ] `C-CF-87` `capability` An asset title is editable by the owning account. `src: Core features 12`
- [ ] `C-CF-88` `capability` An asset description is editable by the owning account. `src: Core features 12`
- [ ] `C-CF-89` `capability` An asset carries many tags. `src: Core features 12`
- [ ] `C-CF-90` `constraint` Library filters for status, tag, favourite apply together. `src: Core features 12`
- [ ] `C-CF-91` `constraint` An archived asset leaves the default library view. `src: Core features 12`
- [ ] `C-CF-92` `constraint` An archived asset remains reachable behind an explicit archived filter. `src: Core features 12`
- [ ] `C-CF-93` `constraint` An archived asset continues to exist in storage. `src: Core features 12`
- [ ] `C-CF-94` `literal` The anonymous allowance is `1` generation. `src: Core features 13`
- [ ] `C-CF-95` `constraint` The anonymous allowance is enforced against a stored subject rather than a cookie. `src: Core features 13`
- [ ] `C-CF-96` `literal` The four offered samples are `sneaker`, `mug`, `chair`, `plant`. `src: Core features 13`
- [ ] `C-CF-97` `constraint` Choosing a sample serves a stored pre-computed asset. `src: Core features 13`
- [ ] `C-CF-98` `constraint` Choosing a sample starts no conversion. `src: Core features 13`
- [ ] `C-CF-99` `contract` A second anonymous generation attempt receives `429`. `src: Core features 13`
- [ ] `C-CF-100` `ui` A refused second anonymous attempt names the spent free allowance as the reason. `src: Core features 13`
- [ ] `C-CF-101` `ui` A refused second anonymous attempt offers registration. `src: Core features 13`
- [ ] `C-CF-102` `literal` An anonymous claim token is valid for `24` hours. `src: Core features 13`
- [ ] `C-CF-103` `capability` An account registered inside the claim window receives the anonymous asset into the library. `src: Core features 13`
- [ ] `C-CF-104` `constraint` An asset claimed after registration keeps the licence stamped at creation. `src: Core features 13`
- [ ] `C-CF-105` `contract` A claim token presented after the claim window receives `410`. `src: Core features 13`
- [ ] `C-CF-106` `literal` The free plan grants `10` credits monthly. `src: Core features 14`
- [ ] `C-CF-107` `literal` The free plan grants a welcome gift of `5` credits. `src: Core features 14`
- [ ] `C-CF-108` `data` The free welcome gift is drawn from a pool that empties. `src: Core features 14`
- [ ] `C-CF-109` `contract` A welcome grant refused for an exhausted pool receives `409`. `src: Core features 14`
- [ ] `C-CF-110` `ui` A welcome grant refused for an exhausted pool names the exhausted pool. `src: Core features 14`
- [ ] `C-CF-111` `constraint` The monthly grant is anchored to the account subscription anniversary. `src: Core features 15`
- [ ] `C-CF-112` `constraint` Granting one monthly period twice grants once. `src: Core features 15`
- [ ] `C-CF-113` `constraint` Unspent monthly credits do not roll over. `src: Core features 15`
- [ ] `C-CF-114` `constraint` The welcome grant does not expire. `src: Core features 15`
- [ ] `C-CF-115` `ui` The pricing page states the roll-over rule for monthly credits. `src: Core features 15`
- [ ] `C-CF-116` `literal` The stored plan keys are `free`, `pro`, `max`. `src: Core features 16`
- [ ] `C-CF-117` `literal` The plan `free` costs `$0`. `src: Core features 16`
- [ ] `C-CF-118` `literal` The plan `pro` lists at `$15.00` per month, struck to `$9.90` per month. `src: Core features 16`
- [ ] `C-CF-119` `literal` The plan `max` lists at `$39.00` per month, struck to `$19.90` per month. `src: Core features 16`
- [ ] `C-CF-120` `literal` The plan `pro` carries the badge `-34% OFF`. `src: Core features 16`
- [ ] `C-CF-121` `literal` The plan `max` carries the badges `-50% OFF`, `Most Popular`. `src: Core features 16`
- [ ] `C-CF-122` `literal` The plan `pro` grants `1000` credits monthly. `src: Core features 16`
- [ ] `C-CF-123` `literal` The plan `max` grants `4000` credits monthly. `src: Core features 16`
- [ ] `C-CF-124` `constraint` The plan `free` permits the tiers `fast`, `standard` alone. `src: Core features 16`
- [ ] `C-CF-125` `constraint` The plan `free` permits the source modes single image, text alone. `src: Core features 16`
- [ ] `C-CF-126` `literal` The plan `free` carries the polygon ceiling `60000`. `src: Core features 16`
- [ ] `C-CF-127` `literal` The plan `pro` carries the polygon ceiling `300000`. `src: Core features 16`
- [ ] `C-CF-128` `constraint` The plan `free` permits no textures. `src: Core features 16`
- [ ] `C-CF-129` `capability` A paid plan permits 4K PBR textures. `src: Core features 16`
- [ ] `C-CF-130` `ui` The pricing page states unlimited downloads of completed models. `src: Core features 16`
- [ ] `C-CF-131` `ui` The pricing page offers email support within 24h on the plan `pro`. `src: Core features 16`
- [ ] `C-CF-132` `ui` The pricing page offers an uptime commitment on the plan `max`. `src: Core features 16`
- [ ] `C-CF-133` `data` A promotion stores a start date, an end date. `src: Core features 17`
- [ ] `C-CF-134` `literal` The active promotion runs from `2026-09-01` to `2026-12-31`. `src: Core features 17`
- [ ] `C-CF-135` `constraint` The list price is charged after the promotion end date. `src: Core features 17`
- [ ] `C-CF-136` `constraint` The list price is displayed after the promotion end date. `src: Core features 17`
- [ ] `C-CF-137` `capability` The gallery at `/gallery` shows a source image beside a finished render. `src: Core features 18`
- [ ] `C-CF-138` `ui` A gallery item names the source of the item. `src: Core features 18`
- [ ] `C-CF-139` `ui` A gallery item names the quality tier that produced the item. `src: Core features 18`
- [ ] `C-CF-140` `literal` The published gallery items are `Brass Compass` at `pro`, `Woven Basket` at `standard`, `Carved Owl` at `ultra`, `Tin Robot` at `fast`. `src: Core features 18`
- [ ] `C-CF-141` `data` A published figure is stored as one row carrying a value, a basis, a measurement date. `src: Core features 19`
- [ ] `C-CF-142` `literal` The stored figure `models_created` is `25000`, measured `2026-09-01`. `src: Core features 19`
- [ ] `C-CF-143` `literal` The stored figure `average_rating` is `4.9` of `5`, measured `2026-09-01`. `src: Core features 19`
- [ ] `C-CF-144` `literal` The stored figure `success_rate` is `99.0` percent, measured `2026-09-01`. `src: Core features 19`
- [ ] `C-CF-145` `literal` The stored figure `countries_served` is `80`, measured `2026-09-01`. `src: Core features 19`
- [ ] `C-CF-146` `literal` The stored figure `average_cost_usd` is `$0.50`, measured `2026-09-01`. `src: Core features 19`
- [ ] `C-CF-147` `literal` The stored figure `conversion_minutes` is `2` to `3`, measured `2026-09-01`. `src: Core features 19`
- [ ] `C-CF-148` `constraint` A published figure is rendered from the stored row everywhere the figure appears. `src: Core features 19`
- [ ] `C-CF-149` `constraint` The figure `success_rate` appears as one value across the whole site. `src: Core features 19`
- [ ] `C-CF-150` `ui` The comparison table compares conversion time `2-3 Days` against `2-3 Minutes`. `src: Core features 20`
- [ ] `C-CF-151` `ui` The comparison table compares success rate `Variable` against `99.0%`. `src: Core features 20`
- [ ] `C-CF-152` `ui` The comparison table compares average cost `$200+` against `$0.50`. `src: Core features 20`
- [ ] `C-CF-153` `ui` The comparison table compares training required `Months` against `None`. `src: Core features 20`
- [ ] `C-CF-154` `ui` The comparison table shows the measurement date beside each stored figure. `src: Core features 20`
- [ ] `C-CF-155` `capability` The route `/3d-tools/online-viewer` previews `15` mesh formats. `src: Core features 21`
- [ ] `C-CF-156` `literal` The viewer format list names `GLB`, `OBJ`, `STL`, `FBX`, `STEP`. `src: Core features 21`
- [ ] `C-CF-157` `capability` The route `/3d-tools/file-converter` converts between declared format pairs. `src: Core features 21`
- [ ] `C-CF-158` `literal` The declared supported conversion pair count is `128`. `src: Core features 21`
- [ ] `C-CF-159` `capability` The route `/3d-tools/3d-text-generator` exports typed text as `GLB`, `OBJ`, `STL`. `src: Core features 21`
- [ ] `C-CF-160` `constraint` A route under `/3d-tools` issues no network request after the initial load. `src: Core features 21`
- [ ] `C-CF-161` `constraint` A route under `/3d-tools` sends no measurement of visitor behaviour. `src: Core features 21`
- [ ] `C-CF-162` `data` The converter holds a conversion matrix of format pairs. `src: Core features 21`
- [ ] `C-CF-163` `constraint` The supported pair count printed by the converter equals the supported entry count of the conversion matrix. `src: Core features 21`
- [ ] `C-CF-164` `contract` A file in an unsupported format is refused with the found format named. `src: Core features 21`
- [ ] `C-CF-165` `ui` The viewer presents a `STEP` file as tessellated geometry. `src: Core features 21`
- [ ] `C-CF-166` `capability` A privacy page is served at `/privacy`. `src: Core features 22`
- [ ] `C-CF-167` `ui` The privacy page is reachable from the footer of every page. `src: Core features 22`
- [ ] `C-CF-168` `ui` The privacy page states what the product stores about an account. `src: Core features 22`
- [ ] `C-CF-169` `ui` The privacy page states the retention period of each plan. `src: Core features 22`
- [ ] `C-CF-170` `ui` The privacy page states that a tool under `/3d-tools` transmits nothing. `src: Core features 22`
- [ ] `C-CF-171` `capability` A terms page is served at `/terms`. `src: Core features 22`
- [ ] `C-CF-172` `capability` A cookie page is served at `/cookie`. `src: Core features 22`
- [ ] `C-CF-173` `ui` The terms page is linked from the registration form. `src: Core features 22`
- [ ] `C-CF-174` `contract` An unknown address receives `404`. `src: Core features 23`
- [ ] `C-CF-175` `ui` An unknown address renders a not-found page carrying the product chrome. `src: Core features 23`
- [ ] `C-CF-176` `ui` The not-found page offers a route back to `/`. `src: Core features 23`
- [ ] `C-CF-177` `ui` The not-found page offers a route back to `/my-assets`. `src: Core features 23`
- [ ] `C-CF-178` `ui` The contact form at `/contact` carries an unattended decoy field. `src: Core features 24`
- [ ] `C-CF-179` `ui` The anonymous generator carries an unattended decoy field. `src: Core features 24`
- [ ] `C-CF-180` `contract` A form submission filling the unattended decoy field receives `429`. `src: Core features 24`
- [ ] `C-CF-181` `literal` A third submission of one form from one subject inside `60` seconds is refused. `src: Core features 24`
- [ ] `C-CF-182` `constraint` A form submission refused for automation writes nothing. `src: Core features 24`
- [ ] `C-CF-183` `ui` A form rejecting invalid input names the failing field inline. `src: Core features 25`
- [ ] `C-CF-184` `ui` A form rejecting invalid input summarises the failures at the top of the form. `src: Core features 25`
- [ ] `C-CF-185` `constraint` A form rejecting invalid input writes nothing. `src: Core features 25`

## C-UF User flow

- [ ] `C-UF-01` `ui` Navigation is a left rail carrying the generator, the gallery, the tools, the library, pricing. `src: User flow`
- [ ] `C-UF-02` `ui` The library work surface is a split detail pane. `src: User flow`
- [ ] `C-UF-03` `ui` Selecting an asset opens the asset beside the list rather than replacing the list. `src: User flow`
- [ ] `C-UF-04` `ui` Generating opens a modal over the current route. `src: User flow`
- [ ] `C-UF-05` `ui` The generating modal confirms the credit cost before submission. `src: User flow`
- [ ] `C-UF-06` `ui` An ordinary confirmation appears as a toast. `src: User flow`
- [ ] `C-UF-07` `ui` A job changing state writes into a live region. `src: User flow`
- [ ] `C-UF-08` `literal` The public routes are `/`, `/gallery`, `/pricing`, `/3d-tools`, `/contact`, `/privacy`, `/terms`, `/cookie`. `src: User flow`
- [ ] `C-UF-09` `literal` The three tool routes are `/3d-tools/online-viewer`, `/3d-tools/file-converter`, `/3d-tools/3d-text-generator`. `src: User flow`
- [ ] `C-UF-10` `literal` The identity routes are `/sign-in`, `/sign-up`. `src: User flow`
- [ ] `C-UF-11` `literal` The session routes are `/my-assets`, `/my-assets/:asset`. `src: User flow`
- [ ] `C-UF-12` `constraint` The route `/my-assets` shows the assets of the signed-in account alone. `src: User flow`
- [ ] `C-UF-13` `constraint` The route `/my-assets/:asset` is reachable by the owning account alone. `src: User flow`
- [ ] `C-UF-14` `ui` Changing the tier from `standard` to `pro` changes the displayed cost from `5` to `10`. `src: User flow`
- [ ] `C-UF-15` `ui` A generator refusal names the balance, the plan tier allowance, or the plan texture allowance as the blocker. `src: User flow`
- [ ] `C-UF-16` `ui` A generator refusal offers the one action that would clear the blocker. `src: User flow`
- [ ] `C-UF-17` `ui` An empty library states what would appear. `src: User flow`
- [ ] `C-UF-18` `ui` An empty library offers the generator. `src: User flow`
- [ ] `C-UF-19` `ui` Each region of the shell skeletons independently. `src: User flow`
- [ ] `C-UF-20` `ui` The left rail never skeletons. `src: User flow`
- [ ] `C-UF-21` `ui` A permission denial names no second account. `src: User flow`
- [ ] `C-UF-22` `ui` Navigating away from an unsaved title warns. `src: User flow`
- [ ] `C-UF-23` `ui` Every error surface shows a request identifier with a copy control. `src: User flow`
- [ ] `C-UF-24` `constraint` A job completing during navigation elsewhere holds the correct state on return. `src: User flow`
- [ ] `C-UF-25` `constraint` Switching locale against a displayed cost changes neither the cost nor the job. `src: User flow`
- [ ] `C-UF-26` `ui` Switching locale against a displayed cost reformats the displayed figure. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface is dark by default. `src: UI/UX notes`
- [ ] `C-UX-02` `constraint` No light theme is built. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The page ground is a near-black neutral. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Every border is a mid grey. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` An announcement banner sits above the header. `src: UI/UX notes`
- [ ] `C-UX-06` `constraint` Only the surface colours actually used are shipped. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` One accent, a bright lime, is carried as a token. `src: UI/UX notes`
- [ ] `C-UX-08` `constraint` The lime accent is spent on the primary action, the live indicator of a running job, a credit balance too low to generate. `src: UI/UX notes`
- [ ] `C-UX-09` `constraint` The lime accent meets the contrast bar against the near-black ground at the interface text size. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The statuses `completed`, `processing`, `failed` each carry an icon, a word, a hue. `src: UI/UX notes`
- [ ] `C-UX-11` `constraint` Status is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` De-emphasis fades toward the mid grey border value. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Type is one sans family at the weights `500`, `600`, `700`. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Body copy is set at `16` over `24`. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Interface text is set at `14` over `20`. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Headings are set at `36` over `40`, `30` over `36`. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Numbers in the library table, the credit ledger, the pricing table are tabular. `src: UI/UX notes`
- [ ] `C-UX-18` `literal` Stacking uses `7` values. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` A slow colour wash sits behind the hero. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Cards float gently. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` A running job carries a pulsing glow. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` A gallery item tilts slightly as the item is approached. `src: UI/UX notes`
- [ ] `C-UX-23` `constraint` Under reduced motion the four continuous animations stop at a resting frame. `src: UI/UX notes`
- [ ] `C-UX-24` `constraint` Under reduced motion every entrance resolves immediately. `src: UI/UX notes`
- [ ] `C-UX-25` `constraint` Under reduced motion the generator progress indication keeps moving. `src: UI/UX notes`
- [ ] `C-UX-26` `constraint` A hover treatment applies only on a device carrying a pointer. `src: UI/UX notes`
- [ ] `C-UX-27` `constraint` Nothing is reachable by hover alone. `src: UI/UX notes`
- [ ] `C-UX-28` `constraint` The operating-system high-contrast mode is handled across the chrome, the library table, the status pills, the generator controls. `src: UI/UX notes`
- [ ] `C-UX-29` `constraint` Body text meets WCAG AA contrast against the ground. `src: UI/UX notes`
- [ ] `C-UX-30` `constraint` Touch targets are comfortably sized. `src: UI/UX notes`
- [ ] `C-UX-31` `constraint` Every interactive element is operable from the keyboard with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-32` `constraint` Every icon-only control carries a label. `src: UI/UX notes`
- [ ] `C-UX-33` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-34` `ui` Each quality tier radio carries the credit cost in the accessible name. `src: UI/UX notes`
- [ ] `C-UX-35` `ui` A job reaching `completed` announces the change. `src: UI/UX notes`
- [ ] `C-UX-36` `ui` A job reaching `failed` announces the change. `src: UI/UX notes`
- [ ] `C-UX-37` `ui` The 3D preview carries a text alternative describing the model. `src: UI/UX notes`
- [ ] `C-UX-38` `ui` The 3D preview orbit is operable from the keyboard. `src: UI/UX notes`
- [ ] `C-UX-39` `ui` The 3D preview zoom is operable from the keyboard. `src: UI/UX notes`
- [ ] `C-UX-40` `constraint` Every content image carries alternative text. `src: UI/UX notes`
- [ ] `C-UX-41` `constraint` Every decorative image declares the decorative role. `src: UI/UX notes`
- [ ] `C-UX-42` `constraint` Every page declares the page language. `src: UI/UX notes`
- [ ] `C-UX-43` `constraint` Prices, dates, numbers are formatted per locale. `src: UI/UX notes`
- [ ] `C-UX-44` `constraint` Text direction is handled rather than assumed. `src: UI/UX notes`
- [ ] `C-UX-45` `constraint` Headings carry line-break guidance for Chinese, Japanese, Korean scripts. `src: UI/UX notes`
- [ ] `C-UX-46` `ui` The page is one landmark structure carrying a banner, a navigation region, a main region, a footer. `src: UI/UX notes`
- [ ] `C-UX-47` `constraint` Headings descend in order without skipping a level. `src: UI/UX notes`
- [ ] `C-UX-48` `ui` A skip control jumps past the chrome. `src: UI/UX notes`
- [ ] `C-UX-49` `constraint` The generator modal traps focus for the open duration. `src: UI/UX notes`
- [ ] `C-UX-50` `constraint` The generator modal returns focus to the opening control on close. `src: UI/UX notes`
- [ ] `C-UX-51` `constraint` The narrow arrangement is the same tree rearranged rather than a second tree. `src: UI/UX notes`
- [ ] `C-UX-52` `literal` Five widths are used symmetrically as both minimum, maximum. `src: UI/UX notes`
- [ ] `C-UX-53` `ui` At a narrow viewport the rail collapses to icons carrying tooltips. `src: UI/UX notes`
- [ ] `C-UX-54` `ui` At a narrow viewport the asset detail pane becomes a full-height sheet. `src: UI/UX notes`
- [ ] `C-UX-55` `ui` At a narrow viewport a table scrolls inside the table container. `src: UI/UX notes`
- [ ] `C-UX-56` `constraint` Nothing overflows sideways at any width. `src: UI/UX notes`
- [ ] `C-UX-57` `constraint` Every navigation target stays reachable in portrait, landscape. `src: UI/UX notes`
- [ ] `C-UX-58` `constraint` The layout holds at a short viewport. `src: UI/UX notes`
- [ ] `C-UX-59` `ui` Each page leads with one primary action visually distinct from every secondary action. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The client is built with Preact, Vite. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The HTTP API is served by Fastify under the `/api` prefix on the app origin. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The datastore is PostgreSQL. `src: Technical requirements`
- [ ] `C-TR-04` `literal` The datastore connection string is read from `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `literal` The value of `DB_URL` equals the value of `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-06` `literal` The object store endpoint is read from `STORAGE_ENDPOINT`. `src: Technical requirements`
- [ ] `C-TR-07` `literal` The object store credentials are read from `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements`
- [ ] `C-TR-08` `literal` The object store bucket name is read from `STORAGE_BUCKET`. `src: Technical requirements`
- [ ] `C-TR-09` `contract` The object store is MinIO. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No backing service outside PostgreSQL, MinIO is installed. `src: Technical requirements`
- [ ] `C-TR-11` `data` The uploaded source image is stored in MinIO. `src: Technical requirements`
- [ ] `C-TR-12` `data` The `glb`, `obj`, `stl`, texture maps, preview image are stored in MinIO. `src: Technical requirements`
- [ ] `C-TR-13` `constraint` The MinIO bucket is not publicly readable. `src: Technical requirements`
- [ ] `C-TR-14` `contract` Every stored object is served through an application path establishing the caller identity. `src: Technical requirements`
- [ ] `C-TR-15` `constraint` A stored object belonging to one account is never returned to a second account. `src: Technical requirements`
- [ ] `C-TR-16` `constraint` A submitted job reaches a terminal state without any external service being contacted. `src: Technical requirements`
- [ ] `C-TR-17` `constraint` A job is observably running at the instant of submission rather than already complete. `src: Technical requirements`
- [ ] `C-TR-18` `literal` The seconds a conversion occupies are read from `GENERATION_SECONDS`. `src: Technical requirements`
- [ ] `C-TR-19` `contract` Session is email, password exchanged for a bearer token. `src: Technical requirements`
- [ ] `C-TR-20` `constraint` A stored password cannot be reversed to the original value. `src: Technical requirements`
- [ ] `C-TR-21` `constraint` No response body carries a password, a bucket credential, a datastore credential. `src: Technical requirements`
- [ ] `C-TR-22` `constraint` Nothing the browser downloads carries a credential. `src: Technical requirements`
- [ ] `C-TR-23` `constraint` Credit accounting is serialisable with respect to one account balance. `src: Technical requirements`
- [ ] `C-TR-24` `constraint` A reservation is recorded rather than overwritten. `src: Technical requirements`
- [ ] `C-TR-25` `constraint` A settlement is recorded rather than overwritten. `src: Technical requirements`
- [ ] `C-TR-26` `contract` Every response carries a request identifier. `src: Technical requirements`
- [ ] `C-TR-27` `constraint` Every public route carries an individual title. `src: Technical requirements`
- [ ] `C-TR-28` `constraint` Every public route carries an individual description. `src: Technical requirements`
- [ ] `C-TR-29` `constraint` No two public routes share a title. `src: Technical requirements`
- [ ] `C-TR-30` `constraint` Every public route declares a social preview title, a preview image. `src: Technical requirements`
- [ ] `C-TR-31` `constraint` A declared social preview image resolves. `src: Technical requirements`
- [ ] `C-TR-32` `constraint` Times are stored, compared in UTC. `src: Technical requirements`
- [ ] `C-TR-33` `literal` Money is stored in integer minor units in `usd`. `src: Technical requirements`
- [ ] `C-TR-34` `constraint` Font faces are subsetted per locale. `src: Technical requirements`
- [ ] `C-TR-35` `constraint` No route ships a rotating model as a sequence of still images. `src: Technical requirements`
- [ ] `C-TR-36` `constraint` No page requests a stock portrait of a person. `src: Technical requirements`
- [ ] `C-TR-37` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-38` `contract` `POST /api/auth/sign-up` registers an account. `src: Technical requirements`
- [ ] `C-TR-39` `contract` `POST /api/auth/login` exchanges an email, a password for an access token. `src: Technical requirements`
- [ ] `C-TR-40` `contract` `GET /api/session` returns the current account, the plan, the balance. `src: Technical requirements`
- [ ] `C-TR-41` `contract` `GET /api/tiers` returns the stored tier table. `src: Technical requirements`
- [ ] `C-TR-42` `contract` `GET /api/plans` returns the three plans, the active promotion. `src: Technical requirements`
- [ ] `C-TR-43` `contract` `POST /api/jobs` submits a generation carrying an idempotency key. `src: Technical requirements`
- [ ] `C-TR-44` `contract` `GET /api/jobs/{id}` returns one job, the job state. `src: Technical requirements`
- [ ] `C-TR-45` `contract` `GET /api/assets` returns the caller library filtered by status, tag, favourite, archived. `src: Technical requirements`
- [ ] `C-TR-46` `contract` `GET /api/assets/{id}` returns one asset owned by the caller. `src: Technical requirements`
- [ ] `C-TR-47` `contract` `PATCH /api/assets/{id}` updates title, description, favourite, archived. `src: Technical requirements`
- [ ] `C-TR-48` `contract` `POST /api/assets/{id}/tags` adds a tag. `src: Technical requirements`
- [ ] `C-TR-49` `contract` `GET /api/assets/{id}/download/{kind}` returns one representation to the owning account. `src: Technical requirements`
- [ ] `C-TR-50` `contract` `GET /api/credits` returns the caller ledger. `src: Technical requirements`
- [ ] `C-TR-51` `contract` `POST /api/claims` exchanges an anonymous claim token for ownership. `src: Technical requirements`
- [ ] `C-TR-52` `contract` `GET /api/samples` returns the four pre-computed samples. `src: Technical requirements`
- [ ] `C-TR-53` `contract` `GET /api/gallery` returns the published gallery items with sources, tiers. `src: Technical requirements`
- [ ] `C-TR-54` `contract` `GET /api/claims/published` returns the stored published figures. `src: Technical requirements`
- [ ] `C-TR-55` `contract` `POST /api/contact` accepts the contact form. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` An `account` row carries email, display name, plan, status, subscription anniversary, created at. `src: Data model`
- [ ] `C-DM-02` `literal` An `account` status is `active` or `deactivated`. `src: Data model`
- [ ] `C-DM-03` `data` A `plan` row carries key, list price, promotional price, promotion start, promotion end, monthly credits, welcome credits, polygon ceiling, allowed tiers, textures allowed, multiple images allowed, queue placement, retention days, licence, rollover. `src: Data model`
- [ ] `C-DM-04` `data` A `quality_tier` row carries key, octree resolution, inference steps, polygon ceiling, credit cost. `src: Data model`
- [ ] `C-DM-05` `data` A `credit_ledger` row carries account, kind, amount, balance after, job, period start, occurred at. `src: Data model`
- [ ] `C-DM-06` `literal` A `credit_ledger` kind is one of `welcome`, `monthly`, `reservation`, `settlement`, `refund`. `src: Data model`
- [ ] `C-DM-07` `data` A `job` row carries owner, source mode, input mode, tier, textures, source object key, recorded octree resolution, recorded inference steps, cost shown, cost charged, queue placement, state, idempotency key, attempt count, error reason, timestamps, row version. `src: Data model`
- [ ] `C-DM-08` `data` An `asset` row carries job, owner, title, description, licence, plan at creation, tier at creation, polygon count, favourite, archived, deletion date, created at. `src: Data model`
- [ ] `C-DM-09` `data` An `asset_representation` row carries asset, kind, object key, byte size. `src: Data model`
- [ ] `C-DM-10` `data` An `asset_tag` row carries asset, tag. `src: Data model`
- [ ] `C-DM-11` `data` A `download_event` row carries asset, account, representation kind, occurred at. `src: Data model`
- [ ] `C-DM-12` `data` An `anonymous_allowance` row carries subject hash, attempts used, first seen at, claim token, claim expires at. `src: Data model`
- [ ] `C-DM-13` `data` A `sample` row carries key, title, source object key, pre-computed asset, tier. `src: Data model`
- [ ] `C-DM-14` `data` A `gallery_item` row carries title, source object key, asset, tier, published. `src: Data model`
- [ ] `C-DM-15` `data` A `published_claim` row carries key, value, unit, basis, measured on. `src: Data model`
- [ ] `C-DM-16` `data` A `conversion_pair` row carries source format, target format, supported. `src: Data model`
- [ ] `C-DM-17` `data` A `contact_message` row carries name, email, body, occurred at. `src: Data model`
- [ ] `C-DM-18` `constraint` Every owned row carries exactly one of an account or an anonymous claim token. `src: Data model`
- [ ] `C-DM-19` `constraint` A read answering for one account never returns a row belonging to a second account. `src: Data model`
- [ ] `C-DM-20` `constraint` A `job` idempotency key is unique per owner. `src: Data model`
- [ ] `C-DM-21` `constraint` A `job` row version changes on every transition. `src: Data model`
- [ ] `C-DM-22` `constraint` Two state changes arriving together on one job produce one transition. `src: Data model`
- [ ] `C-DM-23` `constraint` A `credit_ledger` row is inserted, never updated. `src: Data model`
- [ ] `C-DM-24` `constraint` A `credit_ledger` row is never deleted. `src: Data model`
- [ ] `C-DM-25` `constraint` A `download_event` row is inserted, never updated. `src: Data model`
- [ ] `C-DM-26` `constraint` An account balance equals the sum of the account ledger amounts. `src: Data model`
- [ ] `C-DM-27` `constraint` A `job` reaching `failed` carries a refund equal to the reservation. `src: Data model`
- [ ] `C-DM-28` `constraint` The value `cost_charged` equals the value `cost_shown` on every settled job. `src: Data model`
- [ ] `C-DM-29` `constraint` No `credit_ledger` row leaves a balance below zero. `src: Data model`
- [ ] `C-DM-30` `constraint` The field `asset.licence` is written once at creation. `src: Data model`
- [ ] `C-DM-31` `constraint` The field `asset.plan_at_creation` is written once at creation. `src: Data model`
- [ ] `C-DM-32` `constraint` The field `asset.deletion_date` is written once at creation. `src: Data model`
- [ ] `C-DM-33` `constraint` A later plan change does not move `asset.deletion_date`. `src: Data model`
- [ ] `C-DM-34` `constraint` The field `asset.archived` does not affect `asset.deletion_date`. `src: Data model`
- [ ] `C-DM-35` `constraint` The field `job.queue_priority` is written at submission from the plan held then. `src: Data model`
- [ ] `C-DM-36` `constraint` A `monthly` ledger row is unique per account per period start. `src: Data model`
- [ ] `C-DM-37` `constraint` The value `anonymous_allowance.attempts_used` never exceeds `1`. `src: Data model`
- [ ] `C-DM-38` `constraint` A `sample` resolves to a stored pre-computed asset. `src: Data model`
- [ ] `C-DM-39` `constraint` A `published_claim` key is unique. `src: Data model`
- [ ] `C-DM-40` `constraint` A tier recorded on a job is one of the four stored tier keys. `src: Data model`
- [ ] `C-DM-41` `literal` The seeded accounts are `creator@example.com`, `creator2@example.com`, `creator3@example.com`. `src: Data model`
- [ ] `C-DM-42` `literal` The seeded account password is `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-43` `constraint` Seeding is idempotent, so running the seed twice leaves the same rows. `src: Data model`
- [ ] `C-DM-44` `literal` The seeded samples `sneaker`, `mug`, `chair`, `plant` each carry a pre-computed asset. `src: Data model`
- [ ] `C-DM-45` `literal` The seeded published figures carry the measurement date `2026-09-01`. `src: Data model`
- [ ] `C-DM-46` `literal` The account `creator@example.com` holds the plan `pro` with balance `1000`. `src: Data model`
- [ ] `C-DM-47` `literal` The account `creator2@example.com` holds the plan `free` with balance `15`. `src: Data model`
- [ ] `C-DM-48` `literal` The account `creator3@example.com` holds the plan `free` with balance `5`. `src: Data model`
- [ ] `C-DM-49` `literal` The account `creator@example.com` owns `Harbour Crane`, `Ceramic Teapot`, `Rope Coil`, `Broken Statue`. `src: Data model`
- [ ] `C-DM-50` `literal` The account `creator2@example.com` owns `Paper Lantern`. `src: Data model`
- [ ] `C-DM-51` `data` The asset `Ceramic Teapot` is archived. `src: Data model`
- [ ] `C-DM-52` `data` The asset `Harbour Crane` is favourited. `src: Data model`
- [ ] `C-DM-53` `data` The asset `Paper Lantern` carries the licence `CC-BY-4.0`. `src: Data model`
- [ ] `C-DM-54` `literal` The stored roles are `creator`, `visitor`. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The shell carries a left rail, a header, a main region. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The left rail collapses to icons at a narrow width. `src: Front-end specification`
- [ ] `C-FE-03` `ui` The generator sits on the route `/`. `src: Front-end specification`
- [ ] `C-FE-04` `ui` The generator controls sit together as source mode, input mode, tier radio group, texture toggle, generate control. `src: Front-end specification`
- [ ] `C-FE-05` `ui` Each tier radio carries an individual credit cost. `src: Front-end specification`
- [ ] `C-FE-06` `ui` The upload target sits above the generator controls. `src: Front-end specification`
- [ ] `C-FE-07` `ui` The four samples appear to a caller holding no session. `src: Front-end specification`
- [ ] `C-FE-08` `ui` The generate control opens a modal naming the cost, the tier, the licence, the polygon ceiling. `src: Front-end specification`
- [ ] `C-FE-09` `constraint` A job is submitted only from the confirmation modal. `src: Front-end specification`
- [ ] `C-FE-10` `ui` A running job appears as a card carrying state, stage, tier, reserved cost. `src: Front-end specification`
- [ ] `C-FE-11` `constraint` A running job card is rendered from the server copy of the state. `src: Front-end specification`
- [ ] `C-FE-12` `constraint` The poller slows during a hidden document state. `src: Front-end specification`
- [ ] `C-FE-13` `constraint` The poller stops when no job is running. `src: Front-end specification`
- [ ] `C-FE-14` `ui` The library renders a list on the left, a detail pane on the right. `src: Front-end specification`
- [ ] `C-FE-15` `ui` A library row shows preview, title, tier, licence, status, deletion date. `src: Front-end specification`
- [ ] `C-FE-16` `ui` The detail pane carries editable title, editable description, a tag editor, favourite, archive, three download formats, download history. `src: Front-end specification`
- [ ] `C-FE-17` `ui` The viewer degrades to the preview image when a mesh cannot be held. `src: Front-end specification`
- [ ] `C-FE-18` `ui` Each of the three tool routes carries a drop target, a file input, a result area, a statement of support. `src: Front-end specification`
- [ ] `C-FE-19` `ui` The converter route renders the pair matrix alongside the supported pair count. `src: Front-end specification`
- [ ] `C-FE-20` `ui` A refusal renders where the action was taken. `src: Front-end specification`
- [ ] `C-FE-21` `constraint` A refused form keeps the entered values. `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No translated route tree is built for the twelve languages. `src: Constraints`
- [ ] `C-CN-02` `constraint` No blog route is built. `src: Constraints`
- [ ] `C-CN-03` `constraint` No changelog route is built. `src: Constraints`
- [ ] `C-CN-04` `constraint` No documentation route is built. `src: Constraints`
- [ ] `C-CN-05` `constraint` No unlaunched text, image, audio, video surface is built. `src: Constraints`
- [ ] `C-CN-06` `constraint` No waiting-list route is built. `src: Constraints`
- [ ] `C-CN-07` `constraint` No hosted payment provider is integrated. `src: Constraints`
- [ ] `C-CN-08` `constraint` No component-library scaffolding route is deployed. `src: Constraints`
- [ ] `C-CN-09` `capability` A plan is changed directly against the account with no payment taken. `src: Constraints`
- [ ] `C-CN-10` `constraint` No testimonial illustrated with a placeholder-avatar portrait appears. `src: Constraints`
- [ ] `C-CN-11` `constraint` No gallery item uses a recognisable character from a published work as the source image. `src: Constraints`
- [ ] `C-CN-12` `constraint` A value outside a closed vocabulary is refused rather than stored. `src: Constraints`

## C-BP Build plan

- [ ] `C-BP-01` `capability` The schema, the seed, the MinIO buckets, `GET /api/health` are built first. `src: Build plan`
- [ ] `C-BP-02` `capability` Registration, sign-in, bearer sessions are built over the seeded accounts. `src: Build plan`
- [ ] `C-BP-03` `capability` The stored tier table, the plan table are built with the endpoints reading them. `src: Build plan`
- [ ] `C-BP-04` `capability` The generator controls, the cost calculation, the confirmation modal are built together. `src: Build plan`
- [ ] `C-BP-05` `capability` Job submission, the reservation, the worker advancing a job, the object writes are built together. `src: Build plan`
- [ ] `C-BP-06` `capability` The credit ledger, the append-only history, the contended submission path are built together. `src: Build plan`
- [ ] `C-BP-07` `capability` Failure, refund, submission-key idempotency are built together. `src: Build plan`
- [ ] `C-BP-08` `capability` The library filters, favourite, archive, title, description, tags, downloads, download history are built together. `src: Build plan`
- [ ] `C-BP-09` `capability` The ownership check on every asset read, every object read is built. `src: Build plan`
- [ ] `C-BP-10` `capability` Licence stamping, retention stamping, the downgrade rule, the archive licence file are built together. `src: Build plan`
- [ ] `C-BP-11` `capability` Anonymous generation, the bounded allowance, the pre-computed samples, the claim path are built together. `src: Build plan`
- [ ] `C-BP-12` `capability` The three local tools, the conversion matrix, the matrix count are built together. `src: Build plan`
- [ ] `C-BP-13` `capability` The gallery, the stored published figures, the comparison table, the statistics band are built together. `src: Build plan`
- [ ] `C-BP-14` `capability` The public pages, the not-found page, the per-route metadata, the automated-submission refusal are built together. `src: Build plan`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `literal` The container-internal port is `4173`. `src: Deployment contract`
- [ ] `C-DC-04` `constraint` The port values are read from the environment rather than hardcoded. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The HTTP API is served on the app origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-06` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-07` `constraint` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-08` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-09` `constraint` The directory `.browser_screenshots/` exists at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-10` `constraint` The directory `.downloads/` exists at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No dev server serves the app. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-14` `constraint` The server is not a child of the shell. `src: Deployment contract`
- [ ] `C-DC-15` `constraint` The server binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-16` `constraint` The server never binds `127.0.0.1` or `localhost`. `src: Deployment contract`
- [ ] `C-DC-17` `constraint` No copy of a named backing service is downloaded, installed, compiled, or started. `src: Deployment contract`
- [ ] `C-DC-18` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-19` `constraint` No persistent volume is declared. `src: Deployment contract`
- [ ] `C-DC-20` `constraint` No fixed container name is declared. `src: Deployment contract`
- [ ] `C-DC-21` `constraint` No custom network is declared. `src: Deployment contract`

## Pinned literals

| Value | Section | Item |
|---|---|---|
| `fast` | Core features | `C-CF-07` |
| `standard` | Core features | `C-CF-07` |
| `pro` | Core features | `C-CF-07` |
| `ultra` | Core features | `C-CF-07` |
| `fast` | Core features | `C-CF-08` |
| `196` | Core features | `C-CF-08` |
| `20` | Core features | `C-CF-08` |
| `15000` | Core features | `C-CF-08` |
| `2` | Core features | `C-CF-08` |
| `standard` | Core features | `C-CF-09` |
| `256` | Core features | `C-CF-09` |
| `30` | Core features | `C-CF-09` |
| `30000` | Core features | `C-CF-09` |
| `5` | Core features | `C-CF-09` |
| `pro` | Core features | `C-CF-10` |
| `384` | Core features | `C-CF-10` |
| `40` | Core features | `C-CF-10` |
| `60000` | Core features | `C-CF-10` |
| `10` | Core features | `C-CF-10` |
| `ultra` | Core features | `C-CF-11` |
| `512` | Core features | `C-CF-11` |
| `50` | Core features | `C-CF-11` |
| `300000` | Core features | `C-CF-11` |
| `20` | Core features | `C-CF-11` |
| `300000` | Core features | `C-CF-14` |
| `image-to-3d` | Core features | `C-CF-18` |
| `text-to-3d` | Core features | `C-CF-18` |
| `single-image` | Core features | `C-CF-19` |
| `multiple-images` | Core features | `C-CF-19` |
| `5` | Core features | `C-CF-25` |
| `10` | Core features | `C-CF-26` |
| `multiple-images` | Core features | `C-CF-26` |
| `10` | Core features | `C-CF-27` |
| `CC-BY-4.0` | Core features | `C-CF-32` |
| `CC-BY-4.0` | Core features | `C-CF-33` |
| `customer-owned` | Core features | `C-CF-34` |
| `JPG` | Core features | `C-CF-38` |
| `PNG` | Core features | `C-CF-38` |
| `WEBP` | Core features | `C-CF-38` |
| `queued` | Core features | `C-CF-41` |
| `processing` | Core features | `C-CF-41` |
| `completed` | Core features | `C-CF-41` |
| `failed` | Core features | `C-CF-41` |
| `limited` | Core features | `C-CF-59` |
| `standard` | Core features | `C-CF-59` |
| `higher` | Core features | `C-CF-59` |
| `glb` | Core features | `C-CF-64` |
| `obj` | Core features | `C-CF-64` |
| `stl` | Core features | `C-CF-64` |
| `texture-map` | Core features | `C-CF-64` |
| `preview` | Core features | `C-CF-64` |
| `7` | Core features | `C-CF-74` |
| `pro` | Core features | `C-CF-75` |
| `180` | Core features | `C-CF-75` |
| `max` | Core features | `C-CF-76` |
| `1` | Core features | `C-CF-94` |
| `sneaker` | Core features | `C-CF-96` |
| `mug` | Core features | `C-CF-96` |
| `chair` | Core features | `C-CF-96` |
| `plant` | Core features | `C-CF-96` |
| `24` | Core features | `C-CF-102` |
| `10` | Core features | `C-CF-106` |
| `5` | Core features | `C-CF-107` |
| `free` | Core features | `C-CF-116` |
| `pro` | Core features | `C-CF-116` |
| `max` | Core features | `C-CF-116` |
| `free` | Core features | `C-CF-117` |
| `$0` | Core features | `C-CF-117` |
| `pro` | Core features | `C-CF-118` |
| `$15.00` | Core features | `C-CF-118` |
| `$9.90` | Core features | `C-CF-118` |
| `max` | Core features | `C-CF-119` |
| `$39.00` | Core features | `C-CF-119` |
| `$19.90` | Core features | `C-CF-119` |
| `pro` | Core features | `C-CF-120` |
| `-34% OFF` | Core features | `C-CF-120` |
| `max` | Core features | `C-CF-121` |
| `-50% OFF` | Core features | `C-CF-121` |
| `Most Popular` | Core features | `C-CF-121` |
| `pro` | Core features | `C-CF-122` |
| `1000` | Core features | `C-CF-122` |
| `max` | Core features | `C-CF-123` |
| `4000` | Core features | `C-CF-123` |
| `free` | Core features | `C-CF-126` |
| `60000` | Core features | `C-CF-126` |
| `pro` | Core features | `C-CF-127` |
| `300000` | Core features | `C-CF-127` |
| `2026-09-01` | Core features | `C-CF-134` |
| `2026-12-31` | Core features | `C-CF-134` |
| `Brass Compass` | Core features | `C-CF-140` |
| `pro` | Core features | `C-CF-140` |
| `Woven Basket` | Core features | `C-CF-140` |
| `standard` | Core features | `C-CF-140` |
| `Carved Owl` | Core features | `C-CF-140` |
| `ultra` | Core features | `C-CF-140` |
| `Tin Robot` | Core features | `C-CF-140` |
| `fast` | Core features | `C-CF-140` |
| `models_created` | Core features | `C-CF-142` |
| `25000` | Core features | `C-CF-142` |
| `2026-09-01` | Core features | `C-CF-142` |
| `average_rating` | Core features | `C-CF-143` |
| `4.9` | Core features | `C-CF-143` |
| `5` | Core features | `C-CF-143` |
| `2026-09-01` | Core features | `C-CF-143` |
| `success_rate` | Core features | `C-CF-144` |
| `99.0` | Core features | `C-CF-144` |
| `2026-09-01` | Core features | `C-CF-144` |
| `countries_served` | Core features | `C-CF-145` |
| `80` | Core features | `C-CF-145` |
| `2026-09-01` | Core features | `C-CF-145` |
| `average_cost_usd` | Core features | `C-CF-146` |
| `$0.50` | Core features | `C-CF-146` |
| `2026-09-01` | Core features | `C-CF-146` |
| `conversion_minutes` | Core features | `C-CF-147` |
| `2` | Core features | `C-CF-147` |
| `3` | Core features | `C-CF-147` |
| `2026-09-01` | Core features | `C-CF-147` |
| `GLB` | Core features | `C-CF-156` |
| `OBJ` | Core features | `C-CF-156` |
| `STL` | Core features | `C-CF-156` |
| `FBX` | Core features | `C-CF-156` |
| `STEP` | Core features | `C-CF-156` |
| `128` | Core features | `C-CF-158` |
| `60` | Core features | `C-CF-181` |
| `/` | User flow | `C-UF-08` |
| `/gallery` | User flow | `C-UF-08` |
| `/pricing` | User flow | `C-UF-08` |
| `/3d-tools` | User flow | `C-UF-08` |
| `/contact` | User flow | `C-UF-08` |
| `/privacy` | User flow | `C-UF-08` |
| `/terms` | User flow | `C-UF-08` |
| `/cookie` | User flow | `C-UF-08` |
| `/3d-tools/online-viewer` | User flow | `C-UF-09` |
| `/3d-tools/file-converter` | User flow | `C-UF-09` |
| `/3d-tools/3d-text-generator` | User flow | `C-UF-09` |
| `/sign-in` | User flow | `C-UF-10` |
| `/sign-up` | User flow | `C-UF-10` |
| `/my-assets` | User flow | `C-UF-11` |
| `/my-assets/:asset` | User flow | `C-UF-11` |
| `7` | UI and UX notes | `C-UX-18` |
| `DATABASE_URL` | Technical requirements | `C-TR-04` |
| `DB_URL` | Technical requirements | `C-TR-05` |
| `DATABASE_URL` | Technical requirements | `C-TR-05` |
| `STORAGE_ENDPOINT` | Technical requirements | `C-TR-06` |
| `STORAGE_ACCESS_KEY` | Technical requirements | `C-TR-07` |
| `STORAGE_SECRET_KEY` | Technical requirements | `C-TR-07` |
| `STORAGE_BUCKET` | Technical requirements | `C-TR-08` |
| `GENERATION_SECONDS` | Technical requirements | `C-TR-18` |
| `usd` | Technical requirements | `C-TR-33` |
| `account` | Data model | `C-DM-02` |
| `active` | Data model | `C-DM-02` |
| `deactivated` | Data model | `C-DM-02` |
| `credit_ledger` | Data model | `C-DM-06` |
| `welcome` | Data model | `C-DM-06` |
| `monthly` | Data model | `C-DM-06` |
| `reservation` | Data model | `C-DM-06` |
| `settlement` | Data model | `C-DM-06` |
| `refund` | Data model | `C-DM-06` |
| `creator@example.com` | Data model | `C-DM-41` |
| `creator2@example.com` | Data model | `C-DM-41` |
| `creator3@example.com` | Data model | `C-DM-41` |
| `deku-demo-pw-2026` | Data model | `C-DM-42` |
| `sneaker` | Data model | `C-DM-44` |
| `mug` | Data model | `C-DM-44` |
| `chair` | Data model | `C-DM-44` |
| `plant` | Data model | `C-DM-44` |
| `2026-09-01` | Data model | `C-DM-45` |
| `creator@example.com` | Data model | `C-DM-46` |
| `pro` | Data model | `C-DM-46` |
| `1000` | Data model | `C-DM-46` |
| `creator2@example.com` | Data model | `C-DM-47` |
| `free` | Data model | `C-DM-47` |
| `15` | Data model | `C-DM-47` |
| `creator3@example.com` | Data model | `C-DM-48` |
| `free` | Data model | `C-DM-48` |
| `5` | Data model | `C-DM-48` |
| `creator@example.com` | Data model | `C-DM-49` |
| `Harbour Crane` | Data model | `C-DM-49` |
| `Ceramic Teapot` | Data model | `C-DM-49` |
| `Rope Coil` | Data model | `C-DM-49` |
| `Broken Statue` | Data model | `C-DM-49` |
| `creator2@example.com` | Data model | `C-DM-50` |
| `Paper Lantern` | Data model | `C-DM-50` |
| `creator` | Data model | `C-DM-54` |
| `visitor` | Data model | `C-DM-54` |
| `4173` | Deployment contract | `C-DC-03` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the retry interval a client poller uses between reads of a running job | `C-CF-45` |
| the byte ceiling accepted for one uploaded source image | `C-CF-39` |
| the number of assets one account may hold | `C-CF-86` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 6 | 16 |
| User roles | 5 | 18 |
| Core features | 25 | 185 |
| User flow | 6 | 26 |
| UI and UX notes | 11 | 59 |
| Technical requirements | 9 | 55 |
| Data model | 5 | 54 |
| Front-end specification | 7 | 21 |
| Constraints | 3 | 12 |
| Build plan | 14 | 14 |
| Deployment contract | 13 | 21 |
