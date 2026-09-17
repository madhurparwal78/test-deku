# Checklist: Tempo

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 678
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` One deployed site serves the manual, the example catalogue, the section library, the paid route, the member profiles, the changelog, the magazine, with the pages served from one origin `src: Overview`
- [ ] `C-OV-02` `constraint` Nothing a visitor reads sits behind a signup wall: the manual, the gallery grid at every facet combination, a free example's source, the section library, the changelog, the magazine are open to a visitor with no account `src: Overview`
- [ ] `C-OV-03` `capability` Every numeral the copy quotes about the size of the catalogue is counted from the catalogue rather than typed into a template `src: Overview`
- [ ] `C-OV-04` `constraint` Two places quoting one count never disagree, because both read the same query `src: Overview`
- [ ] `C-OV-05` `constraint` A paid example's file source is absent from every response that reaches a reader holding no licence, by every address `src: Overview`
- [ ] `C-OV-06` `constraint` An entitlement the app cannot resolve refuses rather than allows, so an unresolvable licence never reads as bought `src: Overview`
- [ ] `C-OV-07` `ui` A refusal to a paid reader says the licence is unresolved rather than looking like the offer to buy, so a refused paid example reads apart from an unbought one `src: Overview`
- [ ] `C-OV-08` `constraint` A framed preview runs a stranger's animation beside a signed-in session, so the frame is served without the session cookie `src: Overview`
- [ ] `C-OV-09` `constraint` A project a member submits stays absent from every public response until the maintainer publishes `src: Overview`
- [ ] `C-OV-10` `constraint` The ground is the laboratory dark under a warm off-white ink, with no light colour scheme for the product chrome `src: Overview`
- [ ] `C-OV-11` `capability` The three audiences reach one funnel ending at the example grid, where a count line states how many examples matched `src: Overview`
- [ ] `C-OV-12` `constraint` The declared stack serves every page from one process, so no second service is introduced for any of the surfaces named here `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` One role, `member`, whose permission shape is ownership plus entitlement, so one member cannot read another member's rows `src: User roles`
- [ ] `C-RL-02` `role` A member reads every public route: the manual for each runtime, the gallery narrowed by runtime or by category over the whole catalogue, the section library, the theme file, the paid route, any member's public profile, the changelog, the magazine `src: User roles`
- [ ] `C-RL-03` `role` A member buys lifetime access once, which creates one licence `src: User roles`
- [ ] `C-RL-04` `role` A member saves an example, saving twice leaves one stored row, unsaves an example, submits a showcase project `src: User roles`
- [ ] `C-RL-05` `role` A member reads a paid example's source only when holding the licence `src: User roles`
- [ ] `C-RL-06` `role` A member cannot read another member's saved rows `src: User roles`
- [ ] `C-RL-07` `role` A member cannot read another member's unpublished project, absent from every public response `src: User roles`
- [ ] `C-RL-08` `role` A member cannot publish their own submitted project `src: User roles`
- [ ] `C-RL-09` `contract` Authorization is enforced server-side on every mutating endpoint, so a direct API call from one member's session to another member's saved rows is rejected by the server rather than hidden by the interface `src: User roles`
- [ ] `C-RL-10` `contract` A rejected unauthorized request leaves the protected state unchanged, so a member cannot publish what the server refused `src: User roles`
- [ ] `C-RL-11` `capability` Signup is open from `/signup`, taking an email, a name, a handle, a password, refusing a duplicate of either unique field `src: User roles`
- [ ] `C-RL-12` `contract` The footer of every page links the privacy page, which states what is collected, plus the terms page `src: User roles`
- [ ] `C-RL-13` `literal` Three accounts are seeded, every one stored once with the password `deku-demo-pw-2026` held hashed `src: User roles`
- [ ] `C-RL-14` `literal` The seeded account `member@example.com` is Nova Reyes at the handle `nova`, stored once with a hashed password `src: User roles`
- [ ] `C-RL-15` `literal` The seeded account `member2@example.com` is Kit Alvarez at the handle `kit`, stored once with a hashed password `src: User roles`
- [ ] `C-RL-16` `literal` The seeded account `member3@example.com` is Sol Danner at the handle `sol`, stored once with a hashed password `src: User roles`
- [ ] `C-RL-17` `data` The seeded rows for `member@example.com` hold the licence `tempo-plus-nova`, the saved examples `scroll-velocity` plus `parallax`, the published showcase project `Orbit Atlas`, the submitted showcase project `Field Notes` `src: User roles`
- [ ] `C-RL-18` `data` `member2@example.com` holds no licence, so nothing unlocks for that account on the next request `src: User roles`
- [ ] `C-RL-19` `data` `member3@example.com` holds no licence at seed, being the account whose purchase creates the billing key `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` `POST /api/v1/auth/signup` takes `email`, `name`, `handle`, `password`, creating one member `src: Core features`
- [ ] `C-CF-02` `contract` `POST /api/v1/auth/login` takes `email` plus `password`, answering with a bearer `token` beside the signed-in `member` `src: Core features`
- [ ] `C-CF-03` `contract` Every later call carries `Authorization: Bearer <token>`, with a missing token refused `src: Core features`
- [ ] `C-CF-04` `literal` A token expires 24 hours after issue, so an expired token is refused `src: Core features`
- [ ] `C-CF-05` `literal` A wrong password is refused with the message `Sign in failed` `src: Core features`
- [ ] `C-CF-06` `constraint` An unknown email is refused with the same message as a wrong password, so neither answer reveals whether the login exists `src: Core features`
- [ ] `C-CF-07` `constraint` A missing token, an unknown token, a token past expiry are all refused as unauthenticated `src: Core features`
- [ ] `C-CF-08` `constraint` Nothing an unauthenticated caller asked to change is changed: a missing token, an unknown token, an expired token are refused before any write `src: Core features`
- [ ] `C-CF-09` `literal` Passwords are stored hashed, so the seeded literal `deku-demo-pw-2026` works at login for every seeded account without appearing in any stored record `src: Core features`
- [ ] `C-CF-10` `capability` Signup refuses a duplicate email, naming the field, writing no second row `src: Core features`
- [ ] `C-CF-11` `capability` Signup refuses a duplicate handle, naming the field, writing no second row `src: Core features`
- [ ] `C-CF-12` `constraint` A handle is folded to one case before comparison, so `Nova` is the same handle as `nova` for signup `src: Core features`
- [ ] `C-CF-13` `ui` Signing in at `/login` as `member@example.com` with a wrong password shows the refusal message rather than a page that reads as a server failure `src: Core features`
- [ ] `C-CF-14` `capability` `/docs` is the index, `/docs/react` a runtime index, `/docs/react/use-spring` one page at the current release `src: Core features`
- [ ] `C-CF-15` `literal` The current release is `13.1.0`, named on any docs address carrying no version `src: Core features`
- [ ] `C-CF-16` `capability` A docs address without a version is never permanent: after a newer release is published the same address serves the newer page `src: Core features`
- [ ] `C-CF-17` `literal` `/docs/13.0.4/react/use-spring` names the release `13.0.4` rather than the current one, staying on the versioned address asked for `src: Core features`
- [ ] `C-CF-18` `literal` The three retained releases are `13.1.0`, `13.0.4`, `12.8.2`; any other version answers as not found `src: Core features`
- [ ] `C-CF-19` `capability` A runnable block on a docs page carries the release the source was last executed against, shown beside the block `src: Core features`
- [ ] `C-CF-20` `capability` A runnable block last executed against a release older than the page's own release is marked as such rather than presented as current `src: Core features`
- [ ] `C-CF-21` `constraint` An unknown runtime answers as not found rather than falling back to a runtime that exists `src: Core features`
- [ ] `C-CF-22` `constraint` A version outside the three retained releases answers as not found rather than falling back to the current release `src: Core features`
- [ ] `C-CF-23` `capability` Each docs page names the release the page's subject was introduced in `src: Core features`
- [ ] `C-CF-24` `literal` `use-spring` was introduced in `12.8.2`, which the page names `src: Core features`
- [ ] `C-CF-25` `contract` An address differing only by a trailing slash is not a second page: one of `/docs` or `/docs/` is canonical, the other answering with a permanent redirect `src: Core features`
- [ ] `C-CF-26` `contract` The canonical link element on the served docs page names the canonical slash form `src: Core features`
- [ ] `C-CF-27` `ui` The runtime chooser on `/docs` lists React, JavaScript, Vue `src: Core features`
- [ ] `C-CF-28` `ui` Opening `/docs/react/use-spring` shows a page naming the release `13.1.0` `src: Core features`
- [ ] `C-CF-29` `ui` Opening `/docs/13.0.4/react/use-spring` shows a page naming the release `13.0.4` instead `src: Core features`
- [ ] `C-CF-30` `ui` `/examples` is a grid of cards three across on the widest layout, with a filter row above the grid set in the mono family, uppercase `src: Core features`
- [ ] `C-CF-31` `capability` Filtering is a change of address: every facet combination has an address of its own, rendered on the server `src: Core features`
- [ ] `C-CF-32` `capability` Opening a facet combination address a second time produces the same grid in the same order, so the address is shareable `src: Core features`
- [ ] `C-CF-33` `literal` The four facets are `runtime`, `category`, `access`, `saved` `src: Core features`
- [ ] `C-CF-34` `literal` The three orderings are `newest`, `most-saved`, `title` `src: Core features`
- [ ] `C-CF-35` `literal` `/examples?runtime=react&category=hero-sections` serves only the examples existing for `react` that sit in `hero-sections`, which is the runtime facet narrowing the catalogue beside the category facet `src: Core features`
- [ ] `C-CF-36` `literal` `access=paid` serves the paid examples alone, splitting the paid ones from the free ones `src: Core features`
- [ ] `C-CF-37` `literal` `access=free` serves the free examples alone, splitting the free ones from the paid `src: Core features`
- [ ] `C-CF-38` `literal` `saved=1` serves the signed-in member's saved examples alone `src: Core features`
- [ ] `C-CF-39` `capability` `saved=1` asked for by a visitor who is signed out serves an empty grid stating the reason rather than refusing the address `src: Core features`
- [ ] `C-CF-40` `capability` The grid carries a count line stating how many examples matched, counted from the catalogue for that address `src: Core features`
- [ ] `C-CF-41` `constraint` The count line numeral is never typed into a template `src: Core features`
- [ ] `C-CF-42` `capability` The `title` ordering sorts alphabetically, the `most-saved` ordering sorts by the saves, the `newest` ordering sorts by the published date `src: Core features`
- [ ] `C-CF-43` `constraint` Ranking inside one of the orderings never depends on who is asking, so the `title` sort is the same for every reader `src: Core features`
- [ ] `C-CF-44` `capability` What has to be findable is an example's title, category, runtime, over which the header search trigger narrows the gallery `src: Core features`
- [ ] `C-CF-45` `ui` A free example's card opens the source, carrying no lock mark `src: Core features`
- [ ] `C-CF-46` `ui` A paid example's card seen by a reader holding no licence carries a lock mark in the meta bar, with an open action reading as an upgrade `src: Core features`
- [ ] `C-CF-47` `ui` A paid example's card seen by a reader holding the licence is indistinguishable from a free card `src: Core features`
- [ ] `C-CF-48` `ui` A saved card's save control is filled in the accent `src: Core features`
- [ ] `C-CF-49` `contract` A card states whether the source behind may be opened without the card being opened first `src: Core features`
- [ ] `C-CF-50` `capability` `/examples/<slug>` carries the framed stage running the example, the source in one tab per stored file, a meta bar, a related rail `src: Core features`
- [ ] `C-CF-51` `contract` The meta bar on an example page names the runtime, the category, whether the example is free or paid `src: Core features`
- [ ] `C-CF-52` `capability` Each source tab carries a copy control, whose bytes are the bytes in the panel `src: Core features`
- [ ] `C-CF-53` `constraint` An unknown facet value answers as not found rather than serving the unfiltered grid `src: Core features`
- [ ] `C-CF-54` `literal` `scroll-velocity` is one of the free examples the access facet splits from the paid ones, existing for all three runtimes `src: Core features`
- [ ] `C-CF-55` `literal` `parallax` is one of the free examples the access facet splits from the paid ones, existing for all three runtimes `src: Core features`
- [ ] `C-CF-56` `literal` `skeleton-shimmer` is free, existing for the `react` runtime plus `vue`, so the runtime facet narrows the catalogue to the pair `src: Core features`
- [ ] `C-CF-57` `literal` `floating-action` is free, existing for the `js` runtime alone, so the runtime facet narrows the catalogue to one `src: Core features`
- [ ] `C-CF-58` `literal` `ios-app-folder` is one of the paid examples the access facet splits from the free ones, existing for `react` alone `src: Core features`
- [ ] `C-CF-59` `literal` `ios-pointer` is one of the paid examples the access facet splits from the free ones, existing for `react` plus `js` `src: Core features`
- [ ] `C-CF-60` `literal` `ticker-marquee` is one of the paid examples the access facet splits from the free ones, existing for all three runtimes `src: Core features`
- [ ] `C-CF-61` `ui` Choosing the runtime `react` plus the category `hero-sections` in the filter row leaves the address carrying both facets, with the count line stating the smaller number `src: Core features`
- [ ] `C-CF-62` `ui` Opening that narrowed address a second time brings back the same cards in the same order `src: Core features`
- [ ] `C-CF-63` `ui` Opening `parallax` shows the framed stage, one source tab per file, the meta bar naming the runtime plus the category `src: Core features`
- [ ] `C-CF-64` `ui` Pressing the copy control on the first source tab reports that the source was copied `src: Core features`
- [ ] `C-CF-65` `capability` `/ui` is the section library landing, `/ui/<category>` one category, `/ui/<category>/<slug>` one section `src: Core features`
- [ ] `C-CF-66` `literal` Nine categories are seeded, each carrying an address segment, a name, a blurb, in a fixed order `src: Core features`
- [ ] `C-CF-67` `literal` The category `hero-sections` is named Hero sections, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-68` `literal` The category `pricing` is named Pricing, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-69` `literal` The category `navigation` is named Navigation, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-70` `literal` The category `testimonials` is named Testimonials, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-71` `literal` The category `page-transitions` is named Page transitions, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-72` `literal` The category `bento-grids` is named Bento grids, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-73` `literal` The category `stats-sections` is named Stats sections, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-74` `literal` The category `cta-sections` is named CTA sections, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-75` `literal` The category `footers` is named Footers, seeded in the fixed order the nine categories carry `src: Core features`
- [ ] `C-CF-76` `contract` Each of the nine seeded categories carries the blurb the brief pins for the category, reproduced without a word changed `src: Core features`
- [ ] `C-CF-77` `capability` Each category card carries a count badge reading how many sections are filed under the category, counted from the section catalogue `src: Core features`
- [ ] `C-CF-78` `constraint` The hero's section total is the same query as the catalogue action's total, so two places quoting one count cannot read a different number `src: Core features`
- [ ] `C-CF-79` `literal` Six sections are seeded: `editorial-stagger-hero` in `hero-sections`, `border-beam` in `cta-sections`, `confetti` in `cta-sections`, `command-palette` in `navigation`, `coverflow` in `testimonials`, `sheet` in `page-transitions` `src: Core features`
- [ ] `C-CF-80` `capability` One theme file holds twelve named values, from which every section resolves the section's own timing rather than carrying a timing of the section's own `src: Core features`
- [ ] `C-CF-81` `literal` The theme value `transitions.snap` carries stiffness `1218`, damping `70` `src: Core features`
- [ ] `C-CF-82` `literal` The theme value `transitions.ui` carries stiffness `305`, damping `33` `src: Core features`
- [ ] `C-CF-83` `literal` The theme value `transitions.gentle` carries stiffness `110`, damping `20` `src: Core features`
- [ ] `C-CF-84` `literal` The theme value `transitions.lively` carries stiffness `622`, damping `17` `src: Core features`
- [ ] `C-CF-85` `literal` The theme value `transitions.ambient` carries stiffness `43`, damping `13` `src: Core features`
- [ ] `C-CF-86` `literal` The theme value `stagger.tight` is `0.04` `src: Core features`
- [ ] `C-CF-87` `literal` The theme value `stagger.base` is `0.08` `src: Core features`
- [ ] `C-CF-88` `literal` The theme value `stagger.relaxed` is `0.15` `src: Core features`
- [ ] `C-CF-89` `literal` The theme value `travel.hover` is `4` `src: Core features`
- [ ] `C-CF-90` `literal` The theme value `travel.enter` is `24` `src: Core features`
- [ ] `C-CF-91` `literal` The theme value `travel.section` is `48` `src: Core features`
- [ ] `C-CF-92` `literal` The theme value `reducedMotion` is `"calm"` `src: Core features`
- [ ] `C-CF-93` `contract` Each of the twelve theme values is served with the kind the value belongs to `src: Core features`
- [ ] `C-CF-94` `capability` A section's own page names which of the twelve theme keys the section reads `src: Core features`
- [ ] `C-CF-95` `capability` A section's own page names the style tokens the section expects the buyer to have defined `src: Core features`
- [ ] `C-CF-96` `constraint` A section declaring what the section reads can be matched against a buyer's project before installation rather than afterwards `src: Core features`
- [ ] `C-CF-97` `ui` A five-tab strip sits beside the theme file, one tab per named transition, over a plot `src: Core features`
- [ ] `C-CF-98` `capability` The plot is drawn from the same spring solver the sections use, at the stiffness plus the damping in the theme file `src: Core features`
- [ ] `C-CF-99` `ui` All five curves are drawn at once as thin lines with the selected curve drawn thick `src: Core features`
- [ ] `C-CF-100` `ui` A square beside the plot moves with the selected transition, so a reader sees the curve alongside the feel of the curve `src: Core features`
- [ ] `C-CF-101` `constraint` A plot drawn from a hand-fitted curve rather than from the twelve served theme values would be a claim the product does not honour `src: Core features`
- [ ] `C-CF-102` `contract` One of `/ui` or `/ui/` is canonical, the other answering with a permanent redirect to the canonical slash form `src: Core features`
- [ ] `C-CF-103` `literal` The section library carries the version `0.0.2`, which is not the library's release, named by a changelog entry whose kind marks the entry as the section library's own `src: Core features`
- [ ] `C-CF-104` `ui` The nine category cards each carry a count badge reading the number of sections filed under the category `src: Core features`
- [ ] `C-CF-105` `ui` The theme panel shows the twelve named values as a source file with one active line marked `src: Core features`
- [ ] `C-CF-106` `ui` Pressing the tab named gentle on the spring strip redraws the plot with that curve thick over the other four, moving the square beside the plot with the same transition `src: Core features`
- [ ] `C-CF-107` `capability` Every example page carries a framed stage running the real thing rather than a recording `src: Core features`
- [ ] `C-CF-108` `capability` Every section page carries a framed stage running the real thing, naming the theme keys that section reads `src: Core features`
- [ ] `C-CF-109` `contract` The framed document is served from the app's own origin, granted script execution alone, with a content policy naming the app's own origin as the only destination the frame may reach `src: Core features`
- [ ] `C-CF-110` `constraint` The frame's policy denies form submission, top-level navigation, popups, downloads, so the rest is denied rather than allowed by omission `src: Core features`
- [ ] `C-CF-111` `constraint` The framed preview document is served without the session cookie `src: Core features`
- [ ] `C-CF-112` `constraint` Script inside the preview frame reads no session, no account, no saved row `src: Core features`
- [ ] `C-CF-113` `capability` A read of the member surface attempted from inside the preview frame is refused the way a request carrying no credential is refused `src: Core features`
- [ ] `C-CF-114` `constraint` The refusal the preview frame meets is observable rather than silent: the frame reports the refusal, the page states the refusal `src: Core features`
- [ ] `C-CF-115` `literal` A preview that has not reported itself ready within 5 seconds of wall clock is stopped, with the well stating that the preview did not start `src: Core features`
- [ ] `C-CF-116` `constraint` A stopped preview leaves the rest of the page usable `src: Core features`
- [ ] `C-CF-117` `literal` At most three previews run at once on one page, each preview served without the session cookie `src: Core features`
- [ ] `C-CF-118` `constraint` A preview leaving the viewport is destroyed rather than left running, with the well keeping the size the media will be so nothing shifts on return `src: Core features`
- [ ] `C-CF-119` `ui` The framed document is a nested browsing context with a title, which the keyboard can both enter plus leave `src: Core features`
- [ ] `C-CF-120` `ui` The section library's preview well runs one section at a time, with a shuffle control swapping a different section into the same well without the page moving `src: Core features`
- [ ] `C-CF-121` `ui` Opening `ios-app-folder` signed out leaves the stage running the example, with the source panel offering the upgrade instead of the source `src: Core features`
- [ ] `C-CF-122` `capability` `/plus` is the paid route, selling one product: one payment, one perpetual licence, lifetime updates, no renewal `src: Core features`
- [ ] `C-CF-123` `literal` The list price is `$249.00`, held as `24900` minor units with the currency `USD` `src: Core features`
- [ ] `C-CF-124` `constraint` Money is stored as integer minor units beside a currency code everywhere, never as a decimal fraction `src: Core features`
- [ ] `C-CF-125` `contract` Money returned by the read surface is integer minor units beside a currency code `src: Core features`
- [ ] `C-CF-126` `literal` Two price bands are seeded: the band `list` for the region `US` at `24900` with no reason `src: Core features`
- [ ] `C-CF-127` `literal` The band `ppp-south-asia` is seeded for the region `IN` at `14900` with the reason `Local discount applied` `src: Core features`
- [ ] `C-CF-128` `constraint` A price band is a row in the seeded table rather than a formula `src: Core features`
- [ ] `C-CF-129` `literal` The band applying to a request is resolved from the request header `X-Client-Region`, where `US` resolves to `list` `src: Core features`
- [ ] `C-CF-130` `literal` The region `IN` resolves to the band `ppp-south-asia` from the seeded table `src: Core features`
- [ ] `C-CF-131` `capability` A region with no row in the table resolves to the band `list` `src: Core features`
- [ ] `C-CF-132` `constraint` The price banner appears only when a band other than `list` applies `src: Core features`
- [ ] `C-CF-133` `contract` When the banner appears the banner carries the banded price beside the list price struck through, in the same currency, with the band's reason `src: Core features`
- [ ] `C-CF-134` `contract` When the band `list` applies there is no banner at all `src: Core features`
- [ ] `C-CF-135` `constraint` A banner claiming a discount over a purchase that charges the list price is a false statement about money, which is why the order records the band the banner showed `src: Core features`
- [ ] `C-CF-136` `ui` The purchase panel opens over the pricing board, leaving the board in place behind the panel `src: Core features`
- [ ] `C-CF-137` `capability` The purchase panel collects the buyer's display name plus the buyer's email address `src: Core features`
- [ ] `C-CF-138` `literal` A completed purchase creates a licence whose key is `tempo-plus-` followed by the buyer's handle, so the buyer `sol` receives `tempo-plus-sol` `src: Core features`
- [ ] `C-CF-139` `data` A completed purchase creates an order carrying the currency, the list amount, the discount amount, the total amount, the band code applied, the band's reason `src: Core features`
- [ ] `C-CF-140` `capability` The order records the band so the banner the buyer saw can be reconciled against what was sold `src: Core features`
- [ ] `C-CF-141` `contract` A completed purchase creates a billing account in the billing platform under the licence key as the account's external key `src: Core features`
- [ ] `C-CF-142` `literal` The billing account created by a purchase carries the buyer's display name, the buyer's email address, the currency `USD`, the country `US` `src: Core features`
- [ ] `C-CF-143` `contract` A completed purchase sends one receipt by mail to the buyer's address `src: Core features`
- [ ] `C-CF-144` `constraint` A repeated purchase for the same licence key is refused by the key's own uniqueness in the billing platform, answering with a conflict rather than by a guard in the application `src: Core features`
- [ ] `C-CF-145` `constraint` The refusal of a repeated purchase leaves one billing account, one licence, one order for the key `src: Core features`
- [ ] `C-CF-146` `constraint` A refused purchase sends no second receipt `src: Core features`
- [ ] `C-CF-147` `ui` The panel states that the licence already exists, naming the licence `src: Core features`
- [ ] `C-CF-148` `literal` A purchase requires an idempotency key, honoured for 24 hours, so the same key submitted twice returns the first outcome `src: Core features`
- [ ] `C-CF-149` `constraint` The second request carrying an idempotency key already used writes nothing, returning the first purchase outcome instead `src: Core features`
- [ ] `C-CF-150` `literal` The receipt's subject begins `Tempo+ receipt ` followed by the licence key `src: Core features`
- [ ] `C-CF-151` `constraint` The receipt reaches the buyer's inbox, nobody else, carrying no copied recipient, no blind-copied recipient `src: Core features`
- [ ] `C-CF-152` `contract` The receipt states the total amount, the currency, the band's reason where a band applied `src: Core features`
- [ ] `C-CF-153` `constraint` A purchase that was refused sends no mail at all `src: Core features`
- [ ] `C-CF-154` `ui` The panel closes onto a confirmation naming the licence key beside the total amount `src: Core features`
- [ ] `C-CF-155` `ui` The pricing board behind the closed panel shows the member as holding the licence rather than offering the purchase again `src: Core features`
- [ ] `C-CF-156` `capability` The total is computed on the server in minor units with the client mirroring the stored number `src: Core features`
- [ ] `C-CF-157` `constraint` On a mismatch the server total in minor units wins, the client re-renders from the stored number, the difference is logged `src: Core features`
- [ ] `C-CF-158` `ui` Opening `/plus` with no region header shows no discount banner, with the pricing board stating the price in dollars under the action Get instant access `src: Core features`
- [ ] `C-CF-159` `ui` The proof strip on the paid route carries MIT-licensed code, Lifetime updates, an example count equal to the gallery count line `src: Core features`
- [ ] `C-CF-160` `ui` Submitting the purchase panel as Sol Danner at `member3@example.com` shows a confirmation naming the licence `tempo-plus-sol` beside the total `src: Core features`
- [ ] `C-CF-161` `ui` Signing in as `member3@example.com` then opening the purchase panel over the pricing board leaves the board visible behind the panel `src: Core features`
- [ ] `C-CF-162` `capability` The licence unlocks the paid examples plus the paid documentation pages, nothing else in the product checking the licence `src: Core features`
- [ ] `C-CF-163` `constraint` A paid example's file source is absent from the example's own read address for a reader without the licence `src: Core features`
- [ ] `C-CF-164` `constraint` A paid example's file source is absent from the raw file's own address for a reader holding no licence, which refuses `src: Core features`
- [ ] `C-CF-165` `constraint` A paid example's file source is absent from the gallery listing served without the licence `src: Core features`
- [ ] `C-CF-166` `constraint` A paid example's file source is absent from the document the framed preview loads without the licence `src: Core features`
- [ ] `C-CF-167` `constraint` Absent means not in the response body: a source field present but emptied is not enough, nor is a source present in the markup hidden by a style `src: Core features`
- [ ] `C-CF-168` `ui` A reader signed out still sees the stage run, the meta bar, the category, the runtimes, the description, because the stage is the sales pitch `src: Core features`
- [ ] `C-CF-169` `contract` An entitlement claim is resolved from the licence row on every request, never trusted from the bearer token `src: Core features`
- [ ] `C-CF-170` `capability` A revoked licence stops unlocking on the next request rather than when a token expires `src: Core features`
- [ ] `C-CF-171` `constraint` Entitlement fails closed: an unresolvable licence produces a refusal rather than access `src: Core features`
- [ ] `C-CF-172` `contract` The refusal a reader meets after a failed resolution says the licence could not be confirmed, inviting a retry, which reads apart from the unbought offer to buy `src: Core features`
- [ ] `C-CF-173` `ui` The offer a reader meets after never having bought offers the purchase rather than a retry `src: Core features`
- [ ] `C-CF-174` `data` `member@example.com` holds `tempo-plus-nova`, so the source of `ios-app-folder`, `ios-pointer`, `ticker-marquee` is present in the response `src: Core features`
- [ ] `C-CF-175` `data` `member2@example.com` holds no licence, so the paid source is absent from every response that account receives, by every address `src: Core features`
- [ ] `C-CF-176` `ui` Opening `ios-app-folder` again after the purchase shows the source panel carrying the source rather than the upgrade action `src: Core features`
- [ ] `C-CF-177` `contract` `POST /api/v1/saved` carrying the example's slug writes one row for that member paired with that example `src: Core features`
- [ ] `C-CF-178` `constraint` The pair of member plus example is unique, so saving the same example twice leaves one stored row rather than an error `src: Core features`
- [ ] `C-CF-179` `contract` `DELETE /api/v1/saved/<slug>` removes the stored row for that example `src: Core features`
- [ ] `C-CF-180` `capability` The saved row survives a reload: opening the gallery again shows the card's save control still filled `src: Core features`
- [ ] `C-CF-181` `capability` Opening the member's own profile shows the saved example in the saved panel `src: Core features`
- [ ] `C-CF-182` `constraint` The example in the saved panel is the example the grid showed: the same slug, the same title, the same runtimes, which is the stored row matching the grid `src: Core features`
- [ ] `C-CF-183` `ui` The save control fills the moment the control is pressed, settling afterwards against the server's answer `src: Core features`
- [ ] `C-CF-184` `ui` A save the server refused returns the control to the previous state, stating the reason on the card rather than in a banner elsewhere on the page `src: Core features`
- [ ] `C-CF-185` `ui` The result of a save is announced politely rather than by moving focus `src: Core features`
- [ ] `C-CF-186` `capability` A save attempted with no session takes the visitor to sign in, carrying the example along, writing the row on arrival `src: Core features`
- [ ] `C-CF-187` `constraint` A save begun signed out completes after signing in without the visitor pressing anything a second time `src: Core features`
- [ ] `C-CF-188` `data` An example's saved count is the count of the example's stored saved rows, read from those rows `src: Core features`
- [ ] `C-CF-189` `capability` The `most-saved` ordering on the gallery reads the same stored count `src: Core features`
- [ ] `C-CF-190` `constraint` A member's saved rows are readable by that member alone `src: Core features`
- [ ] `C-CF-191` `constraint` `/@nova` seen by another member carries the published showcase with no saved panel, because the saved rows cannot be read `src: Core features`
- [ ] `C-CF-192` `constraint` Asking the read surface for another member's saved rows is refused `src: Core features`
- [ ] `C-CF-193` `ui` Pressing the save control on the `ios-app-folder` card in the gallery grid fills the control at once `src: Core features`
- [ ] `C-CF-194` `ui` Reloading the gallery leaves the save control on that card still filled `src: Core features`
- [ ] `C-CF-195` `ui` The profile at `/@sol` lists iOS App Folder in the saved panel `src: Core features`
- [ ] `C-CF-196` `ui` Pressing the save control on the `scroll-velocity` card when signed out brings the sign-in page `src: Core features`
- [ ] `C-CF-197` `ui` Signing in as `member2@example.com` returns the page with the `scroll-velocity` save control already filled `src: Core features`
- [ ] `C-CF-198` `capability` `/@<handle>` is a member profile carrying a striped dossier header, the published projects, the saved panel to the owner alone `src: Core features`
- [ ] `C-CF-199` `capability` The publish panel opens over the profile, collecting a title, a source address, a description `src: Core features`
- [ ] `C-CF-200` `capability` Submitting the publish panel writes a project in the state `submitted`, appearing in the owner's own list at once marked as awaiting a decision `src: Core features`
- [ ] `C-CF-201` `constraint` A submitted project is absent from the public profile `src: Core features`
- [ ] `C-CF-202` `constraint` A submitted project is absent from the homepage showcase tape `src: Core features`
- [ ] `C-CF-203` `constraint` A submitted project is absent from the response when the project's own address is asked for by anybody but the owner `src: Core features`
- [ ] `C-CF-204` `constraint` A project reaches the public list only in the state `published` `src: Core features`
- [ ] `C-CF-205` `constraint` A member cannot publish their own project: the move from `submitted` to `published` is a human review by the maintainer `src: Core features`
- [ ] `C-CF-206` `data` `nova` owns one published project, `Orbit Atlas`, plus one submitted project, `Field Notes` `src: Core features`
- [ ] `C-CF-207` `constraint` `/@nova` in a public response carries `Orbit Atlas` with the submitted project `Field Notes` absent `src: Core features`
- [ ] `C-CF-208` `constraint` An unknown handle answers as not found `src: Core features`
- [ ] `C-CF-209` `constraint` A handle is folded to one case before lookup, so `/@NOVA` reaches the same profile as `/@nova` `src: Core features`
- [ ] `C-CF-210` `contract` The dossier header carries the member's display name, the folded handle the profile is reached by, the date of joining, the member's links `src: Core features`
- [ ] `C-CF-211` `ui` A member with no published project gets the dossier header beside an empty state rather than a missing page `src: Core features`
- [ ] `C-CF-212` `ui` Opening `/@kit`, opening the publish panel, submitting a project titled Field Study with an address plus a description puts the project in the owner's list marked as awaiting a decision `src: Core features`
- [ ] `C-CF-213` `ui` The profile at `/@nova` lists Orbit Atlas without listing Field Notes `src: Core features`
- [ ] `C-CF-214` `capability` `/changelog` plus `/magazine` are the two dated feeds, with `/magazine/<slug>` one article `src: Core features`
- [ ] `C-CF-215` `constraint` Both dated feeds are ordered newest first by the published date, stating that ordering `src: Core features`
- [ ] `C-CF-216` `contract` A changelog entry names the release the entry belongs to beside the kind of change `src: Core features`
- [ ] `C-CF-217` `literal` The changelog entry `spring-presets` belongs to the release `13.1.0`, of the kind `feature`, introducing the five named transitions `src: Core features`
- [ ] `C-CF-218` `literal` The changelog entry `exit-animation-fix` belongs to the release `13.0.4`, of the kind `fix` `src: Core features`
- [ ] `C-CF-219` `literal` The changelog entry `pointer-gesture-fix` belongs to the release `12.8.2`, of the kind `fix` `src: Core features`
- [ ] `C-CF-220` `literal` The changelog entry `ui-registry-install` belongs to `0.0.2`, of the kind `release`, carrying a badge naming the section library rather than the library `src: Core features`
- [ ] `C-CF-221` `capability` A changelog entry links to the documentation at the release the entry names, in the permanent versioned form `src: Core features`
- [ ] `C-CF-222` `constraint` Following a changelog entry lands on a versioned docs address that stays on the release the address names `src: Core features`
- [ ] `C-CF-223` `literal` Three articles are seeded, each carrying an author handle: `springs-over-easing`, `the-all-problem`, `reduced-motion-is-not-no-motion` `src: Core features`
- [ ] `C-CF-224` `contract` Each article carries a title, a standfirst, an author handle, a published date, addressable on the article's own address `src: Core features`
- [ ] `C-CF-225` `constraint` An unknown article slug answers as not found `src: Core features`
- [ ] `C-CF-226` `capability` `/about` is the maintainer's page, a public route declaring a title plus a description of the route's own, written in the first person `src: Core features`
- [ ] `C-CF-227` `ui` Opening `/changelog` shows the newest entry naming `13.1.0`, with the section library entry carrying the badge reading `0.0.2`; `/magazine` then lists the three articles newest first `src: Core features`
- [ ] `C-CF-228` `constraint` A route that does not exist serves the not-found document rendered on the server, carried with the not-found status rather than a success status `src: Core features`
- [ ] `C-CF-229` `constraint` The not-found document for an unknown address is not rendered after the client boots `src: Core features`
- [ ] `C-CF-230` `ui` The not-found document carries the wordmark, a drawn figure, the label `PAGE_NOT_FOUND`, a link home `src: Core features`
- [ ] `C-CF-231` `contract` A favicon is served, referenced from the head of every document `src: Core features`
- [ ] `C-CF-232` `contract` Every route carries a meta description of the route's own, no two routes sharing one `src: Core features`
- [ ] `C-CF-233` `constraint` A description describing the site rather than the route is the same defect as no description `src: Core features`
- [ ] `C-CF-234` `capability` `/privacy` states what is collected, how long the record is kept, that nothing is shared, linked from the footer of every page `src: Core features`
- [ ] `C-CF-235` `capability` `/terms` states the licence the code is under, that the paid licence is perpetual, that nothing renews, linked from the footer of every page `src: Core features`
- [ ] `C-CF-236` `contract` Every response carries a security header set: a strict transport policy, a nosniff content type policy, a frame policy, a referrer policy, a content security policy `src: Core features`
- [ ] `C-CF-237` `constraint` No credential the server holds reaches anything the browser downloads: no database address, no billing key, no billing secret, no billing password, no mail host, no other member's stored token `src: Core features`
- [ ] `C-CF-238` `contract` A sitemap lists every public route, with the robots file pointing at the sitemap `src: Core features`
- [ ] `C-CF-239` `ui` Opening `/div` shows a document reading `PAGE_NOT_FOUND` beside a link home, with the turning wireframe figure alongside `src: Core features`
- [ ] `C-CF-240` `ui` The site root shows the header, the hero title carrying the brand word Tempo followed by a full stop, the kicker reading `v13.1.0` `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `ui` `/` serves the hero, the proof strip, the feature atlas, six example cards, the showcase tape, the changelog column, the magazine column `src: User flow`
- [ ] `C-UF-02` `contract` `/docs` serves the documentation index beside the runtime chooser `src: User flow`
- [ ] `C-UF-03` `contract` `/docs/<runtime>` serves one runtime index for `react`, `js`, or `vue`, an unknown runtime answering as not found `src: User flow`
- [ ] `C-UF-04` `contract` `/docs/<runtime>/<slug>` serves one page at the current release, naming that release `src: User flow`
- [ ] `C-UF-05` `contract` `/docs/<version>/<runtime>/<slug>` serves the same page at a named release, permanently `src: User flow`
- [ ] `C-UF-06` `contract` `/examples` serves the gallery grid, where every facet combination is a shareable address of the combination's own `src: User flow`
- [ ] `C-UF-07` `contract` `/examples/<slug>` serves the stage, the source panel with one tab per stored file, the meta bar, the related rail `src: User flow`
- [ ] `C-UF-08` `contract` `/ui` serves the section library landing, the preview well, the twelve theme values `src: User flow`
- [ ] `C-UF-09` `contract` `/ui/<category>` serves one category's sections, counted from the section catalogue `src: User flow`
- [ ] `C-UF-10` `contract` `/ui/<category>/<slug>` serves one section, the section's source, the theme keys the section reads `src: User flow`
- [ ] `C-UF-11` `contract` `/plus` serves the proof strip, the price banner that appears only when a band applies, the pricing board, the comparison table `src: User flow`
- [ ] `C-UF-12` `contract` `/@<handle>` serves a profile: the dossier header, the published showcase, the saved panel to the owner `src: User flow`
- [ ] `C-UF-13` `contract` `/login` serves sign in, `/signup` serves account creation `src: User flow`
- [ ] `C-UF-14` `contract` `/changelog` serves the changelog newest first, `/magazine` the magazine index newest first `src: User flow`
- [ ] `C-UF-15` `contract` `/magazine/<slug>` serves one article carrying the author handle beside the published date `src: User flow`
- [ ] `C-UF-16` `contract` `/about` serves the maintainer's page, `/privacy` the privacy page, `/terms` the terms page stating the licence `src: User flow`
- [ ] `C-UF-17` `contract` Any other address serves the not-found document rendered on the server with the not-found status `src: User flow`
- [ ] `C-UF-18` `capability` The front door is the site root, readable with no account, carrying the header above the hero title `src: User flow`
- [ ] `C-UF-19` `constraint` Nothing a visitor reads is behind a signup wall: the manual, the gallery grid, a free example's source, the section library, the changelog, the magazine are all open, because the free cards carry no lock mark `src: User flow`
- [ ] `C-UF-20` `capability` `/docs/` answers with a permanent redirect to `/docs`, `/ui/` with a permanent redirect to `/ui`, the canonical link element naming the canonical slash form `src: User flow`
- [ ] `C-UF-21` `capability` A visitor who is signed out asking for a member-only surface is sent to `/login` with the destination carried, arriving at that destination after signing in `src: User flow`
- [ ] `C-UF-22` `capability` A signed-in member asking for `/login` or `/signup` is sent to the profile the member's own folded handle reaches `src: User flow`
- [ ] `C-UF-23` `constraint` A member asking for another member's saved rows is refused rather than redirected, because a redirect would say the rows exist `src: User flow`
- [ ] `C-UF-24` `capability` Opening `/examples` shows every seeded example with the count line stating how many matched `src: User flow`
- [ ] `C-UF-25` `capability` Choosing a runtime plus a category in the filter row changes the address, the grid being re-rendered on the server for the new address `src: User flow`
- [ ] `C-UF-26` `capability` Copying the narrowed facet combination address into a second visit produces the same grid in the same order `src: User flow`
- [ ] `C-UF-27` `capability` Opening a card reaches the detail route, whose framed stage runs the example rather than a recording `src: User flow`
- [ ] `C-UF-28` `capability` The bytes the copy control puts on the clipboard are the bytes of the source in the panel `src: User flow`
- [ ] `C-UF-29` `capability` Opening a paid example with no account leaves the stage running, the source panel replaced by the upgrade action `src: User flow`
- [ ] `C-UF-30` `constraint` Asking for the raw file's own address of a paid example without the licence answers with a refusal rather than the source `src: User flow`
- [ ] `C-UF-31` `capability` With the region `IN` the banner shows the banded price with the list price struck through beside the reason `Local discount applied` `src: User flow`
- [ ] `C-UF-32` `capability` With the region `US` there is no banner, the pricing board showing the list price `src: User flow`
- [ ] `C-UF-33` `capability` Submitting the purchase panel writes the billing account keyed by the licence, records the order, sends one receipt `src: User flow`
- [ ] `C-UF-34` `capability` Submitting the same purchase again is refused because the licence key is taken, leaving one order beside one receipt `src: User flow`
- [ ] `C-UF-35` `capability` After the purchase the paid source panel carries the source, the paid cards losing the lock mark `src: User flow`
- [ ] `C-UF-36` `capability` Pressing the save control fills the control at once, the row being written, a reload showing the control still filled `src: User flow`
- [ ] `C-UF-37` `capability` Pressing save with no session takes the visitor to sign in, the save completing on arrival `src: User flow`
- [ ] `C-UF-38` `capability` Submitting a project from the publish panel puts the project in the owner's own list marked as awaiting a decision, absent from the public profile `src: User flow`
- [ ] `C-UF-39` `capability` Opening `/changelog` then following the newest entry reaches the documentation at that release, on an address that stays on the release named `src: User flow`
- [ ] `C-UF-40` `capability` Asking for `/div` brings the not-found document rendered on the server, carrying `PAGE_NOT_FOUND` beside a link home `src: User flow`
- [ ] `C-UF-41` `ui` Every surface that can be empty, unstarted, refused, or broken says which `src: User flow`
- [ ] `C-UF-42` `ui` An empty grid for a facet combination matching nothing says so, offering to clear the facets, rather than looking like a page that failed to load `src: User flow`
- [ ] `C-UF-43` `ui` A preview well that has not started holds exactly the size the media will be `src: User flow`
- [ ] `C-UF-44` `ui` A preview that did not start says so `src: User flow`
- [ ] `C-UF-45` `ui` A refused save returns the control, stating the reason on the card `src: User flow`
- [ ] `C-UF-46` `ui` A refused purchase states which licence key is taken `src: User flow`
- [ ] `C-UF-47` `contract` An entitlement that could not be resolved says the licence could not be confirmed, which is not the page an unbought example shows `src: User flow`
- [ ] `C-UF-48` `ui` A member's own empty saved panel keeps the heading beside an empty state rather than vanishing `src: User flow`
- [ ] `C-UF-49` `ui` A member's own empty showcase keeps the heading beside an empty state rather than vanishing `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The page ground is a near-black carrying a trace of green, with two deeper recesses below carrying the green removed `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The ink is a warm off-white, the secondary ink a neutral warm grey, a half-strength off-white carrying tab labels beside captions `src: UI/UX notes`
- [ ] `C-UX-03` `ui` A card sits one step above the ground, a card's border one step above the card `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Two colour systems resolve into one: a declared set of tokens on the root element is the source, the resolved values are what components read, nothing reaching for a third value `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The accent is set by one attribute on the root element, every accented surface reading that attribute `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The free library resolves the accent to amber `src: UI/UX notes`
- [ ] `C-UX-07` `ui` The paid route, the account routes, the member profiles resolve the accent to green `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A periwinkle blue is the tertiary accent, carrying the turning wireframe figure on the not-found document `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Failure is an orange-tinted red, which is what a refused save states on the card `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A ramp of six saturated colours named after fruit is declared on every route, every badge drawn from the ramp taking a one-tenth wash of the badge's own colour as the ground `src: UI/UX notes`
- [ ] `C-UX-11` `ui` The mono family carries every label, kicker, numeral, code fragment, badge, control on the site `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The sans family carries only what is read as a sentence, so a label set in the sans family reads as a mistake `src: UI/UX notes`
- [ ] `C-UX-13` `constraint` Both families are named with a fallback stack, neither shipping as a file, the fallback metric matched so the swap moves no line, which the declared stack serves from one process `src: UI/UX notes`
- [ ] `C-UX-14` `literal` Labels plus kickers are set at `10px` beside `11px` `src: UI/UX notes`
- [ ] `C-UX-15` `literal` Body prose is set at `12px`, `13px`, `14px`, `15px` in the proportional face, each at the line height measured for the size `src: UI/UX notes`
- [ ] `C-UX-16` `literal` Lead prose is set at `17px` in the proportional face `src: UI/UX notes`
- [ ] `C-UX-17` `literal` Headings are set at `19px` beside `23px` at the bold cut of the proportional face `src: UI/UX notes`
- [ ] `C-UX-18` `literal` An article card title is set at `22px`, a version numeral plus a newsletter lead at `30px`, an account heading at `32px`, a hero title at `44px`, a dossier title at `56px`, each carrying negative tracking of the role's own `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Uppercase mono labels are tracked out by an amount varying with the label's job, tightest on a preview control, loosest on the trust label `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Headings in the proportional face track the other way, negative, proportional to the size `src: UI/UX notes`
- [ ] `C-UX-21` `ui` The site is square: cards, buttons, inputs, thumbnails, panels carry no radius `src: UI/UX notes`
- [ ] `C-UX-22` `ui` The handful of radii that exist live only on dots, pills, terminal chrome, a tab strip `src: UI/UX notes`
- [ ] `C-UX-23` `ui` A hairline grid takes a one-pixel gap over a border-coloured ground with the cells painted in the card ground, so the gap becomes the rule with no border drawn on the feature atlas or the pricing board `src: UI/UX notes`
- [ ] `C-UX-24` `ui` Diagonal hatching at one consistent odd angle is stamped behind the primary action, the reading-route headers, the account frame, the catalogue thumbnails, the changelog version plate `src: UI/UX notes`
- [ ] `C-UX-25` `ui` The four hatch variants differ only in colour, stroke, period `src: UI/UX notes`
- [ ] `C-UX-26` `ui` A dot field, a ruler down the inside edges of a showcase plate, four blur radii each bound to one role, two shadows are the whole rest of the surface vocabulary `src: UI/UX notes`
- [ ] `C-UX-27` `ui` Depth is a closed set of seven stacking values across the whole site, the header taking the highest, no new one introduced `src: UI/UX notes`
- [ ] `C-UX-28` `ui` One house curve carries the wipes beside every clip reveal, rising almost at once, landing flat `src: UI/UX notes`
- [ ] `C-UX-29` `ui` A press curve, a colour curve, one symmetric curve are the only others, so no effect under the pointer invents a seventh `src: UI/UX notes`
- [ ] `C-UX-30` `constraint` Nothing under a pointer moves for longer than half a second, most things moving in about a fifth of one `src: UI/UX notes`
- [ ] `C-UX-31` `constraint` No transition is declared on every property at once: each one names the properties the transition animates, so no hover effect runs longer than the half second the house curve takes `src: UI/UX notes`
- [ ] `C-UX-32` `ui` Six hover moves exist, a seventh being a mistake: fade, invert ink against ground, wipe, brighten the border, underline, lift `src: UI/UX notes`
- [ ] `C-UX-33` `ui` Three infinite linear loops run on the homepage diagram layer at three lengths chosen not to be multiples of one another, so the loops in those cells drift apart `src: UI/UX notes`
- [ ] `C-UX-34` `ui` One shared timeline animates the three stacked homepage cards between two computed layouts without animating layout, so the three cannot fall out of step `src: UI/UX notes`
- [ ] `C-UX-35` `constraint` One frame loop exists in the whole document, every drawn canvas stopping when the canvas leaves the narrow viewport or the widest `src: UI/UX notes`
- [ ] `C-UX-36` `ui` Under reduced motion the three loops stop at the resting frame, every scroll-linked effect snapping to the end state, the wipe becoming a colour change with no travel, entrances becoming opacity alone `src: UI/UX notes`
- [ ] `C-UX-37` `constraint` Nothing carrying information is removed under reduced motion: a bar that fills still fills, filling at once `src: UI/UX notes`
- [ ] `C-UX-38` `literal` Four width thresholds ship, no more: `600px`, `760px`, `900px`, `1200px` `src: UI/UX notes`
- [ ] `C-UX-39` `ui` The capability queries stay beyond the four width thresholds: hover, pointer, reduced motion, colour scheme `src: UI/UX notes`
- [ ] `C-UX-40` `constraint` There is no light colour scheme: the partial one is deleted rather than half kept `src: UI/UX notes`
- [ ] `C-UX-41` `ui` Below `1200px` the content column follows the viewport, the gutters narrowing `src: UI/UX notes`
- [ ] `C-UX-42` `ui` Below `900px` the two-column bands stack, the feature atlas halving the columns `src: UI/UX notes`
- [ ] `C-UX-43` `ui` Below `760px` the pricing board stacks, the comparison table becoming one column `src: UI/UX notes`
- [ ] `C-UX-44` `ui` Below `600px` the navigation labels switch to the short forms, the hero actions going full width stacked, the showcase tape becoming a swipeable rail, the footer columns halving `src: UI/UX notes`
- [ ] `C-UX-45` `constraint` The short navigation labels are both present in the document with one hidden rather than swapped by script `src: UI/UX notes`
- [ ] `C-UX-46` `constraint` Every breakpoint is a layout change, none of them removing a control `src: UI/UX notes`
- [ ] `C-UX-47` `ui` Every control a touch pointer can reach is at least the platform's own minimum touch target, no behaviour depending on hover alone `src: UI/UX notes`
- [ ] `C-UX-48` `constraint` Every text pairing against a ground is measured against the contrast standard for the size of the text, raised where the pairing fails, the measurement recorded rather than eyeballed `src: UI/UX notes`
- [ ] `C-UX-49` `constraint` The two pairings to watch hardest for contrast are the muted warm grey behind body text at the small prose sizes in the feature atlas, plus the half-strength off-white on the card background at the tab-label size `src: UI/UX notes`
- [ ] `C-UX-50` `ui` Every interactive element has a visible focus indicator that is not the hover treatment `src: UI/UX notes`
- [ ] `C-UX-51` `constraint` The wipe is a hover effect, never a focus indicator `src: UI/UX notes`
- [ ] `C-UX-52` `ui` Keyboard navigation reaches every control in source order, the header being first in source order on every route `src: UI/UX notes`
- [ ] `C-UX-53` `ui` The framed preview can be both entered plus left by the keyboard `src: UI/UX notes`
- [ ] `C-UX-54` `ui` Every field has a real label element, no placeholder standing in for one `src: UI/UX notes`
- [ ] `C-UX-55` `ui` Every drawn figure carries a text alternative saying what the figure demonstrates rather than what the figure looks like `src: UI/UX notes`
- [ ] `C-UX-56` `ui` Every classification is carried as a badge letter set in the mono family beside the ramp colour, so the colour is reinforcement rather than the information `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Product routes carry the full navigation, a coloured hero band, a numbered section sequence: `/`, `/docs`, `/ui`, `/plus` `src: Front-end specification`
- [ ] `C-FE-02` `ui` Reading routes carry the compact navigation beside a striped dossier header: `/about`, `/@<handle>`, `/magazine/<slug>`, `/changelog`, `/privacy`, `/terms`, the not-found page `src: Front-end specification`
- [ ] `C-FE-03` `ui` Account routes carry no navigation at all, only the wordmark, so there is nothing to press except the form: `/login`, `/signup` `src: Front-end specification`
- [ ] `C-FE-04` `ui` One header ships, not two: the full navigation is the one kept, the compact variant being a shorter arrangement of the same component rather than a second treatment `src: Front-end specification`
- [ ] `C-FE-05` `ui` The header is sticky, takes the highest stacking value, sits inset from each side plus from the top, overlaying the hero on the routes that have one `src: Front-end specification`
- [ ] `C-FE-06` `ui` The header ground is the accent, the header ink the dark page ink `src: Front-end specification`
- [ ] `C-FE-07` `ui` Inside the header sit the brand lockup at the left, the link cluster, the action cluster `src: Front-end specification`
- [ ] `C-FE-08` `literal` Five navigation labels ride in the header: Docs, Examples, UI, Magazine, the paid action, set in the mono family, uppercase, tracked out `src: Front-end specification`
- [ ] `C-FE-09` `ui` Each navigation label is two stacked copies of the same word in a container clipped to one line height, the incoming copy parked one line above the resting one `src: Front-end specification`
- [ ] `C-FE-10` `ui` Hovering a navigation label translates the pair by one line so the outgoing word leaves upward as the incoming word arrives, both copies carrying identical text `src: Front-end specification`
- [ ] `C-FE-11` `constraint` The rolling label is a mechanical roll rather than a change of word `src: Front-end specification`
- [ ] `C-FE-12` `ui` The compact arrangement of the navigation does not roll: the links fade instead `src: Front-end specification`
- [ ] `C-FE-13` `ui` The search trigger is a square button holding the magnifier glyph, with no visible label, no painted shortcut hint `src: Front-end specification`
- [ ] `C-FE-14` `capability` The search trigger is reachable by keyboard, narrowing the catalogue by the runtime or the category matching the text typed in `src: Front-end specification`
- [ ] `C-FE-15` `ui` The primary action carries a second full copy of itself in inverted ink, parked entirely off the left edge as a degenerate parallelogram `src: Front-end specification`
- [ ] `C-FE-16` `ui` On hover the parked copy's clip expands to a parallelogram wider than the button, so the fill arrives as a diagonal edge travelling left to right at the slant of the wordmark bars `src: Front-end specification`
- [ ] `C-FE-17` `constraint` Both label copies swap ink at the moment the diagonal edge passes, so the text is never caught half inverted `src: Front-end specification`
- [ ] `C-FE-18` `ui` The primary action isolates itself so the wipe clips to the action `src: Front-end specification`
- [ ] `C-FE-19` `ui` Two variants of the primary action exist: a compact solid one in the header, a striped one on the reading routes plus the account form whose ground is the hatch, resting slightly under full opacity `src: Front-end specification`
- [ ] `C-FE-20` `ui` The footer is light rather than dark, the one place the ground inverts `src: Front-end specification`
- [ ] `C-FE-21` `ui` The footer opens with the sponsor band: a mono uppercase heading, a lead in the proportional face, an action with an arrow that moves on the arrow's own, a grid of six sponsor rows `src: Front-end specification`
- [ ] `C-FE-22` `ui` Each sponsor row carries an index numeral, a mark, a dotted leader, the leaves-the-site glyph `src: Front-end specification`
- [ ] `C-FE-23` `literal` Six sponsors are named in the footer, set in the mono family: Prism, Caret, Vector, Keyed, Figment, Verity `src: Front-end specification`
- [ ] `C-FE-24` `ui` The newsletter band's field carries a real label element even where the label is visually hidden `src: Front-end specification`
- [ ] `C-FE-25` `ui` The footer column set carries the privacy page beside the terms page, halving the columns on the narrowest layout `src: Front-end specification`
- [ ] `C-FE-26` `ui` The section heading is one component used on every numbered band: a two-digit mono index, a kicker in the accent, a heading in the proportional face, a lead `src: Front-end specification`
- [ ] `C-FE-27` `ui` The example card is a flush thumbnail at a four-to-three ratio over the hatch wash, a runtime mark chipped into the top left over a blurred plate, a meta bar carrying the title beside the save control `src: Front-end specification`
- [ ] `C-FE-28` `ui` A lock mark sits in the card's meta bar when the example is paid with the reader holding no licence `src: Front-end specification`
- [ ] `C-FE-29` `ui` The save control is the only write action on the homepage, which is why an anonymous visitor pressing the control gets the sign-in path rather than a silent failure `src: Front-end specification`
- [ ] `C-FE-30` `ui` The card thumbnail plays on hover in all four card states, the locked one included `src: Front-end specification`
- [ ] `C-FE-31` `ui` The category card is a media well at a four-to-three ratio, a title row with the name at the left beside a mono count badge at the right, a two-line blurb `src: Front-end specification`
- [ ] `C-FE-32` `ui` The preview shell is a framed stage with a mono control row: a runtime selector, a shuffle control using the shuffle glyph, a reset `src: Front-end specification`
- [ ] `C-FE-33` `ui` The preview well holds exactly the size the media will take, so nothing shifts during loading `src: Front-end specification`
- [ ] `C-FE-34` `ui` The source panel is terminal chrome with three dots, a mono filename, the source at mono, one tab per file, a copy control on each tab `src: Front-end specification`
- [ ] `C-FE-35` `ui` The theme panel is the same terminal chrome over a syntax-coloured source file with one highlighted active line, the highlight drawn as an inset left border in the accent over a faint wash `src: Front-end specification`
- [ ] `C-FE-36` `ui` The spring strip is five mono uppercase tabs over a drawn plot with a tick column at the left beside a tick row underneath `src: Front-end specification`
- [ ] `C-FE-37` `ui` The plot draws all five curves as thin lines with the selected one thick, an accent square beside the plot running the selected transition `src: Front-end specification`
- [ ] `C-FE-38` `ui` A caret in the accent opens the label row, the active transition's stiffness beside the damping sitting at the right of the row `src: Front-end specification`
- [ ] `C-FE-39` `ui` The pricing board is a hairline grid: the recommended plan on the accent ground with the dark ink, a two-digit mono index, a right-aligned flag, a display name, a one-line blurb, the price over a bottom hairline, a feature list one line per feature each prefixed with a plus glyph, a full-width action `src: Front-end specification`
- [ ] `C-FE-40` `ui` The questions band closes the paid route: two columns headed `QUESTION` beside `ANSWER`, one row per frequently asked question, covering pricing, licensing, updates, access `src: Front-end specification`
- [ ] `C-FE-41` `ui` The dossier header on the profile at `/@nova` is a striped frame carrying a mono kicker, a display title, the handle, the joined date, the member's links `src: Front-end specification`
- [ ] `C-FE-42` `ui` The account frame at `/login` is the striped frame again: a heading, a sub line, mono uppercase field labels, a forgotten-password link at the right of the password label, the striped action, a switch line to the other account route `src: Front-end specification`
- [ ] `C-FE-43` `constraint` Every icon is inline geometry drawn square on a view box of the icon's own with no fill, the stroke set to the current ink, nothing being a font, nothing being a file, so no icon carries a corner radius `src: Front-end specification`
- [ ] `C-FE-44` `literal` The icon set is deliberately few shapes: a magnifier, an arrow right, a chevron right, an arrow down, a leaves-the-site box, a tick, a feed, a shuffle, a split-panes pair, a three-dot more, a window frame `src: Front-end specification`
- [ ] `C-FE-45` `literal` Rendered icon sizes run from `11px` to `18px`, drawn square with no radius `src: Front-end specification`
- [ ] `C-FE-46` `ui` The wordmark is one path with two subpaths: three slanted bars beside a dot `src: Front-end specification`
- [ ] `C-FE-47` `constraint` The slant of the wordmark bars is the same angle as the diagonal hatch, so redrawing either redraws both `src: Front-end specification`
- [ ] `C-FE-48` `ui` A second mark, the brand wordmark's glyph alone as a single closed path, renders as a section device plus as the account badge in the header `src: Front-end specification`
- [ ] `C-FE-49` `literal` Three runtime marks identify the three documented runtimes `src: Front-end specification`
- [ ] `C-FE-50` `constraint` Each runtime mark has a full-colour variant whose colours belong to the runtime's own owner, carried on the mark's own primitives rather than read from the root element `src: Front-end specification`
- [ ] `C-FE-51` `constraint` Only the single-colour variant of a runtime mark may be recoloured from the accent on the root element, the variant setting every fill to the current ink `src: Front-end specification`
- [ ] `C-FE-52` `constraint` The component runtime's mark is one ellipse drawn three times under rotation about a shared origin rather than three authored ellipses, served by the declared stack from one process `src: Front-end specification`
- [ ] `C-FE-53` `ui` The not-found figure is two drawn canvases side by side on one frame, the left a turning wireframe `src: Front-end specification`
- [ ] `C-FE-54` `ui` The left canvas is a turning wireframe torus sampled as rings of vertices, projected through a simple perspective divide, rotating about two axes at rates that are not multiples of one another so the figure never repeats `src: Front-end specification`
- [ ] `C-FE-55` `ui` The turning wireframe back half is drawn first at half alpha, the visible cusps being a property of the sampling rather than an added highlight `src: Front-end specification`
- [ ] `C-FE-56` `literal` The right canvas beside the wireframe figure is a histogram strip of sixty-four horizontal bars stacked down the strip, each one pixel tall on a four-pixel pitch, extending leftward from the right edge `src: Front-end specification`
- [ ] `C-FE-57` `ui` The histogram bar lengths beside the wireframe figure are a smoothed noise series seeded once per page load, drifting upward slowly, with two or three bars per screen at full alpha as accents `src: Front-end specification`
- [ ] `C-FE-58` `constraint` Both not-found canvases stop drawing when the viewport no longer contains the content `src: Front-end specification`
- [ ] `C-FE-59` `ui` The hero is a full-bleed band on the amber ground with a dark card starting in from the left holding everything `src: Front-end specification`
- [ ] `C-FE-60` `literal` The hero kicker row carries `Open source / MIT License` at the left beside `v13.1.0` at the right `src: Front-end specification`
- [ ] `C-FE-61` `literal` The hero title is four lines with the brand word in the accent followed by a full stop: `Tempo.`, then `Production-grade`, then `animation library`, then `for the web.` `src: Front-end specification`
- [ ] `C-FE-62` `ui` The hero title carries a clip that wipes the title in from the left, played once on load, on the house curve, being the same shutter as the primary action's wipe `src: Front-end specification`
- [ ] `C-FE-63` `literal` The two hero actions read `Get started` beside `Browse examples` `src: Front-end specification`
- [ ] `C-FE-64` `literal` The hero runtime row carries a caret in the accent, the label `Prev Loom Studio Motion. Available for:`, three chips reading `React`, `JavaScript`, `Vue` `src: Front-end specification`
- [ ] `C-FE-65` `ui` The proof strip sits directly under the hero, still on the accent ground, carrying the three runtime names spread evenly beside `Tempo 13.1.0` pushed right `src: Front-end specification`
- [ ] `C-FE-66` `literal` Five claim cells sit below the proof strip on the dark ground, each a mono uppercase term in the accent beside a description in the proportional face `src: Front-end specification`
- [ ] `C-FE-67` `literal` The first claim cell is `Free`, whose description names the MIT-licensed code the proof strip also carries `src: Front-end specification`
- [ ] `C-FE-68` `literal` The claim cell `Hybrid engine` names JavaScript beside the hardware-accelerated browser interfaces the React runtime uses `src: Front-end specification`
- [ ] `C-FE-69` `literal` The remaining three claim cells read `Production ready`, `Built for AI`, `Tiny footprint`, each term set in the mono family `src: Front-end specification`
- [ ] `C-FE-70` `ui` The feature atlas is a hairline grid of eight cells, four across, two down `src: Front-end specification`
- [ ] `C-FE-71` `ui` Each atlas cell has a stage in the upper portion holding one drawn figure, then a two-digit mono index in the accent, a heading with an arrow that moves on hover, a two-line blurb, a mono readout that is a syntax-coloured fragment of the thing being demonstrated `src: Front-end specification`
- [ ] `C-FE-72` `literal` The eight atlas cells, in order, are `Independent transforms`, `Scroll animation`, `Native gestures`, `Layout animation`, `Spring physics`, `Exit animation`, `Timeline sequences`, `Motion values` `src: Front-end specification`
- [ ] `C-FE-73` `ui` Two of the eight atlas cells invert: the stage takes the accent as the ground with the readout ink flipping to the dark ink `src: Front-end specification`
- [ ] `C-FE-74` `literal` The atlas closes with `AVAILABLE FOR`, three runtime chips reading React, JavaScript, Vue, then `ALL DOCUMENTATION` `src: Front-end specification`
- [ ] `C-FE-75` `ui` The homepage then carries the examples grid of six cards, the showcase tape, the workflow fork, the changelog column, the magazine column, the documentation directory `src: Front-end specification`
- [ ] `C-FE-76` `contract` The showcase tape is a single row of published projects, a submitted project being absent from the tape as from every public response `src: Front-end specification`
- [ ] `C-FE-77` `ui` One band on the paid route is a pinned stage held across a long scroll track with four stages passing through `src: Front-end specification`
- [ ] `C-FE-78` `constraint` The pinned stage scrubs both ways: scrolling back up un-reveals exactly what scrolling down revealed rather than snapping to a resting state `src: Front-end specification`
- [ ] `C-FE-79` `constraint` The curtain over the pinned stage clears in the same scroll distance at every width `src: Front-end specification`
- [ ] `C-FE-80` `constraint` No scroll-linked effect changes a layout property, so nothing under the pointer runs longer than the half second the house curve takes `src: Front-end specification`
- [ ] `C-FE-81` `ui` Below the tablet threshold the pinned track shortens with the stages, below the next threshold down the pinned stage being replaced by a progress readout `src: Front-end specification`
- [ ] `C-FE-82` `ui` Each pinned stage has a heading of the stage's own in the document outline at an address of the stage's own, plus a skip control visible on focus `src: Front-end specification`
- [ ] `C-FE-83` `constraint` No binary asset ships: every icon, the diagonal hatch stripe, every figure, every mark is drawn from coordinates or from a repeating gradient `src: Front-end specification`
- [ ] `C-FE-84` `capability` A catalogue card's still frame is rendered at build time from the example's own stored preview bundle at the first frame of the animation, regenerated whenever the example changes `src: Front-end specification`
- [ ] `C-FE-85` `capability` Before a still frame loads, the card thumbnail place is held by a gradient generated from the example's own identifier, so the same example always gets the same two colours, rendered inline rather than fetched `src: Front-end specification`
- [ ] `C-FE-86` `capability` A member portrait on the profile at `/@nova` that has not been supplied is a flat tile at a colour derived from the handle with the first two characters of the handle set in the mono family `src: Front-end specification`
- [ ] `C-FE-87` `capability` A sponsor mark that has not been supplied is the sponsor's name set in the mono family, uppercase, tracked out, which is a legitimate final treatment as much as a stand-in `src: Front-end specification`
- [ ] `C-FE-88` `constraint` The hatch, the dot field, the ruler are gradients, which is why the site needs no texture file at all `src: Front-end specification`
- [ ] `C-FE-89` `literal` At most four font files load, both families being named rather than shipped, served by the declared stack from one process `src: Front-end specification`
- [ ] `C-FE-90` `constraint` One header component ships, not two `src: Front-end specification`
- [ ] `C-FE-91` `constraint` Four width thresholds ship, not the twenty-five the reference measured `src: Front-end specification`
- [ ] `C-FE-92` `constraint` The light colour scheme is removed rather than left half finished `src: Front-end specification`
- [ ] `C-FE-93` `constraint` The not-found document is rendered on the server, carrying the not-found status `src: Front-end specification`
- [ ] `C-FE-94` `constraint` Exactly one of `/docs` or `/docs/` is canonical, exactly one of `/ui` or `/ui/`, the other in each pair redirecting permanently `src: Front-end specification`
- [ ] `C-FE-95` `constraint` No video plays on its own above the fold, every media well carrying intrinsic dimensions so nothing shifts `src: Front-end specification`
- [ ] `C-FE-96` `constraint` At most three previews run at once, an off-screen preview being destroyed `src: Front-end specification`
- [ ] `C-FE-97` `constraint` The drawn canvases carrying the wireframe figure stop when off screen, capping the pixel density at twice the device's own `src: Front-end specification`
- [ ] `C-FE-98` `constraint` One frame loop exists in the whole document at every one of the four width thresholds `src: Front-end specification`
- [ ] `C-FE-99` `constraint` A route's content is the document the server sent rather than a skeleton filled in by a second request `src: Front-end specification`
- [ ] `C-FE-100` `constraint` A narrow viewport shows no sideways overflow on any route `src: Front-end specification`
- [ ] `C-FE-101` `ui` Narrowing the viewport to a phone width switches the navigation labels to the short forms without content overflowing sideways `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` The site is served as server-rendered pages with hydrated islands rather than as a client-side application fetching its own markup `src: Technical requirements`
- [ ] `C-TR-02` `literal` The frontend framework is Nuxt 3, the read surface under `/api` being Hono, mounted inside the framework's own server so one process serves both `src: Technical requirements`
- [ ] `C-TR-03` `constraint` The first paint a browser receives is the complete document for the route, rendered on the server from the published catalogue, the release records, the signed-in member's own rows `src: Technical requirements`
- [ ] `C-TR-04` `capability` Only the islands needing a client hydrate: the gallery's filter row, the preview stage, the theme file's tab strip, the plot, the save control, the purchase panel `src: Technical requirements`
- [ ] `C-TR-05` `constraint` A facet combination is a server-rendered address rather than a client-side re-sort of a list already in the browser `src: Technical requirements`
- [ ] `C-TR-06` `constraint` One origin, one container-internal port, so there is exactly one origin for the preview frame's policy to allow `src: Technical requirements`
- [ ] `C-TR-07` `constraint` The backend architecture is one declared stack in one process with three trust boundaries, every behaviour that matters being a behaviour at one of the three `src: Technical requirements`
- [ ] `C-TR-08` `constraint` The first boundary is the session: a request either carries a valid bearer token or carries a missing token, an unknown token, an expired token, nothing below that line guessing `src: Technical requirements`
- [ ] `C-TR-09` `constraint` The second boundary is the licence: paid bytes leave the process only for a request whose licence row resolved `src: Technical requirements`
- [ ] `C-TR-10` `constraint` The third boundary is the preview frame, treated as hostile code running next to a signed-in session `src: Technical requirements`
- [ ] `C-TR-11` `constraint` The module architecture is five primitives with nothing below: a card, a frame, a control, a plate, a well, from which the feature atlas cells are built `src: Technical requirements`
- [ ] `C-TR-12` `constraint` State outliving a component lives outside the component: the session, the resolved entitlement, the preferred runtime, the reduced-motion preference are read once per request then passed down `src: Technical requirements`
- [ ] `C-TR-13` `constraint` The rendering strategy is stated per route rather than per component: a product route renders on the server then hydrates named islands, a reading route hydrates nothing, an account route hydrates only the form `src: Technical requirements`
- [ ] `C-TR-14` `constraint` No route renders itself twice: the grid arrives with the document rather than appearing after a separate fetch `src: Technical requirements`
- [ ] `C-TR-15` `literal` The datastore is PostgreSQL, read from `DATABASE_URL`, holding the seeded content rows once per generation `src: Technical requirements`
- [ ] `C-TR-16` `literal` Billing lives in Kill Bill, read from `PAYMENTS_API_URL`, `PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`, `PAYMENTS_BASIC_USER`, `PAYMENTS_BASIC_PASSWORD` `src: Technical requirements`
- [ ] `C-TR-17` `literal` Mail is sent over SMTP to `SMTP_HOST`, which is how a receipt reaches the buyer `src: Technical requirements`
- [ ] `C-TR-18` `literal` The app's own address plus port come from `APP_PUBLIC_URL` beside `APP_PUBLIC_PORT`, which is the one origin the pages share `src: Technical requirements`
- [ ] `C-TR-19` `constraint` No host, no port is hardcoded: every one is read from the environment, so the pages share whatever origin the environment names `src: Technical requirements`
- [ ] `C-TR-20` `constraint` All three backing services are already running, reachable at those variables, never downloaded, installed, compiled, or started by the declared stack in its one process `src: Technical requirements`
- [ ] `C-TR-21` `constraint` Only the libraries named in the brief plus their direct dependencies are used, so the declared stack serves from one process with no second database, cache, queue, object store, identity provider, mail vendor introduced `src: Technical requirements`
- [ ] `C-TR-22` `constraint` Kill Bill is a billing platform rather than a card processor: no charge object, no card token, no decline code, the app never seeing a card number `src: Technical requirements`
- [ ] `C-TR-23` `contract` On a completed purchase the app creates one billing account under the licence's own external key, reading the account back by that key `src: Technical requirements`
- [ ] `C-TR-24` `constraint` The app refers to a billing account by the external key, never by the identifier the platform generates, so a repeated write meets the key conflict `src: Technical requirements`
- [ ] `C-TR-25` `constraint` The app names no plan, creating no subscription: a purchase creates a billing account under the licence key alone `src: Technical requirements`
- [ ] `C-TR-26` `contract` Every billing call carries the api key, the api secret, the admin basic credential, a header naming the writer, none of which reaches anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-27` `constraint` No account is required to read anything: every facet combination address is rendered on the server for a visitor with no session `src: Technical requirements`
- [ ] `C-TR-28` `constraint` An account exists for two jobs: holding what somebody bought, holding the saved row that survives a reload `src: Technical requirements`
- [ ] `C-TR-29` `data` An account holds an identifier, a handle, an authentication method, a display name, the profile links, a preferred runtime, the list of owned things, nothing more: no history of what was read, no stored analytics `src: Technical requirements`
- [ ] `C-TR-30` `literal` Authentication is app-implemented email with password plus bearer tokens, passwords stored hashed, never in a recoverable form `src: Technical requirements`
- [ ] `C-TR-31` `constraint` Authorisation is by ownership plus entitlement, so one member cannot read another member's rows `src: Technical requirements`
- [ ] `C-TR-32` `constraint` The entitlement claim is resolved per request from the licence row, never carried inside the bearer token, never cached past the request that read the row `src: Technical requirements`
- [ ] `C-TR-33` `capability` A licence carrying a revocation date stops unlocking anything on the next request `src: Technical requirements`
- [ ] `C-TR-34` `constraint` A licence the app cannot read produces a refused claim: entitlement fails closed `src: Technical requirements`
- [ ] `C-TR-35` `capability` Per-address rate limiting applies to login plus account creation with a low burst, a low sustained rate, because a wrong password is cheap for the caller `src: Technical requirements`
- [ ] `C-TR-36` `capability` Saving an example plus submitting a project are limited per account rather than per address, a repeat leaving one stored row `src: Technical requirements`
- [ ] `C-TR-37` `constraint` Reading the manual at the current release is not limited beyond ordinary network protection, a docs address never carrying a challenge `src: Technical requirements`
- [ ] `C-TR-38` `contract` Every limited response states the limit, the remaining allowance, when the allowance resets, carrying the same body shape as the answer to an unknown facet value `src: Technical requirements`
- [ ] `C-TR-39` `literal` Every write accepts an idempotency key, honoured for 24 hours, a purchase requiring one `src: Technical requirements`
- [ ] `C-TR-40` `constraint` The second request carrying a used idempotency key returns the first outcome, writing nothing `src: Technical requirements`
- [ ] `C-TR-41` `contract` `GET /api/health` returns `200` once the app is ready to serve `src: Technical requirements`
- [ ] `C-TR-42` `contract` Each request for one of the pages is logged as one structured line carrying the method, the path, the status, the elapsed milliseconds, to standard output, whatever the origin `src: Technical requirements`
- [ ] `C-TR-43` `contract` Every response carries a strict transport policy, a nosniff content type policy, a frame policy, a referrer policy, a content security policy `src: Technical requirements`
- [ ] `C-TR-44` `contract` The content security policy for the framed document names the app's own origin as the only destination reachable, denying form submission, top-level navigation, popups, downloads `src: Technical requirements`
- [ ] `C-TR-45` `constraint` The framed document is served without the session cookie, so script inside has no session to read `src: Technical requirements`
- [ ] `C-TR-46` `constraint` No database address, no billing api key, no billing api secret, no billing admin password, no mail host, no bearer token belonging to another account reaches any document, script, stylesheet, or payload the browser can fetch `src: Technical requirements`
- [ ] `C-TR-47` `contract` A favicon is served at `/favicon.ico`, declared in the head of every document `src: Technical requirements`
- [ ] `C-TR-48` `contract` Every public route declares a title of the route's own plus a description of the route's own, no two routes sharing either `src: Technical requirements`
- [ ] `C-TR-49` `literal` `/docs/react/use-spring` differs from `/docs/13.0.4/react/use-spring` in title plus description, because the release is part of what the route is about `src: Technical requirements`
- [ ] `C-TR-50` `constraint` Money is integer minor units beside a currency code everywhere the amount is stored, returned, or compared, a decimal fraction never being the stored form `src: Technical requirements`
- [ ] `C-TR-51` `capability` A displayed price is formatted from the minor units at the moment of rendering `src: Technical requirements`
- [ ] `C-TR-52` `constraint` Dates are one format in one timezone everywhere, which is what lets both dated feeds order newest first `src: Technical requirements`
- [ ] `C-TR-53` `contract` Collections are cursor paginated with a stated maximum page size, never offset paginated, so the three orderings sort the same rows every time `src: Technical requirements`
- [ ] `C-TR-54` `capability` The bot policy is identification rather than exclusion: a sitemap lists every public route, the robots file names the sitemap, no challenge sitting in front of the manual `src: Technical requirements`
- [ ] `C-TR-55` `constraint` Every stored credential the app uses is read from the environment, scoped to the one service the credential belongs to, never written into anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-56` `constraint` Every dependency is pinned to an exact version, the pinned set the preview frame loads being the pinned set the stored example file names `src: Technical requirements`
- [ ] `C-TR-57` `constraint` Content is immutable, versioned, built from source, published as one generation, nothing writing to content at runtime `src: Technical requirements`
- [ ] `C-TR-58` `constraint` No foreign key crosses from an application row to a content row: an application row references content by a stable identifier plus the generation the row was read at `src: Technical requirements`
- [ ] `C-TR-59` `constraint` Content rows are replaced wholesale on every release, so a foreign key from application data would either block the release or cascade a deletion through a member's saved rows `src: Technical requirements`
- [ ] `C-TR-60` `constraint` Versioning is by release: a documentation page exists once per retained release, so a versioned docs address stays on the release named `src: Technical requirements`
- [ ] `C-TR-61` `constraint` Invalidation has exactly one path, publishing a newer generation, with no second way to expire a content row `src: Technical requirements`
- [ ] `C-TR-62` `contract` A success carries the resource plus the release stamp the resource was read at, which is the current release for an address carrying no version `src: Technical requirements`
- [ ] `C-TR-63` `contract` A failure carries a stable machine code, a human message, the address of the page explaining the code, an unknown facet value answering that way `src: Technical requirements`
- [ ] `C-TR-64` `contract` A validation failure carries a field-keyed map so a form renders errors without a second code path, which is how signup refuses a duplicate `src: Technical requirements`
- [ ] `C-TR-65` `constraint` Every count in the copy is counted from the catalogue: the example total, the tutorial total, the section total, the category total, every per-category count read from the published generation at render time `src: Technical requirements`
- [ ] `C-TR-66` `constraint` No numeral describing the size of the catalogue is typed into a template, two places quoting one count reading the same query `src: Technical requirements`
- [ ] `C-TR-67` `constraint` A catalogue card's still frame for one stored example at one generation is the same bytes every time, on any machine, after a restart `src: Technical requirements`
- [ ] `C-TR-68` `constraint` The holding gradient behind one card thumbnail is the same two colours every time `src: Technical requirements`
- [ ] `C-TR-69` `literal` A preview frame that has not reported itself ready is stopped by the page around the frame at 5 seconds of wall clock, no more than three running at once `src: Technical requirements`
- [ ] `C-TR-70` `constraint` Code that never yields cannot be stopped from inside the preview frame, so the budget is enforced from outside `src: Technical requirements`
- [ ] `C-TR-71` `capability` A request from inside the preview frame for a member surface is refused exactly as a request carrying no credential is refused, the frame reporting the refusal, the page stating the refusal `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Fifteen tables, every timestamp in UTC, the content rows stored once per generation `src: Data model`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`, hashed as normal, the exact literal working at login, written into `/app/USER_README.md` beside each account `src: Data model`
- [ ] `C-DM-03` `data` `releases` carries `version` unique, `released_on`, `channel`, `is_current`, with exactly one row carrying `is_current` `src: Data model`
- [ ] `C-DM-04` `literal` The release `13.1.0` was released on `2026-09-02`, carrying `is_current` `src: Data model`
- [ ] `C-DM-05` `literal` The release `13.0.4` was released on `2026-07-19`, not current `src: Data model`
- [ ] `C-DM-06` `literal` The release `12.8.2` was released on `2026-04-08`, not current `src: Data model`
- [ ] `C-DM-07` `data` `categories` carries `path` unique, `name`, `blurb`, `position`, nine rows in the seeded order `src: Data model`
- [ ] `C-DM-08` `data` `examples` carries `id`, `slug` unique, `title`, `category_path`, `tier`, `runtimes`, `published_at`, `save_count`, `generation`, seven rows `src: Data model`
- [ ] `C-DM-09` `literal` `scroll-velocity` is titled Scroll velocity, filed under `stats-sections`, free, published `2026-09-01` `src: Data model`
- [ ] `C-DM-10` `literal` `parallax` is titled Parallax, filed under `hero-sections`, free, published `2026-08-22` `src: Data model`
- [ ] `C-DM-11` `literal` `skeleton-shimmer` is titled Skeleton Shimmer, filed under `bento-grids`, free, published `2026-08-14` `src: Data model`
- [ ] `C-DM-12` `literal` `floating-action` is titled Floating Action, filed under `cta-sections`, free, published `2026-07-30` `src: Data model`
- [ ] `C-DM-13` `literal` `ios-app-folder` is titled iOS App Folder, filed under `page-transitions`, paid, published `2026-08-27` `src: Data model`
- [ ] `C-DM-14` `literal` `ios-pointer` is titled iOS Pointer, filed under `navigation`, paid, published `2026-08-05` `src: Data model`
- [ ] `C-DM-15` `literal` `ticker-marquee` is titled Ticker, filed under `testimonials`, paid, published `2026-06-11` `src: Data model`
- [ ] `C-DM-16` `data` `save_count` is the count of the example's own `saved_items` rows, read from those rows rather than kept in step by hand `src: Data model`
- [ ] `C-DM-17` `data` `example_files` carries `id`, `example_id`, `path`, `language`, `source`, at least one row per example `src: Data model`
- [ ] `C-DM-18` `constraint` The `source` of a paid example's files is what the licence protects, absent from a response served without the licence `src: Data model`
- [ ] `C-DM-19` `data` `sections` carries everything an example has plus `registry_name`, `theme_keys`, `token_contract`, six rows `src: Data model`
- [ ] `C-DM-20` `literal` `editorial-stagger-hero` reads the theme keys `transitions.gentle`, `stagger.relaxed`, `travel.enter` `src: Data model`
- [ ] `C-DM-21` `literal` `border-beam` reads the theme key `transitions.ambient` `src: Data model`
- [ ] `C-DM-22` `literal` `confetti` reads the theme keys `transitions.lively`, `travel.enter` `src: Data model`
- [ ] `C-DM-23` `literal` `command-palette` reads the theme keys `transitions.snap`, `stagger.tight` `src: Data model`
- [ ] `C-DM-24` `literal` `coverflow` reads the theme keys `transitions.ui`, `travel.hover` `src: Data model`
- [ ] `C-DM-25` `literal` `sheet` reads the theme keys `transitions.ui`, `travel.section` `src: Data model`
- [ ] `C-DM-26` `data` `token_contract` names the style tokens a section expects the buyer to have defined, which makes the category grid's claim checkable before installation `src: Data model`
- [ ] `C-DM-27` `data` `theme_values` carries `key` unique, `value`, `kind`, `position`, twelve rows `src: Data model`
- [ ] `C-DM-28` `data` Of the twelve theme values the five `transition` rows carry a stiffness beside a damping, the three `stagger` rows plus the three `travel` rows carrying one number each, `reducedMotion` carrying a word `src: Data model`
- [ ] `C-DM-29` `data` `doc_pages` carries `id`, `slug`, `runtime`, `title`, `summary`, `body`, `since_version`, `deprecated_version`, `tier`, `generation`, unique on runtime with slug plus generation, a docs address with no version resolving through the current release `src: Data model`
- [ ] `C-DM-30` `literal` The shared page `installation` is titled Installation, a docs page whose introduced release is `12.8.2`, free `src: Data model`
- [ ] `C-DM-31` `literal` The `react` page `use-spring` is titled useSpring, a docs page whose introduced release is `12.8.2`, free `src: Data model`
- [ ] `C-DM-32` `literal` The `react` page `animate-presence` is titled AnimatePresence, a docs page whose introduced release is `13.0.4`, free `src: Data model`
- [ ] `C-DM-33` `literal` The `react` page `layout-animation` is titled Layout animation, a docs page whose introduced release is `13.1.0`, paid `src: Data model`
- [ ] `C-DM-34` `literal` The `js` page `animate` is titled animate, a docs page whose introduced release is `12.8.2`, free `src: Data model`
- [ ] `C-DM-35` `literal` The `js` page `scroll` is titled scroll, a docs page whose introduced release is `13.0.4`, free `src: Data model`
- [ ] `C-DM-36` `literal` The `vue` page `motion-component` is titled Motion component, a docs page whose introduced release is `12.8.2`, free `src: Data model`
- [ ] `C-DM-37` `data` `doc_code_blocks` carries `id`, `doc_page_id`, `position`, `language`, `runtime`, `is_runnable`, `source`, `executed_against_version` `src: Data model`
- [ ] `C-DM-38` `data` `executed_against_version` is what lets a page state that the runnable block ran against the release the page serves, marking a block whose last execution was older `src: Data model`
- [ ] `C-DM-39` `data` `changelog_entries` carries `id`, `slug` unique, `version`, `kind`, `title`, `body`, `published_at`, four rows `src: Data model`
- [ ] `C-DM-40` `data` `articles` carries `id`, `slug` unique, `title`, `standfirst`, `body`, `author_handle`, `published_at`, three rows `src: Data model`
- [ ] `C-DM-41` `literal` The article `springs-over-easing` is titled Springs over easing curves, by the author handle `alex`, published `2026-08-28` `src: Data model`
- [ ] `C-DM-42` `literal` The article `the-all-problem` is titled The cost of animating everything, by the author handle `alex`, published `2026-07-15` `src: Data model`
- [ ] `C-DM-43` `literal` The article `reduced-motion-is-not-no-motion` is titled Reduced motion is not no motion, by the author handle `alex`, published `2026-06-04` `src: Data model`
- [ ] `C-DM-44` `constraint` `author_handle` is a content value rather than a foreign key to an account row, which is the no-crossing rule in practice: an article outlives whoever wrote the article `src: Data model`
- [ ] `C-DM-45` `data` `price_bands` carries `code` unique, `region`, `amount_minor`, `reason`, two rows, a band being a row rather than a formula `src: Data model`
- [ ] `C-DM-46` `data` `accounts` carries `id`, `handle` unique folded, `email` unique folded, `display_name`, `links`, `password_hash`, `preferred_runtime`, `joined_at`, three seeded rows `src: Data model`
- [ ] `C-DM-47` `literal` `member@example.com` at the folded handle `nova` is Nova Reyes, the profile that handle reaches carrying the joined date `2026-03-11` `src: Data model`
- [ ] `C-DM-48` `literal` `member2@example.com` at the folded handle `kit` is Kit Alvarez, the profile that handle reaches carrying the joined date `2026-06-02` `src: Data model`
- [ ] `C-DM-49` `literal` `member3@example.com` at the folded handle `sol` is Sol Danner, the profile that handle reaches carrying the joined date `2026-09-10` `src: Data model`
- [ ] `C-DM-50` `data` `sessions` carries `token`, `account_id`, `issued_at`, `expires_at`, an expired token being refused 24 hours after issue `src: Data model`
- [ ] `C-DM-51` `data` `licences` carries `id`, `external_key` unique, `order_id`, `owner_account_id`, `kind`, `entitlements`, `valid_from`, `valid_until`, `revoked_at` `src: Data model`
- [ ] `C-DM-52` `literal` One licence is seeded at the external key `tempo-plus-nova`, which is the billing account key a purchase creates, of the kind `personal-perpetual`, with a null `valid_until` because a perpetual licence does not expire `src: Data model`
- [ ] `C-DM-53` `constraint` A licence row is never mutated: a revoked licence is a new row, which stops unlocking on the next request `src: Data model`
- [ ] `C-DM-54` `data` `orders` carries `id`, `account_id`, `licence_id`, `currency`, `list_amount_minor`, `discount_amount_minor`, `total_amount_minor`, `price_band_code`, `discount_reason`, `state`, `created_at` `src: Data model`
- [ ] `C-DM-55` `literal` One order is seeded against `tempo-plus-nova`, storing money as integer minor units: currency `USD`, `list_amount_minor` `24900`, `discount_amount_minor` `0`, `total_amount_minor` `24900`, `price_band_code` `list`, `state` `paid` `src: Data model`
- [ ] `C-DM-56` `constraint` An order row is never deleted, so the band the banner showed stays on the record `src: Data model`
- [ ] `C-DM-57` `data` `saved_items` carries `id`, `account_id`, `example_id`, `generation`, `saved_at`, unique on the account paired with the example, so saving twice leaves one stored row `src: Data model`
- [ ] `C-DM-58` `literal` Two stored saved rows are seeded for `member@example.com`, from which the saved count is read: `scroll-velocity` plus `parallax` `src: Data model`
- [ ] `C-DM-59` `constraint` The unique pair is what makes a repeated save leave one stored row without an application-level guard `src: Data model`
- [ ] `C-DM-60` `data` `pending_saves` carries `id`, `session_hint`, `example_slug`, `created_at`, one row per save begun signed out, consumed when that visitor signs in, none seeded `src: Data model`
- [ ] `C-DM-61` `data` `showcase_projects` carries `id`, `account_id`, `title`, `source_url`, `description`, `state`, `submitted_at`, `reviewed_at`, `rejection_reason`, two seeded rows `src: Data model`
- [ ] `C-DM-62` `literal` The seeded project `Orbit Atlas` at `https://orbit-atlas.example.com` is `published` `src: Data model`
- [ ] `C-DM-63` `literal` The seeded project `Field Notes` at `https://field-notes.example.com` is `submitted` `src: Data model`
- [ ] `C-DM-64` `constraint` Only a `published` project row reaches a public response `src: Data model`
- [ ] `C-DM-65` `data` `idempotency_records` carries `key`, `account_id`, `endpoint`, `response_body`, `created_at`, honoured for 24 hours, so the first purchase outcome is what a repeat returns `src: Data model`
- [ ] `C-DM-66` `data` A save begun signed out is kept 24 hours as a pending row, an idempotency record 24 hours, a session until expiry, a rejected showcase project 30 days `src: Data model`
- [ ] `C-DM-67` `data` An order row with its licence is kept, never deleted, so the band the order records outlives the account `src: Data model`
- [ ] `C-DM-68` `contract` One billing call per completed purchase creates a billing account whose external key is the licence's own `external_key`, whose name is the buyer's display name, whose email is the buyer's address, whose currency is `USD`, whose country is `US` `src: Data model`
- [ ] `C-DM-69` `constraint` The app reads the billing account back by the external key, so a repeated purchase meets the key conflict rather than an application guard `src: Data model`
- [ ] `C-DM-70` `data` The billing platform already holds `orbit-amelia`, `orbit-acme`, `orbit-northwind` from bootstrap, which the app neither reads nor writes: a purchase creates one account under the licence key leaving every other untouched `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One site, no tenancy: every reader sees the same published generation of the content rows `src: Constraints`
- [ ] `C-CN-02` `constraint` One product only: no per-seat team plan, no seat stepper, no seat transfer, no renewal cycle, no annual billing, the licence being bought once without expiring `src: Constraints`
- [ ] `C-CN-03` `constraint` No refunds, no dunning, no stored payment method, no card of any kind: the billing key conflict is the only refusal the platform issues `src: Constraints`
- [ ] `C-CN-04` `constraint` No tax calculation, no tax record: the order stores the list amount, the discount amount, the total amount alone `src: Constraints`
- [ ] `C-CN-05` `constraint` No animation performance audit service: no report, no worker fleet, no continuous-integration gate, no audit table, so no foreign key crosses into content rows for one `src: Constraints`
- [ ] `C-CN-06` `constraint` No agent context service: no tool server, no skills, no editor bridge, no machine-readable twin of a page, so the declared stack serves the public routes alone `src: Constraints`
- [ ] `C-CN-07` `constraint` No moderation worker, no automated screening, no transcoding, no takedown queue, no uploaded media anywhere: a submitted project carries a title, an address, a description `src: Constraints`
- [ ] `C-CN-08` `constraint` No external code sandbox handoff, no third-party editor link: the framed preview names the app's own origin as the only destination `src: Constraints`
- [ ] `C-CN-09` `constraint` No site-wide search overlay, no machine search endpoint: narrowing happens on the gallery's own facet combination address `src: Constraints`
- [ ] `C-CN-10` `constraint` No book, no sponsor route, no advertise route, no troubleshooting route, so no public route beyond the ones the sitemap lists `src: Constraints`
- [ ] `C-CN-11` `constraint` No private package registry, no members-only chat platform: the licence unlocks the paid source in the response alone `src: Constraints`
- [ ] `C-CN-12` `constraint` No second language: every route is served in one language with no language segment, no language switch, no translation row among the content rows `src: Constraints`
- [ ] `C-CN-13` `constraint` No consent banner, no third-party script, no product analytics, because nothing recorded carries an identifier, which is what the privacy page states `src: Constraints`
- [ ] `C-CN-14` `constraint` No external network call at runtime: every route is answered by the declared stack in one process from PostgreSQL, the billing platform, the published source `src: Constraints`
- [ ] `C-CN-15` `constraint` No native application, no installable app shell: the pages are served from one origin `src: Constraints`
- [ ] `C-CN-16` `constraint` One colour mode, the laboratory dark, with no light scheme for the product chrome, the footer being the one surface that inverts by design `src: Constraints`
- [ ] `C-CN-17` `constraint` The site stays responsive with three retained releases of seven documentation pages each, seven examples, six sections, nine categories, four changelog entries, three articles, all stored once per generation `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`, the port mapping being `${APP_PUBLIC_PORT}:4173`, both read from the environment, neither hardcoded, the pages served from that one origin `src: Deployment contract`
- [ ] `C-DC-02` `contract` The HTTP read surface is served on that same origin under the `/api` prefix by the declared stack in one process `src: Deployment contract`
- [ ] `C-DC-03` `contract` `GET /api/health` returns `200` once the app is ready, on the origin the pages share `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps, the declared stack serving from one process on boot `src: Deployment contract`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md`, naming the seeded accounts stored once with hashed passwords `src: Deployment contract`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root, empty `src: Deployment contract`
- [ ] `C-DC-07` `constraint` The app root keeps both reserved directories rather than creating either on demand `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server, never a dev server, by the declared stack `src: Deployment contract`
- [ ] `C-DC-09` `constraint` The server keeps running after the session ends rather than as a child of the shell, so the pages stay on the one origin `src: Deployment contract`
- [ ] `C-DC-10` `constraint` The listener binds `0.0.0.0` rather than a loopback address, so the origin the pages share is reachable from outside the container `src: Deployment contract`
- [ ] `C-DC-11` `constraint` The backing services named in the brief are already running, never downloaded, installed, compiled, or started by the declared stack `src: Deployment contract`
- [ ] `C-DC-12` `constraint` Only the providers named in the brief are used by the declared stack in its one process, with no edge functions, no persistent volumes, no fixed container names, no custom networks `src: Deployment contract`
- [ ] `C-DC-13` `contract` Every list endpoint returns a top-level JSON array, sorted by one of the three orderings `src: Deployment contract`
- [ ] `C-DC-14` `contract` Bearer auth is carried on everything except `GET /api/health`, `POST /api/v1/auth/login`, `POST /api/v1/auth/signup`, a missing token being refused elsewhere `src: Deployment contract`
- [ ] `C-DC-15` `contract` An invalid or unauthorized call is rejected as a client error, never with a `5xx`, never with a silent success, an unknown facet value answering the same way `src: Deployment contract`
- [ ] `C-DC-16` `contract` `GET /api/v1/me` answers with the `member` plus `entitled` resolved from the licence row on the next request rather than from the token `src: Deployment contract`
- [ ] `C-DC-17` `contract` `GET /api/v1/docs/{runtime}/{slug}` answers with `title`, `summary`, `body`, `since_version`, `tier`, `release` naming the current release, `code_blocks` each carrying `source`, `is_runnable`, `executed_against_version` `src: Deployment contract`
- [ ] `C-DC-18` `contract` `GET /api/v1/docs/{version}/{runtime}/{slug}` answers with the same shape, `release` naming the version in the address `src: Deployment contract`
- [ ] `C-DC-19` `contract` `GET /api/v1/examples` takes `runtime`, `category`, `access`, `saved`, `sort`, `cursor`, `limit`, answering with `items`, `total`, `next_cursor` `src: Deployment contract`
- [ ] `C-DC-20` `contract` Each gallery card item carries `slug`, `title`, `category`, `tier`, `runtimes`, `save_count`, `saved`, `locked`, `poster`, which states whether the source may be opened `src: Deployment contract`
- [ ] `C-DC-21` `contract` `GET /api/v1/examples/{slug}` answers with `files` where the reader holds the licence, `locked` true with the paid source absent from the response without one `src: Deployment contract`
- [ ] `C-DC-22` `contract` `GET /api/v1/examples/{slug}/files/{path}` answers with the file source, or a refusal where the reader holds no licence `src: Deployment contract`
- [ ] `C-DC-23` `contract` `GET /api/v1/categories` answers with `path`, `name`, `blurb`, `section_count` per category `src: Deployment contract`
- [ ] `C-DC-24` `contract` `GET /api/v1/sections` takes `category`, answering with `slug`, `title`, `category`, `theme_keys`, `token_contract` `src: Deployment contract`
- [ ] `C-DC-25` `contract` `GET /api/v1/theme` answers with `key`, `value`, `kind` per theme value `src: Deployment contract`
- [ ] `C-DC-26` `contract` `GET /api/v1/pricing` answers with `list_amount_minor`, `currency`, `band` carrying `code`, `amount_minor`, `reason`, plus `banner` true only where the band is not the list band `src: Deployment contract`
- [ ] `C-DC-27` `contract` `POST /api/v1/purchases` takes `display_name`, `email`, `idempotency_key`, answering with `licence_key` plus the order, or the refusal a repeated write meets at the billing key `src: Deployment contract`
- [ ] `C-DC-28` `contract` `GET /api/v1/saved` answers with the caller's own saved examples, refusing another member's rows `src: Deployment contract`
- [ ] `C-DC-29` `contract` `POST /api/v1/saved` takes `example_slug`, the same call twice answering with the same stored row `src: Deployment contract`
- [ ] `C-DC-30` `contract` `DELETE /api/v1/saved/{example_slug}` answers with an empty object, the saved row then being gone from the grid `src: Deployment contract`
- [ ] `C-DC-31` `contract` `GET /api/v1/members/{handle}` answers with the member, the joined date, the links, `projects` holding published rows alone, an unknown handle answering as not found `src: Deployment contract`
- [ ] `C-DC-32` `contract` `POST /api/v1/showcase` takes `title`, `source_url`, `description`, answering with the project at the state `submitted` `src: Deployment contract`
- [ ] `C-DC-33` `contract` `GET /api/v1/showcase/{id}` answers to the owner, refusing anybody else where the project is absent from every public response `src: Deployment contract`
- [ ] `C-DC-34` `contract` `GET /api/v1/changelog` answers newest first with `slug`, `version`, `kind`, `title`, `published_at` `src: Deployment contract`
- [ ] `C-DC-35` `contract` `GET /api/v1/magazine` answers newest first with `slug`, `title`, `standfirst`, `author_handle`, `published_at` `src: Deployment contract`
- [ ] `C-DC-36` `contract` `GET /api/v1/magazine/{slug}` answers with one article, both dated feeds staying ordered newest first `src: Deployment contract`
- [ ] `C-DC-37` `constraint` PostgreSQL, the billing platform, the mail transport are the facts, so a licence held in a module-level dictionary rather than read per request is a contract violation `src: Deployment contract`
- [ ] `C-DC-38` `constraint` A billing account the app records in a table of its own without creating the account in the platform is a contract violation `src: Deployment contract`
- [ ] `C-DC-39` `constraint` A receipt the app logs rather than sends by mail is a contract violation `src: Deployment contract`
- [ ] `C-DC-40` `constraint` A `locked` flag computed from a hardcoded list rather than from an entitlement the app resolves, refuses, or reads apart from unbought is a contract violation `src: Deployment contract`
- [ ] `C-DC-41` `constraint` A total in units other than integer minor units, or one the client calculates that the server trusts, is a contract violation `src: Deployment contract`
- [ ] `C-DC-42` `constraint` A paid file's source served from a route the entitlement resolution does not cover is a contract violation, however good the page looks `src: Deployment contract`
- [ ] `C-DC-43` `constraint` The named provider is the fact: the interface plus the content rows stored once per generation can only reflect what lives in the provider, never substitute for the provider `src: Deployment contract`

## Pinned literals

| Value | Meaning | Item | Where |
|---|---|---|---|
| `deku-demo-pw-2026` | value pinned by C-RL-13 | C-RL-13 | User roles |
| `member@example.com` | value pinned by C-RL-14 | C-RL-14 | User roles |
| `nova` | value pinned by C-RL-14 | C-RL-14 | User roles |
| `member2@example.com` | value pinned by C-RL-15 | C-RL-15 | User roles |
| `kit` | value pinned by C-RL-15 | C-RL-15 | User roles |
| `member3@example.com` | value pinned by C-RL-16 | C-RL-16 | User roles |
| `sol` | value pinned by C-RL-16 | C-RL-16 | User roles |
| `Sign in failed` | value pinned by C-CF-05 | C-CF-05 | Core features |
| `13.1.0` | value pinned by C-CF-15 | C-CF-15 | Core features |
| `/docs/13.0.4/react/use-spring` | value pinned by C-CF-17 | C-CF-17 | Core features |
| `13.0.4` | value pinned by C-CF-17 | C-CF-17 | Core features |
| `12.8.2` | value pinned by C-CF-18 | C-CF-18 | Core features |
| `use-spring` | value pinned by C-CF-24 | C-CF-24 | Core features |
| `runtime` | value pinned by C-CF-33 | C-CF-33 | Core features |
| `category` | value pinned by C-CF-33 | C-CF-33 | Core features |
| `access` | value pinned by C-CF-33 | C-CF-33 | Core features |
| `saved` | value pinned by C-CF-33 | C-CF-33 | Core features |
| `newest` | value pinned by C-CF-34 | C-CF-34 | Core features |
| `most-saved` | value pinned by C-CF-34 | C-CF-34 | Core features |
| `title` | value pinned by C-CF-34 | C-CF-34 | Core features |
| `/examples?runtime=react&category=hero-sections` | value pinned by C-CF-35 | C-CF-35 | Core features |
| `react` | value pinned by C-CF-35 | C-CF-35 | Core features |
| `hero-sections` | value pinned by C-CF-35 | C-CF-35 | Core features |
| `access=paid` | value pinned by C-CF-36 | C-CF-36 | Core features |
| `access=free` | value pinned by C-CF-37 | C-CF-37 | Core features |
| `saved=1` | value pinned by C-CF-38 | C-CF-38 | Core features |
| `scroll-velocity` | value pinned by C-CF-54 | C-CF-54 | Core features |
| `parallax` | value pinned by C-CF-55 | C-CF-55 | Core features |
| `skeleton-shimmer` | value pinned by C-CF-56 | C-CF-56 | Core features |
| `vue` | value pinned by C-CF-56 | C-CF-56 | Core features |
| `floating-action` | value pinned by C-CF-57 | C-CF-57 | Core features |
| `js` | value pinned by C-CF-57 | C-CF-57 | Core features |
| `ios-app-folder` | value pinned by C-CF-58 | C-CF-58 | Core features |
| `ios-pointer` | value pinned by C-CF-59 | C-CF-59 | Core features |
| `ticker-marquee` | value pinned by C-CF-60 | C-CF-60 | Core features |
| `pricing` | value pinned by C-CF-68 | C-CF-68 | Core features |
| `navigation` | value pinned by C-CF-69 | C-CF-69 | Core features |
| `testimonials` | value pinned by C-CF-70 | C-CF-70 | Core features |
| `page-transitions` | value pinned by C-CF-71 | C-CF-71 | Core features |
| `bento-grids` | value pinned by C-CF-72 | C-CF-72 | Core features |
| `stats-sections` | value pinned by C-CF-73 | C-CF-73 | Core features |
| `cta-sections` | value pinned by C-CF-74 | C-CF-74 | Core features |
| `footers` | value pinned by C-CF-75 | C-CF-75 | Core features |
| `editorial-stagger-hero` | value pinned by C-CF-79 | C-CF-79 | Core features |
| `border-beam` | value pinned by C-CF-79 | C-CF-79 | Core features |
| `confetti` | value pinned by C-CF-79 | C-CF-79 | Core features |
| `command-palette` | value pinned by C-CF-79 | C-CF-79 | Core features |
| `coverflow` | value pinned by C-CF-79 | C-CF-79 | Core features |
| `sheet` | value pinned by C-CF-79 | C-CF-79 | Core features |
| `transitions.snap` | value pinned by C-CF-81 | C-CF-81 | Core features |
| `1218` | value pinned by C-CF-81 | C-CF-81 | Core features |
| `70` | value pinned by C-CF-81 | C-CF-81 | Core features |
| `transitions.ui` | value pinned by C-CF-82 | C-CF-82 | Core features |
| `305` | value pinned by C-CF-82 | C-CF-82 | Core features |
| `33` | value pinned by C-CF-82 | C-CF-82 | Core features |
| `transitions.gentle` | value pinned by C-CF-83 | C-CF-83 | Core features |
| `110` | value pinned by C-CF-83 | C-CF-83 | Core features |
| `20` | value pinned by C-CF-83 | C-CF-83 | Core features |
| `transitions.lively` | value pinned by C-CF-84 | C-CF-84 | Core features |
| `622` | value pinned by C-CF-84 | C-CF-84 | Core features |
| `17` | value pinned by C-CF-84 | C-CF-84 | Core features |
| `transitions.ambient` | value pinned by C-CF-85 | C-CF-85 | Core features |
| `43` | value pinned by C-CF-85 | C-CF-85 | Core features |
| `13` | value pinned by C-CF-85 | C-CF-85 | Core features |
| `stagger.tight` | value pinned by C-CF-86 | C-CF-86 | Core features |
| `0.04` | value pinned by C-CF-86 | C-CF-86 | Core features |
| `stagger.base` | value pinned by C-CF-87 | C-CF-87 | Core features |
| `0.08` | value pinned by C-CF-87 | C-CF-87 | Core features |
| `stagger.relaxed` | value pinned by C-CF-88 | C-CF-88 | Core features |
| `0.15` | value pinned by C-CF-88 | C-CF-88 | Core features |
| `travel.hover` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `4` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `travel.enter` | value pinned by C-CF-90 | C-CF-90 | Core features |
| `24` | value pinned by C-CF-90 | C-CF-90 | Core features |
| `travel.section` | value pinned by C-CF-91 | C-CF-91 | Core features |
| `48` | value pinned by C-CF-91 | C-CF-91 | Core features |
| `reducedMotion` | value pinned by C-CF-92 | C-CF-92 | Core features |
| `"calm"` | value pinned by C-CF-92 | C-CF-92 | Core features |
| `0.0.2` | value pinned by C-CF-103 | C-CF-103 | Core features |
| `$249.00` | value pinned by C-CF-123 | C-CF-123 | Core features |
| `24900` | value pinned by C-CF-123 | C-CF-123 | Core features |
| `USD` | value pinned by C-CF-123 | C-CF-123 | Core features |
| `list` | value pinned by C-CF-126 | C-CF-126 | Core features |
| `US` | value pinned by C-CF-126 | C-CF-126 | Core features |
| `ppp-south-asia` | value pinned by C-CF-127 | C-CF-127 | Core features |
| `IN` | value pinned by C-CF-127 | C-CF-127 | Core features |
| `14900` | value pinned by C-CF-127 | C-CF-127 | Core features |
| `Local discount applied` | value pinned by C-CF-127 | C-CF-127 | Core features |
| `X-Client-Region` | value pinned by C-CF-129 | C-CF-129 | Core features |
| `tempo-plus-` | value pinned by C-CF-138 | C-CF-138 | Core features |
| `tempo-plus-sol` | value pinned by C-CF-138 | C-CF-138 | Core features |
| `Tempo+ receipt ` | value pinned by C-CF-150 | C-CF-150 | Core features |
| `spring-presets` | value pinned by C-CF-217 | C-CF-217 | Core features |
| `feature` | value pinned by C-CF-217 | C-CF-217 | Core features |
| `exit-animation-fix` | value pinned by C-CF-218 | C-CF-218 | Core features |
| `fix` | value pinned by C-CF-218 | C-CF-218 | Core features |
| `pointer-gesture-fix` | value pinned by C-CF-219 | C-CF-219 | Core features |
| `ui-registry-install` | value pinned by C-CF-220 | C-CF-220 | Core features |
| `release` | value pinned by C-CF-220 | C-CF-220 | Core features |
| `springs-over-easing` | value pinned by C-CF-223 | C-CF-223 | Core features |
| `the-all-problem` | value pinned by C-CF-223 | C-CF-223 | Core features |
| `reduced-motion-is-not-no-motion` | value pinned by C-CF-223 | C-CF-223 | Core features |
| `10px` | value pinned by C-UX-14 | C-UX-14 | UI/UX notes |
| `11px` | value pinned by C-UX-14 | C-UX-14 | UI/UX notes |
| `12px` | value pinned by C-UX-15 | C-UX-15 | UI/UX notes |
| `13px` | value pinned by C-UX-15 | C-UX-15 | UI/UX notes |
| `14px` | value pinned by C-UX-15 | C-UX-15 | UI/UX notes |
| `15px` | value pinned by C-UX-15 | C-UX-15 | UI/UX notes |
| `17px` | value pinned by C-UX-16 | C-UX-16 | UI/UX notes |
| `19px` | value pinned by C-UX-17 | C-UX-17 | UI/UX notes |
| `23px` | value pinned by C-UX-17 | C-UX-17 | UI/UX notes |
| `22px` | value pinned by C-UX-18 | C-UX-18 | UI/UX notes |
| `30px` | value pinned by C-UX-18 | C-UX-18 | UI/UX notes |
| `32px` | value pinned by C-UX-18 | C-UX-18 | UI/UX notes |
| `44px` | value pinned by C-UX-18 | C-UX-18 | UI/UX notes |
| `56px` | value pinned by C-UX-18 | C-UX-18 | UI/UX notes |
| `600px` | value pinned by C-UX-38 | C-UX-38 | UI/UX notes |
| `760px` | value pinned by C-UX-38 | C-UX-38 | UI/UX notes |
| `900px` | value pinned by C-UX-38 | C-UX-38 | UI/UX notes |
| `1200px` | value pinned by C-UX-38 | C-UX-38 | UI/UX notes |
| `18px` | value pinned by C-FE-45 | C-FE-45 | Front-end specification |
| `Open source / MIT License` | value pinned by C-FE-60 | C-FE-60 | Front-end specification |
| `v13.1.0` | value pinned by C-FE-60 | C-FE-60 | Front-end specification |
| `Tempo.` | value pinned by C-FE-61 | C-FE-61 | Front-end specification |
| `Production-grade` | value pinned by C-FE-61 | C-FE-61 | Front-end specification |
| `animation library` | value pinned by C-FE-61 | C-FE-61 | Front-end specification |
| `for the web.` | value pinned by C-FE-61 | C-FE-61 | Front-end specification |
| `Get started` | value pinned by C-FE-63 | C-FE-63 | Front-end specification |
| `Browse examples` | value pinned by C-FE-63 | C-FE-63 | Front-end specification |
| `Prev Loom Studio Motion. Available for:` | value pinned by C-FE-64 | C-FE-64 | Front-end specification |
| `React` | value pinned by C-FE-64 | C-FE-64 | Front-end specification |
| `JavaScript` | value pinned by C-FE-64 | C-FE-64 | Front-end specification |
| `Vue` | value pinned by C-FE-64 | C-FE-64 | Front-end specification |
| `Free` | value pinned by C-FE-67 | C-FE-67 | Front-end specification |
| `Hybrid engine` | value pinned by C-FE-68 | C-FE-68 | Front-end specification |
| `Production ready` | value pinned by C-FE-69 | C-FE-69 | Front-end specification |
| `Built for AI` | value pinned by C-FE-69 | C-FE-69 | Front-end specification |
| `Tiny footprint` | value pinned by C-FE-69 | C-FE-69 | Front-end specification |
| `Independent transforms` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `Scroll animation` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `Native gestures` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `Layout animation` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `Spring physics` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `Exit animation` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `Timeline sequences` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `Motion values` | value pinned by C-FE-72 | C-FE-72 | Front-end specification |
| `AVAILABLE FOR` | value pinned by C-FE-74 | C-FE-74 | Front-end specification |
| `ALL DOCUMENTATION` | value pinned by C-FE-74 | C-FE-74 | Front-end specification |
| `/api` | value pinned by C-TR-02 | C-TR-02 | Technical requirements |
| `DATABASE_URL` | value pinned by C-TR-15 | C-TR-15 | Technical requirements |
| `PAYMENTS_API_URL` | value pinned by C-TR-16 | C-TR-16 | Technical requirements |
| `PAYMENTS_API_KEY` | value pinned by C-TR-16 | C-TR-16 | Technical requirements |
| `PAYMENTS_API_SECRET` | value pinned by C-TR-16 | C-TR-16 | Technical requirements |
| `PAYMENTS_BASIC_USER` | value pinned by C-TR-16 | C-TR-16 | Technical requirements |
| `PAYMENTS_BASIC_PASSWORD` | value pinned by C-TR-16 | C-TR-16 | Technical requirements |
| `SMTP_HOST` | value pinned by C-TR-17 | C-TR-17 | Technical requirements |
| `APP_PUBLIC_URL` | value pinned by C-TR-18 | C-TR-18 | Technical requirements |
| `APP_PUBLIC_PORT` | value pinned by C-TR-18 | C-TR-18 | Technical requirements |
| `/docs/react/use-spring` | value pinned by C-TR-49 | C-TR-49 | Technical requirements |
| `/app/USER_README.md` | value pinned by C-DM-02 | C-DM-02 | Data model |
| `2026-09-02` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `is_current` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `2026-07-19` | value pinned by C-DM-05 | C-DM-05 | Data model |
| `2026-04-08` | value pinned by C-DM-06 | C-DM-06 | Data model |
| `2026-09-01` | value pinned by C-DM-09 | C-DM-09 | Data model |
| `2026-08-22` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `2026-08-14` | value pinned by C-DM-11 | C-DM-11 | Data model |
| `2026-07-30` | value pinned by C-DM-12 | C-DM-12 | Data model |
| `2026-08-27` | value pinned by C-DM-13 | C-DM-13 | Data model |
| `2026-08-05` | value pinned by C-DM-14 | C-DM-14 | Data model |
| `2026-06-11` | value pinned by C-DM-15 | C-DM-15 | Data model |
| `installation` | value pinned by C-DM-30 | C-DM-30 | Data model |
| `animate-presence` | value pinned by C-DM-32 | C-DM-32 | Data model |
| `layout-animation` | value pinned by C-DM-33 | C-DM-33 | Data model |
| `animate` | value pinned by C-DM-34 | C-DM-34 | Data model |
| `scroll` | value pinned by C-DM-35 | C-DM-35 | Data model |
| `motion-component` | value pinned by C-DM-36 | C-DM-36 | Data model |
| `alex` | value pinned by C-DM-41 | C-DM-41 | Data model |
| `2026-08-28` | value pinned by C-DM-41 | C-DM-41 | Data model |
| `2026-07-15` | value pinned by C-DM-42 | C-DM-42 | Data model |
| `2026-06-04` | value pinned by C-DM-43 | C-DM-43 | Data model |
| `2026-03-11` | value pinned by C-DM-47 | C-DM-47 | Data model |
| `2026-06-02` | value pinned by C-DM-48 | C-DM-48 | Data model |
| `2026-09-10` | value pinned by C-DM-49 | C-DM-49 | Data model |
| `tempo-plus-nova` | value pinned by C-DM-52 | C-DM-52 | Data model |
| `personal-perpetual` | value pinned by C-DM-52 | C-DM-52 | Data model |
| `valid_until` | value pinned by C-DM-52 | C-DM-52 | Data model |
| `list_amount_minor` | value pinned by C-DM-55 | C-DM-55 | Data model |
| `discount_amount_minor` | value pinned by C-DM-55 | C-DM-55 | Data model |
| `0` | value pinned by C-DM-55 | C-DM-55 | Data model |
| `total_amount_minor` | value pinned by C-DM-55 | C-DM-55 | Data model |
| `price_band_code` | value pinned by C-DM-55 | C-DM-55 | Data model |
| `state` | value pinned by C-DM-55 | C-DM-55 | Data model |
| `paid` | value pinned by C-DM-55 | C-DM-55 | Data model |
| `Orbit Atlas` | value pinned by C-DM-62 | C-DM-62 | Data model |
| `https://orbit-atlas.example.com` | value pinned by C-DM-62 | C-DM-62 | Data model |
| `published` | value pinned by C-DM-62 | C-DM-62 | Data model |
| `Field Notes` | value pinned by C-DM-63 | C-DM-63 | Data model |
| `https://field-notes.example.com` | value pinned by C-DM-63 | C-DM-63 | Data model |
| `submitted` | value pinned by C-DM-63 | C-DM-63 | Data model |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 12 |
| User roles | 1 | 19 |
| Core features | 26 | 240 |
| User flow | 8 | 49 |
| UI/UX notes | 0 | 56 |
| Front-end specification | 3 | 101 |
| Technical requirements | 14 | 71 |
| Data model | 3 | 70 |
| Constraints | 0 | 17 |
| Deployment contract | 13 | 43 |
