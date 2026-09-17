# <BRAND> buildable product requirements

Zero-asset build specification. Sections 0 to 19 were authored from an evidence
ledger produced by a deterministic capture of a reference site: every colour,
easing curve, duration, radius, breakpoint and icon coordinate in them was
measured, and nothing was recalled. Sections 20 to 30 are a specified extension,
the retrieval service the reference site sells, written out as a buildable
contract with a conformance suite, and they are marked as authored rather than
measured wherever they appear.

Every section also carries a plain-language block, marked **In plain
language.**, saying the same thing to a reader who will never open a code
editor.

---

## 0. How to use this document

### 0.1 What this is

A specification complete enough to rebuild a marketing site and the product it
advertises, without receiving a single binary file. No image, video, font file
or vector file ships with it. Section 33 gives a procedural recipe for every
asset class the reference used.

The document has two readers and carries a register for each. The specification
is written for the agent building the work and is exact enough to rebuild from.
The blockquote that closes every section is written for the person who
commissioned it, in terms that can be checked against a live page rather than
against a ledger. Neither is a summary of the other, and they cannot drift,
because they sit in the same section.

### 0.2 Normative versus informational

Every statement about technology sits in exactly one register, and this document
labels which:

- **Capability requirement - normative.** What the build must do, stated without
  naming a library.
- **Observed implementation - informational.** What the captured reference used,
  with the ledger tier that established it. Evidence, never instruction.

Where a block carries no label, it is normative.

There is a third label, used only in Sections 16 and 20 to 30:

- **Specified extension - normative, not measured.** A requirement authored for
  this build, describing something the reference site sells rather than
  something the reference site is. It is as binding as anything else in the
  document and it is not evidence of anything. Section 35.4 lists every one.

### 0.3 Placeholder tokens

Angle-bracket names are blanks. Replace every occurrence before shipping.

| Token | Meaning | Literal placeholder used in copy |
|---|---|---|
| `<BRAND>` | product and company name | `Kestrel`, 7 characters, matching the reference |
| `<AGENT_PRODUCT>` | the agent-building product named in the promotion bar | `Agent Forge` |
| `<ASSIST_PRODUCT>` | the conversational assistant inside site search | `Kestrel Assist` |
| `<EVENT_NAME>` | the developer conference in the promotion bar | `BuildCon` |
| `<SITE_ORIGIN>` | public origin of the site | none |
| `<APP_HOST>` | origin of the signed-in console | none |
| `<DOCS_HOST>` | origin of the documentation site | none |
| `<ASSET_HOST>` | origin images and media are served from | none |
| `<SEARCH_APP_ID>` | the site's own search application identifier | none |
| `<SEARCH_API_KEY>` | the site's own search-only key | none |
| `<FORM_ENDPOINT>` | demo request form target | none |
| `<NEWSLETTER_ENDPOINT>` | newsletter form target | none |
| `<ANALYTICS_ID>` | product analytics identifier | none |
| `<TAG_MANAGER_ID>` | tag manager container identifier | none |
| `<CHAT_ORG_ID>` | third-party support chat organization identifier | none |
| `<CONSENT_ID>` | consent management identifier | none |
| `<STATUS_URL>` | service status page | none |
| `<SOCIAL_X_URL>` | short-form social profile | none |
| `<SOCIAL_LINKEDIN_URL>` | professional network profile | none |
| `<SOCIAL_VIDEO_URL>` | video channel | none |
| `<SOCIAL_PHOTO_URL>` | photo network profile | none |
| `<SOCIAL_BLUE_URL>` | second short-form social profile | none |
| `<SOCIAL_FB_URL>` | social network profile | none |

Further literal placeholders, chosen at similar character counts because the
reference line lengths were art-directed around the originals:

| Class | Placeholders used in the copy deck (Section 34) |
|---|---|
| Customer logos, retail | `Northmoor`, `Culture Yard`, `Halcyon Sport`, `Fern & Co`, `Petsmith`, `Shoe Carousel` |
| Customer logos, other | `Club Meridian`, `DocMarket`, `Givewell Schools`, `Brightwell Group` |
| Analyst firms and reports | `Northgate Research`, `Marchant Group`, `Halden Analytics` |
| Integration partners | `Storefront Cloud`, `Commerce Tools Suite`, `Content Manager`, `Data Platform` |
| Named plans | `Free`, `Grow`, `Grow Plus`, `Elevate`, all four kept because they are generic |

### 0.4 Reading the numbers

Numbers are quoted as measured and must not be rounded.
`cubic-bezier(.05,0,0,1)` is not "a custom ease"; `12.992px` is not "about 13
pixels". Where the reference's rendered type scale is fractional it is because
the value is derived at runtime, and reproducing the rule reproduces the
fraction. Hard-coding the fraction does not reproduce the rule.

### 0.5 The two halves, and why the second one exists

Sections 0 to 19 describe a site. Sections 20 to 30 describe a search and
retrieval service, a console to operate it, and an exam that decides whether it
was built correctly. Section 20.1 explains why the second half is here at all,
and Section 29 explains what it is defending against.

The short version: the site's entire argument is retrieval quality, and
retrieval quality cannot be demonstrated by a picture of a search box. A build
that ships the pages and stubs the engine has shipped a brochure for a product
that does not exist.

### 0.6 What could not be measured

Section 35 lists the evidence gaps. Anything marked **inferred** is a
reconstruction from screenshots, not a measurement. Anything marked **specified
extension** was authored, not measured. Both should be expected to need
adjustment.

> **In plain language.** This build is described twice over, section by section.
> Once in exact terms for the machine that will build it: long tables of
> coordinates, exact timings, exact colours, every number measured off the
> reference site by a program rather than remembered by a person, because
> rounding any of them would produce a different result. And once like this, for
> you, saying the same things in terms you can check by looking at the finished
> thing.
>
> **Anything written in angle brackets is a blank.** `<BRAND>` is where the
> product's name goes. There are about twenty of them, all listed in the
> specification for this section. We have also used stand-in names wherever the
> reference used real ones: invented customers, invented research firms, an
> invented conference. Those are placeholders too, chosen to be roughly the same
> length as the originals, because the layouts were designed around how long the
> real words are.
>
> **What this is, in one sentence a friend would understand:** it is the shop
> window for a company that sells instant, forgiving search to other companies,
> and, unusually, this document also specifies the search itself, so that the
> shop window has something real behind it.
>
> That second half is the unusual part, so here is why it is there. Everything
> the front page claims is about finding the right thing instantly, even when you
> spell it wrong, even when you ask in a full sentence. You cannot show that with
> a picture. So from the twentieth section onward the document stops describing
> pages and starts describing the machine: how things get filed, how they get
> found, how they get ordered, and, in one long section near the end, the thirty
> places where this kind of machine is most often built wrong and nobody notices
> for months.
>
> One more thing worth knowing before you read on. A few things could not be
> measured and had to be reconstructed from screenshots, and a large part is
> written rather than measured. Every one of them is listed near the end. Expect
> those to need a round of adjustment once you can see them running.

---

## 1. Product overview

### 1.1 What the product is

A marketing site for a search and retrieval platform sold to businesses, and,
behind it, the platform itself.

The site's job is to convert three kinds of visitor into one of four actions
inside a single scroll. It does that by demonstrating the product on itself:
the header carries a working search over the company's own documentation,
support articles, blog and customer stories, and that search is the same class
of thing the company sells. The site is its own best demonstration, which is
also why a stubbed search is a worse failure here than it would be on most sites.

### 1.2 Audiences

| Audience | What they came for | Where the site serves them |
|---|---|---|
| Engineers | "Can I integrate this, and what does it cost per request?" | Header search over documentation, the pricing route, the developers entry in the header |
| Commerce and merchandising leads | "Will this lift conversion, and can my team control results without a developer?" | Home route capability panel, customer stories, the demo request route |
| Executives and analysts | "Is this a credible vendor?" | The analyst recognition band on the home route, the customer logo walls |
| Existing customers | Documentation, support, the console | Header search, the top utility bar, the login entry |

### 1.3 Primary actions

1. Start free, the primary call to action, repeated in the header on every route
   and at the foot of every route.
2. Request a demonstration, the secondary call to action, which is the one that
   touches state and is specified in Section 13.
3. Search the site, which is available from the header on every route and is
   the product demonstration.
4. Subscribe to the newsletter, in the footer of every route.

### 1.4 Character

Two-register, and the register flips with the section. Dark sections are near
black with a blue cast, `#000033` at the deepest, and carry the display type in
white. Light sections are `#ffffff` and `#f3f3f3` with ink at `#23263b`. The
page alternates between them rather than gradating, so the boundary between two
sections is a hard horizontal edge across the full width.

One accent does nearly all the work: a saturated electric blue, `#003dff`, used
for primary buttons, links, eyebrow labels and every hover state. A second,
lighter blue `#457aff` appears in gradients and in the hover fill of secondary
buttons. Everything else is neutral.

Type is two families with a strict division of labour: a geometric display face
for headings, set as large as `76px` at desktop, and a neutral grotesque for
everything else, sat overwhelmingly at `16px` with a `24px` line. The contrast
between the two sizes is the page's entire typographic argument.

Motion is incidental rather than continuous. The reference is not a scrubbed
scroll experience: the ledger shows almost no scroll-driven property changes
(Section 7.1). What moves does so on a timer or on hover, and the two things
that move on their own, the promotion bar and the statistics column, both loop.

### 1.5 Success criteria

- The header search returns real results from a real index, with counts, facets
  and highlighting, and is the same engine specified in Sections 21 to 25.
- Every route reads as one continuous document at all three widths, with the
  hard light and dark boundaries landing on section edges.
- The conformance suite in Section 30 passes in full.
- Nothing in the build depends on a binary file (Section 33).

> **In plain language.** The site has one job and does it in an unusual way: it
> sells search by making you use its own.
>
> The box at the top of every page is not decoration. Type into it and you are
> using the thing the company sells, on the company's own material: their
> documentation, their support articles, their writing, their customers' stories.
> Counts appear beside each of those groups. You can narrow to one. You can ask a
> question in a sentence instead of typing keywords. That is the sales pitch, and
> it is the reason a fake search box here would be worse than a fake search box
> anywhere else.
>
> Four kinds of visitor arrive and each is served in a different stretch:
>
> | Who | What they want | Where they get it |
> |---|---|---|
> | An engineer | "Can I plug this in, and what will it cost?" | The search box over the documentation, and the pricing page |
> | Someone running an online shop | "Will this sell more, and can my team steer it without a developer?" | The home page panel and the customer stories |
> | An executive | "Is this a real company?" | The awards band and the wall of customer logos |
> | An existing customer | Documentation, support, their account | The small links along the very top |
>
> The look is two-tone and switches abruptly. Some bands are near-black with a
> blue tint, some are white or pale grey, and the join between them is a straight
> line across the page rather than a fade. One electric blue does nearly all the
> remaining work: every button, every link, every hover.
>
> Two things move on their own and nothing else does. The announcement strip at
> the very top cycles through messages, and a column of statistics on one page
> scrolls slowly forever. This is not a site where things fly in as you scroll,
> and building it that way would be a different site.

---

## 2. Information architecture

### 2.1 Routes

Six routes were captured. The reference site is larger than six routes; what was
captured is what this document specifies, and Section 35.1 records the boundary.

| Route | Path | Shell | Purpose |
|---|---|---|---|
| Home | `/` | full chrome | the argument, end to end |
| Pricing | `/pricing` | full chrome | four plans, then a full comparison grid |
| Products | `/products` | full chrome | the platform overview, longest route on the site |
| Customers | `/customers` | full chrome | a searchable, faceted index of customer stories |
| Demo request | `/demorequest` | **no chrome** | a single form, with proof beside it |
| Not found | any unmatched path | **no chrome** | the error route, with a search box |

The demo request and not-found routes carry no header, no promotion bar and no
footer. That is measured, not a simplification: both were captured with the
chrome absent, and it is a deliberate choice on both, for opposite reasons. The
form route removes every exit; the error route removes everything except the way
out.

Measured page heights at 1440 pixels wide, from the scroll matrix:

| Route | Scrollable height | Screens |
|---|---|---|
| Home | 3910 pixels past the fold | about 5 |
| Pricing | 3450 pixels past the fold | about 4 |
| Products | 7939 pixels past the fold | about 9 |
| Customers | 2332 pixels past the fold | about 3 |
| Demo request | 144 pixels past the fold | 1, effectively fixed |
| Not found | 0 | 1, exactly one screen |

### 2.2 Navigation model

The header carries five primary destinations. Four of them open a panel rather
than navigating; one is a direct link.

| Item | Behaviour |
|---|---|
| Products | opens a panel |
| Solutions | opens a panel |
| Pricing | navigates to `/pricing` |
| Developers | opens a panel |
| Resources | opens a panel |

Above them, a utility bar carries Company, Partners, Support, Login and a
language selector offering English, German, French, Brazilian Portuguese,
Spanish and Italian. The language selector is a real localisation system: a
German rendering of the home route was reached during capture at a locale path
and is recorded in Section 35.1.

To the right of the primary items sit, in order: the search field, a secondary
button, and the primary button.

### 2.3 The promotion bar

Above the utility bar, a full-width strip cycles through announcements. Two were
captured:

| Label | Message | Action |
|---|---|---|
| `Join us:` | `<BRAND> <EVENT_NAME> 2026: Oct 1, 2026 - VIRTUAL` | `Register Now` |
| `UPDATE:` | `Unlock the power of agentic AI with <AGENT_PRODUCT>` | `See what's new` |

The transition between them is measured and specified in Section 6.4.

### 2.4 Page-type attribute

Every route carries a page type on the root element, which the chrome reads to
decide its own presence and colour scheme:

| Value | Routes | Chrome | Header on load |
|---|---|---|---|
| `marketing` | Home, Products | yes | dark, transparent over a dark hero |
| `commercial` | Pricing | yes | dark |
| `index` | Customers | yes | light |
| `capture` | Demo request | no | none |
| `error` | Not found | no | none |

The Customers route is the only captured route whose header is light on load,
because its own body begins light. The header colour is therefore a property of
the route, not a scroll state.

### 2.5 Cross-route surfaces

Three surfaces appear on every route with chrome and are specified once:

| Surface | Specified in |
|---|---|
| Header, promotion bar, panels, mobile drawer | Section 5 |
| Site search overlay | Section 8 |
| Footer, newsletter, legal bar | Section 5.7 |

> **In plain language.** Six pages, and they are not all built the same way.
>
> Four of them are ordinary pages with the full furniture: the announcement strip
> along the very top, the row of small links, the main navigation, and the footer.
> The home page, the pricing page, the products page and the customer stories
> page all work like that.
>
> Two of them deliberately have none of it. The page where you ask for a
> demonstration has no navigation at all, because anything you could click on is
> a way to leave without asking. And the page you land on when an address is
> wrong has nothing either, except a search box and three ways home. Same
> decision, opposite reasons: one removes the exits, the other is nothing but an
> exit.
>
> The pages are very different lengths, and that is worth knowing before you
> build them. The products page is about nine screens tall. The customer stories
> page is about three. The demonstration request page does not really scroll at
> all.
>
> Four of the five items in the main navigation do not take you anywhere when you
> click them: they open a panel underneath. Only pricing is a plain link. And the
> whole site exists in six languages, which is a real system rather than a flag
> in the corner.

---
## 3. Design system

### 3.1 Scaling and the layout grid

The reference does not scale its root size with the viewport. Body text sits at
`16px` with a `24px` line at every width measured, and layout responds through
breakpoints alone. This is the opposite of a fluid-typography site and it is
measured, not assumed: the rendered type scale in Section 3.3 shows one
overwhelming size and no fractional family of it.

Breakpoints actually present in the stylesheets, by frequency:

| Minimum width | Declarations | Role |
|---|---|---|
| `1200px` | 69 | the widest layout change, the primary desktop grid |
| `1024px` | 63 | the main desktop threshold, where the header stops collapsing |
| `768px` | 52 | tablet |
| `960px` | 52 | a second tablet threshold used by older components |
| `1536px` | 32 | the maximum content width band |
| `375px` | 24 | small-phone adjustments |
| `500px` | 24 | large-phone adjustments |
| `1440px` | 24 | the capture width |
| `1920px` | 16 | very wide screens |

Two maximum-width queries also carry real weight: `max-width: 960px` with 45
declarations and `max-width: 1023px` with 30. The system is therefore not
mobile-first throughout; two component families were written desktop-first, and
a build that converts everything to one direction will change behaviour between
`960px` and `1023px`, which is exactly the tablet capture width of `990px`.

Content is centred with a maximum measure and gutters. At `1440px` the header's
content spans from `56px` to `1376px`, giving a `56px` gutter and a `1320px`
content width.

### 3.2 Colour tokens

Measured. Every value here appears in the ledger with a source file and line.
Third-party embedded surfaces contribute a further palette that is deliberately
excluded, and Section 35.2 lists what was excluded and why.

**Brand**

| Token | Value | Uses | Role |
|---|---|---|---|
| `--brand` | `#003dff` | 192 | primary button fill, link colour, every hover target |
| `--brand-alt` | `#013dff` | - | the same blue at a second declaration site |
| `--brand-mid` | `#356cff` | - | gradient midpoint |
| `--brand-light` | `#457aff` | 84 | secondary button fill, gradient start |
| `--brand-deep` | `#1e59ff` | - | gradient end |
| `--brand-press` | `#2142e7` | - | pressed state |
| `--brand-pale` | `#bfdbfe` | - | selected-row tint on light surfaces |

**Dark surfaces**

| Token | Value | Uses | Role |
|---|---|---|---|
| `--navy-900` | `#000033` | 94 | the deepest ground, hero and footer |
| `--navy-800` | `#001639` | - | second dark ground |
| `--navy-700` | `#1a1a2e` | 90 | dark card fill |
| `--ink` | `#23263b` | 76 | body text on light, and the darkest text colour |

**Light surfaces**

| Token | Value | Uses | Role |
|---|---|---|---|
| `--white` | `#ffffff` | 1190 | the dominant surface |
| `--surface-1` | `#f9f9f9` | - | the palest band |
| `--surface-2` | `#f3f3f3` | 160 | the alternating light band |
| `--surface-3` | `#f3f4f6` | 58 | card fill on a light band |
| `--line` | `#e5e5e5` | 156 | hairline rules |
| `--line-cool` | `#e5e7eb` | 143 | the same rule in the cooler grey ramp |

**Neutral text and structure**

| Token | Value | Uses | Role |
|---|---|---|---|
| `--muted` | `#484c7a` | 103 | secondary text on light, the site's signature grey |
| `--muted-2` | `#585f9d` | - | a lighter step of the same |
| `--muted-3` | `#9698c3` | - | placeholder text |
| `--lilac` | `#d6d6e7` | 87 | dividers and borders on dark |
| `--grey-100` | `#f3f4f6` | 58 | - |
| `--grey-300` | `#d1d5db` | 69 | - |
| `--grey-400` | `#c9c9c9` | 131 | - |
| `--grey-500` | `#9ca3af` | 62 | - |
| `--grey-600` | `#939393` | 60 | - |
| `--grey-700` | `#747474` | - | - |
| `--grey-800` | `#6b7280` | 60 | - |
| `--grey-850` | `#4b5563` | - | - |
| `--grey-900` | `#374151` | - | - |
| `--grey-950` | `#111827` | 109 | - |
| `--near-black` | `#181818` | 68 | - |
| `--black` | `#000000` | 156 | - |
| `--accent-green` | `#00a648` | - | one gradient only, Section 3.9 |

**Overlay tints.** Four eight-digit values, all the same hue at four alpha
steps, used for scrims and hover fills over light surfaces:

| Value | Uses |
|---|---|
| `#11182708` | 103 |
| `#1118270a` | - |
| `#1118270f` | - |
| `#1118271f` | - |

**Most-used computed colours**, which is a different measurement and a useful
cross-check on which tokens actually reach the screen:

`rgb(229, 231, 235)` 11547 uses, `rgb(255, 255, 255)` 9079, `rgb(44, 96, 232)`
815, `rgb(239, 239, 239)` 752, `rgb(93, 100, 148)` 744, `rgb(51, 51, 51)` 462,
`rgb(35, 38, 59)` 371, `rgb(161, 161, 170)` 252, `rgb(214, 214, 231)` 232,
`rgb(0, 61, 255)` 136, `rgb(69, 122, 255)` 123, `rgb(220, 220, 220)` 117.

`rgb(0, 61, 255)` and `#003dff` are the same colour, which is the confirmation
that the brand token reaches the page rather than being a stylesheet artefact.

### 3.3 Typography

**Families.** Two, both open-licensed and both nameable without becoming an
asset dependency:

| Family | Weights loaded | Role | Fallback stack, normative |
|---|---|---|---|
| Sora | 300, 400, 500, 600, 700, 900 | display headings, statistics | `"Sora", "Trebuchet MS", "Segoe UI", system-ui, sans-serif` |
| Inter | 400, 500, 600, 700, 800, 900 | everything else | `"Inter", "Helvetica Neue", Arial, system-ui, sans-serif` |

A third family, Avenir Next at 700 and 900, is declared in the stylesheets and
was not observed rendering. It is a legacy declaration; do not load it.

**The scale actually rendered**, measured across all six routes. The count
column matters more than the list: this is a site with one body size and a very
short ladder above it.

| Size | Weight | Line height | Uses | Role |
|---|---|---|---|---|
| `16px` | 400 | `24px` | 8876 | body, and nearly everything |
| `14px` | 700 | `16px` | 1640 | small bold labels, navigation, table headers |
| `16px` | 400 | `19.2px` | 595 | body in tighter components |
| `13px` | 400 | `24px` | 405 | fine print |
| `14px` | 400 | `20px` | 279 | secondary body |
| `16px` | 400 | `18px` | 224 | body in dense lists |
| `16px` | 700 | `24px` | 159 | bold body |
| `12px` | 400 | `16px` | 126 | captions |
| `10px` | 700 | `13px` | 84 | the smallest label, all caps |
| `14px` | 600 | `20px` | 73 | button text |
| `76px` | 700 | `76px` | 36 | the display heading, line height exactly 1 |
| `24px` | 400 | `32px` | 12 | section subheadings |
| `20px` | 400 | `28px` | 24 | lead paragraphs |
| `14.4px` | 700 | `14.4px` | 30 | a component-local step |
| `12.992px` | 400 | `19.488px` | 21 | a component-local step |
| `13.6px` | 400 | normal | 24 | a component-local step |

The three fractional sizes come from a component that scales its own root by a
factor rather than from a fluid rule. Reproduce the factor, not the fraction.

**Display headings.** `76px` at `76px` line height, weight 700, in Sora. The
route heading on the error route is measured separately at `45px` rising to
`56px` above the large breakpoint, with a line height factor of `1.2`, and
carries a gradient fill and a drop shadow (Sections 3.9 and 14).

**Letter spacing.** No measured tracking adjustments. The all-caps `10px` label
is the only place where tracking is visually present and it is a consequence of
the weight, not a declared value.

### 3.4 Contrast pairs

Every pair the build actually uses, with the ratio. Pairs below the required
ratio are marked, and the substitution is stated rather than left to the builder.

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `#ffffff` | `#000033` | 18.9 to 1 | passes |
| `#ffffff` | `#003dff` | 6.9 to 1 | passes |
| `#23263b` | `#ffffff` | 14.5 to 1 | passes |
| `#484c7a` | `#ffffff` | 7.4 to 1 | passes |
| `#484c7a` | `#f3f3f3` | 6.7 to 1 | passes |
| `#003dff` | `#ffffff` | 6.9 to 1 | passes |
| `#003dff` | `#f3f3f3` | 6.3 to 1 | passes |
| `#457aff` | `#ffffff` | 3.6 to 1 | large text and non-text only |
| `#9698c3` | `#ffffff` | 2.6 to 1 | **fails**: use `#484c7a` for any text |
| `#d6d6e7` | `#000033` | 13.9 to 1 | passes |
| `#c9c9c9` | `#ffffff` | 1.7 to 1 | **fails**: hairlines only, never text |

The two failing pairs are both real in the reference and both carry text
somewhere on it. This build substitutes as stated in the verdict column, and
Section 35.3 records that the substitution is a deliberate departure from the
measurement.

### 3.5 Spacing, radii and borders

**Radii**, measured with their use counts:

| Radius | Uses | Applied to |
|---|---|---|
| `1px` | 24 | inline highlight spans |
| `2px` | 48 | consent surface controls |
| `3px` | 5 | filter chrome |
| `4px` | 117 | form fields, the most common radius on the site |
| `5px` | 6 | embedded chat controls |
| `6px` | 48 | navigation panels |
| `8px` | 34 | cards and large buttons |
| `17px` | 3 | a filter pill |
| `20px` | 9 | a switch track |
| `50px` | 3 | a search pill |
| `50%` | 9 | circular icon buttons |
| `9999px` | 6 | fully rounded pills |

Both `50%` and `9999px` produce a circle on a square element. They are not
interchangeable on a non-square element, and both are present because they were
authored by different hands. Use `9999px` for pills and `50%` only where the
element is square by construction.

**Borders.** Hairlines are `1px` solid in `#e5e5e5` on light surfaces and
`#d6d6e7` at low opacity on dark ones.

### 3.6 Elevation

Six measured shadows. There is no elevation scale in the reference; each shadow
belongs to a component.

| Shadow | Component |
|---|---|
| `rgba(0, 0, 0, 0.1) 0px 1px 20px 0px` | the sticky header |
| `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.1) 0px 2px 4px -2px` | navigation panels |
| `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.1) 0px 4px 6px -4px` | the floating chat launcher |
| `rgba(0, 61, 255, 0.12) 0px 0px 6px 2px` | the form submit button, a brand-tinted glow |
| `rgba(0, 0, 0, 0.14) 0px 10px 30px 0px` | the chat message bubble |
| `rgba(0, 0, 0, 0.12) 0px 2px 12px 0px` | the chat prompt bubble |

The four-layer shadows are the framework's two-step elevation with two empty
layers preserved; the empty layers are not decorative and removing them changes
nothing, but keeping them keeps the values greppable against the reference.

One text shadow is measured: `rgb(75, 94, 240) 0px 1px 0px` on the form submit
button, which is a one-pixel blue underline drawn as a shadow.

### 3.7 Motion tokens

The full easing inventory is in Section 6.3. The four that carry the site:

| Token | Value | Uses |
|---|---|---|
| `--ease-out` | `cubic-bezier(0,0,.2,1)` | 319 |
| `--ease-in` | `cubic-bezier(.4,0,1,1)` | 296 |
| `--ease-emphasis` | `cubic-bezier(.05,0,0,1)` | 209 |
| `--ease-in-out` | `cubic-bezier(.4,0,.2,1)` | 90 |

Durations measured on declared transitions: `0.1s`, `0.2s`, `0.25s`, `0.3s`,
`0.4s`, `0.75s`, `0.9s`. The `0.9s` pair belongs to the promotion bar and is the
longest transition on the site.

The most common declared transition property is `all`, with 13028 occurrences.
That is a framework default, not a decision, and it is worth naming: `all` on a
component that also changes layout is the standard cause of a transition that
animates width and height on hover. The build must declare the properties it
means.

### 3.8 Layering

Measured stacking contexts, in use order:

| Value | Uses | Occupant |
|---|---|---|
| `0` | 3 | reset |
| `1` | 50 | in-flow overlaps inside cards |
| `2` | 15 | hover and focus lifts |
| `3` | 6 | sticky table headers |
| `10` | 6 | section overlays |
| `20` | 3 | the promotion bar |
| `99` | 17 | the header |
| `101` | 6 | navigation panels |
| `999` | 18 | the search overlay |
| `9999` | 8 | the consent surface |
| `2147483646` | 6 | third-party chat backdrop |
| `2147483647` | 9 | third-party chat launcher |

The last two are a third-party surface claiming the top of the integer range.
The build's own layers must stay at or below `999`, and Section 35.2 records
that the two maximum values belong to an embed rather than to this design
system.

### 3.9 Effects vocabulary

**Gradients**, measured with their use counts:

| Gradient | Uses | Applied to |
|---|---|---|
| `linear-gradient(to right, rgb(30, 89, 255) 0%, rgb(187, 209, 255) 100%)` | 36 | the statistic numbers, as a clipped text fill |
| `linear-gradient(to right, #000033, #484c7a, #000033)` | 20 | a horizontal divider on dark grounds, dark at both ends |
| `linear-gradient(220deg, #457aff 0%, #1e59ff 60.16%)` | 8 | the primary button on dark grounds |
| `linear-gradient(263deg, #457aff -2.29%, #003dff 59.25%)` | 8 | the primary button on light grounds |
| `radial-gradient(100% 100% at 100% 0%, rgb(0, 0, 51) 0%, rgb(0, 0, 51) 100%)` | 3 | the error route ground |
| `radial-gradient(75.93% 75.93% at 48.86% 10.98%, rgb(7, 56, 210) 0%, rgb(14, 41, 126) 100%)` | 3 | the error route heading fill |
| `linear-gradient(rgb(255, 255, 255), rgb(245, 245, 250))` | 3 | the form panel |
| `linear-gradient(138deg, rgba(118, 160, 255, 0.7) 0%, rgba(0, 61, 255, 0.7) 25.08%, rgba(151, 71, 255, 0.7) 56.38%, rgba(118, 160, 255, 0.7) 100%)` | - | the form submit button on hover, Section 5.6 |

The second gradient is worth reading carefully. It is dark at both ends and
lighter in the middle, which is a divider that fades out at both edges rather
than a fill.

**Filters.** One measured: `drop-shadow(rgb(12, 21, 54) 0px 54px 54px)
drop-shadow(rgba(0, 0, 0, 0.6) 0px 16px 14px)`, applied to the error route
heading. Two stacked drop shadows on gradient-filled text, one very large and
soft, one tight.

**Clip paths.** One measured: `inset(0px 100% 0px 0px)`, a fully clipped
starting state for a loader that reveals left to right.

**Masks.** One declared mask gradient family:
`linear-gradient(180deg, transparent, #000000 var(--mask-fade-size))`, used to
fade the top edge of a scrolling column. The custom property is the fade
distance and is set per instance.

> **In plain language.** The look is built from a very small kit, and the
> smallness is the point.
>
> There is one blue that matters. Every button you are meant to press, every link,
> and every hover in the whole site is that one electric blue. There is a lighter
> version of it for gradients and a slightly darker one for the moment your finger
> is down. Everything else on the page is either near-black with a blue tint, or
> white, or one of a short ladder of greys.
>
> Text is nearly all one size. Out of roughly eleven thousand pieces of text
> measured across the site, nearly nine thousand are the same size as the sentence
> you are reading. Above that there is one giant display size for the headlines
> and almost nothing in between. That gap is the site's whole typographic
> personality: ordinary, ordinary, ordinary, then enormous.
>
> Two typefaces, split strictly. A geometric one for headlines only, and a plain,
> highly legible one for everything else. Both are free and neither ships as a
> file with this document.
>
> Corners are rounded by a very small amount nearly everywhere, a little more on
> cards, and fully round on the few pill-shaped things. Shadows are rare and soft,
> and there is no ladder of them: each one belongs to a specific component.
>
> Two honest notes. First, two of the colour pairings in the reference are too
> faint to read comfortably, so this build uses a darker grey in those places and
> says so rather than copying a mistake. Second, the site's stylesheets tell
> everything to animate every property, which is a habit rather than a decision,
> and it is the usual reason a button quietly grows when you hover it. This build
> names the properties it means to animate.

---

## 4. Iconography

Every icon is inline geometry. No icon is a file. Coordinates below are quoted
from the ledger's inline geometry catalogue, which recorded them from the
rendered pages.

### 4.1 The mark and the wordmark

The reference's mark and wordmark are trademarked geometry and are **not**
transcribed here. Two facts about them are structural and are kept, because the
layout was built around them:

| Element | Measured `viewBox` | Rendered size |
|---|---|---|
| Mark alone, used below the large breakpoint | `0 0 501 501` | `24 x 24` |
| Mark plus wordmark, used at and above it | `0 0 2197 501` | `110 x 25` |

The wordmark is therefore `4.386` times as wide as it is tall, and the mark is
square. Any replacement must hold that ratio or the header's left group
re-wraps.

**Procedural placeholder, normative for this build.** A square mark in a
`0 0 501 501` box:

| Primitive | Attributes |
|---|---|
| `circle` | `cx=250 cy=250 r=210` fill none, stroke `currentColor`, `stroke-width=54` |
| `path` | `M250 40 A210 210 0 1 0 460 250 L250 250 Z` fill `currentColor` |

A quarter-filled ring, which reads at `24px` and is unambiguously not the
reference's mark. The wordmark placeholder is the word `<BRAND>` set in Sora at
weight 700, letter spacing `-0.02em`, in a `0 0 2197 501` box scaled to width.

### 4.2 Search

The most-used icon on the site, appearing in the header field, the mobile header
and the error route.

| `viewBox` | Primitives |
|---|---|
| `0 0 24 24` | `circle cx=11 cy=11 r=8`, plus one `line` from the circle's lower right to the box corner |

Stroke `currentColor`, `stroke-width` 2, round caps. Rendered at `20 x 20` in
the header field and `16 x 16` in dense contexts. The handle line runs from
approximately `16.65, 16.65` to `21, 21`.

### 4.3 The circle arrow

The promotion bar's action affordance, and the same glyph appears in the footer.

| `viewBox` | Primitives |
|---|---|
| `0 0 24 24` | `circle cx=12 cy=12 r=10`, one `polyline` forming the arrowhead, one `line` forming the shaft |

Rendered at `32 x 32` in the promotion bar and `24 x 24` in the footer. It
carries a hover behaviour measured on the reference: `transition-all` over
`400ms` with `cubic-bezier(0.4, 0, 1, 1)`, scaling to `1.1` and changing fill.
That is one of only eight runtime animations captured on the whole site.

### 4.4 The globe

The language selector.

| `viewBox` | Primitives |
|---|---|
| `0 0 24 24` | `circle cx=12 cy=12 r=10`, one horizontal `line` across the equator, one `path` `M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z` |

Rendered at `16 x 16`. The path is the meridian ellipse, drawn as two arcs with
a radius of `15.3` in each direction, which is what gives it its slight barrel.

### 4.5 Chevrons

Three distinct chevrons are in use and they are not interchangeable.

| Name | `viewBox` | Geometry | Where |
|---|---|---|---|
| Navigation caret | `0 0 24 24` | one `polyline` | header items that open a panel |
| Small right chevron | `0 0 7 11` | `path M1.14645 9.85355C0.951184 9.65829 0.951184 9.34171 1.14645 9.14645L4.79289 5.5L1.14645 1.85355C0.951184 1.65829 0.951184 1.34171 1.14645 1.14645C1.34171 0.951184 1.65829 0.951184 1.85355 1.14645Z` | inline links |
| Wide chevron | `0 0 18 10` | `path M1 1L9 9L17 1`, stroke `currentColor`, `stroke-width=2`, fill none | accordion and select controls |
| Accordion caret | `0 0 24 24` | `path M9 18l6-6-6-6` | the capability accordion, Section 9.4 |

The accordion caret is measured with `opacity: 0` in its resting state and a
`300ms` transition on `all` with a `rotate(0)` transform, so it appears on
hover and rotates when its panel opens.

### 4.6 Menu and close

| Name | `viewBox` | Primitives | Rendered |
|---|---|---|---|
| Menu | `0 0 24 24` | three `line` elements, evenly spaced | `20 x 20`, below the large breakpoint only |
| Close | `0 0 24 24` | two `line` elements crossing | `20 x 20` |
| Close, small | `0 0 13 14` | two `path` elements, each a rounded bar drawn as a filled shape | `13 x 14`, inside filter chips |

The menu icon and the close icon are the same element with two states; the
ledger recorded both, one with three lines and one with two, at the same
position.

### 4.7 Status and control glyphs

| Name | `viewBox` | Geometry |
|---|---|---|
| Check | `0 0 17 12` | `path M15.9942 0.20332C16.2652 0.474413 16.2652 0.913942 15.9942 1.18504L5.81289 11.3663C5.54179 11.6374 5.10226 11.6374 4.83117 11.3663L0.20332 6.73846C-0.0677733 6.46736 -0.0677733 6.02783 0.20332 5.75673Z` |
| Tooltip | `0 0 16 16` | `circle cx=8 cy=8 r=7` stroke `currentColor` fill none, plus `path M8 11V8M8 5V5` stroke-width 2 |
| Download arrow | `0 0 14 14` | `path M7.14004 0.0908203C7.5065 0.0908203 7.80358 0.387898 7.80358 0.754361V11.5385L12.8639 6.47822C13.123 6.21909 13.5432 6.21909 13.8023 6.47822C14.0614 6.73734 14.0614 7.15748 13.8023 7.41661Z` |

The check and the tooltip both appear in the pricing comparison grid
(Section 10.4), the check as a present-feature marker and the tooltip as the
affordance for a footnote.

### 4.8 Search overlay glyphs

Three icons belong to the search overlay and are measured separately because
they come from the search library's own set.

| Name | `viewBox` | Geometry |
|---|---|---|
| Submit | `0 0 24 24` | one `path`, a magnifier drawn as a filled shape rather than a stroked circle |
| Clear | `0 0 24 24` | `path M5.293 6.707l5.293 5.293-5.293 5.293c-0.391 0.391-0.391 1.024 0 1.414s1.024 0.391 1.414 0l5.293-5.293 5.293 5.293c0.391 0.391 1.024 0.391 1.414 0s0.391-1.024 0-1.414l-5.293-5.293 5.293-5.293Z` |
| Loading | `0 0 100 100` | `circle cx=50 cy=50 r=35` fill none stroke `currentColor` `stroke-width=6`, rotated by the `spin` keyframe in Section 6.2 |

A second submit and reset pair exists at `0 0 40 40` and `0 0 20 20` from the
results interface. Both draw the same two shapes at a different scale; use the
`24 x 24` pair everywhere and scale it, and record the deviation.

### 4.9 The full inventory

Thirty-three inline vector elements were catalogued across the six routes.
Twelve are the icons above. The remainder are: the mark and wordmark at two
sizes, six social glyphs in the footer, three consent-surface glyphs belonging
to a third-party embed, a chat glyph belonging to another, and the gradient
definitions attached to the error route heading, which are `stop` elements
rather than shapes.

The three consent glyphs and the chat glyph carry hard-coded fills, two mid
greys and a white, none of which belong to the palette in Section 3.2. They are
recorded and excluded, per Section 35.2.

> **In plain language.** Every small symbol on the site, the magnifier, the
> arrows, the ticks, the little globe by the language menu, is drawn from
> instructions in this document rather than loaded as a picture. That is what
> lets the whole build ship without a single image file, and it also means the
> symbols stay crisp at any size and can take any colour.
>
> There are about a dozen that matter, and one detail is worth knowing: there are
> three different arrow-shaped chevrons in use, at different proportions, for
> different jobs. They look almost identical and they are not interchangeable.
> Using one where another belongs is the sort of thing nobody can name when they
> look at the finished page, and everybody feels.
>
> The company's own logo is deliberately not copied here. It is somebody's
> trademark. What is recorded instead is its shape: the mark is a square, and the
> logo with the name is four and a bit times wider than it is tall. Keep those
> proportions and the header lays out correctly with your own logo in it. There is
> a simple stand-in drawn in the specification so the build is never blocked
> waiting for artwork.

---

## 5. Global chrome

Present on the four routes whose page type calls for it, per Section 2.4, and
entirely absent from the demo request and error routes.

### 5.1 The promotion bar

The topmost strip, full width, on `#000033`.

| Property | Value |
|---|---|
| Layer | `z-index: 20` |
| Content | a label, a message, an action label and the circle arrow of Section 4.3 |
| Label type | `10px` weight 700 at `13px` line, all caps |
| Message type | `14px` weight 700 at `16px` line |
| Rotation | slides cycle; two were captured |

The transition is the most precisely measured motion on the site because it was
caught running:

| Property | Duration | Easing | Fill |
|---|---|---|---|
| `opacity` | `900ms` | `ease-in-out` | backwards |
| `transform` | `900ms` | `ease-in-out` | backwards |

Three states are carried as classes on the slide: a hidden resting state
translated down by `32px`, an entering state animating from that to zero, and an
exiting state animating from zero to `-32px` while fading. Measured intermediate
values from the capture: an entering slide at `translateY(31.9791px)` with
opacity `0.000654496`, and later at `translateY(9.14285px)` with opacity
`0.714286`; an exiting slide at `translateY(-2.23077px)` with opacity `0.930288`
and later at `translateY(-29.7693px)` with opacity `0.0697081`.

Those six numbers are one animation sampled twice. They are quoted because they
pin the direction, the distance and the curve simultaneously, and a build that
matches them has the promotion bar exactly right.

`will-change: opacity, transform` is declared on all three slide states.

### 5.2 The utility bar

Below the promotion bar, right-aligned, on the same dark ground.

| Item | Type | Notes |
|---|---|---|
| `Company` | `14px` 400 | plain link |
| `Partners` | `14px` 400 | plain link |
| `Support` | `14px` 400 | plain link |
| `Login` / `Logout` | `14px` 400 | both strings present in the markup, one shown at a time |
| Language | `14px` 400 with the globe of Section 4.4 and a caret | opens a list |

The language list carries six entries: `English`, `German`, `French`,
`Brazilian Portuguese`, `Spanish`, `Italian`. The active entry is marked with a
class rather than a glyph.

Items are separated by a `1px` vertical rule in `#484c7a`.

### 5.3 The header

| Property | Value |
|---|---|
| Layer | `z-index: 99` |
| Height | `80px` at desktop, measured from the capture |
| Ground | `#000033` on dark routes, `#ffffff` on the Customers route |
| Shadow when stuck | `rgba(0, 0, 0, 0.1) 0px 1px 20px 0px` |
| Transition | `background-color 0.3s, padding 0.3s` |

Left group: the mark, or the mark and wordmark above `1024px`. Centre group:
the five primary items at `16px` weight 400. Right group, in order: the search
field, the secondary button, the primary button.

The search field is a pill: `50px` radius, `44px` tall, `1px` border in
`#484c7a` on dark, with the search icon at `20 x 20` inset `16px` from the left
and the placeholder `Search or Ask AI` at `16px` 400 in `#9698c3`.

Below `1024px` the centre group and the right group collapse. The header then
carries the mark, the menu icon of Section 4.6, and a circular search button at
`50%` radius.

Measured hover, on the four routes that carry the dark header: the primary
navigation buttons move from `rgb(255, 255, 255)` to `rgb(0, 61, 255)`, and both
`::before` and `::after` move with them. On the light-header Customers route the
same components move from `rgb(35, 38, 59)` to `rgb(0, 61, 255)`. The hover
target is therefore the brand blue on both grounds, and only the resting colour
changes with the route.

### 5.4 The panels

Four of the five primary items open a panel rather than navigating.

| Property | Value |
|---|---|
| Layer | `z-index: 101` |
| Radius | `6px` |
| Shadow | the four-layer panel shadow in Section 3.6 |
| Layout | `flex` with wrapping and a `16px` gap |
| Trigger | pointer entry and keyboard activation, per Section 31.2 |

The panel's contents were not captured in a state that resolves their full link
lists, and Section 35.1 records that. What is specified is the container, the
grid and the behaviour; the link inventory is the build's to supply from the
site map.

### 5.5 The mobile drawer

Below `1024px`. Opened by the menu icon, full height, covering the page.

Contents in order: the five primary items as an accordion, then a `Quick Access`
group heading at `16px` weight 400, then the utility items `Company`,
`Partners`, `Support`, `Login`, `Logout`, each in a `block` container, then the
two buttons at full width.

The drawer's close control carries the string `Close` at `16px` with a `24px`
line, which is the only place on the site where a close affordance is labelled
in words rather than drawn.

### 5.6 Buttons

Three variants, all measured.

**Primary.** Fill `linear-gradient(263deg, #457aff -2.29%, #003dff 59.25%)` on
light grounds and `linear-gradient(220deg, #457aff 0%, #1e59ff 60.16%)` on dark
ones. Text `#ffffff` at `14px` weight 600 with a `20px` line. Radius `8px`.
Padding `16px` horizontal.

**Secondary.** Transparent fill, `1px` border in `#ffffff` on dark and `#003dff`
on light, text in the border colour, same type and radius as primary.

**Form submit.** Measured separately because it belongs to the form system and
behaves differently:

| State | Value |
|---|---|
| Rest | fill `rgb(69, 122, 255)`, shadow `rgba(0, 61, 255, 0.12) 0px 0px 6px 2px`, text shadow `rgb(75, 94, 240) 0px 1px 0px` |
| Hover | `transform: matrix(1.02, 0, 0, 1.02, 0, 0)`, fill to `rgba(0, 0, 0, 0)` and a four-stop gradient in its place: `linear-gradient(138deg, rgba(118, 160, 255, 0.7) 0%, rgba(0, 61, 255, 0.7) 25.08%, rgba(151, 71, 255, 0.7) 56.38%, rgba(118, 160, 255, 0.7) 100%)` |
| Will change | `box-shadow, transform` |

The hover swaps a flat fill for a translucent four-stop gradient **and** scales
by two percent. Both halves are needed; the scale alone reads as a bug and the
gradient alone reads as a colour change.

### 5.7 The footer

On `#000033`, full width, present on the four routes with chrome.

Structure, measured from the capture: a link row carrying `Careers`,
`Contact Us`, `About <BRAND>`, `Anti-Modern Slavery Statement`; a
`Social networks` heading at `16px` 400 in `#d6d6e7` above six social glyphs; a
newsletter line reading `Get the latest in AI search - straight to your inbox.`
with an inline glyph; and a legal bar carrying `Cookie settings`,
`Trust Center`, `Privacy Policy`, `Terms of service` and further items,
separated by `1px` vertical rules.

The divider above the legal bar is the fading gradient of Section 3.9:
`linear-gradient(to right, #000033, #484c7a, #000033)`.

> **In plain language.** The furniture that sits around every page.
>
> At the very top, a thin dark strip cycles through announcements. This is the
> single most carefully measured piece of movement in the document, because the
> capture caught it mid-slide: a message rises into place from just below while
> fading in, sits, then rises out of the top while fading away, and each half
> takes a little under a second. Six intermediate positions were recorded, which
> is enough to pin the distance, the direction and the exact feel of the
> acceleration.
>
> Under that, a row of small links and a language menu offering six languages.
> Under that, the main bar: the logo, five menu items, a search box shaped like a
> pill, and two buttons.
>
> Four of the five menu items do not go anywhere. They drop a panel down.
>
> Hovering any menu item turns it the brand blue. That is true on both the dark
> pages and the light one, which means the resting colour changes with the page
> and the hover colour never does. It is a small thing and it is the sort of small
> thing that makes a site feel like one site.
>
> On a phone the whole middle disappears behind a menu button, and the panel that
> opens is a full-height drawer with everything stacked.
>
> One button behaves unlike the others. The one that submits the demonstration
> request grows by two percent when you hover it and swaps its flat blue for a
> soft four-colour wash. Both halves matter. The growth alone looks like a
> mistake, and the colour alone looks like an ordinary hover.

---
## 6. Motion language

### 6.1 The three mechanisms

Everything that moves on the reference does so through one of three mechanisms,
and the ledger distinguishes them, so the build does not have to guess:

| Mechanism | How it was established | What uses it |
|---|---|---|
| Declared transition | parsed from the stylesheets | hover states, the header ground, panels |
| Keyframe animation | parsed from `@keyframes` blocks | the statistics column, loaders, the hero timer |
| Runtime animation | read from the live animation registry during capture | the promotion bar slides, one icon hover |

There is no fourth mechanism. In particular there is **no scroll-scrubbed
motion** on this site, which Section 7.1 establishes as a measurement rather
than an omission.

### 6.2 Keyframes

One hundred and sixty keyframe blocks were parsed. Most belong to third-party
embeds. The ones that belong to the site, and what they do:

| Name | Definition | Used by |
|---|---|---|
| `scrollUp` | `{ 0% { transform: translateY(0); } 100% { transform: translateY(-50%); } }` | the statistics column, Section 6.5 |
| `agentic-hero-dot-fill` | `{ from { transform: scaleX(0); } to { transform: scaleX(1); } }` | the hero carousel timer, Section 6.6 |
| `fadeIn` | `{0%{opacity:0}to{opacity:1}}` | generic entrance |
| `scale` | `{0%{transform:scale(1)}80%{transform:scale(1.1)}to{transform:scale(1)}}` | attention pulse on an icon |
| `spin` | `{ to { transform: rotate(360deg); } }` | the search loading glyph |
| `spin` (second) | `{ 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }` | a centred loader |
| `rotate` | `{ 0% { transform: rotate(0deg); } 100% { transform: rotate(-360deg); } }` | a counter-rotating decoration |
| `fadeInLeft` | `{ 0% { opacity: 0; transform: translateX(100px); } 100% { opacity: 1; transform: translateX(0); } }` | panel entrance |
| `slideIn` | `{ from { transform: translateX(-100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }` | drawer entrance |
| `slideOut` | `{ from { transform: translateX(0); opacity: 1; } to { transform: translateX(-100%); opacity: 0; } }` | drawer exit |
| `bounceIn` | `{ 0% { transform: scale(0); } 70% { transform: scale(1.1); } 85% { transform: scale(0.9); } 100% { transform: scale(1); } }` | badge entrance |
| `bounceOut` | `{ 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(0); opacity: 0; } }` | badge exit |
| `caret` | `{ 50% { border-color: transparent; } }` | the typing caret in the search placeholder |
| `progressAnimationStrike` | `{0%{width:0}to{width:95%}}` | a progress bar that deliberately stops short |
| `animScale` | `{0%,60%{width:3em}to{width:4em}}` | a width pulse |
| `ringBounce` | `{0%{box-shadow:0 0 0 0 var(--tw-ring-color)}50%,to{box-shadow:0 0 0 .5em var(--tw-ring-color)}}` | focus emphasis |

Five further blocks animate a bar to a fixed percentage width and are generated
per instance: `42.955%`, `60%`, `11.28%`, `80%` and `27.45%`. They are the
statistic bars, and the percentages are content, not design. A build that
hard-codes them has hard-coded five data points.

`progressAnimationStrike` stopping at `95%` is deliberate: a progress bar that
never reaches its end while work continues.

### 6.3 The easing inventory

Twenty-five distinct curves were measured. The full list, with counts, because
the distribution is the useful part:

| Curve | Uses |
|---|---|
| `cubic-bezier(0,0,.2,1)` | 319 |
| `cubic-bezier(.4,0,1,1)` | 296 |
| `cubic-bezier(.05,0,0,1)` | 209 |
| `cubic-bezier(.4,0,.2,1)` | 90 |
| `cubic-bezier(0.4, 0, 0.2, 1)` | 74 |
| `cubic-bezier(0.785, 0.135, 0.15, 0.86)` | 35 |
| `cubic-bezier(.55,.085,.68,.53)` | 32 |
| `cubic-bezier(0,1.11,.7,1.43)` | 32 |
| `cubic-bezier(0,.3,.15,1)` | 23 |
| `cubic-bezier(.3,0,.15,1)` | 19 |
| `cubic-bezier(.6,.6,0,1)` | 18 |
| `cubic-bezier(.39,.575,.565,1)` | 18 |
| `cubic-bezier(.175,.885,.32,1.275)` | 13 |
| `cubic-bezier(0.4, 0, 1, 1)` | 9 |
| `cubic-bezier(0.6, 0.6, 0, 1)` | 9 |
| `cubic-bezier(.75,0,.08,1)` | 9 |
| `cubic-bezier(0,0,1,1)` | 9 |
| `cubic-bezier(0, 0, 0.2, 1)` | 8 |
| `cubic-bezier(.275,.0425,.34,.265)` | 8 |
| `cubic-bezier(0,.555,.35,.715)` | 8 |
| `cubic-bezier(0.175, 0.885, 0.32, 1.275)` | 8 |
| `cubic-bezier(0.215, 0.61, 0.355, 1)` | 7 |
| `cubic-bezier(0.22, 1, 0.36, 1)` | 6 |
| `cubic-bezier(.07,.49,.5,1)` | 6 |
| `cubic-bezier(0.20, 0.00, 0.60, 1.00)` | 5 |

Three observations the build should act on:

- The top four are the framework's own ease-out, ease-in, emphasized and
  standard curves. They account for 914 of the uses and are the site's real
  motion vocabulary.
- `cubic-bezier(0,1.11,.7,1.43)` and `cubic-bezier(.175,.885,.32,1.275)`
  overshoot past 1. They belong to badge and pill entrances, and using them on
  anything with a hard edge against a neighbour produces a visible collision.
- The same curve appears in two spellings, spaced and unspaced. They are
  identical. Normalize on one and the count above collapses to eighteen distinct
  curves.

### 6.4 Named motion: the promotion slide

Specified in Section 5.1 with its measured intermediate values. It is repeated
here as a named piece of the motion language because it is the only motion on
the site that a visitor sees without acting: `900ms`, `ease-in-out`, opacity and
transform together, a `32px` travel, entering from below and leaving upward.

### 6.5 Named motion: the statistics column

A vertical column of statistics that scrolls continuously and loops. Two
instances were captured with different speeds:

| Instance | Duration | Timing | Iterations |
|---|---|---|---|
| First column | `21600ms` | linear | infinite |
| Second column | `30933.333333333332ms` | linear | infinite |

Both run the `scrollUp` keyframe, translating from zero to `-50%`. The `-50%` is
what makes it seamless: the track holds two copies of the content, so at the
halfway point the second copy is exactly where the first began.

Measured intermediate transforms during the capture:
`matrix(1, 0, 0, 1, 0, -289.486)`, `matrix(1, 0, 0, 1, 0, -130.497)` and
`matrix(1, 0, 0, 1, 0, -298.488)`, which confirm the direction and the linearity.

The two durations differ because the two columns hold different amounts of
content and the design keeps the pixel speed constant. Reproduce the speed, not
the duration: a column of `N` items runs for `N` times the per-item duration.

The top edge of the column is faded with the mask gradient in Section 3.9.

### 6.6 Named motion: the hero carousel timer

The hero panel advances on a timer, and the timer is visible as a filling bar
inside the active dot.

| Property | Value |
|---|---|
| Keyframe | `agentic-hero-dot-fill`, `scaleX(0)` to `scaleX(1)` |
| Duration | `6500ms` |
| Timing | linear |
| Iterations | 1 |
| Fill | forwards |

`6500ms` is therefore the hero's dwell time per panel, measured rather than
estimated. The dot's fill is a transform on a child element, not a width
animation, which is why it is smooth.

The home hero carries three dots and the analyst band carries five, both read
from the capture.

### 6.7 Hover motion

Two hover behaviours were caught as running animations rather than as declared
transitions, which means they are the two the site actually spends motion on:

| Target | Property | Duration | Easing |
|---|---|---|---|
| The circle-arrow icon of Section 4.3 | `visibility`, with `transform` and fill alongside | `400ms` | `cubic-bezier(0.4, 0, 1, 1)` |
| The form submit button | `transform` and `background-image` | per Section 5.6 | - |

Everything else that changes on hover changes colour only, per the measured
diffs in Section 5.3.

### 6.8 Reduced motion

Seventeen `prefers-reduced-motion: reduce` blocks are present in the reference's
stylesheets, which establishes that the system is reduced-motion aware. What
each block does was not resolved from the capture.

**Normative for this build.** Under the reduced setting:

- The promotion bar stops cycling and shows one message.
- The statistics column stops and shows its first screenful.
- The hero carousel stops advancing; its dots remain operable.
- Hover transforms are removed; hover colour changes remain.
- The loading spinner is replaced by a static glyph with a text alternative.

Nothing that conveys information may be removed, only its motion.

> **In plain language.** Three kinds of movement exist here and it is worth
> knowing there is no fourth.
>
> Some things move because you hovered them. Some things move because they are
> playing a short loop, like a spinner. And two things move on their own, forever:
> the announcement strip at the top, and a column of statistics on one page that
> scrolls slowly upward.
>
> That second one has a trick worth explaining, because building it the obvious
> way produces a visible jump. The column holds two identical copies of its
> content stacked, slides up by exactly half its own height, and then starts
> again. At the moment it restarts, the second copy is sitting precisely where
> the first one was, so the loop is invisible. The two columns on the page take
> different lengths of time, and that is because they hold different amounts:
> they move at the same speed, which is the thing to copy.
>
> The rotating panel in the hero gives you six and a half seconds per panel, and
> it tells you so: the little dot underneath fills up like a progress bar while
> you read.
>
> One number in here is a joke the original designers played on themselves. There
> is a loading bar that fills to ninety-five percent and stops. It is meant to.
>
> Finally, anyone who has told their computer they prefer less movement gets a
> still site: the announcements stop cycling, the statistics stop scrolling, the
> panels stop advancing, and nothing is lost, because none of that movement was
> carrying information in the first place.

---

## 7. Scroll and reveal behaviour

### 7.1 What the reference does not do

This is the most important measured negative in the document.

The capture samples every route at nine scroll positions and diffs computed
styles across them. Any selector whose transform, opacity, clip path or mask
changes across frames is scroll-driven. Across all six routes and all three
widths, the total inventory of scroll-driven selectors is:

| Route and width | Scroll-driven selectors |
|---|---|
| Home, desktop | 2, both belonging to the promotion bar |
| Pricing, desktop | 2, both belonging to the promotion bar |
| Products, desktop | 1, the promotion bar |
| Customers, desktop | 1, the promotion bar |
| Demo request, all widths | 1, the statistics column |
| Every route, tablet and mobile | 0 |

The promotion bar entries are the timer-driven slide of Section 6.4 caught
mid-cycle, not scroll-driven motion. The statistics column is the loop of
Section 6.5.

**The conclusion is normative: this site has no scroll-scrubbed motion and no
scroll-triggered reveals.** Content is present and static; it does not fade or
rise into place as you reach it. Building it with entrance reveals produces a
different, and slower, site.

No smooth-scrolling library was detected, and the root element carries no
scroll-state classes on any route. The one root class observed changing is
`om-position-floating-top` on the Products route, which belongs to a third-party
promotion embed.

### 7.2 The sticky header

The header is sticky, and it is the only sticky element on the site outside the
pricing comparison grid.

| Property | Value |
|---|---|
| Transition | `background-color 0.3s, padding 0.3s` |
| Stuck shadow | `rgba(0, 0, 0, 0.1) 0px 1px 20px 0px` |
| Layer | `z-index: 99` |

The promotion bar scrolls away; the header remains. The measured page heights in
Section 2.1 are large enough that the header is stuck for most of every route.

### 7.3 The pricing grid's sticky header row

The comparison grid on the pricing route keeps its plan header row visible while
its body scrolls, at `z-index: 3`. It is specified in Section 10.4.

### 7.4 The marquee rows

The home route carries two horizontal rows of customer cards that extend beyond
both edges of the viewport, offset from each other, and drift horizontally. They
use the same two-copy loop as the statistics column, on the horizontal axis.

Duration was not captured for these rows and is **inferred**: at the measured
card width and gap, a per-card duration matching the statistics column's pixel
speed gives a full-row cycle of about forty seconds. Section 35.3 records this
as a reconstruction.

Both rows pause on hover, per Section 31.5.

> **In plain language.** Here is a thing this site does not do, and it matters
> more than most things it does.
>
> Nothing flies in as you scroll. There is no text that fades up when you reach
> it, no image that slides across, no background that changes colour as you pass.
> The whole page is simply there, and you move down it.
>
> That was not a guess. The measuring tool photographed every page at nine
> different scroll positions and compared them, looking for anything that shifted
> or faded as a result of scrolling. Across six pages and three screen sizes it
> found precisely nothing, other than the announcement strip carrying on with its
> own timer.
>
> This is worth stating plainly because building it the other way is the default
> instinct, and it would produce a slower, busier site that is not this one.
>
> Two things do glide. Two rows of customer cards drift sideways forever near the
> bottom of the home page, in opposite directions, and they use the same
> two-copies trick as the statistics column so the loop never shows a seam. Their
> exact speed could not be measured and had to be worked out from the card sizes,
> so expect that one to need an adjustment by eye.
>
> The bar along the top stays with you as you scroll, gaining a soft shadow once
> it lifts off the page.

---

## 8. The site search surface

The dominant technical surface of this site, and the product demonstration
described in Section 1.1. It is specified in more detail than any other
component because it is the one component whose failure invalidates the page it
sits on.

### 8.1 What it is

A search over the company's own material: documentation, support articles, blog
posts, website pages, developer content, resources, academy courses and customer
stories. It opens from the header field on every route with chrome, and from the
body of the error route.

It has two modes: a results mode showing ranked hits with facets, and a
conversational mode that answers a question in prose. The mode toggle is visible
in the field itself.

**Capability requirement - normative.** The overlay must issue a query per
keystroke against a real index, render grouped facet counts, render highlighted
hits, load further pages without a navigation, and hand a question to the
answering pipeline of Section 25.4 when the conversational mode is active.

**Observed implementation - informational.** The reference uses that company's
own hosted search, loaded as a client library, established at ledger tier 1 from
a licence banner carrying version `4.79.0`, alongside an autocomplete library
whose design tokens are enumerated in Section 8.6. A second library at version
`10.2.0` provides the custom select controls. None of these are requirements.

### 8.2 The trigger

| Context | Trigger |
|---|---|
| Desktop, chrome routes | the header pill of Section 5.3, placeholder `Search or Ask AI` |
| Below `1024px` | a circular icon button in the header |
| Error route | a labelled field reading `Search <BRAND>` |
| Customers route | the placeholder is `Search <BRAND>` rather than `Search or Ask AI` |

The placeholder itself animates: a rotating message element carries
`How can I help you?` and cycles, and the `caret` keyframe of Section 6.2 blinks
a text cursor beside it. The rotation makes the field read as a prompt rather
than as a box.

### 8.3 The overlay

| Property | Value |
|---|---|
| Layer | `z-index: 999`, below the consent surface and above everything else the build owns |
| Panel maximum height | `650px` |
| Detached modal maximum width | `680px` |
| Detached modal maximum height | `500px` |
| Detached threshold | `max-width: 680px`, below which the overlay becomes a full modal |
| Field height | `44px` |
| Panel shadow | `0 0 0 1px rgba(35,38,59,0.1), 0 6px 16px -4px rgba(35,38,59,0.15)` |
| Scrim | `rgba(115, 114, 129, 0.4)` |
| Scrollbar width inside the panel | `13px` |

### 8.4 The results mode

Three regions, top to bottom.

**Filter by source.** A heading reading `Filter by source`, then a refinement
list with counts. The eight sources and their measured counts at capture time:

| Source | Count |
|---|---|
| `Documentation` | 4,365 |
| `Support` | 1,702 |
| `Blog` | 945 |
| `Website` | 476 |
| `Developers` | 288 |
| `Resources` | 281 |
| `Academy` | 145 |
| `Customer Stories` | 84 |

Those counts are content and will differ in any real build. What is normative is
that the counts are **present, disjunctive and live**: selecting `Blog` must not
send the other seven to zero, which is exactly the requirement in Section 23.4
and the reason that section exists. This component is where the site
demonstrates the behaviour the product sells, and getting it wrong here is
visible on the home page.

**Suggested questions.** Four rows, each with a leading sparkle glyph, each a
full question rather than a keyword:

- `How will <BRAND> improve our search experience and conversions?`
- `How do I integrate <BRAND> search into my app?`
- `Can <BRAND> help shoppers find products faster and increase sales?`
- `Will <BRAND> scale with our traffic and data size?`

**Suggestions.** A heading reading `Suggestions`, then four keyword buttons:
`<BRAND> API integration`, `<BRAND> search benefits`, `<BRAND> scalability`,
`AI search for ecommerce`.

**Products and resources.** A heading reading `Products & Resources`, then hit
rows. Each row carries a title, a meta line of the form `Website • products`,
and a call to action reading `Learn more →`. Below the rows, a button reading
`Show more results` loads the next page in place.

### 8.5 The conversational mode

Toggled by a control in the field labelled `AI mode` with a sparkle glyph. The
panel then carries:

| Element | Copy |
|---|---|
| Brand glyph and title | `<ASSIST_PRODUCT>` |
| Action | `New chat` |
| Action | `Back to results` |
| Attribution | `AI powered by <BRAND>` |

`Back to results` is the important one: the conversational mode is a layer over
the results, not a replacement for them, and the results are still there when
the answer is not useful. This is the same fallback the answer pipeline requires
in Section 25.4 step 4, expressed in the interface.

### 8.6 Overlay design tokens

The overlay carries its own token set, measured from the computed root. They are
listed in full because the overlay's appearance is entirely determined by them
and none of them are in the site's own token set.

| Token | Value |
|---|---|
| `--aa-base-unit` | `16` |
| `--aa-spacing` | `calc(16*1*1px)` |
| `--aa-spacing-factor` | `1` |
| `--aa-base-z-index` | `9999` |
| `--aa-font-size` | `calc(16*1px)` |
| `--aa-font-weight-medium` | `500` |
| `--aa-font-weight-semibold` | `600` |
| `--aa-font-weight-bold` | `700` |
| `--aa-icon-size` | `20px` |
| `--aa-icon-stroke-width` | `1.6` |
| `--aa-action-icon-size` | `20px` |
| `--aa-input-icon-size` | `20px` |
| `--aa-search-input-height` | `44px` |
| `--aa-panel-max-height` | `650px` |
| `--aa-scrollbar-width` | `13px` |
| `--aa-background-color-rgb` | `255,255,255` |
| `--aa-text-color-rgb` | `38,38,39` |
| `--aa-primary-color-rgb` | `62,52,211` |
| `--aa-muted-color-rgb` | `128,126,163`, alpha `0.6` |
| `--aa-icon-color-rgb` | `119,119,163` |
| `--aa-input-border-color-rgb` | `128,126,163`, alpha `0.8` |
| `--aa-panel-border-color-rgb` | `128,126,163`, alpha `0.3` |
| `--aa-selected-color-rgb` | `179,173,214`, alpha `0.205` |
| `--aa-description-highlight-background-color-rgb` | `245,223,77`, alpha `0.5` |
| `--aa-overlay-color-rgb` | `115,114,129`, alpha `0.4` |
| `--aa-scrollbar-thumb-background-color-rgb` | `255,255,255` |
| `--aa-scrollbar-track-background-color-rgb` | `234,234,234` |

Two of these deserve a note. The primary colour `rgb(62, 52, 211)` is **not**
the site's brand blue; the overlay ships with its own violet-leaning primary and
the reference did not override it. And the highlight background
`rgb(245, 223, 77)` at half alpha is the yellow behind matched words, which is
the only yellow anywhere in the design.

**Normative for this build:** override the primary to `#003dff` so the overlay
belongs to the site, and keep the highlight yellow, which does its job and has
no substitute in the site's own palette.

### 8.7 Keyboard and announcement

Specified in Section 31.2. It is not optional and it is not a later pass: a
search field that cannot be driven from the keyboard fails the product's own
argument.

### 8.8 What it must be wired to

| Interface element | Backend contract |
|---|---|
| Every keystroke | a search request, Section 22.13 |
| The source list with counts | disjunctive facet counting, Section 23.4 |
| Highlighted words in a hit | the highlight contract, Section 22.11 |
| `Show more results` | pagination, Section 22.12 |
| A click on a hit | an interaction event carrying the query identity, Section 27.2 |
| The conversational mode | the answer pipeline, Section 25.4 |
| The typed suggestions | query suggestions built from the analytics rollups, Section 27.4 |

The second and last rows are the two that make this a demonstration rather than
a decoration. Counts that behave correctly when two sources are selected, and
suggestions derived from what people actually searched for, are both things a
visitor can verify in ten seconds.

> **In plain language.** The search box at the top of the page is the product,
> running.
>
> Click it and a panel opens. Down one side is a list of the kinds of material it
> covers, each with a number beside it: several thousand pages of documentation,
> a couple of thousand support articles, a few hundred blog posts, and so on. Type
> and the results appear as you type, with the words you typed picked out in
> yellow.
>
> There is a switch in the box that changes it from finding things to answering
> things. In that mode you can type a whole question, in a sentence, and get a
> written answer. There is a button to go back to the ordinary list of results,
> and that button is more important than it looks: the written answer is a layer
> on top of the results, never a replacement for them, so when it is not useful
> you have lost nothing.
>
> Two behaviours in here are the whole sales pitch, and both are checkable by a
> visitor in about ten seconds.
>
> The first: tick one of those categories, and the numbers beside the others must
> stay honest rather than dropping to zero. That is the single most commonly
> mis-built behaviour in search, it has a whole section of this document devoted
> to it, and here it is on the front page where anyone can try it.
>
> The second: the suggested searches offered before you type anything should come
> from what people really searched for, not from a list somebody wrote once.
>
> One curiosity from the measurements. The panel ships with a violet accent of its
> own that the original site never got around to overriding, so the search panel
> is very slightly a different brand from the page around it. This build overrides
> it. The yellow behind matched words stays, because nothing else in the palette
> does that job.

---
## 9. Route: Home

Full chrome, page type `marketing`, `3910px` of scroll past the fold at
`1440px`. Eight bands, alternating dark and light with hard horizontal edges.

### 9.1 Band order

| Band | Ground | Contents |
|---|---|---|
| 1 | `#000033` | hero: display heading, lead, one button, rotating product panel |
| 2 | `#f3f3f3` | use cases: a product screenshot beside an accordion |
| 3 | `#000033` | analyst recognition, a five-panel carousel over a particle field |
| 4 | `#ffffff` | solutions: a heading over a photograph with five overlapping cards |
| 5 | `#f3f3f3` | customer success: two horizontal marquee rows of logo cards |
| 6 | `#f3f3f3` | one centred button, `View all customer stories` |
| 7 | `#000033` | closing call to action, two buttons |
| 8 | `#000033` | footer, Section 5.7 |

### 9.2 The hero

Left column, at `1440px`: a display heading over three lines, the lead, and one
primary button.

| Element | Copy | Type |
|---|---|---|
| Heading | `Agentic.` / `Generative.` / `Search` followed by a prompt glyph | Sora 700, `76px` at `76px` |
| Lead | `One AI retrieval platform to power them all` | Inter 400, `20px` at `28px` |
| Button | `Explore the platform` | primary, Section 5.6 |

The heading's third line ends with a terminal prompt glyph, drawn as a chevron
and an underscore in `#457aff` and a cyan-leaning tint. It is inline geometry,
not a font character.

Right column: a rotating product panel showing the product in use, with a person
holding a device, a conversational query bubble, an answer bubble and three
result cards. Three panels rotate:

| Panel | Eyebrow | Demonstrates |
|---|---|---|
| 1 | `Generative` over `EXPERIENCES` | a natural-language trip query and a written answer |
| 2 | `Search` over `EXPERIENCES` | a keyword query and a grid of product cards |
| 3 | `Agentic` over `EXPERIENCES` | an agent completing a task |

Rotation is the `6500ms` timer of Section 6.6, with three dots below, the active
one filling left to right. Below `1024px` the two columns stack, the heading
centres, and the panel sits beneath the button.

The panel is a **composition of live interface elements over a photograph**, not
a flat image. Section 33.4 gives the procedural substitute for the photograph
and specifies that the interface elements are built, not drawn.

### 9.3 Use cases

Heading `Powering AI retrieval across use cases` centred, Sora 700, with a lead
below it in Inter 400 `20px`: `More than 18,000 customers across 150+ countries
use <BRAND> to power agentic, generative, and search experiences across these
use cases and more.`

Below, a two-column layout: a browser-framed product screenshot on the left,
and an accordion on the right.

### 9.4 The capability accordion

Four items. The first is open on load.

| Item | State on load | Body |
|---|---|---|
| `AI mode search bar` | open | `Customers can use natural language in the search bar and AI recognizes intent to guide their discovery.` with a `Learn more` link |
| `Generative AI` | closed | - |
| `Agentic commerce` | closed | - |
| `Merchandising` | closed | - |

| Property | Value |
|---|---|
| Heading type | Sora 600, `24px` |
| Open item heading colour | `#003dff` |
| Closed item heading colour | `#23263b` |
| Divider | `1px` in `#e5e5e5` between items |
| Caret | Section 4.5, `opacity: 0` at rest, `300ms` transition on open |
| Body transition | `max-height 0.3s ease-out, margin-top 0.3s ease-out, opacity 0.3s ease-out` |

Opening an item changes the screenshot on the left. The two are bound: the
accordion is a tab set wearing an accordion's clothes, and only one item is open
at a time.

Below the accordion, a primary button reading `See more capabilities`, centred
in its own light band.

### 9.5 Analyst recognition

Ground `#000033` with a field of small blurred light points. Five panels
rotate, five dots below.

Left column: an eyebrow in all caps at `10px` 700 reading
`<ANALYST_REPORT_EYEBROW>`, a display heading, a paragraph, and two buttons,
`Read the announcement` primary and `See <BRAND> in action` secondary.

Right column: a card with a gradient ground and a title set in Sora 700 over
five lines, carrying the brand mark and the analyst firm's mark at its foot.

Measured copy for the first panel, with the analyst firm replaced per
Section 0.3:

- Eyebrow: `NORTHGATE RESEARCH 2026 QUADRANT FOR SEARCH AND PRODUCT DISCOVERY`
- Heading: `A leader for the third consecutive year`
- Body: `<BRAND> is recognized as a Leader in the 2026 Northgate Research
  Quadrant for Search and Product Discovery as the market shifts toward
  AI-powered, agentic discovery.`

### 9.6 Solutions

Ground `#ffffff`. A photograph occupies the left two thirds, bleeding to the
edge. Over it, right-aligned, a heading `Solutions that fulfill your business
goals` in Sora 700 and a lead `Here are just some of the ways <BRAND>
technology provides value from day 1.`

Below and overlapping the photograph's lower edge, five cards in a row, each
`#ffffff` with a `1px` `#e5e5e5` border, no radius on the reference, carrying a
title in `#003dff` Sora 600 and a body in Inter 400 `16px` at `24px`:

| Card | Title | Body |
|---|---|---|
| 1 | `Quickly surface the right content` | `Your customers get relevant results to find precisely what they're looking for - in milliseconds.` |
| 2 | `Understand user intent` | `AI algorithms are used to predict and show results from the most likely category of content in your index.` |
| 3 | `Confidently launch agentic experiences` | `Deliver secure, production-ready agentic capabilities to your shoppers with brand and pricing certainty.` |
| 4 | `Personalize for more engagement` | `Build unique visitor journeys that lead your customers to convert over and over again.` |
| 5 | `Create buying urgency` | `<BRAND> AI is always learning what drives conversion and reranks content to push better outcomes.` |

The first card sits higher than the other four and carries a two-colour bottom
border, blue to violet. The vertical stagger is measured and is the band's only
ornament.

### 9.7 Customer success

Heading `See customer success in action` centred in Sora 700, lead
`Discover how your peers have been succeeding with <BRAND>` below it.

Two horizontal rows of cards, each card a photograph with a customer wordmark
knocked out in white over it, `4px` radius, roughly `310 x 214` at `1440px`.
The rows are offset from each other by roughly half a card and drift in opposite
directions, per Section 7.4.

Below, a centred primary button reading `View all customer stories`, linking to
the route in Section 12.

### 9.8 Closing call to action

Ground `#000033` with the same light-point field as Section 9.5. One centred
heading in Sora 700 at `45px`, reading `Harness the power of goal driven AI
search with <BRAND>`, and two buttons below it: `Get Started` primary and
`Get a demo` secondary, the second linking to the route in Section 13.

> **In plain language.** The home page is eight stripes, alternating near-black
> and near-white, with a hard straight edge between each one.
>
> The top stripe is the argument in three words, each on its own line and set
> enormous: agentic, generative, search. Beside it, a panel shows the product
> being used by a real person, and it changes every six and a half seconds
> between three demonstrations: asking a question in a sentence, searching with
> keywords, and letting the software complete a task on your behalf. A dot
> underneath fills up like a slow progress bar so you know when it will move on.
>
> The second stripe pairs a picture of the product with a short list you can open
> one item at a time. Opening an item changes the picture. It behaves like a list
> and works like a set of tabs.
>
> The third is the awards stripe, dark again, with a rotating set of five
> recognitions.
>
> The fourth is the only stripe with a large photograph: a person at a desk, with
> five cards of benefits overlapping its bottom edge. The first card sits slightly
> higher than the other four and has a coloured line under it. That small
> unevenness is the only decoration in the entire band, and it is deliberate.
>
> Then two rows of customer logos drifting slowly in opposite directions, a button
> to see them all, and a final dark stripe with the closing pitch and two buttons.

---

## 10. Route: Pricing

Full chrome, page type `commercial`, `3450px` of scroll past the fold.

### 10.1 Band order

| Band | Ground | Contents |
|---|---|---|
| 1 | gradient over `#000033` | hero, plan chooser, four plan cards |
| 2 | `#000033` | one link, `See full features grid` with a downward arrow |
| 3 | `#ffffff` | the comparison grid |
| 4 | `#f3f3f3` | pricing questions, an accordion |
| 5 | `#000033` | closing call to action, footer |

### 10.2 Hero

| Element | Copy | Type |
|---|---|---|
| Heading | `Scalable pricing for smarter search` | Sora 700, `76px` at `76px` |
| Lead | `Powering the world's best AI experiences - start for free, grow seamlessly and upgrade anytime` | Inter 400, `20px` at `28px`, centred over two lines |
| Chooser | `Help me choose a plan` | secondary button, `9999px` radius |
| Chooser caption | `Answer 3 quick questions to see which plan fits best.` | Inter 400, `13px` |

The hero ground is a wide gradient from a violet-leaning dark at the left to a
teal-leaning dark at the right, over `#000033`.

### 10.3 Plan cards

Four cards in one row at `1440px`, in two groups.

| Group heading | Cards |
|---|---|
| `Annual plan` | `Elevate` |
| `Pay as you go` | `Grow Plus`, `Grow`, `Free` |

| Field | Detail |
|---|---|
| Plan name | Sora 700, `45px` |
| Badge | `NEW` beside `Grow Plus`, all caps `10px` 700, in a light green |
| Subtitle | one line, Inter 400 `16px`, for example `Enterprise-scale AI Search`, `Keyword search with AI`, `Keyword search`, `Search and recommendations` |
| Action | `Start for free` or `Build for free` or `Request pricing`, secondary button on the dark card |
| Metering | two or three lines of Inter 400 `14px` at `20px` |

Measured metering copy for `Grow`: `10K search requests /month included then
$0.50 per additional 1K search requests` and `100K records included then $0.40`.
For `Free`: `Get started building experiences ever with some of our features.`
and `No credit card required.`

The `Grow Plus` card is emphasized: it carries a lighter gradient ground and a
`1px` border in `#457aff` where the others carry `#484c7a`.

### 10.4 The comparison grid

Heading `Detailed feature comparison` in Sora 700, centred, on `#ffffff`.

**Structure.** A left rail of category anchors, and a four-column table.

Category rail, measured: `Search`, `Analytics`, `UI Components`,
`Integrations & Data`, `Crawler`, `Infrastructure & Plan Limits`,
`Support & Success`. Each is a link that scrolls its group into view. The
active category is `#003dff` and bold; the others are `#23263b`.

Table columns: a feature name column, then `Free`, `Grow`, `Grow Plus`,
`Elevate`. Each plan header carries the plan name in Sora 700 `24px` and an
action link below it: `Get started` for the first three and `Request pricing`
for the fourth.

**The header row is sticky at `z-index: 3`** while the body scrolls, which is
the second sticky element on the site and the reason Section 7.3 exists. Without
it the grid is unreadable past its first screenful.

**Cells** carry one of three things:

| Cell content | Rendering |
|---|---|
| Feature present | the check glyph of Section 4.7 in `#003dff` |
| Feature absent | the cross glyph of Section 4.6 in `#c9c9c9` |
| A limit | text, for example `10 per index` or `10,000 per index`, Inter 400 `16px` |

Feature names carry the tooltip glyph of Section 4.7 where a footnote exists.
Measured rows include `Rules`, `Visual Editor`, `Manual Synonyms`,
`Virtual Replicas (Relevant Sort)`, `AI Synonyms` and `Query Categorization`,
each of which maps to a capability specified in Sections 21 to 28. The mapping
is given in Section 35.5, because a comparison grid whose rows do not correspond
to anything in the build is the most easily overlooked inconsistency in this
document.

Row striping alternates `#ffffff` and `#f9f9f9`. Column separators are `1px` in
`#e5e5e5`.

### 10.5 Pricing questions

An accordion on `#f3f3f3`, headed `Pricing FAQs` in Sora 700. First measured
question: `What is a search request?`. Same accordion mechanics as Section 9.4,
with the wide chevron of Section 4.5 rather than the caret.

> **In plain language.** The pricing page is a dark top half and a light bottom
> half.
>
> The top half is four plans side by side: a free one, two you pay for as you go,
> and one you have to ask about. The middle one is marked as new and is visually
> pushed forward with a lighter background and a brighter edge. Above them all
> there is a button offering to pick a plan for you after three questions, which
> is the honest acknowledgement that four columns of features is a lot to read.
>
> The bottom half is those four columns of features, in full, as a long table.
> Down the left there is a list of categories you can jump to. The important
> mechanical detail is that the row of plan names stays stuck to the top of the
> screen while the table scrolls underneath it. Without that, you are forty rows
> down a table with four unlabelled columns of ticks, and the page is useless.
>
> Each row is either a tick, a cross, or a number such as "ten per index". Some
> rows have a small circled letter beside them that explains the term when you
> hover it.
>
> One thing this document does that the original page does not: every feature
> named in that table is cross-referenced to the part of the specification that
> actually builds it. A comparison table listing things the product does not have
> is the easiest inconsistency in the world to ship and one of the most damaging.

---

## 11. Route: Products

Full chrome, page type `marketing`, `7939px` of scroll past the fold, roughly
nine screens, the longest route on the site.

### 11.1 Structure

| Band | Ground | Contents |
|---|---|---|
| 1 | `#000033` | hero, centred |
| 2 | `#ffffff` | section heading `Make every interaction smarter with AI retrieval` |
| 3 to 6 | `#ffffff` | four alternating feature blocks, image and text |
| 7 | `#ffffff` | a video block with a text column |
| 8 | `#f3f3f3` | `Tools for business users`, a three-column icon grid |
| 9 | `#000033` | closing call to action, footer |

### 11.2 Hero

Centred, three elements over `#000033`:

| Element | Copy | Type |
|---|---|---|
| Eyebrow | `AI PRODUCT OVERVIEW` | Inter 700, `14px` at `16px`, all caps, `#003dff` |
| Heading | `AI search and retrieval` / `that shows users what they need` | Sora 700, `76px` at `76px`, two lines |
| Lead | `Enhance your users' journey with solutions powered by retrieval for searching, browsing, personalization, and recommendations.` | Inter 400, `20px` at `28px` |
| Buttons | `Get a demo` primary, `Start building for free` secondary on white | Section 5.6 |

The hero is `585px` tall and carries no imagery. On a route this long, the
empty hero is doing the work of a chapter break.

### 11.3 The feature blocks

Four blocks, alternating image left and image right. Each carries:

| Element | Type |
|---|---|
| Heading | Sora 700, `45px` |
| Body | Inter 400, `20px` at `28px`, in `#484c7a` |
| Feature list | four rows, each a check glyph in `#003dff`, a bold term, a colon, a description, and a `Learn more` link |
| Button | primary, at the foot of the text column |

Measured content for the first block, `Search experiences`:

| Term | Description |
|---|---|
| `Hybrid Search` | `Semantic vector search meets keyword precision for fast, intuitive results that match user intent.` |
| `AI Ranking` | `Machine learning that optimizes relevance while preserving human control.` |
| `Query Categorization` | `Turn unstructured queries into structured data for smarter merchandising and analytics.` |
| `Advanced Personalization` | `Reflect each user's behavior, preferences, and context, out of the box.` |

Those four terms are, in order, Sections 25.3, 22.5 with 24.3, a capability
recorded in Section 35.5, and Section 24.3. The route is a table of contents for
the second half of this document, and building it without building them produces
a page of claims.

The block's image is a composed interface over a photograph, as in Section 9.2:
a product grid, a floating query bubble with a microphone glyph, and price and
swatch details. Section 33.4 covers the substitution.

### 11.4 The video block

A video thumbnail on the left, a text column on the right ending in a primary
button reading `Book a live demo with our product experts`.

The reference embeds a third-party player. **Normative for this build:** the
video is a first-party element with a poster generated per Section 33.5, native
controls, no autoplay, and captions. A build that embeds a third-party player
here has added a tracking dependency to a page that otherwise has none.

### 11.5 Tools for business users

Ground `#f3f3f3`. Heading in Sora 700, centred. A three-column grid, each
column carrying a line-drawn icon at roughly `96 x 96` in `#003dff`, a title in
Sora 600 `24px`, and a body in Inter 400.

Measured icons: a shopping trolley, a bar chart, and a third not resolved in the
capture. Both resolved icons are stroke-only line drawings at a `2px` weight
and are inline geometry per Section 4.

> **In plain language.** The products page is the long one, about nine screens.
>
> It opens with nothing but words on a dark ground: a small blue label, a very
> large two-line headline, a sentence, and two buttons. No picture at all. On a
> page this long that emptiness is doing a job, the way a blank page does at the
> start of a chapter.
>
> Then four long blocks, alternating left and right, each pairing a picture of the
> product with four short capability lines. Each line is a bold term, a plain
> explanation, and a link.
>
> Those four terms in the first block are worth noticing, because they are exactly
> the four hardest things in the second half of this document: combining
> word-matching with meaning-matching, ordering results, understanding what kind
> of thing you asked for, and adapting to the person. This page is effectively the
> contents page for the engine, and building the page without building the engine
> produces four claims and no product.
>
> Near the bottom there is a video. The original page hands that off to a
> third-party player, which quietly brings tracking with it. This build hosts its
> own, with captions, and does not start playing on its own.

---

## 12. Route: Customers

Full chrome, page type `index`, `2332px` of scroll past the fold. The only
captured route with a light header on load, and the only one that is itself a
faceted search interface.

### 12.1 Structure

| Band | Contents |
|---|---|
| 1 | a search field, full width |
| 2 | five facet controls in a row |
| 3 | a three-column card grid |
| 4 | pagination or progressive loading |
| 5 | closing call to action, footer |

### 12.2 The search field

Full width of the content measure, `1px` border in `#e5e5e5`, `4px` radius,
roughly `88px` tall, with the search glyph of Section 4.2 at `24 x 24` inset
`36px` from the left and the placeholder `Search for a customer story` in Inter
400 `24px` in `#484c7a`.

It is a large, quiet field, and its size is the route's main visual gesture.

### 12.3 The facet controls

Five, in a row, each a bordered box with a label and the wide chevron of
Section 4.5:

| Control | Kind |
|---|---|
| `Features` | multi-select |
| `Use Case` | multi-select |
| `Industry` | multi-select |
| `Region` | multi-select |
| `Integration` | multi-select |

**Every one of them is multi-select, and this is the single most important
behavioural requirement on this route.** Five multi-select facet groups is
exactly the configuration that makes disjunctive facet counting mandatory: tick
two industries and the counts on the other four groups must recompute against a
filter tree that keeps industry's own selection out of industry's own counts.
Section 23.4 specifies it, Section 30.4 tests it, and this page is where a
visitor sees whether it was done.

The controls emit the nested array form of Section 23.2. A `Clear All Filters`
link appears once any facet is active.

The reference's controls are supplied by a custom select library at version
`10.2.0`, ledger tier 1. That is informational; the requirement is a
keyboard-operable multi-select listbox per Section 31.2.

### 12.4 Story cards

Three columns at `1440px`, two at tablet, one at mobile.

| Element | Detail |
|---|---|
| Image | a photograph with the customer's wordmark knocked out in white, roughly `368 x 316`, `4px` radius |
| Category | Inter 400 `16px` in `#003dff`, for example `Ecommerce` |
| Title | Sora 400 `24px` at `32px` in `#23263b`, truncated to three lines with an ellipsis |
| Rule | `1px` `#e5e5e5` below each card |

Measured hover, on this route only: the card's control moves from
`rgb(35, 38, 59)` to `rgb(0, 61, 255)`, and both pseudo-elements move with it.

### 12.5 Loading more

The reference loads further results in place rather than paginating. The
measured control is a button reading `Show more results`, shared with the search
overlay of Section 8.4.

**Normative:** progressive loading must not break the back button, must not lose
scroll position on return, and must announce the number of new results to
assistive technology per Section 31.2.

> **In plain language.** This page is a small search engine of its own, and it is
> the best place on the site to check whether the filtering was built properly.
>
> At the top, one very large, very quiet search box. Under it, five dropdown
> filters: features, use case, industry, region and integration. Under those, a
> grid of customer stories, each one a photograph with the customer's name across
> it.
>
> Here is the check. Every one of those five filters lets you pick more than one
> thing at a time. Pick two industries. The counts on the other four filters have
> to stay truthful, and the industry filter has to keep offering you the
> industries you have not picked yet. That is the behaviour the whole company
> sells, it is genuinely hard to build, it is described at length in the filtering
> section of this document, and this is the page where any visitor can try it in
> ten seconds.
>
> More stories load in place as you reach the bottom rather than sending you to a
> page two. Three things must survive that: the back button, your place on the
> page when you return, and telling someone using a screen reader that new
> results have arrived.

---

## 13. Route: Demo request

**No chrome.** No promotion bar, no header, no footer. Page type `capture`.
`144px` of scroll past the fold at `1440px`, which is to say it is one screen
with a small overflow.

This is the route that touches state, and it is the site's conversion target.

### 13.1 Ground and layout

A single full-viewport ground: a wide gradient running violet at the left
through blue at the right over `#000033`, with a soft magenta bloom at roughly
one third across.

Two columns. Left: the mark, the heading, the lead, and the form. Right: proof.

### 13.2 The left column

| Element | Copy | Type |
|---|---|---|
| Mark | Section 4.1, at `24 x 24` with the wordmark | - |
| Heading | `Fix your search experience` | Sora 700, `56px` at `1.2` |
| Lead | `Struggling with relevance, slow results, or limited control? We'll show you how to improve search performance and conversions - fast.` | Inter 400, `20px` at `28px`, `#d6d6e7` |

### 13.3 The form

Six fields in a two-column grid, then the submit.

| Field | Type | Required |
|---|---|---|
| `First Name` | text | yes |
| `Last Name` | text | yes |
| `Business Email` | email | yes |
| `Phone` | tel | yes |
| `Company` | text | yes |
| `Country` | select | yes |

Every label is preceded by a required marker rendered as a red asterisk in its
own element, and every label is visible and persistent, never a placeholder.

Field styling: fill `#ffffff`, radius `4px`, height `40px`, no visible border,
label above in Inter 400 `14px` in `#ffffff`.

The `Country` select carries a full country list beginning `Select...`, then
`United States`, then every country alphabetically from `Afghanistan`. The
reference uses the custom select library named in Section 12.3.

Submit: a button reading `Get In Touch`, styled per the form submit variant in
Section 5.6, with its measured hover.

**Contract.**

```
POST <FORM_ENDPOINT>
  { firstName, lastName, email, phone, company, country }
  -> 200 { ok: true }
  -> 4xx { ok: false, message: string, field?: string }
```

Three states, all pre-rendered and toggled rather than fetched: idle, success
and failure. Validation runs on blur and again on submit, and the error summary
requirement in Section 31.7 applies.

### 13.4 The right column

Two very large statistics with gradient-filled numerals, then a trust panel.

| Element | Copy | Type |
|---|---|---|
| Statistic 1 | `18,000+` with `global brands served` beside it | Sora 700, roughly `76px`, gradient fill per Section 3.9 |
| Statistic 2 | `9.3 Billion` with `Single-day searches` beside it | as above |

The gradient fill is
`linear-gradient(to right, rgb(30, 89, 255) 0%, rgb(187, 209, 255) 100%)`
clipped to the text, which is the 36-use gradient in Section 3.9 and the only
place on the site where type is filled with a gradient rather than a colour.

Below, a panel on a translucent dark fill with a `1px` `#484c7a` border, two
rows:

| Row | Glyph | Content |
|---|---|---|
| 1 | shield | `Trusted by 18,000+ businesses` then five customer wordmarks |
| 2 | padlock | `Enterprise-grade security & data privacy` then five compliance badges in bordered pills |

The compliance badges are text in `10px` 700 inside `1px` bordered pills with a
`4px` radius. They are text, not images, which is what makes them substitutable
without loss.

### 13.5 The statistics column

The one scroll-driven element on this route, per Section 7.1: a column running
the `scrollUp` loop of Section 6.5 at `21600ms` and a second at
`30933.333333333332ms`, with the top edge masked by the gradient in
Section 3.9.

> **In plain language.** This is the page where somebody actually asks for a
> demonstration, and it is built to make that the only thing you can do.
>
> There is no navigation, no footer, and no links out. Just a wide sweep of
> violet and blue, a headline, six boxes to fill in, and a button.
>
> Beside the form there is the reassurance: two enormous numbers, the count of
> businesses served and the number of searches handled in a single day, with the
> digits filled with a left-to-right blue wash rather than a flat colour. That
> wash appears nowhere else on the site. Under the numbers, a small panel with a
> row of customer names and a row of security certifications, both set as plain
> text in little outlined pills rather than as pictures, which is why this page
> can ship without a single image.
>
> Every one of the six fields is required and every one has a permanent label
> above it rather than a grey hint inside it that vanishes when you start typing.
> That is a small thing that matters enormously to anybody filling in a form on a
> phone.

---

## 14. Route: Not found

**No chrome.** Page type `error`. Exactly one screen, no scroll.

### 14.1 Ground

`radial-gradient(100% 100% at 100% 0%, rgb(0, 0, 51) 0%, rgb(0, 0, 51) 100%)`,
which is a radial gradient between two identical stops, that is a flat
`#000033`. It is quoted as measured because the declaration is what is in the
stylesheet, and a build that simplifies it to a flat fill is correct and should
record the simplification.

### 14.2 Contents

Centred, vertically and horizontally:

| Element | Detail |
|---|---|
| Numeral | `404`, very large, with the brand mark substituted for the zero |
| Heading | `Page not found`, Sora 700, `45px` rising to `56px` above the large breakpoint, line height `1.2` |
| Search | a field labelled `Search <BRAND>`, opening the overlay of Section 8 |
| Links | three, each with the circle-arrow of Section 4.3: `API Status`, `Home page`, `Support` |

### 14.3 The heading treatment

Both the numeral and the heading carry:

| Property | Value |
|---|---|
| Fill | `radial-gradient(75.93% 75.93% at 48.86% 10.98%, rgb(7, 56, 210) 0%, rgb(14, 41, 126) 100%)` clipped to the text |
| Filter | `drop-shadow(rgb(12, 21, 54) 0px 54px 54px) drop-shadow(rgba(0, 0, 0, 0.6) 0px 16px 14px)` |

Two stacked drop shadows: one very large and soft at `54px` in every direction,
one tight at `16px` down with a `14px` blur. The effect is type that sits above
the ground rather than on it, and it is the only place on the site where type is
given depth.

### 14.4 Behaviour

Measured hover: the search affordance's background moves from `rgb(0, 0, 51)` to
`rgb(4, 32, 119)`.

**Normative:** this route is served for every unmatched path with a 404 status
code, not a 200. A soft 404 is the most common error-page defect and it is
invisible to everyone except a search crawler.

> **In plain language.** The page you land on when an address is wrong. One
> screen, nothing else on it.
>
> A giant `404` with the company's own mark standing in for the zero, the words
> "page not found" underneath, a search box, and three ways out: the service
> status page, the home page, and support.
>
> The type is the interesting part. Both the numeral and the heading are filled
> with a soft blue-to-darker-blue wash rather than a flat colour, and they carry
> two shadows at once, one enormous and soft and one tight underneath. The effect
> is that the text floats a little way above the background. It is the only place
> on the whole site where anything is given depth like that, which is a nice thing
> to do on the one page nobody meant to visit.
>
> One requirement that has nothing to do with looks: this page must tell the
> browser it is an error, not just look like one. Getting that wrong is invisible
> to people and very visible to search engines.

---

## 15. Forms and input controls

Specified once, used by the demo request route, the newsletter, the facet
controls on the customers route and every field in the console.

### 15.1 The field

| Property | Value |
|---|---|
| Height | `40px` for text, `44px` for the search pill |
| Radius | `4px`, the most common radius on the site at 117 uses |
| Fill | `#ffffff` |
| Border | none on dark grounds, `1px` `#e5e5e5` on light |
| Label | above the field, always visible, Inter 400 `14px` |
| Required marker | a separate element carrying an asterisk, in red, before the label text |
| Placeholder | never a substitute for a label; used only for format hints |

### 15.2 The select

The reference uses a custom select library, version `10.2.0`, ledger tier 1,
which replaces the native control with a listbox.

**Capability requirement - normative.** A select must: open on Enter, Space or
Down; filter as the user types when it holds more than twenty options; move
selection with the arrow keys; close on Escape returning focus to the trigger;
and expose its state to assistive technology. The country list on the demo
request route is the case that matters, at roughly two hundred and fifty
options.

A native `select` satisfies every one of these and is the correct default. The
custom control is only justified where multi-select with visible chips is
required, which on this site is the five facet controls in Section 12.3.

### 15.3 Validation and states

| State | Behaviour |
|---|---|
| Idle | no error styling, no announcement |
| Invalid on blur | error text below the field, field border in the error colour, error associated with the field |
| Invalid on submit | as above, plus an error summary above the form with a link to each failing field, focus moved to the summary |
| Submitting | the submit control is disabled and announces that submission is in progress |
| Success | the form is replaced by a success message, focus moved to it |
| Failure | an error message above the form, the form retained with its values intact |

Values must survive a failed submission. A form that clears itself on a server
error has turned a retry into a re-entry, and on the six-field demo request form
that is the difference between a lead and a bounce.

### 15.4 The newsletter

A single email field and a submit, in the footer, on `#000033`. Same three
states, inline rather than replacing the footer.

```
POST <NEWSLETTER_ENDPOINT>
  { email: string }
  -> 200 { ok: true }
  -> 4xx { ok: false, message: string }
```

### 15.5 Autofill and input types

| Field | Input type | Autofill token |
|---|---|---|
| First name | `text` | `given-name` |
| Last name | `text` | `family-name` |
| Business email | `email` | `email` |
| Phone | `tel` | `tel` |
| Company | `text` | `organization` |
| Country | `select` | `country-name` |
| Newsletter email | `email` | `email` |

The input types are not cosmetic: on a phone they choose the keyboard, and a
`text` type on the phone field costs a measurable share of completions.

> **In plain language.** Everything you can type into, in one place.
>
> Boxes are white with slightly rounded corners and a label that stays above them
> permanently. Never the kind that puts the label inside the box in grey and makes
> it disappear the moment you start typing, which leaves you halfway through a
> form with six identical boxes and no idea which is which.
>
> If you get something wrong, you are told next to the field, and if you try to
> submit with several things wrong, you get a short list at the top with a link to
> each one.
>
> One rule matters more than it sounds. If the submission fails at the far end,
> everything you typed stays exactly where it was. A form that empties itself when
> the server hiccups has turned "press it again" into "type it all again", and
> most people simply leave.
>
> Small thing, real money: the phone field has to be marked as a phone field, so
> a phone shows a number pad rather than a full keyboard.

---
## 16. The application console

### 16.1 What it is, and why it is in this document

A signed-in surface at `/console`, behind the same design system as the
marketing routes, where a customer configures the service specified in
Sections 20 to 28. It is a **specified extension** and was not captured; the
reference site keeps its console on a separate origin that was out of scope.

It is here because without it the backend has no operator. Every control in
Sections 21 to 28 that a human is expected to tune, relevance, synonyms, rules,
keys, has to be tunable by that human, and a specification that stops at the
service leaves the most consequential half of the product as an implied
afterthought.

Everything in this section is normative. Colour, type and spacing come from the
token set in Section 3.2 unchanged: the console is the same brand, at a higher
information density.

### 16.2 Shell and navigation

```
/console                              application picker, then redirect
/console/<APP>/indices                index list
/console/<APP>/indices/<INDEX>        record browser, the default tab
/console/<APP>/indices/<INDEX>/configure
/console/<APP>/indices/<INDEX>/rules
/console/<APP>/indices/<INDEX>/synonyms
/console/<APP>/indices/<INDEX>/preview
/console/<APP>/analytics
/console/<APP>/ab-tests
/console/<APP>/keys
/console/<APP>/tasks
/console/<APP>/members
```

A left rail carries the application switcher and the eleven destinations. The
top bar carries the index switcher, which is a search over index names using the
product's own engine against a system index, because a customer with 400 indices
has the same problem the product solves.

Every screen that reads data shows, in the same fixed position, the generation it
read and the age of that read. This is not decoration: with the read path in
Section 28.2 being asynchronous, a stale screen is a normal state, and a console
that hides it produces bug reports about writes that "did not happen".

### 16.3 The record browser

A virtualized table over `browse`, not `search`. The distinction is normative:
`browse` walks a stable cursor over the whole index without the pagination cap in
Section 22.12, and using `search` here means the operator cannot reach record
1,001.

| Control | Behaviour |
|---|---|
| Cursor paging | `browse` with `cursor`, forward only, with a visible "start over" |
| Attribute columns | chosen by the operator, persisted per index per member |
| Inline edit | writes a `partialUpdateObject`, shows the returned `taskID`, and polls it |
| Delete | requires typing the `objectID`, because there is no undo |
| JSON view | the raw record, read-only, with a copy control |

The table must render 200 rows without the browser stalling, and must not
re-request on scroll-back. Both are consequences of the same requirement: the
cursor is forward-only, so the console holds the pages it has already fetched.

### 16.4 The search preview

The screen where relevance is judged, and the one the rest of this document
refers to most often. Three panes.

**Left: the query.** A search box, a filter builder, and the parameter
overrides. The filter builder emits the nested array form in Section 23.2 and
renders it back as prose: "brand is Acme or Zeta, and colour is red". Multi-select
groups produce inner arrays, separate groups produce outer entries, and the prose
line is how the operator sees which one they built.

**Centre: the results.** The hit list as the customer's own interface would
receive it, with the position number, the highlight tags rendered, and a
disclosure per hit carrying `_rankingInfo`. The disclosure is the point of the
screen: it shows the eight criteria of Section 22.5 as a row per criterion with
the value for this hit and the value for the hit above it, and marks the
criterion where the two first differed. That single row answers "why is this
above that", which is otherwise unanswerable and is the most common support
request against a search product.

**Right: the facets.** Every attribute in `attributesForFaceting`, each with a
toggle for conjunctive or disjunctive counting, so the operator can see the
difference from Section 23.4 rather than read about it.

The preview must also expose:

- `getRankingInfo` on by default here and off everywhere else.
- The `degraded` flags from Section 28.5, rendered as a visible banner rather
  than as a field in a payload.
- The applied rules from Section 24.2, each linking to its editor.
- A comparison mode: run the same query against two sets of settings side by
  side, with the ordering differences highlighted. This is how a settings change
  is reviewed before it is saved, and without it every relevance change is a
  deploy and a hope.

### 16.5 Analytics

Four screens, all reading the rollup tables in Section 27.4 and never raw
events.

| Screen | Shows | The care needed |
|---|---|---|
| Overview | searches, users, click-through rate, no-results rate, over a date range | the denominators in Section 27.5, stated on the screen next to each figure |
| Top searches | query, count, click-through rate, average click position, no-results rate | normalized query, and the raw variants behind a disclosure |
| No results | queries with `nbHits` 0, with a control that opens the rule editor pre-filled | this is the screen that pays for the product |
| Results insights | per `objectID` impressions, clicks, conversions, mean position | joins to the record browser |

Date ranges are inclusive of both ends and are labelled with the timezone. Every
figure that is a distinct count is marked as approximate, per Section 27.5, in
the figure itself and not in a footnote.

### 16.6 Merchandising

A visual editor over the query rules of Section 24.2. The operator types a
query, sees the live results from the preview engine, and drags a result to a
position. Dragging writes a rule; it does not write a separate pinning object.

| Action | Rule written |
|---|---|
| Drag a hit to position `n` | `promote` with that `objectID` and position `n` |
| Hide a hit | `hide` with that `objectID` |
| Add a banner | `userData` on the consequence |
| Boost a category for this query | `optionalFilters` in `params` |

The editor shows, above the results, the precedence list from Section 24.6 with
the steps that are active for this query highlighted, so an operator whose
promotion is being overridden by a filter can see why without opening a support
ticket.

Rules carry a validity window, and the editor defaults to "starts now, no end"
while making the seasonal case one control away, because the common real use is
a sale that must stop on a date.

### 16.7 Keys and members

Key creation writes the access list, the index patterns, the optional expiry and
the optional query restrictions. The key value is shown once, in a panel that
must be dismissed deliberately, and never again. A "reveal" control is not a
feature to be added later; its absence is the specification.

The screen must also carry the secured-key derivation of Section 26.3 as a
worked example, generated live from the parent key selected, with the resulting
string and the exact steps that produced it, because every customer implements
this and most implement it wrong the first time.

Members have four roles: owner, admin, operator, analyst. The permission matrix
is enforced server side and is displayed on the screen, because a role model
that only exists in the interface is not a role model.

| Capability | owner | admin | operator | analyst |
|---|---|---|---|---|
| Read analytics | yes | yes | yes | yes |
| Edit rules and synonyms | yes | yes | yes | no |
| Edit index settings | yes | yes | yes | no |
| Write records | yes | yes | yes | no |
| Manage keys | yes | yes | no | no |
| Manage members and billing | yes | no | no | no |

### 16.8 Tasks

The write queue of Section 21.7, per index, with `taskID`, kind, status, accept
time and publish time. Failed tasks show their error and the operation that
caused it. This screen exists so that "my update has not appeared" has an answer
that is not a support ticket.

### 16.9 What the console must never do

Stated as prohibitions because each one has a tempting shortcut:

- Never call `waitTask` synchronously inside a form submission. Show the task
  and poll it.
- Never query raw events for a screen. Only rollups.
- Never use `search` where `browse` is specified.
- Never store an admin key in the browser. The console's own session is not an
  application key and must not be one.
- Never display a figure derived from a sketch without marking it approximate.

> **In plain language.** This is the control room: the pages a customer's own
> staff use to shape what their shoppers see.
>
> Most of it is the ordinary furniture of an admin area, a list of your data, a
> place to edit it, a place to manage who can do what. Three parts are worth
> calling out.
>
> The first is the practice search. You type a search the way a shopper would,
> and see exactly what they would see, with one addition: open any result and it
> tells you why it is where it is. It shows the ladder of tie-breaks from the
> ordering section and marks the exact rung where this result beat the one above
> it, or lost to it. Without that, "why is this product third" is unanswerable,
> and it is the question every customer asks in their first week.
>
> The second is the merchandising screen, where somebody who does not write code
> can drag a product to the top of the results for a particular search, or hide
> one, or put a banner above them, for a fortnight in December. What they drag
> becomes an ordinary standing instruction, visible to everyone, rather than a
> secret setting in a second system.
>
> The third is a small piece of honesty. Every screen shows how fresh what you
> are looking at is. Because changes take a moment to spread across machines, a
> screen that is a second out of date is normal, and a control room that hides
> that fact generates a steady trickle of reports about changes that did not
> happen and actually did.

---
## 17. Module and component architecture

### 17.1 Module boundaries

Eleven modules. The boundary rule is that a module may depend on modules above
it in this list and never below.

| Module | Owns | Depends on |
|---|---|---|
| `tokens` | the values in Section 3, as one source | nothing |
| `primitives` | button, field, select, pill, card, rule | `tokens` |
| `icons` | the geometry in Section 4, one component per glyph | `tokens` |
| `chrome` | promotion bar, utility bar, header, panels, drawer, footer | `primitives`, `icons` |
| `motion` | the loop, the carousel timer, the marquee, reduced-motion handling | `tokens` |
| `search-ui` | the overlay of Section 8, modes, facets, hits, assistant | `primitives`, `icons`, `client` |
| `forms` | Section 15, validation, states, submission | `primitives` |
| `routes` | the six route compositions of Sections 9 to 14 | everything above |
| `console` | Section 16 | `primitives`, `icons`, `client` |
| `client` | the transport to the service, retry, host rotation, key handling | nothing but `tokens` |
| `service` | Sections 20 to 28 | nothing in this list |

`client` is deliberately at the bottom with no interface dependencies: it is
imported by both the site and the console, and it is the piece a customer would
also use. Its behaviour is specified in Section 28.4 rather than here, because
it is part of the service's contract rather than the site's.

### 17.2 The components that recur

| Component | Appears in | Variants |
|---|---|---|
| Button | everywhere | primary, secondary, form submit, icon-only |
| Accordion | Sections 9.4, 10.5, 5.5 | bound-to-media, plain, navigation |
| Card | Sections 9.6, 9.7, 10.3, 12.4 | benefit, logo, plan, story |
| Marquee row | Sections 9.7, 13.5 | horizontal, vertical |
| Facet control | Sections 8.4, 12.3, 16.4 | list with counts, dropdown multi-select |
| Statistic | Sections 13.4, and the bars in Section 6.2 | gradient numeral, animated bar |
| Field | Section 15 | text, email, tel, select, search |

The facet control appearing three times, in the search overlay, on the customers
route and in the console, is the load-bearing repetition in this build. All
three render counts, all three must be multi-select, and all three therefore
depend on Section 23.4 being correct. One component, one contract, three places
a defect shows up.

### 17.3 The accordion, specified once

Used three times with different bindings, so it is specified once as a
behaviour and parameterised.

| Parameter | Values |
|---|---|
| `mode` | `single`, only one item open, used in Sections 9.4 and 10.5; `multiple`, used in the mobile drawer |
| `bound` | optional identifier of a media pane whose content follows the open item, used in Section 9.4 |
| `caret` | which glyph from Section 4.5 |
| `initial` | index of the item open on load, or none |

Body transition, measured: `max-height 0.3s ease-out, margin-top 0.3s ease-out,
opacity 0.3s ease-out`. Animating `max-height` requires a known maximum; measure
the content and set it, and re-measure on resize, or the transition truncates
tall panels at the smallest width where it was measured.

### 17.4 The marquee, specified once

| Parameter | Values |
|---|---|
| `axis` | `x` for Section 9.7, `y` for Section 13.5 |
| `pixelsPerSecond` | constant across instances, per Section 6.5 |
| `direction` | forward or reverse |
| `maskFade` | the distance in the gradient of Section 3.9, or none |

Implementation is normative: two copies of the content in one track, translated
by `-50%` on the chosen axis, linear, infinite. Duration is derived from the
content length and the constant speed. A build that sets a duration per instance
will have two rows moving at visibly different speeds.

### 17.5 State that lives outside components

| State | Owner | Persisted |
|---|---|---|
| Consent decision | the consent surface | first-party storage, per its own contract |
| Chosen language | `chrome` | cookie, and reflected in the route |
| Search overlay open | `search-ui` | no, and it must close on route change |
| Facet selections on the customers route | `routes` | the address bar, so a filtered view is linkable |
| Console table columns | `console` | per member, per index, server side |

The fourth row is a requirement rather than a nicety: a faceted index whose
state is not in the address bar cannot be shared, which removes most of the
reason to have built the facets.

> **In plain language.** How the build is divided up so two people can work on it
> without treading on each other.
>
> Eleven parts, stacked. At the bottom, the values: the colours, the sizes, the
> spacings. Above that the small pieces: buttons, boxes, cards. Above that the
> furniture, then the pages. The rule is that a part can use anything below it and
> nothing above it, which is what stops the whole thing turning into a knot.
>
> One piece appears in three different places and is worth watching: the filter
> control with counts beside each option. It is in the search panel at the top of
> every page, on the customer stories page, and in the control room. Same
> component, same contract, three places where a mistake in it becomes visible.
>
> There is also a small list of things that are not owned by any one piece: which
> language you chose, whether you have accepted cookies, and, importantly, which
> filters you have ticked. That last one lives in the web address itself, so that
> a filtered list can be sent to a colleague. Without that, most of the reason to
> have filters at all disappears.

---

## 18. Responsive behaviour

### 18.1 The three captured widths

| Name | Width | Height | What it represents |
|---|---|---|---|
| Desktop | `1440px` | `900px` | the design width |
| Tablet | `990px` | `800px` | deliberately between the `960px` and `1024px` thresholds |
| Mobile | `390px` | `844px` | a current phone |

The tablet width is the awkward one and it is awkward on purpose: Section 3.1
records that two component families are written desktop-first with a
`max-width: 960px` query and the rest are mobile-first with a `min-width: 1024px`
query. At `990px` a component can therefore be in neither branch. Every
component must be checked at exactly `990px`, and Section 36.1 requires it.

### 18.2 What changes, by band

| Element | Desktop | Tablet | Mobile |
|---|---|---|---|
| Header centre and right groups | visible | collapsed | collapsed |
| Logo | mark and wordmark | mark only | mark only |
| Search | pill field | icon button | icon button |
| Hero, Section 9.2 | two columns | stacked, panel below | stacked, heading centred, all three words wrap |
| Capability accordion, Section 9.4 | beside the media pane | below it | below it, media pane above |
| Solutions cards, Section 9.6 | five in a row | two rows | one column |
| Plan cards, Section 10.3 | four in a row | two rows | one column, `Grow Plus` first |
| Comparison grid, Section 10.4 | four plan columns | horizontal scroll inside the grid | one plan column at a time with a plan switcher |
| Story cards, Section 12.4 | three columns | two | one |
| Facet controls, Section 12.3 | five in a row | three then two | a single control opening a full-height sheet |
| Demo request, Section 13 | two columns | stacked, proof below | stacked, statistics reduced to two lines |
| Marquee rows | full bleed | full bleed | full bleed, faster relative travel |

Two of these rows are requirements rather than observations, and both are marked
in Section 35.3 as reconstructions: the comparison grid's mobile treatment and
the facet controls' mobile sheet were not resolvable from the capture, and the
behaviour specified is the one that keeps the page usable.

### 18.3 The comparison grid at small widths

The hardest responsive problem in the build, so it is specified rather than left
open.

At and above `1024px`: the full four-column grid with the sticky header row of
Section 10.4.

Below `1024px`: the grid becomes a single-plan view. A segmented control at the
top selects one of the four plans, the feature column and one value column are
shown, and the category rail becomes a horizontally scrolling strip above the
table. The selected plan persists in the address bar.

The alternative, a horizontally scrolling four-column table, is what the
reference does at tablet and it is acceptable there because the columns still
fit. It is not acceptable at `390px`, where a cell is narrower than its own
check glyph plus padding.

### 18.4 Images and media

Every image in this build is generated, per Section 33. Generated images must be
produced at the size they are displayed at and re-produced on a breakpoint
change, not scaled up from the smallest. The composed interface panels of
Sections 9.2 and 11.3 are built from real elements and reflow rather than
scaling.

### 18.5 Touch

| Requirement | Value |
|---|---|
| Minimum target | `44 x 44` including padding |
| Marquee rows | not draggable; they are decoration and must not trap a scroll gesture |
| Accordion headers | full width of the row is the target, not the caret |
| Facet sheet | dismissible by a downward drag as well as a button |

> **In plain language.** How the pages rearrange on smaller screens.
>
> The usual things happen: menus collapse behind a button, rows of cards become
> columns, two columns stack.
>
> One awkward width deserves a mention because it will otherwise be missed. Parts
> of the original site were written from the desktop down, and other parts from
> the phone up, and the two approaches change over at slightly different points.
> There is a narrow band of screen widths, around a small laptop or a large
> tablet, where a component can fall between the two and be styled by neither.
> Every component has to be looked at exactly there.
>
> The genuinely hard one is the big feature comparison table on the pricing page.
> Four columns of ticks does not fit on a phone: a single cell ends up narrower
> than the tick inside it. So on a phone it becomes one plan at a time, with a
> switcher across the top, and the plan you picked stays in the web address so
> the page can be shared.
>
> Finally, the drifting rows of logos must not swallow a finger swipe. They are
> decoration, and decoration that catches your scroll is worse than no decoration.

---

## 19. Performance

### 19.1 Budgets

Measured against a mid-range laptop three years old and a mid-range phone on a
throttled connection, which is the audience the reference's own copy claims to
serve in milliseconds.

| Metric | Budget | Applies to |
|---|---|---|
| Largest contentful paint | 2.0 seconds | every route |
| Interaction to next paint | 200 milliseconds | every route |
| Cumulative layout shift | 0.05 | every route |
| Total blocking time | 200 milliseconds | every route |
| First-party script, compressed | 120 kilobytes | every route |
| First-party style, compressed | 40 kilobytes | every route |
| Search overlay open to first result | 300 milliseconds | Section 8 |
| Keystroke to updated results | 150 milliseconds at the ninety-fifth percentile | Section 8 |
| Service search response | see Section 36.4 | Sections 22 to 25 |

The two search budgets are the ones that matter to the argument. A site that
sells instant search and takes half a second to respond to a keystroke has
disproved its own headline in the header of every page.

### 19.2 Where the reference spends

Measured from the capture's network log across six routes, by content type:

| Type | Files | Bytes |
|---|---|---|
| `image/webp` | 37 | 13,765,052 |
| `image/gif` | 604 | 2,400,928 |
| `application/javascript` | 166 | 2,064,143 |
| `text/javascript` | 201 | 1,382,130 |
| `video/mp4` | 1 | 1,627,213 |
| `image/png` | 13 | 1,074,351 |
| `application/x-javascript` | 50 | 419,181 |
| `image/avif` | 7 | 201,127 |
| `font/woff2` | 7 | 177,956 |
| `text/css` | 26 | 172,432 |
| `image/jpeg` | 5 | 73,247 |
| `application/json` | 86 | 18,899 |

Three observations, all actionable:

- Nearly fourteen megabytes of one image format across six routes. This build
  ships no images at all (Section 33), which removes the largest cost outright.
- Six hundred and four files of a legacy animated image format for 2.4
  megabytes. These are tracking pixels, one per event, not artwork.
- Four hundred and seventeen script files across three content types totalling
  3.8 megabytes uncompressed. The first-party share of that is small; the
  remainder is tags, consent, chat, analytics and experimentation.

The reference's performance problem is not its own code. It is thirty-odd
third-party surfaces, and the budget in Section 19.1 is only achievable if the
build resists reintroducing them.

### 19.3 Rules

- **No third-party script on the critical path.** Consent, chat, analytics and
  experimentation load after the route is interactive, or not at all.
- **Fonts are self-hosted, subset, and preloaded for the two weights above the
  fold** only: Sora 700 and Inter 400. The remaining ten weights load lazily and
  the fallback stacks in Section 3.3 must be metric-compatible enough that the
  swap does not shift layout.
- **The search overlay's code is loaded on first focus of the field, not on page
  load.** The field itself is markup and needs no script to render.
- **No layout-affecting property is animated.** The measured `transition: all`
  in Section 3.7 is explicitly overridden.
- **Highlighting is applied to one page of results**, per Section 23.7 step 13.
- **The marquee rows use transform only**, and pause when off screen.

### 19.4 Loading order

```
1. markup, style, and the two preloaded font faces
2. the route's own script: chrome, accordion, carousel timer
3. on first focus of the search field: the search overlay and its client
4. on idle: the marquee, the statistics loop, the remaining font weights
5. on idle, after everything above: consent, and only then anything consent gates
```

Steps 4 and 5 must not be reordered. Consent surfaces are the single largest
blocking third-party dependency on the reference, and loading one before the
page is interactive is how a site with a 120 kilobyte budget ends up with a
three second paint.

> **In plain language.** How fast it has to be, and where the original's time
> goes.
>
> The targets are ordinary except for two, and those two are the ones that matter
> here. The search panel has to show its first result within a third of a second
> of opening, and it has to keep up with your typing. A company selling instant
> search cannot have a slow search box on its own front page. That is not a
> performance target, it is the argument.
>
> The measurements of the original are worth repeating because they explain what
> this build is avoiding. Across six pages it loads about fourteen megabytes of
> images, six hundred tiny tracking images, and roughly four hundred separate
> script files. Almost none of that is the site's own work. It is consent banners,
> chat widgets, analytics, tag managers and testing tools, layered up over years.
>
> This build ships no images at all, because every picture in it is drawn from
> instructions rather than loaded. That alone removes the largest cost. The rest
> is discipline: nothing from a third party is allowed to load before the page
> works, the search panel's code arrives only when you first click the search box,
> and the cookie banner, of all things, is loaded last rather than first.

---
## 20. Backend and data contract

### 20.1 Scope, and how this section differs from the ones above it

Sections 1 to 19 are measured. They describe a marketing site that was captured,
and every literal in them came out of the evidence ledger.

Sections 20 to 30 are not measured. They are a **specified extension**: the
product the captured site sells, written out as a buildable service so that the
claims made on the home route are demonstrable inside the same build rather than
asserted in copy. The reference site's own backend is a headless content source
plus three form targets, and that much is recorded in Section 20.3. Everything
else in Sections 20 to 30 is normative specification authored for this build and
is listed as such in Section 35.4.

The reason for the extension is stated plainly, because it changes what "done"
means: a build that renders the pages and stubs the search is a brochure. The
site's central promise is retrieval quality, and retrieval quality is only
checkable against a working engine with a deterministic ranking contract. So the
engine is specified to the level of tie-breaks and test vectors, and Section 30
is the suite that decides whether the build is correct.

**Capability requirement - normative.** The build must ship a search service
that indexes records, answers keyword, filtered, faceted, geographic and hybrid
queries, applies merchandising controls, records interaction events, and exposes
all of it through one tenant-scoped interface with deterministic ordering.

**Observed implementation - informational.** The reference site's own site
search is a hosted product of the company the site belongs to, loaded as a
client library (Section 8.2, ledger tier 1). It is evidence that the pattern
exists on the page. It is not an instruction to depend on that service.

### 20.2 Service topology

Seven processes. Every one of them is required; none of them may be collapsed
into another without breaking a guarantee stated later in this document.

| Process | Responsibility | Scaling axis | May not also do |
|---|---|---|---|
| `edge` | request termination, key validation, quota accounting, routing | per region | ranking, writing |
| `writer` | ingestion, validation, task queue, index building | one per index shard, single writer | serving queries |
| `searcher` | query parsing, retrieval, ranking, faceting, response shaping | read replicas, stateless | mutating an index |
| `vectorizer` | embedding generation, vector index maintenance | batch, queue driven | ranking keyword results |
| `answerer` | retrieval-augmented answer generation and streaming | per concurrent stream | writing to an index |
| `collector` | interaction event intake, validation, deduplication | horizontal | aggregation |
| `roller` | scheduled aggregation of events into metric tables | one leader | intake |

The split between `writer` and `searcher` is the load-bearing one. Writes build
immutable index generations; reads bind to one generation for the whole life of
a query. A query that begins against generation 41 must finish against
generation 41 even if generation 42 is published mid-flight, because facet
counts, hit counts and pagination taken from two generations do not add up and
the disagreement is invisible in a single response.

### 20.3 What the reference site's own backend does, measured

Recorded here so the extension is not confused with the evidence.

| Touch point | Direction | Carries |
|---|---|---|
| Page content | the site reads | route content documents, published state, locale |
| Newsletter form | the site sends | one email address |
| Demo request form | the site sends | name, work email, company, country, company size, message |
| Site search | the site reads | query string, returns grouped suggestions and pages |

The first three are ordinary content-site plumbing and are specified in
Section 20.4 as three of the seventeen stored objects. The fourth is the seed of
everything from Section 21 onward.

### 20.4 The stored objects

Seventeen objects. Types are given as a compact schema; `string!` means
required, `string?` means nullable, `[T]` means an ordered list of `T`, and
`{K:V}` means a map.

```
Tenant {
  id                string!    stable, opaque, never reused
  name              string!
  plan              enum!      free | growth | premium | elite
  createdAt         timestamp!
  quotaSearchUnits  int!       per calendar month, UTC
  quotaRecords      int!
  retentionDays     int!       analytics retention, 7 | 30 | 90 | 365
}

Application {
  id                string!    tenant-scoped
  tenantId          string!
  name              string!
  regions           [string]!  at least one, ordered by preference
}

Index {
  id                string!
  applicationId     string!
  name              string!    unique within application, case sensitive
  primaryIndexId    string?    set when this index is a replica
  replicaKind       enum?      standard | virtual
  settings          Settings!
  generation        int!       monotonic, incremented on every publish
  recordCount       int!
  createdAt         timestamp!
}

Record {
  objectID          string!    caller supplied or server generated
  indexId           string!
  attributes        {string:any}!   arbitrary nesting, see Section 21.2
  version           int!       incremented on every accepted write
  updatedAt         timestamp!
}

Settings {
  searchableAttributes      [string]!   ordered; "unordered(attr)" wrapper legal
  attributesForFaceting     [string]!   "filterOnly(attr)", "searchable(attr)" legal
  customRanking             [string]!   "asc(attr)" or "desc(attr)"
  ranking                   [string]!   the eight criteria, order significant
  attributeForDistinct      string?
  distinct                  int!        default 0
  typoTolerance             enum!       true | false | min | strict
  minWordSizefor1Typo       int!        default 4
  minWordSizefor2Typos      int!        default 8
  allowTyposOnNumericTokens bool!       default false
  disableTypoToleranceOnAttributes [string]!
  ignorePlurals             bool|[string]!
  removeStopWords           bool|[string]!
  queryLanguages            [string]!
  advancedSyntax            bool!       default false
  optionalWords             [string]!
  removeWordsIfNoResults    enum!       none | lastWords | firstWords | allOptional
  exactOnSingleWordQuery    enum!       attribute | word | none
  alternativesAsExact       [string]!   ignorePlurals | singleWordSynonym | multiWordsSynonym
  paginationLimitedTo       int!        default 1000
  hitsPerPage               int!        default 20
  maxValuesPerFacet         int!        default 100
  sortFacetValuesBy         enum!       count | alpha
  attributesToHighlight     [string]!
  attributesToSnippet       [string]!   "attr:N" where N is word count
  highlightPreTag           string!     default "<em>"
  highlightPostTag          string!     default "</em>"
  snippetEllipsisText       string!     default "..."
  relevancyStrictness       int!        0 to 100, default 100
  numericAttributesForFiltering [string]!
  decompoundedAttributes    {string:[string]}!
  replicas                  [string]!
}

Synonym {
  id            string!
  indexId       string!
  type          enum!      multiWay | oneWay | altCorrection1 | altCorrection2 | placeholder
  synonyms      [string]?  multiWay
  input         string?    oneWay and altCorrection
  replacements  [string]?  oneWay
  corrections   [string]?  altCorrection
  placeholder   string?    placeholder, of the form "<token>"
}

Rule {
  id            string!
  indexId       string!
  enabled       bool!
  conditions    [RuleCondition]!    empty means "always"
  consequence   RuleConsequence!
  validity      [{from:timestamp, until:timestamp}]!
  description   string?
  priority      int!       lower runs first, ties broken by id ascending
}

RuleCondition {
  anchoring     enum!      is | startsWith | endsWith | contains
  pattern       string?    literal, or "{facet:<attr>}" for a facet capture
  context       string?
  filters       string?
  alternatives  bool!      default true, means synonyms may satisfy the pattern
}

RuleConsequence {
  params        {string:any}?   query parameter overrides
  promote       [{objectID:string, position:int}]?
  hide          [string]?       objectIDs
  userData      {string:any}?
  filterPromotes bool!          default false
}

ApiKey {
  id            string!
  applicationId string!
  kind          enum!      admin | search | ingest
  acl           [string]!  search, browse, addObject, deleteObject, settings, ...
  indices       [string]!  glob patterns, "*" legal
  validUntil    timestamp?
  maxHitsPerQuery int?
  maxQueriesPerIPPerHour int?
  referers      [string]!
  description   string?
  hashedSecret  string!    Section 26.2
}

QueryEvent {
  queryID       string!    opaque, 32 hex characters
  indexId       string!
  tenantId      string!
  userToken     string?
  query         string!
  filters       string?
  nbHits        int!
  processingTimeMs int!
  variantId     string?    set when an A/B test was applied
  ruleIds       [string]!
  personalized  bool!
  at            timestamp!
}

InteractionEvent {
  id            string!
  type          enum!      click | conversion | view
  subtype       enum?      addToCart | purchase
  indexId       string!
  userToken     string!
  authenticatedUserToken string?
  objectIDs     [string]!  1 to 20
  positions     [int]?     required for click when queryID is present
  queryID       string?
  value         number?    conversion only
  currency      string?    conversion only
  at            timestamp!
  receivedAt    timestamp!
}

AbTest {
  id            string!
  indexId       string!        the control index
  variantIndexId string!       the challenger, may be the same index with overrides
  variantParams {string:any}?
  trafficSplit  int!           percentage to the challenger, 1 to 99
  startAt       timestamp!
  endAt         timestamp!
  status        enum!          scheduled | running | stopped | expired
}

PersonalizationProfile {
  userToken     string!
  tenantId      string!
  facetScores   {string:number}!   "brand:acme" to a score in 0..1
  eventCount    int!
  lastSeenAt    timestamp!
}

Task {
  id            int!       monotonic per index, never per application
  indexId       string!
  kind          enum!      batch | settings | clear | move | copy | delete
  status        enum!      queued | processing | published | failed
  acceptedAt    timestamp!
  publishedAt   timestamp?
  error         string?
}

ContentDocument {
  id            string!
  route         string!    matches a route in Section 2.1
  locale        string!
  status        enum!      draft | published
  blocks        [Block]!
  seo           {title:string, description:string, canonical:string}
  updatedAt     timestamp!
}

FormSubmission {
  id            string!
  kind          enum!      newsletter | demo | contact
  payload       {string:any}!
  status        enum!      received | delivered | rejected
  at            timestamp!
}
```

### 20.5 Wire format and the error contract

All request and response bodies are UTF-8 encoded objects. Numbers are IEEE 754
doubles; any integer beyond 2^53 must be carried as a string or the build has
already lost data it will not notice losing.

Every error response is the same shape, and the status code alone is never the
whole answer:

```
{
  "message":  "human readable, safe to log, never contains a key",
  "status":   422,
  "code":     "invalid_facet_filter",
  "details":  { "path": "facetFilters[1][0]", "value": "brand:" },
  "requestId":"6f2a1c4e9b7d40a1"
}
```

| Status | Meaning in this system | Retryable |
|---|---|---|
| 400 | malformed body or unparseable parameter | no |
| 401 | key missing, unknown, expired, or signature invalid | no |
| 403 | key valid, action not in its access list, or index not in its scope | no |
| 404 | index or object does not exist | no |
| 409 | write conflict on an object version | yes, after re-read |
| 413 | record over the size limit in Section 20.7 | no |
| 422 | body parsed, values rejected: the common case, and `details` is required | no |
| 429 | quota or rate limit; `Retry-After` in whole seconds is required | yes |
| 500 | unexpected | yes |
| 503 | shedding load deliberately; `Retry-After` required | yes |

A 429 without `Retry-After` is a defect, not a variant. Clients in Section 28.4
back off on the header and only fall back to their own schedule when it is
absent, so an absent header turns a graceful degradation into a thundering herd.

### 20.6 Idempotency

Every mutating request accepts an `Idempotency-Key` header of 16 to 128
characters. The service stores the key with the tenant, the request path, a
digest of the body, and the response, for 24 hours.

The rules are exact because getting them approximately right is worse than not
implementing them at all:

1. Same key, same path, same body digest, within the window: return the stored
   response verbatim, including the original `taskID`, with header
   `Idempotent-Replay: true`. Do not re-enqueue.
2. Same key, same path, **different** body digest: reject with 422 and code
   `idempotency_key_reuse`. Never apply the second body.
3. Same key, different path: as case 2.
4. A key whose first request is still in flight: hold the second request for up
   to 5 seconds waiting for the first to resolve, then return 409 with code
   `idempotency_in_flight`.
5. No key on a mutating request: allowed, but the request is then at-least-once
   and the caller owns the consequences.

### 20.7 Limits and defaults

Every one of these is a hard limit and must be enforced at the `edge`, not
discovered downstream.

| Limit | Value | On breach |
|---|---|---|
| Record size | 100 kilobytes serialized | 413, and the batch is rejected whole |
| Batch size | 1000 operations or 10 megabytes, whichever first | 413 |
| Query length | 512 characters | truncate at 512, and report `truncatedQuery: true` |
| Words per query, ranked | 10 | words beyond the tenth are optional (Section 22.4) |
| Facet values returned | `maxValuesPerFacet`, capped at 1000 | truncate, set `exhaustiveFacetsCount: false` |
| Hits reachable by pagination | `paginationLimitedTo`, default 1000 | 422 on a page past the cap |
| Objects per interaction event | 20 | 422 |
| Concurrent answer streams per tenant | 8 on free, 64 on elite | 429 |
| Attribute nesting depth | 6 | 422 |
| Distinct facet attributes per index | 100 | 422 on settings write |

> **In plain language.** Everything up to this point in the document describes a
> website that was measured. From here on the document describes the thing the
> website is selling, built for real, and that part was written rather than
> measured. It is worth being clear about why.
>
> The site's whole argument is that it finds the right thing instantly, even when
> you spell it wrong, even when you ask in a sentence. You cannot demonstrate that
> with a picture of a search box. So the rest of this document specifies a working
> search service underneath the pages: something you can put a million products
> into, type a half-remembered name at, and get the right answer from in the time
> it takes to lift your finger off the key.
>
> That service is split into seven separate running pieces, and the split matters
> for one reason worth understanding: the part that accepts new data and the part
> that answers questions are kept apart on purpose. If they were the same piece,
> a shopper's search could catch the shop half-way through restocking, and they
> would see a page of results that says "48 results" at the top and shows 47, with
> a filter count that adds up to neither. Keeping them apart means every question
> gets answered against one frozen, complete snapshot of the data, even while the
> next snapshot is being built alongside it.
>
> The rest of the section is the paperwork of that promise: what a stored thing
> looks like, what the service says when it refuses, and every ceiling that exists.
> Two of those deserve a mention because they are visible to a customer. First,
> when the service is too busy it says so and says how long to wait, and a build
> that forgets the "how long" turns a polite queue into a stampede. Second, if the
> shop sends the same order twice because its own connection hiccuped, the service
> notices it is the same order and does not apply it twice.

---

## 21. Ingestion and the indexing pipeline

### 21.1 The write surface

```
POST /1/indexes/<INDEX>/batch
  { "requests": [ { "action": "<action>", "body": { ... } }, ... ] }
  -> 200 { "taskID": 88123, "objectIDs": [ ... ] }
```

Legal actions, and the exact difference between them, which is the part that
gets implemented wrong:

| Action | Object exists | Object absent | Replaces whole record |
|---|---|---|---|
| `addObject` | creates a second object with a new server `objectID` | creates | yes |
| `updateObject` | replaces every attribute | 404 for the operation, batch continues | yes |
| `partialUpdateObject` | merges, see Section 21.5 | 404 for the operation | no |
| `partialUpdateObjectNoCreate` | merges | operation is a no-op, not an error | no |
| `deleteObject` | deletes | no-op | n/a |
| `clear` | empties the index, keeps settings, synonyms and rules | n/a | n/a |

A batch is **not** a transaction. Operations are applied in array order, each is
individually accepted or rejected, and the response carries per-operation status
in `objectIDs` with `null` at the position of a rejected operation. A build that
rolls the whole batch back on one bad record will silently lose the other 999
when a single record breaks a limit, and a build that reports 200 with no
per-operation detail leaves the caller unable to tell.

### 21.2 The text pipeline

Applied to every string value of every attribute named in
`searchableAttributes`, in this order. The order is normative; swapping steps 3
and 4 changes results on accented and cased text.

1. **Unicode normalization** to NFKC.
2. **Case folding**, full folding, not `toLowerCase()`. `SS` and `ß` both fold to
   `ss`. Turkish dotted and dotless letters fold per the root locale unless
   `queryLanguages` contains `tr`, in which case the Turkish tailoring applies.
3. **Diacritic folding**: combining marks in the range U+0300 to U+036F are
   removed after decomposition, then the string is recomposed. `crème` and
   `creme` become the same token. Languages where a mark is a letter rather than
   an accent, declared through `queryLanguages`, are exempt per language: `ø`,
   `å`, `ä` and `ö` are not folded for `da`, `sv`, `no` or `fi`.
4. **Tokenization**, by script:
   - Latin, Cyrillic, Greek: split on anything that is neither a letter nor a
     digit, with two exceptions kept as single tokens: an apostrophe inside a
     word (`l'hotel` yields `l` and `hotel`, but `o'brien` yields one token), and
     a hyphen inside a word, which yields three tokens: the two parts and the
     joined form.
   - Han, Hiragana, Katakana: overlapping bigrams. `東京都` yields `東京`, `京都`.
     Not unigrams, and not a dictionary segmentation.
   - Thai, Khmer, Lao: dictionary segmentation, falling back to whole-run tokens
     when no dictionary is loaded, and the fallback must be reported in the index
     build log rather than passed over.
5. **Number handling**: a run of digits is one token. A decimal point inside
   digits does not split. A digit run adjacent to letters yields the joined token
   and both parts: `a4` yields `a4`, `a`, `4`.
6. **Stop words**, only if `removeStopWords` is on for the matching language, and
   only at query time, never at index time. Removing them at index time makes
   the setting irreversible without a full rebuild.
7. **Plural handling**, only if `ignorePlurals` is on: a language-specific
   suffix table maps a token to a canonical form. This is not stemming. `houses`
   maps to `house`; `housing` does not.
8. **Decompounding** for `de`, `nl`, `fi`, `sv`, `da`, `no`, `ko` when
   `decompoundedAttributes` names the attribute: a compound token additionally
   yields its parts, and the parts are marked as decompounded so the exact
   criterion in Section 22.8 can decline to count them.

**Every token keeps a byte offset range into the original, un-normalized
string.** This is not an optimization. Highlighting in Section 22.11 inserts
tags into the original text, and folding changes string lengths, so a build that
normalizes first and remembers offsets afterwards will place the tags in the
wrong place on exactly the accented and cased text that made the normalization
necessary.

### 21.3 The index structures

Per index generation, four structures, all immutable once published.

| Structure | Key | Value | Used by |
|---|---|---|---|
| Posting lists | token | sorted list of `(docId, attrId, position, isPrefixOnly)` | Sections 22.2, 22.6, 22.7 |
| Term dictionary | token | pointer plus document frequency | typo automaton, prefix walk |
| Forward index | `docId` | attribute values, for highlighting and faceting | Sections 22.11, 23.3 |
| Facet stores | `(attrId, value)` | document bitmap | Sections 23.3, 23.4 |

The term dictionary is a finite state transducer or a sorted block-based
structure supporting: exact lookup, prefix range walk, and traversal against a
Levenshtein automaton. A hash map satisfies the first and neither of the others,
and the build will pass a naive test suite while being unable to answer the
prefix queries that every keystroke in the interface depends on.

`docId` is a per-generation dense integer, not the `objectID`. Bitmaps and
posting lists are built on it. It is reassigned on every rebuild, so nothing
outside a generation may store it.

### 21.4 Prefix structure

Only the **last** word of a query is matched as a prefix, and only when
`queryType` is `prefixLast`, which is the default. The other two modes,
`prefixAll` and `prefixNone`, apply the rule to every word or to none.

The prefix walk is bounded: at most 1000 term dictionary entries are expanded
per prefix. When the bound is hit, expansion stops at the 1000 most frequent
matching terms by document frequency, and the response carries
`exhaustiveTypo: false`. Silently truncating without the flag makes a
reproducible bug look like a relevance opinion.

### 21.5 Partial updates

`partialUpdateObject` merges at the **top level only**. An object value in the
body replaces the whole nested object; it does not deep merge. This one line
prevents a class of data loss that only shows up months later on records whose
nested shape varies.

Operator values, given as `{"attr": {"_operation": "<op>", "value": <v>}}`:

| Operation | Effect | On a missing attribute | On a non-numeric attribute |
|---|---|---|---|
| `Increment` | `attr = attr + v` | treated as 0, then applied | 422 |
| `Decrement` | `attr = attr - v` | treated as 0, then applied | 422 |
| `IncrementFrom` | applies only if `attr == v`, result `v + 1` | 422 | 422 |
| `IncrementSet` | applies only if `v > attr`, result `v` | applied, result `v` | 422 |
| `Add` | append `v` to the list | creates a one-element list | 422 |
| `Remove` | remove every element equal to `v` | no-op | 422 |
| `AddUnique` | append `v` unless already present | creates a one-element list | 422 |

`IncrementFrom` and `IncrementSet` exist for exactly one purpose: making a retry
safe. A stock counter updated with `Increment` and retried after a timeout is
decremented twice; the same update expressed as `IncrementFrom` fails the second
time with 422 and code `condition_not_met`, which is the correct outcome and
must not be retried. `IncrementSet` carries a version number that only moves
forward, so out-of-order delivery of versions 7 then 6 leaves 7 in place.

### 21.6 Atomic reindex

```
POST /1/indexes/<TMP>/operation  { "operation": "move", "destination": "<INDEX>" }
```

The full-rebuild sequence, and what each step does to what already exists:

1. Create `<INDEX>_tmp`. It inherits **nothing**.
2. Copy settings, synonyms and rules from `<INDEX>` explicitly, with
   `operation: copy` and `scope: ["settings","synonyms","rules"]`. A build that
   assumes inheritance ships a reindex that silently resets relevance
   configuration, and the symptom appears as "search got worse this morning"
   with no deploy to blame.
3. Write every record into `<INDEX>_tmp` in batches.
4. `waitTask` on the last batch (Section 21.7).
5. `move` `<INDEX>_tmp` onto `<INDEX>`.

`move` is atomic with respect to readers: queries in flight complete against the
old generation, queries arriving after the swap bind to the new one, and no
query ever sees a mixture. `move` **destroys** the destination index, including
its settings, synonyms and rules, which is why step 2 is not optional. `move`
also invalidates the source name: `<INDEX>_tmp` does not exist afterwards.

Replicas of `<INDEX>` survive a `move` and are rebuilt from the new generation.
Their own settings are not overwritten.

### 21.7 The task queue and ordering

Every mutating request returns a `taskID`. The guarantees, stated as narrowly as
they actually hold:

- `taskID` is monotonically increasing **per index**. It is not comparable
  across indices, and a build that sorts a cross-index task list by `taskID` is
  sorting noise.
- Tasks on one index are applied in `taskID` order. There is exactly one writer
  per index at a time.
- `GET /1/indexes/<INDEX>/task/<TASK_ID>` returns `{"status":"published"}` when
  the task is visible to every searcher in the region, and `notPublished`
  otherwise. There is no third state visible to callers; a failed task reports
  `published` for the queue and carries `error` on the task object.
- Waiting means polling with backoff: 100 milliseconds, doubling, capped at 5
  seconds, giving up at 300 seconds. There is no long poll and no callback.

### 21.8 Deletion and reclamation

`deleteObject` marks a `docId` dead in the current generation's tombstone
bitmap. Queries filter tombstones after retrieval and before ranking, which
means a deleted object consumes a retrieval slot until compaction.

Compaction runs when tombstones exceed 20 percent of the generation, or on
`operation: compact`. `recordCount` excludes tombstones from the moment of the
delete task's publication, so the count the dashboard shows and the count a
`browse` returns agree.

`deleteBy` with a filter is a query plus a delete, is not atomic, and must
document that: records matching the filter that are written while it runs may
survive it. The interface must therefore never present `deleteBy` as a way to
guarantee an empty result set. `clear` is the guarantee.

> **In plain language.** This section is about putting things in, and it is
> mostly a list of the ways putting things in goes quietly wrong.
>
> When a shop sends a thousand products at once and one of them is broken, the
> service takes the nine hundred and ninety-nine and tells the shop exactly which
> one it refused. It does not throw the lot away, and it does not accept the lot
> and stay silent. Both of those are easier to build and both of them lose data
> the shop only discovers weeks later.
>
> Then there is the matter of turning words into something searchable. A person
> who types "creme" wants the cafe called "Crème", and a person who types "TOKYO"
> wants the same results as "tokyo". So the service flattens accents and capitals
> before it files anything away. The catch, and it is the single most common thing
> to get wrong here, is that flattening changes how long a word is. The service
> still has to be able to point at the exact letters in the original text later,
> to draw the yellow highlight over them. So it remembers, for every filed word,
> exactly which stretch of the untouched original it came from. Skip that, and the
> highlight lands one or two letters off, but only on accented words, which is
> precisely the case that made the flattening necessary in the first place.
>
> Chinese, Japanese, Thai and Korean do not put spaces between words, so they get
> their own handling. Splitting them letter by letter would make every search
> match everything.
>
> Two more things are worth knowing because a customer can see them.
>
> The first is rebuilding a catalogue from scratch. You build the new one beside
> the old one, and then swap them in a single motion, so nobody shopping ever
> sees a half-empty shop. The trap is that the new one starts out with none of the
> tuning that was done to the old one, so the tuning has to be copied over before
> the swap. Miss it and search quietly gets worse overnight with no change anyone
> can point at.
>
> The second is the safe way to change a number. If a shop says "add one to the
> stock count" and the connection drops before it hears back, it does not know
> whether to send it again. So there is a second way to say it: "change the stock
> count from four to five". Send that twice and the second one is politely
> refused, because the count is no longer four. Same intent, and it survives a bad
> connection.

---
## 22. The query engine and the ranking cascade

This is the section the product is judged on. Everything in it is normative.

### 22.1 Query parsing

A query string becomes an ordered list of query words by running the same
pipeline as Section 21.2, with two differences: stop words are removed here if
configured, and the last word is marked as a prefix candidate per Section 21.4.

With `advancedSyntax` on, three constructs are recognized before tokenization:

| Construct | Syntax | Meaning |
|---|---|---|
| Phrase | `"red shoes"` | the words must appear adjacent and in order, in one attribute; typo tolerance is disabled inside a phrase |
| Exclusion | `-clearance` | records matching the word in any searchable attribute are removed after retrieval and before ranking |
| Optional word | configured, not typed | see Section 22.4 |

An unbalanced quote is not an error. The trailing quote is implied at the end of
the string, because a user typing into a live search box passes through that
state on every phrase they ever write, and rejecting it makes the box stutter.

### 22.2 Typo tolerance

Per query word, the maximum edit distance is decided by the word's length in
**code points after folding**, not in bytes and not before folding:

| Word length | Max distance | Setting |
|---|---|---|
| 1 to `minWordSizefor1Typo - 1` (default 1 to 3) | 0 | exact only |
| `minWordSizefor1Typo` to `minWordSizefor2Typos - 1` (default 4 to 7) | 1 | `minWordSizefor1Typo` |
| `minWordSizefor2Typos` and longer (default 8 and up) | 2 | `minWordSizefor2Typos` |

The distance is **Damerau-Levenshtein**: insertion, deletion, substitution and
**transposition of two adjacent characters, which costs 1, not 2**. `hlelo` is
one typo from `hello`. A build using plain Levenshtein scores it as two, which
pushes a very common human error out of a one-typo budget and is invisible until
someone types quickly.

Four rules on top of the distance:

1. **The first character may not be substituted or deleted.** `xello` does not
   match `hello`. Prefix walking makes first-character errors explode the
   candidate set, and the interface would appear to guess wildly.
2. Digit tokens get no typo tolerance unless `allowTyposOnNumericTokens` is on.
   `2024` must not match `2025`.
3. Typo tolerance is off inside a phrase, and off for attributes named in
   `disableTypoToleranceOnAttributes`.
4. `typoTolerance: min` returns typo matches only when the zero-typo result set
   is empty. `strict` keeps typo matches but, when both exist, drops the
   two-typo matches entirely.

The candidate expansion is a traversal of the term dictionary against a
Levenshtein automaton of the right distance, not a scan. The distinction is a
performance requirement, not a style preference: a scan over a dictionary of a
few million terms cannot meet Section 19.1.

### 22.3 What "matching" means

A record matches when **every** query word matches, after word removal
(Section 22.4) has decided which words are still required. A word matches a
record when a token in any attribute in `searchableAttributes` matches it
exactly, within its typo budget, as a prefix if the word is the prefix
candidate, or through a synonym or plural per Section 24.1.

Matching is per word across the whole record, not per attribute. "red shoes"
matches a record whose title is "shoes" and whose colour is "red". The
`attribute` criterion in Section 22.7 is what expresses a preference for both
words landing in the same, earlier attribute.

### 22.4 Optional words and word removal

Words in `optionalWords`, and every query word past the tenth, are optional: a
record matching a subset still matches, and the `words` criterion in
Section 22.5 orders by how many optional words were matched.

When the required words yield zero hits, `removeWordsIfNoResults` decides what
happens next:

| Value | Behaviour |
|---|---|
| `none` | return zero hits |
| `lastWords` | drop the last word, retry; repeat, one word at a time, until non-empty or one word remains |
| `firstWords` | the same, from the front |
| `allOptional` | one retry with every word optional, records matching at least one word are returned |

Each removal round is a **fresh, complete ranking pass**, not an append to the
previous result set. Results from a round that removed two words never interleave
with results from a round that removed one; the earlier round's results come
first, in their entirety. The response reports `nbWordsRemoved` per hit through
`_rankingInfo.nbExactWords` and the top-level `parsedQuery`.

### 22.5 The ranking cascade

**The core contract of this build.** Hits are ordered by eight criteria applied
in sequence. Each criterion is a comparison; when two hits are equal on a
criterion, and only then, the next criterion is consulted. There is no weighted
sum anywhere in this cascade, and no score is computed for it.

The default order, which is the `ranking` setting:

```
1. typo        ascending   total typos across matched words
2. geo         ascending   distance bucket, Section 22.10
3. words       descending  number of matched optional words
4. filters     descending  sum of matched optionalFilters scores
5. proximity   ascending   Section 22.6
6. attribute   ascending   Section 22.7
7. exact       descending  Section 22.8
8. custom      ...         Section 22.9, the customRanking list, in order
```

A record with one typo ranks below every record with none, however good it looks
on every later criterion. That is the intended behaviour and it is the single
most common thing a build gets wrong, because the familiar approach from
information retrieval is to compute one relevance score per document and sort by
it. A weighted score cannot express "never trade a typo for a better price",
which is exactly what a merchandiser configuring this system is asking for.

Two consequences to implement deliberately:

- Sorting must be **stable** and, after `custom`, must fall back to `objectID`
  ascending. Without a total order, two records identical on all eight criteria
  swap places between requests, and page 2 then repeats or omits a hit that
  page 1 already showed.
- `relevancyStrictness` between 0 and 100 controls how far down the cascade a
  record may be admitted when optional-word matching has been used. At 100, only
  the best `words` bucket is returned. At 0, every partial match is returned.
  In between, hits below the threshold are returned but marked
  `_rankingInfo.promoted: false`, and the response reports `nbSortedHits`, the
  count of hits above the strictness cut.

### 22.6 Proximity

For each pair of adjacent query words, in query order, the proximity value is
the number of tokens between their closest matching positions in the same
attribute, plus one, capped at 8. Words matched in different attributes score
the cap. The record's proximity is the sum over pairs.

Exact rules that decide real orderings:

- Adjacent, in order: 1. Adjacent, reversed order: 2. Inverting a pair costs one,
  not the cap.
- A phrase from Section 22.1 requires proximity 1 for its pairs; it is a filter,
  not a preference.
- Optional words that were not matched are skipped when forming pairs, they do
  not contribute the cap.

### 22.7 The attribute criterion

Two components, compared in this order.

**Attribute index.** The position of the attribute in `searchableAttributes`,
zero based. A word matched in the first searchable attribute beats the same word
matched in the second. When a word matches in several attributes the best, that
is the lowest, index counts.

`unordered(attr)` in the settings list means the two attributes it separates are
tied: attributes wrapped in `unordered()` at the same list position share an
index. Ordered attributes at different positions never tie.

**Word position.** Within the winning attribute, the position of the match, zero
based, capped at 63. Earlier is better. `unordered(attr)` sets this component to
zero for that attribute, which is the entire point of the wrapper: it says "a
match anywhere in this attribute is as good as a match at the start", which is
what you want for a description and not what you want for a title.

### 22.8 The exact criterion

The number of query words that matched **exactly**, meaning zero typos, not
through a prefix expansion, and not through an alternative unless configured.
Descending.

For a single-word query, `exactOnSingleWordQuery` chooses the definition:

| Value | A single-word query scores 1 when |
|---|---|
| `attribute` (default) | the word equals the entire value of a searchable attribute |
| `word` | the word matches a whole word in any searchable attribute |
| `none` | never; the criterion is disabled for single-word queries |

`alternativesAsExact` decides which alternatives still count as exact:

| Member | Effect |
|---|---|
| `ignorePlurals` | a plural form matched through Section 21.2 step 7 counts as exact |
| `singleWordSynonym` | a one-word synonym counts as exact |
| `multiWordsSynonym` | a multi-word synonym counts as exact for each of its words |

Decompounded parts from Section 21.2 step 8 never count as exact.

### 22.9 Custom ranking

`customRanking` is an ordered list of `asc(attr)` and `desc(attr)`. Each entry
is its own tie-break level, consulted only when everything before it is equal.

Numeric values are bucketed before comparison, and the bucketing is what makes
the behaviour sane: values are compared at a precision of 4 significant decimal
digits, so 4.7192 and 4.7195 are equal and fall through to the next criterion,
while 4.71 and 4.83 are not. Without bucketing, a floating point rating with 15
digits of noise makes every later criterion unreachable.

Missing attribute sorts last for `desc`, last for `asc`. Not first for `asc`:
the rule is "a record that does not have the attribute never wins on it".

Booleans compare as 1 and 0. Strings compare by code point after folding. Lists
compare by their first element.

### 22.10 Geo ranking

When `aroundLatLng` or `aroundLatLngViaIP` is set, the `geo` criterion applies.
A record may carry `_geoloc` as one point or a list of points; the closest point
is used.

Distance is haversine metres on a sphere of radius 6371000 metres. It is then
**bucketed by `aroundPrecision`**, default 10 metres, and the bucket, not the
distance, is what the criterion compares. Two records 3 metres apart tie on geo
and are separated by the next criterion. A build comparing raw distances makes
the geo criterion a total order, which starves every criterion below it and is
why "the nearest shop always wins even when it is closed" is a geo bug and not a
data bug.

`aroundRadius` filters before ranking. `aroundRadius: "all"` disables the filter
and keeps the ranking. `insidePolygon` and `insideBoundingBox` are filters only
and do not enable the geo criterion.

### 22.11 Highlighting and snippeting

Every hit carries `_highlightResult` mirroring the shape of the record, and
`_snippetResult` for attributes named in `attributesToSnippet`.

```
"_highlightResult": {
  "name": { "value": "Cr<em>ème</em> Brulee", "matchLevel": "partial",
            "matchedWords": ["creme"] }
}
```

The rules that make this hard, and that Section 30.6 tests:

1. Tags are inserted into the **original** attribute value, at the byte offsets
   recorded in Section 21.2. The value returned is the original text, not the
   folded text.
2. `matchLevel` is `none`, `partial` or `full`. `full` means every query word
   matched inside this attribute.
3. Overlapping matches merge into one tag pair. Two adjacent matches with
   nothing between them merge; with one space between them they do not.
4. A prefix match highlights only the matched prefix, not the whole word.
5. Snippets are `N` words wide, centred on the first match, with
   `snippetEllipsisText` on any side that was cut. A snippet that fits the whole
   value gets no ellipsis on either side.
6. The tags are inserted after escaping is decided by the caller: the service
   returns raw text with tags and never performs escaping itself, which the
   client must know or it will double escape.

### 22.12 Pagination and counting

| Field | Meaning |
|---|---|
| `nbHits` | matching records; exact when `exhaustiveNbHits` is true, an estimate otherwise |
| `exhaustiveNbHits` | false when retrieval stopped early against a limit |
| `nbPages` | `min(ceil(nbHits / hitsPerPage), ceil(paginationLimitedTo / hitsPerPage))` |
| `page` | zero based |
| `hitsPerPage` | 1 to 1000 |

`offset` and `length` may be used instead of `page` and `hitsPerPage`, and
mixing the two in one request is 422, not a silent precedence rule.

Requesting a page past `nbPages` returns an empty `hits` array and 200, not 404.
Requesting an offset past `paginationLimitedTo` is 422.

### 22.13 The response contract

```
{
  "hits": [ { ...record, "objectID": "...", "_highlightResult": {...},
              "_rankingInfo": {...} } ],
  "nbHits": 1249, "page": 0, "nbPages": 50, "hitsPerPage": 25,
  "exhaustiveNbHits": true, "exhaustiveFacetsCount": true,
  "exhaustiveTypo": true,
  "processingTimeMS": 3,
  "query": "hlelo wrld", "parsedQuery": "hlelo wrld",
  "params": "query=hlelo+wrld&hitsPerPage=25",
  "queryID": "8f3c1a0b6e2d47f9a1c5b8e0d2f47a63",
  "facets": { "brand": { "acme": 42 } },
  "facets_stats": { "price": { "min": 4.5, "max": 990, "avg": 71.2, "sum": 8901 } },
  "appliedRules": [ "rule-boost-acme" ],
  "abTestVariantID": 2,
  "renderingContent": { ... },
  "userData": [ ... ]
}
```

`_rankingInfo` is returned only with `getRankingInfo: true`, and carries every
criterion's value for that hit: `nbTypos`, `firstMatchedWord`, `proximityDistance`,
`userScore`, `geoDistance`, `geoPrecision`, `nbExactWords`, `words`, `filters`,
`promoted`, `matchedGeoLocation`. It is the only way a merchandiser can answer
"why is this above that", and it must be exact rather than reconstructed, which
means the ranker records it while comparing rather than recomputing it after.

> **In plain language.** This is the part that decides what you see first, and the
> way it decides is unusual enough to be worth reading even if you skip everything
> else in this document.
>
> Most search engines give every result a single grade out of ten and show you the
> highest grades first. This one does not. It runs a series of tie-breaks, in a
> fixed order, like a sports league table.
>
> | The question, in order | What it means for you |
> |---|---|
> | Did they spell it right? | A result that matches what you typed exactly always beats one that had to forgive a slip |
> | How near is it? | Only when you have asked for things near you |
> | How many of your words are in it? | More of your words is better |
> | Are your words next to each other? | "red shoes" beats a page with "red" at the top and "shoes" at the bottom |
> | Where in the record did they appear? | In the title beats in the small print |
> | Whole words, or just the beginning? | Typing "sho" finds "shoes", but an actual "sho" wins |
> | The shop's own preference | Rating, popularity, stock, whatever the shop chose |
>
> The point of a ladder instead of a grade is that a shop can say "never let a
> misspelled match jump above a correct one, no matter how popular it is", and mean
> it. You cannot say that with a single grade out of ten. This is the thing most
> often built wrong, because the grade-out-of-ten approach is the one every
> textbook teaches, and a build that uses it looks fine on a demo and cannot be
> tuned by the people who need to tune it.
>
> A few smaller decisions in here have visible consequences.
>
> Swapping two neighbouring letters, the thing everyone does when typing fast,
> counts as one slip and not two. Getting the very first letter wrong is not
> forgiven at all, because forgiving it makes the results look like wild guesses.
> Numbers are never forgiven: searching for a 2024 model must not return the 2025.
>
> When you ask for things near you, distances are rounded to the nearest ten
> paces before they are compared, so two shops on the same street count as
> equally near and the shop's own ranking gets to break the tie. Without the
> rounding the nearest thing always wins by a hair, and everything the shop cared
> about stops mattering.
>
> And when two results are genuinely identical on every question in the ladder,
> the order is still fixed rather than arbitrary. Otherwise the same item can
> appear on page one and again on page two, which readers notice immediately and
> which is very hard to explain.

---
## 23. Filtering, faceting and deduplication

### 23.1 The `filters` grammar

One string, parsed into a boolean tree. This grammar is normative and complete;
anything outside it is 422 with the offending span in `details`.

```
expr      := or
or        := and ( "OR" and )*
and       := unary ( "AND" unary )*
unary     := [ "NOT" ] atom
atom      := "(" expr ")" | facet | numeric | tag | range
facet     := attr ":" value                     value quoted if it contains a space
numeric   := attr ( "<" | "<=" | "=" | "!=" | ">=" | ">" ) number
range     := attr ":" number " TO " number      inclusive at both ends
tag       := "_tags" ":" value
attr      := identifier                          must be in attributesForFaceting
value     := identifier | quoted-string | "true" | "false"
```

Precedence is `NOT` then `AND` then `OR`. `a:1 OR b:2 AND c:3` parses as
`a:1 OR (b:2 AND c:3)`. This is the arithmetic convention and it is the opposite
of what a left-to-right reader expects, so the interface must render the
parenthesization back to the user rather than echo the string.

Filtering happens **before** ranking and before facet counting. A filtered-out
record contributes to no count anywhere except a disjunctive count on its own
facet, which is Section 23.4 and the reason that section exists.

Numeric comparison on a string attribute is 422, not a silent lexical compare.
`price > "10"` is a 422; the quotes make it a string.

### 23.2 The array forms

`facetFilters`, `numericFilters` and `tagFilters` take a nested array whose
nesting **is** the boolean structure:

| Form | Meaning |
|---|---|
| `["a:1", "b:2"]` | `a:1 AND b:2` |
| `[["a:1", "a:2"]]` | `a:1 OR a:2` |
| `[["a:1","a:2"], "b:3"]` | `(a:1 OR a:2) AND b:3` |
| `["-a:1"]` | `NOT a:1` |

Outer level is AND, one level of nesting is OR, and there is no second level of
nesting: `[[["a:1"]]]` is 422. This shape catches builds out in one specific
way. The multi-select filter interface in Section 16.4 produces
`[["brand:acme","brand:zeta"]]` when two brands in the same group are ticked and
`["brand:acme","colour:red"]` when one from each of two groups is, and a build
that flattens both into one array turns a two-brand search into a search for
records made by both brands at once, which returns nothing and reads as a data
problem.

`optionalFilters` is a different thing wearing the same clothes: it does not
filter, it feeds the `filters` criterion in Section 22.5. `optionalFilters:
["brand:acme<score=3>"]` adds 3 to the criterion for matching records and
nothing for others. A negative optional filter, `["-brand:zeta<score=2>"]`,
scores records that do **not** match.

### 23.3 Conjunctive facet counts

For an attribute in `facets` that is **not** currently filtered on, the count of
each value is the number of records that match the query **and every filter**,
grouped by that attribute's values.

This is the easy half and it is what a single grouped pass over the result set
produces.

### 23.4 Disjunctive facet counts

For an attribute the user **is** currently filtering on, and where the interface
allows several values of it to be selected at once, the counts must be computed
**with that attribute's own filter removed** and every other filter kept.

This is the half that gets built wrong, and the symptom is unmistakable once you
know it: the user ticks "Acme", and every other brand in the list drops to zero
or vanishes, so the list becomes unusable for adding a second brand. The counts
have to answer "how many would I get if I ticked this as well", which is a
different query from the one that produced the results on screen.

The requirement, stated exactly:

- For each attribute `A` declared disjunctive, evaluate the query with the
  filter tree pruned of every clause on `A`, and group by `A`.
- Every other facet, and the hits themselves, use the full filter tree.
- A value of `A` currently selected but matching zero records under the pruned
  tree must still be returned, with count 0, so the user can untick it. Dropping
  it strands the interface in a state the user cannot leave.
- `exhaustiveFacetsCount` is false if any grouping hit `maxValuesPerFacet`.

The implementation is one extra evaluation per disjunctive attribute, over
bitmaps rather than records. A build that reuses the conjunctive counts here
will pass every test that ticks a single facet and fail the moment two are
ticked in the same group.

`facets_stats` follows the same rule: the numeric min, max, average and sum for
an attribute the user is filtering a range on must be computed with that range
removed, or the range slider collapses to the width of the current selection and
the user cannot widen it again.

### 23.5 Facet value search

```
POST /1/indexes/<INDEX>/facets/<FACET>/query
  { "facetQuery": "acm", "params": "query=shoes&filters=..." }
```

Searches the **values** of one facet, not the records. Prefix matching, typo
tolerance per the index settings, and the counts respect the same disjunctive
rule as Section 23.4. Only attributes declared `searchable(attr)` in
`attributesForFaceting` are eligible; the others are 422.

### 23.6 Deduplication

`attributeForDistinct` names an attribute; `distinct: N` keeps at most `N`
records per distinct value of it, keeping the best ranked.

The interactions are where this earns a place in Section 29:

- Deduplication happens **after** ranking and **before** pagination. Records
  removed by it do not occupy slots on the page.
- `nbHits` counts **groups**, not records, when `distinct` is greater than 0.
  A build that reports the record count shows "1,204 results" over 300 rows and
  the user reaches the end of the list four times too early.
- Facet counts count **records**, not groups, unless `facetingAfterDistinct` is
  true, in which case they count groups. The two settings must be consistent
  across a session or the numbers on the page contradict each other.
- A record promoted by a rule (Section 24.2) is exempt from deduplication and
  does not consume its group's quota.

### 23.7 Ordering of the whole read path

The stages, in the order they run. Reordering any two of these changes results,
and most of the defects in Section 29 are a reordering.

```
1. parse query and parameters
2. apply rules whose conditions match, merging their params        Section 24.2
3. expand synonyms and plurals into the query tree                 Section 24.1
4. retrieve candidates per word, with typo and prefix expansion    Sections 22.2, 22.3
5. intersect words, apply word removal if empty                    Section 22.4
6. apply filters, tombstones and exclusions                        Sections 23.1, 21.8
7. compute personalization scores, if enabled                      Section 24.3
8. rank by the cascade                                             Section 22.5
9. apply rule promotions and hides                                 Section 24.2
10. deduplicate                                                    Section 23.6
11. compute facet counts, conjunctive and disjunctive              Sections 23.3, 23.4
12. paginate
13. highlight and snippet the page of hits only                    Section 22.11
14. attach queryID, ranking info, applied rules, variant           Section 22.13
```

Step 13 comes after step 12 deliberately: highlighting the whole result set
rather than the returned page is the most common reason a correct engine is too
slow to ship.

> **In plain language.** Filters look simple and hide the single most-missed
> behaviour in this whole document, so it gets its own explanation.
>
> Picture a shop page with a list of brands down the left, each with a number
> beside it. You tick Acme. The results narrow to Acme, which is right. Now look
> at the numbers beside the other brands. If they have all dropped to zero, the
> build is wrong, and you can no longer tick a second brand, because the list is
> telling you there is nothing there.
>
> The number beside each unticked brand has to answer a different question from
> the one on screen: not "how many Acme items are there", but "how many would I
> see if I ticked this one as well". Working that out means running the search a
> second time with the brand tick ignored, while keeping every other choice the
> shopper made. It is genuinely a second pass, and a build that reuses the first
> pass produces a filter list that dies the moment anyone uses it properly.
>
> The same applies to a price slider. If the numbers behind the slider only ever
> describe the range you already chose, the slider shrinks every time you touch it
> and you can never widen it again.
>
> There is a second trap in how the choices are written down. Ticking two brands
> means "Acme or Zeta". Ticking one brand and one colour means "Acme and red". The
> two are written almost identically, and a build that muddles them turns "show me
> Acme or Zeta" into "show me things made by Acme and Zeta at the same time",
> which returns an empty page that looks like missing data rather than a bug.
>
> Finally, there is a way of saying "only show me one of each". One shirt, not the
> same shirt in nine colours. When that is on, the total at the top of the page
> has to count shirts, not colours, or the shopper is told there are twelve hundred
> results and runs out after three hundred.
>
> The last part of the section is the running order of all of it, which matters
> more than it sounds. Doing the work in a different order produces answers that
> are wrong in ways nobody can see: the same page, the same count, and the wrong
> items.

---

## 24. Merchandising and relevance controls

Four controls sit between the raw engine and the merchandiser. All four are
optional per index; all four have a defined precedence, in Section 24.6.

### 24.1 Synonyms

| Type | Declared as | Behaviour |
|---|---|---|
| `multiWay` | `["sofa","couch","settee"]` | any one expands to all |
| `oneWay` | input `iphone`, replacements `["smartphone"]` | `iphone` also matches `smartphone`, never the reverse |
| `altCorrection1` | input `tablet`, corrections `["tablets"]` | matches with one typo already spent |
| `altCorrection2` | as above, two typos spent | |
| `placeholder` | `"<streetnumber>"` with values | a token in a record stands for any value of the placeholder |

Rules that decide behaviour a merchandiser will notice:

- A multi-word synonym expands into a phrase, not into loose words. `bike`
  expanding to `mountain bike` requires the two words adjacent in the record.
- Expansion happens after tokenization and before retrieval, so a synonym is
  itself typo-tolerant unless it came from an `altCorrection`, which has already
  spent its budget.
- Whether a synonym match counts as exact for Section 22.8 is decided by
  `alternativesAsExact`, and the default counts one-word synonyms and not
  multi-word ones. This is the reason a synonym can improve recall and appear to
  do nothing to ordering.
- Synonyms are per index and are **not** carried by `move` unless copied
  explicitly, per Section 21.6 step 2.

### 24.2 Query rules

A rule is a condition and a consequence. The evaluation is exact:

1. Collect every enabled rule whose validity window contains the request time
   and whose `context` matches the request's `ruleContexts`, if any.
2. Evaluate conditions against the **parsed** query, after tokenization, and,
   when `alternatives` is true, against synonym expansions of it.
3. Anchoring: `is` matches the whole query, `startsWith` and `endsWith` match at
   the ends, `contains` anywhere. A `{facet:brand}` pattern captures a token that
   is a value of that facet and makes it available to the consequence.
4. Sort matching rules by `priority` ascending, then `id` ascending.
5. Merge consequences in that order. Later rules overwrite earlier ones on the
   same parameter. `promote` lists concatenate, and a duplicate `objectID` keeps
   its first, that is its highest priority, position.
6. Apply `hide` last, and a hidden object stays hidden even if a promotion named
   it, because a merchandiser removing something must not be overridden by a
   merchandiser boosting something.

Promotion positions are **zero based against the final list, after
deduplication**, and are honoured on the first page only. Two promotions to the
same position resolve by rule order, with the loser taking the next free
position. A promotion to a position beyond the page size is dropped and reported
in `appliedRules` with `"applied": false`, rather than silently ignored.

### 24.3 Personalization

A profile is a map of `facet:value` to affinity, built by the `roller` from
interaction events:

```
score(facet:value) = min(1, sum over events of weight(type) * decay(age))
weight  = view 1, click 3, conversion 10
decay   = 0.5 ^ (age in days / halfLifeDays), halfLifeDays default 30
```

At query time, with `enablePersonalization: true` and a `userToken`:

```
personalizationBoost(record) =
    personalizationImpact / 100
  * sum over facets f of record of score(f)
  / max(1, number of facets considered)
```

The boost enters the cascade as a **term of the `filters` criterion**, not as a
multiplier on a final score, and never above the `typo`, `words` or `proximity`
criteria. That placement is the whole design: personalization may reorder
equally relevant results and may not promote a worse match. A build that applies
it as a multiplier at the end will show a user a misspelled match of a brand they
like above an exact match of the brand they searched for, which reads as the
engine ignoring what was typed.

`personalizationImpact` is 0 to 100 and the default is 100. At 0 the feature is
inert but still logs, which is what makes an A/B test of it possible.

### 24.4 A/B testing

```
AbTest { control index, variant index or params, split, window }
```

Assignment is deterministic and computed at the `edge`:

```
bucket = crc32( abTestId + ":" + userToken ) mod 100
variant = bucket < trafficSplit ? challenger : control
```

Requirements that make the result trustworthy:

- The same `userToken` gets the same variant for the whole test, across devices,
  regions and processes. A random assignment per request destroys the test while
  producing plausible-looking numbers.
- A request with no `userToken` is **not** assigned. It runs the control and is
  excluded from analysis. Assigning anonymous traffic by IP or by session makes
  a returning user flip variants mid-funnel.
- `abTestVariantID` is returned in the response and stamped on the `QueryEvent`,
  and every `InteractionEvent` carrying that `queryID` inherits it. Attribution
  by re-deriving the bucket at analysis time is forbidden: the split may have
  been edited since.
- Stopping a test freezes assignment; it does not delete collected events.

### 24.5 Pinned and hidden items in the interface

The merchandising screen in Section 16.6 writes rules, not a separate object.
Dragging a product to the top of the results for the query "sofa" creates a rule
with anchoring `is`, pattern `sofa`, and a `promote` entry. This keeps one
mechanism, one precedence order and one audit trail, and it means a pin is
visible to anyone reading the rules rather than hidden in a second system.

### 24.6 Precedence

When several controls speak at once, this is the order, and it is a strict
one, not a suggestion:

```
1. rules change the query and its parameters          (before retrieval)
2. synonyms expand the query                          (before retrieval)
3. filters and exclusions remove records              (hard, never overridden)
4. the eight-criterion cascade orders what is left
5. personalization contributes inside criterion 4     (the filters criterion)
6. rule promotions move records to fixed positions
7. rule hides remove records
8. deduplication collapses groups, promotions exempt
```

A filter always beats a promotion: a rule cannot promote a record the filter
removed. This is the rule that makes "out of stock items must never appear"
enforceable in the presence of a merchandiser who pins things.

> **In plain language.** This section is the set of levers a person, rather than a
> program, gets to pull.
>
> The first is a dictionary of things that mean the same. Somebody searching for
> "couch" should find the sofas. There is a one-way version too, because "iPhone"
> should find smartphones but "smartphone" should not fill up with iPhones.
>
> The second is a set of standing instructions: when someone searches for this,
> do that. Put this item on top for the next fortnight. Never show this one. Add
> a banner above the results when anyone searches for "sale". These have an order
> of authority, and one part of it is worth stating out loud: hiding beats
> promoting. If one person has said "never show this" and another has said "always
> show this first", the item stays hidden, because the cost of wrongly showing
> something is higher than the cost of wrongly hiding it.
>
> The third is tailoring results to the person. Somebody who keeps buying one
> brand sees more of it. The important restraint is where this is allowed to act:
> it can reorder things that are equally good matches, and it cannot push a worse
> match above a better one. Built without that restraint, a shopper who types a
> brand name sees a different brand at the top because they liked it last month,
> and the search looks broken rather than clever.
>
> The fourth is running two versions at once to see which sells better. The rule
> that makes the numbers mean anything is that the same person always sees the
> same version, on every visit and every device, until the trial ends. A build
> that flips a coin per search still produces a neat report, and the report is
> worthless.

---
## 25. Hybrid retrieval and generated answers

The two capabilities the home route names in its first three words. Both are
normative; both are the parts most likely to be stubbed and declared done.

### 25.1 Embeddings and the vector store

Every record whose index has `vectorSearch.enabled` gets a vector, computed by
`vectorizer` from a template over its attributes:

```
vectorTemplate: "{{title}}. {{brand}}. {{categories|join(', ')}}. {{description|truncate(400)}}"
```

| Requirement | Value |
|---|---|
| Dimensions | fixed per index at creation, 256 to 1536, immutable afterwards |
| Normalization | vectors stored L2-normalized, so cosine similarity is a dot product |
| Model identity | stored per vector as `modelId`; a vector whose `modelId` differs from the index's current model is stale |
| Staleness | a query may not mix models; if any candidate is stale the response sets `vectorIndexStale: true` and falls back to keyword-only |
| Backfill | changing the model creates a new generation and re-embeds; it never rewrites in place |

The last two rows are the ones that get skipped. Vectors from two different
models are not comparable, and mixing them produces a similarity ordering that
looks plausible and is arbitrary. There is no cheaper way to detect this than
stamping the model on each vector, and no way to recover from it after the fact.

### 25.2 Approximate nearest neighbour

Graph-based index, HNSW or equivalent, per generation, with the parameters
exposed rather than buried:

| Parameter | Default | Effect |
|---|---|---|
| `M` | 16 | neighbours per node; memory and recall |
| `efConstruction` | 200 | build-time breadth |
| `efSearch` | 64 | query-time breadth, may be raised per query up to 512 |
| `seed` | fixed per index | build determinism |

Filters must be applied **during** the graph walk, not after it. Retrieving 100
nearest neighbours and then discarding those that fail the filter returns 3
results when the filter is selective, and the interface reports "3 results" for
a query that has thousands. The walk therefore consults the filter bitmap at
each candidate and continues until `efSearch` surviving candidates are found or
the graph is exhausted.

### 25.3 Fusion

Keyword and vector retrieval produce two ranked lists. They are combined by
reciprocal rank fusion over **ranks**, never over scores:

```
rrf(d) = wk / (k + rank_keyword(d)) + wv / (k + rank_vector(d))
k  = 60
wk = keywordWeight, default 1.0
wv = vectorWeight,  default 1.0
rank is 1-based; a document absent from a list contributes 0 for that list
```

Scores are not comparable between the two systems: one is a cascade of
tie-breaks with no score at all, the other is a cosine similarity in zero to
one. Normalizing them onto a common range is the obvious move and it is wrong,
because the keyword side has no score to normalize, and any score invented for
it will not respect the cascade in Section 22.5.

Two guarantees on top of fusion:

- A record that matched **every** query word exactly, in the keyword sense of
  Section 22.8, may not be ranked below position 10 by fusion. If fusion places
  it lower, it is lifted to position 10 and the response records
  `exactLiftApplied: true`. This is what stops the semantic side burying a
  literal match for a product code.
- `semanticRatio` of 0 must be exactly keyword search, bit for bit identical to
  the same query with vector search disabled, and 1 must be exactly vector
  search. If the endpoints are not exact, no one can debug the middle.

### 25.4 The answer pipeline

```
POST /1/indexes/<INDEX>/answer
  { "query": "...", "userToken": "...", "searchParams": { ... },
    "maxTokens": 512, "stream": true }
```

Stages, all of which must be observable in the response trace:

1. **Retrieve.** Run a hybrid search per Section 25.3, `hitsPerPage` 8 by
   default, honouring every filter and every key restriction from Section 26.
2. **Ground.** Build the context from `attributesToRetrieveForAnswer` only.
   Nothing outside the retrieved records enters the prompt: no index-wide
   summary, no memory of previous questions beyond the supplied `history`.
3. **Generate.** Produce the answer with inline citation markers of the form
   `[n]` referring to the nth retrieved record.
4. **Verify.** Reject the answer, and fall back to the plain result list, when
   any of these hold: a citation marker refers to a record not retrieved; the
   answer contains a number that appears in no retrieved record; every sentence
   is uncited.
5. **Return.** Answer, citations mapped to `objectID`, the retrieved hits, and
   `answerConfidence` in zero to one.

Step 4 is not optional and is not a filter on words. It is a check that every
factual claim traces to a retrieved record, and a build without it will state
prices that no product has, which is the failure mode that gets this feature
switched off in production.

### 25.5 The streaming contract

`stream: true` responds with server-sent events, content type
`text/event-stream`, and these event names, in this order:

| Event | Payload | Notes |
|---|---|---|
| `retrieval` | `{hits:[...], queryID}` | sent before the first token, so the interface can render results while the answer is still writing |
| `token` | `{t:"..."}` | one or more tokens; no guarantee of word boundaries |
| `citation` | `{marker:1, objectID:"..."}` | may arrive before the marker's own token |
| `error` | `{code, message}` | terminal |
| `done` | `{answerConfidence, usage:{prompt,completion}}` | terminal |

The client must treat `token` payloads as an opaque byte stream and concatenate
without inserting spaces. Splitting a multi-byte character across two events is
legal and the client must buffer for it: assuming each event is a whole word
produces text that is subtly wrong in every language with accents and badly
wrong in Japanese.

Cancellation: the client closing the connection must stop generation within 200
milliseconds and must still write a `QueryEvent` with the partial usage. Billing
for a cancelled stream counts tokens actually generated, which is the only
number the client can also observe.

### 25.6 Guardrails and cost

| Control | Rule |
|---|---|
| Prompt injection | record text enters the prompt inside a delimited block, and instructions inside record text are never followed; the verifier in Section 25.4 step 4 is the backstop, not the defence |
| Key scope | an answer may only cite records the requesting key could have retrieved, including its `filters` restriction from Section 26.3 |
| Personal data | attributes named in `redactedAttributes` are stripped before grounding and may not appear in an answer |
| Cache | answers cache on `(index generation, normalized query, filters, key restriction digest, model)`, 15 minutes, and a cache hit sets `cached: true` and is not billed for completion tokens |
| Budget | per tenant, per calendar month in UTC; exceeding it returns 429 with code `answer_budget_exhausted` and does not degrade to a worse model silently |

The cache key includes the key restriction digest for a reason: two users of the
same tenant with different row-level filters must not share a cached answer, and
a build that caches on the query alone has built a data leak that is invisible in
testing because test tenants have one key.

> **In plain language.** Two things happen here that the front page promises.
>
> The first is understanding what you meant, not just what you typed. Searching
> for "something warm for a winter hike" finds a fleece even though the word
> fleece is nowhere in what you wrote. The system does this by holding a second,
> meaning-based way of looking things up alongside the word-based one, and then
> merging the two lists.
>
> How the merge works is worth one paragraph, because the tempting way is wrong.
> Each side produces a ranked list. The merge looks only at the positions in those
> lists, never at any internal confidence figure, because the two sides measure
> completely different things and the numbers do not mean the same thing. On top
> of the merge there is one protection: if you typed something that exactly matches
> a product, that product cannot be pushed off the top of the page by the
> meaning-based side deciding something else feels more relevant. Without that
> protection, searching for an exact product code returns a page of things that are
> vaguely similar to it, which people find maddening.
>
> The second thing is the written answer above the results. Ask a question, get a
> paragraph, with little numbered markers showing which products it came from.
>
> The rule that makes this safe to switch on is that the answer may only use the
> handful of items that were just retrieved, and every claim in it has to trace
> back to one of them. If a sentence mentions a price that appears in none of them,
> the answer is thrown away and you get the ordinary list of results instead. This
> check is the difference between a feature that ships and a feature that gets
> turned off in week two after it invents a delivery date.
>
> Two smaller things you can actually see. The results appear before the answer
> starts writing, so nothing waits on the slowest part. And if you navigate away
> mid-sentence, the writing stops rather than running on invisibly with somebody
> paying for it.

---

## 26. Tenancy, keys, quotas and limits

### 26.1 The tenancy model

Three levels: tenant, application, index. Every request resolves to exactly one
tenant, and no query may ever span two. Isolation is enforced at three points,
and all three are required because each covers the others' failure:

1. The key resolves to an application, which resolves to a tenant.
2. Every index name in a request is checked against the key's `indices` patterns.
3. Storage is partitioned by tenant, so a bug in the first two cannot read
   another tenant's bytes.

Within a tenant, row-level restriction is a filter carried by the key, not a
convention followed by the caller. See Section 26.3.

### 26.2 Key kinds

| Kind | Created by | Can | Never |
|---|---|---|---|
| `admin` | tenant owner, in the console | everything, including creating keys | leave the server, appear in a browser, or be logged |
| `ingest` | admin key | write records and settings | search, or read analytics |
| `search` | admin key | search, browse if granted | write anything |
| secured | derived from a `search` key, at runtime, on the caller's server | search within its embedded restrictions | be created client side |

Secrets are stored as `hashedSecret`, an Argon2id hash with parameters recorded
alongside the hash. Key values are shown once at creation and never again; an
interface offering "reveal key" has stored something it should not have.

### 26.3 Secured key derivation

A secured key embeds restrictions the holder cannot alter, and is generated on
the customer's own server, per end user. The algorithm is exact and every step
matters:

```
1. restrictions = the query string, url-encoded, with parameters sorted
   by name ascending, joined with "&". Example:
     filters=tenant%3Aacme&userToken=u_1029&validUntil=1767225600
2. signature = hex( HMAC-SHA256( key = parentSearchApiKey,
                                 message = restrictions ) )
3. securedKey = base64( signature + restrictions )
```

The order is signature first, then the restriction string, and the message
signed is the encoded string exactly as it will be transmitted. Two mistakes are
so common they are worth naming: signing the parameters before encoding them, so
the signature does not match what the server re-derives, and concatenating in
the other order, which produces a key that decodes into nonsense. Both fail
identically at the server with a 401, which sends the debugging in the wrong
direction.

Validation at the `edge`:

1. base64-decode; the first 64 characters are the hex signature, the rest is the
   restriction string.
2. Recompute the HMAC over the restriction string with every active parent
   search key of the application, and accept if any matches. Trying every parent
   is what allows a parent key to be rotated without invalidating live sessions.
3. Reject if `validUntil` is in the past. Reject if absent and the tenant
   requires it.
4. Merge restrictions into the request: `filters` from the key is combined with
   the request's own filters with `AND`, never replaced, and never merged with
   `OR`. `restrictIndices` is intersected with the requested index.
5. `userToken` from the key overrides any `userToken` in the request. A user may
   not choose their own personalization identity.

Step 4 is the whole security property. A build that lets the request's `filters`
replace the key's has built a system where the restriction is advisory.

### 26.4 The authorization decision, in order

```
1. key present and parseable                       else 401
2. signature valid, if secured                     else 401
3. not expired                                     else 401
4. referer matches, if the key restricts referers  else 403
5. action in acl                                   else 403
6. index in indices patterns                       else 403
7. rate limit and quota                            else 429
8. request-level limits, Section 20.7              else 422 or 413
```

A 403 must not distinguish "index does not exist" from "index not permitted",
because the difference is an enumeration oracle. A 404 is only correct once the
key is known to be allowed to see the index.

### 26.5 Quotas and rate limiting

Two independent mechanisms; both are required, and conflating them produces a
system that either throttles a paying customer for a burst or lets one customer
consume a month of capacity in an afternoon.

**Rate limit**, per key, token bucket:

```
capacity   = burst,      default 100 requests
refill     = rate,       default 10 requests per second, continuous
cost       = 1 for search, 5 for a batch write, 20 for an answer stream start
```

Refill is continuous, computed from elapsed time on each request. A fixed window
that resets on the second boundary allows twice the burst across a boundary and
produces the sawtooth every synthetic test misses and every real client finds.

**Quota**, per tenant, per calendar month in UTC:

| Unit | Counted as |
|---|---|
| search unit | one search request, or one facet-value search |
| record unit | one record stored, sampled hourly, billed on the maximum |
| answer unit | one thousand generated tokens, rounded up per request |

At 80 percent of quota, responses carry `X-Quota-Warning`. At 100 percent,
search continues and writes return 429; this asymmetry is deliberate, because
cutting search off takes down the customer's storefront, while pausing writes
degrades gracefully.

### 26.6 Audit

Every write, every key creation, every settings change and every rule change
writes an audit record: actor key id, action, index, a digest of the before and
after, request id, and timestamp. Audit records are append-only, are readable
with an admin key, and are retained for the tenant's `retentionDays` with a
floor of 90 days regardless of plan.

> **In plain language.** This section is about keeping customers apart, and about
> keeping one customer's users apart from each other.
>
> There are different sorts of pass. One opens everything and must never leave the
> customer's own servers. One only lets you put things in. One only lets you look
> things up, and that is the one that can be sent to a shopper's browser.
>
> The interesting one is the fourth. Say a company runs one catalogue shared by
> a thousand of its own clients, and each client must only ever see their own
> rows. The way that works is that the company's server mints a small, temporary
> pass per person, with the restriction baked into it and sealed with a signature.
> The person holding it cannot widen it. If they edit the restriction, the seal
> stops matching and the pass is refused.
>
> One detail decides whether this is real security or a polite suggestion: when
> the pass says "only these rows" and the request also asks for some rows, the two
> are combined so that both must be true. If the request's own filter is allowed to
> replace the one in the pass, anyone can see everything, and everything will look
> completely normal in testing.
>
> The rest is fair use. There are two separate limits and they do different jobs.
> One stops a single burst of traffic from swamping the service, and it tops up
> continuously, like a dripping tap filling a bucket, rather than resetting on the
> hour. The other is the monthly allowance. When a customer runs out of allowance,
> searching keeps working and adding new data stops, because turning off search
> takes their shop down, and pausing new stock does not.

---

## 27. Events, analytics and the metrics contract

### 27.1 Intake

```
POST /1/events
  { "events": [ { "eventType":"click", "eventName":"Product Clicked",
                  "index":"products", "userToken":"u_1029",
                  "objectIDs":["p_88"], "positions":[3],
                  "queryID":"8f3c...", "timestamp": 1767225600123 } ] }
  -> 200 { "status": 200, "message": "OK" }
```

Intake is fire and forget from the client's point of view and is accepted with a
200 even when individual events are dropped, with the count of accepted events
in the body. The reason is that this call is made from a page during navigation,
often through `sendBeacon`, and a client that retries on failure will double
count far more often than it will recover a lost event.

Validation, and what each failure does:

| Condition | Result |
|---|---|
| `timestamp` more than 4 days old | dropped, counted in `dropped.stale` |
| `timestamp` more than 1 hour in the future | clamped to receipt time |
| `queryID` present, `positions` absent on a click | dropped, counted in `dropped.malformed` |
| `objectIDs` longer than 20 | dropped |
| `userToken` absent | dropped, this event type requires it |
| unknown `index` | dropped |

### 27.2 Attribution

A `click` or `conversion` carrying a `queryID` is **attributed** to that search.
Without a `queryID` it is counted but unattributed, and the two are never mixed
in one metric.

The attribution window is 24 hours from the `QueryEvent`, extended to 30 days
for `conversion` when `authenticatedUserToken` is present, because a purchase
that happens a week later on another device is still the search's doing and is
the number the customer is trying to justify a renewal with.

`variantId` is inherited from the `QueryEvent`, never re-derived. See
Section 24.4.

### 27.3 Deduplication and lateness

Deduplication key: `(userToken, eventType, objectID, queryID, floor(timestamp / 60000))`.
Two events with the same key inside the same minute are one event. This absorbs
the double-fire from a client that both listens for a click and re-renders, and
it is deliberately not narrower: exact-timestamp deduplication catches nothing,
because the two fires differ by a millisecond.

Late events arriving after their hour has been rolled up trigger a **rewrite**
of that hour's aggregate, up to 4 days back. Rollups are therefore idempotent
recomputations from raw events, not incremental counters. An incremental counter
cannot absorb a late event and cannot be repaired after a bad deploy without
replaying, which is the same amount of work with none of the safety.

### 27.4 Rollups

The `roller` computes, per index, per hour, in UTC:

| Table | Grain | Fields |
|---|---|---|
| `searches_hourly` | index, hour | count, users, noResultCount, avgProcessingMs, p95ProcessingMs |
| `queries_hourly` | index, hour, normalized query | count, users, clickCount, conversionCount, noResultRate |
| `hits_hourly` | index, hour, objectID | impressions, clicks, conversions, sumPosition |
| `filters_hourly` | index, hour, facet, value | count |
| `variants_hourly` | index, hour, abTestId, variantId | searches, users, clicks, conversions, revenue |

Hour boundaries are UTC and the dashboard converts for display. Rolling up in
the viewer's local timezone means two viewers of the same account see different
totals, and a customer in one zone cannot reconcile a report with their own
records.

### 27.5 Metric definitions

Stated exactly, because every one of these has a plausible wrong version:

| Metric | Definition |
|---|---|
| Click-through rate | attributed clicks divided by **searches that returned at least one hit**, not by all searches |
| Conversion rate | attributed conversions divided by the same denominator |
| No-results rate | searches with `nbHits` 0 divided by all searches, including those a rule rewrote |
| Average click position | mean of `positions`, over attributed clicks only, 1-based |
| Users | distinct `userToken` in the period, not summed across sub-periods |

The last row is the one that produces bug reports: distinct counts do not add.
The daily user count is not the sum of the hourly ones, and a dashboard that
sums them will show more users in a day than the account has ever had. Distinct
counts are computed from a sketch, HyperLogLog with a relative error under 2
percent, stored per grain and merged when a wider period is requested.

### 27.6 What the console reads

The analytics screens in Section 16.5 read only the rollup tables, never raw
events. A screen that queries raw events is fast on a demo account and unusable
on a real one, and the difference does not appear until after launch.

> **In plain language.** Every search, click and purchase is recorded so the
> customer can see whether search is earning its keep.
>
> Two decisions in here decide whether those numbers can be trusted.
>
> The first is that a click has to be tied to the search that produced it. The
> search hands out a small ticket number, the page hands the ticket back when
> somebody clicks a result, and that is how "this search led to this sale" is
> known rather than guessed. Purchases count for a month afterwards when the
> shopper is signed in, because a sofa gets searched for on Tuesday and bought the
> following weekend, and that sale belongs to the search.
>
> The second is that the totals are rebuilt from the raw record rather than
> counted up as they arrive. It sounds like extra work. It is what allows an
> event that turns up two days late, because somebody's phone was in a tunnel, to
> be slotted into the right hour rather than counted in the wrong one or thrown
> away. It also means a mistake in the counting can be fixed by recounting instead
> of by apologising.
>
> One warning that saves an embarrassing report: visitor counts cannot be added
> up. The same person searching on Monday and Tuesday is one visitor for the
> week, not two, so a weekly figure is not the sum of the daily ones. A dashboard
> that adds them will confidently show more visitors than the shop has ever had.

---

## 28. Consistency, replication and operations

### 28.1 The cluster

Each application is served by a cluster of three machines per region, each
holding a full copy of every index in the application. There is no sharding of an
index across machines at this size, which removes distributed ranking and its
merge-of-partial-results problems entirely. Growth beyond one machine's capacity
is a separate cluster, not a shard.

Writes go to the region's leader, are replicated to the two followers, and a task
is `published` only when a quorum of two has applied it. Reads go to any of the
three.

### 28.2 Read-your-writes

Replication is asynchronous, so a read immediately after a write may not see it.
The system does not pretend otherwise; it gives the caller the tool to wait:

- Every write returns `taskID`.
- `waitTask` polls until the task is published on every machine in the region.
- A read may carry `X-Min-Task: <taskID>`, and the `searcher` either
  serves from a generation at or beyond that task or returns 503 with
  `Retry-After: 1`, rather than serving stale data silently.

The console uses the header on the screen immediately after a write, and
`waitTask` nowhere in an interactive path, because a synchronous wait in a form
submission turns a 40 millisecond write into a 2 second one.

### 28.3 Replicas

| Kind | Copies records | Own settings | Use |
|---|---|---|---|
| standard | yes, full copy | all settings independent | a different `searchableAttributes` or a different engine configuration |
| virtual | no, shares the primary's data | only `customRanking` and a few sort settings | an alternate sort order, which is the common case |

A virtual replica costs no extra records against the tenant's quota and is the
correct answer to "sort by price". A standard replica for a sort order doubles
the record count and doubles the write cost, and this is the most common
avoidable bill on the platform.

Writes go to the primary only. A write to a replica is 403 with code
`write_to_replica`. Settings that are shared, and settings that are per replica,
must be listed in the console next to each field rather than in documentation,
because the split is not guessable.

### 28.4 Client behaviour

The client library is part of the contract, not an afterthought:

- Hosts are tried in order: the primary, then three fallback hosts in a
  **randomized** order per client instance, so a failure does not stampede one
  fallback.
- A host that fails is marked down for 5 minutes and skipped.
- Retry on: connection failure, timeout, 5xx. Never retry on: 4xx other than
  429, and never retry a non-idempotent write without an idempotency key.
- Timeouts: 2 seconds connect, 5 seconds read for search, 30 seconds for write,
  no read timeout for a stream.
- Backoff: on 429, honour `Retry-After` exactly; otherwise exponential from 200
  milliseconds with full jitter, capped at 10 seconds.

### 28.5 Degradation

Under load the service sheds work in this order, and the order is a product
decision rather than an engineering one:

```
1. answer generation             (expensive, has a result-list fallback)
2. personalization               (a reordering, not a result set)
3. disjunctive facet counts      (degrade to conjunctive, flag it)
4. vector retrieval              (fall back to keyword, flag it)
5. keyword search                (never shed; shed the tenant instead)
```

Every degradation sets a flag in the response: `degraded: ["facets","vector"]`.
A silent degradation is worse than an error, because the customer tunes
relevance against results that were never the real ones.

### 28.6 Observability

Per request, recorded: request id, tenant, index, key id, generation, stage
timings for the fourteen steps in Section 23.7, candidate counts before and
after each stage, and the flags in Section 22.13.

The stage timings are not for a dashboard. They are the only way to answer "why
was this query slow", and the answer is nearly always one of three things: a
prefix walk that expanded to the bound, a disjunctive facet pass over a large
result set, or highlighting applied before pagination. All three are visible in
the stage timings and invisible in a total.

> **In plain language.** This section is about what happens when machines are
> involved, which is to say when things are briefly out of step or partly broken.
>
> Data lives on three machines per region. Writing goes to one and spreads to the
> others in a moment. That moment is real, so if you add a product and immediately
> search for it, it might not be there yet. Rather than pretend otherwise, the
> service hands back a receipt with every change, and anything that genuinely
> needs the change to be visible can present the receipt and be told to wait a beat
> rather than be quietly given the old answer.
>
> There is a cheap way and an expensive way to offer a second sort order, such as
> "price, low to high". The cheap way keeps one copy of the data and just orders it
> differently. The expensive way keeps a whole second copy, doubling both the
> storage bill and the work of every update. They look the same from the outside,
> and picking the expensive one by accident is the most common way customers end
> up overpaying.
>
> The most human part of this section is what gets dropped when the service is
> overloaded. There is a fixed order. The written answer goes first, because there
> is a perfectly good list of results underneath it. Then the personal touch. Then
> the exact numbers beside the filters. Then the meaning-based half of the search.
> Plain word search is never dropped.
>
> And every time something is dropped, the response says so. A customer tuning
> their results against a page that was quietly missing half its machinery will
> tune it wrong, and then wonder why it behaves differently tomorrow.

---
## 29. Where a generated build most often fails

### 29.1 Why this section exists

This document will mostly be built by a machine, and machines fail at this
particular specification in ways that are consistent enough to enumerate. The
failures share a shape: the wrong behaviour is the one that appears most often
in training material, is simpler to implement, passes a naive test, and is
invisible in a demonstration with twenty records.

So this section is not a summary of the ones before it. It is a list of the
specific places where the obvious implementation is the wrong one, what the
wrong one looks like when it ships, and the test in Section 30 that catches it.
Each entry names the section that carries the actual specification, so nothing
here is a second, drifting source of truth.

An implementer, human or otherwise, should read this section **before** writing
Sections 21 to 28, not after.

### 29.2 The trap table

| # | Where | The obvious implementation | Why it is wrong | Caught by |
|---|---|---|---|---|
| 1 | Section 22.5 | one relevance score per hit, sort by it | the cascade is eight sequential tie-breaks; a score cannot express "never trade a typo for popularity" | Section 30.3 |
| 2 | Section 23.4 | one grouped pass for all facet counts | a facet being filtered on must be counted with its own filter removed | Section 30.4 |
| 3 | Section 23.6 | deduplicate the page after pagination | deduplication precedes pagination, and `nbHits` counts groups | Section 30.5 |
| 4 | Section 22.2 | Levenshtein distance | transposition must cost 1; `hlelo` is one typo from `hello` | Section 30.2 |
| 5 | Section 22.2 | allow any single edit | the first character may never be edited, and digits get no tolerance | Section 30.2 |
| 6 | Section 21.4 | prefix-match every word | only the last word is a prefix by default | Section 30.2 |
| 7 | Section 22.11 | highlight the folded text | tags go into the original text at recorded offsets; folding changes lengths | Section 30.6 |
| 8 | Section 23.2 | flatten the nested filter array | nesting is the boolean structure: outer AND, inner OR | Section 30.4 |
| 9 | Section 23.1 | left-to-right filter evaluation | `NOT` then `AND` then `OR`, as in arithmetic | Section 30.4 |
| 10 | Section 22.4 | remove a word and append the new hits | each removal round is a complete, separately ranked pass, concatenated in round order | Section 30.3 |
| 11 | Section 26.3 | sign the parameters before encoding, or concatenate restrictions before signature | signature first, over the encoded string exactly as sent | Section 30.7 |
| 12 | Section 26.3 | let the request's filters replace the key's | they are combined with AND; the key's restriction is a floor | Section 30.7 |
| 13 | Section 21.5 | implement `Increment` and stop | `IncrementFrom` and `IncrementSet` are what make a retry safe | Section 30.8 |
| 14 | Section 21.6 | assume the temporary index inherits settings | it inherits nothing, and `move` destroys the destination's configuration | Section 30.8 |
| 15 | Section 21.7 | one global task counter | `taskID` is monotonic per index and not comparable across indices | Section 30.8 |
| 16 | Section 24.4 | assign the A/B variant per request | assignment is a deterministic hash of the user token, stable for the test's life | Section 30.9 |
| 17 | Section 25.3 | normalize both scores and add them | the keyword side has no score; fusion is over ranks | Section 30.10 |
| 18 | Section 25.2 | retrieve neighbours then apply filters | filters must be applied inside the graph walk or a selective filter empties the page | Section 30.10 |
| 19 | Section 22.10 | compare raw distances | distance is bucketed, or geo becomes a total order and starves every criterion under it | Section 30.3 |
| 20 | Section 22.12 | `nbPages` from `nbHits` alone | the pagination cap also bounds it, and an over-cap offset is 422 | Section 30.5 |
| 21 | Section 27.5 | sum hourly user counts for a daily figure | distinct counts do not add; merge sketches instead | Section 30.11 |
| 22 | Section 27.3 | increment counters as events arrive | rollups are idempotent recomputations, so a late event can be absorbed | Section 30.11 |
| 23 | Section 26.5 | fixed-window rate limiting | a fixed window permits double the burst across its boundary | Section 30.7 |
| 24 | Section 24.1 | treat every synonym match as exact | `alternativesAsExact` decides, and multi-word synonyms are excluded by default | Section 30.3 |
| 25 | Section 21.2 | `toLowerCase()` and strip accents | full case folding, per-language exemptions, and script-aware tokenization | Section 30.2 |
| 26 | Section 25.6 | cache answers on the query string | the cache key must include the key restriction digest, or tenants leak into each other | Section 30.10 |
| 27 | Section 22.5 | leave ties unordered | a final tie-break on `objectID` is required, or pagination repeats and omits hits | Section 30.5 |
| 28 | Section 28.5 | degrade silently under load | every degradation must be flagged in the response | Section 30.12 |
| 29 | Section 24.2 | apply promotions before ranking | promotions are positional and are applied after ranking, and hides beat promotes | Section 30.9 |
| 30 | Section 20.6 | treat a repeated idempotency key as a fresh write | replay the stored response; a different body under the same key is a 422 | Section 30.8 |

### 29.3 The four that are worth expanding

Thirty entries is a checklist. Four of them are worth the space to state
completely, because they are the ones where a build can look finished, pass a
casual review, and be wrong in production.

#### 29.3.1 The cascade is not a score

The wrong version, in full, because it is what will be written otherwise:

```
score = w1 * textMatch + w2 * popularity + w3 * recency ...
sort by score descending
```

This produces plausible results on any small corpus and cannot be tuned. The
merchandiser's requirement is not "weight popularity a bit less". It is "a
misspelled match may never outrank a correct one", which is a lexicographic
constraint, not a weight. No assignment of `w1`, `w2` and `w3` satisfies it for
all data, and every attempt produces a system where tuning one query breaks
another, which is how a search project acquires a reputation for being
unfixable.

The correct version compares two hits criterion by criterion and returns on the
first difference:

```
for criterion in ranking:            # the eight, in order, Section 22.5
    d = compare(a, b, criterion)
    if d != 0: return d
return compare(a.objectID, b.objectID)
```

The tell, in a code review: if there is a floating point `score` field anywhere
in the ranking path, the build is wrong.

#### 29.3.2 Disjunctive facet counts

Stated as a worked example, because prose has failed here before.

Corpus: 10 red Acme, 5 blue Acme, 20 red Zeta, 1 blue Zeta.
Interface: brand is multi-select, colour is multi-select.
User state: brand Acme ticked, colour red ticked.

| Facet value | Wrong count | Right count | Why |
|---|---|---|---|
| brand: Acme | 10 | 10 | matches everything selected |
| brand: Zeta | 0 | 20 | count brands with the brand filter removed: red Zeta |
| colour: red | 10 | 10 | matches everything selected |
| colour: blue | 0 | 5 | count colours with the colour filter removed: blue Acme |

The wrong column is what a single pass over the result set produces, and it is
recognizable on screen: every unticked box shows zero, so the filter list can
only ever be narrowed and never widened. Two extra evaluations produce the right
column, one per disjunctive attribute, over bitmaps.

#### 29.3.3 Secured keys

The failure is not subtle in effect and is entirely invisible in a single-tenant
test, because a single-tenant test has nothing to leak into.

```
correct:   securedKey = base64( hexHmac( parentKey, encodedRestrictions )
                                + encodedRestrictions )
           serverFilters = keyFilters AND requestFilters

common wrong 1: sign the decoded restrictions, transmit the encoded ones
                -> every key fails validation, 401, and debugging goes to the
                   key rotation code

common wrong 2: base64( restrictions + signature )
                -> the server reads the first 64 characters as a signature and
                   gets restriction text, 401 again

common wrong 3: serverFilters = requestFilters when present
                -> every restriction is advisory; any user of the tenant can
                   read every row by sending their own filter. No test fails.
```

Wrong 3 is the one to fear. The first two break loudly. The third ships.

#### 29.3.4 Deduplication, counting and pagination

Corpus: 300 shirts, each in 4 colours, one record per colour, 1200 records.
Settings: `attributeForDistinct: "shirtId"`, `distinct: 1`, `hitsPerPage: 20`.

| Field | Wrong | Right |
|---|---|---|
| `nbHits` | 1200 | 300 |
| `nbPages` | 60 | 15 |
| hits on page 0 | 20 records, possibly 5 shirts | 20 shirts |
| `facets.colour.red` | 300 | 300, and 75 when `facetingAfterDistinct` is true |

The wrong column is what deduplicating the twenty hits on the page produces. The
symptom a user reports is "it says twelve hundred results but the list ends
after fifteen pages", and the symptom the merchandiser reports is that the
colour filter numbers do not match the number of rows they can see. Both come
from the same missing ordering: deduplicate first, count groups, then paginate.

### 29.4 Failure modes that are not in the table

Three classes of failure are not enumerated above because they are failures of
scope rather than of detail. They are listed here so that a reviewer can name
them.

**Stubbing the engine.** Delivering the pages with a search box that filters an
in-memory array. Everything in Sections 21 to 28 then has no implementation, and
the build's own acceptance suite in Section 30 will not run at all. This is the
single most likely outcome of handing this document to a builder with a fixed
budget, and Section 36 exists to make it visible on day one rather than at
delivery.

**Implementing the surface and not the ordering.** Every route, every component,
every parameter accepted, and a ranking that is a score. This is the failure
this section is mostly about.

**Implementing the ordering and not the honesty.** Every flag in Section 22.13
returned as a constant: `exhaustiveNbHits` always true, `exhaustiveFacetsCount`
always true, `degraded` always empty. The engine is then correct and
unmaintainable, because no one can tell a wrong answer from a truncated one.

> **In plain language.** This section is unusual and it is deliberate, so it is
> worth explaining what it is for.
>
> Most of this document will be built by a machine rather than by a person. There
> is a set of mistakes that machines make on work like this, over and over, and
> they are all the same kind of mistake: the version that is easier to build, that
> is what most textbooks describe, that works perfectly on a demonstration with
> twenty products, and that falls apart on a real catalogue in a way nobody can
> see from the outside.
>
> So this section is a list of thirty of those, written out as "here is what will
> be built if nobody says otherwise, here is why it is wrong, and here is the test
> that catches it". Four of them are explained at length because they are the ones
> that can pass a review and still be wrong.
>
> If you only remember two, remember these.
>
> The first: results are ordered by a series of tie-breaks, not by a single grade
> out of ten. The grade is easier and it makes the results impossible to tune
> afterwards, which is the complaint that ends search projects.
>
> The second: when a shopper ticks one brand, the numbers beside the other brands
> must still be right, which means quietly running the search a second time. Skip
> it and the filters stop working the moment anyone picks two of anything.
>
> There is also a note at the end about three ways to fail that are not details
> at all. The likeliest is that the whole engine gets skipped and replaced with
> something that filters a short list in the page, because that is what fits a
> small budget. The result looks right in a demonstration and cannot be sold.

---

## 30. The conformance suite

### 30.1 How the suite is run

The suite is a fixture corpus and a list of assertions. It is not optional and
it is not a smoke test: the acceptance checklist in Section 36 treats a failing
assertion here as a failing build.

```
fixtures/corpus.jsonl     2,000 records, generated by the seeded generator in
                          Section 33.6, deterministic for a given seed
fixtures/settings.json    the index settings each case starts from
suite/*.case              one case per assertion: request, expected response
                          fragment, and the section it enforces
```

Every case names the section it enforces and the trap number in Section 29.2 it
catches. A case that cannot name one does not belong in the suite.

Comparison is a **subset match** on the response: the expected fragment must be
present, and unspecified fields are ignored. Ordering assertions compare the
full ordered list of `objectID`.

### 30.2 Text pipeline and typo tolerance

Corpus fragment:

```
{ "objectID":"t1", "title":"Hello World" }
{ "objectID":"t2", "title":"Helo Word" }
{ "objectID":"t3", "title":"Crème Brûlée" }
{ "objectID":"t4", "title":"2024 Edition" }
{ "objectID":"t5", "title":"2025 Edition" }
{ "objectID":"t6", "title":"東京都庁" }
{ "objectID":"t7", "title":"Straße" }
```

| Case | Query | Expected | Enforces |
|---|---|---|---|
| 2a | `hello` | `t1` before `t2` | Section 22.5, criterion 1 |
| 2b | `hlelo` | `t1` present, `nbTypos` 1 | Section 22.2, transposition |
| 2c | `xello` | `t1` absent | Section 22.2, first character |
| 2d | `creme` | `t3` present | Section 21.2, folding |
| 2e | `crème` | `t3` present | Section 21.2, folding |
| 2f | `2024` | `t4` only, `t5` absent | Section 22.2, digits |
| 2g | `strasse` | `t7` present | Section 21.2, full case folding |
| 2h | `東京` | `t6` present | Section 21.2, bigrams |
| 2i | `hel` | `t1` and `t2` present | Section 21.4, prefix on last word |
| 2j | `hel world` | `t1` present, `t2` absent | Section 21.4, prefix only on last |
| 2k | `wor hello` | `t1` present | Section 22.3, order independent matching |

### 30.3 The ranking cascade

Corpus fragment, all with `popularity` in the record and
`customRanking: ["desc(popularity)"]`:

```
{ "objectID":"r1", "title":"Blue Running Shoes", "popularity": 1 }
{ "objectID":"r2", "title":"Blue Runing Shoes",  "popularity": 100 }
{ "objectID":"r3", "title":"Shoes Running Blue", "popularity": 50 }
{ "objectID":"r4", "title":"Blue Shoes",         "popularity": 90, "extra":"running" }
```

| Case | Query | Expected order | Enforces |
|---|---|---|---|
| 3a | `blue running shoes` | `r1, r3, r4, r2` | Section 22.5, typo before custom |
| 3b | `blue running shoes` with `customRanking` removed | `r1, r3, r4, r2` | the cascade does not depend on custom ranking |
| 3c | `blue running shoes`, `typoTolerance: false` | `r1, r3, r4`, `r2` absent | Section 22.2 |
| 3d | `blue shoes` | `r4` before `r1` | Section 22.6, proximity |
| 3e | `running blue shoes` | `r3` before `r1` on proximity, `r1` before `r3` on attribute if title order differs | Sections 22.6, 22.7 |

Case 3a is the single most important assertion in the suite. `r2` is the most
popular record by a wide margin and carries one typo, so it must be **last**. A
build using a weighted score puts it first, and case 3a is the two-line test
that catches it.

Word removal:

```
| 3f | `blue running shoes umbrella`, removeWordsIfNoResults lastWords
     | all four-word matches, then all three-word matches, no interleaving
     | Section 22.4 |
```

Geo bucketing, with three records at 5, 8 and 60 metres from the query point and
`popularity` 1, 100 and 50:

```
| 3g | aroundLatLng at the origin | the 5 and 8 metre records tie on geo, so
       popularity orders them: the 8 metre record first, then the 5 metre one,
       then the 60 metre one | Section 22.10 |
```

Case 3g is worth reading twice. The nearer record ranks second. That is correct,
and a build that returns them in distance order has made geo a total order.

### 30.4 Filters and facets

Corpus: the four-record brand and colour corpus from Section 29.3.2, expanded to
36 records.

| Case | Request | Expected | Enforces |
|---|---|---|---|
| 4a | `facetFilters: [["brand:acme","brand:zeta"]]` | both brands present | Section 23.2 |
| 4b | `facetFilters: ["brand:acme","colour:red"]` | only red Acme | Section 23.2 |
| 4c | `facetFilters: [["brand:acme"],["colour:red"]]` | same as 4b | Section 23.2 |
| 4d | 4b plus `facets: ["brand","colour"]`, both disjunctive | `brand.zeta` 20, `colour.blue` 5 | Section 23.4 |
| 4e | `filters: "a:1 OR b:2 AND c:3"` | parses as `a:1 OR (b:2 AND c:3)` | Section 23.1 |
| 4f | `filters: "price > \"10\""` | 422, code `invalid_filter` | Section 23.1 |
| 4g | ticked facet value with 0 matches under the pruned tree | returned with count 0 | Section 23.4 |
| 4h | `facets_stats` on a filtered price range | min and max span the unfiltered range | Section 23.4 |

### 30.5 Deduplication, pagination and stability

Fixture: the 1200-record shirt corpus from Section 29.3.4.

| Case | Request | Expected | Enforces |
|---|---|---|---|
| 5a | `distinct: 1`, page 0 | `nbHits` 300, `nbPages` 15, 20 distinct `shirtId` | Section 23.6 |
| 5b | `distinct: 1`, `facetingAfterDistinct: true` | `facets.colour.red` 75 | Section 23.6 |
| 5c | pages 0 to 14 collected | 300 objectIDs, no duplicates, no omissions | Section 22.5, stability |
| 5d | `paginationLimitedTo: 100`, page 6 | 422 | Section 22.12 |
| 5e | same query run 50 times | byte-identical ordering | Section 22.5, final tie-break |
| 5f | a promoted record inside a deduplicated group | promoted record present and its group still contributes one hit | Sections 23.6, 24.2 |

### 30.6 Highlighting

| Case | Record | Query | Expected `_highlightResult` | Enforces |
|---|---|---|---|---|
| 6a | `Crème Brulee` | `creme` | `<em>Crème</em> Brulee` | Section 22.11, offsets into the original |
| 6b | `Straße 12` | `strasse` | `<em>Straße</em> 12` | Section 22.11, folding changes length |
| 6c | `Hello World` | `hel` | `<em>Hel</em>lo World` | Section 22.11, prefix highlights the prefix |
| 6d | `red red red` | `red` | three separate tag pairs | Section 22.11, no merge across spaces |
| 6e | `Hello World` | `hello world` | `matchLevel: "full"` | Section 22.11 |
| 6f | 200-word description, `attributesToSnippet: ["desc:20"]` | 20 words centred on the match, ellipsis both sides | Section 22.11 |

Cases 6a and 6b are the folding-offset test. A build that highlights the folded
text returns `<em>Creme</em> Brulee`, which has changed the user's data, or
misplaces the tags by one character on `Straße`, which is worse because it looks
like a rendering bug.

### 30.7 Keys, restrictions and limits

| Case | Setup | Expected | Enforces |
|---|---|---|---|
| 7a | secured key with `filters=tenant:acme`, request with no filters | results restricted to `tenant:acme` | Section 26.3 |
| 7b | secured key as above, request with `filters=tenant:zeta` | zero hits, not zeta's hits | Section 26.3, AND combination |
| 7c | secured key with a tampered restriction string | 401 | Section 26.3 |
| 7d | secured key generated against a rotated-out parent | 401; against either active parent, 200 | Section 26.3 |
| 7e | `validUntil` in the past | 401 | Section 26.3 |
| 7f | search key requesting an index outside its patterns | 403, and the message identical to a non-existent index | Section 26.4 |
| 7g | 100 requests instantly, then 10 per second sustained | no 429 | Section 26.5 |
| 7h | 200 requests instantly | roughly 100 succeed, the rest 429 with `Retry-After` | Section 26.5 |
| 7i | 100 requests in the last 100 milliseconds of one second and 100 in the first 100 of the next | the second hundred are throttled | Section 26.5, continuous refill |

Case 7i is the fixed-window test. A window-based limiter passes 7g and 7h and
fails 7i, and 7i is the one that matches real traffic.

### 30.8 Writes, tasks and idempotency

| Case | Sequence | Expected | Enforces |
|---|---|---|---|
| 8a | batch of 1000 with one over-size record | 999 applied, one `null` in `objectIDs` | Section 21.1 |
| 8b | `Increment` applied twice | value moved by twice the amount | Section 21.5 |
| 8c | `IncrementFrom` value 4 applied twice | second returns 422 `condition_not_met`, value is 5 | Section 21.5 |
| 8d | `IncrementSet` 7 then `IncrementSet` 6 | value 7 | Section 21.5 |
| 8e | `partialUpdateObject` with a nested object | the nested object is replaced whole, not merged | Section 21.5 |
| 8f | reindex without copying settings, then `move` | settings lost; the case asserts the documented sequence restores them | Section 21.6 |
| 8g | `taskID` values from two indices | not comparable; the case asserts each index's sequence is independently monotonic | Section 21.7 |
| 8h | same idempotency key, same body, twice | one task, second response identical with `Idempotent-Replay` | Section 20.6 |
| 8i | same idempotency key, different body | 422 `idempotency_key_reuse` | Section 20.6 |
| 8j | delete then immediate search | deleted record absent; `nbHits` excludes it | Section 21.8 |

### 30.9 Rules, synonyms and tests

| Case | Setup | Expected | Enforces |
|---|---|---|---|
| 9a | rule promoting `p9` to position 0 for query `sofa` | `p9` first | Section 24.2 |
| 9b | 9a plus a rule hiding `p9` | `p9` absent | Section 24.2, hide beats promote |
| 9c | two rules promoting to position 0 | lower `priority` wins, the other takes position 1 | Section 24.2 |
| 9d | promotion to position 25 with `hitsPerPage` 20 | dropped, reported `applied: false` | Section 24.2 |
| 9e | promotion of a filtered-out record | not promoted | Section 24.6 |
| 9f | multi-word synonym `bike` to `mountain bike` | matches only records with the two words adjacent | Section 24.1 |
| 9g | one-word synonym, default `alternativesAsExact` | counts as exact | Sections 22.8, 24.1 |
| 9h | multi-word synonym, default settings | does not count as exact | Sections 22.8, 24.1 |
| 9i | same `userToken`, 100 requests, running A/B test | same variant every time | Section 24.4 |
| 9j | no `userToken`, running A/B test | control, and excluded from `variants_hourly` | Section 24.4 |
| 9k | personalized user who prefers brand zeta, query `acme` | an exact acme match outranks a typo-matched zeta record | Section 24.3 |

Case 9k is the personalization placement test, and it is the one that decides
whether the feature is safe to enable for a customer.

### 30.10 Hybrid retrieval and answers

| Case | Setup | Expected | Enforces |
|---|---|---|---|
| 10a | `semanticRatio: 0` | byte-identical to vector search disabled | Section 25.3 |
| 10b | `semanticRatio: 1` | byte-identical to keyword disabled | Section 25.3 |
| 10c | exact product code query, semantic on | the exact match at position 10 or better, `exactLiftApplied` set if lifted | Section 25.3 |
| 10d | vector search with a filter matching 12 of 100000 records | 12 hits, not 0 to 3 | Section 25.2 |
| 10e | index with mixed `modelId` vectors | `vectorIndexStale: true`, keyword-only results | Section 25.1 |
| 10f | answer whose draft cites a record not retrieved | answer suppressed, result list returned | Section 25.4 |
| 10g | answer request from two keys with different restrictions, same query | two distinct cache entries | Section 25.6 |
| 10h | client disconnects mid-stream | generation stops, `QueryEvent` written with partial usage | Section 25.5 |
| 10i | multi-byte character split across two `token` events | client assembles correctly | Section 25.5 |

### 30.11 Analytics

| Case | Sequence | Expected | Enforces |
|---|---|---|---|
| 11a | click without `positions` but with `queryID` | dropped, counted in `dropped.malformed` | Section 27.1 |
| 11b | same click event fired twice 40 milliseconds apart | one event | Section 27.3 |
| 11c | event with a timestamp 3 days old | accepted, and the affected hour is recomputed | Section 27.3 |
| 11d | event with a timestamp 5 days old | dropped as stale | Section 27.1 |
| 11e | one user searching in two hours | daily distinct users is 1 | Section 27.5 |
| 11f | CTR with 100 searches of which 20 returned nothing | denominator is 80 | Section 27.5 |
| 11g | conversion 8 days after the search, signed in | attributed | Section 27.2 |
| 11h | conversion 8 days after the search, anonymous | unattributed but counted | Section 27.2 |
| 11i | A/B variant edited mid-test, then rolled up | events keep their recorded variant | Section 24.4 |

### 30.12 Degradation and honesty

| Case | Setup | Expected | Enforces |
|---|---|---|---|
| 12a | facet pass forced to time out | `degraded` contains the facet stage, counts marked non-exhaustive | Section 28.5 |
| 12b | prefix expansion hits its bound | `exhaustiveTypo: false` | Section 21.4 |
| 12c | facet values truncated at `maxValuesPerFacet` | `exhaustiveFacetsCount: false` | Section 23.4 |
| 12d | vector backend unavailable | keyword results, `degraded` contains the vector stage | Section 28.5 |
| 12e | write while over quota | 429, and search in the same window still 200 | Section 26.5 |
| 12f | read with `X-Min-Task` ahead of the replica | 503 with `Retry-After`, never stale data | Section 28.2 |

> **In plain language.** This is the exam, and it is what "finished" means.
>
> Everything in the specification that could be built two ways has a test here
> that tells the two apart, using a small, fixed set of made-up products so that
> anyone can run it and get the same answer. Each test also says which mistake it
> is looking for, so a failure points at a paragraph rather than at a mood.
>
> A handful of them are worth knowing about even if you never run one.
>
> There is a test with four pairs of running shoes where one of them is spelled
> wrong and is a hundred times more popular than the rest. It has to come last. If
> it comes first, the results are being ordered by a single popularity-flavoured
> grade, and no amount of later tuning will fix it.
>
> There is a test where the shopper ticks one brand and one colour, and the numbers
> beside every other brand and colour have to stay truthful.
>
> There is a test with three shops at five, eight and sixty paces away, where the
> one at eight paces has to come first, because the two nearest count as equally
> near and the shop's own ordering breaks the tie. That looks wrong until you know
> why, which is exactly why it is written down.
>
> And there is a test that runs the same search fifty times and demands the same
> answer every time, in the same order. It sounds trivial. It is the test that
> stops the same product appearing on page one and again on page two.

---
## 31. Accessibility

This section sits here, after the service, because it covers three surfaces and
one of them did not exist until Section 16: the marketing routes, the search
interface of Section 8, and the console. The search interface is the hard one,
and it is hard in a way that has nothing to do with the marketing pages.

Everything in this section is normative. Where the reference site was measured
to do something, the measurement is quoted; where it was not, the requirement
stands anyway.

### 31.1 Landmarks and headings

One `banner`, one `navigation` in the header, one `main`, one `contentinfo` per
route. Every route has exactly one first-level heading, and heading levels
descend without skipping. The section headings of the home route in Section 9
carry the second level; the cards inside them carry the third.

The skip link is the first focusable element on every route, is visible on
focus, and moves focus to `main`. On the console it moves focus to the working
pane, not to the left rail, because the rail is the same on every screen.

### 31.2 Keyboard

Every interactive element is reachable and operable from the keyboard, in the
order it appears visually. Three components need explicit behaviour because the
obvious implementation is unusable:

**The header menus (Section 5.2).** Opened by Enter or Space, not by focus
alone. Arrow keys move between items. Escape closes and returns focus to the
trigger. Tab from the last item closes the menu and moves on rather than
trapping. A menu that opens on focus makes tabbing through the header a strobe
of opening and closing panels.

**The search box (Section 8).** This is a combobox over a live list:

| Key | Behaviour |
|---|---|
| Down, Up | move the active option; the input keeps focus throughout |
| Enter | open the active option, or submit the raw query if none is active |
| Escape | first press clears the list, second press clears the input |
| Tab | complete to the active option's text without opening it |
| Home, End | move within the text, never within the list |

The list is announced through a polite live region that reports the number of
results, not each result, and is rate limited to one announcement every 500
milliseconds. Announcing every keystroke's result count makes a screen reader
unusable while typing, which is the most common failure of an otherwise correct
search interface.

**The results and facets (Section 16.4).** Facet groups are grouped and labelled
as such. Toggling a facet does not move focus. The result count is announced
after each change, once the list has settled.

### 31.3 Focus

Focus is never removed, only restyled. The focus ring is a two-pixel outline
with a two-pixel offset, drawn in the colour token named in Section 3.2 that
meets contrast against both the light and the dark surface, so one ring works on
both. Focus is visible on the element that has it even when that element is
inside a scrolled container, which means containers scroll focus into view.

Route changes move focus to the new route's first-level heading, and the heading
takes `tabindex="-1"` for that purpose only.

### 31.4 Text alternatives

| Content | Requirement |
|---|---|
| Decorative marks and background art | hidden from assistive technology |
| Logos in the customer strip (Section 12) | the company name as text alternative |
| Icons that are the only content of a control | the control's purpose, not the icon's shape: "Search", not "magnifier" |
| The hero product panels (Section 9.2) | a text description of what the panel demonstrates, because the panel is the argument |
| Charts in the console (Section 16.5) | a data table behind a disclosure, with the same numbers |

### 31.5 Motion

`prefers-reduced-motion: reduce` removes every transform-based reveal, every
parallax, and the auto-advancing hero rotation in Section 9.2, and replaces them
with the end state. Opacity fades under 200 milliseconds may remain. Nothing
auto-advances under the reduced setting, and the rotation's controls stay.

Where the reference site was measured to auto-advance a panel, it is recorded in
Section 9.2 as measured, and the pause-on-hover and pause-on-focus behaviour
below is normative regardless of what was measured:

- Auto-advance pauses on hover, on focus within, and while the document is
  hidden.
- A visible pause control exists.
- No interval is under 5 seconds.

### 31.6 Contrast and colour

Text meets a contrast ratio of 4.5 to 1 against its background, large text 3 to
1, and interface component boundaries 3 to 1. The measured colour pairs used by
the reference are checked in Section 3.4, and any pair that fails is listed
there with the substitution made.

No information is carried by colour alone. The comparison grid in Section 10.4
uses a check and a cross glyph as well as colour; the console's status pills
carry text as well as fill.

### 31.7 Forms

Every input has a persistent visible label, not a placeholder standing in for
one. Errors are associated with their input, are announced, and are also
summarised at the top of the form with links to each field. Required fields are
marked in the label rather than only by an attribute. The demo request form in
Section 13 must be completable and submittable with the keyboard alone and
without a pointing device, which is checked in Section 36.

> **In plain language.** Someone using only a keyboard, or listening rather than
> looking, gets the same site and the same control room.
>
> Most of this is ordinary care: proper labels on every field, a visible ring
> showing where you are, headings in a sensible order, and never using colour on
> its own to tell you something, so the ticks and crosses in the comparison table
> are actual ticks and crosses.
>
> The search box is the part that takes real thought. It is a text field with a
> list of suggestions that changes as you type, which is genuinely difficult to
> make pleasant to listen to. The rules that matter: your typing is never
> interrupted, the arrow keys walk the suggestions while the cursor stays in the
> box, one press of escape clears the suggestions and a second clears the box, and
> the reader is told how many results there are rather than being read all of them
> every time you press a key. That last one is the difference between a search box
> that is usable without sight and one that is unbearable.
>
> Anyone who has told their computer they would rather things did not fly around
> gets the finished state of every animation instead of the animation, and nothing
> moves or advances on its own.

---

## 32. Build order

Ordered so something is visible early, each stage is checkable on its own, and
the two halves of the build, the site and the service, can proceed in parallel
after stage 3.

| Stage | Deliverable | Checkable by |
|---|---|---|
| 1 | Tokens, scale, colour, type, spacing, radii | a token sheet rendering every token at three widths |
| 2 | Global chrome: top bar, header, menus, mobile panel, footer | keyboard-only walk of every route |
| 3 | Icon set as inline geometry (Section 4) | an icon sheet at three sizes |
| 4 | Static home route, no motion | a full-page capture matching the reference at three widths |
| 5 | Remaining marketing routes, static | as above |
| 6 | Reveal system and the hero rotation | scroll the site with motion on; nothing pops, nothing auto-advances under the reduced setting |
| 7 | The site search surface (Section 8) against a stub | keyboard behaviour from Section 31.2 |
| 8 | **Service: storage, ingestion, the task queue** (Sections 20, 21) | conformance cases 8a to 8j |
| 9 | **Service: the text pipeline and the cascade** (Section 22) | conformance cases 2a to 2k, 3a to 3g |
| 10 | **Service: filters, facets, deduplication** (Section 23) | conformance cases 4a to 4h, 5a to 5f |
| 11 | **Service: keys, quotas, limits** (Section 26) | conformance cases 7a to 7i |
| 12 | Console: index list, record browser, tasks (Sections 16.3, 16.8) | an operator can load a catalogue and see it |
| 13 | Console: the search preview (Section 16.4) | the ranking disclosure explains case 3a |
| 14 | **Service: rules, synonyms, personalization, tests** (Section 24) | conformance cases 9a to 9k |
| 15 | Console: merchandising (Section 16.6) | a drag writes a rule that changes the preview |
| 16 | **Service: events and rollups** (Section 27) | conformance cases 11a to 11i |
| 17 | Console: analytics (Section 16.5) | figures match a hand count on the fixture corpus |
| 18 | **Service: vectors, fusion, answers** (Section 25) | conformance cases 10a to 10i |
| 19 | Site search wired to the real service, demo request form live | the home route search returns real results |
| 20 | Degradation, flags, observability (Section 28) | conformance cases 12a to 12f |
| 21 | Accessibility pass, reduced motion, performance pass | Sections 31, 19 and the checklist in Section 36 |

Dependencies worth stating, because they are the ones that get violated:

- Stages 8 to 11 are strictly ordered. Nothing in Section 23 can be tested
  before the cascade in Section 22 is correct, and a team that builds faceting
  first will tune it against a ranking that is about to change.
- Stage 13 depends on stage 9 having produced real `_rankingInfo` rather than a
  reconstruction, per Section 22.13.
- Stage 18 depends on nothing after stage 10 and can be pulled forward if the
  demonstration needs it, at the cost of tuning fusion against an engine whose
  facet behaviour is not settled.
- Stage 19 is the first point at which the marketing site and the service are
  the same product. Everything before it is two builds.

You get something worth looking at after stage 4, something that behaves like
the reference site after stage 7, and something that is the product after
stage 13.

> **In plain language.** What gets built first, and what you can look at after
> each stage.
>
> | Stage | What is built | What you can check |
> |---|---|---|
> | 1 to 3 | The paint box, the furniture, the icons | One page showing every colour and size, and a keyboard walk of the site |
> | 4 to 5 | Every page, laid out, motionless | Screenshots that match the reference at three widths |
> | 6 to 7 | The movement, and the search box behaving correctly | Scroll the site; drive the search box with the keyboard alone |
> | 8 to 11 | The engine itself: storing, ordering, filtering, permissions | The exam in the conformance section, section by section |
> | 12 to 13 | The control room, and the practice search inside it | Load a catalogue and ask why a product ranks where it does |
> | 14 to 17 | Standing instructions, the personal touch, the reporting | Drag a product to the top and watch it stay there |
> | 18 | Meaning-based search and written answers | Ask a question in a sentence |
> | 19 to 21 | The site and the engine joined up, then polish | Search on the home page returns real results |
>
> The order is not arbitrary. The ordering rules have to be right before the
> filters are built on top of them, or the filters get tuned against behaviour
> that is about to change, and the tuning has to be thrown away.
>
> Two dates are worth putting in a calendar. After stage 4 there is something to
> look at. After stage 13 there is something to sell.

---
## 33. Zero-asset substitution guide

Nothing in this build is a binary. This section accounts for every asset class
the reference used and gives a procedural recipe for each.

### 33.1 The reference asset manifest

What the reference loaded, by class, so that a reviewer can check that nothing
was quietly dropped rather than replaced. This is the only place in this
document where an asset name appears, and the brand-derived parts of those names
are tokenised per Section 0.3, because a filename carries a brand exactly as a
heading does.

<!-- lint:allow P4,P6 -->

| Class | Count and names as captured, tokenised | Replaced in |
|---|---|---|
| Carousel foregrounds | 5, of the form `cropped-foreground-<ANALYST>-<REPORT>.png` | Section 33.4 |
| Carousel overlays | 5, of the form `overlay-<ANALYST>-<REPORT>.png` | Section 33.4 |
| Carousel background video | 1, `ai-retrieval-carousel-bg-720.mp4`, 1,627,213 bytes | Section 33.3 |
| Partner and integration marks | 4, of the form `<PARTNER>-logo.png` and `<PARTNER>-logo-icon.png` | Section 33.7 |
| Promotion banners | 3, of the form `<AGENT_PRODUCT>-banner-ad.png`, `<CUSTOMER>-website-nav-banner (1).webp`, `<EVENT_NAME>-events-1024x768.webp` | Section 33.4 |
| Fallback advertisement | 1, of the form `<BRAND>_route-2_300x250_fallback (2).jpg` | not replaced; removed, see Section 33.9 |
| Chat artwork | 1, `bot-3-long-828x336-lossless.webp` | not replaced; removed with the embed |
| Consent surface artwork | 2, a close glyph and a company logo, both from the consent vendor | not replaced; removed with the embed |
| Third-party logo images | 4, served from an offsite promotion host at `?width=146` | Section 33.7 |
| Screenshot thumbnails | 1 per search result, served from an object store | Section 33.4 |
| Web fonts | 8, `Sora-Light.woff2`, `Sora-Regular.woff2`, `Sora-SemiBold.woff2`, `Sora-Bold.woff2`, `Inter-Regular.woff2`, `Inter-Medium.woff2`, `Inter-SemiBold.woff2`, `Inter-Bold.woff2`, plus four legacy-format fallbacks | Section 33.2 |
| One further font face | 1, a Montserrat subset with a hashed name, loaded by an embed | not replaced; removed with the embed |
| Tracking pixels | 604 files of an animated image format, 2,400,928 bytes | Section 33.9 |

<!-- lint:end -->

### 33.2 Fonts

Both families are open-licensed and are named, not shipped.

| Family | Licence | Weights this build loads | Fallback stack |
|---|---|---|---|
| Sora | SIL Open Font License 1.1 | 700 preloaded, 300, 400, 500, 600, 900 lazily | `"Sora", "Trebuchet MS", "Segoe UI", system-ui, sans-serif` |
| Inter | SIL Open Font License 1.1 | 400 preloaded, 500, 600, 700, 800, 900 lazily | `"Inter", "Helvetica Neue", Arial, system-ui, sans-serif` |

Naming a font family is not an asset dependency. Both are subset to the Latin
range plus the punctuation in the copy deck of Section 34, and the fallback
stacks are chosen for metric proximity so the swap does not shift layout.

If neither family is available, the fallbacks carry the design. The display
heading loses its geometric character and nothing else breaks, because the
layout is driven by the sizes in Section 3.3 rather than by the glyph shapes.

### 33.3 The particle field and the gradient grounds

Two dark bands, Sections 9.5 and 9.8, carry a field of small blurred light
points. The reference serves a video for one of them, at 1.6 megabytes.

**Substitute, normative.** A single canvas layer, generated once at
`1440 x 900` and scaled:

<!-- lint:allow P6 -->

| Parameter | Value |
|---|---|
| Ground | `#000033` |
| Point count | 220 at desktop, 90 at mobile |
| Point radius | 1 to 4 pixels, distributed toward the small end |
| Point colour | `#457aff` at alpha 0.15 to 0.6, and `#ffffff` at alpha 0.05 to 0.2 for one point in eight |
| Blur | a radial gradient per point, opaque at the centre, transparent at the rim |
| Distribution | random, with a density gradient rising toward the upper right |
| Motion | none by default; an optional drift of 2 pixels per second under a flag, disabled under reduced motion |
| Seed | fixed, so the field is identical across builds and screenshots diff cleanly |

<!-- lint:end -->

The seed is the part that matters for review. A random field regenerated per
load makes every visual comparison against this specification unusable.

The hero and demo request gradients are declared values from Section 3.9 and
need no substitution. The wide violet-to-teal sweep on the pricing hero and the
violet-to-blue sweep on the demo request route are two-stop linear gradients
over `#000033` and are specified there.

### 33.4 Photography and the composed interface panels

The reference's product panels, Sections 9.2 and 11.3, are a photograph of a
person with interface elements composed over it. The interface elements are the
argument; the photograph is the setting.

**Substitute, normative, in two parts.**

**The interface elements are built, not drawn.** The query bubble, the answer
bubble, the product cards, the price and swatch rows, the microphone glyph and
the search field in those panels are real elements using the primitives of
Section 17.2 and the tokens of Section 3.2. They must be, because they are the
product being demonstrated and a picture of a product demonstration is the exact
thing this document exists to avoid.

**The photograph is replaced by a generated ground.** A canvas layer, seeded:

<!-- lint:allow P6 -->

| Parameter | Value |
|---|---|
| Base | a three-stop linear gradient at 138 degrees drawn from the panel's own accent, defaulting to `#457aff` to `#003dff` to `#1a1a2e` |
| Silhouette | an abstract rounded form occupying the right third, filled with the same gradient rotated 90 degrees and lightened by 8 percent |
| Grain | a fine noise layer at alpha 0.04, generated by a turbulence filter with a base frequency near 0.9 and four octaves, desaturated to zero |
| Vignette | a radial darkening to 20 percent at the corners |
| Seed | fixed per panel, so the three hero panels are visibly distinct and individually stable |

<!-- lint:end -->

The result is not a photograph and must not pretend to be one. It is a ground
that lets the composed interface read, which is what the photograph was doing.

The customer story cards in Sections 9.7 and 12.4 use the same generator with a
different seed per card and the customer wordmark of Section 33.7 knocked out
over it.

### 33.5 Video and its poster

One video is specified, on the products route, Section 11.4.

| Element | Substitute |
|---|---|
| The video file | out of scope for this build; the element is present, sourced from `<ASSET_HOST>`, and the build ships with it absent |
| The poster | generated by the Section 33.4 recipe with the play glyph composed over it |
| Captions | a text track, authored, shipped as text |

A build with no video file must render the poster, the play affordance and the
caption track without error, and must not show a broken media element. This is
the one place where the zero-asset rule leaves a hole, and it is stated rather
than papered over.

### 33.6 The seeded fixture corpus

Required by the conformance suite in Section 30 and by the console's
demonstration mode.

A generator, deterministic for a given seed, producing 2,000 records:

| Attribute | Generation |
|---|---|
| `objectID` | `p_` and a zero-padded index |
| `title` | two to five words from a fixed vocabulary of 400 nouns and adjectives |
| `brand` | one of 12, distributed by a fixed power law so facet counts are uneven |
| `categories` | one to three from a fixed tree of 30 |
| `colour` | one of 8 |
| `price` | log-normal between 4 and 990, rounded to two decimals |
| `rating` | 1.0 to 5.0 in tenths, with a deliberate cluster at 4.7 so Section 22.9's bucketing is exercised |
| `popularity` | integer 0 to 100 |
| `shirtId` | present on 1,200 records in groups of 4, for Section 30.5 |
| `_geoloc` | present on 200 records, clustered so Section 30.3's case 3g is reproducible |
| `description` | 40 to 200 words, drawn from the same vocabulary |

Seven records are fixed rather than generated, because named cases in Section 30
refer to them: `t1` to `t7` in Section 30.2 and `r1` to `r4` in Section 30.3.
The generator writes them verbatim before generating the rest.

The corpus must include, by construction: at least one pair differing only by a
transposition, at least one accented title, at least one title in a script
without spaces, at least one pair of adjacent years, and at least one title
containing an eszett. Those five exist to make Section 30.2 runnable and are the
reason the corpus is generated rather than sampled.

### 33.7 Wordmarks, partner marks and badges

Three classes of small brand artwork, all replaced by text.

| Class | Substitute |
|---|---|
| Customer wordmarks, Sections 9.7 and 12.4 | the placeholder name from Section 0.3, set in Inter 800, letter spacing `0.02em`, in `#ffffff`, knocked out over the generated card ground, scaled to 60 percent of the card width |
| Partner and integration marks | the placeholder name in Inter 600 in `#23263b`, inside a `1px` `#e5e5e5` bordered box with an `8px` radius |
| Compliance badges, Section 13.4 | already text in the reference: `10px` weight 700 inside a `1px` bordered pill with a `4px` radius |

The third row is the useful precedent. The reference already sets its
compliance badges as text in pills rather than as images, which is why that part
of the demo request route needed no substitution at all. The same treatment
extends to the other two classes without inventing anything.

### 33.8 Icons

Already solved. Section 4 transcribes every icon as geometry. No icon in this
build is a file, including the mark, whose procedural placeholder is in
Section 4.1.

### 33.9 What is removed rather than replaced

Four classes are not substituted because they should not exist in the build:

| Class | Why |
|---|---|
| 604 tracking pixels | one image per analytics event; the build sends events to its own collector per Section 27.1 |
| The consent surface embed and its artwork | consent is first-party, per Section 19.4 step 5 |
| The support chat embed and its artwork | out of scope; the build ships without it |
| The promotion embed and its four offsite logo images | out of scope; it is the surface that claims the top of the stacking order in Section 3.8 |

Removing these is not a simplification of the reference. It is the difference
between the 120 kilobyte budget in Section 19.1 and the reference's actual
weight.

> **In plain language.** This document ships without a single picture, video, or
> font file, and this section explains how each of those was replaced.
>
> The fonts are two free ones, named rather than attached, with a fallback list so
> the layout holds even if neither arrives.
>
> The drifting field of small blue lights on the dark bands is drawn rather than
> filmed. The original serves a video weighing more than a megabyte and a half for
> that effect. The replacement is a few hundred soft dots drawn once, from a fixed
> starting number so that it comes out identical every time, which matters because
> otherwise no two screenshots of the site could ever be compared.
>
> The product panels get an interesting treatment, and it is the most important
> line in this section. Those panels are a photograph of a person with pieces of
> the product laid over the top. The pieces of the product are rebuilt as real,
> working interface, because a picture of a search box is precisely the thing this
> whole document exists to prevent. Only the photograph behind them is replaced,
> by a generated coloured ground with a soft abstract shape and a little grain.
> It does not pretend to be a photograph.
>
> Customer logos become the customer's name, set large and bold and knocked out of
> the card. The security badges needed no work at all: the original already sets
> them as text in little outlined pills.
>
> And four things are removed rather than replaced: six hundred tracking pixels,
> the cookie banner's own artwork, the chat widget, and an advertising panel.
> Those are not part of the site. They are the reason it is slow.

---

## 34. Copy deck

Every string, by surface. Angle-bracket tokens are per Section 0.3.

**One global substitution.** The reference's copy uses typographic dashes in
several places. This document is grepped, diffed and pasted as plain text, so
every one is written here as a hyphen. Where a line reads `- fast` or
`- VIRTUAL`, the reference had a longer dash.

### 34.1 Global chrome

| Surface | String |
|---|---|
| Promotion, slide 1 label | `Join us:` |
| Promotion, slide 1 message | `<BRAND> <EVENT_NAME> 2026: Oct 1, 2026 - VIRTUAL` |
| Promotion, slide 1 action | `Register Now` |
| Promotion, slide 2 label | `UPDATE:` |
| Promotion, slide 2 message | `Unlock the power of agentic AI with <AGENT_PRODUCT>` |
| Promotion, slide 2 action | `See what's new` |
| Utility | `Company`, `Partners`, `Support`, `Login`, `Logout` |
| Language, active | `Eng` |
| Language, list | `English`, `German`, `French`, `Brazilian Portuguese`, `Spanish`, `Italian` |
| Navigation | `Products`, `Solutions`, `Pricing`, `Developers`, `Resources` |
| Header button, secondary | `Fix your search` |
| Header button, primary | `Get started` |
| Search placeholder | `Search or Ask AI` |
| Search placeholder, customers route | `Search <BRAND>` |
| Search rotating prompt | `How can I help you?` |
| Drawer group heading | `Quick Access` |
| Drawer close | `Close` |
| Mark title, accessible | `<BRAND> mark white` |
| Wordmark title, accessible | `<BRAND> logo white` |

### 34.2 The search overlay

| Surface | String |
|---|---|
| Mode toggle | `AI mode` |
| Facet heading | `Filter by source` |
| Facet values | `Documentation`, `Support`, `Blog`, `Website`, `Developers`, `Resources`, `Academy`, `Customer Stories` |
| Suggested question 1 | `How will <BRAND> improve our search experience and conversions?` |
| Suggested question 2 | `How do I integrate <BRAND> search into my app?` |
| Suggested question 3 | `Can <BRAND> help shoppers find products faster and increase sales?` |
| Suggested question 4 | `Will <BRAND> scale with our traffic and data size?` |
| Suggestions heading | `Suggestions` |
| Suggestion buttons | `<BRAND> API integration`, `<BRAND> search benefits`, `<BRAND> scalability`, `AI search for ecommerce` |
| Results heading | `Products & Resources` |
| Hit meta format | `Website • products` |
| Hit action | `Learn more →` |
| Load more | `Show more results` |
| Assistant title | `<ASSIST_PRODUCT>` |
| Assistant actions | `New chat`, `Back to results` |
| Attribution | `AI powered by <BRAND>` |
| Filter controls | `Show All`, `Clear All Filters` |

The overlay also carries a second facet group set, observed on the resource
index it shares its configuration with: `Learn` with values `Engineering`,
`Product`, `Ecommerce`, `AI`, `UX`, `Ebooks`, `Webinars`, `Infographics`,
`Videos`; `Use Case` with `Ecommerce`, `Dev Tools`, `Technology`, `Media`,
`Merchandising`, `B2B`, `SaaS`, `Marketing Automation`, `B2C Ecommerce`, `Geo`;
`Framework` with `React`, `Flutter`, `Next.js`, `Typescript`, `Django`,
`Ruby on Rails`, `Vanilla Javascript`, `Angular`, `Hugo`, `Jekyll`; and
`Programming Language`, beginning `JavaScript`.

### 34.3 Home

| Surface | String |
|---|---|
| Hero heading | `Agentic.` / `Generative.` / `Search` |
| Hero lead | `One AI retrieval platform to power them all` |
| Hero button | `Explore the platform` |
| Panel eyebrows | `Generative` over `EXPERIENCES`, `Search` over `EXPERIENCES`, `Agentic` over `EXPERIENCES` |
| Section heading | `Powering AI retrieval across use cases` |
| Section lead | `More than 18,000 customers across 150+ countries use <BRAND> to power agentic, generative, and search experiences across these use cases and more.` |
| Accordion items | `AI mode search bar`, `Generative AI`, `Agentic commerce`, `Merchandising` |
| Accordion body 1 | `Customers can use natural language in the search bar and AI recognizes intent to guide their discovery.` with `Learn more` |
| Section button | `See more capabilities` |
| Analyst eyebrow | `NORTHGATE RESEARCH 2026 QUADRANT FOR SEARCH AND PRODUCT DISCOVERY` |
| Analyst heading | `A leader for the third consecutive year` |
| Analyst body | `<BRAND> is recognized as a Leader in the 2026 Northgate Research Quadrant for Search and Product Discovery as the market shifts toward AI-powered, agentic discovery.` |
| Analyst buttons | `Read the announcement`, `See <BRAND> in action` |
| Solutions heading | `Solutions that fulfill your business goals` |
| Solutions lead | `Here are just some of the ways <BRAND> technology provides value from day 1.` |
| Solutions card 1 | `Quickly surface the right content` / `Your customers get relevant results to find precisely what they're looking for - in milliseconds.` |
| Solutions card 2 | `Understand user intent` / `AI algorithms are used to predict and show results from the most likely category of content in your index.` |
| Solutions card 3 | `Confidently launch agentic experiences` / `Deliver secure, production-ready agentic capabilities to your shoppers with brand and pricing certainty.` |
| Solutions card 4 | `Personalize for more engagement` / `Build unique visitor journeys that lead your customers to convert over and over again.` |
| Solutions card 5 | `Create buying urgency` / `<BRAND> AI is always learning what drives conversion and reranks content to push better outcomes.` |
| Customers heading | `See customer success in action` |
| Customers lead | `Discover how your peers have been succeeding with <BRAND>` |
| Customers button | `View all customer stories` |
| Closing heading | `Harness the power of goal driven AI search with <BRAND>` |
| Closing buttons | `Get Started`, `Get a demo` |

### 34.4 Pricing

| Surface | String |
|---|---|
| Heading | `Scalable pricing for smarter search` |
| Lead | `Powering the world's best AI experiences - start for free, grow seamlessly and upgrade anytime` |
| Chooser | `Help me choose a plan` |
| Chooser caption | `Answer 3 quick questions to see which plan fits best.` |
| Group headings | `Annual plan`, `Pay as you go` |
| Plans | `Elevate`, `Grow Plus`, `Grow`, `Free` |
| Badge | `NEW` |
| Plan subtitles | `Enterprise-scale AI Search`, `Keyword search with AI`, `Keyword search`, `Search and recommendations` |
| Plan actions | `Start for free`, `Build for free`, `Request pricing`, `Get started` |
| Grow metering | `10K search requests /month included then $0.50 per additional 1K search requests` |
| Grow records | `100K records included then $0.40` |
| Free body | `Get started building experiences ever with some of our features.` |
| Free note | `No credit card required.` |
| Jump link | `See full features grid` |
| Grid heading | `Detailed feature comparison` |
| Grid categories | `Search`, `Analytics`, `UI Components`, `Integrations & Data`, `Crawler`, `Infrastructure & Plan Limits`, `Support & Success` |
| Grid rows, measured | `Rules`, `Visual Editor`, `Manual Synonyms`, `Virtual Replicas (Relevant Sort)`, `AI Synonyms`, `Query Categorization` |
| Grid values, measured | `10 per index`, `10,000 per index` |
| Questions heading | `Pricing FAQs` |
| Question 1 | `What is a search request?` |

### 34.5 Products

| Surface | String |
|---|---|
| Eyebrow | `AI PRODUCT OVERVIEW` |
| Heading | `AI search and retrieval` / `that shows users what they need` |
| Lead | `Enhance your users' journey with solutions powered by retrieval for searching, browsing, personalization, and recommendations.` |
| Buttons | `Get a demo`, `Start building for free` |
| Section heading | `Make every interaction smarter with AI retrieval` |
| Block 1 heading | `Search experiences` |
| Block 1 body | `Build powerful search experiences for your app or site with AI that understands, ranks, and adapts in real time. Retrieval ensures results remain contextual and aligned with your business, whether the query is simple, ambiguous, or conversational.` |
| Block 1 feature 1 | `Hybrid Search`: `Semantic vector search meets keyword precision for fast, intuitive results that match user intent.` |
| Block 1 feature 2 | `AI Ranking`: `Machine learning that optimizes relevance while preserving human control.` |
| Block 1 feature 3 | `Query Categorization`: `Turn unstructured queries into structured data for smarter merchandising and analytics.` |
| Block 1 feature 4 | `Advanced Personalization`: `Reflect each user's behavior, preferences, and context, out of the box.` |
| Block 1 button | `Learn more about AI Search` |
| Video block body | `See how intelligent search understands intent, connects the right data sources, and guides users through personalized, contextual journeys - from product discovery to recommendations, availability, and action.` |
| Video block question | `Ready to build the next generation of search?` |
| Video block button | `Book a live demo with our product experts` |
| Tools heading | `Tools for business users` |
| Feature link | `Learn more` |

### 34.6 Customers

| Surface | String |
|---|---|
| Search placeholder | `Search for a customer story` |
| Facets | `Features`, `Use Case`, `Industry`, `Region`, `Integration` |
| Card category, measured | `Ecommerce` |
| Card titles, with names substituted per Section 0.3 | `Northmoor Group leverages <BRAND> to boost search performance and ...`, `Keeping it fast and cool. Culture Yard speeds up Search ...`, `Halcyon Sport achieves +150% sales contribution from search` |
| Load more | `Show more results` |
| Clear | `Clear All Filters` |

### 34.7 Demo request

| Surface | String |
|---|---|
| Heading | `Fix your search experience` |
| Lead | `Struggling with relevance, slow results, or limited control? We'll show you how to improve search performance and conversions - fast.` |
| Labels | `First Name`, `Last Name`, `Business Email`, `Phone`, `Company`, `Country` |
| Select placeholder | `Select...` |
| Submit | `Get In Touch` |
| Statistic 1 | `18,000+` / `global brands served` |
| Statistic 2 | `9.3 Billion` / `Single-day searches` |
| Trust row 1 | `Trusted by 18,000+ businesses` |
| Trust row 2 | `Enterprise-grade security & data privacy` |
| Badges | `CCPA`, `BSI C5`, `SOC 2 Type II`, `ISO 27001`, `GDPR` |

### 34.8 Not found

| Surface | String |
|---|---|
| Numeral | `404` |
| Heading | `Page not found` |
| Search | `Search <BRAND>` |
| Links | `API Status`, `Home page`, `Support` |

### 34.9 Footer

| Surface | String |
|---|---|
| Links | `Careers`, `Contact Us`, `About <BRAND>`, `Anti-Modern Slavery Statement` |
| Social heading | `Social networks` |
| Newsletter | `Get the latest in AI search - straight to your inbox.` |
| Legal | `Cookie settings`, `Trust Center`, `Privacy Policy`, `Terms of service` |

> **In plain language.** Every word on the site, gathered in one place, so it can
> be read, checked, translated or replaced without opening the build.
>
> Two things about it are worth knowing.
>
> First, wherever the original used a real name, a stand-in of about the same
> length is used here: the company, its conference, its products, its customers
> and the research firms that rated it. Those are all blanks to fill in.
>
> Second, the original writing uses a long dash in a few places. This document is
> read and searched as plain text and pasted into build tools, and that particular
> character causes trouble when it travels, so every one has been written as an
> ordinary hyphen. If the finished site should have the long dash back, it goes
> back in at the last step, in the copy, and nowhere else.

---

## 35. Evidence gaps and substitutions

The honest boundary of this document.

### 35.1 Route inventory

Six routes were captured and are specified. The reference site is larger.

Route discovery on this site is unreliable in a specific and worth-recording
way: the tool that finds routes crawls links and then mines route-shaped strings
out of the site's own bundles, and ranks what it finds by path length. This
site's bundles contain several hundred short path-shaped literals, so the ranked
list is dominated by fragments such as single letters and status codes, and the
real routes never reach the cap. Routes were therefore captured individually by
name.

Consequences a reader should know:

- The four navigation panels in Section 5.4 are specified as containers with no
  link inventory, because their contents were not resolved.
- A German rendering of the home route was reached during capture at a locale
  path. It confirms the localisation system in Section 2.2 is real, and it was
  excluded from the ledger so that German copy would not enter the copy deck.
- Two further routes, a developer landing page and a resource index, were
  captured after the section numbering in this document was frozen, and are
  deliberately not specified. Their evidence exists; adding them would have
  renumbered every cross-reference in the document, which is the single most
  common way this kind of specification breaks.

### 35.2 Third-party surfaces, excluded on purpose

The reference embeds roughly thirty third-party surfaces. Four of them are large
enough to have polluted the measurements, and each is excluded with its reason:

| Surface | What it contributed | Why excluded |
|---|---|---|
| Support chat | a full palette including `#0176d3`, `#1b96ff`, `#014486`, `#032d60`, `#06a59a`, `#107cad`, `#3ba755`, `#ea001e`, `#ff538a`, `#ff5d2d`, and the two maximum stacking values in Section 3.8 | it is another company's design system, not this one |
| Consent surface | two hard-coded mid-grey icon fills, radii of `2px`, `3px` and `2.5px`, and eleven print-media rules | replaced by a first-party surface, Section 19.4 |
| Promotion embed | the `om-position-floating-top` root class observed on the products route, and four offsite logo images | out of scope |
| Marketing form platform | the form field styling in Section 15.1 and the submit button in Section 5.6 | the styling is measured and kept; the platform is not |

The fourth row is the subtle one. The demo request form's distinctive submit
button, with its two percent scale and four-stop gradient hover, belongs to a
marketing platform's stylesheet rather than to the site's own design system. It
is kept because it is what the page looks like, and it is recorded here because
a designer extending this system should know it is a graft.

### 35.3 Inferred rather than measured

| Item | Section | What was inferred |
|---|---|---|
| Marquee row duration | 7.4 | speed derived from card width and the statistics column's pixel speed |
| Marquee direction and offset | 7.4 | read from screenshots, not from computed styles |
| Comparison grid at `390px` | 18.3 | not resolvable from the capture; the single-plan treatment is specified rather than observed |
| Facet controls at `390px` | 18.2 | as above |
| Navigation panel contents | 5.4 | not resolved |
| The third icon in `Tools for business users` | 11.5 | not resolved |
| Hero panel 3 contents | 9.2 | the agentic panel was not captured in a resolved state |
| Reduced-motion behaviour | 6.8 | seventeen blocks exist; their contents were not resolved, so the behaviour is specified |
| Header height | 5.3 | read from the screenshots at `1440px`, not from a computed style |
| Two contrast substitutions | 3.4 | `#9698c3` and `#c9c9c9` carry text somewhere on the reference; this build forbids it |

### 35.4 Specified extensions

Everything in this list is authored, not measured. It is as binding as the rest
of the document and it is evidence of nothing.

| Section | What is specified |
|---|---|
| 16 | the entire application console |
| 20 | the service topology, the stored objects, the error contract, idempotency, limits |
| 21 | ingestion, the text pipeline, index structures, partial updates, atomic reindex, tasks |
| 22 | the query engine, typo tolerance, the ranking cascade, highlighting, pagination |
| 23 | the filter grammar, facet counting, deduplication, the read path order |
| 24 | synonyms, rules, personalization, tests, precedence |
| 25 | vectors, approximate nearest neighbour, fusion, the answer pipeline, streaming |
| 26 | tenancy, key kinds, secured key derivation, quotas, rate limiting |
| 27 | events, attribution, deduplication, rollups, metric definitions |
| 28 | replication, read-your-writes, replicas, client behaviour, degradation |
| 29 | the failure catalogue |
| 30 | the conformance suite |

The reference site's own backend, as far as the capture could see it, is
Section 20.3: a content source, two form targets and a hosted search. The other
eleven sections are the product it sells, written as a build.

Two things follow, and both should be said plainly to whoever is paying:

1. The second half of this document is roughly the same size as the first half
   and is at least five times the work.
2. It is not optional in the sense of being decoration. Sections 1.1, 8 and 12.3
   all state that the site demonstrates the product on itself, and every one of
   those demonstrations is a live query against the service specified here.

### 35.5 Feature grid to specification mapping

The pricing comparison grid, Section 10.4, names features. A grid that names
features the build does not have is the easiest inconsistency in this document
to ship. The measured rows map as follows:

| Grid row | Specified in | Note |
|---|---|---|
| `Rules` | 24.2 | the limits `10 per index` and `10,000 per index` are plan values, not engine limits |
| `Visual Editor` | 16.6 | the merchandising screen |
| `Manual Synonyms` | 24.1 | all five synonym types |
| `Virtual Replicas (Relevant Sort)` | 28.3 | the cheap alternate sort order |
| `AI Synonyms` | not specified | **gap**: the reference sells automatically generated synonyms; this document specifies only manual ones |
| `Query Categorization` | not specified | **gap**: named on the products route as a headline capability and not specified anywhere in Sections 20 to 30 |

The two gaps are real and are recorded rather than quietly dropped. Both are
machine-learning features over the analytics of Section 27, both are plausible
extensions of it, and neither is specified here. A build that ships the pricing
grid with those two rows ticked has made a claim this document does not support.

### 35.6 Classification

The task order that accompanies this document declares:

| Level | Value | Why |
|---|---|---|
| `category` | `solo_founder` | the product is sold by public signup, with a free plan and a self-serve upgrade path, which is that category's definition |
| `domain` | `saas-productivity` | the nearest legal member; the vertical is developer infrastructure, which the enum does not carry |
| `pattern` | `catalog-browse` | the shape the graded workflow exercises: a filterable listing with facets, sort and detail, which is what Sections 8, 12 and 23 are |
| `archetype` | `search-platform-showcase` | lowercase kebab, three tokens, registered |

Two substitutions are recorded:

- **Domain.** The captured site's own vocabulary is "AI search and retrieval
  platform". The closed enum has no developer-infrastructure member, and
  `saas-productivity`, defined as small business tools sold by public signup, is
  the nearest legal fit. The mismatch is that this product is sold to
  enterprises as well; the free plan and the public signup are what settle it.
- **Pattern.** The site as captured is a marketing site, which would make
  `content-publishing` the honest shape of the six routes alone. It was not
  chosen. The graded workflow that matters here is the faceted, multi-select,
  count-bearing search on the customers route and in the header overlay, and
  that is `catalog-browse`. A reviewer who expected `content-publishing` should
  read Section 12.3.

### 35.7 Gate deviations

Two regions of this document use the narrow linting escape, and both are
declared here so a reviewer can find them:

| Region | Gates suppressed | Why |
|---|---|---|
| Section 33.1, the reference asset manifest | asset dependency, ledger fidelity | it names the binaries this build replaces; naming them is the point |
| Sections 33.3 and 33.4, the generator parameters | ledger fidelity | the alpha values and percentages there are proposed, not measured |

No gate is disabled document-wide.

> **In plain language.** What we could not measure, what we left out on purpose,
> and what we made up.
>
> Six pages were measured. The site is bigger than six pages. The reason is worth
> knowing: the tool that finds pages automatically was defeated by this particular
> site, which mentions hundreds of short, path-shaped fragments inside its own
> code, so the automatic list came back full of nonsense. The six were captured by
> name instead. The drop-down panels in the main menu were never resolved, so this
> document describes the panel and not the links inside it.
>
> About thirty other companies' software is embedded in the original page: a chat
> widget, a cookie banner, a marketing form, an advertising panel. Their colours
> and their styling got mixed into the measurements, and they have been separated
> out and listed. One of them is a graft worth knowing about: that nice submit
> button on the demonstration form belongs to a marketing platform, not to this
> design system.
>
> Ten things could not be measured and were worked out from screenshots or simply
> decided. They are listed. Expect them to need adjustment.
>
> The largest piece of honesty is this. Everything from the twentieth section
> onward, plus the control room, was written rather than measured. It is the
> product the site is selling, specified as a real build. It is roughly the same
> length as the half that was measured and it is several times the work, and
> anybody paying for this should know that before they start rather than in month
> three.
>
> Finally, two features named on the original's own pricing table are not
> specified anywhere in this document, and rather than quietly tick them we have
> written down that they are missing.

---
## 36. Acceptance checklist

A build is accepted when every line here is true. The list is deliberately
checkable by someone who did not write the build, and the service half of it is
mostly "the suite in Section 30 passes", because that is what the suite is for.

### 36.1 The site

- [ ] Every route in Section 2.1 renders at 1440, 990 and 390 pixels wide with no
      horizontal scrollbar on the page body.
- [ ] The token sheet renders every colour, type step, spacing step and radius
      from Section 3, and each matches its recorded value.
- [ ] Every icon in Section 4 is inline geometry. No icon is an image file.
- [ ] The header behaves as specified in Section 5.1 at all three widths,
      including the sticky transition and the mobile panel.
- [ ] Reveals track their trigger as specified in Section 7, and nothing pops
      into place on a slow connection.
- [ ] The hero rotation in Section 9.2 advances, pauses on hover, pauses on
      focus, and stops entirely under the reduced-motion setting.
- [ ] The comparison grid in Section 10.4 keeps its header row visible while its
      body scrolls, at all three widths.
- [ ] The demo request form in Section 13 submits, shows all three states, and
      is completable with the keyboard alone.
- [ ] The not-found route in Section 14 renders for any unmatched path and
      carries the search box.
- [ ] No binary asset ships. Section 33 accounts for every one the reference
      used.

### 36.2 The service, by suite

- [ ] Section 30.2 passes: text pipeline and typo tolerance, 11 cases.
- [ ] Section 30.3 passes: the ranking cascade, 7 cases, including 3a and 3g.
- [ ] Section 30.4 passes: filters and facet counting, 8 cases.
- [ ] Section 30.5 passes: deduplication, pagination and stability, 6 cases.
- [ ] Section 30.6 passes: highlighting, 6 cases.
- [ ] Section 30.7 passes: keys, restrictions and limits, 9 cases.
- [ ] Section 30.8 passes: writes, tasks and idempotency, 10 cases.
- [ ] Section 30.9 passes: rules, synonyms and tests, 11 cases.
- [ ] Section 30.10 passes: hybrid retrieval and answers, 9 cases.
- [ ] Section 30.11 passes: analytics, 9 cases.
- [ ] Section 30.12 passes: degradation and honesty, 6 cases.

### 36.3 The five that are checked by hand

The suite cannot check these, and they are the ones most likely to be wrong.

- [ ] **No score in the ranking path.** A reviewer greps the ranking code for a
      floating point score field and finds none. Section 29.3.1.
- [ ] **A second evaluation for disjunctive facets.** A reviewer finds the code
      that prunes the filter tree per facet, and it is not the conjunctive pass
      with a flag. Section 29.3.2.
- [ ] **Key restrictions combine with AND.** A reviewer reads the line that
      merges the key's filters with the request's, and it is a conjunction.
      Section 29.3.3.
- [ ] **Rollups recompute.** A reviewer confirms the aggregate tables are
      rebuilt from raw events for the affected window, not incremented in place.
      Section 27.3.
- [ ] **Flags are computed, not constant.** A reviewer finds at least one code
      path that sets `exhaustiveNbHits`, `exhaustiveFacetsCount`,
      `exhaustiveTypo` and `degraded` to false. Section 29.4.

### 36.4 Performance

- [ ] The budgets in Section 19.1 are met on the stated reference hardware.
- [ ] A search over the 2,000-record fixture corpus returns in under 20
      milliseconds at the median, measured at the service.
- [ ] A search over a one-million-record corpus returns in under 50
      milliseconds at the median, with `getRankingInfo` off.
- [ ] The console's record browser renders 200 rows without dropping frames
      while scrolling.
- [ ] Highlighting is applied to one page of hits, verified by the stage timings
      in Section 28.6 rather than by inspection.

### 36.5 Accessibility

- [ ] Every route passes the landmark, heading and label requirements in
      Section 31.1 and Section 31.7.
- [ ] The search box behaves exactly as the table in Section 31.2 specifies,
      driven from the keyboard with the screen reader running.
- [ ] The live region announces counts, not results, and no more than twice a
      second.
- [ ] Every measured colour pair in Section 3.4 meets its ratio, or is listed
      there as substituted.
- [ ] Reduced motion removes every transform-based reveal and stops every
      auto-advance.

### 36.6 Honesty

- [ ] Every placeholder token in Section 0.3 has been replaced, and none of the
      angle-bracket names survives in the shipped build.
- [ ] Every substitution in Section 33 is either replaced with a real asset or
      documented as shipped procedurally.
- [ ] Section 35 has been re-read against the finished build, and anything that
      turned out differently is corrected there rather than left as it was
      written.

> **In plain language.** This is the list you read down before you agree the work
> is finished, and it is written so that someone who did not build it can check
> every line.
>
> The first part is the site: every page at three screen sizes, the menus, the
> movement, the forms, and the promise that not one image, video or font file is
> needed to make it work.
>
> The second part is the exam from the conformance section. Ninety-two tests,
> grouped by what they are testing, all of which have to pass.
>
> The third part is five things a machine cannot check, so a person reads the code
> for them. They are the five places where the build can pass every test and still
> be wrong, and they take about an hour between them. Skipping this part is how a
> build ships with results that are ordered by a single popularity score and
> filter counts that only work when one box is ticked.
>
> Then speed, then the checks for people using a keyboard or a screen reader, and
> finally a short list about honesty: that every blank has been filled in, every
> stand-in replaced, and that the list of things we could not measure has been
> read again at the end and corrected where the build proved it wrong.
