# Remixable Timeline Editor

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, sign up, remix a template into a
project, tune a block on its timeline, export a version, and send that version to a reviewer who
watches it and approves it, without hitting an error page. A person holding a share link whose
download permission is off must NOT be able to download the file by any means, including a direct
request for the media route, and a reviewer must NOT be able to see anything in the workspace except
the version sent to them. Every uploaded or exported file must live in the object store at its
scheme's key; a copy on the app's own disk does not count.

## Overview

Ferment is a browser video editor for brand and agency creative teams, sold by public signup on
five published plans. Its one idea is that the timeline holds tools, not only footage: a block is a
parameterised motion, type, 3D or shader effect that a member drops on the timeline and tunes with
dials, sliders, prompts or code, and a block a member saves belongs to the team, so nobody rebuilds
the same lower third twice. Each workspace holds its own library of saved blocks, templates it has
remixed, brand kits and projects. What makes it distinctive is that tools, not only media, live on
the timeline, that there are three ways in (remix, describe, code), and that every rationed
resource a plan publishes is enforced rather than merely advertised.

The product is two surfaces on one origin. The marketing site explains the product, publishes the
plans and the rationed resources each plan includes, and moves a visitor into signup. The
application is where a member remixes a template, builds a timeline, exports a version against the
plan's allowance, shares it, and asks named reviewers to approve it.

It deliberately is not a stock media library, a captioning or speech service, a payment processor, a
real-time co-editing service or an organisation-governance console. Enterprise exists as a pricing
card and a sales conversation only.

The genuinely hard part is that almost everything is rationed and almost everything leaves the team:
two members spending the last unit of one allowance in the same second must not both succeed, a
retried export must cost once, and a link, a comment or an approval must keep meaning exactly the
version it was attached to after the project moves on.

## User roles

Two account roles. Owning a workspace is a relationship between a member and a workspace, not a
third role.

| Role | Can do | Cannot do |
|---|---|---|
| `member` | Sign up; belong to one or more workspaces; browse the library; remix, describe and code; build timelines; save blocks and brand kits; upload media; create versions, exports and shares; request approval; comment. The member who owns a workspace also changes its plan, invites and removes members, and reads its charges and share view logs | **Cannot** read or change any workspace they do not belong to, **cannot** place another workspace's saved block, and a member who does not own the workspace **cannot** change its plan, invite, remove members or read its charges |
| `reviewer` | Accept a review invitation; see the versions whose approval was requested of them; watch them; comment on them; record one decision per request | **Cannot** open any workspace, project, library, brand kit, asset, member list or billing route, **cannot** occupy a seat, and **cannot** see a version nobody asked them to review |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `reviewer` session to any `member`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged. The same holds for a member of one workspace calling another workspace's endpoints, and
for a non-owner calling an owner-only endpoint.

Signup is open. Every account created by `/register` is a `member` and owns a new workspace on the
Free plan. A `reviewer` account is created only by accepting a review invitation, and no request
body, form field or header can choose or change an account's role.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Display name | Seeded state |
|---|---|---|---|
| `member@example.com` | member | Nadia Okafor | owns `Juniper Goods` (Pro) |
| `member2@example.com` | member | Theo Brandt | belongs to `Juniper Goods`, does not own it |
| `member3@example.com` | member | Ines Duarte | owns `Solo Sketchbook` (Free) |
| `member4@example.com` | member | Omar Haddad | owns `Basic Bench` (Basic) |
| `reviewer@example.com` | reviewer | Priya Nair | asked to approve version 2 of `Denim Drop remix`; approved its version 1; a named recipient of one share |
| `reviewer2@example.com` | reviewer | Lucas Meyer | nothing has been sent to this account |

## Core features

### Accounts, sessions and workspaces

Ferment runs its own sign-in: a member proves who they are with an email address and a password, and every later call to the API carries the bearer token that sign-in handed back. Only a slow salted hash of each password is kept, and no response ever includes a password or its hash. A signed-in browser is also recognised when a page is rendered, so the header shows
the signed-in state on first paint.

1. `POST /api/auth/signup` with `email`, `password` and `display_name` creates a `member`, creates a
   workspace named by the optional `workspace_name` (or `<display_name>'s workspace` when it is
   absent) on the Free plan with the new member as its owner, and returns an `access_token`. A
   second signup with an address already in use is rejected as invalid and creates nothing. A
   password shorter than ten characters is rejected as invalid.
2. `POST /api/auth/login` with a seeded email and `deku-demo-pw-2026` returns an `access_token`. A wrong password is denied and returns no token.
3. Every guarded endpoint turns away a call that arrives without a token, or with a token Ferment never
   issued, and whatever that call tried to change stays as it was.
4. A signup body that names a `role` still creates a `member`.
5. `GET /api/workspaces` lists only the workspaces the caller belongs to, each with its `id`, `name`,
   `plan_key` and the caller's `relation` to it, `owner` or `member`. A member may belong to several.
6. Everything a member creates (saved blocks, brand kits, projects, assets, versions, exports,
   shares, favourites) belongs to the workspace, not to the person, and stays when that member is
   removed.
7. `PATCH /api/me` stores the member's `interface_scale`, which is one of `100`, `115`, `130` or
   `150` (per cent). Any other value is rejected as invalid and the stored value is unchanged. The setting belongs to the account, so it is back after signing in
   again anywhere.

### Plans and the pricing page

Plans are stored records, and the pricing page, the comparison table, the usage panel and every
enforcement check read the same stored values. No price, limit or saving is typed into a page.

| Key | Name | Monthly, cents | Annual, cents per month | Unit | Member cap | Positioning |
|---|---|---|---|---|---|---|
| `free` | Free | `0` | `0` | Single User | 1 | `Start making videos in minutes for free` |
| `basic` | Basic | `2500` | `1800` | Single User | 1 | `Unlock HD watermark-free exports` |
| `pro` | Pro | `3800` | `3000` | Per Member | 10 | `Team workspaces, brand kits and more` |
| `business` | Business | `7000` | `5900` | Per Member | no cap | `Optimized for larger teams` |
| `enterprise` | Enterprise | Custom | Custom | contact | none | `For businesses that need scale` |

1. Prices are integer cents in `usd`. `2500` is `$25`, not `25`. Annual billing charges twelve times
   the annual per-month figure once per year.
2. `GET /api/plans` returns every plan in the order above with its `quotas`, a list of objects
   carrying `meter`, `limit` and `period`, its `features`, a list of objects carrying `label`, `value`
   and `status`, and its `annual_saving_percent`, computed
   as `(1 - annual / monthly) x 100` rounded to the nearest whole number, halves rounding up: `28`
   for Basic, `21` for Pro, `16` for Business, and no saving for Free or Enterprise. A hard-coded
   percentage is a defect.
3. `/pricing` opens with `Unlimit your creativity.` and
   `Get everything you need to begin, then add more power, flexibility, and control as you grow.`
   Its billing toggle offers `Monthly` and `Annually` and carries the badge `Save up to 28%`, whose
   number is the largest saving across the plans. In annual mode every paid card shows its own
   saving, `Save 28%`, `Save 21%` and `Save 16%`, and its price changes to the annual per-month
   figure.
4. Pro is marked `Most popular`. Each card's call to action is `Get started for Free`,
   `Choose Basic`, `Choose Pro`, `Choose Business` or `Contact Sales`. Each paid card lists
   `Everything in <previous plan>, plus:` and then only what it adds, because the plans are
   cumulative.
5. Pro and Business are billed per member; the Pro card states `Max 10 team members`.
6. Enterprise is a separate tier and the tier boundary is deliberate: it is sold only through
   `Contact Sales`, which leads to `/contact` with the sales audience
   chosen. It lists `Unlimited Cloud Storage`, `Unlimited Saved Components`, `Ultra-HD 4K Exports`,
   `Unlimited Auto-Captioning` and `Org Controls, Security & SSO` as sales conversation topics; none
   of them is built.
7. The comparison table below the cards has these rows, read from the same stored plan features:
   `Cloud storage`, `Export Quality`, `AI Auto-captioning`, `AI Text to Speech`,
   `AI background removal`, `Multiple brand kits`, `Custom fonts`, `Save custom components`,
   `Save designs as custom templates`, `Export as GIF (great for emails!)`,
   `Export as JPEG and PNG`, `Premium templates`, `Flexible components`,
   `Text presets and templates`, `Free stock photos`, `Free stock video`, `Free stock audio` and
   `Free fonts`. A card and the table can never disagree about a number, because both read one
   stored value.
8. A plan feature has a `status` of `available` or `coming_soon`. In this product `AI Auto-captioning`,
   `AI Text to Speech`, `AI background removal`, `Save designs as custom templates`,
   `Free stock photos`, `Free stock video`, `Free stock audio`, `Free fonts` and Business's 4K export
   are `coming_soon`: they are shown with a visible `Coming soon` marker, nothing in the product
   performs them, and no allowance is ever consumed by them.

### Quotas

Seven stored limits per plan. Three are monthly allowances and four are ceilings. A limit of none
means unlimited; `0` means not included.

| Meter | Kind | Free | Basic | Pro | Business | Enterprise |
|---|---|---|---|---|---|---|
| `storage_bytes` | ceiling | 2 GB | 5 GB | 20 GB | 50 GB | none |
| `project_variations` | monthly | `0` | `20` | `250` | `2500` | `0` |
| `caption_minutes` | monthly | `30` | `60` | `120` | `600` | none |
| `speech_characters` | monthly | `0` | `0` | `5000` | `20000` | `0` |
| `brand_kits` | ceiling | `0` | `0` | `5` | `10` | `0` |
| `saved_blocks` | ceiling | `5` | `25` | `50` | `100` | none |
| `members` | ceiling | `1` | `1` | `10` | none | none |

A gigabyte here is `1073741824` bytes. Export frame ceilings: Free up to 1280 by 720, Basic up to
1920 by 1080, Pro and Business up to 2000 on each side, and the shorter side of a frame is held to
the smaller number. Free exports carry a watermark and no other plan's do. Premium templates are
included from Basic upward. Custom fonts in brand kits are included from Pro upward.

1. A monthly allowance is counted per usage window. A window starts on the subscription's anchor day
   and lasts one calendar month, whether the plan is billed monthly or annually, and use in an earlier window never counts
   against the current one.
2. `GET /api/workspaces/{ws}/usage` returns one row per meter with `meter`, `used`, `limit`,
   `period`, `window_start` and `window_end`. `used` for `storage_bytes` is the sum of the bytes of
   the workspace's stored assets and ready exports; for `members` it is members plus pending
   invitations.
3. Every unit passes through the quota ledger the same way: it is reserved, then settled or
   released, and the reset of a monthly allowance is period-anchored rather than calendar-anchored.
   Concurrent consumers of one workspace's balance end in the same state as if they had arrived one
   after another, so consumption is serialisable in effect.
   **Two members of one workspace spending the last unit of any allowance or ceiling in the same
   moment must not both succeed.** Exactly one is accepted, the other is refused, and `used` never
   exceeds `limit`. This holds for project variations, saved blocks, brand kits and members alike.
4. A refusal is informative: it is rejected as a client error carrying `error` = `quota_exceeded`,
   the `meter`, the `limit`, the `plan` and a `message`. The message is exactly one of these:
   - a spent monthly allowance:
     `You've used all your project variations for this month. Basic includes 20.`, following the
     pattern `You've used all your <meter> for this month. <plan> includes <limit>.`
   - a full ceiling:
     `Free includes 5 saved blocks. Remove one or upgrade to add more.`, following the pattern
     `<plan> includes <limit> <meter>. Remove one or upgrade to add more.`
   - a meter the plan does not include:
     `Brand kits are not included in Basic. Upgrade to Pro to use them.`, following the pattern
     `<Meter> are not included in <plan>. Upgrade to <first plan that includes it> to use them.`
   
   - the Pro seat cap: `Pro includes up to 10 members. Upgrade to Business to add more.`
   - an invitation on a single-user plan:
     `Free is for one person. Upgrade to Pro to invite your team.` (or `Basic is for one person.`
     with the same second sentence).
5. Ceilings are enforced when something new is written. A workspace moved to a smaller plan keeps
   everything it already has; it cannot add another of that thing until it is back under the
   ceiling.

### Seats, plan changes and charges

There is no payment provider in this environment. Billing is the app's own record of what each
workspace owes: a subscription and a list of charge lines, all in integer cents, `usd`.

1. `GET /api/workspaces/{ws}/subscription` returns `plan_key`, `billing_period` (`monthly` or
   `annual`), `seats`, `seats_used`, `current_period_start` and `current_period_end`. A monthly period ends one calendar month after it starts and an annual period one calendar year after.
   Period boundaries are UTC calendar dates, sent as timestamps at midnight ending in `Z`.
2. Only the owner may call `POST /api/workspaces/{ws}/subscription` with `plan_key` and
   `billing_period`. A change starts a new period on the current UTC date and writes one
   `plan_change` charge of `seats x price for the period`, where the price is the monthly figure,
   or twelve times the annual per-month figure. Choosing `enterprise` is refused with
   `Enterprise is arranged through Contact Sales.`
3. **Moving from a single-user plan to Pro or Business converts the subscription into seats**: the
   new subscription's `seats` equals the workspace's current member count. On Free and Basic,
   `seats` is always `1`. Moving a workspace with more than one member onto Free or Basic is refused
   with `Free is for one person. Remove the other members before switching.` (or the Basic
   equivalent) and nothing changes.
4. The owner invites with `POST /api/workspaces/{ws}/invitations` and `email`. A pending invitation
   occupies a seat against the `members` ceiling until it is accepted or revoked. On Pro, the
   invitation that would make eleven is refused with the seat-cap message and nothing is stored.
5. `POST /api/invitations/{token}/accept`, called by a signed-in member whose email matches the
   invitation, adds that member to the workspace and increases `seats` by one. On Pro and Business
   the join writes one `seat_added` charge, with `seats` 1, prorated to the rest of the current period:

   `amount_cents = round_half_up(price_for_period x remaining_days / period_days)`

   where `period_days` counts the days from `current_period_start` to `current_period_end`, and
   `remaining_days` counts the days from the UTC date of the join to `current_period_end`, the join
   day included and the end day excluded.

   | Plan and period | Period | Joins on | Remaining / total days | Charge |
   |---|---|---|---|---|
   | Pro, monthly | 2026-09-01 to 2026-10-01 | 2026-09-16 | 15 / 30 | `1900` |
   | Pro, monthly | 2026-09-01 to 2026-10-01 | 2026-09-21 | 10 / 30 | `1267` |
   | Pro, annual | 2026-01-10 to 2027-01-10 | 2026-09-16 | 116 / 365 | `11441` |

6. The owner removes a member with `DELETE /api/workspaces/{ws}/members/{account_id}`. The member
   loses access at once, their work stays in the workspace, `seats` drops by one, and nothing is
   refunded. The owner cannot be removed. Revoking a pending invitation with
   `DELETE /api/workspaces/{ws}/invitations/{id}` releases its seat.
7. `GET /api/workspaces/{ws}/charges`, owner only, lists charge lines newest first with `kind`
   (`plan_change` or `seat_added`), `plan_key`, `seats`, `amount_cents`, `currency`, `period_start`,
   `period_end` and `created_at`.

### The library: blocks, templates, creators, favourites and brand kits

A block declares its parameters and their types, and every control panel is generated from that
declaration, so a block the app has never seen still produces a usable panel. Four control kinds
exist: `dial` (a whole number of degrees from 0 to 359), `slider` (a whole number between its own
`min` and `max`), `prompt` (text up to its own `max_length`) and `code` (text up to 5000
characters).

The library blocks, available to every workspace:

| Block | Category | Parameters (key, control, range, default) |
|---|---|---|
| `Inflate` | Text | `text` prompt up to 40, `Inflate`; `puff` slider 0 to 100, 40; `angle` dial, 0 |
| `Glow` | Text | `text` prompt up to 40, `Glow`; `intensity` slider 0 to 100, 60; `hue` dial, 45 |
| `Focus` | Text | `text` prompt up to 40, `Focus`; `blur` slider 0 to 40, 12 |
| `Halftone` | Text | `text` prompt up to 40, `Halftone`; `dot_size` slider 2 to 24, 8; `angle` dial, 45 |
| `Carousel` | Motion | `caption` prompt up to 60, `New season`; `speed` slider 1 to 10, 4; `tilt` dial, 15 |
| `Ticker` | Motion | `message` prompt up to 120, `Free shipping this week`; `speed` slider 1 to 20, 6 |
| `Orbit Card` | 3D | `title` prompt up to 40, `Orbit`; `orbit` dial, 30; `depth` slider 0 to 100, 50 |
| `Ripple` | Shader | `amplitude` slider 0 to 50, 10; `frequency` slider 1 to 20, 5; `expression` code, `sin(t)` |

1. `GET /api/blocks` lists library blocks, filterable by `category` and by `q` (a case-insensitive
   match on the name), paged with `limit` and `offset`, so the library never has to load every block at once and stays
   smooth when it holds thousands. `GET /api/blocks/{id}` returns one block with its
   `parameter_schema`.
2. Eight templates are published, each addressable by a stable `uuid` at `/templates/<uuid>`, each in
   one of four categories, each credited to a creator:

   | Template | uuid | Category | Creator | Premium |
   |---|---|---|---|---|
   | `Denim Drop` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b01` | `Apparel` | `kiln-collective` | no |
   | `Serum Glow Launch` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b02` | `Beauty` | `halfstep-motion` | no |
   | `Cold Brew Morning` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b03` | `Food & Beverage` | `oriel-park` | no |
   | `Lip Tint Swatches` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b04` | `Beauty` | `kiln-collective` | no |
   | `Night Cream Ritual` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b05` | `Beauty` | `halfstep-motion` | yes |
   | `Feature Reveal` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b06` | `Software / Apps` | `oriel-park` | yes |
   | `Trail Jacket Story` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b07` | `Apparel` | `kiln-collective` | no |
   | `Smoothie Stack` | `5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b08` | `Food & Beverage` | `halfstep-motion` | no |

   `GET /api/templates` filters on `category`; `GET /api/templates/{uuid}` returns one template
   with its `timeline`. An unknown uuid answers not found.
3. Three credited creators exist: `Kiln Collective` at `/creators/kiln-collective`,
   `Halfstep Motion` at `/creators/halfstep-motion` and `Oriel Park` at `/creators/oriel-park`.
   `GET /api/creators/{slug}` returns the creator's `display_name`, `credit` and the templates
   credited to them.
4. A member favourites a library block or a template with `POST /api/workspaces/{ws}/favorites`
   carrying `block_id` or `template_uuid`, never both. Favouriting the same thing twice leaves one favourite.
5. A brand kit has a `name`, one to eight `colours` written as `#RRGGBB` strings, and one to four
   `fonts` named by family. `POST /api/workspaces/{ws}/brand-kits` is metered by the `brand_kits`
   ceiling; a kit with no colours, more than eight, a colour that is not `#RRGGBB`, or a font list outside one to four names is rejected as invalid and writes nothing.

### Remix, Describe and Code

Three ways into a project, each specified in full.

1. **Remix.** `POST /api/workspaces/{ws}/templates/{uuid}/remix` creates a project in that workspace
   named `<template name> remix`, with the template's canvas, frame rate, duration and timeline,
   every block instance keeping its parameter values, `remixed_from` set to the template's uuid,
   and `revision` 1. Remixing a premium template from a Free workspace is refused with
   `Premium templates are not included in Free. Upgrade to Basic to use them.` and creates nothing.
2. **Describe.** `POST /api/workspaces/{ws}/projects/{id}/describe` with a `prompt` creates a new
   project named `<source project name> - described <n>`, where `n` counts that project's
   described variations from 1. A library block matches when its whole name appears in the prompt as whole words, ignoring case,
   and matched blocks are placed in the order their names first appear; each matched block becomes one
   track with one instance starting at 0 and spanning the whole duration, placed at the block's
   current version, and every `prompt`-kind parameter of that instance is set
   to the whole prompt text, cut to the parameter's `max_length`. Each successful Describe consumes
   one `project_variations` unit. A prompt that matches no block is rejected as invalid with
   `Describe matched no blocks. Try naming an effect such as Glow or Halftone.` and consumes
   nothing. Describing from a Free workspace is refused with the not-included message.
3. **Code.** A member saves a custom block with a `parameter_schema` and a `source`. The schema is
   validated: every parameter has a unique lowercase `key`, a `label`, a `control` from the four
   kinds, a `slider` has `min` below `max` and a default between them, a `dial` default lies from 0
   to 359, and a `prompt` has a `max_length` from 1 to 500. An invalid schema is rejected as invalid,
   names the parameter that failed, and writes nothing. `source` is stored and returned as text and
   is never executed by the server.
4. A custom block's source runs only in the browser, isolated from the page: it cannot reach the
   network, the member's session, the page's stored data or any other block, and each frame it
   draws has a time budget. A block that exceeds its budget is paused, its area shows
   `This block stopped responding and was paused.`, playback and editing carry on, and nothing in
   the project is lost.

### Projects and the timeline

1. `POST /api/workspaces/{ws}/projects` takes `name`, `canvas_width` and `canvas_height` (each 16 to
   4096), `fps` (one of 24, 25, 30, 60) and `duration_ms` (1000 to 600000), and creates the project
   at `revision` 1 with an empty timeline.
2. A timeline is a list of `tracks`; each track has an `id`, a free `label` and a list of `items`.
   Every item has an `id`, a `type` of `clip` or `block`, a `start_ms` and a `duration_ms`. A clip
   carries an `asset_id` from the same workspace. A block item carries a `block_id`, the
   `block_version` it was placed with and its own `params`. A track holds clips and block items side
   by side, and the same block placed twice keeps two independent sets of parameter values.
3. `PUT /api/workspaces/{ws}/projects/{id}/timeline` takes `base_revision` and `timeline`. When
   `base_revision` equals the stored revision, the timeline is stored and `revision` goes up by one.
   **Two saves made from the same revision must not both land**: exactly one is accepted, the other
   is rejected as a conflict carrying the stored `revision`, and the stored timeline is the accepted
   one. 
4. A timeline is rejected as invalid, and nothing is stored, when an item starts before zero, runs
   past the project's duration, names an asset from another workspace, names a saved block from
   another workspace, or carries a parameter value outside its declared range or kind.
5. Every edit in the editor, whether trimming a clip, moving an item, turning one dial on one
   instance or adding a track, is one entry in a single undo history that reverses edits in order
   and redoes them in order. `Undo` and `Redo` are keyboard reachable.
6. Playback continues while blocks render, and a slow block never freezes the editor.

### Saved blocks

1. `POST /api/workspaces/{ws}/blocks` saves a custom block at `version` 1 and is metered by the
   `saved_blocks` ceiling, which counts saved blocks, not versions.
2. `PUT /api/workspaces/{ws}/blocks/{id}` stores the edit as the next `version`; earlier versions
   are never changed or removed. A block item already on a timeline keeps the version it was placed
   with, so editing a saved block used in ten projects changes none of them; the editor marks such
   an item with `A newer version of this block exists.` and an action that moves it to the newest
   version.
3. `DELETE /api/workspaces/{ws}/blocks/{id}` removes the block from the workspace library and frees
   its place under the ceiling; items already placed keep rendering from the version they hold.
4. A saved block is visible to every member of its workspace and to nobody else.

### Media and the object store

1. `POST /api/workspaces/{ws}/assets` takes a multipart `file` of type `png`, `jpg`, `gif`, `mp4`, `webm`, `mp3` or `wav`. **The bytes are written to the object store at
   `STORAGE_ENDPOINT` in the bucket named by `STORAGE_BUCKET`, and nowhere else.** A file on the
   app's own filesystem, a blob in a database column or a placeholder shipped with the app is a
   failure of this rule however the page looks.
2. The asset key is `assets/{workspace_id}/{sha256_of_bytes}.{ext}`, for example
   `assets/7/3b1f6c0d9a2e48f7b5c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f60718293a4b5c6d.png`. Uploading the same
   bytes to the same workspace twice leaves one object and one asset row.
3. An unsupported type is rejected as invalid and writes no object. An upload is a new write, so the
   `storage_bytes` ceiling applies to it like any other ceiling.
4. `GET /api/workspaces/{ws}/assets/{id}/content` streams the bytes to members of that workspace
   only. The bucket is private: no object is ever readable at the object store's own address
   without its credentials, and the app never hands a browser a signed object-store address.

### Versions and exports

1. `POST /api/workspaces/{ws}/projects/{id}/versions` freezes the project's current timeline as the
   next version, numbered from 1 within the project, carrying the `project_revision` it froze.
   Versions are never edited. `GET` on the same path lists them newest first.
2. `POST /api/workspaces/{ws}/versions/{vid}/exports` takes `format` (`png`, `jpg`, `gif` or `mp4`),
   `width`, `height`, `fps` (up to 60) and a `request_key`, and returns an export job with `status`
   `rendering`, `progress` 0, `watermarked` (true exactly when the plan is Free) and `is_variation`
   (true when the requested width and height differ from the project's canvas). A frame beyond the
   plan's export ceiling is refused and creates no job.
3. **A variation reserves one `project_variations` unit when its job is created.** The reservation
   is settled when the job becomes `ready` and released when it becomes `failed`, so a failed
   export costs nothing, and a job that is still rendering never lets the window's total pass its
   allowance. 
4. **A request repeated with the same `request_key` in the same workspace returns the same job and
   reserves nothing more**, including when both requests arrive in the same moment.
5. The browser renders the frames from the version's own timeline and uploads the finished file with `PUT /api/workspaces/{ws}/exports/{eid}/file`, whose request body is the
   file's raw bytes. The server accepts it only if its first bytes
   match the format (a PNG signature, a JPEG start marker, `GIF87a` or `GIF89a`, or an `ftyp` box at
   byte 4 for `mp4`) and, for `png`, `jpg` and `gif`, the width and height its own header declares
   equal the requested ones. An accepted file is written to
   `exports/{workspace_id}/{export_id}.{format}`, for example `exports/1/42.png`, the job becomes
   `ready` and records `object_key` and `byte_size`. A rejected file makes the job `failed` with a
   `failure_reason`, releases the reservation and writes no object. A second upload to a job that is
   already `ready` is refused, and the stored object and the usage are unchanged.
6. `PATCH /api/workspaces/{ws}/exports/{eid}` records `progress` from 0 to 100; progress never goes
   down. `POST /api/workspaces/{ws}/exports/{eid}/fail` marks the job `failed`. A job that has been `rendering` for more than 30 minutes is `failed` the next time it is read, and its
   reservation is released; the same check runs before any usage figure or new reservation is computed.
7. `GET /api/workspaces/{ws}/exports/{eid}` returns `status`, `progress`, `queue_position` (how many
   of the workspace's rendering jobs were created before it, plus one), `watermarked`,
   `is_variation`, `object_key` and `failure_reason`. Progress, queue position and the outcome survive a reload.
8. While a job renders, the version page and the job's own `message` read
   `Rendering. We'll let you know when it's ready.`; once it has failed, both read
   `That export didn't finish. We haven't counted it against your quota.`
   `GET /api/workspaces/{ws}/exports/{eid}/file` streams a ready file to workspace members only.

### Shares

1. `POST /api/workspaces/{ws}/versions/{vid}/shares` takes optional `expires_at`, optional
   `passphrase` (8 to 64 characters), `allow_download`, `allow_comments` and optional `recipients`
   (a list of emails), and returns the share's `id`, a 16-character `token` of letters and digits,
   its `url` `/s/<token>` and a `message`: `Anyone with this link can view this version.`, or
   `Only the people you named can view this version.` when recipients are set. A version with no
   ready export cannot be shared: the request is refused with `Export this version before sharing it.`
2. A share always shows the version it was created for, never the project's current timeline. When
   the project has a newer version, the share page says
   `A newer version exists. You're viewing the version you were sent.` The project's
   `superseded_shares` setting, `open` by default, can be set to `closed`, after which a share of any
   version other than the newest answers `This version has been replaced. Ask the sender for the latest link.`
   and serves no media.
3. A share whose `expires_at` has passed, or which the owner revoked with
   `DELETE /api/workspaces/{ws}/shares/{sid}`, answers `This link has expired. Ask the sender for a new one.`
   on its page, is rejected as a client error on every share endpoint, and serves no media.
4. A share with a passphrase serves nothing until `POST /api/shares/{token}/unlock` receives the
   right `passphrase` and returns an `access_token`, which the media and comment endpoints accept as a bearer token or as an `access` query value. A wrong passphrase is
   denied. After five wrong attempts on one share within fifteen minutes, every attempt on it is
   refused for fifteen minutes, the right passphrase included.
5. A share with `recipients` is served only to a signed-in account whose email is on the list; any
   other caller is denied, whether or not they hold the link.
6. `GET /api/shares/{token}/stream` serves the version's ready file inline to anyone the rules above
   admit. **`GET /api/shares/{token}/download` serves it as an attachment only when `allow_download`
   is true, and is refused whenever it is false, whatever else the caller holds.** Hiding the
   download control is not enough; the media route itself refuses.
7. **Each view of a share page is recorded** with its `route`, the viewer's email when signed in,
   and `viewed_at`. The workspace owner reads the page view log with
   `GET /api/workspaces/{ws}/shares/{sid}/views`; nobody else can.

### Timecoded comments

1. A comment is left at a moment, `at_ms`, on a version, through
   `POST /api/workspaces/{ws}/versions/{vid}/comments` by a workspace member or through
   `POST /api/shares/{token}/comments` by an admitted viewer when `allow_comments` is true. When
   `allow_comments` is false the share comment endpoint refuses and stores nothing.
2. A comment is anchored to the first item, in track order, whose span contains `at_ms`, and
   remembers its offset into that item. A moment with no item under it is `unanchored`.
3. `GET /api/workspaces/{ws}/versions/{vid}/comments` returns the comments left on that version and
   on every earlier version of the same project, each with a `state` resolved against this version:
   `anchored`, with `at_ms` recomputed as the anchor item's start in this version plus the offset,
   when the item still exists; `orphaned`, with `at_ms` empty and the note
   `The moment this comment referred to has been edited out.`, when it does not; or `unanchored`,
   keeping its original `at_ms`. A comment never silently points at a different moment: comments keep referential integrity when
   the timeline is mutated, and never re-point at the wrong frame.

### Approval and reviewers

1. `POST /api/workspaces/{ws}/versions/{vid}/approval-requests` takes one to ten `reviewer_emails`.
   Each address gets one request in state `pending`; an address with no account also gets a review
   invitation it accepts at `/review/invite/<token>`, and that request's `invite_url` carries the link
   for the requester to pass on. Asking the same reviewer about the same
   version again changes nothing. The response carries `approval_state`, `waiting_on` and a
   `message`: `Waiting on 2 reviewers.`, or `Waiting on 1 reviewer.` for one. A version with no
   ready export cannot be sent for approval.
2. `POST /api/review-invites/{token}/accept` with a `password` and `display_name` creates a
   `reviewer` account for the invited email and returns an `access_token`. A reviewer occupies no
   seat: `seats` and `seats_used` never change because of one.
3. `GET /api/reviews` lists only the requests addressed to the caller's email. A reviewer can open,
   stream and comment on those versions and nothing else; every workspace endpoint denies them. The
   reviewer's pages carry `You can see this version only.`
4. `POST /api/reviews/{rid}/decision` with `decision` `approved` or `changes_requested` and an
   optional `note` records the addressed reviewer's decision once. A second decision on the same
   request is refused and the first stands. A decision from anybody else is denied.
5. A version's `approval_state` is derived, never set by hand: `not_requested` with no requests,
   `changes_requested` when any request says so, `approved` when every request is approved, and
   `pending` otherwise.
6. A project's `approval_status` follows its newest version: `none`, `pending`,
   `changes_requested` or `approved`, except that it reads `outdated` whenever that newest version is
   approved but the project's timeline has been saved since it was frozen. **An approval never
   carries over to anything changed after it was given.**

### Notifications

1. `GET /api/notifications` lists the caller's in-app notifications, newest first. A reviewer is
   notified once per approval request addressed to them, and the requester once per decision.
2. A retried request or decision notifies nobody a second time. No email, SMS or push is sent.

### Compound cases, decided

Each of these has more than one defensible answer. This product takes the one stated here and
applies it everywhere.

1. **A saved block edited or renamed while an instance of it sits on a timeline.** The name and the
   parameters belong to the version, so the placed instance keeps the name and declaration it was
   placed with, and the editor shows the newer-version marker on it.
2. **A member-written block that stops responding during playback.** It is paused as described
   above and the rest of the frame keeps playing.
3. **A reload while an export is rendering.** The export belongs to the frozen version, not to the
   open timeline, so after the reload the versions page resumes rendering any export the member
   started that is still `rendering` and shows its progress again.
4. **A reconnecting member holding edits made while disconnected.** Their save meets the revision rule like any other.
5. **A member removed while an export they started is still rendering.** The job is marked `failed`
   at the moment of removal and its unit is released; exports that were already `ready` stay in the
   workspace.

### The marketing site, contact and legal pages

1. Every public route renders from stored content, not hard-coded markup, and carries its own
   document title and its own meta description, and no two public routes share either. The titles
   are exactly: `/` `Ferment Video : Online Video Editor Engineered for Creativity`; `/product`
   `Creative Code Video Editor & Motion Design Tools : Ferment`; `/pricing` `Pricing : Ferment`;
   `/contact` `Contact Ferment : Video Editor Sales & Support`; `/blog` `Ferment Blog`; `/login`
   `Login to Ferment`; `/register` `Sign up`; `/explore` `Explore : Ferment`; `/templates`
   `Templates : Ferment`; `/blocks` `Blocks : Ferment`; `/privacy-policy` `Privacy Policy : Ferment`.
2. Every document declares a favicon in its head, and the favicon it declares answers with an image.
3. The home route carries its eleven bands in order with the copy in the front-end specification.
   The customer wall shows only customer names whose record is `approved`, in their stored order;
   `GET /api/customers` returns the same list.
4. `/blog` lists three posts with category chips, `Product`, `Tutorials` and `Customer Stories`,
   which filter the list; each post has its own route at `/blog/<slug>`.
5. `/contact` asks which audience the message is for, `sales` or `support`, then `full_name`,
   `email`, `company` and a `message` of at least 20 characters. `POST /api/contact` stores the
   request with its audience and answers with a `reference` of the form `FC-` followed by six digits.
   The same email, audience and message sent again within ten minutes returns the first reference
   and stores nothing new.
6. Every form in the product rejects invalid input next to the field it names, keeps what was typed,
   and writes nothing; the server validates the same rules again and rejects an invalid body with a
   message naming the field.
7. `/privacy-policy`, `/cookie-policy` and `/terms-of-service` are real pages on this origin, linked
   from every footer. The privacy page states what Ferment stores about a member, a reviewer and a
   visitor (account details, workspace content, share view records, consent records and contact
   requests) and how long each is kept. Every internal link on every public route resolves.
8. `/figma-plugin` is the design-tool plugin page the footer's `Resources` column links to; it says
   the plugin is not available yet.
9. `/projects` and every other signed-in route, requested without a session, redirect to
   `/login?next=<the requested path>`, and signing in returns there.

### The consent panel

1. A first-time visitor sees a panel naming Ferment as the operator, stating that no third party
   receives data from this site, and offering five categories: `Necessary`, locked on, then
   `Functionality`, `Experience`, `Measurement` and `Marketing`, with the controls `Learn more`,
   `Reject all` and `Accept all` at the same level, so rejecting takes as many actions as accepting.
2. `POST /api/consent` stores the choice for a browser's `subject_id`: `choices` maps `functionality`,
   `experience`, `measurement` and `marketing` to true or false (`necessary` is always true), and the
   app keeps one record per category with `granted`, `recorded_at`, the `wording_version` and **the
   exact wording the visitor was shown**, sent as `wording`.
   `GET /api/consent/{subject_id}` returns the latest choice per category.
3. Functionality covers remembering the billing toggle and the interface scale for a signed-out
   visitor; Experience covers the home page's live scene and moving previews, which show their still
   frames when it is refused; Measurement covers counting anonymous marketing route views; Marketing
   covers nothing in this product, and the panel says so.
4. Nothing in a non-necessary category runs or is recorded before the visitor chooses:
   `POST /api/marketing-views` with a `subject_id` and a `route` is refused and records nothing unless
   that subject's latest `measurement` choice is granted.
5. The footer on every route carries a `Cookie settings` control that reopens the panel, and
   withdrawing a choice takes the same effort as giving it.

### When a page does not exist

1. An unknown address renders Ferment's own not-found page, headed `We couldn't find that page.`,
   with links back to `/`, `/templates` and `/pricing`, and answers with a true not-found status.
2. An unknown address under `/api`, including `/api/graphql`, answers a JSON error with `error` =
   `not_found` and a not-found status, never an HTML page.
3. A template uuid, creator slug, blog slug or share token that matches nothing renders the
   not-found page and answers not-found.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: live keychain hero, customer wall, statement, blocks, customisation, toolkit, pillars, three ways, templates, production, showcase | public |
| `/product` | the four pillars, import, edit, enhance and ship, in full | public |
| `/pricing` | billing toggle, five plan cards, quota comparison table | public |
| `/templates` | template gallery filtered by category | public |
| `/templates/5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b01` | one template, its preview, credit and remix action | public |
| `/blocks` | block library filtered by category, with live previews | public |
| `/creators/kiln-collective` | one credited creator's collection | public |
| `/blog` | blog index with category chips | public |
| `/blog/blocks-not-clips` | one blog post | public |
| `/contact` | sales or support request | public |
| `/figma-plugin` | design-tool plugin page | public |
| `/privacy-policy` | privacy page | public |
| `/cookie-policy` | cookie categories page | public |
| `/terms-of-service` | terms page | public |
| `/login` | sign in | public |
| `/register` | open signup | public |
| `/s/k7Qm2pVx9LwR4tNz` | shared version player with comments | share link |
| `/review/invite/<token>` | reviewer sets a password | invite link |
| `/explore` | signed-in dashboard with the seed blocks row | member |
| `/projects` | workspace projects table | member |
| `/projects/<id>` | timeline editor with preview, tracks and parameter panel | member |
| `/projects/<id>/versions` | versions table with exports, shares and approval requests | member |
| `/projects/<id>/versions/<vid>/shared` | share created confirmation | member |
| `/projects/<id>/versions/<vid>/sent` | approval requested confirmation | member |
| `/favorites` | favourite blocks and templates | member |
| `/brand-kits` | workspace brand kits | member |
| `/workspace/members` | members and invitations table | member |
| `/workspace/billing` | plan, seats, usage meters and charges | member |
| `/workspace/billing/changed` | plan change confirmation | owner |
| `/settings` | display name and interface scale | signed in |
| `/review` | reviewer inbox of approval requests | reviewer |
| `/review/<request_id>` | reviewer player, comments and decision | reviewer |
| `/review/<request_id>/decided` | decision recorded confirmation | reviewer |

**Entry and redirects.** A signed-out request for `/projects`, `/explore`, `/favorites`,
`/brand-kits`, `/workspace/members`, `/workspace/billing`, `/settings` or `/review` lands on
`/login?next=<path>`, and signing in returns to that path. A member signing in without a `next`
lands on `/explore`; a reviewer lands on `/review`. A reviewer asking for any member route is
refused rather than let in. Signing out returns to `/`, and the same browser then opens no guarded
route. The header shows `Login` and `Try for free` to a signed-out visitor and `Projects` and
`Dashboard` to a signed-in member, in the same places. A share or review link that has expired says
so on its own page rather than redirecting.

**Journeys.**

1. **Choose a plan.** Open `/pricing`, switch the toggle to `Annually`, read `Save up to 28%` on the
   toggle and `Save 21%` on the Pro card, open the comparison table and find `AI Text to Speech`
   marked `Coming soon`, choose `Choose Pro`, register at `/register` with a new address, and land on
   `/explore` inside a new Free workspace named for you.
2. **Remix and tune.** Sign in as `member@example.com`, open `/templates`, filter `Apparel`, open `Trail Jacket Story`, choose `Remix`, land in the editor on `Trail Jacket Story remix`, drop `Glow`
   from the library onto a track beside a clip, turn its `hue` dial, drag its `intensity` slider,
   type into its `text` prompt, press `Undo` twice and `Redo` once, and save.
3. **Save a block for the team.** In that editor choose `Save as block`, name it, find it in the
   workspace library as version 1, then delete it so the library is as it was.
4. **Export and share.** Open `/projects/<id>/versions` for the remix, choose `Save version`, export
   a `png` at the canvas size, watch progress reach ready, create a share with download switched off
   in the row, land on the confirmation reading `Anyone with this link can view this version.`, open
   `/s/<token>` signed out, watch the version, find no download control, and find that the download
   address itself is refused.
5. **Send for approval.** From the same versions table, request approval from
   `reviewer@example.com`, land on the confirmation reading `Waiting on 1 reviewer.`, sign in as
   `reviewer@example.com`, open `/review`, open the request, leave a comment at a moment on the
   scrubber, choose `Approve`, and land on the decision confirmation. Back as the member, find the
   project marked approved, save a change to its timeline, and find it marked outdated.
6. **Hit a ceiling.** Sign in as `member3@example.com`, save one block (5 of 5), try to save another
   and read `Free includes 5 saved blocks. Remove one or upgrade to add more.`, then delete the block
   you saved.
7. **Fill the last seat.** Sign in as `member@example.com`, open `/workspace/members`, invite an
   address in the row (10 of 10), invite another and read
   `Pro includes up to 10 members. Upgrade to Business to add more.`, then revoke the invitation you
   made.
8. **Decide on cookies.** Open `/` in a fresh browser, choose `Reject all`, reload and find the panel
   gone and the hero showing its still frame, open `Cookie settings` from the footer and choose
   `Accept all`.
9. **Stay in your lane.** Sign in as `reviewer2@example.com`, find `/review` empty, then request a
   `Juniper Goods` project page and be refused.

**States.** Every list has an empty state that says what would appear there and offers the action
that creates it. Every route has a loading state shaped like the content it is waiting for. No
failure takes a route down: a panel that fails to load says so, offers a retry and leaves the rest of
the page working. An export shows rendering with its progress and queue position, ready with its
file, or failed with the no-charge message, and reloading shows the same state. 

## UI/UX notes

**North star.** Somebody opening Ferment should understand within one screen that the timeline is
made of tools they can turn, not clips they can only cut, and should feel that the product is
precise and fast rather than decorated. **Register.** The marketing site is editorial and carries
atmosphere, with the product itself, drawn live, as the first thing seen; the application is an
operational tool, dense and quiet, built for long sessions of repeated small adjustments. Two
stances hold the product together, and a competing editor could rationally invert either:
**monochrome over colourful**, because the member's own footage and brand kit supply the colour,
and **the product over pictures of the product**, because every preview on the site is a real block
drawing itself rather than a screenshot.

**Mode.** The application is designed dark, fully, and has no light mode to grade. The marketing site
alternates dark bands and light bands deliberately, and both grounds are designed in full.

**Palette by role.** Nearly everything is black, white and grey. The dark ground is a near-black
neutral, a deeper near-black sits beneath the editor's stage, and raised dark surfaces are a
near-black neutral lifted by a faint white wash. The light ground is a near-white neutral with a
second near-white one step darker for alternating bands, and pure white is kept for type and marks
on dark. Text hierarchy comes from the opacity of the same two anchors, never from extra hues: a muted
ink for secondary text and a half ink for supporting copy, and any text a visitor needs to read
stays well clear of the faint end of that range. The only chromatic
colour in the design system is one brand gradient running from a light, soft green through a light,
vivid amber to a light, vivid orange, and it only ever appears as a gradient: it is never a flat fill,
never a text colour and never a status colour. Three meanings get their own treatment and nothing
else borrows it: a mid, vivid red means something failed or is about to be destroyed; the brand
gradient drawn as a thin outline means something is rendering or waiting on someone; and success is a
word with a tick on a neutral chip. A state that is none of the three uses neither the red nor the
outline. The exact shades are yours, so long as the gradient stays the only colour and each meaning
keeps its treatment to itself.

**The glowing outline.** The most popular pricing card, the selected template and the block being
edited wear a thin outline painted with the brand gradient, and the outline is deliberately
lopsided: colour runs around roughly two fifths of it and the rest is plain white, so it reads as
light catching one edge rather than as a rainbow ring. An outline with its colours spaced evenly
around the whole edge is a defect even with the right colours.

**Elevation.** Raised surfaces on dark have twenty-four distinguishable levels, each a slightly
brighter white wash, and the step between neighbouring levels shrinks as the levels rise, because on
a dark ground the eye stops noticing equal steps quickly. The timeline uses these levels to separate
tracks, items, the selected item and the floating panels without drawing a border between them.

**Type and typography.** One grotesque family in two widths carries the product: the regular width for everything
and a wider one reserved for the home hero line. A monospace appears only in the code editor and
beside numbers that must line up. There are two scales and they behave differently on purpose: the
document scale used on marketing and reading pages grows when the reader enlarges their browser's
text, while the editor's own furniture (panels, track labels, parameter names, timecodes) keeps a
fixed scale so the timeline does not reflow mid-edit. The interface scale setting in `/settings`
exists to make up for exactly that trade and enlarges the whole editor chrome together. Display
headings on the marketing site are sized from the window's width and their lines sit slightly tighter
than the letters are tall. Figures align in a column wherever amounts, timecodes or counts stack.
Every text style is a named style used everywhere, never a one-off. The families and sizes are
yours, so long as the two widths, the two scales and the monospace rule hold.

**Shape and density.** Corner radius is part of the character, and corners are clearly rounded: cards and panels most, fields and buttons less,
navigation items in between, pill-shaped controls fully round, and small square tiles take a corner
proportional to their size so a tile keeps its shape at any size. The marketing site is spacious, one
thing dominant per view, and sections are separated by space and by the change of ground rather than
by rules. The application is compact: the timeline, the stage and the parameter panel share one
screen without scrolling at a common laptop size, rows in every table sit tight enough that a
workspace's projects fit on one screen, and positions never jump while a member works. The layout
archetype of the application is a persistent left sidebar, `sidebar-nav`, with the working surface
beside it.

**Motion.** The character is `eased` and considered: things arrive quickly and settle slowly, and
nothing loops on its own except the customer wall. The signature entrance is a short rise into place
while fading in, with the fade finishing well before the rise, so an element is already solid for the
last stretch of its travel. Headings arrive a line at a time, each line starting from exactly its own
height below, so a tall heading and a short one finish together; the statement on the home page
arrives a word at a time on the same principle; horizontal rules draw themselves open from nothing.
Each element reveals once and stays; scrolling back never replays it. Pointer and press feedback on
controls is quick and short, one speed everywhere. The easing inventory is small and shared: one
named set of curves serves the whole product, the fade in an entrance runs at an even linear pace
while the movement decelerates, and no component brings a curve of its own. Transitions name the exact properties they
animate; nothing animates every property at once, and nothing moves that nobody designed. The only
overshoot in the product is the dial's knob settling after a turn. Under a reduced-motion request,
every reveal resolves at once to its end state, the home scene holds its still frame, no preview or
video plays by itself, rules appear already drawn, and the short control feedback stays because it is
how a member knows a control responded.

**Components.** Every control has resting, pointed-at, pressed, focused and unavailable states, and
unavailable is never signalled by colour alone. Hover styling applies only where the pointer can
actually hover, so a tapped control on a touch screen never stays stuck looking hovered. There is one
main action style, carrying the strongest contrast on its ground, and one quieter alternative;
each view leads with one main action. Escape closes any open panel, menu or dialog and returns focus
to what opened it. Destructive actions (delete a block, remove a member, revoke a share) ask once
before acting, in the row itself. Every form control has a persistent visible label, never a
placeholder standing in for one.

**Accessibility floors, which are contract rather than taste.** The product meets WCAG 2.2 level AA
on the marketing site and in the editor alike. Body text reaches a contrast of at least `4.5:1`
against its ground, and large text, interface components, the focus indicator and the gradient
outline reach at least `3:1`. Touch targets meet the WCAG 2.2 minimum target size and the editor's
dial and slider handles are comfortably larger than it. Keyboard navigation reaches every control in
the product, including the timeline items, the dial, the sliders, the consent panel and the pricing
toggle, and every focused element shows a visible focus indicator that is never removed. A dial and a
slider change by one step per arrow key and by a larger step with a modifier, and announce their
value. `Skip to content` is the first focusable element on every route. Every heading that is split
into lines or words for its entrance also exists once as a single intact string for assistive
technology, with the split pieces marked decorative, and a line break introduced by the layout never
appears in that string. The home scene has no accessible role of its own; the heading beside it
carries the meaning. Icon-only controls carry a text label. Meaning is never carried by colour alone.
Nothing flashes more than three times a second.

**Responsive.** The layout is responsive and holds at every viewport width between a phone and a
wide desktop, with display type scaling with the window rather than jumping, and only two genuine
rearrangements. At the wider breakpoint the header's navigation starts giving way and the pricing
cards drop from four across to two, with the comparison table scrolling inside itself; at the
narrower breakpoint the navigation becomes a single toggle opening a full panel with subtitles, and
the pricing cards stack. Where those breakpoints fall is yours. The editor needs width: below the
wider breakpoint the stage and the timeline stack, and at phone widths the project opens as a
playable, read-only preview with a note that editing needs a wider window. Nothing on any route
scrolls sideways except the customer wall, the templates marquee and a wide table's own scroll area.

**What it must not look like.** Not a page washed in one hue, not a gradient used as a flat
background, not screenshots standing in for a product that can draw itself, not a marketing
composition inside the editor, and not an editor whose state has to be guessed from a colour with no
word beside it.

## Technical requirements

- Front end: Astro with its Node server adapter, so every route is rendered on the server and arrives
  as complete HTML on first paint, with the interactive regions (the editor, the parameter panels,
  the pricing toggle, the consent panel, the home scene and the block previews) shipped as Astro
  islands written in one component framework Astro integrates officially. Pick one and use it for
  every island. The browser draws the home scene, the block previews and every export frame itself,
  with whatever drawing, three-dimensional and media-encoding packages that needs, installed from the
  public npm registry when the image is built.
- Back end: FastAPI on Python 3.12, served by Uvicorn, with the HTTP API under the `/api` prefix on
  the same origin as the pages; psycopg 3 for PostgreSQL and boto3 for the object store.
- Store: PostgreSQL, reached at `DATABASE_URL`, which the environment also exports as `DB_URL` with
  the same value.
- Objects: MinIO, reached at `STORAGE_ENDPOINT`, with the bucket named by `STORAGE_BUCKET`, which
  already exists and is private, and the credentials `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`.
- Auth: app-implemented email and password with bearer tokens, passwords stored hashed with a slow
  salted algorithm.
- Health: `GET /api/health` returns `200` with `{"status": "ok"}` once PostgreSQL and MinIO are both
  reachable.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are PostgreSQL and MinIO, and reaching for anything else is a
contract violation.

PostgreSQL and MinIO are already running and reachable at those variables. Do not download,
install, compile or start a copy of either, and never hardcode a host, a port or a credential the
environment supplies.

- Nothing the browser downloads carries a database credential, an object-store credential, a bucket
  key it was not entitled to, or another member's token.
- Every public route serves its own title and meta description, a favicon declaration and nothing
  fetched from another origin at runtime: fonts, scripts and styles are served by the app itself.
- Only the two type widths the product uses are loaded, subset to the characters the product
  shows, in one compressed web font format; no further widths are loaded.
- Each public route ships only the script it needs, and the home scene, the marquees and the consent
  panel never delay the first paint of the heading and the call to action.
- All timestamps are UTC and are sent as ISO 8601 strings ending in `Z`. Dates in period and window
  arithmetic are UTC calendar dates.
- A list endpoint returns a top-level JSON array.

## Data model

Thirty-four tables. All timestamps are UTC. Every table has an integer `id`.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

- **`account`**: `id`, `email` unique and stored lowercased, `password_hash`, `display_name`, `role`
  (`member` or `reviewer`), `interface_scale`, `created_at`.
- **`workspace`**: `id`, `name`, `owner_id`, `created_at`.
- **`workspace_member`**: `id`, `workspace_id`, `account_id`, `relation` (`owner` or `member`),
  `joined_at`. An account appears at most once per workspace.
- **`invitation`**: `id`, `workspace_id`, `email`, `token` unique, `state` (`pending`, `accepted` or
  `revoked`), `created_at`, `accepted_at`.
- **`plan`**: `id`, `key` unique, `name`, `sort_order`, `monthly_price_cents`,
  `annual_monthly_price_cents`, `unit`, `member_cap`, `positioning`, `most_popular`, `cta_label`.
- **`plan_feature`**: `id`, `plan_key`, `label`, `value_text`, `status` (`available` or
  `coming_soon`), `sort_order`.
- **`quota`**: `id`, `plan_key`, `meter`, `limit_value` (empty means unlimited), `period`
  (`monthly` or `ceiling`). One row per plan and meter.
- **`subscription`**: `id`, `workspace_id` unique, `plan_key`, `billing_period`, `seats`, `status`,
  `anchor_date`, `current_period_start`, `current_period_end`.
- **`charge`**: `id`, `workspace_id`, `kind`, `plan_key`, `seats`, `amount_cents`, `currency`,
  `period_start`, `period_end`, `created_at`.
- **`meter_balance`**: `id`, `workspace_id`, `meter`, `window_start`, `used`, `limit_value`. One row
  per workspace, meter and window, and `used` is never greater than `limit_value` when a limit exists,
  under concurrent requests as much as under sequential ones.
- **`usage_event`**: `id`, `workspace_id`, `meter`, `amount`, `window_start`, `state` (`reserved`,
  `settled` or `released`), `export_id`, `project_id`, `created_at`, `settled_at`.
- **`creator`**: `id`, `slug` unique, `display_name`, `credit`.
- **`block`**: `id`, `name`, `category` (`Text`, `Motion`, `3D`, `Shader` or `Code`), `kind`
  (`library` or `custom`), `workspace_id` (empty for library blocks), `creator_slug`, `licence`,
  `current_version`, `deleted_at`, `created_by`.
- **`block_version`**: `id`, `block_id`, `version`, `parameter_schema`, `source`, `created_at`. One
  row per block and version, and a stored version is never changed.
- **`template`**: `id`, `uuid` unique, `name`, `category`, `creator_slug`, `premium`,
  `canvas_width`, `canvas_height`, `fps`, `duration_ms`, `timeline`, `sort_order`.
- **`favorite`**: `id`, `workspace_id`, `account_id`, `block_id`, `template_uuid`.
- **`brand_kit`**: `id`, `workspace_id`, `name`, `colours`, `fonts`, `logo_asset_id`.
- **`asset`**: `id`, `workspace_id`, `object_key` unique, `filename`, `content_type`, `byte_size`,
  `sha256`, `created_by`, `created_at`.
- **`project`**: `id`, `workspace_id`, `name`, `canvas_width`, `canvas_height`, `fps`,
  `duration_ms`, `timeline`, `revision`, `remixed_from`, `brand_kit_id`, `superseded_shares`,
  `created_by`, `created_at`, `updated_at`. Two saves from the same revision never both land.
- **`project_version`**: `id`, `project_id`, `number`, `project_revision`, `timeline`, `created_by`,
  `created_at`. Numbers are unique within a project, and a version is never changed.
- **`export_job`**: `id`, `workspace_id`, `version_id`, `request_key`, `format`, `width`, `height`,
  `fps`, `watermarked`, `is_variation`, `status` (`rendering`, `ready` or `failed`), `progress`,
  `failure_reason`, `object_key`, `byte_size`, `created_by`, `created_at`, `finished_at`. One job
  per workspace and `request_key`, however many times or however simultaneously it is requested.
- **`share_link`**: `id`, `workspace_id`, `version_id`, `token` unique, `passphrase_hash`,
  `expires_at`, `allow_download`, `allow_comments`, `recipients`, `revoked_at`, `created_by`,
  `created_at`.
- **`share_view`**: `id`, `share_id`, `route`, `viewer_email`, `viewed_at`.
- **`share_access_attempt`**: `id`, `share_id`, `succeeded`, `attempted_at`.
- **`comment`**: `id`, `version_id`, `author_email`, `at_ms`, `anchor_item_id`, `anchor_offset_ms`,
  `body`, `created_at`.
- **`approval_request`**: `id`, `version_id`, `reviewer_email`, `state` (`pending`, `approved` or
  `changes_requested`), `note`, `requested_by`, `created_at`, `decided_at`. One request per version
  and reviewer.
- **`review_invite`**: `id`, `email`, `token` unique, `accepted_at`.
- **`notification`**: `id`, `account_email`, `kind`, `subject_ref`, `body`, `event_key` unique,
  `created_at`, `read_at`. One notification per event however often the event is retried.
- **`customer_logo`**: `id`, `name`, `sort_order`, `approved`.
- **`blog_post`**: `id`, `slug` unique, `title`, `category`, `summary`, `body`, `published_at`.
- **`contact_request`**: `id`, `reference` unique, `audience`, `full_name`, `email`, `company`,
  `message`, `created_at`.
- **`consent_record`**: `id`, `subject_id`, `category`, `granted`, `wording_version`,
  `wording_shown`, `recorded_at`.
- **`marketing_view`**: `id`, `subject_id`, `route`, `viewed_at`.
- **`marketing_page`**: `id`, `route` unique, `title`, `description`.

Derived rather than stored: `annual_saving_percent` and the `Save up to` figure; the usage shown for
each meter; `seats_used`; a version's `approval_state`; a project's `approval_status`; a comment's
`state` and resolved `at_ms` on a given version; an export's `queue_position`; whether a share is
active, expired or revoked; and whether a rendering export has gone stale. None of them is a column
that can drift from what it is derived from.

**Seed data.**

- The five plans, their quotas and their features exactly as the tables in Core features state.
- The eight library blocks, the eight templates and the three creators exactly as the tables in Core
  features state. `Denim Drop` has a Glow item `title-1` from 0 to 5000 ms and a clip item `clip-3`
  from 10000 to 15000 ms on a 1080 by 1920 canvas at 30 fps lasting 15000 ms.
- Workspace **`Juniper Goods`**: Pro, billed monthly, its current period starting on the UTC date ten
  days before the app first starts and ending one calendar month later, `seats` 2, members
  `member@example.com` (owner) and `member2@example.com`, and seven pending invitations,
  `crew1@example.com` through `crew7@example.com`, so 9 of its 10 member places are taken. One
  `plan_change` charge of `7600` at the period start. Four brand kits, `Juniper Core`,
  `Juniper Holiday`, `Juniper Outdoor` and `Juniper Kids` (4 of 5). Three saved blocks,
  `Juniper Lower Third`, `Juniper Price Tag` and `Spin Forever` (3 of 50), the last a Code block
  whose source never finishes a frame. Project `Denim Drop remix`, remixed from `Denim Drop`, at
  revision 2, with version 1 (revision 1, a ready `png` export at 1080 by 1920, approved by
  `reviewer@example.com`) and version 2 (revision 2, a ready `png` export at 1080 by 1920, approval
  pending from `reviewer@example.com`). In version 2, `title-1` starts at 1000 ms and `clip-3` has
  been removed. Two comments by `reviewer@example.com` on version 1: `Can the glow start softer?` at
  2000 ms and `Hold this shot a beat longer.` at 12000 ms. Four shares of version 1:

  | Token | Settings |
  |---|---|
  | `k7Qm2pVx9LwR4tNz` | open, no expiry, download off, comments on, three recorded views |
  | `pQ4rT8vW2yZ6aB3c` | expired one day before the app first starts, download on |
  | `mN5bV7cX1zL3kJ9h` | passphrase `orchard-lantern-42`, download on, comments off |
  | `dR2fG6hJ8kL0pQ1s` | recipients `reviewer@example.com` only, download off |

- Workspace **`Solo Sketchbook`**: Free, billed monthly, period starting five days before first
  start, owned by `member3@example.com`, with four saved blocks, `Sketch Title`,
  `Sketch Underline`, `Sketch Sticker` and `Sketch Wipe` (4 of 5), and project `First Sketch`
  (1280 by 720, 30 fps, 6000 ms) with no versions.
- Workspace **`Basic Bench`**: Basic, billed monthly, period starting three days before first
  start, owned by `member4@example.com`, with project `Bench Promo` (1080 by 1080, 30 fps,
  10000 ms) and its version 1, which has no ready export. Nineteen settled `project_variations`
  units in the current window (19 of 20), twenty settled units in the previous window, and one
  export job on version 1 (a `png` variation at 540 by 540 with `request_key` `stale-bench-1`)
  created two hours before first start and still marked `rendering`, so it reads as `failed` and
  its unit is released.
- Customer names, 25 rows: `Northwind Apparel`, `Kestrel Foods`, `Lumen Skin`, `Parcel & Pine`,
  `Harlow Coffee`, `Brightline Apps`, `Velo Outfitters`, `Marigold Beauty`, `Stonefruit Kitchen`,
  `Quartz Labs`, `Tidewater Denim`, `Orchid Cosmetics`, `Copperleaf Tea`, `Signal Grove`,
  `Fieldnote Studio`, `Saltmarsh Swim`, `Juniper Goods`, `Aster Pharmacy`, `Longhand Paper`,
  `Mosaic Media`, `Pebble Toys`, `Riverbend Bikes`, `Cinder Candles`, `Glasshouse Juice`, all
  `approved`, in that order, and `Ashgrove Motors`, withdrawn and never shown.
- Three blog posts: `Blocks, Not Clips` (`blocks-not-clips`, `Product`),
  `Tuning a Glow in Four Moves` (`tuning-a-glow-in-four-moves`, `Tutorials`) and
  `How Juniper Goods Ships Weekly` (`how-juniper-goods-ships-weekly`, `Customer Stories`).
- One `marketing_page` row per public route, carrying the titles listed in Core features.
- The seeded export files are rendered by the app itself at first start and written to the bucket at
  their scheme's keys.

Seeding must be idempotent - restarting the app must not duplicate rows, and must not write a second
copy of a seeded object into the bucket.

## Front-end specification

The visual detail the sections above state as intent, surface by surface. Every paragraph describes
something a person can see and a reviewer can reject; the values behind it are yours.

**Information architecture.** Two layers on one origin: the marketing routes, reached from the
floating header and the footer, and the application routes, reached from the sidebar once signed in.
`Blocks` and `Templates` belong to both: a visitor can browse them, and remixing or saving leads
into the application. There is no site search, no breadcrumb trail and no language switch, and the
consent panel is the only interstitial.

**Component architecture.** One shared design-token set (colours, the twenty-four elevation
levels, the gradient and its lopsided outline, both type scales, the corner family and the motion
set) feeds the marketing site and the application alike, so the two can never drift apart; no
component types a colour, size or curve of its own. The reveal behaviour is one component used by
every revealing element, the split heading is one component used by every split heading, and the
gradient outline is one component, so each behaves the same everywhere it appears.

**Zero-asset rule.** The product ships no image files for its own interface and no route requests
one: every picture of the product is a substitution drawn live by the product itself, and customer
logos are not reproduced at all, the customer's name being set as type instead. Fonts are the only
binary files the interface loads.

**Stacking.** The product's own stacking ladder of layers (tracks, items, the playhead, floating
panels, menus, dialogs) always stays beneath the consent panel, which is the topmost layer on every
route.

**Global chrome: the header.** On marketing routes the header is a floating pill set in from the top
and sides on a light, translucent ground, holding two groups: the wordmark followed by the navigation
items `Product`, `Blocks`, `Templates`, `Pricing` and `Blog` and a vertical-ellipsis overflow
control, and, in a separate pill of its own, `Login` and `Try for free` (or `Projects` and
`Dashboard` once signed in). As the page scrolls down the left pill narrows until only the wordmark
and the ellipsis remain, while the right pill does not move or change size, so the two never appear to
slide against each other; scrolling back to the top restores the full navigation. The collapse is one
pill changing width, never two headers cross-fading. On inner marketing routes a small tagline sits
above the navigation, reading `Add Ferment` and `It's a whole new timeline.` At the narrowest widths
the navigation becomes one toggle that opens a full panel, closed by `Close`, in which each item
carries a subtitle the wide header does not show: `Product` with `Explore features`, `Blocks` with
`Browse 1000s of Ferment blocks`, `Templates` with `Start with a template` and `Pricing` with
`Compare our plans`. The layout break inside `Browse 1000s of Ferment blocks` is never part of the
accessible string. `Blocks` and `Templates` lead into the application's own library and gallery.

**Global chrome: skip link and footer.** `Skip to content` is first in the tab order on every route
and becomes visible when focused. The footer has four columns: `Explore` with `Product`, `Pricing`
and `Get in touch`; `Socials` with `Instagram`, `Youtube`, `X`, `LinkedIn` and `Pinterest`, each
pointing at the same account everywhere it appears because the links are read from one record;
`Resources` with `Figma Plugin`; and `Legal` with `Privacy Policy`, `Cookie Policy` and
`Terms of Service`, all on this origin. Beneath them sit the wordmark, `Copyright (C) 2026 Ferment`,
`All rights reserved.` and the `Cookie settings` control.

**The consent panel.** A full-width panel rises from the bottom of the window on a dark ground on a
first visit and sits above everything else on the page, covering roughly the lower third. It names
the operator, states plainly that no third party receives data, lists the five categories with a
switch each (the necessary one shown on and unavailable), and carries `Learn more`, `Reject all` and
`Accept all` together as pill-shaped buttons of equal weight. While open it holds keyboard focus
inside itself, it is announced when it appears, it closes from the keyboard, and closing it returns
focus to where it was. `Learn more` expands each category's plain description in place.

**Home: the hero.** A keychain hangs into the frame from above: a carabiner, a chain made of one link
repeated, a key and four charms, one of them the Ferment wordmark in relief, one a single-letter
charm, one a disc and one blackletter. It is drawn live in the browser from seven separate primitive
pieces, never from one baked model: each chain link is a flattened ring, repeated along a curve with
alternating rotation; the carabiner is a partial ring with a swept gate, a hinge and a spring detail;
the key is an extruded profile, a rounded bow bored with a hole and a notched blade; and each tag
charm is a rounded plate with a bored hole and its lettering in relief. One generated environment
(bright above, dark below, a soft horizon band and two small bright panels for the metal to catch)
drives the lighting of every material, so the chain, clasp and key read as polished metal and the
charms as glossy polymer and translucent coloured resin. It sways gently in
response to the pointer. The fallback is a still frame of the same composition, shown while the pieces load, when
the scene cannot start, when Experience consent is refused and under reduced motion, and the swap
between still and live is not noticeable. The heading `Engineered for Creativity`, the line
`Ferment, the first video editor you can build on.` and the `Get Started` action, which leads to
`/register`, are readable before the scene arrives, and the page never shows an empty box where the
scene will be. The heading is the largest type in the product.

**Home: the bands that follow.** In order: the customer wall, headed
`Teams from top brands and agencies build with Ferment`, a continuous marquee of the approved
customer names set as type in the display face at one consistent weight, never drawn logos, pausing
when it leaves the screen, while pointed at and under reduced motion; the statement,
`Ferment is the first video editor where creatives can build and remix custom design tools right on timeline.`,
at the second-largest display size, arriving word by word; the blocks band, headed
`There's a block for that`, with the line
`Browse curated blocks for motion graphics, kinetic type, 3D, shader effects, and beyond.` and the
tab row `Library | Text Blocks`, whose four previews are the real `Inflate`, `Glow`, `Focus` and
`Halftone` blocks each drawing its own name, with Inflate puffing up letter by letter; the
customisation band, `Infinitely customizable.` with
`Make blocks your own with intuitive dials, sliders, prompts, and even with code.`, showing a live
round dial and a bank of four vertical sliders that visibly change a block beside them; the toolkit
band, `Your new creative toolkit` with
`Customize and save your favorite blocks so your team never starts from scratch again.`; the pillars
band, `Explore features`, `Your new all-in-one video editor.` and `View All Features`, with four
pillars `Import` (`Drop in photos, videos, audio, and assets from anywhere, instantly.`), `Edit`
(`Powerful timeline editing with speed controls, voiceovers, and built-in stock libraries.`),
`Enhance` (`Layer animations, effects, and shaders to elevate every frame.`) and `Ship`
(`Collaborate with your team and export up to 60fps as Image, Video or GIF.`); the three-ways band,
`Create in 3 ways`, with `Remix` (`Start from templates and pre-built blocks designed for real campaigns.`),
`Describe` (`Name the effects you want in plain words and get a new variation to refine.`) and `Code`
(`Write your own block, declare its controls, and share it with your team.`); the templates band,
`Templates inspired by leading brands`, `The best stories are built block by block.` and
`Browse All Templates`, a marquee of the eight templates with their categories; the production band,
`Create more, faster` with `Accelerate your content production.` and
`Ferment makes it simple to scale your creative to every common size and format and try out new variants with a few clicks.`,
then `Turn anything into everything.` with `High performance. Totally programmable.` and its own
paragraph, `One timeline becomes every size a campaign needs, each variation counted against your plan.`;
and the showcase, `Get the look`, crediting `Kiln Collective`, `Halfstep Motion` and `Oriel Park` and
ending in `All Blocks & Templates`. Where no demonstration footage exists, a band shows a drawn
diagram of the timeline (stacked tracks, items at different elevations and a playhead) rather than a
placeholder, and no route requests an image file for any of this.

**Product route.** The four pillars, each expanded into its own band in the same band system, with
the title carrying the product's real positioning, creative code.

**Pricing route.** A two-position segmented toggle, `Monthly` and `Annually`, with the `Save up to`
badge attached to the annual side; switching changes every price in place without a reload and
without the cards changing size. Four purchasable cards sit side by side on a wide screen with the
Enterprise card spanning beneath them; the Pro card wears the lopsided gradient outline and the
`Most popular` marker, and its outline stays concentric with its rounded corners. Each card shows its
name, positioning line, price with its unit, call to action, and its `Everything in ..., plus:` list.
Below, the comparison table has a sticky first column of row labels and a sticky header of plan
names, marks `Coming soon` rows with a word and an icon rather than greyed text alone, and states
`not included` in words where a plan lacks a row. Disclosure rows in the table open to their real
content height smoothly.

**Template gallery and template route.** A grid of template cards, each a live preview of the
template's first seconds running only while in view, with its name, category and creator credit and a
`Premium` marker where it applies. Category filters (`Apparel`, `Beauty`, `Food & Beverage`,
`Software / Apps`) sit above as chips, several may be active, and the chosen set lives in the address
so a filtered view survives a reload. The template route shows a larger preview, the credit linking to
the creator's page, the block list it uses, and `Remix`; a signed-out visitor choosing `Remix` is sent
through sign-in and back.

**Block library and creator route.** The library groups blocks by category tabs with `Library` and
`Text Blocks` among them, shows each block as a live preview drawing its own name or motion, and a
name filter that settles once typing pauses rather than on every keystroke. Opening a block shows its
generated control panel beside its preview so a visitor can turn the dial before signing up. The
creator route shows the creator's name, credit line and collection.

**Blog, contact, legal and plugin routes.** The blog index shows posts as rows with a date, a title
and a category chip; the chips are rounded tags and filter the list. Contact first asks
`What can we help with?` with the two audiences as large choices, then shows the fields; a sent form is
replaced by a confirmation carrying the reference. The legal pages are long-form reading pages at a
comfortable measure with in-page headings.

**Authentication routes.** `/login` and `/register` are single centred forms on the dark ground with
the wordmark above, a persistent label on each field, inline errors beside the field they concern,
and a link between the two. `/register` states the Free plan the new workspace starts on.

**The application shell.** A persistent left sidebar holds `Home`, `Explore`, `Favorites`, then a
`Workspace` group with `My Files`, `Brand Kit`, `Members` and `Billing`, then `Settings`, with the
current item marked by more than colour, and the workspace switcher at its top listing every
workspace the member belongs to. `/explore` leads with a `Seed Blocks` row subtitled
`Start with a block`, a horizontal row of block cards credited to their creators, followed by recent
projects and the templates the workspace remixed. `/projects` is a table first: name, last saved,
revision, versions, approval status as a word, and the member who saved last, sortable by column,
with a new-project row at the top that creates a project in place.

**The editor.** Three regions on one screen: the stage, showing the current frame on the deepest
ground with the canvas proportion kept and a transport row beneath it (play, pause, the playhead
time and the duration in aligned figures); the timeline beneath, with one row per track, a track
label that can be renamed in place, items drawn as raised blocks at distinct elevation levels, clips
showing their media name and block items showing their block name and a small live thumbnail, a
playhead line across all tracks, and a ruler with timecodes; and the parameter panel at the side,
generated from the selected block's declaration. Selection, trimming by the item edges, moving,
copying and deleting behave the same for clips and block items. A dial is a round knob with a marker
and its value in degrees beside it, turned by dragging round it or by the arrow keys; a slider is a
vertical or horizontal track with a handle and its value beside it; a prompt is a text field showing
how many characters remain; a code parameter opens a monospace editor with line numbers and a
`Run` action, and its errors appear beneath it without taking the stage down. `Undo` and `Redo` sit
in the editor's top bar with their keyboard shortcuts shown. A save state reads `Saved`, `Saving` or
`Not saved` beside the project name. The library drawer slides in from the side, filters by category and name,
and blocks are dropped onto a track by dragging or by a keyboard action. `Save as block` opens a
short inline form for the name and category. A paused Code block shows its stopped message in its
own area on the stage and in its item on the timeline, with a `Restart` action.

**Versions route.** A table of versions, newest first: number, created time, who froze it, approval
state as a word, and its exports and shares nested beneath. `Save version` adds a row. Exporting is
an inline row with format, width and height (prefilled with the canvas size and marked as a variation
the moment either differs), and a rendering export shows a progress bar that fills smoothly, its
queue position, and the gradient outline around the row until it is ready or failed. Creating a share
is an inline row with expiry, passphrase, recipients and two switches, `Allow download` and
`Allow comments`; submitting it lands on the full-page confirmation carrying the link, a copy action
and the share message. Requesting approval is an inline row of reviewer addresses; submitting it lands
on the full-page confirmation carrying the waiting message.

**The share page.** A player on a dark ground showing the shared version at its own proportion, the
project name and version number, the superseded notice as a banner above the player when it applies,
and the comments listed beside it in time order, each also shown as a marker on the scrubber; choosing
a marker moves the playhead there. A passphrase-protected share first shows a single passphrase field
and a `View` action; a recipients-only share first asks the visitor to sign in. When download is off
there is no download control at all; when on, `Download` sits under the player. When comments are on,
a field under the player posts a comment at the current playhead time. An expired or replaced share
shows only its message and the wordmark.

**Reviewer surfaces.** `/review` is a table of requests with project, version, requester and state.
`/review/<request_id>` is the share page's player and comments plus two actions, `Approve` and
`Request changes`, with an optional note; after deciding, the full-page confirmation states the
decision and that the requester has been told. The guest scope sentence sits under the reviewer's
name in the header of these pages.

**Workspace routes.** `/workspace/members` is a table of members and pending invitations with the
seat count above it (`9 of 10` style, with the unit named), an invite row at the top, and a remove or
revoke action on each row. `/workspace/billing` shows the current plan and billing period, the period
dates, a meter row for each quota (a bar that fills toward its limit, the used and limit figures in
aligned numbers, and `Unlimited` or `Not included` in words where they apply), then the charges table
and the plan choices; a change lands on the full-page confirmation stating the new plan, seats and the
charge written. `/brand-kits` lists kits with their colour swatches and font names; `/favorites`
lists favourite blocks and templates as the same cards the library uses.

**Settings.** `/settings` offers the display name and the interface scale as four choices, `100%`,
`115%`, `130%` and `150%`, applied to the editor chrome immediately and kept for the account.

**Empty, loading and error states.** In-place content arrives as a skeleton the shape of the content,
never a spinner that collapses the layout. An empty projects table invites a first remix. An empty
review inbox says nothing has been sent yet. A failed panel says what failed, offers a retry and
leaves the page standing. The not-found page keeps the header and footer, shows its heading and its
three ways back.

**Focus.** A focused control shows a visible indicator offset from its edge in the ink colour on light
grounds and in white on dark grounds, shown for keyboard focus and suppressed for pointer clicks, and
never removed anywhere, including inside the consent panel, the timeline and the menu panel. Focusing
an element that has not yet revealed makes it reveal at once, and the content of every page is in the
document and in reading order before any script runs.

## Constraints

- One product, many workspaces. No organisations above workspaces, no single sign-on, no SCIM, no
  organisation-level controls and no immutable audit log; Enterprise is a card and a conversation.
- No payment provider, no card collection, no invoices and no payment callbacks. Charges are the app's
  own records in `usd`.
- No captioning, no speech synthesis, no background removal and no stock media library: those rows
  are published as coming soon and nothing consumes their allowances. No ProRes and no 4K export.
- No saving of designs as custom templates.
- No live co-editing channel: concurrent edits meet at save time, as stated above.
- No server-side rendering of video frames and no execution of member-written block code on the
  server.
- No viewer-tied watermarking burned into shared frames, and no restricted playback by embedding
  domain; playback is restricted by named recipient only.
- No email, SMS or push; notifications are in-app only.
- No third-party analytics, tag manager, consent vendor, font host or content delivery network, and
  no other network call at runtime.
- No native app, no offline mode and one language, English.
- The app stays responsive with a library of several thousand blocks, a few hundred projects per
  workspace and a few thousand exports.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A successful
call returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason. `{ws}` is a workspace `id`, `{vid}` a version `id`, `{eid}` an export job `id` and `{sid}` a
share `id`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | - | `status` |
| `POST /api/auth/signup` | `email`, `password`, `display_name`, `workspace_name` | `access_token`, `email`, `role`, `workspace_id` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `email`, `role` |
| `POST /api/auth/logout` | - | an empty success |
| `GET /api/me` | - | `email`, `display_name`, `role`, `interface_scale` |
| `PATCH /api/me` | `display_name`, `interface_scale` | the account |
| `GET /api/plans` | - | `key`, `name`, `monthly_price_cents`, `annual_monthly_price_cents`, `annual_saving_percent`, `unit`, `member_cap`, `most_popular`, `quotas`, `features` |
| `GET /api/blocks` | `category`, `q`, `limit`, `offset` | library blocks: `id`, `name`, `category`, `kind`, `creator_slug` |
| `GET /api/blocks/{id}` | - | the block with `parameter_schema` and `current_version` |
| `GET /api/templates` | `category` | `uuid`, `name`, `category`, `creator_slug`, `premium` |
| `GET /api/templates/{uuid}` | - | the template with `canvas_width`, `canvas_height`, `fps`, `duration_ms`, `timeline` |
| `GET /api/creators/{slug}` | - | `slug`, `display_name`, `credit`, `templates` |
| `GET /api/blog/posts` | `category` | `slug`, `title`, `category`, `summary`, `published_at` |
| `GET /api/blog/posts/{slug}` | - | the post with `body` |
| `GET /api/customers` | - | `name`, `sort_order` for approved customers |
| `POST /api/contact` | `audience`, `full_name`, `email`, `company`, `message` | `reference` |
| `POST /api/consent` | `subject_id`, `choices`, `wording_version`, `wording` | `subject_id`, `choices`, `recorded_at` |
| `GET /api/consent/{subject_id}` | - | `subject_id`, `choices` |
| `POST /api/marketing-views` | `subject_id`, `route` | the recorded view, or a refusal without measurement consent |
| `GET /api/workspaces` | - | `id`, `name`, `plan_key`, `relation` |
| `GET /api/workspaces/{ws}/members` | - | `account_id`, `email`, `display_name`, `relation` |
| `DELETE /api/workspaces/{ws}/members/{account_id}` | - | an empty success |
| `GET /api/workspaces/{ws}/invitations` | - | `id`, `email`, `state` |
| `POST /api/workspaces/{ws}/invitations` | `email` | `id`, `email`, `state`, `token` |
| `DELETE /api/workspaces/{ws}/invitations/{id}` | - | an empty success |
| `POST /api/invitations/{token}/accept` | - | `workspace_id`, `relation` |
| `GET /api/workspaces/{ws}/subscription` | - | `plan_key`, `billing_period`, `seats`, `seats_used`, `current_period_start`, `current_period_end` |
| `POST /api/workspaces/{ws}/subscription` | `plan_key`, `billing_period` | the subscription |
| `GET /api/workspaces/{ws}/charges` | - | `kind`, `plan_key`, `seats`, `amount_cents`, `currency`, `period_start`, `period_end`, `created_at` |
| `GET /api/workspaces/{ws}/usage` | - | `meter`, `used`, `limit`, `period`, `window_start`, `window_end` |
| `GET /api/workspaces/{ws}/blocks` | - | the workspace's saved blocks |
| `POST /api/workspaces/{ws}/blocks` | `name`, `category`, `parameter_schema`, `source` | the block with `id`, `version` |
| `PUT /api/workspaces/{ws}/blocks/{id}` | `name`, `category`, `parameter_schema`, `source` | the block with its new `version` |
| `DELETE /api/workspaces/{ws}/blocks/{id}` | - | an empty success |
| `GET /api/workspaces/{ws}/blocks/{id}/versions` | - | `version`, `parameter_schema`, `source`, `created_at` |
| `GET /api/workspaces/{ws}/favorites` | - | `id`, `block_id`, `template_uuid` |
| `POST /api/workspaces/{ws}/favorites` | `block_id` or `template_uuid` | the favourite |
| `DELETE /api/workspaces/{ws}/favorites/{id}` | - | an empty success |
| `GET /api/workspaces/{ws}/brand-kits` | - | `id`, `name`, `colours`, `fonts` |
| `POST /api/workspaces/{ws}/brand-kits` | `name`, `colours`, `fonts` | the kit |
| `DELETE /api/workspaces/{ws}/brand-kits/{id}` | - | an empty success |
| `POST /api/workspaces/{ws}/assets` | multipart `file` | `id`, `object_key`, `content_type`, `byte_size` |
| `GET /api/workspaces/{ws}/assets` | - | `id`, `filename`, `object_key`, `content_type`, `byte_size` |
| `GET /api/workspaces/{ws}/assets/{id}/content` | - | the stored bytes |
| `DELETE /api/workspaces/{ws}/assets/{id}` | - | an empty success |
| `GET /api/workspaces/{ws}/projects` | - | `id`, `name`, `revision`, `approval_status`, `updated_at` |
| `POST /api/workspaces/{ws}/projects` | `name`, `canvas_width`, `canvas_height`, `fps`, `duration_ms` | the project with `id`, `revision` |
| `GET /api/workspaces/{ws}/projects/{id}` | - | the project with `timeline`, `revision`, `remixed_from`, `approval_status`, `superseded_shares` |
| `PATCH /api/workspaces/{ws}/projects/{id}` | `name`, `superseded_shares`, `brand_kit_id` | the project |
| `PUT /api/workspaces/{ws}/projects/{id}/timeline` | `base_revision`, `timeline` | the project at its new `revision`, or a conflict carrying `revision` |
| `POST /api/workspaces/{ws}/templates/{uuid}/remix` | - | the new project |
| `POST /api/workspaces/{ws}/projects/{id}/describe` | `prompt` | the new project |
| `GET /api/workspaces/{ws}/projects/{id}/versions` | - | `id`, `number`, `project_revision`, `approval_state`, `created_at` |
| `POST /api/workspaces/{ws}/projects/{id}/versions` | - | the version |
| `GET /api/workspaces/{ws}/versions/{vid}` | - | the version with `timeline`, `approval_state` |
| `POST /api/workspaces/{ws}/versions/{vid}/exports` | `format`, `width`, `height`, `fps`, `request_key` | `id`, `status`, `progress`, `watermarked`, `is_variation` |
| `GET /api/workspaces/{ws}/versions/{vid}/exports` | - | the version's export jobs, each with the fields of a single job |
| `GET /api/workspaces/{ws}/exports/{eid}` | - | `id`, `request_key`, `status`, `progress`, `queue_position`, `watermarked`, `is_variation`, `object_key`, `byte_size`, `failure_reason`, `message` |
| `PATCH /api/workspaces/{ws}/exports/{eid}` | `progress` | the job |
| `PUT /api/workspaces/{ws}/exports/{eid}/file` | the file bytes | the job at `ready`, or at `failed` with `failure_reason` |
| `POST /api/workspaces/{ws}/exports/{eid}/fail` | `reason` | the job at `failed` |
| `GET /api/workspaces/{ws}/exports/{eid}/file` | - | the stored bytes |
| `POST /api/workspaces/{ws}/versions/{vid}/shares` | `expires_at`, `passphrase`, `allow_download`, `allow_comments`, `recipients` | `id`, `token`, `url`, `message` |
| `GET /api/workspaces/{ws}/shares` | - | `id`, `token`, `version_id`, `state`, `allow_download`, `allow_comments` |
| `DELETE /api/workspaces/{ws}/shares/{sid}` | - | an empty success |
| `GET /api/workspaces/{ws}/shares/{sid}/views` | - | `route`, `viewer_email`, `viewed_at` |
| `GET /api/shares/{token}` | - | `project_name`, `version_number`, `allow_download`, `allow_comments`, `superseded`, `message` |
| `POST /api/shares/{token}/unlock` | `passphrase` | `access_token` |
| `GET /api/shares/{token}/stream` | `access` | the file, inline |
| `GET /api/shares/{token}/download` | `access` | the file, as an attachment |
| `GET /api/shares/{token}/comments` | `access` | `at_ms`, `body`, `author_email`, `state` |
| `POST /api/shares/{token}/comments` | `at_ms`, `body` | the comment |
| `GET /api/workspaces/{ws}/versions/{vid}/comments` | - | `id`, `at_ms`, `body`, `author_email`, `state`, `note` |
| `POST /api/workspaces/{ws}/versions/{vid}/comments` | `at_ms`, `body` | the comment |
| `POST /api/workspaces/{ws}/versions/{vid}/approval-requests` | `reviewer_emails` | `approval_state`, `waiting_on`, `message` |
| `GET /api/workspaces/{ws}/versions/{vid}/approval-requests` | - | `id`, `reviewer_email`, `state`, `decided_at`, `invite_url` |
| `GET /api/reviews` | - | `id`, `version_id`, `project_name`, `version_number`, `state` |
| `GET /api/reviews/{rid}` | - | the request with its version |
| `GET /api/reviews/{rid}/stream` | - | the version's file, inline |
| `POST /api/reviews/{rid}/decision` | `decision`, `note` | the request with its `state` |
| `POST /api/review-invites/{token}/accept` | `password`, `display_name` | `access_token`, `role` |
| `GET /api/notifications` | - | `id`, `kind`, `body`, `created_at` |

Bearer auth is required on everything except `GET /api/health`, `GET /api/plans`, the library,
template, creator, blog and customer reads, both auth endpoints, `POST /api/contact`, the consent and
marketing-view endpoints, the review-invite acceptance, and the share endpoints, which apply the share
rules instead.

**No mocks.** MinIO is the only place an uploaded asset or an exported file exists, and PostgreSQL is
the only place the app's records exist. An in-memory list of uploads, a base64 string in a database
column, a file written under the app's own directory, a placeholder file shipped with the app, a
presigned object-store address handed to a browser, a usage counter kept in process memory, or a media
route that answers with bytes it generated on the spot are all the same failure in different clothes.
The named provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger can sign up, remix a template, tune its blocks, export a version, share it and have a
reviewer approve it, and every file involved lives in the object store. Two members spending the last
unit of an allowance at once never both succeed, a retried export is charged once, and a failed one
costs nothing. A share with downloads off cannot be downloaded from any route, and a reviewer sees
only the version sent to them.
