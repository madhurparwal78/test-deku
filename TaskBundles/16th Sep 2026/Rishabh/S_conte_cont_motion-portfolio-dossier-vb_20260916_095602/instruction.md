# Motion Portfolio Dossier

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, move down a dark portfolio home page while nine pictures drift behind the name, narrow the work index to one discipline, open a long case study, follow its chapter rail, save it to a reading list, and come back later to the chapter where they stopped, without hitting an error page. A different stranger, signed in as a reader or signed in as nobody at all, must NOT be able to reach a case study the designer has written but not published, by any means: not from the home page, not from the work index, not from a suggestion, not by typing its address, and not by fetching its image. The images the designer uploads must live as real objects in the `minio` bucket at their scheme's key; a copy on the app container's own disk does not count.

## Overview

This is the portfolio of `Marisol Andrade`, an independent product and brand designer. Its job is credibility: people evaluating Marisol for work read it, and the one thing a visitor is asked to do is send an email.

It holds one long, dark home route that introduces the person, their five disciplines and their work, and eleven long-form case studies, each its own route at the origin root. Eight case studies are articles with a chapter rail down the left; three are galleries. Four systems sit on top of that reading surface: a work index with filters and computed suggestions, a motion preference with three levels, a reading spine that remembers where a reader stopped, and one annotation layer that explains the site's own effects.

Behind it sits the studio, where the designer writes a case study, attaches its images, and publishes or withdraws it. Publishing is the one consequential act: a draft must be absent from the public site entirely, not hidden behind a flag the browser is trusted to honour.

There is no search, no comment, no like, no sharing button, no contact form, no page transition, no light theme and no payment. Reading needs no account. The genuinely hard part is motion that belongs to the visitor: every moving thing has a finished still state, and one setting governs all of it.

The site ships with no binary assets at all. Every still, film, grain and closing name is generated, and the same item always generates the same picture.

## User roles

Two roles, and an anonymous visitor who is neither.

| Role | Can do |
|---|---|
| anonymous visitor | Reads the home page, every published case study, the work index and the privacy page. Keeps reading positions and a motion level in their own browser only. **Cannot** save to a reading list, **cannot** reach the studio, and **cannot** read anything unpublished. |
| `reader` | Everything the anonymous visitor can, plus a reading list, reading positions and a motion level kept on their account and followed across devices. **Cannot** reach any studio route or studio endpoint, **cannot** read or change another account's reading list or preferences, and **cannot** read anything unpublished. |
| `designer` | Signs in at `/login`. Creates case studies, writes chapters, uploads images, previews a draft through the public templates, publishes and withdraws. Reads drafts and their images. The designer account is seeded and is never created through signup. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `reader` session to any `designer`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open and always creates a `reader`, however the request body is shaped; it can never create a `designer`. A reader's reading list and preferences are reachable only with that reader's own session.

Seeded accounts, each with the password `deku-demo-pw-2026`:

| Email | Role |
|---|---|
| `designer@example.com` | `designer` |
| `reader@example.com` | `reader` |
| `reader2@example.com` | `reader` |

## Core features

**1. The publish boundary.** Every case study is published or it is not. A case study that is not published is **absent** from every public response: absent from the home page's featured grid and work list, absent from `/work` and `GET /api/case-studies`, absent from every suggestion pair, and absent from every reading list read. A direct request for its address answers a not-found status with the site's own not-found page, which never names it and reveals nothing about whether it exists. Its images are refused to everyone who is not the `designer`. Publishing makes the listings, the address and the images readable in one act; withdrawing makes all of them unreachable again, immediately. The seeded draft `A Wearable That Knew When to Stay Quiet` at `/kestra-band` is the case to hold to. Saving a draft to a reading list is refused.

**2. Images live in the object store.** Every image and reel the designer uploads is stored in `minio`, the S3-compatible object store, at the key `case-studies/{case_study_id}/{sha256_of_bytes}.{ext}`, for example `case-studies/7/9f2a...d0.png`. The database row records where the bytes are; the bucket is where they are. Every media row carries its intrinsic width and height and a text alternative written by the designer. Two uploads of identical bytes to one case study resolve to one object. Images accept `image/png`, `image/jpeg` and `image/webp`, a reel accepts `video/mp4`, and any other type is rejected as invalid with nothing stored. A case study has at most one `hero` image and at most one `reel`; a new hero replaces the old one. Bytes are served by the app at `GET /api/media/{id}`, never from a publicly readable bucket.

**3. Publishing is refused for an incomplete case study.** Publishing is rejected, and the case study stays a draft, when it has no `hero` image, when any of its media has empty alternative text, or when a `product` case study has no chapter. The refusal is a client error whose `field` is `hero`, `alt_text` or `chapters`, and the banner reads `Add a hero image before publishing.`, `Every image needs alternative text before publishing.` or `Add at least one chapter before publishing.`

**4. The work index.** `/work` shows every published case study at once, with the label `Everything` and the heading `All Work`, in a grid or a list. It filters by client and by discipline and sorts by year or by name, and the whole state lives in the address: `?client=kestra,quitkit&discipline=systems&sort=year-asc&view=list`. A case study is listed only if it carries **every** selected client and **every** selected discipline, so two clients selected together always yield the empty state. Client tokens are `verity-biotics`, `kestra`, `mirror-lab`, `dusk-ritual` and `quitkit`; discipline tokens are `strategy`, `product`, `brand-creative`, `systems` and `spatial-experience`; sort tokens are `year-desc` (the default), `year-asc` and `title-asc`; view tokens are `grid` and `list`. Year ties, and the `title-asc` sort, order by index title from A to Z without regard to case. An unrecognised value is dropped field by field, the rest still applies, the address is rewritten to the corrected state and one line says so. A query string longer than `512` characters is ignored entirely. Every filter change is a history entry, so back and forward walk through filter states; a filter toggled twice in quick succession replaces its entry rather than adding one. Sort and view are remembered as preferences, under rule 10; filters are not.

**5. Suggestions are computed.** The two cards at the foot of a case study, and `GET /api/case-studies/{slug}/related`, are computed over the published case studies. A case study's tags are its client plus its disciplines. For case studies a and b, overlap is the size of their shared tags divided by the size of their combined tags, recency is `1 / (1 + |year(a) - year(b)|)`, and score is `0.75 * overlap + 0.25 * recency`. Slot one is the highest-scoring other case study; scores that are equal to four decimal places go to the slug that sorts first alphabetically. Slot two is chosen for coverage rather than similarity: it is never the current case study and never slot one, and the pair is chosen across the whole published set so that no published case study goes unsuggested and every published case study is reachable from every other in **at most four** suggestion hops. That must stay true after any publish or withdrawal. Worked examples for slot one over the seeded catalogue:

| Case study | Slot one | Score |
|---|---|---|
| `kestra-care` | `kestra-home` | `0.7917` |
| `verity-biotics-product` | `aging-model` | `0.6250` |
| `mirror-lab` | `dusk-ritual` | `0.3125` |
| `quitkit` | `dusk-ritual` (ties `verity-biotics-brand` at `0.3750`) | `0.3750` |

**6. The reading list.** A signed-in account saves a published case study to its reading list and removes it again. Saving the same case study twice leaves exactly one entry. The server remembers, per entry, the furthest point reached (`max_fraction`, from `0` to `1`, which never goes down), where the reader was when they left (`last_fraction`, which may go down), the chapters whose tops the reader has passed (`chapters_read`, which only ever grows), and `completed`, which is true exactly when `max_fraction` is at least `0.95`. Scrolling back up never un-reads a chapter. A progress write whose fraction is outside `0` to `1`, or which names a chapter the case study does not have, is rejected as invalid and changes nothing; progress for a case study that is not on the list is refused. When the designer adds or removes a chapter, every stored position for that case study is discarded: `last_fraction` becomes empty, `chapters_read` becomes empty, and `max_fraction` becomes the smaller of itself and `0.5`. Withdrawing a case study removes it from every reading list read.

**7. The reading spine.** The chapter rail marks chapters as unread, current or read. On a return to a case study that is partly read, a small card in the corner names the furthest chapter in `chapters_read` and offers `Take me back` to where the reader stopped; it appears only when the reader got past the first twentieth, has not completed it, left more than ten minutes ago and the chapters have not changed, and never when the reader arrived at a chapter address or the browser restored the position itself. It dismisses itself after ten seconds and does not return that session. The home page grows a `Carry on` band, listing up to three unfinished case studies with a thin rule filled to how far the reader got, and the band does not exist until something is partly read. A chapter counts as read only after the reader has spent two seconds inside it. `/reading-list` lists the saved case studies with the same rule and a `Take me back` action. For a signed-in reader all of this comes from the server; for an anonymous visitor it comes from their own browser and nothing leaves it. A visitor who has never been here sees none of it.

**8. Motion and comfort.** One setting with three levels, `Everything`, `Less` and `Nothing` (stored as `full`, `reduced` and `still`), governs every moving thing on every route and takes effect without a reload. It starts from the operating system's reduced-motion preference until the visitor chooses, and a change in that system preference applies at once while the visitor has not chosen. `Nothing` means every page arrives finished, not stopped: the three lit passages render at full brightness and unsplit, never stuck dim. A signed-in reader's choice is kept on their account and follows them; an anonymous visitor's is kept in their browser. The tilt permission question is asked once per device, a decline is honoured for as long as this browser may remember (for the session otherwise), and the preferences panel is the only way back.

**9. The annotation layer.** One frosted card component explains things on the page, in three kinds: `place`, `mechanism` and `note`. The city name in the about passage opens the `place` card and the section heading opens the `mechanism` card. A card that explains a number takes it from the same constant the animation reads, never from typed text: with the letter amplitude at `40`, the mechanism card's fourth line reads `startY(i) = -40 * curve(t)`. Each card's content is present in the page as its trigger's description, so it is available without opening anything. A reveal-all mode, off by default, underlines every explained element and lists the explanations above the footer under `Explained on this page`.

**10. A question about this browser.** A first visit with nothing kept adds nothing to the page: no card, no `Carry on` band, no resume card and no read marks. The page carries the question's markup, hidden, until it is answered, and the first time this browser has something to keep (a chapter passed, a motion level chosen, a sort or view changed), a small frosted card in the bottom corner shows it: `May this browser remember your place?`, with `Remember my place` and `Do not remember` at equal prominence. It never covers the page's content. The answer is a cookie named `reading_memory`, `yes` or `no`, lasting 180 days, set by `POST /api/consent`; once it exists the card is not rendered again, and the answer survives a reload. Until a visitor answers `yes`, the browser keeps reading positions, the motion level, the tilt answer and the work index's sort and view for the session only. A signed-in reader's server-side reading list is theirs regardless.

**11. Privacy.** `/privacy`, linked from the footer of every public page, states what the site keeps: for a reader account, the email, a hashed password, the reading list with its positions, and the motion level; in a browser that allowed it, reading positions, the motion level, the tilt answer, and the sort and view of the work index. It says `This site keeps no analytics and sends nothing to anyone else.`

**12. Every internal link resolves.** Every link on every public page that points inside the site leads to a page that answers, including the chapter anchors, `/work`, `/privacy`, `/login` and `/signup`. An anonymous request for `/reading-list` lands on `/login`.

**13. Forms reject invalid input inline.** Signup, sign-in, the studio's case-study form and its chapter form each reject invalid input with an error directly under the field, name that field, and write nothing. An invalid API request is rejected as a client error whose body carries `field`, naming the offending input.

**14. The studio.** `/studio` lists every case study on the left with the word `Published` or `Draft` beside it, and shows the selected one's detail on the right, where a draft is previewed through the public templates. Creating a case study opens its own route, `/studio/case-studies/new`, not a panel over the list. A new case study is always created as a draft; its `home_placement` defaults to `list`, and its `position` defaults to one after the last case study in that placement. The studio's top bar carries `Case studies`, `New case study`, `View site` and `Sign out`. Every save, publish and withdrawal answers with a banner at the top of the detail pane: `Saved as a draft.`, `Published. It is live at /kestra-band.` (with that case study's own slug), and `Withdrawn. /kestra-band no longer answers.` Every studio route and every studio write is refused to an anonymous visitor and to a `reader`.

**15. Security headers.** Every response, page or API, carries a strict transport security header and the content-type options header set to `nosniff`.

## User flow

| Route | Who reaches it | What is there |
|---|---|---|
| `/` | anyone | the seven-band home page; anchors `#hero`, `#featured`, `#about`, `#contact` |
| `/verity-biotics-product`, `/verity-biotics-brand`, `/aging-model`, `/vitality-score`, `/kestra-care`, `/kestra-home`, `/foundry-campaign`, `/foundry-dashboard`, `/mirror-lab`, `/dusk-ritual`, `/quitkit` | anyone | one published case study |
| `/work` | anyone | the work index, state in the query string |
| `/privacy` | anyone | what the site keeps |
| `/reading-list` | signed in | saved case studies and their progress |
| `/login`, `/signup` | anyone | sign in; create a `reader` |
| `/studio` | `designer` | the list and the detail pane |
| `/studio/case-studies/new` | `designer` | the create route |
| `/studio/case-studies/{id}` | `designer` | one case study, drafts included |
| anything else | anyone | the site's own not-found page, with a not-found status |

**Entry and redirects.** The home top bar carries four anchors, `Intro`, `Work`, `About` and `Contact`, and `Work` targets `#featured`, not the work list. An anonymous request for `/reading-list` or a studio route lands on `/login` and returns to the requested page after sign-in. A `reader` who requests a studio route sees `The studio is for the designer.` and no studio content. Signing out returns to `/`. A session that has expired mid-action sends the visitor to `/login` and the action is not applied. Pressing `Save to reading list` while signed out goes to `/login` and saves nothing. A case-study slug may never be one of the site's own words, `work`, `reading-list`, `privacy`, `login`, `signup`, `studio` or `api`, and the form refuses it.

**The refused reader.** Requests `/kestra-band` and receives the not-found page, which does not name the draft. Requests the draft's hero image and is refused. Tries to save it and is refused. Calls a studio endpoint and is refused, with nothing written.

**The prospective client.** Opens `/`; the tiles drift and the name inverts as they pass. The philosophy passage lights up letter by letter. Opens `See all eleven`, selects `Systems`, sees two case studies, opens `/foundry-dashboard`, moves down its rail, and at the foot follows the first suggestion.

**The returning reader.** Signs in as `reader@example.com`. The home page shows `Carry on` with `/kestra-care` and a rule filled to where they got. Opening it, the rail shows its first two chapters as read, and the corner card says `You were in The platform.`; `Take me back` glides there.

**The reader who saves.** Signs up, opens `/foundry-dashboard`, presses `Save to reading list`, moves half way down, and later opens `/reading-list` on another device to find the entry with its progress.

**The visitor who wants stillness.** Opens the preferences panel from the slider icon and picks `Nothing`. Every passage is lit and unsplit, the tiles stand at rest, the films show posters and the cursor dot is gone. A reload keeps it.

**The designer publishes.** Signs in as `designer@example.com`, opens `/studio`, opens `/studio/case-studies/new`, types `work` as the slug and is told directly under the slug field `That address belongs to the site. Choose another.`, fixes it, saves (`Saved as a draft.`), adds a chapter, uploads a hero image with its alternative text, and publishes. The case study now appears on `/` and at `/work`.

**The designer withdraws.** Withdraws a case study from the work list and confirms once at `Withdraw this case study? Its address stops answering at once.` The home list renumbers from `01` with no gap, its address answers not-found, its image stops being served, and it drops out of every reading list and every suggestion.

**States.** The work index empty state reads `Nothing matches those two together. Clear the filters and start again.` with a `Clear filters` chip, and the heading and filter bar stay. An ignored parameter reads `One filter in that link was not recognised and has been dropped.` The reading list empty state reads `Nothing saved yet. Save a case study from its page and it waits here.` A route with no annotations says `Nothing on this page carries an explanation.` in the preferences panel. The work index has no loading state; filtering is immediate and thumbnails hold their box. Every error is a message on the page, never a crash.

## UI/UX notes

The north star: in the first moment a visitor should feel they have walked into a dark, quiet reading room where the work moves only because they do. The register is editorial: atmosphere is allowed, and the subject is always seen first. Brightness over colour, reading over browsing, stillness over performance.

**Motion.** Motion character is eased, and it belongs to the visitor: nothing moves on its own except five short muted films carried by five of the nine tiles behind the name, and every other transition happens because the visitor pointed, scrolled or chose. Three movement curves and no fourth: one leaves quickly and arrives slowly with no overshoot; one overshoots slightly and settles, reserved for small acknowledgements such as a pressed chip; one is slow at both ends and quick through the middle, used only when the three films open like a fan. Durations form a ladder rather than one house value: pointer-following is nearly instant, a pointer acknowledgement is quick, a colour change is the house default, an image's treatment takes a beat longer, and the portrait's warm-up is the slowest image change. Pictures never rest at full brightness, the portrait is the only fully grey image and the only one that warms into colour, and exactly one element grows under the pointer, the reel's play control. There are no page transitions and case-study copy arrives already at full contrast.

**Accessibility.** Every piece of text that has to be read meets WCAG AA contrast against its ground; the rail labels at rest, the two small corner links and the tilt gate's decline are raised to a light neutral already in the ramp to get there. Full keyboard navigation reaches every control, with a visible focus ring in the primary ink, offset from the element and legible on every ground; hover never substitutes for it. The icon-only links carry labels that exist for the keyboard and for assistive technology even when they are not painted. Split passages keep their whole sentence as the accessible text and hide the individual letters. Hero films are decorative and silent, every player shows its poster first. Every control has a comfortable touch target on a phone. Meaning is never carried by colour alone.

**Responsive.** The layout holds at every viewport width across three tiers, desktop, tablet and phone, with no breakpoint that loses a navigation target. There is no hamburger, drawer or overflow menu at any width.

**Palette by role.** The whole site is near-black neutral grounds and neutral inks, and hierarchy is carried by brightness alone. The page is a near-black neutral; the hero, philosophy, about and punchline bands sit one step lighter; cards sit one step lighter again; the palette chips on the brand routes sit a step darker than the page, so a brand's own colour has a neutral hole to sit in. The work band is the one surface with a trace of warmth, a near-black neutral leaning warm, and it appears once; flattening it to the page tone loses the one warm band on the page. Primary ink is a near-white neutral; the home route's accent is a near-white warm neutral, warmer than the case-study accent, so the tone set belongs to each document rather than to the whole site. Body text sits at a light neutral, labels and captions at mid neutrals, decoration at deep neutrals. Exactly two meaning-carrying colours exist, and only inside the frosted cards: a light, vivid green for eyebrows and the location pin, and a near-white, soft blue for named quantities; they never leak into the page. There is no accent, no brand hue, and no success or error colour in the chrome. Every link sets its own colour, so the browser's default mid, vivid blue appears on nothing, neither as text nor as a border. Hairlines and dividers are a deep neutral. The mail link and `[ EMAIL ]` rest at the primary ink and brighten to the pure near-white on hover. The exact shades are yours, so long as those relationships hold.

**Type.** A display serif, `PPEditorialNew`, carries the brand in italic; a neo-grotesque, `PPNeueMontreal`, carries headings and body; `Courier New` carries labels. Editorial type scales with the window and functional type does not. The hero name is larger on a tablet than on a laptop, deliberately.

**Density and shape.** Spacious: bands breathe, and the punchline sits alone in the emptiest band on the site. Corners are almost square.

**Components.** Inputs show the focus ring; a field's error sits directly under that field; every frosted card and the preferences panel close on `Escape` and return focus; `Withdraw` asks once before it acts.

## Front-end specification

### Grounds, inks and tokens

The ten grounds, darkest to lightest: the palette chip ground; the page and every case-study body; the hero, philosophy, about and punchline bands, the insight card; the brand highlight block; the callout, evidence and disclaimer cards and every player; the warm work band; the discipline card's hover ground; the motion gate's divider; the nav meter's unfilled track. Two translucent grounds: the frosted cards, a near-black at a little over half strength over a blur with boosted saturation, and the reel controls, a near-black at half strength over a lighter blur. The frosted card carries one two-part shadow: a wide soft drop, and a hairline inset highlight along its top edge that makes it read as glass rather than as a grey box. There is no other shadow on the site.

The inks, brightest to dimmest: pure near-white for the hero name, the meta values and the palette labels; the primary near-white; pull quotes; large-set passages at rest; the article body; secondary body and section labels; tertiary body; interactive at rest; recessive body; annotation body; annotation minimum; chrome minimum; decorative minimum.

The home route's accent and heading stack differ from the case-study routes', so the token set is declared per document. No transition is declared on every property of every element; each component declares its own transitions by property.

### Type

- Display: `PPEditorialNew`, weights `200` and `400`, italic. Fallback `"Times New Roman", Georgia, serif`. Where the display face is unavailable the italic serif fallback is the substitute, never a sans, at the same sizes.
- Heading and body: `PPNeueMontreal`, weights `300`, `400`, `500` and `700`, with section headings rendered at `800`. Fallback `sans-serif`; the home route adds `Host Grotesk` before the generic.
- Labels and annotations: `Courier New`, fallback `Courier, monospace`.

Sizes at the desktop width, with the rate that is normative: hero name `72px` (`5vw` on desktop, `10vw` on tablet so `99px` at 990 wide, `12vw` on a phone); section heading `72px` (`5vw`, `5vw`, `8vw`); case-study title `67.2px` (`4.667vw`, `5vw`, `9.846vw`); work-list name `48px` (`3.333vw`, `3.5vw`, `6vw`); punchline `43.2px` (`3vw`, `3vw`, `7vw`); philosophy passage `40.32px` (`2.8vw`, `2.8vw`, `6.564vw`); article heading `35.2px` (`2.444vw`, `2.5vw`, `5vw`); opening quote `28.8px`; about quote `22.4px` (`1.556vw`, `2vw`, `4.513vw`); article body `16px`, falling to `14.08px` on a phone; hero sub line `12px`. Functional sizes never scale: `16px`, `13.6px`, `12.8px`, `10.4px`, `9.6px`, `9.92px`, `8.8px`, `8.32px`, `8px`, `7.2px`. Line height is a ratio: `1.0` on the two largest headings, `1.2` on display headings and rail items, `1.35` on the punchline, `1.5` on large quotes, `1.75` on the about quote, `1.8` on body copy, `1.85` on the article body, `2.0` on mono annotations. Emphasis in an article is one step up in weight and brightness and nothing else.

### Iconography

Seven inline marks, no icon font, no icon file, each inheriting the current text colour so brightening a link brightens its mark. The play triangle, filled, on every player. The mail envelope, a rounded rectangle whose flap starts and ends exactly on its top corners. The professional-network card, a rounded square with two stems, a half-unit dot over the left stem drawn as a degenerate line so it takes the same stroke, and an arch. Three discipline marks, each primitive at its own strength: strategy, four bars of unequal length (the third longer than the second) each fainter than the last; brand and creative, a target whose outer ring is heavy and bright, whose middle ring is lighter in both stroke and strength, and whose centre dot is filled and bright; systems, four dots on the compass points joined by four lines, lit from above, so the bottom dot and the two lower lines are dimmer than the rest. The two remaining discipline cards, `Product` and `Spatial Experiences`, carry no mark rather than a guessed one. The preferences mark: two horizontal rails, each with a small ring on it at a different position. Discipline marks are decorative and hidden from assistive technology; the chrome marks are the accessible names of their links.

### Chrome

**Home top bar.** Fixed, transparent, above every band. The name `Marisol Andrade` at the left in the display serif at body size, drawn at seven tenths strength so it sits behind the four nav items despite being larger. Four nav items, `Intro`, `Work`, `About`, `Contact`, each a dot above a mono capital label above a thin track with a fill. The fill is a progress meter: it grows across the track as the visitor moves through that item's section, reads full for a section above the window and empty for one below, and the dot marks the active item. Three marks at the right: mail (label `Email`), network (label `Network`), and preferences; each brightens on hover while a small label rises into place beneath it, and the label finishes before the mark has finished brightening. On a phone the name leaves the layout, the nav moves to the left gutter and narrows, and the bar gets shorter.

**Case-study chrome.** Not fixed, over a soft fade from the page tone to transparent. `Back to portfolio` preceded by a left arrow at the left, the label `Case Study` at the right, and beside it the save control (`Save to reading list`, then `Saved`) and the preferences mark. Nothing else: no meter, no chapter list, no route name. On a phone, for a reader with a reading spine, a single hairline at its foot fills as they read.

**Cursor.** A small pale dot, centred on the pointer, above everything, following on the fastest duration while changing size and colour slowly. It is absent on any pointer that is not fine and at `Nothing`.

**Hover preview.** Pointing at a work-list row lifts one preview image that follows the pointer and fades in and out quickly; one element on one layer, absent on coarse pointers and at `Nothing`.

**Footers.** The case-study footer is one mono line, `All rights reserved`, at the right, with the `Privacy` link. The home footer is contact, then the closing name, then two copyright lines at the bottom right, with the `Privacy` link.

### Motion runtime and scroll

One scroll source feeds every scroll-driven effect, and one motion source feeds every animated component; components subscribe to both and never read either once and remember it. At tablet and desktop widths the scroll glides to a stop instead of stopping dead, and the root element says so; on a phone the platform's own scrolling is left alone. Anchor jumps, the restored position on returning to the home page, and the resume card's jump all go through the smoothing layer and never around it, and the jump waits until the document has settled at its final height. All scroll-driven work runs in one frame loop that reads layout first and writes second, and nothing writes to an element that has no layout box, including the phone-only cards on a desktop.

Every animated subsystem declares its still state, and these are the still states:

| Effect | At `Nothing` |
|---|---|
| hero tiles | their rest positions, no movement |
| lit passages | every character at full brightness, unsplit |
| heading letters | settled |
| phone card pictures | centred in their frames |
| reel control frosting | the shallower blur |
| nav meters | filled to the visitor's real position, updated when a scroll ends |

| Subsystem | `Everything` | `Less` | `Nothing` |
|---|---|---|---|
| hero tiles | drift at their rates | held at rest | off |
| lit passages and heading letters | on | final state, no travel | off, finished |
| smoothing layer | on at tablet and desktop widths, off on a phone | off | off |
| list entrance | rise and fade | fade only | off |
| films | muted loops | posters, play on request | posters, play on request |
| image hover treatment | on | on, at half duration | instant |
| reel | on | on | on, frosting fixed |
| cursor dot | on for fine pointers | on | off |
| rendering surface | on | a static frame | off |

A subsystem without a still state is not finished.

### The hero

A full-window band holding a field of nine tiles on a three-by-three naming grid (top, middle and bottom rows; left, centre and right) and the text layer. The tiles span a factor of eight in area, the largest on the bottom row, and four are cropped at rest by the window's edges (the top-left and bottom-left past the left edge, the top-right and middle-right past the right, and the bottom-left and bottom-centre past the bottom), so the field reads as a window onto something larger rather than a contact sheet. Each tile carries the barest corner softening. Five tiles are muted looping films, the top left, top centre, middle centre, bottom left and bottom right, and the other four are stills.

As the page scrolls each tile travels upward faster than the page by its own rate: middle centre `1.10`, middle left `0.90`, middle right `0.75`, top centre `0.60`, bottom centre `0.50`, bottom left `0.40`, top right `0.35`, top left `0.30`, bottom right `0.25`. The middle row is the fast row, the bottom row is the slow row, and the biggest tiles move least, which reads as depth rather than shear. Each tile chases its target and never quite catches it, settling a beat after the scroll stops; a field fixed rigidly to the scroll position is wrong.

The name, `Marisol Andrade`, sits in a clipping line box shorter than its own type so it rises into place from below on load, and it composites by difference against the drifting tiles, so it inverts as they pass. Under it, three role words, `Founder`, `Designer` and `Artist`, separated by middle dots, and two mono lines, `I build experiences at the intersection` and `of art, science and tech.` These three rise and fade in once on load.

A transparent, full-window rendering surface sits above every home band and below the chrome, home route only, and is never needed to read the page. It draws a single dark, low-poly plane gently displaced by two summed waves, lit from the upper left, whose phase advances with scroll and which tilts toward the pointer or the handset by a few degrees at most. At `Less` it is a static frame; at `Nothing` it is off. On a phone and at `Less` and `Nothing` the tiles are stills only; a tile outside the window has no film attached, and every tile shows its still before its film is ready.

A full-window tilt gate appears only where device orientation exists and is permission-gated: eyebrow `Device Motion` and `Permission Request` joined by a middle dot, title `This site moves with you.`, body `The hero images respond to how you hold and tilt your phone. Allow motion access to experience the full effect.`, the actions `Enable Motion` and `Skip`, and under them `You can change this any time in preferences.` The decline is as legible as the accept. Where orientation does not exist the gate never renders and the tiles follow the pointer instead.

### The lit passages and the settling heading

Three passages light up one character at a time against scroll: the philosophy passage, the about passage and the punchline. Every character rests dimmed, never hidden, at twelve hundredths strength, and highlighted words rest at fifteen hundredths. As a leading edge moves through the passage, a character's progress is its distance behind the edge divided by the window width, clamped between none and all, and its strength is the rest value plus the remainder times the square of its progress, so the visible edge sits about a third of the way into the window. The window is set from the rendered type size: `18.27` characters for the philosophy passage and `6.44` for the about passage, so the glow covers the same distance on the glass. Highlighted words switch to the italic display serif at the same size and step up to the primary ink, and they are whole words: `carefully crafted experiences` and `natural and alive` in the philosophy passage, `part founder, part designer, part artist` in the about passage, and `Art`, `taught me`, `to` and `see` in the punchline. Each passage keeps its whole sentence as its accessible text, finding a phrase that spans two characters still matches, selecting it returns continuous text, and at `Nothing` it is never split at all. Only the passage nearest the window carries a compositing hint, and no more than `64` elements carry one at any moment.

Section headings settle letter by letter: each letter starts pushed down by the letter amplitude, `40`, times the absolute cosine of its position across the word, so the two ends start lowest and the middle barely moves, and all of them rise home together as the heading's scroll progress completes. The ends land first and the middle follows; it is not a left-to-right cascade.

### The home page

Seven bands on a near-black page, in order.

1. **Hero**, as above.
2. **Philosophy.** Label `What I Do`. The passage `I believe great products are not just engineered or designed, they are carefully crafted experiences. My work lives at the intersection of art, science, and technology, where art shapes form and emotion, science guides understanding, and technology quietly enables experiences that feel natural and alive.` on the left; on the right five discipline cards in two columns, the fifth alone on the third row. The card hover is the only ground change on the home page. The cards and their items:
   - `Strategy`: `Product Vision`, `Market & User Insight`, `Go-to-Market`, `Strategic Narrative & Storytelling`
   - `Product`: `Concept to Product`, `Product Design`, `Design Systems & Operations`, `Connected Hardware & IoT`
   - `Brand & Creative`: `Brand Architecture`, `Creative Direction`, `Visual Identity & Design`, `Motion & Video`
   - `Spatial Experiences`: `Retail Experiences`, `Brand Activation Design`, `Service Journey Design`
   - `Systems`: `AI-Native Workflow Design`, `Process & Ops Design`, `Org and Team Building`
3. **Featured.** Label `From Idea to Reality`, heading `Featured Work` (settling letters). Two rows of two cards with the band's gutter carried by the rows, not the band, the first row roughly sixty to forty and the second inverted. Each card: its image held slightly grey and dim until pointed at, when it warms and lifts; its index title; its client's label in capitals; its years, written as the start year and either the end year or `Active`, joined by a middle dot. The four published `featured` case studies in position order fill it.
4. **Work.** The warm band. Label `Selected work` with a trailing link to `/work` reading `See all` plus the published count in words, `See all eleven` for the seeded set, and the line `From products to brands to moving image, every project begins with an idea and ends with something better than the brief.` Then the numbered list of published `list` case studies in position order: a two-digit number computed at read time from `01` with no gap, the index title large and dim so the list reads as an index rather than seven headlines, and a tag line of the client label, the product label where there is one, and the discipline labels, separated by display-serif middle dots. The year is in the row and hidden. Rows enter once, rising and fading, the first two already in place and the rest following one after another.
5. **About.** Label `Beyond the Brief`, heading `About Me`. Four paragraphs:
   - `I grew up in Thanjavur, a city that runs on the quiet ambition of people who build things. My father was one of them. I inherited the instinct.`
   - `Curiosity is how I move through the world. A decade of building companies, designing products, talking to customers, and occasionally overthinking everything has given me a lens that's part founder, part designer, part artist. It's not a job title. It's simply how I see.`
   - `I draw inspiration from unexpected places. A street market in an unfamiliar city. A painting that's going wrong. A small family business that has quietly outlasted every trend. I travel whenever I can, not for the destinations but for the movement. Newness is where I do my best thinking.`
   - `I don't spend much time pitching what I can do. I make things and let them speak.`

   `Thanjavur` opens the `place` card. On the right a portrait, fully grey at rest and warming into colour on hover, then the label `What I've Been Building` and two roles, each the company in the sans, the title in the italic serif and the period in mono: `Verity Biotics`, `Co-Founder & Chief Product Officer`, `APR 2022 - FEB 2026` then `~4 YEARS`; `Kestra`, `Co-Founder & Chief Technology Officer`, `AUG 2015 - APR 2022` then `6 YEARS 8 MONTHS`. The two parts of each period are joined by a middle dot, and the rendered date ranges use a typographic dash where this brief writes a hyphen.
6. **Punchline.** A large, faint open-quote glyph over one centred sentence in the display serif: `Art taught me to see. Science taught me to question. Technology gave me a way to build. I have not stopped since.`
7. **Contact and footer.** Between hairlines, the lead `Always curious about new ideas.` in the italic serif, the address `hello@marisol.example.com` as text and as a mail link, and two stacked mono actions at the right, `[ EMAIL ]` and `[ NETWORK ]`, the second linking to `https://network.example.com/in/marisol-andrade`. Then the closing name, `Marisol Andrade`, drawn as a rendered surface in the heading sans at its heaviest weight, fitted so its width is a little more than the window's and cropped at both edges at every width, with the name also present as a heading behind it. Then the copyright lines `©2026 All rights reserved. Marisol Andrade.` and `Any reproduction, distribution, or use of the materials without permission is prohibited.`

When something is partly read, the `Carry on` band sits between the featured and work bands, on the featured ground: the label `Carry on`, up to three rows reusing the phone work row (thumbnail, title, subtitle, index) with a thin rule filled to the furthest point, and `Forget my place`, which clears all reading state for that browser or account.

On a phone the featured grid becomes four tall cards whose taller pictures slide inside their frames as the card passes, each tagged with the client and year and subtitled with the disciplines, and the work list is a plain list with a small thumbnail per row. Both versions are always in the page and one is switched off.

### Case studies

**Product template** (`/verity-biotics-product`, `/aging-model`, `/vitality-score`, `/kestra-care`, `/kestra-home`, `/foundry-campaign`, `/foundry-dashboard`, `/mirror-lab`). A centred hero: the title in the display serif, the summary narrower than the title, and a meta row of three label and value pairs whose labels come from the content (`Company` or `Brand`; `Role`, `Focus` or `Format`; `Year` or `Period`). Then the full-width hero image, slightly grey and dim. Then the opening quote, large and quiet. Then the body: the chapter rail on the left and the article on the right.

The rail is sticky, lists the chapters present in the document, never assumes they start at one, and marks exactly one as current: the one whose top most recently passed a fixed line in the window. Each item is a mono capital label preceded by a short rule. Unread: a short, dim rule and a recessive label. Current: a long rule and the primary ink, one step heavier. Read: a short rule and label both at a light neutral. The rail is absent on a phone. Rail labels and article headings are different strings and both are carried.

Article blocks, each a closed kind: paragraphs; inline images that break the text column while their captions stay aligned to the image; image pairs, splits and trios; the callout card, with one of the labels `The idea`, `The workflow`, `The insight`, `User response`, `The real output`, `The Experience`, `User Story` or `AI coach in action` over a large quote; the evidence card, in seven slots, label, claim, a rule, a method list, an outcome label, an outcome list and a footnote, the rule separating what is asserted from what supports it; the insight card, a numbered stack of lines with one outlined button that inverts fully on hover; the attribution quote, a card with a small round portrait that links out, whose border is never the browser's link blue; and the disclaimer card, a sentence that links to a related case study. Then the more block: the label, `See all` at the right linking to `/work`, and the two computed suggestion cards. Then the footer.

**Brand template** (`/verity-biotics-brand`, `/dusk-ritual`, `/quitkit`). No rail and no chapters. The same hero and opening, then story blocks labelled `The foundation`, `The brief` or `The idea`; highlight blocks on their own slightly lighter ground carrying the argument in large italic display type; a palette strip of chips on the darkest ground, each chip labelled; a three-line type specimen; full-bleed images with small captions; and three named spacing steps that pace the gallery as content.

`/mirror-lab` also carries one highlight block, and `/verity-biotics-brand` also carries the disclaimer card.

**Media.** `/foundry-campaign` carries the reel: a poster-framed player with play, pause and restart controls; only play shows at rest, and pause and restart are revealed by playback, not by hover. Pointing at play grows it slightly and darkens its ground, and its frosting deepens as the player nears the middle of the window. The same route carries the video trio: three items in a row, and the one pointed at takes space from the other two over the slowest duration on the site, the row keeping its width while it redistributes. Three inline players on other routes carry only the play control. Wide media reach past the text column while their captions stay with the media, and on a phone they sit at column width.

Chapters, anchors, rail labels and article headings:

| Route | Anchor | Rail label | Article heading |
|---|---|---|---|
| `/verity-biotics-product` | `s1` | `The belief` | `The belief we started with` |
| | `s2` | `What we built` | `What we were building` |
| | `s3` | `Design as strategy` | `Design as a strategic decision` |
| | `s4` | `When people held it` | `What happened when people held it` |
| | `s5` | `What we learned` | `What this taught us about trust` |
| `/kestra-care` | `s1` | `The pivot` | `The pivot that set the direction` |
| | `s2` | `The platform` | `A platform, not a feature` |
| | `s3` | `Track trace act` | `Track, trace and act` |
| | `s4` | `The AI coach` | `An AI coach in the pocket` |
| | `s5` | `One designer` | `One designer across the whole stack` |
| | `s6` | `What it became` | `What it became in the end` |
| `/mirror-lab` | `s1` | `The concept` | `A shop that starts with a question` |
| | `s2` | `The experience` | `Ten minutes, start to finish` |
| | `s3` | `The diagnostics` | `Diagnostics without a clinic` |
| | `s4` | `What this proved` | `What the pilot proved` |
| | `s5` | `The model` | `A model other stores can run` |
| `/aging-model` | `s1` | `The question` | `The question prevention cannot answer` |
| | `s2` | `The model` | `Building a model that looks ahead` |
| | `s3` | `What it showed` | `What the model showed people` |
| `/vitality-score` | `s1` | `The noise` | `Too many signals, not enough sense` |
| | `s2` | `One number` | `Designing one number worth checking` |
| | `s3` | `Earning trust` | `Earning trust in a score` |
| | `s4` | `What moved` | `What moved when people used it` |
| `/kestra-home` | `s1` | `The house` | `A house that had never been wired` |
| | `s2` | `The hub` | `One hub for every room` |
| | `s3` | `The installers` | `Designing for the installers first` |
| | `s4` | `The app` | `An app for the whole household` |
| | `s5` | `The families` | `What families actually asked for` |
| | `s6` | `The scale` | `Growing to thousands of homes` |
| | `s7` | `What it left` | `What it left behind` |
| `/foundry-campaign` | `s4` | `Three audiences` | `Three audiences, three anxieties` |
| | `s5` | `The engine` | `A lightweight creative engine` |
| | `s6` | `The reel` | `One reel for every channel` |
| | `s7` | `The trio` | `Three films, one system` |
| | `s8` | `What it made` | `What the engine made` |
| `/foundry-dashboard` | `s1` | `The brief` | `Six weeks and a blank page` |
| | `s2` | `The workflow` | `An AI-assisted workflow` |
| | `s3` | `The guardrails` | `Guardrails that kept the quality` |
| | `s4` | `The build` | `Building in the open` |
| | `s5` | `The review` | `Review as a daily habit` |
| | `s6` | `The launch` | `Launching on schedule` |
| | `s7` | `What it changed` | `What it changed about how we build` |

Each chapter is reachable at its anchor, for example `/foundry-campaign#s4`, and `/foundry-campaign` has no `s1`. Chapter body copy is yours to write, two to four paragraphs per chapter in the voice of the copy below.

Case-study titles, summaries and opening quotes (a route without an opening quote shows none):

| Route | Title | Summary | Opening quote |
|---|---|---|---|
| `/verity-biotics-product` | `Designing Trust in Preventive Health` | `Health data is fragmented and hard to interpret. We used design to make it coherent, understandable, and trusted.` | `The hardest thing about building in preventive health is that we had to prove the category exists before the product could even be considered.` |
| `/verity-biotics-brand` | `Where Art Meets Science` | `The Verity Biotics brand identity was built on a single belief: that science and art are not opposites. One explains the world. The other makes it felt.` | `Biology is beautiful. Most health brands forget that. We built one that did not.` |
| `/aging-model` | `Beyond Biological Age` | `How we built a multimodal biological aging model that went beyond standard biomarkers to show users not just where they were, but where they were heading.` | `Prevention is a hard thing to quantify. How do you know you prevented a disease you never got?` |
| `/vitality-score` | `Making Health Scores Work` | `How a single daily score turned a dozen health signals into one number people could act on.` | none |
| `/kestra-care` | `Turning disconnected health data into daily decisions` | `Kestra Care was a full-stack holistic wellness platform built by one designer, from biomathematical fatigue models to AI lifestyle coaching.` | none |
| `/kestra-home` | `The Smart Home Built For Placeland` | `Kestra Home was a connected home system designed from the wiring up for how families in Placeland actually live.` | none |
| `/foundry-campaign` | `Using AI to Build a Creative System` | `Foundry needed to reach three different audiences with three different anxieties about their health. This is how we built the creative system that did it.` | `Traditional content is slow and expensive. We built a lightweight creative engine instead.` |
| `/foundry-dashboard` | `Using AI to rethink the way we build` | `How the Foundry dashboard went from idea to production in six weeks, and the AI-assisted development workflow we built to make it possible.` | `The question was never whether AI could help us build faster. It was whether we could build a process that kept the quality intact.` |
| `/mirror-lab` | `A Retail Experience That Turns Health Into Action` | `Mirror Lab is a physical wellness experience that compresses diagnostics, insight, and personalised commerce into a single ten-minute visit.` | `Health decisions are not made in clinics. They are made where action is easy.` |
| `/dusk-ritual` | `Designing a brand for better sleep through intentional rituals` | `Dusk Ritual is a premium wellness brand built around the idea that better sleep begins before you close your eyes, and that every part of the evening is part of it.` | `Most sleep brands treat sleep as a problem to fix. We built one that treated it as a ritual to return to.` |
| `/quitkit` | `Quit Like a Badass. Not a Patient.` | `Quitkit was built to make quitting look cool, sound cool, and feel like a choice you made for yourself, not one made for you by a doctor.` | `Quitting is not weakness. It is the hardest thing some people will ever do. We decided it should look like it.` |

Brand highlight statements. `/verity-biotics-brand`: `We're here to empower the change makers.`, `A System, Not Just a Symbol`, `Tech and luxury in the same breath.`, `The Gene Art is the soul of the visual identity.`, `No agency. No branding experience. Just the people who understood it most.` `/dusk-ritual`: `Colour as context. Everything else as constant.`, `A quiet invitation into a nightly journey.`, `Dusk Ritual is a behaviour design system for sleep.` `/quitkit`: `The voice came from the culture, not above it.`, `Bold type. Minimal colour. Maximum presence.`

The catalogue, which is also what the work index, the filters and the suggestions read:

| Slug | Index title | Client | Product | Disciplines | Year | Ends | Template | Placement |
|---|---|---|---|---|---|---|---|---|
| `verity-biotics-product` | `Designing Trust in Preventive Health` | `verity-biotics` | `The Body Ledger` | `strategy`, `product` | `2022` | `Active` | product | featured 1 |
| `kestra-care` | `Turning Disconnected Health Data Into Daily Decisions` | `kestra` | `Kestra Care` | `strategy`, `product` | `2020` | `2023` | product | featured 2 |
| `kestra-home` | `The Smart Home Built For Placeland` | `kestra` | `Kestra Home` | `strategy`, `product` | `2015` | `2021` | product | featured 3 |
| `mirror-lab` | `A Retail Experience That Turns Health Into Action` | `mirror-lab` | none | `brand-creative`, `spatial-experience` | `2025` | `Active` | product | featured 4 |
| `verity-biotics-brand` | `Where Art Meets Science` | `verity-biotics` | none | `brand-creative` | `2022` | none | brand | list 1 |
| `aging-model` | `Beyond Biological Age` | `verity-biotics` | `The Body Ledger` | `product` | `2023` | none | product | list 2 |
| `foundry-campaign` | `Using AI to Build a Creative System` | `verity-biotics` | `Foundry` | `brand-creative`, `systems` | `2024` | none | product | list 3 |
| `foundry-dashboard` | `Using AI to Rethink the Way We Build` | `verity-biotics` | `Foundry` | `product`, `systems` | `2025` | none | product | list 4 |
| `vitality-score` | `Making Health Scores Work` | `kestra` | `Vitality Score` | `product` | `2021` | none | product | list 5 |
| `dusk-ritual` | `Designing a Brand for Better Sleep` | `dusk-ritual` | none | `brand-creative` | `2024` | none | brand | list 6 |
| `quitkit` | `Quit Like a Badass. Not a Patient.` | `quitkit` | none | `brand-creative` | `2023` | none | brand | list 7 |

Client labels: `Verity Biotics`, `Kestra`, `Mirror Lab`, `Dusk Ritual`, `Quitkit`. Discipline labels: `Strategy`, `Product`, `Brand & Creative`, `Systems`, `Spatial Experience`. Filter chips are the labels of the values carried by at least one published case study, so a chip never leads to nothing on its own.

### The work index

`/work` carries the label `Everything`, the heading `All Work`, and a filter bar under it: the label `Narrow it down`; a group `Who it was for` of client chips; a group `What kind of work` of discipline chips; three sort chips, `Newest first`, `Oldest first` and `By name`; two view chips, `Grid` and `List`; and a count, `11 projects` for the seeded set, `1 project` for one. Chips are outlined, mono and small; a pressed chip inverts fully to the primary ink ground, and pressing one gives a small overshooting acknowledgement. The grid view repeats the featured card pairs; the list view repeats the work-band rows with the year shown at the right in mono. When results change, rows fade and rise; on first paint they enter one after another; on a sort change they move to their new places. At `Less` and `Nothing` all of that is instant.

### Overlays and the annotation layer

All frosted cards share one shell: the translucent near-black ground over a saturated blur, the two-part shadow, barely rounded corners, a hairline divider, the green eyebrow, and a layer above every page element except the cursor. One is open at a time, and opening a second closes the first, out and then in, never crossfaded.

- **`place`** (the city): pin `Location`, eyebrow `Pronounced as`, the name as the three syllables `Than`, `ja` and `vur` joined by middle dots in the display serif, the location `City in Tirunelveli, Placeland`, a divider, the line `I call it the city of entrepreneurs`, and the coordinates `11.0000 N` and `76.0000 E` in the soft blue.
- **`mechanism`** (the heading): eyebrow `// under the hood`, title `This might look like a simple animation, here's what's actually going on.`, a divider, six mono lines with named quantities in the soft blue and trailing comments in the primary ink: `n = total letters in heading`; `t = i / (n - 1)` with `// 0 to 1 across letters`; `curve(t) = abs(cos(t * pi))` with `// U-shape`; `startY(i) = -40 * curve(t)`; `currentY(i) = startY(i) * (1 - p)`; `p = scroll progress` with `// 0 to 1`. The footer reads `edges land first`, `middle follows` and `pure math`, joined by middle dots.
- **`note`**: eyebrow `// note`, a divider, and one body block.

Trigger and dismissal: with a fine pointer, a card opens after a short intent delay on hover and closes after the same delay when the pointer leaves both trigger and card; with a touch, a tap opens it and a tap outside or on the trigger closes it; with the keyboard, focus opens it and blur or `Escape` closes it. Placement: below the trigger, aligned to its left edge; flipped above if it would cross the bottom; right-aligned if it would cross the right; clamped to the gutter if it would cross the left; never covering its own trigger, and otherwise centred at the foot of the screen at full width minus the gutter, which is also the phone presentation. A card whose trigger leaves the page closes at once. An annotation that names a missing record or constant renders nothing at all. At `Nothing` cards appear and disappear without fade or travel.

**Preferences panel**, opened from the slider mark on every route: eyebrow `// preferences`, title `How much should move?`, a divider, three full-width level buttons `Everything`, `Less` and `Nothing` as a radio group with the selected one inverted, a one-line help under them (`The full site, as it was designed.`, `Things arrive without travelling. Scrolling is plain.`, `Every page arrives finished. Films wait to be asked.`), a tilt button where the interface exists (`Use device tilt`, or `Device tilt is on`), a reveal-all switch `Show what is explained`, and a footer line: `Kept in this browser only.`, or `This browser will not let us remember. It applies for now.` when the browser refuses. A signed-in reader's choice is also kept on their account.

**Resume card**: the shell anchored bottom left, eyebrow `// where you stopped`, title `You were in` followed by the rail label of the furthest chapter in `chapters_read` and a full stop, a divider, `Take me back` and `Start again`. It takes focus when it appears unless the reader has already scrolled, and `Escape` dismisses it and returns focus.

**Browser question**: the shell anchored bottom left, eyebrow `// this browser`, title `May this browser remember your place?`, body `Only where you stopped reading and how much you want things to move, kept here and nowhere else.`, and the two equal buttons `Remember my place` and `Do not remember`.

### Accessibility details

Contrast replacements: the rail labels at rest, `Back to portfolio`, `See all` and the tilt gate's decline all rise to the light neutral used for secondary body text; the small `Case Study` label stays dim because it is decoration, not a control. The focus ring is a thin outline in the primary ink, offset from the element, on every ground. Every one of the site's hover changes has a keyboard-focus equivalent and is inert on a coarse pointer. The filter chips are toggles in a named group that report their pressed state, and the count is announced politely when it changes. The reveal-all switch announces its state. The hero films carry no audio track and are marked decorative; any film with speech carries captions.

### Terms used in this brief

A short glossary, each term stated as what a visitor sees. **Parallax rate**: pictures moving at different speeds as you scroll, so some rush past and some linger. **Trailing lag**: the pictures settle a beat after the scroll stops instead of being fixed to it. **Lit passage**: a paragraph lighting up left to right with a soft leading edge. **Still state**: what a moving thing looks like with movement switched off, always its finished look. **Frosted card**: a card you can see the page through, blurred like glass. **Difference blend**: the name inverting as pictures pass behind it. **Rail**: the chapter list pinned beside an article that keeps up with where you are. **Reserved box**: an image's space held before the image arrives, so nothing jumps. **Fine pointer** and **coarse pointer**: a mouse or trackpad, as opposed to a finger. **Furthest point** and **last point**: how far a reader ever got, which only moves forward, and where they were when they left.

### Generating every asset: the zero-asset substitution

No binary ships. Every still is drawn from a seed taken from its own identifier, so the same slot always draws the same picture and no two slots match: a two-stop gradient at a seeded angle between two of the near-black grounds, one soft radial highlight at a seeded position in a deep neutral, and grain over it, then the same resting treatment a real photograph gets, in the same box with the same corner softening. The grain is an inline turbulence pattern, fine, over four octaves, fully desaturated and laid over at a low strength. A hero tile's film is its still with the highlight drifting on a slow loop, and there is no film element at all on a phone. A player's poster is its still, and playing it runs a twelve-second generated loop in which the highlight travels and the grain is redrawn; every player keeps its full controls against that loop. The trio is three stills at three seeds with no playback. The portrait is a still at a portrait seed with a soft vertical vignette, and the grey-to-colour hover is kept for the day a real photograph replaces it. The social preview image is generated from the same recipe. The fonts are named and never shipped; the site must read correctly on the fallback stacks alone.

The images the app generates for the seeded case studies are written once, on first start, to the bucket, as each case study's `hero`, with the case study's index title as the alternative text. An uploaded photograph replaces the generated one and nothing else changes.

## Technical requirements

The portfolio is rendered on the server and arrives as complete pages; the motion, the filters, the panel and the cards are layered on top of pages that already read. `Flask` renders those pages through `Jinja` templates and also answers the JSON API under `/api` on the same origin, and `Alpine.js` drives the interactive layer in the browser. With scripting unavailable, the home page and `/work` still list every published case study, every case study still carries its chapters, headings and blocks, the three passages read as ordinary sentences, and each annotation's text is present as its trigger's description.

`PostgreSQL`, reached through `DATABASE_URL`, holds the accounts, the case studies with their disciplines and chapters, the media rows, the reading lists and the preferences. Image and reel bytes, uploaded or generated, are written to `minio`, an S3-compatible store: connect at `STORAGE_ENDPOINT`, write into the bucket named by `STORAGE_BUCKET`, and authenticate with `STORAGE_ACCESS_KEY` plus `STORAGE_SECRET_KEY`. Signing in uses an email and a password the app itself checks; passwords are stored hashed, and sign-in returns an `access_token` for API clients and also sets the same session as an HttpOnly, Secure cookie; the server accepts either `Authorization: Bearer` or that cookie, so server-rendered pages and image requests know who is asking. Once the site is ready to serve, `GET /api/health` answers `200`. Each request the server handles writes a single line to stdout.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor; the only backing services available in this environment are `PostgreSQL` and `minio`, and reaching for anything else is a contract violation. Every host, port, key and password the portfolio uses is read from its environment variable at start-up; none is typed into the source. Both stores are already up when the portfolio boots.

**Security headers.** Every response carries `Strict-Transport-Security` and `X-Content-Type-Options: nosniff`.

**Media serving.** Image and reel bytes reach a browser only through the app, at `GET /api/media/{id}`, which streams them to anyone for a published case study and only to the `designer` for a draft. The bucket is never made publicly readable, and no presigned address is ever issued for a draft's media to anyone but the designer.

**Nothing identifying leaves a browser.** For an anonymous visitor, reading positions, the motion level, the tilt answer and the work index's sort and view stay in that browser, under one stored envelope with one version number: a version mismatch or a parse failure discards the whole envelope rather than migrating it, a failed write carries on for the session, and writes are spaced at least half a second apart and flushed when the page is hidden. Filters are never stored; they live in the address. No credential, key or token belonging to the server appears in anything the browser downloads. The running site calls nothing outside this environment and carries no analytics.

**The hero is the budget.** Every tile shows its still at once and swaps to its film only when the film is ready; a tile outside the window has no film attached; below the tablet edge and at `Less` and `Nothing` no film is attached at all. Every image and film reserves its box before its bytes arrive, so nothing moves after first paint. Anything below the first screen loads as it approaches, and large stills decode without interrupting a reveal. At most `64` elements carry a compositing hint at any moment, each added when its passage or tile comes within a screen of the window and removed when its animation settles, and none at `Nothing`. All scroll-driven work runs in one frame loop per page. Script on the home route stays under `805,638` bytes. The product must stay responsive with the seeded content and with a few thousand reading-list rows.

## Data model

Seven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**accounts.** An `id`, an `email` that is unique and compared without regard to case, a `password_hash`, a `role` that is one of `designer` or `reader`, and a `created_at`.

**case_studies.** An `id` that is stable and opaque and is never derived from the title or the slug; a `slug` that is unique, made of lowercase letters, digits and single hyphens, three to sixty characters long, and never one of the site's own words; a `title` (the page heading); an `index_title` (the label on the home page and the work index); a `summary`; an `opening_quote` that may be empty; a `template` that is one of `product` or `brand`; a `client` that is one of the five client tokens; a `product` label that may be empty; a four-digit `year`; a `year_end` that may be empty and is never before `year`; an `ongoing` flag that is never set together with a `year_end`; a `home_placement` that is one of `featured` or `list`; a `position`; a `published` flag; a `published_at` that is empty while unpublished and stamped on publishing; and a `created_at`. The two-digit work-list number, the tag line, the featured year caption and the suggestion pair are derived at read time and never stored.

**case_study_disciplines.** An `id`, a `case_study_id`, a `discipline` that is one of the five discipline tokens, and a `position`. Every case study carries at least one, and none twice.

**chapters.** An `id`, a `case_study_id`, an `anchor` that is `s` followed by digits and unique within its case study, a `rail_label`, a `heading`, a `body`, and a `position`.

**media.** An `id`, a `case_study_id`, a `role` that is one of `hero`, `still`, `poster` or `reel`, a unique `object_key`, a `content_type`, a `byte_size`, a `sha256` of the bytes, a `width` and a `height` that are never empty, an `alt_text`, and a `created_at`. The object key is `case-studies/{case_study_id}/{sha256_of_bytes}.{ext}`.

**reading_list.** An `id`, an `account_id`, a `case_study_id`, a `saved_at`, a `max_fraction`, a `last_fraction` that may be empty, a `chapters_read` list of anchors, and a `last_seen`; `completed` is computed on read from `max_fraction`. One entry per account and case study.

**preferences.** An `id`, an `account_id` that is unique, a `motion_level` that is one of `full`, `reduced` or `still` or is empty, a `level_source` that is one of `system` or `chosen`, a `reveal_all` flag, and an `updated_at`.

**Invariants, as properties of the running system.**

- A case study that is not published is absent from every public listing, from the home page, from every suggestion pair and from every reading list read; a public read of its slug answers not-found; its media bytes are refused to anyone who is not the `designer`. Publishing makes all of these readable in one act; withdrawing makes them unreachable again.
- The two-digit work-list numbers over the published `list` case studies run from `01` with no gap and no repeat, before and after any publish or withdrawal.
- An object key is unique, and two uploads of identical bytes to one case study resolve to one object.
- Saving the same case study twice leaves one `reading_list` row. `max_fraction` never decreases, `chapters_read` never loses an anchor, and `completed` is true exactly when `max_fraction` is at least `0.95`.
- Adding or removing a chapter empties `last_fraction` and `chapters_read` and caps `max_fraction` at `0.5` on every `reading_list` row for that case study.
- Choosing a motion level stores it with `level_source` `chosen`; sending an empty level hands control back and stores `level_source` `system`. A reader who never chose reads back `level_source` `system` and an empty `motion_level`.
- A refused write writes nothing at all: no row, no partial row, no object.

**Seed data.** The three accounts listed in `## User roles`. The eleven published case studies of the catalogue in `## Front-end specification`, with their titles, summaries, opening quotes, clients, products, disciplines, years, templates, placements and positions, and the chapters in the chapter table. One draft: slug `kestra-band`, title and index title `A Wearable That Knew When to Stay Quiet`, client `kestra`, discipline `product`, year `2019`, template `product`, placement `list` after the seven, chapters `s1` (`The quiet`, `Designing for the hours nobody watches`), `s2` (`The band`, `A band that knew when to stay quiet`) and `s3` (`What it taught`, `What the band taught us`). Every seeded case study, the draft included, carries one generated `hero` image stored in the bucket at its scheme key, whose alternative text is the case study's index title. `reader@example.com` has `kestra-care` saved with `max_fraction` `0.4`, `last_fraction` `0.35`, `chapters_read` `s1` and `s2`, and a `last_seen` one day before first start. `reader2@example.com` has nothing saved. No preferences are seeded.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One designer. No team, no organisation, no second tenant, no designer signup.
- No search, no comments, no likes, no sharing, no newsletter, no chat, no payment.
- No contact form of any kind: the site converts on one mail link and one network link.
- No light theme and no theme switch; the site is one theme by design.
- No page transitions; navigating between routes is a full page load.
- No cookie banner beyond the one question about what this browser may keep, and no consent manager.
- No third-party analytics, no tracking identifier, and no external network call at run time.
- The build ships zero binary assets. Every still, film, grain, closing name and social image is generated, and the licensed fonts are named, never shipped.
- Two discipline marks are deliberately absent rather than invented.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
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

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password` (at least `8` characters) | the created `reader` and an `access_token` |
| `POST /api/auth/login` | `email`, `password` | the account and an `access_token` |
| `GET /api/me` | none | the signed-in account: `id`, `email`, `role` |
| `GET /api/health` | none | a health object |
| `POST /api/consent` | `choice`, one of `yes` or `no` | the stored choice, and sets the `reading_memory` cookie |
| `GET /api/case-studies` | optional `client`, `discipline` (comma-separated tokens), `sort` | a top-level array of published case studies: `slug`, `title`, `index_title`, `client`, `product`, `disciplines`, `year`, `year_end`, `ongoing`, `template`, `home_placement` |
| `GET /api/case-studies/{slug}` | none | one published case study with `summary`, `opening_quote`, `chapters` (each `anchor`, `rail_label`, `heading`) and `media` (each `id`, `role`, `alt_text`, `width`, `height`) |
| `GET /api/case-studies/{slug}/related` | none | a top-level array of exactly two published case studies, slot one first, whenever at least three are published, and otherwise every other published case study |
| `GET /api/filters` | none | `clients` and `disciplines`, each an array of `token` and `label` carried by published case studies |
| `GET /api/media/{id}` | none | the object's bytes |
| `GET /api/reading-list` | none | a top-level array of the caller's entries, newest first: `slug`, `title`, `saved_at`, `max_fraction`, `last_fraction`, `chapters_read`, `completed`, `last_seen` |
| `POST /api/reading-list` | `slug` | the entry |
| `DELETE /api/reading-list/{slug}` | none | an empty success |
| `PUT /api/reading-list/{slug}/progress` | `fraction`, `chapters` (an array of anchors) | the updated entry |
| `GET /api/preferences` | none | `motion_level`, `level_source`, `reveal_all` |
| `PUT /api/preferences` | `motion_level` and or `reveal_all` | the stored preferences |
| `GET /api/studio/case-studies` | none | a top-level array of every case study, published or not, with `id`, `slug`, `index_title`, `published` |
| `POST /api/studio/case-studies` | `slug`, `title`, `index_title`, `summary`, `template`, `client`, `disciplines`, `year`, optional `product`, `opening_quote`, `year_end`, `ongoing`, `home_placement`, `position` | the created case study, unpublished, with its `id` |
| `GET /api/studio/case-studies/{id}` | none | one case study in full, drafts included |
| `PATCH /api/studio/case-studies/{id}` | any editable field | the updated case study |
| `POST /api/studio/case-studies/{id}/chapters` | `anchor`, `rail_label`, `heading`, `body` | the created chapter |
| `DELETE /api/studio/chapters/{id}` | none | an empty success |
| `POST /api/studio/case-studies/{id}/media` | multipart: the `file`, `role`, `alt_text`, `width`, `height` | the created media row with its `object_key` |
| `POST /api/studio/case-studies/{id}/publish` | none | the published case study |
| `POST /api/studio/case-studies/{id}/unpublish` | none | the case study, back to draft |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error whose body carries `field` where an input is at fault, never as a server error and never as a silent success. Authentication, by bearer token or the session cookie, is required on everything except signup, login, health, consent, the public case-study reads, the filters and the media of published case studies. A draft's address and a draft's data answer not-found to everyone but the designer.

### No mocks

`minio` is where the bytes live. An in-memory buffer the app hands back to itself, a file written to the app container's own filesystem, a base64 column in `PostgreSQL`, a hardcoded object key pointing at nothing, or a bucket opened to the public are each a contract violation however good the upload form looks. `PostgreSQL` is where the reading list lives for a signed-in reader: a browser-only copy for an account does not count. The named provider is the fact: the app's own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger scrolls the dark home page, narrows `/work` to one discipline, opens a case study, saves it, and later returns signed in to the chapter where they stopped; with `Nothing` chosen, every page arrives finished, fully lit. The draft at `/kestra-band` reaches nobody outside the studio, on any path, and its image is never served; publishing makes it readable in one act.
