# Marlin

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser and compare fifteen coding models on the benchmark leaderboard, sign up, subscribe a workspace to the `Teams` plan at the `Standard` tier, and put a colleague on a seat, without hitting an error page. A different stranger, signed in to a workspace of their own, must NOT be able to read another workspace's members, usage or spend by any means, including a direct call to the API with a valid token of their own. The billing account must exist as a real record in `killbill` under the workspace's own external key; a green tick the app returns to itself does not count. The invitation must arrive as a real message at the invited address through `mailpit`; a row in the app's own table reading `sent` does not count.

## Overview

Marlin is a coding agent published by Northwind, Inc. and sold to individual developers and to engineering organisations. This is its public site and its account surface: the shop window that explains the agent and its surfaces, the marketplace that hands out the plugins and automations that extend it, the benchmark that justifies its price, and the till that signs people in, sells subscriptions and counts seats. The agent itself, the desktop application, the terminal client and the models are the thing being sold; they are not the thing being built. Wherever a route shows the product, it shows a drawing of it made of markup.

Four audiences arrive and each sees only a quarter of it. An individual developer lands on the home route and wants to understand the product in one screen and download it. A developer weighing cost opens the benchmark and the calculator and wants to know what a task costs and which model to pick. A developer extending the agent opens the marketplace and wants to install a plugin. A team lead opens the teams route and the pricing route and wants to know what a seat costs and how to put four colleagues on one.

Almost everything on the public site is readable without an account. Five actions create state and they are the ones worth building carefully: sign up or sign in, subscribe or change plan and interval, create a workspace and invite a colleague, install a plugin from the marketplace, and record usage against an allowance. Everything else is reading.

What this deliberately is not: no marketplace with money in it, because every plugin and automation is free and there is no payment between a publisher and an installer; no publishing or moderation pipeline; no agent execution platform and no run list; no hosted code product; no documentation site and no help centre; no blog, no careers listing and no community routes; no single sign-on and no directory synchronisation.

The genuinely hard part is that one dataset feeds three routes and one meter feeds two numbers, and neither may ever be typed into a page: the benchmark figures on the leaderboard, on the model routes and inside the calculator come from one registry, and the allowance, the overage and the spend limit all come from one append-only usage table whose replays must not be counted twice.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| visitor (signed out) | read every public route, browse and filter the marketplace, read the leaderboard, use the calculator, resolve a download, read the legal routes, sign up, sign in, submit the sales enquiry form | **install a plugin, create a workspace, subscribe, read any account route, read any workspace's members, usage or spend** |
| member | everything a visitor can do, plus read their own account, read their workspace's member list and usage, install a plugin for themselves, change their own display name and theme | **invite, remove or change a member, change the workspace subscription, set a spend limit, delete the workspace, or read any workspace they do not belong to** |
| owner | everything a member can do, plus invite a colleague, revoke a pending invitation, remove a member, change the workspace tier and interval, set or clear the spend limit, and record usage for the workspace | **remove the last active owner, or read any workspace they do not belong to** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a member session to any owner-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open: anyone may create an account from `/signup` with an address and a password, and a new account belongs to no workspace until it creates one or accepts an invitation. Three accounts are seeded for grading and every one of them uses the password `deku-demo-pw-2026`:

| Address | Display name | Workspace | Role |
|---|---|---|---|
| `owner@example.com` | `Devan Ashworth` | `Aurora Data` | owner |
| `member@example.com` | `Priya Raghunathan` | `Aurora Data` | member |
| `owner2@example.com` | `Marguerite Sandoval` | `Northlight` | owner |

## Core features

### Auth

Accounts are email and password, implemented by this application. Passwords are hashed and never stored or returned in readable form. `POST /api/auth/signup` takes `email`, `password` and `display_name` and returns a bearer token and the new account. `POST /api/auth/signin` takes `email` and `password` and returns a bearer token. Every account route and every mutating endpoint reads that token from the `Authorization` header as a bearer credential.

1. A signup whose address is already registered is rejected as invalid, names the field, and creates no second account.
2. A signin with a wrong password is denied and returns no token. The response does not say whether the address exists, and it takes the same time either way.
3. A request to any account route or any mutating endpoint without a valid bearer token is denied. A token that has expired is denied in the same way.
4. Tokens expire. An expired token on an account route sends the browser back to `/signin` carrying the address it was trying to reach, and the account route renders nothing in the meantime.
5. A return address is honoured only when it is a path on this origin. A return address pointing anywhere else is discarded and sign-in lands on `/account`.

### The public site and its chrome

Every marketing route carries the same fixed bar and the same five-column footer. The bar carries, left to right: the mark, then `Models`, `Product`, `Enterprise`, `Pricing` and `Resources`, then three controls reading `Sign in`, `Contact sales` and `Download`. The very first element in the document is a skip link reading `Skip to content`, hidden until it takes focus. `Enterprise` sits ahead of `Pricing` and the order is not rearranged.

The footer carries five columns. Product: `Agents`, `Teams`, `Enterprise`, `Pricing`, `Code Review`, `CLI`, `Cloud Agents`, `Meridian`, `Marketplace`. Resources: `Download`, `Changelog`, `Docs`, `Learn`, `Value Calculator`, `Forum`, `Help`, `Workshops`, `Status`. Company: `Careers`, `Blog`, `Community`, `Students`, `Brand`, `Future`, `Northwind, Inc.`. Legal: `Terms of Service`, `Acceptable Use Policy`, `Privacy Policy`, `Data Use`, `Security`. Connect: `X`, `LinkedIn`, `YouTube`. Beneath the columns sits a copyright line reading `2026` and `Northwind, Inc.`, one compliance link reading `SOC 2 | ISO27001 | ISO42001 | AIUC-1 Certified`, the three-state theme control and the language control reading `English`.

6. The compliance line is one link, not four. Four links would imply four destinations that do not exist.
7. Six footer destinations leave this origin and are marked as doing so: `Marketplace`, `Learn`, `Forum`, `Help`, `Status` and `Northwind, Inc.`. Each opens in a new context and the opened document cannot reach back to this one.
8. Every internal link on every public route resolves. A link in the chrome or the footer that answers not-found is a defect, and the routes this brief does not build (`Docs`, `Learn`, `Forum`, `Help`, `Workshops`, `Status`, `Careers`, `Blog`, `Community`, `Students`, `Brand`, `Future`, `Acceptable Use Policy`) are the six external destinations above plus routes that render a short placeholder document inside the full chrome rather than a not-found.

The home route is served at `/` and carries: a hero with the headline `Marlin is your coding agent for building ambitious software.`, a primary control reading `Download for macOS` whose platform name is resolved per the download rules below, a secondary control reading `Request a demo` leading to `/contact-sales?source=hero_request_demo`, and beneath them a drawn product window. Then a trust line reading `Trusted every day by teams that build world-class software` above a wall of eight customer marks: `Stitch`, `Northlight`, `Tessera`, `Aurora Data`, `Vantive`, `Plinth`, `Ravelin`, `Calyx`. Then a band headed `Agents turn ideas into code`, a band headed `In every tool, at every step`, an install block, a changelog band and a closing band.

9. At a narrow width the hero's primary control reads `Get started` and drops the platform name, because a handset visitor cannot install a desktop application.
10. The install block carries two tabs, `PowerShell` and `Linux / WSL`, with the first selected. The selected tab is remembered for the visitor. The copy control writes the exact command shown, including the `?win32=true` parameter on the `PowerShell` tab, and confirms by changing its own glyph for about two seconds rather than by opening a message. The command stays selectable text.
11. The changelog band renders the four most recent changelog entries, date and title only, read from the same source as `/changelog` and never from a second hand-maintained list. When that source is unavailable the band is omitted entirely rather than rendered empty.
12. The closing link of the changelog band reads `See what's new in Marlin` and is one of the three places on the whole site that wears the accent colour.

The product route family is six routes sharing one template and differing only in content: `/product`, `/cloud`, `/cli`, `/fixbot`, `/automate` and `/mobile`. Each carries an eyebrow, a headline, a standfirst in the secondary text colour, one primary control, a drawn product window, the trust line and mark wall, two to five feature bands, a testimonial band and a closing band.

| Route | Eyebrow | Headline | Standfirst |
|---|---|---|---|
| `/product` | `Agents` | `Turn ideas into code` | `Delegate implementation to focus on higher-level direction.` |
| `/cloud` | `Cloud` | `The next level of autonomy` | `Cloud agents control their own computers to build ambitious software.` |
| `/cli` | `CLI` | `Ship code with agents` | `Right from your terminal.` |
| `/fixbot` | `Fixbot` | `AI code review that catches real bugs` | `Fixbot detects the hardest logic bugs with a low false positive rate.` |
| `/automate` | `Marlin Automations` | `Save time by eliminating repetitive tasks.` | `Set up agents that run automatically based on schedules or event-based triggers.` |
| `/mobile` | `Mobile` | `Marlin on your phone` | `Start a task from anywhere and pick it up at your desk.` |

13. A route in this family is a content document, not a component tree: a heading, a standfirst, and an ordered list of bands each naming a window variant and its script. Adding a seventh route requires no new component.
14. `/automate` renders a gallery of six template cards whose titles and bodies come from the same marketplace source as the six automations listed below, never from a second copy. Each carries a control reading `Build from template`.

`/business/teams` carries the eyebrow `Marlin Teams`, the headline `Your best engineer's setup, for everyone`, the standfirst `Elevate your team with shared rules, skills, and workflows.`, one control reading `Get Teams`, a trust line reading `Trusted by teams that ship high-quality products.` and bands headed `Customize Marlin for how your team works`, `Agents that learn from your team's codebase`, `Move towards a self-driving codebase`, `Build programmatic agents`, `Agents that don't sleep`, `Your team's quality bar, enforced on every PR` and `Everywhere your team works`.

15. `Get Teams` leads to checkout for the `standard` tier when the visitor is signed in and owns a workspace, to workspace creation when they are signed in and own none, and to `/signup` carrying the intent when they are signed out. After signup or sign-in the intent is honoured rather than dropped.

`/enterprise` carries the headline `Develop enduring software at scale`, the standfirst `The choice for ambitious engineering teams.`, one control reading `Talk to the team` leading to `/contact-sales?source=navbar`, a trust line reading `Trusted by the world's leading enterprises.`, two quotes with a name, a job title and an employer, and bands headed `Your engineering knowledge base` and `Ship better software, faster`.

16. The enterprise route's customer-proportion claim is stored data carrying a source and an as-of date, rendered from that record and never typed into the template. A claim past its expiry date does not render at all.
17. There is no self-serve purchase path for the enterprise plan and there must not be one: its price is `Custom`, and a checkout for a custom price is a contradiction. The only control routes to `/contact-sales`.

`/changelog` is the dated release stream and its structure is one column of entries, newest first. Each entry carries a date at the tertiary colour, a title linking to the entry's own address at `/changelog/<slug>`, a standfirst of one or two paragraphs, and a body of anchored headings each preceded by a visible marker.

Four entries are seeded, newest first: `cloud-agents-without-a-repository`, `subscriptions-and-pinned-skills`, `anchor-hosted-repositories` and `marlinbench-3-2`.

An entry with no body is not renderable: an entry is a title plus a body. An unknown slug answers as not found and is never a redirect to the index, because a stale link to a real past release should say so.

### The model registry and the benchmark leaderboard

One registry of fifteen models feeds three surfaces: `/evals`, the two model routes `/meridian` and `/kestrel`, and the calculator at `/cost-savings`. No route carries its own copy of a number. `GET /api/models` returns the registry, including the benchmark version `MarlinBench 3.2`.

| Rank | `code` | Name | Provider | Score | Cost per task | Tokens per task | Steps per task | Self-reported |
|---|---|---|---|---|---|---|---|---|
| 1 | `meridian-4-max` | `Meridian 4 Max` | `Northwind` | `70.8%` | `281` | `41136` | `46` | no |
| 2 | `kestrel-4` | `Kestrel 4` | `Halyard` | `70.5%` | `1732` | `103525` | `72` | yes |
| 3 | `corvus-3-pro` | `Corvus 3 Pro` | `Ferrous` | `70.0%` | `823` | `61838` | `78` | no |
| 4 | `meridian-4` | `Meridian 4` | `Northwind` | `69.9%` | `234` | `32449` | `39` | no |
| 5 | `lyra-2-ultra` | `Lyra 2 Ultra` | `Orrery` | `69.3%` | `735` | `54239` | `72` | no |
| 6 | `tessel-9` | `Tessel 9` | `Wexford` | `68.4%` | `1173` | `64971` | `56` | no |
| 7 | `corvus-3` | `Corvus 3` | `Ferrous` | `67.2%` | `569` | `28320` | `48` | no |
| 8 | `meridian-4-mini` | `Meridian 4 Mini` | `Northwind` | `67.1%` | `128` | `17942` | `29` | no |
| 9 | `lyra-2` | `Lyra 2` | `Orrery` | `66.5%` | `612` | `30188` | `51` | no |
| 10 | `kestrel-3-5` | `Kestrel 3.5` | `Halyard` | `65.8%` | `944` | `47210` | `63` | no |
| 11 | `tessel-8` | `Tessel 8` | `Wexford` | `64.1%` | `358` | `22904` | `35` | no |
| 12 | `pallas-1-large` | `Pallas 1 Large` | `Calyx` | `62.7%` | `1508` | `88431` | `81` | yes |
| 13 | `corvus-2` | `Corvus 2` | `Ferrous` | `58.3%` | `205` | `19677` | `33` | no |
| 14 | `pallas-1` | `Pallas 1` | `Calyx` | `54.6%` | `176` | `15320` | `28` | no |
| 15 | `glim-7b` | `Glim 7B` | `Plinth` | `47.2%` | not measured | `9840` | `24` | no |

Cost per task is an integer number of minor units in `usd`. `1732` is `$17.32`; it is never stored, computed or transported as `17.32`.

18. `/evals` renders a plot above a leaderboard. The horizontal axis is average cost per task and it descends left to right, so cheap sits on the right and better sits up and to the right on both axes at once. Reversing it to the conventional ascending order inverts the argument the chart is making and is a defect.
19. The leaderboard carries the columns `MODEL`, `SCORE`, `COST / TASK`, `TOKENS / TASK`, `STEPS / TASK`, fifteen rows ranked by score descending, and a colour dot per row tying the row to its series in the plot. The chart's axis labels read `MarlinBench 3.2 score` and `Average cost per task`.
20. A unit switch offers `Cost`, `Tokens` and `Steps` with `Cost` selected. Switching changes which column is emphasised. It does not change which rows exist and it never re-sorts, because re-sorting would move the row the visitor is looking at.
21. `glim-7b` has no measured cost per task. Its row renders with the cost cell reading `not measured`, and it is omitted from the plot entirely. It is never plotted at zero, because zero is the far right of this chart, which is the position the chart uses to mean cheapest.
22. A score marked self-reported is a claim about provenance, not a footnote: the marking reaches the accessible name of the cell, not only a note beneath the table.
23. The plot carries a description naming every model in it, reading `A scatter and line chart comparing Meridian 4 Max through Glim 7B scores against average cost per task.`. The leaderboard beneath it is the accessible equivalent of the plot, so the plot itself may be hidden from assistive technology without loss.
24. `/meridian` is the only route in the product that uses the display face, and it uses it for exactly one word: the model-house name in its hero. It carries a four-column comparison table whose cells are a value plus an optional effort qualifier plus an optional footnote reference, never a preformatted string.
25. `/kestrel` is a landing route for one externally supplied model, rendered from the same registry.

### The value calculator

`/cost-savings` prices a shift of work between models. It is client-only by design: it computes in the browser, submits nothing and stores nothing, and it keeps working with the network switched off once the page has loaded. A visitor's budget is theirs, it is worthless to this product, and holding it would create an obligation the privacy route would then have to describe.

The route carries the headline `Spend less and ship more with your models.`, the standfirst `Move work to more efficient frontier models without giving up quality. Lower your spend or get more done for the same budget.`, a heading reading `Calculate savings`, and the instruction `Input your current expenses to see your savings`. The labelled inputs are `Current monthly spend on models`, `Model you use most`, `Model to shift to` and `Share of work shifted`. A disclosure reading `Advanced` opens a per-model allocation under the heading `Model allocation` with the help line `Split work across models. Adjust each model independently. Or match an advanced Marlin team`, one percentage row per model, and a running total labelled `Total:`.

The outputs are a blended cost per task with `per task` beneath it, a bracketed line naming a percentage `cheaper than` the baseline model, a view switch offering `Cost` and `Tasks`, a headline figure with `saved per month` beneath it and an annual figure in brackets, and a disclosure reading `Show breakdown` containing `Spend reduction`, `New annual spend`, the previous annual spend prefixed `was`, `New cost per task` and the previous cost per task. A footnote reads `Modeled on MarlinBench cost per task. Cost view reprices the same tasks. Tasks view keeps your budget fixed. Actual results depend on your workload.` and a note reads `The calculator reads costs directly from the graph and leaderboard below, shared with /evals.`

26. The allocation is a map from model to an integer percentage and it must total exactly `100`. The control does not silently normalise: it reports the total and refuses to compute, because normalising silently means the numbers being used are not the numbers the visitor typed.
27. Every currency value is an integer number of minor units. No floating-point arithmetic touches money at any point, including intermediate steps, and rounding happens exactly once, at display.
28. The worked example the arithmetic must reproduce: with `Kestrel 4` at `40` and `Meridian 4` at `60` and every other model at `0`, a current monthly spend of `$4,000.00` and `Kestrel 4` as the baseline, the blended cost per task is `$8.33`, which reads as `52%` cheaper than `Kestrel 4`; the saving is `$2,076.21` saved per month and `$24,914.55` per year; the breakdown shows a new annual spend of `$23,085.45` against a previous annual spend of `$48,000.00`, a new cost per task of `$8.33` and a previous cost per task of `$17.32`.
29. The tasks view holds the budget fixed and reports how many more tasks it buys. On the same example it reads `480` tasks against `231`.
30. A shift to a more expensive model is a legal input and produces a negative saving, displayed as a negative saving and never as zero. A calculator that cannot show a bad decision is an advertisement.
31. `glim-7b` has no cost per task and is therefore absent from both selects and from the allocation rows entirely.
32. The route is prefilled with a plausible spend and a default pair of models so it is legible before any input. An empty spend renders the outputs as not applicable, never as zero. An allocation that does not total one hundred suppresses the outputs and marks the total.

### The marketplace

`/marketplace` is the catalogue. Every entry is free: there is no basket, no checkout and no payout anywhere in it. The route carries a sidebar and a content column. The sidebar carries the title `Marketplace`, the filters `Featured`, `Recently Added`, `Plugins` and `Automations`, and the actions `Manage Automations`, `Documentation` and `Publish`. The content column carries the heading `Extend the Agent` and then sections headed `Featured Plugins`, `Featured Automations`, `Recently Added`, `Infrastructure` and `Data & Analytics`, each a grid of cards with a `See All Plugins` or `See All Automations` control and, where truncated, a control reading `View <n> more` carrying the exact residual count.

The catalogue is sixteen published entries. `kind` is `plugin` or `automation`, and the same spelling is used in the address, in the filter and in the stored record.

| `kind` | `slug` | Name | Publisher | Category | Description | Installs |
|---|---|---|---|---|---|---|
| `plugin` | `foolscap` | `Foolscap` | `Foolscap` | `Productivity` | `Search, read, create, and share files.` | `4820` |
| `plugin` | `loop` | `Loop` | `Loop` | `Communication` | `Search channels, send messages, and perform other actions.` | `6140` |
| `plugin` | `trace` | `Trace` | `Trace` | `Productivity` | `Search projects, create tasks, and post comments.` | `3975` |
| `plugin` | `atlas` | `Atlas` | `Atlas` | `Productivity` | `Create, find, and complete tasks and projects.` | `3975` |
| `plugin` | `klaxon` | `Klaxon` | `Klaxon` | `Infrastructure` | `Page responders, manage schedules, and resolve incidents.` | `2860` |
| `plugin` | `radar` | `Radar` | `Radar` | `Infrastructure` | `Query errors, traces, and release health.` | `2545` |
| `plugin` | `shipyard` | `Shipyard` | `Shipyard` | `Infrastructure` | `Deploy branches, roll back releases, and read build logs.` | `3310` |
| `plugin` | `tinbox` | `Tinbox` | `Tinbox` | `Infrastructure` | `Trigger builds, read pipelines, and download artifacts.` | `1490` |
| `plugin` | `quarry` | `Quarry` | `Quarry` | `Data & Analytics` | `Query and update sheets, rows, and workspaces.` | `2280` |
| `plugin` | `lumen` | `Lumen` | `Lumen` | `Data & Analytics` | `Analyze website traffic, audiences, and competitors.` | `1725` |
| `automation` | `assign-pr-reviewers` | `Assign PR reviewers` | `Marlin Team` | `Productivity` | `Assign reviewers based on code changes and auto-approve low-risk PRs` | `1980` |
| `automation` | `summarize-changes-daily` | `Summarize changes daily` | `Marlin Team` | `Communication` | `Post a daily Loop digest summarizing notable repository changes and risks from the previous day` | `1640` |
| `automation` | `find-vulnerabilities` | `Find vulnerabilities` | `Marlin Team` | `Infrastructure` | `Review pull requests for exploitable security issues and flag only validated findings before merge` | `2420` |
| `automation` | `fix-bugs-reported-in-loop` | `Fix bugs reported in Loop` | `Marlin Team` | `Communication` | `Monitor a Loop channel for bug reports, investigate the codebase, and fix with a PR` | `1215` |
| `automation` | `triage-failed-actions` | `Triage failed Forge Actions` | `Marlin Team` | `Infrastructure` | `Investigate failed or cancelled workflow runs and report findings in Loop` | `905` |
| `automation` | `automatic-test-coverage` | `Automatic test coverage` | `Marlin Team` | `Productivity` | `Create an automation to review every new commit and add tests for high-risk logic to improve test coverage.` | `1370` |

A seventeenth entry, the plugin `pallas-connect` named `Pallas Connect`, is seeded in state `withdrawn`.

33. `GET /api/plugins` accepts `q`, `kind`, `category`, `sort`, `page` and `per_page`. `q` searches name, description and publisher together. `kind` and `category` are closed sets and an unknown value is rejected as invalid, never silently ignored: a silent fallback is how a broken filter looks fine in testing and returns the whole catalogue in production.
34. `sort` is one of `relevance`, `recent` and `popular`. `relevance` is the default when `q` is present and `recent` otherwise. `popular` orders by installation count descending and then by `slug` ascending. The tie-break is not pedantry: `trace` and `atlas` both carry `3975` installs, and without it a paginated catalogue shows one of them twice and the other not at all.
35. A search is reflected in the address so it is linkable, and returning to that address reproduces the same result set.
36. `/marketplace/plugin/<slug>` and `/marketplace/automation/<slug>` render the detail: the tile at a larger size, the name, the publisher, the full description, the category, the version, and an install control. A `slug` in state `withdrawn`, such as `pallas-connect`, answers not-found and does not appear in any listing.
37. `POST /api/plugins/{kind}/{slug}/install` requires a bearer token. Installing is idempotent on the pair of subject and plugin: the second call creates no second installation and leaves the installation count exactly as the first call left it. Installing `foolscap` once takes its count from `4820` to `4821`; installing it again leaves it at `4821`.
38. A visitor with no account who uses an install control is sent to `/signin` and returns to the plugin afterwards.
39. A card's description is truncated by a fade at its edge, never by an ellipsis and never by a server-side character cut, because the full text is the accessible name and cutting it on the server loses it.
40. An empty search echoes the query, suggests clearing the filters, and still renders the featured section beneath, because a dead end is worse than a detour. An empty category renders the category heading with an explanation.

### Download and platform resolution

`/download` carries the headline `Use Marlin everywhere you work` and the standfirst `A unified workspace for agents across every surface.`. `GET /api/releases` returns the artifact matrix and `GET /api/releases/resolve` takes `os`, `arch`, `format` and `channel` and answers with one artifact carrying its `version`, `checksum`, `size_bytes` and `published_at`.

Eight platform rows exist, at versions `3.16`, `3.17` and `3.18`, latest first:

| `os` | `arch` | `format` |
|---|---|---|
| `macos` | `arm64` | `dmg` |
| `macos` | `x64` | `dmg` |
| `linux` | `x64` | `deb` |
| `linux` | `arm64` | `deb` |
| `linux` | `armv7` | `deb` |
| `windows` | `x64` | `exe` |
| `windows` | `x64` | `msi` |
| `windows` | `x64` | `zip` |

Version `3.18` publishes seven of the eight: there is no `linux` `armv7` `deb` artifact at `3.18`.

41. Resolution is a pure function from `os`, `arch`, `format` and `channel` to one artifact, and it is data rather than code. The client's declared platform is the primary signal, its declared architecture chooses between architectures, and an explicit query parameter overrides both.
42. Resolution never blocks rendering. The control renders with a neutral label and resolves in place, because a control that appears late shifts the layout.
43. An unknown platform resolves to a page listing every artifact and never to a guess. A wrong installer is worse than a choice.
44. Every artifact carries a checksum and the checksum is displayed beside the control, because this is an executable being downloaded over the internet. The `3.18` `macos` `arm64` `dmg` checksum is `9f2a4c6e8b0d1357a9c2e4f60821b3d5c7e9f0a2b4d6e8f0a1c3e5d7b9f1a3c5`.
45. When an artifact is missing for a resolved platform, the previous version is offered and marked as older. A `linux` `armv7` `deb` request resolves to `3.17` with a visible note that it is not the latest. It never silently falls back to the newest artifact of a different platform, because that is how somebody downloads an installer that will not run.
46. A download is recorded as an event carrying `os`, `arch`, `format`, `version`, resolved channel and the referring route. It is recorded on resolution rather than on completion, because completion is not observable, and it is not tied to an account, because requiring one to download would contradict the free plan.

### Plans, tiers and the subscription

`/pricing` carries the heading `Pricing`, an interval switch offering `Monthly` and `Yearly` with `Monthly` selected, four plan cards, a questions band and the trust line. `GET /api/plans` returns the plans, their tiers and their features.

| Plan | Displayed price | Sub-tiers | Control | Lead line |
|---|---|---|---|---|
| `Hobby` | `Free` | none | `Download` | `Includes:` |
| `Individual` | `$20` `/ mo.` | `Pro`, `Pro+`, `Ultra` | `Get Pro` | `Everything in Hobby, plus:` |
| `Teams` | `$40` `/ user / mo.` | `Standard`, `Premium` | `Get Teams` | `Everything on Individual, plus:` |
| `Enterprise` | `Custom` | none | `Contact Sales` | `Everything on Teams, plus:` |

Four plans, seven purchasable tiers. A plan code alone cannot express entitlement, which is why every gate is keyed on the tier.

| `tier_code` | Plan | Name | Monthly | Yearly | Per seat | Included allowance |
|---|---|---|---|---|---|---|
| `hobby` | `hobby` | `Hobby` | `0` | `0` | no | `500` |
| `pro` | `individual` | `Pro` | `2000` | `20000` | no | `2000` |
| `pro_plus` | `individual` | `Pro+` | `6000` | `60000` | no | `6000` |
| `ultra` | `individual` | `Ultra` | `20000` | `200000` | no | `20000` |
| `standard` | `teams` | `Standard` | `4000` | `40000` | yes | `4000` |
| `premium` | `teams` | `Premium` | `8000` | `80000` | yes | `8000` |
| `enterprise` | `enterprise` | `Enterprise` | custom | custom | yes | pooled |

The four feature lists, rendered from one entitlement record per tier and capability and never authored per card:

- `Hobby`: `No credit card required`, `Limited Agent requests`, `Access to Meridian`.
- `Individual`: `Extended limits on Agent`, `Generous limits for Kestrel 4`, `Access to frontier models`, `Beacon access`, `MCPs, skills, and hooks`, `Cloud agents`, `Fixbot on usage-based billing`.
- `Teams`: `Centralized team billing and administration`, `Team marketplace for internal rules, skills, and plugins`, `Cloud agents and automations with shared team context`, `Beacon access`, `Agentic code reviews with Fixbot`, `Usage analytics to understand team behavior`, `Team-wide privacy mode`, `SAML/OIDC SSO`.
- `Enterprise`: `Pooled usage`, `Invoice/PO billing`, `SCIM seat management`, `Repository, model, and MCP access controls`, `Auto-run, browser, and network controls`, `Audit logs and service accounts`, `AI code tracking API`, `Priority support and account management`.

47. The lists are cumulative and the cumulation is enforced by the system, not by whoever typed the lists. A capability granted at a lower order within a plan is granted at every higher order, and a capability granted on a lower plan is granted on every higher plan. The day a capability is added to a cheaper tier and forgotten on a dearer one, a paying customer has less than somebody paying nothing, and they report it as a billing fault.
48. The interval switch changes the displayed price and the interval carried into checkout. It is reflected in the address so a yearly price is linkable, it is one control pair with one pressed state rather than two independent controls, and switching it never navigates.
49. The questions band is headed `Questions & Answers` and carries four disclosures, each addressable by fragment so a support reply can link to an answer, with the question on the button rather than on a wrapping element. The questions are `What is the right plan for me?`, `What are my payment options?`, `How does usage-based pricing work?` and `Are prices inclusive of taxes?`. The third answer reads `Every plan includes a set amount of model usage. On-demand usage allows you to continue using models after your included amount is consumed, billed in arrears. See our docs for more details.`
50. A signed-in visitor sees their current tier marked as current, and its control reads as a management action rather than a purchase. A lower card's control reads as a downgrade.

`POST /api/billing/checkout` takes `tier_code` and `interval` and subscribes the caller's workspace. The payment platform is `killbill`, reached at `PAYMENTS_API_URL` with `PAYMENTS_API_KEY` and `PAYMENTS_API_SECRET`, plus the platform's own fixed basic credentials, the user `admin` and the password `password`, which are built into the service rather than issued per install. It is a billing platform holding accounts, catalog plans and invoices; it has no charge object, no card token and no decline code, so nothing in this product may reach for one.

51. Checkout creates the workspace's billing account in `killbill` under the external key scheme `marlin-ws-<workspace-slug>`, for example `marlin-ws-northlight`. The account carries the workspace name as `name`, the owner's address as `email`, `USD` as `currency` and `US` as `country`. A personal subject uses `marlin-user-<user-id>` instead.
52. The external key is unique in the payment platform, and that uniqueness is the whole idempotency mechanism: a second checkout for the same workspace is refused by the store rather than by application code, creates no second billing account, and leaves exactly one account with that external key.
53. A second checkout for a workspace that already holds a live subscription is a change of tier or interval, not a creation, and it is rejected as a conflict when it would produce a second live subscription. At most one subscription per subject is in state `active` or `past_due` at any time.
54. The app's own subscription record is a projection. It never shows a billing outcome it has not read back from `killbill`, and the account is always identified by its external key, never by an identifier the payment platform generated.
55. A tier upgrade within a plan is immediate and prorated, charged now for the remainder of the period; a downgrade within a plan takes effect at the end of the period and entitlements persist until then. An interval change from monthly to yearly is immediate and prorated with the credit applied; from yearly to monthly it takes effect at the end of the period. Adding a seat is immediate, prorated for the remainder of the period, and changes the seat count by exactly one; removing a seat takes effect at the end of the period, because the seat is paid for.

### Workspaces, seats and the invitation

A workspace is the tenant boundary. `POST /api/workspaces` takes a `name`, mints a `slug` from it, and makes the caller its first owner with a seat.

56. `POST /api/workspaces/{slug}/invitations` takes `email` and `role` and requires an owner. It creates a pending invitation and sends one message to that address through `mailpit`, over SMTP at `SMTP_HOST` and `SMTP_PORT` with `SMTP_USER` and `SMTP_PASS`.
57. The message is addressed to the invited address only, with no cc and no bcc. Its subject begins with `Marlin invitation:` followed by a space and the workspace name, so an invitation to `Aurora Data` carries the subject `Marlin invitation: Aurora Data`. Its body is non-empty, names the workspace and the inviter's display name, and carries the acceptance address.
58. Inviting an address that already holds a pending invitation for that workspace re-sends the same acceptance link and creates no second invitation.
59. No message is sent when an invitation is revoked, when a member's role changes, or when a member is removed. Those three transitions send nothing.
60. `POST /api/invitations/accept` takes the invitation token and requires a bearer token. It turns the pending invitation into an active membership, consumes one seat, and marks the invitation accepted. A token that is already accepted, revoked or expired is rejected and changes nothing.
61. A member may not invite, remove or change anyone. A direct call to the invitation endpoint from a member's session is denied and creates no invitation and sends no message.
62. Removing a member releases their seat and revokes their sessions at once. The transaction that would remove the last active owner fails and the workspace keeps that owner.
63. A workspace's members, usage and spend are readable only by a member of that workspace. A request for another workspace's members or usage answers not-found rather than forbidden, so that the other workspace's existence is not confirmed by the answer. Asking about something inside a workspace the caller does belong to, without the role for it, answers as denied, because there the existence is not a secret.

### Usage, allowance and overage

`POST /api/workspaces/{slug}/usage-events` records usage and requires an owner. The body carries `idempotency_key`, `model_code`, `surface` and `tasks`. `surface` is one of `desktop`, `terminal`, `cloud`, `mobile`, `review`, `automation` and `api`.

64. Metering records `tasks`, `model_code` and both timestamps; the money is derived. `rated_cost_minor` is `tasks` multiplied by that model's cost per task, computed in integer minor units. A `model_code` with no measured cost per task, such as `glim-7b`, is rejected as invalid and records nothing.
65. Every usage event carries an `idempotency_key` that is unique across the product. Replaying an identical request adds no second row, changes no total and returns the original event. Sending the same key with a different body is rejected as a conflict.
66. Each event carries two timestamps, `occurred_at` and `recorded_at`. `occurred_at` decides which billing period the event belongs to; `recorded_at` decides what the current period's running total shows. An event that arrives after its period is attributed to the period it belongs to and is reported as an adjustment naming that period, never quietly moved into the current one.
67. `GET /api/workspaces/{slug}/usage` returns, for the current billing period, the included allowance, the consumed amount, the on-demand overage and a breakdown by model, by member and by surface. The included allowance for a per-seat tier is the tier's allowance multiplied by the seat count, so `Aurora Data` on `standard` with two seats is included for `8000`.
68. Seeded usage makes `Aurora Data` read `8869` consumed against `8000` included, which is `869` of on-demand overage, displayed as `$8.69`. `Northlight` on `hobby` reads `384` consumed against `500` included and no overage.
69. `PUT /api/workspaces/{slug}/spend-limit` takes `limit_minor` and requires an owner. A null limit means no limit. `Aurora Data` is seeded with a limit of `2500`.
70. On-demand usage past the spend limit is refused, and the refusal names the limit and offers the way to raise it. It is a distinct answer from a permission refusal, because the two have different remedies. Usage inside the included allowance is never refused by a spend limit.
71. Nothing is ever deleted for non-payment. A subscription in state `past_due` removes the ability to spend on demand and never the ability to read: members, usage, installations and settings all survive, and everything is restored on payment with no re-onboarding.

### The account surface

`/account` is an overview showing the current tier, the current period's usage against the allowance, and the workspace. `/account/usage` carries the usage chart and the breakdown with a date-range control. `/account/billing` carries the tier, the interval, the seat count and the subscription state. `/account/members` carries the member list, the pending invitations and, for an owner, the invitation control. `/account/settings` carries the display name, the theme preference and the spend limit.

72. An anonymous request for any `/account` route lands on `/signin` carrying the requested path, and sign-in returns there.
73. A signed-in account belonging to no workspace sees the workspace-scoped areas absent rather than disabled, with one control offering to create a workspace.
74. A member sees `/account/members` as a read-only list with no invitation control, and the endpoint denies them regardless.

### The legal and trust routes

`/security`, `/privacy`, `/terms-of-service` and `/data-use` share one template: a heading, a line reading `Last updated` followed by a date, a contents list headed `Table of Contents` generated from the body's own headings, and a body of anchored headings each carrying a visible marker.

75. `/security` carries seven sections in order: `Certifications and third-party assessments`, `Infrastructure security`, `Client and agent security`, `Securing our own codebase`, `Privacy Mode`, `Account deletion` and `Vulnerability disclosures`. It opens with `Keeping your source code and developer environment secure is important to us. This page outlines how we approach security for Marlin.` Its privacy-mode paragraph reads `Privacy Mode can be enabled in settings or by a team or enterprise admin. Privacy Mode is available to anyone (free or Pro). New team members inherit the team's Privacy Mode settings. When enabled, we will not train on your data. We also implement technical controls and contractual requirements with our model providers to protect your data.` Its disclosure paragraph reads `We acknowledge vulnerability reports within 5 business days and address them as soon as we are able. Critical incidents are communicated via email to affected users.`
76. The four certification names in the footer come from stored records, each with an issuing body, a scope, a validity window and an evidence address, and a certification renders only while it is valid. An expired one disappears by itself, because nothing about a compliance claim should depend on somebody remembering to edit a template.
77. The contents list is generated from the body's headings rather than authored. A legal document whose contents list has drifted from its headings is a document nobody has read recently.
78. An anchor target sits clear of the fixed bar, so a link to a heading does not land underneath it.

### The sales enquiry form

`/contact-sales` is the only public write path. Its left column carries a heading, a positioning paragraph and a customer quote with a `Read story` link in the accent colour; its right column carries the heading `Contact our team`, the note `You can use this form to get in touch with our sales team. Thank you for your interest.` and a two-step form.

79. Step one collects exactly two fields, labelled `Work email` and `What can we help you with?`, the second a select whose placeholder reads `Select one`. Both are marked required with a marker in the accent colour. The control reads `Continue`, not `Submit`, because there is a second step. Step two collects a name, a company, a company size from a closed set, a region and an optional message.
80. A free-address provider is refused on the work-email field with an explanation rather than a silent failure, because the label says work. The topic must be one of a closed set and an unknown value is refused on the server.
81. Validation runs on blur for a field the visitor has left and on submit for everything, and never on every keystroke before a field has been left once. An error is attached to its field, is announced, and focus moves to the first invalid field on a failed submit. The control is never disabled to express invalidity, because a disabled control cannot explain itself.
82. A submission suspected of being automated is accepted, stored and flagged, never rejected, because turning away a real buyer is the most expensive error this form can make. The visitor sees the confirmation once the enquiry is durably stored, not once it has been delivered onward.
83. The `source` parameter is recorded on the enquiry and is never trusted as anything but a label: it is a closed set with an `other` fallback, and an unknown value never widens what the form can do. Four values exist: `navbar`, `hero_request_demo`, `blog_footer` and `help_center`.
84. Submitting the same enquiry twice produces a confirmation both times and one enquiry, because telling somebody they already asked is unhelpful.

### The not-found route, the site map and the page head

85. An address that matches no route renders this product's own not-found page, inside the full chrome, with a plain statement that the page does not exist, no apology and no joke, a search field scoped to the section the address fell in, and three links back. It answers as not found. It is never a redirect to the home route and never a successful answer carrying the home document.
86. The other statuses. A thing that existed and has been removed, such as a withdrawn plugin, answers as gone and says it has been removed rather than that it never existed, because people share those addresses. An unhandled failure answers as a server error and renders a plain document carrying the chrome and a reference code the visitor can quote. Planned unavailability answers as such and offers a retry hint. A handled, expected condition is never a server error.
87. Every public route carries its own title and its own description, and no two routes share either. The title names the route's subject before it names the product.
88. A site map lists every public route and a robots file points at it, both served from this origin at `/sitemap.xml` and `/robots.txt`.
89. Nothing the browser downloads contains a credential, an API key or an administrative token. The payment platform's key and secret, the mail credentials and the database address are read on the server and never reach a document, a script or a response body.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: hero, trust wall, bands, install block, changelog band | none |
| `/product` `/cloud` `/cli` `/fixbot` `/automate` `/mobile` | the product route family | none |
| `/meridian` `/kestrel` | the two model routes | none |
| `/evals` | the benchmark plot and leaderboard | none |
| `/cost-savings` | the value calculator | none |
| `/marketplace` | the catalogue, sidebar and sectioned grids | none |
| `/marketplace/plugin/<slug>` `/marketplace/automation/<slug>` | one catalogue entry | none |
| `/business/teams` | the teams argument | none |
| `/enterprise` | the enterprise argument | none |
| `/pricing` | four plans, seven tiers, the questions band | none |
| `/download` | the artifact matrix and the resolved control | none |
| `/changelog` | the dated release stream | none |
| `/security` `/privacy` `/terms-of-service` `/data-use` | the legal and trust family | none |
| `/contact-sales` | the two-step sales enquiry | none |
| `/signup` `/signin` | create an account, sign in | none |
| `/account` | plan, period usage, workspace | bearer |
| `/account/usage` | the usage chart and breakdown | bearer |
| `/account/billing` | tier, interval, seats, state | bearer |
| `/account/members` | members, invitations, seats | bearer |
| `/account/settings` | display name, theme, spend limit | bearer |
| `/sitemap.xml` `/robots.txt` | the site map and the robots file | none |

**Entry and redirects.** An anonymous request for any `/account` route lands on `/signin` carrying the requested path, and a successful sign-in returns there; a return path that is not a path on this origin is discarded and sign-in lands on `/account`. Sign-in with no return path lands on `/account`. Signing out clears the session and lands on `/`. A token that expires mid-action sends the browser back to `/signin` with the same return behaviour and the account route renders nothing in the meantime. A member reaching `/account/members` sees the list and no invitation control, and a direct call to the invitation endpoint is denied. Any unrouted address renders the product's own not-found page.

**Journeys.**

1. **Compare, then download.** Open `/`, follow `Pricing` in the bar, follow the footer's `Value Calculator` to `/cost-savings`, open `Advanced`, set `Kestrel 4` to `40` and `Meridian 4` to `60`, watch `Total:` reach `100`, read `$8.33` `per task` and `52%` `cheaper than` `Kestrel 4`, switch the view to `Tasks` and read `480` against `231`, then open `/evals`, switch the unit to `Tokens`, confirm `Glim 7B` shows `not measured` in its cost cell, and finish at `/download` where the control names a platform and shows a checksum.
2. **Sign up and subscribe.** Open `/pricing`, switch the interval to `Yearly`, choose `Get Teams`, land on `/signup`, create an account, create the workspace `Northlight Studio`, confirm checkout for the `standard` tier, land on `/account/billing` showing `Standard`, `Yearly` and one seat, and confirm the billing account exists in `killbill` under `marlin-ws-northlight-studio`. Submit the same checkout again and see it refused as a conflict with exactly one billing account still present.
3. **Invite a colleague.** Sign in as `owner@example.com` with `deku-demo-pw-2026`, open `/account/members`, invite `member@example.com` as a `member`, watch the pending row appear in place in the list, confirm the message `Marlin invitation: Aurora Data` arrives at `member@example.com` and nowhere else, sign in as `member@example.com`, accept, and watch the row become active with the seat count rising by one.
4. **Extend the agent.** Open `/marketplace`, filter to `Infrastructure`, sort by `popular`, open `Shipyard`, sign in as `member@example.com`, install it, watch its count rise by one, install it again and watch the count stay where it was.

**States.** Every list has an empty state that names what is absent and offers a way back: an empty search echoes the query and still shows the featured section, an empty category explains itself, a workspace with no pending invitations says so. Every data-backed region has a loading state that keeps the page's own headings and shape rather than collapsing it. Errors render inside the page's chrome as one plain sentence with a reference code the visitor can quote, and never replace the document with a trace. A failed operation leaves no partial state: a refused checkout leaves no half-built subscription and no orphan billing account, and a refused invitation leaves no pending row and sends no message.

## UI/UX notes

Somebody arriving should understand within one screen that this is a working tool for engineers, sold plainly, and that every picture on the page is the tool itself rather than an advertisement for it. The register is a shop window wrapped around an operational tool: the marketing bands may carry atmosphere and the subject, the drawn product window, must be the first thing seen, while the marketplace, the leaderboard and the account surface read quiet, dense and built for scanning.

Four stances govern every judgement, and a competing product could rationally hold the opposite of each. **Paper over panel**: the surface is barely shadowed and reads as paper lifted a hair off a desk, not as floating cards. **Derivation over declaration**: one ink thinned into the paper at stated shares, never a separately authored grey ramp. **Restraint over affordance**: a navigation item fades and nothing else moves, which is the only reason a fifty-link footer does not feel busy. **The subject over the frame**: the drawn window is the illustration and the page around it stays quiet.

**Palette, by role.** Five colours are declared and everything else is derived from them. The page ground is a near-white warm neutral, nearer unbleached paper than white. The ink is a deep warm neutral, a very dark olive-brown that reads as black only until it is set beside a true black. A card ground is one step down from the page ground in the same family, with a four-step ladder beneath it and one warmer card used behind product art. One saturated colour exists, a deep vivid orange, and it appears in exactly three places and nowhere else: the required-field marker on the sales form, a link inside running text, and the changelog band's closing link. It is never a button ground, and the primary control is the ink. Every border, every secondary and tertiary text colour, every overlay and every hover wash is that one ink mixed into the ground at a stated share, so the theme is a handful of roots rather than sixty values. Flattening those mixes into fixed greys looks almost right in daylight and obviously wrong at night.

Two meaning-carrying colours live inside the drawn windows and the usage charts and appear nowhere in the page chrome: a deep soft teal for an inserted line and an added count, and a mid vivid red for a removed line and a removed count. The version-control status set adds a deep vivid orange for modified and a deep soft cyan for untracked. The usage series is a mid soft blue with a faint area fill. The review report's legend carries four severities and two states, the states being a mid soft green for an open change and a light vivid indigo for a merged one, and its total series is a light soft magenta. A state that is none of these may not borrow any of them. The exact shades are yours, so long as the derivation holds, the accent stays rare and off the primary control, and the line wash and the inline token wash stay separately authored at different strengths.

**Typography.** Three roles. Everything is set in one humanist grotesque with a variable weight axis. One display face, which may be the same family at its heaviest optical size, carries exactly one word on exactly one route: the model-house name in the hero of `/meridian`. A monospace with a true oblique carries anything meant to look like a terminal, which is the install block and every pane inside a drawn window. Long-form editorial uses `EB Garamond` with a declared fallback stack. Each family declares a metric-matched local fallback so the swap does not reflow the page.

The scale is one base size of `15px` multiplied by a ratio, and the multiplications are authored rather than their results: `0.875` for captions, `1.375` for a subheading, `2.25` for a band heading, `3.25` for a hero heading and `4.5` for the largest display line. Line height is a multiplier throughout and tightens as size grows, from `1.5` on body text to `1.2` on headings and `1.1` on the display line. Letter spacing tightens as size grows too, which is the only reason the display sizes read as designed rather than as scaled-up body text. Hierarchy comes from size, colour and spacing rather than from weight: the rendered scale is overwhelmingly regular, and reaching for bold reads wrong in a way that is hard to name. Figures line up in a column wherever amounts stack, which is the leaderboard, the calculator's breakdown, the plan prices and the usage table.

**Shape, space and elevation.** Every gap is a multiple of one base unit, which is yours to choose, with the gap between bands roughly three times the gap beneath a heading and about halving on a narrow screen. Corners are barely softened, with two exceptions: every control in the bar is a pill, and the marketplace tile's corner is a proportional curve on a square rather than a fixed radius, which is instantly recognisable as wrong when it is a fixed one even to somebody who cannot say why. The site is barely shadowed: a card's shadow reads as paper lifted a hair, and a dialog is that same shadow plus a ring, the two separable so a card can gain a border on hover without re-authoring its shadow. The most repeated elevation in the product is an inset hairline ring on the marketplace tile, so its rounded corner stays crisp against its own artwork.

**Motion.** Movement is eased throughout: considered entrance and exit easing, reading as a designed interface rather than as a machine. One speed for a state change, one for an entrance and one for an exit, and an exit never uses the entrance curve, because a panel that leaves on a decelerating ease appears to stick. Where an element both moves and appears, the appearing is about five times quicker than the moving, so it is fully solid roughly a fifth of the way through its journey; matching the two lengths is the single most common way to get this wrong and makes the whole product feel like it is fading rather than moving. A visibility change is delayed until the fade ends, so a dismissed layer leaves the pointer's way and the reading order the instant it is gone rather than sitting invisible and catching clicks.

Five moments are named and only these move on their own: a spinner that turns; a pulse that breathes to half strength; a shimmer that is a bar of light sweeping across a loading row, its bright band sitting just past centre so the sweep reads as travelling in a direction, with every shimmering row on a page sharing one clock so a column sweeps as one band rather than as a dozen independent ones; a tile that pops in; and a highlight that wipes in from the left, holds for half its life, then jumps its anchor to the far edge and shrinks away, one movement in two directions. Nothing else animates. The drawn product window plays a scripted sequence once, on entry, and ends in a composed final state; it is not a loop, and any always-running loop pauses when its element leaves the viewport.

Durations are yours to choose and none is quoted here, because the requirement is that everything shares one family of speeds and one family of curves rather than that any particular number is used. What is not yours is the relationship: the state change is the shortest, the entrance sits just above it, the one large positional move on a full-width element is the only thing in the product allowed to take longer than half a second, and nothing uses a speed of its own to feel special.

Every one of these respects `prefers-reduced-motion`. Under a reduce preference the loops stop at their most legible frame, entrances and exits become opacity alone with no travel and no blur, the mark wall and any marquee go static while staying scrollable by pointer and by keyboard, and each drawn window renders its composed final frame directly rather than an empty editor. Colour and state transitions are kept, because a colour change carries meaning and removing it removes feedback.

**Chrome and controls.** The bar is fixed and opaque. Making it translucent is the single easiest way to make this read as a different, more fashionable product. A navigation item fades to about three-quarters strength when pointed at and nothing else happens: no underline appears, no weight changes, no box lights up behind it, and the item's own caret fades with it so the whole item dims as one object. A menu opens on click, closes on a second click, on escape, on a click outside it and on navigation, and only one is open at a time. There is one primary control style and one quieter alternative, plus a ghost and a destructive variant; the primary carries the strongest contrast in the product and is the ink rather than the accent. All four have resting, pointed-at, pressed, focused and unavailable states, the transition moves the colour properties together and nothing else, and unavailable is never signalled by colour alone. This product does not lift its controls when they are pointed at, and adding a lift is the second easiest way to make it read as a different product.

Cards darken when they are pointed at if they sit on the page ground and lighten if they sit on another card. Both directions are deliberate: the second is what keeps a card visible when it is stacked on something its own colour.

**Accessibility bars, which are contract rather than taste.** Three corrections govern the structure before anything else: an address that does not exist announces itself as missing rather than as the home route, anything reachable by keyboard shows a ring when it is reached, and each drawn window is one described region rather than hundreds of loose text nodes. Contrast meets WCAG AA in both themes, verified independently, and the faintest tertiary text is checked against every ground it appears on rather than only against the page ground. Touch targets are comfortably sized on their smaller axis. Keyboard navigation reaches everything a pointer reaches, with a visible focus ring that follows the element's own corner, appears for keyboard focus and is suppressed for pointer focus, and is never removed without replacement. Icon-only controls carry labels. Meaning is never carried by colour alone. One top-level heading per route, naming the route's subject rather than the product, with levels descending without skipping and the eyebrow above a hero not counting as a heading. Each drawn window is one region carrying its written description as content with its internals hidden, or the illustration reads as a wall of disconnected words. The copy control announces success through a live region rather than only by changing its glyph, and the calculator's running total is announced when it changes.

**Responsive.** The layout answers to roughly six widths and holds at every width between them. Narrow: the bar keeps the mark, `Sign in` and the navigation control while the rest becomes a full-height panel that traps focus, stops the document scrolling and returns focus to the control that opened it; bands become one column; the plan cards stack with the current plan first; the mark wall becomes a scrolling row; the marketplace sidebar becomes a control and its grid one column; filter rows become a select; the footer columns stack; comparison tables scroll sideways behind an edge fade rather than being cut. One exception is deliberate: the drawn product window does not shrink at narrow widths but runs off the trailing edge inside a clipped container, because scaling it down makes its text illegible while cropping it implies the window continues. At a narrow viewport the document itself never scrolls sideways, every navigation target stays reachable, and the layout survives a doubled and a quadrupled zoom without losing content or overlapping.

**Theme.** Three states: system, light and dark, with system the default and not the same as light. A visitor whose machine is set to dark and who has never touched the control gets dark on the first paint, with no flash of the wrong theme, which means the choice is known before the document is drawn. Dark re-points the same small set of roots and every derived value follows. Three things do not follow and are authored: the customer marks, which ship in two variants chosen by theme; the ground behind the drawn windows, which needs a dimmed variant; and the added and removed colours, which are tuned for a pale ground and need counterparts at equal perceived contrast rather than the same values.

**What it must not look like.** No page dominated by a single hue family with no second signal. No decoration standing in for content. No marketing composition where the working interface belongs. Nothing borrowed from a template unrelated to a developer tool. No frosted bar, no lifted controls, no fixed corner on the marketplace tile.

## Front-end specification

This section carries the visual detail that does not fit above. Everything here is appearance; nothing here overrides a rule stated elsewhere.

**The drawn product window.** It is the recurring hero object and it appears on the home route, on every route in the product family, on the teams route and on the enterprise route. It is drawn in markup, not photographed and not recorded: a frame with a title bar carrying a three-dot cluster and a centred label, one or more inner panes, and real text inside them.

Its parts, each of which appears in at least one variant:

- **The task list.** Rows grouped under two headings reading `In Progress` and `Ready for Review`, each carrying a count. Each row shows a status glyph, a truncated title, a relative time, and for a completed row a diff summary of an added count in the added colour and a removed count in the removed colour. The subtitle beneath a running row carries the shimmer.
- **The editor pane.** A tab strip of file names, a breadcrumb, a model label, a build control, and a body of syntax-coloured text whose roles are named rather than hard-coded, so the same pane works in both themes.
- **The chat pane.** A prompt bubble on the card ground, then a sequence of agent steps whose labels read `Thought`, `Read`, `Searched`, `Explored`, `Ran`, `Created`, `Started` and `Worked for`. Each step is a label in the secondary text colour and a value in the tertiary, and the running one carries the shimmer. Beneath it a follow-up field whose placeholder reads `Add a follow up...`, with a mode label reading `Agent` or `Plan`, a model label and a submit control; the container takes a focus ring when anything inside it has focus.
- **The terminal pane.** Monospace throughout: a prompt row, a working directory in the secondary colour, a boxed instruction, then step rows, and a status line carrying a mode name, a model name with a percentage and three key hints.
- **The caret.** It is a solid block one line tall in the ink, pulsing. It is a block, not a line, because the whole component is quoting a terminal.

Three composition rules. When two windows overlap, the front one takes the heavier shadow and the one behind takes a hairline ring alone, or the pair reads as two flat cards. When a window sits on the painted ground, a heavily blurred copy of that ground's bright regions is laid back over it, which is what stops the composite reading as a sticker on a photograph. And the window's text content is data rather than markup: one component fed a script of steps, not six components, because six will drift.

**The painted ground.** The wallpaper behind several windows is generated rather than photographed: a vertical gradient from a warm pale sky through a mid band to a darker foreground, taken from the card ladder rather than from saturated colours; two or three soft horizontal bands at low strength standing in for terrain; one warm highlight region standing in for light on a slope; a fine grain overlay with the saturation removed; and a slight vertical softening so no edge in the result is crisp. The grain and the softening are the parts that matter, because a clean gradient reads as a template. The dark variant is the same generation with the brightness reduced.

**The glass treatment.** The `/mobile` route uses one surface treatment found nowhere else: a translucent card whose ground is a diagonal gradient of white falling away in three stops, lifted by four separate shadow layers at once, a bright hairline inset along its top edge, a dimmer one along its bottom, a soft blue-tinted drop and a tight contact shadow, with a faint backdrop softening behind it and a generously rounded corner. The four layers are the whole effect and dropping any one of them flattens it. The larger card variant uses a warmer, more opaque gradient of the same shape.

**The mark, and zero-asset construction.** Every part of the drawn window, the mark and the wallpaper is markup and colour: the product ships no photograph, no recorded video and no icon font, and no route depends on a binary asset arriving. The lockup is a mark and a wordmark in one box whose proportions are fixed: the mark occupies the leading fifth, a small gap follows, and the wordmark fills the rest. The mark itself is a construction rather than a tracing, one closed path with an internal void, drawn as a cube in an isometric-adjacent projection with rounded vertices, never as a stack of three rhombi, which produces visible seams at the size it is used.

**Iconography.** Every glyph is drawn as inline vector, never loaded as a font: a font cannot take two colours, and a font that fails to load leaves its fallback character visible. The set is a downward chevron for an expandable menu, a rightward chevron for a drill-in row, an upward chevron for an open disclosure, a downward arrow to a bar for download, a number sign for a link to a heading, a north-east arrow for a destination that leaves the origin, a shield for the compliance line, a display, a sun and a moon for the three theme states, a globe for the language control, a magnifier for search, a filled check for a plan feature row, and a solid triangle for a compact select. All are drawn on one box at one stroke weight with round caps and joins.

Two composite glyphs carry motion and only these two do: a check ring built from two stacked circles whose dash arrays interpolate, filling from the top rather than from the right; and a pending ring whose chasing arc is deliberately set to a length that does not divide evenly into its circumference, so the sweep never quite repeats. Tidying that length up makes it repeat and it immediately reads as mechanical.

**The customer mark wall.** Eight cells at wide widths, each bordered, each holding a mark constrained to a common height with automatic width. Two marks carry light and dark variants chosen by theme. One variant flips its cells to cycle through more marks than the wall holds: the flip is staggered per cell rather than synchronised, it pauses while the pointer is over the wall so a mark can be read, and under a reduced-motion preference the wall renders one fixed set and does not cycle.

**Overflow and scrolling.** Nothing on this site is tied to scroll position: there is no pinned section, no scrubbed timeline and no hijacked scrolling. An element animates once, the first time any part of it enters view, does not reverse when scrolled back past, and is simply already in place with no movement at all when the visitor arrives with it already in view, so a deep link never lands on an invisible page. Text that runs past its box fades out at its trailing edge rather than being cut or given an ellipsis, and the fade is decoration over a real scroll container the keyboard can reach, never a substitute for one. A vertical variant of that fade, shaped so it holds full strength for the first half and then falls away quickly, marks a list that continues rather than a list that ends.

**States, everywhere.** A loading region keeps its own headings and renders skeleton rows carrying the shimmer, synchronised. An empty region names what is absent and offers the nearest useful action. An error region carries one plain sentence, a reference code and a way back, inside the chrome. A destructive action confirms first. Escape closes any layer that opened over the page and returns focus to whatever opened it.

## Technical requirements

The application is a server-rendered multi-page product built with **Flask** and **Jinja** templates, progressively enhanced with **HTMX** over those same templates plus plain browser scripting for the parts that genuinely need it: the navigation menus and the narrow panel, the drawn window's scripted sequence, the platform resolution, the install block's tab and copy control, the interval switch and the sub-tier switches, the questions accordion, the calculator, the leaderboard's unit switch, the marketplace search and filters, the sales form, and the theme and language controls. Every document arrives as complete HTML from the server; there is no client-side router and no hydrated document.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are **PostgreSQL**, **killbill** and **mailpit**, and reaching for anything else is a contract violation.

The backing services are already running and reachable at their environment variables, and must not be downloaded, installed, compiled or started. Read `DATABASE_URL` for PostgreSQL. Read `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS` for mailpit, which accepts real SMTP. Read `PAYMENTS_API_URL`, `PAYMENTS_API_KEY` and `PAYMENTS_API_SECRET` for killbill; its basic credentials are the service's own fixed pair and are given above. Read `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` for the app's own address. Never hardcode a host or a port.

The killbill surface this product may use is exactly this and nothing else: `GET /1.0/healthcheck` is an unauthenticated liveness probe; `GET /1.0/kb/accounts?externalKey=<key>` answers with the account or reports it absent; `POST /1.0/kb/accounts` takes `name`, `externalKey`, `email`, `currency` and `country`; `GET /1.0/kb/accounts/pagination` lists every account in the tenant; `GET /1.0/kb/catalog/availableBasePlans` lists the plans a subscription may reference; `GET /1.0/kb/invoices/pagination` lists every invoice. Every call under `/1.0/kb/` carries those basic credentials plus the API key and the API secret, and every write additionally names its writer. Refunds, payment methods and chargebacks are not part of this surface and nothing may reach for them.

Authentication is email and password implemented by this application, with a bearer token returned on a successful sign-in and read from the `Authorization` header on every account route and every mutating endpoint. Passwords are hashed. No password, no token and no provider credential is ever returned in a response body or written into a document the browser downloads.

`GET /api/health` returns `200` once the application is ready and its datastore answers. Request logging is one line per request on standard output.

Money is an integer number of minor units in `usd` at every layer: in the datastore, in every response body, in every intermediate computation and in the calculator. It is formatted for display once, at the edge. A cost of `$17.32` is `1732`, and no floating-point value ever holds a monetary amount.

Every response carries the standard security headers, including a strict transport policy and a content-type policy that refuses sniffing. Nothing the browser downloads carries a credential, an API key or an administrative token: the database address, the mail credentials and the payment platform's key and secret are read on the server and never appear in a document, a script, a template or a response body.

Cross-site request forgery is refused on both sides and not on either alone: every state-changing request carries an origin check that fails closed when the header is absent, and every form carries a token bound to the session. No state-changing action is ever reachable by a safe method, which matters here because an install control and an invitation link are exactly the shapes that get turned into a plain link.

Performance is a budget, not an aspiration. The hero is text, so the largest content paint is under two seconds at the median captured width on a mid-range handset over a mobile connection; interaction to next paint is under two hundred milliseconds; cumulative layout shift is under `0.05`; total blocking time is under two hundred milliseconds. The layout-shift budget is the tight one and it names its three risks: the download control resolves in the browser and rewrites its own label, the theme is applied before the first paint, and the drawn windows enter with a movement. Each is mitigated above. Only the first drawn window on a route renders eagerly; the rest render on approach, and any always-running loop pauses when its element leaves the viewport.

Every public route carries its own title and its own description and no two routes share either. A site map at `/sitemap.xml` lists every public route and a robots file at `/robots.txt` points at it. An unrouted address answers as not found and renders this product's own page, never a successful answer carrying the home document.

Validation is declared once per resource and runs on the server for every request regardless of what the browser already checked. A business-rule violation is rejected as a client error with a reason naming the field; it is never a server error and never a silent success. Asking about a workspace the caller does not belong to answers as not found so the workspace's existence is not confirmed; asking about something inside a workspace the caller does belong to, without the role for it, answers as denied. A refusal caused by a spend limit is a distinct answer from a refusal caused by a role, because the two have different remedies and the interface shows different messages.

The data volume the product must stay responsive at: fifteen models, seventeen catalogue entries, twenty-three release artifacts, four changelog entries, seven tiers, and a usage table of a few thousand events per workspace per period.

## Data model

Fourteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`users`** - `id`, `email` (unique, compared without regard to case), `password_hash`, `display_name`, `theme_preference` (one of `system`, `light`, `dark`, defaulting to `system`), `locale`, `created_at`. The address is the login identifier.

**`workspaces`** - `id`, `slug` (unique, kebab-case, minted from the name), `name`, `tier_code`, `seat_count`, `spend_limit_minor` (nullable, where null means no limit), `billing_external_key` (nullable until checkout), `created_at`.

**`memberships`** - `id`, `workspace_id`, `user_id`, `role` (`owner` or `member`), `state` (`invited`, `active` or `removed`), `seat_assigned`, `joined_at`, `removed_at`. One membership per workspace and user. A workspace always holds at least one membership whose role is `owner` and whose state is `active`; the operation that would leave none fails and changes nothing.

**`invitations`** - `id`, `workspace_id`, `email`, `role`, `token`, `state` (`pending`, `accepted`, `revoked` or `expired`), `expires_at`, `created_at`. One `pending` invitation per workspace and address at a time; a second invitation to the same address while one is pending re-sends the same token rather than creating a row.

**`plans`** - `code` (`hobby`, `individual`, `teams`, `enterprise`), `name`, `display_order`, `self_serve`.

**`tiers`** - `code`, `plan_code`, `name`, `order_in_plan`, `monthly_price_minor`, `yearly_price_minor`, `per_seat`, `purchasable`, `included_allowance_minor`. Seven rows, exactly as the pricing table above states them.

**`entitlements`** - `tier_code`, `capability`, `granted`, `limit_value`. One row per tier and capability. A capability granted at a lower `order_in_plan` within a plan is granted at every higher one, and a capability granted on a lower plan is granted on every higher plan; the state in which that does not hold is invalid and the product must refuse to start rather than serve it.

**`subscriptions`** - `id`, `subject_type` (`user` or `workspace`), `subject_id`, `tier_code`, `interval` (`monthly` or `yearly`), `state` (`active`, `past_due` or `canceled`), `seats`, `current_period_start`, `current_period_end`, `cancel_at_period_end`, `billing_external_key`, `created_at`. At most one row per subject is in state `active` or `past_due` at any instant. Two checkout requests racing for one subject must not both succeed: exactly one wins, the other is rejected as a conflict, and afterwards exactly one live subscription and exactly one billing account exist for that subject. The double-charge race is the one this product is most likely to lose.

**`models`** - `code`, `name`, `provider`, `benchmark_score_bp` (the score in hundredths of a percent, so `70.8%` is `7080`), `cost_per_task_minor` (nullable), `tokens_per_task`, `steps_per_task`, `series_index`, `self_reported`, `benchmark_version`. Fifteen rows. `series_index` is a stable ordering so a model keeps the same colour between page loads; it is never assigned by iteration order.

**`plugins`** - `id`, `kind` (`plugin` or `automation`), `slug`, `name`, `publisher`, `category`, `description`, `install_count`, `state` (`published` or `withdrawn`), `published_at`. One row per `kind` and `slug`. `install_count` is derived from `installations` on read rather than trusted as a stored counter that can drift.

**`installations`** - `id`, `subject_type` (`user` or `workspace`), `subject_id`, `plugin_id`, `installed_at`. One row per subject and plugin. A repeated install of the same plugin by the same subject adds no second row and changes no count.

**`release_artifacts`** - `id`, `version`, `os`, `arch`, `format`, `checksum`, `size_bytes`, `published_at`. One row per `version`, `os`, `arch` and `format`. Twenty-three rows: eight platform rows at `3.16` and at `3.17`, and seven at `3.18`.

**`changelog_entries`** - `id`, `slug`, `title`, `body`, `published_at`. Four rows, and the home route's band is a projection of the four most recent by `published_at`.

**`usage_events`** - `id`, `workspace_id`, `user_id`, `idempotency_key` (unique across the table), `model_code`, `surface`, `tasks`, `rated_cost_minor`, `occurred_at`, `recorded_at`, `billing_period`. Append-only. Replaying a request with the same `idempotency_key` adds no row, changes no total and answers with the original event; the same key with a different body is rejected as a conflict. `rated_cost_minor` is `tasks` multiplied by the model's `cost_per_task_minor`, computed in integer minor units. `billing_period` is derived from `occurred_at`, never from `recorded_at`.

**`allowances`** - `subject_type`, `subject_id`, `billing_period`, `included_minor`, `consumed_minor`, `pooled`. One row per subject and period. `consumed_minor` reconciles exactly with the sum of `rated_cost_minor` over that subject's events in that period: a reconciliation that disagrees is a fault, and the number shown to the customer is the one the events support.

**`leads`** - `id`, `email`, `topic`, `source`, `country`, `referring_route`, `suspected_automated`, `delivery_state`, `created_at`.

Every row carrying `workspace_id` is readable only by an account holding an `active` membership in that workspace. This must hold for a direct request with a valid token belonging to another workspace, not only for the pages that render lists.

**Seed data.**

Users: `owner@example.com` as `Devan Ashworth`, `member@example.com` as `Priya Raghunathan`, `owner2@example.com` as `Marguerite Sandoval`, all with the password above.

Workspaces: `Aurora Data` with slug `aurora-data`, tier `standard`, two seats, spend limit `2500`, billing external key `marlin-ws-aurora-data`, an `active` subscription on `standard` at `monthly`, with `owner@example.com` as its `owner` and `member@example.com` as an `active` `member`. `Northlight` with slug `northlight`, tier `hobby`, one seat, no spend limit, no billing external key and no subscription, with `owner2@example.com` as its `owner`.

Usage: `Aurora Data` carries three events, `seed-usage-aurora-1` (`meridian-4`, surface `desktop`, `30` tasks, `7020`), `seed-usage-aurora-2` (`meridian-4-mini`, surface `cloud`, `10` tasks, `1280`) and `seed-usage-aurora-3` (`corvus-3`, surface `review`, `1` task, `569`), summing to `8869` consumed against `8000` included, which is `869` of overage. `Northlight` carries one event, `seed-usage-northlight-1` (`meridian-4-mini`, surface `terminal`, `3` tasks, `384`), against `500` included and no overage.

Catalogue: the sixteen published entries above plus `pallas-connect`, named `Pallas Connect`, in state `withdrawn`.

Registry: the fifteen models above, at benchmark version `MarlinBench 3.2`.

Releases: twenty-three artifacts as described, with `9f2a4c6e8b0d1357a9c2e4f60821b3d5c7e9f0a2b4d6e8f0a1c3e5d7b9f1a3c5` as the checksum of the `3.18` `macos` `arm64` `dmg` artifact.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One product, one origin. No second front end, no separate documentation application, no separate help centre.
- Not built: the agent execution platform and the run list, the hosted code product, the integration and trigger registry, inbound and outbound webhooks, the publishing and moderation pipeline for a catalogue entry, the documentation site, the help centre, the blog, the careers listing, the community, students, workshops, brand and future routes, and the newsletter.
- No payment between a publisher and an installer, no basket, no checkout and no payout in the marketplace. Every entry is free.
- No external identity provider, no single sign-on, no directory synchronisation, no second factor.
- No refunds, no payment methods, no chargebacks: the payment platform in this environment does not expose them.
- No invoice or purchase-order billing path, and no self-serve purchase of the enterprise plan.
- No external network calls at runtime beyond the three named backing services.
- No native application, no handset application, no desktop installer actually produced: the download route resolves to artifact records, it does not build software.
- The calculator submits nothing and stores nothing. Analytics may record that it was used and which view was selected; they may never record the entered spend.
- The product stays responsive at the data volume named in the technical requirements.

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

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `display_name` | `token`, `user` |
| `POST /api/auth/signin` | `email`, `password` | `token`, `user` |
| `GET /api/me` | bearer | `user`, `memberships` |
| `GET /api/models` | none | a top-level JSON array of models, each with `code`, `name`, `provider`, `benchmark_score_bp`, `cost_per_task_minor`, `tokens_per_task`, `steps_per_task`, `series_index`, `self_reported`, `benchmark_version` |
| `GET /api/plans` | none | plans, their tiers and their entitlements |
| `GET /api/plugins` | `q`, `kind`, `category`, `sort`, `page`, `per_page` | `data`, `page` with `number`, `size`, `total_items`, `total_pages`, and `links` |
| `GET /api/plugins/{kind}/{slug}` | none | one catalogue entry |
| `POST /api/plugins/{kind}/{slug}/install` | bearer | the installation and the resulting `install_count` |
| `GET /api/releases` | none | a top-level JSON array of artifacts |
| `GET /api/releases/resolve` | `os`, `arch`, `format`, `channel` | one artifact with `version`, `checksum`, `size_bytes`, `published_at`, and whether it is the latest |
| `GET /api/changelog` | none | a top-level JSON array of entries, newest first |
| `POST /api/workspaces` | bearer, `name` | the workspace and the caller's owner membership |
| `GET /api/workspaces/{slug}` | bearer | the workspace, its tier, its seats and its subscription |
| `GET /api/workspaces/{slug}/members` | bearer | a top-level JSON array of memberships and pending invitations |
| `POST /api/workspaces/{slug}/invitations` | bearer, `email`, `role` | the pending invitation |
| `DELETE /api/workspaces/{slug}/invitations/{id}` | bearer | the revoked invitation |
| `DELETE /api/workspaces/{slug}/members/{id}` | bearer | the removed membership and the new seat count |
| `POST /api/invitations/accept` | bearer, `token` | the new membership and the new seat count |
| `GET /api/workspaces/{slug}/usage` | bearer | `included_minor`, `consumed_minor`, `overage_minor` and the breakdown |
| `POST /api/workspaces/{slug}/usage-events` | bearer, `idempotency_key`, `model_code`, `surface`, `tasks` | the event with its `rated_cost_minor` |
| `PUT /api/workspaces/{slug}/spend-limit` | bearer, `limit_minor` | the workspace with its new limit |
| `POST /api/billing/checkout` | bearer, `tier_code`, `interval` | the subscription and its `billing_external_key` |
| `GET /api/billing/subscription` | bearer | tier, interval, seats, period, state |
| `POST /api/leads` | `email`, `topic`, `source` | the stored enquiry |
| `GET /api/health` | none | `200` |

Bearer authentication is required on everything except sign-up, sign-in, health and the public read endpoints. A list endpoint returns a top-level JSON array unless the table above states an envelope. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success.

**No mocks.** The billing account is the payment platform's record, not a row this app wrote to itself: an in-memory `accounts` map, a hardcoded `{"status":"active"}` response the app returns to itself, or a local table standing in for `killbill` are each a contract violation. The invitation is the message that left over SMTP, not a row reading `sent`: a logged line, a queued job that never connects, or a template rendered into a variable are each a contract violation. The named provider is the fact - the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor can compare fifteen models on the leaderboard, price a shift between two of them in the calculator, resolve a download for their own platform with its checksum shown, and install a plugin once they have signed up. An owner can subscribe a workspace to a paid tier and see the same billing account in the payment platform, and submitting that subscription twice leaves exactly one. An owner can invite a colleague, the invited address receives one message and no other address does, and accepting it consumes exactly one seat. A member of one workspace can read nothing belonging to another.
