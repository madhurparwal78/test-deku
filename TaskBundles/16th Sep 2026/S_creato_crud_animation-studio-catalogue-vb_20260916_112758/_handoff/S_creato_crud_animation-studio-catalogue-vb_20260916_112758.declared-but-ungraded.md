# Declared but ungraded

Obligations the brief states that no grading channel in this bundle can observe. Each was removed from `solution/checklist.md` rather than given a fabricated citation, per the unobservable-obligation rule in `stage-3-checklist.md` (OPEN-DECISIONS D-H).

| Obligation | Why no channel observes it |
|---|---|
| The frontend is Astro with hydrated islands | the frontend framework is named in the brief and is invisible to a black-box grader, which may not read the app's source (G10) |
| The backend is Fastify, serving the HTTP API on the same origin | the backend framework is named in the brief and is invisible to a black-box grader, which may not read the app's source (G10) |
| No second database, cache, queue, object store, identity provider or mail vendor is introduced | the absence of a second backing service cannot be observed from outside the app; the compose file is the only evidence and no grading channel reads it |
| Startup fails loudly on a missing configuration value, never defaulting | a loud failure on malformed configuration happens before the app is reachable, so no channel that reaches the app can witness it |
| Login credentials are written to /app/USER_README.md | the credentials file lives on the agent container's filesystem, which no grading channel opens |
| Reserved .browser_screenshots/ and .downloads/ directories exist empty at the app root | the reserved directories live on the agent container's filesystem, which no grading channel opens |
| No persistent volume, no fixed container name, no custom network is declared | volumes, container names and networks are compose facts, checked by the layout and schema gates rather than by a grading channel |
| All timestamps are stored in UTC | a timestamp's zone is only assertable by reading a stored value, and an assertion on a timestamp is forbidden by the determinism rule |
| Foreign keys are declared and enforced in the database rather than in application code | declared foreign keys are a schema fact, and a black-box grader may not inspect the schema (G10) |

## Added after the grader-channel review

Twelve more obligations, each one an appearance or a network fact that no channel this bundle ships can witness. The browser executor offers snapshot, navigate, click, fill, select, press-key, scroll and get-text: no computed style, no viewport control, no request log. Rather than leave a substep that fails on every run, the obligation is recorded here and the brief still states it.

| Obligation | Why no channel observes it |
|---|---|
| A picture resolves outward from its centre through a mask ... | a reveal mask is a rendered appearance; the browser executor reads text and the accessibility tree, never a paint |
| A tile preview is silent, looping, uncontrolled ... | the playing state of a muted looping element is not readable through any grading channel this bundle ships |
| Under a coarse pointer, a saved-data preference ... | no channel can set a reduced-motion or saved-data preference: the browser context is created once per run from the executor's own argument |
| At most `12` tiles hold a video element ... | counting attached media elements needs a DOM query the browser executor does not offer |
| A tile leaving the window releases its video element ... | as above: the release of a media element is a DOM fact no channel reads |
| A rendition is chosen from the rendered box width ... | the requested rendition is a network fact, and no channel inspects the request log |
| Three responsive compositions exist ... | no channel can resize the viewport, so a composition change between widths cannot be witnessed |
| One play triangle serves the player ... | comparing two rendered vector shapes is a paint comparison no channel makes |
| The wordmark is optically spaced ... | letter advance is a rendered-geometry fact, outside every channel |
| Text crossing a full-bleed panel boundary composites ... | a blend mode is a computed style, and no channel reads computed styles |
| The custom pointer is suppressed on a coarse pointer ... | no channel can present a coarse pointer or an absent pointer |
| A scrubbed element declares no transition ... | a declared transition is a computed style, outside every channel |
