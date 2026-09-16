# Studio Signals

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the report, read a chapter whose every claim sits
beside the chart that supports it, narrow the whole report to the company size they work at,
watch every chart, every base and every figure inside the prose recompute without leaving the
page, and download that filtered report as a markdown document whose tables carry exactly the
numbers they just read. A signed-in reader must be able to save that document to a private
library, and nobody else, signed in or not, may ever read it.

## Overview

Studio Signals is an annual survey of how designers use AI tools, published by Northbeam Research
and Aster & Vale as a long-form report a reader works through. The 2026 wave is the second; the
first ran in 2025, and much of what the report says is movement between the two.

The report is three chapters, `01 Tools`, `02 Craft` and `03 Teams`, each a sequence of numbered
findings followed by three closers. A finding is the atom of the product: a heading that makes a
claim, a paragraph of prose, a chart rendering the figures the claim rests on, the text
equivalent of that chart, and a source line naming the wave, the segment and the base. Every one
of those is generated from one dataset of survey results stored by the service. No figure
anywhere in the product is typed into a template.

Alongside the chapters sit a set of seven case studies, three published and four announced, an
about page carrying the methodology, a markdown export of the whole report, and a generated
citation for any finding.

What the original publication cannot do, and this one must, is let a reader read it as
themselves. A reader chooses a segment (a company size, a work environment, a band of
experience, or any combination of those) and the entire report is recomputed for it, with bases
shrinking, intervals widening and figures below the reporting threshold withheld and explained.
Two segments can be read side by side, and the report says which of their differences the data
actually supports.

A reader with an account keeps their place in each chapter and their chosen segment between
visits, and can save any filtered export to a private library.

The scope boundary that defines this tier of product is a correct, stateful reading interface
over one dataset. This is not a survey tool: nobody answers questions here. It carries no quotations from real
people, no partner organisations or logos, no comment threads, no shared annotations, no film,
and no analytics of what anybody reads.

## User roles

| Role | Can | Cannot |
|---|---|---|
| visitor (no account) | read every chapter, case study and the about page; choose, combine, compare and clear segments; generate a citation; download the export; subscribe to case-study notices; sign up | save an export; keep a reading position or a stored segment |
| `reader` | everything a visitor can; save an export to their own library; download and remove their own saved exports; keep a reading position per chapter; keep a stored segment | read, download or remove another reader's saved export; change another reader's position or segment |

There is one account role. The service enforces every boundary on every request; hiding a control
in the page is never the boundary. A request for another reader's saved export, or for its
download, is answered as a missing record with `404`, never as a refusal, because a refusal
confirms the export exists.

Signup is **open**. Anyone can create a `reader` account from `/sign-up` with a display name, an
email address and a password, and the account is usable at once.

Two accounts are seeded, and every seeded account uses the password `deku-demo-pw-2026`.

| Email | Display name | Role |
|---|---|---|
| `reader@example.com` | Ines Park | `reader` |
| `reader2@example.com` | Tomas Reyes | `reader` |

`reader2@example.com` exists so that isolation is observable: each seeded reader starts with an
empty library, and an export one of them saves must read as missing to the other.

## Core features

### The dataset and its arithmetic

Everything the reader sees is an aggregate over stored `result` rows, recomputed on every request
from the dataset in `## Data model`. The rules below are the product's centre; every chart, every
heading, every takeaway, every export and every citation obeys them identically.

1. **A result is the grain.** One `result` row holds, for one wave, one question, one option and
   one profile cell (a company size, a work environment and an experience band together), the
   number of respondents who chose that option. For a numeric question it holds the sum of their
   answers in tenths. A figure is the sum over the cells a segment covers, divided by that
   segment's respondents. A figure is never stored, and never typed into a template or a sentence.
2. **The question's type decides the arithmetic.** A `single` question's shares, at full
   precision, sum to exactly one across its options. A `multi` question's shares do not sum to one
   and are not rescaled to: each option's share is its selections divided by respondents. A
   `numeric` question publishes a mean, its summed tenths divided by ten and by respondents.
3. **Rounding happens once, at display, from full precision.** A share displays as a whole
   percentage rounded half up (`0.4591` displays `46%`); a mean displays with one decimal rounded
   half up (`5.79` displays `5.8`). A movement is computed from the two full-precision values and
   only then rounded to whole points, never from two rounded shares.
4. **Movement is computed, never stored, and it has states.** Movement compares an option's 2026
   share with its 2025 share within the same segment, in percentage points. Its state is
   `not-comparable` when the question is recorded as not comparable between waves;
   `not-asked` when the option did not exist on the 2025 questionnaire; `suppressed` when the
   segment's 2025 base is below the threshold; `rise` or `fall` when the difference is supported
   and its rounded points are not zero; `no-change` when it is not supported and its rounded points
   are zero; and `not-detectable` otherwise. A `not-asked` movement is never a rise from zero.
5. **A small base is withheld, never drawn.** The reporting threshold is `30` respondents. A
   figure whose base is below it is suppressed: it is not computed into any chart, heading,
   takeaway, export row or citation, and wherever it would have appeared the product says why.
6. **Uncertainty: every share carries an interval.** Its margin, in points, is `1.96` times the square root of
   `p(1 - p) / n`, where `p` is the full-precision share and `n` the base, rounded half up to a
   whole point. The confidence level is stated once for the whole publication as
   `Figures carry a 95% confidence interval.` The interval is surfaced in words only where it
   matters: a share whose base is under `200` displays as `<share>, give or take <margin>. Based
   on <base> answers.`, for example `47%, give or take 7. Based on 195 answers.` for an agency
   segment.
7. **A difference is asserted only when the data supports it.** A difference between two shares,
   whether two segments in one wave or one segment in two waves, is supported when its absolute
   size exceeds `1.96` times the square root of `p1(1 - p1) / n1 + p2(1 - p2) / n2`. An unsupported
   difference keeps its exact values on screen and is described as not established.

A mean carries no interval and takes part in no supported-difference test, because the dataset
holds no dispersion for a numeric question.

### Segments

The reader narrows the report with three controls, one per profiling dimension, each offering
`All` plus its bands. The bands are defined once, in the dataset, and the about page's composition
and every segment breakdown read that one definition.

| Dimension | Address key | Bands (slug and label) |
|---|---|---|
| Company size | `size` | `startup` Startups (1 to 50), `growth` Growth (51 to 500), `scale-up` Scale-up (501 to 2K), `enterprise` Enterprise (2,000+) |
| Work environment | `env` | `in-house` In-house, `agency` Agency, `freelance` Freelance |
| Experience | `exp` | `under-10` Under 10 years, `10-plus` 10 years or more |

Controls compose: choosing a size and an environment yields their intersection, whose base is
smaller than either. A segment's label joins the chosen band labels in dimension order with a
comma and a space, for example `Startups (1 to 50), Agency`; the whole population's label is
`all respondents`.

The segment lives in the address as query parameters, `?size=startup&env=agency`, on every
chapter route and every finding anchor, and the sidebar's chapter links, the rail and the previous
and next controls all carry the segment in force, so a shared link reproduces exactly the figures the sender
saw. The interface always states the segment in force, including the default:
`Showing all respondents.` when nothing is chosen, and
`Showing <label>. <segment base> of <population> respondents.` otherwise, for example
`Showing Startups (1 to 50). 223 of 869 respondents.`

Clearing is one action, `Show everyone`, always available while a segment is in force.

An address that arrives carrying a segment shows `This link opens the report filtered to <label>.`
An address carrying a band that does not exist, such as `?size=galactic`, resolves to the whole
population and says `That link asks for a group this report doesn't have. Showing everyone.`
rather than rendering an empty report.

The interaction obligations of segmentation: changing a segment recomputes the chapter in place
without navigating: the address updates, the
finding under the reader's eye stays under it, and one announcement is made to assistive
technology, `Now showing <label>, <segment base> respondents.`, not one per chart. While the
recomputation is in flight the control reads `Recalculating for <label>.`

### Comparison

A second segment, set with the same three dimensions under `vs_size`, `vs_env` and `vs_exp`, turns
the chapter into a comparison: every share row carries the second segment's value and base beside
the first's, and every chart carries both series. The state line reads
`Comparing <label A> with <label B>.`

Each compared share row states whether its difference is supported under rule 7. A finding's
comparison sentence reads `<label A> <share A>, <label B> <share B>.` followed by
`A real difference between these two groups.` when the focus row's difference is supported, or
`Too close to call for these two groups.` when it is not. `<share A>` and `<share B>` are the
focus option's displayed shares in each segment; a finding with a numeric question, or with no focus
option to name, carries no comparison sentence. A difference between two segments is
drawn with a different treatment from a movement between two waves.

Suppression is per side: when the second segment's base is below the threshold, the chapter shows
the first segment alone and says `<label B> has too few respondents to compare.`

### Chapters and findings

Chapters are one collection rendered by one template, in a reading order that is data. Each
chapter carries its findings in the order below and then three closers, in this order:
`Where do we go from here?`, `Key takeaways` and `Relevant posts & resources`.

| Chapter | Number | Finding id | Short title | Question | Form | Focus option |
|---|---|---|---|---|---|---|
| `tools` | `01` | `usage-frequency` | How often designers use AI | `usage-frequency` | `part-to-whole` | `daily` |
| `tools` | `01` | `stack-ranked` | What is in the stack | `stack-tools` | `ranked-bars` | the top-ranked option |
| `tools` | `01` | `stack-movement` | How the stack moved | `stack-tools` | `movement-list` | the largest supported rise |
| `craft` | `02` | `tool-count` | How many tools | `tool-count` | `segment-breakdown` | `tools` |
| `craft` | `02` | `confidence-by-size` | Confidence by company size | `confidence` | `segment-breakdown` | `very` |
| `craft` | `02` | `stick-reasons` | What makes a tool stick | `stick-reasons` | `ordered-ranking` | the top-ranked option |
| `teams` | `03` | `craft-shift` | How the craft shifted | `craft-shift` | `two-wave` | `substantially` |
| `teams` | `03` | `team-policy` | Written team policies | `team-policy` | `two-wave` | `written` |
| `teams` | `03` | `hiring-outlook` | Hiring outlook | `hiring-outlook` | `part-to-whole` | `grow` |

**The forms.** A finding names its question, its form and its focus, and the chart is derived;
no chart holds its own copy of a number. All figures are from the 2026 wave unless a form says
otherwise.

- `part-to-whole` shows every option of a `single` question in option order, with its share. It
  is refused for a `multi` or `numeric` question.
- `ranked-bars` shows every option ordered by full-precision share, highest first, ties broken by
  option order, with the share printed against each bar.
- `ordered-ranking` lists the options in that same order as a numbered list with the values
  withheld, and a control reveals the values on request.
- `movement-list` shows every option in option order with its 2025 share, its 2026 share and its
  movement, whose cell reads `+19pts` for a rise, `-9pts` for a fall, `No change since 2025.`,
  `No detectable change since 2025.`, `Not asked in 2025`,
  `Asked differently in 2025, so the two are not compared.` or `Too few 2025 answers to compare.`
  for the other states. Those states never render alike.
- `two-wave` shows the focus option's 2025 and 2026 shares as a pair with its movement cell; when
  the question is not comparable it shows 2026 alone with
  `Asked differently in 2025, so the two are not compared.`
- `segment-breakdown` shows the focus option, or the mean for a numeric question, for each company
  size band intersected with the segment in force, each band printing its own base. A band whose
  base is below the threshold reads `not reported, base too small`.

In both ranked forms, two adjacent options whose difference is not supported under rule 7 are
marked together with `These two are too close to separate.`

**Headings are regenerated from the data.** A finding's heading is produced from the segment in
force by the template below, so it can never contradict the chart beneath it. `<share>` is the
focus option's displayed share, `<mean>` the displayed mean, and `<movement>` the focus option's
movement phrase: `up <n> points since 2025`, `down <n> points since 2025`,
`no change since 2025`, `no detectable change since 2025`, `not asked in 2025`,
`asked differently in 2025` or `too few 2025 answers to compare`.

| Finding | Heading template | With the seed, all respondents |
|---|---|---|
| `usage-frequency` | `<share> use AI tools every day, <movement>.` | `46% use AI tools every day, up 16 points since 2025.` |
| `stack-ranked` | `<label> is the most common tool in the stack, used by <share>.`, or when the top two are too close to separate, `<label 1> and <label 2> are the most common tools in the stack, too close to separate.` | `Canvas assistant is the most common tool in the stack, used by 59%.` |
| `stack-movement` | `<label> rose the most, <movement>.` naming the option with the largest supported rise, ties broken by option order, or `No tool in the stack rose detectably since 2025.` when none rose | `Canvas assistant rose the most, up 19 points since 2025.` |
| `tool-count` | `Designers use <mean> AI tools in a typical week.` | `Designers use 5.8 AI tools in a typical week.` |
| `confidence-by-size` | `<share> are very confident judging AI-assisted work.` | `23% are very confident judging AI-assisted work.` |
| `stick-reasons` | `<label> is the first reason a tool sticks.`, or `<label 1> and <label 2> are the first reasons a tool sticks, too close to separate.` | `Speed is the first reason a tool sticks.` |
| `craft-shift` | `<share> say their core craft changed substantially, <movement>.` | `29% say their core craft changed substantially, up 6 points since 2025.` |
| `team-policy` | `<share> work in a team with a written AI policy.` | `38% work in a team with a written AI policy.` |
| `hiring-outlook` | `<share> expect their design team to grow next year.` | `34% expect their design team to grow next year.` |

Under `?size=startup` the same templates read, among others,
`Canvas assistant and Image generator are the most common tools in the stack, too close to separate.`
and `31% say their core craft changed substantially, no detectable change since 2025.`

**A withdrawn finding.** When the segment's 2026 base is below the threshold, every finding in
the chapter is withdrawn for that segment: its heading reads `<short title>: not reported for this
group.`, for example `Hiring outlook: not reported for this group.`, and its chart is replaced by
`Too few respondents in this group to report. <base> answered.` rather than by an empty frame or
by zeros. Under `?size=growth&env=freelance`, twenty respondents, every finding reads this way.

**Prose.** Each finding carries at least one paragraph of prose written for this build, and any
figure inside it is interpolated from the same resolved result as the heading. A sentence whose
figure is suppressed is rewritten with `not reported for this group` in the figure's place.

**Source line.** Every figure carries its provenance: the wave, the question, the segment and the
base. Beneath every chart,
`Source: Studio Signals survey, 2026 wave, <label>, base <segment base>.`, for example
`Source: Studio Signals survey, 2026 wave, all respondents, base 869.`, followed by the short
caveat `Directional, not a benchmark. See methodology.` linking to the methodology.

**Text equivalent.** Every chart has a table headed `The figures behind this chart` stating the
same values in the same order, with the base, present in the page for every reader and used
unchanged by the export.

**Addresses.** Every finding is addressable at `/chapters/<chapter>#<finding id>`, carrying the
segment's query parameters when one is in force.

**The rail.** A sidebar lists every finding by short title and then the three closers, each a link
to its position. It marks exactly one entry as current, visually with a leading rule and
programmatically as the current location, and the current entry is the section the reader is
reading: a chapter scrolled to its end marks its last entry.

**Closers.** `Key takeaways` is a numbered list with one entry per finding, whose text is that
finding's regenerated heading and whose link goes to the finding, so a takeaway can never assert a
figure its finding no longer shows. `Relevant posts & resources` lists further reading as works
with a title, an author and a publication. `Where do we go from here?` poses open questions in
prose.

**Chapter head and navigation.** A chapter opens with its number, its title and a reading time
computed from its own words, `<n> min read, charts excluded`, at two hundred and thirty words a
minute rounded up. It ends with controls to the previous and next chapters, each showing the
sibling's number and title, such as `02 . Craft`; the first chapter has no previous control and
the third no next control.

### Case studies

The case-study set is seven positions, numbered `01` to `07`. Numbering belongs to the set, so an
announced study keeps its number before and after it is published.

| Position | Slug | Subject | Category | State |
|---|---|---|---|---|
| `01` | `harbour-type` | Harbour Type Co. | `TYPE FOUNDRY` | published |
| `02` | `kestrel-health` | Kestrel Health | `HEALTHCARE` | published |
| `03` | `fieldwork-studio` | Fieldwork Studio | `AGENCY` | published |
| `04` | `lumen-transit` | Lumen Transit | `MOBILITY` | announced |
| `05` | `oakline-bank` | Oakline Bank | `FINANCE` | announced |
| `06` | `parcel-and-post` | Parcel & Post | `LOGISTICS` | announced |
| `07` | `quarry-games` | Quarry Games | `GAMES` | announced |

A published study is served at `/cases/<slug>` with its number, subject, category, a one-line
description and a body of written notes. It carries no survey figures and no quotations. An
announced study renders its number, its subject and `Coming soon`, and is not a link;
`/cases/<slug>` for an announced study answers `404` with the not-found page, as does its API
record.

### About and the methodology

`/about` is headed `About this report` and states what the report is, that Northbeam Research and
Aster & Vale produce it, that the 2026 wave follows the 2025 wave, the four readerships it is
written for (design leaders making tooling decisions; designers thinking about their craft and
careers; founders and product teams; students and educators), a credits list by role, and the
methodology.

The methodology states the population of each wave, that the survey was fielded in March of each
year, and the composition by company size, by work environment and by experience, every one
computed from the same dataset the chapters read. The 2026 population is `869` and the 2025
population `709`. It states the confidence level once and the reporting threshold, and carries the
directional caveat in full:

`Because of how the survey was distributed, the sample may lean towards designers who already use AI tools more than most, or who work where adoption is actively supported. We present these findings as directional rather than as absolute benchmarks.`

Every chapter links to the methodology.

### The export

The export is a markdown rendering of the same resolved model the pages render, produced by one
code path; it is never a scrape of a page and never a separately maintained file. Every figure in
it equals the figure on the page for the same segment.

Anyone can download it without an account and without giving an address:
`GET /api/export.md` with the segment's query parameters answers `200` with
`text/markdown; charset=utf-8` and an attachment named `studio-signals-2026.md`. The cover and
every chapter offer it as `Download the report as markdown`, carrying the segment in force.

Markdown is the one format offered. The document is laid out exactly as follows.

- Line 1, the head: `# Studio Signals, 2026 wave. Exported <YYYY-MM-DD>. <Label>.`, where
  `<Label>` is `All respondents` for the whole population and the segment label otherwise, and
  the date is the day of export in UTC. A comparison appends `Comparing <label A> with <label B>.`
- Line 3: `Directional, not a benchmark. See methodology.`
- Line 4: `Figures carry a 95% confidence interval.`
- For each chapter in order, a `## <number> <title>` heading, such as `## 01 Tools`, then for
  each finding a `### <heading>` line carrying the regenerated heading, then the finding's table,
  then its source line.
- The table for `part-to-whole`, `ranked-bars` and `ordered-ranking` has the header
  `| Option | 2026 | Base |` and one row per option in the chart's order, such as
  `| Every day | 46% | 869 |`.
- The table for `two-wave` and `movement-list` has the header `| Option | 2025 | 2026 | Change |`,
  whose `2025` cell is `Not asked in 2025` for a `not-asked` option and `Not compared` for a
  `not-comparable` or `suppressed` movement, and whose `Change` cell is the
  movement cell text.
- The table for `segment-breakdown` has the header `| Company size | 2026 | Base |`, and a
  suppressed band's row reads `| Growth (51 to 500) | not reported, base too small | 20 |`.
- A withdrawn finding exports its heading and `Too few respondents in this group to report.
  <base> answered.` in place of its table.

### The library

A signed-in reader saves an export to a private library through a three-step wizard, each step
its own address, each carrying the choices so far in its query parameters:

| Step | Route | What it asks |
|---|---|---|
| 1 | `/library/new` | the segment, prefilled from the segment the reader came from |
| 2 | `/library/new/compare` | an optional second segment to compare with, or none |
| 3 | `/library/new/review` | shows the export's head line and its figure count, then `Save to library` |

Saving calls `POST /api/exports`, which answers `201` with the record. `/library` shows the
reader's saved exports as a grid of cards, newest first, each with its label (the segment label, or
`Comparing <label A> with <label B>` for a comparison), its date, a download link and `Remove`. A
library with nothing in it reads `Nothing saved yet.` with a link to `/library/new`. Removing a card
removes it at once and restores it with `Could not remove that export.` if the service refuses.

The rules a saved export obeys:

1. **A saved export is one object in the store.** Saving renders the export for the chosen segment
   and stores the rendered bytes as one object under the key `exports/<account id>/<export id>.md`,
   and records the export. The stored object's bytes are exactly the bytes `GET /api/export.md`
   returns for the same segment on the same day. Bytes kept anywhere else do not count.
2. **A saved export is readable only by the reader who saved it.**
   `GET /api/exports/{id}/download` streams the object with `text/markdown; charset=utf-8` to its
   owner. The same request from any other reader answers `404`, and a request with no session
   answers `401`; neither returns a byte of the document, and the record and the object stay
   unchanged.
3. **Only the owner can remove it.** `DELETE /api/exports/{id}` from the owner deletes the record
   and its object from the store; the same request from another reader answers `404` and leaves
   both in place.
4. **The store is not a way around the service.** The bucket carries no anonymous read policy, so
   a request straight to the store for an export's key is refused.

### Citation

Any finding can be cited: `Cite this finding` beneath every chart shows a citation generated from
the finding as displayed, in three shapes built from one object, a sentence, a structured record
and the address alone. The sentence reads:

`Studio Signals, 2026 wave. "<heading>" Base <segment base>, <label>. Directional, not a benchmark. See methodology. Retrieved <YYYY-MM-DD> from <address>.`

The address reproduces exactly that view: the chapter route, the segment's query parameters and
the finding anchor. A citation of a filtered figure also carries
`This citation records that you filtered to <label>.`

### Reading position

A signed-in reader's place is kept per chapter as the finding they reached, never as a scroll
offset. As the reader moves through a chapter the page records the current finding; the record is
the finding's id, or `closers` once the reader reaches the closers.

Returning to a chapter at a recorded position offers
`You were part-way through <number> <title>. Pick up where you left off?` with a link to the
finding; resuming is offered, never forced, so the page does not scroll there on its own. The cover's contents shows each chapter's state:
`Not started` with no record, `Part-way through` with a finding recorded, and `Finished` once
`closers` is recorded. A position survives a reload, signing out and signing back in, and a new
browser.

A signed-in reader's segment is also kept. Opening a chapter with no segment in the address
applies the stored segment by redirecting to the address that carries it. Opening an address that
carries a segment stores that segment, replacing the previous one. `Show everyone` stores the whole
population, and its address carries `segment=all`.

Nothing about what a reader reads is sent anywhere other than this service, and the account page
says so.

### Accounts

`/sign-up` asks for a display name of `1` to `60` characters, an email address and a password of
`8` to `200` characters, links to `/terms`, and creates a `reader`. `/sign-in` signs an account in.
A wrong password and an unknown address answer with the same message,
`That email and password do not match`; an address already registered answers
`That email is already registered`. Signing in returns a bearer token for the API and sets an
HTTP-only session cookie for pages; the API accepts either. Signing out ends both.

`/library` and every `/library/new` step without a session redirect to `/sign-in?next=` followed
by the requested path, and return there after signing in.

### Terms

`/terms` is a page of terms of use for the report, reachable from the footer of every page and
linked from the sign-up form. It states that the report's figures are directional, that a saved
export is private to its reader, and how to delete an account.

### Case-study notices and spam protection

The cover and the footer carry a separate, opt-in form, `Get new case studies`, asking for an email
address and an explicit consent checkbox; downloading the report never requires it.
`POST /api/subscriptions` answers `201` and records the address once.

Both this form and the sign-up form carry a decoy field named `website`, hidden from people and
from assistive technology. A submission with anything in `website` is refused with `400` and
creates nothing. A form submitted repeatedly, a second subscription submission for the same address
within sixty seconds of the first, is refused with `429` and creates nothing.

### Not found and links

Any path that does not resolve renders the report's own not-found page, headed `Page not found`,
with a link back to the cover reading `Back to the report`, inside the full chrome, and answers
`404`. Every internal link on every public page resolves to a page that answers `200`.

## User flow

### Routes

The information architecture is three kinds of route, a cover, a chapter template and a case-study
template, plus standing pages.

| Route | Document title | What it is |
|---|---|---|
| `/` | `Studio Signals 2026` | the cover: the title block, the contents with each chapter's state, the case-study set, the export and the case-study notice form |
| `/chapters/tools` | `01 Tools \| Studio Signals` | chapter one |
| `/chapters/craft` | `02 Craft \| Studio Signals` | chapter two |
| `/chapters/teams` | `03 Teams \| Studio Signals` | chapter three |
| `/cases/<slug>` | `<subject> \| Studio Signals` | a published case study |
| `/about` | `About \| Studio Signals` | about the report and the methodology |
| `/terms` | `Terms \| Studio Signals` | terms of use |
| `/sign-in` | `Sign in \| Studio Signals` | sign in |
| `/sign-up` | `Sign up \| Studio Signals` | create a reader account |
| `/library` | `Library \| Studio Signals` | the reader's saved exports |
| `/library/new` | `Save an export \| Studio Signals` | wizard step 1, the segment |
| `/library/new/compare` | `Save an export \| Studio Signals` | wizard step 2, the comparison |
| `/library/new/review` | `Save an export \| Studio Signals` | wizard step 3, review and save |
| anything else | `Page not found \| Studio Signals` | the not-found page, answering `404` |

Three destinations head the sidebar on every page: `About`, `Case Studies` (the set on the cover)
and `Read the Report`, which goes straight to `/chapters/tools` rather than to a contents page.
Beneath them the sidebar lists the chapters as `01 Tools`, `02 Craft`, `03 Teams`, and on a
chapter the rail and the segment control. `Library` or `Sign in` closes the list. The footer on
every page reads `©2026 Northbeam Research, Aster & Vale. All rights reserved`, with the year taken
from the wave, and links `About`, `Terms` and the methodology.

### Entry and redirects

| Route | Visitor | Reader |
|---|---|---|
| public routes | renders | renders |
| `/chapters/<chapter>` with no segment in the address | renders for all respondents | redirects to the address carrying the stored segment, when one is stored |
| `/sign-in`, `/sign-up` | renders | redirects to `/library` |
| `/library`, `/library/new`, `/library/new/compare`, `/library/new/review` | redirects to `/sign-in?next=<path>` | renders |
| `/cases/<slug>`, announced | not found, `404` | not found, `404` |

A `next` value is used only when it is a path on this site beginning with a single `/`; any other
value sends the reader to `/`.

### Journeys

**A visitor reads as themselves.** They open `/`, choose `Read the Report` and land on
`01 Tools`. The sidebar marks `How often designers use AI` as current, and the heading reads
`46% use AI tools every day, up 16 points since 2025.` beside a chart of five options and its
source line naming all respondents and base 869. They set company size to Startups; without the
page navigating, the address gains `?size=startup`, the state line reads
`Showing Startups (1 to 50). 223 of 869 respondents.`, the heading becomes
`55% use AI tools every day, up 16 points since 2025.`, and the next finding's heading now says two
tools are too close to separate. They download the report as markdown and its first line reads
`# Studio Signals, 2026 wave. Exported <today>. Startups (1 to 50).`

**A visitor compares.** On `02 Craft` with Startups in force they set the comparison to
Enterprise. The state line reads `Comparing Startups (1 to 50) with Enterprise (2,000+).`, every
share row gains a second value, and the confidence finding says
`Startups (1 to 50) 30%, Enterprise (2,000+) 17%. A real difference between these two groups.`

**A visitor narrows too far.** They set Growth and Freelance. Every finding in the chapter is
withdrawn with `Too few respondents in this group to report. 20 answered.`, and the export for
that segment carries the same sentence under each heading.

**A reader keeps a private copy.** They sign in as `reader@example.com`, open `03 Teams` with
Enterprise in force, and choose `Save to library`. The wizard walks the segment, no comparison and
the review, and `Save to library` lands them on `/library` with a new card labelled
`Enterprise (2,000+)`. Its download carries the same numbers as the page. Signed in as
`reader2@example.com`, that export's download answers `404`.

**A reader comes back.** Half-way through `01 Tools` they sign out. Later, signed in again, the
cover's contents shows `01 Tools` as `Part-way through`, and opening the chapter offers
`You were part-way through 01 Tools. Pick up where you left off?`

**A mistyped path.** `/chapters/methods` renders `Page not found` with `Back to the report` and
answers `404`.

### States

| Surface | Loading | Empty | Error |
|---|---|---|---|
| a chapter after a segment change | the control reads `Recalculating for <label>.` and the chart stays at its last values | every finding withdrawn with its reason | `Could not recalculate. Showing <previous label>.` and the previous figures stay |
| `/library` | cards appear as they load | `Nothing saved yet.` with a link to `/library/new` | `Could not load your library.` |
| removing an export | the card leaves at once | `Nothing saved yet.` once the last card leaves | the card returns with `Could not remove that export.` |
| the export download | none; the file downloads | never empty: every finding exports, suppressed or not | the chapter shows `Could not prepare the export.` |

## UI/UX notes

A reader should feel they are holding a well-edited research publication that happens to be
interactive, not a dashboard. The register is plain, unhurried and willing to say what it does
not know. Hierarchy is carried by type size and whitespace alone.

**Flat and square.** The page is ink on a white ground. Nothing is rounded except circles, and
nothing casts a shadow, except the solid block behind the cover title. A build that adds rounded
cards and drop shadows to feel finished has made a different product.

**Colour by role.** Near-black neutral ink on a near-white neutral ground, with the ink turned down
to sixty per cent for secondary text; a mid neutral for tertiary labels; and one accent, a light,
vivid orange, that does all the chart work for a single series. A second series in a comparison is
a deep neutral, so the two are told apart by value as well as by hue. The accent is one token used
everywhere, so a chart and its key can never drift apart. Every link declares its own colour in
every state.

**Typography: two families, two cuts.** `Public Sans` carries everything read as language at cut 400 and cut
500; `JetBrains Mono` carries small uppercase labels and the finding numbers. Long reading and
labelling take different leading, stated once and used consistently.

| Role | Face | Size | Cut | Line height |
|---|---|---|---|---|
| Cover title | Public Sans | `85px` | 500 | `85px` |
| Chapter title | Public Sans | `80px` | 500 | `80px` |
| Chapter number | JetBrains Mono | `48px` | 500 | `48px` |
| Finding heading | Public Sans | `24px` | 500 | `28.8px` |
| Body prose | Public Sans | `16px` | 400 | `22.4px` |
| Chart value and chart label | Public Sans | `14px` | 500 | `19.2px` |
| Captions and source lines | Public Sans | `13px` | 400 | `15.6px` |
| Rail entries | Public Sans | `14px` | 500 | `19.6px` |
| Uppercase labels and case-study categories | JetBrains Mono | `12px` | 400 | `14.4px` |

No figure renders below `13px`; no prose renders below `16px`.

**Motion is an entrance, never a state.** A chart's bars grow from zero once, the first time the
chart enters the window, over a little under a second on a strong ease-out, each bar starting a
short moment after the one before it, with the stagger worked out from the bar's position so an
eleven-bar chart staggers eleven times. A chart never re-animates on scrolling back, and a chart
that finished animating looks identical to one that never animated. The animation is drawn as a
stretch, never as a change of width. Each easing curve is named once and written once. Links move their colour and underline together on a
symmetrical ease. The chapters themselves are still while being read. With reduced motion
requested, every chart renders at its final values with no growth and no stagger, a segment change
moves bars straight to their new values, and the cover's moving ground holds a still frame.

**Accessibility.** Body text and chart values meet the WCAG AA contrast bar of 4.5:1 against their
ground, including secondary text and the rail's inactive entries. Links in prose are underlined at
rest. Every chart has its text equivalent, and colour never carries the only distinction. A
chart's values are reachable in order by keyboard, each announcing its option, its value and its
base. The rail is a navigation landmark whose current entry is marked programmatically. Keyboard
navigation reaches every link and control in reading order, with a visible focus outline. A
segment change is announced once and keeps focus where it was. Exactly one instance of each
navigation element is in the accessibility tree.

**Responsive.** One element per component, arranged responsively. At a wide window the prose sits
beside its chart and the rail is a sticky column on the left; at a narrow window the prose sits
above its chart, and a claim and its chart are never separated. At a narrow window the rail
becomes a control that opens the section list, still marking the current section. A chart never
makes the page scroll sideways: labels move above their bars, and the text equivalent is always
there. Body prose holds a comfortable measure at every width. At two hundred per cent zoom nothing
is lost and nothing scrolls sideways.

## Front-end specification

### Tokens

The design system is small enough to hold in one head, and it is declared once as named tokens
rather than scattered as literals.

| Token | Colour | Role |
|---|---|---|
| `ink` | a near-black neutral | all text and rules |
| `ground` | a near-white neutral | the page |
| `ink-secondary` | the ink at sixty per cent strength | secondary text, inactive rail entries |
| `ink-tertiary` | a mid neutral | tertiary labels only where contrast still holds |
| `panel` | a near-white neutral, faintly cool | the text-equivalent table and the citation panel |
| `accent` | a light, vivid orange | the single series in every chart, the rail's leading rule |
| `compare` | a deep neutral, the second dark | the second series in a comparison |
| `lavender` | a near-white, soft indigo | the band behind a segment state line |
| `sage` | a pale sage, a near-white neutral faintly green | the band behind a comparison state line |

The categorical set for any chart that needs more than one hue is a light, muted lime, a near-white,
soft amber and a light, muted cyan, chosen to stay distinguishable when printed grey; a sequential
scale, where one is needed, runs from a near-white, soft cyan through a light, vivid cyan to a
light, vivid blue, and stays ordered in greyscale. A categorical scale and a sequential scale are
different objects and never substitute for each other.

Radius is zero everywhere except circles. Layering uses eleven contiguous stacking levels and no
large arbitrary values. The finding marks and the rail's leading rule are inline
vectors written into the markup.

### Layout

A chapter is two columns at a wide window: the sidebar with the destinations, the chapters, the
segment and comparison controls and the rail, sticky on the left; and the content column holding a
comfortable measure of prose on the right. Each finding is one region in reading order: its number
in the monospace face, its heading, its prose, its chart, the text equivalent, the source line and
`Cite this finding`. At a wide window the prose sits in a narrower column beside the chart; at a
narrow window it sits above. Nothing may split a finding's heading from its chart, whether a column
break, a lazy load or a page break.

### The charts

A chart is drawn by the server from the resolved finding as plain markup, one row per value, and
enhanced in the browser only for the reveal.

- **Bars** are horizontal, in the accent, square-ended, each labelled above its bar with the option
  label on the left and the value on the right, so a long label never competes with its bar for
  width.
- **Part-to-whole** stacks the option shares in one full-width bar with a key beneath it listing
  each option and share, the options told apart by a pattern of alternating tints as well as by
  position.
- **Two-wave** is two bars for the focus option, 2025 in the tertiary neutral above 2026 in the
  accent, with the movement cell to the right.
- **Movement list** is rows of option, 2025 share, 2026 share and movement cell; a rise and a fall
  carry an upward or downward mark beside the signed points, while the other states are words with
  no mark.
- **Ranked bars** is bars ordered highest first; two neighbours too close to separate are joined
  by a bracket carrying `These two are too close to separate.`
- **Ordered ranking** is a numbered list with no bars, a `Show the values` control revealing each
  share, and the same bracket for neighbours too close to separate.
- **Segment breakdown** is one bar per company size band, each with its base printed under its
  label; a withheld band shows its label, its base and `not reported, base too small` in place of a
  bar.
- **Comparison** adds the compare series beneath each accent bar in the deep neutral, with each
  row's value pair and a small marker reading `supported` or `too close to call`. A movement mark
  never appears on a comparison row, so a difference between groups never looks like a change over
  time.

Every chart's values form a keyboard sequence: the chart takes focus as one stop, and the arrow
keys move through its rows, each announcing `<option>, <value>, base <base>`.

A share whose base is under two hundred prints its interval in words beneath its bar. Every chart
prints its base and source, and both change with the segment.

### The reveal

A little under a second per bar on a strong ease-out, each bar starting a short moment after the
one above it for horizontal bars, a slightly longer moment for vertical ones. The reveal is
triggered once per chart per page load when the chart first enters the window, and a chart already
above the window on load renders at its final values. A segment change while bars are still
growing sends them straight to the new values. Compositing hints are applied to a bar only while it
moves.

### The sidebar and the rail

The sidebar is one element that is arranged differently at different widths. At a wide window it
is a sticky column whose rail marks the current section with a short leading rule in the accent
and the ink, the other entries in the secondary ink with no rule. At a narrow window the navigation is collapsed to a bar at the top of the chapter carrying the chapter title, the segment state and a
`Sections` control that opens the list as a sheet, which closes on choosing an entry or on escape
and returns focus to the control. The current entry is the section whose heading most recently
passed a line about a third of the way down the window, and the last entry once the document is
scrolled to its end.

### The segment and comparison controls

Three selects in the sidebar, `Company size`, `Work environment` and `Experience`, each with `All`
first, then `Compare with` which reveals a second set of three. A change submits at once and swaps
the chapter body in place. The state line sits above the first finding, on the lavender band for a
segment and the sage band for a comparison, with `Show everyone` beside it.

### The cover

A full-width title block: a solid near-black block carrying `Studio Signals` over two lines at the
cover size with `2026` beneath, over a moving ground generated in the page as a slow drift across a
many-stop radial gradient of the categorical colours with a fine grain overlay, and a scatter of
rectangular collage tiles, each a two- or three-stop gradient with grain, placed by a fixed seed so the
cover is the same on every visit. Each tile carries a small uppercase monospace caption naming one
of the four readerships; the captions are editorial copy, not data. Under reduced motion the ground
holds still.

Below the title block: the contents, listing the three chapters with number, title, reading time
and, for a signed-in reader, the chapter's state; the case-study set as a card grid, each card its
number, subject, category and either a link or `Coming soon`; the export link; and the notice form.

### Chrome

Links in running prose are underlined at rest in the ink, and on hover their colour, underline
colour, underline thickness and underline offset move together on a symmetrical ease. Destination
links in the sidebar are not underlined at rest and show the underline on hover and focus.

### Print

The report prints. Page breaks fall between findings, never inside a finding and never inside a
chart. Charts print legibly in grey. The sidebar, the controls, `Cite this finding`, the export
link and the notice form do not print; the segment in force, printed as
`Printing the report as currently filtered: <label>.`, the bases, the source lines and the caveat
do. Every external link prints its address after it.

### Performance

The budget, per route, uncached, at a wide window: everything before the first paint of the title under
`250KB`; script before a chapter is readable under `120KB`; fonts under `150KB`, delivered as one
`woff2` request per face subset to the characters used; the cover's moving ground drawn in the page
with no video and no photograph. A chapter is readable before any script runs, because the server
sends finished markup. No source maps are served in production.

### Compound cases, and the answer this build gives

| Case | Answer |
|---|---|
| A segment changes while a chart is mid-reveal | the bars go straight to the new values |
| A segment withdraws the finding the reader is reading | the withdrawn finding keeps its place and its short title, so the position holds |
| A resume position refers to a finding the dataset no longer has | the chapter opens at the top with `This chapter has changed since you were last here. Starting at the top.` |
| An address carries a segment while a stored one differs | the address wins and replaces the stored one |
| The export is requested while a recomputation is in flight | the export uses the segment in the address at the moment of the request |
| A comparison's verdict changes as the segment narrows | the sentence is regenerated with the new verdict in the same swap as the chart |
| A deep link lands on a finding under a segment that withdraws it | the page scrolls to the withdrawn finding, which states why |
| The report is printed during a recomputation | print uses the figures on screen, which are the previous segment's until the swap lands |

## Technical requirements

Server-rendered pages. Every route's HTML is produced on the server from templates, and the
browser receives finished markup on first paint; the segment controls, the rail, the reveal and
the library are enhanced in place.

| Layer | What to use |
|---|---|
| Server | Node.js 22 with Express, rendering Nunjucks templates |
| Interactive parts | HTMX for the segment and comparison swaps, the wizard steps and the library removal; small hand-written scripts for the rail, the reveal and the cover ground |
| Datastore | PostgreSQL, reached with `pg` at `DATABASE_URL` |
| Object store | MinIO, reached with `@aws-sdk/client-s3` at `STORAGE_ENDPOINT`, bucket `STORAGE_BUCKET`, credentials `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY` |
| Typefaces | `@fontsource/public-sans` and `@fontsource/jetbrains-mono`, served by the app |

Use only the libraries named here plus their direct dependencies, Node's built-in modules, and an
Express session or cookie middleware. Do not introduce a second database, cache, queue, object
store, identity provider, charting service or analytics vendor: the only backing services available
in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract
violation.

**One query layer.** Aggregation, movement, suppression, intervals, supported differences, ranking
and heading generation live in one module that is a pure function of the dataset and the segment.
The chapter pages, the chapter API, the export, the library save and the citation all call it; none
of them computes a figure of its own.

**Identity.** Email and password, implemented by this application. `POST /api/auth/sign-in` returns
a bearer token and sets an HTTP-only, same-site session cookie; every API route accepts either the
`Authorization: Bearer` header or the cookie. A password is stored only as a salted one-way hash
and never returned. Signing out revokes the token and ends the session.

**Exports in the store.** A saved export's object key is `exports/{account_id}/{export_id}.md`,
its content type `text/markdown; charset=utf-8`. The bucket carries no anonymous read policy;
`GET /api/exports/{id}/download` is the only path a saved export travels to a browser.

**Status codes.** An unmatched path answers `404` with the not-found page; so does an announced
case study. Another reader's saved export and its download answer `404`. A request needing a
session that has none answers `401`. An invalid body answers `400` with the error body in
`## Deployment contract`; a subscription repeated within sixty seconds answers `429`.

**Seeding.** On start the application creates its schema and seeds the dataset, the chapters, the
findings, the case studies and the accounts in `## Data model` when they are absent. Starting twice
leaves exactly one copy of every seeded row.

**Performance.** Everything before the title paints under `250KB`, script before a chapter is
readable under `120KB`, fonts under `150KB`, and a chapter's resolved model computed under `300ms`
for any segment.

## Data model

**Entities.** Each entity is one table named exactly as the entity, and each field named below is a
column of the same name.

`account` carries `id`, `email`, `display_name`, a password hash and `created_at`.

`cell` carries `wave` (`2025` or `2026`), `size`, `env`, `exp` and `respondents`: one row per wave
and profile cell.

`question` carries `slug`, `type` (`single`, `multi` or `numeric`), `wording`, `comparable` and
`position`. `option` carries `question`, `slug`, `label`, `position` and `asked_2025`.

`result` carries `wave`, `question`, `option`, `size`, `env`, `exp` and `count`: the respondents in
that cell who chose that option, or for a numeric question the sum of their answers in tenths. An
option not asked in 2025 has no 2025 rows.

`chapter` carries `slug`, `number`, `title` and `position`. `finding` carries `id`, `chapter`,
`position`, `short_title`, `question`, `form` and `focus`.

`case_study` carries `position`, `slug`, `subject`, `category`, `state` (`published` or
`announced`), `description` and `body`.

`progress` carries `account_id`, `chapter`, `finding` and `updated_at`: one row per reader and
chapter. `preference` carries `account_id`, `size`, `env` and `exp`: one row per reader.

`export` carries `id`, `account_id`, `storage_key`, `size`, `env`, `exp`, `vs_size`, `vs_env`,
`vs_exp`, `label` and `created_at`; a segment column holds a band slug, or null when that dimension
was not chosen. `subscription` carries `id`, `email` and `created_at`.

**Field rules.**

| Field | Rule |
|---|---|
| `account.email` | unique, trimmed, lowercased |
| `account.display_name` | `1` to `60` characters |
| `export.storage_key` | follows `exports/{account_id}/{export_id}.md` and is unique |
| `progress.finding` | a finding id of that chapter, or `closers` |
| `subscription.email` | a valid address, trimmed, lowercased |

**Invariants.**

- A figure exists only as an aggregate over `result` rows computed at request time.
- A saved export and its object are readable only by the account that saved it.
- An export's object bytes equal the export rendered for the same segment on the same day.
- Removing an export removes its record and its object.

**Seed: respondents.** Each row is one profile cell's respondents in each wave. The 2025 population
is `709`, the 2026 population `869`.

| Size | Environment | Experience | 2025 | 2026 |
|---|---|---|---|---|
| `startup` | `in-house` | `under-10` | 52 | 60 |
| `startup` | `in-house` | `10-plus` | 21 | 25 |
| `startup` | `agency` | `under-10` | 41 | 48 |
| `startup` | `agency` | `10-plus` | 17 | 20 |
| `startup` | `freelance` | `under-10` | 30 | 40 |
| `startup` | `freelance` | `10-plus` | 26 | 30 |
| `growth` | `in-house` | `under-10` | 74 | 90 |
| `growth` | `in-house` | `10-plus` | 36 | 45 |
| `growth` | `agency` | `under-10` | 31 | 38 |
| `growth` | `agency` | `10-plus` | 18 | 22 |
| `growth` | `freelance` | `under-10` | 9 | 12 |
| `growth` | `freelance` | `10-plus` | 7 | 8 |
| `scale-up` | `in-house` | `under-10` | 66 | 85 |
| `scale-up` | `in-house` | `10-plus` | 49 | 60 |
| `scale-up` | `agency` | `under-10` | 16 | 20 |
| `scale-up` | `agency` | `10-plus` | 12 | 15 |
| `scale-up` | `freelance` | `under-10` | 4 | 5 |
| `scale-up` | `freelance` | `10-plus` | 3 | 4 |
| `enterprise` | `in-house` | `under-10` | 88 | 110 |
| `enterprise` | `in-house` | `10-plus` | 79 | 95 |
| `enterprise` | `agency` | `under-10` | 15 | 18 |
| `enterprise` | `agency` | `10-plus` | 11 | 14 |
| `enterprise` | `freelance` | `under-10` | 2 | 3 |
| `enterprise` | `freelance` | `10-plus` | 2 | 2 |

**Seed: questions.**

| Slug | Type | Wording | Comparable |
|---|---|---|---|
| `usage-frequency` | `single` | How often do you use AI tools in your design work? | yes |
| `stack-tools` | `multi` | Which of these tools are part of your working stack? | yes |
| `tool-count` | `numeric` | How many AI tools do you use in a typical week? | yes |
| `confidence` | `single` | How confident are you judging the quality of AI-assisted work? | yes |
| `stick-reasons` | `multi` | What makes a tool stick in your workflow? | yes |
| `craft-shift` | `single` | Has your core craft changed in the last year? | yes |
| `team-policy` | `single` | Does your team have a written policy on AI tools? | no, the wording changed in 2026 |
| `hiring-outlook` | `single` | Do you expect your design team to grow next year? | yes |

**Seed: results.** Every `result` count is generated from the table below, cell by cell, and
stored. For an option with a rate, in permille, the count for a cell is the cell's respondents
multiplied by the option's rate for that wave plus the shift for the cell's company size, clamped
to the range `0` to `1000`, divided by `1000` and rounded down. A `remainder` option, always the
last option of a `single` question, takes the cell's respondents minus the counts of the question's
other options. For `tool-count` the rate and shift are tenths of a tool, and the count is the cell's
respondents multiplied by the rate plus the shift, the sum of that cell's answers in tenths. Options
are stored in the order listed.

| Question | Option (slug and label) | 2025 | 2026 | `startup` | `growth` | `scale-up` | `enterprise` |
|---|---|---|---|---|---|---|---|
| `usage-frequency` | `daily` Every day | 310 | 470 | +90 | +20 | -30 | -70 |
| `usage-frequency` | `weekly` Every week | 280 | 250 | -10 | +10 | +20 | -10 |
| `usage-frequency` | `monthly` Every month | 170 | 120 | -30 | 0 | +20 | +20 |
| `usage-frequency` | `rarely` Rarely | 140 | 100 | -30 | -20 | 0 | +40 |
| `usage-frequency` | `never` Never | remainder | remainder | remainder | remainder | remainder | remainder |
| `stack-tools` | `canvas-assistant` Canvas assistant | 420 | 610 | +60 | +20 | -20 | -60 |
| `stack-tools` | `image-generator` Image generator | 520 | 548 | +40 | +10 | -10 | -40 |
| `stack-tools` | `code-copilot` Code copilot | 300 | 300 | -20 | 0 | +20 | +30 |
| `stack-tools` | `research-summariser` Research summariser | 380 | 280 | -30 | 0 | +10 | +30 |
| `stack-tools` | `prototype-builder` Prototype builder | not asked | 330 | +80 | +20 | -30 | -70 |
| `tool-count` | `tools` Tools per week | 41 | 58 | +14 | +4 | -6 | -12 |
| `confidence` | `very` Very confident | 180 | 240 | +60 | +20 | -20 | -60 |
| `confidence` | `fairly` Fairly confident | 410 | 430 | 0 | +10 | 0 | -10 |
| `confidence` | `slightly` Slightly confident | 250 | 220 | -30 | -10 | +10 | +30 |
| `confidence` | `not` Not confident | remainder | remainder | remainder | remainder | remainder | remainder |
| `stick-reasons` | `speed` Speed | 610 | 640 | +40 | 0 | -20 | -30 |
| `stick-reasons` | `quality` Quality | 450 | 520 | 0 | +10 | 0 | -10 |
| `stick-reasons` | `team-standard` Team standard | 300 | 500 | -120 | 0 | +60 | +110 |
| `stick-reasons` | `integration` Integration | 400 | 440 | -10 | +10 | 0 | 0 |
| `stick-reasons` | `cost` Cost | 350 | 330 | +70 | +10 | -30 | -60 |
| `craft-shift` | `substantially` Substantially | 240 | 300 | +30 | 0 | -10 | -20 |
| `craft-shift` | `somewhat` Somewhat | 450 | 440 | 0 | 0 | 0 | 0 |
| `craft-shift` | `barely` Barely | remainder | remainder | remainder | remainder | remainder | remainder |
| `team-policy` | `written` Yes, written down | 220 | 380 | -150 | -20 | +60 | +140 |
| `team-policy` | `drafting` It is being drafted | 260 | 240 | -40 | +10 | +20 | +10 |
| `team-policy` | `none` No policy | remainder | remainder | remainder | remainder | remainder | remainder |
| `hiring-outlook` | `grow` Grow | 380 | 350 | +60 | +10 | -20 | -40 |
| `hiring-outlook` | `hold` Hold steady | 420 | 440 | -20 | 0 | +10 | +10 |
| `hiring-outlook` | `shrink` Shrink | remainder | remainder | remainder | remainder | remainder | remainder |

For example, the 2026 count for `usage-frequency` `daily` in the cell `startup`, `in-house`,
`under-10` is `60 × (470 + 90) ÷ 1000` rounded down, `33`.

**Seed: chapters and findings.** The chapters and findings are the two tables in
`## Core features`, stored in that order.

**Seed: case studies.** The seven positions in `## Core features`, each published study with a
one-line description and a body of at least three paragraphs of written notes carrying no survey
figure and no quotation.

**Seed: accounts.** The two readers in `## User roles`, each using the password `deku-demo-pw-2026`,
each with an empty library, no progress and no stored segment. The credentials are written to
`/app/USER_README.md`.

## Constraints

- No survey findings, quotations, partner names, partner logos or credited names from any real
  publication; every figure comes from the dataset in `## Data model`.
- No partner set and no partner disclosure, because this report has no partners.
- No film, no video file and no photograph; the cover's ground and tiles are drawn in the page.
- No accounts beyond the `reader` role, no comments, no shared annotations, no highlights.
- No analytics and no third-party script of any kind; nothing about what a reader reads leaves this
  service.
- No figure typed into a template, a sentence, a takeaway or an export.
- No transition declared on every property at once; transitions are declared per property.
- The export never sits behind the notice form, and the notice form is never pre-checked.
- Research integrity: no generated figure, heading or citation may assert more than the data supports.

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

Segment parameters are the query keys `size`, `env` and `exp`, and for a comparison `vs_size`,
`vs_env` and `vs_exp`, on every route that resolves figures.

| Endpoint | Request | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status": "ok"}` |
| `GET /api/report` | none | `publication`, `wave`, `previous_wave`, `chapters` (each `slug`, `number`, `title`, `reading_minutes`, `findings` of `id` and `short_title`) and `case_studies` (each `position`, `slug`, `subject`, `category`, `state`) |
| `GET /api/segments` | none | `threshold`, `confidence`, `population` (`2025`, `2026`) and `dimensions`, each `key`, `label` and `bands` of `slug`, `label` and `respondents` (`2025`, `2026`) |
| `GET /api/chapters/{slug}` | segment parameters | `chapter` (`slug`, `number`, `title`, `reading_minutes`), `segment` (`label`, `base`, `population`), `comparison` (`label`, `base`, `suppressed`, or null), `notice` (a string or null), `findings` and `takeaways` |
| `GET /api/cases/{slug}` | none | `position`, `slug`, `subject`, `category`, `description`, `body`; `404` for an announced study |
| `GET /api/chapters/{slug}/findings/{id}/citation` | segment parameters | `sentence`, `url`, `filtered_note` (a string or null) and `record` of `publication`, `wave`, `finding`, `heading`, `base`, `segment`, `retrieved`, `url` |
| `GET /api/export.md` | segment parameters | the markdown document |
| `POST /api/auth/sign-up` | `display_name`, `email`, `password`, `website` | the account with `id`, `email`, `display_name`, `role`, and `token` |
| `POST /api/auth/sign-in` | `email`, `password` | the account and `token`, and sets the session cookie |
| `POST /api/auth/sign-out` | none | an empty body |
| `GET /api/auth/me` | none | the account |
| `GET /api/progress` | none | a top-level JSON array, one per chapter in order, of `chapter`, `finding` (or null) and `state` (`not-started`, `part-way`, `finished`) |
| `PUT /api/progress/{chapter}` | `finding` | the chapter's progress row |
| `GET /api/preferences` | none | `size`, `env`, `exp`, each a band slug or null |
| `PUT /api/preferences` | `size`, `env`, `exp` | the preferences |
| `POST /api/exports` | `size`, `env`, `exp`, `vs_size`, `vs_env`, `vs_exp`, each optional | `201` and the export with `id`, `label`, `storage_key`, `created_at` |
| `GET /api/exports` | none | a top-level JSON array of the reader's own exports, newest first |
| `GET /api/exports/{id}/download` | none | the stored markdown |
| `DELETE /api/exports/{id}` | none | an empty body |
| `POST /api/subscriptions` | `email`, `consent`, `website` | `201` and `id`, `email` |

A resolved finding in `findings` carries `id`, `number`, `short_title`, `question`, `type`,
`form`, `heading`, `base`, `suppressed`, `message` (the withdrawal sentence, or null), `source`,
`comparison_sentence` (or null) and `rows`. A row carries `option`, `label`, `value` (the
full-precision share as a fraction, or the full-precision mean, or null when withheld), `display`,
`base`, `margin_points` (or null for a mean), `movement` (`state` and `points` in a `part-to-whole`, `two-wave` or
`movement-list` row, and null otherwise), `previous` (the displayed 2025 share in a `two-wave` or `movement-list` row, or null when the
movement is `not-asked`, `not-comparable` or `suppressed`),
`tied_with_next` (in a ranked form), `option` holding the company size band slug in a `segment-breakdown` row, `suppressed` (in a breakdown), and `compare` (`value`,
`display`, `base`, `suppressed`, `supported`) in a comparison. `takeaways` is an array of `finding`
and `text`, one per finding in order.

Field names are exact. A successful call returns the named resource or shape, and an invalid or
unauthorized call is rejected as a client error, never as a server error and never as a silent
success. Every error body carries `error`, a human-readable message, and `field`, the name of the
field at fault or null. An unknown band in a segment parameter is not an error: the response
resolves for all respondents and `notice` carries the unknown-segment sentence.

### No mocks

The figures this product reports have to be aggregates over rows in PostgreSQL, and every saved
export has to exist in MinIO. A chapter typed into a template, a figure cached as rendered text, a
heading written by hand, an export written to the application's disk or into a database column, a
library held in memory, and a private export hidden only by leaving its card out of another
reader's page while its download still answers are each a contract violation however convincing
the page looks.

## Definition of done

A stranger reads a chapter, narrows the report to Startups and sees every chart, base, heading and
figure in the prose recompute in place, then downloads a markdown export whose tables carry those
same figures. A narrow enough segment is withheld and explained rather than drawn. A reader saves a
filtered export to their library, and it exists in the store as that same document, readable by
nobody else.
