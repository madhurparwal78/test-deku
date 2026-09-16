# Checklist: Larkwise

Items: 170
Unpinned values flagged: 4
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

The coverage target, restated from `instruction.md` alone. One row per core ask,
each cited back to the section of the brief that states the obligation.

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves a marketing surface beside a learning surface under one name. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `literal` Every seeded learner can sign in with the pinned password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-02` `role` A cross account progress read is denied at the api with the rows unchanged. `src: User roles`
- [ ] `C-RL-03` `role` An unauthenticated request to a learner route is denied, redirecting the page to sign in. `src: User roles`
- [ ] `C-RL-04` `role` A learner cannot write a derived total directly. `src: User roles`
- [ ] `C-RL-05` `role` A restricted account is offered no purchase route anywhere. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `constraint` Signup with an existing email is refused, writing no second account row. `src: Core features, rule 1`
- [ ] `C-CF-02` `capability` Anonymous sample progress moves to the new account created from the same browser. `src: Core features, rule 4`
- [ ] `C-CF-03` `literal` The subject picker lists forty-two subjects in promoted order. `src: Core features`
- [ ] `C-CF-04` `literal` Only three subjects are open: `english`, `chess`, `math`. `src: Core features, rule 5`
- [ ] `C-CF-05` `capability` Every open subject page exposes two playable samples from the first unit. `src: Core features, rule 7`
- [ ] `C-CF-06` `data` A sample attempt is stored without an account against the browsing token. `src: Core features, rule 7`
- [ ] `C-CF-07` `literal` The english subject is taught from Spanish. `src: Core features, rule 8`
- [ ] `C-CF-08` `capability` Two language runs declare their own language on a subject page. `src: Core features, rule 93`
- [ ] `C-CF-09` `constraint` Enrolment is idempotent for one subject, leaving one row with the goal intact. `src: Core features, rule 9`
- [ ] `C-CF-10` `literal` A lesson session is assembled with twelve exercises. `src: Core features, rule 10`
- [ ] `C-CF-11` `constraint` A session exercise list is fixed after assembly, surviving a re-read. `src: Core features, rule 10`
- [ ] `C-CF-12` `constraint` Session assembly respects the type run, the concept run, the interleave positions, the opening ease. `src: Core features, rule 11`
- [ ] `C-CF-13` `literal` Attempt states are the four pinned values `correct`, `correct_with_note`, `incorrect`, `skipped`. `src: Core features, rule 14`
- [ ] `C-CF-14` `constraint` A wrong answer is requeued once as a different exercise for the same concept. `src: Core features, rule 15`
- [ ] `C-CF-15` `constraint` The frustration guard ends a concept after three wrong attempts inside one session. `src: Core features, rule 16`
- [ ] `C-CF-16` `capability` An interrupted session is resumable, offered rather than resumed silently. `src: Core features, rule 18`
- [ ] `C-CF-17` `constraint` Session reconcile is idempotent, so a second report does not double count. `src: Core features, rule 20`
- [ ] `C-CF-18` `constraint` Concurrent session reports produce one accepted result with nothing half-written. `src: Core features, rule 21`
- [ ] `C-CF-19` `constraint` Reconcile recomputes awards from stored attempts rather than from the report. `src: Core features, rule 20`
- [ ] `C-CF-20` `constraint` An out of order attempt report is refused, storing nothing. `src: Core features, rule 22`
- [ ] `C-CF-21` `constraint` An attempt faster than the human floor earns nothing. `src: Core features, rule 23`
- [ ] `C-CF-22` `constraint` A browser clock offset never moves an award. `src: Core features, rule 24`
- [ ] `C-CF-23` `data` Traces are rebuildable from the attempt log alone. `src: Core features, rule 51`
- [ ] `C-CF-24` `literal` Recall probability matches the pinned formula with the half-life inside its clamp. `src: Core features, rule 41`
- [ ] `C-CF-25` `literal` Due time matches the pinned formula at the default target retention `0.90`. `src: Core features, rule 46`
- [ ] `C-CF-26` `constraint` Trace evaluation is deterministic at one instant. `src: Core features, rule 53`
- [ ] `C-CF-27` `constraint` A returning learner is not buried by the backlog, seeing a proportion of the subject. `src: Core features, rule 48`
- [ ] `C-CF-28` `constraint` The ability estimate moves without loosening what counts as correct. `src: Core features, rule 55`
- [ ] `C-CF-29` `constraint` Hearts regenerate on read, carrying the partial interval forward. `src: Core features, rule 58`
- [ ] `C-CF-30` `literal` A wrong answer in a lesson costs one heart. `src: Core features, rule 60`
- [ ] `C-CF-31` `constraint` A wrong answer in a review costs no heart. `src: Core features, rule 60`
- [ ] `C-CF-32` `constraint` Lesson progress survives running out of hearts. `src: Core features, rule 61`
- [ ] `C-CF-33` `literal` Practice restores one heart at most once per interval. `src: Core features, rule 62`
- [ ] `C-CF-34` `data` The streak is recomputed from history on read against a stored local date. `src: Core features, rule 74`
- [ ] `C-CF-35` `constraint` A timezone change does not shorten the streak. `src: Core features, rule 66`
- [ ] `C-CF-36` `constraint` The day boundary survives both daylight transitions under the declared day shift. `src: Core features, rule 67`
- [ ] `C-CF-37` `constraint` A streak freeze is consumed once per local date. `src: Core features, rule 71`
- [ ] `C-CF-38` `constraint` Streak repair restores the exact previous length. `src: Core features, rule 73`
- [ ] `C-CF-39` `literal` Experience awarded matches the pinned table for a lesson, a review, a practice, a perfect run, a first run of the day. `src: Core features, rule 76`
- [ ] `C-CF-40` `literal` The promotion zone with the demotion zone partition the board seven up, five down. `src: Core features, rule 80`
- [ ] `C-CF-41` `constraint` Cohort standings order breaks ties by the earlier earner. `src: Core features, rule 81`
- [ ] `C-CF-42` `constraint` The cohort week closes at one instant for every member, then freezes. `src: Core features, rule 82`
- [ ] `C-CF-43` `constraint` The reader's own standings row is current after earning. `src: Core features, rule 85`
- [ ] `C-CF-44` `constraint` Unit progress is never reduced by a write. `src: Core features, rule 89`
- [ ] `C-CF-45` `constraint` The session is pinned to a subject version at assembly. `src: Core features, rule 90`
- [ ] `C-CF-46` `capability` The subject graph is validated at load for acyclicity, reachability, concept order. `src: Core features, rule 87`
- [ ] `C-CF-47` `constraint` Subject content safety checks refuse a subject whose bank or solution is bad. `src: Core features, rule 92`
- [ ] `C-CF-48` `constraint` An untranslated guidebook falls back with a marker rather than staying hidden. `src: Core features, rule 91`
- [ ] `C-CF-49` `constraint` An expired token is denied on every protected route. `src: Core features, rule 3`
- [ ] `C-CF-50` `constraint` A password hash is never returned by any endpoint. `src: Core features, Auth`
- [ ] `C-CF-51` `constraint` A session start in a closed subject is refused, writing nothing. `src: Core features, rule 5`
- [ ] `C-CF-52` `capability` The accepted answer set expands from the declared grammar inside its ceiling. `src: Core features, rule 25`
- [ ] `C-CF-53` `capability` Normalization order is applied before comparison, folding case after the control characters go. `src: Core features, rule 26`
- [ ] `C-CF-54` `constraint` A typo within threshold is accepted with a note rather than silently. `src: Core features, rule 30`
- [ ] `C-CF-55` `constraint` A missing accent is accepted with a note rather than silently. `src: Core features, rule 29`
- [ ] `C-CF-56` `constraint` A near miss that is a taught word is marked incorrect. `src: Core features, rule 32`
- [ ] `C-CF-57` `capability` A free word order answer is matched as a multiset over the declared tokens. `src: Core features, rule 34`
- [ ] `C-CF-58` `constraint` A word bank holds no valid alternative answer among its distractors. `src: Core features, rule 36`
- [ ] `C-CF-59` `constraint` The word bank shuffle is stable across a reload. `src: Core features, rule 37`
- [ ] `C-CF-60` `constraint` A free text answer is never filtered by character. `src: Core features, rule 38`
- [ ] `C-CF-61` `constraint` A regrade refunds hearts without touching settled standings. `src: Core features, rule 39`
- [ ] `C-CF-62` `literal` The feed route serves the same page as the root under one title. `src: Core features, rule 94`
- [ ] `C-CF-63` `constraint` No learner count or efficacy claim appears on any public page. `src: Core features, rule 97`
- [ ] `C-CF-64` `constraint` Every internal link on a public route resolves. `src: Core features, rule 99`
- [ ] `C-CF-65` `capability` The terms page is linked from the signup form beside the privacy page in every footer. `src: Core features, rule 100`
- [ ] `C-CF-66` `literal` An unknown address answers not found with the pinned title `Error 404`. `src: Core features, rule 102`
- [ ] `C-CF-67` `capability` A mistyped subject address renders the picker page. `src: Core features, rule 103`
- [ ] `C-CF-68` `data` Page views are recorded, readable by their owner alone. `src: Core features, rule 104`
- [ ] `C-CF-69` `capability` Long form pages carry contents, a dated summary, a capped measure. `src: Core features, rule 105`
- [ ] `C-CF-70` `literal` The first view of the marketing page ships no binary inside its transfer ceiling. `src: Core features, rule 110`
- [ ] `C-CF-71` `capability` The picker scrolls with the pointer, by drag, with the arrow keys, pressing a row to enrol in place. `src: Core features`
- [ ] `C-CF-72` `capability` An answer is marked on the page with the result appearing without a page load. `src: Core features, rule 17`
- [ ] `C-CF-73` `capability` A subject page states that the subject is not open yet, offering the picker underneath. `src: Core features, rule 5`
- [ ] `C-CF-74` `constraint` No start control is offered on a subject that is not open. `src: Core features, rule 5`
- [ ] `C-CF-75` `capability` The failed address reads on the not-found page beside a link back to the subject index. `src: Core features, rule 102`
- [ ] `C-CF-76` `capability` A mistyped subject address reads its own distinct page carrying the picker. `src: Core features, rule 103`
- [ ] `C-CF-77` `capability` The site-language list writes each language in that language's own name. `src: Core features, rule 98`
- [ ] `C-CF-78` `capability` The preference panel records a refused cookie category that survives a reload. `src: Core features, rule 101`
- [ ] `C-CF-79` `capability` The english subject page reads a Spanish prompt beside an English answer field. `src: Core features, rule 8`
- [ ] `C-CF-80` `capability` Both sample exercises are answerable before signup from the same browser. `src: Core features, rule 7`
- [ ] `C-CF-81` `constraint` No percentage, mastery figure or draining bar appears on the profile. `src: Core features, rule 52`
- [ ] `C-CF-82` `capability` The path after a long absence offers a normal length session rather than a backlog count. `src: Core features, rule 48`
- [ ] `C-CF-83` `constraint` A subject mark is a rounded square carrying a short code rather than a national flag. `src: Core features`
- [ ] `C-CF-84` `constraint` The memory model is shown as strong skills rather than as a number. `src: Core features, rule 52`
- [ ] `C-CF-85` `constraint` A held-back account is never publicly marked, staying in its cohort mid-week. `src: Core features, rule 86`
- [ ] `C-CF-86` `constraint` The editorial route uses the same tokens as every other route. `src: Core features, rule 106`
- [ ] `C-CF-87` `constraint` The two paid tier pages carry no price. `src: Core features, rule 107`

## C-UF User flow

- [ ] `C-UF-01` `capability` An empty history renders its own empty state. `src: User flow, States`
- [ ] `C-UF-02` `literal` Learner routes resolve at their pinned addresses beside the public ones. `src: User flow`
- [ ] `C-UF-03` `capability` Pressing the primary action carries a visitor through signup onto the learner path. `src: User flow, journey 1`
- [ ] `C-UF-04` `capability` Walking the path to the next unit through twelve exercises ends on a summary. `src: User flow, journey 2`
- [ ] `C-UF-05` `capability` The session summary reads one experience total beside one streak after a finished lesson. `src: User flow, journey 3`
- [ ] `C-UF-06` `capability` Reloading the session summary reads that same experience total beside that same streak. `src: User flow, journey 3`
- [ ] `C-UF-07` `capability` The profile reads a weekly total before a session is finished. `src: User flow, journey 2`
- [ ] `C-UF-08` `capability` The profile total moves by one award after one finished lesson rather than two. `src: User flow, journey 2`
- [ ] `C-UF-09` `capability` The learner path shows only the signed-in account's own subject. `src: User flow, journey 4`
- [ ] `C-UF-10` `capability` Opening a learner route when signed out lands on the sign-in page with the destination remembered. `src: User flow`
- [ ] `C-UF-11` `capability` Signing in lands on the remembered destination rather than the default path. `src: User flow`
- [ ] `C-UF-12` `capability` Returning after closing the tab offers the resumable session rather than resuming silently. `src: User flow, States`
- [ ] `C-UF-13` `capability` The settings page reads the timezone, the day shift, the daily goal. `src: User flow`
- [ ] `C-UF-14` `capability` Changing the timezone leaves the streak count unchanged on the profile. `src: User flow, journey 6`
- [ ] `C-UF-15` `capability` The history on the new account reads the sample attempts already recorded. `src: User flow, journey 1`
- [ ] `C-UF-16` `capability` An error arrives as a panel over a surface that stays usable. `src: User flow, States`

## C-UX UI/UX notes

- [ ] `C-UX-01` `capability` Body text meets the contrast bar against its own background. `src: UI/UX notes`
- [ ] `C-UX-02` `capability` A narrow viewport has no sideways overflow, keeping every navigation target reachable. `src: UI/UX notes`
- [ ] `C-UX-03` `literal` Pinned session copy appears verbatim across the claims, the hero, the platforms band, the footer. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A wrong answer carries a cross shape beside a word rather than colour alone. `src: Front-end specification`
- [ ] `C-UX-05` `literal` A transposed letter reads the typo note beside the accepted answer. `src: UI/UX notes`
- [ ] `C-UX-06` `literal` A missing accent reads the accent note in the player. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Each page leads with one primary action, visually distinct from every secondary one. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Type, depth, density, the control states all follow one visual system across every route. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The palette is carried by role with a semantic alias naming each entry. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Movement overshoots then settles, at one constant fraction of the travel. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` The loading indicator is three dots breathing at three phases of one animation. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` A request for reduced motion resolves the spring to a fade, holding the hero at its first frame. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Every text run carries its own language attribute across the interface. `src: Core features`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Public routes declare unique preview titles beside a description, with the preview image resolving. `src: Technical requirements`
- [ ] `C-TR-02` `contract` No credential or token is referenced in anything the browser downloads from the application. `src: Technical requirements`
- [ ] `C-TR-03` `contract` Request logging never carries a password, a token or an email address. `src: Technical requirements`
- [ ] `C-TR-04` `contract` Learner routes resolve as server-rendered markup on first paint. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Attempt rows persist, surviving a reread as the source of every derived number. `src: Data model, attempts`
- [ ] `C-DM-02` `literal` The cohort holds twelve seeded members at `Bronze` inside the capacity ceiling. `src: Data model, Seed data`
- [ ] `C-DM-03` `data` Seeding is idempotent across a restart for accounts, subjects, units, exercises. `src: Data model, Seed data`
- [ ] `C-DM-04` `data` Attempt rows are unique on the session with the presented index. `src: Data model, attempts`
- [ ] `C-DM-05` `data` A trace row is unique on the account with the concept, rebuildable from the attempt log. `src: Data model, traces`
- [ ] `C-DM-06` `data` The session row carries a reconcile mark written once, so a repeat cannot double count. `src: Data model, sessions`
- [ ] `C-DM-07` `data` The streak row holds the last completed day as a date recomputed on read. `src: Data model, streaks`
- [ ] `C-DM-08` `data` The hearts row holds a refill mark that a read leaves in place. `src: Data model, hearts`
- [ ] `C-DM-09` `data` Unit states are keyed by unit identity rather than by position, never reduced by a write. `src: Data model, unit_states`
- [ ] `C-DM-10` `data` The courses table carries forty-two subject rows in picker order. `src: Data model, courses`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The hero opens the page with two actions beside the scene, ahead of four claim sections in strict alternation. `src: Core features`
- [ ] `C-FE-02` `ui` The path chrome shows the streak flame, the experience gem, the hearts, the league trophy. `src: Front-end specification, The path`
- [ ] `C-FE-03` `ui` The history timeline reads one entry for that lesson, newest first. `src: Front-end specification, The history timeline`
- [ ] `C-FE-04` `ui` Heart exhaustion on a restricted account offers practice or waiting with no price. `src: Core features`
- [ ] `C-FE-05` `ui` The path states the time to the next heart when the hearts are gone. `src: Core features`
- [ ] `C-FE-06` `ui` The hearts readout beside the path matches the count in the exercise player. `src: Core features`
- [ ] `C-FE-07` `ui` Finishing a practice session moves the heart count by one on the page. `src: Core features`
- [ ] `C-FE-08` `ui` The canonical answer is shown under a wrong answer in the player. `src: Core features`
- [ ] `C-FE-09` `ui` The path carries the freeze message after a missed day. `src: Core features`
- [ ] `C-FE-10` `ui` The history marks a missed day as a freeze rather than as a gap. `src: Core features`
- [ ] `C-FE-11` `ui` The league page reads twelve rows with a promotion zone across the top seven. `src: User flow`
- [ ] `C-FE-12` `ui` The league page reads a demotion zone across the bottom five rows. `src: User flow`
- [ ] `C-FE-13` `ui` The league deadline reads converted into the member's own timezone. `src: Core features`
- [ ] `C-FE-14` `ui` Tapping a placed word back out returns the word to its original place in the bank. `src: Core features`
- [ ] `C-FE-15` `ui` The not-found page carries the product's own character in a puzzled pose. `src: Core features`
- [ ] `C-FE-16` `ui` The footer's six groups carry entries that open as real pages. `src: Core features`
- [ ] `C-FE-17` `ui` The profile reads strong skills, skills needing practice, what is due today. `src: Core features`
- [ ] `C-FE-18` `ui` The exercise player fills the screen with one exercise beside a progress element. `src: Front-end specification, The exercise player`
- [ ] `C-FE-19` `ui` The session summary names what the lesson earned beside the streak. `src: Core features`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No address outside the application is referenced anywhere in the build. `src: Constraints`
- [ ] `C-CN-02` `constraint` Audio exercise types are suppressed, so subjects stay completable. `src: Constraints`
- [ ] `C-CN-03` `constraint` No friend graph, no learner-written text, no feature assignment exists. `src: Constraints`
- [ ] `C-CN-04` `constraint` Audio playback, speech recognition, pronunciation are all absent, so the audio exercise types stay suppressed. `src: Constraints`
- [ ] `C-CN-05` `constraint` No third-party script or analytics vendor is referenced from outside the application at run time. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The health endpoint returns ok once the app is ready behind its production server. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The user readme carries every seeded login so a reader can sign in. `src: Deployment contract`
- [ ] `C-DC-03` `contract` List endpoints return top level arrays. `src: Deployment contract, API shapes`
- [ ] `C-DC-04` `contract` An invalid call is a client error naming the reason. `src: Deployment contract, API shapes`
- [ ] `C-DC-05` `contract` Every route resolves at the public address the environment pins. `src: Deployment contract`
- [ ] `C-DC-06` `contract` The http api is served on the same origin under its prefix, where health returns ok. `src: Deployment contract`
- [ ] `C-DC-07` `contract` The server keeps running after the session ends, so the health endpoint still returns ok. `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server binds every address rather than loopback, so the health endpoint returns ok from outside. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The app starts from the environment image with no manual steps before the health endpoint returns ok. `src: Deployment contract`
- [ ] `C-DC-10` `contract` Reserved screenshot directories exist at the app root where the health endpoint returns ok. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | User roles | `C-RL-01` |
| `english` | Core features, rule 5 | `C-CF-04` |
| `chess` | Core features, rule 5 | `C-CF-04` |
| `math` | Core features, rule 5 | `C-CF-04` |
| `correct` | Core features, rule 14 | `C-CF-13` |
| `correct_with_note` | Core features, rule 14 | `C-CF-13` |
| `incorrect` | Core features, rule 14 | `C-CF-13` |
| `skipped` | Core features, rule 14 | `C-CF-13` |
| `0.90` | Core features, rule 46 | `C-CF-25` |
| `Bronze` | Data model, Seed data | `C-DM-02` |
| `Error 404` | Core features, rule 102 | `C-CF-66` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the human floor per exercise type | `C-CF-21` |
| the due-load threshold below which new concepts are introduced | `C-CF-27` |
| the earning-rate ceiling above which a standing is held back | `C-CF-85` |
| the exact geometry of the generated character set | `C-UX-08` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 1 |
| User roles | 2 | 5 |
| Core features | 23 | 87 |
| User flow | 4 | 16 |
| UI/UX notes | 8 | 13 |
| Technical requirements | 4 | 4 |
| Data model | 10 | 10 |
| Front-end specification | 2 | 19 |
| Constraints | 5 | 5 |
| Deployment contract | 10 | 10 |

