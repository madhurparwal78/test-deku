# Thirty

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, read the marketing site,
sign in as a sales rep, move a deal across the opportunities board and watch the lane totals
recount, and read that same change back on the record's timeline with their name and the time on
it, without hitting an error page.

A different stranger, signed in as the other sales rep, must NOT be able to reach a company row
they do not own by any means: not in the table, not in a lane total, not in a dashboard number,
not in search, not in an export, and not through the keyed interface. When a workflow sends
notice of that change, the message must exist as a real message in the Mailpit inbox of exactly
the addressed person; a confirmation the app draws for itself is not a sent message.

## Overview

Thirty is a customer relationship platform whose shape is data rather than code. A workspace
starts with the usual nouns, Companies, People, Opportunities, Tasks, Notes, Dashboards and
Workflows, but none of them is a hard-coded screen: every one is a row in a metadata store, and
an administrator creates, renames and deletes objects, fields, relations and views at runtime
while the team keeps working. Add an object and the product grows a rail entry, a table, record
pages, search coverage, a permission surface and a programmatic resource for it at once.

The product is sold by a public marketing site at the same address: a landing page, a product
tour, pricing, customer stories, partners, an apps marketplace, release notes, a positioning
essay, the legal pages and a halftone image generator. The site's trick, and the build's, is that
every product picture on it is the platform's own component running seeded fixtures. The
companies table in the hero assembles itself row by row because it is the real table. The
opportunities board deals its own cards because it is the real board.

Two kinds of person use it. Administrators shape the workspace: the schema, the views, the roles
and row rules, the workflows, the keys and the plan. Members live in the records the shape
produces, and see only what the rules allow them to see.

It deliberately is not several things. There is no real electronic mail provider, no real single
sign-on identity provider, no real language model, no analytics endpoint and no payment
processor: billing is stateful and simulated, and the identity integrations are stored
configuration behind an interface. It ships no image, font or video file at all. There is no
native application and no offline mode.

The genuinely hard part is that nothing may ever be quietly stranded or quietly leaked: a schema
change must name every view, filter, workflow trigger and permission rule that depends on what it
is about to alter before it lands, and one permission answer about a row must be the same answer
at every door in the product.

## User roles

| Role | Can read | Can write |
|---|---|---|
| `owner` | everything an admin can read, plus billing, plan state and seat counts | everything an admin can write, plus the plan, the seats and the transfer of ownership. **Cannot** read or write another workspace, and **cannot** exempt itself from an audit entry |
| `admin` | all records regardless of row rules, the schema, all views, roles, permission rules, workflows, keys, apps and import batches | objects, fields, relations, views, roles and permission rules, workflows, apps, keys and imports. **Cannot** change the plan, the seats or billing, and **cannot** delete the audit trail |
| `member` | only the records the permission rules admit, through every path without exception | records they are admitted to create or update, their own private views, their own notes and tasks. **Cannot** create, rename or delete any object, field, relation or permission rule; **cannot** read or issue a key; **cannot** see another member's private view; **cannot** reach any settings surface except their own security settings |

Custom roles are not a fourth name in this list. An administrator builds one at runtime from
grants, read, create, update and delete, taken per object, plus field-level read masks, and
assigns it to a membership. A custom role can never grant more than the administrator who built
it holds.

Three actors in the workspace are not people, and every one of them is attributed by name on
every row it touches and every entry it writes: a key acting under its own identity, a workflow
acting under the workflow's name, and an installed app acting under the app's name. A fourth,
`System`, covers seeding. A created-by cell and an audit entry must render the actor kind
honestly, never flattening a robot into the person who configured it.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `member` session to any `admin`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Signup is closed. There is no public registration form anywhere in the product; an administrator
invites a person by electronic mail and that invitation is the only way a membership is created.
The following accounts are seeded, and every one of them signs in with the password
`deku-demo-pw-2026`:

| Email | Role | What it holds |
|---|---|---|
| `owner@example.com` | owner | owns the workspace and the plan |
| `admin@example.com` | admin | owns no records; shapes everything |
| `member@example.com` | member | account owner of five seeded companies |
| `member2@example.com` | member | account owner of the other four |

The two members are the visibility boundary the whole product is measured against: a seeded rule
on Companies binds a row to its account owner, so each of them sees their own companies and never
the other's, everywhere.

## Core features

### Auth and identity

Accounts sign in with an electronic mail address and a password, and the app issues a bearer
token the client sends on every request after that. Passwords are stored hashed, never
recoverable. A token expires and an expired token is refused.

1. A sign-in with the right address and the right password succeeds and returns a token. A
   sign-in with the right address and a wrong password is denied, and the response must not
   reveal whether the address exists.
2. A second factor is enrolled from the security settings. Once enrolled, a correct password
   alone does not produce a session: the app asks for a code and issues the token only when the
   code is right. A wrong or expired code is denied and leaves no session behind.
3. Signup is closed: a request that tries to create an account without an invitation is denied,
   and no membership row is written.
4. Removing a member, shrinking a role or disabling a key takes effect on sessions that are
   already open, within a second. A person removed while reading a table must be refused on their
   next request; a session that keeps working because the client cached the old answer is the
   failure this rule exists to close.
5. Single sign-on and directory provisioning exist as stored configuration on the Organization
   plan and above, and they are inert: the configuration is saved, shown back and clearly marked
   as awaiting a provider. An app that claims a federated sign-in succeeded without one is wrong.

### The marketing site

Twelve public addresses plus a not-found page, all reachable without a session, all carrying the
site's chrome.

1. The header carries the logo tile, then Product, Resources as a dropdown, Customers and Pricing,
   then two count chips reading `55.9K` and `7.2K`, then `Log in` and `Get started`. It stays
   at the top of the page as the page scrolls. On a narrow screen the centre links fold into a
   menu sheet and `Get started` stays visible.
2. The footer carries four columns. Sitemap: Home, Product, Pricing, Customers, Partners, Why
   Thirty. Help: Developers, User Guide, Release Notes, Halftone generator. Legal: Privacy
   Policy, Terms and Conditions, Trust Center. Connect: LinkedIn. Beside them sit `Talk to us`,
   `Get started`, the line `(C) 2026 - Thirty`, and a language selector reading `English`.
3. A terms page at `/terms` and a privacy page at `/privacy-policy` are reachable from the footer
   of every page, including from inside the workspace. The privacy page states what the workspace
   records about a person and how long an archived row is kept before it is purged. The terms page
   is also linked from the invitation acceptance form, and a person cannot accept an invitation
   without that link being present on the form.
4. The landing page carries eight bands in this order: the hero; the trusted-by logo bar; the
   Problem band; the Solution band; the go-to-market band; the in-production case tiles; the
   testimonial slider; and the closing question band above the footer.
5. The hero reads `Build your Enterprise CRM at AI Speed` in the display voice over a halftone
   field, with the standfirst `Thirty gives technical teams the building blocks for a custom CRM
   that meets complex business needs and quickly adapts as the business evolves.` and the two
   actions `Get started` and `Talk to us`. Below it sits the product window holding the companies
   table, with the AI build session window overlapping its corner.
6. The logo bar reads `trusted by`, then ten fully desaturated wordmarks set as text, then
   `+10k others`.
7. The Problem band reads `The Problem.` beside `A custom CRM gives your org an edge, but
   building one comes with tradeoffs`, and names two tradeoffs: `The Giant Monolith - Proprietary
   languages, slow deployment cycles, and "black box" logic.` and `The In-house Burden - It's
   fragile. V1 ships quickly, but maintaining and making changes is a long term burden.`
8. The Solution band reads `Stop settling for trade-offs.` above `Assemble, iterate and adapt a
   robust CRM, that's quick to flex` and `Compose your CRM and internal apps with a single
   extensibility toolkit.`, then three pull cards, `Production grade quality`, `AI for rapid
   iterations` and `Control without drag`, each linking to its case page, then the numbered
   triptych `01 Begin with production-grade building blocks`, `02 Continue iteration without
   friction` and `03 Stay in control with our open-source software`.
9. The go-to-market band reads `Skip the clunky UX that always comes with custom.` above `Make
   your GTM team happy with a CRM they'll love` and carries three mock plates:
   `Familiar, modern interface` with the line `Thirty makes it simple. It's clean, intuitive, and
   built to feel like Notion.`; `Live data and AI built` with `Everything updates in real time,
   with AI chat always ready to help you move faster.`; and `Fast path to action` with `Smart
   patterns, shortcuts, and layouts make everyday tasks faster and easier to execute.`
10. The in-production band reads `Dev teams power company-wide change with Thirty` and carries
    three case tiles, each closing with `Read the case`.
11. The testimonial slider carries three quotations in the display voice with an author plate and
    a pager reading the current position out of three: the flexibility quotation, the foundation
    quotation and the interface quotation, each attributed to a fictional speaker.
12. The closing band is the FAQ, and its seven questions and their answers appear verbatim on
    every marketing page. It reads `Any Questions?` and `Stop fighting custom. Start building, with
    Thirty`, above seven disclosure rows that open one at a time: whether Thirty is really open
    source; how long it takes to get started; whether a team can migrate from Salesforce or
    HubSpot; whether customising needs a developer; whether developers can extend it with code;
    whether it works with Claude, ChatGPT and Cursor; and what Thirty costs. The answers name the
    thirty-day trial, the four-hour onboarding packs, going live in one to two weeks, CSV and the
    keyed interface for fifty thousand records and above, the scaffold command
    `npx create-thirty-app`, a per-workspace connector for assistants, and the two per-seat prices.
13. The product page reads `A CRM for teams that move fast` over the same live companies table,
    then the fast-workspace trio, `Fly through your workspace with shortcuts and short load
    times.`, `See updates as they happen. Work with your team and agents seamlessly.` and `AI
    chat, settings, and records in a side panels for fast, single-screen access.`, then the
    no-code band reading `Customization`, `Go the extra mile with no-code` and `Need a quick
    change? Skip the engineering ticket. Customize your workspace in minutes.` beside the schema
    graph, with the numbered rail opening `01 Data model - Add objects and fields`, then bands for
    views, permissions, workflows and the AI surfaces, then the shared question band and footer.
14. The schema graph on that page is not a drawing. It renders from the same metadata store the
    workspace uses, seeded with `People` at 840 records and 22 fields, `Companies` at 120 records
    and 39 fields, `Opportunities` at 64 records and 11 fields, `Employment History` at 48 records
    and 8 fields, and `Demos` at 45 records, with relation lines drawn between them. Create an
    object in the workspace and this graph gains it.
15. The customers index reads `See how teams build on Thirty` above the trusted-by band and a
    mixed grid of quotation-led plates and summary tiles, and it closes with `Ready to build your
    own story?`. The metric pairs are pinned: `150 hrs` saved per month, `2,000+` daily messages,
    a `Q1 2026` record quarter, an AI-assisted Salesforce migration, self-hosted full ownership,
    `3` product lines on a single CRM, no-code customizations, `90%+` lower CRM cost, zero manual
    work at the core, `1 click` proposal automation, `4` tools connected through the keyed
    interface, and API-first tool integration.
16. Four case pages open from that index, each carrying a title, a category chip, a read-time
    chip, the metric band, a body in a narrow reading column, pull quotations and the closing
    actions: the real estate agency built around its messaging channel, the consulting firm that
    made the platform its integration backbone, the agribusiness with the modular setup, and the
    education group that escaped a vendor shutdown.
17. The partners page reads `Find a Thirty Partner` and lists certified implementation partners
    as cards carrying a region chip, a speciality chip and an outbound link.
18. The apps page reads `Marketplace` above `Apps for Thirty`, with the filter chips `All`,
    `Enrichment`, `Productivity` and `Search`, and four vetted app cards each carrying a category
    chip, a description, `Install` and `Learn more`: `Findable`, a structured web search connector
    for agents, under Search; `Call Recorder` under Productivity; `Last contact` under
    Productivity; and `Enrich Labs`, which enriches People and Companies, under Enrichment.
    `Install` leads into the workspace install flow.
19. The releases page reads `Latest Releases` above `Discover the newest features and
    improvements in Thirty, the #1 Open Source CRM.` with a `Technical notes` chip and dated
    entries in the reading column, over a halftone cover plate.
20. The why page carries a positioning essay in the reading column at `/why-thirty`. The privacy
    policy and the terms of service are dated documents in the same column.
21. Any address that matches no route renders the product's own not-found page, reading
    `404: This page could not be found.` in the site's own treatment, carrying a way back to the
    landing page, and answering as not found rather than as success.
22. Every internal link on every public page resolves to a page that exists. A link in the header,
    the footer, a band or a card that answers as not found is a defect.

### Live product mocks

Every product picture on the marketing site is the platform's own component running a seeded
fixture with a driver that plays its behaviour. None of them is an image, a video or a recording.

1. The companies table mock is the real table view rendering the nine-company fixture across
   thirteen columns: `Companies`, `Url`, `Created By`, `Address`, `Account Owner`, `ICP`, `ARR`,
   `Linkedin`, `Industry`, `Main contact`, `Employees`, `Opportunities`, `Added`. Its rail reads
   Favorites with `Sales Dashboard` and Workspace with Companies, People, Opportunities, Tasks,
   Notes, Dashboards, Workflows and `Book a demo`. Its view bar reads `All Companies - 9` beside
   Filter, Sort and Options.
2. The nine seeded companies are pinned exactly: `Arcadia Labs` at `arcadialabs.ai`, ICP true,
   `$500,000` ARR, AI Research, 612 employees, the Enterprise Expansion opportunity, added
   `Jul 1, 2023`; `Meshwork` at `meshwork.com`, ICP false, `$1,000,000`, Professional Networking,
   19,300 employees, Talent Outreach, `Jul 3, 2023`; `Chatterbox` at `chatterbox.com`, ICP true,
   `$2,300,000`, Collaboration Software, 4,500 employees, Workspace Renewal, `Jul 5, 2023`;
   `Papertrail` at `papertrail.com`, ICP false, `$750,000`, Productivity Software, 620 employees,
   Workspace Consolidation, `Jul 8, 2023`; `Pixelforge` at `pixelforge.com`, ICP true,
   `$3,500,000`, Design Tools, 1,300 employees, AI Prototyping and Design Ops, `Jul 12, 2023`;
   `Codeharbor` at `codeharbor.com`, ICP true, `$900,000`, Developer Platform, 3,800 employees,
   Copilot Rollout, `Jul 14, 2023`; `Wanderstay` at `wanderstay.com`, ICP true, `$4,200,000`,
   Travel, 6,900 employees, Host Ops, `Jul 15, 2023`; `Ledgerline` at `ledgerline.com`, ICP true,
   `$1,800,000`, Payments, 7,400 employees, Billing Expansion, `Jul 17, 2023`; and
   `Quartz Capital` at `quartzcap.com`, ICP false, `$6,000,000`, Venture Capital, 1,100 employees,
   Fund Ops, `Jul 20, 2023`.
3. The created-by column of that fixture mixes actor kinds on purpose: people, one actor named for
   an API key, one named for a workflow, and `System`. Every row keeps a street address, an
   account owner and a main contact drawn as people with initials.
4. The kanban mock is the real board, headed `All opportunities 9`, `Identified 3` and
   `Qualified 1`, carrying the cards `Codeharbor $6,562.04 OPP-1`, `Pixelforge $6,562.04 OPP-2`,
   `Wanderstay $2,433.89 OPP-8` and `Papertrail $2,650 OPP-6` with the chip `New`, each with an
   owner avatar and a date. It shimmers skeleton cards before the real ones arrive, drags one card
   between lanes on a loop with a named collaborator's cursor arriving beside it, and throws
   confetti when a deal closes.
5. The filtered-table mock carries the removable chips `Type is Customer` and `Employees > 500`.
6. The palette mock opens over the table, types its query with a caret, walks the results and
   executes one. Its rows are pinned: a Record Selection group with `Send email`, `Export
   selection as CSV` and `Delete 8 records`; an object group with `Import data` and `Create
   company`; a Navigate group with `Go to People` on `G then P`, `Go to Opportunities` on
   `G then O` and `Go to settings` on `G then S`; and a Settings group with `Switch to dark mode`.
7. The AI build session mock replays a scripted fixture: an editor window streaming five file
   diffs beside a chat pane whose steps arrive one after another and end in a summary chip, with a
   terminal line typing itself. Its prompt is pinned: `Scaffold a launch-ops CRM in my workspace
   with rockets, launches, payloads, customers, and launch sites, with relevant actions for each.`
   The diffs cover a schema identifiers file, a launch object, a payload object, a rocket object,
   an upcoming-launches view and an integration test, each with its added-line count.
8. The workflow mock raises its nodes, fades in their ports, draws its edges along their length
   and fades the branch labels last. The schema graph band raises object cards on a dark dotted
   ground, draws relation lines and pops a filter chip away. The live-data band raises rows, sweeps
   a highlight across a rail item and raises the dashboard widgets. The record page mock arrives
   top to bottom: header, field rows, relations, tab bar, timeline.
9. Each mock arms when it is scrolled into view and plays once. Under a reduced-motion preference
   every mock renders in its finished state, with no loop, no drag and no confetti.

### The halftone generator

A full-screen ink tool at `/halftone`, and the source of every illustration on the site.

1. The left side renders a three-dimensional scene as horizontal dashed strokes whose length and
   density carry the tone, drawn in the ink grey or the brand blue. The header line reads
   `Idle auto-rotate is active` and the scene turns slowly by itself.
2. The right side is a control rail with the tabs `Design`, `Animations` and `Export`. Design
   holds five groups. Source offers Torus Knot, Sphere, Torus, Icosahedron, Box, Cone, Cylinder,
   Octahedron, Dodecahedron, Tetrahedron, Sun Coin, Lotus Coin, Arrow Target and Dollar Coin,
   plus the brand image and a file upload. Visualization holds a camera distance. Lighting holds a
   key light, a fill, an ambient level, an angle and a height. Material offers Solid or Glass with
   a roughness and a metalness. Halftone chooses whether the dashes describe the light areas or
   the dark ones, and holds a dash scale, a power and a width. Colors sets the dash colour, which
   starts at the brand blue, and the background.
3. Moving any control updates the render while the control is moving, not after it is released.
4. The Animations tab drives turntable presets. The Export tab renders the current frame, or a
   sequence, to a file the browser downloads.
5. Under a reduced-motion preference the scene renders still and the idle rotation does not start.
6. The site's own plates, the hero field, the band plates and the release cover, are produced by
   this same generator when the application is built. No halftone plate is a stored image file.

### Pricing and plan gating

1. The pricing page reads `Simple Pricing` above `Start your free trial today without credit
   card.`, with a Monthly and Yearly toggle carrying a `-25%` chip, and a `Selfhosting` tab.
2. Three plan cards are pinned. `Pro` at `$9` per user per month: Full customization; Create
   custom apps; AI Agents with custom skills; 50 workflow credits per year included; Standard
   support. `Organization` at `$19` per user per month: Everything in Pro; Row-level permissions;
   SAML/OIDC SSO; Custom domain; Priority support. `Enterprise` from `$50k` per year: Everything
   in Organization; Single-tenant isolation; IP allow-listing; SCIM provisioning; Dedicated
   support and SLA. The first two carry `Start for free` and the third carries `Talk to sales`.
3. Switching to Yearly reprices every card by the same twenty-five percent saving, computed once
   from one source and never restated as a second hardcoded figure.
4. A partners cross-sell reads `Need help with customization?` below the cards.
5. The comparison matrix lists every row in groups that open one at a time: Price and Seats limit;
   Workspace with custom objects, fields, views, the view types `Table, Kanban, Calendar`, layout,
   records, CSV import and export and languages at 30 and above; Reports; Emails and Calendar; AI
   and Automations; and Security with two-factor authentication and its kin.
6. Every row of that matrix is a real gate read from the workspace's plan state, not a marketing
   claim. Row-level permission rules, single sign-on configuration and a custom domain exist to be
   configured only on Organization and above: on Pro the surfaces are absent, and a direct request
   to create a row rule on a Pro workspace is denied and writes nothing.
7. Two-factor authentication is available on every plan.
8. Seats follow membership: inviting a member raises the seat count, removing one lowers it, and
   the billing page reads the same number the roles page does.
9. A downgrade locks above-plan configuration, it never deletes it. A row rule written on
   Organization survives a downgrade to Pro as a stored, clearly labelled, inert rule, and it stops
   filtering. Restoring the plan restores its effect with no re-entry.

### The workspace shell

1. The rail carries the workspace switcher with its logo tile and name, a search control, panel
   toggles, a `New chat` action, a Favorites group holding pinned views and records, a Workspace
   group listing every active object, and the utility entries.
2. The Workspace group is a live mirror of the metadata store, not a coded menu. Creating,
   renaming, hiding or reordering an object in settings changes the rail for every signed-in
   member within a second, without anyone reloading a page.
3. The main pane carries the object header with its icon, its name, its New control and the
   palette chip, then the view bar with the view name, the record count and the view switcher
   beside Filter, Sort and Options, then the view body.
4. A right side panel hosts the AI chat, settings and a record preview without leaving the current
   screen.

### The metadata engine

This is the centre of the product. Objects, fields, relations and views are rows, and the rest of
the product reads them.

1. An administrator creates an object by giving a singular label, a plural label and an icon. The
   moment it is saved it exists end to end: a rail entry, a table view with the system columns,
   record pages, inclusion in search, a permission surface, and an addressable resource in the
   keyed interface. A product that requires a restart, a migration step or a redeploy before any
   one of those appears has not built the engine.
2. The field types are at least: text, number, currency in integer minor units, date, date and
   time, boolean, single select, multi select, rating, links, electronic mail addresses, phone
   numbers, address, and relation. Select options carry a colour drawn from the accent set.
3. A relation is created once, as a one-to-many or many-to-one pair, and is visible and navigable
   from both sides immediately. Deleting one side archives the pair together; leaving a half
   relation pointing at nothing is a defect.
4. Renaming a field preserves every stored value. A rename that empties a column is a failure,
   not a cosmetic change.
5. Changing a field's type converts every value where the conversion is lossless and refuses the
   change where it is not, naming the count of rows that block it. Converting a text field whose
   rows include values that are not numbers into a number field must refuse and must state how
   many rows are in the way; it must not silently blank them and must not partially convert.
6. Deleting an object or a field soft-hides it for thirty days before it is purged, and it stays
   restorable for that whole window.
7. No mutation may strand a dependent. Before a change lands, the product lists every view,
   filter, sort, workflow trigger, workflow action and permission rule that references what is
   about to change, and the change either cascades through them or is blocked, exactly as the
   listed plan said it would. A view left pointing at a field that no longer exists, a workflow
   whose trigger silently never fires again, or a permission rule that quietly stops filtering are
   each the failure this rule exists to prevent.
8. Two administrators editing the schema at the same time converge without corrupting the store.
   Where both change the same piece of metadata, exactly one succeeds; the other is told its view
   of the metadata was stale and is offered the change again against the current version. Both
   edits silently landing, or the later one overwriting the earlier with no notice, is the defect.
9. A member working in a view while the schema changes under them sees the change applied in
   place. The view must not crash, must not blank, and must not need a reload.
10. The starter set, Companies, People, Opportunities, Tasks, Notes, Dashboards and Workflows,
    ships as seeded metadata and seeded rows, not as hard-coded screens. Deleting a seeded object
    must behave exactly as deleting one an administrator created.

### The table view

1. The table has a sticky header row carrying a type glyph per column, a checkbox column, a New
   row affordance at the end and a summary footer. The header stays visible while the body
   scrolls.
2. Cells render by type, not by convention: a company cell carries a drawn logo chip beside the
   name; a link cell renders as a small pill with a drawn site mark; a person cell carries an
   avatar chip; a boolean shows a check or a cross paired with its word; currency is right aligned
   with thousands separators; a select renders as a coloured chip paired with its label; a
   relation renders as a stack of chips with a count for the overflow.
3. Any cell edits in place. Entry is by keyboard, Escape abandons the edit and leaves the stored
   value alone, Enter commits it. A currency or number cell refuses a value that is not a number at
   the cell, before anything is stored, and says which field is wrong.
4. **A committed cell edit is the persisted truth.** The value shown in the cell after a commit
   must be the value stored, and reloading the page, opening the record page or reading the same
   record through the keyed interface must return that same value. A cell that shows a new value
   while the store still holds the old one, or that reverts on reload, is the single most important
   failure in this product.
5. Ten thousand rows in one view scroll smoothly with the header in place and without a row
   tearing, shearing or rendering blank as it arrives. Drawing only what is on screen is expected;
   how is yours.
6. Columns resize, reorder by dragging, hide and pin to the left, and every one of those choices
   persists for that person on that view across a sign-out and back.
7. Rows multi-select, including a shift-held range, and the selection drives the bulk actions:
   delete to the bin, export the selection, and edit one field across the selection. A bulk edit is
   one audited act and one undo, never one entry per row.
8. Sort and filter state renders in the view bar as removable chips, and removing a chip restores
   the rows it was hiding.
9. While one person is typing in a cell, another person's edit to a different cell of the same row
   arrives in the visible row without stealing the caret and without losing a keystroke. Where both
   people commit to the very same cell, the later commit is the stored value, the earlier writer is
   told their value was replaced, the cell flashes, and an audit entry records both. Neither side
   may be overwritten silently, and redrawing the whole row so the caret is lost is a failure.
10. The created-by cell renders the actor honestly, including when the creator was a key, a
    workflow or an installed app rather than a person.

### Kanban and calendar

1. Any object carrying a single-select field can be presented as a board grouped by it. Lanes
   carry a count and, where the object has a currency field, a lane total.
2. A card carries the record title, a company chip, an amount, a date, an owner avatar and the
   record's own short code in the style of `OPP-1`.
3. Dragging a card into another lane writes the underlying field, and the move appears on the
   record's timeline as an attributed transition. Both the source and the destination lane totals
   recount as the card lands; a total that only refreshes on reload is wrong.
4. Each lane carries its own New control, and lanes collapse.
5. The calendar renders date-bearing objects by day. Dragging an entry to another day re-dates the
   record, and the change is attributed like any other.
6. Each object holds named views, each with its own filters, sorts, visible columns and grouping.
   A view is either private to the person who made it or shared across the workspace, and a
   private view is invisible to everyone else including an administrator's view list.
7. Favouriting a view or a record pins it to the Favorites group in the rail for that person only.

### The record page and timeline

1. The left side is the record card: a header with the icon or drawn logo, the name and the quick
   actions, then field rows grouped and editable in place, then relation sections listing related
   records as chips with add and detach controls.
2. The right side is a set of tabs. Timeline carries every field change, note, task, message and
   workflow touch as an entry with its actor and its age. Notes carries rich text cards. Tasks
   carries checkable items with an assignee and a due date. Emails and Calendar carries threads
   and events fed from fixtures behind an interface. Files carries attachments.
3. The timeline is not a second log. It is a projection of the same event stream the audit trail
   reads, so an entry that appears in one must appear in the other with the same actor and the
   same time.
4. A field edit made by one person in the table appears on another person's open record page
   within a second, attributed to whoever made it, without a reload.

### Search, filters and the command palette

1. The palette opens from a keyboard shortcut anywhere in the workspace and from the search chip.
   It offers type-ahead across records, objects, views and actions, with results grouped by kind.
2. Two-key navigation sequences work from anywhere in the workspace, are listed in the palette,
   and never fire while the person is typing in a text input.
3. The filter builder offers operators that belong to the field's type: is and is not for a
   select, contains for text, greater than for a number, in future for a date, and empty for
   anything. Several conditions combine with and-logic, and the built filter saves into a view.
4. Full-text search spans every object with per-object grouping.
5. Search, its result counts and anything exported from it obey the row rules exactly. A row a
   member may not see never appears in their search results, never contributes to a count they can
   read, and never lands in a file they export.

### Workflows

1. A workflow is a graph. Trigger nodes are: a record created; a record updated in a way that
   matches a filter; a record deleted; a schedule; and a manual run from the palette. Action nodes
   are: create or update a record; send an electronic mail message; enqueue an agent step; and call
   an outbound web request with a signed payload. Branch nodes carry conditions.
2. Every run is durable and audited. The run records its trigger, and each node records its input,
   its output and its outcome, all readable in a run history. A node that fails marks the run
   failed and stores the error. A retry is an explicit act that is recorded as a retry; nothing
   retries itself into a duplicate.
3. **Exactly one run per workflow per triggering event.** A single record update that matches two
   workflows starts both, once each. The same update must never start the same workflow twice,
   however many surfaces observed it.
4. A workflow that edits the object it is triggered by must not chase itself: a depth limit halts
   the chain and writes a visible halt entry into the run history naming why it stopped. An
   unbounded cascade is a failure even when every individual run looks correct.
5. Editing a workflow creates a new version. Runs already in flight finish on the version they
   started on, and the run history says which version each run used.
6. Workflow credits are counted per run and checked at the gate against the plan, with a visible
   meter. A run attempted past the allowance is refused with a reason and consumes nothing.
7. The electronic mail action sends over real SMTP. The message is addressed to exactly the
   address the node resolved, with no carbon copy and no blind carbon copy. Its subject begins with
   `Workflow:` followed by a space and the workflow's name, so a run of a workflow named
   `Stage change notice` produces the subject `Workflow: Stage change notice`. The body is not
   empty and names the record the run acted on.
8. A run that does not reach the message node sends nothing: a run halted by the cycle guard, a
   run refused at the credit gate, a run whose branch went the other way, and a dry run of a
   workflow that has not been activated each leave the inbox untouched.

### Permissions and audit

1. Roles grant, and rules restrict. A permission rule binds rows of an object to their owner, to a
   team, or to a filter, and it can mask named fields from reading.
2. One authority answers the question "may this actor see this row", and every read path asks it:
   the table, the board lanes and their totals, the calendar, the record page, search, every
   dashboard aggregate, every export and every read through the keyed interface, including reads a
   workflow makes. Two paths that disagree about one row is the defect this rule exists to close.
3. A request for a row a rule hides is answered as not found. It must not be answered as forbidden,
   because that confirms the row exists.
4. Aggregates are computed after the rows are filtered, never before. A hidden row must not move a
   visible count, a sum, a lane total or a dashboard number by any amount. Two members reading the
   same board or the same dashboard may honestly see different totals, and each total must
   reconcile exactly with the rows that member can list.
5. Hiding a row in the interface while the query behind it still returns the row is not a
   permission rule and does not satisfy any of the above.
6. A field mask holds on every path too: a masked field is absent from the record page, absent from
   the table, absent from the export file and absent from the keyed interface's response, not
   merely blanked in the browser.
7. The audit trail is append-only. It records schema changes, permission changes, sign-ins,
   exports and record mutations, each with its actor, whether that actor is a person, a key, a
   workflow or an app, its time, and the value before and after. It filters by actor and by object.
   Nothing in the product deletes or edits an entry.

### AI chat, scaffolding and apps

1. The chat panel answers questions it can compute from the workspace: counts, sums and lookups
   over the records the asker is allowed to see. Every answer names the records it read. A question
   it cannot answer from the data gets an honest refusal, never an invented figure.
2. The chat obeys the row rules like every other read path: it must not compute a sum over a row
   the asker cannot see, and it must not cite one.
3. Create-with-AI inside the workspace scaffolds a described set of objects and fields through the
   real metadata engine, from a small grammar of templates, and marks everything it creates as a
   draft for a person to review before it is active.
4. Installing an app from the marketplace writes an app row carrying its name, its scopes and the
   objects and fields it adds, through the same metadata engine, and gives it its own actor
   identity. Every row it then touches is attributed to it.
5. Uninstalling an app archives its contributions reversibly. Reinstalling restores them.

### Import, export and the keyed interface

1. CSV import runs per object. The uploader detects the delimiter and the encoding, then shows a
   mapping table pairing each column with a field, previewing the type it will land as, and
   flagging the rows that will fail and why.
2. Duplicate handling is chosen before the import runs: skip the duplicate, or update the existing
   record matched on a chosen key.
3. A dry run reports the counts that would land without writing anything.
4. A committed import is one batch: one undo handle and one audit entry. Undoing it removes
   exactly the rows it created and restores exactly the values it changed, in one act.
5. Fifty thousand rows import with visible progress and complete.
6. Exporting a view produces exactly the rows and the columns that view shows to that person,
   with nothing hidden added back in. Exporting a selection exports the selection.
7. Keys are issued per workspace with scopes, shown once and never shown again, and revocable. A
   revoked key is refused on its next request.
8. Every object is addressable through the keyed interface the moment it exists, with list,
   filter, create, update and delete, all of them honouring the same permission answers the
   interface does.
9. Webhook subscriptions are made per object. Deliveries carry a signature and are retried on
   failure, and a retry is recorded rather than silently repeated.

### Dashboards

1. A dashboard is a record of the seeded Dashboards object holding a grid of widgets: a number, a
   bar, a line, a donut and a table snapshot, each over any object, each with its own filters and
   date range.
2. Widgets rearrange by dragging, and a dashboard favourites to the rail. The seeded
   `Sales Dashboard` is favourited for every seeded account.
3. Every widget's number is computed after the row rules are applied, so two people may correctly
   read different numbers from the same dashboard, and each person's number reconciles with the
   rows they can list.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | landing: hero with the live companies table and the AI build session, logo bar, Problem, Solution, go-to-market, cases, testimonials, questions | public |
| `/product` | feature tour: live table, the no-code band with the schema graph, views, permissions, workflow and AI bands | public |
| `/pricing` | three plans, the billing toggle, the full comparison matrix | public |
| `/customers` | case-study index with metric cards | public |
| `/customers/<case>` | the four case pages | public |
| `/partners` | certified partner directory | public |
| `/apps` | the vetted apps marketplace with its four filter chips | public |
| `/releases` | release notes index | public |
| `/why-thirty` | the positioning essay | public |
| `/halftone` | the halftone generator tool | public |
| `/privacy-policy` | what the workspace records and for how long | public |
| `/terms` | terms and conditions, also linked from the invitation form | public |
| `/login` | sign in, then the second factor when one is enrolled | public |
| `/workspace` | redirects to the first rail entry | session |
| `/workspace/o/<object>` | that object's default view | session |
| `/workspace/o/<object>/v/<view>` | a named view of that object | session |
| `/workspace/o/<object>/r/<record>` | the record page | session |
| `/workspace/search` | full results across every object | session |
| `/workspace/imports/<batch>` | an import batch, its mapping, its errors and its undo | session |
| `/workspace/settings/data-model` | objects, fields and relations | admin |
| `/workspace/settings/roles` | roles, custom roles and permission rules | admin |
| `/workspace/settings/views` | view configuration across objects | admin |
| `/workspace/settings/keys` | keys, scopes and webhook subscriptions | admin |
| `/workspace/settings/workspace` | workspace name, members and invitations | admin |
| `/workspace/settings/billing` | plan, seats and the credit meter | owner |
| `/workspace/settings/security` | password and the second factor, for the signed-in person | session |
| anything else | the product's own not-found page | public |

The command palette is not a route. It is a global overlay reachable from every workspace surface
by its keyboard shortcut and from the search chip, and it is the fastest path to every action in
this brief.

**Entry and redirects.** An unauthenticated request for any `/workspace` address lands on `/login`
and returns to the address that was asked for once the sign-in succeeds. When a second factor is
enrolled, the code is asked for before any session exists. Signing out returns to `/` and the old
token stops working immediately. A token that expires part way through an edit leaves the record
exactly as it was and returns the person to `/login`. A `member` who asks for an admin settings
address is refused rather than shown the page with its controls greyed out. A request for a record
a permission rule hides is answered as not found.

**Journeys.**

1. Sign in as `admin@example.com`. Open the data model studio, create an object, and watch the
   rail gain it in a second browser already signed in as `member@example.com`. Add a text field
   and a currency field, pair a relation to Companies, then delete a field that a saved view and a
   workflow trigger both use: read the list of dependents the product shows, confirm, and find
   both the view and the workflow changed exactly as the list said.
2. Sign in as `member@example.com`. Open Companies, filter to `Type is Customer`, sort by ARR,
   edit `Arcadia Labs` ARR in place, reload the page, and read the new value back from the cell,
   the record page and the keyed interface.
3. Open Opportunities as a board. Drag `OPP-1` from Identified to Qualified, watch both lane
   totals recount as it lands, then open the record and read the transition on the timeline with
   `member@example.com` and the time against it.
4. Open the palette, type `export`, choose `Export selection as CSV` and receive a file carrying
   exactly the rows and columns that view was showing.
5. Open Companies, choose Import data, upload a file, map its columns, read the rows flagged as
   failures with their reasons, run the dry run, commit, then undo the batch from
   `/workspace/imports/<batch>` and find the table exactly as it was.
6. Sign in as `member@example.com` and `member2@example.com` side by side. Compare the Companies
   table, the board lane totals, the `Sales Dashboard` numbers, a search for a company name and an
   export. Each surface shows each member only their own companies, and neither member can reach
   the other's row by asking for its address directly.
7. Sign in as `admin@example.com`, build a workflow that triggers on an Opportunity stage change
   and sends notice, run it, then read the run history: the trigger, each node's input, output and
   outcome, the version the run used, and the message in the addressed inbox.

**States.** Every list has an empty state that names what would fill it and offers the action that
would. Every page has a loading state, and the table's is a skeleton of rows rather than a spinner
over the whole screen. An error renders in place with a way back and never replaces the
application with a stack trace. A view whose object has been deleted says so plainly instead of
failing. A workspace with no dashboards, no workflows and no keys still renders those surfaces
with their empty states rather than a blank pane.

## UI/UX notes

Somebody arriving here should understand in one screen that this is a working instrument rather
than a picture of one, and that its shape is theirs to change. This is an operational product:
quiet, dense but organised, built for scanning and for the same action repeated all day. The
marketing shell is the only place atmosphere is allowed, and even there the first thing seen is
the product itself running.

Two stances govern every judgement, and a competing product could rationally hold either opposite.
**Ink and one blue over a palette**: meaning is carried by one near-black at different strengths,
and exactly one hue is allowed to be the brand. **Hairline over shadow**: separation comes from a
thin line and from space, and depth is spent only where something genuinely floats.

The ground is a pure near-white neutral. One near-black neutral carries text, borders and
dividers, stepped by transparency rather than by a second family, so the reading hierarchy is one
colour at several strengths and never a second grey family competing with it. One light, vivid
blue is the brand, and it appears only on links, on accents and on the halftone plates; anything
that is not one of those three may not wear it. A named grey ladder runs from near-white through
light and mid neutrals down to a deep neutral, and it belongs to drawn logos and mock surfaces
only. Four accent colours carry meaning and appear nowhere else: a light, soft green for something
that worked, a near-white, soft red for something that has gone wrong, a near-white, muted amber
for something still in progress, and a light, soft violet for a category that is none of those
three. A state that is none of the four must not borrow any of them. Two hover fills exist, one
deep for an ink control and one near-white for a light one. The exact shades are yours, so long as
they hold the relationships above.

Type carries four voices with one job each. A grotesk does all the working type. A single serif
weight speaks the display headlines and nothing else, which is what gives the marketing pages
their editorial voice. A mono sets navigation labels in uppercase with generous letterspacing, and
it also sets chips, figures and code. One pixel-styled mono face exists for terminal moments and
appears nowhere else. The relationships matter more than the values: a display headline reads as a
title from across a desk, a section headline is clearly its subordinate, and the working interface
sits in a deliberately dense band well below body size, because that density is the product's
point. Figures line up in a column wherever amounts stack. The exact families and the exact sizes
are yours.

Corners are barely softened and the softness is graded: chips are the sharpest thing in the
product, controls a step softer, cards a step softer again, and a fully rounded shape appears only
on pills and avatars. Nothing rounds up to the friendly default. Every measure of space is a
multiple of one base unit, which is yours to choose. Density is compact: rows sit tight so a full
working list fits one screen without scrolling, and the marketing pages breathe by comparison.

Cards are flat with a hairline border, with a stronger hairline available where a card must assert
itself. Depth is spent like money: a small paired lift under a floating row, a deep one under the
drawn product windows, an inset bevel on a light chip, and nothing else. Every product
demonstration sits inside a drawn window chrome with three traffic dots and a centred title. A
dotted texture runs through the system as grids on dark and light bands, with a fine scanline
repeat and a generated grain.

Every control states its states. A button, a chip, a cell editor and a rail item each have a
resting, a pointed-at, a pressed, a focused and an unavailable appearance, and unavailable is never
signalled by colour alone. Escape closes any overlay. A destructive action asks first and names
what it is about to affect.

Each page leads with exactly one primary action, visually distinct from every secondary one: `Get
started` on the marketing pages and the object's New control inside the workspace. Two controls
wearing the primary treatment on one screen is the failure.

Motion has one character throughout, eased: things leave quickly and arrive slowly, and every
transition in the product shares that feel so nothing moves in a way that makes it look special.
Colour and fill changes are shorter and flatter than movement. One playful overshoot exists in the
whole product and is spent on the confetti when a deal closes. Movement is never used to decorate
a decision: nothing animates underneath a person who is choosing something. A reduced-motion
preference is respected everywhere, and under it every scene renders finished and nothing loops.

The product commits to light. A dark presentation exists only inside the dark mock bands and the
halftone tool, which are surfaces rather than a theme, and a dark mode toggle is an action the
palette offers rather than a second design to be judged.

Accessibility is a floor, not a preference. Contrast meets WCAG AA for body text against its
background and for every accent chip against the surface it sits on. Touch targets are comfortably
sized. Keyboard navigation reaches everything with a visible focus ring, and the focus ring is the
one thing that animates under every circumstance. Icon-only controls carry labels. Meaning is never
carried by colour alone: a select chip pairs its dot with a word, a boolean pairs its mark with a
word, and a lane says its state in text.

The layout is responsive at every width and not merely at the two the design was drawn for.
Marketing folds to one calm column on a phone, with the hero demonstration scrolling inside its own
window rather than breaking the page. The workspace is honest about being a desk tool and degrades
with grace: the rail becomes icons, the record page stacks its card above its timeline, the table
pans sideways with its first column pinned, and the palette fills a narrow viewport. Nothing
overflows the page sideways at any width, and every navigation target stays reachable.

What this must not look like: a page dominated by one hue family with no second signal; decoration
standing in for content; a marketing composition where the working interface belongs; or anything
borrowed from a subject that is not this one.

## Technical requirements

The marketing pages are server-rendered, so the first response a browser receives already carries
the page's real markup and its copy; the workspace surfaces hydrate over that markup as islands
rather than replacing it with a blank shell. Build the server with **FastAPI** on Python and the
interface with **SolidStart**. The HTTP API is served by the same origin under the `/api` prefix.
Data lives in **PostgreSQL**, reached at `DATABASE_URL`. Electronic mail is sent over real SMTP to
**Mailpit**, reached at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. The app's own
address and port are read from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a
port; read every one of them from the environment. Both backing services are already running and
must not be downloaded, installed or started.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are PostgreSQL and Mailpit, and reaching for anything else is a
contract violation.

`GET /api/health` returns `200` once the app is ready to serve.

Logs are structured lines carrying identifiers only. No log line may contain a record value, a
person's name, an address, a telephone number or any field an administrator could mark as
sensitive, and none may contain a password, a token, a key secret or a signing secret. A log line
that carries the contents of a row is a defect even when the row is seeded fixture data.

Nothing the browser downloads may carry a credential. No database URL, no mail credential, no key
secret, no signing secret and no administrative token may appear in any served page, in any script
or style file, in any bundled asset or in any response the interface receives on a public route.
The interface reads only what an authenticated person is entitled to read.

Every public route carries its own document title and its own description, and no two public
routes share either. Every public route also declares a social preview title and a preview image
address, and that address resolves to an image the application itself serves. A route whose title
is the site name alone, or whose preview address answers as not found, has not met this.

Three things are single in this architecture and nothing may work around them. One view engine
renders every object, and the table, the board and the calendar are three presentations of one
view model rather than three separate components. One authority answers every question about
whether an actor may read a row. One event stream carries every change, and the record timeline,
the audit trail, the live surfaces and the webhook deliveries are all readings of it.

Liveness and performance are stated as outcomes rather than as techniques:

- Another person's change appears on an open surface within a second, without anyone reloading.
  This covers a table cell, a board card, a record page, a rail entry and a dashboard number.
- A client that loses its connection and returns receives the changes it missed, in the order they
  happened, with nothing repeated and nothing skipped.
- Ten thousand rows in one view scroll smoothly with the header in place, with no row rendering
  blank, torn or duplicated as it arrives.
- A permission-filtered read of a thousand rows completes within one and a half times an
  unfiltered read of the same thousand rows. Safety may cost something; it may not cost an order
  of magnitude.
- Fifty thousand rows import with progress visible throughout and the batch completes.
- An export of a large view begins streaming without first assembling the whole file in memory.
- The seeded workspace is interactive within two seconds of a signed-in person opening it.
- The halftone tool loads its rendering engine only when its own route is opened, and the site's
  halftone plates are produced when the application is built rather than when a page is served.

Two behaviours must hold when requests arrive at the same instant, and both are stated as
outcomes rather than as techniques. When two administrators save a change to the same piece of
metadata at the same moment, exactly one succeeds; the other receives a conflict response naming
the current version and is offered its change again against it, and the store never ends up
holding a blend of the two. When the same mutating request arrives twice, whether because a
workflow was triggered twice by two observers of one event or because a client retried, the second
arrival must not create a second record, a second run, a second message or a second import batch.

## Data model

Fourteen entities. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**workspace.** Name, plan tier, seat count, credits used. One row: this deployment is one
workspace. Every gate in the product reads this row rather than a second copy of the plan.

**membership.** The account, its role of `owner`, `admin` or `member`, the custom role when one is
assigned, and the seat state. The role is the server's answer about what an actor may do; the
interface never decides it. Exactly one membership carries `owner`.

**object metadata.** Singular label, plural label, icon, display order, active flag, archived-at.
Labels are unique across active objects. An archived object stays restorable for thirty days and is
purged after that. Derived rather than stored: the record count and the field count the schema
graph shows.

**field metadata.** Its object, its name, its type, its options for a select, its unique flag, its
display order, archived-at. A name is unique within its object. A rename preserves every stored
value. A type change either converts every value or changes nothing at all, and where it changes
nothing the count of rows that blocked it is reported.

**relation metadata.** The two paired fields and the cardinality, one-to-many or many-to-one. Both
sides are always present or both are archived; a relation with one live side is invalid state.

**view.** Its object, its type of table, kanban or calendar, its filters, its sorts, its visible
and pinned columns, its grouping field, its owner and whether it is shared. A view never references
a field or an object that is not live. Derived rather than stored: the record count in the view
bar.

**record.** Its object, its typed values, its created-by actor, its created-at and updated-at, its
short code in the style of `OPP-1`. A field marked unique admits one row per value, and a second
write of the same value is refused by the store rather than by a check the interface makes first.

**event.** Actor, actor kind, verb, target object, target record, the value before, the value
after, and the time. Append-only: nothing in the product updates or deletes an event. This one
table feeds the record timeline, the audit trail, every live surface and every webhook delivery, so
those four can never disagree about what happened.

**workflow, workflow version, run, run step.** A workflow holds its name and its active flag; a
version holds the graph, the trigger and its version number; a run holds the workflow, the version
it pinned, its trigger event, its status and its times; a run step holds its node, its input, its
output, its outcome and its order in the run. A run keeps the version it started on for its whole
life.

**permission rule.** Its role or actor, its object, its grants, its row filter and its masked
fields. Evaluated identically wherever a row is read. A rule stored while the plan does not permit
it is retained and marked inert.

**identity.** Credentials hashed, the second-factor enrolment and its state, the live sessions and
their expiry, and the stored single sign-on configuration. Sessions are revocable individually and
in bulk. The stored configuration is shown back but never acted on.

**key, webhook, app.** A key holds its name, its scopes, the hash of its secret, its actor identity
and its revoked-at; the secret itself is shown once at creation and never stored in readable form.
A webhook holds its object, its address and its signing secret. An app holds its name, its scopes,
the metadata it contributed and its actor identity, so every row it touched stays attributed after
it is uninstalled.

**import batch.** The object, the mapping, the duplicate strategy, the counts attempted, landed and
rejected, the per-row errors, the undo handle and the audit entry. One batch is one undo.

**dashboard, widget.** A dashboard is a record of the Dashboards object. A widget holds its kind,
its object, its filters, its date range and its place in the grid. Derived rather than stored:
every number a widget shows, computed on read from the rows the reader is permitted to list.

Money is stored in integer minor units in `usd`, so `$9.00` is `900` and never `9.00` or `9`. A
currency value read back through any path returns the same integer that was written.

**Seed data.** The workspace is named `Thirty`, on the `Organization` plan. The seven starter
objects exist as metadata rows. Companies holds the nine fixture rows named in `## Core features`
with their thirteen columns, five owned by `member@example.com` and four by `member2@example.com`.
People and Opportunities hold the related rows, including the four board cards `OPP-1`, `OPP-2`,
`OPP-6` and `OPP-8`. The Companies view `All Companies` shows nine rows. One dashboard named
`Sales Dashboard` is favourited for every account. One permission rule binds a Companies row to its
account owner for the `member` role. One workflow named `Stage change notice` is seeded, active,
and triggers on an Opportunity stage change. The created-by column carries people, one actor named
for a key, one named for a workflow and the `System` actor, so the actor kinds are all present
before anyone does anything. Seeding must be idempotent - restarting the app must not duplicate
rows.

## Front-end specification

This section carries the visual detail that will not fit inside `## UI/UX notes`. Everything here
is description rather than measurement: where the source material recorded an exact value, the
requirement is the relationship or the character it produced, and the value itself is yours.

### The grid and the reading columns

The marketing pages centre on a single content measure with generous outer margin, and long-form
pages, the why essay, the legal documents, the release notes and the case bodies, sit in a
narrower reading column inside it so a line of prose never runs wider than is comfortable. The
workspace uses the full width: it is a working surface and margin there is wasted space.

### Marketing header

A white bar, hairline along its bottom edge, that stays put as the page scrolls. The logo tile
sits at the left; the centre carries Product, Resources, Customers and Pricing in the uppercase
mono voice, separated by hairlines rather than by dots or pipes; Resources opens a dropdown
holding Developers, User Guide, Release Notes and their kin. To the right sit the two count chips,
small mono-label pills each carrying a drawn mark, a star for the repository count and a speech
bubble for the community count, each with an outbound arrow. Then `Log in` as an outline control
and `Get started` as the ink-filled one. At a narrow width the centre links collapse into a menu
sheet and `Get started` stays on the bar.

### Footer

Ink on white, four columns under uppercase mono column heads, with grey links that brighten on
hover. Below them sit the calls to action, the copyright line and the language selector, with the
social glyph row. Directly above the footer on every marketing page sits the closing question band
with its seven disclosure rows.

### Shared furniture

Buttons come in three forms only: an ink fill, an outline and a plain text control. Marketing sets
their labels in uppercase mono; the product mocks set them in sentence case, because that is what
the real product does. A hover swaps the fill to the paired hover colour on a short, flat ease.
Disclosure rows, the questions and the matrix groups, open by growing their own row rather than by
sliding a panel over the page, on the plainer of the two eases. The testimonial slider shows one
quotation plate at a time in the display voice, with arrows and a pager reading the current
position out of three. Case cards pair a metric value above its label, carry an oversized drawn
quotation mark and a category chip. Every product demonstration sits inside the drawn window
chrome.

### Design tokens, by name

The design system names its colours rather than scattering them, and the names are part of the
contract because the mock surfaces and the drawn logos refer to them. Define the ground as
`--surface`, the near-black that carries everything as `--ink` with its transparency steps driving
text hierarchy and the hairline `--line`, and the single brand hue as `--color-blue`.

The named grey ladder, lightest first, reads `--color-chalk`, `--color-neutral`, `--color-fog`,
`--color-silver`, `--color-ash`, `--color-stone`, `--color-iron`, `--color-graphite` and
`--color-charcoal`. It exists for mock surfaces and drawn logos and is never used for text.

The four accent tokens are `--color-green` for something that worked, `--color-error` for
something that has gone wrong, `--color-yellow` for something still in progress and
`--color-pink` for a category that is none of those three. They dress the select-option chips, the
status dots and the highlights, and nothing else. Two hover tokens complete the set,
`--color-black-hover` for an ink control and `--color-white-hover` for a light one.

The shades behind every one of these names are yours, so long as they hold the relationships in
`## UI/UX notes`.

### Motion, in detail

There is one easing vocabulary and it is small. A single house settle carries nearly everything,
leaving quickly and arriving slowly; colour and fill changes run shorter and flatter than it;
small transforms use a tighter version of the same feel; opacity changes and the disclosure
expansions use a plainer curve than either; and one playful overshoot exists in the whole product
and is spent only on the confetti. The exact curves and durations are yours, so long as one
character is recognisable across every surface.

The mock choreography is armed by scroll and plays once per band, and it moves things by shifting
and fading them rather than by redrawing them, so a band that has finished stays finished.

The workspace uses that same vocabulary at that same character, so crossing from the marketing
pages into the product does not feel like changing products.

### The drawn asset system

This is a zero-asset build. No binary asset ships with this application, and every substitution
below is drawn or generated by code.

- The halftone plates, the hero field, the band plates and the release cover, are rendered by the
  halftone generator when the application is built, in ink grey or the brand blue.
- The logo is a drawn square monogram tile, a white glyph on an ink ground, softened a little more
  than a card is. The wordmark is the product name set in the grotesk.
- The repository and community marks are neutral drawn shapes, a star and a speech bubble, not
  borrowed service logos.
- Fixture company logos are drawn monogram tiles taken from the grey ladder. People avatars are
  circles carrying seeded initials.
- The trusted-by bar is ten plain text wordmarks in the mono face, fully desaturated.
- The light grain texture, the dot grids and the scanline repeat are generated tiles.
- The four type families are hosted and swap in rather than blocking the first paint, with system
  fallbacks behind each.

### Iconography

Interface icons are a single compact stroke set at one size, matching the product rather than the
marketing: object glyphs for a building, a person, a target, a check, a note, a chart and a bolt;
view controls; a glyph per field type; drag handles. A select chip pairs a half-strength dot with
its text. Avatars are fully rounded circles falling back to initials. Cursor art in the
go-to-market band is drawn triangles with name tags that pop as they arrive.

### The table, in detail

The header row stays put while the body moves under it, and each header cell carries its field
type's glyph before the name. A checkbox column leads, and a New row affordance closes the body. A
summary footer sits beneath. Column widths are dragged from the header edge; a column is picked up
by its header and dropped between two others; pinning a column to the left holds it in place while
the rest pans. A cell under edit shows its editor inside the cell's own bounds rather than floating
over its neighbours, and an editor that rejects a value says which field and why beside the cell,
not in a corner of the screen. A selected row is marked by a change of surface rather than by
colour alone. Sort and filter chips sit in the view bar and each carries its own remove control.

### The board and the calendar

Lanes are columns of equal width with a header carrying the lane name, its count and, where the
object has money in it, its total. A card is a small flat surface with a hairline: title, company
chip, amount, date, owner avatar and record code. A card in flight follows the pointer and the
lane it would land in marks itself. Lane totals recount as the card lands rather than after it
settles. A collapsed lane becomes a narrow rail carrying its name and count turned on its side.
The calendar is a month of day cells that fill from the top, each entry a compact chip carrying its
title and time; an entry is dragged to another day and re-dates there.

### The record page

A two-part page: the record card on one side, the tabbed workspace on the other. The card opens
with the record's icon or drawn logo, its name as the largest thing on the page, and its quick
actions. Field rows sit in labelled groups, each row a label and a value that becomes editable
where it stands. Relation sections list related records as chips with an add control and a detach
control on each. The tab bar carries Timeline, Notes, Tasks, Emails and Calendar, and Files. A
timeline entry is one line: actor, what changed, from what to what, and how long ago. Entries
arrive newest first.

### The command palette

A centred overlay above a dimmed page, opening with an empty input and a caret. Results group under
quiet mono headings, one group per kind, each row carrying its glyph, its label and, where it has
one, its key sequence set in the mono face at the right-hand edge. The highlighted row moves with
the arrow keys and never with the pointer alone. On a narrow viewport the overlay fills the screen.

### The AI side panel

The one translucent surface in the product: it blurs and slightly enriches whatever sits behind
it, and it carries a soft lift beneath its edge so it reads as floating above the work rather than
docked into it. Its messages are plain text blocks; a cited record renders as a chip that opens the
record. A refusal reads as a plain sentence, not as an error state.

### The dark mock surfaces

Three surfaces are dark: the schema graph band, the AI build session editor and the halftone tool.
They invert the ink system rather than introducing new colours, white text on the near-black at
graded strengths, over a dotted ground. They are surfaces, not a theme, and nothing else in the
product goes dark unless the palette's dark-mode action is used.

### The halftone tool layout

The scene fills the left of the screen with the header line above it. The control rail runs down
the right, its tabs across the top, its groups stacked under labelled headings with each control on
its own row: a label at the left, the control at the right, and its current value shown in the mono
face. At a narrow width the rail stacks below the scene rather than shrinking beside it.

### Responsive behaviour, stated by width

On a phone the marketing pages become one column: band plates stack, the hero demonstration
letterboxes and scrolls sideways inside its own window rather than pushing the page wide, the
comparison matrix scrolls inside its own container, and the halftone tool stacks its rail below
the scene. At tablet width the workspace keeps working: the rail collapses to icons with the
labels on hover, the record page stacks its card above its tabs, tables pan sideways with the
first column pinned, and the palette fills the screen. On a desk everything is present at once.
Every drag has a menu equivalent: a board card moves through a move action, and a column reorders
from the view options. No page overflows sideways at any width.

### Announcements and focus

Focus is never lost: opening an overlay moves focus into it, closing one returns focus to whatever
opened it, and an inline editor keeps focus inside itself until it commits or abandons. Arrow
keys, home, end and the page keys walk the table as a grid, and each cell announces its field
type and its value. Three things are announced as they happen rather than only drawn: a row edited
by somebody else, a workflow run finishing, and import progress.

## Constraints

- One workspace per deployment. There is no workspace switcher between tenants and no
  cross-workspace read of any kind.
- Signup is closed. No public registration form exists anywhere in the product.
- No real third-party service. No external mail vendor, no external identity provider, no external
  language model, no analytics endpoint, no payment processor and no outbound call to any of them
  at runtime.
- The single sign-on and directory provisioning surfaces store configuration and do nothing else.
- Billing is simulated and stateful. No card is taken, no invoice is issued, and no money moves.
- The AI surfaces compute from the workspace's own records or refuse. No answer is generated from
  anything else.
- No binary asset ships: no image file, no font file, no video, no audio, no icon sprite.
- No native application, no offline mode, no service other than the two named.
- No comments, no likes, no direct messaging between members, and no public sharing of a record
  outside the workspace.
- The app stays responsive with ten thousand records in a single view and fifty thousand rows in a
  single import batch.

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

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password`, `code` when a second factor is enrolled | `token`, `role`, `requires_code` |
| `POST /api/auth/logout` | none | the session ended |
| `GET /api/objects` | none | a top-level JSON array of objects, each with `name_singular`, `name_plural`, `icon`, `field_count`, `record_count` |
| `POST /api/objects` | `name_singular`, `name_plural`, `icon` | the created object |
| `PATCH /api/objects/{object}` | any of `name_singular`, `name_plural`, `icon`, `active` | the updated object, or the dependent list when one must be confirmed first |
| `DELETE /api/objects/{object}` | none | the archived object and its `purge_at` |
| `GET /api/objects/{object}/fields` | none | a top-level JSON array of fields, each with `name`, `type`, `options`, `is_unique` |
| `POST /api/objects/{object}/fields` | `name`, `type`, `options`, `is_unique` | the created field |
| `PATCH /api/objects/{object}/fields/{field}` | any of `name`, `type`, `options` | the updated field, or a refusal carrying `blocking_rows` |
| `GET /api/objects/{object}/dependents` | `field` when the question is about one field | a top-level JSON array of dependents, each with `kind`, `name` and `action` |
| `GET /api/objects/{object}/records` | `view`, `filter`, `sort`, `cursor`, `limit` | `records`, `total`, `next_cursor`, all of them permission-filtered |
| `POST /api/objects/{object}/records` | the typed values | the created record with its `code` and `created_by` |
| `PATCH /api/objects/{object}/records/{record}` | the changed values, `version` | the updated record, or a conflict naming the current `version` |
| `DELETE /api/objects/{object}/records/{record}` | none | the archived record |
| `GET /api/views` | `object` | a top-level JSON array of views with `type`, `filters`, `sorts`, `columns`, `group_by`, `is_shared` |
| `GET /api/search` | `q` | a top-level JSON array of grouped results, permission-filtered |
| `GET /api/aggregates` | `object`, `group_by`, `metric`, `filter` | the grouped totals, computed after row filtering |
| `POST /api/imports` | the file, `object`, `mapping`, `duplicate_strategy`, `dry_run` | the batch with `attempted`, `landed`, `rejected`, `row_errors`, `undo_handle` |
| `POST /api/imports/{batch}/undo` | none | the batch reversed, as one act |
| `GET /api/exports` | `view` or `selection` | the file carrying exactly the permitted rows and columns |
| `GET /api/workflows/{workflow}/runs` | none | a top-level JSON array of runs with `trigger`, `version`, `status` and their `steps` |
| `POST /api/workflows/{workflow}/runs` | `record` for a manual run | the run, or a refusal when the credit gate is closed |
| `GET /api/audit` | `actor`, `object`, `cursor` | a top-level JSON array of entries with `actor`, `actor_kind`, `verb`, `before`, `after`, `at` |
| `GET /api/plan` | none | `tier`, `seats`, `credits_used`, `credits_included` |

Every endpoint except `POST /api/auth/login`, `GET /api/health` and the webhook receivers requires
the bearer token. A webhook receiver authenticates by the signature on the payload and never by a
person's token. A request that breaks a rule in this brief is rejected as a client error carrying
a reason, never as a server error and never as a silent success. A list endpoint returns a
top-level JSON array.

### No mocks

Two services back this application and the data has to actually be in them.

The following are contract violations however convincing the interface looks: an in-memory array of
records that disappears when the process restarts; a JSON or SQLite file on the app's own disk
standing in for the database; a message the app records as sent without handing it to the mail
server; a screenshot, a recorded video or a static image standing in for a product mock; a stored
halftone image file standing in for a generated plate; a hardcoded answer returned from the AI
panel that was not computed from the records; and a permission decision made only in the interface
while the query behind it still returns the row.

The named provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger can read the marketing site, sign in as a seeded sales rep and work real records
through a table, a board and a calendar that are the same components the site's pictures are. An
administrator can reshape the workspace while that rep keeps working, and nothing the rep depends
on is ever silently stranded. Each rep sees only the rows the permission rules admit, and sees the
same answer in the table, the totals, the search box, the export and the keyed interface. A
workflow that fires leaves one run, one complete diary of what it did, and exactly one message in
the addressed inbox.
