# Checklist: Quarto Structured Content Platform
Items: 246
Unpinned values flagged: 3
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `constraint` Every object inside an array carries a permanent name assigned at creation. `src: Overview`
- [ ] `C-OV-02` `data` Rich text is stored as structure rather than as markup. `src: Overview`
- [ ] `C-OV-03` `capability` A public marketing property plus an authenticated studio are served from one deployment. `src: Overview`
- [ ] `C-OV-04` `capability` The Content Store answers queries without depending on the editing application. `src: Overview`
- [ ] `C-OV-05` `data` A document stores named fields under a type rather than a rendered page. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `literal` Every seeded person signs in with the password `deku-demo-pw-2026`. `src: User roles seeded people`
- [ ] `C-RL-02` `role` A password other than the seeded one yields no bearer token. `src: User roles seeded people`
- [ ] `C-RL-03` `role` A contributor may not publish or unpublish a document. `src: User roles table`
- [ ] `C-RL-04` `role` A contributor may create a draft inside their own department. `src: User roles table`
- [ ] `C-RL-05` `role` A denied publish leaves the published state untouched. `src: User roles`
- [ ] `C-RL-06` `role` An editor may publish a document inside their own department. `src: User roles table`
- [ ] `C-RL-07` `role` An editor may not read the audit log. `src: User roles table`
- [ ] `C-RL-08` `role` An editor may not deploy a schema or run a migration. `src: User roles table`
- [ ] `C-RL-09` `role` An administrator alone may read the audit log. `src: User roles table`
- [ ] `C-RL-10` `role` An administrator may not patch or publish a document. `src: User roles table`
- [ ] `C-RL-11` `role` A document outside the caller's own department is answered as not found. `src: User roles`
- [ ] `C-RL-12` `role` A restricted document is absent from a query answer rather than hidden afterwards. `src: User roles`
- [ ] `C-RL-13` `literal` A write moving a document out of the writer's own grant is refused with the code `grant_escape_refused`. `src: User roles`
- [ ] `C-RL-14` `role` A viewer may not read a draft under any perspective. `src: User roles table`
- [ ] `C-RL-15` `role` A viewer reads published documents only. `src: User roles table`
- [ ] `C-RL-16` `role` A contributor may patch a draft inside their own department. `src: User roles table`

## C-CF Core features

- [ ] `C-CF-01` `contract` `POST /api/auth/login` returns an opaque bearer access token. `src: Core features rule 1`
- [ ] `C-CF-02` `contract` A wrong password is refused at login. `src: Core features rule 1`
- [ ] `C-CF-03` `contract` An address no seeded person holds is refused the same way a wrong password is refused. `src: Core features rule 1`
- [ ] `C-CF-04` `constraint` A refusal at login names no reason that would reveal which addresses exist. `src: Core features rule 1`
- [ ] `C-CF-05` `contract` `GET /api/me` reports the signed-in person with their role plus their department. `src: Core features rule 3`
- [ ] `C-CF-06` `role` A caller carrying no bearer token is denied at `GET /api/me`. `src: Core features rule 3`
- [ ] `C-CF-07` `capability` Role, department, grant are read from storage on every request rather than from the token. `src: Core features rule 2`
- [ ] `C-CF-08` `contract` `GET /api/datasets` returns each dataset with visibility, document count, asset count. `src: Core features rule 4`
- [ ] `C-CF-09` `data` A document carries `_id`, `_type`, `_rev`, `_createdAt`, `_updatedAt`. `src: Core features rule 7`
- [ ] `C-CF-10` `constraint` A client supplying `_rev`, `_createdAt` or `_updatedAt` on a write is refused. `src: Core features rule 7`
- [ ] `C-CF-11` `data` A document created with a five-item array comes back with five distinct keys. `src: Core features rule 9`
- [ ] `C-CF-12` `contract` `POST /api/data/mutate/{dataset}` accepts a client transaction identifier plus ordered mutations. `src: Core features rule 29`
- [ ] `C-CF-13` `constraint` Saving a document ten times leaves every array key unchanged. `src: Core features rule 9`
- [ ] `C-CF-14` `capability` An editing surface sends a patch rather than a whole-document replacement. `src: Core features rule 30`
- [ ] `C-CF-15` `capability` A patch naming an array item by key lands on that item after a concurrent head insert. `src: Core features rule 33`
- [ ] `C-CF-16` `data` A path addresses an array object through the key predicate form. `src: Core features rule 32`
- [ ] `C-CF-17` `literal` One hundred concurrent increments of one counter leave the counter at `100`. `src: Core features rule 31`
- [ ] `C-CF-18` `data` The patch operations are the closed list the brief names. `src: Core features rule 31`
- [ ] `C-CF-19` `literal` Replaying a transaction identifier inside `TRANSACTION_REPLAY_WINDOW_SEC` applies nothing. `src: Core features rule 37`
- [ ] `C-CF-20` `capability` A replayed transaction identifier returns the original result. `src: Core features rule 37`
- [ ] `C-CF-21` `literal` A revision mismatch is refused with the code `revision_mismatch`. `src: Core features rule 36`
- [ ] `C-CF-22` `constraint` A patch based on a superseded revision never overwrites the newer one. `src: Core features rule 36`
- [ ] `C-CF-23` `capability` A patch whose later operation is invalid applies none of its operations. `src: Core features rule 35`
- [ ] `C-CF-24` `capability` Patch operations apply in the order given. `src: Core features rule 35`
- [ ] `C-CF-25` `capability` Emboldening the middle of an unmarked span produces three spans. `src: Core features rule 16`
- [ ] `C-CF-26` `constraint` The first span resulting from a split keeps the original key. `src: Core features rule 16`
- [ ] `C-CF-27` `data` A span carries a key, text, a marks array. `src: Core features rule 11`
- [ ] `C-CF-28` `capability` Adjacent spans whose marks are equal as sets are merged. `src: Core features rule 17`
- [ ] `C-CF-29` `constraint` A merge keeps the earlier of the two span keys. `src: Core features rule 17`
- [ ] `C-CF-30` `capability` An orphaned `markDefs` entry is removed on the write that orphaned the entry. `src: Core features rule 14`
- [ ] `C-CF-31` `data` An annotation is stored in `markDefs` under a key referenced from `marks`. `src: Core features rule 12`
- [ ] `C-CF-32` `data` A decorator is stored as a literal string in `marks`. `src: Core features rule 12`
- [ ] `C-CF-33` `contract` Five consecutive bulleted blocks render as one list of five items. `src: Core features rule 19`
- [ ] `C-CF-34` `data` A list is a run of adjacent blocks sharing one list marker. `src: Core features rule 18`
- [ ] `C-CF-35` `constraint` Markup characters stored inside span text come back byte-identical. `src: Core features rule 21`
- [ ] `C-CF-36` `constraint` A renderer infers no structure that the stored data does not carry. `src: Core features rule 21`
- [ ] `C-CF-37` `data` The `drafts` perspective returns a document under the published identifier. `src: Core features rule 26`
- [ ] `C-CF-38` `data` The draft identity is the published identity prefixed with `drafts.`. `src: Core features rule 22`
- [ ] `C-CF-39` `data` The `raw` perspective exposes the stored draft under its prefixed identifier. `src: Core features rule 26`
- [ ] `C-CF-40` `contract` `GET /api/data/history/{dataset}/{id}` returns every revision of the document. `src: Core features rule 25`
- [ ] `C-CF-41` `constraint` Restoring a revision appends a new revision rather than rewinding the chain. `src: Core features rule 25`
- [ ] `C-CF-42` `data` A read reports one of the four publication states the brief names. `src: Core features rule 23`
- [ ] `C-CF-43` `data` The four seeded articles report four distinct publication states. `src: Core features rule 23`
- [ ] `C-CF-44` `capability` Unpublishing creates the draft plus removes the published document in one transaction. `src: Core features rule 24`
- [ ] `C-CF-45` `capability` Publishing writes the published document plus removes the draft in one transaction. `src: Core features rule 24`
- [ ] `C-CF-46` `contract` Publishing answers with the revision the publish produced. `src: Core features rule 25`
- [ ] `C-CF-47` `contract` `GET /api/data/listen/{dataset}` opens with a welcome event. `src: Core features rule 52`
- [ ] `C-CF-48` `data` A change event carries the previous revision, the resulting revision, the transaction identifier. `src: Core features rule 52`
- [ ] `C-CF-49` `contract` `POST /api/data/query/{dataset}` returns a result beside a cost record. `src: Core features rule 43`
- [ ] `C-CF-50` `data` A cost record carries the count of documents examined. `src: Core features rule 49`
- [ ] `C-CF-51` `data` The query language supports filter, order, slice, projection, dereference, rename. `src: Core features rule 43`
- [ ] `C-CF-52` `capability` A parameter carrying query syntax is treated as a literal string. `src: Core features rule 45`
- [ ] `C-CF-53` `constraint` A parameter value is never spliced into the query text. `src: Core features rule 45`
- [ ] `C-CF-54` `literal` A query exceeding a bound is refused with the code `query_bound_exceeded`. `src: Core features rule 51`
- [ ] `C-CF-55` `capability` A bound refusal names the predicate that made the query expensive. `src: Core features rule 51`
- [ ] `C-CF-56` `literal` The dereference depth bound is `5`. `src: Core features rule 51`
- [ ] `C-CF-57` `literal` A migration invoked without `apply` writes nothing. `src: Core features rule 81`
- [ ] `C-CF-58` `capability` A dry run reports the affected count plus a sample of before-and-after pairs. `src: Core features rule 81`
- [ ] `C-CF-59` `capability` Running one migration twice leaves the second run with nothing to change. `src: Core features rule 82`
- [ ] `C-CF-60` `capability` A migration resumes from a stored cursor. `src: Core features rule 82`
- [ ] `C-CF-61` `capability` A migration touching rich text keeps every surviving block key. `src: Core features rule 84`
- [ ] `C-CF-62` `capability` A migration touching rich text keeps every surviving span key. `src: Core features rule 84`
- [ ] `C-CF-63` `literal` A migration targeting `production` without the retyped name is refused with `production_confirmation_required`. `src: Core features rule 85`
- [ ] `C-CF-64` `constraint` The migration runner has no default dataset. `src: Core features rule 85`
- [ ] `C-CF-65` `capability` Switching a dataset to `public` requires the dataset name typed again. `src: Core features rule 88`
- [ ] `C-CF-66` `capability` The visibility confirmation states the count of documents becoming world-readable. `src: Core features rule 88`
- [ ] `C-CF-67` `capability` A release publishes every member document in one transaction. `src: Core features rule 101`
- [ ] `C-CF-68` `literal` A release above the transaction bound is refused at creation with `release_too_large`. `src: Core features rule 101`
- [ ] `C-CF-69` `capability` A word split across spans by a mark is indexed as one word. `src: Core features rule 103`
- [ ] `C-CF-70` `contract` `GET /api/search/{dataset}` answers an editor search over the dataset. `src: Core features rule 102`
- [ ] `C-CF-71` `literal` An unmatched path returns `404` under the title `Page not found`. `src: Core features rule 121`
- [ ] `C-CF-72` `constraint` No unmatched path renders the home page. `src: Core features rule 121`
- [ ] `C-CF-73` `capability` Every internal link on every public route resolves. `src: Core features rule 122`
- [ ] `C-CF-74` `contract` `GET /sitemap.xml` lists every public route. `src: Core features rule 124`
- [ ] `C-CF-75` `contract` `GET /robots.txt` names the sitemap by absolute address. `src: Core features rule 124`
- [ ] `C-CF-76` `capability` A recorded cookie decision survives a reload. `src: Core features rule 123`
- [ ] `C-CF-77` `capability` A lead form submitted repeatedly in quick succession is refused. `src: Core features rule 125`
- [ ] `C-CF-78` `capability` Search results are filtered against the caller's grants at query time. `src: Core features rule 106`
- [ ] `C-CF-79` `data` Editor search covers drafts; consumer search covers published documents only. `src: Core features rule 102`
- [ ] `C-CF-80` `contract` A read carrying no credentials defaults to the `published` perspective. `src: Core features rule 27`
- [ ] `C-CF-81` `constraint` A draft-only document is absent from an anonymous read. `src: Core features rule 27`
- [ ] `C-CF-82` `constraint` A draft-only article never appears on the blog index. `src: Core features rule 120`
- [ ] `C-CF-83` `data` The blog reads articles from the `production` dataset under the published perspective. `src: Core features rule 120`
- [ ] `C-CF-84` `capability` A published-only caller asking for drafts receives published content with a stated downgrade. `src: Core features rule 95`
- [ ] `C-CF-85` `constraint` A downgraded answer carries no draft-only document. `src: Core features rule 95`
- [ ] `C-CF-86` `literal` A mutation by query carrying no filter is refused with `unfiltered_mutation_refused`. `src: Core features rule 38`
- [ ] `C-CF-87` `constraint` A refused mutation by query removes no document. `src: Core features rule 38`
- [ ] `C-CF-88` `literal` A mutation by query without the confirmation flag is refused with `mutation_by_query_unconfirmed`. `src: Core features rule 38`
- [ ] `C-CF-89` `data` Every mutation by query is written to the audit log with query text, count, actor. `src: Core features rule 38`
- [ ] `C-CF-90` `contract` `GET /api/project/audit` returns the chained entries to an administrator. `src: Core features rule 38`
- [ ] `C-CF-91` `literal` Publishing with a draft-only strong dependency is refused with `publish_dependencies_unpublished`. `src: Core features rule 42`
- [ ] `C-CF-92` `capability` A refusal for an unpublished dependency names the dependency. `src: Core features rule 42`
- [ ] `C-CF-93` `literal` Deleting a strongly referenced document is refused with `delete_blocked_by_references`. `src: Core features rule 40`
- [ ] `C-CF-94` `capability` The refusal of a blocked delete names the referring documents. `src: Core features rule 40`
- [ ] `C-CF-95` `capability` A dangling weak reference dereferences to null rather than raising. `src: Core features rule 41`
- [ ] `C-CF-96` `data` A reference carries a target identifier plus a strength. `src: Core features rule 39`
- [ ] `C-CF-97` `literal` Uploaded bytes live in the bucket named by `STORAGE_BUCKET` under `assets/{dataset}/{sha256_of_bytes}.{ext}`. `src: Core features rule 73`
- [ ] `C-CF-98` `data` An asset identifier embeds the content hash plus the dimensions. `src: Core features rule 72`
- [ ] `C-CF-99` `capability` Uploading identical bytes twice yields one asset referenced twice. `src: Core features rule 72`
- [ ] `C-CF-100` `literal` A derived rendering is cached under `derived/{dataset}/{sha256_of_bytes}/{parameter_digest}.{ext}`. `src: Core features rule 74`
- [ ] `C-CF-101` `capability` Changing one use's crop leaves every other use of that asset unchanged. `src: Core features rule 71`
- [ ] `C-CF-102` `data` A use owns the crop, the hotspot, the alternative text. `src: Core features rule 71`
- [ ] `C-CF-103` `capability` A square rendering of an edge hotspot keeps the hotspot region fully visible. `src: Core features rule 77`
- [ ] `C-CF-104` `capability` A width beyond the original clamps rather than upscaling. `src: Core features rule 78`
- [ ] `C-CF-105` `contract` An asset in a private dataset is served only through the authenticated streaming endpoint. `src: Core features rule 75`
- [ ] `C-CF-106` `literal` A mislabelled upload is refused with the code `asset_type_refused`. `src: Core features rule 80`
- [ ] `C-CF-107` `capability` An upload type is determined from the leading bytes rather than the filename. `src: Core features rule 80`
- [ ] `C-CF-108` `constraint` A refused upload creates no asset row. `src: Core features rule 80`
- [ ] `C-CF-109` `ui` The playground shows the cost of a query beside its result. `src: Core features rule 49`
- [ ] `C-CF-110` `ui` The dry-run report names the dataset in its first line. `src: Core features rule 85`
- [ ] `C-CF-111` `ui` Editor search accepts a word whose middle is emboldened. `src: Core features rule 103`
- [ ] `C-CF-112` `ui` The not-found page suggests the nearest real route for a near-miss address. `src: Core features rule 121`
- [ ] `C-CF-113` `ui` An invalid demo request names the offending field inline. `src: Core features rule 125`
- [ ] `C-CF-114` `ui` The section rail carries the five numbered entries the brief names. `src: Core features rule 114`
- [ ] `C-CF-115` `ui` Every rail entry moves the reader to the matching section. `src: Core features rule 114`
- [ ] `C-CF-116` `ui` The install command pill carries the command the brief names. `src: Core features rule 113`
- [ ] `C-CF-117` `ui` The copy control copies the command text alone. `src: Core features rule 113`
- [ ] `C-CF-118` `ui` A refused publish offers to publish every dependency in one action. `src: Core features rule 42`
- [ ] `C-CF-119` `ui` A dataset's visibility is shown wherever the dataset is named. `src: Core features rule 87`
- [ ] `C-CF-120` `ui` Every code block names its language beside a copy control. `src: Core features rule 116`
- [ ] `C-CF-121` `constraint` No syntax highlighter is sent to the browser. `src: Core features rule 116`
- [ ] `C-CF-122` `ui` The not-found page carries the address that failed plus a way back. `src: Core features rule 121`
- [ ] `C-CF-123` `ui` Refusing cookies is offered by one control of the same prominence as accepting. `src: Core features rule 123`

## C-UF User flow

- [ ] `C-UF-01` `contract` `/pricing` serves the plans route. `src: User flow route table`
- [ ] `C-UF-02` `contract` `/enterprise` serves the buyer's route. `src: User flow route table`
- [ ] `C-UF-03` `contract` `/privacy` serves what the product stores. `src: User flow route table`
- [ ] `C-UF-04` `contract` `/terms` serves the terms. `src: User flow route table`
- [ ] `C-UF-05` `contract` `/docs` serves the documentation home. `src: User flow route table`
- [ ] `C-UF-06` `contract` `/cookie-settings` serves the revisitable cookie decision. `src: User flow route table`
- [ ] `C-UF-07` `contract` `/signin` serves the sign-in form; `/studio` serves the dataset chooser. `src: User flow route table`
- [ ] `C-UF-08` `contract` `/d/{dataset}/desk` serves the document table; `/d/{dataset}/doc/{id}` serves the document editor. `src: User flow route table`
- [ ] `C-UF-09` `ui` A refusal at sign-in is shown inline on the form. `src: User flow states`
- [ ] `C-UF-10` `ui` The page keeps whatever was typed after a refusal. `src: User flow states`
- [ ] `C-UF-11` `ui` A control the viewer may not use is absent rather than present. `src: User flow states`
- [ ] `C-UF-12` `contract` `/d/{dataset}/search` serves editor search. `src: User flow route table`
- [ ] `C-UF-13` `contract` `/blog` serves the editorial index. `src: User flow route table`
- [ ] `C-UF-14` `ui` A refetch keeps existing rows on screen without losing scroll position. `src: User flow states`
- [ ] `C-UF-15` `ui` An error is an inline message in the region that produced the error. `src: User flow states`
- [ ] `C-UF-16` `contract` `/d/{dataset}/doc/{id}/history` serves the revision chain. `src: User flow route table`
- [ ] `C-UF-17` `ui` A blocked publish is reported inline rather than as a whole-page error. `src: User flow states`
- [ ] `C-UF-18` `contract` `/project/datasets` serves datasets, visibility, copy, delete to an administrator. `src: User flow route table`
- [ ] `C-UF-19` `contract` `/project/audit` serves the audit log to an administrator alone. `src: User flow route table`
- [ ] `C-UF-20` `contract` `/d/{dataset}/vision` serves the query playground. `src: User flow route table`
- [ ] `C-UF-21` `ui` Every list carries an empty state naming the action that creates the first entry. `src: User flow states`
- [ ] `C-UF-22` `contract` `/d/{dataset}/media` serves the media library. `src: User flow route table`
- [ ] `C-UF-23` `ui` A refused upload is reported inline in the media library. `src: User flow states`
- [ ] `C-UF-24` `ui` A filtered list returning nothing names each active filter with a clear control. `src: User flow states`
- [ ] `C-UF-25` `contract` `/project/migrations` serves the migration runner to an administrator. `src: User flow route table`
- [ ] `C-UF-26` `contract` `/d/{dataset}/releases` serves releases to an editor. `src: User flow route table`
- [ ] `C-UF-27` `ui` A partial failure shows loaded rows with an inline retry for the missing range. `src: User flow states`
- [ ] `C-UF-28` `ui` Search that cannot answer says so rather than returning nothing. `src: User flow states`
- [ ] `C-UF-29` `contract` `/` serves the marketing home. `src: User flow route table`
- [ ] `C-UF-30` `contract` `/contact` serves the demo request form. `src: User flow route table`
- [ ] `C-UF-31` `ui` `/d/{dataset}/doc/{id}/published` serves the publish confirmation to an editor. `src: User flow route table`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The document table shows one document per row under a shared header. `src: UI/UX notes layout`
- [ ] `C-UX-02` `ui` Every badge carries a label together with a shape rather than a colour alone. `src: UI/UX notes layout`
- [ ] `C-UX-03` `ui` Creating a document opens a modal over the document table rather than navigating away. `src: UI/UX notes layout`
- [ ] `C-UX-04` `ui` The document editor is a single column of fields at a capped measure. `src: Front-end specification studio shell`
- [ ] `C-UX-05` `ui` Body copy on a published article is set at the body size the brief names. `src: UI/UX notes type`
- [ ] `C-UX-06` `ui` Sortable columns announce their sort state. `src: UI/UX notes layout`
- [ ] `C-UX-07` `ui` Each document row carries a publication state badge readable without opening the document. `src: UI/UX notes layout`
- [ ] `C-UX-08` `ui` Each image use shows its own alternative text beside the image. `src: UI/UX notes accessibility`
- [ ] `C-UX-09` `ui` Editing the crop of one use is offered on the image block of the document editor. `src: Front-end specification studio shell`
- [ ] `C-UX-10` `ui` The document table reads as one dense table of rows rather than a grid of cards. `src: UI/UX notes layout`
- [ ] `C-UX-11` `ui` Every button wears the full capsule shape. `src: UI/UX notes shape`
- [ ] `C-UX-12` `ui` The brand colour renders as white on a dark surface. `src: UI/UX notes colour`
- [ ] `C-UX-13` `ui` The four publication states each carry their own label. `src: UI/UX notes layout`
- [ ] `C-UX-14` `ui` The copy confirmation holds at the peak before settling. `src: UI/UX notes motion`
- [ ] `C-UX-15` `ui` Motion is opt-in for people who have not asked for less movement. `src: UI/UX notes motion`
- [ ] `C-UX-16` `ui` The mega-menu opens on focus, closes on Escape, returns focus to the trigger. `src: UI/UX notes accessibility`
- [ ] `C-UX-17` `literal` A skip link reading `Skip to content` is the first focusable element. `src: UI/UX notes accessibility`
- [ ] `C-UX-18` `ui` No content is hidden at any width except the install command pill. `src: UI/UX notes responsive`
- [ ] `C-UX-19` `ui` Every route fits the viewport horizontally at phone width. `src: UI/UX notes responsive`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Two clients patching different items of one array both succeed. `src: Technical requirements concurrency`
- [ ] `C-TR-02` `capability` Server-side arithmetic replaces a read followed by a write on every counter. `src: Technical requirements concurrency`
- [ ] `C-TR-03` `literal` The replay window is read from `TRANSACTION_REPLAY_WINDOW_SEC`. `src: Technical requirements configuration`
- [ ] `C-TR-04` `constraint` A refused mutation leaves no revision, no audit entry, no event. `src: Technical requirements concurrency`
- [ ] `C-TR-05` `contract` The server renders every route as markup before the browser receives the route. `src: Technical requirements stack`
- [ ] `C-TR-06` `capability` The revision, the history entry, the announcement record are written in one transaction. `src: Technical requirements one write`
- [ ] `C-TR-07` `constraint` No read reaches storage without a dataset predicate plus a grant predicate. `src: Technical requirements dataset boundary`
- [ ] `C-TR-08` `capability` One authorization decision is made per request before the body is validated. `src: Technical requirements authorization`
- [ ] `C-TR-09` `capability` The audit chain verifies end to end after a hundred concurrent audited actions. `src: Technical requirements audit`
- [ ] `C-TR-10` `literal` The object store is reached at `STORAGE_ENDPOINT` with `STORAGE_ACCESS_KEY` plus `STORAGE_SECRET_KEY`. `src: Technical requirements stack`
- [ ] `C-TR-11` `contract` The JSON API is served from the same origin under the `/api` prefix. `src: Technical requirements stack`
- [ ] `C-TR-12` `literal` The datastore is reached with the connection string in `DATABASE_URL`. `src: Technical requirements stack`
- [ ] `C-TR-13` `constraint` An authorization outcome is never cached. `src: Technical requirements authorization`
- [ ] `C-TR-14` `capability` The document store together with the revision store form the permanent record. `src: Technical requirements derived stores`
- [ ] `C-TR-15` `constraint` A dataset identifier taken from a request body never decides which dataset is read. `src: Technical requirements dataset boundary`

## C-DM Data model

- [ ] `C-DM-01` `data` A dataset row carries visibility, document count, asset count. `src: Data model dataset`
- [ ] `C-DM-02` `literal` The datasets `production` plus `staging` are seeded. `src: Data model seed data`
- [ ] `C-DM-03` `data` A document row is unique on the dataset plus the identifier together. `src: Data model document`
- [ ] `C-DM-04` `literal` The document `article-migrating-schemas` is seeded as published. `src: Data model seed data`
- [ ] `C-DM-05` `data` A transaction row is unique on the client-supplied identifier. `src: Data model transaction`
- [ ] `C-DM-06` `data` Every mutation produces a new revision identifier. `src: Data model invariants`
- [ ] `C-DM-07` `data` A revision row chains to the row before through a previous revision column. `src: Data model revision`
- [ ] `C-DM-08` `literal` The document `article-keys-and-arrays` is seeded as never published. `src: Data model seed data`
- [ ] `C-DM-09` `data` A draft is an ordinary row whose identifier carries the reserved prefix. `src: Data model document`
- [ ] `C-DM-10` `data` A migration run row carries a mode defaulting to the dry run. `src: Data model migration run`
- [ ] `C-DM-11` `literal` The document `article-aurora-pipeline` is seeded as published with unpublished edits. `src: Data model seed data`
- [ ] `C-DM-12` `data` A new dataset row carries the private visibility until an administrator changes the setting. `src: Data model dataset`
- [ ] `C-DM-13` `data` A release row carries its member document identifiers plus its state. `src: Data model release`
- [ ] `C-DM-14` `data` A lead row carries the work address, the name, the company, the team size. `src: Data model lead`
- [ ] `C-DM-15` `literal` The document `article-quarterly-letter` is seeded under the `marketing` department. `src: Data model seed data`
- [ ] `C-DM-16` `data` A grant row carries a role, a dataset, a query filter. `src: Data model grant`
- [ ] `C-DM-17` `data` The audit log is append-only, hash-chained, written through a single writer. `src: Data model audit entry`
- [ ] `C-DM-18` `literal` The document `author-tomas` is seeded as a draft alone. `src: Data model seed data`
- [ ] `C-DM-19` `data` A reference edge row carries origin, target, path, strength. `src: Data model reference edge`
- [ ] `C-DM-20` `literal` The asset `image-9f2ae1c4d0b7-1600x900-png` is seeded at `assets/production/9f2ae1c4d0b7.png`. `src: Data model seed data`
- [ ] `C-DM-21` `data` An asset row is unique on the dataset plus the identifier together. `src: Data model asset`
- [ ] `C-DM-22` `constraint` Crop, hotspot, alternative text are absent from the asset row. `src: Data model asset`
- [ ] `C-DM-23` `literal` The seeded image keeps its own crop together with its own alternative text in each use. `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Rows sit tight enough that a full screen of documents is readable at once. `src: Front-end specification studio shell`
- [ ] `C-FE-02` `ui` The two very large closing actions are the ordinary button at a larger size. `src: Front-end specification radius`
- [ ] `C-FE-03` `ui` A public dataset carries a band across the top bar of the studio. `src: Front-end specification studio shell`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No document of one department is visible to a person of another department, at any address. `src: Constraints`
- [ ] `C-CN-02` `constraint` No draft content reaches a caller carrying no credentials. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The app answers at `APP_PUBLIC_URL` with the HTTP API under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-03` `literal` The server binds `0.0.0.0`, so the app is reachable from outside the container. `src: Deployment contract`
- [ ] `C-DC-04` `contract` Every list endpoint returns a top-level JSON array. `src: Deployment contract API shapes`
- [ ] `C-DC-05` `contract` A rejected call carries a stable machine-readable code plus a readable message. `src: Deployment contract API shapes`
- [ ] `C-DC-06` `constraint` No in-memory store substitutes for the datastore or the object store. `src: Deployment contract no mocks`
- [ ] `C-DC-07` `contract` A successful call returns the named resource or shape. `src: Deployment contract API shapes`
- [ ] `C-DC-08` `contract` An unauthorized call is rejected as a client error rather than as a server error. `src: Deployment contract API shapes`
- [ ] `C-DC-09` `literal` The container-internal port is `4173`, read from the environment. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `GET /api/health` | a value the brief pins | `C-DC-01` |
| `200` | a value the brief pins | `C-DC-01` |
| `APP_PUBLIC_URL` | a value the brief pins | `C-DC-02` |
| `/api` | a value the brief pins | `C-DC-02` |
| `0.0.0.0` | a value the brief pins | `C-DC-03` |
| `deku-demo-pw-2026` | a value the brief pins | `C-RL-01` |
| `production` | a value the brief pins | `C-DM-02` |
| `staging` | a value the brief pins | `C-DM-02` |
| `article-migrating-schemas` | a value the brief pins | `C-DM-04` |
| `100` | a value the brief pins | `C-CF-17` |
| `TRANSACTION_REPLAY_WINDOW_SEC` | a value the brief pins | `C-CF-19` |
| `revision_mismatch` | a value the brief pins | `C-CF-21` |
| `article-keys-and-arrays` | a value the brief pins | `C-DM-08` |
| `query_bound_exceeded` | a value the brief pins | `C-CF-54` |
| `5` | a value the brief pins | `C-CF-56` |
| `apply` | a value the brief pins | `C-CF-57` |
| `article-aurora-pipeline` | a value the brief pins | `C-DM-11` |
| `production_confirmation_required` | a value the brief pins | `C-CF-63` |
| `release_too_large` | a value the brief pins | `C-CF-68` |
| `404` | a value the brief pins | `C-CF-71` |
| `Page not found` | a value the brief pins | `C-CF-71` |
| `article-quarterly-letter` | a value the brief pins | `C-DM-15` |
| `marketing` | a value the brief pins | `C-DM-15` |
| `grant_escape_refused` | a value the brief pins | `C-RL-13` |
| `unfiltered_mutation_refused` | a value the brief pins | `C-CF-86` |
| `mutation_by_query_unconfirmed` | a value the brief pins | `C-CF-88` |
| `publish_dependencies_unpublished` | a value the brief pins | `C-CF-91` |
| `author-tomas` | a value the brief pins | `C-DM-18` |
| `delete_blocked_by_references` | a value the brief pins | `C-CF-93` |
| `STORAGE_BUCKET` | a value the brief pins | `C-CF-97` |
| `assets/{dataset}/{sha256_of_bytes}.{ext}` | a value the brief pins | `C-CF-97` |
| `image-9f2ae1c4d0b7-1600x900-png` | a value the brief pins | `C-DM-20` |
| `assets/production/9f2ae1c4d0b7.png` | a value the brief pins | `C-DM-20` |
| `STORAGE_ENDPOINT` | a value the brief pins | `C-TR-10` |
| `STORAGE_ACCESS_KEY` | a value the brief pins | `C-TR-10` |
| `STORAGE_SECRET_KEY` | a value the brief pins | `C-TR-10` |
| `derived/{dataset}/{sha256_of_bytes}/{parameter_digest}.{ext}` | a value the brief pins | `C-CF-100` |
| `asset_type_refused` | a value the brief pins | `C-CF-106` |
| `DATABASE_URL` | a value the brief pins | `C-TR-12` |
| `4173` | a value the brief pins | `C-DC-09` |
| `Skip to content` | a value the brief pins | `C-UX-17` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of every colour role | `C-UX-12` |
| the base spacing unit the layout is built on | `C-UX-11` |
| the exact easing pair carrying the two speeds | `C-UX-14` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 5 | 5 |
| User roles | 2 | 16 |
| Core features | 61 | 123 |
| User flow | 10 | 31 |
| UI/UX notes | 9 | 19 |
| Technical requirements | 15 | 15 |
| Data model | 5 | 23 |
| Front-end specification | 2 | 3 |
| Constraints | 2 | 2 |
| Deployment contract | 9 | 9 |
