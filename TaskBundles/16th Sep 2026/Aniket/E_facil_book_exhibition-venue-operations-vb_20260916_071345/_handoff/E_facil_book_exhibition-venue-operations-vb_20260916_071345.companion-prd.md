# <BRAND> - an exhibition venue operations platform, buildable product requirements

Two deliverables in one build, sharing one design system:

1. The public site, rebuilt to pixel and motion fidelity from a measured
   capture: a trilingual venue site with an events calendar, a visitor
   section, an organiser section carrying an interactive floor plan of the
   whole campus, an about section, news, contact and the legal set.
2. The operations platform behind it: the system that actually runs a
   40,000 square metre campus of six halls, an event hall and a modular
   meeting centre, from a sales enquiry through a held floor plan, an
   accredited build-up, a live event with badged entrances, and an invoice.

The public site is the shop window of a real building. Every capacity, area
and combination in it is a physical constraint, and the platform behind it
is graded on whether it can reason about the organisation that operates
them: overlapping spaces, several parties on one site at once, contractors
with different rights, and a safety regime that must hold on the worst day.

Every section is written twice: an exact specification, then a quoted block
opening with **In plain language** for a reader who does not build software.

## 0. How to use this document

Sections 2 to 13 specify the public site as measured. Sections 14 to 30
specify the platform; each carries a difficulty grade. Sections 31 to 36
cover the data contract, architecture and quality bars. Sections 37 to 41
carry the build order and difficulty map, the copy deck, the substitution
recipe for every binary asset, the honest list of what could not be
measured, and the acceptance checklist.

Angle-bracket names are blanks to fill with your own values; placeholders
of similar length are pre-chosen where they sit inside literal copy.

| Token | Meaning | Placeholder used in copy |
|---|---|---|
| `<BRAND>` | venue name | Meridian Xpo |
| `<CITY>` | the host city | Meridian |
| `<REGION>` | the surrounding region | the western province |
| `<GROUP>` | the parent group | Vantage Venues Group |
| `<ACQUIRER>` | the acquiring group in the news fixture | Fairwell Group |
| `<RESTAURANT>` | the in-house restaurant brand | The Glasshouse |
| `<BOULEVARD>` | the covered boulevard connecting the halls | The Promenade |
| `<CHARTER>` | the sustainability charter awarded ten years running | the regional sustainability charter |
| `<SITE_ORIGIN>` | public host | meridianxpo.com |
| `<APP_HOST>` | the signed-in operations host | ops.meridianxpo.com |

Difficulty grades, used per feature and mapped in Section 37:

| Grade | Meaning |
|---|---|
| medium | conventional build work; correctness is expected |
| hard | subtle correctness under overlapping resources, several actors or time; partial failure is likely without care |
| expert | fails quietly when built naively; graded on the edge cases |

There is no easy grade in this document by design.

> **In plain language.** One file describes both halves of a real venue:
> the website the public sees, measured to the pixel, and the system the
> staff run the building with, which is this document's own design. The
> hard half is hard for a specific reason: the halls can be combined and
> divided, several customers are on site at once with their own builders
> and caterers, and the safety rules have to hold when a hall is full of
> people. Software that reasons about a whole organisation is the exam
> here.

## 1. Product overview

The venue's own line: when ideas need space. Nearly 40,000 square metres
of halls and rooms, hired not as bare space but with a team that takes
care of catering, ticketing, parking, technical support and safety.

Capability requirements at the highest level, all normative:

- Must reproduce the public site per Sections 3 to 13 at the three
  captured widths, in three languages, with the interactive floor plan
  built from the real space model rather than a picture of it.
- Must model the campus as a graph of combinable spaces, where halls,
  the event hall, the meeting rooms, the covered boulevard and the
  passages between halls can be hired whole, combined or divided, and
  no two events may ever hold the same square metre at the same time
  (Section 15, expert).
- Must run the enquiry to contract path: an option held against dates
  and spaces with an expiry, competing options ranked, and a confirmed
  booking that consumes the option atomically (Section 16, expert).
- Must plan an event across its full life: build-up, run and tear-down
  windows that are part of the booking rather than an afterthought, on
  a campus timeline several events share (Section 17, expert).
- Must accredit the parties: organisers, exhibitors, contractors,
  caterers and staff, each with different rights on different days and
  in different spaces (Section 19, expert).
- Must control access: badges and entrance scanning that reflect
  accreditation, capacity and safety state in real time (Section 20,
  expert).
- Must hold the safety regime: occupancy limits per space and per
  combination, exit capacity, incident recording and an evacuation
  state that overrides everything else (Section 21, expert).
- Must order and cost the extras the venue sells: catering, technical
  services, furniture, parking allocations and stand services, each
  with lead times and cut-offs (Sections 22 and 23, hard).
- Must publish: the public calendar, each event's public page and the
  visitor information, in three languages, from the same records the
  operations team works in (Section 24, hard).

Observed implementation of the reference site, informational only: a
Drupal site with a bespoke theme, jQuery 4.0.0 and a focus-trap helper
(tier 1 licence banners), GSAP ScrollTrigger and a Swiper carousel
(tier 6 identifiers), a consent-management platform, a variable
sans-serif family and an icon font, and an inline vector floor plan. The
rebuild is stack-agnostic; the capability requirements bind.

> **In plain language.** The product is the software a large exhibition
> centre runs on. The public half is a handsome website with a calendar
> and a map of the halls. The working half books those halls, and that
> is harder than it sounds: two halls can be joined into one, a corridor
> can be hired as exhibition space or left as a walkway, and every
> booking needs days on either side to build and dismantle. On top of
> that sit the builders, caterers and exhibitors who all need different
> doors on different days, and a fire-safety limit that must never be
> exceeded.

## 2. Information architecture

### 2.1 Public routes, in three languages

Every route exists under three language prefixes, and the language
switcher preserves the current page rather than returning home.

| Path (English form) | Purpose |
|---|---|
| `/LANG` | home: hero, upcoming events, visit and organise invitations, hall summary, inspiration, newsletter, news |
| `/LANG/calendar` | the events calendar |
| `/LANG/visit` | visitor hub |
| `/LANG/visit/accessibility-parking` | how to reach the venue and park |
| `/LANG/visit/food-drinks` | eating and drinking on site |
| `/LANG/visit/what-to-do-city` | the surrounding city |
| `/LANG/visit/frequently-asked-questions` | visitor questions |
| `/LANG/organize` | organiser hub |
| `/LANG/organize/spaces` | the floor plan and every hall's specification |
| `/LANG/organize/meetings` | the modular meeting centre |
| `/LANG/organize/catering` | catering offer |
| `/LANG/organize/RESTAURANT-kitchen` | the in-house restaurant brand |
| `/LANG/organize/accessibility-region` | reaching the venue as an organiser |
| `/LANG/organize/unique-events` | case studies |
| `/LANG/organize/unique-events/CASE` | one case study per event |
| `/LANG/about` | about hub |
| `/LANG/about/who-are-we` | the team and the venue |
| `/LANG/about/history` | fifty years of the site |
| `/LANG/about/sustainability-safety` | the charter and the safety regime |
| `/LANG/about/media-kit-documents` | logos, plans and the safety manual |
| `/LANG/news` | news index |
| `/LANG/news/ARTICLE` | one article |
| `/LANG/news/newsletter` | newsletter subscription |
| `/LANG/contact` | contact and enquiry |
| `/LANG/general-conditions`, `/LANG/privacy-policy`, `/LANG/cookies` | legal set |
| `*` | not-found |

### 2.2 Platform surfaces

Behind sign-in at `<APP_HOST>`: the campus calendar, the enquiry and
option desk, the booking and contract file, the floor-plan planner, the
services and catering orders, accreditation and badges, entrance and
access control, the safety and occupancy board, the works and technical
schedule, invoicing, the public-content desk that publishes to the site,
and reporting.

> **In plain language.** The public site is about twenty-five pages, each
> in three languages: the calendar, everything a visitor needs, everything
> an organiser needs including a real map of the halls, the company pages,
> the news and the legal set. Behind the sign-in door is the working
> system: what is booked where and when, who may come in which door, what
> is being served, and whether the building is safe right now.
## 3. Design system

### 3.1 Ground, spacing and grid

Captured at 1440x900, 990x800 and 390x844. Spacing is fluid by design:
the measured rhythm tokens clamp between fixed bounds and scale with the
viewport, a tiny step from 3.125rem to 5.625rem, a small step from
3.75rem to 7.5rem, a default step from 5rem to 9.375rem, and a large step
from 7.5rem to 12.5rem, each interpolating on viewport width. Section
padding uses the same ladder, so vertical rhythm is one system rather
than a set of magic numbers.

The measured breakpoint ladder is normative and unusually tall: 30em,
46em, 61.25em, 71.875em (the dominant step, carrying six hundred rules),
90em, 100em and 120em, with a small number of pixel rules at 400px, 768px
and a 600px maximum. Motion is gated positively by a
no-preference query rather than negatively, and hover styling sits behind
a hover-capability query.

The z-index ladder is measured and must be closed: -1000 for ambient
backdrops, -1, 1, 2, 3, 9, 10 and 11 for content and raised chrome, 20
for sticky bars, and the overlay range for modals, the consent dialog and
the lightbox. The capture shows two escaped values in the very high
integer range, introduced by third-party widgets; the rebuild assigns
overlays a named token at the top of its own ladder and never competes
with an arbitrary large number, so a future widget cannot silently cover
the safety-critical surfaces of Section 21.

### 3.2 Colour

Measured root tokens, normative:

| Token | Value | Role |
|---|---|---|
| `--color-primary`, `--color-link` | `#d2251f` | the brand red: primary actions, links, accents |
| `--color-primary-dark` | `#500404` | the deep maroon that carries all body text |
| `--color-secondary`, `--color-link-hover` | `#ff604b` | the coral hover and secondary accent |
| `--color-secondary-dark` | `#e0372c` | pressed and deeper secondary |
| `--color-tertiary` | `#ff604b30` | the coral at 19 percent for washes and selection |
| `--color-background`, `--color-light` | `#ffffff` | page ground |
| `--color-light-hover` | `#e9e9e9` | hover fill on light surfaces |
| `--color-grey` | `#929292` | secondary text |
| `--color-grey-70` | `#b3b3b3` | tertiary text |
| `--color-grey-light` | `#d3d3d3` | hairlines and dividers |
| `--color-error` | `#a94442` | validation errors, over a `#fff4f4` wash |

Two support washes are measured and carry meaning in the calendar and
notices: a warm sand at `#f4daa6` and a soft coral at `#f9c9bf`. The
most-used computed ink is a near-black at `rgb(20, 20, 20)` for headings
over the maroon body text, and the brand red appears in bulk as
`rgb(210, 37, 31)`.

### 3.3 Type

One family does everything: a variable geometric sans in weights 100
through 900, roman and italic, with a system fallback stack, plus an icon
font for interface glyphs. Weight tokens are named from thin through
black, and the base is 400 at 1rem with a 1.5 line height.

Measured scale: 16px/24px body (the workhorse at 28,226 uses), 15px/24px
the dense interface and card band at 400, 600 and 700, 14px/21px fine
print, 12px/14.4px micro-labels, 20px/30px card titles, 18px/18px
compact heads, and a fluid display ladder rendering around 16px to 19.4px
at 500 in its measured intermediate steps, which is the clamp function
sampled mid-scale rather than a fixed size.

### 3.4 Surfaces and depth

Depth is restrained: hairline borders in the grey-light token, soft
shadows at black 10 and 20 percent for raised cards, a 26 percent step
for overlays, and full-bleed imagery with a dark scrim for hero and card
overlays. The default transition speed is a measured 0.3 seconds, and the
single easing curve used across the whole site is the reveal curve of
Section 6, applied 88 times.

Cards are the site's primary object: an event card carries an image, a
status chip (open to the public, or trade fair with registration
required), a title, a date or date range, a time range, one or more space
chips naming the halls used, a sector chip, a description and outbound
actions. The same card renders in the calendar, on the home page and in
search results.

> **In plain language.** The venue's colours are a strong red for
> anything you can press, a deep maroon for reading, and a coral that
> appears when you hover, all on white with hairline grey rules. One
> typeface does everything, from the giant headline to the small print.
> Spacing is elastic: the gaps between sections grow smoothly with the
> window rather than jumping at fixed sizes. The workhorse object is the
> event card, which shows a photograph, whether the event is open to the
> public, when it runs and which halls it occupies.

## 4. Iconography and the floor plan

- The logo is a wordmark supplied as a vector; it is rebuilt as drawn
  geometry per Section 37 and always carries an accessible name.
- Interface glyphs come from an icon font in the reference build. An
  icon font is a graded defect rather than a style choice: it fails when
  the font fails, is announced as a letter by assistive technology, and
  cannot inherit two colours. The rebuild replaces it with a drawn
  stroke set on a 24 box inheriting text colour, each glyph carrying a
  title where it is meaningful and hidden where it is decorative:
  chevron, arrow, close, search, menu, calendar, location pin, clock,
  download, external link, plus the social marks.
- The wordmark is drawn geometry on a `0 0 843 248` box, twenty-five
  letterform paths beginning `M249.651 182.059`; it is reproduced as
  those paths, never as a font glyph, and always carries an accessible
  name.
- The floor plan is measured as a single inline vector on a
  `0 0 1563.8 1080` box carrying seventy primitives, drawn as closed
  polygons rather than paths: each hall is a polygon (the first,
  `472.84 339.19 495.83 325.92 347.81 246.12 347.81 266.19`, is a
  connecting way), with the campus outline, the halls, the boulevard and
  the passages as sibling regions and the hall numbers as text nodes
  positioned inside them. A second decorative vector on a
  `0 0 498 1116` box carries the page's angled background form. The plan
  is inline vector geometry, not an image: an outline of the campus with each hall as a
  closed region carrying its number as a text node (1 through 6 plus the
  event hall marked XXL), the meeting centre, the covered boulevard
  connecting the halls, and the passages between adjacent halls. Regions
  are interactive: hovering lifts a region and its number, choosing one
  scrolls to that hall's specification, and the plan is keyboard
  navigable region by region with a visible focus outline. It is drawn
  from the space model of Section 15, so a space added in operations
  appears on the public plan without redrawing anything.
- Event status chips and sector chips are pill labels, never colour
  alone.

> **In plain language.** Every small picture is drawn from coordinates
> rather than shipped as an image, including the map of the site. That
> map is not a picture: each hall is a shape that knows which hall it is,
> lights up as you move over it, can be reached with the keyboard, and
> comes from the same list of spaces the staff book, so it can never
> disagree with reality.

## 5. Global chrome

### 5.1 Header

A utility strip carries the jobs link, the parent group link and the
three language codes. Beneath it sits the main bar: the wordmark at left
and six primary items (calendar, visit, organise, about, news, contact),
of which visit, organise and about open a panel of child links. A search
control opens a full-width overlay with one field labelled to search the
whole website. Below the tablet step the whole navigation collapses into
a panel that keeps the same order and the same language codes.

The language switcher is graded: it must preserve the current page and
its parameters, so switching language on a hall page lands on the same
hall in the new language, not the home page.

### 5.2 Footer

The wordmark, the sustainability charter mark, the copyright line and
four legal links (general conditions, the safety manual, the privacy
policy and the cookie policy), plus the newsletter invitation and the
three social profiles. The safety manual link points into the media kit
page's document anchor, which is a real anchor and must resolve.

### 5.3 Consent

A consent platform gates statistics and marketing categories with a
necessary category that cannot be refused. Refusal is honoured: nothing
in the statistics or marketing categories loads until consent is given,
and withdrawing consent stops it thereafter. The consent record carries
an identity and a date, and the cookie policy page lists every cookie by
provider, purpose, retention and type, generated from the same
declaration the banner enforces rather than hand-written.

### 5.4 Shared furniture

Buttons in solid red, outline and text forms with the measured 0.3 second
transition; breadcrumbs on every inner page; carousels for galleries and
case studies with keyboard controls and honest pagination; accordions for
questions; a lightbox for gallery images; and a newsletter capture band.

> **In plain language.** A slim strip at the very top holds the jobs
> link, the group link and the three languages. The main bar has six
> sections, three of which open panels. Switching language keeps you on
> the page you were reading, which sounds obvious and is exactly the
> thing that is usually broken. The footer holds the legal set and the
> safety manual, and the cookie notice actually obeys a refusal instead
> of merely recording it.

## 6. Motion language

### 6.1 Easing

One curve carries the site, measured eighty-eight times:
`cubic-bezier(.16,1,.3,1)`, a strong decelerating settle. The default
duration token is 0.3 seconds. Motion is gated positively behind a
no-preference query, so the reduced-motion state is the default rather
than an afterthought.

### 6.2 Named behaviours, all measured

| Behaviour | Specification |
|---|---|
| scroll reveals | section content rises and fades on the settle curve as its band enters, once per band, driven by a scroll-position library |
| hero arrow bounce | a downward cue translating 0.9375rem and back, inviting the first scroll |
| wiggle | a five-degree rotation settle used to draw attention to a single element |
| carousel slides | horizontal and vertical slide-in and slide-out pairs offset by the carousel gap token, with crossfades for the lightbox |
| lightbox zoom | images enter scaling from 0.975 with a 16px rise and leave the same way, with a throw-out variant on dismissal |
| progress bar | a scaling bar for carousel and gallery progress |
| spinners | rotation loops for loading states |

Under reduced motion, which is the default state, none of the reveals,
bounces, wiggles or slide animations run: content renders in place and
carousels change slides instantly.

> **In plain language.** The whole site moves with a single gesture: a
> quick glide that slows into place. Sections arrive as you scroll, a
> small arrow bounces to invite that first scroll, and galleries slide
> and zoom. Because the site asks the device first, anyone who prefers
> stillness gets a completely still page by default rather than having
> to opt out.
## 7. Route: home

Band order normative; copy in Section 38.

1. Hero: the display line "when ideas need space" over a full-bleed
   image with a dark scrim, two actions (view the calendar, organise your
   event) and the bouncing scroll cue.
2. Coming soon: three event cards from the calendar, each with its status
   chip, dates, times, hall chips, sector and outbound actions, over an
   all-events link.
3. Visitor invitation: a banner asking whether the reader is visiting
   soon, with the practical-information paragraph and a plan-your-visit
   action.
4. Organiser invitation: the paragraph about a versatile venue for
   conferences, corporate events, trade shows and meetings, the promise
   that the venue does not merely rent halls, and the fifty-years-of-
   experience line, followed by a nine-image gallery with a lightbox.
5. The right setting: the "blank canvas of nearly 40,000 square metres"
   paragraph with two actions, then four summary blocks, verbatim in
   Section 36: six halls each with its own character; the meeting centre
   of five rooms usable separately or combined; the covered boulevard
   that connects all halls, has two entrances and doubles as exhibition
   or catering space; and the in-house restaurant that combines
   self-service speed with bistro quality.
6. Inspiration: case cards, each carrying the halls it used, over a
   more-events link.
7. Stay up to date: the newsletter invitation and the three social
   profiles.
8. Newsflash: news cards with a category chip, a date and a read link.
9. Footer.

> **In plain language.** The front page says its promise in four words
> over a photograph, shows what is coming soon, then splits the audience:
> visitors get practical information, organisers get the pitch and a
> gallery. It then explains the building in four blocks, six halls, five
> meeting rooms, the covered boulevard and the restaurant, shows what
> other people have staged there, and ends with the newsletter and the
> news.

## 8. Route: calendar

The public calendar is the venue's most-used page and the platform's
public face.

- Every entry is an event card per Section 3 with its status chip (open
  to the public, or trade fair with registration required), title, date
  or date range, daily time range, the halls it occupies, its sector,
  its description and its outbound actions (its own website, and a
  ticket link where selling is external).
- Filters: by month and date range, by status, by sector, and by hall,
  with the filter state shareable through the address bar and reflected
  in the page title for screen readers.
- The calendar reads the same records the operations platform books, but
  publishes only what an event's organiser has marked public and only
  after its publication date, so an event held in the diary for a client
  who has not announced it is invisible here (Section 24, graded).
- Multi-day events render once with their range, not once per day, and
  an event running past midnight belongs to the day it started.

> **In plain language.** The calendar lists what is on: what it is,
> whether anyone can walk in or it is a trade fair needing registration,
> which halls it fills, and when. You can filter by month, by kind and by
> hall, and share that filtered view as a link. Crucially, an event only
> appears here once its organiser has agreed to announce it, because the
> same diary holds bookings nobody is allowed to know about yet.

## 9. Route: organise, spaces

The specification's physical backbone, and the page that binds Section
15. It carries the interactive floor plan of Section 4 and, beneath it,
one specification block per space with its capacity, area, unique
features and the event types it suits. The measured inventory is
normative fixture data:

| Space | Capacity | Area | Character and suitability |
|---|---|---|---|
| Hall 1 | up to 1,620 visitors | 6,090 m² | the oldest hall, characteristic wooden trusses giving a vintage look; wooden columns; trade fairs and conferences |
| Hall 2 | up to 1,740 visitors | 4,058 m² | elongated, in the same style as Hall 1, wooden trusses worked into the ceiling; trade fairs, conferences, performances |
| Hall 3 | up to 1,680 visitors | 3,601 m² | the smallest hall, characteristic yellow grid ceiling; yellow tube structure, riggable; trade fairs and events |
| Hall 4 | up to 3,660 visitors | 7,685 m² | the largest and most recent hall; black box |
| Hall 5 | up to 5,160 visitors | 4,723 m² | a square black box, excellent for events and parties; acoustic panels; parties, club nights, trade fairs |
| Hall 6 | up to 1,860 visitors | 5,055 m² | the same style as Hall 3 but considerably larger; trade fairs, conferences, events |
| The event hall (XXL) | up to 2,000 people | 2,000 m² | the newest event hall, suitable for any reception or conference; a tribune seating 550; parties, receptions, conferences, seminars |
| Meeting Centre | four combinable MC rooms beside the event hall | 1,679 m² total | modular, its own entrance, a terrace with garden; meetings and receptions |

Note the inversion that any capacity model must respect: Hall 5 holds
more people than Hall 4 in less than two thirds of the floor area,
because capacity is a function of layout, exits and licensing rather than
of square metres. A build that derives capacity from area is wrong, and
Section 15 grades it.

The page closes with the flexible-combinations paragraph, the venue-team
introduction, six reasons organisers choose the venue (in-house
experience, flexible spaces, bespoke catering, easy access, ample
parking with 2,500 spaces, and end-to-end care), a case-study strip and
an enquiry form.

> **In plain language.** This page is the building, written down. A map
> you can click, then a card per hall with how many people it holds, how
> big it is, what makes it distinctive and what it is good for. One
> detail matters more than it looks: the hall that holds the most people
> is not the biggest one, because capacity comes from exits and licences,
> not floor area. Software that guesses capacity from size gets this
> building wrong.

## 10. Routes: organise, the rest

- Meetings: the modular meeting centre, its rooms, their combinations,
  the audiovisual provision and the catering that accompanies a meeting,
  with its own contact team block.
- Catering: the offer from receptions through walking dinners to the
  self-service exhibition restaurant, with the note that catering is
  in-house.
- The in-house restaurant: the fast-gourmet kitchen brand, its concept
  and its role on busy fair days.
- Accessibility and the region: reaching the venue by road, rail and air
  as an organiser, and what the surrounding region offers delegates.
- Unique events: case studies, each naming the spaces used and what was
  done with them. The measured cases are normative fixtures: a high-end
  trade event using Halls 4 and 5 plus the passage between them; a
  corporate event where an agency transformed Hall 3 for more than 900
  guests with mobile catering points and the south entrance used for
  access control; and a five-edition public fair using Halls 1, 2, 3 and
  6 for the fair and children's play area with the meeting rooms and the
  event hall used for signings, presentations and interviews.

Every case study demonstrates the combination model of Section 15, and
the third one is the specification's canonical stress case.

> **In plain language.** The rest of the organiser section covers the
> meeting rooms, the food, the restaurant, how to get here, and real
> examples. Those examples are the important part: one event used two
> halls plus the corridor between them, another filled a single hall with
> a party for nine hundred people, and a book fair took four halls, the
> meeting rooms and the event hall at once. Any booking system for this
> building has to be able to describe all three.

## 11. Routes: visit

- The visitor hub, then accessibility and parking (routes, the 2,500
  parking spaces, public transport and drop-off), food and drink on
  site, what to do in the city, and the frequently asked questions as an
  accordion.
- Visitor pages are the most-read pages during an event and must be
  legible on a phone in a car park: large touch targets, no reliance on
  hover, and the practical facts above the fold.

> **In plain language.** Everything a visitor needs on the day: how to
> get here, where to park, what to eat, what to do in town and the
> answers to the questions the desk is asked most. These pages are read
> on a phone in a car park, so the practical facts come first.

## 12. Routes: about and news

- About: the hub, who we are, the history of fifty years on the site,
  sustainability and safety, and the media kit with downloadable logos,
  floor plans and the safety manual behind a real document anchor.
- News: an index of cards with category chips and dates, and article
  pages. The measured fixtures are a corporate item about the parent
  group being acquired and a sustainability item about the venue
  achieving the regional charter for the tenth consecutive year; both
  ship with substituted names.
- The news index is graded lightly for one thing: an article published
  in one language and not yet translated must not disappear from the
  other languages, and must be labelled as available in another language
  rather than silently omitted.

> **In plain language.** The company pages and the newsroom. One rule
> matters: a piece of news written only in Dutch should still be visible
> to a French reader, marked as being in another language, rather than
> quietly vanishing, because a visitor comparing the three versions of
> the site should never wonder what they are not being shown.

## 13. Routes: contact, legal and not-found

- Contact: the enquiry form that starts the sales path of Section 16,
  with the measured fields (first name, last name, email, and the kind of
  event being organised) plus the date range, expected visitors and the
  spaces of interest. Submission creates an enquiry in the platform, not
  merely an email, and the form states what happens next.
- Legal: general conditions, the privacy policy and the cookie policy,
  each dated and in the reading column, with the cookie policy generated
  from the consent declaration per Section 5.
- Not-found: the measured screen with a route home and a search field.

> **In plain language.** The contact form is the front door of the sales
> process: filling it in actually creates an enquiry in the system rather
> than sending an email into somebody's inbox. Then the legal pages, and
> a lost-visitor page that offers search rather than a dead end.
## 14. Platform: the operations shell

Difficulty: medium.

Behind sign-in: a campus calendar as the home surface, an enquiry desk,
booking files, the floor-plan planner, services and catering,
accreditation, access control, the safety board, works scheduling,
invoicing, the publishing desk and reporting.

Roles are the venue's real ones and are enforced server-side: sales,
event coordinator, operations, technical, catering, security, finance,
publisher, and a read-only management role. A role is scoped to a
function, not to a person, and a person may hold several. Every gate is
enforced at the data layer, and a forged request from a role that lacks a
right fails even though the interface never offers it.

> **In plain language.** Signed in, staff see the campus diary first,
> then the desks they work at. The venue's real jobs are the roles:
> sales, coordination, operations, technical, catering, security,
> finance and publishing. What each may do is enforced in the vault
> rather than merely hidden on screen.

## 15. Platform: the space model

Difficulty: expert. This is the heart of the exam.

The campus is a graph, not a list:

- Every space is a node with an area, a licensed capacity, an entrance
  set, and an availability calendar. Capacity is a stored, licensed
  figure per space and per layout, never derived from area (Section 9
  proves why: the venue's highest-capacity hall is not its largest).
- Spaces compose: adjacent halls combine into one hireable space, the
  passage between two halls is itself hireable and is also what makes
  the combination possible, the covered boulevard connects every hall
  and can be hired as exhibition or catering space while remaining the
  public route between halls, and the meeting rooms combine with one
  another and with the event hall. Composition is data: a combination is
  a node whose children are the spaces it consumes.
- The overlap rule, graded: holding a combination holds every descendant
  space, and holding any descendant blocks every ancestor combination. No
  two bookings may ever hold the same square metre at the same time, and
  the check must be one authority used by the enquiry desk, the planner,
  the public calendar and the reporting alike. Checking availability only
  at the leaf level, or only at the level booked, is the named wrong fix
  here: it passes every casual test and double-books the boulevard.
- Circulation constraint: the boulevard may be hired as exhibition space
  only while a compliant public route between the halls in use remains,
  so hiring it is refused when the resulting route would fail the
  occupancy rules of Section 21. This is the constraint that makes the
  model more than a calendar.
- Layouts: a space has named layouts (theatre, cabaret, banquet, stand
  grid, standing) each with its own capacity and its own build time; the
  layout chosen changes both the number the safety board enforces and
  the hours the works schedule reserves.
- Capacity per combination is not the sum of its parts: a combination
  carries its own licensed figure, because exits and circulation change
  when a wall opens. The build must store combination capacities and
  refuse to add children's numbers.

> **In plain language.** The building is not a list of rooms, it is a set
> of shapes that fit inside one another. Two halls plus the corridor
> between them become one big space; the covered street that links every
> hall can be rented for stands but still has to work as the way people
> walk from hall to hall. So the software cannot simply mark a room busy:
> booking the combination must lock every part of it, booking any part
> must lock the combination, and the number of people allowed in a joined
> space is its own licensed figure, not the two smaller numbers added
> together. Getting this wrong is invisible in a demo and catastrophic on
> the day.

## 16. Platform: enquiry, option and contract

Difficulty: expert.

- An enquiry arrives from the public form or from sales and carries
  dates, expected visitors, event type and spaces of interest.
- An option is a soft hold on named spaces across named dates, with an
  expiry and a rank. Several options may exist on the same space and
  dates, ranked first, second and third; taking a lower-ranked option
  does not block a higher one, and confirming any option releases the
  others with a notification. The rank behaviour is graded, because
  first-refusal is how venues actually sell.
- A challenge, the venue trade's own mechanism: a lower-ranked option
  may challenge the holder, who has a stated window to confirm or
  release. The window, the notification and the automatic outcome on
  expiry are all part of the model, not a manual process.
- Confirmation converts the option into a booking atomically: the space
  set, the build-up and tear-down windows of Section 17 and the contract
  record are created in one transaction, and two coordinators confirming
  competing options in the same instant resolve to exactly one booking
  and one clear refusal.
- The contract file holds the terms, the priced services, the deposit
  schedule and the signatures; a signed contract locks the space set,
  and any later change goes through an amendment that records who
  approved it and what it moved.

> **In plain language.** Venues sell space by holding it. Several
> customers can hold the same week in order of preference, and if the
> second in line wants to commit, the first is asked to decide within a
> stated time. All of that is in the software rather than in somebody's
> head, and when two people finally confirm at the same second, exactly
> one booking exists afterwards.

## 17. Platform: the event timeline

Difficulty: expert.

A booking is not a day, it is a span with phases: access, build-up,
run, tear-down and clearance, each with its own start and end, its own
occupancy rules and its own accreditation profile.

- Build-up and tear-down consume the space exactly as the run does, so
  the next event cannot begin building while the previous one is still
  dismantling in the same hall. The campus timeline shows every phase of
  every event on one axis, and the graded case is the tight turnaround:
  two events sharing a hall on consecutive days must be refused unless
  the tear-down and build-up windows genuinely fit, with the shortfall
  named in hours.
- Phase changes cascade: extending a run pushes tear-down, which may
  collide with the next booking's build-up, which must raise a conflict
  to a coordinator rather than silently overwriting either.
- Shared infrastructure is scheduled with the spaces: loading docks,
  freight lifts, forklifts, rigging crews and power drops are finite and
  are booked against the same timeline; two events building at once may
  contend for a dock, and the schedule must show and resolve that.
- Layout build times from Section 15 seed the default phase lengths.
  Treating build-up and tear-down as calendar annotations beside the
  booking rather than as occupancy of the space is the named wrong fix
  here: the diary looks correct and two events collide in the hall.

> **In plain language.** An event is not one day in the diary. It is the
> days spent building it, the days it runs, and the days spent taking it
> down, and all of those occupy the hall. The classic mistake is booking
> two events back to back and discovering that one cannot get out while
> the other is coming in. The software refuses that, and tells you how
> many hours short you are. The same goes for the loading bays and the
> forklifts, which two events building at once will otherwise fight over.

## 18. Platform: the floor-plan planner

Difficulty: expert, and it is the frontend expert.

The planner is where an event's floor plan is drawn on the venue's own
geometry:

- The canvas renders the true space geometry from Section 15, at scale,
  with structural constraints drawn as first-class objects: columns, the
  wooden trusses and their heights, doors and their widths, fire exits
  and their required clearances, rigging points and their load limits,
  power and water positions, and the ceiling height envelope.
- Objects placed on it (stands, catering points, stages, seating blocks,
  entrances) snap to a grid, carry dimensions, and are validated live:
  a stand that blocks an exit, encroaches on a required aisle width,
  sits on a column, or exceeds a rigging point's load is flagged at the
  moment it is placed, with the rule named and the offending measurement
  shown.
- Performance under load, graded: a plan of eight hundred stands pans
  and zooms at frame rate, and validation runs incrementally on the
  objects a change actually affects rather than the whole plan, so
  dragging a stand never stalls the canvas.
- Concurrency, graded: two planners working the same plan see each
  other's cursors and changes within a second, edits merge per object,
  and an object one planner is dragging cannot be moved out from under
  them; a conflicting simultaneous move resolves to one position on both
  screens without either planner's other work being lost.
- Versions: a plan has revisions with a compare view, an approval state
  and an approver, and the approved revision is the one that flows to
  the works schedule, the safety board and the exhibitor pack.

> **In plain language.** The plan is drawn on the real building, with
> its columns, doors, fire exits and rigging points all present as things
> the drawing knows about. Put a stand across a fire exit and it is
> flagged the moment you let go, with the rule quoted and the distance
> named. It has to stay smooth with eight hundred stands on it, and two
> planners must be able to work on it at once without either one's work
> disappearing.

## 19. Platform: accreditation

Difficulty: expert.

Every person on site belongs to a party with rights that vary by day,
by phase and by space:

- Parties: the organiser, exhibitors, stand contractors, the venue's own
  operations and technical staff, caterers, security, cleaners and
  visitors. Each is accredited per event, per phase and per space set.
- Accreditation carries evidence where the law requires it: insurance
  certificates with expiry dates, risk assessments for the works being
  done, competence records for rigging and electrical work, and
  identity for security. An expired certificate withdraws the
  accreditation automatically at the moment it expires, not at the next
  manual review, and any badge derived from it stops working.
- Delegation, the enterprise case: an organiser accredits its
  exhibitors; an exhibitor accredits its own stand contractor. Rights
  granted downstream can never exceed the granter's own rights, and
  revoking an organiser's accreditation cascades to everyone
  accredited under it within a second. This cascade is graded, because
  it is exactly where naive permission systems leak. Leaving revocation
  and expiry to a nightly job is the named wrong fix: it passes every
  demo and leaves a withdrawn contractor holding a working badge.
- A person may hold accreditations for several concurrent events from
  different parties; their rights at any instant are the union of what
  is currently valid, scoped to the space and phase they are standing
  in.

> **In plain language.** Everyone on site, the organiser, their
> exhibitors, the builders those exhibitors hire, the caterers, the
> cleaners, is accredited for particular days, particular halls and
> particular phases. Papers matter: an insurance certificate that
> expires at midnight takes the badge with it. And because an organiser
> vouches for its exhibitors, who vouch for their builders, withdrawing
> the organiser has to withdraw everyone underneath, immediately, which
> is precisely where this kind of software usually leaks.

## 20. Platform: access control

Difficulty: expert.

- Every entrance is a controlled point with a mode per phase: staff
  only, contractor, exhibitor, trade visitor with registration, or open
  public. The measured case study in Section 10 uses one entrance for
  access control while other entrances stay closed, so entrance mode is
  per event and per phase, not a site-wide setting.
- Badges are issued from accreditation and are scanned at entrances.
  A scan is evaluated against current accreditation, current phase,
  current space rights and the current occupancy of Section 21, and the
  decision is returned within a bounded time even when the network to
  the central system is degraded.
- Offline tolerance, graded: an entrance whose connection drops keeps
  admitting on a locally cached rule set with a stated staleness bound,
  queues its scans, and reconciles on reconnect; revocations issued
  while it was offline take effect on reconnect and the resulting
  admitted-after-revocation events are surfaced to security rather than
  swallowed. Admitting nobody when offline is unsafe in a crowd, and
  admitting everybody is a breach; the specification requires the
  middle path and the grader drives it.
- Anti-passback and re-entry: a badge that has entered and not left
  cannot be used again at another entrance, with a stated grace for
  legitimate re-entry, and the rule may be relaxed per event.
- Every scan, admitted or refused, is written to an append-only log
  with the entrance, the badge, the decision and the reason.

> **In plain language.** Each door can be set differently for each part
> of an event: builders only during build-up, registered trade visitors
> on the first day, everyone on the public day. Badges are checked at the
> door against who you are, what phase it is and whether the hall is
> already full. If a door loses its connection it must not lock everyone
> out nor let everyone in; it carries on with the rules it last knew, for
> a stated time, and confesses on reconnect if it let someone in who had
> just been withdrawn.

## 21. Platform: occupancy and safety

Difficulty: expert. This is the section that must hold on the worst day.

- Live occupancy per space is derived from entrance and internal scans
  and is compared continuously against the licensed capacity of the
  space or combination in its current layout. Approaching the limit
  raises a graded alert; reaching it closes admission to that space
  while leaving exits free.
- Occupancy is a graph problem, not a counter: a person admitted to a
  combination is present in every constituent hall, and moving between
  halls through the boulevard must not double-count them. A naive
  per-door counter overstates occupancy and closes a hall that is not
  full; the grader drives exactly that traffic pattern. Counting per
  door is the named wrong fix, and it fails only once a joined hall is
  busy, which is the day it matters.
- Exit capacity: each space's licensed figure is bound to its available
  exits in the current plan, so an approved floor plan that blocks an
  exit reduces the licensed figure automatically and the safety board
  shows the new number and why.
- Incidents are first-class: raised with a type, a location on the floor
  plan, a severity and an owner, with a timeline of actions and a
  required close-out.
- Evacuation state overrides everything: declaring it opens all
  entrances as exits, suspends admission, publishes muster information
  to staff devices, and freezes the access log for the investigation.
  Nothing in the system may prevent an exit.
- The regime is auditable: the venue holds a sustainability and safety
  charter awarded ten consecutive years and publishes a safety manual,
  so every capacity change, plan approval, incident and evacuation drill
  is recorded append-only with actor and time.

> **In plain language.** The building has legal limits on how many
> people may be inside each hall, and those limits depend on the exits,
> which the floor plan can block. So the plan and the safety limit are
> connected: approve a plan that blocks a door and the allowed number
> drops, visibly, with the reason. Counting people is harder than it
> sounds, because someone who walks from one joined hall into the next
> has not arrived twice. And when the alarm goes, everything else stops
> mattering: every door becomes an exit, and the record freezes for the
> investigation.

## 22. Platform: services, catering and technical orders

Difficulty: hard.

- The venue sells services with the space: catering from receptions to
  walking dinners to the self-service restaurant, technical services
  (power drops, rigging, lighting, sound, internet), furniture, cleaning,
  waste, signage, and parking allocations.
- Each service has a lead time and an order cut-off relative to the
  event phase, a unit and a price, and some have dependencies (a rigging
  order requires an approved plan; a power drop requires a position on
  that plan). Ordering after the cut-off is possible only with a
  surcharge and an approval, and both are recorded.
- Catering orders carry headcounts with a confirmation deadline,
  dietary requirements, service times tied to the run phase, and
  delivery points that are positions on the floor plan (the measured
  case study places mobile catering points throughout a hall).
- Exhibitor ordering: exhibitors order for their own stand within the
  organiser's rules, which may cap spend, restrict suppliers or require
  approval; the organiser sees the aggregate.

> **In plain language.** Renting the hall is the start; the venue also
> sells the power, the rigging, the furniture, the cleaning and the food.
> Each of those has a deadline, and ordering late costs more and needs
> permission, which the system records rather than arguing about later.
> Catering is tied to the plan, so a coffee point has a place on the map
> as well as a time.

## 23. Platform: invoicing and settlement

Difficulty: hard.

- A booking accrues charges from the space hire, the phase durations,
  the services ordered, the consumption metered during the event
  (power, water, waste, cleaning hours) and any late-order surcharges.
- Money is integer minor units throughout, with the value-added tax
  regime applied per line by rule with the rounding recorded, so lines
  sum exactly to the invoice.
- Deposits and stage payments follow the contract schedule; the final
  invoice reconciles estimates to actuals with every variance
  attributable to its cause, and an exhibitor's own charges are billed
  to the exhibitor while the organiser sees the summary.
- Damage and cleaning charges arising from tear-down inspection are
  raised with evidence and a dispute path.

> **In plain language.** The bill is the sum of the hall, the days, the
> services ordered, and what was actually used, with the difference
> between the estimate and the reality explained line by line rather
> than presented as a surprise. Exhibitors pay their own extras
> directly, and anything charged for damage comes with photographs and
> a way to argue.

## 24. Platform: publishing to the public site

Difficulty: hard.

The public calendar and event pages are published from the operations
records, in three languages, and the boundary is graded:

- An event carries a publication state (private, announced, published)
  and a publication date; nothing reaches the public site before that
  date, and a client's unannounced booking is invisible even though it
  occupies the diary.
- Public fields are an explicit subset: title, description, dates,
  public times, status, sector, the halls named for wayfinding, the
  organiser's own links. Internal fields (rates, contacts, contract
  terms, occupancy, incidents) can never be published, and the build
  must make that structurally impossible rather than a matter of care.
  Filtering internal fields at render time is the named wrong fix: one
  forgotten template exposes a rate card.
- Translations: each public field carries per-language values with a
  translation state; a missing translation falls back with a visible
  label per Section 12 rather than showing an empty field or the wrong
  language silently.
- Publishing is atomic per event and takes effect on the public site
  within a minute; unpublishing removes it just as fast, because an
  event pulled at a client's request must actually disappear.

> **In plain language.** What the public sees comes from the same diary
> the staff use, but only the parts an organiser has agreed to announce,
> only after the agreed date, and only the fields meant for the public.
> Rates and contact details cannot leak, by construction rather than by
> being careful. And when a client asks for their event to come off the
> site, it goes within the minute.

## 25. Platform: the exhibitor portal

Difficulty: hard.

Exhibitors are the venue's largest population of users and get their own
surface: their stand and its position on the approved plan, their
accreditation and badges, their service orders within the organiser's
rules, their build-up slot for the loading dock, their documents (the
safety manual, the technical specification, the deadlines), and their
invoices. Everything they see is scoped to their stand, and the grader
forges a request for another exhibitor's orders and position.

> **In plain language.** The hundreds of companies exhibiting at a fair
> each get a small private area: where their stand is, who from their
> team may come in, what they have ordered, when their van can use the
> loading bay, and what they owe. What they can see stops at their own
> stand.

## 26. Platform: works and technical scheduling

Difficulty: hard.

The venue's own crews and equipment are finite and shared across
concurrent events: riggers, electricians, cleaners, forklifts and their
drivers, lifts, and the loading docks of Section 17. Work orders are
scheduled against people and equipment with competence requirements
(only a qualified rigger may be scheduled to rigging work), shift
limits, and a clash view. A work order whose plan approval is withdrawn
is suspended rather than silently executed.

> **In plain language.** The people and machines that make an event
> happen are a shared, limited resource, and the schedule treats them
> that way: the right qualification for the job, no double-booking of a
> forklift, no shifts that break working-hours rules, and no work
> carried out against a plan that has just been withdrawn.

## 27. Platform: reporting

Difficulty: medium.

Occupancy of the campus over time by space and by combination, revenue
per event and per square metre per day, service attachment rates,
turnaround performance against the phase model, incident rates and
close-out times, accreditation compliance including expired-certificate
events, and the sustainability metrics the charter requires (waste
streams, energy per event, reusable stand material). Every figure derives
from the ledgers, and the same period totalled along different axes must
agree exactly.

> **In plain language.** The reports answer the questions a venue's
> management actually asks: how full is the campus, what does each
> square metre earn, how quickly can we turn a hall around, how often do
> incidents happen and how fast are they closed, and how are we doing
> against the sustainability charter we have held for ten years.

## 28. Platform: integrations

Difficulty: hard.

- Ticketing: external ticketing systems own sales for public events; the
  platform imports sold volumes for occupancy forecasting and accepts
  scan events from ticket gates, deduplicated against its own scans.
- Parking: the 2,500 spaces are allocated per event with pre-booked
  allocations for exhibitors and staff, and live counts feed the
  visitor-information pages.
- Finance: invoices and payments synchronise to an accounting system
  behind an interface, idempotently, so a retried export never
  duplicates an invoice.
- Publishing: the public site consumes the published subset of Section
  24 through one authority.

> **In plain language.** Tickets are usually sold by somebody else, so
> the system takes their numbers and their gate scans without
> double-counting. The car park is allocated per event and its live
> count reaches the visitor pages. And the accounts leave through one
> tidy door that cannot produce the same invoice twice.
## 29. Platform: wayfinding and the visitor day

Difficulty: expert, and it is a frontend expert.

The venue's own case study notes that visitors find their way thanks to
the direct connection between the spaces used, and the public site
carries the plan. On the day, wayfinding is a live surface:

- The visitor plan is the same geometry as Section 4, rendered for a
  phone held in a corridor: the visitor's entrance, the halls in use for
  the event they came for, the catering points from the approved floor
  plan, the toilets, the exits and the route between them.
- It must work on the venue's worst network: the plan and the current
  event's data are cached on first load, the page renders fully offline,
  and a stale cache announces its age rather than silently showing
  yesterday's layout. A build that requires the network to draw the map
  is the named wrong fix, because the halls are steel boxes and the
  signal dies inside them.
- Live state changes what it shows: a hall closed for turnaround, an
  entrance switched from public to staff, a catering point sold out, or
  an incident closing a route all redraw the map within a minute of the
  operations change, and a closed route is never offered as a path.
- Accessibility is not a mode: the plan has a step-free route layer, and
  every route it draws is available as an ordered list of written
  directions, because a map is unusable to a portion of visitors and
  the venue's own accessibility page promises otherwise.
- Language follows the visitor, not the venue: the three languages of
  Section 2 apply here, and a visitor who arrived on the French site
  gets French directions.

> **In plain language.** On the day, the map on your phone has to work
> inside a steel hall where the signal dies, so it is downloaded before
> you need it and says how old it is rather than lying. It shows only the
> halls your event is using, where the coffee is, and where the exits
> are, and it redraws when the venue closes a route. Everyone who cannot
> read a map gets the same directions written out, step by step, in
> their own language.

## 30. Platform: the annual campus plan

Difficulty: expert.

A venue does not sell days one at a time; it plans a year, and that plan
is where the money is made or lost:

- The annual view shows every hall across a year with confirmed
  bookings, options at their ranks, and the recurring anchor events that
  return every edition, together with maintenance windows, the venue's
  own fair concepts, and the closed periods.
- Recurring events hold their slot across editions: a fair in its fifth
  edition carries a provisional hold on the same week next year, which
  ages into a real option and then a booking, and losing that hold is a
  commercial event the system surfaces rather than a silent gap.
- Yield: the planner shows revenue per square metre per day for any
  window, so a coordinator can see what a low-value booking costs in
  displaced capacity. Accepting a booking that blocks a larger one is a
  decision, and the system makes it a visible one.
- Maintenance is scheduled against the same space model as events: a
  floor resurfacing in Hall 3 occupies Hall 3 exactly as an event does,
  and cannot be booked over.
- Scenario planning: a coordinator may fork the annual plan, move
  bookings in the fork to test a rearrangement, and see the conflicts
  and yield differences before committing; committing applies the fork
  atomically or fails whole, never partially.

> **In plain language.** Venues plan a year at a time. The big fairs come
> back every year and hold their week, the halls need resurfacing
> sometimes, and saying yes to a small booking in a big hall can quietly
> cost more than it earns. This view shows all of that on one line per
> hall, lets a planner try a rearrangement in a copy without touching
> reality, and then either applies the whole rearrangement or none of it.

## 31. Backend and data contract

Entities and invariants are normative; names are the builder's.

| Entity | Key fields | Invariants |
|---|---|---|
| space | kind, area, entrances, parent and child links | capacity never derived from area |
| layout | space, name, capacity, build hours | capacity is licensed data per layout |
| combination | member spaces, licensed capacity | own capacity, never the sum of children |
| availability hold | space set, window, kind (option or booking), rank, expiry | holding any node blocks ancestors and descendants |
| enquiry | contact, dates, spaces of interest, source | creates from the public form |
| option | enquiry, space set, window, rank, challenge state | ranks unique per space and window |
| booking | option, contract, phases | confirmation is atomic across spaces, phases and contract |
| phase | booking, kind, window | phases occupy space exactly as the run does |
| resource | docks, lifts, forklifts, crews | finite; scheduled on the same timeline |
| floor plan, revision, object | geometry, constraints, approval | approved revision drives works, safety and packs |
| party, accreditation | event, phase, space set, evidence, expiry, granter | rights never exceed the granter's; revocation cascades |
| badge, scan | accreditation, entrance, decision, reason | append-only; offline scans reconcile |
| occupancy sample | space, count, at | derived from the graph, never double-counted |
| incident, evacuation | type, location, severity, owner, timeline | append-only; exit never blocked |
| service order | booking or exhibitor, service, quantity, cut-off state | dependencies enforced; late orders recorded |
| invoice, line, payment | amounts in minor units, tax rule, rounding record | lines sum exactly to the invoice |
| publication | event, state, date, per-language fields | public subset structurally separate from internal fields |
| audit row | actor, action, target, before, after, at | append-only in the store |

Schema evolution: the space model, layout capacities, licence figures
and accreditation rules all version, and every booking, plan revision,
badge and invoice records the version it was written under. A licence
figure revised after a fire-safety inspection must not retro-fit last
year's approved plans or the occupancy records taken under them:
history reads at its own version, and only future bookings inherit the
new figure. Migrations are forward-only, run once, and are covered by
fixtures the grader holds. Rewriting historical capacity to today's
figure is the named wrong fix, and for a venue holding a safety charter
it is the difference between an audit passed and an audit failed.

Every list surface has a designed empty state naming its one next
action: a hall with no bookings in the window, an event with no
exhibitors yet, a plan with no objects, an accreditation list awaiting
evidence, an entrance with no scans, a safety board with no incidents,
and a calendar filtered to nothing. An empty state that renders nothing
is treated as an unfinished screen.

Cross-cutting: money and occupancy are integers; timestamps absolute and
rendered in the venue's zone with explicit handling of the twice-yearly
clock change during overnight build-up; one event stream drives the
campus calendar, the planner, access control and the safety board so
every surface converges within a second; overlap, capacity, accreditation
validity and publication scope are enforced in the store, never only in
application code; personal data of visitors and contractors is
encrypted at rest, minimised, and cleared on the retention schedule the
privacy policy promises; the audit trail is append-only in the store, not
by convention.

> **In plain language.** Underneath sit a few strict ledgers: which
> square metres are held and by whom, who may come in and until when,
> how many people are inside, and what everything costs. The rules that
> matter, no two events on the same floor, no capacity invented from
> floor area, no rights greater than the person who granted them, live
> in the filing cabinet itself, so no screen and no clever request can
> break them.

## 32. Component architecture and liveness

- One space-availability authority answers every question about whether
  a space is free, used by the enquiry desk, the planner, the public
  calendar, reporting and any integration; a second implementation
  anywhere is a defect.
- One occupancy evaluator serves the safety board, the access decision
  and the public capacity display.
- The floor-plan geometry, the overlap resolver, the accreditation
  evaluator, the tax calculator and the phase-fit calculator are pure
  modules tested against fixture inputs whose expected outputs are
  grader-held.
- One event stream (server push with a one-second polling fallback)
  carries holds, phase changes, plan revisions, scans, occupancy and
  incidents; entrances additionally hold a local cache per Section 20.
- The public site consumes only the published projection of Section 24,
  through one authority, and the interactive floor plan renders from the
  same space model the planner uses.

> **In plain language.** There is exactly one thing in the system that
> knows whether a hall is free, and everything else asks it. There is
> exactly one thing that knows how many people are inside. The map on
> the public website and the map the planners draw on are the same
> shapes from the same source, so the website can never show a hall the
> building does not have.

## 33. Responsive behaviour

- Public pages reflow to 390px across all three languages, with the
  longest language deciding the layout: navigation labels, chips and
  buttons must not wrap or truncate in the language with the longest
  strings, and the build is checked in that language rather than in
  English.
- The floor plan on a phone becomes a pannable, pinch-zoomable region
  list with the same keyboard and screen-reader semantics, and each
  hall's specification is reachable without the plan.
- Calendar filters collapse into a sheet; event cards stack keeping the
  status chip, dates and hall chips visible.
- The operations console is desktop-first, but three surfaces must work
  on a phone because they are used on the floor: access control, the
  safety board and incident raising. Those three are specified for
  gloved, one-handed use with large targets and high contrast.

> **In plain language.** The public site folds down to a phone in three
> languages, and the layout is checked against the wordiest language
> rather than the shortest, which is the usual way multilingual sites
> break. The map becomes something you can pinch and pan. And three
> parts of the staff system, the door, the safety board and reporting an
> incident, are designed to be used one-handed while walking.

## 34. Accessibility

- Motion is gated positively per Section 6, so a still page is the
  default; the hero cue, reveals and carousels all respect it.
- The floor plan is fully operable without a pointer: regions are
  focusable in a stated order, each announces its hall, capacity and
  area, and selecting one moves focus to that hall's specification.
- The three languages each carry a correct document language, and the
  switcher announces itself; a page available in another language only
  is labelled per Section 12.
- Event cards never rely on colour: status is a labelled chip, and hall
  chips carry names.
- Forms label every field, tie errors to their inputs, and never rely on
  placeholder text as a label; the enquiry form states what happens
  next.
- Operational surfaces used on the floor meet contrast and target-size
  requirements under bright light, and the safety board's alerts are
  announced as well as coloured.

> **In plain language.** Stillness is the default, not an option. The map
> can be driven entirely from the keyboard, and each hall says its own
> name, size and capacity out loud. Every colour that means something,
> an event being open to the public, a hall approaching its limit, also
> says it in words.

## 35. Performance

- Public pages: the calendar renders a year of events with filters
  applied in under a second from indexed, paginated queries; images are
  served in modern formats at the sizes actually displayed; the floor
  plan is inline geometry and adds no image weight.
- The planner holds frame rate at eight hundred objects per Section 18,
  with incremental validation.
- Access decisions return within a bounded time at the door, including
  the degraded path of Section 20, because a queue at an entrance is a
  safety problem, not a latency problem.
- Occupancy recomputes per scan without a full recount, and the safety
  board updates within a second of a scan.
- The event stream batches bursts per frame; a hall opening its doors
  produces thousands of scans in minutes and must not degrade the
  console.

> **In plain language.** The public calendar is quick even with a year of
> events in it. The plan stays smooth with hundreds of stands. Most
> importantly, the door decides fast even when the network is poor,
> because a slow door is a crowd on the pavement, and the safety board
> knows the new number within a second of each person walking in.

## 36. Security, privacy and abuse

Difficulty: hard.

- Event isolation: one organiser can never see another's plan, orders,
  exhibitor list or rates, including through search, exports, the
  exhibitor portal and any integration; a forged cross-event read
  returns not-found without leaking existence.
- Personal data minimisation: contractor identity documents and visitor
  data are collected only where the law or the safety regime requires,
  retained on a stated schedule, and cleared automatically; the privacy
  policy's promises bind the implementation.
- Badge integrity: badges are signed and time-bound, cannot be
  transferred between people, and a cloned badge is detected by the
  anti-passback rule of Section 20 and raised to security.
- The audit trail is append-only in the store and covers accreditation
  grants and revocations, capacity changes, plan approvals, publication
  changes, access-rule changes, invoice adjustments and evacuation
  declarations, with actor, time and before-and-after values.
- Standard hardening: state-changing requests protected against
  cross-site forgery, no state change on a GET, session cookies
  http-only and same-site, secrets never returned by any read path, and
  uploads validated server-side and served through signed short-lived
  links.

> **In plain language.** Two events running in neighbouring halls must
> not be able to see each other's plans, suppliers or prices. Documents
> collected for safety are kept only as long as the law requires and
> then deleted by the system rather than by somebody remembering.
> Badges cannot be lent or copied without security hearing about it. And
> every consequential act is written in a book that cannot be edited,
> because a venue with a safety charter has to be able to prove what
> happened.
## 37. Build order and difficulty map

Build order, each stage demonstrable: tokens, chrome, three languages
and the reveal grammar (3 to 6); home, calendar and the visit section (7,
8, 11); the space model and the interactive floor plan together, because
the public plan is the model made visible (15, 9); the remaining
organiser, about, news and legal routes (10, 12, 13); the operations
shell and the enquiry-to-contract path (14, 16); the event timeline and
resources (17); the floor-plan planner (18); accreditation (19); access
control and occupancy together (20, 21); services, invoicing and the
exhibitor portal (22, 23, 25); publishing (24); works scheduling,
reporting and integrations (26, 27, 28); wayfinding and the annual
campus plan (29, 30); hardening (33 to 36) against Section 41.

| Area | Grade |
|---|---|
| public fidelity, chrome, three languages (3 to 7, 11 to 13) | medium |
| language switcher preserving page and parameters (5) | hard |
| the interactive floor plan from the space model (4, 9) | hard |
| calendar filters, shareable state, multi-day events (8) | hard |
| the space model: combinations, overlap, circulation (15) | expert |
| licensed capacity per space and combination (15) | expert |
| options, ranks, challenge, atomic confirmation (16) | expert |
| phases occupying space, turnaround refusal, cascades (17) | expert |
| shared docks, lifts and crews on one timeline (17, 26) | hard |
| the planner: live constraint validation at scale (18) | expert |
| concurrent planners merging without lost work (18) | expert |
| accreditation with evidence expiry and cascade revocation (19) | expert |
| entrance modes per event and phase (20) | hard |
| offline entrance tolerance and reconciliation (20) | expert |
| occupancy as a graph, no double counting (21) | expert |
| exits binding licensed capacity to the approved plan (21) | expert |
| evacuation overriding all other state (21) | hard |
| services with cut-offs and plan dependencies (22) | hard |
| invoicing, tax rounding, estimate-to-actual variance (23) | hard |
| publication scope structurally separated from internals (24) | expert |
| exhibitor portal scoped to its own stand (25) | hard |
| event isolation, badge integrity, retention (36) | hard |
| offline visitor wayfinding with live invalidation (29) | expert |
| written directions and step-free routes as first class (29) | hard |
| annual plan: recurring holds, yield, atomic scenarios (30) | expert |
| maintenance occupying space like an event (30) | hard |
| versioned licence figures with history at its own version (31) | hard |

Side balance: the expert tier is split across both halves on purpose.
Backend machinery (the space graph and its overlap rule, licensed
capacity, option ranks and atomic confirmation, phase occupancy,
accreditation cascade, offline access reconciliation, occupancy without
double counting, publication scope, annual scenario commits) and
frontend machinery (the interactive floor plan driven by the model, the
planner's live constraint validation at eight hundred objects,
concurrent planners merging per object, offline visitor wayfinding with
live invalidation, the three-language layout and the on-floor safety
surfaces) each carry expert or heavy hard weight, so a delivery strong on
one side alone cannot clear the exam.

Adversarial notes: the seeds, race scripts, traffic patterns, offline
scripts, plan fixtures and expected figures referenced throughout are
grader-held and are not part of the delivery. A build that hard-codes
expected figures, derives capacity from floor area, checks availability
only at the level booked, sums a combination's capacity from its
children, treats build-up and tear-down as annotations rather than
occupancy, counts occupancy per door, admits nobody or everybody when an
entrance goes offline, leaves revocation to a nightly job, publishes
by filtering internal fields at render time, requires the network to
draw the visitor map, applies a scenario partially, or retro-fits
historical capacity to a revised licence figure will pass its own retries and
still fail the held materials.

Calibration intent: the mediums should land cleanly, most hards should
land with effort, and the experts are the exam; roughly a fifth to a
third of the graded surface is expected to fall short on a first
delivery and be caught by Section 41.

> **In plain language.** Build the website first, then the model of the
> building, because the public map is that model made visible. Then the
> selling, the diary with its build and tear-down days, the plan, the
> passes, the doors and the safety board, and the money last. The
> ranking is honest: the handsome public pages are the easy third. The
> exam is the building itself, halls that fit inside one another, limits
> that come from exits rather than floor area, and a door that has to
> keep deciding correctly when the network drops.

## 38. Copy deck

Literal copy with the Section 0 substitutions. Capacities, areas,
parking figures, hall characteristics, dates and the case studies are
kept exactly as measured; the venue, the city, the parent group, the
acquiring group, the restaurant brand, the charter and the named client
are substituted. All copy exists in three languages; the Dutch capture is
the source of record and the English capture corroborates it.

### 36.1 Chrome

- Utility strip: Jobs · <GROUP> · nl · fr · en
- Main navigation: Calendar · Visit (Accessibility & parking, Food &
  drinks, What to do in <CITY>, Frequently Asked Questions) · Organize
  (Spaces, Meetings, Catering, The <RESTAURANT>, Accessibility & region,
  Unique events) · About <BRAND> (Who are we?, History, Sustainability &
  safety, Media kit & documents) · News · Contact
- Search: "Search entire website"
- Footer: "(C) 2026 <BRAND>" · General terms & conditions · Safety
  manual · Privacy policy · Cookie Policy · "Subscribe to the
  newsletter" · Instagram, LinkedIn, Facebook
- Not-found: the measured 404 screen

### 36.2 Home

- Hero: "when ideas need space" / "View our calendar" / "Organize your
  event"
- Upcoming: "Coming soon to <BRAND>" / "All events"; the measured event
  fixtures with their status chips ("Open to the public", "Trade fair -
  registration required"), dates, times, hall chips and sectors
  ("Lifestyle & Sports", "Sustainability")
- Visitor band: "Are you visiting <BRAND> soon?" / "Great, we look
  forward to welcoming you! Click through for all practical information
  on parking, accessibility, accommodation and answers to frequently
  asked questions. That way, you don't have to worry about anything and
  can make the most of your visit." / "Plan your visit"
- Organiser band: "Your next event at <BRAND>?" / "<BRAND> is a
  versatile event venue in <REGION> to host conferences, corporate
  events, trade shows, meetings and other events." / "A unique idea
  deserves the right location. We don't just rent out our event halls.
  We are happy to think along with you and explore the possibilities
  together. This way, we create the ideal setting for your trade fair,
  conference, event or meeting. Thanks to our modern facilities and 50
  years of experience, we bring your big or small plans to life down to
  the finest details. Our team takes care of everything from A to Z,
  whether it's catering, ticketing, parking, technical support or
  safety."
- Setting band: "when ideas need space" / "The right setting for every
  concept" / "From an intimate reception to a large-scale corporate
  event. From a niche trade fair to a well-attended public event. From a
  strategic meeting to an inspiring conference... Our venue is a blank
  canvas of nearly 40,000 m² where (almost) anything is possible, as
  long as you dare to dream." / "Organize in <BRAND>" / "Discover the
  halls"
- The four blocks, verbatim: "6 halls: versatility at its best" with its
  paragraph; "Meeting center: 5 rooms, endless possibilities" with its
  paragraph; "<BOULEVARD>: covered boulevard" with the paragraph about
  connecting all the halls, being the beating heart, its two entrances
  and its use as additional exhibition space or catering area; "The
  <RESTAURANT>: Fast Gourmet Kitchen" with the self-service and bistro
  paragraph
- Inspiration: "Get inspired" / "Get inspired by a selection of events
  recently held at <BRAND>." / "More unique events"
- Newsletter: "Stay up to date" with its paragraph and "Subscribe to the
  newsletter" / "Follow us"
- News: "Xpo Newsflash" / "Curious about our latest news? We take you
  behind the scenes at <BRAND>." / "All newsflashes"

### 36.3 Spaces

"Flexible halls and rooms" with the paragraph about a versatile offer of
halls, party and meeting rooms that can be arranged entirely to the
client's wishes; "View the floor plan" / "Start your request" / "Get
inspired"; the floor plan with regions 1 to 6 and XXL; then the
specification blocks of Section 9 verbatim, each with Capacity, Surface
area, Unique features and Suitable for; then "Flexible combinations
tailored to you" with its paragraph; "Say hi to the Venue team" with the
proactive-support paragraph and "Contact us"; "Why do organizers choose
<BRAND>?" with its six reasons (In-house experience, Flexible spaces
with "6 flexible halls and 5 modular meeting rooms", Bespoke catering,
Easily accessible as a congestion-free location, Ample parking with
"2,500 parking spaces", End-to-end care); "The spaces in use" with the
case strip.

### 36.4 Case studies, verbatim

- The architecture trade event: "an exclusive, high-end trade event
  aimed at (interior) architects, engineers and specifiers, with a
  strong focus on product innovations. They make use of Hall 4, Hall 5,
  and the convenient passage between them, the Transit."
- The interior-sector corporate event: "Hall 3 was transformed by event
  agency <AGENCY> into a stunning and unique corporate event. More than
  900 guests enjoyed live performances and acts while savoring a walking
  dinner provided by our in-house catering. Mobile catering points were
  installed throughout the hall. The spacious South entrance was used
  for access control."
- The book fair: "<FAIR> has now been held in <BRAND> for 5 editions!
  They use Halls 1, 2, 3 and 6 for the fair and the children's play
  area. The MC rooms and the XXL serve as the setting for book signings,
  presentations and interviews. Visitors can easily find their way
  thanks to the direct connection between all the spaces used."

### 36.5 News fixtures

- Corporate: "<ACQUIRER> completes acquisition of <GROUP>" dated
  03.08.2026 with the line about the deal creating opportunities for
  expansion and continued growth among specialist event communities,
  leveraging complementary capabilities.
- Sustainability: "<BRAND> achieves <CHARTER> for the 10th consecutive
  year" dated 07.07.2026, with its paragraph about recognition for
  companies integrating sustainable enterprise into daily operations
  through concrete actions and objectives. This fixture is deliberately
  reproduced with its original-language body under an English heading,
  because the reference site publishes it that way and Section 12's
  translation-state rule exists to handle exactly this.

> **In plain language.** Every visible sentence is collected here in
> three languages: the four-word promise, the invitations to visitors
> and organisers, the four blocks describing the building, every hall
> with its real capacity and floor area, the three case studies naming
> which halls they used, and the two news items. The building's numbers
> are exactly as measured; the names of the venue, the city, the group
> and the clients are invented stand-ins.

## 39. Zero-asset substitution guide

No binary ships. Proposed values not measured sit inside allow markers.

- The floor plan is inline vector geometry drawn per Section 4 from the
  space model, never an exported image.
- Photography (hero, galleries, hall images, case studies, news, team):
  seeded procedural compositions per subject, layered gradient fields in
  the brand palette with a soft scrim and the measured card treatment,
  each carrying its caption and alternative text; the gallery lightbox
  shows the same generated art at a larger size.
- The wordmark, the charter mark and the social glyphs are drawn per
  Section 4; the icon font is replaced by a drawn stroke set.
- Downloadable documents in the media kit (logo pack, floor plans,
  safety manual, technical specification) are generated at build time
  from the space model and the specification itself, so the plan a
  contractor downloads is the plan the planner uses.
- Fonts: the variable sans from a hosted service with the measured
  system fallback stack.

Reference asset manifest, the binaries this guide replaces:

<!-- lint:allow P4,P6 -->
| Class | Representative files | Substitute |
|---|---|---|
| venue photography | hero, gallery, hall and case-study images | seeded procedural compositions |
| news and team imagery | article and portrait images | seeded compositions and drawn monograms |
| brand marks | wordmark, charter mark, social glyphs | drawn geometry |
| icon font | the interface glyph font | drawn stroke set |
| documents | logo pack, floor plans, safety manual | generated from the model at build time |
<!-- lint:end -->

> **In plain language.** Nothing in the build is a downloaded picture.
> The map is drawn from the same data the staff book halls with. The
> photographs become warm colour fields with their captions intact. And
> the floor plan a contractor downloads is generated from the real
> model, so it can never be an out-of-date copy.

## 40. Evidence gaps and substitutions

1. The operations platform does not exist publicly; Sections 14 to 30
   and 36 are authored from what the site states about the building and
   its operation: the hall inventory with capacities and areas, the
   combination promise, the covered boulevard's dual role, the passage
   between two halls named in a case study, the entrance used for access
   control in another, the 2,500 parking spaces, the in-house catering,
   the fifty years of operation, the sustainability and safety charter
   held ten consecutive years, and the published safety manual. The
   difficulty grades are part of the specification's intent.
2. The route crawl spent slots on the three language roots and a consent
   endpoint; the sustainability and safety page, the media kit page and
   the organiser accessibility page were missed by the cap and captured
   in a supplemental pass with the kit's own functions, together with
   the English spaces page for cross-language corroboration, before the
   ledger was finalised.
3. No video assets exist on the site.
4. The captured copy deck is dominated by the consent platform's own
   dialog text, which is third-party interface copy rather than the
   venue's; the venue's page copy was read from the probe records
   directly and is what Section 38 transcribes. The consent dialog is
   specified behaviourally in Section 5 rather than reproduced verbatim.
5. Brand substitutions, one to one: the venue, the city, the region, the
   parent group, the acquiring group, the restaurant brand, the
   sustainability charter, the named event agency, the named book fair
   and the individual events in the calendar fixtures. Hall numbers,
   capacities, areas, the parking figure, the 40,000 square metre total,
   the fifty-year history and the ten-year charter run are measured and
   kept.
6. A supplementary English extraction of the site provided during
   authoring corroborated the navigation, the four building blocks and
   the case studies; no specification rests on it alone.
7. The meeting centre is described as five rooms on the home page and as
   four MC rooms beside the event hall on the spaces page. Both are
   reproduced as measured, and Section 15's model resolves the
   difference by treating the event hall as a fifth combinable room of
   the meeting centre, which is what the case study describing the MC
   rooms and the XXL used together implies. This is recorded because it
   is an inference, not a measurement.
8. Hall 4's suitability line was not captured, while every other hall's
   was; the specification carries the measured fields and marks that one
   as not captured rather than inventing it.
9. Prices, contract terms, staffing levels and the real booking system
   are commercially confidential and absent from the capture; the
   platform's rates and lead times are the build's own fixtures, and the
   acceptance checklist grades internal consistency rather than fidelity
   to the venue's real commercial terms.

> **In plain language.** Honesty corner. The staff system was never
> visible, so everything about it here is designed from what the site
> says about the building, and the site says a great deal: how big each
> hall is, how many people it holds, which halls a particular fair used,
> and which door was used for access control. Three pages the crawler
> missed were fetched with the same tools and folded in. The site
> contradicts itself once about whether the meeting centre has four
> rooms or five, and rather than choosing silently, this document says
> so and explains its reading.

## 41. Acceptance checklist

The grading materials behind these lines, seeds, race scripts, traffic
patterns, offline scripts, plan fixtures and expected figures, are
grader-held and absent from the delivered repository: results must be
derived from this specification alone, on any attempt, and a delivery
that hard-codes expected outputs fails.

Medium:

- [ ] Every public route matches the capture at the three widths in all
      three languages: tokens, the single easing, band order, chrome,
      footer, not-found, and stillness by default under the positive
      motion gate.
- [ ] The copy deck appears verbatim, including every hall's capacity,
      area, character and suitability, the four building blocks, the
      three case studies and the parking figure.
- [ ] The operations shell, roles and campus calendar work end to end,
      with forged requests from insufficient roles refused server-side.
- [ ] Reporting figures derive from the ledgers and agree across axes;
      every list surface has a designed empty state naming its next
      action.
- [ ] A licence figure revised after an inspection applies to future
      bookings only; last year's approved plans and occupancy records
      still read at the version they were written under.

Hard:

- [ ] The language switcher preserves the page and its parameters in all
      three languages; a page available in one language only is labelled
      rather than omitted; the longest language does not break any
      layout.
- [ ] The public floor plan renders from the space model, is keyboard
      operable region by region, announces each hall's name, capacity and
      area, and a space added in operations appears without redrawing.
- [ ] Calendar filters are shareable through the address, multi-day
      events render once with their range, and an event past midnight
      belongs to the day it started.
- [ ] Entrance modes vary per event and per phase; services enforce
      cut-offs, surcharges and plan dependencies; invoices reconcile
      estimates to actuals with attributable variance and lines summing
      exactly.
- [ ] The exhibitor portal is scoped to its own stand, and a forged
      request for another exhibitor's orders or position returns
      not-found; event isolation holds across search, exports and
      integrations.
- [ ] Evacuation opens every entrance as an exit, suspends admission,
      freezes the log, and nothing in the system can prevent an exit.

Expert:

- [ ] Space battery: holding a combination blocks every constituent and
      every ancestor; holding any constituent blocks the combination;
      one authority answers availability for the desk, the planner, the
      public calendar and reporting identically; capacity is the stored
      licensed figure per space, per layout and per combination and is
      never derived from area nor summed from children; hiring the
      boulevard is refused when the remaining public route would fail
      the occupancy rules.
- [ ] Sales battery: ranked options coexist on the same space and dates;
      a challenge runs its window and resolves automatically on expiry;
      confirming creates spaces, phases and contract atomically; two
      confirmations of competing options in the same instant produce
      exactly one booking and one refusal.
- [ ] Timeline battery: build-up and tear-down occupy space exactly as
      the run does; a tight turnaround is refused with the shortfall
      named in hours; extending a run cascades into the next booking as
      a raised conflict rather than an overwrite; docks, lifts and crews
      are contended and resolved on the same timeline.
- [ ] Planner battery: eight hundred objects pan and zoom at frame rate
      with incremental validation; a stand blocking an exit, encroaching
      an aisle, sitting on a column or exceeding a rigging load is
      flagged on placement with the rule named and the measurement
      shown; two planners merge per object with no lost work and no
      object moved out from under a dragging hand.
- [ ] Accreditation battery: an expiring certificate withdraws its
      accreditation and its badges at the moment of expiry, not at a
      nightly job; delegated rights never exceed the granter's;
      revoking an organiser cascades to every exhibitor and contractor
      accredited beneath it within a second.
- [ ] Access and occupancy battery: an entrance that loses its
      connection keeps deciding on a cached rule set within a stated
      staleness bound, queues scans, reconciles on reconnect and
      surfaces admitted-after-revocation events; occupancy is computed
      on the space graph so movement between joined halls never
      double-counts; an approved plan that blocks an exit reduces the
      licensed figure automatically with the reason shown.
- [ ] Wayfinding battery: the visitor map renders fully offline from a
      cache taken on first load, announces the age of a stale cache,
      redraws within a minute of a hall closing or an entrance changing
      mode, never offers a closed route, and provides every route as
      written directions with a step-free layer, in the visitor's own
      language.
- [ ] Annual battery: recurring holds age from provisional to option to
      booking and surface when lost; maintenance occupies space exactly
      as an event does and cannot be booked over; a forked scenario
      commits atomically or fails whole, never partially.
- [ ] Publication battery: nothing reaches the public site before its
      publication date; internal fields are structurally incapable of
      publication rather than filtered at render; unpublishing removes
      an event within a minute; per-language translation states behave
      as specified.

> **In plain language.** The exam, easiest first. The ordinary lines
> check the site is faithful in three languages and the desk works. The
> hard lines poke at the switcher, the map, the exhibitor walls and the
> evacuation. The brutal lines are the building itself: halls that fit
> inside one another and must never be double-sold, a capacity that
> comes from exits rather than floor area, two events that cannot pass
> through the same hall on the same night, a plan that flags a blocked
> fire exit the moment a stand lands on it, a withdrawn organiser whose
> builders lose their badges within the second, and a door that keeps
> deciding correctly when the network goes down.
