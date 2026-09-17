# Checklist: deku/immersive-experience-showcase-vb

Items: 324
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Unpinned values flagged: 6

## C-OV Overview

- [ ] `C-OV-01` `capability` A producer writes anything, publishing nothing. `src: Overview`
- [ ] `C-OV-02` `capability` A virtual scroller captures wheel, touch, key input, integrating each into one offset. `src: Overview`
- [ ] `C-OV-03` `constraint` The product ships no photograph, no video file, no model, no font binary, no sound file. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` Only an editor may add a discipline term. `src: User roles`
- [ ] `C-RL-02` `role` An anonymous visitor cannot read any unpublished record on any route. `src: User roles`
- [ ] `C-RL-03` `role` A signed in producer asking through a public route reads no unpublished record either. `src: User roles`
- [ ] `C-RL-04` `role` A producer revokes only the tokens that producer minted. `src: User roles`
- [ ] `C-RL-05` `role` A producer moving a record to the live state is denied by the server. `src: User roles`
- [ ] `C-RL-06` `role` The stored state is untouched after a refused publish attempt. `src: User roles`
- [ ] `C-RL-07` `role` An editor moves a record to the live state, along with the withdrawn state. `src: User roles`
- [ ] `C-RL-08` `role` No role, the editor included, holds a capability removing a log row. `src: User roles`
- [ ] `C-RL-09` `role` A producer calling the reel reorder endpoint is denied. `src: User roles`
- [ ] `C-RL-10` `role` The stored reel order is unchanged after a refused reorder. `src: User roles`
- [ ] `C-RL-11` `role` Deleting a media master requires the editor role. `src: User roles`
- [ ] `C-RL-12` `role` A draft image leaks no more than the draft text does. `src: User roles`
- [ ] `C-RL-13` `role` No response tells an anonymous caller whether an address sits on the list already. `src: User roles`
- [ ] `C-RL-14` `contract` Authorization is enforced on the server for every mutating endpoint. `src: User roles`
- [ ] `C-RL-15` `constraint` Hiding a control in the interface is not authorization. `src: User roles`
- [ ] `C-RL-16` `contract` A direct call from an anonymous session to a console endpoint is denied. `src: User roles`
- [ ] `C-RL-17` `contract` The protected state is unchanged after a denied call. `src: User roles`
- [ ] `C-RL-18` `contract` A role is read from the session, never from the request body. `src: User roles`
- [ ] `C-RL-19` `literal` The seeded accounts are `producer@example.com`, `producer2@example.com`, `editor@example.com`. `src: User roles`
- [ ] `C-RL-20` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `literal` The seeded discipline vocabulary is `Design`, `Experience`, `3D`, `Tech`, `Strategy`, `Branding`, `E-shop`, `Web3`, `NFT`, `Film`. `src: Core features`
- [ ] `C-CF-02` `contract` The disciplines endpoint returns the ten terms in position order. `src: Core features`
- [ ] `C-CF-03` `constraint` A discipline is a controlled vocabulary entry rather than a free text string. `src: Core features`
- [ ] `C-CF-04` `contract` A producer posting a discipline outside the vocabulary is refused as invalid. `src: Core features`
- [ ] `C-CF-05` `contract` The projects endpoint returns every published case study without pagination. `src: Core features`
- [ ] `C-CF-06` `data` The seeded index carries sixteen published entries. `src: Core features`
- [ ] `C-CF-07` `literal` The index opens `Arven`, `Aurel Vance Experience`, `Chastenay Belfort`, `Faiseurs d'Ourcq`, `Grale`, `Halom`. `src: Core features`
- [ ] `C-CF-08` `literal` The index closes `Verrine Watchmaking Salon 24`. `src: Core features`
- [ ] `C-CF-09` `constraint` The captured index order is alphabetical by title across every project type. `src: Core features`
- [ ] `C-CF-10` `capability` A title opening with a diacritic sorts where a reader expects. `src: Core features`
- [ ] `C-CF-11` `contract` A record whose state is not published is absent from every public endpoint response. `src: Core features`
- [ ] `C-CF-12` `literal` The seeded records awaiting sign off are `marivella`, `oryx7`. `src: Core features`
- [ ] `C-CF-13` `contract` The public route of an unpublished record answers not found. `src: Core features`
- [ ] `C-CF-14` `contract` The sitemap omits every unpublished route. `src: Core features`
- [ ] `C-CF-15` `literal` A preview token is `prv_` followed by thirty two lowercase hexadecimal characters. `src: Core features`
- [ ] `C-CF-16` `literal` The worked preview token is `prv_6d1f4a08c39b27e5d0a4f81c6b3e97d2`. `src: Core features`
- [ ] `C-CF-17` `contract` The preview endpoint verifies the token on the server before returning the record. `src: Core features`
- [ ] `C-CF-18` `capability` A preview response carries the record in the draft state. `src: Core features`
- [ ] `C-CF-19` `contract` A token naming a different record answers not found. `src: Core features`
- [ ] `C-CF-20` `contract` A guessed token answers not found. `src: Core features`
- [ ] `C-CF-21` `contract` An expired token answers not found. `src: Core features`
- [ ] `C-CF-22` `capability` An editor revokes every outstanding token for a record in one action. `src: Core features`
- [ ] `C-CF-23` `contract` A revoked token answers not found without delay. `src: Core features`
- [ ] `C-CF-24` `constraint` A preview token is stored as a hash rather than as the value. `src: Core features`
- [ ] `C-CF-25` `contract` Every preview response refuses indexing along with archiving. `src: Core features`
- [ ] `C-CF-26` `constraint` The preview route is never prerendered. `src: Core features`
- [ ] `C-CF-27` `contract` Minting a preview token returns the value once. `src: Core features`
- [ ] `C-CF-28` `constraint` No endpoint returns a minted token value a second time. `src: Core features`
- [ ] `C-CF-29` `capability` A preview token expires at a fixed interval from minting. `src: Core features`
- [ ] `C-CF-30` `capability` A preview token expires on the record reaching the live state. `src: Core features`
- [ ] `C-CF-31` `capability` A producer moves a record from draft to review, along with the reverse. `src: Core features`
- [ ] `C-CF-32` `literal` The four record states are `draft`, `in_review`, `published`, `unpublished`. `src: Core features`
- [ ] `C-CF-33` `constraint` A record is never deleted, being withdrawn instead. `src: Core features`
- [ ] `C-CF-34` `contract` Publishing is refused when a referenced media is not ready. `src: Core features`
- [ ] `C-CF-35` `contract` A refused publish names the failing record. `src: Core features`
- [ ] `C-CF-36` `data` The seeded record `oryx7` references a media still being derived. `src: Core features`
- [ ] `C-CF-37` `constraint` A refused publish writes no log row of outcome succeeded. `src: Core features`
- [ ] `C-CF-38` `constraint` The refusal on a missing subtitle sits at the storage layer rather than in the console. `src: Core features`
- [ ] `C-CF-39` `contract` A reel section of zero duration is refused on write. `src: Core features`
- [ ] `C-CF-40` `capability` A reel total duration is the sum of the section durations. `src: Core features`
- [ ] `C-CF-41` `contract` Every transition writes one log row. `src: Core features`
- [ ] `C-CF-42` `data` A log row carries the instant, the acting account, the record type, the record slug, the state moved from, the state moved to, the outcome, the routes invalidated. `src: Core features`
- [ ] `C-CF-43` `constraint` The publish log is append only. `src: Core features`
- [ ] `C-CF-44` `contract` The publish log endpoint returns rows newest first. `src: Core features`
- [ ] `C-CF-45` `literal` The seeded home reel order is `lambert-vitrine`, `grale`, `verrine-end-of-year-23`. `src: Core features`
- [ ] `C-CF-46` `contract` The home reel endpoint returns the three entries in the stored order. `src: Core features`
- [ ] `C-CF-47` `data` A reel entry carries a title, a type, a description, a media of the entry's own. `src: Core features`
- [ ] `C-CF-48` `capability` Reordering the home reel is an editor capability. `src: Core features`
- [ ] `C-CF-49` `constraint` Adding a project to the collection changes the home page for nobody. `src: Core features`
- [ ] `C-CF-50` `constraint` The home reel is an ordered editorial subset rather than a query with a limit. `src: Core features`
- [ ] `C-CF-51` `data` The published record `aurel-vance-experience` sits off the reel. `src: Core features`
- [ ] `C-CF-52` `capability` A reel entry whose project is withdrawn disappears from the reel. `src: Core features`
- [ ] `C-CF-53` `constraint` No reel entry renders pointing at a missing page. `src: Core features`
- [ ] `C-CF-54` `contract` A master is stored unmodified in object storage, keyed by content hash. `src: Core features`
- [ ] `C-CF-55` `literal` A master key is `media/<content-hash>/master.<ext>`. `src: Core features`
- [ ] `C-CF-56` `capability` Intrinsic dimensions, a duration where one exists, a media type are extracted on upload. `src: Core features`
- [ ] `C-CF-57` `literal` A rendition key is `media/<content-hash>/<variant>.<ext>`. `src: Core features`
- [ ] `C-CF-58` `literal` The worked rendition key is `media/9f2ad0c4/medium.avif`. `src: Core features`
- [ ] `C-CF-59` `literal` The still ladder variants are `placeholder`, `xs`, `sm`, `md`, `lg`, `xl`. `src: Core features`
- [ ] `C-CF-60` `constraint` Every rendition is content addressed, immutable, never overwritten. `src: Core features`
- [ ] `C-CF-61` `constraint` A rendition on the application container filesystem is a contract violation. `src: Core features`
- [ ] `C-CF-62` `constraint` A row holding the media bytes is a contract violation. `src: Core features`
- [ ] `C-CF-63` `constraint` A media marked ready whose object is absent from the bucket is a contract violation. `src: Core features`
- [ ] `C-CF-64` `literal` The media states are `uploaded`, `deriving`, `ready`, `failed`. `src: Core features`
- [ ] `C-CF-65` `contract` A media delete is refused when any record references the media. `src: Core features`
- [ ] `C-CF-66` `contract` A refused media delete lists the referencing records. `src: Core features`
- [ ] `C-CF-67` `capability` A successful media delete removes the master with every rendition. `src: Core features`
- [ ] `C-CF-68` `capability` Derivation is idempotent, so a rerun skips renditions already written. `src: Core features`
- [ ] `C-CF-69` `capability` Each rendition is written to a temporary key, then moved atomically. `src: Core features`
- [ ] `C-CF-70` `contract` A media belonging to an unpublished record is served only through an authenticated endpoint. `src: Core features`
- [ ] `C-CF-71` `constraint` A draft media is never served by a direct bucket address. `src: Core features`
- [ ] `C-CF-72` `contract` Resubmitting a known address returns the same response as a new address. `src: Core features`
- [ ] `C-CF-73` `literal` A malformed address is refused with the message `Invalid email format`. `src: Core features`
- [ ] `C-CF-74` `constraint` A refused intake writes nothing. `src: Core features`
- [ ] `C-CF-75` `constraint` Client validation is a courtesy, repeated in full by the server. `src: Core features`
- [ ] `C-CF-76` `capability` The intake form carries an unattended decoy field. `src: Core features`
- [ ] `C-CF-77` `contract` A submission filling the decoy field is refused, writing nothing. `src: Core features`
- [ ] `C-CF-78` `contract` A cross origin post from an unrecognised origin is rejected. `src: Core features`
- [ ] `C-CF-79` `constraint` A confirmation token is single use, expiring, held as a hash. `src: Core features`
- [ ] `C-CF-80` `constraint` Only a confirmed address sits on the list. `src: Core features`
- [ ] `C-CF-81` `contract` A second use of one confirmation token reports the same confirmation. `src: Core features`
- [ ] `C-CF-82` `constraint` A second use of one confirmation token re subscribes nobody. `src: Core features`
- [ ] `C-CF-83` `capability` Submitting the intake is the consent. `src: Core features`
- [ ] `C-CF-84` `contract` An outbound click records the project slug with nothing identifying. `src: Core features`
- [ ] `C-CF-85` `constraint` An outbound click is never recorded as a conversion. `src: Core features`
- [ ] `C-CF-86` `constraint` No measured event carries a personal identifier, a full address, free text. `src: Core features`
- [ ] `C-CF-87` `capability` Four events close the measurement loop, nothing else being measured. `src: Core features`
- [ ] `C-CF-88` `constraint` A slug may not change after a record has been published once. `src: Core features`
- [ ] `C-CF-89` `constraint` A slug is lowercase, hyphen separated, unique within the collection. `src: Core features`
- [ ] `C-CF-90` `contract` A slug colliding with a reserved word is refused. `src: Core features`
- [ ] `C-CF-91` `literal` A failed sign in answers `Incorrect email or password`. `src: Core features`
- [ ] `C-CF-92` `constraint` One wording answers a wrong password along with an address holding no account. `src: Core features`
- [ ] `C-CF-93` `constraint` Passwords are stored hashed, never in clear. `src: Core features`
- [ ] `C-CF-94` `capability` Sign in is rate limited per account, per source, with a progressive delay. `src: Core features`
- [ ] `C-CF-95` `capability` Signup is open, creating a producer. `src: Core features`
- [ ] `C-CF-96` `literal` The sitemap is served at `/sitemap.xml`. `src: Core features`
- [ ] `C-CF-97` `literal` The robots file is served at `/robots.txt`. `src: Core features`
- [ ] `C-CF-98` `contract` The robots file names the sitemap, refusing the preview route. `src: Core features`
- [ ] `C-CF-99` `capability` Every response carries a strict transport policy, a nosniff policy, a frame ancestors refusal, a referrer policy, a cross origin opener policy, a permissions policy. `src: Core features`
- [ ] `C-CF-100` `capability` The permissions policy denies camera, microphone, geolocation, payment. `src: Core features`
- [ ] `C-CF-101` `capability` The content policy enumerates every permitted connection target rather than wildcarding one. `src: Core features`
- [ ] `C-CF-102` `constraint` No inline script runs without a nonce. `src: Core features`
- [ ] `C-CF-103` `constraint` No credential, key, content host, store key, token appears in anything the browser downloads. `src: Core features`
- [ ] `C-CF-104` `literal` The seeded retired paths are `/cases/lambert-vitrine`, `/cases/vitrine`, `/cases/grale`. `src: Core features`
- [ ] `C-CF-105` `contract` A retired path resolves permanently in one hop to the project. `src: Core features`
- [ ] `C-CF-106` `contract` A retired path whose target is withdrawn resolves to the index route. `src: Core features`
- [ ] `C-CF-107` `contract` A chapter saved with a scene index outside the registered range is refused as invalid. `src: Core features`
- [ ] `C-CF-108` `constraint` A scene index is validated on save rather than on render. `src: Core features`
- [ ] `C-CF-109` `literal` The seeded chapter slugs are `where-we-started`, `how-we-work`, `what-we-refuse`, `the-people`, `the-craft`, `the-studio`. `src: Core features`
- [ ] `C-CF-110` `constraint` A chapter numeral label is stored rather than derived from position. `src: Core features`
- [ ] `C-CF-111` `contract` A project detail response carries the blocks, the disciplines, the reel relation. `src: Core features`
- [ ] `C-CF-112` `contract` The reel endpoint returns the reel for a published project. `src: Core features`
- [ ] `C-CF-113` `contract` The reel endpoint answers not found for a project that is not published. `src: Core features`
- [ ] `C-CF-114` `data` One reel is seeded against `lambert-vitrine`, carrying three sections. `src: Core features`
- [ ] `C-CF-115` `capability` The outbound control opens in a new browsing context, carrying no referrer, no opener relationship. `src: Core features`
- [ ] `C-CF-116` `constraint` A case study without a live address renders without the outbound control. `src: Core features`
- [ ] `C-CF-117` `capability` The backstage overlay pushes a history entry, so a back gesture returns to the case study. `src: Core features`
- [ ] `C-CF-118` `constraint` Subtitles render by default rather than as a setting. `src: Core features`
- [ ] `C-CF-119` `constraint` The control opening a reel is absent when the case study carries no reel. `src: Core features`
- [ ] `C-CF-120` `literal` The empty index line reads `Nothing published yet. Write to the studio.` `src: Core features`
- [ ] `C-CF-121` `literal` The not found headline reads `That page has moved on.` `src: Core features`
- [ ] `C-CF-122` `literal` The not found action reads `See all projects`. `src: Core features`
- [ ] `C-CF-123` `constraint` Every failure surface renders the same chrome, the same scene, the same footer as a working route. `src: Core features`
- [ ] `C-CF-124` `literal` The server error headline reads `Something is temporarily out of reach.` `src: Core features`
- [ ] `C-CF-125` `literal` The server error retry control reads `Try again`. `src: Core features`
- [ ] `C-CF-126` `literal` The offline line reads `You are offline. The pages you have already opened are still here.` `src: Core features`
- [ ] `C-CF-127` `capability` A publish rebuilds exactly the routes the change touches. `src: Core features`
- [ ] `C-CF-128` `capability` A first publish rebuilds that project along with the index. `src: Core features`
- [ ] `C-CF-129` `capability` A change to the home reel order rebuilds the home page. `src: Core features`
- [ ] `C-CF-130` `capability` A change to the global record rebuilds every route. `src: Core features`
- [ ] `C-CF-131` `capability` The publish gate requires every reel section carrying audio to carry a subtitle. `src: Core features`
- [ ] `C-CF-132` `capability` The publish gate requires every media element to declare both intrinsic dimensions. `src: Core features`
- [ ] `C-CF-133` `capability` The publish gate requires every outbound target to be an absolute address with a secure scheme. `src: Core features`
- [ ] `C-CF-134` `capability` The publish gate requires every media to carry an alternative text or an explicit decorative mark. `src: Core features`
- [ ] `C-CF-135` `capability` A preview token is a capability bound to one record identifier along with one content state. `src: Core features`
- [ ] `C-CF-136` `constraint` A preview token is read only. `src: Core features`
- [ ] `C-CF-137` `capability` The privacy notice names every processor, stating the single data class with the retention. `src: Core features`
- [ ] `C-CF-138` `capability` The privacy notice is versioned, so a consent record references the version shown. `src: Core features`
- [ ] `C-CF-139` `capability` Every form field validates inline, naming the field that failed, writing nothing on a refusal. `src: Core features`
- [ ] `C-CF-140` `constraint` No third party script, pixel, frame, beacon loads before an explicit affirmative consent. `src: Core features`
- [ ] `C-CF-141` `ui` The consent interface offers accept along with reject at equal prominence. `src: Core features`
- [ ] `C-CF-142` `capability` Withdrawing consent deletes the client state that category created without a reload. `src: Core features`
- [ ] `C-CF-143` `capability` A global privacy control signal is honoured as a rejection without a prompt. `src: Core features`
- [ ] `C-CF-144` `constraint` Subtitles render by default across the backstage overlay. `src: Core features`
- [ ] `C-CF-145` `constraint` There is no bare error page in the product. `src: Core features`
- [ ] `C-CF-146` `capability` A missing media renders a reserved box at the right shape with a generated placeholder. `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `literal` The home route is `/`. `src: User flow`
- [ ] `C-UF-02` `literal` One case study route is `/projects/lambert-vitrine`. `src: User flow`
- [ ] `C-UF-03` `literal` The case study seeded without a live address is `/projects/verrine-end-of-year-23`. `src: User flow`
- [ ] `C-UF-04` `literal` The backstage overlay route is `/projects/lambert-vitrine/backstage`. `src: User flow`
- [ ] `C-UF-05` `literal` The project index route is `/projects`. `src: User flow`
- [ ] `C-UF-06` `contract` A retired path resolves in one hop rather than through a chain. `src: User flow`
- [ ] `C-UF-07` `literal` The console sign in route is `/console/sign-in`. `src: User flow`
- [ ] `C-UF-08` `literal` The record editor route is `/console/projects/marivella`. `src: User flow`
- [ ] `C-UF-09` `contract` An anonymous caller reaching a console route is sent to the console sign in route. `src: User flow`
- [ ] `C-UF-10` `contract` A caller sent to the console sign in route is returned to the route asked for once signed in. `src: User flow`
- [ ] `C-UF-11` `literal` The home reel order editor route is `/console/reel`, open to an editor. `src: User flow`
- [ ] `C-UF-12` `contract` A producer reaching the reel order route is refused rather than shown a read only copy. `src: User flow`
- [ ] `C-UF-13` `data` The index carries seventeen entries once the record awaiting sign off is published. `src: User flow`
- [ ] `C-UF-14` `literal` The publish log route is `/console/publish-log`. `src: User flow`
- [ ] `C-UF-15` `literal` The draft reader route is `/preview`. `src: User flow`
- [ ] `C-UF-16` `contract` A preview address carrying no token answers not found. `src: User flow`
- [ ] `C-UF-17` `literal` The privacy notice route is `/privacy`. `src: User flow`
- [ ] `C-UF-18` `literal` The studio story route is `/about-us`. `src: User flow`
- [ ] `C-UF-19` `literal` One studio chapter route is `/about-us/where-we-started`. `src: User flow`
- [ ] `C-UF-20` `literal` The media library route is `/console/media`. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `capability` A hard flick pulls the camera back, blowing the titles up, dropping every interface control. `src: UI/UX notes`
- [ ] `C-UX-02` `capability` Every open overlay traps focus, restoring focus to the opening control on close. `src: UI/UX notes`
- [ ] `C-UX-03` `capability` Every overlay closes on the escape key, carrying a role along with an accessible name. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Pointing at an index row brightens nothing, every other row receding instead. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` A hairline grows in under the name being pointed at. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The recovery from the dimming runs about twice as slowly as the dimming. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` The console is dense, with stable positions, carrying no atmosphere. `src: UI/UX notes`
- [ ] `C-UX-08` `constraint` The public register along with the console register are built separately rather than unified. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The signature interaction on the index inverts the usual highlight. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A pointer sweeping the list leaves a soft wake rather than a strobe. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` The interface is achromatic, a near-black neutral with a warm near-white neutral carrying the product. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The world behind the words never goes away. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` The outgoing page leaves instantly, the incoming page arriving slowly. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Movement arrives slowly, leaving quickly. `src: UI/UX notes`
- [ ] `C-UX-15` `literal` The transitional serif is `EB Garamond`, carrying every title with every index entry. `src: UI/UX notes`
- [ ] `C-UX-16` `literal` The neo grotesque is `Archivo`, carrying every piece of interface text. `src: UI/UX notes`
- [ ] `C-UX-17` `literal` `Archivo Light` carries the mailing list input alone. `src: UI/UX notes`
- [ ] `C-UX-18` `constraint` Display type is proportional to the window, interface text never scaling. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` One radius exists across the product, fully round. `src: UI/UX notes`
- [ ] `C-UX-20` `constraint` Every rectangular thing, every media block, every input, every panel is square. `src: UI/UX notes`
- [ ] `C-UX-21` `literal` The skip link reads `Skip to content`. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` The skip link is first in tab order on every route. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Every control is reachable by keyboard in document order with a visible focus indicator. `src: UI/UX notes`
- [ ] `C-UX-24` `constraint` The focus indicator is not the pointer dot. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` A case study headline is drawn inside the scene from glyph geometry. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` The document carries the headline string as real text available to assistive technology. `src: UI/UX notes`
- [ ] `C-UX-27` `constraint` The scene rendering of a headline is treated as decoration. `src: UI/UX notes`
- [ ] `C-UX-28` `constraint` Nothing overflows sideways at a phone width. `src: UI/UX notes`
- [ ] `C-UX-29` `constraint` Five layout stops exist, everything else being generated by the scaling law. `src: UI/UX notes`
- [ ] `C-UX-30` `ui` The console inverts the public register deliberately. `src: UI/UX notes`
- [ ] `C-UX-31` `constraint` A person doing repeated editorial work wants density. `src: UI/UX notes`
- [ ] `C-UX-32` `constraint` The console carries neither the background scene nor the public motion. `src: UI/UX notes`
- [ ] `C-UX-33` `constraint` There is no thumbnail wall, no filter chip, no card with a hover lift. `src: UI/UX notes`
- [ ] `C-UX-34` `constraint` There is no cookie banner pushing the page down. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `constraint` The tuning panel sits behind a dynamic import unreachable in a production build. `src: Front-end specification`
- [ ] `C-FE-02` `literal` The opening statement is the four word nodes `Innovative`, `digital`, `experiences`, `studio`. `src: Front-end specification`
- [ ] `C-FE-03` `literal` The loader hint reads `Scroll down`. `src: Front-end specification`
- [ ] `C-FE-04` `ui` The loader rail is scaled from the resource manager completed byte fraction. `src: Front-end specification`
- [ ] `C-FE-05` `constraint` The loader never rests on a fraction, offering the lighter scene on a stall. `src: Front-end specification`
- [ ] `C-FE-06` `literal` The stalled loader carries the pinned stall sentence. `src: Front-end specification`
- [ ] `C-FE-07` `literal` The stalled loader control reads `Continue with the lighter version`. `src: Front-end specification`
- [ ] `C-FE-08` `capability` The reel entry title is drawn inside the scene at the display medium size. `src: Front-end specification`
- [ ] `C-FE-09` `capability` The reel entry description is carried by the document as selectable text. `src: Front-end specification`
- [ ] `C-FE-10` `literal` The case study outbound control reads `Launch website`. `src: Front-end specification`
- [ ] `C-FE-11` `literal` The case study reel control reads `See backstage`. `src: Front-end specification`
- [ ] `C-FE-12` `literal` The footer projects action reads `See all projects` or `See next project`. `src: Front-end specification`
- [ ] `C-FE-13` `ui` The footer list action expands the footer into a full panel, hiding the page content behind. `src: Front-end specification`
- [ ] `C-FE-14` `literal` The consent line reads `By submitting you agree to receive occasional studio news. Unsubscribe any time.` `src: Front-end specification`
- [ ] `C-FE-15` `ui` The panel submit sits at the hidden opacity with a default cursor until submission becomes available. `src: Front-end specification`
- [ ] `C-FE-16` `ui` The accepted message names the address submitted. `src: Front-end specification`
- [ ] `C-FE-17` `literal` The rate limited message reads `Too many attempts. Try again in a minute.` `src: Front-end specification`
- [ ] `C-FE-18` `literal` The temporary failure message reads `Something went wrong at our end. Try again.` `src: Front-end specification`
- [ ] `C-FE-19` `ui` The temporary failure leaves the typed address in the field. `src: Front-end specification`
- [ ] `C-FE-20` `ui` An index row takes the full width with the items aligned to the end. `src: Front-end specification`
- [ ] `C-FE-21` `ui` The project type sits in a narrow span right aligned at the secondary opacity. `src: Front-end specification`
- [ ] `C-FE-22` `ui` The project title sits to the right of the type column in the serif face. `src: Front-end specification`
- [ ] `C-FE-23` `ui` The not found route carries scene material of its own rather than a static page. `src: Front-end specification`
- [ ] `C-FE-24` `ui` Every route reports a document height equal to the window height at every width. `src: Front-end specification`
- [ ] `C-FE-25` `ui` The scrolling element is an inner container with an overflow of the container's own. `src: Front-end specification`
- [ ] `C-FE-26` `constraint` Anything assuming the document scrolls is broken by default. `src: Front-end specification`
- [ ] `C-FE-27` `ui` An index row's type column dims when a sibling is under the pointer. `src: Front-end specification`
- [ ] `C-FE-28` `ui` Five neutral roles exist with no hue among them. `src: Front-end specification`
- [ ] `C-FE-29` `constraint` A vivid amber with a soft green belong to a development panel stylesheet unreachable in a shipped build. `src: Front-end specification`
- [ ] `C-FE-30` `ui` The scene canvas fills the window at the ground level on every route. `src: Front-end specification`
- [ ] `C-FE-31` `ui` Six elements mount once outside the routed content, surviving every navigation. `src: Front-end specification`
- [ ] `C-FE-32` `capability` Moving between routes shows a view, hiding another, inside one running scene. `src: Front-end specification`
- [ ] `C-FE-33` `ui` The continuity across a transition is carried by the scene alone. `src: Front-end specification`
- [ ] `C-FE-34` `constraint` Sound is off on arrival, requiring an explicit action to start. `src: Front-end specification`
- [ ] `C-FE-35` `literal` The sound control first arrival hint reads `Click to enable sound`. `src: Front-end specification`
- [ ] `C-FE-36` `constraint` A visitor who never enables sound has no audio object created. `src: Front-end specification`
- [ ] `C-FE-37` `ui` The sound control sits at the bottom right above every overlay. `src: Front-end specification`
- [ ] `C-FE-38` `ui` Subtitle cues are split into word nodes one cue per frame. `src: Front-end specification`
- [ ] `C-FE-39` `ui` Subtitle words reveal with a fade offset, a fade in delay, a fade out delay. `src: Front-end specification`
- [ ] `C-FE-40` `ui` One hairline thickness carries every underline, the loader rail, the video scrubber gutter. `src: Front-end specification`
- [ ] `C-FE-41` `ui` The video scrubber runs across the vertical centre of the window. `src: Front-end specification`
- [ ] `C-FE-42` `ui` The video scrubber reads as a horizon line rather than as a progress bar. `src: Front-end specification`
- [ ] `C-FE-43` `ui` The video ground fills the window in the pure near-black with a mask over the ground. `src: Front-end specification`
- [ ] `C-FE-44` `ui` The loader figure prints the completed byte fraction of the resource manager. `src: Front-end specification`
- [ ] `C-FE-45` `ui` The loader carries a wordmark, a progress figure in the serif, a progress rail, a baseline of four words, a hint. `src: Front-end specification`
- [ ] `C-FE-46` `ui` The loader locks scrolling until the scene reports ready. `src: Front-end specification`
- [ ] `C-FE-47` `capability` The virtual scroller binds the space bar, the page keys, the arrow keys, the home key, the end key by hand. `src: Front-end specification`
- [ ] `C-FE-48` `constraint` The scroller replaced the behaviour providing keyboard travel, so each key is put back. `src: Front-end specification`
- [ ] `C-FE-49` `capability` Browser scroll restoration on a back navigation is disabled explicitly, the offset being restored by hand. `src: Front-end specification`
- [ ] `C-FE-50` `ui` The not found route carries a headline, an action, the navigation control, the sound control, the footer. `src: Front-end specification`
- [ ] `C-FE-51` `ui` Below the tablet stop the index type column is hidden, the title taking the whole row. `src: Front-end specification`
- [ ] `C-FE-52` `ui` The footer reveals on crossing half the footer's own height into view. `src: Front-end specification`
- [ ] `C-FE-53` `ui` The footer baseline block rises, fading over the slowest single element move in the product. `src: Front-end specification`
- [ ] `C-FE-54` `ui` The footer hide reverses the reveal in a fraction of the time. `src: Front-end specification`
- [ ] `C-FE-55` `literal` The footer baseline reads `Find out more across all our productions`. `src: Front-end specification`
- [ ] `C-FE-56` `ui` At rest the reel media planes drift vertically against a mask moving at a fraction of their speed. `src: Front-end specification`
- [ ] `C-FE-57` `ui` In the fast state the vertical drift falls away as a horizontal factor rises to full. `src: Front-end specification`
- [ ] `C-FE-58` `ui` The relief moves at the same rate in both scroller states. `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` The preview route response is never stored at the edge. `src: Technical requirements`
- [ ] `C-TR-02` `constraint` The captioning rule is enforced as a storage constraint, as a publish gate rule, as a console field requirement. `src: Technical requirements`
- [ ] `C-TR-03` `capability` An editor is warned before withdrawing a project that sits on the reel. `src: Technical requirements`
- [ ] `C-TR-04` `contract` A save carrying a stale version is rejected as a conflict rather than applied. `src: Technical requirements`
- [ ] `C-TR-05` `capability` The console shows who else holds the record open. `src: Technical requirements`
- [ ] `C-TR-06` `constraint` Every credential is server side, rotatable without a deploy. `src: Technical requirements`
- [ ] `C-TR-07` `ui` The console shows, before any withdrawal, exactly what will change. `src: Technical requirements`
- [ ] `C-TR-08` `ui` The console shows the count of ready variants against expected on a media. `src: Technical requirements`
- [ ] `C-TR-09` `ui` The consent interface is an overlay rather than a banner displacing the page. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The disciplines table holds ten rows. `src: Data model`
- [ ] `C-DM-02` `data` The project disciplines join carries a position per term. `src: Data model`
- [ ] `C-DM-03` `data` The index order is derived on read rather than stored as a rank. `src: Data model`
- [ ] `C-DM-04` `data` The preview tokens table carries a token hash, a record type, a record slug, an issuing account, an issue instant, an expiry instant, a revocation instant. `src: Data model`
- [ ] `C-DM-05` `data` One preview token row is seeded against `marivella`. `src: Data model`
- [ ] `C-DM-06` `constraint` A reel section row carrying an audio media without a subtitle media cannot exist. `src: Data model`
- [ ] `C-DM-07` `data` A reel section duration is a whole count of milliseconds rather than a float of seconds. `src: Data model`
- [ ] `C-DM-08` `data` The publish log outcome is one of succeeded, failed, partially applied. `src: Data model`
- [ ] `C-DM-09` `data` The home reel entries table holds three rows. `src: Data model`
- [ ] `C-DM-10` `constraint` The media content hash is unique, so uploading one file twice produces one record. `src: Data model`
- [ ] `C-DM-11` `data` The media renditions triple of media, variant, format appears at most once. `src: Data model`
- [ ] `C-DM-12` `constraint` The normalised address is unique, so a resubmission changes nothing. `src: Data model`
- [ ] `C-DM-13` `data` A subscriber row carries the normalised address, the display form, the state, the source route, the consent version, the consent instant, the confirmation instant. `src: Data model`
- [ ] `C-DM-14` `constraint` The subscribers table is the only table holding personal data. `src: Data model`
- [ ] `C-DM-15` `literal` The subscriber states are `pending`, `confirmed`, `unsubscribed`, `bounced`. `src: Data model`
- [ ] `C-DM-16` `data` A project row carries a version. `src: Data model`
- [ ] `C-DM-17` `constraint` The retired path is the primary key, so a collision is unstorable. `src: Data model`
- [ ] `C-DM-18` `data` The projects table holds eighteen rows. `src: Data model`
- [ ] `C-DM-19` `data` The chapters table holds six rows. `src: Data model`
- [ ] `C-DM-20` `data` The accounts table holds three rows. `src: Data model`
- [ ] `C-DM-21` `data` The media table holds four rows, one still being derived. `src: Data model`
- [ ] `C-DM-22` `contract` Seeding is idempotent, so restarting the application duplicates no row. `src: Data model`
- [ ] `C-DM-23` `literal` The block kinds are `hero`, `text`, `media`, `split_media`, `image_push`. `src: Data model`
- [ ] `C-DM-24` `constraint` A block payload is validated against the schema for the kind on write. `src: Data model`
- [ ] `C-DM-25` `constraint` A block is polymorphic over a project owner along with a chapter owner. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No search provider exists, no filter control sitting on the index. `src: Constraints`
- [ ] `C-CN-02` `constraint` No payment provider exists, nothing being for sale. `src: Constraints`
- [ ] `C-CN-03` `constraint` No client portal, no per client view, no invoice, no price exists anywhere. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The health endpoint answers ready once the application has started. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The application is reachable at the public address read from the environment. `src: Deployment contract`
- [ ] `C-DC-03` `constraint` Neither the public address nor the public port is hardcoded. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The application starts from the environment image with no manual step. `src: Deployment contract`
- [ ] `C-DC-05` `contract` A production build is served rather than a development server. `src: Deployment contract`
- [ ] `C-DC-06` `contract` Login credentials are written to the credential file at the application root. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `producer@example.com` | User roles | `C-RL-19` |
| `producer2@example.com` | User roles | `C-RL-19` |
| `editor@example.com` | User roles | `C-RL-19` |
| `deku-demo-pw-2026` | User roles | `C-RL-20` |
| `Design` | Core features | `C-CF-01` |
| `Experience` | Core features | `C-CF-01` |
| `3D` | Core features | `C-CF-01` |
| `Tech` | Core features | `C-CF-01` |
| `Strategy` | Core features | `C-CF-01` |
| `Branding` | Core features | `C-CF-01` |
| `E-shop` | Core features | `C-CF-01` |
| `Web3` | Core features | `C-CF-01` |
| `NFT` | Core features | `C-CF-01` |
| `Film` | Core features | `C-CF-01` |
| `Arven` | Core features | `C-CF-07` |
| `Aurel Vance Experience` | Core features | `C-CF-07` |
| `Chastenay Belfort` | Core features | `C-CF-07` |
| `Faiseurs d'Ourcq` | Core features | `C-CF-07` |
| `Grale` | Core features | `C-CF-07` |
| `Halom` | Core features | `C-CF-07` |
| `Verrine Watchmaking Salon 24` | Core features | `C-CF-08` |
| `marivella` | Core features | `C-CF-12` |
| `oryx7` | Core features | `C-CF-12` |
| `prv_` | Core features | `C-CF-15` |
| `prv_6d1f4a08c39b27e5d0a4f81c6b3e97d2` | Core features | `C-CF-16` |
| `draft` | Core features | `C-CF-32` |
| `in_review` | Core features | `C-CF-32` |
| `published` | Core features | `C-CF-32` |
| `unpublished` | Core features | `C-CF-32` |
| `lambert-vitrine` | Core features | `C-CF-45` |
| `grale` | Core features | `C-CF-45` |
| `verrine-end-of-year-23` | Core features | `C-CF-45` |
| `media/<content-hash>/master.<ext>` | Core features | `C-CF-55` |
| `media/<content-hash>/<variant>.<ext>` | Core features | `C-CF-57` |
| `media/9f2ad0c4/medium.avif` | Core features | `C-CF-58` |
| `placeholder` | Core features | `C-CF-59` |
| `xs` | Core features | `C-CF-59` |
| `sm` | Core features | `C-CF-59` |
| `md` | Core features | `C-CF-59` |
| `lg` | Core features | `C-CF-59` |
| `xl` | Core features | `C-CF-59` |
| `uploaded` | Core features | `C-CF-64` |
| `deriving` | Core features | `C-CF-64` |
| `ready` | Core features | `C-CF-64` |
| `failed` | Core features | `C-CF-64` |
| `Invalid email format` | Core features | `C-CF-73` |
| `Incorrect email or password` | Core features | `C-CF-91` |
| `/sitemap.xml` | Core features | `C-CF-96` |
| `/robots.txt` | Core features | `C-CF-97` |
| `/cases/lambert-vitrine` | Core features | `C-CF-104` |
| `/cases/vitrine` | Core features | `C-CF-104` |
| `/cases/grale` | Core features | `C-CF-104` |
| `where-we-started` | Core features | `C-CF-109` |
| `how-we-work` | Core features | `C-CF-109` |
| `what-we-refuse` | Core features | `C-CF-109` |
| `the-people` | Core features | `C-CF-109` |
| `the-craft` | Core features | `C-CF-109` |
| `the-studio` | Core features | `C-CF-109` |
| `Nothing published yet. Write to the studio.` | Core features | `C-CF-120` |
| `That page has moved on.` | Core features | `C-CF-121` |
| `See all projects` | Core features | `C-CF-122` |
| `Something is temporarily out of reach.` | Core features | `C-CF-124` |
| `Try again` | Core features | `C-CF-125` |
| `You are offline. The pages you have already opened are still here.` | Core features | `C-CF-126` |
| `/` | User flow | `C-UF-01` |
| `/projects/lambert-vitrine` | User flow | `C-UF-02` |
| `/projects/verrine-end-of-year-23` | User flow | `C-UF-03` |
| `/projects/lambert-vitrine/backstage` | User flow | `C-UF-04` |
| `/projects` | User flow | `C-UF-05` |
| `/console/sign-in` | User flow | `C-UF-07` |
| `/console/projects/marivella` | User flow | `C-UF-08` |
| `/console/reel` | User flow | `C-UF-11` |
| `/console/publish-log` | User flow | `C-UF-14` |
| `/preview` | User flow | `C-UF-15` |
| `/privacy` | User flow | `C-UF-17` |
| `/about-us` | User flow | `C-UF-18` |
| `/about-us/where-we-started` | User flow | `C-UF-19` |
| `/console/media` | User flow | `C-UF-20` |
| `EB Garamond` | UI/UX notes | `C-UX-15` |
| `Archivo` | UI/UX notes | `C-UX-16` |
| `Archivo Light` | UI/UX notes | `C-UX-17` |
| `Skip to content` | UI/UX notes | `C-UX-21` |
| `Innovative` | Front-end specification | `C-FE-02` |
| `digital` | Front-end specification | `C-FE-02` |
| `experiences` | Front-end specification | `C-FE-02` |
| `studio` | Front-end specification | `C-FE-02` |
| `Scroll down` | Front-end specification | `C-FE-03` |
| `Continue with the lighter version` | Front-end specification | `C-FE-07` |
| `Launch website` | Front-end specification | `C-FE-10` |
| `See backstage` | Front-end specification | `C-FE-11` |
| `See next project` | Front-end specification | `C-FE-12` |
| `By submitting you agree to receive occasional studio news. Unsubscribe any time.` | Front-end specification | `C-FE-14` |
| `Too many attempts. Try again in a minute.` | Front-end specification | `C-FE-17` |
| `Something went wrong at our end. Try again.` | Front-end specification | `C-FE-18` |
| `Click to enable sound` | Front-end specification | `C-FE-35` |
| `Find out more across all our productions` | Front-end specification | `C-FE-55` |
| `pending` | Data model | `C-DM-15` |
| `confirmed` | Data model | `C-DM-15` |
| `unsubscribed` | Data model | `C-DM-15` |
| `bounced` | Data model | `C-DM-15` |
| `hero` | Data model | `C-DM-23` |
| `text` | Data model | `C-DM-23` |
| `media` | Data model | `C-DM-23` |
| `split_media` | Data model | `C-DM-23` |
| `image_push` | Data model | `C-DM-23` |
| `This is taking longer than it should.` | Front-end specification | `C-FE-06` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact value of every neutral colour role | `C-UX-11` |
| the exact size of every type scale token | `C-UX-18` |
| the exact duration of every named curve | `C-UX-14` |
| the exact width of each of the five layout stops | `C-UX-29` |
| the exact level of each of the nine opacity steps | `C-FE-15` |
| the address of the live site each case study links to | `C-CF-116` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 3 | 3 |
| User roles | 7 | 20 |
| Core features | 52 | 146 |
| User flow | 9 | 20 |
| UI and UX notes | 12 | 34 |
| Technical requirements | 6 | 9 |
| Data model | 9 | 25 |
| Front-end specification | 34 | 58 |
| Constraints | 2 | 3 |
| Deployment contract | 5 | 6 |

