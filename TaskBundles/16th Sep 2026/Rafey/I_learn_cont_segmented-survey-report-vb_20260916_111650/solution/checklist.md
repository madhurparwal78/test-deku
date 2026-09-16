# Checklist: Studio Signals

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, deployment
Sections absent: buildplan
Items: 176
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `data` A published share, like every figure, is generated from one dataset of stored survey results. `src: Overview, Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` A request for another reader's saved export, or the export's download, answers `404`. `src: User roles, User roles para`
- [ ] `C-RL-02` `role` A `reader` is denied removing another reader's saved export. `src: User roles, User roles table row 2`
- [ ] `C-RL-03` `role` A `reader` is denied listing another reader's saved exports. `src: User roles, User roles table row 2`
- [ ] `C-RL-04` `capability` Anyone creates a `reader` account from `/sign-up`, usable at once. `src: User roles, User roles signup para`

## C-CF Core features

- [ ] `C-CF-01` `ui` The chapter rail lists every finding by short title, then the three closers. `src: Core features, The rail para`
- [ ] `C-CF-02` `literal` With the seed the first heading states `46%` daily use of AI tools, a rise of 16 since 2025. `src: Core features, Headings table row 1`
- [ ] `C-CF-03` `literal` The source line reads `Source: Studio Signals survey, 2026 wave, all respondents, base 869.` for the whole population. `src: Core features, Source line para`
- [ ] `C-CF-04` `ui` The short caveat `Directional, not a benchmark. See methodology.` follows each source line as a methodology link. `src: Core features, Source line para`
- [ ] `C-CF-05` `ui` A chapter scrolled to its end marks the last rail entry as current. `src: Core features, The rail para`
- [ ] `C-CF-06` `ui` The first chapter ends with a next control showing `02 . Craft`, with no previous control. `src: Core features, Chapter head para`
- [ ] `C-CF-07` `data` The chapters `tools`, `craft`, `teams` carry three findings each, in reading order. `src: Core features, Chapters table`
- [ ] `C-CF-08` `constraint` Every finding heading is regenerated from the data by the finding's heading template. `src: Core features, Headings para`
- [ ] `C-CF-09` `literal` For all respondents the `stack-ranked` heading matches the template, naming `Canvas assistant` at `59%`. `src: Core features, Headings table row 2`
- [ ] `C-CF-10` `constraint` Every chart has a figures table stating the same values in the same order. `src: Core features, Text equivalent para`
- [ ] `C-CF-11` `constraint` Each key takeaway's text is that finding's regenerated heading, in finding order. `src: Core features, Closers para`
- [ ] `C-CF-12` `literal` A chapter head reads `<n> min read, charts excluded`. `src: Core features, Chapter head para`
- [ ] `C-CF-13` `constraint` The third chapter has no next control; the first has no previous control. `src: Core features, Chapter head para`
- [ ] `C-CF-14` `literal` The methodology states a 2026 population of `869`, a 2025 population of `709`. `src: Core features, About para`
- [ ] `C-CF-15` `ui` The methodology states the composition by company size, work environment, experience. `src: Core features, About para`
- [ ] `C-CF-16` `literal` The methodology carries the full caveat ending `directional rather than as absolute benchmarks.`. `src: Core features, About para`
- [ ] `C-CF-17` `data` A published figure is the sum of stored result rows over the segment's cells divided by respondents. `src: Core features, Dataset rule 1`
- [ ] `C-CF-18` `constraint` A `single` question's full-precision shares sum to one; a `multi` question's shares are not rescaled. `src: Core features, Dataset rule 2`
- [ ] `C-CF-19` `constraint` A `numeric` question publishes a mean of summed tenths divided by ten, by respondents. `src: Core features, Dataset rule 2`
- [ ] `C-CF-20` `literal` The numeric `tool-count` mean heading reads `Designers use 5.8 AI tools in a typical week.` with the seed. `src: Core features, Headings table row 4`
- [ ] `C-CF-21` `constraint` A movement rounds the difference of full-precision shares once, never subtracting two rounded shares. `src: Core features, Dataset rule 3`
- [ ] `C-CF-22` `literal` A share displays as a whole percentage rounded half up, `0.4591` displaying `46%`. `src: Core features, Dataset rule 3`
- [ ] `C-CF-23` `constraint` A share's margin follows the stated interval formula, `1.96` times the root of `p(1 - p) / n`. `src: Core features, Dataset rule 6`
- [ ] `C-CF-24` `constraint` The segments endpoint's composition is computed from the same cells the chapters read. `src: Core features, About para`
- [ ] `C-CF-25` `literal` The about page states the confidence level once as `Figures carry a 95% confidence interval.`. `src: Core features, Dataset rule 6`
- [ ] `C-CF-26` `ui` Changing a segment recomputes the chapter in place, the address gaining the segment without navigating. `src: Core features, Segments para`
- [ ] `C-CF-27` `literal` The state line reads `Showing Startups (1 to 50). 223 of 869 respondents.` under `?size=startup`. `src: Core features, Segments para`
- [ ] `C-CF-28` `literal` Under `?size=startup` the stack heading names two tools too close to separate. `src: Core features, Headings para`
- [ ] `C-CF-29` `ui` A source line names the segment in force with the segment base. `src: Core features, Source line para`
- [ ] `C-CF-30` `ui` `Show everyone` clears the segment in one action. `src: Core features, Segments para`
- [ ] `C-CF-31` `literal` With no segment the state line reads `Showing all respondents.`. `src: Core features, Segments para`
- [ ] `C-CF-32` `ui` An address carrying an unknown band shows the unknown-group notice above the whole report. `src: Core features, Segments para`
- [ ] `C-CF-33` `literal` An address carrying a segment shows the filtered-link notice naming the segment label. `src: Core features, Segments para`
- [ ] `C-CF-34` `literal` An unknown band resolves to all respondents with the unknown-group notice ending `Showing everyone.`. `src: Core features, Segments para`
- [ ] `C-CF-35` `capability` A reader chooses a segment, every heading recomputed for that segment. `src: Core features, Overview para 4`
- [ ] `C-CF-36` `constraint` Segment controls compose into an intersection whose base is smaller than either band. `src: Core features, Segments para`
- [ ] `C-CF-37` `literal` Segment controls compose labels in dimension order, for example `Startups (1 to 50), Agency`. `src: Core features, Segments para`
- [ ] `C-CF-38` `literal` The state line reads `Showing <label>. <segment base> of <population> respondents.` for a chosen segment. `src: Core features, Segments para`
- [ ] `C-CF-39` `literal` A segment change makes one announcement, `Now showing <label>, <segment base> respondents.`. `src: Core features, Segments para`
- [ ] `C-CF-40` `constraint` The finding under the reader's eye stays under the reader's eye through a segment change. `src: Core features, Segments para`
- [ ] `C-CF-41` `constraint` A ranking reorders by full-precision share, ties broken by option order. `src: Core features, Forms para`
- [ ] `C-CF-42` `literal` Under Enterprise the ranking heading names Speed with Team standard as too close to separate. `src: Core features, Headings table row 6`
- [ ] `C-CF-43` `constraint` Every finding is addressable at `/chapters/<chapter>#<finding id>` carrying the segment's query parameters. `src: Core features, Addresses para`
- [ ] `C-CF-44` `literal` A withdrawn chart reads `Too few respondents` followed by the group's answered count. `src: Core features, Withdrawn finding para`
- [ ] `C-CF-45` `ui` A breakdown band below the threshold reads `not reported, base too small` with the band base printed. `src: Core features, Forms para`
- [ ] `C-CF-46` `literal` A share whose base is under `200` shows as `47%, give or take 7. Based on 195 answers.` for an agency segment. `src: Core features, Dataset rule 6`
- [ ] `C-CF-47` `constraint` A segment below the `30` respondent threshold withholds every figure from chart, heading, takeaway, export row. `src: Core features, Dataset rule 5`
- [ ] `C-CF-48` `literal` A withdrawn finding's heading gives the reason, the short title marked not reported for the group. `src: Core features, Withdrawn finding para`
- [ ] `C-CF-49` `constraint` A segment breakdown intersects each company size band with the segment in force, each band printing the band base. `src: Core features, Forms para`
- [ ] `C-CF-50` `constraint` A withdrawn finding exports the heading plus the too-few-respondents sentence in place of the table. `src: Core features, Export para`
- [ ] `C-CF-51` `literal` A movement whose 2025 segment base is below the threshold has state `suppressed`, cell text `Too few 2025 answers to compare.`. `src: Core features, Dataset rule 4`
- [ ] `C-CF-52` `ui` The movement list renders rise, fall, no change, no detectable change, not asked as distinct cells. `src: Core features, Forms para`
- [ ] `C-CF-53` `ui` A `two-wave` chart for a non-comparable question shows 2026 alone with the asked-differently sentence. `src: Core features, Forms para`
- [ ] `C-CF-54` `literal` Adjacent ranked options whose difference is unsupported are marked with `These two are too close to separate.`. `src: Core features, Forms para`
- [ ] `C-CF-55` `constraint` The rule assigns each movement state: `rise` or `fall` when supported, `no-change` when unsupported rounding to zero, `not-detectable` otherwise. `src: Core features, Dataset rule 4`
- [ ] `C-CF-56` `literal` The stack movement cell reads `+19pts` for a rise, `-9pts` for a fall. `src: Core features, Forms para`
- [ ] `C-CF-57` `constraint` A not asked option's movement is never a rise from zero. `src: Core features, Dataset rule 4`
- [ ] `C-CF-58` `constraint` A question recorded as not comparable between waves gives movement state `not-comparable`. `src: Core features, Dataset rule 4`
- [ ] `C-CF-59` `literal` The comparison state line reads `Comparing <label A> with <label B>.`. `src: Core features, Comparison para`
- [ ] `C-CF-60` `literal` An unsupported focus difference reads `Too close to call for these two groups.`. `src: Core features, Comparison para`
- [ ] `C-CF-61` `literal` A comparison whose second base is under the threshold says `<label B> has too few respondents to compare.`. `src: Core features, Comparison para`
- [ ] `C-CF-62` `constraint` A difference between two shares is supported when larger than `1.96` times the root of the summed binomial variances. `src: Core features, Dataset rule 7`
- [ ] `C-CF-63` `literal` A supported comparison sentence reads `A real difference between these two groups.`. `src: Core features, Comparison para`
- [ ] `C-CF-64` `constraint` Suppression is per side: a short second segment leaves the first segment shown alone. `src: Core features, Comparison para`
- [ ] `C-CF-65` `ui` Every chapter offers `Download the report as markdown` carrying the segment in force. `src: Core features, Export para`
- [ ] `C-CF-66` `ui` The citation sentence opens with the publication, the wave, the quoted heading of the finding. `src: Core features, Citation para`
- [ ] `C-CF-67` `contract` `GET /api/export.md` answers `200` with `text/markdown; charset=utf-8`, attachment `studio-signals-2026.md`, no account needed. `src: Core features, Export para`
- [ ] `C-CF-68` `constraint` Every figure in the export equals the figure on the page for the same segment, from one code path. `src: Core features, Export para`
- [ ] `C-CF-69` `literal` The export head reads `# Studio Signals, 2026 wave. Exported <YYYY-MM-DD>. <Label>.`. `src: Core features, Export para`
- [ ] `C-CF-70` `literal` Under the export head, line 3 carries the short caveat, line 4 the confidence sentence. `src: Core features, Export para`
- [ ] `C-CF-71` `contract` The `two-wave`, `movement-list` export table header is `| Option | 2025 | 2026 | Change |`. `src: Core features, Export para`
- [ ] `C-CF-72` `contract` The `segment-breakdown` export table header is `| Company size | 2026 | Base |`. `src: Core features, Export para`
- [ ] `C-CF-73` `constraint` The export follows the segment in force, stating the segment at the head, against every figure. `src: Core features, Export para`
- [ ] `C-CF-74` `literal` The citation sentence reads `Studio Signals, 2026 wave. "<heading>" Base <segment base>, <label>.` then the caveat, retrieval date, address. `src: Core features, Citation para`
- [ ] `C-CF-75` `literal` A filtered citation carries a note recording the filter to the segment label. `src: Core features, Citation para`
- [ ] `C-CF-76` `ui` Wizard step 1 at `/library/new` asks for the segment, prefilled from the segment the reader came from. `src: Core features, Library table row 1`
- [ ] `C-CF-77` `ui` Wizard step 2 at `/library/new/compare` asks for an optional comparison segment. `src: Core features, Library table row 2`
- [ ] `C-CF-78` `ui` Wizard step 3 at `/library/new/review` shows the export head line with the figure count before `Save to library`. `src: Core features, Library table row 3`
- [ ] `C-CF-79` `ui` `/library` shows saved exports as a card grid, each card a label, a date, a download link, `Remove`. `src: Core features, Library para`
- [ ] `C-CF-80` `ui` Removing a card removes the card at once, restoring the card with `Could not remove that export.` on refusal. `src: Core features, Library para`
- [ ] `C-CF-81` `constraint` A saved export's object bytes equal the bytes `GET /api/export.md` returns for the same segment on the same day. `src: Core features, Library para`
- [ ] `C-CF-82` `constraint` Removing an export deletes the export record, the stored object. `src: Core features, Library para`
- [ ] `C-CF-83` `literal` A comparison export's label reads `Comparing <label A> with <label B>`. `src: Core features, Library para`
- [ ] `C-CF-84` `ui` A library route with no session sends the visitor to sign in, returning there after signing in. `src: Core features, Accounts para`
- [ ] `C-CF-85` `contract` A saved export's download answers `401` to a request with no session. `src: Core features, Library para`
- [ ] `C-CF-86` `ui` The cover contents shows `Part-way through` for a chapter with a finding recorded. `src: Core features, Reading position para`
- [ ] `C-CF-87` `literal` Returning offers `You were part-way through <number> <title>. Pick up where you left off?`. `src: Core features, Reading position para`
- [ ] `C-CF-88` `constraint` A reading position survives a reload, signing out, signing back in, a new browser. `src: Core features, Reading position para`
- [ ] `C-CF-89` `constraint` A chapter reads `Not started` with no record, `Part-way through` with a finding, `Finished` once `closers` is recorded. `src: Core features, Reading position para`
- [ ] `C-CF-90` `constraint` A reader opening a chapter with no segment in the address is redirected to the address carrying the stored segment. `src: Core features, Reading position para`
- [ ] `C-CF-91` `constraint` Opening an address carrying a segment stores that segment, replacing the previous one. `src: Core features, Reading position para`
- [ ] `C-CF-92` `literal` `Show everyone` clears the stored segment, the address carrying `segment=all`. `src: Core features, Reading position para`
- [ ] `C-CF-93` `ui` `/sign-up` links to `/terms` on the form. `src: Core features, Accounts para`
- [ ] `C-CF-94` `ui` An announced case study renders the number, the subject, `Coming soon`, never as a link. `src: Core features, Case studies para`
- [ ] `C-CF-95` `ui` `Get new case studies` asks for an email address with an explicit, unticked consent checkbox. `src: Core features, Case-study notices para`
- [ ] `C-CF-96` `literal` The not-found page is headed `Page not found` with a link reading `Back to the report`. `src: Core features, Not found para`
- [ ] `C-CF-97` `constraint` A submission with anything in the decoy `website` field is refused with `400`, creating nothing. `src: Core features, Case-study notices para`
- [ ] `C-CF-98` `constraint` A second subscription for the same address within sixty seconds is refused with `429`. `src: Core features, Case-study notices para`
- [ ] `C-CF-99` `contract` `POST /api/subscriptions` answers `201`, recording the address once. `src: Core features, Case-study notices para`
- [ ] `C-CF-100` `constraint` A wrong password, an unknown address answer with one shared credential-mismatch message. `src: Core features, Accounts para`
- [ ] `C-CF-101` `constraint` `/terms` is reachable from the footer of every page, linked from the sign-up form. `src: Core features, Terms para`
- [ ] `C-CF-102` `contract` Any unknown path renders the not-found page inside the full chrome, answering `404`. `src: Core features, Not found para`
- [ ] `C-CF-103` `contract` `/cases/<slug>` for an announced case study answers `404`, as does the study's API record. `src: Core features, Case studies para`
- [ ] `C-CF-104` `data` Published case studies are `01` Harbour Type Co., `02` Kestrel Health, `03` Fieldwork Studio. `src: Core features, Case studies table`
- [ ] `C-CF-105` `constraint` Every internal link on every public page resolves to a page answering `200`. `src: Core features, Not found para`
- [ ] `C-CF-106` `ui` The previous control, the next control, the chapter links all carry the segment in force. `src: Core features, Segments para`
- [ ] `C-CF-107` `ui` A citation comes in three shapes built from one object: a sentence, a structured record, the address alone. `src: Core features, Citation para`
- [ ] `C-CF-108` `ui` A withdrawn finding reads as a designed state of the chapter. `src: Core features, Withdrawn finding para`

## C-UF User flow

- [ ] `C-UF-01` `capability` `Read the Report` opens `/chapters/tools` directly rather than a contents page. `src: User flow, Routes para`
- [ ] `C-UF-02` `literal` Under Startups the first heading becomes `55%` daily use, a rise of 16 since 2025. `src: User flow, Journeys para 1`
- [ ] `C-UF-03` `contract` Segment keys `size`, `env`, `exp` recompute every chapter heading. `src: User flow, API para`
- [ ] `C-UF-04` `ui` Under Growth with Freelance every finding is withdrawn with the twenty-respondent reason. `src: User flow, Journeys para 3`
- [ ] `C-UF-05` `literal` Startups against Enterprise reads `Startups (1 to 50) 30%, Enterprise (2,000+) 17%. A real difference between these two groups.`. `src: User flow, Journeys para 2`
- [ ] `C-UF-06` `literal` An empty library reads `Nothing saved yet.` with a link to `/library/new`. `src: User flow, States table row 2`
- [ ] `C-UF-07` `contract` A visitor reaching `/library` or a wizard step is redirected to `/sign-in?next=<path>`. `src: User flow, Entry table row 4`
- [ ] `C-UF-08` `ui` Returning to a part-read chapter offers the resume prompt without scrolling. `src: User flow, Journeys para 5`
- [ ] `C-UF-09` `literal` The footer names both publishers with the wave year, `©2026 Northbeam Research, Aster & Vale. All rights reserved`. `src: User flow, Routes para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `constraint` The rail is a navigation landmark whose current entry is marked programmatically. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-02` `constraint` With reduced motion, every chart renders at final values with no growth. `src: UI/UX notes, Motion para`
- [ ] `C-UX-03` `constraint` A segment change is announced once, keeping focus where the focus was. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-04` `constraint` Body text, chart values meet the WCAG AA contrast bar of 4.5:1 against their ground. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-05` `constraint` No figure renders below `13px`; no prose renders below `16px`. `src: UI/UX notes, Typography para`
- [ ] `C-UX-06` `constraint` A chart never makes the page scroll sideways. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-07` `ui` At a narrow window the prose sits above the prose's chart, a claim never separated from the claim's chart. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-08` `ui` A chart never re-animates on scrolling back into view. `src: UI/UX notes, Motion para`
- [ ] `C-UX-09` `ui` Body prose holds a comfortable measure at every width. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-10` `ui` Links move colour, underline together on a symmetrical ease. `src: UI/UX notes, Motion para`
- [ ] `C-UX-11` `ui` Keyboard navigation shows a visible focus outline on every sidebar control. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-12` `ui` At a narrow window chart labels move above their bars. `src: UI/UX notes, Responsive para`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The cover title block is a solid near-black block reading `Studio Signals` over two lines with `2026` beneath. `src: Front-end specification, The cover para`
- [ ] `C-FE-02` `ui` The cover ground is a slow drifting gradient with grain, scattered with captioned tiles. `src: Front-end specification, The cover para`
- [ ] `C-FE-03` `ui` The cover contents lists the three chapters with number, title, reading time. `src: Front-end specification, The cover para`
- [ ] `C-FE-04` `ui` The cover shows the case-study set as a card grid of seven numbered cards. `src: Front-end specification, The cover para`
- [ ] `C-FE-05` `ui` A wide window sets the finding prose beside the chart as one region. `src: Front-end specification, Layout para`
- [ ] `C-FE-06` `constraint` Each chapter page is server-rendered markup carrying every heading, figures table, source line. `src: Front-end specification, The charts para`
- [ ] `C-FE-07` `constraint` A share whose base is under two hundred prints the interval in words beneath the bar. `src: Front-end specification, The charts para`
- [ ] `C-FE-08` `ui` A rise or a fall carries an upward or downward mark beside the signed figure; other states read as words. `src: Front-end specification, The charts para`
- [ ] `C-FE-09` `ui` The ordered ranking is a numbered list with values withheld, a `Show the values` control revealing each share. `src: Front-end specification, The charts para`
- [ ] `C-FE-10` `ui` A comparison adds the compare series beneath each accent bar in the deep neutral. `src: Front-end specification, The charts para`
- [ ] `C-FE-11` `ui` A movement mark never appears on a comparison row. `src: Front-end specification, The charts para`
- [ ] `C-FE-12` `ui` The cover title block keeps the title legible over the moving ground at every moment. `src: Front-end specification, The cover para`
- [ ] `C-FE-13` `ui` Each bar starts a short moment after the bar above, the stagger worked out per bar. `src: Front-end specification, The reveal para`
- [ ] `C-FE-14` `ui` At a narrow window the rail sits behind a `Sections` control opening the section list as a sheet. `src: Front-end specification, The sidebar para`
- [ ] `C-FE-15` `ui` Part-to-whole options are told apart by alternating tints, not by position alone. `src: Front-end specification, The charts para`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` One query layer serves the chapter pages, the chapter API, the export, the library save, the citation. `src: Technical requirements, One query layer para`
- [ ] `C-TR-02` `contract` A saved export's content type is `text/markdown; charset=utf-8`. `src: Technical requirements, Exports in the store para`
- [ ] `C-TR-03` `contract` A saved export's object key is `exports/{account_id}/{export_id}.md`. `src: Technical requirements, Exports in the store para`
- [ ] `C-TR-04` `constraint` The bucket carries no anonymous read policy for export objects. `src: Technical requirements, Exports in the store para`

## C-DM Data model

- [ ] `C-DM-01` `data` Every stored `result` count follows the seed generation rule from the rates, shifts, respondents. `src: Data model, Seed results para`
- [ ] `C-DM-02` `literal` Under the seed generation rule the 2026 `daily` result count for `startup`, `in-house`, `under-10` is `33`. `src: Data model, Seed results para`
- [ ] `C-DM-03` `constraint` An option not asked in 2025 has no 2025 result rows. `src: Data model, Entities para`
- [ ] `C-DM-04` `data` The `team-policy` question is recorded as not comparable, the wording changed in 2026. `src: Data model, Seed questions table`
- [ ] `C-DM-05` `constraint` Options are stored in the order listed, the order breaking ranking ties. `src: Data model, Seed results para`
- [ ] `C-DM-06` `constraint` An export's object bytes equal the export rendered for the same segment on the same day. `src: Data model, Invariants`
- [ ] `C-DM-07` `data` An `export` row carries `account_id`, `storage_key`, the segment columns, `label`, `created_at`. `src: Data model, Entities para`
- [ ] `C-DM-08` `constraint` A saved export, the export's object are readable only by the account that saved the export. `src: Data model, Invariants`
- [ ] `C-DM-09` `data` A reading position is a `progress` row carrying `account_id`, `chapter`, `finding`, `updated_at`. `src: Data model, Entities para`
- [ ] `C-DM-10` `constraint` `progress.finding` is a finding id of that chapter, or `closers`. `src: Data model, Field rules table`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No published share is typed into a template, a sentence, a takeaway, an export. `src: Constraints, constraints bullet`
- [ ] `C-CN-02` `constraint` The export never sits behind the notice form. `src: Constraints, constraints bullet`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` `GET /api/report` returns the chapters with `slug`, `number`, `title`, `reading_minutes`, `findings`. `src: Deployment contract, API table`
- [ ] `C-DC-02` `contract` `takeaways` carries `finding`, `text`, one per finding in order. `src: Deployment contract, API para`
- [ ] `C-DC-03` `contract` `GET /api/segments` returns `threshold`, `confidence`, `population`, `dimensions` with band `respondents`. `src: Deployment contract, API table`
- [ ] `C-DC-04` `contract` An unknown band is no error: the response resolves for all respondents, `notice` carrying the unknown-segment sentence. `src: Deployment contract, API para`
- [ ] `C-DC-05` `contract` An adjacent ranked row too close to separate carries `tied_with_next`. `src: Deployment contract, API para`
- [ ] `C-DC-06` `contract` A comparison row carries `compare` with `value`, `display`, `base`, `suppressed`, `supported`. `src: Deployment contract, API para`
- [ ] `C-DC-07` `contract` The citation returns `sentence`, `url`, `filtered_note`, `record` with `heading`, `base`, `segment`, `retrieved`. `src: Deployment contract, API table`
- [ ] `C-DC-08` `contract` `POST /api/exports` returns `201` with the export `id`, `label`, `storage_key`, `created_at`. `src: Deployment contract, API table`
- [ ] `C-DC-09` `contract` `GET /api/exports` returns the reader's own exports newest first. `src: Deployment contract, API table`
- [ ] `C-DC-10` `contract` `GET /api/progress` returns one row per chapter with `chapter`, `finding`, `state`. `src: Deployment contract, API table`
- [ ] `C-DC-11` `contract` `POST /api/auth/sign-up` creates a reader account usable at once, returning `role`, `token`. `src: Deployment contract, API table`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `46%` | pinned value | C-CF-02 | Core features, Headings table row 1 |
| `Source: Studio Signals survey, 2026 wave, all respondents, base 869.` | pinned value | C-CF-03 | Core features, Source line para |
| `stack-ranked` | pinned value | C-CF-09 | Core features, Headings table row 2 |
| `Canvas assistant` | pinned value | C-CF-09 | Core features, Headings table row 2 |
| `59%` | pinned value | C-CF-09 | Core features, Headings table row 2 |
| `<n> min read, charts excluded` | pinned value | C-CF-12 | Core features, Chapter head para |
| `869` | pinned measure | C-CF-14 | Core features, About para |
| `709` | pinned measure | C-CF-14 | Core features, About para |
| `directional rather than as absolute benchmarks.` | pinned value | C-CF-16 | Core features, About para |
| `tool-count` | pinned value | C-CF-20 | Core features, Headings table row 4 |
| `Designers use 5.8 AI tools in a typical week.` | pinned value | C-CF-20 | Core features, Headings table row 4 |
| `0.4591` | pinned measure | C-CF-22 | Core features, Dataset rule 3 |
| `Figures carry a 95% confidence interval.` | pinned value | C-CF-25 | Core features, Dataset rule 6 |
| `Showing Startups (1 to 50). 223 of 869 respondents.` | pinned value | C-CF-27 | Core features, Segments para |
| `?size=startup` | pinned value | C-CF-27 | Core features, Segments para |
| `Showing all respondents.` | pinned value | C-CF-31 | Core features, Segments para |
| `Showing everyone.` | pinned value | C-CF-34 | Core features, Segments para |
| `Startups (1 to 50), Agency` | pinned value | C-CF-37 | Core features, Segments para |
| `Showing <label>. <segment base> of <population> respondents.` | pinned value | C-CF-38 | Core features, Segments para |
| `Now showing <label>, <segment base> respondents.` | pinned value | C-CF-39 | Core features, Segments para |
| `Too few respondents` | pinned value | C-CF-44 | Core features, Withdrawn finding para |
| `200` | pinned measure | C-CF-46 | Core features, Dataset rule 6 |
| `47%, give or take 7. Based on 195 answers.` | pinned value | C-CF-46 | Core features, Dataset rule 6 |
| `suppressed` | pinned value | C-CF-51 | Core features, Dataset rule 4 |
| `Too few 2025 answers to compare.` | pinned value | C-CF-51 | Core features, Dataset rule 4 |
| `These two are too close to separate.` | pinned value | C-CF-54 | Core features, Forms para |
| `+19pts` | pinned value | C-CF-56 | Core features, Forms para |
| `-9pts` | pinned value | C-CF-56 | Core features, Forms para |
| `Comparing <label A> with <label B>.` | pinned value | C-CF-59 | Core features, Comparison para |
| `Too close to call for these two groups.` | pinned value | C-CF-60 | Core features, Comparison para |
| `<label B> has too few respondents to compare.` | pinned value | C-CF-61 | Core features, Comparison para |
| `A real difference between these two groups.` | pinned value | C-CF-63 | Core features, Comparison para |
| `# Studio Signals, 2026 wave. Exported <YYYY-MM-DD>. <Label>.` | pinned value | C-CF-69 | Core features, Export para |
| `Studio Signals, 2026 wave. "<heading>" Base <segment base>, <label>.` | pinned value | C-CF-74 | Core features, Citation para |
| `Comparing <label A> with <label B>` | pinned value | C-CF-83 | Core features, Library para |
| `You were part-way through <number> <title>. Pick up where you left off?` | pinned value | C-CF-87 | Core features, Reading position para |
| `Show everyone` | pinned value | C-CF-92 | Core features, Reading position para |
| `segment=all` | pinned value | C-CF-92 | Core features, Reading position para |
| `Page not found` | pinned value | C-CF-96 | Core features, Not found para |
| `Back to the report` | pinned value | C-CF-96 | Core features, Not found para |
| `55%` | pinned value | C-UF-02 | User flow, Journeys para 1 |
| `Startups (1 to 50) 30%, Enterprise (2,000+) 17%. A real difference between these two groups.` | pinned value | C-UF-05 | User flow, Journeys para 2 |
| `Nothing saved yet.` | pinned value | C-UF-06 | User flow, States table row 2 |
| `/library/new` | route | C-UF-06 | User flow, States table row 2 |
| `©2026 Northbeam Research, Aster & Vale. All rights reserved` | pinned value | C-UF-09 | User flow, Routes para |
| `daily` | pinned value | C-DM-02 | Data model, Seed results para |
| `startup` | pinned value | C-DM-02 | Data model, Seed results para |
| `in-house` | pinned value | C-DM-02 | Data model, Seed results para |
| `under-10` | pinned value | C-DM-02 | Data model, Seed results para |
| `33` | pinned measure | C-DM-02 | Data model, Seed results para |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the chapter word count behind the reading time | C-CF-12 | computed from prose the builder writes, so no literal minute count is given |
| the export id | C-TR-03 | named inside the key scheme with no literal format given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 1 |
| User roles | 1 | 4 |
| Core features | 27 | 108 |
| User flow | 7 | 9 |
| UI and UX notes | 1 | 12 |
| Front-end specification | 7 | 15 |
| Technical requirements | 4 | 4 |
| Data model | 0 | 10 |
| Constraints | 0 | 2 |
| Deployment contract | 9 | 11 |

