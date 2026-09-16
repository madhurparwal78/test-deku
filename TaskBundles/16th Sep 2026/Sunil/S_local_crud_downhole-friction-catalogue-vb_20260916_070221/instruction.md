# Downhole Friction Catalogue

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, read a field case
for a real well, submit their own well data from the enquiry band at the foot of that case,
and see the request they just sent come back with a reference, without hitting an error page.
The request they submitted must exist as a real row in PostgreSQL carrying the route it was
sent from, and it must still be there, unchanged and readable by a signed-in engineer, after
the app restarts. A panel the app shows itself is not the record.

## Overview

TORQ designs, manufactures and runs downhole tools that reduce friction and vibration in
directional and extended-reach oil wells. This is its public catalogue and field-evidence
site, plus the small signed-in desk where the firm's own engineers work what the site brings
in.

The product is five parts and they are load-bearing in this order. A product catalogue: three
hardware classes across five families, each with named size variants, each variant carrying a
specification table, index to detail. A field-evidence library: ten wells, each a card
carrying the tool configuration, the well geometry, a measured result and a date, each
opening into a case route whose spine is measured numbers. A service description: a four step
engineering cycle from modelling a candidate well to delivering a before and after report. A
firm profile: why the firm builds rather than distributes, what its material is, and what it
has done. And an enquiry funnel: one form, repeated at the foot of almost every route, that
takes a visitor's well data and turns it into a modelling request.

The catalogue and the evidence library are the same argument told twice, and they must stay
cross-linked in both directions: a product detail route names the cases that ran it, and a
case names the product that ran. Five audiences read this site and they want different
things from it. A drilling engineer at an operator wants to know whether the tool holds
torque under the limit to total depth on a specific well profile, and leaves with a
comparable inclination, a measured torque delta and a modelling request submitted. A well
construction supervisor wants to know whether the tool installs inside a trip without adding
rig time. A drilling contractor wants sizes, lateral load ratings and service life against
the pipe already in the yard. Procurement wants to know who the firm is, whether it
manufactures, and whether supply is predictable. The firm's own field engineer wants a page
to show a client on a laptop at a rig. The register throughout is engineer to engineer: the
product never says "solutions" where it can print a number.

The genuinely hard part is the enquiry funnel, and it is the only thing on this site that
touches state. Everything above it exists to make a visitor confident enough to reach it. It
must survive a double submit, it must record which of the nine routes it was sent from, and
what it wrote must be exactly what a signed-in engineer reads back afterwards.

What this deliberately is not: there is no cart, no checkout and no price anywhere, because
nothing here is bought. There is no public account; a visitor never signs in. There is no
search field on the evidence library, no filters, no facets, no sort control and no
pagination. There is no third party vector map, no award badge, no comments, no likes and no
messaging.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (anonymous, no account) | read every public route in both locales; browse the catalogue and the evidence library; submit a well data enquiry; subscribe from the footer | **cannot read any modelling request**, **cannot change any request's status or assignment**, **cannot reach the desk at all** |
| Engineer (signed in) | everything a visitor can, plus read the modelling request queue, open one request, change its status, assign it to an engineer, and add a note | **cannot delete a request**, **cannot edit the well data a visitor submitted** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a Visitor session to any Engineer-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged. A request read, a status change and an assignment are
all Engineer-only, and an anonymous caller gets none of them.

Signup is open: anyone can register an engineer account with an email and a password. Two
accounts are seeded so the product can be driven without registering:

- `engineer@example.com`
- `engineer2@example.com`

## Core features

### Auth

Email and password, implemented by the app. No external identity provider. A successful login
returns a bearer token; the client sends it as `Authorization: Bearer <token>` on every desk
request. Passwords are stored hashed, never in plain text. Tokens expire; an expired token on
a desk request is rejected and the pending change is not applied. Signup is open and creates
an engineer account. There is no password reset in this product.

1. Login with a seeded email and the seeded password returns a token and the engineer's
   display name.
2. Login with a wrong password is rejected as invalid and returns no token.
3. Every public catalogue and evidence route is readable with no token at all.

### The enquiry funnel

This is the workflow the product exists for.

1. The enquiry band appears at the foot of **every route except privacy and contacts**. It
   has four parts in order: a bracketed eyebrow reading "We reply within a day"; the headline
   "Run the numbers on your well"; the standfirst "Send your well data and constraints - we'll
   run T&D modeling and come back with a configuration and the expected impact."; and the
   form.
2. The contacts route does not carry the band at the foot. It promotes the same form to be
   the page's main content.
3. The form fields are: First name (text, required), Last name (text, required), Email
   (email, required), Phone (tel, optional), Message (a resizable textarea, optional) and a
   required consent checkbox. First and last name sit side by side, email and phone sit side
   by side, and message and consent run full width.
4. The consent label reads "I consent to the processing of my personal data (name, email,
   phone, message content) by TORQ Systems LLC for the purpose of handling my request and
   contacting me, under the Personal Data Processing Policy.", and "Personal Data Processing
   Policy" is a real inline link to the privacy route.
5. **The submit control is genuinely disabled until consent is ticked, not merely dimmed**,
   and the reason is announced rather than only shown. Its label is "Contact us".
6. A submission carries, in addition to the fields above, the locale it was sent under and
   **the route it was sent from**. The same band appears at the foot of nine routes, and a
   lead is worth much more when the firm knows whether it came from a product page or a case
   page, so the route is part of the record and not optional.
7. A successful submission creates one modelling request, reveals the success panel in place
   titled "Thank you!" with the body "Your request has been sent. We will get back within 24
   hours.", and shows the request's own reference.
8. A rejected or failed submission reveals the failure panel in place, titled "Oops!" with the
   body "Sending failed. Please try again later or email info@torq.tech." **The failure panel
   must name that fallback mailbox.** A submission here is commercially valuable to both
   parties and a silent failure loses a lead permanently.
9. **Both panels exist in the served markup at all times and are revealed, never injected.** A
   visitor whose script has partly failed still has the fallback mailbox in the page.
10. **Submitting the same enquiry twice in immediate succession creates exactly one modelling
    request, never two.** The second attempt returns the first request's reference rather than
    minting a second one, and the stored row is not written a second time. The control is
    disabled for the duration of the request.
11. Every form rejects invalid input inline, names the field that is wrong, and **writes
    nothing at all**: a missing first name, a missing last name, a malformed email address, or
    an unticked consent box each leave the database exactly as it was. A rejected submission
    is denied as a client error with a reason, never a silent success.
12. The footer subscribe form takes one email field and its own consent checkbox, whose copy
    is separate from the enquiry consent and narrower in scope: "I consent to the processing
    of my email by TORQ Systems LLC to receive informational materials, under the Personal
    Data Processing Policy." Subscribing the same address twice does not create a second
    subscriber row.

### The modelling request desk

1. An engineer signs in at the desk login and lands on the queue.
2. The queue is a table, newest first, one row per modelling request, showing the reference,
   the name, the email, the route it came from, the status and who it is assigned to.
3. **The row must match what the visitor's form displayed, field for field, and it must
   survive a restart.** The first name, last name, email, phone, message, locale and source
   route stored are exactly what was submitted, and reloading the desk or restarting the app
   returns the same values.
4. Status is one of `new`, `modelling`, `configured`, `reported`, `declined`, with that exact
   casing. A request starts at `new`. It moves forward through that order one step at a time,
   and `declined` is reachable from any state. **No other transition exists**: a request at
   `reported` cannot be moved back to `new`, and the attempt is denied as invalid with a
   reason, leaving the stored status unchanged.
5. Status and assignment are changed in the request's own row in the queue, without leaving
   the queue. The row shows the new value at once, and if the save is refused the row returns
   to its previous value and the reason is announced.
6. Assigning a request sets it to one of the engineer accounts. A request may be assigned to
   nobody.
7. An engineer can add a note to a request. Notes are additive; nothing overwrites the
   visitor's own words.
8. **No engineer can delete a request and no engineer can edit the well data the visitor
   submitted.** Both are denied by the server and the underlying row must not change.
9. One modelling request is seeded, reference `REQ-1001`, at status `new`, assigned to
   nobody, so the queue is never empty on a fresh install.

### The product catalogue

Five families in one index, in this order, each a card in a two column grid:

| Family code | Class line | Size variants |
|---|---|---|
| FRS | Friction Reduction System | FRS-89, FRS-102, FRS-127, FRS-149 |
| SVR | Shock and Vibration Reducer | SVR-120, SVR-172 |
| TRANSFER X1 | Transfer | 89, 102, 127 |
| TRANSFER X3 | Transfer | 89, 102, 127 |
| TRANSFER X6 | Transfer | 89, 102, 127 |

1. Ten size variants exist across the five families, and **every one of them appears in the
   size table on its family's detail route**. A variant listed on a card and missing from a
   table is a defect.
2. Each card carries the full class name in small type at the top left, the family code in
   the largest type on the page across the middle, a small side elevation render of the tool
   under it, a hand-broken two line description, and a row of its size variants along the
   bottom left. A "Learn more" control appears in the bottom right on hover.
3. The card descriptions are fixed copy: FRS is "Friction reduction system for the drill
   string."; SVR is "Shock and vibration reducer for the BHA."; TRANSFER X1 is "Short sub for
   full-string configurations."; TRANSFER X3 is "Mid-length sub - BHA only."; TRANSFER X6 is
   "Longest sub of the lineup - max damping zone."
4. A product detail route opens with a banner: a bracketed eyebrow reading "Products", the
   family code as one swept line, the class name as a second, and the family description
   across two or three more.
5. Below the banner is a dark band of result cards. Each card carries three parts in this
   order: an annotation naming **the provenance of the number**, the figure itself as a
   counting odometer, and a label naming the quantity. The provenance annotation is required
   on every figure and has no default. It is what separates a marketing figure from an
   engineering one.
6. POLYTECH is the university bench-test partner whose bench the first two figures come from.
   On FRS the four result cards are: a POLYTECH bench axial friction reduction, a POLYTECH
   bench circumferential friction reduction, an in-house material friction coefficient on
   steel, and a field hook load on POOH reduction prefixed "up to". The band's standfirst
   reads "Bench testing at POLYTECH and field testing across 9 pilot runs confirmed both
   axial and circumferential friction reduction relative to steel."
7. On TRANSFER X3 the three result cards are: a stick-slip index SSI reduction, a weight on
   bit WOB lift, and a rate of penetration ROP lift.
8. A "How it works" numbered list follows, three or four items, each with a two digit index,
   an optional aspect name beside it, a title and a body. On FRS the four items are the
   plain-bearing principle; "Friction coefficient < 0.06" under the aspect Material; "1-2 min
   to install" under the aspect Installation; and "2M-revolution service life" under the
   aspect Service life. Their bodies state that the drill pipe rotates inside a stationary
   composite sleeve pressed against the wellbore wall or casing by lateral load and never
   touching the pipe body; that the low-friction composite is the in-house Polymer One, where
   steel on steel runs at 0.13 in the lab, so 2x+ less friction; that it mounts on the pipe
   during a trip or on the catwalk, held by two high-strength aluminum stop collars (4xM8,
   class 10.9), with no steel frame and no hinges inside the sleeve; and that it runs 2M
   revolutions in cased hole and 500k revolutions in open hole at a wear rate of 0.01 g/cm2
   per GOST 13087-2018.
9. On TRANSFER X3 the three how-it-works items are a kinematically decoupled stabilizer whose
   stabilizing sections rotate and shift radially relative to the body so no reactive lateral
   load is transferred to the drill string; a composite-reinforced bearing module, an adaptive
   floating bearing section reinforced with composite rings that damps axial and torsional
   shocks, under the aspect Design; and a constant flow ID with low pressure drop inside the
   sub and no impact on mud flow rate or mud motor operation, under the aspect Hydraulics.
10. A material panel appears on the FRS route only, since it is the only family whose
    differentiator is the compound. It is titled "Polymer One", standfirst "TORQ's own
    formulation. Low-friction composite. Frameless - no steel reinforcement inside the
    sleeve.", and carries a five row parameter and value table: friction coefficient 0.06
    (wet, on steel; steel-on-steel: 0.13); axial friction reduction -64% vs steel;
    circumferential friction reduction -51% vs steel; max rotational speed 200 rpm; and
    **Steel frame / None**. That last row is the argument of the whole page in one cell: the
    product is defined by an absence and the table prints it.
11. The size table is headed "Sizes" and runs one column per variant. On FRS the columns are
    Parameter, FRS-89, FRS-102, FRS-127 and FRS-149*, and the six parameter rows are pipe
    size in mm (89, 101.6, 127.0, 149.2), system length in mm (510 throughout), max lateral
    load in kgf (2200, 2500, 2200), stop collar axial force in tf (7.5, 8.0, 10.0), service
    life cased in thousands of revolutions (2000 throughout) and service life open hole in
    thousands of revolutions (500 throughout).
12. **An unmeasured cell prints a single dash character, never a blank and never a zero.**
    The FRS-89 column carries five such cells, and the footnote below the table reads
    "*FRS-149 - pilot batch. Max temperature 100C, stop collar make-up torque 25 N-m. FRS-89
    specs being finalized - datasheet in progress." A blank cell reads as an oversight; a
    printed dash reads as a deliberate "not yet stated", which is what it is.
13. On TRANSFER X3 the size table columns are Parameter, 89, 102 and 127, and the rows are
    length in mm (1225 throughout), body OD in mm (127.0, 136.7, 168.3), OD across blades in
    mm (136.7-152.4, 142.9-152.4, 212.7), wall thickness in mm (10.4, 10.4, 12.7), hydraulic
    diameter in mm (134.1-147.6, 138.7-147.6, 203.2), max lateral load in kgf (3500
    throughout) and service life in millions of revolutions (5 throughout).
14. Each product route closes with a numbered application list, titled "What FRS is used for"
    on FRS and "When to use" on TRANSFER X3, carrying the same items as that family's panel
    on the home route. The duplication is deliberate: the two routes are entered from
    different places and neither can assume the other was read.
15. TRANSFER X1 and TRANSFER X6 are built on the TRANSFER X3 template and are reachable from
    their cards.

### The field-evidence library

1. Ten case cards in a two column grid, **ordered by date descending**, running from November
   2025 down to February 2025 with three cards sharing March 2025. The date is a month and a
   year with no day, because a case is dated by the run and a run is a campaign rather than
   an instant.
2. Each card carries, in this arrangement: the well geometry and region at the top left, hand
   broken across two lines; the family code in the largest type, centred; two configuration
   lines under it, each preceded by a small square marker; the measured result in one to
   three hand broken lines at the lower left; the month and year under that; and a "View
   case" control at the bottom right revealed on hover.
3. **The two configuration markers are different colours and the difference carries meaning.**
   The first line names the tool variant and type the firm supplied and takes the accent
   square. The second names the pipe that was already in the hole and takes a grey square.
   That is the distinction between what the firm supplied and what was already there, and it
   is why the two lines are not one string.
4. The ten cards are: Hor 90 / Western Siberia, FRS-89 type 1 on drill pipe 89, November
   2025; Hor 90 / Eastern Siberia, FRS-89 type 1 on drill pipe 89, October 2025; Hor 88 /
   Western Siberia, FRS-127 type 1 on drill pipe 127 + HWDP-147, August 2025; Hor 83 /
   Western Siberia, FRS-127 type 1 on drill pipe 127 + HWDP-147, July 2025; S-shape 61 /
   Volga-Ural, FRS-127 type 1 on drill pipe 127, June 2025; Northgate field, FRS-127 type 1
   on drill pipe 127, April 2025; Hor 90 / Western Siberia, FRS-127 type 1 on drill pipe 127,
   March 2025; Hor 92 / Western Siberia, FRS-102 type 1 on drill pipe 102, March 2025; Hor 83
   / Western Siberia, FRS-127 type 1 on drill pipe 127, March 2025; and S-shape 40 / Western
   Siberia, FRS-127 type 1 on drill pipe 127, February 2025.
5. Their result lines are dense on purpose and are pinned copy. In card order: "-33% torque,
   -33 t on POOH, +13 t on slack-off. Actual mu ~0.17 vs 0.25-0.30 forecast."; "Oscillator
   dropped. HD 2,661 m (actual) vs 2,096 m (no-FRS forecast). -19% torque, -14 t."; "-17%
   torque, -13 t on POOH, +10 t on slack-off. Well drilled to TD 3,990 m with no incidents.";
   "-36% torque, -20 t on POOH. Enables drilling without HWDP-147."; "2,745 m reach, -26%
   torque, -12 t on POOH. Unlocks wells with targets up to 3,200 m out."; "-32% torque, -26 t
   on POOH"; "-31% torque, -15 t on POOH, slide ROP +50% (20 to 30 m/h)."; "-39% torque, -11
   t on POOH, slide ROP 12 m/h at 4,500 m. +500 m headroom for longer horizontal."; "-48%
   torque at final TD 3,394 m, -15 t on POOH at 2,950 m."; and "-33% torque, -7 t on POOH.
   1,458 m reach vs 797/325 m on prior wells on the field."
6. The index banner is two swept lines: "Field tests", then "Each case is a real well with
   documented parameters." That second line is the contract this route makes, and the data
   model enforces it: **a case record without measured parameters is not publishable.**
7. A case detail route is keyed by **the well number, not by a slug**. `/en/cases/22061` is
   the well 22061 case. All ten case routes exist.
8. A case route opens with a bracketed eyebrow carrying the field name, the word "Well" as a
   swept line, and the well number set inside the bracket motif, so the title reads as an
   instrument reading rather than as a heading. Then three swept standfirst lines.
9. A dark metric bar follows, three headline figures in three ruled cells: total depth in
   metres, horizontal reach in metres, and the count of tools run. On well 22061 these are
   4,025 m, 2,938 m and 100. Each is a counting odometer and the thousands separator is
   static text between the digit strips, so it does not slide.
10. A well profile section headed "Well profile" under the eyebrow "Inputs" carries one
    metric card per measurement, each with a two line description naming the quantity **and
    the run it came from**. On well 22061: Torque / Run #1 with mud motor; Torque / Run #3
    with RSS; and Hook load on POOH / Run #1. A case with three runs produces three different
    numbers for the same quantity, and printing them without saying which run each came from
    is the one thing that would make this page useless to its reader.
11. A "Project goals" numbered list of four goals, written as imperatives stated before the
    run: "Reduce drilling torque", "Reduce hook load on POOH", "Eliminate surface vibration",
    "Headroom for longer reach". These are the page's hypothesis.
12. A "Technology" section under the eyebrow "Solution" carries one panel per tool used, with
    the family code, a type badge reading "Type 1", the family description, and the first
    three how-it-works items from that family's product route with the material name removed.
    The case page quotes the product page rather than restating it differently.
13. A "Key results" section under the eyebrow "Outcome" carries three result cards using the
    same component as the product route: an annotation carrying the before and after values,
    an odometer carrying the delta, and a label naming the quantity. On well 22061: "36.4 to
    24.6 kN-m" / Bit torque; "40 to 32 kN-m" / Bit torque (RSS); and "140 to 114 t" / Hook
    load on POOH.
14. A "Conclusions and lessons" list under the eyebrow "Takeaways" restates each goal with a
    badge and the per-run figures. On well 22061: "Torque reduction", badge "Done", body "Run
    #1: -32% (-12 kN-m). Run #2: -18% (-7 kN-m). Run #3: -20% (-8 kN-m)."; "Hook load on POOH
    reduction", badge "Done", body "Run #1: -26 t vs forecast. Run #3: -10 t vs the BHA
    without FRS."; and "Surface vibration eliminated", badge "Done", body "Allowable top-drive
    rotary speed raised from 90 to 140-160 rpm." A neutral badge variant exists for an outcome
    that is neither met nor missed.
15. Three tagged cards follow, one per outcome type: an incident, a reconfiguration
    recommendation and an additional effect, tagged "FRS incident", "Reconfiguration
    recommendation" and "Extra effect", titled Equipment, Engineering and analysis, and
    Implementation support.
16. The route closes on a single unattributed verdict paragraph: "Forecast vs actual torque
    held within 8% - the T&D model proves out for sizing protector count and placement on long
    horizontal sections." **That paragraph is the page's own verdict on its model and it names
    a tolerance.** A case page that reports only successes and never how far the forecast
    missed is not evidence, so it is required on every case.

### The engineering service

1. The banner reads "Engineering" over "We analyze well data, pick the FRS configuration, and
   forecast the outcome. We don't guess - we run the numbers.", under the eyebrow "Services".
2. Four service cards on a dark ground, each with a two digit index, a title and a one line
   body: 01 T&D modeling, "Torque-and-drag modeling for candidate wells."; 02 Configuration,
   "FRS sizing, count, and placement."; 03 Field support, "We're on site during the run."; 04
   Operations report, "Result on record - before vs after." Each carries a drawn octagonal
   glyph above its title, and card 04's glyph is drawn with a dashed outline, which marks it
   as the deliverable rather than an activity.
3. The same four steps are stated again at length as the process cycle, headed "Full cycle -
   from candidate well to a verified result report." with the standfirst "Four steps that take
   complex runs from forecast to delivery." Step 01 adds that T&D modelling is **free for
   qualified candidates**; step 02 becomes FRS configuration and adds placement intervals for
   the calculated profile; step 03 adds tracking placement and logging parameters; step 04
   adds fact against forecast in one document. **The two lists are not redundant and both are
   required**: the first is the menu, the second is the commitment, and the second is where
   the qualifying offer lives.
4. A qualification list headed "We work wells where friction is the operational risk." with
   four conditions. Each carries a **printed threshold in its annotation slot**, not a label,
   because the list is a self-qualification tool: a reader holds their own well up against
   four printed numbers and decides whether to fill in the form. The four are: "DLS typ. 3-6
   deg/30m" / ERD - horizontal sections; "WOB loss typ. 30-50%" / Drilling with motor; "up to
   -15 t on POOH" / Hook load on POOH constraints; and "DLS > 4 deg/30m" / High wellbore
   curvature.
5. Their bodies are distinct from one another. Horizontal sections 1,500-3,500 m, where
   friction stacks up and without FRS the torque blows past the limit well before TD. Drilling
   with motor, where getting axial load down to the bit is critical and high friction in the
   lateral kills WOB to the BHA and ROP with it. Hook load on POOH constraints, where the
   overpull budget on a long lateral is spent before the string is out and the tool buys back
   the margin that lets the trip finish. High curvature, which multiplies normal load on the
   wellbore wall, causing tool wear and torque loss.
6. Two case cards close the route under "Proven in the field", using the same card component
   as the evidence library. Two rather than ten: this route is a service pitch and the full
   library is one click away.

### The firm profile

1. The about banner is four hand broken lines, opening on two very short ones and widening:
   "We're engineers." / "Not distributors." / "You don't get a box of tools - you get a
   full-cycle solution" / "that takes operational risk off the table." Keep the line lengths;
   a four line banner that opens short and widens is a composition.
2. A material note sits under the banner as a footnote to it: an asterisk, the title "Polymer
   One.", and the line "Our own development - engineered to deliver the results we promise."
3. Two long statements are set word by word and brighten in reading order as the reader
   scrolls through them. Under the eyebrow "History": "We don't just sell tools - we own the
   outcome. We develop the technology, manufacture it, and stay with every project from
   scenario modeling to a verified result in the field." Under the eyebrow "About us": "First
   in Russia to deploy frameless FRS protectors - and we built the material for them, with
   properties the market didn't have." These are the two claims the firm most wants read and
   the treatment is used on nothing else.
4. Three pillar cards: Technology / "Patented in-house technologies" / "No compromises when
   chasing the right result."; Production / "In-house production" / "Continuous production
   cycle, predictable supply."; and Engineering / "Engineering by senior specialists", whose
   body must be its own distinct sentence about the seniority and field experience of the
   engineering staff and must not repeat the production card's body. Build the set once.
5. Two technology cards. The first is titled "Polymer One" with the body "Low-friction
   composite without a steel frame. Friction coefficient mu = 0.06 in wet contact with steel -
   steel itself runs at mu = 0.13.", and a three column comparison table whose columns are
   Parameter, Polymer One and Steel, with rows "mu / 0.06 / 0.13" and "Friction reduction /
   -64% / baseline". **The word "baseline" in the last cell does the work of a number and is
   the right choice**: steel is the reference condition, not a competitor. The second card is
   titled "Frameless" over "FRS protector", body "Reduces friction, dampens vibration.", a
   spec label "Sizes" and four size values 88.9, 101.6, 127.0, 149.2, closing with a "To
   equipment" control to the products index.
6. A "Facts in numbers" section with two counting figures, each carrying a badge reading
   "Fact": one labelled "Different projects where our technology has been successfully
   deployed" and one labelled "Operations completed across Russia", whose figure carries a
   static `+` suffix alongside the digit strips.

### Locale, routing and the site shell

1. Two locales. The default locale is served without a prefix at the site root; English is
   served under the `/en` prefix. **The prefix is the only difference between the two route
   trees.**
2. Switching locale replaces the prefix and **holds the rest of the path**. A visitor reading
   the TRANSFER X3 route who switches language is still reading the TRANSFER X3 route. A build
   that drops them to the home route is wrong.
3. Every entity carries both locales, or falls back with the fallback marked.
4. The thousands separator and the decimal separator are locale dependent, and they are
   content in the markup between the digit strips rather than formatting applied afterwards.
5. **Every internal link on every public route resolves.** There is no unlinked route: every
   route is reachable by following links from the locale home, and no link leads anywhere that
   answers not-found.
6. An unknown address renders the product's own not-found page on the standard shell, with the
   header, the footer and a control back to the locale home, and answers not-found. A case
   number that does not exist does the same, from the evidence index.
7. Navigation between routes does not full-reload the document, and the header persists across
   the swap.
8. Every route except the home route is built from one shell: header, a page banner carrying
   an eyebrow, a large swept title and one or two standfirst lines, the route body, the
   enquiry band, and the footer. The privacy route omits the enquiry band.
9. The privacy route is load-bearing rather than decorative, because every consent label links
   to it. It names the legal entity TORQ Systems LLC, the categories of personal data the two forms
   collect,
   the purpose of processing, the retention period, and the contact route for a data subject
   request. **The categories it lists must match what the forms actually send**, so adding a
   field to either form changes this route in the same change.
10. The footer carries four columns: the registered office address, a Pages column linking
    About, Case Studies, Products, Engineering and Contacts, a Contact column carrying
    info@torq.tech and +7 (000) 0000000, and the Subscribe column. Under them sits a colophon
    row reading "(c) 2026 TORQ Systems LLC", "Privacy Policy" and "Made by Studio Kessler".

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home under the default locale | none |
| `/en` | home under the English locale | none |
| `/en/products` | the five card equipment index | none |
| `/en/products/frs` | FRS detail | none |
| `/en/products/svr` | SVR detail | none |
| `/en/products/x1` | TRANSFER X1 detail | none |
| `/en/products/x3` | TRANSFER X3 detail | none |
| `/en/products/x6` | TRANSFER X6 detail | none |
| `/en/cases` | the ten card evidence index | none |
| `/en/cases/22061` | one case, keyed by well number | none |
| `/en/engineering` | the service description | none |
| `/en/about` | the firm profile | none |
| `/en/contacts` | the form as the page's main content | none |
| `/en/privacy` | the policy every consent label links to | none |
| `/en/desk/login` | engineer sign in | none |
| `/en/desk` | the modelling request queue | engineer |
| `/en/desk/REQ-1001` | one request | engineer |

**Entry and redirects.** An anonymous visitor who opens `/en/desk` or any request route lands
on `/en/desk/login` with the destination held, and is served it after signing in. Signing in
lands on `/en/desk`. Signing out returns to the locale home. A token that expires mid-action
lands on `/en/desk/login` and the pending change is not applied. Switching locale replaces the
prefix and holds the path. An unknown address renders the product's own not-found page.

**Journey 1, the graded one: find a comparable well and ask for a calculation.** Open
`/en/cases`. Read the ten cards. Open `/en/cases/22061`. Read the metric bar, the goals, the
technology and the key results. Scroll to the enquiry band. Fill first name, last name and
email, tick consent, submit. The success panel appears in place with the request reference,
and the route it was sent from is part of the record.

**Journey 2: compare sizes.** Open `/en/products`. Open the FRS card. Read the size table:
four variant columns, six parameter rows, a dash in each unmeasured cell of the FRS-89 column,
and the footnote explaining the pilot batch.

**Journey 3: self-qualify.** Open `/en/engineering`. Read the four qualifying conditions and
their printed thresholds. Reach the enquiry band at the foot of the same route.

**Journey 4: cross-link both ways.** From `/en/products/frs`, open a case that ran FRS. From
that case, return to the product that ran.

**Journey 5: work the queue.** Sign in at `/en/desk/login` as `engineer@example.com`. The
queue shows `REQ-1001` and the request just submitted. Change the new one's status to
`modelling` in its row and assign it to `engineer2@example.com`. Reload. Both changes are
still there and every submitted field still reads back exactly as it was sent.

**Journey 6: rejection.** Submit the enquiry with consent unticked; the submit control is
disabled and nothing is written. Submit with a malformed email; the field is named inline and
nothing is written. Try to move a `reported` request back to `new`; the change is denied and
the stored status is unchanged.

**States.** Every list has an empty state and says so in words rather than rendering an empty
table. Every route has a loading state. The two enquiry panels are present in the markup at
all times. A failure never navigates the visitor away from where they were: a form service
that cannot be reached shows the failure panel in place, and an evidence index whose case
cannot be found returns the not-found page rather than an empty screen. Errors never crash the
app.

## UI/UX notes

This product should read as an instrument, not as a brochure. The honest north star here is
comprehension: a sceptical drilling engineer should be able to weigh a claim in the first
moment, and atmosphere would work against that. The register is operational and the whole
visual system exists to make numbers and their provenance legible.

Five decisions carry the character and they are not negotiable. **A ruled ground:** the page
is a near-white neutral field divided by hairline rules into cells, content sits inside the
cells, and the rules do not stop at section boundaries, so the document reads as one sheet of
graph paper rather than as a stack of bands. There are more rules than filled areas, and that
is the point. **Dark inserts, not a dark theme:** individual bands invert to a near-black
neutral while the rest of the page stays light, and the header re-colours itself against
whatever band is behind it. Commit to the light ground and design it fully; the contacts route
is the one route that is dark throughout. **One accent used as a marker:** a light, vivid red
appears as the small filled square before a list number, as the button ground, and almost
nowhere else. It is a pointer, not a colour scheme, and it appears nowhere that is not an
action or an index. **Brackets and cut corners:** eyebrow labels are wrapped in a drawn
bracket pair, and every button, tag, card preview and contact mark has its corners cut on a
chamfer rather than rounded, on all eight corners. The only rounded thing in the body of the
site is the status badge on a case conclusion, and it stays rounded because a badge is meant
to read as a chip rather than as a machined part. **Numbers that count:** every headline
figure spins up from a strip of digits when it enters the window.

**Palette by role, by relationship and exclusivity rather than by notation.** The ground is a
near-white neutral and pure white is an accent used sparingly, never the ground. Body copy is
a deep neutral and is the most-used colour on the site. Headings on a light band are a
near-black neutral; on a dark band they are a near-white neutral and body copy there is a
light neutral. Annotations, eyebrow labels and table headers are a mid neutral, a step back
from body copy. Hairline rules are a light neutral on a light ground and a deep neutral on an
inverted one, and a hairline wash over either ground is the same neutral carried at low
strength, inverted with the band. The primary action wears a light, vivid red and **it is the only thing on a page
wearing it**, darkening to a mid, vivid red under the pointer; the label inside it is a
near-black neutral. A disabled control and a disabled label are a light neutral and a mid
neutral and are never signalled by colour alone. Three colours carry meaning and nothing else
may borrow them: the colour that means a field is wrong is a light, vivid red, the colour that
means a field is validated is a light, vivid green, and the colour that means a field is
warned is a deep, soft red, which is also the colour of the warning glyph beside it. The failure panel sits on a near-white, muted red ground and the success
panel on a near-white, muted green one, and the panel's ground is a near-white warm neutral
where it meets the page. Build the palette in three layers, a raw ramp, an alias layer that
renames it and a semantic layer that assigns the roles above, and let components reference the
semantic layer only: that is what makes a band invertible by re-pointing two tokens rather
than by writing a second set of colours. The exact shades are yours, so long as they hold the
relationships and the exclusivity rules above.

**Typography.** One family, `Monument Grotesk`, a variable grotesque on a weight axis from
`200` to `1000`, self-hosted as one preloaded file with `font-display: swap`, subset to the
two locales rather than split across dozens of font responses, with the fallback stack
`"Monument Grotesk", Arial, sans-serif` exactly as written: Arial is the second stop
deliberately, because its metrics are close enough that a swap during load shifts line breaks
less than a generic sans would. The rendered weight is `400` everywhere. A family code on a
card is set at `6em` on a line height of `1`, dropping to `4.75em` at tablet width; the hero
headline at `3.75em` on `0.933`; a section headline at `3em`; a card title at `1.5em`; a
numbered item at `1.2em`; body copy at `1em`; a card description or table cell at `0.875em`;
and a table header, footnote or eyebrow at `0.75em`. Large type overlaps its own line box on
purpose. Figures align wherever amounts stack, which is every table and every metric bar.
Headlines are hand broken and the breaks are preserved rather than re-wrapped. Case is a
styling decision: eyebrows, annotations, button labels, navigation items and numbered titles
render uppercase with letter spacing while the strings behind them stay sentence case.

**Motion, by character and uniformity.** Six easing roles exist and no more should be added: a
house curve for every scale, wipe and sweep; a transform curve for the locale dropdown and the
route transition; a fade curve for every staggered reveal; a press curve; a focus curve; and
one named wipe for the product slider. A sweep takes longer to arrive than to leave, which is
what makes an element read as being placed rather than toggled. Everything decelerates hard
except the press, which is symmetric in both directions. Content does not appear, it arrives,
and it arrives in five named ways: blocks **fade** into place as they reach the window and
nothing else happens to them, no rise and no scale, and once revealed they stay revealed;
hand-broken headline lines **rise** one at a time, each from behind the line above it; a page
banner title is swept by a **marker bar, one bar per line**, never one per title; a long
statement on the firm profile brightens **word by word in reading order** as it passes up the
window and dims again on the way back; and every headline figure **spins up like an odometer**
through two full digit cycles, so it looks like it is winding up rather than nudging into
place. Every interactive element carries two copies of its own label, and pointing at it grows
and fades the visible copy while the smaller copy grows into place behind a coloured ground
that wipes open from the middle outward; because both copies are always present, moving the
pointer away mid-animation reverses cleanly without a jump. A press compresses the control
slightly more in height than in width, which reads as a key being pushed rather than as a
shrink. Under a reduced-motion preference every one of those is simply present and finished
from the start: content at full strength, lines at home, words bright, the final figure
printed, the marker bar at full height, no smoothing on the scroll, and hover animation off
entirely. Respect that preference under every character, and gate hover effects on the device
having a fine pointer as well.

**Density and arrangement.** Comfortable rather than tight: rows and cells have room to
breathe because this is reading matter, not a queue to process, and the ruled cells do the
separating work that dividers and shadows would otherwise do. Space over dividers, and calm
over expressive. The public routes carry one persistent top navigation and nothing else: no
secondary navigation, no breadcrumb anywhere, and the current route's item marked by a change
of ground rather than by an underline. Each page leads with exactly one primary action,
visually distinct from every secondary one, and on a public route that action is the enquiry
band's submit; a page with two things competing to be the obvious next step has none. The
signed-in desk is the one surface with a different arrangement: a persistent sidebar beside a
table-first queue where a row is edited in place, and the edited row shows its new value at
once and returns to the previous one with a message if the save is refused.

**Responsive behaviour holds at every width between the named tiers.** There are three: a
laptop width and above, a tablet width, and a handset width. At the tablet breakpoint the five
navigation items fold into a single Menu toggle and the root type size stops shrinking, and
those two things happen at the same boundary on purpose, so nothing both reflows and rescales
at once. Below it the card grids go from two columns to one, the very large family codes come
down a size, and the drifting decorative shapes are calmed from four rates to two, because a
narrow viewport scrolls past content faster and a drift tuned for a wide screen reads as
jitter on a narrow one. **A specification table never makes the document scroll sideways**: it
is the one piece of content here that cannot be reflowed without destroying it, so it scrolls
horizontally inside its own cell with the first column held, and nothing else on the page
overflows sideways at any width. Every navigation target stays reachable at the narrow width.

**Accessibility is a floor, not a finish.** Text and its background meet WCAG AA contrast in
the committed light scheme and in the dark bands, and the pairs to check first are the greyer
labels at partial opacity on a dark ground; where one fails, raise the opacity rather than
changing the colour, because the ramp is the design and the opacity is decoration. Full
keyboard navigation with a visible focus ring, touch targets comfortably sized, real labels on
every field and on every icon-only control, and meaning never carried by colour alone.
**Every content image carries alternative text that says what it shows, and every decorative
image declares itself decorative** - which here means the drifting shapes, the texture fields
and the octagonal service glyphs are decorative and the tool renders, the platform wireframe
and the placeholder client marks are content. Two obligations are specific to this product and
both are required: a counting figure's digit strip must not be read out as a run of digits, so
mark the strips presentational and expose the target value once as text; and the form fields,
which are underlined with the field name sitting on the line rather than boxed, must each
carry a real label behind that placeholder, visually hidden if the composition requires it,
because the placeholder disappears the moment the visitor types.

## Technical requirements

Frontend: Astro with interactive islands. Backend: FastAPI. Storage: PostgreSQL, reached at
`DATABASE_URL`. Auth: app-implemented email and password with bearer tokens. Health:
`GET /api/health` returns `200`. Logging: structured request logs to stdout.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing
service available in this environment is PostgreSQL, and reaching for anything else is a
contract violation.

The rendering model is server-rendered pages with interactive islands, and it is observable:
every catalogue route, evidence route and editorial route arrives as complete HTML, so the
banner, the tables and the copy are readable in the response before any script runs, and only
the enquiry form, the locale control, the reveal behaviour and the desk hydrate as islands.
The dynamic surface of this product is small by design - two form submissions and one
signed-in queue - and the rest is content that does not change between requests.

PostgreSQL is already running and reachable at `DATABASE_URL`. Do not download, install,
compile or start a copy of it. Never hardcode a host or a port; read them from the
environment.

**No binary asset ships with this product.** No photograph, no raster render, no video, no
compiled model file, no icon font. The iconography is fifteen inline vectors and every one is
geometry that inherits its
colour from the surrounding text. Every texture field is a generated repeating pattern rather
than a tiled image, because the same pattern is used at four different scales. Every tool
render and the platform wireframe are drawn geometry produced at build time. Every client mark
in the partner grid is a generated placeholder plate carrying two or three letters, because a
real client mark is a third party trademark and naming a client is a commercial statement
about work performed. Where a portrait would go, use the initials of a role on a plain plate,
never a generated face. The well profile is drawn as inline vector geometry from the case
record's own measurements rather than shipped as a picture of a chart: a chart shipped as an
image is a number that cannot be checked, on a product whose entire argument is that its
numbers can be checked. One font file ships, subset to the character sets the two locales
need.

Performance: the largest element painted on first load must be the hero headline, not any
media. Nothing
else may be allowed to become the largest paint by arriving earlier or larger. The heavy
behaviour loads late: the decorative and scroll-driven work is requested only as its band
approaches the window, and none of it is requested at all under a reduced-motion preference.
No third party script is loaded from anywhere; there is no runtime network.

Every response carries its own title and description, and no two routes share them.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

### engineer

`id`, `email` (unique), `password_hash`, `display_name`. Two seeded rows.

### product_family

`code` (unique), `class_name`, `description`, `summary`, `position` (integer, the index
order). Five rows: FRS, SVR, TRANSFER X1, TRANSFER X3, TRANSFER X6.

### product_variant

`family_code` (references `product_family.code`), `label`, `position`. `label` is unique
within a family. Ten rows across the five families.

### spec_row

`family_code`, `parameter`, `position`, and one cell per variant. A cell whose value has not
been measured stores the single dash character, which is what the table renders. Stored, not
substituted at render time, so an unmeasured cell and a missing row are different things.

### well_case

`well_number` (unique, and the route key), `field_name`, `region`, `geometry`, `run_month`
(month and year, no day), `tool_line`, `pipe_line`, `result_lines` (ordered, hand broken),
`verdict`, `position`. Ten rows. List order is newest first by `run_month`.

### case_metric

`well_number`, `kind` (`headline`, `profile` or `result`), `provenance`, `before`, `after`,
`unit`, `delta`, `sign`, `label`, `run_label`, `position`. **`provenance` is required and has
no default**, and `before` and `after` are stored rather than derived from `delta`: a
percentage delta cannot reconstruct the absolute pair, and the product prints both.

### case_conclusion

`well_number`, `position`, `title`, `badge`, `body`.

### case_product

`well_number`, `family_code`, `variant_label`. This join is what makes the cross-link resolve
in both directions, so it is a real table rather than a string on the case.

### modelling_request

`id`, `request_ref` (unique), `first_name`, `last_name`, `email`, `phone` (nullable),
`message` (nullable), `consent` (boolean), `locale`, `source_route`, `status`,
`assigned_to` (nullable, references `engineer.id`), `submitted_at`. `status` is one of
`new`, `modelling`, `configured`, `reported`, `declined`, with that exact casing, and
`request_ref` is the reference shown back to the visitor.

### subscriber

`email` (unique), `consent`, `locale`, `subscribed_at`.

Invariants, each stated as a property of the running system:

- A modelling request exists only where consent was given. A submission without it leaves the
  table exactly as it was.
- A request's status follows the order above one step at a time, except that `declined` is
  reachable from any state. Any other transition is rejected as invalid with a reason and the
  stored status does not change.
- Submitting the identical enquiry twice in immediate succession leaves exactly one row, and
  the second attempt reports the reference the first one created. The stored row is not
  written a second time.
- Subscribing an address that is already subscribed leaves exactly one row for that address.
- A case metric without a provenance value is not publishable and does not render.
- Every product variant appears in exactly one size table column set.
- Every case joins at least one product variant.
- No stored well data a visitor submitted is ever edited afterwards, and no request row is
  ever removed.

**Seed data.** Two engineers, `engineer@example.com` and `engineer2@example.com`, both with
the corpus password. Five product families and their ten variants. Ten well cases running from
November 2025 down to February 2025, with well 22061 seeded complete: three headline metrics
(4,025 m total depth, 2,938 m reach, 100 tools run), three profile cards, three result cards
and three conclusions. One modelling request, reference `REQ-1001`, status `new`, assigned to
nobody, so the queue is never empty on a fresh install. Seeding must be idempotent -
restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual specification in full. Nothing graded lives only here.

**Information architecture.** Twelve public routes and no more, one persistent header, no
secondary navigation and no breadcrumb anywhere, so a reader is never more than one click from
anywhere. The layering of the page is shallow and fixed: a cell ground, its content above it,
a card foreground above its media, a hover layer above that, then the odometer strips, the
marker bars, the depth readout, the enquiry feedback panels, the header and its blur, and the
menu panel and route-transition curtain at the top. Keep the descent sequence's rendered layer
*behind* the document rather than in front of it: the document's dark bands are what let it
show through, and moving it in front inverts the whole mechanism.

**Scaling.** Type and spacing are sized as a fraction of the window rather than in fixed
units, so the page grows and shrinks as one piece instead of reflowing into a different
layout, and the scaling stops at a laptop width below and at a very large display above. A
build that hard-codes a rendered size is correct at exactly one window width.

**The page shell.** Header, then on every route but home a page banner carrying a bracketed
eyebrow, a large marker-swept title and one or two standfirst lines, then the route body, then
the enquiry band, then the footer. The privacy route omits the enquiry band; the contacts
route promotes the form to be the body.

**Global chrome.** The header, the footer, the enquiry band and the route transition are one
system shared by every route, and a preloader guard puts the hero headline into its final
state immediately if the reveal behaviour never runs, so a visitor whose script fails still
reads the hero rather than a blank band.

**The header.** Fixed to the top of the window on every route at a reserved height, built as a
row of cells with a hairline between each, continuous with the page rules: the header is not a
bar sitting on the page, it is the first row of the same sheet. Left, the wordmark, linking to
the locale home. Centre, five items: Cases, About, Products, Engineering, Contacts. Right, a
spacer cell that absorbs the remaining width, then a globe control opening the locale list,
then a single accent-tinted contact control. The left
and right gutters are real cells, not padding, and the rules that bound them continue down the
whole page. The active item's cell takes a lighter fill and keeps its own colour. Behind the
header sit five stacked blurred layers, each blurring twice as much as the one before and each
masked to reveal a band of its own height, so the blur deepens smoothly with distance below
the header edge instead of stopping at a hard line. The header detects whether the band under
it is light or dark and swaps its text, rule and icon colours between the light and inverse
members of the palette. At the tablet breakpoint the five centre items collapse behind a
toggle labelled Menu, whose panel is chamfered on its bottom two corners only because its top
edge meets the header, and whose items enter one after another on the tighter stagger ladder.

**The wordmark and the bracket motif.** Supply one inline vector wordmark, monochrome, drawn
so it inherits the surrounding colour, which survives a colour inversion without a second copy
because it is a solid single-colour shape with no internal light or dark detail. The eyebrow
bracket is the most-used vector on the site and wraps every eyebrow label as a matched pair,
the right member being the left rotated rather than a second drawing. It is a bracket with a
diagonal waist, stepping inward near the top and back out near the bottom, which is what gives
a label a machined look rather than a typographic one; substituting the literal bracket
characters from the typeface loses the motif. The wordmark's pictorial mark is that same
bracket mirrored and enclosed in a filled square, which is the one relationship in the identity
worth keeping.

**The rest of the iconography.** Fifteen inline vectors carry every symbol this
product draws, all of them geometry, all inheriting their colour from the text around
them. A language globe
drawn as an outline circle with one vertical meridian, one equator and two latitude arcs bowed
in opposite directions. A shallow dropdown chevron with rounded joints that rotates when the
locale list is open. A close cross drawn as a single closed filled outline rather than as two
strokes, so it takes a fill and not a stroke width. Four controls for the case list panel: a
close cross, a previous and a next arrow with a long shaft so it reads as a directional arrow
rather than a chevron, a reopen chevron, and a location marker as a teardrop with a ring
inside it. Three contact marks in the footer, each in a chamfered cell: an open envelope drawn
as a single stroked path with both flap diagonals meeting in the middle; a messenger mark as a
speech bubble with its tail dragged to the lower left with a handset glyph inside it; and a
send mark as a paper plane drawn as an outline with its internal fold lines, which is what
makes it read as folded rather than flat. And one filled accent flag, a rectangle with a
triangular point on its right end, which is the one vector that is always the accent colour
rather than inheriting.

**The chamfer.** Every button, tag, card preview, media well and contact mark has its corners
cut on a 45 degree bevel rather than rounded, and the cut is applied to **all eight corners,
not four**: the chamfer reads as a machined bevel precisely because it is symmetric, and a
four-corner variant reads as a speech bubble. Four cut sizes are in use, the smallest on a
small button ground, a middle one on contact marks and media wells, a larger one on the large
button ground, and the largest on a card preview ground. Two shapes are deliberately not
symmetric: the handset menu panel, cut on its bottom two corners only, and the tapered band
above the footer, which narrows on each side as it descends and makes the page appear to
funnel into the footer.

**Buttons.** One component, two sizes, one accent. Its padding is asymmetric, with more room
on the trailing side than the leading one, because the button carries a leading arrow glyph
and the optical centre of the label sits left of the box centre without it. Its ground is two
chamfered layers, a resting one and a hover one, driven by the same wipe as every other
interactive element. Focus uses its own curve and a fractionally darker colour than the resting
state.

**The eleven section types, and nothing else.** Every route is assembled from: the page
banner; an eyebrow and headline pair; a two column card grid; a numbered list of titles only;
a numbered list of titles with bodies; a result card row; a metric bar; a specification table;
a media well holding a tool render; a word-fill statement; and the enquiry band. Adding a
twelfth is a design decision rather than an implementation one, and the coherence of this
product comes from the smallness of that list.

**The home route, ten bands in this order.** A full-window hero on a dark ground carrying the
headline "Pushing the limits of drilling" hand broken across two lines, the standfirst
"Engineered systems that control friction, vibration, and load transfer - so the BHA stays
stable and longer reaches stay on plan.", and one large "View cases" control. An about band on
a light ground: the eyebrow "about us", the headline "From well data to verified field
results - one engineering loop.", a "Learn more" control, and three cards - Equipment, whose
body claims the full cycle of design, manufacturing, deployment and field support; Engineering
and modeling, whose body claims the run is modelled for the specific well with all constraints
and all risks; and Field support, whose body claims engineers on site tracking placement and
documenting the outcome. A "By the numbers" band with the headline "Results, proven" over "on
real projects" and two headline results, each an odometer with a range annotation above it and
a "View case" control below: "27 to 14 kN-m" labelled Torque, and "140 to 117 t" labelled Hook
load on POOH. **The annotation carries the before and after values and the odometer carries
the delta, and both are needed**: a delta alone is unfalsifiable and a pair alone does not read
at a glance. A dark process band with the annotation "Process", the headline "Friction
reduction while drilling. Proven by data." and the body "We follow four key steps to be
confident of success in challenging runs", carrying a wireframe drawing of an offshore
drilling platform in hairlines on near black in its left cell. A near-black **descent sequence** band
carrying the eyebrow "TORQ systems", the headline "Friction and vibration act in different
zones - the solution has to work in every one of them", the standfirst "Combined, these
solutions significantly extend lateral reach while drilling", a depth readout reading "0 m"
against a fading lattice of small squares, and three plain controls labelled "To start",
"Scroll" and "Skip". **Those captions are served in the markup rather than injected**, so they
are readable without script, and the skip control is the first focusable control inside the
band: the skip control releases the pin on the sequence and moves past it, and the restart
control returns it to the start. The hint is two looping marks on deliberately different
periods so the pair never settles into lockstep. If the rendered layer fails to initialise,
the pin releases immediately and the static state shows instead, and under a reduced-motion
preference the descent sequence is never requested at all. An equipment showcase on the light ground: three full-width panels, one per hardware
family, each with the family name at display size prefixed by a literal `//` - the prefix is
part of the heading string, not a border, and it is what makes the name read as a code rather
than as a title - a standfirst, a media well holding the tool render, a second end-on render
fading into the ground rather than ending at a rectangle, a numbered list with an accent square
marker per item, and a "Learn more" control. FRS carries five list items, SVR four and TRANSFER
X3 four. A case studies grid. A dark band of client marks, each a generated placeholder plate
in a chamfered cell whose label descends into place from above. A dark band listing every case
well by region with a control to open each, which is the same set the evidence index carries
and never the only path to it. Then the enquiry band, the tapered band and the footer.

**The product card.** The family code is the largest type on the page and the render under it
is small. That inversion is the card's whole character - the name is the product, the picture
is a footnote - and a build that makes the render the hero of the card will look like a
different product. The cell has no chamfer and no border of its own; it is bounded by the page
rules, which is why the grid reads as ruled cells rather than as floating cards.

**The case card**, the richest component here and the one worth building first. Geometry and
region at the top left, hand broken across two lines in the numbered-item size. The family
code centred at display size. Two configuration lines under it, each with a small square
marker, the first accent and the second grey. One to three hand-broken result lines at the
lower left, each rising into place from behind the line above it, which is why they must not
re-wrap. The month and year under that. A "View case" control at the bottom right on hover.

**The odometer.** One clipped strip per digit position carrying the digits `0` through `9`
**twice over**, translated so the target digit sits in the window. Two full cycles, not one: a
strip carrying the digits once can only travel downward to its target, and carrying them twice
lets a figure land by travelling through a dozen digits rather than two, which is what makes a
large number look like it is spinning up. The sign, the thousands separator and the unit are
static text between the strips, never on a strip, which is why the separator does not slide.
The depth readout on the home route is the one figure that is a continuous function of scroll
position rather than a figure triggered once: it counts back down when the visitor scrolls up,
and the lattice beside it thins and fades against the same value.

**The reveal behaviour.** One observer serves every revealing element on a route. It adds a
state class when the element crosses into the window from below, then stops observing it
permanently, so scrolling back up does not re-hide content and scrolling back down does not
re-run the fade. The stagger is a class chosen at build time from a small set of steps, not a
value computed per element at runtime, and the ladders cap at five or six members and repeat
rather than growing, which is what stops the last card in a long grid arriving long after the
first. Under a reduced-motion preference the state class is served in the markup and nothing is
observed at all.

**The scroll behaviour.** The document scrolls under a controller that smooths a wheel notch
into an eased travel, and everything driven from position reads one shared value per frame
rather than each computing its own relationship, which is what stops them drifting apart under
load. Some effects are triggered once on entry and must not reverse - the fade, the line rise,
the marker sweep and the triggered odometers. Others are driven from position and must reverse
- the word fill, the drifting decorative shapes, the footer reveal and the depth readout. The
footer is parked behind the document and revealed by the document sliding off it, with a dark
veil over it clearing as it comes, so the footer is at its darkest when it is least visible.
Twenty-three decorative shapes drift behind the content on the home, product and engineering
routes at four different rates, and they are the only decorative elements here. The smoothing
must be disabled under a reduced-motion preference, and it must not break the browser's own
find, anchor and page-key behaviour: `PageUp`, `PageDown`, `Home` and `End` must all work.

**Generated geometry.** The decorative shapes are chamfered outlines drawn in hairlines, in
four named families that drift behind the engineering route: shape-stack as three offset
octagons, shape-bloom as four rotated lobes about a centre, shape-vault as four nested
chamfered rectangles, and shape-trace as an open path with two right-angle turns, each family
member differing only in scale and rotation.
The service glyphs are concentric chamfered octagons, two to four deep, hairline stroked and
unfilled, with the fourth card's outermost outline dashed. The dot field is a repeating radial
pattern of fine dots on a regular lattice and the cross field is the same lattice carrying
small plus glyphs, both generated rather than tiled. Where a surface needs tooth, use a
generated grain at low strength. The tool renders are composed from primitives: the drill pipe
as a tube swept along a vertical head, a constant-curvature build section and a long horizontal
run; a tool joint as a short wider cylinder at each pipe length; an FRS sleeve as a matte dark
cylinder with shallow longitudinal flutes and a plain bore, flanked by two thin collars; an SVR
body as a longer cylinder with two fluted sections either side of a plain waist; a TRANSFER sub
as a cylinder with three raised helical blades visibly separated from the body, which is the
kinematic decoupling the copy describes; and a drill bit as a short lobed body carrying rings
of small cutters and a central nozzle. Light them with six generated lighting lookups, one each for satin steel,
raw steel, dark satin pipe, matte composite, a grey studio and a red metal, so the metal reads
as brushed steel and the sleeves read as dark matte composite. No photography ships: the
production panels become generated monochrome plates with grain over them. **The contrast between the matte composite and the steel
beside it is the entire visual argument of the product**, so it is worth more care than
anything else in this paragraph.

**Responsive detail.** Two columns for the card grids at the laptop and tablet widths, one at
the handset width. The metric bar's three cells stack at the handset width. The footer columns
stack. The footer reveal is deliberately stronger at the handset width than at the laptop
width. A specification table scrolls inside its own cell and never scrolls the document.

## Constraints

- Single tenant. There is no organisation, no workspace and no tenant boundary.
- No cart, no checkout, no price, no currency and no payment of any kind.
- No public account. A visitor never signs in, and no public route requires a session.
- No third party vector map and no map provider token. The wells are listed and linked in
  plain markup.
- No rendered three-dimensional scene, no video and no animated media file.
- No search field, filter, facet, sort control or pagination on the evidence library. Ten
  cases is the whole library and every value a reader would search for is printed on every
  card.
- No map, office photograph, staff list or opening hours on the contacts route.
- No comments, no likes, no messaging, no file upload, no export and no print view.
- No email is sent by this product. A submission is recorded and read at the desk.
- No external network calls at runtime.
- No native or mobile application.
- The product must stay responsive with ten cases, five families, ten variants and a
  modelling request queue in the low thousands of rows.

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
| `POST /api/auth/login` | `email`, `password` | a bearer token and the engineer's `display_name` |
| `POST /api/auth/signup` | `email`, `password`, `display_name` | the created engineer |
| `GET /api/products` | none | a top-level JSON array of families with their variants |
| `GET /api/products/{code}` | none | one family with its results, mechanics, spec table and applications |
| `GET /api/cases` | none | a top-level JSON array of cases, newest first |
| `GET /api/cases/{well_number}` | none | one case with its metrics, goals, technology, results and conclusions |
| `POST /api/enquiry` | `firstName` (string, required), `lastName` (string, required), `email` (string, required), `phone` (string, optional), `message` (string, optional), `consent` (boolean, required and must be true), `locale` (string, required), `sourceRoute` (string, required) | the created request's `request_ref` and `status` |
| `POST /api/subscribe` | `email`, `consent`, `locale` | the subscriber's `email` |
| `GET /api/requests` | none, engineer only | a top-level JSON array of modelling requests, newest first |
| `GET /api/requests/{request_ref}` | none, engineer only | one modelling request with every submitted field |
| `PATCH /api/requests/{request_ref}` | `status` and/or `assigned_to`, engineer only | the updated request |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call
returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error with a reason, never a `5xx` and never a silent success. Bearer auth is required on
everything except login, signup, health and the public catalogue and evidence endpoints.

## Definition of done

A drilling engineer can read a field case for a real well, send their well data from the form
at the foot of that case, and get back a reference for the request they just made. One of the
firm's engineers signs in and reads that request with every field exactly as it was sent,
including which route it came from, moves it forward through the queue, and finds it unchanged
after the app restarts. Sending the same enquiry twice leaves one request, not two, and a
submission without consent leaves none at all.
