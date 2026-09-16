# Checklist: Meridian Cloud

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment, done
Sections absent: buildplan
Items: 797
Unpinned values flagged: 1

Declared section code: `C-FE` Front-end specification.

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public site for the cloud platform `Meridian Cloud`. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app serves a private desk with its own sign-in for the staff who publish the site. `src: Overview para 1`
- [ ] `C-OV-03` `ui` The site makes credible the claim that `Tessera` stays strongly consistent across regions. `src: Overview para 1`
- [ ] `C-OV-04` `constraint` A visitor reads the published product pages with no account. `src: Overview para 2`
- [ ] `C-OV-05` `capability` A visitor browses the published products as a flat index. `src: Overview para 2`
- [ ] `C-OV-06` `capability` A visitor browses products through the three seeded product families. `src: Overview para 2`
- [ ] `C-OV-07` `capability` A visitor browses products through the six seeded industry solutions. `src: Overview para 2`
- [ ] `C-OV-08` `capability` A visitor opens a product to read its claims with its highlights rail. `src: Overview para 2`
- [ ] `C-OV-09` `capability` A visitor downloads a datasheet from its card. `src: Overview para 2`
- [ ] `C-OV-10` `capability` A visitor looks through the card art of every published product in one grid. `src: Overview para 2`
- [ ] `C-OV-11` `capability` A visitor writes a value in one named console region, reading the value back from another. `src: Overview para 2`
- [ ] `C-OV-12` `capability` A visitor reads the synchronized-clock uncertainty band in the console. `src: Overview para 2`
- [ ] `C-OV-13` `capability` A visitor severs a link between console regions, then restores the link. `src: Overview para 2`
- [ ] `C-OV-14` `capability` A visitor ends by submitting the contact-sales form. `src: Overview para 2`
- [ ] `C-OV-15` `capability` Data architects are answered by the flagship product route with the console. `src: Overview para 3`
- [ ] `C-OV-16` `capability` Engineering leaders are answered by the highlights rail with the service level. `src: Overview para 3`
- [ ] `C-OV-17` `capability` Platform teams are answered by the industry solutions. `src: Overview para 3`
- [ ] `C-OV-18` `capability` Executives with analysts are answered by the customer proof wall. `src: Overview para 3`
- [ ] `C-OV-19` `constraint` No audience is served by a surface the brief does not describe. `src: Overview para 3`
- [ ] `C-OV-20` `capability` An editor drafts a product page, attaching its art with its datasheet. `src: Overview para 4`
- [ ] `C-OV-21` `capability` A publisher publishes a product page, then returns the page to draft. `src: Overview para 4`
- [ ] `C-OV-22` `capability` An administrator reads the stored contact-sales submissions with the page-view log. `src: Overview para 4`
- [ ] `C-OV-23` `constraint` An unpublished product is absent from every public surface. `src: Overview para 4`
- [ ] `C-OV-24` `constraint` The address of an unpublished product answers not found. `src: Overview para 4`
- [ ] `C-OV-25` `constraint` Nothing on the site is bought. `src: Overview para 5`
- [ ] `C-OV-26` `constraint` No visitor account exists. `src: Overview para 5`
- [ ] `C-OV-27` `constraint` The assistant calls no language model. `src: Overview para 5`
- [ ] `C-OV-28` `capability` A visitor reads the eight published products, proves a cross-region read on the console, sends an enquiry an administrator finds. `src: Definition of done`
- [ ] `C-OV-29` `constraint` A draft product, its art, its datasheet stay unreadable outside the desk until published. `src: Definition of done`

## C-RL User roles

- [ ] `C-RL-01` `role` The app carries four roles, `visitor`, `editor`, `publisher`, `administrator`. `src: User roles table`
- [ ] `C-RL-02` `role` A `visitor` holds no account. `src: User roles table`
- [ ] `C-RL-03` `role` A visitor reads every published product, family, industry, datasheet, art piece. `src: User roles table`
- [ ] `C-RL-04` `role` A visitor uses the console. `src: User roles table`
- [ ] `C-RL-05` `role` A visitor writes a contact-sales submission. `src: User roles table`
- [ ] `C-RL-06` `role` A visitor cannot read a draft, its art or its datasheet. `src: User roles table`
- [ ] `C-RL-07` `role` A visitor cannot read an enquiry or the page-view log. `src: User roles table`
- [ ] `C-RL-08` `role` A visitor cannot reach the desk. `src: User roles table`
- [ ] `C-RL-09` `constraint` The app seeds no account for a `visitor`. `src: User roles table`
- [ ] `C-RL-10` `role` An `editor` holds a seeded account. `src: User roles table`
- [ ] `C-RL-11` `role` An editor reads every product in both states at the desk. `src: User roles table`
- [ ] `C-RL-12` `role` An editor drafts a product, edits the product, attaches art with a datasheet, saves. `src: User roles table`
- [ ] `C-RL-13` `role` An editor cannot publish. `src: User roles table`
- [ ] `C-RL-14` `role` An editor cannot return a product to draft. `src: User roles table`
- [ ] `C-RL-15` `role` An editor cannot read an enquiry or the page-view log. `src: User roles table`
- [ ] `C-RL-16` `role` A `publisher` holds a seeded account. `src: User roles table`
- [ ] `C-RL-17` `role` A publisher writes everything an editor writes, plus publish with return to draft. `src: User roles table`
- [ ] `C-RL-18` `role` A publisher cannot read an enquiry or the page-view log. `src: User roles table`
- [ ] `C-RL-19` `role` An `administrator` holds a seeded account. `src: User roles table`
- [ ] `C-RL-20` `role` An administrator reads the stored enquiries with the page-view log. `src: User roles table`
- [ ] `C-RL-21` `constraint` Authorization is enforced server-side on every mutating endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-22` `constraint` A direct API call from an editor session to a publisher-only endpoint is denied, leaving the state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-23` `constraint` A direct API call from a publisher session to an administrator-only endpoint is denied. `src: User roles, authorization paragraph`
- [ ] `C-RL-24` `constraint` A direct API call with no session to a desk endpoint is denied. `src: User roles, authorization paragraph`
- [ ] `C-RL-25` `constraint` Signup is closed. `src: User roles, signup paragraph`
- [ ] `C-RL-26` `constraint` The app carries no registration form, no registration endpoint, no password reset. `src: User roles, signup paragraph`
- [ ] `C-RL-27` `literal` The app seeds the editor address `editor@example.com`. `src: User roles, seeded account table`
- [ ] `C-RL-28` `literal` The app seeds the publisher address `publisher@example.com`. `src: User roles, seeded account table`
- [ ] `C-RL-29` `literal` The app seeds the administrator address `administrator@example.com`. `src: User roles, seeded account table`
- [ ] `C-RL-30` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles, seeded account table`
- [ ] `C-RL-31` `contract` The app writes each seeded address with its password into `/app/USER_README.md`. `src: User roles, seeded account table`

## C-CF Core features

- [ ] `C-CF-01` `constraint` The app keeps a `draft` product out of the product index. `src: Core features rule 1`
- [ ] `C-CF-02` `constraint` The app keeps a `draft` product out of every family. `src: Core features rule 1`
- [ ] `C-CF-03` `constraint` The app keeps a `draft` product datasheet absent from the grid of download cards. `src: Core features rule 1`
- [ ] `C-CF-04` `constraint` The app keeps a `draft` product out of the art gallery. `src: Core features rule 1`
- [ ] `C-CF-05` `constraint` The app keeps a `draft` product out of the header search overlay. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` The app keeps a `draft` product out of the related row of any other product. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` The app keeps a `draft` product out of the home product rail. `src: Core features rule 1`
- [ ] `C-CF-08` `constraint` The app keeps a `draft` product out of the mega-menu. `src: Core features rule 1`
- [ ] `C-CF-09` `constraint` The app keeps a `draft` product out of the industry proof cards. `src: Core features rule 1`
- [ ] `C-CF-10` `constraint` Returning a published product to draft removes the product from every public surface at once. `src: Core features rule 1`
- [ ] `C-CF-11` `constraint` A `draft` product address answers exactly as an address naming no product does. `src: Core features rule 2`
- [ ] `C-CF-12` `constraint` A `draft` product address never answers forbidden. `src: Core features rule 2`
- [ ] `C-CF-13` `constraint` The art bytes of a `draft` product answer not found to a request carrying no valid desk bearer token. `src: Core features rule 3`
- [ ] `C-CF-14` `constraint` The datasheet bytes of a `draft` product answer not found to a request carrying no valid desk bearer token. `src: Core features rule 3`
- [ ] `C-CF-15` `constraint` The bucket is not readable without credentials. `src: Core features rule 3`
- [ ] `C-CF-16` `capability` A request carrying a desk bearer token is served the bytes of a `draft` product. `src: Core features rule 3`
- [ ] `C-CF-17` `constraint` Returning a product to draft stops its art with its datasheet bytes at once. `src: Core features rule 3`
- [ ] `C-CF-18` `constraint` No query parameter on a public endpoint makes the endpoint answer with a `draft` product. `src: Core features rule 4`
- [ ] `C-CF-19` `constraint` Every content image carries alternative text describing what the image depicts. `src: Core features rule 5`
- [ ] `C-CF-20` `constraint` A decorative image declares itself decorative with empty alternative text. `src: Core features rule 5`
- [ ] `C-CF-21` `constraint` The app refuses a publish where an art piece carries an empty description. `src: Core features rule 5`
- [ ] `C-CF-22` `capability` The app offers a cookie choice on the first public surface of a visitor. `src: Core features rule 6`
- [ ] `C-CF-23` `literal` The cookie choice carries an `Accept` control with a `Decline` control. `src: Core features rule 6`
- [ ] `C-CF-24` `capability` The cookie choice carries a link to the privacy page. `src: Core features rule 6`
- [ ] `C-CF-25` `constraint` The app sets no analytics cookie before the visitor chooses. `src: Core features rule 6`
- [ ] `C-CF-26` `constraint` The app sets no preference cookie before the visitor chooses. `src: Core features rule 6`
- [ ] `C-CF-27` `constraint` The only cookie a choice sets is the one recording the choice. `src: Core features rule 6`
- [ ] `C-CF-28` `capability` The app remembers the cookie choice across public surfaces. `src: Core features rule 7`
- [ ] `C-CF-29` `constraint` The cookie choice band does not return after a reload once chosen. `src: Core features rule 7`
- [ ] `C-CF-30` `constraint` A dismissed promo banner is remembered for the session without a cookie. `src: Core features rule 7`
- [ ] `C-CF-31` `constraint` No two public routes share a page title. `src: Core features rule 8`
- [ ] `C-CF-32` `constraint` No two public routes share a description meta tag. `src: Core features rule 8`
- [ ] `C-CF-33` `capability` A product page title carries the product name. `src: Core features rule 8`
- [ ] `C-CF-34` `capability` A product page description carries the product summary. `src: Core features rule 8`
- [ ] `C-CF-35` `capability` Every public route carries a canonical link to its own address. `src: Core features rule 9`
- [ ] `C-CF-36` `capability` The app records a page view for every public route the app serves. `src: Core features rule 10`
- [ ] `C-CF-37` `capability` A page view records the route as requested with the time. `src: Core features rule 10`
- [ ] `C-CF-38` `constraint` The page-view log carries no cookie, no visitor identifier. `src: Core features rule 10`
- [ ] `C-CF-39` `constraint` The page-view log records every view whatever the cookie choice. `src: Core features rule 10`
- [ ] `C-CF-40` `constraint` Only an administrator reads the page-view log. `src: Core features rule 10`
- [ ] `C-CF-41` `literal` The app serves the consistency console at `/console`. `src: Core features rule 11`
- [ ] `C-CF-42` `capability` The app embeds the consistency console among the home bands. `src: Core features rule 11`
- [ ] `C-CF-43` `literal` The app embeds the console on `/product/tessera`. `src: Core features rule 11`
- [ ] `C-CF-44` `literal` The console names the five regions `us-central`, `eu-west`, `asia-south`, `sa-east`, `au-southeast`. `src: Core features rule 12`
- [ ] `C-CF-45` `constraint` A console request naming any other region is refused as invalid. `src: Core features rule 12`
- [ ] `C-CF-46` `capability` A console write takes a region, a key, a value. `src: Core features rule 13`
- [ ] `C-CF-47` `literal` A console write answers with a commit timestamp with `uncertainty_ms`. `src: Core features rule 13`
- [ ] `C-CF-48` `constraint` `uncertainty_ms` is always greater than zero. `src: Core features rule 13`
- [ ] `C-CF-49` `constraint` A console write does not answer before `uncertainty_ms` milliseconds have passed. `src: Core features rule 13`
- [ ] `C-CF-50` `literal` Every console timestamp is an ISO 8601 UTC string with milliseconds, like `2026-09-16T09:06:10.123Z`. `src: Core features rule 13`
- [ ] `C-CF-51` `constraint` A console write missing its key or its value is refused as invalid, naming the missing field. `src: Core features rule 13`
- [ ] `C-CF-52` `literal` A console read takes a region, a key, a mode of `strong`, `bounded`, `exact`. `src: Core features rule 14`
- [ ] `C-CF-53` `capability` A console read answers with the value, its timestamp, its staleness, a latency figure. `src: Core features rule 14`
- [ ] `C-CF-54` `literal` The read staleness is whole milliseconds behind the latest acknowledged write, `0` for a `strong` read. `src: Core features rule 14`
- [ ] `C-CF-55` `capability` The read latency figure is a whole number of milliseconds. `src: Core features rule 14`
- [ ] `C-CF-56` `constraint` A console read in any other mode is refused as invalid. `src: Core features rule 14`
- [ ] `C-CF-57` `constraint` A read in mode `strong` never returns a value older than any acknowledged write. `src: Core features rule 15`
- [ ] `C-CF-58` `capability` Writing in one region, then reading from any other, returns the value just written. `src: Core features rule 15`
- [ ] `C-CF-59` `constraint` A read in mode `bounded` never returns a value staler than the bound the read is given. `src: Core features rule 16`
- [ ] `C-CF-60` `capability` A read in mode `exact` returns the value committed at or before the given timestamp. `src: Core features rule 16`
- [ ] `C-CF-61` `literal` A `bounded` read takes a bound of whole milliseconds above zero. `src: Core features rule 16`
- [ ] `C-CF-62` `constraint` A `bounded` read with no valid bound is refused as invalid, naming the bound. `src: Core features rule 16`
- [ ] `C-CF-63` `constraint` An `exact` read with no timestamp is refused as invalid, naming the timestamp. `src: Core features rule 16`
- [ ] `C-CF-64` `capability` The partition control severs one named region from the rest. `src: Core features rule 17`
- [ ] `C-CF-65` `capability` The partition control restores a severed region. `src: Core features rule 17`
- [ ] `C-CF-66` `constraint` Severing a region already severed changes nothing, answering the same five regions. `src: Core features rule 17`
- [ ] `C-CF-67` `constraint` A write against a severed region is refused. `src: Core features rule 18`
- [ ] `C-CF-68` `capability` The refusal says the region will not accept a write the region cannot safely agree on. `src: Core features rule 18`
- [ ] `C-CF-69` `capability` A write on the majority side still commits with a region severed. `src: Core features rule 18`
- [ ] `C-CF-70` `capability` Restoring a severed region re-syncs the region to the majority value. `src: Core features rule 19`
- [ ] `C-CF-71` `constraint` No console state is ever readable as corrupted or forked. `src: Core features rule 19`
- [ ] `C-CF-72` `capability` The console exposes the current value per region as text. `src: Core features rule 20`
- [ ] `C-CF-73` `capability` The console exposes the clock uncertainty as text. `src: Core features rule 20`
- [ ] `C-CF-74` `capability` The console exposes the partition status as text. `src: Core features rule 20`
- [ ] `C-CF-75` `capability` The console resets to its seeded state on request, every region unsevered. `src: Core features rule 21`
- [ ] `C-CF-76` `constraint` A reset with no region severed answers the same seeded state, changing nothing. `src: Core features rule 21`
- [ ] `C-CF-77` `literal` The app serves the flat product index at `/product` under its heading with a count line. `src: Core features rule 22`
- [ ] `C-CF-78` `capability` The product index carries a heading, a count line, a filter bar, a card grid. `src: Core features rule 22`
- [ ] `C-CF-79` `literal` The app serves one published product at `/product/{slug}` with its eyebrow, heading, highlights rail. `src: Core features rule 23`
- [ ] `C-CF-80` `capability` A product page carries its eyebrow, its heading, its lead, its summary. `src: Core features rule 23`
- [ ] `C-CF-81` `capability` A product page carries its highlights rail with one claim band per highlight line. `src: Core features rule 23`
- [ ] `C-CF-82` `capability` A product page carries its card art, its datasheet where the product has one, a related row. `src: Core features rule 23`
- [ ] `C-CF-83` `capability` The related row carries up to three other published products sharing a family. `src: Core features rule 24`
- [ ] `C-CF-84` `capability` The related row is ordered by sort index ascending. `src: Core features rule 24`
- [ ] `C-CF-85` `constraint` A product sharing no family with another shows no related row. `src: Core features rule 24`
- [ ] `C-CF-86` `capability` The app narrows the product index by name on a partial, case-insensitive match. `src: Core features rule 25`
- [ ] `C-CF-87` `capability` The app narrows the product index by family. `src: Core features rule 25`
- [ ] `C-CF-88` `literal` The family filter takes the family slug, like `?family=databases`. `src: Core features rule 25`
- [ ] `C-CF-89` `constraint` A family slug naming no family answers a top-level empty array. `src: Core features rule 25`
- [ ] `C-CF-90` `literal` The app orders the product index by name ascending where the sort is `name`. `src: Core features rule 26`
- [ ] `C-CF-91` `literal` The app orders the product index most recently added first where the sort is `recent`. `src: Core features rule 26`
- [ ] `C-CF-92` `constraint` A sort other than `name` or `recent` is refused as invalid. `src: Core features rule 26`
- [ ] `C-CF-93` `capability` The app carries the active name filter, family filter, sort in the address. `src: Core features rule 27`
- [ ] `C-CF-94` `constraint` Reloading a product-index address applies the same three selections again. `src: Core features rule 27`
- [ ] `C-CF-95` `literal` A product-index filter matching nothing answers with a top-level empty array. `src: Core features rule 28`
- [ ] `C-CF-96` `capability` The product index shows its empty message with a way to clear the filter. `src: Core features rule 28`
- [ ] `C-CF-97` `literal` The app serves the three seeded families at `/family`. `src: Core features rule 29`
- [ ] `C-CF-98` `capability` A family card carries the family name, its standfirst, its published count. `src: Core features rule 29`
- [ ] `C-CF-99` `literal` The app serves one family at `/family/{slug}` with its editorial introduction. `src: Core features rule 30`
- [ ] `C-CF-100` `capability` A family page carries its head, its standfirst, its editorial intro, its published products. `src: Core features rule 30`
- [ ] `C-CF-101` `constraint` A family holding no published product answers with an ordinary empty surface, never not found. `src: Core features rule 30`
- [ ] `C-CF-102` `literal` The app serves the six seeded industries at `/solution` filtered by chips reading `All` plus each industry name. `src: Core features rule 31`
- [ ] `C-CF-103` `capability` An industry card carries its name, its proof stat line, its named customer. `src: Core features rule 31`
- [ ] `C-CF-104` `capability` The home industry explorer swaps its right panel to the selected industry proof card. `src: Core features rule 32`
- [ ] `C-CF-105` `constraint` The industry explorer swaps without loading another address. `src: Core features rule 32`
- [ ] `C-CF-106` `literal` The app serves the datasheet library at `/datasheet`. `src: Core features rule 33`
- [ ] `C-CF-107` `capability` The library lists the datasheets of published products plus the three platform datasheets. `src: Core features rule 33`
- [ ] `C-CF-108` `ui` A datasheet card carries a cover generated from the document own first page. `src: Core features rule 34`
- [ ] `C-CF-109` `capability` A datasheet card carries its page count. `src: Core features rule 34`
- [ ] `C-CF-110` `literal` A datasheet card shows its file size in megabytes to one decimal place. `src: Core features rule 34`
- [ ] `C-CF-111` `ui` A datasheet cover is never a separately uploaded picture. `src: Core features rule 34`
- [ ] `C-CF-112` `capability` A datasheet registered with no picture of any kind still shows a cover. `src: Core features rule 34`
- [ ] `C-CF-113` `literal` A datasheet download carries a `Content-Disposition` of `attachment`. `src: Core features rule 35`
- [ ] `C-CF-114` `literal` `Meridian Platform Overview` downloads as `meridian-platform-overview.pdf`. `src: Core features rule 35`
- [ ] `C-CF-115` `literal` The app serves the art gallery at `/gallery` as one grid. `src: Core features rule 36`
- [ ] `C-CF-116` `literal` The art gallery pages at `24` pieces. `src: Core features rule 36`
- [ ] `C-CF-117` `capability` The art gallery narrows to one family. `src: Core features rule 36`
- [ ] `C-CF-118` `literal` The art gallery pages from page `1`, narrowing by family slug. `src: Core features rule 36`
- [ ] `C-CF-119` `constraint` A gallery page past the last answers a top-level empty array. `src: Core features rule 36`
- [ ] `C-CF-120` `constraint` A gallery page below `1` is refused as invalid. `src: Core features rule 36`
- [ ] `C-CF-121` `constraint` The app streams every art piece with every datasheet from the bucket itself. `src: Core features rule 37`
- [ ] `C-CF-122` `constraint` The app hands the browser no link to the bucket. `src: Core features rule 37`
- [ ] `C-CF-123` `capability` The app takes a contact submission of a full name, a work email, a company, a region, an interest. `src: Core features rule 38`
- [ ] `C-CF-124` `literal` The contact region is one of `Americas`, `Europe`, `Asia Pacific`. `src: Core features rule 38`
- [ ] `C-CF-125` `literal` The contact interest is one of `Evaluation`, `Migration`, `Pricing`. `src: Core features rule 38`
- [ ] `C-CF-126` `capability` The app answers a contact submission with an enquiry identifier. `src: Core features rule 38`
- [ ] `C-CF-127` `capability` The contact message is optional. `src: Core features rule 38`
- [ ] `C-CF-128` `constraint` The app refuses a submission whose work email is not an address. `src: Core features rule 39`
- [ ] `C-CF-129` `literal` The app refuses a contact name shorter than `2` characters. `src: Core features rule 39`
- [ ] `C-CF-130` `literal` The app refuses a contact message running past `1000` characters. `src: Core features rule 39`
- [ ] `C-CF-131` `constraint` The app refuses a submission whose region is outside the listed values. `src: Core features rule 39`
- [ ] `C-CF-132` `constraint` The app refuses a submission whose interest is outside the listed values. `src: Core features rule 39`
- [ ] `C-CF-133` `capability` A contact refusal names the field the refusal is about. `src: Core features rule 39`
- [ ] `C-CF-134` `capability` The app stores every contact submission. `src: Core features rule 40`
- [ ] `C-CF-135` `constraint` Only an administrator reads the stored submissions, newest first. `src: Core features rule 40`
- [ ] `C-CF-136` `literal` The app serves the assistant surface at `/ask` with its greeting, four suggestions, its counter. `src: Core features rule 41`
- [ ] `C-CF-137` `literal` Typing or pasting past `500` characters keeps the first 500 in the assistant field. `src: Core features rule 41`
- [ ] `C-CF-138` `capability` The assistant counter reads how many of the 500 characters are entered. `src: Core features rule 41`
- [ ] `C-CF-139` `constraint` The assistant sends a query nowhere, answering nothing. `src: Core features rule 41`
- [ ] `C-CF-140` `literal` The app serves the desk sign-in at `/desk/login`. `src: Core features rule 42`
- [ ] `C-CF-141` `constraint` A signed-out `/desk` shows the sign-in card rather than the product list. `src: Core features rule 42`
- [ ] `C-CF-142` `constraint` Every desk endpoint denies a request carrying no bearer token as unauthorized. `src: Core features rule 43`
- [ ] `C-CF-143` `constraint` Every desk endpoint denies a request carrying a malformed bearer token as unauthorized. `src: Core features rule 43`
- [ ] `C-CF-144` `constraint` A wrong password with an unknown address are refused identically. `src: Core features rule 44`
- [ ] `C-CF-145` `capability` The desk lists products in both states at `/desk`. `src: Core features rule 45`
- [ ] `C-CF-146` `literal` A desk row carries a badge reading `Live` or `Draft`. `src: Core features rule 45`
- [ ] `C-CF-147` `literal` The desk filter counts come from `GET /api/desk/products/counts` as `all`, `published`, `draft`. `src: Core features rule 45`
- [ ] `C-CF-148` `literal` Each desk row carries `art_count`. `src: Core features rule 45`
- [ ] `C-CF-149` `capability` Selecting a desk row opens the product detail pane beside the list without leaving `/desk`. `src: Core features rule 45`
- [ ] `C-CF-150` `literal` The detail pane control `Open in composer` opens `/desk/product/{id}`. `src: Core features rule 45`
- [ ] `C-CF-151` `constraint` Entering the composer creates no row. `src: Core features rule 46`
- [ ] `C-CF-152` `constraint` A product row comes into existence on the first save. `src: Core features rule 46`
- [ ] `C-CF-153` `constraint` An upload target is issued only for a product that already has an id. `src: Core features rule 46`
- [ ] `C-CF-154` `capability` An uploaded datasheet registers with its title, the app reading its page count from the stored document. `src: Core features rule 46`
- [ ] `C-CF-155` `constraint` Registering an object key the bucket does not hold is refused as invalid. `src: Core features rule 46`
- [ ] `C-CF-156` `constraint` A created product always lands in state `draft`, whatever the request body says. `src: Core features rule 47`
- [ ] `C-CF-157` `constraint` An editor publish is denied as unauthorized, leaving the state unchanged. `src: Core features rule 48`
- [ ] `C-CF-158` `constraint` An editor return to draft is denied as unauthorized, leaving the state unchanged. `src: Core features rule 48`
- [ ] `C-CF-159` `constraint` The app refuses a publish where a required field is empty. `src: Core features rule 49`
- [ ] `C-CF-160` `constraint` The app refuses a publish where the web address is already held. `src: Core features rule 49`
- [ ] `C-CF-161` `constraint` The app refuses a publish where the web address is a reserved segment. `src: Core features rule 49`
- [ ] `C-CF-162` `constraint` The app refuses a publish where the product carries no art piece. `src: Core features rule 49`
- [ ] `C-CF-163` `capability` The required fields are the product name, the web address, the eyebrow, the summary, the claim body. `src: Core features rule 49`
- [ ] `C-CF-164` `capability` A draft may be saved incomplete. `src: Core features rule 49`
- [ ] `C-CF-165` `capability` A draft may be saved with a web address another product already holds. `src: Core features rule 49`
- [ ] `C-CF-166` `literal` The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `datasheet`, `gallery`, `console`, `ask`, `contact`, `privacy`, `terms`, `404`. `src: Core features rule 50`
- [ ] `C-CF-167` `constraint` Exactly one of two simultaneous publishes naming the same web address succeeds. `src: Core features rule 51`
- [ ] `C-CF-168` `capability` The composer fills the web address in from the product name. `src: Core features rule 52`
- [ ] `C-CF-169` `constraint` The composer stops filling the web address once the editor has edited the address by hand. `src: Core features rule 52`
- [ ] `C-CF-170` `literal` The app refuses a product name of one or two characters at save with at publish. `src: Core features rule 53`
- [ ] `C-CF-171` `literal` The app refuses a summary longer than `240` characters. `src: Core features rule 53`
- [ ] `C-CF-172` `capability` An empty product name saves as an incomplete draft, refused only at publish. `src: Core features rule 53`
- [ ] `C-CF-173` `capability` Returning a product to draft asks for confirmation before the change takes effect. `src: Core features rule 54`
- [ ] `C-CF-174` `literal` Only an administrator reads the page-view log at `/desk/views`. `src: Core features rule 55`
- [ ] `C-CF-175` `capability` The views surface shows a count per public route with a list of recent views. `src: Core features rule 55`
- [ ] `C-CF-176` `capability` Signing out of the desk returns the sign-in card. `src: Core features rule 56`
- [ ] `C-CF-177` `constraint` An ended session token is refused afterwards. `src: Core features rule 56`
- [ ] `C-CF-178` `literal` The app serves the privacy page at `/privacy`. `src: Core features rule 57`
- [ ] `C-CF-179` `literal` The app serves the site terms at `/terms`. `src: Core features rule 57`
- [ ] `C-CF-180` `constraint` The footer of every surface reaches the privacy page with the site terms. `src: Core features rule 57`
- [ ] `C-CF-181` `capability` The app renders the not-found surface of the platform for any unmatched path. `src: Core features rule 58`
- [ ] `C-CF-182` `constraint` The not-found surface sits inside the global header with the footer. `src: Core features rule 58`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves `/` with no account. `src: User flow route table`
- [ ] `C-UF-02` `literal` The app serves `/product` with no account. `src: User flow route table`
- [ ] `C-UF-03` `literal` The app serves `/product/{slug}` with no account. `src: User flow route table`
- [ ] `C-UF-04` `literal` The app serves `/family` with no account. `src: User flow route table`
- [ ] `C-UF-05` `literal` The app serves `/family/{slug}` with no account. `src: User flow route table`
- [ ] `C-UF-06` `literal` The app serves `/solution` with no account. `src: User flow route table`
- [ ] `C-UF-07` `literal` The app serves `/datasheet` with no account. `src: User flow route table`
- [ ] `C-UF-08` `literal` The app serves `/gallery` with no account. `src: User flow route table`
- [ ] `C-UF-09` `literal` The app serves `/console` with no account. `src: User flow route table`
- [ ] `C-UF-10` `literal` The app serves `/ask` with no account. `src: User flow route table`
- [ ] `C-UF-11` `literal` The app serves `/contact` with no account. `src: User flow route table`
- [ ] `C-UF-12` `literal` The app serves `/privacy` with no account. `src: User flow route table`
- [ ] `C-UF-13` `literal` The app serves `/terms` with no account. `src: User flow route table`
- [ ] `C-UF-14` `literal` The app serves `/desk/login` with no account. `src: User flow route table`
- [ ] `C-UF-15` `literal` The app serves `/desk` to editor, publisher, administrator. `src: User flow route table`
- [ ] `C-UF-16` `literal` The app serves `/desk/product/new` to editor, publisher, administrator. `src: User flow route table`
- [ ] `C-UF-17` `literal` The app serves `/desk/product/{id}` to editor, publisher, administrator. `src: User flow route table`
- [ ] `C-UF-18` `literal` The app serves `/desk/enquiries` to administrator. `src: User flow route table`
- [ ] `C-UF-19` `literal` The app serves `/desk/views` to administrator. `src: User flow route table`
- [ ] `C-UF-20` `capability` A first-time visitor reads the cookie choice band, pressing `Decline`. `src: User flow journey 1`
- [ ] `C-UF-21` `constraint` After declining, the band is gone on the next public surface with after a reload. `src: User flow journey 1`
- [ ] `C-UF-22` `constraint` After declining, no analytics cookie is set. `src: User flow journey 1`
- [ ] `C-UF-23` `capability` A visitor opening three public routes finds a different page title with a different description on each. `src: User flow journey 2`
- [ ] `C-UF-24` `literal` The product page title carries `Tessera`. `src: User flow journey 2`
- [ ] `C-UF-25` `literal` A visitor writing `amber` into `us-central` then reading from `eu-west` in mode `strong` receives `amber`. `src: User flow journey 3`
- [ ] `C-UF-26` `capability` The console read in journey 3 carries a latency figure with a staleness of `0`. `src: User flow journey 3`
- [ ] `C-UF-27` `literal` A visitor severing `asia-south` is refused a write against that region. `src: User flow journey 4`
- [ ] `C-UF-28` `literal` A write into `eu-west` commits with `asia-south` severed. `src: User flow journey 4`
- [ ] `C-UF-29` `capability` Restoring `asia-south` makes the region rejoin. `src: User flow journey 4`
- [ ] `C-UF-30` `literal` A signed-out visitor opening `/product/halyard` receives the heading `We cannot find that page`. `src: User flow journey 5`
- [ ] `C-UF-31` `constraint` `Halyard` is absent from the product index, the `Networking` family, the art gallery, the header search. `src: User flow journey 5`
- [ ] `C-UF-32` `literal` A visitor reads the eyebrow `Tessera database` on the flagship product route. `src: User flow journey 6`
- [ ] `C-UF-33` `literal` A visitor reads the heading `One database, every region, one truth` on the flagship product route. `src: User flow journey 6`
- [ ] `C-UF-34` `capability` A visitor follows a related card to another published product sharing a family. `src: User flow journey 6`
- [ ] `C-UF-35` `literal` A visitor reads the count line `8 products` on the product index. `src: User flow journey 7`
- [ ] `C-UF-36` `literal` Typing `slip` into the name field leaves `Slipstream` as the only card. `src: User flow journey 7`
- [ ] `C-UF-37` `capability` Choosing the family `Databases`, copying the address, reloading, keeps the family filter applied. `src: User flow journey 8`
- [ ] `C-UF-38` `literal` The sort `Name, A to Z` orders the cards alphabetically. `src: User flow journey 9`
- [ ] `C-UF-39` `literal` The sort `Recently added` puts the newest first. `src: User flow journey 9`
- [ ] `C-UF-40` `literal` Typing `zzzz` shows the empty message with a `Clear filter` control. `src: User flow journey 10`
- [ ] `C-UF-41` `literal` A visitor reads the family name `Databases` with its standfirst on its family route. `src: User flow journey 11`
- [ ] `C-UF-42` `capability` A visitor follows `Families` in the header to the three cards with their published counts. `src: User flow journey 11`
- [ ] `C-UF-43` `literal` Selecting `Telecommunications` swaps the explorer to its proof card with its stat line, its customer. `src: User flow journey 12`
- [ ] `C-UF-44` `literal` A visitor reads the card for `Meridian Platform Overview` with its cover, page count, file size. `src: User flow journey 13`
- [ ] `C-UF-45` `capability` A visitor downloads a datasheet from the library. `src: User flow journey 13`
- [ ] `C-UF-46` `capability` A visitor narrowing the gallery to `Databases` opens one piece, reading its alternative text with the product name. `src: User flow journey 14`
- [ ] `C-UF-47` `literal` A visitor submits the contact form with the region `Europe` with the interest `Evaluation`. `src: User flow journey 15`
- [ ] `C-UF-48` `capability` A visitor reads the success banner with its enquiry identifier. `src: User flow journey 15`
- [ ] `C-UF-49` `literal` An editor signs in as `editor@example.com` with the password `deku-demo-pw-2026`. `src: User flow journey 16`
- [ ] `C-UF-50` `literal` Typing the name `Kestrel` fills the web address in as `kestrel`. `src: User flow journey 16`
- [ ] `C-UF-51` `capability` The editor saves the draft before attaching one art piece with a description. `src: User flow journey 16`
- [ ] `C-UF-52` `constraint` The editor finds no publish control available. `src: User flow journey 16`
- [ ] `C-UF-53` `literal` A publisher signs in as `publisher@example.com`. `src: User flow journey 17`
- [ ] `C-UF-54` `capability` The publisher selects `Kestrel` in the list, reads its detail pane, then presses `Open in composer`. `src: User flow journey 17`
- [ ] `C-UF-55` `capability` Publishing shows the published message exactly as the copy deck states. `src: User flow journey 17`
- [ ] `C-UF-56` `capability` Returning to draft asks for confirmation before the change. `src: User flow journey 17`
- [ ] `C-UF-57` `capability` Returning to draft shows the returned message exactly as the copy deck states. `src: User flow journey 17`
- [ ] `C-UF-58` `literal` An administrator signs in as `administrator@example.com`. `src: User flow journey 18`
- [ ] `C-UF-59` `capability` The administrator reads the submission of journey 15 on the enquiries surface. `src: User flow journey 18`
- [ ] `C-UF-60` `capability` The administrator reads a count for `/product` with the time of a recent view. `src: User flow journey 18`

## C-UX UI and UX notes

- [ ] `C-UX-01` `constraint` The site is fully operable by keyboard with screen reader. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-02` `constraint` Body text with supporting copy meet WCAG AA contrast against their grounds. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-03` `ui` The light cool neutral never carries copy a visitor must read. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-04` `constraint` Every interactive element is reachable in document order. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-05` `constraint` The focus ring is never removed, only restyled. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-06` `constraint` Every navigation target is comfortably sized for a finger. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-07` `constraint` The app carries one `banner`, one `main` per route, one `contentinfo`. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-08` `constraint` The app carries navigation landmarks for the primary nav with the product sub-nav. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-09` `constraint` The app carries one `h1` per route. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-10` `constraint` Headings descend without skipping a level. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-11` `constraint` Every icon-only control carries an accessible name. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-12` `capability` Dialogs with overlays close on Escape. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-13` `capability` A closed dialog returns focus to what opened the dialog. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-14` `capability` A destructive action asks for confirmation before the action takes effect. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-15` `constraint` Every console state pairs its colour with a word. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-16` `ui` Every badge pairs its colour with a word. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-17` `constraint` Under reduced motion, sliding, rotation, auto-advance stop, opacity fades staying but shortening. `src: UI/UX notes, the accessibility paragraph`
- [ ] `C-UX-18` `ui` The platform reads as calm with serious in the first moment. `src: UI/UX notes, the north star paragraph`
- [ ] `C-UX-19` `ui` The platform makes one precise technical claim a visitor can challenge. `src: UI/UX notes, the north star paragraph`
- [ ] `C-UX-20` `ui` A visitor can put the claim to the proof on the page. `src: UI/UX notes, the north star paragraph`
- [ ] `C-UX-21` `constraint` The page ground of every surface is a near-white neutral. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-22` `ui` Section bands sit on a near-white neutral one step below the page ground. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-23` `ui` Inset wells sit one step below the section bands. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-24` `ui` Hairlines with skeletons sit one step below the inset wells. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-25` `ui` Card with control borders are a near-white neutral. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-26` `ui` Body text with headings take a deep neutral. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-27` `ui` Supporting copy, captions, every metadata line a visitor reads take a mid cool neutral. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-28` `ui` Disabled text alone takes the mid cool neutral one step lighter. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-29` `ui` Placeholders take a light cool neutral. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-30` `constraint` The footer with its link columns sits on the page ground like every other surface. `src: UI/UX notes, the palette paragraph`
- [ ] `C-UX-31` `ui` A single mid, vivid blue marks everything a visitor can act on. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-32` `ui` Pressed states, emphasis, pointed-at link text take the mid, vivid blue darker. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-33` `ui` The button hover fill with the chip fill are a near-white cool neutral, selected navigation one step deeper. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-34` `ui` The mid, vivid blue marks everything currently selected. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-35` `ui` Nothing inert wears the mid, vivid blue but the console commit-wait bar. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-36` `ui` No brand hue fills a button. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-37` `ui` No brand hue colours the text of a link. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-38` `ui` The four brand hues appear in the wordmark, the gradient bar, the product marks, the active-label underline. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-39` `ui` Failure takes a mid, vivid red, marking only a refusal. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-40` `ui` A success banner sits on a near-white neutral fill with a mid, soft green left border. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-41` `ui` A failure banner sits on a near-white warm neutral fill, its text in the mid, vivid red. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-42` `ui` Success takes a mid, soft green, marking only a completed action or a good state. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-43` `ui` The mid, vivid orange is the warning accent, marking the `Draft` badge as unfinished. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-44` `constraint` The product commits to the light scheme. `src: UI/UX notes, the action colour paragraph`
- [ ] `C-UX-45` `literal` Display headings, product titles, card titles take the family `Manrope`. `src: UI/UX notes, the type paragraph`
- [ ] `C-UX-46` `literal` Body, navigation, badges, filter controls, metadata take the family `Inter`. `src: UI/UX notes, the type paragraph`
- [ ] `C-UX-47` `constraint` No font file ships with the build. `src: UI/UX notes, the type paragraph`
- [ ] `C-UX-48` `constraint` Type is a humanist geometric sans set calmly. `src: UI/UX notes, the type paragraph`
- [ ] `C-UX-49` `constraint` Cards take one soft product radius, buttons with text fields a tighter one, chips a full pill, icon buttons a circle. `src: UI/UX notes, the shape paragraph`
- [ ] `C-UX-50` `constraint` The largest control group takes the product radius, feature tiles a softer one, filter toggles with the rounded primary button a full pill. `src: UI/UX notes, the shape paragraph`
- [ ] `C-UX-51` `ui` One decorative asymmetric radius appears on the active side-rail item of a product route. `src: UI/UX notes, the shape paragraph`
- [ ] `C-UX-52` `constraint` Density reads as spacious on an eight-step rhythm. `src: UI/UX notes, the density paragraph`
- [ ] `C-UX-53` `ui` Reading columns hold a generous reading measure. `src: UI/UX notes, the density paragraph`
- [ ] `C-UX-54` `constraint` The default gutter with card padding are one step of the rhythm, band separation double. `src: UI/UX notes, the density paragraph`
- [ ] `C-UX-55` `constraint` The fixed header holds a constant height across every route. `src: UI/UX notes, the density paragraph`
- [ ] `C-UX-56` `ui` Bands are separated by air rather than by lines. `src: UI/UX notes, the density paragraph`
- [ ] `C-UX-57` `ui` The change of ground between neighbouring bands is the only separation drawn between them. `src: UI/UX notes, the density paragraph`
- [ ] `C-UX-58` `ui` Nothing is drawn in the seam between two neighbouring bands. `src: UI/UX notes, the density paragraph`
- [ ] `C-UX-59` `ui` The product rail advancing one card is a named moment, eased with brief. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-60` `ui` A band fading in from below as the band enters the viewport is a named moment, eased with brief. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-61` `constraint` The brand gradient turns a half-turn once on load, then holds. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-62` `constraint` Nothing is scroll-scrubbed. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-63` `constraint` The skeleton shimmer is the one animation that loops. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-64` `capability` The mega-menu panel drops open with its chevron turning. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-65` `capability` The console uncertainty band narrows with its commit-wait bar filling. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-66` `constraint` Five easing characters carry the whole product. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-67` `capability` A desk message enters on a short decelerating travel. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-68` `capability` A severed region's links go dashed. `src: UI/UX notes, the motion paragraph`
- [ ] `C-UX-69` `ui` A control shows a resting, a pointed-at, a pressed, a focused, an unavailable state. `src: UI/UX notes, the components paragraph`
- [ ] `C-UX-70` `constraint` A field carries its label above with any failure message directly beneath. `src: UI/UX notes, the components paragraph`
- [ ] `C-UX-71` `ui` Unavailable is signalled by more than colour. `src: UI/UX notes, the components paragraph`
- [ ] `C-UX-72` `ui` A card, a control, a console state each read as finished with nothing in a placeholder look. `src: UI/UX notes, the components paragraph`
- [ ] `C-UX-73` `constraint` The product is responsive across five breakpoints. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-74` `constraint` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-75` `constraint` Every navigation target stays reachable at a narrow viewport. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-76` `constraint` Rows of cards fold to a single column at a narrow viewport. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-77` `ui` At a phone width the product route reads comfortably, nothing crowding the next. `src: UI/UX notes, the responsive paragraph`
- [ ] `C-UX-78` `ui` No surface is dominated by one hue family with no second signal. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-79` `constraint` No band is rendered empty rather than omitted. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-80` `constraint` No spinner stands in for content that is already drawn. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-81` `constraint` No console proof is a colour with no word. `src: UI/UX notes, the design-against-failures paragraph`
- [ ] `C-UX-82` `constraint` No marketing composition stands where the working desk belongs. `src: UI/UX notes, the design-against-failures paragraph`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` Every public route arrives as HTML carrying its content on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-02` `capability` Only the console, the product rail, the industry explorer hydrate on public routes. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The server is `Fastify`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` The client is `SolidStart` in TypeScript. `src: Technical requirements para 1`
- [ ] `C-TR-05` `constraint` The app introduces no second database, cache, queue, object store or search service. `src: Technical requirements para 2`
- [ ] `C-TR-06` `constraint` The app makes no third-party runtime call but the font service. `src: Technical requirements para 2`
- [ ] `C-TR-07` `constraint` The app uses only the libraries named in the brief plus their direct dependencies. `src: Technical requirements para 2`
- [ ] `C-TR-08` `constraint` The app introduces no identity provider or mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-09` `literal` The app reads the `PostgreSQL` connection from `DATABASE_URL`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-10` `literal` The app reads the `MinIO` endpoint from `STORAGE_ENDPOINT`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-11` `literal` The app reads the bucket from `STORAGE_BUCKET`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-12` `literal` The app reads the `MinIO` keys from `STORAGE_ACCESS_KEY` with `STORAGE_SECRET_KEY`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-13` `literal` The app reads the origin from `APP_PUBLIC_URL` with the outside port from `APP_PUBLIC_PORT`. `src: Technical requirements, environment variable table`
- [ ] `C-TR-14` `constraint` The app hardcodes no host. `src: Technical requirements, the running services paragraph`
- [ ] `C-TR-15` `literal` A desk session token expires after `12` hours. `src: Technical requirements, the sessions paragraph`
- [ ] `C-TR-16` `constraint` Passwords are stored hashed. `src: Technical requirements, the sessions paragraph`
- [ ] `C-TR-17` `capability` `POST /api/auth/login` takes an email with a password, answering with a bearer token. `src: Technical requirements, the sessions paragraph`
- [ ] `C-TR-18` `literal` An upload target expires after `15` minutes, scoped to one object key. `src: Technical requirements, the object writes paragraph`
- [ ] `C-TR-19` `literal` The upload answer carries `url`, `method`, `headers`, `object_key`. `src: Technical requirements, the object writes paragraph`
- [ ] `C-TR-20` `capability` The browser puts the bytes at the target; the desk then registers the object key. `src: Technical requirements, the object writes paragraph`
- [ ] `C-TR-21` `literal` The app serves art bytes at `GET /api/media/art/{art_id}`. `src: Technical requirements, the object reads paragraph`
- [ ] `C-TR-22` `literal` The app serves datasheet bytes at `GET /api/media/datasheets/{datasheet_id}`. `src: Technical requirements, the object reads paragraph`
- [ ] `C-TR-23` `constraint` Each media route resolves the owning product state before streaming a byte. `src: Technical requirements, the object reads paragraph`
- [ ] `C-TR-24` `constraint` Saving one product twice creates no second product. `src: Technical requirements, the concurrency paragraph`
- [ ] `C-TR-25` `constraint` A console commit is acknowledged only after its reported uncertainty has passed. `src: Technical requirements, the console paragraph`
- [ ] `C-TR-26` `constraint` A write against a severed region is refused rather than reconciled later. `src: Technical requirements, the console paragraph`
- [ ] `C-TR-27` `literal` The largest home content paints in under `2.5` seconds on a fourth-generation mobile connection. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-28` `literal` An interaction paints its next frame in under `200` milliseconds. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-29` `literal` No surface shifts its layout by more than a tenth of a viewport. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-30` `literal` The compressed JavaScript the home surface delivers stays under `180KB`. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-31` `literal` No more than `3` requests block first paint on the home surface. `src: Technical requirements, the performance paragraph`
- [ ] `C-TR-32` `constraint` The console, the product rail, below-fold generated art are deferred until after first paint. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-33` `constraint` Only the hero mark with the first row of cards loads eagerly. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-34` `constraint` Every image below the fold loads lazily. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-35` `constraint` Every generated image declares its intrinsic width with its height. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-36` `constraint` Every generated image is delivered with a candidate set plus a sizes hint. `src: Technical requirements, the media weight paragraph`
- [ ] `C-TR-37` `literal` `GET /api/health` answers with the body `{"status": "ready"}`. `src: Technical requirements, the health paragraph`
- [ ] `C-TR-38` `constraint` The app logs no credential, no bearer token, no contact submission body. `src: Technical requirements, the health paragraph`
- [ ] `C-TR-39` `contract` The app logs one structured line per request on stdout with the method, the path, the status, the duration. `src: Technical requirements, the health paragraph`
- [ ] `C-TR-40` `capability` The app derives the per-family published count on read. `src: Technical requirements, the derivation paragraph`
- [ ] `C-TR-41` `capability` The app derives the datasheet file size on read. `src: Technical requirements, the derivation paragraph`
- [ ] `C-TR-42` `capability` The app derives the `art_count` on the desk list on read. `src: Technical requirements, the derivation paragraph`
- [ ] `C-TR-43` `capability` The app derives a console read staleness with latency on read. `src: Technical requirements, the derivation paragraph`
- [ ] `C-TR-44` `capability` The app derives the per-route view count on read. `src: Technical requirements, the derivation paragraph`
- [ ] `C-TR-45` `constraint` Restarting the app duplicates no row. `src: Technical requirements, the derivation paragraph`

## C-DM Data model

- [ ] `C-DM-01` `data` The app carries thirteen tables with every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-02` `data` The app carries `id`, `email`, `password_hash`, `role`, `created_at` on an account. `src: Data model, the accounts paragraph`
- [ ] `C-DM-03` `data` The app carries `account_id`, `token_hash`, `expires_at`, `ended_at` on a session. `src: Data model, the sessions paragraph`
- [ ] `C-DM-04` `data` An account `role` is `editor`, `publisher` or `administrator`. `src: Data model, the accounts paragraph`
- [ ] `C-DM-05` `data` The app carries `eyebrow`, `heading`, `lead`, `summary`, `claim_body` on a product. `src: Data model, the products paragraph`
- [ ] `C-DM-06` `data` The app carries `state` on a product, `draft` or `published` in lowercase. `src: Data model, the products paragraph`
- [ ] `C-DM-07` `data` The app carries `families`, `featured`, `sort_index` on a product. `src: Data model, the products paragraph`
- [ ] `C-DM-08` `data` The app carries `service_level`, `regions_available`, `created_at`, `updated_at` on a product. `src: Data model, the products paragraph`
- [ ] `C-DM-09` `data` A product `slug` is unique among published products. `src: Data model, the products paragraph`
- [ ] `C-DM-10` `data` The three families are seeded, never written from the desk. `src: Data model, the families paragraph`
- [ ] `C-DM-11` `data` The app carries `line`, `sort_index` on a highlight, one claim band per line. `src: Data model, the highlights paragraph`
- [ ] `C-DM-12` `data` The app carries `object_key`, `alt_text`, `seed`, `width`, `height` on an art piece. `src: Data model, the art paragraph`
- [ ] `C-DM-13` `data` The app leaves `product_id` null on a platform datasheet. `src: Data model, the datasheets paragraph`
- [ ] `C-DM-14` `data` A datasheet stores its `page_count`, read from the document at registration or seed, never its byte size. `src: Data model, the datasheets paragraph`
- [ ] `C-DM-15` `data` The app carries `region`, `key`, `value`, `commit_timestamp`, `uncertainty_ms` on a console write. `src: Data model, the console paragraph`
- [ ] `C-DM-16` `data` The app carries `region`, `severed` on a partition row. `src: Data model, the console paragraph`
- [ ] `C-DM-17` `data` The app carries `name`, `work_email`, `company`, `region`, `interest`, `message`, `received_at` on an enquiry. `src: Data model, the enquiries paragraph`
- [ ] `C-DM-18` `data` The app carries `route`, `viewed_at` on a page view. `src: Data model, the page views paragraph`
- [ ] `C-DM-19` `literal` The seeded families carry the standfirsts from the family table. `src: Data model, the family table`
- [ ] `C-DM-20` `literal` The seeded families carry the intros from the family table. `src: Data model, the family table`
- [ ] `C-DM-21` `literal` The app stores an art piece under `products/<product_id>/art/<sha256_of_bytes>.<ext>`. `src: Data model, the object key table`
- [ ] `C-DM-22` `literal` The app stores a product datasheet under `products/<product_id>/datasheet/<sha256_of_bytes>.pdf`. `src: Data model, the object key table`
- [ ] `C-DM-23` `literal` The app stores a platform datasheet under `platform/<datasheet_id>/<sha256_of_bytes>.pdf`. `src: Data model, the object key table`
- [ ] `C-DM-24` `literal` The seed holds nine products, eight `published` with one `draft`. `src: Data model, the seed table`
- [ ] `C-DM-25` `literal` The seeded products are created in `sort_index` order, the most recent being `Halyard`, then `Foundry`. `src: Data model, the seed table`
- [ ] `C-DM-26` `literal` The seed gives `Databases` 4 published products, `Networking` 3, `Analytics` 3. `src: Data model, the seed table`
- [ ] `C-DM-27` `literal` Each seeded art piece takes the product slug plus its sort index as its `seed`, like `tessera-1`. `src: Data model, the seeded art paragraph`
- [ ] `C-DM-28` `literal` Each seeded art piece is drawn at `1200` by `900`. `src: Data model, the seeded art paragraph`
- [ ] `C-DM-29` `literal` Each seeded art piece carries the alternative text `<product name> card art, generated field <sort index> of <art count>`. `src: Data model, the seeded art paragraph`
- [ ] `C-DM-30` `literal` The first `Tessera` art piece reads `Tessera card art, generated field 1 of 3`. `src: Data model, the seeded art paragraph`
- [ ] `C-DM-31` `literal` `Tessera` carries the lead `A fully managed relational database with strong consistency across regions, backed by synchronized clocks.` `src: Data model, the Tessera paragraph`
- [ ] `C-DM-32` `literal` `Tessera` carries the service level `99.999%` with `5` regions available. `src: Data model, the Tessera paragraph`
- [ ] `C-DM-33` `literal` Every seeded product other than `Tessera` carries its own name as its heading. `src: Data model, the Tessera paragraph`
- [ ] `C-DM-34` `literal` The app seeds the platform datasheets `Meridian Platform Overview`, `The Global Network`, `Consistency Explained`. `src: Data model, the seed paragraph`
- [ ] `C-DM-35` `literal` The app seeds the five console regions unsevered. `src: Data model, the seed paragraph`
- [ ] `C-DM-36` `literal` The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Bank`, `Truenorth`, `Stonecraft`, `Threadly`, `Marea Global`, `The Gazette`. `src: Data model, the customer paragraph`
- [ ] `C-DM-37` `literal` The testimonial is attributed to `Anjali Rao`, `SVP of Engineering for Network Automation`, `Harrowgate`. `src: Data model, the testimonial paragraph`
- [ ] `C-DM-38` `literal` The testimonial card carries its quote exactly as the testimonial paragraph states. `src: Data model, the testimonial paragraph`
- [ ] `C-DM-39` `literal` The app seeds `Tessera` at `tessera` as `published` in Databases, featured, sort index `1`, with `3` art pieces, with the datasheet `Tessera Technical Overview`. `src: Data model, the seed table`
- [ ] `C-DM-40` `literal` The app seeds `Slipstream` at `slipstream` as `published` in Networking, featured, sort index `2`, with `2` art pieces. `src: Data model, the seed table`
- [ ] `C-DM-41` `literal` The app seeds `Beacon Enterprise` at `beacon-enterprise` as `published` in Analytics, featured, sort index `3`, with `2` art pieces. `src: Data model, the seed table`
- [ ] `C-DM-42` `literal` The app seeds `Quarry` at `quarry` as `published` in Databases, Analytics, featured, sort index `4`, with `2` art pieces. `src: Data model, the seed table`
- [ ] `C-DM-43` `literal` The app seeds `Bastion` at `bastion` as `published` in Networking, featured, sort index `5`, with `2` art pieces. `src: Data model, the seed table`
- [ ] `C-DM-44` `literal` The app seeds `Anvil` at `anvil` as `published` in Networking, Databases, featured, sort index `6`, with `2` art pieces. `src: Data model, the seed table`
- [ ] `C-DM-45` `literal` The app seeds `Lattice` at `lattice` as `published` in Analytics, not featured, sort index `7`, with `2` art pieces. `src: Data model, the seed table`
- [ ] `C-DM-46` `literal` The app seeds `Foundry` at `foundry` as `published` in Databases, not featured, sort index `8`, with `2` art pieces. `src: Data model, the seed table`
- [ ] `C-DM-47` `literal` The app seeds `Halyard` at `halyard` as `draft` in Networking, not featured, sort index `9`, with `3` art pieces, with the datasheet `Halyard Technical Overview`. `src: Data model, the seed table`
- [ ] `C-DM-48` `literal` `Tessera` carries the highlight line `Reads always reflect the latest write` at sort index `1`. `src: Data model, the highlight table`
- [ ] `C-DM-49` `literal` `Tessera` carries its highlight line at sort index `2` exactly as the table states. `src: Data model, the highlight table`
- [ ] `C-DM-50` `literal` `Tessera` carries the highlight line `Correct through network partitions, never corrupted` at sort index `3`. `src: Data model, the highlight table`
- [ ] `C-DM-51` `literal` `Tessera` carries the highlight line `Massive transaction scale with no consistency trade` at sort index `4`. `src: Data model, the highlight table`
- [ ] `C-DM-52` `literal` `Tessera` carries the highlight line `Synchronous multi-region replication` at sort index `5`. `src: Data model, the highlight table`
- [ ] `C-DM-53` `literal` `Tessera` carries its highlight line at sort index `6` exactly as the table states. `src: Data model, the highlight table`
- [ ] `C-DM-54` `literal` `Tessera` carries the highlight line `Automatic failover with zero data loss` at sort index `7`. `src: Data model, the highlight table`
- [ ] `C-DM-55` `literal` `Tessera` carries the highlight line `Five-nines availability, multi-region` at sort index `8`. `src: Data model, the highlight table`
- [ ] `C-DM-56` `literal` The app seeds the industry `Retail` at `retail` with the customer `Vessel Foods`. `src: Data model, the industry table`
- [ ] `C-DM-57` `literal` The industry `Retail` carries the stat line `9 of the top 10 retail companies build on Meridian Cloud`. `src: Data model, the industry table`
- [ ] `C-DM-58` `literal` The app seeds the industry `Financial services` at `financial-services` with the customer `Cobalt Bank`. `src: Data model, the industry table`
- [ ] `C-DM-59` `literal` The industry `Financial services` carries the stat line `Nearly 90% of the largest global banks run regulated workloads here`. `src: Data model, the industry table`
- [ ] `C-DM-60` `literal` The app seeds the industry `Healthcare` at `healthcare` with the customer `Truenorth`. `src: Data model, the industry table`
- [ ] `C-DM-61` `literal` The industry `Healthcare` carries the stat line `Clinical records stay in region, with one consistent read`. `src: Data model, the industry table`
- [ ] `C-DM-62` `literal` The app seeds the industry `Telecommunications` at `telecommunications` with the customer `Harrowgate`. `src: Data model, the industry table`
- [ ] `C-DM-63` `literal` The industry `Telecommunications` carries the stat line `Issue resolution cut from hours to minutes across a national network`. `src: Data model, the industry table`
- [ ] `C-DM-64` `literal` The app seeds the industry `Government` at `government` with the customer `Marea Global`. `src: Data model, the industry table`
- [ ] `C-DM-65` `literal` The industry `Government` carries the stat line `Residency guarantees met in 5 regions at once`. `src: Data model, the industry table`
- [ ] `C-DM-66` `literal` The app seeds the industry `Manufacturing` at `manufacturing` with the customer `Stonecraft`. `src: Data model, the industry table`
- [ ] `C-DM-67` `literal` The industry `Manufacturing` carries the stat line `Plant telemetry at 1 million writes a second, ordered globally`. `src: Data model, the industry table`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` The body step is `16px` over `24px` at `400`. `src: Front-end specification, type scale`
- [ ] `C-FE-02` `literal` The body-medium step is `16px` over `24px` at `500`. `src: Front-end specification, type scale`
- [ ] `C-FE-03` `literal` The body-tall step is `16px` over `26px` at `500`. `src: Front-end specification, type scale`
- [ ] `C-FE-04` `literal` The small step is `14px` over `24px` at `400`. `src: Front-end specification, type scale`
- [ ] `C-FE-05` `literal` The dense step is `13px` over `24px` at `400`. `src: Front-end specification, type scale`
- [ ] `C-FE-06` `literal` The lead step is `18px` over `28px` at `400`. `src: Front-end specification, type scale`
- [ ] `C-FE-07` `literal` The title step is `20px` over `28px` at `500`. `src: Front-end specification, type scale`
- [ ] `C-FE-08` `literal` The heading step is `24px` over `32px` at `500`. `src: Front-end specification, type scale`
- [ ] `C-FE-09` `literal` The display step is `28px` over `36px` at `400`. `src: Front-end specification, type scale`
- [ ] `C-FE-10` `literal` The micro step is `12px` over `16px` at `400`. `src: Front-end specification, type scale`
- [ ] `C-FE-11` `literal` The button step is `14px` over `36px` at `500`. `src: Front-end specification, type scale`
- [ ] `C-FE-12` `literal` `Manrope` carries the display, heading, title steps. `src: Front-end specification, type scale`
- [ ] `C-FE-13` `literal` `Inter` carries every other type step. `src: Front-end specification, type scale`
- [ ] `C-FE-14` `literal` Both families are declared against the fallback stack `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`. `src: Front-end specification, type scale`
- [ ] `C-FE-15` `capability` Every route declares its shell as a page-type attribute. `src: Front-end specification, information architecture`
- [ ] `C-FE-16` `literal` The `landing` shell is full-width bands with no side rail, used by the home route alone. `src: Front-end specification, information architecture`
- [ ] `C-FE-17` `literal` The `product` shell is a left sticky sub-nav with a right highlights rail, used by every product route. `src: Front-end specification, information architecture`
- [ ] `C-FE-18` `literal` The `tool` shell is a centred single-purpose surface, used by the console with the assistant. `src: Front-end specification, information architecture`
- [ ] `C-FE-19` `literal` The `index` shell is a filterable card grid, used by the five index surfaces. `src: Front-end specification, information architecture`
- [ ] `C-FE-20` `constraint` No route invents a layout of its own. `src: Front-end specification, information architecture`
- [ ] `C-FE-21` `constraint` Scaling is in fixed steps rather than viewport-derived units. `src: Front-end specification, scaling, typography and the effects vocabulary`
- [ ] `C-FE-22` `constraint` The body root is a fixed size. `src: Front-end specification, scaling, typography and the effects vocabulary`
- [ ] `C-FE-23` `constraint` No type step is invented outside the eleven. `src: Front-end specification, scaling, typography and the effects vocabulary`
- [ ] `C-FE-24` `constraint` A resting card draws no shadow, only its hairline border. `src: Front-end specification, scaling, typography and the effects vocabulary`
- [ ] `C-FE-25` `constraint` The effects vocabulary is seven entries, the skeleton shimmer with the focus ring among them, nothing outside drawn. `src: Front-end specification, scaling, typography and the effects vocabulary`
- [ ] `C-FE-26` `capability` The edge-fade mask softens the product rail with the customer wall at both ends. `src: Front-end specification, scaling, typography and the effects vocabulary`
- [ ] `C-FE-27` `capability` A dropdown panel casts a deeper two-part shadow. `src: Front-end specification, elevation`
- [ ] `C-FE-28` `literal` Body text with supporting copy meet a contrast of at least `4.5` to 1. `src: Front-end specification, accessibility values`
- [ ] `C-FE-29` `literal` A navigation target is at least `44` by `44` on its shorter side. `src: Front-end specification, accessibility values`
- [ ] `C-FE-30` `literal` The first focusable element on every route is a `Skip to content` link into the `main` landmark. `src: Front-end specification, accessibility values`
- [ ] `C-FE-31` `literal` Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-32` `literal` The grid is `twelve` columns, capping at a maximum width. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-33` `literal` The product grid is three across at `xl`, two at `md`, one below. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-34` `literal` The family index is three in a row at `lg`, stacked below `md`. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-35` `literal` The datasheet library is four across at `xl`, three at `lg`, two at `md`, one below. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-36` `literal` The gallery masonry runs one column below `md`, two at `md`, three at `lg`, four at `xl`. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-37` `literal` The industry grid is three at `lg`, two at `md`, one below. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-38` `literal` The product rail shows one card with part of the next below `md`, three at `lg` with above. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-39` `constraint` The primary navigation collapses into a drawer below `md`. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-40` `constraint` Below `lg` a product route sub-nav becomes a dropdown with the highlights rail inline below the hero. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-41` `ui` Below `md` the console stacks its four parts vertically with shortened region labels. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-42` `constraint` Below `md` the ask bar docks full-width above the footer. `src: Front-end specification, layout and breakpoints`
- [ ] `C-FE-43` `constraint` The dialog layer, holding the search overlay, the confirmation, the message stack, sits in front of everything. `src: Front-end specification, elevation`
- [ ] `C-FE-44` `constraint` The cookie band sits above the header in the stacking order. `src: Front-end specification, elevation`
- [ ] `C-FE-45` `constraint` The layers run from the back: page flow, sticky sub-nav, in-page rails, the ask bar, dropdowns, the header, the cookie band, the dialog layer. `src: Front-end specification, elevation`
- [ ] `C-FE-46` `ui` A hovered card with a hovered button raise on a soft two-part shadow. `src: Front-end specification, elevation`
- [ ] `C-FE-47` `constraint` The focus ring is a solid ring in the mid, vivid blue. `src: Front-end specification, elevation`
- [ ] `C-FE-48` `capability` The header is a fixed bar spanning the full width on the page ground. `src: Front-end specification, chrome`
- [ ] `C-FE-49` `capability` The header carries a hairline bottom border, a label warming to the mid, vivid blue when pointed at. `src: Front-end specification, chrome`
- [ ] `C-FE-50` `capability` The wordmark carries the four brand hues letter by letter. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-51` `literal` The wordmark reads `Meridian` plus `Cloud`, linking to the home route. `src: Front-end specification, chrome`
- [ ] `C-FE-52` `capability` Each primary navigation label opens its matching public route. `src: Front-end specification, chrome`
- [ ] `C-FE-53` `capability` The header right cluster holds a search control with a filled `Start free` button opening the contact form. `src: Front-end specification, chrome`
- [ ] `C-FE-54` `capability` `Products` opens a full-width mega-menu grouping the published products by family. `src: Front-end specification, chrome`
- [ ] `C-FE-55` `capability` Escape closes the mega-menu. `src: Front-end specification, chrome`
- [ ] `C-FE-56` `constraint` Only one mega-menu panel is open at a time. `src: Front-end specification, chrome`
- [ ] `C-FE-57` `capability` Below `md` the drawer slides in from the left over a dimmed backdrop. `src: Front-end specification, chrome`
- [ ] `C-FE-58` `capability` Each drawer item is a row with a trailing arrow, `Start free` pinned to the panel foot, a close control dismissing the drawer. `src: Front-end specification, chrome`
- [ ] `C-FE-59` `capability` The search overlay filters the published products by name. `src: Front-end specification, chrome`
- [ ] `C-FE-60` `capability` Escape or a press on the scrim closes the search overlay, focus trapped until then. `src: Front-end specification, chrome`
- [ ] `C-FE-61` `capability` Submitting the ask bar opens the assistant with the query prefilled. `src: Front-end specification, chrome`
- [ ] `C-FE-62` `capability` A rounded-pill ask bar is fixed near the foot of the viewport on the home with product routes. `src: Front-end specification, chrome`
- [ ] `C-FE-63` `capability` The footer column headings open their public routes. `src: Front-end specification, chrome`
- [ ] `C-FE-64` `capability` The footer baseline links open the privacy page with the site terms. `src: Front-end specification, chrome`
- [ ] `C-FE-65` `capability` The cookie band stands only until the visitor chooses. `src: Front-end specification, chrome`
- [ ] `C-FE-66` `ui` The cookie band never covers the primary action of the surface behind the band. `src: Front-end specification, chrome`
- [ ] `C-FE-67` `literal` Every public route title is the surface name followed by `- Meridian Cloud`. `src: Front-end specification, chrome`
- [ ] `C-FE-68` `capability` The home bands run hero, product rail, console, industry explorer, customer proof, closing band, footer. `src: Front-end specification, home`
- [ ] `C-FE-69` `ui` The rail, the explorer, the closing band sit on the section ground. `src: Front-end specification, home`
- [ ] `C-FE-70` `ui` The hero is one centred group with generous top space. `src: Front-end specification, home`
- [ ] `C-FE-71` `capability` The hero controls `Get started for free` with `Contact sales` both open the contact form. `src: Front-end specification, home`
- [ ] `C-FE-72` `capability` The gradient product mark sits above the home display heading. `src: Front-end specification, home`
- [ ] `C-FE-73` `capability` The hero pill link opens the assistant surface. `src: Front-end specification, home`
- [ ] `C-FE-74` `capability` The product rail advances one card on a timer, paged by a previous with a next control. `src: Front-end specification, home`
- [ ] `C-FE-75` `capability` Selecting a rail card opens its product route, the first being `Tessera`. `src: Front-end specification, home`
- [ ] `C-FE-76` `capability` Each rail card carries an eyebrow, a title line, generated art. `src: Front-end specification, home`
- [ ] `C-FE-77` `ui` Each rail card is a deep neutral fill with near-white text over its art, the band on the section ground. `src: Front-end specification, home`
- [ ] `C-FE-78` `constraint` The rail shows only published products carrying the `featured` flag, ordered by sort index. `src: Front-end specification, home`
- [ ] `C-FE-79` `constraint` The rail pads nothing where fewer products are flagged. `src: Front-end specification, home`
- [ ] `C-FE-80` `constraint` The whole rail band is omitted where no product is flagged. `src: Front-end specification, home`
- [ ] `C-FE-81` `ui` The industry explorer keeps the six industries listed beside the proof panel. `src: Front-end specification, home`
- [ ] `C-FE-82` `literal` `Retail` is the industry selected on arrival. `src: Front-end specification, home`
- [ ] `C-FE-83` `capability` The closing band controls both open the contact form. `src: Front-end specification, home`
- [ ] `C-FE-84` `capability` The customer proof is an edge-faded wall of eight wordmark tiles beside the testimonial card. `src: Front-end specification, home`
- [ ] `C-FE-85` `literal` The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `Scale`, `Replication`, `Read modes`, `Failover`, `Service levels`. `src: Front-end specification, product route`
- [ ] `C-FE-86` `capability` Selecting a sub-nav item scrolls to that band. `src: Front-end specification, product route`
- [ ] `C-FE-87` `capability` A dismissible promo banner above the hero links to the console. `src: Front-end specification, product route`
- [ ] `C-FE-88` `capability` The product hero carries a console link opening the console. `src: Front-end specification, product route`
- [ ] `C-FE-89` `capability` A claim band console link opens the console with a region pair prefilled. `src: Front-end specification, product route`
- [ ] `C-FE-90` `capability` The highlights rail lists the highlight lines as jump links. `src: Front-end specification, product route`
- [ ] `C-FE-91` `capability` One claim band stands per highlight line, in sort order. `src: Front-end specification, product route`
- [ ] `C-FE-92` `ui` Each claim band states its capability as a claim a buyer could challenge. `src: Front-end specification, product route`
- [ ] `C-FE-93` `capability` The `Tessera` bands cover consistency, clock ordering, partitions, scale with sharding, replication, read staleness, failover, availability. `src: Front-end specification, product route`
- [ ] `C-FE-94` `capability` Selecting an art piece opens the piece with its alternative text plus the product name. `src: Front-end specification, product route`
- [ ] `C-FE-95` `constraint` A datasheet card carries its cover in a three-by-four aspect ratio. `src: Front-end specification, product route`
- [ ] `C-FE-96` `capability` The related row sits under its heading with up to three cards sharing a family. `src: Front-end specification, product route`
- [ ] `C-FE-97` `capability` A family page carries a head still, the family name, its standfirst, its intro, its products. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-98` `capability` The product index filter bar is sticky, holding the name field, the family selector, the sort selector. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-99` `capability` The solution index filters its six cards by chips. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-100` `capability` The product index, family index, solution index, datasheet library, gallery each carry a breadcrumb. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-101` `constraint` The composer offers no field for a datasheet cover. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-102` `capability` The gallery masonry keeps each piece's own aspect ratio. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-103` `constraint` Pressing the gallery more control adds pieces without moving those already drawn or the footer. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-104` `capability` The gallery lightbox carries the product name, the alternative text, a link to the product. `src: Front-end specification, family, solution, datasheet and gallery surfaces`
- [ ] `C-FE-105` `capability` The console carries four parts, the region globe among them, with a throughput meter along the foot. `src: Front-end specification, the consistency console`
- [ ] `C-FE-106` `capability` The region map draws the five region nodes as discs joined by thin links. `src: Front-end specification, the consistency console`
- [ ] `C-FE-107` `capability` Writing commits the value, flashing the committed state with a checkmark. `src: Front-end specification, the consistency console`
- [ ] `C-FE-108` `capability` Both console groups work from the keyboard with the same outcomes as a pointer. `src: Front-end specification, the consistency console`
- [ ] `C-FE-109` `capability` The clock readout shows each region clock as an uncertainty band rather than a single instant. `src: Front-end specification, the consistency console`
- [ ] `C-FE-110` `capability` A committed write shows a commit-wait equal to the uncertainty band before acknowledging. `src: Front-end specification, the consistency console`
- [ ] `C-FE-111` `capability` On cut, a severed node greys with its links drawn dashed. `src: Front-end specification, the consistency console`
- [ ] `C-FE-112` `capability` A refused write shows the status circle with the refusal caption. `src: Front-end specification, the consistency console`
- [ ] `C-FE-113` `capability` Restoring the link shows the skeleton shimmer briefly before the region rejoins. `src: Front-end specification, the consistency console`
- [ ] `C-FE-114` `capability` The throughput meter shows transactions a second rising with the consistency tick holding. `src: Front-end specification, the consistency console`
- [ ] `C-FE-115` `ui` Under reduced motion the console becomes a still labelled diagram with a one-line caption under each part. `src: Front-end specification, the consistency console`
- [ ] `C-FE-116` `constraint` Every console control carries an accessible name. `src: Front-end specification, the consistency console`
- [ ] `C-FE-117` `constraint` With no scripting, the console becomes the same still labelled diagram, every control still present. `src: Front-end specification, the consistency console`
- [ ] `C-FE-118` `constraint` A request for reduced motion disables movement everywhere, the console still usable. `src: Front-end specification, the consistency console`
- [ ] `C-FE-119` `literal` The assistant greeting sits at the `heading` step. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-120` `capability` The assistant carries four suggestion pills. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-121` `literal` The first assistant suggestion reads `How can I try Meridian Cloud products for free?` `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-122` `literal` The second assistant suggestion reads `How do I evaluate Tessera?` `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-123` `literal` The third assistant suggestion reads `Discover solutions for my industry`. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-124` `literal` The fourth assistant suggestion reads `Summarize what is new`. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-125` `capability` The contact form fields carry their labels above with any failure message beneath. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-126` `capability` The contact success banner shows the enquiry identifier. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-127` `literal` The contact form fields read `Full name`, `Work email`, `Company`, `Region`, `Interest`, `Message`. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-128` `capability` The privacy page states the platform records a page view per route with its time, plus a contact submission, nothing else. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-129` `capability` The privacy page states the page-view log sets no cookie, the cookie choice governing cookies alone. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-130` `capability` The not-found surface carries a control back to the home route. `src: Front-end specification, assistant, contact and standing surfaces`
- [ ] `C-FE-131` `capability` A failed sign-in nudges the card once, turning its border the failure red. `src: Front-end specification, the desk`
- [ ] `C-FE-132` `literal` The desk sign-in fields read `Email` with `Password`. `src: Front-end specification, the desk`
- [ ] `C-FE-133` `capability` Every signed-in desk page carries a left sidebar holding `Products`, `Sign out` at its foot. `src: Front-end specification, the desk`
- [ ] `C-FE-134` `capability` The desk sidebar shows `Evaluation requests` with `Page views` to an administrator only. `src: Front-end specification, the desk`
- [ ] `C-FE-135` `capability` The product list carries three filter controls each with a count, a new control, the table beside a detail pane. `src: Front-end specification, the desk`
- [ ] `C-FE-136` `literal` The desk table columns read `Name`, `Families`, `State`, `Art`, `Last edited`. `src: Front-end specification, the desk`
- [ ] `C-FE-137` `ui` Selecting a row marks the row, filling the pane with its name, badge, summary, art. `src: Front-end specification, the desk`
- [ ] `C-FE-138` `ui` The table stays in view beside the filled detail pane. `src: Front-end specification, the desk`
- [ ] `C-FE-139` `constraint` Below `lg` the detail pane stacks under the table. `src: Front-end specification, the desk`
- [ ] `C-FE-140` `literal` A `Live` badge sets its word in a deep neutral on the mid, soft green. `src: Front-end specification, the desk`
- [ ] `C-FE-141` `literal` A `Draft` badge sets its word in a deep neutral on the mid, vivid orange. `src: Front-end specification, the desk`
- [ ] `C-FE-142` `capability` The composer is drawn from the public design system. `src: Front-end specification, the desk`
- [ ] `C-FE-143` `literal` The first six composer fields read `Product name`, `Web address`, `Eyebrow`, `Summary`, `Claim body`, `Families, up to three`. `src: Front-end specification, the desk`
- [ ] `C-FE-144` `literal` The last six composer fields read `Show on the front page`, `Service level`, `Regions available`, `Highlight lines`, `Art`, `Datasheet`. `src: Front-end specification, the desk`
- [ ] `C-FE-145` `capability` The art field shows how far each attached upload has got. `src: Front-end specification, the desk`
- [ ] `C-FE-146` `capability` The publish with return-to-draft controls show only to a publisher or an administrator. `src: Front-end specification, the desk`
- [ ] `C-FE-147` `capability` Return to draft opens a confirmation dialog with a cancel control. `src: Front-end specification, the desk`
- [ ] `C-FE-148` `capability` The enquiries surface lists stored submissions newest first with name, company, region, interest, arrival. `src: Front-end specification, the desk`
- [ ] `C-FE-149` `capability` The views surface shows a count per route ordered by count descending, with a list of recent views. `src: Front-end specification, the desk`
- [ ] `C-FE-150` `capability` An editor action is answered by a toast message in a corner of the desk. `src: Front-end specification, the desk`
- [ ] `C-FE-151` `literal` A desk message dismisses after `five` seconds or on press. `src: Front-end specification, the desk`
- [ ] `C-FE-152` `literal` The desk message stack holds at most `three`, a fourth displacing the oldest. `src: Front-end specification, the desk`
- [ ] `C-FE-153` `constraint` Nothing on the public side raises a desk message. `src: Front-end specification, the desk`
- [ ] `C-FE-154` `literal` The iconography is `eleven` marks drawn from coordinates in the build. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-155` `capability` Each utility mark takes the colour of the text around the mark. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-156` `constraint` The eleven marks: wordmark, chevron, arrow-forward, play triangle, status circle, checkmark, search glyph, diamond, product mark, send glyph, globe. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-157` `ui` The diamond mark takes the mid, vivid orange; the gradient product mark carries the brand gradient. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-158` `ui` Secondary emphasis takes the mid, vivid blue one step darker than the primary. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-159` `ui` The testimonial attribution takes a deep neutral one step lighter than headings. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-160` `ui` The console confirmed-write state takes the mid, soft green darker. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-161` `ui` A rare category chip takes a near-white cool neutral with a violet cast. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-162` `ui` Secondary dividers take a light cool neutral one step deeper than a hairline. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-163` `constraint` Motion comes in three kinds of moment: a quick change on point, focus or open; an entrance or a loop; the reveal-on-enter fade. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-164` `constraint` Scroll position drives nothing but the fade in from below. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-165` `constraint` The named keyframes are the fade in from below, the rail slide, the gradient half-turn, the skeleton shimmer, the badge grow, the focus grow. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-166` `constraint` No captured scroll depth is re-enacted. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-167` `constraint` Product card art is a seeded generated field. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-168` `constraint` Customer logos with category logos are wordmark tiles set in type. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-169` `capability` A testimonial portrait, where one exists, is a generated monogram disc rather than a photograph. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-170` `constraint` Diagrams are drawn in the build. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-171` `constraint` Nothing generated stands in for a claim; a diagram shows how the console works, never a figure the console did not produce. `src: Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide`
- [ ] `C-FE-172` `ui` Every card, chip, field, badge keeps one look on every surface where the element appears. `src: Front-end specification, components`
- [ ] `C-FE-173` `constraint` No photograph, film, icon file, font file or compressed texture ships with the build. `src: Front-end specification, media system`
- [ ] `C-FE-174` `constraint` The same product always produces the same art. `src: Front-end specification, media system`
- [ ] `C-FE-175` `constraint` Every generated image loads behind a placeholder ground from its own average colour. `src: Front-end specification, media system`
- [ ] `C-FE-176` `capability` A generated datasheet carries a cover with the product name, a contents page, one page per highlight line. `src: Front-end specification, media system`
- [ ] `C-FE-177` `literal` The header primary control reads `Start free`. `src: Front-end specification, copy`
- [ ] `C-FE-178` `literal` The skip link reads `Skip to content`. `src: Front-end specification, copy`
- [ ] `C-FE-179` `literal` The home heading reads `The new way to cloud with Meridian`. `src: Front-end specification, copy`
- [ ] `C-FE-180` `literal` The home lead string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-181` `literal` The home primary control reads `Get started for free`. `src: Front-end specification, copy`
- [ ] `C-FE-182` `literal` The home outline control reads `Contact sales`. `src: Front-end specification, copy`
- [ ] `C-FE-183` `literal` The home assistant pill reads `Try Beacon Enterprise, the front door to AI for every employee`. `src: Front-end specification, copy`
- [ ] `C-FE-184` `literal` The rail heading reads `Products that hold their promises`. `src: Front-end specification, copy`
- [ ] `C-FE-185` `literal` The explorer heading reads `Solutions for your industry`. `src: Front-end specification, copy`
- [ ] `C-FE-186` `literal` The proof heading reads `Teams that build here`. `src: Front-end specification, copy`
- [ ] `C-FE-187` `literal` The closing heading reads `Start your evaluation`. `src: Front-end specification, copy`
- [ ] `C-FE-188` `literal` The ask bar placeholder reads `Ask anything about Meridian Cloud`. `src: Front-end specification, copy`
- [ ] `C-FE-189` `literal` The cookie band body reads `We use cookies to measure how the site is used.` `src: Front-end specification, copy`
- [ ] `C-FE-190` `literal` The product index heading reads `Every product on the platform`. `src: Front-end specification, copy`
- [ ] `C-FE-191` `literal` The product index name field reads `Filter by name`. `src: Front-end specification, copy`
- [ ] `C-FE-192` `literal` The product index empty reads `Nothing matches that. Try a different family, or clear the filter.` `src: Front-end specification, copy`
- [ ] `C-FE-193` `literal` The product index empty control reads `Clear filter`. `src: Front-end specification, copy`
- [ ] `C-FE-194` `literal` The product console link string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-195` `literal` The related row heading reads `Related products`. `src: Front-end specification, copy`
- [ ] `C-FE-196` `literal` The family index heading reads `Three ways into the platform`. `src: Front-end specification, copy`
- [ ] `C-FE-197` `literal` The family empty string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-198` `literal` The solution index heading reads `Solutions by industry`. `src: Front-end specification, copy`
- [ ] `C-FE-199` `literal` The solution filter chip reads `All`. `src: Front-end specification, copy`
- [ ] `C-FE-200` `literal` The datasheet library heading reads `Datasheets to download`. `src: Front-end specification, copy`
- [ ] `C-FE-201` `literal` The gallery heading reads `Every product, drawn`. `src: Front-end specification, copy`
- [ ] `C-FE-202` `literal` The gallery lightbox link string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-203` `literal` The gallery more control reads `Show more`. `src: Front-end specification, copy`
- [ ] `C-FE-204` `literal` The console refusal string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-205` `literal` The assistant greeting reads `Hello, how can I help?` `src: Front-end specification, copy`
- [ ] `C-FE-206` `literal` The assistant counter reads `0 of 500 characters entered`. `src: Front-end specification, copy`
- [ ] `C-FE-207` `literal` The assistant caption reads `Built with Beacon Enterprise`. `src: Front-end specification, copy`
- [ ] `C-FE-208` `literal` The contact submit reads `Contact sales`. `src: Front-end specification, copy`
- [ ] `C-FE-209` `literal` The contact success reads `Thank you. Your evaluation request is with us.` `src: Front-end specification, copy`
- [ ] `C-FE-210` `literal` The privacy heading reads `What we record`. `src: Front-end specification, copy`
- [ ] `C-FE-211` `literal` The terms heading reads `Using the platform`. `src: Front-end specification, copy`
- [ ] `C-FE-212` `literal` The not-found heading reads `We cannot find that page`. `src: Front-end specification, copy`
- [ ] `C-FE-213` `literal` The not-found body string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-214` `literal` The footer columns string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-215` `literal` The footer baseline read `Privacy`, `Site terms`. `src: Front-end specification, copy`
- [ ] `C-FE-216` `literal` The footer fine print reads `Meridian Cloud. All rights reserved.` `src: Front-end specification, copy`
- [ ] `C-FE-217` `literal` The desk sign-in heading reads `Sign in to the desk`. `src: Front-end specification, copy`
- [ ] `C-FE-218` `literal` The desk sign-in submit reads `Sign in`. `src: Front-end specification, copy`
- [ ] `C-FE-219` `literal` The desk sign-in failure string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-220` `literal` The desk list heading reads `Products`. `src: Front-end specification, copy`
- [ ] `C-FE-221` `literal` The desk detail pane control reads `Open in composer`. `src: Front-end specification, copy`
- [ ] `C-FE-222` `literal` The desk sidebar sign-out control reads `Sign out`. `src: Front-end specification, copy`
- [ ] `C-FE-223` `literal` The desk filter controls read `All`, `Live`, `Draft`. `src: Front-end specification, copy`
- [ ] `C-FE-224` `literal` The desk new control reads `New product`. `src: Front-end specification, copy`
- [ ] `C-FE-225` `literal` The desk badges read `Live`, `Draft`. `src: Front-end specification, copy`
- [ ] `C-FE-226` `literal` The desk art field label string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-227` `literal` The desk composer controls read `Save draft`, `Publish`, `Return to draft`. `src: Front-end specification, copy`
- [ ] `C-FE-228` `literal` The desk return confirmation string appears exactly as the copy deck states. `src: Front-end specification, copy`
- [ ] `C-FE-229` `literal` The desk confirmation cancel reads `Cancel`. `src: Front-end specification, copy`
- [ ] `C-FE-230` `literal` The desk enquiries heading reads `Evaluation requests`. `src: Front-end specification, copy`
- [ ] `C-FE-231` `literal` The desk views heading reads `Page views`. `src: Front-end specification, copy`
- [ ] `C-FE-232` `literal` The message, upload failed string appears exactly as the copy deck states. `src: Front-end specification, copy`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app carries no payments, no pricing calculator, no billing. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app carries no visitor accounts, no registration endpoint, no password reset flow, no visitor profile. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The assistant calls no language model, answering nothing. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The app carries no search service; the overlay filters published products inside the app. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` The app sends no email; the contact form stores its submission. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` The app carries no localisation with no language selector. `src: Constraints bullet 6`
- [ ] `C-CN-07` `constraint` The app carries no newsletter signup. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` The app carries three product families, not six. `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` The app carries no video, no video thumbnail. `src: Constraints bullet 9`
- [ ] `C-CN-10` `constraint` The app carries no multi-tenancy, no single sign-on. `src: Constraints bullet 10`
- [ ] `C-CN-11` `constraint` The page-view log is the app's own table, with no third-party analytics vendor. `src: Constraints bullet 11`
- [ ] `C-CN-12` `constraint` `Start free` with `Get started for free` open the contact-sales form. `src: Constraints bullet 12`
- [ ] `C-CN-13` `constraint` The networking with the assistant products carry no separate template. `src: Constraints bullet 13`
- [ ] `C-CN-14` `constraint` The app ships no binary asset. `src: Constraints bullet 15`
- [ ] `C-CN-15` `literal` The app stays responsive with the seeded `9` products, `20` art pieces, `5` datasheets, `6` industries, `8` customers, `3` desk accounts. `src: Constraints bullet 16`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, reading both from the environment. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `contract` The app serves a production build, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, no child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The app binds `0.0.0.0`, never a loopback address. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `contract` The backing services are already running; the app starts no copy of any. `src: Deployment contract bullet 10`
- [ ] `C-DC-11` `contract` The app uses only the providers named in the brief, with no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-12` `contract` The app carries no persistent volume, no fixed container name, no custom network. `src: Deployment contract bullet 12`
- [ ] `C-DC-13` `constraint` An invalid or unauthorized call is rejected as a client error, never a server error, never a silent success. `src: Deployment contract, API shapes table`
- [ ] `C-DC-14` `constraint` List endpoints return a top-level JSON array. `src: Deployment contract, API shapes table`
- [ ] `C-DC-15` `constraint` Every response is served from `PostgreSQL` with `MinIO`, no fixture file or in-memory stub standing in. `src: Deployment contract, no mocks`
- [ ] `C-DC-16` `constraint` Art with datasheet bytes live in the bucket, not on the app container disk. `src: Deployment contract, no mocks`
- [ ] `C-DC-17` `constraint` The console regions with writes are rows, not a client-side simulation. `src: Deployment contract, no mocks`
- [ ] `C-DC-18` `literal` `GET /api/health` answers `{"status": "ready"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-19` `literal` `GET /api/products` takes `family`, `sort` of `name` or `recent`, `name`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-20` `literal` `GET /api/products` answers rows carrying `id`, `slug`, `name`, `eyebrow`, `summary`, `families`, `featured`, `sort_index`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-21` `literal` `GET /api/products/{slug}` answers one published product with `heading`, `lead`, `highlights`, `art`, `datasheet`, `related`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-22` `constraint` `GET /api/products/{slug}` answers not found where the product is `draft` or absent. `src: Deployment contract, API shapes table`
- [ ] `C-DC-23` `literal` `GET /api/families` answers three rows carrying `id`, `slug`, `name`, `standfirst`, `published_count`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-24` `literal` `GET /api/families/{slug}` answers one family with `intro` plus `products`, its published products. `src: Deployment contract, API shapes table`
- [ ] `C-DC-25` `literal` `GET /api/industries` answers six rows in `sort_index` order carrying `slug`, `name`, `stat_line`, `customer_name`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-26` `literal` `GET /api/customers` answers eight rows in `sort_index` order carrying `id`, `name`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-27` `literal` `GET /api/datasheets` answers rows carrying `id`, `title`, `page_count`, `byte_size`, `product_name` where one exists. `src: Deployment contract, API shapes table`
- [ ] `C-DC-28` `literal` `GET /api/art` takes `family` as a slug with `page` counting from `1`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-29` `literal` `GET /api/art` answers pages of 24 rows carrying `id`, `product_slug`, `product_name`, `alt_text`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-30` `constraint` `GET /api/media/art/{art_id}` answers not found where the owner is `draft` with no valid desk bearer token. `src: Deployment contract, API shapes table`
- [ ] `C-DC-31` `constraint` `GET /api/media/datasheets/{datasheet_id}` answers not found where the owner is `draft` with no valid desk bearer token. `src: Deployment contract, API shapes table`
- [ ] `C-DC-32` `literal` `POST /api/console/write` takes `region`, `key`, `value`, answering `commit_timestamp` with `uncertainty_ms`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-33` `literal` `POST /api/console/read` takes `region`, `key`, `mode`, `bound`, `timestamp`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-34` `literal` `POST /api/console/read` answers `value`, `timestamp`, `staleness`, `latency_ms`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-35` `literal` `POST /api/console/partition` takes `region` with `severed`, answering `regions`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-36` `literal` `POST /api/console/reset` answers `regions`, every region unsevered. `src: Deployment contract, API shapes table`
- [ ] `C-DC-37` `literal` `POST /api/contact` takes `name`, `work_email`, `company`, `region`, `interest`, `message`, answering `ok` with `enquiry_id`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-38` `literal` `POST /api/auth/login` takes `email` with `password`, answering `access_token` with `role`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-39` `literal` `POST /api/auth/logout` ends the session. `src: Deployment contract, API shapes table`
- [ ] `C-DC-40` `literal` `GET /api/desk/products` takes `state` of `all`, `published`, `draft`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-41` `literal` `GET /api/desk/products` answers rows carrying `id`, `slug`, `name`, `state`, `families`, `featured`, `art_count`, `updated_at`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-42` `literal` `GET /api/desk/products/counts` answers `all`, `published`, `draft`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-43` `literal` `GET /api/desk/products/{id}` answers one product in either state with `art` plus `datasheet`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-44` `literal` `POST /api/desk/products` answers the created product, always `draft`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-45` `literal` `PATCH /api/desk/products/{id}` answers the updated product. `src: Deployment contract, API shapes table`
- [ ] `C-DC-46` `literal` `POST /api/desk/products/{id}/publish` answers the published product or a refusal naming the condition. `src: Deployment contract, API shapes table`
- [ ] `C-DC-47` `literal` `POST /api/desk/products/{id}/unpublish` answers the product back in `draft`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-48` `constraint` Publish with unpublish answer only a publisher or an administrator. `src: Deployment contract, API shapes table`
- [ ] `C-DC-49` `literal` `POST /api/desk/uploads` takes `product_id`, `kind` of `art` or `datasheet`, `filename`, `content_type`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-50` `literal` `POST /api/desk/art` takes `product_id`, `object_key`, `alt_text`, `width`, `height`, `sort_index`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-51` `literal` `POST /api/desk/datasheets` takes `product_id`, `object_key`, `title`, answering `id`, `title`, `page_count`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-52` `literal` `GET /api/desk/enquiries` answers the stored submissions newest first, to an administrator only. `src: Deployment contract, API shapes table`
- [ ] `C-DC-53` `literal` `GET /api/desk/views` answers `counts` entries carrying `route`, `count`, ordered by `count` descending, plus `recent` entries carrying `route`, `viewed_at`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-54` `constraint` `GET /api/desk/views` answers an administrator only. `src: Deployment contract, API shapes table`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Meridian Cloud` | The app serves a public site for the cloud platform `Meridian Cloud` | C-OV-01 | Overview para 1 |
| `Tessera` | The site makes credible the claim that `Tessera` stays strongly consistent across regions | C-OV-03 | Overview para 1 |
| `visitor` | The app carries four roles, `visitor`, `editor`, `publisher`, `administrator` | C-RL-01 | User roles table |
| `editor` | The app carries four roles, `visitor`, `editor`, `publisher`, `administrator` | C-RL-01 | User roles table |
| `publisher` | The app carries four roles, `visitor`, `editor`, `publisher`, `administrator` | C-RL-01 | User roles table |
| `administrator` | The app carries four roles, `visitor`, `editor`, `publisher`, `administrator` | C-RL-01 | User roles table |
| `editor@example.com` | The app seeds the editor address `editor@example.com` | C-RL-27 | User roles, seeded account table |
| `publisher@example.com` | The app seeds the publisher address `publisher@example.com` | C-RL-28 | User roles, seeded account table |
| `administrator@example.com` | The app seeds the administrator address `administrator@example.com` | C-RL-29 | User roles, seeded account table |
| `deku-demo-pw-2026` | Every seeded account uses the password `deku-demo-pw-2026` | C-RL-30 | User roles, seeded account table |
| `/app/USER_README.md` | The app writes each seeded address with its password into `/app/USER_README.md` | C-RL-31 | User roles, seeded account table |
| `draft` | The app keeps a `draft` product out of the product index | C-CF-01 | Core features rule 1 |
| `Accept` | The cookie choice carries an `Accept` control with a `Decline` control | C-CF-23 | Core features rule 6 |
| `Decline` | The cookie choice carries an `Accept` control with a `Decline` control | C-CF-23 | Core features rule 6 |
| `/console` | The app serves the consistency console at `/console` | C-CF-41 | Core features rule 11 |
| `/product/tessera` | The app embeds the console on `/product/tessera` | C-CF-43 | Core features rule 11 |
| `us-central` | The console names the five regions `us-central`, `eu-west`, `asia-south`, `sa-east`, `au-sout... | C-CF-44 | Core features rule 12 |
| `eu-west` | The console names the five regions `us-central`, `eu-west`, `asia-south`, `sa-east`, `au-sout... | C-CF-44 | Core features rule 12 |
| `asia-south` | The console names the five regions `us-central`, `eu-west`, `asia-south`, `sa-east`, `au-sout... | C-CF-44 | Core features rule 12 |
| `sa-east` | The console names the five regions `us-central`, `eu-west`, `asia-south`, `sa-east`, `au-sout... | C-CF-44 | Core features rule 12 |
| `au-southeast` | The console names the five regions `us-central`, `eu-west`, `asia-south`, `sa-east`, `au-sout... | C-CF-44 | Core features rule 12 |
| `uncertainty_ms` | A console write answers with a commit timestamp with `uncertainty_ms` | C-CF-47 | Core features rule 13 |
| `2026-09-16T09:06:10.123Z` | Every console timestamp is an ISO 8601 UTC string with milliseconds, like `2026-09-16T09:06:1... | C-CF-50 | Core features rule 13 |
| `strong` | A console read takes a region, a key, a mode of `strong`, `bounded`, `exact` | C-CF-52 | Core features rule 14 |
| `bounded` | A console read takes a region, a key, a mode of `strong`, `bounded`, `exact` | C-CF-52 | Core features rule 14 |
| `exact` | A console read takes a region, a key, a mode of `strong`, `bounded`, `exact` | C-CF-52 | Core features rule 14 |
| `0` | The read staleness is whole milliseconds behind the latest acknowledged write, `0` for a `str... | C-CF-54 | Core features rule 14 |
| `/product` | The app serves the flat product index at `/product` under its heading with a count line | C-CF-77 | Core features rule 22 |
| `/product/{slug}` | The app serves one published product at `/product/{slug}` with its eyebrow, heading, highligh... | C-CF-79 | Core features rule 23 |
| `?family=databases` | The family filter takes the family slug, like `?family=databases` | C-CF-88 | Core features rule 25 |
| `name` | The app orders the product index by name ascending where the sort is `name` | C-CF-90 | Core features rule 26 |
| `recent` | The app orders the product index most recently added first where the sort is `recent` | C-CF-91 | Core features rule 26 |
| `/family` | The app serves the three seeded families at `/family` | C-CF-97 | Core features rule 29 |
| `/family/{slug}` | The app serves one family at `/family/{slug}` with its editorial introduction | C-CF-99 | Core features rule 30 |
| `/solution` | The app serves the six seeded industries at `/solution` filtered by chips reading `All` plus ... | C-CF-102 | Core features rule 31 |
| `All` | The app serves the six seeded industries at `/solution` filtered by chips reading `All` plus ... | C-CF-102 | Core features rule 31 |
| `/datasheet` | The app serves the datasheet library at `/datasheet` | C-CF-106 | Core features rule 33 |
| `Content-Disposition` | A datasheet download carries a `Content-Disposition` of `attachment` | C-CF-113 | Core features rule 35 |
| `attachment` | A datasheet download carries a `Content-Disposition` of `attachment` | C-CF-113 | Core features rule 35 |
| `Meridian Platform Overview` | `Meridian Platform Overview` downloads as `meridian-platform-overview.pdf` | C-CF-114 | Core features rule 35 |
| `meridian-platform-overview.pdf` | `Meridian Platform Overview` downloads as `meridian-platform-overview.pdf` | C-CF-114 | Core features rule 35 |
| `/gallery` | The app serves the art gallery at `/gallery` as one grid | C-CF-115 | Core features rule 36 |
| `24` | The art gallery pages at `24` pieces | C-CF-116 | Core features rule 36 |
| `1` | The art gallery pages from page `1`, narrowing by family slug | C-CF-118 | Core features rule 36 |
| `Americas` | The contact region is one of `Americas`, `Europe`, `Asia Pacific` | C-CF-124 | Core features rule 38 |
| `Europe` | The contact region is one of `Americas`, `Europe`, `Asia Pacific` | C-CF-124 | Core features rule 38 |
| `Asia Pacific` | The contact region is one of `Americas`, `Europe`, `Asia Pacific` | C-CF-124 | Core features rule 38 |
| `Evaluation` | The contact interest is one of `Evaluation`, `Migration`, `Pricing` | C-CF-125 | Core features rule 38 |
| `Migration` | The contact interest is one of `Evaluation`, `Migration`, `Pricing` | C-CF-125 | Core features rule 38 |
| `Pricing` | The contact interest is one of `Evaluation`, `Migration`, `Pricing` | C-CF-125 | Core features rule 38 |
| `2` | The app refuses a contact name shorter than `2` characters | C-CF-129 | Core features rule 39 |
| `1000` | The app refuses a contact message running past `1000` characters | C-CF-130 | Core features rule 39 |
| `/ask` | The app serves the assistant surface at `/ask` with its greeting, four suggestions, its counter | C-CF-136 | Core features rule 41 |
| `500` | Typing or pasting past `500` characters keeps the first 500 in the assistant field | C-CF-137 | Core features rule 41 |
| `/desk/login` | The app serves the desk sign-in at `/desk/login` | C-CF-140 | Core features rule 42 |
| `/desk` | A signed-out `/desk` shows the sign-in card rather than the product list | C-CF-141 | Core features rule 42 |
| `Live` | A desk row carries a badge reading `Live` or `Draft` | C-CF-146 | Core features rule 45 |
| `Draft` | A desk row carries a badge reading `Live` or `Draft` | C-CF-146 | Core features rule 45 |
| `GET /api/desk/products/counts` | The desk filter counts come from `GET /api/desk/products/counts` as `all`, `published`, `draft` | C-CF-147 | Core features rule 45 |
| `all` | The desk filter counts come from `GET /api/desk/products/counts` as `all`, `published`, `draft` | C-CF-147 | Core features rule 45 |
| `published` | The desk filter counts come from `GET /api/desk/products/counts` as `all`, `published`, `draft` | C-CF-147 | Core features rule 45 |
| `art_count` | Each desk row carries `art_count` | C-CF-148 | Core features rule 45 |
| `Open in composer` | The detail pane control `Open in composer` opens `/desk/product/{id}` | C-CF-150 | Core features rule 45 |
| `/desk/product/{id}` | The detail pane control `Open in composer` opens `/desk/product/{id}` | C-CF-150 | Core features rule 45 |
| `desk` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `api` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `media` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `product` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `family` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `solution` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `datasheet` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `gallery` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `console` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `ask` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `contact` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `privacy` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `terms` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `404` | The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `data... | C-CF-166 | Core features rule 50 |
| `240` | The app refuses a summary longer than `240` characters | C-CF-171 | Core features rule 53 |
| `/desk/views` | Only an administrator reads the page-view log at `/desk/views` | C-CF-174 | Core features rule 55 |
| `/privacy` | The app serves the privacy page at `/privacy` | C-CF-178 | Core features rule 57 |
| `/terms` | The app serves the site terms at `/terms` | C-CF-179 | Core features rule 57 |
| `/` | The app serves `/` with no account | C-UF-01 | User flow route table |
| `/contact` | The app serves `/contact` with no account | C-UF-11 | User flow route table |
| `/desk/product/new` | The app serves `/desk/product/new` to editor, publisher, administrator | C-UF-16 | User flow route table |
| `/desk/enquiries` | The app serves `/desk/enquiries` to administrator | C-UF-18 | User flow route table |
| `amber` | A visitor writing `amber` into `us-central` then reading from `eu-west` in mode `strong` rece... | C-UF-25 | User flow journey 3 |
| `/product/halyard` | A signed-out visitor opening `/product/halyard` receives the heading `We cannot find that page` | C-UF-30 | User flow journey 5 |
| `We cannot find that page` | A signed-out visitor opening `/product/halyard` receives the heading `We cannot find that page` | C-UF-30 | User flow journey 5 |
| `Halyard` | `Halyard` is absent from the product index, the `Networking` family, the art gallery, the hea... | C-UF-31 | User flow journey 5 |
| `Networking` | `Halyard` is absent from the product index, the `Networking` family, the art gallery, the hea... | C-UF-31 | User flow journey 5 |
| `Tessera database` | A visitor reads the eyebrow `Tessera database` on the flagship product route | C-UF-32 | User flow journey 6 |
| `One database, every region, one truth` | A visitor reads the heading `One database, every region, one truth` on the flagship product r... | C-UF-33 | User flow journey 6 |
| `8 products` | A visitor reads the count line `8 products` on the product index | C-UF-35 | User flow journey 7 |
| `slip` | Typing `slip` into the name field leaves `Slipstream` as the only card | C-UF-36 | User flow journey 7 |
| `Slipstream` | Typing `slip` into the name field leaves `Slipstream` as the only card | C-UF-36 | User flow journey 7 |
| `Databases` | Choosing the family `Databases`, copying the address, reloading, keeps the family filter applied | C-UF-37 | User flow journey 8 |
| `Name, A to Z` | The sort `Name, A to Z` orders the cards alphabetically | C-UF-38 | User flow journey 9 |
| `Recently added` | The sort `Recently added` puts the newest first | C-UF-39 | User flow journey 9 |
| `zzzz` | Typing `zzzz` shows the empty message with a `Clear filter` control | C-UF-40 | User flow journey 10 |
| `Clear filter` | Typing `zzzz` shows the empty message with a `Clear filter` control | C-UF-40 | User flow journey 10 |
| `Families` | A visitor follows `Families` in the header to the three cards with their published counts | C-UF-42 | User flow journey 11 |
| `Telecommunications` | Selecting `Telecommunications` swaps the explorer to its proof card with its stat line, its c... | C-UF-43 | User flow journey 12 |
| `Kestrel` | Typing the name `Kestrel` fills the web address in as `kestrel` | C-UF-50 | User flow journey 16 |
| `kestrel` | Typing the name `Kestrel` fills the web address in as `kestrel` | C-UF-50 | User flow journey 16 |
| `banner` | The app carries one `banner`, one `main` per route, one `contentinfo` | C-UX-07 | UI/UX notes, the accessibility paragraph |
| `main` | The app carries one `banner`, one `main` per route, one `contentinfo` | C-UX-07 | UI/UX notes, the accessibility paragraph |
| `contentinfo` | The app carries one `banner`, one `main` per route, one `contentinfo` | C-UX-07 | UI/UX notes, the accessibility paragraph |
| `h1` | The app carries one `h1` per route | C-UX-09 | UI/UX notes, the accessibility paragraph |
| `Manrope` | Display headings, product titles, card titles take the family `Manrope` | C-UX-45 | UI/UX notes, the type paragraph |
| `Inter` | Body, navigation, badges, filter controls, metadata take the family `Inter` | C-UX-46 | UI/UX notes, the type paragraph |
| `Fastify` | The server is `Fastify` | C-TR-03 | Technical requirements para 1 |
| `SolidStart` | The client is `SolidStart` in TypeScript | C-TR-04 | Technical requirements para 1 |
| `PostgreSQL` | The app reads the `PostgreSQL` connection from `DATABASE_URL` | C-TR-09 | Technical requirements, environment variable table |
| `DATABASE_URL` | The app reads the `PostgreSQL` connection from `DATABASE_URL` | C-TR-09 | Technical requirements, environment variable table |
| `MinIO` | The app reads the `MinIO` endpoint from `STORAGE_ENDPOINT` | C-TR-10 | Technical requirements, environment variable table |
| `STORAGE_ENDPOINT` | The app reads the `MinIO` endpoint from `STORAGE_ENDPOINT` | C-TR-10 | Technical requirements, environment variable table |
| `STORAGE_BUCKET` | The app reads the bucket from `STORAGE_BUCKET` | C-TR-11 | Technical requirements, environment variable table |
| `STORAGE_ACCESS_KEY` | The app reads the `MinIO` keys from `STORAGE_ACCESS_KEY` with `STORAGE_SECRET_KEY` | C-TR-12 | Technical requirements, environment variable table |
| `STORAGE_SECRET_KEY` | The app reads the `MinIO` keys from `STORAGE_ACCESS_KEY` with `STORAGE_SECRET_KEY` | C-TR-12 | Technical requirements, environment variable table |
| `APP_PUBLIC_URL` | The app reads the origin from `APP_PUBLIC_URL` with the outside port from `APP_PUBLIC_PORT` | C-TR-13 | Technical requirements, environment variable table |
| `APP_PUBLIC_PORT` | The app reads the origin from `APP_PUBLIC_URL` with the outside port from `APP_PUBLIC_PORT` | C-TR-13 | Technical requirements, environment variable table |
| `12` | A desk session token expires after `12` hours | C-TR-15 | Technical requirements, the sessions paragraph |
| `POST /api/auth/login` | `POST /api/auth/login` takes an email with a password, answering with a bearer token | C-TR-17 | Technical requirements, the sessions paragraph |
| `15` | An upload target expires after `15` minutes, scoped to one object key | C-TR-18 | Technical requirements, the object writes paragraph |
| `url` | The upload answer carries `url`, `method`, `headers`, `object_key` | C-TR-19 | Technical requirements, the object writes paragraph |
| `method` | The upload answer carries `url`, `method`, `headers`, `object_key` | C-TR-19 | Technical requirements, the object writes paragraph |
| `headers` | The upload answer carries `url`, `method`, `headers`, `object_key` | C-TR-19 | Technical requirements, the object writes paragraph |
| `object_key` | The upload answer carries `url`, `method`, `headers`, `object_key` | C-TR-19 | Technical requirements, the object writes paragraph |
| `GET /api/media/art/{art_id}` | The app serves art bytes at `GET /api/media/art/{art_id}` | C-TR-21 | Technical requirements, the object reads paragraph |
| `GET /api/media/datasheets/{datasheet_id}` | The app serves datasheet bytes at `GET /api/media/datasheets/{datasheet_id}` | C-TR-22 | Technical requirements, the object reads paragraph |
| `2.5` | The largest home content paints in under `2.5` seconds on a fourth-generation mobile connection | C-TR-27 | Technical requirements, the performance paragraph |
| `200` | An interaction paints its next frame in under `200` milliseconds | C-TR-28 | Technical requirements, the performance paragraph |
| `180KB` | The compressed JavaScript the home surface delivers stays under `180KB` | C-TR-30 | Technical requirements, the performance paragraph |
| `3` | No more than `3` requests block first paint on the home surface | C-TR-31 | Technical requirements, the performance paragraph |
| `GET /api/health` | `GET /api/health` answers with the body `{"status": "ready"}` | C-TR-37 | Technical requirements, the health paragraph |
| `{"status": "ready"}` | `GET /api/health` answers with the body `{"status": "ready"}` | C-TR-37 | Technical requirements, the health paragraph |
| `id` | The app carries `id`, `email`, `password_hash`, `role`, `created_at` on an account | C-DM-02 | Data model, the accounts paragraph |
| `email` | The app carries `id`, `email`, `password_hash`, `role`, `created_at` on an account | C-DM-02 | Data model, the accounts paragraph |
| `password_hash` | The app carries `id`, `email`, `password_hash`, `role`, `created_at` on an account | C-DM-02 | Data model, the accounts paragraph |
| `role` | The app carries `id`, `email`, `password_hash`, `role`, `created_at` on an account | C-DM-02 | Data model, the accounts paragraph |
| `created_at` | The app carries `id`, `email`, `password_hash`, `role`, `created_at` on an account | C-DM-02 | Data model, the accounts paragraph |
| `account_id` | The app carries `account_id`, `token_hash`, `expires_at`, `ended_at` on a session | C-DM-03 | Data model, the sessions paragraph |
| `token_hash` | The app carries `account_id`, `token_hash`, `expires_at`, `ended_at` on a session | C-DM-03 | Data model, the sessions paragraph |
| `expires_at` | The app carries `account_id`, `token_hash`, `expires_at`, `ended_at` on a session | C-DM-03 | Data model, the sessions paragraph |
| `ended_at` | The app carries `account_id`, `token_hash`, `expires_at`, `ended_at` on a session | C-DM-03 | Data model, the sessions paragraph |
| `eyebrow` | The app carries `eyebrow`, `heading`, `lead`, `summary`, `claim_body` on a product | C-DM-05 | Data model, the products paragraph |
| `heading` | The app carries `eyebrow`, `heading`, `lead`, `summary`, `claim_body` on a product | C-DM-05 | Data model, the products paragraph |
| `lead` | The app carries `eyebrow`, `heading`, `lead`, `summary`, `claim_body` on a product | C-DM-05 | Data model, the products paragraph |
| `summary` | The app carries `eyebrow`, `heading`, `lead`, `summary`, `claim_body` on a product | C-DM-05 | Data model, the products paragraph |
| `claim_body` | The app carries `eyebrow`, `heading`, `lead`, `summary`, `claim_body` on a product | C-DM-05 | Data model, the products paragraph |
| `state` | The app carries `state` on a product, `draft` or `published` in lowercase | C-DM-06 | Data model, the products paragraph |
| `families` | The app carries `families`, `featured`, `sort_index` on a product | C-DM-07 | Data model, the products paragraph |
| `featured` | The app carries `families`, `featured`, `sort_index` on a product | C-DM-07 | Data model, the products paragraph |
| `sort_index` | The app carries `families`, `featured`, `sort_index` on a product | C-DM-07 | Data model, the products paragraph |
| `service_level` | The app carries `service_level`, `regions_available`, `created_at`, `updated_at` on a product | C-DM-08 | Data model, the products paragraph |
| `regions_available` | The app carries `service_level`, `regions_available`, `created_at`, `updated_at` on a product | C-DM-08 | Data model, the products paragraph |
| `updated_at` | The app carries `service_level`, `regions_available`, `created_at`, `updated_at` on a product | C-DM-08 | Data model, the products paragraph |
| `slug` | A product `slug` is unique among published products | C-DM-09 | Data model, the products paragraph |
| `line` | The app carries `line`, `sort_index` on a highlight, one claim band per line | C-DM-11 | Data model, the highlights paragraph |
| `alt_text` | The app carries `object_key`, `alt_text`, `seed`, `width`, `height` on an art piece | C-DM-12 | Data model, the art paragraph |
| `seed` | The app carries `object_key`, `alt_text`, `seed`, `width`, `height` on an art piece | C-DM-12 | Data model, the art paragraph |
| `width` | The app carries `object_key`, `alt_text`, `seed`, `width`, `height` on an art piece | C-DM-12 | Data model, the art paragraph |
| `height` | The app carries `object_key`, `alt_text`, `seed`, `width`, `height` on an art piece | C-DM-12 | Data model, the art paragraph |
| `product_id` | The app leaves `product_id` null on a platform datasheet | C-DM-13 | Data model, the datasheets paragraph |
| `page_count` | A datasheet stores its `page_count`, read from the document at registration or seed, never it... | C-DM-14 | Data model, the datasheets paragraph |
| `region` | The app carries `region`, `key`, `value`, `commit_timestamp`, `uncertainty_ms` on a console w... | C-DM-15 | Data model, the console paragraph |
| `key` | The app carries `region`, `key`, `value`, `commit_timestamp`, `uncertainty_ms` on a console w... | C-DM-15 | Data model, the console paragraph |
| `value` | The app carries `region`, `key`, `value`, `commit_timestamp`, `uncertainty_ms` on a console w... | C-DM-15 | Data model, the console paragraph |
| `commit_timestamp` | The app carries `region`, `key`, `value`, `commit_timestamp`, `uncertainty_ms` on a console w... | C-DM-15 | Data model, the console paragraph |
| `severed` | The app carries `region`, `severed` on a partition row | C-DM-16 | Data model, the console paragraph |
| `work_email` | The app carries `name`, `work_email`, `company`, `region`, `interest`, `message`, `received_a... | C-DM-17 | Data model, the enquiries paragraph |
| `company` | The app carries `name`, `work_email`, `company`, `region`, `interest`, `message`, `received_a... | C-DM-17 | Data model, the enquiries paragraph |
| `interest` | The app carries `name`, `work_email`, `company`, `region`, `interest`, `message`, `received_a... | C-DM-17 | Data model, the enquiries paragraph |
| `message` | The app carries `name`, `work_email`, `company`, `region`, `interest`, `message`, `received_a... | C-DM-17 | Data model, the enquiries paragraph |
| `received_at` | The app carries `name`, `work_email`, `company`, `region`, `interest`, `message`, `received_a... | C-DM-17 | Data model, the enquiries paragraph |
| `route` | The app carries `route`, `viewed_at` on a page view | C-DM-18 | Data model, the page views paragraph |
| `viewed_at` | The app carries `route`, `viewed_at` on a page view | C-DM-18 | Data model, the page views paragraph |
| `products/<product_id>/art/<sha256_of_bytes>.<ext>` | The app stores an art piece under `products/<product_id>/art/<sha256_of_bytes>.<ext>` | C-DM-21 | Data model, the object key table |
| `products/<product_id>/datasheet/<sha256_of_bytes>.pdf` | The app stores a product datasheet under `products/<product_id>/datasheet/<sha256_of_bytes>.pdf` | C-DM-22 | Data model, the object key table |
| `platform/<datasheet_id>/<sha256_of_bytes>.pdf` | The app stores a platform datasheet under `platform/<datasheet_id>/<sha256_of_bytes>.pdf` | C-DM-23 | Data model, the object key table |
| `Foundry` | The seeded products are created in `sort_index` order, the most recent being `Halyard`, then ... | C-DM-25 | Data model, the seed table |
| `Analytics` | The seed gives `Databases` 4 published products, `Networking` 3, `Analytics` 3 | C-DM-26 | Data model, the seed table |
| `tessera-1` | Each seeded art piece takes the product slug plus its sort index as its `seed`, like `tessera-1` | C-DM-27 | Data model, the seeded art paragraph |
| `1200` | Each seeded art piece is drawn at `1200` by `900` | C-DM-28 | Data model, the seeded art paragraph |
| `900` | Each seeded art piece is drawn at `1200` by `900` | C-DM-28 | Data model, the seeded art paragraph |
| `<product name> card art, generated field <sort index> of <art count>` | Each seeded art piece carries the alternative text `<product name> card art, generated field ... | C-DM-29 | Data model, the seeded art paragraph |
| `Tessera card art, generated field 1 of 3` | The first `Tessera` art piece reads `Tessera card art, generated field 1 of 3` | C-DM-30 | Data model, the seeded art paragraph |
| `A fully managed relational database with strong consistency across regions, backed by synchronized clocks.` | `Tessera` carries the lead `A fully managed relational database with strong consistency acros... | C-DM-31 | Data model, the Tessera paragraph |
| `99.999%` | `Tessera` carries the service level `99.999%` with `5` regions available | C-DM-32 | Data model, the Tessera paragraph |
| `5` | `Tessera` carries the service level `99.999%` with `5` regions available | C-DM-32 | Data model, the Tessera paragraph |
| `The Global Network` | The app seeds the platform datasheets `Meridian Platform Overview`, `The Global Network`, `Co... | C-DM-34 | Data model, the seed paragraph |
| `Consistency Explained` | The app seeds the platform datasheets `Meridian Platform Overview`, `The Global Network`, `Co... | C-DM-34 | Data model, the seed paragraph |
| `Harrowgate` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `Vessel Foods` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `Cobalt Bank` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `Truenorth` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `Stonecraft` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `Threadly` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `Marea Global` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `The Gazette` | The app seeds the proof wall customers in the order `Harrowgate`, `Vessel Foods`, `Cobalt Ban... | C-DM-36 | Data model, the customer paragraph |
| `Anjali Rao` | The testimonial is attributed to `Anjali Rao`, `SVP of Engineering for Network Automation`, `... | C-DM-37 | Data model, the testimonial paragraph |
| `SVP of Engineering for Network Automation` | The testimonial is attributed to `Anjali Rao`, `SVP of Engineering for Network Automation`, `... | C-DM-37 | Data model, the testimonial paragraph |
| `tessera` | The app seeds `Tessera` at `tessera` as `published` in Databases, featured, sort index `1`, w... | C-DM-39 | Data model, the seed table |
| `Tessera Technical Overview` | The app seeds `Tessera` at `tessera` as `published` in Databases, featured, sort index `1`, w... | C-DM-39 | Data model, the seed table |
| `slipstream` | The app seeds `Slipstream` at `slipstream` as `published` in Networking, featured, sort index... | C-DM-40 | Data model, the seed table |
| `Beacon Enterprise` | The app seeds `Beacon Enterprise` at `beacon-enterprise` as `published` in Analytics, feature... | C-DM-41 | Data model, the seed table |
| `beacon-enterprise` | The app seeds `Beacon Enterprise` at `beacon-enterprise` as `published` in Analytics, feature... | C-DM-41 | Data model, the seed table |
| `Quarry` | The app seeds `Quarry` at `quarry` as `published` in Databases, Analytics, featured, sort ind... | C-DM-42 | Data model, the seed table |
| `quarry` | The app seeds `Quarry` at `quarry` as `published` in Databases, Analytics, featured, sort ind... | C-DM-42 | Data model, the seed table |
| `4` | The app seeds `Quarry` at `quarry` as `published` in Databases, Analytics, featured, sort ind... | C-DM-42 | Data model, the seed table |
| `Bastion` | The app seeds `Bastion` at `bastion` as `published` in Networking, featured, sort index `5`, ... | C-DM-43 | Data model, the seed table |
| `bastion` | The app seeds `Bastion` at `bastion` as `published` in Networking, featured, sort index `5`, ... | C-DM-43 | Data model, the seed table |
| `Anvil` | The app seeds `Anvil` at `anvil` as `published` in Networking, Databases, featured, sort inde... | C-DM-44 | Data model, the seed table |
| `anvil` | The app seeds `Anvil` at `anvil` as `published` in Networking, Databases, featured, sort inde... | C-DM-44 | Data model, the seed table |
| `6` | The app seeds `Anvil` at `anvil` as `published` in Networking, Databases, featured, sort inde... | C-DM-44 | Data model, the seed table |
| `Lattice` | The app seeds `Lattice` at `lattice` as `published` in Analytics, not featured, sort index `7... | C-DM-45 | Data model, the seed table |
| `lattice` | The app seeds `Lattice` at `lattice` as `published` in Analytics, not featured, sort index `7... | C-DM-45 | Data model, the seed table |
| `7` | The app seeds `Lattice` at `lattice` as `published` in Analytics, not featured, sort index `7... | C-DM-45 | Data model, the seed table |
| `foundry` | The app seeds `Foundry` at `foundry` as `published` in Databases, not featured, sort index `8... | C-DM-46 | Data model, the seed table |
| `8` | The app seeds `Foundry` at `foundry` as `published` in Databases, not featured, sort index `8... | C-DM-46 | Data model, the seed table |
| `halyard` | The app seeds `Halyard` at `halyard` as `draft` in Networking, not featured, sort index `9`, ... | C-DM-47 | Data model, the seed table |
| `9` | The app seeds `Halyard` at `halyard` as `draft` in Networking, not featured, sort index `9`, ... | C-DM-47 | Data model, the seed table |
| `Halyard Technical Overview` | The app seeds `Halyard` at `halyard` as `draft` in Networking, not featured, sort index `9`, ... | C-DM-47 | Data model, the seed table |
| `Reads always reflect the latest write` | `Tessera` carries the highlight line `Reads always reflect the latest write` at sort index `1` | C-DM-48 | Data model, the highlight table |
| `Correct through network partitions, never corrupted` | `Tessera` carries the highlight line `Correct through network partitions, never corrupted` at... | C-DM-50 | Data model, the highlight table |
| `Massive transaction scale with no consistency trade` | `Tessera` carries the highlight line `Massive transaction scale with no consistency trade` at... | C-DM-51 | Data model, the highlight table |
| `Synchronous multi-region replication` | `Tessera` carries the highlight line `Synchronous multi-region replication` at sort index `5` | C-DM-52 | Data model, the highlight table |
| `Automatic failover with zero data loss` | `Tessera` carries the highlight line `Automatic failover with zero data loss` at sort index `7` | C-DM-54 | Data model, the highlight table |
| `Five-nines availability, multi-region` | `Tessera` carries the highlight line `Five-nines availability, multi-region` at sort index `8` | C-DM-55 | Data model, the highlight table |
| `Retail` | The app seeds the industry `Retail` at `retail` with the customer `Vessel Foods` | C-DM-56 | Data model, the industry table |
| `retail` | The app seeds the industry `Retail` at `retail` with the customer `Vessel Foods` | C-DM-56 | Data model, the industry table |
| `9 of the top 10 retail companies build on Meridian Cloud` | The industry `Retail` carries the stat line `9 of the top 10 retail companies build on Meridi... | C-DM-57 | Data model, the industry table |
| `Financial services` | The app seeds the industry `Financial services` at `financial-services` with the customer `Co... | C-DM-58 | Data model, the industry table |
| `financial-services` | The app seeds the industry `Financial services` at `financial-services` with the customer `Co... | C-DM-58 | Data model, the industry table |
| `Nearly 90% of the largest global banks run regulated workloads here` | The industry `Financial services` carries the stat line `Nearly 90% of the largest global ban... | C-DM-59 | Data model, the industry table |
| `Healthcare` | The app seeds the industry `Healthcare` at `healthcare` with the customer `Truenorth` | C-DM-60 | Data model, the industry table |
| `healthcare` | The app seeds the industry `Healthcare` at `healthcare` with the customer `Truenorth` | C-DM-60 | Data model, the industry table |
| `Clinical records stay in region, with one consistent read` | The industry `Healthcare` carries the stat line `Clinical records stay in region, with one co... | C-DM-61 | Data model, the industry table |
| `telecommunications` | The app seeds the industry `Telecommunications` at `telecommunications` with the customer `Ha... | C-DM-62 | Data model, the industry table |
| `Issue resolution cut from hours to minutes across a national network` | The industry `Telecommunications` carries the stat line `Issue resolution cut from hours to m... | C-DM-63 | Data model, the industry table |
| `Government` | The app seeds the industry `Government` at `government` with the customer `Marea Global` | C-DM-64 | Data model, the industry table |
| `government` | The app seeds the industry `Government` at `government` with the customer `Marea Global` | C-DM-64 | Data model, the industry table |
| `Residency guarantees met in 5 regions at once` | The industry `Government` carries the stat line `Residency guarantees met in 5 regions at once` | C-DM-65 | Data model, the industry table |
| `Manufacturing` | The app seeds the industry `Manufacturing` at `manufacturing` with the customer `Stonecraft` | C-DM-66 | Data model, the industry table |
| `manufacturing` | The app seeds the industry `Manufacturing` at `manufacturing` with the customer `Stonecraft` | C-DM-66 | Data model, the industry table |
| `Plant telemetry at 1 million writes a second, ordered globally` | The industry `Manufacturing` carries the stat line `Plant telemetry at 1 million writes a sec... | C-DM-67 | Data model, the industry table |
| `16px` | The body step is `16px` over `24px` at `400` | C-FE-01 | Front-end specification, type scale |
| `24px` | The body step is `16px` over `24px` at `400` | C-FE-01 | Front-end specification, type scale |
| `400` | The body step is `16px` over `24px` at `400` | C-FE-01 | Front-end specification, type scale |
| `26px` | The body-tall step is `16px` over `26px` at `500` | C-FE-03 | Front-end specification, type scale |
| `14px` | The small step is `14px` over `24px` at `400` | C-FE-04 | Front-end specification, type scale |
| `13px` | The dense step is `13px` over `24px` at `400` | C-FE-05 | Front-end specification, type scale |
| `18px` | The lead step is `18px` over `28px` at `400` | C-FE-06 | Front-end specification, type scale |
| `28px` | The lead step is `18px` over `28px` at `400` | C-FE-06 | Front-end specification, type scale |
| `20px` | The title step is `20px` over `28px` at `500` | C-FE-07 | Front-end specification, type scale |
| `32px` | The heading step is `24px` over `32px` at `500` | C-FE-08 | Front-end specification, type scale |
| `36px` | The display step is `28px` over `36px` at `400` | C-FE-09 | Front-end specification, type scale |
| `12px` | The micro step is `12px` over `16px` at `400` | C-FE-10 | Front-end specification, type scale |
| `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif` | Both families are declared against the fallback stack `system-ui, -apple-system, "Segoe UI", ... | C-FE-14 | Front-end specification, type scale |
| `landing` | The `landing` shell is full-width bands with no side rail, used by the home route alone | C-FE-16 | Front-end specification, information architecture |
| `tool` | The `tool` shell is a centred single-purpose surface, used by the console with the assistant | C-FE-18 | Front-end specification, information architecture |
| `index` | The `index` shell is a filterable card grid, used by the five index surfaces | C-FE-19 | Front-end specification, information architecture |
| `4.5` | Body text with supporting copy meet a contrast of at least `4.5` to 1 | C-FE-28 | Front-end specification, accessibility values |
| `44` | A navigation target is at least `44` by `44` on its shorter side | C-FE-29 | Front-end specification, accessibility values |
| `Skip to content` | The first focusable element on every route is a `Skip to content` link into the `main` landmark | C-FE-30 | Front-end specification, accessibility values |
| `sm` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-31 | Front-end specification, layout and breakpoints |
| `md` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-31 | Front-end specification, layout and breakpoints |
| `lg` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-31 | Front-end specification, layout and breakpoints |
| `xl` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-31 | Front-end specification, layout and breakpoints |
| `xxl` | Five breakpoints are named `sm`, `md`, `lg`, `xl`, `xxl` in ascending order | C-FE-31 | Front-end specification, layout and breakpoints |
| `twelve` | The grid is `twelve` columns, capping at a maximum width | C-FE-32 | Front-end specification, layout and breakpoints |
| `Meridian` | The wordmark reads `Meridian` plus `Cloud`, linking to the home route | C-FE-51 | Front-end specification, chrome |
| `Cloud` | The wordmark reads `Meridian` plus `Cloud`, linking to the home route | C-FE-51 | Front-end specification, chrome |
| `Start free` | The header right cluster holds a search control with a filled `Start free` button opening the... | C-FE-53 | Front-end specification, chrome |
| `Products` | `Products` opens a full-width mega-menu grouping the published products by family | C-FE-54 | Front-end specification, chrome |
| `- Meridian Cloud` | Every public route title is the surface name followed by `- Meridian Cloud` | C-FE-67 | Front-end specification, chrome |
| `Get started for free` | The hero controls `Get started for free` with `Contact sales` both open the contact form | C-FE-71 | Front-end specification, home |
| `Contact sales` | The hero controls `Get started for free` with `Contact sales` both open the contact form | C-FE-71 | Front-end specification, home |
| `Overview` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Consistency` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Synchronized clock` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Partitions` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Scale` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Replication` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Read modes` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Failover` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `Service levels` | The `Tessera` sub-nav reads `Overview`, `Consistency`, `Synchronized clock`, `Partitions`, `S... | C-FE-85 | Front-end specification, product route |
| `How can I try Meridian Cloud products for free?` | The first assistant suggestion reads `How can I try Meridian Cloud products for free?` | C-FE-121 | Front-end specification, assistant, contact and standing surfaces |
| `How do I evaluate Tessera?` | The second assistant suggestion reads `How do I evaluate Tessera?` | C-FE-122 | Front-end specification, assistant, contact and standing surfaces |
| `Discover solutions for my industry` | The third assistant suggestion reads `Discover solutions for my industry` | C-FE-123 | Front-end specification, assistant, contact and standing surfaces |
| `Summarize what is new` | The fourth assistant suggestion reads `Summarize what is new` | C-FE-124 | Front-end specification, assistant, contact and standing surfaces |
| `Full name` | The contact form fields read `Full name`, `Work email`, `Company`, `Region`, `Interest`, `Mes... | C-FE-127 | Front-end specification, assistant, contact and standing surfaces |
| `Work email` | The contact form fields read `Full name`, `Work email`, `Company`, `Region`, `Interest`, `Mes... | C-FE-127 | Front-end specification, assistant, contact and standing surfaces |
| `Company` | The contact form fields read `Full name`, `Work email`, `Company`, `Region`, `Interest`, `Mes... | C-FE-127 | Front-end specification, assistant, contact and standing surfaces |
| `Region` | The contact form fields read `Full name`, `Work email`, `Company`, `Region`, `Interest`, `Mes... | C-FE-127 | Front-end specification, assistant, contact and standing surfaces |
| `Interest` | The contact form fields read `Full name`, `Work email`, `Company`, `Region`, `Interest`, `Mes... | C-FE-127 | Front-end specification, assistant, contact and standing surfaces |
| `Message` | The contact form fields read `Full name`, `Work email`, `Company`, `Region`, `Interest`, `Mes... | C-FE-127 | Front-end specification, assistant, contact and standing surfaces |
| `Email` | The desk sign-in fields read `Email` with `Password` | C-FE-132 | Front-end specification, the desk |
| `Password` | The desk sign-in fields read `Email` with `Password` | C-FE-132 | Front-end specification, the desk |
| `Sign out` | Every signed-in desk page carries a left sidebar holding `Products`, `Sign out` at its foot | C-FE-133 | Front-end specification, the desk |
| `Evaluation requests` | The desk sidebar shows `Evaluation requests` with `Page views` to an administrator only | C-FE-134 | Front-end specification, the desk |
| `Page views` | The desk sidebar shows `Evaluation requests` with `Page views` to an administrator only | C-FE-134 | Front-end specification, the desk |
| `Name` | The desk table columns read `Name`, `Families`, `State`, `Art`, `Last edited` | C-FE-136 | Front-end specification, the desk |
| `State` | The desk table columns read `Name`, `Families`, `State`, `Art`, `Last edited` | C-FE-136 | Front-end specification, the desk |
| `Art` | The desk table columns read `Name`, `Families`, `State`, `Art`, `Last edited` | C-FE-136 | Front-end specification, the desk |
| `Last edited` | The desk table columns read `Name`, `Families`, `State`, `Art`, `Last edited` | C-FE-136 | Front-end specification, the desk |
| `Product name` | The first six composer fields read `Product name`, `Web address`, `Eyebrow`, `Summary`, `Clai... | C-FE-143 | Front-end specification, the desk |
| `Web address` | The first six composer fields read `Product name`, `Web address`, `Eyebrow`, `Summary`, `Clai... | C-FE-143 | Front-end specification, the desk |
| `Eyebrow` | The first six composer fields read `Product name`, `Web address`, `Eyebrow`, `Summary`, `Clai... | C-FE-143 | Front-end specification, the desk |
| `Summary` | The first six composer fields read `Product name`, `Web address`, `Eyebrow`, `Summary`, `Clai... | C-FE-143 | Front-end specification, the desk |
| `Claim body` | The first six composer fields read `Product name`, `Web address`, `Eyebrow`, `Summary`, `Clai... | C-FE-143 | Front-end specification, the desk |
| `Families, up to three` | The first six composer fields read `Product name`, `Web address`, `Eyebrow`, `Summary`, `Clai... | C-FE-143 | Front-end specification, the desk |
| `Show on the front page` | The last six composer fields read `Show on the front page`, `Service level`, `Regions availab... | C-FE-144 | Front-end specification, the desk |
| `Service level` | The last six composer fields read `Show on the front page`, `Service level`, `Regions availab... | C-FE-144 | Front-end specification, the desk |
| `Regions available` | The last six composer fields read `Show on the front page`, `Service level`, `Regions availab... | C-FE-144 | Front-end specification, the desk |
| `Highlight lines` | The last six composer fields read `Show on the front page`, `Service level`, `Regions availab... | C-FE-144 | Front-end specification, the desk |
| `Datasheet` | The last six composer fields read `Show on the front page`, `Service level`, `Regions availab... | C-FE-144 | Front-end specification, the desk |
| `five` | A desk message dismisses after `five` seconds or on press | C-FE-151 | Front-end specification, the desk |
| `three` | The desk message stack holds at most `three`, a fourth displacing the oldest | C-FE-152 | Front-end specification, the desk |
| `eleven` | The iconography is `eleven` marks drawn from coordinates in the build | C-FE-154 | Front-end specification, iconography, motion mechanisms and the zero-asset substitution guide |
| `The new way to cloud with Meridian` | The home heading reads `The new way to cloud with Meridian` | C-FE-179 | Front-end specification, copy |
| `Try Beacon Enterprise, the front door to AI for every employee` | The home assistant pill reads `Try Beacon Enterprise, the front door to AI for every employee` | C-FE-183 | Front-end specification, copy |
| `Products that hold their promises` | The rail heading reads `Products that hold their promises` | C-FE-184 | Front-end specification, copy |
| `Solutions for your industry` | The explorer heading reads `Solutions for your industry` | C-FE-185 | Front-end specification, copy |
| `Teams that build here` | The proof heading reads `Teams that build here` | C-FE-186 | Front-end specification, copy |
| `Start your evaluation` | The closing heading reads `Start your evaluation` | C-FE-187 | Front-end specification, copy |
| `Ask anything about Meridian Cloud` | The ask bar placeholder reads `Ask anything about Meridian Cloud` | C-FE-188 | Front-end specification, copy |
| `We use cookies to measure how the site is used.` | The cookie band body reads `We use cookies to measure how the site is used.` | C-FE-189 | Front-end specification, copy |
| `Every product on the platform` | The product index heading reads `Every product on the platform` | C-FE-190 | Front-end specification, copy |
| `Filter by name` | The product index name field reads `Filter by name` | C-FE-191 | Front-end specification, copy |
| `Nothing matches that. Try a different family, or clear the filter.` | The product index empty reads `Nothing matches that. Try a different family, or clear the fil... | C-FE-192 | Front-end specification, copy |
| `Related products` | The related row heading reads `Related products` | C-FE-195 | Front-end specification, copy |
| `Three ways into the platform` | The family index heading reads `Three ways into the platform` | C-FE-196 | Front-end specification, copy |
| `Solutions by industry` | The solution index heading reads `Solutions by industry` | C-FE-198 | Front-end specification, copy |
| `Datasheets to download` | The datasheet library heading reads `Datasheets to download` | C-FE-200 | Front-end specification, copy |
| `Every product, drawn` | The gallery heading reads `Every product, drawn` | C-FE-201 | Front-end specification, copy |
| `Show more` | The gallery more control reads `Show more` | C-FE-203 | Front-end specification, copy |
| `Hello, how can I help?` | The assistant greeting reads `Hello, how can I help?` | C-FE-205 | Front-end specification, copy |
| `0 of 500 characters entered` | The assistant counter reads `0 of 500 characters entered` | C-FE-206 | Front-end specification, copy |
| `Built with Beacon Enterprise` | The assistant caption reads `Built with Beacon Enterprise` | C-FE-207 | Front-end specification, copy |
| `Thank you. Your evaluation request is with us.` | The contact success reads `Thank you. Your evaluation request is with us.` | C-FE-209 | Front-end specification, copy |
| `What we record` | The privacy heading reads `What we record` | C-FE-210 | Front-end specification, copy |
| `Using the platform` | The terms heading reads `Using the platform` | C-FE-211 | Front-end specification, copy |
| `Privacy` | The footer baseline read `Privacy`, `Site terms` | C-FE-215 | Front-end specification, copy |
| `Site terms` | The footer baseline read `Privacy`, `Site terms` | C-FE-215 | Front-end specification, copy |
| `Meridian Cloud. All rights reserved.` | The footer fine print reads `Meridian Cloud. All rights reserved.` | C-FE-216 | Front-end specification, copy |
| `Sign in to the desk` | The desk sign-in heading reads `Sign in to the desk` | C-FE-217 | Front-end specification, copy |
| `Sign in` | The desk sign-in submit reads `Sign in` | C-FE-218 | Front-end specification, copy |
| `New product` | The desk new control reads `New product` | C-FE-224 | Front-end specification, copy |
| `Save draft` | The desk composer controls read `Save draft`, `Publish`, `Return to draft` | C-FE-227 | Front-end specification, copy |
| `Publish` | The desk composer controls read `Save draft`, `Publish`, `Return to draft` | C-FE-227 | Front-end specification, copy |
| `Return to draft` | The desk composer controls read `Save draft`, `Publish`, `Return to draft` | C-FE-227 | Front-end specification, copy |
| `Cancel` | The desk confirmation cancel reads `Cancel` | C-FE-229 | Front-end specification, copy |
| `20` | The app stays responsive with the seeded `9` products, `20` art pieces, `5` datasheets, `6` i... | C-CN-15 | Constraints bullet 16 |
| `${APP_PUBLIC_PORT}:4173` | The port mapping is `${APP_PUBLIC_PORT}:4173`, reading both from the environment | C-DC-02 | Deployment contract bullet 1 |
| `/api` | The HTTP API is served on the same origin under the `/api` prefix | C-DC-03 | Deployment contract bullet 2 |
| `.browser_screenshots/` | Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root, empty | C-DC-06 | Deployment contract bullet 6 |
| `.downloads/` | Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root, empty | C-DC-06 | Deployment contract bullet 6 |
| `0.0.0.0` | The app binds `0.0.0.0`, never a loopback address | C-DC-09 | Deployment contract bullet 9 |
| `GET /api/products` | `GET /api/products` takes `family`, `sort` of `name` or `recent`, `name` | C-DC-19 | Deployment contract, API shapes table |
| `sort` | `GET /api/products` takes `family`, `sort` of `name` or `recent`, `name` | C-DC-19 | Deployment contract, API shapes table |
| `GET /api/products/{slug}` | `GET /api/products/{slug}` answers one published product with `heading`, `lead`, `highlights`... | C-DC-21 | Deployment contract, API shapes table |
| `highlights` | `GET /api/products/{slug}` answers one published product with `heading`, `lead`, `highlights`... | C-DC-21 | Deployment contract, API shapes table |
| `art` | `GET /api/products/{slug}` answers one published product with `heading`, `lead`, `highlights`... | C-DC-21 | Deployment contract, API shapes table |
| `related` | `GET /api/products/{slug}` answers one published product with `heading`, `lead`, `highlights`... | C-DC-21 | Deployment contract, API shapes table |
| `GET /api/families` | `GET /api/families` answers three rows carrying `id`, `slug`, `name`, `standfirst`, `publishe... | C-DC-23 | Deployment contract, API shapes table |
| `standfirst` | `GET /api/families` answers three rows carrying `id`, `slug`, `name`, `standfirst`, `publishe... | C-DC-23 | Deployment contract, API shapes table |
| `published_count` | `GET /api/families` answers three rows carrying `id`, `slug`, `name`, `standfirst`, `publishe... | C-DC-23 | Deployment contract, API shapes table |
| `GET /api/families/{slug}` | `GET /api/families/{slug}` answers one family with `intro` plus `products`, its published pro... | C-DC-24 | Deployment contract, API shapes table |
| `intro` | `GET /api/families/{slug}` answers one family with `intro` plus `products`, its published pro... | C-DC-24 | Deployment contract, API shapes table |
| `products` | `GET /api/families/{slug}` answers one family with `intro` plus `products`, its published pro... | C-DC-24 | Deployment contract, API shapes table |
| `GET /api/industries` | `GET /api/industries` answers six rows in `sort_index` order carrying `slug`, `name`, `stat_l... | C-DC-25 | Deployment contract, API shapes table |
| `stat_line` | `GET /api/industries` answers six rows in `sort_index` order carrying `slug`, `name`, `stat_l... | C-DC-25 | Deployment contract, API shapes table |
| `customer_name` | `GET /api/industries` answers six rows in `sort_index` order carrying `slug`, `name`, `stat_l... | C-DC-25 | Deployment contract, API shapes table |
| `GET /api/customers` | `GET /api/customers` answers eight rows in `sort_index` order carrying `id`, `name` | C-DC-26 | Deployment contract, API shapes table |
| `GET /api/datasheets` | `GET /api/datasheets` answers rows carrying `id`, `title`, `page_count`, `byte_size`, `produc... | C-DC-27 | Deployment contract, API shapes table |
| `title` | `GET /api/datasheets` answers rows carrying `id`, `title`, `page_count`, `byte_size`, `produc... | C-DC-27 | Deployment contract, API shapes table |
| `byte_size` | `GET /api/datasheets` answers rows carrying `id`, `title`, `page_count`, `byte_size`, `produc... | C-DC-27 | Deployment contract, API shapes table |
| `product_name` | `GET /api/datasheets` answers rows carrying `id`, `title`, `page_count`, `byte_size`, `produc... | C-DC-27 | Deployment contract, API shapes table |
| `GET /api/art` | `GET /api/art` takes `family` as a slug with `page` counting from `1` | C-DC-28 | Deployment contract, API shapes table |
| `page` | `GET /api/art` takes `family` as a slug with `page` counting from `1` | C-DC-28 | Deployment contract, API shapes table |
| `product_slug` | `GET /api/art` answers pages of 24 rows carrying `id`, `product_slug`, `product_name`, `alt_t... | C-DC-29 | Deployment contract, API shapes table |
| `POST /api/console/write` | `POST /api/console/write` takes `region`, `key`, `value`, answering `commit_timestamp` with `... | C-DC-32 | Deployment contract, API shapes table |
| `POST /api/console/read` | `POST /api/console/read` takes `region`, `key`, `mode`, `bound`, `timestamp` | C-DC-33 | Deployment contract, API shapes table |
| `mode` | `POST /api/console/read` takes `region`, `key`, `mode`, `bound`, `timestamp` | C-DC-33 | Deployment contract, API shapes table |
| `bound` | `POST /api/console/read` takes `region`, `key`, `mode`, `bound`, `timestamp` | C-DC-33 | Deployment contract, API shapes table |
| `timestamp` | `POST /api/console/read` takes `region`, `key`, `mode`, `bound`, `timestamp` | C-DC-33 | Deployment contract, API shapes table |
| `staleness` | `POST /api/console/read` answers `value`, `timestamp`, `staleness`, `latency_ms` | C-DC-34 | Deployment contract, API shapes table |
| `latency_ms` | `POST /api/console/read` answers `value`, `timestamp`, `staleness`, `latency_ms` | C-DC-34 | Deployment contract, API shapes table |
| `POST /api/console/partition` | `POST /api/console/partition` takes `region` with `severed`, answering `regions` | C-DC-35 | Deployment contract, API shapes table |
| `regions` | `POST /api/console/partition` takes `region` with `severed`, answering `regions` | C-DC-35 | Deployment contract, API shapes table |
| `POST /api/console/reset` | `POST /api/console/reset` answers `regions`, every region unsevered | C-DC-36 | Deployment contract, API shapes table |
| `POST /api/contact` | `POST /api/contact` takes `name`, `work_email`, `company`, `region`, `interest`, `message`, a... | C-DC-37 | Deployment contract, API shapes table |
| `ok` | `POST /api/contact` takes `name`, `work_email`, `company`, `region`, `interest`, `message`, a... | C-DC-37 | Deployment contract, API shapes table |
| `enquiry_id` | `POST /api/contact` takes `name`, `work_email`, `company`, `region`, `interest`, `message`, a... | C-DC-37 | Deployment contract, API shapes table |
| `password` | `POST /api/auth/login` takes `email` with `password`, answering `access_token` with `role` | C-DC-38 | Deployment contract, API shapes table |
| `access_token` | `POST /api/auth/login` takes `email` with `password`, answering `access_token` with `role` | C-DC-38 | Deployment contract, API shapes table |
| `POST /api/auth/logout` | `POST /api/auth/logout` ends the session | C-DC-39 | Deployment contract, API shapes table |
| `GET /api/desk/products` | `GET /api/desk/products` takes `state` of `all`, `published`, `draft` | C-DC-40 | Deployment contract, API shapes table |
| `GET /api/desk/products/{id}` | `GET /api/desk/products/{id}` answers one product in either state with `art` plus `datasheet` | C-DC-43 | Deployment contract, API shapes table |
| `POST /api/desk/products` | `POST /api/desk/products` answers the created product, always `draft` | C-DC-44 | Deployment contract, API shapes table |
| `PATCH /api/desk/products/{id}` | `PATCH /api/desk/products/{id}` answers the updated product | C-DC-45 | Deployment contract, API shapes table |
| `POST /api/desk/products/{id}/publish` | `POST /api/desk/products/{id}/publish` answers the published product or a refusal naming the ... | C-DC-46 | Deployment contract, API shapes table |
| `POST /api/desk/products/{id}/unpublish` | `POST /api/desk/products/{id}/unpublish` answers the product back in `draft` | C-DC-47 | Deployment contract, API shapes table |
| `POST /api/desk/uploads` | `POST /api/desk/uploads` takes `product_id`, `kind` of `art` or `datasheet`, `filename`, `con... | C-DC-49 | Deployment contract, API shapes table |
| `kind` | `POST /api/desk/uploads` takes `product_id`, `kind` of `art` or `datasheet`, `filename`, `con... | C-DC-49 | Deployment contract, API shapes table |
| `filename` | `POST /api/desk/uploads` takes `product_id`, `kind` of `art` or `datasheet`, `filename`, `con... | C-DC-49 | Deployment contract, API shapes table |
| `content_type` | `POST /api/desk/uploads` takes `product_id`, `kind` of `art` or `datasheet`, `filename`, `con... | C-DC-49 | Deployment contract, API shapes table |
| `POST /api/desk/art` | `POST /api/desk/art` takes `product_id`, `object_key`, `alt_text`, `width`, `height`, `sort_i... | C-DC-50 | Deployment contract, API shapes table |
| `POST /api/desk/datasheets` | `POST /api/desk/datasheets` takes `product_id`, `object_key`, `title`, answering `id`, `title... | C-DC-51 | Deployment contract, API shapes table |
| `GET /api/desk/enquiries` | `GET /api/desk/enquiries` answers the stored submissions newest first, to an administrator only | C-DC-52 | Deployment contract, API shapes table |
| `GET /api/desk/views` | `GET /api/desk/views` answers `counts` entries carrying `route`, `count`, ordered by `count` ... | C-DC-53 | Deployment contract, API shapes table |
| `counts` | `GET /api/desk/views` answers `counts` entries carrying `route`, `count`, ordered by `count` ... | C-DC-53 | Deployment contract, API shapes table |
| `count` | `GET /api/desk/views` answers `counts` entries carrying `route`, `count`, ordered by `count` ... | C-DC-53 | Deployment contract, API shapes table |
| `Build on one database that spans every region and never disagrees with itself. Start with an evaluation.` | the home lead, in full | C-FE-180 | Front-end specification, copy |
| `Try it in the console` | the product console link, in full | C-FE-194 | Front-end specification, copy |
| `Nothing is in this family yet. It will fill up.` | the family empty, in full | C-FE-197 | Front-end specification, copy |
| `Read about this product` | the gallery lightbox link, in full | C-FE-202 | Front-end specification, copy |
| `That region will not accept a write it cannot safely agree on.` | the console refusal, in full | C-FE-204 | Front-end specification, copy |
| `It may have moved, or it may never have been here. The platform is still where you left it.` | the not-found body, in full | C-FE-213 | Front-end specification, copy |
| `Why Meridian Cloud` | the footer columns, in full | C-FE-214 | Front-end specification, copy |
| `Products and pricing` | the footer columns, in full | C-FE-214 | Front-end specification, copy |
| `Solutions` | the footer columns, in full | C-FE-214 | Front-end specification, copy |
| `Resources` | the footer columns, in full | C-FE-214 | Front-end specification, copy |
| `Engage` | the footer columns, in full | C-FE-214 | Front-end specification, copy |
| `That address and password do not match.` | the desk sign-in failure, in full | C-FE-219 | Front-end specification, copy |
| `Describe this image` | the desk art field label, in full | C-FE-226 | Front-end specification, copy |
| `Return this product to draft?` | the desk return confirmation, in full | C-FE-228 | Front-end specification, copy |
| `That upload did not finish. Try it again.` | the message, upload failed, in full | C-FE-232 | Front-end specification, copy |
| `Synchronized clocks with atomic and satellite time` | Tessera highlight line 2 | C-DM-49 | Data model, the highlight table |
| `Tunable read staleness when you want it` | Tessera highlight line 6 | C-DM-53 | Data model, the highlight table |
| `Relational and analytical stores that keep one answer everywhere.` | the databases standfirst | C-DM-19 | Data model, the family table |
| `The paths your data travels, kept short and private.` | the networking standfirst | C-DM-19 | Data model, the family table |
| `Questions asked of data where it already lives.` | the analytics standfirst | C-DM-19 | Data model, the family table |
| `Every database here is managed, replicated across regions and read through the same consistency guarantees.` | the databases intro | C-DM-20 | Data model, the family table |
| `Traffic stays on the platform's own network from the edge to the region that serves it.` | the networking intro | C-DM-20 | Data model, the family table |
| `Analysis runs beside the data, so a report reads the same rows the application just wrote.` | the analytics intro | C-DM-20 | Data model, the family table |
| `We put agents to work across our network and cut issue resolution from hours to minutes.` | the testimonial quote | C-DM-38 | Data model, the testimonial paragraph |
| `Published. It is live now.` | the published message | C-UF-55 | Front-end specification, copy |
| `Returned to draft. It is no longer public.` | the returned message | C-UF-57 | Front-end specification, copy |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the sha256 of the bytes inside an object key | C-DM-21 | the key scheme names the digest of the uploaded bytes, which no value can pin ahead of an upload |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 5 | 29 |
| User roles | 3 | 31 |
| Core features | 31 | 182 |
| User flow | 3 | 60 |
| UI and UX notes | 5 | 82 |
| Technical requirements | 10 | 45 |
| Data model | 3 | 67 |
| Front-end specification | 29 | 232 |
| Constraints | 1 | 15 |
| Deployment contract | 9 | 54 |
| Definition of done | 1 | 2 |

The middle column is the mechanical count of sentences carrying a modal or reporting verb. It understates the real obligation count, because a great many asks in this brief are stated as plain declaratives in a table row. Every section was read row by row and sentence by sentence, and the right-hand column is the result of that read rather than of the verb scan.

