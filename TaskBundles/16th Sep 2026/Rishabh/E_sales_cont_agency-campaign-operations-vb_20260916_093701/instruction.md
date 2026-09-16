# Agency Campaign Operations

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser and read the campaign `Night Signal` in Japanese and in English, with its
full ordered credit list and its award results, without hitting an error page.
Two things cannot be faked in the app itself. A creative cleared for
one car maker must NOT be able to learn anything about the rival car maker's
work by any means: not from a list, a search, a suggestion, a report, a staff
profile, an audit trail or an error message. And a campaign under embargo must
be unreachable to the public by any means, its film and stills included: the
bytes must live as real objects in the `minio` bucket at their scheme's key and
be served only through the app's own authorising handler once the embargo lifts;
a copy on the app container's own disk does not count.

## Overview

`KURO\MEIDO` is two deliverables sharing one design system.

The first is the agency's public site: a bilingual, kinetic-typography showcase
of its campaigns, its newsroom and its awards, with the methodology page, the
company record, careers, sustainability, contact and the legal set. Every public
route except preview links exists in Japanese at the root and in English under the
`/en/` prefix.

The second is the operations platform behind it, under `/studio`: the system the
agency actually runs on. Competing client accounts are walled from one another.
Account directors open briefs, producers staff crews and track budgets against a
rate card, creatives and strategists move work through internal review and client
approval, legal clears rights per market, and an editor publishes a finished
campaign with its full credit list to the public site in two languages.

The public site is a portfolio and the platform is the organisation that produced
it. Every credit line, client name and medal tally on the site is an assertion the
platform must be able to make truthfully. The genuinely hard part is that the
agency serves two rival car makers at once, `Hoshino Motors` and
`Tsubame Automotive`, and neither may ever learn anything about the other's work.

What this product is not: there is no client login, no self-service signup, no
executive dashboard, no global administrator, no payments, no invoicing, no mail
delivery, no chat and no third-party analytics.

## User roles

Five platform roles, and anonymous visitors who read the public site. Signup is
closed: every platform account is seeded. Every studio read is also bounded by the
confidentiality wall in `## Core features` rule 1, whatever the role.

| Role | Can read | Can write |
|---|---|---|
| `account_director` | briefs, jobs, work, credits and costs on accounts they are cleared for | opens briefs on accounts they own; approves estimates on the client's behalf; converts a brief into a job; records a client's approval of a work version; records case-study permission; grants and revokes clearances on accounts they own. **Cannot** write estimates, staff crews, record rights, lift a legal hold or publish |
| `producer` | the same, plus rate cards and the people directory | writes estimates; staffs crews and ends assignments; records time and third-party cost; publishes rate cards; closes periods; adds people, renames them and records a departure; withdraws a work version not under hold. **Cannot** approve an estimate, record rights, lift a legal hold or publish |
| `creative` | jobs they are cleared for, their files, comments and costs | uploads work versions; sets internal review status; comments; records their own time. Strategists, planners, technical directors, engineers and AI specialists sign in as `creative` too. **Cannot** approve an estimate, staff a crew, record rights, edit credits or publish |
| `legal` | jobs they are cleared for, with their rights and holds | records rights clearances; places a legal hold; lifts a legal hold with a reason. **Cannot** publish or edit credits |
| `editor` | jobs they are cleared for, campaigns, articles, the awards desk and the page-view log | creates campaign and article records; edits translations and credit lists; uploads hero media; records award entries and results; creates and revokes preview links; publishes and unpublishes. **Cannot** grant clearances, record rights or lift a legal hold |

The agency's other actors fold into these five: the awards manager's work is the
editor's awards desk, and talent and people administration is the producer's.
There is no executive role. Officers appear on the public company record only, and
nobody holds a standing exemption from the wall.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `creative` session
to any `editor`-only, `producer`-only, `legal`-only or `account_director`-only
endpoint must be rejected by the server (an unauthorized request is denied, not
served), leaving the protected state unchanged.

Seeded accounts, each with the password `deku-demo-pw-2026`:

| Email | Role | Person | Cleared for |
|---|---|---|---|
| `account_director@example.com` | `account_director` | Rin Takeda | `hoshino-motors`, `kagerou-beverages` |
| `account_director2@example.com` | `account_director` | Sora Imai | `tsubame-automotive`, `aozora-airlines`, `minato-rail` |
| `producer@example.com` | `producer` | Kenji Mori | `hoshino-motors`, `kagerou-beverages`, `aozora-airlines`, `minato-rail` |
| `producer2@example.com` | `producer` | Aya Fujita | `tsubame-automotive`, `kagerou-beverages` |
| `creative@example.com` | `creative` | Haru Ueno | `hoshino-motors`, `kagerou-beverages` |
| `creative2@example.com` | `creative` | Mei Sato | `tsubame-automotive` |
| `legal@example.com` | `legal` | Daichi Ono | `hoshino-motors`, `kagerou-beverages`, `aozora-airlines`, `minato-rail` |
| `editor@example.com` | `editor` | Yui Kondo | `hoshino-motors`, `kagerou-beverages`, `aozora-airlines`, `minato-rail` |

`account_director@example.com` owns `hoshino-motors` and `kagerou-beverages`;
`account_director2@example.com` owns `tsubame-automotive`, `aozora-airlines` and
`minato-rail`.

## Core features

In one view, the rules below require: the confidentiality wall on every read path
(rule 1); work bytes in the `minio` bucket at their scheme's key (rule 9); a
four-condition publication gate (rule 24); embargoed campaigns unreachable, bytes
included, and released on time with nobody present (rule 25); per-field bilingual
fallback (rule 27); and, on the public site, terms and privacy pages linked from
every footer, a designed not-found page, a page-view log, a sitemap and robots file,
and alternative text on every content image (rules 36 to 40).

**1. The confidentiality wall.** A person reads a job only while they hold a
current clearance for **every** account that job belongs to. Clearance is granted
per person per account, carries a start and an end date, and is revoked when
someone moves between competing accounts. The wall is one predicate applied to
every read path, not a filter in one list view. For a person outside the wall, a
job does not exist anywhere: absent from the job list, from internal search, from
autocomplete, from the jobs export, from the burn report's totals, from a
colleague's assignment history in the people directory; its audit trail answers exactly as a missing job does; and a direct
fetch of its identifier returns the same not-found status and the same body shape
as an identifier that never existed, so the difference never confirms existence.
Its files are never served to that person. The seeded job `Hoshino EV Launch`
carries the in-progress campaign `Midnight Charge`; `creative2@example.com` finds no
trace of either, while `creative@example.com` reads both in full. No account, whatever its role, reads every job: there is no bypass.

**2. Split jobs take the intersection.** A job may belong to several accounts,
as a co-branded campaign does. Its apportionment divides the whole in basis points
and must sum to exactly `10000`; a conversion whose shares sum to anything else is
refused and writes nothing. Its wall is the **intersection** of its accounts'
walls: a person must be cleared for every one of them. The seeded split job
`Sky Tea Partnership` belongs to `kagerou-beverages` at `6000` and
`aozora-airlines` at `4000`; `producer@example.com` reads it, and
`creative@example.com`, cleared for `kagerou-beverages` only, gets a not-found.
Someone cleared for only one of the accounts reads nothing of the job, so neither
client learns of the other's involvement.

**3. Competing accounts and cooling-off.** Each client carries a competitor set;
`hoshino-motors` and `tsubame-automotive` compete. A clearance for an account
whose client competes with a client the person currently holds, or held within
the last `90` days, is refused: the person must serve the cooling-off period and
hold neither in between. Membership of a client-dedicated unit derives a clearance
for that unit's account and excludes its competitors, so the org chart and explicit
grants can never disagree. `Hoshino Unit` is dedicated to `hoshino-motors` and
`Kagerou Studio` to `kagerou-beverages`.

**4. Briefs become jobs.** A brief is opened by an `account_director` against one
or more accounts they own. It carries the business problem, the convention to be
broken in the methodology's own terms, the deliverables, the deadline, an
indicative budget and the markets it runs in. A brief becomes a job **only** when
it has an approved estimate, a named producer and a rate card pinned to it; a
conversion missing any of the three is refused and creates no job. A `producer`
writes the estimate and an `account_director` approves it on the client's behalf;
a revised estimate needs that approval again. A `creative` attempting an approval
is denied and the estimate stays unapproved.

**5. Rate cards are pinned.** A rate card is a versioned table of role to hourly
rate in whole yen with an effective date range. The current card is the one with the
latest effective start on or before today whose range has not ended. On conversion a
job pins the card that is current at that moment and keeps it for life. Publishing a newer card
changes no cost on any job already converted, and a report run last month still
reproduces. The seeded card `RC-2026` is current at first start; the older
`RC-2025` stays pinned to the jobs behind the 2025 campaigns.

**6. Time and cost.** Time is recorded against a job, by person and role, in whole
minutes. Its cost is the pinned card's hourly rate for that role times the minutes,
divided by sixty, in whole yen, rounded half up. Worked example: `450` minutes as
`Art Director` on a job pinned to `RC-2026` costs `90000`, because the hourly rate
is `12000`. A third-party cost records the original amount in that currency's minor
units, the original currency, the converted amount in yen, the exchange rate used
and the date of that rate, all exactly as entered: `125000` in `usd` converted at
`148.50` on `2026-03-31` is `185625` yen, and later exchange rates never touch it.
A job's cost is its time cost plus its converted third-party costs, and the ledger
currency is `jpy`. Money is held as integers throughout.

**7. Closed periods are corrected forward.** A `producer` closes a calendar month.
Correcting a time entry whose month is closed leaves the original entry exactly as
it was and creates a new adjusting entry, in an open period, that references the
original and carries the difference in minutes and in cost. Correcting an entry in
an open month simply updates it.

**8. Crews are dated and append-only.** A crew is a set of dated assignments: a
person, a role, a start date, an end date and the minutes committed per week.
Replacing someone ends their assignment and opens another; an assignment is never
deleted, and a request to delete one is refused. The history therefore still says
who was on a job in any week. A person's committed minutes per week across all
overlapping assignments may never exceed their capacity. An assignment that would
exceed it is refused. Where the producer can read every conflicting job, the
refusal names them. Where any conflicting job is walled from that producer, the
refusal says exactly `That person is fully committed in the weeks you selected.`
and nothing else: no job title, no identifier, no count. A person may be staffed
only onto a job whose every account they are cleared for, so a person cleared for
`tsubame-automotive` is refused on `Hoshino EV Launch`. Roles carry seniority:
`Creative Director` and `Senior Creative Director` are different roles.

**9. Work files are versioned.** Every job holds numbered versions of its work,
counted from `1`. A new upload is a new version and never overwrites an earlier
one. Each version's bytes are stored in `minio`, the S3-compatible object store, at
the key `jobs/{job_id}/versions/{version_number}/{sha256_of_bytes}.{ext}`, for
example `jobs/7f3c2a/versions/3/9f2a...d0.png`. The database row records where the
bytes are; the bucket is where they are. Hero films and stills of a campaign are stored the
same way at `campaigns/{campaign_id}/{sha256_of_bytes}.{ext}`, and reach the public only
through the app's public asset handler once the campaign is public. Version bytes are served only to people
the wall admits, through the app's own authorising handler.

**10. Two review tracks.** Each version carries two independent statuses. The
internal track, set by a `creative` for the crew's creative leadership, is one of
`pending`, `approved`, `changes_requested` or `withdrawn`. The client track, set by
an `account_director` on the client's behalf, is one of `pending`, `approved` or
`changes_requested`. Setting one never changes the other: a version may be
client-approved and internally withdrawn at the same moment.

**11. Comments stay where they were made.** A comment attaches to one version and
to a timecode or a region of it, never to the job, so a comment made on version `3`
still reads correctly once version `4` exists. Each comment carries a visibility,
`internal` or `client`. The client view of a version carries its `client` comments
and **never** an `internal` one, on any endpoint, in any field.

**12. Rollback adds, never removes.** Restoring an earlier version creates a new
version whose bytes and digest are the earlier one's and which records the version
it restored. The versions in between remain, because a legal hold may protect them.

**13. Rights clearance per market.** Nothing publishes without clearance. A
`legal` user records rights per job: `music` (track, licence, term, territories,
permitted media), `talent` (each performer, their term, territories, permitted
media and buyout), `imagery` (stock or commissioned source and its licence terms),
`claims` (the substantiation for each factual claim in the copy), `trademark`
(permission for third-party marks in the work) and `festival_exhibition`. Every
right has a term and a set of markets, written as two-letter country codes such as
`JP`, `US` and `DE`. Festival exhibition is its own right: showing work to a jury in
a territory is never assumed from a media clearance. Clearance for a market is
complete on a given day when the job has at least one right whose territories
include that market, and every right whose territories include that market is
`cleared` and runs on that day.

**14. Rights expire per market, unattended.** On the day a right's term ends, the
campaign leaves the public site in the markets that right covered and stays
visible in every market where its rights still run, with nobody pressing anything.
The seeded campaign `Tide Clock` is published to `JP` and `DE`; its talent buyout
for `DE` ended the day before the app first started, so it is absent from every
public read for market `DE` and present for market `JP`.

**15. Legal hold outranks everything.** A `legal` user places a hold on a job under
dispute. While it holds, no version of that job may be deleted, no assignment
altered and no comment removed, and every retention schedule is suspended for that
job, whatever a client's deletion request says. Lifting a hold needs the `legal`
role and a written reason; a lift without a reason is refused, and a `producer`
attempting a lift is denied with the hold left in place. Placing and lifting a hold
are audited with the actor, the time and the reason.

**16. Credits are an ordered list of entries.** A published campaign carries the
crew that made it. An entry is a role, in Japanese and in English, and one or more
people credited jointly. A role may appear more than once in one list, and the
order is an editorial decision stored exactly as the editor set it, never
recomputed alphabetically or by seniority. A compound role such as
`Technical Director and Programmer` is one role. The seeded campaign
`Night Signal` shows the pattern: `Experience Planner` appears twice, and one
`Producer` entry credits `Yuto Baba`, `Riko Nishi` and `Sho Ota` together.

**17. Credits must be true.** A person can be newly added to a credit list only if
they hold, or have held, a dated assignment on the campaign's job, and only while
they hold a current clearance for every account of that job; either failure refuses
the whole save and leaves the list unchanged. People already on a list, departed
people included, stay on it when the list is saved again. Credits survive departure: a person who
leaves stays credited on everything they made. A person who changes their name is
shown under the new name on every credit list, except on entries where the editor
pinned names, which keep the name under which the work was made.

**18. Credit lists never lose a colleague's edit.** Every credit list carries a
revision. A save states the revision it was read at. Two saves from the same
revision cannot both succeed: exactly one is accepted and the other is refused as a
conflict, with the list unchanged, and the studio shows the person both their
version and the current one so nothing is silently discarded. Every mutation is safe
to repeat, and a conflict always gets a real presentation in the studio, never a silent
last-write-wins, which on a credit list deletes a colleague's correction.

**19. Departure and return.** When a `producer` records a departure, the person's
assignments end on the departure date, their clearances are revoked, their capacity
drops to zero and their record becomes `departed`; nothing cascades and every credit
stays. A departed person's record stays resolvable inside the studio for the audit
trail and is never shown publicly as a profile. A `producer` records a return, which sets the record back to `active` with a weekly
capacity of `2400` minutes. A person who returns keeps their
identity and credit history, gains new assignments, and needs fresh clearances,
which are never restored automatically; moving between the two car accounts on
return still serves the cooling-off period.

**20. The people directory.** A person carries names in both scripts, a reading for
collation, roles with seniority, a unit, a weekly capacity in minutes, clearances
with their dates, skills and an employment status. A colleague without clearance
for a job sees that person's assignment history with the walled assignments removed
and no hint that anything was removed, not even a count.

**21. Awards are counted, never typed.** An award body has its own name, season,
deadlines, fee schedule, categories and ranks. A category is a path of a section
and a category name within one body. Ranks belong to their body: `Lotus Festival`
awards `Grand Lotus`, `Gold`, `Silver`, `Bronze` and `Jade Petal`, and `Jade Petal`
exists at no other body; `North Star Awards` awards `Gold`, `Silver`, `Bronze` and
`Merit`. A rank may count toward another: `Grand Lotus` is its own rank and also
counts toward `Gold`. An entry is one campaign in one category of one body in one
year; a second entry with the same campaign, body, category and year is refused.
One campaign may therefore hold several results from one body in one year.

**22. Only confirmed results are published.** An entry's status is `submitted` when
it is made. Recording an unconfirmed result makes the entry `shortlisted`; confirming
a result, or closing the entry with no result, makes it `closed`. Only confirmed
results reach any public surface; a shortlist is never shown as a win. Entries cost
money, so each entry's fee is recorded as a third-party cost in yen on the
campaign's job, and each entry records the client's permission as a reference.

**23. One tally behind every total.** A campaign's award list, a news article's
per-campaign breakdown and the agency-wide tally are three views of the same
confirmed results. Confirming one result moves all three together. The headline
figure per rank rolls each rank into the rank it counts toward. For
`Lotus Festival` in `2025` the itemised results are `Grand Lotus` 1, `Gold` 2,
`Silver` 2, `Bronze` 2 and `Jade Petal` 2, nine in all, and the headline reads
`Gold` 3, `Silver` 2, `Bronze` 2 and `Jade Petal` 2. `Jade Petal` stays its own
rank in every tally and is never folded into another rank.

**24. The publication gate.** An `editor` publishes a campaign to chosen markets,
and all four conditions must hold: clearance is complete and unexpired for those
markets; the client has granted case-study permission, which an
`account_director` records separately from approving the work, because clients
routinely approve a campaign and refuse its use as agency promotion; the credit
list has at least one entry and passes rule 17; and any embargo has lifted, or the
publish is a scheduled one. A refused publish changes nothing and lists every
failed condition by name among `clearance`, `case_study_permission`, `credits` and
`embargo`, the last for an immediate publish of a campaign whose embargo moment is still
ahead. A scheduled publish whose release moment falls
after any of its rights ends is refused at scheduling time, naming the reason
`rights_expire_before_release`, with the notice
`The campaign cannot be published yet: clearance for one market expires before the scheduled date.`

**25. Embargo is unreachability.** A campaign or article may carry an embargo
moment with a timezone. Before that moment it is absent from every index, feed,
the sitemap and public search; its public address answers with the same not-found
status and screen as an address that never existed, never with a forbidden screen;
and its hero film and stills are never served to the public, whatever address is
tried. The seeded campaign `Silent Aurora` is embargoed until
`2099-01-01T09:00:00+09:00`. At the embargo moment the item becomes reachable
everywhere at once with nobody present: the seeded campaign `Harbour Lights` is
scheduled for release ninety seconds after the app first starts, and from then on
it is public with no further action.

**26. Preview links.** An `editor` creates a preview link for an unpublished or
embargoed campaign for the client or a festival jury. A preview link is signed,
expires after the minutes it was created with, can be revoked individually, and its
responses forbid indexing. The link opens at `/preview/<token>`. A revoked or expired
link answers not-found.

**27. Bilingual content, per field.** An item has one identity and a translation per
locale, `ja` and `en`. Each translation has its own status: `absent`, `drafted`,
`in_translation`, `reviewed` or `published`. Fallback is uniform on every surface
and happens per field: a published translation of a field is shown; a field whose
translation is absent or unpublished shows the other locale's published text, with
the element's language attribute set to that other locale so screen readers switch
voice; an item with no published translation in either locale does not exist in
either, absent from indexes and not-found at its address; and a sentence is never
finished in the other language. The seeded campaign `Quiet Engine` has a published
English title and no English description, so in English its title is English and
its description is the Japanese original marked `ja`. `Rice Field Radio` exists in
Japanese only. `Winter Kite` has no published translation at all and is therefore
absent everywhere. Credit names fall back per name. A campaign published in only
one language is listed and served in both, the missing language falling back field
by field: `Rice Field Radio` is on the English work index, and its English address
shows the Japanese text marked `ja`. The language switch of rule 28 is the one place
that sends a reader to the index instead.

**28. Language switching keeps your place.** Switching language on a campaign opens
the same campaign in the other language. Where that campaign has no published
translation in the target language, the switch opens the work index in the target
language with the note
`That campaign is not yet available in English, so here is all of our work.` and
never the home page or a not-found screen. A page shown through fallback carries
`The page is not yet available in English; showing the Japanese original.`

**29. Collation and dates.** Japanese sorts by reading, not by character code, so
every name that can be sorted carries a reading. The client register in Japanese
lists `Aozora Airlines`, `Kagerou Beverages`, `Tsubame Automotive`,
`Hoshino Motors`, `Minato Rail` in that order; in English it lists
`Aozora Airlines`, `Hoshino Motors`, `Kagerou Beverages`, `Minato Rail`,
`Tsubame Automotive`. Dates render in English in the long form, `21 June 2025`, and
in Japanese in the era-agnostic numeric form, `2025年6月21日`.

**30. Search finds Japanese.** Public search finds a campaign by its Japanese title,
its English title, or its reading, and any run of characters inside a Japanese
title matches, because Japanese has no spaces between words. Searching `信号` finds
`Night Signal`, whose Japanese title is `夜の信号`, and so does searching its reading
fragment `しんごう`, while a search split on spaces alone would find almost
nothing.

**31. The work index.** Campaigns are listed newest first with their total count,
twelve per page, numbered. A year facet offers all, then one entry per year for the
five most recent years that hold published work, newest first, then `before`,
which collects everything older than the oldest listed year. That boundary is
derived from the published work every time and moves as years roll over; it is
never hard-coded. The year and the page both live in the address as query
parameters, so a filtered view is linkable and survives a reload. Choosing a year
resets to page one, and a page number that no longer exists after a change falls
back to the last page that does, never to an empty page. Only campaigns public in
the requested market count.

**32. Campaign detail.** A campaign shows its title, a fact block with its clients,
category, month and year and any external site, its hero film or still, an outline
collapsed behind a read-more control that expands in place, its awards grouped by
body and year with each row carrying the category path and the rank, its credit
list, a share set with a copy-link control that confirms, and four related
campaigns. A campaign has a list of clients with one marked primary: the index
card shows the primary and the detail shows all. `Night Signal` lists
`Kagerou Beverages` as primary with `Aozora Airlines` and `Minato Rail`.

**33. The newsroom.** Articles are listed newest first, nine per page. Two facets
compose freely in the address: category, one of `news`, `awards` and `stories`,
matched as a contains test because an article may carry several; and year. An
empty intersection shows the filtered empty state rather than a blank page. An
article shows its title, standfirst, date, category chips and a structured body with
headings, lists, quotations and links. An award article also shows a per-campaign
breakdown of body, category path and rank, read from the same results as the
campaign pages: `Lotus Festival 2025 results` is tagged both `awards` and `news`.

**34. Company and careers records.** The company record carries its own
last-updated date and lists the legal name, the address with postal code and
building, the telephone, the founding date, the officers with full titles and the
auditor. An officer is a person, a title at this company and, optionally, a
concurrent position elsewhere, which is shown in parentheses after the title and
never as a second title here: `Hiroshi Kudo`, `Non-executive Director`, holds a
concurrent position at `Meido Group`. Ten organisational units are listed, two of
them dedicated to a single client. A careers opening is a record with a track,
`new_graduate` or `internship`, a title and an external apply address; its link is
marked as leaving the site and opens in a new context, and when the openings cannot
be loaded the page offers the contact route with
`We cannot reach the recruiting service right now. Here is how to contact us directly.`

**35. The contact form.** The form carries an enquiry type, a name, a company, an
email, an optional telephone, a message, and a consent box for the privacy policy
that starts unticked and must be ticked deliberately. The four types are
`new_business`, `recruitment`, `press` and `general`. Validation runs on the server
and is repeated in the browser. Errors sit next to their field, are announced to
assistive technology, and focus moves to the first one. The submit control is disabled while a submission is in flight, but a
disabled button fails on a refresh, so each rendering of the form
fetches a fresh idempotency key, and a key submitted twice, by a double click, a
refresh or a retry, stores exactly one enquiry. A submission arriving less than one
second after its key was issued is refused. A hidden decoy field named `website`
that a person never fills refuses the submission when filled. Repeated submissions
from one address or network slow down gradually rather than hitting a hard wall,
and the form can never be used to send mail to an arbitrary address. A submission
without consent is refused and stores nothing. Each type routes to a desk through a
routing table held as data: `new_business` to `newbusiness@kuromeido.example.com`,
`recruitment` to `careers@kuromeido.example.com`, `press` to
`press@kuromeido.example.com`, and `general`, which has no recipient, falls back to
the default desk `desk@kuromeido.example.com` with a routing warning recorded,
never silently dropped. Routing is recorded on the enquiry; no mail is sent. The
confirmation reads `Thank you. We will reply within two working days.` in English
and says the same in Japanese, and every error message exists in both languages.
Uploads, where the form accepts one, are checked by their content rather than their
extension, capped in size, kept out of anything served directly and handed out only
through an authorising handler.

**36. The terms and privacy pages.** A terms page and a privacy page, each with
numbered clauses, a last-updated date and a table of contents that deep-links to
every clause, exist in both languages. Every public page links to both from its
footer, which is the page's footer landmark, and the contact form links to the terms page
beside its consent box. Where
the English text of a clause set lags the Japanese, the per-field fallback of rule
27 applies.

**37. The not-found screen.** Any address that does not resolve, including
addresses shaped like an old publishing platform's endpoints such as `/wp-json/`, returns a real not-found
status with the designed screen: the three-dimensional numeral treatment, the
apology line `Sorry, nothing lives at that address.`, and links back to the home
page and to the work index. The requested path is never echoed into the page.

**38. The page-view log.** Every public page view records one row carrying the route
and the time, and nothing personal. Only an `editor` reads the log, at
`/studio/page-views`, newest first.

**39. Sitemap and robots.** `/sitemap.xml` lists every public route in both
languages, including every published campaign and article that is public now, and
never an embargoed, unpublished or untranslated one. `/robots.txt` points at the
sitemap by its full address and keeps `/studio` and `/preview/` out of indexing.

**40. Images carry alternative text.** Every content image on the public site,
every campaign still, hero poster, officer portrait and generated client wordmark,
carries alternative text in the page's language naming what it shows. Decorative
images, the liquid gradient, the diagonal lattice, the hatched block and the seal
where it repeats as ornament, declare themselves decorative so assistive
technology skips them.

**41. Audit.** Every privileged action is written to an append-only audit log with
the actor, the subject, the time, the before and after, and a reason where the
action requires one: placing or lifting a legal hold, a clearance grant or
revocation, and a credit list change after publication. Reading the audit
trail of a job is itself a read of that job and obeys the wall. No endpoint edits or
deletes an audit event; such a request is refused and the event remains.

## User flow

The information architecture has two halves: the public routes in two languages, and the
platform surfaces behind sign-in under `/studio`.

| Route | Who reaches it | What is there |
|---|---|---|
| `/` and `/en/` | anyone | the home composition |
| `/methodology/` | anyone | the `Rupture` methodology and its three-step diagram |
| `/work/` | anyone | the campaign index with its odometer count, year facet and pages |
| `/work/<slug>/` | anyone, public campaigns only | one campaign |
| `/news/` | anyone | the newsroom with category and year facets |
| `/news/<slug>/` | anyone, public articles only | one article |
| `/company/` | anyone | the company record |
| `/careers/` | anyone | culture, values, activities and openings |
| `/sustainability/` | anyone | the sustainability position |
| `/contact/` | anyone | the routed enquiry form |
| `/privacy/` and `/terms/` | anyone | the legal set |
| `/sitemap.xml` and `/robots.txt` | anyone | the index files |
| `/preview/<token>` | anyone holding a live preview link | one unpublished or embargoed campaign, never indexed |
| `/login` | anyone | platform sign-in |
| `/studio` | every platform role | the desk overview, including `Nothing is waiting for your approval.` when empty |
| `/studio/accounts` | every platform role | clients and the accounts the viewer is cleared for |
| `/studio/briefs` | every platform role | briefs as a table |
| `/studio/briefs/<id>` | every platform role | one brief with its estimates, approval and conversion |
| `/studio/briefs/new/1`, `/studio/briefs/new/2`, `/studio/briefs/new/3` | `account_director` | the three-step new-brief wizard |
| `/studio/jobs` and `/studio/jobs/<id>` | every platform role | jobs as a table, one job in detail |
| `/studio/jobs/<id>/crew` | every platform role | the crew board |
| `/studio/jobs/<id>/files` | every platform role | versions, the two review tracks, comments |
| `/studio/jobs/<id>/costs` | every platform role | time, third-party cost and burn |
| `/studio/clearance` | every platform role | rights per job and market, and legal holds |
| `/studio/people` | every platform role | the people directory |
| `/studio/rate-cards` | every platform role | rate card versions |
| `/studio/awards` | every platform role | bodies, entries and results |
| `/studio/publishing` and `/studio/publishing/<id>` | every platform role | campaigns and articles with the publication gate |
| `/studio/reports` | every platform role | burn and the jobs export |
| `/studio/page-views` | `editor` | the page-view log |

Every public route except `/preview/<token>` also exists under the `/en/` prefix with the same trailing
slash, for example `/en/work/` and `/en/work/night-signal/`.

**Studio shape.** A persistent top navigation bar runs across every studio route:
`Desk`, `Accounts`, `Briefs`, `Jobs`, `Clearance`, `People`, `Rate cards`, `Awards`,
`Publishing`, `Reports`. Every studio list is a table with sortable column headers
and one row per record. Opening a new brief is a three-step wizard, each step its
own address: step one captures the title and picks the accounts and markets, step two captures the
problem, the convention to break, the deliverables and the deadline, step three
captures the indicative budget and confirms. Going back keeps what was typed. Every
successful write confirms with a toast at the foot of the screen, and every refusal
shows a toast carrying the reason and an inline message beside the field involved.

**Entry and redirects.** A signed-out visitor opening any `/studio` address is sent
to `/login` and returned to that address after signing in; signing in without a
destination lands on `/studio`. Signing out returns to `/login`. When a session
expires mid-action, the action is refused, a toast says the session ended, the
unsaved input stays on screen, and signing in again returns to the same address. A
role that cannot write on a studio page sees it without the controls it cannot use,
and the server refuses the write regardless. A walled job's address shows the same
not-found screen as a missing one.

**The visitor.** Opens `/`, watches the hero statement settle, scrolls to the work
carousel and drags it. Opens `WORK`, sees the odometer land on the total, chooses
`2025`, and the address gains the year. Opens `Night Signal`, expands the outline,
reads the `Lotus Festival` awards and the credits, copies the link and sees it
confirmed. Switches to English and stays on `Night Signal`. Filters the newsroom to
`awards` in `2025`. Opens `CONTACT`, leaves consent unticked, sees the error beside
the box, ticks it, sends, and reads the confirmation.

**The account director.** Signs in as `account_director@example.com`, opens
`/studio/briefs/new/1`, walks the three steps for `kagerou-beverages`, and sees a
toast. After the producer writes an estimate, opens the brief at
`/studio/briefs/<id>`, approves the estimate and converts the brief,
naming Kenji Mori as producer.

**The producer.** Signs in as `producer@example.com`, opens `Kagerou Summer Tea`,
staffs a person, asks for more weekly minutes than that person has left and receives
the capacity refusal, records time and a third-party cost on the job, and reads its
burn.

**The creative and legal.** On `Kagerou Summer Tea`, `creative@example.com` uploads a
version, marks it
internally approved and leaves an internal comment and a client comment.
`legal@example.com` records rights per market and places and lifts a hold with a
reason.

**The editor.** Signs in as `editor@example.com`, opens `/studio/publishing`, opens
`Paper Lanterns`, sees all four gate conditions met, publishes it to `JP` and `US`,
sees the toast, and finds it on `/work/` and `/en/work/`.

**The walled creative.** Signs in as `creative2@example.com`, finds no
`Hoshino EV Launch` in the jobs table, gets no suggestion for it while typing
`Hoshino` in the search box, and gets the not-found screen at its address.

**States.** Every list, panel and detail view on both halves declares four states.
Empty says what would be here, why it is not, and the one action that changes it,
and distinguishes never-had-any from filtered-to-nothing: the work index filtered
to a year with nothing shows `No campaigns in that year yet. Clear the filter to see everything.`
with a control that clears the filter, and never implies the agency has no work;
the newsroom shows `No articles match those filters.`; the studio desk shows
`Nothing is waiting for your approval.` Loading shows skeletons in the final
layout's shape so nothing jumps. Error says what failed, whether a retry makes
sense, and offers it, never a bare code; a failed studio save says
`That did not save. Your work is still here, so try again.` Offline, public pages
already fetched stay readable, and the studio says the last action did not save
and keeps it rather than discarding it. Errors never crash the app.

## UI/UX notes

The north star for the public site: in the first moment a visitor should feel that
this agency makes things move, and read it in enormous type. The north star for the
studio is comprehension. The public site is an editorial register with atmosphere,
where the work is seen first; the studio is an operational register, quiet and
dense, built for scanning and repeated action, with no oversized heroes.

**Motion.** Motion is the public site's primary material, and it is eased: considered
entrances and exits, never a bounce. Stillness is the default: every effect is
additive and runs only when the visitor has not asked for reduced motion. Six named
curves exist as a closed vocabulary: a decelerating entrance, an accelerating exit, a
long, hard settle for the big type, an interface transition, the marquee's own
easing where it is not steady, and a sweeping curve for the full-screen overlay. The
named moments are: the marquee bands; display words rising and fading in on the long
settle, staggered; the overlay wiping in and back out in reverse; the work carousel
advancing with a numbered index under drag and keyboard; campaign stills scaling
slowly under their scrim on hover; the liquid gradient flowing; the not-found
numerals turning in three dimensions; and the new-work chip sliding in past a scroll
threshold. The studio's motion is limited to the toast arriving and leaving.

**Accessibility.** The target is WCAG AA. Body text and its background meet the AA
contrast ratio of at least `4.5:1` on every route; the grey ladder is checked against the measured
grounds rather than assumed, and its darker steps are used only for large display
type or on the light bands. The acid yellow on the near-black ground passes comfortably;
near-black type on the acid yellow is checked before it is used at small sizes. Focus is
visible on every interactive element against the black ground, which the browser
default is not, and focus order follows reading order despite the layered motion.
Keyboard navigation reaches everything. Touch targets are at least `44` by `44` pixels.
Icon-only controls carry labels, and meaning is never carried by colour alone.

**Mode.** The whole product is dark only: the public site and the studio both sit on the
near-black ground, and there is no light theme and no theme switch.

**Palette, public site.** The look is a deliberately tiny palette. The ground of
almost every band is a near-black neutral. Type, rules and marks on that ground are a
near-white neutral. There is exactly one accent, an acid yellow that leans toward green and never toward
orange (by the colour vocabulary, a mid, vivid amber); it marks the fine diagonal
rules behind the hero, active states and highlights, and nothing else on a page
wears it. Raised surfaces and card grounds
are three further near-black neutrals, each a step lighter than the ground.
Secondary and disabled type uses a grey ladder of one deep neutral and three mid
neutrals; tertiary type and hairlines use light neutrals and near-white neutrals;
the inverted bands use four near-white neutrals. The colour that means something
went wrong is a mid, vivid red, used sparingly for errors and nowhere else, with a
near-white warm neutral as its tint. White at seventy and at fifty percent strength
are the two secondary type strengths on the ground, and black at half strength is
the scrim over imagery. Colours belonging to an embedded video player or to a
partner's logo are never brand colours and never enter the system. The exact values
are yours, so long as they hold these roles.

**Palette, studio.** The same near-black ground and near-white type, the acid yellow
reserved for the one primary action on each screen, which brightens slightly under the
pointer and on focus, and the red for refusals. Status words carry meaning-carrying
colours of their own: a mid, vivid green for `approved`, `cleared` and `published`,
and a mid, vivid orange for `pending`, `changes_requested` and `scheduled`; status is
carried by words as well as colour, never by colour alone. Destructive studio actions,
such as unpublishing, revoking a clearance, ending an assignment or withdrawing a
version, ask for confirmation before they run, and Escape cancels the confirmation.

**Type.** Two registers, as a bilingual site requires, and Japanese and Latin never
share a display line: a bilingual statement is two lines, each in its own register.
`Noto Sans JP`, loaded as a variable face and known in the style layer as
`notosansjp`, sets all Japanese copy and the Japanese interface. `Archivo`, at its
widest width, is the wide-tracked Latin grotesk for the Latin display and marquee
register, set in capitals with generous letterspacing. `Noto Color Emoji` is a
fallback face only. The signature typographic device is letterspacing pushed until
it becomes rhythm: marquee lines are set character by character with wide gaps, so a
phrase reads as a texture from across the room and as words up close. The scale runs
from the full-bleed display for the marquee and hero words down through section
heads, card titles, body and a micro-label band for coordinates, dates and category
chips; the micro register is where the site keeps its factual furniture. Studio
figures use tabular numerals wherever amounts stack.

The type steps are reconstructions faithful in ratio. On a desktop window they are:
the full-bleed display at `160px`, section heads at `56px`, card titles at `24px`,
body at `16px` and the micro label at `11px`, all in the family of the line's own
script. The display scales down with the window so it stays full-bleed at every
width, and the other steps hold. The studio sets body at `14px` and table figures at
`13px`.

**Shape and depth.** No rounded corners, no soft shadows, no centred column: content
runs in bands from edge to edge, and depth comes from planes of moving type layered
over one another, which is the whole look. Content runs in edge-to-edge bands, and
the floating menu pill with its clipped corner is the one rounded shape.

**Responsive.** The layout holds from a phone to a very wide display with no
sideways scrolling at any width. There is one dominant breakpoint between tablet and
desktop, two further steps for very wide displays, a tablet step and two narrow
guards. Hover effects fire only for a fine pointer that can hover; touch devices get
the touch fallbacks. On a phone the floating menu moves out of the way of the
on-screen keyboard and never covers a form field or a video control. Studio tables
scroll inside their own frame on a narrow viewport rather than pushing the page
sideways.

## Front-end specification

### Ground and grid

The public site is designed at three captured widths: a desktop window, a
tablet-landscape window and a phone. The breakpoint ladder is deliberately sparse:
one dominant step between tablet and desktop carrying most of the rules with its
mirrored form for the small side, two steps for very wide displays, one for the
tablet case and two narrow guards. Pointer capability is checked as hover together
with a fine pointer, and a no-hover query carries the touch fallbacks. Motion is
gated positively: most rules sit behind a no-preference query and a handful behind an
explicit reduce query. Content runs full-bleed in bands, and the composition comes
from the motion rather than from a grid.

### Layering

The layering order is discrete and honoured rather than improvised, because the
marquee bands, the floating control and the full-screen overlay compete for the same
space. From the bottom: the marquee underlay that sits behind content; the in-flow
stacking steps; raised cards; the sticky new-work chip and the floating control; the
overlay surface; the consent banner; and the lightbox and anything modal on top. The
overlay sits above the floating control that opens it, and the consent banner is
never trapped beneath either.

### Surfaces and marks

- Fine diagonal rules in the accent behind the hero, drawn as vector lines.
- The seal: a stamped rounded-triangle mark carrying the city in a small circle at the
  apex set on a curve, the lockup across the centre, a founding line beneath and two
  small glyph boxes at the base, drawn geometry reproduced at three sizes, the
  smallest dropping the founding line. It is the site's only ornament.
- The hatched block, repeating diagonal stripes, used as a spacer and an emphasis rule.
- The scrim over campaign imagery so white type stays legible.
- The floating menu control: a black pill with a clipped corner fixed at the foot of
  the viewport on every page.
- The lockup is the two parent names joined by a backslash, `KURO\MEIDO`, set as live
  text in the Latin grotesk with wide tracking; the backslash is the brand's signature
  character and also appears alone, at display size, as a graphic.
- The pirate flag: the agency calls itself a pirate ship rather than a navy, and a
  simple drawn flag mark in the stroke set, inheriting text colour, carries that
  register. It is drawn, never an emoji, so it renders identically everywhere.
- Interface glyphs are a thin stroke set on a twenty-four unit box inheriting text
  colour: arrow, chevron, close, menu bars, external link, play and the social marks.
- Category chips, `creative` and `innovation`, and award-body names are text, never
  icons, so they can be searched and translated.

### Split text

Display headings, page titles, client names and whole paragraphs are set character by
character, each character its own element, so reveals stagger per character and
Japanese can run vertically; page titles split into single Latin letters and body
paragraphs into single kana and kanji. The parent keeps the unsplit string as its
accessible name and the character elements are hidden from assistive technology, so a
screen reader announces one sentence rather than eighty fragments, and the text stays
selectable, findable with the browser's find and translatable. Under reduced motion
the text is plain and unsplit. Japanese splits per character because it has no
spaces between words, so a split on whitespace would leave the Japanese half unsplit
while the English half animates.

### Global chrome

**The floating menu.** There is no conventional header. The black pill at the foot is
labelled `MENU` with a small glyph. Choosing it opens a full-screen overlay listing the
eight primary destinations in the display register, `WORK`, `NEWS`, `METHODOLOGY`,
`COMPANY`, `CAREERS`, `SUSTAINABILITY`, `CONTACT` and `HOME`, with the language pair and
the social links. The overlay traps focus, returns focus to the pill on close, makes
the page behind inert rather than merely covered, closes on escape and on choosing a
destination, and its own close control is labelled `Close menu`.

**Language.** The pair is shown as two codes, `JA` and `EN`, with the current one marked
as current rather than as a link, and switching follows rule 28.

**Footer.** The footer is itself a marquee band carrying the office line, the
coordinates, the founding year and the pirate line, over three link columns: content,
utility (including the terms page and the privacy page) and social. Below them sit the
language pair, a back-to-top control and the copyright line `(c) KURO\MEIDO Inc.`. A
sticky new-work chip sits above the footer promoting the latest campaign.

**Shared furniture.** Category chips; date lines in the micro register; the seal at
several sizes; the hatched spacer; a lightbox for campaign stills; the consent banner
with its categories, `Necessary`, `Analytics` and `Marketing`; and the new-work chip.

### The marquee system

Several bands of letterspaced type scroll sideways at different speeds and in opposite
directions, layered over one another on the black ground. Each band is a continuous
loop with no visible seam at any window width: its content is duplicated and moved by
exactly one track width, and the join is invisible everywhere. Speed is set as distance
per second, not as a loop duration, so a wider window does not change the reading pace. Scrolling
accelerates the bands, scrolling up reverses them, and they settle back to their own
speed afterwards, which is what makes the page feel physical. Bands pause off-screen and
while the tab is hidden, and under reduced motion they stop entirely and render as
static letterspaced lines. The marquee holds a steady sixty frames a second on a
mid-range phone and never makes the page jump.

Under reduced motion, which is the default here: marquees are still, reveals are plain,
the carousel changes instantly, the gradient is a single still frame, the not-found
numerals are still, and no film plays by itself.

### Home

A long scroll composition, not a short landing page, in this order.

1. **Hero.** The lockup, then the methodology line in two registers: the lowercase
   premise `rupture is not destruction.` answered by the full-bleed capitalised
   `RUPTURE IS CREATION.` Fine diagonal accent rules sit behind, and three micro-register
   facts anchor the corner: the founding year `EST. 2006`, the city `TOKYO` and the
   coordinates `35.6581 N 139.7561 E`.
2. **Positioning.** Three to four lines in the body register:
   `We use creativity to move business and to reshape society and culture. We set the pace of change through innovation and world-class creative work, challenging conventions and helping brands shape what comes next.`
3. **Statement band.** The capitalised triplet `CREATE. INVENT. HAVE IDEAS.` and the
   methodology word at display size.
4. **Work carousel.** Recent public campaigns as cards carrying client, title, a one-line
   description and category chips; draggable, with a numbered index and keyboard
   control.
5. **Who we are.** Two columns pairing the positioning with the methodology's history:
   in continuous use since `1992` as the network's DNA, meaning creative destruction,
   not damage.
6. **Partners.** The client wordmark wall.
7. **News.** The latest articles with date, category chip and title.
8. **Closing marquee.** The office identity band as a continuous loop: `TOKYO JAPAN`, the
   lockup in both scripts, `KURO\MEIDO` and `クロメイド`, the coordinates, the district
   `KAIGAN, CHUOKU`, the street number `1-2-3`, `EST. 2006` and the whitespace line
   `We are the method company. We help brands find strategic and creative whitespace.`
   It ends on `READY TO BREAK SOMETHING`.

A banner strip pinned above the composition carries the current headline announcement
and links to the article behind it.

### Methodology

A philosophy statement, then the three-step framework as its own diagram. The name is
`Rupture` with the registered-trademark sign rendered as a real superscript character in
both languages, never as letters in parentheses.

| Step | Content |
|---|---|
| Convention | the received assumption to break, which everyone accepts without noticing |
| Vision | the ideal state on the other side of breaking it |
| Method | the idea that breaks the convention and realises the vision |

The three terms appear both as a running statement and as a labelled diagram drawn as
geometry, and each node of the diagram is reachable by keyboard with its description as
accessible text.

### Work index and campaign detail

The index heading is a digit-roll odometer: columns of numerals spin to land on the real
total from the server, and one, two and three digit totals land without the layout
moving. Cards reveal on scroll; their stills scale slowly under the scrim on hover, for
fine pointers only. The detail page opens with a back-to-index control and the title
split per character at display size, then follows rule 32.

Two facts a naive build gets wrong: a campaign may hold several awards from one body in
one year in different categories, and a campaign has several clients with one primary.

### Company

In order: the office identity band with the coordinates and the district, the
positioning lines, the methodology statement, a long company narrative set per
character, and then the formal record. The record carries these rows and its own
last-updated date, `2026-04-01`:

| Row | Content |
|---|---|
| legal name | `KURO\MEIDO Inc.` |
| address | postal code `104-0061`, then `Kaigan Tower 14F, 1-2-3 Kaigan, Chuo-ku, Tokyo` including the building |
| telephone | the main line, `+81-3-5555-0100` |
| founded | the founding date, `1 April 2006` |
| representatives | the named officers with full titles |
| auditor | one named officer |

Officers, in order: `Kaito Mizuno`, `President & CEO`; `Emi Hayashi`,
`Chief Operating Officer`; `Ren Shibata`, `Chief Creative Officer`; `Hiroshi Kudo`,
`Non-executive Director`, concurrently `Executive Officer, Meido Group`;
`Laura Chen`, `Non-executive Director`, concurrently
`Regional President, KURO Worldwide`; and the auditor `Masato Ide`, `Auditor`,
concurrently `Audit Partner, Meido Group`. The two parent groups are the domestic
`Meido Group` and the global network `KURO Worldwide`.

Ten organisational units: `Planning`, `Media Experience Design`, `Corporate Strategy`,
`Finance`, `Executive Management`, `Hoshino Unit` (dedicated to `hoshino-motors`),
`Kagerou Studio` (dedicated to `kagerou-beverages`), `Rupture Lab`,
`Integrated Business Leadership`, and `Minato Media Partners`, the jointly owned media
agency. A directory that treats units as flat departments cannot say that two of them
sit inside a client's wall by construction.

### Careers

The longest page, in order: a positions control jumping to the openings; the recruitment
film behind a poster frame with a play control, opening a dialog that explains the film is
a local placeholder, with captions; the culture statement, the pirate line set
bilingually at display size, `WHY JOIN THE NAVY WHEN YOU CAN BE A PIRATE` and
`海軍に入るな、海賊になれ。`, each in its own register; the five values as cards, each an
English display phrase, a Japanese rendering and a paragraph:

| English | Japanese |
|---|---|
| `BE A PIRATE` | `海賊であれ` |
| `CREATIVITY COMES FROM DIVERSITY` | `多様性が創造性を生む` |
| `UNCOMMON HUMANITY` | `並外れた人間らしさ` |
| `GOOD ENOUGH IS NOT ENOUGH` | `十分では足りない` |
| `BE BRAVE` | `勇敢であれ` |

The third value's paragraph is about being the person who serves their colleagues. Then
the activities, the internal and social-contribution programmes; then the openings. The
two seeded openings are `Creative, new graduates 2027` on the `new_graduate` track with
the apply address `https://careers.example.org/kuromeido/new-graduates`, and
`Summer internship 2027` on the `internship` track with
`https://careers.example.org/kuromeido/internships`.

### Sustainability, contact and the legal set

Sustainability states the agency's position on using its work for social change, with its
programmes and commitments. Contact is the routed form of rule 35, the shortest real page.
Privacy and terms are long structured prose per rule 36. Not-found follows rule 37 and is
a designed page, never a framework default.

### Copy deck

Every string below is exact. The voice is declarative, short, unafraid and bilingual, with
a streak of self-mocking bravado.

| Where | Text |
|---|---|
| hero premise | `rupture is not destruction.` |
| hero answer | `RUPTURE IS CREATION.` |
| statement triplet | `CREATE. INVENT. HAVE IDEAS.` |
| closing marquee | `READY TO BREAK SOMETHING` |
| culture | `WHY JOIN THE NAVY WHEN YOU CAN BE A PIRATE` |
| empty work index | `No campaigns in that year yet. Clear the filter to see everything.` |
| empty newsroom | `No articles match those filters.` |
| empty studio desk | `Nothing is waiting for your approval.` |
| failed save | `That did not save. Your work is still here, so try again.` |
| recruiting service unreachable | `We cannot reach the recruiting service right now. Here is how to contact us directly.` |
| capacity refusal | `That person is fully committed in the weeks you selected.` |
| publication gate | `The campaign cannot be published yet: clearance for one market expires before the scheduled date.` |
| fallback notice | `The page is not yet available in English; showing the Japanese original.` |
| language switch without translation | `That campaign is not yet available in English, so here is all of our work.` |
| enquiry confirmation | `Thank you. We will reply within two working days.` |
| not-found apology | `Sorry, nothing lives at that address.` |
| consent line | `I have read the privacy policy, which I accept.` |

The consent banner names its three categories, and the privacy and terms pages carry the
prose of rule 36.

### Generating every asset

No binary from any other site ships, and the build contains zero copied assets.

| Asset | How it is made |
|---|---|
| diagonal accent lattice | a tiling vector pattern in the accent: a repeating parallel slash at a one-to-two slope on a steady pitch, paired vertical rules at the edges and at each slash cluster, horizontal rails closing the band, drawn at three band heights, stroke only, no fill |
| the seal | vector geometry as described above, at three sizes |
| the lockup | live text in the Latin grotesk, never an image, so it translates and scales |
| the pirate flag | a drawn vector flag in the stroke set, inheriting text colour |
| client wordmark wall | invented wordmarks for each client in the Latin grotesk at one optical size, white on black at reduced strength, brightening on hover; no real company's mark is ever reproduced |
| campaign stills and heroes | abstract compositions of flat palette fields with the lattice overlaid, or a still frame of the gradient, one per campaign, in a modern image format with a fallback |
| the liquid gradient film | a flowing orange and yellow field rebuilt procedurally as an animated multi-stop gradient, seeded, looping without a seam, paused off-screen, a single still frame under reduced motion |
| the not-found animation | drawn vector numerals with a perspective turn and a short entrance on the long settle, still under reduced motion |
| the recruitment film | a locally generated placeholder clip or poster frame with a play control that opens a dialog explaining the substitution, with authored captions |
| fonts | the openly licensed faces named in `## UI/UX notes`, subset by character range |
| favicon and social images | generated from the seal and the lockup at the required sizes |

## Technical requirements

The app is a single-page application: the browser receives a small HTML shell and a
script bundle, and every route renders on the client. The front end is `SolidJS`,
built with `Vite` into static assets. The backend and the HTTP API are `Express`, which
serves the built assets and the JSON API under `/api` on the same origin. Because the
server knows the public route table and the public set, it answers an unknown address,
an unpublished campaign's address, the address of a campaign with no published
translation in either language and an embargoed
campaign's address with a real `404` status carrying the shell that renders the
not-found screen, and it serves `/sitemap.xml` and `/robots.txt` itself.

Records go into `PostgreSQL`, found at `DATABASE_URL`. Every work version, hero film,
still and uploaded file goes into `minio`, the S3-compatible object store at
`STORAGE_ENDPOINT`: the bucket name comes from `STORAGE_BUCKET`, and the key pair from
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The bucket stays private; bytes reach a
browser only through the app's own authorising handlers, and a signed link the app
issues never outlives the clearance or the preview link that granted it. Staff sign in
with an email and a password the app itself checks; passwords are stored hashed, a
successful login returns a bearer token as `access_token`, tokens expire `8` hours after issue, and the role
is always read from the stored account, never from a request. Sessions rotate when a
privilege changes. Once the app can reach both backing services, `GET /api/health`
answers `200`. Each request writes one structured line to stdout that carries no
personal data and no identifier of walled material.

Use only the libraries named here plus their direct dependencies. Do not introduce a
second database, cache, queue, object store, identity provider or mail vendor: the only
backing services available in this environment are `PostgreSQL` and `minio`, and
reaching for anything else is a contract violation. Hosts, ports, keys and passwords
all come from environment variables and none is written into the code. Both services
are up before the app starts, so they are never fetched, installed, built or launched
by it.

**The authority principle: one authority behind many doors.** This is the architecture's
one governing rule. Each fact has exactly one computation that every
surface calls: one clearance predicate for every read path including search, export,
aggregates and audit; one medal tally for every published total; one cost computation
for every financial surface; one availability computation for staffing, refusals and
utilisation; and one fallback resolver for every bilingual surface. Changing one
underlying record moves every surface that shows it on the next read, including
reports, exports and totals.

**Aggregates obey the wall.** A burn total, a utilisation figure or any count is computed
over the viewer's readable set only. Where that makes a figure partial, the response
says so with `partial` set to true rather than quietly under-reporting.

**Time-based transitions run unattended.** Embargo release and rights expiry happen at
their moment on the server's clock, visible on the next read at the latest, with nobody
present and no external scheduler. A failed transition is written to the log as an
error, since its only other symptom is wrong content on the public internet.

**Conflicting saves.** Records several people edit carry a revision. Two writes from the
same revision: exactly one is accepted, the other is refused as a conflict and changes
nothing. Every mutating endpoint is safe to retry.

**Identifiers** are opaque and non-sequential, because sequential identifiers leak the
count and the rate of new client work.

**Security headers.** Every response carries a content-type options header refusing to
sniff, a frame-ancestors restriction that denies framing, a referrer policy, and a
content security policy permitting this origin and nothing wider. Every mutating form is
protected against cross-site request forgery. Preview link responses carry
`X-Robots-Tag: noindex`.

**Uploads** are checked by content rather than by extension, capped at `200` megabytes,
never executed, and served only through an authorising handler.

**Nothing the browser downloads carries a secret.** No object-store key, database
password, other user's token or API key appears in any script, stylesheet, document or
source map.

**Performance.** The largest content paints within two and a half seconds on a mid-range
phone on a throttled connection; interactions respond within two hundred milliseconds;
cumulative layout shift stays under one tenth, which the odometer and the split text both
threaten; marquee and scroll animation hold sixty frames a second on mid-range hardware;
the hero renders without waiting for films or below-fold images. Images declare their
dimensions, below-fold media is deferred, and the Japanese face is split by character
range so a Latin-only page never downloads the full kanji set.

**Reconstructed values.** The exact type steps and tracking are reconstructions
faithful in ratio, the marquee speeds and their scroll coupling are tuning values, the
platform itself is designed rather than captured from a real system, other award
bodies' rank sets are seeded, and the lifetime award history beyond the seeded years is
not carried.

**Volume.** The product stays responsive with the seeded content, a few thousand time
entries and a few thousand page views.

**Operations.** Backups are proved by restoring one, not merely taken. Schema changes run
forward-only with a documented way back, online, and a change that would rewrite
historical cost or credit records is refused; history is append-only. Every stored record
carries a schema version.

**Retention.** Enquiries are kept for `24` months, time entries for `7` years,
work versions for `5` years after their job closes, and audit events for `10`
years; on expiry a record is deleted or anonymised on schedule, except under legal
hold, which suspends the schedule entirely. A client's deletion request, handled by
the agency's operators outside this product's screens, removes their personal data
but never the agency's financial records or credit history, and the refusal says why
rather than failing silently. A signed link the app issues never outlives the
clearance or the preview link that granted it.

**No external calls at run time.** The running app calls nothing outside this
environment; the page-view log is the app's own, and the careers apply links are plain
outbound links.

## Data model

Forty-two tables. All timestamps are UTC; embargo moments are stored with their offset.
Money is whole yen in integers, currency `jpy`, and third-party amounts are integers in
their own currency's minor units.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

Table names below are exact. Column names are exact where given.

- **users**: id, `email` (unique, compared without regard to case), password hash, `role`
  (one of `account_director`, `producer`, `creative`, `legal`, `editor`), person id.
- **people**: id, English name, Japanese name, reading, unit, weekly capacity in minutes,
  status (`active` or `departed`), departure date, skills.
- **units**: id, slug, English and Japanese names, the dedicated account where there is one.
- **clients**: id, `slug`, English name, Japanese name, reading.
- **client_competitors**: a symmetric pair of competing clients.
- **client_accounts**: id, slug, client, owning person.
- **person_clearances**: id, person, account, start, end, revocation date, cooling-off end,
  source (`grant` or `unit`).
- **briefs**, **brief_accounts**, **estimates**: the brief, its accounts, and numbered
  estimate versions with an amount and a status (`draft`, `approved`); a brief's status is
`open` or `converted`.
- **jobs**: id, brief, title, producer, pinned rate card version, legal hold flag, status
  (`open` or `closed`).
- **job_accounts**: job, account, share in basis points.
- **rate_cards** and **rate_card_rates**: version, effective from, effective to; role and
  hourly rate.
- **assignments**: id, job, person, role, start, end, minutes per week. Never deleted.
- **time_entries**: id, job, person, role, work date, minutes, cost, the entry it adjusts.
- **periods**: month and closing time.
- **cost_entries**: id, job, supplier, amount in minor units, currency, converted amount in
  yen, exchange rate, rate date.
- **work_versions**: id, job, number, label, `object_key`, digest, content type, internal
  status, client status, the number it was restored from, withdrawal time.
- **comments**: id, version, author, body, visibility, timecode or region.
- **rights**: id, job, right, subject, licence reference, term start, term end,
  territories, permitted media, status (`pending` or `cleared`).
- **campaigns**: id, `slug`, job, year, month, categories, external address, hero media,
  state (`draft`, `scheduled`, `published`, `unpublished`), embargo moment, markets.
- **campaign_clients**: campaign, client, primary flag, position.
- **translations**: item kind, item, locale, field, value, status. Translation is per
  field, never per item.
- **credit_entries** and **credit_people**: the ordered entries of a campaign with both
  role languages, the pin flag and the list revision; the ordered people of each entry
  with the names pinned when the entry was pinned.
- **publication_permissions**: campaign, kind (`case_study`), reference, who granted it.
- **preview_links**: token, campaign, expiry, revocation.
- **media_assets**: id, object key, digest, content type, width, height, alternative text
  in both languages.
- **award_bodies**, **award_ranks**, **award_categories**: the body; its ranks with an
  order and the rank each counts toward; its section and category paths.
- **award_entries**: id, campaign, body, category, year, fee, client permission reference,
  status (`submitted`, `shortlisted`, `closed`); unique on campaign, body, category and year.
- **award_results**: id, entry, rank, confirmed flag, confirmation date.
- **articles** and **article_campaigns**: slug, date, categories, the award body and year an
  award article reports, state, embargo moment; the campaigns an article relates to.
- **enquiries**: id, `idempotency_key` (unique), type, name, company, email, telephone,
  message, consent, routed desk, routing warning.
- **enquiry_routes**: enquiry type and recipient, which may be empty.
- **page_views**: id, `route`, time of the view.
- **audit_events**: id, actor, `action`, subject kind, subject, before, after, reason, time.
- **officers**, **openings**: the company record's officers and the careers openings.

These relations are the ones most often modelled wrongly: a job belongs to many accounts
with an apportionment; a credit entry has many people and entries are ordered within a
campaign; an award entry's uniqueness includes its category; a rank belongs to a body and
may count toward another rank; an assignment is dated and never edited away; a translation
is per field.

**Invariants, as properties of the running system.**

- A person reads a job only while cleared for every one of its accounts, on every read
  path, and a walled job's identifier answers exactly as a missing one does.
- A clearance for a competitor of a client the person holds or held within `90` days is
  refused; a client-dedicated unit's members are cleared for its account.
- A job's shares sum to `10000`.
- A converted job's rate card version never changes, and its historical costs never move
  when a newer card is published.
- A refused write writes nothing: no row, no partial row, no object.
- Committed minutes per week never exceed a person's capacity in any week.
- An assignment is never deleted.
- A version's number and bytes never change once stored, and a legal hold refuses every
  deletion on its job.
- A credit list write from a stale revision changes nothing.
- Every credited person holds or held an assignment on the campaign's job.
- A departure never removes a credit.
- An award entry is unique on campaign, body, category and year, and only confirmed
  results are counted anywhere.
- An audit event is never edited or deleted.
- An enquiry key stores at most one enquiry.

**Seed data.** The eight accounts in `## User roles`, each linked to its person.

People in the directory, with their Japanese names and readings:

| English | Japanese | Reading | Unit |
|---|---|---|---|
| Rin Takeda | 武田 凛 | たけだ りん | Integrated Business Leadership |
| Sora Imai | 今井 空 | いまい そら | Integrated Business Leadership |
| Kenji Mori | 森 健二 | もり けんじ | Planning |
| Aya Fujita | 藤田 彩 | ふじた あや | Planning |
| Haru Ueno | 上野 晴 | うえの はる | Hoshino Unit |
| Mei Sato | 佐藤 芽衣 | さとう めい | Media Experience Design |
| Daichi Ono | 小野 大地 | おの だいち | Corporate Strategy |
| Yui Kondo | 近藤 結衣 | こんどう ゆい | Media Experience Design |
| Ren Shibata | 柴田 蓮 | しばた れん | Executive Management |
| Takumi Aoki | 青木 巧 | あおき たくみ | Rupture Lab |
| Shun Kaneda | 金田 瞬 | かねだ しゅん | Kagerou Studio |
| Kaito Arai | 新井 海斗 | あらい かいと | Kagerou Studio |
| Mio Hirano | 平野 澪 | ひらの みお | Kagerou Studio |
| Nana Ishii | 石井 奈々 | いしい なな | Planning |
| Leo Tanaka | 田中 怜央 | たなか れお | Rupture Lab |
| Asuka Noda | 野田 明日香 | のだ あすか | Media Experience Design |
| Kou Endo | 遠藤 航 | えんどう こう | Planning |
| Yuto Baba | 馬場 悠斗 | ばば ゆうと | Planning |
| Riko Nishi | 西 莉子 | にし りこ | Planning |
| Sho Ota | 太田 翔 | おおた しょう | Planning |
| Ami Goto | 後藤 亜美 | ごとう あみ | Integrated Business Leadership |
| Kei Yamada | 山田 圭 | やまだ けい | Media Experience Design |

Every active person has a weekly capacity of `2400` minutes. Every seeded clearance
runs from `2026-01-01` to `2099-12-31`, and the unit clearances of `Hoshino Unit` and
`Kagerou Studio` members are derived the same way. The thirteen active people credited
on `night-signal` also hold `kagerou-beverages` clearances; Kaito Arai also holds an `aozora-airlines` clearance.

Clients, with their competitor sets:

| Slug | English | Japanese | Reading | Competes with |
|---|---|---|---|---|
| `hoshino-motors` | Hoshino Motors | 星野自動車 | ほしのじどうしゃ | `tsubame-automotive` |
| `tsubame-automotive` | Tsubame Automotive | 燕オートモーティブ | つばめおーともーてぃぶ | `hoshino-motors` |
| `kagerou-beverages` | Kagerou Beverages | 陽炎飲料 | かげろういんりょう | none |
| `aozora-airlines` | Aozora Airlines | 青空航空 | あおぞらこうくう | none |
| `minato-rail` | Minato Rail | 湊鉄道 | みなとてつどう | none |

Each client has one account with the same slug, owned as listed in `## User roles`.

Rate cards, hourly rates in whole yen:

| Role | `RC-2025` | `RC-2026` |
|---|---|---|
| `Creative Director` | `16800` | `18000` |
| `Senior Creative Director` | `19200` | `21000` |
| `Art Director` | `10800` | `12000` |
| `Copywriter` | `10800` | `12000` |
| `Strategist` | `13200` | `15000` |
| `Producer` | `10800` | `12000` |
| `Technical Director` | `13200` | `15000` |

`RC-2025` runs from `2025-01-01` to `2025-12-31`; `RC-2026` runs from `2026-01-01` with no
end.

Open jobs, all pinned to `RC-2026` with an approved estimate: `Hoshino EV Launch` on
`hoshino-motors`, producer Kenji Mori, with the in-progress draft campaign
`Midnight Charge` (`midnight-charge`); `Tsubame Rally Series` on `tsubame-automotive`,
producer Aya Fujita; `Kagerou Summer Tea` on `kagerou-beverages`, producer Kenji Mori;
and the split job `Sky Tea Partnership`, producer Kenji Mori. Seeded assignments on the
open jobs all run from `2026-01-05` to `2026-12-27` at `1200` minutes per week: Haru
Ueno on `Hoshino EV Launch` as `Creative Director` and on `Kagerou Summer Tea` as
`Copywriter`, which fills Haru Ueno's week; Mei Sato on `Tsubame Rally Series` as
`Art Director`; and Kaito Arai on `Sky Tea Partnership` as `Creative Director`.

Every public campaign also has a closed job behind it on its primary client's account
alone, at `10000`, pinned to the card of its year, with a `cleared` `music` right
covering that campaign's markets to `2099-12-31` and case-study permission recorded;
`tide-clock` carries the two talent rights described below instead.

Thirty campaigns are public in markets `JP` and `US`:

| Year | Slug | English title | Japanese title | Primary client | Category |
|---|---|---|---|---|---|
| 2026 | `blue-hour-rail` | Blue Hour Rail | 青い時間の鉄道 | Minato Rail | creative |
| 2026 | `tea-for-two-cities` | Tea for Two Cities | 二都市の茶 | Kagerou Beverages | creative |
| 2026 | `open-sky-lab` | Open Sky Lab | 開かれた空の研究所 | Aozora Airlines | innovation |
| 2026 | `mountain-switchback` | Mountain Switchback | 山のつづら折り | Tsubame Automotive | creative |
| 2025 | `night-signal` | Night Signal | 夜の信号 | Kagerou Beverages | innovation, creative |
| 2025 | `quiet-engine` | Quiet Engine | 静かなエンジン | Hoshino Motors | creative |
| 2025 | `rice-field-radio` | Rice Field Radio | 田んぼのラジオ | Kagerou Beverages | creative |
| 2025 | `salt-and-steel` | Salt and Steel | 塩と鋼 | Tsubame Automotive | creative |
| 2025 | `morning-gate` | Morning Gate | 朝の門 | Aozora Airlines | creative |
| 2025 | `tide-clock` | Tide Clock | 潮の時計 | Minato Rail | innovation |
| 2024 | `cloud-orchard` | Cloud Orchard | 雲の果樹園 | Kagerou Beverages | creative |
| 2024 | `steady-hands` | Steady Hands | 確かな手 | Hoshino Motors | creative |
| 2024 | `long-weekend-line` | Long Weekend Line | 長い週末の線路 | Minato Rail | creative |
| 2024 | `paper-wings` | Paper Wings | 紙の翼 | Aozora Airlines | innovation |
| 2024 | `dust-and-dawn` | Dust and Dawn | 砂塵と夜明け | Tsubame Automotive | creative |
| 2023 | `first-frost` | First Frost | 初霜 | Kagerou Beverages | creative |
| 2023 | `silver-bolt` | Silver Bolt | 銀の稲妻 | Hoshino Motors | innovation |
| 2023 | `window-seat` | Window Seat | 窓側の席 | Aozora Airlines | creative |
| 2023 | `iron-lullaby` | Iron Lullaby | 鉄の子守唄 | Minato Rail | creative |
| 2022 | `lantern-market` | Lantern Market | 提灯市場 | Kagerou Beverages | creative |
| 2022 | `torque-poems` | Torque Poems | トルクの詩 | Tsubame Automotive | creative |
| 2022 | `cabin-garden` | Cabin Garden | 機内の庭 | Aozora Airlines | innovation |
| 2022 | `coin-station` | Coin Station | 硬貨の駅 | Minato Rail | creative |
| 2021 | `green-signal` | Green Signal | 青信号 | Hoshino Motors | creative |
| 2021 | `glass-harbor` | Glass Harbor | 硝子の港 | Kagerou Beverages | creative |
| 2021 | `tail-wind` | Tail Wind | 追い風 | Aozora Airlines | creative |
| 2020 | `empty-platform` | Empty Platform | 空のホーム | Minato Rail | creative |
| 2020 | `slow-brew` | Slow Brew | ゆっくり淹れる | Kagerou Beverages | creative |
| 2019 | `first-drive` | First Drive | 初めての運転 | Hoshino Motors | creative |
| 2019 | `paper-map` | Paper Map | 紙の地図 | Tsubame Automotive | creative |

Every public campaign has published titles and descriptions in both languages, except
`quiet-engine`, whose English description is absent, and `rice-field-radio`, which has no
English translation. `tide-clock` is public in `JP` and `DE` instead, with a `talent` right
for `DE` whose term ended the day before first start and a `talent` right for `JP` running
to `2099-12-31`. `night-signal` lists `Kagerou Beverages` as primary, then
`Aozora Airlines` and `Minato Rail`. `night-signal`'s Japanese reading is `よるのしんごう`.

Four further campaigns, all year `2026`, each with published titles and descriptions
in both languages unless stated: `silent-aurora` (Silent Aurora, 静かなオーロラ, Kagerou
Beverages), scheduled for markets `JP` and `US` with the embargo
`2099-01-01T09:00:00+09:00` and a hero still in the bucket; `harbour-lights` (Harbour
Lights, 港の灯り, Minato Rail), scheduled for markets `JP` and `US` and released ninety
seconds after first start, on its own job on `minato-rail` pinned to `RC-2026`, with a
`cleared` `music` right for `JP` and `US` running to `2099-12-31`, case-study permission
`PERM-HARBOUR-LIGHTS`, and one credit entry, `Producer` Kenji Mori, who holds an
assignment on that job; `paper-lanterns` (Paper Lanterns, 紙の提灯, Kagerou Beverages),
a draft on its own job on `kagerou-beverages` pinned to `RC-2026`, with a `cleared`
`music` right for `JP` and `US` running to `2099-12-31`, case-study permission
`PERM-PAPER-LANTERNS`, and one credit entry, `Creative Director` Kaito Arai, who holds an
assignment on that job, so every gate condition is met; and `winter-kite` (Winter Kite,
冬の凧, Aozora Airlines), recorded for markets `JP` and `US` with translations drafted in
both languages and published in neither. At first start the work index lists thirty
campaigns in both languages; after the release of `harbour-lights` it lists
thirty-one.

The credit list of `night-signal`, in this order: `Chief Creative Officer` Ren Shibata;
`Head of Innovation` Takumi Aoki; `Senior Creative Director` Shun Kaneda;
`Creative Director` Kaito Arai; `Art Director` Mio Hirano; `Experience Planner` Nana Ishii;
`Technical Director and Programmer` Leo Tanaka; `Senior Copywriter` Asuka Noda;
`Experience Planner` Kou Endo; `Producer` Yuto Baba, Riko Nishi and Sho Ota;
`Account Director` Ami Goto; `Editor` Kei Yamada. Shun Kaneda departed on `2026-02-27`.
Each of them holds a matching assignment on that campaign's job.

Award bodies: `lotus-festival` (`Lotus Festival`, June) and `north-star-awards`
(`North Star Awards`, November), with the ranks named in `## Core features` rule 21.
Confirmed `Lotus Festival` results for `2025`:

| Campaign | Category path | Rank |
|---|---|---|
| `night-signal` | Innovation / Early-stage Technology | `Grand Lotus` |
| `night-signal` | Digital Craft / Interface | `Gold` |
| `night-signal` | Brand Experience / Activation | `Silver` |
| `quiet-engine` | Film / Film Craft | `Gold` |
| `quiet-engine` | Outdoor / Ambient | `Silver` |
| `quiet-engine` | Film / Direction | `Bronze` |
| `quiet-engine` | Outdoor / Transit | `Bronze` |
| `rice-field-radio` | Radio and Audio / Audio Craft | `Jade Petal` |
| `rice-field-radio` | Radio and Audio / Use of Music | `Jade Petal` |

`night-signal` also holds a shortlisted, unconfirmed entry in Film / Film Craft for `2025`.
`cloud-orchard` holds one confirmed `North Star Awards` `Merit` for `2024`.

Twenty published articles, nine per page. Among them `lotus-festival-2025-results`
(`Lotus Festival 2025 results`, dated `2025-06-21`, categories `awards` and `news`,
reporting `Lotus Festival` `2025`). The rest are spread over `2024` to `2026` across the
three categories, and no `stories` article is dated `2019`.

Enquiry routes as in rule 35. Officers and openings as in `## Front-end specification`.
No page views and no enquiries are seeded.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One agency, one organisation. The only walls are between accounts; there is no second
  tenant.
- No client login and no client portal; a client sees work through preview links only.
- No self-service signup, no password reset by mail, no single sign-on.
- No executive role, no global administrator, and no standing exemption from the wall.
- No payments, invoicing or billing provider. Costs are recorded, not charged.
- No mail is sent by the app; enquiry routing is recorded.
- No third-party analytics, no consent-platform vendor and no external network call at
  run time. The consent banner is the app's own.
- No external applicant tracking integration beyond an outbound apply link.
- No binary asset copied from any other site; every asset is generated.
- No rounded corners, no soft shadows and no centred single column on the public site.
- The seed carries twenty articles and thirty-five campaign records, and the indexes
  are built for hundreds of campaigns and articles: paging, facets and search stay
  correct at that volume.
- No notifications of any kind: the product sends no mail, no push message and no
  in-app notification.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not be
  running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Every endpoint below is under the `/api` prefix. Field names are exact. Dates are
`YYYY-MM-DD`, moments are ISO 8601 with an offset, months are `YYYY-MM`, markets are
two-letter codes, and money is an integer.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | `access_token` and `account` with `email`, `role`, `person_id` |
| `GET /api/auth/me` | none | `email`, `role`, `person_id` |
| `POST /api/auth/signup` | anything | refused as a client error; no account is created |
| `GET /api/health` | none | a health object |
| `GET /api/clients` | optional `locale` | a top-level array of `slug`, `name`, `reading`, `competitors` in that locale's collation order |
| `GET /api/accounts` | none | a top-level array of the accounts the caller is cleared for: `slug`, `client`, `owner_person_id` |
| `GET /api/people` | optional `locale` | a top-level array of `id`, `name`, `reading`, `unit`, `status` in collation order |
| `GET /api/people/{id}` | none | `id`, `name_en`, `name_ja`, `reading`, `unit`, `status`, `capacity_minutes`, `clearances` (each `id`, `account`, `starts_on`, `ends_on`, `revoked_on`, `source`), `assignments` (each `id`, `job_id`, `role`, `starts_on`, `ends_on`, readable jobs only) |
| `POST /api/people` | `name_en`, `name_ja`, `reading`, `unit` (a unit name such as `Planning` or `Hoshino Unit`), `capacity_minutes` | the person |
| `PATCH /api/people/{id}` | any of `name_en`, `name_ja`, `reading` | the person |
| `POST /api/people/{id}/depart` | `departed_on` | the person, `status` `departed` |
| `POST /api/people/{id}/return` | `returned_on` | the person, `status` `active`, `capacity_minutes` `2400` |
| `POST /api/people/{id}/clearances` | `account`, `starts_on`, `ends_on` | the clearance |
| `POST /api/clearances/{id}/revoke` | `revoked_on` | the clearance |
| `POST /api/briefs` | `accounts`, `title`, `problem`, `convention`, `deliverables`, `deadline`, `budget_minor`, `markets` | the brief, `status` `open` |
| `GET /api/briefs` | none | a top-level array of readable briefs: `id`, `title`, `accounts`, `status` |
| `POST /api/briefs/{id}/estimates` | `amount_minor` | the estimate: `id`, `version`, `amount_minor`, `status` `draft` |
| `POST /api/estimates/{id}/approve` | none | the estimate, `status` `approved` |
| `POST /api/briefs/{id}/convert` | `producer_person_id`, `apportionment` (each `account`, `share_bp`) | the job: `id`, `title`, `accounts`, `apportionment`, `rate_card_version` |
| `GET /api/jobs` | none | a top-level array of readable jobs: `id`, `title`, `accounts`, `estimate_minor`, `actual_minor`, `legal_hold` |
| `GET /api/jobs/{id}` | none | one readable job: `id`, `title`, `accounts`, `rate_card_version`, `legal_hold`, `status` |
| `GET /api/jobs/{id}/cost` | none | `rate_card_version`, `time_minor`, `third_party_minor`, `total_minor`, `currency` |
| `GET /api/jobs/{id}/audit` | none | a top-level array of `id`, `action`, `actor_person_id`, `at`, `reason` |
| `DELETE /api/audit-events/{id}` | none | refused as a client error; the event remains |
| `GET /api/search` | `q` | a top-level array of readable `kind`, `id`, `title` |
| `GET /api/autocomplete` | `q` | a top-level array of readable `kind`, `id`, `label` |
| `GET /api/reports/burn` | none | `jobs_counted`, `estimate_minor`, `actual_minor`, `partial` |
| `GET /api/reports/jobs.csv` | none | CSV with a header row and one row per readable job, carrying its title |
| `GET /api/rate-cards` | none | a top-level array of `version`, `effective_from`, `effective_to` |
| `GET /api/rate-cards/{version}` | none | `version`, `effective_from`, `effective_to`, `rates` (an object of role to hourly amount) |
| `POST /api/rate-cards` | `version`, `effective_from`, `rates` | the card |
| `POST /api/jobs/{id}/assignments` | `person_id`, `role`, `starts_on`, `ends_on`, `minutes_per_week` | the assignment: `id`, `person_id`, `role`, `starts_on`, `ends_on`, `minutes_per_week` |
| `GET /api/jobs/{id}/assignments` | none | a top-level array of every assignment, ended ones included |
| `POST /api/assignments/{id}/end` | `ends_on` | the assignment |
| `DELETE /api/assignments/{id}` | none | refused as a client error |
| `POST /api/jobs/{id}/time-entries` | `person_id`, `role`, `work_date`, `minutes` | the entry: `id`, `minutes`, `cost_minor`, `period`, `adjusts_entry_id` |
| `GET /api/jobs/{id}/time-entries` | none | a top-level array of entries |
| `POST /api/periods/{month}/close` | none | `month`, `closed` |
| `POST /api/time-entries/{id}/corrections` | `minutes` | the adjusting entry when the original's month is closed, otherwise the updated entry |
| `POST /api/jobs/{id}/costs` | `supplier`, `amount_minor`, `currency`, `converted_minor`, `fx_rate`, `fx_date` | the cost entry with every field as stored |
| `POST /api/jobs/{id}/versions` | multipart `file`, `label` | the version: `number`, `label`, `object_key`, `sha256`, `internal_status`, `client_status`, `restored_from` |
| `GET /api/jobs/{id}/versions` | none | a top-level array of versions |
| `GET /api/jobs/{id}/versions/{number}` | none | the version with every comment |
| `GET /api/jobs/{id}/versions/{number}/client-view` | none | the version with its `client` comments only |
| `GET /api/jobs/{id}/versions/{number}/content` | none | the bytes |
| `DELETE /api/jobs/{id}/versions/{number}` | none | the withdrawal, or a refusal under legal hold |
| `POST /api/jobs/{id}/versions/{number}/restore` | none | the new version |
| `POST /api/jobs/{id}/versions/{number}/internal-review` | `status` | the version |
| `POST /api/jobs/{id}/versions/{number}/client-review` | `status` | the version |
| `POST /api/jobs/{id}/versions/{number}/comments` | `body`, `visibility`, `timecode` or `region` | the comment |
| `POST /api/jobs/{id}/rights` | `right`, `subject`, `licence_ref`, `term_start`, `term_end`, `territories`, `media`, `status` | the right |
| `GET /api/jobs/{id}/rights` | none | a top-level array of rights |
| `POST /api/jobs/{id}/legal-hold` | `reason` | the job, `legal_hold` true |
| `POST /api/jobs/{id}/legal-hold/lift` | `reason` | the job, `legal_hold` false |
| `POST /api/campaigns` | `job_id`, `slug`, `year`, `month`, `categories`, `clients` (each `slug`, `primary`), `external_url` | the campaign: `id`, `slug`, `state` `draft` |
| `GET /api/campaigns` | optional `slug` | a top-level array of readable campaigns: `id`, `slug`, `job_id`, `state`, `embargo_at`, `hero_asset_id` |
| `PUT /api/campaigns/{id}/translations/{locale}` | `title`, `description`, `status` | the translation |
| `POST /api/campaigns/{id}/hero` | multipart `file`, `alt_en`, `alt_ja` | the media: `id`, `object_key`, `sha256`; the key is `campaigns/{campaign_id}/{sha256_of_bytes}.{ext}` |
| `GET /api/campaigns/{id}/credits` | none | `revision` and `entries` (each `position`, `role_en`, `role_ja`, `pin_names`, `people`, each person `person_id`, `name_en`, `name_ja`) |
| `PUT /api/campaigns/{id}/credits` | `revision`, `entries` (each `role_en`, `role_ja`, `pin_names`, `people` as person ids) | the list with its new `revision` |
| `POST /api/campaigns/{id}/permissions` | `kind`, `reference` | the permission |
| `POST /api/campaigns/{id}/publish` | `markets`, optional `embargo_at` | the campaign, `state` `published` or `scheduled`; a refusal carries `reasons` |
| `POST /api/campaigns/{id}/unpublish` | none | the campaign |
| `POST /api/campaigns/{id}/preview-links` | `expires_in_minutes` | `token`, `expires_at` |
| `POST /api/preview-links/{token}/revoke` | none | the link |
| `GET /api/preview/{token}` | none, no sign-in | the campaign as it will appear |
| `POST /api/articles` | `slug`, `date`, `categories`, `award_body`, `award_year`, `title_ja`, `title_en`, `body_ja`, `body_en` | the article: `id`, `slug`, `state` |
| `POST /api/articles/{id}/publish` | optional `embargo_at` | the article |
| `GET /api/award-bodies` | none | a top-level array of `slug`, `name`, `ranks` (each `name`, `ordinal`, `counts_toward`), `categories` (each `id`, `section`, `name`) |
| `POST /api/award-bodies/{slug}/categories` | `section`, `name` | the category |
| `POST /api/award-entries` | `campaign_id`, `body`, `category_id`, `year`, `fee_minor`, `client_permission_ref` | the entry: `id`, `status` |
| `POST /api/award-entries/{id}/results` | `rank`, `confirmed` | the result: `id`, `rank`, `confirmed`, `entry_status` |
| `POST /api/award-results/{id}/confirm` | none | the result, with `entry_status` |
| `POST /api/award-entries/{id}/close` | none | the entry, `status` `closed` |
| `GET /api/public/campaigns` | `locale`, `year` (a year or `before`), `page`, `market` | `total`, `page`, `page_count`, `year_buckets` (a list of strings in facet order: `all`, each listed year, `before`), `items` (each `slug`, `title`, `description`, `primary_client`, `categories`, `year`) |
| `GET /api/public/campaigns/{slug}` | `locale`, `market` | `slug`, `title`, `description`, `lang` (the locale shown for `title` and for `description`), `clients` (each `name`, `primary`), `categories`, `date`, `external_url`, `hero_asset_id`, `awards` (each `body` as the body's name, `year`, `results` of `category` and `rank`), `credits` (each `position`, `role`, `people` of `name` and `lang`), `related` |
| `GET /api/public/news` | `locale`, `category`, `year`, `page` | `total`, `page`, `page_count`, `items` (each `slug`, `title`, `date`, `categories`) |
| `GET /api/public/news/{slug}` | `locale` | the article, with `breakdown` (each `campaign`, `category`, `rank`) on an award article |
| `GET /api/public/awards/tally` | optional `body` (a body slug), `year` | `total`, `itemised` and `headline`, each a list of `rank` and `count`; a rank that rolls into another is absent from `headline` |
| `GET /api/public/search` | `q`, `locale` | a top-level array of `kind`, `slug`, `title` |
| `GET /api/public/company` | `locale` | `legal_name`, `address`, `telephone`, `founded`, `updated`, `officers` (each `name`, `title`, `concurrent_position`), `units` (each `name`, `dedicated_client`) |
| `GET /api/public/careers` | `locale` | `values`, `openings` (each `track`, `title`, `apply_url`) |
| `GET /api/public/assets/{id}` | none | the bytes of a public campaign's media |
| `GET /api/enquiries/key` | none | `idempotency_key` |
| `POST /api/enquiries` | `idempotency_key`, `type`, `name`, `company`, `email`, `telephone`, `message`, `consent`, `website` | `id`, `routed_to`, `routing_warning` |
| `POST /api/page-views` | `route` | the recorded view |
| `GET /api/page-views` | none | a top-level array of `route` and `viewed_at`, newest first |

Public read endpoints default to `locale` `ja` and `market` `JP`. A list endpoint returns a
top-level JSON array unless its row above names its fields. A successful call returns the
named resource or shape; an invalid or unauthorized call is rejected as a client error,
never as a server error and never as a silent success, and a refusal body carries a
`message`. A read of anything the wall hides answers exactly as a missing record does.
Bearer authentication is required on everything except login, health, the `public`
endpoints, the preview endpoint, the enquiry endpoints and the page-view record.

### No mocks

`minio` is where the bytes live. An in-memory buffer the app hands back to itself, a file
written to the app container's own filesystem, a base64 column in `PostgreSQL`, a hero
film copied into the public build, or an object key pointing at nothing is each a contract
violation however good the upload screen looks. `PostgreSQL` is where the records live: a
tally, a cost or a clearance list held in memory and never stored is the same violation.
The named provider is the fact: the app's own interface can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger reads `Night Signal` in Japanese and in English with its ordered credits and
its `Lotus Festival` results, and an editor publishes `Paper Lanterns` to the public site
in both languages. Nobody cleared only for `Tsubame Automotive` can find any trace of
`Hoshino EV Launch`.
