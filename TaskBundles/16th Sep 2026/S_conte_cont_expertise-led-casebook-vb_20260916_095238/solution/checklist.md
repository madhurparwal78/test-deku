# Checklist: Expertise Led Casebook

Source: instruction.md
Sections present: overview, user roles, core features, user flow, ui and ux notes, front-end specification, technical requirements, data model, constraints, deployment contract, definition of done
Sections absent: build plan
Items: 644
Unpinned values flagged: 11

## C-OV Overview

- [ ] `C-OV-01` `capability` The site files the studio's work under four expertises, `Real Estate`, `Corporate`, `Startups`, `eCommerce`. `src: Overview`
- [ ] `C-OV-02` `capability` Each expertise has a landing page of its own. `src: Overview`
- [ ] `C-OV-03` `capability` The public site carries a work index, case study pages, a company page, a contact page, a privacy notice. `src: Overview`
- [ ] `C-OV-04` `constraint` The product has no blog, no article, no career page, no cart, no payment, no search box, no comment thread on a case study, no rating. `src: Overview`
- [ ] `C-OV-05` `constraint` Nothing on the public site changes during a visit to the page. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor reads every published page without an account. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An anonymous visitor is denied every studio route. `src: User roles table row 1`
- [ ] `C-RL-03` `role` Signup always creates an account whose role is `visitor`. `src: User roles`
- [ ] `C-RL-04` `role` A `visitor` session is denied every studio endpoint. `src: User roles table row 2`
- [ ] `C-RL-05` `role` An `editor` reads every case study, draft or published. `src: User roles table row 3`
- [ ] `C-RL-06` `role` An `editor` creates case studies. `src: User roles table row 3`
- [ ] `C-RL-07` `role` An `editor` edits case studies. `src: User roles table row 3`
- [ ] `C-RL-08` `role` An `editor` sets a cover on a case study. `src: User roles table row 3`
- [ ] `C-RL-09` `role` An `editor` is denied publishing a case study. `src: User roles table row 3`
- [ ] `C-RL-10` `role` An `editor` is denied unpublishing a case study. `src: User roles table row 3`
- [ ] `C-RL-11` `role` An `editor` is denied deleting a case study. `src: User roles table row 3`
- [ ] `C-RL-12` `role` An `editor` is denied reordering the shelf. `src: User roles table row 3`
- [ ] `C-RL-13` `role` An `editor` is denied filling a feature slot. `src: User roles table row 3`
- [ ] `C-RL-14` `role` An `editor` is denied reading a brief. `src: User roles table row 3`
- [ ] `C-RL-15` `role` An `editor` is denied changing a brief. `src: User roles table row 3`
- [ ] `C-RL-16` `role` An `editor` is denied the page-view log. `src: User roles table row 3`
- [ ] `C-RL-17` `role` An `editor` sees no unread brief count. `src: User roles table row 3`
- [ ] `C-RL-18` `role` An `editor` sees the sessions of the editor's own account. `src: User roles table row 3`
- [ ] `C-RL-19` `role` The `owner` publishes case studies. `src: User roles table row 4`
- [ ] `C-RL-20` `role` The `owner` unpublishes case studies. `src: User roles table row 4`
- [ ] `C-RL-21` `role` The `owner` deletes case studies. `src: User roles table row 4`
- [ ] `C-RL-22` `role` The `owner` reads briefs. `src: User roles table row 4`
- [ ] `C-RL-23` `role` The `owner` archives briefs. `src: User roles table row 4`
- [ ] `C-RL-24` `role` The `owner` deletes briefs. `src: User roles table row 4`
- [ ] `C-RL-25` `role` Exactly one account holds the role `owner`. `src: User roles table row 4`
- [ ] `C-RL-26` `role` A refused call from an `editor` session leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-27` `role` A refused call from a `visitor` session leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-28` `role` A refused call with no session leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-29` `role` Signup never creates an `owner` or an `editor` account. `src: User roles`
- [ ] `C-RL-30` `literal` The seeded account `owner@example.com` holds the role `owner` under the display name `Mara Lind`. `src: User roles seeded accounts row 1`
- [ ] `C-RL-31` `literal` The seeded account `editor@example.com` holds the role `editor` under the display name `Jonas Weller`. `src: User roles seeded accounts row 2`
- [ ] `C-RL-32` `literal` The seeded account `visitor@example.com` holds the role `visitor`. `src: User roles seeded accounts row 3`
- [ ] `C-RL-33` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` A draft case study is absent from the public work list. `src: Core features rule 1`
- [ ] `C-CF-02` `capability` A draft case study is absent from every expertise landing. `src: Core features rule 1`
- [ ] `C-CF-03` `capability` A draft case study is absent from the front page. `src: Core features rule 1`
- [ ] `C-CF-04` `capability` A draft case study is absent from the sitemap. `src: Core features rule 1`
- [ ] `C-CF-05` `capability` A draft case study is absent from every next link of another case study. `src: Core features rule 1`
- [ ] `C-CF-06` `capability` A public request for a draft case study address answers not found. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` The not found answer for a draft reveals nothing about the draft. `src: Core features rule 1`
- [ ] `C-CF-08` `role` A draft cover's bytes are refused to everyone not signed in as `owner` or `editor`. `src: Core features rule 1`
- [ ] `C-CF-09` `capability` Publishing makes the listing, the address, the cover readable in one act. `src: Core features rule 1`
- [ ] `C-CF-10` `literal` The seeded draft `Pinemark Mobile App` makes `/work/pinemark-mobile-app` answer not found. `src: Core features rule 1`
- [ ] `C-CF-11` `capability` Unpublishing takes a case study off every public list at once. `src: Core features rule 2`
- [ ] `C-CF-12` `capability` Unpublishing makes the case study cover private again. `src: Core features rule 2`
- [ ] `C-CF-13` `capability` A withdrawn case study address answers gone with the line `No longer here`. `src: Core features rule 2`
- [ ] `C-CF-14` `literal` The seeded withdrawn `Ostend Loyalty Store` makes `/work/ostend-loyalty-store` answer gone. `src: Core features rule 2`
- [ ] `C-CF-15` `capability` A publish without an expertise is refused with `Choose an expertise before publishing.` `src: Core features rule 3`
- [ ] `C-CF-16` `capability` A publish without a tag is refused with `Add at least one tag before publishing.` `src: Core features rule 3`
- [ ] `C-CF-17` `capability` A publish without a cover is refused with `Add a cover before publishing.` `src: Core features rule 3`
- [ ] `C-CF-18` `capability` A publish missing several things names the first missing one, in the order expertise, tag, cover. `src: Core features rule 3`
- [ ] `C-CF-19` `capability` A publish needs the cover to carry alternative text. `src: Core features rule 3`
- [ ] `C-CF-20` `constraint` A refused publish changes nothing. `src: Core features rule 3`
- [ ] `C-CF-21` `constraint` Saving a case study never publishes the case study. `src: Core features rule 3`
- [ ] `C-CF-22` `capability` Every cover is a PNG stored as an object in `minio`. `src: Core features rule 4`
- [ ] `C-CF-23` `constraint` The product offers no upload of any kind. `src: Core features rule 4`
- [ ] `C-CF-24` `literal` The cover object key follows `covers/{case_study_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 4`
- [ ] `C-CF-25` `capability` The control `Generate cover` draws a cover from the cover seed in the chosen palette. `src: Core features rule 4`
- [ ] `C-CF-26` `capability` The control `Generate cover` draws from the saved cover seed with the saved palette. `src: Core features rule 4`
- [ ] `C-CF-27` `ui` Changing the cover seed or palette in the editor saves the case study before a cover is drawn. `src: Core features rule 4`
- [ ] `C-CF-28` `literal` The cover seed is a whole number from `0` to `999999`. `src: Core features rule 4`
- [ ] `C-CF-29` `literal` The cover palette is one of `mono`, `warm`, `cool`. `src: Core features rule 4`
- [ ] `C-CF-30` `capability` The same cover seed with the same palette draws the same cover bytes. `src: Core features rule 4`
- [ ] `C-CF-31` `data` Every cover row records the intrinsic width, height of the cover image. `src: Core features rule 4`
- [ ] `C-CF-32` `data` Every cover row records the cover's alternative text. `src: Core features rule 4`
- [ ] `C-CF-33` `capability` A cover request without alternative text is refused. `src: Core features rule 4`
- [ ] `C-CF-34` `capability` Generating twice from one seed with one palette for one case study resolves to one object. `src: Core features rule 4`
- [ ] `C-CF-35` `data` Every case study carries a whole-number `version` starting at `1`. `src: Core features rule 5`
- [ ] `C-CF-36` `data` Every feature slot carries a whole-number `version` starting at `1`. `src: Core features rule 5`
- [ ] `C-CF-37` `capability` An accepted write raises the stored version by one. `src: Core features rule 5`
- [ ] `C-CF-38` `capability` Setting a cover, publishing, unpublishing each raise the case study version by one. `src: Core features rule 5`
- [ ] `C-CF-39` `capability` A write sending an older version is refused as a conflict, carrying the conflict message about a change made somewhere else. `src: Core features rule 5`
- [ ] `C-CF-40` `literal` The conflict message reads `changed somewhere else` ending `you were working.` `src: Core features rule 5`
- [ ] `C-CF-41` `capability` A case study, slot or shelf write sending no version is refused as a conflict, carrying the conflict message. `src: Core features rule 5`
- [ ] `C-CF-42` `constraint` A write refused as a conflict changes nothing. `src: Core features rule 5`
- [ ] `C-CF-43` `capability` Two concurrent writes from the same version admit exactly one. `src: Core features rule 5`
- [ ] `C-CF-44` `constraint` Nothing is merged automatically. `src: Core features rule 5`
- [ ] `C-CF-45` `ui` The studio shows a conflict in place with `Keep mine`, `Take theirs`, writing nothing until the person chooses. `src: Core features rule 5`
- [ ] `C-CF-46` `capability` A repeated case study create with one `Idempotency-Key` within 24 hours creates one case study. `src: Core features rule 6`
- [ ] `C-CF-47` `capability` A repeated brief with one `Idempotency-Key` within 24 hours creates one brief. `src: Core features rule 6`
- [ ] `C-CF-48` `capability` A repeated create with the same idempotency key returns the first answer. `src: Core features rule 6`
- [ ] `C-CF-49` `capability` The public work list follows shelf order, never recency. `src: Core features rule 7`
- [ ] `C-CF-50` `capability` Every expertise landing lists case studies in shelf order. `src: Core features rule 7`
- [ ] `C-CF-51` `capability` The next link of a case study follows shelf order. `src: Core features rule 7`
- [ ] `C-CF-52` `capability` The owner reorders the shelf at `/studio/shelf`. `src: Core features rule 7`
- [ ] `C-CF-53` `ui` A shelf row moves by dragging. `src: Core features rule 7`
- [ ] `C-CF-54` `ui` A shelf row moves from the keyboard with the arrow keys on the row's handle. `src: Core features rule 7`
- [ ] `C-CF-55` `ui` A saved reorder shows `Order saved.` `src: Core features rule 7`
- [ ] `C-CF-56` `ui` A reorder is applied optimistically before the server answers. `src: Core features rule 7`
- [ ] `C-CF-57` `capability` A shelf reorder names every case study once. `src: Core features rule 7`
- [ ] `C-CF-58` `capability` A shelf reorder carries the shelf `version` read before the reorder. `src: Core features rule 7`
- [ ] `C-CF-59` `capability` A shelf reorder sent with an older shelf version is refused, the saved order unchanged. `src: Core features rule 7`
- [ ] `C-CF-60` `capability` A shelf reorder sent with no shelf version is refused, the saved order unchanged. `src: Core features rule 7`
- [ ] `C-CF-61` `capability` A shelf reorder refused for an older or missing shelf version shows the conflict line, then `The order changed. Yours was not saved.` `src: Core features rule 7`
- [ ] `C-CF-62` `ui` A shelf reorder refused for an older or missing shelf version offers `Keep mine` with `Take theirs`, the rows animating back to the saved order. `src: Core features rule 7`
- [ ] `C-CF-63` `capability` An accepted shelf reorder raises the shelf version by one. `src: Core features rule 7`
- [ ] `C-CF-64` `capability` A shelf reorder leaves every case study `version` as before. `src: Core features rule 7`
- [ ] `C-CF-65` `capability` A withdrawn case study keeps the withdrawn case study's shelf place. `src: Core features rule 7`
- [ ] `C-CF-66` `capability` Publishing a withdrawn case study again returns the case study to the kept shelf place. `src: Core features rule 7`
- [ ] `C-CF-67` `capability` A new case study joins the end of the shelf. `src: Core features rule 7`
- [ ] `C-CF-68` `capability` The front page shows exactly two slots under each expertise. `src: Core features rule 8`
- [ ] `C-CF-69` `constraint` The front page shows the owner's slot choices, never the two most recent case studies. `src: Core features rule 8`
- [ ] `C-CF-70` `literal` There are `8` feature slots, two per expertise. `src: Core features rule 8`
- [ ] `C-CF-71` `constraint` A feature slot refuses a case study that is not published. `src: Core features rule 8`
- [ ] `C-CF-72` `constraint` A feature slot refuses a case study of another expertise. `src: Core features rule 8`
- [ ] `C-CF-73` `constraint` A case study holds at most one feature slot. `src: Core features rule 8`
- [ ] `C-CF-74` `capability` A feature slot may hold nothing. `src: Core features rule 8`
- [ ] `C-CF-75` `ui` Filling a slot shows `Featured on the home page.` `src: Core features rule 8`
- [ ] `C-CF-76` `ui` Emptying a slot shows `No longer featured. Still published.` `src: Core features rule 8`
- [ ] `C-CF-77` `capability` The case study replaced in a feature slot stays published. `src: Core features rule 8`
- [ ] `C-CF-78` `capability` The case study replaced in a feature slot stays on the public work list. `src: Core features rule 8`
- [ ] `C-CF-79` `constraint` Writing a feature slot never writes to a case study row. `src: Core features rule 8`
- [ ] `C-CF-80` `ui` The front page opens on the flat pale grey with the headline `Design.`, `Development.`, `Mastership.` `src: Core features rule 9`
- [ ] `C-CF-81` `ui` The third headline line on the front page is set in white. `src: Core features rule 9`
- [ ] `C-CF-82` `ui` The front page carries the statement about `exceptional digital products & services, eCommerce,` with the circle cluster. `src: Core features rule 9`
- [ ] `C-CF-83` `ui` The bar `Select an expertise` jumps down the front page, not acting as a filter. `src: Core features rule 9`
- [ ] `C-CF-84` `ui` The showreel panel on the front page is labelled `Watch`, `Showreel`. `src: Core features rule 9`
- [ ] `C-CF-85` `ui` Each expertise band carries a number in a circle from `01` to `04`. `src: Core features rule 9`
- [ ] `C-CF-86` `capability` Each expertise band carries the expertise name with the expertise sentence. `src: Core features rule 9`
- [ ] `C-CF-87` `ui` Each expertise band carries a `Learn More` control leading to the expertise landing. `src: Core features rule 9`
- [ ] `C-CF-88` `capability` Each expertise band shows the two featured case studies side by side. `src: Core features rule 9`
- [ ] `C-CF-89` `ui` An empty feature slot shows nothing in the front page band. `src: Core features rule 9`
- [ ] `C-CF-90` `constraint` The front page band never fills an empty slot with a recent case study. `src: Core features rule 9`
- [ ] `C-CF-91` `ui` The front page carries `Our Capabilities` with five items. `src: Core features rule 9`
- [ ] `C-CF-92` `ui` The company band shows `20+` over `Years of experience` with `More About Us`. `src: Core features rule 9`
- [ ] `C-CF-93` `ui` The dark client strip holds seven client names a visitor drags sideways. `src: Core features rule 9`
- [ ] `C-CF-94` `ui` Pointing at a client name reveals a paragraph. `src: Core features rule 9`
- [ ] `C-CF-95` `capability` The work index shows every published case study. `src: Core features rule 10`
- [ ] `C-CF-96` `ui` The work index lays the cards out in two columns. `src: Core features rule 10`
- [ ] `C-CF-97` `constraint` The work index has no paging. `src: Core features rule 10`
- [ ] `C-CF-98` `ui` A work card shows the cover at twice as wide as tall. `src: Core features rule 10`
- [ ] `C-CF-99` `ui` A work card shows the case study title. `src: Core features rule 10`
- [ ] `C-CF-100` `ui` A work card shows the tags joined by a comma with a space. `src: Core features rule 10`
- [ ] `C-CF-101` `ui` The filter chip row scrolls sideways, never wrapping. `src: Core features rule 10`
- [ ] `C-CF-102` `ui` The chip `All Works` comes first, clearing every filter. `src: Core features rule 10`
- [ ] `C-CF-103` `ui` The filter row offers the four expertises, then an `Industries` group of eleven tags. `src: Core features rule 10`
- [ ] `C-CF-104` `capability` The work filter lives in the address as `?expertise=<slug>` with a repeatable `&tag=<slug>`. `src: Core features rule 10`
- [ ] `C-CF-105` `capability` Two tag filters show case studies carrying either tag. `src: Core features rule 10`
- [ ] `C-CF-106` `capability` An expertise filter with a tag filter shows case studies carrying both. `src: Core features rule 10`
- [ ] `C-CF-107` `capability` An unknown filter value is dropped from the work filter. `src: Core features rule 10`
- [ ] `C-CF-108` `ui` The address is rewritten without an unknown filter value. `src: Core features rule 10`
- [ ] `C-CF-109` `ui` The back button undoes a work filter. `src: Core features rule 10`
- [ ] `C-CF-110` `ui` A reload keeps the work filter. `src: Core features rule 10`
- [ ] `C-CF-111` `ui` A work filter matching nothing shows `Nothing matches that.`, the active filters, `Clear filters`. `src: Core features rule 10`
- [ ] `C-CF-112` `capability` Filtering on the `Real Estate` tag never filters on the `Real Estate` expertise. `src: Core features rule 10`
- [ ] `C-CF-113` `capability` Filtering on the `Real Estate` expertise never filters on the `Real Estate` tag. `src: Core features rule 10`
- [ ] `C-CF-114` `ui` A case study page opens with the case study title set very large. `src: Core features rule 11`
- [ ] `C-CF-115` `ui` A case study page shows a breadcrumb trail. `src: Core features rule 11`
- [ ] `C-CF-116` `ui` A case study page shows the client with the year. `src: Core features rule 11`
- [ ] `C-CF-117` `ui` The cover runs the full width of the case study page. `src: Core features rule 11`
- [ ] `C-CF-118` `capability` A case study page shows the case study body blocks. `src: Core features rule 11`
- [ ] `C-CF-119` `capability` A case study page shows the next published case study in the whole shelf order, whatever filter the visitor came from. `src: Core features rule 11`
- [ ] `C-CF-120` `capability` The next case study wraps from the last case study back to the first. `src: Core features rule 11`
- [ ] `C-CF-121` `literal` The body block kinds are `paragraph`, `heading`, `image`, `image_pair`, `quote`, `facts`. `src: Core features rule 11`
- [ ] `C-CF-122` `constraint` A seventh block kind is refused when a case study is saved. `src: Core features rule 11`
- [ ] `C-CF-123` `ui` Going back to the work index returns the visitor to the same place in the list. `src: Core features rule 11`
- [ ] `C-CF-124` `literal` The four landings are `/expertise/real-estate`, `/expertise/corporate`, `/expertise/startups`, `/expertise/ecommerce`. `src: Core features rule 12`
- [ ] `C-CF-125` `ui` An expertise landing opens on the pale grey with the expertise name set enormous, the circle cluster shown. `src: Core features rule 12`
- [ ] `C-CF-126` `ui` An expertise landing shows the expertise sentence under the opening. `src: Core features rule 12`
- [ ] `C-CF-127` `capability` An expertise landing lists every published case study of the landing's expertise. `src: Core features rule 12`
- [ ] `C-CF-128` `ui` An expertise landing ends with an invitation to get in touch. `src: Core features rule 12`
- [ ] `C-CF-129` `literal` The contact page carries `We operate worldwide. Choose the office nearest to you`. `src: Core features rule 13`
- [ ] `C-CF-130` `literal` The contact page lists the offices `Riga, Latvia`, `Oslo, Norway`. `src: Core features rule 13`
- [ ] `C-CF-131` `ui` The brief form carries the heading `Get in touch`. `src: Core features rule 13`
- [ ] `C-CF-132` `ui` The brief form fields run `Your name`, `Company name`, `Phone number`, `E-mail`, `Comment` in order. `src: Core features rule 13`
- [ ] `C-CF-133` `ui` The brief form marks `Company name` with `(optional)`. `src: Core features rule 13`
- [ ] `C-CF-134` `ui` The brief form offers an optional choice of expertise. `src: Core features rule 13`
- [ ] `C-CF-135` `literal` The brief budget values are `under_25k`, `25k_to_75k`, `75k_to_150k`, `over_150k`, all optional. `src: Core features rule 13`
- [ ] `C-CF-136` `ui` The budget choices show to the visitor as `Under 25k`, `25k to 75k`, `75k to 150k`, `Over 150k`. `src: Core features rule 13`
- [ ] `C-CF-137` `capability` A brief naming an unknown expertise is refused under the expertise field with `Choose one of the listed expertises.` `src: Core features rule 13`
- [ ] `C-CF-138` `capability` A brief naming an unknown budget is refused under the budget field with `Choose one of the listed budgets.` `src: Core features rule 13`
- [ ] `C-CF-139` `capability` A comment breaking both comment rules shows only `A few more words, please.` `src: Core features rule 13`
- [ ] `C-CF-140` `capability` A brief without a phone, an expertise or a budget is accepted. `src: Core features rule 13 table row 3`
- [ ] `C-CF-141` `literal` The brief form carries the consent line `By clicking the Submit button you agree to our Privacy Policy terms`. `src: Core features rule 13`
- [ ] `C-CF-142` `ui` The brief form ends with the large round `Submit` button. `src: Core features rule 13`
- [ ] `C-CF-143` `ui` The phone field formats the number as the number is typed. `src: Core features rule 13`
- [ ] `C-CF-144` `data` A stored brief phone keeps only digits with an optional leading plus. `src: Core features rule 13`
- [ ] `C-CF-145` `ui` The phone field never moves the caret backwards. `src: Core features rule 13`
- [ ] `C-CF-146` `capability` A brief with an empty name is refused with `Tell us what to call you.` `src: Core features rule 13 table row 1`
- [ ] `C-CF-147` `literal` A brief company runs `0` to `120` characters. `src: Core features rule 13 table row 2`
- [ ] `C-CF-148` `capability` A brief phone with fewer than six digits is refused with `That number looks incomplete.` `src: Core features rule 13 table row 3`
- [ ] `C-CF-149` `literal` A brief phone, when given, holds `6` to `20` digits. `src: Core features rule 13 table row 3`
- [ ] `C-CF-150` `capability` A brief with an invalid email is refused with `That address will not reach you.` `src: Core features rule 13 table row 4`
- [ ] `C-CF-151` `capability` A brief email has one at sign with text either side, holding no spaces. `src: Core features rule 13 table row 4`
- [ ] `C-CF-152` `capability` A brief comment under ten characters is refused with `A few more words, please.` `src: Core features rule 13 table row 5`
- [ ] `C-CF-153` `capability` A brief comment with more than two web addresses is refused with `Fewer links, please.` `src: Core features rule 13 table row 6`
- [ ] `C-CF-154` `literal` A brief name runs `1` to `80` characters. `src: Core features rule 13 table row 1`
- [ ] `C-CF-155` `capability` A brief name is measured after trimming surrounding spaces. `src: Core features rule 13 table row 1`
- [ ] `C-CF-156` `literal` A brief comment runs `10` to `4000` characters. `src: Core features rule 13 table row 5`
- [ ] `C-CF-157` `capability` A brief comment is measured after trimming surrounding spaces. `src: Core features rule 13 table row 5`
- [ ] `C-CF-158` `literal` A brief email runs `1` to `254` characters. `src: Core features rule 13 table row 4`
- [ ] `C-CF-159` `capability` The server enforces every brief field rule, not only the page. `src: Core features rule 13`
- [ ] `C-CF-160` `ui` Pressing `Submit` on an empty brief form shows every message under the failing field. `src: Core features rule 13`
- [ ] `C-CF-161` `ui` No button anywhere in the product is ever greyed out. `src: Core features rule 13`
- [ ] `C-CF-162` `ui` A refused brief leaves every field holding the typed value. `src: Core features rule 13`
- [ ] `C-CF-163` `ui` An accepted brief replaces the form in place with `Thank you!`, `We'll be in touch soonest!`, `Homepage`. `src: Core features rule 13`
- [ ] `C-CF-164` `capability` An accepted brief records the page the visitor was on as `source_path`. `src: Core features rule 13`
- [ ] `C-CF-165` `capability` A brief whose hidden `website` field is filled is spam that stores nothing. `src: Core features rule 14`
- [ ] `C-CF-166` `capability` A brief whose `form_token` is under two seconds old is spam that stores nothing. `src: Core features rule 14`
- [ ] `C-CF-167` `capability` A brief with no `form_token` is spam that stores nothing. `src: Core features rule 14`
- [ ] `C-CF-168` `capability` A brief whose `form_token` the server never issued is spam that stores nothing. `src: Core features rule 14`
- [ ] `C-CF-169` `capability` A brief reusing a `form_token` already used is spam that stores nothing. `src: Core features rule 14`
- [ ] `C-CF-170` `capability` A spam brief gets the same answer an accepted brief gets. `src: Core features rule 14`
- [ ] `C-CF-171` `capability` The route `GET /api/briefs/token` issues the brief `form_token`. `src: Core features rule 14`
- [ ] `C-CF-172` `capability` A fourth brief from one e-mail address within one hour is refused. `src: Core features rule 14`
- [ ] `C-CF-173` `constraint` The brief rate limit refusal names no limit. `src: Core features rule 14`
- [ ] `C-CF-174` `constraint` The brief form asks no puzzle, no image challenge. `src: Core features rule 14`
- [ ] `C-CF-175` `capability` An accepted brief lands in the brief inbox as `unread`. `src: Core features rule 15`
- [ ] `C-CF-176` `role` Only the `owner` reaches the brief inbox at `/studio/inbox`. `src: Core features rule 15`
- [ ] `C-CF-177` `ui` An inbox row shows the sender name with the company. `src: Core features rule 15`
- [ ] `C-CF-178` `ui` An inbox row shows the chosen expertise with the chosen budget. `src: Core features rule 15`
- [ ] `C-CF-179` `ui` An inbox row shows the first comment line with the arrival time. `src: Core features rule 15`
- [ ] `C-CF-180` `capability` The brief inbox lists briefs newest first. `src: Core features rule 15`
- [ ] `C-CF-181` `ui` Unread inbox rows show at full strength with read rows faded. `src: Core features rule 15`
- [ ] `C-CF-182` `ui` At a wide window the inbox list sits beside the opened brief. `src: Core features rule 15`
- [ ] `C-CF-183` `capability` An opened brief has an address of the form `/studio/inbox/<id>`. `src: Core features rule 15`
- [ ] `C-CF-184` `ui` An opened brief shows the whole comment, the phone, the email, the source page. `src: Core features rule 15`
- [ ] `C-CF-185` `ui` An opened brief offers `Archive`, `Mark unread`, `Delete`, `Reply`. `src: Core features rule 15`
- [ ] `C-CF-186` `ui` The control `Reply` opens a mail composition to the brief sender. `src: Core features rule 15`
- [ ] `C-CF-187` `capability` Opening a brief in the inbox marks the brief `read`. `src: Core features rule 15`
- [ ] `C-CF-188` `capability` Reading a brief through `GET /api/studio/briefs/{id}` leaves the brief state unchanged. `src: Core features rule 15`
- [ ] `C-CF-189` `capability` An archived brief becomes `archived`. `src: Core features rule 15`
- [ ] `C-CF-190` `capability` A brief comment is stored exactly as typed. `src: Core features rule 15`
- [ ] `C-CF-191` `ui` The inbox shows a brief comment exactly as typed, a typed tag appearing as plain characters. `src: Core features rule 15`
- [ ] `C-CF-192` `constraint` No link in a brief comes alive in the inbox, no picture in a brief loads. `src: Core features rule 15`
- [ ] `C-CF-193` `literal` The seeded brief from `Ines Duval` carries markup in the brief comment. `src: Core features rule 15`
- [ ] `C-CF-194` `ui` The studio rail shows the unread count beside `Inbox`. `src: Core features rule 15`
- [ ] `C-CF-195` `ui` A brief arriving with the inbox open appears at the top without the list scrolling. `src: Core features rule 15`
- [ ] `C-CF-196` `ui` The unread count beside `Inbox` rises without a reload. `src: Core features rule 15`
- [ ] `C-CF-197` `constraint` The unread count with the inbox list are the only real-time parts of the product. `src: Core features rule 15`
- [ ] `C-CF-198` `ui` The dashboard shows the tiles `Published work`, `Drafts` to everyone signed in. `src: Core features rule 16`
- [ ] `C-CF-199` `capability` The dashboard counts published case studies separately from draft case studies. `src: Core features rule 16`
- [ ] `C-CF-200` `capability` The owner dashboard carries the unread brief count as `unread_briefs`. `src: Core features rule 16`
- [ ] `C-CF-201` `capability` An editor dashboard carries no unread brief count at all. `src: Core features rule 16`
- [ ] `C-CF-202` `ui` An editor dashboard shows no `Unread briefs` tile. `src: Core features rule 16`
- [ ] `C-CF-203` `ui` The dashboard lists the ten most recently changed case studies with briefs, newest first. `src: Core features rule 16`
- [ ] `C-CF-204` `ui` Each dashboard recent row links to the item the row names. `src: Core features rule 16`
- [ ] `C-CF-205` `capability` An editor dashboard recent list carries case studies only. `src: Core features rule 16`
- [ ] `C-CF-206` `data` Each dashboard `recent` row carries `kind`, `id`, `title`, `changed_at`. `src: Core features rule 16`
- [ ] `C-CF-207` `literal` A dashboard `recent` row `kind` is `case_study` or `brief`. `src: Core features rule 16`
- [ ] `C-CF-208` `capability` The case study editor lives at `/studio/work/new`, `/studio/work/<id>` as dedicated routes. `src: Core features rule 17`
- [ ] `C-CF-209` `literal` A case study title runs `1` to `120` characters. `src: Core features rule 17`
- [ ] `C-CF-210` `capability` A case study slug is derived from the title, editable afterwards. `src: Core features rule 17`
- [ ] `C-CF-211` `constraint` A case study slug is lowercase words joined by hyphens, unique. `src: Core features rule 17`
- [ ] `C-CF-212` `literal` A case study client runs `0` to `80` characters. `src: Core features rule 17`
- [ ] `C-CF-213` `literal` A case study year is four digits from `1990` to the current year. `src: Core features rule 17`
- [ ] `C-CF-214` `literal` A case study summary runs `0` to `280` characters. `src: Core features rule 17`
- [ ] `C-CF-215` `ui` The editor offers a shuffle control for the cover seed. `src: Core features rule 17`
- [ ] `C-CF-216` `ui` A block is added by pressing a plus between blocks, choosing one of the six kinds. `src: Core features rule 17`
- [ ] `C-CF-217` `constraint` A block is never dragged in from a palette. `src: Core features rule 17`
- [ ] `C-CF-218` `ui` The whole case study editor works from the keyboard. `src: Core features rule 17`
- [ ] `C-CF-219` `ui` Pressing `Save` shows `Saved just now.` `src: Core features rule 17`
- [ ] `C-CF-220` `ui` The controls `Publish`, `Unpublish` appear for the owner only. `src: Core features rule 17`
- [ ] `C-CF-221` `ui` Publishing shows the status line beginning `Published.` `src: Core features rule 17`
- [ ] `C-CF-222` `ui` Unpublishing shows the status line beginning `Unpublished.` `src: Core features rule 17`
- [ ] `C-CF-223` `ui` A server refusal puts the server message under the failing field, moving focus there. `src: Core features rule 17`
- [ ] `C-CF-224` `capability` A case study slug is kept when the title changes. `src: Core features rule 17`
- [ ] `C-CF-225` `capability` A slug already in use is refused with `That address is already used by another case study.` `src: Core features rule 17`
- [ ] `C-CF-226` `capability` A wrong address or password at sign in is refused with the line beginning `That did not match.` `src: Core features rule 18`
- [ ] `C-CF-227` `constraint` The sign in refusal never names the wrong half. `src: Core features rule 18`
- [ ] `C-CF-228` `capability` Five failed sign ins in a row lock the account for fifteen minutes. `src: Core features rule 18`
- [ ] `C-CF-229` `capability` A locked account refuses the right password with a line beginning `Too many attempts.` `src: Core features rule 18`
- [ ] `C-CF-230` `capability` A signed-out request for a studio route goes to `/sign-in?next=` followed by the intended path. `src: Core features rule 18`
- [ ] `C-CF-231` `capability` After signing in the person lands on the intended studio path. `src: Core features rule 18`
- [ ] `C-CF-232` `capability` A return path other than one leading slash with a studio route lands on `/studio`. `src: Core features rule 18`
- [ ] `C-CF-233` `ui` The account page lists every live session with a browser description, start time, last use. `src: Core features rule 19`
- [ ] `C-CF-234` `ui` The account page marks the current session. `src: Core features rule 19`
- [ ] `C-CF-235` `ui` The account page carries the note beginning `A revoked session ends`. `src: Core features rule 19`
- [ ] `C-CF-236` `capability` The route `GET /api/sessions` lists the live sessions of the signed-in account. `src: Core features rule 19`
- [ ] `C-CF-237` `data` Each session carries `id`, `user_agent_summary`, `created_at`, `last_seen_at`, `current`. `src: Core features rule 19`
- [ ] `C-CF-238` `capability` The `current` flag is true for the session making the request. `src: Core features rule 19`
- [ ] `C-CF-239` `capability` The control `Sign out everywhere` ends every session of the account, the current session included. `src: Core features rule 19`
- [ ] `C-CF-240` `ui` The control `Sign out everywhere` asks the person to type to confirm. `src: Core features rule 19`
- [ ] `C-CF-241` `ui` A role-refused studio route shows a designed page with `403`, `Not permitted`, `Back to studio`. `src: Core features rule 20`
- [ ] `C-CF-242` `ui` The refusal page sits inside the site's own frame, never a redirect, never blank. `src: Core features rule 20`
- [ ] `C-CF-243` `ui` The refusal page keeps the studio rail minus the items the role cannot reach. `src: Core features rule 20`
- [ ] `C-CF-244` `ui` The inbox refusal page adds `Briefs are visible to the owner only.` `src: Core features rule 20`
- [ ] `C-CF-245` `capability` An unknown address answers not found. `src: Core features rule 21`
- [ ] `C-CF-246` `ui` The not found page sits inside the site's own frame. `src: Core features rule 21`
- [ ] `C-CF-247` `ui` The not found page shows `404` as large as the front page headline with `Not found`, `Back to work`. `src: Core features rule 21`
- [ ] `C-CF-248` `constraint` The not found page never prints the requested path. `src: Core features rule 21`
- [ ] `C-CF-249` `ui` The gone surface reads `410`, `No longer here`, `Back to work`. `src: Core features rule 21`
- [ ] `C-CF-250` `ui` The privacy notice at `/privacy-policy` states that each public page view is kept as the route with the time. `src: Core features rule 21`
- [ ] `C-CF-251` `ui` The privacy notice states that the site keeps what a brief's sender typed. `src: Core features rule 21`
- [ ] `C-CF-252` `ui` The privacy notice states that the cookie choice stays in the visitor's own browser. `src: Core features rule 21`
- [ ] `C-CF-253` `ui` The privacy notice ends without an invitation to get in touch. `src: Core features rule 21`
- [ ] `C-CF-254` `capability` Every public route view records one page view row with the route, the time. `src: Core features rule 22`
- [ ] `C-CF-255` `constraint` A page view reported for a studio route is accepted, stored nowhere. `src: Core features rule 22`
- [ ] `C-CF-256` `role` Only the `owner` reads the page-view log. `src: Core features rule 22`
- [ ] `C-CF-257` `capability` The page-view log lists views newest first. `src: Core features rule 22`
- [ ] `C-CF-258` `constraint` A page view records nothing beyond the route, the time. `src: Core features rule 22`
- [ ] `C-CF-259` `capability` Every public route sets a title of the route's own. `src: Core features rule 23`
- [ ] `C-CF-260` `capability` Every public route sets a description of the route's own. `src: Core features rule 23`
- [ ] `C-CF-261` `constraint` No two public routes share a title or a description. `src: Core features rule 23`
- [ ] `C-CF-262` `capability` The front page title is `Digital Product Design & Development Agency | Northform`. `src: Core features rule 23`
- [ ] `C-CF-263` `capability` The work index title is `Work | Northform`. `src: Core features rule 23`
- [ ] `C-CF-264` `ui` A case study page title is the case study title followed by ` | Northform`. `src: Core features rule 23`
- [ ] `C-CF-265` `ui` An expertise landing title is the expertise name followed by ` | Northform`. `src: Core features rule 23`
- [ ] `C-CF-266` `capability` The company page title is `Company | Northform`. `src: Core features rule 23`
- [ ] `C-CF-267` `capability` The contact page title is `Northform's Contact Details | Northform`. `src: Core features rule 23`
- [ ] `C-CF-268` `capability` The privacy page title is `Privacy Policy | Northform`. `src: Core features rule 23`
- [ ] `C-CF-269` `ui` The studio title is `Studio | Northform`. `src: Core features rule 23`
- [ ] `C-CF-270` `capability` The file `/sitemap.xml` lists every public route with every published case study, every landing. `src: Core features rule 23`
- [ ] `C-CF-271` `constraint` The file `/sitemap.xml` lists no draft case study, no withdrawn case study. `src: Core features rule 23`
- [ ] `C-CF-272` `capability` The file `/robots.txt` names the sitemap. `src: Core features rule 23`
- [ ] `C-CF-273` `capability` The file `/robots.txt` keeps crawlers out of `/studio`. `src: Core features rule 23`
- [ ] `C-CF-274` `capability` Every content image carries alternative text. `src: Core features rule 24`
- [ ] `C-CF-275` `capability` A cover's alternative text is the text the case study author wrote. `src: Core features rule 24`
- [ ] `C-CF-276` `ui` A client name image carries the client name as alternative text. `src: Core features rule 24`
- [ ] `C-CF-277` `ui` A decorative mark declares the mark decorative, hidden from assistive technology. `src: Core features rule 24`
- [ ] `C-CF-278` `ui` The circle cluster is hidden from assistive technology. `src: Core features rule 24`
- [ ] `C-CF-279` `ui` The generated loops are hidden from assistive technology. `src: Core features rule 24`
- [ ] `C-CF-280` `capability` A fresh installation already knows the four expertises in order with the eight slots. `src: Core features rule 25`
- [ ] `C-CF-281` `capability` Everything the studio writes persists on the server. `src: Core features rule 25`
- [ ] `C-CF-282` `ui` The cookie choice, an unsent brief, a list's filters live in the browser. `src: Core features rule 25`
- [ ] `C-CF-283` `constraint` The studio offers no way to add a fifth expertise. `src: Core features rule 25`
- [ ] `C-CF-284` `ui` A timeout, a refusal or a dropped connection never clears a form. `src: Core features rule 26`
- [ ] `C-CF-285` `ui` Offline, the brief form shows `You are offline.` followed by `Your brief is saved here` with the reconnect clause. `src: Core features rule 26`
- [ ] `C-CF-286` `ui` A held brief sends once when the connection returns. `src: Core features rule 26`
- [ ] `C-CF-287` `ui` A case study form whose session expired keeps the fields, offering a sign in. `src: Core features rule 26`

## C-UF User flow

- [ ] `C-UF-01` `capability` The company page shows the statement, the figures, the capabilities, the clients. `src: User flow table row 5`
- [ ] `C-UF-02` `capability` The route `/work` shows every published case study. `src: User flow table row 2`
- [ ] `C-UF-03` `capability` The route `/work/<slug>` shows one published case study with the next. `src: User flow table row 3`
- [ ] `C-UF-04` `capability` The route `/company` shows the company page. `src: User flow table row 5`
- [ ] `C-UF-05` `capability` The route `/contact` shows the offices with the brief form. `src: User flow table row 6`
- [ ] `C-UF-06` `capability` The route `/privacy-policy` shows the privacy notice. `src: User flow table row 7`
- [ ] `C-UF-07` `capability` The sign in page serves the sign in form to a signed-out person. `src: User flow table row 8`
- [ ] `C-UF-08` `role` The studio work list at `/studio/work` shows every case study, draft or published, to the `owner`, the `editor`. `src: User flow table row 10`
- [ ] `C-UF-09` `role` The shelf route is reachable by the `owner` only. `src: User flow table row 12`
- [ ] `C-UF-10` `role` The page-view route `/studio/page-views` is reachable by the `owner` only. `src: User flow table row 14`
- [ ] `C-UF-11` `role` The account route `/studio/account` is reachable by the `owner`, the `editor`. `src: User flow table row 15`
- [ ] `C-UF-12` `capability` A signed-in person opening the sign in page lands on the studio dashboard. `src: User flow entry and redirects`
- [ ] `C-UF-13` `role` An `editor` opening an owner-only studio route sees the refusal page. `src: User flow entry and redirects`
- [ ] `C-UF-14` `role` A `visitor` opening a studio route sees the refusal page. `src: User flow entry and redirects`
- [ ] `C-UF-15` `ui` The header control `Expertise` opens a panel of the four expertises. `src: User flow entry and redirects`
- [ ] `C-UF-16` `ui` The expertise panel closes on the same control, on the Escape key, on any navigation. `src: User flow entry and redirects`
- [ ] `C-UF-17` `capability` The owner journey publishes `Aster Row Residences` for the client `Halden` in `2025`. `src: User flow owner journey`
- [ ] `C-UF-18` `ui` The owner journey generates a `warm` cover with alternative text before publishing. `src: User flow owner journey`
- [ ] `C-UF-19` `capability` The published `Aster Row Residences` appears last on the public work index. `src: User flow owner journey`
- [ ] `C-UF-20` `capability` The published `Aster Row Residences` appears on the `Real Estate` landing. `src: User flow owner journey`
- [ ] `C-UF-21` `capability` The owner journey features `Aster Row Residences` in the second `Real Estate` slot on the front page. `src: User flow owner journey`
- [ ] `C-UF-22` `capability` The case study `Harbour Quarter` stays on the public work index after leaving the slot. `src: User flow owner journey`
- [ ] `C-UF-23` `capability` The visitor journey filters the work index to `Corporate`, the address gaining `?expertise=corporate`. `src: User flow visitor journey`
- [ ] `C-UF-24` `capability` The visitor journey adds the tag `Banking` to the work filter. `src: User flow visitor journey`
- [ ] `C-UF-25` `capability` The visitor journey opens `Kestrel Annual Review`. `src: User flow visitor journey`
- [ ] `C-UF-26` `capability` The visitor journey follows the next case study. `src: User flow visitor journey`
- [ ] `C-UF-27` `ui` The visitor journey reads a message under each required field after submitting an empty form. `src: User flow visitor journey`
- [ ] `C-UF-28` `ui` The visitor journey sees `Thank you!` replace the form where the form stood. `src: User flow visitor journey`
- [ ] `C-UF-29` `ui` The owner journey opens the brief from `Ines Duval`. `src: User flow owner reads a brief`
- [ ] `C-UF-30` `ui` The owner journey sees the markup of that brief as plain characters. `src: User flow owner reads a brief`
- [ ] `C-UF-31` `ui` The owner journey archives the brief from `Ines Duval`. `src: User flow owner reads a brief`
- [ ] `C-UF-32` `capability` The withdraw journey unpublishes `Northline Self Care`. `src: User flow owner withdraws`
- [ ] `C-UF-33` `capability` The withdraw journey finds `Northline Self Care` gone from `/work`. `src: User flow owner withdraws`
- [ ] `C-UF-34` `capability` The withdraw journey publishes `Northline Self Care` back into the same shelf place. `src: User flow owner withdraws`
- [ ] `C-UF-35` `ui` The wrong-address journey shows `Not found` for the draft, `No longer here` for the withdrawn case study. `src: User flow wrong address`
- [ ] `C-UF-36` `ui` Every list, page has a loading state carrying words. `src: User flow states`
- [ ] `C-UF-37` `ui` An error state offers a way forward. `src: User flow states`
- [ ] `C-UF-38` `ui` Every list, page has an offline state. `src: User flow states`
- [ ] `C-UF-39` `ui` A region never goes blank. `src: User flow states`
- [ ] `C-UF-40` `ui` Nothing changes size when the state of a region changes. `src: User flow states`
- [ ] `C-UF-41` `constraint` A loading placeholder never shimmers, never pulses. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The ink is a near-black neutral with a faint cool cast. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The ground is a near-white neutral. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The opening screen, the grey bands sit on a flat pale grey. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Every other colour on screen is the ink or the white at a lower strength. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The one alarm colour, a light soft red, marks a failed field only. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Error sentences are set in the ink. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` True black appears only in the print stylesheet. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Nothing tints a cover. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Ink over pale meets WCAG AA contrast. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A raised contrast setting darkens faint captions, following the system preference. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` The site is designed light-first with no separate dark mode. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Success, in-progress are said in words on the status line, never by colour alone. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Borders are the ink at a low strength. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The primary action is the solid dark pill. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Touch targets are comfortably sized. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Every icon-only control carries a text label for assistive technology. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` A panel decides whether the panel's ink is dark on pale or pale on dark. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` The page alternates white, grey, near-black bands. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` The header words fade across a band boundary instead of flipping. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Links never underline, never move. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` A link fades to half strength on hover. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Exactly one drop shadow exists in the product, on the cookie bar. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Each page leads with one primary action set apart from every secondary control. `src: UI/UX notes`
- [ ] `C-UX-24` `ui` The primary action on the contact page is the large round `Submit`, on the dashboard `New case study`. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` Motion uses one eased, long-tailed curve. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` A sharper curve moves the header arriving from above, the cookie bar sliding in sideways. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` Headings animate in letter by letter, each letter rising from below the line. `src: UI/UX notes`
- [ ] `C-UX-28` `ui` The circle cluster draws on, each circle starting from a different point. `src: UI/UX notes`
- [ ] `C-UX-29` `ui` A pill button label rolls upward on hover. `src: UI/UX notes`
- [ ] `C-UX-30` `ui` Nothing slides sideways as the page scrolls. `src: UI/UX notes`
- [ ] `C-UX-31` `ui` No page fades on navigation. `src: UI/UX notes`
- [ ] `C-UX-32` `ui` No control grows on hover. `src: UI/UX notes`
- [ ] `C-UX-33` `ui` The loading spinner is the only looping animation. `src: UI/UX notes`
- [ ] `C-UX-34` `ui` A reduced-motion preference removes the letter rise, the draw-on, the smooth scrolling. `src: UI/UX notes`
- [ ] `C-UX-35` `ui` Density is spacious, with bands reading as separate without a dividing line. `src: UI/UX notes`
- [ ] `C-UX-36` `ui` A form field at rest shows only the label. `src: UI/UX notes`
- [ ] `C-UX-37` `ui` A focused field lifts the label as a thin rule draws in from the left. `src: UI/UX notes`
- [ ] `C-UX-38` `ui` Layout follows the window shape, so a sideways phone never gets a tablet layout. `src: UI/UX notes`
- [ ] `C-UX-39` `ui` Type scales smoothly between the two wide sizes, stepping down on a phone. `src: UI/UX notes`
- [ ] `C-UX-40` `ui` The layout has five sizes. `src: UI/UX notes`
- [ ] `C-UX-41` `ui` Body text on a medium window is slightly smaller than on a phone. `src: UI/UX notes`
- [ ] `C-UX-42` `ui` At a phone viewport the header collapses to the wordmark with a two-line menu glyph. `src: UI/UX notes`
- [ ] `C-UX-43` `ui` At a phone viewport the work grid keeps two columns. `src: UI/UX notes`
- [ ] `C-UX-44` `ui` At a phone viewport nothing scrolls sideways except the filter row. `src: UI/UX notes`
- [ ] `C-UX-45` `ui` A print stylesheet sets text in true black. `src: UI/UX notes`
- [ ] `C-UX-46` `ui` Keyboard navigation reaches every control with a visible focus outline. `src: UI/UX notes`
- [ ] `C-UX-47` `ui` A letter-split heading reads to assistive technology as one piece of text. `src: UI/UX notes`
- [ ] `C-UX-48` `ui` Icons are hidden from assistive technology. `src: UI/UX notes`
- [ ] `C-UX-49` `ui` Reordering the shelf from the keyboard announces each new position. `src: UI/UX notes`
- [ ] `C-UX-50` `ui` The studio uses the public site's header, type, greys. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` The type family is `Inter Tight`. `src: Front-end specification type`
- [ ] `C-FE-02` `literal` The regular cut `400` sets body, interface, captions. `src: Front-end specification type`
- [ ] `C-FE-03` `literal` The medium cut `500` sets headings with the current navigation item. `src: Front-end specification type`
- [ ] `C-FE-04` `constraint` No third font cut exists. `src: Front-end specification type`
- [ ] `C-FE-05` `literal` The display size `180px` sets the headline, the company figure, a failure code. `src: Front-end specification type`
- [ ] `C-FE-06` `literal` The first heading is `90px`; the third heading is `38px`. `src: Front-end specification type`
- [ ] `C-FE-07` `literal` Body is `22px`, interface `16px`, small `14px`, caption `12px`. `src: Front-end specification type`
- [ ] `C-FE-08` `literal` The breadcrumb, the consent line are `10px`, never scaled, never tracked. `src: Front-end specification type`
- [ ] `C-FE-09` `ui` Tracking is negative everywhere, tightest at the display size. `src: Front-end specification type`
- [ ] `C-FE-10` `literal` The type fallback is `"Helvetica Neue", Helvetica, Arial, system-ui, sans-serif`, adjusted against reflow. `src: Front-end specification type`
- [ ] `C-FE-11` `ui` The header carries the wordmark `Northform`, the `Expertise` control, the links `Work`, `Company`, `Contact`. `src: Front-end specification global chrome`
- [ ] `C-FE-12` `ui` The header is thin, sticky. `src: Front-end specification global chrome`
- [ ] `C-FE-13` `ui` Pointing at an expertise in the panel plays a short silent generated loop. `src: Front-end specification global chrome`
- [ ] `C-FE-14` `ui` The expertise loop is created on the first opening of the panel. `src: Front-end specification global chrome`
- [ ] `C-FE-15` `ui` The expertise loop stops when the panel closes. `src: Front-end specification global chrome`
- [ ] `C-FE-16` `ui` The expertise loop never delays the panel opening. `src: Front-end specification global chrome`
- [ ] `C-FE-17` `ui` Four button roles exist: a pale pill, a solid dark pill, a card square, a header square. `src: Front-end specification global chrome`
- [ ] `C-FE-18` `ui` The footer carries `Get In Touch` above five social links `Network One` to `Network Five` with rules between. `src: Front-end specification global chrome`
- [ ] `C-FE-19` `ui` The footer carries the copyright sign, `1998`, a hyphen, the current year. `src: Front-end specification global chrome`
- [ ] `C-FE-20` `ui` The footer carries a `Privacy Policy` link. `src: Front-end specification global chrome`
- [ ] `C-FE-21` `ui` The cookie bar notice about `website uses cookies` offers `Accept`. `src: Front-end specification global chrome`
- [ ] `C-FE-22` `ui` The cookie choice survives a reload. `src: Front-end specification global chrome`
- [ ] `C-FE-23` `ui` The skip link reads `Skip to content`. `src: Front-end specification global chrome`
- [ ] `C-FE-24` `ui` Nine marks are drawn inline in the page. `src: Front-end specification iconography`
- [ ] `C-FE-25` `ui` Every mark uses straight lines, right angles, diagonals or circles, unfilled, with square ends. `src: Front-end specification iconography`
- [ ] `C-FE-26` `ui` The close cross is taller than wide; the menu glyph is two long thin rules. `src: Front-end specification iconography`
- [ ] `C-FE-27` `ui` The circle cluster is overlapping dashed circles, each with one long gap at an angle of the circle's own. `src: Front-end specification iconography`
- [ ] `C-FE-28` `ui` A card carries a notched square block in the cover's bottom right corner holding the plus. `src: Front-end specification cards, covers and other media`
- [ ] `C-FE-29` `ui` The corner block alternates in a checker on the work index, alternating across the two cards of a front page band. `src: Front-end specification cards, covers and other media`
- [ ] `C-FE-30` `ui` Covers keep full colour. `src: Front-end specification cards, covers and other media`
- [ ] `C-FE-31` `ui` A generated cover places three to seven rectangles, circles or quarter arcs on a twelve-by-six grid, at most one filled. `src: Front-end specification cards, covers and other media`
- [ ] `C-FE-32` `ui` The palettes paint the generated cover as mono white ground with ink marks, warm pale grey ground with one alarm shape at most, cool ink ground with white marks. `src: Front-end specification cards, covers and other media`
- [ ] `C-FE-33` `ui` A faint grain lies over every generated cover. `src: Front-end specification cards, covers and other media`
- [ ] `C-FE-34` `constraint` The build ships no photograph, no video, no image file of the studio's own. `src: Front-end specification zero-asset substitution`
- [ ] `C-FE-35` `constraint` The only files shipped beside the code are the font files for `Inter Tight`. `src: Front-end specification zero-asset substitution`
- [ ] `C-FE-36` `ui` The showreel, the four expertise loops are generated. `src: Front-end specification zero-asset substitution`
- [ ] `C-FE-37` `ui` On a laptop the showreel shows a trailing round label `Watch showreel`. `src: Front-end specification the cursor and the showreel`
- [ ] `C-FE-38` `ui` On a laptop the client strip shows a trailing round label `Drag`. `src: Front-end specification the cursor and the showreel`
- [ ] `C-FE-39` `constraint` The trailing pointer label never exists on touch devices. `src: Front-end specification the cursor and the showreel`
- [ ] `C-FE-40` `capability` The showreel loads nothing until pressed. `src: Front-end specification the cursor and the showreel`
- [ ] `C-FE-41` `ui` At wide sizes the site smooths scrolling. `src: Front-end specification the scroll system`
- [ ] `C-FE-42` `ui` At a phone size scrolling is native. `src: Front-end specification the scroll system`
- [ ] `C-FE-43` `ui` Arrow keys, page keys, in-page links, find-on-page, the back position keep working under smooth scrolling. `src: Front-end specification the scroll system`
- [ ] `C-FE-44` `constraint` A slow machine gets scrolling handed back to the browser for the visit. `src: Front-end specification the scroll system`
- [ ] `C-FE-45` `constraint` The public site, the studio load as separate parts, never together. `src: Front-end specification architecture of the front end`
- [ ] `C-FE-46` `ui` Four shared pieces carry the design: the type, the buttons, the form fields, the case study card. `src: Front-end specification architecture of the front end`
- [ ] `C-FE-47` `literal` The expertise sentences begin `Luxury real estate website design - iconic websites for iconic properties.`, `Inspiring, functional,`, `From idea to a product:`, `High-class eCommerce solutions`. `src: Front-end specification the copy deck`
- [ ] `C-FE-48` `literal` The capability headings are `Web & mobile apps`, `UX & product design`, `Product development`, `Award-class web design`, `Communication design`. `src: Front-end specification the copy deck`
- [ ] `C-FE-49` `literal` The capability bodies begin `Services, self-care, eCommerce, payments,`, `User research, journey maps,`, `Minimum viable`, `World-class advanced promotional`, `Naming, branding, communication strategy,`. `src: Front-end specification the copy deck`
- [ ] `C-FE-50` `literal` The company copy reads `We are a strategic partner to our clients.` followed by `We will help you to ideate, design`. `src: Front-end specification the copy deck`
- [ ] `C-FE-51` `literal` The clients are `Meridian Air`, `Halden`, `Northline`, `Kestrel Bank`, `Ostend Credit`, `Vantage`, `Pinemark`. `src: Front-end specification the copy deck`
- [ ] `C-FE-52` `literal` The eleven tag slugs are `promo-website`, `corporate-website`, `online-store`, `self-service`, `saas`, `banking`, `customer-portal`, `trading-platform`, `branding`, `3d-visualisation`, `real-estate`. `src: Front-end specification the copy deck`
- [ ] `C-FE-53` `literal` The eleven tag names are `Promo Website`, `Corporate Website`, `Online Store`, `Self-Service`, `SaaS`, `Banking`, `Customer Portal`, `Trading Platform`, `Branding`, `3D & Visualisation`, `Real Estate`. `src: Front-end specification the copy deck`
- [ ] `C-FE-54` `literal` The four expertise slugs in order are `real-estate`, `corporate`, `startups`, `ecommerce`. `src: Front-end specification the copy deck`
- [ ] `C-FE-55` `ui` The studio rail reads `Work`, `Shelf`, `Inbox`, `Page views`, `Account`. `src: Front-end specification the copy deck`
- [ ] `C-FE-56` `ui` An editor's studio rail omits the owner-only items. `src: Front-end specification the copy deck`
- [ ] `C-FE-57` `ui` The studio controls read `New case study`, `Save`, `Publish`, `Unpublish`, `Delete`, `Generate cover`, `Archive`, `Mark unread`, `Reply`, `Keep mine`, `Take theirs`, `Sign in`, `Sign out everywhere`, `Back to studio`, `Back to work`. `src: Front-end specification the copy deck`
- [ ] `C-FE-58` `ui` An empty shelf slot reads `Nothing featured.` `src: Front-end specification the copy deck`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The browser receives a single-page application built with `Angular` in TypeScript. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The server is `Express` in TypeScript. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The server hands the production build to every non-API path, so a deep link opens the route. `src: Technical requirements`
- [ ] `C-TR-04` `contract` Case studies, tags, expertises, slots, briefs, sessions, accounts, page views live in `PostgreSQL` at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Covers live in `minio` at `STORAGE_ENDPOINT`. `src: Technical requirements`
- [ ] `C-TR-06` `literal` The bucket is named by `STORAGE_BUCKET`. `src: Technical requirements`
- [ ] `C-TR-07` `literal` The storage key pair comes from `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements`
- [ ] `C-TR-08` `capability` Cover bytes reach the browser through `GET /api/covers/{id}`, which checks the case study state on every request. `src: Technical requirements`
- [ ] `C-TR-09` `role` A cover of an unpublished case study needs the bearer token of an owner or editor. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` The bucket is never exposed directly to the browser. `src: Technical requirements`
- [ ] `C-TR-11` `capability` The app checks the email, password sign in itself. `src: Technical requirements`
- [ ] `C-TR-12` `data` Passwords are stored hashed. `src: Technical requirements`
- [ ] `C-TR-13` `literal` The route `POST /api/auth/login` returns an `access_token` accepted as a bearer token. `src: Technical requirements`
- [ ] `C-TR-14` `contract` Each handled request writes one line to stdout. `src: Technical requirements`
- [ ] `C-TR-15` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements`
- [ ] `C-TR-16` `constraint` The app uses only the named libraries with their direct dependencies. `src: Technical requirements`
- [ ] `C-TR-17` `constraint` No host, port, key, password is written into the code. `src: Technical requirements`
- [ ] `C-TR-18` `constraint` No credential appears in any file the browser downloads. `src: Technical requirements`
- [ ] `C-TR-19` `capability` Every response carries a content-type options header refusing sniffing. `src: Technical requirements`
- [ ] `C-TR-20` `capability` Every response carries a frame restriction denying framing. `src: Technical requirements`
- [ ] `C-TR-21` `capability` Every response carries a referrer policy. `src: Technical requirements`
- [ ] `C-TR-22` `capability` Every response carries a content security policy limited to the site's own origin. `src: Technical requirements`
- [ ] `C-TR-23` `contract` A refusal answers with an `error` object holding `code`, `message`, `fields`. `src: Technical requirements`
- [ ] `C-TR-24` `literal` The refusal `code` is one of `bad_request`, `unauthenticated`, `forbidden`, `not_found`, `gone`, `conflict`, `unprocessable`, `rate_limited`, `locked`. `src: Technical requirements`
- [ ] `C-TR-25` `contract` An `unprocessable` refusal maps each failing field name to the inline message. `src: Technical requirements`
- [ ] `C-TR-26` `constraint` An animation takes the same time on a slow machine as on a fast one. `src: Technical requirements`
- [ ] `C-TR-27` `constraint` The first page appears quickly on an ordinary three-year-old laptop. `src: Technical requirements`
- [ ] `C-TR-28` `constraint` The running site calls nothing outside the environment. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds eleven tables, every timestamp in UTC. `src: Data model`
- [ ] `C-DM-02` `contract` Every seeded account with the password is written into `/app/USER_README.md`. `src: Data model`
- [ ] `C-DM-03` `data` The `accounts` table holds `id`, `email`, `password_hash`, `display_name`, `role`, `failed_attempts`, `locked_until`, `created_at`. `src: Data model accounts`
- [ ] `C-DM-04` `data` An account email is unique, compared without regard to case. `src: Data model accounts`
- [ ] `C-DM-05` `data` The `sessions` table holds `id`, `account_id`, `token_hash`, `user_agent_summary`, `created_at`, `last_seen_at`, `expires_at`, `revoked_at`. `src: Data model sessions`
- [ ] `C-DM-06` `data` The column `token_hash` holds a hash of the token, never the token. `src: Data model sessions`
- [ ] `C-DM-07` `data` The `expertises` table holds `id`, `slug`, `name`, `sentence`, `position` from `0` to `3`. `src: Data model expertises`
- [ ] `C-DM-08` `data` The `tags` table holds `id`, `slug`, `name` for exactly the eleven tags. `src: Data model tags`
- [ ] `C-DM-09` `data` The `case_studies` table holds `id`, `slug`, `title`, `client`, `year`, `expertise_id`, `summary`, `cover_seed`, `cover_palette`, `cover_id`, `blocks`, `position`, `published`, `published_at`, `withdrawn_at`, `author_id`, `version`, `created_at`, `updated_at`. `src: Data model case_studies`
- [ ] `C-DM-10` `data` A case study slug is unique. `src: Data model case_studies`
- [ ] `C-DM-11` `data` A case study shelf position is unique across every case study. `src: Data model case_studies`
- [ ] `C-DM-12` `data` The column `withdrawn_at` is set on withdrawal, cleared on publish. `src: Data model case_studies`
- [ ] `C-DM-13` `data` The column `published_at` is empty for an unpublished case study. `src: Data model case_studies`
- [ ] `C-DM-14` `data` The column `author_id` is kept when the author's account is removed. `src: Data model case_studies`
- [ ] `C-DM-15` `data` The `case_study_tags` table holds `id`, `case_study_id`, `tag_id`, each pair once. `src: Data model case_study_tags`
- [ ] `C-DM-16` `data` The `covers` table holds `id`, `case_study_id`, `object_key`, `content_type`, `byte_size`, `sha256`, `width`, `height`, `alt_text`, `created_at`. `src: Data model covers`
- [ ] `C-DM-17` `data` A cover `object_key` is unique. `src: Data model covers`
- [ ] `C-DM-18` `data` The `feature_slots` table holds `id`, `expertise_id`, `position`, `case_study_id`, `version` in eight rows. `src: Data model feature_slots`
- [ ] `C-DM-19` `data` A feature slot `position` is `0` or `1`. `src: Data model feature_slots`
- [ ] `C-DM-20` `data` The `shelf` table holds `id`, `version` in one row. `src: Data model shelf`
- [ ] `C-DM-21` `constraint` A shelf reorder changes places only. `src: Data model invariants`
- [ ] `C-DM-22` `data` The `briefs` table holds `id`, `name`, `company`, `phone`, `email`, `comment`, `expertise`, `budget`, `state`, `source_path`, `received_at`. `src: Data model briefs`
- [ ] `C-DM-23` `data` A brief `state` is one of `unread`, `read`, `archived`. `src: Data model briefs`
- [ ] `C-DM-24` `constraint` The next link, the dashboard counts, the unread count, public visibility are derived on read. `src: Data model`
- [ ] `C-DM-25` `data` The `page_views` table holds `id`, `route`, `viewed_at`. `src: Data model page_views`
- [ ] `C-DM-26` `constraint` Shelf places are unique, gap-free. `src: Data model invariants`
- [ ] `C-DM-27` `constraint` A refused write writes no row, no partial row, no object. `src: Data model invariants`
- [ ] `C-DM-28` `literal` Twelve case studies are seeded in the pinned shelf order, from `Cliffside Residences` to `Pinemark Mobile App`. `src: Data model seed data`
- [ ] `C-DM-29` `literal` Ten seeded case studies are published, `Harbour Quarter` among them. `src: Data model seed data`
- [ ] `C-DM-30` `literal` Seeded shelf place 1 is `Cliffside Residences` at `cliffside-residences`, client `Halden`, year `2024`, expertise `real-estate`, published. `src: Data model seed data table`
- [ ] `C-DM-31` `literal` Seeded shelf place 2 is `Kestrel Annual Review` at `kestrel-annual-review`, client `Kestrel Bank`, year `2024`, expertise `corporate`, published. `src: Data model seed data table`
- [ ] `C-DM-32` `literal` Seeded shelf place 3 is `Vantage Onboarding` at `vantage-onboarding`, client `Vantage`, year `2025`, expertise `startups`, published. `src: Data model seed data table`
- [ ] `C-DM-33` `literal` Seeded shelf place 4 is `Meridian Duty Free` at `meridian-duty-free`, client `Meridian Air`, year `2024`, expertise `ecommerce`, published. `src: Data model seed data table`
- [ ] `C-DM-34` `literal` Seeded shelf place 5 is `Harbour Quarter` at `harbour-quarter`, client `Northline`, year `2023`, expertise `real-estate`, published. `src: Data model seed data table`
- [ ] `C-DM-35` `literal` Seeded shelf place 6 is `Ostend Loyalty Store` at `ostend-loyalty-store`, client `Ostend Credit`, year `2021`, expertise `ecommerce`, withdrawn. `src: Data model seed data table`
- [ ] `C-DM-36` `literal` Seeded shelf place 7 is `Ostend Investor Portal` at `ostend-investor-portal`, client `Ostend Credit`, year `2022`, expertise `corporate`, published. `src: Data model seed data table`
- [ ] `C-DM-37` `literal` Seeded shelf place 8 is `Pinemark Trading Desk` at `pinemark-trading-desk`, client `Pinemark`, year `2023`, expertise `startups`, published. `src: Data model seed data table`
- [ ] `C-DM-38` `literal` Seeded shelf place 9 is `Halden Home Store` at `halden-home-store`, client `Halden`, year `2022`, expertise `ecommerce`, published. `src: Data model seed data table`
- [ ] `C-DM-39` `literal` Seeded shelf place 10 is `Northline Self Care` at `northline-self-care`, client `Northline`, year `2021`, expertise `corporate`, published. `src: Data model seed data table`
- [ ] `C-DM-40` `literal` Seeded shelf place 11 is `Vantage Pitch Site` at `vantage-pitch-site`, client `Vantage`, year `2025`, expertise `startups`, published. `src: Data model seed data table`
- [ ] `C-DM-41` `literal` Seeded shelf place 12 is `Pinemark Mobile App` at `pinemark-mobile-app`, client `Pinemark`, year `2025`, expertise `startups`, draft. `src: Data model seed data table`
- [ ] `C-DM-42` `literal` Seeded shelf place 1 carries the tags `promo-website`, `real-estate`. `src: Data model seed data table`
- [ ] `C-DM-43` `literal` Seeded shelf place 2 carries the tags `corporate-website`, `banking`. `src: Data model seed data table`
- [ ] `C-DM-44` `literal` Seeded shelf place 3 carries the tags `saas`, `self-service`. `src: Data model seed data table`
- [ ] `C-DM-45` `literal` Seeded shelf place 4 carries the tags `online-store`, `branding`. `src: Data model seed data table`
- [ ] `C-DM-46` `literal` Seeded shelf place 5 carries the tags `real-estate`, `3d-visualisation`. `src: Data model seed data table`
- [ ] `C-DM-47` `literal` Seeded shelf place 6 carries the tags `online-store`. `src: Data model seed data table`
- [ ] `C-DM-48` `literal` Seeded shelf place 7 carries the tags `customer-portal`, `banking`. `src: Data model seed data table`
- [ ] `C-DM-49` `literal` Seeded shelf place 8 carries the tags `trading-platform`, `saas`. `src: Data model seed data table`
- [ ] `C-DM-50` `literal` Seeded shelf place 9 carries the tags `online-store`. `src: Data model seed data table`
- [ ] `C-DM-51` `literal` Seeded shelf place 10 carries the tags `self-service`, `customer-portal`. `src: Data model seed data table`
- [ ] `C-DM-52` `literal` Seeded shelf place 11 carries the tags `promo-website`. `src: Data model seed data table`
- [ ] `C-DM-53` `literal` Seeded shelf place 12 carries the tags `saas`. `src: Data model seed data table`
- [ ] `C-DM-54` `literal` A seeded case study's cover seed is the seeded place number, `1` to `12`, with palette `mono`. `src: Data model seed data`
- [ ] `C-DM-55` `literal` The shelf row starts at `version` `1`. `src: Data model seed data`
- [ ] `C-DM-56` `literal` The `real-estate` slots start as `Cliffside Residences` then `Harbour Quarter`. `src: Data model seed data`
- [ ] `C-DM-57` `literal` The `corporate` slots start as `Kestrel Annual Review` then `Ostend Investor Portal`. `src: Data model seed data`
- [ ] `C-DM-58` `literal` The `startups` slots start as `Vantage Onboarding` then `Pinemark Trading Desk`. `src: Data model seed data`
- [ ] `C-DM-59` `literal` The `ecommerce` slots start as `Meridian Duty Free` then `Halden Home Store`. `src: Data model seed data`
- [ ] `C-DM-60` `literal` The seeded brief from `Ines Duval` carries `ines.duval@example.com`, company `Halden`, expertise `real-estate`, budget `75k_to_150k`, state `unread`. `src: Data model seed data`
- [ ] `C-DM-61` `literal` The comment of the `Ines Duval` brief is `A site for our coastal tower. <b>Launch before March</b>` `src: Data model seed data`
- [ ] `C-DM-62` `literal` The seeded brief from `Tomas Berg` carries `tomas.berg@example.com`, company `Vantage`, expertise `startups`, budget `25k_to_75k`, state `unread`. `src: Data model seed data`
- [ ] `C-DM-63` `literal` The comment of the `Tomas Berg` brief is `We need an onboarding flow for a savings app.` `src: Data model seed data`
- [ ] `C-DM-64` `literal` The seeded brief from `Lea Park` carries `lea.park@example.com`, company `Pinemark`, expertise `ecommerce`, budget `under_25k`, state `read`. `src: Data model seed data`
- [ ] `C-DM-65` `literal` The comment of the `Lea Park` brief is `Could you quote for a small online store refresh?` `src: Data model seed data`
- [ ] `C-DM-66` `capability` Every seeded case study carries a generated cover in the bucket with alternative text. `src: Data model seed data`
- [ ] `C-DM-67` `capability` Every seeded case study body holds at least one paragraph block. `src: Data model seed data`
- [ ] `C-DM-68` `constraint` No page views are seeded. `src: Data model seed data`
- [ ] `C-DM-69` `capability` Seeding is idempotent across a restart. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product holds one studio, no organisation, no team workspace, no second tenant. `src: Constraints`
- [ ] `C-CN-02` `constraint` The build has no blog index, no article route, no article editor, no career page. `src: Constraints`
- [ ] `C-CN-03` `constraint` No email leaves the product: no reset link, no invitation, no address change. `src: Constraints`
- [ ] `C-CN-04` `constraint` The product never asks the browser for permission to notify. `src: Constraints`
- [ ] `C-CN-05` `constraint` The product tells people things only under the pressed control, at the top of a list, beside `Inbox`. `src: Constraints`
- [ ] `C-CN-06` `constraint` The public site has no search box, no sort. `src: Constraints`
- [ ] `C-CN-07` `constraint` A publish appears on the next load, never live. `src: Constraints`
- [ ] `C-CN-08` `constraint` The product loads no third-party analytics, no tracking cookie. `src: Constraints`
- [ ] `C-CN-09` `constraint` Nothing a visitor types is counted. `src: Constraints`
- [ ] `C-CN-10` `constraint` The product ships one language, showing dates in UTC in one fixed format. `src: Constraints`
- [ ] `C-CN-11` `constraint` No long dash appears in any string. `src: Constraints`
- [ ] `C-CN-12` `constraint` The product embeds no third-party video player. `src: Constraints`
- [ ] `C-CN-13` `constraint` The product stays responsive with a few thousand page views, a few hundred briefs. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-04` `literal` The route `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-06` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-07` `literal` Empty `.browser_screenshots/`, `.downloads/` directories exist at the app root. `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server, never a dev server. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, never a child of the shell. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`, never a loopback address. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` No backing service named in the brief is downloaded, installed, compiled, started. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No persistent volume, no fixed container name, no custom network is declared. `src: Deployment contract`
- [ ] `C-DC-14` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` An invalid or unauthorized call is rejected as a client error, never as a server error. `src: Deployment contract API shapes`
- [ ] `C-DC-16` `contract` An invalid or unauthorized call is never answered as a silent success. `src: Deployment contract API shapes`
- [ ] `C-DC-17` `contract` Bearer authentication is required on every `/api/studio` endpoint, on `/api/sessions`, on `/api/auth/me`. `src: Deployment contract API shapes`
- [ ] `C-DC-18` `contract` Bearer authentication is required on `GET /api/covers/{id}` for a cover whose case study is not published. `src: Deployment contract API shapes`
- [ ] `C-DC-19` `contract` Every other listed endpoint is public. `src: Deployment contract API shapes`
- [ ] `C-DC-20` `data` An `expertise` field always holds an expertise slug. `src: Deployment contract API shapes`
- [ ] `C-DC-21` `data` A `tags` field always holds an array of tag slugs. `src: Deployment contract API shapes`
- [ ] `C-DC-22` `capability` The route `GET /api/site` returns `expertises` in order, `tags`, `clients`, `featured`. `src: Deployment contract API shapes`
- [ ] `C-DC-23` `contract` Each `featured` slot in `GET /api/site` holds a published case study or `null`. `src: Deployment contract API shapes`
- [ ] `C-DC-24` `contract` The route `POST /api/studio/work` takes `title`, optional `slug`, `client`, `year`, `expertise`, `tags`, `summary`, `cover_seed`, `cover_palette`, `blocks`. `src: Deployment contract API shapes`
- [ ] `C-DC-25` `capability` The route `GET /api/expertise/{slug}` returns an expertise with a `work` list. `src: Deployment contract API shapes`
- [ ] `C-DC-26` `capability` The route `POST /api/studio/work` returns an unpublished case study at version one with the shelf position. `src: Deployment contract API shapes`
- [ ] `C-DC-27` `data` A case study response carries `id`, `slug`, `title`, `client`, `year`, `expertise`, `tags`, `summary`, `cover_seed`, `cover_palette`, `cover`, `blocks`, `position`, `published`, `version`. `src: Deployment contract API shapes`
- [ ] `C-DC-28` `data` A cover response carries `id`, `object_key`, `alt_text`, `width`, `height`. `src: Deployment contract API shapes`
- [ ] `C-DC-29` `data` A brief response carries the sent fields with `id`, `state`, `received_at`. `src: Deployment contract API shapes`
- [ ] `C-DC-30` `capability` The route `PUT /api/studio/shelf` takes `order` with the shelf `version`, returning the shelf `version` with `work`. `src: Deployment contract API shapes`
- [ ] `C-DC-31` `capability` The route `GET /api/studio/slots` returns the eight slots with `id`, `expertise`, `position`, `case_study_id`, `version`. `src: Deployment contract API shapes`
- [ ] `C-DC-32` `contract` The route `POST /api/auth/signup` takes `email`, `password`, optional `display_name`, returning the account with `role`, `access_token`. `src: Deployment contract API shapes`
- [ ] `C-DC-33` `contract` The route `POST /api/auth/login` takes `email`, `password`, returning the account with `role`, `access_token`. `src: Deployment contract API shapes`
- [ ] `C-DC-34` `contract` The route `GET /api/auth/me` returns the signed-in account with `role`. `src: Deployment contract API shapes`
- [ ] `C-DC-35` `contract` The route `GET /api/sessions` returns a top-level array of the account's live sessions. `src: Deployment contract API shapes`
- [ ] `C-DC-36` `contract` The route `DELETE /api/sessions` ends every session of the account. `src: Deployment contract API shapes`
- [ ] `C-DC-37` `contract` The route `GET /api/work` takes optional `expertise`, repeatable `tag`, returning published case studies in shelf order. `src: Deployment contract API shapes`
- [ ] `C-DC-38` `contract` The route `GET /api/work/{slug}` returns one published case study with `blocks`, `tags`, `expertise`, `cover`, `next`. `src: Deployment contract API shapes`
- [ ] `C-DC-39` `contract` The route `GET /api/covers/{id}` returns the cover bytes. `src: Deployment contract API shapes`
- [ ] `C-DC-40` `contract` The route `GET /api/briefs/token` returns a `form_token`. `src: Deployment contract API shapes`
- [ ] `C-DC-41` `contract` The route `POST /api/briefs` takes `name`, `company`, `phone`, `email`, `comment`, `expertise`, `budget`, `source_path`, `form_token`, `website`, returning `id`. `src: Deployment contract API shapes`
- [ ] `C-DC-42` `contract` The route `POST /api/briefs` with `POST /api/studio/work` accept an optional `Idempotency-Key` header. `src: Deployment contract API shapes`
- [ ] `C-DC-43` `contract` The route `POST /api/page-views` takes `route`, returning the recorded view for a public route. `src: Deployment contract API shapes`
- [ ] `C-DC-44` `contract` The route `POST /api/page-views` answers a `/studio` route with an empty acknowledgement, storing no row. `src: Deployment contract API shapes`
- [ ] `C-DC-45` `contract` The route `GET /api/studio/shelf` returns the shelf `version` with `work`, every case study in shelf order. `src: Deployment contract API shapes`
- [ ] `C-DC-46` `contract` The route `GET /api/studio/dashboard` returns `published_count`, `draft_count`, `recent`, with `unread_briefs` for the owner only. `src: Deployment contract API shapes`
- [ ] `C-DC-47` `contract` The route `GET /api/studio/work` returns a top-level array of every case study in shelf order. `src: Deployment contract API shapes`
- [ ] `C-DC-48` `contract` The route `GET /api/studio/work/{id}` returns one case study with `version`, `position`, `published`, `cover`. `src: Deployment contract API shapes`
- [ ] `C-DC-49` `contract` The route `PATCH /api/studio/work/{id}` takes the changed fields with `version`, returning the updated case study. `src: Deployment contract API shapes`
- [ ] `C-DC-50` `contract` The route `DELETE /api/studio/work/{id}` takes `version`. `src: Deployment contract API shapes`
- [ ] `C-DC-51` `contract` The route `POST /api/studio/work/{id}/cover` takes `generate` set to `true`, `alt_text`, `version`, returning the cover with `object_key`. `src: Deployment contract API shapes`
- [ ] `C-DC-52` `contract` The route `POST /api/studio/work/{id}/publish` takes `version`, returning the published case study. `src: Deployment contract API shapes`
- [ ] `C-DC-53` `contract` The route `DELETE /api/studio/work/{id}/publish` takes `version`, returning the unpublished case study. `src: Deployment contract API shapes`
- [ ] `C-DC-54` `contract` The route `PUT /api/studio/slots/{id}` takes `case_study_id` or `null` with `version`, returning the slot. `src: Deployment contract API shapes`
- [ ] `C-DC-55` `contract` The route `GET /api/studio/briefs` takes optional `state`, returning briefs newest first. `src: Deployment contract API shapes`
- [ ] `C-DC-56` `contract` The route `GET /api/studio/briefs/{id}` returns one brief. `src: Deployment contract API shapes`
- [ ] `C-DC-57` `contract` The route `PATCH /api/studio/briefs/{id}` takes `state`, returning the brief. `src: Deployment contract API shapes`
- [ ] `C-DC-58` `contract` The route `DELETE /api/studio/briefs/{id}` deletes the brief. `src: Deployment contract API shapes`
- [ ] `C-DC-59` `contract` The route `GET /api/studio/page-views` returns page views newest first. `src: Deployment contract API shapes`
- [ ] `C-DC-60` `constraint` An in-memory buffer, a container file, a base64 column, a dangling object key never stands in for the object store. `src: Deployment contract no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Real Estate` | the value in the item: The site files the studio's work under four expertises, (this value), Corporate, Startups, eCommerce. | C-OV-01 | Overview |
| `Corporate` | the value in the item: The site files the studio's work under four expertises, Real Estate, (this value), Startups, eCommerce. | C-OV-01 | Overview |
| `Startups` | the value in the item: The site files the studio's work under four expertises, Real Estate, Corporate, (this value), eCommerce. | C-OV-01 | Overview |
| `eCommerce` | the value in the item: The site files the studio's work under four expertises, Real Estate, Corporate, Startups, (this value). | C-OV-01 | Overview |
| `visitor` | the value in the item: Signup always creates an account whose role is (this value). | C-RL-03 | User roles |
| `editor` | the value in the item: An (this value) reads every case study, draft or published. | C-RL-05 | User roles table row 3 |
| `owner` | the value in the item: The (this value) publishes case studies. | C-RL-19 | User roles table row 4 |
| `owner@example.com` | seeded owner account | C-RL-30 | User roles seeded accounts row 1 |
| `Mara Lind` | the value in the item: The seeded account owner@example.com holds the role owner under the display name (this value). | C-RL-30 | User roles seeded accounts row 1 |
| `editor@example.com` | seeded editor account | C-RL-31 | User roles seeded accounts row 2 |
| `Jonas Weller` | the value in the item: The seeded account editor@example.com holds the role editor under the display name (this value). | C-RL-31 | User roles seeded accounts row 2 |
| `visitor@example.com` | seeded visitor account | C-RL-32 | User roles seeded accounts row 3 |
| `deku-demo-pw-2026` | seeded password for every account | C-RL-33 | User roles |
| `Pinemark Mobile App` | the value in the item: The seeded draft (this value) makes /work/pinemark-mobile-app answer not found. | C-CF-10 | Core features rule 1 |
| `/work/pinemark-mobile-app` | the value in the item: The seeded draft Pinemark Mobile App makes (this value) answer not found. | C-CF-10 | Core features rule 1 |
| `No longer here` | the value in the item: A withdrawn case study address answers gone with the line (this value). | C-CF-13 | Core features rule 2 |
| `Ostend Loyalty Store` | the value in the item: The seeded withdrawn (this value) makes /work/ostend-loyalty-store answer gone. | C-CF-14 | Core features rule 2 |
| `/work/ostend-loyalty-store` | the value in the item: The seeded withdrawn Ostend Loyalty Store makes (this value) answer gone. | C-CF-14 | Core features rule 2 |
| `Choose an expertise before publishing.` | the value in the item: A publish without an expertise is refused with (this value) | C-CF-15 | Core features rule 3 |
| `Add at least one tag before publishing.` | the value in the item: A publish without a tag is refused with (this value) | C-CF-16 | Core features rule 3 |
| `Add a cover before publishing.` | the value in the item: A publish without a cover is refused with (this value) | C-CF-17 | Core features rule 3 |
| `minio` | the value in the item: Every cover is a PNG stored as an object in (this value). | C-CF-22 | Core features rule 4 |
| `covers/{case_study_id}/{sha256_of_bytes}.{ext}` | cover object key scheme | C-CF-24 | Core features rule 4 |
| `Generate cover` | the value in the item: The control (this value) draws a cover from the cover seed in the chosen palette. | C-CF-25 | Core features rule 4 |
| `0` | the value in the item: The cover seed is a whole number from (this value) to 999999. | C-CF-28 | Core features rule 4 |
| `999999` | highest cover seed | C-CF-28 | Core features rule 4 |
| `mono` | the value in the item: The cover palette is one of (this value), warm, cool. | C-CF-29 | Core features rule 4 |
| `warm` | the value in the item: The cover palette is one of mono, (this value), cool. | C-CF-29 | Core features rule 4 |
| `cool` | the value in the item: The cover palette is one of mono, warm, (this value). | C-CF-29 | Core features rule 4 |
| `version` | the value in the item: Every case study carries a whole-number (this value) starting at 1. | C-CF-35 | Core features rule 5 |
| `1` | the value in the item: Every case study carries a whole-number version starting at (this value). | C-CF-35 | Core features rule 5 |
| `changed somewhere else` | the value in the item: The conflict message reads (this value) ending you were working. | C-CF-40 | Core features rule 5 |
| `you were working.` | the value in the item: The conflict message reads changed somewhere else ending (this value) | C-CF-40 | Core features rule 5 |
| `This changed somewhere else while you were working.` | the full wording the item quotes in part | C-CF-40 | Core features rule 5 |
| `Keep mine` | the value in the item: The studio shows a conflict in place with (this value), Take theirs, writing nothing until the person chooses. | C-CF-45 | Core features rule 5 |
| `Take theirs` | the value in the item: The studio shows a conflict in place with Keep mine, (this value), writing nothing until the person chooses. | C-CF-45 | Core features rule 5 |
| `Idempotency-Key` | the value in the item: A repeated case study create with one (this value) within 24 hours creates one case study. | C-CF-46 | Core features rule 6 |
| `/studio/shelf` | the value in the item: The owner reorders the shelf at (this value). | C-CF-52 | Core features rule 7 |
| `Order saved.` | the value in the item: A saved reorder shows (this value) | C-CF-55 | Core features rule 7 |
| `The order changed. Yours was not saved.` | the value in the item: A shelf reorder refused for an older or missing shelf version shows the conflict line, then (this value) | C-CF-61 | Core features rule 7 |
| `8` | feature slot count | C-CF-70 | Core features rule 8 |
| `Featured on the home page.` | the value in the item: Filling a slot shows (this value) | C-CF-75 | Core features rule 8 |
| `No longer featured. Still published.` | the value in the item: Emptying a slot shows (this value) | C-CF-76 | Core features rule 8 |
| `Design.` | the value in the item: The front page opens on the flat pale grey with the headline (this value), Development., Mastership. | C-CF-80 | Core features rule 9 |
| `Development.` | the value in the item: The front page opens on the flat pale grey with the headline Design., (this value), Mastership. | C-CF-80 | Core features rule 9 |
| `Mastership.` | the value in the item: The front page opens on the flat pale grey with the headline Design., Development., (this value) | C-CF-80 | Core features rule 9 |
| `exceptional digital products & services, eCommerce,` | the value in the item: The front page carries the statement about (this value) with the circle cluster. | C-CF-82 | Core features rule 9 |
| `We design and develop exceptional digital products & services, eCommerce, and brand communication solutions.` | the full wording the item quotes in part | C-CF-82 | Core features rule 9 |
| `Select an expertise` | the value in the item: The bar (this value) jumps down the front page, not acting as a filter. | C-CF-83 | Core features rule 9 |
| `Watch` | the value in the item: The showreel panel on the front page is labelled (this value), Showreel. | C-CF-84 | Core features rule 9 |
| `Showreel` | the value in the item: The showreel panel on the front page is labelled Watch, (this value). | C-CF-84 | Core features rule 9 |
| `01` | the value in the item: Each expertise band carries a number in a circle from (this value) to 04. | C-CF-85 | Core features rule 9 |
| `04` | the value in the item: Each expertise band carries a number in a circle from 01 to (this value). | C-CF-85 | Core features rule 9 |
| `Learn More` | the value in the item: Each expertise band carries a (this value) control leading to the expertise landing. | C-CF-87 | Core features rule 9 |
| `Our Capabilities` | the value in the item: The front page carries (this value) with five items. | C-CF-91 | Core features rule 9 |
| `20+` | the value in the item: The company band shows (this value) over Years of experience with More About Us. | C-CF-92 | Core features rule 9 |
| `Years of experience` | the value in the item: The company band shows 20+ over (this value) with More About Us. | C-CF-92 | Core features rule 9 |
| `More About Us` | the value in the item: The company band shows 20+ over Years of experience with (this value). | C-CF-92 | Core features rule 9 |
| `All Works` | the value in the item: The chip (this value) comes first, clearing every filter. | C-CF-102 | Core features rule 10 |
| `Industries` | the value in the item: The filter row offers the four expertises, then an (this value) group of eleven tags. | C-CF-103 | Core features rule 10 |
| `?expertise=<slug>` | the value in the item: The work filter lives in the address as (this value) with a repeatable &tag=<slug>. | C-CF-104 | Core features rule 10 |
| `&tag=<slug>` | the value in the item: The work filter lives in the address as ?expertise=<slug> with a repeatable (this value). | C-CF-104 | Core features rule 10 |
| `Nothing matches that.` | the value in the item: A work filter matching nothing shows (this value), the active filters, Clear filters. | C-CF-111 | Core features rule 10 |
| `Clear filters` | the value in the item: A work filter matching nothing shows Nothing matches that., the active filters, (this value). | C-CF-111 | Core features rule 10 |
| `paragraph` | the value in the item: The body block kinds are (this value), heading, image, image_pair, quote, facts. | C-CF-121 | Core features rule 11 |
| `heading` | the value in the item: The body block kinds are paragraph, (this value), image, image_pair, quote, facts. | C-CF-121 | Core features rule 11 |
| `image` | the value in the item: The body block kinds are paragraph, heading, (this value), image_pair, quote, facts. | C-CF-121 | Core features rule 11 |
| `image_pair` | the value in the item: The body block kinds are paragraph, heading, image, (this value), quote, facts. | C-CF-121 | Core features rule 11 |
| `quote` | the value in the item: The body block kinds are paragraph, heading, image, image_pair, (this value), facts. | C-CF-121 | Core features rule 11 |
| `facts` | the value in the item: The body block kinds are paragraph, heading, image, image_pair, quote, (this value). | C-CF-121 | Core features rule 11 |
| `/expertise/real-estate` | the value in the item: The four landings are (this value), /expertise/corporate, /expertise/startups, /expertise/ecommerce. | C-CF-124 | Core features rule 12 |
| `/expertise/corporate` | the value in the item: The four landings are /expertise/real-estate, (this value), /expertise/startups, /expertise/ecommerce. | C-CF-124 | Core features rule 12 |
| `/expertise/startups` | the value in the item: The four landings are /expertise/real-estate, /expertise/corporate, (this value), /expertise/ecommerce. | C-CF-124 | Core features rule 12 |
| `/expertise/ecommerce` | the value in the item: The four landings are /expertise/real-estate, /expertise/corporate, /expertise/startups, (this value). | C-CF-124 | Core features rule 12 |
| `We operate worldwide. Choose the office nearest to you` | the value in the item: The contact page carries (this value). | C-CF-129 | Core features rule 13 |
| `Riga, Latvia` | the value in the item: The contact page lists the offices (this value), Oslo, Norway. | C-CF-130 | Core features rule 13 |
| `Oslo, Norway` | the value in the item: The contact page lists the offices Riga, Latvia, (this value). | C-CF-130 | Core features rule 13 |
| `Get in touch` | the value in the item: The brief form carries the heading (this value). | C-CF-131 | Core features rule 13 |
| `Your name` | the value in the item: The brief form fields run (this value), Company name, Phone number, E-mail, Comment in order. | C-CF-132 | Core features rule 13 |
| `Company name` | the value in the item: The brief form fields run Your name, (this value), Phone number, E-mail, Comment in order. | C-CF-132 | Core features rule 13 |
| `Phone number` | the value in the item: The brief form fields run Your name, Company name, (this value), E-mail, Comment in order. | C-CF-132 | Core features rule 13 |
| `E-mail` | the value in the item: The brief form fields run Your name, Company name, Phone number, (this value), Comment in order. | C-CF-132 | Core features rule 13 |
| `Comment` | the value in the item: The brief form fields run Your name, Company name, Phone number, E-mail, (this value) in order. | C-CF-132 | Core features rule 13 |
| `(optional)` | the value in the item: The brief form marks Company name with (this value). | C-CF-133 | Core features rule 13 |
| `under_25k` | the value in the item: The brief budget values are (this value), 25k_to_75k, 75k_to_150k, over_150k, all optional. | C-CF-135 | Core features rule 13 |
| `25k_to_75k` | the value in the item: The brief budget values are under_25k, (this value), 75k_to_150k, over_150k, all optional. | C-CF-135 | Core features rule 13 |
| `75k_to_150k` | the value in the item: The brief budget values are under_25k, 25k_to_75k, (this value), over_150k, all optional. | C-CF-135 | Core features rule 13 |
| `over_150k` | the value in the item: The brief budget values are under_25k, 25k_to_75k, 75k_to_150k, (this value), all optional. | C-CF-135 | Core features rule 13 |
| `Under 25k` | the value in the item: The budget choices show to the visitor as (this value), 25k to 75k, 75k to 150k, Over 150k. | C-CF-136 | Core features rule 13 |
| `25k to 75k` | the value in the item: The budget choices show to the visitor as Under 25k, (this value), 75k to 150k, Over 150k. | C-CF-136 | Core features rule 13 |
| `75k to 150k` | the value in the item: The budget choices show to the visitor as Under 25k, 25k to 75k, (this value), Over 150k. | C-CF-136 | Core features rule 13 |
| `Over 150k` | the value in the item: The budget choices show to the visitor as Under 25k, 25k to 75k, 75k to 150k, (this value). | C-CF-136 | Core features rule 13 |
| `Choose one of the listed expertises.` | the value in the item: A brief naming an unknown expertise is refused under the expertise field with (this value) | C-CF-137 | Core features rule 13 |
| `Choose one of the listed budgets.` | the value in the item: A brief naming an unknown budget is refused under the budget field with (this value) | C-CF-138 | Core features rule 13 |
| `A few more words, please.` | the value in the item: A comment breaking both comment rules shows only (this value) | C-CF-139 | Core features rule 13 |
| `By clicking the Submit button you agree to our Privacy Policy terms` | the value in the item: The brief form carries the consent line (this value). | C-CF-141 | Core features rule 13 |
| `Submit` | the value in the item: The brief form ends with the large round (this value) button. | C-CF-142 | Core features rule 13 |
| `Tell us what to call you.` | the value in the item: A brief with an empty name is refused with (this value) | C-CF-146 | Core features rule 13 table row 1 |
| `120` | the value in the item: A brief company runs 0 to (this value) characters. | C-CF-147 | Core features rule 13 table row 2 |
| `That number looks incomplete.` | the value in the item: A brief phone with fewer than six digits is refused with (this value) | C-CF-148 | Core features rule 13 table row 3 |
| `6` | the value in the item: A brief phone, when given, holds (this value) to 20 digits. | C-CF-149 | Core features rule 13 table row 3 |
| `20` | the value in the item: A brief phone, when given, holds 6 to (this value) digits. | C-CF-149 | Core features rule 13 table row 3 |
| `That address will not reach you.` | the value in the item: A brief with an invalid email is refused with (this value) | C-CF-150 | Core features rule 13 table row 4 |
| `Fewer links, please.` | the value in the item: A brief comment with more than two web addresses is refused with (this value) | C-CF-153 | Core features rule 13 table row 6 |
| `80` | the value in the item: A brief name runs 1 to (this value) characters. | C-CF-154 | Core features rule 13 table row 1 |
| `10` | the value in the item: A brief comment runs (this value) to 4000 characters. | C-CF-156 | Core features rule 13 table row 5 |
| `4000` | the value in the item: A brief comment runs 10 to (this value) characters. | C-CF-156 | Core features rule 13 table row 5 |
| `254` | the value in the item: A brief email runs 1 to (this value) characters. | C-CF-158 | Core features rule 13 table row 4 |
| `Thank you!` | the value in the item: An accepted brief replaces the form in place with (this value), We'll be in touch soonest!, Homepage. | C-CF-163 | Core features rule 13 |
| `We'll be in touch soonest!` | the value in the item: An accepted brief replaces the form in place with Thank you!, (this value), Homepage. | C-CF-163 | Core features rule 13 |
| `Homepage` | the value in the item: An accepted brief replaces the form in place with Thank you!, We'll be in touch soonest!, (this value). | C-CF-163 | Core features rule 13 |
| `source_path` | the value in the item: An accepted brief records the page the visitor was on as (this value). | C-CF-164 | Core features rule 13 |
| `website` | the value in the item: A brief whose hidden (this value) field is filled is spam that stores nothing. | C-CF-165 | Core features rule 14 |
| `form_token` | the value in the item: A brief whose (this value) is under two seconds old is spam that stores nothing. | C-CF-166 | Core features rule 14 |
| `GET /api/briefs/token` | the value in the item: The route (this value) issues the brief form_token. | C-CF-171 | Core features rule 14 |
| `unread` | the value in the item: An accepted brief lands in the brief inbox as (this value). | C-CF-175 | Core features rule 15 |
| `/studio/inbox` | the value in the item: Only the owner reaches the brief inbox at (this value). | C-CF-176 | Core features rule 15 |
| `/studio/inbox/<id>` | the value in the item: An opened brief has an address of the form (this value). | C-CF-183 | Core features rule 15 |
| `Archive` | the value in the item: An opened brief offers (this value), Mark unread, Delete, Reply. | C-CF-185 | Core features rule 15 |
| `Mark unread` | the value in the item: An opened brief offers Archive, (this value), Delete, Reply. | C-CF-185 | Core features rule 15 |
| `Delete` | the value in the item: An opened brief offers Archive, Mark unread, (this value), Reply. | C-CF-185 | Core features rule 15 |
| `Reply` | the value in the item: An opened brief offers Archive, Mark unread, Delete, (this value). | C-CF-185 | Core features rule 15 |
| `read` | the value in the item: Opening a brief in the inbox marks the brief (this value). | C-CF-187 | Core features rule 15 |
| `GET /api/studio/briefs/{id}` | the value in the item: Reading a brief through (this value) leaves the brief state unchanged. | C-CF-188 | Core features rule 15 |
| `archived` | the value in the item: An archived brief becomes (this value). | C-CF-189 | Core features rule 15 |
| `Ines Duval` | the value in the item: The seeded brief from (this value) carries markup in the brief comment. | C-CF-193 | Core features rule 15 |
| `Inbox` | the value in the item: The studio rail shows the unread count beside (this value). | C-CF-194 | Core features rule 15 |
| `Published work` | the value in the item: The dashboard shows the tiles (this value), Drafts to everyone signed in. | C-CF-198 | Core features rule 16 |
| `Drafts` | the value in the item: The dashboard shows the tiles Published work, (this value) to everyone signed in. | C-CF-198 | Core features rule 16 |
| `unread_briefs` | the value in the item: The owner dashboard carries the unread brief count as (this value). | C-CF-200 | Core features rule 16 |
| `Unread briefs` | the value in the item: An editor dashboard shows no (this value) tile. | C-CF-202 | Core features rule 16 |
| `recent` | the value in the item: Each dashboard (this value) row carries kind, id, title, changed_at. | C-CF-206 | Core features rule 16 |
| `kind` | the value in the item: Each dashboard recent row carries (this value), id, title, changed_at. | C-CF-206 | Core features rule 16 |
| `id` | the value in the item: Each dashboard recent row carries kind, (this value), title, changed_at. | C-CF-206 | Core features rule 16 |
| `title` | the value in the item: Each dashboard recent row carries kind, id, (this value), changed_at. | C-CF-206 | Core features rule 16 |
| `changed_at` | the value in the item: Each dashboard recent row carries kind, id, title, (this value). | C-CF-206 | Core features rule 16 |
| `case_study` | the value in the item: A dashboard recent row kind is (this value) or brief. | C-CF-207 | Core features rule 16 |
| `brief` | the value in the item: A dashboard recent row kind is case_study or (this value). | C-CF-207 | Core features rule 16 |
| `/studio/work/new` | the value in the item: The case study editor lives at (this value), /studio/work/<id> as dedicated routes. | C-CF-208 | Core features rule 17 |
| `/studio/work/<id>` | the value in the item: The case study editor lives at /studio/work/new, (this value) as dedicated routes. | C-CF-208 | Core features rule 17 |
| `1990` | the value in the item: A case study year is four digits from (this value) to the current year. | C-CF-213 | Core features rule 17 |
| `280` | the value in the item: A case study summary runs 0 to (this value) characters. | C-CF-214 | Core features rule 17 |
| `Save` | the value in the item: Pressing (this value) shows Saved just now. | C-CF-219 | Core features rule 17 |
| `Saved just now.` | the value in the item: Pressing Save shows (this value) | C-CF-219 | Core features rule 17 |
| `Publish` | the value in the item: The controls (this value), Unpublish appear for the owner only. | C-CF-220 | Core features rule 17 |
| `Unpublish` | the value in the item: The controls Publish, (this value) appear for the owner only. | C-CF-220 | Core features rule 17 |
| `Published.` | the value in the item: Publishing shows the status line beginning (this value) | C-CF-221 | Core features rule 17 |
| `Published. It is on the site now.` | the full wording the item quotes in part | C-CF-221 | Core features rule 17 |
| `Unpublished.` | the value in the item: Unpublishing shows the status line beginning (this value) | C-CF-222 | Core features rule 17 |
| `Unpublished. It is off the site.` | the full wording the item quotes in part | C-CF-222 | Core features rule 17 |
| `That address is already used by another case study.` | the value in the item: A slug already in use is refused with (this value) | C-CF-225 | Core features rule 17 |
| `That did not match.` | the value in the item: A wrong address or password at sign in is refused with the line beginning (this value) | C-CF-226 | Core features rule 18 |
| `That did not match. Check both fields and try again.` | the full wording the item quotes in part | C-CF-226 | Core features rule 18 |
| `Too many attempts.` | the value in the item: A locked account refuses the right password with a line beginning (this value) | C-CF-229 | Core features rule 18 |
| `/sign-in?next=` | the value in the item: A signed-out request for a studio route goes to (this value) followed by the intended path. | C-CF-230 | Core features rule 18 |
| `/studio` | the value in the item: A return path other than one leading slash with a studio route lands on (this value). | C-CF-232 | Core features rule 18 |
| `A revoked session ends` | the value in the item: The account page carries the note beginning (this value). | C-CF-235 | Core features rule 19 |
| `A revoked session ends the next time it is used.` | the full wording the item quotes in part | C-CF-235 | Core features rule 19 |
| `GET /api/sessions` | the value in the item: The route (this value) lists the live sessions of the signed-in account. | C-CF-236 | Core features rule 19 |
| `user_agent_summary` | the value in the item: Each session carries id, (this value), created_at, last_seen_at, current. | C-CF-237 | Core features rule 19 |
| `created_at` | the value in the item: Each session carries id, user_agent_summary, (this value), last_seen_at, current. | C-CF-237 | Core features rule 19 |
| `last_seen_at` | the value in the item: Each session carries id, user_agent_summary, created_at, (this value), current. | C-CF-237 | Core features rule 19 |
| `current` | the value in the item: Each session carries id, user_agent_summary, created_at, last_seen_at, (this value). | C-CF-237 | Core features rule 19 |
| `Sign out everywhere` | the value in the item: The control (this value) ends every session of the account, the current session included. | C-CF-239 | Core features rule 19 |
| `403` | the value in the item: A role-refused studio route shows a designed page with (this value), Not permitted, Back to studio. | C-CF-241 | Core features rule 20 |
| `Not permitted` | the value in the item: A role-refused studio route shows a designed page with 403, (this value), Back to studio. | C-CF-241 | Core features rule 20 |
| `Back to studio` | the value in the item: A role-refused studio route shows a designed page with 403, Not permitted, (this value). | C-CF-241 | Core features rule 20 |
| `Briefs are visible to the owner only.` | the value in the item: The inbox refusal page adds (this value) | C-CF-244 | Core features rule 20 |
| `404` | the value in the item: The not found page shows (this value) as large as the front page headline with Not found, Back to work. | C-CF-247 | Core features rule 21 |
| `Not found` | the value in the item: The not found page shows 404 as large as the front page headline with (this value), Back to work. | C-CF-247 | Core features rule 21 |
| `Back to work` | the value in the item: The not found page shows 404 as large as the front page headline with Not found, (this value). | C-CF-247 | Core features rule 21 |
| `410` | the value in the item: The gone surface reads (this value), No longer here, Back to work. | C-CF-249 | Core features rule 21 |
| `/privacy-policy` | the value in the item: The privacy notice at (this value) states that each public page view is kept as the route with the time. | C-CF-250 | Core features rule 21 |
| `/sitemap.xml` | the value in the item: The file (this value) lists every public route with every published case study, every landing. | C-CF-270 | Core features rule 23 |
| `/robots.txt` | the value in the item: The file (this value) names the sitemap. | C-CF-272 | Core features rule 23 |
| `You are offline.` | the value in the item: Offline, the brief form shows (this value) followed by Your brief is saved here with the reconnect clause. | C-CF-285 | Core features rule 26 |
| `Your brief is saved here` | the value in the item: Offline, the brief form shows You are offline. followed by (this value) with the reconnect clause. | C-CF-285 | Core features rule 26 |
| `You are offline. Your brief is saved here and will send when you reconnect.` | the full wording the item quotes in part | C-CF-285 | Core features rule 26 |
| `/work` | the value in the item: The route (this value) shows every published case study. | C-UF-02 | User flow table row 2 |
| `/work/<slug>` | the value in the item: The route (this value) shows one published case study with the next. | C-UF-03 | User flow table row 3 |
| `/company` | the value in the item: The route (this value) shows the company page. | C-UF-04 | User flow table row 5 |
| `/contact` | the value in the item: The route (this value) shows the offices with the brief form. | C-UF-05 | User flow table row 6 |
| `/studio/work` | the value in the item: The studio work list at (this value) shows every case study, draft or published, to the owner, the editor. | C-UF-08 | User flow table row 10 |
| `/studio/page-views` | the value in the item: The page-view route (this value) is reachable by the owner only. | C-UF-10 | User flow table row 14 |
| `/studio/account` | the value in the item: The account route (this value) is reachable by the owner, the editor. | C-UF-11 | User flow table row 15 |
| `Expertise` | the value in the item: The header control (this value) opens a panel of the four expertises. | C-UF-15 | User flow entry and redirects |
| `Aster Row Residences` | the value in the item: The owner journey publishes (this value) for the client Halden in 2025. | C-UF-17 | User flow owner journey |
| `Halden` | the value in the item: The owner journey publishes Aster Row Residences for the client (this value) in 2025. | C-UF-17 | User flow owner journey |
| `2025` | the value in the item: The owner journey publishes Aster Row Residences for the client Halden in (this value). | C-UF-17 | User flow owner journey |
| `Harbour Quarter` | the value in the item: The case study (this value) stays on the public work index after leaving the slot. | C-UF-22 | User flow owner journey |
| `?expertise=corporate` | the value in the item: The visitor journey filters the work index to Corporate, the address gaining (this value). | C-UF-23 | User flow visitor journey |
| `Banking` | the value in the item: The visitor journey adds the tag (this value) to the work filter. | C-UF-24 | User flow visitor journey |
| `Kestrel Annual Review` | the value in the item: The visitor journey opens (this value). | C-UF-25 | User flow visitor journey |
| `Northline Self Care` | the value in the item: The withdraw journey unpublishes (this value). | C-UF-32 | User flow owner withdraws |
| `New case study` | the value in the item: The primary action on the contact page is the large round Submit, on the dashboard (this value). | C-UX-24 | UI/UX notes |
| `Inter Tight` | type family | C-FE-01 | Front-end specification type |
| `400` | the value in the item: The regular cut (this value) sets body, interface, captions. | C-FE-02 | Front-end specification type |
| `500` | the value in the item: The medium cut (this value) sets headings with the current navigation item. | C-FE-03 | Front-end specification type |
| `180px` | the value in the item: The display size (this value) sets the headline, the company figure, a failure code. | C-FE-05 | Front-end specification type |
| `90px` | the value in the item: The first heading is (this value); the third heading is 38px. | C-FE-06 | Front-end specification type |
| `38px` | the value in the item: The first heading is 90px; the third heading is (this value). | C-FE-06 | Front-end specification type |
| `22px` | the value in the item: Body is (this value), interface 16px, small 14px, caption 12px. | C-FE-07 | Front-end specification type |
| `16px` | the value in the item: Body is 22px, interface (this value), small 14px, caption 12px. | C-FE-07 | Front-end specification type |
| `14px` | the value in the item: Body is 22px, interface 16px, small (this value), caption 12px. | C-FE-07 | Front-end specification type |
| `12px` | the value in the item: Body is 22px, interface 16px, small 14px, caption (this value). | C-FE-07 | Front-end specification type |
| `10px` | the value in the item: The breadcrumb, the consent line are (this value), never scaled, never tracked. | C-FE-08 | Front-end specification type |
| `"Helvetica Neue", Helvetica, Arial, system-ui, sans-serif` | the value in the item: The type fallback is (this value), adjusted against reflow. | C-FE-10 | Front-end specification type |
| `Northform` | the value in the item: The header carries the wordmark (this value), the Expertise control, the links Work, Company, Contact. | C-FE-11 | Front-end specification global chrome |
| `Work` | the value in the item: The header carries the wordmark Northform, the Expertise control, the links (this value), Company, Contact. | C-FE-11 | Front-end specification global chrome |
| `Company` | the value in the item: The header carries the wordmark Northform, the Expertise control, the links Work, (this value), Contact. | C-FE-11 | Front-end specification global chrome |
| `Contact` | the value in the item: The header carries the wordmark Northform, the Expertise control, the links Work, Company, (this value). | C-FE-11 | Front-end specification global chrome |
| `Get In Touch` | the value in the item: The footer carries (this value) above five social links Network One to Network Five with rules between. | C-FE-18 | Front-end specification global chrome |
| `Network One` | the value in the item: The footer carries Get In Touch above five social links (this value) to Network Five with rules between. | C-FE-18 | Front-end specification global chrome |
| `Network Five` | the value in the item: The footer carries Get In Touch above five social links Network One to (this value) with rules between. | C-FE-18 | Front-end specification global chrome |
| `1998` | the value in the item: The footer carries the copyright sign, (this value), a hyphen, the current year. | C-FE-19 | Front-end specification global chrome |
| `Privacy Policy` | the value in the item: The footer carries a (this value) link. | C-FE-20 | Front-end specification global chrome |
| `website uses cookies` | the value in the item: The cookie bar notice about (this value) offers Accept. | C-FE-21 | Front-end specification global chrome |
| `Accept` | the value in the item: The cookie bar notice about website uses cookies offers (this value). | C-FE-21 | Front-end specification global chrome |
| `This website uses cookies` | the full wording the item quotes in part | C-FE-21 | Front-end specification global chrome |
| `Skip to content` | the value in the item: The skip link reads (this value). | C-FE-23 | Front-end specification global chrome |
| `Watch showreel` | the value in the item: On a laptop the showreel shows a trailing round label (this value). | C-FE-37 | Front-end specification the cursor and the showreel |
| `Drag` | the value in the item: On a laptop the client strip shows a trailing round label (this value). | C-FE-38 | Front-end specification the cursor and the showreel |
| `Luxury real estate website design - iconic websites for iconic properties.` | the value in the item: The expertise sentences begin (this value), Inspiring, functional,, From idea to a product:, High-class eCommerce solutions. | C-FE-47 | Front-end specification the copy deck |
| `Inspiring, functional,` | the value in the item: The expertise sentences begin Luxury real estate website design - iconic websites for iconic properties., (this value), From idea to a product:, High-class eCommerce solutions. | C-FE-47 | Front-end specification the copy deck |
| `From idea to a product:` | the value in the item: The expertise sentences begin Luxury real estate website design - iconic websites for iconic properties., Inspiring, functional,, (this value), High-class eCommerce solutions. | C-FE-47 | Front-end specification the copy deck |
| `High-class eCommerce solutions` | the value in the item: The expertise sentences begin Luxury real estate website design - iconic websites for iconic properties., Inspiring, functional,, From idea to a product:, (this value). | C-FE-47 | Front-end specification the copy deck |
| `Inspiring, functional, and result-oriented websites for enterprises. Full-cycle award-winning solutions from strategy to launch.` | the full wording the item quotes in part | C-FE-47 | Front-end specification the copy deck |
| `From idea to a product: creating successful digital services for innovative startups and established businesses.` | the full wording the item quotes in part | C-FE-47 | Front-end specification the copy deck |
| `High-class eCommerce solutions with research-grounded UX design, award-class UI design and top-grade front-end.` | the full wording the item quotes in part | C-FE-47 | Front-end specification the copy deck |
| `Web & mobile apps` | the value in the item: The capability headings are (this value), UX & product design, Product development, Award-class web design, Communication design. | C-FE-48 | Front-end specification the copy deck |
| `UX & product design` | the value in the item: The capability headings are Web & mobile apps, (this value), Product development, Award-class web design, Communication design. | C-FE-48 | Front-end specification the copy deck |
| `Product development` | the value in the item: The capability headings are Web & mobile apps, UX & product design, (this value), Award-class web design, Communication design. | C-FE-48 | Front-end specification the copy deck |
| `Award-class web design` | the value in the item: The capability headings are Web & mobile apps, UX & product design, Product development, (this value), Communication design. | C-FE-48 | Front-end specification the copy deck |
| `Communication design` | the value in the item: The capability headings are Web & mobile apps, UX & product design, Product development, Award-class web design, (this value). | C-FE-48 | Front-end specification the copy deck |
| `Services, self-care, eCommerce, payments,` | the value in the item: The capability bodies begin (this value), User research, journey maps,, Minimum viable, World-class advanced promotional, Naming, branding, communication strategy,. | C-FE-49 | Front-end specification the copy deck |
| `User research, journey maps,` | the value in the item: The capability bodies begin Services, self-care, eCommerce, payments,, (this value), Minimum viable, World-class advanced promotional, Naming, branding, communication strategy,. | C-FE-49 | Front-end specification the copy deck |
| `Minimum viable` | the value in the item: The capability bodies begin Services, self-care, eCommerce, payments,, User research, journey maps,, (this value), World-class advanced promotional, Naming, branding, communication strategy,. | C-FE-49 | Front-end specification the copy deck |
| `World-class advanced promotional` | the value in the item: The capability bodies begin Services, self-care, eCommerce, payments,, User research, journey maps,, Minimum viable, (this value), Naming, branding, communication strategy,. | C-FE-49 | Front-end specification the copy deck |
| `Naming, branding, communication strategy,` | the value in the item: The capability bodies begin Services, self-care, eCommerce, payments,, User research, journey maps,, Minimum viable, World-class advanced promotional, (this value). | C-FE-49 | Front-end specification the copy deck |
| `Services, self-care, eCommerce, payments, custom apps for enterprises and startups.` | the full wording the item quotes in part | C-FE-49 | Front-end specification the copy deck |
| `User research, journey maps, prototyping, value proposition validation, design iterations, design systems and interface kits.` | the full wording the item quotes in part | C-FE-49 | Front-end specification the copy deck |
| `Minimum viable and lovable products, fast prototyping, agile development, modern front-end frameworks, a mature back-end framework, cloud infrastructure, support, maintenance, scaling.` | the full wording the item quotes in part | C-FE-49 | Front-end specification the copy deck |
| `World-class advanced promotional and corporate creative websites.` | the full wording the item quotes in part | C-FE-49 | Front-end specification the copy deck |
| `Naming, branding, communication strategy, 3D, print, copywriting.` | the full wording the item quotes in part | C-FE-49 | Front-end specification the copy deck |
| `We are a strategic partner to our clients.` | the value in the item: The company copy reads (this value) followed by We will help you to ideate, design. | C-FE-50 | Front-end specification the copy deck |
| `We will help you to ideate, design` | the value in the item: The company copy reads We are a strategic partner to our clients. followed by (this value). | C-FE-50 | Front-end specification the copy deck |
| `We are a strategic partner to our clients. We will help you to ideate, design and implement your product from beginning to end.` | the full wording the item quotes in part | C-FE-50 | Front-end specification the copy deck |
| `Meridian Air` | the value in the item: The clients are (this value), Halden, Northline, Kestrel Bank, Ostend Credit, Vantage, Pinemark. | C-FE-51 | Front-end specification the copy deck |
| `Northline` | the value in the item: The clients are Meridian Air, Halden, (this value), Kestrel Bank, Ostend Credit, Vantage, Pinemark. | C-FE-51 | Front-end specification the copy deck |
| `Kestrel Bank` | the value in the item: The clients are Meridian Air, Halden, Northline, (this value), Ostend Credit, Vantage, Pinemark. | C-FE-51 | Front-end specification the copy deck |
| `Ostend Credit` | the value in the item: The clients are Meridian Air, Halden, Northline, Kestrel Bank, (this value), Vantage, Pinemark. | C-FE-51 | Front-end specification the copy deck |
| `Vantage` | the value in the item: The clients are Meridian Air, Halden, Northline, Kestrel Bank, Ostend Credit, (this value), Pinemark. | C-FE-51 | Front-end specification the copy deck |
| `Pinemark` | the value in the item: The clients are Meridian Air, Halden, Northline, Kestrel Bank, Ostend Credit, Vantage, (this value). | C-FE-51 | Front-end specification the copy deck |
| `promo-website` | the value in the item: The eleven tag slugs are (this value), corporate-website, online-store, self-service, saas, banking, customer-portal, trading-platform, branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `corporate-website` | the value in the item: The eleven tag slugs are promo-website, (this value), online-store, self-service, saas, banking, customer-portal, trading-platform, branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `online-store` | the value in the item: The eleven tag slugs are promo-website, corporate-website, (this value), self-service, saas, banking, customer-portal, trading-platform, branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `self-service` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, (this value), saas, banking, customer-portal, trading-platform, branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `saas` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, self-service, (this value), banking, customer-portal, trading-platform, branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `banking` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, self-service, saas, (this value), customer-portal, trading-platform, branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `customer-portal` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, self-service, saas, banking, (this value), trading-platform, branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `trading-platform` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, self-service, saas, banking, customer-portal, (this value), branding, 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `branding` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, self-service, saas, banking, customer-portal, trading-platform, (this value), 3d-visualisation, real-estate. | C-FE-52 | Front-end specification the copy deck |
| `3d-visualisation` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, self-service, saas, banking, customer-portal, trading-platform, branding, (this value), real-estate. | C-FE-52 | Front-end specification the copy deck |
| `real-estate` | the value in the item: The eleven tag slugs are promo-website, corporate-website, online-store, self-service, saas, banking, customer-portal, trading-platform, branding, 3d-visualisation, (this value). | C-FE-52 | Front-end specification the copy deck |
| `Promo Website` | the value in the item: The eleven tag names are (this value), Corporate Website, Online Store, Self-Service, SaaS, Banking, Customer Portal, Trading Platform, Branding, 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `Corporate Website` | the value in the item: The eleven tag names are Promo Website, (this value), Online Store, Self-Service, SaaS, Banking, Customer Portal, Trading Platform, Branding, 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `Online Store` | the value in the item: The eleven tag names are Promo Website, Corporate Website, (this value), Self-Service, SaaS, Banking, Customer Portal, Trading Platform, Branding, 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `Self-Service` | the value in the item: The eleven tag names are Promo Website, Corporate Website, Online Store, (this value), SaaS, Banking, Customer Portal, Trading Platform, Branding, 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `SaaS` | the value in the item: The eleven tag names are Promo Website, Corporate Website, Online Store, Self-Service, (this value), Banking, Customer Portal, Trading Platform, Branding, 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `Customer Portal` | the value in the item: The eleven tag names are Promo Website, Corporate Website, Online Store, Self-Service, SaaS, Banking, (this value), Trading Platform, Branding, 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `Trading Platform` | the value in the item: The eleven tag names are Promo Website, Corporate Website, Online Store, Self-Service, SaaS, Banking, Customer Portal, (this value), Branding, 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `Branding` | the value in the item: The eleven tag names are Promo Website, Corporate Website, Online Store, Self-Service, SaaS, Banking, Customer Portal, Trading Platform, (this value), 3D & Visualisation, Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `3D & Visualisation` | the value in the item: The eleven tag names are Promo Website, Corporate Website, Online Store, Self-Service, SaaS, Banking, Customer Portal, Trading Platform, Branding, (this value), Real Estate. | C-FE-53 | Front-end specification the copy deck |
| `corporate` | the value in the item: The four expertise slugs in order are real-estate, (this value), startups, ecommerce. | C-FE-54 | Front-end specification the copy deck |
| `startups` | the value in the item: The four expertise slugs in order are real-estate, corporate, (this value), ecommerce. | C-FE-54 | Front-end specification the copy deck |
| `ecommerce` | the value in the item: The four expertise slugs in order are real-estate, corporate, startups, (this value). | C-FE-54 | Front-end specification the copy deck |
| `Shelf` | the value in the item: The studio rail reads Work, (this value), Inbox, Page views, Account. | C-FE-55 | Front-end specification the copy deck |
| `Page views` | the value in the item: The studio rail reads Work, Shelf, Inbox, (this value), Account. | C-FE-55 | Front-end specification the copy deck |
| `Account` | the value in the item: The studio rail reads Work, Shelf, Inbox, Page views, (this value). | C-FE-55 | Front-end specification the copy deck |
| `Sign in` | the value in the item: The studio controls read New case study, Save, Publish, Unpublish, Delete, Generate cover, Archive, Mark unread, Reply, Keep mine, Take theirs, (this value), Sign out everywhere, Back to studio, Back to work. | C-FE-57 | Front-end specification the copy deck |
| `Nothing featured.` | the value in the item: An empty shelf slot reads (this value) | C-FE-58 | Front-end specification the copy deck |
| `Angular` | the value in the item: The browser receives a single-page application built with (this value) in TypeScript. | C-TR-01 | Technical requirements |
| `Express` | the value in the item: The server is (this value) in TypeScript. | C-TR-02 | Technical requirements |
| `PostgreSQL` | the value in the item: Case studies, tags, expertises, slots, briefs, sessions, accounts, page views live in (this value) at DATABASE_URL. | C-TR-04 | Technical requirements |
| `DATABASE_URL` | the value in the item: Case studies, tags, expertises, slots, briefs, sessions, accounts, page views live in PostgreSQL at (this value). | C-TR-04 | Technical requirements |
| `STORAGE_ENDPOINT` | the value in the item: Covers live in minio at (this value). | C-TR-05 | Technical requirements |
| `STORAGE_BUCKET` | the value in the item: The bucket is named by (this value). | C-TR-06 | Technical requirements |
| `STORAGE_ACCESS_KEY` | the value in the item: The storage key pair comes from (this value), STORAGE_SECRET_KEY. | C-TR-07 | Technical requirements |
| `STORAGE_SECRET_KEY` | the value in the item: The storage key pair comes from STORAGE_ACCESS_KEY, (this value). | C-TR-07 | Technical requirements |
| `GET /api/covers/{id}` | the value in the item: Cover bytes reach the browser through (this value), which checks the case study state on every request. | C-TR-08 | Technical requirements |
| `POST /api/auth/login` | the value in the item: The route (this value) returns an access_token accepted as a bearer token. | C-TR-13 | Technical requirements |
| `access_token` | the value in the item: The route POST /api/auth/login returns an (this value) accepted as a bearer token. | C-TR-13 | Technical requirements |
| `error` | the value in the item: A refusal answers with an (this value) object holding code, message, fields. | C-TR-23 | Technical requirements |
| `code` | the value in the item: A refusal answers with an error object holding (this value), message, fields. | C-TR-23 | Technical requirements |
| `message` | the value in the item: A refusal answers with an error object holding code, (this value), fields. | C-TR-23 | Technical requirements |
| `fields` | the value in the item: A refusal answers with an error object holding code, message, (this value). | C-TR-23 | Technical requirements |
| `bad_request` | the value in the item: The refusal code is one of (this value), unauthenticated, forbidden, not_found, gone, conflict, unprocessable, rate_limited, locked. | C-TR-24 | Technical requirements |
| `unauthenticated` | the value in the item: The refusal code is one of bad_request, (this value), forbidden, not_found, gone, conflict, unprocessable, rate_limited, locked. | C-TR-24 | Technical requirements |
| `forbidden` | the value in the item: The refusal code is one of bad_request, unauthenticated, (this value), not_found, gone, conflict, unprocessable, rate_limited, locked. | C-TR-24 | Technical requirements |
| `not_found` | the value in the item: The refusal code is one of bad_request, unauthenticated, forbidden, (this value), gone, conflict, unprocessable, rate_limited, locked. | C-TR-24 | Technical requirements |
| `gone` | the value in the item: The refusal code is one of bad_request, unauthenticated, forbidden, not_found, (this value), conflict, unprocessable, rate_limited, locked. | C-TR-24 | Technical requirements |
| `conflict` | the value in the item: The refusal code is one of bad_request, unauthenticated, forbidden, not_found, gone, (this value), unprocessable, rate_limited, locked. | C-TR-24 | Technical requirements |
| `unprocessable` | the value in the item: The refusal code is one of bad_request, unauthenticated, forbidden, not_found, gone, conflict, (this value), rate_limited, locked. | C-TR-24 | Technical requirements |
| `rate_limited` | the value in the item: The refusal code is one of bad_request, unauthenticated, forbidden, not_found, gone, conflict, unprocessable, (this value), locked. | C-TR-24 | Technical requirements |
| `locked` | the value in the item: The refusal code is one of bad_request, unauthenticated, forbidden, not_found, gone, conflict, unprocessable, rate_limited, (this value). | C-TR-24 | Technical requirements |
| `/app/USER_README.md` | where logins are written | C-DM-02 | Data model |
| `accounts` | the value in the item: The (this value) table holds id, email, password_hash, display_name, role, failed_attempts, locked_until, created_at. | C-DM-03 | Data model accounts |
| `email` | the value in the item: The accounts table holds id, (this value), password_hash, display_name, role, failed_attempts, locked_until, created_at. | C-DM-03 | Data model accounts |
| `password_hash` | the value in the item: The accounts table holds id, email, (this value), display_name, role, failed_attempts, locked_until, created_at. | C-DM-03 | Data model accounts |
| `display_name` | the value in the item: The accounts table holds id, email, password_hash, (this value), role, failed_attempts, locked_until, created_at. | C-DM-03 | Data model accounts |
| `role` | the value in the item: The accounts table holds id, email, password_hash, display_name, (this value), failed_attempts, locked_until, created_at. | C-DM-03 | Data model accounts |
| `failed_attempts` | the value in the item: The accounts table holds id, email, password_hash, display_name, role, (this value), locked_until, created_at. | C-DM-03 | Data model accounts |
| `locked_until` | the value in the item: The accounts table holds id, email, password_hash, display_name, role, failed_attempts, (this value), created_at. | C-DM-03 | Data model accounts |
| `sessions` | the value in the item: The (this value) table holds id, account_id, token_hash, user_agent_summary, created_at, last_seen_at, expires_at, revoked_at. | C-DM-05 | Data model sessions |
| `account_id` | the value in the item: The sessions table holds id, (this value), token_hash, user_agent_summary, created_at, last_seen_at, expires_at, revoked_at. | C-DM-05 | Data model sessions |
| `token_hash` | the value in the item: The sessions table holds id, account_id, (this value), user_agent_summary, created_at, last_seen_at, expires_at, revoked_at. | C-DM-05 | Data model sessions |
| `expires_at` | the value in the item: The sessions table holds id, account_id, token_hash, user_agent_summary, created_at, last_seen_at, (this value), revoked_at. | C-DM-05 | Data model sessions |
| `revoked_at` | the value in the item: The sessions table holds id, account_id, token_hash, user_agent_summary, created_at, last_seen_at, expires_at, (this value). | C-DM-05 | Data model sessions |
| `expertises` | the value in the item: The (this value) table holds id, slug, name, sentence, position from 0 to 3. | C-DM-07 | Data model expertises |
| `slug` | the value in the item: The expertises table holds id, (this value), name, sentence, position from 0 to 3. | C-DM-07 | Data model expertises |
| `name` | the value in the item: The expertises table holds id, slug, (this value), sentence, position from 0 to 3. | C-DM-07 | Data model expertises |
| `sentence` | the value in the item: The expertises table holds id, slug, name, (this value), position from 0 to 3. | C-DM-07 | Data model expertises |
| `position` | the value in the item: The expertises table holds id, slug, name, sentence, (this value) from 0 to 3. | C-DM-07 | Data model expertises |
| `3` | the value in the item: The expertises table holds id, slug, name, sentence, position from 0 to (this value). | C-DM-07 | Data model expertises |
| `tags` | the value in the item: The (this value) table holds id, slug, name for exactly the eleven tags. | C-DM-08 | Data model tags |
| `case_studies` | the value in the item: The (this value) table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `client` | the value in the item: The case_studies table holds id, slug, title, (this value), year, expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `year` | the value in the item: The case_studies table holds id, slug, title, client, (this value), expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `expertise_id` | the value in the item: The case_studies table holds id, slug, title, client, year, (this value), summary, cover_seed, cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `summary` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, (this value), cover_seed, cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `cover_seed` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, (this value), cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `cover_palette` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, (this value), cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `cover_id` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, (this value), blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `blocks` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, cover_id, (this value), position, published, published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `published` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, (this value), published_at, withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `published_at` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, published, (this value), withdrawn_at, author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `withdrawn_at` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, published, published_at, (this value), author_id, version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `author_id` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, (this value), version, created_at, updated_at. | C-DM-09 | Data model case_studies |
| `updated_at` | the value in the item: The case_studies table holds id, slug, title, client, year, expertise_id, summary, cover_seed, cover_palette, cover_id, blocks, position, published, published_at, withdrawn_at, author_id, version, created_at, (this value). | C-DM-09 | Data model case_studies |
| `case_study_tags` | the value in the item: The (this value) table holds id, case_study_id, tag_id, each pair once. | C-DM-15 | Data model case_study_tags |
| `case_study_id` | the value in the item: The case_study_tags table holds id, (this value), tag_id, each pair once. | C-DM-15 | Data model case_study_tags |
| `tag_id` | the value in the item: The case_study_tags table holds id, case_study_id, (this value), each pair once. | C-DM-15 | Data model case_study_tags |
| `covers` | the value in the item: The (this value) table holds id, case_study_id, object_key, content_type, byte_size, sha256, width, height, alt_text, created_at. | C-DM-16 | Data model covers |
| `object_key` | the value in the item: The covers table holds id, case_study_id, (this value), content_type, byte_size, sha256, width, height, alt_text, created_at. | C-DM-16 | Data model covers |
| `content_type` | the value in the item: The covers table holds id, case_study_id, object_key, (this value), byte_size, sha256, width, height, alt_text, created_at. | C-DM-16 | Data model covers |
| `byte_size` | the value in the item: The covers table holds id, case_study_id, object_key, content_type, (this value), sha256, width, height, alt_text, created_at. | C-DM-16 | Data model covers |
| `sha256` | the value in the item: The covers table holds id, case_study_id, object_key, content_type, byte_size, (this value), width, height, alt_text, created_at. | C-DM-16 | Data model covers |
| `width` | the value in the item: The covers table holds id, case_study_id, object_key, content_type, byte_size, sha256, (this value), height, alt_text, created_at. | C-DM-16 | Data model covers |
| `height` | the value in the item: The covers table holds id, case_study_id, object_key, content_type, byte_size, sha256, width, (this value), alt_text, created_at. | C-DM-16 | Data model covers |
| `alt_text` | the value in the item: The covers table holds id, case_study_id, object_key, content_type, byte_size, sha256, width, height, (this value), created_at. | C-DM-16 | Data model covers |
| `feature_slots` | the value in the item: The (this value) table holds id, expertise_id, position, case_study_id, version in eight rows. | C-DM-18 | Data model feature_slots |
| `shelf` | the value in the item: The (this value) table holds id, version in one row. | C-DM-20 | Data model shelf |
| `briefs` | the value in the item: The (this value) table holds id, name, company, phone, email, comment, expertise, budget, state, source_path, received_at. | C-DM-22 | Data model briefs |
| `company` | the value in the item: The briefs table holds id, name, (this value), phone, email, comment, expertise, budget, state, source_path, received_at. | C-DM-22 | Data model briefs |
| `phone` | the value in the item: The briefs table holds id, name, company, (this value), email, comment, expertise, budget, state, source_path, received_at. | C-DM-22 | Data model briefs |
| `comment` | the value in the item: The briefs table holds id, name, company, phone, email, (this value), expertise, budget, state, source_path, received_at. | C-DM-22 | Data model briefs |
| `expertise` | the value in the item: The briefs table holds id, name, company, phone, email, comment, (this value), budget, state, source_path, received_at. | C-DM-22 | Data model briefs |
| `budget` | the value in the item: The briefs table holds id, name, company, phone, email, comment, expertise, (this value), state, source_path, received_at. | C-DM-22 | Data model briefs |
| `state` | the value in the item: The briefs table holds id, name, company, phone, email, comment, expertise, budget, (this value), source_path, received_at. | C-DM-22 | Data model briefs |
| `received_at` | the value in the item: The briefs table holds id, name, company, phone, email, comment, expertise, budget, state, source_path, (this value). | C-DM-22 | Data model briefs |
| `page_views` | the value in the item: The (this value) table holds id, route, viewed_at. | C-DM-25 | Data model page_views |
| `route` | the value in the item: The page_views table holds id, (this value), viewed_at. | C-DM-25 | Data model page_views |
| `viewed_at` | the value in the item: The page_views table holds id, route, (this value). | C-DM-25 | Data model page_views |
| `Cliffside Residences` | the value in the item: Twelve case studies are seeded in the pinned shelf order, from (this value) to Pinemark Mobile App. | C-DM-28 | Data model seed data |
| `cliffside-residences` | the value in the item: Seeded shelf place 1 is Cliffside Residences at (this value), client Halden, year 2024, expertise real-estate, published. | C-DM-30 | Data model seed data table |
| `2024` | the value in the item: Seeded shelf place 1 is Cliffside Residences at cliffside-residences, client Halden, year (this value), expertise real-estate, published. | C-DM-30 | Data model seed data table |
| `kestrel-annual-review` | the value in the item: Seeded shelf place 2 is Kestrel Annual Review at (this value), client Kestrel Bank, year 2024, expertise corporate, published. | C-DM-31 | Data model seed data table |
| `Vantage Onboarding` | the value in the item: Seeded shelf place 3 is (this value) at vantage-onboarding, client Vantage, year 2025, expertise startups, published. | C-DM-32 | Data model seed data table |
| `vantage-onboarding` | the value in the item: Seeded shelf place 3 is Vantage Onboarding at (this value), client Vantage, year 2025, expertise startups, published. | C-DM-32 | Data model seed data table |
| `Meridian Duty Free` | the value in the item: Seeded shelf place 4 is (this value) at meridian-duty-free, client Meridian Air, year 2024, expertise ecommerce, published. | C-DM-33 | Data model seed data table |
| `meridian-duty-free` | the value in the item: Seeded shelf place 4 is Meridian Duty Free at (this value), client Meridian Air, year 2024, expertise ecommerce, published. | C-DM-33 | Data model seed data table |
| `harbour-quarter` | the value in the item: Seeded shelf place 5 is Harbour Quarter at (this value), client Northline, year 2023, expertise real-estate, published. | C-DM-34 | Data model seed data table |
| `2023` | the value in the item: Seeded shelf place 5 is Harbour Quarter at harbour-quarter, client Northline, year (this value), expertise real-estate, published. | C-DM-34 | Data model seed data table |
| `ostend-loyalty-store` | the value in the item: Seeded shelf place 6 is Ostend Loyalty Store at (this value), client Ostend Credit, year 2021, expertise ecommerce, withdrawn. | C-DM-35 | Data model seed data table |
| `2021` | the value in the item: Seeded shelf place 6 is Ostend Loyalty Store at ostend-loyalty-store, client Ostend Credit, year (this value), expertise ecommerce, withdrawn. | C-DM-35 | Data model seed data table |
| `Ostend Investor Portal` | the value in the item: Seeded shelf place 7 is (this value) at ostend-investor-portal, client Ostend Credit, year 2022, expertise corporate, published. | C-DM-36 | Data model seed data table |
| `ostend-investor-portal` | the value in the item: Seeded shelf place 7 is Ostend Investor Portal at (this value), client Ostend Credit, year 2022, expertise corporate, published. | C-DM-36 | Data model seed data table |
| `2022` | the value in the item: Seeded shelf place 7 is Ostend Investor Portal at ostend-investor-portal, client Ostend Credit, year (this value), expertise corporate, published. | C-DM-36 | Data model seed data table |
| `Pinemark Trading Desk` | the value in the item: Seeded shelf place 8 is (this value) at pinemark-trading-desk, client Pinemark, year 2023, expertise startups, published. | C-DM-37 | Data model seed data table |
| `pinemark-trading-desk` | the value in the item: Seeded shelf place 8 is Pinemark Trading Desk at (this value), client Pinemark, year 2023, expertise startups, published. | C-DM-37 | Data model seed data table |
| `Halden Home Store` | the value in the item: Seeded shelf place 9 is (this value) at halden-home-store, client Halden, year 2022, expertise ecommerce, published. | C-DM-38 | Data model seed data table |
| `halden-home-store` | the value in the item: Seeded shelf place 9 is Halden Home Store at (this value), client Halden, year 2022, expertise ecommerce, published. | C-DM-38 | Data model seed data table |
| `northline-self-care` | the value in the item: Seeded shelf place 10 is Northline Self Care at (this value), client Northline, year 2021, expertise corporate, published. | C-DM-39 | Data model seed data table |
| `Vantage Pitch Site` | the value in the item: Seeded shelf place 11 is (this value) at vantage-pitch-site, client Vantage, year 2025, expertise startups, published. | C-DM-40 | Data model seed data table |
| `vantage-pitch-site` | the value in the item: Seeded shelf place 11 is Vantage Pitch Site at (this value), client Vantage, year 2025, expertise startups, published. | C-DM-40 | Data model seed data table |
| `pinemark-mobile-app` | the value in the item: Seeded shelf place 12 is Pinemark Mobile App at (this value), client Pinemark, year 2025, expertise startups, draft. | C-DM-41 | Data model seed data table |
| `12` | the value in the item: A seeded case study's cover seed is the seeded place number, 1 to (this value), with palette mono. | C-DM-54 | Data model seed data |
| `ines.duval@example.com` | the value in the item: The seeded brief from Ines Duval carries (this value), company Halden, expertise real-estate, budget 75k_to_150k, state unread. | C-DM-60 | Data model seed data |
| `A site for our coastal tower. <b>Launch before March</b>` | the value in the item: The comment of the Ines Duval brief is (this value) | C-DM-61 | Data model seed data |
| `Tomas Berg` | the value in the item: The seeded brief from (this value) carries tomas.berg@example.com, company Vantage, expertise startups, budget 25k_to_75k, state unread. | C-DM-62 | Data model seed data |
| `tomas.berg@example.com` | the value in the item: The seeded brief from Tomas Berg carries (this value), company Vantage, expertise startups, budget 25k_to_75k, state unread. | C-DM-62 | Data model seed data |
| `We need an onboarding flow for a savings app.` | the value in the item: The comment of the Tomas Berg brief is (this value) | C-DM-63 | Data model seed data |
| `Lea Park` | the value in the item: The seeded brief from (this value) carries lea.park@example.com, company Pinemark, expertise ecommerce, budget under_25k, state read. | C-DM-64 | Data model seed data |
| `lea.park@example.com` | the value in the item: The seeded brief from Lea Park carries (this value), company Pinemark, expertise ecommerce, budget under_25k, state read. | C-DM-64 | Data model seed data |
| `Could you quote for a small online store refresh?` | the value in the item: The comment of the Lea Park brief is (this value) | C-DM-65 | Data model seed data |
| `APP_PUBLIC_URL` | the value in the item: The app is reachable at (this value). | C-DC-01 | Deployment contract |
| `${APP_PUBLIC_PORT}:4173` | port mapping | C-DC-02 | Deployment contract |
| `/api` | the value in the item: The HTTP API is served on the same origin under the (this value) prefix. | C-DC-03 | Deployment contract |
| `GET /api/health` | the value in the item: The route (this value) returns 200 once the app is ready. | C-DC-04 | Deployment contract |
| `200` | the value in the item: The route GET /api/health returns (this value) once the app is ready. | C-DC-04 | Deployment contract |
| `.browser_screenshots/` | the value in the item: Empty (this value), .downloads/ directories exist at the app root. | C-DC-07 | Deployment contract |
| `.downloads/` | the value in the item: Empty .browser_screenshots/, (this value) directories exist at the app root. | C-DC-07 | Deployment contract |
| `0.0.0.0` | the value in the item: The server binds (this value), never a loopback address. | C-DC-10 | Deployment contract |
| `/api/studio` | the value in the item: Bearer authentication is required on every (this value) endpoint, on /api/sessions, on /api/auth/me. | C-DC-17 | Deployment contract API shapes |
| `/api/sessions` | the value in the item: Bearer authentication is required on every /api/studio endpoint, on (this value), on /api/auth/me. | C-DC-17 | Deployment contract API shapes |
| `/api/auth/me` | the value in the item: Bearer authentication is required on every /api/studio endpoint, on /api/sessions, on (this value). | C-DC-17 | Deployment contract API shapes |
| `GET /api/site` | the value in the item: The route (this value) returns expertises in order, tags, clients, featured. | C-DC-22 | Deployment contract API shapes |
| `clients` | the value in the item: The route GET /api/site returns expertises in order, tags, (this value), featured. | C-DC-22 | Deployment contract API shapes |
| `featured` | the value in the item: The route GET /api/site returns expertises in order, tags, clients, (this value). | C-DC-22 | Deployment contract API shapes |
| `null` | the value in the item: Each featured slot in GET /api/site holds a published case study or (this value). | C-DC-23 | Deployment contract API shapes |
| `POST /api/studio/work` | the value in the item: The route (this value) takes title, optional slug, client, year, expertise, tags, summary, cover_seed, cover_palette, blocks. | C-DC-24 | Deployment contract API shapes |
| `GET /api/expertise/{slug}` | the value in the item: The route (this value) returns an expertise with a work list. | C-DC-25 | Deployment contract API shapes |
| `work` | the value in the item: The route GET /api/expertise/{slug} returns an expertise with a (this value) list. | C-DC-25 | Deployment contract API shapes |
| `cover` | the value in the item: A case study response carries id, slug, title, client, year, expertise, tags, summary, cover_seed, cover_palette, (this value), blocks, position, published, version. | C-DC-27 | Deployment contract API shapes |
| `PUT /api/studio/shelf` | the value in the item: The route (this value) takes order with the shelf version, returning the shelf version with work. | C-DC-30 | Deployment contract API shapes |
| `order` | the value in the item: The route PUT /api/studio/shelf takes (this value) with the shelf version, returning the shelf version with work. | C-DC-30 | Deployment contract API shapes |
| `GET /api/studio/slots` | the value in the item: The route (this value) returns the eight slots with id, expertise, position, case_study_id, version. | C-DC-31 | Deployment contract API shapes |
| `POST /api/auth/signup` | the value in the item: The route (this value) takes email, password, optional display_name, returning the account with role, access_token. | C-DC-32 | Deployment contract API shapes |
| `password` | the value in the item: The route POST /api/auth/signup takes email, (this value), optional display_name, returning the account with role, access_token. | C-DC-32 | Deployment contract API shapes |
| `GET /api/auth/me` | the value in the item: The route (this value) returns the signed-in account with role. | C-DC-34 | Deployment contract API shapes |
| `DELETE /api/sessions` | the value in the item: The route (this value) ends every session of the account. | C-DC-36 | Deployment contract API shapes |
| `GET /api/work` | the value in the item: The route (this value) takes optional expertise, repeatable tag, returning published case studies in shelf order. | C-DC-37 | Deployment contract API shapes |
| `tag` | the value in the item: The route GET /api/work takes optional expertise, repeatable (this value), returning published case studies in shelf order. | C-DC-37 | Deployment contract API shapes |
| `GET /api/work/{slug}` | the value in the item: The route (this value) returns one published case study with blocks, tags, expertise, cover, next. | C-DC-38 | Deployment contract API shapes |
| `next` | the value in the item: The route GET /api/work/{slug} returns one published case study with blocks, tags, expertise, cover, (this value). | C-DC-38 | Deployment contract API shapes |
| `POST /api/briefs` | the value in the item: The route (this value) takes name, company, phone, email, comment, expertise, budget, source_path, form_token, website, returning id. | C-DC-41 | Deployment contract API shapes |
| `POST /api/page-views` | the value in the item: The route (this value) takes route, returning the recorded view for a public route. | C-DC-43 | Deployment contract API shapes |
| `GET /api/studio/shelf` | the value in the item: The route (this value) returns the shelf version with work, every case study in shelf order. | C-DC-45 | Deployment contract API shapes |
| `GET /api/studio/dashboard` | the value in the item: The route (this value) returns published_count, draft_count, recent, with unread_briefs for the owner only. | C-DC-46 | Deployment contract API shapes |
| `published_count` | the value in the item: The route GET /api/studio/dashboard returns (this value), draft_count, recent, with unread_briefs for the owner only. | C-DC-46 | Deployment contract API shapes |
| `draft_count` | the value in the item: The route GET /api/studio/dashboard returns published_count, (this value), recent, with unread_briefs for the owner only. | C-DC-46 | Deployment contract API shapes |
| `GET /api/studio/work` | the value in the item: The route (this value) returns a top-level array of every case study in shelf order. | C-DC-47 | Deployment contract API shapes |
| `GET /api/studio/work/{id}` | the value in the item: The route (this value) returns one case study with version, position, published, cover. | C-DC-48 | Deployment contract API shapes |
| `PATCH /api/studio/work/{id}` | the value in the item: The route (this value) takes the changed fields with version, returning the updated case study. | C-DC-49 | Deployment contract API shapes |
| `DELETE /api/studio/work/{id}` | the value in the item: The route (this value) takes version. | C-DC-50 | Deployment contract API shapes |
| `POST /api/studio/work/{id}/cover` | the value in the item: The route (this value) takes generate set to true, alt_text, version, returning the cover with object_key. | C-DC-51 | Deployment contract API shapes |
| `generate` | the value in the item: The route POST /api/studio/work/{id}/cover takes (this value) set to true, alt_text, version, returning the cover with object_key. | C-DC-51 | Deployment contract API shapes |
| `true` | the value in the item: The route POST /api/studio/work/{id}/cover takes generate set to (this value), alt_text, version, returning the cover with object_key. | C-DC-51 | Deployment contract API shapes |
| `POST /api/studio/work/{id}/publish` | the value in the item: The route (this value) takes version, returning the published case study. | C-DC-52 | Deployment contract API shapes |
| `DELETE /api/studio/work/{id}/publish` | the value in the item: The route (this value) takes version, returning the unpublished case study. | C-DC-53 | Deployment contract API shapes |
| `PUT /api/studio/slots/{id}` | the value in the item: The route (this value) takes case_study_id or null with version, returning the slot. | C-DC-54 | Deployment contract API shapes |
| `GET /api/studio/briefs` | the value in the item: The route (this value) takes optional state, returning briefs newest first. | C-DC-55 | Deployment contract API shapes |
| `PATCH /api/studio/briefs/{id}` | the value in the item: The route (this value) takes state, returning the brief. | C-DC-57 | Deployment contract API shapes |
| `DELETE /api/studio/briefs/{id}` | the value in the item: The route (this value) deletes the brief. | C-DC-58 | Deployment contract API shapes |
| `GET /api/studio/page-views` | the value in the item: The route (this value) returns page views newest first. | C-DC-59 | Deployment contract API shapes |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the current year a case study year may not pass | C-CF-213 | a moving bound, resolved from the server's UTC date |
| the exact shades of the ink, the ground, the pale grey | C-UX-01 | carried as words by the brief's own rule, never as values |
| the length of the signature curve's settle | C-UX-25 | named as a character, with no duration given |
| the front page title, Digital Product Design & Development Agency then a vertical bar then Northform | C-CF-262 | pinned in the brief; the vertical bar cannot sit in this table |
| the work index title, Work then a vertical bar then Northform | C-CF-263 | pinned in the brief; the vertical bar cannot sit in this table |
| a case study page title, the case study title then a vertical bar then Northform | C-CF-264 | pinned in the brief; the vertical bar cannot sit in this table |
| an expertise landing title, the expertise name then a vertical bar then Northform | C-CF-265 | pinned in the brief; the vertical bar cannot sit in this table |
| the company page title, Company then a vertical bar then Northform | C-CF-266 | pinned in the brief; the vertical bar cannot sit in this table |
| the contact page title, Northform's Contact Details then a vertical bar then Northform | C-CF-267 | pinned in the brief; the vertical bar cannot sit in this table |
| the privacy notice title, Privacy Policy then a vertical bar then Northform | C-CF-268 | pinned in the brief; the vertical bar cannot sit in this table |
| every studio page title, Studio then a vertical bar then Northform | C-CF-269 | pinned in the brief; the vertical bar cannot sit in this table |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 5 | 5 |
| User roles | 13 | 33 |
| Core features | 122 | 287 |
| User flow | 36 | 41 |
| UI and UX notes | 34 | 50 |
| Front-end specification | 38 | 58 |
| Technical requirements | 18 | 28 |
| Data model | 39 | 69 |
| Constraints | 13 | 13 |
| Deployment contract | 57 | 60 |
| Definition of done | 0 | 0 |

Counts are prose sentences plus table rows that state an obligation; copy-deck wording and rationale are excluded. Overview has a sixth obligation sentence that restates Core features rule 8. Definition of done carries no new obligation: its three sentences restate the visitor, owner and draft-boundary items already itemised under their own sections, so the section adds no item; the restated items are C-UF-23, C-UF-25, C-UF-28, C-CF-191, C-UF-17, C-UF-20, C-UF-21, C-CF-22, C-CF-25, C-CF-77, C-CF-01, C-CF-02, C-CF-03, C-CF-04, C-CF-05, C-CF-06, C-CF-07, C-CF-08.
