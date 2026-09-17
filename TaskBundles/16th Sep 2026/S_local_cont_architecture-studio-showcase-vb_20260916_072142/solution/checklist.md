# Checklist: Norrgaard

Items: 131
Unpinned values flagged: 4
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

The coverage target, restated from `instruction.md` alone. One row per core ask,
each cited back to the section of the brief that states the obligation.

## C-OV Overview

- [ ] `C-OV-01` `capability` The site reads as one continuous surface rather than as a set of separate pages. `src: Overview`
- [ ] `C-OV-02` `constraint` No basket, no price, no transaction appears anywhere on the site. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `literal` Every seeded account signs in with the pinned password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-02` `role` A signup always produces a reader role, whatever the request body asks for. `src: Core features, rule 4`
- [ ] `C-RL-03` `role` A reader cannot publish or edit any content. `src: User roles`
- [ ] `C-RL-04` `role` A reader cannot read a draft project by any route. `src: User roles`
- [ ] `C-RL-05` `role` A reader cannot read another account's enquiry. `src: User roles`
- [ ] `C-RL-06` `role` An unauthenticated studio route is denied, redirecting the page to sign in. `src: User flow`
- [ ] `C-RL-07` `role` No publish control appears on any route a reader can open. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `constraint` A signup with an existing email is refused, writing no second account row. `src: Core features, rule 1`
- [ ] `C-CF-02` `constraint` An expired token is denied on every protected route. `src: Core features, rule 3`
- [ ] `C-CF-03` `constraint` A password hash is never returned by any endpoint. `src: Core features, Auth`
- [ ] `C-CF-04` `capability` The project list returns published projects in order. `src: Core features, rule 38`
- [ ] `C-CF-05` `literal` A project area renders with a thousands separator: `58,079 m2`. `src: Core features, rule 5`
- [ ] `C-CF-06` `capability` A project detail carries its body beside its gallery image rows. `src: Core features, rule 43`
- [ ] `C-CF-07` `data` Team, offices, awards, publications are all ordered collections of the content model. `src: Core features, rule 6`
- [ ] `C-CF-08` `literal` The legal route carries eight numbered chapters. `src: Core features, rule 52`
- [ ] `C-CF-09` `data` Gallery photographs feed the arc in order from the content model. `src: Core features, rule 36`
- [ ] `C-CF-10` `data` The arc settings record is one editable record holding every arc parameter. `src: Core features, rule 9`
- [ ] `C-CF-11` `capability` An editor creates a project from the studio surface with no code change. `src: Core features, rule 8`
- [ ] `C-CF-12` `data` An image reference carries alt text, a ratio, a seed rather than a file path. `src: Core features, rule 7`
- [ ] `C-CF-13` `constraint` A draft project is absent from every public list. `src: Core features, rule 10`
- [ ] `C-CF-14` `constraint` A draft project address answers not found to a visitor rather than refusing. `src: Core features, rule 10`
- [ ] `C-CF-15` `constraint` A draft object is not publicly readable from the bucket. `src: Core features, rule 11`
- [ ] `C-CF-16` `constraint` A published cover object is readable from the bucket. `src: Core features, rule 11`
- [ ] `C-CF-17` `literal` Cover bytes are uploaded to the bucket at the key scheme `projects/{project_id}/{sha256_of_bytes}.png`. `src: Core features, rule 14`
- [ ] `C-CF-18` `constraint` Regenerating an image from one seed writes no second object. `src: Core features, rule 16`
- [ ] `C-CF-19` `capability` Publishing flips the flag, recording when the flip happened. `src: Core features, rule 12`
- [ ] `C-CF-20` `constraint` Unpublishing returns the project, with every object of that project, to invisible. `src: Core features, rule 12`
- [ ] `C-CF-21` `literal` An enquiry is stored with a unique reference of twelve lowercase characters. `src: Core features, rule 46`
- [ ] `C-CF-22` `constraint` A duplicate enquiry submission creates one row, returning the first reference. `src: Core features, rule 49`
- [ ] `C-CF-23` `data` Page views are recorded with their route, readable by an editor alone. `src: Core features, rule 69`
- [ ] `C-CF-24` `capability` An editor reads every enquiry received, newest first. `src: Core features, rule 51`
- [ ] `C-CF-25` `constraint` A public list query cannot ask for unpublished rows by any parameter. `src: Core features, rule 13`
- [ ] `C-CF-26` `constraint` An invalid enquiry is refused inline, naming the field at fault. `src: Core features, rule 47`
- [ ] `C-CF-27` `constraint` A filled decoy field marks an enquiry invalid, with nothing written. `src: Core features, rule 48`
- [ ] `C-CF-28` `literal` Repeated enquiries from one origin beyond `3` inside `3600` seconds are refused. `src: Core features, rule 48`
- [ ] `C-CF-29` `capability` The enquiry confirmation address shows its reference. `src: Core features, rule 46`
- [ ] `C-CF-30` `literal` An unknown address answers not found under an honest title. `src: Core features, rule 68`
- [ ] `C-CF-31` `constraint` Every internal link on a public route resolves. `src: Core features, rule 61`
- [ ] `C-CF-32` `capability` The legal route is linked from the signup form as the terms page. `src: Core features, rule 55`
- [ ] `C-CF-33` `literal` The project index opens in `List` mode. `src: Core features, rule 39`
- [ ] `C-CF-34` `capability` A chosen view mode survives a move to another route, then back. `src: Core features, rule 40`
- [ ] `C-CF-35` `capability` The navigation marks the active route, re-marking on every route change. `src: Core features, rule 63`
- [ ] `C-CF-36` `constraint` A reduced motion request resolves every reveal to its end state. `src: UI/UX notes`
- [ ] `C-CF-37` `capability` Legal chapters expand from the keyboard, exposing whether each is open. `src: Core features, rule 53`
- [ ] `C-CF-38` `capability` Each heading past the founding block arrives a line at a time on being scrolled into view. `src: Core features, rule 27`
- [ ] `C-CF-39` `capability` The radial figure behind the statement fades in as the statement is reached. `src: Core features, rule 22`
- [ ] `C-CF-40` `capability` The fanned photographs rotate, then settle, over the black arc section under scroll. `src: Core features, rule 24`
- [ ] `C-CF-41` `capability` The three statistics read over black, each a numeral beside a serif label, before the office list closes the route. `src: Core features, rule 25`
- [ ] `C-CF-42` `constraint` Neither draft project appears in any of the three index modes. `src: Core features, rule 10`
- [ ] `C-CF-43` `constraint` A draft address renders the not-found page rather than a refusal. `src: Core features, rule 10`
- [ ] `C-CF-44` `capability` Moving to another route, then back, reads the remembered arrangement rather than the default. `src: Core features, rule 40`
- [ ] `C-CF-45` `capability` The eighth legal chapter carries an illustrative-content statement. `src: Core features, rule 54`
- [ ] `C-CF-46` `literal` The not-found page carries a link back to the home page beside a line in the studio's voice. `src: Core features, rule 67`
- [ ] `C-CF-47` `capability` A reveal scrolled half way into its block reads half done. `src: Core features, rule 29`
- [ ] `C-CF-48` `capability` Scrolling back up drops the lines back below their boxes rather than replaying. `src: Core features, rule 29`
- [ ] `C-CF-49` `capability` The navigation stays legible on crossing from the white hero into the black section. `src: Core features, rule 57`
- [ ] `C-CF-50` `capability` Every footer entry that is a link opens a real page. `src: Core features, rule 59`
- [ ] `C-CF-51` `constraint` The seven media entries are text rather than links to another site. `src: Core features, rule 59`
- [ ] `C-CF-52` `literal` The contact route reads three contact groups set large in the serif. `src: Core features, rule 66`
- [ ] `C-CF-53` `literal` The award statements close the about route. `src: Core features, rule 64`
- [ ] `C-CF-54` `capability` The picture layer meets the layout above with no visible seam. `src: Core features, rule 32`

## C-UF User flow

- [ ] `C-UF-01` `capability` An empty enquiry list renders its own empty state. `src: User flow, States`
- [ ] `C-UF-02` `literal` Public routes resolve at their pinned addresses. `src: User flow`
- [ ] `C-UF-03` `capability` Pressing `Visit` on a project opens that building's own route. `src: User flow, journey 3`
- [ ] `C-UF-04` `capability` A sent enquiry lands on a confirmation address showing its reference. `src: User flow, journey 4`
- [ ] `C-UF-05` `capability` Opening the studio route signed out lands on the sign-in page with the destination remembered. `src: User flow`
- [ ] `C-UF-06` `capability` Signing in as an editor lands on the remembered destination. `src: User flow`
- [ ] `C-UF-07` `capability` The studio content index opens for a signed-in editor. `src: User flow, journey 6`
- [ ] `C-UF-08` `capability` A published draft appears in the project index straight afterwards. `src: User flow, journey 6`
- [ ] `C-UF-09` `capability` An error is shown in place on the surface the visitor was already on. `src: User flow, States`
- [ ] `C-UF-10` `capability` An unpublished project slug answers not found to anybody but an editor. `src: User flow`
- [ ] `C-UF-11` `capability` A reader cannot open the studio content surface, being refused rather than redirected. `src: User flow`

## C-UX UI/UX notes

- [ ] `C-UX-01` `capability` Body text meets the contrast bar against its own background. `src: UI/UX notes`
- [ ] `C-UX-02` `capability` A narrow viewport has no sideways overflow on any public route. `src: UI/UX notes`
- [ ] `C-UX-03` `capability` Every generated image carries alternative text describing what the image shows. `src: UI/UX notes`
- [ ] `C-UX-04` `literal` Pinned interface copy appears verbatim across the navigation, the footer, the statements. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The palette holds only neutrals, with the grey staying secondary. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Two families carry the whole site: the serif at display sizes, the sans for interface. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Movement is one house character everywhere rather than a different feel per surface. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Text arrives a line at a time rather than a block at a time. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A reduced-motion request leaves the site usable rather than stripped. `src: Core features`
- [ ] `C-UX-10` `ui` A visible focus ring follows the keyboard across every control. `src: Core features`
- [ ] `C-UX-11` `ui` The narrow arrangement stacks into single columns carrying the same content. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The fanned arc re-spreads smoothly across a window drag rather than jumping. `src: Core features`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Public routes declare unique titles, each beside its own description, no two sharing either. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Generated cover bytes are uploaded to the MinIO bucket, leaving the content model in PostgreSQL. `src: Technical requirements`
- [ ] `C-TR-03` `contract` Request logging never carries a password, a token or an email address. `src: Technical requirements`
- [ ] `C-TR-04` `contract` No credential is referenced in anything the browser downloads from the application. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` An image row digest matches the stored object bytes. `src: Data model, Invariants`
- [ ] `C-DM-02` `data` Enquiry rows persist, surviving a reread. `src: Data model, enquiries`
- [ ] `C-DM-03` `data` Seeding is idempotent across a restart for accounts, projects, images, collections alike. `src: Data model, Seed data`
- [ ] `C-DM-04` `data` Project images are unique on the project with the kind, then the order. `src: Data model, project_images`
- [ ] `C-DM-05` `data` Seeding across a restart fills twelve tables whose timestamps are all UTC. `src: Data model`
- [ ] `C-DM-06` `literal` The readme carries the seeded login password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-07` `data` An existing account email is unique, so a second signup writes no row. `src: Data model, accounts`
- [ ] `C-DM-08` `data` A project slug is unique across the projects table. `src: Data model, projects`
- [ ] `C-DM-09` `data` An enquiry reference is unique across the enquiries table. `src: Data model, Invariants`
- [ ] `C-DM-10` `data` The published flag changes only through the two publish actions. `src: Data model, Invariants`
- [ ] `C-DM-11` `data` A refused enquiry writes no row at all. `src: Data model, Invariants`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The hero render fills the first screen with the wordmark set bottom-left in the display serif. `src: Core features`
- [ ] `C-FE-02` `ui` The enquiry modal opens over the current route from the footer action. `src: Core features`
- [ ] `C-FE-03` `ui` An enquiry field needing attention carries the faint tint beside its own name. `src: UI/UX notes`
- [ ] `C-FE-04` `ui` An email address with no at-sign carries the same treatment as an empty message. `src: Core features`
- [ ] `C-FE-05` `ui` The index reads as a single vertical column with the caption inline. `src: Core features`
- [ ] `C-FE-06` `ui` Switching to grid reads the offset two-column arrangement, cards at staggered offsets. `src: Core features`
- [ ] `C-FE-07` `ui` Switching to gallery reads the looser masonry of mixed-width frames. `src: Core features`
- [ ] `C-FE-08` `ui` The legal route reads eight numbered chapter labels. `src: Core features`
- [ ] `C-FE-09` `ui` Every chapter body grows into place when the chapter is opened from the keyboard. `src: UI/UX notes`
- [ ] `C-FE-10` `ui` An address that exists nowhere reads the studio's own not-found page. `src: Core features`
- [ ] `C-FE-11` `ui` The team grid reads four across, staggered vertically so rows interleave. `src: Core features`
- [ ] `C-FE-12` `ui` The hero sets the studio name at the top of the type scale over a full-bleed render. `src: Core features`
- [ ] `C-FE-13` `ui` The mode pill floats at the bottom centre with the active option marked. `src: Core features`
- [ ] `C-FE-14` `ui` The enquiry modal leaves the route behind inert for as long as the modal is open. `src: Core features`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No address outside the application is referenced anywhere in the build. `src: Constraints`
- [ ] `C-CN-02` `constraint` No binary asset is referenced anywhere in the build. `src: Constraints`
- [ ] `C-CN-03` `constraint` No brand hue appears, nor any rounded corner outside the one raised control group. `src: Constraints`
- [ ] `C-CN-04` `constraint` No search box, no filter, no sort control appears on the index. `src: Constraints`
- [ ] `C-CN-05` `constraint` No notification leaves the application, because no address outside the application is referenced. `src: Constraints`
- [ ] `C-CN-06` `constraint` No visitor-written text is readable by another visitor. `src: Constraints`

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
| `58,079 m2` | Core features, rule 5 | `C-CF-05` |
| `projects/{project_id}/{sha256_of_bytes}.png` | Core features, rule 14 | `C-CF-17` |
| `3` | Core features, rule 48 | `C-CF-28` |
| `3600` | Core features, rule 48 | `C-CF-28` |
| `List` | Core features, rule 39 | `C-CF-33` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the enquiry rate window an origin must stay under | `C-CF-28` |
| the arc radius ratio and sweep the fan is drawn at | `C-CF-10` |
| the aspect ratio each image reference declares | `C-CF-12` |
| the per-frame tilt the fan follows | `C-UX-12` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 2 |
| User roles | 3 | 7 |
| Core features | 14 | 54 |
| User flow | 5 | 11 |
| UI/UX notes | 6 | 12 |
| Technical requirements | 3 | 4 |
| Data model | 6 | 11 |
| Front-end specification | 2 | 14 |
| Constraints | 3 | 6 |
| Deployment contract | 10 | 10 |

