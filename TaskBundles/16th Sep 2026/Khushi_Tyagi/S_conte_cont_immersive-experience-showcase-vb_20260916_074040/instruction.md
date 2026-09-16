# Kindling Atelier

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, fall through one continuous
lit scene past a curated reel of the studio's work, open a case study, read it, play its behind
the scenes reel, and leave an email address at the foot of the page, without hitting an error
page. A case study that has not been published must not be readable by that stranger on any route
or through any endpoint; the only thing that opens it is a preview token the server verifies, and
a draft that a crawler or a direct request can reach is the failure this product exists to
prevent. A producer may write anything and publish nothing: an attempt to publish from a producer
session must be refused by the server and must leave the stored state untouched, and a refusal
drawn only in the console interface does not count. Every media rendition must be a real object in
`minio` at its content addressed key, and every published record, every preview token and every
publish log row must be a real row in `postgres` that survives a restart; bytes on the app's own
disk and a success the app returns to itself do not count.

## Overview

Kindling Atelier is the portfolio of a small digital experience studio that sells commissioned
work to luxury and corporate brands, together with the content console the studio runs it from.
The two halves share nothing but a content interface. The public showcase is the product: one
continuous lit scene running behind every route, a reel of case studies laid against it, a case
study reader, a behind the scenes reel, a studio story told as numbered chapters, and a mailing
list intake. The console exists so that the showcase can change without a deploy.

The window never scrolls. Every route is exactly one window tall, and a virtual scroller captures
wheel, touch and key input, integrates it into an offset, smooths it and applies it as a
transform, so that the copy and the camera move from the same value in the same frame. That one
decision produces most of what is distinctive here and most of what is hard: everything a browser
normally does for a scrolling page has to be put back by hand.

Three visitors arrive and none of them holds an account. A prospective client scans the reel,
opens two case studies and looks for the client names. A jury or a peer studio sits through the
loader, turns the sound on and opens the behind the scenes reel. A candidate reads the studio
chapters. There is no visitor identity in this product beyond a consent record and an optional
email address on a list.

Inside the studio, four people work behind one console. The rule that carries the whole design is
that a producer can write anything and publish nothing, and an editor signs off. That is what
makes the four state workflow real rather than advisory, and it is why the draft gate is the
mechanic this product is graded hardest on: an unpublished case study for a client launch that
leaks before its embargo is the failure that costs a studio the relationship.

The genuinely hard part is the pair of boundaries underneath the showcase. Draft content must be
unreadable without a server verified token, and a media pipeline must never leave a published
route referencing a rendition that does not exist. Both are invisible while they work and
unrecoverable when they do not.

Kindling Atelier deliberately is not: a client portal, a shop, a payment surface, a customer
relationship system, a comment or social feed, a search engine, a translation service or a
realtime collaboration tool. There is no sign in on the public side, no per client view, no shared
asset review, no invoice, no time tracking and no price anywhere. It ships no photograph, no video
file, no model, no colour grade table, no font binary and no sound file, and it makes no network
call to any other origin at run time.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Anonymous visitor | Read every published case study, the full index, the studio story and every published chapter; open a behind the scenes reel and the video overlay; follow an outbound link; submit one email address to the mailing list; accept or reject the measurement category; read the privacy notice | **Cannot read any record that is not published, on any route or through any endpoint, without a valid preview token. Cannot reach any console route. Cannot learn from any response whether an address is already on the mailing list** |
| `producer` | Everything a visitor can, plus sign in to the console, create and edit a draft case study or chapter, upload a media master, mint and revoke a preview token for a record, move a record from draft to in review, read the publish log and read the media library | **Cannot move any record to published. Cannot move a record out of published. Cannot reorder the home reel. Cannot delete a media master. Cannot edit the discipline vocabulary. Cannot read or write another producer's preview tokens** |
| `editor` | Everything a producer can, plus move a record to published and back to unpublished, reorder the home reel, edit the discipline vocabulary, delete a media master, and promote a scene configuration to the live one | **Cannot delete a publish log row, and no role can. Cannot delete a media master that any record still references** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from an anonymous session to any console endpoint, or from a
`producer` session to any `editor`-only endpoint, must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

The draft gate is the same rule pointed at reads. A record whose state is `draft`, `in_review` or
`unpublished` is absent from every public listing, answers not found on its own public route, and
is absent from every public endpoint's response, for an anonymous caller and for a signed in
producer alike when they ask through a public route. The one exception is the preview route, which
takes a token, verifies it on the server, and serves that one record in that one state.

Signup is open and creates a `producer`. A role is read from the session, never from the request
body. Three accounts are seeded, all with the password `deku-demo-pw-2026`:
`producer@example.com` and `producer2@example.com` as producers, and `editor@example.com` as the
editor.

## Core features

### Auth and the console session

Console accounts are email and password, held by this app. The public showcase has no sign in, no
session, no profile and no personalised surface, and no public response may vary by anything other
than the requested path.

1. `POST /api/auth/login` returns the account and a bearer token under the key `access_token`,
   which the client sends on every authenticated call. Passwords are stored hashed, never in clear.
2. A failed sign in answers with one wording for a wrong password and for an address that holds no
   account, `Incorrect email or password`, so the form cannot be used to discover which addresses
   hold accounts.
3. Sign in is rate limited per account and per source with a progressive delay rather than a
   lockout, because a lockout on a three person console is a denial of service anybody who knows a
   colleague's address can deliver.
4. `POST /api/auth/signup` with an address that is already held is rejected as invalid and writes
   no second account row. A new account is a `producer`.
5. A stale token is denied on every authenticated call rather than served, and the surface offers
   sign in again without discarding what was typed.
6. `GET /api/auth/me` returns the signed in account and its role, and answers denied without a
   token. A role change revokes every outstanding session for the affected account.
7. Every account carries a last used timestamp. Deactivating an account revokes its sessions and
   its preview tokens in one action, and the publish log keeps its account identifier as a stable
   value afterwards so an audit does not develop holes when somebody leaves the studio.

### The content model and the seeded catalogue

Six content types: three singletons, the home record, the studio record and the global record, and
three collections, projects, chapters and reels. Everything on every public route comes out of this
model.

1. A project carries a title, a slug, a type, a discipline list, an optional live address, an
   ordered block list, an optional reel and an optional list of retired paths.
2. The project type is one of exactly three values: `Web Experience`, `Corporate`, `E-Shop`.
3. **The disciplines are a controlled vocabulary, not a free text string.** They are their own
   collection, referenced many to many, and only an `editor` may add a term. Ten are seeded:
   `Design`, `Experience`, `3D`, `Tech`, `Strategy`, `Branding`, `E-shop`, `Web3`, `NFT`, `Film`.
   Rendering splits nothing, because there is nothing to split.
4. `GET /api/disciplines` returns the ten in position order. A producer posting a discipline that
   is not in the vocabulary is rejected as invalid, which is what stops `3d`, `3D` and `three d`
   appearing in one afternoon.
5. Eighteen projects are seeded:

| Slug | Title | Type | State |
|---|---|---|---|
| `lambert-vitrine` | `Lambert Vitrine` | `Web Experience` | `published` |
| `aurel-vance-experience` | `Aurel Vance Experience` | `Web Experience` | `published` |
| `verrine-end-of-year-23` | `Verrine End of Year 23` | `E-Shop` | `published` |
| `chastenay-belfort` | `Chastenay Belfort` | `Web Experience` | `published` |
| `verrine-in-time` | `Verrine in Time` | `Web Experience` | `published` |
| `grale` | `Grale` | `Corporate` | `published` |
| `harwick-spirit-meridian-hour` | `Harwick Spirit Meridian Hour` | `Web Experience` | `published` |
| `nasira-destination` | `Nasira Destination` | `Web Experience` | `published` |
| `nidvar` | `Nidvar` | `Corporate` | `published` |
| `orrery-orbital-stewardship` | `Orrery Orbital Stewardship` | `Corporate` | `published` |
| `arven` | `Arven` | `Corporate` | `published` |
| `prade-holding` | `Prade Holding` | `Web Experience` | `published` |
| `faiseurs-d-ourcq` | `Faiseurs d'Ourcq` | `Web Experience` | `published` |
| `verrine-watchmaking-salon-24` | `Verrine Watchmaking Salon 24` | `Web Experience` | `published` |
| `rocheval-perrin-casquette` | `Rocheval Perrin Casquette` | `E-Shop` | `published` |
| `halom` | `Halom` | `Web Experience` | `published` |
| `marivella` | `Marivella` | `Web Experience` | `in_review` |
| `oryx7` | `Oryx7` | `Web Experience` | `in_review` |

Sixteen are published and two are in review. `verrine-end-of-year-23` carries no live address,
because that live site has been retired; every other project carries one.

6. The seeded descriptions, which the reel and the index carry verbatim:
   `Lambert Vitrine` reads
   `Explore our collaboration with Lambert on Vitrine, showcasing the Maison's Web 3 vision through its first digital trunk.`
   `Aurel Vance Experience` reads
   `Step into Aurel Vance's poetry in a digital journey, capturing life's profound moments with artistic depth.`
   `Verrine End of Year 23` reads
   `Discover Verrine's End of Year: redefining elegance with an immersive campaign, Beyond the Clouds.`
   `Chastenay Belfort` reads
   `Explore the rich heritage and vineyards of Chastenay Belfort through immersive digital storytelling.`
   `Verrine in Time` reads
   `Dive into a journey with Ilan Voss, unveiling Verrine's timeless bond with time in a stunning digital showcase.`
   `Grale` reads
   `Explore the Grale ecosystem, a mobile first gateway showcasing their unified crypto ecosystem through cutting edge digital design.`
   `Harwick Spirit Meridian Hour` reads
   `Embark on the pioneering flights of Ada Jansen, Colm Prendergast and Hugh Merrivale. Discover Harwick Spirit Meridian Hour: honoring aviation pioneers with precision and innovation.`
   `Nasira Destination` reads
   `Explore Nasira's Vision: A captivating digital experience redefining the urban heart of Saudi Arabia.`
   `Nidvar` reads
   `Dive deeper into Nidvar's vision, an extraordinary blend of human centric design and immersive storytelling.`
   `Orrery Orbital Stewardship` reads
   `Discover Orrery's Journey in Orbital Stewardship, Shaping Innovation and Pioneering Impact.`
   `Arven` reads
   `Navigate safely through radioactive zones with Arven's cutting edge innovations, explore interactive wireframes and gamified design solutions.`
   `Prade Holding` reads
   `Unveil the essence of authentic hospitality with Prade Holdings, an immersive experience that celebrates dreams and culture.`
   `Faiseurs d'Ourcq` reads
   `Step into Faiseurs d'Ourcq's digital world, an interactive journey blending art, history and storytelling for a truly immersive experience.`
   `Verrine Watchmaking Salon 24` reads
   `An inspiring selection of Verrine timepieces, offering a remarkable journey for the Watchmaking Salon 2024.`
   `Rocheval Perrin Casquette` reads
   `Rediscover the Limited Edition RP Casquette, Experience Modern Elegance and Timeless Heritage from Rocheval Perrin.`
   `Halom` reads
   `Dive into the essence of cryptocurrency and explore Halom's immersive universe, unlocking the story of their evolving crypto platform through symbolic storytelling.`
   `Marivella` reads
   `Step into an exquisite 3D journey through Marivella, where Elena Rossi Chiari's visionary designs come to life in breathtaking detail.`
   `Oryx7` reads
   `Uncover the secrets of Oryx7 and the rise of EVA in the immersive "Vault Archives" experience.`

7. Six studio chapters are seeded, each with a numeral, a title and a slug: `Where we started` at
   `where-we-started`, `How we work` at `how-we-work`, `What we refuse` at `what-we-refuse`,
   `The people` at `the-people`, `The craft` at `the-craft`, and `The studio` at `the-studio`. The
   first five carry the numerals `I`, `II`, `III`, `IV` and `V`; the sixth is marked by the studio
   mark rather than by a numeral, which is the studio saying that the last chapter is itself.
8. A chapter carries a scene index binding it to one of six declared scene views, validated against the
   registered scene count when it is saved rather than when it is rendered. A chapter saved with an
   index outside the range is rejected as invalid.
9. The numeral label is stored rather than derived from position, so an editor can renumber without
   reordering and reorder without renumbering.
10. The global record carries the footer baseline, the studio mailbox `studio@example.com`, the
    studio street address, the projects panel title and a second curated ordered project list.

### The home reel and its ordering contract

1. The home reel is an **ordered editorial subset**, stored as an explicit ordered list on the home
   record. It is not a query with a limit and it is not a flag on the project.
2. **Adding a project to the collection must not change the home page.** Publishing a case study at
   eleven at night must not rearrange the studio's front page without anybody deciding to.
3. Three of the sixteen published projects are seeded on the reel, in this order:
   `lambert-vitrine`, `grale`, `verrine-end-of-year-23`. `aurel-vance-experience` is published and
   is not on the reel, which is what makes the reel a curated subset rather than a truncation.
4. `GET /api/home-reel` returns those three in that order, each carrying its title, its type, its
   description and its own media, which may differ from the media in the case study's own body.
   Reusing the case study's first media on the reel produces a home page that looks like a contact
   sheet, and the model exists to prevent it.
5. A reel entry whose project has been unpublished disappears from the reel and never renders as an
   entry pointing at a missing page.
6. `PUT /api/console/home-reel` reorders the reel and is an `editor` capability. A `producer`
   calling it is denied and the stored order is unchanged.

### The project index

1. `/projects` lists **every published case study**, without pagination and without a query limit,
   and the document carries all of them.
2. The captured order is alphabetical by title and crosses project types freely. There is no
   grouping, no filter control and no search.
3. The sort is a stable alphabetical sort on a normalising key rather than on the raw title, so a
   title beginning with a diacritic or a typographic apostrophe sorts where a reader expects.
4. With the seeded catalogue the index carries sixteen entries, opening
   `Arven`, `Aurel Vance Experience`, `Chastenay Belfort`, `Faiseurs d'Ourcq`, `Grale`,
   `Halom` and closing `Verrine Watchmaking Salon 24`. Neither `Marivella` nor `Oryx7`
   appears, because neither is published. Eighteen are seeded, sixteen are published and three
   are on the home reel, which is what makes the reel a curated subset rather than a truncation.
5. Each row carries the project type and the project title, and the accessible name of the row is
   the whole entry rather than the title alone.
6. With no published case studies the route renders its chrome, one line of copy reading
   `Nothing published yet. Write to the studio.` and the footer. It never renders an empty grid.

### The draft gate

The mechanic this product is graded hardest on.

1. A record whose state is not `published` is **absent from every public endpoint's response** and
   its own public route answers not found. That holds for `/projects`, `/api/projects`,
   `/api/home-reel`, the sitemap and the case study route itself.
2. **A preview token is a capability, not a session.** It is opaque and high entropy, is bound to
   one record identifier and one content state, is read only, and is stored as a hash so that a
   database dump is not a set of working preview links.
3. A preview token is `prv_` followed by thirty two lowercase hexadecimal characters. Worked
   example: `prv_6d1f4a08c39b27e5d0a4f81c6b3e97d2`. One is seeded against `marivella`.
4. `GET /api/preview/{token}` verifies the token **on the server** and returns that one record in
   its draft state. A build that reads a token in the browser and asks for drafts with a shared
   credential has moved the studio's entire unpublished pipeline behind a value the visitor can
   read.
5. A token that has expired, that has been revoked, or that names a different record answers not
   found. A guessed token answers not found.
6. A preview token expires at a fixed interval from minting and on its record reaching `published`.
7. Any `editor` may revoke every outstanding token for a record in one action, and a `producer` may
   revoke only the tokens they minted. A revoked token answers not found immediately.
8. **Every preview response refuses indexing and archiving**, and the preview route is never
   prerendered and never cached. A search engine that finds a preview publishes it.
9. `POST /api/console/projects/{slug}/preview-tokens` mints one and returns it once. The token
   value is never returned again by any endpoint.

### The publish boundary and the four states

1. Four states and no chain: `draft` is being written, `in_review` is complete and awaiting sign
   off, `published` is live, `unpublished` is withdrawn and retained. All four except `published`
   are previewable.
2. `POST /api/console/projects/{slug}/transition` carries the target state. A `producer` may move a
   record from `draft` to `in_review` and back. **A `producer` moving a record to `published` is
   denied by the server and the stored state is unchanged.**
3. An `editor` may move a record to `published` and back to `unpublished`.
4. A record is never deleted. Unpublishing retains it.
5. The transition to `published` is the only one that rebuilds anything, and it must be
   transactional with that rebuild: a record that reaches `published` and whose rebuild fails is
   visible as failed rather than sitting green while the site shows the old version.
6. A slug is lowercase and hyphen separated, is unique within its collection including unpublished
   records, and **may not be changed after a record has been published once**. A case study that
   has been shared, awarded and linked for two years and then has its slug tidied is a case study
   whose inbound authority has been thrown away.
7. A slug may not collide with a reserved word, and the deny list holds the section names and the
   operational route.

### The publish gate

Cross record rules evaluated on the transition to `published`. Each one blocks the transition and
names the failing record.

1. Every referenced media is `ready`. `oryx7` is seeded referencing a media that is still
   `deriving`, so an `editor` attempting to publish it is refused and the refusal names that media.
2. Every reel section that carries audio carries a subtitle.
3. Every video carrying speech carries a caption track.
4. Every media element declares both intrinsic dimensions.
5. Every outbound target is an absolute address with a secure scheme.
6. Every internal relation points at a record that is published or is being published in the same
   transition.
7. The record carries at least one block.
8. No retired path collides with a live route or with another record's retired path.
9. Every media carries an alternative text or an explicit decorative mark.

A refused publish writes no publish log row of outcome succeeded, leaves the record in its previous
state, and returns the failing rule and the failing record.

### The publish log

1. Every transition writes one row carrying the instant, the acting account, the record type and
   slug, the state moved from, the state moved to, the outcome, and the list of routes invalidated.
2. **The log is append only.** The console offers no edit and no delete, and no role, including
   `editor`, has any capability that removes a row.
3. `GET /api/console/publish-log` returns the rows newest first and is readable by both roles.
4. A publish rebuilds exactly the routes the change touches and no others. A change to a project's
   body rebuilds that project. A change to its title, type or disciplines rebuilds that project,
   the index, and the home page if it is on the reel. A first publish rebuilds that project and the
   index. An unpublish rebuilds the index, the home page if it was on the reel, and every project
   whose next link pointed at it. A change to the home reel order rebuilds the home page. A change
   to the global record rebuilds every route, because the footer is on all of them.
5. The console must show, before any unpublish or delete, exactly what will change. A director
   unpublishing a case study because a client asked needs to know in that moment that it was also
   the third entry on the home page.

### The media pipeline

1. A producer uploads a master through `POST /api/console/media`. The master is stored unmodified
   in `minio`, keyed by its content hash.
2. Intrinsic dimensions, a duration where the media has one, and a media type are extracted and
   written to the record.
3. A rendition key is `media/<content-hash>/<variant>.<ext>`. Worked example:
   `media/9f2ad0c4/medium.avif`. A master key is `media/<content-hash>/master.<ext>`.
4. The still ladder carries six variants: `placeholder` at a longest edge small enough to inline,
   then `xs`, `sm`, `md`, `lg` and `xl`, each in a modern format with a conventional fallback.
5. **Every rendition is content addressed and immutable.** Replacing a media means a new hash and a
   new key, never an overwrite, which is what allows a long cache lifetime and means a rendition is
   never invalidated.
6. A media record moves through `uploaded`, `deriving`, `ready` and `failed`. A record referencing a
   media that is not `ready` may be edited and may not be published.
7. Derivation is idempotent and resumable. Each rendition is written to a temporary key and moved
   atomically, so a job killed halfway leaves no partial rendition, and a rerun skips renditions
   that already exist.
8. A derivation that fails permanently marks the media `failed`, names the failing variant, and
   does not block the other variants.
9. **The bytes live in `minio` and nowhere else.** A rendition on the app container's filesystem, a
   row holding the bytes, or a record marked ready whose object is absent from the bucket, are each
   a contract violation.
10. `DELETE /api/console/media/{id}` requires the `editor` role, is refused while any record
    references the media, and the refusal lists the referencing records. A successful delete removes
    the master and every rendition and writes a publish log row.
11. A media belonging to a record that is not published is served only through an authenticated
    endpoint on this app and never by a direct bucket address, so a draft's imagery leaks no more
    than its text does.

### The behind the scenes reel

1. A reel is an overlay over a case study, reached from `See backstage`, and it pushes a history
   entry so a back gesture returns to the case study rather than to the index.
2. A reel carries a title and an ordered list of sections. Each section carries a duration in whole
   milliseconds, one audio file, one subtitle file and a list of media, each media carrying a scale,
   a vertical position and its intrinsic width and height.
3. The total duration is the sum of the section durations. A section of zero duration is rejected on
   write, because it divides by zero in the timeline normalisation.
4. **A section that carries audio and carries no subtitle cannot be stored.** The refusal is at the
   storage layer, not in the console, because this is the rule most likely to be worked around under
   deadline. A studio that publishes a narrated film with no captions has excluded every deaf
   visitor from its own portfolio.
5. Subtitles render by default and are not a setting.
6. One reel is seeded against `lambert-vitrine`, carrying three sections, each with a duration, an
   audio file, a subtitle file and two media.
7. `GET /api/reels/{project_slug}` returns the reel for a published project and answers not found
   for a project that is not published.
8. The control that opens a reel is not rendered when the case study carries no reel, and a reel
   with no sections does not open.
9. Entering the reel suspends the ambient bed and restores it on exit. If the visitor has not
   enabled sound, the reel plays silently with its subtitles and offers the sound control rather
   than prompting for it.

### The mailing list intake

The one form in the product, one field, and the only write path an anonymous visitor can reach.

1. `POST /api/subscribers` carries one address and nothing else. There is no contact form, no brief
   form and no file upload anywhere on the public side.
2. **Resubmitting a known address returns the same success response as a new one, and the response
   never distinguishes the two.** A response that says already subscribed turns the studio's list
   into a service for checking whether a given person is on it.
3. The address is stored unconfirmed with a single use, expiring confirmation token held as a hash,
   and only a confirmed address is on the list.
4. `GET /api/subscribers/confirm/{token}` confirms it. A second use of the same token reports the
   same confirmation rather than an error and never re subscribes.
5. Submitting is the consent. The stored row keeps the consent instant and the version of the
   consent text that was shown, because a consent that cannot say what was agreed to is not a
   consent record.
6. The row holds the normalised address, the display form, the state, the source route, the consent
   version, the consent instant and the confirmation instant, and nothing else. It is the only
   table in the product holding personal data.
7. Intake is rate limited per address and per source over a short window and a long window, and a
   rate limited response carries a retry hint rather than a bare rejection.
8. The confirmation message is rate limited per address independently of the intake, so submitting repeatedly
   cannot be used to send a stranger a stream of mail.
9. The request must carry an origin the server recognises, and a cross origin post from elsewhere
   is rejected.
10. A bot mitigation is evaluated on the server: the form carries an unattended decoy field, and a
    submission that fills it is refused and writes nothing.
11. Client validation is a courtesy and the server repeats all of it. A malformed address is
    refused with the message `Invalid email format`, and nothing is written.
12. Four outcomes, each distinguishable: accepted, which names the submitted address in its
    confirmation; refused as malformed; rate limited, which names a wait; and temporarily
    unavailable, which offers a retry control and **leaves the typed address in the field**.
13. An unsubscribe link requires no sign in, is honoured immediately and permanently, and a second
    use reports the same confirmation.
14. An unconfirmed address is deleted when its confirmation window expires.

### The commercial loop

1. `Launch website` is the case study's commercial payload and the link to the live site the studio
   built. It opens in a new browsing context, carries no referrer and no opener relationship, and is
   recorded as an outbound click.
2. The link is optional. `verrine-end-of-year-23` is seeded with no live address and renders without
   the control rather than with a dead one.
3. `POST /api/outbound-clicks` records the project slug and nothing identifying. **An outbound click
   is never recorded as a conversion**, because the studio never learns what happened at the other
   end.
4. Four events close the loop and nothing else is measured: a reel entry opened, carrying the
   project slug and its position; a live site launched, carrying the project slug; a backstage reel
   viewed, carrying the slug and the fraction reached; and an address submitted, carrying the source
   route alone.
5. No event carries a personal identifier, a full address, an email address or free text.

### Failure, empty and offline surfaces

1. **Every failure surface renders the same chrome, the same scene and the same footer as a working
   route.** There is no bare error page, because a studio that sells production values cannot ship
   one.
2. An address matching no route answers not found and renders the error view with the headline
   `That page has moved on.` and an action reading `See all projects`.
3. A retired path resolves permanently and in one hop to its project. Three are seeded:
   `/cases/lambert-vitrine` and `/cases/vitrine` resolve to `lambert-vitrine`, and `/cases/grale`
   resolves to `grale`. A retired path whose target has been unpublished resolves to `/projects`
   rather than to an error. Distinguishing a retired path from a path that never existed is the
   difference between keeping and losing a decade of inbound links.
4. A server failure renders from a statically hosted document with no content query of its own,
   carrying the headline `Something is temporarily out of reach.` and a retry control reading
   `Try again`. An error page that depends on the system that just failed is an error page that
   also fails.
5. With no connection the shell renders from a cached copy with the line
   `You are offline. The pages you have already opened are still here.` and every route already
   opened remains reachable.
6. A failed rebuild leaves the previous site standing.
7. A missing media renders its reserved box at the right shape with a generated placeholder, so
   nothing shifts.
8. A block the content interface cannot resolve is skipped, the rest of the body renders, and the
   failure is reported. A single bad block must never blank a case study.
9. Everywhere a surface would be empty, the control that opens it is not rendered rather than
   rendered opening nothing.

### What the browser downloads

1. **No credential, API key, content host, store key or token appears in anything the browser
   downloads**: not in a document, not in a script, not in a style sheet, not in a comment and not
   in an inline configuration object.
2. Every response carries the standard security headers, including a strict transport policy with a
   long age, a nosniff content type policy, a frame ancestors refusal, a strict origin when cross
   origin referrer policy, a same origin cross origin opener policy, and a permissions policy
   denying camera, microphone, geolocation and payment.
3. The content security policy enumerates every permitted connection target rather than wildcarding
   one, permits no inline script without a nonce, and names a report endpoint, so a tag added
   outside the review process is visible rather than merely blocked.
4. **No third party script, pixel, frame or beacon loads before an explicit affirmative consent.**
   The consent interface offers accept and reject with equal prominence, records the decision with
   an instant and a policy version, and is reopenable from the footer. Consent gates loading, not
   firing: a build that loads a tag and then tells it not to send has already handed over the
   visitor's address.
5. Withdrawing consent deletes the client state that category created and stops all further sending
   within the same page view, without a reload. A global privacy control signal is honoured as a
   rejection without a prompt.
6. A privacy notice lives at `/privacy`, is linked from the footer and from the consent interface,
   names every processor, states the single data class and its retention, and is versioned so the
   consent record can reference the version that was shown.
7. Every form field validates inline, names the field that failed, and writes nothing on a refusal.
8. The sitemap at `/sitemap.xml` lists every published public route and no unpublished one, and
   `/robots.txt` names the sitemap and refuses the preview route.

## User flow

There is no persistent menu. The public showcase carries exactly one contextual navigation control
in the top centre of the window, whose label depends on where the visitor is, and every other
destination is reached from the footer or from the content itself.

| Route | Purpose | Auth |
|---|---|---|
| `/` | The home reel: the opening statement, the curated entries, the footer | public |
| `/projects` | The full index of published case studies | public |
| `/projects/lambert-vitrine` | One case study | public |
| `/projects/aurel-vance-experience` | One case study | public |
| `/projects/verrine-end-of-year-23` | One case study, with no live address | public |
| `/projects/grale` | One case study | public |
| `/projects/lambert-vitrine/backstage` | The behind the scenes reel overlay, its own history entry | public |
| `/about-us` | The studio story, a numbered chapter list | public |
| `/about-us/where-we-started` | One studio chapter, one scene | public |
| `/about-us/how-we-work` | One studio chapter | public |
| `/about-us/what-we-refuse` | One studio chapter | public |
| `/about-us/the-people` | One studio chapter | public |
| `/about-us/the-craft` | One studio chapter | public |
| `/about-us/the-studio` | One studio chapter, marked by the studio mark | public |
| `/privacy` | The privacy notice | public |
| `/preview` | The draft reader, resolved by token | preview token |
| `/console/sign-in` | The console sign in | public |
| `/console` | The console home and its collection lists | `producer` |
| `/console/projects/marivella` | The record editor | `producer` |
| `/console/media` | The media library | `producer` |
| `/console/reel` | The home reel order editor | `editor` |
| `/console/publish-log` | The publish log | `producer` |
| `/sitemap.xml` | Every published public route | public |
| `/robots.txt` | Names the sitemap, refuses the preview route | public |
| anything unmatched | Not found, answering not found | public |

The navigation control reads `About` on the home route and leads to the studio page. On every
other public route it reads `Back`, expanding on hover to `Back to Home`, and leads to the home
reel. On a chapter it becomes a previous and a next control, wrapping at both ends. Whatever the
visual treatment, the control is a real link with a real destination in its markup before any
script runs, and its accessible name is the expanded form rather than the truncated one: a control
whose accessible name is `Back` tells a screen reader nothing about where back is.

Three surfaces look like routes and are not: the behind the scenes reel, which is an overlay that
does push a history entry because it is a distinct piece of content; the full window video player,
which is an overlay and does not; and the mailing list panel, which is a state flag on the footer.

**Entry and redirects.** An anonymous caller reaching any `/console` route is sent to
`/console/sign-in` and returned to the route asked for once signed in. Signing out returns to `/`.
A `producer` reaching `/console/reel` is refused rather than shown a read-only copy. A token that
expires during an edit leaves the typed body in place and offers sign in again. A preview address
carrying no token, an expired token or a revoked token answers not found. A retired path resolves
permanently in one hop.

**Journeys.**

1. **Fall through the reel.** Open `/`. The loader counts a real fraction to completion and the
   four opening words arrive one at a time with `Scroll down` beside them. Scroll: the entries
   drift against their masks, and a hard flick pulls the camera back, blows the titles up and drops
   every interface control. Activate the first entry, `Lambert Vitrine`. The pointer label reads a
   loading state, the case study resolves, and the route changes without the scene remounting.
2. **Read a case study.** On `/projects/lambert-vitrine` read the headline, the discipline row and
   the three actions. Follow `Launch website`: it opens in a new context and one outbound click row
   exists for that slug afterwards, and no order, invoice or conversion row exists anywhere.
3. **Play the backstage reel.** Press `See backstage`. The overlay opens, its subtitles render by
   default, a drag scrubs it and the narration follows. Press the escape key: focus returns to the
   `See backstage` control and the route is the case study again.
4. **Leave an address.** Open the footer panel, type an address, submit. The confirmation names the
   address submitted and stays until the panel is closed. Submit the same address again: the same
   response comes back, saying nothing about whether it was already stored.
5. **Write and fail to publish.** Sign in at `/console/sign-in` as `producer@example.com` with
   `deku-demo-pw-2026`. Open `/console/projects/marivella`, edit a block, mint a preview token and
   open it in a fresh context: the draft reads. Attempt to move the record to `published`: refused,
   and the record is still `in_review` afterwards.
6. **Publish.** Sign in as `editor@example.com`. Move `marivella` to `published`. The index now
   carries seventeen entries, the publish log carries a new row naming the routes invalidated, and the
   preview token minted in journey five now answers not found.
7. **Be stopped by the gate.** As the editor, attempt to publish `oryx7`. Refused, and the refusal
   names the media that is still deriving. Attempt to store a reel section carrying audio and no
   subtitle: refused at the storage layer.
8. **Miss.** Open an address that matches no route: the error view renders with the headline
   `That page has moved on.` and the response says not found. Open `/cases/lambert-vitrine`: it
   resolves permanently, in one hop, to `/projects/lambert-vitrine`.

**States.** Every listing carries an empty state and a loading state. The home reel with nothing
published renders the opening statement and the footer and collapses the reel region without an
error. The index with nothing published renders its one line of copy. A case study with no blocks
renders its headline and its actions. A chapter whose record is not published renders as text
without a control. A media that failed to derive renders its reserved box and a generated
placeholder at the right shape. A loader that receives no progress offers the lighter scene with
the line `This is taking longer than it should.` and a control reading
`Continue with the lighter version`. Every form message renders beside the field it belongs to, in
words rather than by a change of border colour alone, and a refusal leaves everything else typed.

## UI/UX notes

**North star.** Somebody arriving should feel, before they have read a word, that this studio can
build the thing they came to commission. The site is the portfolio, not a description of one.

**Register.** Editorial and expressive on the public side: one continuous lit world, almost no
interface, and every colour on the page coming out of the work itself. The console inverts that
deliberately, because a person doing repeated editorial work wants density, stable positions and
no atmosphere at all. Build both and do not unify them.

**Restraint over decoration.** The interface says almost nothing so that the work can say
everything. **Weight over speed.** Movement arrives slowly and leaves quickly, so the site reads as
considered rather than nervous. **Continuity over transition.** The world behind the words never
goes away, which is what lets one page stop existing and another begin without a cross fade.

**Colour.** The interface is achromatic, and that is a thesis rather than a restriction. Two
values carry the whole product: a near-black neutral and a warm near-white neutral. Everything that
looks like colour comes out of the scene layer and the case study media, never out of the
interface. Three further neutral roles exist and are used almost nowhere: a pure near-white as the
clear colour behind the home view, a pure near-black as the clear colour on a dark view and behind
the video, and a mid neutral for the fast scroll rail alone. A build that introduces a hue into the
interface has reproduced none of this. The exact values are yours, so long as the two carrying
values hold WCAG AA contrast against each other in both directions and no third hue appears in any
interface surface.

**Opacity is the design system.** Because there is no hue to work with, faintness carries meaning,
and there are exactly nine levels each with one job: full for the selected, the active and the
hovered rule; a hover level for any control under the pointer; a secondary level for the type
column, the address and the progress bar at rest; a hidden level for the pointer dot over a control
that owns its own cursor and for a disabled submit; a progress level for the scrubber gutter under
the pointer; a rail level for the loader rail; a gutter level for the scrubber gutter at rest; a
dimmed level for an unselected row while a sibling is hovered; and zero for everything before its
reveal. A tenth level breaks the grammar. The levels themselves are yours; the count and the
one-job-each rule are not.

**The signature interaction.** On the project index, pointing at a row makes **nothing brighten**.
The row stays exactly where it was and every other row recedes, and a hairline grows in under the
name being pointed at. The recovery is about twice as slow as the dimming, so a pointer sweeping
down the list leaves a soft wake rather than a strobe. That inversion is the clearest statement of
the whole design, and a build that highlights the hovered row instead has inverted the thesis.

**Type.** Three faces, one weight each, and one of them is used in exactly one place. `EB Garamond`
is the transitional serif with old style figures, and it carries every title, every index entry and
the loader figure. `Archivo` is the neo grotesque and carries every piece of interface text.
`Archivo Light` carries the mailing list input and nothing else, so a visitor who never opens that
panel never downloads it. Both families declare a swap behaviour and a metrically compatible
fallback, because the loader figure counts up from the first frame and a swap that shifts its width
mid count is visible. Display type is proportional to the window until the window becomes very
wide and then stops; interface text never scales at all, because a wider screen is not a reason to
read bigger words.

**Shape.** One radius exists in the whole product and it is fully round, on the pointer dot, the
scroll dots and the sound dial dot. Every rectangular thing, every media block, every input and
every panel, is square. There is one round thing and it is repeated.

**Motion.** Three families of curve and seven named ones, registered once and referred to by name
from the document and from the scene alike, so a link and a camera and a piece of type share one
sense of weight. One ease carries every fade and every state cross fade in the interface. A second
carries anything that arrives and stops. A third carries anything that leaves quickly and
decelerates hard. Things arrive slowly and leave fast: a phrase assembles word by word from the
front over a long tail and unravels from the back in a fifth of the time. Scrolling downward and
scrolling upward use different curves, and the downward one overshoots slightly and drifts back
while the upward one does not, which is where the sense of weight comes from. Exactly one repeating animation exists in the product, a
marquee; it pauses when the tab is hidden and does not run at all under a reduced motion
preference. Under the same preference every scroll driven camera move becomes a cut at the same
stops, every word and character reveal resolves immediately to its end state, the fluid response
holds its rest state, the sound dial stops turning, and the loader keeps counting, because that is
information rather than decoration. The scene itself is not disabled: a reduced motion preference
is a request to stop things moving that the visitor did not ask to move, not a request to delete
the product. The exact speeds and curves are yours, so long as the three families stay distinct and
nothing uses a fourth to feel special.

**The page transition.** The outgoing page leaves instantly and the incoming one arrives slowly, so
the two never cross fade. The continuity is carried entirely by the scene, which does not unmount.

**Accessibility.** This shape of product is the one most likely to leave people out, so the bars
are specific. The single most important one: a case study headline is drawn inside the scene from
glyph geometry, which means it is not text, so the document must carry the same string as real text
available to assistive technology and to a text search, and the scene's rendering is treated as
decoration. A skip link is first in tab order on every route and moves focus to the main landmark,
which on a page whose scrolling is synthetic is the only way past the chrome without a pointer.
Every control is reachable by keyboard in document order with a visible focus indicator that is not
the pointer dot, and a focus move never moves the pointer dot. The virtual scroller binds the space
bar, the page keys, the arrow keys, the home key and the end key by hand, because it replaced the
behaviour that provided them. Every overlay traps focus while open, restores it to the control that
opened it on close, closes on the escape key, and carries a role and an accessible name. No control
requires a drag as its only input. Every icon carries an accessible name or is hidden from
assistive technology, and exactly one vector carries meaning, the wordmark, whose label is the
studio name. Body text holds WCAG AA contrast; the faint levels are permitted only where they are
never the sole indicator of anything, and the index dimming is reinforcement while the hairline is
the primary indicator. Under a forced colours preference every hairline rule and every input
boundary takes a system colour rather than disappearing. Touch targets are comfortably sized and
meaning is never carried by colour alone.

**Responsive.** Five layout stops and no more; everything else that looks like a breakpoint is the
type scale doing arithmetic and must be generated rather than hand written. The layout holds at
every width between the stops and nothing overflows sideways at a phone width. On a coarse pointer
the pointer dot, its labels, the index dimming, the index preview and every hover sound are all
absent, and **no action may exist only as a hover**: the clipboard copy, the preview media and the
backstage control each have a tap equivalent, and the first additionally has a real mail link. The
graphics tier decides which scene a visitor gets, not the window width, so a narrow window on a
workstation gets the full scene and a wide window on a low power laptop does not.

**What it must not look like.** Not a conventional portfolio grid: no thumbnail wall, no filter
chips, no card with a hover lift. Not a marketing landing page: no hero carousel, no testimonial
band, no logo wall, no cookie banner that pushes the page down. And not a house style wearing this
palette: if the scene, the achromatic interface and the dimming inversion were removed and the
result still read as this studio, the character was never built.

## Technical requirements

The application is server rendered. Every public route is a prerendered document resolved at
publish time from the content model, and the copy, the alternative text, the discipline tags and
the outbound link of a case study are present in the served document before any script executes. A
visitor on a slow connection, a crawler and a reader with scripting disabled all get the whole
page. The scene is an enhancement over that document and never a precondition for it, and no scene
resource may be a render blocking request.

Stack: Django serving its own templates on the backend, with progressive enhancement in the browser
and no client side framework. Storage is `postgres`, reached at `DATABASE_URL`, which is also
published as `DB_URL` with the same value. Object storage is `minio`, reached at
`STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`.
Authentication is email and password held by this app for the console only, with a bearer token
the client sends on authenticated calls and passwords stored hashed. `GET /api/health` returns
`200` once the app is ready. Requests are logged to stdout, structured, carrying a level, a
correlation identifier, an actor where one exists and a route or job name, and carrying no personal
data; log volume is bounded per request so a loop cannot fill the store.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing services
available in this environment are `postgres` and `minio`, and reaching for anything else is a
contract violation.

Read every address, port, bucket name and credential from the environment. Never hardcode a host, a
port, a bucket or a key for any backing service, and never hardcode `APP_PUBLIC_URL` or
`APP_PUBLIC_PORT`.

Four layers, and the boundary between the third and the fourth is the whole architecture. The
content layer owns the queries, the types and the normalisation and knows about the content model
only. The document layer owns the routes, the components and the interface state and knows about
content and the design tokens. The scene layer owns the views, the components, the resources and
the renderer and knows about the design tokens and a scroll offset. The bridge is the only place
the last two meet, and it carries four operations and nothing else: show a view with its identifier
and its document references, report loaded and ready and progress, publish the scroll offset and
the pointer position for the frame, and publish the interface state fields the scene consumes.
Neither layer may reach into the other. A global handle on the scene application means every
component in the document can mutate the render loop, and there is no way to reason about a frame
after that.

The order within a frame is fixed and explicit: resolve input, integrate the virtual offset, apply
the document transform, publish the offset and the pointer, update the scene, render. A build where
the scene reads the offset before the document has applied it has a one frame lag between the copy
and the world behind it, and on this product that is visible.

One interface state store with a small, named field set, every field having a named consumer: the
window size, the background colour with its dark flag and its transition flag, the open overlay
with its payload, the audio muted flag, the pointer state, the navigation control type, the footer
in view flag, the footer bottom reached flag, the fast scroll flag, the first scroll flag, the
interface hovered flag, the list panel open flag and the loader visible flag. A rebuild should not
exceed it.

The document root carries, set before first paint, exactly three facts: whether the pointer is
coarse, whether reduced motion is requested, and which graphics tier the scene resolved to.
**The browser name and the browser version are not among them.** Writing them is a fingerprinting
surface with no consumer that a pointer or a feature query cannot serve, and this product must not
collect it.

The graphics tier is resolved once, from a bundled benchmark table rather than from a fetch, before
the resource manager starts, and its result is written to the root so that the scene and the
interface branch on one value. Putting a third party origin in the critical path of the first scene
frame is not permitted. The tier is overridable by a stored preference so a visitor whose device is
misclassified can choose the other path.

Modules load per route. The current view's scene resources load after first paint at low priority;
every other view's load on demand. No audio object is created and no audio file is requested until
the visitor enables sound. Video is never preloaded and the poster stands in its place. The light
cut of the grotesque loads only when the mailing list panel opens. Reel media load on opening the
reel and never before.

Performance obligations, all of them requirements rather than aspirations, because the product's
whole commercial argument is that it feels expensive and runs smoothly. The served document stays
small enough to arrive in one round trip. First contentful paint lands inside a second and a half
on a mid tier connection and the largest contentful paint inside two and a half. Cumulative layout
shift stays near zero, achieved structurally rather than by tuning: every media carries its
intrinsic dimensions in the content model and every rendered box declares its ratio before the file
arrives, every font declares a metrically compatible fallback, nothing is inserted above existing
content after first paint, and the consent interface is an overlay rather than a banner that pushes
the page. Interaction to next paint stays under the interactive bar. The scene reaches its first
frame inside the agreed budget on the reference tier, and the frame budget holds while scrolling.
A regression in any of these blocks a deploy, measured on the five route kinds at three widths.

Runtime hygiene, each one a real pattern rather than a style preference. Layer promotion is set
around a move and cleared after, never left declared, because dozens of media planes promoted at
once on the reel will exhaust texture memory. Interpolation is frame rate independent, so the site
does not feel different on a high refresh display, which on a studio portfolio means the machines
art directors use. Rectangles are measured against the virtual scroller's own offset rather than
against the document, and cached across a frame rather than read per element. Split text is
reverted on unmount and never left in the document. Timelines are killed on unmount and on being
superseded. Scene resources are disposed by name on view unmount. **A route change returns the heap
to within a bounded delta of its state before that route**: a portfolio is walked through fifteen
entries in a sitting, and a leak per navigation is a crash.

The scene hosts a fixed set of registered views, one per route kind plus a second identical case
study view. That second view exists so that a move from one case study to another can build the
incoming scene while the outgoing one is still rendering. The two alternate rather than swap, so a
third consecutive navigation reuses the first, whose resources have been released by then; a build
that keeps allocating views leaks a scene per navigation. Shaders are compiled before a view is
shown rather than on its first frame, because revealing first drops frames on every route change.
A view declares its own resource list with a fallback keyed on a coarse pointer or a low tier,
resolved to the same internal name so the scene graph is written against one name and the tier
decision happens once. A failed resource never stalls the loader: each item carries a timeout and a
substitution, a failed model resolves to its lower detail variant and a failed texture to a
generated one.

The renderer handles a lost graphics context: on loss it stops the render loop, marks every
resource invalid and shows the document content at full opacity over a static ground; on restore it
rebuilds the renderer, reloads the current view's resources and fades the scene back in over the
same duration as a normal view show. The visitor never sees a blank canvas and the document stays
readable throughout.

Every outbound call to a backing service has a timeout shorter than the caller's own budget and a
circuit breaker, every credential is server side and rotatable without a deploy, and no backing
service sits in the critical path of a page render, because every public route is already rendered.

Every inbound webhook verifies a signature over the raw body before parsing it, with a constant
time comparison and a timestamp inside the signed payload rejected outside a short window, and is
idempotent on the sender's own event identifier. An unsigned webhook endpoint is a public write
interface. A handler acknowledges within the sender's timeout and does the work on a queue.

Background work runs on three primitives and choosing the right one is most of it: a durable queue
with retries for media derivation and outbound events, a scheduled trigger for the publish
scheduler and the retention passes, and a single long running build request for the site rebuild.
Build requests arriving while a build is running are coalesced into one follow up build, so an
editor publishing six case studies in a minute produces two builds rather than six and the second
reflects all six. The scheduler takes a short lease on each record it processes so two instances
cannot publish the same record twice, and a record whose scheduled time passed while the scheduler
was down is published on the next run with the actual time recorded alongside the scheduled one,
never skipped. Retention passes delete unconfirmed subscribers past their window, publish log rows
past two years, expired preview tokens, expired sessions, orphaned renditions after a grace period,
and non live scene configurations older than a year keeping the last ten per view.

### Operations, governance and observability

**Conventions.** One naming convention runs through the whole system, and the tier classification
the scene resolves to is the only capability flag anything branches on.

**Caching, delivery and invalidation.** Static documents and immutable media, served from an edge,
with no request time content query on any public route. The prerender manifest is resolved at
build time from the content model and carries every published route, the not found document, the
server error document and one redirect rule per retired path. A prerendered document is not stored
in the browser and is revalidated at the edge; an immutable content addressed rendition, a hashed
bundle and a web font are each held for a year; the intake response and the preview route are
never stored. Invalidation is computed from the dependency table rather than applied site wide as
a shortcut, and rendering and invalidation are ordered: the rendered document reaches the origin
before the edge key is purged, because purging first opens a window in which the edge fetches and
caches the old document. Media renditions are never invalidated, because they are never
overwritten. The edge serves stale content while revalidating and on an origin error, with an
outer bound, which is what leaves the previous site standing when a build fails. Transport is
encrypted only with a strict policy including subdomains, the protocol is multiplexed so a route
pulling forty small textures is not queued, text is compressed with a negotiated modern algorithm,
and media are never recompressed at the edge because the pipeline produced the final bytes.

**Scheduling.** A record may carry a scheduled publish time, indexed so the scheduler is a cheap
query rather than a scan, because a case study for a client launch is embargoed until the client's
own launch and the studio must not have to be awake for it. A scheduled publish that fires while
the store is unavailable retries with backoff and alerts on exhausting its retries: a silent
missed embargo is a client relationship problem, not a software one.

**Concurrent editing.** A record carries a version and a save carrying a stale version is rejected
as a conflict rather than applied, and the console shows who else has the record open. At this
team size a full collaborative editor is not warranted; a lost update is.

**Versioning.** The intake carries a version in its path, the content queries are versioned by the
model's own migrations, and a scene configuration payload carries a schema version. A payload
whose version the running scene does not recognise is ignored entirely in favour of the code
default rather than applied partially, because a half applied configuration is a scene that looks
subtly wrong in a way nobody can reproduce. A configuration is fetched at scene start with a short
timeout and a hard fallback to the code default, so a slow store is never an availability
dependency, and promoting one takes effect immediately without a rebuild, which makes the fastest
revert in the whole system an art direction revert.

**What talks to what.** Three inbound events and two outbound. Inbound: a content record changed,
a message bounced or was complained about, and a build finished. Outbound: a record was published,
and a media derivation failed. Receiving one verifies its signature and its timestamp before
parsing and is idempotent on the sender's own event identifier, because providers retry. A hard
bounce moves a subscriber to bounced and it is never sent to again; three soft bounces within a
window do the same; **a complaint moves a subscriber to unsubscribed immediately and permanently,
with no confirmation and no resubscription without an explicit new opt in**, because ignoring
complaints is how a studio loses its ability to send anything at all. Every outbound event carries
a version, an identifier, an instant and a payload, is delivered at least once with backoff, and
is written in the same transaction as the state change it describes so that it is not lost when
the process dies between the two.

**Notifications.** The studio hears about a record published, a scheduled publish fired, a
scheduled publish failed after its retries, a build failed, a derivation failed permanently, the
intake error rate crossing its threshold, and the origin serving stale beyond its bound. To an
individual, only failures and account changes leave the console: an upload that finished deriving
and a record published by somebody else are shown in the console alone, while an upload that
failed, a role change and a deactivation are sent. A studio of six people that is mailed about
every success filters that mailbox. Every notification is enqueued rather than sent inline, is
deduplicated on an event key, and degrades silently: one that cannot be delivered is logged and
never blocks the operation that produced it.

**Referential integrity.** A home reel entry whose project is unpublished is dropped from the
rendered reel and the editor is warned before the unpublish. A studio section whose chapter is
unpublished renders as text without a control. A project whose reel is unpublished renders no
backstage control. A project's next link is resolved at build time from the live index order so it
cannot dangle. A block's media cannot be deleted while any record references it.

**The captioning rule, restated.** It appears three times and it is one rule: audio without a
transcript cannot be published. It is enforced as a storage constraint on the reel section, as a
cross record rule in the publish gate for video, and as a field level requirement in the console.
Three layers, because this is the rule most likely to be worked around under deadline.

**Data governance.** One class of personal data exists, in one table: a subscriber's address, the
route they gave it on, and the instants of their consent and confirmation. The lawful basis is
consent, given by submitting, with the consent text version stored. Retention: a confirmed
subscriber until they unsubscribe and then a suppression record only; an unconfirmed subscriber
deleted at the end of the confirmation window; a suppression record indefinitely, holding a hash
of the address and nothing else, which is what lets the studio refuse to add it again by accident
and is a narrower retention than keeping the address; the publish log two years; sessions until
expiry; operational logs thirty days; and aggregated performance data thirteen months.
**Pseudonymisation**: where an identifier must be retained for a security or operational purpose
rather than a contact purpose it is stored as a keyed hash rather than as the value, which applies
to the agent string and the address on a session record and to any correlation of a subscriber in
a log line.

**What must not be collected**, absent entirely rather than merely unused: a visitor identifier of
any kind on the public site; the browser name and version written to the document root; an address
logged with an analytics event; and any field beyond the address on the intake.

**Subject rights.** Because there is exactly one table and exactly one field, every right is a
single operation. Access is a request to the studio mailbox answered with one row. Erasure is the
unsubscribe link itself, performed immediately with no sign in, leaving only the suppression hash.
Rectification is an unsubscribe and a resubscribe. Portability is one row on request. Objection is
the unsubscribe link. A privacy notice names every processor, states the single data class and its
retention, and is versioned so a consent record can reference the version that was shown.

**Observability and failure handling.** What is instrumented: the public site's field performance
and its client errors; the build's duration, outcome, routes rendered and invalidation set; the
derivation queue's depth, oldest item age, failure rate and dead letter count; the scheduler's lag
between scheduled and actual; the intake's rate, acceptance rate, rate limit rate and error rate;
the webhooks' receipt rate, signature failure rate and duplicate rate; and the edge's hit ratio,
stale served rate and origin error rate. Uncaught errors, unhandled rejections and graphics
context losses are reported with a stack, a route, a tier and a release identifier, carrying no
personal data, sampled, and gated behind the measurement consent. A graphics context loss is
reported as its own signal rather than as an error, because its rate by tier is the number that
decides whether the reduced scene's threshold is set correctly. Every request carries a
correlation identifier propagated through the queue and into every log line and every outbound
event.

**Alerts**, nine and no more, because a studio of six people that gets thirty alerts a day reads
none of them: a build failure; a scheduled publish missed after retries; a derivation dead letter;
a derivation queue whose oldest item is older than an hour; an intake error rate above a small
share over a short window; an intake volume above a multiple of its trailing baseline, which is
the abuse signal; an edge origin error rate above a small share; stale served beyond its bound;
and a regression in the scene's first frame time by tier. Anything below these thresholds belongs
on a dashboard rather than in a notification.

**The failure playbook.** A content store that is down leaves the live site unaffected and blocks
publishing. A failed build leaves the previous deploy standing and the queue coalesces the retry.
**A build that succeeds with the wrong content is reverted by redeploying the previous build**,
which is possible because the manifest is deterministic, and then republished from corrected
content. A degraded edge serves stale. A stuck derivation queue publishes nothing and leaves media
deriving until it is drained and its dead letter inspected. A configuration promotion that looks
wrong is reverted by promoting the previous one, with no rebuild. Suspected leaked credentials are
rotated wholesale and every session and preview token revoked.

**The principle underneath all of it**: every failure surface renders the same chrome, the same
scene and the same footer as a working route, and **resilience** is a property of the architecture
rather than a set of guards bolted on afterwards. The build order follows from the same principle
and runs in phases: the content model and the console first, then the media pipeline, then the
build and the publish workflow, then the design system and every route as a static layout, then
the scroller and the motion, then the scene and its views one at a time, and finally the intake,
the consent and the accessibility, performance and observability passes. What can be **deferred**
is the reduced scene until the scene views exist, the scheduler, the second curated project list
and the chapter scenes beyond the first. What can never be deferred is the captioning constraint,
because adding it later means auditing every existing record; the credential separation, because a
credential in a bundle is disclosed the moment it ships; the intrinsic dimensions, because they
are captured at upload and adding them later means reprocessing every master; the slug
immutability, because the redirect table has to exist before the first slug is ever changed; and
the consent gate, because shipping without it means the earliest visitors were tracked without
consent.

**Budgets, stated as sizes.** The served document stays at or under forty kilobytes compressed and
the initial script at or under a hundred and fifty kilobytes compressed. The document, the
critical style and the two fonts are the only blocking stage; the initial script is deferred; the
tier resolution, the current view's resources and the visible media blocks' resources all follow
without blocking; and the light font cut, the audio and the video load only on the action that
needs each.

## Data model

Twenty one tables. All timestamps are UTC, absolute and zone aware, never a local time. Identifiers
are opaque and sortable by creation and are never sequential integers on an externally visible
surface. Enumerations are constrained at the database level rather than held as free strings.
Foreign keys are declared with explicit behaviour on delete. Records are unpublished rather than
deleted; media deletion is real.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not
a secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`projects`** - `slug` unique and immutable after a first publish; `title`; `type`, one of
`Web Experience`, `Corporate`, `E-Shop`; `description`; `live_url`, nullable; `state`, one of
`draft`, `in_review`, `published`, `unpublished`; `first_published_at` nullable; `published_at`
nullable; `version`; `created_by`; `updated_by`; `created_at`; `updated_at`. Eighteen rows.

**`disciplines`** - `key` unique; `label`; `position`. Ten rows, the controlled vocabulary.

**`project_disciplines`** - `project_slug`; `discipline_key`; `position`. A project's discipline
list, many to many, so a term can be renamed once and everywhere.

**`project_retired_paths`** - `path`, unique and the primary key; `project_slug`. Three rows. The
primary key on the path is what makes a collision unstorable rather than merely refused.

**`blocks`** - `id`; `owner_type`, one of `project`, `chapter`; `owner_slug`; `position`; `kind`,
one of `hero`, `text`, `media`, `split_media`, `image_push`; `payload`. Polymorphic over its owner,
because a block belongs to a project or to a chapter and the two are otherwise unrelated. The
payload is structured rather than free and is validated against the schema for its kind on write, so
a payload failing its schema is rejected rather than accepted and rendered defensively.

**`block_media`** - `block_id`; `position`; `media_id`; `width_step`; `placement`, one of centred,
centre left, centre right, left then right, right then left; `margin_step`; `offset_y`; `legend`
nullable; `alt_text` nullable; `decorative`; `preview_media_id` nullable. A media element carries
its own intrinsic width and height through its media record, which is what lets the document
reserve the exact box before a byte arrives.

**`chapters`** - `slug` unique; `title`; `number_label`, text rather than an integer because the
sixth is the studio mark and not a numeral; `scene_index`, constrained to the registered scene
range; `state`; `first_published_at`; `published_at`; `version`. Six rows.

**`studio_sections`** - `position`; `number_label`; `title`; `description`; `cta_label`;
`chapter_slug` nullable. The studio page's ordered list, with the number stored rather than derived.

**`home_reel_entries`** - `position`; `project_slug`; `media_id`. Three rows. The reel's own media
is declared here rather than borrowed from the project's body.

**`reels`** - `project_slug` unique; `title`; `state`; `published_at`. One row, against
`lambert-vitrine`.

**`reel_sections`** - `reel_id`; `position`; `duration_ms`, a whole count of milliseconds rather
than a float of seconds because the timeline is summed and a float sum of twelve durations does not
equal the total a producer typed; `audio_media_id` nullable; `subtitle_media_id` nullable. Three
rows. **A row carrying an audio media and carrying no subtitle media cannot exist.** That
constraint is the single most useful one in the schema, because it turns an accessibility policy
into something no code path can bypass.

**`reel_section_media`** - `reel_section_id`; `position`; `media_id`; `scale`; `position_y`;
`intrinsic_width`; `intrinsic_height`.

**`media`** - `content_hash` unique; `original_name`; `mime`; `byte_size`; `intrinsic_width`;
`intrinsic_height`; `duration_ms` nullable; `state`, one of `uploaded`, `deriving`, `ready`,
`failed`; `uploaded_by`; `created_at`. The unique content hash means uploading the same file twice
produces one record, which on a portfolio where one client mark appears in nine case studies is a
real saving. Four rows, one of them still `deriving`.

**`media_renditions`** - `media_id`; `variant`, one of `placeholder`, `xs`, `sm`, `md`, `lg`, `xl`;
`format`; `width`; `height`; `byte_size`; `storage_key`. The triple of media, variant and format
appears at most once, which is the derivation idempotency expressed in the schema: enqueuing the
same derivation twice is a no operation rather than a duplicate.

**`accounts`** - `email` unique and compared without regard to case; `password_hash`;
`display_name`; `role`, one of `producer`, `editor`; `state`; `last_used_at`; `created_at`. Three
rows.

**`preview_tokens`** - `token_hash`; `record_type`; `record_slug`; `issued_by`; `issued_at`;
`expires_at`; `revoked_at` nullable. The hash is stored and never the token, because a database dump
must not be a set of working preview links. One row, against `marivella`.

**`publish_log`** - `occurred_at`; `actor_account_id`, stable after deactivation; `record_type`;
`record_slug`; `from_state`; `to_state`; `outcome`, one of succeeded, failed, partially applied;
`invalidated_routes`. Append only: no application path removes a row.

**`subscribers`** - `email_normalised` unique; `email_display`; `state`, one of `pending`,
`confirmed`, `unsubscribed`, `bounced`; `source_route`; `consent_text_version`; `consent_at`;
`confirmed_at` nullable; `confirmation_token_hash` nullable; `confirmation_expires_at`. The unique
constraint on the normalised address is what makes the intake idempotent for free: a resubmission
is an upsert that changes nothing and returns the same response. This is the only table in the
product holding personal data.

**`outbound_clicks`** - `project_slug`; `occurred_at`. One row per follow of a case study's
live address, carrying nothing identifying: no visitor identifier, no address, no free text, and
no outcome, because the studio never learns what happened at the other end. Empty at seed.

**`sessions`** - `account_id`; `token_hash`; `issued_at`; `expires_at`; `revoked_at` nullable;
`agent_hash`; `source_hash`. The agent string and the source address are stored as keyed hashes
rather than as values, which is the pseudonymisation rule applied to the one record that has an
operational reason to keep them. Empty at seed.

**`scene_configs`** - `view_name`; `label`; `payload`; `created_by`; `created_at`; `is_live`. At
most one row per view carries `is_live`, which is what makes promoting one a single write rather
than a two step that can fail between the steps, and what makes reverting an art direction change
one action. Configurations are immutable once written: tuning produces new records and promotion
selects one.

Derived rather than stored: the reel's total duration, which is the sum of its section durations
computed on read; the index order, which is a stable sort on a normalising key rather than a stored
rank; a project's next link, resolved at build time from the live index order so it cannot dangle;
and the count of ready variants against expected on a media, shown in the console.

Seed data is exactly the catalogue in Core features, plus ten disciplines, six chapters with their
numerals, one reel of three sections against `lambert-vitrine`, three retired paths, one live
preview token against `marivella`, four media of which one is `deriving` and is referenced by
`oryx7`, and three accounts.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

### The design thesis

The interface is achromatic. Two values carry the entire product, one near-black neutral and one
warm near-white neutral, and everything that looks like colour comes out of the scene layer and the
case study media, never out of the interface. That is why the palette is four entries long and the
opacity scale is nine: the design's whole expressive range in flat interface terms is faintness,
not hue.

### Colour roles

Five neutral roles and no hue. The ink role is a near-black neutral and carries every glyph, every
hairline rule, the pointer dot and the dark backdrop; it is by a wide margin the most resolved value
in the product. The paper role is a warm near-white neutral and carries the page ground and every
glyph on a dark backdrop. An inverse ink role is a pure near-black neutral and is the scene clear
colour on a dark view and the video backdrop. A pure paper role is a pure near-white neutral and is
the scene clear colour on the home view alone. A muted ink role is a mid neutral and appears in
exactly one place, the fast scroll indicator rail.

Two further values exist in the reference and must not reach a visitor: a vivid amber and a light,
soft green that belong to a development panel stylesheet. A build that ships either has shipped its
debug tooling, and the tuning panel must be behind a dynamic import unreachable in a production
build so that it cannot happen.

The exact values are yours, so long as the ink and paper pair holds WCAG AA contrast in both
directions, the paper role reads as warm rather than neutral white, and no interface surface
anywhere carries a hue.

### The opacity scale

Nine levels, each with one fixed meaning, and a build that invents a tenth has broken the grammar.
Full carries the selected item, the active state and the hovered rule. A hover level carries any
interface control under the pointer and the loader hint on a pointer device. A secondary level
carries the project type column, the footer address and the progress bar at rest. A hidden level
carries the pointer dot over a control that owns its own cursor, and a disabled submit. A progress
level carries the video scrubber gutter under the pointer. A rail level carries the loader progress
rail. A gutter level carries the video scrubber gutter at rest. A dimmed level carries a project
type in the unselected state while a sibling is hovered. Zero carries every element before its
reveal, and it is the most resolved of all of them.

The pair at the secondary and the dimmed level is the whole interaction on the project index.

### The scaling law

One law generates every fluid size and width in the product, and it is declared once rather than
hand written per token. A display size is declared as a base size at a reference width, and then
expressed three ways: below the token's own floor width it is fixed at its floor size; between the
floor width and an upper stop it is expressed as a fraction of the viewport width derived from the
base; at or above the upper stop it is fixed at the base scaled by a constant factor. The upper
stop is the same for every token. The lower stop is derived per token from its own floor size, at
the width where the fluid value equals it.

**Interface text does not scale at all.** Every token marked fixed carries an identical declaration
above and below the reference width, pinning it to its base size at every width. That is a
deliberate second policy: display type is proportional to the window and the text you have to read
is not.

Widths obey the same law. The mailing list input's width is a fraction of the viewport, capped
above the upper stop and floored below its own floor width, and both stops fall out of the law
rather than being chosen.

The law is what makes sixteen measured breakpoints into five real ones. **Only five layout stops
are hand written**; every other width in the product is generated by the law, and sixteen hand
maintained breakpoints is a design system nobody can change.

### The type scale

Fourteen tokens, each with a base, a policy, a family and a role. Three carry the scene's own drawn
type at three sizes, and those three are the tell that the scene draws its own text: they are
resolved on hidden measuring nodes and were never visible in a screenshot. A hero size drives the
index preview media's sizing basis. A display large and a display medium carry the scene rendered
title at its largest camera distance and at its resting distance. A panel size carries the mailing
list input in the light cut. Three title sizes carry the case study headline, a text block lead and
a text block subhead. A loader size carries the progress figure. An entry size carries an index
entry title. Three body sizes carry a case study paragraph, a case study caption and a chapter
paragraph. An interface size carries every control, every label, the type column, the discipline
row and the validation line, and is the most used token that carries actual words. A small
interface size carries the pointer label.

The index entry title's line height is not a typographic value, it is a layout one: it collapses
the line box so that the underline rule sits where the design wants it rather than where the font's
descender would put it. A build that normalises that number to something sensible moves every
underline on the index.

### Layout

One grid on every route: twelve equal columns, a fixed gutter, a fluid row gap obeying the scaling
law, items aligned to the start of their row, a container maximum, and a side padding that steps
once at the tablet stop. Content is centred inside the maximum with automatic margins, and at the
widest layouts it sits as a column within substantial ground on both sides, which is deliberate
because the scene fills that ground.

The measured column vocabulary, which is the layout language of the whole product: the loader mark
takes a narrow span at the left, the loader figure and its rail take the centre, the loader hint
takes the right; an index entry's type column takes a narrow span right aligned within it and its
title takes the span to the right of that; the index preview media takes a span on the left; a list
row takes the full twelve. Below the tablet stop the index type column is hidden entirely and the
title takes the full width.

**The window is the container.** Every route reports a document height exactly equal to the window
height at every width, which means the document is one window tall and never grows. Three
consequences must be built in from the first commit rather than retrofitted: the scrolling element
is an inner container with its own overflow rather than the document; element positions for any
scroll driven effect are measured against that container's transform rather than against the
document; and anything that assumes the document scrolls is broken by default.

Seven stacking levels, and the gaps between them are as meaningful as the values: the scene canvas
and page content at the ground, anything that must sit over a media block just above it, the fast
scroll indicator above that, the contextual navigation control at the chrome level, the intro
loader above the chrome, the video overlay far above, and **the sound control above the video
overlay**. That last ordering is deliberate: a visitor who has just been given sound must be able
to take it away without closing anything first.

One hairline weight carries every underline, the loader rail and the video scrubber gutter and bar.
One radius exists and it is full, on the pointer dot, the scroll dots and the sound dial dot alone.
Everything rectangular is square.

**Every value above is declared once as a named token and consumed by reference.** A build that
inlines the ink value in forty components has made the dark variant impossible without touching
forty components. The dark variant is a token swap and nothing else: on a dark backdrop the ink and
paper roles exchange, and the loader ground, the loader text, the pointer colour, the sound control
colour, the underline rule and the scene clear colour all follow from that one exchange. No
component implements its own dark treatment, and the scene clear colour is animated in the same
frame from the same value as the page ground, because a page ground that swaps in one duration and
a scene that swaps in another produces a visible seam at the canvas edge on every route change.

### Iconography and the mark

Every icon is geometry, declared inline, tinted by the current text colour. There is no icon font
and no icon image. Two vector assets and three script drawn primitives are the entire set, which is
another way of saying the design does not use icons and uses type and dots instead.

**The wordmark** is a single vector: a shield glyph followed by the studio name set as letterform
outlines rather than as live text. The shield is the studio's standalone mark, an outline open at
the top whose sides curve inward to a rounded point at the bottom, with a vertical stem descending
the centre and a crossbar across it. It is a monogram locked into a shield silhouette. The
letterform advances give a tracking of roughly a third of an em, which is the wide spacing the mark
reads with. The wordmark has a minimum width that steps down once at the phone stop and otherwise
takes a fraction of its grid column.

**The mark reveal** is the most reused motion idea in the product. A gradient filled rectangle
three times the width of the mark, opaque for its first third and transparent for its last third,
is used as a mask and translated across the mark, which wipes the letters in from the left over one
mark width with a soft edge a third of a mark wide. **The reveal is driven by the loader's own
progress value rather than by a duration**, so a mark on a fast connection is not still wiping in
after the scene is ready.

**The sound dial** is two concentric stroked circles and a dot. The rest ring is hidden by default.
The active ring is fully undrawn at rest and animates its dash offset to zero, drawing itself
around like a slow clock hand, then rotates a full turn roughly every half minute for as long as
sound is on. The dot is a small full radius square that marks the muted state. The ring takes the
ink colour on a light ground and the paper colour on a dark one.

**The scroll dot cluster** is a set of absolutely positioned small full radius dots, one carrying a
default state at full opacity and one carrying an active state. The transitions are deliberately
asymmetric: a dot appearing takes a quarter of the time a dot becoming the active one takes, so the
indicator snaps on and settles slowly. On a fast scroll the cluster's rail takes the muted ink.

**The pointer dot** is two nested nodes, both fixed at the window origin and both parked off screen
until the first pointer move, one following the pointer directly and one following it with easing.
Both carry negative margins against their padding so their hit area is exactly zero. On a coarse
pointer both pin to the centre of the window and the label becomes static.

Exactly one vector carries meaning, the wordmark, whose accessible label is the studio name. The
shield, the dial, the dots and the rails are decorative and all are hidden from assistive
technology. No icon is an image file.

### Global chrome

Six elements mount once outside the routed content and survive every navigation, and nothing else
does: the scene canvas filling the window at the ground level on every route; the intro loader
filling the window above the chrome on first load only; the contextual navigation control fixed at
the top centre on every route after the loader; the sound control fixed at the bottom right on
every route; the pointer layer on pointer devices only; and the scroll indicator on pointer devices
only. The footer is not chrome: it is part of the routed content, it participates in the virtual
scroll, and it has a scene view of its own.

**The application shell** is three nested containers: the document root carrying platform and
capability state, the page ground carrying the ground colour, and the application container which
is the virtual scrolling element and is exactly window sized.

**The intro loader** is the first surface a visitor sees. It is a full window fixed layer above the
chrome that locks scrolling until the scene reports ready. It carries the ground, the wordmark at a
fraction of its column starting fully transparent until its wipe, a progress figure in the serif, a
progress rail beneath the figure at the rail opacity scaled from its left origin, a baseline of four
separately animated words, and a hint reading `Scroll down`.

**The loader must report real progress.** The rail is scaled from the resource manager's completed
byte fraction and the figure prints that same fraction. A loader that animates to nearly complete
and waits is the single most common way a site of this shape lies to a visitor about whether it is
working. **The loader must have a stall path**: if no resource completes within a bounded interval
it offers the reduced scene with the line `This is taking longer than it should.` and a control
reading `Continue with the lighter version`, and after a longer interval it takes that path
regardless of progress. It never sits on a fraction.

**The contextual navigation control** sits top centre and is one control whose label depends on the
route. Its structure is a default text node and two separately animated word nodes, which is what
makes the expansion a per word reveal rather than a text swap. It hides itself in two situations:
while the fast scroll state is active, and while a page has declared itself hidden.

### Motion

**Three families of curve**, and knowing which family a motion belongs to is most of getting it
right. An interface ease carries every fade, every opacity change and every state cross fade in the
interface layer, and it is by far the most declared. A settle ease carries anything that arrives
and stops: the video scrubber and its gutter. A lift ease carries anything that leaves quickly and
decelerates hard: an inline link.

**Seven named curves** are registered by name and referred to by that name from script, and they
are the studio's motion vocabulary: a transition in for something arriving, with almost no
acceleration and a very long tail; a transition out for something leaving, with a slightly slower
start and the same tail; a fast and a slow pair identical to those two and used by the scene layer;
a circle draw for the sound dial ring; and two parallax curves, one for the scene title's response
to scroll and one for a media block's. The two parallax curves overshoot downward before
recovering, which is what makes a media block appear to lag the scroll and then catch up rather
than tracking it linearly.

**The scroll timeline uses a different curve going down from going up**, and that asymmetry is the
reason the site feels like it has weight. Both downward scene curves carry a control point past
their end, which is an overshoot: scrolling down pushes the scene slightly past its target and lets
it come back. The camera curve is the identity, so the camera tracks scroll exactly while the scene
overshoots against it, and the parallax between them is generated by that difference rather than by
a multiplier. A narrow width carries its own downward curve.

**The duration ladder** carries six steps and they are ordered rather than measured here. The
fastest and most declared is a scroll dot appearing. Next is an inline link's colour and opacity.
Next is a page leaving and a project type dimming. Next is the default interface fade and the
pointer showing and hiding, which is the most common pair. Above that sits a colour and transform
pair, and the longest declared transition in the product is a slow atmospheric fade. Two
transitions carry a delayed visibility change, which is the standard technique for removing a faded
element from the hit testing surface only after it has finished fading.

**Exactly one keyframe animation exists in the whole product**, a marquee that translates a
duplicated list by half its own width plus one gutter so the seam is invisible. Everything else
that moves is driven from script or from scroll. The marquee pauses when the tab is hidden and does
not run at all under a reduced motion preference, because an infinitely repeating translation is
the single animation here that a vestibular sensitivity guideline names directly.

**The word reveal** is the most repeated motion idea. A text node is split into word spans, each
span offset and transparent, and the spans animate in on a stagger. The asymmetry is the whole
effect: words arrive slowly, from the front, over a long tail, and they leave in a fifth of the
time, from the back, so the phrase unravels rather than fading. The container recentres itself as
it grows by reading the measured width of the hidden expansion text. **The split must be non
destructive and reversible**, the accessible name of the control must be the whole phrase, and the
split spans must not be announced individually.

**One place splits by character rather than by word**, the sound control's hint reading
`Click to enable sound`, because per character splits are expensive and this one runs once. The
split must be hidden from assistive technology entirely and the original string exposed. The case
study headline also reveals per glyph, but through the scene rather than through a document split.

**The underline is the signature interaction.** A hairline rule under a control, scaled on the
horizontal axis, with the origin swapped between the two directions: it grows in from the left on
pointer enter and shrinks out to the right on pointer leave, so it travels in one direction across
two interactions. That origin swap is what makes it read as a wipe rather than a squash. It reveals
on entering the window with a short delay and retracts instantly on leaving. A mid flight reversal
guard is required: if the rule is already animating and its current scale is more than a hair from
the midpoint, the running timeline is killed and a fresh one starts from the current value rather
than from zero, which is what stops a rapid pointer sweep along a list producing a rule that snaps.
Alongside the scale, both the label and the rule ramp to the hover opacity. On the project index the
same idea runs at a faster tempo, with the origin right at rest and left on hover, and it is gated
behind a minimum width so it never runs on a touch device.

**The page transition** is asymmetric in the extreme: the leave is instantaneous and the enter is
slow, so the two documents never cross fade. The outgoing page is gone before the incoming one
starts, and the continuity across the transition is carried entirely by the scene, which does not
unmount. That is the architectural decision the whole product is built around.

### The virtual scroll system

**The page does not scroll.** Wheel, touch and key input are captured, integrated into a virtual
offset, smoothed, and applied as a translation on an inner container. The virtual scroller is not
optional and cannot be swapped for native scrolling, because the scene reads the same offset in the
same frame as the content and a native scroll cannot guarantee that. That seam is exactly what this
architecture exists to remove.

The scroller carries four parameters: a per frame interpolation factor toward the target offset, a
global speed multiplier, a delta multiplier converting one wheel notch into offset, and a separate
delta multiplier for the fast state. The interpolation factor is deliberately small, which produces
a very long tail and the drift after a flick. **The interpolation must be frame rate independent**,
converting a per frame factor into a per second one, because a raw per frame interpolation makes the
site feel different on a high refresh display, which on a studio portfolio means it feels wrong on
exactly the machines art directors use.

**The scroller does not have a speed, it has a state**, and three components read it. In the slow
state the camera sits at its resting zoom and the titles at their resting scale. In the fast state
the camera pulls back, the titles blow up to well over twice their size, and the interface hides.
Between them the values interpolate. Entering and leaving each state carries its own easing
parameters, and the asymmetry is deliberate and opposite in the two states: entering fast is easier
than leaving it, and leaving slow is easier than entering it, so the site is biased toward the calm
state. The pointer's own response in the fast state snaps out essentially instantly while taking a
full beat to enter.

**What the fast state changes**, read together: the camera pulls back, the scene titles scale up
against the global scale, the navigation control hides, the sound control hides, the pointer
indicator swaps to the fast rail in the muted ink, and the media parallax flattens, with the mask
factor and the vertical position factor dropping to nothing while the horizontal factor rises to
full. The reel reads as a single horizontal sweep rather than a set of layered planes. Scrolling
slowly does the opposite. It is one gesture with two entirely different visual results and it is
the most distinctive thing this product does.

**Four surfaces lock the scroller** and each must restore it exactly: the intro loader locks on
mount and releases when the scene reports ready; the video overlay and the behind the scenes reel
each lock on open and release on close, restoring the previous offset; the mailing list panel locks
on open and releases on close. **The lock must be reference counted**, because two overlays can be
open at once in this product, a video inside a reel, and a build that releases the lock when the
inner one closes drops the visitor back into a scrolling page underneath an open overlay.

**Six browser behaviours break because the page does not scroll, and each must be put back.** The
browser's own scroll restoration on a back navigation is disabled explicitly, the virtual offset is
persisted per route in memory, and it is restored before the first frame of the incoming view. A
fragment link is intercepted, its target resolved against the virtual container, and the virtual
offset animated. **Keyboard scrolling with the space bar, the page keys, the arrow keys, the home
key and the end key is bound explicitly**, with the same page and line increments a native scroller
would use; this is the row that gets forgotten and the one that fails an accessibility review
outright. A printed page gets a print stylesheet that releases the transform, unsets the fixed
positioning and lets the content flow. A visitor who has disabled script gets a complete document
with the transform never applied. Find in page is the one behaviour that cannot be restored: the
document carries every case study's full text so a search locates it, but the browser cannot bring
the match into view, and that is stated plainly rather than pretended away.

**On a touch device** the same virtual scroller captures the input, which means the momentum is the
studio's and not the platform's. The smoothing is reduced and the delta multiplier raised so a
flick travels a comparable distance to a native flick, and an overscroll at either end is clamped
rather than rubber banded, because a rubber band on a transformed container exposes the ground
behind it.

### The realtime scene layer

A single full window canvas at the ground level, mounted once, that never unmounts. It hosts a
registry of views, one renderer, one resource manager and one camera manager. Every route
corresponds to a view, and moving between routes shows and hides views inside one continuously
running scene rather than creating and destroying scenes.

The registry carries a home view bound to the home route; a studio view bound to the studio page; six
chapter views, one per chapter, none of them preloaded because a visitor reaches at most one; a
project view and a second identical project view for the case study to case study move; an index
view; a backstage view for the reel overlay; and a footer view that is on every route. Each view
declares its own class, its own configuration object and its own resource list with a preload policy.

**The view manager** holds one active view at a time, shown and hidden by timeline rather than by
mount and unmount, with a second view stackable over the active one for the reel. Showing a view
resolves its resources, creates its components, compiles its shaders and then runs the view's own
show timeline. Hiding runs the hide timeline and then releases view scoped resources but not shared
ones. Readiness is a two stage flag, loaded and then ready, so the interface can distinguish assets
having arrived from the first frame having been drawn.

**The home view** is the signature surface: a lit bas relief that the camera descends past, with the
case study reel laid out against it. The composer applies a bloom and no motion blur. The relief
declares a model with a lower detail variant for coarse pointers and low tiers, its own scroll
speed, and a camera with a deliberately shallow depth range, which is what lets the depth buffer
resolve the fine relief detail without banding; a rebuild that opens that range to be safe will get
depth artefacts across the whole relief. A scroll driven extrusion carries a noise size, a speed, a
mask range and a strength, and a chromatic mask carries a fresnel sharpness and opacity and a
shadow range and opacity.

**The fluid response** is the single most expensive thing in the product. Both the home relief and
the chapter scenes carry a pointer driven fluid simulation with a brush stage, an advection stage,
a pressure stage and an appearance stage, each carrying its own parameter group, the appearance
stage carrying separate red, green and blue coefficients, and the home and chapter scenes carry
different values for the same parameters. The pressure solver runs a very
small number of iterations, and that number is the one that matters: it is low, which is what makes
the fluid affordable, and it is why the effect reads as a smear rather than as a physically
convincing swirl. **That is an art direction decision, not a budget one**, and a rebuild that raises
it to a textbook count gets a different and worse looking result at several times the cost. A
separate flow map feeds the relief's surface with a dissipation just under full, which is what
makes the trail persist for several seconds. The fluid does not run on a low graphics tier and does
not run under a reduced motion preference, and both cases fall back to the rest state of the same
shader, which must be a valid image rather than a blank buffer.

**The resource manager** lets each view declare an item list and a preload policy separately for
development and production. An item may declare a fallback keyed on a coarse pointer or a low tier,
**resolved to the same internal name so nothing downstream changes**, which is what keeps the tier
decision in one place at load time; a build that branches on tier inside the scene code has
scattered that decision across every component. The six chapter views share a common item set
declared once and referenced. After the first view is shown a second pass adds the items the visible
media blocks need. A runtime flag selects between a supercompressed texture format and a
conventional one, and **a device that cannot decode the supercompressed format never downloads it**,
because the format decision is made from the graphics capability report before the first texture
request rather than after a failed decode. On unmount every resource is disposed by name and the
registry is cleared. A failed resource never stalls the loader.

**Type is drawn inside the scene.** Three signed distance field glyph atlases, one per family plus a
numerals only set, each with a companion metrics description, are generated at build time from the
chosen families rather than shipped. The document lays a string out at a known size on a hidden
measuring node, the scene reads the resulting metrics, and the glyph geometry is positioned from
them, which is what keeps the scene drawn title and the document title in agreement at every width.
The chapter numerals are a six entry sequence, the first five numerals and the studio mark, three of
which carry a manual optical correction, which is the tell that they are set as display type rather
than laid out by a metric. The home title carries its own reveal driven by a thickness stage and a fade stage over a
distance field with a noise term rather than by opacity, which produces letters bleeding into existence
rather than fading in, and both its stages animate their range past their visible bounds so the
edges finish cleanly.

**Colour grading** is applied to every scene as a lookup table, as the last stage of the composer
after the bloom, and it must be crossfadeable between two tables so a scene can move from a day
grade to a night grade over time rather than switching. The studio scene carries a day grade and a
night grade, each chapter carries one of its own, and the footer carries one.

**Context loss** is handled: the render loop stops, every resource is marked invalid, and the
document content shows at full opacity over a static ground; on restore the renderer is rebuilt, the
current view's resources reload, and the scene fades back in over the same duration as a normal view
show. The visitor never sees a blank canvas and the document stays readable throughout.

The not found route has its own scene material rather than falling back to a static page.

### The sound layer

Fourteen named sounds, three looping ambient beds, one event sound, one looping texture and eleven
short interface sounds. **The eleven short ones live in one sprite and the four long ones are
separate streams**, and that split is the correct one: a sprite avoids eleven round trips for sounds
that must fire within a frame of a pointer event, and a stream avoids holding a multi megabyte
decoded buffer for a bed that fades in over two seconds anyway. Beds are created as streaming
instances rather than decoded buffers.

The catalogue: a home ambience bed entering the home view; a case study ambience bed; a studio
ambience bed; a transition sound on moving from the home route to the studio page, which is the one
non ambient event sound in the product; a stone texture loop on a chapter scene; an index link click
and an index link hover; an inbound hover on the studio control from home and on the home control
from the studio; a chapter entry hover; a hover on any underlined control and on the sound control;
and three transition stings on the corresponding view changes.

**Four independent mute reasons** resolve to one effective state: a product default, the visitor's
own choice, a blur reason set by the tab losing visibility, and the effective state which is true if
any is true. **Sound is off on arrival and requires an explicit action to start, with no exception.**
A visitor who has not asked for sound and gets it has been ambushed, and on a studio portfolio that
is the one mistake a prospective client remembers. A pending theme is held: if a view asks for its
bed while the product is still muted, the request is stored rather than dropped and plays when the
visitor first enables sound, which is why turning sound on halfway down the reel starts the right
bed rather than silence.

Beds cross fade rather than cut: the outgoing bed fades from its current volume to zero and is
unloaded on completing, and the incoming one is created at zero volume and faded to its maximum. A
request for the bed already playing returns immediately. A change to the visitor's own mute setting
ramps the master volume rather than snapping it.

**The sound control** sits at the bottom right above every overlay. At rest the ring is retracted,
the dial is scaled slightly up and the dot is visible, and the label reads `Off` with `On`
transparent. Hovering fades the ring in and scales the dial down. Enabling runs an ordered sequence:
the `Off` label fades out, the `On` label slides and fades in, the ring progress runs part way
around, and the dot scales to nothing; then the ring rotates a full turn roughly every half minute
for as long as sound is on. Disabling reverses it and scales the dot back in from a larger value on
a fine pointer than on a coarse one, which is a noticeably different gesture on a phone. Hovering
plays the secondary control hover sound, but only on a fine pointer.

On first arrival the control carries the hint `Click to enable sound`, split per character. **The
hint must be a real label on the control** for assistive technology with the split hidden from it,
the control must be a real button reachable by keyboard, and its state must be exposed as a pressed
state rather than only as a visual difference between two words. Its accessible name reads
`Enable sound` when sound is off and `Disable sound` when it is on.

When the tab becomes hidden the product mutes for the blur reason without changing the visitor's own
preference, and unmutes on becoming visible only if the visitor had sound on. A suspended audio
context is resumed on the next gesture and never before. **A visitor who never enables sound has no
audio object created and no audio file requested at all**, which is a performance requirement as
much as a courtesy: the streaming beds are the largest media class after video.

### The pointer, cursor and hover system

Three separate things follow the pointer and conflating them is the usual way this gets rebuilt
badly: the pointer dot with its optional label, the scroll indicator dot cluster, and the scene
pointer, which is a normalised and a clip space position handed to the shaders. They share one
source of pointer position and nothing else.

The pointer dot's easing converts a per frame interpolation into a per second one, which is what
makes the follower arrive late by a constant perceived amount regardless of refresh rate.

**The label is the product's tooltip, its affordance hint and its loading indicator at once.** It
reads `Copy to clipboard` on entering the footer mailbox and `Copied` on activating it, cleared
after a few seconds, and it reads a loading state on any control whose target is still resolving.
The loading state is load bearing: the hidden opacity state is suppressed while it shows, and the
fast state does not hide the dot while it shows. **Every pointer label must have a non pointer
equivalent**: the copy action is a real button with a real accessible name and a live region
announcing the result, and the loading state is exposed as a busy state on the control. A label that
exists only as a floating string beside a pointer does not exist for a visitor who does not use one.

Every hover effect is gated behind a pointer capability query rather than a script detected class,
applying on hover for a fine pointer and on the active state for a coarse one. On a coarse pointer
the underline wipe is not applied and the rule rests at full scale, the index dimming is not
applied, the index preview media is not shown at all, and no hover sound ever plays.

The hover catalogue: an inline link in a text block ramps to the hover opacity on the lift ease; any
basic control that is not disabled ramps to the hover opacity on the interface ease; an index entry
title's rule scales in from the left; an index entry's type column dims when a sibling is hovered
and recovers about twice as slowly, which is what makes sweeping a pointer down the list feel like a
spotlight rather than a strobe; the video scrubber's bar and gutter both brighten when the track is
hovered; the mailing list input's placeholder brightens when its wrapper is hovered; and the footer
mailbox ramps to the hover opacity.

**Everything reachable by pointer is reachable by keyboard**, in document order, with a visible focus
indicator that is not the pointer dot, and a focus move does not move the pointer dot. An index
entry's enlarged hit area is real padding on the link rather than an offset pseudo element, so that
the focus ring matches the hit area: a hit area larger than the focus ring is a control that looks
smaller than it is.

### The routes

**The home reel.** The front page is one continuous vertical movement from the studio's positioning
statement to a mailbox, with no sections in the ordinary sense. The opening screen carries the
wordmark, the positioning statement as four separately animated words, `Innovative`, `digital`,
`experiences` and `studio`, and the hint `Scroll down` at the hover opacity on a fine pointer and at
full opacity below the phone stop. Every element starts fully transparent and each word fades on its
own stagger rather than as a block.

Each reel entry carries a description in the body size, a title drawn in the scene at the display
medium size, and a type in the interface size. **The scene draws the title and the document carries
the description and the type**, and that split is deliberate: the title has to scale with the camera
and the description has to be selectable text.

The reel's response to scroll is a set of separate multipliers on the same offset. At rest the media
planes drift vertically against a mask that moves at a fraction of their speed, so each one appears
to be seen through a moving window. In the fast state the vertical drift and the mask drift both go
to nothing while a horizontal factor comes up to full, so the whole reel shears sideways and the
titles blow up. The relief moves at the same rate in both states, which is what keeps the world
stable while the content in front of it changes character.

The show and hide timelines are asymmetric. The view fades in over roughly four times as long as it
fades out. The move to the studio page is the longest single transition in the product, carrying a
slow camera zoom and the one non ambient event sound; it is the studio's set piece and everything
else on the home route resolves in a couple of seconds or less. The hover pair is asymmetric in the
opposite direction to everything else: the relief brightens quickly and takes about four times as
long to settle back.

**Activating a reel entry does not navigate first and load second.** The pointer label switches to a
loading state, the case study's content resolves and its media begin loading, the incoming view's
resources reach the ready threshold, the outgoing document leaves instantly, and the incoming one
fades in while the scene crossfades views. **Step three must have a timeout**: if the incoming view
is not ready within a bounded interval the navigation proceeds anyway with the reduced scene,
because a visitor who activated a control and got nothing concludes within about two seconds that
the site is broken.

**The project index** is the only route that is a list rather than a composition, and it is
deliberately plain: the scene behind it is quiet and the interaction is entirely typographic. A row
takes the full width with its items aligned to the end; the project type sits in a narrow span right
aligned within it at the secondary opacity; the project title sits to the right of it in the serif,
its width fitted to the text. Rows stack with a small gap and a fluid vertical padding, and the
whole list is nudged left of true centre as an optical correction. The floating preview media sits
in a span on the left, absolutely positioned, taking no pointer events, sized by declaring a font
size and measuring in ems so that it scales by exactly the same law as the type around it from one
declaration. Under the preview sits the discipline row, each tag its own separately animated node.
**Preview media must be lazily resolved, at most one in flight at a time, and cancelled when the
pointer leaves before it arrives**: sweeping a pointer down thirty six rows must not start thirty six
downloads. Below the tablet stop the type column is hidden and the title takes the full width.

**A case study** is one piece of work told as an ordered list of blocks, and the route is a template:
everything on it comes from the content record. The opening carries the navigation control, a
centred headline, a primary action reading `Launch website`, a secondary action reading
`See backstage` with an indicator, and a footer action reading `See next project`. The headline
reveals per glyph through the scene rather than through the document. **The secondary action renders
only when the case study carries a reel.**

Five block types compose every case study and there are no others: a hero carrying a text, an
alignment, a call to action label and a target; a text block carrying two texts, an alignment, and a
size and a layout per text; a media block carrying a media list, a background colour, a background
image, an optional full video source and a caption; a split media block carrying a media list, a
background colour and a background image; and an image push carrying a title, two footer texts and
an image. Two sizes and three alignments is the whole typographic control an editor has, which is
correct: a portfolio whose editors can choose any size produces a portfolio that looks like several
studios.

Every block composes from the same media element, whose fields are the layout vocabulary of the
product: the media, an optional video preview serving as poster and hover loop, a legend, a width on
a step scale, a position drawn from five placements, a margin on a step scale, a manual vertical
offset, and the intrinsic width and height. **That last pair is why this content model is better
than most**: because the intrinsic dimensions come down with the record, the document reserves the
exact box before a byte of media has loaded and the page does not shift.

On a media block, a background colour and a background image are mutually exclusive and the image
wins; a dark background sets the dark variant flag; a video source turns the block into a poster
that opens the overlay, and **the thing that opens it must be a real activation control with an
accessible name naming the video rather than a clickable image**. The next project control resolves
to the next entry in the index order, wrapping at the end, and reads `See all projects` when there
is no next entry.

**The behind the scenes reel** is an overlay: a timed sequence of media, narrated, subtitled, and
scrubbable by scroll and by drag. It is the most technically unusual surface here because it is a
linear film assembled at runtime out of separate stills, audio and subtitle files. Its current time
is a scalar smoothed toward a target rather than set, advanced from three inputs at once: the
virtual scroller, a drag on the canvas, and the passage of time. Three separate smoothed deltas are
tracked, one for scroll, one for drag while held and one for drag after release, which is what makes
a flick coast and a wheel scroll not. Subtitle files are resolved alongside the media and the reel
does not begin until every declared subtitle has arrived; each cue is parsed and then split into
word nodes **incrementally, one cue per frame rather than all at once**, because a reel with a dozen
sections carries hundreds of cues and splitting them in one pass blocks the main thread long enough
to drop the reel's opening. Words reveal with a fade offset, a fade in delay and a fade out delay.
Per section audio plays against the reel's own timeline rather than as a media element with its own
clock, so scrubbing the reel scrubs the narration.

**The studio page** presents the studio's own story as a numbered chapter list rather than as prose,
reached from the single word `About`. Each section carries a numeral, a title, one sentence, a call
to action label and a relation to its chapter. Its scene carries the largest resource list in the
product and two colour grades named for a day and a night state, which is the evidence that this
scene has a time of day rather than a fixed grade.

**A studio chapter** is one chapter and one of six declared scenes, bound by a scene index on the
record. A chapter's body is restricted to two block types, an opening and prose, against five for a
case study: the chapters are writing and the case studies are exhibits. Each chapter view declares a
shared common resource set plus one scene model and one glow map of its own. Three reveal lights
sweep the scene over its reveal, each starting and finishing at a different point and each accepting
a different band of surface angles, so the geometry is discovered in three passes rather than lit
all at once; the third contributes no direct intensity and only mixes surface normals, which softens
the seam between the other two. Each numeral carries its own glow map and its own parameter set, and
two of the six carry hand corrections, one brighter because its shape is thinner and one nudged
sideways because it looks off centre otherwise; a rebuild that normalises them will make the second
chapter look dim and the fourth look off centre. Previous and next controls wrap at both ends, each
playing its own transition sting, and a chapter transition is a view change inside the scene rather
than a document reload. A chapter reached directly still resolves its previous and next controls
from the studio page's ordered list.

**The video overlay** is a full window player and the only surface in the product with transport
controls. The ground fills the window in the pure near-black, a mask sits over it, and the video
fills its box on a cover fit. **The scrubber runs across the vertical centre of the window rather
than along the bottom**, which is unusual and is the whole visual identity of the player: it is a
horizon line, not a progress bar. Its bar sits at the secondary opacity and its gutter at the gutter
opacity, both brightening when the track is hovered, and the bar carries a transition on its
transform which is what smooths a seek rather than snapping it. Seeking is a scrub rather than a
click to seek: pressing pauses, moving seeks continuously, and releasing resumes.

The open sequence is ordered: the chrome fades in, a loading bar runs, and then the scrubber, the
close control, the video and the mask all fade in together and playback starts. The interactive flag
is only set when the video's own fade completes, so a press during the opening does nothing rather
than seeking a video that is not yet visible. On open the current ambient bed is remembered and
stopped; **if the visitor is muted the video plays with its volume at zero rather than not playing
at all**, which is the correct choice because the visitor sees the film and enabling sound mid
playback does not restart it. On close the volume fades out and the remembered bed restarts. After a
couple of seconds without pointer movement the chrome fades away so the visitor is just watching,
and any movement brings it back; on a coarse pointer the auto hide does not run at all.

**The player must expose a real transport**: a play and pause control, a keyboard accessible
scrubber with arrow key seeking, a mute control, an elapsed and a total time, and a captions control
when the media carries a caption track. Every video with speech carries captions and the player
renders them. The overlay traps focus, returns focus to the control that opened it, and carries a
role and an accessible name.

**The footer** is the end of every route, with its own scene view, its own parallax and the
product's only form. It carries a two line baseline reading
`Find out more across all our productions`, a projects action reading `See all projects` or
`See next project`, the studio address at the secondary opacity, the studio mailbox
`studio@example.com` with its clipboard action, the control that opens the mailing list panel, and
three outbound social links. It reveals on crossing half its own height into view: the baseline
block rises and fades over the slowest single element move in the product, then each baseline word
fades on a stagger and the address, the mailbox, the list action and the social links all arrive at
once. The footer arrives like a held breath. The hide reverses it in a fraction of the time.

The projects action translates vertically by the footer's own progress, and switches between a three
dimensional and a two dimensional transform depending on whether a smooth scroll is running, which
is a deliberate optimisation: the promoted layer is only worth its memory while something is moving.
**Layer promotion must be transient**, set around each move and cleared after.

Opening the list action expands the footer into a full panel and hides the page content behind it.
The panel carries an open control at the bottom left, a close control at the top centre, a wrapper
centred both ways with its items aligned to their baselines, the input in the light cut with a
collapsed line height, a hairline rule under the input, a submit at the interface size, an error
line positioned below the input and a done line positioned near the bottom. The rule draws itself in
from the left a moment before the input is usable, which is the same wipe idea as the underline and
the mark reveal: three unrelated components, one gesture. The submit sits at the hidden opacity with
a default cursor while it cannot submit. **The mailbox must also be a real mail link**, so a visitor
who wants to write rather than copy can, and so the action degrades when the clipboard interface is
unavailable or denied; the copy result is announced in a live region.

**The not found route** renders the error view with its own scene material, a headline, an action
reading `See all projects`, the navigation control, the sound control and the footer, and a real not
found status on the response rather than a redirect or a success.

### Responsive behaviour

Five layout stops are hand written and everything else is generated by the scaling law. Above the
upper stop every fluid token freezes at its cap and the layout is unchanged. At the reference width
and below, the loader figure and hint shift their columns. At the tablet stop the loader mark, figure
and hint all take the full width, and the index type column is hidden with the title taking the whole
row. At the narrow stop the index hover interaction stops being applied at all. At the phone stop the
loader mark's minimum width steps down, its baseline caps its width, and **the scroll hint goes from
the hover opacity to full**, which is a small decision with a real reason: on a phone the hint is the
only thing telling a visitor that the page responds to a swipe, so it stops being a whisper. At the
small phone stop the remaining adjustments apply, and a short window in landscape carries its own
set.

The container padding steps once at the tablet stop against a fixed maximum.

What a phone loses and what it must not: the pointer dot and its labels go, but every action those
labels described stays as a visible control; the index dimming and preview go, but the full index
stays as a single readable column; every hover sound goes, but every click sound stays; the fluid
response's pointer input goes, but its rest state and the scene stay; the video overlay's control
auto hide goes, and the controls stay permanently visible.

**Which scene a visitor gets is decided by the graphics tier, not by the window width.** A narrow
window on a workstation gets the full scene and a wide window on a low power laptop does not.

Even though the product is single locale, the layout must not assume a direction: the underline
origins, the word reveal direction and the index alignment are all expressed in logical properties,
so adding a right to left locale is a translation task rather than a rebuild. That costs nothing now
and is unaffordable later.

### The reduced scene

Selected at the lowest graphics tier, on a graphics context failure, on a stalled loader, or by the
visitor's own override. The full detail model becomes the low detail variant declared alongside it;
the full dimension textures become the reduced pair; the bloom goes and the colour grade stays; the
fluid response holds its rest state; the scroll driven camera moves are retained because they are
cheap; the scene drawn type is retained because the atlases are small; and the chapter reveal lights
become a single static light.

**The reduced scene is a complete, art directed result rather than a degraded one.** Every route is
signed off in both states, because a meaningful fraction of the visitors to a studio portfolio are
on hardware that will get the second one.

### Copy

Every string a visitor can read. Line breaks inside a string are significant, because the headline
grid was art directed around them.

The opening statement is four separate word nodes: `Innovative`, `digital`, `experiences`,
`studio`. The loader hint and the home hint both read `Scroll down`.

The navigation control reads `About` on the home route and `Back` elsewhere, expanding to
`Back to Home` through two separately animated word nodes reading `to` and `Home`. The footer
projects action reads `See all projects`, or `See next project` on a case study with a successor.
A case study's outbound control reads `Launch website` and its reel control reads `See backstage`.
The sound control reads `Off` when sound is disabled and `On` when it is enabled, and its first
arrival hint reads `Click to enable sound`.

The footer baseline reads `Find out more across all our productions`. The footer mailbox is
`studio@example.com`. The pointer label on the mailbox reads `Copy to clipboard`, and `Copied` after
the copy.

The mailing list panel's validation message on a malformed address reads `Invalid email format`.
Its rate limited message reads `Too many attempts. Try again in a minute.` Its temporary failure
message reads `Something went wrong at our end. Try again.` and leaves the typed address in the
field. Its accepted message names the address submitted. Its consent line reads
`By submitting you agree to receive occasional studio news. Unsubscribe any time.`

The not found headline reads `That page has moved on.` and its action reads `See all projects`. The
server error headline reads `Something is temporarily out of reach.` and its retry control reads
`Try again`. The offline line reads
`You are offline. The pages you have already opened are still here.` The stalled loader line reads
`This is taking longer than it should.` and its control reads `Continue with the lighter version`.
The empty index line reads `Nothing published yet. Write to the studio.` The skip link reads
`Skip to content`. The sound control's accessible name reads `Enable sound` when sound is off and
`Disable sound` when it is on. The behind the scenes overlay's accessible name names the case study
it belongs to and the video overlay's names the video.

### Zero asset substitution

This product ships no binary file of any kind. Every asset class is replaced by a recipe, and where
the substitute is worse than the original this says so.

**Noise and grain.** Every noise texture is a tiling field and all of them are generatable: a
masking noise as an inline turbulence filter, fractal, at a fine base frequency with several octaves
and its saturation removed by a colour matrix; a colour noise as the same with saturation retained
and fewer octaves so the channels decorrelate; a fractal noise as the same at a much lower base
frequency with more octaves, which produces the large scale cloud structure a scroll driven
extrusion needs; two attenuation ramps generated on a canvas as radial gradients at two different
gammas; a sparkle noise as sparse bright points on black with a small blur; and a dust particle as a
single radial gradient from a white centre to a transparent edge. All are generated once at start
into offscreen canvases and uploaded as textures rather than regenerated per frame.

**The scene models.** This is the substitution that most affects the result and the one where
honesty matters most. The home bas relief becomes a subdivided plane displaced along its normal by
the fractal noise at two octaves with a ridge function applied so the noise produces sharp crests
rather than rolling hills: the character is right and the specific carved forms are lost. The studio
background becomes a set of lathe and rounded box primitives forming a shallow amphitheatre with the
same displacement at a larger scale. The six chapter scenes become six arrangements of primitives
differing in silhouette and count. The index background becomes a capsule chain following a spline.
The footer form becomes a single large rounded box, rotated, filling the lower half of the frame.
**Keep the original object names**: the entire value of this substitution is that the application
code is unchanged when the studio supplies real models. Supply the animation as a keyframe table at
the captured scroll stops, marked as inferred.

**Lit sphere maps and colour grades.** A lit sphere map is generated on a canvas as a radial
gradient centred slightly above centre, with a bright upper hemisphere, a dark lower one, a soft
horizon a little above the middle and one small hot specular toward the upper left; spend effort
here, because it is the substitute that most affects how the scene reads. The error scene's map is
the same generator with the specular tightened and the hemispheres desaturated. A colour grade is
generated as an identity lookup cube and then transformed by a declared curve per channel, with a
day grade lifted and warmed, a night grade lowered and cooled, six chapter grades interpolating
between them with a progressive hue rotation, and a footer grade at reduced strength.

**Photographic and video media.** Every case study media is generated from a seed derived from the
case study's slug and the media's position: a canvas gradient in two of the neutral roles with the
noise composited at low opacity, at the intrinsic dimensions declared in the record. Video is
substituted by a canvas rendered animation of the same generator with a slowly rotating gradient
angle, captured to a stream, so the video overlay has something with a real duration to scrub.
**Every generated placeholder is visibly a placeholder**, because a generated image that could be
mistaken for the studio's work is a worse outcome than an obvious grey field: it will ship.

**Web fonts.** Name the families and do not ship them. `EB Garamond` is the transitional serif with
old style figures at one weight; `Archivo` is the neo grotesque at one weight; `Archivo Light` is
its light cut. Each declares a fallback stack, and the fallback must be metrically compatible enough
that the loader figure does not reflow on swap.

**Glyph atlases.** The three distance field atlases are generated at build time from the chosen
families rather than shipped, as a build step with a declared input, so they regenerate when the
studio supplies its own licensed faces.

**Audio.** The three ambient beds are three detuned oscillators each through a low pass filter with
a slow modulation, the three beds differing in root and filter. The transition event is a filtered
noise burst with an exponential decay, band passed low, which reads as the sound the original name
describes. The stone texture loop is granular noise, short grains of filtered noise at a steady rate
with randomised pitch, looping to match the original's declared length. The eleven interface sounds
are short enveloped tones, each with a stated waveform, frequency sweep and duration, a hover being
a fast attack and a short decay on a triangle sweeping down and a click the same envelope on a sine
sweeping lower, with the remaining nine varying the root by a musical interval so the set is a
scale. **Generate the sprite offsets from the generated durations**: a hand maintained offset map
drifts the first time a sound is re cut.

## Constraints

Single tenant, one brand, one locale, one content space: nothing is scoped by tenant and there is
no row level isolation problem. No visitor account, no sign in on the public side, no profile and
no personalised surface. No client portal, no per client view, no shared asset review, no invoice,
no time tracking and no price anywhere. No payment provider and nothing to buy. No customer
relationship system: the studio's mailbox is the pipeline. No comment surface and no social feed.
No search provider and no filter control on the index. No translation service and no second locale.
No federated identity, no group claims, no provisioning, no attribute based rules over resource
hierarchies, no multi stage approval chain with delegation, no tamper evident audit with compliance
retention, and no distributed transaction across services: one write path, one cache, one queue.
No realtime layer: a case study published while a visitor is on the index does not update the page
they were served. No live tuning panel in production, and no debug flag that changes rendering
there. No third party analytics, consent management or tag script loaded before an explicit
consent, and no advertising category at all. No external network call at run time. No binary asset:
no photograph, no video file, no model, no colour grade table, no font file and no sound file ships
with this build. No mail service: the list confirmation is composed into an outbox row and the
confirmation link is what moves an address to confirmed. The catalogue holds at most a few hundred
projects and a few thousand media, and every route, listing and query must stay responsive there.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | readiness |
| `POST /api/auth/signup` | `email`, `password` | the created account and a token |
| `POST /api/auth/login` | `email`, `password` | the account and a bearer token under the key `access_token` |
| `POST /api/auth/logout` | none | acknowledgement |
| `GET /api/auth/me` | none | the signed in account and its `role` |
| `GET /api/projects` | none | a top-level array of published projects in index order |
| `GET /api/projects/{slug}` | none | one published project with its blocks, disciplines and reel relation |
| `GET /api/home-reel` | none | a top-level array of the curated ordered entries |
| `GET /api/disciplines` | none | a top-level array of the controlled vocabulary in position order |
| `GET /api/chapters` | none | a top-level array of published chapters in studio order |
| `GET /api/chapters/{slug}` | none | one published chapter with its blocks and `scene_index` |
| `GET /api/reels/{project_slug}` | none | the reel with its ordered sections |
| `GET /api/preview/{token}` | none | one record in its draft state |
| `POST /api/console/projects` | `title`, `slug`, `type`, `description`, `disciplines` | the created project in `draft` |
| `PATCH /api/console/projects/{slug}` | the editable fields and a `version` | the updated project |
| `POST /api/console/projects/{slug}/transition` | `to_state` | the project and its new state |
| `POST /api/console/projects/{slug}/preview-tokens` | none | the minted token, returned once |
| `DELETE /api/console/preview-tokens/{id}` | none | acknowledgement |
| `GET /api/console/media` | none | a top-level array of media with a ready variant count |
| `POST /api/console/media` | the master bytes and a filename | the media record in `deriving` |
| `DELETE /api/console/media/{id}` | none | acknowledgement, or a refusal listing the referencing records |
| `POST /api/console/reels/{project_slug}/sections` | `duration_ms`, `audio_media_id`, `subtitle_media_id`, `media` | the created section |
| `PUT /api/console/home-reel` | an ordered list of `project_slug` | the new reel order |
| `GET /api/console/publish-log` | none | a top-level array of rows, newest first |
| `POST /api/subscribers` | `email` | the same acknowledgement for a new and for a known address |
| `GET /api/subscribers/confirm/{token}` | none | the confirmation |
| `POST /api/outbound-clicks` | `project_slug` | acknowledgement |

Field names are exact. A successful login answers with the bearer token under the key
`access_token`, and the client sends it as a bearer credential on every authenticated call. A list
endpoint returns a top-level JSON array. Bearer auth is required on every `/api/console` endpoint;
the preview endpoint authenticates by its token alone; the public read endpoints and the intake
require none. A successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a silent success. An
authorisation failure answers as forbidden rather than as not found, because hiding the existence of
a record is a technique for a multi tenant system and here it only makes debugging harder for the
three people who work in the console. A validation failure names the field and the rule and echoes
none of the submitted value. A server failure carries a correlation identifier that matches the one
in the structured log, which is what makes a visitor's report actionable.

### No mocks

`postgres` and `minio` are the fact. An in-memory list of projects, a JSON file of publish log
rows, a `state` flag the app sets on itself without a row behind it, renditions written to the app
container's filesystem, a media marked `ready` whose object is absent from the bucket, a preview
token compared in the browser, or a hardcoded success the app returns to itself, are each a
contract violation however good the interface looks. Every published record, every preview token,
every publish log row and every subscriber must exist as a real row in `postgres` and survive a
restart, and every master and every rendition must exist as a real object in `minio` at its content
addressed key. The named provider is the fact - the app's UI and its own tables can only reflect
what lives in the provider, never substitute for it.

## Definition of done

A stranger can fall through one continuous lit scene past a curated reel, open a case study, read
it, play its behind the scenes reel with its subtitles, follow the link to the live site the studio
built, and leave an email address that the site accepts once and tells them nothing about twice. A
case study that has not been published is invisible to that stranger everywhere, and opens only
through a preview link the server checks. A producer signed in to the console can write that case
study, upload its media and show it privately, and cannot make it live. An editor can, and the
publish is refused while any of its media is still deriving, and is written to a log nobody can
delete from.
