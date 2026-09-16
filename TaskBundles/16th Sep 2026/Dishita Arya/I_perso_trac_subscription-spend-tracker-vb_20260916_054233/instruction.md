# Driplog

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, read the landing page end to end, follow `See it in motion` to the promo band, sign in as `user@example.com`, and see the overview answer three questions at once: `$211.80` a month, `$2,541.55` a year, `$6.96` a day, with the next charge at the top of the upcoming list and a countdown against it, without hitting an error page. The hard part is the arithmetic and the calendar. Every figure on every surface descends from one annual number held in integer minor units, so the overview, the insight charts, the widget routes and the exported file must agree to the minor unit for any store; and the reminder the product promises must reach the timeline exactly once per charge occurrence, never twice because two tabs were open and never silently not at all.

## Overview

Driplog answers one question: what do your subscriptions really cost? Everything you pay for lives in one list, the honest total per day, month and year is always on screen, and a nudge arrives the day before money leaves.

The product is two halves on one origin, sharing one design system. The first is a public marketing site: one long editorial landing page in fourteen bands, a blog index, a privacy policy, a terms page and a not-found screen. The second is the tracker itself at `/app`, behind the landing page's `See it in motion` promise: subscriptions with price, currency and billing cycle, honest per-day, per-month and per-year arithmetic in integer minor units with dated currency conversion, calendar-correct renewal dates with a day-before reminder, a tolerant text importer, a staged receipt reader, insights with price-effective history, glanceable widget and watch surfaces, a free cap of six behind a paywall, undo for every mutation, and a snapshot export that restores.

It is deliberately not a budgeting app, not a bank connection and not a bill payer. It never touches an account, never cancels a real subscription anywhere, and has no social surface: no comments, no sharing, no following, no messaging. One person, one list, one honest number.

The genuinely hard part is that the money and the calendar must both be exactly right: no cent may be invented or eaten anywhere between the store and the screen, and a charge anchored to the 31st must clamp to the end of a short month and come back to the 31st afterwards.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (signed out) | Read the landing page, the blog index and its five articles, the privacy policy and the terms page; open the read-only demo store that powers the hero; sign up; sign in | **Never read, create or change a real subscription, a reminder, a scan, an entitlement or a setting belonging to anybody** |
| Owner (signed in) | Everything about their own list: subscriptions, one-time expenses, categories, imports, scans, reminders, insights, undo, the bin, the entitlement, the settings, the export and the delete-all | **Never read or change another owner's list by any means, and never exceed the free cap while unentitled, whatever the interface offers** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Visitor session to any Owner-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. An Owner requesting another Owner's record reads as not found, never as forbidden, because the existence of somebody else's subscription is itself private.

Signup is open. Two accounts are seeded so both boundaries are real, `user@example.com` and `user2@example.com`, both on the seeded password. The demo store belongs to nobody and is readable by everybody; it is read-only and every surface that renders it says so.

## Core features

### Auth

Email and password exchange for a bearer token sent on every owner request; an expired or absent token is rejected and mutates nothing; signup refuses an address already registered and refuses a password under ten characters, naming the field. The signup form carries a link to the terms page and the person cannot complete signup without the terms link being present on that form.

### The subscription record and the overview

A subscription carries: a name; a price in a currency, entered as text and stored as integer minor units; a billing cycle, one of `weekly`, `every two weeks`, `monthly`, `quarterly`, `half-yearly`, `yearly` or `every N days`; the first-bill anchor date; an optional trial with its own end date and post-trial price; a category; an icon, which is a chosen glyph or the name's first letter; a colour drawn from the product palette; a kind, `recurring` or `one-time`; a status, `active`, `paused` or `cancelled` with its effective date; and free notes.

1. The overview answers three questions at once: the monthly figure at the left, the yearly figure at the right and a multi-hue donut between them, under the title `Your spending` and over the line `Based on your regular and one-time expenses`. A segmented header offers `Calculator` and `AI Spend`; a filter offers `All`, `Recurring` and `One-time`.
2. Below the totals, `Where your money goes` lists one row per category with an icon chip, the category name, an exact per-month figure and a per-year approximation rounded to the nearest ten units of the home currency. Rows are ordered by the monthly figure, largest first.
3. Below that, the upcoming charges run as a timeline, nearest first, each row carrying the subscription, its charge date, its amount in the home currency and a countdown chip stating the whole days remaining. The countdown turns over at local midnight in the owner's zone, not at a fixed offset from when the page was opened.
4. Creating a subscription opens a sheet that rises from the bottom edge and carries three steps, each with its own address: what it is, what it costs, and when it charges. The sheet may be left at any step with nothing written, and a reload on any step returns to that step with the values entered so far intact. Validation is inline and names the field: a negative price is refused, an absent anchor date is refused, and neither writes anything.
5. Editing a price or a cycle asks one question before it saves, `Apply from next renewal` or `Correct history`, and writes a price-change entry either way. This is the next-renewal fork, and the two arms of the fork must diverge. `Apply from next renewal` leaves every past month computed at the old price. `Correct history` recomputes every past month at the new price. The two must produce different insight histories for the same edit; a build that writes the entry and ignores the choice is wrong.
6. Cancelling asks for the effective date, keeps every past charge, moves the record to the cancelled ledger and starts accruing avoided cost from that date. A cancelled subscription is never deleted by cancelling, and it never appears in the upcoming timeline.
7. Typing a name in the editor suggests from the bundled offline service fixture, which carries a glyph initial and a default colour for each known name. The suggestion list is served by this app from its own store and reaches no other service.
8. One-time expenses join the `All` view only in the calendar month they fall in. The `Recurring` filter excludes them entirely, and for any store and any month the `All` figures must equal `Recurring` plus `One-time` to the minor unit.

### The honest-math engine

All arithmetic is integer minor units. No floating-point value may reach the screen or the API as a money figure, in any layer.

9. Cycles annualise as follows and nowhere else: `weekly` is `52.1775` periods a year, `every two weeks` is half that, `monthly` is `12`, `quarterly` is `4`, `half-yearly` is `2`, `yearly` is `1`, and `every N days` is `365.2425` divided by `N`. Rounding happens half-to-even, at the final step before a figure is shown or returned, and nowhere earlier.
10. The annual figure is the only aggregate that is accumulated. The monthly figure is the annual figure divided by twelve, and the daily figure is the annual figure divided by three hundred and sixty five, each rounded once at the end. The engine's unrounded daily value multiplied by three hundred and sixty five reconstructs the annual value exactly, and its unrounded monthly value multiplied by twelve does the same; only the displayed figures are rounded. A per-day cost computed from a monthly figure that was itself rounded is the named wrong answer.
11. Category subtotals and donut segments must sum exactly to the displayed total, at every period. Distribute the rounding by largest remainder, never by truncation, so no unit is missing anywhere on the overview.
12. Each subscription keeps its entry currency. The account has one home currency and the app ships a dated daily-rate table at least a year deep. A historical figure converts at the rate effective on the charge date; a projection converts at the latest rate; and wherever a converted figure is shown the surface names the rate date it used.
13. Conversion rounds half-to-even to the home currency's minor unit at the last step only. A currency with no minor unit must never grow decimals anywhere: `jpy` prices are whole yen in, whole yen out.
14. Changing the home currency reconverts every figure on screen and changes no stored value. Re-reading any subscription after the change returns the same `price_minor` and the same `currency` it had before.
15. One engine, four mirrors, and their cross-surface equivalence is the point. The overview, the widget routes, the insight charts and the exported file read one code path, and for any store state the four must agree to the minor unit. A cached per-surface total, or a second implementation behind one of the four, cannot hold this and is the named wrong fix.

### Renewal dates and reminders

16. Monthly-family cycles anchor to the first-bill day of the month and clamp to the month end without losing the anchor: a charge anchored on the 31st falls on the 28th in February of a common year, the 29th in a leap year, and returns to the 31st in March. Quarterly, half-yearly and yearly anchors behave identically, so a yearly anchor of `2024-02-29` charges on `2025-02-28` and again on `2028-02-29`.
17. Weekly-family and `every N days` cycles are exact interval arithmetic from the anchor and never clamp.
18. Pausing suspends the sequence; resuming re-anchors forward from the resume date and never back-charges the paused span. A trial inserts its end date as the first paid charge boundary and the price switches on it, so the charge on the trial end date is the post-trial price.
19. The default reminder is the day before each charge, at a local time the owner sets. Per-subscription overrides allow `same_day` and `three_days_before`. Every charge sequence is computed as civil local dates in the owner's zone, and a reminder set for a wall-clock time fires at that wall clock on both sides of a daylight-saving change, so its instant in coordinated universal time moves by an hour across the transition and its local time does not.
20. A reminder is written to the reminders timeline exactly once per charge occurrence. Running the reminder pass twice for the same moment writes no second timeline entry and reports nothing fired the second time. Two passes started at the same moment for the same store must not both write: exactly one completes and the other is rejected with a conflict response, and afterwards each occurrence still has exactly one entry.
21. A pass that runs more than twenty four hours after an occurrence's scheduled instant records that occurrence as `missed` rather than as `fired`, and the timeline says so in words. A missed reminder is never re-announced as if it had arrived on time.

### Import and portability

22. The import sheet accepts pasted text or a dropped text file holding an App Store subscriptions listing. The parser reads the name, the price, the currency, the cycle and the next charge date out of listings written in four locales, and it must handle month-first and day-first dates, comma decimal separators, thin-space thousands groups, and a currency written as a symbol before the amount or as a code after it. These four lines are readable and are the shape the parser is built against: `Lumen Play - Monthly - Renews Jan 15, 2027 - $10.99` is `Lumen Play`, `1099`, `usd`, monthly, `2027-01-15`; `Papercut Stationery - Every 90 days - Renews 17/02/2026 - GBP 18.00` is `Papercut Stationery`, `1800`, `gbp`, every 90 days, `2026-02-17`; `Cellar & Vine - Monatlich - Verlaengert am 05.12.2026 - 24,90 EUR` is `Cellar & Vine`, `2490`, `eur`, monthly, `2026-12-05`; and `Grid & Ember Energy - Annuel - Renouvellement le 01/12/2026 - 1 317,00 EUR` is `Grid & Ember Energy`, `131700`, `eur`, yearly, `2026-12-01`.
23. A row whose name, price, currency, cycle or date could not be read with certainty is returned with `confidence` of `low` and the fields it could not read left empty. The parser never guesses a value it did not read, never crashes on arbitrary text, and returns an empty row list rather than an error for text that holds no listing at all. A parser that recognises only the four lines above is wrong: the rules are the specification, the lines are examples of them.
24. Parsed rows land in a preview table with per-row confidence and editable cells. A row is a duplicate of an existing subscription when the two names match after folding case and dropping every character that is not a letter or a digit, and their annualised costs in the home currency are within five percent of each other. A duplicate offers `Merge` or `Skip` and defaults to neither.
25. Confirming writes every accepted row as one action, so a twelve-row import is one entry on the command stack and one undo reverses all twelve.
26. The export file is comma separated and its header is exactly `name,price_minor,currency,cycle,cycle_days,anchor_date,category,icon,colour,kind,status,cancelled_on,trial_ends_on,trial_price_minor,notes`. Importing an exported file into an empty store reproduces that store: every field of every record comes back with the value it had, to the minor unit, and the round trip loses nothing.

### The receipt reader

27. The `AI Spend` surface reads a receipt and files it. Five sample receipts ship with the app and are offered from a tray; dropping one runs a staged extraction and returns a result card naming the merchant, the date, the total and the line items filed into categories. `receipt-01` is `Kettle Club`, `2026-08-02`, `1200` in `usd`, one line `Filter subscription` under `Cafes & Dining`. `receipt-02` is `Harvest Box`, `2026-08-05`, `1799` in `usd`, one line `Weekly box` under `Groceries`. `receipt-03` is `Cafe Meridien`, `2026-08-09`, `5500` in `aed`, one line `Monthly pass` under `Cafes & Dining`. `receipt-04` is `Thread & Last`, `2026-07-28`, `6500` in `gbp`, one line `Half-year membership` under `Shopping`. `receipt-05` is `Northwind Fibre`, `2026-08-01`, `5500` in `usd`, two lines, `Fibre 300` at `4500` and `Router rental` at `1000`, both under `Utilities`.
28. Any other uploaded image returns the honest state `We could not read this one` with the manual entry form already open, and never a guess.
29. The picture is thrown away. After a scan the uploaded bytes must be absent from the store, from the app's own filesystem and from every response: only the extracted values, a content hash of the bytes and a drawn placeholder thumbnail persist. Uploading the same bytes twice is recognised by that hash and offers the earlier scan rather than filing a second one.
30. Scan history lives with the owner's list under a retention setting in days; entries older than the retention window are gone on the next read. Each entry converts into either a one-time expense or a subscription draft. The whole surface is behind the entitlement.

### Glanceable surfaces

31. Four standalone routes render the glanceable surfaces from real store data with no chrome around them: a small home-screen widget, a medium one, a lock-screen strip and a watch face. Each carries the next charge, its countdown and the monthly total, themeable light or dark, and each is a real route that renders on its own rather than a picture of one.
32. A change made in the main app appears on every widget route within sixty seconds without the route being asked to reload more often than that.
33. The watch face is drawn, not photographed: a rounded-square face carrying the complication rows, the owner's chosen accent colour and the rotating daily affirmation line. Its captured shape is `Streamio Premium · Aug 11 · 2D · 84 AED` over the time `5:58`, the date `SUN 9` and the weather line `Dubai 41`, and everything but the time, the date and the weather is bound to live data.

### Premium and the paywall

34. Free allows six subscriptions with every breakdown, every reminder, every icon and every colour. The seventh opens the paywall sheet, which reuses the pricing band's own cards and copy.
35. The gate lives under the list, not in the interface. A direct request to create a seventh subscription without an active entitlement is refused by the store whatever route it arrives by, including an import batch that would carry the count past six and an undo that would restore a seventh. The refusal names the cap.
36. The `Monthly` and `Yearly` positions reprice live from one stored pair: `799` minor units a month and `2972` minor units a year. Twelve monthly payments are `9588`, so the yearly saving displays as `-69%`, computed from that pair rather than written down twice.
37. Confirming premium writes an entitlement carrying the plan, the start date and the renewal date. Restore, cancel and expiry all exist. Expiry drops the store back to free rules without deleting anything: subscriptions beyond the sixth become read-only, and premium-only data, custom categories and scan history, survives intact and locked.

### Insights

38. A year heatmap gives one cell per day, its intensity set by the amount charged that day, computed from the charge sequences rather than from the subscriptions directly. Hovering a cell names the charges on it, and the same information is available as text without hovering.
39. A twelve-month trend stacks monthly bars by category, exact to the engine, with the current month split visibly into the part already charged and the part still scheduled.
40. Price history lists every change entry with its old price, its new price and its effective date. A month before an increase must be computed at the price that was effective then, never at today's price. This temporal correctness is the point of the whole surface.
41. The trials watch lists trials ending within thirty days, soonest first, calling out the post-trial price. The savings counter totals the avoided cost of every cancelled subscription since its effective date.

### Undo, the bin and the keyboard

42. Every mutation flows through one command stack with undo and redo at least fifty steps deep, and a batch collapses to one step. Undo replays through the engines rather than patching screens, so undoing a price change restores the earlier projections on the overview, in the insight charts and on the widget routes.
43. Each destructive act raises a toast carrying an `Undo` action that stays for eight seconds. The stack is also walkable from the keyboard, and the whole app is reachable without a pointer: a slash focuses search, the arrow keys walk the list, enter opens the focused row, and the editor sheet, the paywall and every confirm trap focus and restore it on close.
44. Deleting is soft for thirty days. A bin in settings lists soft-deleted records with a restore, and a purge is a separate explicit act.

### Sync, snapshot and erasure

45. Two tabs open on the same account converge within one second of any change in either: the second tab shows the new figure without being reloaded by hand.
46. A snapshot export writes one versioned file holding the whole store, the subscriptions, the price history, the entitlement, the settings, the reminder timeline and the scan values, and it may be sealed with a passphrase. Restoring it reproduces an equivalent store. A snapshot whose version is newer than the app knows is refused with a message saying so, and changes nothing.
47. `Delete all data` does what it says in one confirmed step and proves it by returning the account to its first-run state with an empty list and a zero total.
48. A settings meter states the storage in use and warns as it approaches the limit. A write that would exceed the limit fails whole, with a visible error and no partial record left behind.

### The public site

49. The landing page runs fourteen bands in this order: hero, overview, breakdown, reminders, import, AI Spend, widgets, watch, manifesto, privacy manifesto, pricing, questions, threads card, promo and footer. Every band's copy is fixed and is listed in the front-end specification; none of it is improvised.
50. The blog index is titled `Things we learned while staring.` over five cards, each a media figure, a headline and a one-line standfirst. Each card opens an article that reuses the legal reading column.
51. A privacy page is reachable from the footer of every page and states, in its own words, exactly what Driplog keeps about a person and for how long: the subscriptions they typed, the figures read off a receipt, a content hash of any image they dropped, and an anonymous count of route views with no identity attached. It states plainly that the image itself is not kept, that nothing is sold, and that there is no advertising in the product. Its section headings are `Who We Are`, `What We Collect`, `AI Processing (AI Spend)`, `Analytics & Advertising`, `Third-Party Services`, `Website Analytics`, `Purchases`, `Data Storage & Deletion`, `Your Rights` and `Contact`, and it carries the dated line `Last updated: August 11, 2026`.
52. A terms page is reachable from the footer of every page and is linked from the signup form. Its numbered sections are `Eligibility`, `Subscription (Premium)`, `AI Features`, `Receipt Scanning`, `Intellectual Property`, `Trademarks`, `Disclaimer`, `Limitation of Liability`, `Termination` and `Contact`, it carries the dated line `Last updated: July 8, 2026`, and it states the binding product claims: free tracks up to six subscriptions with full features, Premium is monthly or yearly and removes the cap, Driplog does not cancel a real subscription anywhere on anyone's behalf, reminders depend on the device's own settings, and exchange rates are estimates.
53. An address that matches no route renders Driplog's own not-found screen, a floating white pill reading `Page not found` over the paper ground with the navigation still above it, and answers as not found rather than as a page that worked.
54. An anonymous route-view count is kept: one row per public route per day with a count and no identity, readable by a signed-in owner in settings. It records the route and the day and nothing else, which is the whole of the claim the privacy page makes.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the landing page, one long scroll in fourteen bands | public |
| `/blog` | the article index, five editorial cards | public |
| `/blog/<slug>` | one article in the reading column | public |
| `/privacy` | the privacy policy | public |
| `/terms` | the terms of use | public |
| `/sign-in` | account entry | public |
| `/sign-up` | account creation, carrying the terms link | public |
| `/demo` | the read-only demo store the hero renders | public |
| `/app` | the overview: totals, donut, category rows, upcoming timeline | owner |
| `/app/subscriptions/new/basics` | editor sheet, step one | owner |
| `/app/subscriptions/new/cost` | editor sheet, step two | owner |
| `/app/subscriptions/new/schedule` | editor sheet, step three | owner |
| `/app/subscriptions/<id>` | one subscription, edited in the same sheet | owner |
| `/app/import` | paste and file import with the preview table | owner |
| `/app/ai-spend` | the receipt reader and its history | owner |
| `/app/insights` | heatmap, trend, price history, trials, savings | owner |
| `/app/settings` | premium, reminders, data, widgets, bin, storage | owner |
| `/w/small` | the small widget, standalone | owner |
| `/w/medium` | the medium widget, standalone | owner |
| `/w/lock` | the lock-screen strip, standalone | owner |
| `/w/watch` | the watch face, standalone | owner |
| `*` | the not-found pill | public |

**Entry and redirects.** A signed-out request for any `/app` or `/w` route lands on `/sign-in` carrying the intended path and returns there after signing in; with no intended path it lands on `/app`. Signing out returns to `/`. An expired token refuses the action, changes nothing and returns to `/sign-in`. Another owner's subscription, scan or snapshot reads as not found. A request for a seventh subscription from an account without an entitlement returns to the paywall sheet with the cap named and nothing written.

**Journeys.** Open `/`, read the hero, follow `See it in motion` to the promo band and `Get the app` to `/sign-in`; sign in as `user@example.com` and read `$211.80`, `$2,541.55` and `$6.96` on `/app` with `Harvest Box` in the upcoming timeline. Add a seventh subscription and land on the paywall reading `Free to start. Premium when you grow.`; switch the toggle to `Yearly` and watch the premium card reprice to `$29.72` with `-69%` beside it. Sign in as `user2@example.com`, open `/app/import`, paste the four listing lines, watch `Cellar & Vine` flag as a duplicate of the existing record, choose `Skip` for it and `Merge` for none, confirm the rest as one action, then undo once and see the whole batch gone. Open `/app/insights` and read `Northbridge Auto` at `$175.00` in the months before `2026-04-01` and `$185.00` after it. Open `/app/ai-spend`, drop `receipt-05` and file `Fibre 300` and `Router rental` under `Utilities`.

**States.** Every list has an empty state: a first-run `/app` reads `Nothing is tracked yet` with one control to add the first subscription, and the upcoming timeline reads `No charges scheduled` rather than showing an empty frame. Every page has a loading state that reserves the space its content will occupy, so nothing shifts when the figures arrive. Every error is a rendered message naming what happened and what to do, never a blank screen and never a raw stack. A list that fails to load never blanks the totals above it.

## UI/UX notes

The north star: somebody arriving should understand in the first moment that this is a small, opinionated product that tells them one uncomfortable number honestly, and should feel unhurried rather than sold to. The register is editorial consumer, not operational tool: the public half may carry atmosphere and a point of view, and the subject, the product's own screen, must be the first thing seen. Inside `/app` the same system runs at working density, because a ledger a person reads every week is a reading surface and not a dashboard.

The product reads printed rather than lit. The page ground is a near-white warm neutral, nearer uncoated paper than white, with a second, deeper near-white warm neutral for the bands that need to sit back; cards on it are a near-white neutral and the two must stay separate without a dividing line. Ink is a near-black warm neutral, and a second near-black neutral carries the cool dark bands. Secondary text is a mid warm neutral and is reserved for text at lede size or larger, or paired with a stronger twin, so it never carries a small label alone. Exactly one signal colour exists, a mid, vivid red at the orange edge of red, and it appears only on the thing you are meant to press, on an alert and on the numbered step chips; a surface that is none of those must not borrow it. A quiet near-white, muted blue and its mid, soft blue ink carry the small uppercase eyebrow labels and one washed panel, and a near-white cool neutral is that panel's ground. Hairlines are ink at a tenth of its strength and nothing else. Frosted surfaces are white at roughly three quarters strength with the page glowing through. The footer inverts the whole system to a near-black neutral warming toward a near-black warm neutral at its foot, with links in a light cool neutral that brighten to white. One orange ramp runs from the signal colour through a light, vivid orange to a light, soft orange and paints exactly one edge, the hero device frame. The exact values are yours, so long as each holds its role and its exclusivity above.

Type is two sans faces and no more, and they are an identity rather than a preference, so they are named exactly: Inter Tight carries display at weights 600 to 800, Inter carries everything else at 400 to 700, both loaded with swap over the fallback stack `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`. The measured size scale is in the front-end specification and is normative. Figures align down a column wherever amounts stack: the totals card, the category rows, the upcoming timeline, the plan prices and the insight axes.

The whole site sits under a faint film grain, one generated noise tile repeated and blended at low strength, which is the single biggest reason the page reads as paper. It is omitted inside `/app`, where the figures are the subject.

Motion is **eased**: everything has a considered entrance and exit, motion reads as a designed interface rather than a machine responding, and one family of curves governs the whole product. Five moments are named and each must exist as itself. The reveal: headlines split into word spans and assemble word by word, rising from below out of a soft blur into sharpness, siblings stepping a beat behind one another, scroll-triggered per band and played once. The float: the hero device bobs slowly and continuously, as if on water. The pulse: a ring swells out of a live dot and fades. The ring: the reminder card gives one bell-shake wiggle when its band arrives. The cue: the scroll cue wipes vertically from its top and releases from its bottom. Buttons are magnetic, drifting a few pixels toward the pointer within a small radius and returning on leave, and easing to a slightly softer strength while pointed at; where the pointer cannot hover, magnetism is off and the press state carries the feedback. One passage pins the page while its four sentences pass, each word brightening from muted to ink as the scrub reaches it, so the paragraph reads itself onto the page at the speed the reader scrolls. Movement draws on one small vocabulary of curves, each with its own role, the long reveal, the shorter interface move and the spring that carries a pop, and nothing reaches outside that vocabulary for a different speed to feel special. Under a reduced-motion preference the smoothing is off, the reveals become plain appearances, the float, the pulse, the ring and the scrub all hold still, and the promo film does not autoplay; nothing is removed, and the page is complete standing still.

Density is spacious on the public half and comfortable inside the app: the gap between bands is several times the gap under a heading and roughly halves on a narrow screen, every gap is a multiple of one base unit that is yours to choose, and inside the app the rows sit close enough that a week of upcoming charges fits one screen without crowding. Corners are generous to the point of being pills on controls and navigation, softer but still generous on cards and figures, and the footer's top corners are the most generous shape in the product. Shadows are deep and soft rather than tight, as if cards hover just above the page, and there are exactly three of them by role, resting, heroic and small, plus one coloured glow that belongs to the signal colour alone.

The layout archetype is **top-nav**: one floating pill above everything, holding the wordmark and five links and one signal-coloured action, keeping its geometry at every width and folding its link row behind a menu control on a narrow screen. There is no sidebar anywhere in the product.

Each page leads with exactly one primary action, visually distinct from every secondary one, and there is never a second thing on a page competing for that weight: the hero's is the store control with `See it in motion` beside it as the quieter alternative, the pricing band's is `Go Premium` with `Start free` quieter beside it, the empty overview's is the control that adds the first subscription, and the paywall's is `Go Premium`.

Space over dividers: sections read as separate because of the air around them, and a rule is drawn only where two rows of the same kind must be told apart. Calm over expressive inside `/app`: nothing moves while a person is reading a figure, and a total never animates its digits.

The product commits to one mode and designs it fully: the paper ground is the light mode, and it is the mode every surface is drawn for. A dark mode is optional, and the two dark surfaces the product does ship, the privacy band and the footer, are inversions inside the light design rather than a second theme. The glanceable routes are the one exception and carry both, because a phone decides that for itself.

Accessibility is contract, not taste. Body text and its background meet WCAG AA contrast in every theme the product ships, and the same holds for the inverted footer and the dark privacy band. Touch targets are comfortably sized on every surface, at least forty four pixels on their shorter side. Keyboard navigation reaches every control in reading order with a visible focus ring that never depends on the signal colour alone; icon-only controls carry text labels; and meaning is never carried by colour alone, so every chart pairs its hue with a label and a value and every unavailable control says why in words. Word-split headlines stay one accessible string, split visually and not semantically, and the pinned passage reads as one paragraph to assistive technology. Countdowns and the heatmap carry text equivalents. Every content image carries alternative text and every decorative one declares itself decorative.

Responsive behaviour holds at every width between the named tiers rather than only at them. The landing page becomes one column: the hero's device moves below the copy, each band's figure stacks under its own copy, the plan cards stack, and the display type steps down while the pinned passage keeps working. The app is fully usable at phone width: the totals stack above the donut, category rows run full width, the editor sheet becomes full height, and nothing overflows sideways at any viewport, with every navigation target still reachable.

What this must not look like: no page dominated by one hue family with no second signal, no decoration standing in for content, no marketing composition where the working ledger belongs, and no figure rendered as an image when it could be text a reader can select and a screen reader can speak.

## Technical requirements

The stack is fixed. The frontend is **SvelteKit**, server-rendering every route so the browser receives complete, readable markup on first paint, with only the parts that genuinely need behaviour hydrated as islands: the scroll choreography, the editor sheet, the import preview, the pricing toggle and the undo toast. The backend is **Fastify**, serving the HTTP API on the same origin under the `/api` prefix. The datastore is **PostgreSQL**, reached at `DATABASE_URL`. Read every host and port from the environment and never hardcode one.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor. The only backing service available in this environment is PostgreSQL, and reaching for anything else is a contract violation.

Auth is app-implemented: email and password exchanged for a bearer token, passwords stored hashed with a modern password hash, tokens expiring. `GET /api/health` returns `200` once the app is ready. All timestamps are stored in coordinated universal time; every account carries a time zone, and every civil-date calculation resolves in that zone.

The money engine and the date engine are each reachable by exactly one path. The overview, the four widget routes, the insight endpoints and the export all read that path, and for any store state their figures agree to the minor unit. Money is an integer count of minor units with its currency code beside it, in every layer including the browser, and no floating-point money value exists anywhere in the product. The demo store is served read-only: every write against it is refused and every surface rendering it is marked as a demo.

**Simultaneous requests.** When two requests race to write the same reminder occurrence, exactly one of them wins and the other is refused. The loser receives a `409` conflict response naming the occurrence that was already recorded, never a silent success and never a second entry written behind the first. The same holds for the seventh subscription against the free cap and for two snapshot restores started together: exactly one takes effect. A reminder pass replayed for a moment the store has already settled returns the same run summary it returned the first time and must not create a second timeline entry for any occurrence, and an import confirmed twice with the same batch identifier must not create a second set of rows. Choose any mechanism.

**Paginated reads.** Every list endpoint accepts a `page_size` parameter, defaults it to `20` and caps it at `100`. A request naming a page above that cap, for instance `limit=500` written as a page size, is refused with the cap named in the message rather than served with a page quietly cut down to fit. Every list response carries `next_cursor` beside its `data` array together with a `has_more` flag stating whether a further page exists, and that opaque cursor is the only handle a caller ever needs in order to ask for the page after this one. The cursor is a keyset cursor over a stable ordering key rather than an offset cursor, so a list that receives new rows between two reads never repeats a row and never skips one.

**Responsiveness at volume.** The app must stay usable with one thousand subscriptions on one account: the list stays smooth when it is long, an edit made part way down it keeps its focus and does not tear the rows around it, and the totals header must have recomputed before the next frame the reader sees. The widget routes each return a document under fifty kilobytes before their data, and reflect a change made in the main app within sixty seconds.

**Every public route carries its own title and description**, and no two routes share either string. Every public route also declares a social preview title and a social preview image, and that image resolves to a real response from this app's own origin rather than to an address it cannot serve.

**Performance and store version.** The performance bar is the responsiveness stated above rather than a paint measurement, and it holds at the stated volume rather than only on an empty account. The store carries a recorded schema version, and schema migrations are forward only: the app refuses to open a store whose recorded schema version is newer than the one it knows, says so in words, and changes nothing. A migration that cannot finish leaves the previous version readable rather than half-written.

The app makes no outbound network call at run time. The service-name suggestion list, the daily-rate table and the five sample receipts are all fixtures this app serves from its own store.

## Data model

Twelve tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

- `owner`: `id`, `email` unique and compared case-insensitively, `name`, `password_hash`, `home_currency`, `time_zone`, `created_at`.
- `subscription`: `id`, `owner_id` nullable for the demo store, `name`, `price_minor` a non-negative integer, `currency`, `cycle` in `weekly`, `every_two_weeks`, `monthly`, `quarterly`, `half_yearly`, `yearly`, `every_n_days`; `cycle_days` nullable and required only for `every_n_days`; `anchor_date` required; `category_id`, `icon`, `colour`, `kind` in `recurring`, `one_time`; `status` in `active`, `paused`, `cancelled`; `cancelled_on` nullable, `paused_on` nullable, `trial_ends_on` nullable, `trial_price_minor` nullable, `notes`, `deleted_at` nullable. A subscription with `kind` of `one_time` carries its own single date in `anchor_date` and no cycle behaviour.
- `price_change`: `id`, `subscription_id`, `old_price_minor`, `new_price_minor`, `effective_on`, `mode` in `next_renewal`, `correct_history`; `created_at`. Append only: a row is never updated or removed, and the temporal figures are computed from it.
- `category`: `id`, `owner_id` nullable, `name`, `colour`, `builtin`. A builtin category is never deleted. A category with `builtin` false belongs to an owner and may only exist while that owner is entitled.
- `reminder_rule`: `id`, `owner_id`, `subscription_id` nullable, `offset` in `same_day`, `day_before`, `three_days_before`; `local_time`. Exactly one row per owner has a null `subscription_id` and is that owner's default; the rest are sparse overrides.
- `reminder_entry`: `id`, `owner_id`, `subscription_id`, `occurrence_date`, `scheduled_at`, `state` in `fired`, `missed`; `created_at`. At most one row exists for a given subscription and occurrence date, at every moment. Two passes started together for the same occurrence must not both write: exactly one succeeds and the other is rejected.
- `scan`: `id`, `owner_id`, `merchant`, `scanned_on`, `total_minor`, `currency`, `lines`, `content_hash` unique per owner, `thumbnail_kind`, `created_at`. No column of this table, and no file on the app's own disk, holds the bytes of the uploaded image.
- `entitlement`: `id`, `owner_id` unique, `plan` in `monthly`, `yearly`; `state` in `active`, `cancelled`, `expired`; `started_on`, `renews_on`. At most one row per owner. It is what the store consults before a seventh subscription, a custom category or a scan is written.
- `command`: `id`, `owner_id`, `kind`, `payload`, `inverse`, `batch_id` nullable, `position`, `created_at`. Rows sharing a `batch_id` undo and redo together as one step. The stack keeps at least fifty steps per owner.
- `bin_entry`: `id`, `owner_id`, `entity_kind`, `snapshot`, `deleted_at`. A row older than thirty days is gone from every read.
- `rate`: `base_currency`, `quote_currency`, `as_of_date`, `rate`. A bundled read-only fixture, unique per triple, at least a year deep.
- `route_view`: `route`, `on_date`, `count`. Unique per route and date, carrying no identity of any kind.

Derived rather than stored: every per-day, per-month and per-year figure; every category subtotal and donut segment; the next charge date and its countdown; the savings total; the storage meter; and whether a trial is inside its final thirty days.

**Currencies and rates.** The home currency of both seeded accounts is `usd`. The rate table is dated `2026-09-15` at its head and holds, against one unit of the quoted currency in `usd`: `eur` at `1.0850`, `gbp` at `1.2640`, `aed` at `0.2723` and `jpy` at `0.006740`. `jpy` has no minor unit and its prices are whole yen.

**The seven builtin categories** are `Groceries`, `Loans`, `Cafes & Dining`, `Shopping`, `Health & Fitness`, `Entertainment` and `Utilities`.

**Seed data.**

Owners: `user@example.com` (Nadia Ferreira, home currency `usd`, time zone `UTC`, reminder default `day_before` at `09:00`) and `user2@example.com` (Owen Mbeki, home currency `usd`, time zone `America/New_York`, reminder default `day_before` at `09:00`, entitlement `active` on the `monthly` plan).

The demo store carries thirty active recurring subscriptions across five currencies and every cycle, owned by nobody and readable by everybody. Its overview must read `1,262.19 $ per month`, `15,146.33 $ per year` and `41.50 $ per day`, which are `126219`, `1514633` and `4150` in minor units of `usd`.

| Name | Currency | Cycle | Price (minor) | Category | Anchor |
|---|---|---|---|---|---|
| `Harvest Box` | usd | weekly | `1799` | Groceries | `2026-02-04` |
| `Cellar & Vine` | eur | monthly | `2490` | Groceries | `2025-12-05` |
| `Stonemill Bakery` | gbp | every two weeks | `950` | Groceries | `2026-01-09` |
| `Tokyo Pantry` | jpy | monthly | `3800` | Groceries | `2025-10-22` |
| `Orchard Annual Box` | usd | yearly | `253251` | Groceries | `2025-03-15` |
| `Northbridge Auto` | usd | monthly | `18500` | Loans | `2024-01-31` |
| `Sable Student Loan` | usd | monthly | `9200` | Loans | `2023-09-12` |
| `Rivergate Top-up` | usd | yearly | `51600` | Loans | `2024-07-07` |
| `Kettle Club` | usd | monthly | `1200` | Cafes & Dining | `2026-03-31` |
| `Roastline Beans` | usd | every 45 days | `2400` | Cafes & Dining | `2026-05-02` |
| `Bistro Pass` | eur | quarterly | `4500` | Cafes & Dining | `2025-11-30` |
| `Cafe Meridien` | aed | monthly | `5500` | Cafes & Dining | `2026-04-08` |
| `Supper Circle` | usd | yearly | `129019` | Cafes & Dining | `2025-05-20` |
| `Atelier Print Club` | usd | quarterly | `3900` | Shopping | `2026-01-20` |
| `Thread & Last` | gbp | half-yearly | `6500` | Shopping | `2024-03-31` |
| `Papercut Stationery` | usd | every 90 days | `1800` | Shopping | `2026-02-17` |
| `Everyday Carry Club` | usd | yearly | `104663` | Shopping | `2025-08-02` |
| `Basin Lane Fitness` | usd | monthly | `4900` | Health & Fitness | `2025-11-03` |
| `Calm Current` | usd | yearly | `6999` | Health & Fitness | `2024-02-29` |
| `Pilates Quarterly` | eur | quarterly | `5900` | Health & Fitness | `2025-09-30` |
| `Hydra Watch Coach` | aed | weekly | `2500` | Health & Fitness | `2026-06-01` |
| `Bellrock Physio Plan` | usd | yearly | `5308` | Health & Fitness | `2025-04-11` |
| `Streamio Premium` | aed | monthly | `8400` | Entertainment | `2025-08-11` |
| `Lumen Play` | usd | monthly | `1099` | Entertainment | `2026-01-15` |
| `Kinoteca` | eur | quarterly | `2990` | Entertainment | `2025-10-05` |
| `Radiolark` | jpy | monthly | `980` | Entertainment | `2026-04-18` |
| `Playhouse Season Pass` | usd | yearly | `45261` | Entertainment | `2025-06-26` |
| `Northwind Fibre` | usd | monthly | `5500` | Utilities | `2025-06-21` |
| `Vaultline Backup` | usd | yearly | `7900` | Utilities | `2025-02-28` |
| `Grid & Ember Energy` | usd | yearly | `31700` | Utilities | `2024-12-01` |

The demo store's seven category rows, ordered as the overview orders them, are `Groceries` at `36800` a month and `441600` a year, shown as about `4,420 $`; `Loans` at `32000` and `384000`; `Cafes & Dining` at `16700` and `200400`; `Shopping` at `12000` and `144000`; `Health & Fitness` at `11019` and `132233`; `Entertainment` at `8900` and `106800`; and `Utilities` at `8800` and `105600`. The seven monthly figures sum to `126219` and the seven yearly figures sum to `1514633`, exactly.

`user@example.com` holds exactly six active subscriptions, which is the free cap: `Lumen Play` (`usd`, monthly, `1099`, Entertainment, anchor `2026-01-15`), `Basin Lane Fitness` (`usd`, monthly, `4900`, Health & Fitness, anchor `2025-11-03`), `Northwind Fibre` (`usd`, monthly, `5500`, Utilities, anchor `2025-06-21`), `Vaultline Backup` (`usd`, yearly, `7900`, Utilities, anchor `2025-02-28`), `Kettle Club` (`usd`, monthly, `1200`, Cafes & Dining, anchor `2026-03-31`) and `Harvest Box` (`usd`, weekly, `1799`, Groceries, anchor `2026-02-04`). That account's overview reads `21180` a month, `254155` a year and `696` a day, which display as `$211.80`, `$2,541.55` and `$6.96`.

`user2@example.com` holds nine active subscriptions: `Streamio Premium` (`aed`, monthly, `8400`, Entertainment, anchor `2025-08-11`), `Northbridge Auto` (`usd`, monthly, `18500`, Loans, anchor `2024-01-31`), `Calm Current` (`usd`, yearly, `6999`, Health & Fitness, anchor `2024-02-29`), `Thread & Last` (`gbp`, half-yearly, `6500`, Shopping, anchor `2024-03-31`), `Roastline Beans` (`usd`, every 45 days, `2400`, Cafes & Dining, anchor `2026-05-02`), `Cellar & Vine` (`eur`, monthly, `2490`, Groceries, anchor `2025-12-05`), `Radiolark` (`jpy`, monthly, `980`, Entertainment, anchor `2026-04-18`), `Pilates Quarterly` (`eur`, quarterly, `5900`, Health & Fitness, anchor `2025-09-30`) and `Atelier Print Club` (`usd`, quarterly, `3900`, anchor `2026-01-20`) in that owner's one custom category `Studio`. Those nine read `31159` a month, `373910` a year and `1024` a day, which display as `$311.59`, `$3,739.10` and `$10.24`.

`user2@example.com` also holds: one price change on `Northbridge Auto` from `17500` to `18500` effective `2026-04-01` in `next_renewal` mode, so every month before April 2026 computes at `175.00` and every month from it computes at `185.00`; one trial, `Foldspace Studio` (`usd`, monthly, post-trial price `1499`, category `Studio`) whose trial ends `2026-09-28`; one cancelled record, `Kinoteca` (`eur`, quarterly, `2990`, Entertainment) cancelled effective `2026-06-30`, feeding the savings counter; one one-time expense, `Winter Tyres` (`usd`, `24000`, Shopping) dated `2026-08-14`; and two scan entries, from `receipt-01` and `receipt-05`.

The service-name suggestion fixture carries every subscription name listed above with its glyph initial and its default colour. The five sample receipts are `receipt-01` through `receipt-05` with the extractions pinned in Core features.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

### Type and the measured scale

Two families and no more, both loaded with swap from a hosted font service over the fallback stack `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`: Inter Tight for display at weights 600 to 800, Inter for everything else at 400 to 700. There is no third family and no serif anywhere; identifiers and figures use Inter with tabular figures rather than a monospace face. The scale below is measured and normative.

| Size | Weight | Line height | Use |
|---|---|---|---|
| `103.68px` | 800 | `107.827px` | hero display, wide desktop |
| `93.6px` | 800 | `91.728px` | hero display, at the capture width |
| `64.35px` | 800 | `1.0` | the manifesto words |
| `58px` to `60px` | 600 | `1.1` | band headlines |
| `41.58px` | 600 | `45.7px` | band headlines, tablet |
| `50px` | 800 | `51px` | the footer call to action |
| `28px` | 600 | `31.92px` | card titles |
| `24px` | 700 | `31.2px` | plan prices |
| `19px` | 700 | `30.4px` | question rows |
| `17px` | 400 | `27.2px` | lede paragraphs |
| `16px` | 400 | `25.6px` | body |
| `14px` | 400 to 600 | `22.4px` | fine print and buttons |
| `12px` | 700 | `19.2px` | eyebrows, uppercase and letterspaced, in the periwinkle ink |

Display headlines are set tight and carry italic emphasis spans: the hero's second sentence is italic, and the breakdown band's third line `Per day.` is italic.

### Ground, grid and grain

The content column is one fixed maximum width with a side padding that grows with the viewport and stops growing at a comfortable maximum. The layout changes at six measured steps as the window narrows, and a tablet window sits between the widest phone step and the desktop column; hover styling applies only where the pointer can hover, and every reduced-motion rule is normative rather than decorative.

A film grain sits over the whole public site: one generated fractal-noise tile, drawn once at a small square size and repeated, blended multiply at a little over a third strength. It is one repeated tile and never a full-viewport repaint, and it is omitted inside `/app`.

### Radius, shadow and glass

Corners run a scale by role rather than by taste: a full pill on navigation, buttons and toggles; the most generous soft corner on plan and feature cards; a smaller soft corner on media figures and app cards; a distinct larger corner on the hero device with a tighter one on the screen inside it; a small soft corner on the frosted code card; full rounds on chips and circular controls; and the footer's top corners the most generous shape on the page, stepping down on a narrow screen.

Shadows are three by role and one by colour: a resting card shadow, a deeper heroic one for the cards that must float, a small tight one for chips and small controls, and one glow in the signal colour that belongs to the primary action, the closing CTA and the pricing toggle's knob and to nothing else. A periwinkle panel carries its own soft glow. The beta sheet lifts on a broad upward shadow and the footer badge on a tight dark one.

The navigation pill is liquid glass: a translucent white tint that deepens as the page scrolls, a diagonal sheen running across it, a brighter edge, and a backdrop distortion that blurs and lifts the saturation of whatever passes beneath. Where an engine cannot produce a backdrop effect, the pill falls back to the solid frosted surface and nothing else changes.

### Iconography and the mark

The wordmark is set in Inter Tight at its heaviest weight. The app icon is a drawn rounded square in the signal colour carrying a white bold letterform. Functional icons are stroke vectors on a twenty four unit box that inherit the colour of the text beside them: an up arrow for back-to-top, the same arrow rotated for the footer contact affordance, a plus for the question rows, and a paired speaker for the promo sound control, one with mute strokes and one with sound waves. Numbered step chips are small circles in the signal colour carrying white digits `1`, `2` and `3`. The footer carries six monochrome social marks, drawn as paths, resting in the light cool neutral and brightening to white.

No binary asset ships. This is the zero-asset substitution guide, and every item below is the substitution for something the reference product shipped as a file. The hero device is drawn: an ink body, the orange ramp as its frame edge, a drawn camera pill, and its screen is the live overview component rendering the demo store rather than a film. The editorial figures, the breakdown portrait, the watch arm, the threads card and the import hand, are seeded procedural art direction, layered soft radial gradients in band-specific palettes with the grain over them, each carrying its caption. The code card by the hero is a decorative, non-scannable finder pattern, three corner squares and a seeded dot grid in ink on white behind frosted glass, labelled as decorative, with the whole card linking onward. The store badge is a drawn rounded rectangle with an ink ground, a white border, a drawn platform glyph and a two-line label. The push card is a drawn notification: leading app glyph, bold first line, body line, timestamp, on frosted white. The promo band renders a drawn poster, ink ground, wordmark and a play affordance, and plays a scripted tour built from the real app surfaces with the sound toggle honoured.

### Global chrome

First paint is a loader: a paper-cream cover holding the wordmark alone. The loader fades out once the fonts and the hero are ready, and it never returns on a later navigation inside the site. The navigation pill floats above all content, keeps its geometry at every width and folds its link row behind a menu control below the tablet step. A circular frosted button sits at the bottom right, hidden until the first band has passed, rising into place and scrolling smoothly to the top. The promo figure carries a circular sound toggle that swaps the two speaker glyphs.

The footer inverts the page. It carries the giant call to action `Download Driplog to get Started` with the app-icon glyph standing in for the wordmark's first letter; the drawn store badge over the fine line `iPhone · iOS 17+ · Free to start`; a `Join beta` link; a brand row with the six social marks; the row `Driplog`, `Help Center`, `Contact us`, `Privacy Policy`, `Terms of Use`; and the line `(C) 2026 Driplog. All rights reserved.` `Help Center` is plain text because the help centre is not part of this build. `Contact us` reaches `hello@driplog.app`. The store badge lifts slightly when pointed at and the contact link brightens to white along with its drawn underline.

`Join beta` opens a bottom sheet over a dimmed backdrop, rounded at the top, carrying a close cross, the display copy `Be the first one` and `to be onboard`, and one signal-coloured pill `Join Beta`. It rises on the spring, closes on the cross, on the backdrop or on Escape, and traps focus while open.

### The fourteen bands, in order

1. **Hero.** Left: the display headline `All your subscriptions. And what they really cost.` with the second sentence italic, assembling word by word on load rather than on scroll; the lede `Everything you pay for in one place, the honest total per day, month and year, and a quiet nudge the day before the money leaves.`; the signal-coloured pill `Download on the App Store` and the ghost pill `See it in motion`, which scrolls smoothly to the promo band. Right: the drawn device, bobbing, its screen the live overview rendering the demo store, with the decorative frosted card floating at its foot.
2. **Overview.** Eyebrow `Overview`; headline `See how much you really spend.`; a device figure showing the overview screen; the lede `Open the app and the sums are already done. How many you are paying for, what it costs a month and a year, no spreadsheet in sight. The next charges line up below, nearest first, so nothing sneaks up on you.`; three ticks, `Live monthly & yearly totals`, `A countdown to every charge`, `Any currency, converted at daily rates`.
3. **Breakdown.** Eyebrow `Breakdown`; the three-line headline `Per year. Per month. Per day.` with the last line italic; the lede `That "cheap" annual plan, divided by 365, is still a small daily habit. Driplog shows the number that actually lands each day, so renewing becomes a choice instead of a reflex.`; an editorial portrait figure, sunlit and warm, built procedurally.
4. **Reminders.** Eyebrow `Reminders`; headline `Never get surprise-charged again.`; the lede `The day before the money leaves, a gentle tap on the shoulder. So you renew because you meant to, not because you forgot it was there.`; a figure carrying a stack of drawn push cards that arrive with the bell-shake, the face reading `Subscription Reminder: Tomorrow is your Fitness App renewal`.
5. **Import.** Eyebrow `Setup · One screenshot`; headline `Import what Apple already charges you for.`; the lede `Everything on your Apple ID sits on one screen. Screenshot it, drop it in, and we read the names, prices and dates for you.`; three numbered chips, `Open Subscriptions`, `Take a screenshot`, `Drop it in here`; and the live import surface presented full bleed on a signal-coloured panel, carrying its own copy `Import your Apple subscriptions`, `Open App Store`, `Upload screenshots` and `Add manually`.
6. **AI Spend.** Eyebrow `Premium · AI Spend`; headline `Snap a receipt. Let AI do the math.`; the lede `Typing receipts is a chore. Snapping one is a tap. The AI pulls out the numbers, files them into categories, and throws the photo away.`; a dark heroic card carrying the live reader surface in demo mode.
7. **Widgets.** Eyebrow `Premium · Widgets`; headline `Your next payment, right on the Home Screen.`; the lede `What is due next, on the Home and Lock Screen. You find out without opening the app, which is the highest praise an app can get. Comes with Premium.`; a device figure carrying the live widget routes.
8. **Watch.** Eyebrow `Apple Watch`; headline `The next charge, on your wrist.`; the lede `A complication on the watch face shows what is due next and what it costs. Pick its colour right on the watch. The daily affirmation lives there too.`; a drawn watch with an aqua-on-ink procedural arm, an orange drawn strap and the complication bound to live data.
9. **Manifesto.** The pinned passage, four sentences at the manifesto size, each word inking from muted to ink as the scrub passes it, with `Roughly` and `one honest number` flipping to italic display emphasis: `You know roughly what you pay every month. Roughly is the problem. All your subscriptions. We counted ours and cancelled three the same evening. Driplog turns that quiet leak into one honest number you can act on.`
10. **Privacy manifesto.** A dark band: the display headline `Private by Design.`; the paragraph `What you pay for lives in your own private space, not in a shared ledger. We never sell it, and there are no ads in the app. We do count anonymous taps, so we know which screen to fix next. That is the entire list.`; four badge chips, `Private sync`, `No ads in the app`, `No data sold`, `Anonymous stats only`.
11. **Pricing.** Eyebrow `Pricing`; headline `Free to start. Premium when you grow.`; a `Monthly` and `Yearly` toggle whose knob carries the signal-coloured glow and whose yearly position shows `-69%`; two plan cards at the most generous corner. `Free`, `$0`, `Enough to see the whole picture.`, with the ticks `Up to 6 subscriptions`, `Per day / month / year breakdowns`, `Renewal reminders`, `Custom icons & colours`, `Private sync & privacy`, and the ghost button `Start free`. `Premium`, flagged `Most popular` in a signal-coloured chip, `$7.99 /mo` under the monthly position over `Billed monthly. Cancel anytime.`, carrying the premium gradient wash, with the ticks `Unlimited subscriptions`, `AI Spend: scan receipts & statements`, `Widgets for Home and Lock Screen`, `Personal calculation categories`, `Everything in Free`, `Support an app with zero ads`, and the signal-coloured button `Go Premium`. The toggle reprices the premium card for real.
12. **Questions.** Eyebrow `FAQ`; headline `Good questions.`; six hairline-divided rows, each with a signal-coloured plus that rotates a quarter turn when open, each a real disclosure control. `Do I have to connect my bank?` answers `Never. Driplog doesn't touch your bank. You add subscriptions yourself. Takes a minute, and nothing about your finances ever leaves your hands.` `Where is my data stored?` answers `Your subscriptions sit in your own private space, tied to your account and synced across your devices. Nobody else can read them, and we never sell them.` `Do you track me?` answers `Not your money. We count anonymous events like "opened the app" or "added a subscription", and nothing else. No names, no amounts, no subscription list, and no advertising identifier. The full breakdown is in the privacy policy.` `What do I get for free?` answers `Up to six subscriptions with full breakdowns, reminders, custom icons and private sync. When six stops being enough, Premium unlocks unlimited subscriptions and the AI Spend scanner.` `How does AI Spend handle my receipts?` answers `AI reads the numbers and forgets the picture. Images are analysed, values extracted, photo discarded. We keep only hashes, never the pictures.` `Can I cancel Premium anytime?` answers `Yes, in two taps. Your free plan keeps working. No hard feelings.`
13. **Threads card.** A procedural gradient card at the most generous corner advertising the maker's feed, labelled with the drawn platform glyph and `@driplog`.
14. **Promo and footer.** The promo figure, the target of `See it in motion`, scales up as it enters and plays muted inline with the sound toggle beside it; then the closing footer with its soft periwinkle glow behind the call to action.

### Blog, legal and not-found

`/blog` is titled `Things we learned while staring.` over five cards, each a media figure, a headline and a one-line standfirst, entering with the reveal grammar as they scroll in, the small signal-coloured chip on a card softening when the card is pointed at.

| Title | Standfirst |
|---|---|
| `Too Lazy to Type In Every Expense? Let AI Read Your Receipts` | `Manual expense entry is why most spending trackers get abandoned. AI Spend in Driplog reads receipts and statements from a photo and does the math for you.` |
| `How Much Do Your Subscriptions Really Cost Per Year?` | `The average person pays for 12 subscriptions and remembers four. Here is how to find your real yearly number in five minutes, and what to do with it.` |
| `Forgot to Cancel a Free Trial? Here Is How to Stop Paying for It` | `Free trials are built to be forgotten. Here is how to cancel them on iPhone, get a refund when you are charged, and never let it happen again.` |
| `The Best Way to Track Subscriptions on iPhone in 2026` | `Spreadsheets, bank apps, iOS settings or a dedicated tracker? An honest comparison of every way to track subscriptions on iPhone, with a privacy checklist.` |
| `Subscription Creep: Why Your Money Quietly Disappears Every Month` | `Subscription creep is the slow stacking of small recurring charges plus silent price increases. Here is how it works on your psychology and how to beat it.` |

The legal shell is the navigation, a narrow reading column on the paper ground, the title with its dated meta line, subheaded sections, tick lists separated by hairlines, and the full footer with its beta sheet. Links underline when pointed at, and the `Join beta` link carries a drawn underline that wipes in from its left edge. The five blog articles reuse this shell.

The not-found screen is a floating white pill at a full round with the deep card shadow, reading `Page not found` over the paper ground, with the navigation intact above it and a minimal footer below.

### The application surfaces

The app uses the same tokens at working density, with the grain off and white cards on the paper ground. The overview is the specification for the hero's screen and for the widget miniatures: one component, three modes, never three implementations. It carries the segmented header `Calculator` and `AI Spend`, the title `Your spending`, the `All` and `Recurring` and `One-time` filter, the totals card with the monthly figure left, the yearly right and the multi-hue donut between them, the line `Based on your regular and one-time expenses`, then `Where your money goes`, then the upcoming timeline. A floating signal-coloured plus opens the editor sheet. In demo mode the whole surface is read-only and carries a visible mark saying so.

The toast, the sheet and the confirm are one primitive each for the entire product, so an undo toast on the overview and an undo toast in the import preview are the same object in two places.

## Constraints

One person per list and one home currency at a time. No bank connection, no card, no real payment: the entitlement is stateful but its purchase is simulated inside this app. No second owner on a list, no sharing, no invitation, no comment, no like, no follow and no messaging. No email, no push service and no outbound notification of any kind: the reminders timeline inside the app is the only delivery channel this build has. No file upload except the receipt image, whose bytes are never kept. No object storage, no queue, no cache and no second datastore. No third-party sign-in, no magic link and no password reset by mail. No third-party analytics, advertising or measurement vendor, and no outbound network call at run time for any reason, including fonts, rates and brand logos, all of which this app serves itself. No native or mobile application: the widget and watch surfaces are browser routes. No search engine, no recommendation and no machine-learned model: the receipt reader is a staged fixture and says so. Driplog never cancels a real subscription anywhere on anybody's behalf. The app must stay responsive with 1000 subscriptions, 200 price changes, 5000 reminder entries and 2000 command rows on one account.

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

**API shapes.** Every `/api/app` route takes a bearer token; signup, login, health, the demo store and the public content routes do not. Every list endpoint returns a JSON object carrying a top-level `data` array plus `next_cursor` and `has_more`. Every money field is an integer of minor units and carries its `currency` beside it.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `name` | `access_token`, `owner` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `owner` |
| `GET /api/auth/me` | | `owner` with `home_currency` and `time_zone` |
| `GET /api/demo/overview` | `filter` | `month_minor`, `year_minor`, `day_minor`, `currency`, `categories`, `upcoming`, `read_only` |
| `GET /api/content/pricing` | | `plans` with `monthly_minor`, `yearly_minor`, `saving_percent` |
| `GET /api/content/posts` | `page_size`, `cursor` | `data` of posts with `slug`, `title`, `standfirst` |
| `GET /api/app/overview` | `filter` | `month_minor`, `year_minor`, `day_minor`, `categories` with `month_minor`, `year_minor` and `year_approx_minor`, `upcoming` with `charge_date` and `days_remaining` |
| `GET /api/app/subscriptions` | `page_size`, `cursor`, `filter`, `status` | `data`, `next_cursor`, `has_more` |
| `POST /api/app/subscriptions` | the record fields | the subscription |
| `GET /api/app/subscriptions/{id}` | | the subscription with its `price_changes` |
| `PATCH /api/app/subscriptions/{id}` | the changed fields, `price_change_mode` | the subscription and the new `price_change` |
| `POST /api/app/subscriptions/{id}/pause` | | the subscription |
| `POST /api/app/subscriptions/{id}/resume` | | the subscription |
| `POST /api/app/subscriptions/{id}/cancel` | `effective_date` | the subscription and the savings entry |
| `DELETE /api/app/subscriptions/{id}` | | the bin entry |
| `GET /api/app/subscriptions/{id}/charges` | `from`, `to` | `charge_dates`, and `prices`, a map from each charge date to the price in minor units effective on that date |
| `POST /api/app/categories` | `name`, `colour` | the category, or a refusal when the account holds no active entitlement |
| `GET /api/app/insights/heatmap` | `year` | `days` with `on_date`, `total_minor`, `charges` |
| `GET /api/app/insights/trend` | | twelve `months` with `category_totals`, `charged_minor`, `scheduled_minor` |
| `GET /api/app/insights/price-history` | `page_size`, `cursor` | `data` of changes with `old_price_minor`, `new_price_minor`, `effective_on` |
| `GET /api/app/insights/trials` | | `trials` ending within thirty days, soonest first |
| `GET /api/app/insights/savings` | | `saved_minor` and one row per cancelled subscription |
| `POST /api/app/import/parse` | `text` | `rows` with `name`, `price_minor`, `currency`, `cycle`, `next_charge_date`, `confidence`, `duplicate_of` |
| `POST /api/app/import/commit` | `rows`, `batch_id` | `created`, `skipped`, `batch_id` |
| `GET /api/app/export.csv` | | the pinned header and one line per record |
| `POST /api/app/import/csv` | the file | `created` and the restored store |
| `GET /api/app/export/snapshot` | `passphrase` | the sealed versioned snapshot |
| `POST /api/app/import/snapshot` | the snapshot, `passphrase` | the restored store, or a refusal naming the version |
| `POST /api/app/scans` | `sample_id`, or the uploaded image | the scan with `merchant`, `scanned_on`, `total_minor`, `lines`, `content_hash` |
| `GET /api/app/scans` | `page_size`, `cursor` | `data`, `next_cursor`, `has_more` |
| `GET /api/app/entitlement` | | `plan`, `state`, `started_on`, `renews_on` |
| `POST /api/app/entitlement/subscribe` | `plan` | the entitlement |
| `POST /api/app/entitlement/cancel` | | the entitlement |
| `POST /api/app/entitlement/restore` | | the entitlement |
| `GET /api/app/reminders/schedule` | `from`, `to` | `occurrences` with `subscription_id`, `occurrence_date`, `local_time`, `scheduled_at` |
| `POST /api/app/reminders/run` | `as_of` | `fired`, `missed`, `skipped` |
| `GET /api/app/reminders/timeline` | `page_size`, `cursor` | `data`, `next_cursor`, `has_more` |
| `POST /api/app/undo` | | the reverted command and the store after it |
| `POST /api/app/redo` | | the reapplied command |
| `GET /api/app/bin` | `page_size`, `cursor` | `data`, `next_cursor`, `has_more` |
| `POST /api/app/bin/{id}/restore` | | the restored record |
| `GET /api/app/settings` | | `home_currency`, `time_zone`, `reminder_default`, `retention_days`, `theme`, `storage_used_bytes` |
| `PATCH /api/app/settings` | the changed fields | the settings |
| `GET /api/app/stats/views` | | one row per route and day with its `count` |
| `POST /api/app/data/delete-all` | `confirm` | the emptied first-run state |
| `GET /api/health` | | `200` |

A successful call returns the named resource or shape. An invalid, unauthorized or out-of-state call is rejected as a client error, never a `5xx` and never a silent success, and carries a stable machine-readable `code` and a human `message`.

**No mocks.** The subscriptions, the price changes, the reminder entries, the scans, the entitlements, the commands and the bin live in PostgreSQL and nowhere else. An in-memory array of subscriptions, a totals figure held in a module variable, a JSON file of records on the app's own disk, a figure the app prints without reading the rows beneath it, or an image kept on the container's filesystem after a scan are all contract violations however good the interface looks. PostgreSQL is the fact: the app's screens and its own caches can only reflect what lives there, never substitute for it.

## Definition of done

A person can read the landing page, sign in, and see their real monthly, yearly and daily cost with the next charge counted down at the top, in any currency, exact to the minor unit on every surface that shows it. A subscription anchored to the end of a month charges on the right day in every month after it, leap February included. The day-before reminder reaches the timeline exactly once per charge. A seventh subscription on a free account is refused under the list rather than hidden above it.
