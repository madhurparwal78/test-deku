# Checklist: Veyra Fault Triage

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 126
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` A pilot logs a completed survey flight with fault zones. `src: Overview para 1`
- [ ] `C-OV-02` `capability` A confirmed fault emails the owner of the site. `src: Overview para 1`
- [ ] `C-OV-03` `capability` A confirmed fault leaves the triage queue. `src: Overview para 1`
- [ ] `C-OV-04` `constraint` Site owners never sign in to the product. `src: Overview para 3`

## C-RL User roles

- [ ] `C-RL-01` `role` An administrator creates a site. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An administrator creates a staff account. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A pilot logs a survey flight with fault zones. `src: User roles table row 2`
- [ ] `C-RL-04` `role` A pilot claiming a fault is denied at the API. `src: User roles table row 2`
- [ ] `C-RL-05` `role` A pilot creating a site is denied at the API. `src: User roles table row 2`
- [ ] `C-RL-06` `role` An engineer claims an open fault. `src: User roles table row 3`
- [ ] `C-RL-07` `role` An engineer deciding a fault held by another engineer is denied at the API. `src: User roles table row 3`
- [ ] `C-RL-08` `role` An engineer creating a site is denied at the API. `src: User roles table row 3`
- [ ] `C-RL-09` `role` An engineer creating a staff account is denied at the API. `src: User roles table row 3`
- [ ] `C-RL-10` `contract` Authorization is enforced server side on every mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-11` `constraint` The product offers no sign up. `src: User roles para 3`
- [ ] `C-RL-12` `literal` The seeded accounts are `administrator@example.com`, `pilot@example.com`, `engineer@example.com`, `engineer2@example.com`. `src: User roles para 3`

## C-CF Core features

- [ ] `C-CF-01` `capability` Staff sign in with an email address plus a password at `/login`. `src: Core features 1 rule 1`
- [ ] `C-CF-02` `ui` A wrong password shows the message beginning `That email`. `src: Core features 1 rule 1`
- [ ] `C-CF-03` `contract` A wrong password issues no token. `src: Core features 1 rule 1`
- [ ] `C-CF-04` `contract` A deactivated account is refused at sign in. `src: Core features 1 rule 2`
- [ ] `C-CF-05` `ui` The sign in card says `Accounts are created by your administrator.` `src: Core features 1 rule 3`
- [ ] `C-CF-06` `literal` A site asset class is one of `wind_turbines`, `solar_farms`, `power_lines`, `substations`. `src: Core features 2 rule 1`
- [ ] `C-CF-07` `constraint` A site name is unique. `src: Core features 2 rule 2`
- [ ] `C-CF-08` `constraint` An inactive site accepts no new survey. `src: Core features 2 rule 3`
- [ ] `C-CF-09` `constraint` A survey with no fault zone is rejected as invalid. `src: Core features 3 rule 3`
- [ ] `C-CF-10` `constraint` A survey with more than 20 fault zones is rejected as invalid. `src: Core features 3 rule 3`
- [ ] `C-CF-11` `literal` A fault zone kind is one of `crack`, `deformation`, `corrosion`, `vegetation_encroachment`. `src: Core features 3 rule 2`
- [ ] `C-CF-12` `constraint` A fault zone ranked above 4 is rejected as invalid. `src: Core features 3 rule 2`
- [ ] `C-CF-13` `constraint` A survey flown-at time in the future is rejected as invalid. `src: Core features 3 rule 3`
- [ ] `C-CF-14` `constraint` A survey coverage above 100 square kilometres is rejected as invalid. `src: Core features 3 rule 3`
- [ ] `C-CF-15` `data` A rejected survey leaves no survey row. `src: Core features 3 rule 4`
- [ ] `C-CF-16` `data` A rejected survey leaves no fault row. `src: Core features 3 rule 4`
- [ ] `C-CF-17` `data` Every fault created by a survey starts `open`. `src: Core features 3 rule 5`
- [ ] `C-CF-18` `ui` The survey page shows a message carrying the real count of faults added. `src: Core features 3 rule 5`
- [ ] `C-CF-19` `capability` The queue lists every open fault. `src: Core features 4 rule 1`
- [ ] `C-CF-20` `capability` The queue orders faults by rank from 4 down to 1. `src: Core features 4 rule 1`
- [ ] `C-CF-21` `capability` The queue orders faults of equal rank by measured deformation from largest to smallest. `src: Core features 4 rule 1`
- [ ] `C-CF-22` `capability` The queue orders faults of equal rank with equal deformation by flown-at time from oldest to newest. `src: Core features 4 rule 1`
- [ ] `C-CF-23` `ui` A queue line shows the name of the engineer holding a claimed fault. `src: Core features 4 rule 2`
- [ ] `C-CF-24` `capability` The queue narrows by asset class. `src: Core features 4 rule 3`
- [ ] `C-CF-25` `ui` An empty queue shows `The queue is clear.` `src: Core features 4 rule 4`
- [ ] `C-CF-26` `capability` An engineer claiming an open fault sets the fault to `claimed`. `src: Core features 5 rule 1`
- [ ] `C-CF-27` `data` A claim writes one `claimed` entry to the fault history. `src: Core features 5 rule 1`
- [ ] `C-CF-28` `contract` Two simultaneous claims on one open fault produce exactly one accepted claim. `src: Core features 5 rule 2`
- [ ] `C-CF-29` `contract` A losing simultaneous claim is refused as a conflict naming the holder. `src: Core features 5 rule 2`
- [ ] `C-CF-30` `data` Simultaneous claims leave exactly one `claimed` history entry. `src: Core features 5 rule 2`
- [ ] `C-CF-31` `constraint` Claiming a decided fault is refused as a conflict. `src: Core features 5 rule 3`
- [ ] `C-CF-32` `capability` A released fault returns to `open` with no claimant. `src: Core features 5 rule 4`
- [ ] `C-CF-33` `role` Only the engineer holding a claimed fault confirms the fault. `src: Core features 6 rule 1`
- [ ] `C-CF-34` `ui` The confirm step names the owner email before sending. `src: Core features 6 rule 2`
- [ ] `C-CF-35` `capability` Confirming a claimed fault sets the fault to `confirmed`. `src: Core features 6 rule 2`
- [ ] `C-CF-36` `constraint` A dismissal reason under 10 characters is rejected as invalid. `src: Core features 6 rule 3`
- [ ] `C-CF-37` `data` A dismissed fault stores the dismissal reason. `src: Core features 6 rule 3`
- [ ] `C-CF-38` `capability` A decided fault leaves the queue for every viewer. `src: Core features 6 rule 4`
- [ ] `C-CF-39` `contract` Confirming a fault sends exactly one email to the site owner email. `src: Core features 7 rule 1`
- [ ] `C-CF-40` `literal` The confirmation email subject begins with `Confirmed fault at`. `src: Core features 7 rule 2`
- [ ] `C-CF-41` `constraint` Dismissing a fault sends no email. `src: Core features 7 rule 4`
- [ ] `C-CF-42` `constraint` Releasing a fault sends no email. `src: Core features 7 rule 4`
- [ ] `C-CF-43` `data` Every fault decision writes an entry to the fault history. `src: Core features 6 rule 4`
- [ ] `C-CF-44` `capability` The overview counts faults per asset class by status. `src: Core features 8 rule 1`
- [ ] `C-CF-45` `data` The all-sites overview figure equals the sum of the four asset classes. `src: Core features 8 rule 2`
- [ ] `C-CF-46` `ui` The landing page shows the product name as large outlined lettering over a pale wash. `src: Core features 9 rule 1`
- [ ] `C-CF-47` `ui` The landing page shows the line `Autonomous LIDAR inspection systems.` `src: Core features 9 rule 1`
- [ ] `C-CF-48` `ui` The capabilities selector switches between `Scan`, `Connection`, `Compactness`. `src: Core features 9 rule 2`
- [ ] `C-CF-49` `ui` The landing page ends in the primary action `Sign in to the console`. `src: Core features 9 rule 3`
- [ ] `C-CF-50` `capability` A console page view is recorded with the route. `src: Core features 10 rule 1`
- [ ] `C-CF-51` `capability` The administrator reads the page view count per route. `src: Core features 10 rule 2`

## C-UF User flow

- [ ] `C-UF-01` `capability` A signed-out visit to a console route redirects to `/login`. `src: User flow Entry and redirects`
- [ ] `C-UF-02` `capability` A successful sign in returns to the console route first requested. `src: User flow Entry and redirects`
- [ ] `C-UF-03` `ui` A role opening a route beyond its role sees the heading `Not permitted`. `src: User flow Entry and redirects`
- [ ] `C-UF-04` `ui` Every console page carries a breadcrumb trail. `src: User flow Entry and redirects`
- [ ] `C-UF-05` `capability` The engineer confirms the seeded crack at `Harrow Ridge Wind Farm` from the queue. `src: User flow Journey 1`
- [ ] `C-UF-06` `ui` A toast confirms the email after the engineer confirms a fault. `src: User flow Journey 1`
- [ ] `C-UF-07` `ui` A losing claimant sees the name of the engineer holding the fault. `src: User flow Journey 2`
- [ ] `C-UF-08` `capability` The pilot logs a survey on `Saltmarsh Solar Array` from `/console/surveys/new`. `src: User flow Journey 3`
- [ ] `C-UF-09` `ui` Every list has an empty state saying why the list is empty. `src: User flow States`
- [ ] `C-UF-10` `ui` A form error sits under the field the error belongs to. `src: User flow States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Fault rank is carried by a numeral, never by hue alone. `src: UI/UX notes Colour`
- [ ] `C-UX-02` `ui` Primary text uses one deep cool neutral ink. `src: UI/UX notes Colour`
- [ ] `C-UX-03` `ui` Links use a mid, muted cyan. `src: UI/UX notes Colour`
- [ ] `C-UX-04` `ui` Confirmed status dots use a light, muted teal. `src: UI/UX notes Colour`
- [ ] `C-UX-05` `ui` Type is set in `Switzer`. `src: UI/UX notes Type`
- [ ] `C-UX-06` `ui` Bracketed labels use `Proto Mono`. `src: UI/UX notes Type`
- [ ] `C-UX-07` `ui` Icons are drawn in the page from lines. `src: UI/UX notes Iconography`
- [ ] `C-UX-08` `ui` The fault page carries a half-dome gauge whose notch marks the fault rank. `src: UI/UX notes Iconography`
- [ ] `C-UX-09` `ui` Every console page has a top bar with a UTC clock. `src: UI/UX notes Global chrome`
- [ ] `C-UX-10` `ui` The menu opens a full-height panel from the right edge. `src: UI/UX notes Global chrome`
- [ ] `C-UX-11` `ui` Motion is calm with no overshoot. `src: UI/UX notes Motion`
- [ ] `C-UX-12` `ui` Reduced motion removes the blurs, wipes, rises, pulses. `src: UI/UX notes Motion`
- [ ] `C-UX-13` `ui` Each page leads with one primary action distinct from every secondary action. `src: UI/UX notes Components`
- [ ] `C-UX-14` `ui` Every journey works with keyboard navigation alone. `src: UI/UX notes Accessibility`
- [ ] `C-UX-15` `ui` Body text meets WCAG AA contrast. `src: UI/UX notes Accessibility`
- [ ] `C-UX-16` `ui` A narrow viewport shows the queue as a stack of cards. `src: UI/UX notes Responsive`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Data is stored in the PostgreSQL database at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` Email is sent through Mailpit. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` `POST /api/auth/login` returns `access_token`. `src: Technical requirements para 3`
- [ ] `C-TR-04` `contract` Every endpoint except the health route requires a bearer token. `src: Technical requirements para 3`
- [ ] `C-TR-05` `contract` The site declares a favicon with a `rel="icon"` link that resolves. `src: Technical requirements para 4`
- [ ] `C-TR-06` `contract` Every response carries a `Strict-Transport-Security` header. `src: Technical requirements para 5`
- [ ] `C-TR-07` `contract` Every response carries `X-Content-Type-Options: nosniff`. `src: Technical requirements para 5`
- [ ] `C-TR-08` `constraint` The seeded password appears in no file the browser downloads. `src: Technical requirements para 6`
- [ ] `C-TR-09` `constraint` The database connection string appears in no file the browser downloads. `src: Technical requirements para 6`
- [ ] `C-TR-10` `contract` `GET /api/health` returns `200`. `src: Technical requirements para 8`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model para 2`
- [ ] `C-DM-02` `contract` The seeded accounts are written to `/app/USER_README.md`. `src: Data model para 2`
- [ ] `C-DM-03` `data` A staff email is unique. `src: Data model staff`
- [ ] `C-DM-04` `data` A fault status is one of `open`, `claimed`, `confirmed`, `dismissed`. `src: Data model faults`
- [ ] `C-DM-05` `data` A fault holds at most one claimant at any time. `src: Data model invariants bullet 1`
- [ ] `C-DM-06` `data` A claimed fault records `claimed_by`. `src: Data model invariants bullet 3`
- [ ] `C-DM-07` `data` A decided fault records `decided_by`. `src: Data model invariants bullet 3`
- [ ] `C-DM-08` `data` A fault history entry is never edited after being written. `src: Data model fault_events`
- [ ] `C-DM-09` `data` A survey with the survey faults is written together or not at all. `src: Data model invariants bullet 4`
- [ ] `C-DM-10` `data` The seed carries four sites, one per asset class. `src: Data model Seed data`
- [ ] `C-DM-11` `data` The seed carries three open faults on `Harrow Ridge Wind Farm`. `src: Data model Seed data`
- [ ] `C-DM-12` `data` Seeding on restart duplicates no seeded row. `src: Data model Seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Site owners have no account. `src: Constraints bullet 2`
- [ ] `C-CN-02` `constraint` The product offers no password reset. `src: Constraints bullet 3`
- [ ] `C-CN-03` `constraint` The product offers no single sign-on. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The product offers no attachments on a fault. `src: Constraints bullet 8`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The HTTP API is served under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-03` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-04` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes`
- [ ] `C-DC-05` `contract` An invalid call is rejected as a client error, never a server error. `src: Deployment contract API shapes`
- [ ] `C-DC-06` `constraint` A confirmation email recorded without delivery through Mailpit is a contract violation. `src: Deployment contract No mocks`
- [ ] `C-DC-07` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `administrator@example.com` | seeded administrator email | C-RL-12 | User roles para 3 |
| `pilot@example.com` | seeded pilot email | C-RL-12 | User roles para 3 |
| `engineer@example.com` | seeded engineer email | C-RL-12 | User roles para 3 |
| `engineer2@example.com` | second seeded engineer email | C-RL-12 | User roles para 3 |
| `wind_turbines` | asset class | C-CF-06 | Core features 2 rule 1 |
| `solar_farms` | asset class | C-CF-06 | Core features 2 rule 1 |
| `power_lines` | asset class | C-CF-06 | Core features 2 rule 1 |
| `substations` | asset class | C-CF-06 | Core features 2 rule 1 |
| `crack` | fault kind | C-CF-11 | Core features 3 rule 2 |
| `deformation` | fault kind | C-CF-11 | Core features 3 rule 2 |
| `corrosion` | fault kind | C-CF-11 | Core features 3 rule 2 |
| `vegetation_encroachment` | fault kind | C-CF-11 | Core features 3 rule 2 |
| `Confirmed fault at` | confirmation email subject prefix | C-CF-40 | Core features 7 rule 2 |
| `deku-demo-pw-2026` | password for every seeded account | C-DM-01 | Data model para 2 |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 4 | 4 |
| User roles | 12 | 12 |
| Core features | 51 | 51 |
| User flow | 10 | 10 |
| UI and UX notes | 16 | 16 |
| Technical requirements | 10 | 10 |
| Data model | 12 | 12 |
| Constraints | 4 | 4 |
| Deployment contract | 7 | 7 |
