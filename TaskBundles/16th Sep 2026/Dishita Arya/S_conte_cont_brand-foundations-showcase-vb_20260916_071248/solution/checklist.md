# Checklist: Latticework Foundations

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract
Sections absent: buildplan
Items: 619
Unpinned values flagged: 1

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public brand-foundations site as a sequence of full-screen editorial chapters. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app presents each chapter as one essay wrapped around a single foundational idea. `src: Overview para 1`
- [ ] `C-OV-03` `role` A designer reads the tone groups, the logo lockups, the clear space, the typography from the chapters. `src: Overview para 1`
- [ ] `C-OV-04` `role` A partner reads a quotable statement of the brand from the chapters. `src: Overview para 1`
- [ ] `C-OV-05` `role` A prospective customer reaches the free trial at the end of a chapter rather than at the top of a page. `src: Overview para 1`
- [ ] `C-OV-06` `constraint` The app offers a visitor exactly one state-changing action, starting a free website trial from a chapter's closing poster. `src: Overview para 2`
- [ ] `C-OV-07` `capability` The app lets an author write a chapter, order the chapter's sections, generate the chapter's imagery, publish the chapter. `src: Overview para 2`
- [ ] `C-OV-08` `constraint` The app treats an unpublished chapter as not a public chapter. `src: Overview para 2`
- [ ] `C-OV-09` `ui` The product reads near-monochrome almost all of the time. `src: Overview para 3`
- [ ] `C-OV-10` `ui` The product introduces colour only where the content is about colour. `src: Overview para 3`
- [ ] `C-OV-11` `constraint` The app omits comments, likes, sharing, a social graph, chat, a newsletter. `src: Overview para 4`
- [ ] `C-OV-12` `constraint` The app omits search across chapters. `src: Overview para 4`
- [ ] `C-OV-13` `constraint` The app omits payment of every kind, so the trial takes no card. `src: Overview para 4`
- [ ] `C-OV-14` `constraint` The app omits a second brand, multi-tenancy. `src: Overview para 4`
- [ ] `C-OV-15` `constraint` The app omits third-party analytics, a consent vendor, a content host, an asset host. `src: Overview para 4`
- [ ] `C-OV-16` `constraint` The app ships no binary asset of any kind with the build. `src: Overview para 4`
- [ ] `C-OV-17` `capability` The app drives the page ground, the text colour, the media ground, the logo fill directly from scroll position. `src: Overview para 5`
- [ ] `C-OV-18` `constraint` The app interpolates the page ground continuously between stops rather than switching at a section boundary. `src: Overview para 5`
- [ ] `C-OV-19` `constraint` The app reverses the colour interpolation with scroll direction. `src: Overview para 5`
- [ ] `C-OV-20` `constraint` The app keeps text readable at every point between two stops rather than only at the stops themselves. `src: Overview para 5`
- [ ] `C-OV-21` `capability` The app treats every statement of the brief as normative, each one settleable by looking at the running site. `src: Overview para 6`
- [ ] `C-OV-22` `capability` The app supplies a procedural substitution for the model geometry, the loader flourish, the audio cues, the hover craft. `src: Overview para 7`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads the index carousel. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor reads every published chapter. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor reads the full-screen menu, the model surface, the not-found body. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A signed-out visitor submits a free trial. `src: User roles table row 1`
- [ ] `C-RL-05` `constraint` The app refuses a signed-out request for an unpublished chapter at every address. `src: User roles table row 1`
- [ ] `C-RL-06` `constraint` The app refuses a signed-out request for an unpublished chapter's image. `src: User roles table row 1`
- [ ] `C-RL-07` `constraint` The app refuses a signed-out request for the author surface, the endpoints surface. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A reader reads everything a signed-out visitor reads, signed in. `src: User roles table row 2`
- [ ] `C-RL-09` `constraint` The app refuses a reader request for an unpublished chapter at every address. `src: User roles table row 2`
- [ ] `C-RL-10` `constraint` The app refuses a reader request for an unpublished chapter's image. `src: User roles table row 2`
- [ ] `C-RL-11` `constraint` The app refuses a reader request to publish anything. `src: User roles table row 2`
- [ ] `C-RL-12` `role` An author writes, reorders, generates imagery for, publishes chapters the author owns. `src: User roles table row 3`
- [ ] `C-RL-13` `role` An author reads the author's own drafts, the drafts' imagery. `src: User roles table row 3`
- [ ] `C-RL-14` `role` An author reads the trial list. `src: User roles table row 3`
- [ ] `C-RL-15` `role` An author reaches the endpoints surface. `src: User roles table row 3`
- [ ] `C-RL-16` `constraint` The app refuses one author's request to read a chapter owned by another author. `src: User roles table row 3`
- [ ] `C-RL-17` `constraint` The app refuses one author's request to edit a chapter owned by another author. `src: User roles table row 3`
- [ ] `C-RL-18` `constraint` The app refuses one author's request to publish a chapter owned by another author. `src: User roles table row 3`
- [ ] `C-RL-19` `constraint` The app enforces authorization server side on every mutating endpoint. `src: User roles, enforcement paragraph`
- [ ] `C-RL-20` `constraint` The app rejects a direct API call from a reader session to an author-only endpoint, leaving the protected state unchanged. `src: User roles, enforcement paragraph`
- [ ] `C-RL-21` `constraint` The app reads the role from the signed-in account's own record, never from a request body, a query parameter, a caller-controlled header. `src: User roles, enforcement paragraph`
- [ ] `C-RL-22` `capability` The app opens signup to anyone. `src: User roles, signup paragraph`
- [ ] `C-RL-23` `constraint` The app gives an account created through signup the reader role. `src: User roles, signup paragraph`
- [ ] `C-RL-24` `constraint` The app refuses a signup request that asks for the author role. `src: User roles, signup paragraph`
- [ ] `C-RL-25` `literal` The app seeds the account `author@example.com` as an author named Wren Calloway. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-26` `literal` The app gives `author@example.com` ownership of the colour, logo, typography, photography chapters. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-27` `literal` The app seeds the account `author2@example.com` as an author named Osian Petrie. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-28` `literal` The app gives `author2@example.com` ownership of the motion chapter. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-29` `literal` The app seeds the account `reader@example.com` as a reader named Marit Sandoval. `src: User roles, seeded accounts paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app exchanges an email address plus a password for a bearer token. `src: Core features, Auth para`
- [ ] `C-CF-02` `constraint` The app stores a password under a modern memory-hard password hash, never in a recoverable form. `src: Core features, Auth para`
- [ ] `C-CF-03` `contract` The client sends the bearer token as a credential on every API call. `src: Core features, Auth para`
- [ ] `C-CF-04` `constraint` The app expires a token, returning the caller to the sign-in route with the pending work unwritten. `src: Core features, Auth para`
- [ ] `C-CF-05` `constraint` The app refuses a sign-in carrying a wrong password. `src: Core features, Auth rule 1`
- [ ] `C-CF-06` `constraint` The app keeps a sign-in refusal silent about which of the two values was wrong. `src: Core features, Auth rule 1`
- [ ] `C-CF-07` `capability` The app invalidates a token on sign-out. `src: Core features, Auth rule 2`
- [ ] `C-CF-08` `constraint` The app denies a request replaying an invalidated token. `src: Core features, Auth rule 2`
- [ ] `C-CF-09` `constraint` The app refuses a signup request asking for the author role as invalid, creating nothing. `src: Core features, Auth rule 3`
- [ ] `C-CF-10` `data` The app holds five chapters in a fixed running order. `src: Core features, chapter set rule 1`
- [ ] `C-CF-11` `literal` The app orders the chapters `01` Color, `02` Logo, `03` Typography, `04` Photography, `05` Motion. `src: Core features, chapter set rule 1`
- [ ] `C-CF-12` `data` The app gives each chapter a slug, a running index label, a parenthetical eyebrow, a display title, a lead, an ordered set of sections. `src: Core features, chapter set rule 1`
- [ ] `C-CF-13` `literal` The app publishes the seeded chapters `color`, `logo`. `src: Core features, chapter set rule 2`
- [ ] `C-CF-14` `literal` The app leaves the seeded chapters `typography`, `photography`, `motion` unpublished. `src: Core features, chapter set rule 2`
- [ ] `C-CF-15` `ui` The index advertises all five chapters by name. `src: Core features, chapter set rule 3`
- [ ] `C-CF-16` `constraint` The index resolves only the published chapters. `src: Core features, chapter set rule 3`
- [ ] `C-CF-17` `ui` Choosing an unpublished card does not navigate, so the card states that the chapter is not yet published. `src: Core features, chapter set rule 3`
- [ ] `C-CF-18` `constraint` The app refuses a signed-out reader an unpublished chapter at the chapter's own address. `src: Core features, chapter set rule 4`
- [ ] `C-CF-19` `constraint` The app refuses a signed-in reader an unpublished chapter through the chapter endpoint. `src: Core features, chapter set rule 4`
- [ ] `C-CF-20` `constraint` The app refuses a signed-in reader an unpublished chapter through the sections endpoint. `src: Core features, chapter set rule 4`
- [ ] `C-CF-21` `constraint` The app omits an unpublished chapter from every public list. `src: Core features, chapter set rule 4`
- [ ] `C-CF-22` `constraint` The app omits an unpublished chapter from the sitemap. `src: Core features, chapter set rule 4`
- [ ] `C-CF-23` `capability` The app serves an unpublished chapter to the chapter's own author. `src: Core features, chapter set rule 5`
- [ ] `C-CF-24` `constraint` The app denies one author an unpublished chapter owned by a second author, exactly as a signed-out visitor is denied. `src: Core features, chapter set rule 5`
- [ ] `C-CF-25` `capability` Publishing makes a chapter readable at the chapter's slug. `src: Core features, chapter set rule 6`
- [ ] `C-CF-26` `data` Publishing records the moment of publication. `src: Core features, chapter set rule 6`
- [ ] `C-CF-27` `capability` Publishing adds a chapter to the sitemap. `src: Core features, chapter set rule 6`
- [ ] `C-CF-28` `capability` Unpublishing reverses the readability, the recorded moment, the sitemap entry. `src: Core features, chapter set rule 6`
- [ ] `C-CF-29` `constraint` The app refuses a request to publish a chapter carrying no sections, changing nothing. `src: Core features, chapter set rule 7`
- [ ] `C-CF-30` `constraint` The index does not scroll the document. `src: Core features, index carousel rule 1`
- [ ] `C-CF-31` `capability` The carousel advances in place on the index. `src: Core features, index carousel rule 1`
- [ ] `C-CF-32` `ui` Each card carries the chapter's index label, the chapter's parenthetical eyebrow, a framed image. `src: Core features, index carousel rule 2`
- [ ] `C-CF-33` `ui` A card's frame window morphs between shapes as the card moves. `src: Core features, index carousel rule 2`
- [ ] `C-CF-34` `literal` The card eyebrows read `( Color )`, `( Logo )`, `( Typography )`, `( Photography )`, `( Motion )`. `src: Core features, index carousel rule 2`
- [ ] `C-CF-35` `ui` The carousel advances on the previous arrow control, on the next arrow control. `src: Core features, index carousel rule 3`
- [ ] `C-CF-36` `ui` The carousel advances on drag. `src: Core features, index carousel rule 3`
- [ ] `C-CF-37` `ui` The carousel advances on the left arrow key, on the right arrow key. `src: Core features, index carousel rule 3`
- [ ] `C-CF-38` `constraint` All three carousel controls reach the same card. `src: Core features, index carousel rule 3`
- [ ] `C-CF-39` `ui` On first entry the index shows the two display words, the lead line, before the cards take over. `src: Core features, index carousel rule 4`
- [ ] `C-CF-40` `ui` A label on the card in view invites entry with the pinned invitation string. `src: Core features, index carousel rule 5`
- [ ] `C-CF-41` `capability` The app drives the page ground, the ink, a section-local ground, a section-local ink, the media ground from scroll position on an editorial chapter. `src: Core features, colour system rule 1`
- [ ] `C-CF-42` `constraint` The app resolves the five animated properties once at the document root, so every component reads the same values. `src: Core features, colour system rule 1`
- [ ] `C-CF-43` `constraint` The media ground is derived from the page ground rather than declared independently. `src: Core features, colour system rule 2`
- [ ] `C-CF-44` `ui` The media ground tracks the page ground two shades lighter, so imagery never sits on exactly the page ground. `src: Core features, colour system rule 2`
- [ ] `C-CF-45` `literal` The colour chapter moves the ground through `Core`, `Dark`, `Bright`, `Light` in that order. `src: Core features, colour system rule 3`
- [ ] `C-CF-46` `ui` The colour journey ends on white. `src: Core features, colour system rule 3`
- [ ] `C-CF-47` `data` The app stores the desktop, tablet, phone journeys as separate rows, so a phone does not inherit the desktop stops. `src: Core features, colour system rule 4`
- [ ] `C-CF-48` `constraint` At any scroll position the ground is the interpolation between the two bracketing stops rather than a stepped switch at a boundary. `src: Core features, colour system rule 5`
- [ ] `C-CF-49` `constraint` Scrolling backward runs the colour interpolation in reverse. `src: Core features, colour system rule 5`
- [ ] `C-CF-50` `ui` The ink flips between the light value, the dark value at the contrast crossover. `src: Core features, colour system rule 6`
- [ ] `C-CF-51` `constraint` The ink flip happens before either value falls below the value's contrast floor. `src: Core features, colour system rule 6`
- [ ] `C-CF-52` `ui` The logo chapter drives the logo fill, the counter-fill instead of the full journey. `src: Core features, colour system rule 7`
- [ ] `C-CF-53` `ui` The logo chapter keeps the ground near white, near black, so the mark carries the colour. `src: Core features, colour system rule 7`
- [ ] `C-CF-54` `ui` The shuffle control reshuffles the current tone group's swatch samples. `src: Core features, colour system rule 8`
- [ ] `C-CF-55` `ui` The shuffle control cross-fades the poster imagery with the reshuffled swatches. `src: Core features, colour system rule 8`
- [ ] `C-CF-56` `constraint` The shuffle control changes what is displayed, writing nothing. `src: Core features, colour system rule 8`
- [ ] `C-CF-57` `ui` Body copy splits into lines, each line rising into place as the line's opacity rises. `src: Core features, reveals rule 1`
- [ ] `C-CF-58` `constraint` The app scrubs the line reveal against scroll position rather than triggering the reveal on an intersection. `src: Core features, reveals rule 1`
- [ ] `C-CF-59` `constraint` Scrolling backward un-plays every reveal rather than replaying the reveal forward. `src: Core features, reveals rule 2`
- [ ] `C-CF-60` `ui` Lines within a block stagger, so a paragraph assembles line by line. `src: Core features, reveals rule 3`
- [ ] `C-CF-61` `constraint` The line splitter re-splits on resize. `src: Core features, reveals rule 3`
- [ ] `C-CF-62` `ui` The parenthetical eyebrow rides a shorter ladder slightly after the lines the eyebrow labels. `src: Core features, reveals rule 4`
- [ ] `C-CF-63` `ui` A control holds two copies of the arrow glyph. `src: Core features, reveals rule 5`
- [ ] `C-CF-64` `ui` Both arrow layers move by one glyph height on hover, on focus, on a carousel advance. `src: Core features, reveals rule 5`
- [ ] `C-CF-65` `constraint` The arrow rolls rather than fades. `src: Core features, reveals rule 5`
- [ ] `C-CF-66` `ui` A logo lockup is revealed by a clip wipe from the lockup's bottom edge, fully clipped to fully open. `src: Core features, reveals rule 6`
- [ ] `C-CF-67` `ui` The inner content of a logo lockup counter-translates, so the lockup holds position as the window opens. `src: Core features, reveals rule 6`
- [ ] `C-CF-68` `capability` Wheel input, touch input drive one eased virtual scroll position. `src: Core features, reveals rule 7`
- [ ] `C-CF-69` `constraint` Every scrubbed timeline reads the one eased scroll position. `src: Core features, reveals rule 7`
- [ ] `C-CF-70` `constraint` The scroll smoothing pauses for as long as the full-screen menu is open, resuming on close. `src: Core features, reveals rule 7`
- [ ] `C-CF-71` `constraint` Scroll progress comes from a marker element's position relative to the viewport rather than from an absolute document offset. `src: Core features, reveals rule 8`
- [ ] `C-CF-72` `constraint` A chapter of any height lands the chapter's reveals, the chapter's colour on the right sections. `src: Core features, reveals rule 8`
- [ ] `C-CF-73` `constraint` The route mask plays once on a route change rather than being scrubbed. `src: Core features, reveals rule 9`
- [ ] `C-CF-74` `constraint` The carousel enter, the carousel leave play once rather than being scrubbed. `src: Core features, reveals rule 9`
- [ ] `C-CF-75` `ui` The colour chapter opens on a white ground carrying the display headline. `src: Core features, colour chapter rule 1`
- [ ] `C-CF-76` `literal` The colour chapter's display headline reads `Color`. `src: Core features, colour chapter rule 1`
- [ ] `C-CF-77` `ui` The colour chapter sets the chapter lead large across the page. `src: Core features, colour chapter rule 1`
- [ ] `C-CF-78` `ui` Four tone-group sections follow the opening, each a full-bleed ground carrying a large word, a short definition. `src: Core features, colour chapter rule 2`
- [ ] `C-CF-79` `literal` The `Core` definition states that the tones support the brand imagery style, never blending into the background, never creating too harsh a contrast. `src: Core features, colour chapter rule 2`
- [ ] `C-CF-80` `literal` The `Dark` definition states that the tones stand as a background colour in place of true black. `src: Core features, colour chapter rule 2`
- [ ] `C-CF-81` `literal` The `Bright` definition states that the tones are saturated yet sophisticated, suited as an accent, suited across social media. `src: Core features, colour chapter rule 2`
- [ ] `C-CF-82` `literal` The `Light` definition states that the tones give an off-white background, pairing best with content-heavy designs. `src: Core features, colour chapter rule 2`
- [ ] `C-CF-83` `ui` Sticky poster stacks pin between the tone groups, revealing by clip, cross-fading the stack's imagery. `src: Core features, colour chapter rule 3`
- [ ] `C-CF-84` `ui` A poster caption names the tone, the application. `src: Core features, colour chapter rule 3`
- [ ] `C-CF-85` `ui` A paginated thumbnail rail steps through the examples, stating the rail's position. `src: Core features, colour chapter rule 4`
- [ ] `C-CF-86` `literal` The longer rail reads `01 / 07`. `src: Core features, colour chapter rule 4`
- [ ] `C-CF-87` `literal` The shorter rail reads `01 / 04`. `src: Core features, colour chapter rule 4`
- [ ] `C-CF-88` `literal` A swatch sample carries the `HEX` label beside the value of the sample the label names. `src: Core features, colour chapter rule 5`
- [ ] `C-CF-89` `constraint` The swatch readout is the one place in the product showing a colour value as text. `src: Core features, colour chapter rule 5`
- [ ] `C-CF-90` `ui` The colour chapter closes on a poster carrying the trial call to action. `src: Core features, colour chapter rule 6`
- [ ] `C-CF-91` `literal` The colour chapter carries an `Explore Colors` affordance after the closing poster. `src: Core features, colour chapter rule 6`
- [ ] `C-CF-92` `literal` The colour chapter's next-chapter affordance reads `Photography`. `src: Core features, colour chapter rule 6`
- [ ] `C-CF-93` `ui` The logo chapter opens on a white ground carrying the display headline, the chapter lead. `src: Core features, logo chapter rule 1`
- [ ] `C-CF-94` `literal` The logo chapter's display headline reads `Logo`. `src: Core features, logo chapter rule 1`
- [ ] `C-CF-95` `ui` A dark section follows the logo chapter's opening immediately below. `src: Core features, logo chapter rule 1`
- [ ] `C-CF-96` `ui` The mark is presented as a monogram, a wordmark set in the display face. `src: Core features, logo chapter rule 2`
- [ ] `C-CF-97` `constraint` The monogram, the wordmark are painted through masks rather than drawn as strokes. `src: Core features, logo chapter rule 2`
- [ ] `C-CF-98` `capability` One fill colour drives the monogram, the wordmark, so the mask animates independently as the visitor scrolls. `src: Core features, logo chapter rule 2`
- [ ] `C-CF-99` `ui` A logo chapter section states the clear space rule, which surrounds the logo so other elements neither compete with nor crowd the logo. `src: Core features, logo chapter rule 3`
- [ ] `C-CF-100` `ui` A logo chapter section states the secondary-colour rule. `src: Core features, logo chapter rule 3`
- [ ] `C-CF-101` `ui` A logo chapter section states the misuse rule, that the logo is never shown warped, distorted, oriented at an angle. `src: Core features, logo chapter rule 3`
- [ ] `C-CF-102` `literal` The partnership lockup is built around an equidistant `X` between brand names. `src: Core features, logo chapter rule 4`
- [ ] `C-CF-103` `ui` The partnership cross is built from a quarter the thickness of the E's horizontal stroke, angled at 45 degrees to make a perfect square. `src: Core features, logo chapter rule 4`
- [ ] `C-CF-104` `literal` A second lockup is the `Latticework Presents` lockup for cinematic video. `src: Core features, logo chapter rule 4`
- [ ] `C-CF-105` `literal` The logo chapter's paginated in-use gallery reads `01 / 07`. `src: Core features, logo chapter rule 5`
- [ ] `C-CF-106` `ui` The in-use gallery shows the mark applied across formats, revealed by the logo-block wipe. `src: Core features, logo chapter rule 5`
- [ ] `C-CF-107` `ui` A mark-in-motion block sits inside the gallery with the block's opacity, position scrubbed. `src: Core features, logo chapter rule 5`
- [ ] `C-CF-108` `ui` The mark-in-motion block opens in an overlay dismissed by the close cross. `src: Core features, logo chapter rule 5`
- [ ] `C-CF-109` `capability` A three-dimensional renderer composites a scene into a canvas sized to the viewport. `src: Core features, model surface rule 1`
- [ ] `C-CF-110` `capability` The three-dimensional scene uses a perspective camera. `src: Core features, model surface rule 1`
- [ ] `C-CF-111` `ui` The scene is a centred, faceted, low-polygon model shaded by surface normal, so facets take colour from orientation. `src: Core features, model surface rule 2`
- [ ] `C-CF-112` `constraint` The normal-shaded material needs no texture. `src: Core features, model surface rule 2`
- [ ] `C-CF-113` `ui` A solid red primitive flanks the model on the left, a solid blue primitive on the right, on a plain ground. `src: Core features, model surface rule 2`
- [ ] `C-CF-114` `ui` The model turns slowly about the model's vertical axis. `src: Core features, model surface rule 2`
- [ ] `C-CF-115` `constraint` The frame loop stops entirely when the model surface is off-screen. `src: Core features, model surface rule 3`
- [ ] `C-CF-116` `constraint` The frame loop resumes when the model surface returns to the screen. `src: Core features, model surface rule 3`
- [ ] `C-CF-117` `constraint` The model geometry is composed from primitives rather than loaded. `src: Core features, model surface rule 4`
- [ ] `C-CF-118` `constraint` A debug parameter panel stays development-only, never shipping. `src: Core features, model surface rule 4`
- [ ] `C-CF-119` `capability` The app generates every image the product shows once, from a seed derived from the image's media key. `src: Core features, imagery rule 1`
- [ ] `C-CF-120` `ui` A generated image is tinted from the tone group the image sits in. `src: Core features, imagery rule 1`
- [ ] `C-CF-121` `literal` The app stores generated image bytes in MinIO at `STORAGE_ENDPOINT`, `STORAGE_BUCKET`. `src: Core features, imagery rule 1`
- [ ] `C-CF-122` `literal` The app reaches the object store with `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Core features, imagery rule 1`
- [ ] `C-CF-123` `constraint` No image bytes live on the app's filesystem. `src: Core features, imagery rule 1`
- [ ] `C-CF-124` `constraint` No image bytes live in a database column. `src: Core features, imagery rule 1`
- [ ] `C-CF-125` `literal` The object key scheme is `media/{chapter_slug}/{media_key}/{sha256_of_bytes}.png`. `src: Core features, imagery rule 2`
- [ ] `C-CF-126` `literal` The worked example stores the media key `core-poster-01` under the colour chapter at the scheme's key. `src: Core features, imagery rule 2`
- [ ] `C-CF-127` `constraint` The same seed under the same generator produces the same bytes, so a regenerated image lands on the same key. `src: Core features, imagery rule 3`
- [ ] `C-CF-128` `constraint` The digest in an object key is the digest of the bytes, so a stored image is answerable against the digest. `src: Core features, imagery rule 3`
- [ ] `C-CF-129` `ui` A tone-group image, an in-use image is a soft studio gradient in the group's colour carrying a faint film grain. `src: Core features, imagery rule 4`
- [ ] `C-CF-130` `ui` A storefront mock, a product-interface mock is a flat colour-blocked layout. `src: Core features, imagery rule 4`
- [ ] `C-CF-131` `ui` Every generated image is marked as a placeholder, so no image is mistaken for the brand's real photography. `src: Core features, imagery rule 4`
- [ ] `C-CF-132` `capability` A published chapter's image is readable by anyone. `src: Core features, imagery rule 5`
- [ ] `C-CF-133` `constraint` An unpublished chapter's image is served only through an authenticated stream on the product's own origin. `src: Core features, imagery rule 5`
- [ ] `C-CF-134` `constraint` The authenticated stream checks the caller before reading the object. `src: Core features, imagery rule 5`
- [ ] `C-CF-135` `constraint` The bucket is never publicly readable. `src: Core features, imagery rule 5`
- [ ] `C-CF-136` `constraint` The app hands out no pre-signed address for a stored object. `src: Core features, imagery rule 5`
- [ ] `C-CF-137` `constraint` Every media row has a real object at the row's key. `src: Core features, imagery rule 6`
- [ ] `C-CF-138` `constraint` Every object under a chapter's prefix has a media row. `src: Core features, imagery rule 6`
- [ ] `C-CF-139` `ui` The mark-in-motion block, the poster sequences are looped generated sequences produced by the product rather than video files. `src: Core features, imagery rule 7`
- [ ] `C-CF-140` `literal` The closing poster carries the pinned trial title, the pinned trial body, one email field, one control. `src: Core features, trial rule 1`
- [ ] `C-CF-141` `constraint` The trial form carries exactly three states, `idle`, `success`, `failure`. `src: Core features, trial rule 2`
- [ ] `C-CF-142` `constraint` All three trial states are present in the page, toggled rather than injected when the answer arrives. `src: Core features, trial rule 2`
- [ ] `C-CF-143` `capability` The app accepts a valid address, answering with the pinned success copy. `src: Core features, trial rule 3`
- [ ] `C-CF-144` `constraint` The app refuses an address that is not a valid address inline, beside the field, naming the field. `src: Core features, trial rule 4`
- [ ] `C-CF-145` `constraint` A refused trial submission writes nothing. `src: Core features, trial rule 4`
- [ ] `C-CF-146` `constraint` Submitting the same address twice produces exactly one record. `src: Core features, trial rule 5`
- [ ] `C-CF-147` `constraint` A repeat trial submission does not move the first record's moment. `src: Core features, trial rule 5`
- [ ] `C-CF-148` `capability` The app answers a repeat trial submission as a success, so a visitor is never told off for pressing twice. `src: Core features, trial rule 5`
- [ ] `C-CF-149` `data` A trial record keeps which chapter the visitor was reading at submission. `src: Core features, trial rule 6`
- [ ] `C-CF-150` `constraint` The trial list is readable by an author, by nobody else. `src: Core features, trial rule 7`
- [ ] `C-CF-151` `capability` An author creates a chapter through a route per step, details, sections, media, then review. `src: Core features, author surface rule 1`
- [ ] `C-CF-152` `ui` Each wizard step is reachable at the step's own address. `src: Core features, author surface rule 1`
- [ ] `C-CF-153` `ui` The review step carries the publish control. `src: Core features, author surface rule 1`
- [ ] `C-CF-154` `capability` An author reorders a chapter's sections by dragging a row. `src: Core features, author surface rule 2`
- [ ] `C-CF-155` `ui` A dragged row moves at once. `src: Core features, author surface rule 2`
- [ ] `C-CF-156` `ui` A refused reorder puts the dragged row back with a message saying so. `src: Core features, author surface rule 2`
- [ ] `C-CF-157` `constraint` Section positions stay contiguous from one after a reorder, so a reorder is a permutation rather than an insertion leaving a hole. `src: Core features, author surface rule 2`
- [ ] `C-CF-158` `capability` An author generates a section's imagery from the author surface, writing the bytes to the object store, the row beside the bytes. `src: Core features, author surface rule 3`
- [ ] `C-CF-159` `constraint` Every form in the author surface refuses invalid input inline, naming the field that was wrong. `src: Core features, author surface rule 4`
- [ ] `C-CF-160` `constraint` A form that refuses writes nothing. `src: Core features, author surface rule 4`
- [ ] `C-CF-161` `constraint` The endpoints surface is reachable by an author only. `src: Core features, author surface rule 5`
- [ ] `C-CF-162` `ui` The endpoints surface exercises the content functions in isolation under a single pinned heading. `src: Core features, author surface rule 5`
- [ ] `C-CF-163` `constraint` The endpoints surface is not a public chapter, appearing in no sitemap. `src: Core features, author surface rule 5`
- [ ] `C-CF-164` `ui` A fixed header band paints no ground of the band's own. `src: Core features, chrome rule 1`
- [ ] `C-CF-165` `literal` The header carries the wordmark `Latticework Foundations` at the left. `src: Core features, chrome rule 1`
- [ ] `C-CF-166` `literal` The header carries the `Index` control at the right. `src: Core features, chrome rule 1`
- [ ] `C-CF-167` `ui` The wordmark composites against whatever passes behind the wordmark, reading dark on the white colour chapter, light on the dark index. `src: Core features, chrome rule 1`
- [ ] `C-CF-168` `ui` The menu button opens a full-screen menu over a frosted ground. `src: Core features, chrome rule 2`
- [ ] `C-CF-169` `ui` Menu items rest at full opacity, dimming when a sibling is pointed at, so the pointed-at item stands alone. `src: Core features, chrome rule 2`
- [ ] `C-CF-170` `constraint` The full-screen menu traps focus for as long as the menu is open. `src: Core features, chrome rule 2`
- [ ] `C-CF-171` `ui` The full-screen menu closes on the close cross. `src: Core features, chrome rule 2`
- [ ] `C-CF-172` `constraint` The full-screen menu returns focus to the control that opened the menu. `src: Core features, chrome rule 2`
- [ ] `C-CF-173` `ui` A route change is covered by a mask that wipes away on arrival. `src: Core features, chrome rule 3`
- [ ] `C-CF-174` `literal` First load shows a counter climbing to `100%` beside the word `Loading`. `src: Core features, chrome rule 4`
- [ ] `C-CF-175` `ui` The loader mark turns slowly counter-clockwise. `src: Core features, chrome rule 4`
- [ ] `C-CF-176` `constraint` The page entrance is gated on the loader completing rather than on a timer. `src: Core features, chrome rule 4`
- [ ] `C-CF-177` `ui` A first-time visitor is asked once about non-essential cookies in the product's own panel. `src: Core features, chrome rule 5`
- [ ] `C-CF-178` `constraint` Rejecting non-essential cookies is exactly as easy as accepting. `src: Core features, chrome rule 5`
- [ ] `C-CF-179` `constraint` The cookie answer survives a reload. `src: Core features, chrome rule 5`
- [ ] `C-CF-180` `literal` An unknown address renders a single centred line reading `404: Page not found` under the full chrome. `src: Core features, chrome rule 6`
- [ ] `C-CF-181` `contract` An unknown address answers not-found. `src: Core features, chrome rule 6`
- [ ] `C-CF-182` `ui` The not-found body carries a way back to the index. `src: Core features, chrome rule 6`
- [ ] `C-CF-183` `constraint` The not-found body carries no chapter motion, driving no colour system. `src: Core features, chrome rule 6`
- [ ] `C-CF-184` `constraint` Every internal link on every public route resolves to a route that exists, answering. `src: Core features, chrome rule 7`
- [ ] `C-CF-185` `capability` A sitemap lists every published public route. `src: Core features, chrome rule 8`
- [ ] `C-CF-186` `capability` A robots file names the sitemap. `src: Core features, chrome rule 8`
- [ ] `C-CF-187` `capability` The site serves a favicon, declaring the favicon in the document head. `src: Core features, chrome rule 8`
- [ ] `C-CF-188` `capability` Every public route declares a social preview title, a social preview image. `src: Core features, chrome rule 9`
- [ ] `C-CF-189` `constraint` A declared social preview image resolves. `src: Core features, chrome rule 9`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves the index carousel at `/`. `src: User flow route table`
- [ ] `C-UF-02` `literal` The app serves the colour chapter at `/color` once published. `src: User flow route table`
- [ ] `C-UF-03` `literal` The app serves the logo chapter at `/logo` once published. `src: User flow route table`
- [ ] `C-UF-04` `literal` The app serves the unpublished chapter address `/typography` to the chapter's author only. `src: User flow route table`
- [ ] `C-UF-05` `literal` The app serves the unpublished chapter address `/photography` to the chapter's author only. `src: User flow route table`
- [ ] `C-UF-06` `literal` The app serves the unpublished chapter address `/motion` to the chapter's author only. `src: User flow route table`
- [ ] `C-UF-07` `literal` The app serves the full-screen menu at `/menu`. `src: User flow route table`
- [ ] `C-UF-08` `literal` The app serves the model surface at `/webgl`. `src: User flow route table`
- [ ] `C-UF-09` `literal` The app serves the endpoints surface at `/lambda` to an author only. `src: User flow route table`
- [ ] `C-UF-10` `literal` The app serves account creation at `/signup`. `src: User flow route table`
- [ ] `C-UF-11` `literal` The app serves sign-in at `/login`. `src: User flow route table`
- [ ] `C-UF-12` `literal` The app serves sign-out at `/logout`. `src: User flow route table`
- [ ] `C-UF-13` `literal` The app serves the author's own chapters at `/studio` as a card grid. `src: User flow route table`
- [ ] `C-UF-14` `literal` The app serves the first wizard step at `/studio/chapters/new/details`. `src: User flow route table`
- [ ] `C-UF-15` `literal` The app serves the second wizard step at `/studio/chapters/new/sections`. `src: User flow route table`
- [ ] `C-UF-16` `literal` The app serves the third wizard step at `/studio/chapters/new/media`. `src: User flow route table`
- [ ] `C-UF-17` `literal` The app serves the fourth wizard step at `/studio/chapters/new/review`. `src: User flow route table`
- [ ] `C-UF-18` `literal` The app serves one chapter's reorderable sections at `/studio/chapters/<slug>` to the owning author. `src: User flow route table`
- [ ] `C-UF-19` `literal` The app serves the trial list at `/studio/trials` to an author. `src: User flow route table`
- [ ] `C-UF-20` `literal` The app serves a sitemap at `/sitemap.xml`. `src: User flow route table`
- [ ] `C-UF-21` `literal` The app serves a robots file at `/robots.txt`. `src: User flow route table`
- [ ] `C-UF-22` `literal` The app serves a favicon at `/favicon.ico`. `src: User flow route table`
- [ ] `C-UF-23` `literal` The app answers readiness at `GET /api/health`. `src: User flow route table`
- [ ] `C-UF-24` `constraint` An unauthenticated request for a `/studio` address goes to `/login` carrying the address that was asked for. `src: User flow, entry paragraph`
- [ ] `C-UF-25` `constraint` An unauthenticated request for `/lambda` goes to `/login` carrying the address that was asked for. `src: User flow, entry paragraph`
- [ ] `C-UF-26` `capability` A caller redirected to sign-in lands on the requested address once signed in. `src: User flow, entry paragraph`
- [ ] `C-UF-27` `capability` Signing in sends an author to `/studio`. `src: User flow, entry paragraph`
- [ ] `C-UF-28` `capability` Signing in sends a reader to `/`. `src: User flow, entry paragraph`
- [ ] `C-UF-29` `capability` Signing out returns the caller to `/`, stopping the token from working. `src: User flow, entry paragraph`
- [ ] `C-UF-30` `constraint` A token expiring part way through an edit returns the author to `/login` with nothing written. `src: User flow, entry paragraph`
- [ ] `C-UF-31` `constraint` The server refuses a reader a `/studio` address rather than merely showing a page without the link. `src: User flow, entry paragraph`
- [ ] `C-UF-32` `constraint` The server refuses a reader `/lambda` rather than merely showing a page without the link. `src: User flow, entry paragraph`
- [ ] `C-UF-33` `constraint` Every unknown address other than an unpublished chapter's renders the not-found body, answering not-found. `src: User flow, entry paragraph`
- [ ] `C-UF-34` `ui` A visitor opening `/` sees the counter climb, the entrance play, the carousel take over. `src: User flow, journey 1`
- [ ] `C-UF-35` `ui` Pressing the next control morphs the frame window as the image inside holds still. `src: User flow, journey 1`
- [ ] `C-UF-36` `ui` Scrolling `/color` washes the ground continuously rather than switching at each section. `src: User flow, journey 2`
- [ ] `C-UF-37` `ui` Scrolling `/color` back up un-rises the lines rather than replaying the lines. `src: User flow, journey 2`
- [ ] `C-UF-38` `ui` Pressing the shuffle control reorders the swatches, cross-fading the poster imagery, writing nothing. `src: User flow, journey 3`
- [ ] `C-UF-39` `capability` Submitting an address at the closing poster replaces the idle state in place with the success copy. `src: User flow, journey 4`
- [ ] `C-UF-40` `constraint` Submitting the same address a second time leaves exactly one record. `src: User flow, journey 4`
- [ ] `C-UF-41` `ui` Following the explore affordance then the next-chapter affordance arrives at `/logo` through the route mask. `src: User flow, journey 5`
- [ ] `C-UF-42` `constraint` A direct request for `/typography` is refused, serving no chapter content. `src: User flow, journey 6`
- [ ] `C-UF-43` `ui` An author signing in lands on `/studio`, showing the author's own chapters as a card grid. `src: User flow, journey 7`
- [ ] `C-UF-44` `capability` Walking the four wizard steps then publishing makes the new chapter readable at the chapter's slug, joining the sitemap. `src: User flow, journey 7`
- [ ] `C-UF-45` `capability` A saved section order survives a reload with positions contiguous from one. `src: User flow, journey 8`
- [ ] `C-UF-46` `constraint` A request by `author@example.com` for the `motion` chapter, the chapter's sections, the chapter's image is denied on all three. `src: User flow, journey 9`
- [ ] `C-UF-47` `constraint` A request by `reader@example.com` for `/studio`, `/studio/trials`, `/lambda` is denied on all three. `src: User flow, journey 10`
- [ ] `C-UF-48` `ui` Scrolling the model surface out of view stops the frame loop rather than continuing to draw. `src: User flow, journey 11`
- [ ] `C-UF-49` `ui` Every list carries an empty state naming what would fill the list. `src: User flow, states paragraph`
- [ ] `C-UF-50` `ui` Every surface that waits says so, the first-load counter included. `src: User flow, states paragraph`
- [ ] `C-UF-51` `constraint` An error never leaves a blank page. `src: User flow, states paragraph`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product reads as a gallery rather than a manual in the first moment. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The product feels unhurried, the way a room holding one object holds a visitor. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The register is editorial, so the subject is the first thing seen, never an operational dashboard. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `ui` The product chooses restraint over expression, continuity over punctuation, space over dividers. `src: UI/UX notes para 1`
- [ ] `C-UX-05` `ui` The resting page ground is a near-white neutral carrying a near-black neutral ink. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` A second near-black neutral serves as the section ground in place of true black. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` A near-white neutral one step deeper carries hairlines, inactive interface. `src: UI/UX notes para 2`
- [ ] `C-UX-08` `ui` A further near-white neutral is the off-white ground, also the ground behind imagery. `src: UI/UX notes para 2`
- [ ] `C-UX-09` `constraint` The near-white ground dominates by close to two orders of magnitude over every other value. `src: UI/UX notes para 2`
- [ ] `C-UX-10` `constraint` The near-black section ground is the second structural colour. `src: UI/UX notes para 2`
- [ ] `C-UX-11` `ui` Three accents stay in reserve, appearing rarely: a mid soft orange, a mid vivid blue, a mid vivid red. `src: UI/UX notes para 2`
- [ ] `C-UX-12` `constraint` The three accents are never part of the resting surface. `src: UI/UX notes para 2`
- [ ] `C-UX-13` `ui` A small set of translucent neutrals carries hairlines, scrims, unavailable states on the light ground, on the dark ground. `src: UI/UX notes para 2`
- [ ] `C-UX-14` `ui` The `Core` group is a deep warm neutral on the wider tiers, a near-black neutral on a phone. `src: UI/UX notes para 3`
- [ ] `C-UX-15` `ui` The `Dark` group is a deep neutral on desktop, on phone, a mid warm neutral on a tablet. `src: UI/UX notes para 3`
- [ ] `C-UX-16` `ui` The `Bright` group is a light soft orange on desktop, on phone, a mid soft orange on a tablet. `src: UI/UX notes para 3`
- [ ] `C-UX-17` `ui` The `Light` group is near-white on every tier. `src: UI/UX notes para 3`
- [ ] `C-UX-18` `ui` The ink is near-white across the two dark groups, near-black across the two light groups. `src: UI/UX notes para 3`
- [ ] `C-UX-19` `ui` The logo chapter's fill moves from near-black toward a light cool neutral on desktop, a deep soft orange on a tablet, a near-black neutral on a phone. `src: UI/UX notes para 3`
- [ ] `C-UX-20` `ui` The logo chapter's counter-fill moves toward near-white. `src: UI/UX notes para 3`
- [ ] `C-UX-21` `literal` The display, heading, interface face is `Grotesk Display` at weights 300, 400, 500, 600, 700. `src: UI/UX notes para 4`
- [ ] `C-UX-22` `literal` The editorial companion is `Grotesk Serif` at 300, 400, 500, upright, italic. `src: UI/UX notes para 4`
- [ ] `C-UX-23` `literal` The oversized poster lettering is `Grotesk Condensed` at 300, 400, 500, 700, 900. `src: UI/UX notes para 4`
- [ ] `C-UX-24` `constraint` Each type role falls back through a normative stack, loading with swap behaviour, so no line of type is ever invisible. `src: UI/UX notes para 4`
- [ ] `C-UX-25` `ui` The rendered type scale runs from the largest full-bleed poster words down to the eyebrow index numbers at the pinned sizes. `src: UI/UX notes para 4`
- [ ] `C-UX-26` `constraint` The rendered sizes are the result of a viewport-derived root rather than values to hard-code. `src: UI/UX notes para 4`
- [ ] `C-UX-27` `ui` Headings are set solid, at a line height near the heading's own size, so poster words bleed off the viewport edges. `src: UI/UX notes para 4`
- [ ] `C-UX-28` `ui` Everything structural is square. `src: UI/UX notes para 5`
- [ ] `C-UX-29` `ui` The only circles in the product are the pagination dots, the menu dots. `src: UI/UX notes para 5`
- [ ] `C-UX-30` `ui` Code, small chips carry the one small softening. `src: UI/UX notes para 5`
- [ ] `C-UX-31` `ui` The mocked search field inside the in-use posters is the one pill shape anywhere. `src: UI/UX notes para 5`
- [ ] `C-UX-32` `ui` Density is spacious, one subject per screen, room around the subject. `src: UI/UX notes para 5`
- [ ] `C-UX-33` `ui` Sections are separated by space rather than by a dividing rule. `src: UI/UX notes para 5`
- [ ] `C-UX-34` `ui` The twelve-column grid holds at every width. `src: UI/UX notes para 5`
- [ ] `C-UX-35` `ui` The gap between sections is a multiple of the gap beneath a heading rather than an independent measure. `src: UI/UX notes para 5`
- [ ] `C-UX-36` `ui` The motion character is eased, a considered entrance, a considered exit. `src: UI/UX notes para 6`
- [ ] `C-UX-37` `ui` One house ease-out is the dominant curve, carrying the reveal transforms, a slow-out settle easing off at the end. `src: UI/UX notes para 6`
- [ ] `C-UX-38` `ui` A sine ease-out carries the colour, background moves. `src: UI/UX notes para 6`
- [ ] `C-UX-39` `ui` A symmetric sine ease-in-out carries transitions that come, go the same way. `src: UI/UX notes para 6`
- [ ] `C-UX-40` `ui` A standard curve carries interface state changes. `src: UI/UX notes para 6`
- [ ] `C-UX-41` `ui` A quad ease-out carries the slower, longer transforms. `src: UI/UX notes para 6`
- [ ] `C-UX-42` `ui` A cubic ease-in-out carries the long colour sweep. `src: UI/UX notes para 6`
- [ ] `C-UX-43` `ui` A width hold grows a width almost instantly, holding a long tail. `src: UI/UX notes para 6`
- [ ] `C-UX-44` `constraint` Colour is always the slowest thing on the page. `src: UI/UX notes para 6`
- [ ] `C-UX-45` `constraint` A state change is always the quickest thing on the page. `src: UI/UX notes para 6`
- [ ] `C-UX-46` `constraint` Nothing uses a different speed to feel special. `src: UI/UX notes para 6`
- [ ] `C-UX-47` `constraint` Exactly one keyframe loop exists in the product, the loader's mark turning counter-clockwise. `src: UI/UX notes para 6`
- [ ] `C-UX-48` `constraint` No blanket rule transitions every property on an interactive shell. `src: UI/UX notes para 6`
- [ ] `C-UX-49` `ui` Text rises into place line by line, un-rising on the way back up. `src: UI/UX notes para 7`
- [ ] `C-UX-50` `ui` A parenthetical tag lands a beat after the sentence the tag labels. `src: UI/UX notes para 7`
- [ ] `C-UX-51` `ui` An arrow rolls over to a fresh copy of itself rather than fading. `src: UI/UX notes para 7`
- [ ] `C-UX-52` `ui` A logo lockup wipes open from the lockup's bottom edge as the lockup's content holds still. `src: UI/UX notes para 7`
- [ ] `C-UX-53` `ui` A card's picture frame changes shape as the picture inside holds position. `src: UI/UX notes para 7`
- [ ] `C-UX-54` `ui` The menu arrives over a frosted ground, dimming the items a pointer is not on. `src: UI/UX notes para 7`
- [ ] `C-UX-55` `ui` The whole page washes from one tone group to the next as a continuous repaint. `src: UI/UX notes para 7`
- [ ] `C-UX-56` `constraint` Under a reduced-motion preference each named moment is replaced rather than frozen. `src: UI/UX notes para 7`
- [ ] `C-UX-57` `ui` Under reduced motion the line cascade resolves to the end state with a short fade, no movement. `src: UI/UX notes para 7`
- [ ] `C-UX-58` `ui` Under reduced motion the repaint applies each section's end colour as a short cross-fade rather than a scrub. `src: UI/UX notes para 7`
- [ ] `C-UX-59` `ui` Under reduced motion the loader shows the counter without the turning mark. `src: UI/UX notes para 7`
- [ ] `C-UX-60` `ui` Under reduced motion the carousel advances by a cut. `src: UI/UX notes para 7`
- [ ] `C-UX-61` `constraint` Under reduced motion the fade is preserved, so movement alone is what goes. `src: UI/UX notes para 7`
- [ ] `C-UX-62` `ui` Index cards live in a shallow three-dimensional stack, tilting as the cards pass. `src: UI/UX notes para 8`
- [ ] `C-UX-63` `ui` Layering runs a short set of stacking levels, content at the bottom, interface above, menu with route mask at the top. `src: UI/UX notes para 8`
- [ ] `C-UX-64` `constraint` Nothing is introduced above the top stacking level. `src: UI/UX notes para 8`
- [ ] `C-UX-65` `ui` A component draws resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes para 9`
- [ ] `C-UX-66` `constraint` Unavailable is never signalled by colour alone. `src: UI/UX notes para 9`
- [ ] `C-UX-67` `ui` Escape closes the menu, the video overlay, returning focus to the control that opened either. `src: UI/UX notes para 9`
- [ ] `C-UX-68` `constraint` Hover treatments are declared only where a fine pointer exists. `src: UI/UX notes para 9`
- [ ] `C-UX-69` `constraint` Anything revealing on hover is permanently revealed where there is no pointer, so a tap never leaves a control stuck looking pressed. `src: UI/UX notes para 9`
- [ ] `C-UX-70` `ui` A coarse pointer gets the drag affordance. `src: UI/UX notes para 9`
- [ ] `C-UX-71` `constraint` Each route carries one first-rank heading naming the chapter. `src: UI/UX notes para 10`
- [ ] `C-UX-72` `constraint` The parenthetical eyebrows are not headings. `src: UI/UX notes para 10`
- [ ] `C-UX-73` `constraint` A main landmark wraps chapter content, the header is a banner, the full-screen menu is a labelled dialog. `src: UI/UX notes para 10`
- [ ] `C-UX-74` `ui` Every chapter is reachable by keyboard navigation, the carousel advancing with the arrow keys. `src: UI/UX notes para 10`
- [ ] `C-UX-75` `constraint` A visible focus ring is present throughout, never suppressed. `src: UI/UX notes para 10`
- [ ] `C-UX-76` `constraint` Every content image carries a text alternative from the content layer. `src: UI/UX notes para 10`
- [ ] `C-UX-77` `constraint` Every decorative image declares itself decorative. `src: UI/UX notes para 10`
- [ ] `C-UX-78` `constraint` The model surface, the mark's mask geometry are hidden from assistive technology. `src: UI/UX notes para 10`
- [ ] `C-UX-79` `constraint` The loader announces progress politely. `src: UI/UX notes para 10`
- [ ] `C-UX-80` `constraint` Body text holds a contrast ratio at or above `4.5:1` at every point between two stops. `src: UI/UX notes para 10`
- [ ] `C-UX-81` `constraint` Large text holds a contrast ratio at or above `3:1` at every point between two stops. `src: UI/UX notes para 10`
- [ ] `C-UX-82` `constraint` No interactive target is smaller than a comfortable fingertip. `src: UI/UX notes para 10`
- [ ] `C-UX-83` `constraint` Every icon-only control carries a name saying what the control does rather than what the control depicts. `src: UI/UX notes para 10`
- [ ] `C-UX-84` `ui` The layout turns on one primary breakpoint, with orientation refinements, pointer refinements above. `src: UI/UX notes para 11`
- [ ] `C-UX-85` `constraint` The layout holds at every width between the named tiers rather than only at the tiers. `src: UI/UX notes para 11`
- [ ] `C-UX-86` `ui` Below the breakpoint the carousel, the poster layouts restack to a single column. `src: UI/UX notes para 11`
- [ ] `C-UX-87` `ui` Below the breakpoint the side margin, the column width contract as the twelve-column structure survives. `src: UI/UX notes para 11`
- [ ] `C-UX-88` `constraint` The colour journey uses the journey's own per-tier stops rather than inheriting the desktop stops. `src: UI/UX notes para 11`
- [ ] `C-UX-89` `constraint` Landscape, portrait each get a refinement at the same boundary rather than being collapsed to width alone. `src: UI/UX notes para 11`
- [ ] `C-UX-90` `constraint` A full-height surface measures the real visible height rather than the naive viewport unit. `src: UI/UX notes para 11`
- [ ] `C-UX-91` `constraint` At a narrow viewport nothing overflows sideways. `src: UI/UX notes para 11`
- [ ] `C-UX-92` `constraint` At a narrow viewport every navigation target stays reachable. `src: UI/UX notes para 11`
- [ ] `C-UX-93` `ui` Each page leads with one clear primary action, visually distinct from every secondary one. `src: UI/UX notes, primary action paragraph`
- [ ] `C-UX-94` `constraint` Nothing competes with a page's one primary action. `src: UI/UX notes, primary action paragraph`
- [ ] `C-UX-95` `constraint` No page is dominated by one hue family with no second signal for meaning. `src: UI/UX notes, failures paragraph`
- [ ] `C-UX-96` `constraint` Colour is never used as decoration outside the chapter that is about colour. `src: UI/UX notes, failures paragraph`
- [ ] `C-UX-97` `constraint` No reveal replays forward on the way back up. `src: UI/UX notes, failures paragraph`
- [ ] `C-UX-98` `constraint` No decoration stands in for content on a page whose subject is the content. `src: UI/UX notes, failures paragraph`
- [ ] `C-UX-99` `constraint` No marketing composition appears inside the author surface. `src: UI/UX notes, failures paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` One token layer is defined once at the document root, consumed everywhere. `src: Front-end specification, token layer`
- [ ] `C-FE-02` `ui` The grid is twelve columns expressed through named tokens. `src: Front-end specification, token layer`
- [ ] `C-FE-03` `ui` The named grid tokens are a column count, a nominal column width at the desktop tier, a column gap that is the gutter between columns. `src: Front-end specification, token layer`
- [ ] `C-FE-04` `ui` The named grid tokens carry a page side margin, a reserved header band, a gap around the carousel arrow controls. `src: Front-end specification, token layer`
- [ ] `C-FE-05` `ui` The named grid tokens carry a reserved footer band at the bottom, a spacer reconciling the collapsing mobile browser chrome. `src: Front-end specification, token layer`
- [ ] `C-FE-06` `constraint` The root sizing is viewport-derived, so type, spacing grow together between the tiers. `src: Front-end specification, token layer`
- [ ] `C-FE-07` `constraint` Reproducing the sizing rule is what produces the fractional rendered scale. `src: Front-end specification, token layer`
- [ ] `C-FE-08` `ui` Three widths are the references, a desktop width, a tablet width, a phone width. `src: Front-end specification, token layer`
- [ ] `C-FE-09` `ui` Colour tokens are declared on the root by role rather than by hue. `src: Front-end specification, token layer`
- [ ] `C-FE-10` `ui` The declared roles carry the text colour on light grounds, the text colour on dark grounds, the near-black section ground. `src: Front-end specification, token layer`
- [ ] `C-FE-11` `ui` The declared roles carry the off-white ground that doubles as the default media ground, the hairline grey, the three reserved accents. `src: Front-end specification, token layer`
- [ ] `C-FE-12` `ui` The declared roles carry the five animated properties at the properties' resting values. `src: Front-end specification, token layer`
- [ ] `C-FE-13` `constraint` The header declares a transparent ground, never painting one. `src: Front-end specification, token layer`
- [ ] `C-FE-14` `ui` A handful of structural greys sit between the near-black, the near-white for hairlines, dividers. `src: Front-end specification, token layer`
- [ ] `C-FE-15` `ui` The wordmark, the carousel interface text, the invitation label composite against whatever passes behind them. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-16` `constraint` One declared colour reads correctly on a white chapter, on a dark index, without switching by rule. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-17` `ui` A heavy backdrop blur sits behind the full-screen menu ground. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-18` `ui` A light backdrop blur sits behind the consent panel. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-19` `ui` The editorial reveal, the carousel frame are driven by clip geometry rather than by opacity. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-20` `ui` The clip vocabulary is a wipe hidden from the bottom up, a fully open state, three carousel aspect insets. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-21` `ui` Carousel items, the items' inner fills preserve three-dimensional space. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-22` `constraint` Compositor hints go only on elements animating right now. `src: Front-end specification, effects vocabulary`
- [ ] `C-FE-23` `ui` Stacking runs scrolling content at the bottom two levels. `src: Front-end specification, layering`
- [ ] `C-FE-24` `ui` Stacking runs the carousel, the chapter interface in the middle band. `src: Front-end specification, layering`
- [ ] `C-FE-25` `ui` Stacking runs the full-screen menu, the page-transition mask at the top. `src: Front-end specification, layering`
- [ ] `C-FE-26` `constraint` Each glyph is drawn on a declared viewBox whose path extent fills the box. `src: Front-end specification, iconography`
- [ ] `C-FE-27` `ui` The directional arrow is one closed path filled with the current colour, mirrored on the vertical axis for the left variant. `src: Front-end specification, iconography`
- [ ] `C-FE-28` `ui` A control holds a main arrow layer, a secondary arrow layer, translating together so one glyph leaves as the duplicate arrives. `src: Front-end specification, iconography`
- [ ] `C-FE-29` `ui` The close cross is a square canvas holding two full-diagonal strokes with round caps, stroked in the current colour. `src: Front-end specification, iconography`
- [ ] `C-FE-30` `ui` The close cross dismisses the full-screen menu, the video overlay. `src: Front-end specification, iconography`
- [ ] `C-FE-31` `ui` The ring is a single unfilled circle at one hairline stroke, used as a control outline, a pagination mark. `src: Front-end specification, iconography`
- [ ] `C-FE-32` `ui` The dot is a filled, fully round disc sized by the dot's container, used as a pagination mark, a menu-position mark. `src: Front-end specification, iconography`
- [ ] `C-FE-33` `constraint` The four glyphs are inline geometry, never a file. `src: Front-end specification, iconography`
- [ ] `C-FE-34` `ui` The brand mark is a monogram symbol, a wordmark, both painted through masks rather than as strokes. `src: Front-end specification, iconography`
- [ ] `C-FE-35` `capability` A single fill colour drives the mark, so the mask animates independently. `src: Front-end specification, iconography`
- [ ] `C-FE-36` `constraint` The mark's own geometry is supplied as two inline symbols used exactly as masks, so the scroll recolour works unchanged whatever mark is dropped in. `src: Front-end specification, iconography`
- [ ] `C-FE-37` `constraint` An internal mask reference, an internal filter reference is made unique per instance, so two copies of one drawing never collide. `src: Front-end specification, iconography`
- [ ] `C-FE-38` `ui` The header is a fixed band of the reserved header height painting no ground. `src: Front-end specification, global chrome`
- [ ] `C-FE-39` `ui` On a chapter the left label is joined by a second line reading the index word, both taking part in the scroll reveal. `src: Front-end specification, global chrome`
- [ ] `C-FE-40` `ui` The menu button's only state change is a fade to half opacity. `src: Front-end specification, global chrome`
- [ ] `C-FE-41` `ui` The full-screen menu is a fixed overlay above all content, over a heavy backdrop blur, on a ground at low opacity. `src: Front-end specification, global chrome`
- [ ] `C-FE-42` `ui` The page-transition mask wipes away on arrival on the house curve. `src: Front-end specification, global chrome`
- [ ] `C-FE-43` `ui` The page-transition mask carries the same near-zero rounded corner the carousel frame rests at. `src: Front-end specification, global chrome`
- [ ] `C-FE-44` `ui` The page loader shows a percentage counting up beside the loading word, with a mark turning continuously counter-clockwise. `src: Front-end specification, global chrome`
- [ ] `C-FE-45` `constraint` The loader mark is the one keyframe loop in the product. `src: Front-end specification, global chrome`
- [ ] `C-FE-46` `ui` The consent panel is the product's own plain, accessible panel over a light backdrop blur. `src: Front-end specification, global chrome`
- [ ] `C-FE-47` `ui` Advancing the carousel translates the stack of cards through three-dimensional space, so cards tilt rather than slide flat. `src: Front-end specification, carousel engine`
- [ ] `C-FE-48` `ui` Each carousel card is a framed image with a caption, an index number, an eyebrow. `src: Front-end specification, carousel engine`
- [ ] `C-FE-49` `ui` The visible card's frame mask morphs between a tall portrait window, a wide landscape window, a slim band. `src: Front-end specification, carousel engine`
- [ ] `C-FE-50` `ui` The carousel frame rests at a rounded-rectangle corner whose softening is almost nothing. `src: Front-end specification, carousel engine`
- [ ] `C-FE-51` `ui` The content inside the frame counter-translates, so the image holds position as the window reshapes. `src: Front-end specification, carousel engine`
- [ ] `C-FE-52` `ui` Individual cards reveal with rectangular clip insets opening from a centred rectangle to fully open rather than with the morph. `src: Front-end specification, carousel engine`
- [ ] `C-FE-53` `ui` The inverse logo card opens from a zero-area polygon to the card's full rectangle. `src: Front-end specification, carousel engine`
- [ ] `C-FE-54` `ui` The carousel interface text uses the difference blend. `src: Front-end specification, carousel engine`
- [ ] `C-FE-55` `ui` The index places the wordmark top-left, the index control top-right, the framed card at the centre. `src: Front-end specification, route index`
- [ ] `C-FE-56` `ui` The index places the card's number bottom-left, the card's eyebrow bottom-centre, the arrows bottom-right. `src: Front-end specification, route index`
- [ ] `C-FE-57` `constraint` Five chapters are advertised on the index, two of which resolve. `src: Front-end specification, route index`
- [ ] `C-FE-58` `ui` The colour chapter sets the lead large across the page in the line cascade, each line rising on scroll. `src: Front-end specification, route colour`
- [ ] `C-FE-59` `ui` Each tone-group section is a full-bleed colour ground carrying the group's large word, a short definition. `src: Front-end specification, route colour`
- [ ] `C-FE-60` `ui` The page ground washes to the group's colour as each tone-group section arrives. `src: Front-end specification, route colour`
- [ ] `C-FE-61` `ui` Sticky poster stacks pin, revealing by clip as the stack's imagery cross-fades. `src: Front-end specification, route colour`
- [ ] `C-FE-62` `ui` A paginated thumbnail rail with arrow controls steps through the examples, stating the rail's position. `src: Front-end specification, route colour`
- [ ] `C-FE-63` `literal` The mocked posters carry the pinned trial title, the pinned storefront line, showing a demo template. `src: Front-end specification, route colour`
- [ ] `C-FE-64` `constraint` The mocked search field is the one place a pill-shaped field with elaborate corners appears. `src: Front-end specification, route colour`
- [ ] `C-FE-65` `literal` The colour chapter carries the pinned notes copy, primary copy, in-use copy, secondary copy, pull-quote copy. `src: Front-end specification, route colour copy table`
- [ ] `C-FE-66` `ui` The logo chapter opens on a white ground carrying the headline, the lead, a dark section immediately below. `src: Front-end specification, route logo`
- [ ] `C-FE-67` `ui` The logo chapter recolours the mark through the scroll-driven fill, the counter-fill, re-forming as the visitor scrolls. `src: Front-end specification, route logo`
- [ ] `C-FE-68` `ui` The logo chapter carries a construction section, a rules section, a lockups section, a paginated in-use gallery, a mark-in-motion block. `src: Front-end specification, route logo`
- [ ] `C-FE-69` `literal` The logo chapter carries the pinned design copy, systems copy, clear-space copy, secondary-colour copy, misuse copy. `src: Front-end specification, route logo copy table`
- [ ] `C-FE-70` `literal` The logo chapter carries the pinned lockups copy, partnership copy, presents copy, in-use copy. `src: Front-end specification, route logo copy table`
- [ ] `C-FE-71` `literal` The logo chapter's next-chapter affordance reads `Typography`. `src: Front-end specification, route logo copy table`
- [ ] `C-FE-72` `ui` The model surface is hosted under the global chrome. `src: Front-end specification, development surfaces`
- [ ] `C-FE-73` `ui` The endpoints surface is a single heading over the standard shell, exercising the content functions in isolation. `src: Front-end specification, development surfaces`
- [ ] `C-FE-74` `ui` The not-found body is the global chrome over a single centred line, with the ground at the ground's resting value. `src: Front-end specification, development surfaces`
- [ ] `C-FE-75` `capability` The line splitter splits a text block into lines, driving the cascade. `src: Front-end specification, modules`
- [ ] `C-FE-76` `constraint` The line splitter re-splits on resize. `src: Front-end specification, modules`
- [ ] `C-FE-77` `capability` The eyebrow module carries the parenthetical tag, the running number. `src: Front-end specification, modules`
- [ ] `C-FE-78` `capability` The arrow button module is the two-layer arrow control. `src: Front-end specification, modules`
- [ ] `C-FE-79` `capability` The poster stack module is the pinning, clipping gallery used by both chapters. `src: Front-end specification, modules`
- [ ] `C-FE-80` `capability` The video overlay module carries the mark-in-motion block, the poster sequences, dismissed by the close cross. `src: Front-end specification, modules`
- [ ] `C-FE-81` `capability` The colour driver maps scroll position to the animated properties, writing the properties to the document root. `src: Front-end specification, modules`
- [ ] `C-FE-82` `constraint` The colour driver lives at the top level, so colour behaves identically on every chapter. `src: Front-end specification, modules`
- [ ] `C-FE-83` `capability` The scroll service owns the smoothed position, the marker-derived progress, the single animation-frame callback. `src: Front-end specification, modules`
- [ ] `C-FE-84` `ui` The trial form carries one email field, one control on the closing poster. `src: Front-end specification, trial form`
- [ ] `C-FE-85` `constraint` A trial refusal names the field beside the field. `src: Front-end specification, trial form`
- [ ] `C-FE-86` `constraint` The trial control is the page's one primary action, with nothing competing. `src: Front-end specification, trial form`
- [ ] `C-FE-87` `constraint` Every pinned string is looked up by locale, by key rather than written into the markup. `src: Front-end specification, copy table`
- [ ] `C-FE-88` `literal` The five campaign names in the logo captions are `Maker Community`, `Built to Sell`, `Refresh 2025`, `Change Your World`, `Frontsite`. `src: Front-end specification, copy table`
- [ ] `C-FE-89` `literal` The studio credited in the colophon is `Northmark`. `src: Front-end specification, copy table`
- [ ] `C-FE-90` `constraint` The zero-asset rule gives every class of asset the product would load a substitution instead. `src: Front-end specification, generated imagery`
- [ ] `C-FE-91` `ui` Each generated picture honours the media row's ratio, tone, text alternative. `src: Front-end specification, generated imagery`
- [ ] `C-FE-92` `constraint` The carousel window shapes, the resting corner, the reveal insets, the transition corner are clip geometry over a bounding-box coordinate system. `src: Front-end specification, generated imagery`
- [ ] `C-FE-93` `constraint` One clip definition scales to every card size. `src: Front-end specification, generated imagery`
- [ ] `C-FE-94` `constraint` The tone-group grounds need no picture, being the interpolation written to the page ground. `src: Front-end specification, generated imagery`
- [ ] `C-FE-95` `ui` The mark-in-motion clip is a looped generated sequence of the mark re-forming through the mark's mask over a tone-group ground. `src: Front-end specification, generated imagery`
- [ ] `C-FE-96` `ui` An interface cue is synthesised at run time as a short enveloped tone with a fast decay, with no ambient bed. `src: Front-end specification, generated imagery`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The rendering model is a single-page application over a JSON interface, one shell, client-side routing, one chapter mounted at a time. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` Each chapter's content is fetched as JSON rather than delivered as a document per route. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The frontend is `Lit` with `Vite`, built to a production bundle of standard custom elements. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` The backend is `FastAPI`, serving the bundle for every address the router owns. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The backend serves the HTTP API on the same origin under the `/api` prefix. `src: Technical requirements para 1`
- [ ] `C-TR-06` `literal` The datastore is PostgreSQL at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-07` `literal` The object store is MinIO at `STORAGE_ENDPOINT`, `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-08` `literal` The public origin, port are `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. `src: Technical requirements para 1`
- [ ] `C-TR-09` `constraint` Every host, port, credential is read from the environment, never hardcoded. `src: Technical requirements para 1`
- [ ] `C-TR-10` `constraint` The app uses only the libraries named in the brief plus the libraries' direct dependencies. `src: Technical requirements para 2`
- [ ] `C-TR-11` `constraint` The app introduces no second database, cache, queue, object store, identity provider, mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-12` `literal` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements para 3`
- [ ] `C-TR-13` `contract` Logs are structured, one line of JSON per request on standard output. `src: Technical requirements para 4`
- [ ] `C-TR-14` `data` A log line carries the method, the route, the status, the elapsed milliseconds, a request identifier. `src: Technical requirements para 4`
- [ ] `C-TR-15` `constraint` The request identifier comes back in the body of every error response. `src: Technical requirements para 4`
- [ ] `C-TR-16` `constraint` No password, no token, no object key is written to a log. `src: Technical requirements para 4`
- [ ] `C-TR-17` `constraint` No credential, no key, no admin token appears in anything the browser downloads. `src: Technical requirements para 6`
- [ ] `C-TR-18` `constraint` The object store's credentials never leave the server. `src: Technical requirements para 6`
- [ ] `C-TR-19` `constraint` The product fetches nothing from outside the product's own origin at run time. `src: Technical requirements para 7`
- [ ] `C-TR-20` `constraint` No web font binary, analytics beacon, consent vendor, content host, asset host is fetched. `src: Technical requirements para 7`
- [ ] `C-TR-21` `constraint` One animation-frame callback drives the scroll timelines, the colour driver. `src: Technical requirements para 8`
- [ ] `C-TR-22` `constraint` The three-dimensional frame loop halts when the loop's surface is off-screen. `src: Technical requirements para 8`
- [ ] `C-TR-23` `constraint` Text is split once per layout, re-split only on resize. `src: Technical requirements para 8`
- [ ] `C-TR-24` `literal` Compositor hints are capped at fewer than `120` elements in total. `src: Technical requirements para 8`
- [ ] `C-TR-25` `constraint` Compositor hints are applied only to elements currently animating. `src: Technical requirements para 8`
- [ ] `C-TR-26` `constraint` The first content paints before the loader hands over, with nothing shifting position afterwards. `src: Technical requirements para 8`
- [ ] `C-TR-27` `literal` The frame budget during a scrolling chapter, a visible model surface, is a sustained `60fps` rather than an average. `src: Technical requirements para 8`
- [ ] `C-TR-28` `constraint` Loading order runs the loader, the first chapter's shell, then that chapter's content, then the model surface. `src: Technical requirements para 8`
- [ ] `C-TR-29` `capability` The copy layer is addressed by locale, by key rather than written into markup. `src: Technical requirements para 9`
- [ ] `C-TR-30` `constraint` One locale ships. `src: Technical requirements para 9`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema carries nine tables. `src: Data model para 1`
- [ ] `C-DM-02` `constraint` The app records every stored timestamp in coordinated universal time. `src: Data model para 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-04` `constraint` The seeded password is hashed as normal, with the exact literal working at login. `src: Data model, password paragraph`
- [ ] `C-DM-05` `literal` The seeded password is written into `/app/USER_README.md` alongside each account. `src: Data model, password paragraph`
- [ ] `C-DM-06` `data` The `account` table holds an id, an email unique, compared case-insensitively, a display name, a password hash, a role, a creation moment. `src: Data model, identity paragraph`
- [ ] `C-DM-07` `literal` The account table's role column is one of `author`, `reader`. `src: Data model, identity paragraph`
- [ ] `C-DM-08` `data` The `session` table holds an id, an account id, a token hash, an expiry, a creation moment. `src: Data model, identity paragraph`
- [ ] `C-DM-09` `data` The `chapter` table holds an id, a unique slug, an index label, an eyebrow, a title, a lead, a published flag, a publication moment, an owning author, a creation moment. `src: Data model, content paragraph`
- [ ] `C-DM-10` `literal` The chapter slug is one of `color`, `logo`, `typography`, `photography`, `motion`. `src: Data model, content paragraph`
- [ ] `C-DM-11` `constraint` Chapters are ordered by index label. `src: Data model, content paragraph`
- [ ] `C-DM-12` `data` The `section` table holds an id, a chapter id, a position, a kind, an eyebrow, an index label, a heading, a body. `src: Data model, content paragraph`
- [ ] `C-DM-13` `literal` A section kind is one of `intro`, `tone-group`, `poster-stack`, `rules`, `in-use`, `cta`. `src: Data model, content paragraph`
- [ ] `C-DM-14` `constraint` A section is unique on the chapter id together with the position. `src: Data model, content paragraph`
- [ ] `C-DM-15` `data` The `tone_stop` table holds an id, a section id, a group name, a tier, a ground, an ink, a position. `src: Data model, content paragraph`
- [ ] `C-DM-16` `literal` A tone stop tier is one of `desktop`, `tablet`, `mobile`. `src: Data model, content paragraph`
- [ ] `C-DM-17` `constraint` One tone stop row exists per group per tier. `src: Data model, content paragraph`
- [ ] `C-DM-18` `data` The `caption` table holds an id, a section id, a position, a text. `src: Data model, content paragraph`
- [ ] `C-DM-19` `data` The `copy_entry` table holds an id, a locale, a key, a value, unique on locale together with key. `src: Data model, content paragraph`
- [ ] `C-DM-20` `data` The `media_ref` table holds an id, a section id, a unique media key, a ratio, a tone, an alternative text, a unique object key, a byte size, a digest, a generation moment. `src: Data model, media paragraph`
- [ ] `C-DM-21` `data` The `trial_signup` table holds an id, a unique email, a source chapter id, a creation moment. `src: Data model, the one write paragraph`
- [ ] `C-DM-22` `constraint` A chapter's public readability is derived from the published flag alone, so no second flag can disagree. `src: Data model, derived paragraph`
- [ ] `C-DM-23` `constraint` The index advertises every chapter, resolving the published subset. `src: Data model, derived paragraph`
- [ ] `C-DM-24` `constraint` The ground behind imagery is derived from the page ground. `src: Data model, derived paragraph`
- [ ] `C-DM-25` `constraint` A tone stop's ink is chosen so the pair clears the pair's contrast floor. `src: Data model, derived paragraph`
- [ ] `C-DM-26` `constraint` The crossover between the two inks is derived from the interpolation rather than stored per section. `src: Data model, derived paragraph`
- [ ] `C-DM-27` `constraint` The digest in a media object's key is the digest of the bytes themselves. `src: Data model, derived paragraph`
- [ ] `C-DM-28` `constraint` A chapter whose published flag is false is served by no public route, appearing in no sitemap. `src: Data model, invariants paragraph`
- [ ] `C-DM-29` `constraint` A media row's object exists at the row's object key. `src: Data model, invariants paragraph`
- [ ] `C-DM-30` `constraint` Section positions are contiguous from one within a chapter after any reorder. `src: Data model, invariants paragraph`
- [ ] `C-DM-31` `constraint` One trial signup exists per address. `src: Data model, invariants paragraph`
- [ ] `C-DM-32` `constraint` Every string the product displays resolves to a copy entry for the active locale. `src: Data model, invariants paragraph`
- [ ] `C-DM-33` `literal` The app seeds `color` at index `01`, published, owned by `author@example.com`. `src: Data model, seed data`
- [ ] `C-DM-34` `literal` The app seeds `logo` at index `02`, published, owned by `author@example.com`. `src: Data model, seed data`
- [ ] `C-DM-35` `literal` The app seeds `typography` at index `03`, unpublished, owned by `author@example.com`. `src: Data model, seed data`
- [ ] `C-DM-36` `literal` The app seeds `photography` at index `04`, unpublished, owned by `author@example.com`. `src: Data model, seed data`
- [ ] `C-DM-37` `literal` The app seeds `motion` at index `05`, unpublished, owned by `author2@example.com`. `src: Data model, seed data`
- [ ] `C-DM-38` `data` The colour chapter seeds an intro section, four tone-group sections, two poster-stack sections, a rules section, a closing call-to-action section. `src: Data model, seed data`
- [ ] `C-DM-39` `data` The logo chapter seeds an intro, a mark section, a rules section, an in-use section, a closing call-to-action section. `src: Data model, seed data`
- [ ] `C-DM-40` `data` The app seeds twelve tone stop rows, one per group per tier. `src: Data model, seed data`
- [ ] `C-DM-41` `literal` The colour chapter seeds nine captions, the first reading `Primary, Product UI`. `src: Data model, seed data`
- [ ] `C-DM-42` `literal` The logo chapter seeds seven captions, the first reading `Logo, Maker Community, Campaign`. `src: Data model, seed data`
- [ ] `C-DM-43` `literal` Three demo template names appear in the mocks, `Meridian`, `Kiln`, `Atelier`. `src: Data model, seed data`
- [ ] `C-DM-44` `literal` One trial signup is seeded on `hollis@example.com`. `src: Data model, seed data`
- [ ] `C-DM-45` `constraint` Seeding is idempotent, so restarting the app duplicates no rows. `src: Data model, closing line`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product is one brand on one origin shipping one locale. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` No second origin serves assets, content, signup. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` No photograph in any image format ships or is fetched. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` No video file, no audio file ships or is fetched. `src: Constraints bullet 2`
- [ ] `C-CN-05` `constraint` No font binary ships or is fetched. `src: Constraints bullet 2`
- [ ] `C-CN-06` `constraint` No three-dimensional model file, no compressed geometry ships or is fetched. `src: Constraints bullet 2`
- [ ] `C-CN-07` `constraint` No vector-animation document, no compiled runtime for one ships or is fetched. `src: Constraints bullet 2`
- [ ] `C-CN-08` `constraint` Every picture, every clip, every cue is generated by the product. `src: Constraints bullet 2`
- [ ] `C-CN-09` `constraint` No third-party analytics, consent vendor, content host, asset host, measurement identifier is used. `src: Constraints bullet 3`
- [ ] `C-CN-10` `constraint` Nothing leaves the origin at run time, so no page-view beacon exists. `src: Constraints bullet 3`
- [ ] `C-CN-11` `constraint` No external script is loaded. `src: Constraints bullet 3`
- [ ] `C-CN-12` `constraint` No payment, no card detail is handled, so the trial is free. `src: Constraints bullet 4`
- [ ] `C-CN-13` `constraint` No comments, likes, sharing, social graph, chat, newsletter, cross-chapter search exist. `src: Constraints bullet 5`
- [ ] `C-CN-14` `constraint` No email is sent by the app, with no mail server available. `src: Constraints bullet 6`
- [ ] `C-CN-15` `constraint` No native application, no offline mode exists. `src: Constraints bullet 7`
- [ ] `C-CN-16` `constraint` No keyframe loop exists beyond the loader's turning mark. `src: Constraints bullet 8`
- [ ] `C-CN-17` `constraint` The model, the loader flourish, the audio cues are reconstructions expected to be close rather than exact. `src: Constraints bullet 9`
- [ ] `C-CN-18` `literal` The app stays responsive with `5` chapters, `40` sections, `120` media rows, `5000` trial signups. `src: Constraints bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` Reserved `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The app serves a production build behind a static server, a preview server, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends, never a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The server binds `0.0.0.0`, never `127.0.0.1`, never `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `contract` The backing services named in the brief are already running, so none is downloaded, installed, compiled, started. `src: Deployment contract bullet 10`
- [ ] `C-DC-13` `contract` The app uses only the providers named in the brief, with no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-14` `contract` The app declares no persistent volumes, no fixed container names, no custom networks. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `literal` `POST /api/auth/sign-up` accepts `email`, `password`, `display_name`, returning the account with a bearer token. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `literal` `POST /api/auth/sign-in` accepts `email`, `password`, returning a bearer token with an expiry. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `literal` `POST /api/auth/sign-out` invalidates the caller's token. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `literal` `GET /api/chapters` returns a top-level JSON array of every chapter. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `data` Each chapter row carries a slug, an index label, an eyebrow, a title, a published flag. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `literal` `GET /api/chapters/<slug>` returns the chapter with ordered sections for an entitled caller. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `literal` `GET /api/chapters/<slug>/sections` returns a top-level JSON array of sections in position order. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `literal` `POST /api/chapters` creates an unpublished chapter owned by the caller. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `literal` `POST /api/chapters/<slug>/sections` creates a section at the end of the order. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `literal` `PUT /api/chapters/<slug>/order` accepts an `order` list, returning sections with positions contiguous from one. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `literal` `POST /api/chapters/<slug>/publish` publishes the chapter, recording the moment. `src: Deployment contract, API shapes`
- [ ] `C-DC-26` `literal` `POST /api/chapters/<slug>/unpublish` unpublishes the chapter. `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `literal` `POST /api/sections/<id>/media` returns the media row with an object key, a digest, writing the bytes to the object store. `src: Deployment contract, API shapes`
- [ ] `C-DC-28` `literal` `GET /api/media/<media_key>/content` streams the stored object for an entitled caller only. `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `literal` `GET /api/copy` accepts a `locale`, returning the keyed copy entries. `src: Deployment contract, API shapes`
- [ ] `C-DC-30` `literal` `POST /api/trials` accepts `email`, `source_chapter_slug`, producing exactly one signup per address. `src: Deployment contract, API shapes`
- [ ] `C-DC-31` `literal` `GET /api/trials` returns a top-level JSON array of signups for an author only. `src: Deployment contract, API shapes`
- [ ] `C-DC-32` `constraint` Bearer auth is required on everything except sign-up, sign-in, health, the public chapter reads, the copy read, the trial submission. `src: Deployment contract, auth paragraph`
- [ ] `C-DC-33` `constraint` An invalid call is rejected as a client error, never a server error, never a silent success. `src: Deployment contract, auth paragraph`
- [ ] `C-DC-34` `constraint` An unauthorized call is rejected as a client error, never a server error, never a silent success. `src: Deployment contract, auth paragraph`
- [ ] `C-DC-35` `constraint` Image bytes on the app container's filesystem are a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-36` `constraint` A base64 column in PostgreSQL holding an image is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-37` `constraint` A picture the browser redraws on every request instead of a stored object is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-38` `constraint` A self-answered stored acknowledgement is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-39` `constraint` Chapters held in a process rather than in PostgreSQL are a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-40` `constraint` MinIO, PostgreSQL are the fact, so the app's own screens reflect what lives in them rather than substituting for them. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Source |
|---|---|---|---|
| `author@example.com` | seeded author account | C-RL-25 | User roles, seeded accounts paragraph |
| `author2@example.com` | second seeded author account | C-RL-27 | User roles, seeded accounts paragraph |
| `reader@example.com` | seeded reader account | C-RL-29 | User roles, seeded accounts paragraph |
| `hollis@example.com` | the seeded trial address | C-DM-44 | Data model, seed data |
| `deku-demo-pw-2026` | the password on every seeded account | C-DM-03 | Data model, password paragraph |
| `/app/USER_README.md` | credential file path | C-DM-05 | Data model, password paragraph |
| `/` | the index carousel route | C-UF-01 | User flow route table |
| `/color` | the colour chapter route | C-UF-02 | User flow route table |
| `/logo` | the logo chapter route | C-UF-03 | User flow route table |
| `/typography` | an unpublished chapter route | C-UF-04 | User flow route table |
| `/photography` | an unpublished chapter route | C-UF-05 | User flow route table |
| `/motion` | an unpublished chapter route | C-UF-06 | User flow route table |
| `/menu` | the full-screen menu route | C-UF-07 | User flow route table |
| `/webgl` | the model surface route | C-UF-08 | User flow route table |
| `/lambda` | the endpoints surface route | C-UF-09 | User flow route table |
| `/signup` | the account creation route | C-UF-10 | User flow route table |
| `/login` | the sign-in route | C-UF-11 | User flow route table |
| `/logout` | the sign-out route | C-UF-12 | User flow route table |
| `/studio` | the author's chapter list route | C-UF-13 | User flow route table |
| `/studio/chapters/new/details` | wizard step one | C-UF-14 | User flow route table |
| `/studio/chapters/new/sections` | wizard step two | C-UF-15 | User flow route table |
| `/studio/chapters/new/media` | wizard step three | C-UF-16 | User flow route table |
| `/studio/chapters/new/review` | wizard step four | C-UF-17 | User flow route table |
| `/studio/chapters/<slug>` | one chapter's section order route | C-UF-18 | User flow route table |
| `/studio/trials` | the trial list route | C-UF-19 | User flow route table |
| `/sitemap.xml` | the sitemap route | C-UF-20 | User flow route table |
| `/robots.txt` | the robots route | C-UF-21 | User flow route table |
| `/favicon.ico` | the favicon route | C-UF-22 | User flow route table |
| `GET /api/health` | the readiness route | C-UF-23 | User flow route table |
| `200` | the readiness status | C-TR-12 | Technical requirements para 3 |
| `/api` | the API prefix | C-TR-05 | Technical requirements para 1 |
| `DATABASE_URL` | database connection variable | C-TR-06 | Technical requirements para 1 |
| `STORAGE_ENDPOINT` | object store address variable | C-CF-121 | Technical requirements para 1 |
| `STORAGE_BUCKET` | object store bucket variable | C-CF-121 | Technical requirements para 1 |
| `STORAGE_ACCESS_KEY` | object store key variable | C-CF-122 | Core features, imagery rule 1 |
| `STORAGE_SECRET_KEY` | object store secret variable | C-CF-122 | Core features, imagery rule 1 |
| `APP_PUBLIC_URL` | public address variable | C-TR-08 | Technical requirements para 1 |
| `APP_PUBLIC_PORT` | public port variable | C-TR-08 | Technical requirements para 1 |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | C-DC-02 | Deployment contract bullet 1 |
| `4173` | container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `0.0.0.0` | the bind address | C-DC-11 | Deployment contract bullet 9 |
| `127.0.0.1` | the forbidden loopback bind | C-DC-11 | Deployment contract bullet 9 |
| `localhost` | the forbidden loopback name | C-DC-11 | Deployment contract bullet 9 |
| `.browser_screenshots/` | reserved screenshot directory | C-DC-07 | Deployment contract bullet 6 |
| `.downloads/` | reserved download directory | C-DC-08 | Deployment contract bullet 6 |
| `Lit` | the frontend library | C-TR-03 | Technical requirements para 1 |
| `Vite` | the frontend build tool | C-TR-03 | Technical requirements para 1 |
| `FastAPI` | the backend framework | C-TR-04 | Technical requirements para 1 |
| `color` | the colour chapter slug | C-CF-13 | Data model, content paragraph |
| `logo` | the logo chapter slug | C-CF-13 | Data model, content paragraph |
| `typography` | an unpublished chapter slug | C-CF-14 | Data model, content paragraph |
| `photography` | an unpublished chapter slug | C-CF-14 | Data model, content paragraph |
| `motion` | an unpublished chapter slug | C-CF-14 | Data model, content paragraph |
| `01` | the colour chapter index label | C-CF-11 | Core features, chapter set rule 1 |
| `02` | the logo chapter index label | C-CF-11 | Core features, chapter set rule 1 |
| `03` | the typography chapter index label | C-CF-11 | Core features, chapter set rule 1 |
| `04` | the photography chapter index label | C-CF-11 | Core features, chapter set rule 1 |
| `05` | the motion chapter index label | C-CF-11 | Core features, chapter set rule 1 |
| `author` | the author role value | C-DM-07 | Data model, identity paragraph |
| `reader` | the reader role value | C-DM-07 | Data model, identity paragraph |
| `intro` | a section kind | C-DM-13 | Data model, content paragraph |
| `tone-group` | a section kind | C-DM-13 | Data model, content paragraph |
| `poster-stack` | a section kind | C-DM-13 | Data model, content paragraph |
| `rules` | a section kind | C-DM-13 | Data model, content paragraph |
| `in-use` | a section kind | C-DM-13 | Data model, content paragraph |
| `cta` | a section kind | C-DM-13 | Data model, content paragraph |
| `desktop` | a tone stop tier | C-DM-16 | Data model, content paragraph |
| `tablet` | a tone stop tier | C-DM-16 | Data model, content paragraph |
| `mobile` | a tone stop tier | C-DM-16 | Data model, content paragraph |
| `Core` | the first tone group | C-CF-45 | Core features, colour system rule 3 |
| `Dark` | the second tone group | C-CF-45 | Core features, colour system rule 3 |
| `Bright` | the third tone group | C-CF-45 | Core features, colour system rule 3 |
| `Light` | the fourth tone group | C-CF-45 | Core features, colour system rule 3 |
| `idle` | the trial form's resting state | C-CF-141 | Core features, trial rule 2 |
| `success` | the trial form's accepted state | C-CF-141 | Core features, trial rule 2 |
| `failure` | the trial form's refused state | C-CF-141 | Core features, trial rule 2 |
| `media/{chapter_slug}/{media_key}/{sha256_of_bytes}.png` | the object key scheme | C-CF-125 | Core features, imagery rule 2 |
| `core-poster-01` | the worked example's media key | C-CF-126 | Core features, imagery rule 2 |
| `Latticework Foundations` | the wordmark | C-CF-165 | Core features, chrome rule 1 |
| `Index` | the index control label | C-CF-166 | Core features, chrome rule 1 |
| `Loading` | the loader label | C-CF-174 | Core features, chrome rule 4 |
| `100%` | the loader's full figure | C-CF-174 | Core features, chrome rule 4 |
| `Tap to Explore` | the carousel invitation | C-CF-01 | Core features, index carousel rule 5 |
| `A website makes it real` | the trial title | C-FE-01 | Front-end specification, route colour |
| `Get your free website trial today. No credit card required.` | the trial body | C-CF-01 | Core features, trial rule 1 |
| `Thank you. You are on the list.` | the trial success copy | C-CF-01 | Core features, trial rule 3 |
| `Something went wrong, please try again.` | the trial failure copy | C-CF-01 | Core features, trial rule 4 |
| `404: Page not found` | the not-found line | C-CF-180 | Core features, chrome rule 6 |
| `Latticework` | the first index display word | C-CF-104 | Core features, index carousel rule 4 |
| `Foundations` | the second index display word | C-CF-165 | Core features, index carousel rule 4 |
| `Discover the essential guiding principles and distinctive visual elements that define the Latticework identity.` | the index lead line | C-CF-01 | Core features, index carousel rule 4 |
| `( Color )` | the colour card eyebrow | C-CF-34 | Core features, index carousel rule 2 |
| `( Logo )` | the logo card eyebrow | C-CF-34 | Core features, index carousel rule 2 |
| `( Typography )` | the typography card eyebrow | C-CF-34 | Core features, index carousel rule 2 |
| `( Photography )` | the photography card eyebrow | C-CF-34 | Core features, index carousel rule 2 |
| `( Motion )` | the motion card eyebrow | C-CF-34 | Core features, index carousel rule 2 |
| `Color` | the colour chapter headline | C-CF-76 | Core features, colour chapter rule 1 |
| `Our color approach prioritizes elegance, restraint, and timelessness. The palette is intentionally neutral so that, like a gallery, it serves as a blank slate, creating a visual language that enhances our content rather than competes with it.` | the colour chapter lead | C-CF-01 | Core features, colour chapter rule 1 |
| `Our Core tones are designed to support our brand imagery style, never blending into the background or creating too harsh a contrast.` | the Core definition | C-CF-01 | Core features, colour chapter rule 2 |
| `Used as a background color in place of true black, our Dark tones work best when displaying multiple image styles, functional designs, or text-heavy content.` | the Dark definition | C-CF-01 | Core features, colour chapter rule 2 |
| `Our Bright tones are saturated yet sophisticated, ideally suited as an accent color or across social media.` | the Bright definition | C-CF-01 | Core features, colour chapter rule 2 |
| `Used when in need of an off-white background color, our Light tones pair best with UI or content-heavy designs.` | the Light definition | C-CF-01 | Core features, colour chapter rule 2 |
| `01 / 07` | the longer thumbnail rail position | C-CF-86 | Core features, colour chapter rule 4 |
| `01 / 04` | the shorter thumbnail rail position | C-CF-87 | Core features, colour chapter rule 4 |
| `HEX` | the swatch label | C-CF-88 | Core features, colour chapter rule 5 |
| `Shuffle Color` | the shuffle control label | C-CF-01 | Core features, colour system rule 8 |
| `Explore Colors` | the colour explore affordance | C-CF-91 | Core features, colour chapter rule 6 |
| `Photography` | the colour chapter's next-chapter affordance | C-CF-92 | Core features, colour chapter rule 6 |
| `Made with Latticework` | the storefront mock copy | C-FE-01 | Front-end specification, route colour |
| `Logo` | the logo chapter headline | C-CF-94 | Core features, logo chapter rule 1 |
| `Latticework's logo captures a core conviction: that designing a beautiful website should be elegantly simple. Wherever the logo appears, it immediately signals our brand ethos, clarity over clutter, and impact over noise.` | the logo chapter lead | C-CF-01 | Core features, logo chapter rule 1 |
| `X` | the partnership lockup cross | C-CF-102 | Core features, logo chapter rule 4 |
| `Latticework Presents` | the presents lockup | C-CF-104 | Core features, logo chapter rule 4 |
| `Typography` | the logo chapter's next-chapter affordance | C-FE-71 | Front-end specification, route logo copy table |
| `Lambda Endpoints Test` | the endpoints surface heading | C-CF-01 | Core features, author surface rule 5 |
| `The goal is to ensure harmony with the overall design.` | the colour notes copy | C-FE-01 | Front-end specification, route colour copy table |
| `Our color palette is grounded in four tonal groups: core, dark, bright, and light, with the core tones serving as our foundation. To maintain visual consistency, our essential brand elements, typography, logo, and icons, appear in black and white whenever possible.` | the colour primary copy | C-FE-01 | Front-end specification, route colour copy table |
| `Beyond the four groups of our color palette, one or two additional tones are often introduced as accents to provide contrast and depth.` | the colour secondary copy | C-FE-01 | Front-end specification, route colour copy table |
| `Image directs color palette` | the notes image copy | C-FE-01 | Front-end specification, route colour copy table |
| `From playful to experimental solutions` | the colour pull quote | C-FE-01 | Front-end specification, route colour copy table |
| `Designed for clarity, impact, and hierarchy.` | the logo notes copy | C-FE-01 | Front-end specification, route logo copy table |
| `Two essential elements define the logo. The symbol, an abstracted monogram of two interlocking S's, creates a distinctive emblem, while the wordmark is set in Grotesk Display, the bespoke typeface crafted for our brand.` | the logo design copy | C-FE-01 | Front-end specification, route logo copy table |
| `For maximum visibility and impact, the logo is surrounded by a designated clear space to prevent other elements from competing with or crowding it.` | the clear space copy | C-FE-01 | Front-end specification, route logo copy table |
| `To preserve clarity and impact, the logo is never shown warped, distorted, or oriented at an angle.` | the misuse copy | C-FE-01 | Front-end specification, route logo copy table |
| `Grotesk Display` | the display family | C-UX-21 | UI/UX notes para 4 |
| `Grotesk Serif` | the editorial serif family | C-UX-22 | UI/UX notes para 4 |
| `Grotesk Condensed` | the condensed poster family | C-UX-23 | UI/UX notes para 4 |
| `Maker Community` | a logo caption campaign name | C-FE-88 | Front-end specification, copy table |
| `Built to Sell` | a logo caption campaign name | C-FE-88 | Front-end specification, copy table |
| `Refresh 2025` | a logo caption campaign name | C-FE-88 | Front-end specification, copy table |
| `Change Your World` | a logo caption campaign name | C-FE-88 | Front-end specification, copy table |
| `Frontsite` | a logo caption campaign name | C-FE-88 | Front-end specification, copy table |
| `Northmark` | the studio in the colophon | C-FE-89 | Front-end specification, copy table |
| `Primary, Product UI` | the first colour caption | C-DM-41 | Data model, seed data |
| `Logo, Maker Community, Campaign` | the first logo caption | C-DM-42 | Data model, seed data |
| `Meridian` | a demo template name | C-DM-43 | Data model, seed data |
| `Kiln` | a demo template name | C-DM-43 | Data model, seed data |
| `Atelier` | a demo template name | C-DM-43 | Data model, seed data |
| `4.5:1` | the body-text contrast floor | C-UX-80 | UI/UX notes para 10 |
| `3:1` | the large-text contrast floor | C-UX-81 | UI/UX notes para 10 |
| `120` | the compositor-hint cap | C-TR-24 | Technical requirements para 8 |
| `60fps` | the sustained frame budget | C-TR-27 | Technical requirements para 8 |
| `5` | the seeded chapter count | C-CN-18 | Constraints bullet 10 |
| `40` | the section volume | C-CN-18 | Constraints bullet 10 |
| `5000` | the trial signup volume | C-CN-18 | Constraints bullet 10 |
| `POST /api/auth/sign-up` | a graded endpoint | C-DC-15 | Deployment contract, API shapes |
| `POST /api/auth/sign-in` | a graded endpoint | C-DC-16 | Deployment contract, API shapes |
| `POST /api/auth/sign-out` | a graded endpoint | C-DC-17 | Deployment contract, API shapes |
| `GET /api/chapters` | a graded endpoint | C-DC-18 | Deployment contract, API shapes |
| `GET /api/chapters/<slug>` | a graded endpoint | C-DC-20 | Deployment contract, API shapes |
| `GET /api/chapters/<slug>/sections` | a graded endpoint | C-DC-21 | Deployment contract, API shapes |
| `POST /api/chapters` | a graded endpoint | C-DC-22 | Deployment contract, API shapes |
| `POST /api/chapters/<slug>/sections` | a graded endpoint | C-DC-23 | Deployment contract, API shapes |
| `PUT /api/chapters/<slug>/order` | a graded endpoint | C-DC-24 | Deployment contract, API shapes |
| `POST /api/chapters/<slug>/publish` | a graded endpoint | C-DC-25 | Deployment contract, API shapes |
| `POST /api/chapters/<slug>/unpublish` | a graded endpoint | C-DC-26 | Deployment contract, API shapes |
| `POST /api/sections/<id>/media` | a graded endpoint | C-DC-27 | Deployment contract, API shapes |
| `GET /api/media/<media_key>/content` | a graded endpoint | C-DC-28 | Deployment contract, API shapes |
| `GET /api/copy` | a graded endpoint | C-DC-29 | Deployment contract, API shapes |
| `POST /api/trials` | a graded endpoint | C-DC-30 | Deployment contract, API shapes |
| `GET /api/trials` | a graded endpoint | C-DC-31 | Deployment contract, API shapes |
| `email` | the trial request field | C-DC-15 | Deployment contract, API shapes |
| `password` | the sign-in request field | C-DC-15 | Deployment contract, API shapes |
| `display_name` | the sign-up request field | C-DC-15 | Deployment contract, API shapes |
| `source_chapter_slug` | the trial request field naming the chapter | C-DC-30 | Deployment contract, API shapes |
| `order` | the reorder request field | C-DC-24 | Deployment contract, API shapes |
| `locale` | the copy request field | C-DC-29 | Deployment contract, API shapes |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the chapter slug inside a generated object key | C-CF-125 | named by scheme, with the five slugs pinned separately in the Data model |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 4 | 22 |
| User roles | 1 | 29 |
| Core features | 12 | 189 |
| User flow | 6 | 51 |
| UI and UX notes | 3 | 99 |
| Front-end specification | 7 | 96 |
| Technical requirements | 6 | 30 |
| Data model | 3 | 45 |
| Constraints | 1 | 18 |
| Deployment contract | 11 | 40 |
