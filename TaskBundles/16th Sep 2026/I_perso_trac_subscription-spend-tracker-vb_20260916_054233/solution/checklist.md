# Checklist: Driplog

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 712
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public landing page at the site root. `src: Overview para 2`
- [ ] `C-OV-02` `capability` The app serves a blog index of five article cards. `src: Overview para 2`
- [ ] `C-OV-03` `capability` The app serves a privacy policy page. `src: Overview para 2`
- [ ] `C-OV-04` `capability` The app serves a terms page. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The app serves a not-found screen for an unmatched address. `src: Overview para 2`
- [ ] `C-OV-06` `capability` The app serves the tracker at `/app` behind a sign-in. `src: Overview para 2`
- [ ] `C-OV-07` `capability` The app shows a per-day cost figure. `src: Overview para 1`
- [ ] `C-OV-08` `capability` The app shows a per-month cost figure. `src: Overview para 1`
- [ ] `C-OV-09` `capability` The app shows a per-year cost figure. `src: Overview para 1`
- [ ] `C-OV-10` `capability` The app raises a reminder the day before a charge. `src: Overview para 1`
- [ ] `C-OV-11` `constraint` The app excludes comments from the product surface. `src: Overview para 3`
- [ ] `C-OV-12` `constraint` The app excludes sharing from the product surface. `src: Overview para 3`
- [ ] `C-OV-13` `constraint` The app excludes following from the product surface. `src: Overview para 3`
- [ ] `C-OV-14` `constraint` The app excludes messaging from the product surface. `src: Overview para 3`
- [ ] `C-OV-15` `constraint` The app never connects to a bank. `src: Overview para 3`
- [ ] `C-OV-16` `constraint` The app never cancels a real subscription on a person's behalf. `src: Overview para 3`
- [ ] `C-OV-17` `constraint` The app invents no minor unit anywhere between the store surface, the screen. `src: Overview para 4`
- [ ] `C-OV-18` `constraint` The app clamps a charge anchored to the 31st into a short month. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads the landing page. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor reads the blog index. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor reads each of the five articles. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A signed-out visitor reads the privacy policy. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A signed-out visitor reads the terms page. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A signed-out visitor opens the read-only demo store. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A signed-out visitor signs up for an account. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A signed-out visitor signs in to an existing account. `src: User roles table row 1`
- [ ] `C-RL-09` `constraint` A signed-out visitor never reads a real subscription belonging to anybody. `src: User roles table row 1`
- [ ] `C-RL-10` `constraint` A signed-out visitor never creates a real subscription belonging to anybody. `src: User roles table row 1`
- [ ] `C-RL-11` `constraint` A signed-out visitor never changes a reminder belonging to anybody. `src: User roles table row 1`
- [ ] `C-RL-12` `constraint` A signed-out visitor never changes an entitlement belonging to anybody. `src: User roles table row 1`
- [ ] `C-RL-13` `role` A signed-in owner reads every subscription on the owner's own list. `src: User roles table row 2`
- [ ] `C-RL-14` `role` A signed-in owner changes a setting on the owner's own list. `src: User roles table row 2`
- [ ] `C-RL-15` `role` A signed-in owner exports the owner's own list. `src: User roles table row 2`
- [ ] `C-RL-16` `role` A signed-in owner erases the owner's own list. `src: User roles table row 2`
- [ ] `C-RL-17` `constraint` A signed-in owner never reads a subscription belonging to another owner. `src: User roles table row 2`
- [ ] `C-RL-18` `constraint` A signed-in owner never exceeds the free cap without an active entitlement. `src: User roles table row 2`
- [ ] `C-RL-19` `constraint` The server rejects an unauthorized mutating request rather than serving the request. `src: User roles, authorization paragraph`
- [ ] `C-RL-20` `constraint` The server leaves protected state unchanged after rejecting an unauthorized request. `src: User roles, authorization paragraph`
- [ ] `C-RL-21` `constraint` The server answers a request for another owner's record as not found. `src: User roles, authorization paragraph`
- [ ] `C-RL-22` `capability` The app offers an open signup route. `src: User roles, signup paragraph`
- [ ] `C-RL-23` `literal` The app signs in `user@example.com` with the seeded password. `src: User roles, signup paragraph`
- [ ] `C-RL-24` `literal` The app signs in `user2@example.com` with the seeded password. `src: User roles, signup paragraph`
- [ ] `C-RL-25` `constraint` The app refuses every write against the demo store. `src: User roles, signup paragraph`
- [ ] `C-RL-26` `ui` The app marks every surface rendering the demo store as a demo. `src: User roles, signup paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app exchanges an email with a password for a bearer token. `src: Core features, Auth`
- [ ] `C-CF-02` `constraint` The app stores a password hashed. `src: Core features, Auth`
- [ ] `C-CF-03` `constraint` The app rejects a request carrying an expired token. `src: Core features, Auth`
- [ ] `C-CF-04` `constraint` The app performs no mutation for a request carrying an absent token. `src: Core features, Auth`
- [ ] `C-CF-05` `constraint` The app refuses a signup for an address already registered. `src: Core features, Auth`
- [ ] `C-CF-06` `constraint` The app refuses a signup password under ten characters. `src: Core features, Auth`
- [ ] `C-CF-07` `ui` The app names the refused field on a refused signup. `src: Core features, Auth`
- [ ] `C-CF-08` `ui` The signup form carries a link to the terms page. `src: Core features, Auth`
- [ ] `C-CF-09` `data` A subscription record stores a name. `src: Core features, the subscription record`
- [ ] `C-CF-10` `data` A subscription record stores a price as integer minor units. `src: Core features, the subscription record`
- [ ] `C-CF-11` `data` A subscription record stores a currency code beside the price. `src: Core features, the subscription record`
- [ ] `C-CF-12` `data` A subscription record stores a billing cycle drawn from the seven named cycles. `src: Core features, the subscription record`
- [ ] `C-CF-13` `data` A subscription record stores a first-bill anchor date. `src: Core features, the subscription record`
- [ ] `C-CF-14` `data` A subscription record stores a kind of `recurring` or `one-time`. `src: Core features, the subscription record`
- [ ] `C-CF-15` `data` A subscription record stores a status of `active`, `paused`, or `cancelled`. `src: Core features, the subscription record`
- [ ] `C-CF-16` `ui` The overview shows the monthly figure at the left of the totals card. `src: Core features rule 1`
- [ ] `C-CF-17` `ui` The overview shows the yearly figure at the right of the totals card. `src: Core features rule 1`
- [ ] `C-CF-18` `ui` The overview shows a multi-hue donut between the two totals. `src: Core features rule 1`
- [ ] `C-CF-19` `literal` The overview carries the title `Your spending`. `src: Core features rule 1`
- [ ] `C-CF-20` `ui` The overview carries a note line beneath the totals card naming regular expenses, one-time expenses. `src: Core features rule 1`
- [ ] `C-CF-21` `literal` The overview carries a segmented header offering `Calculator`, `AI Spend`. `src: Core features rule 1`
- [ ] `C-CF-22` `literal` The overview carries a filter offering `All`, `Recurring`, `One-time`. `src: Core features rule 1`
- [ ] `C-CF-23` `literal` The overview carries the heading `Where your money goes`. `src: Core features rule 2`
- [ ] `C-CF-24` `capability` Each category row carries an exact per-month figure. `src: Core features rule 2`
- [ ] `C-CF-25` `capability` Each category row carries a per-year approximation rounded to the nearest ten units of the home currency. `src: Core features rule 2`
- [ ] `C-CF-26` `constraint` The category rows are ordered by the monthly figure, largest first. `src: Core features rule 2`
- [ ] `C-CF-27` `ui` The upcoming charges run as a timeline ordered nearest first. `src: Core features rule 3`
- [ ] `C-CF-28` `ui` Each upcoming row carries a countdown chip stating whole days remaining. `src: Core features rule 3`
- [ ] `C-CF-29` `constraint` The countdown turns over at local midnight in the owner's zone. `src: Core features rule 3`
- [ ] `C-CF-30` `ui` Creating a subscription opens a sheet rising from the bottom edge. `src: Core features rule 4`
- [ ] `C-CF-31` `capability` The editor sheet carries three steps, each with its own address. `src: Core features rule 4`
- [ ] `C-CF-32` `constraint` Leaving the editor sheet at any step writes nothing. `src: Core features rule 4`
- [ ] `C-CF-33` `capability` Reloading an editor step returns to that step with the entered values intact. `src: Core features rule 4`
- [ ] `C-CF-34` `constraint` The app refuses a negative price without writing anything. `src: Core features rule 4`
- [ ] `C-CF-35` `constraint` The app refuses an absent anchor date without writing anything. `src: Core features rule 4`
- [ ] `C-CF-36` `literal` Editing a price asks `Apply from next renewal` or `Correct history` before saving. `src: Core features rule 5`
- [ ] `C-CF-37` `data` Editing a price writes a price-change entry under either answer. `src: Core features rule 5`
- [ ] `C-CF-38` `constraint` The `Apply from next renewal` answer leaves every past month computed at the old price. `src: Core features rule 5`
- [ ] `C-CF-39` `constraint` The `Correct history` answer recomputes every past month at the new price. `src: Core features rule 5`
- [ ] `C-CF-40` `constraint` The two answers produce different insight histories for the same edit. `src: Core features rule 5`
- [ ] `C-CF-41` `capability` Cancelling asks for the effective date. `src: Core features rule 6`
- [ ] `C-CF-42` `constraint` Cancelling keeps every past charge. `src: Core features rule 6`
- [ ] `C-CF-43` `data` Cancelling moves the record to the cancelled ledger. `src: Core features rule 6`
- [ ] `C-CF-44` `capability` Cancelling starts accruing avoided cost from the effective date. `src: Core features rule 6`
- [ ] `C-CF-45` `constraint` Cancelling never deletes the record. `src: Core features rule 6`
- [ ] `C-CF-46` `constraint` A cancelled subscription never appears in the upcoming timeline. `src: Core features rule 6`
- [ ] `C-CF-47` `capability` Typing a name in the editor suggests from the bundled offline service fixture. `src: Core features rule 7`
- [ ] `C-CF-48` `constraint` The suggestion list reaches no service outside the app. `src: Core features rule 7`
- [ ] `C-CF-49` `constraint` A one-time expense joins the `All` view only in the calendar month of the expense. `src: Core features rule 8`
- [ ] `C-CF-50` `constraint` The `Recurring` filter excludes every one-time expense. `src: Core features rule 8`
- [ ] `C-CF-51` `constraint` The `All` figures equal `Recurring` plus `One-time` to the minor unit. `src: Core features rule 8`
- [ ] `C-CF-52` `constraint` No floating-point value reaches the API as a money figure. `src: Core features, the honest-math engine`
- [ ] `C-CF-53` `constraint` No floating-point value reaches the screen as a money figure. `src: Core features, the honest-math engine`
- [ ] `C-CF-54` `literal` A `weekly` cycle annualises at `52.1775` periods a year. `src: Core features rule 9`
- [ ] `C-CF-55` `constraint` An `every two weeks` cycle annualises at half the weekly period count. `src: Core features rule 9`
- [ ] `C-CF-56` `literal` A `monthly` cycle annualises at `12` periods a year. `src: Core features rule 9`
- [ ] `C-CF-57` `literal` A `quarterly` cycle annualises at `4` periods a year. `src: Core features rule 9`
- [ ] `C-CF-58` `literal` A `half-yearly` cycle annualises at `2` periods a year. `src: Core features rule 9`
- [ ] `C-CF-59` `literal` A `yearly` cycle annualises at `1` period a year. `src: Core features rule 9`
- [ ] `C-CF-60` `literal` An `every N days` cycle annualises at `365.2425` divided by the day count. `src: Core features rule 9`
- [ ] `C-CF-61` `constraint` Rounding happens half-to-even. `src: Core features rule 9`
- [ ] `C-CF-62` `constraint` Rounding happens at the final step before a figure is shown. `src: Core features rule 9`
- [ ] `C-CF-63` `capability` The annual figure is the only accumulated aggregate. `src: Core features rule 10`
- [ ] `C-CF-64` `capability` The monthly figure is the annual figure divided by twelve. `src: Core features rule 10`
- [ ] `C-CF-65` `capability` The daily figure is the annual figure divided by three hundred sixty five. `src: Core features rule 10`
- [ ] `C-CF-66` `constraint` The unrounded daily value multiplied by three hundred sixty five reconstructs the annual value exactly. `src: Core features rule 10`
- [ ] `C-CF-67` `constraint` The unrounded monthly value multiplied by twelve reconstructs the annual value exactly. `src: Core features rule 10`
- [ ] `C-CF-68` `constraint` A per-day figure computed from a rounded monthly figure is refused as the wrong answer. `src: Core features rule 10`
- [ ] `C-CF-69` `constraint` Category subtotals sum exactly to the displayed total at every period. `src: Core features rule 11`
- [ ] `C-CF-70` `constraint` Donut segments sum exactly to the displayed total at every period. `src: Core features rule 11`
- [ ] `C-CF-71` `constraint` The app distributes rounding across categories by largest remainder. `src: Core features rule 11`
- [ ] `C-CF-72` `constraint` The app never distributes rounding across categories by truncation. `src: Core features rule 11`
- [ ] `C-CF-73` `data` Each subscription keeps the entry currency of that subscription. `src: Core features rule 12`
- [ ] `C-CF-74` `data` The account carries one home currency. `src: Core features rule 12`
- [ ] `C-CF-75` `data` The app ships a dated daily-rate table at least a year deep. `src: Core features rule 12`
- [ ] `C-CF-76` `constraint` A historical figure converts at the rate effective on the charge date. `src: Core features rule 12`
- [ ] `C-CF-77` `constraint` A projection converts at the latest rate. `src: Core features rule 12`
- [ ] `C-CF-78` `ui` A surface showing a converted figure names the rate date used. `src: Core features rule 12`
- [ ] `C-CF-79` `constraint` Conversion rounds half-to-even at the last step only. `src: Core features rule 13`
- [ ] `C-CF-80` `literal` A `jpy` price never grows a decimal anywhere. `src: Core features rule 13`
- [ ] `C-CF-81` `capability` Changing the home currency reconverts every figure on screen. `src: Core features rule 14`
- [ ] `C-CF-82` `constraint` Changing the home currency changes no stored value. `src: Core features rule 14`
- [ ] `C-CF-83` `constraint` The overview, the widget routes, the insight charts, the exported file agree to the minor unit. `src: Core features rule 15`
- [ ] `C-CF-84` `constraint` A cached per-surface total is refused as the wrong fix. `src: Core features rule 15`
- [ ] `C-CF-85` `capability` A monthly-family cycle anchors to the first-bill day of the month. `src: Core features rule 16`
- [ ] `C-CF-86` `constraint` A charge anchored on the 31st falls on the 28th in February of a common year. `src: Core features rule 16`
- [ ] `C-CF-87` `constraint` A charge anchored on the 31st falls on the 29th in February of a leap year. `src: Core features rule 16`
- [ ] `C-CF-88` `constraint` A charge anchored on the 31st returns to the 31st in March. `src: Core features rule 16`
- [ ] `C-CF-89` `literal` A yearly anchor of `2024-02-29` charges on `2025-02-28`. `src: Core features rule 16`
- [ ] `C-CF-90` `literal` A yearly anchor of `2024-02-29` charges on `2028-02-29`. `src: Core features rule 16`
- [ ] `C-CF-91` `constraint` A weekly-family cycle is exact interval arithmetic from the anchor. `src: Core features rule 17`
- [ ] `C-CF-92` `constraint` An `every N days` cycle never clamps. `src: Core features rule 17`
- [ ] `C-CF-93` `capability` Pausing suspends the charge sequence. `src: Core features rule 18`
- [ ] `C-CF-94` `capability` Resuming re-anchors the charge sequence forward from the resume date. `src: Core features rule 18`
- [ ] `C-CF-95` `constraint` Resuming never back-charges the paused span. `src: Core features rule 18`
- [ ] `C-CF-96` `constraint` A trial end date is the first paid charge boundary. `src: Core features rule 18`
- [ ] `C-CF-97` `constraint` The charge on the trial end date carries the post-trial price. `src: Core features rule 18`
- [ ] `C-CF-98` `capability` The default reminder falls the day before each charge. `src: Core features rule 19`
- [ ] `C-CF-99` `data` The owner sets the local time of the default reminder. `src: Core features rule 19`
- [ ] `C-CF-100` `literal` A per-subscription override allows `same_day`. `src: Core features rule 19`
- [ ] `C-CF-101` `literal` A per-subscription override allows `three_days_before`. `src: Core features rule 19`
- [ ] `C-CF-102` `constraint` A charge sequence resolves as civil local dates in the owner's zone. `src: Core features rule 19`
- [ ] `C-CF-103` `constraint` A reminder fires at the same wall clock on both sides of a daylight-saving change. `src: Core features rule 19`
- [ ] `C-CF-104` `constraint` A reminder instant in coordinated universal time moves by an hour across a daylight-saving change. `src: Core features rule 19`
- [ ] `C-CF-105` `constraint` A reminder reaches the timeline exactly once per charge occurrence. `src: Core features rule 20`
- [ ] `C-CF-106` `constraint` A second reminder pass for the same moment writes no second timeline entry. `src: Core features rule 20`
- [ ] `C-CF-107` `capability` A second reminder pass for the same moment reports nothing fired. `src: Core features rule 20`
- [ ] `C-CF-108` `constraint` Two reminder passes started together never both write. `src: Core features rule 20`
- [ ] `C-CF-109` `constraint` The losing reminder pass receives a conflict response. `src: Core features rule 20`
- [ ] `C-CF-110` `literal` A pass running more than twenty four hours after the scheduled instant records the occurrence as `missed`. `src: Core features rule 21`
- [ ] `C-CF-111` `ui` The timeline states a missed occurrence in words. `src: Core features rule 21`
- [ ] `C-CF-112` `constraint` A missed reminder is never re-announced as arriving on time. `src: Core features rule 21`
- [ ] `C-CF-113` `capability` The import sheet accepts pasted text. `src: Core features rule 22`
- [ ] `C-CF-114` `capability` The import sheet accepts a dropped text file. `src: Core features rule 22`
- [ ] `C-CF-115` `literal` The line `Lumen Play - Monthly - Renews Jan 15, 2027 - $10.99` reads as `1099` in `usd`. `src: Core features rule 22`
- [ ] `C-CF-116` `literal` The line `Papercut Stationery - Every 90 days - Renews 17/02/2026 - GBP 18.00` reads as `1800` in `gbp`. `src: Core features rule 22`
- [ ] `C-CF-117` `literal` The line `Cellar & Vine - Monatlich - Verlaengert am 05.12.2026 - 24,90 EUR` reads as `2490` in `eur`. `src: Core features rule 22`
- [ ] `C-CF-118` `literal` The line `Grid & Ember Energy - Annuel - Renouvellement le 01/12/2026 - 1 317,00 EUR` reads as `131700` in `eur`. `src: Core features rule 22`
- [ ] `C-CF-119` `literal` A row read with doubt returns `confidence` of `low`. `src: Core features rule 23`
- [ ] `C-CF-120` `constraint` A row read with doubt leaves the unread fields empty. `src: Core features rule 23`
- [ ] `C-CF-121` `constraint` The parser never guesses a value the parser did not read. `src: Core features rule 23`
- [ ] `C-CF-122` `constraint` The parser never crashes on arbitrary pasted text. `src: Core features rule 23`
- [ ] `C-CF-123` `constraint` The parser returns an empty row list for text holding no listing. `src: Core features rule 23`
- [ ] `C-CF-124` `ui` Parsed rows land in a preview table carrying per-row confidence. `src: Core features rule 24`
- [ ] `C-CF-125` `ui` Every preview cell is editable before the confirm. `src: Core features rule 24`
- [ ] `C-CF-126` `capability` A parsed row matches an existing subscription when the folded names match. `src: Core features rule 24`
- [ ] `C-CF-127` `capability` A parsed row matches an existing subscription when the annualised costs fall within five percent. `src: Core features rule 24`
- [ ] `C-CF-128` `literal` A duplicate row offers `Merge` or `Skip`. `src: Core features rule 24`
- [ ] `C-CF-129` `constraint` A duplicate row defaults to neither answer. `src: Core features rule 24`
- [ ] `C-CF-130` `constraint` Confirming an import writes every accepted row as one action. `src: Core features rule 25`
- [ ] `C-CF-131` `constraint` One undo reverses a whole import batch. `src: Core features rule 25`
- [ ] `C-CF-132` `literal` The export header reads `name,price_minor,currency,cycle,cycle_days,anchor_date,category,icon,colour,kind,status,cancelled_on,trial_ends_on,trial_price_minor,notes`. `src: Core features rule 26`
- [ ] `C-CF-133` `constraint` Importing an exported file into an empty store reproduces every field to the minor unit. `src: Core features rule 26`
- [ ] `C-CF-134` `capability` The app offers five sample receipts from a tray. `src: Core features rule 27`
- [ ] `C-CF-135` `ui` Dropping a sample receipt runs a staged extraction. `src: Core features rule 27`
- [ ] `C-CF-136` `ui` The result card files each line item into a category. `src: Core features rule 27`
- [ ] `C-CF-137` `literal` `receipt-01` extracts `Kettle Club` on `2026-08-02` at `1200` in `usd`. `src: Core features rule 27`
- [ ] `C-CF-138` `literal` `receipt-02` extracts `Harvest Box` on `2026-08-05` at `1799` in `usd`. `src: Core features rule 27`
- [ ] `C-CF-139` `literal` `receipt-03` extracts `Cafe Meridien` on `2026-08-09` at `5500` in `aed`. `src: Core features rule 27`
- [ ] `C-CF-140` `literal` `receipt-04` extracts `Thread & Last` on `2026-07-28` at `6500` in `gbp`. `src: Core features rule 27`
- [ ] `C-CF-141` `literal` `receipt-05` extracts `Northwind Fibre` on `2026-08-01` at `5500` in `usd`. `src: Core features rule 27`
- [ ] `C-CF-142` `literal` `receipt-05` files `Fibre 300` at `4500` under `Utilities`. `src: Core features rule 27`
- [ ] `C-CF-143` `literal` `receipt-05` files `Router rental` at `1000` under `Utilities`. `src: Core features rule 27`
- [ ] `C-CF-144` `ui` Any other uploaded image returns an unreadable state rather than a value. `src: Core features rule 28`
- [ ] `C-CF-145` `ui` An unreadable upload opens the manual entry form. `src: Core features rule 28`
- [ ] `C-CF-146` `constraint` An unreadable upload never returns a guessed value. `src: Core features rule 28`
- [ ] `C-CF-147` `constraint` The uploaded bytes are absent from the store after a scan. `src: Core features rule 29`
- [ ] `C-CF-148` `constraint` The uploaded bytes are absent from the app's own filesystem after a scan. `src: Core features rule 29`
- [ ] `C-CF-149` `constraint` The uploaded bytes are absent from every response after a scan. `src: Core features rule 29`
- [ ] `C-CF-150` `data` A scan persists a content hash of the uploaded bytes. `src: Core features rule 29`
- [ ] `C-CF-151` `capability` Uploading the same bytes twice offers the earlier scan. `src: Core features rule 29`
- [ ] `C-CF-152` `constraint` Uploading the same bytes twice files no second scan. `src: Core features rule 29`
- [ ] `C-CF-153` `data` Scan history carries a retention setting in days. `src: Core features rule 30`
- [ ] `C-CF-154` `constraint` A scan older than the retention window is gone from the next read. `src: Core features rule 30`
- [ ] `C-CF-155` `constraint` The scan surface sits behind the entitlement. `src: Core features rule 30`
- [ ] `C-CF-156` `capability` The app serves a small home-screen widget as a standalone route. `src: Core features rule 31`
- [ ] `C-CF-157` `capability` The app serves a medium home-screen widget as a standalone route. `src: Core features rule 31`
- [ ] `C-CF-158` `capability` The app serves a lock-screen strip as a standalone route. `src: Core features rule 31`
- [ ] `C-CF-159` `capability` The app serves a watch face as a standalone route. `src: Core features rule 31`
- [ ] `C-CF-160` `constraint` A change in the main app appears on every widget route within sixty seconds. `src: Core features rule 32`
- [ ] `C-CF-161` `literal` The watch face complication takes the shape `Streamio Premium · Aug 11 · 2D · 84 AED`. `src: Core features rule 33`
- [ ] `C-CF-162` `literal` A free account holds up to `6` subscriptions. `src: Core features rule 34`
- [ ] `C-CF-163` `ui` The seventh subscription opens the paywall sheet. `src: Core features rule 34`
- [ ] `C-CF-164` `ui` The paywall sheet reuses the pricing band's cards. `src: Core features rule 34`
- [ ] `C-CF-165` `constraint` A direct request for a seventh subscription without an entitlement is refused by the store. `src: Core features rule 35`
- [ ] `C-CF-166` `constraint` An import batch carrying the count past six is refused without an entitlement. `src: Core features rule 35`
- [ ] `C-CF-167` `constraint` An undo restoring a seventh subscription is refused without an entitlement. `src: Core features rule 35`
- [ ] `C-CF-168` `ui` The refusal names the cap. `src: Core features rule 35`
- [ ] `C-CF-169` `literal` The premium plan stores `799` minor units a month. `src: Core features rule 36`
- [ ] `C-CF-170` `literal` The premium plan stores `2972` minor units a year. `src: Core features rule 36`
- [ ] `C-CF-171` `literal` Twelve monthly premium payments total `9588` minor units. `src: Core features rule 36`
- [ ] `C-CF-172` `literal` The yearly saving displays as `-69%`. `src: Core features rule 36`
- [ ] `C-CF-173` `constraint` The yearly saving is computed from the stored pair rather than written twice. `src: Core features rule 36`
- [ ] `C-CF-174` `constraint` An expired entitlement deletes nothing. `src: Core features rule 37`
- [ ] `C-CF-175` `constraint` A subscription beyond the sixth becomes read-only after expiry. `src: Core features rule 37`
- [ ] `C-CF-176` `constraint` A custom category survives an entitlement lapse intact. `src: Core features rule 37`
- [ ] `C-CF-177` `constraint` Scan history survives an entitlement lapse intact. `src: Core features rule 37`
- [ ] `C-CF-178` `ui` The year heatmap gives one cell per day. `src: Core features rule 38`
- [ ] `C-CF-179` `ui` Heatmap cell intensity follows the amount charged that day. `src: Core features rule 38`
- [ ] `C-CF-180` `constraint` The heatmap computes from the charge sequences rather than from the subscriptions directly. `src: Core features rule 38`
- [ ] `C-CF-181` `ui` Hovering a heatmap cell names the charges on that day. `src: Core features rule 38`
- [ ] `C-CF-182` `ui` The heatmap offers the same information as text without hovering. `src: Core features rule 38`
- [ ] `C-CF-183` `ui` The twelve-month trend stacks monthly bars by category. `src: Core features rule 39`
- [ ] `C-CF-184` `ui` The current month splits visibly into the charged part, the scheduled part. `src: Core features rule 39`
- [ ] `C-CF-185` `ui` Price history lists every change entry with the effective date. `src: Core features rule 40`
- [ ] `C-CF-186` `constraint` A month before an increase computes at the price effective then. `src: Core features rule 40`
- [ ] `C-CF-187` `constraint` A month before an increase never computes at today's price. `src: Core features rule 40`
- [ ] `C-CF-188` `capability` The trials watch lists trials ending within thirty days, soonest first. `src: Core features rule 41`
- [ ] `C-CF-189` `ui` The trials watch calls out the post-trial price. `src: Core features rule 41`
- [ ] `C-CF-190` `capability` The savings counter totals avoided cost from each cancellation's effective date. `src: Core features rule 41`
- [ ] `C-CF-191` `constraint` Every mutation flows through one command stack. `src: Core features rule 42`
- [ ] `C-CF-192` `literal` The command stack holds at least `50` steps. `src: Core features rule 42`
- [ ] `C-CF-193` `constraint` A batch collapses to one step on the command stack. `src: Core features rule 42`
- [ ] `C-CF-194` `constraint` Undo replays through the engines rather than patching screens. `src: Core features rule 42`
- [ ] `C-CF-195` `literal` A destructive act raises a toast carrying an `Undo` action. `src: Core features rule 43`
- [ ] `C-CF-196` `literal` The undo toast stays for `8` seconds. `src: Core features rule 43`
- [ ] `C-CF-197` `ui` The editor sheet traps focus for as long as the sheet stays open. `src: Core features rule 43`
- [ ] `C-CF-198` `literal` Deleting is soft for `30` days. `src: Core features rule 44`
- [ ] `C-CF-199` `capability` The settings bin lists every soft-deleted record with a restore. `src: Core features rule 44`
- [ ] `C-CF-200` `constraint` A purge is a separate explicit act. `src: Core features rule 44`
- [ ] `C-CF-201` `constraint` Two tabs on one account converge within one second of a change. `src: Core features rule 45`
- [ ] `C-CF-202` `constraint` The second tab shows the new figure without a manual reload. `src: Core features rule 45`
- [ ] `C-CF-203` `capability` A snapshot export writes one versioned file holding the whole store. `src: Core features rule 46`
- [ ] `C-CF-204` `capability` A snapshot may be sealed with a passphrase. `src: Core features rule 46`
- [ ] `C-CF-205` `capability` Restoring a snapshot reproduces an equivalent store. `src: Core features rule 46`
- [ ] `C-CF-206` `constraint` A snapshot of a newer version is refused with a message naming the version. `src: Core features rule 46`
- [ ] `C-CF-207` `constraint` A refused snapshot changes nothing. `src: Core features rule 46`
- [ ] `C-CF-208` `literal` `Delete all data` empties the account in one confirmed step. `src: Core features rule 47`
- [ ] `C-CF-209` `capability` After erasure the account returns to the first-run state with a zero total. `src: Core features rule 47`
- [ ] `C-CF-210` `ui` A settings meter states the storage in use. `src: Core features rule 48`
- [ ] `C-CF-211` `ui` The storage meter warns as the limit approaches. `src: Core features rule 48`
- [ ] `C-CF-212` `constraint` A write exceeding the storage limit fails whole. `src: Core features rule 48`
- [ ] `C-CF-213` `constraint` A failed oversized write leaves no partial record behind. `src: Core features rule 48`
- [ ] `C-CF-214` `constraint` The landing page runs fourteen bands in the stated order. `src: Core features rule 49`
- [ ] `C-CF-215` `constraint` Every band's copy is fixed rather than improvised. `src: Core features rule 49`
- [ ] `C-CF-216` `ui` The blog index carries the pinned editorial title line above the cards. `src: Core features rule 50`
- [ ] `C-CF-217` `ui` The blog index carries five cards. `src: Core features rule 50`
- [ ] `C-CF-218` `capability` Each blog card opens an article reusing the legal reading column. `src: Core features rule 50`
- [ ] `C-CF-219` `capability` A privacy page is reachable from the footer of every page. `src: Core features rule 51`
- [ ] `C-CF-220` `constraint` The privacy page states what the app keeps about a person. `src: Core features rule 51`
- [ ] `C-CF-221` `constraint` The privacy page states plainly that an uploaded image is not kept. `src: Core features rule 51`
- [ ] `C-CF-222` `literal` The privacy page carries the dated line `Last updated: August 11, 2026`. `src: Core features rule 51`
- [ ] `C-CF-223` `capability` A terms page is reachable from the footer of every page. `src: Core features rule 52`
- [ ] `C-CF-224` `capability` The terms page is linked from the signup form. `src: Core features rule 52`
- [ ] `C-CF-225` `literal` The terms page carries the dated line `Last updated: July 8, 2026`. `src: Core features rule 52`
- [ ] `C-CF-226` `constraint` The terms page states that a free account tracks up to six subscriptions with full features. `src: Core features rule 52`
- [ ] `C-CF-227` `literal` An unmatched address renders the pill reading `Page not found`. `src: Core features rule 53`
- [ ] `C-CF-228` `ui` The not-found screen keeps the navigation above the pill. `src: Core features rule 53`
- [ ] `C-CF-229` `constraint` An unmatched address answers as not found rather than as a page that worked. `src: Core features rule 53`
- [ ] `C-CF-230` `data` The app keeps one route-view row per public route per day. `src: Core features rule 54`
- [ ] `C-CF-231` `constraint` A route-view row carries no identity. `src: Core features rule 54`
- [ ] `C-CF-232` `capability` A signed-in owner reads the route-view counts in settings. `src: Core features rule 54`

## C-UF User flow

- [ ] `C-UF-01` `contract` The route `/` serves the landing page. `src: User flow route table`
- [ ] `C-UF-02` `contract` The route `/blog` serves the article index. `src: User flow route table`
- [ ] `C-UF-03` `contract` The route `/blog/<slug>` serves one article. `src: User flow route table`
- [ ] `C-UF-04` `contract` The route `/privacy` serves the privacy policy. `src: User flow route table`
- [ ] `C-UF-05` `contract` The route `/terms` serves the terms of use. `src: User flow route table`
- [ ] `C-UF-06` `contract` The route `/sign-in` serves account entry. `src: User flow route table`
- [ ] `C-UF-07` `contract` The route `/sign-up` serves account creation. `src: User flow route table`
- [ ] `C-UF-08` `contract` The route `/demo` serves the read-only demo store. `src: User flow route table`
- [ ] `C-UF-09` `contract` The route `/app` serves the overview. `src: User flow route table`
- [ ] `C-UF-10` `contract` The route `/app/subscriptions/new/basics` serves editor step one. `src: User flow route table`
- [ ] `C-UF-11` `contract` The route `/app/subscriptions/new/cost` serves editor step two. `src: User flow route table`
- [ ] `C-UF-12` `contract` The route `/app/subscriptions/new/schedule` serves editor step three. `src: User flow route table`
- [ ] `C-UF-13` `contract` The route `/app/subscriptions/<id>` serves one subscription. `src: User flow route table`
- [ ] `C-UF-14` `contract` The route `/app/import` serves the import surface. `src: User flow route table`
- [ ] `C-UF-15` `contract` The route `/app/ai-spend` serves the receipt reader. `src: User flow route table`
- [ ] `C-UF-16` `contract` The route `/app/insights` serves the charts. `src: User flow route table`
- [ ] `C-UF-17` `contract` The route `/app/settings` serves the settings surface. `src: User flow route table`
- [ ] `C-UF-18` `contract` The route `/w/small` serves the small widget standalone. `src: User flow route table`
- [ ] `C-UF-19` `contract` The route `/w/medium` serves the medium widget standalone. `src: User flow route table`
- [ ] `C-UF-20` `contract` The route `/w/lock` serves the lock-screen strip standalone. `src: User flow route table`
- [ ] `C-UF-21` `contract` The route `/w/watch` serves the watch face standalone. `src: User flow route table`
- [ ] `C-UF-22` `constraint` Every `/app` route requires an owner session. `src: User flow route table`
- [ ] `C-UF-23` `constraint` Every `/w` route requires an owner session. `src: User flow route table`
- [ ] `C-UF-24` `capability` A signed-out request for an `/app` route lands on `/sign-in` carrying the intended path. `src: User flow, entry and redirects`
- [ ] `C-UF-25` `capability` Signing in returns to the intended path. `src: User flow, entry and redirects`
- [ ] `C-UF-26` `capability` A sign-in with no intended path lands on `/app`. `src: User flow, entry and redirects`
- [ ] `C-UF-27` `capability` Signing out returns to `/`. `src: User flow, entry and redirects`
- [ ] `C-UF-28` `constraint` An expired token refuses the action without changing anything. `src: User flow, entry and redirects`
- [ ] `C-UF-29` `capability` An expired token returns the person to `/sign-in`. `src: User flow, entry and redirects`
- [ ] `C-UF-30` `constraint` Another owner's subscription reads as not found. `src: User flow, entry and redirects`
- [ ] `C-UF-31` `capability` A seventh subscription without an entitlement returns to the paywall sheet. `src: User flow, entry and redirects`
- [ ] `C-UF-32` `capability` Following the hero ghost pill scrolls to the promo band. `src: User flow, journeys`
- [ ] `C-UF-33` `capability` Following `Get the app` reaches `/sign-in`. `src: User flow, journeys`
- [ ] `C-UF-34` `literal` Signing in as `user@example.com` shows `$211.80` a month. `src: User flow, journeys`
- [ ] `C-UF-35` `literal` Signing in as `user@example.com` shows `$2,541.55` a year. `src: User flow, journeys`
- [ ] `C-UF-36` `literal` Signing in as `user@example.com` shows `$6.96` a day. `src: User flow, journeys`
- [ ] `C-UF-37` `literal` The upcoming timeline for `user@example.com` carries `Harvest Box`. `src: User flow, journeys`
- [ ] `C-UF-38` `literal` The paywall reads `Free to start. Premium when you grow.` `src: User flow, journeys`
- [ ] `C-UF-39` `literal` The `Yearly` toggle position reprices the premium card to `$29.72`. `src: User flow, journeys`
- [ ] `C-UF-40` `literal` The insight history for `Northbridge Auto` reads `$175.00` before `2026-04-01`. `src: User flow, journeys`
- [ ] `C-UF-41` `literal` The insight history for `Northbridge Auto` reads `$185.00` from `2026-04-01`. `src: User flow, journeys`
- [ ] `C-UF-42` `literal` A first-run overview reads `Nothing is tracked yet`. `src: User flow, states`
- [ ] `C-UF-43` `ui` A first-run overview carries one control adding the first subscription. `src: User flow, states`
- [ ] `C-UF-44` `literal` An empty upcoming timeline reads `No charges scheduled`. `src: User flow, states`
- [ ] `C-UF-45` `ui` Every page carries a loading state reserving the space of the content. `src: User flow, states`
- [ ] `C-UF-46` `ui` Every error renders a message naming what happened. `src: User flow, states`
- [ ] `C-UF-47` `ui` Every error renders a message naming what to do. `src: User flow, states`
- [ ] `C-UF-48` `constraint` A list failing to load never blanks the totals above the list. `src: User flow, states`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The page ground is a near-white warm neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-02` `ui` Cards are a near-white neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-03` `ui` A card stays visibly separate from the ground without a dividing line. `src: UI/UX notes, palette`
- [ ] `C-UX-04` `ui` Ink is a near-black warm neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-05` `ui` Secondary text is a mid warm neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-06` `constraint` The mid warm neutral never carries a small label alone. `src: UI/UX notes, palette`
- [ ] `C-UX-07` `ui` Exactly one signal colour exists, a mid vivid red at the orange edge. `src: UI/UX notes, palette`
- [ ] `C-UX-08` `constraint` The signal colour appears only on a primary action, an alert, or a numbered step chip. `src: UI/UX notes, palette`
- [ ] `C-UX-09` `ui` A near-white muted blue carries the eyebrow labels. `src: UI/UX notes, palette`
- [ ] `C-UX-10` `ui` A mid soft blue carries the eyebrow ink. `src: UI/UX notes, palette`
- [ ] `C-UX-11` `ui` The footer inverts to a near-black neutral warming to a near-black warm neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-12` `ui` Footer links rest in a light cool neutral, brightening to white. `src: UI/UX notes, palette`
- [ ] `C-UX-13` `constraint` The orange ramp paints the hero device frame edge alone. `src: UI/UX notes, palette`
- [ ] `C-UX-14` `ui` Inter Tight carries display at the 600 to 800 grades. `src: UI/UX notes, type`
- [ ] `C-UX-15` `ui` Inter carries everything else at the 400 to 700 grades. `src: UI/UX notes, type`
- [ ] `C-UX-16` `literal` Both faces fall back to `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`. `src: UI/UX notes, type`
- [ ] `C-UX-17` `ui` Figures align down a column wherever amounts stack. `src: UI/UX notes, type`
- [ ] `C-UX-18` `ui` A generated film grain tile repeats over the whole public site. `src: UI/UX notes, grain`
- [ ] `C-UX-19` `constraint` The film grain is omitted inside `/app`. `src: UI/UX notes, grain`
- [ ] `C-UX-20` `ui` Motion carries an eased character across the whole product. `src: UI/UX notes, motion`
- [ ] `C-UX-21` `ui` A headline assembles word by word out of a soft blur. `src: UI/UX notes, motion`
- [ ] `C-UX-22` `constraint` A band reveal plays once. `src: UI/UX notes, motion`
- [ ] `C-UX-23` `ui` The hero device floats slowly, continuously. `src: UI/UX notes, motion`
- [ ] `C-UX-24` `ui` The reminder card gives one bell-shake wiggle on arrival. `src: UI/UX notes, motion`
- [ ] `C-UX-25` `ui` One passage pins the page for the length of four sentences. `src: UI/UX notes, motion`
- [ ] `C-UX-26` `ui` Each word of the pinned passage brightens from muted to ink as the scrub reaches the word. `src: UI/UX notes, motion`
- [ ] `C-UX-27` `constraint` Nothing uses a different speed to feel special. `src: UI/UX notes, motion`
- [ ] `C-UX-28` `constraint` A reduced-motion preference turns the scroll smoothing off. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-29` `constraint` A reduced-motion preference turns a reveal into a plain appearance. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-30` `constraint` A reduced-motion preference holds the float still. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-31` `constraint` A reduced-motion preference holds the bell-shake still. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-32` `constraint` A reduced-motion preference holds the word scrub still. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-33` `constraint` A reduced-motion preference stops the promo film autoplaying. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-34` `constraint` A reduced-motion preference removes nothing from the page. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-35` `ui` Density is spacious on the public half. `src: UI/UX notes, density`
- [ ] `C-UX-36` `ui` Density is comfortable inside `/app`. `src: UI/UX notes, density`
- [ ] `C-UX-37` `ui` The layout archetype is a floating top navigation pill. `src: UI/UX notes, layout`
- [ ] `C-UX-38` `constraint` The navigation pill keeps the geometry of the pill at every width. `src: UI/UX notes, layout`
- [ ] `C-UX-39` `ui` The link row folds behind a menu control on a narrow screen. `src: UI/UX notes, layout`
- [ ] `C-UX-40` `constraint` No sidebar appears anywhere in the product. `src: UI/UX notes, layout`
- [ ] `C-UX-41` `constraint` Each page leads with exactly one primary action. `src: UI/UX notes, single action`
- [ ] `C-UX-42` `ui` The primary action is visually distinct from every secondary one. `src: UI/UX notes, single action`
- [ ] `C-UX-43` `constraint` Nothing moves during the reading of a figure inside `/app`. `src: UI/UX notes, stance`
- [ ] `C-UX-44` `constraint` A total never animates the digits of the total. `src: UI/UX notes, stance`
- [ ] `C-UX-45` `constraint` Body text meets WCAG AA contrast against the background of the body text. `src: UI/UX notes, accessibility`
- [ ] `C-UX-46` `constraint` The inverted footer meets WCAG AA contrast. `src: UI/UX notes, accessibility`
- [ ] `C-UX-47` `constraint` The dark privacy band meets WCAG AA contrast. `src: UI/UX notes, accessibility`
- [ ] `C-UX-48` `literal` A touch target measures at least `44` pixels on the shorter side. `src: UI/UX notes, accessibility`
- [ ] `C-UX-49` `constraint` Keyboard navigation reaches every control in reading order. `src: UI/UX notes, accessibility`
- [ ] `C-UX-50` `ui` A visible focus ring never depends on the signal colour alone. `src: UI/UX notes, accessibility`
- [ ] `C-UX-51` `constraint` Colour never carries meaning alone. `src: UI/UX notes, accessibility`
- [ ] `C-UX-52` `ui` Every chart pairs a hue with a label, a value. `src: UI/UX notes, accessibility`
- [ ] `C-UX-53` `ui` An unavailable control says why in words. `src: UI/UX notes, accessibility`
- [ ] `C-UX-54` `constraint` A word-split headline stays one accessible string. `src: UI/UX notes, accessibility`
- [ ] `C-UX-55` `constraint` The pinned passage reads as one paragraph to assistive technology. `src: UI/UX notes, accessibility`
- [ ] `C-UX-56` `ui` Every content image carries alternative text. `src: UI/UX notes, accessibility`
- [ ] `C-UX-57` `ui` Every decorative image declares the image decorative. `src: UI/UX notes, accessibility`
- [ ] `C-UX-58` `constraint` The landing page becomes one column at a narrow viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-59` `ui` The hero device moves below the copy at a narrow viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-60` `ui` The plan cards stack at a narrow viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-61` `constraint` The pinned passage keeps working at a narrow viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-62` `ui` The totals stack above the donut at phone width. `src: UI/UX notes, responsive`
- [ ] `C-UX-63` `ui` Category rows run full width at phone width. `src: UI/UX notes, responsive`
- [ ] `C-UX-64` `ui` The editor sheet becomes full height at phone width. `src: UI/UX notes, responsive`
- [ ] `C-UX-65` `constraint` Nothing overflows sideways at any viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-66` `constraint` Every navigation target stays reachable at any viewport. `src: UI/UX notes, responsive`
- [ ] `C-UX-67` `constraint` No page is dominated by one hue family with no second signal. `src: UI/UX notes, failure modes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is SvelteKit. `src: Technical requirements, stack`
- [ ] `C-TR-02` `constraint` Every route is server-rendered so the browser receives complete markup on first paint. `src: Technical requirements, stack`
- [ ] `C-TR-03` `contract` The backend is Fastify. `src: Technical requirements, stack`
- [ ] `C-TR-04` `contract` The HTTP API is served under the `/api` prefix on the same origin. `src: Technical requirements, stack`
- [ ] `C-TR-05` `contract` The datastore is PostgreSQL. `src: Technical requirements, stack`
- [ ] `C-TR-06` `literal` The datastore is reached at `DATABASE_URL`. `src: Technical requirements, stack`
- [ ] `C-TR-07` `constraint` Every host is read from the environment rather than hardcoded. `src: Technical requirements, stack`
- [ ] `C-TR-08` `constraint` Every port is read from the environment rather than hardcoded. `src: Technical requirements, stack`
- [ ] `C-TR-09` `constraint` No second database is introduced. `src: Technical requirements, libraries`
- [ ] `C-TR-10` `constraint` No object store is introduced. `src: Technical requirements, libraries`
- [ ] `C-TR-11` `contract` Auth exchanges an email with a password for a bearer token. `src: Technical requirements, auth`
- [ ] `C-TR-12` `constraint` A password is stored with a modern password hash. `src: Technical requirements, auth`
- [ ] `C-TR-13` `constraint` A token expires. `src: Technical requirements, auth`
- [ ] `C-TR-14` `literal` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements, auth`
- [ ] `C-TR-15` `constraint` Every timestamp is stored in coordinated universal time. `src: Technical requirements, auth`
- [ ] `C-TR-16` `data` Every account carries a time zone. `src: Technical requirements, auth`
- [ ] `C-TR-17` `constraint` Every civil-date calculation resolves in the account's zone. `src: Technical requirements, auth`
- [ ] `C-TR-18` `constraint` The money engine is reachable by exactly one path. `src: Technical requirements, engines`
- [ ] `C-TR-19` `constraint` The date engine is reachable by exactly one path. `src: Technical requirements, engines`
- [ ] `C-TR-20` `constraint` Money is an integer count of minor units in every layer. `src: Technical requirements, engines`
- [ ] `C-TR-21` `constraint` A money value carries a currency code beside the money value. `src: Technical requirements, engines`
- [ ] `C-TR-22` `constraint` The demo store refuses every write. `src: Technical requirements, engines`
- [ ] `C-TR-23` `constraint` Two requests racing to write one reminder occurrence resolve to exactly one winner. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-24` `literal` The losing writer receives a `409` conflict response. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-25` `constraint` The conflict response names the occurrence already recorded. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-26` `constraint` Two simultaneous attempts at a seventh subscription resolve to exactly one winner. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-27` `constraint` Two snapshot restores started together resolve to exactly one taking effect. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-28` `constraint` A replayed reminder pass returns the same run summary as the first pass. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-29` `constraint` A replayed reminder pass creates no second timeline entry. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-30` `constraint` An import confirmed twice under one batch identifier creates no second set of rows. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-31` `literal` Every list endpoint accepts a `page_size` parameter. `src: Technical requirements, paginated reads`
- [ ] `C-TR-32` `literal` A list endpoint defaults `page_size` to `20`. `src: Technical requirements, paginated reads`
- [ ] `C-TR-33` `literal` A list endpoint caps `page_size` at `100`. `src: Technical requirements, paginated reads`
- [ ] `C-TR-34` `constraint` A page size above the cap is refused with the cap named in the message. `src: Technical requirements, paginated reads`
- [ ] `C-TR-35` `constraint` A page size above the cap is never served as a page quietly cut down. `src: Technical requirements, paginated reads`
- [ ] `C-TR-36` `literal` Every list response carries a `next_cursor` beside the `data` array. `src: Technical requirements, paginated reads`
- [ ] `C-TR-37` `literal` Every list response carries a `has_more` flag. `src: Technical requirements, paginated reads`
- [ ] `C-TR-38` `constraint` The cursor is a keyset cursor over a stable ordering key. `src: Technical requirements, paginated reads`
- [ ] `C-TR-39` `constraint` A list receiving new rows between two reads never repeats a row. `src: Technical requirements, paginated reads`
- [ ] `C-TR-40` `constraint` A list receiving new rows between two reads never skips a row. `src: Technical requirements, paginated reads`
- [ ] `C-TR-41` `literal` The app stays usable with `1000` subscriptions on one account. `src: Technical requirements, responsiveness`
- [ ] `C-TR-42` `constraint` An edit part way down a long list keeps the focus of the edit. `src: Technical requirements, responsiveness`
- [ ] `C-TR-43` `constraint` The totals header recomputes before the next frame the reader sees. `src: Technical requirements, responsiveness`
- [ ] `C-TR-44` `literal` A widget route returns a document under `50` kilobytes before the data of the route. `src: Technical requirements, responsiveness`
- [ ] `C-TR-45` `data` The store carries a recorded schema version. `src: Technical requirements, performance`
- [ ] `C-TR-46` `constraint` The app refuses to open a store whose recorded schema version is newer than the known version. `src: Technical requirements, performance`
- [ ] `C-TR-47` `constraint` A refused newer store changes nothing. `src: Technical requirements, performance`
- [ ] `C-TR-48` `constraint` Every public route carries a title unique across the routes. `src: Technical requirements, metadata`
- [ ] `C-TR-49` `constraint` Every public route carries a description unique across the routes. `src: Technical requirements, metadata`
- [ ] `C-TR-50` `constraint` Every public route declares a social preview title. `src: Technical requirements, metadata`
- [ ] `C-TR-51` `constraint` Every public route declares a social preview image. `src: Technical requirements, metadata`
- [ ] `C-TR-52` `constraint` A social preview image resolves to a real response from the app's own origin. `src: Technical requirements, metadata`
- [ ] `C-TR-53` `constraint` The app makes no outbound network call at run time. `src: Technical requirements, fixtures`
- [ ] `C-TR-54` `data` The app serves the service-name suggestion list from the app's own store. `src: Technical requirements, fixtures`
- [ ] `C-TR-55` `data` The app serves the daily-rate table from the app's own store. `src: Technical requirements, fixtures`
- [ ] `C-TR-56` `data` The app serves the five sample receipts from the app's own store. `src: Technical requirements, fixtures`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-02` `literal` The seeded password is written into `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` The `owner` table carries an `email` unique, compared case-insensitively. `src: Data model, owner`
- [ ] `C-DM-04` `data` The `subscription` table carries a non-negative integer `price_minor`. `src: Data model, subscription`
- [ ] `C-DM-05` `data` The `subscription` table carries a required `anchor_date`. `src: Data model, subscription`
- [ ] `C-DM-06` `data` The `subscription` table carries a `cycle_days` required only for `every_n_days`. `src: Data model, subscription`
- [ ] `C-DM-07` `constraint` A `one_time` subscription carries the single date of the expense in `anchor_date`. `src: Data model, subscription`
- [ ] `C-DM-08` `constraint` A `one_time` subscription carries no cycle behaviour. `src: Data model, subscription`
- [ ] `C-DM-09` `data` The `price_change` table carries a `mode` of `next_renewal` or `correct_history`. `src: Data model, price change`
- [ ] `C-DM-10` `constraint` A `price_change` row is never removed. `src: Data model, price change`
- [ ] `C-DM-11` `constraint` A builtin category is never deleted. `src: Data model, category`
- [ ] `C-DM-12` `constraint` A custom category exists only for an entitled account. `src: Data model, category`
- [ ] `C-DM-13` `constraint` Exactly one `reminder_rule` row per owner carries a null `subscription_id`. `src: Data model, reminder rule`
- [ ] `C-DM-14` `constraint` At most one `reminder_entry` exists for one subscription on one occurrence date. `src: Data model, reminder entry`
- [ ] `C-DM-15` `constraint` Two passes started together for one occurrence never both write a `reminder_entry`. `src: Data model, reminder entry`
- [ ] `C-DM-16` `data` A `reminder_entry` carries a `state` of `fired` or `missed`. `src: Data model, reminder entry`
- [ ] `C-DM-17` `data` A `scan` row carries a `content_hash` unique per owner. `src: Data model, scan`
- [ ] `C-DM-18` `constraint` No column of the `scan` table holds the bytes of the uploaded image. `src: Data model, scan`
- [ ] `C-DM-19` `constraint` No file on the app's own disk holds the bytes of the uploaded image. `src: Data model, scan`
- [ ] `C-DM-20` `constraint` At most one `entitlement` row exists per owner. `src: Data model, entitlement`
- [ ] `C-DM-21` `constraint` The store consults the entitlement before writing a seventh subscription. `src: Data model, entitlement`
- [ ] `C-DM-22` `constraint` The store consults the entitlement before writing a custom category. `src: Data model, entitlement`
- [ ] `C-DM-23` `constraint` The store consults the entitlement before writing a scan. `src: Data model, entitlement`
- [ ] `C-DM-24` `constraint` Rows sharing a `batch_id` undo together as one step. `src: Data model, command`
- [ ] `C-DM-25` `constraint` Rows sharing a `batch_id` redo together as one step. `src: Data model, command`
- [ ] `C-DM-26` `constraint` A `bin_entry` older than thirty days is gone from every read. `src: Data model, bin entry`
- [ ] `C-DM-27` `data` The `rate` table is a bundled read-only fixture unique per currency pair on a date. `src: Data model, rate`
- [ ] `C-DM-28` `data` A `route_view` row is unique per route on a date. `src: Data model, route view`
- [ ] `C-DM-29` `constraint` A `route_view` row carries no identity of any kind. `src: Data model, route view`
- [ ] `C-DM-30` `constraint` The next charge date is derived rather than stored. `src: Data model, derived`
- [ ] `C-DM-31` `literal` The home currency of both seeded accounts is `usd`. `src: Data model, currencies`
- [ ] `C-DM-32` `literal` The rate table is dated `2026-09-15` at the head of the table. `src: Data model, currencies`
- [ ] `C-DM-33` `literal` The rate for `eur` is `1.0850`. `src: Data model, currencies`
- [ ] `C-DM-34` `literal` The rate for `gbp` is `1.2640`. `src: Data model, currencies`
- [ ] `C-DM-35` `literal` The rate for `aed` is `0.2723`. `src: Data model, currencies`
- [ ] `C-DM-36` `literal` The rate for `jpy` is `0.006740`. `src: Data model, currencies`
- [ ] `C-DM-37` `literal` The builtin categories are `Groceries`, `Loans`, `Cafes & Dining`, `Shopping`, `Health & Fitness`, `Entertainment`, `Utilities`. `src: Data model, categories`
- [ ] `C-DM-38` `literal` The account `user@example.com` is seeded as Nadia Ferreira in zone `UTC`. `src: Data model, seed data`
- [ ] `C-DM-39` `literal` The account `user2@example.com` is seeded as Owen Mbeki in zone `America/New_York`. `src: Data model, seed data`
- [ ] `C-DM-40` `literal` The account `user2@example.com` carries an `active` entitlement on the `monthly` plan. `src: Data model, seed data`
- [ ] `C-DM-41` `literal` The demo store carries `30` active recurring subscriptions. `src: Data model, seed data`
- [ ] `C-DM-42` `constraint` The demo store spans five currencies. `src: Data model, seed data`
- [ ] `C-DM-43` `constraint` The demo store spans every cycle. `src: Data model, seed data`
- [ ] `C-DM-44` `literal` The demo overview reads `126219` minor units a month. `src: Data model, seed data`
- [ ] `C-DM-45` `literal` The demo overview reads `1514633` minor units a year. `src: Data model, seed data`
- [ ] `C-DM-46` `literal` The demo overview reads `4150` minor units a day. `src: Data model, seed data`
- [ ] `C-DM-47` `literal` The demo category `Groceries` reads `36800` a month, `441600` a year. `src: Data model, seed data`
- [ ] `C-DM-48` `literal` The demo category `Loans` reads `32000` a month, `384000` a year. `src: Data model, seed data`
- [ ] `C-DM-49` `literal` The demo category `Cafes & Dining` reads `16700` a month, `200400` a year. `src: Data model, seed data`
- [ ] `C-DM-50` `literal` The demo category `Shopping` reads `12000` a month, `144000` a year. `src: Data model, seed data`
- [ ] `C-DM-51` `literal` The demo category `Health & Fitness` reads `11019` a month, `132233` a year. `src: Data model, seed data`
- [ ] `C-DM-52` `literal` The demo category `Entertainment` reads `8900` a month, `106800` a year. `src: Data model, seed data`
- [ ] `C-DM-53` `literal` The demo category `Utilities` reads `8800` a month, `105600` a year. `src: Data model, seed data`
- [ ] `C-DM-54` `literal` The demo category `Groceries` shows a per-year approximation of about `4,420 $`. `src: Data model, seed data`
- [ ] `C-DM-55` `literal` The account `user@example.com` holds exactly `6` active subscriptions. `src: Data model, seed data`
- [ ] `C-DM-56` `literal` The account `user@example.com` reads `21180` minor units a month. `src: Data model, seed data`
- [ ] `C-DM-57` `literal` The account `user@example.com` reads `254155` minor units a year. `src: Data model, seed data`
- [ ] `C-DM-58` `literal` The account `user@example.com` reads `696` minor units a day. `src: Data model, seed data`
- [ ] `C-DM-59` `literal` The account `user2@example.com` holds nine active subscriptions. `src: Data model, seed data`
- [ ] `C-DM-60` `literal` The account `user2@example.com` reads `31159` minor units a month. `src: Data model, seed data`
- [ ] `C-DM-61` `literal` The account `user2@example.com` reads `373910` minor units a year. `src: Data model, seed data`
- [ ] `C-DM-62` `literal` The account `user2@example.com` reads `1024` minor units a day. `src: Data model, seed data`
- [ ] `C-DM-63` `literal` A price change on `Northbridge Auto` moves `17500` to `18500` effective `2026-04-01`. `src: Data model, seed data`
- [ ] `C-DM-64` `literal` The seeded trial `Foldspace Studio` ends `2026-09-28` at a post-trial price of `1499`. `src: Data model, seed data`
- [ ] `C-DM-65` `literal` The seeded cancellation `Kinoteca` takes effect `2026-06-30`. `src: Data model, seed data`
- [ ] `C-DM-66` `literal` The seeded one-time expense `Winter Tyres` is `24000` dated `2026-08-14`. `src: Data model, seed data`
- [ ] `C-DM-67` `literal` The account `user2@example.com` carries one custom category `Studio`. `src: Data model, seed data`
- [ ] `C-DM-68` `constraint` Seeding is idempotent so a restart duplicates no row. `src: Data model, seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` Display type is set in `Inter Tight`. `src: Front-end specification, type`
- [ ] `C-FE-02` `literal` Body type is set in `Inter`. `src: Front-end specification, type`
- [ ] `C-FE-03` `constraint` No third family appears anywhere. `src: Front-end specification, type`
- [ ] `C-FE-04` `constraint` No serif appears anywhere. `src: Front-end specification, type`
- [ ] `C-FE-05` `ui` Figures use tabular figures rather than a monospace face. `src: Front-end specification, type`
- [ ] `C-FE-06` `literal` The hero display on a wide desktop is `103.68px` set at the 800 grade. `src: Front-end specification, scale`
- [ ] `C-FE-07` `literal` The hero display at the capture width is `93.6px` set at the 800 grade. `src: Front-end specification, scale`
- [ ] `C-FE-08` `literal` The manifesto words are `64.35px` set at the 800 grade. `src: Front-end specification, scale`
- [ ] `C-FE-09` `literal` Band headlines run `58px` to `60px` set at the 600 grade. `src: Front-end specification, scale`
- [ ] `C-FE-10` `literal` The footer call to action is `50px` set at the 800 grade. `src: Front-end specification, scale`
- [ ] `C-FE-11` `literal` Card titles are `28px` set at the 600 grade. `src: Front-end specification, scale`
- [ ] `C-FE-12` `literal` Plan prices are `24px` set at the 700 grade. `src: Front-end specification, scale`
- [ ] `C-FE-13` `literal` Question rows are `19px` set at the 700 grade. `src: Front-end specification, scale`
- [ ] `C-FE-14` `literal` Lede paragraphs are `17px` set at the 400 grade. `src: Front-end specification, scale`
- [ ] `C-FE-15` `literal` Body copy is `16px` set at the 400 grade. `src: Front-end specification, scale`
- [ ] `C-FE-16` `literal` Eyebrows are `12px` set at the 700 grade, uppercase, letterspaced. `src: Front-end specification, scale`
- [ ] `C-FE-17` `ui` The hero's second sentence is set italic. `src: Front-end specification, scale`
- [ ] `C-FE-18` `literal` The breakdown band's third line `Per day.` is set italic. `src: Front-end specification, scale`
- [ ] `C-FE-19` `ui` The content column has one fixed maximum width. `src: Front-end specification, ground`
- [ ] `C-FE-20` `ui` The layout changes at six measured steps as the window narrows. `src: Front-end specification, ground`
- [ ] `C-FE-21` `ui` The film grain is one generated fractal-noise tile drawn once, repeated. `src: Front-end specification, ground`
- [ ] `C-FE-22` `ui` Navigation, buttons, toggles carry a full pill corner. `src: Front-end specification, shape`
- [ ] `C-FE-23` `ui` The footer's top corners are the most generous shape on the page. `src: Front-end specification, shape`
- [ ] `C-FE-24` `constraint` The signal-coloured glow belongs to the primary action, the closing CTA, the pricing knob alone. `src: Front-end specification, shadow`
- [ ] `C-FE-25` `ui` The navigation pill carries a translucent white tint deepening on scroll. `src: Front-end specification, glass`
- [ ] `C-FE-26` `ui` The navigation pill blurs whatever passes beneath the pill. `src: Front-end specification, glass`
- [ ] `C-FE-27` `ui` The app icon is a drawn rounded square in the signal colour carrying a white letterform. `src: Front-end specification, mark`
- [ ] `C-FE-28` `constraint` No binary asset ships with the build. `src: Front-end specification, assets`
- [ ] `C-FE-29` `ui` The hero device is drawn with an ink body. `src: Front-end specification, assets`
- [ ] `C-FE-30` `constraint` The hero device screen renders the live overview component rather than a film. `src: Front-end specification, assets`
- [ ] `C-FE-31` `ui` Editorial figures are seeded procedural layered radial gradients. `src: Front-end specification, assets`
- [ ] `C-FE-32` `ui` The code card is a decorative non-scannable finder pattern. `src: Front-end specification, assets`
- [ ] `C-FE-33` `constraint` The code card is labelled decorative. `src: Front-end specification, assets`
- [ ] `C-FE-34` `ui` First paint is a loader holding the wordmark alone on paper cream. `src: Front-end specification, chrome`
- [ ] `C-FE-35` `constraint` The loader fades out once the fonts, the hero are ready. `src: Front-end specification, chrome`
- [ ] `C-FE-36` `constraint` The loader never returns on a later navigation inside the site. `src: Front-end specification, chrome`
- [ ] `C-FE-37` `ui` A circular frosted back-to-top button sits at the bottom right. `src: Front-end specification, chrome`
- [ ] `C-FE-38` `constraint` The back-to-top button stays hidden until the first band has passed. `src: Front-end specification, chrome`
- [ ] `C-FE-39` `ui` The promo figure carries a circular sound toggle swapping two speaker glyphs. `src: Front-end specification, chrome`
- [ ] `C-FE-40` `literal` The footer carries the call to action `Download Driplog to get Started`. `src: Front-end specification, footer`
- [ ] `C-FE-41` `literal` The footer carries the fine line `iPhone · iOS 17+ · Free to start`. `src: Front-end specification, footer`
- [ ] `C-FE-42` `literal` The footer carries a `Join beta` link. `src: Front-end specification, footer`
- [ ] `C-FE-43` `literal` The footer row reads `Driplog`, `Help Center`, `Contact us`, `Privacy Policy`, `Terms of Use`. `src: Front-end specification, footer`
- [ ] `C-FE-44` `literal` The footer carries the line `(C) 2026 Driplog. All rights reserved.` `src: Front-end specification, footer`
- [ ] `C-FE-45` `constraint` `Help Center` is plain text rather than a link. `src: Front-end specification, footer`
- [ ] `C-FE-46` `literal` `Contact us` reaches `hello@driplog.app`. `src: Front-end specification, footer`
- [ ] `C-FE-47` `literal` The beta sheet carries the display copy `Be the first one`, `to be onboard`. `src: Front-end specification, beta sheet`
- [ ] `C-FE-48` `literal` The beta sheet carries the pill `Join Beta`. `src: Front-end specification, beta sheet`
- [ ] `C-FE-49` `constraint` The beta sheet closes on the cross, on the backdrop, on Escape. `src: Front-end specification, beta sheet`
- [ ] `C-FE-50` `constraint` The beta sheet traps focus for as long as the sheet stays open. `src: Front-end specification, beta sheet`
- [ ] `C-FE-51` `literal` The hero headline opens `All your subscriptions.` `src: Front-end specification, band 1`
- [ ] `C-FE-52` `ui` The hero lede is the pinned sentence naming the honest total, the quiet nudge. `src: Front-end specification, band 1`
- [ ] `C-FE-53` `literal` The hero carries the pill `Download on the App Store`. `src: Front-end specification, band 1`
- [ ] `C-FE-54` `ui` The hero carries a ghost pill beside the store pill. `src: Front-end specification, band 1`
- [ ] `C-FE-55` `constraint` The hero headline assembles word by word on load rather than on scroll. `src: Front-end specification, band 1`
- [ ] `C-FE-56` `literal` Band two carries the eyebrow `Overview`. `src: Front-end specification, band 2`
- [ ] `C-FE-57` `literal` Band two carries the headline `See how much you really spend.` `src: Front-end specification, band 2`
- [ ] `C-FE-58` `literal` Band two carries the tick `Live monthly & yearly totals`. `src: Front-end specification, band 2`
- [ ] `C-FE-59` `literal` Band two carries the tick `A countdown to every charge`. `src: Front-end specification, band 2`
- [ ] `C-FE-60` `literal` Band two carries the tick `Any currency, converted at daily rates`. `src: Front-end specification, band 2`
- [ ] `C-FE-61` `literal` Band three carries the eyebrow `Breakdown`. `src: Front-end specification, band 3`
- [ ] `C-FE-62` `literal` Band three carries the headline `Per year. Per month. Per day.` `src: Front-end specification, band 3`
- [ ] `C-FE-63` `literal` Band four carries the eyebrow `Reminders`. `src: Front-end specification, band 4`
- [ ] `C-FE-64` `literal` Band four carries the headline `Never get surprise-charged again.` `src: Front-end specification, band 4`
- [ ] `C-FE-65` `literal` Band four's push card reads `Subscription Reminder: Tomorrow is your Fitness App renewal`. `src: Front-end specification, band 4`
- [ ] `C-FE-66` `literal` Band five carries the eyebrow `Setup · One screenshot`. `src: Front-end specification, band 5`
- [ ] `C-FE-67` `literal` Band five carries the headline `Import what Apple already charges you for.` `src: Front-end specification, band 5`
- [ ] `C-FE-68` `literal` Band five carries the numbered chip `Open Subscriptions`. `src: Front-end specification, band 5`
- [ ] `C-FE-69` `literal` Band five carries the numbered chip `Take a screenshot`. `src: Front-end specification, band 5`
- [ ] `C-FE-70` `ui` Band five carries a third numbered chip instructing the drop. `src: Front-end specification, band 5`
- [ ] `C-FE-71` `literal` The import surface carries the copy `Import your Apple subscriptions`. `src: Front-end specification, band 5`
- [ ] `C-FE-72` `literal` The import surface carries the control `Open App Store`. `src: Front-end specification, band 5`
- [ ] `C-FE-73` `literal` The import surface carries the control `Upload screenshots`. `src: Front-end specification, band 5`
- [ ] `C-FE-74` `literal` The import surface carries the control `Add manually`. `src: Front-end specification, band 5`
- [ ] `C-FE-75` `literal` Band six carries the eyebrow `Premium · AI Spend`. `src: Front-end specification, band 6`
- [ ] `C-FE-76` `literal` Band six carries the headline `Snap a receipt. Let AI do the math.` `src: Front-end specification, band 6`
- [ ] `C-FE-77` `literal` Band seven carries the eyebrow `Premium · Widgets`. `src: Front-end specification, band 7`
- [ ] `C-FE-78` `literal` Band seven carries the headline `Your next payment, right on the Home Screen.` `src: Front-end specification, band 7`
- [ ] `C-FE-79` `literal` Band eight carries the eyebrow `Apple Watch`. `src: Front-end specification, band 8`
- [ ] `C-FE-80` `literal` Band eight carries the headline `The next charge, on your wrist.` `src: Front-end specification, band 8`
- [ ] `C-FE-81` `literal` Band nine carries the manifesto passage opening `You know roughly what you pay every month.` `src: Front-end specification, band 9`
- [ ] `C-FE-82` `literal` The manifesto closes `Driplog turns that quiet leak into one honest number you can act on.` `src: Front-end specification, band 9`
- [ ] `C-FE-83` `literal` Band ten carries the headline `Private by Design.` `src: Front-end specification, band 10`
- [ ] `C-FE-84` `literal` Band ten carries the badge `Private sync`. `src: Front-end specification, band 10`
- [ ] `C-FE-85` `literal` Band ten carries the badge `No ads in the app`. `src: Front-end specification, band 10`
- [ ] `C-FE-86` `literal` Band ten carries the badge `No data sold`. `src: Front-end specification, band 10`
- [ ] `C-FE-87` `literal` Band ten carries the badge `Anonymous stats only`. `src: Front-end specification, band 10`
- [ ] `C-FE-88` `literal` Band eleven carries the eyebrow `Pricing`. `src: Front-end specification, band 11`
- [ ] `C-FE-89` `literal` Band eleven carries the headline `Free to start. Premium when you grow.` `src: Front-end specification, band 11`
- [ ] `C-FE-90` `literal` The pricing toggle offers `Monthly`, `Yearly`. `src: Front-end specification, band 11`
- [ ] `C-FE-91` `literal` The free card reads `Free`, `$0`, `Enough to see the whole picture.` `src: Front-end specification, band 11`
- [ ] `C-FE-92` `literal` The free card carries the tick `Up to 6 subscriptions`. `src: Front-end specification, band 11`
- [ ] `C-FE-93` `literal` The free card carries the tick `Per day / month / year breakdowns`. `src: Front-end specification, band 11`
- [ ] `C-FE-94` `literal` The free card carries the tick `Renewal reminders`. `src: Front-end specification, band 11`
- [ ] `C-FE-95` `literal` The free card carries the tick `Custom icons & colours`. `src: Front-end specification, band 11`
- [ ] `C-FE-96` `literal` The free card carries the tick `Private sync & privacy`. `src: Front-end specification, band 11`
- [ ] `C-FE-97` `literal` The free card carries the button `Start free`. `src: Front-end specification, band 11`
- [ ] `C-FE-98` `literal` The premium card carries the flag `Most popular`. `src: Front-end specification, band 11`
- [ ] `C-FE-99` `literal` The premium card reads `$7.99 /mo` over `Billed monthly. Cancel anytime.` `src: Front-end specification, band 11`
- [ ] `C-FE-100` `literal` The premium card carries the tick `Unlimited subscriptions`. `src: Front-end specification, band 11`
- [ ] `C-FE-101` `literal` The premium card carries the tick `AI Spend: scan receipts & statements`. `src: Front-end specification, band 11`
- [ ] `C-FE-102` `ui` The premium card carries a tick naming widgets for the home screen, the lock screen. `src: Front-end specification, band 11`
- [ ] `C-FE-103` `literal` The premium card carries the tick `Personal calculation categories`. `src: Front-end specification, band 11`
- [ ] `C-FE-104` `literal` The premium card carries the tick `Everything in Free`. `src: Front-end specification, band 11`
- [ ] `C-FE-105` `literal` The premium card carries the tick `Support an app with zero ads`. `src: Front-end specification, band 11`
- [ ] `C-FE-106` `literal` The premium card carries the button `Go Premium`. `src: Front-end specification, band 11`
- [ ] `C-FE-107` `literal` Band twelve carries the eyebrow `FAQ`. `src: Front-end specification, band 12`
- [ ] `C-FE-108` `literal` Band twelve carries the headline `Good questions.` `src: Front-end specification, band 12`
- [ ] `C-FE-109` `ui` Band twelve carries six hairline-divided disclosure rows. `src: Front-end specification, band 12`
- [ ] `C-FE-110` `literal` A question reads `Do I have to connect my bank?` `src: Front-end specification, band 12`
- [ ] `C-FE-111` `literal` A question reads `Where is my data stored?` `src: Front-end specification, band 12`
- [ ] `C-FE-112` `literal` A question reads `Do you track me?` `src: Front-end specification, band 12`
- [ ] `C-FE-113` `literal` A question reads `What do I get for free?` `src: Front-end specification, band 12`
- [ ] `C-FE-114` `literal` A question reads `How does AI Spend handle my receipts?` `src: Front-end specification, band 12`
- [ ] `C-FE-115` `literal` A question reads `Can I cancel Premium anytime?` `src: Front-end specification, band 12`
- [ ] `C-FE-116` `literal` Band thirteen carries the handle `@driplog`. `src: Front-end specification, band 13`
- [ ] `C-FE-117` `ui` Band fourteen scales the promo figure up as the figure enters. `src: Front-end specification, band 14`
- [ ] `C-FE-118` `literal` The blog card `Too Lazy to Type In Every Expense? Let AI Read Your Receipts` appears on the index. `src: Front-end specification, blog`
- [ ] `C-FE-119` `literal` The blog card `How Much Do Your Subscriptions Really Cost Per Year?` appears on the index. `src: Front-end specification, blog`
- [ ] `C-FE-120` `ui` The blog index carries a card about cancelling a forgotten free trial. `src: Front-end specification, blog`
- [ ] `C-FE-121` `literal` The blog card `The Best Way to Track Subscriptions on iPhone in 2026` appears on the index. `src: Front-end specification, blog`
- [ ] `C-FE-122` `literal` The blog card `Subscription Creep: Why Your Money Quietly Disappears Every Month` appears on the index. `src: Front-end specification, blog`
- [ ] `C-FE-123` `ui` The legal shell is a narrow reading column on the paper ground. `src: Front-end specification, legal`
- [ ] `C-FE-124` `ui` The legal shell carries the title with a dated meta line. `src: Front-end specification, legal`
- [ ] `C-FE-125` `constraint` The five articles reuse the legal shell. `src: Front-end specification, legal`
- [ ] `C-FE-126` `ui` The not-found pill is white at a full round with the deep card shadow. `src: Front-end specification, not found`
- [ ] `C-FE-127` `constraint` The app surfaces use the same tokens at working density. `src: Front-end specification, app surfaces`
- [ ] `C-FE-128` `constraint` One overview component serves the app home, the hero screen, the widget miniatures. `src: Front-end specification, app surfaces`
- [ ] `C-FE-129` `ui` A floating signal-coloured plus opens the editor sheet. `src: Front-end specification, app surfaces`
- [ ] `C-FE-130` `constraint` The demo mode overview is read-only, carrying a visible mark. `src: Front-end specification, app surfaces`
- [ ] `C-FE-131` `constraint` One toast primitive serves the whole product. `src: Front-end specification, app surfaces`
- [ ] `C-FE-132` `constraint` One sheet primitive serves the whole product. `src: Front-end specification, app surfaces`
- [ ] `C-FE-133` `constraint` One confirm primitive serves the whole product. `src: Front-end specification, app surfaces`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One person owns one list. `src: Constraints`
- [ ] `C-CN-02` `constraint` One home currency applies at a time. `src: Constraints`
- [ ] `C-CN-03` `constraint` No bank connection exists. `src: Constraints`
- [ ] `C-CN-04` `constraint` The entitlement purchase is simulated inside the app. `src: Constraints`
- [ ] `C-CN-05` `constraint` No email is sent. `src: Constraints`
- [ ] `C-CN-06` `constraint` The in-app reminders timeline is the only delivery channel. `src: Constraints`
- [ ] `C-CN-07` `constraint` No file upload exists beyond the receipt image. `src: Constraints`
- [ ] `C-CN-08` `constraint` No third-party analytics vendor is used. `src: Constraints`
- [ ] `C-CN-09` `constraint` No native application ships. `src: Constraints`
- [ ] `C-CN-10` `constraint` The widget surfaces are browser routes. `src: Constraints`
- [ ] `C-CN-11` `constraint` No machine-learned model runs. `src: Constraints`
- [ ] `C-CN-12` `constraint` The receipt reader is a staged fixture saying so. `src: Constraints`
- [ ] `C-CN-13` `literal` The app stays responsive with `200` price changes on one account. `src: Constraints`
- [ ] `C-CN-14` `literal` The app stays responsive with `5000` reminder entries on one account. `src: Constraints`
- [ ] `C-CN-15` `literal` The app stays responsive with `2000` command rows on one account. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract`
- [ ] `C-DC-03` `literal` The outward port comes from `APP_PUBLIC_PORT`. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-05` `literal` `GET /api/health` returns `200` once ready. `src: Deployment contract`
- [ ] `C-DC-06` `constraint` The app starts from the environment image with no manual step. `src: Deployment contract`
- [ ] `C-DC-07` `literal` Credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-08` `literal` A reserved `.browser_screenshots/` directory exists at the app root. `src: Deployment contract`
- [ ] `C-DC-09` `literal` A reserved `.downloads/` directory exists at the app root. `src: Deployment contract`
- [ ] `C-DC-10` `constraint` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` No dev server is served. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` The server is not a child of the shell. `src: Deployment contract`
- [ ] `C-DC-14` `literal` The server binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-15` `constraint` The server never binds a loopback-only address. `src: Deployment contract`
- [ ] `C-DC-16` `constraint` No backing service is downloaded, installed, compiled, or started by the app. `src: Deployment contract`
- [ ] `C-DC-17` `constraint` No persistent volume is declared. `src: Deployment contract`
- [ ] `C-DC-18` `contract` `POST /api/auth/signup` takes an email, a password, a name. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `contract` `POST /api/auth/login` returns an access token. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `contract` `GET /api/demo/overview` returns the demo totals. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `contract` `GET /api/content/pricing` returns the plan pair with the saving percent. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `contract` `GET /api/app/overview` returns the totals, the categories, the upcoming list. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `contract` `GET /api/app/subscriptions` returns a paginated list. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `contract` `POST /api/app/subscriptions` creates one subscription. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `contract` `PATCH /api/app/subscriptions/{id}` takes a price change mode. `src: Deployment contract, API shapes`
- [ ] `C-DC-26` `contract` `POST /api/app/subscriptions/{id}/cancel` takes an effective date. `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `contract` `GET /api/app/subscriptions/{id}/charges` returns the charge dates in a window. `src: Deployment contract, API shapes`
- [ ] `C-DC-28` `contract` `GET /api/app/insights/heatmap` returns one entry per charged day. `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `contract` `GET /api/app/insights/price-history` returns the change entries. `src: Deployment contract, API shapes`
- [ ] `C-DC-30` `contract` `GET /api/app/insights/savings` returns the avoided cost total. `src: Deployment contract, API shapes`
- [ ] `C-DC-31` `contract` `POST /api/app/import/parse` returns parsed rows with a confidence. `src: Deployment contract, API shapes`
- [ ] `C-DC-32` `contract` `POST /api/app/import/commit` writes the accepted rows under one batch. `src: Deployment contract, API shapes`
- [ ] `C-DC-33` `contract` `GET /api/app/export.csv` returns the pinned header with one line per record. `src: Deployment contract, API shapes`
- [ ] `C-DC-34` `contract` `POST /api/app/scans` returns the extraction with a content hash. `src: Deployment contract, API shapes`
- [ ] `C-DC-35` `contract` `GET /api/app/entitlement` returns the plan with the state. `src: Deployment contract, API shapes`
- [ ] `C-DC-36` `contract` `GET /api/app/reminders/schedule` returns the occurrences in a window. `src: Deployment contract, API shapes`
- [ ] `C-DC-37` `contract` `POST /api/app/reminders/run` takes an `as_of` instant. `src: Deployment contract, API shapes`
- [ ] `C-DC-38` `contract` `GET /api/app/reminders/timeline` returns the written entries. `src: Deployment contract, API shapes`
- [ ] `C-DC-39` `contract` `POST /api/app/undo` reverts the newest command. `src: Deployment contract, API shapes`
- [ ] `C-DC-40` `contract` `GET /api/app/stats/views` returns one row per route on a date. `src: Deployment contract, API shapes`
- [ ] `C-DC-41` `contract` `POST /api/app/data/delete-all` empties the account. `src: Deployment contract, API shapes`
- [ ] `C-DC-42` `constraint` An invalid call is rejected as a client error. `src: Deployment contract, API shapes`
- [ ] `C-DC-43` `constraint` An invalid call never returns a silent success. `src: Deployment contract, API shapes`
- [ ] `C-DC-44` `data` A rejection carries a stable machine-readable `code`. `src: Deployment contract, API shapes`
- [ ] `C-DC-45` `data` A rejection carries a human `message`. `src: Deployment contract, API shapes`
- [ ] `C-DC-46` `constraint` The subscriptions live in PostgreSQL rather than in an in-memory array. `src: Deployment contract, no mocks`
- [ ] `C-DC-47` `constraint` The reminder entries live in PostgreSQL rather than in a module variable. `src: Deployment contract, no mocks`
- [ ] `C-DC-48` `constraint` The commands live in PostgreSQL rather than in a file on the app's own disk. `src: Deployment contract, no mocks`
- [ ] `C-DC-49` `constraint` An image is never kept on the container filesystem after a scan. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `user@example.com` | pinned value the product carries | C-RL-23 | User roles, signup paragraph |
| `user2@example.com` | pinned value the product carries | C-RL-24 | User roles, signup paragraph |
| `Your spending` | pinned value the product carries | C-CF-19 | Core features rule 1 |
| `Calculator` | pinned value the product carries | C-CF-21 | Core features rule 1 |
| `AI Spend` | pinned value the product carries | C-CF-21 | Core features rule 1 |
| `All` | pinned value the product carries | C-CF-22 | Core features rule 1 |
| `Recurring` | pinned value the product carries | C-CF-22 | Core features rule 1 |
| `One-time` | pinned value the product carries | C-CF-22 | Core features rule 1 |
| `Where your money goes` | pinned value the product carries | C-CF-23 | Core features rule 2 |
| `Apply from next renewal` | pinned value the product carries | C-CF-36 | Core features rule 5 |
| `Correct history` | pinned value the product carries | C-CF-36 | Core features rule 5 |
| `weekly` | pinned value the product carries | C-CF-54 | Core features rule 9 |
| `52.1775` | pinned value the product carries | C-CF-54 | Core features rule 9 |
| `monthly` | pinned value the product carries | C-CF-56 | Core features rule 9 |
| `12` | pinned value the product carries | C-CF-56 | Core features rule 9 |
| `quarterly` | pinned value the product carries | C-CF-57 | Core features rule 9 |
| `4` | pinned value the product carries | C-CF-57 | Core features rule 9 |
| `half-yearly` | pinned value the product carries | C-CF-58 | Core features rule 9 |
| `2` | pinned value the product carries | C-CF-58 | Core features rule 9 |
| `yearly` | pinned value the product carries | C-CF-59 | Core features rule 9 |
| `1` | pinned value the product carries | C-CF-59 | Core features rule 9 |
| `every N days` | pinned value the product carries | C-CF-60 | Core features rule 9 |
| `365.2425` | pinned value the product carries | C-CF-60 | Core features rule 9 |
| `jpy` | pinned value the product carries | C-CF-80 | Core features rule 13 |
| `2024-02-29` | pinned value the product carries | C-CF-89 | Core features rule 16 |
| `2025-02-28` | pinned value the product carries | C-CF-89 | Core features rule 16 |
| `2028-02-29` | pinned value the product carries | C-CF-90 | Core features rule 16 |
| `same_day` | pinned value the product carries | C-CF-100 | Core features rule 19 |
| `three_days_before` | pinned value the product carries | C-CF-101 | Core features rule 19 |
| `missed` | pinned value the product carries | C-CF-110 | Core features rule 21 |
| `Lumen Play - Monthly - Renews Jan 15, 2027 - $10.99` | pinned value the product carries | C-CF-115 | Core features rule 22 |
| `1099` | pinned value the product carries | C-CF-115 | Core features rule 22 |
| `usd` | pinned value the product carries | C-CF-115 | Core features rule 22 |
| `Papercut Stationery - Every 90 days - Renews 17/02/2026 - GBP 18.00` | pinned value the product carries | C-CF-116 | Core features rule 22 |
| `1800` | pinned value the product carries | C-CF-116 | Core features rule 22 |
| `gbp` | pinned value the product carries | C-CF-116 | Core features rule 22 |
| `Cellar & Vine - Monatlich - Verlaengert am 05.12.2026 - 24,90 EUR` | pinned value the product carries | C-CF-117 | Core features rule 22 |
| `2490` | pinned value the product carries | C-CF-117 | Core features rule 22 |
| `eur` | pinned value the product carries | C-CF-117 | Core features rule 22 |
| `Grid & Ember Energy - Annuel - Renouvellement le 01/12/2026 - 1 317,00 EUR` | pinned value the product carries | C-CF-118 | Core features rule 22 |
| `131700` | pinned value the product carries | C-CF-118 | Core features rule 22 |
| `confidence` | pinned value the product carries | C-CF-119 | Core features rule 23 |
| `low` | pinned value the product carries | C-CF-119 | Core features rule 23 |
| `Merge` | pinned value the product carries | C-CF-128 | Core features rule 24 |
| `Skip` | pinned value the product carries | C-CF-128 | Core features rule 24 |
| `name,price_minor,currency,cycle,cycle_days,anchor_date,category,icon,colour,kind,status,cancelled_on,trial_ends_on,trial_price_minor,notes` | pinned value the product carries | C-CF-132 | Core features rule 26 |
| `receipt-01` | pinned value the product carries | C-CF-137 | Core features rule 27 |
| `Kettle Club` | pinned value the product carries | C-CF-137 | Core features rule 27 |
| `2026-08-02` | pinned value the product carries | C-CF-137 | Core features rule 27 |
| `1200` | pinned value the product carries | C-CF-137 | Core features rule 27 |
| `receipt-02` | pinned value the product carries | C-CF-138 | Core features rule 27 |
| `Harvest Box` | pinned value the product carries | C-CF-138 | Core features rule 27 |
| `2026-08-05` | pinned value the product carries | C-CF-138 | Core features rule 27 |
| `1799` | pinned value the product carries | C-CF-138 | Core features rule 27 |
| `receipt-03` | pinned value the product carries | C-CF-139 | Core features rule 27 |
| `Cafe Meridien` | pinned value the product carries | C-CF-139 | Core features rule 27 |
| `2026-08-09` | pinned value the product carries | C-CF-139 | Core features rule 27 |
| `5500` | pinned value the product carries | C-CF-139 | Core features rule 27 |
| `aed` | pinned value the product carries | C-CF-139 | Core features rule 27 |
| `receipt-04` | pinned value the product carries | C-CF-140 | Core features rule 27 |
| `Thread & Last` | pinned value the product carries | C-CF-140 | Core features rule 27 |
| `2026-07-28` | pinned value the product carries | C-CF-140 | Core features rule 27 |
| `6500` | pinned value the product carries | C-CF-140 | Core features rule 27 |
| `receipt-05` | pinned value the product carries | C-CF-141 | Core features rule 27 |
| `Northwind Fibre` | pinned value the product carries | C-CF-141 | Core features rule 27 |
| `2026-08-01` | pinned value the product carries | C-CF-141 | Core features rule 27 |
| `Fibre 300` | pinned value the product carries | C-CF-142 | Core features rule 27 |
| `4500` | pinned value the product carries | C-CF-142 | Core features rule 27 |
| `Utilities` | pinned value the product carries | C-CF-142 | Core features rule 27 |
| `Router rental` | pinned value the product carries | C-CF-143 | Core features rule 27 |
| `1000` | pinned value the product carries | C-CF-143 | Core features rule 27 |
| `Streamio Premium · Aug 11 · 2D · 84 AED` | pinned value the product carries | C-CF-161 | Core features rule 33 |
| `6` | pinned value the product carries | C-CF-162 | Core features rule 34 |
| `799` | pinned value the product carries | C-CF-169 | Core features rule 36 |
| `2972` | pinned value the product carries | C-CF-170 | Core features rule 36 |
| `9588` | pinned value the product carries | C-CF-171 | Core features rule 36 |
| `-69%` | pinned value the product carries | C-CF-172 | Core features rule 36 |
| `50` | pinned value the product carries | C-CF-192 | Core features rule 42 |
| `Undo` | pinned value the product carries | C-CF-195 | Core features rule 43 |
| `8` | pinned value the product carries | C-CF-196 | Core features rule 43 |
| `30` | pinned value the product carries | C-CF-198 | Core features rule 44 |
| `Delete all data` | pinned value the product carries | C-CF-208 | Core features rule 47 |
| `Last updated: August 11, 2026` | pinned value the product carries | C-CF-222 | Core features rule 51 |
| `Last updated: July 8, 2026` | pinned value the product carries | C-CF-225 | Core features rule 52 |
| `Page not found` | pinned value the product carries | C-CF-227 | Core features rule 53 |
| `$211.80` | pinned value the product carries | C-UF-34 | User flow, journeys |
| `$2,541.55` | pinned value the product carries | C-UF-35 | User flow, journeys |
| `$6.96` | pinned value the product carries | C-UF-36 | User flow, journeys |
| `Free to start. Premium when you grow.` | pinned value the product carries | C-UF-38 | User flow, journeys |
| `Yearly` | pinned value the product carries | C-UF-39 | User flow, journeys |
| `$29.72` | pinned value the product carries | C-UF-39 | User flow, journeys |
| `Northbridge Auto` | pinned value the product carries | C-UF-40 | User flow, journeys |
| `$175.00` | pinned value the product carries | C-UF-40 | User flow, journeys |
| `2026-04-01` | pinned value the product carries | C-UF-40 | User flow, journeys |
| `$185.00` | pinned value the product carries | C-UF-41 | User flow, journeys |
| `Nothing is tracked yet` | pinned value the product carries | C-UF-42 | User flow, states |
| `No charges scheduled` | pinned value the product carries | C-UF-44 | User flow, states |
| `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` | pinned value the product carries | C-UX-16 | UI/UX notes, type |
| `44` | pinned value the product carries | C-UX-48 | UI/UX notes, accessibility |
| `DATABASE_URL` | pinned value the product carries | C-TR-06 | Technical requirements, stack |
| `GET /api/health` | pinned value the product carries | C-TR-14 | Technical requirements, auth |
| `200` | pinned value the product carries | C-TR-14 | Technical requirements, auth |
| `409` | pinned value the product carries | C-TR-24 | Technical requirements, simultaneous requests |
| `page_size` | pinned value the product carries | C-TR-31 | Technical requirements, paginated reads |
| `20` | pinned value the product carries | C-TR-32 | Technical requirements, paginated reads |
| `100` | pinned value the product carries | C-TR-33 | Technical requirements, paginated reads |
| `next_cursor` | pinned value the product carries | C-TR-36 | Technical requirements, paginated reads |
| `data` | pinned value the product carries | C-TR-36 | Technical requirements, paginated reads |
| `has_more` | pinned value the product carries | C-TR-37 | Technical requirements, paginated reads |
| `deku-demo-pw-2026` | pinned value the product carries | C-DM-01 | Data model, password paragraph |
| `/app/USER_README.md` | pinned value the product carries | C-DM-02 | Data model, password paragraph |
| `2026-09-15` | pinned value the product carries | C-DM-32 | Data model, currencies |
| `1.0850` | pinned value the product carries | C-DM-33 | Data model, currencies |
| `1.2640` | pinned value the product carries | C-DM-34 | Data model, currencies |
| `0.2723` | pinned value the product carries | C-DM-35 | Data model, currencies |
| `0.006740` | pinned value the product carries | C-DM-36 | Data model, currencies |
| `Groceries` | pinned value the product carries | C-DM-37 | Data model, categories |
| `Loans` | pinned value the product carries | C-DM-37 | Data model, categories |
| `Cafes & Dining` | pinned value the product carries | C-DM-37 | Data model, categories |
| `Shopping` | pinned value the product carries | C-DM-37 | Data model, categories |
| `Health & Fitness` | pinned value the product carries | C-DM-37 | Data model, categories |
| `Entertainment` | pinned value the product carries | C-DM-37 | Data model, categories |
| `UTC` | pinned value the product carries | C-DM-38 | Data model, seed data |
| `America/New_York` | pinned value the product carries | C-DM-39 | Data model, seed data |
| `active` | pinned value the product carries | C-DM-40 | Data model, seed data |
| `126219` | pinned value the product carries | C-DM-44 | Data model, seed data |
| `1514633` | pinned value the product carries | C-DM-45 | Data model, seed data |
| `4150` | pinned value the product carries | C-DM-46 | Data model, seed data |
| `36800` | pinned value the product carries | C-DM-47 | Data model, seed data |
| `441600` | pinned value the product carries | C-DM-47 | Data model, seed data |
| `32000` | pinned value the product carries | C-DM-48 | Data model, seed data |
| `384000` | pinned value the product carries | C-DM-48 | Data model, seed data |
| `16700` | pinned value the product carries | C-DM-49 | Data model, seed data |
| `200400` | pinned value the product carries | C-DM-49 | Data model, seed data |
| `12000` | pinned value the product carries | C-DM-50 | Data model, seed data |
| `144000` | pinned value the product carries | C-DM-50 | Data model, seed data |
| `11019` | pinned value the product carries | C-DM-51 | Data model, seed data |
| `132233` | pinned value the product carries | C-DM-51 | Data model, seed data |
| `8900` | pinned value the product carries | C-DM-52 | Data model, seed data |
| `106800` | pinned value the product carries | C-DM-52 | Data model, seed data |
| `8800` | pinned value the product carries | C-DM-53 | Data model, seed data |
| `105600` | pinned value the product carries | C-DM-53 | Data model, seed data |
| `4,420 $` | pinned value the product carries | C-DM-54 | Data model, seed data |
| `21180` | pinned value the product carries | C-DM-56 | Data model, seed data |
| `254155` | pinned value the product carries | C-DM-57 | Data model, seed data |
| `696` | pinned value the product carries | C-DM-58 | Data model, seed data |
| `31159` | pinned value the product carries | C-DM-60 | Data model, seed data |
| `373910` | pinned value the product carries | C-DM-61 | Data model, seed data |
| `1024` | pinned value the product carries | C-DM-62 | Data model, seed data |
| `17500` | pinned value the product carries | C-DM-63 | Data model, seed data |
| `18500` | pinned value the product carries | C-DM-63 | Data model, seed data |
| `Foldspace Studio` | pinned value the product carries | C-DM-64 | Data model, seed data |
| `2026-09-28` | pinned value the product carries | C-DM-64 | Data model, seed data |
| `1499` | pinned value the product carries | C-DM-64 | Data model, seed data |
| `Kinoteca` | pinned value the product carries | C-DM-65 | Data model, seed data |
| `2026-06-30` | pinned value the product carries | C-DM-65 | Data model, seed data |
| `Winter Tyres` | pinned value the product carries | C-DM-66 | Data model, seed data |
| `24000` | pinned value the product carries | C-DM-66 | Data model, seed data |
| `2026-08-14` | pinned value the product carries | C-DM-66 | Data model, seed data |
| `Studio` | pinned value the product carries | C-DM-67 | Data model, seed data |
| `Inter Tight` | pinned value the product carries | C-FE-01 | Front-end specification, type |
| `Inter` | pinned value the product carries | C-FE-02 | Front-end specification, type |
| `103.68px` | pinned value the product carries | C-FE-06 | Front-end specification, scale |
| `93.6px` | pinned value the product carries | C-FE-07 | Front-end specification, scale |
| `64.35px` | pinned value the product carries | C-FE-08 | Front-end specification, scale |
| `58px` | pinned value the product carries | C-FE-09 | Front-end specification, scale |
| `60px` | pinned value the product carries | C-FE-09 | Front-end specification, scale |
| `50px` | pinned value the product carries | C-FE-10 | Front-end specification, scale |
| `28px` | pinned value the product carries | C-FE-11 | Front-end specification, scale |
| `24px` | pinned value the product carries | C-FE-12 | Front-end specification, scale |
| `19px` | pinned value the product carries | C-FE-13 | Front-end specification, scale |
| `17px` | pinned value the product carries | C-FE-14 | Front-end specification, scale |
| `16px` | pinned value the product carries | C-FE-15 | Front-end specification, scale |
| `12px` | pinned value the product carries | C-FE-16 | Front-end specification, scale |
| `Per day.` | pinned value the product carries | C-FE-18 | Front-end specification, scale |
| `Download Driplog to get Started` | pinned value the product carries | C-FE-40 | Front-end specification, footer |
| `iPhone · iOS 17+ · Free to start` | pinned value the product carries | C-FE-41 | Front-end specification, footer |
| `Join beta` | pinned value the product carries | C-FE-42 | Front-end specification, footer |
| `Driplog` | pinned value the product carries | C-FE-43 | Front-end specification, footer |
| `Help Center` | pinned value the product carries | C-FE-43 | Front-end specification, footer |
| `Contact us` | pinned value the product carries | C-FE-43 | Front-end specification, footer |
| `Privacy Policy` | pinned value the product carries | C-FE-43 | Front-end specification, footer |
| `Terms of Use` | pinned value the product carries | C-FE-43 | Front-end specification, footer |
| `(C) 2026 Driplog. All rights reserved.` | pinned value the product carries | C-FE-44 | Front-end specification, footer |
| `hello@driplog.app` | pinned value the product carries | C-FE-46 | Front-end specification, footer |
| `Be the first one` | pinned value the product carries | C-FE-47 | Front-end specification, beta sheet |
| `to be onboard` | pinned value the product carries | C-FE-47 | Front-end specification, beta sheet |
| `Join Beta` | pinned value the product carries | C-FE-48 | Front-end specification, beta sheet |
| `All your subscriptions.` | pinned value the product carries | C-FE-51 | Front-end specification, band 1 |
| `Download on the App Store` | pinned value the product carries | C-FE-53 | Front-end specification, band 1 |
| `Overview` | pinned value the product carries | C-FE-56 | Front-end specification, band 2 |
| `See how much you really spend.` | pinned value the product carries | C-FE-57 | Front-end specification, band 2 |
| `Live monthly & yearly totals` | pinned value the product carries | C-FE-58 | Front-end specification, band 2 |
| `A countdown to every charge` | pinned value the product carries | C-FE-59 | Front-end specification, band 2 |
| `Any currency, converted at daily rates` | pinned value the product carries | C-FE-60 | Front-end specification, band 2 |
| `Breakdown` | pinned value the product carries | C-FE-61 | Front-end specification, band 3 |
| `Per year. Per month. Per day.` | pinned value the product carries | C-FE-62 | Front-end specification, band 3 |
| `Reminders` | pinned value the product carries | C-FE-63 | Front-end specification, band 4 |
| `Never get surprise-charged again.` | pinned value the product carries | C-FE-64 | Front-end specification, band 4 |
| `Subscription Reminder: Tomorrow is your Fitness App renewal` | pinned value the product carries | C-FE-65 | Front-end specification, band 4 |
| `Setup · One screenshot` | pinned value the product carries | C-FE-66 | Front-end specification, band 5 |
| `Import what Apple already charges you for.` | pinned value the product carries | C-FE-67 | Front-end specification, band 5 |
| `Open Subscriptions` | pinned value the product carries | C-FE-68 | Front-end specification, band 5 |
| `Take a screenshot` | pinned value the product carries | C-FE-69 | Front-end specification, band 5 |
| `Import your Apple subscriptions` | pinned value the product carries | C-FE-71 | Front-end specification, band 5 |
| `Open App Store` | pinned value the product carries | C-FE-72 | Front-end specification, band 5 |
| `Upload screenshots` | pinned value the product carries | C-FE-73 | Front-end specification, band 5 |
| `Add manually` | pinned value the product carries | C-FE-74 | Front-end specification, band 5 |
| `Premium · AI Spend` | pinned value the product carries | C-FE-75 | Front-end specification, band 6 |
| `Snap a receipt. Let AI do the math.` | pinned value the product carries | C-FE-76 | Front-end specification, band 6 |
| `Premium · Widgets` | pinned value the product carries | C-FE-77 | Front-end specification, band 7 |
| `Your next payment, right on the Home Screen.` | pinned value the product carries | C-FE-78 | Front-end specification, band 7 |
| `Apple Watch` | pinned value the product carries | C-FE-79 | Front-end specification, band 8 |
| `The next charge, on your wrist.` | pinned value the product carries | C-FE-80 | Front-end specification, band 8 |
| `You know roughly what you pay every month.` | pinned value the product carries | C-FE-81 | Front-end specification, band 9 |
| `Driplog turns that quiet leak into one honest number you can act on.` | pinned value the product carries | C-FE-82 | Front-end specification, band 9 |
| `Private by Design.` | pinned value the product carries | C-FE-83 | Front-end specification, band 10 |
| `Private sync` | pinned value the product carries | C-FE-84 | Front-end specification, band 10 |
| `No ads in the app` | pinned value the product carries | C-FE-85 | Front-end specification, band 10 |
| `No data sold` | pinned value the product carries | C-FE-86 | Front-end specification, band 10 |
| `Anonymous stats only` | pinned value the product carries | C-FE-87 | Front-end specification, band 10 |
| `Pricing` | pinned value the product carries | C-FE-88 | Front-end specification, band 11 |
| `Monthly` | pinned value the product carries | C-FE-90 | Front-end specification, band 11 |
| `Free` | pinned value the product carries | C-FE-91 | Front-end specification, band 11 |
| `$0` | pinned value the product carries | C-FE-91 | Front-end specification, band 11 |
| `Enough to see the whole picture.` | pinned value the product carries | C-FE-91 | Front-end specification, band 11 |
| `Up to 6 subscriptions` | pinned value the product carries | C-FE-92 | Front-end specification, band 11 |
| `Per day / month / year breakdowns` | pinned value the product carries | C-FE-93 | Front-end specification, band 11 |
| `Renewal reminders` | pinned value the product carries | C-FE-94 | Front-end specification, band 11 |
| `Custom icons & colours` | pinned value the product carries | C-FE-95 | Front-end specification, band 11 |
| `Private sync & privacy` | pinned value the product carries | C-FE-96 | Front-end specification, band 11 |
| `Start free` | pinned value the product carries | C-FE-97 | Front-end specification, band 11 |
| `Most popular` | pinned value the product carries | C-FE-98 | Front-end specification, band 11 |
| `$7.99 /mo` | pinned value the product carries | C-FE-99 | Front-end specification, band 11 |
| `Billed monthly. Cancel anytime.` | pinned value the product carries | C-FE-99 | Front-end specification, band 11 |
| `Unlimited subscriptions` | pinned value the product carries | C-FE-100 | Front-end specification, band 11 |
| `AI Spend: scan receipts & statements` | pinned value the product carries | C-FE-101 | Front-end specification, band 11 |
| `Personal calculation categories` | pinned value the product carries | C-FE-103 | Front-end specification, band 11 |
| `Everything in Free` | pinned value the product carries | C-FE-104 | Front-end specification, band 11 |
| `Support an app with zero ads` | pinned value the product carries | C-FE-105 | Front-end specification, band 11 |
| `Go Premium` | pinned value the product carries | C-FE-106 | Front-end specification, band 11 |
| `FAQ` | pinned value the product carries | C-FE-107 | Front-end specification, band 12 |
| `Good questions.` | pinned value the product carries | C-FE-108 | Front-end specification, band 12 |
| `Do I have to connect my bank?` | pinned value the product carries | C-FE-110 | Front-end specification, band 12 |
| `Where is my data stored?` | pinned value the product carries | C-FE-111 | Front-end specification, band 12 |
| `Do you track me?` | pinned value the product carries | C-FE-112 | Front-end specification, band 12 |
| `What do I get for free?` | pinned value the product carries | C-FE-113 | Front-end specification, band 12 |
| `How does AI Spend handle my receipts?` | pinned value the product carries | C-FE-114 | Front-end specification, band 12 |
| `Can I cancel Premium anytime?` | pinned value the product carries | C-FE-115 | Front-end specification, band 12 |
| `@driplog` | pinned value the product carries | C-FE-116 | Front-end specification, band 13 |
| `Too Lazy to Type In Every Expense? Let AI Read Your Receipts` | pinned value the product carries | C-FE-118 | Front-end specification, blog |
| `How Much Do Your Subscriptions Really Cost Per Year?` | pinned value the product carries | C-FE-119 | Front-end specification, blog |
| `The Best Way to Track Subscriptions on iPhone in 2026` | pinned value the product carries | C-FE-121 | Front-end specification, blog |
| `Subscription Creep: Why Your Money Quietly Disappears Every Month` | pinned value the product carries | C-FE-122 | Front-end specification, blog |
| `5000` | pinned value the product carries | C-CN-14 | Constraints |
| `2000` | pinned value the product carries | C-CN-15 | Constraints |
| `APP_PUBLIC_URL` | pinned value the product carries | C-DC-01 | Deployment contract |
| `4173` | pinned value the product carries | C-DC-02 | Deployment contract |
| `APP_PUBLIC_PORT` | pinned value the product carries | C-DC-03 | Deployment contract |
| `.browser_screenshots/` | pinned value the product carries | C-DC-08 | Deployment contract |
| `.downloads/` | pinned value the product carries | C-DC-09 | Deployment contract |
| `0.0.0.0` | pinned value the product carries | C-DC-14 | Deployment contract |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the token expiry duration | C-TR-18 | named as expiring, with no duration given in the brief |
| the base spacing unit | C-UX-50 | named as one unit the builder chooses, with no size given in the brief |
| the six measured layout steps | C-FE-23 | named as six steps, with no width given in the brief |
| the storage limit | C-CF-253 | named as a limit the runtime sets, with no byte count given in the brief |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 18 |
| User roles | 3 | 26 |
| Core features | 29 | 232 |
| User flow | 6 | 48 |
| UI/UX notes | 8 | 67 |
| Technical requirements | 12 | 56 |
| Data model | 10 | 68 |
| Front-end specification | 12 | 133 |
| Constraints | 2 | 15 |
| Deployment contract | 13 | 49 |

