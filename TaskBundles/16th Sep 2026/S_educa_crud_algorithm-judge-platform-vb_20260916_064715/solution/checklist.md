# Checklist: Bytefold

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 505
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a catalogue of algorithm problems to filter by topic, difficulty, category. `src: Overview para 1`
- [ ] `C-OV-02` `data` Every problem carries a statement, constraints, a starter signature per language, hidden cases. `src: Overview para 1`
- [ ] `C-OV-03` `capability` A member filters the catalogue, opens a problem, writes a solution in the embedded editor, submits the solution. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The app runs a submitted solution against hidden cases under a time limit, a memory limit. `src: Overview para 1`
- [ ] `C-OV-05` `capability` A settled submission returns a verdict, a runtime, a memory figure, a percentile. `src: Overview para 1`
- [ ] `C-OV-06` `ui` The marketing route carries the pitch, an employer wall, a read-only editor demonstration. `src: Overview para 2`
- [ ] `C-OV-07` `ui` Contests show a live countdown, a ranked ladder carrying ratings. `src: Overview para 2`
- [ ] `C-OV-08` `capability` Study plans carry per-member progress beside curated explore cards. `src: Overview para 2`
- [ ] `C-OV-09` `capability` The discussion feed carries categories, votes, view counts. `src: Overview para 2`
- [ ] `C-OV-10` `capability` A paid tier sells two subscription terms from a price list per region. `src: Overview para 2`
- [ ] `C-OV-11` `role` Public route addresses for the catalogue, statements, discussion, pricing answer a signed-out visitor. `src: Overview para 3`
- [ ] `C-OV-12` `constraint` Subscribing completes on the next request inside the product, with no external payment processor. `src: Overview para 4`
- [ ] `C-OV-13` `constraint` Every browser request stays on the app origin, so no binary asset or third-party collector loads. `src: Overview para 4`


## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor browses the catalogue problems in number order. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor runs a solution against the example cases. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor submission is denied as unauthenticated. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A signed-out draft write, vote or contest registration is denied. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A signed-in member submits, keeps a solved set, keeps a streak, saves drafts. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A member cannot read another member's submission. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A member cannot read another member's draft. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A member without an entitlement is denied a gated statement. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A member without an entitlement is denied the employer filter. `src: User roles table row 2`
- [ ] `C-RL-10` `role` No member reads a problem's hidden case inputs in any problem response. `src: User roles table row 2`
- [ ] `C-RL-11` `role` An entitled subscriber reads the gated statement. `src: User roles table row 3`
- [ ] `C-RL-12` `role` An entitled subscriber filtering by employers receives results. `src: User roles table row 3`
- [ ] `C-RL-13` `role` Authorization is enforced by the server, so a direct API call without the entitlement is denied. `src: User roles para after table`
- [ ] `C-RL-14` `role` A gated premium submission is denied, leaving the protected state unchanged. `src: User roles para after table`
- [ ] `C-RL-15` `role` A submission from a caller with absent credentials is denied as unauthenticated. `src: User roles para 2 after table`
- [ ] `C-RL-16` `role` A signed-in member asking for a gated statement is refused as payment-required. `src: User roles para 2 after table`
- [ ] `C-RL-17` `role` A request for another member's submission answers as if the record does not exist. `src: User roles para 2 after table`
- [ ] `C-RL-18` `capability` Registration is open: a fresh address answers like a known one. `src: User roles para 3 after table`
- [ ] `C-RL-19` `literal` The seeded account `member@example.com` signs in as `nadia_roux` with no entitlement. `src: User roles seed table row 1`
- [ ] `C-RL-20` `literal` The seeded account `member2@example.com` signs in as `tomas_iversen` with no entitlement. `src: User roles seed table row 2`
- [ ] `C-RL-21` `literal` The seeded account `subscriber@example.com` signs in as `priya_shah`. `src: User roles seed table row 3`
- [ ] `C-RL-22` `literal` Every seeded account signs in with the corpus password `deku-demo-pw-2026`. `src: User roles para 3 after table`


## C-CF Core features

- [ ] `C-CF-01` `capability` Accounts sign in with an email address, a password implemented by the app. `src: Core features Auth para 1`
- [ ] `C-CF-02` `literal` A seeded account sign-in answers `200` with an `access_token` field. `src: Core features Auth para 1`
- [ ] `C-CF-03` `capability` A successful sign-in sets a session cookie for browser use. `src: Core features Auth para 1`
- [ ] `C-CF-04` `constraint` The session cookie alone is refused on the `/api` routes. `src: Core features Auth para 1`
- [ ] `C-CF-05` `constraint` Signing out ends that session at once, so the bearer token is refused afterwards. `src: Core features Auth para 1`
- [ ] `C-CF-06` `literal` A password shorter than `8` characters is rejected as invalid input. `src: Core features Auth para 1`
- [ ] `C-CF-07` `literal` A password of `128` characters is accepted, never echoed. `src: Core features Auth para 1`
- [ ] `C-CF-08` `literal` A sign-in with a wrong password answers `401`. `src: Core features Auth para 1`
- [ ] `C-CF-09` `constraint` A password never appears in a registration or sign-in response body. `src: Core features Auth para 1`
- [ ] `C-CF-10` `literal` The members table stores one state value of `unverified`, `active`, `restricted`, `locked`, `deleted`. `src: Core features Auth rule 1`
- [ ] `C-CF-11` `capability` `GET /api/me` reports the member state moving from unverified to active. `src: Core features Auth rule 1`
- [ ] `C-CF-12` `literal` A newly registered member is `unverified`. `src: Core features Auth rule 1`
- [ ] `C-CF-13` `capability` An `unverified` member may submit a solution. `src: Core features Auth rule 1`
- [ ] `C-CF-14` `constraint` An `unverified` member is forbidden to vote. `src: Core features Auth rule 1`
- [ ] `C-CF-15` `constraint` An `unverified` member is forbidden to register for a contest. `src: Core features Auth rule 1`
- [ ] `C-CF-16` `literal` `5` consecutive failed sign-ins lock the account. `src: Core features Auth rule 2`
- [ ] `C-CF-17` `constraint` A `locked` account is refused sign-in with exactly the wrong-password message. `src: Core features Auth rule 2`
- [ ] `C-CF-18` `capability` Registration lowercases the domain of an address for comparison, so the domain case signs in to the same account. `src: Core features Auth rule 3`
- [ ] `C-CF-19` `constraint` Address normalisation preserves the local part exactly. `src: Core features Auth rule 3`
- [ ] `C-CF-20` `constraint` A username colliding case-insensitively is rejected as invalid input. `src: Core features Auth rule 3`
- [ ] `C-CF-21` `constraint` A username colliding after confusable folding is rejected as invalid input. `src: Core features Auth rule 3`
- [ ] `C-CF-22` `capability` Registration answers identically for a known address, a fresh address. `src: Core features Auth rule 4`
- [ ] `C-CF-23` `constraint` Registration of a known address creates no second account, keeps the original password. `src: Core features Auth rule 4`
- [ ] `C-CF-24` `capability` Verification completed in the product moves a member from `unverified` to `active`. `src: Core features Auth rule 5`
- [ ] `C-CF-25` `ui` The account route offers the verification link inside the product. `src: Core features Auth rule 5`
- [ ] `C-CF-26` `capability` The session list names every session with a device label, a last-seen time. `src: Core features Auth rule 5`
- [ ] `C-CF-27` `capability` Ending a session from the session list signs that device out. `src: Core features Auth rule 5`
- [ ] `C-CF-28` `constraint` Sign-out answers the same whether or not a session existed. `src: Core features Auth rule 6`
- [ ] `C-CF-29` `constraint` Signing out one session leaves other sessions signed in. `src: Core features Auth rule 6`
- [ ] `C-CF-30` `literal` The catalogue at `/problemset/` lists `240` published problems. `src: Core features catalogue intro`
- [ ] `C-CF-31` `ui` The catalogue carries a left rail, two rows of topic chips with an `Expand` control, a row of category pills. `src: Core features catalogue intro`
- [ ] `C-CF-32` `ui` At the widest tier the catalogue carries a right rail of panels. `src: Core features catalogue intro`
- [ ] `C-CF-33` `literal` The `category` axis selects exactly one of `algorithms`, `database`, `shell`, `concurrency`, `javascript`, `pandas`. `src: Core features catalogue rule 1`
- [ ] `C-CF-34` `literal` The catalogue first response carries category pills reading `All Topics`, `Algorithms`, `Database`, `Shell`, `Concurrency`, `JavaScript`, `Pandas`. `src: Core features catalogue rule 1`
- [ ] `C-CF-35` `ui` `All Topics` is the default pill with exactly one pill active at a time. `src: Core features catalogue rule 1`
- [ ] `C-CF-36` `literal` The `topics` axis selects zero or more of the `47` topic tags. `src: Core features catalogue rule 1`
- [ ] `C-CF-37` `literal` The catalogue `difficulty` filter selects zero or more of `Easy`, `Medium`, `Hard`. `src: Core features catalogue rule 1`
- [ ] `C-CF-38` `literal` The `status` filter selects exactly one of `all`, `unsolved`, `solved`, `attempted` for the member. `src: Core features catalogue rule 1`
- [ ] `C-CF-39` `capability` The `employers` axis selects zero or more employer tags. `src: Core features catalogue rule 1`
- [ ] `C-CF-40` `capability` The `search` axis matches the problem number, the title. `src: Core features catalogue rule 1`
- [ ] `C-CF-41` `constraint` A facet count applies every other axis as a conjunction. `src: Core features catalogue rule 2`
- [ ] `C-CF-42` `constraint` Two selected topics return only problems carrying both tags. `src: Core features catalogue rule 2`
- [ ] `C-CF-43` `constraint` A catalogue difficulty filter of two values returns problems of either. `src: Core features catalogue rule 2`
- [ ] `C-CF-44` `constraint` Two selected employers return problems of either employer. `src: Core features catalogue rule 2`
- [ ] `C-CF-45` `capability` The `status` filter reads the member's own solved rows. `src: Core features catalogue rule 3`
- [ ] `C-CF-46` `constraint` A signed-out `status` filter other than `all` fails with the invalid-data failure type. `src: Core features catalogue rule 3`
- [ ] `C-CF-47` `capability` Every category, topic tag facet value carries a problem count. `src: Core features catalogue rule 4`
- [ ] `C-CF-48` `constraint` A facet count equals the list the filter would return with that value added. `src: Core features catalogue rule 4`
- [ ] `C-CF-49` `constraint` A facet count excludes the value's own multi-select axis. `src: Core features catalogue rule 4`
- [ ] `C-CF-50` `constraint` Facet counts move when the filter set changes. `src: Core features catalogue rule 4`
- [ ] `C-CF-51` `constraint` Topic chips order by problem count descending, then by name ascending. `src: Core features catalogue rule 5`
- [ ] `C-CF-52` `literal` The default catalogue order is problem number ascending. `src: Core features catalogue rule 6`
- [ ] `C-CF-53` `capability` The catalogue orders by acceptance, difficulty, frequency, title. `src: Core features catalogue rule 6`
- [ ] `C-CF-54` `constraint` Every catalogue order sorts by its key, then breaks ties on the problem number ascending. `src: Core features catalogue rule 6`
- [ ] `C-CF-55` `literal` A catalogue page lists `50` problems, the pages addressed by a cursor. `src: Core features catalogue rule 7`
- [ ] `C-CF-56` `constraint` Walking every page of an order yields each stored problem exactly once. `src: Core features catalogue rule 7`
- [ ] `C-CF-57` `constraint` A page past the end is empty, successful, with a null cursor, the correct total. `src: Core features catalogue rule 7`
- [ ] `C-CF-58` `capability` The day's featured problem is pinned above the result set. `src: Core features catalogue rule 8`
- [ ] `C-CF-59` `constraint` The pinned daily row is not part of the result set, so page two begins after row fifty. `src: Core features catalogue rule 8`
- [ ] `C-CF-60` `capability` The shuffle control opens a problem drawn from the problems surviving the current filter. `src: Core features catalogue rule 9`
- [ ] `C-CF-61` `ui` Catalogue rows are zebra striped on alternate rows. `src: Core features catalogue rule 10`
- [ ] `C-CF-62` `literal` Every catalogue row renders a status mark, the title as `<number>. <title>`, an acceptance percentage to one decimal place. `src: Core features catalogue rule 10`
- [ ] `C-CF-63` `ui` Every catalogue row renders a five-bar frequency histogram. `src: Core features catalogue rule 10`
- [ ] `C-CF-64` `literal` The catalogue first response renders rows with the difficulty words `Easy`, `Med.`, `Hard`. `src: Core features catalogue rule 10`
- [ ] `C-CF-65` `literal` The difficulty filter renders the words `Easy`, `Medium`, `Hard`. `src: Core features catalogue rule 10`
- [ ] `C-CF-66` `ui` Without an entitlement the frequency histogram renders greyed under a padlock. `src: Core features catalogue rule 10`
- [ ] `C-CF-67` `constraint` An `employers` filter without an entitlement is refused as payment-required. `src: Core features catalogue rule 10`
- [ ] `C-CF-68` `constraint` The catalogue row payload is identical for every caller, carrying no member status. `src: Core features catalogue rule 11`
- [ ] `C-CF-69` `capability` The per-member status overlay returns solved or attempted for a member's problem. `src: Core features catalogue rule 11`
- [ ] `C-CF-70` `capability` A stored solved row, a stored draft read back the same for the member on the next request. `src: Core features catalogue rule 12`
- [ ] `C-CF-71` `ui` Reloading the catalogue as a member shows the solved mark stored for a solved problem. `src: Core features catalogue rule 12`
- [ ] `C-CF-72` `constraint` The filter state lives in the query string in full. `src: Core features catalogue rule 13`
- [ ] `C-CF-73` `capability` A catalogue filter address opened in a fresh session reproduces the same rows in order. `src: Core features catalogue rule 13`
- [ ] `C-CF-74` `capability` Searching `Two Sum` returns `1. Two Sum` first. `src: Core features catalogue rule 14`
- [ ] `C-CF-75` `constraint` An all-digit search matches the problem number first, exactly. `src: Core features catalogue rule 14`
- [ ] `C-CF-76` `literal` The catalogue first response carries the search field reading `Search questions`. `src: Core features catalogue rule 15`
- [ ] `C-CF-77` `ui` The control row carries a sort control, a filter control, a shuffle control. `src: Core features catalogue rule 15`
- [ ] `C-CF-78` `literal` The catalogue first response carries the solved counter reading `0/240 Solved`. `src: Core features catalogue rule 15`
- [ ] `C-CF-79` `literal` The catalogue first response carries a `Weekly Premium` strip of slots `W1` to `W5`. `src: Core features catalogue rule 15`
- [ ] `C-CF-80` `literal` The catalogue first response carries a coin balance with a `Redeem` link, a `Rules` link. `src: Core features catalogue rule 15`
- [ ] `C-CF-81` `literal` The catalogue first response carries the employer search field reading `Search for a company...`. `src: Core features catalogue rule 15`
- [ ] `C-CF-82` `ui` The right rail carries a daily calendar with a streak badge. `src: Core features catalogue rule 15`
- [ ] `C-CF-83` `constraint` Every internal link on every public route resolves. `src: Core features catalogue rule 16`
- [ ] `C-CF-84` `literal` Internal links for `Library`, `Quest`, `Explore`, `Study Plan`, `Help Center`, `Bug Bounty`, `Terms`, `Privacy Policy` resolve on the public routes. `src: Core features catalogue rule 16`
- [ ] `C-CF-85` `literal` `Online Interview`, `Assessment`, `Store`, `Redeem`, `Download App` open pages of the product. `src: Core features catalogue rule 16`
- [ ] `C-CF-86` `capability` An unknown address renders the product's own not-found page, answering not-found. `src: Core features catalogue rule 16`
- [ ] `C-CF-87` `ui` The not-found page sits inside the application shell with a way back to the catalogue. `src: Core features catalogue rule 16`
- [ ] `C-CF-88` `capability` An unknown problem slug renders the not-found page on the workspace route. `src: Core features catalogue rule 16`
- [ ] `C-CF-89` `constraint` A problem is addressed by slug at `/problems/two-sum/`, the number being display only. `src: Core features workspace rule 1`
- [ ] `C-CF-90` `literal` Four workspace tabs answer at `/description/`, `/editorial/`, `/solutions/`, `/submissions/`. `src: Core features workspace rule 1`
- [ ] `C-CF-91` `ui` Reloading a workspace tab lands on the same tab. `src: Core features workspace rule 1`
- [ ] `C-CF-92` `constraint` The workspace submissions tab address shows signed-out visitors a sign-in prompt. `src: Core features workspace rule 1`
- [ ] `C-CF-93` `ui` A statement renders paragraphs, lists, fenced code in the monospace stack without syntax colouring. `src: Core features workspace rule 2`
- [ ] `C-CF-94` `literal` The description markup labels example blocks `Input`, `Output`. `src: Core features workspace rule 2`
- [ ] `C-CF-95` `constraint` The statement markup carries no image element. `src: Core features workspace rule 2`
- [ ] `C-CF-96` `literal` Topic tags sit behind a `Topics` disclosure closed by default. `src: Core features workspace rule 3`
- [ ] `C-CF-97` `ui` Each hint sits behind a disclosure of the hint's own. `src: Core features workspace rule 3`
- [ ] `C-CF-98` `literal` The description markup carries a `Discussion` link beside the metadata strip. `src: Core features workspace rule 3`
- [ ] `C-CF-99` `ui` The metadata strip shows the accepted count, the submission count, the acceptance rate. `src: Core features workspace rule 3`
- [ ] `C-CF-100` `ui` The statement carries a like, dislike pair with counts. `src: Core features workspace rule 3`
- [ ] `C-CF-101` `constraint` Topic tag names are absent from the delivered description markup of an unsolved problem. `src: Core features workspace rule 4`
- [ ] `C-CF-102` `constraint` Employer tags are omitted from the problem payload without an entitlement. `src: Core features workspace rule 4`
- [ ] `C-CF-103` `ui` Above the wide breakpoint the workspace shows statement tabs beside the editor above a console, split by a draggable divider. `src: Core features workspace rule 5`
- [ ] `C-CF-104` `literal` Below the wide breakpoint the panes become a two-tab switcher labelled `Problem`, `Code`. `src: Core features workspace rule 5`
- [ ] `C-CF-105` `capability` The divider position moved by arrow keys is remembered for the member after a reload. `src: Core features workspace rule 5`
- [ ] `C-CF-106` `constraint` The workspace divider is a separator carrying a value, a minimum, a maximum. `src: Core features workspace rule 5`
- [ ] `C-CF-107` `ui` The workspace route suppresses the left rail, the footer. `src: Core features workspace rule 6`
- [ ] `C-CF-108` `ui` The workspace top bar carries a problem navigator reading `<current> / <total>` with previous, next controls. `src: Core features workspace rule 7`
- [ ] `C-CF-109` `literal` The offered language set is `python3`, `javascript`, another language rejected. `src: Core features editor rule 1`
- [ ] `C-CF-110` `constraint` A run or submission in a language outside `python3`, `javascript` is rejected as invalid input. `src: Core features editor rule 1`
- [ ] `C-CF-111` `ui` The editor provides syntax colouring, line numbers, fold markers, bracket matching. `src: Core features editor rule 1`
- [ ] `C-CF-112` `ui` The editor provides find, replace with a regular-expression mode, a size control. `src: Core features editor rule 1`
- [ ] `C-CF-113` `ui` The editor soft-wrap toggle is off by default. `src: Core features editor rule 1`
- [ ] `C-CF-114` `ui` Pressing return after a `python3` line opening a block indents the next line by four spaces. `src: Core features editor rule 1`
- [ ] `C-CF-115` `constraint` A draft is stored per member, problem, language. `src: Core features editor rule 2`
- [ ] `C-CF-116` `capability` Writing a draft in one language leaves the draft of the other language untouched. `src: Core features editor rule 2`
- [ ] `C-CF-117` `ui` Switching the language selector away then back restores the earlier buffer exactly. `src: Core features editor rule 2`
- [ ] `C-CF-118` `capability` A signed-in member's draft is written through to the service. `src: Core features editor rule 3`
- [ ] `C-CF-119` `constraint` A signed-out draft write to the service is denied. `src: Core features editor rule 3`
- [ ] `C-CF-120` `ui` A signed-out local draft is offered as a merge on signing in. `src: Core features editor rule 3`
- [ ] `C-CF-121` `literal` The console carries three tabs `Testcase`, `Result`, `Debugger`. `src: Core features editor rule 4`
- [ ] `C-CF-122` `constraint` The workspace markup exposes the console tabs as a tab list. `src: Core features editor rule 4`
- [ ] `C-CF-123` `ui` The testcase tab shows one editable field per parameter. `src: Core features editor rule 4`
- [ ] `C-CF-124` `constraint` A run case giving a string for an integer array parameter is rejected as invalid input. `src: Core features editor rule 4`
- [ ] `C-CF-125` `literal` A run carrying more than `10` custom cases is rejected. `src: Core features editor rule 4`
- [ ] `C-CF-126` `constraint` A custom case result shows the produced output with no expected value. `src: Core features editor rule 5`
- [ ] `C-CF-127` `ui` The `Debugger` tab sits behind the entitlement. `src: Core features editor rule 6`
- [ ] `C-CF-128` `literal` The workspace markup renders the toolbar labels `Reset`, `Format`, `Copy`, `Run`, `Submit`, `Notes`, `Timer`. `src: Core features editor rule 7`
- [ ] `C-CF-129` `ui` `Reset` confirms before discarding the buffer. `src: Core features editor rule 7`
- [ ] `C-CF-130` `constraint` A run executes the example cases plus the custom cases. `src: Core features run table`
- [ ] `C-CF-131` `capability` A signed-out visitor run executes the example cases. `src: Core features run table`
- [ ] `C-CF-132` `constraint` A practice submission moves the submission count by one. `src: Core features run table`
- [ ] `C-CF-133` `constraint` An accepted practice submission moves the accepted count by one. `src: Core features run table`
- [ ] `C-CF-134` `constraint` A run moves neither counter. `src: Core features run table`
- [ ] `C-CF-135` `constraint` A run shows every example case with the input, the expected output, the produced output, a pass mark. `src: Core features run table`
- [ ] `C-CF-136` `constraint` A submission without an `Idempotency-Key` is rejected as invalid input. `src: Core features run table`
- [ ] `C-CF-137` `literal` A source past `64KB` is refused at intake, leaving no submission row. `src: Core features judge rule 1`
- [ ] `C-CF-138` `constraint` A gated premium submission is refused as payment-required, leaving no row. `src: Core features judge rule 1`
- [ ] `C-CF-139` `constraint` A submission in an unregistered contest context is refused as forbidden. `src: Core features judge rule 2`
- [ ] `C-CF-140` `constraint` A refused contest submission leaves no submission row. `src: Core features judge rule 2`
- [ ] `C-CF-141` `constraint` Problems of a contest not yet started answer not-found. `src: Core features judge rule 2`
- [ ] `C-CF-142` `capability` Intake answers before the submitted program has run. `src: Core features judge rule 3`
- [ ] `C-CF-143` `literal` Intake returns the submission identifier with the state `pending`. `src: Core features judge rule 3`
- [ ] `C-CF-144` `literal` An intake submission settles to the state `done` on a later read. `src: Core features judge rule 4`
- [ ] `C-CF-145` `literal` The submissions table stores verdict values of `Accepted`, `Wrong Answer`, `Time Limit Exceeded`, `Memory Limit Exceeded`, `Runtime Error`, `Compile Error`, `Output Limit Exceeded`, `Internal Error`, `Rejected`. `src: Core features judge rule 4`
- [ ] `C-CF-146` `constraint` Judging stops at the first failing case, recording that case index. `src: Core features judge rule 5`
- [ ] `C-CF-147` `constraint` The same wrong source names the same failing case index twice. `src: Core features judge rule 5`
- [ ] `C-CF-148` `constraint` An accepted submission comes from a program exiting cleanly with matching output. `src: Core features judge rule 6`
- [ ] `C-CF-149` `constraint` A failing case from output that fails the comparator settles `Wrong Answer`. `src: Core features judge rule 6`
- [ ] `C-CF-150` `constraint` A program exiting cleanly having produced no answer is `Wrong Answer`, not `Runtime Error`. `src: Core features judge rule 6`
- [ ] `C-CF-151` `constraint` A program exceeding the time limit settles `Time Limit Exceeded`. `src: Core features judge rule 6`
- [ ] `C-CF-152` `constraint` A program exceeding the memory limit settles `Memory Limit Exceeded`, never a crash. `src: Core features judge rule 6`
- [ ] `C-CF-153` `constraint` A program exiting non-zero settles `Runtime Error` with the captured standard error. `src: Core features judge rule 6`
- [ ] `C-CF-154` `constraint` An answer past the output byte cap settles `Output Limit Exceeded`. `src: Core features judge rule 6`
- [ ] `C-CF-155` `constraint` A `python3` syntax error settles `Compile Error` carrying the diagnostic. `src: Core features judge rule 6`
- [ ] `C-CF-156` `constraint` A loop ignoring signals is still stopped from outside as `Time Limit Exceeded`. `src: Core features judge rule 7`
- [ ] `C-CF-157` `capability` A non-terminating solution settles `Time Limit Exceeded` within the judging deadline. `src: Core features judge rule 7`
- [ ] `C-CF-158` `constraint` A solution sleeping thirty seconds settles `Time Limit Exceeded` by the wall-clock limit. `src: Core features judge rule 8`
- [ ] `C-CF-159` `literal` The base limits read `2000` ms, `262144` KB in the problem detail. `src: Core features judge rule 9`
- [ ] `C-CF-160` `literal` The language multipliers declared in the problem detail read `2.0` for `javascript`, `3.0` for `python3`. `src: Core features judge rule 9`
- [ ] `C-CF-161` `ui` A time limit verdict shows the multiplier for the chosen language. `src: Core features judge rule 9`
- [ ] `C-CF-162` `capability` A javascript solution is accepted though the runtime reserves a large address space. `src: Core features judge rule 9`
- [ ] `C-CF-163` `constraint` An isolated program reaches no network, no database, no app surface. `src: Core features judge rule 10`
- [ ] `C-CF-164` `constraint` The isolated program environment names no database, member, problem. `src: Core features judge rule 10`
- [ ] `C-CF-165` `constraint` The isolated program working directory is discarded between cases. `src: Core features judge rule 10`
- [ ] `C-CF-166` `capability` An isolated program opening network sockets still receives a verdict. `src: Core features judge rule 10`
- [ ] `C-CF-167` `literal` The problem detail declares the `comparator`, `exact` for Two Sum. `src: Core features judge rule 11`
- [ ] `C-CF-168` `literal` The `numeric-tolerance` comparator accepts a median off by `1e-7`, refuses one off by `0.1`. `src: Core features judge rule 11`
- [ ] `C-CF-169` `literal` The `unordered` comparator accepts every ordering in any order, refuses an ordering listed twice. `src: Core features judge rule 11`
- [ ] `C-CF-170` `literal` Every published problem stores a comparator from `exact`, `numeric-tolerance`, `unordered`, `unordered-deep`, `any-of`. `src: Core features judge rule 11`
- [ ] `C-CF-171` `constraint` A median within tolerance is accepted, so a floating-point value is never compared for equality. `src: Core features judge rule 11`
- [ ] `C-CF-172` `literal` A failing case reveals the case index with the input, expected, produced values truncated to `1000` characters. `src: Core features judge rule 12`
- [ ] `C-CF-173` `constraint` A time limit verdict reveals the limit, the multiplier, never the input. `src: Core features judge rule 12`
- [ ] `C-CF-174` `constraint` A memory limit verdict never reveals the input. `src: Core features judge rule 12`
- [ ] `C-CF-175` `literal` A runtime error reveals standard error capped at `4KB`, never the input. `src: Core features judge rule 12`
- [ ] `C-CF-176` `constraint` Hidden case inputs stored in the database never appear in a problem response. `src: Core features judge rule 12`
- [ ] `C-CF-177` `capability` A replayed idempotency key with the same body returns the original submission. `src: Core features judge rule 13`
- [ ] `C-CF-178` `constraint` A replayed idempotency key with a different body is rejected as a conflict. `src: Core features judge rule 13`
- [ ] `C-CF-179` `literal` The same source resubmitted inside `10s` is refused as a conflict. `src: Core features judge rule 13`
- [ ] `C-CF-180` `capability` A resubmission after the window is accepted. `src: Core features judge rule 13`
- [ ] `C-CF-181` `constraint` An accepted submission stores exactly one solved row for the member. `src: Core features judge rule 14`
- [ ] `C-CF-182` `constraint` A wrong answer leaves an attempted row, no solved row. `src: Core features judge rule 14`
- [ ] `C-CF-183` `constraint` The acceptance figure equals the accepted count over the submission count at one decimal. `src: Core features judge rule 15`
- [ ] `C-CF-184` `constraint` Simultaneous accepted submissions move both counters by exactly their number. `src: Core features judge rule 16`
- [ ] `C-CF-185` `constraint` Contest submissions leave the public counters unmoved during the running contest. `src: Core features judge rule 17`
- [ ] `C-CF-186` `constraint` The same wrong source settles the same verdict, the same failing case index. `src: Core features judge rule 18`
- [ ] `C-CF-187` `literal` The daily endpoint reports the day in `UTC`. `src: Core features progress rule 1`
- [ ] `C-CF-188` `literal` The daily endpoint reports the seconds left until `UTC` midnight. `src: Core features progress rule 2`
- [ ] `C-CF-189` `ui` The catalogue pins the day's problem with a calendar mark. `src: Core features progress rule 2`
- [ ] `C-CF-190` `literal` The right rail shows a month grid with the current day filled, a `Day 1` label, a countdown read to the second. `src: Core features progress rule 2`
- [ ] `C-CF-191` `capability` A first accepted solve of any problem starts the streak at one. `src: Core features progress rule 3`
- [ ] `C-CF-192` `constraint` A solve the day after the last qualifying day increments the streak by one. `src: Core features progress rule 4`
- [ ] `C-CF-193` `constraint` A solve after a gap resets the streak to one, keeping the longest run. `src: Core features progress rule 4`
- [ ] `C-CF-194` `constraint` The streak keeps the longest run at or above the current run. `src: Core features progress rule 4`
- [ ] `C-CF-195` `constraint` The streak advances at most once for two solves on one day. `src: Core features progress rule 5`
- [ ] `C-CF-196` `literal` The coin ledger reasons are `daily`, `streak_milestone`, `contest`, `redemption`, `purchase`, `adjustment`, `refund`. `src: Core features progress rule 6`
- [ ] `C-CF-197` `constraint` The coin balance equals the ledger sum. `src: Core features progress rule 6`
- [ ] `C-CF-198` `constraint` Redeeming more coins than the balance is refused, leaving the balance unchanged. `src: Core features progress rule 6`
- [ ] `C-CF-199` `constraint` An accepted submission stores an integer runtime, memory figure, percentile. `src: Core features progress rule 7`
- [ ] `C-CF-200` `constraint` A wrong answer records no runtime, no memory figure. `src: Core features progress rule 7`
- [ ] `C-CF-201` `capability` The submission list returns the caller's own submissions newest first. `src: Core features progress rule 8`
- [ ] `C-CF-202` `ui` The `Submissions` tab lists attempts with verdict, language, runtime, memory, time. `src: Core features progress rule 8`
- [ ] `C-CF-203` `constraint` Another member's submission answers not-found. `src: Core features progress rule 8`
- [ ] `C-CF-204` `ui` The study plan route shows a featured row, then rows grouped by theme. `src: Core features learning rule 1`
- [ ] `C-CF-205` `literal` The learning page renders the pinned plan names `Bytefold 75`, `Top Interview 150`, `SQL 50`, `Introduction to Pandas`. `src: Core features learning rule 1`
- [ ] `C-CF-206` `literal` The study plan listing carries the four seeded plans `Bytefold 75`, `Top Interview 150`, `SQL 50`, `Introduction to Pandas`. `src: Core features learning rule 1`
- [ ] `C-CF-207` `literal` The learning page renders the pinned subtitles `Crack SQL Interview in 50 Qs`, `Learn Basic Pandas in 15 Qs`. `src: Core features learning rule 1`
- [ ] `C-CF-208` `literal` The learning page renders the pinned groups `Cracking Coding Interview`, `Advanced Algorithms`, `Most Liked`. `src: Core features learning rule 1`
- [ ] `C-CF-209` `literal` The featured plan public address `/studyplan/bytefold-75/` answers with a page. `src: Core features learning rule 1`
- [ ] `C-CF-210` `constraint` A plan detail lists the plan items in the authored order with the member's own status. `src: Core features learning rule 1`
- [ ] `C-CF-211` `constraint` Plan progress is derived from the solved set, never stored. `src: Core features learning rule 2`
- [ ] `C-CF-212` `capability` Solving a plan's problem from the catalogue advances the plan progress. `src: Core features learning rule 2`
- [ ] `C-CF-213` `ui` An explore card carries a cover, a chapter count, an item count, a two-line clamped excerpt. `src: Core features learning rule 3`
- [ ] `C-CF-214` `literal` The seeded explore cards `crash-course`, `beginners-guide`, `cheatsheet` answer at their own public addresses. `src: Core features learning rule 3`
- [ ] `C-CF-215` `ui` The premium `cheatsheet` card stays listed with the chapter bodies behind the entitlement. `src: Core features learning rule 3`
- [ ] `C-CF-216` `literal` The discussion feed carries at least `3` seeded posts with a category, a title, an author, a vote total, a view count, a reply count. `src: Core features learning rule 4`
- [ ] `C-CF-217` `literal` The discussion page renders the orders `Best`, `Hot`, `Newest`, `Most Votes`. `src: Core features learning rule 4`
- [ ] `C-CF-218` `ui` A feed row shows an upvote arrow with a count, an eye with a view count, a speech bubble with a reply count. `src: Core features learning rule 4`
- [ ] `C-CF-219` `constraint` A repeated vote in the same direction toggles the vote off. `src: Core features learning rule 5`
- [ ] `C-CF-220` `literal` An up-vote changed to a down-vote moves the vote total by `-2`. `src: Core features learning rule 5`
- [ ] `C-CF-221` `constraint` Simultaneous votes from one member leave at most one stored vote. `src: Core features learning rule 5`
- [ ] `C-CF-222` `constraint` A second read of a post on the same day leaves the view count unchanged. `src: Core features learning rule 6`
- [ ] `C-CF-223` `ui` A solution post carrying a full answer is collapsed behind a spoiler control by default. `src: Core features learning rule 7`
- [ ] `C-CF-224` `constraint` A contest listing entry carries a start instant, a duration in seconds, never an end. `src: Core features contests rule 1`
- [ ] `C-CF-225` `literal` A contest carries a cadence of `weekly`, `biweekly`, a state of `scheduled`, `running`, `finished`. `src: Core features contests rule 1`
- [ ] `C-CF-226` `capability` The running contest serves four problems, each with a value. `src: Core features contests rule 1`
- [ ] `C-CF-227` `literal` The contest route shows the running contest, the upcoming pair with a countdown, a ladder, past contests reading `0 / 4`. `src: Core features contests rule 1`
- [ ] `C-CF-228` `capability` Registration for a scheduled contest is stored once per member. `src: Core features contests rule 2`
- [ ] `C-CF-229` `capability` Registration for the running contest is accepted. `src: Core features contests rule 2`
- [ ] `C-CF-230` `constraint` A scheduled contest's problem list answers not-found before the window opens. `src: Core features contests rule 2`
- [ ] `C-CF-231` `constraint` An accepted contest submission on a problem adds the problem value to the contest total. `src: Core features contests rule 3`
- [ ] `C-CF-232` `literal` A compile error before the accepted submission adds `300` seconds of penalty. `src: Core features contests rule 4`
- [ ] `C-CF-233` `constraint` A wrong submission on a problem never solved adds no penalty. `src: Core features contests rule 5`
- [ ] `C-CF-234` `constraint` A wrong submission after the accepted one adds no penalty. `src: Core features contests rule 5`
- [ ] `C-CF-235` `constraint` Standings order by total descending, then penalty ascending. `src: Core features contests rule 6`
- [ ] `C-CF-236` `constraint` Repeated reads of the standings return the same order. `src: Core features contests rule 6`
- [ ] `C-CF-237` `capability` Standings answer at the contest's own ranking address. `src: Core features contests rule 7`
- [ ] `C-CF-238` `ui` The ladder carries each competitor's rating, attended count. `src: Core features contests rule 8`
- [ ] `C-CF-239` `ui` The pricing route shows two terms against the region price list. `src: Core features paid rule 1`
- [ ] `C-CF-240` `constraint` Every price is an integer of the minor unit with a currency code. `src: Core features paid rule 1`
- [ ] `C-CF-241` `literal` The seeded `US` price list in `usd` reads `3500` monthly, `15900` yearly against `42000`. `src: Core features paid rule 1`
- [ ] `C-CF-242` `literal` The subscribe route renders the prices `$35.00`, `$159.00`, the struck `$420.00`. `src: Core features paid rule 1`
- [ ] `C-CF-243` `literal` The yearly card renders the saving `62%`. `src: Core features paid rule 2`
- [ ] `C-CF-244` `literal` The yearly card renders the per-month figure `$13.25`. `src: Core features paid rule 2`
- [ ] `C-CF-245` `constraint` A price list row carries an effective window, an availability flag. `src: Core features paid rule 3`
- [ ] `C-CF-246` `literal` The `EU` price list in `eur` is seeded at `3200`, `14900`, not available. `src: Core features paid rule 3`
- [ ] `C-CF-247` `constraint` Subscribing in the unavailable `EU` region is rejected as invalid input. `src: Core features paid rule 3`
- [ ] `C-CF-248` `ui` The yearly card is tinted warm, marked `Most Popular`, with the strike price beside the annual amount. `src: Core features paid rule 4`
- [ ] `C-CF-249` `ui` Without the entitlement the debugger, autocomplete, saved playgrounds show a padlocked affordance. `src: Core features paid rule 4`
- [ ] `C-CF-250` `ui` Without the entitlement an editorial body shows a padlocked affordance with the price. `src: Core features paid rule 4`
- [ ] `C-CF-251` `constraint` Gated fields are absent from the payload, so employer tags reach only an entitled subscriber. `src: Core features paid rule 5`
- [ ] `C-CF-252` `constraint` A gated statement read without an entitlement is refused as payment-required, never forbidden. `src: Core features paid rule 6`
- [ ] `C-CF-253` `constraint` A premium row stays public, the premium body staying gated. `src: Core features paid rule 6`
- [ ] `C-CF-254` `constraint` Exactly one premium problem sits in each difficulty band. `src: Core features paid rule 6`
- [ ] `C-CF-255` `capability` Subscribing serves the gated statement on the next request. `src: Core features paid rule 7`
- [ ] `C-CF-256` `constraint` Subscribing twice stores one active entitlement. `src: Core features paid rule 7`


## C-UF User flow

- [ ] `C-UF-01` `capability` The public routes of the route table answer with a page, footer pages among them. `src: User flow route table`
- [ ] `C-UF-02` `contract` The public route addresses `/`, `/problemset/` answer with a page. `src: User flow route table rows 1-2`
- [ ] `C-UF-03` `contract` The app serves `/contest/<slug>/`, `/contest/<slug>/ranking/`, `/explore/<card>/`, `/studyplan/<slug>/`, `/discuss/post/<id>/`, `/u/<username>/` as public pages. `src: User flow route table`
- [ ] `C-UF-04` `contract` The app serves `/interview/online-interview/`, `/interview/assessment/` as public pages. `src: User flow route table rows 24-25`
- [ ] `C-UF-05` `contract` `/list/`, `/quest/`, `/playground/`, `/store/`, `/store/redeem/` are member-only routes. `src: User flow route table rows 19-23`
- [ ] `C-UF-06` `capability` A signed-out request for a member-only route redirects to sign-in carrying the intended path in `next`. `src: User flow entry para`
- [ ] `C-UF-07` `ui` Signing in from a redirect lands on the intended path rather than a dashboard. `src: User flow entry para`
- [ ] `C-UF-08` `ui` Signing out on a public route stays on that route. `src: User flow entry para`
- [ ] `C-UF-09` `ui` A member opening a gated body sees the padlocked affordance with the price, never a blank page. `src: User flow entry para`
- [ ] `C-UF-10` `ui` Ticking `Medium`, `Dynamic Programming` gives a total equal to the count shown beside the topic before ticking. `src: User flow journey 1`
- [ ] `C-UF-11` `ui` Clicking `1. Two Sum` arrives at `/problems/two-sum/description/`. `src: User flow journey 1`
- [ ] `C-UF-12` `ui` Pressing `Run` shows every example case in the `Result` tab with input, expected, produced, a pass mark. `src: User flow journey 2`
- [ ] `C-UF-13` `ui` The verdict panel shows `pending`, then `judging`, then a single verdict. `src: User flow journey 3`
- [ ] `C-UF-14` `ui` An accepted verdict shows the runtime, the memory, both percentiles. `src: User flow journey 3`
- [ ] `C-UF-15` `ui` Pressing `Submit` again at once with the same source is refused as a conflict. `src: User flow journey 3`
- [ ] `C-UF-16` `ui` A non-terminating submission reads `Time Limit Exceeded` naming the case index, the limit, the multiplier, the page still usable. `src: User flow journey 4`
- [ ] `C-UF-17` `ui` Registering for the scheduled contest leaves the contest problems unreadable. `src: User flow journey 5`
- [ ] `C-UF-18` `ui` Solving a problem marks the calendar day, advances the streak badge by one. `src: User flow journey 6`
- [ ] `C-UF-19` `ui` The subscriber opens a premium statement, the member sees the padlocked row for the same problem. `src: User flow journey 7`
- [ ] `C-UF-20` `ui` A filtered catalogue with no matches says so, offering to clear the narrowest facet. `src: User flow states para`
- [ ] `C-UF-21` `ui` The catalogue loading state is a skeleton of rows at the row's own height. `src: User flow states para`
- [ ] `C-UF-22` `ui` A failed region keeps the chrome, carries a message, a retry control. `src: User flow states para`


## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Outside the marketing route the product reads quiet, dense, organised. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The marketing shell is a full-bleed single column of bands with a dark hero cut by a diagonal wedge. `src: UI/UX notes shells para`
- [ ] `C-UX-03` `ui` The marketing route carries an embedded editor demonstration, a wall of employer marks. `src: UI/UX notes shells para`
- [ ] `C-UX-04` `ui` The application shell is a fixed top bar with a left rail, a centre column, a right rail at the widest tier. `src: UI/UX notes shells para`
- [ ] `C-UX-05` `ui` The marketing primary action arrives inside the application shell. `src: UI/UX notes shells para`
- [ ] `C-UX-06` `ui` The page ground is a near-white neutral behind pure white cards in the light theme. `src: UI/UX notes palette para`
- [ ] `C-UX-07` `ui` One hairline border value carries the product. `src: UI/UX notes palette para`
- [ ] `C-UX-08` `ui` The brand mark, the paid-tier link, premium affordances wear a vivid orange worn by nothing else. `src: UI/UX notes palette para`
- [ ] `C-UX-09` `ui` The primary action is a vivid blue, one per page. `src: UI/UX notes palette para`
- [ ] `C-UX-10` `ui` Difficulty wears teal for `Easy`, amber for `Medium`, red for `Hard`, the word always beside the colour. `src: UI/UX notes palette para`
- [ ] `C-UX-11` `ui` An accepted verdict is green, a pending or judging state a neutral rather than red. `src: UI/UX notes palette para`
- [ ] `C-UX-12` `ui` Badges, streak flames, event ribbons draw on five accents. `src: UI/UX notes palette para`
- [ ] `C-UX-13` `ui` Two themes ship, switched instantly from a control, remembered for the member after a reload. `src: UI/UX notes theme para`
- [ ] `C-UX-14` `constraint` With no member override the dark theme follows the operating system preference. `src: UI/UX notes theme para`
- [ ] `C-UX-15` `ui` The dark theme darkens the ground with independently authored role values. `src: UI/UX notes theme para`
- [ ] `C-UX-16` `ui` Every route meets WCAG AA contrast in both themes. `src: UI/UX notes contrast para`
- [ ] `C-UX-17` `ui` The three difficulty labels are resolved for contrast the same way. `src: UI/UX notes contrast para`
- [ ] `C-UX-18` `literal` The interface stack begins `system-ui` with body text at `14px` on `21px`. `src: UI/UX notes typography para`
- [ ] `C-UX-19` `literal` Code, the editor use the stack beginning `ui-monospace`. `src: UI/UX notes typography para`
- [ ] `C-UX-20` `ui` Anything larger than body text is a heading, anything smaller metadata, with no third register. `src: UI/UX notes typography para`
- [ ] `C-UX-21` `ui` Acceptance percentages, runtimes, penalties align on tabular figures down a column. `src: UI/UX notes typography para`
- [ ] `C-UX-22` `ui` Every icon is inline stroke geometry taking colour from the surrounding text, one geometry throughout. `src: UI/UX notes iconography para`
- [ ] `C-UX-23` `ui` Gradients stay decorative: a premium badge ribbon, a paid-tier wash, a striped progress bar, card covers. `src: UI/UX notes iconography para`
- [ ] `C-UX-24` `ui` Buttons, rows, inputs carry a near-square softness, pills, chips, the search field, the avatar being fully round. `src: UI/UX notes shape para`
- [ ] `C-UX-25` `ui` Learning cards are built from a head, a foot with the play control overhanging the seam. `src: UI/UX notes shape para`
- [ ] `C-UX-26` `ui` The application shell is compact with three elevation steps. `src: UI/UX notes shape para`
- [ ] `C-UX-27` `constraint` No rendered element transitions every property. `src: UI/UX notes motion para`
- [ ] `C-UX-28` `ui` The skeleton breath pulses on placeholder rows with a shimmer crossing an unloaded block. `src: UI/UX notes moments para`
- [ ] `C-UX-29` `ui` Expanding the topic rail moves height, position, transform together as hidden chips arrive. `src: UI/UX notes moments para`
- [ ] `C-UX-30` `ui` Contest ladder rows arrive in index order, each popping in with a blur that resolves. `src: UI/UX notes moments para`
- [ ] `C-UX-31` `ui` A toast rises from below overshooting once, leaving on opacity alone, at most three stacking. `src: UI/UX notes moments para`
- [ ] `C-UX-32` `ui` One marketing card drifts slowly, endlessly. `src: UI/UX notes moments para`
- [ ] `C-UX-33` `constraint` Under a reduced-motion preference no endless animation keeps running. `src: UI/UX notes reduced motion para`
- [ ] `C-UX-34` `ui` Every control shows a visible focus state, an unavailable state not signalled by colour alone. `src: UI/UX notes components para`
- [ ] `C-UX-35` `ui` `Escape` closes the topmost overlay. `src: UI/UX notes components para`
- [ ] `C-UX-36` `ui` Sign-up validation names the wrong field inline, writing nothing. `src: UI/UX notes components para`
- [ ] `C-UX-37` `ui` Creating a saved list opens a modal trapping focus, returning focus to the opener on close. `src: UI/UX notes components para`
- [ ] `C-UX-38` `ui` One primary action leads each page, visually distinct from every secondary action. `src: UI/UX notes primary action para`
- [ ] `C-UX-39` `ui` The catalogue, explore, study plan routes carry the left rail; contest, discussion, pricing carry none. `src: UI/UX notes layout para`
- [ ] `C-UX-40` `ui` At the narrowest tier the rail becomes a drawer behind a menu control, the row drops the frequency column. `src: UI/UX notes layout para`
- [ ] `C-UX-41` `ui` At the narrowest tier the price cards stack, the workspace becomes the `Problem`, `Code` switcher. `src: UI/UX notes layout para`
- [ ] `C-UX-42` `ui` On the tablet tier the rail returns as an icon-only strip, the contest pair stacking. `src: UI/UX notes layout para`
- [ ] `C-UX-43` `ui` At the widest tier the right rails appear, the main column centring. `src: UI/UX notes layout para`
- [ ] `C-UX-44` `constraint` At a narrow viewport no public route overflows sideways. `src: UI/UX notes layout para`
- [ ] `C-UX-45` `ui` At a narrow viewport the streak becomes a chip, employer chips an `Employers` facet, the digest a `Topics` control. `src: UI/UX notes panel para`
- [ ] `C-UX-46` `ui` The topic rail scrolls horizontally, snapping to chip boundaries, fading at both ends. `src: UI/UX notes panel para`
- [ ] `C-UX-47` `constraint` The catalogue is a table with header cells, a header carrying the sort state. `src: UI/UX notes accessibility para`
- [ ] `C-UX-48` `literal` The status tick is named `Solved`, an absent tick named nothing. `src: UI/UX notes accessibility para`
- [ ] `C-UX-49` `constraint` The pager marks the current page, a polite region announcing the result count. `src: UI/UX notes accessibility para`
- [ ] `C-UX-50` `constraint` The workspace exposes a tab list, polite, assertive live regions. `src: UI/UX notes accessibility para`
- [ ] `C-UX-51` `literal` The workspace editor is labelled, described by text stating the `Escape` sequence. `src: UI/UX notes accessibility para`
- [ ] `C-UX-52` `constraint` The contest countdown is a named timer. `src: UI/UX notes accessibility para`
- [ ] `C-UX-53` `literal` The shortcut `/` focuses the global search; `g` then `p` opens the catalogue; `g` then `c` opens contests. `src: UI/UX notes accessibility para`
- [ ] `C-UX-54` `literal` The keyboard shortcut `?` opens the shortcut sheet. `src: UI/UX notes accessibility para`
- [ ] `C-UX-55` `ui` The shortcut sheet is reachable from the account menu. `src: UI/UX notes accessibility para`
- [ ] `C-UX-56` `ui` No page is dominated by a single hue family, no decoration standing in for content. `src: UI/UX notes closing para`
- [ ] `C-UX-57` `ui` The catalogue opens on the working list rather than a marketing hero band. `src: UI/UX notes closing para`


## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` The backend is a NestJS application rendering Handlebars templates. `src: Technical requirements para 1`
- [ ] `C-TR-02` `constraint` The catalogue first response is server rendered, already carrying rows. `src: Technical requirements para 1`
- [ ] `C-TR-03` `constraint` Interactive fragments are requested by `hx-` attributes in the server-rendered markup. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The PostgreSQL at `DATABASE_URL` holds the members, problem tables. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The public origin, port come from `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `constraint` The app uses only the named libraries, no second database, cache, queue, object store, identity provider, mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-07` `contract` `GET /api/health` answers `200` on the public URL. `src: Technical requirements para 3`
- [ ] `C-TR-08` `literal` Every response carries an `X-Correlation-Id` header equal to a failure `trace`. `src: Technical requirements para 3`
- [ ] `C-TR-09` `constraint` The executing side holds no database credential, no route to the app HTTP surface. `src: Technical requirements para 4`
- [ ] `C-TR-10` `constraint` Intake records the submission, the program running afterwards. `src: Technical requirements para 5`
- [ ] `C-TR-11` `constraint` Publicly identical payloads are answered separately from per-member payloads. `src: Technical requirements para 6`
- [ ] `C-TR-12` `literal` A catalogue list response carries `count`, `limit`, `next_cursor`. `src: Technical requirements para 7`
- [ ] `C-TR-13` `literal` `fields=+category` adds `category` to every row; `fields=number,slug` returns only those fields. `src: Technical requirements para 7`
- [ ] `C-TR-14` `literal` A submission accepts an `Idempotency-Key` header. `src: Technical requirements para 7`
- [ ] `C-TR-15` `literal` A failure carries a `type` from `invalid_data`, `not_found`, `not_allowed`, `unauthorized`, `conflict`, `payment_required`, `unexpected_state`, `rate_limited`, `judge_unavailable`. `src: Technical requirements para 8`
- [ ] `C-TR-16` `constraint` A failure message is safe to show a member, never a stack trace. `src: Technical requirements para 8`
- [ ] `C-TR-17` `literal` A failure carries a `message`, a `code`, a `trace`. `src: Technical requirements para 8`
- [ ] `C-TR-18` `literal` The failure type travels with the status code: `400` `invalid_data`, `401` `unauthorized`, `402` `payment_required`, `404` `not_found`. `src: Technical requirements para 8`
- [ ] `C-TR-19` `constraint` Every public route carries a unique title, a unique description. `src: Technical requirements metadata para`
- [ ] `C-TR-20` `constraint` Every public route declares a social preview title, a social preview image resolving from the app origin. `src: Technical requirements metadata para`
- [ ] `C-TR-21` `constraint` The favicon is declared in the document head, resolving as a vector document. `src: Technical requirements metadata para`
- [ ] `C-TR-22` `constraint` Every browser request stays on the app origin. `src: Technical requirements metadata para`
- [ ] `C-TR-23` `constraint` No browser request on the app origin returns a database credential. `src: Technical requirements metadata para`
- [ ] `C-TR-24` `constraint` Browser requests stay free of a hot-reload client. `src: Technical requirements metadata para`
- [ ] `C-TR-25` `constraint` No binary image, font or video asset is fetched by the browser. `src: Technical requirements assets para`
- [ ] `C-TR-26` `ui` Every mark, glyph, illustration, employer logo is drawn inline as vector geometry. `src: Technical requirements assets para`
- [ ] `C-TR-27` `ui` An avatar is a monogram of initials on a ground derived from the name, stable per member. `src: Technical requirements assets para`
- [ ] `C-TR-28` `constraint` An accepted submission stores the runtime as integer milliseconds. `src: Technical requirements time para`
- [ ] `C-TR-29` `constraint` The contest listing carries durations as integer seconds. `src: Technical requirements time para`
- [ ] `C-TR-30` `literal` The daily endpoint reports the calendar day as `YYYY-MM-DD`. `src: Technical requirements time para`


## C-DM Data model

- [ ] `C-DM-01` `constraint` The pinned tables of the data model, twenty-four in all, carry their columns in the running PostgreSQL. `src: Data model intro`
- [ ] `C-DM-02` `literal` `/app/USER_README.md` lists each seeded account beside the password `deku-demo-pw-2026`. `src: Data model password para`
- [ ] `C-DM-03` `data` The members table carries `email`, `username`, `display_name`, `password_hash`, `state`, `region`, `theme`. `src: Data model members para`
- [ ] `C-DM-04` `data` The sessions table carries `member_id`, `last_seen_at`, `device_label`, `revoked_at`. `src: Data model sessions para`
- [ ] `C-DM-05` `data` The problems table carries `number`, `slug`, `difficulty`, `category`, `is_premium`, `state`, the counters. `src: Data model problems para`
- [ ] `C-DM-06` `literal` The problems table stores difficulty values `easy`, `medium`, `hard`; state values `draft`, `published`, `withdrawn`. `src: Data model problems para`
- [ ] `C-DM-07` `constraint` Published problems carry unique numbers, unique slugs. `src: Data model problems para`
- [ ] `C-DM-08` `constraint` Difficulty is authored, so a `Hard` row reads a high acceptance, a `Med.` row a low one. `src: Data model problems para`
- [ ] `C-DM-09` `constraint` The submissions table references the problem by identifier, carrying no problem number column. `src: Data model problems para`
- [ ] `C-DM-10` `data` The tag tables carry `slug`, `name`, `kind`, `problem_count`; the join carries `frequency` from `1` to `5`. `src: Data model tags para`
- [ ] `C-DM-11` `data` The problem signatures table carries `starter`, `entry_point`, `imports`, `parameters`, `returns`, `mutates`, `indent`. `src: Data model signatures para`
- [ ] `C-DM-12` `literal` The Two Sum signature declares `nums` of type `array<int>`, `target` of type `int`, returning `array<int>`. `src: Data model signatures para`
- [ ] `C-DM-13` `data` The `test_sets` tables carry `comparator`, `time_limit_ms`, `memory_limit_kb`, `output_limit_bytes` columns. `src: Data model test sets para`
- [ ] `C-DM-14` `literal` Every published problem stores an output limit, `65536` bytes for Two Sum. `src: Data model test sets para`
- [ ] `C-DM-15` `data` The `test_cases` tables carry `index`, `input`, `expected`, `is_example` columns. `src: Data model test sets para`
- [ ] `C-DM-16` `data` The submissions table carries `source_hash`, `context`, `verdict`, `failed_case_index`, `runtime_ms`, `memory_kb`, `idempotency_key`. `src: Data model submissions para`
- [ ] `C-DM-17` `literal` The submissions table stores context values `practice` or `contest:<slug>`. `src: Data model submissions para`
- [ ] `C-DM-18` `data` The run requests table stores unscored runs apart from submissions. `src: Data model run requests para`
- [ ] `C-DM-19` `data` The progress tables carry `first_accepted_at` for solved rows, `first_attempted_at` for attempted rows. `src: Data model solved set para`
- [ ] `C-DM-20` `constraint` Two accepted submissions arriving together leave one solved row. `src: Data model solved set para`
- [ ] `C-DM-21` `data` The progress tables store `last_qualifying_day` as a date column. `src: Data model streaks para`
- [ ] `C-DM-22` `constraint` Two draft writes arriving together leave one stored row holding one of the two bodies. `src: Data model drafts para`
- [ ] `C-DM-23` `data` The study plan tables carry `group`, `is_featured`, `is_premium`, `position`. `src: Data model study plans para`
- [ ] `C-DM-24` `data` The contests table carries `starts_at`, `duration_seconds`, `cadence`, `state`, no end column. `src: Data model contests para`
- [ ] `C-DM-25` `constraint` Two registrations arriving together leave one stored participation. `src: Data model contests para`
- [ ] `C-DM-26` `data` The prices table carries `amount_minor`, `list_amount_minor`, `available`, `effective_from`, `effective_to`. `src: Data model prices para`
- [ ] `C-DM-27` `data` The price tables carry `period_start`, `period_end`, entitlement state values active, canceled, expired. `src: Data model prices para`
- [ ] `C-DM-28` `data` The posts table carries `kind`, `view_count`; the votes table carries a `value` of -1 or 1. `src: Data model posts para`
- [ ] `C-DM-29` `data` The coin ledger table carries `sequence`, `delta`, `reason`, `reference` with no zero delta. `src: Data model coin ledger para`
- [ ] `C-DM-30` `literal` The catalogue lists `240` seeded published problems. `src: Data model seed para`
- [ ] `C-DM-31` `literal` The pinned daily row is the seeded `3568. Minimum Moves to Clean the Classroom`. `src: Data model seed para`
- [ ] `C-DM-32` `literal` Seeded rows read `47.4%` `Med.`, `49.2%` `Med.`, `39.9%` `Med.`, `47.5%` `Hard`, `21.7%` `Med.`, `65.6%` `Hard`, `68.1%` `Hard`, `76.4%` `Hard`. `src: Data model seed para`
- [ ] `C-DM-33` `literal` The app seeds `1. Two Sum` at `58.1%` `Easy`. `src: Data model seed para`
- [ ] `C-DM-34` `literal` The app seeds forty-seven topic tags by name from `Array` through `Rolling Hash`, each carrying a problem. `src: Data model seed para`
- [ ] `C-DM-35` `constraint` Every category, every topic tag carries at least one problem. `src: Data model seed para`
- [ ] `C-DM-36` `constraint` Topic tag counts equal the problems the catalogue returns for the tag. `src: Data model seed para`
- [ ] `C-DM-37` `literal` The Two Sum problem detail declares the topic tags `Array`, `Hash Table` when asked. `src: Data model seed para`
- [ ] `C-DM-38` `constraint` Every published problem stores signatures in both languages, ten cases, an example, a comparator. `src: Data model seed para`
- [ ] `C-DM-39` `literal` A hidden Two Sum case holds more than four values in `nums`. `src: Data model seed para`
- [ ] `C-DM-40` `literal` `46. Permutations` declares the `unordered` comparator at slug `permutations`. `src: Data model seed para`
- [ ] `C-DM-41` `literal` `4. Median of Two Sorted Arrays` at slug `median-of-two-sorted-arrays` declares `numeric-tolerance`. `src: Data model seed para`
- [ ] `C-DM-42` `literal` The contest listing seeds `weekly-contest-431` past, `weekly-contest-432` upcoming, `biweekly-contest-150` running for `14` days. `src: Data model contest seed para`
- [ ] `C-DM-43` `literal` The running contest problems `two-sum`, `add-two-numbers`, `median-of-two-sorted-arrays`, `sudoku-solver` carry the values `3`, `4`, `5`, `6`. `src: Data model contest seed para`
- [ ] `C-DM-44` `constraint` The scheduled contest stores four problems absent from the catalogue. `src: Data model contest seed para`
- [ ] `C-DM-45` `literal` Plan slugs `bytefold-75`, `top-interview-150` are seeded, the second premium, `Bytefold 75` carrying Two Sum. `src: Data model plan seed para`
- [ ] `C-DM-46` `literal` A seeded `solution` post on `1. Two Sum` sits in the discussion feed. `src: Data model plan seed para`
- [ ] `C-DM-47` `literal` `subscriber@example.com` holds an active yearly entitlement in region `US`. `src: Data model plan seed para`
- [ ] `C-DM-48` `constraint` The pinned tables carry seeded accounts, problems, plans once each. `src: Data model closing para`


## C-CN Constraints

- [ ] `C-CN-01` `constraint` The data model carries no organisation, team or workspace table above the member. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The footer download page is a public page of the product. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` Subscribing against the product's own price list serves the gated statement. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` Verification completes inside the product with no outbound mail. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` No public or member route offers a file input. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` No browser request reaches an analytics collector, captcha or identity provider off the origin. `src: Constraints bullet 6`
- [ ] `C-CN-07` `literal` The `/admin/` address answers not-found. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` A language outside `python3`, `javascript` is rejected as invalid input. `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` A submitted program makes no external network call. `src: Constraints bullet 9`
- [ ] `C-CN-10` `constraint` The server makes no external network call at run time. `src: Constraints bullet 9`
- [ ] `C-CN-11` `literal` Cursor pages cover all `240` stored problems at the seeded scale. `src: Constraints bullet 10`


## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The health route answers at `APP_PUBLIC_URL` from outside the app container. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The container-internal port `4173` is reached through the public port mapping. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The health route answers on the public origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` answers `200` through port `4173`. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app answers at verification time, started from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `literal` `/app/USER_README.md` carries the seeded credentials. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `constraint` Every browser request stays clear of a development client, so a production build serves the app. `src: Deployment contract bullet 7`
- [ ] `C-DC-09` `contract` The server keeps answering at verification time after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `literal` The server binds `0.0.0.0` so the health route answers from outside the container. `src: Deployment contract bullet 9`
- [ ] `C-DC-11` `constraint` The members, problem tables carry their pinned columns in the provided PostgreSQL rather than a started copy. `src: Deployment contract bullet 10`
- [ ] `C-DC-12` `constraint` The app uses only the named providers with no edge function, persistent volume, fixed container name or custom network. `src: Deployment contract bullets 11-12`
- [ ] `C-DC-13` `contract` An invalid call is rejected as a client error with the failure envelope. `src: Deployment contract API shapes para`
- [ ] `C-DC-14` `contract` A submission without a bearer token is rejected as unauthenticated. `src: Deployment contract API shapes para`
- [ ] `C-DC-15` `contract` `POST /api/auth/register` takes an email, a username, a password, answering registration identically for a known address. `src: Deployment contract API table`
- [ ] `C-DC-16` `contract` `POST /api/auth/login` signs a seeded account in, returning `access_token`, `member_id`, `username`, `state`. `src: Deployment contract API table`
- [ ] `C-DC-17` `contract` `POST /api/auth/logout` answers for a signed-in or signed-out caller. `src: Deployment contract API table`
- [ ] `C-DC-18` `contract` The in-product verification endpoint moves a new member to active. `src: Deployment contract API table`
- [ ] `C-DC-19` `contract` `GET /api/sessions` lists sessions with `device_label`, `last_seen_at`, `current`; `DELETE /api/sessions/<id>` ends one. `src: Deployment contract API table`
- [ ] `C-DC-20` `contract` `GET /api/me` returns `member_id`, `username`, `state`, `entitlement` for a member after verification. `src: Deployment contract API table`
- [ ] `C-DC-21` `contract` `GET /api/problems` lists the catalogue problems with `count`, `limit`, `next_cursor`, `pinned`, `rows`. `src: Deployment contract API table`
- [ ] `C-DC-22` `contract` `GET /api/problems/facets` returns `categories`, `topics`, `difficulty`, `employers` as value, count entries. `src: Deployment contract API table`
- [ ] `C-DC-23` `contract` `GET /api/problems/status` returns `problem_id`, `status` solved for a member. `src: Deployment contract API table`
- [ ] `C-DC-24` `contract` `GET /api/problems/<slug>` returns the detail fields with `comparator`, `time_limit_ms`, `memory_limit_kb`, `multipliers`. `src: Deployment contract API table`
- [ ] `C-DC-25` `contract` `GET /api/problems/<slug>/signature` declares `entry_point`, `parameters`, `returns`, `mutates`, `starter` in both languages. `src: Deployment contract API table`
- [ ] `C-DC-26` `contract` `GET /api/problems/<slug>/daily` returns `is_daily`, `day`, `seconds_remaining`. `src: Deployment contract API table`
- [ ] `C-DC-27` `contract` `POST /api/problems/<slug>/run` returns `run_id`, example cases carrying `kind`, `input`, `expected`, `produced`, `passed`. `src: Deployment contract API table`
- [ ] `C-DC-28` `contract` `POST /api/submissions` returns `submission_id` with `state` `pending`. `src: Deployment contract API table`
- [ ] `C-DC-29` `contract` `GET /api/submissions/<id>` returns verdict, runtime, memory, percentiles, `reveal`. `src: Deployment contract API table`
- [ ] `C-DC-30` `contract` `GET /api/submissions` returns the caller's own submissions newest first. `src: Deployment contract API table`
- [ ] `C-DC-31` `contract` `GET /api/drafts/<slug>`, `PUT /api/drafts/<slug>` read, write a draft by language. `src: Deployment contract API table`
- [ ] `C-DC-32` `contract` `GET /api/streak` returns `current`, `longest`, `last_qualifying_day` stored as a date. `src: Deployment contract API table`
- [ ] `C-DC-33` `contract` `GET /api/coins` returns `balance`; `POST /api/coins/redeem` takes an amount, a reference. `src: Deployment contract API table`
- [ ] `C-DC-34` `contract` `GET /api/studyplans` returns plans with `item_count`, `solved_count`; the detail returns ordered items. `src: Deployment contract API table`
- [ ] `C-DC-35` `contract` `GET /api/contests` returns `running`, `upcoming`, `past`, `ladder`. `src: Deployment contract API table`
- [ ] `C-DC-36` `contract` `GET /api/contests/<slug>/problems` returns the contest problems with a position, a value. `src: Deployment contract API table`
- [ ] `C-DC-37` `contract` `POST /api/contests/<slug>/register` records a registration. `src: Deployment contract API table`
- [ ] `C-DC-38` `contract` `GET /api/contests/<slug>/ranking` returns `rank`, `username`, `penalty`, `solved`. `src: Deployment contract API table`
- [ ] `C-DC-39` `contract` `GET /api/prices` returns `plan`, `region`, `currency`, `amount_minor`, `list_amount_minor`, `available`. `src: Deployment contract API table`
- [ ] `C-DC-40` `contract` `POST /api/subscribe` returns `plan`, `region`, `currency`, `amount_minor`, `period_start`, `period_end`, `state`, the gated statement served next. `src: Deployment contract API table`
- [ ] `C-DC-41` `contract` `GET /api/posts` returns feed entries; `GET /api/posts/<id>` returns `view_count`. `src: Deployment contract API table`
- [ ] `C-DC-42` `contract` `POST /api/posts/<id>/vote` toggles the vote, returning the total with `my_vote`. `src: Deployment contract API table`
- [ ] `C-DC-43` `constraint` A non-terminating solution settles as a time limit, so the judge really executes the program. `src: Deployment contract no mocks para`
- [ ] `C-DC-44` `constraint` A failing hidden case settles the verdict, computed from cases the page never sent. `src: Deployment contract no mocks para`
- [ ] `C-DC-45` `constraint` A time limit stops a program rather than delaying a response, so a sleeping program is stopped. `src: Deployment contract no mocks para`
- [ ] `C-DC-46` `constraint` A wrong answer leaves no solved row, so a solved row exists only after an accepted submission. `src: Deployment contract no mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `member@example.com` | seeded member email | C-RL-19 | User roles seed table row 1 |
| `nadia_roux` | seeded member username | C-RL-19 | User roles seed table row 1 |
| `member2@example.com` | second seeded member email | C-RL-20 | User roles seed table row 2 |
| `tomas_iversen` | second seeded member username | C-RL-20 | User roles seed table row 2 |
| `subscriber@example.com` | seeded subscriber email | C-RL-21 | User roles seed table row 3 |
| `priya_shah` | seeded subscriber username | C-RL-21 | User roles seed table row 3 |
| `deku-demo-pw-2026` | password for every seeded account | C-RL-22 | User roles para 3 after table |
| `200` | health route success code | C-CF-02 | Core features Auth para 1 |
| `access_token` | sign-in response field carrying the bearer token | C-CF-02 | Core features Auth para 1 |
| `8` | minimum password length in characters | C-CF-06 | Core features Auth para 1 |
| `128` | lower bound on the maximum password length | C-CF-07 | Core features Auth para 1 |
| `401` | status a wrong-password sign-in answers | C-CF-08 | Core features Auth para 1 |
| `unverified` | account state before address verification | C-CF-10 | Core features Auth rule 1 |
| `active` | account state after verification, also an entitlement state | C-CF-10 | Core features Auth rule 1 |
| `restricted` | account state after a moderation action | C-CF-10 | Core features Auth rule 1 |
| `locked` | account state after repeated failed sign-in | C-CF-10 | Core features Auth rule 1 |
| `deleted` | account state after a completed deletion | C-CF-10 | Core features Auth rule 1 |
| `5` | value of the third contest problem | C-CF-16 | Core features Auth rule 2 |
| `/problemset/` | catalogue route | C-CF-30 | Core features catalogue intro |
| `240` | published problems seeded | C-CF-30 | Core features catalogue intro |
| `category` | the exclusive catalogue filter axis | C-CF-33 | Core features catalogue rule 1 |
| `algorithms` | category value | C-CF-33 | Core features catalogue rule 1 |
| `database` | category value | C-CF-33 | Core features catalogue rule 1 |
| `shell` | category value | C-CF-33 | Core features catalogue rule 1 |
| `concurrency` | category value | C-CF-33 | Core features catalogue rule 1 |
| `javascript` | category value, also an offered language | C-CF-33 | Core features catalogue rule 1 |
| `pandas` | category value | C-CF-33 | Core features catalogue rule 1 |
| `All Topics` | default category pill label | C-CF-34 | Core features catalogue rule 1 |
| `Algorithms` | category pill label | C-CF-34 | Core features catalogue rule 1 |
| `Database` | category pill label | C-CF-34 | Core features catalogue rule 1 |
| `Shell` | category pill label | C-CF-34 | Core features catalogue rule 1 |
| `Concurrency` | category pill label | C-CF-34 | Core features catalogue rule 1 |
| `JavaScript` | category pill label | C-CF-34 | Core features catalogue rule 1 |
| `Pandas` | category pill label | C-CF-34 | Core features catalogue rule 1 |
| `topics` | the multi-select topic filter axis | C-CF-36 | Core features catalogue rule 1 |
| `47` | seeded topic tags | C-CF-36 | Core features catalogue rule 1 |
| `difficulty` | the multi-select difficulty filter axis | C-CF-37 | Core features catalogue rule 1 |
| `Easy` | difficulty word in a catalogue row and in a filter | C-CF-37 | Core features catalogue rule 1 |
| `Medium` | difficulty word in a filter | C-CF-37 | Core features catalogue rule 1 |
| `Hard` | difficulty word in a catalogue row and in a filter | C-CF-37 | Core features catalogue rule 1 |
| `status` | the per-member filter axis | C-CF-38 | Core features catalogue rule 1 |
| `all` | status value meaning no per-member narrowing | C-CF-38 | Core features catalogue rule 1 |
| `unsolved` | status value, also a per-member overlay value | C-CF-38 | Core features catalogue rule 1 |
| `solved` | status value, also a per-member overlay value | C-CF-38 | Core features catalogue rule 1 |
| `attempted` | status value, also a per-member overlay value | C-CF-38 | Core features catalogue rule 1 |
| `50` | catalogue rows per page | C-CF-55 | Core features catalogue rule 7 |
| `<number>. <title>` | catalogue row title scheme | C-CF-62 | Core features catalogue rule 10 |
| `Med.` | difficulty word in a catalogue row | C-CF-64 | Core features catalogue rule 10 |
| `Search questions` | catalogue search field placeholder | C-CF-76 | Core features catalogue rule 15 |
| `0/240 Solved` | solved counter copy in the control row | C-CF-78 | Core features catalogue rule 15 |
| `Weekly Premium` | right rail strip title | C-CF-79 | Core features catalogue rule 15 |
| `W1` | first weekly premium slot label | C-CF-79 | Core features catalogue rule 15 |
| `W5` | last weekly premium slot label | C-CF-79 | Core features catalogue rule 15 |
| `Redeem` | coin redemption link label | C-CF-80 | Core features catalogue rule 15 |
| `Rules` | coin rules link label | C-CF-80 | Core features catalogue rule 15 |
| `Search for a company...` | trending employers search placeholder | C-CF-81 | Core features catalogue rule 15 |
| `Library` | left rail destination label | C-CF-84 | Core features catalogue rule 16 |
| `Quest` | left rail destination label | C-CF-84 | Core features catalogue rule 16 |
| `Explore` | left rail destination label | C-CF-84 | Core features catalogue rule 16 |
| `Study Plan` | left rail destination label | C-CF-84 | Core features catalogue rule 16 |
| `Help Center` | footer destination label | C-CF-84 | Core features catalogue rule 16 |
| `Bug Bounty` | footer destination label | C-CF-84 | Core features catalogue rule 16 |
| `Terms` | footer destination label | C-CF-84 | Core features catalogue rule 16 |
| `Privacy Policy` | footer destination label | C-CF-84 | Core features catalogue rule 16 |
| `Online Interview` | interview surface link label | C-CF-85 | Core features catalogue rule 16 |
| `Assessment` | assessment surface link label | C-CF-85 | Core features catalogue rule 16 |
| `Store` | top bar menu label | C-CF-85 | Core features catalogue rule 16 |
| `Download App` | footer download page link label | C-CF-85 | Core features catalogue rule 16 |
| `/description/` | workspace statement tab path suffix | C-CF-90 | Core features workspace rule 1 |
| `/editorial/` | workspace editorial tab path suffix | C-CF-90 | Core features workspace rule 1 |
| `/solutions/` | workspace solutions tab path suffix | C-CF-90 | Core features workspace rule 1 |
| `/submissions/` | workspace submissions tab path suffix | C-CF-90 | Core features workspace rule 1 |
| `Input` | example block label in a statement | C-CF-94 | Core features workspace rule 2 |
| `Output` | example block label in a statement | C-CF-94 | Core features workspace rule 2 |
| `Topics` | spoiler disclosure label, also the narrow-width digest control | C-CF-96 | Core features workspace rule 3 |
| `Discussion` | metadata strip link label | C-CF-98 | Core features workspace rule 3 |
| `Problem` | narrow workspace tab label | C-CF-104 | Core features workspace rule 5 |
| `Code` | narrow workspace tab label | C-CF-104 | Core features workspace rule 5 |
| `python3` | offered language | C-CF-109 | Core features editor rule 1 |
| `Testcase` | console tab label | C-CF-121 | Core features editor rule 4 |
| `Result` | console tab label | C-CF-121 | Core features editor rule 4 |
| `Debugger` | console tab label | C-CF-121 | Core features editor rule 4 |
| `10` | custom cases per problem, also the minimum cases per problem | C-CF-125 | Core features editor rule 4 |
| `Reset` | toolbar control label | C-CF-128 | Core features editor rule 7 |
| `Format` | toolbar control label | C-CF-128 | Core features editor rule 7 |
| `Copy` | toolbar control label | C-CF-128 | Core features editor rule 7 |
| `Run` | toolbar control label for an unscored execution | C-CF-128 | Core features editor rule 7 |
| `Submit` | toolbar control label for a scored execution | C-CF-128 | Core features editor rule 7 |
| `Notes` | toolbar control label | C-CF-128 | Core features editor rule 7 |
| `Timer` | toolbar control label for the member stopwatch | C-CF-128 | Core features editor rule 7 |
| `64KB` | submission source cap | C-CF-137 | Core features judge rule 1 |
| `pending` | submission state at intake | C-CF-143 | Core features judge rule 3 |
| `done` | submission state once settled | C-CF-144 | Core features judge rule 4 |
| `Accepted` | verdict when every case passes | C-CF-145 | Core features judge rule 4 |
| `Wrong Answer` | verdict when output fails the comparator | C-CF-145 | Core features judge rule 4 |
| `Time Limit Exceeded` | verdict when the processor-time limit is exceeded | C-CF-145 | Core features judge rule 4 |
| `Memory Limit Exceeded` | verdict when the memory limit is exceeded | C-CF-145 | Core features judge rule 4 |
| `Runtime Error` | verdict when the program exits non-zero | C-CF-145 | Core features judge rule 4 |
| `Compile Error` | verdict when the interpreter refuses the source | C-CF-145 | Core features judge rule 4 |
| `Output Limit Exceeded` | verdict when output passes the byte cap | C-CF-145 | Core features judge rule 4 |
| `Internal Error` | verdict for a platform fault | C-CF-145 | Core features judge rule 4 |
| `Rejected` | verdict for a submission refused for abuse | C-CF-145 | Core features judge rule 4 |
| `2000` | base processor-time limit in milliseconds | C-CF-159 | Core features judge rule 9 |
| `262144` | base memory limit in kilobytes | C-CF-159 | Core features judge rule 9 |
| `2.0` | javascript time multiplier | C-CF-160 | Core features judge rule 9 |
| `3.0` | python3 time multiplier | C-CF-160 | Core features judge rule 9 |
| `comparator` | problem detail field naming the declared comparator | C-CF-167 | Core features judge rule 11 |
| `exact` | comparator name | C-CF-167 | Core features judge rule 11 |
| `numeric-tolerance` | comparator name | C-CF-168 | Core features judge rule 11 |
| `1e-7` | median offset the numeric-tolerance comparator accepts | C-CF-168 | Core features judge rule 11 |
| `0.1` | median offset the numeric-tolerance comparator refuses | C-CF-168 | Core features judge rule 11 |
| `unordered` | comparator name | C-CF-169 | Core features judge rule 11 |
| `unordered-deep` | comparator name | C-CF-170 | Core features judge rule 11 |
| `any-of` | comparator name | C-CF-170 | Core features judge rule 11 |
| `1000` | hidden case revelation truncation in characters | C-CF-172 | Core features judge rule 12 |
| `4KB` | standard error truncation in a runtime error verdict | C-CF-175 | Core features judge rule 12 |
| `10s` | duplicate source refusal window | C-CF-179 | Core features judge rule 13 |
| `UTC` | the fixed zone a day is measured in | C-CF-187 | Core features progress rule 1 |
| `Day 1` | daily calendar label in the right rail | C-CF-190 | Core features progress rule 2 |
| `daily` | coin ledger reason | C-CF-196 | Core features progress rule 6 |
| `streak_milestone` | coin ledger reason | C-CF-196 | Core features progress rule 6 |
| `contest` | coin ledger reason | C-CF-196 | Core features progress rule 6 |
| `redemption` | coin ledger reason | C-CF-196 | Core features progress rule 6 |
| `purchase` | coin ledger reason | C-CF-196 | Core features progress rule 6 |
| `adjustment` | coin ledger reason | C-CF-196 | Core features progress rule 6 |
| `refund` | coin ledger reason | C-CF-196 | Core features progress rule 6 |
| `Bytefold 75` | seeded study plan name | C-CF-205 | Core features learning rule 1 |
| `Top Interview 150` | seeded study plan name | C-CF-205 | Core features learning rule 1 |
| `SQL 50` | seeded study plan name | C-CF-205 | Core features learning rule 1 |
| `Introduction to Pandas` | seeded study plan name | C-CF-205 | Core features learning rule 1 |
| `Crack SQL Interview in 50 Qs` | SQL 50 plan subtitle | C-CF-207 | Core features learning rule 1 |
| `Learn Basic Pandas in 15 Qs` | Introduction to Pandas plan subtitle | C-CF-207 | Core features learning rule 1 |
| `Cracking Coding Interview` | study plan group heading | C-CF-208 | Core features learning rule 1 |
| `Advanced Algorithms` | study plan group heading | C-CF-208 | Core features learning rule 1 |
| `Most Liked` | study plan group heading | C-CF-208 | Core features learning rule 1 |
| `/studyplan/bytefold-75/` | featured study plan address | C-CF-209 | Core features learning rule 1 |
| `crash-course` | seeded explore card slug | C-CF-214 | Core features learning rule 3 |
| `beginners-guide` | seeded explore card slug | C-CF-214 | Core features learning rule 3 |
| `cheatsheet` | seeded premium explore card slug | C-CF-214 | Core features learning rule 3 |
| `3` | retry attempt cap, also the wall-clock multiple of the processor limit | C-CF-216 | Core features learning rule 4 |
| `Best` | default discussion order name | C-CF-217 | Core features learning rule 4 |
| `Hot` | discussion order name | C-CF-217 | Core features learning rule 4 |
| `Newest` | discussion order name | C-CF-217 | Core features learning rule 4 |
| `Most Votes` | discussion order name | C-CF-217 | Core features learning rule 4 |
| `-2` | vote total change when an up-vote becomes a down-vote | C-CF-220 | Core features learning rule 5 |
| `weekly` | contest cadence | C-CF-225 | Core features contests rule 1 |
| `biweekly` | contest cadence | C-CF-225 | Core features contests rule 1 |
| `scheduled` | contest state before the window opens | C-CF-225 | Core features contests rule 1 |
| `running` | contest state inside the window | C-CF-225 | Core features contests rule 1 |
| `finished` | contest state after the window closes | C-CF-225 | Core features contests rule 1 |
| `0 / 4` | past contest solved count copy | C-CF-227 | Core features contests rule 1 |
| `300` | penalty seconds per earlier unaccepted contest submission | C-CF-232 | Core features contests rule 4 |
| `US` | seeded price list region | C-CF-241 | Core features paid rule 1 |
| `usd` | seeded price list currency | C-CF-241 | Core features paid rule 1 |
| `3500` | seeded monthly price in minor units | C-CF-241 | Core features paid rule 1 |
| `15900` | seeded yearly price in minor units | C-CF-241 | Core features paid rule 1 |
| `42000` | seeded yearly list price in minor units | C-CF-241 | Core features paid rule 1 |
| `$35.00` | monthly price as displayed | C-CF-242 | Core features paid rule 1 |
| `$159.00` | yearly price as displayed | C-CF-242 | Core features paid rule 1 |
| `$420.00` | struck yearly list price as displayed | C-CF-242 | Core features paid rule 1 |
| `62%` | computed yearly saving as displayed | C-CF-243 | Core features paid rule 2 |
| `$13.25` | yearly per-month figure as displayed | C-CF-244 | Core features paid rule 2 |
| `EU` | seeded region priced but unavailable | C-CF-246 | Core features paid rule 3 |
| `eur` | currency of the EU price list | C-CF-246 | Core features paid rule 3 |
| `3200` | EU monthly price in minor units | C-CF-246 | Core features paid rule 3 |
| `14900` | EU yearly price in minor units | C-CF-246 | Core features paid rule 3 |
| `system-ui` | first family of the interface font stack | C-UX-18 | UI/UX notes typography para |
| `14px` | body text size | C-UX-18 | UI/UX notes typography para |
| `21px` | body line height | C-UX-18 | UI/UX notes typography para |
| `ui-monospace` | first family of the code font stack | C-UX-19 | UI/UX notes typography para |
| `Solved` | accessible name of the status tick | C-UX-48 | UI/UX notes accessibility para |
| `Escape` | key named in the editor description for leaving the editor | C-UX-51 | UI/UX notes accessibility para |
| `/` | shortcut focusing the global search, also the marketing route | C-UX-53 | UI/UX notes accessibility para |
| `g` | first key of the navigation chords | C-UX-53 | UI/UX notes accessibility para |
| `p` | second key of the catalogue chord | C-UX-53 | UI/UX notes accessibility para |
| `c` | second key of the contests shortcut chord | C-UX-53 | UI/UX notes accessibility para |
| `?` | shortcut opening the sheet of chords | C-UX-54 | UI/UX notes accessibility para |
| `X-Correlation-Id` | response header carrying the correlation identifier | C-TR-08 | Technical requirements para 3 |
| `trace` | failure field carrying the correlation identifier | C-TR-08 | Technical requirements para 3 |
| `count` | catalogue list field carrying the total | C-TR-12 | Technical requirements para 7 |
| `limit` | catalogue list field carrying the page size | C-TR-12 | Technical requirements para 7 |
| `next_cursor` | catalogue list field carrying the next cursor | C-TR-12 | Technical requirements para 7 |
| `fields=+category` | fields parameter adding category to the default row | C-TR-13 | Technical requirements para 7 |
| `fields=number,slug` | fields parameter replacing the default row fields | C-TR-13 | Technical requirements para 7 |
| `Idempotency-Key` | header accepted by every mutating request | C-TR-14 | Technical requirements para 7 |
| `type` | failure envelope field naming the failure class | C-TR-15 | Technical requirements para 8 |
| `invalid_data` | failure type for invalid input | C-TR-15 | Technical requirements para 8 |
| `not_found` | failure type for a record that must not be confirmed | C-TR-15 | Technical requirements para 8 |
| `not_allowed` | failure type for a forbidden action on a public record | C-TR-15 | Technical requirements para 8 |
| `unauthorized` | failure type for absent or invalid credentials | C-TR-15 | Technical requirements para 8 |
| `conflict` | failure type for a conflicting request | C-TR-15 | Technical requirements para 8 |
| `payment_required` | failure type for a gated read without an entitlement | C-TR-15 | Technical requirements para 8 |
| `unexpected_state` | failure type for a request the state cannot satisfy | C-TR-15 | Technical requirements para 8 |
| `rate_limited` | failure type for a refused rate | C-TR-15 | Technical requirements para 8 |
| `judge_unavailable` | failure type when the judge cannot accept work | C-TR-15 | Technical requirements para 8 |
| `message` | failure field safe to show a member | C-TR-17 | Technical requirements para 8 |
| `code` | failure field carrying the machine-readable code | C-TR-17 | Technical requirements para 8 |
| `400` | status paired with invalid_data | C-TR-18 | Technical requirements para 8 |
| `402` | status paired with payment_required | C-TR-18 | Technical requirements para 8 |
| `404` | status paired with not_found | C-TR-18 | Technical requirements para 8 |
| `YYYY-MM-DD` | format of a calendar day in the API | C-TR-30 | Technical requirements time para |
| `/app/USER_README.md` | credential file path | C-DM-02 | Data model password para |
| `easy` | stored difficulty value | C-DM-06 | Data model problems para |
| `medium` | stored difficulty value | C-DM-06 | Data model problems para |
| `hard` | stored difficulty value | C-DM-06 | Data model problems para |
| `draft` | problem state before review | C-DM-06 | Data model problems para |
| `published` | problem state once live | C-DM-06 | Data model problems para |
| `withdrawn` | problem state after removal | C-DM-06 | Data model problems para |
| `nums` | the integer array parameter of the seeded Two Sum signature | C-DM-12 | Data model signatures para |
| `array<int>` | signature type of the Two Sum nums parameter and return | C-DM-12 | Data model signatures para |
| `target` | the integer parameter of the seeded Two Sum signature | C-DM-12 | Data model signatures para |
| `int` | signature type of the Two Sum target parameter | C-DM-12 | Data model signatures para |
| `65536` | default output limit in bytes | C-DM-14 | Data model test sets para |
| `practice` | submission context outside a contest | C-DM-17 | Data model submissions para |
| `contest:<slug>` | submission context for a contest | C-DM-17 | Data model submissions para |
| `3568. Minimum Moves to Clean the Classroom` | seeded daily featured problem | C-DM-31 | Data model seed para |
| `47.4%` | seeded acceptance figure for the daily featured problem | C-DM-32 | Data model seed para |
| `49.2%` | seeded acceptance figure for Add Two Numbers | C-DM-32 | Data model seed para |
| `39.9%` | seeded acceptance of 3. Longest Substring Without Repeating Characters | C-DM-32 | Data model seed para |
| `47.5%` | seeded acceptance figure for Median of Two Sorted Arrays | C-DM-32 | Data model seed para |
| `21.7%` | seeded acceptance figure for String to Integer | C-DM-32 | Data model seed para |
| `65.6%` | seeded acceptance figure for Sudoku Solver | C-DM-32 | Data model seed para |
| `68.1%` | seeded acceptance of 42. Trapping Rain Water | C-DM-32 | Data model seed para |
| `76.4%` | seeded acceptance of 51. N-Queens | C-DM-32 | Data model seed para |
| `1. Two Sum` | seeded catalogue row | C-DM-33 | Data model seed para |
| `58.1%` | seeded acceptance figure for Two Sum | C-DM-33 | Data model seed para |
| `Array` | first seeded topic tag by name | C-DM-34 | Data model seed para |
| `Rolling Hash` | last seeded topic tag by name | C-DM-34 | Data model seed para |
| `Hash Table` | topic tag carried by 1. Two Sum | C-DM-37 | Data model seed para |
| `46. Permutations` | seeded problem declaring the unordered comparator | C-DM-40 | Data model seed para |
| `permutations` | slug of 46. Permutations | C-DM-40 | Data model seed para |
| `4. Median of Two Sorted Arrays` | seeded catalogue row | C-DM-41 | Data model seed para |
| `median-of-two-sorted-arrays` | slug of 4. Median of Two Sorted Arrays | C-DM-41 | Data model seed para |
| `weekly-contest-431` | seeded finished contest slug | C-DM-42 | Data model contest seed para |
| `weekly-contest-432` | seeded scheduled contest slug | C-DM-42 | Data model contest seed para |
| `biweekly-contest-150` | seeded running contest slug | C-DM-42 | Data model contest seed para |
| `14` | days the running contest lasts | C-DM-42 | Data model contest seed para |
| `two-sum` | slug of 1. Two Sum | C-DM-43 | Data model contest seed para |
| `add-two-numbers` | slug of 2. Add Two Numbers | C-DM-43 | Data model contest seed para |
| `sudoku-solver` | slug of 37. Sudoku Solver | C-DM-43 | Data model contest seed para |
| `4` | value of the second contest problem | C-DM-43 | Data model contest seed para |
| `6` | value of the fourth contest problem | C-DM-43 | Data model contest seed para |
| `bytefold-75` | featured study plan slug | C-DM-45 | Data model plan seed para |
| `top-interview-150` | premium study plan slug | C-DM-45 | Data model plan seed para |
| `solution` | post kind of the seeded Two Sum solution post | C-DM-46 | Data model plan seed para |
| `/admin/` | address answering not-found because no operator console ships | C-CN-07 | Constraints bullet 7 |
| `0.0.0.0` | required bind address | C-DC-10 | Deployment contract bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 13 |
| User roles | 3 | 22 |
| Core features | 62 | 256 |
| User flow | 11 | 22 |
| UI and UX notes | 14 | 57 |
| Technical requirements | 8 | 30 |
| Data model | 13 | 48 |
| Constraints | 2 | 11 |
| Deployment contract | 19 | 46 |

The instruction also carries a `## Definition of done` section. Every clause in it restates an
obligation already carried by an item above, so under the restatement rule it produces no block
of its own and no ledger row.
