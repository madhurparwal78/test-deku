# Checklist: deku/vehicle-range-catalogue-vb

Items: 343
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Unpinned values flagged: 7

## C-OV Overview

- [ ] `C-OV-01` `capability` The product is a public marketing, range-browsing site for one car maker. `src: Overview`
- [ ] `C-OV-02` `capability` A family is the unit the home route presents; a variant is the unit the overview lists. `src: Overview`
- [ ] `C-OV-03` `constraint` The product sells nothing: no cart, no price, no checkout anywhere in the product. `src: Overview`
- [ ] `C-OV-04` `capability` The one thing an anonymous visitor accumulates is a comparison set. `src: Overview`
- [ ] `C-OV-05` `capability` The one thing an account adds is saving a comparison set under a name. `src: Overview`
- [ ] `C-OV-06` `constraint` Every facet count is derived rather than stored. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor reads every one of the six public routes. `src: User roles`
- [ ] `C-RL-02` `role` An anonymous visitor cannot save a comparison set under a name. `src: User roles`
- [ ] `C-RL-03` `role` An anonymous visitor cannot read, rename or delete any saved comparison. `src: User roles`
- [ ] `C-RL-04` `role` An owner can save, read, open, rename, delete their own saved comparisons. `src: User roles`
- [ ] `C-RL-05` `role` An owner cannot read another owner's saved comparison by any route. `src: User roles`
- [ ] `C-RL-06` `role` An owner cannot rename or delete another owner's saved comparison. `src: User roles`
- [ ] `C-RL-07` `role` No role can create, edit or retire a family, variant, market or promotion. `src: User roles`
- [ ] `C-RL-08` `contract` Authorization is enforced on the server for every mutating endpoint. `src: User roles`
- [ ] `C-RL-09` `contract` A denied request leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-10` `contract` A refusal for another owner's saved comparison is indistinguishable from one that does not exist. `src: User roles`
- [ ] `C-RL-11` `contract` The owner a saved comparison belongs to is read from the session, never the request body. `src: User roles`
- [ ] `C-RL-12` `capability` Signup is open, creates an `owner`. `src: User roles`
- [ ] `C-RL-13` `literal` The seeded accounts are `owner@example.com`, `owner2@example.com`. `src: User roles`
- [ ] `C-RL-14` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-15` `data` Each seeded owner holds one saved comparison at first start. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `literal` The six families are `900`, `700`, `Volten`, `Cardinal`, `Terra`, `Sierran`. `src: Core features`
- [ ] `C-CF-02` `data` Ninety two variants sit under the six families. `src: Core features`
- [ ] `C-CF-03` `contract` The home route, the model overview read the same stored range. `src: Core features`
- [ ] `C-CF-04` `data` Each family stores a home order, a facet order as two independent orderings. `src: Core features`
- [ ] `C-CF-05` `constraint` Neither ordering is derived from the other, neither is alphabetical. `src: Core features`
- [ ] `C-CF-06` `literal` The home grid order is `900`, `700`, `Volten`, `Cardinal`, `Terra`, `Sierran`. `src: Core features`
- [ ] `C-CF-07` `literal` The facet order under `All` is `700`, `900`, `Volten`, `Cardinal`, `Terra`, `Sierran`. `src: Core features`
- [ ] `C-CF-08` `data` The family `700` is seeded in the unavailable state. `src: Core features`
- [ ] `C-CF-09` `literal` An unavailable family carries the chip `Model currently unavailable for order.` `src: Core features`
- [ ] `C-CF-10` `constraint` An unavailable family's tile carries no arrow control. `src: Core features`
- [ ] `C-CF-11` `capability` The model overview is one route, not one per family. `src: Core features`
- [ ] `C-CF-12` `contract` The family in the path pre-applies the series facet. `src: Core features`
- [ ] `C-CF-13` `literal` The four facets are `Model series`, `Body Design`, `Seats`, `Drive`. `src: Core features`
- [ ] `C-CF-14` `contract` `Model series` is single-select, defaults to `All`. `src: Core features`
- [ ] `C-CF-15` `contract` `Body Design`, `Seats`, `Drive` are multi-select, default to empty. `src: Core features`
- [ ] `C-CF-16` `capability` Values within one facet combine as alternatives. `src: Core features`
- [ ] `C-CF-17` `capability` Separate facets combine as requirements. `src: Core features`
- [ ] `C-CF-18` `contract` Every facet value carries its count, shown at all times rather than only when selected. `src: Core features`
- [ ] `C-CF-19` `contract` A count is computed against the other facets but not against the facet whose row shows that count. `src: Core features`
- [ ] `C-CF-20` `literal` The seeded series counts are `92`, `10`, `22`, `22`, `9`, `5`, `24`. `src: Core features`
- [ ] `C-CF-21` `data` The six family counts sum to the count on `All`. `src: Core features`
- [ ] `C-CF-22` `capability` Selecting a family reduces the result list, updates every other facet's counts. `src: Core features`
- [ ] `C-CF-23` `constraint` The series counts themselves do not change when a series is selected. `src: Core features`
- [ ] `C-CF-24` `constraint` A facet count is never stored as a column on the range data. `src: Core features`
- [ ] `C-CF-25` `constraint` There is no sort control anywhere on the overview route. `src: Core features`
- [ ] `C-CF-26` `contract` Ordering within a group is the stored house order, never by any statistic. `src: Core features`
- [ ] `C-CF-27` `capability` An empty result is a valid response rather than an error. `src: Core features`
- [ ] `C-CF-28` `constraint` Results are never presented as one flat list. `src: Core features`
- [ ] `C-CF-29` `contract` Results are gathered into groups by body style, each with a heading naming the body. `src: Core features`
- [ ] `C-CF-30` `literal` The two seeded `900` group headings are `900 Corsa Model variants`, `900 Corsa Cabriolet Model variants`. `src: Core features`
- [ ] `C-CF-31` `constraint` A group with no matching variants is absent entirely rather than present, empty. `src: Core features`
- [ ] `C-CF-32` `contract` A variant card carries the cutout, name, chip row, three statistics, consumption, technical link, two actions, the compare checkbox. `src: Core features`
- [ ] `C-CF-33` `literal` The model year chip reads `2027`. `src: Core features`
- [ ] `C-CF-34` `contract` The chip row carries the model year then two to three quieter chips for powertrain, drive, transmission. `src: Core features`
- [ ] `C-CF-35` `contract` The three statistics are always acceleration, power, top speed, in that order. `src: Core features`
- [ ] `C-CF-36` `contract` Each statistic renders as a value above its label. `src: Core features`
- [ ] `C-CF-37` `contract` The statistic label is stored per variant rather than fixed per statistic. `src: Core features`
- [ ] `C-CF-38` `literal` The six seeded `900` variants are `Corsa`, `Corsa T`, `Corsa S`, `Corsa 4S`, `Corsa GTS`, `Corsa 4 GTS`. `src: Core features`
- [ ] `C-CF-39` `literal` The seeded acceleration values are `3.9 s`, `4.5 s`, `3.3 s`, `3.3 s`, `3.0 s`, `3.0 s`. `src: Core features`
- [ ] `C-CF-40` `literal` The seeded power values are `290 kW / 394 PS`, `353 kW / 480 PS`, `398 kW / 541 PS`. `src: Core features`
- [ ] `C-CF-41` `literal` The seeded top speeds are `294 km/h`, `295 km/h`, `308 km/h`, `312 km/h`. `src: Core features`
- [ ] `C-CF-42` `literal` The seeded powertrain chip on all six `900` variants is `Gasoline`. `src: Core features`
- [ ] `C-CF-43` `literal` The seeded drive chips are `Rear-Wheel Drive`, `All-Wheel Drive`. `src: Core features`
- [ ] `C-CF-44` `literal` The seeded transmission chips are `Automatic`, `Manual`. `src: Core features`
- [ ] `C-CF-45` `literal` The acceleration label is `Acceleration 0 - 100 km/h with Sport Chrono Package` on every seeded `900` variant except `Corsa T`. `src: Core features`
- [ ] `C-CF-46` `literal` `Corsa T` carries the acceleration label `Acceleration 0 - 100 km/h`. `src: Core features`
- [ ] `C-CF-47` `literal` The power label is `Power (kW) / Power (PS)` on `Corsa`, `Corsa T`, `Corsa S`, `Corsa 4S`. `src: Core features`
- [ ] `C-CF-48` `literal` The power label is `Power combined (kW) / Power combined (PS)` on `Corsa GTS`, `Corsa 4 GTS`. `src: Core features`
- [ ] `C-CF-49` `literal` The top-speed label is `Top speed` on all six seeded variants. `src: Core features`
- [ ] `C-CF-50` `literal` The consumption prefix is `Fuel consumption combined (model range):`. `src: Core features`
- [ ] `C-CF-51` `literal` The emissions clause is `CO2-emissions combined (model range):`. `src: Core features`
- [ ] `C-CF-52` `literal` The seeded consumption figures are `10.4 - 9.9 l/100 km`, `10.9 - 10.4 l/100 km`, `10.6 - 10.1 l/100 km`, `11.0 - 10.4 l/100 km`, `10.8 - 10.3 l/100 km`. `src: Core features`
- [ ] `C-CF-53` `literal` The seeded emissions figures are `237 - 227 g/km`, `248 - 237 g/km`, `242 - 230 g/km`, `249 - 237 g/km`, `246 - 234 g/km`. `src: Core features`
- [ ] `C-CF-54` `constraint` A variant of an unavailable family carries the unavailable chip, no `Configure` action. `src: Core features`
- [ ] `C-CF-55` `capability` Ticking a card adds that variant to the comparison set; unticking a card removes that variant. `src: Core features`
- [ ] `C-CF-56` `contract` A ticked variant filtered out of view stays in the comparison set. `src: Core features`
- [ ] `C-CF-57` `contract` A ticked variant returns still ticked when a facet change brings that variant back into view. `src: Core features`
- [ ] `C-CF-58` `literal` The comparison set is capped at four variants. `src: Core features`
- [ ] `C-CF-59` `contract` At the cap, unticked checkboxes are disabled rather than hidden. `src: Core features`
- [ ] `C-CF-60` `capability` The cap is stated in the interface. `src: Core features`
- [ ] `C-CF-61` `contract` The comparison set is carried in the query string alongside the facets. `src: Core features`
- [ ] `C-CF-62` `contract` Opening a shared address in a fresh session shows the same narrowed list with the same variants ticked. `src: Core features`
- [ ] `C-CF-63` `ui` A change to the comparison set is announced to assistive technology rather than only shown. `src: Core features`
- [ ] `C-CF-64` `constraint` Resetting the facets does not clear the comparison set. `src: Core features`
- [ ] `C-CF-65` `capability` A signed-in owner saves the current comparison set under a name from its own route. `src: Core features`
- [ ] `C-CF-66` `contract` A saved comparison stores the ticked variants together with the facets in force at the moment of saving. `src: Core features`
- [ ] `C-CF-67` `contract` Opening a saved comparison restores both the variants, the facets. `src: Core features`
- [ ] `C-CF-68` `contract` A restored saved comparison matches what was on screen, after a reload, in a fresh session. `src: Core features`
- [ ] `C-CF-69` `contract` A saved comparison name is required, is trimmed of surrounding whitespace. `src: Core features`
- [ ] `C-CF-70` `literal` A saved comparison name is at most eighty characters. `src: Core features`
- [ ] `C-CF-71` `contract` An empty or whitespace-only name is rejected inline, names the field, writes nothing. `src: Core features`
- [ ] `C-CF-72` `contract` A saved comparison name is unique per owner. `src: Core features`
- [ ] `C-CF-73` `contract` Two different owners may each hold a saved comparison of the same name. `src: Core features`
- [ ] `C-CF-74` `contract` Saving under a name the owner already holds is rejected, writes nothing. `src: Core features`
- [ ] `C-CF-75` `capability` An owner may rename their own saved comparison. `src: Core features`
- [ ] `C-CF-76` `capability` An owner may delete their own saved comparison. `src: Core features`
- [ ] `C-CF-77` `contract` Saving with an empty comparison set is rejected. `src: Core features`
- [ ] `C-CF-78` `contract` Any request naming another owner's saved comparison is denied, the stored row is unchanged. `src: Core features`
- [ ] `C-CF-79` `ui` A save, rename or delete confirms with a transient message that does not replace the page. `src: Core features`
- [ ] `C-CF-80` `capability` The saved-comparison list reflects a change without a reload. `src: Core features`
- [ ] `C-CF-81` `contract` Submitting the same save twice produces one saved comparison, never two. `src: Core features`
- [ ] `C-CF-82` `ui` The home route runs five bands: hero, highlight row, range headline, range grid, discover row. `src: Core features`
- [ ] `C-CF-83` `capability` The hero plays a silent film inline, muted, without the visitor asking. `src: Core features`
- [ ] `C-CF-84` `contract` The hero headline, its call to action are readable before any video byte is requested. `src: Core features`
- [ ] `C-CF-85` `constraint` The hero poster is the only image on the route that loads eagerly. `src: Core features`
- [ ] `C-CF-86` `contract` The film is requested only after the poster has painted. `src: Core features`
- [ ] `C-CF-87` `contract` Blocking the video leaves the route complete, usable with the poster in place. `src: Core features`
- [ ] `C-CF-88` `capability` One round control at the lower right of the hero pauses, resumes playback. `src: Core features`
- [ ] `C-CF-89` `ui` The playback control is keyboard reachable, announcing state rather than carrying state by shape alone. `src: Core features`
- [ ] `C-CF-90` `contract` A reduced-motion visitor gets the poster, no playback at all. `src: Core features`
- [ ] `C-CF-91` `ui` The range grid is two columns on a wide screen, one on a narrow one. `src: Core features`
- [ ] `C-CF-92` `contract` The whole range tile is a single link to that family's model overview. `src: Core features`
- [ ] `C-CF-93` `contract` Each tile carries the signature, one to three availability chips, a body description, a round arrow control. `src: Core features`
- [ ] `C-CF-94` `literal` The seeded tile chips are `Gasoline`, `Electric`, `Hybrid`. `src: Core features`
- [ ] `C-CF-95` `literal` The seeded tile descriptions are the six lines given for `900`, `700`, `Volten`, `Cardinal`, `Terra`, `Sierran`. `src: Core features`
- [ ] `C-CF-96` `contract` The highlight row, the discover row are the same component with different data. `src: Core features`
- [ ] `C-CF-97` `contract` The market selector is served outside the locale segment. `src: Core features`
- [ ] `C-CF-98` `literal` The selector heading is `Select your market or region`. `src: Core features`
- [ ] `C-CF-99` `literal` The seven region groups are `Africa`, `Asia`, `Australia/Oceania`, `Europe`, `Latin America`, `Middle East`, `North America`. `src: Core features`
- [ ] `C-CF-100` `contract` Each market entry names the market, its languages, links to the home route under that locale. `src: Core features`
- [ ] `C-CF-101` `contract` The seven groups are rendered from a stored region key rather than hard-coded. `src: Core features`
- [ ] `C-CF-102` `contract` The selector is reachable from the header globe, the footer `Change` link on every route. `src: Core features`
- [ ] `C-CF-103` `capability` A first-time visitor is asked once about non-essential storage. `src: Core features`
- [ ] `C-CF-104` `contract` The storage panel carries a heading, one paragraph, a cookie policy link, two controls. `src: Core features`
- [ ] `C-CF-105` `literal` The two storage controls read `Accept all`, `Only necessary cookies`. `src: Core features`
- [ ] `C-CF-106` `contract` The storage answer persists, the panel does not return after a reload. `src: Core features`
- [ ] `C-CF-107` `capability` A separate market prompt offers to move the visitor to their local market. `src: Core features`
- [ ] `C-CF-108` `contract` The market prompt is dismissible independently of the storage panel, does not return. `src: Core features`
- [ ] `C-CF-109` `ui` Both panels hold keyboard focus; open, return focus to their trigger on close. `src: Core features`
- [ ] `C-CF-110` `ui` Both panels close on the escape key. `src: Core features`
- [ ] `C-CF-111` `constraint` Neither panel may be bypassed by scrolling the page behind the panel. `src: Core features`
- [ ] `C-CF-112` `contract` Three legal routes ship, each is reachable from the footer legal row on every route. `src: Core features`
- [ ] `C-CF-113` `contract` The privacy policy states what the product stores, covering scope, controller, categories, purposes, recipients, location, retention, contact. `src: Core features`
- [ ] `C-CF-114` `literal` The legal notice names `Valdris Motoren AG` at `Werkstrasse 1, 70000 Rheinstadt`. `src: Core features`
- [ ] `C-CF-115` `literal` The legal notice carries `District Court Rheinstadt`, `HRB no. 000000`, `VAT ID No. XX 000 000 000`. `src: Core features`
- [ ] `C-CF-116` `literal` The legal notice carries `info@example-origin`, `(+00) 0000 000-0`. `src: Core features`
- [ ] `C-CF-117` `contract` The legal notice lists six executive board members, a consumer dispute-resolution statement. `src: Core features`
- [ ] `C-CF-118` `contract` The cookie policy embeds the same live storage settings panel the first-visit dialog opens. `src: Core features`
- [ ] `C-CF-119` `ui` Each legal route carries an in-page contents list above the first heading. `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `literal` The home route is `/:locale`. `src: User flow`
- [ ] `C-UF-02` `literal` The model overview is `/:locale/models/:family`. `src: User flow`
- [ ] `C-UF-03` `literal` The market selector is `/countries`. `src: User flow`
- [ ] `C-UF-04` `literal` The legal routes are `/:locale/legal-notice`, `/:locale/privacy`, `/:locale/cookie-policy`. `src: User flow`
- [ ] `C-UF-05` `literal` The account routes are `/:locale/sign-up`, `/:locale/sign-in`. `src: User flow`
- [ ] `C-UF-06` `literal` The saved-comparison routes are `/:locale/comparisons`, `/:locale/comparisons/new`, `/:locale/comparisons/:id`. `src: User flow`
- [ ] `C-UF-07` `literal` The seeded default locale segment is `international-en`. `src: User flow`
- [ ] `C-UF-08` `contract` An anonymous request for any saved-comparison route redirects to sign in. `src: User flow`
- [ ] `C-UF-09` `contract` After signing in the visitor lands on the route originally asked for, not the home route. `src: User flow`
- [ ] `C-UF-10` `contract` Signing out returns to the home route, makes the saved comparisons unreachable. `src: User flow`
- [ ] `C-UF-11` `contract` An expired session refuses the action, writes nothing, preserves the route for after sign in. `src: User flow`
- [ ] `C-UF-12` `contract` An owner asking for another owner's saved comparison is refused rather than redirected to sign in. `src: User flow`
- [ ] `C-UF-13` `contract` An unknown address renders the product's own not-found page with a way back, answers not found. `src: User flow`
- [ ] `C-UF-14` `contract` A route carrying an unknown facet key ignores that key, rendering normally. `src: User flow`
- [ ] `C-UF-15` `capability` Following a range tile opens the overview with that family pre-applied. `src: User flow`
- [ ] `C-UF-16` `capability` Every list has an empty state. `src: User flow`
- [ ] `C-UF-17` `capability` The saved-comparison list tells an owner that no comparison has been saved yet, offering a link to the overview. `src: User flow`
- [ ] `C-UF-18` `capability` Every route has a loading state, the hero shows its poster rather than an empty rectangle. `src: User flow`
- [ ] `C-UF-19` `contract` A failed request states what failed, leaves the page usable rather than blank. `src: User flow`
- [ ] `C-UF-20` `contract` A rejecting form names the field at fault, keeps what was typed, writes nothing. `src: User flow`
- [ ] `C-UF-21` `literal` A worked saved-comparison name is `Weekend coupes`. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every colour is declared once as a light, dark pair, a band chooses which half applies. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The page ground is a near-white neutral in light, a near-black neutral in dark. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The near-black ground carries a trace of blue rather than being a true black. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Four colours carry meaning, appear nowhere else: informational, success, in-progress, failure. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The focus ring is a single vivid blue identical in both schemes. `src: UI/UX notes`
- [ ] `C-UX-06` `constraint` Exactly one drop shadow exists in the whole build. `src: UI/UX notes`
- [ ] `C-UX-07` `constraint` Cards are separated from the ground by corner softness, scheme rather than by elevation. `src: UI/UX notes`
- [ ] `C-UX-08` `literal` The type weights in use are `400`, `600`, `700`. `src: UI/UX notes`
- [ ] `C-UX-09` `literal` Body text is `16px` over `24px`, secondary labels are `14px`, legal text is `12px`. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Every size above the three fixed ones is fluid, clamped at both ends rather than stepped. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Headlines are never set bold; the normal face carries every headline. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Every declared border is a single hairline of one thickness. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Four durations, three easing curves are declared once, used everywhere. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The motion character is eased: nothing springs, bounces or overshoots. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Travel distance rises with the size of the element, so a headline travels further than a small control. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Travel distance roughly halves on a narrow screen. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Range tiles begin faintly visible rather than fully transparent. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Every reveal plays once, holds; nothing replays on scrolling back. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Within a group each item waits a fixed step longer than the one before, capped after a few steps. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` The range grid reveals per tile rather than per row. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` A reveal scrolled past is cancelled rather than queued, the group is already in its final state. `src: UI/UX notes`
- [ ] `C-UX-22` `constraint` Nothing on the site is scrubbed against scroll position. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Whole bands change scheme as a timed colour transition on one clock rather than as a swap. `src: UI/UX notes`
- [ ] `C-UX-24` `ui` The family signature steps through a ramp of greys rather than interpolating between two ends. `src: UI/UX notes`
- [ ] `C-UX-25` `constraint` The scroll indicator under the hero is the only looping element on the site. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` Round icon buttons raise their frosted fill on hover, do not scale or move. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` The range tile carries the hover state rather than the arrow control inside the tile. `src: UI/UX notes`
- [ ] `C-UX-28` `ui` Inline anchors in prose are underlined at rest, not on hover. `src: UI/UX notes`
- [ ] `C-UX-29` `ui` Hover effects are suppressed where the pointer is coarse. `src: UI/UX notes`
- [ ] `C-UX-30` `contract` Body text meets WCAG AA contrast against its ground in both schemes. `src: UI/UX notes`
- [ ] `C-UX-31` `ui` Chip labels stay legible over photography behind a frosted blur, dropping the blur requires a solid fill rather than lower contrast. `src: UI/UX notes`
- [ ] `C-UX-32` `contract` Full keyboard navigation reaches every interactive element with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-33` `ui` Icon-only controls carry text labels for assistive technology. `src: UI/UX notes`
- [ ] `C-UX-34` `contract` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-35` `ui` Each range tile is one tab stop, so tabbing the six families takes six presses. `src: UI/UX notes`
- [ ] `C-UX-36` `contract` The compare controls are real checkboxes operable by the space key. `src: UI/UX notes`
- [ ] `C-UX-37` `contract` The facet groups expose their expanded state. `src: UI/UX notes`
- [ ] `C-UX-38` `contract` One main region, one page heading per route, with heading order descending without gaps. `src: UI/UX notes`
- [ ] `C-UX-39` `contract` The header, main region, footer are landmarks, the filter rail is a complementary region. `src: UI/UX notes`
- [ ] `C-UX-40` `contract` The three statistics on a variant card are marked up as a description list. `src: UI/UX notes`
- [ ] `C-UX-41` `contract` Every content image carries a description naming the family, setting; decorative scrims carry none. `src: UI/UX notes`
- [ ] `C-UX-42` `ui` Reduced motion applies every reveal's end state immediately, leaves the page complete, static. `src: UI/UX notes`
- [ ] `C-UX-43` `ui` Six width tiers exist, the tablet tier carries the major layout change. `src: UI/UX notes`
- [ ] `C-UX-44` `contract` Nothing overflows sideways at a narrow viewport, every navigation target stays reachable. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The page is a twelve-region grid with a gutter that grows with the viewport. `src: Front-end specification`
- [ ] `C-FE-02` `ui` Two elements establish an isolated stacking context: the application root, the main region. `src: Front-end specification`
- [ ] `C-FE-03` `constraint` Nothing stacks above the ceiling those two contexts establish. `src: Front-end specification`
- [ ] `C-FE-04` `contract` A fixed header on every route holds four things: menu, wordmark, globe, account. `src: Front-end specification`
- [ ] `C-FE-05` `ui` The wordmark is centred in the viewport rather than between the control groups. `src: Front-end specification`
- [ ] `C-FE-06` `literal` The menu control carries the word `Menu` beside its icon. `src: Front-end specification`
- [ ] `C-FE-07` `ui` Over the hero the header carries no fill, no border, takes the dark scheme. `src: Front-end specification`
- [ ] `C-FE-08` `ui` Off the hero the header takes the page ground, a hairline bottom border. `src: Front-end specification`
- [ ] `C-FE-09` `ui` The footer is dark scheme on every route regardless of the scheme of the band above the footer. `src: Front-end specification`
- [ ] `C-FE-10` `contract` The footer runs five stacked bands in a fixed order. `src: Front-end specification`
- [ ] `C-FE-11` `literal` The scroll-up control reads `Scroll up`. `src: Front-end specification`
- [ ] `C-FE-12` `literal` The region row reads `Current Region / Language`, `International / English`, `Change`. `src: Front-end specification`
- [ ] `C-FE-13` `literal` The three footer column headings are `Locations & Contacts`, `Company`, `Valdris on the web`. `src: Front-end specification`
- [ ] `C-FE-14` `literal` The first footer column carries `Get in touch`. `src: Front-end specification`
- [ ] `C-FE-15` `literal` The second footer column carries six links pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-16` `literal` The third footer column carries three links pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-17` `literal` The copyright line reads `(c) 2027 Valdris Motoren AG.` `src: Front-end specification`
- [ ] `C-FE-18` `literal` The legal row carries `Legal Notice.`, `Privacy Policy.`, `Cookie Policy.`, `Consumption/Emissions.`, `Open Source Software Notice.`, `Whistleblower System.`, `Accessibility.` `src: Front-end specification`
- [ ] `C-FE-19` `constraint` Every legal row link carries its terminal full stop inside the link text. `src: Front-end specification`
- [ ] `C-FE-20` `contract` The footer carries the two disclaimer paragraphs verbatim. `src: Front-end specification`
- [ ] `C-FE-21` `literal` The storage dialog heading is `Your cookie settings.`, its subheading is `Personalised experiences at full control.` `src: Front-end specification`
- [ ] `C-FE-22` `literal` The market prompt carries the switch-to-local-market question pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-23` `literal` The market prompt controls read `Go to Local Market`, `International`. `src: Front-end specification`
- [ ] `C-FE-24` `literal` The hero heading reads `Sierran.`, the hero action reads `Discover more`. `src: Front-end specification`
- [ ] `C-FE-25` `ui` The hero heading is bottom-left aligned rather than centred. `src: Front-end specification`
- [ ] `C-FE-26` `contract` The hero consumption disclaimer belongs to the hero rather than to the band below the hero. `src: Front-end specification`
- [ ] `C-FE-27` `literal` The three highlight titles are pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-28` `constraint` The highlight disclaimer is a single paragraph covering all three cards, clauses separated by a vertical bar. `src: Front-end specification`
- [ ] `C-FE-29` `literal` The range headline reads `Your Valdris journey starts now.` `src: Front-end specification`
- [ ] `C-FE-30` `ui` The range headline is left-aligned, the discover heading is centred. `src: Front-end specification`
- [ ] `C-FE-31` `literal` The discover heading reads `Discover`, the tile action reads `Explore`. `src: Front-end specification`
- [ ] `C-FE-32` `literal` The three discover titles are pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-33` `ui` Every tile carries its parts in a fixed order: signature, top scrim, media, bottom scrim, chips, description, arrow. `src: Front-end specification`
- [ ] `C-FE-34` `ui` The arrow control inside a tile is decorative, out of the tab order. `src: Front-end specification`
- [ ] `C-FE-35` `ui` The scrim darkens toward the caption through many eased stops rather than as a two-stop ramp. `src: Front-end specification`
- [ ] `C-FE-36` `ui` The scrim caps short of fully opaque so the photograph stays visible under the caption. `src: Front-end specification`
- [ ] `C-FE-37` `ui` Two scrim instances exist per tile, one to the top, one to the bottom. `src: Front-end specification`
- [ ] `C-FE-38` `ui` A second gradient fades the sticky `Filter` control into the page. `src: Front-end specification`
- [ ] `C-FE-39` `ui` The overview sits on the surface colour rather than the page ground. `src: Front-end specification`
- [ ] `C-FE-40` `literal` The overview heading reads `Model overview`. `src: Front-end specification`
- [ ] `C-FE-41` `literal` The resume aside reads `Do you already have a configuration?` above `Load saved configuration`. `src: Front-end specification`
- [ ] `C-FE-42` `literal` The rail aside carries the body-type question pinned in the literals table, above `Understand the differences`. `src: Front-end specification`
- [ ] `C-FE-43` `literal` The rail reset control reads `Reset Filter`, the small-viewport control reads `Filter`. `src: Front-end specification`
- [ ] `C-FE-44` `ui` The filter rail is sticky within the page. `src: Front-end specification`
- [ ] `C-FE-45` `contract` Each series row is a label, a count in parentheses in a quieter colour. `src: Front-end specification`
- [ ] `C-FE-46` `ui` The variant card carries its parts top to bottom in a fixed order. `src: Front-end specification`
- [ ] `C-FE-47` `ui` The cutout image overflows the top edge of the card with the wheels on the card boundary. `src: Front-end specification`
- [ ] `C-FE-48` `literal` The variant card carries four control labels pinned in the literals table: `Explore in Detail`, `Configure`, `Compare`, the technical-data link. `src: Front-end specification`
- [ ] `C-FE-49` `ui` Legal prose is held to the narrowest measure with an in-page contents list. `src: Front-end specification`
- [ ] `C-FE-50` `ui` The responsive matrix holds per module across the three tiers. `src: Front-end specification`
- [ ] `C-FE-51` `contract` The range tile is a separate implementation below the tablet tier rather than a restyle. `src: Front-end specification`
- [ ] `C-FE-52` `contract` Presentation primitives are defined once, consumed identically on every route. `src: Front-end specification`
- [ ] `C-FE-53` `contract` A route composes modules, a module composes primitives, a primitive composes nothing. `src: Front-end specification`
- [ ] `C-FE-54` `contract` A module owns its scheme declaration, nothing else about its colour. `src: Front-end specification`
- [ ] `C-FE-55` `constraint` The range tile, promoted card, variant card are three separate modules. `src: Front-end specification`
- [ ] `C-FE-56` `contract` The highlight row, discover row are one module built once. `src: Front-end specification`
- [ ] `C-FE-57` `constraint` No module reaches into another module to position that module. `src: Front-end specification`
- [ ] `C-FE-58` `constraint` No module holds a copy of the range data. `src: Front-end specification`
- [ ] `C-FE-59` `contract` Facet selections, the anonymous comparison set live in the query string. `src: Front-end specification`
- [ ] `C-FE-60` `contract` The storage choice, market-prompt dismissal are durable per visitor. `src: Front-end specification`
- [ ] `C-FE-61` `literal` Ten icons appear across the routes, each in its named place. `src: Front-end specification`
- [ ] `C-FE-62` `contract` All ten icons are drawn rather than fetched, stroked, inherit the current text colour. `src: Front-end specification`
- [ ] `C-FE-63` `ui` The family signature is a mask over a colour-filled element rather than a coloured picture. `src: Front-end specification`
- [ ] `C-FE-64` `contract` Each wordmark is one continuous path in a connected italic script at a shared skew. `src: Front-end specification`
- [ ] `C-FE-65` `constraint` The build ships no binary file of any kind. `src: Front-end specification`
- [ ] `C-FE-66` `contract` Tile photography is canvas-generated, seeded from the family key. `src: Front-end specification`
- [ ] `C-FE-67` `contract` The scrim is applied over generated photography unchanged rather than substituted. `src: Front-end specification`
- [ ] `C-FE-68` `contract` The variant cutout is composed from primitives rather than a rectangle. `src: Front-end specification`
- [ ] `C-FE-69` `contract` The hero film is a generated loop delivered as an adaptive segmented stream. `src: Front-end specification`
- [ ] `C-FE-70` `contract` Store badges, social marks are drawn as neutral monochrome geometry. `src: Front-end specification`
- [ ] `C-FE-71` `contract` The crest is a neutral quartered roundel carrying no resemblance to a heraldic crest. `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `literal` The frontend is Angular built with Vite. `src: Technical requirements`
- [ ] `C-TR-02` `literal` The backend is Flask serving a JSON API under the `/api` prefix. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The rendering model is a single-page application, so the server renders no page markup. `src: Technical requirements`
- [ ] `C-TR-04` `literal` Storage is PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `contract` `DATABASE_URL` is read from the environment, never hardcoded. `src: Technical requirements`
- [ ] `C-TR-06` `literal` Authentication is app-implemented email, password with bearer tokens. `src: Technical requirements`
- [ ] `C-TR-07` `literal` The health endpoint `/api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-08` `constraint` No second database, cache, queue, object store, identity provider or mail vendor is introduced. `src: Technical requirements`
- [ ] `C-TR-09` `constraint` PostgreSQL is already running, is not downloaded, installed, compiled or started. `src: Technical requirements`
- [ ] `C-TR-10` `contract` The typeface is a freely licensed narrow humanist grotesque with lining figures, loaded from a package. `src: Technical requirements`
- [ ] `C-TR-11` `contract` Two font faces load before first paint, both are preloaded. `src: Technical requirements`
- [ ] `C-TR-12` `contract` Every face loads with swap behaviour. `src: Technical requirements`
- [ ] `C-TR-13` `literal` Script before the hero is interactive stays under 150 kilobytes compressed. `src: Technical requirements`
- [ ] `C-TR-14` `literal` Stylesheet before first paint stays under 40 kilobytes compressed. `src: Technical requirements`
- [ ] `C-TR-15` `contract` Zero video bytes are requested before the headline is readable. `src: Technical requirements`
- [ ] `C-TR-16` `constraint` Every image other than the hero poster loads as the image approaches the viewport. `src: Technical requirements`
- [ ] `C-TR-17` `constraint` None of the six range tiles loads eagerly. `src: Technical requirements`
- [ ] `C-TR-18` `constraint` The film is never preloaded, at any level. `src: Technical requirements`
- [ ] `C-TR-19` `contract` Every response carries the standard security headers, a strict transport policy, a nosniff content-type policy. `src: Technical requirements`
- [ ] `C-TR-20` `contract` A sitemap lists every public route; a robots file names the sitemap. `src: Technical requirements`
- [ ] `C-TR-21` `constraint` No credential, API key, token or database URL appears in anything the browser downloads. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Eight tables carry the product. `src: Data model`
- [ ] `C-DM-02` `constraint` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-03` `literal` The tables are `families`, `variants`, `markets`, `promotions`, `owners`, `saved_comparisons`, `saved_comparison_variants`, `consent_choices`. `src: Data model`
- [ ] `C-DM-04` `data` A family stores `home_order`, `facet_order` as two independent unique orderings. `src: Data model`
- [ ] `C-DM-05` `data` A variant stores each statistic as a value, its own label. `src: Data model`
- [ ] `C-DM-06` `data` A market stores a `region_key` from the seven region values. `src: Data model`
- [ ] `C-DM-07` `data` A promotion stores a `row_key` of `highlight` or `discover`. `src: Data model`
- [ ] `C-DM-08` `constraint` The highlight consumption disclaimer is a field on the row rather than on any card. `src: Data model`
- [ ] `C-DM-09` `data` An owner email is unique, case-insensitive. `src: Data model`
- [ ] `C-DM-10` `contract` A saved comparison name is unique per owner rather than globally. `src: Data model`
- [ ] `C-DM-11` `contract` A variant appears at most once in one saved comparison. `src: Data model`
- [ ] `C-DM-12` `constraint` Every facet count is computed on each request, is never a column. `src: Data model`
- [ ] `C-DM-13` `constraint` An anonymous visitor's comparison set is not stored at all. `src: Data model`
- [ ] `C-DM-14` `data` The seeded variant distribution is `700` ten, `900` twenty two, `Volten` twenty two, `Cardinal` nine, `Terra` five, `Sierran` twenty four. `src: Data model`
- [ ] `C-DM-15` `data` Markets cover all seven regions, `international-en` is marked the default locale. `src: Data model`
- [ ] `C-DM-16` `data` Six promotions are seeded, three in each row. `src: Data model`
- [ ] `C-DM-17` `contract` Seeding is idempotent, restarting the app does not duplicate rows. `src: Data model`
- [ ] `C-DM-18` `literal` The password `deku-demo-pw-2026` works at login, is written into `/app/USER_README.md`. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The site ships one language, one market-neutral international locale. `src: Constraints`
- [ ] `C-CN-02` `constraint` No profile, no preferences, no password reset, no email of any kind. `src: Constraints`
- [ ] `C-CN-03` `constraint` The configurator, stock finder, connected-services product, saved-configuration system are not built. `src: Constraints`
- [ ] `C-CN-04` `constraint` The newsroom, careers site, investor-relations site, per-market sites are not built. `src: Constraints`
- [ ] `C-CN-05` `constraint` Only three of the seven footer legal documents ship. `src: Constraints`
- [ ] `C-CN-06` `capability` The out-of-scope controls are present, styled, leading nowhere. `src: Constraints`
- [ ] `C-CN-07` `constraint` The comparison view itself is out of scope; the selection, its persistence ship. `src: Constraints`
- [ ] `C-CN-08` `constraint` No price is quoted anywhere, there is no cart, no checkout. `src: Constraints`
- [ ] `C-CN-09` `constraint` There is no breadcrumb anywhere. `src: Constraints`
- [ ] `C-CN-10` `constraint` No third-party tracking pixel, no consent vendor. `src: Constraints`
- [ ] `C-CN-11` `constraint` No external network calls at runtime. `src: Constraints`
- [ ] `C-CN-12` `constraint` The product stays responsive at ninety two variants, around two hundred markets. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `APP_PUBLIC_PORT` to the container-internal `4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under `/api`. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-05` `literal` Credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-06` `literal` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served, never a dev server. `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, is not a child of the shell. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0` rather than loopback. `src: Deployment contract`
- [ ] `C-DC-10` `constraint` No persistent volumes, no fixed container names, no custom networks. `src: Deployment contract`
- [ ] `C-DC-11` `contract` List endpoints return a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-12` `contract` An invalid or unauthorized call is rejected as a client error, never a server error, never a silent success. `src: Deployment contract`
- [ ] `C-DC-13` `contract` Bearer auth is required on everything under `/api/comparisons`, on nothing else. `src: Deployment contract`
- [ ] `C-DC-14` `contract` `GET /api/variants` returns counts for every facet value under the current selection. `src: Deployment contract`
- [ ] `C-DC-15` `contract` A series facet count is computed against the other three facets only. `src: Deployment contract`
- [ ] `C-DC-16` `literal` The graded endpoints are those listed in the API shapes table. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `owner@example.com` | User roles | `C-RL-13` |
| `owner2@example.com` | User roles | `C-RL-13` |
| `deku-demo-pw-2026` | User roles | `C-RL-14` |
| `900` | Core features | `C-CF-01` |
| `700` | Core features | `C-CF-01` |
| `Volten` | Core features | `C-CF-01` |
| `Cardinal` | Core features | `C-CF-01` |
| `Terra` | Core features | `C-CF-01` |
| `Sierran` | Core features | `C-CF-01` |
| `Model currently unavailable for order.` | Core features | `C-CF-09` |
| `Model series` | Core features | `C-CF-13` |
| `Body Design` | Core features | `C-CF-13` |
| `Seats` | Core features | `C-CF-13` |
| `Drive` | Core features | `C-CF-13` |
| `All` | Core features | `C-CF-14` |
| `92` | Core features | `C-CF-20` |
| `10` | Core features | `C-CF-20` |
| `22` | Core features | `C-CF-20` |
| `9` | Core features | `C-CF-20` |
| `5` | Core features | `C-CF-20` |
| `24` | Core features | `C-CF-20` |
| `900 Corsa Model variants` | Core features | `C-CF-30` |
| `900 Corsa Cabriolet Model variants` | Core features | `C-CF-30` |
| `2027` | Core features | `C-CF-33` |
| `Corsa` | Core features | `C-CF-38` |
| `Corsa T` | Core features | `C-CF-38` |
| `Corsa S` | Core features | `C-CF-38` |
| `Corsa 4S` | Core features | `C-CF-38` |
| `Corsa GTS` | Core features | `C-CF-38` |
| `Corsa 4 GTS` | Core features | `C-CF-38` |
| `3.9 s` | Core features | `C-CF-39` |
| `4.5 s` | Core features | `C-CF-39` |
| `3.3 s` | Core features | `C-CF-39` |
| `3.0 s` | Core features | `C-CF-39` |
| `290 kW / 394 PS` | Core features | `C-CF-40` |
| `353 kW / 480 PS` | Core features | `C-CF-40` |
| `398 kW / 541 PS` | Core features | `C-CF-40` |
| `294 km/h` | Core features | `C-CF-41` |
| `295 km/h` | Core features | `C-CF-41` |
| `308 km/h` | Core features | `C-CF-41` |
| `312 km/h` | Core features | `C-CF-41` |
| `Gasoline` | Core features | `C-CF-42` |
| `Rear-Wheel Drive` | Core features | `C-CF-43` |
| `All-Wheel Drive` | Core features | `C-CF-43` |
| `Automatic` | Core features | `C-CF-44` |
| `Manual` | Core features | `C-CF-44` |
| `Acceleration 0 - 100 km/h with Sport Chrono Package` | Core features | `C-CF-45` |
| `Acceleration 0 - 100 km/h` | Core features | `C-CF-46` |
| `Power (kW) / Power (PS)` | Core features | `C-CF-47` |
| `Power combined (kW) / Power combined (PS)` | Core features | `C-CF-48` |
| `Top speed` | Core features | `C-CF-49` |
| `Fuel consumption combined (model range):` | Core features | `C-CF-50` |
| `CO2-emissions combined (model range):` | Core features | `C-CF-51` |
| `10.4 - 9.9 l/100 km` | Core features | `C-CF-52` |
| `10.9 - 10.4 l/100 km` | Core features | `C-CF-52` |
| `10.6 - 10.1 l/100 km` | Core features | `C-CF-52` |
| `11.0 - 10.4 l/100 km` | Core features | `C-CF-52` |
| `10.8 - 10.3 l/100 km` | Core features | `C-CF-52` |
| `237 - 227 g/km` | Core features | `C-CF-53` |
| `248 - 237 g/km` | Core features | `C-CF-53` |
| `242 - 230 g/km` | Core features | `C-CF-53` |
| `249 - 237 g/km` | Core features | `C-CF-53` |
| `246 - 234 g/km` | Core features | `C-CF-53` |
| `Electric` | Core features | `C-CF-94` |
| `Hybrid` | Core features | `C-CF-94` |
| `Select your market or region` | Core features | `C-CF-98` |
| `Africa` | Core features | `C-CF-99` |
| `Asia` | Core features | `C-CF-99` |
| `Australia/Oceania` | Core features | `C-CF-99` |
| `Europe` | Core features | `C-CF-99` |
| `Latin America` | Core features | `C-CF-99` |
| `Middle East` | Core features | `C-CF-99` |
| `North America` | Core features | `C-CF-99` |
| `Accept all` | Core features | `C-CF-105` |
| `Only necessary cookies` | Core features | `C-CF-105` |
| `Valdris Motoren AG` | Core features | `C-CF-114` |
| `Werkstrasse 1, 70000 Rheinstadt` | Core features | `C-CF-114` |
| `District Court Rheinstadt` | Core features | `C-CF-115` |
| `HRB no. 000000` | Core features | `C-CF-115` |
| `VAT ID No. XX 000 000 000` | Core features | `C-CF-115` |
| `info@example-origin` | Core features | `C-CF-116` |
| `(+00) 0000 000-0` | Core features | `C-CF-116` |
| `/:locale` | User flow | `C-UF-01` |
| `/:locale/models/:family` | User flow | `C-UF-02` |
| `/countries` | User flow | `C-UF-03` |
| `/:locale/legal-notice` | User flow | `C-UF-04` |
| `/:locale/privacy` | User flow | `C-UF-04` |
| `/:locale/cookie-policy` | User flow | `C-UF-04` |
| `/:locale/sign-up` | User flow | `C-UF-05` |
| `/:locale/sign-in` | User flow | `C-UF-05` |
| `/:locale/comparisons` | User flow | `C-UF-06` |
| `/:locale/comparisons/new` | User flow | `C-UF-06` |
| `/:locale/comparisons/:id` | User flow | `C-UF-06` |
| `international-en` | User flow | `C-UF-07` |
| `Weekend coupes` | User flow | `C-UF-21` |
| `400` | UI/UX notes | `C-UX-08` |
| `600` | UI/UX notes | `C-UX-08` |
| `700` | UI/UX notes | `C-UX-08` |
| `16px` | UI/UX notes | `C-UX-09` |
| `24px` | UI/UX notes | `C-UX-09` |
| `14px` | UI/UX notes | `C-UX-09` |
| `12px` | UI/UX notes | `C-UX-09` |
| `Menu` | Front-end specification | `C-FE-06` |
| `Scroll up` | Front-end specification | `C-FE-11` |
| `Current Region / Language` | Front-end specification | `C-FE-12` |
| `International / English` | Front-end specification | `C-FE-12` |
| `Change` | Front-end specification | `C-FE-12` |
| `Locations & Contacts` | Front-end specification | `C-FE-13` |
| `Company` | Front-end specification | `C-FE-13` |
| `Valdris on the web` | Front-end specification | `C-FE-13` |
| `Get in touch` | Front-end specification | `C-FE-14` |
| `(c) 2027 Valdris Motoren AG.` | Front-end specification | `C-FE-17` |
| `Legal Notice.` | Front-end specification | `C-FE-18` |
| `Privacy Policy.` | Front-end specification | `C-FE-18` |
| `Cookie Policy.` | Front-end specification | `C-FE-18` |
| `Consumption/Emissions.` | Front-end specification | `C-FE-18` |
| `Open Source Software Notice.` | Front-end specification | `C-FE-18` |
| `Whistleblower System.` | Front-end specification | `C-FE-18` |
| `Accessibility.` | Front-end specification | `C-FE-18` |
| `Your cookie settings.` | Front-end specification | `C-FE-21` |
| `Personalised experiences at full control.` | Front-end specification | `C-FE-21` |
| `Do you want to switch to your local market for correct content and pricing?` | Front-end specification | `C-FE-22` |
| `Go to Local Market` | Front-end specification | `C-FE-23` |
| `International` | Front-end specification | `C-FE-23` |
| `Sierran.` | Front-end specification | `C-FE-24` |
| `Discover more` | Front-end specification | `C-FE-24` |
| `Your Valdris journey starts now.` | Front-end specification | `C-FE-29` |
| `Discover` | Front-end specification | `C-FE-31` |
| `Explore` | Front-end specification | `C-FE-31` |
| `Model overview` | Front-end specification | `C-FE-40` |
| `Do you already have a configuration?` | Front-end specification | `C-FE-41` |
| `Load saved configuration` | Front-end specification | `C-FE-41` |
| `What are the differences in body types and model designations?` | Front-end specification | `C-FE-42` |
| `Understand the differences` | Front-end specification | `C-FE-42` |
| `Reset Filter` | Front-end specification | `C-FE-43` |
| `Filter` | Front-end specification | `C-FE-43` |
| `Explore in Detail` | Front-end specification | `C-FE-48` |
| `Configure` | Front-end specification | `C-FE-48` |
| `Technical data and standard equipment` | Front-end specification | `C-FE-48` |
| `Compare` | Front-end specification | `C-FE-48` |
| `DATABASE_URL` | Technical requirements | `C-TR-04` |
| `/api/health` | Technical requirements | `C-TR-07` |
| `200` | Technical requirements | `C-TR-07` |
| `families` | Data model | `C-DM-03` |
| `variants` | Data model | `C-DM-03` |
| `markets` | Data model | `C-DM-03` |
| `promotions` | Data model | `C-DM-03` |
| `owners` | Data model | `C-DM-03` |
| `saved_comparisons` | Data model | `C-DM-03` |
| `saved_comparison_variants` | Data model | `C-DM-03` |
| `consent_choices` | Data model | `C-DM-03` |
| `/app/USER_README.md` | Data model | `C-DM-18` |
| `APP_PUBLIC_URL` | Deployment contract | `C-DC-01` |
| `APP_PUBLIC_PORT` | Deployment contract | `C-DC-02` |
| `4173` | Deployment contract | `C-DC-02` |
| `.browser_screenshots/` | Deployment contract | `C-DC-06` |
| `.downloads/` | Deployment contract | `C-DC-06` |
| `/api` | Deployment contract | `C-DC-03` |
| `/api/comparisons` | Deployment contract | `C-DC-13` |
| `/api/variants` | Deployment contract | `C-DC-14` |

| `Investor Relations` | Front-end specification | `C-FE-15` |
| `Career` | Front-end specification | `C-FE-15` |
| `Global Partnership Council` | Front-end specification | `C-FE-15` |
| `Compliance` | Front-end specification | `C-FE-15` |
| `Newsroom & Press` | Front-end specification | `C-FE-15` |
| `Information Security` | Front-end specification | `C-FE-15` |
| `Valdris Homepage` | Front-end specification | `C-FE-16` |
| `Valdris Configurator` | Front-end specification | `C-FE-16` |
| `Valdris Connect` | Front-end specification | `C-FE-16` |
| `Do you want to switch to your local market for correct content and pricing?` | Front-end specification | `C-FE-22` |
| `Volten Turbo Cross Tourer.` | Front-end specification | `C-FE-27` |
| `The new 900 GTX S/C.` | Front-end specification | `C-FE-27` |
| `Cardinal 4.` | Front-end specification | `C-FE-27` |
| `Valdris Experience.` | Front-end specification | `C-FE-32` |
| `E-Performance - Sustainable mobility` | Front-end specification | `C-FE-32` |
| `Valdris Finder.` | Front-end specification | `C-FE-32` |
| `What are the differences in body types and model designations?` | Front-end specification | `C-FE-42` |
| `Technical data and standard equipment` | Front-end specification | `C-FE-48` |
| `GET /api/health` | Technical requirements | `C-TR-07` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact colour value of every palette role | `C-UX-01` |
| the exact duration of each of the four speeds and the shape of each of the three curves | `C-UX-13` |
| the exact corner radius at each rung of the ladder | `C-UX-12` |
| the exact viewport width of each of the six tiers | `C-UX-43` |
| the exact font family chosen for the narrow humanist grotesque | `C-TR-10` |
| the values inside `Body Design`, `Seats` and `Drive` | `C-CF-15` |
| the destinations of the out-of-scope controls, which lead nowhere | `C-CN-06` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 4 | 6 |
| User roles | 6 | 15 |
| Core features | 62 | 119 |
| User flow | 12 | 21 |
| UI/UX notes | 28 | 44 |
| Technical requirements | 12 | 21 |
| Data model | 11 | 18 |
| Front-end specification | 41 | 71 |
| Constraints | 9 | 12 |
| Deployment contract | 13 | 16 |
