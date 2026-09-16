# Checklist: Spatial Studio Portfolio

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract
Sections absent: buildplan
Items: 521
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The app publishes a showcase site for a studio that builds interactive three-dimensional content for the web. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app presents three named product lines as long scrolling arguments. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The app sets out four service disciplines as long-form text. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The app lists seven numbered client cases from an index into full write-ups. `src: Overview para 1`
- [ ] `C-OV-05` `capability` The app publishes one studio email address. `src: Overview para 1`
- [ ] `C-OV-06` `capability` The app publishes one office address. `src: Overview para 1`
- [ ] `C-OV-07` `capability` The app publishes two social profile links. `src: Overview para 1`
- [ ] `C-OV-08` `constraint` The app takes no payment. `src: Overview para 1`
- [ ] `C-OV-09` `capability` The app runs a full-viewport three-dimensional stage behind every route for the whole visit. `src: Overview para 2`
- [ ] `C-OV-10` `ui` The app floats a translucent blurred layer of typography over the stage. `src: Overview para 2`
- [ ] `C-OV-11` `capability` The app keeps the stage on every route without exception. `src: Overview para 2`
- [ ] `C-OV-12` `role` A studio editor drafts a case study. `src: Overview para 3`
- [ ] `C-OV-13` `role` A studio editor uploads cover media for a case study. `src: Overview para 3`
- [ ] `C-OV-14` `role` A studio editor publishes a case study. `src: Overview para 3`
- [ ] `C-OV-15` `capability` Anyone sends an enquiry from the contact route. `src: Overview para 3`
- [ ] `C-OV-16` `constraint` The app offers no search. `src: Overview para 5`
- [ ] `C-OV-17` `constraint` The app offers no filtering. `src: Overview para 5`
- [ ] `C-OV-18` `constraint` The app offers no tagging. `src: Overview para 5`
- [ ] `C-OV-19` `constraint` The app paginates no listing. `src: Overview para 5`
- [ ] `C-OV-20` `constraint` The app carries no blog. `src: Overview para 5`
- [ ] `C-OV-21` `constraint` The app carries no comments. `src: Overview para 5`
- [ ] `C-OV-22` `constraint` The app carries no messaging between visitors. `src: Overview para 5`
- [ ] `C-OV-23` `constraint` The app offers no language switch. `src: Overview para 5`
- [ ] `C-OV-24` `constraint` The app carries no cart. `src: Overview para 5`
- [ ] `C-OV-25` `constraint` The app ships no native application. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads every published route. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor copies the studio email address. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor copies the office address. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A signed-out visitor sends an enquiry. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A signed-out visitor answers the cookie choice. `src: User roles table row 1`
- [ ] `C-RL-06` `constraint` The app denies a signed-out visitor a draft case study. `src: User roles table row 1`
- [ ] `C-RL-07` `constraint` The app denies a signed-out visitor the media of a draft case study. `src: User roles table row 1`
- [ ] `C-RL-08` `constraint` The app denies a signed-out visitor every studio address. `src: User roles table row 1`
- [ ] `C-RL-09` `constraint` The app denies a signed-out visitor every enquiry. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A reader sees the enquiries that same reader submitted. `src: User roles table row 2`
- [ ] `C-RL-11` `constraint` The app denies a reader a draft case study. `src: User roles table row 2`
- [ ] `C-RL-12` `constraint` The app denies a reader the media of a draft case study. `src: User roles table row 2`
- [ ] `C-RL-13` `constraint` The app denies a reader every studio address. `src: User roles table row 2`
- [ ] `C-RL-14` `constraint` The app denies a reader another account's enquiries. `src: User roles table row 2`
- [ ] `C-RL-15` `constraint` The app denies a reader the creation of a case study. `src: User roles table row 2`
- [ ] `C-RL-16` `constraint` The app denies a reader the publishing of a case study. `src: User roles table row 2`
- [ ] `C-RL-17` `role` An editor creates a case study. `src: User roles table row 3`
- [ ] `C-RL-18` `role` An editor edits a case study. `src: User roles table row 3`
- [ ] `C-RL-19` `role` An editor publishes a case study. `src: User roles table row 3`
- [ ] `C-RL-20` `role` An editor unpublishes a case study. `src: User roles table row 3`
- [ ] `C-RL-21` `role` An editor uploads media. `src: User roles table row 3`
- [ ] `C-RL-22` `role` An editor reads every enquiry. `src: User roles table row 3`
- [ ] `C-RL-23` `role` An editor marks an enquiry read. `src: User roles table row 3`
- [ ] `C-RL-24` `role` An editor reads the page-view log. `src: User roles table row 3`
- [ ] `C-RL-25` `constraint` The app enforces authorization server-side on every mutating endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-26` `constraint` The app denies a direct API call from a reader session to an editor-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-27` `constraint` The app leaves the protected state unchanged when a reader session calls an editor-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-28` `capability` The app opens signup to anyone. `src: User roles, signup paragraph`
- [ ] `C-RL-29` `constraint` The app creates a reader account from every signup. `src: User roles, signup paragraph`
- [ ] `C-RL-30` `constraint` The app offers no way to sign up as an editor. `src: User roles, signup paragraph`
- [ ] `C-RL-31` `literal` The app seeds the account `editor@example.com` in the editor role. `src: User roles, seeded accounts table`
- [ ] `C-RL-32` `literal` The app seeds the account `reader@example.com` in the reader role. `src: User roles, seeded accounts table`
- [ ] `C-RL-33` `literal` The app seeds the account `reader2@example.com` in the reader role. `src: User roles, seeded accounts table`
- [ ] `C-RL-34` `literal` The app accepts the password `deku-demo-pw-2026` for every seeded account. `src: User roles, seeded accounts table`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app signs an account in with an email address plus a password. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `contract` The app returns a bearer token on a successful sign-in. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `constraint` The app stores every password hashed. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `constraint` The app rejects an expired bearer token on a protected route. `src: Core features, Auth para 1`
- [ ] `C-CF-05` `capability` The app returns a visitor whose token expired to the sign-in route. `src: Core features, Auth para 1`
- [ ] `C-CF-06` `capability` The app keeps the contents of a part-filled form after an expired token returns the visitor to sign-in. `src: Core features, Auth para 1`
- [ ] `C-CF-07` `constraint` The app creates a reader from a signup request that asks for another role. `src: Core features, Auth para 1`
- [ ] `C-CF-08` `literal` The app accepts a sign-in of a seeded email with `deku-demo-pw-2026`. `src: Core features, Auth rule 1`
- [ ] `C-CF-09` `constraint` The app denies a sign-in that pairs a correct email with a wrong password. `src: Core features, Auth rule 2`
- [ ] `C-CF-10` `constraint` The app names neither the email nor the password as the wrong half of a denied sign-in. `src: Core features, Auth rule 2`
- [ ] `C-CF-11` `constraint` The app denies an unauthenticated call to a protected API route. `src: Core features, Auth rule 3`
- [ ] `C-CF-12` `capability` The app paints one drawing surface sized to the viewport. `src: Core features, The stage para 1`
- [ ] `C-CF-13` `ui` The app fixes the drawing surface in place behind all page content. `src: Core features, The stage para 1`
- [ ] `C-CF-14` `constraint` The app carries exactly one drawing surface per document. `src: Core features, The stage rule 1`
- [ ] `C-CF-15` `literal` The app paints the drawing surface on `/terms/`. `src: Core features, The stage rule 1`
- [ ] `C-CF-16` `literal` The app paints the drawing surface on `/privacy/`. `src: Core features, The stage rule 1`
- [ ] `C-CF-17` `literal` The app paints the drawing surface on `/cookies/`. `src: Core features, The stage rule 1`
- [ ] `C-CF-18` `capability` The app paints the drawing surface on the not-found page. `src: Core features, The stage rule 1`
- [ ] `C-CF-19` `constraint` The app swaps the scene inside the surface on a route change. `src: Core features, The stage rule 2`
- [ ] `C-CF-20` `constraint` The app keeps the drawing surface alive across a route change. `src: Core features, The stage rule 2`
- [ ] `C-CF-21` `ui` The app carries a scene class on the document root. `src: Core features, The stage rule 3`
- [ ] `C-CF-22` `ui` The app carries each route's own name as a class on that route's root. `src: Core features, The stage rule 3`
- [ ] `C-CF-23` `constraint` The app keeps the drawing surface out of the keyboard focus order. `src: Core features, The stage rule 4`
- [ ] `C-CF-24` `constraint` The app repeats in the document any text the scene carries. `src: Core features, The stage rule 5`
- [ ] `C-CF-25` `ui` The app shows a dark out-of-focus city on the home route stage. `src: Core features, The stage scene paragraph`
- [ ] `C-CF-26` `ui` The app shows a point-cloud landscape on the first product line stage. `src: Core features, The stage scene paragraph`
- [ ] `C-CF-27` `ui` The app shows a lit pale interior on the second product line stage. `src: Core features, The stage scene paragraph`
- [ ] `C-CF-28` `ui` The app shows a violet field carrying a wireframe product on the third product line stage. `src: Core features, The stage scene paragraph`
- [ ] `C-CF-29` `ui` The app shows a saturated colour block behind each cluster on the cases index stage. `src: Core features, The stage scene paragraph`
- [ ] `C-CF-30` `ui` The app shows a dot-matrix globe on the contact route stage. `src: Core features, The stage scene paragraph`
- [ ] `C-CF-31` `ui` The app throws every scene out of focus except where a single object is the subject. `src: Core features, The stage closing paragraph`
- [ ] `C-CF-32` `data` A case study carries a slug. `src: Core features, Case studies para 1`
- [ ] `C-CF-33` `data` A case study carries a two-digit number. `src: Core features, Case studies para 1`
- [ ] `C-CF-34` `data` A case study carries a client name. `src: Core features, Case studies para 1`
- [ ] `C-CF-35` `data` A case study carries a title. `src: Core features, Case studies para 1`
- [ ] `C-CF-36` `data` A case study carries a cover clip. `src: Core features, Case studies para 1`
- [ ] `C-CF-37` `data` A case study carries a brief paragraph opening with the client name as a link. `src: Core features, Case studies para 1`
- [ ] `C-CF-38` `data` A case study carries between eight body sections at the fewest to eleven at the most. `src: Core features, Case studies para 1`
- [ ] `C-CF-39` `data` A case study carries a result paragraph. `src: Core features, Case studies para 1`
- [ ] `C-CF-40` `literal` The app serves only published cases from `/api/cases`. `src: Core features, Case studies rule 1`
- [ ] `C-CF-41` `constraint` The app orders the public case listing newest published first. `src: Core features, Case studies rule 1`
- [ ] `C-CF-42` `capability` The app resolves a published case at its own slug address for a signed-out visitor. `src: Core features, Case studies rule 2`
- [ ] `C-CF-43` `constraint` The app keeps a draft case out of every public listing. `src: Core features, Case studies rule 3`
- [ ] `C-CF-44` `constraint` The app denies a signed-out request for a draft case by slug. `src: Core features, Case studies rule 3`
- [ ] `C-CF-45` `constraint` The app denies a reader request for a draft case by slug. `src: Core features, Case studies rule 3`
- [ ] `C-CF-46` `constraint` The app denies every media object belonging to a draft case to a signed-out visitor. `src: Core features, Case studies rule 3`
- [ ] `C-CF-47` `constraint` The app denies every media object belonging to a draft case to a reader. `src: Core features, Case studies rule 3`
- [ ] `C-CF-48` `capability` The app serves a draft case normally to an editor. `src: Core features, Case studies rule 3`
- [ ] `C-CF-49` `capability` The app makes the listing, the address, the media of a case readable in the one act of publishing. `src: Core features, Case studies rule 4`
- [ ] `C-CF-50` `capability` The app returns a published case to draft on unpublishing. `src: Core features, Case studies rule 5`
- [ ] `C-CF-51` `constraint` The app makes an unpublished case unreachable again. `src: Core features, Case studies rule 5`
- [ ] `C-CF-52` `constraint` The app denies a reader the publish endpoint. `src: Core features, Case studies rule 6`
- [ ] `C-CF-53` `constraint` The app leaves a case status unchanged after a reader calls the publish endpoint. `src: Core features, Case studies rule 6`
- [ ] `C-CF-54` `constraint` The app keeps every case number unique. `src: Core features, Case studies rule 7`
- [ ] `C-CF-55` `constraint` The app runs the case number sequence over all cases rather than per client. `src: Core features, Case studies rule 7`
- [ ] `C-CF-56` `literal` The app stores every uploaded byte in the bucket named by `STORAGE_BUCKET`. `src: Core features, Media para 1`
- [ ] `C-CF-57` `literal` The app reaches the object store at `STORAGE_ENDPOINT`. `src: Core features, Media para 1`
- [ ] `C-CF-58` `literal` The app authenticates to the object store with `STORAGE_ACCESS_KEY`. `src: Core features, Media para 1`
- [ ] `C-CF-59` `literal` The app authenticates to the object store with `STORAGE_SECRET_KEY`. `src: Core features, Media para 1`
- [ ] `C-CF-60` `constraint` The app writes no uploaded byte to the app container filesystem. `src: Core features, Media para 1`
- [ ] `C-CF-61` `constraint` The app writes no uploaded byte to a database column. `src: Core features, Media para 1`
- [ ] `C-CF-62` `literal` The app keys every object `cases/{case_id}/{sha256_of_bytes}.{ext}`. `src: Core features, Media rule 1`
- [ ] `C-CF-63` `constraint` The app resolves two uploads of identical bytes for one case to a single object. `src: Core features, Media rule 2`
- [ ] `C-CF-64` `data` A media row records the object key, the content type, the byte size, the digest, the alternative text, the decorative flag. `src: Core features, Media rule 3`
- [ ] `C-CF-65` `constraint` The app serves media belonging to a draft case only to an editor. `src: Core features, Media rule 4`
- [ ] `C-CF-66` `constraint` The app expires a presigned media link within five minutes when presigned links are the chosen mechanism. `src: Core features, Media rule 4`
- [ ] `C-CF-67` `constraint` The app removes the objects of a deleted case from the bucket. `src: Core features, Media rule 5`
- [ ] `C-CF-68` `literal` The app serves the first product line at `/cirrus/`. `src: Core features, Product lines para 1`
- [ ] `C-CF-69` `literal` The app serves the second product line at `/emporium/`. `src: Core features, Product lines para 1`
- [ ] `C-CF-70` `literal` The app serves the third product line at `/facet/`. `src: Core features, Product lines para 1`
- [ ] `C-CF-71` `literal` The app redirects `/solutions/` to the first product line. `src: Core features, Product lines rule 5`
- [ ] `C-CF-72` `constraint` The app carries no product index page. `src: Core features, Product lines rule 5`
- [ ] `C-CF-73` `constraint` The app gives each product line exactly three mechanism steps. `src: Core features, Product lines rule 1`
- [ ] `C-CF-74` `constraint` The app gives each product line between six features at the fewest to nine at the most. `src: Core features, Product lines rule 2`
- [ ] `C-CF-75` `constraint` The app shows the interactive selector on the second product line only, plus the third. `src: Core features, Product lines rule 3`
- [ ] `C-CF-76` `capability` The app changes the stage scene material when a visitor selects one of the three selector options. `src: Core features, Product lines rule 4`
- [ ] `C-CF-77` `ui` The app holds the chosen selector option in its selected state after the pointer leaves. `src: Core features, Product lines rule 4`
- [ ] `C-CF-78` `literal` The app serves the four service disciplines on one route at `/services/`. `src: Core features, Services para 1`
- [ ] `C-CF-79` `literal` The app reaches the first discipline at `/services/#graphics`. `src: Core features, Services para 1`
- [ ] `C-CF-80` `literal` The app reaches the second discipline at `/services/#ui`. `src: Core features, Services para 1`
- [ ] `C-CF-81` `literal` The app reaches the third discipline at `/services/#assets`. `src: Core features, Services para 1`
- [ ] `C-CF-82` `literal` The app reaches the fourth discipline at `/services/#cloud`. `src: Core features, Services para 1`
- [ ] `C-CF-83` `constraint` The app gives each discipline exactly four bullets. `src: Core features, Services rule 1`
- [ ] `C-CF-84` `constraint` The app keeps a navigation caption distinct from the page heading for each discipline. `src: Core features, Services rule 2`
- [ ] `C-CF-85` `literal` The app seeds the cases index with seven published cases numbered `01` through `07`. `src: Core features, Cases index table`
- [ ] `C-CF-86` `literal` The app seeds a draft case numbered `08` titled `Substation Twin`. `src: Core features, Cases index para 3`
- [ ] `C-CF-87` `literal` The app denies `/cases/substation-twin` to a signed-out visitor. `src: Core features, Cases index para 3`
- [ ] `C-CF-88` `constraint` The app carries no heading on the cases index. `src: Core features, Cases index para 1`
- [ ] `C-CF-89` `capability` The app features the first three published cases on the home route. `src: Core features, Cases index para 4`
- [ ] `C-CF-90` `ui` The app sets the studio question in three display lines on the contact route. `src: Core features, Contact para 1`
- [ ] `C-CF-91` `ui` The app fades a hidden label into view on hover over the email copy control. `src: Core features, Contact para 2`
- [ ] `C-CF-92` `capability` The app copies the studio email address when a visitor activates the email copy control. `src: Core features, Contact para 2`
- [ ] `C-CF-93` `capability` The app copies the office address when a visitor activates the address copy control. `src: Core features, Contact para 2`
- [ ] `C-CF-94` `ui` The app shows both copy labels unconditionally on a touch device. `src: Core features, Contact para 2`
- [ ] `C-CF-95` `capability` The app announces the result of a copy. `src: Core features, Contact para 2`
- [ ] `C-CF-96` `data` An enquiry carries a name, an email address, an optional organisation, a message. `src: Core features, Contact para 3`
- [ ] `C-CF-97` `capability` The app accepts an enquiry whose required fields are present with a parsing email address. `src: Core features, Contact rule 1`
- [ ] `C-CF-98` `capability` The app answers an accepted enquiry with a confirmation shown in place. `src: Core features, Contact rule 1`
- [ ] `C-CF-99` `constraint` The app rejects an invalid enquiry inline. `src: Core features, Contact rule 2`
- [ ] `C-CF-100` `constraint` The app names the failing field in a rejected enquiry response. `src: Core features, Contact rule 2`
- [ ] `C-CF-101` `constraint` The app writes no row for a rejected enquiry. `src: Core features, Contact rule 2`
- [ ] `C-CF-102` `capability` The app carries an unattended decoy field on the enquiry form. `src: Core features, Contact rule 3`
- [ ] `C-CF-103` `constraint` The app refuses an enquiry arriving with the decoy field filled. `src: Core features, Contact rule 3`
- [ ] `C-CF-104` `constraint` The app writes nothing for an enquiry refused over the decoy field. `src: Core features, Contact rule 3`
- [ ] `C-CF-105` `constraint` The app refuses repeated enquiries submitted in quick succession from one origin after the first. `src: Core features, Contact rule 4`
- [ ] `C-CF-106` `constraint` The app writes nothing for an enquiry refused as a repeat. `src: Core features, Contact rule 4`
- [ ] `C-CF-107` `literal` The app lists every enquiry to an editor at `/studio/enquiries` newest first. `src: Core features, Contact rule 5`
- [ ] `C-CF-108` `capability` The app marks an enquiry read for an editor. `src: Core features, Contact rule 5`
- [ ] `C-CF-109` `constraint` The app denies a reader the enquiry list endpoint. `src: Core features, Contact rule 5`
- [ ] `C-CF-110` `constraint` The app shows a reader only the enquiries that same reader submitted. `src: Core features, Contact rule 5`
- [ ] `C-CF-111` `literal` The app serves the terms document at `/terms/`. `src: Core features, Legal para 1`
- [ ] `C-CF-112` `literal` The app serves the privacy document at `/privacy/`. `src: Core features, Legal para 1`
- [ ] `C-CF-113` `literal` The app serves the cookie document at `/cookies/`. `src: Core features, Legal para 1`
- [ ] `C-CF-114` `constraint` The app carries the full chrome on every legal route. `src: Core features, Legal para 1`
- [ ] `C-CF-115` `constraint` The app carries the full stage on every legal route. `src: Core features, Legal para 1`
- [ ] `C-CF-116` `constraint` The app carries the full motion system on every legal route. `src: Core features, Legal para 1`
- [ ] `C-CF-117` `capability` The app states on the privacy route what the product stores about a visitor. `src: Core features, Legal rule 1`
- [ ] `C-CF-118` `capability` The app states on the privacy route how long visitor data is kept. `src: Core features, Legal rule 1`
- [ ] `C-CF-119` `ui` The app reaches the privacy route from the footer of every page. `src: Core features, Legal rule 1`
- [ ] `C-CF-120` `ui` The app reaches the terms route from the footer of every page. `src: Core features, Legal rule 2`
- [ ] `C-CF-121` `ui` The app links the terms route from the signup form. `src: Core features, Legal rule 2`
- [ ] `C-CF-122` `capability` The app asks a first-time visitor once about non-essential cookies. `src: Core features, Legal rule 3`
- [ ] `C-CF-123` `literal` The app labels the cookie notice link `Cookie Policy`. `src: Core features, Legal rule 3`
- [ ] `C-CF-124` `literal` The app labels the cookie notice button `OK`. `src: Core features, Legal rule 3`
- [ ] `C-CF-125` `constraint` The app keeps the cookie answer across a reload. `src: Core features, Legal rule 3`
- [ ] `C-CF-126` `constraint` The app records no page view before the visitor has answered the cookie choice. `src: Core features, Legal rule 4`
- [ ] `C-CF-127` `data` A recorded page view carries its route plus the time of the view. `src: Core features, Legal rule 4`
- [ ] `C-CF-128` `constraint` The app shows the page-view log to an editor only. `src: Core features, Legal rule 4`
- [ ] `C-CF-129` `capability` The app renders its own not-found page for any address matching no route. `src: Core features, Legal rule 5`
- [ ] `C-CF-130` `ui` The app offers a way back to the home route from the not-found page. `src: Core features, Legal rule 5`
- [ ] `C-CF-131` `contract` The app answers not-found for an address matching no route. `src: Core features, Legal rule 5`
- [ ] `C-CF-132` `constraint` The app resolves every wrong address to one catch-all page. `src: Core features, Legal rule 5`
- [ ] `C-CF-133` `constraint` The app resolves every internal link on every public route. `src: Core features, Legal rule 6`
- [ ] `C-CF-134` `literal` The app lists every public route in `/sitemap.xml`. `src: Core features, Sitemap rule 1`
- [ ] `C-CF-135` `constraint` The app keeps a draft case study out of the sitemap. `src: Core features, Sitemap rule 1`
- [ ] `C-CF-136` `literal` The app names the sitemap inside `/robots.txt`. `src: Core features, Sitemap rule 2`
- [ ] `C-CF-137` `capability` The app adds a case to the sitemap on publishing. `src: Core features, Sitemap rule 3`
- [ ] `C-CF-138` `capability` The app removes a case from the sitemap on unpublishing. `src: Core features, Sitemap rule 3`
- [ ] `C-CF-139` `literal` The app shows an editor the case list beside the selected case at `/studio/cases`. `src: Core features, Studio console para 1`
- [ ] `C-CF-140` `ui` The app changes the address to the selected case slug as the selection changes. `src: Core features, Studio console para 1`
- [ ] `C-CF-141` `ui` The app stacks the two panes below the wide breakpoint. `src: Core features, Studio console para 1`
- [ ] `C-CF-142` `literal` The app opens case creation at `/studio/cases/new`. `src: Core features, Studio console para 2`
- [ ] `C-CF-143` `ui` The app updates a case row at once on publishing. `src: Core features, Studio console para 3`
- [ ] `C-CF-144` `ui` The app returns a case row to its previous state with a message in place when a save does not land. `src: Core features, Studio console para 3`
- [ ] `C-CF-145` `constraint` The app refuses a reader at every studio address. `src: Core features, Studio console rule 1`
- [ ] `C-CF-146` `capability` The app sends an unauthenticated visitor at a studio address to the sign-in route. `src: Core features, Studio console rule 2`
- [ ] `C-CF-147` `capability` The app returns a visitor to the requested studio address after signing in. `src: Core features, Studio console rule 2`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves the home route at `/`. `src: User flow route table row 1`
- [ ] `C-UF-02` `literal` The app serves the services route at `/services/`. `src: User flow route table row 6`
- [ ] `C-UF-03` `literal` The app serves the cases index at `/cases/`. `src: User flow route table row 7`
- [ ] `C-UF-04` `literal` The app serves the contact route at `/contact/`. `src: User flow route table row 9`
- [ ] `C-UF-05` `literal` The app serves the sign-in route at `/login`. `src: User flow route table row 15`
- [ ] `C-UF-06` `literal` The app serves the signup route at `/signup`. `src: User flow route table row 16`
- [ ] `C-UF-07` `literal` The app serves the case list at `/studio/cases`. `src: User flow route table row 17`
- [ ] `C-UF-08` `constraint` The app answers every route on its bare form. `src: User flow, trailing-slash paragraph`
- [ ] `C-UF-09` `constraint` The app answers every route on its trailing-slash form. `src: User flow, trailing-slash paragraph`
- [ ] `C-UF-10` `capability` The app sends an unauthenticated visitor at a studio address to the sign-in route. `src: User flow, entry paragraph`
- [ ] `C-UF-11` `capability` The app lands an editor on the case list after signing in. `src: User flow, entry paragraph`
- [ ] `C-UF-12` `capability` The app lands a reader on the home route after signing in. `src: User flow, entry paragraph`
- [ ] `C-UF-13` `capability` The app returns a visitor to the home route after signing out. `src: User flow, entry paragraph`
- [ ] `C-UF-14` `constraint` The app stops a bearer token working after signing out. `src: User flow, entry paragraph`
- [ ] `C-UF-15` `ui` The app paints the stage behind the first headline before the loader clears. `src: User flow, journey 1`
- [ ] `C-UF-16` `ui` The app pins three statements in turn on the home route. `src: User flow, journey 1`
- [ ] `C-UF-17` `ui` The app fades the whole page between the dark theme, the pale one. `src: User flow, journey 2`
- [ ] `C-UF-18` `ui` The app swings the three mechanism steps into view one after another. `src: User flow, journey 2`
- [ ] `C-UF-19` `ui` The app opens a case detail with its cover clip filling the opening. `src: User flow, journey 3`
- [ ] `C-UF-20` `ui` The app places a back link at the left of the case detail content column. `src: User flow, journey 3`
- [ ] `C-UF-21` `ui` The app heads the final case detail section `Result`. `src: User flow, journey 3`
- [ ] `C-UF-22` `constraint` The app refuses a second identical enquiry submitted at once. `src: User flow, journey 4`
- [ ] `C-UF-23` `constraint` The app denies a signed-out request for the draft case cover object. `src: User flow, journey 5`
- [ ] `C-UF-24` `capability` The app shows an editor every case with the draft one marked draft. `src: User flow, journey 6`
- [ ] `C-UF-25` `capability` The app resolves a newly published case address for a signed-out visitor. `src: User flow, journey 6`
- [ ] `C-UF-26` `ui` The app shows an empty state on a cases index with nothing published. `src: User flow, states paragraph`
- [ ] `C-UF-27` `ui` The app shows an empty state on an enquiry list carrying no row. `src: User flow, states paragraph`
- [ ] `C-UF-28` `ui` The app shows the waiting indicator only when the stage is unready one frame after the document becomes interactive. `src: User flow, states paragraph`
- [ ] `C-UF-29` `ui` The app keeps the stage rendering through an error. `src: User flow, states paragraph`
- [ ] `C-UF-30` `ui` The app reports an error in place rather than taking the route down. `src: User flow, states paragraph`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface reads as a thin translucent layer floating in front of the moving background. `src: UI/UX notes, north star`
- [ ] `C-UX-02` `ui` The public routes read consumer, editorial, with atmosphere seen before the words. `src: UI/UX notes, register`
- [ ] `C-UX-03` `ui` The studio console reads quiet, dense, organised for scanning. `src: UI/UX notes, register`
- [ ] `C-UX-04` `ui` The public routes are spacious in density. `src: UI/UX notes, register`
- [ ] `C-UX-05` `ui` The studio console is compact in density. `src: UI/UX notes, register`
- [ ] `C-UX-06` `ui` The page carries a visible four-rule grid with crosshair marks. `src: UI/UX notes, six decisions`
- [ ] `C-UX-07` `ui` A class on the document root swaps the two-token theme per route. `src: UI/UX notes, six decisions`
- [ ] `C-UX-08` `ui` Every reveal is a class flip rather than a timeline. `src: UI/UX notes, six decisions`
- [ ] `C-UX-09` `ui` The default theme sets a deep neutral page ground under near-white neutral ink. `src: UI/UX notes, colour paragraph`
- [ ] `C-UX-10` `ui` The pale theme sets a light cool neutral ground under deep, muted cyan ink. `src: UI/UX notes, colour paragraph`
- [ ] `C-UX-11` `ui` The pale theme inverts both filled panels to deep, muted cyan carrying near-white ink. `src: UI/UX notes, colour paragraph`
- [ ] `C-UX-12` `ui` The accent is a mid, vivid teal reading as pure cyan. `src: UI/UX notes, colour paragraph`
- [ ] `C-UX-13` `constraint` The accent appears on hover, on the active state, on text selection, nowhere else. `src: UI/UX notes, colour paragraph`
- [ ] `C-UX-14` `literal` The interface sets `DM Sans` for everything at weights 300, 400, 500, 600, 700. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-15` `literal` The interface sets `DM Mono` in the regular cut for exactly one label. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-16` `literal` The root type is `16px` stepping to `20px` at the tablet breakpoint. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-17` `literal` The display scale steps `64px` to `128px` in the heaviest cut. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-18` `literal` The display scale steps `48px` to `96px` in the heaviest cut. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-19` `literal` The display scale steps `36px` to `72px` in the heaviest cut. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-20` `literal` The display scale steps `30px` to `48px` in the heaviest cut. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-21` `literal` The display scale steps `24px` to `32px` in the heaviest cut. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-22` `literal` The small label steps `12px` to `16px` in the regular cut. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-23` `ui` One leading override sets `125%` on running prose only. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-24` `ui` The motion character is eased, with every state change leaving quickly, arriving slowly. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-25` `constraint` The interface carries exactly one duration for every state change. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-26` `constraint` The interface reserves the double duration for four moments only. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-27` `constraint` The interface introduces no third duration. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-28` `constraint` The interface introduces no second custom curve. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-29` `ui` The navigation chevron snaps over then settles on the one authored curve. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-30` `ui` A waiting element slides one displacement step, fading up over the same moment. `src: UI/UX notes, reveal paragraph`
- [ ] `C-UX-31` `ui` A waiting element turned edge-on swings around into view along a shallow arc. `src: UI/UX notes, reveal paragraph`
- [ ] `C-UX-32` `ui` A staggered group hands over with each element starting as the previous finishes. `src: UI/UX notes, reveal paragraph`
- [ ] `C-UX-33` `ui` Pointing at a control turns that control the accent colour with nothing else changing. `src: UI/UX notes, hover paragraph`
- [ ] `C-UX-34` `ui` Pressing a control adds a soft inner shading to that control, moving nothing. `src: UI/UX notes, hover paragraph`
- [ ] `C-UX-35` `ui` The contact copy label fades in rather than changing colour. `src: UI/UX notes, hover paragraph`
- [ ] `C-UX-36` `constraint` A reduced-motion preference neutralises the reveal classes so content arrives already in place. `src: UI/UX notes, reduced motion paragraph`
- [ ] `C-UX-37` `constraint` A reduced-motion preference stops the two idle animations. `src: UI/UX notes, reduced motion paragraph`
- [ ] `C-UX-38` `constraint` A reduced-motion preference makes the route transition instant. `src: UI/UX notes, reduced motion paragraph`
- [ ] `C-UX-39` `constraint` A reduced-motion preference holds the stage framing rather than removing the stage. `src: UI/UX notes, reduced motion paragraph`
- [ ] `C-UX-40` `constraint` Body text meets WCAG AA contrast against its ground in both themes. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-41` `constraint` Text over a translucent panel meets the contrast bar against the lightest frame the stage produces behind that panel. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-42` `constraint` Every content image carries alternative text describing what the image shows. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-43` `constraint` A decorative image declares itself decorative rather than carrying a description. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-44` `constraint` Every icon-only control carries a label. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-45` `constraint` No meaning is carried by colour alone. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-46` `constraint` Every touch target is comfortably sized. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-47` `constraint` Keyboard navigation reaches every control with a visible focus ring. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-48` `constraint` The two navigation panels open on keyboard focus. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-49` `constraint` The three selector options are focusable, operable by arrow keys, operable by space. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-50` `constraint` The focus ring pairs the accent with an outer dark halo. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-51` `constraint` Each route carries exactly one first-level heading. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-52` `constraint` The display lines forming a heading are one element with line breaks inside. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-53` `ui` The type scale doubles at the tablet breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-54` `ui` The navigation bar replaces the toggle at the tablet breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-55` `ui` The page gutter widens at the wide breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-56` `ui` The case card moves to the centre at the wide breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-57` `ui` The services index appears in the left column at the wide breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-58` `ui` The navigation bar narrows to half the grid at the ultra-wide breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-59` `ui` Each pinned block is half the viewport height at every width. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-60` `constraint` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-61` `constraint` Every navigation target stays reachable at a narrow viewport. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-62` `literal` The viewport declaration is `width=device-width, initial-scale=1.0` with nothing else. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-63` `ui` The selector responds to a first tap as a selection on a touch device. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-64` `ui` Each page leads with exactly one primary action distinct from every secondary one. `src: UI/UX notes, primary action paragraph`
- [ ] `C-UX-65` `ui` The footer call to action is the only oversized link on a public route. `src: UI/UX notes, primary action paragraph`
- [ ] `C-UX-66` `ui` The enquiry submit control is the primary action on the contact route. `src: UI/UX notes, primary action paragraph`
- [ ] `C-UX-67` `ui` The publish control is the primary action in the studio console. `src: UI/UX notes, primary action paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every rule is scoped under a single `site-root` class on the application root. `src: Front-end specification, namespace`
- [ ] `C-FE-02` `ui` Solid leading is the default everywhere, so looser leading is an explicit override. `src: Front-end specification, namespace`
- [ ] `C-FE-03` `ui` The per-route colour class carrying a product name is `color-facet` for the third product line. `src: Front-end specification, namespace`
- [ ] `C-FE-04` `ui` The theme is a class on the document root rather than a set of custom properties. `src: Front-end specification, theme tokens`
- [ ] `C-FE-05` `ui` The document element carries the theme transition on background colour, colour, fill. `src: Front-end specification, theme tokens`
- [ ] `C-FE-06` `ui` The second product line carries `color-light`. `src: Front-end specification, theme assignment`
- [ ] `C-FE-07` `ui` The third product line carries a scene class beside `color-light`. `src: Front-end specification, theme assignment`
- [ ] `C-FE-08` `constraint` No stylesheet rule matches the scene class. `src: Front-end specification, theme assignment`
- [ ] `C-FE-09` `ui` A third theme class affects the cover caption opacity alone, staying unused. `src: Front-end specification, theme assignment`
- [ ] `C-FE-10` `ui` `panel-blurred` is a pure frosting carrying a hairline edge over no ground of its own. `src: Front-end specification, panels`
- [ ] `C-FE-11` `ui` `panel-translucent` carries the panel colour at part alpha. `src: Front-end specification, panels`
- [ ] `C-FE-12` `ui` `panel-opaque` declares a backdrop blur over an opaque ground. `src: Front-end specification, panels`
- [ ] `C-FE-13` `constraint` The backdrop filter appears on the three panel classes only. `src: Front-end specification, panels`
- [ ] `C-FE-14` `constraint` The spacing scale keeps its three fractional steps unrounded. `src: Front-end specification, spacing`
- [ ] `C-FE-15` `ui` The `cop` class is the page gutter on every page container. `src: Front-end specification, spacing`
- [ ] `C-FE-16` `ui` Widths are twelfths of the parent as `w-1` through `w-12`. `src: Front-end specification, spacing`
- [ ] `C-FE-17` `ui` The three responsive prefixes map onto the tablet, wide, ultra-wide breakpoints. `src: Front-end specification, spacing`
- [ ] `C-FE-18` `ui` Every radius utility sets overflow hidden alongside the radius. `src: Front-end specification, utility layer`
- [ ] `C-FE-19` `ui` `t-high` is the only leading override in the system. `src: Front-end specification, utility layer`
- [ ] `C-FE-20` `ui` The three tiled patterns are drawn as gradients rather than loaded. `src: Front-end specification, patterns`
- [ ] `C-FE-21` `ui` `pattern-dots` carries the look as the faint perforation over case media. `src: Front-end specification, patterns`
- [ ] `C-FE-22` `ui` Every shadow is a zero-offset, zero-spread glow. `src: Front-end specification, shadows`
- [ ] `C-FE-23` `ui` The case media panel carries the heaviest glow as a vignette. `src: Front-end specification, shadows`
- [ ] `C-FE-24` `ui` A pressed button acquires an inner shadow without moving. `src: Front-end specification, shadows`
- [ ] `C-FE-25` `ui` Every mark in the interface is inline vector geometry. `src: Front-end specification, iconography`
- [ ] `C-FE-26` `constraint` The interface loads no icon font, no sprite, no image file for a mark. `src: Front-end specification, iconography`
- [ ] `C-FE-27` `ui` One chevron drawing serves four rotations. `src: Front-end specification, iconography`
- [ ] `C-FE-28` `ui` The case detail back link is the only element using the chevron pointing left. `src: Front-end specification, iconography`
- [ ] `C-FE-29` `ui` The logotype is a faceted kite drawn as a filled body plus an outline. `src: Front-end specification, iconography`
- [ ] `C-FE-30` `ui` The shield appears on the legal routes from the tablet breakpoint up. `src: Front-end specification, iconography`
- [ ] `C-FE-31` `ui` The navigation bar right edge lands on the grid fourth rule. `src: Front-end specification, navigation bar`
- [ ] `C-FE-32` `ui` The navigation bar holds five content-sized entries. `src: Front-end specification, navigation bar`
- [ ] `C-FE-33` `ui` The active navigation entry ground goes fully transparent under an inner shadow. `src: Front-end specification, navigation bar`
- [ ] `C-FE-34` `ui` A navigation panel grows downward out of the bar rather than floating over the bar. `src: Front-end specification, dropdown panels`
- [ ] `C-FE-35` `ui` A navigation panel ground goes opaque as the panel opens. `src: Front-end specification, dropdown panels`
- [ ] `C-FE-36` `literal` The navigation panel lists `Cirrus` under the category `Data`. `src: Front-end specification, dropdown table`
- [ ] `C-FE-37` `literal` The navigation panel lists `Emporium` under the category `Retail`. `src: Front-end specification, dropdown table`
- [ ] `C-FE-38` `literal` The navigation panel lists `Facet` under the category `Retail`. `src: Front-end specification, dropdown table`
- [ ] `C-FE-39` `constraint` The four service entries are anchors into one route rather than separate pages. `src: Front-end specification, dropdown table`
- [ ] `C-FE-40` `ui` One square toggle replaces the bar below the tablet breakpoint. `src: Front-end specification, menu toggle`
- [ ] `C-FE-41` `ui` Four named keyframes change the toggle bars into a cross. `src: Front-end specification, menu toggle`
- [ ] `C-FE-42` `ui` The two toggle bars meet in the middle as a single line at the midpoint stop. `src: Front-end specification, menu toggle`
- [ ] `C-FE-43` `ui` The logotype drops to the muted ink whenever the mobile panel is open. `src: Front-end specification, logotype`
- [ ] `C-FE-44` `ui` The footer stays pointer-transparent until reached. `src: Front-end specification, footer`
- [ ] `C-FE-45` `ui` The footer veil fades over the double duration against the standard duration of the content beneath. `src: Front-end specification, footer`
- [ ] `C-FE-46` `ui` The footer chevron overlaps the last letter of the call to action. `src: Front-end specification, footer`
- [ ] `C-FE-47` `literal` The home route footer reads `Next up` over `Explore our` plus `Solutions`. `src: Front-end specification, calls to action table`
- [ ] `C-FE-48` `literal` The cases footer reads `Have a project in mind?` over `Let's` plus `Talk`. `src: Front-end specification, calls to action table`
- [ ] `C-FE-49` `literal` The footer small print carries the lowercase links `contact`, `terms`, `privacy`. `src: Front-end specification, footer`
- [ ] `C-FE-50` `literal` The footer carries a back-to-top control labelled `Back to top`. `src: Front-end specification, footer`
- [ ] `C-FE-51` `ui` The drawn grid shows four hairlines distributed evenly across the grid container. `src: Front-end specification, drawn grid`
- [ ] `C-FE-52` `ui` A fifth grid rule is present in the markup collapsing to nothing. `src: Front-end specification, drawn grid`
- [ ] `C-FE-53` `ui` Each crosshair mark is a plus sign centred exactly on a grid intersection. `src: Front-end specification, drawn grid`
- [ ] `C-FE-54` `ui` The top mark row moves to the viewport top below the tablet breakpoint. `src: Front-end specification, drawn grid`
- [ ] `C-FE-55` `ui` The clipping frame insets the stage to the page gutter in its framed state. `src: Front-end specification, drawn grid`
- [ ] `C-FE-56` `ui` The pending dots fade in turn on an endless linear cycle. `src: Front-end specification, loader`
- [ ] `C-FE-57` `literal` The cookie notice carries an underlined `Cookie Policy` link. `src: Front-end specification, loader`
- [ ] `C-FE-58` `literal` The scroll arrow sits above the label `Scroll down`. `src: Front-end specification, loader`
- [ ] `C-FE-59` `literal` Every video element carries the fallback text `Your browser does not support the video tag.` `src: Front-end specification, loader`
- [ ] `C-FE-60` `ui` A pinned block occupies the lower half of the screen, leaving the upper half to the stage. `src: Front-end specification, scroll system`
- [ ] `C-FE-61` `ui` The home route carries two groups of pinned blocks, of three, of four. `src: Front-end specification, scroll system`
- [ ] `C-FE-62` `ui` A pinned block goes out of focus continuously through the hand-over. `src: Front-end specification, scroll system`
- [ ] `C-FE-63` `ui` The product route progress bar stays near-white ink in both themes. `src: Front-end specification, scroll system`
- [ ] `C-FE-64` `constraint` Reveals are driven by intersection with the viewport rather than a scroll offset table. `src: Front-end specification, scroll system`
- [ ] `C-FE-65` `ui` A `scroll-trigger` container gains `enabled` when the container comes into view. `src: Front-end specification, reveal vocabulary`
- [ ] `C-FE-66` `ui` Six offset classes give a waiting element one displacement step. `src: Front-end specification, reveal vocabulary`
- [ ] `C-FE-67` `ui` Four pivot classes set the transform origin behind the element rather than on its face. `src: Front-end specification, reveal vocabulary`
- [ ] `C-FE-68` `ui` Six delay classes step by the interface duration. `src: Front-end specification, reveal vocabulary`
- [ ] `C-FE-69` `constraint` The reveal rule set is declared a second time scoped under `layer`. `src: Front-end specification, reveal vocabulary`
- [ ] `C-FE-70` `ui` Four nested full-viewport elements surround the drawing surface. `src: Front-end specification, stage layers`
- [ ] `C-FE-71` `constraint` The overlay layer stays pointer-transparent by default. `src: Front-end specification, stage layers`
- [ ] `C-FE-72` `ui` One ordinary layout content column acts as a perspective root. `src: Front-end specification, stage layers`
- [ ] `C-FE-73` `ui` Clips sit inside media panels rather than on the stage. `src: Front-end specification, video`
- [ ] `C-FE-74` `ui` A media caption stays hidden until an info button is activated. `src: Front-end specification, video`
- [ ] `C-FE-75` `constraint` The engineering captions stay in the studio voice rather than being rewritten. `src: Front-end specification, video`
- [ ] `C-FE-76` `literal` The home opening reads `Adding` over `Dimension` plus `to the web`. `src: Front-end specification, route compositions`
- [ ] `C-FE-77` `ui` Every display line is its own element carrying its own reveal class. `src: Front-end specification, route compositions`
- [ ] `C-FE-78` `ui` The cover caption holds the same faintness in every theme. `src: Front-end specification, route compositions`
- [ ] `C-FE-79` `ui` The product name is set smaller than its own description on a home pinned block. `src: Front-end specification, route compositions`
- [ ] `C-FE-80` `constraint` The red `Discover` rule is debugging residue left unbuilt. `src: Front-end specification, route compositions`
- [ ] `C-FE-81` `literal` The services handoff card carries `Take a look at our` over `Services`. `src: Front-end specification, route compositions`
- [ ] `C-FE-82` `ui` A product route runs seven movements in a fixed order. `src: Front-end specification, route compositions`
- [ ] `C-FE-83` `ui` The arc gauge rises out of its panel floor from both directions at once. `src: Front-end specification, route compositions`
- [ ] `C-FE-84` `constraint` One gauge component with a variant serves both config pagers. `src: Front-end specification, route compositions`
- [ ] `C-FE-85` `ui` The services index shows the current discipline in full ink over three dimmed ones. `src: Front-end specification, route compositions`
- [ ] `C-FE-86` `ui` The services bullets read tighter than the prose around them. `src: Front-end specification, route compositions`
- [ ] `C-FE-87` `ui` The case index info card straddles the media panel bottom edge. `src: Front-end specification, route compositions`
- [ ] `C-FE-88` `ui` The case number is set with a slashed zero glyph. `src: Front-end specification, route compositions`
- [ ] `C-FE-89` `literal` The case detail back link reads `View` over `All cases`. `src: Front-end specification, route compositions`
- [ ] `C-FE-90` `ui` `ui-title` plus `ui-paragraph` are the only content-specific type classes. `src: Front-end specification, route compositions`
- [ ] `C-FE-91` `constraint` The case detail route pins nothing. `src: Front-end specification, route compositions`
- [ ] `C-FE-92` `literal` The contact route opens `Hello` over `How can`, `we assist`, `you today?` `src: Front-end specification, route compositions`
- [ ] `C-FE-93` `literal` The contact route sets the studio address `studio@prismlabs.co` at the third display step. `src: Front-end specification, route compositions`
- [ ] `C-FE-94` `literal` The contact office block reads `Ridderstraat 118`, `2200 Herentals`, `Belgium`. `src: Front-end specification, route compositions`
- [ ] `C-FE-95` `literal` The contact business block reads `Business Info` over `Meridian Comm. V.` plus `BE 0000 000 000`. `src: Front-end specification, route compositions`
- [ ] `C-FE-96` `ui` A non-breaking space keeps the office address from breaking mid-token. `src: Front-end specification, route compositions`
- [ ] `C-FE-97` `literal` The not-found route reads `Page Not` over `Found`. `src: Front-end specification, route compositions`
- [ ] `C-FE-98` `ui` The not-found route is exactly two viewport heights. `src: Front-end specification, route compositions`
- [ ] `C-FE-99` `ui` Every route is the same five-deep stack. `src: Front-end specification, module architecture`
- [ ] `C-FE-100` `ui` Twenty-four reusable components make up the interface. `src: Front-end specification, module architecture`
- [ ] `C-FE-101` `constraint` Exactly one piece of client state outlives the page. `src: Front-end specification, module architecture`
- [ ] `C-FE-102` `constraint` The build ships no binary asset of any kind. `src: Front-end specification, zero-asset guide`
- [ ] `C-FE-103` `constraint` The stage scenes are generated from primitives rather than loaded. `src: Front-end specification, zero-asset guide`
- [ ] `C-FE-104` `literal` The seeded first product line claim opens `An astonishing` above the figure `80%`. `src: Front-end specification, copy deck`
- [ ] `C-FE-105` `literal` The seeded services heading reads `Services to amplify your next web project`. `src: Front-end specification, copy deck`
- [ ] `C-FE-106` `literal` The seeded first case title reads `Oil & Gas Data Visualization`. `src: Front-end specification, copy deck`
- [ ] `C-FE-107` `literal` The seeded first case client reads `Delta AI`. `src: Front-end specification, copy deck`
- [ ] `C-FE-108` `constraint` The seed copy corrects the four typographic errors in the source material. `src: Front-end specification, copy deck`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The server produces the document for every public route. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The browser receives rendered markup on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The front end is built with `SvelteKit`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` The HTTP API is built with `Hono`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` Data is stored in `PostgreSQL` reached at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `literal` Uploaded bytes are stored in `minio`. `src: Technical requirements para 1`
- [ ] `C-TR-07` `contract` Authentication is email plus password with bearer tokens. `src: Technical requirements para 1`
- [ ] `C-TR-08` `constraint` Passwords are hashed. `src: Technical requirements para 1`
- [ ] `C-TR-09` `literal` The app answers `GET /api/health` with `200` once ready. `src: Technical requirements para 1`
- [ ] `C-TR-10` `contract` The app logs one line per request to stdout. `src: Technical requirements para 1`
- [ ] `C-TR-11` `constraint` The app introduces no second database. `src: Technical requirements para 2`
- [ ] `C-TR-12` `constraint` The app introduces no cache. `src: Technical requirements para 2`
- [ ] `C-TR-13` `constraint` The app introduces no queue. `src: Technical requirements para 2`
- [ ] `C-TR-14` `constraint` The app introduces no second object store. `src: Technical requirements para 2`
- [ ] `C-TR-15` `constraint` The app introduces no external identity provider. `src: Technical requirements para 2`
- [ ] `C-TR-16` `constraint` The app introduces no mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-17` `constraint` The app reads every host, every port, every credential from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-18` `constraint` The app starts no copy of a backing service. `src: Technical requirements para 3`
- [ ] `C-TR-19` `contract` Every public route emits its own title. `src: Technical requirements, metadata`
- [ ] `C-TR-20` `contract` Every public route emits its own description. `src: Technical requirements, metadata`
- [ ] `C-TR-21` `contract` Every public route emits its own canonical link. `src: Technical requirements, metadata`
- [ ] `C-TR-22` `constraint` No two routes share a title. `src: Technical requirements, metadata`
- [ ] `C-TR-23` `constraint` No two routes share a description. `src: Technical requirements, metadata`
- [ ] `C-TR-24` `contract` The home route description is the studio positioning sentence about 3D web solutions for industry, science, retail. `src: Technical requirements, metadata`
- [ ] `C-TR-25` `contract` A case detail title carries the case title with the studio name appended. `src: Technical requirements, metadata`
- [ ] `C-TR-26` `literal` The social preview sets `twitter:card` to the large-image summary form. `src: Technical requirements, metadata`
- [ ] `C-TR-27` `constraint` No locale alternate is declared. `src: Technical requirements, metadata`
- [ ] `C-TR-28` `literal` The app lists every public route in `/sitemap.xml`. `src: Technical requirements, sitemap`
- [ ] `C-TR-29` `literal` The app names the sitemap inside `/robots.txt`. `src: Technical requirements, sitemap`
- [ ] `C-TR-30` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements, credentials`
- [ ] `C-TR-31` `contract` Every route holds sixty frames per second during scrolling with the stage running. `src: Technical requirements, frame budget`
- [ ] `C-TR-32` `contract` The first meaningful frame includes the stage. `src: Technical requirements, frame budget`
- [ ] `C-TR-33` `constraint` A route change rebuilds no drawing surface. `src: Technical requirements, frame budget`
- [ ] `C-TR-34` `constraint` Only compositing properties change during scroll. `src: Technical requirements, frame budget`
- [ ] `C-TR-35` `constraint` No scroll handler reads a layout property. `src: Technical requirements, frame budget`
- [ ] `C-TR-36` `constraint` The app makes no external network call at run time. `src: Technical requirements, network`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema carries nine tables. `src: Data model para 1`
- [ ] `C-DM-02` `constraint` Every timestamp is UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-04` `literal` The seeded password is written into `/app/USER_README.md` beside each account. `src: Data model, password paragraph`
- [ ] `C-DM-05` `data` An account carries an id, an email unique without regard to case, a password hash, a role, a creation time. `src: Data model, accounts`
- [ ] `C-DM-06` `data` A solution carries an id, a unique slug, a name, two category lines, a theme, a scene key. `src: Data model, solutions`
- [ ] `C-DM-07` `data` A solution section carries a kind of `mechanism` or `feature`, a heading, a body, a position. `src: Data model, solution_sections`
- [ ] `C-DM-08` `data` A service carries a unique anchor, a heading, a navigation caption, a navigation sub-caption, two promises. `src: Data model, services`
- [ ] `C-DM-09` `data` A service bullet carries a label, a sentence, a position. `src: Data model, service_bullets`
- [ ] `C-DM-10` `data` A case carries a unique slug, a unique two-digit number, a client, a title, a brief paragraph, a result paragraph. `src: Data model, cases`
- [ ] `C-DM-11` `data` A case carries a status of `draft` or `published`. `src: Data model, cases`
- [ ] `C-DM-12` `data` A case carries a published time that is null for a draft case. `src: Data model, cases`
- [ ] `C-DM-13` `constraint` Public readability is derived from the case status rather than stored twice. `src: Data model, cases`
- [ ] `C-DM-14` `data` A case section carries an optional media element, an optional caption, a heading, a body, a position. `src: Data model, case_sections`
- [ ] `C-DM-15` `data` A media row carries a unique object key, a content type, a byte size, a digest, alternative text. `src: Data model, media`
- [ ] `C-DM-16` `data` A media row carries a kind of `cover` or `body`. `src: Data model, media`
- [ ] `C-DM-17` `data` An enquiry carries a name, an email address, an optional organisation, a message, a submission time. `src: Data model, enquiries`
- [ ] `C-DM-18` `data` An enquiry carries a read time that is null until an editor marks the enquiry read. `src: Data model, enquiries`
- [ ] `C-DM-19` `data` A page view carries a route plus the time of the view. `src: Data model, page_views`
- [ ] `C-DM-20` `data` A consent row carries a visitor token, whether analytics are allowed, when the choice was made. `src: Data model, consents`
- [ ] `C-DM-21` `constraint` A draft case is absent from every public listing. `src: Data model, invariants`
- [ ] `C-DM-22` `constraint` A draft case is denied on a direct read by slug to anyone who is not an editor. `src: Data model, invariants`
- [ ] `C-DM-23` `constraint` Every object key is unique. `src: Data model, invariants`
- [ ] `C-DM-24` `constraint` Every case number is unique across cases. `src: Data model, invariants`
- [ ] `C-DM-25` `constraint` A decorative media row carries the empty string as alternative text. `src: Data model, invariants`
- [ ] `C-DM-26` `constraint` A rejected enquiry writes no row, no partial row, no object. `src: Data model, invariants`
- [ ] `C-DM-27` `literal` The seed carries three solutions named `Cirrus`, `Emporium`, `Facet`. `src: Data model, seed data`
- [ ] `C-DM-28` `literal` The seed carries four services anchored `graphics`, `ui`, `assets`, `cloud`. `src: Data model, seed data`
- [ ] `C-DM-29` `literal` The seed carries eight cases, seven published, one draft slugged `substation-twin`. `src: Data model, seed data`
- [ ] `C-DM-30` `constraint` The seed carries exactly three mechanism rows per solution. `src: Data model, seed data`
- [ ] `C-DM-31` `constraint` The seed carries exactly four bullets per service. `src: Data model, seed data`
- [ ] `C-DM-32` `constraint` The seed carries no enquiry. `src: Data model, seed data`
- [ ] `C-DM-33` `constraint` Seeding is idempotent, so restarting the app duplicates no row. `src: Data model, seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one tenant. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app carries no organisation, no team, no workspace. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` The app paginates neither the cases index nor any other listing. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` The app carries no likes. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The app carries no second locale. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The app carries no pricing. `src: Constraints bullet 5`
- [ ] `C-CN-07` `constraint` The app carries no subscription. `src: Constraints bullet 5`
- [ ] `C-CN-08` `constraint` The app sends no data to a third-party analytics service. `src: Constraints bullet 6`
- [ ] `C-CN-09` `constraint` The page-view log is read by an editor only. `src: Constraints bullet 6`
- [ ] `C-CN-10` `constraint` The app offers no offline mode. `src: Constraints bullet 7`
- [ ] `C-CN-11` `constraint` The app carries no sitemap page in the navigation. `src: Constraints bullet 8`
- [ ] `C-CN-12` `constraint` Every texture, every mark, every scene, every media stand-in is generated. `src: Constraints bullet 9`
- [ ] `C-CN-13` `constraint` The app hard-codes no scroll trigger point. `src: Constraints bullet 10`
- [ ] `C-CN-14` `constraint` The app stays responsive with a few hundred enquiries. `src: Constraints bullet 11`
- [ ] `C-CN-15` `constraint` The app stays responsive with a few thousand page-view rows. `src: Constraints bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `constraint` The app hardcodes neither the public URL nor the public port. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `literal` The app answers `GET /api/health` with `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-08` `literal` A reserved `.browser_screenshots/` directory exists empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `literal` A reserved `.downloads/` directory exists empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `contract` The app serves a production build behind a static server rather than a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-11` `contract` The server keeps running after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-12` `contract` The server is no child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-13` `literal` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-14` `constraint` The server binds neither `127.0.0.1` nor `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-15` `constraint` The app downloads no copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-16` `constraint` The app uses no edge function. `src: Deployment contract bullet 11`
- [ ] `C-DC-17` `constraint` The app uses no persistent volume. `src: Deployment contract bullet 12`
- [ ] `C-DC-18` `constraint` The app uses no fixed container name. `src: Deployment contract bullet 12`
- [ ] `C-DC-19` `constraint` The app uses no custom network. `src: Deployment contract bullet 12`
- [ ] `C-DC-20` `contract` Every list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `contract` An invalid call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `contract` An unauthorized call is rejected rather than served silently. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `contract` Bearer authentication is required on every endpoint except signup, login, health, the public read routes, the consent route, the enquiry submission. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `constraint` No in-memory buffer stands in for the object store. `src: Deployment contract, No mocks`
- [ ] `C-DC-25` `constraint` No file on the app container filesystem stands in for the object store. `src: Deployment contract, No mocks`
- [ ] `C-DC-26` `constraint` No base64 database column stands in for the object store. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `editor@example.com` | pinned value | C-RL-31 | User roles, seeded accounts table |
| `reader@example.com` | pinned value | C-RL-32 | User roles, seeded accounts table |
| `reader2@example.com` | pinned value | C-RL-33 | User roles, seeded accounts table |
| `deku-demo-pw-2026` | pinned value | C-RL-34 | User roles, seeded accounts table |
| `/terms/` | pinned value | C-CF-15 | Core features, The stage rule 1 |
| `/privacy/` | pinned value | C-CF-16 | Core features, The stage rule 1 |
| `/cookies/` | pinned value | C-CF-17 | Core features, The stage rule 1 |
| `/api/cases` | pinned value | C-CF-40 | Core features, Case studies rule 1 |
| `STORAGE_BUCKET` | pinned value | C-CF-56 | Core features, Media para 1 |
| `STORAGE_ENDPOINT` | pinned value | C-CF-57 | Core features, Media para 1 |
| `STORAGE_ACCESS_KEY` | pinned value | C-CF-58 | Core features, Media para 1 |
| `STORAGE_SECRET_KEY` | pinned value | C-CF-59 | Core features, Media para 1 |
| `cases/{case_id}/{sha256_of_bytes}.{ext}` | pinned value | C-CF-62 | Core features, Media rule 1 |
| `/cirrus/` | pinned value | C-CF-68 | Core features, Product lines para 1 |
| `/emporium/` | pinned value | C-CF-69 | Core features, Product lines para 1 |
| `/facet/` | pinned value | C-CF-70 | Core features, Product lines para 1 |
| `/solutions/` | pinned value | C-CF-71 | Core features, Product lines rule 5 |
| `/services/` | pinned value | C-CF-78 | Core features, Services para 1 |
| `/services/#graphics` | pinned value | C-CF-79 | Core features, Services para 1 |
| `/services/#ui` | pinned value | C-CF-80 | Core features, Services para 1 |
| `/services/#assets` | pinned value | C-CF-81 | Core features, Services para 1 |
| `/services/#cloud` | pinned value | C-CF-82 | Core features, Services para 1 |
| `01` | pinned value | C-CF-85 | Core features, Cases index table |
| `07` | pinned value | C-CF-85 | Core features, Cases index table |
| `08` | pinned value | C-CF-86 | Core features, Cases index para 3 |
| `Substation Twin` | pinned value | C-CF-86 | Core features, Cases index para 3 |
| `/cases/substation-twin` | pinned value | C-CF-87 | Core features, Cases index para 3 |
| `/studio/enquiries` | pinned value | C-CF-107 | Core features, Contact rule 5 |
| `Cookie Policy` | pinned value | C-CF-123 | Core features, Legal rule 3 |
| `OK` | pinned value | C-CF-124 | Core features, Legal rule 3 |
| `/sitemap.xml` | pinned value | C-CF-134 | Core features, Sitemap rule 1 |
| `/robots.txt` | pinned value | C-CF-136 | Core features, Sitemap rule 2 |
| `/studio/cases` | pinned value | C-CF-139 | Core features, Studio console para 1 |
| `/studio/cases/new` | pinned value | C-CF-142 | Core features, Studio console para 2 |
| `/` | pinned value | C-UF-01 | User flow route table row 1 |
| `/cases/` | pinned value | C-UF-03 | User flow route table row 7 |
| `/contact/` | pinned value | C-UF-04 | User flow route table row 9 |
| `/login` | pinned value | C-UF-05 | User flow route table row 15 |
| `/signup` | pinned value | C-UF-06 | User flow route table row 16 |
| `DM Sans` | pinned value | C-UX-14 | UI/UX notes, type paragraph |
| `DM Mono` | pinned value | C-UX-15 | UI/UX notes, type paragraph |
| `16px` | pinned value | C-UX-16 | UI/UX notes, type paragraph |
| `20px` | pinned value | C-UX-16 | UI/UX notes, type paragraph |
| `64px` | pinned value | C-UX-17 | UI/UX notes, type paragraph |
| `128px` | pinned value | C-UX-17 | UI/UX notes, type paragraph |
| `48px` | pinned value | C-UX-18 | UI/UX notes, type paragraph |
| `96px` | pinned value | C-UX-18 | UI/UX notes, type paragraph |
| `36px` | pinned value | C-UX-19 | UI/UX notes, type paragraph |
| `72px` | pinned value | C-UX-19 | UI/UX notes, type paragraph |
| `30px` | pinned value | C-UX-20 | UI/UX notes, type paragraph |
| `24px` | pinned value | C-UX-21 | UI/UX notes, type paragraph |
| `32px` | pinned value | C-UX-21 | UI/UX notes, type paragraph |
| `12px` | pinned value | C-UX-22 | UI/UX notes, type paragraph |
| `width=device-width, initial-scale=1.0` | pinned value | C-UX-62 | UI/UX notes, responsive paragraph |
| `Cirrus` | pinned value | C-FE-36 | Front-end specification, dropdown table |
| `Data` | pinned value | C-FE-36 | Front-end specification, dropdown table |
| `Emporium` | pinned value | C-FE-37 | Front-end specification, dropdown table |
| `Retail` | pinned value | C-FE-37 | Front-end specification, dropdown table |
| `Facet` | pinned value | C-FE-38 | Front-end specification, dropdown table |
| `Next up` | pinned value | C-FE-47 | Front-end specification, calls to action table |
| `Explore our` | pinned value | C-FE-47 | Front-end specification, calls to action table |
| `Solutions` | pinned value | C-FE-47 | Front-end specification, calls to action table |
| `Have a project in mind?` | pinned value | C-FE-48 | Front-end specification, calls to action table |
| `Let's` | pinned value | C-FE-48 | Front-end specification, calls to action table |
| `Talk` | pinned value | C-FE-48 | Front-end specification, calls to action table |
| `contact` | pinned value | C-FE-49 | Front-end specification, footer |
| `terms` | pinned value | C-FE-49 | Front-end specification, footer |
| `privacy` | pinned value | C-FE-49 | Front-end specification, footer |
| `Back to top` | pinned value | C-FE-50 | Front-end specification, footer |
| `Scroll down` | pinned value | C-FE-58 | Front-end specification, loader |
| `Your browser does not support the video tag.` | pinned value | C-FE-59 | Front-end specification, loader |
| `Adding` | pinned value | C-FE-76 | Front-end specification, route compositions |
| `Dimension` | pinned value | C-FE-76 | Front-end specification, route compositions |
| `to the web` | pinned value | C-FE-76 | Front-end specification, route compositions |
| `Take a look at our` | pinned value | C-FE-81 | Front-end specification, route compositions |
| `Services` | pinned value | C-FE-81 | Front-end specification, route compositions |
| `View` | pinned value | C-FE-89 | Front-end specification, route compositions |
| `All cases` | pinned value | C-FE-89 | Front-end specification, route compositions |
| `Hello` | pinned value | C-FE-92 | Front-end specification, route compositions |
| `How can` | pinned value | C-FE-92 | Front-end specification, route compositions |
| `we assist` | pinned value | C-FE-92 | Front-end specification, route compositions |
| `you today?` | pinned value | C-FE-92 | Front-end specification, route compositions |
| `studio@prismlabs.co` | pinned value | C-FE-93 | Front-end specification, route compositions |
| `Ridderstraat 118` | pinned value | C-FE-94 | Front-end specification, route compositions |
| `2200 Herentals` | pinned value | C-FE-94 | Front-end specification, route compositions |
| `Belgium` | pinned value | C-FE-94 | Front-end specification, route compositions |
| `Business Info` | pinned value | C-FE-95 | Front-end specification, route compositions |
| `Meridian Comm. V.` | pinned value | C-FE-95 | Front-end specification, route compositions |
| `BE 0000 000 000` | pinned value | C-FE-95 | Front-end specification, route compositions |
| `Page Not` | pinned value | C-FE-97 | Front-end specification, route compositions |
| `Found` | pinned value | C-FE-97 | Front-end specification, route compositions |
| `An astonishing` | pinned value | C-FE-104 | Front-end specification, copy deck |
| `80%` | pinned value | C-FE-104 | Front-end specification, copy deck |
| `Services to amplify your next web project` | pinned value | C-FE-105 | Front-end specification, copy deck |
| `Oil & Gas Data Visualization` | pinned value | C-FE-106 | Front-end specification, copy deck |
| `Delta AI` | pinned value | C-FE-107 | Front-end specification, copy deck |
| `SvelteKit` | pinned value | C-TR-03 | Technical requirements para 1 |
| `Hono` | pinned value | C-TR-04 | Technical requirements para 1 |
| `PostgreSQL` | pinned value | C-TR-05 | Technical requirements para 1 |
| `DATABASE_URL` | pinned value | C-TR-05 | Technical requirements para 1 |
| `minio` | pinned value | C-TR-06 | Technical requirements para 1 |
| `GET /api/health` | pinned value | C-TR-09 | Technical requirements para 1 |
| `200` | pinned value | C-TR-09 | Technical requirements para 1 |
| `twitter:card` | pinned value | C-TR-26 | Technical requirements, metadata |
| `/app/USER_README.md` | pinned value | C-DM-04 | Data model, password paragraph |
| `graphics` | pinned value | C-DM-28 | Data model, seed data |
| `ui` | pinned value | C-DM-28 | Data model, seed data |
| `assets` | pinned value | C-DM-28 | Data model, seed data |
| `cloud` | pinned value | C-DM-28 | Data model, seed data |
| `substation-twin` | pinned value | C-DM-29 | Data model, seed data |
| `APP_PUBLIC_URL` | pinned value | C-DC-01 | Deployment contract bullet 1 |
| `${APP_PUBLIC_PORT}:4173` | pinned value | C-DC-02 | Deployment contract bullet 1 |
| `.browser_screenshots/` | pinned value | C-DC-08 | Deployment contract bullet 6 |
| `.downloads/` | pinned value | C-DC-09 | Deployment contract bullet 6 |
| `0.0.0.0` | pinned value | C-DC-13 | Deployment contract bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the two social profile addresses | C-OV-07 | named by role with no address given |
| the maps link target | C-CF-96 | named by label with no address given |
| the scene class carried by the third product line | C-FE-07 | named by role with no class string given |
| the copyright year in the footer | C-FE-49 | named by role with no value given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 25 |
| User roles | 2 | 34 |
| Core features | 19 | 147 |
| User flow | 9 | 30 |
| UI and UX notes | 6 | 67 |
| Front-end specification | 24 | 108 |
| Technical requirements | 7 | 36 |
| Data model | 3 | 33 |
| Constraints | 2 | 15 |
| Deployment contract | 9 | 26 |
