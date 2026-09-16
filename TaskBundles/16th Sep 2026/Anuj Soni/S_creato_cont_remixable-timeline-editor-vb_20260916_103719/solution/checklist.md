# Checklist: Remixable Timeline Editor

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 661
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public marketing site for a browser video editor. `src: Overview, para 2`
- [ ] `C-OV-02` `capability` The app serves a signed-in editor on the same origin as the marketing site. `src: Overview, para 2`
- [ ] `C-OV-03` `capability` A block on the timeline is a parameterised effect tuned by dials, sliders, prompts or code. `src: Overview, para 1`
- [ ] `C-OV-04` `constraint` A saved block belongs to the team workspace rather than to one person. `src: Overview, para 1`
- [ ] `C-OV-05` `constraint` The product offers no stock media library. `src: Overview, para 3`
- [ ] `C-OV-06` `constraint` The product processes no payments. `src: Overview, para 3`
- [ ] `C-OV-07` `constraint` Enterprise exists only as a pricing card plus a sales conversation. `src: Overview, para 3`
- [ ] `C-OV-08` `constraint` Two members spending the last unit of one allowance never both succeed. `src: Overview, para 4`
- [ ] `C-OV-09` `constraint` A retried export costs one unit. `src: Overview, para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` The app defines two account roles, `member` plus `reviewer`. `src: User roles, para 1`
- [ ] `C-RL-02` `role` Owning a workspace is a relationship rather than a third role. `src: User roles, para 1`
- [ ] `C-RL-03` `role` A member may belong to more than one workspace. `src: User roles, table row 1`
- [ ] `C-RL-04` `role` The workspace owner changes the workspace plan. `src: User roles, table row 1`
- [ ] `C-RL-05` `role` The workspace owner invites a member by email. `src: User roles, table row 1`
- [ ] `C-RL-06` `role` The workspace owner removes a member. `src: User roles, table row 1`
- [ ] `C-RL-07` `role` The workspace owner reads the workspace charges. `src: User roles, table row 1`
- [ ] `C-RL-08` `role` The workspace owner reads the share view logs. `src: User roles, table row 1`
- [ ] `C-RL-09` `role` A member who does not own the workspace cannot change the plan. `src: User roles, table row 1`
- [ ] `C-RL-10` `role` A member who does not own the workspace cannot invite anyone. `src: User roles, table row 1`
- [ ] `C-RL-11` `role` A member who does not own the workspace cannot read the charges. `src: User roles, table row 1`
- [ ] `C-RL-12` `role` A member cannot read a workspace the member does not belong to. `src: User roles, table row 1`
- [ ] `C-RL-13` `role` A member cannot place a saved block from another workspace. `src: User roles, table row 1`
- [ ] `C-RL-14` `role` A reviewer account comes from accepting a review invitation. `src: User roles, table row 2`
- [ ] `C-RL-15` `role` A reviewer sees only versions whose approval was requested of that reviewer. `src: User roles, table row 2`
- [ ] `C-RL-16` `role` A reviewer comments on a version sent to that reviewer. `src: User roles, table row 2`
- [ ] `C-RL-17` `role` A reviewer records one decision per approval request. `src: User roles, table row 2`
- [ ] `C-RL-18` `role` A reviewer cannot open any workspace project page. `src: User roles, table row 2`
- [ ] `C-RL-19` `role` A reviewer occupies no seat. `src: User roles, table row 2`
- [ ] `C-RL-20` `constraint` The server rejects a reviewer call to a member endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-21` `constraint` A denied request leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-22` `constraint` The server rejects a member call to another workspace's endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-23` `constraint` The server rejects a non-owner call to an owner-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-24` `role` Signup through `/register` creates a `member`. `src: User roles, signup paragraph`
- [ ] `C-RL-25` `role` Signup creates a Free workspace owned by the new member. `src: User roles, signup paragraph`
- [ ] `C-RL-26` `constraint` No request field chooses the role of an account. `src: User roles, signup paragraph`
- [ ] `C-RL-27` `literal` The app seeds the account `member@example.com`. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-28` `literal` The app seeds the account `member2@example.com`. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-29` `literal` The app seeds the account `member3@example.com`. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-30` `literal` The app seeds the account `member4@example.com`. `src: User roles, seeded accounts table row 4`
- [ ] `C-RL-31` `literal` The app seeds the reviewer account `reviewer@example.com`. `src: User roles, seeded accounts table row 5`
- [ ] `C-RL-32` `literal` The app seeds the reviewer account `reviewer2@example.com`. `src: User roles, seeded accounts table row 6`
- [ ] `C-RL-33` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-34` `data` The account for Nadia Okafor owns the workspace named Juniper Goods. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-35` `data` The account for Theo Brandt belongs to Juniper Goods without owning the workspace. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-36` `data` The account for Ines Duarte owns the Free workspace named Solo Sketchbook. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-37` `data` The account for Omar Haddad owns the Basic workspace named Basic Bench. `src: User roles, seeded accounts table row 4`
- [ ] `C-RL-38` `data` No approval request is addressed to the reviewer Lucas Meyer. `src: User roles, seeded accounts table row 6`

## C-CF Core features

- [ ] `C-CF-01` `capability` A signup returns an `access_token`. `src: Core features, Accounts rule 1`
- [ ] `C-CF-02` `constraint` A second signup with a stored address is rejected as invalid. `src: Core features, Accounts rule 1`
- [ ] `C-CF-03` `constraint` A signup password shorter than ten characters is rejected as invalid. `src: Core features, Accounts rule 1`
- [ ] `C-CF-04` `data` Signup names the new workspace from `workspace_name` when supplied. `src: Core features, Accounts rule 1`
- [ ] `C-CF-05` `data` Signup without a workspace name uses the display name followed by the possessive workspace suffix. `src: Core features, Accounts rule 1`
- [ ] `C-CF-06` `capability` Login with a seeded address returns an `access_token`. `src: Core features, Accounts rule 2`
- [ ] `C-CF-07` `constraint` Login with a wrong password returns no token. `src: Core features, Accounts rule 2`
- [ ] `C-CF-08` `constraint` A guarded endpoint denies a call carrying no token. `src: Core features, Accounts rule 3`
- [ ] `C-CF-09` `constraint` A guarded endpoint denies a call carrying a token the app never issued. `src: Core features, Accounts rule 3`
- [ ] `C-CF-10` `constraint` A signup body naming a role still creates a member. `src: Core features, Accounts rule 4`
- [ ] `C-CF-11` `capability` The workspace list returns only the caller's workspaces. `src: Core features, Accounts rule 5`
- [ ] `C-CF-12` `data` Each listed workspace carries the caller's `relation` as owner or member. `src: Core features, Accounts rule 5`
- [ ] `C-CF-13` `data` Work a member created stays in the workspace after the member is removed. `src: Core features, Accounts rule 6`
- [ ] `C-CF-14` `capability` The account endpoint stores the member's `interface_scale`. `src: Core features, Accounts rule 7`
- [ ] `C-CF-15` `constraint` An interface scale outside the four allowed values is rejected as invalid. `src: Core features, Accounts rule 7`
- [ ] `C-CF-16` `data` A stored interface scale is back after signing in again. `src: Core features, Accounts rule 7`
- [ ] `C-CF-17` `data` The app stores every password hashed. `src: Core features, Accounts para 1`
- [ ] `C-CF-18` `constraint` No endpoint returns a password or password hash. `src: Core features, Accounts para 1`
- [ ] `C-CF-19` `capability` A signed-in browser shows the signed-in header on first paint. `src: Core features, Accounts para 1`
- [ ] `C-CF-20` `data` The plans list returns five plans in the stored order. `src: Core features, Plans rule 2`
- [ ] `C-CF-21` `literal` Basic costs `2500` cents monthly. `src: Core features, Plans table row 2`
- [ ] `C-CF-22` `literal` Basic costs `1800` cents per month billed annually. `src: Core features, Plans table row 2`
- [ ] `C-CF-23` `literal` Pro costs `3800` cents monthly. `src: Core features, Plans table row 3`
- [ ] `C-CF-24` `literal` Pro costs `3000` cents per month billed annually. `src: Core features, Plans table row 3`
- [ ] `C-CF-25` `literal` Business costs `7000` cents monthly. `src: Core features, Plans table row 4`
- [ ] `C-CF-26` `literal` Business costs `5900` cents per month billed annually. `src: Core features, Plans table row 4`
- [ ] `C-CF-27` `data` Prices are integer cents in `usd`. `src: Core features, Plans rule 1`
- [ ] `C-CF-28` `data` Annual billing charges twelve times the annual per-month figure. `src: Core features, Plans rule 1`
- [ ] `C-CF-29` `constraint` The annual saving percent derives from the stored prices, rounded half up. `src: Core features, Plans rule 2`
- [ ] `C-CF-30` `literal` Basic reports an annual saving of `28`. `src: Core features, Plans rule 2`
- [ ] `C-CF-31` `literal` Pro reports an annual saving of `21`. `src: Core features, Plans rule 2`
- [ ] `C-CF-32` `literal` Business reports an annual saving of `16`. `src: Core features, Plans rule 2`
- [ ] `C-CF-33` `literal` The pricing route opens with `Unlimit your creativity.` `src: Core features, Plans rule 3`
- [ ] `C-CF-34` `capability` The pricing billing toggle offers a monthly position beside an annual position. `src: Core features, Plans rule 3`
- [ ] `C-CF-35` `literal` The pricing toggle badge reads `Save up to 28%`. `src: Core features, Plans rule 3`
- [ ] `C-CF-36` `capability` Annual mode shows each paid pricing card's own saving. `src: Core features, Plans rule 3`
- [ ] `C-CF-37` `capability` Annual mode switches each paid pricing card to the annual per-month price. `src: Core features, Plans rule 3`
- [ ] `C-CF-38` `literal` The Pro pricing card carries the marker `Most popular`. `src: Core features, Plans rule 4`
- [ ] `C-CF-39` `capability` Each pricing card carries the call to action named for that plan. `src: Core features, Plans rule 4`
- [ ] `C-CF-40` `capability` Each paid pricing card lists only additions after its everything-in line. `src: Core features, Plans rule 4`
- [ ] `C-CF-41` `data` The Pro plan carries a per-member unit. `src: Core features, Plans rule 5`
- [ ] `C-CF-42` `data` The Business plan carries a per-member unit. `src: Core features, Plans rule 5`
- [ ] `C-CF-43` `literal` The Pro pricing card states `Max 10 team members`. `src: Core features, Plans rule 5`
- [ ] `C-CF-44` `capability` Choosing Contact Sales opens the contact route with the sales audience chosen. `src: Core features, Plans rule 6`
- [ ] `C-CF-45` `constraint` Enterprise topics are sales conversation items that nothing in the product performs. `src: Core features, Plans rule 6`
- [ ] `C-CF-46` `data` Plan features carry every comparison row label from cloud storage to free fonts. `src: Core features, Plans rule 7`
- [ ] `C-CF-47` `capability` Pricing cards agree with the comparison table on every number. `src: Core features, Plans rule 7`
- [ ] `C-CF-48` `data` Each plan feature carries a `status` of available or coming soon. `src: Core features, Plans rule 8`
- [ ] `C-CF-49` `data` The rows listed as coming soon carry the `coming_soon` status. `src: Core features, Plans rule 8`
- [ ] `C-CF-50` `ui` Each coming soon row on the pricing comparison shows a visible marker in words. `src: Core features, Plans rule 8`
- [ ] `C-CF-51` `constraint` No allowance is consumed by a coming soon feature. `src: Core features, Plans rule 8`
- [ ] `C-CF-52` `data` The stored storage ceilings are 2, 5, 20 or 50 GB by plan. `src: Core features, Quotas table`
- [ ] `C-CF-53` `data` The stored monthly project variation limits are 0, 20, 250 or 2500 by plan. `src: Core features, Quotas table`
- [ ] `C-CF-54` `data` The stored monthly captioning limits are 30, 60, 120 or 600 minutes by plan. `src: Core features, Quotas table`
- [ ] `C-CF-55` `data` The stored monthly speech limits are 0, 0, 5000 or 20000 characters by plan. `src: Core features, Quotas table`
- [ ] `C-CF-56` `data` The stored brand kit ceilings are 0, 0, 5 or 10 by plan. `src: Core features, Quotas table`
- [ ] `C-CF-57` `data` The stored saved block ceilings are 5, 25, 50 or 100 by plan. `src: Core features, Quotas table`
- [ ] `C-CF-58` `data` The stored member ceilings are 1, 1, 10 or unlimited by plan. `src: Core features, Quotas table`
- [ ] `C-CF-59` `literal` A gigabyte counts `1073741824` bytes. `src: Core features, Quotas para after the table`
- [ ] `C-CF-60` `constraint` A Free export frame is held to 1280 by 720. `src: Core features, Quotas para after the table`
- [ ] `C-CF-61` `constraint` A Basic export frame is held to 1920 by 1080. `src: Core features, Quotas para after the table`
- [ ] `C-CF-62` `constraint` A Pro export frame is held to 2000 on each side. `src: Core features, Quotas para after the table`
- [ ] `C-CF-63` `data` Only Free exports carry a watermark. `src: Core features, Quotas para after the table`
- [ ] `C-CF-64` `constraint` Premium templates are included from Basic upward. `src: Core features, Quotas para after the table`
- [ ] `C-CF-65` `constraint` Brand kit fonts are included from Pro upward. `src: Core features, Quotas para after the table`
- [ ] `C-CF-66` `constraint` A usage window starts on the subscription anchor day. `src: Core features, Quotas rule 1`
- [ ] `C-CF-67` `constraint` Use from an earlier window never counts against the current window. `src: Core features, Quotas rule 1`
- [ ] `C-CF-68` `capability` The usage endpoint returns one row per meter. `src: Core features, Quotas rule 2`
- [ ] `C-CF-69` `data` Storage use sums the bytes of stored assets plus ready exports. `src: Core features, Quotas rule 2`
- [ ] `C-CF-70` `data` Member use counts members plus pending invitations. `src: Core features, Quotas rule 2`
- [ ] `C-CF-71` `constraint` Every unit is reserved before being settled or released. `src: Core features, Quotas rule 3`
- [ ] `C-CF-72` `constraint` Two concurrent variation claims on the last unit never both succeed. `src: Core features, Quotas rule 3`
- [ ] `C-CF-73` `constraint` Two concurrent block saves at the saved-block ceiling never both succeed. `src: Core features, Quotas rule 3`
- [ ] `C-CF-74` `constraint` Two concurrent invitations at the member ceiling never both succeed. `src: Core features, Quotas rule 3`
- [ ] `C-CF-75` `constraint` Two concurrent brand kits at the brand-kit ceiling never both succeed. `src: Core features, Quotas rule 3`
- [ ] `C-CF-76` `constraint` A meter never reports usage above its limit. `src: Core features, Quotas rule 3`
- [ ] `C-CF-77` `literal` A quota refusal carries the error code `quota_exceeded`. `src: Core features, Quotas rule 4`
- [ ] `C-CF-78` `data` A quota refusal names the meter, the limit, the plan plus a message. `src: Core features, Quotas rule 4`
- [ ] `C-CF-79` `capability` A spent monthly allowance is refused with the pinned monthly sentence. `src: Core features, Quotas rule 4`
- [ ] `C-CF-80` `capability` A full ceiling is refused with the pinned ceiling sentence. `src: Core features, Quotas rule 4`
- [ ] `C-CF-81` `capability` A meter the plan lacks is refused with the pinned not-included sentence. `src: Core features, Quotas rule 4`
- [ ] `C-CF-82` `capability` The eleventh Pro seat is refused with the pinned seat-cap sentence. `src: Core features, Quotas rule 4`
- [ ] `C-CF-83` `capability` An invitation on a single-user plan is refused with the pinned one-person sentence. `src: Core features, Quotas rule 4`
- [ ] `C-CF-84` `constraint` Ceilings apply whenever something new is written. `src: Core features, Quotas rule 5`
- [ ] `C-CF-85` `constraint` A workspace moved to a smaller plan keeps every existing item. `src: Core features, Quotas rule 5`
- [ ] `C-CF-86` `constraint` A workspace over a new ceiling cannot add another item of that kind. `src: Core features, Quotas rule 5`
- [ ] `C-CF-87` `capability` The subscription endpoint returns plan, billing period, seats, seats used plus period dates. `src: Core features, Seats rule 1`
- [ ] `C-CF-88` `data` A monthly period ends one calendar month after the period starts. `src: Core features, Seats rule 1`
- [ ] `C-CF-89` `constraint` Only the workspace owner may change the plan. `src: Core features, Seats rule 2`
- [ ] `C-CF-90` `data` A plan change starts a new period on the current UTC date. `src: Core features, Seats rule 2`
- [ ] `C-CF-91` `data` A plan change writes one `plan_change` charge of seats times the period price. `src: Core features, Seats rule 2`
- [ ] `C-CF-92` `capability` Choosing the enterprise plan is refused with the pinned sales sentence. `src: Core features, Seats rule 2`
- [ ] `C-CF-93` `data` Moving from a single-user plan to Pro sets seats to the current member count. `src: Core features, Seats rule 3`
- [ ] `C-CF-94` `data` Free or Basic subscriptions always hold one seat. `src: Core features, Seats rule 3`
- [ ] `C-CF-95` `capability` Moving a multi-member workspace onto a single-user plan is refused with the pinned switching sentence. `src: Core features, Seats rule 3`
- [ ] `C-CF-96` `constraint` A pending invitation occupies a seat. `src: Core features, Seats rule 4`
- [ ] `C-CF-97` `constraint` The refused eleventh Pro invitation stores nothing. `src: Core features, Seats rule 4`
- [ ] `C-CF-98` `capability` Accepting an invitation with the matching email adds the member to the workspace. `src: Core features, Seats rule 5`
- [ ] `C-CF-99` `data` Accepting an invitation raises seats by one. `src: Core features, Seats rule 5`
- [ ] `C-CF-100` `data` A join on Pro writes one prorated `seat_added` charge. `src: Core features, Seats rule 5`
- [ ] `C-CF-101` `constraint` The seat charge rounds half up the period price times remaining days over period days. `src: Core features, Seats rule 5`
- [ ] `C-CF-102` `literal` A Pro monthly join with fifteen of thirty days left charges `1900`. `src: Core features, Seats rule 5 table row 1`
- [ ] `C-CF-103` `literal` A Pro monthly join with ten of thirty days left charges `1267`. `src: Core features, Seats rule 5 table row 2`
- [ ] `C-CF-104` `literal` A Pro annual join with 116 of 365 days left charges `11441`. `src: Core features, Seats rule 5 table row 3`
- [ ] `C-CF-105` `constraint` A removed member loses workspace access at once. `src: Core features, Seats rule 6`
- [ ] `C-CF-106` `data` Removing a member lowers seats by one without a refund. `src: Core features, Seats rule 6`
- [ ] `C-CF-107` `constraint` The workspace owner cannot be removed. `src: Core features, Seats rule 6`
- [ ] `C-CF-108` `constraint` Revoking a pending invitation releases its seat. `src: Core features, Seats rule 6`
- [ ] `C-CF-109` `capability` The charges list returns charge lines newest first to the owner. `src: Core features, Seats rule 7`
- [ ] `C-CF-110` `capability` Every control panel is generated from the declared parameters of its block. `src: Core features, Library para 1`
- [ ] `C-CF-111` `data` A parameter control is one of dial, slider, prompt or code. `src: Core features, Library para 1`
- [ ] `C-CF-112` `data` The library holds the eight seeded blocks with their declared parameters. `src: Core features, Library table`
- [ ] `C-CF-113` `literal` The `Glow` block declares `intensity` as a slider from 0 to 100. `src: Core features, Library table row 2`
- [ ] `C-CF-114` `capability` The block list filters by category plus by name. `src: Core features, Library rule 1`
- [ ] `C-CF-115` `capability` The block list pages with a limit plus an offset. `src: Core features, Library rule 1`
- [ ] `C-CF-116` `capability` A block detail returns its `parameter_schema`. `src: Core features, Library rule 1`
- [ ] `C-CF-117` `data` Eight templates are seeded with stable uuids. `src: Core features, Library rule 2 table`
- [ ] `C-CF-118` `data` Each template carries one of four categories. `src: Core features, Library rule 2 table`
- [ ] `C-CF-119` `data` Night Cream Ritual plus Feature Reveal are the premium templates. `src: Core features, Library rule 2 table rows 5 to 6`
- [ ] `C-CF-120` `capability` A template detail returns the template timeline. `src: Core features, Library rule 2`
- [ ] `C-CF-121` `capability` The template list filters by category. `src: Core features, Library rule 2`
- [ ] `C-CF-122` `constraint` An unknown template uuid answers not found. `src: Core features, Library rule 2`
- [ ] `C-CF-123` `data` Three credited creators are seeded with their slugs. `src: Core features, Library rule 3`
- [ ] `C-CF-124` `capability` A creator detail returns the credited templates. `src: Core features, Library rule 3`
- [ ] `C-CF-125` `constraint` A favourite names a block or a template, never both. `src: Core features, Library rule 4`
- [ ] `C-CF-126` `constraint` Favouriting the same target twice leaves one favourite. `src: Core features, Library rule 4`
- [ ] `C-CF-127` `constraint` Brand kit creation counts against the brand-kit ceiling. `src: Core features, Library rule 5`
- [ ] `C-CF-128` `constraint` A brand kit font list outside one to four names is rejected as invalid. `src: Core features, Library rule 5`
- [ ] `C-CF-129` `constraint` A brand kit colour list outside one to eight hex colour strings is rejected as invalid. `src: Core features, Library rule 5`
- [ ] `C-CF-130` `capability` Remix creates a workspace project named after the template. `src: Core features, Remix Describe Code rule 1`
- [ ] `C-CF-131` `data` A remixed project keeps every block instance's parameter values. `src: Core features, Remix Describe Code rule 1`
- [ ] `C-CF-132` `data` A remixed project records the template uuid in `remixed_from`. `src: Core features, Remix Describe Code rule 1`
- [ ] `C-CF-133` `capability` Remixing a premium template from Free is refused with the pinned premium sentence. `src: Core features, Remix Describe Code rule 1`
- [ ] `C-CF-134` `capability` Describe creates a new project from a prompt. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-135` `data` A described project is named after the source project with a running number. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-136` `constraint` Describe places one track per matched library block in prompt order. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-137` `data` Describe sets every prompt parameter to the prompt cut to its maximum length. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-138` `constraint` A successful Describe consumes one project variation. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-139` `capability` A prompt matching no block is rejected with the pinned no-match sentence. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-140` `constraint` A rejected Describe consumes nothing. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-141` `constraint` Describe from a Free workspace is refused as not included. `src: Core features, Remix Describe Code rule 2`
- [ ] `C-CF-142` `constraint` An invalid custom parameter schema is rejected as invalid. `src: Core features, Remix Describe Code rule 3`
- [ ] `C-CF-143` `constraint` The schema refusal names the parameter that failed. `src: Core features, Remix Describe Code rule 3`
- [ ] `C-CF-144` `data` A custom block source is stored plus returned as text. `src: Core features, Remix Describe Code rule 3`
- [ ] `C-CF-145` `capability` A custom block's source runs in the browser isolated from the page. `src: Core features, Remix Describe Code rule 4`
- [ ] `C-CF-146` `capability` A block over its frame budget is paused with the pinned stopped sentence. `src: Core features, Remix Describe Code rule 4`
- [ ] `C-CF-147` `capability` Playback carries on after a block is paused. `src: Core features, Remix Describe Code rule 4`
- [ ] `C-CF-148` `constraint` Pausing a block loses nothing in the project. `src: Core features, Remix Describe Code rule 4`
- [ ] `C-CF-149` `capability` A new project starts at revision 1 with an empty timeline. `src: Core features, Projects rule 1`
- [ ] `C-CF-150` `constraint` A project canvas, frame rate or duration outside the stated ranges is rejected as invalid. `src: Core features, Projects rule 1`
- [ ] `C-CF-151` `data` A timeline item carries an id, a type, a start plus a duration. `src: Core features, Projects rule 2`
- [ ] `C-CF-152` `capability` One track holds clip items beside block items. `src: Core features, Projects rule 2`
- [ ] `C-CF-153` `data` The same block placed twice keeps two independent parameter sets. `src: Core features, Projects rule 2`
- [ ] `C-CF-154` `capability` A save from the stored revision advances the revision by one. `src: Core features, Projects rule 3`
- [ ] `C-CF-155` `constraint` Two saves from the same revision never both land. `src: Core features, Projects rule 3`
- [ ] `C-CF-156` `constraint` A stale-revision save is rejected as a conflict carrying the stored revision. `src: Core features, Projects rule 3`
- [ ] `C-CF-157` `constraint` An item starting before zero or running past the duration is rejected as invalid. `src: Core features, Projects rule 4`
- [ ] `C-CF-158` `constraint` A timeline naming another workspace's asset or saved block is rejected as invalid. `src: Core features, Projects rule 4`
- [ ] `C-CF-159` `constraint` A parameter value outside its declared range is rejected as invalid. `src: Core features, Projects rule 4`
- [ ] `C-CF-160` `capability` Undo reverses editor edits in order across every kind of edit. `src: Core features, Projects rule 5`
- [ ] `C-CF-161` `capability` Redo reapplies undone editor edits in order. `src: Core features, Projects rule 5`
- [ ] `C-CF-162` `capability` Undo plus redo are keyboard reachable in the editor. `src: Core features, Projects rule 5`
- [ ] `C-CF-163` `capability` Playback continues during block rendering. `src: Core features, Projects rule 6`
- [ ] `C-CF-164` `capability` Saving a custom block stores version 1. `src: Core features, Saved blocks rule 1`
- [ ] `C-CF-165` `constraint` The saved-block ceiling counts blocks rather than versions. `src: Core features, Saved blocks rule 1`
- [ ] `C-CF-166` `capability` Editing a saved block stores the next version. `src: Core features, Saved blocks rule 2`
- [ ] `C-CF-167` `data` Earlier block versions are never changed or removed. `src: Core features, Saved blocks rule 2`
- [ ] `C-CF-168` `data` A placed block item keeps the block version of its placement. `src: Core features, Saved blocks rule 2`
- [ ] `C-CF-169` `capability` A placed editor item behind the newest version shows the pinned newer-version marker. `src: Core features, Saved blocks rule 2`
- [ ] `C-CF-170` `capability` Deleting a saved block frees its place under the ceiling. `src: Core features, Saved blocks rule 3`
- [ ] `C-CF-171` `data` Items already placed keep their version after the block is deleted. `src: Core features, Saved blocks rule 3`
- [ ] `C-CF-172` `constraint` A saved block is invisible outside its workspace. `src: Core features, Saved blocks rule 4`
- [ ] `C-CF-173` `constraint` An upload outside the seven accepted types is rejected as invalid. `src: Core features, Media rule 3`
- [ ] `C-CF-174` `capability` Uploaded bytes are written to the object store bucket named by `STORAGE_BUCKET`. `src: Core features, Media rule 1`
- [ ] `C-CF-175` `constraint` Uploaded bytes live nowhere except the object store. `src: Core features, Media rule 1`
- [ ] `C-CF-176` `literal` The asset key follows `assets/{workspace_id}/{sha256_of_bytes}.{ext}`. `src: Core features, Media rule 2`
- [ ] `C-CF-177` `constraint` The same bytes uploaded twice to one workspace leave one object. `src: Core features, Media rule 2`
- [ ] `C-CF-178` `constraint` Asset content streams only to members of its workspace. `src: Core features, Media rule 4`
- [ ] `C-CF-179` `constraint` No stored object is readable at the object store address without credentials. `src: Core features, Media rule 4`
- [ ] `C-CF-180` `constraint` The app never hands a browser a signed object store address. `src: Core features, Media rule 4`
- [ ] `C-CF-181` `capability` Saving a version freezes the current timeline as the next number. `src: Core features, Versions rule 1`
- [ ] `C-CF-182` `data` A version records the frozen project revision. `src: Core features, Versions rule 1`
- [ ] `C-CF-183` `constraint` A version never changes after creation. `src: Core features, Versions rule 1`
- [ ] `C-CF-184` `capability` The versions list returns newest first. `src: Core features, Versions rule 1`
- [ ] `C-CF-185` `capability` An export request returns a job in `rendering` at progress 0. `src: Core features, Versions rule 2`
- [ ] `C-CF-186` `data` An export job is watermarked exactly when the plan is Free. `src: Core features, Versions rule 2`
- [ ] `C-CF-187` `data` An export job is a variation when its size differs from the canvas. `src: Core features, Versions rule 2`
- [ ] `C-CF-188` `constraint` A frame beyond the plan's export ceiling creates no job. `src: Core features, Versions rule 2`
- [ ] `C-CF-189` `constraint` A variation reserves one unit when its job is created. `src: Core features, Versions rule 3`
- [ ] `C-CF-190` `constraint` A ready export settles its reserved unit. `src: Core features, Versions rule 3`
- [ ] `C-CF-191` `constraint` A failed export releases its reserved unit. `src: Core features, Versions rule 3`
- [ ] `C-CF-192` `constraint` A repeated request key returns the same job without a second reservation. `src: Core features, Versions rule 4`
- [ ] `C-CF-193` `constraint` Two simultaneous requests with one key produce one job. `src: Core features, Versions rule 4`
- [ ] `C-CF-194` `constraint` An export file whose first bytes miss the format signature is refused. `src: Core features, Versions rule 5`
- [ ] `C-CF-195` `constraint` An image export whose header size differs from the request is refused. `src: Core features, Versions rule 5`
- [ ] `C-CF-196` `literal` A ready export is stored at `exports/{workspace_id}/{export_id}.{format}`. `src: Core features, Versions rule 5`
- [ ] `C-CF-197` `data` A ready export records `object_key` plus `byte_size`. `src: Core features, Versions rule 5`
- [ ] `C-CF-198` `data` A refused export file marks the job failed with a `failure_reason`. `src: Core features, Versions rule 5`
- [ ] `C-CF-199` `constraint` A refused export file writes no object. `src: Core features, Versions rule 5`
- [ ] `C-CF-200` `constraint` A second upload to a ready export is refused without a second charge. `src: Core features, Versions rule 5`
- [ ] `C-CF-201` `constraint` Export progress never goes down. `src: Core features, Versions rule 6`
- [ ] `C-CF-202` `capability` The fail endpoint marks an export failed. `src: Core features, Versions rule 6`
- [ ] `C-CF-203` `constraint` An export left rendering beyond thirty minutes reads as failed with its unit released. `src: Core features, Versions rule 6`
- [ ] `C-CF-204` `data` An export reports its queue position among earlier rendering jobs. `src: Core features, Versions rule 7`
- [ ] `C-CF-205` `capability` Export progress with its queue position survives a reload of the versions page. `src: Core features, Versions rule 7`
- [ ] `C-CF-206` `capability` A rendering export on the versions page shows the pinned rendering sentence. `src: Core features, Versions rule 8`
- [ ] `C-CF-207` `capability` A failed export on the versions page shows the pinned no-charge sentence. `src: Core features, Versions rule 8`
- [ ] `C-CF-208` `constraint` A ready export file streams only to workspace members. `src: Core features, Versions rule 8`
- [ ] `C-CF-209` `capability` Creating a share returns an id, a token, a url plus a message. `src: Core features, Shares rule 1`
- [ ] `C-CF-210` `data` A share token is sixteen letters or digits. `src: Core features, Shares rule 1`
- [ ] `C-CF-211` `capability` An open share returns the pinned anyone-with-the-link sentence. `src: Core features, Shares rule 1`
- [ ] `C-CF-212` `capability` A share with recipients returns the pinned named-people sentence. `src: Core features, Shares rule 1`
- [ ] `C-CF-213` `capability` Sharing a version without a ready export is refused with the pinned export-first sentence. `src: Core features, Shares rule 1`
- [ ] `C-CF-214` `constraint` A share always shows the version the share was created for. `src: Core features, Shares rule 2`
- [ ] `C-CF-215` `capability` A share of an older version carries the pinned newer-version notice. `src: Core features, Shares rule 2`
- [ ] `C-CF-216` `constraint` A closed superseded share answers the pinned replaced sentence with no media. `src: Core features, Shares rule 2`
- [ ] `C-CF-217` `capability` An expired share answers the pinned expired sentence. `src: Core features, Shares rule 3`
- [ ] `C-CF-218` `constraint` Every endpoint of an expired share is rejected as a client error. `src: Core features, Shares rule 3`
- [ ] `C-CF-219` `constraint` A revoked share serves no media. `src: Core features, Shares rule 3`
- [ ] `C-CF-220` `constraint` A passphrase share serves nothing before unlock. `src: Core features, Shares rule 4`
- [ ] `C-CF-221` `capability` The right passphrase returns an `access_token` for the share. `src: Core features, Shares rule 4`
- [ ] `C-CF-222` `constraint` A wrong passphrase is denied. `src: Core features, Shares rule 4`
- [ ] `C-CF-223` `constraint` After five wrong passphrases the right passphrase is refused too. `src: Core features, Shares rule 4`
- [ ] `C-CF-224` `constraint` A recipients share is served only to a signed-in named account. `src: Core features, Shares rule 5`
- [ ] `C-CF-225` `capability` The stream endpoint serves the ready file inline to an admitted viewer. `src: Core features, Shares rule 6`
- [ ] `C-CF-226` `constraint` The download endpoint refuses whenever download is switched off. `src: Core features, Shares rule 6`
- [ ] `C-CF-227` `capability` The download endpoint serves an attachment when download is switched on. `src: Core features, Shares rule 6`
- [ ] `C-CF-228` `data` Each share page view is recorded with its route. `src: Core features, Shares rule 7`
- [ ] `C-CF-229` `constraint` Only the workspace owner reads the page view log. `src: Core features, Shares rule 7`
- [ ] `C-CF-230` `capability` A workspace member leaves a comment at a moment on a version. `src: Core features, Comments rule 1`
- [ ] `C-CF-231` `capability` An admitted viewer comments through a share when comments are on. `src: Core features, Comments rule 1`
- [ ] `C-CF-232` `constraint` The share comment endpoint refuses when comments are off. `src: Core features, Comments rule 1`
- [ ] `C-CF-233` `data` A comment anchors to the first item under its moment. `src: Core features, Comments rule 2`
- [ ] `C-CF-234` `data` A comment at a moment with no item is `unanchored`. `src: Core features, Comments rule 2`
- [ ] `C-CF-235` `capability` A version's comment list includes comments from earlier versions of the project. `src: Core features, Comments rule 3`
- [ ] `C-CF-236` `data` A carried comment whose item remains is `anchored` at the item's new start plus the offset. `src: Core features, Comments rule 3`
- [ ] `C-CF-237` `data` A carried comment whose item is gone is `orphaned` with the pinned edited-out note. `src: Core features, Comments rule 3`
- [ ] `C-CF-238` `constraint` A comment never moves to a different moment. `src: Core features, Comments rule 3`
- [ ] `C-CF-239` `capability` An approval request creates one pending request per reviewer address. `src: Core features, Approval rule 1`
- [ ] `C-CF-240` `capability` An address with no account receives a review invitation. `src: Core features, Approval rule 1`
- [ ] `C-CF-241` `constraint` Asking the same reviewer about the same version again changes nothing. `src: Core features, Approval rule 1`
- [ ] `C-CF-242` `capability` The approval response carries the pinned waiting sentence. `src: Core features, Approval rule 1`
- [ ] `C-CF-243` `constraint` A version without a ready export cannot be sent for approval. `src: Core features, Approval rule 1`
- [ ] `C-CF-244` `capability` Accepting a review invitation creates a reviewer account with a token. `src: Core features, Approval rule 2`
- [ ] `C-CF-245` `constraint` A reviewer never changes seats or seats used. `src: Core features, Approval rule 2`
- [ ] `C-CF-246` `capability` The reviews list returns only requests addressed to the caller. `src: Core features, Approval rule 3`
- [ ] `C-CF-247` `constraint` A reviewer streams only versions addressed to that reviewer. `src: Core features, Approval rule 3`
- [ ] `C-CF-248` `capability` Reviewer pages carry the pinned guest-scope sentence. `src: Core features, Approval rule 3`
- [ ] `C-CF-249` `constraint` A second decision on one request is refused. `src: Core features, Approval rule 4`
- [ ] `C-CF-250` `constraint` A decision from anyone but the addressed reviewer is denied. `src: Core features, Approval rule 4`
- [ ] `C-CF-251` `data` A version approval state is derived from its requests. `src: Core features, Approval rule 5`
- [ ] `C-CF-252` `data` Any request asking for changes makes the version `changes_requested`. `src: Core features, Approval rule 5`
- [ ] `C-CF-253` `data` A version with every request approved reads `approved`. `src: Core features, Approval rule 5`
- [ ] `C-CF-254` `data` A project approval status follows its newest version. `src: Core features, Approval rule 6`
- [ ] `C-CF-255` `constraint` A save after approval marks the project `outdated`. `src: Core features, Approval rule 6`
- [ ] `C-CF-256` `capability` A reviewer is notified once per approval request. `src: Core features, Notifications rule 1`
- [ ] `C-CF-257` `capability` The requester is notified once per decision. `src: Core features, Notifications rule 1`
- [ ] `C-CF-258` `constraint` A retried request notifies nobody a second time. `src: Core features, Notifications rule 2`
- [ ] `C-CF-259` `constraint` Notifications stay inside the app with no email, SMS or push. `src: Core features, Notifications rule 2`
- [ ] `C-CF-260` `data` A placed instance keeps the block name of its placement version. `src: Core features, Compound cases rule 1`
- [ ] `C-CF-261` `capability` A stopped member-written block leaves the rest of the frame playing. `src: Core features, Compound cases rule 2`
- [ ] `C-CF-262` `capability` Reloading the versions page resumes a member's rendering export. `src: Core features, Compound cases rule 3`
- [ ] `C-CF-263` `constraint` A reconnecting member's save meets the revision rule. `src: Core features, Compound cases rule 4`
- [ ] `C-CF-264` `constraint` Removing a member fails that member's rendering export with its unit released. `src: Core features, Compound cases rule 5`
- [ ] `C-CF-265` `data` Ready exports of a removed member stay in the workspace. `src: Core features, Compound cases rule 5`
- [ ] `C-CF-266` `literal` The home route carries the title `Ferment Video : Online Video Editor Engineered for Creativity`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-267` `literal` The product route carries the title `Creative Code Video Editor & Motion Design Tools : Ferment`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-268` `literal` The pricing route carries the title `Pricing : Ferment`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-269` `literal` The contact route carries the title `Contact Ferment : Video Editor Sales & Support`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-270` `literal` The blog route carries the title `Ferment Blog`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-271` `literal` The login route carries the title `Login to Ferment`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-272` `literal` The signup route carries the title `Sign up`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-273` `literal` The dashboard route carries the title `Explore : Ferment`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-274` `literal` The template gallery carries the title `Templates : Ferment`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-275` `literal` The block library carries the title `Blocks : Ferment`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-276` `literal` The privacy route carries the title `Privacy Policy : Ferment`. `src: Core features, Marketing rule 1`
- [ ] `C-CF-277` `constraint` No two public routes share a meta description. `src: Core features, Marketing rule 1`
- [ ] `C-CF-278` `constraint` Public routes render from stored content. `src: Core features, Marketing rule 1`
- [ ] `C-CF-279` `capability` Every document declares a favicon that answers with an image. `src: Core features, Marketing rule 2`
- [ ] `C-CF-280` `capability` The home route carries its eleven bands in order. `src: Core features, Marketing rule 3`
- [ ] `C-CF-281` `data` The customer wall shows only approved customer names in stored order. `src: Core features, Marketing rule 3`
- [ ] `C-CF-282` `capability` The blog index filters by its three category chips. `src: Core features, Marketing rule 4`
- [ ] `C-CF-283` `capability` Each blog post has its own route. `src: Core features, Marketing rule 4`
- [ ] `C-CF-284` `capability` The contact form asks for the audience before the other fields. `src: Core features, Marketing rule 5`
- [ ] `C-CF-285` `data` A contact request is stored with its audience. `src: Core features, Marketing rule 5`
- [ ] `C-CF-286` `literal` A contact request answers with a reference starting `FC-`. `src: Core features, Marketing rule 5`
- [ ] `C-CF-287` `constraint` A repeated contact request within ten minutes returns the first reference. `src: Core features, Marketing rule 5`
- [ ] `C-CF-288` `constraint` A contact message under twenty characters is rejected as invalid. `src: Core features, Marketing rule 5`
- [ ] `C-CF-289` `capability` Every form flags invalid input next to the field named. `src: Core features, Marketing rule 6`
- [ ] `C-CF-290` `constraint` An invalid form submission writes nothing. `src: Core features, Marketing rule 6`
- [ ] `C-CF-291` `constraint` The server rejects an invalid body with a message naming the field. `src: Core features, Marketing rule 6`
- [ ] `C-CF-292` `capability` The privacy, cookie plus terms pages are real pages on the same origin. `src: Core features, Marketing rule 7`
- [ ] `C-CF-293` `capability` Every footer links the privacy, cookie plus terms pages. `src: Core features, Marketing rule 7`
- [ ] `C-CF-294` `capability` The privacy page names what Ferment stores about members, reviewers plus visitors. `src: Core features, Marketing rule 7`
- [ ] `C-CF-295` `capability` The privacy page states how long each kind of record is kept. `src: Core features, Marketing rule 7`
- [ ] `C-CF-296` `constraint` Every internal link on every public route resolves. `src: Core features, Marketing rule 7`
- [ ] `C-CF-297` `capability` The plugin page says the plugin is not available yet. `src: Core features, Marketing rule 8`
- [ ] `C-CF-298` `capability` A signed-out request for projects redirects to login carrying the requested path. `src: Core features, Marketing rule 9`
- [ ] `C-CF-299` `capability` Signing in from a redirect returns to the requested path. `src: Core features, Marketing rule 9`
- [ ] `C-CF-300` `capability` A first-time visitor sees the consent panel with five categories. `src: Core features, Consent rule 1`
- [ ] `C-CF-301` `capability` The necessary consent category shows as locked on. `src: Core features, Consent rule 1`
- [ ] `C-CF-302` `capability` Rejecting consent takes as many actions as accepting consent. `src: Core features, Consent rule 1`
- [ ] `C-CF-303` `data` A consent choice is stored per category with its time. `src: Core features, Consent rule 2`
- [ ] `C-CF-304` `data` A consent record stores the exact wording shown. `src: Core features, Consent rule 2`
- [ ] `C-CF-305` `capability` The consent read returns the latest choice per category. `src: Core features, Consent rule 2`
- [ ] `C-CF-306` `capability` Refusing the experience consent category shows still frames in place of the live scene. `src: Core features, Consent rule 3`
- [ ] `C-CF-307` `capability` The consent panel says the marketing category covers nothing. `src: Core features, Consent rule 3`
- [ ] `C-CF-308` `constraint` A marketing view is refused without granted measurement consent. `src: Core features, Consent rule 4`
- [ ] `C-CF-309` `constraint` A refused marketing view records nothing. `src: Core features, Consent rule 4`
- [ ] `C-CF-310` `capability` The footer cookie settings control reopens the consent panel. `src: Core features, Consent rule 5`
- [ ] `C-CF-311` `capability` An unknown address renders the pinned not-found heading. `src: Core features, Not found rule 1`
- [ ] `C-CF-312` `constraint` An unknown address answers with a not-found status. `src: Core features, Not found rule 1`
- [ ] `C-CF-313` `capability` The not-found page links back to the home, templates plus pricing routes. `src: Core features, Not found rule 1`
- [ ] `C-CF-314` `constraint` An unknown API address answers JSON with the error `not_found`. `src: Core features, Not found rule 2`
- [ ] `C-CF-315` `constraint` The graphql address under the API answers a JSON not-found error. `src: Core features, Not found rule 2`
- [ ] `C-CF-316` `constraint` An unknown creator, blog post or share token renders the not-found page. `src: Core features, Not found rule 3`

## C-UF User flow

- [ ] `C-UF-01` `capability` Every public route in the route table renders. `src: User flow, route table`
- [ ] `C-UF-02` `capability` Every member route in the route table renders for a signed-in member. `src: User flow, route table`
- [ ] `C-UF-03` `capability` A signed-out request for a guarded route lands on login with the path. `src: User flow, Entry and redirects`
- [ ] `C-UF-04` `capability` A member signing in without a destination lands on the dashboard. `src: User flow, Entry and redirects`
- [ ] `C-UF-05` `capability` A reviewer signing in lands on the review inbox. `src: User flow, Entry and redirects`
- [ ] `C-UF-06` `constraint` A reviewer asking for a member route is refused. `src: User flow, Entry and redirects`
- [ ] `C-UF-07` `capability` Signing out returns to the home route. `src: User flow, Entry and redirects`
- [ ] `C-UF-08` `constraint` A signed-out browser opens no guarded route. `src: User flow, Entry and redirects`
- [ ] `C-UF-09` `capability` The header shows Login plus Try for free when signed out. `src: User flow, Entry and redirects`
- [ ] `C-UF-10` `capability` The header shows Projects plus Dashboard when signed in. `src: User flow, Entry and redirects`
- [ ] `C-UF-11` `capability` An expired share link says so on its own page. `src: User flow, Entry and redirects`
- [ ] `C-UF-12` `capability` A visitor chooses a plan from the pricing route before registering. `src: User flow, Journeys 1`
- [ ] `C-UF-13` `capability` A member remixes a template before tuning a block on the timeline. `src: User flow, Journeys 2`
- [ ] `C-UF-14` `capability` A member saves a block for the team before deleting the saved block. `src: User flow, Journeys 3`
- [ ] `C-UF-15` `capability` A member exports a version before sharing the version with download off. `src: User flow, Journeys 4`
- [ ] `C-UF-16` `capability` A reviewer approves a version sent by a member. `src: User flow, Journeys 5`
- [ ] `C-UF-17` `capability` A Free member meets the saved-block ceiling. `src: User flow, Journeys 6`
- [ ] `C-UF-18` `capability` A workspace owner meets the Pro seat cap. `src: User flow, Journeys 7`
- [ ] `C-UF-19` `capability` A visitor rejects cookies before accepting cookies from the footer. `src: User flow, Journeys 8`
- [ ] `C-UF-20` `capability` A second reviewer finds an empty review inbox. `src: User flow, Journeys 9`
- [ ] `C-UF-21` `ui` Every list shows an empty state naming its creating action. `src: User flow, States`
- [ ] `C-UF-22` `ui` Every route shows a loading state shaped like its content. `src: User flow, States`
- [ ] `C-UF-23` `capability` A failed panel offers a retry without taking the route down. `src: User flow, States`
- [ ] `C-UF-24` `capability` An export shows rendering, ready or failed after a reload. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The first screen presents the timeline as a surface of adjustable tools. `src: UI/UX notes, north star`
- [ ] `C-UX-02` `ui` The marketing site carries editorial atmosphere with the live product seen first. `src: UI/UX notes, register`
- [ ] `C-UX-03` `ui` The editor reads as a dense, quiet operational tool. `src: UI/UX notes, register`
- [ ] `C-UX-04` `ui` Every surface keeps to black, white or grey outside the brand gradient. `src: UI/UX notes, register stances`
- [ ] `C-UX-05` `ui` The editor is designed dark throughout. `src: UI/UX notes, mode`
- [ ] `C-UX-06` `ui` The marketing site alternates designed dark bands with designed light bands. `src: UI/UX notes, mode`
- [ ] `C-UX-07` `ui` The green to amber to orange gradient is the only chromatic colour. `src: UI/UX notes, palette`
- [ ] `C-UX-08` `ui` The brand gradient never appears as a flat fill, a text colour or a status colour. `src: UI/UX notes, palette`
- [ ] `C-UX-09` `ui` Text hierarchy comes from opacity on two anchors. `src: UI/UX notes, palette`
- [ ] `C-UX-10` `ui` A red appears only for failure or destruction. `src: UI/UX notes, palette`
- [ ] `C-UX-11` `ui` A gradient outline marks something rendering or waiting. `src: UI/UX notes, palette`
- [ ] `C-UX-12` `ui` Success shows as a word with a tick on a neutral chip. `src: UI/UX notes, palette`
- [ ] `C-UX-13` `ui` The gradient outline runs colour around roughly two fifths of its edge. `src: UI/UX notes, glowing outline`
- [ ] `C-UX-14` `ui` The most popular pricing card wears the lopsided gradient outline. `src: UI/UX notes, glowing outline`
- [ ] `C-UX-15` `ui` Raised dark surfaces show distinguishable levels with shrinking steps. `src: UI/UX notes, elevation`
- [ ] `C-UX-16` `ui` The timeline separates tracks from items by elevation rather than borders. `src: UI/UX notes, elevation`
- [ ] `C-UX-17` `ui` One grotesque family in two widths carries the product. `src: UI/UX notes, type`
- [ ] `C-UX-18` `ui` A monospace appears only in the code editor or beside aligned numbers. `src: UI/UX notes, type`
- [ ] `C-UX-19` `ui` Reading pages enlarge with the browser text size. `src: UI/UX notes, type`
- [ ] `C-UX-20` `ui` Editor chrome keeps a fixed scale under browser text enlargement. `src: UI/UX notes, type`
- [ ] `C-UX-21` `capability` The interface scale setting enlarges the editor chrome together. `src: UI/UX notes, type`
- [ ] `C-UX-22` `ui` Marketing display headings size with the window width. `src: UI/UX notes, type`
- [ ] `C-UX-23` `ui` Stacked amounts, timecodes or counts align in columns. `src: UI/UX notes, type`
- [ ] `C-UX-24` `ui` Cards round most, fields round less, pills round fully. `src: UI/UX notes, shape`
- [ ] `C-UX-25` `ui` The marketing site separates sections with space rather than rules. `src: UI/UX notes, shape`
- [ ] `C-UX-26` `ui` The editor fits stage, timeline plus panel on one laptop screen. `src: UI/UX notes, density`
- [ ] `C-UX-27` `ui` The application keeps a persistent left sidebar. `src: UI/UX notes, density`
- [ ] `C-UX-28` `ui` Movement arrives quickly before settling slowly. `src: UI/UX notes, motion`
- [ ] `C-UX-29` `ui` Nothing loops on its own except the customer wall. `src: UI/UX notes, motion`
- [ ] `C-UX-30` `ui` Entering elements rise into place with the fade finishing first. `src: UI/UX notes, motion`
- [ ] `C-UX-31` `ui` Headings arrive a line at a time from each line's own height. `src: UI/UX notes, motion`
- [ ] `C-UX-32` `ui` The home statement arrives a word at a time. `src: UI/UX notes, motion`
- [ ] `C-UX-33` `ui` Horizontal rules draw themselves open. `src: UI/UX notes, motion`
- [ ] `C-UX-34` `ui` Scrolling back never replays a reveal. `src: UI/UX notes, motion`
- [ ] `C-UX-35` `ui` One shared set of easing curves serves the whole product. `src: UI/UX notes, motion`
- [ ] `C-UX-36` `ui` The dial knob is the only element that overshoots. `src: UI/UX notes, motion`
- [ ] `C-UX-37` `capability` A reduced-motion request resolves every reveal at once. `src: UI/UX notes, motion`
- [ ] `C-UX-38` `capability` A reduced-motion request holds the home scene on its still frame. `src: UI/UX notes, motion`
- [ ] `C-UX-39` `ui` Every control shows resting, pointed-at, pressed, focused plus unavailable states. `src: UI/UX notes, components`
- [ ] `C-UX-40` `ui` An unavailable control is marked by more than colour. `src: UI/UX notes, components`
- [ ] `C-UX-41` `ui` Hover styling applies only where a pointer can hover. `src: UI/UX notes, components`
- [ ] `C-UX-42` `ui` Each view leads with one main action. `src: UI/UX notes, components`
- [ ] `C-UX-43` `capability` Escape closes an open panel before returning focus to its opener. `src: UI/UX notes, components`
- [ ] `C-UX-44` `capability` A destructive action asks once in its row before acting. `src: UI/UX notes, components`
- [ ] `C-UX-45` `ui` Every form control keeps a visible label. `src: UI/UX notes, components`
- [ ] `C-UX-46` `ui` The product meets WCAG 2.2 level AA. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-47` `literal` Body text reaches a contrast of `4.5:1` against its ground. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-48` `literal` Large text with interface components reaches a contrast of `3:1`. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-49` `ui` Touch targets meet the WCAG 2.2 minimum target size. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-50` `capability` Keyboard navigation reaches every control, timeline items among them. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-51` `ui` Every focused element shows a visible focus indicator. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-52` `capability` A dial changes one step per arrow key. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-53` `capability` A dial announces its value to assistive technology. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-54` `capability` The skip link is the first focusable element on every route. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-55` `capability` A split heading also exists as one intact string for assistive technology. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-56` `capability` The home scene carries no accessible role of its own. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-57` `capability` Icon-only controls carry text labels. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-58` `ui` Nothing flashes more than three times a second. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-59` `ui` The layout holds at every viewport width from phone to desktop. `src: UI/UX notes, responsive`
- [ ] `C-UX-60` `ui` At the wider breakpoint pricing cards drop to two across. `src: UI/UX notes, responsive`
- [ ] `C-UX-61` `ui` At the narrower breakpoint navigation becomes one toggle opening a full panel. `src: UI/UX notes, responsive`
- [ ] `C-UX-62` `ui` At phone widths a project opens as a read-only playable preview. `src: UI/UX notes, responsive`
- [ ] `C-UX-63` `ui` No route scrolls sideways outside the marquees or wide tables. `src: UI/UX notes, responsive`
- [ ] `C-UX-64` `ui` No page is washed in one hue or uses the gradient as a flat background. `src: UI/UX notes, what it must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every route arrives as complete server-rendered HTML on first paint. `src: Technical requirements, bullet 1`
- [ ] `C-TR-02` `capability` The browser draws the home scene, block previews plus export frames itself. `src: Technical requirements, bullet 1`
- [ ] `C-TR-03` `capability` The HTTP API is served under the API prefix on the same origin as the pages. `src: Technical requirements, bullet 2`
- [ ] `C-TR-04` `contract` The app reaches PostgreSQL at `DATABASE_URL`. `src: Technical requirements, bullet 3`
- [ ] `C-TR-05` `contract` The app reaches MinIO at `STORAGE_ENDPOINT` with the storage credentials. `src: Technical requirements, bullet 4`
- [ ] `C-TR-06` `contract` The bucket named by the storage bucket variable already exists privately. `src: Technical requirements, bullet 4`
- [ ] `C-TR-07` `contract` Passwords are hashed with a slow salted algorithm. `src: Technical requirements, bullet 5`
- [ ] `C-TR-08` `literal` The health route answers `{"status": "ok"}`. `src: Technical requirements, bullet 6`
- [ ] `C-TR-09` `contract` Health answers once PostgreSQL plus MinIO are reachable. `src: Technical requirements, bullet 6`
- [ ] `C-TR-10` `contract` The app uses no backing service beyond PostgreSQL plus MinIO. `src: Technical requirements, libraries paragraph`
- [ ] `C-TR-11` `contract` The app starts no copy of PostgreSQL or MinIO. `src: Technical requirements, already running paragraph`
- [ ] `C-TR-12` `constraint` Nothing the browser downloads carries a credential. `src: Technical requirements, bullet 7`
- [ ] `C-TR-13` `constraint` Public routes fetch nothing from another origin at runtime. `src: Technical requirements, bullet 8`
- [ ] `C-TR-14` `capability` Every public route declares a favicon in its head. `src: Technical requirements, bullet 8`
- [ ] `C-TR-15` `capability` Only the two used type widths load, in one web font format. `src: Technical requirements, bullet 9`
- [ ] `C-TR-16` `capability` The heading plus call to action paint before the home scene loads. `src: Technical requirements, bullet 10`
- [ ] `C-TR-17` `contract` Every timestamp is UTC ISO 8601 ending in `Z`. `src: Technical requirements, bullet 11`
- [ ] `C-TR-18` `contract` A list endpoint returns a top-level JSON array. `src: Technical requirements, bullet 12`

## C-DM Data model

- [ ] `C-DM-01` `data` The store holds the named tables, each with an integer `id`. `src: Data model, para 1`
- [ ] `C-DM-02` `literal` Every seeded login is written to `/app/USER_README.md` with the corpus password. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` The `account` table stores `email` lowercased beside a `role`. `src: Data model, account bullet`
- [ ] `C-DM-04` `data` An account appears at most once per workspace in `workspace_member`. `src: Data model, workspace_member bullet`
- [ ] `C-DM-05` `data` An `invitation` state is pending, accepted or revoked. `src: Data model, invitation bullet`
- [ ] `C-DM-06` `data` The `plan` table stores both price figures per plan. `src: Data model, plan bullet`
- [ ] `C-DM-07` `data` The `quota` table stores one row per plan for each meter. `src: Data model, quota bullet`
- [ ] `C-DM-08` `data` The `subscription` table holds one row per workspace. `src: Data model, subscription bullet`
- [ ] `C-DM-09` `data` The `charge` table stores amounts in cents with a `currency`. `src: Data model, charge bullet`
- [ ] `C-DM-10` `data` A `meter_balance` row never holds usage above its limit. `src: Data model, meter_balance bullet`
- [ ] `C-DM-11` `data` A `usage_event` state is reserved, settled or released. `src: Data model, usage_event bullet`
- [ ] `C-DM-12` `data` A stored `block_version` row never changes. `src: Data model, block_version bullet`
- [ ] `C-DM-13` `data` The `template` table stores each template under a unique `uuid`. `src: Data model, template bullet`
- [ ] `C-DM-14` `data` The `asset` table stores each object key once. `src: Data model, asset bullet`
- [ ] `C-DM-15` `data` The `project` table stores the timeline with its `revision`. `src: Data model, project bullet`
- [ ] `C-DM-16` `data` Version numbers are unique within a project. `src: Data model, project_version bullet`
- [ ] `C-DM-17` `data` The `export_job` table holds one job per workspace request key. `src: Data model, export_job bullet`
- [ ] `C-DM-18` `data` The `share_link` table stores each token once with a hashed passphrase. `src: Data model, share_link bullet`
- [ ] `C-DM-19` `data` The `share_view` table records each share page view. `src: Data model, share_view bullet`
- [ ] `C-DM-20` `data` The `comment` table stores the anchor item with its offset. `src: Data model, comment bullet`
- [ ] `C-DM-21` `data` The `approval_request` table holds one request per version for each reviewer. `src: Data model, approval_request bullet`
- [ ] `C-DM-22` `data` The `notification` table holds one row per event key. `src: Data model, notification bullet`
- [ ] `C-DM-23` `data` The `consent_record` table stores the wording shown. `src: Data model, consent_record bullet`
- [ ] `C-DM-24` `constraint` Approval states, usage figures plus savings are derived rather than stored columns. `src: Data model, derived paragraph`
- [ ] `C-DM-25` `data` The five plans are seeded with their quotas plus features. `src: Data model, seed data bullet 1`
- [ ] `C-DM-26` `data` The eight blocks, eight templates plus three creators are seeded. `src: Data model, seed data bullet 2`
- [ ] `C-DM-27` `data` The Denim Drop template holds a Glow item from 0 to 5000 ms beside a clip from 10000 ms. `src: Data model, seed data bullet 2`
- [ ] `C-DM-28` `data` Juniper Goods is a monthly Pro workspace whose period started ten days before first start. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-29` `data` Juniper Goods holds two members with seven pending invitations. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-30` `literal` Juniper Goods carries one plan change charge of `7600`. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-31` `data` Juniper Goods holds four brand kits. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-32` `data` Juniper Goods holds three saved blocks, Spin Forever among them. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-33` `data` Denim Drop remix sits at revision 2 with two versions. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-34` `data` Version 1 of Denim Drop remix has a ready png export approved by the first reviewer. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-35` `data` Version 2 of Denim Drop remix has a ready png export awaiting the first reviewer. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-36` `data` Version 1 of Denim Drop remix carries the two seeded reviewer comments. `src: Data model, seed data Juniper Goods bullet`
- [ ] `C-DM-37` `literal` Share `k7Qm2pVx9LwR4tNz` is open with download off. `src: Data model, seed data shares table row 1`
- [ ] `C-DM-38` `literal` Share `pQ4rT8vW2yZ6aB3c` expired a day before first start. `src: Data model, seed data shares table row 2`
- [ ] `C-DM-39` `literal` Share `mN5bV7cX1zL3kJ9h` needs the passphrase `orchard-lantern-42`. `src: Data model, seed data shares table row 3`
- [ ] `C-DM-40` `literal` Share `dR2fG6hJ8kL0pQ1s` admits only the first seeded reviewer. `src: Data model, seed data shares table row 4`
- [ ] `C-DM-41` `data` The open seeded share carries three recorded views. `src: Data model, seed data shares table row 1`
- [ ] `C-DM-42` `data` Solo Sketchbook holds four saved blocks on the Free plan. `src: Data model, seed data Solo Sketchbook bullet`
- [ ] `C-DM-43` `data` First Sketch is a 1280 by 720 project with no versions. `src: Data model, seed data Solo Sketchbook bullet`
- [ ] `C-DM-44` `data` Basic Bench holds nineteen settled variations in the current window. `src: Data model, seed data Basic Bench bullet`
- [ ] `C-DM-45` `data` Basic Bench holds twenty settled variations in the previous window. `src: Data model, seed data Basic Bench bullet`
- [ ] `C-DM-46` `literal` The `stale-bench-1` export on Bench Promo reads as failed. `src: Data model, seed data Basic Bench bullet`
- [ ] `C-DM-47` `data` Version 1 of Bench Promo has no ready export. `src: Data model, seed data Basic Bench bullet`
- [ ] `C-DM-48` `data` Twenty-four approved customer names are seeded in order beside one withdrawn name. `src: Data model, seed data customer bullet`
- [ ] `C-DM-49` `data` Three blog posts are seeded with their slugs. `src: Data model, seed data blog bullet`
- [ ] `C-DM-50` `data` Each public route has one stored page row with its title. `src: Data model, seed data page bullet`
- [ ] `C-DM-51` `contract` Seeded export files are written to the bucket at their keys. `src: Data model, seed data export bullet`
- [ ] `C-DM-52` `contract` A restart duplicates no seeded row. `src: Data model, seeding paragraph`
- [ ] `C-DM-53` `contract` A restart writes no second copy of a seeded object. `src: Data model, seeding paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `capability` The block library plus the template gallery are browsable signed out. `src: Front-end specification, information architecture`
- [ ] `C-FE-02` `constraint` The product has no site search. `src: Front-end specification, information architecture`
- [ ] `C-FE-03` `ui` One shared token set styles the marketing site plus the application. `src: Front-end specification, component architecture`
- [ ] `C-FE-04` `ui` Every revealing element behaves identically. `src: Front-end specification, component architecture`
- [ ] `C-FE-05` `constraint` No route requests an image file for the interface. `src: Front-end specification, zero-asset rule`
- [ ] `C-FE-06` `ui` Customer names on the home wall appear as type rather than drawn logos. `src: Front-end specification, zero-asset rule`
- [ ] `C-FE-07` `ui` The consent panel sits above every other layer. `src: Front-end specification, stacking`
- [ ] `C-FE-08` `ui` The marketing header is a floating pill beside a separate account pill. `src: Front-end specification, header`
- [ ] `C-FE-09` `ui` Scrolling down narrows the left header pill to the wordmark plus ellipsis. `src: Front-end specification, header`
- [ ] `C-FE-10` `ui` The right header pill keeps its place during the collapse. `src: Front-end specification, header`
- [ ] `C-FE-11` `capability` The header navigation lists Product, Blocks, Templates, Pricing plus Blog. `src: Front-end specification, header`
- [ ] `C-FE-12` `literal` Inner marketing routes show the tagline `Add Ferment`. `src: Front-end specification, header`
- [ ] `C-FE-13` `ui` The narrow navigation panel shows a subtitle under each item. `src: Front-end specification, header`
- [ ] `C-FE-14` `literal` The narrow Blocks item carries the subtitle `Browse 1000s of Ferment blocks`. `src: Front-end specification, header`
- [ ] `C-FE-15` `ui` The skip link becomes visible when focused. `src: Front-end specification, skip link`
- [ ] `C-FE-16` `capability` The footer carries Explore, Socials, Resources plus Legal columns. `src: Front-end specification, footer`
- [ ] `C-FE-17` `constraint` Each social network links the same account everywhere. `src: Front-end specification, footer`
- [ ] `C-FE-18` `literal` The footer reads `Copyright (C) 2026 Ferment`. `src: Front-end specification, footer`
- [ ] `C-FE-19` `ui` The consent panel rises from the bottom on a dark ground. `src: Front-end specification, consent panel`
- [ ] `C-FE-20` `capability` The open consent panel holds keyboard focus inside the panel. `src: Front-end specification, consent panel`
- [ ] `C-FE-21` `capability` The consent panel is announced when shown. `src: Front-end specification, consent panel`
- [ ] `C-FE-22` `capability` The learn more control expands each consent category description in place. `src: Front-end specification, consent panel`
- [ ] `C-FE-23` `ui` The home hero shows a live keychain hanging from above. `src: Front-end specification, home hero`
- [ ] `C-FE-24` `ui` The keychain chain is one repeated link with distinct charms. `src: Front-end specification, home hero`
- [ ] `C-FE-25` `ui` The keychain chain, clasp plus key read as polished metal. `src: Front-end specification, home hero`
- [ ] `C-FE-26` `capability` A still frame of the same keychain composition shows during scene loading. `src: Front-end specification, home hero`
- [ ] `C-FE-27` `capability` The hero heading plus Get Started action are readable before the scene arrives. `src: Front-end specification, home hero`
- [ ] `C-FE-28` `capability` The hero Get Started action leads to the signup route. `src: Front-end specification, home hero`
- [ ] `C-FE-29` `ui` The customer wall is a continuous marquee that pauses when pointed at. `src: Front-end specification, home bands`
- [ ] `C-FE-30` `capability` The home statement carries the pinned statement sentence. `src: Front-end specification, home bands`
- [ ] `C-FE-31` `ui` The home blocks band shows live Inflate, Glow, Focus plus Halftone previews. `src: Front-end specification, home bands`
- [ ] `C-FE-32` `ui` The home customisation band shows a live dial with four vertical sliders. `src: Front-end specification, home bands`
- [ ] `C-FE-33` `capability` The home pillars band names Import, Edit, Enhance plus Ship. `src: Front-end specification, home bands`
- [ ] `C-FE-34` `capability` The home three-ways band gives Remix, Describe plus Code each a body line. `src: Front-end specification, home bands`
- [ ] `C-FE-35` `constraint` The two home production headings carry different body copy. `src: Front-end specification, home bands`
- [ ] `C-FE-36` `capability` The home showcase credits the three creators. `src: Front-end specification, home bands`
- [ ] `C-FE-37` `ui` A home band without footage shows a drawn timeline diagram. `src: Front-end specification, home bands`
- [ ] `C-FE-38` `capability` The product route expands the four pillars into bands. `src: Front-end specification, product route`
- [ ] `C-FE-39` `ui` Switching the pricing billing period changes prices without a reload or card resizing. `src: Front-end specification, pricing route`
- [ ] `C-FE-40` `ui` Four purchasable pricing cards sit side by side above the Enterprise card on a wide screen. `src: Front-end specification, pricing route`
- [ ] `C-FE-41` `ui` The pricing comparison table keeps its row labels plus plan names in view. `src: Front-end specification, pricing route`
- [ ] `C-FE-42` `ui` The pricing comparison table states missing rows in words. `src: Front-end specification, pricing route`
- [ ] `C-FE-43` `ui` Template gallery cards preview their template whenever on screen. `src: Front-end specification, template gallery`
- [ ] `C-FE-44` `capability` The template gallery category chips allow several at once. `src: Front-end specification, template gallery`
- [ ] `C-FE-45` `capability` A filtered template gallery view survives a reload through the address. `src: Front-end specification, template gallery`
- [ ] `C-FE-46` `capability` The template route shows the preview, the credit, the block list plus the Remix action. `src: Front-end specification, template route`
- [ ] `C-FE-47` `capability` A signed-out Remix on the template route goes through sign-in before returning. `src: Front-end specification, template route`
- [ ] `C-FE-48` `ui` The block library groups blocks under category tabs. `src: Front-end specification, block library`
- [ ] `C-FE-49` `capability` The block library name filter settles once typing pauses. `src: Front-end specification, block library`
- [ ] `C-FE-50` `capability` An opened library block shows its generated control panel beside its preview. `src: Front-end specification, block library`
- [ ] `C-FE-51` `ui` The blog index shows each post as a dated row with a category chip. `src: Front-end specification, blog routes`
- [ ] `C-FE-52` `capability` The contact route first asks what the visitor needs help with. `src: Front-end specification, contact route`
- [ ] `C-FE-53` `capability` A sent contact form is replaced by a confirmation carrying the reference. `src: Front-end specification, contact route`
- [ ] `C-FE-54` `ui` Login plus signup are single centred forms with persistent labels. `src: Front-end specification, authentication routes`
- [ ] `C-FE-55` `capability` The signup route states the Free plan the new workspace starts on. `src: Front-end specification, authentication routes`
- [ ] `C-FE-56` `capability` The application sidebar holds Home, Explore, Favorites plus a Workspace group. `src: Front-end specification, application shell`
- [ ] `C-FE-57` `capability` The sidebar workspace switcher lists every workspace the member belongs to. `src: Front-end specification, application shell`
- [ ] `C-FE-58` `literal` The dashboard leads with `Seed Blocks` subtitled `Start with a block`. `src: Front-end specification, application shell`
- [ ] `C-FE-59` `ui` The projects route is a sortable table with approval status in words. `src: Front-end specification, application shell`
- [ ] `C-FE-60` `capability` A new project is created in place from a row at the top of the projects table. `src: Front-end specification, application shell`
- [ ] `C-FE-61` `ui` The editor shows stage, timeline plus parameter panel on one screen. `src: Front-end specification, editor`
- [ ] `C-FE-62` `ui` The editor transport row shows playhead time beside the duration. `src: Front-end specification, editor`
- [ ] `C-FE-63` `capability` A timeline track label is renamed in place. `src: Front-end specification, editor`
- [ ] `C-FE-64` `ui` Timeline block items show their block name with a live thumbnail. `src: Front-end specification, editor`
- [ ] `C-FE-65` `ui` A playhead line crosses every timeline track. `src: Front-end specification, editor`
- [ ] `C-FE-66` `ui` A dial control is a round knob showing its value in degrees. `src: Front-end specification, editor`
- [ ] `C-FE-67` `ui` A slider control shows its handle beside its value. `src: Front-end specification, editor`
- [ ] `C-FE-68` `ui` A prompt control shows how many characters remain. `src: Front-end specification, editor`
- [ ] `C-FE-69` `capability` A code parameter opens a monospace editor with line numbers. `src: Front-end specification, editor`
- [ ] `C-FE-70` `capability` Code parameter errors appear beneath the editor without breaking the stage. `src: Front-end specification, editor`
- [ ] `C-FE-71` `capability` The editor shows a saved, saving or unsaved state beside the project name. `src: Front-end specification, editor`
- [ ] `C-FE-72` `capability` The editor library drawer filters blocks for dropping onto a track. `src: Front-end specification, editor`
- [ ] `C-FE-73` `capability` A block can be placed on a timeline track from the keyboard. `src: Front-end specification, editor`
- [ ] `C-FE-74` `capability` The editor save-as-block action opens an inline form for name plus category. `src: Front-end specification, editor`
- [ ] `C-FE-75` `capability` A paused editor block offers a restart action. `src: Front-end specification, editor`
- [ ] `C-FE-76` `ui` The versions route lists versions newest first with exports nested beneath. `src: Front-end specification, versions route`
- [ ] `C-FE-77` `capability` The versions export row prefills the canvas size before marking a variation once changed. `src: Front-end specification, versions route`
- [ ] `C-FE-78` `ui` A rendering export on the versions route shows a progress bar with its queue position. `src: Front-end specification, versions route`
- [ ] `C-FE-79` `capability` The versions share row offers allow-download plus allow-comments switches. `src: Front-end specification, versions route`
- [ ] `C-FE-80` `capability` Creating a share lands on a confirmation carrying the share link. `src: Front-end specification, versions route`
- [ ] `C-FE-81` `capability` Requesting approval lands on a confirmation carrying the waiting sentence. `src: Front-end specification, versions route`
- [ ] `C-FE-82` `ui` The share page player shows the version at its own proportion. `src: Front-end specification, share page`
- [ ] `C-FE-83` `capability` Comment markers on the share scrubber move the playhead when chosen. `src: Front-end specification, share page`
- [ ] `C-FE-84` `capability` A passphrase share page first shows one passphrase field with a view action. `src: Front-end specification, share page`
- [ ] `C-FE-85` `constraint` A share page with download off shows no download control. `src: Front-end specification, share page`
- [ ] `C-FE-86` `capability` A share page with comments on posts a comment at the playhead time. `src: Front-end specification, share page`
- [ ] `C-FE-87` `ui` The review inbox is a table of approval requests. `src: Front-end specification, reviewer surfaces`
- [ ] `C-FE-88` `capability` The review page offers approve plus request-changes actions with an optional note. `src: Front-end specification, reviewer surfaces`
- [ ] `C-FE-89` `capability` A review decision lands on a confirmation stating the decision. `src: Front-end specification, reviewer surfaces`
- [ ] `C-FE-90` `ui` The members route shows the seat count above a members table. `src: Front-end specification, workspace routes`
- [ ] `C-FE-91` `capability` An invitation is sent from a row at the top of the members table. `src: Front-end specification, workspace routes`
- [ ] `C-FE-92` `ui` Each billing meter shows a bar toward its limit with the figures. `src: Front-end specification, workspace routes`
- [ ] `C-FE-93` `ui` A billing meter without a limit reads unlimited or not included in words. `src: Front-end specification, workspace routes`
- [ ] `C-FE-94` `capability` A plan change lands on a confirmation stating plan, seats plus charge. `src: Front-end specification, workspace routes`
- [ ] `C-FE-95` `ui` Brand kits show their colour swatches with font names. `src: Front-end specification, workspace routes`
- [ ] `C-FE-96` `ui` Favourites reuse the library cards. `src: Front-end specification, workspace routes`
- [ ] `C-FE-97` `capability` Settings offers the interface scale as four choices applied at once. `src: Front-end specification, settings`
- [ ] `C-FE-98` `ui` Loading content appears as skeletons rather than spinners. `src: Front-end specification, empty loading error states`
- [ ] `C-FE-99` `ui` An empty projects table invites a first remix. `src: Front-end specification, empty loading error states`
- [ ] `C-FE-100` `ui` An empty review inbox says nothing has been sent yet. `src: Front-end specification, empty loading error states`
- [ ] `C-FE-101` `ui` The not-found page keeps the header with the footer. `src: Front-end specification, empty loading error states`
- [ ] `C-FE-102` `ui` The focus indicator sits offset from the control edge. `src: Front-end specification, focus`
- [ ] `C-FE-103` `ui` Pointer clicks show no focus indicator. `src: Front-end specification, focus`
- [ ] `C-FE-104` `capability` Focusing an unrevealed element reveals the element at once. `src: Front-end specification, focus`
- [ ] `C-FE-105` `capability` Page content sits in the document before any script runs. `src: Front-end specification, focus`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product has no organisation layer above workspaces. `src: Constraints, bullet 1`
- [ ] `C-CN-02` `constraint` The product offers no single sign-on. `src: Constraints, bullet 1`
- [ ] `C-CN-03` `constraint` The product holds no payment provider, card or invoice. `src: Constraints, bullet 2`
- [ ] `C-CN-04` `constraint` The product performs no captioning, speech synthesis or background removal. `src: Constraints, bullet 3`
- [ ] `C-CN-05` `constraint` The product offers no ProRes or 4K export. `src: Constraints, bullet 3`
- [ ] `C-CN-06` `constraint` The product cannot save a design as a custom template. `src: Constraints, bullet 4`
- [ ] `C-CN-07` `constraint` Concurrent edits meet at save time without a live channel. `src: Constraints, bullet 5`
- [ ] `C-CN-08` `constraint` The server renders no video frames. `src: Constraints, bullet 6`
- [ ] `C-CN-09` `constraint` Shared frames carry no viewer-tied watermark. `src: Constraints, bullet 7`
- [ ] `C-CN-10` `constraint` Playback is restricted by named recipient only. `src: Constraints, bullet 7`
- [ ] `C-CN-11` `constraint` Notifications never leave the app. `src: Constraints, bullet 8`
- [ ] `C-CN-12` `constraint` No third-party analytics, fonts or networks load at runtime. `src: Constraints, bullet 9`
- [ ] `C-CN-13` `constraint` The product ships in one language with no offline mode. `src: Constraints, bullet 10`
- [ ] `C-CN-14` `constraint` The app stays responsive with thousands of library blocks. `src: Constraints, bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `contract` The public port is read from `APP_PUBLIC_PORT`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-04` `contract` The HTTP API is served under the `/api` prefix. `src: Deployment contract, bullet 2`
- [ ] `C-DC-05` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract, bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, bullet 4`
- [ ] `C-DC-07` `contract` Login credentials are written to the credentials file at the app root. `src: Deployment contract, bullet 5`
- [ ] `C-DC-08` `literal` Empty `.browser_screenshots/` plus `.downloads/` directories exist at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-09` `contract` The app serves a production build rather than a dev server. `src: Deployment contract, bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract, bullet 8`
- [ ] `C-DC-11` `literal` The server binds `0.0.0.0`. `src: Deployment contract, bullet 9`
- [ ] `C-DC-12` `contract` The backing services are used as already running. `src: Deployment contract, bullet 10`
- [ ] `C-DC-13` `contract` The app uses only the named providers with no edge functions. `src: Deployment contract, bullet 11`
- [ ] `C-DC-14` `contract` The app adds no persistent volumes, fixed container names or custom networks. `src: Deployment contract, bullet 12`
- [ ] `C-DC-15` `contract` Field names in API bodies match the API shapes table. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` An invalid or unauthorized call is rejected as a client error with a message. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `contract` Bearer auth guards every endpoint outside the listed public ones. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `contract` MinIO is the only place an uploaded or exported file exists. `src: Deployment contract, No mocks`
- [ ] `C-DC-19` `contract` PostgreSQL is the only place the app's records exist. `src: Deployment contract, No mocks`
- [ ] `C-DC-20` `contract` Usage counters live in the store rather than process memory. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-RL-33 | User roles, seeded accounts paragraph |
| `member@example.com` | seeded owner of Juniper Goods | C-RL-27 | User roles, seeded accounts table row 1 |
| `member2@example.com` | seeded member of Juniper Goods | C-RL-28 | User roles, seeded accounts table row 2 |
| `member3@example.com` | seeded owner of Solo Sketchbook | C-RL-29 | User roles, seeded accounts table row 3 |
| `member4@example.com` | seeded owner of Basic Bench | C-RL-30 | User roles, seeded accounts table row 4 |
| `reviewer@example.com` | seeded reviewer with requests | C-RL-31 | User roles, seeded accounts table row 5 |
| `reviewer2@example.com` | seeded reviewer with nothing addressed | C-RL-32 | User roles, seeded accounts table row 6 |
| `member` | the member account role | C-RL-01 | User roles, para 1 |
| `reviewer` | the reviewer account role | C-RL-01 | User roles, para 1 |
| `/register` | open signup route | C-RL-24 | User roles, signup paragraph |
| `2500` | Basic monthly price in cents | C-CF-21 | Core features, Plans table row 2 |
| `1800` | Basic annual per-month price in cents | C-CF-22 | Core features, Plans table row 2 |
| `3800` | Pro monthly price in cents | C-CF-23 | Core features, Plans table row 3 |
| `3000` | Pro annual per-month price in cents | C-CF-24 | Core features, Plans table row 3 |
| `7000` | Business monthly price in cents | C-CF-25 | Core features, Plans table row 4 |
| `5900` | Business annual per-month price in cents | C-CF-26 | Core features, Plans table row 4 |
| `28` | Basic annual saving percent | C-CF-30 | Core features, Plans rule 2 |
| `21` | Pro annual saving percent | C-CF-31 | Core features, Plans rule 2 |
| `16` | Business annual saving percent | C-CF-32 | Core features, Plans rule 2 |
| `Unlimit your creativity.` | pricing heading | C-CF-33 | Core features, Plans rule 3 |
| `Save up to 28%` | billing toggle badge | C-CF-35 | Core features, Plans rule 3 |
| `Most popular` | Pro card marker | C-CF-38 | Core features, Plans rule 4 |
| `Max 10 team members` | Pro card member line | C-CF-43 | Core features, Plans rule 5 |
| `1073741824` | bytes in a gigabyte | C-CF-59 | Core features, Quotas para after the table |
| `quota_exceeded` | quota refusal error code | C-CF-77 | Core features, Quotas rule 4 |
| `You've used all your project variations for this month. Basic includes 20.` | monthly allowance refusal |  | see instruction.md |
| `Free includes 5 saved blocks. Remove one or upgrade to add more.` | ceiling refusal |  | see instruction.md |
| `Brand kits are not included in Basic. Upgrade to Pro to use them.` | not-included refusal |  | see instruction.md |
| `Pro includes up to 10 members. Upgrade to Business to add more.` | seat cap refusal |  | see instruction.md |
| `Free is for one person. Upgrade to Pro to invite your team.` | single-user invitation refusal |  | see instruction.md |
| `Enterprise is arranged through Contact Sales.` | enterprise plan refusal |  | see instruction.md |
| `Free is for one person. Remove the other members before switching.` | multi-member downgrade refusal |  | see instruction.md |
| `1900` | first proration example | C-CF-102 | Core features, Seats rule 5 table row 1 |
| `1267` | second proration example | C-CF-103 | Core features, Seats rule 5 table row 2 |
| `11441` | third proration example | C-CF-104 | Core features, Seats rule 5 table row 3 |
| `Glow` | library block with an intensity slider | C-CF-113 | Core features, Library table row 2 |
| `intensity` | Glow slider parameter | C-CF-113 | Core features, Library table row 2 |
| `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b01` | uuid of the Denim Drop template |  | see instruction.md |
| `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b06` | uuid of the premium Feature Reveal template |  | see instruction.md |
| `Premium templates are not included in Free. Upgrade to Basic to use them.` | premium remix refusal |  | see instruction.md |
| `Describe matched no blocks. Try naming an effect such as Glow or Halftone.` | describe no-match refusal |  | see instruction.md |
| `This block stopped responding and was paused.` | paused code block message |  | see instruction.md |
| `A newer version of this block exists.` | newer block version marker |  | see instruction.md |
| `assets/{workspace_id}/{sha256_of_bytes}.{ext}` | asset object key scheme | C-CF-176 | Core features, Media rule 2 |
| `exports/{workspace_id}/{export_id}.{format}` | export object key scheme | C-CF-196 | Core features, Versions rule 5 |
| `Rendering. We'll let you know when it's ready.` | rendering export message |  | see instruction.md |
| `That export didn't finish. We haven't counted it against your quota.` | failed export message |  | see instruction.md |
| `Anyone with this link can view this version.` | open share message |  | see instruction.md |
| `Only the people you named can view this version.` | recipients share message |  | see instruction.md |
| `Export this version before sharing it.` | share refusal without a ready export |  | see instruction.md |
| `A newer version exists. You're viewing the version you were sent.` | superseded share notice |  | see instruction.md |
| `This version has been replaced. Ask the sender for the latest link.` | closed superseded share message |  | see instruction.md |
| `This link has expired. Ask the sender for a new one.` | expired share message |  | see instruction.md |
| `The moment this comment referred to has been edited out.` | orphaned comment note |  | see instruction.md |
| `Waiting on 1 reviewer.` | approval waiting message for one reviewer |  | see instruction.md |
| `Waiting on 2 reviewers.` | approval waiting message for two reviewers |  | see instruction.md |
| `You can see this version only.` | reviewer guest scope sentence |  | see instruction.md |
| `Ferment Video : Online Video Editor Engineered for Creativity` | home title | C-CF-266 | Core features, Marketing rule 1 |
| `Creative Code Video Editor & Motion Design Tools : Ferment` | product title | C-CF-267 | Core features, Marketing rule 1 |
| `Pricing : Ferment` | pricing title | C-CF-268 | Core features, Marketing rule 1 |
| `Contact Ferment : Video Editor Sales & Support` | contact title | C-CF-269 | Core features, Marketing rule 1 |
| `Ferment Blog` | blog title | C-CF-270 | Core features, Marketing rule 1 |
| `Login to Ferment` | login title | C-CF-271 | Core features, Marketing rule 1 |
| `Sign up` | signup title | C-CF-272 | Core features, Marketing rule 1 |
| `Explore : Ferment` | dashboard title | C-CF-273 | Core features, Marketing rule 1 |
| `Templates : Ferment` | gallery title | C-CF-274 | Core features, Marketing rule 1 |
| `Blocks : Ferment` | library title | C-CF-275 | Core features, Marketing rule 1 |
| `Privacy Policy : Ferment` | privacy title | C-CF-276 | Core features, Marketing rule 1 |
| `FC-` | contact reference prefix | C-CF-286 | Core features, Marketing rule 5 |
| `We couldn't find that page.` | not-found heading |  | see instruction.md |
| `not_found` | unknown API error code | C-CF-314 | Core features, Not found rule 2 |
| `Cookie settings` | footer control reopening the consent panel |  | see instruction.md |
| `Reject all` | consent reject control |  | see instruction.md |
| `Accept all` | consent accept control |  | see instruction.md |
| `4.5:1` | body text contrast floor | C-UX-47 | UI/UX notes, accessibility floors |
| `3:1` | component contrast floor | C-UX-48 | UI/UX notes, accessibility floors |
| `DATABASE_URL` | variable naming the store |  | see instruction.md |
| `STORAGE_ENDPOINT` | variable naming the object store |  | see instruction.md |
| `STORAGE_BUCKET` | variable naming the bucket |  | see instruction.md |
| `{"status": "ok"}` | health body | C-TR-08 | Technical requirements, bullet 6 |
| `Z` | suffix on every timestamp |  | see instruction.md |
| `/app/USER_README.md` | file carrying the seeded logins | C-DM-02 | Data model, password paragraph |
| `7600` | seeded Juniper Goods plan change charge | C-DM-30 | Data model, seed data Juniper Goods bullet |
| `k7Qm2pVx9LwR4tNz` | open seeded share token | C-DM-37 | Data model, seed data shares table row 1 |
| `pQ4rT8vW2yZ6aB3c` | expired seeded share token | C-DM-38 | Data model, seed data shares table row 2 |
| `mN5bV7cX1zL3kJ9h` | passphrase seeded share token | C-DM-39 | Data model, seed data shares table row 3 |
| `orchard-lantern-42` | seeded share passphrase | C-DM-39 | Data model, seed data shares table row 3 |
| `dR2fG6hJ8kL0pQ1s` | recipients-only seeded share token | C-DM-40 | Data model, seed data shares table row 4 |
| `stale-bench-1` | request key of the stale seeded export | C-DM-46 | Data model, seed data Basic Bench bullet |
| `Add Ferment` | inner route tagline | C-FE-12 | Front-end specification, header |
| `Browse 1000s of Ferment blocks` | narrow Blocks subtitle | C-FE-14 | Front-end specification, header |
| `Copyright (C) 2026 Ferment` | footer copyright line | C-FE-18 | Front-end specification, footer |
| `Seed Blocks` | dashboard row heading | C-FE-58 | Front-end specification, application shell |
| `Start with a block` | dashboard row subtitle | C-FE-58 | Front-end specification, application shell |
| `APP_PUBLIC_URL` | variable naming the public origin | C-DC-01 | Deployment contract, bullet 1 |
| `4173` | container-internal port | C-DC-02 | Deployment contract, bullet 1 |
| `APP_PUBLIC_PORT` | variable naming the public port | C-DC-03 | Deployment contract, bullet 1 |
| `/api` | API prefix | C-DC-04 | Deployment contract, bullet 2 |
| `GET /api/health` | health route | C-DC-05 | Deployment contract, bullet 3 |
| `200` | health status | C-DC-05 | Deployment contract, bullet 3 |
| `.browser_screenshots/` | reserved empty directory | C-DC-08 | Deployment contract, bullet 6 |
| `.downloads/` | reserved empty directory | C-DC-08 | Deployment contract, bullet 6 |
| `0.0.0.0` | bind address | C-DC-11 | Deployment contract, bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the wording a consent panel shows | C-CF-304 | the brief requires the exact wording to be stored but leaves the text to the builder |
| the credit line of each creator | C-CF-123 | creator credits are named as a field with no pinned text |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 9 |
| User roles | 1 | 38 |
| Core features | 59 | 316 |
| User flow | 8 | 24 |
| UI and UX notes | 9 | 64 |
| Technical requirements | 8 | 18 |
| Data model | 4 | 53 |
| Front-end specification | 24 | 105 |
| Constraints | 0 | 14 |
| Deployment contract | 12 | 20 |
