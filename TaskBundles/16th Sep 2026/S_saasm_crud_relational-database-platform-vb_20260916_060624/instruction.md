# Relational Database Platform

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, sign in as an editor, open a base,
change a cell in a grid view, watch the rollup two tables above it change with it, reload the page
and find both values exactly as they were left, without hitting an error page. A different stranger
who holds a role in another workspace must NOT be able to read that base, that table, that record or
that operation log by any means, including a direct request for a record by its own identifier. A
write that a blocking guard refuses must leave nothing behind at all: no cell, no record, no
recomputed neighbour and no appended operation. A green banner the app shows itself does not count;
the stored data is the fact.

## Overview

A team builds its own working tools over its own data without writing production code. The
hierarchy is fixed and each level is owned by exactly one level above it: a workspace holds bases, a
base holds tables of records, a table holds fields, a field carries a type, and a cell is a record
crossed with a field. A view is a live query over one table rather than a saved copy of it, so
filtering a view never changes the table and never changes what anybody else sees in another view.

Over that core sit computed fields that resolve through a dependency graph across tables, and an
organisation model of workspaces and five collaboration roles. Beneath it sits the substrate that
the rest is derived from: an append-only operation log, where every write appends one operation and
nothing ever rewrites one. Record history and historical reads are readings of that log rather than
rows stored beside it, which is what makes the log the truth rather than a diary that can disagree
with the data.

It deliberately is not a spreadsheet and not a document tool. There are no attachments and no file
upload, no automations, no forms, no app builder, no extensions, no comments, no notifications, no
external synchronisation, no payment and no artificial intelligence features.

The genuinely hard part is that the product's memory has to be derived rather than kept. A cell edit
must recompute exactly the computed fields that depend on it and nothing else, a historical read has
to rebuild values that were never stored as a snapshot, and a guard has to judge the value a write
would have produced before that write is allowed to exist.

## User roles

Five roles. A role is granted on a workspace and inherited by every base in it, so the same person
may be an owner of one workspace and hold nothing in another. A direct base grant is additive on top.

| Role | Can do | Cannot do |
|---|---|---|
| `owner` | everything a `creator` can do, plus grant and revoke membership, change roles, create and delete bases, create and delete guards, and lock and unlock views | **cannot** act in a workspace they hold no membership in |
| `creator` | everything an `editor` can do, plus create, rename and delete tables and fields, change a field's type and configuration, and create and delete views | **cannot** grant membership, change a role, create or delete a base, or create or delete a guard |
| `editor` | read everything in the workspace, create, change and delete records and cell values, and create and change collaborative views | **cannot** create, rename or delete a table or a field, change a field type, or lock a view |
| `commenter` | read everything in the workspace and create and change views that belong only to them | **cannot** change any cell value, ever, whatever any other setting says, and **cannot** change a collaborative view |
| `reader` | read everything in the workspace | **cannot** write anything anywhere |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `commenter` session to any `editor`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

Effective permission resolves two grant paths and the more permissive of the two wins. A base grant
may raise a member above their inherited workspace role and may never lower them below it; a lower
base grant is stored and has no effect, and the interface says so where the grant is made. A member
with no membership and no base grant reaches nothing: a request naming a record in a workspace they
have no role in is answered as though no such record exists, never as a refusal that confirms it.

Signup is open. A new account holds no membership until one is granted, so it sees an empty
workspace list and nothing else. Every seeded account uses the password `deku-demo-pw-2026`.
`owner@example.com`, `creator@example.com`, `editor@example.com`, `commenter@example.com` and
`reader@example.com` hold those five roles in `Northfield Commercial`. `owner2@example.com` is the
owner of `Harbourline Studio` and holds nothing in `Northfield Commercial`.

## Core features

### Records and the grid

1. `POST /api/bases/{baseId}/tables/{tableId}/records` creates a record.
   `PATCH /api/bases/{baseId}/tables/{tableId}/records/{recordId}` changes cell values.
   `DELETE /api/bases/{baseId}/tables/{tableId}/records/{recordId}` removes one.
   `GET /api/bases/{baseId}/tables/{tableId}/records` returns the records of a table as a top-level
   JSON array, each carrying its identifier, its cell values by field identifier, and the current
   value of every computed field on it.
2. **A cell written through the grid is stored, and a re-read after a reload returns exactly what
   the grid displayed, including every computed field that depends on it.** The value the interface
   shows, the value the record endpoint returns and the value that survives a restart of the browser
   are one value. A value the app holds only in the page is not stored.
3. Deleting a record removes its cells and both sides of every link that named it, and leaves every
   rollup, count and lookup that reached it correct on the next read.
4. A base holds at most `50000` records. Exceeding it is refused, and the refusal names the limit and
   its value.
5. `autoNumber` increases within its table and no two records in one table ever carry the same auto
   number, including when two records are created at the same moment.
6. A field name of `200` characters and a cell value of `10000` characters are both accepted and
   break no layout.

### Auth

Authentication is email and password, implemented by this app. The product has no other surface: an
address under `/api` that this brief does not name answers as not found rather than as a feature
nobody described. `POST /api/auth/signup` creates an account.
`POST /api/auth/login` returns a bearer token. Every other endpoint except `GET /api/health` carries
`Authorization: Bearer <token>`. `GET /api/auth/me` returns the signed-in account. Passwords are
hashed and the plaintext is never stored and never returned in any response. A token expires, and an
expired or absent token reads as not signed in: the request is denied and nothing is written.

### Workspaces and bases

1. `GET /api/workspaces` returns only the workspaces the caller holds a membership or a base grant
   in, as a top-level JSON array.
2. A base belongs to exactly one workspace and never spans two.
3. A base holds at most `100` tables. A workspace holds at most `1000` bases. Exceeding either is
   refused, and the refusal names the limit and its value.
4. Only an `owner` creates or deletes a base. A `creator`, `editor`, `commenter` or `reader`
   attempting either is denied by the server and no base is created or removed.
5. A request for a base, table, view, record, guard or operation in a workspace the caller holds no
   grant in is answered as though the thing does not exist. This holds for a direct request naming
   the identifier, not only for a link the interface declines to draw.

### Identifiers

Every object carries a stable identifier of exactly `17` characters: a three-character type prefix
followed by `14` characters drawn from the digits and the upper-case letters. The prefixes are `wsp`
for a workspace, `bas` for a base, `tbl` for a table, `viw` for a view, `fld` for a field, `rec` for
a record, `grd` for a guard and `opn` for an operation. A worked example of a record identifier is
`rec7QW2M4KX9T0ZB1`. An identifier is never reused and never renumbered once issued, including after
the object it names is deleted.

### Tables and fields

1. A table holds at most `500` fields. Field names are unique within their table. Exceeding the
   limit, or reusing a name, is refused and the refusal names what was wrong.
2. Exactly one field in each table is the primary field. It is the first field, it cannot be hidden
   in any view, it cannot be a computed type, and it is what a linked record displays.
3. Every table has at least one `grid` view, and that view cannot be deleted.
4. `GET /api/field-types` returns all `19` field types as a top-level JSON array, each carrying its
   `slug`, whether it is `computed`, and the configuration keys it accepts.

The nineteen field types, with the exact slug each one is addressed by:

| # | Name | Slug | Stores | Computed | Configuration |
|---|---|---|---|---|---|
| 1 | Single line text | `singleLineText` | one line of text | no | `defaultValue` |
| 2 | Long text | `multilineText` | a multi-line string | no | none |
| 3 | Number | `number` | integer or decimal | no | `precision` `0` to `8`, `allowNegative` |
| 4 | Currency | `currency` | number | no | `precision` `0` to `7`, `symbol` |
| 5 | Percent | `percent` | number | no | `precision` `0` to `8` |
| 6 | Checkbox | `checkbox` | true or false | no | none |
| 7 | Single select | `singleSelect` | one choice name | no | `choices`, each a name and a colour name |
| 8 | Multiple select | `multipleSelects` | several choice names | no | `choices`, each a name and a colour name |
| 9 | Date | `date` | an ISO 8601 calendar date | no | `dateFormat` |
| 10 | Date and time | `dateTime` | an ISO 8601 date and time | no | `timeZone`, `dateFormat`, `timeFormat` |
| 11 | Rating | `rating` | a positive whole number | no | `max` `1` to `10` |
| 12 | Duration | `duration` | whole seconds | no | `durationFormat` |
| 13 | Link to another record | `multipleRecordLinks` | an array of record identifiers in another table | no | `linkedTableId`, `prefersSingleRecordLink`, `inverseLinkFieldId` |
| 14 | Lookup | `multipleLookupValues` | an array of one field's values across the linked records | yes | `recordLinkFieldId`, `fieldIdInLinkedTable`, conditions |
| 15 | Rollup | `rollup` | an aggregation over looked-up values | yes | `recordLinkFieldId`, `fieldIdInLinkedTable`, aggregation, conditions |
| 16 | Count | `count` | how many records are linked | yes | `recordLinkFieldId`, conditions |
| 17 | Formula | `formula` | whatever the expression returns | yes | `formula`, `isValid`, `referencedFieldIds` |
| 18 | Created time | `createdTime` | when the record was created | yes | none |
| 19 | Auto number | `autoNumber` | an increasing whole number | yes | none |

5. A choice on a `singleSelect` or a `multipleSelects` field carries a name and a colour, and the
   colour is chosen from exactly these ten names: `blue`, `cyan`, `teal`, `green`, `yellow`,
   `orange`, `red`, `pink`, `purple` and `grey`. The name is the colour: a choice chip shows its
   colour name as text as well as wearing it, because the colour is meaning somebody assigned and
   the exact shade of each of the ten is yours.
6. A computed field is never writable. A request that sets a value on a `formula`, `rollup`,
   `multipleLookupValues`, `count`, `createdTime` or `autoNumber` field is refused and the stored
   value does not change.
7. Precision is a display decision and never a storage decision. A `number` with precision `2` given
   `3.14159` stores `3.14159` and displays `3.14`; reading the record back returns `3.14159`.
8. A `duration` stores whole seconds whatever format it displays in. Ninety minutes is stored as
   `5400`.
9. A `dateTime` resolves against its own field's configured timezone, so one stored instant reads as
   the correct local time for each of three configured timezones.

### Links, lookups, rollups and counts

1. A link field stores references to records in another table and displays each one by that table's
   primary field.
2. Links are symmetric by default. Creating a link writes the mirrored reference under the inverse
   field in the other table, and deleting either side removes both.
3. The single-link preference is a picker restriction, not a stored rule. When it is off the picker
   offers one record per cell, and several links may still arrive through a direct request. The
   property prefers a single link; it does not enforce one, and existing multi-link cells stay valid
   when it is turned off.
4. A link field carries one-to-one, one-to-many and many-to-many relationships, and the field's
   configuration surfaces `inverseLinkFieldId` so the other side of the relationship is nameable.
5. Traversal is one hop deep. Lookup, rollup and count each traverse exactly `1` hop through the
   link field named by `recordLinkFieldId`, and lookup and rollup each read the field named by
   `fieldIdInLinkedTable`. More than one hop is built by chaining fields, never by a deeper
   traversal.
6. All three accept conditions that narrow which linked records are included.
7. A configuration that has become invalid, because the field it names was deleted or retyped into
   something it cannot read, blanks every cell in that field until it is fixed, and the field reports
   which field broke it. The rest of the table keeps working.
8. `rollup` supports exactly `16` aggregations, and the three counting ones are different from each
   other:

| Aggregation | Behaviour |
|---|---|
| `AND` | true when every value is true |
| `OR` | true when any value is true |
| `XOR` | true when an odd number of values are true |
| `SUM` | the total |
| `AVERAGE` | the mean |
| `MAX` | the largest |
| `MIN` | the smallest |
| `COUNT` | how many values are numbers and not empty |
| `COUNTA` | how many values are not empty, of any type |
| `COUNTALL` | how many records are linked, empty values included |
| `ARRAYCOMPACT` | the values with empty ones removed |
| `ARRAYFLATTEN` | the values with nesting removed |
| `ARRAYJOIN` | the values joined into one string by a separator |
| `ARRAYSLICE` | a run of the values from a start to an end |
| `ARRAYUNIQUE` | the values with repeats removed |
| `CONCATENATE` | the text values joined |

9. Worked example, and the algorithm must reproduce it exactly. A campaign links to `4`
   deliverables whose looked-up `Hours` values are `12`, `0`, empty, and the text `n/a`. `COUNT`
   returns `2`, because only `12` and `0` are numbers and not empty. `COUNTA` returns `3`, counting
   `12`, `0` and `n/a` and skipping the empty one. `COUNTALL` returns `4`, counting every linked
   record whatever it holds. `SUM` returns `12`. `MIN` returns `0` and not `12`, because an empty
   value is skipped and a zero is not. Those six numbers are the ones to reproduce.

### Formula fields and the dependency graph

1. `formula` supports exactly `12` functions: `IF`, `CONCATENATE`, `LEN`, `LOWER`, `UPPER`, `TRIM`,
   `FIND`, `SEARCH`, `SUM`, `ROUND`, `DATETIME_DIFF` and `TODAY`. It also supports text joining with
   `&`, the four arithmetic operators and the six comparisons.
2. `FIND` is case-sensitive and `SEARCH` is not. `FIND("ab", "AB")` finds nothing and
   `SEARCH("ab", "AB")` finds a match at the first character. That difference is deliberate and must
   survive.
3. A formula records which fields it reads, and those references are what the dependency graph is
   built from.
4. Changing one cell recomputes exactly the computed fields that depend on it, then the fields that
   depend on those, across tables through link fields, and then stops. A computed field that no path
   reaches is not recomputed.
5. A field that two dependency paths both reach is computed once for a single change, not twice.
6. Moving a link from one record to another invalidates the computed fields of both the record that
   lost the link and the record that gained it.
7. A formula whose referenced field is deleted or retyped into something it cannot read is marked
   invalid, holds no value, and names the field that broke it.
8. A configuration that would make a computed field depend on itself, directly or through other
   fields, is refused when the field is saved and not when it is read.
9. Rounding is stated rather than inherited: `ROUND` rounds half away from zero, so `2.5` rounds to
   `3` and `-2.5` rounds to `-3`.
10. Decimal arithmetic on money is exact: adding `0.1` and `0.2` gives `0.3`, and a `currency` total
   of `1200.00` and `800.00` is `2000.00`.
11. A formula evaluation is free of side effects and bounded: evaluating a formula writes nothing,
   reads nothing outside the record and the fields it names, and cannot run without end.

### Views

1. Three view types, addressed by the exact slugs `grid`, `gallery` and `kanban`. A view belongs to
   exactly one table and is a live query over it, never a copy.
2. A table holds at most `1000` views.
3. `grid` carries a row height of `short`, `medium` or `tall`, hides, shows and reorders fields,
   filters, sorts, groups, and carries a summary row.
4. `gallery` shows one card per record and chooses which fields appear on the card. Card size
   follows the viewport and is not set by hand.
5. `kanban` stacks records by exactly one `singleSelect` field named in the view's `config` under
   the key `stackFieldId`. There is no second stacking level. A view holds at most `200` stacks.
6. **Filtering.** Operators depend on the field type. Text offers `contains`, `does not contain`,
   `is`, `is not`, `is empty` and `is not empty`. Numbers offer the six comparisons. Dates offer
   `is`, `is before`, `is after`, `is on or before` and `is on or after`. A link field offers
   `has any of`, `has all of` and `has none of`. Each level of a condition group carries exactly one
   conjunction, so `AND` and `OR` never mix at the same level. Nesting reaches `3` levels and no
   deeper. A view carries at most `49` conditions, standalone and grouped together, and the `50th`
   is refused naming the limit and its value.
7. **Sorting.** Up to `10` sort levels. Text sorts alphabetically, numbers numerically, dates
   chronologically, and a checkbox sorts unchecked before checked. A `singleSelect` or
   `multipleSelects` field sorts by the order its choices are configured in, never alphabetically.
   Automatic sort is on by default: while it is on, records re-sort on every change and dragging a
   row to reorder it is disabled. Turning automatic sort off enables drag-reordering and exposes a
   control that re-applies the sort on demand.
8. **Grouping.** Up to `3` levels, one main group and two subgroups. Groupable field types are
   `singleSelect`, `multipleSelects`, `date` and `multipleRecordLinks`. Every group header carries
   its value, how many records it holds and whether it is collapsed. A record cannot be created
   directly into a group formed on a computed field, because there is no value to write; the attempt
   is refused and names the reason.
9. **View modes**, addressed by the exact slugs `collaborative`, `personal` and `locked`. A
   `collaborative` view is the default and any member who may edit views may change it. A `personal`
   view is configured only by the account that created it, and a request from another account to
   change it is denied. A `locked` view cannot have its configuration changed by anybody until an
   `owner` or a `creator` unlocks it, and locking protects the configuration and never the records:
   editing a cell through a locked view still works for a member who may edit cells.

### The operation log

1. Every write appends exactly one operation to its base's log. Nothing ever updates an operation
   and nothing ever deletes one.
2. An operation carries its own identifier, a `sequence`, the moment it happened, the account that
   caused it, the `kind` of change, the type and identifier of what it touched, and the values
   `before` and `after`.
3. Within one base, `sequence` starts at `1`, increases strictly, is never reused and never skipped.
   Two writes to the same base arriving at the same moment produce two operations carrying two
   different sequence numbers, and the log left behind contains no gap and no repeat.
4. Operations group into transactions. One transaction is atomic across every operation inside it:
   either all of its operations are in the log or none of them is, and a reader never sees half of
   one.
5. `GET /api/bases/{baseId}/operations` returns the log newest first as a top-level JSON array, and
   accepts a `since` query parameter returning only operations after that sequence.
6. **Record history** is a reading of the log for one record, not a second table.
   `GET /api/bases/{baseId}/tables/{tableId}/records/{recordId}/history` returns who changed which
   field, from what to what and when, newest first, including the record's creation.
7. **A historical read** shows a table as it stood at a chosen sequence.
   `GET /api/bases/{baseId}/tables/{tableId}/records?asOf={sequence}` returns the values as they were
   then, with every computed field recomputed from those values rather than replayed from a cache,
   so a historical read of a rollup is correct even for a sequence before that rollup was configured.
8. A historical read is never editable. A request that changes anything while naming `asOf` is
   refused.
9. A historical read applies today's permissions and not the permissions of that moment. Somebody
   who has since lost their grant cannot reach the past through it, and somebody who has since
   gained one can.
10. **Replay verification** reads the log forward from the first sequence and compares what it
   rebuilds against what is stored. `GET /api/bases/{baseId}/operations/replay` answers whether the
   two agree, and where they do not it names the first sequence at which they part company. A write
   path that bypasses the log is exactly what this finds, which is why no write path may bypass it.

### Guards

1. A guard is a write-time invariant an `owner` declares on a base. It names the table it watches,
   the condition that must not hold, a `mode` of exactly `blocking` or `advisory`, and the `message`
   a person sees when it fires.
2. The message is shown exactly as it was authored, character for character, in the response and in
   the interface. A refusal in somebody else's words is a refusal nobody acts on.
3. Guards are evaluated after computed fields have been recomputed and before the write is
   committed, so a guard may name a `rollup` or a `formula` and read the value the write would have
   produced.
4. A `blocking` guard refuses the write and leaves nothing behind: no cell, no record, no link, no
   recomputed neighbour and no appended operation.
5. An `advisory` guard allows the write and records a violation that stays listed in the guards panel
   until the data stops violating it.
6. Guards apply on every path into the data without exception. A write arriving as a direct API
   request is refused exactly as a write typed into a cell is.
7. A base holds at most `200` guards. `GET /api/bases/{baseId}/guards` lists them,
   `POST /api/bases/{baseId}/guards` creates one and `DELETE /api/bases/{baseId}/guards/{guardId}`
   removes one. Only an `owner` may create or delete a guard.
8. Two guards are seeded on `Campaign Planning` and their messages are exactly these strings:
   `A deliverable cannot be marked Done with an empty estimate.` on `Deliverables`, `blocking`;
   and `A campaign over 40 hours of tasks usually needs a second owner.` on `Campaigns`, `advisory`,
   with one violation already outstanding against `Autumn Lantern`.

### Refusals

Four kinds of refusal exist and they read as four different things: a refusal for permission, a
refusal for a structural limit, a refusal from a `blocking` guard, and a refusal for invalid input.
Every one of them names what was refused and why, in the product's own words, and none of them is a
generic failure. No refusal leaves a partial write behind.

### A privacy page

`/privacy` states what the product stores about a member, which is their email address, their
display name, the workspaces they hold a role in and every operation they caused, and states how long
each of those is kept. It is reachable from the footer of every page, including `/login` and
`/signup`, and it is readable without signing in.

### Every internal link resolves

Every link the app draws to one of its own routes resolves to a real page. No internal link on any
route answers not-found. An address the app does not recognise renders the product's own not-found
page, which carries a way back to `/workspaces`, and answers as not found rather than as a page that
worked.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | redirect to `/workspaces` when signed in, `/login` otherwise | none |
| `/login` | sign in | none |
| `/signup` | create an account | none |
| `/go` | the command palette as its own address | required |
| `/workspaces` | the workspaces this account holds a role in | required |
| `/workspaces/:workspaceId` | the bases in one workspace | required |
| `/bases/:baseId` | the base editor, opening the first table's first view | required |
| `/bases/:baseId/tables/:tableId/views/:viewId` | one view of one table | required |
| `/bases/:baseId/records/:recordId` | one record's fields and history | required |
| `/bases/:baseId/guards` | the guards panel | required |
| `/bases/:baseId/history` | the operation log, newest first | required |
| `/privacy` | what the product stores and for how long | none |

**Entry and redirects.** An unauthenticated request for a required route lands on `/login` and
returns to the requested route after signing in. Signing out returns to `/login` and the old token
stops working. A token that expires part-way through an action leaves the account not signed in with
nothing written. A member who reaches a base they hold no grant on is answered as though no such base
exists, never with a greyed-out editor. An unknown address renders the not-found page.

**Journeys.**

1. Sign in as `editor@example.com`, open `Campaign Planning`, land on the `Campaigns` grid, click the
   `Budget` cell on `Autumn Lantern`, type `1450.00`, press Enter. Reload. The cell reads `1450.00`,
   the `Total Hours` and `Deliverable Count` on that row are unchanged, and the detail pane beside
   the grid shows `1450.00` too.
2. As `editor@example.com`, change a task's `Minutes`. The deliverable's `Hours` changes and the
   campaign's `Total Hours` changes with it. No other campaign changes.
3. As `editor@example.com`, tick `Done` on a deliverable whose `Estimate` is empty. The write is
   refused, an inline banner carries the guard's own message exactly, and after a reload `Done` is
   still unticked.
4. Sign in as `commenter@example.com` and open the same grid. No cell is editable. Changing that
   cell by a direct request is denied and the stored value does not change.
5. Sign in as `owner2@example.com` and ask for `Campaign Planning` by its identifier. The answer is
   that no such base exists.
6. As `creator@example.com`, open `/bases/:baseId/history`, pick an operation and open the table as
   of that sequence. A full-width band names the mode, the grid takes its historical treatment, and
   no cell is editable.
7. Open `/bases/:baseId/records/:recordId` and read that record's history newest first, including
   its creation.
8. As `creator@example.com`, add two conditions joined by `AND` to the `Campaigns` grid view. The
   filter control shows a count of `2` and the rows drop to those that match. A filter matching
   nothing shows the filtered-to-nothing state naming the filter, which is not the empty state.
9. Open the command palette, type a table name, jump to it, and create a record in the slide-over.
   The new row appears at the bottom of the grid carrying an auto number one higher than the
   previous highest.
10. From the footer of any page, open `/privacy` and read what the product stores.

**States.** Every list has a written empty state. Being filtered to nothing is a different state
from being empty and names the filter responsible. Every page has a loading state. Errors never
crash the app and never leave a partial write.

## UI/UX notes

The north star: somebody opening a base understands in one look what the table holds, which view
they are in, and whether what they are reading is live. The register is operational throughout. This
is an instrument, not a brochure: quiet chrome and loud data. Density over decoration, and stability
over movement, because the same person opens the same table forty times a day and every pixel of
chrome is a pixel of data they did not get.

The governing constraint on colour is that people assign colour names to their own select choices,
so the interface's own palette is nearly colourless or it competes with the content. Ground,
surfaces, rules and text are all neutral: the ground a near-white neutral that is not quite white,
the surface records live on a lighter near-white neutral above it, toolbars and sidebars a sunk
near-white neutral below it, primary text a near-black neutral, secondary text and field names a mid
neutral, row numbers and placeholders a light neutral, grid lines a near-white neutral and the
sticky column edge a light neutral one step stronger. One accent, a mid, vivid blue, means
interactive and appears nowhere else: focus, selection edge, links and the one primary action. The
selected range fills with a near-white cool neutral wash of that same accent.

Three meaning colours, each used for one meaning and nowhere else: a mid, soft green for a guard
passing and a log that verifies; a mid, soft orange for approaching a limit and for an advisory
guard; a mid, vivid red for a blocked guard, an invalid formula and a denial. The historical read
band is a mid cool neutral, deliberately outside both the accent and the meaning families, so a mode
band can never be mistaken for a status. State is never carried by colour alone: a refusal is
coloured, carries a glyph and carries the word. The exact shades are yours, so long as they hold
those two rules.

Type is `IBM Plex Sans` at weights 400, 500 and 600 for the whole interface including the contents
of cells, chosen for unusually clear numerals and a narrow lowercase that survives a dense table.
`IBM Plex Mono` at 400 carries record identifiers, formula expressions, guard conditions and
operation payloads. `IBM Plex Serif` at 500 is reserved for `/privacy`, where a document voice is
correct and a table's voice is not. Sizes are `20px` over `28px` for a page or modal title, `16px`
over `24px` for a section heading, `14px` over `20px` for body, `13px` over `18px` for a grid cell,
`12px` over `16px` for a field header and `11px` over `14px` for a caption or row number. Nothing in
the base editor is larger than the page title. Every numeric, currency, percent, duration, rating,
count and rollup column sets its figures on tabular numerals so a column of amounts lines up.

Density is compact: rows sit tight so a full table fits one screen and somebody scans rather than
scrolls. Corners are barely softened throughout, because this is an instrument and not a card deck,
and depth is read from a hairline rather than from a shadow. The layout archetype is a command
palette first: the palette opens over any surface and is the fastest way to any workspace, base,
table, view or record, and the sidebars remain for the person who would rather point. The work
surface is a split pane with the records on one side and the selected record's detail on the other,
both visible at once, so somebody working through a table never loses their place. Creating anything
opens a slide-over panel over the current surface rather than navigating away from it. Feedback is
an inline banner that stays until it is dismissed or replaced; nothing that matters is announced in
something that disappears on its own.

Motion character is mechanical. Every transition runs short and straight, with no easing curve
bending either end of it, so a change reads as a machine answering rather than as a movement
somebody choreographed. A committed cell
does not animate at all, because the value simply is and anything else reads as
lag, and it carries no transition of any kind. A row entering or leaving a view
collapses its height while fading, and that transition is suppressed entirely when many rows change
at once, because a bulk change should land rather than cascade. Collapsing a group transitions its
height. A popover fades in while rising slightly and closes instantly. Dragging a row lifts it,
displaces its neighbours and drops instantly. Entering a historical read drops a full-width band in
and gives the grid its own treatment, and that is deliberately the most noticeable movement in the
product, because entering a non-live mode must be impossible to miss. A blocked guard
shakes the offending cell briefly alongside its authored message, and it is the only
decorative movement here because it is felt before it is read. Status crossfades rather than spinning: a state and a time
beats a spinner. Everything above is suppressed under reduced motion, where the guard shake becomes
a persistent outline and the mode band simply appears.

Each page leads with exactly one primary action, visually distinct from every secondary one: a view
leads with creating a record, the guards panel with creating a guard, and the sign-in page with
signing in. Every content image carries alternative text and a decorative image declares itself
decorative.

Accessibility floors are contract, not taste. Contrast meets WCAG 2.1 AA, and grid cell text, which
is read for hours, is held above that. Every interactive element carries a visible focus ring at a
contrast of at least 3:1 against its own background, in both themes. Touch targets are at least 44
by 44 CSS pixels. Full keyboard navigation of the grid is a correctness requirement rather than a
nicety: arrows move the selection, tab advances, Enter begins editing and Escape cancels, so the
muscle memory somebody brings from a spreadsheet works. The grid reads as a semantic table to
assistive technology whatever technique renders it, and the current cell announces its field name,
its value and its position. Icon-only controls carry labels. Each select choice colour carries a
name from the ten in the choice palette, which spans the blue, cyan, teal, green, yellow, orange,
red, pink, purple and grey families, because the colour is meaning somebody assigned and meaning
must be reachable without sight. Entering or leaving a historical read is announced, not only
banded.

The product is committed to light, with a dark theme carrying every role above at the same contrast.
Responsive behaviour holds at phone, tablet and desktop widths and at every width between them: as
the viewport narrows the left sidebar collapses to icons and then the view sidebar becomes a
dropdown, and at phone width the editor leads with the record detail rather than attempting a full
grid. The grid never reflows: it scrolls in both directions inside its own container, and the page
body never scrolls sideways at any width.

What it must not look like: no page dominated by a single hue family with no second signal, no
decoration standing in for content, no marketing composition where the working interface belongs,
and no oversized hero on a screen whose job is a table.

## Front-end specification

This section carries the detail that `## UI/UX notes` states in summary. It adds no business rule.

**The base editor.** The screen everything else is downstream of. A left sidebar lists the
workspace's bases and, inside the open base, its tables; it collapses to icons. A table bar runs
across the top carrying one tab per table with an add-table control at the end; the bar scrolls on
overflow and never wraps to a second line. A view sidebar lists the current table's views, with a
lock marker on a `locked` view and a person marker on a `personal` one. A toolbar sits above the
work surface carrying hide fields, filter, sort, group, row height, guards and historical read. Each
of those opens a popover, and each shows a count beside its name when it is currently doing
something, so an active filter is never invisible. The work surface fills the rest.

**The grid.** The header row stays put while the body scrolls, and so does the primary column while
the body scrolls sideways. A row-number gutter runs down the left carrying the row number, a control
that opens the record and a hover checkbox. An add-row control sits at the bottom and an add-field
control at the right. Columns are dragged to resize and to reorder. Selection covers a single cell,
a shift-extended range, a whole row and a whole column, and the selected range carries the accent
wash and a fill handle at its bottom-right corner. A summary row is pinned at the bottom with a
per-column aggregate chooser. A group header carries its value, its record count, its collapse state
and its per-column aggregates.

**The record detail.** The right half of the split pane, and also its own address. It carries every
field of the record including the computed ones, and that record's history newest first. Fields are
not reordered from here, because reordering belongs to the view.

**Mode chrome.** A historical read takes an unmistakable full-width band across the top of the work
surface and a distinct grid treatment underneath it. Nobody may mistake a historical read for live
data, so the band names the mode and the sequence it is reading at, and every editing affordance in
the grid is gone rather than merely disabled.

**The guards panel.** One row per guard carrying its table, its condition, its mode and its authored
message, with outstanding advisory violations listed under the guard that raised them and a link to
each violating record. The one primary action creates a guard.

**The base history.** One row per operation, newest first, carrying the sequence, the moment, the
account, the kind of change and what it touched. Opening a row shows the before and after values
side by side, set in the monospace face, and offers to open the table as of that sequence.

**The command palette.** It opens over any surface and is also reachable at `/go`. It takes typed
text and matches workspaces, bases, tables, views and records by name, groups the matches by what
they are, and moves the selection with the arrow keys. Enter goes to the selected result and Escape
closes without going anywhere.

**Empty and error presentation, all written.** An empty table reads that there are no records yet
and offers to add one. Being filtered to nothing is its own state and names the filter responsible
rather than reusing the empty-table wording. An empty group, an empty view list, a search with no
results, a base with no guards yet and a log with nothing since a chosen sequence each carry their
own sentence. A refusal appears as an inline banner naming what was refused and why, and a blocking
guard's banner carries the guard's own message unaltered.

**Components and their states.** Every control has a resting, a pointed-at, a pressed, a focused and
an unavailable state, and unavailable is never signalled by colour alone. Escape closes any popover,
slide-over or palette. A destructive action, which is deleting a record, a field, a table, a view or
a guard, asks for confirmation first and names what will be removed. A cell in edit carries a
visible edit affordance distinct from its selected state.

**Machine-readable hooks.** These exact attribute names and values are a contract. The element
holding the records carries `data-view` taking exactly `grid`, `gallery` or `kanban`. The base
editor root carries `data-mode` taking exactly `live` or `history`. A column header carries
`data-field-type` taking the field type slug exactly as spelled in the field type table. A grid row
carries `data-record-id` taking that record's identifier. A refusal banner raised by a guard carries
`data-guard-mode` taking exactly `blocking` or `advisory`.

**Type and colour restated only where the detail is new.** The monospace face carries record
identifiers, formula expressions, guard conditions and operation payloads wherever they appear,
including inside the history rows and the guards panel. The serif face appears on `/privacy` and
nowhere else. Choice chips expose their colour's name as text, and a setting renders choices with
distinguishing patterns as well as fills, so a choice is told apart without colour vision.

## Technical requirements

Nuxt 3 for the frontend and Fastify for the HTTP API, on Node 20, with PostgreSQL for storage. The
rendering model is server-rendered pages with interactive islands: the browser receives complete
HTML for a route on first paint and only the interactive parts hydrate, so the grid, the command
palette and the slide-over become live while the rest of the page is already readable. Both halves
are served from one origin on container-internal port `4173`, bound `0.0.0.0`, with the HTTP API
under the `/api` prefix on that same origin.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing service
available in this environment is `postgres`, and reaching for anything else is a contract violation.

`postgres` is already running and reachable at `DATABASE_URL`, read from the environment. The
environment also exports `DB_URL` carrying the same value. Never hardcode a host, a port or a
credential. `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` are read from the environment too.

Auth is email and password implemented by this app, with a bearer token returned at login and
carried on every endpoint except `GET /api/health`. Passwords are hashed.

`GET /api/health` returns `200` once the app is ready. Logging is one line per request to standard
output carrying the method, the path and the outcome.

The app serves a favicon and declares it in the document head, so a tab and a bookmark both show the
product's own mark rather than a blank page. Every public route declares its own social preview
title and its own social preview image, and the image resolves to a real image over HTTP rather than
to a missing file. No credential, API key, token or database URL appears in anything the browser
downloads, including the HTML the server renders, the JavaScript it serves and any data embedded in
either.

## Data model

Ten tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**accounts** - identifier, email (unique, compared without case), password hash, display name,
created at. The plaintext password is stored nowhere and returned nowhere.

**workspaces** - identifier, slug (unique), name, created at.

**memberships** - identifier, workspace, account, role, created at. One membership per account per
workspace. Role is one of `owner`, `creator`, `editor`, `commenter`, `reader`.

**base_grants** - identifier, base, account, role, created at. One grant per account per base. The
effective role on a base is the more permissive of the membership role and the grant role.

**bases** - identifier, workspace, name, created at.

**tables** - identifier, base, name, position, created at.

**fields** - identifier, table, name, type, configuration, position, whether it is the primary
field, whether it is valid, why it is invalid, created at. Name is unique within its table. Exactly
one primary field per table, at the first position, never a computed type.

**records** - identifier, table, auto number, created at, created by, deleted at.

**cells** - record, field, value, keyed by the record and the field together. Only non-computed
fields have a row here. **Computed values are derived on read and stored nowhere**: `formula`,
`rollup`, `multipleLookupValues`, `count` and `createdTime` have no stored value, and a build that
keeps one has to keep it correct, which is the thing this design removes.

**links** - identifier, link field, from record, to record. A pair appears once per link field. The
mirrored reference under the inverse field is written in the same operation.

**views** - identifier, table, name, type, mode, owning account when the mode is `personal`, and a
configuration holding filters, sorts, groups, hidden fields, row height and the stack field.

**guards** - identifier, base, table, name, condition, mode, message, created at.

**operations** - identifier, base, sequence, occurred at, actor, kind, target type, target
identifier, before, after.

**Invariants, stated as properties of the running system.**

Operation sequence numbers are unique within their base. Two writes to one base that arrive at the
same moment produce two operations with two different sequence numbers; exactly one sequence value
is issued to each, the log contains no gap and no repeat, and neither write is lost. An operation
row, once written, is never changed and never removed.

Auto numbers are unique within their table. Two records created in one table at the same moment
never receive the same auto number.

A write refused by a `blocking` guard leaves no trace: no cell row, no record row, no link row, no
recomputed neighbour and no operation row.

Deleting a record leaves no link row naming it on either side, and leaves every rollup, count and
lookup that reached it correct on the next read.

**Seed data.** Six accounts: `owner@example.com` as Nadia Holt,
`creator@example.com` as Piotr Selby, `editor@example.com` as Rosa Ibekwe,
`commenter@example.com` as Tomas Frey, `reader@example.com` as Lena Ward,
and `owner2@example.com` as Idris Vaughn.

Two workspaces. `Northfield Commercial`, slug `northfield-commercial`, with Nadia as `owner`, Piotr
as `creator`, Rosa as `editor`, Tomas as `commenter` and Lena as `reader`. `Harbourline Studio`,
slug `harbourline-studio`, with Idris as `owner` and nobody else.

`Northfield Commercial` holds one base, `Campaign Planning`, with three tables. `Campaigns` has the
primary field `Name` (`singleLineText`), `Stage` (`singleSelect` over `Planning`, `Live` and
`Wrapped`), `Budget` (`currency`), `Deliverables` (`multipleRecordLinks`), `Total Hours` (`rollup`
summing `Hours` over the linked deliverables), `Deliverable Count` (`count`) and `Owner Note`
(`formula`, seeded deliberately invalid because the field it referenced was retyped). Its three
records are `Autumn Lantern` (`Live`, `1200.00`), `Harbour Nights` (`Planning`, `800.00`) and
`Winter Ledger` (`Wrapped`, `450.00`). `Deliverables` has the primary field `Title`, `Due` (`date`),
`Done` (`checkbox`), `Estimate` (`duration`), `Tasks` (`multipleRecordLinks`), `Hours` (`rollup`
summing `Minutes` over the linked tasks) and `Task Names` (`multipleLookupValues` of the linked
tasks' `Title`); its six records are `Launch film`, `Print run`, `Site refresh`, `Press pack`,
`Signage` and `Mailer`. `Tasks` has the primary field `Title`, `Minutes` (`number`, precision `0`),
`Urgency` (`rating`, maximum `5`), `Labels` (`multipleSelects`), `Logged` (`dateTime`), `Created`
(`createdTime`) and `Ref` (`autoNumber`), with nine records.

`Harbourline Studio` holds one base, `Studio Roster`, with one table `People` whose primary field is
`Name` and whose second field is `Craft` (`singleSelect`), holding two records, `Ada Renn` and
`Bo Kessler`.

Two guards are seeded on `Campaign Planning` with the messages given in Core features, and the
operation log for that base already carries the operations that created everything above, starting
at sequence `1`, so a historical read and a record history both return something on first load.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One product, two seeded workspaces. A member reaches only what their grants reach.
- No file upload, no attachments and no object store.
- No email, no notifications and no mail vendor.
- No payment, no plans, no billing and no subscription.
- No realtime push and no presence. A change made by somebody else is seen on the next read.
- No automations, no app designer, no forms, no extensions, no scripting and no webhooks.
- No API tokens for third parties, no external synchronisation and no artificial intelligence.
- No single sign-on, no directory provisioning, no enterprise administration panel, no audit export
  and no retention policy.
- No branching, no merging, no what-if overlays, no snapshots, no record templates, no record
  colouring and no comments.
- No calendar view, no timeline view, no gantt view, no list view and no form view.
- No native application and no offline mode.
- No external network calls at run time.
- The app must stay responsive with `50000` records in a base and `500` fields on a table.

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

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `display_name` | the created account and a bearer token |
| `POST /api/auth/login` | `email`, `password` | a bearer token |
| `GET /api/auth/me` | none | the signed-in account |
| `GET /api/health` | none | a body stating the app is ready |
| `GET /api/field-types` | none | a top-level JSON array of all `19` field types with `slug` and `computed` |
| `GET /api/workspaces` | none | a top-level JSON array of the caller's workspaces |
| `GET /api/workspaces/{workspaceId}/bases` | none | a top-level JSON array of that workspace's bases |
| `GET /api/bases/{baseId}` | none | the base with its tables, fields and views |
| `GET /api/bases/{baseId}/tables/{tableId}/records` | `viewId`, `asOf` | a top-level JSON array of records with cell values and computed values |
| `POST /api/bases/{baseId}/tables/{tableId}/records` | `cells` keyed by field identifier | the created record |
| `PATCH /api/bases/{baseId}/tables/{tableId}/records/{recordId}` | `cells` keyed by field identifier | the updated record with its recomputed fields |
| `DELETE /api/bases/{baseId}/tables/{tableId}/records/{recordId}` | none | an empty success |
| `GET /api/bases/{baseId}/tables/{tableId}/records/{recordId}/history` | none | a top-level JSON array, newest first |
| `POST /api/bases/{baseId}/tables/{tableId}/fields` | `name`, `type`, `config` | the created field |
| `PATCH /api/bases/{baseId}/tables/{tableId}/fields/{fieldId}` | `name`, `type`, `config` | the updated field |
| `GET /api/bases/{baseId}/views/{viewId}` | none | the view with its configuration |
| `PATCH /api/bases/{baseId}/views/{viewId}` | `name`, `mode`, `config` | the updated view |
| `GET /api/bases/{baseId}/operations` | `since` | a top-level JSON array, newest first |
| `GET /api/bases/{baseId}/operations/replay` | none | whether the log and the data agree, and the first sequence where they do not |
| `GET /api/bases/{baseId}/guards` | none | a top-level JSON array of guards |
| `POST /api/bases/{baseId}/guards` | `tableId`, `name`, `condition`, `mode`, `message` | the created guard |
| `DELETE /api/bases/{baseId}/guards/{guardId}` | none | an empty success |

**Response shapes.** These field names are exact.

- A workspace carries `id`, `slug`, `name` and `role`, where `role` is the caller's effective role.
- A base carries `id`, `name`, `tables` and `limits`; a table inside it carries `id`, `name`,
  `fields` and `views`.
- `limits` names every structural limit and its value, under the exact keys `recordsPerBase`,
  `tablesPerBase`, `basesPerWorkspace`, `fieldsPerTable`, `viewsPerTable`,
  `filterConditionsPerView`, `filterNesting`, `groupLevels`, `sortLevels`, `kanbanStacks` and
  `guardsPerBase`. A refusal for a structural limit names the same value.
- A field carries `id`, `name`, `type`, `config`, `isPrimary` and `isValid`.
- A view carries `id`, `name`, `type`, `mode` and `config`.
- A record carries `id`, `autoNumber`, `cells` keyed by field identifier holding the stored values,
  and `computed` keyed by field identifier holding the value of every computed field on that row.
- A history entry carries `sequence`, `occurredAt`, `actor`, `fieldId`, `before` and `after`.
- An operation carries `id`, `sequence`, `occurredAt`, `actor`, `kind`, `targetType`, `targetId`,
  `before` and `after`.
- A guard carries `id`, `tableId`, `name`, `condition`, `mode` and `message`.
- A field type carries `slug`, `name`, `computed` and `config`.
- The replay answer carries `agrees` and, when the two part company, `firstDivergentSequence`.
- A refusal carries `error`, an object holding `code` and `message`; the `message` of a blocking
  guard refusal is that guard's `message` character for character.

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns the
named resource or shape. An invalid or unauthorized call is rejected as a client error, never as a
server error and never as a silent success. Bearer auth is carried on everything except
`POST /api/auth/signup`, `POST /api/auth/login` and `GET /api/health`.

**No mocks.** `postgres` is the fact. An in-memory records array, a JSON file on the app's own disk,
a SQLite file beside the app, a hardcoded response the app returns to itself, or an operation log
kept only in the running process are each a contract violation however good the interface looks. The
named provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

Somebody signs in, opens a base, changes a cell in a grid view and sees every computed field that
depends on it change with it, and after a reload the grid, the record detail and the record endpoint
all show the same value. A member of another workspace is answered as though that base does not
exist. A write a blocking guard refuses leaves the data exactly as it was and appends nothing to the
log, and the guard's own message is what the person reads.
