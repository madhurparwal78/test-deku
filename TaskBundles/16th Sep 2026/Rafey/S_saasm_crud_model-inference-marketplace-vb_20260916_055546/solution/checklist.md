# Checklist: Modelport

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, deployment
Sections absent: buildplan
Items: 409
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public catalogue of models addressed as `owner/name`. `src: Overview, Overview para 2`
- [ ] `C-OV-02` `capability` The app gives a signed in developer a console holding tokens, run history, spend controls, deployments, invoices. `src: Overview, Overview para 2`
- [ ] `C-OV-03` `capability` The catalogue is browsable without an account. `src: Overview, Overview para 2`
- [ ] `C-OV-04` `capability` The app draws down a prepaid free allowance before charged usage accrues. `src: Overview, Overview para 4`
- [ ] `C-OV-05` `constraint` A per-account spend cap stops new work rather than sending a warning. `src: Overview, Overview para 4`
- [ ] `C-OV-06` `constraint` The app holds no comments, likes, follows, direct messages, forum. `src: Overview, Overview para 5`
- [ ] `C-OV-07` `constraint` The app holds no fine tuning. `src: Overview, Overview para 5`
- [ ] `C-OV-08` `constraint` Every model in the catalogue returns text or a structured object. `src: Overview, Overview para 5`
- [ ] `C-OV-09` `constraint` A prediction is billed at most once. `src: Overview, Overview para 6`

## C-RL User roles

- [ ] `C-RL-01` `role` A `member` browses the catalogue signed out. `src: User roles, User roles table row 1`
- [ ] `C-RL-02` `role` A `member` runs a private model owned by an account holding that member. `src: User roles, User roles table row 1`
- [ ] `C-RL-03` `role` A `member` publishes models under their own handle. `src: User roles, User roles table row 1`
- [ ] `C-RL-04` `role` A `member` creates their own deployments. `src: User roles, User roles table row 1`
- [ ] `C-RL-05` `role` A `member` is denied another account's predictions, usage rows, invoices, tokens, private models. `src: User roles, User roles table row 1`
- [ ] `C-RL-06` `role` A `member` is denied adding a member to an organisation. `src: User roles, User roles table row 1`
- [ ] `C-RL-07` `role` A `member` is denied changing another member's role. `src: User roles, User roles table row 1`
- [ ] `C-RL-08` `role` An `owner` changes a member's role in the organisation under their ownership. `src: User roles, User roles table row 2`
- [ ] `C-RL-09` `role` An `owner` changes the visibility of a model the organisation owns. `src: User roles, User roles table row 2`
- [ ] `C-RL-10` `role` An `owner` is denied a personal account's predictions, tokens. `src: User roles, User roles table row 2`
- [ ] `C-RL-11` `role` The server enforces authorization on every mutating endpoint. `src: User roles, authorization para`
- [ ] `C-RL-12` `role` A denied call leaves the protected state unchanged. `src: User roles, authorization para`
- [ ] `C-RL-13` `capability` Signup is open, so anyone creates an account from `/signup`. `src: User roles, signup para`
- [ ] `C-RL-14` `capability` An account created from `/signup` is usable at once. `src: User roles, signup para`
- [ ] `C-RL-15` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles, seeded accounts para`
- [ ] `C-RL-16` `literal` The account `owner@example.com` is an `owner` of the organisation `northlight`. `src: User roles, User roles seed table row 1`
- [ ] `C-RL-17` `literal` The account `member@example.com` is a `member` of the organisation `northlight`. `src: User roles, User roles seed table row 2`
- [ ] `C-RL-18` `literal` The account `member2@example.com` belongs to no organisation. `src: User roles, User roles seed table row 3`
- [ ] `C-RL-19` `constraint` An organisation account never signs in. `src: User roles, organisation para`
- [ ] `C-RL-20` `data` A personal account shares one handle namespace with an organisation account. `src: User roles, organisation para`

## C-CF Core features

- [ ] `C-CF-01` `capability` An account is created from `/signup` with an email address, a password, a handle. `src: Core features, Core features rule 1`
- [ ] `C-CF-02` `constraint` A password is stored hashed, never in clear text. `src: Core features, Core features rule 1`
- [ ] `C-CF-03` `literal` The literal `deku-demo-pw-2026` works at login for every seeded account. `src: Core features, Core features rule 1`
- [ ] `C-CF-04` `constraint` Deleting the session cookie alone is not a sign out. `src: Core features, Core features rule 2`
- [ ] `C-CF-05` `contract` The machine interface authenticates with a bearer credential in the `Authorization` header. `src: Core features, Core features rule 3`
- [ ] `C-CF-06` `constraint` A handle with a leading hyphen is refused. `src: Core features, Core features rule 4`
- [ ] `C-CF-07` `constraint` A handle with a trailing hyphen is refused. `src: Core features, Core features rule 4`
- [ ] `C-CF-08` `literal` The reserved handle list holds `playground`, `account`, `settings`, `dashboard`, `predictions`, `trainings`. `src: Core features, Core features rule 5`
- [ ] `C-CF-09` `constraint` The reserved handle list is consulted before any other handle validation. `src: Core features, Core features rule 5`
- [ ] `C-CF-10` `capability` The router resolves a leading path segment against account handles second. `src: Core features, Core features rule 5`
- [ ] `C-CF-11` `capability` The router answers not found when a leading path segment matches neither. `src: Core features, Core features rule 5`
- [ ] `C-CF-12` `ui` `/explore` opens with the title `Explore`. `src: Core features, Core features rule 7`
- [ ] `C-CF-13` `contract` A model is addressed `/<owner>/<model>`. `src: Core features, Core features rule 8`
- [ ] `C-CF-14` `ui` An owner with no public models renders the header with one honest line. `src: Core features, Core features rule 8`
- [ ] `C-CF-15` `ui` A model card shows a description, a run count, a badge row. `src: Core features, Core features rule 9`
- [ ] `C-CF-16` `capability` A run count below `1000` renders as the unabbreviated integer. `src: Core features, Core features rule 11`
- [ ] `C-CF-17` `literal` The seeded run counts render as `17.9M`, `469.7K`, `4M`, `17`. `src: Core features, Core features rule 11`
- [ ] `C-CF-18` `capability` The popular column orders by a stored ranking number. `src: Core features, Core features rule 12`
- [ ] `C-CF-19` `capability` A model card prints the lifetime run count rather than the ranking number. `src: Core features, Core features rule 12`
- [ ] `C-CF-20` `constraint` The ranking number is never printed. `src: Core features, Core features rule 12`
- [ ] `C-CF-21` `data` A collection holds a slug, a title, a one line description, an ordered model list. `src: Core features, Core features rule 13`
- [ ] `C-CF-22` `capability` The remainder count equals the collection's size minus three. `src: Core features, Core features rule 13`
- [ ] `C-CF-23` `literal` The collection `summarise-text` holds `northlight/scribe-2`, `blackpine-labs/prism-2-flex`. `src: Core features, Core features rule 14`
- [ ] `C-CF-24` `literal` `northlight/scribe-2` is seeded `official`. `src: Core features, Core features rule 15`
- [ ] `C-CF-25` `ui` The `Cold` badge prints that version's declared load time in seconds. `src: Core features, Core features rule 16`
- [ ] `C-CF-26` `contract` `/search` renders the same search as the header combobox. `src: Core features, Core features rule 17`
- [ ] `C-CF-27` `constraint` The search shortcut does nothing with focus inside a text field. `src: Core features, Core features rule 17`
- [ ] `C-CF-28` `capability` Search matches a model on its address, name, description. `src: Core features, Core features rule 18`
- [ ] `C-CF-29` `capability` Search matches an owner on its handle, display name. `src: Core features, Core features rule 18`
- [ ] `C-CF-30` `capability` Search results are grouped by kind. `src: Core features, Core features rule 18`
- [ ] `C-CF-31` `ui` The model page header shows the owner avatar first. `src: Core features, Core features rule 21`
- [ ] `C-CF-32` `ui` A visually hidden heading on the model page carries the full model address. `src: Core features, Core features rule 21`
- [ ] `C-CF-33` `capability` The first model page response carries the model record. `src: Core features, Core features rule 22`
- [ ] `C-CF-34` `role` An anonymous reader receives the schema, form, examples, README, snippets. `src: Core features, Core features rule 24`
- [ ] `C-CF-35` `constraint` The API tab never prints a credential for an anonymous reader. `src: Core features, Core features rule 25`
- [ ] `C-CF-36` `ui` Each example shows its full input. `src: Core features, Core features rule 26`
- [ ] `C-CF-37` `contract` `/<owner>/<model>/readme` renders the author's markdown. `src: Core features, Core features rule 27`
- [ ] `C-CF-38` `constraint` A script bearing address in author markdown is stripped. `src: Core features, Core features rule 27`
- [ ] `C-CF-39` `ui` The versions list marks a version whose input schema differs from the previous version. `src: Core features, Core features rule 28`
- [ ] `C-CF-40` `literal` Version `3b71e0c9` of `northlight/scribe-2` is seeded withdrawn. `src: Core features, Core features rule 29`
- [ ] `C-CF-41` `constraint` A create naming a withdrawn version writes no prediction row. `src: Core features, Core features rule 29`
- [ ] `C-CF-42` `constraint` No hand written run form exists in the build. `src: Core features, Core features rule 30`
- [ ] `C-CF-43` `capability` A schema type `string` renders a single line text input. `src: Core features, Core features rule 31`
- [ ] `C-CF-44` `capability` A `string` carrying the format hint `text` renders an auto growing textarea. `src: Core features, Core features rule 31`
- [ ] `C-CF-45` `capability` A `number` renders a numeric input bounded by `minimum`, `maximum`. `src: Core features, Core features rule 31`
- [ ] `C-CF-46` `capability` An `object` renders a collapsed JSON editor for that subtree. `src: Core features, Core features rule 31`
- [ ] `C-CF-47` `ui` A field row renders a required marker where the field is required. `src: Core features, Core features rule 32`
- [ ] `C-CF-48` `capability` The advanced disclosure's open state is remembered per model in the browser. `src: Core features, Core features rule 33`
- [ ] `C-CF-49` `ui` A rejected submit marks the control invalid for assistive technology. `src: Core features, Core features rule 35`
- [ ] `C-CF-50` `constraint` A rejected submission writes no prediction row. `src: Core features, Core features rule 35`
- [ ] `C-CF-51` `literal` A server rejection of the input carries the error type `prediction_input_invalid`. `src: Core features, Core features rule 36`
- [ ] `C-CF-52` `capability` Editing the JSON updates the form. `src: Core features, Core features rule 37`
- [ ] `C-CF-53` `constraint` A round trip through both tabs preserves `0`, `false`, an empty string, `null`. `src: Core features, Core features rule 37`
- [ ] `C-CF-54` `constraint` No credential is inlined into any snippet. `src: Core features, Core features rule 38`
- [ ] `C-CF-55` `capability` The form prefills from the schema defaults where no featured example exists. `src: Core features, Core features rule 39`
- [ ] `C-CF-56` `literal` The textarea hint reads `Shift + Return to add a new line`. `src: Core features, Core features rule 40`
- [ ] `C-CF-57` `capability` An anonymous submit resolves to `/signin` carrying a return target. `src: Core features, Core features rule 41`
- [ ] `C-CF-58` `data` The mapping from input to priced quantity is declared in the version's metadata. `src: Core features, Core features rule 42`
- [ ] `C-CF-59` `ui` The `Booting` output state is named separately from `Queued`. `src: Core features, Core features rule 43`
- [ ] `C-CF-60` `literal` The `Booting` state for a twelve second load carries the phrase `usually takes 12 seconds the first time`. `src: Core features, Core features rule 43`
- [ ] `C-CF-61` `ui` The elapsed value is set large under the output. `src: Core features, Core features rule 44`
- [ ] `C-CF-62` `capability` The output renderer is chosen from the version's declared output type. `src: Core features, Core features rule 45`
- [ ] `C-CF-63` `constraint` A rendered output reserves its space before the content arrives. `src: Core features, Core features rule 45`
- [ ] `C-CF-64` `literal` The action row opens with the tweak control, then `Share`, `Download`, `Report`, `View full prediction`. `src: Core features, Core features rule 47`
- [ ] `C-CF-65` `capability` The tweak control loads the prediction's exact input back into the form without running. `src: Core features, Core features rule 47`
- [ ] `C-CF-66` `capability` A prediction's output is purged one hour after the run completed. `src: Core features, Core features rule 48`
- [ ] `C-CF-67` `ui` A present output prints its remaining lifetime beside the download control. `src: Core features, Core features rule 48`
- [ ] `C-CF-68` `constraint` A prediction identifier is 14 characters long. `src: Core features, Core features rule 49`
- [ ] `C-CF-69` `data` A prediction records the output, an error string on failure, logs, metrics. `src: Core features, Core features rule 50`
- [ ] `C-CF-70` `data` A prediction references an immutable version rather than a mutable model pointer. `src: Core features, Core features rule 52`
- [ ] `C-CF-71` `constraint` The span from `created_at` to `started_at` is never billed. `src: Core features, Core features rule 53`
- [ ] `C-CF-72` `capability` A prediction on a `Cold` version waits its declared load time in `starting`. `src: Core features, Core features rule 54`
- [ ] `C-CF-73` `literal` `northlight/scribe-2` is seeded `Warm`. `src: Core features, Core features rule 54`
- [ ] `C-CF-74` `constraint` A poll response carries a cache directive forbidding an intermediary from storing the record. `src: Core features, Core features rule 55`
- [ ] `C-CF-75` `literal` A blocking wait is asked for with the header `Prefer: wait=<seconds>`. `src: Core features, Core features rule 55`
- [ ] `C-CF-76` `capability` A blocking wait returns the pending record rather than a timeout at its ceiling. `src: Core features, Core features rule 55`
- [ ] `C-CF-77` `contract` A server sent stream is served at `/api/predictions/<id>/events`. `src: Core features, Core features rule 55`
- [ ] `C-CF-78` `constraint` The four read modes never report a state the others have not reached. `src: Core features, Core features rule 55`
- [ ] `C-CF-79` `literal` A webhook address failing either check is rejected with `webhook_url_not_allowed`. `src: Core features, Core features rule 56`
- [ ] `C-CF-80` `constraint` The webhook address check is re-applied at delivery time. `src: Core features, Core features rule 56`
- [ ] `C-CF-81` `capability` A terminal state writes one usage row in that same transaction. `src: Core features, Core features rule 57`
- [ ] `C-CF-82` `data` A delivery attempt records the last status code, the next attempt instant. `src: Core features, Core features rule 58`
- [ ] `C-CF-83` `capability` A failed delivery is retried with backoff for roughly 24 hours. `src: Core features, Core features rule 58`
- [ ] `C-CF-84` `literal` The same key with a different body is rejected with `idempotency_key_conflict`. `src: Core features, Core features rule 59`
- [ ] `C-CF-85` `constraint` Idempotency keys are scoped to the account. `src: Core features, Core features rule 59`
- [ ] `C-CF-86` `constraint` A cancel of a terminal prediction is rejected as invalid. `src: Core features, Core features rule 60`
- [ ] `C-CF-87` `capability` `/predictions` filters by model, status, source, date range. `src: Core features, Core features rule 61`
- [ ] `C-CF-88` `constraint` A prediction cursor stays valid across a page of new inserts. `src: Core features, Core features rule 61`
- [ ] `C-CF-89` `constraint` A token's clear value appears in no log line, audit row, error body, database column. `src: Core features, Core features rule 64`
- [ ] `C-CF-90` `data` A token carries a name supplied by its creator. `src: Core features, Core features rule 65`
- [ ] `C-CF-91` `role` A token created under an organisation acts as that organisation. `src: Core features, Core features rule 65`
- [ ] `C-CF-92` `role` A `run` token creates predictions. `src: Core features, Core features rule 66`
- [ ] `C-CF-93` `literal` A create presented with a `read` token is rejected with `token_scope_insufficient`. `src: Core features, Core features rule 66`
- [ ] `C-CF-94` `capability` A revoked token is refused on its very next use. `src: Core features, Core features rule 68`
- [ ] `C-CF-95` `ui` Revoking a token asks for the token's name to be typed first. `src: Core features, Core features rule 69`
- [ ] `C-CF-96` `literal` The revoke screen carries the phrase `Type the token's name to revoke`. `src: Core features, Core features rule 69`
- [ ] `C-CF-97` `capability` A token create past the limit is refused with the limit named. `src: Core features, Core features rule 70`
- [ ] `C-CF-98` `data` Every charge traces to one hardware class or priced unit. `src: Core features, Core features rule 71`
- [ ] `C-CF-99` `constraint` Summing the itemised rows of a period yields exactly the invoice total for that period. `src: Core features, Core features rule 71`
- [ ] `C-CF-100` `literal` `cpu-small` is rated `25` micro units per second. `src: Core features, Core features rule 73`
- [ ] `C-CF-101` `literal` `gpu-a40` is displayed as `GPU A40` with `8x` processors, `48GB` memory. `src: Core features, Core features rule 73`
- [ ] `C-CF-102` `ui` A scheduled rate is shown beside the date of effect. `src: Core features, Core features rule 74`
- [ ] `C-CF-103` `literal` Under `per_output_item` the quantity is the number of output items with a divisor of `1`. `src: Core features, Core features rule 75`
- [ ] `C-CF-104` `constraint` One billing path serves all three pricing modes. `src: Core features, Core features rule 75`
- [ ] `C-CF-105` `literal` `orchard/quickdraw-2` with `count` `3` costs `120000` micro units at `40000` per item. `src: Core features, Core features rule 76`
- [ ] `C-CF-106` `data` Hourly rollups exist per account, per model, per hardware class. `src: Core features, Core features rule 78`
- [ ] `C-CF-107` `constraint` Rollups are a cache over the usage rows rather than a source of truth. `src: Core features, Core features rule 78`
- [ ] `C-CF-108` `capability` A daily reconciliation re-sums the previous day's usage rows. `src: Core features, Core features rule 79`
- [ ] `C-CF-109` `literal` The default monthly spend cap is `2000000` micro units. `src: Core features, Core features rule 80`
- [ ] `C-CF-110` `constraint` The cap check is identical for the web run form, the machine interface, a deployment. `src: Core features, Core features rule 81`
- [ ] `C-CF-111` `literal` Warning notices fire at 50, 80, 95 per cent of the cap. `src: Core features, Core features rule 83`
- [ ] `C-CF-112` `constraint` The free allowance is consumed before charged spend. `src: Core features, Core features rule 84`
- [ ] `C-CF-113` `contract` `/account/usage` carries a date range picker defaulting to the current period. `src: Core features, Core features rule 85`
- [ ] `C-CF-114` `ui` The by day view draws the free allowance as its own band. `src: Core features, Core features rule 85`
- [ ] `C-CF-115` `capability` Every usage view exports the underlying rows as a file generated in the browser. `src: Core features, Core features rule 85`
- [ ] `C-CF-116` `data` An invoice carries the period, line items by model, by hardware class. `src: Core features, Core features rule 86`
- [ ] `C-CF-117` `ui` `/account/billing` shows the payment method as a masked reference. `src: Core features, Core features rule 87`
- [ ] `C-CF-118` `capability` A deployment accepts predictions at its own address. `src: Core features, Core features rule 89`
- [ ] `C-CF-119` `data` A deployment name is unique within its owning account. `src: Core features, Core features rule 90`
- [ ] `C-CF-120` `capability` `min_instances` of zero means scale to nothing when idle. `src: Core features, Core features rule 90`
- [ ] `C-CF-121` `ui` The deployment creation form states the standing cost of `min_instances` above zero per day. `src: Core features, Core features rule 91`
- [ ] `C-CF-122` `literal` One instance on `cpu-small` costs `2160000` micro units per day. `src: Core features, Core features rule 91`
- [ ] `C-CF-123` `constraint` Scaling decisions never read processor utilisation. `src: Core features, Core features rule 92`
- [ ] `C-CF-124` `capability` An instance is added when queue age has been above target for fifteen seconds. `src: Core features, Core features rule 92`
- [ ] `C-CF-125` `constraint` At most one scale down decision is made every cooldown. `src: Core features, Core features rule 92`
- [ ] `C-CF-126` `capability` Changing a deployment's version writes a release row. `src: Core features, Core features rule 95`
- [ ] `C-CF-127` `data` A release row records the actor, the instant, the previous value, the new value. `src: Core features, Core features rule 95`
- [ ] `C-CF-128` `constraint` Rollback never edits or deletes a release row. `src: Core features, Core features rule 95`
- [ ] `C-CF-129` `ui` The deployment page charts requests per minute, queue depth, queue age over one hour. `src: Core features, Core features rule 96`
- [ ] `C-CF-130` `ui` The deployment page shows the release log newest first with a rollback control per row. `src: Core features, Core features rule 96`
- [ ] `C-CF-131` `literal` The deployment `arden-hale/tidy-live` pins `arden-hale/notes-tidy` version `9a2b61de`. `src: Core features, Core features rule 97`
- [ ] `C-CF-132` `contract` `/models/new/packaging` takes the declarative packaging document. `src: Core features, Core features rule 98`
- [ ] `C-CF-133` `constraint` Each publish step is reachable by its own address. `src: Core features, Core features rule 98`
- [ ] `C-CF-134` `capability` The output schema is derived from the packaging document with the predict signature. `src: Core features, Core features rule 99`
- [ ] `C-CF-135` `constraint` A failure at any publish step leaves no version row. `src: Core features, Core features rule 101`
- [ ] `C-CF-136` `data` A version carries `id`, the owning model, `created_at`, `created_by`. `src: Core features, Core features rule 102`
- [ ] `C-CF-137` `literal` A version status is `building`, `active`, `deprecated`, or `withdrawn`. `src: Core features, Core features rule 102`
- [ ] `C-CF-138` `constraint` A version is never deleted during the lifetime of a prediction referencing that version. `src: Core features, Core features rule 102`
- [ ] `C-CF-139` `capability` Withdrawal states its reason to callers. `src: Core features, Core features rule 102`
- [ ] `C-CF-140` `constraint` An organisation has at least one owner at all times. `src: Core features, Core features rule 105`
- [ ] `C-CF-141` `contract` `/<org>/settings/members` lists members with their role. `src: Core features, Core features rule 106`
- [ ] `C-CF-142` `ui` `/<org>/settings/members` offers a control to remove a member. `src: Core features, Core features rule 106`
- [ ] `C-CF-143` `role` `/<org>/settings/members` is reachable only by an owner of that organisation. `src: Core features, Core features rule 106`
- [ ] `C-CF-144` `role` A denied membership call leaves the membership rows unchanged. `src: Core features, Core features rule 106`
- [ ] `C-CF-145` `constraint` A role change does not wait for the member's next sign in. `src: Core features, Core features rule 108`
- [ ] `C-CF-146` `role` A private model is readable only by principals of the owning account. `src: Core features, Core features rule 109`
- [ ] `C-CF-147` `role` A prediction is readable only by the creating account. `src: Core features, Core features rule 109`
- [ ] `C-CF-148` `role` A deployment is readable only by its owning account. `src: Core features, Core features rule 109`
- [ ] `C-CF-149` `role` A request for `arden-hale/notes-tidy` by `member2@example.com` is answered as missing. `src: Core features, Core features rule 110`
- [ ] `C-CF-150` `role` A request for a prediction on `arden-hale/notes-tidy` by `member2@example.com` is answered as missing. `src: Core features, Core features rule 110`
- [ ] `C-CF-151` `capability` The audit log records a token created, rotated, revoked, used for the first time. `src: Core features, Core features rule 111`
- [ ] `C-CF-152` `capability` The audit log records a spend cap changed. `src: Core features, Core features rule 111`
- [ ] `C-CF-153` `constraint` The audit log is append only. `src: Core features, Core features rule 111`
- [ ] `C-CF-154` `data` An audit entry carries the acting principal, the action. `src: Core features, Core features rule 112`
- [ ] `C-CF-155` `data` An audit entry carries a hash of its own content. `src: Core features, Core features rule 113`
- [ ] `C-CF-156` `contract` An account's audit log is readable at `/api/account/audit`. `src: Core features, Core features rule 113`
- [ ] `C-CF-157` `literal` The cookie answer is stored under the name `mp_cookie_choice`. `src: Core features, Core features rule 114`
- [ ] `C-CF-158` `literal` The announcement band dismissal is keyed by the promotion identifier `promo-autumn-2026`. `src: Core features, Core features rule 114`
- [ ] `C-CF-159` `capability` Every form rejects invalid input inline rather than on a separate page. `src: Core features, Core features rule 115`
- [ ] `C-CF-160` `constraint` Inline rejection holds for the deployment form, the publish wizard, the report form. `src: Core features, Core features rule 115`
- [ ] `C-CF-161` `capability` Every public route carries its own document title. `src: Core features, Core features rule 116`
- [ ] `C-CF-162` `capability` Every public route carries its own meta description. `src: Core features, Core features rule 116`
- [ ] `C-CF-163` `contract` `/robots.txt` names the sitemap by its absolute address. `src: Core features, Core features rule 117`
- [ ] `C-CF-164` `ui` The not-found page names the address that was tried. `src: Core features, Core features rule 118`
- [ ] `C-CF-165` `constraint` No token value appears in anything the browser downloads. `src: Core features, Core features rule 120`
- [ ] `C-CF-166` `constraint` No database password appears in anything the browser downloads. `src: Core features, Core features rule 120`
- [ ] `C-CF-167` `capability` Every page view of a public route is recorded with the route that was viewed. `src: Core features, Core features rule 121`
- [ ] `C-CF-168` `capability` Every public route declares a social preview title in its document head. `src: Core features, Core features rule 122`
- [ ] `C-CF-169` `capability` Every public route declares a social preview image in its document head. `src: Core features, Core features rule 122`
- [ ] `C-CF-170` `contract` The machine interface is JSON in, JSON out. `src: Core features, Core features rule 123`
- [ ] `C-CF-171` `constraint` Lists are paginated by cursor everywhere. `src: Core features, Core features rule 124`
- [ ] `C-CF-172` `literal` The default list limit is `25`. `src: Core features, Core features rule 124`
- [ ] `C-CF-173` `literal` A list response carries `results`, `next`, `previous`. `src: Core features, Core features rule 124`
- [ ] `C-CF-174` `constraint` List ordering is fixed per resource with the identifier as the final tie breaker. `src: Core features, Core features rule 124`
- [ ] `C-CF-175` `literal` Every error body carries `type`, `title`, `detail`, `status`, `instance`, `errors`. `src: Core features, Core features rule 125`
- [ ] `C-CF-176` `literal` The error types are `handle_reserved`, `model_version_withdrawn`, `idempotency_key_conflict`, `spend_cap_exceeded`. `src: Core features, Core features rule 126`
- [ ] `C-CF-177` `literal` Requests are rate limited per token at `60` requests per minute. `src: Core features, Core features rule 127`
- [ ] `C-CF-178` `data` Every response carries the remaining allowance for the applicable bucket. `src: Core features, Core features rule 127`
- [ ] `C-CF-179` `literal` A request past the rate limit is refused with the error type `rate_limited`. `src: Core features, Core features rule 127`
- [ ] `C-CF-180` `constraint` Work past the concurrency limit is never refused. `src: Core features, Core features rule 127`

## C-UF User flow

- [ ] `C-UF-01` `contract` `/` signed out renders the marketing home with the live example, the two catalogue rails. `src: User flow, User flow routes table row 1`
- [ ] `C-UF-02` `contract` `/collections/<slug>` shows one curated collection with its full model list. `src: User flow, User flow routes table row 3`
- [ ] `C-UF-03` `contract` `/privacy` states what the product stores about an account. `src: User flow, User flow routes table row 6`
- [ ] `C-UF-04` `contract` `/terms` states the terms of use. `src: User flow, User flow routes table row 7`
- [ ] `C-UF-05` `contract` `/signup` creates an account, claims a handle. `src: User flow, User flow routes table row 11`
- [ ] `C-UF-06` `contract` `/<owner>/<model>/settings` is reachable by the owner of the model. `src: User flow, User flow routes table row 19`
- [ ] `C-UF-07` `contract` `/account/tokens` mints, rotates, renames, revokes tokens. `src: User flow, User flow routes table row 23`
- [ ] `C-UF-08` `ui` Every console route carries the persistent left sidebar. `src: User flow, routes closing para`
- [ ] `C-UF-09` `capability` An anonymous request for a console route redirects to `/signin` carrying the requested address. `src: User flow, entry bullet 1`
- [ ] `C-UF-10` `capability` Signing in with no return target lands on `/dashboard`. `src: User flow, entry bullet 2`
- [ ] `C-UF-11` `constraint` A signed in request for `/` is not a redirect, so the address bar still reads `/`. `src: User flow, entry bullet 3`
- [ ] `C-UF-12` `role` A `member` opening `/<org>/settings/members` for an unowned organisation sees a missing page. `src: User flow, entry bullet 6`
- [ ] `C-UF-13` `role` A private model requested by a reader outside the owning account is answered as a missing page. `src: User flow, entry bullet 7`
- [ ] `C-UF-14` `capability` A handle that is neither reserved nor an account is answered by the not-found page. `src: User flow, entry bullet 8`
- [ ] `C-UF-15` `ui` The home route shows a code panel beside the output of that exact sample. `src: User flow, User flow journey 1`
- [ ] `C-UF-16` `ui` The `northlight/scribe-2` page shows the `Official` badge, the `Warm` badge, the run count `17.9M`. `src: User flow, User flow journey 1`
- [ ] `C-UF-17` `capability` Reloading the token screen shows the prefix with the last four characters only. `src: User flow, User flow journey 3`
- [ ] `C-UF-18` `ui` The metrics panel itemises a `northlight/scribe-2` run as `4` seconds at `25` micro units giving `100`. `src: User flow, User flow journey 4`
- [ ] `C-UF-19` `ui` The `orchard/quickdraw-2` form carries a `count` numeric field with a slider bounded at `1`, `4`. `src: User flow, User flow journey 5`
- [ ] `C-UF-20` `ui` An empty `subject` with a `count` of `9` marks both controls invalid. `src: User flow, User flow journey 6`
- [ ] `C-UF-21` `constraint` The `Run` control stays enabled through a rejected submission. `src: User flow, User flow journey 6`
- [ ] `C-UF-22` `ui` Cancelling a booting run moves the panel through `canceling` to `canceled`. `src: User flow, User flow journey 7`
- [ ] `C-UF-23` `capability` A second create carrying one idempotency key returns the first prediction unchanged. `src: User flow, User flow journey 8`
- [ ] `C-UF-24` `constraint` Two creates carrying one idempotency key leave one row in `/predictions`. `src: User flow, User flow journey 8`
- [ ] `C-UF-25` `constraint` A run past the cap writes no prediction row. `src: User flow, User flow journey 9`
- [ ] `C-UF-26` `role` The same create sent to the machine interface past the cap is refused with the same error type. `src: User flow, User flow journey 9`
- [ ] `C-UF-27` `role` `member2@example.com` requesting another account's prediction identifier sees the not-found page. `src: User flow, User flow journey 10`
- [ ] `C-UF-28` `capability` Rollback adds a release row pointing back at the earlier version. `src: User flow, User flow journey 12`
- [ ] `C-UF-29` `constraint` Rollback removes no release row. `src: User flow, User flow journey 12`
- [ ] `C-UF-30` `ui` Every list carries an empty state saying what would be there. `src: User flow, User flow states bullet 1`
- [ ] `C-UF-31` `ui` Every list carries a loading state occupying the final geometry. `src: User flow, User flow states bullet 2`
- [ ] `C-UF-32` `ui` A feedback banner stays until dismissed or until the reader navigates. `src: User flow, User flow states bullet 3`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product runs a poster register alongside a document register. `src: UI/UX notes, register para`
- [ ] `C-UX-02` `ui` The poster register appears in the home hero, the featured catalogue card. `src: UI/UX notes, poster para`
- [ ] `C-UX-03` `ui` The document register sets every identifier in monospace. `src: UI/UX notes, document para`
- [ ] `C-UX-04` `ui` Secondary ink carrying every metadata line is a mid neutral. `src: UI/UX notes, palette para`
- [ ] `C-UX-05` `ui` Cost emphasis is a deep vivid orange on a near-white muted amber band. `src: UI/UX notes, palette para`
- [ ] `C-UX-06` `constraint` Anything lighter than a mid neutral is a border or a disabled state rather than text. `src: UI/UX notes, palette para`
- [ ] `C-UX-07` `constraint` No status is carried by colour alone. `src: UI/UX notes, palette guard para`
- [ ] `C-UX-08` `literal` The body face is `Space Grotesk`. `src: UI/UX notes, type table row 1`
- [ ] `C-UX-09` `literal` The display face is `Fraunces`. `src: UI/UX notes, type table row 3`
- [ ] `C-UX-10` `literal` Secondary body copy is `14px` over `20px`. `src: UI/UX notes, scale table`
- [ ] `C-UX-11` `literal` A card title is `16px` over `24px` at `600`. `src: UI/UX notes, scale table`
- [ ] `C-UX-12` `literal` A route title is `36px`. `src: UI/UX notes, scale table`
- [ ] `C-UX-13` `literal` The home hero is `72px` over a line height of `0.95`. `src: UI/UX notes, scale table`
- [ ] `C-UX-14` `ui` The type scale is fixed rather than sized against the viewport. `src: UI/UX notes, scale para`
- [ ] `C-UX-15` `constraint` The document register carries no shadow on any element. `src: UI/UX notes, shape para`
- [ ] `C-UX-16` `ui` A raised surface is raised by a hairline border over a marginally whiter ground. `src: UI/UX notes, shape para`
- [ ] `C-UX-17` `ui` Content arriving after a fetch fades in. `src: UI/UX notes, motion para`
- [ ] `C-UX-18` `ui` A refused form submission nudges sideways by a single hair then back. `src: UI/UX notes, motion para`
- [ ] `C-UX-19` `capability` The hero cycle pauses when the document is hidden. `src: UI/UX notes, motion para`
- [ ] `C-UX-20` `constraint` The model list, the run form, the pricing table, long form prose never move. `src: UI/UX notes, stillness para`
- [ ] `C-UX-21` `capability` Under reduced motion the rails become ordinary scrollable lists with a visible affordance. `src: UI/UX notes, reduced motion para`
- [ ] `C-UX-22` `ui` The model page places the run form in one pane with the output panel in the other. `src: UI/UX notes, layout para`
- [ ] `C-UX-23` `capability` A link to a heading lands that heading below the header. `src: UI/UX notes, layout para`
- [ ] `C-UX-24` `ui` Every interactive element carries a resting, pointed at, pressed, focused, unavailable state. `src: UI/UX notes, components para`
- [ ] `C-UX-25` `ui` The theme control is a three way control in the footer status bar. `src: UI/UX notes, mode para`
- [ ] `C-UX-26` `capability` The dark theme inverts the roles of the neutral ramp rather than the hues. `src: UI/UX notes, mode para`
- [ ] `C-UX-27` `constraint` The theme choice is stored server visibly, so first paint is already correct. `src: UI/UX notes, mode para`
- [ ] `C-UX-28` `constraint` Body text meets WCAG AA against its ground in both themes. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-29` `ui` Every content image carries alternative text naming the depicted subject. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-30` `constraint` A decorative graphic declares itself decorative, carrying no alternative text. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-31` `constraint` Each route carries one first level heading with no skipped levels. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-32` `ui` A skip link is the first focusable element on every route. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-33` `capability` A prediction status change is announced politely as a status transition. `src: UI/UX notes, live regions para`
- [ ] `C-UX-34` `constraint` Streaming output is never announced token by token. `src: UI/UX notes, live regions para`
- [ ] `C-UX-35` `ui` At the narrow tier every console table becomes one card per row. `src: UI/UX notes, responsive para`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every symbol in the product is drawn geometry rather than a loaded picture. `src: Front-end specification, iconography para 1`
- [ ] `C-FE-02` `constraint` No icon package, no icon font is used. `src: Front-end specification, iconography para 1`
- [ ] `C-FE-03` `ui` The interface icon set holds a horizontal rule, a play mark in a circle, a lightning bolt. `src: Front-end specification, iconography para 2`
- [ ] `C-FE-04` `ui` A wait with no known duration replaces the ring with a turning partial arc. `src: Front-end specification, ring para`
- [ ] `C-FE-05` `capability` The ring is reused for any determinate wait longer than two seconds. `src: Front-end specification, ring para`
- [ ] `C-FE-06` `ui` Three bands sit at the top of every public route. `src: Front-end specification, chrome para 1`
- [ ] `C-FE-07` `ui` The header carries the glyph beside the wordmark at its left. `src: Front-end specification, header para`
- [ ] `C-FE-08` `literal` The header menu reads `Explore`, `Pricing`, `Docs`, `Blog`, `Changelog`, `Sign in`. `src: Front-end specification, header para`
- [ ] `C-FE-09` `ui` On a document register route the same backdrop element is fully transparent. `src: Front-end specification, transparent header para`
- [ ] `C-FE-10` `capability` Focus is trapped inside an open disclosure panel. `src: Front-end specification, disclosure para`
- [ ] `C-FE-11` `constraint` The document behind an open disclosure panel is locked without shifting the layout. `src: Front-end specification, disclosure para`
- [ ] `C-FE-12` `literal` The footer `Company` column holds `Home`, `About`, `Changelog`, `Join us`, `Terms`, `Privacy`, `Status`, `Support`. `src: Front-end specification, footer para`
- [ ] `C-FE-13` `ui` Four elements stick: the header, the run form footer, the console sidebar, the output pane. `src: Front-end specification, sticky para`
- [ ] `C-FE-14` `capability` A rail pauses under a pointer. `src: Front-end specification, rails para`
- [ ] `C-FE-15` `ui` Anything with a known shape shows a skeleton at that shape rather than a spinner. `src: Front-end specification, first paint para`
- [ ] `C-FE-16` `constraint` Every image, every media box declares its intrinsic dimensions before its bytes arrive. `src: Front-end specification, first paint para`
- [ ] `C-FE-17` `capability` Opening a prediction from a list pushes a history entry. `src: Front-end specification, scroll para`
- [ ] `C-FE-18` `ui` A list card description is clamped to one line. `src: Front-end specification, card para`
- [ ] `C-FE-19` `ui` Focus rings a model card rather than its inner link. `src: Front-end specification, card states para`
- [ ] `C-FE-20` `constraint` A withdrawn model's link still resolves. `src: Front-end specification, card states para`
- [ ] `C-FE-21` `ui` An enumeration with more than a handful of members renders as a select rather than radios. `src: Front-end specification, run form para`
- [ ] `C-FE-22` `literal` The home subheading closes `Deploy custom models. All with one line of code.` `src: Front-end specification, home para`
- [ ] `C-FE-23` `constraint` The hero sample comes from the same generator the run form's snippet tabs use. `src: Front-end specification, home para`
- [ ] `C-FE-24` `ui` The chip group is a real radio group with a group label, arrow key movement. `src: Front-end specification, home para`
- [ ] `C-FE-25` `constraint` Selecting a chip reorders already loaded rails on the client rather than fetching. `src: Front-end specification, home para`
- [ ] `C-FE-26` `literal` The inverted panel cells read `Automatic scale`, `Pay for what you use`, `Forget about infrastructure`, plus a monitoring cell. `src: Front-end specification, home para`
- [ ] `C-FE-27` `ui` A panel cell whose value cannot be served renders without its chart. `src: Front-end specification, home para`
- [ ] `C-FE-28` `capability` With the catalogue unavailable the rails render from a cached snapshot with a freshness note. `src: Front-end specification, home degraded para`
- [ ] `C-FE-29` `ui` The pricing route states that a private model runs on reserved capacity. `src: Front-end specification, pricing para`
- [ ] `C-FE-30` `constraint` The fast booting exception appears in the version list, the deployment form, the invoice line. `src: Front-end specification, pricing para`
- [ ] `C-FE-31` `capability` The hardware table derives the rate per hour from the rate per second. `src: Front-end specification, pricing para`
- [ ] `C-FE-32` `ui` The pricing route states that queue time is never billed. `src: Front-end specification, pricing para`
- [ ] `C-FE-33` `constraint` No raw stack trace, no framework error overlay ever reaches a reader. `src: Front-end specification, not found para`
- [ ] `C-FE-34` `ui` The console sidebar marks its active entry. `src: Front-end specification, console para`
- [ ] `C-FE-35` `ui` The dashboard shows month to date spend against the cap with a bar, the days remaining. `src: Front-end specification, console para`
- [ ] `C-FE-36` `constraint` Console tables virtualise past a threshold. `src: Front-end specification, console para`
- [ ] `C-FE-37` `ui` The generative field is a stack of three soft ellipses drifting under a heavy blur. `src: Front-end specification, zero-asset para`
- [ ] `C-FE-38` `constraint` A generated monogram is never inverted. `src: Front-end specification, zero-asset para`
- [ ] `C-FE-39` `constraint` The same model address always produces the same generated cover. `src: Front-end specification, zero-asset para`
- [ ] `C-FE-40` `literal` The narrow tier menu trigger reads `Menu`. `src: Front-end specification, copy deck`
- [ ] `C-FE-41` `literal` The explore remainder reads `and <N> more`. `src: Front-end specification, copy deck`
- [ ] `C-FE-42` `literal` The install command reads `npm install modelport`. `src: Front-end specification, copy deck`
- [ ] `C-FE-43` `literal` The cookie band reads `We use non-essential cookies to remember your choices. Accept or decline.` `src: Front-end specification, copy deck`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Pages are produced on the server from Jinja templates by a Flask application. `src: Technical requirements, Technical requirements para 1`
- [ ] `C-TR-02` `contract` Interactive behaviour is Alpine.js attached to the markup the server already sent. `src: Technical requirements, Technical requirements para 1`
- [ ] `C-TR-03` `constraint` The catalogue stays readable with script disabled. `src: Technical requirements, Technical requirements para 1`
- [ ] `C-TR-04` `contract` Data lives in PostgreSQL running as the `postgres` service. `src: Technical requirements, Technical requirements para 2`
- [ ] `C-TR-05` `literal` PostgreSQL is reached through the `DATABASE_URL` environment variable. `src: Technical requirements, Technical requirements para 2`
- [ ] `C-TR-06` `constraint` Only the libraries named in the brief plus their direct dependencies are used. `src: Technical requirements, Technical requirements para 3`
- [ ] `C-TR-07` `capability` A presented credential is verified by hashing the presented value, then looking up that hash. `src: Technical requirements, Technical requirements para 4`
- [ ] `C-TR-08` `constraint` Credential verification is a single indexed lookup rather than a scan. `src: Technical requirements, Technical requirements para 4`
- [ ] `C-TR-09` `constraint` Any comparison of a secret is constant time. `src: Technical requirements, Technical requirements para 4`
- [ ] `C-TR-10` `constraint` A revoked credential stops working everywhere within one second. `src: Technical requirements, Technical requirements para 5`
- [ ] `C-TR-11` `capability` Revocation publishes an invalidation that removes the cached entry at once. `src: Technical requirements, Technical requirements para 5`
- [ ] `C-TR-12` `contract` `GET /api/health` returns `200` once the application is ready. `src: Technical requirements, Technical requirements para 6`
- [ ] `C-TR-13` `capability` Every request carries a request identifier that appears in the error body, in the logs. `src: Technical requirements, Technical requirements para 7`
- [ ] `C-TR-14` `data` Three latencies are recorded separately on every prediction. `src: Technical requirements, Technical requirements para 7`
- [ ] `C-TR-15` `constraint` Seeding is idempotent, so restarting never duplicates a row. `src: Technical requirements, Technical requirements para 8`
- [ ] `C-TR-16` `constraint` An outbound fetch of a user supplied address goes through one place. `src: Technical requirements, Technical requirements para 10`
- [ ] `C-TR-17` `constraint` An outbound fetch connects to the address that was resolved. `src: Technical requirements, Technical requirements para 10`
- [ ] `C-TR-18` `constraint` A redirect is re-checked at every hop under a hop limit. `src: Technical requirements, Technical requirements para 10`
- [ ] `C-TR-19` `constraint` An outbound fetch applies a byte ceiling, a connection timeout, a total timeout. `src: Technical requirements, Technical requirements para 10`
- [ ] `C-TR-20` `constraint` A content type policy forbids sniffing. `src: Technical requirements, Technical requirements para 11`
- [ ] `C-TR-21` `capability` Admission checks the credential, the model, the input, the key, the cap, the concurrency, in order. `src: Technical requirements, admission para`
- [ ] `C-TR-22` `constraint` A shortage of capacity is queued with an honest status rather than refused. `src: Technical requirements, admission para`
- [ ] `C-TR-23` `capability` A sweep purges an output past its retention window, setting `data_removed`. `src: Technical requirements, caching para`
- [ ] `C-TR-24` `capability` A spend threshold crossing writes an in product notification the account reads. `src: Technical requirements, notifications para`
- [ ] `C-TR-25` `constraint` A notification is deduplicated per kind per period. `src: Technical requirements, notifications para`
- [ ] `C-TR-26` `data` Telemetry holds the three latencies, the error rate by class, queue depth, queue age. `src: Technical requirements, measurable para`
- [ ] `C-TR-27` `data` Telemetry holds the delivery age, the attempt count per webhook endpoint. `src: Technical requirements, measurable para`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds twenty five tables. `src: Data model, opening line`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password para`
- [ ] `C-DM-03` `contract` The seeded credentials are written into `/app/USER_README.md`. `src: Data model, password para`
- [ ] `C-DM-04` `data` Every tenant owned table carries `account_id` as a real foreign key. `src: Data model, conventions para`
- [ ] `C-DM-05` `data` Durations are stored as an integer count of milliseconds. `src: Data model, conventions para`
- [ ] `C-DM-06` `data` The `accounts` table holds `id`, `handle`, `kind`, `display_name`, `email`, `avatar_seed`, `state`. `src: Data model, accounts`
- [ ] `C-DM-07` `data` `accounts.handle` is unique without regard to case across every row. `src: Data model, accounts`
- [ ] `C-DM-08` `data` The `users_profile` table holds `account_id` beside `password_hash`. `src: Data model, users_profile`
- [ ] `C-DM-09` `data` `memberships.role` is `owner` or `member`. `src: Data model, memberships`
- [ ] `C-DM-10` `data` `tokens.token_hash` is unique. `src: Data model, tokens`
- [ ] `C-DM-11` `data` The `models` table holds `owner_account_id`, `name`, `visibility`, `default_version_id`, `official`. `src: Data model, models`
- [ ] `C-DM-12` `data` The `model_versions` table holds `pricing_mode`, `rate_micros`, `unit_divisor`, `quantity_source`. `src: Data model, model_versions`
- [ ] `C-DM-13` `data` `model_versions.pricing_mode` is `per_second`, `per_output_item` or `per_thousand_output_tokens`. `src: Data model, model_versions`
- [ ] `C-DM-14` `data` The `model_redirects` table is written on a rename or a transfer. `src: Data model, model_redirects`
- [ ] `C-DM-15` `data` Exactly one `hardware_classes` row is in force for a class at any instant. `src: Data model, hardware_classes`
- [ ] `C-DM-16` `data` The pair of account with idempotency key is unique wherever the key is present. `src: Data model, predictions`
- [ ] `C-DM-17` `data` The pair of deployment owner with lower cased name is unique. `src: Data model, deployments`
- [ ] `C-DM-18` `data` The `usage_rollups` table is keyed on account, bucket start, granularity, model, hardware class. `src: Data model, usage_rollups`
- [ ] `C-DM-19` `data` The `outbox` table holds `aggregate_type`, `aggregate_id`, `event_type`, `payload`, `published_at`. `src: Data model, outbox`
- [ ] `C-DM-20` `data` The `idempotency_keys` table is keyed on the account with the key. `src: Data model, idempotency_keys`
- [ ] `C-DM-21` `data` A stored idempotency snapshot is returned unchanged with its status. `src: Data model, idempotency_keys`
- [ ] `C-DM-22` `constraint` The application connects as a role that cannot read across accounts. `src: Data model, isolation para`
- [ ] `C-DM-23` `constraint` Work that legitimately crosses accounts connects as a separate role. `src: Data model, isolation para`
- [ ] `C-DM-24` `literal` Version `8f1c0a4d` declares `prompt`, a required `string` with the format hint `text`. `src: Data model, seed data`
- [ ] `C-DM-25` `literal` Version `8f1c0a4d` declares `include_title`, a `boolean` defaulting to `false`. `src: Data model, seed data`
- [ ] `C-DM-26` `literal` Version `c41d7b20` declares `subject`, a required `string`. `src: Data model, seed data`
- [ ] `C-DM-27` `literal` Version `c41d7b20` outputs an `array` of objects carrying `title`, `summary`, `tags`. `src: Data model, seed data`
- [ ] `C-DM-28` `literal` Version `c41d7b20` takes its priced quantity from the value of `count`. `src: Data model, seed data`
- [ ] `C-DM-29` `literal` Version `5e09a3f6` declares `text`, a required `string` with the format hint `text`. `src: Data model, seed data`
- [ ] `C-DM-30` `literal` Version `5e09a3f6` is priced `per_thousand_output_tokens` on `gpu-a40` at `3750` micro units. `src: Data model, seed data`
- [ ] `C-DM-31` `literal` Version `9a2b61de` declares `bullets`, a `boolean` defaulting to `true`. `src: Data model, seed data`
- [ ] `C-DM-32` `literal` `orchard/quickdraw-2` carries two examples. `src: Data model, seed data`
- [ ] `C-DM-33` `constraint` Restarting the app never duplicates a seeded row. `src: Data model, closing line`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The account is the one tenant boundary, so no sharing lattice exists. `src: Constraints, Constraints bullet 1`
- [ ] `C-CN-02` `constraint` No fine tuning, no training job exists. `src: Constraints, Constraints bullet 3`
- [ ] `C-CN-03` `constraint` The platform runs every prediction itself, recording the quantities each version declares. `src: Constraints, Constraints bullet 5`
- [ ] `C-CN-04` `constraint` No comparison bench, no editorial archive, no change history, no documentation site exists. `src: Constraints, Constraints bullet 7`
- [ ] `C-CN-05` `constraint` No federated sign in, no single sign on, no second factor exists. `src: Constraints, Constraints bullet 8`
- [ ] `C-CN-06` `literal` The app stays responsive with fifty thousand model rows. `src: Constraints, Constraints bullet 13`
- [ ] `C-CN-07` `literal` The app stays responsive with two hundred thousand prediction rows. `src: Constraints, Constraints bullet 13`
- [ ] `C-CN-08` `literal` The usage screen renders the current period in under one second at that volume. `src: Constraints, Constraints bullet 13`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract, Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` Both the port with the public address are read from the environment. `src: Deployment contract, Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract, Deployment contract bullet 3`
- [ ] `C-DC-04` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract, Deployment contract bullet 5`
- [ ] `C-DC-05` `contract` A production build is served behind a static or preview server. `src: Deployment contract, Deployment contract bullet 7`
- [ ] `C-DC-06` `contract` The server is not a child of the shell. `src: Deployment contract, Deployment contract bullet 8`
- [ ] `C-DC-07` `contract` The backing services named in the brief are already running. `src: Deployment contract, Deployment contract bullet 10`
- [ ] `C-DC-08` `contract` No persistent volume, no fixed container name, no custom network is declared. `src: Deployment contract, Deployment contract bullet 12`
- [ ] `C-DC-09` `contract` `POST /api/auth/login` sets the session cookie. `src: Deployment contract, API shapes table row 2`
- [ ] `C-DC-10` `contract` `GET /api/models` accepts `cursor`, `limit`, `collection`, `warm`, `owner`. `src: Deployment contract, API shapes table row 5`
- [ ] `C-DC-11` `contract` `POST /api/models` returns the model beside the created version's `digest`. `src: Deployment contract, API shapes table row 8`
- [ ] `C-DC-12` `contract` `POST /api/predictions` accepts `version` or `model`, `input`, `webhook_url`, `webhook_events`, `deployment`. `src: Deployment contract, API shapes table row 13`
- [ ] `C-DC-13` `contract` `POST /api/predictions/<id>/cancel` returns the prediction with `canceling` or `canceled`. `src: Deployment contract, API shapes table row 16`
- [ ] `C-DC-14` `contract` `POST /api/tokens` returns the token row beside the clear `token` value once. `src: Deployment contract, API shapes table row 20`
- [ ] `C-DC-15` `contract` `GET /api/account/usage` returns `total_micros`, `free_allowance_remaining_micros`, `cap_micros`, `rows`. `src: Deployment contract, API shapes table row 24`
- [ ] `C-DC-16` `contract` `PUT /api/account/spend-cap` takes `monthly_cap_micros`. `src: Deployment contract, API shapes table row 25`
- [ ] `C-DC-17` `contract` `PATCH /api/deployments/<owner>/<name>` returns the deployment beside the new release row. `src: Deployment contract, API shapes table row 30`
- [ ] `C-DC-18` `constraint` A list endpoint with a fixed row shape returns a top-level JSON array. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-19` `constraint` An invalid or unauthorized call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-20` `constraint` An in memory prediction list that resets on restart is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-21` `constraint` A usage total held in a variable rather than summed from rows is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-22` `constraint` An audit chain computed at read time is a contract violation. `src: Deployment contract, No mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | pinned value | C-RL-15 | User roles, seeded accounts para |
| `owner@example.com` | seeded account email | C-RL-16 | User roles, User roles seed table row 1 |
| `owner` | pinned value | C-RL-16 | User roles, User roles seed table row 1 |
| `northlight` | pinned value | C-RL-16 | User roles, User roles seed table row 1 |
| `member@example.com` | seeded account email | C-RL-17 | User roles, User roles seed table row 2 |
| `member` | pinned value | C-RL-17 | User roles, User roles seed table row 2 |
| `member2@example.com` | seeded account email | C-RL-18 | User roles, User roles seed table row 3 |
| `playground` | pinned value | C-CF-08 | Core features, Core features rule 5 |
| `account` | pinned value | C-CF-08 | Core features, Core features rule 5 |
| `settings` | pinned value | C-CF-08 | Core features, Core features rule 5 |
| `dashboard` | pinned value | C-CF-08 | Core features, Core features rule 5 |
| `predictions` | pinned value | C-CF-08 | Core features, Core features rule 5 |
| `trainings` | pinned value | C-CF-08 | Core features, Core features rule 5 |
| `17.9M` | pinned value | C-CF-17 | Core features, Core features rule 11 |
| `469.7K` | pinned value | C-CF-17 | Core features, Core features rule 11 |
| `4M` | pinned value | C-CF-17 | Core features, Core features rule 11 |
| `17` | pinned value | C-CF-17 | Core features, Core features rule 11 |
| `summarise-text` | pinned value | C-CF-23 | Core features, Core features rule 14 |
| `northlight/scribe-2` | pinned value | C-CF-23 | Core features, Core features rule 14 |
| `blackpine-labs/prism-2-flex` | pinned value | C-CF-23 | Core features, Core features rule 14 |
| `official` | pinned value | C-CF-24 | Core features, Core features rule 15 |
| `3b71e0c9` | pinned value | C-CF-40 | Core features, Core features rule 29 |
| `prediction_input_invalid` | pinned value | C-CF-51 | Core features, Core features rule 36 |
| `Shift + Return to add a new line` | pinned value | C-CF-56 | Core features, Core features rule 40 |
| `Booting` | pinned value | C-CF-60 | Core features, Core features rule 43 |
| `usually takes 12 seconds the first time` | pinned value | C-CF-60 | Core features, Core features rule 43 |
| `Share` | pinned value | C-CF-64 | Core features, Core features rule 47 |
| `Download` | pinned value | C-CF-64 | Core features, Core features rule 47 |
| `Report` | pinned value | C-CF-64 | Core features, Core features rule 47 |
| `View full prediction` | pinned value | C-CF-64 | Core features, Core features rule 47 |
| `Warm` | pinned value | C-CF-73 | Core features, Core features rule 54 |
| `Prefer: wait=<seconds>` | pinned value | C-CF-75 | Core features, Core features rule 55 |
| `webhook_url_not_allowed` | pinned value | C-CF-79 | Core features, Core features rule 56 |
| `idempotency_key_conflict` | pinned value | C-CF-84 | Core features, Core features rule 59 |
| `read` | pinned value | C-CF-93 | Core features, Core features rule 66 |
| `token_scope_insufficient` | pinned value | C-CF-93 | Core features, Core features rule 66 |
| `Type the token's name to revoke` | pinned value | C-CF-96 | Core features, Core features rule 69 |
| `cpu-small` | pinned value | C-CF-100 | Core features, Core features rule 73 |
| `25` | pinned value | C-CF-100 | Core features, Core features rule 73 |
| `gpu-a40` | pinned value | C-CF-101 | Core features, Core features rule 73 |
| `GPU A40` | pinned value | C-CF-101 | Core features, Core features rule 73 |
| `8x` | pinned value | C-CF-101 | Core features, Core features rule 73 |
| `48GB` | pinned value | C-CF-101 | Core features, Core features rule 73 |
| `per_output_item` | pinned value | C-CF-103 | Core features, Core features rule 75 |
| `1` | pinned value | C-CF-103 | Core features, Core features rule 75 |
| `orchard/quickdraw-2` | pinned value | C-CF-105 | Core features, Core features rule 76 |
| `count` | pinned value | C-CF-105 | Core features, Core features rule 76 |
| `3` | pinned value | C-CF-105 | Core features, Core features rule 76 |
| `120000` | pinned value | C-CF-105 | Core features, Core features rule 76 |
| `40000` | pinned value | C-CF-105 | Core features, Core features rule 76 |
| `2000000` | pinned value | C-CF-109 | Core features, Core features rule 80 |
| `2160000` | pinned value | C-CF-122 | Core features, Core features rule 91 |
| `arden-hale/tidy-live` | pinned value | C-CF-131 | Core features, Core features rule 97 |
| `arden-hale/notes-tidy` | pinned value | C-CF-131 | Core features, Core features rule 97 |
| `9a2b61de` | pinned value | C-CF-131 | Core features, Core features rule 97 |
| `building` | pinned value | C-CF-137 | Core features, Core features rule 102 |
| `active` | pinned value | C-CF-137 | Core features, Core features rule 102 |
| `deprecated` | pinned value | C-CF-137 | Core features, Core features rule 102 |
| `withdrawn` | pinned value | C-CF-137 | Core features, Core features rule 102 |
| `mp_cookie_choice` | pinned value | C-CF-157 | Core features, Core features rule 114 |
| `promo-autumn-2026` | pinned value | C-CF-158 | Core features, Core features rule 114 |
| `results` | pinned value | C-CF-173 | Core features, Core features rule 124 |
| `next` | pinned value | C-CF-173 | Core features, Core features rule 124 |
| `previous` | pinned value | C-CF-173 | Core features, Core features rule 124 |
| `type` | pinned value | C-CF-175 | Core features, Core features rule 125 |
| `title` | pinned value | C-CF-175 | Core features, Core features rule 125 |
| `detail` | pinned value | C-CF-175 | Core features, Core features rule 125 |
| `status` | pinned value | C-CF-175 | Core features, Core features rule 125 |
| `instance` | pinned value | C-CF-175 | Core features, Core features rule 125 |
| `errors` | pinned value | C-CF-175 | Core features, Core features rule 125 |
| `handle_reserved` | pinned value | C-CF-176 | Core features, Core features rule 126 |
| `model_version_withdrawn` | pinned value | C-CF-176 | Core features, Core features rule 126 |
| `spend_cap_exceeded` | pinned value | C-CF-176 | Core features, Core features rule 126 |
| `60` | pinned value | C-CF-177 | Core features, Core features rule 127 |
| `rate_limited` | pinned value | C-CF-179 | Core features, Core features rule 127 |
| `Space Grotesk` | pinned value | C-UX-08 | UI/UX notes, type table row 1 |
| `Fraunces` | pinned value | C-UX-09 | UI/UX notes, type table row 3 |
| `14px` | pinned value | C-UX-10 | UI/UX notes, scale table |
| `20px` | pinned value | C-UX-10 | UI/UX notes, scale table |
| `16px` | pinned value | C-UX-11 | UI/UX notes, scale table |
| `24px` | pinned value | C-UX-11 | UI/UX notes, scale table |
| `600` | pinned value | C-UX-11 | UI/UX notes, scale table |
| `36px` | pinned value | C-UX-12 | UI/UX notes, scale table |
| `72px` | pinned value | C-UX-13 | UI/UX notes, scale table |
| `0.95` | pinned value | C-UX-13 | UI/UX notes, scale table |
| `Explore` | pinned value | C-FE-08 | Front-end specification, header para |
| `Pricing` | pinned value | C-FE-08 | Front-end specification, header para |
| `Docs` | pinned value | C-FE-08 | Front-end specification, header para |
| `Blog` | pinned value | C-FE-08 | Front-end specification, header para |
| `Changelog` | pinned value | C-FE-08 | Front-end specification, header para |
| `Sign in` | pinned value | C-FE-08 | Front-end specification, header para |
| `Company` | pinned value | C-FE-12 | Front-end specification, footer para |
| `Home` | pinned value | C-FE-12 | Front-end specification, footer para |
| `About` | pinned value | C-FE-12 | Front-end specification, footer para |
| `Join us` | pinned value | C-FE-12 | Front-end specification, footer para |
| `Terms` | pinned value | C-FE-12 | Front-end specification, footer para |
| `Privacy` | pinned value | C-FE-12 | Front-end specification, footer para |
| `Status` | pinned value | C-FE-12 | Front-end specification, footer para |
| `Support` | pinned value | C-FE-12 | Front-end specification, footer para |
| `Deploy custom models. All with one line of code.` | pinned value | C-FE-22 | Front-end specification, home para |
| `Automatic scale` | pinned value | C-FE-26 | Front-end specification, home para |
| `Pay for what you use` | pinned value | C-FE-26 | Front-end specification, home para |
| `Forget about infrastructure` | pinned value | C-FE-26 | Front-end specification, home para |
| `Menu` | pinned value | C-FE-40 | Front-end specification, copy deck |
| `and <N> more` | pinned value | C-FE-41 | Front-end specification, copy deck |
| `npm install modelport` | pinned value | C-FE-42 | Front-end specification, copy deck |
| `We use non-essential cookies to remember your choices. Accept or decline.` | pinned value | C-FE-43 | Front-end specification, copy deck |
| `DATABASE_URL` | pinned value | C-TR-05 | Technical requirements, Technical requirements para 2 |
| `8f1c0a4d` | pinned value | C-DM-24 | Data model, seed data |
| `prompt` | pinned value | C-DM-24 | Data model, seed data |
| `string` | pinned value | C-DM-24 | Data model, seed data |
| `text` | pinned value | C-DM-24 | Data model, seed data |
| `include_title` | pinned value | C-DM-25 | Data model, seed data |
| `boolean` | pinned value | C-DM-25 | Data model, seed data |
| `false` | pinned value | C-DM-25 | Data model, seed data |
| `c41d7b20` | pinned value | C-DM-26 | Data model, seed data |
| `subject` | pinned value | C-DM-26 | Data model, seed data |
| `array` | pinned value | C-DM-27 | Data model, seed data |
| `summary` | pinned value | C-DM-27 | Data model, seed data |
| `tags` | pinned value | C-DM-27 | Data model, seed data |
| `5e09a3f6` | pinned value | C-DM-29 | Data model, seed data |
| `per_thousand_output_tokens` | pinned value | C-DM-30 | Data model, seed data |
| `3750` | pinned value | C-DM-30 | Data model, seed data |
| `bullets` | pinned value | C-DM-31 | Data model, seed data |
| `true` | pinned value | C-DM-31 | Data model, seed data |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the per endpoint webhook signing secret | C-CF-01 | named as the signing key with no literal given |
| the server side pepper used when hashing a token | C-CF-01 | named as an input to the hash with no literal given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 4 | 9 |
| User roles | 2 | 20 |
| Core features | 54 | 180 |
| User flow | 27 | 32 |
| UI and UX notes | 11 | 35 |
| Front-end specification | 31 | 43 |
| Technical requirements | 14 | 27 |
| Data model | 2 | 33 |
| Constraints | 1 | 8 |
| Deployment contract | 19 | 22 |

