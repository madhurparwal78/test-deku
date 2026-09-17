# <BRAND> buildable product requirements

Zero-asset build specification, authored from the evidence ledger produced by
stages 0 and 1 against a captured reference site. Every colour, easing curve,
duration, grid formula, weight, radius and breakpoint below was measured.
Nothing was recalled. Every section also carries a plain-language block, marked
**In plain language.**, saying the same thing to a reader who will never open a
code editor.

The build has two halves and both are graded. The public surface is a
heavy-aesthetic marketing site whose fidelity is measured against the ledger.
The product behind it is a governed internal-tools platform whose correctness is
measured by the thirty graded workflows of Section 30, sorted into medium, hard
and expert. Neither half is optional and neither half can be passed by doing the
other one well.

---

## 0. How to use this document

### 0.1 What this is

A specification complete enough to build from without receiving a single binary
file. No photograph, typeface file, icon file, texture or video ships with it.
Section 33 gives a procedural recipe for every asset class the reference used.

This file has two readers and carries a register for each. The specification is
written for the agent doing the build and is exact enough to rebuild from. The
blockquote that closes every section is written for the person who commissioned
the build, in terms that can be checked against a running product rather than
against the ledger. Neither is a summary of the other, and they cannot drift,
because they sit in the same section under the same number.

### 0.2 Normative versus informational

Every statement about technology sits in exactly one register, and this document
labels which:

- **Capability requirement - normative.** What the build must do, stated without
  naming a library. These are the requirements.
- **Observed implementation - informational.** What the captured reference used,
  with the ledger tier that established it. Evidence, never instruction. The
  build is free to satisfy the capability with whatever the kit already draws.

Where a block carries no label, it is normative.

### 0.3 Placeholder tokens

Angle-bracket names are blanks. Replace every occurrence before shipping.

| Token | Meaning | Literal placeholder used in copy |
|---|---|---|
| `<BRAND>` | the product name, as it appears in running copy and in the footer wordmark | `Girder` - 6 characters, matching the reference |
| `<BRAND_SLUG>` | three-letter prefix on custom properties and module identifiers | `gdr` |
| `<SITE_ORIGIN>` | public origin of the marketing site | none |
| `<APP_HOST>` | origin the authenticated product is served from | none |
| `<ASSET_HOST>` | origin uploaded imagery and video are fetched from | none |
| `<DOCS_HOST>` | origin the documentation is served from | none |
| `<COMMUNITY_HOST>` | origin the community forum is served from | none |
| `<ANALYTICS_ID>` | analytics measurement identifier | none |
| `<CUSTOMER_1>` to `<CUSTOMER_6>` | named customers in the logo wall and the result cards | `Northgate`, `Bellweather`, `Halcyon`, `Trestle`, `Vantage`, `Ironwood` |
| `<AUTHOR_1>` to `<AUTHOR_3>` | bylines on the three article cards | `Dana Whitfield`, `Sam Okonjo`, `Riley Vance` |
| `<PARTNER_1>` to `<PARTNER_5>` | third-party products named in the import and connector strips | `Beacon`, `Loom`, `Quarry`, `Pilot`, `Anchor` |
| `<PAYMENTS_PARTNER>` | the payment provider named inside a sample prompt | `Ledgerline` |
| `<GAME_TITLE>` | the title of the game on the not-found route | `404 Blocks` |
| `<COPYRIGHT_YEAR>` | year in the footer copyright line | `2026` |

Every real name the reference carried has been replaced above: the product, six
customer companies, three article authors, five named third-party products, one
payment provider and one trademarked game. The placeholders were chosen at similar character counts,
because the reference line lengths were art-directed around the originals. The
footer wordmark in particular is set at display size across two thirds of the
viewport, and a name one character longer rewraps the entire footer.

### 0.4 Reading the numbers

Numbers are quoted as measured and must not be rounded. The reference derives
almost every dimension from a thirty-six column formula rather than from a table
of fixed values (Section 3.1), so reproducing the formula reproduces the
numbers, while hard-coding the numbers does not reproduce the formula.

Easing curves are quoted exactly as the reference stylesheet writes them,
including the reference's own inconsistent spelling of the same curve in two
places, because the fidelity gate compares this document against the stylesheet
rather than against a parser.

### 0.5 The two halves, and how they are graded

| Half | What is graded | How |
|---|---|---|
| Public surface, Sections 3 to 17 | visual and motion fidelity against the measurements in this document | reviewed, advisory, never moves the score |
| Product surface, Sections 18 to 29 | behaviour, through thirty end-to-end workflows | mechanically, and it is the entire score |

Section 30 is the graded set. It is the section to read first if you are
deciding what to build, and the section to read last before calling the build
finished.

### 0.6 What could not be measured

Section 34 lists the evidence gaps. Anything marked **inferred** is a
reconstruction rather than a measurement. The largest single gap is that the
authenticated product surface is behind a sign-in and could not be captured at
all, so Sections 18 to 29 are normative specification informed by the product
imagery on the public routes, not measurement. The second largest is that route
discovery reached twelve of the reference's routes and several of those resolved
to a not-found page, so the public surface is specified from five distinct page
types rather than from the whole site.

> **In plain language.** This build is described twice over, section by section.
> Once in exact terms for the machine doing the work: long tables of
> measurements, exact timings, exact colours, every number taken off the
> reference by a program rather than remembered by a person, because rounding
> any of them produces something visibly different. And once like this, for you,
> saying the same things in terms you can check by looking at the finished
> product. The two carry the same section numbers, so anything you want the
> detail on has a twin with the same number.
>
> **Anything written in angle brackets is a blank.** `<BRAND>` is where the
> product's name goes. There are about fifteen of them, all listed in the token
> table in the specification for this section. We have also used stand-in names
> everywhere the reference used real ones: the product itself, six customer
> companies, three writers with articles on the front page, five other companies
> named in passing, one payment provider and one trademarked game. Those are
> placeholders too, chosen
> to be roughly the same length as the originals, because the layouts were
> designed around how long the real words are. The giant name across the bottom
> of every page is the one to watch: one extra letter rearranges the whole
> footer.
>
> **What this is, in one sentence a friend would understand:** it is a tool that
> lets a company's engineers build the internal screens their staff use every
> day, connected straight to the company's real records, with the whole thing
> locked down tightly enough that the security team signs it off, and a very
> dark, very confident website out front selling exactly that promise.
>
> There are two halves and they are judged completely differently. The public
> website is judged on whether it looks and moves like the reference. The
> product behind the sign-in is judged by a robot that sits down and tries to do
> thirty specific jobs with it, and counts how many actually worked. That count
> is the score. A beautiful website with a broken product scores close to
> nothing.
>
> One more thing before you read on. The product behind the sign-in could not be
> photographed, because you need an account to see it. Everything in this
> document about the app builder, the permissions and the record-keeping is
> therefore a specification of what it must do, not a description of what the
> reference does. It is labelled that way wherever it appears, and Section 34
> lists every gap of that kind.

---

## 1. Product overview

### 1.1 What the product is

A platform for building internal software. A developer connects the company's
existing databases and services, assembles screens over them by dragging
components onto a grid and binding them to queries, and publishes those screens
to colleagues who run them against production records. The platform's claim is
not that building is possible: it is that building is possible **without the
security team saying no**, and every part of the product is arranged around
defending that claim.

The public site sells the claim. The product has to be able to survive it.

### 1.2 The two surfaces

| Surface | Who sees it | What it must do |
|---|---|---|
| Marketing site | anyone | Establish that this is enterprise-grade, take a demo request, take a self-serve signup |
| Product | invited members of an organisation | Everything in Sections 18 to 29 |

### 1.3 What makes the public surface feel expensive

The reference is a heavy-aesthetic build in an unusually disciplined vocabulary.
It gets its register from six devices and very little else:

1. **A single near-black field.** The entire site sits on `#151515` with type in
   a warm off-white `#e9ebdf`. There is no light page anywhere in the captured
   set, and the document declares its colour scheme as dark rather than
   supporting both.
2. **A thirty-six column formula.** Every horizontal dimension is derived from
   `calc(1440px/36)`, so the layout is one rule rather than a table of
   breakpoint values. Section 3.1.
3. **One easing family, applied to everything.** Nine named curves, all
   symmetric around the same shape, with `cubic-bezier(0.72,0,0.12,1)` carrying
   the overwhelming majority of transitions. Section 6.1.
4. **Pixel icons.** Every icon is drawn as one-unit squares on a small integer
   grid rather than as curves. Section 4.
5. **Continuous slow motion.** Three infinite animations run at all times at
   very long durations: a gradient border at `18000ms`, a text shimmer at
   `6000ms` and a logo marquee at `140000ms`. Nothing about them is fast enough
   to read as an animation; they read as the page being alive. Section 6.4.
6. **A custom cursor with four states.** The pointer is replaced by a drawn
   cursor that carries a contextual label. Section 10.

Nothing bounces, nothing parallaxes on the pointer except one illustration,
nothing is three dimensional, and there is no light mode. The restraint is the
design.

### 1.4 The public conversions

Three, in descending order of value to the business:

| Conversion | Where | Section |
|---|---|---|
| Demo request | its own route, and the header on every page | Section 14 |
| Self-serve signup | the header on every page, and the prompt composer | Section 8 |
| Newsletter subscription | the footer band on the home route | Section 11.7 |

The prompt composer of Section 8 is the unusual one. It sits at the centre of
the hero, accepts a typed sentence describing an application, and is the entry
point to the self-serve product. It is simultaneously the site's most expensive
piece of interaction design and its primary funnel.

### 1.5 Audience

Two, and the site talks to both at once without splitting into two sites: the
engineer who will build with it, and the person who will have to approve it. The
copy deck of Section 32 alternates between them almost line by line, and the
build must not resolve that tension by dropping either voice.

> **In plain language.** This is a tool for building the screens a company's own
> staff use: the page where support looks up an order, the page where an
> operations team approves a refund, the page where a warehouse marks a shipment
> late. Companies have always built these badly and slowly. This product makes
> them fast to build, and its real promise is that the fast version still passes
> the security review.
>
> There are two things to build. A public website selling that promise, and the
> actual product behind the sign-in.
>
> The website is very dark, almost black, with warm off-white writing on it.
> There is no light version of any page. Everything on it lines up to an
> invisible grid of thirty-six columns, and almost everything that moves uses the
> same single motion, so the whole site feels like one object rather than a
> collection of pages. Three things move continuously and extremely slowly: a
> glow that creeps around the edge of the main box, a shimmer that crosses a line
> of text, and a strip of customer logos sliding past. All three are slow enough
> that you do not catch them moving; you just notice the page is not dead. Even
> the mouse pointer is replaced with a drawn one that changes shape and picks up
> a small label depending on what it is over.
>
> The website wants three things from a visitor, in this order of value: book a
> demo, start using it for free, or join the mailing list. The most interesting
> piece on the page is the big box in the middle of the first screen, where you
> type a sentence describing the app you want. It is both the prettiest thing on
> the site and the front door to the product.
>
> One last thing worth understanding about the writing on this site: it is
> talking to two people at once. The engineer who will build with it, and the
> manager who has to sign it off. Almost every paragraph swaps between them. It
> would be easier to pick one, and picking one would lose the site.

---

## 2. Information architecture

### 2.1 Public route table

Twelve routes were reached by the capture. Five carry distinct page types and
are specified individually; the remainder resolved to the not-found route of
Section 15 and are recorded here because that is itself a measured fact about
the reference.

| Route | Page type | Section | Notes |
|---|---|---|---|
| `/` | Home | Section 11 | The longest page on the site by an order of magnitude |
| `/ai` | Platform pillar | Section 12 | One of four pillar pages the navigation promises |
| `/blog` | Index | Section 13 | Article index with a category taxonomy |
| `/demo` | Conversion form | Section 14 | Also reached as `/demo` with a source parameter |
| `/404` | Not found | Section 15 | Carries a playable game, per Section 15.2 |

### 2.2 Routes the navigation promises

The header and footer of Section 5 name forty-one destinations between them. The
capture reached five of those. The remainder are specified as required routes
without page-level layouts, because the ledger holds their labels but not their
contents:

| Group | Destinations |
|---|---|
| Platform | Build, Launch, Scale, Govern |
| Capabilities | App builder, AppGen, Agents, AI primitives, AI app security, Workflows, Database, External apps, Mobile apps, Self-hosting |
| Audience by team | Data, Engineering, Operations |
| Audience by industry | Financial services, Manufacturing |
| Audience by size | Enterprise, Startups |
| Discover | App gallery, Integrations, Templates, Utilities, Customer stories, Videos, Resource hub, Interactive tour |
| Developers | Documentation, Community, University, API reference, RPC reference, CLI reference, Hire a developer |
| Company | About, Careers, Partners, Support, Newsroom |
| Legal and trust | Terms of use, Privacy policy, Security, Trust Center, Changelog, Status, Site map |
| Conversion | Pricing, Use cases, Sign in, Book a demo, Start for free |

**Capability requirement - normative.** Every destination above resolves. A
navigation that promises forty-one pages and delivers five is the defect this
table exists to prevent, and the not-found route is not an acceptable answer for
a link the site itself renders.

### 2.3 Product route table

The authenticated surface. Reconstructed, per Section 34.2.

| Route | Purpose | Section |
|---|---|---|
| Sign in, second factor, invitation | authentication | Section 18 |
| Workspace home | the app list | Section 22.1 |
| App editor | authoring | Section 19 |
| App runtime | the published app, at its own address | Section 19.1 |
| Resources | connections and credentials | Section 22.2 |
| Administration | members, groups, permissions, policies, audit | Section 22.3 |

### 2.4 Two rules the route structure carries

1. **The editor and the runtime are different addresses and different bundles.**
   An end user's session never loads editor code, per Section 23.1.
2. **A published app's address is stable across releases.** Promotion changes
   what is served at the address, never the address, so a link an end user
   bookmarked survives every release, per Section 27.3.

> **In plain language.** The site is arranged in two layers, and they barely
> touch each other.
>
> The public layer is the website: the front page, a page for each part of the
> platform, a blog, a page for booking a demo, and the page you land on when a
> link is wrong. We were able to photograph five kinds of page. The menus promise
> around forty destinations, and every one of them has to actually go somewhere.
> A menu full of links to nowhere is worse than a smaller menu, and it is the
> most common way a site like this falls apart six months after launch.
>
> The private layer is the product: signing in, your list of apps, the screen
> where you build one, the screen where your colleagues use one, the place you
> set up connections to your databases, and the administration screens.
>
> Two rules about the private layer are worth knowing now. The screen for
> building an app and the screen for using one are completely separate, and
> somebody who only uses apps never downloads the building tools at all: it makes
> their pages lighter and it means there is nothing there for them to poke at.
> And the address of a published app never changes when you publish a new
> version, so a link somebody saved a year ago still works.

---

## 3. Design system

### 3.1 The scaling rule

Every horizontal dimension on the public surface derives from one formula. This
is the most consequential measurement in the document, because building any
component before it is settled means rebuilding that component.

| Property | Value |
|---|---|
| Column count | `36` |
| Column width | `calc(1440px/36)` |
| Inner grid width | `calc(calc(1440px/36)*calc(36 - 2))` |
| Inner grid ceiling | `1440px` |
| Document width | `1425px` |
| Outer gutter | `calc((1425px - calc(calc(1440px/36)*calc(36 - 2)))/2)` |
| Site maximum width | `2240px` |

**Capability requirement - normative.** The grid is expressed as these
declarations, not as their evaluated results. Two of the seven values are
themselves expressions over the other two, and a build that flattens them to
pixel constants produces a layout that is correct at one width and wrong
everywhere else.

The two subtracted columns in the inner-width formula are the outer gutters: the
content occupies thirty-four of thirty-six columns and the remaining two are
split either side.

### 3.2 Spacing

| Token | Value |
|---|---|
| `--spacing` | `0.25rem` |
| `--spacing-hairline` | `0.0625rem` |
| `--spacing-half-hairline` | `0.03125rem` |

The hairline is a design-system decision rather than a rounding artefact: it is
the border width on cards, table cells, the logo wall and the footer columns,
and it is what keeps a page of boxes from reading as a page of boxes.

### 3.3 Colour tokens

The reference carries a three-layer token system: raw ramps, semantic surface
roles, and per-component state sets. All three layers are reproduced, because
the component layer is what makes the interface consistent and it cannot be
derived from the other two.

**Layer one, the neutral ramps.**

| Token | Value |
|---|---|
| `--raw-neutral-dark-black-0` | `#000` |
| `--raw-neutral-dark-black-1` | `#0e0e0e` |
| `--raw-neutral-dark-black-2-primary` | `#151515` |
| `--raw-neutral-dark-black-3` | `#242424` |
| `--raw-neutral-dark-black-4` | `#2e2f2d` |
| `--raw-neutral-dark-black-5` | `#3f403d` |
| `--raw-neutral-light-white-0` | `#fff` |
| `--raw-neutral-light-white-1` | `#f7f8f4` |
| `--raw-neutral-light-white-2-primary` | `#e9ebdf` |
| `--raw-neutral-light-white-3` | `#cbccc4` |
| `--raw-neutral-light-white-4` | `#b6b8af` |
| `--raw-neutral-light-white-5` | `#94958e` |

**Layer one, the eight accent ramps.** Each accent carries seven steps, in the
order darkest, darker, dark, primary, light, lighter, lightest.

| Accent | darkest | darker | dark | primary | light | lighter | lightest |
|---|---|---|---|---|---|---|---|
| blue | `#101e2d` | `#1b2e44` | `#2d4c71` | `#518dd2` | `#71a2da` | `#b0ccea` | `#d8e6f3` |
| green | `#081e19` | `#0e352c` | `#185849` | `#4d9987` | `#6eac9c` | `#afd1c6` | `#d7e9e0` |
| orange | `#2b1713` | `#491f16` | `#793325` | `#e8765e` | `#ec8f7a` | `#f5c2b2` | `#fae1d6` |
| pink | `#280d28` | `#3d163d` | `#652466` | `#cc64ce` | `#d581d7` | `#e8bae8` | `#f4ddf2` |
| purple | `#271c3f` | `#3f2a68` | `#53397c` | `#9874d2` | `#ab8eda` | `#d0c1ea` | `#e8e1f3` |
| red | `#2f0909` | `#531717` | `#832424` | `#ef4444` | `#ff7171` | `#fca9a9` | `#ffcfcf` |
| yellow | `#301a08` | `#4a2b11` | `#7c481c` | `#eca438` | `#efb55b` | `#f6d6a0` | `#fbebcc` |
| lime | `#272502` | `#56521e` | `#8d8737` | `#e0d643` | `#f9ec75` | `#f7eda9` | `#fcf8de` |

The gray accent is four steps rather than seven: `#282522`, `#433e38`,
`#8b867f`, `#c8bfb5`, with `#ded9d3` as its lightest.

**Layer one, the alpha ladders.** Two ladders, one per neutral, at six and seven
stops. They are what every scrim, hairline and muted rule on the site is made
of, and they are quoted here as eight-digit values because that is how the
reference declares them.

| Stop | On `#151515` | On `#e9ebdf` | On `#f7f8f4` |
|---|---|---|---|
| 0 | `#15151500` | `#e9ebdf00` | `#f7f8f400` |
| 6 | `#15151510` | `#e9ebdf10` | `#f7f8f410` |
| 12 | `#1515151f` | `#e9ebdf1f` | `#f7f8f41f` |
| 20 | - | `#e9ebdf33` | `#f7f8f433` |
| 24 | `#1515153d` | - | - |
| 40 | `#15151566` | `#e9ebdf66` | `#f7f8f466` |
| 60 | `#15151599` | `#e9ebdf99` | `#f7f8f499` |
| 80 | - | `#e9ebdfcc` | `#f7f8f4cc` |
| 90 | - | - | `#f7f8f4dd` |

**Layer two, the semantic surfaces.**

| Token | Value | Role |
|---|---|---|
| `--surface-background-base` | `#151515` | the page |
| `--surface-background` | `#161212` | raised panels |
| `--surface-background-muted` | `#0e0e0e` | recessed wells |
| `--surface-background-focused` | `#242424` | hovered or focused panel |
| `--surface-text-primary` | `#e9ebdf` | body and headline |
| `--surface-text-muted` | `#cbccc4` | secondary copy |
| `--surface-text-disabled` | `#b6b8af` | disabled |
| `--surface-text-base` | `#f6f6f4` | inverted contexts |
| `--surface-text-code-expression` | `#59a7cb` | expressions inside the composer |
| `--surface-stroke` | `#354045` | panel border |
| `--surface-details-neutral` | `#e9ebdf` | rules and dividers |
| `--surface-details-logo-bg` | `#e9ebdf` | logo tiles |
| `--surface-selection-background` | `#ffe44d` | text selection |
| `--surface-selection-text` | `#161212` | text selection |
| `--surface-lightbox-scrim` | `#0009` | overlay scrim |
| `--surface-lightbox-active` | `#000c` | overlay at rest |

**Layer two, the semantic states.** Three roles, four steps each.

| Role | 8 | 10 | 11 | 12 |
|---|---|---|---|---|
| critical | `#e79295` | `#f15264` | `#c72844` | `#651722` |
| warning | `#e0a24e` | `#f1a42e` | `#aa6800` | `#4b371d` |
| success | `#52bb9d` | `#11997a` | `#008163` | `#1a3c32` |

**Layer three, the component sets.** Every interactive component declares a full
state set rather than deriving hover from opacity. Four are given in full here;
the remainder follow the identical shape and are listed in Section 5.

| Component | State | Background | Text | Icon | Stroke |
|---|---|---|---|---|---|
| Button primary | default | `#e9ebdf` | `#151515` | `#151515` | - |
| Button primary | hover | `#fff` | `#151515` | `#151515` | - |
| Button primary | active | `#fff` | `#15151500` | `#151515` | - |
| Button tertiary | default | `#242424` | `#e9ebdf` | `#e9ebdf` | - |
| Button tertiary | hover | `#2e2f2d` | `#e9ebdf` | `#e9ebdf` | - |
| Button tertiary | active | `#2e2f2d` | `#e9ebdf00` | `#e9ebdf` | - |
| Nav item | default | - | `#e9ebdf` | `#e9ebdf` | `#e9ebdf66` |
| Nav item | hover | - | `#f7f8f4` | `#f7f8f4` | `#e9ebdf66` |
| Nav item | active | - | `#cbccc4` | `#cbccc4` | `#e9ebdf66` |
| Nav item | inactive | - | `#e9ebdf66` | `#e9ebdf66` | `#e9ebdf66` |
| Input | default | `#e9ebdf00` | `#e9ebdf` | - | `#e9ebdf10` |
| Input | hover | `#e9ebdf33` | `#e9ebdf` | - | `#e9ebdf1f` |
| Input | focused | `#f7f8f4` | `#151515` | - | `#15151500` |

Two details in that table are the whole reason layer three exists. The active
state of every button sets its **text** to a fully transparent value while
leaving the icon opaque, which is how the reference produces a press that reads
as the label being punched out rather than dimmed. And the input inverts
completely on focus, from transparent-on-dark to solid light with dark text,
which is a far larger state change than a focus ring and is the single most
recognisable interaction on the forms.

The secondary button carries the same six-value set once per accent, in blue,
gray, green, orange, pink, purple, red and yellow, with the primary as the
default stroke, the lighter step as hover and active stroke, and the text going
transparent on active. Eight accents times six values is forty-eight tokens and
they are all in the ledger.

### 3.4 Typography

**Observed implementation - informational.** Four families, all licensed rather
than open: a variable grotesque at weights `100` to `900`, a fixed grotesque at
`400` and `700`, a serif at `400` and `500` with italics, and a display face at
`100` and `300`. All are declared `font-display: swap`.

**Capability requirement - normative.** Section 33.4 gives the substitution.
The build ships no typeface file that is not open-licensed, and the fallback
stack is metrically matched so that the swap does not move the layout.

Weights, as tokens:

| Token | Value |
|---|---|
| `--font-weight-body` | `300` |
| `--font-weight-headline` | `300` |
| `--font-weight-headline-xxs` | `380` |
| `--font-weight-title` | `570` |
| `--font-weight-semibold` | `600` |
| `--font-weight-bold` | `700` |

The two fractional weights are the signature. `380` and `570` are only reachable
on a variable face, and they are what stops the interface type from reading as
either regular or bold.

Tracking, as tokens:

| Token | Value |
|---|---|
| `--letter-spacing-headline-xxl` | `-0.031em` |
| `--letter-spacing-headline-xl` | `-0.022em` |
| `--letter-spacing-headline-lg` | `-0.02em` |
| `--letter-spacing-headline-md` | `-0.01em` |
| `--letter-spacing-headline-sm` | `-0.01em` |
| `--letter-spacing-headline-xs` | `-0.01em` |
| `--letter-spacing-headline-xxs` | `-0.01em` |
| `--letter-spacing-body` | `0.01em` |
| `--letter-spacing-title` | `0.02em` |

Tracking tightens as size grows and opens as size shrinks, which is ordinary
practice done properly: the display sizes are tightened by roughly three percent
and the small caps label is opened by two.

The rendered scale, measured across the captured routes and quoted at the
fractions it actually produced:

| Size | Weight | Line height | Uses | Where |
|---|---|---|---|---|
| `16px` | `400` | `24px` | 14944 | body copy, the default |
| `12px` | `400` | `14.4px` | 2131 | captions and labels |
| `12px` | `300` | `12px` | 1458 | small caps eyebrows |
| `20px` | `380` | `24px` | 717 | card headings |
| `14px` | `400` | `16.8px` | 553 | dense interface copy |
| `36px` | `100` | `36px` | 437 | section headings |
| `24px` | `380` | `28.8px` | 343 | subheadings |
| `60px` | `400` | `60px` | 294 | display |
| `28px` | `100` | `28px` | 217 | display, mobile |
| `10.4px` | `400` | `12.48px` | 209 | legal and footnote |
| `48px` | `300` | `50.4px` | 5 | the rarest heading size on the site |

Line height is `1.5` at body sizes, `1.2` at caption sizes and exactly `1` at
display sizes. The `36px` and `28px` rows at weight `100` are the site's
headline voice, and setting them at any heavier weight is the single change that
would most damage the register.

### 3.5 Radii

| Token | Value |
|---|---|
| `--radius-sm` | `0.25rem` |
| `--radius-md` | `0.375rem` |
| `--radius-lg` | `0.5rem` |
| `--radius-xl` | `0.75rem` |
| `--radius-2xl` | `1rem` |
| `--radius-3xl` | `1.5rem` |

Measured in use, beyond the token set: `4px` on logo tiles and badges, `5px` on
inline thumbnails, `8px` on secondary controls, `12px` on filter chips, `20px`
on the bordered promo box, `24px` on the gradient-bordered composer, `36px` on
pill badges, `0px 0px 36px 36px` on the hero video frame, which is square at the
top and heavily rounded at the bottom, and a fully-rounded pill expressed as an
absurdly large radius on every circular control.

**Capability requirement - normative.** The pill radius is expressed as a value
large enough to guarantee a semicircle at any height, not as a per-component
half-height calculation. That is what stops a pill from becoming a rounded
rectangle when its content wraps.

### 3.6 Elevation and depth

The reference uses almost no shadow. Three shadow values exist in the whole
capture:

| Use | Value |
|---|---|
| Logo tile | a one-pixel spread ring in `rgb(233, 234, 231)`, with four empty shadow layers preserved ahead of it |
| Cursor label | `rgba(0, 0, 0, 0.12) 0px 1px 2px 0px` plus a half-pixel white ring |
| Feature card | `rgba(0, 0, 0, 0.35) 0px 68px 116px 0px` |

The third is the only real shadow on the site, and it is enormous: sixty-eight
pixels down and a hundred and sixteen of blur, at thirty-five percent black.
That single value is what lifts the feature card off a near-black page, where a
conventional shadow would be invisible.

Depth is otherwise carried by blur. Four backdrop blur values are in use:
`blur(16px)` on badges, `blur(8px)` on floating controls, `blur(6px)` on one
button, and `blur(3px)` on the cursor label and the background figures.

### 3.7 Theme

**Capability requirement - normative.** The public surface is dark only. The
document declares a dark colour scheme and a theme colour of `#151515`, and the
build must declare both, so that browser chrome, form controls and scrollbars
match rather than rendering light widgets on a black page.

The product surface of Sections 18 to 29 carries both themes. The token layers
of Section 3.3 are the mechanism: layer two is redefined per theme, layers one
and three are not.

### 3.8 Breakpoints

| Query | Uses | Role |
|---|---|---|
| `min-width: 400px` | 6 | large phone |
| `min-width: 640px` | 10 | small tablet |
| `min-width: 768px` | 69 | tablet, the dominant breakpoint |
| `min-width: 1024px` | 35 | small desktop |
| `min-width: 1280px` | 13 | desktop |
| `min-width: 1440px` | 15 | wide, and the token ceiling |
| `min-width: 1920px` | 5 | very wide |
| `max-width: 543px` | 2 | phone override |
| `max-width: 767px` | 5 | below tablet override |
| `max-width: 1011px` | 6 | below small desktop override |

Two height queries also carry layout, at `min-height: 724px` and
`min-height: 881px`, both used in their negated form as well. They govern the
hero, which fits itself to the viewport rather than to a fixed height.

Two capability queries are in use: `hover: hover` at eleven declarations and
`hover: none` at five, so the reference branches on pointer capability rather
than on width for its hover treatments. `prefers-reduced-motion: reduce` carries
thirteen declarations and `no-preference` carries three, which means reduced
motion is a real branch in the reference stylesheet and not an afterthought.

### 3.9 Depth ordering

| Layer | Value |
|---|---|
| Base | `0` |
| Raised | `1`, `2` |
| Sticky content | `10`, `20`, `30` |
| Overlay | `50`, `100` |
| Navigation | `1000` |
| Frame | `1500` |
| Modal | `2000` |
| Cursor | `3000` |
| Skip link | `9999` |

The cursor sits above the modal, which is correct and is the kind of thing that
is only ever discovered by opening a dialog with a custom cursor and watching
the cursor disappear behind it. The skip link sits above everything, which is
the only way a skip link works.

> **In plain language.** The design system is the set of decisions that get made
> once and then never argued about again, and this reference has an unusually
> strict one.
>
> **Everything lines up to thirty-six columns.** Not a table of sizes for phone,
> tablet and desktop, but one piece of arithmetic that produces all of them. That
> is why the site feels engineered rather than arranged. It also means the very
> first thing to build is that arithmetic, because every measurement in the rest
> of this document is derived from it, and doing it last means doing everything
> twice.
>
> **The colours are a system three levels deep.** At the bottom, plain ladders of
> each colour from nearly black to nearly white. In the middle, names for jobs
> rather than colours: the page, a raised panel, ordinary text, quiet text,
> a warning. At the top, every button and menu and box gets its own complete set
> of colours for resting, hovering and being pressed. That top level is the
> expensive one and it is the one that makes an interface feel considered rather
> than assembled.
>
> Two small things in there are worth knowing because they are what people
> actually notice. When you press a button, its label goes completely
> transparent while the little arrow stays, so the press reads as the word being
> punched out of the button rather than the button dimming. And when you click
> into a text box, it does not get a glowing outline: the whole box flips from
> transparent-on-black to solid pale with dark writing. It is a big, confident
> change, and it is the most memorable thing about the forms.
>
> **The type is set unusually light.** Headings are drawn in the thinnest weight
> the typeface has, at large sizes, tightened up so the letters almost touch.
> Body writing is a step heavier. There is almost nothing in between. Setting the
> headings any heavier is the single change that would most cheapen the site, and
> it is the change a build will drift towards by accident.
>
> **There is almost no shadow anywhere.** On a nearly black page an ordinary drop
> shadow is invisible, so the site uses only one real shadow, and it is enormous:
> a soft dark pool falling a long way below one card. Everything else that needs
> to feel like it is floating is blurred behind instead, like frosted glass.
>
> **There is no light version of the public site.** It is dark, and it tells the
> browser it is dark, so that the scrollbars and the browser's own furniture
> match instead of showing up as bright white strips against black.

---

## 4. Iconography

### 4.1 The rule that governs every icon

The reference draws icons as **one-unit squares on a small integer grid**, not
as curves. Thirty inline vectors were transcribed and the majority are built
entirely from `1` by `1` rectangles at integer coordinates. This is the site's
strongest single identity signal after the colour, and it is cheap to get right
and impossible to fake with a conventional icon set.

**Capability requirement - normative.** Icons ship as inline geometry, not as
files. Every icon in this section is given as coordinates and must be
reproduced from them.

### 4.2 The caret

Used on every navigation item with a submenu, on the mobile back control, and
rotated for direction. Drawn as a staircase of seven squares.

| Element | x | y | width | height |
|---|---|---|---|---|
| rect | 3 | 7 | 1 | 1 |
| rect | 4 | 6 | 1 | 1 |
| rect | 2 | 6 | 1 | 1 |
| rect | 5 | 5 | 1 | 1 |
| rect | 1 | 5 | 1 | 1 |
| rect | 6 | 4 | 1 | 1 |
| rect | 0 | 4 | 1 | 1 |

View box `0 0 7 12`. Rendered at `7` by `12` in the mobile back control and at
the same ratio inline in the navigation. The mobile back control rotates it by
ninety degrees; the desktop navigation item rotates it by minus ninety below the
small-desktop breakpoint and leaves it upright above.

Note that the shape is deliberately open at the point: there is no square at
`x=3, y=4`, so the caret is a chevron of two diagonal arms rather than a filled
triangle.

### 4.3 The action arrow

The most-used icon on the site. It appears inline after every link that leads
somewhere, and it is the only icon that animates.

| Attribute | Value |
|---|---|
| View box | `0 0 24 24` |
| Rendered | `24` by `24` |
| Path | `M12 5v2h2v2h2v2H4v2h12v2h-2v2h-2v2h2v-2h2v-2h2v-2h2v-2h-2V9h-2V7h-2V5z` |

The path is a right-pointing arrow drawn as a staircase in two-unit steps, which
is the same pixel-grid discipline expressed as a path rather than as rectangles.
Its resting transform is `matrix(1, 0, 0, 1, -8, 1.92)`, which is what sits it
optically on the text baseline rather than on the box baseline, and it moves on
hover per Section 6.5.

### 4.4 The search glyph

| Element | Attributes |
|---|---|
| circle | `cx=11 cy=11 r=8` |
| path | `m21 21-4.35-4.35` |

View box `0 0 24 24`, rendered at `16` by `16` in the header and at `16` by `16`
in the mobile menu. This is the one icon in the set drawn as true geometry
rather than on the pixel grid, which is a legitimate exception: a circle of
radius eight cannot be drawn convincingly from unit squares at this size.

### 4.5 The close and dismiss glyph

Shares the action arrow's path exactly, rendered at `24` by `24` and rotated by
the consuming component. One path serving two icons is a deliberate economy and
should be reproduced as one asset rather than two.

### 4.6 The forty-two-square ornament

A `0 0 40 40` figure built from forty-two unit squares, used as the decorative
mark in the feature cards. The captured run of coordinates traces a diagonal
from `(30, 20)` down to `(21, 29)` in single steps, with two squares repeated at
each end of the run.

| Element | x | y |
|---|---|---|
| rect | 30 | 20 |
| rect | 29 | 21 |
| rect | 28 | 22 |
| rect | 27 | 23 |
| rect | 26 | 24 |
| rect | 25 | 25 |
| rect | 24 | 26 |
| rect | 23 | 27 |
| rect | 22 | 28 |
| rect | 21 | 29 |

All squares are `1` by `1` and take `currentColor`, so the ornament inherits the
text colour of its card rather than carrying its own. The two duplicated squares
at the ends of the run are reproduced as found; they are how the reference
thickens the terminals without adding a second element.

### 4.7 The wordmark

| Attribute | Value |
|---|---|
| View box | `0 0 87 17` |
| Rendered in the header | `92` by `18` |
| Construction | one path plus a separate mark |

The mark is a stepped glyph in the same pixel language as the icons, set to the
left of the word. In the footer the same lockup is set at display size across
roughly two thirds of the viewport width, per Section 5.6.

**Capability requirement - normative.** The wordmark is `<BRAND>` and is
redrawn, not reproduced. What is normative is the ratio, the position of the
mark relative to the word, and that the mark is built from the same unit-square
vocabulary as the icons.

### 4.8 Icon colour and sizing

| Context | Size | Colour |
|---|---|---|
| Header navigation | `16` by `16` | `--nav-items-default-icon`, `#e9ebdf` |
| Inline in a link | `24` by `24` | `currentColor` |
| Mobile menu | `16` by `16` | `--surface-details-neutral-alpha-60`, `#e9ebdf99` |
| Feature card ornament | `40` by `40` | `currentColor` |
| Buttons | `16` by `16` | the button's own icon token, per Section 3.3 |

Icons in buttons take the button's icon token, which is not the button's text
token. That distinction is what allows the pressed state of Section 3.3 to fade
the label while keeping the arrow.

> **In plain language.** Every small symbol on this site is drawn out of tiny
> squares on a coarse grid, like an icon from an early computer, rather than
> with smooth curves. It is the second most recognisable thing about the site
> after its colour, it costs nothing, and using an ordinary off-the-shelf icon
> set instead would quietly undo more of the site's character than any other
> single substitution in this document.
>
> There are only about half a dozen distinct symbols in the whole thing: a small
> chevron for menus that open, an arrow that follows every link, a magnifying
> glass, a cross for closing things, a decorative diagonal of squares on the
> cards, and the logo. The arrow is the one that carries the site, because it
> sits after almost every link and it is the only symbol that moves.
>
> The magnifying glass is the one exception to the square-drawing rule, and it is
> allowed to be: a circle that small cannot be built out of squares without
> looking like a mistake rather than a style.
>
> One detail that matters more than it sounds: symbols inside buttons are
> coloured separately from the button's writing. That is what makes the pressed
> state work, where the word disappears and the little arrow stays.

---

## 5. Global chrome

### 5.1 The header

Fixed to the top of every route, at the full document width.

| Property | Value |
|---|---|
| Height | `5rem` |
| Height token | `--nav-offset`, `5rem` |
| Height plus banner | `calc(5rem + 2.5rem)` |
| Banner height | `2.5rem` |
| Sticky offset | `2.5rem` |
| Background at rest | `#15151500`, fully transparent |
| Background when scrolled | `#000c` |
| Background when a menu is open | `#000c` |
| Depth | `1000` |

The header is transparent over the hero and acquires a seventy-five percent black
field only after the page scrolls, which is why the hero video reads as
full-bleed. The transition between the two is carried by the site's default
transition of Section 6.1.

### 5.2 Header contents, left to right

| Item | Type | Behaviour |
|---|---|---|
| Skip link | anchor | Visually hidden until focused, then pinned at depth `9999`, per Section 25.2 |
| Wordmark | link to home | Section 4.7 |
| Solution | menu | Opens the expanded panel of Section 5.3 |
| Audience | menu | Opens the expanded panel of Section 5.3 |
| Resources | menu | Opens the expanded panel of Section 5.3 |
| Use cases | link | Direct |
| Pricing | link | Direct |
| Search | button | Opens the search overlay of Section 16, labelled with a keyboard hint |
| Sign in | link | To the product |
| Book a demo | button, tertiary | To Section 14 |
| Start for free | button, primary | To signup |

The search control carries a rendered keyboard hint in a `kbd` element, held at
zero opacity until the control is hovered or focused. The hint is the
platform-appropriate modifier plus `K`, and the shortcut must work globally, per
Section 16.2.

### 5.3 The expanded menu panel

**Capability requirement - normative.** The three menus open a single shared
panel rather than three separate dropdowns. The panel is positioned at the
header's own height, spans the document width, and animates as one object.

Measured behaviour:

| Property | Value |
|---|---|
| Position | absolute, at `top: 5rem`, `left: 0` |
| Transform at rest | `matrix(1, 0, 0, 1, 0, 0)` |
| Outer clip | `inset(-4px)` on the navigation shell |
| Background | `#000c` |

The panel's content is three column groups whose headings are set in the small
caps eyebrow of Section 3.4, at `12px` weight `300` with `0.02em` of tracking.
Group labels: Platform, Capabilities, Team, Industry, Type, Discover,
Developers, Company.

The `inset(-4px)` clip on the shell is four pixels larger than the shell in
every direction, which is how the panel's own shadow and border escape the clip
while the panel's content does not. Reproducing the clip at `inset(0px)` looks
identical until the panel opens.

### 5.4 The header conversion pair

Two controls sit together at the right, in tertiary and primary treatments,
which is the site's whole conversion strategy expressed as two buttons:

| Control | Treatment | Tokens |
|---|---|---|
| Book a demo | tertiary | background `#242424`, hover `#2e2f2d`, text `#e9ebdf` |
| Start for free | primary | background `#e9ebdf`, hover `#fff`, text `#151515` |

The pairing is normative. The high-intent, high-value action is the quieter of
the two, and the low-friction action is the loud one. Reversing them changes the
funnel.

### 5.5 The mobile header

Below the tablet breakpoint the three menus collapse into a single full-height
sheet. Measured:

| Property | Value |
|---|---|
| Nav height, phone | `5.5rem` |
| Nav height, tablet and above | `7.75rem` |
| Nav scale, phone | `0.58` |
| Nav scale, tablet and above | `1` |

The `0.58` scale factor is applied as a transform on the header contents rather
than as a separate set of type sizes, which is why the phone header is
proportionally identical to the desktop one rather than merely smaller. A
measured transform of `matrix(0.58, 0, 0, 0.58, 0, 0)` confirms it in use.

The sheet carries a Back control using the rotated caret of Section 4.2, so that
a submenu is a push rather than an expand.

### 5.6 The footer

Five link columns, a conversion pair, a social row, a legal row, and the display
wordmark.

| Property | Value |
|---|---|
| Background | `--footer-background`, `#151515` |
| Column rule | `--footer-border`, `#e9ebdf99` |
| Link colour | `--footer-text`, `#cbccc4` |
| Muted colour | `--footer-text-muted`, `#b6b8af` |
| Wordmark colour | `--footer-logo`, `#e9ebdf` |

Columns, in order: Platform, Capabilities, Audience, Resources, Company. Column
headings are the small caps eyebrow. Beneath the columns sit the same two
conversion controls as the header, then three social links, then the legal row
of Terms of use, Privacy policy, Security, Trust Center, Changelog, Status and
Site map, then the copyright line.

The display wordmark occupies the full width beneath all of it, set large enough
that the word alone spans roughly two thirds of the viewport with the mark to
its left. It is the last thing on every page and it is the site's signature.

### 5.7 The banner

A `2.5rem` strip above the header, carrying one announcement and a link. Its
height participates in the layout through `calc(5rem + 2.5rem)` rather than by
pushing content, so a route with no banner and a route with one place their
content identically relative to the header.

### 5.8 Buttons

Four treatments. All share the same geometry and differ only in tokens.

| Treatment | Where | Token family |
|---|---|---|
| Primary | the site's one loud action | `--btn-primary-*` |
| Secondary | eight accent variants, used on pillar routes | `--btn-secondary-<accent>-*` |
| Tertiary | the quiet companion to primary | `--btn-tertiary-*` |
| Text with arrow | inline in copy, the most common of the four | Section 6.5 |

Every treatment carries `default`, `hover` and `active`, and every `active` sets
the text token to a transparent value, per Section 3.3.

> **In plain language.** The bar across the top and the block across the bottom,
> which appear on every page.
>
> The top bar is see-through while you are at the top of the page, so the video
> behind it runs edge to edge without interruption, and it fades to almost solid
> black the moment you scroll. Three of its menu items open one shared panel
> rather than three separate dropdowns, which is why the menus feel like one
> object opening rather than three things taking turns.
>
> At the right sit the two things the site wants from you, and their loudness is
> backwards on purpose. Booking a demo is worth far more to the business, and it
> is the quiet dark button. Starting for free is the loud pale one. That is
> deliberate, because the loud button is the one that costs the visitor nothing,
> and swapping them would change who ends up doing what.
>
> On a phone the whole bar is not redesigned; it is shrunk to just over half
> size as one piece, so the proportions stay exactly right. The menus become a
> full-screen sheet that slides sideways with a back arrow, rather than a list
> of things that expand in place.
>
> At the very bottom, under all the links and the small print, the product's
> name is set enormous, spanning most of the width of the screen. It is the last
> thing on every page and it is the site's signature move.

---

## 6. Motion language

### 6.1 The easing family

Eleven named curves. Every one of them is symmetric around the same underlying
shape, which is why the site moves like one object.

| Token | Curve |
|---|---|
| `--<BRAND_SLUG>-ease-in-out` | `cubic-bezier(0.72,0,0.12,1)` |
| `--<BRAND_SLUG>-ease-in` | `cubic-bezier(0.12,0,0.72,0)` |
| `--<BRAND_SLUG>-ease-out` | `cubic-bezier(0.12,1,0.72,1)` |
| `--<BRAND_SLUG>-ease-in-back` | `cubic-bezier(0.12,0,0.72,-0.4)` |
| `--<BRAND_SLUG>-ease-out-back` | `cubic-bezier(0.12,1.4,0.72,1)` |
| `--<BRAND_SLUG>-ease-in-out-back` | `cubic-bezier(0.72,-0.4,0.36,1.4)` |
| `--<BRAND_SLUG>-ease-in-out-soft` | `cubic-bezier(0.72,0,0.36,1)` |
| `--<BRAND_SLUG>-ease-in-soft` | `cubic-bezier(0.64,0,0.76,1)` |
| `--<BRAND_SLUG>-ease-out-soft` | `cubic-bezier(0.24,0.01,0.36,1)` |
| `--<BRAND_SLUG>-sine` | `cubic-bezier(0.36,0,0.64,1)` |
| `--<BRAND_SLUG>-linear` | `cubic-bezier(0,0,1,1)` |

Read the numbers and the family becomes obvious: `0.12` and `0.72` recur in
every curve, swapped between the two control points depending on direction, and
the `back` variants push one control point past its bound to `-0.4` or `1.4`.
This is one curve authored once and reflected, not nine curves chosen.

The default, applied wherever a transition does not name one:

| Token | Value |
|---|---|
| `--default-transition-timing-function` | `cubic-bezier(0.72,0,0.12,1)` |
| `--default-transition-duration` | `0.15s` |

`cubic-bezier(0.72,0,0.12,1)` carries the overwhelming majority of declared
transitions on the site. If one value in this document had to be right, it is
that one.

### 6.2 Durations

| Duration | Uses | What it carries |
|---|---|---|
| `0.1s` | 4005 | colour and border on interactive elements |
| `0.15s` | 21 | the declared default |
| `0.2s` | 96 | small state changes |
| `0.3s` | 42 | transform plus opacity pairs |
| `0.4s` | 168 | the transform group, the site's standard move |
| `0.6s` | 21 | opacity on large elements |

The distribution is the point. Four thousand declarations at a tenth of a
second and one hundred and sixty-eight at four tenths means the site does almost
all of its state change faster than a reader can perceive it as motion, and
reserves visible motion for a small number of specific moves.

**Capability requirement - normative.** Transform, translate, scale and rotate
are transitioned as a group with identical duration and curve, per the measured
declarations. Transitioning `transform` alone while leaving the individual
properties untransitioned produces a component that snaps under one interaction
and eases under another.

### 6.3 The transition groups, as declared

The five groups that appear more than a hundred times each, reproduced as
authored:

| Group | Declaration |
|---|---|
| Default | `0.1s cubic-bezier(0.72, 0, 0.12, 1)` |
| Fade | `opacity 0.6s cubic-bezier(0.72, 0, 0.12, 1)` |
| Move and fade | `transform 0.3s cubic-bezier(0.72, 0, 0.12, 1), opacity 0.3s cubic-bezier(0.72, 0, 0.12, 1)` |
| Quick fade | `opacity 0.4s cubic-bezier(0.72, 0, 0.12, 1)` |
| Colour set | `color 0.3s cubic-bezier(0.72, 0, 0.12, 1), background-color 0.3s cubic-bezier(0.72, 0, 0.12, 1), border-color 0.3s cubic-bezier(0.72, 0, 0.12, 1), outline-color 0.3s cubic-bezier(0.72, 0, 0.12, 1)` |

Note that the reference writes the same curve with spaces after its commas here
and without them in the token definitions of Section 6.1. Both spellings are
reproduced as found.

### 6.4 The three continuous animations

Three animations run forever, at durations long enough that none reads as
motion.

| Animation | Duration | Timing | Iterations | Fill |
|---|---|---|---|---|
| Gradient border | `18000ms` | `linear` | infinite | `none` |
| Composer shimmer | `6000ms` | `linear` | infinite | `none` |
| Logo marquee | `140000ms` | `linear` | infinite | `none` |

Their keyframes:

| Animation | Keyframes |
|---|---|
| Gradient border | `0% { background-position: -50% -50% } 50% { background-position: 150% 150% } 100% { background-position: -50% -50% }` |
| Composer shimmer | `0% { background-position: 200% } 100% { background-position: -200% }` |
| Logo marquee | `0% { transform: translate(0) } 100% { transform: translateX(var(--distance-percentage, -50%)) }` |

The marquee's use of a custom property with a fallback of `-50%` is what makes
one keyframe serve rows of different content lengths: the row measures itself
and writes its own distance, and the fallback covers the duplicated-content case.

**Capability requirement - normative.** All three respect reduced motion by
stopping entirely rather than by shortening, per Section 25.4. A shimmer at a
tenth of the duration is worse for the reader it was disabled for than no
shimmer at all.

### 6.5 The link arrow, which is the site's signature interaction

Every text link that leads somewhere carries the arrow of Section 4.3 and an
underline that wipes rather than fades. Two keyframe sets carry it:

| Element | Keyframes |
|---|---|
| The link body | `0% { transform-origin: 100%; transform: scaleX(1) } 50% { transform-origin: 100%; transform: scaleX(0) } 50.01% { transform-origin: 0; transform: scaleX(0) } 100% { transform-origin: 0; transform: scaleX(1) }` |
| The underline | `0% { background-position: 100% 100%; background-size: 100% 1px } 50% { background-position: 100% 100%; background-size: 0% 1px } 50.01% { background-position: 0 100%; background-size: 0% 1px } 100% { background-position: 0 100%; background-size: 100% 1px } ` |

The `50.01%` stop is the mechanism and it must be reproduced exactly. At the
midpoint the underline has collapsed to zero width against its right edge; one
hundredth of a percent later its origin jumps to the left edge while it is still
invisible; then it grows back out to full width. The result is an underline that
retracts to the right and re-emerges from the left, which reads as the link
being replaced rather than merely highlighted. Interpolating between the two
origins instead, or rounding `50.01%` to `50%`, produces a symmetric wipe that
looks like nothing.

The underline is drawn as a background image, `linear-gradient(rgb(233, 235, 223), rgb(233, 235, 223))`,
sized `100% 1px`. Its muted variant uses `linear-gradient(rgb(203, 204, 196), rgb(203, 204, 196))`.

The arrow itself translates on hover, from its resting
`matrix(1, 0, 0, 1, -8, 1.92)`, under
`transform 0.4s cubic-bezier(0.72, 0, 0.12, 1)`.

### 6.6 The remaining named animations

| Name | Keyframes | Where |
|---|---|---|
| Fade in up | `0% { opacity: 0; transform: translateY(1rem) } 100% { opacity: 1; transform: translateY(0) }` | hero pillar content |
| Fade in | `0% { opacity: 0 } 100% { opacity: 1 }` | hero pillar content |
| Settle in | `0% { scale: 102% } 100% { scale: 100% }` | media on first paint |
| Bounce x | `0% { transform: translate(0) } 50% { transform: translate(.25rem) } 100% { transform: translate(0) }` | pillar tab links |
| Progress bar fill | `0% { transform: scaleY(0) } 100% { transform: scaleY(1) }` | feature tab timer |
| Gradient shift | `0% { background-position: 0% } 100% { background-position: 200% }` | badges |
| Chrome gradient shift | `0% { background-position: 0% } 100% { background-position: 400% }` | badges |
| Red light pulse | `0% { background-color: #f15264 } 100% { background-color: #e79295 }` | critical badge |
| Marquee | `0% { transform: translate(0%) } 100% { transform: translate(-50%) }` | image strips |
| Scroll left | `0% { transform: translate(0) } 100% { transform: translate(-50%) }` | logo grid |
| Scroll right | `0% { transform: translate(0, 0) } 100% { transform: translate(-20%) }` | partner strip |
| Shimmer | `0% { background-position: 200% 0 } 100% { background-position: -200% 0 }` | video placeholder |

**Settle in** is worth naming because it is the cheapest expensive-looking thing
in the whole set: media arrives at one hundred and two percent and relaxes to
one hundred, so every image on the site appears to come to rest rather than to
appear.

The **progress bar fill** exists twice with different keyframes, one animating
to `scaleY(1)` and one staying at `scaleY(0)`. The second is the paused state of
the feature tab timer, expressed as an animation that goes nowhere rather than
as a stopped animation, which keeps the element's animation state consistent
across tabs.

### 6.7 Hover, measured

The hover pass found two treatments across every captured route, and they are
the entire hover vocabulary of the public site:

| Selector | Property | From | To |
|---|---|---|---|
| Icon-bearing link | opacity | `1` | `0.8` |
| Text link | color | `rgb(233, 235, 223)` | `rgb(203, 204, 196)` |
| Text link | borderColor | `rgb(233, 235, 223)` | `rgb(203, 204, 196)` |
| Text link, `::before` | color and borderColor | `rgb(233, 235, 223)` | `rgb(203, 204, 196)` |
| Text link, `::after` | color and borderColor | `rgb(233, 235, 223)` | `rgb(203, 204, 196)` |

That both pseudo-elements shift with the parent is the detail worth
transcribing: the arrow and the underline are `::before` and `::after`, and a
build that colours only the anchor leaves the arrow at full brightness while the
text dims.

**Observed limitation.** The reference's hover work is largely transform-based
and the capture's property set is narrow, so the wipe of Section 6.5 appears in
this table only as a colour change. It is reconstructed from the keyframes and
the declared transitions rather than observed, per Section 34.4.

> **In plain language.** How things move.
>
> There are eleven named movements on this site and they are all the same movement
> reflected and stretched. That is why everything feels like it belongs to one
> object rather than to a collection of components, and it is the cheapest way to
> buy that impression. One of the eleven does almost all the work.
>
> Almost everything happens fast enough that you do not see it as movement at
> all: four thousand of the site's transitions are a tenth of a second, which
> registers as "the colour is different now" rather than as an animation. Visible
> movement is saved for a handful of specific moments.
>
> Three things move continuously and never stop. A soft light creeps around the
> border of the main box, taking eighteen seconds to go round. A pale sheen
> crosses the placeholder text every six seconds. And a strip of customer logos
> slides past taking well over two minutes to complete a lap. All three are far
> too slow to catch in the act. They are there so that the page never looks
> frozen, and if any of them were sped up to a normal animation speed the page
> would immediately look cheap.
>
> **The one interaction worth building carefully is the link underline.** When
> you hover a link, the underline does not fade or slide across. It shrinks away
> to the right until it is gone, and then grows back out from the left. The trick
> is a single hundredth-of-a-second beat at the halfway point where the line is
> invisible and jumps sides. Miss that beat and you get an ordinary sliding
> underline that nobody notices. Include it and the link reads as being swapped
> for a fresh one. It is the site's best small moment.
>
> One more worth having: pictures arrive very slightly too large and settle to
> their real size. It is almost imperceptible and it makes every image on the
> site feel like it came to rest rather than popped into existence.
>
> Finally, all of the continuous movement stops completely for anyone who has
> asked their computer to reduce motion. Not slowed down, not shortened.
> Stopped.

---

## 7. Scroll system

### 7.1 What is scroll-driven, measured

The home route drives twelve selectors from scroll position at desktop, eight at
tablet and seven at phone. The count itself is the finding: this is a site with
a small number of deliberate scroll effects, not a site where everything fades
in.

| Selector | Property | Distinct values across nine frames |
|---|---|---|
| Bobbing glass illustration, floating item | transform | 81 |
| Hero video frame | filter | 15 |
| Hero video frame | opacity | 14 |
| Logo marquee row | transform | 6 |
| Feature column | opacity | 3 |
| Header background figure | opacity | 2 |
| Link arrow | transform | 2 |
| Link underline | background image | 2 |
| Story media item | opacity | 2 |
| Story media group | opacity | 2 |
| Illustration group | filter | 2 |
| Bordered strip | transform | 2 |

Eighty-one distinct transform values across nine sampled frames means the
illustration is continuously scrubbed rather than stepped, and it is the only
element on the site of which that is true.

### 7.2 The document scroll state

| Property | Value |
|---|---|
| Root classes, all routes | `scroll-pt-nav-offset dark` |
| Scroll padding top | `--nav-offset`, `5rem` |

The root class set never changes across the nine sampled frames on any captured
route. **This is a significant negative finding.** The reference does not drive a
state machine from classes on the document element: there is no `is-scrolled`,
no `has-menu-open`, no scroll-direction class. Every scroll effect is local to
the element that carries it.

**Capability requirement - normative.** Scroll effects are implemented locally,
against the element's own intersection with the viewport, and not by writing
global state to the document element. A build that adds a scroll-direction class
to the root has invented a mechanism the reference does not have, and will
produce different behaviour whenever two effects disagree.

The scroll padding is what makes in-page anchors land below the fixed header
rather than behind it, and it is derived from the header height token rather
than duplicated.

### 7.3 Document heights, as sampled

| Route and breakpoint | Sampled scroll positions |
|---|---|
| Home, desktop | `0, 1318, 2746, 4064, 5492, 6810, 8238, 8783, 8783` |
| Home, tablet | `0, 1582, 3296, 4878, 6593, 8175, 9889, 11471, 13186` |
| Home, phone | `0, 1241, 2587, 3829, 5174, 6416, 7761, 9003, 9282` |

The desktop column is the interesting one: the last two samples are identical,
which means the page stopped scrolling before the final sampling position. The
home route at desktop is shorter than nine even samples, and the tablet layout
is half again as tall as the desktop one because the same content reflows to
fewer columns.

### 7.4 The hero video ramp

The most complex scroll effect on the site, and the one worth building
carefully.

The hero video frame carries fifteen distinct filter values and fourteen
opacity values across the scroll. Measured filter values include
`blur(0px)`, `blur(4.72697px)`, `blur(5.26563px)`, `blur(5.34086px)`,
`blur(7.12607px)` and `blur(8px)`. Measured opacity values include `0.109242`,
`0.332393`, `0.341796` and `0.409129`.

**Capability requirement - normative.** Blur and opacity ramp together, from
`blur(0px)` at full opacity to `blur(8px)` at low opacity, driven continuously
by scroll position rather than by a stepped set of classes. The fractional
values above are samples of a continuous ramp, not the ramp's definition:
reproducing the ramp reproduces them, and hard-coding them does not reproduce
the ramp.

The frame's radius is `0px 0px 36px 36px`, square at the top where it meets the
header and heavily rounded at the bottom, and the video inside it is masked
by a vertical gradient at the top so that it dissolves into the header rather
than ending at a line.

### 7.5 The masking gradients

Three mask families, all reproduced as measured:

| Mask | Value | Where |
|---|---|---|
| Vertical soft edge | `linear-gradient(rgba(0, 0, 0, 0) 0px, rgb(0, 0, 0) 28px, rgb(0, 0, 0) calc(100% - 28px), rgba(0, 0, 0, 0) 100%)` | scrolling panels |
| Horizontal soft edge | `linear-gradient(90deg, rgba(0, 0, 0, 0), rgb(0, 0, 0) -7.5px, rgb(0, 0, 0) calc(100% + 7.5px), rgba(0, 0, 0, 0))` | marquee rows |
| Wide horizontal edge | `linear-gradient(90deg, rgba(0, 0, 0, 0), rgb(0, 0, 0) -532.5px, rgb(0, 0, 0) calc(100% + 532.5px), rgba(0, 0, 0, 0))` | full-width marquee |

The negative offsets in the horizontal masks are not errors. They push the
opaque region beyond the element's own bounds, which produces a fade that is
wider than the element and therefore begins outside it. The three values,
`-7.5px`, `-232.5px` and `-532.5px`, are the same mask instantiated at three
widths, and they are derived from the element rather than authored.

Two gradients are declared with a custom property for the fade width:
`linear-gradient(90deg,transparent,#000 var(--mask-spacing)` and its spaced
variant. That is the mechanism; the pixel values above are its output.

### 7.6 The vertical scrim

The hero carries a top-down scrim as a nineteen-stop gradient from
`#15151500` through to solid, which is a hand-tuned approximation of a
perceptual fade rather than a linear one. The measured stops begin
`#15151500 0%`, `#15151501 0.9%`, `#15151502 2.4%`, `#15151505 4.5%`,
`#1515150b 6.9%`, `#15151513 9.9%`, `#15151520 13.5%`, `#15151531 17.5%`,
`#15151547 21.7%`, `#15151561 26.5%`, `#1515158a 33%`.

**Capability requirement - normative.** The scrim is reproduced as a multi-stop
gradient with an accelerating alpha curve. A two-stop linear gradient in its
place produces a visible band across the hero, which is the exact artefact the
nineteen stops exist to remove.

A second instance of the same construction exists on white,
beginning `#fff0 0%`, `#ffffff01 0.400001%`, `#ffffff02 1.2%`,
`#ffffff05 2.2%`, `#ffffff0b 3.4%`, `#ffffff13 4.9%`.

### 7.7 The grid lines

A decorative figure draws vertical rules at three densities:

| Spacing | Declaration |
|---|---|
| `40px` | `repeating-linear-gradient(90deg, rgb(77, 153, 135), rgb(77, 153, 135) 1px, rgba(0, 0, 0, 0) 1px, rgba(0, 0, 0, 0) 40px)` |
| `27.0833px` | the same, at `27.0833px` |
| `14.4231px` | the same, at `14.4231px` |

The colour is `#4d9987`, the green accent primary. The two fractional spacings
are the thirty-six column grid of Section 3.1 evaluated at two viewport widths,
which means the decorative rules are the layout grid made briefly visible rather
than an unrelated pattern. The same construction exists in the vertical
direction and against `--accent-background-color`.

> **In plain language.** How the page reacts to scrolling.
>
> Far less than you would expect, and that is a deliberate choice worth
> respecting. Twelve things on the front page respond to scrolling. Everything
> else is simply there.
>
> The one thing that is genuinely tied to your scrolling, moving continuously
> with it rather than playing once when it comes into view, is a floating glass
> illustration that drifts as you move. Everything else either fades in once or
> slides at its own pace regardless of you.
>
> The most elaborate effect is the video at the top. As you scroll away from it,
> it goes gradually out of focus and gradually fades, both at the same time, in
> step with your scrolling rather than on a timer. Its frame is square at the top
> and generously rounded at the bottom, and the video dissolves into the bar at
> the top instead of stopping at an edge.
>
> There is a detail in how those fades are made that is worth insisting on. Where
> the page fades from black to transparent, it does so through nineteen separate
> steps rather than two. That sounds like fussiness and it is not: a plain
> two-step fade produces a visible band across the picture, and the nineteen
> steps exist to remove it. Anyone rebuilding this will be tempted to simplify it
> and will reintroduce the band.
>
> And a nice piece of quiet craft: the faint vertical lines drawn across some
> sections are not decoration invented for the look. They are the site's own
> underlying column grid, briefly made visible.

---

## 8. The prompt composer

### 8.1 What it is

A large text field at the centre of the hero, into which a visitor types a
sentence describing an application they want. It is the site's primary
self-serve funnel and its most expensive piece of interaction design, and it is
the one component on the public surface that is genuinely an application rather
than a page element.

### 8.2 Geometry and treatment

| Property | Value |
|---|---|
| Radius | `24px` |
| Border | the animated gradient of Section 8.3 |
| Background | `--surface-background-base`, `#151515` |
| Placeholder colour | `--surface-text-muted`, `#cbccc4` |
| Token colour | `--surface-text-code-expression`, `#59a7cb` |
| Content padding | `1rem` |
| Shadow | `rgba(0, 0, 0, 0.35) 0px 68px 116px 0px` |

The shadow is the site's one real shadow, per Section 3.6, and it is applied
here. That is the whole reason it exists.

### 8.3 The gradient border

**Capability requirement - normative.** The border is a moving gradient
constrained to the border region, not a background bleeding out from behind the
card.

| Property | Value |
|---|---|
| Animation | gradient border pulse, `18000ms`, `linear`, infinite |
| Keyframes | `0% { background-position: -50% -50% } 50% { background-position: 150% 150% } 100% { background-position: -50% -50% }` |
| Radius | `24px` |
| Mask | `linear-gradient(rgb(255, 255, 255) 0px, rgb(255, 255, 255) 0px), linear-gradient(rgb(255, 255, 255) 0px, rgb(255, 255, 255) 0px)` |
| Composite | the two mask layers are composited so that only the ring survives |
| Pointer events | none |

The two-layer mask is the mechanism and it is the part a build will get wrong.
One layer covers the whole element, the second covers the element inset by the
border width, and the second is subtracted from the first. What survives is a
ring of exactly the border width, following the `24px` radius, through which the
moving gradient shows. Drawing the gradient on a parent and covering its middle
with an opaque child works until the card sits over anything other than a flat
colour, which on this page it does.

### 8.4 The placeholder shimmer

While the composer is unfocused, its placeholder text carries a slow sheen.

| Property | Value |
|---|---|
| Animation | shimmer text, `6000ms`, `linear`, infinite |
| Keyframes | `0% { background-position: 200% } 100% { background-position: -200% }` |
| Background | `linear-gradient(90deg, rgb(21, 21, 21) 0%, rgba(21, 21, 21, 0.6) 50%, rgb(21, 21, 21) 100%)` |
| Applied by | clipping the gradient to the text |

The gradient is authored in the page colour rather than in white: it is a
travelling *hole* in a dark overlay rather than a travelling highlight. On a
near-black page that reads as the text quietly brightening and dimming rather
than as a glare passing over it, which is the difference between this effect and
the loading shimmer of Section 6.6.

**Capability requirement - normative.** The shimmer stops on focus. A sheen
crossing text the visitor is actively typing is an active nuisance rather than a
flourish.

### 8.5 Token chips

Typing an at-sign in the composer opens a picker of data sources, and choosing
one inserts a chip rather than plain text.

| Element | Treatment |
|---|---|
| The at-sign | its own element, so it can be styled apart from the name |
| The name | `--surface-text-code-expression`, `#59a7cb`, underlined |
| The icon box | a `50%` radius container carrying the source's mark |

**Capability requirement - normative.**

1. A chip is **atomic**: one press of backspace at its trailing edge selects it,
   a second removes it whole, and the caret can never land inside it.
2. A chip carries a **reference**, not a label. Renaming the source it points to
   changes the chip's rendering and not the value the composer submits.
3. The picker is keyboard-navigable, filters as the visitor types after the
   at-sign, and closes on escape without removing the at-sign already typed.
4. Chips survive a paste and a copy round trip as chips.

This is the single most under-built component on sites of this kind. A composer
that renders the chip as coloured text and submits the raw string works
perfectly in a demonstration and breaks the moment a source is renamed or a
visitor edits the middle of their sentence.

### 8.6 The composer's furniture

| Element | Behaviour |
|---|---|
| Starter prompts | A menu of pre-written sentences that replace the field's contents |
| Submit | A circular control at the trailing edge, per Section 3.5's pill radius |
| Import strip | A control below the composer offering import from other builders, opening a list carrying `<PARTNER_1>` to `<PARTNER_5>` |
| Connector strip | A second control offering connection to external coding agents, carrying the same treatment |

Both strips render a horizontal cluster of overlapping source marks to the left
of their label, at `4px` radius each, with the leftmost on top.

### 8.7 Submission

**Capability requirement - normative.** Submitting the composer from the public
site is a signup, not a build. The sentence and any chips are carried through
the signup flow and are the first thing the visitor sees inside the product, so
that the promise made on the marketing page is kept by the first screen behind
it.

The composer never contacts a model from the public page, and never sends its
contents to an analytics destination.

> **In plain language.** The big box in the middle of the front page where you
> type a sentence describing the app you want.
>
> It looks expensive because of two things. A soft light travels slowly around
> its border, taking eighteen seconds to go all the way round, and it is a real
> ring of light following the rounded corners rather than a glow leaking out from
> behind the box. And it casts the only genuine shadow on the entire site: a
> large soft pool falling well below it, which is what lifts it off an almost
> black page where a normal shadow would be invisible.
>
> While you are not typing in it, the grey example text has a slow sheen passing
> across it. The sheen is made backwards from how you would expect: instead of a
> bright streak moving over dark text, it is a moving gap in a dark veil. On a
> near-black page that reads as the words breathing rather than as a glare. It
> stops the moment you click in, because a shimmer moving over text somebody is
> typing is just annoying.
>
> **The part that will be built wrong is the at-sign.** When you type an at-sign,
> a list of your data sources appears, and picking one drops a little coloured
> tag into your sentence. That tag has to behave as one object: one press of
> backspace selects it, another deletes the whole thing, and your cursor can
> never end up stuck inside the middle of it. It also has to remember which
> source it points at rather than just its name, so that renaming the source
> later updates the tag instead of breaking it. The easy version of this looks
> identical in a demonstration and falls apart the first time somebody edits the
> middle of their sentence.
>
> Finally: typing here and pressing the arrow signs you up. Whatever you typed
> travels with you and is waiting for you on the first screen inside. Losing it
> at the door would break the one promise the front page makes.

---

## 9. Marquee and logo systems

### 9.1 Why this is a section

Six of the site's twelve named animations are marquees, and the logo wall is the
single largest block of content on the home route. The reference treats
horizontal infinite scrolling as a design system component with one
implementation and several instantiations, and the build must too.

### 9.2 The one mechanism

| Property | Value |
|---|---|
| Keyframes | `0% { transform: translate(0) } 100% { transform: translateX(var(--distance-percentage, -50%)) }` |
| Timing | `linear`, infinite |
| Longest measured duration | `140000ms` |
| Measured transform mid-run | `matrix(1, 0, 0, 1, -1049.5, 0)` |
| Track | `display: flex`, `width: max-content`, no shrink, with a fixed gap |

**Capability requirement - normative.**

1. The track's contents are duplicated so that the wrap point is invisible, and
   the distance is written to `--distance-percentage` by the component after it
   measures itself. The `-50%` fallback in the keyframe covers the exactly
   duplicated case and must be retained.
2. The animation is applied to the track, never to each item.
3. The row is masked at both edges by the horizontal soft-edge gradient of
   Section 7.5, so items enter and leave through a fade rather than at a hard
   boundary.
4. Duration is derived from content width so that rows of different lengths
   travel at the same apparent speed. Two rows at the same duration and
   different widths move at visibly different speeds, which is the defect this
   requirement exists to prevent.
5. The animation stops entirely under reduced motion, per Section 25.4, and the
   row becomes a horizontally scrollable region so its content is still
   reachable.

### 9.3 The instantiations

| Instance | Direction | Distance | Notes |
|---|---|---|---|
| Logo marquee | leading | custom property | The home route's customer wall |
| Logo grid scroll | leading | `-50%` | A second, denser treatment |
| Image marquee | leading | `-50%` | Media strips on pillar routes |
| Category media preview | leading | custom property | Blog category previews |
| App gallery row | leading | custom property | `140000ms`, the slowest on the site |
| Partner strip, forward | leading | `-20%` | Paired with its reverse |
| Partner strip, reverse | trailing | from `-20%` to `0` | Runs against its partner |

The paired partner strips travelling in opposite directions at the same duration
are a deliberate effect: two rows in opposition read as depth without any
transform in the third dimension.

### 9.4 The logo tile

| Property | Value |
|---|---|
| Radius | `4px` |
| Background | `--surface-details-logo-bg`, `#e9ebdf` |
| Ring | a one-pixel spread in `rgb(233, 234, 231)` |
| Border | hairline, per Section 3.2 |

**Capability requirement - normative.** Customer marks are rendered as
monochrome silhouettes on the pale tile rather than as full-colour logos. Every
mark is `<CUSTOMER_1>` through `<CUSTOMER_6>`, redrawn per Section 33.5, and no
mark ships as a file.

### 9.5 The feature tab system

The home route carries a tabbed feature block whose tabs advance on a timer.

| Element | Behaviour |
|---|---|
| Tab list | vertical, on the leading side |
| Progress indicator | a bar per tab, filled by `progress bar fill` scaling from `scaleY(0)` to `scaleY(1)` |
| Advance | automatic, on the progress animation's completion |
| Paused | the second progress keyframe set, which animates from `scaleY(0)` to `scaleY(0)` |
| Panel | the trailing side, cross-fading between tabs |

**Capability requirement - normative.**

1. The timer pauses on hover, on focus within the block, and when the block is
   out of the viewport. An auto-advancing carousel that keeps advancing while
   nobody is looking at it wastes the visitor's place when they return.
2. Selecting a tab by hand stops the automatic advance for the remainder of the
   session rather than resuming it after the current interval.
3. The tab list is a real tab list for keyboard and assistive technology, per
   Section 25.3, and the progress bars are decorative rather than announced.
4. The paused state is expressed as an animation that does not progress rather
   than as a removed animation, matching the reference, so that the element's
   animation state is identical in both cases and no reflow occurs on pause.

> **In plain language.** The strips of logos and pictures that slide sideways
> forever, and the block of features that changes by itself.
>
> Half of the moving things on this site are sliding strips, so they are built
> once and used six times rather than written out six times. The mechanism is
> that the contents are secretly duplicated, the strip slides exactly one copy's
> width, and then jumps back to the start, which you never see because at that
> instant the second copy is exactly where the first one was.
>
> Two details make the difference between this looking good and looking cheap.
> Each strip fades out at its left and right edges rather than being cut off at a
> hard line, so logos drift in and out of view instead of appearing and vanishing
> at an edge. And the speed is worked out from how wide the contents are, so a
> strip with four logos and a strip with twenty travel at the same apparent pace.
> Giving them both the same duration instead is the obvious shortcut and it makes
> one of them visibly race.
>
> There is also a pair of strips that slide in opposite directions at the same
> speed. Two rows moving against each other reads as depth without anything
> actually being three-dimensional. It is a very old trick and it still works.
>
> The block that changes by itself needs one piece of manners. It stops advancing
> while you are hovering it, while you are keyboard-focused inside it, and while
> it is off the screen. And once you have chosen a tab yourself, it stops
> advancing for good. Nothing is more irritating than reading something that
> slides away because a timer nobody asked for ran out.

---

## 10. The cursor system

### 10.1 What it is

The reference replaces the pointer with a drawn cursor that carries a contextual
label. Four named states are declared as full token sets, which is a strong
signal that this is a designed system rather than a decoration.

### 10.2 The state tokens

| State | Cursor fill | Cursor stroke | Label background | Label stroke | Label text |
|---|---|---|---|---|---|
| default | `#fff` | `#000` | `#fff` | `#000` | `#fff` |
| hover | `#fff` | `#000` | `#0009` | `#8b867f` | `#fff` |
| active | `#fff` | `#fff` | `#15151599` | `#c8bfb5` | `#e9ebdf` |
| message | `#fff` | `#000` | `#0009` | `#e9ebdf00` | `#fff` |

The `active` row is the one to read carefully. Its cursor stroke goes to white,
matching its fill, so the drawn cursor loses its outline and becomes a solid
white shape at the moment of pressing. Its label stroke, meanwhile, becomes
visible. The emphasis moves from the pointer to the label.

### 10.3 Geometry and motion

| Property | Value |
|---|---|
| Cursor transform | `matrix(1, 0, 0, 1, -1.6, -1.6)` |
| Outer ring transform, at rest | `matrix(1, 0, 0, 1, -100, -100)` |
| Label backdrop | `blur(3px)` |
| Label radius | `6px` |
| Label shadow | `rgba(0, 0, 0, 0.12) 0px 1px 2px 0px, rgb(255, 255, 255) 0px 0px 0px 0.5px` |
| Label transition | `transform 0.3s cubic-bezier(0.72, 0, 0.12, 1)` |
| Depth | `3000` |

The cursor's own offset of minus one and six tenths in both axes centres the
drawn shape on the true pointer position. The outer ring parks at minus one
hundred in both axes when idle, which is how it is hidden without a display
change: it is simply moved off the element.

**Capability requirement - normative.** The label follows the pointer under a
transition rather than being positioned per frame, at
`transform 0.3s cubic-bezier(0.72, 0, 0.12, 1)`. That three-tenths lag is the
entire effect. A label pinned exactly to the pointer feels stuck to the mouse; a
label arriving a beat late feels like it has weight.

### 10.4 What the cursor must not break

**Capability requirement - normative.**

1. The custom cursor is **enhancement only**. Under `hover: none` it does not
   render at all, per the reference's own pointer-capability branch in
   Section 3.8.
2. The real cursor is hidden only over regions the custom cursor covers. Text
   inputs, text selection and native controls keep their own cursors.
3. It never renders during a text selection drag.
4. It sits at depth `3000`, above the modal layer at `2000`, per Section 3.9.
5. It is not focusable, is hidden from assistive technology, and carries no
   information that is not also available another way. A label that only exists
   inside the cursor is information a keyboard user cannot reach.
6. It stops following under reduced motion; the label snaps rather than lagging.

> **In plain language.** The mouse pointer is replaced with a drawn one, and it
> picks up a small floating label depending on what it is over.
>
> There are four looks: normal, hovering something, pressing something, and
> carrying a message. The pressing one is the nicest and the most easily missed:
> at the moment you press, the drawn pointer loses its dark outline and becomes a
> solid white shape, while the little label it is carrying gains one. The
> attention moves from the pointer to the label.
>
> **The one thing that makes this feel expensive is a third of a second of lag.**
> The label does not sit exactly on the pointer; it chases it and arrives just
> after you stop. Pinned exactly, it feels glued to the mouse and slightly cheap.
> Arriving a beat late, it feels like it has weight. That is the whole trick.
>
> It also has to know when to get out of the way. It does not appear at all on a
> touchscreen. It leaves text boxes alone, so people can still see where they are
> typing and select words normally. It sits above everything including pop-up
> dialogs, which sounds obvious and is exactly the sort of thing that is
> discovered only when a dialog opens and the pointer vanishes behind it. And
> nothing is ever said only in that little label, because somebody navigating by
> keyboard never sees it.

---

## 11. Route: Home

### 11.1 Shape

The longest page on the site by a wide margin: roughly nine thousand pixels of
scroll at desktop and thirteen thousand at tablet, per Section 7.3. It is the
argument in full, and every other public route is a chapter of it.

| Band | Contents |
|---|---|
| 1 | Hero: headline, announcement pill, prompt composer, import and connector strips, video frame |
| 2 | Feature block: three pillars under one heading, with the tab system of Section 9.5 |
| 3 | Value block: three columns under a second heading |
| 4 | Logo wall and results |
| 5 | Industry blocks |
| 6 | Second composer, at the foot of the argument |
| 7 | Article cards |
| 8 | Footer, per Section 5.6 |

### 11.2 The hero

| Element | Treatment |
|---|---|
| Headline | display size, weight `100`, tracking `-0.031em`, on one line at desktop |
| Announcement | a pill badge carrying a gradient, plus a sentence and a link |
| Composer | Section 8 |
| Strips | Section 8.6 |
| Video frame | Section 7.4 |
| Playback control | a pause control at the leading edge, at pill radius |
| Film link | a pill at the foot of the frame carrying two-tone copy |

The hero sizes itself to the viewport through the height queries of Section 3.8
at `724px` and `881px`, in both their positive and negated forms, rather than to
a fixed height.

**Capability requirement - normative.** The video is decorative, muted, looping,
and carries a visible pause control. It does not autoplay on a metered
connection or under reduced motion, and the poster frame is a procedural
substitute per Section 33.6. The pause state persists for the session.

### 11.3 The announcement badge

| Property | Value |
|---|---|
| Radius | `36px` |
| Background | `linear-gradient(103deg, color(srgb 0.690196 0.8 0.917647 / 0.5) 12.9%, color(srgb 0.964706 0.839216 0.627451 / 0.5) 49.6%, color(srgb 0.909804 0.462745 0.368627 / 0.5) 84%)` |
| Animation | gradient shift, `0%` to `200%` background position |
| Backdrop | `blur(16px)` |

The gradient is authored in a wide colour space at half opacity over the page,
which is why it reads as a tinted pane rather than as a coloured pill. A
substitution in a narrower space loses roughly the whole effect, and the
substitution guide gives the fallback in Section 33.7.

A second badge treatment uses the flat `--surface-accent-background-green`,
`#0e352c`, for the New marker in the navigation.

### 11.4 The feature block

Heading, a link to the gallery, and three pillars. Each pillar carries an
eyebrow, a heading at `24px` weight `380`, a paragraph, and a link with the
arrow of Section 6.5. The pillars are announced by the fade-in-up keyframe of
Section 6.6 and, at desktop, are pinned against a media panel that changes with
the active pillar.

Scroll evidence for the pinning is in Section 7.1: the feature column carries
three distinct opacity values across the scroll and the story media group
carries two, which is a cross-fade between panels rather than a scrubbed
timeline.

### 11.5 The results band

A logo wall of six customer marks in a hairline-ruled grid, followed by result
cards.

| Element | Treatment |
|---|---|
| Logo cell | hairline border, pale tile per Section 9.4 |
| Result card | a large figure, a claim, and a link carrying the arrow |
| Media card | an image at `5px` radius with the ring of Section 3.6 |

**Capability requirement - normative.** Every figure quoted in this band is
attributed to a named customer and every customer name is a placeholder token.
Unattributed numbers in this position are the single most legally exposed
element on a marketing site of this kind.

### 11.6 The industry blocks

Two blocks of the same shape, one for supply chain and one for financial
services, each carrying a heading, a paragraph and a media panel. They exist to
give the enterprise reader a page they can send to a colleague, and their copy is
in Section 32.5.

### 11.7 The closing band

A second prompt composer, identical to Section 8 but pre-filled with a different
sentence, and a newsletter subscription control. This is the site's second
funnel entry and it is at the foot of a nine-thousand-pixel page on purpose: it
catches the reader who read the whole argument.

Subscription posts to the contract in Section 27.11.

### 11.8 The article cards

Three cards, each carrying an illustration, a headline and a byline in small
caps. The first is set larger than the other two in an asymmetric grid.
Bylines are `<AUTHOR_1>` to `<AUTHOR_3>`.

> **In plain language.** The front page, which is the whole argument and is
> around nine thousand pixels long. Every other public page is a chapter of it.
>
> It opens with one enormous line of very thin type, the typing box of Section 8,
> and a video running edge to edge behind everything. Then three pillars of what
> the product does, each with its own picture that changes as you move between
> them. Then three reasons enterprises pick it. Then a wall of customer logos and
> some large numbers about money saved. Then two blocks aimed at specific
> industries, which exist so an enterprise reader has a page they can forward to
> a colleague. Then the typing box again, at the bottom, for the person who read
> the whole thing. Then three articles. Then the footer.
>
> The video needs manners: it is silent, it loops, it has a visible pause button,
> it does not start on a phone connection or for anyone who has asked for less
> movement, and if you pause it, it stays paused.
>
> Every large number in the logo section is attached to a named company. That is
> not a design preference. A big claim about money saved with nobody's name
> against it is the most legally exposed thing on a page like this.

---

## 12. Route: Platform pillar

### 12.1 Shape

One of four pillar routes the navigation promises. The captured instance is the
AI pillar; the other three carry the same layout with different content, and the
build must treat this as one template rather than four pages.

| Band | Contents |
|---|---|
| 1 | Hero: eyebrow, headline, paragraph, conversion pair |
| 2 | Capability grid |
| 3 | Media strip, per Section 9.3 |
| 4 | Integration wall |
| 5 | Customer proof |
| 6 | Conversion band |
| 7 | Footer |

### 12.2 The accent

**Capability requirement - normative.** Each pillar route selects one of the
eight accents of Section 3.3 and uses the matching secondary button set from
Section 5.8 throughout. The accent is the only thing that differs between the
four routes, and it is what makes them feel like a set rather than duplicates.

### 12.3 The document metadata

Measured on the captured pillar:

| Field | Value |
|---|---|
| Theme colour | `#151515` |
| Colour scheme | `dark` |
| Viewport | `width=device-width, initial-scale=1` |

Every captured route declares the same three. They are normative on every route,
including the not-found route.

> **In plain language.** Four near-identical pages, one for each part of the
> platform, built from one template rather than four times over. The only thing
> that changes between them is which accent colour they use, and that is enough
> to make them feel like a family instead of copies.

---

## 13. Route: Blog index

### 13.1 Shape

An article index with a category taxonomy, published from a content source
rather than authored in the build.

| Element | Behaviour |
|---|---|
| Category strip | Horizontal, with the category media preview marquee of Section 9.3 |
| Featured article | One card at larger scale |
| Article grid | The remainder, in a hairline-ruled grid |
| Card | Illustration, headline, byline in small caps |
| Pagination | Cursor-based, per Section 26.5 |

### 13.2 The content contract

**Capability requirement - normative.** Articles come from the content model of
Section 17. The index is generated at build time and revalidated on publish, and
a draft article is never reachable at a public address, including by direct
address and including through the search index of Section 16.

### 13.3 Byline and attribution

Bylines are set in the small caps eyebrow of Section 3.4, at `12px` weight `300`.
Every author name is a placeholder token, per Section 0.3. Author pages are
required destinations, per Section 2.2.

> **In plain language.** The blog listing. Articles come out of a content system
> rather than being typed into the build, so the marketing team can publish
> without a developer.
>
> One rule matters more than the layout: a draft must never be reachable. Not by
> guessing its address, and not by turning up in the site's own search. Drafts
> leaking is the classic failure of a setup like this, and it is always the
> search that leaks them.

---

## 14. Route: Demo request

### 14.1 What it is

The site's highest-value conversion, on its own route, reachable from the header
of every page and from a source-tagged variant.

### 14.2 The form

| Field | Type | Required | Validation |
|---|---|---|---|
| Work email | email | yes | must parse as an address; a consumer mail domain is accepted but recorded |
| Reason for demo | select | yes | one of the three declared options |

Options, as measured: explore the enterprise product, explore a use case,
professional services.

The consent line beneath the control states that submitting agrees to the
privacy policy and consents to marketing communications, and it links the
privacy route. It is not a checkbox in the reference; it is a statement.

**Capability requirement - normative.** Where the visitor's jurisdiction
requires affirmative consent, the statement becomes an unchecked box and the
submit is disabled until it is checked. That branch is a legal requirement, not
a design preference, and the build must carry both forms.

### 14.3 States

Per the contract in Section 27.11:

| State | What the page shows |
|---|---|
| `sent` | The confirmation, replacing the form block |
| `invalid` | Field-level messages, form retained |
| `spam` | A distinct message, form retained |
| `failed` | A retry message, with every typed value retained |

### 14.4 The proof rail

Beside the form sit two customer results and a claim about the number of
companies using the product. They carry `<CUSTOMER_1>` and `<CUSTOMER_2>` and
the same attribution rule as Section 11.5.

### 14.5 The return control

A control at the foot of the route scrolls back to the form, carrying an upward
arrow. It appears only once the form has left the viewport.

> **In plain language.** The page for booking a demonstration, which is the most
> valuable thing a visitor can do on this site.
>
> It asks for two things and no more: a work email address and a one-line reason
> for wanting the demo. Every extra field costs conversions, and this form's
> restraint is deliberate.
>
> Underneath, a line saying that submitting agrees to the privacy policy. In some
> countries that line has to become a tick box that starts empty, so the build
> needs both versions and has to know when to show which. That is a legal
> requirement rather than a design choice.
>
> The thing to get right is what happens when it fails. If our end breaks, the
> visitor's typed email must still be sitting in the box when the error appears.
> Losing a serious enterprise enquiry to a hiccup is the worst thing this page can
> do, and it is entirely preventable.

---

## 15. Route: Not found

### 15.1 Shape

| Element | Copy |
|---|---|
| Message | The path that was not found, then an offer of somewhere better |
| Action | A link home |
| The rest | Section 15.2 |

The route carries the full header and footer, and declares the same metadata as
every other route, per Section 12.3.

### 15.2 The game

The reference puts a playable falling-blocks game on its not-found page. It is
measured, it is real, and it is specified here because it is the most
distinctive single thing in the captured set and because it is a genuine piece
of engineering rather than a decoration.

| Element | Measured |
|---|---|
| Title | a labelled heading |
| Level readout | starting at `1` |
| Match readout | starting at `5` |
| Score readout | starting at `0` |
| Restart | bound to `r` |
| Move left | bound to the left arrow |
| Move right | bound to the right arrow |
| Drop | bound to the down arrow |
| Rotate | bound to the up arrow |

**Capability requirement - normative.**

1. The game is keyboard-driven, and every binding above is displayed on screen
   beside its action rather than hidden in a help panel.
2. It is also playable by touch, with the same actions on visible controls.
3. It does not capture the arrow keys until it has focus, and it releases them
   on blur. A not-found page that steals the page-down key from somebody trying
   to reach the footer is a worse failure than not having a game.
4. It stops when off screen and under reduced motion, and it never plays sound
   without an explicit control.
5. Its readouts are a live region, per Section 25.3, so the score is available
   to somebody who cannot see the board.
6. Score is per-session and local to the visitor's browser. It is not sent
   anywhere.

The board's cell treatment reuses the pixel vocabulary of Section 4: one-unit
squares on an integer grid, in the accent ramps of Section 3.3.

> **In plain language.** The page you land on when a link is wrong. It says what
> was not found, offers a way home, and then, unexpectedly, contains a playable
> falling-blocks game with a score, levels and keyboard controls.
>
> That is not a joke item to skip. It is in the reference, it works, and it is
> the single most memorable thing on the site.
>
> It does need to be a good citizen. The keys it uses are shown on screen next to
> what they do. It works by touch too. It does not grab the arrow keys until you
> have actually clicked into it, and it lets go the moment you click away, so it
> never hijacks the keys from somebody just trying to scroll down the page. It
> stops when it is off screen. It never makes a noise you did not ask for. And
> the score is announced in a way a screen reader can pick up, so it is not a
> game only sighted people can play.

---

## 16. Search

### 16.1 What it is

A site-wide overlay, reachable from the header control of Section 5.2 and from a
global keyboard shortcut.

### 16.2 Behaviour

**Capability requirement - normative.**

| Concern | Requirement |
|---|---|
| Shortcut | The platform modifier plus `K`, working from any route, and not while a text field has focus |
| Hint | Rendered in the header at zero opacity, revealed on hover or focus of the control |
| Open | Focus moves into the field; the page beneath does not scroll |
| Query | Debounced, cancelling superseded requests, per Section 27.4's cancellation rule |
| Results | Grouped by type, keyboard-navigable, with the active result always scrolled into view |
| Empty | A distinct state naming what was searched for |
| Close | Escape, the scrim, and the close control, all returning focus to the header control |
| Scope | Published public routes only, per Section 13.2 |

### 16.3 The overlay treatment

| Property | Value |
|---|---|
| Scrim | `--surface-lightbox-scrim`, `#0009` |
| Panel background | `--surface-background`, `#161212` |
| Panel stroke | `--surface-stroke`, `#354045` |
| Depth | `2000` |
| Field, focused | inverts per the input tokens of Section 3.3 |

> **In plain language.** The search, which opens over the page rather than
> taking you to a search page.
>
> It has a keyboard shortcut, and the shortcut is shown on the search button
> itself, faintly, appearing when you hover it. Small courtesy, and it is how
> people find out the shortcut exists at all.
>
> The behaviours that matter are the dull ones. Typing quickly must not leave you
> looking at the results for three letters ago. Escape closes it and puts you back
> on the button you opened it from, so keyboard users do not get dumped at the
> top of the page. And it only ever finds published pages, never drafts.

---

## 17. Content model

### 17.1 Why this is specified

**Observed implementation - informational.** The reference serves its marketing
content from a hosted content platform, established at ledger tier 4 by the
presence of its asset origin in the network capture. The marketing surface is
therefore not authored in the build.

**Capability requirement - normative.** The build separates content from
presentation with the following model. The platform is not specified; the
contract is.

### 17.2 The types

| Type | Fields |
|---|---|
| Page | slug, title, description, theme accent, ordered band list |
| Band | a discriminated union over the band types of Sections 11 and 12 |
| Article | slug, title, excerpt, body, author reference, category reference, published state, published time, illustration reference |
| Author | name, role, biography, portrait reference |
| Category | slug, name, preview media list |
| Customer | name, mark reference, industry, ordered result list |
| Result | figure, claim, customer reference, link |
| Navigation | ordered group list, each with a label and ordered destinations |
| Announcement | text, link, active window |

### 17.3 The rules

**Capability requirement - normative.**

1. **Navigation is content, not code.** The forty-one destinations of
   Section 2.2 are authored, and a destination that resolves to nothing fails
   validation at publish rather than at request.
2. **The announcement banner has a validity window** and disappears on its own,
   because an announcement banner nobody removes is the most common piece of
   stale content on a marketing site.
3. **Every media reference resolves to a described image.** Alternative text is
   a required field on the content type, not an optional one filled in later.
4. **Publishing revalidates only the affected routes**, and a publish that
   revalidates the whole site is a defect at this content volume.
5. **Draft state is enforced at the data layer**, so that no route, index or
   search path can return one. Section 13.2 asserts it.

> **In plain language.** The words and pictures on the public site come out of a
> content system that the marketing team edits, rather than being typed into the
> code by a developer.
>
> Four rules are worth insisting on. The menus are content too, so marketing can
> add a page without waiting for a release, and the system refuses to publish a
> menu item pointing at nothing. The announcement strip at the very top has a
> start and end date and removes itself, because otherwise it is still advertising
> last spring's conference in October. Every picture must have a written
> description before it can be published, rather than after. And unpublished
> drafts are blocked at the source, so there is no route, no listing and no search
> result that can reach one.

---

## 18. Route: authentication

### 18.1 What is here

Four screens under one chrome: sign in, federated sign in, second factor, and
invitation acceptance. There is no public sign-up on the enterprise path; an
account exists because somebody was invited or because the identity provider
provisioned it. The self-serve path of Section 5.4 creates an organisation and
then lands on the same screens.

### 18.2 Sign in

| Element | Behaviour |
|---|---|
| Email field | Autocomplete declared, validated on blur, and the submit is not blocked on client validation alone |
| Continue | Resolves the organisation from the address domain and routes to password or to the federated provider |
| Password field | Rendered only when the resolved organisation permits password authentication |
| Federated | Renders the organisation's provider by name, and is the only control shown where the organisation enforces federation |
| Failure | One message for an unknown address and a wrong password alike, per Section 18.5 |
| Rate limit | Per address and per source, with a stated lockout, and the lockout is an audited event |

### 18.3 Second factor

**Capability requirement - normative.** Where the organisation requires it, the
second factor is demanded before any session with authority is issued, not
after. The intermediate state holds no grants at all. A partially authenticated
session that can read anything is a defect.

### 18.4 Invitation acceptance

| Step | Requirement |
|---|---|
| Token | Single use, time-limited, bound to the invited address, invalidated on use and on revocation of the invitation |
| Landing | The invitee sees the organisation and the inviting principal before they accept |
| Existing account | Acceptance adds a membership; it never creates a second account for the same address |
| Expiry | An expired token offers to request a fresh invitation and never reveals whether the organisation exists |

### 18.5 What the screens must not reveal

**Capability requirement - normative.** No screen in this route may distinguish,
to an unauthenticated caller, between an address that has an account and one that
does not: not by message, not by status code, not by response timing, and not by
whether a password field appeared. Organisation resolution by email domain is
the one permitted disclosure, and it discloses only that a domain is federated.

> **In plain language.** The way in. Four screens: signing in, signing in through
> the company's own login system, the second step with a code, and accepting an
> invitation.
>
> There is no public sign-up here. On this path you have an account because
> somebody invited you or because your employer's staff directory created one.
>
> The important discipline is about what these screens give away to a stranger. A
> wrong password and an address that has never been heard of produce the same
> message, the same colour, and take the same length of time to come back. If
> "no such account" is even slightly faster than "wrong password", somebody can
> work through a list of email addresses and learn which of your customers'
> staff work here. That is why these four screens are worth their own section for
> what is, on the face of it, a login box.

---

## 19. The builder canvas

### 19.1 What it is

The authoring surface: a grid the builder drops components onto, binds to
queries, and arranges into an application. It is the most expensive single
component in the build and the one every graded workflow in Section 30.3 passes
through.

It is also the surface with the least captured evidence. The reference's builder
is behind authentication and could not be captured, per Section 34.2. What
follows is a normative specification of the capability, informed by the builder
imagery on the marketing routes, and it is labelled inferred wherever it rests
on those images rather than on measurement.

### 19.2 The layout

Four regions, fixed, resizable at their shared edges, persisted per builder:

| Region | Position | Holds | Collapsible |
|---|---|---|---|
| Component tree | left rail | the app's component hierarchy, searchable, drag-reorderable | yes |
| Canvas | centre, above | the grid, the components, the selection and the drop affordances | no |
| Query panel | centre, below | the query list, the editor and the result pane | yes |
| Inspector | right rail | the properties of the current selection | yes |

The vertical split between canvas and query panel is a draggable divider with a
persisted ratio. The persisted ratio is per builder and per app, not global: a
builder working on a query-heavy app and a layout-heavy app wants two different
splits, and resetting one when the other is opened is the kind of small
disrespect that makes a tool feel borrowed.

### 19.3 The grid

**Capability requirement - normative.**

| Property | Requirement |
|---|---|
| Columns | Fixed count across the canvas width, so a layout is resolution-independent |
| Row height | Fixed unit; component height is a whole number of units |
| Placement | A component occupies a rectangle of whole columns by whole rows |
| Collision | Two components may not occupy the same cell. A drop that would collide displaces rather than overlaps |
| Displacement | Displaced components move down, in tree order, and the displacement is one operation for undo purposes |
| Reflow | Removing a component does not close the gap it leaves. Silent reflow on delete makes undo feel broken even when it is correct |

The last row is a judgement the specification makes deliberately. Automatic
compaction is defensible and this build does not do it, because a builder who
deletes a component and watches the whole layout jump has lost their place, and
the undo that follows restores the component but not their confidence.

### 19.4 Drag, drop and resize

**Capability requirement - normative.**

| Interaction | Behaviour |
|---|---|
| Drag from the component library | A ghost follows the pointer; the target cells are outlined; an invalid target is refused visibly rather than accepted and corrected |
| Drag on the canvas | Same, with the origin cells shown vacated |
| Multi-select | Rubber band on empty canvas, and modified click to add or remove; a multi-select move is one operation |
| Resize | Handles on all eight edges and corners, snapped to the grid, with a live outline and a minimum of one cell in each axis |
| Keyboard | Selection moves by arrow key, resizes by modified arrow key, and every drag operation is reachable without a pointer, per Section 25 |
| Cancel | Escape during a drag returns the component to its origin, and produces no operation on the undo stack |
| Pointer capture | The drag survives the pointer leaving the canvas or the window, and terminates cleanly if the pointer is released outside |

**Observed implementation - informational.** The builder imagery on the marketing
routes shows a snapped grid with visible column guides during drag. The guide
treatment is inferred from those images; the snapping behaviour is a requirement
regardless.

### 19.5 The operation log

This is the mechanism that makes workflow H4 and workflow H8 passable, and it is
the single most consequential architectural decision on the frontend.

**Capability requirement - normative.**

1. Every canvas mutation is an **operation** with a type, a payload and an
   inverse: `add`, `remove`, `move`, `resize`, `reparent`, `set-property`,
   `bind`, `unbind`, `rename`.
2. Operations are appended to a log against a base version hash, and the log is
   what is transmitted, per Section 27.5.
3. Undo applies the inverse of the last operation. Redo re-applies it. A
   multi-select move is one operation with one inverse, so it undoes in one
   step.
4. The log survives reload. Reopening an app replays it, so undo depth is not
   bounded by the session.
5. Renaming a component rewrites references in bindings as part of the same
   operation, so an undo of a rename restores the bindings too. A rename that
   breaks bindings and an undo that does not restore them is the same defect
   twice.

A snapshot stack is the tempting alternative and it fails in a specific,
demonstrable way: it cannot express "undo just the resize" once a multi-select
has been moved, and it grows without bound on large apps. Workflow H4 is written
to distinguish the two.

### 19.6 Selection and focus

| State | Treatment |
|---|---|
| Hovered | A one-unit outline in the accent, no fill |
| Selected | A two-unit outline plus the eight resize handles |
| Multi-selected | Each member outlined; a single bounding outline around the set carries the handles |
| Focused by keyboard | The selected treatment plus a visible focus ring that survives a high-contrast setting |
| Locked | Outline in a muted tone, no handles, and drag refused with a reason |
| Erroring | Outline in the error tone plus a badge carrying the error count, per Section 19.8 |

Selection is not focus. A builder tabbing through the inspector must not lose
the canvas selection, and a build that conflates the two makes keyboard
authoring impossible.

### 19.7 Binding

**Capability requirement - normative.** A binding is an expression evaluated
against a scope containing the app's queries, its components' state and a small
standard library.

| Property | Requirement |
|---|---|
| Syntax | A single, documented expression syntax, identical in every bindable field |
| Scope | Queries by name, components by name, the current row in a repeated context, and nothing else. No access to the host page, the network or storage |
| Evaluation | Sandboxed, time-bounded, and unable to block the interface |
| Dependency graph | Maintained, acyclic, and checked at bind time. A cycle is refused with both ends named |
| Re-evaluation | Only bindings downstream of a changed value re-evaluate. A property change must not re-run the whole graph |
| Errors | Surface on the component and in the inspector field that produced them, with the expression and the failure, never as a blank value |
| Type | A binding's resolved type is visible in the inspector, so a builder can see that a date arrived as a string |

The dependency graph is what makes the difference between a builder that stays
responsive at two hundred components and one that does not. Re-evaluating
everything on every keystroke is correct and unusable.

### 19.8 Error surfacing

**Capability requirement - normative.** Three levels, and they are distinct:

| Level | Example | Where it appears |
|---|---|---|
| Authoring error | a binding references a deleted query | Inspector field, component badge, and a tree badge on every ancestor |
| Runtime error | a query returned `failed` | The bound component's own error state, and the query panel |
| Platform error | the workspace lost its connection to the server | A single global banner, never a per-component storm |

The third row is a requirement about restraint. A connection loss that renders
forty component-level error states has told the builder nothing and destroyed
their ability to see the one error that was already there.

### 19.9 Performance under load

**Capability requirement - normative.** The canvas holds two hundred components
and thirty queries and remains interactive:

| Measure | Bound |
|---|---|
| Drag and resize | Tracks the pointer without dropping frames, on the reference hardware of Section 26.2 |
| Selection change | Repaints only the previously and newly selected subtrees |
| Binding re-evaluation | Only the downstream subgraph, per Section 19.7 |
| Tree rendering | Virtualised beyond the visible rows |
| Save | Transmits operations, not the document, so save cost is proportional to what changed |
| Initial open | The canvas is interactive before every query has returned; a query still in flight renders its component in a loading state rather than blocking the canvas |

> **In plain language.** This is the screen where somebody builds an app by
> dragging pieces onto a page, and it is the hardest single thing in this build.
>
> It is laid out in four parts: a list of everything on the page down the left, a
> big grid in the middle where the pieces go, a panel underneath for the
> questions you ask the database, and a properties panel down the right for
> whatever is currently selected. The dividers between them can be dragged and
> they remember where you left them, separately for each app, because somebody
> working on a database-heavy app and a layout-heavy app wants different shapes
> and having one reset the other is the kind of small rudeness that makes a tool
> feel like somebody else's.
>
> Things snap to a grid. Two pieces can never sit on top of each other; dropping
> one where another already sits pushes that one down rather than overlapping.
> Deleting a piece leaves the hole where it was, on purpose, so the rest of the
> page does not jump around while you are working.
>
> **The most important invisible decision here is how undo works.** The obvious
> way is to photograph the whole page after every change and step backwards
> through the photographs. It is easier to build and it feels correct until the
> moment somebody selects five things, moves them together, and presses undo. So
> instead, every single action records how to reverse itself: this piece moved
> from here to here, so undoing it means moving it back. Moving five things at
> once is one action with one reversal. It also means undo still works after you
> close the laptop and come back tomorrow, because the list of actions is kept
> rather than the photographs.
>
> Pieces on the page get their contents by referring to each other and to the
> database questions, in short written expressions. The build keeps a map of what
> depends on what, so that changing one thing recalculates only the things that
> actually depend on it. Recalculating everything on every keystroke gives
> exactly the same answers and makes the tool unusable at any real size.
>
> Errors have to be told apart. A mistake in something you wrote appears on the
> piece you wrote it on. A failure from the database appears on the piece showing
> the data. And losing the connection to the server puts up one message at the
> top, not forty red boxes, because forty red boxes tell you nothing and hide the
> one real problem that was already there.

---

## 20. Component library and the inspector

### 20.1 The library

**Capability requirement - normative.** The library is grouped, searchable and
keyboard-reachable. Every entry declares its default size in grid units, its
bindable properties with their types, its events, and the state it exposes to
other components' bindings.

| Group | Members | The one that carries the weight |
|---|---|---|
| Data | table, list, key-value, chart, statistic | table, Section 21 |
| Input | text, number, date, select, multiselect, checkbox, switch, slider, file, rich text | select, because of Section 20.5 |
| Layout | container, tabs, stack, modal, drawer, form, divider, spacer | form, because it owns submission state |
| Action | button, icon button, menu, link | button, because it is where the permission of Section 28.4 is felt |
| Display | text, image, icon, badge, progress, avatar, timeline | text, because it is the most-used bindable |
| Navigation | breadcrumb, pagination, steps, sidebar | pagination, which must be bound to the server, not the array |

A component is a contract, not a rendering. Two properties of the contract are
normative:

1. **Every component exposes its state under its own name**, so any other
   component can bind to it. A table exposes its selected row, its page, its
   sort and its filter. A form exposes its values, its validity and its
   submission state.
2. **Every component that can be busy has a busy state, an empty state and an
   error state**, and all three are specified rather than left to the
   implementer. A grid with no empty state ships an empty grid that looks broken.

### 20.2 The inspector

The right rail, showing the current selection's properties, grouped and ordered:
content, then data, then appearance, then interaction, then layout, then
identity.

| Field type | Editor | Bindable |
|---|---|---|
| String | single line, expands to multiline on overflow | yes |
| Number | stepper with typed entry, unit shown where the property has one | yes |
| Boolean | switch | yes |
| Enumerated | segmented control at three or fewer members, select above | yes |
| Colour | token picker first, custom second, per Section 3.3 | yes |
| Query | picker listing the app's queries, with an inline create | not applicable |
| Event | a list of handlers, each an action plus its parameters | not applicable |
| Expression | monospace field with the resolved value and type shown beneath | it is one |

**Capability requirement - normative.**

1. **Every bindable field can be switched to an expression in place**, without a
   modal, and switched back with the last static value retained.
2. **The resolved value is shown under every bound field**, live. A builder must
   never have to run the app to find out what an expression evaluates to.
3. **Editing is committed on blur and on enter, and reverted on escape.** An
   inspector that commits on every keystroke fills the operation log with
   noise and makes undo useless.
4. **Multi-selection shows the intersection of properties**, with differing
   values marked, and editing one applies to all.

### 20.3 Events and actions

An event handler is a declared action, not a script. The action set is closed:

| Action | Parameters | Notes |
|---|---|---|
| Run query | query, parameters | The parameters are bindings |
| Set component property | component, property, value | The only way one component writes to another |
| Navigate | app, route, parameters | Within the workspace, or to an external target that is declared |
| Open or close overlay | modal or drawer | |
| Show notification | level, message, duration | |
| Copy to clipboard | value | |
| Download | value, filename, type | Subject to the export permission of Section 28.7 |
| Trigger workflow | workflow, payload | Asynchronous, returns a run identity |

**Capability requirement - normative.** Handlers run in declaration order. A
failing handler halts the chain and reports which handler failed, rather than
continuing silently. A handler chain that swallows a failed mutation and then
shows a success notification is the worst available defect in this surface, and
it is the default behaviour of a naive implementation.

### 20.4 Forms

**Capability requirement - normative.**

| Concern | Requirement |
|---|---|
| Validation | Declared per field, evaluated client-side for feedback and server-side for truth |
| Submission | Disabled while in flight, and the disable is driven by the request state, not by a timer |
| Double submission | Refused by the idempotency key of Section 27.8, not only by the disabled control |
| Failure | Every value the user typed is retained, and the error is attached to the field that caused it where the server identifies one |
| Success | The bound data refreshes, and the form resets or retains per its declared behaviour |
| Dirty state | Navigating away from a dirty form warns, and the warning is reachable by keyboard |

### 20.5 The select, and why it is called out

A select bound to a query is where three of this build's recurring problems
meet: it fetches from the server, it may hold more options than can be sent, and
it is an input.

**Capability requirement - normative.** A bound select fetches asynchronously,
searches server-side above a stated option count, debounces its search, retains
the selected value's label even when that value is not in the current page of
results, and does not lose the selection when the query re-runs. The last clause
is the one that is always missing.

> **In plain language.** These are the pieces somebody drags onto the page, and
> the panel on the right where their settings live.
>
> Every piece publishes what it is currently doing, under its own name, so other
> pieces can respond to it. A table announces which row is selected; a button
> somewhere else can then be wired to that. That is how a screen becomes an
> application rather than a poster.
>
> Every piece that can be waiting also has to say what it looks like while
> waiting, what it looks like with nothing in it, and what it looks like when
> something went wrong. Skipping the last two is how you end up with a table that
> looks broken when it is simply empty.
>
> In the settings panel, any setting can be switched from a fixed value to a
> little calculation, and the answer that calculation currently produces is shown
> underneath it as you type. Somebody building a screen should never have to run
> the app to find out what their expression came out as.
>
> When a button is pressed, it runs a list of actions in order. If one of them
> fails, the list stops and says which one failed. The tempting mistake is to
> carry on regardless and show a cheerful "saved" message anyway, which teaches
> people to trust a screen that is lying to them.
>
> One small piece gets a paragraph of its own: the dropdown that gets its options
> from the database. It is where three separate problems meet, and the one that
> is always got wrong is this: when the options reload, the thing the user had
> already chosen must still be chosen, and must still show its name, even if it
> is not in the batch of options that just came back.

---

## 21. The data grid

### 21.1 Why the table is specified separately

Because it is the component the product is bought for. An internal tool is
usually a table with two buttons, and every hard property of this build shows up
in it: server-side everything, permission-aware columns, editable cells that
mutate rows, and enough rows to punish any implementation that touches the DOM
per row.

### 21.2 Data flow

**Capability requirement - normative.**

| Operation | Where it happens | Never |
|---|---|---|
| Paging | Server, by cursor where the resource supports it, by offset otherwise | fetch all, page in the browser |
| Sorting | Server, on declared sortable columns | sort the fetched page and call it sorted |
| Filtering | Server, as bound parameters | filter the fetched page |
| Search | Server, debounced, cancelling superseded requests | |
| Aggregation | Server | |
| Selection | Client, with the selection expressed as keys, so it survives a refetch | store row indices |

Workflow M6 asserts this over fifty thousand rows, and the assertion is on the
network payload rather than on the appearance of the screen, because a grid that
fetches everything and pages in the browser looks identical until it does not.

### 21.3 Rendering

**Capability requirement - normative.**

| Property | Requirement |
|---|---|
| Virtualisation | Rows and columns both, with a stated overscan |
| Row identity | A stable key from the data, never the array index |
| Column sizing | Per-column, resizable, persisted per user per app, with a content-fit action |
| Frozen columns | Leading columns pinnable, and the pinned region scrolls vertically in lock with the body |
| Row height | Uniform by default; variable height is opt-in and requires measurement rather than estimation |
| Scrolling | The header never detaches from the body during momentum scrolling |

Row identity from the data rather than the index is what makes selection survive
a refetch, which is what makes the selection binding in Section 20.1 correct.

### 21.4 Cells

| Type | Display | Editable |
|---|---|---|
| Text | truncated with a title, wrapping opt-in | inline |
| Number | right-aligned, thousands separated, precision declared | inline |
| Currency | right-aligned, **integer minor units**, never a float | inline |
| Date and time | formatted in the viewer's zone, with the zone shown where it matters | picker |
| Boolean | checkbox, tri-state where the column is nullable | toggle |
| Enumerated | badge with a declared tone per value | select |
| Link | truncated, with the target shown | inline |
| JSON | collapsed summary, expandable in place | modal |
| Image | thumbnail from a signed URL | replace |
| Action | buttons, permission-gated per row per Section 28.4 | not applicable |

Currency as integer minor units is a requirement, not a preference. A grid that
holds money in a floating-point number will produce a total that is wrong by a
penny in front of a finance team, and that is the end of the tool's credibility.

### 21.5 Editing

**Capability requirement - normative.**

1. An edited cell is **staged**, not written. Staged changes are visible as
   such, per row and per cell.
2. Staged changes are committed by an explicit action, as one mutation, with one
   idempotency key.
3. A failed commit **retains the staged values** and marks the rows that failed
   with the reason.
4. A successful commit refetches rather than patching the local copy, because
   the resource may have applied defaults, triggers or its own row-level rules.
5. A cell the acting principal may not write is not editable, and the refusal is
   decided by Section 28, not by a column flag in the app definition.

Point 4 is worth defending. Patching locally is faster and it is how the grid
starts to disagree with the database, silently, in ways nobody notices until a
number is quoted in a meeting.

### 21.6 Empty, loading and error

| State | Treatment |
|---|---|
| Loading, first | Skeleton rows at the configured page size, header already correct |
| Loading, subsequent | The existing rows stay, dimmed, with a progress indication in the header |
| Empty, no filter | An explanatory empty state naming what would appear here |
| Empty, filtered | A distinct state naming the filter and offering to clear it |
| Denied | The refusal of Section 27.4, stated as a refusal |
| Error | The mapped error of Section 27.10, with a retry that reuses the same parameters |
| Truncated | An explicit banner naming the row cap that was hit, per Section 27.9 |

"Empty" and "denied" being visually distinct is the interface half of the
contract in Section 27.4, and it is asserted by workflow H3.

> **In plain language.** The table is the thing this whole product is really
> bought for. Most internal tools are a table with a couple of buttons, so every
> hard problem in this build turns up in it.
>
> The rule that governs it: the table never fetches everything. When somebody
> sorts, searches, filters or turns a page, the database does that work and sends
> back one page. The lazy version, fetching all fifty thousand rows and doing the
> work in the browser, looks exactly the same on a demo with a hundred rows and
> falls over completely on real data. The test for this watches the network
> traffic rather than the screen, because the screen cannot tell you which one
> you built.
>
> Money is stored as whole pennies, never as a decimal number. Decimal numbers in
> computers are very slightly inexact, and the moment a total is a penny out in
> front of a finance team, nobody trusts the tool again.
>
> When somebody edits cells, the changes are held up on screen as pending until
> they press save, and then all of them are sent as one instruction. If the save
> fails, the typed values stay exactly where they are and the failed rows are
> marked with the reason. After a save succeeds, the table asks the database for
> the rows again rather than assuming it knows what happened, because the
> database may have filled in defaults or applied rules of its own. Assuming is
> faster, and it is how the screen quietly starts disagreeing with the database.
>
> Finally, an empty table and a table you are not allowed to see must never look
> the same. "There are no orders" and "you may not view orders" are completely
> different facts, and merging them is how a permissions bug hides for a year.

---

## 22. Route: workspace, resources and administration

### 22.1 The workspace home

The list of apps, and the surfaces around it.

| Element | Behaviour |
|---|---|
| App list | Filtered by the caller's grants at the server, not filtered in the client from a full list |
| Grouping | By folder, with folders carrying their own grants |
| Search | Server-side, across names and descriptions the caller may see |
| Row | Name, environment badges showing where it is released, last edit, last editor |
| Create | Opens an empty app in the editor at a new draft version |
| Recents and favourites | Per user, and never a route by which an unentitled app becomes visible |

The first row is the whole security posture of this screen. Fetching every app
and hiding the ones the caller may not see puts the entire catalogue of an
organisation's internal tooling into the network tab.

### 22.2 Resources

| Element | Behaviour |
|---|---|
| List | Type, name, environments configured, last test result and time |
| Create | Typed form per resource class, per Section 27.7, with credentials write-only per Section 27.6 |
| Test | Server-side, returning reachable or a failure class |
| Environments | One credential set per environment, and the production set independently permissioned |
| Usage | Which apps and workflows reference this resource, so that deletion can be refused with a list rather than cascading |
| Delete | Refused while referenced; the refusal names the references |

### 22.3 Administration

| Surface | Contents |
|---|---|
| Members | Principals, status, groups, last activity, and the invitation and removal actions |
| Groups | Membership, nesting, and the grants held, with the source of each membership shown |
| Permissions | The grant matrix, editable, with explicit deny as a first-class value per Section 28.3 |
| Policies | Row predicates and column masks, versioned, with a preview against a chosen principal |
| Identity | Federation configuration, provisioning status, claim mapping, and the last synchronisation |
| Environments | The ordered list, which are protected, and the approval requirement per environment |
| Audit | The queryable trail of Section 29.4 |
| Usage and quota | Consumption against the bounds of Section 27.9 |

### 22.4 The permission debugger

**Capability requirement - normative.** Administration carries a surface that
answers the four questions of Section 28.9 directly: pick a principal and a
resource, and see the decision, the ordered rules that produced it, and the
grant chain each rule came from.

This is specified as a product surface rather than as a developer tool because
the alternative is that the answer lives in a log an administrator cannot read.
An organisation cannot operate a permission system it cannot interrogate, and
the request "can you check whether Dana can see the refunds table" arrives
weekly.

### 22.5 Destructive actions

**Capability requirement - normative.** Deleting a resource, a group, an
environment or an app is confirmed by typing the object's name, states what
will break by naming the references, and is recoverable for a stated window
before it becomes permanent. Removing a member is immediate in effect, per
workflow X1, and recoverable in record.

> **In plain language.** Everything behind the sign-in that is not the app
> builder itself: the list of apps, the database connections, and the
> administration screens.
>
> The app list only ever contains apps you are allowed to open. That sounds
> obvious and it is the most commonly broken thing on this kind of screen: the
> lazy version fetches every app in the company and hides the ones you should not
> see, which puts a complete catalogue of the company's internal tools one glance
> at the network tab away.
>
> Database connections are set up here. Passwords can be set and replaced but
> never read back, and a connection cannot be deleted while apps are using it -
> instead you are told which apps those are.
>
> The administration screens are where people, groups and permissions live, and
> one of them deserves calling out because most products in this category do not
> have it: a screen where an administrator picks a person and a thing, and is
> shown the answer plus the reasoning. Not "Dana can see this", but "Dana can see
> this because Dana is in Support, Support is inside Operations, and Operations
> was granted read access on the fourth of March by Sam." Somebody asks that
> question about once a week, and without this screen the only person who can
> answer it is an engineer reading a database by hand.

---

## 23. Module and component architecture

### 23.1 The three applications

One repository, three deployable surfaces, and the boundary between them is a
requirement rather than a preference:

| Surface | Serves | May import |
|---|---|---|
| Marketing | the unauthenticated routes of Sections 12 to 17 | the design system, and nothing from the product |
| Studio | the authenticated authoring surface, Sections 18 to 22 | the design system, the product runtime |
| Runtime | published apps, for end users | the design system, the product runtime, and nothing from the editor |

The third row is load-bearing. An end user's bundle must not contain the editor.
It is a weight argument and, more importantly, a surface argument: code that is
not shipped cannot be driven.

### 23.2 Layering

```
design system      tokens, primitives, icons          no product knowledge
runtime            components, bindings, query client no editor knowledge
editor             canvas, inspector, operation log   depends on runtime
server             api, authz, resources, audit       no knowledge of any client
```

**Capability requirement - normative.** Dependencies point one way only, and the
build enforces it rather than documenting it. A lint rule that fails the build on
an upward import is the mechanism; a paragraph in a readme is not.

### 23.3 The primitives worth naming

| Primitive | Responsibility |
|---|---|
| `TokenProvider` | Exposes the design tokens of Section 3 and the theme resolution of Section 3.7 |
| `Reveal` | The scroll-triggered entrance of Section 6, one implementation, used everywhere |
| `QueryClient` | Execution, cancellation, de-duplication, retry policy and cache keying for Section 27.4 |
| `Binding` | Parsing, dependency registration, sandboxed evaluation and typed result for Section 19.7 |
| `OperationLog` | Append, invert, replay and rebase for Section 19.5 |
| `Decision` | The client-side mirror of Section 28.2, advisory only, never enforcement |
| `AuditedAction` | Wraps a mutation so that the effect and its audit event share a transaction boundary |
| `Virtualizer` | Row and column windowing for Section 21.3 |

`Decision` being explicitly advisory is worth the line it takes. Naming it that
way in the code is what stops a later contributor from reaching for it as a
guard and believing they have secured something.

### 23.4 State

| State | Lives | Survives |
|---|---|---|
| Server state | the server, mirrored in `QueryClient` | nothing; it is refetched |
| App definition | the server, as versions | everything |
| Draft edits | the operation log, synchronised | reload, per Section 19.5 |
| Component runtime state | the runtime's store, keyed by component name | route change within the app |
| Editor view state | local, per user per app | reload |
| Session | an http-only, same-site cookie | tab close, per its own lifetime |

**Capability requirement - normative.** No product state is held in a module
scope singleton. The runtime must be able to mount two apps in one document, for
the preview of Section 19.2 and for the embedded case, without them sharing
state.

> **In plain language.** How the code is arranged, which sounds like an internal
> matter and has one consequence a non-engineer should insist on.
>
> There are three separate things being served: the public website, the tool for
> building apps, and the apps themselves once published. Somebody who only uses
> apps their colleagues built never receives the building tool at all. That is
> partly about speed, and mostly about safety: code that was never sent to their
> computer is code nobody can poke at.
>
> The other decision worth knowing is that the rules about who may do what live
> in one place, and everything else has to go and ask. There is a small piece of
> that in the screens, and it is explicitly labelled as advisory: it exists only
> so the interface can hide buttons somebody cannot use, and it is never trusted
> to actually stop them. Naming it that way in the code is what stops a future
> developer from reaching for it, believing they have locked something, and
> being wrong.

---

## 24. Responsive behaviour

### 24.1 The two responsive problems

They are different and the document keeps them apart:

1. **The marketing surface** is responsive in the ordinary sense: one content
   set, three breakpoints, the measured behaviour of Section 3.8.
2. **The product surface** is not one layout at three sizes. The editor is a
   desktop instrument and says so; the runtime is where the responsive work
   happens, because a published app is read on a phone in a warehouse.

### 24.2 The editor

**Capability requirement - normative.** Below the stated minimum width the
editor does not attempt a phone layout. It states plainly that authoring needs a
larger display, and offers the app's preview, which is fully usable. A collapsed,
tab-switched, four-region editor on a phone is worse than an honest refusal:
it looks usable and it is not.

Between the minimum and the desktop width the rails collapse to overlays and the
canvas keeps the full width.

### 24.3 The runtime

**Capability requirement - normative.** A published app declares its layout per
breakpoint. The builder authors the desktop layout and may override placement
per breakpoint; where they do not, components stack in tree order at full width.

| Component | Below the stated breakpoint |
|---|---|
| Table | Column priority per column; low-priority columns collapse into an expandable row detail. Horizontal scrolling of a fifteen-column grid on a phone is not a responsive strategy |
| Form | One column, full-width controls, and the submit is reachable without the keyboard covering it |
| Modal | Full-screen sheet |
| Tabs | Scrollable strip, never wrapped to two rows |
| Chart | Legend below, tooltips on tap with an explicit dismiss |

### 24.4 Touch

Every interaction in the runtime is reachable by touch, at the stated minimum
target size, and no runtime interaction requires hover to be discoverable. Hover
in the runtime is enhancement only.

> **In plain language.** How it behaves on smaller screens, and there are two
> different answers because there are two different problems.
>
> The public website is responsive in the ordinary way: the same content
> rearranged for phone, tablet and desktop.
>
> The tool for building apps is not. It is a desktop instrument and it says so.
> Below a certain width it does not attempt a phone version; it says plainly that
> building needs a bigger screen, and offers a fully working preview of the app
> instead. That is a deliberate refusal. A four-panel building tool crammed into
> a phone looks usable and is not, which wastes somebody's time more thoroughly
> than an honest message would.
>
> The published apps themselves absolutely do have to work on a phone, because
> that is where they get used: somebody in a warehouse, on a shop floor, in a
> van. The one that needs real thought is the table. Fifteen columns on a phone
> is not solved by letting people scroll sideways. Instead each column is ranked,
> the important ones stay, and the rest fold into a row you can tap open.

---

## 25. Accessibility

### 25.1 The standard, and the honest part

**Capability requirement - normative.** The marketing surface and the runtime
meet the stated conformance level in full. The editor canvas meets it for every
surface except direct manipulation, where the requirement is restated rather
than waived: **every canvas operation has a keyboard path**, per Section 19.4,
and that path is documented in the interface rather than only in a help page.

### 25.2 Structure

| Requirement | Detail |
|---|---|
| Landmarks | One main per view, banner, contentinfo, and navigation landmarks labelled where there are several |
| Headings | One first-level heading per view, no skipped levels |
| Names | Every control has an accessible name that matches its visible label where it has one |
| Language | Declared on the document, and on any element whose language differs |
| Titles | Unique per route, leading with the specific and ending with the product |

### 25.3 The four surfaces that need their own answer

| Surface | The requirement |
|---|---|
| Canvas | A tree view is the accessible peer of the canvas, not a fallback: selection, reorder, reparent, resize and delete all work from it, and the two stay synchronised |
| Data grid | A grid role with correct row and column counts including virtualised rows, arrow-key navigation, and an announcement of the row count after every filter |
| Overlays | Focus moves in on open, is trapped, returns to the invoking control on close, and escape always closes |
| Live regions | Query completion, save state, validation failure and permission refusal are announced; a refusal that is only a colour change has not been communicated |

The grid row is where this is most often failed, because virtualisation and
correct row counts are in direct tension. Reporting the count of rendered rows
rather than the count of total rows tells a screen reader user that a fifty
thousand row table has thirty rows in it.

### 25.4 Motion and contrast

**Capability requirement - normative.** A reduced-motion preference removes
scroll-driven transforms, entrance animations and looping media, and preserves
every state change as an instantaneous one. Nothing in the build conveys state
by colour alone. Contrast is met at the stated ratios for text, for interface
components and for the focus indicator, in both themes of Section 3.7.

> **In plain language.** Making sure the product works for people who cannot use
> a mouse, cannot see the screen, or have asked their computer to stop moving
> things around.
>
> For the website and for the published apps, that is the full standard, no
> exceptions. For the building tool there is one honest complication: dragging
> things around a canvas is inherently a mouse activity. Rather than pretend
> otherwise or quietly skip it, the answer is that the list of components down the
> side is not a lesser alternative to the canvas. It is an equal one. Everything
> you can do by dragging can be done from that list with a keyboard: select,
> move, resize, nest, delete.
>
> The one that is most often got wrong is the big table. Because only the rows
> you can see actually exist on the page, a screen reader is usually told the
> table has thirty rows in it when it has fifty thousand. Getting that number
> right is fiddly and it is the difference between a usable table and a
> misleading one.
>
> And for anyone who has asked for less movement: everything that slides, fades
> or drifts simply stops. Not shortened. Stopped. Every change still happens, it
> just happens instantly.

---

## 26. Performance

### 26.1 What is being measured, and where

The marketing surface and the product are measured against different things, and
one budget for both is how a product gets optimised for a lighthouse score while
the grid stays slow.

| Surface | The measure that matters |
|---|---|
| Marketing | Time to the first meaningful paint, and stability of the layout after it |
| Editor | Interaction latency under a large app, per Section 19.9 |
| Runtime | Time from route entry to first useful row, and grid interaction latency |

### 26.2 Reference conditions

Every bound in this document is stated against: a four-year-old mid-range
laptop, a throttled connection at the stated profile, and an app of two hundred
components and thirty queries over a table of fifty thousand rows. A bound
without conditions is a wish.

### 26.3 The marketing budget

| Measure | Bound |
|---|---|
| Initial payload, compressed | stated cap, and the cap is enforced in the build |
| Fonts | Subset, preloaded for the first-render faces only, with the fallback metrically matched so the swap does not move the layout |
| Media | Deferred below the fold, dimensions declared, and no autoplaying video above the fold on a metered connection |
| Layout stability | No shift after first paint from anything the build controls |
| Third parties | Loaded after interaction or after consent, never blocking first paint |

### 26.4 The product budget

| Measure | Bound |
|---|---|
| Editor bundle | Split so that the runtime is not paid for twice, and the resource-type editors of Section 27.7 are loaded on demand |
| First useful row | Time from route entry to first row rendered, with the query's own duration reported separately so a slow resource is not mistaken for a slow product |
| Grid scroll | Sustained frame rate at the stated bound with virtualisation active |
| Save | Proportional to the operations, not to the app, per Section 19.9 |
| Memory | Bounded across a long editing session; an operation log that grows without compaction is a leak with a good excuse |

### 26.5 Server bounds

| Path | Bound |
|---|---|
| Decision | The authorisation call of Section 28.2 is bounded and is not per row. A per-row permission check is the specification's named anti-pattern |
| Query dispatch | Platform overhead stated separately from resource time, in every response |
| Audit write | On the transaction, and bounded, per Section 29.3 |
| List endpoints | Cursor paginated, with no unbounded list endpoint anywhere in the API |

> **In plain language.** How fast it has to be, and under what conditions.
>
> The important part is the second half of that sentence. A speed target with no
> conditions attached is a wish. So every number in this build is measured on a
> four-year-old mid-range laptop, on a deliberately slowed connection, with an app
> of two hundred pieces and thirty database questions over a table of fifty
> thousand rows. Anything that is fast on a new machine on office broadband with
> ten rows of test data has been measured under conditions that do not exist.
>
> The website and the product are judged on different things, deliberately. For
> the website, how quickly something meaningful appears, and whether the page
> stops jumping about once it has. For the product, how quickly it reacts while
> you are working in it.
>
> One measurement is separated out on purpose: when a screen is waiting on a
> customer's own database, the time their database took is reported apart from
> the time our product took. Otherwise every slow database in the world looks
> like a slow product, and nobody can tell the difference well enough to fix
> either.

---

## 27. Backend and data contract

### 27.1 Scope, and why this section is the largest in the document

The marketing surface of Sections 12 to 17 talks to a server for three things:
a demo request, a newsletter subscription and a search index. That is a
half-page contract and it is given in Section 27.11.

Everything else in this section specifies the product the marketing surface is
selling: a governed internal-tools platform where the browser is a thin
authoring client and every fact of consequence lives on the server. The
authenticated surface could not be captured, for the reason given in
Section 34.2, so this section is normative specification rather than
measurement, and it is labelled as such throughout.

The one sentence that generates the rest of the section:

**The client never holds a credential, never composes a statement, and is never
the authority on what a principal may see.**

Every subsection below is a consequence of that sentence. A build that violates
it once has not built this product, however closely the pixels match.

### 27.2 The principal model

Six principal types. They are not roles; roles are attached to them.

| Principal | Created by | Authenticates with | Can hold grants |
|---|---|---|---|
| `user` | invitation or identity-provider provisioning | password with second factor, or federated assertion | yes |
| `group` | admin, or mapped from an identity-provider claim | not applicable | yes, and members inherit |
| `service_account` | admin | key pair, rotated | yes, never interactive |
| `agent` | builder, scoped to one app or workflow | delegated token, always acting for a user | yes, never more than its delegator |
| `workflow` | builder | internal token bound to the run | yes, bounded to its declared resources |
| `installation` | operator | instance identity | administrative only |

Two rules that the type table exists to make enforceable:

1. **An `agent` principal may never hold a grant its delegating `user` does not
   hold.** The check is at grant resolution, not at grant assignment, because
   the delegator's rights can shrink after the agent is created.
2. **A `service_account` may never be a member of a group whose grants were
   authored for interactive users.** Non-interactive principals get their own
   groups, so that a human-facing permission change cannot silently widen a
   machine's reach.

### 27.3 Core entities

Twenty-two tables. Names are indicative; the shape is normative.

| Entity | Key relationships | Notes |
|---|---|---|
| `organization` | root of every scope | carries residency region and retention policy |
| `workspace` | belongs to `organization` | the unit apps and resources live in |
| `membership` | `user` x `workspace`, with role and expiry | expiry is a column that something reads, per Section 28.6 |
| `group` | belongs to `organization`, self-referential parent | nesting is depth-limited and cycle-checked at write |
| `group_member` | `group` x principal | carries `source`: manual, or the identity-provider claim it came from |
| `resource` | belongs to `workspace`, typed | holds no secret; holds a reference to one |
| `credential` | belongs to `resource`, per `environment` | ciphertext only, per Section 27.6 |
| `environment` | belongs to `organization` | at least staging and production; ordered for promotion |
| `app` | belongs to `workspace` | a container, not a version |
| `app_version` | belongs to `app`, immutable, content-hashed | the thing that actually runs |
| `release` | `app_version` x `environment`, with promoter and time | promotion is an insert, never an update |
| `component` | belongs to `app_version` | tree, ordered, with layout and binding |
| `query` | belongs to `app_version`, references `resource` | parameterised, never concatenated |
| `query_run` | belongs to `query`, per execution | duration, row count, principal, outcome; no result payload |
| `workflow` | belongs to `workspace` | scheduled or triggered |
| `workflow_run` | belongs to `workflow` | step-level status, retry count, idempotency key |
| `permission` | grant edge: principal x scope x action x effect | explicit deny is a value, per Section 28.3 |
| `policy` | belongs to `organization` | column masks and row predicates, versioned |
| `audit_event` | append-only, hash-chained | Section 29 |
| `approval` | belongs to a promotable object | requester, approver, decision, bound hash |
| `api_key` | belongs to a principal, scoped | prefix stored in clear, remainder hashed |
| `erasure_request` | belongs to `organization` | tracks completion per store, per Section 29.6 |

Three shapes worth stating explicitly because they are the ones commonly got
wrong:

- **`app_version` is immutable and content-addressed.** Editing an app writes a
  new version. Promotion points an environment at a version. Rollback points it
  back. Nothing about a release is a boolean.
- **`query_run` never stores the result.** It stores that the run happened, who
  ran it, against what, for how long, and how many rows. Storing results turns
  the run log into a shadow copy of the customer's database with none of its
  access controls.
- **`permission` is an edge with an effect, not a role string on a user.** The
  resolution rules are Section 28.

### 27.4 The query contract

**Capability requirement - normative.**

A query is a named, parameterised, resource-bound statement stored against an
`app_version`. It is executed by the server on behalf of a principal. The
contract:

| Property | Requirement |
|---|---|
| Composition | Parameters are bound by the driver. String interpolation into a statement is a defect regardless of the escaping applied |
| Identity | Execution carries the acting principal, and the resource's own database user is not the authority on what the principal may see |
| Authorisation | Resolved per execution, per Section 28.4, before the statement is sent |
| Policy | Row predicates and column masks are applied by the server, per Section 28.7, on the path all readers share |
| Timeout | Bounded, per resource, with the connection returned to the pool on expiry |
| Cancellation | A superseded execution is cancelled at the resource, not merely ignored at the client |
| Concurrency | Bounded per organisation, per Section 27.9 |
| Result shape | Typed. A column's type travels with it, so the grid does not infer a date from a string |
| Errors | Typed and mapped, per Section 27.10 |
| Recording | One `query_run` row per execution, and one audit event per execution against a resource carrying a policy |

Request:

| Field | Type | Required | Validation |
|---|---|---|---|
| `app_version` | content hash | yes | must exist, must be the version released to the caller's environment when the caller is an end user |
| `query` | name | yes | must exist within that version |
| `parameters` | object | yes, may be empty | each key must be declared by the query; undeclared keys are rejected rather than ignored |
| `environment` | name | yes | must be one the principal may reach |
| `idempotency_key` | string | for mutating queries | per Section 27.8 |

Response states:

| State | Meaning | What the interface shows |
|---|---|---|
| `ok` | executed, rows returned | Result in the bound components, with row count and duration |
| `denied` | authorisation refused | A refusal naming the action, never the data that would have been returned |
| `invalid` | parameter validation failed | Field-level messages against the inputs that produced them |
| `unreachable` | resource could not be reached | The resource name and the failure class; never the host, never the credential |
| `timeout` | exceeded the resource's bound | The bound that was exceeded, and the option to re-run |
| `throttled` | organisation quota exhausted | The quota and when it resets, per Section 27.9 |
| `failed` | statement executed and errored | The driver's message, mapped per Section 27.10 |

The distinction between `denied` and `ok` with zero rows is load-bearing and
must be preserved end to end. Collapsing a refusal into an empty result set is
how a permission bug becomes invisible for a year.

### 27.5 The editor contract

The authoring client is not trusted with app state either. It holds a working
copy and sends operations.

**Capability requirement - normative.**

1. Canvas edits are transmitted as **operations against a base version hash**,
   not as a whole-document save. A save whose base hash is no longer current is
   rejected with the current version and the conflicting operations, per
   workflow H8.
2. The undo stack is a **command stack**: each operation carries its inverse.
   Reload replays the log rather than restoring a snapshot, so undo survives the
   session, per workflow H4.
3. **Autosave is to a draft, never to a release.** A draft is a mutable pointer
   at a chain of operations; a version is the frozen result of that chain.
4. **Two builders in one app is an expected state, not an error state.** Presence
   is broadcast. Conflict is surfaced with a diff. Silent overwrite is a defect.

### 27.6 Secrets

**Capability requirement - normative.**

| Rule | Detail |
|---|---|
| Storage | Credentials are encrypted at rest with a per-organisation key. The application key is not the database key |
| Envelope | Data keys are wrapped by a key manager the application cannot read in the clear, so a database compromise alone does not yield credentials |
| Egress | No credential, in whole or in part, is ever serialised into a response body, a bundled asset, a log line, an error, an audit record, an export or a support tool |
| Write-only fields | A credential field renders as a set indicator plus a replace action, never as a masked value that could be revealed by a client-side toggle |
| Rotation | Rotation is an operation with its own audit event, and the previous value is destroyed rather than versioned |
| Test connection | Tests run server-side and return reachable or not reachable, with a failure class, and never the resource's own error text verbatim when that text can carry the host or the user |

Workflow H6 asserts this against every other workflow's traffic. It is written
as an assertion over the whole run rather than as a page to visit, because that
is where this fails: not on the credential form, but in the error body of an
unrelated screen at three in the morning.

### 27.7 The resource surface

**Capability requirement - normative.** The platform must connect to resources
of at least these classes, and the class is what the specification binds, never
a vendor:

| Class | What the platform must handle | The correctness trap |
|---|---|---|
| Relational database | Pooling, parameter binding, typed results, transactions, timeouts | A pool sized per instance rather than per resource, so one slow resource starves every other |
| HTTP API | Auth schemes, retries with backoff, pagination, response typing | Retrying a non-idempotent POST |
| Object storage | Signed, expiring, single-purpose upload and download URLs | Signing a URL that grants the bucket rather than the object |
| Message or queue | Publish with delivery semantics stated | At-least-once treated as exactly-once downstream |
| Warehouse | Long-running statements, cost attribution, result size caps | No cap, so one query materialises a hundred million rows into memory |
| Model provider | Streaming, token accounting, prompt and response redaction | Customer data crossing into a provider whose region contradicts Section 29.7 |

Each resource declares its environment bindings, its timeout, its concurrency
bound and its retry policy. None of these are global constants.

### 27.8 Idempotency and retries

**Capability requirement - normative.**

1. Every mutating call across a service boundary carries an idempotency key.
2. The key is derived from the logical operation - the run and the step, the
   submission and the target - and never from wall-clock time or a random value
   generated at send time, because both defeat the retry they exist to protect.
3. Keys are retained at least as long as the longest retry window, and a
   repeated key returns the first result rather than re-executing.
4. Inbound webhooks are verified by signature before the body is parsed, and the
   delivery identifier is the idempotency key for the receipt.
5. A partially failed multi-step workflow resumes at the failed step. Re-running
   from the beginning is only correct if every prior step was idempotent, and the
   specification does not assume it was.

### 27.9 Quota, rate limiting and fair share

**Capability requirement - normative.**

| Dimension | Bound | Behaviour at the bound |
|---|---|---|
| Concurrent queries per organisation | configured per plan | queue, then `throttled` with a reset time |
| Queries per principal per minute | configured per plan | `throttled`, with the principal named in the audit event |
| Rows per result | configured per resource | truncate with an explicit truncation flag in the response, never silently |
| Payload size in and out | configured globally | reject at the edge before parsing |
| Workflow runs per schedule tick | exactly one | overlapping ticks skip with a recorded reason rather than stacking |

Scheduling between organisations is fair-share, not first-come: one organisation
saturating its own bound may not degrade another's latency. Workflow X6 asserts
exactly this, and it is the reason the bound is per organisation rather than
global.

### 27.10 Error mapping

**Capability requirement - normative.** Resource errors are mapped before they
leave the server. The mapping table is part of the build, not an afterthought:

| Source condition | Mapped state | What the actor is told |
|---|---|---|
| Authentication failure at the resource | `unreachable` | the resource name and that its credentials were refused |
| Host resolution or network failure | `unreachable` | the resource name and that it could not be reached |
| Statement syntax error | `failed` | the driver message, with host, port, user and database elided |
| Constraint violation | `failed` | the constraint's human name where the schema provides one |
| Statement timeout | `timeout` | the bound that was exceeded |
| Permission refusal inside the resource | `failed` | that the resource refused, distinctly from the platform refusing |

The last row matters: "your database said no" and "we said no" are different
facts, and merging them makes both permission systems undebuggable.

### 27.11 The marketing surface contract

Three endpoints, and this is the whole of what the unauthenticated site needs.

| Endpoint | Method | Fields | Response states |
|---|---|---|---|
| Demo request | POST | work email required and validated as an address, name, company, team size, message | `sent`, `invalid`, `spam`, `failed` |
| Subscription | POST | email required, source route | `sent`, `invalid`, `already`, `failed` |
| Site search | GET | query string, cursor | `ok`, `invalid`, `failed` |

**Capability requirement - normative.**

1. Both POST endpoints are rate limited per address and per source, and both are
   protected by a check that does not rely on a hidden field alone.
2. On `failed`, every value the visitor typed is retained in the form. Losing a
   demo request to a transient error is the most expensive single failure the
   marketing surface can produce.
3. Free-text fields are stored and rendered as text, never as markup, wherever
   they are later read, including in whatever internal tool the sales team reads
   them in.
4. Search is read-only, is not authenticated, and indexes only published public
   routes. An index that can be made to return a draft is a content leak.
5. Analytics is gated on consent, and no form field value is ever sent to an
   analytics destination.

> **In plain language.** This is the part that lives on the company's own
> machines rather than in the visitor's browser, and it is the biggest part of
> the build for one reason: the browser is not trusted with anything that
> matters.
>
> The public website barely needs a server at all. Three things: a form for
> asking for a demo, a box for signing up to the newsletter, and the search. If
> the demo form fails, whatever the visitor typed must still be sitting in the
> boxes, because losing a serious enquiry to a hiccup is the worst thing this
> half of the build can do.
>
> The product behind the sign-in is where the real work is. The rule that
> generates almost everything else in this section is a single sentence: the
> browser never holds a password to a customer's database, never writes the
> question that gets asked of it, and never decides what the person is allowed to
> see. Every one of those decisions is made on the server, every time, even when
> the screen has already decided to hide the button.
>
> A few specific things are worth understanding because they are the ones most
> often built wrongly.
>
> **A saved app is a new copy, not an edit.** Every time somebody saves, a
> complete frozen copy is kept. Publishing means pointing the live version at one
> of those copies. That is what makes going back to yesterday's version instant
> and safe rather than a rescue operation.
>
> **Being refused and finding nothing must never look the same.** If somebody is
> not allowed to see a customer's records, the answer is "you are not allowed to
> see this", not an empty screen. When those two are merged, a permission bug can
> sit undiscovered for a year, because an empty table looks like an honest empty
> table.
>
> **Passwords to customer databases are write-only.** You can set one and you can
> replace one. Nothing in the product will ever show you one again, in any
> screen, any log, any error message or any support tool, and the checks for that
> run across every other test rather than on the one page where the password is
> typed. That is deliberate: this never leaks on the password screen, it leaks in
> the error message of something unrelated.
>
> **The system assumes it will be asked to do things twice.** Networks retry.
> Buttons get double-clicked. Scheduled jobs overlap. So every instruction that
> changes something carries a label saying which instruction it is, and doing the
> same one twice does nothing the second time. Without that, a retry after a
> timeout charges a customer twice, and it will happen in the first month.

---

## 28. Authorization model

### 28.1 Why this is its own section

Because the alternative is that it is not one. The characteristic failure of
this product class is authorisation expressed as conditionals scattered through
feature code, where the rule that governs a screen lives in the screen. That
arrangement cannot be audited, cannot be tested as a matrix, and cannot answer
the only question anyone ever asks of it: *who can see this row, and why?*

**Capability requirement - normative.** Authorisation is a **layer** with a
single entry point. Feature code asks it a question and obeys the answer.
Feature code does not contain the rule.

### 28.2 The question the layer answers

One call, one shape, everywhere:

```
decide(principal, action, resource, context) -> allow | deny + reason
```

| Argument | Carries |
|---|---|
| `principal` | the acting identity, its type, its groups, its active grants and its delegation chain |
| `action` | a verb from a closed set: `read`, `write`, `execute`, `publish`, `promote`, `administer`, `export` |
| `resource` | the object and its full scope chain: organisation, workspace, app, environment, and where relevant the column |
| `context` | environment, time, source address, session assurance level, and the request identifier |

Three properties of the shape do the work:

1. **`reason` is always returned, on allow as well as on deny.** The reason is
   what makes the audit trail of Section 29 legible and the permission debugger
   of Section 22.4 possible. A decision that cannot explain itself is not
   auditable.
2. **`context` carries time.** Grants expire. A decision layer that cannot see
   the clock cannot express a time-bounded grant, which is workflow X3.
3. **`resource` carries the whole scope chain**, not the leaf. Inheritance is
   resolved inside the layer, so no caller has to know that a workspace grant
   implies an app grant.

### 28.3 Resolution order

Grants are edges with an effect. The order is fixed and is not configurable,
because a configurable resolution order is a permission system nobody can reason
about:

| Step | Rule |
|---|---|
| 1 | Collect every grant reaching the principal: direct, through group membership, through nested groups, through active time-bounded grants |
| 2 | Discard grants whose validity window does not contain the request time |
| 3 | Discard grants whose environment does not match the request environment |
| 4 | If any surviving grant is an explicit `deny` for this action at any scope in the chain, the decision is deny. **Deny always wins, and deny is never inherited away by a narrower allow** |
| 5 | If any surviving grant is an `allow` for this action at any scope in the chain, the decision is allow |
| 6 | Otherwise deny. **The default is deny, at every scope, for every action** |

Step 4 before step 5 is the entire design. A permission system where a narrow
allow can overcome a broad deny cannot express "this group may never export",
which is the sentence every compliance review asks for.

### 28.4 Where the decision is made

**Capability requirement - normative.**

| Surface | Decision required | Client may |
|---|---|---|
| Query execution | Yes, per execution, before the statement is sent | nothing |
| Mutating query | Yes, and separately from the read that populated the form | nothing |
| App load | Yes, for the version and the environment | nothing |
| Component visibility | Advisory only | hide, for tidiness |
| Export | Yes, and distinctly from `read`, per Section 28.7 | nothing |
| Promotion | Yes, plus the approval of Section 28.8 | nothing |
| Administration | Yes | nothing |

The second column is the specification. The third column exists to say something
the first cannot: the client is permitted to hide a control it believes is
disallowed, purely so the interface is not a field of dead buttons, and that
hiding is **never** the enforcement. Workflow H2 drives the API directly with a
principal whose client would have hidden the control, and a build that succeeds
there has failed the workflow.

### 28.5 Caching a decision

**Capability requirement - normative.** Decisions may be cached. The cache has
four obligations:

1. Keyed by principal, action, resource and environment, and by the version of
   every grant and policy that contributed to the decision.
2. Invalidated by any write to a grant, a group membership, a policy or a
   principal's status, propagating within a stated bound measured in seconds.
3. Never spanning organisations, including in warming and pre-computation jobs.
   Workflow X9 asserts this against a background job specifically because that
   is where cross-tenant leakage survives.
4. Never used to satisfy a decision whose context includes an expiring grant
   within its remaining window.

Obligation 2 is what workflow X1 measures. A session-lifetime authorisation
cache is the most common way a departed employee keeps access, and it is
invisible until somebody tests for it.

### 28.6 Time-bounded grants

**Capability requirement - normative.**

1. Every membership and every grant may carry a validity window.
2. Expiry is enforced **at decision time**, not by a job that sweeps the table.
   A sweeper is a correctness backstop and a tidiness measure; it is never the
   mechanism, because a sweeper that fails leaves access open.
3. Elevation is requested with a stated reason, approved by a principal other
   than the requester, and bounded at grant time to a maximum the organisation
   configures.
4. The elevated interval is queryable as an interval: who, what, from when, to
   when, on whose approval, for what stated reason.

### 28.7 Row predicates and column policy

**Capability requirement - normative.**

| Mechanism | Applied where | Asserted by |
|---|---|---|
| Row predicate | Composed into the statement server-side, as a bound predicate, before execution | H3 |
| Column mask | Applied to the result on the server, on the single path every reader shares | X4 |
| Export policy | A separate action, decided separately from `read` | X4 |

Two rules that the word "shared" in that table is carrying:

- **There is one result path.** The app renderer, the raw result pane, the CSV
  export, the scheduled workflow's output and the public API return results
  through the same masking code. A second path is how X4 is failed, and it is
  usually the export, because the export was written last and by somebody else.
- **A mask is not a formatting rule.** The masked value never leaves the server.
  Sending the value and starring it in the client is a leak with a costume on.

Aliasing, aggregating and joining around a masked column are all attempts the
workflow makes. The defence is that masking is bound to the column's identity in
the result, not to its name in the statement.

### 28.8 Approval as an authorisation primitive

**Capability requirement - normative.** Promotion to a protected environment
requires an approval that is:

1. **Granted by a principal other than the requester.** Self-approval is refused
   even when the requester holds the approve grant.
2. **Bound to the exact content hash** of the version being promoted. Any edit
   invalidates the approval; there is no such thing as an approval of an app.
3. **Recorded with the reason given at request time**, which is a required field.
4. **Expiring.** An approval not acted on within its window lapses rather than
   waiting indefinitely.

### 28.9 The permission matrix must be inspectable

**Capability requirement - normative.** An administrator can ask, and get an
answer without reading code:

| Question | The answer must show |
|---|---|
| What can this principal reach? | every resource, the action, and the grant chain that produced it |
| Who can reach this resource? | every principal, direct and inherited, with the same chain |
| Why was this decision made? | the ordered rules that fired, ending on the one that decided |
| What changed? | a diff of the matrix between two points in time |

The last row is why grants are versioned rather than updated in place. "Who
could see this in March" is a question that gets asked after an incident, and a
mutable permission table cannot answer it.

> **In plain language.** This section is about who is allowed to see and do
> what, and it is separate from everything else on purpose.
>
> The usual way this gets built is that each screen decides for itself, with a
> line of code buried in it saying "if this person is an admin". That works right
> up until somebody asks a question the company will definitely eventually ask:
> *who exactly can see this customer's records, and how did they get that
> permission?* With the rules scattered across two hundred screens, nobody can
> answer. So here the rules live in one place, and every screen has to ask that
> one place before it does anything.
>
> There are a few rules about how the answer is worked out, and they matter more
> than they sound.
>
> **The starting answer is always no.** Permission has to be granted, never
> assumed, at every level.
>
> **A ban always beats a permission.** If somebody has been specifically barred
> from exporting data, no other permission anywhere can quietly re-enable it.
> Without that rule you cannot express "these people may never export", which is
> the first thing any security review asks for.
>
> **Hiding a button is not security.** The screen is allowed to hide controls
> somebody cannot use, so the interface is not full of dead buttons. But the
> server has to refuse the action independently, because anyone can make the
> request without using the screen. One of the tests does exactly that.
>
> **Permissions have expiry dates that are actually checked.** Temporary access
> for an emergency has to end by itself. The dangerous version of this is a
> system with an expiry date written down that nothing ever looks at, and a
> nightly clean-up job that quietly stopped running in March.
>
> **When somebody loses access, they lose it now.** Not the next time they log
> in. If a person leaves the company at two o'clock, two o'clock is when the
> screens stop working for them, and one of the tests sits there with a session
> already open to check.
>
> **Hidden columns are hidden on the server.** If somebody is not allowed to see
> a customer's home address, the address never leaves the building. Sending it to
> the browser and covering it with asterisks is not hiding it, and the test tries
> to get at it through the spreadsheet export, which is where that shortcut is
> always found out.

---

## 29. Audit, retention and observability

### 29.1 What an audit trail is for

Not for debugging. Debugging is Section 29.8. An audit trail exists so that a
person who does not trust the operator can establish, later, what happened. That
reader changes the requirements completely: the record must be complete, must be
attributable, must be ordered, and must be impossible to have quietly altered by
the operator whose behaviour it records.

**Capability requirement - normative.** The audit store is append-only. No
application principal holds update or delete on it. If the deployment's database
grants those to the application user, the audit trail is decorative.

### 29.2 What is recorded

| Event class | Recorded on | Carries beyond the common envelope |
|---|---|---|
| Authentication | sign-in, sign-out, failure, second-factor challenge, federated assertion | assurance level, identity provider, and the claim set on a federated sign-in |
| Authorisation | every deny, and every allow on a policy-carrying resource | the decision reason from Section 28.2 |
| Query execution | every execution against a resource carrying a policy, and every mutating execution | query identity, resource, row count, duration, outcome, and never the result |
| Editing | app version created, component changed, query changed, resource created or edited | the version hash before and after |
| Release | promotion, rollback, approval requested, granted, refused, lapsed | environment, version hash, approver |
| Identity | member invited, accepted, removed, group membership changed, provisioning event | the source of the change: manual, or the provider claim |
| Permission | grant created, edited, revoked, expired, policy version published | the diff |
| Secret | credential set, rotated, deleted, test-connection run | never any part of the value |
| Erasure | request received, per-store completion, final attestation | the stores covered |
| Administration | setting changed, key issued or revoked, residency or retention altered | previous and new value |

The common envelope on every event: event identity, monotonic sequence within
the organisation, time from a trusted source, acting principal and its type, the
delegation chain where the actor is an `agent`, source address, request
identifier, session identity, organisation, workspace, target object and its
version, outcome, and the hash of the preceding event.

### 29.3 Tamper evidence

**Capability requirement - normative.**

1. Each event carries the hash of its predecessor within the organisation's
   chain, so an alteration or a deletion breaks every subsequent link.
2. The chain head is anchored on a stated interval to a store the application
   cannot write, so that rewriting the entire chain is also detectable.
3. Verification is an operation an auditor can run themselves, returning the
   first divergent sequence number rather than a boolean.
4. Records are written on the same transaction boundary as the effect they
   record. An effect that commits without its event, or an event that commits
   without its effect, are both defects.

Point 4 is the one most often skipped, and it is what makes the difference
between an audit trail and a log of things the application remembered to
mention.

### 29.4 Reading the trail

**Capability requirement - normative.** The trail is queryable by actor, by
target object, by action, by outcome and by time window, in combination, at a
latency that makes an incident review possible rather than theoretical. Results
are paginated and exportable, and the export is itself an audited action, per
Section 28.4.

An auditor's session is read-only by construction: the auditor role holds `read`
on the audit scope and holds nothing else anywhere, so an auditor cannot alter
the thing they are auditing even by accident.

### 29.5 Retention

**Capability requirement - normative.**

| Class | Bound |
|---|---|
| Audit events | Retained for the organisation's configured compliance window, which has a floor the operator cannot lower below the regulatory minimum for the region |
| Query run records | Retained on a shorter window than audit events, because they are operational |
| Query results | Not retained. There is no result cache that outlives the request unless the organisation enables one explicitly, and an enabled cache inherits the policy that produced the rows |
| Drafts and versions | Retained per app, with a configurable ceiling on version count and a floor of the currently released version plus its predecessor |
| Personal data in operational stores | Retained per the organisation's policy, and enumerated per store so that Section 29.6 can be satisfied |

### 29.6 Erasure

**Capability requirement - normative.** An erasure request must be satisfiable
across every store that holds a copy, and the specification requires those
stores to be enumerated rather than remembered:

| Store class | Obligation |
|---|---|
| Primary tables | Remove or irreversibly anonymise |
| Search indexes | Remove, and confirm removal by query rather than by assumption |
| Caches | Invalidate, including any pre-computed authorisation decision keyed on the principal |
| Derived and denormalised stores | Enumerated per deployment; each reports its own completion |
| Exports and generated files | Removed from object storage, including versioned copies |
| Backups | Covered by a stated policy, with the restoration path required to re-apply outstanding erasures |
| Audit trail | **Retains the event, the actor, the time and the outcome. Discards the payload.** |

The final row is the one that decides whether an erasure implementation is
correct. Erasing the audit event destroys the evidence that the erasure was
performed, which fails the same regulation it was trying to satisfy. Workflow X7
asserts both halves.

### 29.7 Residency

**Capability requirement - normative.** An organisation pinned to a region has
its primary rows, its query results in transit, its logs, its search indexes,
its exports and its backups confined to that region. Cross-region movement is
permitted only for data the organisation has classified as non-personal, and
every crossing is recorded.

The trap this is written against is not a page. It is a background job:
cache warming, index rebuilding, aggregate computation and usage reporting are
all written by somebody who is thinking about throughput, and each of them will
happily read every organisation in one pass. Workflow X9 drives a background job
for that reason.

### 29.8 Observability, which is a different thing

**Capability requirement - normative.**

| Signal | Requirement |
|---|---|
| Tracing | A request identifier is generated at the edge, propagated across every service boundary, attached to every log line and returned to the client on error so a user can quote it |
| Logs | Structured. Per-organisation isolation, so support cannot read one tenant's logs while investigating another |
| Personal data in logs | Prohibited. Parameters are logged by name and type, never by value. Result rows are never logged |
| Metrics | Per organisation, per resource, per query: rate, error rate, duration distribution, quota consumption. High cardinality on organisation and resource is a requirement, not an accident |
| Alerting | Bound to stated objectives on the query path and the editor save path, because those two are what an outage of this product actually means |
| Cost | Query cost attributable to organisation, workspace and app, so that Section 27.9 can be enforced on evidence rather than on guesswork |

The separation from Section 29.1 is deliberate and worth stating: the audit
trail answers "who did this", is retained for years and may not be edited; the
observability stack answers "why is this slow", is retained for weeks and is
routinely dropped. Merging them produces a system that is too noisy to audit and
too expensive to keep.

> **In plain language.** Two different record-keeping systems, built for two
> different readers, and it matters that they stay separate.
>
> The first is the audit trail, and it is not for the engineers. It is for
> somebody a year from now, possibly somebody who does not trust the company,
> asking who looked at a particular customer's record. So it records every
> meaningful action: who signed in, who was refused, who ran what against which
> database, who changed somebody's permissions, who published what to the live
> system and who approved it.
>
> The important property is that it cannot be quietly edited. Each entry is
> sealed with a fingerprint of the one before it, so removing or changing a
> single line breaks every line after it and the break can be found. The company
> running the software cannot rewrite its own history without that being
> detectable, and an auditor can run the check themselves rather than being told
> the result. An audit trail that the operator can edit is not an audit trail; it
> is a diary.
>
> It also records what it must not keep. It notes that a query ran, who ran it
> and how many rows came back. It never keeps the rows. Otherwise the audit
> system slowly becomes a second, unprotected copy of the customer's database.
>
> When somebody exercises their right to be forgotten, their data has to go from
> everywhere it was copied to: the main tables, the search, the caches, the
> spreadsheet exports sitting in storage, and the backups. But the audit trail
> keeps the fact that the erasure happened, who asked and when, and throws away
> only the personal details. Deleting the record of the deletion would destroy
> the proof that the law was followed.
>
> The second system is the ordinary engineering one: what is slow, what is
> failing, which customer is affected. It is noisy, it is kept for weeks rather
> than years, and it is allowed to be thrown away. The one hard rule it shares is
> that customer data never appears in it. The system records that a query ran
> with a parameter called `customer_email`; it never records what that email was.

---

## 30. Graded workflows and difficulty tiers

### 30.1 Why this section exists

This build is not delivered as one score. It is delivered as a set of **graded
workflows**: end-to-end journeys a verifier drives against the running
application and marks passed or failed. The score is the ratio.

```
score = journeys passed / total journeys
```

A workflow is a journey, not a unit test. It starts at a URL with a stated
actor and ends at an assertion about state that the actor can see, or about
state the actor must not be able to see. Nothing in this section is graded by
reading source. Source that looks correct and does not run scores zero, and a
deploy that does not come up is a hard zero for the whole run.

### 30.2 The ladder, and where this product sits on it

The corpus ladder has five rungs: trivial, easy, medium, hard, expert.
**Difficulty is measured, never declared** - a workflow's rung is assigned from
observed pass rates across agents, not from how hard it looked when it was
written. The rung labels below are therefore predictions, and the calibration
run is what settles them.

This product contributes nothing at trivial and nothing at easy, and that is a
property of the product rather than an authoring choice. The smallest useful
action in an internal-tools platform crosses a resource boundary: it opens a
connection the operator configured, runs a statement against somebody else's
database, and returns rows that a permission rule may have to strip before they
reach the browser. There is no version of that which is a form posting to
itself. The three rungs this build populates are:

| Rung | What a workflow at this rung demands | Actors | Boundary crossed |
|---|---|---|---|
| Medium | One correct round trip. A single actor, a single resource, a single unit of state that changes and stays changed. | 1 | client to server to one external resource |
| Hard | Correctness under a second party. Two actors with different rights, or one actor plus concurrency, or one actor plus an integration that can lie. | 2, or 1 plus a race | tenant isolation, release boundary, integration contract |
| Expert | Correctness under an organisation and under time. Policy that outlives a session, evidence that must survive tampering, grants that expire, stores that must forget. | many, including a machine principal | org, environment, region, retention window |

The move from medium to hard is the move from "does it work" to "does it still
work when somebody else is in the room". The move from hard to expert is the
move from "does it still work" to "can you prove it did, a year later, to
somebody who does not trust you".

### 30.3 Medium workflows

Single actor. Every one of these is a complete journey and none of them is a
component demo.

| ID | Workflow | Actor | Passes when |
|---|---|---|---|
| M1 | Connect a resource | admin | A Postgres resource is created from host, port, database, user and password; a test connection reports reachable; the resource appears in the resource list with its type and its last-tested time |
| M2 | Author and run a read query | builder | A query named against the M1 resource returns rows in the query result pane, with the row count and the execution time shown, and the same query re-run after a table change returns the changed rows |
| M3 | Bind a table to a query | builder | A table component dropped on the canvas is bound to the M2 query, renders one column per returned field, and paginates without refetching the full result set |
| M4 | Write one row through a form | builder | A form bound to an insert query creates a row, the bound table refreshes without a page reload, and the new row is present after a hard reload |
| M5 | Persist the canvas | builder | An app with at least four components at non-default positions is saved, the browser is closed, and the app reopens with every position, size and binding intact |
| M6 | Server-side filter, sort and search | end user | Filtering, sorting and searching a table of at least fifty thousand rows is executed by the resource, not in the browser; the network shows one request per interaction and the payload never carries the full table |
| M7 | Typed query failure | builder | A query pointed at a resource with a rotated password fails with a typed, human-readable error naming the resource and the failure class, and no stack trace, no host name and no credential fragment reaches the browser |
| M8 | Invite a member | admin | An invited address receives an invitation, accepts it, lands in the workspace, and sees exactly the apps their group grants and no others in the app list |
| M9 | Environment switch | builder | The same query run against the staging environment and the production environment uses different credentials and returns different rows, and the environment in force is visible in the editor at all times |
| M10 | Run an app as an end user | end user | The published app opens at its own URL with no editor chrome, no component tree, no query panel and no route by which an end user can reach the editor |

**What fails first at this rung.** Filtering fifty thousand rows in the browser
after fetching all of them. A table that renders but paginates client-side. A
save that stores component positions but not bindings, so the app reopens
looking right and doing nothing. A query error surfaced as the raw driver
exception, which is how connection strings end up in a screenshot.

### 30.4 Hard workflows

Two actors, or one actor and a race, or one actor and an integration that is
allowed to misbehave.

| ID | Workflow | Actors | Passes when |
|---|---|---|---|
| H1 | Release boundary | builder, end user | The builder edits a published app; the end user's running session continues to serve the published release; the end user sees the change only after the builder promotes it, and can be moved back by promoting the previous release |
| H2 | Group-scoped mutation | admin, support member | A member of a read-only group opens an app containing a delete button, and the delete is refused by the server, not hidden by the client; hiding it in the client and permitting it at the API is a fail |
| H3 | Row-level restriction | two members of different groups | The same app opened by two actors returns different row sets from the same query, the restriction is applied by the server, and neither actor can widen it by editing a client-side parameter |
| H4 | Undo across a session | builder | Twenty canvas operations including a delete, a resize, a rebind and a multi-select move are undone and redone in exact inverse order; the stack is a command stack, so a reload replays to the same state rather than restoring one snapshot |
| H5 | In-flight query discipline | end user | Rapid interaction fires overlapping queries; superseded requests are cancelled, results arrive in request order or are discarded, and the grid never renders the response to a filter the user has already changed |
| H6 | Secrets stay server-side | builder, inspector | No credential, connection string, bearer token or private key appears in any client payload, any bundled asset, any error body or any audit record rendered in the browser, at any point in any of the other workflows |
| H7 | Webhook receipt | machine principal | An inbound webhook with a valid signature is accepted once; the same delivery replayed is accepted zero further times; an invalid signature is rejected; a slow handler does not block the response |
| H8 | Concurrent editors | two builders | Two builders edit one app at once; the second save does not silently overwrite the first; the loser is told what happened and offered the diff. Last-write-wins is a fail even when no data is lost by luck |
| H9 | Query timeout and blast radius | builder | A deliberately slow statement is cut off at the stated timeout, the connection is returned to the pool, and the workspace stays responsive for every other actor while it runs |
| H10 | Scheduled run | machine principal | A workflow scheduled every fifteen minutes runs, records a run history entry with its output and duration, retries a failure with backoff, and does not run twice for one schedule tick |

**What fails first at this rung.** Permission enforced in the client only, which
is the single most common way this product class is built wrong. A release model
that is a boolean rather than an immutable version, so promoting cannot be
undone. Undo implemented as a snapshot stack, which is undetectable until a
multi-select move is undone. Overlapping queries resolved in arrival order, so
the grid settles on the answer to a stale filter. A webhook handler with no
signature check and no idempotency key, which works perfectly until the provider
retries.

### 30.5 Expert workflows

An organisation, a clock, and a reader who does not trust the operator.

| ID | Workflow | Principals | Passes when |
|---|---|---|---|
| X1 | Identity revocation mid-session | identity provider, member | A member is removed from a group at the identity provider; their existing session loses the app on the next authorised action rather than on next login; the removal is visible in the audit trail as an identity event, not as an application event |
| X2 | Tamper-evident audit | auditor | Every query execution, permission change, release promotion, resource edit and credential rotation is recorded append-only with actor, principal type, request identifier, source address and time; the chain is verifiable; a record altered directly in the store is detectable by that verification |
| X3 | Break-glass grant | approver, on-call engineer | An engineer requests elevated access with a reason, an approver who is not the requester grants it for a bounded window, the grant expires on its own, and the elevated period is queryable as a distinct interval in the audit trail |
| X4 | Column-level policy | policy admin, analyst | A policy masks a column for one group; the mask holds in the app, in the raw query result, in a CSV export and in a scheduled run's output; an analyst cannot recover the value by aliasing the column, aggregating it, or joining around it |
| X5 | Promotion with approval | builder, approver | Promotion from staging to production requires an approval from a principal other than the author, the approval is bound to the exact release hash, and re-promotion after any edit requires a fresh approval |
| X6 | Noisy tenant | two organisations | One organisation saturates its query quota; the other organisation's queries are unaffected in latency and in success rate; the throttled organisation gets a typed quota error rather than a timeout |
| X7 | Erasure across stores | data subject, operator | An erasure request removes the subject's personal data from primary tables, caches, search indexes, exports and query result history, while the audit trail retains the event, the actor and the time and no longer retains the payload |
| X8 | Idempotent cross-service retry | machine principal | A workflow run that fails after a partial external write is retried and does not double-write; the idempotency key is derived from the run and step, not from wall-clock time; the reconciliation is visible in the run history |
| X9 | Residency pinning | two organisations in two regions | An organisation pinned to a region has its rows, its query results, its logs and its backups stay in that region; a cache-warming job crossing the boundary is a fail even though no user ever sees the data |
| X10 | Full-fidelity export and reimport | operator | A workspace exports apps, queries, permission groups and environment bindings as portable definitions, and a reimport into an empty workspace reproduces the permission matrix exactly, including denies |

**What fails first at this rung.** Authorisation checked once at login and cached
for the session, so X1 fails silently. An audit table with an UPDATE grant on it,
which is not an audit table. Grants with an expiry column that nothing ever
reads. A masking policy applied in the presentation layer, which X4's export path
walks straight around. Cross-tenant leakage in the one code path nobody drives by
hand, which is why X9 is written as a background job rather than as a page.

### 30.6 Composition, and how it differs from the corpus

Thirty workflows, ten at each rung, each worth one thirtieth. **The set is not
weighted.** The programme's scoring contract is `journeys passed / total
journeys` and this document does not invent a second one on top of it: a hard
workflow is not worth two medium ones, it is simply harder to pass, and letting
the pass rate say so is the entire point of measuring difficulty rather than
declaring it.

| Rung | Workflows | Share of this graded set | Share of the corpus | What passing the rung certifies |
|---|---|---|---|---|
| Trivial | 0 | 0 percent | 5 percent | not exercised by this product |
| Easy | 0 | 0 percent | 20 percent | not exercised by this product |
| Medium | 10 | 33 percent | 40 percent | The agent can build a correct product surface over a real data source |
| Hard | 10 | 33 percent | 25 percent | The agent can keep it correct with a second party present |
| Expert | 10 | 33 percent | 10 percent | The agent can reason about an organisation over time |

The two right-hand columns are the interesting comparison. Across the whole
corpus the ladder narrows sharply towards the top: two thirds of all tasks sit
at medium or below, and expert is one task in ten. This build inverts that. It
contributes nothing at the bottom two rungs and three times the corpus share at
the top, because an internal-tools platform is one of the few products whose
ordinary requirements are genuinely organisational.

That makes this task a **calibration instrument rather than a representative
sample**. It is not here to tell you how an agent does on average. It is here to
find the cliff: the rung at which a model that looked competent stops being
competent. A frontier model is expected to clear most of the medium set, to be
mixed across the hard set, and to fail most of the expert set, and the exact
place where that transition happens is the measurement this task exists to
produce.

Two consequences for whoever reads a score from this task:

1. **A score around a third is a pass of the medium set and nothing else.** That
   is a real result and it means the agent built a working product. It is not a
   product anybody should connect to a production database.
2. **A score above two thirds is an extraordinary claim** and should be checked
   against the negative assertions of Section 30.7 before it is believed, because
   the cheapest way to appear to pass this set is to satisfy every workflow that
   asks for something to happen and none that asks for something to be refused.

### 30.7 Rules the graded set obeys

1. **Every workflow is driven through the interface or the public API.** None is
   asserted by reading the database directly, except where the assertion is
   specifically that the database does not contain something.
2. **Negative assertions are first-class.** Half of the hard and expert set
   asserts that something is *not* visible, *not* permitted or *not* retained.
   A build that only satisfies positive assertions is the failure mode this
   whole tier structure exists to catch.
3. **No mocks at any stage.** Every resource, identity provider, mail sink and
   object store the workflows touch is a real service the verifier can
   interrogate.
4. **Credentials for the admin, the auditor and the mail sink are withheld from
   the build and held by the verifier.** A build that invents its own admin
   account passes nothing.
5. **The rung is a prediction until calibration.** Any workflow that every agent
   passes moves down a rung, and any workflow no agent passes is re-examined for
   being underspecified rather than being hard.

> **In plain language.** The finished build is not marked out of ten by somebody
> forming an impression of it. It is marked by a robot that sits down and does
> thirty specific jobs with it, one after another, and counts how many actually
> worked. The score is that count divided by thirty. Nothing about how the code
> looks moves the number, and if the thing will not start up at all, the score is
> zero, whatever is in it.
>
> The thirty jobs are sorted into three levels of hardness, and there is a reason
> none of them is easy. In this kind of product, even the simplest job reaches
> out and touches a real company database that belongs to somebody else. There
> is no beginner version of that.
>
> **The middle level is one person doing one thing properly.** Connect to a
> database. Ask it a question. Put the answer on the screen in a table. Add a
> form that changes a record and watch the table update. Close the browser,
> reopen it, and find your work exactly where you left it. These are the jobs
> that decide whether this is a product at all.
>
> **The hard level adds a second person, or a race.** Somebody else is editing
> the same screen at the same time. Somebody with fewer rights presses a button
> they should not be allowed to press, and it has to be the server that says no,
> not the screen quietly hiding the button. Somebody is using the live version
> while you are changing it, and they must keep seeing the old one until you say
> otherwise. Somebody types quickly enough that four questions are in flight at
> once, and the screen must not end up showing the answer to the question they
> already changed their mind about.
>
> **The expert level adds a company and a calendar.** Somebody leaves the
> business and has to lose access straight away, not the next time they log in.
> A year later an auditor asks who looked at a particular customer record, and
> the answer has to be there and has to be impossible to have quietly edited. An
> engineer needs emergency access at three in the morning, gets it for two hours,
> and loses it again without anybody remembering to take it away. A customer asks
> to be forgotten, and being forgotten has to mean gone from the search index and
> the backups and the spreadsheet exports too, not just the main table.
>
> Half of the harder jobs are checks that something does **not** happen. That is
> deliberate. Anyone can build a thing that does what it is asked. The difficult
> and valuable part is building a thing that reliably refuses.

---

## 31. Build order

### 31.1 Sequence

| Step | Deliverable | Depends on | Unlocks |
|---|---|---|---|
| 1 | Tokens, scaling rule, theme resolution | Section 3 | everything |
| 2 | Primitives, icons, chrome | Sections 4, 5, 23.3 | the marketing surface |
| 3 | Marketing routes, static | Sections 12 to 17 | a reviewable site in week one |
| 4 | Motion and scroll wiring | Sections 6, 7 | the marketing surface, finished |
| 5 | Identity, sessions, the decision layer | Sections 18, 28.1 to 28.4 | every authenticated surface |
| 6 | Resources, credentials, the query contract | Sections 22.2, 27.4, 27.6 | M1, M2 |
| 7 | Runtime: components, bindings, query client | Sections 19.7, 20, 23.2 | M3, M4 |
| 8 | Data grid | Section 21 | M6 |
| 9 | Editor: canvas, inspector, operation log | Sections 19.2 to 19.6, 20.2 | M5, H4 |
| 10 | Versions, releases, environments | Sections 27.3, 27.5 | M9, M10, H1 |
| 11 | Groups, grants, policies, the debugger | Sections 22.3, 22.4, 28.5 to 28.7 | M8, H2, H3 |
| 12 | Audit trail and its verification | Section 29.1 to 29.4 | X2 |
| 13 | Workflows, schedules, webhooks | Sections 27.7, 27.8 | H7, H10, X8 |
| 14 | Federation, provisioning, revocation | Sections 18.2, 28.5 | X1 |
| 15 | Approvals, time-bounded grants, break-glass | Sections 28.6, 28.8 | X3, X5 |
| 16 | Quota, fair share, residency | Sections 27.9, 29.7 | X6, X9 |
| 17 | Retention, erasure, export and reimport | Sections 29.5, 29.6 | X7, X10 |
| 18 | Accessibility pass | Section 25 | |
| 19 | Performance pass against the bounds | Section 26 | |

### 31.2 Why this order

**The decision layer is step 5, before any feature that needs it.** Retrofitting
authorisation is the single most expensive mistake available in this build,
because every screen written before it exists will have grown its own rule, and
those rules are invisible until somebody audits them. Building the layer first
costs a week; retrofitting it costs the project.

**The runtime precedes the editor,** because the editor's job is to produce
something the runtime renders, and building the authoring surface first produces
an editor that can express things the runtime cannot execute.

**The operation log arrives with the canvas, not after it.** It is not a feature
that can be added to a canvas that saves documents; it is the shape of the
canvas. Step 9 delivers both or neither.

**The audit trail is step 12, before workflows and federation,** so that those
subsystems are audited from their first commit. An audit trail added to a
subsystem after the fact has gaps that nobody can enumerate.

**Steps 14 to 17 are the expert tier and they come last,** because each of them
asserts a property of the whole system rather than a feature of one screen, and
they cannot be built until there is a whole system to assert against.

### 31.3 What can be looked at, and when

| After step | What is reviewable |
|---|---|
| 3 | The complete public site, readable, with nothing moving |
| 4 | The public site as it will ship |
| 8 | A working internal tool: connect, query, table, form. The product's core claim, end to end |
| 10 | The same tool, published, with an end user running it against production |
| 12 | The governance story: who did what, provable |
| 17 | The finished article |

Step 8 is the checkpoint that matters commercially. Everything before it is
scaffolding and everything after it is trust.

> **In plain language.** What order to build it in, and what you will be able to
> look at along the way.
>
> First the sizing rule and the colours, because every other measurement is
> derived from them and leaving them until later means doing everything twice.
> Then the top bar, the bottom block, the symbols and the type, which is enough
> to judge whether the thing feels right at all. Then the whole public website,
> with nothing moving. Then the movement.
>
> **Then, before any screen that needs it, the rules about who is allowed to do
> what.** This is the single most important ordering decision in the document.
> Bolting permissions on afterwards is the most expensive mistake available here,
> because every screen written before that day will have grown its own private
> rule, and those rules are invisible until somebody audits them. Doing it first
> costs about a week. Doing it last costs the project.
>
> Then connections to databases, then the pieces that display data, then the
> table, then the building tool, then publishing and versions, then permissions
> groups, then the record-keeping, then the scheduled jobs, then the company
> login system, then approvals and temporary access, then the quotas and the data
> residency rules, then the deletion machinery.
>
> The checkpoint that matters commercially is roughly two thirds of the way
> through: connect to a database, ask it a question, show a table, add a form
> that changes a record. At that point the product's entire promise exists, end to
> end, and can be shown to somebody. Everything before it is scaffolding and
> everything after it is trust.

---

## 32. Copy deck

Every string is transcribed as measured, with brand and third-party names
substituted per Section 0.3. Typographic dashes have been normalised to hyphens;
the reference sets three em dashes in body copy and they are marked where they
occur. Curly apostrophes are reproduced as the reference sets them.

### 32.1 Global chrome

| Slot | String |
|---|---|
| Skip link | Skip to main content |
| Mobile back | Back |
| Menu 1 | Solution |
| Menu 2 | Audience |
| Menu 3 | Resources |
| Link | Use cases |
| Link | Pricing |
| Search control | Search |
| Search hint | the platform modifier plus K |
| Link | Sign in |
| Tertiary button | Book a demo |
| Primary button | Start for free |

### 32.2 Navigation groups

| Group | Members |
|---|---|
| Featured | AI app security. Ship vibe-coded apps securely |
| Platform | Build. Launch. Scale. Govern |
| Capabilities | Agents. App builder. AI primitives. Workflows. Database. External apps. Mobile apps. Self-hosting. AppGen |
| Team | Data. Engineering. Operations |
| Industry | Financial services. Manufacturing |
| Type | Enterprise. Startups |
| Discover | App gallery. Integrations. Templates. Utilities. Blog. Customer stories. Videos. Resource hub. Interactive tour |
| Developers | Documentation. Community. <BRAND> University. API reference. RPC reference. CLI reference. Hire a developer |
| Company | About. Careers. Partners. Support. Newsroom |

The App gallery entry carries the New badge of Section 11.3.

### 32.3 Home hero

| Slot | String |
|---|---|
| Headline | Secure your vibe-coded apps |
| Announcement badge | New |
| Announcement | Explore the new <BRAND> app builder for free |
| Composer placeholder, part 1 | Build an order management tool that tracks all orders from the order management |
| Composer chip | @<BRAND> Database |
| Composer placeholder, part 2 | and flags an order if it is delayed by more than 3 days. |
| Composer menu | Starter prompts |
| Import strip | Import apps built in other platforms |
| Connector strip | Build via MCP |
| Film link, muted half | See what's new. |
| Film link, bright half | Watch the film |

The composer's placeholder is also present as a single unbroken string for
assistive technology, which is the correct handling of a sentence broken into
three elements by a chip and must be reproduced.

### 32.4 Home feature block

| Slot | String |
|---|---|
| Heading | Apps that mean business |
| Link | View app gallery |
| Pillar heading | Build powerful apps from anywhere |
| Pillar 1 title | <BRAND> app builder |
| Pillar 1 badge | New |
| Pillar 1 body | Describe what you want and get a full, production-ready app with enterprise security and governance built in. |
| Pillar 1 link | Learn about the app builder |
| Pillar 2 title | MCP server |
| Pillar 2 body | Build an app from your favorite AI coding agent and deploy it here within your governed <BRAND> environment. |
| Pillar 2 link | Read the MCP server docs |
| Pillar 3 title | Import React code |
| Pillar 3 body | Deploy apps built in <PARTNER_1>, <PARTNER_2>, and other platforms. Upload a ZIP file or sync with <PARTNER_3>. |
| Pillar 3 link | Read the app import docs |
| Section 2 heading | Securely connect to your production data |
| Section 2 body | Every app you build connects directly to your production data sources. Access is governed by your existing permissions, no extra configuration required. |
| Section 2 link | See the full list of integrations |
| Section 3 heading | Ship safely, with governance built in |
| Section 3 body | Deploy with auth, access controls, and audit logging already in place. Fast to production, without sacrificing security. |
| Section 3 link | Learn about security and governance |

The body of Section 2 above contains the first of the reference's three em
dashes, between "permissions" and "no extra configuration". It is set here as a
comma, per Section 34.5.

Each pillar link is rendered in two elements so that the final word cannot wrap
away from the arrow. The break points are after "app", after "server" and after
"import" respectively, and they are art direction rather than an accident.

### 32.5 Home value and industry blocks

| Slot | String |
|---|---|
| Heading | Why enterprises choose <BRAND> |
| Column 1 title | Production-ready from day one |
| Column 1 body | Don't choose between moving fast or shipping something that'll actually pass a security review. What you build in <BRAND> is enterprise-grade from the start, no rebuild, no audit scramble, no IT veto. |
| Column 2 title | From one great app to operational excellence |
| Column 2 body | Point solutions help you build apps. You change how your business operates with <BRAND>. One platform to manage, orchestrate, and scale everything you build. |
| Column 3 title | More teams building, no new risk |
| Column 3 body | Business teams move fast, IT keeps full visibility, and governance is centralized. That's the foundation that makes app generation actually work. |
| Logo wall heading | Trusted by 10,000+ teams to generate production-ready AI applications |
| Result 1 | <CUSTOMER_1> saved $8M and 20,000+ hours |
| Result 2 | 10x reduction in dev time across 1600 studios |
| Result 3 | 10x increase in patients treated |
| Result 4 | <CUSTOMER_2> saved $6M and 36,000+ hours |
| Result 5 | $3M+ profit generated and 80% faster development |
| Result link | Read story |
| Industry 1 title | For supply chain solutions |
| Industry 1 body | The leading manufacturers and logistics companies use <BRAND> to modernize operations across warehouses, fulfillment centers, and global supply networks. |
| Industry 2 title | For financial services solutions |
| Industry 2 body | The leading banks and fintech companies use <BRAND> to modernize operations without compromising compliance. |

Column 1's body carries the second em dash, between "from the start" and "no
rebuild", set here as a comma.

### 32.6 Home closing band

| Slot | String |
|---|---|
| Heading | Start today |
| Composer placeholder | Build me a revenue dashboard that visualizes sales trends across product categories using my @<PAYMENTS_PARTNER> data |
| Newsletter heading | Get the latest from <BRAND> |
| Article 1 | Ship vibe-coded apps to production |
| Article 1 byline | By <AUTHOR_1> |
| Article 2 | What happens after AI builds your prototype? |
| Article 2 byline | By <AUTHOR_2> |
| Article 3 | 3 questions that tell you whether you're actually governing AI |
| Article 3 byline | By <AUTHOR_3> |

### 32.7 Footer

| Column | Members |
|---|---|
| Platform | Build. Launch. Scale. Govern |
| Capabilities | AI app security. AppGen. Agents. AI primitives. App builder. Mobile apps. Workflows. Database. External apps. Self-hosting |
| Audience | Data. Engineering. Operations. Financial services. Manufacturing. Enterprise. Startups |
| Resources | Use cases. App gallery. Integrations. Templates. Utilities. Blog. Customer stories. Videos. Resource hub. Documentation. <BRAND> University. Hire a developer |
| Company | About. Careers. Partners. Newsroom |
| Conversion | Start for free. Book a demo |
| Legal | Terms of use. Privacy policy. Security. Trust Center. Changelog. Status. Site map |
| Copyright | (c) <BRAND> <COPYRIGHT_YEAR> |

The footer's Capabilities column carries ten entries against the header's nine,
and orders them differently. Both are reproduced as measured; the difference is
not an error to normalise.

### 32.8 Demo route

| Slot | String |
|---|---|
| Heading | Book a <BRAND> demo |
| Body | New to <BRAND>? Schedule a 1:1 session with an expert from our team to learn more. |
| Field label | Work Email |
| Field label | Reason for demo |
| Select placeholder | Select reason |
| Option 1 | Explore <BRAND> Enterprise |
| Option 2 | Explore a <BRAND> Use Case |
| Option 3 | Professional Services |
| Submit | Book a demo |
| Consent, part 1 | By submitting this form, you agree to our |
| Consent, link | privacy policy |
| Consent, part 2 | and consent to receiving marketing communications from <BRAND>. |
| Proof 1 | Develops 50x faster with <BRAND> |
| Proof 2 | Saved $8M and increased efficiency by 20% |
| Proof 3 | Over 10,000 companies from startups to the Fortune 500 use <BRAND> to run their business. |
| Return control | Return to form |

### 32.9 Not-found route

| Slot | String |
|---|---|
| Message | The page "/404" wasn't found... Let's find a better place. |
| Action | Go to homepage |
| Game title | <GAME_TITLE> |
| Readout | Level: 1 |
| Readout | Match: 5 |
| Readout | Score: 0 |
| Control | Restart, bound to r |
| Control | Move Left, bound to the left arrow |
| Control | Move Right, bound to the right arrow |
| Control | Drop, bound to the down arrow |
| Control | Rotate, bound to the up arrow |

The message interpolates the path that was requested, which is why the captured
instance names `/404` itself. **Capability requirement - normative.** The
interpolated path is escaped as text. A not-found page that reflects an
unescaped path is a cross-site scripting vector, and it is the most commonly
shipped one on the entire web.

### 32.10 Document titles and descriptions

| Route | Title | Description |
|---|---|---|
| Home | Build internal software better, with AI. | <BRAND> | none captured |
| Pillar | Automate and speed up business processes with AI | <BRAND> | With <BRAND> AI, build bespoke AI-powered tools for your business |
| Blog | Cache | <BRAND> Blog | none captured |
| Demo | Book a Demo - <BRAND> | <BRAND> | New to <BRAND>? Schedule a 1:1 session with an expert from our team to learn more. |
| Not found | none | none |

The not-found route ships an empty title, which is a defect in the reference and
is not reproduced. **Capability requirement - normative.** Every route has a
unique, specific title, leading with the page and ending with the product.

> **In plain language.** Every word on the public site, written out so it can be
> handed to whoever is writing or translating it.
>
> A few notes on it. Wherever the product's name appeared, we have put a
> placeholder instead, and the same for the six customer companies, the three
> writers and the other products named in passing. The reference used three long
> dashes in its writing and we have turned them into commas, because a long dash
> pasted into build tooling causes real trouble later and nobody ever notices it
> was changed.
>
> Two things in here are instructions rather than words. The links that end in an
> arrow are deliberately split so the last word cannot end up alone on a new line
> away from its arrow. And the page that says "we could not find that page"
> repeats back the address you asked for, which means the address has to be
> treated as plain text rather than as instructions. Getting that wrong is the
> single most commonly shipped security hole on the entire web, and it is one
> line of code to get right.

---

## 33. Zero-asset substitution guide

Every recipe below replaces a binary the reference shipped. Nothing in this
build downloads a file the reference served.

<!-- lint:allow P4,P6 -->

### 33.1 What is being replaced

| Class | Count in the capture | Weight |
|---|---|---|
| Typeface files, woff2 | 223 | 11958634 bytes |
| Video, mp4 | 4 | 19171924 bytes |
| Raster imagery, webp | 297 | 10661520 bytes |
| Raster icons and marks, png | 63 | 41889 bytes |
| Animated marks, gif | 1277 | 51197 bytes |
| Vector, svg | 175 | 7284 bytes |

The three columns are the argument for this section. The reference ships roughly
forty-two megabytes of binary across those six classes, and this build ships
none of it.

### 33.2 The named binaries

| File | Class | Replaced by |
|---|---|---|
| variable grotesque, woff2 | typeface | Section 33.4 |
| fixed grotesque regular and bold, woff2 | typeface | Section 33.4 |
| hero teaser video, mp4 | video | Section 33.6 |
| hero poster, webp | image | Section 33.6 |
| five external-import marks, png | icon | Section 33.5 |
| five connector marks, png | icon | Section 33.5 |

<!-- lint:end -->

### 33.3 Icons

Already solved. Every icon in Section 4 is given as coordinates and is drawn
inline. No icon file ships.

### 33.4 Typefaces

**Capability requirement - normative.** The build ships no licensed typeface.
The requirement is the shape, not the name:

| Role | Requirement | Fallback stack |
|---|---|---|
| Display and interface | A grotesque with a variable weight axis reaching at least `100` and at least `700`, with the fractional weights `380` and `570` reachable | a variable open grotesque, then `ui-sans-serif`, `system-ui`, `sans-serif` |
| Body | The same family at `300` and `400` | as above |
| Serif accents | A transitional serif at `400` and `500` with true italics | an open transitional serif, then `Georgia`, `serif` |
| Monospace | Any | `ui-monospace`, `SFMono-Regular`, `Menlo`, `Monaco`, `Consolas`, `monospace` |

The variable axis is not optional. Section 3.4's weights of `380` and `570` are
unreachable on a static family, and rounding them to `400` and `600` visibly
changes the interface. If no open variable grotesque is available to the build,
round to the nearest available weight and record it as a deviation rather than
silently substituting.

Subsetting is required, the first-render faces are preloaded, and the fallback
is metrically adjusted so that the swap does not move the layout, per
Section 26.3.

### 33.5 Customer marks and connector icons

**Capability requirement - normative.** Every third-party mark is redrawn as
inline geometry in the pixel vocabulary of Section 4, as a monochrome silhouette
on the pale tile of Section 9.4. No mark reproduces a real trademark: the six
customers are `<CUSTOMER_1>` to `<CUSTOMER_6>` and the five partners are
`<PARTNER_1>` to `<PARTNER_5>`, and their marks are invented.

Recipe: for each placeholder name, draw a mark on a `0 0 24 24` grid from
between six and fourteen unit squares, using the same staircase and block
vocabulary as Section 4.6. Vary the density between marks so the wall does not
read as one repeated shape. Fill is `--surface-background-base`, `#151515`, on
the tile.

### 33.6 The hero video and its poster

**Capability requirement - normative.** The build ships no video file. The hero
frame is filled by a generated animation:

| Layer | Recipe |
|---|---|
| Ground | The vertical scrim of Section 7.6, at its measured nineteen stops |
| Field | Two radial gradients at the lower corners, reproducing the measured `radial-gradient(80% 50% at 0% 100%, color(srgb 0.176471 0.298039 0.443137 / 0.75) 0%, rgba(0, 0, 0, 0) 100%)` and its warm counterpart at the trailing corner |
| Motion | A slow drift of both radial centres, at a period no shorter than the gradient border's `18000ms`, so it reads as light rather than as animation |
| Grain | The tiling noise of Section 33.8 at low opacity |
| Poster | The first frame of the above, rendered once |

The reference's video shows a product screenshot behind a chart. Do not
reconstruct it. A generated field of slow coloured light in the measured palette
is closer to the intended effect than a poor imitation of an interface, and it
carries none of the risk of shipping a screenshot of somebody else's product.

### 33.7 Wide-gamut gradients

The announcement badge of Section 11.3 and the hero field are authored in a wide
colour space. **Capability requirement - normative.** Author in the wide space
with an explicit fallback in the narrower one, declared in that order, so that
a display capable of the wide gamut gets it and one that is not gets a defined
result rather than a browser-chosen approximation.

### 33.8 Grain

A tiling noise texture as an inline vector filter serialised to a data URI:
turbulence at a base frequency around `0.9` for fine grain at three hundred
pixels, four octaves for tonal variation, and a colour matrix at zero saturation
to remove the colour speckle. Applied at low opacity over the hero field.

### 33.9 Article and category illustrations

Canvas-generated placeholders keyed by a seed derived from the article's slug,
composed from two accent ramps of Section 3.3 so that the grid of cards reads as
one family. Dimensions are declared in the markup so that no layout shift occurs
when they render.

> **In plain language.** The reference site downloads about forty-two megabytes
> of files: fonts, videos, pictures and logos. This build ships none of them, and
> this section says what to make instead.
>
> Symbols are already solved: they are drawn from coordinates written out earlier
> in this document.
>
> Fonts are the one place to be careful. The reference uses typefaces that have
> to be paid for. What actually matters is not their names but one property: the
> interface uses two in-between weights that only exist on a font with a
> continuous weight dial. Substituting a font that only comes in regular and bold
> and rounding to the nearest is a visible change, so if that has to happen it
> gets written down as a known deviation rather than quietly done.
>
> The video at the top is replaced by a generated one: a slow drift of coloured
> light in the site's own palette, with a very fine grain over it. That is
> deliberate rather than lazy. The original video shows a screenshot of the
> product, and a mediocre imitation of somebody's interface looks far worse than
> an abstract field of light, as well as being somebody else's screenshot.
>
> Customer logos are invented, drawn in the same little-squares style as the rest
> of the symbols, as flat silhouettes. They are placeholders, they are not
> anybody's real trademark, and each is drawn with a slightly different density so
> the wall does not look like the same shape repeated six times.

---

## 34. Evidence gaps and substitutions

### 34.1 What this section is

The honest boundary of the document. Everything below either could not be
measured or was substituted, and a reviewer should read this section before
trusting any specification that depends on it.

### 34.2 The authenticated product could not be captured

**The largest gap by a wide margin.** The reference's product surface is behind a
sign-in. The capture reached the marketing site only.

| Section | Status |
|---|---|
| Sections 3 to 17 | measured |
| Sections 18 to 22 | normative specification, informed by product imagery on the public routes; not measured |
| Sections 23 to 26 | normative, part measured: the responsive and motion evidence is from the public surface, the product bounds are specified |
| Sections 27 to 29 | normative specification; nothing measured |
| Section 30 | authored against this document, not measured |

This is not a defect in the capture. It is the correct boundary: authoring a
product specification from imagery would produce invention dressed as evidence,
and the pipeline exists to prevent exactly that. What Sections 18 to 29 are is a
specification of what such a product must do to be correct, and they should be
read as requirements rather than as a description of the reference.

### 34.3 Route coverage is thin

Route discovery reached twelve addresses. Five carried distinct page types; the
other seven resolved to the not-found route.

The discovery method is a crawl of the rendered links plus a scan of the
bundles for path-shaped strings, and the scan's results are ordered by path
length. The reference's real routes are mostly longer than the analytics and
system paths that the scan also finds, so the shorter junk paths displaced them.
Section 2.2 lists the forty-one destinations the navigation names, taken from the
copy deck rather than from a capture, and they are specified as required routes
without layouts.

**What this costs the document:** the pricing route, the customer stories, the
app gallery, the templates index and the four platform pillars beyond the
captured one are specified as templates rather than as pages. Their design
system, chrome, motion and grid are fully measured, because those are global.
Their content and band order are not.

### 34.4 Hover evidence is thin

The hover pass compares a narrow property set on a narrow candidate set, and it
returned two treatments per route across every captured route. The site's real
hover work is transform-based and does not appear.

The link wipe of Section 6.5 is therefore **reconstructed** from the keyframe
definitions and the declared transitions rather than observed in a before-and-
after diff. The keyframes are measured and exact; that they fire on hover is
inferred. Expect this to need one round of adjustment against a running build.

### 34.5 Typographic normalisations

The reference sets three em dashes in body copy, at the points marked in
Sections 32.4 and 32.5. They are set as commas in this document. The reference's
curly apostrophes are reproduced as found.

### 34.6 Taxonomy substitutions

The task order names three closed-enum members, and two of them are
substitutions:

| Level | Value | Why |
|---|---|---|
| Category | `enterprise` | Exact. Internal tools with roles and row-level security is the category's definition |
| Domain | `data-analytics-bi` | **Substituted.** The product is horizontal and has no vertical of its own. The nearest legal member is the internal-data-tooling vertical; the enum has no member for a platform that spans all of them |
| Pattern | `admin-console` | **Substituted, mildly.** The product is a builder of admin consoles rather than an admin console. The pattern is exact for the product's own governance surface of Section 22.3 and for the apps it produces, and inexact for the builder itself |

### 34.7 Values that are samples rather than definitions

Three sets of numbers in this document are outputs of a rule, not the rule:

| Section | Values | The rule |
|---|---|---|
| Section 7.4 | the fractional blur and opacity values | a continuous scroll-driven ramp |
| Section 7.5 | `-7.5px`, `-232.5px`, `-532.5px` | one mask evaluated at three element widths |
| Section 7.7 | `27.0833px`, `14.4231px` | the thirty-six column grid at two viewport widths |

Hard-coding any of them reproduces one instance and breaks every other.

### 34.8 Things the reference does that this document declines to reproduce

| Behaviour | Why not |
|---|---|
| An empty document title on the not-found route | a defect, per Section 32.10 |
| Fourteen thousand declarations of `transition: all` | it transitions properties that should not be transitioned and defeats the property groups of Section 6.2 |
| Analytics and marketing paths in the bundle | out of scope, and Section 27.11 states the consent requirement instead |

The middle row is worth a sentence. The reference declares a transition on every
property more than fourteen thousand times, which is a framework default rather
than a design decision, and reproducing it would transition layout properties
during resize and produce visible lag on the grid of Section 3.1.

### 34.9 Substituted names

Fifteen placeholder tokens, listed in Section 0.3. Every real name in the
capture was replaced: the product, six customers, three article authors, five
partner products and one payment provider. No real trademark is reproduced, and
Section 33.5 requires the marks to be redrawn rather than traced.

> **In plain language.** What we could not find out, and what we changed.
>
> **The big one: we could not get inside the product.** You need an account, and
> the capture only ever saw the public website. So everything in this document
> about the app builder, the permissions system and the record-keeping is a
> specification of what it has to do, not a description of what the original
> does. It is honest work and it is the right way round, because the alternative
> is guessing what is behind the sign-in and presenting the guess as fact. Read
> those sections as requirements.
>
> **We reached far fewer pages than the menus promise.** The tool that found
> pages to photograph got twelve addresses, five of which were real pages and
> seven of which turned out to be nothing. The menus name about forty
> destinations. All the global things, the colours, the type, the grid, the
> motion, the bar at the top and the block at the bottom, are fully measured
> because they are the same on every page. What is missing is the specific
> content and running order of pages like pricing and customer stories.
>
> **The link underline is our best reconstruction, not an observation.** The
> exact recipe for it is measured and precise; that it is triggered by hovering
> is our reading of it. Expect to adjust it once you can see it running.
>
> **Numbers that look oddly precise are usually samples.** Several values in this
> document, like a blur of just under five pixels, are one frame of something
> continuous rather than a setting to type in. Where that is true it says so, and
> typing the number in instead of building the rule produces something that is
> correct in one place and wrong everywhere else.
>
> **Every real name has been replaced.** The product, six customer companies,
> three writers and six other products. The logos are to be redrawn as invented
> shapes rather than traced from the originals.

---

## 35. Acceptance checklist

### 35.1 Gate order

A build is accepted when every line below is true. The order is the order to
check them in, because a failure high in the list makes the ones beneath it
meaningless.

| # | Assertion | Evidence |
|---|---|---|
| 1 | The application deploys and serves every declared route | a deploy that does not come up scores zero regardless of contents |
| 2 | No credential, token or key appears in any client payload, bundle, log or error | workflow H6, run across every other workflow |
| 3 | Every mutating endpoint refuses an unauthorised principal at the server | workflow H2, driven at the API |
| 4 | Empty results and refusals are distinguishable end to end | workflows H3, M7 |
| 5 | The default decision, at every scope and action, is deny | Section 28.3 |
| 6 | Explicit deny cannot be overcome by any allow | Section 28.3 |
| 7 | Grid paging, sorting, filtering and search are executed by the resource | workflow M6, asserted on the network |
| 8 | Money is held and computed in integer minor units | Section 21.4 |
| 9 | Undo is a command stack and survives reload | workflow H4 |
| 10 | Concurrent saves conflict rather than overwrite | workflow H8 |
| 11 | A published release is immutable and rollback is a promotion | workflow H1 |
| 12 | Every mutating cross-boundary call carries a derived idempotency key | Section 27.8 |
| 13 | Webhooks verify signature before parse and are idempotent per delivery | workflow H7 |
| 14 | Authorisation is re-decided within the stated bound after a grant change | workflow X1 |
| 15 | The audit trail is append-only, hash-chained and independently verifiable | workflow X2 |
| 16 | Audit events commit on the transaction of the effect they record | Section 29.3 |
| 17 | Column masks hold in the app, the raw result, the export and scheduled output | workflow X4 |
| 18 | Time-bounded grants expire at decision time, not by a sweeper | Section 28.6 |
| 19 | Promotion approvals are bound to a content hash and forbid self-approval | workflow X5 |
| 20 | One organisation's load does not degrade another's | workflow X6 |
| 21 | Erasure covers every enumerated store and preserves the audit event | workflow X7 |
| 22 | No cross-organisation read occurs in any background job | workflow X9 |
| 23 | Every canvas operation has a keyboard path, and the tree is its accessible peer | Section 25.3 |
| 24 | Reduced motion removes every scroll-driven and entrance animation | Section 25.4 |
| 25 | Every performance bound holds under the reference conditions | Section 26.2 |
| 26 | No personal data appears in any log line | Section 29.8 |
| 27 | The build contains no binary asset from the reference | Section 33 |
| 28 | Every placeholder token has been replaced | Section 0.3 |

### 35.2 What is not on this list

Visual fidelity to the reference is reviewed and is advisory. It does not move
the score. A build that reproduces every measurement in Sections 3 to 17 and
fails line 3 has shipped a data breach with excellent typography.

> **In plain language.** The list to check before calling this finished, in the
> order to check it.
>
> The order is not arbitrary. If the thing will not start up, nothing below that
> line means anything. If passwords to customer databases are leaking, nothing
> below that line means anything either. So the list runs from the failures that
> make everything else irrelevant down to the ones that are merely bad.
>
> Roughly half the list is checking that something does **not** happen: a
> password does not appear anywhere, an unauthorised person is refused by the
> server and not merely by a hidden button, one customer's load does not slow
> another customer down, a background job does not quietly read across company
> boundaries. That balance is deliberate. Building something that does what it is
> asked is the easy half. Building something that reliably refuses is the half
> that is worth paying for.
>
> One line at the bottom is worth reading twice: **how closely it resembles the
> reference site does not move the score.** It is reviewed, it is commented on,
> and it counts for nothing. A build that reproduces every measurement in this
> document perfectly and fails the third line has shipped a data breach with
> excellent typography.

---
