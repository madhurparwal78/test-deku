# Keepers of the Reach

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, scroll the story route with sound off, filter all ten thousand Keepers down by trait, read a journal entry and download a press file, then create an account, bind a wallet address by returning the challenge phrase the server issued them, and land on their own citizen page, without hitting an error page. The hard part is the boundary around a citizen record: a citizen's three generated passport documents and their achievement files must be readable by that citizen and by nobody else, through any route, and the passport bytes must live in the MinIO bucket under the key scheme pinned below. A copy of those bytes on the app container's own filesystem, or a column in PostgreSQL holding the image itself, is not the object store and does not count.

## Overview

Keepers of the Reach is the public face of a fixed collection of ten thousand illustrated characters, the Keepers, and of the community that holds them. The site does five jobs at once and the tension between them is the whole design problem. It tells a story: the landing route is a scroll driven sequence of staged scenes with sound, not a page of text, and a first time visitor is meant to come away knowing what the world is. It is a catalogue: all ten thousand Keepers are browsable and filterable by thirteen visual traits, whether or not the visitor holds one. It is a membership directory: a visitor who holds a Keeper can prove it, claim a citizen page, set a nickname, choose a representative Keeper and accumulate achievements. It is a publication: an editorial journal carries updates in four categories. It is a press office: a media library of images, video and audio is downloadable by anyone, with a brand pack.

The audience is in four parts. A visitor has no identity at all and reads everything: story, catalogue, filters, journal, media, about, legal. A signed in account is the same visitor with somewhere to put a claim. A verified citizen is an account that has bound an address and can write to the one record that is theirs. An operator drives the passport pipeline and never appears in the interface.

There is no administrator role inside the application, and that is a deliberate constraint rather than an omission. Editorial power lives in seeded editorial records and infrastructure power lives outside the app. The application has exactly one privileged relationship: an account may write to the citizen record whose address it bound, and to no other.

What this product deliberately is not: there is no minting, no trading, no payment of any kind, no comments, no likes, no direct messaging, no following and no social graph between citizens. The mint route exists and presents a closed state rather than an error. The catalogue links out to a marketplace listing and never transacts.

The world has a fixed vocabulary and the product uses it everywhere, so a reader meets each word once. One catalogue item is called a Keeper. A verified holder is called a Citizen. A lore grouping of Keepers is called an Order. The lore name for the setting is The Reach, and the lore name for the central place inside it is The Hold. The in-world assistant invoked by press and hold on the protocol route is called ORA. Profile settings live on the citizen route itself rather than on a settings subdomain of their own. Everything outside the citizen directory is a read-only surface.

The genuinely hard part is that the identity model is small while the delivery problem is not: one sentence of authorization sits underneath a thirteen facet search over ten thousand records, a pinned scene route, and an asynchronous document pipeline whose output must never be readable by the wrong person.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor | Read the story, protocol, catalogue, filters, journal, media, about, legal and mint routes. Open the console. Read any citizen's public fields: address, nickname, biography, representative Keeper, holdings, earned achievements and derived statistics. Download media files. | **Cannot read any citizen's passport documents or achievement files. Cannot write anything. Cannot see the unearned achievement list of another citizen as if it were their own.** |
| Account | Everything a visitor can, plus request a binding challenge for an address, bind that address, and see their own account state in the action slot. | **Cannot write to any citizen record until an address is bound. Cannot bind an address another account has already bound. Cannot award an achievement.** |
| Citizen | Everything an account can, plus read their own passport documents and achievement files, edit their own nickname, biography and representative Keeper, request regeneration of their own documents, and delete their own record. | **Cannot read or write any other citizen's record, documents or achievement files. Cannot award an achievement to themselves or to anybody else. Cannot open the render harness.** |

The whole authorization model is one sentence: an account may write to the citizen record whose address it bound, and to no other. Everything else is world readable except a citizen's generated documents and their achievement files, which are readable only by that citizen. The permission matrix, stated completely because it is short:

| Operation | Visitor | Account | Citizen, another record | Citizen, own record |
|---|---|---|---|---|
| Read catalogue and filters | yes | yes | yes | yes |
| Read journal, media, about, legal | yes | yes | yes | yes |
| Read a citizen's public fields | yes | yes | yes | yes |
| Read holdings for a bound address | no | yes | yes | yes |
| Read a citizen's passport documents | no | no | no | yes |
| Read a citizen's achievement files | no | no | no | yes |
| Write profile fields | no | no | no | yes |
| Request regeneration | no | no | no | yes |
| Delete the record | no | no | no | yes |
| Award an achievement | no | no | no | no |
| Open the render harness | no | no | no | no |

Authorization is enforced **server-side on every mutating endpoint**, derived from the bearer token and never inferred from a path parameter, a header, a query value or anything else the caller controls. Hiding a button in the UI is not authorization: a direct API call from a visitor or account session to any citizen-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. One shared decision helper resolves the session, folds both addresses to their lowercase spelling, compares them and returns the answer, and every write calls it, because the moment two handlers compare addresses in two different ways one of them does it carelessly and fails open.

Signup is open. Anybody may create an account with an email address and a password. Binding an address is a separate, second act and is what turns an account into a citizen.

Every seeded account uses the password `deku-demo-pw-2026`.

| Email | Bound address | Holds |
|---|---|---|
| `member@example.com` | `0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801` | three Keepers, with passport documents already generated |
| `member2@example.com` | `0xB2c4E5d6F7a8B9c0D1e2F3a4B5c6D7e8F9a0B102` | two Keepers, with passport documents already generated |
| `member3@example.com` | `0xC3d5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1D203` | none. A bound address that holds nothing is a legitimate end state and is never presented as an error |

Awarding is a server side operation with no interface path. There is no circumstance under which a request from a browser awards anything.

## Core features

### Auth

1. An account is an email address and a password. Passwords are stored hashed; the plaintext is never stored and never returned. Signup is open at `/signup` and takes an email address and a password; a duplicate email is rejected as invalid with the field named.
2. `POST /api/auth/login` takes `{ "email", "password" }` and returns a bearer token. The client sends it as `Authorization: Bearer <token>` on every request that is not login, signup, health, or a public read. A token expires after twelve hours; a request carrying an expired or unknown token is denied.
3. `POST /api/auth/logout` revokes the presented token server side. A revoked token is denied on its next use, not merely forgotten by the browser.
4. Every form in the product refuses automated submission: a form carrying a filled unattended decoy field is refused, and the same form submitted repeatedly in quick succession from one source is refused with a retry hint. Neither refusal writes anything.
5. There is no password reset channel, because there is no mail service in this environment. A signed in session is the only way back into an account.

### Binding an address

The product has no passwords for addresses and no accounts in the usual wallet sense. An identity over an address is control of that address, demonstrated by returning a phrase only the holder of the session could have been given.

1. `POST /api/session/challenge` takes `{ "address" }` from an authenticated account and returns `{ "statement", "nonce", "domain", "issued_at", "expires_at" }`. The server generates the nonce, binds it to that address and that account, stores it with a short expiry, and marks it single use.
2. The statement the server returns names the site's own origin, the address, the nonce and the expiry, all four. A statement missing any of them is not a statement.
3. `POST /api/session/verify` takes `{ "address", "nonce" }`. The server compares the presented nonce to the stored one, checks it is not expired and not already consumed, consumes it, and binds the address to the calling account. The decision is taken on the server. A client may check locally for immediate feedback and that result is never trusted.
4. A nonce is single use. Replaying a consumed nonce is rejected as gone, not accepted. An expired nonce is rejected as gone. A nonce issued for one address presented against another is rejected.
5. Disconnecting revokes the binding server side. `POST /api/session/revoke` clears the binding and revokes the outstanding challenge rows for that address; it does not merely delete a local value.
6. An address already bound to a different account is rejected as unavailable, and the refusal names neither the other account nor its email.
7. Address comparison anywhere in the product is case insensitive. Two spellings of the same address differing only in case resolve to the same citizen and compare equal. The stored display spelling is what is shown; the lowercased spelling is what is looked up.
8. A malformed address fails closed. An address that is not `0x` followed by forty hexadecimal digits is rejected as invalid before it reaches any lookup.
9. The challenge operation is rate limited per address and per source, because it is the one write an account can make before it owns anything. Repeated failures for one address are refused with a retry hint.
10. On a fresh load with a valid token, reconnection is silent: the account and its bound address are restored without asking for a new challenge, and the action slot renders its bound state directly rather than flickering through the signed-out one. A valid token whose address binding was revoked elsewhere restores the account and nothing else, and that is a normal state on a second device rather than an error: the citizen can read their own private fields and cannot write until they bind again.
11. Six constructions are contract violations here, and each is named because a naive implementation reaches for one of them. A fixed message that never changes, so one proof is valid forever. A message carrying no domain, so a proof collected by any other site is accepted here. A message carrying no expiry, so revocation is impossible. A decision taken in the browser and trusted by the server, which is not authentication at all. A credential kept anywhere page script can read it, whether a script-readable cookie or a value in browser storage, because any injected script then exfiltrates a permanent credential. And a disconnect that deletes only locally, so a copied credential survives the citizen disconnecting. The bearer token is never written into a script-readable cookie, and a session credential kept as a cookie instead must be httpOnly and Secure with SameSite set to Lax, short lived, and bound to the account it authenticates.

### The catalogue

1. The catalogue is served as one packed, immutable, pre-built index document from the MinIO bucket, not from a query interface. Its shape is `{ "traits": [ { "name", "values": [ { "name" } ] } ], "tokens": [ [ id, [ [ trait index, value index ] ], "image digest" ] ] }`. Facet values are stored once in the header and referenced by index in each record, which is a deliberate trade of readability for transfer size and must be preserved.
2. The index holds exactly `10000` tokens and `13` traits. The thirteen facets and their value counts are fixed content: Ear `12`, Entity `2`, Eyes `35`, Face `38`, Hair `51`, Headgear `34`, Hand `12`, Innerwear `41`, Mouth `27`, Neck `11`, Outerwear `56`, Special `47`, Tattoo `7`.
3. Images are addressed by content digest, never by identifier, so an image address is immutable and cacheable forever. Grid thumbnail: `thumbs/<digest>.png`. Detail image: `images/<digest>.png`. Full bleed variant: `images_fullbleed/<digest>.png`. The full bleed address is derived from the detail address by substituting that one path segment, and that derivation lives in one place because it is applied in three.
4. The display index and the on-chain identifier are not the same number. They differ by a fixed shift of `5022` and wrap at the collection size of `10000`. The conversion runs in both directions and the wrap is arithmetic, not a truncation: a shift that takes the display index below zero wraps to the top of the range rather than staying negative. Worked examples the app is held to: display `0` is on-chain `4978`; display `5022` is on-chain `0`; display `5021` is on-chain `9999`; display `9999` is on-chain `4977`; and on-chain `4978` is display `0`. Getting this wrong sends half of the marketplace links to the wrong item and does so silently.
5. Filters are applied in the browser over the loaded index. Selecting several values within one facet is a union; selecting across facets is an intersection. A visitor selecting two hair values and one headgear value sees items that carry either hair value and that headgear value.
6. The filter pass is chunked, yields to the browser between chunks, and carries a cancellation handle so that a filter change mid pass abandons the pass rather than racing it or queueing behind it. Derived per record data is computed once on first access and reused, because a pass touches every record.
7. Search by identifier is a distinct filter type that replaces rather than intersects with facet filters, and the two are mutually exclusive in both directions: applying an identifier search clears the facets, and applying a facet clears an identifier search.
8. Default order is ascending by on-chain identifier. A shuffle control randomises the result order in place with an unbiased shuffle, and any subsequent filter change clears the shuffle and restores sorted order.
9. A switch at the top of the route selects between the whole collection and the holdings of the bound address. Its states, in this order of precedence: no address bound shows a connect prompt in the results area; a request in flight shows a skeleton grid at the last known result count; a bound address with no citizen record shows a prompt to register; a bound address with a citizen record and zero holdings shows an explicit empty state naming the address; a bound address with holdings shows the grid filtered by the same facets; a failed request shows the last good result with a stale notice and a retry. An address that holds nothing and an address the system has never seen are different situations and must read differently.
10. Selecting an item opens a detail overlay carrying the full image, the identifier in both forms, the full trait list with each trait's rarity, a link to the licence route, and a link to the marketplace listing built from the on-chain identifier. The overlay is a route state, not a component state: it is linkable, closes on the escape key and on the browser back button, returns focus to the grid cell that opened it, and does not lose the grid's scroll position behind it.
11. Ten thousand grid cells are never all mounted. Cells outside the view plus a margin are not rendered, images load only for cells inside a smaller margin, and an image request is cancelled when its cell leaves that margin during a fast scroll. The cell aspect is fixed, which makes the visible range exact rather than estimated.
12. The route reports its own state honestly: the facet rail renders from the index header as soon as it arrives and the grid fills in progressively, so the index fetch never blocks the route's first paint.

### The filters route

1. `/filters` is the facet panel as a standalone page. At narrow widths the rail cannot sit beside the results, so this route is the drill down target: the visitor opens filters, chooses, applies, and returns to the catalogue with the selection carried across.
2. The selection lives in the address bar, not in component state, so the return navigation carries it, a back gesture reopens the panel in the state it was left, and a filtered view is linkable and survives a reload.
3. The route is a title, a search field carrying the placeholder `SEARCH BY ID...`, then the thirteen facets as an accordion list, each row a label and an expand glyph, separated by hairlines.
4. Each facet row expands to reveal its values, each with a checkbox and a live count of matching items given the other facets' current selections. Those counts come from the same single chunked pass as the grid, once, and never from thirteen separate passes.
5. A facet value whose count under the current selection is zero is shown disabled rather than hidden, so the panel does not reflow while the visitor is working in it.
6. Validation, stated as outcomes: an identifier outside the range is marked invalid and the message names the valid range; a non-numeric identifier is rejected as the visitor types rather than on submit; an identifier that is valid but absent produces an empty result with the identifier echoed; selecting every value in one facet is treated as no filter on that facet; and a selection matching nothing offers to undo the last added facet specifically, by name, as well as `CLEAR ALL`. An empty state that offers only to clear everything punishes a visitor who made nine good choices and one bad one.

### The citizen directory

1. `/citizen/<address>` is the public page for one bound address, and `/citizen/<address>/achievements` is the same record with the achievement panel expanded. The address in the path is matched case insensitively.
2. A citizen record composes six things: the address and its abbreviations, which are public; the profile of nickname, biography and representative Keeper, which is public; the holdings, which are public; the achievements, of which only the earned ones are public; the derived statistics of points, earned count and total count, which are public; and the files, meaning the generated passport documents and the achievement wallpapers, which are readable by the owner alone.
3. `GET /api/citizens/<address>` returns the record. The `renders` object and its timestamps are returned only to the authenticated owner. To every other caller the `renders` key is **absent**, not empty and not null, so a caller cannot tell "has no documents" from "not permitted to see them".
4. An address with no citizen record returns not found, not an empty citizen. The difference is what lets the interface tell its first two states apart.
5. The citizen chooses one owned Keeper as their representative. If none is chosen the first holding is used. The page's colour scheme is derived from that Keeper's own background colour rather than chosen: the hue is held and the saturation and lightness are replaced with a fixed pair, producing a default, a dark and a light variant. This is why every citizen page looks like a member of the same family while being individually coloured, and it is computed rather than stored so that changing the representative Keeper recolours the page immediately.
6. Every derived surface colour is contrast checked against the ink placed on it before use, and the ink switches between the light and the dark value when a derived surface fails the check. With ten thousand possible source colours, a generative palette that is never contrast checked will certainly produce unreadable text.
7. Four of the thirteen traits are promoted on the page: entity, special, hair and innerwear. A trait absent from the representative Keeper renders as a dash rather than being omitted, so the four slots never collapse.
8. Achievements come in two kinds, `mark` and `badge`, grouped into sectors, each carrying a difficulty of `standard`, `rare` or `elite`, a point value and a list of unlocked files. Unearned achievements are listed rather than hidden, with their names and point values visible and their marks drawn in the unearned state. A progression system that hides what is unearned gives the citizen nothing to aim at.
9. Statistics are derived by intersecting the citizen's earned identifier list with the published achievement catalogue and summing points over the intersection. They are never stored, because a stored total drifts from the list the moment an achievement's point value is edited.
10. Editing is available to the verified owner of the address alone, and only through `PATCH /api/citizens/<address>/profile`. For a citizen who is not the visitor, the edit affordances are **not rendered**, not rendered and disabled. An interface that ships a disabled control to every visitor has already told the world the control exists and has usually shipped the code path with it.
11. Field rules, enforced on the server as well as in the field: the nickname is `3` to `24` characters of letters, digits and single interior spaces, with no leading or trailing space, and is unique across citizens compared case insensitively and with interior spaces collapsed; the biography is up to `280` characters of plain text with no markup and newlines collapsed; the representative Keeper must be an identifier the address holds at write time, revalidated against the holdings ledger and not against the cache, because a citizen can sell a Keeper between loading the page and saving.
12. Two citizens claiming the same nickname at the same instant: at most one succeeds. The other is refused with `nickname_taken` and nothing is written for it. This holds under two simultaneous requests, not only when they arrive one after another.
13. A partial update omits fields rather than sending nulls, and an explicit null clears a field. The two are distinguishable, or a citizen can never clear their biography.
14. Every write validates inline before it writes: an invalid nickname or biography is refused with the offending field named in the response and shown beside that field in the form, and nothing at all is written. A refused write leaves the stored record byte for byte as it was.
15. A citizen may delete their own record. Deletion clears the profile, deletes the generated passport documents from the bucket, clears the holdings cache, marks the citizen row deleted, and keeps in the audit trail the fact of the deletion and its actor while dropping the field values. An address that deletes and then binds again is a new citizen with no achievements, and the interface says so plainly rather than appearing to have lost their history.

### The passport documents

1. Three documents are generated for each citizen: `document_front`, `document_back` and `share_image`. Each is an image object in the MinIO bucket, written by the server. The app never draws them in the browser, never keeps their bytes on its own filesystem and never stores their bytes in a PostgreSQL column.
2. The object key scheme is fixed: `citizens/<address_lower>/<face>/<content_hash>.png`, for example `citizens/0xa7d3f1b2c4e5d6a7b8c9d0e1f2a3b4c5d6e7f801/document_front/9f2a1c7d4b6e8a0f2c4d6e8a0b2c4d6e8f0a2c4d6e8b0a2c4d6e8f0a2c4d6e8b.png`. The address segment is the lowercased spelling.
3. The content hash covers every input that affects the output: the nickname, the biography, the representative Keeper identifier, that Keeper's image digest, the sorted list of earned achievement identifiers, and a template version. A generation run whose computed hash equals the stored hash for a face exits without producing anything. That one field is what stops a citizen who saves the same value twice from queueing the same work twice.
4. Generation runs outside the request path. A profile write that changes the content hash, an achievement award, or an explicit request each put the affected faces into `pending`; a face reaches `ready` with a new object key and an updated timestamp, or `failed` with a stated reason. `GET /api/citizens/<address>/renders` returns per face the state, the address to read it and the last updated time, and also a suggested next poll interval so the client backs off rather than polling on a fixed timer. It is a single cheap read.
5. A run writes a new key derived from the content hash and then repoints the row. The previous object is not overwritten. That makes the change atomic from a reader's point of view and makes a bad run recoverable by repointing rather than by regenerating.
6. Generation is idempotent. A run delivered twice produces one set of documents, because the second delivery finds the hashes equal and exits.
7. `POST /api/citizens/<address>/renders` requests regeneration, owner only, limited to a small number per citizen per day, and returns the run already in flight rather than starting a second.
8. While a face is pending, the page shows the previous document with a regenerating marker rather than a spinner in its place. A citizen who has always had a document never sees it vanish because they edited one line of their biography.
9. A passport document is a private object. It is never publicly readable from the bucket. The app hands the owner a short lived address minted at the moment they ask for it, and hands no such address to anybody else. A request for another citizen's document, by any route including a guessed object key, is refused.
10. `/render-asset` is the operator harness that renders exactly one document face at a fixed size with no chrome, no scene, no audio, no smooth scroll and no page view logging. It refuses without a valid, expiring, signed parameter, it never reads a browser session because it runs without one, it emits a machine readable ready signal once fonts, images and layout have settled so that a capture happens on a finished frame rather than after a fixed wait, and it returns a non-success status for an address with no citizen record so that a failed run is a failed run rather than a blank image. It is never linked, never listed in the sitemap and never indexable.

### Achievements

1. Achievement rules are evaluated on the server only. An achievement whose criterion is holdings based is re-evaluated whenever holdings are refreshed.
2. Awarding is idempotent by construction: one row per address and achievement pair, so an evaluation that runs twice awards nothing the second time.
3. Every award writes an audit row recording which rule fired and on what evidence.
4. Achievements are never revoked automatically. A citizen who earned an award and later sold the Keeper keeps the award. This is a product decision, stated here because the alternative, silently removing awards when holdings change, is what a naive implementation does.
5. An unpublished achievement is invisible: it appears in no list, earned or unearned, and contributes no points.

### Holdings

1. Holdings are read from a ledger the server owns and are never read from the browser. `GET /api/citizens/<address>/holdings` returns `{ "success", "has_citizen_record", "holdings": [ { "token_id", "on_chain_id", "image_digest" } ], "observed_at", "stale" }`.
2. `has_citizen_record` exists so the catalogue's holdings view can tell its third state from its fourth. It is present and correct even when the holdings list is empty.
3. The response is served from the holdings cache when the cached observation is inside its freshness window and from the ledger otherwise. When the ledger read fails and a cached observation exists, the cached list is returned with `stale` true and a success status, because a stale holdings list is far more useful than an error.
4. The cache is a cache and is never the authority for a write. The representative Keeper check at write time goes to the ledger. When the ledger cannot answer, the write is refused with a clear reason rather than accepted on the cache's word. This is the one place in the product where an outage blocks a write, and it is correct: the alternative is letting a citizen claim a Keeper they no longer hold.

### The story route

1. `/` is a pinned, scroll driven sequence. The document is barely taller than the window and the whole sequence is driven by scroll input against a pinned stage rather than by document height.
2. The load sequence is fixed: the frame's action slot renders first with identity already resolved, so the slot never flickers between states; then a preloader carrying a rule, a progress bar, a left label reading `LOADING - <percent>%` and a right label cycling system status lines including `INITIALIZING SYSTEM...<n>` and `LOADING ATTRIBUTES`; then the audio control with its enable prompt; then the wordmark; then the scene.
3. The preloader reports real progress against the byte weight of the current scene's prefetch set. It is not a timed animation. A preloader that lies is worse than no preloader on a route this heavy.
4. The preloader times out after ten seconds. Beyond that the route presents its text content over a static field and continues without the scene, showing `SCENE UNAVAILABLE. CONTINUING WITHOUT IT.` A visitor is never held at a percentage that never completes.
5. Four in-page sections are addressable from the route submenu: `Project`, `The Hold`, `Factions` and `The World`. Each is a scroll range on the pinned stage, and selecting one scrubs the scroll position to that range's start over a fixed duration rather than jumping, so the scene passes through the intervening states rather than cutting.
6. A character carousel sits in the sequence as a three dimensional arrangement of cards that rotates with scroll, firing three distinct audio cues at three positions in its travel. Cards are recycled rather than all mounted, and recycling never resets a card's transform mid rotation.
7. Degraded states, all of which keep the route usable: with no hardware rendering, a static field with the wordmark, the section text, working navigation and no preloader; with a scene set that fails to load, the same plus a dismissible notice; with reduced motion asked for, the sections become an ordinary scrolling document and the scene renders one still per section; with audio unavailable, everything else proceeds and the audio control renders disabled with a reason; on a slow or metered connection, sequence sets are reduced to their first and last frames and the scene continues.

### The protocol route

1. `/protocol` is a single long form statement over a scene, with five in-page sections addressable from the submenu: `VISION`, `WORLD`, `CHARACTERS`, `PORTAL` and `UNION`.
2. The route carries a press and hold control labelled `HOLD [SPACEBAR] FOR ORA MODE`, operable by pointer and by the space key. Holding it raises an overlay whose progress runs from nothing to complete as the hold accumulates, starts a live level meter, and reveals the narration for the current section.
3. The control releases and reverses on pointer up, on key up, on window blur, and on the pointer leaving the window. The last of those is the one that gets missed: a held control that never receives its release event because the pointer left the window leaves the overlay stuck open.
4. The level meter is driven by real audio analysis when sound is enabled and by a synthetic envelope when it is muted, so the control looks alive either way. A meter that flatlines when muted tells the visitor the feature is broken.
5. The control is reachable by keyboard, announces its held state, and offers an equivalent non-held path to the same content, because a press and hold gesture is not available to every visitor. For keyboard and assistive technology it behaves as a toggle labelled `ORA mode`: activate to start, activate again to stop. The hold behaviour is an enhancement on top of the toggle, never the only path.

### The journal

1. `/journal` carries a category tab row of `ALL`, `UPDATES`, `COMMUNITY` and `FINDERS LAB`, a full width display wordmark, the strapline `DISCOVER WHAT IS NEW IN THE REACH` at its lower left, a date stamp at its lower right reading `LATEST ARTICLE: <date>`, a hero entry with full bleed art occupying the remaining fold, and a grid of entries below.
2. Category selection is a route state reflected in the address, so a shared link to a category arrives filtered and a reload keeps it.
3. An entry carries a title, a category, a publication date, a hero asset, a body and an author, and is addressed by slug at `/journal/<slug>`.
4. The body arrives as a structured document and is rendered through a resolver that maps each node type to a component. It is never inserted as raw markup. The resolver handles at minimum: paragraph, heading levels two and three, bullet and ordered lists, block quote, inline emphasis and strong, inline link, image with caption, embedded video, horizontal rule and code block.
5. Links inside the body are classified at render time by the link type recorded in the document, never by inspecting the address, because a relative link and an absolute link to the same place must behave the same. An internal link becomes an in-app navigation; an external link becomes an anchor carrying the safety attributes for cross origin targets.
6. Draft entries are reachable only through a preview mode that is not the default, and the preview flag is never derivable from a query parameter alone on a normal response.
7. States: a category with no entries shows a named empty state offering the `ALL` category; an unknown slug shows the product's own not-found presentation with a link back to the index; an entry whose body is empty still renders its title, date and hero with a short notice in the body area; a missing hero asset leaves the layout holding its shape behind a generated placeholder.

### The media library

1. `/media` is the press library. A type filter row carries `ALL`, `IMAGE`, `VIDEO` and `AUDIO`, each with a live count, seeded as `ALL 71`, `IMAGE 31`, `VIDEO 34` and `AUDIO 6`. The counts sum: thirty one plus thirty four plus six is seventy one. A count row that does not sum is the most common defect in a filtered library.
2. The route also carries a giant display wordmark low on the field, an item preview panel, a total count on the right reading `<n> FILES`, and a file data column listing the selected item's filename under `FILE DATA`, with `PUBLISHED`, `FILE SIZE` and `FILE FORMAT`.
3. Selecting a type filters the list and updates the address. Selecting an item fills the file data column and the preview. Images preview as stills, video previews muted with a play control, audio previews as a waveform with a transport.
4. Downloads are served through a signed, expiring address issued per request, never by exposing the bucket path. The signed address is minted when the download control is activated and not when the item is selected, so a page of thirty four items never mints thirty four credentials the visitor will not use.
5. A single brand pack archive covers the whole identity. Its version is in its filename and is displayed beside the control as `DOWNLOAD BRAND PACK v<version>`, so a journalist can tell whether the copy they hold is current.
6. States: with no item selected the file data column shows its labels with dashes and the preview shows an empty field; a type with no items shows a named empty state while the other type counts stay visible; an unavailable preview asset leaves the item selectable and downloadable behind a generated placeholder; an expired download address is silently re-fetched on activation and then the download proceeds; a download blocked by the browser shows a notice explaining the block with the file data still visible.

### The about route

1. `/about` is a flat, dense, typographic route with no scene: a coloured field with the drafting grid visible as hairlines, a top bar carrying a marker, the label `CONNECT ON` and two community links, and a repeating roster of team cards.
2. Each card carries a name set large in the display face, a marker glyph and a role in monospace beneath it, and a two digit index number at the card's lower right. Cards alternate with empty cells, and diagonal hairlines cross some empty cells, so the roster reads as a technical drawing rather than a staff list.
3. Interleaved with the roster, a statement block carries a two line display heading, a monospace strapline prefixed with a double slash, and a corner cut control labelled `SEE OPEN POSITIONS`.
4. The roster is seeded content rather than hard coded markup. Each roster member carries a display name, a role, a position and an optional link. The index shown on the card is assigned by position, not stored, so removing a member leaves no gap in the numbering.
5. The open positions control is an external navigation carrying the safety attributes for cross origin targets, and degrades to a plain contact instruction when no destination is configured.

### The legal routes and the licence

1. Three routes carry long form documents: `/legal/terms-of-service`, `/legal/privacy-policy` and `/legal/legal-license`. All three are seeded documents rendered through the same structured document resolver as the journal, with an automatically generated section index, anchored headings, and a last updated date taken from the record rather than from the file.
2. The privacy route is the product's privacy page. It is reachable from the footer of every page and names each field the product stores about a citizen, which is the address, the optional nickname, the optional biography, the holdings cache and the audit trail, together with how long each is kept and how a citizen removes it.
3. The licence route is the one with product consequence rather than boilerplate consequence: it states what a holder may do commercially with their Keeper's artwork, and the catalogue's detail overlay links to it from every item.

### The console

1. A terminal overlay is available from every route, and it has four invocations. The backtick key toggles it, a control in the frame toggles it, the escape key closes the response window if one is open and otherwise closes the console, and a click on the underlay closes it.
2. The panel carries a title bar with a protocol label on the left and a network label on the right reading `THE REACH Mainnet`, a horizontal rule, an output region, and an input row with a glyph, the typed text and a blinking caret. A session identifier is generated per open, decorative, and marked as decorative.
3. The command set is seeded content rather than compiled in. Each command carries an input string and a structured response. Matching is case insensitive and exact against the whole input.
4. A small number of commands are internal and resolved in code before the seeded set is consulted, so an editor cannot shadow a navigation command by defining one with the same input. The seeded internal command `connect_citizens` routes the visitor to `/registration` and closes the console.
5. An unrecognised command appends the response `The command "<input>" does not exist. Please try again.` naming the attempted input. The attempted input is inserted as text and never as markup. It is the one place in the product where a visitor's own typing is echoed back to the screen, and that is the reason the rule exists.
6. The output region scrolls to its end on every append. The input is focused on open and refocused on any click inside the panel. At narrow widths a response opens in its own window over the console rather than appending, because the output region is too short to read in. Command history is navigable with the up and down arrows. The console's state is discarded entirely on close: history, output, session identifier and pending response.

### The mint route

`/mint` presents a closed state: a headline, a short statement that no Keeper is currently being issued, a live count of the collection, and a link to the catalogue. It never takes payment, never issues a Keeper, and never returns a server error. A route that errors rather than presenting a closed state is itself a defect.

### The registration route

1. `/registration` is where an account becomes a citizen. It renders without the frame and without the footer: a full bleed field, a diagnostic column of monospace status lines at the top left that type on in sequence, an exit control at the top right carrying the corner cut and labelled `/ EXIT APPLICATION`, and centred on the field an audio sigil, the title `THE HOLD CITIZEN BUREAU`, the two line instruction `Welcome to the Citizen application service. Please proceed by connecting your Wallet.` and one corner cut connect control labelled `CONNECT WALLET`.
2. The diagnostic column is decorative and is hidden from assistive technology. It carries no information the visitor needs, and reading it aloud line by line is actively obstructive.
3. The flow, in order: arrive with no address entered; enter or choose an address; request the challenge; the server issues the statement; return the nonce; the server verifies, consumes the nonce and creates the citizen record if it is absent; redirect to the citizen page.
4. Every state has a presentation and a recovery. No address entered shows the connect control. A request in flight disables the control, shows a progress indicator and a message naming what is being waited on. A refused request shows `THE REQUEST WAS DECLINED. TRY AGAIN WHEN READY.` with the control re-enabled and no retry counter. A challenge that expires before the nonce comes back shows a message and re-issues on the next attempt. An address already bound elsewhere is refused with a message that names neither the other account nor its email. An address bound successfully that holds no Keepers shows `THIS WALLET HOLDS NONE OF THE COLLECTION YET.` with a link to the catalogue; that is a legitimate end state and is not an error. An unreachable server shows a message, retries with backoff, and preserves the entered address.
5. Switching the signed in account while a citizen page is open discards everything private on screen immediately and returns the page to its public presentation. This is a security requirement, not a convenience: a visitor who switches accounts must not continue to see the previous account's private fields.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Story. The pinned scroll sequence | none |
| `/protocol` | Protocol. The statement, with the hold control | none |
| `/gallery` | Catalogue. Ten thousand Keepers, thirteen facets | none, binding optional |
| `/filters` | Facet panel, standalone, the narrow width drill down | none |
| `/journal` | Journal index, four categories | none |
| `/journal/<slug>` | Journal entry | none |
| `/media` | Media library and brand pack | none |
| `/about` | Roster and studio | none |
| `/mint` | Closed mint state | none |
| `/legal/terms-of-service` | Terms | none |
| `/legal/privacy-policy` | Privacy page | none |
| `/legal/legal-license` | Artwork licence, linked from every catalogue item | none |
| `/signup` | Create an account | none |
| `/login` | Sign in | none |
| `/registration` | Bind an address | account |
| `/citizen/<address>` | Citizen page, public read, owner write | none to read |
| `/citizen/<address>/achievements` | Citizen page with achievements expanded | none to read |
| `/render-asset` | Operator harness, one document face | signed parameter |

**Entry and redirects.** An unauthenticated visitor who opens `/registration` is sent to `/login` with the destination remembered and is returned to it after signing in. Signing in from the action slot with no remembered destination lands on the citizen page of the bound address, or on `/registration` when no address is bound. Signing out clears the bearer token, revokes it on the server and returns to `/`. A token that expires mid action leaves the page where it is, refuses the action with `Your session has ended. Connect again to continue.` and offers sign-in without discarding what the visitor had typed. A signed in visitor who opens a citizen page that is not theirs sees the public record with no edit affordance rendered. An unknown address on `/citizen/<address>` renders the product's own not-found presentation carrying `Nothing here. Check the address and try again.` and, when the address is the visitor's own bound address, an invitation to register. An unknown address anywhere else in the product renders the same not-found page, which answers as not found and offers a way back.

**Journey: browse and filter.** Open `/gallery`. The count reads `10000 KEEPERS` under the `KEEPERS COLLECTION` tab. Open the facet rail, expand Hair, tick two values, expand Headgear, tick one. The result count updates and is announced. Open an item; the overlay shows `KEEPER <index>`, both identifiers, every trait with its rarity, and the licence link. Press escape; focus returns to the cell that opened the overlay and the grid is where it was.

**Journey: bind an address and claim a page.** Open `/signup`, create an account, then open `/registration`. Enter `0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801` and request the challenge; the statement comes back naming the site's origin, the address, the nonce and the expiry. Return the nonce. The server consumes it, binds the address and redirects to `/citizen/0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801`. Submit the same nonce a second time; it is refused as gone.

**Journey: edit a citizen page.** Signed in as `member@example.com`, open the citizen page and open the editor dialog. Change the nickname to a free value and save. The record shows the new value at once; if the server refuses the write, the old value is put back and the reason is shown beside the field. The passport faces move to `pending`, the previous documents stay on screen with a regenerating marker reading `UPDATING YOUR DOCUMENTS.`, and the faces return to `ready` with new object keys and later timestamps. Save the identical value again and no new work is queued.

**Journey: the boundary.** Signed in as `member2@example.com`, open `/citizen/0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801`. The public record renders; no `renders` key is present; no edit control exists in the markup. Send `PATCH /api/citizens/0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801/profile` directly with that session; it is denied with `You can only change your own page.`, the row is unchanged, and the attempt is audited. Ask the app for a read address for that citizen's `document_front`; it is refused. Ask the bucket directly for the object; it is refused there too.

**States.** Every list has a named empty state: no results under a filter, no entries in a journal category, no items of a media type, no holdings for a bound address, no citizens matching a directory search. Every page has a loading state that holds the layout rather than collapsing it. Every error renders in place, keeps the frame and navigation working, and never replaces the page with a stack trace, a query or a storage key. A rate limited request shows `Too many attempts. Try again in <n> minutes.` An unresolvable holdings read shows `We cannot confirm what this wallet holds right now.` Anything unclassified shows `Something went wrong. Reference <request id>.` with the request identifier the response carried.

## UI/UX notes

The north star: somebody arriving should understand within one screen that this is a world with a fixed population of ten thousand, and that the site is a technical document about that world rather than a marketing page for it. Every later decision resolves against that. The register is consumer and editorial with an operational spine: the Keepers and their scenes are the first thing seen on the story, protocol and catalogue routes, while the citizen directory reads as an operator surface, labelled and numbered and dense. Drafting sheet over brochure. Evidence over persuasion.

Almost nothing here is sized in fixed units. One factor is derived from the window width against a fixed design width, and every dimension in the interface is a multiple of it, so the whole layout enlarges and reduces together like a photograph being scaled rather than a page reflowing. Text sizes, gaps, radii, stroke weights and drawn geometry all consume that one factor. The exact design width is yours; what must be true is that no component reads the window for itself and that a control looks the same at three widths with no fixed dimension anywhere in it.

The palette is deliberately tiny, and its smallness is the point: black and white carry the entire interface and everything else on the screen is artwork. One accent, a light vivid lime, is reserved for anything live or selected, the active facet, the audio cue and the progress indicator, and it appears nowhere else. One field colour, a light soft blue, belongs to the about route and to no other. One colour, a mid soft red, means something has gone wrong, and it is used for error text and invalid field borders and for nothing decorative. The scene overlays carry their own field, a deep muted teal on the protocol route, lit by a light vivid orange, a mid soft lime and a mid vivid orange. The console window draws its stroke and its label in its own light soft blue over a mostly opaque dark fill, and the about route's travelling overlay band is a light soft indigo. The exact values are yours, so long as each keeps its exclusivity and its role. Every surface declares its ink colour and its hairline colour together as a pair, so a control dropped onto a dark field, a light field or the about route's field inverts correctly without knowing where it is.

Typography carries four roles and two licence positions. A variable display grotesk sets headlines and citizen names, with a real weight range rather than one weight faked by the browser. An angular display face sets the wordmark and the giant route titles, and because those are a small number of fixed strings at display sizes they are drawn as geometry rather than shipped as a font file, which removes the licence, the request and the loading state at once. A monospace sets every micro label, index number, status line and console line, and its figures line up in a column wherever numbers stack. A Japanese sans covers the Japanese variants of all of the above. Two of the four are commercially licensed and are never redistributed with the source; open substitutes stand in. Every family declares a real fallback stack and text stays visible during font load rather than being hidden. The display headline sets its leading tighter than its own size, which is what makes a stacked two line headline read as a block rather than as two lines; that relationship is the requirement, the sizes are yours.

The signature shape is not a radius. It is a corner cut: one corner of a rectangle replaced by a straight diagonal, and it appears on every button, every panel and the console window. It is generated from parameters given a width, a height, an inset and which corner to cut, never drawn as an image, so it stays exact at every scale. Corners elsewhere are barely softened. The console window is the one place where two cuts of deliberately different sizes meet on one shape, and copying one to the other is the likeliest way to get it wrong.

Density is the operator's, not the brochure's, wherever data is shown: catalogue captions, file data, achievement rows and status lines sit tight enough that a full set reads without scrolling past it, while the story, protocol and about routes are open enough that the subject dominates. Space is made by leaving columns of the drafting grid empty rather than by adding a gutter, and the grid's hairlines can be shown on demand, switching between their dark and light values with the surface behind them. Space over dividers.

Motion has one family of curves and three speeds, and the uniformity is the requirement rather than the curve. Anything answering the pointer moves quickly. Anything a panel does to itself is slower. An acknowledgement is close to instant. Nothing uses a different speed to feel special, and no transition is declared across every property of every element, because a blanket transition animates layout as well and is a reset artefact rather than a design decision. Overshoot is allowed on large shapes and never on small text, where it reads as a rendering fault.

The named moments, each of which must exist and be recognisable: elements entering the view rise a short distance while fading in, once, then stay arrived. Console output and status lines type on character by character. The console caret blinks. Status dots blink. Loading and system messages flash in a run of hard opacity steps rather than fading, which is what makes a status line read as a machine reporting; smoothing it to a fade removes the character of every loading state in the product. Live indicators pulse outward and fade. The scroll prompt bounces. Loading rings spin, and a counter rotating pair spins against each other. Vector strokes use a draw-on reveal, drawing themselves in along their own path. A sheen sweeps across a control on press. A replaced label wipes in from the left. On a navigational link, a coloured panel waits just off the label's left edge, slides across under the word while the word itself flips to the opposite ink colour, and on leaving continues out to the right rather than reversing, so it always travels one direction, like a card pushed through a slot. Buttons do not use that effect: each draws its own background into a surface sized to itself so it can carry the corner cut and still light cleanly at any size, redrawing when the window, the scale or the pixel density changes. Every interactive control may carry an enter cue and a distinct leave cue, and those cues are suppressed while the pointer is moving fast, or a sweep across a menu fires every cue at once, and suppressed entirely where there is no hover at all.

Scrolling is not native on the scrollable routes: the content is slid under the visitor a fraction of a second behind their input, which is what gives the site its heavy gliding feel, while the real scroll position stays the source of truth so that find, anchors and the back button keep working. Only transform and opacity are ever tied to scroll position. Reveals are built from two panels moving apart in opposite directions rather than one edge wiping across, so things read as opening rather than as being uncovered. A progress indicator is scrubbed on every route and is close to invisible by design: it reports where the visitor is without competing with the page.

The reduced motion preference is honoured rather than shortened: native scrolling is restored, and everything tied to scroll position snaps to its end state at its trigger point instead of interpolating. Under every motion character, including the quietest, that preference is respected. Sound is off on arrival and never plays without an explicit action; one control, showing a small level meter, turns it on, its state lasts the session, and muting mutes everything at once so that a scene which starts a sound while muted does not become audible when unmuting mid scene.

Accessibility is a floor, not a preference, and the commitments below are the ones a site of this kind normally fails. The product meets WCAG AA: body text and its background meet the AA contrast ratio on every surface including the derived citizen palettes, non-text indicators meet the non-text minimum against both the dark and the light field, touch targets are comfortably sized, and meaning is never carried by colour alone. Every route is reachable and every operation completable by keyboard navigation alone, including filtering the catalogue, opening an item, binding an address and editing a citizen page, with a visible focus indicator everywhere and focus order following the visual order. The menu, the console and every overlay trap focus and restore it to the control that opened them. Icon-only controls carry labels. Every content image carries alternative text, and a catalogue item's alternative text is composed from its identifier and its trait values, while the drafting grid, the crosshair, the diagnostic column and the console session identifier declare themselves decorative and are hidden from assistive technology. Filter result counts, render progress and error messages announce politely; nothing announces assertively except an error the visitor caused. Doubling the text size clips, overlaps and hides nothing. The pinned scene routes expose a parallel linear readable document carrying every fact the scenes carry, present in the markup rather than generated, reachable by a skip link, with the scene itself marked decorative: it is not an alternative version of the page, it is the page with a scene drawn over it. One thing is explicitly not claimed: the scenes themselves are not described, because a scene carries mood rather than information and narrating a moving three dimensional scene produces something worse than silence. Every fact a scene carries is in the parallel document instead.

The layout is responsive across three widths, and unusually the wide width is the base while the narrow width carries the overrides, because the scenes are authored wide. The arrangement holds at every width between the named tiers, nothing overflows sideways at a narrow viewport, and every navigation target stays reachable there. Which behaviour a visitor gets is decided by pointer and hover capability rather than by width alone and never by inspecting the browser's user agent, so a narrow window on a laptop keeps hover behaviour and a wide touch display does not get it.

Each page leads with one clear primary action, visually distinct from every secondary one, and the primary action is the only thing on its page wearing the accent.

The product commits to two designed presentations and no third: the scene routes and the console carry light ink on a dark field, and the document routes, the catalogue and the citizen directory carry dark ink on a light field. Both are designed fully, the theme belongs to the route rather than to a visitor preference, and there is no separate theme switch to design or to judge. Every component inverts correctly on either field because it reads its ink from the surface it sits on.

What this must not look like: no page dominated by a single hue family with no second signal; no decoration standing in for content; no marketing composition where the working interface belongs; no roster, catalogue or file list that reads as a template with this product's nouns dropped into it. The exact shades, sizes, spacings and durations are yours, so long as every rule above holds.

## Technical requirements

The frontend is Preact with Vite, built for production and served by a static or preview server. The backend is Litestar on Python 3.12, serving the HTTP interface under the `/api` prefix on the same origin. The browser receives an application shell on first paint and the interface data arrives as JSON over that same origin; route changes after the first paint are resolved in the browser without a full document request. The datastore is PostgreSQL, read from `DATABASE_URL`. The object store is MinIO, read from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The public origin and port are read from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port. Authentication is app implemented: email and password, hashed passwords, bearer tokens. `GET /api/health` returns `200` once the app is ready.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation.

**Route metadata.** Every public route carries its own title and its own description, and no two routes share either. Landing directly on a deep address returns the same page a visitor reaches by navigating to it, with that route's own title and description, so a shared link opens correctly rather than on the home route.

**Delivery paths and caching.** Three paths exist and their cache policies are never merged for convenience. Content addressed objects in the bucket, meaning the packed catalogue index, the Keeper images and the media files, are immutable and long lived; a change publishes a new name and nothing is ever invalidated in place. Page responses from the origin are short lived and revalidated. Anything carrying citizen data is not cached at any tier: no response containing a citizen's record, holdings, renders or achievement files may carry a cacheable directive, at the edge, at the origin or in the browser. A shared cache serving one citizen's page to another is the worst failure this product can have.

**The packed index.** It is published to the bucket under a content addressed name and fetched once per session. It is not re-fetched when the visitor moves between the catalogue and the filters route. Parsing it does not block the interface: it is parsed away from the work that keeps the page responsive, or in chunks that yield, so that a mid-range phone never freezes while reading it. Filtering runs off the main work where the platform offers somewhere to run it, falling back to the chunked approach, and the chunked approach is the specified behaviour while the other is the optimisation, in that order, so the product is correct before it is fast.

**Object keys and privacy of objects.** Citizen passport documents and achievement files are private objects: they are never publicly readable, and every access is a short lived address minted per request for the owner only. Media downloads are likewise minted per activation. Nothing in the product hands out a bucket path.

**Secrets and public configuration.** The storage credentials and the session signing material live in the server environment only and never reach the browser. No credential, API key or admin token appears in anything the browser downloads: not in a script bundle, not in a JSON payload, not in an HTML attribute, not in a source map. Public runtime configuration is limited to the public origin, the collection size, the identifier shift and the asset prefix, and nothing else crosses.

**Interface conventions.** Three conventions hold across every operation rather than being restated per endpoint. Every request carries a request identifier, generated by the server when the client does not supply one, echoed in the response and present in every log line for that request and in every audit row it writes. Every write carries an idempotency key, and a repeated key returns the first response rather than doing the work again. Every response that could be personalised carries a no-store directive, because the failure that convention prevents, a shared cache serving one citizen's page to another, is the worst failure this product can have.

**What is instrumented, and what alerts.** Logs are structured, one line per request, carrying the identifier, route, status, duration and the actor address where a session exists. A nickname or a biography never appears in a log line. Errors return a stable machine readable code, a message safe to display, and the request identifier, and never a stack trace, a query or a storage key. Counters exist for registrations, bindings, profile writes, awards and regeneration requests, and for generation depth, the age of the oldest queued face and the failure rate. An alert is raised on: any failed generation reaching its attempt limit; an oldest queued face older than the generation budget; a sustained rise in refused-as-forbidden responses, which is either a defect or an attempt; a sustained holdings failure rate before the read quota is exhausted; and any failure to mint a download or document address, because that breaks every document and every download at once. The holdings ledger stands in for an external ownership indexer, and its read budget is tracked per-address and alerted before exhaustion rather than after it.

**Rate limits.** The binding challenge is limited per address and per source. Verification is limited per address. Profile writes are limited per session. Regeneration is limited per citizen per day and deduplicated while a run is in flight. Holdings reads carry a minimum interval per address independent of the caller, so a page refresh loop cannot consume the budget. The catalogue and the static objects are not limited. A refused request answers with a retry hint.

**Degradation.** The product has a defined order in which capability is given up, and the visitor can find out where they are on it: full, with scenes, sequences, audio, smooth scroll and all motion; reduced, with sequences cut to their endpoints and audio on demand; still, with one image per scene section and no sequence playback; flat, with no scene, static fields, and scrubbed motion replaced by ordinary reveals; document, with native scrolling and content only. Each rung is reachable by detection and by explicit preference. A visitor reporting that the site looks broken is usually a visitor who has been silently dropped two rungs without being told.

**Failure behaviour.** With the seeded editorial records unreadable, every editorial route serves its last successful render with a stale marker and the site stays readable. With the holdings ledger unreadable, citizen pages render from the cache with a stale marker on holdings, and a write that needs ownership is refused with a clear reason. With the generation queue unavailable, profile writes still succeed and the affected faces stay pending until the queue returns. With the object store unavailable, the catalogue stays usable and items show placeholders. In no failure mode does the catalogue become unreadable. With no hardware rendering, every route is readable and navigable. With browser storage blocked entirely, the site renders correctly on default preferences: every read of it is wrapped so a blocked store yields defaults rather than an error, and it holds preferences only, never a token, never an address and never any part of a citizen record.

**Performance.** The catalogue route paints before the index arrives and becomes interactive quickly after it. A filter change paints its first result promptly and no single piece of filter work holds the main work long enough to drop a frame. Scene sets are prefetched as units ahead of their scroll range with a ceiling on how many are in flight, prioritised by scroll direction, and a reversal of direction reprioritises rather than cancelling so a visitor who scrolls up and back down does not pay twice. A save-data or metered-connection signal reduces each set to its endpoints. A detached scene set releases what it held rather than retaining it, because a scene layer that only ever allocates exhausts a device on a long session. No uncompressed audio is delivered to a visitor. A first visit to the story route stays within a small fraction of the collection's total asset weight, and layout does not shift as content arrives.

**Assets.** This is a zero-asset build and the substitution for every binary is specified rather than left open: nothing in this build requires a binary asset to be supplied. Keeper artwork, journal heroes, media previews and the scene sequences are generated: a deterministic generator keyed by an item's content digest derives a hue, two accent hues and a composition seed, and renders a soft radial field with two overlapping silhouettes over a hairline grid, so the same digest always produces the same picture and the collection is visibly varied. The same generator produces the background colour the citizen palette is derived from, so that palette exercises its full range rather than one colour. Scene objects are composed from primitive geometry lit by a key, a fill and a rim, and every scene object keeps the name the scene code addresses it by, because a renamed substitute is silently absent. Audio cues are built from oscillators and filtered noise on a shared bus, and are built lazily on first unmute so a visitor who never unmutes never pays for an audio context. Surface grain is generated rather than shipped. Icons ship as inline vector geometry in the document rather than as a sprite sheet, an icon font or a request.

**Rendering discipline.** The pixel ratio used for every drawn surface is clamped, because an uncapped high density display multiplies the pixel count of a full window scene for no perceptible gain. Rendering pauses when the document is hidden, when the scene is out of view and after a configured idle period. One observer computes the scale and notifies its subscribers, and no component reads the window for itself. One frame loop drives every per-frame consumer, consumers register with a priority, and every consumer tolerates an arbitrary gap between frames rather than assuming a fixed step. A layer promotion hint is applied to an element that is actually about to change and removed afterwards, never declared across hundreds of elements at once, which promotes more layers than the compositor can hold and is slower than not declaring it at all. Development affordances such as camera controls and post-processing toggles are compiled out of the production build rather than defaulted off.

**Input handling.** The nickname and the biography are validated on the server, stored as text, escaped at render and never interpolated into markup. Console input is echoed as text only. Stored structured documents are rendered through the node resolver and never as raw markup. An address parameter is validated before use and a malformed one fails closed. An identifier search is parsed as an integer and range checked before it reaches any query. A signed parameter is verified before any work is done, not after.

## Data model

Eleven core tables plus the account table. All timestamps are UTC, every timestamp column is a timestamptz, every address column is a fixed-width char of forty two characters, every digest column is a fixed-width char of sixty four, the request identifier is a uuid, and a flag column is a boolean whose default is false. A column described below as nullable holds null where nothing has been set; every other column is not null.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**account.** `id`, `email` unique and matched lowercased, `password_hash`, `created_at`, `status` one of `active`, `suspended`, `deleted`.

**citizen.** `address` as the primary key in its display spelling, `address_lower` derived lowercase and unique, `account_id` unique and referencing account, `bound_at`, `created_at`, `updated_at`, `last_seen_at` nullable, `status` one of `active`, `suspended`, `deleted`. Lookup happens on the lowercase column and never on the display one, so a request carrying either spelling resolves; the display column is what is shown. One account binds at most one address and one address is bound by at most one account.

**profile.** `address` as primary key referencing citizen and cascading on delete, `nickname` nullable up to `24` characters, `nickname_normalised` derived lowercase with interior whitespace collapsed, `bio` nullable up to `280` characters, `representative_token_id` nullable referencing token, `updated_at`. Two citizens cannot hold the same normalised nickname at the same time. A citizen who has never set one collides with nobody, because the uniqueness applies only where a nickname is present. This holds under two simultaneous writes of the same nickname: exactly one succeeds and the other is refused.

**render.** Primary key on `address` and `face`, where `face` is one of `document_front`, `document_back`, `share_image`. `object_key`, `state` one of `pending`, `ready`, `failed`, `failure_reason` nullable, `last_updated`, `content_hash`. The content hash is a digest of the nickname, the biography, the representative Keeper identifier, that Keeper's image digest, the sorted earned achievement identifier list and a template version. A run whose computed hash equals the stored hash for a face produces nothing.

**sector.** `id`, `name`, `position`.

**achievement.** `id`, `kind` one of `mark` or `badge`, `sector_id` referencing sector, `name`, `description`, `difficulty` one of `standard`, `rare` or `elite`, `points` which is always greater than zero, `published_at` nullable where null means invisible.

**achievement_file.** `id`, `achievement_id` referencing achievement and cascading on delete, `kind` one of `img`, `video` or `audio`, `title`, `object_key`, `fill_background`.

**citizen_achievement.** Primary key on `address` and `achievement_id`, plus `awarded_at`, `awarded_by` naming the run or operator that awarded it, and `evidence` recording why. The composite key is what makes awarding idempotent: an evaluation that runs twice awards nothing the second time.

**holding_ledger.** Primary key on `address_lower` and `token_id`. This is the authority for ownership. Every write that needs to know what an address holds reads this.

**holding_cache.** Primary key on `address` and `token_id`, plus `observed_at` and `source` one of `ledger` or `manual`. This is a cache and is treated as one: it serves reads and is never the authority for a write.

**token.** `id` as the display index from zero to nine thousand nine hundred and ninety nine, `on_chain_id` unique and derived by the shift of `5022` wrapping at `10000`, `image_digest`, `background_color` which is the source of the derived citizen palette.

**trait.** `id` as the index used in the packed catalogue, `name` unique, `position`.

**trait_value.** Primary key on `trait_id` and `value_index`, plus `name` and `count`, where the count is the occurrence total used for the rarity shown in the detail overlay.

**token_trait_value.** Primary key on `token_id` and `trait_id`, with a foreign key on the trait and value pair referencing trait_value. A Keeper carries at most one value per trait, which the packed catalogue format cannot express on its own. A Keeper missing a trait is normal and a Keeper carrying two values for one trait is corruption.

**session_challenge.** `id`, `address`, `account_id`, `nonce` unique, `statement`, `issued_at`, `expires_at`, `consumed_at` nullable, `revoked_at` nullable. A row is created when the challenge is issued and the same row is consumed when it is verified. A row with a consumed timestamp can never be consumed again, and two simultaneous verifications of one nonce produce exactly one binding.

**audit_log.** `id`, `at`, `actor_address` nullable, `action`, `subject`, `before`, `after`, `request_id`, `ip_hash` nullable. Every profile write, every achievement award, every binding verification, every deletion and every generation outcome writes one row, and the row is written in the same transaction as the change it records. An audit trail written outside the transaction that changed the data disagrees with the data the first time a write fails halfway. The table is append only: the application role holds insert and select on it and holds neither update nor delete.

**Editorial tables.** `journal_entry` carries `slug` unique, `title`, `category` one of `updates`, `community` or `finders_lab`, `published_at`, `hero_key`, `body` as a structured document and `author`. `media_item` carries `id`, `title`, `media_kind` one of `image`, `video` or `audio`, `object_key`, `published_at`, `byte_size` and `file_format`. `roster_member` carries `id`, `display_name`, `role`, `position` and an optional `link`. `legal_document` carries `slug`, `title`, `body` as a structured document and `last_updated`. `console_command` carries `input` unique and `response` as a structured document.

**Derived rather than stored.** The citizen's point total, earned count and total count; the on-chain identifier shown beside a display index; a trait value's rarity share; the roster index number shown on a card; the media type counts; and every colour on a citizen page.

**Seed data.** `10000` tokens across `13` traits with the value counts pinned in Core features, each with a distinct image digest and background colour. Three accounts, all using the corpus password: `member@example.com` bound to `0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801` holding three Keepers with all three faces already `ready`; `member2@example.com` bound to `0xB2c4E5d6F7a8B9c0D1e2F3a4B5c6D7e8F9a0B102` holding two Keepers with all three faces already `ready`; and `member3@example.com` bound to `0xC3d5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1D203` holding none. Eight achievements across three sectors, of which `member@example.com` has earned three and `member2@example.com` has earned one, with one achievement left unpublished so its invisibility is observable. Six journal entries spread across the three real categories. Seventy one media items split thirty one images, thirty four videos and six audio files. Six roster members. Three legal documents. Four console commands, one of which is `connect_citizens`. Seeding is idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual and structural detail the product is held to. It states what must be true, in words. Every exact value, every shade, every duration and every measurement is the builder's to choose, so long as the relationships below hold.

### The frame

A persistent chrome sits above the route outlet and does not unmount on navigation, which is what lets its state, its open menu and its audio context survive a route change. It is four hairline edges inset from the window on every side, enclosing the route content, and it renders in one of two themes: light ink on a dark field, or dark ink on a light field. The theme is set by the route and animated on a route change rather than switched. Each edge is drawn as its own element so the edges can be animated independently, which a single border on one container cannot do. The content region is clipped to the frame's inner rectangle, so a full bleed scene renders at full window size and is masked rather than being sized to fit, which is what lets it survive the frame animating without re-rendering.

The frame has three parts in order of prominence. The burger sits in its top left corner and is present on every route. The route submenu sits top centre and its contents depend on the route. The action slot sits top right and its contents depend on identity state.

### The burger and the menu

The burger is two horizontal strokes of unequal length, the lower shorter than the upper, which is what stops it reading as every other menu button. On hover it acquires a visible border which arrives from fully transparent to solid, on a control whose only softened corner is the top left one. Opening the menu plays the menu open cue, traps focus inside the menu, renders the full route list as a vertical stack with per item hover, renders the language and region selectors, and renders the community links. It closes on the escape key, on the burger, and on selecting a route. While the menu is animating open or closed it accepts no pointer input, because a menu that takes a click mid animation navigates to whatever happened to be under the cursor when it started.

### The route submenu

| Route | Submenu |
|---|---|
| Story | `Project`, `The Hold`, `Factions`, `The World` |
| Protocol | `VISION`, `WORLD`, `CHARACTERS`, `PORTAL`, `UNION` |
| Gallery | `KEEPERS COLLECTION`, `MY COLLECTION` |
| Journal | `ALL`, `UPDATES`, `COMMUNITY`, `FINDERS LAB` |
| Media | `ALL`, `IMAGE`, `VIDEO`, `AUDIO`, each with a live count |

On Story and Protocol the submenu items are in-page anchors that scrub the scroll position rather than jumping. On Gallery, Journal and Media they are filter states reflected in the address, so a filtered view is linkable and survives a reload.

### The action slot

| Identity state | Control | Behaviour |
|---|---|---|
| Signed out | `SIGN IN` | Opens the sign-in route |
| Signed in, no address bound | `CONNECT WALLET` | Opens `/registration` |
| Signed in, address bound | The abbreviated address plus `DISCONNECT` | Disconnect revokes the binding on the server |

The address is abbreviated as its first six characters, an ellipsis, then its last four. A second, longer abbreviation of the first eighteen and the last seven is used on the citizen page, where there is room for it.

### The audio control and the footer

The audio control is a circular control showing a small level meter, with the label `CLICK TO ENABLE SOUND` beneath it while muted and `CLICK TO MUTE SOUND` once unmuted. Audio starts muted and never auto-plays; this control is the only thing that unmutes; its state lasts the session. Muting mutes everything at one place rather than pausing individual sources.

The footer is present on scrollable routes and absent on the pinned scene routes. It carries the studio credit `SITE BY Studio North`, the rights line `KEEPERS OF THE REACH. ALL RIGHTS RESERVED.`, the community links under the label `CONNECT ON`, the links to all three legal routes including the privacy page, the brand pack download, and a contact address.

### The warning overlays

Two overlays render above everything. A widescreen warning appears when the window aspect is wider than the supported maximum and asks the visitor to narrow the window. An orientation warning appears when a touch device is held in landscape and asks the visitor to rotate. Both are dismissed by resolving the condition, and both offer a continue-anyway control after a short delay, so a visitor on a display that cannot rotate is never locked out.

### Iconography

Every symbol ships as inline vector geometry in the document: no sprite sheet, no icon font, no request, nothing that can go blurry and nothing that adds a loading state. Each icon is specified by its drawing box and its primitives so it reproduces exactly at any scale.

The achievement marks come in two families distinguished by silhouette. The common achievement is a flat topped hexagon; the rare achievement is an elongated shield. Each is drawn as a filled shape inside a ring, and the ring is what carries the earned state: unearned, the ring sits shrunk slightly inside where it belongs, so the moment the achievement is earned the ring snaps outward to full size. Each mark carries a glow behind it whose intensity is driven by hover and by earned state, and a difficulty class that changes the mark's colour treatment and never its geometry.

The console window chrome is one shape with a cut top right corner and a cut bottom right corner that are deliberately different sizes, a stroke in the console's own blue over a mostly opaque dark fill, a horizontal rule separating the title bar from the body, and a close glyph built from two short diagonal strokes.

A tall vertical crosshair mark sits at a fixed offset from the frame's left edge, vertically centred, on every route. It is the one icon that is positioned rather than inline, and it is decorative.

### Layer order

One owned stacking order governs the whole product and no component invents a value outside it. From back to front: the persistent frame, the footer, ordinary overlays such as popups and the media detail, the resize and orientation warnings, the preloader, the full-screen menu, and the console. A development overlay exists in development only and never ships.

### Viewport height

Full height surfaces do not resize when a mobile browser's address bar retracts. The height is recorded once and held, so a scene pinned to the window does not jump mid scroll when the browser chrome slides away. The native scrollbar is suppressed by the smooth scroll, its width is measured and accounted for, and the layout does not shift when it disappears.

### The scroll and scrubbing system

The document body is held still and a content wrapper is moved in response to wheel, touch and keyboard input, lagging the input and catching up over several frames, while the native scroll position stays the source of truth so browser find, anchors and the back button keep working. Position and rotation are carried on separate nested elements rather than composed into one transform, so each can be driven from a different scroll range with a different curve. A reveal is built from a nested pair of mask elements travelling in opposite directions, a mask-outer holding a mask-inner, which produces a wipe with a moving band rather than a single travelling edge. The same pairing appears at the top and the bottom of a section, so a section opens from both edges at once. A progress element is scrubbed on every route, scaled on its horizontal axis from nothing to full rather than translated, and sits at an opacity low enough to be almost invisible.

At the narrow width the scrubbed set reduces to a background drift, a single parallax layer and the smooth scroll itself. That reduction happens by not creating the reduced timelines at all, not by creating them and skipping them, because the cost being avoided is the layout and paint work rather than the arithmetic.

### The scene layer

The story and protocol routes render a real time three dimensional scene behind the interface, full window, masked to the frame's inner rectangle. It holds a smooth frame rate on a three year old laptop with integrated graphics, pauses entirely when the tab is hidden or the scene is scrolled out of view, presents a complete legible page when hardware rendering is unavailable, and never blocks the first paint of the surrounding interface.

Behind and between the three dimensional passes, the scenes play sequences of still frames rather than video, so each frame can be held against a scroll position instead of played on a clock. Five scenes exist by name: an establishing scene, a home scene, a factions scene, a universe scene and a transition scene. The frame format is negotiated at run time against what the rendering context supports, preferring a compressed texture format that uploads directly to the graphics device, then a modern lossy still format the browser decodes, then a lossless still as the final fallback: the compressed format costs more network to save main-thread time, and that trade is deliberate. A sequence is never requested frame by frame as the visitor scrolls; each set is prefetched as a unit ahead of its scroll range with a ceiling on concurrency, and the scroll range consuming it refuses to advance past the last decoded frame rather than showing a gap.

Two overlay effects carry the scenes' character. A threshold filter blurs a layer heavily and then raises its contrast hard, which snaps soft edges into merging blobs like drops of liquid running together; the blur and the contrast move together, because raising one without the other produces a smear rather than a merge. It is the cheapest expensive-looking effect in the product. Blend modes carry the rest: one overlay mask multiplies its light against the field, another darkens. A band of the about route's indigo, fading to nothing at both ends, travels down the roster as the visitor scrolls, lighting each card as it passes. That band is the entire motion design of the about route and it is one element, which is worth knowing before somebody builds it as fifty separate animations.

The catalogue's preview stack is a real three dimensional card arrangement in perspective with its nested cards preserving depth, not a two dimensional simulation of one.

Fourteen audio cues exist in three groups: interface cues for menu open, menu close, menu rollover and menu text rollover, which are short and dry; scene cues for the intro animation, the logo intro, three carousel positions, a flow transition, a transition, a text animation loop and a press sheen, which are musical and layered; and one long looping low wind ambience. The ambient bed cross-fades between scenes rather than stopping and starting. Interface cues are pooled so a rapid run of hovers reuses one instance rather than allocating one per event.

### The card mask and the About field

Each roster card sits on a non-rectangular field produced by a parametric generator: a rounded rectangle with one corner cut, at the card's aspect, emitted as vector markup and used directly as a mask. Two aspects, one generator, which is strictly better than shipping two vector files because it scales with the interface.

### Module and component architecture

Layers are routes, layouts, chrome, surfaces, primitives, scene, state and platform, and dependencies point downward only. A primitive may not reach up into a state store and the scene layer may not reach into a surface. There are four state stores with clear ownership: identity owns the account, the bound address, the errors and the session; catalogue owns the packed index, the facets, the applied filters, the results and the selection, and persists only through the address bar; citizen owns the assembled record for the current citizen route and persists nothing; application owns the scale, the viewport, the pointer, the mute state, the theme, the route and the scene flags, and persists preferences only.

Errors are held as a list with explicit clearing rather than as a single current-error field, because more than one error can be true at once and each is independently resolvable. The pointer is exposed in two derived forms, one running from zero to one for interface work and one running from minus one to one with the vertical axis inverted for the scene layer, because deriving one from the other at every use site is where sign errors come from.

### Responsive behaviour, per route

| Route | Wide | Narrow |
|---|---|---|
| Story | Pinned scene, four sections, carousel | Scene reduced to key stills, sections become a scrolling document |
| Protocol | Scene with the hold control | Static field, the narration as an expandable panel |
| Gallery | Facet rail beside a multi-column card grid | Fewer columns, facets move to `/filters` |
| Citizen | Documents side by side, achievements as a grid | Documents stacked, achievements as a list |
| Journal | Hero plus grid | Single column, hero unchanged |
| Media | Preview beside the file data column | Preview above the file data, list below |
| About | Roster grid with diagonals | Single column cards, diagonals dropped |

### Copy

Every string in the interface is keyed and externalised rather than written inline, and no sentence is assembled by joining fragments, because the fragments reorder in translation. Every string is reachable in Japanese. The functional labels pinned in Core features and in the tables above are reproduced exactly.

## Constraints

- One collection of `10000` Keepers and `13` traits. There is no second collection, no second chain, no second contract.
- No minting, no trading, no payment of any kind, no wallet transaction. The mint route presents a closed state.
- No comments, no likes, no direct messaging, no following, and no social graph between citizens.
- No administrator or editor surface inside the application. Editorial rows are seeded.
- No outbound email, no SMS, no push notification, no third-party analytics service, and no outbound network call at run time to anything other than PostgreSQL and MinIO.
- No native application, no browser extension, no offline installation.
- No personal field ever leaves the product: an address may be logged, a nickname and a biography never are, and neither ever reaches any external destination.
- The app must stay responsive with `10000` tokens in the catalogue, `13` facets with `373` values between them, seventy one media items, and a citizen record carrying its full achievement catalogue, without the catalogue route becoming unusable.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ "email", "password" }` | the created account and a bearer token |
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "token", "account" }` |
| `POST /api/auth/logout` | none | empty on success; the presented token is revoked |
| `GET /api/health` | none | `{ "status": "ok" }` |
| `POST /api/session/challenge` | `{ "address" }` | `{ "statement", "nonce", "domain", "issued_at", "expires_at" }` |
| `POST /api/session/verify` | `{ "address", "nonce" }` | the bound citizen record |
| `POST /api/session/revoke` | none | empty on success; the binding is revoked server side |
| `GET /api/session` | none | the current account and bound address, or nothing |
| `GET /api/citizens` | `?q=&limit=&offset=` | a top-level JSON array of public citizen summaries |
| `GET /api/citizens/<address>` | none | the assembled record; `renders` present for the owner only |
| `PATCH /api/citizens/<address>/profile` | `{ "nickname"?, "bio"?, "representative_token_id"? }` | the updated profile and the current render state |
| `DELETE /api/citizens/<address>` | none | empty on success, owner only |
| `GET /api/citizens/<address>/holdings` | none | `{ "success", "has_citizen_record", "holdings", "observed_at", "stale" }` |
| `GET /api/citizens/<address>/renders` | none | per face `{ "state", "url", "last_updated" }` plus a suggested poll interval, owner only |
| `POST /api/citizens/<address>/renders` | `{ "faces"? }` | the run in flight or a newly started one, owner only |
| `GET /api/achievements` | none | a top-level JSON array of published achievements with their sectors |
| `GET /api/catalogue` | none | `{ "index_url", "token_count", "trait_count", "id_shift" }` |
| `GET /api/tokens/<id>` | none | one token with its traits, rarities and both identifiers |
| `GET /api/journal` | `?category=` | a top-level JSON array of entries |
| `GET /api/journal/<slug>` | none | one entry with its structured body |
| `GET /api/media` | `?kind=` | a top-level JSON array of items with the per-kind counts |
| `POST /api/media/<id>/download` | none | a short lived address for that one item |
| `GET /api/roster` | none | a top-level JSON array of roster members |
| `GET /api/legal/<slug>` | none | one legal document with its structured body |
| `GET /api/console/commands` | none | a top-level JSON array of seeded commands |

Every list endpoint returns a top-level JSON array. Bearer authentication is required on everything except signup, login, health and the public reads above. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success, carrying a stable code, a displayable message and the request identifier. The stable codes are `session_required`, `session_address_mismatch`, `citizen_not_found`, `nickname_taken`, `nickname_invalid`, `bio_too_long`, `token_not_owned`, `address_already_bound`, `challenge_expired`, `rate_limited`, `ledger_unavailable` and `render_in_flight`.

### No mocks

MinIO is the only place the passport documents, the achievement files, the media files and the packed catalogue index actually live. Each of the following is a contract violation however good the interface looks: an in-memory table of documents, image bytes written to the app container's own filesystem, a PostgreSQL column holding an image, a hardcoded success response the app returns to itself instead of writing an object, a public bucket policy standing in for a minted address, or a catalogue index compiled into the JavaScript bundle instead of published as an object. The named provider is the fact: the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor with no account can scroll the story with sound off, narrow ten thousand Keepers to a handful across thirteen traits, open one and reach its licence, read a journal entry and download a press file. Somebody who signs up can bind an address by returning the challenge phrase the server issued, and the same phrase never works twice. Their citizen page carries their nickname, their representative Keeper and their achievements, and its three passport documents live in the bucket and open only for them. Another citizen sees that page's public half and nothing more, and a direct request for its private half or a write to it is refused with the record unchanged.
