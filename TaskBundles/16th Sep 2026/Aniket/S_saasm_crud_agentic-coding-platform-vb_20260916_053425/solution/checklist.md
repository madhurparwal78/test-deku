# Checklist: Marlin

Items: 315
Unpinned values flagged: 0
Sections present: Overview, User roles, Core features, User flow, UI and UX notes, Front-end specification, Technical requirements, Data model, Constraints, Deployment contract

---

## C-OV Overview

- [ ] `C-OV-1` `capability` The product is a public marketing site with a signed-in account surface for a coding agent sold to developers. `src: Overview para 1`
- [ ] `C-OV-2` `capability` The product does not build the coding agent, the desktop application, the terminal client, the models. `src: Overview para 1`
- [ ] `C-OV-3` `capability` Every public marketing route is readable without an account. `src: Overview para 3`
- [ ] `C-OV-4` `constraint` One benchmark registry feeds the leaderboard, the two model routes, the calculator, with no route holding its own copy of a figure. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-1` `role` A signed-out visitor may read every public route. `src: User roles table`
- [ ] `C-RL-2` `role` A signed-out visitor may not install a marketplace entry. `src: User roles table`
- [ ] `C-RL-3` `role` A signed-out visitor may not read any account route. `src: User roles table`
- [ ] `C-RL-4` `role` A member may read the member list of the workspace the member belongs to. `src: User roles table`
- [ ] `C-RL-5` `role` A member may not invite, remove, change any membership. `src: User roles table`
- [ ] `C-RL-6` `role` An owner may invite a colleague by address. `src: User roles table`
- [ ] `C-RL-7` `role` An owner may set, clear the workspace spend limit. `src: User roles table`
- [ ] `C-RL-8` `contract` A direct API call from a member session to an owner-only endpoint is denied by the server, leaving the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-9` `constraint` Signup is open to anyone from the signup route. `src: User roles, signup policy`
- [ ] `C-RL-10` `literal` Three accounts are seeded: `owner@example.com`, `member@example.com`, `owner2@example.com`. `src: User roles, seeded accounts`
- [ ] `C-RL-11` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles, seeded accounts`

## C-CF Core features

- [ ] `C-CF-1` `capability` An account is created by posting an address, a password, a display name to the signup endpoint. `src: Core features, Auth`
- [ ] `C-CF-2` `capability` A successful signin returns a bearer token. `src: Core features, Auth`
- [ ] `C-CF-3` `contract` A signup whose address is already registered is rejected as invalid, creating no second account. `src: Core features rule 1`
- [ ] `C-CF-4` `contract` A signin with a wrong password is denied, returning no token. `src: Core features rule 2`
- [ ] `C-CF-5` `contract` A signin refusal does not reveal whether the address exists. `src: Core features rule 2`
- [ ] `C-CF-6` `contract` A request to an account route without a valid bearer token is denied. `src: Core features rule 3`
- [ ] `C-CF-7` `contract` An expired token on an account route sends the browser to the signin route carrying the address the browser was trying to reach. `src: Core features rule 4`
- [ ] `C-CF-8` `contract` A return address that is not a path on the product own origin is discarded, so signin lands on the account overview. `src: Core features rule 5`
- [ ] `C-CF-9` `data` Passwords are hashed, never stored in readable form. `src: Core features, Auth`
- [ ] `C-CF-10` `ui` Every marketing route carries the same fixed bar. `src: Core features, public site`
- [ ] `C-CF-11` `ui` Every marketing route carries the same five-column footer. `src: Core features, public site`
- [ ] `C-CF-12` `literal` The first element in the document is a skip link reading `Skip to content`. `src: Core features, public site`
- [ ] `C-CF-13` `ui` The bar carries five centre items in the order Models, Product, Enterprise, Pricing, Resources. `src: Core features, public site`
- [ ] `C-CF-14` `literal` The bar carries three controls reading `Sign in`, `Contact sales`, `Download`. `src: Core features, public site`
- [ ] `C-CF-15` `ui` The footer compliance line names four certifications separated by vertical bars, reading SOC 2, ISO27001, ISO42001, AIUC-1 Certified. `src: Core features rule 6`
- [ ] `C-CF-16` `contract` The footer compliance line is one link, never four. `src: Core features rule 6`
- [ ] `C-CF-17` `ui` Six footer destinations that leave the origin are marked as leaving, opening in a new context. `src: Core features rule 7`
- [ ] `C-CF-18` `contract` Every internal link on every public route resolves. `src: Core features rule 8`
- [ ] `C-CF-19` `literal` The home headline reads `Marlin is your coding agent for building ambitious software.` `src: Core features, home route`
- [ ] `C-CF-20` `literal` The home trust line reads `Trusted every day by teams that build world-class software`. `src: Core features, home route`
- [ ] `C-CF-21` `ui` The home hero carries a primary control naming the resolved platform, a secondary control reading Request a demo. `src: Core features, home route`
- [ ] `C-CF-22` `literal` At a narrow width the home primary control reads `Get started`, dropping the platform name. `src: Core features rule 9`
- [ ] `C-CF-23` `literal` The install block carries two tabs, `PowerShell`, `Linux / WSL`, with the first selected. `src: Core features rule 10`
- [ ] `C-CF-24` `capability` The install tab selection is remembered for the visitor. `src: Core features rule 10`
- [ ] `C-CF-25` `capability` The install copy control writes the exact command shown, confirming by changing its own glyph for about two seconds. `src: Core features rule 10`
- [ ] `C-CF-26` `capability` The home changelog band renders the four most recent entries, date, title only, from the same source as the changelog route. `src: Core features rule 11`
- [ ] `C-CF-27` `contract` When the changelog source is unavailable the home band is omitted entirely, never rendered empty. `src: Core features rule 11`
- [ ] `C-CF-28` `literal` The home changelog band closing link reads `See what's new in Marlin`. `src: Core features rule 12`
- [ ] `C-CF-29` `ui` The eight customer marks on the home wall are Stitch, Northlight, Tessera, Aurora Data, Vantive, Plinth, Ravelin, Calyx. `src: Core features, home route`
- [ ] `C-CF-30` `capability` Six product routes share one template, differing only in content. `src: Core features, product route family`
- [ ] `C-CF-31` `ui` Each product route carries an eyebrow, a headline, a standfirst in the secondary text colour. `src: Core features, product route family`
- [ ] `C-CF-32` `constraint` A product route is a content document, so a seventh route requires no new component. `src: Core features rule 13`
- [ ] `C-CF-33` `capability` The automations route renders six template cards from the same marketplace source as the six seeded automations. `src: Core features rule 14`
- [ ] `C-CF-34` `literal` Each automation template card carries a control reading `Build from template`. `src: Core features rule 14`
- [ ] `C-CF-35` `literal` The teams route headline reads `Your best engineer's setup, for everyone`. `src: Core features, teams route`
- [ ] `C-CF-36` `capability` The teams route control leads to checkout when the visitor owns a workspace, to workspace creation when the visitor owns none, to signup when signed out. `src: Core features rule 15`
- [ ] `C-CF-37` `capability` An intent carried into signup is honoured after signup, never dropped. `src: Core features rule 15`
- [ ] `C-CF-38` `literal` The enterprise route headline reads `Develop enduring software at scale`. `src: Core features, enterprise route`
- [ ] `C-CF-39` `data` The enterprise customer-proportion claim is stored data carrying a source, an as-of date. `src: Core features rule 16`
- [ ] `C-CF-40` `contract` A claim past its expiry date does not render. `src: Core features rule 16`
- [ ] `C-CF-41` `constraint` There is no self-serve purchase path for the enterprise plan. `src: Core features rule 17`
- [ ] `C-CF-42` `ui` The changelog route is one column of entries, newest first, each carrying a date, a title, a standfirst, a body. `src: Core features, changelog`
- [ ] `C-CF-43` `literal` Four changelog entries are seeded: `cloud-agents-without-a-repository`, `subscriptions-and-pinned-skills`, `anchor-hosted-repositories`, `marlinbench-3-2`. `src: Core features, changelog`
- [ ] `C-CF-44` `contract` An unknown changelog slug answers as not found, never redirecting to the index. `src: Core features, changelog`
- [ ] `C-CF-45` `data` The model registry holds fifteen rows, each with a code, a name, a provider, a benchmark figure, a cost per task, tokens per task, steps per task. `src: Core features, model registry`
- [ ] `C-CF-46` `literal` The benchmark version is `MarlinBench 3.2`. `src: Core features, model registry`
- [ ] `C-CF-47` `data` Cost per task is an integer number of minor units, so `$17.32` is `1732`. `src: Core features, model registry`
- [ ] `C-CF-48` `contract` The benchmark plot horizontal axis descends left to right, placing the cheapest model at the right edge. `src: Core features rule 18`
- [ ] `C-CF-49` `ui` The leaderboard carries fifteen rows ranked by the benchmark figure descending, each with a colour dot tying the row to its plot series. `src: Core features rule 19`
- [ ] `C-CF-50` `ui` The leaderboard unit switch offers three choices with the first selected. `src: Core features rule 20`
- [ ] `C-CF-51` `contract` Switching the leaderboard unit changes which column is emphasised, never which rows exist, never the ordering. `src: Core features rule 20`
- [ ] `C-CF-52` `literal` The model `glim-7b` carries no measured cost per task. `src: Core features rule 21`
- [ ] `C-CF-53` `contract` A model with no measured cost per task is omitted from the plot, never plotted at zero. `src: Core features rule 21`
- [ ] `C-CF-54` `contract` A self-reported benchmark figure is marked in the accessible name of its cell, not only in a note beneath the table. `src: Core features rule 22`
- [ ] `C-CF-55` `ui` The benchmark plot carries a written description naming every model plotted in the chart. `src: Core features rule 23`
- [ ] `C-CF-56` `ui` The vendor model route uses the display face for exactly one word. `src: Core features rule 24`
- [ ] `C-CF-57` `capability` The partner model route renders from the same registry, never from a hand-authored figure. `src: Core features rule 25`
- [ ] `C-CF-58` `constraint` The calculator computes in the browser, submitting nothing, storing nothing. `src: Core features, value calculator`
- [ ] `C-CF-59` `contract` The calculator allocation must total exactly `100`, so a total that does not reach one hundred suppresses the outputs. `src: Core features rule 26`
- [ ] `C-CF-60` `contract` The calculator never silently normalises an allocation. `src: Core features rule 26`
- [ ] `C-CF-61` `constraint` No floating-point arithmetic touches money at any step of the calculator. `src: Core features rule 27`
- [ ] `C-CF-62` `literal` With `Kestrel 4` at `40`, `Meridian 4` at `60`, the blended cost per task is `$8.33`. `src: Core features rule 28`
- [ ] `C-CF-63` `literal` On the worked example the comparison line reads `52%` cheaper than `Kestrel 4`. `src: Core features rule 28`
- [ ] `C-CF-64` `literal` On the worked example the saving reads `$2,076.21` saved per month, `$24,914.55` per year. `src: Core features rule 28`
- [ ] `C-CF-65` `literal` On the worked example the breakdown shows a new annual spend of `$23,085.45` against `$48,000.00`. `src: Core features rule 28`
- [ ] `C-CF-66` `literal` On the worked example the tasks view reads `480` against `231`. `src: Core features rule 29`
- [ ] `C-CF-67` `contract` A shift to a more expensive model produces a negative saving, displayed as a loss, never as zero. `src: Core features rule 30`
- [ ] `C-CF-68` `contract` A model with no cost per task is absent from both calculator selects, from the allocation rows. `src: Core features rule 31`
- [ ] `C-CF-69` `ui` The calculator is prefilled with a plausible spend, a default pair of models. `src: Core features rule 32`
- [ ] `C-CF-70` `contract` An empty spend renders the calculator outputs as not applicable, never as zero. `src: Core features rule 32`
- [ ] `C-CF-71` `data` The catalogue holds sixteen published entries of two kinds. `src: Core features, marketplace`
- [ ] `C-CF-72` `literal` A seventeenth entry, `pallas-connect`, is seeded in state `withdrawn`. `src: Core features, marketplace`
- [ ] `C-CF-73` `capability` The catalogue listing endpoint accepts a query, a kind, a category, a sort, a page, a page size. `src: Core features rule 33`
- [ ] `C-CF-74` `capability` The catalogue query searches name, description, publisher together. `src: Core features rule 33`
- [ ] `C-CF-75` `contract` An unknown kind, an unknown category is rejected as invalid, never silently ignored. `src: Core features rule 33`
- [ ] `C-CF-76` `contract` The popularity ordering breaks a tie on the slug ascending. `src: Core features rule 34`
- [ ] `C-CF-77` `contract` A catalogue search is reflected in the address, so returning to the address reproduces the result set. `src: Core features rule 35`
- [ ] `C-CF-78` `capability` A catalogue detail route renders the tile, the name, the publisher, the full description, the category, the version, an install control. `src: Core features rule 36`
- [ ] `C-CF-79` `contract` A withdrawn catalogue entry answers as not found, appearing in no listing. `src: Core features rule 36`
- [ ] `C-CF-80` `contract` Installing is idempotent on the pair of subject, plugin, so a second call creates no second installation. `src: Core features rule 37`
- [ ] `C-CF-81` `literal` Installing `foolscap` once takes its count from `4820` to `4821`. `src: Core features rule 37`
- [ ] `C-CF-82` `contract` A signed-out visitor using an install control is sent to signin, returning to the entry afterwards. `src: Core features rule 38`
- [ ] `C-CF-83` `ui` A card description is truncated by a fade at its edge, never by an ellipsis, never by a server-side cut. `src: Core features rule 39`
- [ ] `C-CF-84` `ui` An empty catalogue search echoes the query, still rendering the featured section beneath. `src: Core features rule 40`
- [ ] `C-CF-85` `data` Eight platform rows exist at three versions, with no `linux` `armv7` `deb` artifact at `3.18`. `src: Core features, download`
- [ ] `C-CF-86` `capability` Resolution is a pure function from operating system, architecture, format, channel to one artifact. `src: Core features rule 41`
- [ ] `C-CF-87` `capability` An explicit query parameter overrides the declared platform, the declared architecture. `src: Core features rule 41`
- [ ] `C-CF-88` `contract` Resolution never blocks rendering, so the control renders with a neutral label, resolving in place. `src: Core features rule 42`
- [ ] `C-CF-89` `contract` An unknown platform resolves to a page listing every artifact, never to a guess. `src: Core features rule 43`
- [ ] `C-CF-90` `contract` Every artifact carries a checksum displayed beside the control. `src: Core features rule 44`
- [ ] `C-CF-91` `literal` The `3.18` `macos` `arm64` `dmg` checksum is `9f2a4c6e8b0d1357a9c2e4f60821b3d5c7e9f0a2b4d6e8f0a1c3e5d7b9f1a3c5`. `src: Core features rule 44`
- [ ] `C-CF-92` `contract` A missing artifact for a resolved platform offers the previous version marked as older, never a different platform. `src: Core features rule 45`
- [ ] `C-CF-93` `data` A download is recorded on resolution, carrying operating system, architecture, format, version, channel, referring route. `src: Core features rule 46`
- [ ] `C-CF-94` `constraint` A download event is not tied to an account. `src: Core features rule 46`
- [ ] `C-CF-95` `data` Four plans carry seven purchasable tiers. `src: Core features, plans`
- [ ] `C-CF-96` `literal` The pricing cards display `Free`, `$20` `/ mo.`, `$40` `/ user / mo.`, `Custom`. `src: Core features, plans`
- [ ] `C-CF-97` `contract` A capability granted at a lower tier order within a plan is granted at every higher order. `src: Core features rule 47`
- [ ] `C-CF-98` `contract` A capability granted on a lower plan is granted on every higher plan. `src: Core features rule 47`
- [ ] `C-CF-99` `capability` The interval switch changes the displayed price, the interval carried into checkout. `src: Core features rule 48`
- [ ] `C-CF-100` `contract` The interval switch is reflected in the address, never navigating. `src: Core features rule 48`
- [ ] `C-CF-101` `literal` The questions band is headed `Questions & Answers`, carrying four disclosures. `src: Core features rule 49`
- [ ] `C-CF-102` `contract` Each pricing disclosure is addressable by fragment. `src: Core features rule 49`
- [ ] `C-CF-103` `ui` A signed-in visitor sees the current tier marked as current, with its control reading as a management action. `src: Core features rule 50`
- [ ] `C-CF-104` `capability` Checkout creates the workspace billing account in the payment platform under a pinned external key. `src: Core features rule 51`
- [ ] `C-CF-105` `literal` The workspace external key scheme is `marlin-ws-<workspace-slug>`, for example `marlin-ws-northlight`. `src: Core features rule 51`
- [ ] `C-CF-106` `data` The billing account carries the workspace name, the owner address, the currency `USD`, the country `US`. `src: Core features rule 51`
- [ ] `C-CF-107` `contract` A second checkout for the same workspace creates no second billing account, leaving exactly one account with that external key. `src: Core features rule 52`
- [ ] `C-CF-108` `contract` A checkout that would produce a second live subscription for one subject is rejected as a conflict. `src: Core features rule 53`
- [ ] `C-CF-109` `contract` The product never shows a billing outcome the product has not read back from the payment platform. `src: Core features rule 54`
- [ ] `C-CF-110` `contract` The billing account is always identified by its external key, never by a generated identifier. `src: Core features rule 54`
- [ ] `C-CF-111` `capability` A tier upgrade within a plan is immediate, prorated for the remainder of the period. `src: Core features rule 55`
- [ ] `C-CF-112` `capability` A tier downgrade within a plan takes effect at the end of the period, with entitlements persisting until then. `src: Core features rule 55`
- [ ] `C-CF-113` `capability` Adding a seat is immediate, changing the seat count by exactly one. `src: Core features rule 55`
- [ ] `C-CF-114` `capability` Removing a seat takes effect at the end of the period. `src: Core features rule 55`
- [ ] `C-CF-115` `capability` Creating a workspace mints a slug from the name, making the caller its first owner with a seat. `src: Core features, workspaces`
- [ ] `C-CF-116` `capability` An owner invites a colleague by posting an address, a role to the workspace invitation endpoint. `src: Core features rule 56`
- [ ] `C-CF-117` `capability` An invitation sends one message over real SMTP to the invited address. `src: Core features rule 56`
- [ ] `C-CF-118` `literal` The invitation subject begins `Marlin invitation:` followed by a space, the workspace name. `src: Core features rule 57`
- [ ] `C-CF-119` `literal` An invitation to the seeded workspace carries the subject `Marlin invitation: Aurora Data`. `src: Core features rule 57`
- [ ] `C-CF-120` `contract` The invitation message is addressed to the invited address only, with no copy recipient, no blind copy recipient. `src: Core features rule 57`
- [ ] `C-CF-121` `contract` The invitation body is non-empty, naming the workspace, the inviter display name, the acceptance address. `src: Core features rule 57`
- [ ] `C-CF-122` `contract` Inviting an address that already holds a pending invitation re-sends the same acceptance link, creating no second invitation. `src: Core features rule 58`
- [ ] `C-CF-123` `contract` Revoking an invitation sends no message. `src: Core features rule 59`
- [ ] `C-CF-124` `contract` Changing a member role sends no message. `src: Core features rule 59`
- [ ] `C-CF-125` `contract` Removing a member sends no message. `src: Core features rule 59`
- [ ] `C-CF-126` `capability` Accepting an invitation turns the pending row into an active membership, consuming one seat. `src: Core features rule 60`
- [ ] `C-CF-127` `contract` An invitation token already accepted, revoked, expired is rejected, changing nothing. `src: Core features rule 60`
- [ ] `C-CF-128` `contract` A member calling the invitation endpoint directly is denied, creating no invitation, sending no message. `src: Core features rule 61`
- [ ] `C-CF-129` `contract` Removing a member releases the seat, revoking that member sessions at once. `src: Core features rule 62`
- [ ] `C-CF-130` `contract` The operation that would remove the last active owner fails, leaving the workspace with that owner. `src: Core features rule 62`
- [ ] `C-CF-131` `contract` A request for another workspace members, usage answers as not found rather than as denied. `src: Core features rule 63`
- [ ] `C-CF-132` `contract` A request inside the caller own workspace without the role for the action answers as denied. `src: Core features rule 63`
- [ ] `C-CF-133` `capability` Recording usage requires an owner, taking an idempotency key, a model code, a surface, a task count. `src: Core features, usage`
- [ ] `C-CF-134` `data` The rated cost is the task count multiplied by the model cost per task in integer minor units. `src: Core features rule 64`
- [ ] `C-CF-135` `contract` A model code with no measured cost per task is rejected as invalid, recording nothing. `src: Core features rule 64`
- [ ] `C-CF-136` `contract` Replaying a usage request with the same idempotency key adds no second row, changing no total. `src: Core features rule 65`
- [ ] `C-CF-137` `contract` The same idempotency key sent with a different body is rejected as a conflict. `src: Core features rule 65`
- [ ] `C-CF-138` `data` Each usage event carries two timestamps, one for when the usage happened, one for when the product recorded the usage. `src: Core features rule 66`
- [ ] `C-CF-139` `contract` A late usage event is attributed to the period the usage belongs to, never moved into the current period. `src: Core features rule 66`
- [ ] `C-CF-140` `capability` The usage endpoint returns the included allowance, the consumed amount, the overage, a breakdown by model, by member, by surface. `src: Core features rule 67`
- [ ] `C-CF-141` `contract` The included allowance for a per-seat tier is the tier allowance multiplied by the seat count. `src: Core features rule 67`
- [ ] `C-CF-142` `literal` The seeded workspace `aurora-data` reads `8869` consumed against `8000` included, leaving `869` of overage. `src: Core features rule 68`
- [ ] `C-CF-143` `literal` The seeded workspace `northlight` reads `384` consumed against `500` included with no overage. `src: Core features rule 68`
- [ ] `C-CF-144` `capability` An owner sets, clears the workspace spend limit in minor units. `src: Core features rule 69`
- [ ] `C-CF-145` `contract` Usage past the spend limit is refused with a distinct answer naming the limit. `src: Core features rule 70`
- [ ] `C-CF-146` `contract` Usage inside the included allowance is never refused by a spend limit. `src: Core features rule 70`
- [ ] `C-CF-147` `contract` Nothing is deleted for non-payment, so members, usage, installations, settings survive a lapsed subscription. `src: Core features rule 71`
- [ ] `C-CF-148` `ui` The account overview shows the current tier, the period usage against the allowance, the workspace. `src: Core features, account surface`
- [ ] `C-CF-149` `contract` An anonymous request for an account route lands on signin carrying the requested path. `src: Core features rule 72`
- [ ] `C-CF-150` `ui` An account belonging to no workspace sees workspace areas absent rather than disabled. `src: Core features rule 73`
- [ ] `C-CF-151` `ui` A member sees the members area as a read-only list with no invitation control. `src: Core features rule 74`
- [ ] `C-CF-152` `ui` The four legal routes share one template with a heading, an updated line, a contents list, an anchored body. `src: Core features, legal routes`
- [ ] `C-CF-153` `ui` The security route carries seven sections in a fixed order beginning with certifications, ending with vulnerability disclosures. `src: Core features rule 75`
- [ ] `C-CF-154` `data` Each certification carries an issuing body, a scope, a validity window, an evidence address. `src: Core features rule 76`
- [ ] `C-CF-155` `contract` A certification renders only during its validity window, so an expired certification disappears by itself. `src: Core features rule 76`
- [ ] `C-CF-156` `contract` The contents list is generated from the body headings, never authored. `src: Core features rule 77`
- [ ] `C-CF-157` `ui` An anchor target sits clear of the fixed bar. `src: Core features rule 78`
- [ ] `C-CF-158` `ui` Step one of the sales form collects exactly two fields. `src: Core features rule 79`
- [ ] `C-CF-159` `literal` The sales form step one control reads `Continue`. `src: Core features rule 79`
- [ ] `C-CF-160` `contract` A free-address provider is refused on the work address field with an explanation. `src: Core features rule 80`
- [ ] `C-CF-161` `contract` An unknown enquiry topic is refused on the server. `src: Core features rule 80`
- [ ] `C-CF-162` `ui` Validation runs on blur for a field the visitor has left, on submit for everything. `src: Core features rule 81`
- [ ] `C-CF-163` `ui` A failed submit moves focus to the first invalid field. `src: Core features rule 81`
- [ ] `C-CF-164` `constraint` The sales form control is never disabled to express invalidity. `src: Core features rule 81`
- [ ] `C-CF-165` `contract` A submission suspected of being automated is accepted, stored, flagged, never refused. `src: Core features rule 82`
- [ ] `C-CF-166` `contract` The visitor sees the confirmation once the enquiry is durably stored. `src: Core features rule 82`
- [ ] `C-CF-167` `data` The enquiry source is a closed set of four values with a fallback. `src: Core features rule 83`
- [ ] `C-CF-168` `contract` Submitting the same enquiry twice produces a confirmation both times, one stored enquiry. `src: Core features rule 84`
- [ ] `C-CF-169` `contract` An address matching no route renders the product own not-found page inside the full chrome, answering as not found. `src: Core features rule 85`
- [ ] `C-CF-170` `ui` The not-found page offers a search field scoped to the section the address fell in, three links back. `src: Core features rule 85`
- [ ] `C-CF-171` `contract` A removed thing answers as gone, saying the thing has been removed. `src: Core features rule 86`
- [ ] `C-CF-172` `contract` An unhandled failure answers as a server error, rendering a reference code the visitor can quote. `src: Core features rule 86`
- [ ] `C-CF-173` `contract` Every public route carries its own title, its own description, with no two routes sharing either. `src: Core features rule 87`
- [ ] `C-CF-174` `contract` A site map lists every public route, with a robots file pointing at the site map. `src: Core features rule 88`
- [ ] `C-CF-175` `contract` Nothing the browser downloads contains a credential, an interface key, an administrative token. `src: Core features rule 89`

## C-UF User flow

- [ ] `C-UF-1` `contract` Every route named in the brief route table is reachable. `src: User flow, route table`
- [ ] `C-UF-2` `contract` Signin with no return path lands on the account overview. `src: User flow, entry`
- [ ] `C-UF-3` `contract` Signing out clears the session, landing on the home route. `src: User flow, entry`
- [ ] `C-UF-4` `contract` A token expiring mid-action sends the browser to signin with the same return behaviour. `src: User flow, entry`
- [ ] `C-UF-5` `capability` A visitor can reach the calculator from the footer, set an allocation, read the saving. `src: User flow, journey 1`
- [ ] `C-UF-6` `capability` A visitor can sign up from the pricing route, create a workspace, confirm checkout, land on the billing area. `src: User flow, journey 2`
- [ ] `C-UF-7` `capability` An owner can invite a colleague, with the pending row appearing in place in the member list. `src: User flow, journey 3`
- [ ] `C-UF-8` `capability` A colleague can accept an invitation, with the seat count rising by one. `src: User flow, journey 3`
- [ ] `C-UF-9` `capability` A signed-in visitor can filter the catalogue by category, sort by popularity, install an entry. `src: User flow, journey 4`
- [ ] `C-UF-10` `ui` Every list has an empty state naming what is absent, offering a way back. `src: User flow, states`
- [ ] `C-UF-11` `ui` Every data-backed region has a loading state keeping the page headings, shape. `src: User flow, states`
- [ ] `C-UF-12` `contract` A failed operation leaves no partial state, so a refused checkout leaves no orphan billing account. `src: User flow, states`
- [ ] `C-UF-13` `contract` A refused invitation leaves no pending row, sending no message. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` The page ground is a near-white warm neutral, nearer unbleached paper than white. `src: UI/UX notes, palette`
- [ ] `C-UX-2` `ui` The foreground is a deep warm neutral reading as a very dark olive-brown. `src: UI/UX notes, palette`
- [ ] `C-UX-3` `ui` Every border, secondary text colour, overlay, hover wash is the foreground mixed into the ground at a stated share. `src: UI/UX notes, palette`
- [ ] `C-UX-4` `ui` One saturated colour appears in exactly three places, never as a button ground. `src: UI/UX notes, palette`
- [ ] `C-UX-5` `ui` The primary control carries the strongest contrast in the product, taking the foreground colour. `src: UI/UX notes, chrome`
- [ ] `C-UX-6` `ui` A deep soft teal marks an inserted line, a mid vivid red marks a removed line, neither appearing in the page chrome. `src: UI/UX notes, palette`
- [ ] `C-UX-7` `ui` Everything is set in one humanist grotesque carrying a variable axis of stroke thickness. `src: UI/UX notes, typography`
- [ ] `C-UX-8` `ui` The type scale is one base size multiplied by a ratio, with the multiplication authored rather than the result. `src: UI/UX notes, typography`
- [ ] `C-UX-9` `ui` Figures line up in a column wherever amounts stack. `src: UI/UX notes, typography`
- [ ] `C-UX-10` `ui` The marketplace tile corner is a proportional curve on a square rather than a fixed radius. `src: UI/UX notes, shape`
- [ ] `C-UX-11` `ui` Motion is eased throughout, with one speed for a state change, one for an entrance, one for an exit. `src: UI/UX notes, motion`
- [ ] `C-UX-12` `ui` An exit never uses the entrance curve. `src: UI/UX notes, motion`
- [ ] `C-UX-13` `ui` Where an element both moves, appears, the appearing is about five times quicker than the moving. `src: UI/UX notes, motion`
- [ ] `C-UX-14` `ui` Five named moments move on their own, with nothing else animating. `src: UI/UX notes, motion`
- [ ] `C-UX-15` `ui` Every shimmering row on a page shares one clock. `src: UI/UX notes, motion`
- [ ] `C-UX-16` `ui` A reduced-motion preference stops every loop at its most legible frame. `src: UI/UX notes, motion`
- [ ] `C-UX-17` `ui` Colour transitions survive a reduced-motion preference because a colour change carries meaning. `src: UI/UX notes, motion`
- [ ] `C-UX-18` `ui` The fixed bar is opaque, never translucent. `src: UI/UX notes, chrome`
- [ ] `C-UX-19` `ui` A navigation item fades to about three-quarters strength when pointed at, with nothing else changing. `src: UI/UX notes, chrome`
- [ ] `C-UX-20` `ui` The product does not lift its controls when pointed at. `src: UI/UX notes, chrome`
- [ ] `C-UX-21` `ui` A card darkens when pointed at on the page ground, lightening when pointed at on another card. `src: UI/UX notes, chrome`
- [ ] `C-UX-22` `ui` Contrast meets WCAG AA in both themes, verified independently. `src: UI/UX notes, accessibility`
- [ ] `C-UX-23` `ui` Keyboard navigation reaches everything a pointer reaches, with a visible focus ring. `src: UI/UX notes, accessibility`
- [ ] `C-UX-24` `ui` Meaning is never carried by colour alone. `src: UI/UX notes, accessibility`
- [ ] `C-UX-25` `ui` Each drawn window is one region carrying a written description, with its internals hidden from assistive technology. `src: UI/UX notes, accessibility`
- [ ] `C-UX-26` `ui` The layout answers to roughly six widths, holding at every width between them. `src: UI/UX notes, responsive`
- [ ] `C-UX-27` `ui` The document never scrolls sideways at any viewport width. `src: UI/UX notes, responsive`
- [ ] `C-UX-28` `ui` The drawn window runs off the trailing edge inside a clipped container at narrow widths rather than shrinking. `src: UI/UX notes, responsive`
- [ ] `C-UX-29` `ui` The theme control offers three states with system as the default. `src: UI/UX notes, theme`
- [ ] `C-UX-30` `ui` A visitor whose machine is set to dark sees dark on the first paint with no flash of the wrong theme. `src: UI/UX notes, theme`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` The drawn window carries a frame, a title bar, inner panes holding real text. `src: Front-end specification, drawn window`
- [ ] `C-FE-2` `ui` The task list groups rows under two headings, each carrying a count. `src: Front-end specification, task list`
- [ ] `C-FE-3` `ui` The chat pane renders a sequence of labelled agent steps, with the running step carrying the shimmer. `src: Front-end specification, chat pane`
- [ ] `C-FE-4` `ui` The caret is a solid block one line tall rather than a thin line. `src: Front-end specification, caret`
- [ ] `C-FE-5` `ui` When two windows overlap the front takes the heavier shadow, the one behind takes a hairline ring alone. `src: Front-end specification, composition`
- [ ] `C-FE-6` `ui` A window over the painted ground carries a blurred copy of that ground bright regions laid back on top. `src: Front-end specification, composition`
- [ ] `C-FE-7` `constraint` The drawn window text content is data, so one component is fed a script of steps. `src: Front-end specification, composition`
- [ ] `C-FE-8` `ui` The wallpaper is generated rather than photographed, carrying grain, a vertical softening. `src: Front-end specification, painted ground`
- [ ] `C-FE-9` `constraint` Every glyph is drawn as inline vector, never loaded as a font. `src: Front-end specification, iconography`
- [ ] `C-FE-10` `ui` The mobile route uses one translucent layered surface treatment found nowhere else. `src: Front-end specification, glass treatment`
- [ ] `C-FE-11` `constraint` No route depends on a binary image, a recorded video, an icon font arriving. `src: Front-end specification, zero-asset`
- [ ] `C-FE-12` `ui` An element animates once on first entering view, never reversing when scrolled back past. `src: Front-end specification, overflow`
- [ ] `C-FE-13` `ui` Text running past its box fades at the trailing edge over a real scroll container the keyboard can reach. `src: Front-end specification, overflow`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` The application is server-rendered, so every document arrives as complete markup from the server. `src: Technical requirements, stack`
- [ ] `C-TR-2` `constraint` Only the named libraries plus their direct dependencies are used. `src: Technical requirements, stack`
- [ ] `C-TR-3` `constraint` No second datastore, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements, stack`
- [ ] `C-TR-4` `contract` The three backing services are already running, so none is downloaded, installed, compiled, started. `src: Technical requirements, services`
- [ ] `C-TR-5` `literal` The datastore address is read from `DATABASE_URL`. `src: Technical requirements, services`
- [ ] `C-TR-6` `literal` The mail credentials are read from `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`. `src: Technical requirements, services`
- [ ] `C-TR-7` `literal` The payment credentials are read from `PAYMENTS_API_URL`, `PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`. `src: Technical requirements, services`
- [ ] `C-TR-8` `constraint` No host, no port is hardcoded. `src: Technical requirements, services`
- [ ] `C-TR-9` `constraint` Only the six named payment-platform paths are used, with refunds, payment methods, chargebacks out of reach. `src: Technical requirements, payment surface`
- [ ] `C-TR-10` `contract` A bearer token is read from the authorization header on every account route, every mutating endpoint. `src: Technical requirements, auth`
- [ ] `C-TR-11` `contract` No password, no token, no provider credential is returned in a response body. `src: Technical requirements, auth`
- [ ] `C-TR-12` `contract` Money is an integer number of minor units at every layer, formatted once at the edge. `src: Technical requirements, money`
- [ ] `C-TR-13` `contract` Every response carries the standard security headers. `src: Technical requirements, headers`
- [ ] `C-TR-14` `contract` Every state-changing request carries an origin check failing closed on a missing header. `src: Technical requirements, forgery`
- [ ] `C-TR-15` `contract` No state-changing action is reachable by a safe method. `src: Technical requirements, forgery`
- [ ] `C-TR-16` `contract` Server-side validation runs for every request regardless of what the browser already checked. `src: Technical requirements, validation`
- [ ] `C-TR-17` `contract` A business-rule violation is rejected as a client error naming the field, never as a server error. `src: Technical requirements, validation`
- [ ] `C-TR-18` `contract` A refusal caused by a spend limit is a distinct answer from a refusal caused by a role. `src: Technical requirements, validation`

## C-DM Data model

- [ ] `C-DM-1` `data` Fourteen tables exist, with every timestamp in UTC. `src: Data model, opening`
- [ ] `C-DM-2` `literal` Every seeded account uses the password `deku-demo-pw-2026`, written into `/app/USER_README.md`. `src: Data model, credentials`
- [ ] `C-DM-3` `data` The users table carries a unique address compared without regard to case. `src: Data model, users`
- [ ] `C-DM-4` `data` The workspaces table carries a unique slug, a tier code, a seat count, a nullable spend limit, a nullable billing external key. `src: Data model, workspaces`
- [ ] `C-DM-5` `data` One membership exists per workspace, per user. `src: Data model, memberships`
- [ ] `C-DM-6` `contract` A workspace always holds at least one active owner membership. `src: Data model, memberships`
- [ ] `C-DM-7` `data` One pending invitation exists per workspace, per address at a time. `src: Data model, invitations`
- [ ] `C-DM-8` `data` Seven tier rows exist carrying a plan code, an order within the plan, a monthly price, a yearly price, a per-seat flag, an included allowance. `src: Data model, tiers`
- [ ] `C-DM-9` `data` One entitlement row exists per tier, per capability. `src: Data model, entitlements`
- [ ] `C-DM-10` `contract` The product refuses to start rather than serve a state where the cumulative entitlement promise does not hold. `src: Data model, entitlements`
- [ ] `C-DM-11` `contract` At most one subscription row per subject is in a live state at any instant. `src: Data model, subscriptions`
- [ ] `C-DM-12` `contract` Two checkout requests racing for one subject produce exactly one winner, one conflict, one live subscription. `src: Data model, subscriptions`
- [ ] `C-DM-13` `data` The model series ordering is stable, never assigned by iteration order. `src: Data model, models`
- [ ] `C-DM-14` `data` One catalogue row exists per kind, per slug. `src: Data model, plugins`
- [ ] `C-DM-15` `data` The install count is derived from the installation rows rather than trusted as a stored counter. `src: Data model, plugins`
- [ ] `C-DM-16` `data` One installation row exists per subject, per plugin. `src: Data model, installations`
- [ ] `C-DM-17` `data` Twenty-three release artifact rows exist, one per version, operating system, architecture, format. `src: Data model, artifacts`
- [ ] `C-DM-18` `data` The usage table is append-only with an idempotency key unique across the table. `src: Data model, usage events`
- [ ] `C-DM-19` `data` The billing period is derived from when the usage happened, never from when the product recorded the usage. `src: Data model, usage events`
- [ ] `C-DM-20` `contract` The consumed amount reconciles exactly with the sum of the rated costs over the period. `src: Data model, allowances`
- [ ] `C-DM-21` `contract` A row carrying a workspace reference is readable only by an account holding an active membership in that workspace. `src: Data model, tenancy`
- [ ] `C-DM-22` `contract` Tenancy holds for a direct request with a valid token belonging to another workspace, not only for rendered pages. `src: Data model, tenancy`
- [ ] `C-DM-23` `literal` The seeded workspaces are `Aurora Data` with slug `aurora-data`, `Northlight` with slug `northlight`. `src: Data model, seed data`
- [ ] `C-DM-24` `literal` Four usage events are seeded: `seed-usage-aurora-1`, `seed-usage-aurora-2`, `seed-usage-aurora-3`, `seed-usage-northlight-1`. `src: Data model, seed data`
- [ ] `C-DM-25` `contract` Seeding is idempotent, so restarting the application duplicates no row. `src: Data model, seed data`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` One product, one origin, with no separate documentation application, no separate help centre. `src: Constraints`
- [ ] `C-CN-2` `constraint` The agent execution platform, the run list, the hosted code product are not built. `src: Constraints`
- [ ] `C-CN-3` `constraint` The integration registry, inbound webhooks, outbound webhooks are not built. `src: Constraints`
- [ ] `C-CN-4` `constraint` The publishing pipeline, the moderation queue for a catalogue entry are not built. `src: Constraints`
- [ ] `C-CN-5` `constraint` Every catalogue entry is free, with no basket, no checkout, no payout in the marketplace. `src: Constraints`
- [ ] `C-CN-6` `constraint` No external identity provider, no single sign-on, no directory synchronisation exists. `src: Constraints`
- [ ] `C-CN-7` `constraint` No refund, no payment method, no chargeback path exists. `src: Constraints`
- [ ] `C-CN-8` `constraint` No external network call is made at runtime beyond the three named backing services. `src: Constraints`
- [ ] `C-CN-9` `constraint` The calculator stores nothing, so analytics never record the entered spend. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The app must be reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-2` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, with `4173` the container-internal port. `src: Deployment contract`
- [ ] `C-DC-3` `contract` The HTTP API is served on that same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-4` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-5` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-6` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-7` `contract` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-8` `contract` A production build is served behind a static, preview server rather than a development server. `src: Deployment contract`
- [ ] `C-DC-9` `contract` The server keeps running after the session ends, never as a child of the shell. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No persistent volume, no fixed container name, no custom network is used. `src: Deployment contract`
- [ ] `C-DC-13` `contract` Every graded endpoint carries the request shape, the return shape named in the interface table. `src: Deployment contract, API shapes`
- [ ] `C-DC-14` `contract` A list endpoint returns a top-level array unless the interface table states an envelope. `src: Deployment contract, API shapes`
- [ ] `C-DC-15` `contract` An invalid call is rejected as a client error rather than as a server error, never as a silent success. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` The billing account is the payment platform record rather than a row the product wrote to itself. `src: Deployment contract, no mocks`
- [ ] `C-DC-17` `contract` The invitation is the message that left over SMTP rather than a row reading sent. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `owner@example.com` | pinned in the brief | `C-RL-10` |
| `member@example.com` | pinned in the brief | `C-RL-10` |
| `owner2@example.com` | pinned in the brief | `C-RL-10` |
| `deku-demo-pw-2026` | pinned in the brief | `C-RL-11` |
| `Skip to content` | pinned in the brief | `C-CF-12` |
| `Sign in` | pinned in the brief | `C-CF-14` |
| `Contact sales` | pinned in the brief | `C-CF-14` |
| `Download` | pinned in the brief | `C-CF-14` |
| `Marlin is your coding agent for building ambitious software.` | pinned in the brief | `C-CF-19` |
| `Trusted every day by teams that build world-class software` | pinned in the brief | `C-CF-20` |
| `Get started` | pinned in the brief | `C-CF-22` |
| `PowerShell` | pinned in the brief | `C-CF-23` |
| `Linux / WSL` | pinned in the brief | `C-CF-23` |
| `See what's new in Marlin` | pinned in the brief | `C-CF-28` |
| `Build from template` | pinned in the brief | `C-CF-34` |
| `Your best engineer's setup, for everyone` | pinned in the brief | `C-CF-35` |
| `Develop enduring software at scale` | pinned in the brief | `C-CF-38` |
| `cloud-agents-without-a-repository` | pinned in the brief | `C-CF-43` |
| `subscriptions-and-pinned-skills` | pinned in the brief | `C-CF-43` |
| `anchor-hosted-repositories` | pinned in the brief | `C-CF-43` |
| `marlinbench-3-2` | pinned in the brief | `C-CF-43` |
| `MarlinBench 3.2` | pinned in the brief | `C-CF-46` |
| `glim-7b` | pinned in the brief | `C-CF-52` |
| `Kestrel 4` | pinned in the brief | `C-CF-62` |
| `40` | pinned in the brief | `C-CF-62` |
| `Meridian 4` | pinned in the brief | `C-CF-62` |
| `60` | pinned in the brief | `C-CF-62` |
| `$8.33` | pinned in the brief | `C-CF-62` |
| `52%` | pinned in the brief | `C-CF-63` |
| `Kestrel 4` | pinned in the brief | `C-CF-63` |
| `$2,076.21` | pinned in the brief | `C-CF-64` |
| `$24,914.55` | pinned in the brief | `C-CF-64` |
| `$23,085.45` | pinned in the brief | `C-CF-65` |
| `$48,000.00` | pinned in the brief | `C-CF-65` |
| `480` | pinned in the brief | `C-CF-66` |
| `231` | pinned in the brief | `C-CF-66` |
| `pallas-connect` | pinned in the brief | `C-CF-72` |
| `withdrawn` | pinned in the brief | `C-CF-72` |
| `foolscap` | pinned in the brief | `C-CF-81` |
| `4820` | pinned in the brief | `C-CF-81` |
| `4821` | pinned in the brief | `C-CF-81` |
| `3.18` | pinned in the brief | `C-CF-91` |
| `macos` | pinned in the brief | `C-CF-91` |
| `arm64` | pinned in the brief | `C-CF-91` |
| `dmg` | pinned in the brief | `C-CF-91` |
| `9f2a4c6e8b0d1357a9c2e4f60821b3d5c7e9f0a2b4d6e8f0a1c3e5d7b9f1a3c5` | pinned in the brief | `C-CF-91` |
| `Free` | pinned in the brief | `C-CF-96` |
| `$20` | pinned in the brief | `C-CF-96` |
| `/ mo.` | pinned in the brief | `C-CF-96` |
| `$40` | pinned in the brief | `C-CF-96` |
| `/ user / mo.` | pinned in the brief | `C-CF-96` |
| `Custom` | pinned in the brief | `C-CF-96` |
| `Questions & Answers` | pinned in the brief | `C-CF-101` |
| `marlin-ws-<workspace-slug>` | pinned in the brief | `C-CF-105` |
| `marlin-ws-northlight` | pinned in the brief | `C-CF-105` |
| `Marlin invitation:` | pinned in the brief | `C-CF-118` |
| `Marlin invitation: Aurora Data` | pinned in the brief | `C-CF-119` |
| `aurora-data` | pinned in the brief | `C-CF-142` |
| `8869` | pinned in the brief | `C-CF-142` |
| `8000` | pinned in the brief | `C-CF-142` |
| `869` | pinned in the brief | `C-CF-142` |
| `northlight` | pinned in the brief | `C-CF-143` |
| `384` | pinned in the brief | `C-CF-143` |
| `500` | pinned in the brief | `C-CF-143` |
| `Continue` | pinned in the brief | `C-CF-159` |
| `DATABASE_URL` | pinned in the brief | `C-TR-5` |
| `SMTP_HOST` | pinned in the brief | `C-TR-6` |
| `SMTP_PORT` | pinned in the brief | `C-TR-6` |
| `SMTP_USER` | pinned in the brief | `C-TR-6` |
| `SMTP_PASS` | pinned in the brief | `C-TR-6` |
| `PAYMENTS_API_URL` | pinned in the brief | `C-TR-7` |
| `PAYMENTS_API_KEY` | pinned in the brief | `C-TR-7` |
| `PAYMENTS_API_SECRET` | pinned in the brief | `C-TR-7` |
| `deku-demo-pw-2026` | pinned in the brief | `C-DM-2` |
| `/app/USER_README.md` | pinned in the brief | `C-DM-2` |
| `Aurora Data` | pinned in the brief | `C-DM-23` |
| `aurora-data` | pinned in the brief | `C-DM-23` |
| `Northlight` | pinned in the brief | `C-DM-23` |
| `northlight` | pinned in the brief | `C-DM-23` |
| `seed-usage-aurora-1` | pinned in the brief | `C-DM-24` |
| `seed-usage-aurora-2` | pinned in the brief | `C-DM-24` |
| `seed-usage-aurora-3` | pinned in the brief | `C-DM-24` |
| `seed-usage-northlight-1` | pinned in the brief | `C-DM-24` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 4 |
| User roles | 3 | 11 |
| Core features | 50 | 175 |
| User flow | 7 | 13 |
| UI and UX notes | 5 | 30 |
| Front-end specification | 3 | 13 |
| Technical requirements | 5 | 18 |
| Data model | 10 | 25 |
| Constraints | 2 | 9 |
| Deployment contract | 12 | 17 |

