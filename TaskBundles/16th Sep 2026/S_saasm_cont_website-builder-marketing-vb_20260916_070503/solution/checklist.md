# Checklist: Orb Website Builder

Items: 166
Unpinned values flagged: 3
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product is a public marketing surface joined to a sign-up surface, plus a small console for whoever owns a site `src: Overview`
- [ ] `C-OV-02` `capability` A visitor reaches an account from the home route by the header pill, an in-page primary button, the domain field, or the login link `src: Overview`
- [ ] `C-OV-03` `constraint` Orb is not a page editor, not a shop, not an analytics product `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads every marketing route without signing in `src: User roles`
- [ ] `C-RL-02` `role` A visitor cannot open the owner console `src: User roles`
- [ ] `C-RL-03` `role` A visitor cannot read a site nobody has published `src: User roles`
- [ ] `C-RL-04` `role` An owner lists only the sites inside their own workspace `src: User roles`
- [ ] `C-RL-05` `contract` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-06` `literal` Three accounts are seeded: `owner@example.com`, `owner2@example.com`, `visitor@example.com` `src: User roles`
- [ ] `C-RL-07` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` `POST /api/auth/login` returns an access token for a correct email-password pair `src: Core features`
- [ ] `C-CF-02` `contract` A wrong password is denied without disclosing which half was wrong `src: Core features`
- [ ] `C-CF-03` `data` A stored password is a hash, never the literal typed at sign-in `src: Core features`
- [ ] `C-CF-04` `ui` The home route renders seventeen bands stacked in one column in the stated order `src: Core features`
- [ ] `C-CF-05` `capability` Exactly one row of an accordion is open at a time, so opening a row closes whichever was open `src: Core features`
- [ ] `C-CF-06` `capability` The first solutions accordion row is open on load; every questions row is closed `src: Core features`
- [ ] `C-CF-07` `capability` A horizontal gallery scrolls sideways inside a region of its own, never capturing page scroll `src: Core features`
- [ ] `C-CF-08` `ui` Both horizontal galleries are reachable, operable from the keyboard `src: Core features`
- [ ] `C-CF-09` `capability` The seven category chips form one single-select group moved through by arrow keys `src: Core features`
- [ ] `C-CF-10` `capability` Selecting a category chip replaces the rail content with no page navigation `src: Core features`
- [ ] `C-CF-11` `data` Every questions answer sits in the document at first paint `src: Core features`
- [ ] `C-CF-12` `ui` The assistant heading exists twice, with the cycling copy hidden from assistive technology `src: Core features`
- [ ] `C-CF-13` `ui` The point of sale route sets its headline left aligned `src: Core features`
- [ ] `C-CF-14` `ui` On a dark band the primary button inverts to a near-white ground under an ink label `src: Core features`
- [ ] `C-CF-15` `capability` An address the router does not know renders the product's own not-found page `src: Core features`
- [ ] `C-CF-16` `contract` The not-found route answers with a not-found status, never a success status `src: Core features`
- [ ] `C-CF-17` `data` The not-found route carries exactly two meta tags, with no sharing metadata `src: Core features`
- [ ] `C-CF-18` `ui` The not-found route carries the same header, the same footer, as every other route `src: Core features`
- [ ] `C-CF-19` `literal` Nine campaign aliases serve the home document: `/as`, `/gs`, `/v1`, `/v2`, `/412`, `/416`, `/417`, `/419`, `/md/` `src: Core features`
- [ ] `C-CF-20` `capability` An alias rewrites the address bar to the origin root before first paint `src: Core features`
- [ ] `C-CF-21` `contract` `GET /api/domains/availability` answers with a normalised label, an exact result, ranked suggestions, a partial flag `src: Core features`
- [ ] `C-CF-22` `data` A registered name answers as unavailable, under a registry status of registered `src: Core features`
- [ ] `C-CF-23` `literal` A free name answers as available at `1200` minor units in `usd` for a year `src: Core features`
- [ ] `C-CF-24` `contract` The suggestion count defaults to eight, capped at twenty `src: Core features`
- [ ] `C-CF-25` `contract` A padded, mixed-case query normalises to the same lower-cased label `src: Core features`
- [ ] `C-CF-26` `contract` An empty domain query is refused as invalid, naming the field, recording nothing `src: Core features`
- [ ] `C-CF-27` `contract` One address is limited to twenty domain queries a minute, degrading to cached data `src: Core features`
- [ ] `C-CF-28` `data` A recorded domain query carries no identifier of whoever typed the label `src: Core features`
- [ ] `C-CF-29` `literal` `GET /api/templates` clamps a page size larger than `48` rather than refusing `src: Core features`
- [ ] `C-CF-30` `literal` The library holds `33` distinct templates across seven named categories `src: Core features`
- [ ] `C-CF-31` `contract` The template listing carries a facet count per category, ordered by a stable ranking `src: Core features`
- [ ] `C-CF-32` `contract` A category outside the seven is refused as invalid, naming the field `src: Core features`
- [ ] `C-CF-33` `ui` The template rail shows thirty-five template links beside seven category links `src: Core features`
- [ ] `C-CF-34` `contract` `POST /api/accounts` creates an account, a workspace, an empty first site in one transaction `src: Core features`
- [ ] `C-CF-35` `data` A new site is created as a draft, with no live revision, at a free address `src: Core features`
- [ ] `C-CF-36` `contract` A repeat sign-up on one address inside ten minutes creates no second account `src: Core features`
- [ ] `C-CF-37` `contract` A password under eight characters is refused as invalid, writing nothing `src: Core features`
- [ ] `C-CF-38` `ui` The sign-up form links to the terms page before an account can be created `src: Core features`
- [ ] `C-CF-39` `contract` A sign-up filling the unattended decoy field is refused, writing nothing `src: Core features`
- [ ] `C-CF-40` `ui` Sign-up success lands on a full-page confirmation naming the new site, naming its free address `src: Core features`
- [ ] `C-CF-41` `ui` The owner console lists the signed-in owner's sites as a table of rows `src: Core features`
- [ ] `C-CF-42` `contract` `GET /api/sites` returns a top-level array holding only the caller's own sites `src: Core features`
- [ ] `C-CF-43` `ui` A site is added as a new row opened inside the table, saved without leaving the page `src: Core features`
- [ ] `C-CF-44` `contract` A slug already taken anywhere in the product is refused as invalid, writing nothing `src: Core features`
- [ ] `C-CF-45` `contract` Reading one site is denied to an owner who does not own that site `src: Core features`
- [ ] `C-CF-46` `literal` Uploaded bytes land in the object store under `sites/{site_id}/{sha256_of_bytes}.{ext}` `src: Core features`
- [ ] `C-CF-47` `constraint` No byte of an uploaded picture rests on the app container filesystem, nor inside a database column `src: Core features`
- [ ] `C-CF-48` `contract` Content type is settled by inspecting the bytes, never by the supplied name `src: Core features`
- [ ] `C-CF-49` `data` Every uploaded picture carries alternative text supplied by the owner `src: Core features`
- [ ] `C-CF-50` `contract` Uploading identical bytes to one site twice leaves one object, one row `src: Core features`
- [ ] `C-CF-51` `contract` Uploading to a site the caller does not own is denied `src: Core features`
- [ ] `C-CF-52` `contract` Publishing moves a site from draft to published, naming a live revision `src: Core features`
- [ ] `C-CF-53` `contract` A published site answers at its public address to anybody `src: Core features`
- [ ] `C-CF-54` `contract` A draft site's public address answers as not found, disclosing nothing `src: Core features`
- [ ] `C-CF-55` `contract` A draft site's picture is streamed only to the owner of that site `src: Core features`
- [ ] `C-CF-56` `contract` An anonymous request for a draft site's picture is denied `src: Core features`
- [ ] `C-CF-57` `contract` A second owner requesting a draft picture is denied `src: Core features`
- [ ] `C-CF-58` `constraint` Knowing an object key does not let anyone read a draft site's bytes `src: Core features`
- [ ] `C-CF-59` `contract` Rollback returns a published site to draft, clearing the live revision, touching no draft `src: Core features`
- [ ] `C-CF-60` `contract` Two simultaneous publishes of one site leave exactly one live revision `src: Core features`
- [ ] `C-CF-61` `ui` A terms page is reachable from the footer of every route `src: Core features`
- [ ] `C-CF-62` `ui` A privacy page states what the product records about a visitor `src: Core features`
- [ ] `C-CF-63` `literal` The footer legal row reads `Terms of Use`, `Privacy Policy`, `© 2006-2026 orb.com, Inc` `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `contract` Ten named routes answer, beside the nine aliases, beside the catch-all `src: User flow`
- [ ] `C-UF-02` `contract` An unauthenticated request for the console lands on the sign-in route `src: User flow`
- [ ] `C-UF-03` `capability` Signing out returns to the home route, clearing the session `src: User flow`
- [ ] `C-UF-04` `ui` An owner opening another owner's site sees the product's own refusal page `src: User flow`
- [ ] `C-UF-05` `ui` Every list carries an empty state rather than an error `src: User flow`
- [ ] `C-UF-06` `ui` A deferred media block reserves its space so nothing moves on arrival `src: User flow`
- [ ] `C-UF-07` `ui` The domain result region announces itself politely when the answer arrives `src: User flow`
- [ ] `C-UF-08` `capability` The journey from domain search to a draft site completes without an error page `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The page ground reads near-white, the headlines near-black, the body copy mid neutral `src: UI/UX notes`
- [ ] `C-UX-02` `ui` One mid, vivid blue belongs to the header pill, to inline links, to nothing else `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Seven oversized blurred circles sit behind the hero, edges always off stage `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The field holds each colour on a plateau, stepping quickly, never blending `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Anything the visitor triggers resolves inside a third of a second `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Anything the page does by itself runs at three seconds or slower `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Section cards arrive uncovered from below, settling short of full strength `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Under a reduced-motion preference the field holds at one phase, the marquee holds `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Two type families carry the product, named exactly, loaded with a swap policy `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Shadows are cool-tinted, reading as a soft pool a long way below the element `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Each page leads with one primary action, distinct from every secondary control `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Body text meets WCAG AA contrast against its ground `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Full keyboard navigation in document order reaches every control, under a visible focus indicator `src: UI/UX notes`
- [ ] `C-UX-14` `ui` At a narrow viewport nothing overflows sideways, every navigation target staying reachable `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every scaled value is the canvas value times window width over canvas width `src: Front-end specification`
- [ ] `C-FE-02` `ui` Three canvases carry the design: a small one, a medium one, a large one `src: Front-end specification`
- [ ] `C-FE-03` `ui` Inside a breakpoint band every scaled value moves linearly, so nothing steps `src: Front-end specification`
- [ ] `C-FE-04` `ui` The legal caption, the chrome type, the corner radii do not scale `src: Front-end specification`
- [ ] `C-FE-05` `ui` The type scale carries eighteen named roles at the sizes given `src: Front-end specification`
- [ ] `C-FE-06` `ui` Letter-spacing is a negative percentage of the size; line-height is a unitless ratio `src: Front-end specification`
- [ ] `C-FE-07` `ui` A theme is fifty-nine numbered palette slots, not a set of named colours `src: Front-end specification`
- [ ] `C-FE-08` `ui` Layer blur softens the ambient circles; backdrop blur frosts the cards `src: Front-end specification`
- [ ] `C-FE-09` `ui` Four gradients carry the design: the warm wash, the frosted fill, the circle fill, the mesh `src: Front-end specification`
- [ ] `C-FE-10` `ui` Every icon is vector geometry drawn in the page, never a font, never a file `src: Front-end specification`
- [ ] `C-FE-11` `ui` The wordmark is three letters over a solid ground rectangle of the box dimensions `src: Front-end specification`
- [ ] `C-FE-12` `ui` The header stays fixed at full strength at every scroll position, never shrinking `src: Front-end specification`
- [ ] `C-FE-13` `ui` Three header items open a full-width panel of four columns over a promotional strip `src: Front-end specification`
- [ ] `C-FE-14` `ui` All three panels sit in the document at first paint, hidden by state `src: Front-end specification`
- [ ] `C-FE-15` `ui` A panel closes on pointer leave, on Escape, on focus leaving its subtree `src: Front-end specification`
- [ ] `C-FE-16` `ui` The footer carries six columns above a legal row `src: Front-end specification`
- [ ] `C-FE-17` `ui` The home route renders the measured copy deck string for string `src: Front-end specification`
- [ ] `C-FE-18` `ui` The point of sale route renders the measured copy deck string for string `src: Front-end specification`
- [ ] `C-FE-19` `ui` Three groups change with scroll position; nothing else moves `src: Front-end specification`
- [ ] `C-FE-20` `ui` The field pauses when the hero leaves the window, resuming on re-entry `src: Front-end specification`
- [ ] `C-FE-21` `ui` The field degrades to plain rounded boxes, interchangeable at a glance `src: Front-end specification`
- [ ] `C-FE-22` `ui` The point of sale route carries two ambient boxes, never the full field `src: Front-end specification`
- [ ] `C-FE-23` `ui` Seventeen components assemble every band, with nothing else `src: Front-end specification`
- [ ] `C-FE-24` `literal` One stable semantic class of the form `ui-<role>` marks anything selectable `src: Front-end specification`
- [ ] `C-FE-25` `ui` Placeholder pictures are drawn from a seed, never downloaded `src: Front-end specification`
- [ ] `C-FE-26` `ui` The hero headline is the largest element painted first `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` One Node process serves the rendered routes beside the HTTP interface `src: Technical requirements`
- [ ] `C-TR-02` `contract` Routes render on the server, hydrating without re-rendering the tree `src: Technical requirements`
- [ ] `C-TR-03` `literal` Rows persist in PostgreSQL reached through `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-04` `literal` Bytes persist in MinIO reached through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` `src: Technical requirements`
- [ ] `C-TR-05` `literal` The app reads `APP_PUBLIC_URL`, `APP_PUBLIC_PORT` from the environment `src: Technical requirements`
- [ ] `C-TR-06` `constraint` No host, no port, no credential is hardcoded `src: Technical requirements`
- [ ] `C-TR-07` `constraint` No second database, cache, queue, object store, identity provider is introduced `src: Technical requirements`
- [ ] `C-TR-08` `literal` `GET /api/health` returns `200` once the app is ready `src: Technical requirements`
- [ ] `C-TR-09` `contract` One structured log line per request carries a request identifier `src: Technical requirements`
- [ ] `C-TR-10` `data` Every public route carries its own title, its own description, shared with no other route `src: Technical requirements`
- [ ] `C-TR-11` `data` An indexable route carries seventeen head tags `src: Technical requirements`
- [ ] `C-TR-12` `data` A social preview image is generated rather than stored, resolving on every public route `src: Technical requirements`
- [ ] `C-TR-13` `data` A favicon is served, declared in the document head of every route `src: Technical requirements`
- [ ] `C-TR-14` `constraint` No credential, key or admin token appears in anything the browser downloads `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Eight tables carry the product, under timestamps in UTC `src: Data model`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`, written into `/app/USER_README.md` `src: Data model`
- [ ] `C-DM-03` `data` A workspace belongs to exactly one account; a site belongs to exactly one workspace `src: Data model`
- [ ] `C-DM-04` `data` No two sites anywhere share a slug `src: Data model`
- [ ] `C-DM-05` `data` A site's live revision stays empty until the first publish, naming a real revision after `src: Data model`
- [ ] `C-DM-06` `data` A media row records the key, the content type, the byte size, the alternative text `src: Data model`
- [ ] `C-DM-07` `literal` The first owner's workspace is `Kestrel Studio`, holding a published site beside a draft site `src: Data model`
- [ ] `C-DM-08` `literal` The second owner's workspace is `Cedar Workshop`, holding one draft site `src: Data model`
- [ ] `C-DM-09` `contract` Seeding is idempotent, so restarting the app duplicates no row `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No page editor ships: no node tree, no session protocol, no undo `src: Constraints`
- [ ] `C-CN-02` `constraint` No site generation ships `src: Constraints`
- [ ] `C-CN-03` `constraint` No commerce ships: no catalogue, no cart, no payment, no ledger `src: Constraints`
- [ ] `C-CN-04` `constraint` No automation engine, no analytics pipeline, no extension runtime ships `src: Constraints`
- [ ] `C-CN-05` `constraint` No custom domain is registered, delegated, pointed or certificated `src: Constraints`
- [ ] `C-CN-06` `constraint` No outbound email of any kind is sent `src: Constraints`
- [ ] `C-CN-07` `constraint` No external network call happens at run time `src: Constraints`
- [ ] `C-CN-08` `ui` Every chrome destination outside the named routes resolves to an honest placeholder `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is the public port onto the container-internal port `src: Deployment contract`
- [ ] `C-DC-03` `literal` The HTTP interface is served on the same origin under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-05` `literal` Login credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-06` `literal` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served behind a static or preview server, never a dev server `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, never a child of the shell `src: Deployment contract`
- [ ] `C-DC-09` `literal` The listener binds `0.0.0.0`, never a loopback address `src: Deployment contract`
- [ ] `C-DC-10` `constraint` The backing services are already running; no copy is downloaded, installed or started `src: Deployment contract`
- [ ] `C-DC-11` `constraint` No edge function, no persistent volume, no fixed container name, no custom network `src: Deployment contract`
- [ ] `C-DC-12` `contract` Thirteen endpoints answer under the field names given `src: Deployment contract`
- [ ] `C-DC-13` `contract` An invalid or unauthorized call is rejected as a client error, never as a server error `src: Deployment contract`
- [ ] `C-DC-14` `constraint` An in-memory media array, a filesystem copy, a database blob are each a violation `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `owner@example.com` | the first seeded owner | `C-RL-06` |
| `owner2@example.com` | the second seeded owner | `C-RL-06` |
| `visitor@example.com` | the seeded visitor | `C-RL-06` |
| `deku-demo-pw-2026` | the password every seeded account uses | `C-RL-07` |
| `POST /api/auth/login` | the sign-in endpoint | `C-CF-01` |
| `/as` | a campaign alias | `C-CF-19` |
| `/gs` | a campaign alias | `C-CF-19` |
| `/v1` | a campaign alias | `C-CF-19` |
| `/v2` | a campaign alias | `C-CF-19` |
| `/412` | a campaign alias | `C-CF-19` |
| `/416` | a campaign alias | `C-CF-19` |
| `/417` | a campaign alias | `C-CF-19` |
| `/419` | a campaign alias | `C-CF-19` |
| `/md/` | a campaign alias | `C-CF-19` |
| `GET /api/domains/availability` | the domain availability endpoint | `C-CF-21` |
| `1200` | the yearly price of a free name, in minor units | `C-CF-23` |
| `usd` | the currency of every amount | `C-CF-23` |
| `GET /api/templates` | the public template endpoint | `C-CF-29` |
| `48` | the cap on a template page size | `C-CF-29` |
| `33` | the count of distinct templates | `C-CF-30` |
| `POST /api/accounts` | the sign-up endpoint | `C-CF-34` |
| `GET /api/sites` | the owner site listing endpoint | `C-CF-42` |
| `sites/{site_id}/{sha256_of_bytes}.{ext}` | the object key scheme | `C-CF-46` |
| `Terms of Use` | the first legal row link | `C-CF-63` |
| `Privacy Policy` | the second legal row link | `C-CF-63` |
| `© 2006-2026 orb.com, Inc` | the copyright line | `C-CF-63` |
| `ui-<role>` | the stable semantic class form | `C-FE-24` |
| `DATABASE_URL` | the datastore variable | `C-TR-03` |
| `STORAGE_ENDPOINT` | the object store address variable | `C-TR-04` |
| `STORAGE_BUCKET` | the bucket variable | `C-TR-04` |
| `STORAGE_ACCESS_KEY` | the object store key variable | `C-TR-04` |
| `STORAGE_SECRET_KEY` | the object store secret variable | `C-TR-04` |
| `APP_PUBLIC_URL` | the public address variable | `C-TR-05` |
| `APP_PUBLIC_PORT` | the public port variable | `C-TR-05` |
| `GET /api/health` | the readiness endpoint | `C-TR-08` |
| `200` | the ready health status | `C-TR-08` |
| `/app/USER_README.md` | the credential file | `C-DM-02` |
| `Kestrel Studio` | the first owner's workspace | `C-DM-07` |
| `Cedar Workshop` | the second owner's workspace | `C-DM-08` |
| `/api` | the interface prefix | `C-DC-03` |
| `.browser_screenshots/` | a reserved directory | `C-DC-06` |
| `.downloads/` | a reserved directory | `C-DC-06` |
| `0.0.0.0` | the bind address | `C-DC-09` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade behind every named colour role | `C-UX-01` |
| the display family name, left to the builder | `C-UX-09` |
| the corner radius values behind the four named sizes | `C-FE-04` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 3 |
| User roles | 1 | 7 |
| Core features | 26 | 63 |
| User flow | 6 | 8 |
| UI/UX notes | 8 | 14 |
| Front-end specification | 24 | 26 |
| Technical requirements | 11 | 14 |
| Data model | 6 | 9 |
| Constraints | 6 | 8 |
| Deployment contract | 13 | 14 |
