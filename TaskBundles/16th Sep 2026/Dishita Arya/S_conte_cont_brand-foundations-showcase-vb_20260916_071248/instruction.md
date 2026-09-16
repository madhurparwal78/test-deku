# Latticework Foundations

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, page through the index carousel, open the colour chapter, scroll it while the whole page repaints continuously through its four tone groups, and start a free website trial from the poster that closes it, without hitting an error page. Two things in that sentence cannot be arranged inside the app's own screens. Every image the product shows must exist as a real object in MinIO at the key scheme pinned below: bytes on the app's own disk, a column in PostgreSQL holding an image, or a picture the browser redraws on every request are each a contract violation however good the page looks. And a chapter that is not published must not be readable by a signed-out visitor, by a reader, or by another author, at its own address or at any other, and its generated image must not be fetchable from the object store by anyone who is not its author.

## Overview

Latticework Foundations is a public brand-foundations site for a website builder: an online brand book. It presents the visual system as a sequence of full-screen editorial chapters, each one a short essay wrapped around one foundational idea, with motion and colour doing most of the persuading. Three audiences read it. Designers and brand teams came for the rules: the tone groups, the logo lockups, the clear space, the typography. Partners and press came for a quotable statement of the brand. Prospective customers came for the trial, and they reach it at the end of a chapter rather than at the top of a page.

It is not an application a visitor logs into. A visitor's only state-changing action is starting a free website trial from a chapter's closing poster. Behind the public surface there is an author, who writes chapters, orders their sections, generates their imagery and publishes them, and an unpublished chapter is not a public chapter.

The character is restrained, gallery-like and confident. It is near-monochrome almost all of the time, and colour is introduced only where the content is about colour. Type is large and quiet, motion is slow and continuous, and nothing blinks or demands. The product's own words for its palette state the intent: it prioritises elegance, restraint, and timelessness, and is intentionally neutral so that, like a gallery, it serves as a blank slate.

What it deliberately is not. No comments, no likes, no sharing, no social graph, no chat, no newsletter. No search across chapters. No payment of any kind: the trial is free and takes no card. No second brand and no multi-tenancy. No third-party analytics, consent vendor, content host or asset host. No native application. And no binary asset of any kind ships with the build: no photograph, no video file, no font binary, no three-dimensional model file, no audio file and no vector-animation document.

The genuinely hard part is that the colour is not decoration, it is the chapter. The page ground, the text colour, the media ground and the logo fill are driven directly from scroll position and must interpolate continuously between stops, reverse with scroll direction, and keep text readable at every point between two stops rather than only at the stops themselves. A build that plays the chapter on an intersection trigger, or that switches colour at a section boundary, has built a different product.

Every statement in this brief is normative: it is what the finished product must do, and each one is an acceptance condition somebody can settle by looking at the running site. Nothing here is informational commentary about how anything was once built. Where a capability is named rather than a library, any implementation that delivers the capability satisfies it.

Four parts of this specification are honest evidence gaps rather than records, because they could not be measured, and their classification matters because it tells you what to aim at: the three-dimensional model's own geometry and its turn, the drawn flourish behind the loader, the interface audio cues, and the hover craft. Each is carried here as a procedural substitution that has to do the same job rather than as a shape to match, and each should be expected to need a round of adjustment.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (signed out) | Read the index carousel, every published chapter, the full-screen menu, the model surface and the not-found body; submit a free trial | **Read any unpublished chapter at any address, read an unpublished chapter's image, reach the author surface or the endpoints-test surface, or write anything except a trial** |
| Reader | Everything a visitor can do, signed in | **Read any unpublished chapter at any address, read an unpublished chapter's image, reach the author surface or the endpoints-test surface, or publish anything** |
| Author | Everything a reader can do, plus write, reorder, generate imagery for and publish their **own** chapters, read their own drafts and their drafts' imagery, read the trial list, and reach the endpoints-test surface | **Read, edit or publish another author's chapter, its sections or its imagery** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Reader session to any Author-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The role is read from the signed-in account's own record and never from a request body, a query parameter or a header the caller controls.

Signup is open. Anyone may create an account, and an account created through signup is a Reader; the Author role is not self-assignable.

Three accounts are seeded, every one of them on the password named in `## Data model`. `author@example.com` is Wren Calloway, an Author, who owns the `color`, `logo`, `typography` and `photography` chapters. `author2@example.com` is Osian Petrie, an Author, who owns the `motion` chapter. `reader@example.com` is Marit Sandoval, a Reader.

## Core features

### Auth

Email and password are exchanged for a bearer token. Passwords are stored under a modern memory-hard password hash and never in any recoverable form. The client sends the token as a bearer credential on every API call. Tokens expire, and an expired token returns the caller to the sign-in route with the pending work unwritten.

1. Signing in with a wrong password is refused, and the refusal does not say which of the two was wrong.
2. Signing out invalidates the token; a request replaying that token afterwards is denied.
3. An account created through signup is a Reader. A request that asks for the Author role at signup is refused as invalid and creates nothing.

### The chapter set and what publication means

This is the rule the whole product rests on.

1. Five chapters exist, in this running order: `01` Color, `02` Logo, `03` Typography, `04` Photography, `05` Motion. Each carries a slug, a running index label, a parenthetical eyebrow, a display title, a lead and an ordered set of sections.
2. `color` and `logo` are published. `typography`, `photography` and `motion` are not.
3. **The index advertises all five by name and resolves only the published ones.** Choosing an unpublished card does not navigate; the card states that the chapter is not yet published.
4. **An unpublished chapter is not readable by a signed-out visitor and not readable by a Reader**, at its own address, through the chapter endpoint, through its sections endpoint, or through any list. It appears in no sitemap.
5. An unpublished chapter is readable by its own author and by nobody else. `author@example.com` asking for `motion`, which belongs to `author2@example.com`, is denied exactly as a signed-out visitor is.
6. Publishing makes the chapter readable at its slug, records the moment, and adds it to the sitemap. Unpublishing reverses all three.
7. Publishing a chapter with no sections is refused as invalid and changes nothing.

### The index carousel

1. The index does not scroll the document. The carousel advances in place.
2. Each card carries its chapter's index label, its parenthetical eyebrow (`( Color )`, `( Logo )`, `( Typography )`, `( Photography )`, `( Motion )`) and a framed image whose window morphs between shapes as the card moves.
3. The carousel advances on the previous and next arrow controls, on drag, and on the left and right arrow keys, and all three reach the same card.
4. On first entry the display words `Latticework` and `Foundations` and the lead line `Discover the essential guiding principles and distinctive visual elements that define the Latticework identity.` introduce the carousel before the cards take over.
5. A `Tap to Explore` label invites entry into the card in view.

### The scroll-driven colour system

The signature surface, and the one thing a build is most likely to get almost right.

1. On an editorial chapter the page ground, the ink, a section-local ground, its matching section-local ink and the media ground are all driven from scroll position and are resolved once at the document root, so every component reads the same values.
2. The media ground is **derived, not independent**: it is a lightness-shifted twin that tracks the page ground two points lighter, so imagery never sits on exactly the page ground.
3. The colour chapter moves the ground through four tone groups in this order: `Core`, `Dark`, `Bright`, `Light`, ending on white.
4. **The stops differ by tier.** The desktop, tablet and phone journeys are art-directed separately and are stored as separate rows, so a phone does not simply inherit the desktop stops.
5. **At any scroll position the ground is the interpolation between the two bracketing stops, never a stepped switch at a boundary.** Scrolling backward runs the interpolation in reverse.
6. The ink flips between its light and dark values at the contrast crossover. That flip may be a short cross-fade, and it must happen before either value falls below its floor.
7. The logo chapter drives the logo fill and its counter-fill instead of the full journey: the ground stays near white and near black and the mark itself carries the colour.
8. A `Shuffle Color` control on the colour chapter reshuffles the current tone group's swatch samples and cross-fades the poster imagery with them. It changes what is displayed and writes nothing.

### The reveals and the scroll contract

1. Body copy and headings split into lines, and each line rises into place while its opacity rises, scrubbed against scroll position rather than triggered by an intersection.
2. **Scrolling backward un-plays every reveal rather than replaying it forward.** This is the check that separates a scrubbed timeline from a trigger, and a build that replays has not met the requirement.
3. Lines within a block stagger, so a paragraph assembles line by line, and the splitter re-splits on resize.
4. The parenthetical eyebrow and its running number ride a shorter ladder slightly after the lines they label, so the tag lands after its paragraph.
5. A control holds two copies of the arrow glyph, and on hover, on focus and on a carousel advance both layers move by one glyph height, so the resting glyph leaves and its duplicate arrives. It rolls rather than fades.
6. A logo lockup is revealed by a clip wipe from its bottom edge, fully clipped to fully open, scrubbed against scroll, with the inner content counter-translating so the lockup holds position while its window opens.
7. Scrolling is smoothed: wheel and touch drive one eased virtual position and every scrubbed timeline reads that one value. The smoothing pauses while the full-screen menu is open and resumes when it closes.
8. Progress comes from where a marker element sits relative to the viewport rather than from an absolute document offset, so a chapter of any height still lands its reveals and its colour on the right sections.
9. The route mask and the carousel enter and leave are triggered and play once; everything else named here is scrubbed.

### The colour chapter

1. It opens on a white ground with the display headline `Color` and a lead set large across the page: `Our color approach prioritizes elegance, restraint, and timelessness. The palette is intentionally neutral so that, like a gallery, it serves as a blank slate, creating a visual language that enhances our content rather than competes with it.`
2. Four tone-group sections follow, each a full-bleed ground with a large word and a short definition. `Core` tones support the brand imagery style, never blending into the background or creating too harsh a contrast. `Dark` tones are used as a background colour in place of true black and work best with multiple image styles, functional designs or text-heavy content. `Bright` tones are saturated yet sophisticated and are suited as an accent or across social media. `Light` tones are for an off-white background and pair best with UI or content-heavy designs.
3. Between the groups, sticky poster stacks pin and reveal by clip, cross-fading their imagery, with captions naming the tone and the application.
4. A paginated thumbnail rail steps through the examples and states its position, reading `01 / 07` on the longer rail and `01 / 04` on the shorter one.
5. Swatch samples carry a `HEX` label beside the value of the sample they name, which is the one place in the product where a colour value is shown as text, because the chapter is about colour.
6. The chapter closes on a poster carrying the trial call to action and then an `Explore Colors` affordance and a next-chapter affordance reading `Photography`.

### The logo chapter

1. It opens on a white ground with the display headline `Logo` and the lead `Latticework's logo captures a core conviction: that designing a beautiful website should be elegantly simple. Wherever the logo appears, it immediately signals our brand ethos, clarity over clutter, and impact over noise.` A dark section follows immediately below it.
2. The mark is presented as a monogram, described in the copy as an abstracted monogram of two interlocking S's, plus a wordmark set in the display face. Both are painted through masks rather than drawn as strokes, so one fill colour drives them and the mask animates independently as the visitor scrolls.
3. Sections state the rules: clear space, which surrounds the logo so other elements neither compete with nor crowd it; secondary-colour use; and misuse, which is that the logo is never shown warped, distorted, or oriented at an angle.
4. Lockups are specified: a partnership lockup built around an equidistant `X` between brand names, built from a quarter the thickness of the E's horizontal stroke and angled at 45 degrees to make a perfect square; and a `Latticework Presents` lockup for cinematic video.
5. A paginated in-use gallery, reading `01 / 07`, shows the mark applied across formats and is revealed by the logo-block wipe. A mark-in-motion block sits inside it, its opacity and position scrubbed, and it opens in an overlay dismissed by the close cross.

### The three-dimensional model surface

1. A three-dimensional renderer composites a scene into a canvas sized to the viewport, with a perspective camera.
2. The scene is a centred, faceted, low-polygon model shaded by surface normal, so facets take their colour from their orientation and no texture is needed, flanked by a solid red primitive on the left and a solid blue primitive on the right, on a plain ground, turning slowly about its vertical axis.
3. **The frame loop stops entirely when the surface is off-screen and resumes when it returns.** A loop that runs while nothing is watching is the single largest cost on the page.
4. The model geometry is composed from primitives rather than loaded, and any debug parameter panel is development-only and does not ship.

### Generated imagery and the object store

1. Every image the product shows is **generated once by the product** from a seed derived from its media key, tinted from the tone group it sits in, and the bytes live in **MinIO**, the S3-compatible object store at `STORAGE_ENDPOINT` and `STORAGE_BUCKET`, reached with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. No image bytes live on the app's filesystem and none live in a database column.
2. The key scheme is `media/{chapter_slug}/{media_key}/{sha256_of_bytes}.png`. A worked example: the colour chapter's first poster, whose media key is `core-poster-01`, is stored at `media/color/core-poster-01/9f2ab1c4e7d0a5b8c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4.png`.
3. The same seed and the same generator produce the same bytes, so the same image regenerated lands on the same key. The digest in the key is the digest of the bytes, so a stored image is verifiable against it.
4. For the tone-group and in-use sections the generated image is a soft studio gradient in the group's colour with a faint film grain; for the storefront and product-interface mocks it is a flat colour-blocked layout. Every one of them is marked as a placeholder so it is never mistaken for the brand's real photography.
5. A published chapter's image is readable by anyone. **An unpublished chapter's image is served only through an authenticated stream on this origin that checks the caller before it reads the object.** The bucket is never publicly readable and no pre-signed address is ever handed out.
6. Every media row has a real object at its key, and every object under a chapter's prefix has a row. One without the other is a defect.
7. The mark-in-motion block and the poster videos are the same mechanism: a looped, generated sequence produced by the product rather than a video file, shown through the same overlay.

### The free website trial

The one write a visitor can make.

1. The closing poster of a chapter carries the title `A website makes it real` and the body `Get your free website trial today. No credit card required.`, one email field and one control.
2. The form has exactly three states, `idle`, `success` and `failure`, all present in the page and toggled rather than injected when the answer arrives.
3. A valid address is accepted and answered with `Thank you. You are on the list.`
4. An address that is not a valid address is refused inline, beside the field, with the field named, and **nothing is written**. The failure copy is `Something went wrong, please try again.`
5. **Submitting the same address twice produces exactly one record.** The second submission does not create a second row and does not change the first row's moment; it is answered as a success, so a visitor is never told off for pressing twice.
6. The record keeps which chapter the visitor was reading when they submitted.
7. The trial list is readable by an Author and by nobody else.

### The author surface

1. An author creates a chapter through a route per step: details, sections, media, then review, each reachable at its own address, and the review step carries the publish control.
2. An author reorders a chapter's sections by dragging a row. **The row moves at once, and if the save is refused it is put back with a message saying so.** After a reorder the positions are contiguous from one: a reorder is a permutation, never an insertion that leaves a hole.
3. An author generates a section's imagery from the surface, which writes the bytes to the object store and the row beside it.
4. Every form here refuses invalid input inline, names the field that was wrong, and writes nothing when it refuses.
5. The endpoints-test surface is reachable by an Author only and exercises the content functions in isolation under the heading `Lambda Endpoints Test`. It is not a public chapter and is in no sitemap.

### The chrome, the not-found body and the launch surface

1. A fixed header band that paints no ground of its own carries the wordmark `Latticework Foundations` at the left and the `Index` control at the right. Both composite against whatever passes behind them, which is why the same wordmark reads dark on the white colour chapter and light on the dark index.
2. The menu button opens a full-screen menu over a frosted ground. Its items rest at full opacity and dim when a sibling is pointed at, so the pointed-at item stands alone. It traps focus while open, closes on the close cross, and returns focus to the control that opened it.
3. A route change is covered by a mask that wipes away on arrival.
4. First load shows a counter climbing to `100%` beside the word `Loading`, with a mark turning slowly counter-clockwise. **The page entrance is gated on the loader completing, not on a timer.**
5. A first-time visitor is asked once about non-essential cookies in the product's own panel, with rejecting exactly as easy as accepting, and the answer survives a reload.
6. An unknown address renders the product's own not-found body, a single centred line reading `404: Page not found` under the full chrome with a way back to the index, and answers not-found. It carries no chapter motion and does not drive the colour system.
7. **Every internal link on every public route resolves to a route that exists and answers.** A link to an address that does not answer is a defect the build catches rather than something a reader discovers.
8. A sitemap lists every published public route and a robots file points at it. The site serves a favicon and declares it in the document head.
9. Every public route declares a social preview title and a preview image, and that preview image resolves.

## User flow

The information architecture is one origin carrying three groups of addresses: the public chapters, the author surface and the two development surfaces.

| Route | Purpose | Auth |
|---|---|---|
| `/` | The index carousel | public |
| `/color` | The colour chapter | public while published |
| `/logo` | The logo chapter | public while published |
| `/typography` | An advertised chapter, unpublished | its author only |
| `/photography` | An advertised chapter, unpublished | its author only |
| `/motion` | An advertised chapter, unpublished | its author only |
| `/menu` | The full-screen menu as its own address | public |
| `/webgl` | The three-dimensional model surface | public |
| `/lambda` | The endpoints-test surface | Author |
| `/signup` | Create a Reader account | public |
| `/login`, `/logout` | Sign in and out | public |
| `/studio` | The author's own chapters, as a card grid | Author |
| `/studio/chapters/new/details` | New chapter, step one | Author |
| `/studio/chapters/new/sections` | New chapter, step two | Author |
| `/studio/chapters/new/media` | New chapter, step three | Author |
| `/studio/chapters/new/review` | New chapter, step four, and the publish control | Author |
| `/studio/chapters/<slug>` | One chapter's sections, reorderable | Author, own chapter only |
| `/studio/trials` | The trial list | Author |
| `/sitemap.xml`, `/robots.txt`, `/favicon.ico` | Sitemap, robots and favicon | public |
| `GET /api/health` | Readiness | public |

**Entry and redirects.** An unauthenticated request for any `/studio` address or for `/lambda` goes to `/login` carrying the address that was asked for, and lands there once signed in. Signing in sends an Author to `/studio` and a Reader to `/`. Signing out returns to `/` and the token stops working. A token that expires part way through an edit returns the Author to `/login` with nothing written. A Reader asking for a `/studio` address or `/lambda` is refused by the server, not merely shown a page without the link. An unpublished chapter's address is refused to everybody but its own author. Every other unknown address renders the not-found body and answers not-found.

**Journeys.**

1. A visitor opens `/`. The counter climbs to `100%` beside `Loading`, the entrance plays, and the carousel takes over showing `Latticework` and `Foundations` over the lead line. They press the next control, watch the frame window morph while the image inside holds still, and open `( Color )`.
2. On `/color` they scroll from the white opening through `Core`, `Dark`, `Bright` and `Light`. The ground washes continuously rather than switching at each section, and the ink flips so the text stays readable. They scroll back up and the lines un-rise rather than replaying.
3. They press `Shuffle Color`, the swatches reorder and the poster imagery cross-fades, and nothing is written.
4. They reach the closing poster reading `A website makes it real`, type `hollis@example.com` into the one field and press the control. The idle state is replaced in place by `Thank you. You are on the list.` They press it again with the same address and are answered the same way, and there is still exactly one record.
5. They follow `Explore Colors`, then the next-chapter affordance reading `Photography`, and arrive at `/logo` through the route mask, where the mark rather than the page takes the colour.
6. A visitor opens `/typography` directly. The request is refused and no chapter content is served. A completely unknown address renders `404: Page not found` under the full chrome instead.
7. `author@example.com` signs in and lands on `/studio`, which shows their four chapters as a card grid. They walk the four wizard steps at `/studio/chapters/new/details`, `/studio/chapters/new/sections`, `/studio/chapters/new/media` and `/studio/chapters/new/review`, generate the new chapter's imagery, which lands in the object store at its key, and publish it from the review step. It becomes readable at its slug and joins the sitemap.
8. The same Author opens `/studio/chapters/color`, drags the third section above the second, and the row moves at once. The order survives a reload, and the positions are still contiguous from one.
9. `author@example.com` asks for `/motion`, for its sections and for its generated image. All three are denied, because that chapter belongs to `author2@example.com`.
10. `reader@example.com` signs in, reads `/color` and `/logo` in full, and is denied `/studio`, `/studio/trials`, `/lambda` and every unpublished chapter's address.
11. A visitor opens `/webgl`, watches the model turn between its red and blue neighbours, scrolls it out of view, and the frame loop stops rather than continuing to draw.

**States.** Every list has an empty state naming what would fill it: an Author with no chapters yet, a chapter with no sections yet, an empty trial list. Every surface that waits says it is waiting, including the first-load counter and the moment a generated image is still being produced. An error never leaves a blank page. The not-found body carries the full chrome and a way back to the index, because somebody who mistypes an address is one press away from the thing they came for.

## UI/UX notes

Somebody arriving here should understand in the first moment that this is a gallery rather than a manual, and should feel unhurried, the way a room holding one object holds you. That is what every later decision resolves against. The register is editorial: the subject itself is the first thing seen, the composition carries atmosphere, and nothing here is an operational dashboard. Restraint over expression, continuity over punctuation, space over dividers.

Colour is named by role, and the ratio between the roles is the requirement rather than the list. The resting page ground is a near-white neutral and the ink on it is a near-black neutral. A second near-black neutral is the section ground used in place of true black. A near-white neutral one step deeper carries hairlines and inactive interface, and a further near-white neutral is the off-white ground that is also the ground behind imagery. The near-white ground dominates by close to two orders of magnitude over every other value and the near-black section ground is the second structural colour; build to that weighting or the product stops reading as a gallery. Three accents are held in reserve and appear rarely: a mid, soft orange, a mid, vivid blue, and a mid, vivid red. They are the one or two additional tones the copy describes as introduced as accents for contrast and depth, never part of the resting surface. A small set of translucent neutrals carries hairlines, scrims and unavailable states on both the light and the dark ground. The exact shades are yours, so long as the weighting above holds and the accents stay guests.

The animated colours are a separate system from the resting palette and are the chapter's substance. Four tone groups carry the colour chapter: `Core` is a deep warm neutral on the wider tiers and a near-black neutral on a phone, `Dark` is a deep neutral on desktop and phone and a mid warm neutral on a tablet, `Bright` is a light, soft orange on desktop and phone and a mid, soft orange on a tablet, and `Light` is near-white everywhere. The ink is near-white across the two dark groups and near-black across the two light ones. The logo chapter drives its mark instead: the fill moves from near-black toward a light cool neutral on desktop, a deep, soft orange on a tablet and a near-black neutral on a phone, while its counter-fill moves toward near-white. Within those descriptions the exact values are yours.

Type is three families and no fourth, and here the exact identity is the specification rather than the value. `Grotesk Display` is the display, heading and interface face at weights 300, 400, 500, 600 and 700. `Grotesk Serif` is the editorial companion at 300, 400 and 500, upright and italic. `Grotesk Condensed` carries the oversized poster lettering at 300, 400, 500, 700 and 900. Each falls back through a normative stack and loads with swap behaviour, so no line of type is ever invisible while a face resolves. The rendered scale runs `200px` over `160px` for the largest full-bleed poster words, `137.5px` over `110px` for secondary poster words, `104px` and `100px` for a chapter display headline, `85px` for a large section word, `68.75px` for a reduced chapter headline, `58.4375px` and `58.24px` over `52.416px` for a lead set large, `49.92px` for a sub-heading, `32px` over `35.2px` for a card or poster title, `24px` and `22px` over `24.2px` for body-large, `20.8px` and `20px` over `22.88px` and `22px` for body, `16.64px`, `16.5px` and `16px` over `18.304px` and `17.6px` for interface text, `15.6px` and `15px` for labels, `14.56px` and `13.75px` over `16.016px` and `15.125px` for small labels and captions, and `11px` and `10.3125px` over `12.1px` for eyebrow index numbers and fine print. Those are the rendered result of a viewport-derived root rather than values to hard-code; reproduce the sizing rule and the fractions follow. Headings are set solid, at a line height near their own size, so the poster words can bleed off the edges of the viewport.

Everything structural is square. The only circles in the product are the pagination and menu dots. Code and small chips carry the one small softening, and the single elaborate set of corners belongs to the mocked search field inside the colour chapter's in-use posters, which is the one pill shape anywhere. Density is spacious: one subject per screen, room around it, and sections separated by space rather than by a dividing rule. The twelve-column grid holds at every width, and the gap between sections is a multiple of the gap beneath a heading rather than an independent measure.

The motion character is **eased**: a considered entrance and exit, so motion reads as a designed interface rather than as a machine responding. One house ease-out is the dominant curve and carries the reveal transforms, appearing more often than every other curve put together: a slow-out settle that eases off at the end rather than starting sharply. A sine ease-out carries the colour and background moves. A symmetric sine ease-in-out carries transitions that come and go the same way. A standard curve carries interface state changes. A quad ease-out carries the slower, longer transforms. A cubic ease-in-out carries the long colour sweep. A width hold grows a width almost instantly and then holds a long tail. Colour is always the slowest thing on the page and a state change is always the quickest. Nothing uses a different speed to feel special. There is exactly one keyframe loop in the whole product, the loader's mark turning counter-clockwise; everything else is a declared transition or a scrubbed timeline, and no further loop is added, because the stillness is deliberate. There is no blanket rule that transitions every property on an interactive shell, because such a rule quietly animates things nobody intended.

The moments worth naming, because a build that names none of them ships none of them: text rises into place line by line and un-rises on the way back up; a parenthetical tag and its number land a beat after the sentence they label; an arrow rolls over to a fresh copy of itself rather than fading; a logo lockup wipes open from its bottom edge while its content holds still; a card's picture frame changes shape while the picture inside it holds position; a route change is covered by a mask that wipes away on arrival; the menu arrives over a frosted ground and the items a pointer is not on dim behind it; and the whole page washes from one tone group to the next as a continuous repaint. Under a reduced-motion preference each of those is **replaced rather than frozen**: the line cascade resolves to its end state with a short fade and no movement, the repaint applies each section's end colour as a short cross-fade instead of a scrub, the loader shows its counter without the turning mark, and the carousel advances by a cut. The fade is preserved; movement is what goes.

Depth is real on the index rather than implied: the cards live in a shallow three-dimensional stack and tilt as they pass, which is why the carousel does not read as a flat slider. Layering runs a short, disciplined set of stacking levels, with scrolling content at the bottom, chapter and carousel interface above it, and the menu and the route mask above everything; nothing is introduced above that top level.

Components are specified by what they do in each state rather than by their dimensions. Resting, pointed-at, pressed, focused and unavailable are all drawn, and unavailable is never signalled by colour alone. Escape closes the menu and the video overlay and returns focus to the control that opened it. Hover treatments are declared only where a fine pointer exists, and anything that reveals on hover is permanently revealed where there is none, so a tap on a phone never leaves a control stuck looking pressed; a coarse pointer gets the drag affordance instead.

Accessibility is contract and does not vary with any of the above. One first-rank heading per route naming the chapter, and the parenthetical eyebrows are not headings. A main landmark wraps chapter content, the header is a banner, and the full-screen menu is a labelled dialog. Every chapter is reachable and operable by keyboard navigation: the carousel advances with the arrow keys, the menu traps focus and restores it to its opener, the close cross is focusable, and the explore affordances are in the tab order. A visible focus ring is present throughout and is never suppressed. Every content image carries a text alternative from the content layer and every decorative one declares itself decorative; the three-dimensional surface and the mark's mask geometry are hidden from assistive technology; the loader announces its progress politely. Because the ink flips against a moving ground, the WCAG AA bars have to hold through the whole interpolation and not only at the stops: body text stays at or above a contrast ratio of `4.5:1` and large text at or above `3:1` at every point between two stops, and the crossover between the light and dark ink happens before either falls below its floor. No interactive target is smaller than a comfortable fingertip, and every icon-only control carries a name saying what it does rather than what it depicts.

The layout turns on one primary boundary, with orientation and pointer refinements on top of it, and it holds at every width between the named tiers rather than only at them. Above the boundary the wide multi-column compositions hold; below it the carousel and the poster layouts restack to a single column while the side margin and the column width contract and the twelve-column structure survives. The colour journey uses its own per-tier stops rather than inheriting the desktop ones. Landscape and portrait each get their own refinement at the same boundary, because a short landscape phone and a tall portrait one need different full-screen compositions, and collapsing them to width alone loses one of the two. Viewport-height handling is its own requirement: any full-height surface measures the real visible height rather than the naive viewport unit, or the carousel and the colour grounds jump the moment a phone's address bar slides away. At a narrow viewport nothing overflows sideways and every navigation target stays reachable. Where the breakpoint falls is yours, so long as the arrangement never breaks between the tiers.

**Each page leads with one clear primary action, visually distinct from every secondary one.** On a chapter that action is the free trial and it waits until the closing poster; on the index it is entering the card in view; in the author surface it is the one control that moves the work forward. There is never a second thing competing with it.

Five failures to design against, and each is a failure rather than a fashion. A page dominated by one hue family with no second signal for meaning. Colour used as decoration outside the chapter that is about colour. A reveal that replays forward on the way back up, which turns a scrubbed timeline into a trigger and breaks the whole scroll contract. Decoration standing in for content on a page whose subject is the content. And a marketing composition inside the author's surface, which is working software.

## Technical requirements

The stack is fixed. The rendering model is a single-page application over a JSON interface: one shell, client-side routing, one chapter mounted at a time, and each chapter's content fetched as JSON rather than delivered as a document per route. The frontend is **Lit with Vite**, built to a production bundle of standard custom elements. The backend is **FastAPI**, which serves that bundle for every address the router owns and serves the HTTP API on the same origin under the `/api` prefix. The datastore is **PostgreSQL** at `DATABASE_URL`. The object store is **MinIO** at `STORAGE_ENDPOINT` and `STORAGE_BUCKET`, reached with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The public origin and port are `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read every host, port and credential from the environment and never hardcode one. The backing services named in this brief are already running at those variables.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation.

Auth is app-implemented: email and password exchanged for a bearer token, passwords under a modern memory-hard password hash, tokens that expire. `GET /api/health` returns `200` once the app is ready.

Logs are structured, one line of JSON per request on standard output, carrying the method, the route, the status, the elapsed milliseconds and a request identifier, and that identifier comes back in the body of every error response. No password, no token and no object key is ever written to a log.

**A sitemap lists every published public route and a robots file points at it.** The site serves a favicon and declares it in the document head. **Every public route declares its own social preview title and its own preview image, and that preview image resolves rather than pointing at an address that answers nothing.**

No credential, no key and no admin token appears in anything the browser downloads, and the object store's own credentials never leave the server.

The product fetches nothing from outside its own origin at run time. No web font binary, no analytics beacon, no consent vendor, no content host and no asset host.

The performance budgets are requirements rather than aspirations. One animation-frame callback drives the scroll timelines and the colour driver; parallel loops are what make a scrubbed page stutter. The three-dimensional frame loop halts when its surface is off-screen. Text is split once per layout and re-split only on resize. Compositor hints are capped at fewer than `120` elements in total and are applied only to elements that are currently animating. The first content paints before the loader hands over, and nothing shifts position afterwards. The frame budget while a chapter is scrolling with the colour system running, and while the model surface is visible, is a sustained `60fps` on a three-year-old laptop rather than an average. Loading order follows from that: the loader and the first chapter's shell first, then that chapter's content, then the model surface and anything below the fold.

The copy layer is addressed by locale and key rather than written into markup, so the product's strings are data. One locale ships.

The app stays responsive with `5` chapters, `40` sections, `120` media rows and `5000` trial signups.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**Identity.** `account` holds `id`, `email` unique and compared case-insensitively, `display_name`, `password_hash`, `role` among `author` and `reader`, and `created_at`. `session` holds `id`, `account_id`, `token_hash`, `expires_at` and `created_at`.

**Content.** `chapter` holds `id`, `slug` unique among `color`, `logo`, `typography`, `photography` and `motion`, `index_label`, `eyebrow`, `title`, `lead`, `published`, `published_at`, `author_account_id` and `created_at`; order is by `index_label`. `section` holds `id`, `chapter_id`, `position`, `kind` among `intro`, `tone-group`, `poster-stack`, `rules`, `in-use` and `cta`, plus `eyebrow`, `index_label`, `heading` and `body`, unique on `chapter_id` and `position` together. `tone_stop` holds `id`, `section_id`, `group_name` among `Core`, `Dark`, `Bright` and `Light`, `tier` among `desktop`, `tablet` and `mobile`, `ground`, `ink` and `position`, with one row per group per tier. `caption` holds `id`, `section_id`, `position` and `text`. `copy_entry` holds `id`, `locale`, `key` and `value`, unique on `locale` and `key` together.

**Media.** `media_ref` holds `id`, `section_id`, `media_key` unique, `ratio`, `tone`, `alt`, `object_key` unique, `byte_size`, `digest` and `generated_at`. `object_key` is where the generated bytes live in the object store and `digest` is the digest of those bytes.

**The one write.** `trial_signup` holds `id`, `email` unique, `source_chapter_id` and `created_at`.

**Which values are derived rather than stored.** A chapter's public readability is derived from `published` and from nothing else, so there is no second flag that can disagree with it. The set of chapters the index advertises is every chapter; the set that resolves is the published subset. The ground behind imagery is derived from the page ground, one lightness step lighter. A tone stop's ink is chosen so the pair clears its contrast floor, and the crossover between the two inks is derived from the interpolation rather than stored per section. The digest in a media object's key is the digest of the bytes themselves.

**Invariants, as properties of the running system.** A chapter whose `published` is false is served by no public route, appears in no sitemap and is readable only by its own author. Every `media_ref` has a real object at its `object_key`, and every object under a chapter's prefix has a row. `section.position` is contiguous from one within a chapter after any reorder, so a reorder is a permutation rather than an insertion that leaves a hole. One `trial_signup` exists per address: a second submission of the same address creates no second row and does not move the first row's moment. Every string the product displays resolves to a `copy_entry` for the active locale.

**Seed data.** Five chapters: `01` `color` and `02` `logo` published and owned by `author@example.com`; `03` `typography` and `04` `photography` unpublished and owned by `author@example.com`; `05` `motion` unpublished and owned by `author2@example.com`. The colour chapter carries an intro section, four tone-group sections named `Core`, `Dark`, `Bright` and `Light`, two poster-stack sections, a rules section and a closing `cta` section; the logo chapter carries an intro, a mark section, a rules section, an in-use section and a `cta` section. Twelve `tone_stop` rows, one per group per tier. Nine captions on the colour chapter, reading `Primary, Product UI`, `Primary, Marking poster`, `Primary, Mobile Website Comp`, `Primary, Poster Layout`, `Primary, Template Marketing`, `Secondary, Dark, Layout`, `Secondary, Light, UI Highlight`, `Secondary, Core, Layout` and `Secondary, Bright, Web`. Seven captions on the logo chapter, reading `Logo, Maker Community, Campaign`, `Logo, Built to Sell, Static Poster`, `Logo, Refresh 2025, Product UI`, `Logo, Refresh 2025, Web`, `Logo, Change Your World, Social`, `Logo, Change Your World, Static Poster` and `Logo, Frontsite, Web`. Three demo template names are used in the mocks: `Meridian`, `Kiln` and `Atelier`. Three accounts as named in `## User roles`. One trial signup already exists on `hollis@example.com`.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual and structural detail that `## UI/UX notes` states as intent. Everything here is a requirement on what a reader sees. No colour is given as a code, no space as a measurement and no motion as a timing; type is the one exception, because a family and a size are an identity a builder cannot guess.

### The token layer and the grid

One token layer defined once at the document root and consumed everywhere. The grid is twelve columns expressed through named tokens: a column count, a nominal column width at the desktop tier, a column gap that is the gutter between columns, a page side margin, a reserved header band, a gap around the carousel arrow controls, a reserved footer band at the bottom, and a spacer that reconciles the collapsing mobile browser chrome. The root sizing is viewport-derived so that type and spacing grow together between the tiers; that rule is what produces the fractional rendered scale, and transcribing the fractions without the rule reproduces the numbers and not the behaviour. Three widths are the reference points: a desktop width, a tablet width and a phone width.

Colour tokens are declared on the root by role: the text colour on light grounds and icon strokes, the text colour on dark grounds and light grounds, the near-black section ground used in place of true black, the off-white ground which is also the default media ground, the hairline and inactive-interface grey, the three reserved accents, and the five animated properties at their resting values. The header declares a transparent ground of its own and never paints one. A handful of structural greys sit between the near-black and the near-white for hairlines and dividers.

### The effects vocabulary

Four effects appear often enough to be system decisions rather than local flourishes, and each one earns its place.

- **The difference blend on chrome.** The wordmark, the carousel interface text and the `Tap to Explore` label composite against whatever passes behind them rather than switching colour by rule. It is the single most characterful thing in the product and it is why one declared colour reads correctly on a white chapter and on a dark index alike.
- **Frosted overlays.** A heavy backdrop blur behind the full-screen menu ground, and a light one behind the consent panel.
- **Reveal masks.** The editorial reveal and the carousel frame are driven by clip geometry rather than by opacity: a wipe hidden from the bottom up, a fully open state, and the carousel's three aspect insets.
- **Depth.** The carousel items and their inner fills preserve three-dimensional space, so the index is a stack rather than a flat slider.

Compositor hints are the one part of this vocabulary that is capped rather than encouraged: they go only on elements that are animating right now, and they stay under the total named in `## Technical requirements`.

### Layering

Stacking runs a short set of levels and no more: the scrolling content at the bottom two, the carousel and chapter interface in the middle band, and the full-screen menu and page-transition mask at the top. Nothing is introduced above the top of that set.

### Iconography

Four glyphs and one mask mechanism, all inline geometry, none of them a file. Each is drawn on its own declared viewBox whose path extent fills it, so the glyph stays sharp at any size and takes the current colour.

- **The directional arrow.** One closed path, filled with the current colour, mirrored on the vertical axis for the left variant. A control holds two copies of it, a main layer and a secondary layer, which translate together so one glyph leaves as its duplicate arrives.
- **The close cross.** A square canvas holding two full-diagonal strokes with round caps, stroked in the current colour, used to dismiss the full-screen menu and the video overlay.
- **The ring.** A single unfilled circle at one hairline stroke, used as a control outline and as a pagination mark.
- **The dot.** A filled disc, fully round, sized by its container, used as a pagination and menu-position mark.

The brand mark is two elements, a monogram symbol and a wordmark, and both are painted through SVG masks rather than as strokes, so a single fill colour drives them and the mask animates independently. The mark's own geometry is yours to supply as two inline symbols used exactly as masks; the mechanism is what is specified, so the scroll recolour and the re-forming animation work unchanged whatever mark is dropped in. Where a drawing carries an internal mask or filter reference, that reference is made unique per instance, because two copies of one drawing on a page that declare the same internal identifier collide and one of them renders wrong.

### Global chrome

**The header** is a fixed band of the reserved header height that paints no ground. It carries `Latticework Foundations` at the left and `Index` at the right, both compositing with a difference blend so they invert against whatever passes behind them rather than switching colour by rule. On a chapter the left label is joined by a second line reading `Index`, and both take part in the scroll reveal.

**The menu button** opens the full-screen menu and its only state change is a fade to half opacity.

**The full-screen menu** is a fixed overlay above all content over a heavy backdrop blur and a ground at low opacity. Its items rest at full opacity and dim when a sibling is pointed at, so the pointed-at item stands alone. It closes on the close cross.

**The page-transition mask** covers a route change and wipes away on arrival, on the house curve, carrying the same near-zero rounded corner the carousel frame rests at.

**The page loader** shows a percentage counting to `100%` beside the word `Loading`, with a mark turning continuously counter-clockwise, which is the one keyframe loop in the product. The page entrance is gated on the loader completing rather than on a timer.

**The consent panel** is the product's own plain, accessible panel over a light backdrop blur, with rejecting exactly as easy as accepting, and its answer survives a reload.

### The carousel engine

The document does not scroll on the index; the carousel advances instead. Each card is a framed image with a caption, an index number and an eyebrow. Advancing translates the stack of cards through three-dimensional space, which is why the cards tilt rather than slide flat, while the visible card's frame mask morphs between window shapes: a tall portrait window, a wide landscape window, a slim band, and the resting rounded-rectangle corner whose softening is almost nothing. The content inside the frame counter-translates so the image holds position while its window reshapes. Individual cards reveal with rectangular clip insets opening from a centred rectangle to fully open rather than with the morph, and the inverse logo card opens from a zero-area polygon to its full rectangle. Controls are the previous and next arrows, drag, and the arrow keys, and the interface text uses the difference blend.

### Route: the index

Top-left the wordmark, top-right `Index`, centre the framed carousel card, bottom-left the card's index number, bottom-centre the card's eyebrow in parentheses, bottom-right the previous and next arrows. On first entry the display words `Latticework` and `Foundations` and the lead line introduce the carousel before the cards take over. Each card advertises a chapter with its number, its eyebrow and its framed image, and a `Tap to Explore` label on the difference blend invites entry. Five chapters are advertised and two of them resolve.

### Route: the colour chapter

A white ground, the display headline `Color` at the chapter-headline size, and the lead set large across the page in the line cascade, each line rising as the visitor scrolls.

Four tone-group sections follow, one per group, each a full-bleed colour ground carrying the group's large word at the large-section-word size and a short definition, with the page ground washing to that group's colour. Between them, sticky poster stacks pin and reveal by clip while their imagery cross-fades, with captions naming the tone and the application. A paginated thumbnail rail with the arrow controls steps through the examples and states its position.

Swatch samples carry a `HEX` label beside the value they name, and the `Shuffle Color` control reshuffles them. The mocked storefront and product-interface posters read `A website makes it real` and `Made with Latticework` and show a demo template, and they are the one place in the product where a pill-shaped field with elaborate corners appears.

The chapter closes on the poster carrying the trial call to action, then `Explore Colors`, then the next-chapter affordance reading `Photography`.

Its copy, pinned:

| Key | Copy |
|---|---|
| notes-1 | `The goal is to ensure harmony with the overall design.` |
| primary | `Our color palette is grounded in four tonal groups: core, dark, bright, and light, with the core tones serving as our foundation. To maintain visual consistency, our essential brand elements, typography, logo, and icons, appear in black and white whenever possible.` |
| in-use-1 | `Our color approach prioritizes sophistication, using muted, refined tones that allow customers to take center stage through photography and imagery while steering clear of saturated colors and the conventionally "friendly" palette often seen in tech.` |
| secondary | `Beyond the four groups of our color palette, one or two additional tones are often introduced as accents to provide contrast and depth.` |
| notes-image | `Image directs color palette` |
| secondary-note | `Secondary colors always complement our imagery, never overpowering it or blending into it. When an image contains multiple hues, we choose a tone that best supports the broader design.` |
| in-use-2 | `The more complex and colorful the imagery, the more freedom there is to pull from it to best suit the purpose of the design.` |
| pull-quote | `From playful to experimental solutions` |

### Route: the logo chapter

A white ground, the display headline `Logo`, the lead, and a dark section immediately below on the near-black section ground. The mark is presented as the monogram and the wordmark through the mask mechanism, recoloured by the scroll-driven fill and counter-fill and re-forming as the visitor scrolls. Sections carry the construction and the rules, then the lockups, then a paginated in-use gallery revealed by the logo-block wipe with its captions, then the mark-in-motion block whose opacity and position are scrubbed and which opens in the overlay.

Its copy, pinned:

| Key | Copy |
|---|---|
| notes-1 | `Designed for clarity, impact, and hierarchy.` |
| design | `Two essential elements define the logo. The symbol, an abstracted monogram of two interlocking S's, creates a distinctive emblem, while the wordmark is set in Grotesk Display, the bespoke typeface crafted for our brand.` |
| systems | `Systems for consistency. Our spacing, scale, type, and color formulas create a cohesive system that is versatile, expressive, and unmistakably Latticework, while ensuring consistency across all applications.` |
| clearspace | `For maximum visibility and impact, the logo is surrounded by a designated clear space to prevent other elements from competing with or crowding it.` |
| secondary-colour | `When the logo appears in secondary colors, it ensures visual harmony while staying true to our balance of sophistication and restraint.` |
| misuse | `To preserve clarity and impact, the logo is never shown warped, distorted, or oriented at an angle.` |
| lockups | `Built for versatility, the logo adapts easily to custom lockups for partnerships, product features, and video content, showcasing our range without losing identity.` |
| partnership | `Partnership lockups. A visual expression of collaboration, our partnership lockups use an equidistant 'X' between brand names. The 'X' is built from a quarter the thickness of the E's horizontal stroke, and then angled at 45 degrees, creating a perfect square.` |
| presents | `Latticework Presents. The Latticework Presents lockup creates clean and balanced introductions for our most cinematic videos, while providing instant brand recognition.` |
| in-use | `The refined simplicity of our logo allows it to show up seamlessly across a wide range of formats, while maintaining clarity and brand integrity.` |
| next | `Typography` |

### Routes: the development surfaces and the not-found body

`/webgl` hosts the model surface under the global chrome. `/lambda` is a single heading reading `Lambda Endpoints Test` over the standard shell, exercising the content functions in isolation, reachable by an Author only. Any unknown address renders a minimal body: the global chrome over a single centred line reading `404: Page not found`. It carries no chapter motion and does not drive the colour system; the ground stays at its resting value.

### Modules

The component architecture is six shared parts plus two app-level services, and the two services are what make the product one product rather than three chapters that happen to match.

- **The line splitter** splits a text block into lines and drives the cascade. It must re-split on resize.
- **The eyebrow and index** is the parenthetical tag and the running number.
- **The arrow button** is the two-layer arrow control.
- **The carousel** is the engine above.
- **The poster stack** is the pinning, clipping gallery used by both chapters.
- **The video overlay** carries the mark-in-motion block and the poster sequences and is dismissed by the close cross.
- **The colour driver** is an app-level service that maps scroll position to the animated properties and writes them to the document root. It lives at the top level so colour behaves identically on every chapter rather than being re-implemented per chapter.
- **The scroll service** owns the smoothed position, the marker-derived progress and the single animation-frame callback every scrubbed timeline reads.

### The trial form

One email field and one control on the closing poster. The three states, `idle`, `success` and `failure`, are all present in the page and toggled, never injected when the answer arrives. The copy is pinned below. A refusal names the field beside the field. The control is the page's one primary action and nothing competes with it.

### Copy

Every string below is pinned, and every one of them is looked up by locale and key rather than written into the markup.

| Where | String |
|---|---|
| Wordmark | `Latticework Foundations` |
| Index control | `Index` |
| Loader text | `Loading` |
| Loader figure | `100%` |
| Carousel invitation | `Tap to Explore` |
| Trial title | `A website makes it real` |
| Trial body | `Get your free website trial today. No credit card required.` |
| Trial success | `Thank you. You are on the list.` |
| Trial failure | `Something went wrong, please try again.` |
| Not found | `404: Page not found` |
| Index display words | `Latticework` and `Foundations` |
| Index lead | `Discover the essential guiding principles and distinctive visual elements that define the Latticework identity.` |
| Card eyebrows | `( Color )`, `( Logo )`, `( Typography )`, `( Photography )`, `( Motion )` |
| Colour chapter title | `Color` |
| Colour chapter lead | `Our color approach prioritizes elegance, restraint, and timelessness. The palette is intentionally neutral so that, like a gallery, it serves as a blank slate, creating a visual language that enhances our content rather than competes with it.` |
| Tone group Core | `Core` and `Our Core tones are designed to support our brand imagery style, never blending into the background or creating too harsh a contrast.` |
| Tone group Dark | `Dark` and `Used as a background color in place of true black, our Dark tones work best when displaying multiple image styles, functional designs, or text-heavy content.` |
| Tone group Bright | `Bright` and `Our Bright tones are saturated yet sophisticated, ideally suited as an accent color or across social media.` |
| Tone group Light | `Light` and `Used when in need of an off-white background color, our Light tones pair best with UI or content-heavy designs.` |
| Swatch label | `HEX` |
| Shuffle control | `Shuffle Color` |
| Colour explore affordance | `Explore Colors` |
| Colour next chapter | `Photography` |
| Storefront mock | `Made with Latticework` |
| Logo chapter title | `Logo` |
| Logo chapter lead | `Latticework's logo captures a core conviction: that designing a beautiful website should be elegantly simple. Wherever the logo appears, it immediately signals our brand ethos, clarity over clutter, and impact over noise.` |
| Endpoints surface | `Lambda Endpoints Test` |
| Thumbnail rail positions | `01 / 07` and `01 / 04` |

The five campaign names in the logo captions are `Maker Community`, `Built to Sell`, `Refresh 2025`, `Change Your World` and `Frontsite`. The studio credited in the colophon is `Northmark`.

### Generated imagery, in detail

The zero-asset rule governs this whole section: no binary ships and no binary is fetched, and every class of asset the product would otherwise load has a substitution here instead. Every picture is produced by the product itself, keyed by a seed derived from its media key and tinted from the tone group it sits in, honouring that media row's ratio, tone and text alternative. For a tone-group or in-use section the picture is a soft studio gradient in the group's colour carrying a faint film grain; for a storefront or product-interface mock it is a flat colour-blocked layout. Each one is marked as a placeholder. The reveal and frame geometry is drawn rather than loaded: the carousel window shapes, the resting corner, the reveal insets and the page-transition corner are all clip geometry applied over a bounding-box coordinate system, so one definition scales to every card size. The tone-group grounds need no picture at all, because they are the interpolation written to the page ground. The mark-in-motion clip is a looped generated sequence of the mark re-forming through its mask over a tone-group ground, shown through the video overlay. Any interface cue is synthesised at run time as a short enveloped tone with a fast decay for advance and select, with no ambient bed and no audio file.

## Constraints

- One brand, one origin, one locale shipped. No second origin for assets, content or signup.
- No binary asset of any kind ships or is fetched: no photograph in any modern image format, no video file, no audio file, no font binary in `woff2`, `ttf` or any other format, no three-dimensional model file or compressed geometry, and no vector-animation document or the `wasm` runtime that would play one. Every picture, every clip and every cue is generated by the product.
- No third-party analytics, consent vendor, content host, asset host or measurement identifier. Nothing leaves this origin at run time, so no page-view beacon exists and no external script is loaded.
- No payment of any kind and no card details. The trial is free.
- No comments, no likes, no sharing, no social graph, no chat, no newsletter and no search across chapters.
- No second database, cache, queue, object store, identity provider or mail vendor. No email is sent by this app and no mail server is available to it.
- No native application and no offline mode.
- No keyframe loop beyond the loader's turning mark, and no blanket transition rule on an interactive shell.
- The three-dimensional model, the loader's drawn flourish and the interface audio cues are reconstructions rather than records, and are expected to be close rather than exact.
- The app stays responsive with `5` chapters, `40` sections, `120` media rows and `5000` trial signups.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/sign-up` | `email`, `password`, `display_name` | the account and a bearer token |
| `POST /api/auth/sign-in` | `email`, `password` | a bearer token and its expiry |
| `POST /api/auth/sign-out` | | the token invalidated |
| `GET /api/chapters` | | a top-level JSON array of every chapter, each with its `slug`, `index_label`, `eyebrow`, `title` and `published` |
| `GET /api/chapters/<slug>` | | the chapter with its ordered sections, for a caller entitled to read it |
| `GET /api/chapters/<slug>/sections` | | a top-level JSON array of that chapter's sections in position order |
| `POST /api/chapters` | `slug`, `index_label`, `eyebrow`, `title`, `lead` | the created chapter, unpublished, owned by the caller |
| `POST /api/chapters/<slug>/sections` | `kind`, `eyebrow`, `index_label`, `heading`, `body` | the created section at the end of the order |
| `PUT /api/chapters/<slug>/order` | `order`, a list of section identifiers | the sections in their new order, positions contiguous from one |
| `POST /api/chapters/<slug>/publish` | | the chapter published, with the moment recorded |
| `POST /api/chapters/<slug>/unpublish` | | the chapter unpublished |
| `POST /api/sections/<id>/media` | `media_key`, `ratio`, `tone`, `alt` | the media row with its `object_key` and `digest`, the bytes written to the object store |
| `GET /api/media/<media_key>/content` | | the stored object streamed, for an entitled caller only |
| `GET /api/copy` | `locale` | the copy entries for that locale, keyed |
| `POST /api/trials` | `email`, `source_chapter_slug` | the signup, exactly one per address |
| `GET /api/trials` | | a top-level JSON array of signups, for an Author only |
| `GET /api/health` | | readiness |

Bearer auth is required on everything except sign-up, sign-in, health, the public chapter reads, the copy read and the trial submission. A successful call returns the named resource or shape, and an invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success.

### No mocks

The object store is not simulated. Image bytes on the app container's filesystem, a base64 column in PostgreSQL, a picture the browser redraws on every request instead of a stored object, or a `{"stored": true}` the app returns to itself are each a contract violation however good the page looks. The same holds for the datastore: chapters held in a process rather than in PostgreSQL disappear when the app restarts, and a chapter set assembled from a module-level list is not a content layer. **MinIO and PostgreSQL are the fact: this app's own screens and its own tables can only reflect what lives in them, never substitute for them.**

## Definition of done

A stranger can page through the index carousel, open the colour chapter, and watch the whole page repaint continuously through `Core`, `Dark`, `Bright` and `Light` while the text stays readable at every point between the stops, then scroll back up and see the reveals un-play rather than replay. They can start a free website trial from the closing poster, and pressing it twice with the same address still leaves exactly one record. Every picture on the page is a real object in the store at its own key. An unpublished chapter is unreachable by anyone but its author, at every address it has.
