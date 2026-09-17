# Checklist: Founder License Storefront

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment, done
Sections absent: buildplan
Items: 658
Unpinned values flagged: 0. Every value a grader asserts is pinned by an item, recorded in the pinned-literals table, or carried by the brief position its item cites, such as the privacy and terms heading identifiers named at their `src`.

Definition of done restates five Core features asks; its citation is merged into those items rather than given a block.

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a storefront with sixteen content routes. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app keeps a beta registration ledger with a capped founder cohort. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The app emails each registrant an access link. `src: Overview para 1`
- [ ] `C-OV-04` `capability` One release registry feeds the download redirect plus the signed update feed. `src: Overview para 1`
- [ ] `C-OV-05` `capability` The app includes a small operator console. `src: Overview para 1`
- [ ] `C-OV-06` `constraint` No endpoint accepts prompt content. `src: Overview para 3; Constraints bullet 2`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads every public route without a session. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A visitor registers on `/download` without any password. `src: User roles table row 1; User roles para 3`
- [ ] `C-RL-03` `role` A visitor asks for a fresh access link without a session. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A visitor files a data request without a session. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A visitor follows `/downloads/latest` without a session. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A visitor reads `/appcast.xml` without a session. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A registrant with an access session reads the registrant's own founder place on `/beta/status`. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A registrant session never returns another registrant's status. `src: User roles table row 2`
- [ ] `C-RL-09` `role` The server denies every operator endpoint to a visitor. `src: User roles table row 1; User roles para 2`
- [ ] `C-RL-10` `role` The server denies every operator endpoint to a registrant session. `src: User roles table row 2; User roles para 2`
- [ ] `C-RL-11` `role` A denied operator call leaves the protected state unchanged. `src: User roles para 2`
- [ ] `C-RL-12` `role` The operator signs in on `/operator` with email plus password. `src: User roles table row 3; Core features, Operator console rule 1`
- [ ] `C-RL-13` `role` The operator lists registrations. `src: User roles table row 3`
- [ ] `C-RL-14` `role` The operator publishes a release. `src: User roles table row 3; Core features, Operator console rule 2`
- [ ] `C-RL-15` `role` The operator revokes a release. `src: User roles table row 3; Core features, Operator console rule 2`
- [ ] `C-RL-16` `role` The operator revokes a registrant's active access links. `src: User roles table row 3; Core features, Operator console rule 2`
- [ ] `C-RL-17` `constraint` The operator console offers no signup. `src: User roles para 3`

## C-CF Core features

- [ ] `C-CF-01` `literal` The founder cohort holds exactly `1000` places. `src: Core features, Founder places rule 1`
- [ ] `C-CF-02` `literal` Places `1` to `500` sit in tier `1` at `2900`. `src: Core features, Founder places rule 1`
- [ ] `C-CF-03` `literal` Places `501` to `1000` sit in tier `2` at `3900`. `src: Core features, Founder places rule 1`
- [ ] `C-CF-04` `literal` Founder prices use currency `usd`. `src: Core features, Founder places rule 1`
- [ ] `C-CF-05` `capability` A registration of an address without a place receives the next free place as long as places remain. `src: Core features, Founder places rule 2`
- [ ] `C-CF-06` `constraint` The founder price follows the place number rather than the date. `src: Core features, Founder places rule 2`
- [ ] `C-CF-07` `constraint` Simultaneous registrations never receive the same place. `src: Core features, Founder places rule 3; Definition of done`
- [ ] `C-CF-08` `constraint` Held places always run from 1 to N with no gaps. `src: Core features, Founder places rule 3; Definition of done`
- [ ] `C-CF-09` `literal` The cohort state reads `closed` once every place is held. `src: Core features, Founder places rule 4`
- [ ] `C-CF-10` `capability` A registration after the cohort closes still succeeds with the same response. `src: Core features, Founder places rule 4`
- [ ] `C-CF-11` `constraint` A registration after the cohort closes receives no place. `src: Core features, Founder places rule 4; Definition of done`
- [ ] `C-CF-12` `constraint` A founder place is never reassigned, released or resold. `src: Core features, Founder places rule 5; User roles table row 3`
- [ ] `C-CF-13` `constraint` An address holds at most one founder place. `src: Core features, Founder places rule 5`
- [ ] `C-CF-14` `capability` Each held place has exactly one billing account in Kill Bill. `src: Core features, Founder places rule 6; Definition of done`
- [ ] `C-CF-15` `literal` The billing account externalKey is `lumen-founder-` plus the place padded to four digits. `src: Core features, Founder places rule 6`
- [ ] `C-CF-16` `literal` The billing account carries currency `USD`. `src: Core features, Founder places rule 6`
- [ ] `C-CF-17` `literal` The billing account carries country `US`. `src: Core features, Founder places rule 6`
- [ ] `C-CF-18` `capability` The billing account carries the registrant's email. `src: Core features, Founder places rule 6`
- [ ] `C-CF-19` `capability` The billing account name is the registrant's name, falling back to the email. `src: Core features, Founder places rule 6`
- [ ] `C-CF-20` `constraint` A repeat registration creates no second billing account. `src: Core features, Founder places rule 6`
- [ ] `C-CF-21` `constraint` A registration creates no invoice in Kill Bill. `src: Core features, Founder places rule 6; Technical requirements, Kill Bill`
- [ ] `C-CF-22` `data` `GET /api/founder/allocation` returns `cap`, `tier_size`, `claimed`, `remaining`, `state`, `current_tier`, `current_price_minor`, `currency`. `src: Core features, Founder places rule 7`
- [ ] `C-CF-23` `literal` The allocation `current_tier` reads `null` once the cohort is closed. `src: Core features, Founder places rule 7`
- [ ] `C-CF-24` `capability` The allocation figures equal the places actually held. `src: Core features, Founder places rule 7`
- [ ] `C-CF-25` `capability` The `/download` registration form succeeds with scripting disabled. `src: Core features, Beta registration rule 1`
- [ ] `C-CF-26` `constraint` Client-side checks never block a submission the server accepts. `src: Core features, Beta registration rule 1; Front-end specification, Join the beta`
- [ ] `C-CF-27` `data` `POST /api/beta/register` accepts `email`, `name`, `platform_version`, `role`, `primary_use`, `consent`, `company_website`. `src: Core features, Beta registration rule 2`
- [ ] `C-CF-28` `capability` The server stores the registration email trimmed. `src: Core features, Beta registration rule 3`
- [ ] `C-CF-29` `capability` The server stores the registration email lowercased. `src: Core features, Beta registration rule 3`
- [ ] `C-CF-30` `constraint` Addresses differing only in letter case form one registration. `src: Core features, Beta registration rule 3`
- [ ] `C-CF-31` `constraint` The server rejects a registration without an email. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-32` `constraint` The server rejects a registration with a malformed email. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-33` `literal` The server rejects an email longer than `254` characters. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-34` `constraint` The server rejects a registration without consent. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-35` `literal` The server rejects a `name` longer than `120` characters. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-36` `literal` The server rejects a `role` longer than `120` characters. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-37` `literal` The server rejects a `primary_use` longer than `240` characters. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-38` `constraint` A rejected registration stores nothing. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-39` `constraint` A rejected registration sends no email. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-40` `data` A rejected registration returns an `errors` object keyed by field name. `src: Core features, Beta registration rule 4`
- [ ] `C-CF-41` `literal` The server stores a `platform_version` outside `26.1`, `26.2`, `26.3`, `27` as empty. `src: Core features, Beta registration rule 5`
- [ ] `C-CF-42` `literal` A successful registration returns `status` set to `sent`. `src: Core features, Beta registration rule 6`
- [ ] `C-CF-43` `literal` A successful registration returns the message `Check your inbox for your access link.` `src: Core features, Beta registration rule 6`
- [ ] `C-CF-44` `capability` A successful registration echoes the normalised email. `src: Core features, Beta registration rule 6`
- [ ] `C-CF-45` `constraint` A repeat registration returns the same keys with the same wording as a first registration. `src: Core features, Beta registration rule 6`
- [ ] `C-CF-46` `constraint` A filled `company_website` trap field returns the normal success response. `src: Core features, Beta registration rule 7`
- [ ] `C-CF-47` `constraint` A filled trap field stores nothing. `src: Core features, Beta registration rule 7`
- [ ] `C-CF-48` `constraint` A filled trap field sends no email. `src: Core features, Beta registration rule 7`
- [ ] `C-CF-49` `capability` Each successful registration emails an access link. `src: Core features, Beta registration rule 8`
- [ ] `C-CF-50` `literal` An address receives at most `3` access emails in any rolling hour. `src: Core features, Beta registration rule 8`
- [ ] `C-CF-51` `constraint` The hourly email limit counts registrations with re-requests together. `src: Core features, Beta registration rule 8`
- [ ] `C-CF-52` `constraint` A submission past the hourly limit still returns the success response. `src: Core features, Beta registration rule 8`
- [ ] `C-CF-53` `constraint` A submission past the hourly limit sends no further email. `src: Core features, Beta registration rule 8`
- [ ] `C-CF-54` `constraint` Registration is never limited per network origin. `src: Core features, Beta registration rule 8`
- [ ] `C-CF-55` `literal` Each stored registration records `challenge_status` as `not_run`. `src: Core features, Beta registration rule 9`
- [ ] `C-CF-56` `capability` The access email travels over SMTP through Mailpit. `src: Core features, Access links rule 1`
- [ ] `C-CF-57` `constraint` The access email goes to the registrant only, with no cc or bcc. `src: Core features, Access links rule 1`
- [ ] `C-CF-58` `literal` The access email subject is `Your Lumen Prompt beta access link`. `src: Core features, Access links rule 1`
- [ ] `C-CF-59` `literal` The first plain-text line of the access email is the link `<APP_PUBLIC_URL>/beta/access/<token>`. `src: Core features, Access links rule 1`
- [ ] `C-CF-60` `literal` A first registration email's second line reads `You are registered for the Lumen Prompt beta.` `src: Core features, Access links rule 1`
- [ ] `C-CF-61` `literal` A later link email's second line carries the pinned already-on-the-list sentence. `src: Core features, Access links rule 1`
- [ ] `C-CF-62` `literal` An access email names a held founder place after `Your founder place:`. `src: Core features, Access links rule 1`
- [ ] `C-CF-63` `literal` A token holds at least `32` characters drawn from letters, digits, hyphens or underscores. `src: Core features, Access links rule 2`
- [ ] `C-CF-64` `constraint` The server stores a token only as a hash. `src: Core features, Access links rule 2`
- [ ] `C-CF-65` `literal` A link opens at most `5` times. `src: Core features, Access links rule 3`
- [ ] `C-CF-66` `literal` A link lives `14` days. `src: Core features, Access links rule 3`
- [ ] `C-CF-67` `literal` A new link marks older active links of the same address `superseded`. `src: Core features, Access links rule 3`
- [ ] `C-CF-68` `capability` Opening a live link counts one open. `src: Core features, Access links rule 4`
- [ ] `C-CF-69` `literal` The click log keeps at most one click per link per `30`-minute window. `src: Core features, Access links rule 4`
- [ ] `C-CF-70` `capability` Opening a live link sets an access session cookie. `src: Core features, Access links rule 4`
- [ ] `C-CF-71` `constraint` The access session lasts no longer than the link's remaining life. `src: Core features, Access links rule 4`
- [ ] `C-CF-72` `literal` A live link shows `Your access link is confirmed`. `src: Core features, Access links rule 4`
- [ ] `C-CF-73` `literal` A live link page offers a `Download for Mac` control to `/downloads/latest`. `src: Core features, Access links rule 4`
- [ ] `C-CF-74` `constraint` A failed link answers with a client-error status other than not-found. `src: Core features, Access links rule 5`
- [ ] `C-CF-75` `constraint` A failed link page never shows an email address. `src: Core features, Access links rule 5`
- [ ] `C-CF-76` `literal` A revoked or superseded link shows the pinned no-longer-valid heading. `src: Core features, Access links rule 5`
- [ ] `C-CF-77` `literal` A link opened after its fifth open shows the pinned used-up heading. `src: Core features, Access links rule 5`
- [ ] `C-CF-78` `literal` A link past its lifetime shows the pinned expired heading. `src: Core features, Access links rule 5`
- [ ] `C-CF-79` `literal` An unknown or malformed link shows the pinned not-recognised heading. `src: Core features, Access links rule 5`
- [ ] `C-CF-80` `capability` The not-recognised link page links to `/contact`. `src: Core features, Access links rule 5`
- [ ] `C-CF-81` `constraint` Failure precedence runs revoked, used up, expired, superseded. `src: Core features, Access links rule 5`
- [ ] `C-CF-82` `capability` Every failed link page carries the re-request form. `src: Core features, Access links rule 5; Front-end specification, Access and error pages`
- [ ] `C-CF-83` `capability` The first open after a fifth open emails the link owner a fresh link. `src: Core features, Access links rule 6`
- [ ] `C-CF-84` `capability` The used-up page says a fresh link was sent. `src: Core features, Access links rule 6`
- [ ] `C-CF-85` `data` `POST /api/beta/resend` takes `email`. `src: Core features, Access links rule 7`
- [ ] `C-CF-86` `literal` The resend endpoint always answers `If that address is registered, a fresh access link is on its way.` `src: Core features, Access links rule 7`
- [ ] `C-CF-87` `capability` The resend endpoint emails a fresh link to a registered address. `src: Core features, Access links rule 7`
- [ ] `C-CF-88` `constraint` The resend endpoint creates nothing for an unknown address. `src: Core features, Access links rule 7`
- [ ] `C-CF-89` `data` `GET /api/beta/status` returns `email`, `founder_position`, `founder_tier`, `founder_price_minor`, `currency`, `billing_account`. `src: Core features, Access links rule 8`
- [ ] `C-CF-90` `literal` `billing_account` reads `ready` only once the Kill Bill account for the place reads back. `src: Core features, Access links rule 8`
- [ ] `C-CF-91` `literal` `billing_account` reads `pending` until the Kill Bill account for the place reads back. `src: Core features, Access links rule 8`
- [ ] `C-CF-92` `constraint` `GET /api/beta/status` without a session is denied. `src: Core features, Access links rule 8`
- [ ] `C-CF-93` `capability` One release registry feeds the changelog, release notes, distribution panel, redirect plus feed. `src: Core features, Release registry rule 1; Definition of done`
- [ ] `C-CF-94` `constraint` No release surface hard-codes a version, size or checksum. `src: Core features, Release registry rule 1; Deployment contract, No mocks`
- [ ] `C-CF-95` `capability` The current stable release is the published release with the highest build. `src: Core features, Release registry rule 2; Data model, Derived`
- [ ] `C-CF-96` `data` `GET /api/releases` returns every release with its registry fields, highest build first. `src: Deployment contract, API shapes`
- [ ] `C-CF-97` `data` `GET /api/releases/{version}` returns that release with `notes`, answering not found for an unknown version. `src: Deployment contract, API shapes`
- [ ] `C-CF-98` `literal` The seeded current stable release is `0.2.3` with build `4`. `src: Core features, Release registry rule 2`
- [ ] `C-CF-99` `capability` `/downloads/latest` redirects to the current stable `download_url`. `src: Core features, Release registry rule 3`
- [ ] `C-CF-100` `literal` `/downloads/latest` carries `Cache-Control: no-store`. `src: Core features, Release registry rule 3; Technical requirements, Caching`
- [ ] `C-CF-101` `capability` Each redirect raises the release `download_count` by exactly one. `src: Core features, Release registry rule 3`
- [ ] `C-CF-102` `capability` `/appcast.xml` carries one item per published release. `src: Core features, Release registry rule 4`
- [ ] `C-CF-103` `constraint` `/appcast.xml` carries no item for a revoked release. `src: Core features, Release registry rule 4`
- [ ] `C-CF-104` `constraint` Feed items run highest build first. `src: Core features, Release registry rule 4`
- [ ] `C-CF-105` `data` Each feed enclosure repeats the registry `download_url`, `size_bytes` with `ed_signature` unchanged. `src: Core features, Release registry rule 4`
- [ ] `C-CF-106` `capability` A published release becomes current stable at once on every release surface. `src: Core features, Release registry rule 5; Technical requirements, Caching`
- [ ] `C-CF-107` `capability` A revoked release leaves the feed at once. `src: Core features, Release registry rule 5`
- [ ] `C-CF-108` `capability` A revoked release leaves the download redirect at once. `src: Core features, Release registry rule 5`
- [ ] `C-CF-109` `capability` `/changelog` shows a revoked release with the pinned revoked notice. `src: Core features, Release registry rule 5; Front-end specification, Changelog`
- [ ] `C-CF-110` `constraint` `/changelog` shows no download control for a revoked release. `src: Core features, Release registry rule 5; Front-end specification, Changelog`
- [ ] `C-CF-111` `constraint` The server rejects a publish whose `version` is not three dot-separated numbers. `src: Core features, Release registry rule 6`
- [ ] `C-CF-112` `constraint` The server rejects a publish whose `version` already exists. `src: Core features, Release registry rule 6`
- [ ] `C-CF-113` `constraint` The server rejects a publish whose `build` is not greater than every existing build. `src: Core features, Release registry rule 6; Data model, releases`
- [ ] `C-CF-114` `constraint` The server rejects a publish whose `sha256` is not 64 lowercase hexadecimal characters. `src: Core features, Release registry rule 6`
- [ ] `C-CF-115` `constraint` A rejected publish stores nothing. `src: Core features, Release registry rule 6`
- [ ] `C-CF-116` `capability` An unknown release-notes version shows the not-found page with a link to `/changelog`. `src: Core features, Release registry rule 7`
- [ ] `C-CF-117` `data` `POST /api/auth/login` returns `access_token`. `src: Core features, Operator console rule 1`
- [ ] `C-CF-118` `data` Operator endpoints read `Authorization: Bearer <token>`. `src: Core features, Operator console rule 1`
- [ ] `C-CF-119` `constraint` A wrong operator password is denied without a token. `src: Core features, Operator console rule 1; Core features, Auth`
- [ ] `C-CF-120` `capability` `GET /api/admin/registrations` lists registrations newest first. `src: Core features, Operator console rule 2`
- [ ] `C-CF-121` `capability` `GET /api/admin/registrations` filtered by `email` returns only that normalised address. `src: Core features, Operator console rule 2`
- [ ] `C-CF-122` `data` `POST /api/admin/releases` publishes a release for the operator. `src: Core features, Operator console rule 2`
- [ ] `C-CF-123` `data` `POST /api/admin/releases/{version}/revoke` revokes that release for the operator. `src: Core features, Operator console rule 2`
- [ ] `C-CF-124` `data` `POST /api/admin/access-links/revoke` returns the count as `revoked`. `src: Core features, Operator console rule 2`
- [ ] `C-CF-125` `ui` The operator console lists registrations with their founder places. `src: Core features, Operator console rule 4`
- [ ] `C-CF-126` `ui` The operator console lists releases with their status. `src: Core features, Operator console rule 4`
- [ ] `C-CF-127` `ui` The operator console offers a revoke control on each published release. `src: Core features, Operator console rule 4`
- [ ] `C-CF-128` `literal` `POST /api/checkout/founder` is rejected with `checkout_not_open`. `src: Core features, Checkout rule 1`
- [ ] `C-CF-129` `constraint` A checkout attempt creates no billing account. `src: Core features, Checkout rule 1`
- [ ] `C-CF-130` `constraint` A checkout attempt creates no invoice. `src: Core features, Checkout rule 1`
- [ ] `C-CF-131` `literal` `/checkout/founder` with `/checkout/return` show `Founder checkout opens at 1.0`. `src: Core features, Checkout rule 1; User flow journey 7`
- [ ] `C-CF-132` `capability` The checkout pages link to `/download`. `src: Core features, Checkout rule 1`
- [ ] `C-CF-133` `literal` `POST /api/licence/activate` is rejected with `licensing_not_open`. `src: Core features, Checkout rule 2`
- [ ] `C-CF-134` `literal` `/licence/activate` shows `Licence activation opens at 1.0`. `src: Core features, Checkout rule 2`
- [ ] `C-CF-135` `capability` `/legal/data-request` takes an email with a kind. `src: Core features, Data requests rule 1`
- [ ] `C-CF-136` `literal` A data-request kind is one of `access`, `export`, `correction`, `deletion`. `src: Core features, Data requests rule 1`
- [ ] `C-CF-137` `data` `POST /api/legal/data-requests` stores the request with its email plus kind. `src: Core features, Data requests rule 1`
- [ ] `C-CF-138` `literal` A stored data request carries status `open`. `src: Core features, Data requests rule 1`
- [ ] `C-CF-139` `literal` The data-request endpoint answers `We will reply to that address within 30 days.` `src: Core features, Data requests rule 1`
- [ ] `C-CF-140` `constraint` The server rejects a data request without an email. `src: Core features, Data requests rule 2`
- [ ] `C-CF-141` `constraint` The server rejects a data request with any other kind. `src: Core features, Data requests rule 2`
- [ ] `C-CF-142` `constraint` A rejected data request stores nothing. `src: Core features, Data requests rule 2`
- [ ] `C-CF-143` `ui` Cmd K or Ctrl K opens the command palette on every route. `src: Core features, Site-wide rule 1; Front-end specification, Command palette`
- [ ] `C-CF-144` `ui` The command palette works entirely by keyboard. `src: Core features, Site-wide rule 1`
- [ ] `C-CF-145` `capability` Every page footer links to the privacy page. `src: Core features, Site-wide rule 2`
- [ ] `C-CF-146` `capability` Every page footer links to the terms page. `src: Core features, Site-wide rule 2`
- [ ] `C-CF-147` `constraint` Every internal link on every public route resolves. `src: Core features, Site-wide rule 3`
- [ ] `C-CF-148` `capability` An unknown address shows the branded not-found page with a not-found status. `src: Core features, Site-wide rule 4; User flow, Entry`
- [ ] `C-CF-149` `capability` The not-found page links to `/`, `/download`, `/changelog`, `/contact`. `src: Core features, Site-wide rule 4; Front-end specification, Access and error pages`
- [ ] `C-CF-150` `ui` The not-found page shows a hint for the palette shortcut. `src: Core features, Site-wide rule 4`
- [ ] `C-CF-151` `constraint` The server stores the operator password hashed. `src: Core features, Auth`
- [ ] `C-CF-152` `constraint` A request with an invalid operator token is denied. `src: Core features, Auth; User flow, Entry`
- [ ] `C-CF-153` `constraint` The access session cookie is HttpOnly. `src: Core features, Auth`
- [ ] `C-CF-154` `constraint` The operator sign-in offers no password reset. `src: Core features, Auth; Constraints bullet 5`

## C-UF User flow

- [ ] `C-UF-01` `capability` `/` serves the home page. `src: User flow route table row 1`
- [ ] `C-UF-02` `capability` `/download` serves the join-the-beta page. `src: User flow route table row 2`
- [ ] `C-UF-03` `capability` `/use-cases` serves the use-case index. `src: User flow route table row 3`
- [ ] `C-UF-04` `capability` `/use-cases/reusable-ai-prompt-templates` serves an acquisition page. `src: User flow route table row 4`
- [ ] `C-UF-05` `capability` `/use-cases/prompt-version-history` serves an acquisition page. `src: User flow route table row 5`
- [ ] `C-UF-06` `capability` `/use-cases/prompt-manager-for-mac` serves an acquisition page. `src: User flow route table row 6`
- [ ] `C-UF-07` `capability` `/use-cases/local-first-prompt-library` serves an acquisition page. `src: User flow route table row 7`
- [ ] `C-UF-08` `capability` `/use-cases/hotkey-prompt-injection-macos` serves an acquisition page. `src: User flow route table row 8`
- [ ] `C-UF-09` `capability` `/changelog` serves the release index. `src: User flow route table row 9`
- [ ] `C-UF-10` `capability` `/release-notes/0.2.3` serves the current release notes. `src: User flow route table row 10`
- [ ] `C-UF-11` `capability` `/roadmap` serves the roadmap. `src: User flow route table row 11`
- [ ] `C-UF-12` `capability` `/blog` serves the article index. `src: User flow route table row 12`
- [ ] `C-UF-13` `capability` `/blog/prompts-are-work-product` serves an article. `src: User flow route table row 13`
- [ ] `C-UF-14` `capability` `/blog/stop-rewriting-your-best-prompt` serves an article. `src: User flow route table row 14`
- [ ] `C-UF-15` `capability` `/press` serves the press kit. `src: User flow route table row 15`
- [ ] `C-UF-16` `capability` `/contact` serves the contact page. `src: User flow route table row 16`
- [ ] `C-UF-17` `capability` `/privacy` serves the privacy policy. `src: User flow route table row 17`
- [ ] `C-UF-18` `capability` `/terms` serves the terms. `src: User flow route table row 18`
- [ ] `C-UF-19` `capability` `/beta/access/{token}` redeems an emailed link. `src: User flow route table row 19`
- [ ] `C-UF-20` `capability` `/beta/status` shows the registration state with the founder place. `src: User flow route table row 20`
- [ ] `C-UF-21` `capability` `/legal/data-request` serves the data-request intake. `src: User flow route table row 21`
- [ ] `C-UF-22` `capability` `/checkout/founder` serves the not-yet-open checkout page. `src: User flow route table row 22`
- [ ] `C-UF-23` `capability` `/checkout/return` serves the not-yet-open checkout return page. `src: User flow route table row 23`
- [ ] `C-UF-24` `capability` `/licence/activate` serves the not-yet-open licence page. `src: User flow route table row 24`
- [ ] `C-UF-25` `capability` `/operator` serves the operator sign-in with console. `src: User flow route table row 25`
- [ ] `C-UF-26` `capability` `/downloads/latest` answers with a redirect. `src: User flow route table row 26`
- [ ] `C-UF-27` `capability` `/appcast.xml` serves the update feed. `src: User flow route table row 27`
- [ ] `C-UF-28` `capability` `/sitemap.xml` serves the sitemap. `src: User flow route table row 28`
- [ ] `C-UF-29` `capability` `/robots.txt` serves the crawl rules. `src: User flow route table row 29`
- [ ] `C-UF-30` `literal` `/beta/status` without a session shows `Open the link in your email to see your status`. `src: User flow, Entry`
- [ ] `C-UF-31` `capability` `/beta/status` without a session shows the re-request form. `src: User flow, Entry`
- [ ] `C-UF-32` `capability` `/operator` without an operator session shows the sign-in form. `src: User flow, Entry`
- [ ] `C-UF-33` `capability` A successful operator sign-in shows the console. `src: User flow, Entry`
- [ ] `C-UF-34` `literal` The console's `Sign out` returns the operator to `/`. `src: User flow, Entry`
- [ ] `C-UF-35` `constraint` A registrant access session never opens the operator console. `src: User flow, Entry`
- [ ] `C-UF-36` `capability` A home anchor followed from another route navigates home then scrolls to the section. `src: User flow, Entry`
- [ ] `C-UF-37` `capability` The access route drops the token from the address bar once the session is set. `src: User flow, Entry; Front-end specification, Access and error pages`
- [ ] `C-UF-38` `ui` Submitting the registration form replaces the form in place with a `Check your inbox` panel. `src: User flow journey 1`
- [ ] `C-UF-39` `ui` The success panel names the submitted address. `src: User flow journey 1`
- [ ] `C-UF-40` `ui` The success panel suggests checking the spam folder. `src: User flow journey 1`
- [ ] `C-UF-41` `ui` The success panel shows `Resend link` disabled with a visible 60-second count. `src: User flow journey 1; Front-end specification, Join the beta`
- [ ] `C-UF-42` `ui` The access page focuses the `Download for Mac` control. `src: User flow journey 2; Front-end specification, Access and error pages`
- [ ] `C-UF-43` `ui` `/beta/status` shows the founder place after the link opens. `src: User flow journey 2`
- [ ] `C-UF-44` `ui` The seeded expired link page shows the re-request form. `src: User flow journey 3`
- [ ] `C-UF-45` `ui` Re-requesting from the expired page shows the resend sentence. `src: User flow journey 3`
- [ ] `C-UF-46` `ui` On `/` the palette lists the Blueprints group first. `src: User flow journey 4`
- [ ] `C-UF-47` `ui` Typing `roadmap` in the palette then pressing Enter opens `/roadmap`. `src: User flow journey 4`
- [ ] `C-UF-48` `ui` The `/changelog` current stable block shows `0.2.3`. `src: User flow journey 5`
- [ ] `C-UF-49` `ui` `Read the notes` leads to `/release-notes/0.2.3`, which shows `Known issues`. `src: User flow journey 5`
- [ ] `C-UF-50` `ui` The console lists `registrant@example.com` at founder place 1. `src: User flow journey 6`
- [ ] `C-UF-51` `ui` The console lists release `0.2.0` as revoked. `src: User flow journey 6`
- [ ] `C-UF-52` `literal` A console search matching nothing shows `No registrations match`. `src: User flow, States`
- [ ] `C-UF-53` `capability` The registrations endpoint answers an empty array for an unregistered address. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Floating panes render translucent over a pale cool ground. `src: UI/UX notes, Material`
- [ ] `C-UX-02` `ui` A faint square grid is printed on the page ground. `src: UI/UX notes, Material`
- [ ] `C-UX-03` `ui` Each floating pane carries a thin near-white edge. `src: UI/UX notes, Material`
- [ ] `C-UX-04` `ui` Each floating pane carries a large soft shadow with a lit top line. `src: UI/UX notes, Material`
- [ ] `C-UX-05` `ui` Panes stay readable with the backdrop blur switched off. `src: UI/UX notes, Material; Front-end specification, Space`
- [ ] `C-UX-06` `ui` The page ground is a near-white cool neutral. `src: UI/UX notes, Palette`
- [ ] `C-UX-07` `ui` Primary text is a near-black cool neutral. `src: UI/UX notes, Palette`
- [ ] `C-UX-08` `ui` One light soft blue accent marks every primary action. `src: UI/UX notes, Palette`
- [ ] `C-UX-09` `ui` The blue accent marks selection with keyboard focus. `src: UI/UX notes, Palette`
- [ ] `C-UX-10` `constraint` The blue accent appears on nothing decorative. `src: UI/UX notes, Palette`
- [ ] `C-UX-11` `constraint` Teal marks attached material only, never a control. `src: UI/UX notes, Palette`
- [ ] `C-UX-12` `ui` Status text uses the darker text colour of success, warning or danger. `src: UI/UX notes, Palette`
- [ ] `C-UX-13` `ui` The injection history ledger is the only dark region. `src: UI/UX notes, Palette; Front-end specification, Colour`
- [ ] `C-UX-14` `ui` The dark ledger uses near-white text with a pale mint accent. `src: UI/UX notes, Palette`
- [ ] `C-UX-15` `ui` Window mockups draw red, orange, green title-bar dots. `src: UI/UX notes, Palette`
- [ ] `C-UX-16` `ui` Monospace marks only machine-read content such as key names, variables, versions, checksums, routes, timestamps. `src: UI/UX notes, Type`
- [ ] `C-UX-17` `ui` Display text with body text use the system interface typeface. `src: UI/UX notes, Type`
- [ ] `C-UX-18` `ui` Moving elements share one eased house curve. `src: UI/UX notes, Motion`
- [ ] `C-UX-19` `ui` Panels arrive by rising a short distance with a fade in. `src: UI/UX notes, Motion`
- [ ] `C-UX-20` `ui` Colour, border, background, shadow transition together. `src: UI/UX notes, Motion`
- [ ] `C-UX-21` `constraint` A reduced-motion preference stops every loop with every sweep. `src: UI/UX notes, Motion; Front-end specification, Motion language`
- [ ] `C-UX-22` `ui` Under reduced motion, arrivals appear with a short fade. `src: UI/UX notes, Motion`
- [ ] `C-UX-23` `ui` The navigation is a floating top capsule, not a full-width bar. `src: UI/UX notes, Density; Front-end specification, Global chrome`
- [ ] `C-UX-24` `ui` Pricing, use cases, articles appear as card grids. `src: UI/UX notes, Density`
- [ ] `C-UX-25` `ui` Instruments sit beside copy on wide screens, above copy on narrow screens. `src: UI/UX notes, Density; Front-end specification, Home`
- [ ] `C-UX-26` `ui` Buttons rise slightly under the pointer. `src: UI/UX notes, Components`
- [ ] `C-UX-27` `ui` A pressed button settles with a shrinking shadow. `src: UI/UX notes, Components; Front-end specification, Motion language`
- [ ] `C-UX-28` `constraint` The focus ring shows on keyboard focus only, never on a pointer click. `src: UI/UX notes, Components; Front-end specification, Focus`
- [ ] `C-UX-29` `capability` Escape closes every dialog. `src: UI/UX notes, Components`
- [ ] `C-UX-30` `ui` A selected row carries a glow with a persistent left marker. `src: UI/UX notes, Components; Front-end specification, Focus`
- [ ] `C-UX-31` `ui` The site is designed fully in light mode. `src: UI/UX notes, Mode`
- [ ] `C-UX-32` `capability` Only the release notes pages follow a dark system appearance. `src: UI/UX notes, Mode; Front-end specification, Release notes`
- [ ] `C-UX-33` `literal` Body text keeps a contrast of at least `4.5:1` against the composited background. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-34` `literal` Primary text on the page ground keeps a contrast of at least `7:1`. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-35` `ui` Every foreground inside the dark ledger stays readable against the dark ground. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-36` `ui` Touch targets are comfortably sized. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-37` `ui` Keyboard navigation reaches every control with a visible focus ring. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-38` `ui` Every icon-only control has a label. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-39` `constraint` Colour alone never carries meaning. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-40` `ui` The layout holds at phone, tablet, desktop widths. `src: UI/UX notes, Responsive`
- [ ] `C-UX-41` `constraint` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes, Responsive; Front-end specification, The instrument system`
- [ ] `C-UX-42` `ui` Every navigation target stays reachable at a narrow viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-43` `ui` Below the wide breakpoint the six navigation links collapse into a menu button. `src: UI/UX notes, Responsive; Front-end specification, Global chrome`
- [ ] `C-UX-44` `constraint` Panes never render as opaque flat cards without depth. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-45` `constraint` No page is dominated by a single hue without a second signal. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-46` `constraint` Marketing decoration never stands where the working instruments belong. `src: UI/UX notes, What it must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every public route returns its content in server-rendered HTML with scripting disabled. `src: Technical requirements, Stack`
- [ ] `C-TR-02` `contract` The app keeps its data in the PostgreSQL database at `DATABASE_URL`. `src: Technical requirements, Environment`
- [ ] `C-TR-03` `contract` The app sends mail through the Mailpit server at `SMTP_HOST` with `SMTP_PORT`. `src: Technical requirements, Environment`
- [ ] `C-TR-04` `contract` The app reaches Kill Bill through `PAYMENTS_API_URL` with the four `PAYMENTS_` credentials. `src: Technical requirements, Environment; Technical requirements, Kill Bill`
- [ ] `C-TR-05` `contract` The app builds absolute email links from `APP_PUBLIC_URL`. `src: Technical requirements, Environment`
- [ ] `C-TR-06` `literal` Kill Bill writes carry `X-Killbill-CreatedBy`. `src: Technical requirements, Kill Bill`
- [ ] `C-TR-07` `constraint` A conflict on an existing externalKey is treated as success. `src: Technical requirements, Kill Bill`
- [ ] `C-TR-08` `literal` `GET /api/health` answers `200` with `status` set to `ok`. `src: Technical requirements, Health; Deployment contract bullet 3`
- [ ] `C-TR-09` `literal` Every response carries `Strict-Transport-Security: max-age=31536000; includeSubDomains`. `src: Technical requirements, Security headers`
- [ ] `C-TR-10` `literal` Every response carries `X-Content-Type-Options: nosniff`. `src: Technical requirements, Security headers`
- [ ] `C-TR-11` `literal` Every response carries `Referrer-Policy: strict-origin-when-cross-origin`. `src: Technical requirements, Security headers`
- [ ] `C-TR-12` `constraint` The content security policy allows only the site's own origin. `src: Technical requirements, Security headers`
- [ ] `C-TR-13` `capability` `/sitemap.xml` lists every one of the sixteen content routes as an absolute address. `src: Technical requirements, Crawling`
- [ ] `C-TR-14` `constraint` `/sitemap.xml` lists nothing beyond the sixteen content routes. `src: Technical requirements, Crawling`
- [ ] `C-TR-15` `literal` `/robots.txt` carries `Disallow: /downloads/latest`. `src: Technical requirements, Crawling`
- [ ] `C-TR-16` `literal` `/robots.txt` carries `Disallow: /api/`. `src: Technical requirements, Crawling`
- [ ] `C-TR-17` `literal` `/robots.txt` carries `Disallow: /beta/access/`. `src: Technical requirements, Crawling`
- [ ] `C-TR-18` `literal` `/robots.txt` carries `Disallow: /checkout/`. `src: Technical requirements, Crawling`
- [ ] `C-TR-19` `literal` `/robots.txt` names the sitemap on a `Sitemap:` line. `src: Technical requirements, Crawling`
- [ ] `C-TR-20` `literal` The access route markup carries `<meta name="robots" content="noindex">`. `src: Technical requirements, Crawling; Front-end specification, Access and error pages`
- [ ] `C-TR-21` `capability` Every content route carries a canonical link to the route itself. `src: Technical requirements, Crawling; Front-end specification, Use-case pages`
- [ ] `C-TR-22` `constraint` A use-case page never canonicalises to the use-case index. `src: Technical requirements, Crawling`
- [ ] `C-TR-23` `literal` Release notes carry `Cache-Control: public, max-age=3600, stale-while-revalidate=86400`. `src: Technical requirements, Caching`
- [ ] `C-TR-24` `literal` `/changelog` carries `Cache-Control: no-store`. `src: Technical requirements, Caching`
- [ ] `C-TR-25` `literal` `/appcast.xml` declares the `xmlns:sparkle` namespace `http://www.andymatuschak.org/xml-namespaces/sparkle`. `src: Technical requirements, Update feed format`
- [ ] `C-TR-26` `literal` Each feed item title reads `Lumen Prompt` followed by the version. `src: Technical requirements, Update feed format`
- [ ] `C-TR-27` `literal` Each feed item carries `sparkle:version` holding the build. `src: Technical requirements, Update feed format`
- [ ] `C-TR-28` `literal` Each feed item carries `sparkle:shortVersionString` holding the version. `src: Technical requirements, Update feed format`
- [ ] `C-TR-29` `literal` Each feed item carries `sparkle:minimumSystemVersion` holding the release `min_os`. `src: Technical requirements, Update feed format`
- [ ] `C-TR-30` `literal` Each feed item carries `sparkle:releaseNotesLink` to the release notes route. `src: Technical requirements, Update feed format`
- [ ] `C-TR-31` `literal` Each feed enclosure carries `type="application/octet-stream"`. `src: Technical requirements, Update feed format`
- [ ] `C-TR-32` `literal` Each feed enclosure carries `sparkle:edSignature`. `src: Technical requirements, Update feed format`
- [ ] `C-TR-33` `constraint` No route accepts a Blueprint, context file, rendered prompt or history row. `src: Technical requirements, System boundary`

## C-DM Data model

- [ ] `C-DM-01` `data` The database holds a `operators` table. `src: Data model para 1`
- [ ] `C-DM-02` `data` The database holds a `registrations` table. `src: Data model para 1`
- [ ] `C-DM-03` `data` The database holds a `founder_slots` table. `src: Data model para 1`
- [ ] `C-DM-04` `data` The database holds a `access_links` table. `src: Data model para 1`
- [ ] `C-DM-05` `data` The database holds a `access_clicks` table. `src: Data model para 1`
- [ ] `C-DM-06` `data` The database holds a `releases` table. `src: Data model para 1`
- [ ] `C-DM-07` `data` The database holds a `download_events` table. `src: Data model para 1`
- [ ] `C-DM-08` `data` The database holds a `data_requests` table. `src: Data model para 1`
- [ ] `C-DM-09` `constraint` The database stores timestamps in UTC. `src: Data model para 1`
- [ ] `C-DM-10` `literal` Money is stored in integer minor units with currency `usd`. `src: Data model para 1`
- [ ] `C-DM-11` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: Data model para 2`
- [ ] `C-DM-12` `data` `operators` holds `id`, `email`, `display_name`, `password_hash`, `created_at`. `src: Data model, operators`
- [ ] `C-DM-13` `data` `registrations` holds `id`, `email`, `name`, `platform_version`, `role`, `primary_use`, `consent_at`, `challenge_status`, `created_at`, `updated_at`. `src: Data model, registrations`
- [ ] `C-DM-14` `literal` `challenge_status` takes one of `not_run`, `passed`, `failed`. `src: Data model, registrations`
- [ ] `C-DM-15` `data` `founder_slots` holds `position`, `registration_id`, `tier`, `price_minor`, `currency`, `killbill_external_key`, `claimed_at`. `src: Data model, founder_slots`
- [ ] `C-DM-16` `constraint` `founder_slots` never stores a position outside 1 to 1000. `src: Data model, founder_slots`
- [ ] `C-DM-17` `constraint` Each `founder_slots` row has `tier` with `price_minor` agreeing with `position`. `src: Data model, founder_slots`
- [ ] `C-DM-18` `data` `access_links` holds `id`, `registration_id`, `token_hash`, `status`, `opens`, `max_opens`, `created_at`, `expires_at`. `src: Data model, access_links`
- [ ] `C-DM-19` `literal` An `access_links` row carries a `status` of `active`, `revoked` or `superseded`. `src: Data model, access_links`
- [ ] `C-DM-20` `capability` A new link's `expires_at` falls 14 days after its `created_at`. `src: Data model, access_links`
- [ ] `C-DM-21` `constraint` `opens` never exceeds `max_opens`, even under simultaneous opens. `src: Data model, access_links`
- [ ] `C-DM-22` `data` `access_clicks` holds `id`, `access_link_id`, `clicked_at`. `src: Data model, access_clicks`
- [ ] `C-DM-23` `data` `releases` holds `version`, `build`, `published_at`, `min_os`, `size_bytes`, `sha256`, `ed_signature`, `download_url`, `summary`, `notes`, `status`. `src: Data model, releases`
- [ ] `C-DM-24` `literal` A `releases` row carries a `status` of `published` or `revoked`. `src: Data model, releases`
- [ ] `C-DM-25` `data` `download_events` holds `id`, `release_version`, `access_link_id`, `created_at`. `src: Data model, download_events`
- [ ] `C-DM-26` `capability` A download from a registrant session records the access link on the download event. `src: Data model, download_events`
- [ ] `C-DM-27` `data` `data_requests` holds `id`, `email`, `kind`, `status`, `created_at`. `src: Data model, data_requests`
- [ ] `C-DM-28` `constraint` A release `download_count` is derived from download events. `src: Data model, Derived; Deployment contract, No mocks`
- [ ] `C-DM-29` `constraint` Cohort figures are derived from `founder_slots`. `src: Data model, Derived`
- [ ] `C-DM-30` `constraint` Link expiry is derived from `expires_at`. `src: Data model, Derived`
- [ ] `C-DM-31` `data` The seed holds operator `operator@example.com` named `Devrim`. `src: Data model, Seed data; User roles, Seeded people`
- [ ] `C-DM-32` `data` The seed holds registration `registrant@example.com` named `Ada Registrant`. `src: Data model, Seed data; User roles, Seeded people`
- [ ] `C-DM-33` `data` The seed holds registration `registrant2@example.com` named `Ben Registrant`. `src: Data model, Seed data; User roles, Seeded people`
- [ ] `C-DM-34` `data` The seed holds registration `registrant3@example.com` named `Cy Registrant`. `src: Data model, Seed data; User roles, Seeded people`
- [ ] `C-DM-35` `literal` Seeded registrations record consent with `challenge_status` set to `not_run`. `src: Data model, Seed data`
- [ ] `C-DM-36` `literal` Seeded place 1 belongs to `registrant@example.com` at tier 1 for `2900` under `lumen-founder-0001`. `src: Data model, Seed data; User roles, Seeded people`
- [ ] `C-DM-37` `capability` The app opens the `lumen-founder-0001` Kill Bill account at first start. `src: Data model, Seed data`
- [ ] `C-DM-38` `literal` Seeded link `seed-live-4b7d9e2a61c3f085` is active for `registrant@example.com`. `src: Data model, Seed data`
- [ ] `C-DM-39` `literal` Seeded link `seed-revoked-9a4d7e1f5b20` is revoked. `src: Data model, Seed data`
- [ ] `C-DM-40` `literal` Seeded link `seed-expired-7c1e2a9b4d36` for `registrant2@example.com` is already expired. `src: Data model, Seed data; User roles, Seeded people`
- [ ] `C-DM-41` `literal` Seeded link `seed-usedup-3f8b6d0c2e71` for `registrant3@example.com` has used all five opens. `src: Data model, Seed data; User roles, Seeded people`
- [ ] `C-DM-42` `literal` The seed holds published release `0.2.3` with its pinned build, date, size, checksum, signature, address, summary. `src: Data model, Seed data`
- [ ] `C-DM-43` `literal` The seed holds published release `0.2.2` with its pinned build, date, size, checksum, signature, address, summary. `src: Data model, Seed data`
- [ ] `C-DM-44` `literal` The seed holds published release `0.2.1` with its pinned build, date, size, checksum, signature, address, summary. `src: Data model, Seed data`
- [ ] `C-DM-45` `literal` The seed holds revoked release `0.2.0` with its pinned build, date, size, checksum, signature, address, summary. `src: Data model, Seed data`
- [ ] `C-DM-46` `capability` The `0.2.3` release notes list the five pinned known issues. `src: Data model, Seed data; Front-end specification, Release notes`
- [ ] `C-DM-47` `constraint` Restarting the app never duplicates seeded rows. `src: Data model, Seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Pages name the product Lumen Prompt, published by Halyard Labs. `src: Front-end specification, Identity`
- [ ] `C-FE-02` `ui` Copy names the destination apps Chatwell, Cadence, Vertan, Caret. `src: Front-end specification, Identity`
- [ ] `C-FE-03` `literal` The `0.2.3` release notes name the import sources Espresso, Alder, Rayline, Obelisk. `src: Front-end specification, Identity`
- [ ] `C-FE-04` `literal` The footer base line reads `(c) 2026 Halyard Labs`. `src: Front-end specification, Global chrome`
- [ ] `C-FE-05` `literal` The single support address is `hello@example.com`. `src: Front-end specification, Identity`
- [ ] `C-FE-06` `literal` Release binaries with the press kit are served from `https://downloads.example.com`. `src: Front-end specification, Identity`
- [ ] `C-FE-07` `constraint` No provider credential appears in anything the browser downloads. `src: Front-end specification, Identity`
- [ ] `C-FE-08` `literal` The home route shows the beats Summon hotkey, Search library, Fill variables, Inject history with their pinned descriptions. `src: Front-end specification, The product the site sells`
- [ ] `C-FE-09` `ui` Pages use Blueprint, Context, Time Machine, Injection History with the pinned meanings. `src: Front-end specification, The product the site sells`
- [ ] `C-FE-10` `literal` The navigation links read Product, Workflow, Use cases, Pricing, Blog, FAQ. `src: Front-end specification, Navigation model`
- [ ] `C-FE-11` `literal` Product, Workflow, Pricing, FAQ target `#features`, `#workflow`, `#pricing`, `#help` on the home route. `src: Front-end specification, Navigation model`
- [ ] `C-FE-12` `capability` The navigation shows `Join beta` on every route. `src: Front-end specification, Navigation model`
- [ ] `C-FE-13` `capability` The footer shows `Join beta`. `src: Front-end specification, Navigation model`
- [ ] `C-FE-14` `ui` Every content route ends with the `Join beta` call to action. `src: Front-end specification, Navigation model`
- [ ] `C-FE-15` `capability` The `Join beta` action leads to `/download`. `src: Front-end specification, Navigation model`
- [ ] `C-FE-16` `ui` A linked home section never lands underneath the navigation capsule. `src: Front-end specification, Navigation model`
- [ ] `C-FE-17` `ui` Exactly one navigation item is active on the home route at a time. `src: Front-end specification, Navigation model`
- [ ] `C-FE-18` `ui` The eyebrow pill shows a faint accent fill with darker accent text. `src: Front-end specification, Colour`
- [ ] `C-FE-19` `ui` Selected text shows a translucent accent highlight. `src: Front-end specification, Colour`
- [ ] `C-FE-20` `ui` The focus ring stays visible inside the dark history region. `src: Front-end specification, Colour`
- [ ] `C-FE-21` `constraint` The traffic dots are hidden from assistive technology. `src: Front-end specification, Colour`
- [ ] `C-FE-22` `literal` Secondary text on a resting pane keeps a contrast of at least `4.5:1`. `src: Front-end specification, Contrast obligations`
- [ ] `C-FE-23` `literal` Meaningful tertiary text keeps a contrast of at least `4.5:1`. `src: Front-end specification, Contrast obligations`
- [ ] `C-FE-24` `literal` Placeholder text keeps a contrast of at least `3:1`. `src: Front-end specification, Contrast obligations`
- [ ] `C-FE-25` `literal` `IBM Plex Mono` is the only downloaded font family. `src: Front-end specification, Typography`
- [ ] `C-FE-26` `literal` `IBM Plex Mono` ships in weights `400`, `500`, `600`. `src: Front-end specification, Typography`
- [ ] `C-FE-27` `capability` Downloaded font faces swap in so text is never invisible. `src: Front-end specification, Typography`
- [ ] `C-FE-28` `literal` Body prose renders at `16px` on a `24px` line height. `src: Front-end specification, Typography`
- [ ] `C-FE-29` `literal` Text below display size uses only the sizes `10px`, `11px`, `12px`, `14px`, `16px`, `18px`. `src: Front-end specification, Typography`
- [ ] `C-FE-30` `literal` Uppercase eyebrow labels render at `11px`, bold at `700`. `src: Front-end specification, Typography`
- [ ] `C-FE-31` `ui` Every uppercase label below `13px` carries open letter spacing. `src: Front-end specification, Typography`
- [ ] `C-FE-32` `ui` Display sizes scale fluidly with the viewport. `src: Front-end specification, Typography`
- [ ] `C-FE-33` `ui` The hero headline sets on four lines at the widest width. `src: Front-end specification, Typography`
- [ ] `C-FE-34` `ui` The hero headline stays readable without hyphenation at the narrowest width. `src: Front-end specification, Typography`
- [ ] `C-FE-35` `ui` Consecutive sections keep a generous block rhythm. `src: Front-end specification, Space, radius, elevation and blur`
- [ ] `C-FE-36` `ui` Legal pages with articles use the two widest prose measures. `src: Front-end specification, Space, radius, elevation and blur`
- [ ] `C-FE-37` `ui` Controls inside a pane use a smaller radius than the pane. `src: Front-end specification, Space, radius, elevation and blur`
- [ ] `C-FE-38` `constraint` Only capsule-shaped things use the fully rounded shape. `src: Front-end specification, Space, radius, elevation and blur`
- [ ] `C-FE-39` `ui` Resting panes use the card shadow with floating instruments using a deeper head-up shadow. `src: Front-end specification, Space, radius, elevation and blur`
- [ ] `C-FE-40` `ui` The selected launcher row glows blue. `src: Front-end specification, Space, radius, elevation and blur`
- [ ] `C-FE-41` `ui` The navigation bar carries the heaviest blur on the site. `src: Front-end specification, Space, radius, elevation and blur`
- [ ] `C-FE-42` `ui` The page ground shows a diagonal white sheen over warm white with pale blue radial washes. `src: Front-end specification, The signature gradients`
- [ ] `C-FE-43` `ui` Command surfaces share a white sheen over teal with blue radials. `src: Front-end specification, The signature gradients`
- [ ] `C-FE-44` `ui` The page-transition curtain carries a diagonal white band over a cool vertical ramp. `src: Front-end specification, The signature gradients`
- [ ] `C-FE-45` `ui` The focus ring offset matches the surface behind the control. `src: Front-end specification, Focus and selection`
- [ ] `C-FE-46` `ui` Icons are inline strokes in the current text colour. `src: Front-end specification, Iconography`
- [ ] `C-FE-47` `ui` Icons inside controls stay square without stretching. `src: Front-end specification, Iconography`
- [ ] `C-FE-48` `constraint` Decorative icons inside labelled controls are hidden from assistive technology. `src: Front-end specification, Iconography`
- [ ] `C-FE-49` `constraint` A meaningful icon always has visible text beside the icon. `src: Front-end specification, Iconography`
- [ ] `C-FE-50` `ui` Icons follow the pinned families for actions, domain nouns, verification, navigation, status. `src: Front-end specification, Iconography`
- [ ] `C-FE-51` `ui` The wordmark is a filled blue disc holding a rounded glyph. `src: Front-end specification, Iconography`
- [ ] `C-FE-52` `ui` The navigation capsule sits centred without touching the viewport top. `src: Front-end specification, Global chrome`
- [ ] `C-FE-53` `ui` The capsule holds the wordmark, a divider, six links, a key cap, the `Join beta` pill in that order. `src: Front-end specification, Global chrome`
- [ ] `C-FE-54` `constraint` The navigation capsule never hides on scroll. `src: Front-end specification, Global chrome`
- [ ] `C-FE-55` `literal` The skip link reads `Skip to content`. `src: Front-end specification, Global chrome`
- [ ] `C-FE-56` `capability` The skip link is the first focusable element. `src: Front-end specification, Global chrome`
- [ ] `C-FE-57` `capability` The skip link moves focus into the main landmark. `src: Front-end specification, Global chrome`
- [ ] `C-FE-58` `ui` The skip link stays above the viewport until focused. `src: Front-end specification, Global chrome`
- [ ] `C-FE-59` `capability` The small-width menu opens as a dialog. `src: Front-end specification, Global chrome`
- [ ] `C-FE-60` `capability` The small-width menu traps focus. `src: Front-end specification, Global chrome`
- [ ] `C-FE-61` `capability` Escape closes the small-width menu, returning focus to the menu button. `src: Front-end specification, Global chrome`
- [ ] `C-FE-62` `capability` The small-width menu locks page scroll. `src: Front-end specification, Global chrome`
- [ ] `C-FE-63` `capability` The page behind the open small-width menu is inert. `src: Front-end specification, Global chrome`
- [ ] `C-FE-64` `ui` The small-width menu rises into place, then leaves rising a shorter distance. `src: Front-end specification, Global chrome`
- [ ] `C-FE-65` `ui` The footer shows four columns at the widest width, collapsing to two, then one. `src: Front-end specification, Global chrome`
- [ ] `C-FE-66` `literal` The footer Product column lists Features, Workflow, Beta, Use cases, Changelog, Roadmap. `src: Front-end specification, Global chrome`
- [ ] `C-FE-67` `literal` The footer Resources column lists FAQ, Blog, Templates, Version history, Join beta. `src: Front-end specification, Global chrome`
- [ ] `C-FE-68` `literal` The footer Company column lists Contact, Privacy, Terms, Press. `src: Front-end specification, Global chrome`
- [ ] `C-FE-69` `capability` The footer Templates with Version history items link to the matching acquisition pages. `src: Front-end specification, Global chrome`
- [ ] `C-FE-70` `literal` The footer base line shows `Lumen Prompt is not affiliated with Northgate, Bellweather or Halcyon.` `src: Front-end specification, Global chrome`
- [ ] `C-FE-71` `literal` The disclaimer renders at no less than `12px`. `src: Front-end specification, Global chrome`
- [ ] `C-FE-72` `ui` A pale curtain sweeps across the page on each route change. `src: Front-end specification, Global chrome`
- [ ] `C-FE-73` `capability` After a route change the incoming main landmark receives focus. `src: Front-end specification, Global chrome`
- [ ] `C-FE-74` `ui` Pointer movement uses the frost curve with arrivals using frost settle. `src: Front-end specification, Motion language`
- [ ] `C-FE-75` `ui` Hover, colour, border, shadow changes use the fast duration. `src: Front-end specification, Motion language`
- [ ] `C-FE-76` `ui` The two blinking carets never blink in lockstep. `src: Front-end specification, Motion language`
- [ ] `C-FE-77` `ui` The headline key caps drop in from above. `src: Front-end specification, Motion language`
- [ ] `C-FE-78` `ui` The launcher panel arrives from below. `src: Front-end specification, Motion language`
- [ ] `C-FE-79` `ui` The launcher panel rocks gently on a loop. `src: Front-end specification, Motion language`
- [ ] `C-FE-80` `ui` A specular band sweeps across panes. `src: Front-end specification, Motion language`
- [ ] `C-FE-81` `constraint` Only one sweep runs in a viewport at a time. `src: Front-end specification, Motion language`
- [ ] `C-FE-82` `constraint` A loop stops once its element leaves the viewport. `src: Front-end specification, Motion language`
- [ ] `C-FE-83` `ui` Section entrances stagger their children, capped at six. `src: Front-end specification, Motion language`
- [ ] `C-FE-84` `capability` The hero headline, sub-headline, both actions, three chips stay visible with scripts disabled. `src: Front-end specification, Motion language`
- [ ] `C-FE-85` `capability` End, Home, Space keep paging the home page. `src: Front-end specification, Scroll and page transitions`
- [ ] `C-FE-86` `capability` Back navigation restores the earlier scroll position. `src: Front-end specification, Scroll and page transitions`
- [ ] `C-FE-87` `capability` Scrolling inside the history ledger never scrolls the page. `src: Front-end specification, Scroll and page transitions`
- [ ] `C-FE-88` `ui` The workflow connector draws with scroll, lighting each step as the tip passes. `src: Front-end specification, Scroll and page transitions`
- [ ] `C-FE-89` `ui` The hero instrument shows three tilted layers with the back layer desaturated. `src: Front-end specification, Scroll and page transitions`
- [ ] `C-FE-90` `ui` The palette with the small-width menu sit above every other layer. `src: Front-end specification, Scroll and page transitions`
- [ ] `C-FE-91` `literal` The palette Blueprints group lists Client brief summary, Code review checklist, Research synthesis, Meeting follow-up, Release notes draft. `src: Front-end specification, Command palette`
- [ ] `C-FE-92` `literal` The palette Blueprint categories read WRITING, ENGINEERING, RESEARCH, OPERATIONS, PRODUCT. `src: Front-end specification, Command palette`
- [ ] `C-FE-93` `ui` Palette Blueprint bodies show double-brace variables. `src: Front-end specification, Command palette`
- [ ] `C-FE-94` `ui` The launcher instrument with the library mockup show the same five Blueprints. `src: Front-end specification, Command palette`
- [ ] `C-FE-95` `literal` The palette destinations group lists seventeen entries, among them `Release notes 0.2.3`. `src: Front-end specification, Command palette`
- [ ] `C-FE-96` `capability` The palette input is a combobox with list autocompletion. `src: Front-end specification, Command palette`
- [ ] `C-FE-97` `capability` The palette input sets `aria-expanded`, `aria-controls`, `aria-activedescendant`. `src: Front-end specification, Command palette`
- [ ] `C-FE-98` `capability` The first Blueprint is the initial active palette option. `src: Front-end specification, Command palette`
- [ ] `C-FE-99` `capability` Spellcheck with autocomplete are off on the palette input. `src: Front-end specification, Command palette`
- [ ] `C-FE-100` `capability` The palette dialog carries a visually hidden title naming the dialog. `src: Front-end specification, Command palette`
- [ ] `C-FE-101` `capability` The navigation key cap opens the palette. `src: Front-end specification, Command palette`
- [ ] `C-FE-102` `capability` A forward slash opens the palette when focus sits outside any field. `src: Front-end specification, Command palette`
- [ ] `C-FE-103` `constraint` A forward slash typed inside a text field never opens the palette. `src: Front-end specification, Command palette`
- [ ] `C-FE-104` `capability` Up with Down move the palette selection, wrapping at both ends. `src: Front-end specification, Command palette`
- [ ] `C-FE-105` `capability` Escape closes the palette. `src: Front-end specification, Command palette`
- [ ] `C-FE-106` `capability` Tab stays trapped inside the palette. `src: Front-end specification, Command palette`
- [ ] `C-FE-107` `literal` The palette footer hint uses the verb `Inject`. `src: Front-end specification, Command palette`
- [ ] `C-FE-108` `capability` Activating a palette Blueprint scrolls to the matching home section. `src: Front-end specification, Command palette`
- [ ] `C-FE-109` `constraint` Activating a palette Blueprint sends nothing anywhere. `src: Front-end specification, Command palette`
- [ ] `C-FE-110` `capability` Within each group, palette search ranks an exact prefix above a word prefix. `src: Front-end specification, Command palette`
- [ ] `C-FE-111` `literal` Palette search wraps each matched run in a `<mark>` element. `src: Front-end specification, Command palette`
- [ ] `C-FE-112` `capability` Palette search matches Blueprint categories with Blueprint bodies. `src: Front-end specification, Command palette`
- [ ] `C-FE-113` `capability` An empty palette query lists every entry in the pinned order. `src: Front-end specification, Command palette`
- [ ] `C-FE-114` `capability` A palette query with no matches offers `/download` with `/contact`. `src: Front-end specification, Command palette`
- [ ] `C-FE-115` `capability` An open palette makes the page behind the palette inert. `src: Front-end specification, Command palette`
- [ ] `C-FE-116` `capability` Closing the palette returns focus to the trigger. `src: Front-end specification, Command palette`
- [ ] `C-FE-117` `capability` The first palette shortcut press after load opens the palette. `src: Front-end specification, Command palette`
- [ ] `C-FE-118` `capability` The small-width menu carries a labelled search entry. `src: Front-end specification, Command palette`
- [ ] `C-FE-119` `capability` Every palette destination is reachable from the site's links without scripting. `src: Front-end specification, Command palette`
- [ ] `C-FE-120` `ui` The seven instruments are built from markup rather than images. `src: Front-end specification, The instrument system`
- [ ] `C-FE-121` `ui` Every instrument with plausible content carries a demonstration-data label. `src: Front-end specification, The instrument system`
- [ ] `C-FE-122` `literal` The history ledger carries the label `Demonstration data`. `src: Front-end specification, Home`
- [ ] `C-FE-123` `ui` Interactive instruments respond to the keyboard. `src: Front-end specification, The instrument system`
- [ ] `C-FE-124` `ui` Every instrument stays legible as a still image. `src: Front-end specification, The instrument system`
- [ ] `C-FE-125` `literal` `Try the hotkey` opens the hotkey demonstration dialog. `src: Front-end specification, The instrument system`
- [ ] `C-FE-126` `capability` Cmd Shift Space or Ctrl Shift Space opens the hotkey demonstration. `src: Front-end specification, The instrument system`
- [ ] `C-FE-127` `ui` Typing in the hotkey demonstration filters the five Blueprints. `src: Front-end specification, The instrument system`
- [ ] `C-FE-128` `ui` Enter in the hotkey demonstration renders the finished prompt with blanks filled. `src: Front-end specification, The instrument system`
- [ ] `C-FE-129` `constraint` The hotkey demonstration opens only in a window both wide enough, tall enough. `src: Front-end specification, The instrument system`
- [ ] `C-FE-130` `constraint` The hotkey demonstration writes to the clipboard only when `Copy` is pressed. `src: Front-end specification, The instrument system`
- [ ] `C-FE-131` `capability` The hotkey demonstration announces the result count politely. `src: Front-end specification, The instrument system`
- [ ] `C-FE-132` `capability` The hotkey demonstration traps focus, returning focus to the trigger on close. `src: Front-end specification, The instrument system`
- [ ] `C-FE-133` `ui` Switching a context tray file updates the counts beneath the tray. `src: Front-end specification, The instrument system`
- [ ] `C-FE-134` `ui` Switching a context tray file off dims the matching token in the prompt body. `src: Front-end specification, The instrument system`
- [ ] `C-FE-135` `ui` A docking chip appears to travel continuously between lists. `src: Front-end specification, The instrument system`
- [ ] `C-FE-136` `ui` The dock target shows a receptive state before the drop. `src: Front-end specification, The instrument system`
- [ ] `C-FE-137` `ui` The window mockup shows title-bar dots, a sidebar, a capsule search field, rows, a detail strip. `src: Front-end specification, The instrument system`
- [ ] `C-FE-138` `ui` Hovering a window mockup row updates the detail strip. `src: Front-end specification, The instrument system`
- [ ] `C-FE-139` `literal` The home route shows the fourteen pinned section headings in order. `src: Front-end specification, Home`
- [ ] `C-FE-140` `literal` The home route shows the pinned eyebrows above the section headings. `src: Front-end specification, Home`
- [ ] `C-FE-141` `constraint` Home eyebrows are never marked up as headings. `src: Front-end specification, Home`
- [ ] `C-FE-142` `ui` Section one's eyebrow is a pill with a live green status dot. `src: Front-end specification, Home`
- [ ] `C-FE-143` `literal` The home route carries the section anchors `#features`, `#workflow`, `#pricing`, `#help`. `src: Front-end specification, Home`
- [ ] `C-FE-144` `ui` A hand-drawn blue underline sits beneath the headline's final word. `src: Front-end specification, Home`
- [ ] `C-FE-145` `literal` The hero shows the key caps `Cmd`, `Shift`, `Space`. `src: Front-end specification, Home`
- [ ] `C-FE-146` `literal` The hero shows the pinned sub-headline about keeping reused prompts one keystroke away. `src: Front-end specification, Home`
- [ ] `C-FE-147` `literal` The hero note reads `Free during beta. No card required.` `src: Front-end specification, Home`
- [ ] `C-FE-148` `literal` The hero chips read `Local-first`, `Signed builds`, `No subscription`. `src: Front-end specification, Home`
- [ ] `C-FE-149` `ui` The primary hero action stacks `FREE DURING BETA` above `Join beta` beside a mail icon. `src: Front-end specification, Home`
- [ ] `C-FE-150` `ui` The outlined `Try the hotkey` action ends in a key-cap chip. `src: Front-end specification, Home`
- [ ] `C-FE-151` `ui` The hero launcher floats tilted with three key caps linked to the panel by a thin connector. `src: Front-end specification, Home`
- [ ] `C-FE-152` `ui` Without motion the hero launcher rests still with the first row selected. `src: Front-end specification, Home`
- [ ] `C-FE-153` `ui` Pointing at a launcher row selects the row, updating the context strip. `src: Front-end specification, Home`
- [ ] `C-FE-154` `literal` The workflow runner names `Client brief summary` with the claim `No context switch`. `src: Front-end specification, Home`
- [ ] `C-FE-155` `literal` The workflow output card is labelled `Finished prompt`. `src: Front-end specification, Home`
- [ ] `C-FE-156` `literal` The three product-surface sections carry their pinned bullets. `src: Front-end specification, Home`
- [ ] `C-FE-157` `ui` The time theatre shows four versions, each with a number, a state word, a relative date. `src: Front-end specification, Home`
- [ ] `C-FE-158` `ui` The scrubber thumb demonstrates itself until touched. `src: Front-end specification, Home`
- [ ] `C-FE-159` `ui` The difference panel prefixes lines with a plus or a minus in text. `src: Front-end specification, Home`
- [ ] `C-FE-160` `capability` The version scrubber is a range control operated by arrows, Home, End. `src: Front-end specification, Home`
- [ ] `C-FE-161` `literal` The version scrubber announces a version label such as `Version 3, starred`. `src: Front-end specification, Home`
- [ ] `C-FE-162` `ui` The packet section shows three numbered cards under a header card. `src: Front-end specification, Home`
- [ ] `C-FE-163` `ui` Ledger timestamps render in monospace with aligned figures. `src: Front-end specification, Home`
- [ ] `C-FE-164` `literal` The ledger shows six rows naming target apps with `Quick copy` or a file count. `src: Front-end specification, Home`
- [ ] `C-FE-165` `literal` The beta note is signed by Devrim with `See the roadmap` linking to `/roadmap`. `src: Front-end specification, Home`
- [ ] `C-FE-166` `ui` The local-first section shows four guarantees beside a boundary diagram. `src: Front-end specification, Home`
- [ ] `C-FE-167` `literal` The comparison is a table with a caption, column headers, row headers. `src: Front-end specification, Home`
- [ ] `C-FE-168` `literal` The comparison table carries the seven pinned features with the three qualified cells. `src: Front-end specification, Home`
- [ ] `C-FE-169` `capability` Comparison marks carry present or absent in their accessible names. `src: Front-end specification, Home`
- [ ] `C-FE-170` `literal` The comparison footnote reads `Comparison checked on 2026-08-15 against each tool's public documentation.` `src: Front-end specification, Home`
- [ ] `C-FE-171` `capability` Below the comparison breakpoint each competing tool shows as a card. `src: Front-end specification, Home`
- [ ] `C-FE-172` `capability` No two comparison tables share a caption. `src: Front-end specification, Home`
- [ ] `C-FE-173` `ui` The Lumen Prompt column stays visible as the table scrolls at intermediate widths. `src: Front-end specification, Home`
- [ ] `C-FE-174` `ui` Pricing shows three cards with the founder card emphasised. `src: Front-end specification, Home`
- [ ] `C-FE-175` `literal` The Free card shows `$0` with the post-1.0 limits of 25 Blueprints, 3 contexts, 30 days of Injection History. `src: Front-end specification, Home`
- [ ] `C-FE-176` `literal` The founder card shows `About the cost of 15 billable minutes` with `Every 1.x update, for life`. `src: Front-end specification, Home`
- [ ] `C-FE-177` `literal` The founder card lists the four pinned bullets. `src: Front-end specification, Home`
- [ ] `C-FE-178` `literal` The founder card shows `Standard licence at 1.0: $49`. `src: Front-end specification, Home`
- [ ] `C-FE-179` `literal` The founder card action `Claim a founder place` leads to `/download`. `src: Front-end specification, Home`
- [ ] `C-FE-180` `literal` The founder card notes `Checkout is not open yet. Registering holds your place.` `src: Front-end specification, Home`
- [ ] `C-FE-181` `literal` The 1.0 card lists `Standard licence` at `$49`, `Extended licence` at `$79`, `Update renewal` at `$19`. `src: Front-end specification, Home`
- [ ] `C-FE-182` `literal` The 1.0 card states `Requires macOS 26.1 or later`. `src: Front-end specification, Home`
- [ ] `C-FE-183` `capability` The founder card renders the live cohort state from the allocation endpoint. `src: Front-end specification, Home`
- [ ] `C-FE-184` `literal` With fewer than 500 places held the founder card shows `$29` above `N of 500 founder places left at $29`. `src: Front-end specification, Home`
- [ ] `C-FE-185` `capability` With 500 to 999 places held the founder card shows `$39` with claimed plus left counts. `src: Front-end specification, Home`
- [ ] `C-FE-186` `literal` With every place held the founder card shows `Founder places are all claimed` with the action `Join the beta`. `src: Front-end specification, Home`
- [ ] `C-FE-187` `constraint` Nothing on the site implies a subscription. `src: Front-end specification, Home`
- [ ] `C-FE-188` `literal` The help panel lists the eight pinned questions in order. `src: Front-end specification, Home`
- [ ] `C-FE-189` `literal` The help panel shows the chips `Privacy`, `Pricing`, `Beta`, `Platform`. `src: Front-end specification, Home`
- [ ] `C-FE-190` `ui` The help panel is framed as a console with a title bar with an `Esc` chip. `src: Front-end specification, Home`
- [ ] `C-FE-191` `capability` Each help trigger is a button inside a heading carrying an expanded state. `src: Front-end specification, Home`
- [ ] `C-FE-192` `ui` Help items animate to their measured content height. `src: Front-end specification, Home`
- [ ] `C-FE-193` `capability` Several help items stay open at once. `src: Front-end specification, Home`
- [ ] `C-FE-194` `capability` Help category chips filter without navigating, keeping open items open. `src: Front-end specification, Home`
- [ ] `C-FE-195` `literal` Help items open when linked as `#faq-01` to `#faq-08`. `src: Front-end specification, Home`
- [ ] `C-FE-196` `capability` All eight help answers ship in the delivered markup. `src: Front-end specification, Home`
- [ ] `C-FE-197` `capability` Help answer 08 names Chatwell, Cadence, Vertan, Caret. `src: Front-end specification, Home`
- [ ] `C-FE-198` `literal` The closing section states `Requires macOS 26.1 or later.` above a four-row beta access card. `src: Front-end specification, Home`
- [ ] `C-FE-199` `literal` `/download` shows the chips `Free during beta`, `No card required`, `Open registration`, `Founder pricing before 1.0`. `src: Front-end specification, Join the beta`
- [ ] `C-FE-200` `literal` The distribution panel is headed `Official distribution`. `src: Front-end specification, Join the beta`
- [ ] `C-FE-201` `capability` The distribution panel shows the current stable version with build from the registry. `src: Front-end specification, Join the beta`
- [ ] `C-FE-202` `literal` The distribution panel shows the pinned verification claim. `src: Front-end specification, Join the beta`
- [ ] `C-FE-203` `literal` The distribution panel shows `/downloads/latest` with `/appcast.xml`. `src: Front-end specification, Join the beta`
- [ ] `C-FE-204` `literal` The distribution panel requirement reads `macOS 26.1 or later` for the current release. `src: Front-end specification, Join the beta`
- [ ] `C-FE-205` `capability` The distribution panel shows a truncated checksum whose `Copy` control copies the full value. `src: Front-end specification, Join the beta`
- [ ] `C-FE-206` `capability` The distribution panel links to `/changelog`. `src: Front-end specification, Join the beta`
- [ ] `C-FE-207` `capability` The explainer is a numbered list of exactly four steps. `src: Front-end specification, Join the beta`
- [ ] `C-FE-208` `capability` The trap field sits off screen, removed from the tab order, hidden from assistive technology. `src: Front-end specification, Join the beta`
- [ ] `C-FE-209` `capability` The email field carries an email type, an email autofill hint, spellcheck off. `src: Front-end specification, Join the beta`
- [ ] `C-FE-210` `literal` The name field shows the placeholder `Optional`. `src: Front-end specification, Join the beta`
- [ ] `C-FE-211` `literal` The platform select offers `Not sure`, `macOS 26.1`, `macOS 26.2`, `macOS 26.3`, `macOS 27`. `src: Front-end specification, Join the beta`
- [ ] `C-FE-212` `literal` The role field shows the pinned placeholder naming three example roles. `src: Front-end specification, Join the beta`
- [ ] `C-FE-213` `literal` The primary use field shows the pinned placeholder naming three example uses. `src: Front-end specification, Join the beta`
- [ ] `C-FE-214` `literal` The consent checkbox carries the pinned consent sentence. `src: Front-end specification, Join the beta`
- [ ] `C-FE-215` `ui` The submit button reads `Join the beta`, filled blue, full width at narrow widths. `src: Front-end specification, Join the beta`
- [ ] `C-FE-216` `literal` The form shows `One email with your link. No newsletter.` `src: Front-end specification, Join the beta`
- [ ] `C-FE-217` `literal` The form shows the pinned fallback note about builds not yet ready. `src: Front-end specification, Join the beta`
- [ ] `C-FE-218` `capability` The form markup marks email with consent as required. `src: Front-end specification, Join the beta`
- [ ] `C-FE-219` `literal` A missing email shows `Enter an email address so we can send your access link.` `src: Front-end specification, Join the beta`
- [ ] `C-FE-220` `literal` A malformed email shows the pinned probable-typo message. `src: Front-end specification, Join the beta`
- [ ] `C-FE-221` `literal` A missing consent shows `Confirm you want the access link.` `src: Front-end specification, Join the beta`
- [ ] `C-FE-222` `ui` Errors render beneath each invalid field. `src: Front-end specification, Join the beta`
- [ ] `C-FE-223` `ui` An error summary at the top links to each invalid field. `src: Front-end specification, Join the beta`
- [ ] `C-FE-224` `capability` The error summary takes focus on a failed submission. `src: Front-end specification, Join the beta`
- [ ] `C-FE-225` `capability` Each invalid control is marked invalid, pointing at its message. `src: Front-end specification, Join the beta`
- [ ] `C-FE-226` `ui` Error text uses the darker danger colour beside an icon. `src: Front-end specification, Join the beta`
- [ ] `C-FE-227` `capability` Errors clear as the visitor types. `src: Front-end specification, Join the beta`
- [ ] `C-FE-228` `capability` Entered values survive a failed submission. `src: Front-end specification, Join the beta`
- [ ] `C-FE-229` `ui` The success panel shows the cohort as a whole, never the visitor's own place. `src: Front-end specification, Join the beta`
- [ ] `C-FE-230` `ui` The success panel looks identical for a first registration or a repeat. `src: Front-end specification, Join the beta`
- [ ] `C-FE-231` `constraint` A double submission is absorbed rather than duplicated. `src: Front-end specification, Join the beta`
- [ ] `C-FE-232` `capability` Submitting offline shows a message with every value preserved. `src: Front-end specification, Join the beta`
- [ ] `C-FE-233` `literal` `/use-cases` shows the five numbered cards with the pinned eyebrows, titles, routes. `src: Front-end specification, Use cases`
- [ ] `C-FE-234` `ui` Each use-case card is wholly a link led by a large monospace numeral. `src: Front-end specification, Use cases`
- [ ] `C-FE-235` `capability` The radial diagram nodes link to the five use-case pages. `src: Front-end specification, Use cases`
- [ ] `C-FE-236` `ui` The radial diagram shows a core with a teal-blue bloom, glinting nodes, a scan fading toward the edges. `src: Front-end specification, Use cases`
- [ ] `C-FE-237` `literal` The radial diagram labels read `Client briefs`, `Code reviews`, `Research notes`. `src: Front-end specification, Use cases`
- [ ] `C-FE-238` `literal` Each use-case page shows its pinned eyebrow with its pinned first-level heading. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-239` `constraint` Each use-case page has exactly one first-level heading. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-240` `ui` Use-case pages carry the pinned blocks in order. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-241` `literal` The use-case contrast block columns read `Without Lumen Prompt` with `With Lumen Prompt`. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-242` `literal` Use-case pages carry the pinned synthetic-data disclaimer. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-243` `literal` The use-case mockup carries the label `Demonstration data`. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-244` `constraint` The `Related use cases` section never links to the page itself. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-245` `literal` Each use-case page carries `BreadcrumbList` with `FAQPage` structured data. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-246` `literal` `/` with `/download` carry `SoftwareApplication` structured data. `src: Front-end specification, Use-case pages`
- [ ] `C-FE-247` `literal` `/changelog` shows the pinned sub-heading about one source of truth. `src: Front-end specification, Changelog`
- [ ] `C-FE-248` `capability` The current stable block shows the version, summary, full checksum, stored download count. `src: Front-end specification, Changelog`
- [ ] `C-FE-249` `capability` The current stable block carries a release film with a poster image. `src: Front-end specification, Changelog`
- [ ] `C-FE-250` `literal` The current stable block offers `Download` with `Read the notes`. `src: Front-end specification, Changelog`
- [ ] `C-FE-251` `capability` Each earlier release shows version, date, size, truncated checksum, summary, notes link. `src: Front-end specification, Changelog`
- [ ] `C-FE-252` `literal` Release notes show the note `Lumen Prompt is free during the beta.` `src: Front-end specification, Release notes`
- [ ] `C-FE-253` `literal` Release notes sections run in the pinned order from `What is new` through `Known issues` to `Reporting problems`. `src: Front-end specification, Release notes`
- [ ] `C-FE-254` `capability` Release notes render completely without scripts. `src: Front-end specification, Release notes`
- [ ] `C-FE-255` `ui` Release notes fit a small panel at a narrow width. `src: Front-end specification, Release notes`
- [ ] `C-FE-256` `literal` `/roadmap` shows the pinned caveat about order changing with beta feedback. `src: Front-end specification, Roadmap`
- [ ] `C-FE-257` `literal` The roadmap shows Now, Next, Later with the eleven pinned items. `src: Front-end specification, Roadmap`
- [ ] `C-FE-258` `constraint` The roadmap shows no dates, percentages or progress bars. `src: Front-end specification, Roadmap`
- [ ] `C-FE-259` `capability` The variable-memory roadmap item states per-Blueprint scoping. `src: Front-end specification, Roadmap`
- [ ] `C-FE-260` `capability` The sharing roadmap item states sharing needs no account layer or shared server. `src: Front-end specification, Roadmap`
- [ ] `C-FE-261` `literal` `/blog` lists `Stop rewriting your best prompt` above `Prompts are work product`. `src: Front-end specification, Blog`
- [ ] `C-FE-262` `capability` Each blog card shows a category, a date, a reading time, a title, a summary. `src: Front-end specification, Blog`
- [ ] `C-FE-263` `capability` Reading time equals the article body word count divided by 200, rounded up. `src: Front-end specification, Blog`
- [ ] `C-FE-264` `capability` An article page shows the title, date, reading time, prose, related articles. `src: Front-end specification, Blog`
- [ ] `C-FE-265` `constraint` Blog routes carry no instrument or mockup. `src: Front-end specification, Blog`
- [ ] `C-FE-266` `literal` `/press` offers `Download the press kit (48 MB)` linking to the pinned archive. `src: Front-end specification, Press`
- [ ] `C-FE-267` `capability` The press fact sheet shows the seven pinned rows. `src: Front-end specification, Press`
- [ ] `C-FE-268` `capability` `/press` shows twenty-three captioned captures. `src: Front-end specification, Press`
- [ ] `C-FE-269` `capability` Each capture caption doubles as the capture's alternative text. `src: Front-end specification, Press`
- [ ] `C-FE-270` `capability` Each capture carries explicit dimensions. `src: Front-end specification, Press`
- [ ] `C-FE-271` `capability` A `Light` or `Dark` control switches the capture variants. `src: Front-end specification, Press`
- [ ] `C-FE-272` `capability` The two motion loops are muted with a poster, without preloading. `src: Front-end specification, Press`
- [ ] `C-FE-273` `constraint` The motion loops never autoplay under reduced motion. `src: Front-end specification, Press`
- [ ] `C-FE-274` `capability` Press images below the fold load lazily. `src: Front-end specification, Press`
- [ ] `C-FE-275` `literal` The usage guidelines are two lists headed `You may` with `You may not` carrying the pinned items. `src: Front-end specification, Press`
- [ ] `C-FE-276` `literal` `/contact` shows the pinned one-address sentence. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-277` `literal` `/contact` shows `hello@example.com` as selectable text with a mail link. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-278` `literal` The contact mail link carries the subject `Lumen Prompt support` with blanks `macOS version:` plus `Lumen Prompt version:`. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-279` `capability` Privacy with terms show a generated table of contents. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-280` `literal` Privacy headings carry the pinned identifiers. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-281` `literal` Terms headings carry the pinned identifiers. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-282` `capability` Privacy with terms print without backgrounds. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-283` `capability` The privacy page states the fourteen-day session, no analytics, the three processors. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-284` `capability` The privacy `Your rights` section links to `/legal/data-request`. `src: Front-end specification, Contact, Privacy and Terms`
- [ ] `C-FE-285` `constraint` Pages load nothing from another origin. `src: Front-end specification, Access and error pages; Constraints bullet 8`
- [ ] `C-FE-286` `constraint` The access page never forwards on its own under reduced motion. `src: Front-end specification, Access and error pages`
- [ ] `C-FE-287` `constraint` The site's demonstrations never contradict the application description. `src: Front-end specification, The Mac application the pages describe`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app exposes no admin area beyond `/operator`. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` Visitors see no account signup, password or profile area. `src: Constraints bullet 4`
- [ ] `C-CN-03` `constraint` No public route offers a file upload. `src: Constraints bullet 11`
- [ ] `C-CN-04` `constraint` The app stays responsive with every one of the 1000 founder places held. `src: Constraints bullet 12`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app serves container port `4173` behind the `${APP_PUBLIC_PORT}:4173` mapping. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under `/api`. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-05` `contract` The server keeps running after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-06` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-07` `data` API responses use the exact field names of the API shapes table. `src: Deployment contract, API shapes`
- [ ] `C-DC-08` `data` List endpoints return a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-09` `contract` Invalid or unauthorized calls return a client error, never a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-10` `constraint` A founder place never exists without a matching Kill Bill account. `src: Deployment contract, No mocks`
- [ ] `C-DC-11` `constraint` The access email is delivered through Mailpit rather than written to a log. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `1000` | The founder cohort holds exactly 1000 places | C-CF-01 | Core features, Founder places rule 1 |
| `1` | Places 1 to 500 sit in tier 1 at 2900 | C-CF-02 | Core features, Founder places rule 1 |
| `500` | Places 1 to 500 sit in tier 1 at 2900 | C-CF-02 | Core features, Founder places rule 1 |
| `2900` | Places 1 to 500 sit in tier 1 at 2900 | C-CF-02 | Core features, Founder places rule 1 |
| `501` | Places 501 to 1000 sit in tier 2 at 3900 | C-CF-03 | Core features, Founder places rule 1 |
| `1000` | Places 501 to 1000 sit in tier 2 at 3900 | C-CF-03 | Core features, Founder places rule 1 |
| `2` | Places 501 to 1000 sit in tier 2 at 3900 | C-CF-03 | Core features, Founder places rule 1 |
| `3900` | Places 501 to 1000 sit in tier 2 at 3900 | C-CF-03 | Core features, Founder places rule 1 |
| `usd` | Founder prices use currency usd | C-CF-04 | Core features, Founder places rule 1 |
| `closed` | The cohort state reads closed once every place is held | C-CF-09 | Core features, Founder places rule 4 |
| `lumen-founder-` | The billing account externalKey is lumen-founder- plus the place pa... | C-CF-15 | Core features, Founder places rule 6 |
| `USD` | The billing account carries currency USD | C-CF-16 | Core features, Founder places rule 6 |
| `US` | The billing account carries country US | C-CF-17 | Core features, Founder places rule 6 |
| `current_tier` | The allocation current_tier reads null once the cohort is closed | C-CF-23 | Core features, Founder places rule 7 |
| `null` | The allocation current_tier reads null once the cohort is closed | C-CF-23 | Core features, Founder places rule 7 |
| `254` | The server rejects an email longer than 254 characters | C-CF-33 | Core features, Beta registration rule 4 |
| `name` | The server rejects a name longer than 120 characters | C-CF-35 | Core features, Beta registration rule 4 |
| `120` | The server rejects a name longer than 120 characters | C-CF-35 | Core features, Beta registration rule 4 |
| `role` | The server rejects a role longer than 120 characters | C-CF-36 | Core features, Beta registration rule 4 |
| `120` | The server rejects a role longer than 120 characters | C-CF-36 | Core features, Beta registration rule 4 |
| `primary_use` | The server rejects a primary_use longer than 240 characters | C-CF-37 | Core features, Beta registration rule 4 |
| `240` | The server rejects a primary_use longer than 240 characters | C-CF-37 | Core features, Beta registration rule 4 |
| `platform_version` | The server stores a platform_version outside 26.1, 26.2, 26.3, 27 a... | C-CF-41 | Core features, Beta registration rule 5 |
| `26.1` | The server stores a platform_version outside 26.1, 26.2, 26.3, 27 a... | C-CF-41 | Core features, Beta registration rule 5 |
| `26.2` | The server stores a platform_version outside 26.1, 26.2, 26.3, 27 a... | C-CF-41 | Core features, Beta registration rule 5 |
| `26.3` | The server stores a platform_version outside 26.1, 26.2, 26.3, 27 a... | C-CF-41 | Core features, Beta registration rule 5 |
| `27` | The server stores a platform_version outside 26.1, 26.2, 26.3, 27 a... | C-CF-41 | Core features, Beta registration rule 5 |
| `status` | A successful registration returns status set to sent | C-CF-42 | Core features, Beta registration rule 6 |
| `sent` | A successful registration returns status set to sent | C-CF-42 | Core features, Beta registration rule 6 |
| `Check your inbox for your access link.` | A successful registration returns the message Check your inbox for... | C-CF-43 | Core features, Beta registration rule 6 |
| `3` | An address receives at most 3 access emails in any rolling hour | C-CF-50 | Core features, Beta registration rule 8 |
| `challenge_status` | Each stored registration records challenge_status as not_run | C-CF-55 | Core features, Beta registration rule 9 |
| `not_run` | Each stored registration records challenge_status as not_run | C-CF-55 | Core features, Beta registration rule 9 |
| `Your Lumen Prompt beta access link` | The access email subject is Your Lumen Prompt beta access link | C-CF-58 | Core features, Access links rule 1 |
| `<APP_PUBLIC_URL>/beta/access/<token>` | The first plain-text line of the access email is the link <APP_PUBL... | C-CF-59 | Core features, Access links rule 1 |
| `You are registered for the Lumen Prompt beta.` | A first registration email's second line reads You are registered f... | C-CF-60 | Core features, Access links rule 1 |
| `Your founder place:` | An access email names a held founder place after Your founder place: | C-CF-62 | Core features, Access links rule 1 |
| `32` | A token holds at least 32 characters drawn from letters, digits, hy... | C-CF-63 | Core features, Access links rule 2 |
| `5` | A link opens at most 5 times | C-CF-65 | Core features, Access links rule 3 |
| `14` | A link lives 14 days | C-CF-66 | Core features, Access links rule 3 |
| `superseded` | A new link marks older active links of the same address superseded | C-CF-67 | Core features, Access links rule 3 |
| `30` | The click log keeps at most one click per link per 30-minute window | C-CF-69 | Core features, Access links rule 4 |
| `Your access link is confirmed` | A live link shows Your access link is confirmed | C-CF-72 | Core features, Access links rule 4 |
| `Download for Mac` | A live link page offers a Download for Mac control to /downloads/la... | C-CF-73 | Core features, Access links rule 4 |
| `/downloads/latest` | A live link page offers a Download for Mac control to /downloads/la... | C-CF-73 | Core features, Access links rule 4 |
| `If that address is registered, a fresh access link is on its way.` | The resend endpoint always answers If that address is registered, a... | C-CF-86 | Core features, Access links rule 7 |
| `billing_account` | billing_account reads ready only once the Kill Bill account for the... | C-CF-90 | Core features, Access links rule 8 |
| `ready` | billing_account reads ready only once the Kill Bill account for the... | C-CF-90 | Core features, Access links rule 8 |
| `billing_account` | billing_account reads pending until the Kill Bill account for the p... | C-CF-91 | Core features, Access links rule 8 |
| `pending` | billing_account reads pending until the Kill Bill account for the p... | C-CF-91 | Core features, Access links rule 8 |
| `0.2.3` | The seeded current stable release is 0.2.3 with build 4 | C-CF-98 | Core features, Release registry rule 2 |
| `4` | The seeded current stable release is 0.2.3 with build 4 | C-CF-98 | Core features, Release registry rule 2 |
| `/downloads/latest` | /downloads/latest carries Cache-Control: no-store | C-CF-100 | Core features, Release registry rule 3 |
| `Cache-Control: no-store` | /downloads/latest carries Cache-Control: no-store | C-CF-100 | Core features, Release registry rule 3 |
| `POST /api/checkout/founder` | POST /api/checkout/founder is rejected with checkout_not_open | C-CF-128 | Core features, Checkout rule 1 |
| `checkout_not_open` | POST /api/checkout/founder is rejected with checkout_not_open | C-CF-128 | Core features, Checkout rule 1 |
| `/checkout/founder` | /checkout/founder with /checkout/return show Founder checkout opens... | C-CF-131 | Core features, Checkout rule 1 |
| `/checkout/return` | /checkout/founder with /checkout/return show Founder checkout opens... | C-CF-131 | Core features, Checkout rule 1 |
| `Founder checkout opens at 1.0` | /checkout/founder with /checkout/return show Founder checkout opens... | C-CF-131 | Core features, Checkout rule 1 |
| `POST /api/licence/activate` | POST /api/licence/activate is rejected with licensing_not_open | C-CF-133 | Core features, Checkout rule 2 |
| `licensing_not_open` | POST /api/licence/activate is rejected with licensing_not_open | C-CF-133 | Core features, Checkout rule 2 |
| `/licence/activate` | /licence/activate shows Licence activation opens at 1.0 | C-CF-134 | Core features, Checkout rule 2 |
| `Licence activation opens at 1.0` | /licence/activate shows Licence activation opens at 1.0 | C-CF-134 | Core features, Checkout rule 2 |
| `access` | A data-request kind is one of access, export, correction, deletion | C-CF-136 | Core features, Data requests rule 1 |
| `export` | A data-request kind is one of access, export, correction, deletion | C-CF-136 | Core features, Data requests rule 1 |
| `correction` | A data-request kind is one of access, export, correction, deletion | C-CF-136 | Core features, Data requests rule 1 |
| `deletion` | A data-request kind is one of access, export, correction, deletion | C-CF-136 | Core features, Data requests rule 1 |
| `open` | A stored data request carries status open | C-CF-138 | Core features, Data requests rule 1 |
| `We will reply to that address within 30 days.` | The data-request endpoint answers We will reply to that address wit... | C-CF-139 | Core features, Data requests rule 1 |
| `/beta/status` | /beta/status without a session shows Open the link in your email to... | C-UF-30 | User flow, Entry |
| `Open the link in your email to see your status` | /beta/status without a session shows Open the link in your email to... | C-UF-30 | User flow, Entry |
| `Sign out` | The console's Sign out returns the operator to / | C-UF-34 | User flow, Entry |
| `/` | The console's Sign out returns the operator to / | C-UF-34 | User flow, Entry |
| `No registrations match` | A console search matching nothing shows No registrations match | C-UF-52 | User flow, States |
| `4.5:1` | Body text keeps a contrast of at least 4.5:1 against the composited... | C-UX-33 | UI/UX notes, Accessibility |
| `7:1` | Primary text on the page ground keeps a contrast of at least 7:1 | C-UX-34 | UI/UX notes, Accessibility |
| `X-Killbill-CreatedBy` | Kill Bill writes carry X-Killbill-CreatedBy | C-TR-06 | Technical requirements, Kill Bill |
| `GET /api/health` | GET /api/health answers 200 with status set to ok | C-TR-08 | Technical requirements, Health |
| `200` | GET /api/health answers 200 with status set to ok | C-TR-08 | Technical requirements, Health |
| `status` | GET /api/health answers 200 with status set to ok | C-TR-08 | Technical requirements, Health |
| `ok` | GET /api/health answers 200 with status set to ok | C-TR-08 | Technical requirements, Health |
| `Strict-Transport-Security: max-age=31536000; includeSubDomains` | Every response carries Strict-Transport-Security: max-age=31536000;... | C-TR-09 | Technical requirements, Security headers |
| `X-Content-Type-Options: nosniff` | Every response carries X-Content-Type-Options: nosniff | C-TR-10 | Technical requirements, Security headers |
| `Referrer-Policy: strict-origin-when-cross-origin` | Every response carries Referrer-Policy: strict-origin-when-cross-or... | C-TR-11 | Technical requirements, Security headers |
| `/robots.txt` | /robots.txt carries Disallow: /downloads/latest | C-TR-15 | Technical requirements, Crawling |
| `Disallow: /downloads/latest` | /robots.txt carries Disallow: /downloads/latest | C-TR-15 | Technical requirements, Crawling |
| `/robots.txt` | /robots.txt carries Disallow: /api/ | C-TR-16 | Technical requirements, Crawling |
| `Disallow: /api/` | /robots.txt carries Disallow: /api/ | C-TR-16 | Technical requirements, Crawling |
| `/robots.txt` | /robots.txt carries Disallow: /beta/access/ | C-TR-17 | Technical requirements, Crawling |
| `Disallow: /beta/access/` | /robots.txt carries Disallow: /beta/access/ | C-TR-17 | Technical requirements, Crawling |
| `/robots.txt` | /robots.txt carries Disallow: /checkout/ | C-TR-18 | Technical requirements, Crawling |
| `Disallow: /checkout/` | /robots.txt carries Disallow: /checkout/ | C-TR-18 | Technical requirements, Crawling |
| `/robots.txt` | /robots.txt names the sitemap on a Sitemap: line | C-TR-19 | Technical requirements, Crawling |
| `Sitemap:` | /robots.txt names the sitemap on a Sitemap: line | C-TR-19 | Technical requirements, Crawling |
| `<meta name="robots" content="noindex">` | The access route markup carries <meta name="robots" content="noindex"> | C-TR-20 | Technical requirements, Crawling |
| `Cache-Control: public, max-age=3600, stale-while-revalidate=86400` | Release notes carry Cache-Control: public, max-age=3600, stale-whil... | C-TR-23 | Technical requirements, Caching |
| `/changelog` | /changelog carries Cache-Control: no-store | C-TR-24 | Technical requirements, Caching |
| `Cache-Control: no-store` | /changelog carries Cache-Control: no-store | C-TR-24 | Technical requirements, Caching |
| `/appcast.xml` | /appcast.xml declares the xmlns:sparkle namespace http://www.andyma... | C-TR-25 | Technical requirements, Update feed format |
| `xmlns:sparkle` | /appcast.xml declares the xmlns:sparkle namespace http://www.andyma... | C-TR-25 | Technical requirements, Update feed format |
| `http://www.andymatuschak.org/xml-namespaces/sparkle` | /appcast.xml declares the xmlns:sparkle namespace http://www.andyma... | C-TR-25 | Technical requirements, Update feed format |
| `Lumen Prompt` | Each feed item title reads Lumen Prompt followed by the version | C-TR-26 | Technical requirements, Update feed format |
| `sparkle:version` | Each feed item carries sparkle:version holding the build | C-TR-27 | Technical requirements, Update feed format |
| `sparkle:shortVersionString` | Each feed item carries sparkle:shortVersionString holding the version | C-TR-28 | Technical requirements, Update feed format |
| `sparkle:minimumSystemVersion` | Each feed item carries sparkle:minimumSystemVersion holding the rel... | C-TR-29 | Technical requirements, Update feed format |
| `min_os` | Each feed item carries sparkle:minimumSystemVersion holding the rel... | C-TR-29 | Technical requirements, Update feed format |
| `sparkle:releaseNotesLink` | Each feed item carries sparkle:releaseNotesLink to the release note... | C-TR-30 | Technical requirements, Update feed format |
| `type="application/octet-stream"` | Each feed enclosure carries type="application/octet-stream" | C-TR-31 | Technical requirements, Update feed format |
| `sparkle:edSignature` | Each feed enclosure carries sparkle:edSignature | C-TR-32 | Technical requirements, Update feed format |
| `usd` | Money is stored in integer minor units with currency usd | C-DM-10 | Data model para 1 |
| `deku-demo-pw-2026` | Every seeded account signs in with the password deku-demo-pw-2026 | C-DM-11 | Data model para 2 |
| `challenge_status` | challenge_status takes one of not_run, passed, failed | C-DM-14 | Data model, registrations |
| `not_run` | challenge_status takes one of not_run, passed, failed | C-DM-14 | Data model, registrations |
| `passed` | challenge_status takes one of not_run, passed, failed | C-DM-14 | Data model, registrations |
| `failed` | challenge_status takes one of not_run, passed, failed | C-DM-14 | Data model, registrations |
| `access_links` | An access_links row carries a status of active, revoked or superseded | C-DM-19 | Data model, access_links |
| `status` | An access_links row carries a status of active, revoked or superseded | C-DM-19 | Data model, access_links |
| `active` | An access_links row carries a status of active, revoked or superseded | C-DM-19 | Data model, access_links |
| `revoked` | An access_links row carries a status of active, revoked or superseded | C-DM-19 | Data model, access_links |
| `superseded` | An access_links row carries a status of active, revoked or superseded | C-DM-19 | Data model, access_links |
| `releases` | A releases row carries a status of published or revoked | C-DM-24 | Data model, releases |
| `status` | A releases row carries a status of published or revoked | C-DM-24 | Data model, releases |
| `published` | A releases row carries a status of published or revoked | C-DM-24 | Data model, releases |
| `revoked` | A releases row carries a status of published or revoked | C-DM-24 | Data model, releases |
| `challenge_status` | Seeded registrations record consent with challenge_status set to no... | C-DM-35 | Data model, Seed data |
| `not_run` | Seeded registrations record consent with challenge_status set to no... | C-DM-35 | Data model, Seed data |
| `registrant@example.com` | Seeded place 1 belongs to registrant@example.com at tier 1 for 2900... | C-DM-36 | Data model, Seed data |
| `2900` | Seeded place 1 belongs to registrant@example.com at tier 1 for 2900... | C-DM-36 | Data model, Seed data |
| `lumen-founder-0001` | Seeded place 1 belongs to registrant@example.com at tier 1 for 2900... | C-DM-36 | Data model, Seed data |
| `seed-live-4b7d9e2a61c3f085` | Seeded link seed-live-4b7d9e2a61c3f085 is active for registrant@exa... | C-DM-38 | Data model, Seed data |
| `registrant@example.com` | Seeded link seed-live-4b7d9e2a61c3f085 is active for registrant@exa... | C-DM-38 | Data model, Seed data |
| `seed-revoked-9a4d7e1f5b20` | Seeded link seed-revoked-9a4d7e1f5b20 is revoked | C-DM-39 | Data model, Seed data |
| `seed-expired-7c1e2a9b4d36` | Seeded link seed-expired-7c1e2a9b4d36 for registrant2@example.com i... | C-DM-40 | Data model, Seed data |
| `registrant2@example.com` | Seeded link seed-expired-7c1e2a9b4d36 for registrant2@example.com i... | C-DM-40 | Data model, Seed data |
| `seed-usedup-3f8b6d0c2e71` | Seeded link seed-usedup-3f8b6d0c2e71 for registrant3@example.com ha... | C-DM-41 | Data model, Seed data |
| `registrant3@example.com` | Seeded link seed-usedup-3f8b6d0c2e71 for registrant3@example.com ha... | C-DM-41 | Data model, Seed data |
| `0.2.3` | The seed holds published release 0.2.3 with its pinned build, date,... | C-DM-42 | Data model, Seed data |
| `0.2.2` | The seed holds published release 0.2.2 with its pinned build, date,... | C-DM-43 | Data model, Seed data |
| `0.2.1` | The seed holds published release 0.2.1 with its pinned build, date,... | C-DM-44 | Data model, Seed data |
| `0.2.0` | The seed holds revoked release 0.2.0 with its pinned build, date, s... | C-DM-45 | Data model, Seed data |
| `0.2.3` | The 0.2.3 release notes name the import sources Espresso, Alder, Ra... | C-FE-03 | Front-end specification, Identity |
| `(c) 2026 Halyard Labs` | The footer base line reads (c) 2026 Halyard Labs | C-FE-04 | Front-end specification, Global chrome |
| `hello@example.com` | The single support address is hello@example.com | C-FE-05 | Front-end specification, Identity |
| `https://downloads.example.com` | Release binaries with the press kit are served from https://downloa... | C-FE-06 | Front-end specification, Identity |
| `#features` | Product, Workflow, Pricing, FAQ target #features, #workflow, #prici... | C-FE-11 | Front-end specification, Navigation model |
| `#workflow` | Product, Workflow, Pricing, FAQ target #features, #workflow, #prici... | C-FE-11 | Front-end specification, Navigation model |
| `#pricing` | Product, Workflow, Pricing, FAQ target #features, #workflow, #prici... | C-FE-11 | Front-end specification, Navigation model |
| `#help` | Product, Workflow, Pricing, FAQ target #features, #workflow, #prici... | C-FE-11 | Front-end specification, Navigation model |
| `4.5:1` | Secondary text on a resting pane keeps a contrast of at least 4.5:1 | C-FE-22 | Front-end specification, Contrast obligations |
| `4.5:1` | Meaningful tertiary text keeps a contrast of at least 4.5:1 | C-FE-23 | Front-end specification, Contrast obligations |
| `3:1` | Placeholder text keeps a contrast of at least 3:1 | C-FE-24 | Front-end specification, Contrast obligations |
| `IBM Plex Mono` | IBM Plex Mono is the only downloaded font family | C-FE-25 | Front-end specification, Typography |
| `IBM Plex Mono` | IBM Plex Mono ships in weights 400, 500, 600 | C-FE-26 | Front-end specification, Typography |
| `400` | IBM Plex Mono ships in weights 400, 500, 600 | C-FE-26 | Front-end specification, Typography |
| `500` | IBM Plex Mono ships in weights 400, 500, 600 | C-FE-26 | Front-end specification, Typography |
| `600` | IBM Plex Mono ships in weights 400, 500, 600 | C-FE-26 | Front-end specification, Typography |
| `16px` | Body prose renders at 16px on a 24px line height | C-FE-28 | Front-end specification, Typography |
| `24px` | Body prose renders at 16px on a 24px line height | C-FE-28 | Front-end specification, Typography |
| `10px` | Text below display size uses only the sizes 10px, 11px, 12px, 14px,... | C-FE-29 | Front-end specification, Typography |
| `11px` | Text below display size uses only the sizes 10px, 11px, 12px, 14px,... | C-FE-29 | Front-end specification, Typography |
| `12px` | Text below display size uses only the sizes 10px, 11px, 12px, 14px,... | C-FE-29 | Front-end specification, Typography |
| `14px` | Text below display size uses only the sizes 10px, 11px, 12px, 14px,... | C-FE-29 | Front-end specification, Typography |
| `16px` | Text below display size uses only the sizes 10px, 11px, 12px, 14px,... | C-FE-29 | Front-end specification, Typography |
| `18px` | Text below display size uses only the sizes 10px, 11px, 12px, 14px,... | C-FE-29 | Front-end specification, Typography |
| `11px` | Uppercase eyebrow labels render at 11px, bold at 700 | C-FE-30 | Front-end specification, Typography |
| `700` | Uppercase eyebrow labels render at 11px, bold at 700 | C-FE-30 | Front-end specification, Typography |
| `Skip to content` | The skip link reads Skip to content | C-FE-55 | Front-end specification, Global chrome |
| `Lumen Prompt is not affiliated with Northgate, Bellweather or Halcyon.` | The footer base line shows Lumen Prompt is not affiliated with Nort... | C-FE-70 | Front-end specification, Global chrome |
| `12px` | The disclaimer renders at no less than 12px | C-FE-71 | Front-end specification, Global chrome |
| `Release notes 0.2.3` | The palette destinations group lists seventeen entries, among them... | C-FE-95 | Front-end specification, Command palette |
| `Inject` | The palette footer hint uses the verb Inject | C-FE-107 | Front-end specification, Command palette |
| `<mark>` | Palette search wraps each matched run in a <mark> element | C-FE-111 | Front-end specification, Command palette |
| `Demonstration data` | The history ledger carries the label Demonstration data | C-FE-122 | Front-end specification, Home |
| `Try the hotkey` | Try the hotkey opens the hotkey demonstration dialog | C-FE-125 | Front-end specification, The instrument system |
| `#features` | The home route carries the section anchors #features, #workflow, #p... | C-FE-143 | Front-end specification, Home |
| `#workflow` | The home route carries the section anchors #features, #workflow, #p... | C-FE-143 | Front-end specification, Home |
| `#pricing` | The home route carries the section anchors #features, #workflow, #p... | C-FE-143 | Front-end specification, Home |
| `#help` | The home route carries the section anchors #features, #workflow, #p... | C-FE-143 | Front-end specification, Home |
| `Cmd` | The hero shows the key caps Cmd, Shift, Space | C-FE-145 | Front-end specification, Home |
| `Shift` | The hero shows the key caps Cmd, Shift, Space | C-FE-145 | Front-end specification, Home |
| `Space` | The hero shows the key caps Cmd, Shift, Space | C-FE-145 | Front-end specification, Home |
| `Free during beta. No card required.` | The hero note reads Free during beta. No card required | C-FE-147 | Front-end specification, Home |
| `Local-first` | The hero chips read Local-first, Signed builds, No subscription | C-FE-148 | Front-end specification, Home |
| `Signed builds` | The hero chips read Local-first, Signed builds, No subscription | C-FE-148 | Front-end specification, Home |
| `No subscription` | The hero chips read Local-first, Signed builds, No subscription | C-FE-148 | Front-end specification, Home |
| `Client brief summary` | The workflow runner names Client brief summary with the claim No co... | C-FE-154 | Front-end specification, Home |
| `No context switch` | The workflow runner names Client brief summary with the claim No co... | C-FE-154 | Front-end specification, Home |
| `Finished prompt` | The workflow output card is labelled Finished prompt | C-FE-155 | Front-end specification, Home |
| `Version 3, starred` | The version scrubber announces a version label such as Version 3, s... | C-FE-161 | Front-end specification, Home |
| `Quick copy` | The ledger shows six rows naming target apps with Quick copy or a f... | C-FE-164 | Front-end specification, Home |
| `See the roadmap` | The beta note is signed by Devrim with See the roadmap linking to /... | C-FE-165 | Front-end specification, Home |
| `/roadmap` | The beta note is signed by Devrim with See the roadmap linking to /... | C-FE-165 | Front-end specification, Home |
| `Comparison checked on 2026-08-15 against each tool's public documentation.` | The comparison footnote reads Comparison checked on 2026-08-15 agai... | C-FE-170 | Front-end specification, Home |
| `$0` | The Free card shows $0 with the post-1.0 limits of 25 Blueprints, 3... | C-FE-175 | Front-end specification, Home |
| `About the cost of 15 billable minutes` | The founder card shows About the cost of 15 billable minutes with E... | C-FE-176 | Front-end specification, Home |
| `Every 1.x update, for life` | The founder card shows About the cost of 15 billable minutes with E... | C-FE-176 | Front-end specification, Home |
| `Standard licence at 1.0: $49` | The founder card shows Standard licence at 1.0: $49 | C-FE-178 | Front-end specification, Home |
| `Claim a founder place` | The founder card action Claim a founder place leads to /download | C-FE-179 | Front-end specification, Home |
| `/download` | The founder card action Claim a founder place leads to /download | C-FE-179 | Front-end specification, Home |
| `Checkout is not open yet. Registering holds your place.` | The founder card notes Checkout is not open yet. Registering holds... | C-FE-180 | Front-end specification, Home |
| `Standard licence` | The 1.0 card lists Standard licence at $49, Extended licence at $79... | C-FE-181 | Front-end specification, Home |
| `$49` | The 1.0 card lists Standard licence at $49, Extended licence at $79... | C-FE-181 | Front-end specification, Home |
| `Extended licence` | The 1.0 card lists Standard licence at $49, Extended licence at $79... | C-FE-181 | Front-end specification, Home |
| `$79` | The 1.0 card lists Standard licence at $49, Extended licence at $79... | C-FE-181 | Front-end specification, Home |
| `Update renewal` | The 1.0 card lists Standard licence at $49, Extended licence at $79... | C-FE-181 | Front-end specification, Home |
| `$19` | The 1.0 card lists Standard licence at $49, Extended licence at $79... | C-FE-181 | Front-end specification, Home |
| `Requires macOS 26.1 or later` | The 1.0 card states Requires macOS 26.1 or later | C-FE-182 | Front-end specification, Home |
| `$29` | With fewer than 500 places held the founder card shows $29 above N... | C-FE-184 | Front-end specification, Home |
| `N of 500 founder places left at $29` | With fewer than 500 places held the founder card shows $29 above N... | C-FE-184 | Front-end specification, Home |
| `Founder places are all claimed` | With every place held the founder card shows Founder places are all... | C-FE-186 | Front-end specification, Home |
| `Join the beta` | With every place held the founder card shows Founder places are all... | C-FE-186 | Front-end specification, Home |
| `Privacy` | The help panel shows the chips Privacy, Pricing, Beta, Platform | C-FE-189 | Front-end specification, Home |
| `Pricing` | The help panel shows the chips Privacy, Pricing, Beta, Platform | C-FE-189 | Front-end specification, Home |
| `Beta` | The help panel shows the chips Privacy, Pricing, Beta, Platform | C-FE-189 | Front-end specification, Home |
| `Platform` | The help panel shows the chips Privacy, Pricing, Beta, Platform | C-FE-189 | Front-end specification, Home |
| `#faq-01` | Help items open when linked as #faq-01 to #faq-08 | C-FE-195 | Front-end specification, Home |
| `#faq-08` | Help items open when linked as #faq-01 to #faq-08 | C-FE-195 | Front-end specification, Home |
| `Requires macOS 26.1 or later.` | The closing section states Requires macOS 26.1 or later. above a fo... | C-FE-198 | Front-end specification, Home |
| `/download` | /download shows the chips Free during beta, No card required, Open... | C-FE-199 | Front-end specification, Join the beta |
| `Free during beta` | /download shows the chips Free during beta, No card required, Open... | C-FE-199 | Front-end specification, Join the beta |
| `No card required` | /download shows the chips Free during beta, No card required, Open... | C-FE-199 | Front-end specification, Join the beta |
| `Open registration` | /download shows the chips Free during beta, No card required, Open... | C-FE-199 | Front-end specification, Join the beta |
| `Founder pricing before 1.0` | /download shows the chips Free during beta, No card required, Open... | C-FE-199 | Front-end specification, Join the beta |
| `Official distribution` | The distribution panel is headed Official distribution | C-FE-200 | Front-end specification, Join the beta |
| `/downloads/latest` | The distribution panel shows /downloads/latest with /appcast.xml | C-FE-203 | Front-end specification, Join the beta |
| `/appcast.xml` | The distribution panel shows /downloads/latest with /appcast.xml | C-FE-203 | Front-end specification, Join the beta |
| `macOS 26.1 or later` | The distribution panel requirement reads macOS 26.1 or later for th... | C-FE-204 | Front-end specification, Join the beta |
| `Optional` | The name field shows the placeholder Optional | C-FE-210 | Front-end specification, Join the beta |
| `Not sure` | The platform select offers Not sure, macOS 26.1, macOS 26.2, macOS... | C-FE-211 | Front-end specification, Join the beta |
| `macOS 26.1` | The platform select offers Not sure, macOS 26.1, macOS 26.2, macOS... | C-FE-211 | Front-end specification, Join the beta |
| `macOS 26.2` | The platform select offers Not sure, macOS 26.1, macOS 26.2, macOS... | C-FE-211 | Front-end specification, Join the beta |
| `macOS 26.3` | The platform select offers Not sure, macOS 26.1, macOS 26.2, macOS... | C-FE-211 | Front-end specification, Join the beta |
| `macOS 27` | The platform select offers Not sure, macOS 26.1, macOS 26.2, macOS... | C-FE-211 | Front-end specification, Join the beta |
| `One email with your link. No newsletter.` | The form shows One email with your link. No newsletter | C-FE-216 | Front-end specification, Join the beta |
| `Enter an email address so we can send your access link.` | A missing email shows Enter an email address so we can send your ac... | C-FE-219 | Front-end specification, Join the beta |
| `Confirm you want the access link.` | A missing consent shows Confirm you want the access link | C-FE-221 | Front-end specification, Join the beta |
| `/use-cases` | /use-cases shows the five numbered cards with the pinned eyebrows,... | C-FE-233 | Front-end specification, Use cases |
| `Client briefs` | The radial diagram labels read Client briefs, Code reviews, Researc... | C-FE-237 | Front-end specification, Use cases |
| `Code reviews` | The radial diagram labels read Client briefs, Code reviews, Researc... | C-FE-237 | Front-end specification, Use cases |
| `Research notes` | The radial diagram labels read Client briefs, Code reviews, Researc... | C-FE-237 | Front-end specification, Use cases |
| `Without Lumen Prompt` | The use-case contrast block columns read Without Lumen Prompt with... | C-FE-241 | Front-end specification, Use-case pages |
| `With Lumen Prompt` | The use-case contrast block columns read Without Lumen Prompt with... | C-FE-241 | Front-end specification, Use-case pages |
| `Demonstration data` | The use-case mockup carries the label Demonstration data | C-FE-243 | Front-end specification, Use-case pages |
| `BreadcrumbList` | Each use-case page carries BreadcrumbList with FAQPage structured data | C-FE-245 | Front-end specification, Use-case pages |
| `FAQPage` | Each use-case page carries BreadcrumbList with FAQPage structured data | C-FE-245 | Front-end specification, Use-case pages |
| `/` | / with /download carry SoftwareApplication structured data | C-FE-246 | Front-end specification, Use-case pages |
| `/download` | / with /download carry SoftwareApplication structured data | C-FE-246 | Front-end specification, Use-case pages |
| `SoftwareApplication` | / with /download carry SoftwareApplication structured data | C-FE-246 | Front-end specification, Use-case pages |
| `/changelog` | /changelog shows the pinned sub-heading about one source of truth | C-FE-247 | Front-end specification, Changelog |
| `Download` | The current stable block offers Download with Read the notes | C-FE-250 | Front-end specification, Changelog |
| `Read the notes` | The current stable block offers Download with Read the notes | C-FE-250 | Front-end specification, Changelog |
| `Lumen Prompt is free during the beta.` | Release notes show the note Lumen Prompt is free during the beta | C-FE-252 | Front-end specification, Release notes |
| `What is new` | Release notes sections run in the pinned order from What is new thr... | C-FE-253 | Front-end specification, Release notes |
| `Known issues` | Release notes sections run in the pinned order from What is new thr... | C-FE-253 | Front-end specification, Release notes |
| `Reporting problems` | Release notes sections run in the pinned order from What is new thr... | C-FE-253 | Front-end specification, Release notes |
| `/roadmap` | /roadmap shows the pinned caveat about order changing with beta fee... | C-FE-256 | Front-end specification, Roadmap |
| `/blog` | /blog lists Stop rewriting your best prompt above Prompts are work... | C-FE-261 | Front-end specification, Blog |
| `Stop rewriting your best prompt` | /blog lists Stop rewriting your best prompt above Prompts are work... | C-FE-261 | Front-end specification, Blog |
| `Prompts are work product` | /blog lists Stop rewriting your best prompt above Prompts are work... | C-FE-261 | Front-end specification, Blog |
| `/press` | /press offers Download the press kit (48 MB) linking to the pinned... | C-FE-266 | Front-end specification, Press |
| `Download the press kit (48 MB)` | /press offers Download the press kit (48 MB) linking to the pinned... | C-FE-266 | Front-end specification, Press |
| `You may` | The usage guidelines are two lists headed You may with You may not... | C-FE-275 | Front-end specification, Press |
| `You may not` | The usage guidelines are two lists headed You may with You may not... | C-FE-275 | Front-end specification, Press |
| `/contact` | /contact shows the pinned one-address sentence | C-FE-276 | Front-end specification, Contact, Privacy and Terms |
| `/contact` | /contact shows hello@example.com as selectable text with a mail link | C-FE-277 | Front-end specification, Contact, Privacy and Terms |
| `hello@example.com` | /contact shows hello@example.com as selectable text with a mail link | C-FE-277 | Front-end specification, Contact, Privacy and Terms |
| `Lumen Prompt support` | The contact mail link carries the subject Lumen Prompt support with... | C-FE-278 | Front-end specification, Contact, Privacy and Terms |
| `macOS version:` | The contact mail link carries the subject Lumen Prompt support with... | C-FE-278 | Front-end specification, Contact, Privacy and Terms |
| `Lumen Prompt version:` | The contact mail link carries the subject Lumen Prompt support with... | C-FE-278 | Front-end specification, Contact, Privacy and Terms |
| `This access link is no longer valid` | revoked or superseded link heading | C-CF-76 | Core features, Access links rule 5 |
| `This access link has been used up` | used-up link heading | C-CF-77 | Core features, Access links rule 5 |
| `This access link has expired` | expired link heading | C-CF-78 | Core features, Access links rule 5 |
| `We do not recognise this access link` | unknown or malformed link heading | C-CF-79 | Core features, Access links rule 5 |
| `You were already on the list, so this is a fresh link.` | second line of a later link email | C-CF-61 | Core features, Access links rule 1 |
| `Your founder place: 7` | worked example of the founder place line | C-CF-62 | Core features, Access links rule 1 |
| `Order and scope change with beta feedback.` | roadmap caveat | C-FE-256 | Front-end specification, Roadmap |
| `Check the address, it looks like a typo.` | malformed email message | C-FE-220 | Front-end specification, Join the beta |
| `Signed and notarised binary; update feed signed with a separate key` | distribution panel verification claim | C-FE-202 | Front-end specification, Join the beta |
| `Consultant, researcher or engineer` | role field placeholder | C-FE-212 | Front-end specification, Join the beta |
| `Client briefs, code review or research notes` | primary use field placeholder | C-FE-213 | Front-end specification, Join the beta |
| `Send me my beta access link and occasional beta updates at this address. I have read the privacy policy.` | consent sentence | C-FE-214 | Front-end specification, Join the beta |
| `If no build is ready when you open your link, the page confirms your registration and we email you when the first build ships.` | form fallback note | C-FE-217 | Front-end specification, Join the beta |
| `Lumen Prompt keeps the prompts you reuse at work one keystroke away, with their variables, files and history.` | hero sub-headline | C-FE-146 | Front-end specification, Home |
| `Release notes are linked from each version, so this page and the in-app updater share one source of truth.` | changelog sub-heading | C-FE-247 | Front-end specification, Changelog |
| `This release was revoked and is no longer offered.` | revoked release notice | C-CF-109 | Core features, Release registry rule 5 |
| `Beta questions, support, privacy requests and press all reach a person at one address.` | contact sentence | C-FE-276 | Front-end specification, Contact, Privacy and Terms |
| `The visual language follows the running application, but the content is purpose-built synthetic marketing data, not real workspace text.` | synthetic-data disclaimer | C-FE-242 | Front-end specification, Use-case pages |
| `One-time payment` | founder card bullet | C-FE-177 | Front-end specification, Home |
| `Numbered founder place` | founder card bullet | C-FE-177 | Front-end specification, Home |
| `Signed builds and updates` | founder card bullet | C-FE-177 | Front-end specification, Home |
| `Price locked to your place` | founder card bullet | C-FE-177 | Front-end specification, Home |
| `https://downloads.example.com/lumen-prompt/press-kit.zip` | press kit archive | C-FE-266 | Front-end specification, Press |
| `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.3.dmg` | seeded 0.2.3 download address | C-DM-42 | Data model, Seed data |
| `08035fead80e0cfe09a8ad0bc7d7486a353c38890810acd9ed2cb8372df9bb5a` | seeded 0.2.3 checksum | C-DM-42 | Data model, Seed data |
| `72hn8fG8m3U31YYqCB378cZKcpDwXR+iNhBHIvstb8USInEGvUdXHuRZdNMAK0OyBz2RmbRD7zMyOz4RQa2cRg==` | seeded 0.2.3 signature | C-DM-42 | Data model, Seed data |
| `24117248` | seeded 0.2.3 size in bytes | C-DM-42 | Data model, Seed data |
| `2026-08-28` | seeded 0.2.3 publication date | C-DM-42 | Data model, Seed data |
| `Faster search, steadier injection and a clearer version history.` | seeded 0.2.3 summary | C-DM-42 | Data model, Seed data |
| `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.2.dmg` | seeded 0.2.2 download address | C-DM-43 | Data model, Seed data |
| `c2e5920ade47626fae119eb565b325979707e168705380a4791055818855780c` | seeded 0.2.2 checksum | C-DM-43 | Data model, Seed data |
| `23855104` | seeded 0.2.2 size in bytes | C-DM-43 | Data model, Seed data |
| `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.1.dmg` | seeded 0.2.1 download address | C-DM-44 | Data model, Seed data |
| `6557b3ed2d20b07757b7c5080ef611a1b0c7b4c855393417a5060d5c20f03cda` | seeded 0.2.1 checksum | C-DM-44 | Data model, Seed data |
| `23592960` | seeded 0.2.1 size in bytes | C-DM-44 | Data model, Seed data |
| `https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.0.dmg` | seeded 0.2.0 download address | C-DM-45 | Data model, Seed data |
| `b10364b9f7d0b4a8ee44327567675ec333eafcd6d627a5935a9789c4fdb0e020` | seeded 0.2.0 checksum | C-DM-45 | Data model, Seed data |
| `23330816` | seeded 0.2.0 size in bytes | C-DM-45 | Data model, Seed data |
| `Also in this release` | release notes section heading | C-FE-253 | Front-end specification, Release notes |
| `Fixed` | release notes section heading | C-FE-253 | Front-end specification, Release notes |
| `Performance` | release notes section heading | C-FE-253 | Front-end specification, Release notes |
| `Updates` | release notes section heading | C-FE-253 | Front-end specification, Release notes |
| `/blog/stop-rewriting-your-best-prompt` | newer article route | C-UF-14 | User flow route table row 14 |
| `/blog/prompts-are-work-product` | older article route | C-UF-13 | User flow route table row 13 |

### Referenced but not pinned

None that a grader asserts. Values the brief lists inside an item's own `src` position, such as the privacy and terms heading identifiers, are pinned by that item rather than given a row here.

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 6 |
| User roles | 1 | 17 |
| Core features | 22 | 154 |
| User flow | 14 | 53 |
| UI and UX notes | 3 | 46 |
| Technical requirements | 10 | 33 |
| Data model | 4 | 47 |
| Front-end specification | 45 | 287 |
| Constraints | 0 | 4 |
| Deployment contract | 11 | 11 |

Constraints bullets carry no obligation verb the segmenter counts; every bullet still maps to an item here or to the declared-but-ungraded list.

## Declared but ungraded

Stated in instruction.md, carried here for the reviewer, and deliberately not checklist items: no grader in this environment can observe them (OPEN-DECISIONS D-H). Each carries its reason.

* The app is built with TypeScript on Node.js 20, SolidStart plus Express. (src: Technical requirements, Stack) why: The implementation stack is invisible from outside the app; INV6 bars source reading on the reward path, and the vendored recompute.py does not render source criteria.
* The app uses no second database, cache, queue, object store, identity provider or mail vendor. (src: Technical requirements, Stack) why: Absence of an unnamed backing service cannot be observed over HTTP or through the three capability adapters.
* The app creates no subscription, payment method or refund in Kill Bill. (src: Technical requirements, Kill Bill) why: The payments adapter reads accounts and invoices only; invoices are graded, the rest is outside reference/K K.4.
* The server writes one structured log line per request to stdout, never a full token. (src: Technical requirements, Health) why: Container stdout is not available to the verifier.
* The signing key never reaches this server. (src: Technical requirements, Update feed format) why: Key custody is an operational fact, not an app observable.
* `/app/USER_README.md` lists each seeded account with the password. (src: Data model para 2) why: The verifier runs in a separate container and cannot read /app (stage-3 names this as the canonical unobservable).
* Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root. (src: Deployment contract bullet 6) why: The app filesystem is not visible to the verifier.
* A production build is served behind a static or preview server. (src: Deployment contract bullet 7) why: Build mode has no stable external signature across frameworks.
* The app downloads, installs or starts no copy of a backing service. (src: Deployment contract bullet 10) why: Not observable from the verifier container.
* The app uses no edge functions. (src: Deployment contract bullet 11) why: Not observable from the verifier container.
* The app uses no persistent volumes, fixed container names or custom networks. (src: Deployment contract bullet 12) why: Container configuration is outside the app surface.
* Every page shows a loading state. (src: User flow, States) why: Loading states are transient and not reproducible deterministically.
* A server error renders the branded error page with a request identifier, a retry, a link to `/downloads/latest`. (src: User flow, States) why: A server fault cannot be induced from outside without mocking.
* A failing layout still renders a minimal inline-styled page. (src: Front-end specification, Access and error pages) why: Cannot be induced from outside.
* A backend failure keeps values with a try-again message; a reload after a server error keeps values. (src: Front-end specification, Join the beta) why: A backend fault cannot be induced from outside.
* A cohort closing mid-visit updates the success panel honestly. (src: Front-end specification, Join the beta) why: A race between a page load and the thousandth place is not reproducible deterministically.
* The submitting state marks the action busy with fields disabled. (src: Front-end specification, Join the beta) why: The form's submit target is the app's choice, so the request cannot be held open reliably.
* The founder card shows its static content with no badge when the count cannot be read. (src: Front-end specification, Home) why: The allocation endpoint cannot be made to fail from outside.
* A published release's notes stay exactly as published. (src: Front-end specification, Release notes) why: No edit path exists to exercise.
* Smooth scrolling, if added, halts while a dialog is open with no fight against scroll restoration. (src: Front-end specification, Scroll and page transitions) why: Optional behaviour; the observable halves (keyboard paging, restoration, nested scroll) are graded separately.
* The docking copy is hidden from assistive technology, announcing once on completion. (src: Front-end specification, The instrument system) why: The flying copy exists only mid-animation.
* The orbit ring with the scan are hidden from assistive technology. (src: Front-end specification, Use cases) why: Decorative elements have no stable locator the brief pins.
* The app calls no AI vendor from the server. (src: Constraints bullet 3) why: Server-side egress is not observable; the browser half is graded by fe_no_analytics.
* The app has no general permission engine, organisation chart or approval chain. (src: Constraints bullet 9) why: An absence of internal architecture is not observable.
* The native macOS application is not built here. (src: Constraints bullet 10) why: A scope statement with no app observable.
* The app stays responsive with 10000 registrations with 100 releases. (src: Constraints bullet 12) why: Seeding that volume would take the verifier past its budget.
