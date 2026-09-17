# Modelport

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
browse the model catalogue, open a model page, sign in, take an access token, and
create a prediction that reaches `succeeded` with its charge itemised against that
account, without hitting an error page. A different stranger, signed in as another
account, must NOT be able to read that prediction, that account's usage rows or that
account's private models by any means, including a direct request for their
identifiers. The charge has to be a real row in the usage ledger for the exact
amount the rate table implies: a number the page prints to itself does not count,
and the itemised rows for a period must add up to that period's total with nothing
left over.

## Overview

Modelport is a hosted inference platform for developers who would rather rent
accelerators than own them. It is four things at once. A public catalogue of models,
each addressed as `owner/name`, browsable and searchable without an account. A run
form on every model page, generated at request time from that model version's own
declared input schema rather than hand written for each model. A console where a
signed-in developer keeps tokens, run history, spend controls, deployments and
invoices. And a run plane that queues a prediction, executes it, meters it per
second or per unit, and reports what it cost.

The people it serves are the browsing developer who wants to know whether a model
can do the thing they imagined, the integrating developer who wants a credential and
a snippet, the operator who wants a bill they can forecast, and the model author who
wants distribution. Half the catalogue's value is that the models in it were
published by somebody else, so publishing is a first class surface and not an
afterthought.

The business model is metered per-second compute: a prepaid free allowance is drawn
down first, charged usage accrues after it, and a per-account spend cap stops new work
rather than warning about it. Nothing is invoiced in advance and nothing is sold by
the seat.

It deliberately is not a social product. There are no comments, no likes, no
follows, no direct messages and no forum. There is no fine tuning, no multi model
comparison bench and no file upload: every model in this catalogue takes text and
numbers as input and returns text or a structured object. There are no image, video
or audio outputs, no editorial archive, no change history and no enterprise sales
form. Payment is not taken; the invoice is produced from the usage rows and sits
unpaid.

The genuinely hard part is the meter. A prediction is billed at most once, and only
for the work an attempt actually did; a queued prediction that never ran is billed
nothing; and the itemised rows a customer can read must reconcile exactly with the
total they are invoiced, at every scale, under retries and duplicate reports.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `member` | Browse the catalogue signed out or signed in, run any public model and any private model owned by an account they belong to, mint and revoke their own tokens, publish models under their own handle, read their own predictions, usage and invoices, set their own monthly spend cap, create and release their own deployments | **Cannot read another account's predictions, usage rows, invoices, tokens or private models. Cannot add or remove a member of an organisation. Cannot change an organisation's monthly spend cap. Cannot change another member's role.** |
| `owner` | Everything a `member` can do, and for the organisation they own: add and remove members, change a member's role, set the organisation's monthly spend cap, read the organisation's usage rows and invoices, and change the visibility of a model the organisation owns | **Cannot remove the last remaining owner of an organisation. Cannot read a different organisation's records. Cannot read a personal account's predictions or tokens, including a member's own.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a
`member` session to any `owner`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

An unauthorized read of a record that exists is answered as a missing record, not as
a refusal. A refusal confirms the identifier is real, which is how one account maps
another account's work.

Signup is **open**. Anyone can create an account with an email address and a
password from `/signup`, and the account is usable at once.

Four accounts are seeded, and every seeded account uses the password
`deku-demo-pw-2026`.

| Email | Handle | Kind | Role |
|---|---|---|---|
| `owner@example.com` | `maren-vos` | user | `owner` of the organisation `northlight` |
| `member@example.com` | `arden-hale` | user | `member` of the organisation `northlight` |
| `member2@example.com` | `vela-research` | user | belongs to no organisation |

Three organisation accounts are seeded with no login of their own: `northlight`,
`orchard` and `blackpine-labs`. An organisation holds models, tokens and a bill; it
never signs in. A personal account and an organisation account share one handle
namespace, because a model is addressed as `handle/model-name` and the address
cannot be ambiguous about what kind of owner it names.

`member2@example.com` exists so that isolation is observable: it owns nothing in
`northlight`, and every record belonging to `arden-hale`, `maren-vos` or
`northlight` must read as missing to it.

## Core features

### Auth

1. An account is created from `/signup` with an email address, a password and a
   handle. The password is stored hashed, never in clear text, and the seeded
   literal `deku-demo-pw-2026` must work at login for every seeded account.
2. Sign in at `/signin` with email and password. A browser session is carried in a
   cookie marked `HttpOnly`, `SameSite=Lax` and `Path=/`. Signing out revokes the
   session record on the server; deleting the cookie alone is not a sign out.
3. The machine interface authenticates with a bearer credential in the standard
   `Authorization` header. A credential is never accepted in a query parameter.
   Requests from the browser carry the session cookie and a per-session CSRF token,
   never a bearer token, so a token is never exposed to page script. The sign in
   response carries that session's CSRF value as `csrf_token`, and a state changing
   request made with the cookie presents it in the `X-CSRF-Token` header. No state
   changing operation is reachable by `GET`.
4. A handle is 1 to 39 characters from `a-z`, `0-9` and the hyphen, with no leading
   hyphen, no trailing hyphen and no double hyphen. Handles are unique without
   regard to case across personal and organisation accounts.
5. The reserved handle list is checked before any other handle validation:
   `explore`, `pricing`, `enterprise`, `docs`, `blog`, `changelog`, `about`,
   `terms`, `privacy`, `support`, `status`, `signin`, `signup`, `playground`,
   `account`, `settings`, `dashboard`, `predictions`, `trainings`, `deployments`,
   `collections`, `search`, `api`, `static`, `assets`, `home`. A signup claiming any
   of them is rejected as invalid with the error type `handle_reserved`, and no
   account row is written. The router resolves a single leading path segment in this
   fixed order: the reserved list first, then an account handle, then not found.
6. The same list is used by the router and by the handle validator. There is one
   list, read twice.

### The catalogue

7. `/explore` is the catalogue front page and opens with the title `Explore`. It
   carries two labelled columns side by side at the wide tier: a left column headed
   `LATEST` holding one featured model card, and a right column headed
   `POPULAR MODELS` holding a vertical list of model cards ordered by rank.
8. A model is addressed `/<owner>/<model>`, an owner profile at `/<owner>`. The
   owner profile lists that owner's public models and their total run count across
   those models. An owner with no public models renders the header and one honest
   line rather than an empty grid.
9. Every model card is one component rendered at four sizes: a wide `rail` card on
   the home route, a compact `list` card in the catalogue and on owner profiles, a
   large `featured` card at the head of the `LATEST` column, and an `inline`
   reference used wherever a model is named inside prose. All four read the same
   record. The card shows the owner, a literal `/` separator that copies as text,
   the model name, a description, a run count and a badge row.
10. The owner segment and the model name truncate independently, so a long model
    name never pushes its owner out of view. The whole card is one link to the model
    page and the owner segment is a second link to the owner profile, and a keyboard
    reaches both.
11. Run count formatting is unified across every surface that prints one, because
    the reference these numbers come from renders them inconsistently and a buyer
    comparing two models deserves one format. The rule: Below `1000` the integer
    is shown unabbreviated. From `1000` to `999999` it is shown to one decimal place
    with the suffix `K`. At `1000000` and above it is shown to one decimal place
    with the suffix `M`. A trailing zero after the decimal point is dropped. The
    exact value is carried on the element as a `title` attribute. The seeded counts
    render as `17.9M`, `469.7K`, `4M` and `17`.
12. The order of the popular column comes from a stored rank score, and the number
    printed on each card stays the lifetime run count. The score is recomputed on a
    schedule from runs in a trailing window with a decay, plus a term for the number
    of distinct accounts that ran the model, so an old model with an enormous
    lifetime count does not hold the top of the list forever. The score is not
    printed.
13. A collection is a stored, curated, ordered list of models with a slug, a title
    and a one line description, served at `/collections/<slug>`. It is not a saved
    search. The collections band on `/explore` shows each collection's first three
    models by curated order, never by popularity, followed by the remainder count
    written as `and N more`, where `N` is the collection's size minus three.
14. Two collections are seeded. `summarise-text`, titled `Summarise long text`, with
    the description `Use AI to summarise long text with an API`, holding
    `northlight/scribe-2` and `blackpine-labs/prism-2-flex`. `structure-any-text`,
    titled `Turn text into structured data`, with the description
    `Use AI to turn text into structured data with an API`, holding
    `orchard/quickdraw-2`.
15. A model marked `official` carries an `Official` badge. The badge is granted by
    the platform and cannot be set by the model's own author through any endpoint.
    `northlight/scribe-2` is seeded `official`; no other seeded model is.
16. A model page carries a status badge with one of four states: `Warm`, `Cold`,
    `Busy` and `Unavailable`. `Warm` states that an instance is loaded and the first
    run starts at once. `Cold` states that no instance is loaded and prints that
    version's declared load time in seconds beside the word. `Busy` states that
    instances are loaded and saturated. `Unavailable` states that the version is
    withdrawn or that no capacity exists for its hardware class.

### Search

17. `/search` and the header combobox are one search rendered twice. The combobox
    placeholder shows two example queries rather than the word `Search`:
    `Search 'best summarising models' or 'text to structured data'`. A keyboard hint
    beside it names the platform modifier and the letter `k`, and the shortcut opens
    the combobox from anywhere on the page except while focus is inside a text
    field.
18. Search matches models on their address, name and description; owners on their
    handle and display name; and collections on their title and description.
    Results are grouped by kind, and the group order is fixed as models, then
    owners, then collections. Groups are never interleaved by score.
19. An exact model address always ranks first within the models group and is never
    displaced by a looser match. A query that matches nothing names the query back
    to the reader and offers the nearest collection, rather than rendering an empty
    panel.
20. Results are paginated with a cursor, and the facets entity kind, collection and
    warm only are carried as query parameters so a filtered search is a link
    somebody can send.

### The model page

21. `/<owner>/<model>` is the most important route in the product. Its header
    carries, in order: the owner avatar, the address with `owner` as a link and a
    literal `/` separator, a copy control that copies the address, a one sentence
    description, the badge row, and a tab strip reading `Playground`, `API`,
    `Examples` and `README`. A visually hidden heading carries the full address.
22. The first response for the model page carries the model record, the default
    version's input schema, the badge data and the example that prefills the form.
    Nothing above the fold waits on a second request, because the schema is what
    draws the form.
23. The page runs the model's default version unless a version digest is named in
    the address. When a digest is named and it is not the default, the header says
    so, prints the digest in monospace and offers a way back to the default.
24. An anonymous reader gets the whole page: schema, form, examples, README and
    snippets. Only submission is gated.
25. `/<owner>/<model>/api` renders the generated integration documentation for the
    model: the install command, the name of the environment variable that holds the
    credential, the create call built from the current input object, one example per
    read mode, and the input and output schema rendered as tables with types,
    defaults, bounds and descriptions. The credential itself is never printed into
    the page for an anonymous reader.
26. `/<owner>/<model>/examples` is a gallery of runs that really succeeded. Each
    example names the version it ran against, shows its full input, and carries a
    control that loads that input back into the form. An example whose input no
    longer validates against the current schema is hidden rather than left to break.
27. `/<owner>/<model>/readme` renders the author's markdown through a sanitiser with
    an allowlist of elements and attributes. Event handler attributes and
    script bearing addresses are stripped. External links are rendered with the
    opener relationship removed. The same content is served as plain text at
    `/<owner>/<model>/readme.md` so it can be read without the page around it.
28. `/<owner>/<model>/versions` lists every published version, newest first, with
    the digest shortened to eight characters, the created date, the status, the
    default hardware class, a marker where that version's input schema differs from
    the version before it, and an action that opens the model page pinned to that
    version. The list is append only.
29. A version whose status is `withdrawn` is refused for new runs and its row states
    the author's reason inline. `northlight/scribe-2` version `3b71e0c9` is seeded
    withdrawn with the reason
    `Replaced by 8f1c0a4d, which fixes truncated summaries.` A create naming a
    withdrawn version is rejected with the error type `model_version_withdrawn` and
    no prediction row is written.

### The schema driven run form

30. The run form is a pure function of the version's input schema. There is no per
    model branch anywhere, no allowlist of known models, and no hand written form.
    A model whose schema the builder has never seen must still render a usable form.
31. The declared type vocabulary maps to controls as follows. A `string` renders a
    single line text input. A `string` carrying the format hint `text` renders an
    auto growing textarea. A `string` carrying an `enum` renders a select. An
    `integer` or a `number` renders a numeric input bounded by the schema's
    `minimum` and `maximum`, and renders a slider in addition when both bounds and a
    `step` are declared. A `boolean` renders a checkbox labelled with the field
    name. An `array` of scalars renders a repeating row editor with add and remove
    controls. An `object` renders a collapsed JSON editor for that subtree.
32. Each field row renders in this fixed order: a type glyph, the field name in
    monospace, a required marker where the field is required, the declared type in
    the body face, the control, the description, and a line beginning `Default:`
    printing the default value as JSON. The `Default:` line is what tells a reader
    that an empty control is not the same as a missing value.
33. Field order comes from the schema's declared `order` property. Where the schema
    declares no order, required fields come first and optional fields follow in
    declaration order. Fields the schema marks `advanced` collapse into a disclosure
    below the primary set, and the disclosure's open state is remembered per model
    in the browser.
34. Validation runs in two layers and the client layer is a convenience, never the
    authority. The client checks required presence, type, enum membership, numeric
    bounds and string length, on blur and on submit, never on every keystroke. The
    server re derives the same rules from the stored schema and is what decides.
35. A rejected submit puts the message directly below the control, marks the control
    invalid for assistive technology, points the control at its message, and moves
    focus to the first invalid control. The submit control never disables itself on
    an invalid form: a disabled control that will not say why is worse than a
    refusal that does. A rejected submission writes no prediction row.
36. A server side rejection of the input carries the error type
    `prediction_input_invalid` and a `errors` array, in field order, each entry
    carrying `field`, `code` and `detail`.
37. The input panel carries five tabs: `Form`, `JSON`, `Node.js`, `Python` and
    `HTTP`. The `JSON` tab holds the same input object as the form. Editing the
    JSON updates the form and editing the form updates the JSON. Invalid JSON is
    reported inline and does not destroy the form's last valid state. The round trip
    is lossless: `0`, `false`, an empty string and `null` each survive the trip and
    stay distinct from a field that is absent.
38. The three snippet tabs are read only and are generated from the same input
    object the request is built from, so a snippet that is copied and run elsewhere
    produces the identical request. No credential is inlined into a snippet: the
    snippet reads the credential from the environment variable
    `MODELPORT_API_TOKEN`, and that name is printed on the API tab and on the token
    screen.
39. The form is prefilled in this order of precedence: the model's featured example
    if it declares one, otherwise the schema defaults; then any input values carried
    on the query string, which are validated before they are applied and dropped
    with a notice when they are invalid; then the last input used for this model on
    this browser, with a control named `Reset to default inputs` that returns to the
    defaults.
40. Submit sits in a footer pinned to the bottom of the input column, holding the
    outlined `Reset to default inputs` control and a solid `Run` control carrying
    the suffix `(ctrl+enter)`. The textarea publishes its own hint reading
    `Shift + Return to add a new line`.
41. An anonymous submit makes no request. The control resolves to `/signin`
    carrying a return target that restores the exact input, so signing in lands the
    reader back on a filled form. The page states
    `Sign in to run this model. We will bring you back here with your inputs.`
42. The form states what the run will cost before the run. Where the version is
    priced by time, the page shows the charge implied by the version's declared run
    seconds at its hardware rate and labels it as an estimate. Where the version is
    priced per unit of output, the page shows the exact charge for the current
    inputs, because it is knowable. The number changes when an input that drives it
    changes, and the mapping from input to the priced quantity is declared in the
    version's own metadata.

### The output surface

43. The output column is a state machine with six designed states, each visually and
    textually distinct from the others. `Empty` shows the model's most recent example
    output at reduced prominence, labelled as an example. `Queued` shows a
    determinate progress ring and the honest sentence
    `Waiting for a machine.` where a position is known. `Booting` is named
    separately from `Queued` and prints the version's declared load time, reading
    `Loading this model onto a machine. This usually takes 12 seconds the first time.`
    for a version whose load time is 12 seconds. `Streaming` shows text arriving
    piece by piece. `Succeeded` shows the rendered output, the elapsed time and the
    action row. `Failed` and `Canceled` show the error string in a monospaced block
    with the logs already expanded.
44. The elapsed time is printed under the output as a label reading `Generated in`
    above the value in seconds, set large. It is the number the reader was waiting
    on.
45. The renderer is chosen from the version's declared output type and never by
    sniffing the response. A `string` output renders as markdown through the same
    sanitiser as the README, with a raw toggle, and while a run is streaming the raw
    text is shown and markdown is rendered once the stream ends. An `object` or an
    `array` output renders as a collapsible JSON view with a copy control. Every
    rendered output reserves its space before the content arrives, so the panel does
    not resize under the reader.
46. A disclosure labelled `Show logs` sits under the output, collapsed by default on
    success and expanded by default on failure. The log view follows the tail while
    the run is active and detaches when the reader scrolls up.
47. The action row reads, in order: `Tweak it`, `Share`, `Download`, `Report` and
    `View full prediction`. `Tweak it` loads this prediction's exact input back into
    the form without running it. `Share` mints a read only link with its own
    identifier and its own expiry, and is offered only for a prediction on a public
    model. `Download` fetches the output with a filename derived from the model
    address and the prediction identifier. `Report` opens a report form with a short
    closed category list and an optional note. `View full prediction` navigates to
    `/predictions/<id>`.
48. Outputs are not kept forever. A prediction's output is purged one hour after the
    run completed, the record survives with its metadata and its `data_removed` flag
    set true, and the panel prints
    `The output for this prediction has been deleted. The record of the run is kept.`
    A purged prediction never renders a broken frame. While an output is still
    present the panel prints the remaining lifetime next to the download control.

### Predictions and the run plane

49. A prediction is one execution of one model version against one input. It is the
    row the meter reads, the row the invoice sums and the row a developer debugs
    against. Its identifier begins `pr` and is 14 characters long, and it is
    returned before the work starts.
50. A prediction records: the version it ran, the validated input, a status, the
    output, an error string when it failed, logs, metrics, `created_at`,
    `started_at`, `completed_at`, the source it came from, and `data_removed`.
51. The status vocabulary is exactly `starting`, `processing`, `succeeded`, `failed`
    and `canceled`, in lower case. The interface additionally shows `canceling`
    while a cancel has been asked for and not yet acknowledged. Status is monotonic:
    a prediction that has reached `succeeded`, `failed` or `canceled` never leaves
    that state, and a late report about a terminal prediction is dropped.
52. A prediction always references an immutable version, never a mutable model
    pointer, so a run can be reproduced from its own record after the model's
    default version has moved on. A create that names a model address rather than a
    digest resolves the default version and returns the resolved digest in the
    response.
53. `created_at` to `started_at` is queue time and is never billed. `started_at` to
    `completed_at` is the part that is billed.
54. A version whose status badge is `Cold` keeps no instance loaded between runs on
    shared capacity, so every prediction on it waits its declared load time in
    `starting` before it begins processing. A version whose badge is `Warm` begins
    processing at once. `blackpine-labs/prism-2-flex` is seeded `Cold` with a
    declared load time of `12` seconds; `northlight/scribe-2` and
    `orchard/quickdraw-2` are seeded `Warm`; `arden-hale/notes-tidy` is seeded
    `Cold` with a declared load time of `2` seconds.
55. A caller reads a result in one of four ways, all of which read the same state
    machine and none of which may report a state the others have not reached. An
    asynchronous poll: create returns at once with the status `starting` and a poll
    address, and every poll response carries a cache directive that forbids an
    intermediary from storing it. A blocking wait: the create request carries the
    header `Prefer: wait=<seconds>`, the server holds the connection up to a
    published ceiling of `60` seconds and returns the terminal record if it arrives
    and the pending record otherwise, never a timeout. A server sent stream at
    `/api/predictions/<id>/events`, which carries an event identifier per frame,
    resumes from a `Last-Event-ID` header on reconnect, and closes after emitting one
    terminal event. A webhook, described below.
56. A create may carry a `webhook_url` and a `webhook_events` list drawn from
    `start`, `output`, `logs` and `completed`. The address must use the `https`
    scheme and must resolve outside the private, loopback, link local and multicast
    ranges. An address that fails either check is rejected with the error type
    `webhook_url_not_allowed` and no prediction row is written. The check is
    re applied at delivery time, because a name that resolved publicly yesterday can
    resolve to an internal address today.
57. On a terminal state the platform writes, in one transaction, the prediction's
    status, timings, metrics and output; one usage row; and one outbox row for the
    event `prediction.completed`. A separate publisher moves outbox rows to the
    delivery log after the transaction commits. Nothing publishes a delivery from
    the request that created the prediction, so a caller is never told about a
    result the platform cannot then produce.
58. Each delivery attempt is recorded with its endpoint, the event identifier, the
    attempt count, the last status code and the next attempt instant. A delivery is
    signed over the timestamp and the raw body with a per endpoint secret, and the
    signature and the timestamp travel in headers. Retries back off with jitter for
    roughly 24 hours on a connection failure and on any `5xx`. A `4xx` other than a
    rate limit response is not retried. Delivery order is not guaranteed, so every
    payload carries the prediction's current status and a sequence number that only
    increases. The delivery log for a prediction is readable by its owner at
    `/api/predictions/<id>/deliveries`, and every row carries a replay control.
59. Creation accepts an `Idempotency-Key` header. The same key with the same body
    within 24 hours returns the original prediction and starts no second run, with
    the same response body and the same status code. The same key with a different
    body is rejected with the error type `idempotency_key_conflict`, and no second
    prediction row is written. Keys are scoped to the account, so two accounts using
    one key do not collide. Twenty concurrent creates carrying one key and one body
    produce exactly one prediction.
60. Cancellation is cooperative. A cancel moves the record to `canceling` and to
    `canceled` only once the run has stopped. A prediction cancelled while it is
    still `starting` never ran, so it produces no usage row and is billed nothing. A
    cancel of a prediction already in a terminal state is rejected as invalid and
    changes nothing.
61. `/predictions` is a filterable table over the account's own predictions with
    filters for model, status, source and date range, sorted by creation instant
    descending only. Pagination is by cursor, never by offset, because the list
    grows while it is read and an offset shows duplicates and skips rows. The cursor
    encodes the creation instant and the identifier as a tie breaker, and stays
    valid across a page of new inserts.
62. `/predictions/<id>` shows four panels in this order: the output rendered by its
    type, the input as submitted with a control that copies the whole object as a
    request body, the logs, and the metrics with the cost itemised. The itemised
    cost names the priced quantity, the unit, the rate applied and the resulting
    charge, so the number can be checked by hand. A control reruns the same input as
    a new prediction.

### Tokens

63. A token is the product in one string: whoever holds it can spend the account's
    money. It is shaped as the prefix `mp_` followed by 40 characters drawn from the
    upper case letters, the lower case letters and the digits. The prefix exists so
    a leaked credential is recognisable, and the pattern is published on the API
    tab.
64. Only a hash of the token is stored. The clear value appears in exactly one HTTP
    response, at creation, and in no log line, audit row, error body or database
    column. Thereafter the screen shows the prefix and the last four characters
    only. The creation panel states
    `This is the only time we will show you this token. Copy it now.`
65. Every token carries a name supplied by its creator, a creation instant, the
    account that created it, a last used instant and a last used source address. A
    token belongs to an account; a token created under an organisation acts as that
    organisation and is visible to that organisation's owners.
66. Scopes are `read`, `run`, `write` and `admin`. A `run` token may create
    predictions and read its own results. A `read` token may create nothing and a
    create presented with one is rejected with the error type
    `token_scope_insufficient`, leaving no prediction row. Scope is checked on the
    server for every operation.
67. Expiry is optional and is chosen from `30`, `90`, `365` days or never.
68. Rotation issues a new value and marks the old one to expire after a grace window
    of `24` hours, with both live during the window, because the old value is
    embedded in something that is running. Revocation is immediate: a revoked token
    is refused on its very next use, and the refusal is indistinguishable in shape
    from the refusal a token with an insufficient scope receives.
69. Revoking a token asks for the token's name to be typed first, and the screen
    states
    `Type the token's name to revoke it. Anything using it will stop working immediately.`
70. The token table is sorted by last used with never used tokens first, because
    those are the forgotten ones. Its columns are name, masked value, scope pills,
    created, last used, expiry and a row menu carrying rotate, rename and revoke.
    An account holds at most `20` tokens, and a create past that is refused with the
    limit named and the least recently used token suggested for revocation.

### Metering and spend controls

71. Every charge is traceable to one prediction, one hardware class or priced unit,
    a start instant, an end instant and a published rate. A customer must be able to
    sum the itemised rows of a period and arrive at exactly the invoice total for
    that period, with no reconciling item.
72. Money is held as integer micro units of United States dollars, written
    `amount_micros`, with the currency `usd`. `1000000` micro units is one dollar.
    No amount is held or computed as a decimal fraction anywhere.
73. Hardware is a closed set of named classes. The seeded catalogue is:

    | Class | Display name | Processors | Memory | Accelerator memory | Rate |
    |---|---|---|---|---|---|
    | `cpu-small` | `CPU (Small)` | `1x` | `2GB` | `-` | `25` micro units per second |
    | `cpu-large` | `CPU (Large)` | `4x` | `8GB` | `-` | `100` micro units per second |
    | `gpu-a40` | `GPU A40` | `8x` | `48GB` | `48GB` | `1200` micro units per second |

74. A rate row carries `effective_from` and `effective_to` as a half open interval,
    and exactly one row per class covers any instant. A prediction is priced with
    the rate in force at its start instant, never with today's rate, so a rate
    change never reprices history. A rate scheduled to take effect later is shown on
    the pricing route beside the current rate, with its date, before it takes
    effect.
75. The charge for a prediction is one formula in three configurations. It is the
    priced `quantity` multiplied by `rate_micros`, divided by the unit divisor, and
    rounded up to the next whole micro unit. Under `per_second` the quantity is the
    recorded run seconds and the divisor is `1`. Under `per_output_item` the
    quantity is the number of items in the output and the divisor is `1`. Under
    `per_thousand_output_tokens` the quantity is the recorded output token count and
    the divisor is `1000`. There is one billing path, not three.
76. The seeded pricing and the charges it implies:

    | Model | Priced | Rate | Divisor | Quantity | Charge |
    |---|---|---|---|---|---|
    | `northlight/scribe-2` | `per_second` on `cpu-small` | `25` | `1` | `4` seconds | `100` |
    | `arden-hale/notes-tidy` | `per_second` on `cpu-small` | `25` | `1` | `2` seconds | `50` |
    | `orchard/quickdraw-2` with `count` `3` | `per_output_item` on `cpu-large` | `40000` | `1` | `3` items | `120000` |
    | `blackpine-labs/prism-2-flex` with `max_words` `60` | `per_thousand_output_tokens` on `gpu-a40` | `3750` | `1000` | `60` tokens | `225` |
    | `blackpine-labs/prism-2-flex` with `max_words` `7` | `per_thousand_output_tokens` on `gpu-a40` | `3750` | `1000` | `7` tokens | `27` |

    The last row is the one that settles the rounding: `7` multiplied by `3750` is
    `26250`, divided by `1000` is `26.25`, and the charge is `27`.
77. Exactly one usage row exists per prediction. A second report of the same
    completed prediction adds no second row and changes no amount. The uniqueness is
    a property of the stored data, not of a read the code performs before writing.
78. Hourly and daily rollups per account, per model and per hardware class are a
    cache over the usage rows and never a source of truth. Deleting every rollup and
    rebuilding from the usage rows reproduces every historical figure exactly.
79. A daily reconciliation re sums the raw usage rows for the previous day and
    compares them against the stored rollups and the running invoice total. Any
    difference at all, down to a single micro unit, raises a record naming the
    account and the amount, and the raw rows are what win.
80. Each account carries a monthly spend cap. The default cap is `2000000` micro
    units. Once month to date spend has crossed the cap, a new prediction is refused
    with the error type `spend_cap_exceeded` before any work is started, and the
    message reads
    `This run would take you over your monthly limit of $2.00. Raise the limit or wait until the period resets.`
81. The cap is checked in the create path on the server, before scheduling, and it
    is the same check for every entry point: the web run form, the machine
    interface, and a prediction addressed at a deployment. Greying out a button is a
    courtesy and never the enforcement.
82. Work already running is never killed by a cap, so a cap can be exceeded by at
    most the value of the work in flight when it was crossed, and the usage screen
    says so rather than implying a hard ceiling.
83. Warning notices fire once per period per threshold at 50, 80 and 95 per cent of
    the cap, and are not repeated within the period.
84. Every account has a free allowance of `500000` micro units per period, consumed
    before charged spend and displayed as its own balance rather than blended into
    the spend figure.
85. `/account/usage` carries a date range picker defaulting to the current period
    and three views over the same rows: by day, by model, and by source. The by day
    view draws the free allowance as its own band rather than as another colour of
    spend. The by model view is sorted by cost. Every view exports the underlying
    rows as a file generated in the browser from data already fetched, carrying the
    same identifiers the screen shows.

### Billing

86. An invoice is generated from usage rows and never from rollups, and is immutable
    once issued. A correction is a credit note that references the original. Each
    invoice carries the period, line items by model and hardware class, the
    quantity, the unit rate, the free allowance applied as a discount line, and a
    total. Re rendering an invoice a year later reproduces the same numbers.
87. `/account/billing` shows the current period's accrued usage, the free allowance
    remaining, the projected total at the current run rate and the cap; the payment
    method as a masked reference; the invoice list with status, amount, period and
    a download; and the billing details, which are editable and audited. Payment is
    not taken in this environment, so an issued invoice stays `open`.
88. Money is rendered from the stored integer micro units and never from a fraction
    computed in the page. A period total is shown to two decimal places. A single
    run is shown to four significant figures, because a single run can legitimately
    cost less than one cent, and showing it as `$0.00` reads as free. Where a value
    would round to zero at two places, the smaller unit is shown instead.

### Deployments

89. A deployment is a named, owned configuration that pins one immutable version to
    reserved capacity with its own scaling bounds, so first run latency stops being
    a surprise. It is addressed `/<owner>/<deployment-name>` and accepts predictions
    at its own address, so moving an integration from shared capacity to reserved
    capacity is a one line change.
90. A deployment carries a name that is unique within its owning account and
    immutable after creation, a model version, a hardware class, `min_instances`,
    `max_instances` and `concurrency`. `min_instances` of zero means scale to
    nothing when idle and accept the cold start; one or more means always warm and
    billed continuously whether or not anything runs.
91. The creation form states the standing cost of `min_instances` above zero in
    money per day, beside the control that sets it, before the change is saved. For
    one instance on `cpu-small` that is `2160000` micro units per day, and the form
    reads
    `Keeping 1 instance warm on cpu-small costs about $2.16 per day, whether or not anything runs.`
92. Scaling decisions are made on queue depth and queue age, never on processor
    utilisation. Instances are added when queue age has been above the target for
    fifteen seconds or when queue depth exceeds concurrency multiplied by the
    current instance count. Instances are removed after a cooldown of idle time,
    which defaults to five minutes and is settable between one and sixty minutes. At
    most one scale up decision is made every ten seconds and one scale down every
    cooldown.
93. A cooldown shorter than the pinned version's declared load time is refused, with
    the measured load time named, because a deployment that scales down faster than
    its model loads spends its life loading.
94. At `max_instances` further work queues rather than failing, and the queue age is
    shown in the interface and carried in the response headers.
95. Changing the version or the hardware class writes a release row recording who,
    when, from what, to what and an optional note. A release rolls forward by
    starting new instances before draining old ones. Rollback is a first class
    control that writes a new release pointing at the previous configuration; it
    never edits or deletes a release row.
96. `/deployments/<owner>/<name>` shows the address, the current version digest, the
    hardware class and a live instance count with its bounds; requests per minute,
    queue depth and queue age over one hour with the scaling decisions marked on the
    same axis; median and ninety ninth percentile run time and the cold start count
    reported separately; the error rate by class with the most recent failing
    prediction linked; the release log newest first with a rollback control on each
    row; and the standing cost so far this period shown separately from per run
    cost.
97. One deployment is seeded: `arden-hale/tidy-live`, pinned to
    `arden-hale/notes-tidy` version `9a2b61de`, on `cpu-small`, with
    `min_instances` `0`, `max_instances` `3` and `concurrency` `1`.

### Publishing a model

98. Publishing is a three step wizard, one route per step. `/models/new/identity`
    takes the owner handle, the model name, the one line description and the
    licence. `/models/new/packaging` takes the declarative packaging document that
    names the base environment, the system packages, the language packages and the
    predictor entry point, and takes the typed signature of the predict method.
    `/models/new/review` shows the derived input schema, the derived output schema
    and the digest, and carries the confirm control. Each step is reachable by its
    own address, and the address a reader is on is the step they are on.
99. The input and output schema are derived from the submitted packaging document
    and the predict signature, never from anything typed into a schema field. There
    is one source of truth for a version's schema, and the run form, the machine
    interface and the validator all read it.
100. The version identifier is the content digest of the packaging document and the
     derived schema together, so identical content is always the same version.
     Pushing identical content twice returns the existing version and creates no
     second row.
101. A failure at any step of publication leaves no version row and no partial
     registry entry. Publication is atomic: a version is never half visible.
102. A version carries `id`, the model it belongs to, `created_at`, `created_by`,
     the derived schema, the default hardware class, a status from `building`,
     `active`, `deprecated` and `withdrawn`, a withdrawal reason where it has one,
     and a `fast_boot` flag. A version is never mutated and is never deleted while
     a prediction references it. Deprecation hides a version from the catalogue and
     warns on use; withdrawal refuses new runs and states its reason to callers.
103. Moving a model from private to public requires a description, a licence and at
     least one example that has run successfully, and the transition is recorded in
     the audit log. Moving a model from public to private is permitted, and the
     confirmation names the model and states how many other accounts ran it in the
     last ninety days.
104. Renaming or transferring a model keeps the old address working as a permanent
     redirect, so an integration that pinned the old address keeps running.

### Organisations and membership

105. An organisation has exactly two roles, `owner` and `member`. An organisation
     must have at least one owner at all times, and an attempt to remove the last
     owner is refused.
106. `/<org>/settings/members` lists members with their role and a control to change
     it or remove them, and is reachable only by an owner of that organisation. A
     `member` requesting it, or calling the endpoints behind it, is denied at the
     server and the membership rows are unchanged.
107. Removing a member revokes that member's organisation scoped tokens in the same
     write that removes the membership. A membership removed while a token is live
     leaves nothing usable behind.
108. A role change takes effect on the next authorization evaluation, not on the
     member's next sign in.
109. Visibility follows ownership. A public model is readable by anyone including an
     anonymous reader, and runnable by any authenticated principal holding the `run`
     scope with budget remaining. A private model is readable and runnable only by
     principals of the owning account. A version inherits its model's visibility and
     can never be public while its model is private. A prediction is readable only
     by the account that created it, unless it ran on a public model and was shared
     by explicit action. A deployment is readable only by its owning account. Usage
     rows and invoices are readable by an `owner` only.
110. `arden-hale/notes-tidy` is seeded private. A request for it, for any of its
     versions, or for any prediction on it, made by `member2@example.com`, is
     answered as a missing record. The response is the same shape a request for an
     identifier that was never issued receives.

### Audit

111. An append only audit log records: a token created, rotated, revoked or used for
     the first time; a member added, removed or role changed; a model's visibility
     changed; a deployment released, scaled or deleted; a spend cap changed; and
     billing details changed.
112. Each entry carries the acting principal, the action, the resource type and
     identifier, the before and after values of the fields that changed, the source
     address, the request identifier and the instant.
113. Each entry carries a hash of its own content and the hash of the previous entry
     for the same account, written at the time the entry is written. Recomputing the
     chain over an account's entries detects a deleted entry, a reordered entry or
     an edited field. An account's audit log is readable by that account at
     `/api/account/audit` and by nobody else.

### The launch surface

114. A first time visitor is asked once, in a dismissible band, whether non
     essential cookies are allowed. The answer is stored under the name
     `mp_cookie_choice` with the value `accepted` or `declined`, survives a reload,
     and the band does not reappear for that browser. The announcement band above
     the header is dismissible separately, its dismissal is keyed by the promotion
     identifier `promo-autumn-2026` so a later promotion reappears, and dismissing
     it reflows the header upward without the page jumping.
115. Every form in the product rejects invalid input inline rather than on a
     separate page, names the field that was wrong in the message beside it, and
     writes nothing when it rejects. This holds for signup, sign in, the run form,
     the token form, the deployment form, the publish wizard and the report form.
116. Every public route carries its own document title and its own meta description,
     and no two public routes share either one.
117. `/sitemap.xml` lists every public route in the product, and `/robots.txt` names
     that sitemap by its absolute address.
118. An address that resolves to nothing renders the product's own not-found page
     rather than a server default, answers as not-found, keeps the global header and
     footer including the search control, names the address that was tried, offers a
     way back to the catalogue, and lists the three closest model addresses. A
     withdrawn model is not a not-found: it renders the model with its withdrawal
     reason and its version list.
119. The site serves a favicon at `/favicon.ico` and declares it in the document
     head of every route.
120. Nothing the browser downloads carries a credential. No token value, no database
     password and no session secret appears in any HTML document, any stylesheet,
     any script bundle or any JSON response the browser can reach while signed out
     or signed in as an ordinary account.
121. Every page view of a public route is recorded with the route that was viewed
     and the instant it was viewed. A model's owner reads the page view count for
     that model's own routes at `/api/models/<owner>/<name>/views`, and nobody else
     can.
122. Every public route declares a social preview title and a social preview image in
     its document head, and the declared preview image resolves rather than
     returning not-found.

### The machine interface

123. The interface is resource oriented, JSON in and JSON out, served under the
     `/api` prefix on the same origin. The resources are predictions, models,
     versions, deployments, collections, tokens, account and webhooks.
124. Lists are paginated by cursor everywhere and offsets are not offered. A request
     carries `cursor` and `limit`, the default limit is `25` and the maximum is
     `100`. A response carries `results`, `next` and `previous`, with `next` and
     `previous` both opaque and both absent where there is no further page. Ordering
     is fixed per resource with the identifier as the final tie breaker.
125. Every error carries the same body: `type`, a stable machine readable slug that
     never changes meaning; `title`, stable prose; `detail`, which may name values;
     `status`, the numeric status of the response; `instance`, the request
     identifier; and `errors`, an array of field errors in field order rather than a
     map. The request identifier is printed in every error surface in the interface,
     and it begins `req_`.
126. The error type vocabulary is closed: `authentication_required`,
     `token_scope_insufficient`, `not_found`, `prediction_input_invalid`,
     `handle_reserved`, `model_version_withdrawn`, `idempotency_key_conflict`,
     `spend_cap_exceeded`, `webhook_url_not_allowed`, `quota_exceeded` and
     `rate_limited`. No error body carries a credential, an input document or a
     stack trace.
127. Requests are rate limited per token at `60` requests per minute. Every response
     carries the remaining allowance and the reset instant for the applicable
     bucket. A request past the limit is refused with the error type `rate_limited`
     carrying a retry hint. Concurrent predictions are a different limit and behave
     differently: past the concurrency limit work is queued with its position
     reported, not refused.
128. Within the major version fields may be added and never removed or retyped,
     enumerations may gain members so callers tolerate unknown ones, and defaults
     never change silently. A model's own input schema is exempt and cannot be
     otherwise, which is why the version list marks a schema change and why a caller
     pins a digest.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | Signed out: the marketing home with the live example and the two catalogue rails. Signed in: the dashboard replaces it at the same address | none |
| `/explore` | The catalogue front page: featured, popular and the collections band | none |
| `/collections/<slug>` | One curated collection and its full model list | none |
| `/search` | Faceted search over models, owners and collections | none |
| `/pricing` | The rate card, the hardware table and the billing rules | none |
| `/privacy` | What the product stores about an account and for how long | none |
| `/terms` | The terms of use | none |
| `/sitemap.xml` | Every public route | none |
| `/robots.txt` | Points at the sitemap | none |
| `/signin` | Sign in, carrying an optional return target | none |
| `/signup` | Create an account and claim a handle | none |
| `/<owner>` | Owner profile and that owner's public models | none |
| `/<owner>/<model>` | Model detail with the run form and the output panel | none to view, session or token to run |
| `/<owner>/<model>/api` | Generated integration documentation for the model | none |
| `/<owner>/<model>/examples` | Gallery of runs that succeeded, each loadable into the form | none |
| `/<owner>/<model>/readme` | The author's long form description | none |
| `/<owner>/<model>/readme.md` | The same content as plain text | none |
| `/<owner>/<model>/versions` | Every published version, newest first | none |
| `/<owner>/<model>/settings` | Visibility, description, licence and the default version pointer | owner of the model |
| `/dashboard` | Recent runs, month to date spend against the cap, and the deployments summary | session |
| `/predictions` | Filterable run history over the account's own predictions | session |
| `/predictions/<id>` | One prediction: output, input, logs, metrics and cost | session, owner only |
| `/account/tokens` | Mint, rotate, rename and revoke tokens | session |
| `/account/usage` | Usage by day, by model and by source, with export | session |
| `/account/billing` | Current period, payment method, invoices and billing details | session, owner for an organisation |
| `/account/organisations` | The organisations this account belongs to and its role in each | session |
| `/<org>/settings/members` | Add, remove and re role members of an organisation | session, owner of that organisation |
| `/models/new/identity` | Publish, step one: owner, name, description, licence | session |
| `/models/new/packaging` | Publish, step two: the packaging document and the predict signature | session |
| `/models/new/review` | Publish, step three: the derived schemas, the digest and confirm | session |
| `/deployments` | The account's deployments with their instance counts | session |
| `/deployments/<owner>/<name>` | One deployment: traffic, latency, errors, releases and cost | session, owner only |

Every route under `/dashboard`, `/predictions`, `/account`, `/models/new` and
`/deployments` is a console route and carries the persistent left sidebar described
in `## UI/UX notes`. Every public route carries the header and footer instead.

### Entry and redirects

- An anonymous request for a console route redirects to `/signin` carrying the
  requested address as a return target, and signing in lands on that address rather
  than on the dashboard.
- Signing in with no return target lands on `/dashboard`.
- A signed in request for `/` renders the dashboard at that same address. It is not
  a redirect, and the address bar still reads `/`.
- Signing out revokes the session on the server and lands on `/`.
- A session that has expired mid action returns the reader to `/signin` with the
  return target set to the address they were on, and the action is not performed.
- A `member` who opens `/<org>/settings/members` for an organisation they do not own
  is answered as a missing page, and the same request made against the endpoint
  behind it is denied at the server with the membership rows unchanged.
- A request for `/<owner>/<model>` where the model is private and the reader is not
  a principal of the owning account is answered as a missing page.
- A request for a handle that is neither reserved nor an account is answered by the
  not found page, which names the address and lists the three closest model
  addresses.

### Journeys

1. **A visitor reads the catalogue and opens a model.** Open `/`. The hero reads
   `Run AI with an API.` over the gradient ground, with a code panel on one side and
   the output of that exact sample on the other. Below it, a chip group labelled
   `With Modelport you can` and two model rails drifting in opposite directions.
   Click `Explore models`. `/explore` opens with the title `Explore`, the `LATEST`
   column and the `POPULAR MODELS` column side by side. Click the card for
   `northlight/scribe-2`. The model page opens with the address in the header, the
   `Official` badge, the `Warm` badge, the run count reading `17.9M`, and the run
   form already drawn from the version's schema with the featured example in the
   prompt field.
2. **A visitor tries to run and is asked to sign in.** On
   `/<owner>/<model>` for `northlight/scribe-2`, type a prompt and press `Run`. No
   request is made. The page states
   `Sign in to run this model. We will bring you back here with your inputs.` and
   the control resolves to `/signin`. Sign in as `member@example.com` with
   `deku-demo-pw-2026`. The model page returns with the prompt still in the field.
3. **A developer takes a token and runs a model.** From the sidebar open
   `/account/tokens`. Press the create control, name the token `laptop`, choose the
   scope `run`, and confirm. The full value is shown once in a monospaced field
   beside the sentence
   `This is the only time we will show you this token. Copy it now.` Reload the
   page; the row now shows the prefix and the last four characters only. Open
   `northlight/scribe-2`, press `Run`, and watch the output panel move from `Queued`
   to `Succeeded`, ending with the label `Generated in` above the elapsed time and
   the action row underneath.
4. **The charge appears and reconciles.** Open `/predictions`. The newest row is the
   run just made, with its status pill, the model address in monospace, the duration
   and the cost. Open it. The metrics panel itemises the charge as `4` seconds at
   `25` micro units per second, giving `100`. Open `/account/usage` for the current
   period. The by model view lists `northlight/scribe-2` with one run and a cost of
   `100`, and the period total equals the sum of the itemised rows.
5. **A run form renders from a schema the reader has never seen.** Open
   `orchard/quickdraw-2`. The form carries a required `subject` text field, a
   `count` numeric field with a slider bounded at `1` and `4`, and a `style` select
   holding fifteen options, each row showing its type, its description and its
   `Default:` line. Switch to the `JSON` tab, change `count` to `3`, switch back:
   the numeric field reads `3` and the estimated cost has changed to `120000` micro
   units. Press `Run`. The output panel renders three structured cards.
6. **An invalid input is refused inline.** On `orchard/quickdraw-2`, clear the
   `subject` field and set `count` to `9`. Press `Run`. The page keeps the reader
   where they are, marks both controls invalid, puts one message under each naming
   the field, moves focus to `subject`, and writes no prediction row. The `Run`
   control stays enabled throughout.
7. **A cold run is cancelled before it starts and is never billed.** Open
   `blackpine-labs/prism-2-flex`. The badge reads `Cold` and names its load time.
   Press `Run`. The output panel shows the booting state and the sentence naming
   `12` seconds. Press the cancel control. The panel moves through `canceling` to
   `canceled`. Open `/account/usage`; the period total is unchanged and no row
   exists for that prediction.
8. **A repeated create charges once.** Send two creates for `northlight/scribe-2`
   carrying the same `Idempotency-Key` and the same body. The second returns the
   first prediction unchanged. `/predictions` shows one row, and `/account/usage`
   shows one usage row and one charge.
9. **The spend cap stops the next run.** Open `/account/usage` and set the monthly
   cap to a value below the month to date spend. Return to `northlight/scribe-2` and
   press `Run`. An inline banner appears above the form reading
   `This run would take you over your monthly limit of $2.00. Raise the limit or wait until the period resets.`
   with a link that opens the cap control. No prediction row is written. The same
   create sent to the machine interface is refused with the same error type.
10. **Another account cannot read this one's work.** Sign out, sign in as
    `member2@example.com`, and request the prediction identifier from journey 3
    directly at `/predictions/<id>`. The answer is the not found page, not a
    refusal. Request `arden-hale/notes-tidy`; the answer is the same.
11. **An author publishes a model.** Open `/models/new/identity`, give the owner
    `arden-hale`, the name `notes-tidy-2`, a description and a licence, and
    continue. On `/models/new/packaging` paste the packaging document and the
    predict signature, and continue. `/models/new/review` shows the derived input
    schema, the derived output schema and the digest. Confirm. The model page
    opens, the version list holds one row, and submitting the identical packaging
    document again returns the same digest and adds no second row.
12. **A deployment is released and rolled back.** Open
    `/deployments/arden-hale/tidy-live`. Change the pinned version and save. The
    release log gains a row naming the actor, the instant and both versions. Press
    rollback on the previous row. A new release row is added pointing back at the
    earlier version, and no release row is removed or edited.
13. **A revoked token stops working at once.** On `/account/tokens`, open the row
    menu for `laptop` and choose revoke. Type the token's name to confirm. Send a
    create with that token. It is refused, and the refusal is the same shape a token
    without the `run` scope receives.
14. **An owner manages membership.** Sign in as `owner@example.com`, open
    `/northlight/settings/members`, and change `arden-hale` to `owner`. The row
    updates and the audit log gains an entry naming the actor, the before value and
    the after value. Attempt to remove the only remaining owner; the control refuses
    and the membership rows are unchanged.

### States

- Every list has an empty state that says what would be there and what to do next.
  `/predictions` before the first run shows the run form bound to
  `northlight/scribe-2` with an example prefilled, not an illustration.
  `/deployments` with none shows one line and a link to `/models/new/identity`.
  `/account/tokens` with none shows one line and the create control.
- Every list and every panel has a loading state that occupies the final geometry, so
  nothing shifts when the content lands. A card awaiting its cover shows a sweep
  across the card's exact final shape, never a spinner and never a collapsed box.
- Feedback for a completed or refused action is an inline banner placed directly
  above the region the action belongs to, never a floating toast and never a full
  page interstitial. The banner states what happened, names the field or the record
  it concerns, and stays until it is dismissed or the reader navigates.
- An error never crashes the page. A failed fetch leaves the surrounding page
  readable, states what failed, and offers the action again. A server error renders
  a stable page carrying the request identifier.
- A withdrawn version renders the form disabled with the author's reason beside it
  and a link to the version list.

## UI/UX notes

**The north star.** A developer should understand, within the first screen, that
this is a shop where somebody else's machine runs somebody else's model and the
price is printed. Comprehension first, atmosphere second.

**The register, and why it changes halfway down.** The product runs two visual
registers on purpose, and blending them produces something that reads as neither.

The **poster register** is a saturated corner to corner wash running from a light,
vivid violet through a mid, vivid red into a light, soft amber, overlaid with a fine
dot halftone that is denser at the edges than in the middle, so the surface reads as
printed rather than rendered. White type sits on it carrying a hard offset shadow
with no blur, which is what makes it read as ink printed slightly off register
rather than as a web gradient. It appears in the home hero, the featured catalogue
card and nowhere else above the footer. The halftone is drawn, never loaded: it is a
repeating pattern of small circles, tiled tightly, multiplied over the wash.

The **document register** is a near-white neutral ground, deep neutral ink,
hairline near-white neutral rules, monospace for every identifier, no shadow on
anything, and generous line height. It is everything else: the catalogue lists, the
model page, pricing, the console, the legal routes.

The switch between them is abrupt. On the home route the wash ends at a hard
horizontal edge and the next block begins on the document ground. There is no fade,
and adding one reads as an accident.

**Palette by role.** Every colour in the interface resolves through a named role, and
no colour is mixed at a use site. The page ground and the raised card ground are
both near-white neutrals, the card ground a shade above the page. Body ink is a deep
neutral and is the most used colour in the product. Secondary ink, which carries
every metadata line, is a mid neutral and appears wherever a value is subordinate to
the thing it describes. Rules and dividers are a near-white neutral, always one
physical hairline and never a shadow standing in for a border. The brand accent is a
mid, vivid red used flat for run counts and for links inside the document register,
and the wash itself is reserved for surfaces and never for text. A mid, soft teal
inside a light, muted green ring is the live status mark and appears nowhere else.
Cost emphasis is a deep, vivid orange on a near-white, muted amber band, used on the
pricing route and on a spend warning. The destructive and required mark is a mid,
vivid red at a darker step than the accent, and it is what the required marker on
every form control wears. An informational cross reference inside long prose is a
mid, vivid blue. Anything lighter than a mid neutral is a border or a disabled
state and is never text. The exact shades are yours, so long as each role keeps its
exclusivity and each pairing clears the contrast bar below.

**What the palette must not become.** No surface is allowed to be a single hue
family with no second signal, and no status is carried by colour alone: the live
mark pairs its colour with a word, the required marker pairs its colour with a
visible asterisk and a programmatic required state, and every chart pairs its series
with a direct label.

**Type.** Three families, and each has one job.

Typography carries three families. The body face is a geometric grotesque with
squared terminals, shipped at regular, medium, semibold and bold, with a regular
italic and a semibold italic.

| Role | Family | Stack |
|---|---|---|
| Body and interface | `Space Grotesk` | `Space Grotesk, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif` |
| Every identifier | `JetBrains Mono` | `JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` |
| Display headlines only | `Fraunces` | `Fraunces, Space Grotesk, Georgia, serif` |

The scale, which is fixed rather than fluid, so prose stays readable at every width
and nothing is sized against the viewport:

| Size | Weight | Line height | Role |
|---|---|---|---|
| `16px` | `400` | `24px` | Body |
| `14px` | `400` | `20px` | Secondary body, metadata, table cells |
| `12px` | `400` | `16px` | Badge text, captions, keyboard hints |
| `18px` | `400` | `32px` | Long form prose |
| `16px` | `400` | `20px` | Dense body inside a card |
| `14px` | `600` | `20px` | Emphasis in a metadata line |
| `18px` | `600` | `32px` | Long form subheads |
| `16px` | `600` | `24px` | Card titles |
| `24px` | `400` | `35px` | Section subheads |
| `24px` | `600` | `32px` | Section heads |
| `20px` | `500` | `28px` | Panel heads |
| `36px` | `600` | tight | Route title |
| `48px` and `60px` | `400` | tight | The two marketing head steps |
| `72px` | `400` | `0.95` | The home hero, stepping down one step on a narrow viewport |

Available weights are `400`, `500`, `600` and `700`. Tracking is `-0.025em` on
display sizes and `0.05em` on the small upper case labels of the catalogue tab
strips. Fallback faces are metric adjusted so that the swap does not reflow the
page.

**The monospace rule.** Every identifier a person could type or paste is set in the
monospace family: model addresses, version digests, token prefixes, hardware class
names, field names in the run form, rates and durations. Prose is never monospaced.
This single rule does more for legibility here than any other decision in the
system.

**Shape and elevation.** Corners are square on every catalogue card, every table cell
and the hero panel, softened only slightly on buttons, inputs and code blocks, a
little more on menus, and most on a dialog. Badges, status chips and avatar marks
are fully rounded. The document register has no shadows at all: a thing that looks
raised is raised by a hairline border and a marginally whiter ground. Four shadows
exist in the whole product and each has one job: a ring around a small pill badge, a
ring around a focused form control, a ring around the live status dot, and a single
lift under the floating code panel in the home hero.

**Density.** The document register reads compact where a person is scanning and
comfortable where they are reading. A console table sits tight enough that a full
page of run history fits one screen without scrolling past the filters, while long
form prose is given room. Space over dividers: sections read as separate because of
the room around them, not because a rule was drawn between them.

**Motion.** This is a restrained product wearing a loud skin. The colour is loud and
the motion is almost absent, and that restraint is what makes a page of forty model
cards read as a directory rather than as a showreel. The default is a quick,
symmetrical colour change on point and on focus, applied to text colour, background
colour, border colour and underline colour together and never to every property at
once. Marketing surfaces use a slower version of the same curve where a hover
changes a large area. Beyond that there are exactly five moments that move, and a
build that adds a sixth has changed the design rather than enhanced it: content
that arrives after a fetch fades in; a card waiting for its cover carries a sweep
across its final shape; a busy indicator turns; the live status dot pulses once and
settles; and a refused form submission nudges sideways by a single hair and back,
small enough to register as a refusal and too small to read as a cartoon. The home
hero runs one composed cycle, and it is the only thing that plays without being
asked: a ring fills over ten seconds, the next sample types itself into the code
panel, the output beside it cross fades, and its caption swaps a little faster. The
cycle pauses when the document is hidden and when the pointer is over the panel.
Motion is never tied to scroll position anywhere in the product: there is no
parallax, nothing is pinned while the page moves behind it, and nothing reveals on
entry. Content is present when the document is.

**What must not move.** The model list, the run form as it renders from a schema, the
pricing table and long form prose. People are reading or filling those in.

**Reduced motion.** Under a reduced motion preference the hero cycle freezes on its
first sample with manual paging controls and the ring hidden, the rails become
ordinary horizontally scrollable lists with a visible affordance, the sweep and the
pulse are replaced by a static tint at their midpoint, and the status dot stays
solid. The quick colour change on hover is kept, because a fifteen hundredth of a
second colour change is not what the preference is asking about and removing it
makes the interface feel broken rather than calm.

**Layout.** Console routes carry a persistent left sidebar naming the console
sections, and the sidebar is the navigation model for everything behind sign in.
Public routes carry the top header instead: an announcement band, then the wordmark,
the search combobox, the menu, the sign in link and one primary action. The working
surfaces are split panes. On the model page the run form sits in one pane and the
output panel in the other, and the output pane stays in view while a long form
scrolls. In the console a filtered list sits beside the detail of the selected row,
and selecting a row updates the address so the state can be sent to somebody else.
The header sticks once the announcement band has scrolled away, and a link to a
heading lands that heading below the header rather than under it.

**Components and their states.** Every interactive element has a resting, pointed at,
pressed, focused and unavailable state, and unavailable is never signalled by colour
alone. A solid button empties on hover rather than darkening: its ground goes
transparent and its text and border take the ink colour. An outlined button tints
its ground faintly and moves its border to the ink colour. A clear button gains a
faint ground and nothing else. Escape closes any menu, popover or dialog and returns
focus to the control that opened it. A destructive action confirms first, and the
confirmation names the thing being destroyed.

**Mode and theming.** The product commits to both a light and a dark theme, plus a system
setting, switched from a three way control in the footer status bar. The theme is
carried on the root element, and every colour resolves through a role rather than a
literal, because two hard coded colours anywhere make a dark theme impossible to
finish. The dark theme inverts the roles of the neutral ramp rather than the hues:
the lightest ground becomes the darkest and the darkest ink becomes the lightest,
and every other family gets its own dark ramp at the same steps. The system setting
follows the operating system and updates live without a reload. The choice is stored
where the server can read it, so the first paint is already in the right theme; a
theme that flashes light before turning dark is worse than having no dark theme. The
poster register does not invert: the wash is the same in both themes and the type
over it stays white. Generated output is never filtered or dimmed by the theme,
because a model's output is content.

**Accessibility.** Body text and its ground meet WCAG AA in both themes, and the
white type on the wash is carried by its hard shadow, which is an accessibility
mechanism rather than a decoration and must not be dropped. One visible focus
indicator is used everywhere, a two hair ring in the ink colour offset from the
element, inverted over dark and over the wash; it is never removed, including after
a mouse click. Full keyboard navigation reaches every control, including the copy
controls, the card lift and the rails. Every touch target on a coarse pointer is at
least `44px`. Every icon only control carries an accessible name on the control
rather than on the icon, and every decorative icon is hidden from assistive
technology. Every content image carries alternative text naming what it shows, and a
model cover's alternative text names the model address; a purely decorative graphic,
including the halftone and the gradient rails, declares itself decorative and carries
no alternative text. One first level heading per route, no skipped levels, and the
home hero's display line is that heading rather than the sentence under it. Landmarks
are declared for the banner, the navigation, the main region, the complementary rails
and the footer, and the two catalogue columns are labelled regions, because a column
position is not something a screen reader user can perceive. A skip link is the first
focusable element on every route and moves focus to the main region, which matters
more here than usual because the header holds a combobox and six menu items.

**Live regions.** A prediction's status change is announced politely as a status
transition only, never as the output content. Streaming output is not a live region:
the panel announces that output is arriving and the finished text is available as
ordinary content afterwards, because announcing every token is unusable. A queue
position is announced on change and no more than once every ten seconds.

**Responsive behaviour.** The layout is mobile first with one decisive breakpoint at
the tablet tier and a second at the wide tier. At the narrow tier everything is a
single column with a comfortable gutter, the header collapses to the glyph with a
truncated search field and a menu disclosure, every tab strip becomes a select, and
every console table becomes one card per row with the primary identifier as its
title. At the tablet tier card grids go to two columns and the wordmark returns. At
the wide tier the model page splits into its two panes, the catalogue shows its
paired columns, and the output pane becomes sticky. Beyond that the containers stop
growing and the gutters absorb the rest.

Two responsive decisions are load bearing. The catalogue does not simply stack its
two columns in source order at narrow widths, because stacking makes that route more
than three times taller than it needs to be; it interleaves them instead, as the
featured card, then the first few popular models, then the rest of the popular list
behind a show more control, then the collections, one collection per screen. And on
the model page at narrow widths the output pane sits above the run form, so the
first thing a reader sees is what the model produces rather than the questions it
asks, with the run control pinned above the keyboard inset and inside the device
safe area.

Every hover effect is gated on a fine pointer, so a tap never leaves a card stuck
looking hovered. The rails pause on hover for a fine pointer and become ordinary
scroll containers under touch.

## Front-end specification

This section carries the visual and interaction detail that `## UI/UX notes` states
as direction. Where the two could be read as disagreeing, `## UI/UX notes` governs
the intent and this section governs the arrangement.

### Iconography

Every symbol in the product is drawn geometry rather than a loaded picture, and no
icon package or icon font is used. Two coordinate systems exist and are kept apart,
because their stroke weights are not interchangeable: interface icons are filled
paths on a large square grid with their weight expressed as path thickness, and
editorial icons are stroked paths on a small square grid with round caps and joins
and no fill. Icons inherit their colour from the text around them and are never
given a colour of their own, which is what lets them survive the dark theme.

The interface set is closed and named: a caret pointing right for the announcement
band's link, a caret pointing down for menu and select triggers, a close mark for
the band's dismiss control, a filled dot for the model status chip, a horizontal
rule for list separators and for an empty value, a play mark inside a circle for a
cover that carries motion, a lightning bolt on the primary call to action and on the
catalogue's latest tab, a prohibit mark for the zero training data handling badge,
an arrow rising into an arc for the rerun control, and a cog for the settings entry.
The editorial set is four: a copy mark built from two overlapping rectangles, a
document mark with ruled lines, a terminal mark with a chevron, and a globe with one
horizontal line and a meridian.

The determinate progress ring is a primitive rather than an icon and is the only
determinate wait indicator in the product. It is two stacked circular paths of equal
stroke weight, a track and a value, with the value driven by the length of its own
dash rather than by a rotation, so the fill reads as elapsed time instead of as a
spinner. Its timing is always linear, because an eased clock is a lying clock. Where
no duration is known the ring is replaced by a turning partial arc, which is
visually distinct on purpose. The ring is reused for any determinate wait longer
than two seconds, including a queued prediction whose position is known.

The brand mark is two related assets and both are pure geometry. The glyph is three
polygons forming a stepped bracket, reused by reference rather than duplicated per
instance, carrying a title element naming the product, and it stays legible at
favicon size, which the three polygon construction satisfies and a detailed mark
would not. The wordmark is the same three polygons followed by the letterforms of
the product name.

### The global chrome

Three bands sit at the top of every public route and their combined height is the
sum of two tokens, kept separate because the first band can be dismissed and the
header must reflow when it goes. The header's sticky offset reads those tokens and
never a constant, and the scroll padding that keeps an anchored heading clear of the
header reads the same value, so a link to a heading lands correctly whether the band
is present or not.

The announcement band centres a small square publisher mark, the promotional line
and a caret, with a dismiss control at its right edge. Its ground is a blurred
backdrop over whatever the route's hero is, so it tints rather than covers. Its link
gains an underline on hover. Dismissing it removes the band and reflows the header
upward as a height change rather than a display change, so the page does not jump.
The dismissal is remembered per browser for the life of that promotion and is keyed
by the promotion identifier, so a new promotion reappears for somebody who dismissed
the previous one. Every route renders correctly with no band at all.

The header carries the glyph and the wordmark at its left, then the search combobox,
then a menu of six items reading `Explore`, `Pricing`, `Docs`, `Blog`, `Changelog`
and `Sign in`, then a solid primary action carrying the lightning icon and the label
`Try for free`. The wordmark hides at the narrow tier, leaving the glyph. The
combobox is a short field with a hairline border, the placeholder naming two example
queries, and a keyboard hint rendered as two key elements holding the platform
modifier and the letter. The hint is computed from the platform, showing the command
symbol on Apple hardware and the control word elsewhere.

On a route whose hero is the poster wash the header paints no solid ground. A
backdrop element behind it carries a soft white radial fade with a light blur, which
lifts the header's dark type off the wash without drawing a bar across it. On a
document register route the same element is present with every stop fully
transparent, which is how the treatment is switched off without switching
components.

At the narrow tier the menu is replaced by an outlined control labelled `Menu`
opening a disclosure panel holding the same six links in the same order, the primary
action styled as a full width link, a rule, and one promoted item. Focus moves into
the panel on open, is trapped while it is open, and returns to the trigger on close.
Escape, a click outside and a navigation all dismiss it. The document behind is
locked while it is open and the lock does not shift the layout by the width of the
scrollbar. The trigger carries its expanded state and the panel is a labelled
region.

The footer opens with a band of three diagonal stripes carrying the poster wash,
which is the only place the wash appears at the bottom of a page and is what returns
the document register to the poster register before the page ends. Below it the
wordmark sits at the left beside three labelled columns. `Product` holds `Explore`,
`Pricing`, `Docs`, `Blog` and `Changelog`. `Community` holds `Commons`, `Feed` and
`Sourcehub`. `Company` holds `Home`, `About`, `Changelog`, `Join us`, `Terms`,
`Privacy`, `Status` and `Support`. A full width rule closes the footer, and under it
sits a live platform status indicator at the left reading `All services are online`
behind the status dot inside its ring, and a three way theme control at the right
offering system, light and dark. The status indicator reads a real status record and
has three states: all services operational, degraded, and incident. A degraded or
incident state names the affected component and links to the status page. An
indicator that is green because it was hard coded green is worse than no indicator,
because it is consulted exactly when the product is broken. Footer links move their
colour and their underline from the secondary ink to the body ink on hover.

### Scroll, sticky and the rails

Four things stick and no others: the header once the announcement band has scrolled
away; the run form's footer at the bottom of the input pane, with a ground that
masks the scrolling content at its left and right edges; the console sidebar, which
scrolls independently and marks its active entry; and the output pane on the model
page at the wide tier, so a long input form does not scroll the result off screen.

Two horizontal rails of model cards run on the home route in opposite directions at
walking pace, taking roughly a minute and a half to complete one lap. Both rails
share one movement definition, and the second sets its start and end in reverse
rather than running a negative direction. The card group is duplicated so that the
loop is seamless, the duplicate is hidden from assistive technology, and without
that hiding a screen reader announces every model twice. The rails pause when the
pointer is over them and when focus is inside them. The rail must be operable with
the movement switched off: it is a horizontally scrollable region with keyboard
scroll support and the movement is a decoration on top of that, because a rail
implemented as movement alone is a rail no keyboard user can reach the end of.

Nothing fades in on first paint. Server rendered content is visible immediately, and
content that arrives later fades in once. Anything with a known shape shows a
skeleton at that exact shape rather than a spinner, so the layout does not shift when
the content lands, and every image and every media box declares its
intrinsic dimensions or an aspect ratio before its bytes arrive, so the space
reserved for it is already correct. Back navigation to a catalogue list restores both the scroll
position and any pages already loaded, or a reader loses their place after every
model they open. Switching tabs inside the model route does not scroll, so the
model's header stays in view. Opening a prediction from a list pushes a history entry
so that back returns to the list where it was. A link to a heading inside a long
document moves focus to that heading, so the next keyboard step continues from
there.

Any route whose document runs longer than roughly twenty screens either paginates or
windows its list, mounting entries within one screen of the reader and unmounting
them outside it, with a jump control and an address per entry so a link to an old
entry does not require scrolling past everything above it. A legal route is the
exception: it stays one continuous document so it remains selectable, printable and
findable with the browser's own find, and it gets a sticky table of contents and
nothing else. An accordion over legal text is a dark pattern.

### The model card, in detail

The frame is a hairline border on a near-white ground with square corners and no
shadow. The cover fills its side of the frame and bleeds to the frame's own edge
with no inset and no rounding, square on the rail and list variants and widescreen
on the featured variant. The restraint of the frame is what makes the cover read as
content rather than as decoration. The owner sits in secondary ink at the secondary
body size and truncates with an ellipsis at the container width. The model name sits
in body ink at the card title size and truncates independently. The separator is a
literal `/` inside a span that preserves its space, never a border and never a
generated pseudo element, so the address copies correctly when a reader selects it.
The description is secondary ink at the secondary body size, clamped to two lines on
the rail variant and one on the list variant. The run count is monospace at the badge
size in the brand accent, followed by the word `runs` in secondary ink. Badges sit on
a footer rule as fully rounded pills with a ring and badge sized text.

The states are designed rather than defaulted. Loading shows the card's exact final
geometry with the sweep moving across the cover, the title and the description.
A model with no cover gets a generated field keyed by a hash of its address, so the
same model always draws the same placeholder, and the placeholder carries a subdued
corner label saying it is a placeholder, because presenting a generated gradient as
a model's own output misrepresents the product. Hover lifts the card by a small
translation and moves its border to the ink colour, and this lift is the one place
in the product where a transform is used decoratively. Focus rings the card rather
than the inner link. A model whose only version is withdrawn renders with its cover
desaturated and a `Withdrawn` badge, and its link still resolves, because a dead link
is worse than an explained one.

The badge set is closed and adding to it is a schema change, which is the point.
`Official` means published by the organisation that made the model and wears a
neutral ring with a check mark. `Warm` means at least one instance is loaded, and
wears the status dot inside its ring with a single pulse. `Cold` means no instance is
loaded, and the model page prints the measured load time beside it in words a reader
can act on rather than in jargon. `Priced by multiple properties` means the model is
not billed by time alone and links to the pricing route. `Data privacy` and
`Zero training` are data handling commitments, each linking to the clause that
defines it, and the second wears the prohibit mark.

### The run form and the output pane, in detail

Each generated field renders as a row: the type glyph, the field name in monospace,
the required marker in the destructive red where the field is required, the declared
type in the body face in secondary ink, then the control, then the description, then
the `Default:` line printing the default as JSON. Where the schema supplies a human
title that title is the visible label and the machine name becomes the secondary
line; the description is associated as a description rather than as a label so it is
announced after the field rather than instead of it, and the type and default are
announced through it, because a bare type name tells a listener nothing. The required
marker is hidden from assistive technology so it is not read as punctuation, and the
programmatic required state carries the meaning. An enumeration with more than a
handful of members is a select rather than a group of radios, because a fifteen
option radio group is worse for everybody.

A rejected submission moves focus to the first invalid control, puts a summary at the
top of the form linking to each invalid control, marks each control invalid and
points it at its own message, announces the messages politely on blur and assertively
on submit, and nudges the form once. The submit control never disables.

The five input tabs collapse to a select at the narrow tier, which is the pattern
every tab strip in the product follows. The output pane carries two tabs, `Preview`
and `JSON`. The elapsed label `Generated in` sits above its value, set large,
immediately under the output. The action row sits under that. The logs disclosure
reads `Show logs`, is monospaced at the badge size, scrolls inside its own container,
follows the tail while the run is active and detaches when the reader scrolls up.
Log volume is capped per prediction and the cap is stated in the interface when it is
reached.

### Route compositions

**Home, signed out.** Eight blocks, and the register changes twice. The hero in the
poster register: the display headline split so its second line can be styled
separately, reading `Run` `AI` on one line and `with an` `API` `.` on the next,
white on the wash with the hard offset shadow; a subheading in white reading
`Run and fine-tune models. Deploy custom models. All with one line of code.`; and a
solid primary action reading `Get started for free`. Beside it, a floating panel in
the document register carrying the snippet lift, holding a tab strip of `Node`,
`Python` and `HTTP` and a highlighted sample that names the client library, reads the
credential from an environment variable, declares a model address and an input
object, and awaits a single call. The sample must be real, runnable code for the
model currently shown in the output card beside it, produced by the same generator
the run form's snippet tabs use. The progress ring sits at the panel's right,
counting the ten seconds to the next sample.

The output card beside the panel shows the current sample's own output bled to the
panel's edge, with a caption in white semibold at its lower left carrying a soft
shadow, and beneath the caption the model address in monospace at the badge size on a
blurred backdrop so it stays readable over anything. Each caption's model address is a
link to that model's route, and the card itself is not a link, because a card link and
a caption link would compete. The rotation holds five samples, each pairing the caption named in the copy deck
with the seeded model that produced it, and each caption's model address is its own
link. It never shows a broken
frame: a sample whose media cannot be produced is skipped to the next one.

Then the document register begins at a hard edge: a line reading
`With Modelport you can` followed by a single select group of seven chips reading
`Summarise text`, `Extract structured data`, `Rewrite text`, `Caption text`,
`Classify text`, `Translate text` and `Large Language Models (LLMs)`. The group is a
real radio group with a group label and arrow key movement between chips, its
selected state is not carried by colour alone, and selecting a chip reorders the
already loaded rails on the client rather than fetching, so the rails never stall.
Then the two rails, then a solid `Explore models` and an outlined `Push a model`. The
second is the only place on the home route that addresses model authors and must not
be dropped.

Then `How it works`, three numbered steps in the document register each pairing a
paragraph with a real code sample, flanked at both page edges by narrow vertical rails
carrying the wash, which is what keeps the colour present while the content is dark
on light. Then `Deploy custom models`, two code blocks and a paragraph: the first
block is the packaging configuration naming the base environment, the system
packages, the language version, the packages and the predictor entry point, and the
second is the predictor class itself, with a setup method that loads weights once and
a predict method whose typed signature becomes the input schema.

Then an inverted panel on a deep neutral ground with headings and figures in the brand
accent and body copy in white, holding four cells. `Automatic scale` pairs its claim
with a bar histogram of request volume. `Pay for what you use` pairs its claim with a
monospaced rate list, one row per hardware class with its per second price, ending in
a link to the pricing route. `Forget about infrastructure` pairs its claim with a
treemap of packed rectangles. `Logging and monitoring` pairs its claim with a line
chart labelled `Prediction throughput (requests per second)` over a two hour axis.
Every one of those charts renders from real values: the rate list reads the hardware
catalogue and the throughput chart reads a public aggregate. A cell whose value cannot
be served renders without its chart rather than with an invented one. The charts are
decorative for assistive technology and their content is stated in the adjacent copy,
which is why the copy names the numbers.

Then the close: a large display call to action, a short paragraph naming the product
and its parent organisation, a solid `Get started` button, the stripe band and the
footer.

The home route degrades honestly. If the catalogue is unavailable the rails render
from a cached snapshot with a subdued freshness note and the hero is unaffected,
because the hero is the pitch and must survive a catalogue outage. With script
disabled the hero, the copy, the first screen of both rails, both catalogue actions,
every code sample and the footer all render; only the rotation and the chip filter
are lost.

**Explore.** The title, then the two labelled columns, then the collections band,
which is the largest region on the route. Each collection is a display sized heading,
a one line description written as a use case, three model references and the
remainder count. Tabs are small upper case labels with wider tracking, an icon at the
left and an underline on the active tab; they are real tabs, so arrow keys move
between them, the panel is labelled by its tab, and the selected tab is reflected in
the address so a link can open the route on a chosen tab. Loading shows card
skeletons at final geometry in both columns. An empty search inside a collection
falls back to that collection's own description and its full list rather than
rendering blank. A stale ranking renders from the last computed snapshot with no
visible difference, because a slightly stale ranking is not an error condition.

**Pricing.** The title `Pricing`, then one paragraph stating the whole model in two
sentences, then three anchored subsections in this order and no other: public models,
private models, hardware. The public subsection carries prose and a worked table of
real models with their real prices, read from the model records rather than typed
into the page, each row an inline model reference with its description and its price
in monospace with the unit in secondary ink. The private subsection states plainly
that a private model runs on reserved capacity rather than a shared queue, that
billing therefore covers setup time, idle time and active processing rather than
active processing alone, that capacity scales with demand, and that a fast booting
variant is the one exception and bills only for active processing. That exception is
stated in three places or it will surprise somebody: the version list, the deployment
creation form and the invoice line. The hardware subsection is one row per class with
its display name, its class identifier in monospace, its rate per second to six
decimal places in monospace, its rate per hour in secondary ink derived from the per
second rate rather than stored separately, its accelerator, its processor count, its
accelerator memory and its memory. At the narrow tier it becomes one card per class
with label and value pairs, because a nine column table cannot be made to work on a
phone. The page also states three things a build tends to drop: that queue time is
never billed, that a per model estimate is on each model page, and what the free
allowance for a new account is, in the same units as the rate table.

**Owner profile.** A header carrying the avatar, the display name, the handle in
monospace, a one line description, a source link and a total run count across the
owner's models; then that owner's models as list cards ordered by rank score with a
filter for output type and a sort control offering newest and most run; then any
collections the owner curates. An owner with no public models renders the header and
one honest line, because a handle may exist for an account that only runs private
models. The route serves a person and an organisation alike and must not assume
which.

**Not found and the error surface.** A model that cannot be found states the address
that was tried, offers a search for the model's name and lists the three nearest
matches from the catalogue, because a mistyped model address is the most common way
to land here and a generic page wastes it. An owner that cannot be found does the
same, scoped to owners. A private model a reader may not see renders as not found
rather than as a refusal. A withdrawn model is not a not found: it renders with its
withdrawal reason and its version list. A server error renders a stable page carrying
the request identifier, which is what support will ask for, plus a link to the status
page. No raw stack trace and no framework error overlay ever reaches a reader. Both
pages keep the global chrome, because a reader who lands on a not found still needs
the search control that would fix it.

**The console.** Every console route carries the left sidebar, which lists
`Dashboard`, `Predictions`, `Tokens`, `Usage`, `Billing`, `Deployments`,
`Organisations` and `Publish a model`, marks the active entry, and collapses to a
disclosure above the content at the narrow tier. The dashboard answers three
questions in this order and the layout expresses that order at every width: what did
I run recently and did it work, what am I spending and how close am I to the limit I
set, and what should I run next. Its regions are a run bar bound to the last model
used and collapsed to a single input and a submit; the ten most recent predictions
with their output preview, model address, status pill, duration and cost; the month
to date spend against the cap with a bar and the days remaining in the period; the
deployments with their instance count, queue depth and error rate over one hour; and
three curated collections. Before the first run, the recent runs region shows the run
form bound to a small fast model with an example prefilled rather than an
illustration, and the spend region shows the free allowance remaining rather than a
zero.

The recent runs region reflects a prediction reaching a terminal state within two
seconds of it doing so, without a page reload. One live connection is held per tab
and not one per row, carrying status frames the client merges by identifier into
whatever it already holds. Where the live connection is unavailable the client falls
back to polling at a fixed interval that backs off, and the fallback is visible in
the interface as a subdued freshness note rather than hidden. A reader with eight
tabs open must not hold eight connections: either the connection is shared between
same origin tabs, or it is dropped for a tab that is not visible and resumed when it
becomes visible again. The build states which of the two it does.

Console tables are cursor paginated and virtualise past a threshold, charts are
downsampled to the width being drawn, and the usage screen renders the current period
from precomputed rollups rather than from raw rows, because summing millions of rows
on the transactional path is how a usage screen takes half a minute.

### Drawing everything, loading nothing

This is a zero-asset build, and every substitution below is deliberate. No picture,
font file, typeface file or sound is supplied with this brief, and none is needed.
Typefaces are named and loaded from an open provider rather than shipped.

The halftone over the wash is an inline repeating pattern of small filled circles,
multiplied over the gradient. The dots densify towards the frame edges, which is
achieved by laying a second, coarser pattern over the first and masking it with a
radial fade whose opaque end is at the edge.

The generative field behind the company statement is a stack of three soft ellipses
in the wash's own violet, red and blue, on a near-white ground, drifting slowly
against each other under a heavy blur so the stack reads as one moving mass rather
than as three shapes. It drifts rather than loops: one pass takes at least a minute.
Under reduced motion and at the narrow tier a single static frame of the same stack
is what renders.

A publisher mark is a generated monogram: the handle's first character in the display
face, white on a ground whose hue comes from a hash of the handle at a fixed
saturation and lightness, so every publisher is distinguishable and no two adjacent
cards collide. It is square with the button rounding and carries no border, and a
generated monogram is never inverted; the inversion flag applies only to a supplied
mark.

An account avatar is generated from the account identifier: the handle is hashed to a
hue, then a small square cell grid mirrored on its vertical axis is filled at a fixed
density, the ground the hue at a high lightness and the cells the same hue much
darker. It is emitted inline rather than requested, so it is stable, distinguishable
in a list and costs no round trip.

A model cover is a generated field seeded by the model address: a two stop gradient
drawn from the palette roles, overlaid with the halftone at low opacity, with the
model's name set in the display face at the lower left. The same address always
produces the same cover. Example outputs use the same generator at a different seed
per example with the example's input as its caption. Every generated cover carries a
subdued corner label saying it is a placeholder.

A customer mark on a marketing surface is the company's name set in the display face
at one optical size in secondary ink at reduced opacity, because a row of wordmarks
in one weight reads as a logo wall and avoids inventing eight fake logos.

Only three font files load before first paint, and both faces used above the fold are
preloaded with metric compatible fallbacks so the swap does not reflow. Every third
party script is deferred and none blocks first paint. Route level splitting keeps the
run form and the output renderers on the model route alone, and the generative field
loads only on its own route, only above the tablet tier, and only when reduced motion
is not requested.

### Copy deck

Every string below is fixed. Where a value varies it is written as a name in angle
brackets.

| Slot | Copy |
|---|---|
| Announcement band | `Summarise more for less this week` |
| Search placeholder | `Search 'best summarising models' or 'text to structured data'` |
| Header primary action | `Try for free` |
| Narrow tier menu trigger | `Menu` |
| Status bar | `All services are online` |
| Home headline fragments | `Run` `AI` / `with an` `API` `.` |
| Home subheading | `Run and fine-tune models. Deploy custom models. All with one line of code.` |
| Home primary action | `Get started for free` |
| Home snippet tabs | `Node`, `Python`, `HTTP` |
| Hero rotation captions | `A poolside patio at sunset with vintage lounge chairs`; `A soft armchair shaped like a peeled banana`; `A woman relaxing in a french bookstore`; `A futuristic robot looking into the distance`; `An abstract painting of a sunrise` |
| Chip group label | `With Modelport you can` |
| Catalogue actions | `Explore models`, `Push a model` |
| Home section heads | `How it works`, `Deploy custom models` |
| Home step lead-in | `Then, you can run it with one line of code:` |
| Home code lead-ins | `First, define the environment your model runs in with Keg's config file:`, `Next, define how predictions are run on your model with predict.py:` |
| Inverted panel, one | `Automatic scale` / `If you get a ton of traffic, Modelport scales up automatically to handle the demand. If you don't get any traffic, we scale down to zero and don't charge you a thing.` |
| Inverted panel, two | `Pay for what you use` / `Modelport only bills you for how long your code is running. You don't pay for expensive accelerators when you're not using them.` |
| Inverted panel, three | `Forget about infrastructure` / `Deploying machine learning models at scale is hard. If you've tried, you know. API servers, weird dependencies, enormous model weights, accelerator toolkits, batching.` |
| Inverted panel, four | `Logging and monitoring` / `Metrics let you keep an eye on how your models are performing, and logs let you zoom in on particular predictions to debug how your model is behaving.` |
| Chart label | `Prediction throughput (requests per second)` |
| Panel link | `Learn more about pricing` |
| Home closing body | `Building with Modelport and Skylark, you can wake up with an idea and watch it hit the front page of the news by the time you go to bed.` |
| Home closing action | `Get started` |
| Explore title and tabs | `Explore`, `LATEST`, `POPULAR MODELS` |
| Explore remainder | `and <N> more` |
| Featured card action | `Get started` |
| Model copy control | `Copy` |
| Model tabs | `Playground`, `API`, `Examples`, `README` |
| Model panel heads | `Input`, `Output` |
| Model input tabs | `Form`, `JSON`, `Node.js`, `Python`, `HTTP` |
| Model output tabs | `Preview`, `JSON` |
| Textarea hint | `Shift + Return to add a new line` |
| Default line | `Default:` |
| Form actions | `Reset to default inputs`, `Run (ctrl+enter)` |
| Elapsed label | `Generated in` |
| Result actions | `Tweak it`, `Share`, `Download`, `Report`, `View full prediction` |
| Logs toggle | `Show logs` |
| Examples strip | `Examples`, `View more examples` |
| Integration lead-in | `Run this model in Node.js with one line of code:` |
| Install lead-in | `Install Modelport's Node.js client library:` |
| Install command | `npm install modelport` |
| Auth lead-in | `Set the MODELPORT_API_TOKEN environment variable:` |
| Pricing title and anchors | `Pricing`, `Public models`, `Private models`, `Hardware pricing` |
| Pricing lead | `You only pay for what you use on Modelport. Some models are billed by hardware and time, others by input and output.` |
| Sign-in head | `Welcome to Modelport.` |
| Sign-in legal | `By signing in, you agree to our terms of service and privacy policy.` |
| Run gate, anonymous | `Sign in to run this model. We will bring you back here with your inputs.` |
| Spend cap reached | `This run would take you over your monthly limit of $2.00. Raise the limit or wait until the period resets.` |
| Queue position | `Waiting for a machine.` |
| Cold start | `Loading this model onto a machine. This usually takes 12 seconds the first time.` |
| Output expiry | `This file will be deleted soon. Download it if you need to keep it.` |
| Output purged | `The output for this prediction has been deleted. The record of the run is kept.` |
| Token created | `This is the only time we will show you this token. Copy it now.` |
| Token revoke confirm | `Type the token's name to revoke it. Anything using it will stop working immediately.` |
| Deployment idle cost | `Keeping 1 instance warm on cpu-small costs about $2.16 per day, whether or not anything runs.` |
| Version withdrawn | `This version was withdrawn by its author on <DATE>. Reason: <REASON>.` |
| Not found, model | `We could not find <ADDRESS>. Here are the closest models we do have.` |
| Read-only mode | `We are in read-only mode. Runs already in progress will finish; new runs are paused.` |
| Cookie band | `We use non-essential cookies to remember your choices. Accept or decline.` |

## Technical requirements

The application is server rendered. Pages are produced on the server from Jinja
templates by a Flask application, and the browser receives complete HTML on first
paint. Interactive behaviour on top of that HTML is Alpine.js, attached to the markup
the server already sent, so the catalogue and the documentation surfaces remain
readable and navigable with script disabled. The model page's shell, its metadata and
its version schema all arrive in that first response, because the schema is what
draws the run form and a form that appears a second after the page has settled reads
as a broken page. The HTTP interface is served by the same Flask application under
the `/api` prefix on the same origin.

Data lives in PostgreSQL, which is already running as the `postgres` service and is
reached through the `DATABASE_URL` environment variable. Read both `DATABASE_URL` and
the app's public address from the environment; never hardcode a host, a port or a
credential.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor - the only backing services available in this environment are
PostgreSQL through `postgres`, and reaching for anything else is a contract violation.

Accounts authenticate with an email address and a password. Passwords are stored
hashed. A browser session is carried in a cookie marked `HttpOnly`, `SameSite=Lax`
and `Path=/`; the machine interface authenticates with a bearer credential in the
`Authorization` header. A token's stored form is a hash, never the value itself, and
a presented credential is verified by hashing what was presented and looking that up,
so verification is a single indexed lookup rather than a scan. Any comparison of a
secret is constant time. A refusal for an unknown credential and a refusal for a
credential whose scope is insufficient are indistinguishable in their body and in
their timing, because the difference between them tells a caller which guesses to
keep.

A revoked credential stops working everywhere within one second. A verification
result may be cached for at most sixty seconds keyed by the credential's hash, and
revocation publishes an invalidation that removes the entry at once; the sixty second
expiry is the backstop for a missed invalidation, not the mechanism. The same
invalidation path carries a membership removal, a model visibility change and a spend
cap change, because for all four a stale acceptance is a money or access problem
rather than a staleness problem.

`GET /api/health` returns `200` once the application is ready to serve.

Every request carries a request identifier, and that identifier appears in the error
body, in every log line for the request and in the interface wherever an error is
shown. Logs are one structured event per line carrying the request identifier, the
account, the route and the outcome, and never an input document, an output, a
credential or an email address. Three latencies are recorded separately on every
prediction, because a single end to end number hides which of them moved: the time
from creation to start, the time a cold version spends loading, and the model's own
run time. Only the last is billed.

The application seeds its own data on first start, and seeding is idempotent, so
restarting the application never duplicates a row.

Every response that varies by principal carries a private cache directive, and no
shared cache may ever store one. Anonymous catalogue and documentation responses are
cacheable. Prediction records, usage rows, invoices, tokens and private model
metadata are never cached at any layer.

Outbound fetches of an address a user supplied all go through one place. The scheme
must be `https`; the hostname is resolved first and refused when it lands in a
private, loopback, link local, multicast or metadata range in either address family;
the connection is then made to the address that was resolved, so a name cannot resolve
differently between the check and the connection; a redirect is re checked at every
hop against the same rules under a hop limit; no credential, cookie or custom header
is forwarded; and a byte ceiling, a connection timeout and a total timeout all apply
and are published.

Every response carries the standard security headers, including a policy forbidding
inline script, a policy denying framing on application routes, a referrer policy that
does not leak paths to third parties, and a content type policy that forbids
sniffing. Author supplied markdown is rendered through an allowlist sanitiser before
it reaches any page.

**Information architecture.** The top level namespace is the account namespace, so
the router resolves a single leading segment against the reserved list, then against
account handles, then answers not found. Handle resolution is the one place in the
product where an ambiguity has to be settled by a fixed order rather than by a
guess, and a renamed handle resolves through a permanent redirect so old links keep
working.

**The architecture, stated as boundaries rather than as processes.** The backend
divides into modules and no module reads another module's tables directly: accounts
and authorization; the catalogue of models, versions, collections and examples;
predictions and their admission; the run plane that executes a queued prediction;
metering; billing; delivery; and search. One authorization module decides every
`(principal, action, resource)` question and every entry point calls it; scattering
role comparisons through request handlers is what produces a cross account leak. The
money path has one writer. The front end mirrors that with three layers that only
depend downwards: primitives, then components that know about this product, then the
route compositions that fetch. No primitive imports a domain type and no component
below a route fetches, which is what lets the run form be the same component on the
model page, on the dashboard and in the examples gallery.

**Admission.** A create is admitted in a fixed order before anything is queued: the
credential is valid and its scope is sufficient; the model and version exist, are
not withdrawn and are visible to this principal; the input validates against the
version's schema; the idempotency key is checked; the spend cap and free allowance
are checked; and the account's concurrency for that hardware class is checked. A
failure at any of those is the caller's and is refused. A shortage of capacity is
the platform's and is queued with an honest status rather than refused.

**Autoscaling.** A deployment's instance count moves within its own bounds on queue
depth and queue age. The fleet behind every deployment moves more slowly, on the
aggregate queue age per hardware class, because acquiring capacity is slow; when the
warm buffer for a class is exhausted the product degrades honestly with longer
queues and truthful estimates rather than with silent failures.

**Caching and the file lifecycle.** Anonymous catalogue responses are cacheable and
everything that varies by principal is not. A prediction's output has a retention
window of one hour, after which a sweep purges it and sets `data_removed` on the
record; the record survives its own payload. Retention is enforced by that sweep and
verified by a second pass that samples expired keys and confirms they are gone,
because retention that is only a policy document is not retention.

**Notifications.** A spend threshold crossing, a token nearing expiry, a membership
change and a leaked credential each write an in product notification the account can
read, deduplicated per kind per period so a busy account is not notified hourly. No
notification body ever carries a credential, an input document or an output.

**Trust and safety.** A published model is somebody else's program description
rendered on a page this product serves, so author supplied markdown is treated as
hostile and sanitised, a report control sits on every output surface and every model
page, and a report is written to a durable record and queued for a person rather than
acknowledged and dropped.

**What must be measurable.** Telemetry is the three latencies per prediction, the
error rate by class, queue depth and queue age, and the delivery age and attempt
count per webhook endpoint. Alerting fires on what a customer feels rather than on
an internal curiosity: the create path's error rate, queue age above target, any
reconciliation difference at all, delivery age or dead letter growth, and an
invalidation that has fallen behind. Performance is budgeted rather than hoped for:
the catalogue and model routes reach their largest paint quickly, a form control or
a tab switch responds without a perceptible wait, the layout does not shift once
content lands, and the console's long lists stay flat as they grow.

**Rollout.** The build ships in phases, and the four things that must not be
deferred are row-level scoping, integer money, the audit chain and the idempotency
key on creation, because each is cheap now and a rewrite later.

Serve a production build. The application must survive the end of the session that
started it.

## Data model

Twenty five tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is
benchmark fixture data, not a secret. Hash it as normal; the exact literal
must work at login, and it must be written into `/app/USER_README.md`
alongside each account so a grader can sign in.

Keys are opaque sortable identifiers generated by the application, never a sequential
integer a caller could increment to probe for another account's records. Every
tenant owned table carries `account_id` as a real foreign key and it is the leading
column of the ordering that supports every list query over that table. Money is an
integer count of micro units in a column named with the suffix `_micros`, beside a
currency column holding `usd`. Instants are stored with their zone in a single zone
and rendered for the reader. Durations are stored as an integer count of
milliseconds. Enumerated values are constrained at the database level rather than in
application constants, because background work writes through the database too. Soft
deletion exists only where a grace period is promised.

### accounts

`id`, `handle`, `kind`, `display_name`, `email`, `avatar_seed`, `state`,
`created_at`, `deleted_at`. `handle` is unique without regard to case across every
row. `email` is required when `kind` is `user`, may be absent when `kind` is
`organization`, and is unique among users. `kind` is `user` or `organization` and is
set at creation and never changed. `state` is `active`, `suspended` or `deleting`.

### users_profile

`account_id`, `password_hash`. One row per account whose `kind` is `user`.

### sessions

`id`, `account_id`, `created_at`, `last_seen_at`, `expires_at`, `user_agent`,
`ip_hash`, `revoked_at`. A session is a server side record; the cookie carries only
its opaque identifier.

### memberships

`id`, `org_account_id`, `user_account_id`, `role`, `created_at`. `role` is `owner` or
`member`. The pair of account references is unique, so one user holds one role in one
organisation. At least one row with the role `owner` exists for every organisation at
all times.

### tokens

`id`, `account_id`, `created_by`, `name`, `prefix`, `last_four`, `token_hash`,
`scopes`, `expires_at`, `last_used_at`, `last_used_ip_hash`, `revoked_at`,
`rotated_from`. `token_hash` is unique. The clear value is stored nowhere.

### audit_events

`id`, `account_id`, `actor_id`, `action`, `resource_type`, `resource_id`, `before`,
`after`, `ip_hash`, `request_id`, `created_at`, `prev_hash`, `hash`. Rows are
appended and never updated or removed. `prev_hash` is the `hash` of the previous row
for the same account and `hash` covers the row's own content together with
`prev_hash`.

### models

`id`, `owner_account_id`, `name`, `visibility`, `description`, `licence`,
`default_version_id`, `readme_markdown`, `source_url`, `official`, `created_at`,
`deleted_at`. The pair of owner and lower cased name is unique. `visibility` is
`public` or `private`. `official` is set by the platform.

### model_versions

`id`, `model_id`, `digest`, `input_schema`, `output_schema`, `hardware_class`,
`packaging_document`, `status`, `withdrawn_reason`, `fast_boot`, `load_seconds`,
`run_seconds`, `pricing_mode`, `rate_micros`, `unit_divisor`, `quantity_source`,
`created_by`, `created_at`. The pair of model and digest is unique. `status` is
`building`, `active`, `deprecated` or `withdrawn`. `pricing_mode` is `per_second`,
`per_output_item` or `per_thousand_output_tokens`. `quantity_source` names which
recorded value is the priced quantity. A row is never updated after it is created,
apart from `status` and `withdrawn_reason`.

### model_stats

`model_id`, `run_count_total`, `run_count_28d`, `distinct_accounts_28d`, `score`,
`computed_at`. Derived from the prediction rows on a schedule; `run_count_total` is
what a card prints and `score` is what the popular column orders by.

### model_examples

`id`, `model_id`, `prediction_id`, `position`, `featured`, `created_at`. An example
points at a prediction that really succeeded, which is what makes every example on
the site reproducible.

### model_redirects

`old_owner`, `old_name`, `model_id`, `created_at`. Written on a rename or a transfer,
so an old address keeps resolving.

### collections and collection_models

`collections` holds `id`, `slug`, `title`, `description`, `position`.
`collection_models` holds `collection_id`, `model_id` and `position`, keyed on the
pair, and `position` is the curated order the band reads.

### hardware_classes

`id`, `class`, `display_name`, `cpus`, `memory_mb`, `accel_memory_mb`,
`rate_micros_per_second`, `effective_from`, `effective_to`. `effective_from` and
`effective_to` describe a half open interval, and for any class and any instant
exactly one row is in force. That property is held by the stored data rather than by
a check the application performs before writing.

### predictions

`id`, `account_id`, `model_version_id`, `deployment_id`, `source`, `status`, `input`,
`output`, `error`, `logs`, `metrics`, `hardware_class`, `idempotency_key`,
`webhook_url`, `webhook_events`, `created_at`, `started_at`, `completed_at`,
`canceled_at`, `data_removed`. The pair of account and idempotency key is unique
wherever the key is present. `source` is `web`, `api` or `deployment`. `input` and
`output` are document columns; everything a list query filters or sorts on is a real
column of its own, because putting status or hardware class inside the document is
how the run history becomes a full scan.

### deployments and deployment_releases

`deployments` holds `id`, `owner_account_id`, `name`, `model_version_id`,
`hardware_class`, `min_instances`, `max_instances`, `concurrency`, `cooldown_seconds`,
`created_at`, `deleted_at`, with the pair of owner and lower cased name unique.
`deployment_releases` holds `id`, `deployment_id`, `from_version_id`, `to_version_id`,
`from_hardware`, `to_hardware`, `actor_id`, `note`, `created_at`, and is append only:
the deployment row holds current state and the release table holds the history.

### usage_records

`id`, `account_id`, `prediction_id`, `hardware_class`, `quantity`, `unit`,
`rate_micros`, `unit_divisor`, `amount_micros`, `occurred_at`, `source`.
`prediction_id` is unique across the whole table. That single property is what makes
one completed prediction produce exactly one charge however many times its completion
is reported.

### usage_rollups

`account_id`, `bucket_start`, `granularity`, `model_id`, `hardware_class`,
`quantity`, `amount_micros`, keyed on all five of the first columns. Rollups are
derived from the usage rows and can be discarded and rebuilt from them at any time.

### spend_controls

`account_id`, `monthly_cap_micros`, `alert_thresholds`, `free_allowance_micros`,
`allowance_resets_at`. One row per account.

### invoices and invoice_lines

`invoices` holds `id`, `account_id`, `period_start`, `period_end`, `status`,
`subtotal_micros`, `discount_micros`, `total_micros`, `issued_at`. `invoice_lines`
holds `id`, `invoice_id`, `model_id`, `hardware_class`, `quantity`, `unit`,
`rate_micros`, `amount_micros`. A line descends from usage rows and never from a
rollup, and an issued invoice is never updated.

### outbox and webhook_deliveries

`outbox` holds `id`, `aggregate_type`, `aggregate_id`, `event_type`, `payload`,
`created_at`, `published_at`, and an unpublished row is what a publisher looks for.
`webhook_deliveries` holds `id`, `prediction_id`, `endpoint_url`, `event_id`,
`event_type`, `payload`, `status`, `attempts`, `next_attempt_at`, `last_status_code`,
`sequence`, `created_at`.

### page_views

`id`, `route`, `model_id`, `account_id`, `occurred_at`. One row per page view of a
public route. `model_id` is present where the route belongs to a model, which is what lets a
model's owner read the count for their own model and nobody else's.

### notifications

`id`, `account_id`, `kind`, `period`, `payload`, `read_at`, `created_at`. One row per in
product notice. The pair of `kind` and `period` is unique per account, which is what makes
a threshold notice fire once per period rather than once per crossing.

### prediction_shares

`id`, `prediction_id`, `created_by`, `expires_at`, `created_at`. One row per read only
share of a prediction on a public model. The share carries its own identifier, so a shared
link never exposes the prediction's own.

### reports

`id`, `reporter_account_id`, `prediction_id`, `model_id`, `category`, `note`,
`status`, `created_at`.

### idempotency_keys

`account_id`, `key`, `request_fingerprint`, `response_snapshot`, `created_at`, keyed
on the account and the key. The stored snapshot is what a repeat of the same request
receives, returned unchanged including its status.

### The relationships that carry the product

A prediction points at a version and never at a model, because a model's default
version pointer moves and a prediction's does not, and reproducibility depends on
that distinction. A deployment also pins a version, and changing it writes a release
row rather than editing the deployment. A usage row points at a prediction and at
nothing else, and an invoice line aggregates usage rows, so there is no path from an
invoice to a model that does not pass through usage. A token belongs to an account,
and an account is either a user or an organisation, which is why an organisation
token needs no table of its own. An example points at a real prediction.

Row-level scoping is the tenancy boundary and it is not a later addition: tenant
scoped reads are scoped by owner in the query itself rather than filtered
after retrieval, and never from an owner value a caller supplied. The application
connects as a role that cannot read across accounts, and work that legitimately
crosses accounts connects as a separate role.

### Seed data

Seeded on first start, idempotently.

Accounts: `owner@example.com` with the handle `maren-vos`,
`member@example.com` with the handle `arden-hale`, and
`member2@example.com` with the handle `vela-research`, all with the password
`deku-demo-pw-2026`; plus the organisation accounts `northlight`, `orchard` and
`blackpine-labs`, which have no login. `maren-vos` is an `owner` of `northlight` and
`arden-hale` is a `member` of it. `vela-research` belongs to no organisation.

Hardware classes: `cpu-small`, `cpu-large` and `gpu-a40`, with the rates in
`## Core features`, each with one row in force from the first start and no end.

Models and versions:

| Model | Owner | Visibility | Official | Versions | Status badge | Run count |
|---|---|---|---|---|---|---|
| `northlight/scribe-2` | `northlight` | public | yes | `8f1c0a4d` active and default, `3b71e0c9` withdrawn | `Warm` | `17900000` |
| `orchard/quickdraw-2` | `orchard` | public | no | `c41d7b20` active and default | `Warm` | `469700` |
| `blackpine-labs/prism-2-flex` | `blackpine-labs` | public | no | `5e09a3f6` active and default | `Cold`, load `12` seconds | `4000000` |
| `arden-hale/notes-tidy` | `arden-hale` | private | no | `9a2b61de` active and default | `Cold`, load `2` seconds | `17` |

Version `8f1c0a4d` of `northlight/scribe-2` declares the input fields `prompt`, a
required `string` with the format hint `text`; `max_words`, an `integer` with a
minimum of `10`, a maximum of `200`, a step of `10` and a default of `60`; `tone`, a
`string` with the enum `plain`, `formal`, `playful` and a default of `plain`; and
`include_title`, a `boolean` with a default of `false`. Its output is a `string`. It
is priced `per_second` on `cpu-small` with `run_seconds` of `4`. Its featured example
carries the prompt `Summarise the quarterly report for a busy reader.`

Version `c41d7b20` of `orchard/quickdraw-2` declares `subject`, a required `string`;
`count`, an `integer` with a minimum of `1`, a maximum of `4`, a step of `1` and a
default of `1`; and `style`, a `string` with fifteen enum members: `plain`, `terse`,
`formal`, `playful`, `technical`, `academic`, `journalistic`, `poetic`, `legal`,
`marketing`, `narrative`, `instructional`, `conversational`, `analytic` and
`persuasive`, with a default of `plain`. Its output is an `array` of objects, each
carrying `title`, `summary` and `tags`. It is priced `per_output_item` on `cpu-large`
at `40000` micro units per item, and the priced quantity is the value of `count`.

Version `5e09a3f6` of `blackpine-labs/prism-2-flex` declares `text`, a required
`string` with the format hint `text`; `max_words`, an `integer` with a minimum of `5`,
a maximum of `500`, a step of `1` and a default of `60`; and `keep_headings`, a
`boolean` with a default of `true` and marked advanced. Its output is a `string`. It
is priced `per_thousand_output_tokens` on `gpu-a40` at `3750` micro units per
thousand, and the priced quantity is the recorded output token count, which for this
version equals the value of `max_words`.

Version `9a2b61de` of `arden-hale/notes-tidy` declares `notes`, a required `string`
with the format hint `text`, and `bullets`, a `boolean` with a default of `true`. Its
output is a `string`. It is priced `per_second` on `cpu-small` with `run_seconds` of
`2`.

Collections: `summarise-text` and `structure-any-text`, as described in
`## Core features`.

Deployment: `arden-hale/tidy-live` as described in `## Core features`.

Spend controls: every seeded account starts with a `monthly_cap_micros` of `2000000`,
a `free_allowance_micros` of `500000`, and alert thresholds at 50, 80 and 95 per
cent.

Examples: `northlight/scribe-2` carries one featured example that points at a seeded
prediction which succeeded. `orchard/quickdraw-2` carries two.

Predictions: three seeded predictions belonging to `arden-hale`, all `succeeded`,
one on each public model, each with its usage row already written, so
`/predictions`, `/account/usage` and the examples gallery are not empty on a first
visit.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One tenant boundary, and it is the account. There is no sharing lattice, no
  territory model and no record sharing rule beyond the explicit share of a
  prediction on a public model.
- No payment is taken. There is no card capture, no payment provider, no dunning
  ladder and no tax calculation. An issued invoice stays `open`.
- No fine tuning and no training jobs. A model gains a version by being published,
  never by being trained here.
- No file inputs and no file outputs. Every model in this catalogue takes text,
  numbers, booleans and objects, and returns text or a structured object. There is no
  upload, no dropzone, no image, video or audio renderer, and no waveform view.
- No real accelerator. The platform runs every prediction itself and records the
  quantities each version declares, so a run's cost is knowable in advance and a
  run's result is the same every time for the same input.
- No outbound email and no SMS. Notices about spend thresholds, token expiry and
  membership changes are in product records readable by the account, not messages
  sent anywhere.
- No multi model comparison bench, no editorial archive, no change history, no
  documentation site, no enterprise sales form and no status page of our own beyond
  the indicator in the footer.
- No federated sign in, no single sign on, no directory provisioning and no second
  factor. Email and password is the only way in.
- No multi region placement and no data residency constraint. One region, one
  control plane, one run plane.
- No content moderation pipeline. A report is recorded and queued for a person; no
  automated screening runs and nothing is blocked by policy in this environment.
- No external network calls at runtime. The application talks to PostgreSQL and to
  nothing else, and an outbound webhook delivery attempt is recorded in the delivery
  log whether or not it reaches anybody.
- No native application and no offline mode.
- The application stays responsive with fifty thousand model rows, two hundred
  thousand prediction rows and two hundred thousand usage rows for one account in a
  single period. The usage screen for that account renders the current period in
  under one second.

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
| `POST /api/auth/signup` | `email`, `password`, `handle` | the account with `id`, `handle`, `kind`, `email` |
| `POST /api/auth/login` | `email`, `password` | the account with `csrf_token` for the session, and sets the session cookie |
| `POST /api/auth/logout` | none | an empty body, and revokes the session |
| `GET /api/health` | none | `{"status": "ok"}` |
| `GET /api/models` | `cursor`, `limit`, `collection`, `warm`, `owner` | `results`, `next`, `previous`, each result carrying `owner`, `name`, `description`, `run_count`, `official`, `status_badge`, `default_version` |
| `GET /api/models/<owner>/<name>` | none | the model, its default version digest, its `input_schema`, its `output_schema`, its pricing and its badges |
| `GET /api/models/<owner>/<name>/versions` | `cursor`, `limit` | `results` newest first, each carrying `digest`, `status`, `hardware_class`, `created_at`, `schema_changed`, `withdrawn_reason` |
| `GET /api/models/<owner>/<name>/views` | none | `count`, the page view total for that model's own routes |
| `POST /api/models` | `owner`, `name`, `description`, `licence`, `packaging_document`, `predict_signature`, `visibility` | the model and the created version with its `digest` |
| `PATCH /api/models/<owner>/<name>` | `visibility`, `description`, `licence`, `default_version` | the updated model |
| `GET /api/collections` | none | a top-level JSON array of collections, each with `slug`, `title`, `description`, `model_count` |
| `GET /api/collections/<slug>` | `cursor`, `limit` | the collection and its models in curated order |
| `GET /api/search` | `q`, `kind`, `collection`, `warm`, `cursor`, `limit` | `groups`, an ordered array of `{kind, results}` |
| `POST /api/predictions` | `version` or `model`, `input`, optional `webhook_url`, optional `webhook_events`, optional `deployment`; headers `Idempotency-Key` and `Prefer` | the prediction with `id`, `status`, `version`, `input`, `created_at` |
| `GET /api/predictions` | `cursor`, `limit`, `model`, `status`, `source`, `from`, `to` | `results`, `next`, `previous` |
| `GET /api/predictions/<id>` | none | the prediction with `status`, `output`, `error`, `logs`, `metrics`, `data_removed` and the itemised `cost` |
| `POST /api/predictions/<id>/cancel` | none | the prediction with `status` `canceling` or `canceled` |
| `GET /api/predictions/<id>/events` | header `Last-Event-ID` | a server-sent event stream ending in one terminal event |
| `GET /api/predictions/<id>/deliveries` | none | a top-level JSON array of delivery rows with `event_id`, `event_type`, `status`, `attempts`, `next_attempt_at`, `sequence` |
| `POST /api/predictions/<id>/share` | none | a read-only share with its own `id` and its own `expires_at` |
| `GET /api/tokens` | none | a top-level JSON array of tokens with `id`, `name`, `prefix`, `last_four`, `scopes`, `created_at`, `last_used_at`, `expires_at` |
| `POST /api/tokens` | `name`, `scopes`, `expires_in_days` | the token row and, once only, the clear `token` value |
| `POST /api/tokens/<id>/rotate` | none | the new token row and, once only, the clear value, with the old row's `expires_at` set |
| `DELETE /api/tokens/<id>` | `name` for confirmation | an empty body, and the token is refused on its next use |
| `GET /api/hardware` | none | a top-level JSON array of hardware classes with `class`, `display_name`, `cpus`, `memory_mb`, `accel_memory_mb`, `rate_micros_per_second` |
| `GET /api/account/usage` | `from`, `to`, `group_by` | `total_micros`, `free_allowance_remaining_micros`, `cap_micros` and `rows`, each row carrying `prediction_id`, `model`, `hardware_class`, `quantity`, `unit`, `rate_micros`, `amount_micros` |
| `PUT /api/account/spend-cap` | `monthly_cap_micros` | the updated spend controls |
| `GET /api/account/invoices` | `cursor`, `limit` | `results`, each with `period_start`, `period_end`, `status`, `subtotal_micros`, `discount_micros`, `total_micros` |
| `GET /api/account/invoices/<id>` | none | the invoice and its `lines` |
| `GET /api/account/audit` | `cursor`, `limit` | `results` newest first, each with `action`, `resource_type`, `resource_id`, `before`, `after`, `created_at`, `prev_hash`, `hash`, `actor`, `request_id` |
| `GET /api/account/notifications` | none | a top-level JSON array of in-product notices with `kind`, `period`, `payload`, `read_at`, `created_at` |
| `GET /api/deployments` | `cursor`, `limit` | `results`, each with `owner`, `name`, `version`, `hardware_class`, `min_instances`, `max_instances`, `concurrency` |
| `POST /api/deployments` | `name`, `version`, `hardware_class`, `min_instances`, `max_instances`, `concurrency`, `cooldown_seconds` | the deployment |
| `PATCH /api/deployments/<owner>/<name>` | `version`, `hardware_class`, `min_instances`, `max_instances`, `concurrency`, `cooldown_seconds`, `note` | the deployment and the release row it wrote |
| `GET /api/deployments/<owner>/<name>/releases` | `cursor`, `limit` | `results` newest first, each with `from_version`, `to_version`, `actor`, `note`, `created_at` |
| `GET /api/deployments/cost` | `hardware_class`, `min_instances` | `standing_cost_micros_per_day` for that configuration |
| `GET /api/deployments/<owner>/<name>/metrics` | none | `instances`, `queue_depth`, `queue_age_seconds`, `requests_per_minute`, `error_rate`, `cold_starts` |
| `POST /api/deployments/<owner>/<name>/rollback` | `release` | the deployment and the new release row |
| `GET /api/organisations` | none | a top-level JSON array of the organisations this account belongs to, with the account's role in each |
| `POST /api/organisations/<handle>/members` | `handle`, `role` | the membership |
| `PATCH /api/organisations/<handle>/members/<member>` | `role` | the membership |
| `DELETE /api/organisations/<handle>/members/<member>` | none | an empty body |
| `POST /api/reports` | `prediction` or `model`, `category`, `note` | the report |

Field names are exact. A list endpoint whose row shape is fixed returns a top-level
JSON array; a paginated endpoint returns the `results` envelope described above. A
successful call returns the named resource or shape, and an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a silent
success, carrying the error body described in `## Core features`. Bearer
authentication applies to everything except sign up, sign in, the health route and
the public catalogue reads.

### No mocks

The rows this product reports on have to exist in PostgreSQL. An in memory list of
predictions that resets when the process restarts, a usage total held in a variable
rather than summed from rows, a token table that keeps the clear value so the masked
display can be reconstructed, an audit chain computed at read time rather than
written at write time, and a hardware rate typed into a template rather than read
from the catalogue are each a contract violation however convincing the page looks.
PostgreSQL is the fact - the app's UI and its own reporting can only reflect what
lives in it, never substitute for it.

## Definition of done

A stranger can browse the catalogue, open a model page, sign in, take a token and
create a prediction that reaches `succeeded`, charged as one usage row for the amount
the rate table implies. Repeating that create with the same idempotency key produces no
second run and no second charge. The itemised rows for a period add up to that period's
total with nothing left over, and once the monthly cap is crossed no new run starts
anywhere. A second account asking for that account's records is told they do not exist.
