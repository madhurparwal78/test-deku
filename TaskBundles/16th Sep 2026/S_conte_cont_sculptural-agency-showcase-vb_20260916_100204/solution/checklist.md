# Checklist: Iron Wood

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 579
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves the public website of the Iron Wood studio. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app serves a signed-in studio for the site's editors. `src: Overview para 1`
- [ ] `C-OV-03` `ui` The award badges sit directly under the first self-description paragraph on the home page. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The public site carries ten content routes. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The public site carries a terms page. `src: Overview para 2`
- [ ] `C-OV-06` `capability` The public site carries an error page. `src: Overview para 2`
- [ ] `C-OV-07` `constraint` A draft is refused on its public page to everyone except the owning editor. `src: Overview para 4`
- [ ] `C-OV-08` `constraint` A draft never appears in a listing, a category count or the sitemap. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An editor signs in to the studio. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An editor creates a case study as a draft. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An editor creates an article as a draft. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An editor publishes a case study owned by that same editor. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An editor unpublishes an entry owned by that same editor. `src: User roles table row 1`
- [ ] `C-RL-06` `role` An editor uploads an image to an entry owned by that same editor. `src: User roles table row 1`
- [ ] `C-RL-07` `role` An editor reads a draft owned by that same editor. `src: User roles table row 1`
- [ ] `C-RL-08` `role` An editor reads every enquiry. `src: User roles table row 1`
- [ ] `C-RL-09` `role` An editor moves an enquiry forward through the enquiry states. `src: User roles table row 1`
- [ ] `C-RL-10` `role` The app denies an editor access to a draft owned by another editor. `src: User roles table row 1`
- [ ] `C-RL-11` `role` The app denies an editor the ability to publish a draft owned by another editor. `src: User roles table row 1`
- [ ] `C-RL-12` `role` The app denies an editor access to a draft image owned by another editor. `src: User roles table row 1`
- [ ] `C-RL-13` `role` The app denies an editor the ability to edit a published entry owned by another editor. `src: User roles table row 1`
- [ ] `C-RL-14` `role` A client signs up without an invitation. `src: User roles table row 2`
- [ ] `C-RL-15` `role` A client reads every published page. `src: User roles table row 2`
- [ ] `C-RL-16` `role` An enquiry sent by a signed-in client is attached to the client's account. `src: User roles table row 2`
- [ ] `C-RL-17` `role` A client reads the enquiries attached to the client's own account. `src: User roles table row 2`
- [ ] `C-RL-18` `role` The app denies a client access to any draft record. `src: User roles table row 2`
- [ ] `C-RL-19` `role` The app denies a client access to any draft image. `src: User roles table row 2`
- [ ] `C-RL-20` `role` The app denies a client the ability to create a case study. `src: User roles table row 2`
- [ ] `C-RL-21` `role` The app denies a client the ability to upload an image. `src: User roles table row 2`
- [ ] `C-RL-22` `role` The app denies a client access to another person's enquiries. `src: User roles table row 2`
- [ ] `C-RL-23` `role` The app denies a client the ability to change an enquiry state. `src: User roles table row 2`
- [ ] `C-RL-24` `role` A visitor with no account sends an enquiry. `src: User roles para 1`
- [ ] `C-RL-25` `role` An anonymous enquiry is stored with no account attached. `src: User roles para 1`
- [ ] `C-RL-26` `role` The app rejects a direct API call from a client session to an editor-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-27` `role` A rejected authorization attempt leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-28` `constraint` Signup creates a client account with no approval step. `src: User roles, signup paragraph`
- [ ] `C-RL-29` `constraint` The site never creates an editor account through signup. `src: User roles, signup paragraph`
- [ ] `C-RL-30` `literal` The seeded account `editor@example.com` holds the role `editor`. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-31` `literal` The seeded account `editor2@example.com` holds the role `editor`. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-32` `literal` The seeded account `client@example.com` holds the role `client`. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-33` `literal` The seeded account for Nadia carries the display name `Nadia Brooks`. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-34` `literal` The seeded account for Owen carries the display name `Owen Pike`. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-35` `literal` The seeded account for Leo carries the display name `Leo Marsh`. `src: User roles, seeded accounts table row 3`

## C-CF Core features

- [ ] `C-CF-01` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `constraint` The app stores each password only as a hash. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `literal` A successful `POST /api/auth/login` returns a bearer token in the field `access_token`. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `capability` Protected API requests carry the bearer token. `src: Core features, Auth para 1`
- [ ] `C-CF-05` `ui` An expired session mid-action shows an inline banner offering a fresh sign-in. `src: Core features, Auth para 1`
- [ ] `C-CF-06` `ui` An expired session mid-action keeps the form the person was filling. `src: Core features, Auth para 1`
- [ ] `C-CF-07` `literal` `POST /api/auth/sign-up` takes the fields `email`, `password`, `display_name`. `src: Core features, Auth para 2`
- [ ] `C-CF-08` `capability` Sign-up creates a client account. `src: Core features, Auth para 2`
- [ ] `C-CF-09` `constraint` A second signup with an address already in use is refused as invalid. `src: Core features, Auth para 2`
- [ ] `C-CF-10` `constraint` A refused duplicate signup creates no account. `src: Core features, Auth para 2`
- [ ] `C-CF-11` `constraint` The app offers no password reset flow. `src: Core features, Auth para 2`
- [ ] `C-CF-12` `capability` Editors keep case studies. `src: Core features, publication para 1`
- [ ] `C-CF-13` `capability` Editors keep articles. `src: Core features, publication para 1`
- [ ] `C-CF-14` `literal` Each entry carries a `state` of `draft` or `published`. `src: Core features, publication para 1`
- [ ] `C-CF-15` `constraint` A slug holds lowercase letters, digits or hyphens, starting with a letter. `src: Core features, publication para 1`
- [ ] `C-CF-16` `capability` An editor creates each new entry as a draft. `src: Core features rule 1`
- [ ] `C-CF-17` `constraint` The app refuses a draft's public page to an anonymous visitor. `src: Core features rule 1`
- [ ] `C-CF-18` `constraint` The app refuses a draft's API record to an anonymous visitor. `src: Core features rule 1`
- [ ] `C-CF-19` `constraint` The app refuses a draft's API record to a client. `src: Core features rule 1`
- [ ] `C-CF-20` `constraint` The app refuses a draft's API record to a different editor. `src: Core features rule 1`
- [ ] `C-CF-21` `constraint` The app refuses a draft's stored image to everyone except the owning editor. `src: Core features rule 1`
- [ ] `C-CF-22` `constraint` A refused draft request discloses nothing about the draft's existence. `src: Core features rule 1`
- [ ] `C-CF-23` `constraint` A draft never appears in the case study index. `src: Core features rule 2`
- [ ] `C-CF-24` `constraint` A draft never appears in the article archive. `src: Core features rule 2`
- [ ] `C-CF-25` `constraint` A draft never counts toward a category's entry count. `src: Core features rule 2`
- [ ] `C-CF-26` `constraint` A draft never appears among the related articles on an article page. `src: Core features rule 2`
- [ ] `C-CF-27` `constraint` A draft never appears in the next-project section of a case study. `src: Core features rule 2`
- [ ] `C-CF-28` `constraint` A draft address never appears in the sitemap. `src: Core features rule 2`
- [ ] `C-CF-29` `capability` Publishing an entry makes the entry readable at its public route. `src: Core features rule 3`
- [ ] `C-CF-30` `capability` Publishing an entry stamps `published_at` in UTC. `src: Core features rule 3`
- [ ] `C-CF-31` `capability` Publishing a case study appends the case study to the index listing. `src: Core features rule 3`
- [ ] `C-CF-32` `capability` Publishing a case study adds the case study address to the sitemap. `src: Core features rule 3`
- [ ] `C-CF-33` `capability` Unpublishing withdraws the public page from everyone except the owner. `src: Core features rule 3`
- [ ] `C-CF-34` `capability` Unpublishing withdraws the API record from everyone except the owner. `src: Core features rule 3`
- [ ] `C-CF-35` `capability` Unpublishing withdraws the entry's images from everyone except the owner. `src: Core features rule 3`
- [ ] `C-CF-36` `capability` Unpublishing removes the entry from its listing. `src: Core features rule 3`
- [ ] `C-CF-37` `capability` Unpublishing removes the entry address from the sitemap. `src: Core features rule 3`
- [ ] `C-CF-38` `capability` Unpublishing an article lowers the category entry count. `src: Core features rule 3`
- [ ] `C-CF-39` `constraint` At most one published case study holds a given slug. `src: Core features rule 4`
- [ ] `C-CF-40` `constraint` At most one published article holds a given slug. `src: Core features rule 4`
- [ ] `C-CF-41` `capability` A draft may hold a slug already taken by a published entry. `src: Core features rule 4`
- [ ] `C-CF-42` `constraint` Publishing a draft onto a taken slug is refused as a conflict. `src: Core features rule 4`
- [ ] `C-CF-43` `constraint` A draft refused on a taken slug stays a draft. `src: Core features rule 4`
- [ ] `C-CF-44` `constraint` Two simultaneous publishes claiming one slug never both succeed. `src: Core features rule 4`
- [ ] `C-CF-45` `constraint` The losing publish leaves no half-published entry. `src: Core features rule 4`
- [ ] `C-CF-46` `constraint` The losing publish takes no listing position. `src: Core features rule 4`
- [ ] `C-CF-47` `data` A case study references services by relation rows. `src: Core features rule 5`
- [ ] `C-CF-48` `constraint` Naming a service outside the eight services is refused as invalid. `src: Core features rule 5`
- [ ] `C-CF-49` `constraint` A case study refused for an unknown service writes nothing. `src: Core features rule 5`
- [ ] `C-CF-50` `capability` The case study services list renders on the index row. `src: Core features rule 5`
- [ ] `C-CF-51` `capability` The case study services list renders on the case study page. `src: Core features rule 5`
- [ ] `C-CF-52` `data` An article references exactly one category. `src: Core features rule 6`
- [ ] `C-CF-53` `constraint` An article with no category is refused as invalid. `src: Core features rule 6`
- [ ] `C-CF-54` `constraint` An article with an unknown category is refused as invalid. `src: Core features rule 6`
- [ ] `C-CF-55` `role` A write from a different editor leaves an entry unchanged. `src: Core features rule 7`
- [ ] `C-CF-56` `literal` Uploaded images live in the MinIO bucket named by `STORAGE_BUCKET`. `src: Core features, images para 1`
- [ ] `C-CF-57` `literal` The object key follows `media/{kind}/{entry_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 8`
- [ ] `C-CF-58` `literal` The key segment `kind` reads `case-study` or `article`. `src: Core features rule 8`
- [ ] `C-CF-59` `capability` An upload records the object key, the content type, the byte size, the alternative text. `src: Core features rule 8`
- [ ] `C-CF-60` `constraint` Uploaded image bytes reach the bucket rather than the app container's filesystem. `src: Core features rule 8`
- [ ] `C-CF-61` `constraint` No database column holds image bytes. `src: Core features rule 8`
- [ ] `C-CF-62` `literal` The app accepts only `image/png`, `image/jpeg` or `image/webp` uploads. `src: Core features rule 9`
- [ ] `C-CF-63` `literal` The app accepts uploads up to `5 MB`. `src: Core features rule 9`
- [ ] `C-CF-64` `constraint` A refused upload reaches neither the bucket nor the database. `src: Core features rule 9`
- [ ] `C-CF-65` `literal` Image bytes are served through `GET /api/media/{asset_id}/content`. `src: Core features rule 10`
- [ ] `C-CF-66` `capability` The media content route streams an image of a published entry to anyone. `src: Core features rule 10`
- [ ] `C-CF-67` `capability` The media content route streams a draft image to the owning editor. `src: Core features rule 10`
- [ ] `C-CF-68` `constraint` The bucket refuses unsigned public reads. `src: Core features rule 10`
- [ ] `C-CF-69` `constraint` The app issues no time-limited link to a stored object. `src: Core features rule 10`
- [ ] `C-CF-70` `constraint` The same bytes sent twice to one entry create no second object. `src: Core features rule 11`
- [ ] `C-CF-71` `constraint` The same bytes sent twice to one entry create no second asset record. `src: Core features rule 11`
- [ ] `C-CF-72` `capability` A repeated upload returns the existing asset. `src: Core features rule 11`
- [ ] `C-CF-73` `constraint` An upload without alternative text is refused as invalid. `src: Core features rule 12`
- [ ] `C-CF-74` `capability` Uploaded images appear on the entry page in upload order with their alternative text. `src: Core features rule 12`
- [ ] `C-CF-75` `capability` The index at `/works` lists every published case study as a row. `src: Core features rule 13`
- [ ] `C-CF-76` `literal` The ten seeded case studies lead the index in seeded order. `src: Core features rule 13`
- [ ] `C-CF-77` `capability` A case study published later joins the end of the index. `src: Core features rule 13`
- [ ] `C-CF-78` `capability` Index rows alternate the picture side, starting with the picture on the right. `src: Core features rule 14`
- [ ] `C-CF-79` `literal` Each index row carries `data-case-study-row`. `src: Core features rule 14`
- [ ] `C-CF-80` `literal` Each index row carries `data-slug` set to the case study slug. `src: Core features rule 14`
- [ ] `C-CF-81` `literal` Each index row carries `data-image-side` set to `right` or `left`. `src: Core features rule 14`
- [ ] `C-CF-82` `capability` An index row shows the case study label, title, services list. `src: Core features rule 15`
- [ ] `C-CF-83` `capability` An index row opens the case study page at `/works/{slug}`. `src: Core features rule 15`
- [ ] `C-CF-84` `capability` A case study page shows the client name above a subtitle. `src: Core features rule 16`
- [ ] `C-CF-85` `literal` The case study fact sheet carries a `Visit site` link to the client site. `src: Core features rule 16`
- [ ] `C-CF-86` `literal` The case study fact sheet shows the `Industry` label beside the case study label. `src: Core features rule 16`
- [ ] `C-CF-87` `literal` The case study fact sheet shows the `Year` label beside the case study year. `src: Core features rule 16`
- [ ] `C-CF-88` `capability` A case study page shows the case study body. `src: Core features rule 16`
- [ ] `C-CF-89` `literal` The closing section headed `Next project` names the next case study in index order. `src: Core features rule 16`
- [ ] `C-CF-90` `capability` The next project of the last case study is the first case study. `src: Core features rule 16`
- [ ] `C-CF-91` `capability` The archive at `/blog` lists published articles newest first. `src: Core features rule 17`
- [ ] `C-CF-92` `capability` The archive shows four articles to a page. `src: Core features rule 17`
- [ ] `C-CF-93` `literal` Each archive row carries `data-article-row`. `src: Core features rule 17`
- [ ] `C-CF-94` `literal` Each archive row carries `data-slug`. `src: Core features rule 17`
- [ ] `C-CF-95` `literal` Each archive row shows the reading time in the form `7 min read`. `src: Core features rule 17`
- [ ] `C-CF-96` `capability` Each archive row shows the article category, title, publication date. `src: Core features rule 17`
- [ ] `C-CF-97` `literal` The pagination control carries the label `More`. `src: Core features rule 18`
- [ ] `C-CF-98` `literal` The pagination control carries `data-pagination="next"`. `src: Core features rule 18`
- [ ] `C-CF-99` `literal` The pagination control links to the next page as `?page=2`. `src: Core features rule 18`
- [ ] `C-CF-100` `capability` Pressing More appends the next rows beneath the rows already shown without reloading the document. `src: Core features rule 18`
- [ ] `C-CF-101` `constraint` The last archive page offers no More control. `src: Core features rule 18`
- [ ] `C-CF-102` `capability` An archive page such as `/blog?page=2` renders on its own. `src: Core features rule 18`
- [ ] `C-CF-103` `literal` The category tabs run `All`, `Product design`, `Engineering`, `Studio life`. `src: Core features rule 19`
- [ ] `C-CF-104` `capability` Each category tab links to the category route `/blog-categories/{slug}`. `src: Core features rule 19`
- [ ] `C-CF-105` `literal` Each category tab carries the published count as `data-count`. `src: Core features rule 19`
- [ ] `C-CF-106` `literal` The tab for the current page carries `aria-current="page"`. `src: Core features rule 19`
- [ ] `C-CF-107` `capability` A category route lists only published articles of the category. `src: Core features rule 20`
- [ ] `C-CF-108` `capability` A category route paginates in the archive template. `src: Core features rule 20`
- [ ] `C-CF-109` `capability` An article page shows the article title, category, date, reading time. `src: Core features rule 21`
- [ ] `C-CF-110` `capability` An article page shows the article body beside a contents list. `src: Core features rule 21`
- [ ] `C-CF-111` `literal` The article reading progress bar carries `data-reading-progress`. `src: Core features rule 21`
- [ ] `C-CF-112` `capability` The related articles on an article page come from the same category. `src: Core features rule 21`
- [ ] `C-CF-113` `ui` The article sidebar carries share links beside the contents list. `src: Core features rule 21`
- [ ] `C-CF-114` `capability` The related section holds up to two of the newest published articles of the category other than the current article. `src: Core features rule 21`
- [ ] `C-CF-115` `constraint` Only article pages carry `data-reading-progress`. `src: Core features rule 21`
- [ ] `C-CF-116` `literal` The contact form carries `data-enquiry-form`. `src: Core features rule 22`
- [ ] `C-CF-117` `literal` The contact form fields carry the names `Service`, `Budget`, `Name`, `Email`, `Message`. `src: Core features rule 22`
- [ ] `C-CF-118` `literal` A hidden field named `bpGCap` carries the bot-check token. `src: Core features rule 22`
- [ ] `C-CF-119` `literal` A decoy field named `Website` sits in the form out of sight. `src: Core features rule 22`
- [ ] `C-CF-120` `capability` The Service field offers the eight services as fixed options. `src: Core features rule 23`
- [ ] `C-CF-121` `literal` The Budget field offers `Under $10k`, `$10k - $30k`, `$30k - $60k`, `$60k - $100k`, `Over $100k`. `src: Core features rule 23`
- [ ] `C-CF-122` `constraint` A Service value outside the options is refused with nothing stored. `src: Core features rule 23`
- [ ] `C-CF-123` `constraint` A Budget value outside the options is refused with nothing stored. `src: Core features rule 23`
- [ ] `C-CF-124` `constraint` An enquiry with an empty Name is refused. `src: Core features rule 24`
- [ ] `C-CF-125` `constraint` An enquiry with an empty Email is refused. `src: Core features rule 24`
- [ ] `C-CF-126` `constraint` An enquiry with an empty Message is refused. `src: Core features rule 24`
- [ ] `C-CF-127` `constraint` An enquiry with a malformed email address is refused as invalid. `src: Core features rule 24`
- [ ] `C-CF-128` `capability` An enquiry refusal names the field at fault. `src: Core features rule 24`
- [ ] `C-CF-129` `literal` `GET /api/bot-check` returns a `token`. `src: Core features rule 25`
- [ ] `C-CF-130` `capability` The contact page renders with a fresh bot-check token. `src: Core features rule 25`
- [ ] `C-CF-131` `literal` A bot-check token expires after `ten minutes`. `src: Core features rule 25`
- [ ] `C-CF-132` `constraint` A bot-check token serves one submission only. `src: Core features rule 25`
- [ ] `C-CF-133` `constraint` An enquiry with a missing token is refused. `src: Core features rule 25`
- [ ] `C-CF-134` `constraint` An enquiry with an unknown token is refused. `src: Core features rule 25`
- [ ] `C-CF-135` `constraint` An enquiry whose decoy field `Website` arrives filled is refused. `src: Core features rule 26`
- [ ] `C-CF-136` `literal` A third enquiry from one address within `sixty seconds` is refused. `src: Core features rule 26`
- [ ] `C-CF-137` `ui` The failure panel states a plain reason for each refusal. `src: Core features rule 26`
- [ ] `C-CF-138` `literal` An accepted enquiry is stored with the state `new`. `src: Core features rule 27`
- [ ] `C-CF-139` `capability` An accepted enquiry from a signed-in sender carries the sender's account. `src: Core features rule 27`
- [ ] `C-CF-140` `capability` An accepted enquiry makes the success panel replace the form in place without navigating. `src: Core features rule 27`
- [ ] `C-CF-141` `literal` The success panel carries `data-form-result="success"`. `src: Core features rule 27`
- [ ] `C-CF-142` `literal` The success panel heading reads `Thank you. Your enquiry is with us.` `src: Core features rule 27`
- [ ] `C-CF-143` `literal` The success panel line opens `We read every message`, closing `reply within two working days.` `src: Core features rule 27`
- [ ] `C-CF-144` `literal` The failure panel carries `data-form-result="failure"`. `src: Core features rule 28`
- [ ] `C-CF-145` `literal` The failure panel line opens `Something went wrong`, closing `Everything you typed is still here.` `src: Core features rule 28`
- [ ] `C-CF-146` `capability` A failed submission keeps every typed value in its field. `src: Core features rule 28`
- [ ] `C-CF-147` `capability` Both result panels sit hidden in the contact page from the start. `src: Core features rule 28`
- [ ] `C-CF-148` `literal` The contact page carries one element marked `data-bot-check`. `src: Core features rule 29`
- [ ] `C-CF-149` `constraint` No route other than the contact page carries `data-bot-check`. `src: Core features rule 29`
- [ ] `C-CF-150` `literal` An editor moves an enquiry from `new` to `in_conversation`. `src: Core features rule 30`
- [ ] `C-CF-151` `literal` An editor moves an open enquiry to `closed`. `src: Core features rule 30`
- [ ] `C-CF-152` `constraint` A closed enquiry stays closed. `src: Core features rule 30`
- [ ] `C-CF-153` `literal` Enquiry state changes go through `PATCH /api/enquiries/{id}`. `src: Core features rule 30`
- [ ] `C-CF-154` `constraint` A backward enquiry move is refused with the row unchanged. `src: Core features rule 30`
- [ ] `C-CF-155` `literal` `GET /api/enquiries` returns every enquiry to an editor. `src: Core features rule 31`
- [ ] `C-CF-156` `capability` The enquiry list returns only the caller's own enquiries to a client. `src: Core features rule 31`
- [ ] `C-CF-157` `constraint` The enquiry list is refused to a visitor with no session. `src: Core features rule 31`
- [ ] `C-CF-158` `literal` A signed-in client reads enquiries newest first at `/account/enquiries`. `src: Core features rule 31`
- [ ] `C-CF-159` `literal` Each account enquiry row carries `data-enquiry-state`. `src: Core features rule 31`
- [ ] `C-CF-160` `literal` The home page carries one element marked `data-scene="mascot-hero"`. `src: Core features rule 32`
- [ ] `C-CF-161` `literal` The home page carries seven elements marked `data-scene="culture-object"`. `src: Core features rule 32`
- [ ] `C-CF-162` `literal` The case study index carries one element marked `data-scene="works-field"`. `src: Core features rule 32`
- [ ] `C-CF-163` `literal` The case study index carries one element marked `data-scene="works-preview"`. `src: Core features rule 32`
- [ ] `C-CF-164` `constraint` No other route carries a `data-scene` element. `src: Core features rule 32`
- [ ] `C-CF-165` `constraint` A route without a scene starts no renderer. `src: Core features rule 32`
- [ ] `C-CF-166` `literal` The culture objects carry `data-object` in the order `rocket`, `wand`, `arrow`, `bomb`, `thumb`, `bond`, `flame`. `src: Core features rule 33`
- [ ] `C-CF-167` `constraint` Each culture object is a separate scene. `src: Core features rule 33`
- [ ] `C-CF-168` `ui` The home page sculpture draws live only at desktop widths. `src: Core features rule 34`
- [ ] `C-CF-169` `ui` Below desktop width a still of the sculpture stands in the hero. `src: Core features rule 34`
- [ ] `C-CF-170` `ui` The culture objects draw live at every width. `src: Core features rule 34`
- [ ] `C-CF-171` `ui` Both case study index scenes draw live at every width. `src: Core features rule 34`
- [ ] `C-CF-172` `ui` Both case study index scenes draw the faceted honey badger. `src: Core features rule 34`
- [ ] `C-CF-173` `ui` The footer carries a standing still of the mascot. `src: Core features rule 35`
- [ ] `C-CF-174` `ui` The contact hero carries a standing still of the mascot. `src: Core features rule 35`
- [ ] `C-CF-175` `ui` The about page carries a still of the mascot seated in a chair. `src: Core features rule 35`
- [ ] `C-CF-176` `ui` The error page carries a still of a low faceted rock form. `src: Core features rule 35`
- [ ] `C-CF-177` `literal` Every band carries `data-ground` set to `dark`, `light` or `tinted`. `src: Core features rule 36`
- [ ] `C-CF-178` `constraint` No two neighbouring bands share a ground. `src: Core features rule 36`
- [ ] `C-CF-179` `literal` Every route opens on a `dark` band except the case study index, which opens `light`. `src: Core features rule 37`
- [ ] `C-CF-180` `capability` Each route carries its pinned band sequence. `src: Core features rule 37`
- [ ] `C-CF-181` `capability` The home hero shares the first dark band with the process section. `src: Core features rule 37`
- [ ] `C-CF-182` `constraint` The footer carries no `data-ground`. `src: Core features rule 37`
- [ ] `C-CF-183` `literal` The header carries the links `Services.`, `Works.`, `About.`, `Blog.` beside a `Contact` button. `src: Core features rule 38`
- [ ] `C-CF-184` `literal` The drawer carries `Home.`, `Services.`, `Works.`, `About.`, `Blog.`, `Hire us.`. `src: Core features rule 38`
- [ ] `C-CF-185` `literal` The drawer carries the labels `facebook`, `behance`, `instagram`, `dribbble`, `clutch`, `linkedin`, `awwwards`. `src: Core features rule 38`
- [ ] `C-CF-186` `literal` The drawer contact block lists `hello@example.com` under Contact. `src: Core features rule 38`
- [ ] `C-CF-187` `literal` The drawer contact block lists `hr@example.com` under Careers. `src: Core features rule 38`
- [ ] `C-CF-188` `capability` The drawer carries both office addresses. `src: Core features rule 38`
- [ ] `C-CF-189` `capability` The header Contact button opens the contact page. `src: Core features rule 38`
- [ ] `C-CF-190` `literal` The drawer carries the marker `data-drawer`. `src: Core features rule 39`
- [ ] `C-CF-191` `literal` The drawer trigger is a button marked `data-drawer-trigger` reporting `aria-expanded`. `src: Core features rule 39`
- [ ] `C-CF-192` `capability` Every public route except the contact page ends with the footer. `src: Core features rule 40`
- [ ] `C-CF-193` `literal` The footer lead-in reads `Have a product in mind?`. `src: Core features rule 40`
- [ ] `C-CF-194` `literal` The oversized footer link label opens with `Let's build`. `src: Core features rule 40`
- [ ] `C-CF-195` `capability` The oversized footer link opens the contact page. `src: Core features rule 40`
- [ ] `C-CF-196` `literal` The footer copyright line reads `© 2026 Iron Wood - UX UI Design Agency`. `src: Core features rule 40`
- [ ] `C-CF-197` `literal` The footer carries a `Privacy Policy` link to `/privacy-policy`. `src: Core features rule 40`
- [ ] `C-CF-198` `literal` The footer carries a `Terms` link to `/terms`. `src: Core features rule 40`
- [ ] `C-CF-199` `constraint` The footer social labels omit behance. `src: Core features rule 40`
- [ ] `C-CF-200` `literal` The office switcher uses two buttons marked `data-office-switch` reporting `aria-pressed`. `src: Core features rule 41`
- [ ] `C-CF-201` `literal` Exactly one of two images marked `data-office-image` carries `data-active="true"`. `src: Core features rule 41`
- [ ] `C-CF-202` `capability` Pressing an office switch button makes that office image active. `src: Core features rule 41`
- [ ] `C-CF-203` `literal` Each word-by-word heading carries `data-split-heading` with the full text as `aria-label`. `src: Core features rule 42`
- [ ] `C-CF-204` `literal` The services motif carries `data-motif="hive"`. `src: Core features rule 43`
- [ ] `C-CF-205` `literal` The motif holds one part marked `data-motif-part="hive"` beside three orbit parts. `src: Core features rule 43`
- [ ] `C-CF-206` `literal` Exactly one orbit part carries `data-phase="reverse"`. `src: Core features rule 43`
- [ ] `C-CF-207` `capability` Every public route carries a distinct title. `src: Core features rule 44`
- [ ] `C-CF-208` `capability` Every public route carries a distinct meta description. `src: Core features rule 44`
- [ ] `C-CF-209` `literal` The sitemap at `/sitemap.xml` lists every public content route. `src: Core features rule 45`
- [ ] `C-CF-210` `capability` The sitemap lists every published case study, article, category route. `src: Core features rule 45`
- [ ] `C-CF-211` `literal` The robots file at `/robots.txt` carries a full `Sitemap:` address. `src: Core features rule 45`
- [ ] `C-CF-212` `literal` Every public route declares `og:title` with `og:image`. `src: Core features rule 46`
- [ ] `C-CF-213` `literal` The preview image address follows `/social-preview/{page_key}` without a file extension. `src: Core features rule 46`
- [ ] `C-CF-214` `capability` The preview image address answers with a generated image. `src: Core features rule 46`
- [ ] `C-CF-215` `literal` The home page preview image uses the page key `home`. `src: Core features rule 46`
- [ ] `C-CF-216` `capability` The terms page at `/terms` states the terms of use. `src: Core features rule 47`
- [ ] `C-CF-217` `capability` Every route with a footer links to the terms page. `src: Core features rule 47`
- [ ] `C-CF-218` `literal` The sign-up form reads `By creating an account you agree to the Terms of Service.` `src: Core features rule 47`
- [ ] `C-CF-219` `capability` The privacy policy at `/privacy-policy` states what the site stores. `src: Core features rule 48`
- [ ] `C-CF-220` `literal` The privacy policy names `hello@example.com` for removal requests. `src: Core features rule 48`
- [ ] `C-CF-221` `capability` An unknown address answers not-found with the site's own page. `src: Core features rule 49`
- [ ] `C-CF-222` `literal` The not-found page reads `Sorry! The page you're looking for was not found`. `src: Core features rule 49`
- [ ] `C-CF-223` `literal` The not-found page shows `404` beneath the message. `src: Core features rule 49`
- [ ] `C-CF-224` `literal` The not-found page offers a `Back to home` link. `src: Core features rule 49`
- [ ] `C-CF-225` `capability` The not-found page keeps the header, the drawer, the pointer ring. `src: Core features rule 49`
- [ ] `C-CF-226` `constraint` The not-found page carries no footer. `src: Core features rule 49`
- [ ] `C-CF-227` `ui` The not-found page fills one viewport with nothing to scroll. `src: Core features rule 49`

## C-UF User flow

- [ ] `C-UF-01` `capability` The app serves `/` to visitors with no session. `src: User flow, routes table row 1`
- [ ] `C-UF-02` `capability` The app serves `/services` to visitors with no session. `src: User flow, routes table row 2`
- [ ] `C-UF-03` `capability` The app serves `/works` to visitors with no session. `src: User flow, routes table row 3`
- [ ] `C-UF-04` `capability` The app serves a case study page at `/works/{slug}`. `src: User flow, routes table row 4`
- [ ] `C-UF-05` `capability` The app serves `/about-us` to visitors with no session. `src: User flow, routes table row 5`
- [ ] `C-UF-06` `capability` The app serves `/blog` to visitors with no session. `src: User flow, routes table row 6`
- [ ] `C-UF-07` `capability` The app serves an article page at `/blog/{slug}`. `src: User flow, routes table row 7`
- [ ] `C-UF-08` `capability` The app serves a category route at `/blog-categories/{slug}`. `src: User flow, routes table row 8`
- [ ] `C-UF-09` `capability` The app serves `/contact` to visitors with no session. `src: User flow, routes table row 9`
- [ ] `C-UF-10` `capability` The app serves `/privacy-policy` to visitors with no session. `src: User flow, routes table row 10`
- [ ] `C-UF-11` `capability` The app serves `/terms` to visitors with no session. `src: User flow, routes table row 11`
- [ ] `C-UF-12` `capability` The app serves `/sign-in` to visitors with no session. `src: User flow, routes table row 12`
- [ ] `C-UF-13` `capability` The app serves `/sign-up` to visitors with no session. `src: User flow, routes table row 13`
- [ ] `C-UF-14` `role` The page `/account/enquiries` requires a client session. `src: User flow, routes table row 14`
- [ ] `C-UF-15` `role` The page `/studio` requires an editor session. `src: User flow, routes table row 15`
- [ ] `C-UF-16` `role` The wizard step `/studio/new/details` requires an editor session. `src: User flow, routes table row 16`
- [ ] `C-UF-17` `role` The wizard step `/studio/new/media` requires an editor session. `src: User flow, routes table row 17`
- [ ] `C-UF-18` `role` The wizard step `/studio/new/review` requires an editor session. `src: User flow, routes table row 18`
- [ ] `C-UF-19` `role` The entry page `/studio/entries/{kind}/{id}` requires an editor session. `src: User flow, routes table row 19`
- [ ] `C-UF-20` `role` The page `/studio/enquiries` requires an editor session. `src: User flow, routes table row 20`
- [ ] `C-UF-21` `capability` The app serves `/sitemap.xml`. `src: User flow, routes table row 21`
- [ ] `C-UF-22` `capability` The app serves `/robots.txt`. `src: User flow, routes table row 22`
- [ ] `C-UF-23` `capability` The app serves generated preview images under `/social-preview/{page_key}`. `src: User flow, routes table row 23`
- [ ] `C-UF-24` `constraint` The about route keeps the spelling `/about-us`. `src: User flow, routes para 1`
- [ ] `C-UF-25` `capability` A signed-out visitor reaching a protected page is sent to `/sign-in`. `src: User flow, entry para 1`
- [ ] `C-UF-26` `capability` Signing in lands the visitor on the remembered protected address. `src: User flow, entry para 1`
- [ ] `C-UF-27` `capability` Signing in sends an editor to `/studio`. `src: User flow, entry para 1`
- [ ] `C-UF-28` `capability` Signing in sends a client to `/account/enquiries`. `src: User flow, entry para 1`
- [ ] `C-UF-29` `capability` A client reaching a studio page is shown the client's own enquiries. `src: User flow, entry para 1`
- [ ] `C-UF-30` `capability` Signing out returns the visitor to the home page. `src: User flow, entry para 1`
- [ ] `C-UF-31` `ui` Moving between public routes swaps the page without reloading the document. `src: User flow, entry para 1`
- [ ] `C-UF-32` `ui` A route change resets the scroll position to the top of the new route. `src: User flow, entry para 1`
- [ ] `C-UF-33` `ui` The drawer trigger, the pointer ring, the scrolling behaviour survive a route change. `src: User flow, entry para 1`
- [ ] `C-UF-34` `literal` The wizard steps carry `data-wizard-step` set to `details`, `media`, `review`. `src: User flow, journeys para 3`
- [ ] `C-UF-35` `literal` Each studio card carries `data-entry-state`. `src: User flow, journeys para 3`
- [ ] `C-UF-36` `capability` The studio opens on a card grid of the entries the editor owns. `src: User flow, journeys para 3`
- [ ] `C-UF-37` `ui` An inline banner confirms each saved draft or publication in place. `src: User flow, journeys para 3`
- [ ] `C-UF-38` `ui` Every list shows an empty state. `src: User flow, states para 1`
- [ ] `C-UF-39` `ui` Every page shows a loading state. `src: User flow, states para 1`
- [ ] `C-UF-40` `ui` A client with no enquiries sees one sentence with a link to the contact page. `src: User flow, states para 1`
- [ ] `C-UF-41` `ui` Appending the next archive page shows a quiet loading indicator in place of More. `src: User flow, states para 1`
- [ ] `C-UF-42` `ui` A category with no published article shows one sentence under the tabs. `src: User flow, states para 1`
- [ ] `C-UF-43` `ui` A failed request leaves an inline banner on a usable page. `src: User flow, states para 1`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The first screen conveys a studio that has shipped crafted digital products. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` Each public route leads with one clear primary action. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` The studio pages carry a quiet operational register without atmosphere. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `ui` Every type size, line height, gutter, padding is a clean multiple of one base unit. `src: UI/UX notes, scale para`
- [ ] `C-UX-05` `ui` The base unit shifts slightly between laptop, tablet, phone widths. `src: UI/UX notes, scale para`
- [ ] `C-UX-06` `ui` One neo-grotesque sans sets every word of body text or heading text. `src: UI/UX notes, type para`
- [ ] `C-UX-07` `ui` The sans appears in five steps from light to bold. `src: UI/UX notes, type para`
- [ ] `C-UX-08` `ui` One heavy display face appears only on the loader wordmark, the home wordmark, the case study client name. `src: UI/UX notes, type para`
- [ ] `C-UX-09` `constraint` No monospace face loads. `src: UI/UX notes, type para`
- [ ] `C-UX-10` `ui` Headings shrink as the screen narrows. `src: UI/UX notes, type para`
- [ ] `C-UX-11` `ui` The body step grows on a phone, with no body step shrinking there. `src: UI/UX notes, type para`
- [ ] `C-UX-12` `ui` Only the two largest heading steps change at tablet width. `src: UI/UX notes, type para`
- [ ] `C-UX-13` `ui` The wordmark `Ironwood` fills the full content width on a laptop. `src: UI/UX notes, type para`
- [ ] `C-UX-14` `ui` The dark ground is a near-black neutral shared by strong ink. `src: UI/UX notes, colour para`
- [ ] `C-UX-15` `ui` The light ground is white, the tinted ground a near-white neutral. `src: UI/UX notes, colour para`
- [ ] `C-UX-16` `ui` Body ink is a deep neutral, muted ink a lighter deep neutral. `src: UI/UX notes, colour para`
- [ ] `C-UX-17` `ui` Copy on dark grounds is white, muted copy on dark grounds white at half strength. `src: UI/UX notes, colour para`
- [ ] `C-UX-18` `ui` The border colour is a near-white neutral darker than the tinted ground. `src: UI/UX notes, colour para`
- [ ] `C-UX-19` `ui` The failure panel is the only pink surface. `src: UI/UX notes, colour para`
- [ ] `C-UX-20` `ui` The pointer ring wears a mid neutral grey of its own. `src: UI/UX notes, colour para`
- [ ] `C-UX-21` `constraint` The site carries no brand accent hue. `src: UI/UX notes, colour para`
- [ ] `C-UX-22` `ui` The case study index drops from white into its dark band with no transition band. `src: UI/UX notes, grounds para`
- [ ] `C-UX-23` `ui` Sections separate by a ground change rather than a drawn line. `src: UI/UX notes, grounds para`
- [ ] `C-UX-24` `constraint` Nothing on the site casts a soft drop shadow. `src: UI/UX notes, depth para`
- [ ] `C-UX-25` `ui` Exactly one hard two-tone diagonal sits behind the services hero. `src: UI/UX notes, depth para`
- [ ] `C-UX-26` `constraint` No grain or noise overlay appears anywhere. `src: UI/UX notes, depth para`
- [ ] `C-UX-27` `ui` Content snaps to three recurring vertical lines on a wide screen. `src: UI/UX notes, column para`
- [ ] `C-UX-28` `ui` The journey section alone starts at the container edge. `src: UI/UX notes, column para`
- [ ] `C-UX-29` `ui` Container side padding halves on a tablet, halving again on a phone. `src: UI/UX notes, column para`
- [ ] `C-UX-30` `ui` Corners stay nearly square, with softer corners on gallery images. `src: UI/UX notes, shape para`
- [ ] `C-UX-31` `ui` The tablet mockup nests a rounder screen inside a frame. `src: UI/UX notes, shape para`
- [ ] `C-UX-32` `ui` Client marks, partner marks, award badges appear drained of colour at low strength. `src: UI/UX notes, imagery para`
- [ ] `C-UX-33` `ui` Team portraits appear drained of saturation. `src: UI/UX notes, imagery para`
- [ ] `C-UX-34` `ui` The sculptures show flat faces with a hard edge between faces. `src: UI/UX notes, imagery para`
- [ ] `C-UX-35` `ui` A text link grows a painted rule from zero width to full width as the text brightens. `src: UI/UX notes, links para`
- [ ] `C-UX-36` `ui` The header Contact button empties its fill rather than changing colour. `src: UI/UX notes, links para`
- [ ] `C-UX-37` `ui` The header Contact label brightens before the fill has drained. `src: UI/UX notes, links para`
- [ ] `C-UX-38` `ui` An arrow leaves along its own diagonal as a twin arrives from behind. `src: UI/UX notes, links para`
- [ ] `C-UX-39` `ui` The drawer trigger rules sweep out of a window as twins slide in. `src: UI/UX notes, links para`
- [ ] `C-UX-40` `ui` An unavailable control is never shown by colour alone. `src: UI/UX notes, links para`
- [ ] `C-UX-41` `ui` Scrolling back up runs every scroll-driven reveal backward. `src: UI/UX notes, motion para`
- [ ] `C-UX-42` `ui` Headings arrive one word at a time as the section comes up. `src: UI/UX notes, motion para`
- [ ] `C-UX-43` `ui` Larger blocks travel further than words when revealed. `src: UI/UX notes, motion para`
- [ ] `C-UX-44` `ui` A case study picture seems pushed outward by the opening window. `src: UI/UX notes, motion para`
- [ ] `C-UX-45` `ui` A custom cursor ring trails the pointer, turning slowly without stopping. `src: UI/UX notes, motion para`
- [ ] `C-UX-46` `ui` The footer is uncovered like lifting a sheet. `src: UI/UX notes, motion para`
- [ ] `C-UX-47` `constraint` No blanket transition applies to every element. `src: UI/UX notes, motion para`
- [ ] `C-UX-48` `ui` Hover treatments apply only to pointers that can hover. `src: UI/UX notes, motion para`
- [ ] `C-UX-49` `ui` The about page, privacy page, terms page, error page stay still on scroll. `src: UI/UX notes, absence para`
- [ ] `C-UX-50` `ui` The studio pages carry no scroll-driven motion. `src: UI/UX notes, absence para`
- [ ] `C-UX-51` `ui` The layout holds at every viewport width with no horizontal scrolling. `src: UI/UX notes, responsive para`
- [ ] `C-UX-52` `ui` The index row reveal happens on a laptop only. `src: UI/UX notes, responsive para`
- [ ] `C-UX-53` `ui` Case study pictures fade without moving on a tablet. `src: UI/UX notes, responsive para`
- [ ] `C-UX-54` `ui` Case study pictures stay still on a phone. `src: UI/UX notes, responsive para`
- [ ] `C-UX-55` `ui` The culture objects form a two-column grid below laptop width. `src: UI/UX notes, responsive para`
- [ ] `C-UX-56` `ui` The hive motif keeps moving at every width. `src: UI/UX notes, responsive para`
- [ ] `C-UX-57` `ui` Below the phone breakpoint the drawer is the only navigation. `src: UI/UX notes, responsive para`
- [ ] `C-UX-58` `ui` Text meets WCAG 2.2 AA contrast of 4.5 to 1 against its actual background. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-59` `ui` Header links stay legible over the white band of the case study index. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-60` `ui` Split word fragments stay hidden from assistive technology. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-61` `ui` A reduced-motion preference renders split headings as plain text. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-62` `ui` Keyboard navigation reaches every control with a visible focus ring on all three grounds. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-63` `ui` A row with a decorative arrow is one focus target. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-64` `ui` Interactive targets meet the WCAG 2.2 minimum target size. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-65` `ui` Icon-only controls carry labels. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-66` `ui` Content images carry alternative text, with decorative images marked decorative. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-67` `ui` The cursor ring stays off without a fine pointer or under reduced motion. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-68` `ui` Reduced motion restores native scrolling with every effect in its final state. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-69` `ui` Entry states, enquiry states, active tabs carry a word beside the colour. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-70` `ui` The studio sidebar reads `Entries`, `New entry`, `Enquiries`, `Sign out`. `src: UI/UX notes, studio para`
- [ ] `C-UX-71` `ui` Studio cards sit at compact density with title, kind, slug, state chip. `src: UI/UX notes, studio para`
- [ ] `C-UX-72` `ui` The wizard keeps its step names visible. `src: UI/UX notes, studio para`
- [ ] `C-UX-73` `ui` Every panel that covers the page closes on Escape. `src: UI/UX notes, studio para`
- [ ] `C-UX-74` `ui` Unpublishing asks once through a control naming the entry. `src: UI/UX notes, studio para`
- [ ] `C-UX-75` `constraint` Third-party accent colours never render anywhere. `src: UI/UX notes, avoid para`
- [ ] `C-UX-76` `constraint` No glass blur appears on a public page. `src: UI/UX notes, avoid para`
- [ ] `C-UX-77` `ui` Hairlines separate only stacked rows of one kind. `src: UI/UX notes, avoid para`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every public route arrives complete in the server-rendered HTML. `src: Technical requirements para 1`
- [ ] `C-TR-02` `capability` The HTTP API lives under `/api` on the page origin. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` Persisted data lives in PostgreSQL reached through `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` Stored images live in MinIO reached through `STORAGE_ENDPOINT`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` `GET /api/health` answers `200` once ready. `src: Technical requirements para 1`
- [ ] `C-TR-06` `ui` The full-height index scene renders at viewport height rather than band height. `src: Technical requirements, scene para`
- [ ] `C-TR-07` `constraint` No page references a video, model, raster or icon file. `src: Technical requirements, asset para`
- [ ] `C-TR-08` `ui` The sculptures are composed from simple solids with flat faces. `src: Technical requirements, asset para`
- [ ] `C-TR-09` `ui` The arrow stroke thickens with the text beside the arrow. `src: Technical requirements, asset para`
- [ ] `C-TR-10` `ui` Scrolling stays smooth with both index scenes on screen. `src: Technical requirements, performance para`
- [ ] `C-TR-11` `ui` The site stays smooth with a many-screen case study document. `src: Technical requirements, performance para`
- [ ] `C-TR-12` `constraint` Exactly two typefaces download. `src: Technical requirements, fonts para`
- [ ] `C-TR-13` `constraint` No page loads a script, style, image or frame from another origin. `src: Technical requirements, third-party para`

## C-DM Data model

- [ ] `C-DM-01` `data` Table `app_user` carries the pinned account fields. `src: Data model, app_user para`
- [ ] `C-DM-02` `data` Table `service` holds exactly eight rows. `src: Data model, service para`
- [ ] `C-DM-03` `literal` The eight services are `Design thinking workshop`, `UX/UI design`, `Fractional CTO`, `Website development`, `Dedicated team`, `Software development`, `Branding design`, `Website design`. `src: Data model, service para`
- [ ] `C-DM-04` `data` Table `case_study` carries the pinned case study fields. `src: Data model, case_study para`
- [ ] `C-DM-05` `data` Table `case_study_service` pairs a case study with a service. `src: Data model, case_study para`
- [ ] `C-DM-06` `data` Tables `article_category`, `article` carry the pinned fields. `src: Data model, article para`
- [ ] `C-DM-07` `data` Table `media_asset` carries the pinned media fields. `src: Data model, media_asset para`
- [ ] `C-DM-08` `data` Table `enquiry` carries the pinned enquiry fields. `src: Data model, enquiry para`
- [ ] `C-DM-09` `data` Table `bot_check_token` records `issued_at` for each token. `src: Data model, enquiry para`
- [ ] `C-DM-10` `data` The content tables carry the pinned culture, testimonial, badge, logo, team, office fields. `src: Data model, content tables para`
- [ ] `C-DM-11` `data` Pages read office details from the `office` table. `src: Data model, content tables para`
- [ ] `C-DM-12` `data` Readability stays derived rather than stored in a column. `src: Data model, derived para`
- [ ] `C-DM-13` `data` A category entry count is computed on read from published articles. `src: Data model, derived para`
- [ ] `C-DM-14` `data` The next project is computed on read from index order. `src: Data model, derived para`
- [ ] `C-DM-15` `data` The sitemap is computed on read from published rows. `src: Data model, derived para`
- [ ] `C-DM-16` `literal` The categories are `Product design`, `Engineering`, `Studio life`. `src: Data model, seed para 1`
- [ ] `C-DM-17` `literal` The category slugs are `product-design`, `engineering`, `studio-life`. `src: Data model, seed para 1`
- [ ] `C-DM-18` `literal` The seeded case study `Lumen Pay` holds the slug `lumen-pay`. `src: Data model, seed table row 1`
- [ ] `C-DM-19` `literal` The seeded case studies carry the names, labels, titles, years in the seed table. `src: Data model, seed table`
- [ ] `C-DM-20` `literal` The seeded case study `Lumen Pay` lists `UX/UI design`, `Software development`, `Branding design`. `src: Data model, seed table row 1`
- [ ] `C-DM-21` `literal` The draft case study `Nightjar` with slug `nightjar` belongs to `editor@example.com`. `src: Data model, seed para 2`
- [ ] `C-DM-22` `literal` The seeded draft case study carries one stored image. `src: Data model, seed para 2`
- [ ] `C-DM-23` `literal` The seeded articles carry the titles, slugs, categories, reading times, dates in the seed table. `src: Data model, article seed table`
- [ ] `C-DM-24` `literal` The draft article `Hiring a design partner in 2027` belongs to `editor2@example.com`. `src: Data model, seed para 3`
- [ ] `C-DM-25` `literal` The seven culture values carry the titles `Lift-off ready`, `Technomagicians`, `Aim for the point`, `Go wow or go home`, `Win-Win partnership`, `Bonding together`, `Keep the fire`. `src: Data model, seed para 4`
- [ ] `C-DM-26` `literal` The testimonials name `Mara Lindqvist`, `Tomas Reyes`, `Priya Anand`. `src: Data model, seed para 5`
- [ ] `C-DM-27` `literal` The award badges read `Pixel Guild Site of the Day`, `Studio Honors Gold`, `Product Craft Award`, `Design Circle Pick`, `Web Makers Top Studio`. `src: Data model, seed para 6`
- [ ] `C-DM-28` `literal` The team lists `Hana Ito`, `Marco Silva`, `Ruth Okafor`, `Dev Patel`, `Ingrid Moe`, `Sam Carter`. `src: Data model, seed para 6`
- [ ] `C-DM-29` `literal` The offices are `First Office` at `85 Example St, District 4,` beside `Second Office` at `60 Example Pl, Example NSW 2000`. `src: Data model, seed para 6`
- [ ] `C-DM-30` `literal` The seeded anonymous enquiry comes from `ada.quinn@example.com`. `src: Data model, seed para 7`
- [ ] `C-DM-31` `literal` The seeded client enquiry asks for `UX/UI design` at `$30k - $60k`. `src: Data model, seed para 7`
- [ ] `C-DM-32` `literal` The enquiries page of the seeded client lists that client enquiry with the state `new`. `src: Data model, seed para 7`
- [ ] `C-DM-33` `literal` The seeded anonymous enquiry holds the state `in_conversation`. `src: Data model, seed para 7`
- [ ] `C-DM-34` `literal` The seeded anonymous enquiry message reads `We want a faster marketing site with a case study library.` `src: Data model, seed para 7`
- [ ] `C-DM-35` `literal` The first office telephone is `+1 555 0100`. `src: Data model, seed para 6`
- [ ] `C-DM-36` `literal` The Lumen Pay subtitle opens `Fintech product, designed`. `src: Data model, seed para 2`
- [ ] `C-DM-37` `literal` The Lumen Pay site address is `https://lumen-pay.example.com`. `src: Data model, seed para 2`
- [ ] `C-DM-38` `literal` The seeded draft image carries the alternative text `Nightjar concept board`. `src: Data model, seed para 3`
- [ ] `C-DM-39` `capability` The home strip carries five client marks, the partner strip seven. `src: Data model, seed para 6`
- [ ] `C-DM-40` `constraint` Restarting the app duplicates no seeded row. `src: Data model, seed para 8`
- [ ] `C-DM-41` `literal` The seeded password appears in `/app/USER_README.md` beside each account. `src: Data model para 1`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The loader counter climbs to one hundred as the track fills. `src: Front-end specification, loader para`
- [ ] `C-FE-02` `ui` The loader panel leaves upward once complete. `src: Front-end specification, loader para`
- [ ] `C-FE-03` `ui` The loader returns briefly on a route change. `src: Front-end specification, loader para`
- [ ] `C-FE-04` `ui` The header scrolls away with the page. `src: Front-end specification, header para`
- [ ] `C-FE-05` `ui` The drawer trigger inverts against whatever passes behind the trigger. `src: Front-end specification, drawer para 1`
- [ ] `C-FE-06` `ui` The drawer slides in from the right as a two-column panel. `src: Front-end specification, drawer para 2`
- [ ] `C-FE-07` `ui` Drawer links arrive one after another. `src: Front-end specification, drawer para 2`
- [ ] `C-FE-08` `ui` Escape or an outside press closes the drawer with focus back on the trigger. `src: Front-end specification, drawer para 2`
- [ ] `C-FE-09` `ui` The oversized footer link is the largest interactive target on the site. `src: Front-end specification, footer para`
- [ ] `C-FE-10` `ui` Every mark is inline geometry inheriting the surrounding colour. `src: Front-end specification, iconography para`
- [ ] `C-FE-11` `ui` The send control's inner ring fills around the circle during sending. `src: Front-end specification, iconography para`
- [ ] `C-FE-12` `ui` The home wordmark reads as a watermark a shade lighter than the dark ground. `src: Front-end specification, home para 2`
- [ ] `C-FE-13` `ui` The live badger sculpture overlaps the wordmark, hanging off the left edge. `src: Front-end specification, home para 2`
- [ ] `C-FE-14` `ui` The sculpture grows, shifts right, then leaves the frame as the page scrolls. `src: Front-end specification, home para 2`
- [ ] `C-FE-15` `ui` The sculpture stays pinned after the ground beneath has turned dark. `src: Front-end specification, home para 2`
- [ ] `C-FE-16` `literal` The home intro heading opens `Award-winning digital agency specializing in design`. `src: Front-end specification, home para 3`
- [ ] `C-FE-17` `literal` The home intro link reads `See our services`. `src: Front-end specification, home para 3`
- [ ] `C-FE-18` `literal` The process words run `Empathize`, `Define`, `Ideate`, `Prototype`, a fifth word, then `Repeat`. `src: Front-end specification, home para 4`
- [ ] `C-FE-19` `ui` The process words stack one per line, centred, each arriving on scroll. `src: Front-end specification, home para 4`
- [ ] `C-FE-20` `literal` The process link reads `See our work`. `src: Front-end specification, home para 4`
- [ ] `C-FE-21` `ui` The culture objects float in a composed scatter over the ghosted logo watermark. `src: Front-end specification, home para 5`
- [ ] `C-FE-22` `ui` Each culture object rotates, bobbing out of step with the other objects. `src: Front-end specification, home para 5`
- [ ] `C-FE-23` `ui` Each culture object casts a soft contact shadow on the white ground. `src: Front-end specification, home para 5`
- [ ] `C-FE-24` `literal` The client strip heading reads `We've been doing brilliant work with brilliant brands`. `src: Front-end specification, home para 6`
- [ ] `C-FE-25` `ui` Client tiles arrive one after another. `src: Front-end specification, home para 6`
- [ ] `C-FE-26` `literal` The testimonial heading reads `What our clients talk about us`. `src: Front-end specification, home para 7`
- [ ] `C-FE-27` `ui` Each testimonial is a two-column entry, attribution beside quote. `src: Front-end specification, home para 7`
- [ ] `C-FE-28` `literal` The services hero sentence names the `hive` of creativity. `src: Front-end specification, services para 1`
- [ ] `C-FE-29` `ui` The services hero sits a step smaller than other heroes. `src: Front-end specification, services para 1`
- [ ] `C-FE-30` `ui` The hive hangs across the dark-to-light boundary, mirrored horizontally. `src: Front-end specification, services para 2`
- [ ] `C-FE-31` `ui` The hive sways, the bees bob on a loop half as long, one bee in opposite phase. `src: Front-end specification, services para 2`
- [ ] `C-FE-32` `ui` Scroll movement adds to the motif loops rather than replacing them. `src: Front-end specification, services para 2`
- [ ] `C-FE-33` `literal` The service list carries the label `Agency Services`. `src: Front-end specification, services para 3`
- [ ] `C-FE-34` `literal` The service rows name `MVP`, `UX/UI design`, `Website development`, `Software development`, `Branding design`, `Dedicated team`, `Fractional CTO`. `src: Front-end specification, services para 3`
- [ ] `C-FE-35` `literal` The working section reads `How we work with you` over `Discover`, `Design`, `Deliver`. `src: Front-end specification, services para 4`
- [ ] `C-FE-36` `literal` The team promise reads `A team that ships alongside yours`. `src: Front-end specification, services para 5`
- [ ] `C-FE-37` `literal` The index hero reads `We build`, `award-winning products`, `that everyone loves.`. `src: Front-end specification, index para 1`
- [ ] `C-FE-38` `ui` A slow lit background scene moves behind every index row. `src: Front-end specification, index para 2`
- [ ] `C-FE-39` `ui` Each index row reveals label, title, tags, arrow in order. `src: Front-end specification, index para 2`
- [ ] `C-FE-40` `ui` The live preview replaces a row picture under the pointer at the same size. `src: Front-end specification, index para 2`
- [ ] `C-FE-41` `ui` The case study hero centres the client name in the display face. `src: Front-end specification, case study para 1`
- [ ] `C-FE-42` `ui` The fact sheet sits against both margins with an empty middle. `src: Front-end specification, case study para 2`
- [ ] `C-FE-43` `ui` Case study media blocks recur at three widths, one bleeding off both edges. `src: Front-end specification, case study para 3`
- [ ] `C-FE-44` `ui` A picture sits across the line where the document ground changes. `src: Front-end specification, case study para 3`
- [ ] `C-FE-45` `ui` Case study images drift at different rates in a parallax on a laptop. `src: Front-end specification, case study para 3`
- [ ] `C-FE-46` `ui` The next-project section fills one viewport, darkened toward the foot. `src: Front-end specification, case study para 4`
- [ ] `C-FE-47` `literal` The about page carries the hidden heading `About Iron Wood`. `src: Front-end specification, about para 1`
- [ ] `C-FE-48` `ui` The about hero shows the seated still with no headline over the still. `src: Front-end specification, about para 1`
- [ ] `C-FE-49` `literal` The journey section carries `Our journey` above the partner label `Trusted by product teams at`. `src: Front-end specification, about para 2`
- [ ] `C-FE-50` `ui` The team grid runs three columns with drained portraits. `src: Front-end specification, about para 3`
- [ ] `C-FE-51` `literal` The team heading reads `The people behind the work`. `src: Front-end specification, about para 3`
- [ ] `C-FE-52` `literal` The office heading reads `Two offices, one studio`. `src: Front-end specification, about para 4`
- [ ] `C-FE-53` `ui` The archive hero is the shortest hero on the site. `src: Front-end specification, archive para 1`
- [ ] `C-FE-54` `ui` The current tab underline grows in as the page scrolls. `src: Front-end specification, archive para 2`
- [ ] `C-FE-55` `ui` Archive rows separate the date from the reading time with a tiny round dot. `src: Front-end specification, archive para 3`
- [ ] `C-FE-56` `ui` The More control is a single centred square button. `src: Front-end specification, archive para 3`
- [ ] `C-FE-57` `ui` The article hero window, picture move at two rates as the window fades. `src: Front-end specification, article para 1`
- [ ] `C-FE-58` `ui` The reading progress bar sits pinned below the hero, filling horizontally. `src: Front-end specification, article para 1`
- [ ] `C-FE-59` `ui` The article sidebar stays beside the reader for the whole body. `src: Front-end specification, article para 2`
- [ ] `C-FE-60` `literal` The article sidebar carries `Contents`. `src: Front-end specification, article para 2`
- [ ] `C-FE-61` `literal` The related section reads `Related articles`. `src: Front-end specification, article para 2`
- [ ] `C-FE-62` `literal` The contact hero reads `Be our client. Get that buzz`. `src: Front-end specification, contact para 1`
- [ ] `C-FE-63` `literal` The contact information column labels read `Email`, `Careers`, `Follow us`. `src: Front-end specification, contact para 2`
- [ ] `C-FE-64` `ui` Form fields show a rule beneath the value with no box. `src: Front-end specification, contact para 3`
- [ ] `C-FE-65` `ui` The form rows pair Service with Budget, Name with Email, then Message full width. `src: Front-end specification, contact para 3`
- [ ] `C-FE-66` `literal` The send control carries the accessible name `Send enquiry`. `src: Front-end specification, contact para 3`
- [ ] `C-FE-67` `ui` The failure panel is a pale soft red surface. `src: Front-end specification, contact para 3`
- [ ] `C-FE-68` `literal` The legal pages carry the headings `Privacy Policy`, `Terms of Service`. `src: Front-end specification, legal para`
- [ ] `C-FE-69` `ui` The legal pages set one centred text column. `src: Front-end specification, legal para`
- [ ] `C-FE-70` `ui` The not-found page composition centres on a light-to-dark seam under the rock still. `src: Front-end specification, error para`
- [ ] `C-FE-71` `ui` The sculptures move between their three known poses within the stated motion characters. `src: Front-end specification, motion authored para`
- [ ] `C-FE-72` `ui` The sign-in form places each field error directly beneath the field. `src: Front-end specification, sign-in para`
- [ ] `C-FE-73` `ui` The account page lists enquiries with a state chip carrying a word. `src: Front-end specification, sign-in para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The site serves one studio with one set of editors. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` The app takes no payment of any kind. `src: Constraints para 2`
- [ ] `C-CN-03` `constraint` The app sends no email of any kind. `src: Constraints para 3`
- [ ] `C-CN-04` `constraint` The app offers no newsletter. `src: Constraints para 2`
- [ ] `C-CN-05` `constraint` The app offers no site search. `src: Constraints para 2`
- [ ] `C-CN-06` `constraint` The app offers no filtering beyond the category tabs. `src: Constraints para 2`
- [ ] `C-CN-07` `constraint` The app offers no language switch. `src: Constraints para 2`
- [ ] `C-CN-08` `constraint` The app offers no dark-mode toggle. `src: Constraints para 2`
- [ ] `C-CN-09` `constraint` The app offers no comments or reactions. `src: Constraints para 2`
- [ ] `C-CN-10` `constraint` The app offers no careers application flow. `src: Constraints para 2`
- [ ] `C-CN-11` `constraint` Enquiries carry no file attachments. `src: Constraints para 2`
- [ ] `C-CN-12` `constraint` The app builds none of the client products the case studies describe. `src: Constraints para 2`
- [ ] `C-CN-13` `constraint` The app makes no outbound network call at run time. `src: Constraints para 3`
- [ ] `C-CN-14` `constraint` Every client, partner or award mark is a generated setting of an invented name. `src: Constraints para 4`
- [ ] `C-CN-15` `constraint` Every person named on the site is invented. `src: Constraints para 4`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping follows `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Reserved directories `.browser_screenshots/`, `.downloads/` both exist empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` The app serves a production build, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-11` `contract` The app uses the already-running backing services. `src: Deployment contract bullet 10`
- [ ] `C-DC-12` `literal` The API serves `POST /api/auth/login`. `src: Deployment contract, API shapes row 2`
- [ ] `C-DC-13` `literal` The API serves `GET /api/services`. `src: Deployment contract, API shapes row 3`
- [ ] `C-DC-14` `literal` The API serves `GET /api/case-studies`. `src: Deployment contract, API shapes row 4`
- [ ] `C-DC-15` `literal` The API serves `GET /api/case-studies/{slug}`. `src: Deployment contract, API shapes row 5`
- [ ] `C-DC-16` `literal` The API serves `POST /api/case-studies`. `src: Deployment contract, API shapes row 6`
- [ ] `C-DC-17` `literal` The API serves `PATCH /api/case-studies/{id}`. `src: Deployment contract, API shapes row 7`
- [ ] `C-DC-18` `literal` The API serves `POST /api/case-studies/{id}/publish`. `src: Deployment contract, API shapes row 8`
- [ ] `C-DC-19` `literal` The API serves `POST /api/case-studies/{id}/unpublish`. `src: Deployment contract, API shapes row 9`
- [ ] `C-DC-20` `literal` The API serves `POST /api/case-studies/{id}/media`. `src: Deployment contract, API shapes row 10`
- [ ] `C-DC-21` `literal` The API serves `GET /api/articles`. `src: Deployment contract, API shapes row 11`
- [ ] `C-DC-22` `literal` The API serves `GET /api/articles/{slug}`. `src: Deployment contract, API shapes row 12`
- [ ] `C-DC-23` `literal` The API serves `POST /api/articles`. `src: Deployment contract, API shapes row 13`
- [ ] `C-DC-24` `literal` The API serves `PATCH /api/articles/{id}`. `src: Deployment contract, API shapes row 14`
- [ ] `C-DC-25` `literal` The API serves `POST /api/articles/{id}/publish`. `src: Deployment contract, API shapes row 15`
- [ ] `C-DC-26` `literal` The API serves `POST /api/articles/{id}/unpublish`. `src: Deployment contract, API shapes row 16`
- [ ] `C-DC-27` `literal` The API serves `POST /api/articles/{id}/media`. `src: Deployment contract, API shapes row 17`
- [ ] `C-DC-28` `literal` The API serves `GET /api/article-categories`. `src: Deployment contract, API shapes row 18`
- [ ] `C-DC-29` `literal` The API serves `POST /api/enquiries`. `src: Deployment contract, API shapes row 19`
- [ ] `C-DC-30` `literal` The API serves `GET /api/enquiries`. `src: Deployment contract, API shapes row 20`
- [ ] `C-DC-31` `literal` `GET /api/case-studies` with `state=draft` returns only the caller's own drafts. `src: Deployment contract, API shapes row 4`
- [ ] `C-DC-32` `literal` `POST /api/case-studies` takes `services` as a list of service names. `src: Deployment contract, API shapes row 6`
- [ ] `C-DC-33` `literal` A media upload sends the file as `file` beside `alt_text`. `src: Deployment contract, API shapes row 10`
- [ ] `C-DC-34` `literal` `GET /api/articles` filters by `category` over pages counted by `page`. `src: Deployment contract, API shapes row 11`
- [ ] `C-DC-35` `literal` `POST /api/articles` takes `category` as a category slug with `read_minutes`. `src: Deployment contract, API shapes row 13`
- [ ] `C-DC-36` `literal` A sign-up response returns `access_token` with `user` fields `id`, `email`, `role`, `display_name`. `src: Deployment contract, API shapes row 1`
- [ ] `C-DC-37` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes para`
- [ ] `C-DC-38` `contract` An invalid call is rejected as a client error. `src: Deployment contract, API shapes para`
- [ ] `C-DC-39` `contract` Bearer auth guards every write. `src: Deployment contract, API shapes para`
- [ ] `C-DC-40` `contract` Public reads, the bot check, login, sign-up, health answer without a token. `src: Deployment contract, API shapes para`
- [ ] `C-DC-41` `data` A case study record carries the pinned fields, with `services` as service names. `src: Deployment contract, record para`
- [ ] `C-DC-42` `data` An article record carries `category` with `slug` beside `name`. `src: Deployment contract, record para`
- [ ] `C-DC-43` `data` An enquiry record carries the pinned enquiry fields. `src: Deployment contract, record para`
- [ ] `C-DC-44` `data` A category entry carries `slug`, `name`, `entry_count`. `src: Deployment contract, API shapes row 19`
- [ ] `C-DC-45` `data` The service list returns each service `name`. `src: Deployment contract, API shapes row 3`
- [ ] `C-DC-46` `constraint` No in-memory list stands in for the entry tables. `src: Deployment contract, No mocks para`
- [ ] `C-DC-47` `constraint` An enquiry is acknowledged only with a stored row. `src: Deployment contract, No mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `editor@example.com` | pinned by the brief at the citation beside it | C-RL-30 | User roles, seeded accounts table row 1 |
| `editor` | pinned by the brief at the citation beside it | C-RL-30 | User roles, seeded accounts table row 1 |
| `editor2@example.com` | pinned by the brief at the citation beside it | C-RL-31 | User roles, seeded accounts table row 2 |
| `client@example.com` | pinned by the brief at the citation beside it | C-RL-32 | User roles, seeded accounts table row 3 |
| `client` | pinned by the brief at the citation beside it | C-RL-32 | User roles, seeded accounts table row 3 |
| `Nadia Brooks` | pinned by the brief at the citation beside it | C-RL-33 | User roles, seeded accounts table row 1 |
| `Owen Pike` | pinned by the brief at the citation beside it | C-RL-34 | User roles, seeded accounts table row 2 |
| `Leo Marsh` | pinned by the brief at the citation beside it | C-RL-35 | User roles, seeded accounts table row 3 |
| `deku-demo-pw-2026` | pinned by the brief at the citation beside it | C-CF-01 | Core features, Auth para 1 |
| `POST /api/auth/login` | pinned by the brief at the citation beside it | C-CF-03 | Core features, Auth para 1 |
| `access_token` | pinned by the brief at the citation beside it | C-CF-03 | Core features, Auth para 1 |
| `POST /api/auth/sign-up` | pinned by the brief at the citation beside it | C-CF-07 | Core features, Auth para 2 |
| `email` | pinned by the brief at the citation beside it | C-CF-07 | Core features, Auth para 2 |
| `password` | pinned by the brief at the citation beside it | C-CF-07 | Core features, Auth para 2 |
| `display_name` | pinned by the brief at the citation beside it | C-CF-07 | Core features, Auth para 2 |
| `state` | pinned by the brief at the citation beside it | C-CF-14 | Core features, publication para 1 |
| `draft` | pinned by the brief at the citation beside it | C-CF-14 | Core features, publication para 1 |
| `published` | pinned by the brief at the citation beside it | C-CF-14 | Core features, publication para 1 |
| `STORAGE_BUCKET` | pinned by the brief at the citation beside it | C-CF-56 | Core features, images para 1 |
| `media/{kind}/{entry_id}/{sha256_of_bytes}.{ext}` | pinned by the brief at the citation beside it | C-CF-57 | Core features rule 8 |
| `kind` | pinned by the brief at the citation beside it | C-CF-58 | Core features rule 8 |
| `case-study` | pinned by the brief at the citation beside it | C-CF-58 | Core features rule 8 |
| `article` | pinned by the brief at the citation beside it | C-CF-58 | Core features rule 8 |
| `image/png` | pinned by the brief at the citation beside it | C-CF-62 | Core features rule 9 |
| `image/jpeg` | pinned by the brief at the citation beside it | C-CF-62 | Core features rule 9 |
| `image/webp` | pinned by the brief at the citation beside it | C-CF-62 | Core features rule 9 |
| `5 MB` | pinned by the brief at the citation beside it | C-CF-63 | Core features rule 9 |
| `GET /api/media/{asset_id}/content` | pinned by the brief at the citation beside it | C-CF-65 | Core features rule 10 |
| `data-case-study-row` | pinned by the brief at the citation beside it | C-CF-79 | Core features rule 14 |
| `data-slug` | pinned by the brief at the citation beside it | C-CF-80 | Core features rule 14 |
| `data-image-side` | pinned by the brief at the citation beside it | C-CF-81 | Core features rule 14 |
| `right` | pinned by the brief at the citation beside it | C-CF-81 | Core features rule 14 |
| `left` | pinned by the brief at the citation beside it | C-CF-81 | Core features rule 14 |
| `Visit site` | pinned by the brief at the citation beside it | C-CF-85 | Core features rule 16 |
| `Industry` | pinned by the brief at the citation beside it | C-CF-86 | Core features rule 16 |
| `Year` | pinned by the brief at the citation beside it | C-CF-87 | Core features rule 16 |
| `Next project` | pinned by the brief at the citation beside it | C-CF-89 | Core features rule 16 |
| `data-article-row` | pinned by the brief at the citation beside it | C-CF-93 | Core features rule 17 |
| `7 min read` | pinned by the brief at the citation beside it | C-CF-95 | Core features rule 17 |
| `More` | pinned by the brief at the citation beside it | C-CF-97 | Core features rule 18 |
| `data-pagination="next"` | pinned by the brief at the citation beside it | C-CF-98 | Core features rule 18 |
| `?page=2` | pinned by the brief at the citation beside it | C-CF-99 | Core features rule 18 |
| `All` | pinned by the brief at the citation beside it | C-CF-103 | Core features rule 19 |
| `Product design` | pinned by the brief at the citation beside it | C-CF-103 | Core features rule 19 |
| `Engineering` | pinned by the brief at the citation beside it | C-CF-103 | Core features rule 19 |
| `Studio life` | pinned by the brief at the citation beside it | C-CF-103 | Core features rule 19 |
| `data-count` | pinned by the brief at the citation beside it | C-CF-105 | Core features rule 19 |
| `aria-current="page"` | pinned by the brief at the citation beside it | C-CF-106 | Core features rule 19 |
| `data-reading-progress` | pinned by the brief at the citation beside it | C-CF-111 | Core features rule 21 |
| `data-enquiry-form` | pinned by the brief at the citation beside it | C-CF-116 | Core features rule 22 |
| `Service` | pinned by the brief at the citation beside it | C-CF-117 | Core features rule 22 |
| `Budget` | pinned by the brief at the citation beside it | C-CF-117 | Core features rule 22 |
| `Name` | pinned by the brief at the citation beside it | C-CF-117 | Core features rule 22 |
| `Email` | pinned by the brief at the citation beside it | C-CF-117 | Core features rule 22 |
| `Message` | pinned by the brief at the citation beside it | C-CF-117 | Core features rule 22 |
| `bpGCap` | pinned by the brief at the citation beside it | C-CF-118 | Core features rule 22 |
| `Website` | pinned by the brief at the citation beside it | C-CF-119 | Core features rule 22 |
| `Under $10k` | pinned by the brief at the citation beside it | C-CF-121 | Core features rule 23 |
| `$10k - $30k` | pinned by the brief at the citation beside it | C-CF-121 | Core features rule 23 |
| `$30k - $60k` | pinned by the brief at the citation beside it | C-CF-121 | Core features rule 23 |
| `$60k - $100k` | pinned by the brief at the citation beside it | C-CF-121 | Core features rule 23 |
| `Over $100k` | pinned by the brief at the citation beside it | C-CF-121 | Core features rule 23 |
| `GET /api/bot-check` | pinned by the brief at the citation beside it | C-CF-129 | Core features rule 25 |
| `token` | pinned by the brief at the citation beside it | C-CF-129 | Core features rule 25 |
| `ten minutes` | pinned by the brief at the citation beside it | C-CF-131 | Core features rule 25 |
| `sixty seconds` | pinned by the brief at the citation beside it | C-CF-136 | Core features rule 26 |
| `new` | pinned by the brief at the citation beside it | C-CF-138 | Core features rule 27 |
| `data-form-result="success"` | pinned by the brief at the citation beside it | C-CF-141 | Core features rule 27 |
| `Thank you. Your enquiry is with us.` | pinned by the brief at the citation beside it | C-CF-142 | Core features rule 27 |
| `We read every message` | pinned by the brief at the citation beside it | C-CF-143 | Core features rule 27 |
| `reply within two working days.` | pinned by the brief at the citation beside it | C-CF-143 | Core features rule 27 |
| `data-form-result="failure"` | pinned by the brief at the citation beside it | C-CF-144 | Core features rule 28 |
| `Something went wrong` | pinned by the brief at the citation beside it | C-CF-145 | Core features rule 28 |
| `Everything you typed is still here.` | pinned by the brief at the citation beside it | C-CF-145 | Core features rule 28 |
| `data-bot-check` | pinned by the brief at the citation beside it | C-CF-148 | Core features rule 29 |
| `in_conversation` | pinned by the brief at the citation beside it | C-CF-150 | Core features rule 30 |
| `closed` | pinned by the brief at the citation beside it | C-CF-151 | Core features rule 30 |
| `PATCH /api/enquiries/{id}` | pinned by the brief at the citation beside it | C-CF-153 | Core features rule 30 |
| `GET /api/enquiries` | pinned by the brief at the citation beside it | C-CF-155 | Core features rule 31 |
| `/account/enquiries` | pinned by the brief at the citation beside it | C-CF-158 | Core features rule 31 |
| `data-enquiry-state` | pinned by the brief at the citation beside it | C-CF-159 | Core features rule 31 |
| `data-scene="mascot-hero"` | pinned by the brief at the citation beside it | C-CF-160 | Core features rule 32 |
| `data-scene="culture-object"` | pinned by the brief at the citation beside it | C-CF-161 | Core features rule 32 |
| `data-scene="works-field"` | pinned by the brief at the citation beside it | C-CF-162 | Core features rule 32 |
| `data-scene="works-preview"` | pinned by the brief at the citation beside it | C-CF-163 | Core features rule 32 |
| `data-object` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `rocket` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `wand` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `arrow` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `bomb` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `thumb` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `bond` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `flame` | pinned by the brief at the citation beside it | C-CF-166 | Core features rule 33 |
| `data-ground` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 36 |
| `dark` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 36 |
| `light` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 36 |
| `tinted` | pinned by the brief at the citation beside it | C-CF-177 | Core features rule 36 |
| `Services.` | pinned by the brief at the citation beside it | C-CF-183 | Core features rule 38 |
| `Works.` | pinned by the brief at the citation beside it | C-CF-183 | Core features rule 38 |
| `About.` | pinned by the brief at the citation beside it | C-CF-183 | Core features rule 38 |
| `Blog.` | pinned by the brief at the citation beside it | C-CF-183 | Core features rule 38 |
| `Contact` | pinned by the brief at the citation beside it | C-CF-183 | Core features rule 38 |
| `Home.` | pinned by the brief at the citation beside it | C-CF-184 | Core features rule 38 |
| `Hire us.` | pinned by the brief at the citation beside it | C-CF-184 | Core features rule 38 |
| `facebook` | pinned by the brief at the citation beside it | C-CF-185 | Core features rule 38 |
| `behance` | pinned by the brief at the citation beside it | C-CF-185 | Core features rule 38 |
| `instagram` | pinned by the brief at the citation beside it | C-CF-185 | Core features rule 38 |
| `dribbble` | pinned by the brief at the citation beside it | C-CF-185 | Core features rule 38 |
| `clutch` | pinned by the brief at the citation beside it | C-CF-185 | Core features rule 38 |
| `linkedin` | pinned by the brief at the citation beside it | C-CF-185 | Core features rule 38 |
| `awwwards` | pinned by the brief at the citation beside it | C-CF-185 | Core features rule 38 |
| `hello@example.com` | pinned by the brief at the citation beside it | C-CF-186 | Core features rule 38 |
| `hr@example.com` | pinned by the brief at the citation beside it | C-CF-187 | Core features rule 38 |
| `data-drawer` | pinned by the brief at the citation beside it | C-CF-190 | Core features rule 39 |
| `data-drawer-trigger` | pinned by the brief at the citation beside it | C-CF-191 | Core features rule 39 |
| `aria-expanded` | pinned by the brief at the citation beside it | C-CF-191 | Core features rule 39 |
| `Have a product in mind?` | pinned by the brief at the citation beside it | C-CF-193 | Core features rule 40 |
| `Let's build` | pinned by the brief at the citation beside it | C-CF-194 | Core features rule 40 |
| `© 2026 Iron Wood - UX UI Design Agency` | pinned by the brief at the citation beside it | C-CF-196 | Core features rule 40 |
| `Privacy Policy` | pinned by the brief at the citation beside it | C-CF-197 | Core features rule 40 |
| `/privacy-policy` | pinned by the brief at the citation beside it | C-CF-197 | Core features rule 40 |
| `Terms` | pinned by the brief at the citation beside it | C-CF-198 | Core features rule 40 |
| `/terms` | pinned by the brief at the citation beside it | C-CF-198 | Core features rule 40 |
| `data-office-switch` | pinned by the brief at the citation beside it | C-CF-200 | Core features rule 41 |
| `aria-pressed` | pinned by the brief at the citation beside it | C-CF-200 | Core features rule 41 |
| `data-office-image` | pinned by the brief at the citation beside it | C-CF-201 | Core features rule 41 |
| `data-active="true"` | pinned by the brief at the citation beside it | C-CF-201 | Core features rule 41 |
| `data-split-heading` | pinned by the brief at the citation beside it | C-CF-203 | Core features rule 42 |
| `aria-label` | pinned by the brief at the citation beside it | C-CF-203 | Core features rule 42 |
| `data-motif="hive"` | pinned by the brief at the citation beside it | C-CF-204 | Core features rule 43 |
| `data-motif-part="hive"` | pinned by the brief at the citation beside it | C-CF-205 | Core features rule 43 |
| `data-phase="reverse"` | pinned by the brief at the citation beside it | C-CF-206 | Core features rule 43 |
| `/sitemap.xml` | pinned by the brief at the citation beside it | C-CF-209 | Core features rule 45 |
| `/robots.txt` | pinned by the brief at the citation beside it | C-CF-211 | Core features rule 45 |
| `Sitemap:` | pinned by the brief at the citation beside it | C-CF-211 | Core features rule 45 |
| `og:title` | pinned by the brief at the citation beside it | C-CF-212 | Core features rule 46 |
| `og:image` | pinned by the brief at the citation beside it | C-CF-212 | Core features rule 46 |
| `/social-preview/{page_key}` | pinned by the brief at the citation beside it | C-CF-213 | Core features rule 46 |
| `home` | pinned by the brief at the citation beside it | C-CF-215 | Core features rule 46 |
| `By creating an account you agree to the Terms of Service.` | pinned by the brief at the citation beside it | C-CF-218 | Core features rule 47 |
| `Sorry! The page you're looking for was not found` | pinned by the brief at the citation beside it | C-CF-222 | Core features rule 49 |
| `404` | pinned by the brief at the citation beside it | C-CF-223 | Core features rule 49 |
| `Back to home` | pinned by the brief at the citation beside it | C-CF-224 | Core features rule 49 |
| `data-wizard-step` | pinned by the brief at the citation beside it | C-UF-34 | User flow, journeys para 3 |
| `details` | pinned by the brief at the citation beside it | C-UF-34 | User flow, journeys para 3 |
| `media` | pinned by the brief at the citation beside it | C-UF-34 | User flow, journeys para 3 |
| `review` | pinned by the brief at the citation beside it | C-UF-34 | User flow, journeys para 3 |
| `data-entry-state` | pinned by the brief at the citation beside it | C-UF-35 | User flow, journeys para 3 |
| `DATABASE_URL` | pinned by the brief at the citation beside it | C-TR-03 | Technical requirements para 1 |
| `STORAGE_ENDPOINT` | pinned by the brief at the citation beside it | C-TR-04 | Technical requirements para 1 |
| `GET /api/health` | pinned by the brief at the citation beside it | C-TR-05 | Technical requirements para 1 |
| `200` | pinned by the brief at the citation beside it | C-TR-05 | Technical requirements para 1 |
| `Design thinking workshop` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `UX/UI design` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `Fractional CTO` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `Website development` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `Dedicated team` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `Software development` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `Branding design` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `Website design` | pinned by the brief at the citation beside it | C-DM-03 | Data model, service para |
| `product-design` | pinned by the brief at the citation beside it | C-DM-17 | Data model, seed para 1 |
| `engineering` | pinned by the brief at the citation beside it | C-DM-17 | Data model, seed para 1 |
| `studio-life` | pinned by the brief at the citation beside it | C-DM-17 | Data model, seed para 1 |
| `Lumen Pay` | pinned by the brief at the citation beside it | C-DM-18 | Data model, seed table row 1 |
| `lumen-pay` | pinned by the brief at the citation beside it | C-DM-18 | Data model, seed table row 1 |
| `Nightjar` | pinned by the brief at the citation beside it | C-DM-21 | Data model, seed para 2 |
| `nightjar` | pinned by the brief at the citation beside it | C-DM-21 | Data model, seed para 2 |
| `Hiring a design partner in 2027` | pinned by the brief at the citation beside it | C-DM-24 | Data model, seed para 3 |
| `Lift-off ready` | pinned by the brief at the citation beside it | C-DM-25 | Data model, seed para 4 |
| `Technomagicians` | pinned by the brief at the citation beside it | C-DM-25 | Data model, seed para 4 |
| `Aim for the point` | pinned by the brief at the citation beside it | C-DM-25 | Data model, seed para 4 |
| `Go wow or go home` | pinned by the brief at the citation beside it | C-DM-25 | Data model, seed para 4 |
| `Win-Win partnership` | pinned by the brief at the citation beside it | C-DM-25 | Data model, seed para 4 |
| `Bonding together` | pinned by the brief at the citation beside it | C-DM-25 | Data model, seed para 4 |
| `Keep the fire` | pinned by the brief at the citation beside it | C-DM-25 | Data model, seed para 4 |
| `Mara Lindqvist` | pinned by the brief at the citation beside it | C-DM-26 | Data model, seed para 5 |
| `Tomas Reyes` | pinned by the brief at the citation beside it | C-DM-26 | Data model, seed para 5 |
| `Priya Anand` | pinned by the brief at the citation beside it | C-DM-26 | Data model, seed para 5 |
| `Pixel Guild Site of the Day` | pinned by the brief at the citation beside it | C-DM-27 | Data model, seed para 6 |
| `Studio Honors Gold` | pinned by the brief at the citation beside it | C-DM-27 | Data model, seed para 6 |
| `Product Craft Award` | pinned by the brief at the citation beside it | C-DM-27 | Data model, seed para 6 |
| `Design Circle Pick` | pinned by the brief at the citation beside it | C-DM-27 | Data model, seed para 6 |
| `Web Makers Top Studio` | pinned by the brief at the citation beside it | C-DM-27 | Data model, seed para 6 |
| `Hana Ito` | pinned by the brief at the citation beside it | C-DM-28 | Data model, seed para 6 |
| `Marco Silva` | pinned by the brief at the citation beside it | C-DM-28 | Data model, seed para 6 |
| `Ruth Okafor` | pinned by the brief at the citation beside it | C-DM-28 | Data model, seed para 6 |
| `Dev Patel` | pinned by the brief at the citation beside it | C-DM-28 | Data model, seed para 6 |
| `Ingrid Moe` | pinned by the brief at the citation beside it | C-DM-28 | Data model, seed para 6 |
| `Sam Carter` | pinned by the brief at the citation beside it | C-DM-28 | Data model, seed para 6 |
| `First Office` | pinned by the brief at the citation beside it | C-DM-29 | Data model, seed para 6 |
| `85 Example St, District 4,` | pinned by the brief at the citation beside it | C-DM-29 | Data model, seed para 6 |
| `Second Office` | pinned by the brief at the citation beside it | C-DM-29 | Data model, seed para 6 |
| `60 Example Pl, Example NSW 2000` | pinned by the brief at the citation beside it | C-DM-29 | Data model, seed para 6 |
| `ada.quinn@example.com` | pinned by the brief at the citation beside it | C-DM-30 | Data model, seed para 7 |
| `We want a faster marketing site with a case study library.` | pinned by the brief at the citation beside it | C-DM-34 | Data model, seed para 7 |
| `+1 555 0100` | pinned by the brief at the citation beside it | C-DM-35 | Data model, seed para 6 |
| `Fintech product, designed` | pinned by the brief at the citation beside it | C-DM-36 | Data model, seed para 2 |
| `https://lumen-pay.example.com` | pinned by the brief at the citation beside it | C-DM-37 | Data model, seed para 2 |
| `Nightjar concept board` | pinned by the brief at the citation beside it | C-DM-38 | Data model, seed para 3 |
| `/app/USER_README.md` | pinned by the brief at the citation beside it | C-DM-41 | Data model para 1 |
| `Award-winning digital agency specializing in design` | pinned by the brief at the citation beside it | C-FE-16 | Front-end specification, home para 3 |
| `See our services` | pinned by the brief at the citation beside it | C-FE-17 | Front-end specification, home para 3 |
| `Empathize` | pinned by the brief at the citation beside it | C-FE-18 | Front-end specification, home para 4 |
| `Define` | pinned by the brief at the citation beside it | C-FE-18 | Front-end specification, home para 4 |
| `Ideate` | pinned by the brief at the citation beside it | C-FE-18 | Front-end specification, home para 4 |
| `Prototype` | pinned by the brief at the citation beside it | C-FE-18 | Front-end specification, home para 4 |
| `Repeat` | pinned by the brief at the citation beside it | C-FE-18 | Front-end specification, home para 4 |
| `See our work` | pinned by the brief at the citation beside it | C-FE-20 | Front-end specification, home para 4 |
| `We've been doing brilliant work with brilliant brands` | pinned by the brief at the citation beside it | C-FE-24 | Front-end specification, home para 6 |
| `What our clients talk about us` | pinned by the brief at the citation beside it | C-FE-26 | Front-end specification, home para 7 |
| `hive` | pinned by the brief at the citation beside it | C-FE-28 | Front-end specification, services para 1 |
| `Agency Services` | pinned by the brief at the citation beside it | C-FE-33 | Front-end specification, services para 3 |
| `MVP` | pinned by the brief at the citation beside it | C-FE-34 | Front-end specification, services para 3 |
| `How we work with you` | pinned by the brief at the citation beside it | C-FE-35 | Front-end specification, services para 4 |
| `Discover` | pinned by the brief at the citation beside it | C-FE-35 | Front-end specification, services para 4 |
| `Design` | pinned by the brief at the citation beside it | C-FE-35 | Front-end specification, services para 4 |
| `Deliver` | pinned by the brief at the citation beside it | C-FE-35 | Front-end specification, services para 4 |
| `A team that ships alongside yours` | pinned by the brief at the citation beside it | C-FE-36 | Front-end specification, services para 5 |
| `We build` | pinned by the brief at the citation beside it | C-FE-37 | Front-end specification, index para 1 |
| `award-winning products` | pinned by the brief at the citation beside it | C-FE-37 | Front-end specification, index para 1 |
| `that everyone loves.` | pinned by the brief at the citation beside it | C-FE-37 | Front-end specification, index para 1 |
| `About Iron Wood` | pinned by the brief at the citation beside it | C-FE-47 | Front-end specification, about para 1 |
| `Our journey` | pinned by the brief at the citation beside it | C-FE-49 | Front-end specification, about para 2 |
| `Trusted by product teams at` | pinned by the brief at the citation beside it | C-FE-49 | Front-end specification, about para 2 |
| `The people behind the work` | pinned by the brief at the citation beside it | C-FE-51 | Front-end specification, about para 3 |
| `Two offices, one studio` | pinned by the brief at the citation beside it | C-FE-52 | Front-end specification, about para 4 |
| `Contents` | pinned by the brief at the citation beside it | C-FE-60 | Front-end specification, article para 2 |
| `Related articles` | pinned by the brief at the citation beside it | C-FE-61 | Front-end specification, article para 2 |
| `Be our client. Get that buzz` | pinned by the brief at the citation beside it | C-FE-62 | Front-end specification, contact para 1 |
| `Careers` | pinned by the brief at the citation beside it | C-FE-63 | Front-end specification, contact para 2 |
| `Follow us` | pinned by the brief at the citation beside it | C-FE-63 | Front-end specification, contact para 2 |
| `Send enquiry` | pinned by the brief at the citation beside it | C-FE-66 | Front-end specification, contact para 3 |
| `Terms of Service` | pinned by the brief at the citation beside it | C-FE-68 | Front-end specification, legal para |
| `GET /api/services` | pinned by the brief at the citation beside it | C-DC-13 | Deployment contract, API shapes row 3 |
| `GET /api/case-studies` | pinned by the brief at the citation beside it | C-DC-14 | Deployment contract, API shapes row 4 |
| `GET /api/case-studies/{slug}` | pinned by the brief at the citation beside it | C-DC-15 | Deployment contract, API shapes row 5 |
| `POST /api/case-studies` | pinned by the brief at the citation beside it | C-DC-16 | Deployment contract, API shapes row 6 |
| `PATCH /api/case-studies/{id}` | pinned by the brief at the citation beside it | C-DC-17 | Deployment contract, API shapes row 7 |
| `POST /api/case-studies/{id}/publish` | pinned by the brief at the citation beside it | C-DC-18 | Deployment contract, API shapes row 8 |
| `POST /api/case-studies/{id}/unpublish` | pinned by the brief at the citation beside it | C-DC-19 | Deployment contract, API shapes row 9 |
| `POST /api/case-studies/{id}/media` | pinned by the brief at the citation beside it | C-DC-20 | Deployment contract, API shapes row 10 |
| `GET /api/articles` | pinned by the brief at the citation beside it | C-DC-21 | Deployment contract, API shapes row 11 |
| `GET /api/articles/{slug}` | pinned by the brief at the citation beside it | C-DC-22 | Deployment contract, API shapes row 12 |
| `POST /api/articles` | pinned by the brief at the citation beside it | C-DC-23 | Deployment contract, API shapes row 13 |
| `PATCH /api/articles/{id}` | pinned by the brief at the citation beside it | C-DC-24 | Deployment contract, API shapes row 14 |
| `POST /api/articles/{id}/publish` | pinned by the brief at the citation beside it | C-DC-25 | Deployment contract, API shapes row 15 |
| `POST /api/articles/{id}/unpublish` | pinned by the brief at the citation beside it | C-DC-26 | Deployment contract, API shapes row 16 |
| `POST /api/articles/{id}/media` | pinned by the brief at the citation beside it | C-DC-27 | Deployment contract, API shapes row 17 |
| `GET /api/article-categories` | pinned by the brief at the citation beside it | C-DC-28 | Deployment contract, API shapes row 18 |
| `POST /api/enquiries` | pinned by the brief at the citation beside it | C-DC-29 | Deployment contract, API shapes row 19 |
| `state=draft` | pinned by the brief at the citation beside it | C-DC-31 | Deployment contract, API shapes row 4 |
| `services` | pinned by the brief at the citation beside it | C-DC-32 | Deployment contract, API shapes row 6 |
| `file` | pinned by the brief at the citation beside it | C-DC-33 | Deployment contract, API shapes row 10 |
| `alt_text` | pinned by the brief at the citation beside it | C-DC-33 | Deployment contract, API shapes row 10 |
| `category` | pinned by the brief at the citation beside it | C-DC-34 | Deployment contract, API shapes row 11 |
| `page` | pinned by the brief at the citation beside it | C-DC-34 | Deployment contract, API shapes row 11 |
| `read_minutes` | pinned by the brief at the citation beside it | C-DC-35 | Deployment contract, API shapes row 13 |
| `user` | pinned by the brief at the citation beside it | C-DC-36 | Deployment contract, API shapes row 1 |
| `id` | pinned by the brief at the citation beside it | C-DC-36 | Deployment contract, API shapes row 1 |
| `role` | pinned by the brief at the citation beside it | C-DC-36 | Deployment contract, API shapes row 1 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact colour value behind every named colour role | C-UX-14 | carried as family, tone and shade rather than as a value |
| the exact type sizes of each heading and body step | C-UX-04 | carried as relationships to one base unit rather than as values |
| the telephone number of each office | C-DM-28 | named as present with no literal number given |
| the body text of each seeded case study and article | C-DM-18 | named as present with no literal text given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 8 |
| User roles | 3 | 35 |
| Core features | 21 | 227 |
| User flow | 7 | 43 |
| UI and UX notes | 13 | 77 |
| Technical requirements | 9 | 13 |
| Data model | 6 | 41 |
| Front-end specification | 7 | 73 |
| Constraints | 0 | 15 |
| Deployment contract | 11 | 47 |

`## Definition of done` produces no items. Every clause in it restates an ask already
carried by `## Core features`, and section 3.5 folds a restatement into the item it
restates rather than minting a second one.

Asks withdrawn because no channel can observe them, recorded rather than carried per
OPEN-DECISIONS D-H: the framework names Django and HTMX, the structured request log,
the absence of a second database or cache or queue, the bundling of browser code at
image build, the three separable layers, the single spacing scale for case study
blocks, the font swap behaviour and fallback stack, the persistence of the scroll
driver across a page swap as an internal mechanism, the per-frame callback for scenes,
the persistent volume and container name bans, the table count, and the empty studio grid
(every seeded editor owns entries, so that state cannot be reached).
