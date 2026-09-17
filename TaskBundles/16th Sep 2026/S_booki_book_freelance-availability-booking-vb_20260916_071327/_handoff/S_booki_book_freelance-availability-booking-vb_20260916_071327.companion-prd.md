# <BRAND> buildable product requirements

Zero-asset build specification, authored from the evidence ledger produced by
stages 0 and 1 against a captured reference site. Every colour, easing curve,
duration, radius and icon coordinate below was measured. Nothing was recalled.
Every section also carries a plain-language block, marked **In plain language.**,
saying the same thing to a reader who will never open a code editor.

This capture is the most complete in the set. The document scrolls, so the
nine-position scroll matrix is real evidence rather than nine samples of one
frame; three routes render distinct documents; and the ledger carries `42`
declared colours, `29` inline drawings and `87` effect values. Where earlier
sections of this document say a value was measured, it was measured at every
breakpoint.

**Sections 16 to 28 and Section 34 are an extension.** The reference has a live
availability signal and a six-step enquiry form, and nothing behind either. Those
sections specify the booking and account layer, each marked **[extension]** in
its heading and traced in Section 37.3 to the measured surface it was derived
from.

---

## 0. How to use this document

### 0.1 What this is

A specification complete enough to rebuild the site and its booking layer
without receiving a single binary file. No image, video, three-dimensional
model, audio file or font file ships with it. Section 36 gives a procedural
recipe for every asset class the reference used.

This file has two readers and carries a register for each. The specification is
written for the agent building the site. The blockquote that closes every
section is written for the person who commissioned the build, in terms that can
be checked against a live page rather than against the ledger.

### 0.2 Normative versus informational

- **Capability requirement - normative.** What the build must do, stated without
  naming a library.
- **Observed implementation - informational.** What the captured reference used,
  with the ledger tier that established it. Evidence, never instruction.

Where a block carries no label, it is normative.

### 0.3 Measured versus extended

- **Measured.** Parsed from the capture by a program. Reproduce it exactly.
- **[extension].** Required by the brief, not observed. Colour, type, spacing,
  motion and marks in an extension come from Sections 3, 4 and 6 and from
  nowhere else, and may not introduce a value that is not already here.

### 0.4 The palette warning

The ledger's runtime-palette list carries `69` hexadecimal values, of which
roughly forty are an alphabetical run of standard colour names shipped inside a
library lookup table: a pale blue, an antique white, an azure, a beige, a
crimson, a gold and so on, in alphabetical order from `a` to `l`. They are a
dependency's data, not a design decision, and none of them appears anywhere on
screen.

Section 3.2 lists the palette this build uses. Anything not in that table is not
a colour of this site, however many times it appears in the ledger.

### 0.5 Placeholder tokens

Angle-bracket names are blanks. Replace every occurrence before shipping.

| Token | Meaning | Literal placeholder used in copy |
|---|---|---|
| `<BRAND>` | the person and the site | `Elian Moreau`, 12 characters, matching the reference exactly |
| `<GIVEN_NAME>` | the first line of the lockup | `Elian`, 5 characters |
| `<FAMILY_NAME>` | the second line of the lockup | `Moreau`, 6 characters |
| `<SITE_ORIGIN>` | public origin | none |
| `<APP_HOST>` | origin the booking layer is served from | none |
| `<CONTENT_API>` | the content service the work index reads from | none |
| `<AUTH_ISSUER>` | account service | none |
| `<MAIL_SENDER>` | address transactional mail is sent from | none |
| `<CONTACT_EMAIL>` | the public enquiry address | none |
| `<SOCIAL_ONE>`, `<SOCIAL_TWO>`, `<SOCIAL_THREE>` | the three social links | `Linkedin`, `Postline`, `Showcase` |
| `<AWARD_ONE>`, `<AWARD_TWO>` | the two award badges | none |
| `<PROJECT_ONE>` to `<PROJECT_NINE>` | the nine work entries | Section 35.7 |

**Class names are scrubbed too.** The reference ships hashed module class names
that carry no brand token, so they are safe, but the two award badge element
identifiers name their awarding bodies and are replaced. Where a measured
selector is quoted, any brand-derived part is replaced and noted.

### 0.6 Reading the numbers

Numbers are quoted as measured. The rendered type scale is fractional,
`14.4px`, `17.6px`, `19.2px`, `28.8px`, `49.5px`, `97.5px`, because sizing is
derived from a root scale under a utility layer (Section 3.5). Reproducing the
derivation reproduces the fractions.

### 0.7 What could not be measured

Section 37 lists the evidence gaps. Anything marked **inferred** is a
reconstruction from screenshots rather than a measurement.

> **In plain language.** This build is described twice over, section by section:
> once exactly, for the machine that will build it, and once like this, for you.
> The two carry the same section numbers.
>
> **This capture went well.** Unlike some sites, this one scrolls normally, so
> our tool could walk down the whole page taking measurements at nine positions
> on every screen size. Almost everything in this document is measured rather
> than guessed, and the places where it is not are listed at the end.
>
> **One warning about colour.** Our measuring program found sixty-nine colours in
> the code, but about forty of them are a list of standard colour names that
> comes bundled inside a library the site uses: things like beige, crimson and
> gold, in alphabetical order. None of them is on the screen. The real palette is
> a much shorter list and it is in Section 3.
>
> **You are also commissioning the half the reference only hints at.** It says
> "available now for work" and has a form to fill in, and nothing behind either.
> The booking system, the accounts and the project pipeline are additions, each
> one marked, each built only from parts measured elsewhere on the site.

---

## 1. Product overview

### 1.1 What the product is

The portfolio and enquiry desk of a freelance creative developer, and the
booking layer behind it. The site's job is to establish craft, show nine
projects, state availability, and convert a visitor into a scoped enquiry.

The extension turns that enquiry into a booking: an open project window, a
scoped brief against it, a proposal, and a confirmed start date.

### 1.2 Audiences

| Audience | What they came for | Where they land |
|---|---|---|
| A founder with a product to build | proof of craft, and whether he is free | Section 9, Section 5.3 |
| A product lead at a studio | the work, and what he actually does | Section 11, Section 10.4 |
| A recruiter or client comparing | services, experience, awards | Section 10 |
| A returning client **[extension]** | their brief and its state | Section 18 |

### 1.3 The measured proposition

Four statements, all measured, in the order the document presents them:

| Where | Copy |
|---|---|
| the hero eyebrow | `Creative Developer` |
| the hero, at display size | `<GIVEN_NAME> <FAMILY_NAME>` |
| under it | `Located in France` |
| the about section, revealed word by word | `An award-winning, product-minded frontend engineer with a background in aerospace engineering and human factors. I design and build visually striking web and mobile products where usability, reliability and performance matter, from concept to launch, with a strong focus on thoughtful UX, engaging interactions and practical AI-powered workflows.` |

The fourth is the whole positioning statement and the longest measured string in
the capture. The aerospace background is the differentiator and is stated in the
first sentence.

### 1.4 What makes it expensive to build

1. **Two grounds, hard cut.** A near-black hero and a lavender work section,
   meeting at a hard edge with a rounded top, measured as a `20px` corner pair
   (Section 3.7).
2. **Outlined display type.** The condensed display face rendered as an outline
   rather than a fill, measured on the hero eyebrow and both section titles
   (Section 3.4).
3. **Word-level shadow reveal.** Every word of the about statement exists twice,
   once as a shadow copy at `0.15` opacity, measured on `138` elements
   (Section 6.4).
4. **A scroll-scrubbed document.** Fourteen selectors change under scroll on the
   home document alone, including a card stack, a clip path and the header's own
   backdrop blur (Section 7.3).
5. **Sound.** Twenty-one audio files and a measured `Sound | OFF` control
   (Section 14).

### 1.5 Success criteria

- A visitor can tell within one frame what he does, where he is, and whether he
  is available.
- Every one of the nine projects is reachable in one interaction from `/work`.
- A visitor can submit a scoped enquiry without an account.
- A visitor can pick an open project window and hold it **[extension]**.
- The document holds its frame budget with the render layer running
  (Section 32).

> **In plain language.** This is the personal site of a freelance developer who
> builds unusually good-looking web and mobile products, and who came to it from
> aerospace engineering, which is the thing that makes him different and which
> the site says in its first sentence.
>
> It has to do three jobs: prove he can do the work, show the work, and make it
> easy to ask him about a project. There is a green badge at the top that says he
> is available, which is the single most commercially important element on the
> page.
>
> Five things make it expensive to build. The page switches between a near-black
> top and a soft lavender middle with a hard, rounded edge between them. The big
> display lettering is drawn as an outline rather than filled in. Every word of
> the paragraph about him exists twice, once as a faint shadow, so the words
> appear to lift off the page as you scroll. Fourteen separate things on the home
> page move in response to your scrolling. And the site has sound, with a control
> to turn it off.

---

## 2. Information architecture

### 2.1 What the capture found

Twelve paths, of which three are real.

| Path | What it is | In this build |
|---|---|---|
| `/` | the home document, `5042px` at desktop | Sections 9 to 11 |
| `/work` | the work index, a distinct document | Section 12 |
| `/contact` | the enquiry document, a distinct document | Section 13 |
| `/work/` | the same document as `/work` | one canonical form, Section 2.4 |
| `/gtag/js`, `/g/collect`, `/mc/collect` | the analytics vendor's endpoints, scraped from its bundle | excluded, Section 37.1 |
| `/as`, `/as/d`, `/gs`, `/g/d` | catch-all fragments serving the home document | excluded, Section 37.1 |
| `/wp-content` | returns `403: Forbidden`, measured | excluded, and Section 37.6 |

### 2.2 The route set this build ships

| Path | Section | Access |
|---|---|---|
| `/` | Sections 9 to 11 | public |
| `/work` | Section 12 | public |
| `/work/<slug>` | Section 12.5 | public |
| `/contact` | Section 13 | public |
| `/availability` | Section 15 | public **[extension]** |
| `/enquiry/<id>` | Section 18 | enquiry token, or owner **[extension]** |
| `/signin`, `/reset` | Section 16 | public **[extension]** |
| `/account` | Section 16 | client **[extension]** |
| `/studio`, `/studio/pipeline` | Section 17 | studio role **[extension]** |
| `/legal/privacy` | Section 15.5 | public |

The home document carries an `#about` anchor, measured as an element identifier
with its own rounded top corners (Section 3.7). Anchors resolve to scroll
positions and must survive a cold load.

### 2.3 The measured chrome

Present on all three real routes at every breakpoint.

| Slot | Content | Notes |
|---|---|---|
| left | the name lockup, two lines, with two small key glyphs | Section 5.2 |
| centre | the availability pill, `available now for work` with a dot | Section 5.3 |
| right | `Sound | OFF` | Section 14 |
| right | four links, `Home`, `About`, `Work`, `Contact`, or a burger | Section 5.4 |

Measured: the header carries a scroll-driven `backdrop-filter`, taking two
values, `blur(0px)` and a blurred state. The chrome has no ground of its own
until the document scrolls under it.

### 2.4 Route hygiene

`/work` and `/work/` both resolved. This build serves one canonical form,
without the trailing slash, and redirects the other permanently. Two addresses
for one document splits analytics and search ranking, and it is free to fix.

### 2.5 The persistent rail

Measured on every route at desktop: a fixed rail at the left edge carrying two
award badges and a vertical `Honors` label, at `x = 0` to `53` and
`y = 337` to `562`. It is `171px` tall in its own drawing and rotated to read
bottom-to-top.

It never scrolls and is present on all three routes. It is the only element in
the document that is neither chrome nor content.

> **In plain language.** There are only three real pages: the home page, the work
> list, and the contact page. The other nine addresses our tool found are either
> the analytics company's own endpoints, which it mistook for links, or the same
> home page served under another name.
>
> Along the top of every page: his name at the left, a green badge in the middle
> saying he is available for work, a control to turn the sound off, and the
> navigation at the right. The header has no background of its own until you
> start scrolling, at which point what is behind it blurs.
>
> Down the left edge, fixed in place and never scrolling, there is a narrow strip
> with two award badges and the word Honors reading bottom to top. It is on every
> page and it is neither part of the header nor part of the page content, which
> is unusual and worth keeping.
>
> One small free win: the work list answers on two slightly different addresses.
> We serve one and redirect the other, because two addresses for one page splits
> your search ranking for no benefit.

---

## 3. Design system

### 3.1 The ground rule

Two grounds, alternating down the document: a near-black for the hero, the
contact surface and the footer, and a pale lavender for the about and work
surfaces. One accent, a deep purple, which is the ink on lavender and the fill
on every solid control. One signal colour, a green, which means one thing only:
he is available.

A build that uses the green for anything but availability has broken the system.

### 3.2 Colour tokens

Declared values with their stylesheet counts, and the computed count where the
same value was measured on rendered elements.

| Token | Value | Declared | Computed | Role |
|---|---|---|---|---|
| `--c-paper` | `#ffffff` | 32 | 721 | text on the dark ground, and solid pills on lavender |
| `--c-text` | `#e5e7eb` | 2 | 6553 | the inherited body colour, the most-rendered value in the document |
| `--c-mist` | `#f0f1fa` | 16 | 1506 | the palest surface, cards and panels |
| `--c-lavender` | `#e7d8ff` | 3 | 1143 | the work and about ground |
| `--c-ink` | `#141516` | 10 | 668 | the dark ground |
| `--c-purple` | `#321469` | 13 | 213 | ink on lavender, and the solid control fill |
| `--c-green` | `#219653` | 1 | 30 | availability, and nothing else |
| `--c-black` | `#000000` | 8 | high | the outer stop of the hero gradient |
| `--c-violet` | `#8d54ff` | 1 | not computed | the accent stop, Section 8.3 |
| `--c-violet-bright` | `#ac4bff` | 1 | not computed | the second accent stop |
| `--c-grey` | `#6c6c6c` | 2 | not computed | disabled and placeholder text on dark |
| `--c-grey-cool` | `#9ba2af` | 2 | not computed | secondary text on dark |
| `--c-near-black` | `#0a0a0a` | 1 | high | the footer ground |
| `--c-panel` | `#18181b` | 1 | not computed | form field grounds on dark |

Measured alpha forms, to be reproduced as declared and never re-derived:

| Value | Declared | Use |
|---|---|---|
| `#ffffff26` | 2 | hairline borders on the dark ground |
| `#ffffffe6` | 1 | text at rest over the render layer |
| `#1415164d` | 1 | the scrim under the chrome |
| `#8b5cf640` | 2 | the hero's violet halo, Section 8.3 |
| `#3214691f` | 1 | the lightest purple wash on lavender |
| `#32146938` | 1 | the purple rule on lavender |
| `#210d463f` | 1 | the card shadow's own tint |
| `#10032a33` | 1 | the deepest purple wash |
| `#7631f58c` | 1 | the selection and focus tint |
| `#00000099`, `#000000bf`, `#00000040` | 1 each | three scrim strengths on media |

Also measured as computed values: `rgba(33, 150, 83, 0.3)` on `30` elements,
the availability dot's halo, and `rgba(20, 21, 22, 0.6)` on `27`, the header
scrim.

### 3.3 What is not in the palette

Section 0.4. The ledger's runtime list carries roughly forty standard colour
names from a library's lookup table. None renders. A reviewer checking this
document against the ledger will find `#dc143c` and `#ffd700` there and not
here, and that is correct.

Two further declared values are a utility layer's defaults and are not design
decisions: `#f3f4f6` and `#222222`, each declared once in the same stylesheet as
the reset.

### 3.4 Type families

| Family | Weight | Display | Role |
|---|---|---|---|
| ClashDisplayR | 400 | swap | the working face, all body and interface text |
| ClashDisplayB | 700 | swap | headings and emphasis |
| August | 400 | swap | the condensed display face, used only as an outline |

All three are declared with a paired fallback face, measured as `ClashDisplayR
Fallback`, `ClashDisplayB Fallback` and `August Fallback`. That pairing is a
metrics-matched fallback and is the reason the page does not reflow when the
faces arrive. Reproduce it (Section 32.4).

**The display face is used as an outline, not a fill.** Measured on the hero
eyebrow and both section titles: the glyphs are rendered with a stroke and a
transparent fill. That single decision carries most of the site's character, and
filling it produces a different site.

### 3.5 The rendered scale

| Token | Size | Weight | Line-height | Count |
|---|---|---|---|---|
| `.display-xl` | `97.5px` | 400 | `146.25px` | 25 |
| `.display-l` | `96px` | 400 | `96px` | 54 |
| `.display-m` | `80px` | 700 | `120px` | 34 |
| `.display-s` | `72px` | 400 | `72px` | 106 |
| `.display-xs` | `60px` | 400 | `60px` | 27 |
| `.h1` | `49.5px` | 400 | `49.5px` | 106 |
| `.h1-bold` | `48px` | 700 | `72px` | 54 |
| `.h2` | `36px` | 700 | `40px` | 20 |
| `.h3` | `32px` | 400 | `32px` | 106 |
| `.h4` | `28.8px` | 700 | `43.2px` | 18 |
| `.lead` | `24px` | 400 | `36px` | 254 |
| `.lead-tight` | `24px` | 400 | `24px` | 139 |
| `.subhead` | `20px` | 400 | `30px` | 253 |
| `.subhead-tight` | `20px` | 400 | `20px` | 139 |
| `.subhead-bold` | `20px` | 700 | `28px` | 20 |
| `.body-l` | `19.2px` | 400 | `28.8px` | 1543 |
| `.body-m` | `18px` | 400 | `27px` | 247 |
| `.body-m-tight` | `18px` | 400 | `18px` | 139 |
| `.body-m-bold` | `18px` | 700 | `27px` | 30 |
| `.body` | `17.6px` | 400 | `26.4px` | 30 |
| `.base` | `16px` | 400 | `24px` | 2966 |
| `.base-light` | `16px` | 300 | `24px` | 44 |
| `.base-bold` | `16px` | 700 | `24px` | 33 |
| `.caption` | `14.4px` | 400 | `21.6px` | 72 |

The two dominant sizes are `16px` on `24px` at `2966` elements and `19.2px` on
`28.8px` at `1543`. Both are exactly `1.5` line-height, and `19.2` is `16`
scaled by `1.2`. The scale is a `1.2` ratio applied to a `16px` root under a
utility layer, and `14.4`, `17.6`, `28.8`, `49.5` and `97.5` are its other
steps.

The measured `97.5px` on `146.25px` is a `1.5` line-height at display size,
which is unusual and deliberate: the largest type on the site is the most
loosely set, because it is a paragraph rather than a heading (Section 10.3).

### 3.6 The scale tokens as measured

The utility layer's own scale was measured on the root and is the derivation
above, stated in its own terms:

| Token | Value | Line-height |
|---|---|---|
| `--text-base` | `1rem` | `calc(1.5 / 1)` |
| `--text-lg` | `1.125rem` | `calc(1.75 / 1.125)` |
| `--text-xl` | `1.25rem` | `calc(1.75 / 1.25)` |
| `--text-2xl` | `1.5rem` | `calc(2 / 1.5)` |
| `--text-4xl` | `2.25rem` | `calc(2.5 / 2.25)` |
| `--text-5xl` | `3rem` | `1` |
| `--text-6xl` | `3.75rem` | `1` |
| `--text-7xl` | `4.5rem` | `1` |
| `--text-8xl` | `6rem` | `1` |

Everything from `--text-5xl` upward is set solid. That is the rule: display type
is set at `1`, body type at `1.5`, and nothing in between exists.

### 3.7 Radius

| Value | Count | Applied to |
|---|---|---|
| `20px` | 75 | cards, the modal container, the mobile project panel |
| `16px` | 66 | media wells, the availability pill's container |
| `10px` | 54 | the work title and description pills |
| `50px` | 39 | the availability pill and the arrow control |
| `90px` | 30 | an award badge |
| `50%` | 8 | the custom cursor and its label |
| `12px` | 3 | the bento panel |
| `20px 20px 0px 0px` | 4 | the about section, and the mobile contact surface |
| `0px 0px 0px 20px` | 29 | the route label |
| `0px 0px 20px` | 29 | the page body's own bottom corners |
| `20px 0px 0px 20px` | 3 | a left-attached panel |
| `0px 20px 20px 0px` | 3 | a right-attached panel |
| `14.4px`, `9.9px` | 12 each | the image container at two breakpoints |

Two families: `20px` for anything that is a surface, `10px` and `16px` for
anything that sits on one, and `50px` for anything that is a control. The
one-sided pairs are what makes the sections read as sheets sliding over each
other (Section 7.4).

### 3.8 Depth

Measured stacking values: `1` (306), `10` (57), `13` (40), `12` (30), `47` (30),
`48` (29), `49` (29), `6` (16), `0` (9), `-10` (8), `11` (8), `2` (3), `5` (2),
`105` (2).

| Layer | Value | Contents |
|---|---|---|
| render layer | `-10` | Section 8 |
| document | `0` to `6` | sections, cards, media |
| sticky and pinned | `10` to `13` | the fixed rail, pinned cards |
| chrome | `47` to `49` | the header, the availability pill, the burger |
| cursor and modal | `105` | the custom cursor and the project modal |

The `47`, `48`, `49` triplet is three chrome elements one above another and is a
smell: they are one layer with three children. This build declares the chrome at
`47` and orders its children in the document (Section 37.6).

> **In plain language.** Two backgrounds that alternate as you scroll: a
> near-black for the top and the bottom, and a soft lavender in the middle. One
> deep purple that is the writing colour on the lavender and the fill of the
> solid buttons. And one green, which means exactly one thing: he is available
> for work. If the green ever appears on something else, the system is broken.
>
> Three typefaces. One for everything you read, a bold version of it for
> headings, and a tall narrow one used only for the very large lettering. That
> third one is never filled in: it is drawn as an outline, with the background
> showing through the letters, and that single decision carries most of the
> site's personality.
>
> The type sizes are all derived from one number by multiplying repeatedly, which
> is why several of them have decimals. Big lettering is set tight, with lines
> almost touching; ordinary reading text is set loose. There is nothing in
> between, and that gap is deliberate.
>
> Corners are rounded in two ways: whole panels get a generous rounding, and
> things sitting on those panels get a smaller one. Some panels are rounded on
> only two corners, which is what makes the sections look like sheets of paper
> sliding over one another.

---

## 4. Iconography

Twenty-nine inline drawings were captured. They fall into four groups, and only
the first two are the site's own.

### 4.1 The site's own marks

| Mark | viewBox | Rendered | Where |
|---|---|---|---|
| the monogram | `0 0 34 36` | `30px`, and `90px` as an ornament | the name lockup, and a card corner |
| the burger | `0 0 100 100` | `30px` | the chrome at mobile and at narrow desktop |
| the arrow | `0 0 30 30` | `30px` and `50px` | the scroll control, the back-to-top control, the cursor |
| the eight-point star | `0 0 200 200` | `35px` to `48px` | the section titles, as a separator |
| the availability dot | `0 0 20 20` | `30px` | the pill, Section 5.3 |
| the `Honors` rail | `53` by `171` | as measured | Section 2.5 |
| the underline | a two-point path | `484px` by `2px` | Section 6.5 |
| the text arc | a quadratic path | `1008px` wide | Section 4.6 |

### 4.2 The monogram

`viewBox="0 0 34 36"`, four paths. The first is the enclosing form:

`M17 3.96C17 1.77295 15.3256 0 13.26 0H3.74C1.67446 0 0 1.77295 0 3.96V14.1695C0 16.3565 1.67446 18.1294 3.74 18.1294H13.26C15.3256 18.1294 17 19.9024 17 22.0894V32.04C1`

Two overlapping rounded squares of side `17` and corner radius `3.96`, offset by
`17` on both axes, so the mark reads as two keycaps stepped diagonally. The
remaining three paths are the letterforms inside them. At `30px` the two caps
sit beside the name; at `90px` one is used alone as a card ornament.

### 4.3 The burger

`viewBox="0 0 100 100"`, three paths, and it is not three parallel bars:

- `m 70,33 h -40 c 0,0 -8.5,-0.149796 -8.5,8.5 0,8.649796 8.5,8.5 8.5,8.5 h 20 v -20`
- `m 70,50 h -30`
- the third mirrors the first through the centre

The top and bottom strokes curl back on themselves at their left ends, so the
mark is a bar between two hooks. On activation the hooks unwind and the three
strokes cross; the `stroke-dasharray` and `stroke-dashoffset` transition
measured on `90` elements at `0.4s` is what draws them (Section 6.6).

### 4.4 The arrow

`viewBox="0 0 30 30"`, one path, three instances:

`M6.25 20C7.1775 20 8.5625 20.9163 9.725 21.8438C11.225 23.0363 12.5338 24.4612 13.5325 26.095C14.2813 27.32 15 28.805 15 30M15 30C15 28.805 15.7187 27.3187 16.4675 26.0`

A downward arrow whose head is two curves rather than two straight strokes, so
the head is a soft chevron. It is stroked, not filled. Rotated `180deg` for
back-to-top, measured as `matrix(1, 0, 0, -1, 0, 0)` on `9` elements, which is a
vertical flip rather than a rotation and preserves the curve direction.

### 4.5 The star

`viewBox="0 0 200 200"`, one path plus a rect:

`M107.143 0H92.8571V63.2531L69.1621 4.60582L55.9166 9.95735L80.2255 70.1239L34.3401 24.2385L24.2386 34.3401L68.2177 78.3191L11.2241 53.4181L5.50459 66.5089L65.8105 92.85`

Sixteen points on a `200` field centred at `100`, alternating on the cardinal
and diagonal axes, outer radius `100` and a bar width of `14.286`. It is a
sixteen-point asterisk, not an eight-point star, and it separates the two words
of each section title: `Selected` star `work`, and `About` star `me`.

### 4.6 The text arc

A quadratic path, `M0 250 Q503.99999999999994 250, 1007.9999999999999 250`,
`1008px` wide inside a `707` by `500` box positioned `250px` above its parent.
A control point equal to the endpoints makes it a straight line at rest; the
scroll system bends it by moving the control point, and text set on it curves.
Measured `transform` on the same element takes three distinct values under
scroll (Section 7.3).

### 4.7 The two groups that are not the site's own

**Tool marks.** Fourteen drawings at `21px` in a horizontal band: the tools
named in the services copy and their siblings. They are third-party logos, are
not redrawn here, and are replaced in Section 36.5.

**Award badges.** Two drawings at `50px` and `90px` in the fixed rail. Both name
their awarding bodies in their element identifiers and both are third-party
marks. Replaced by `<AWARD_ONE>` and `<AWARD_TWO>` and specified as a generic
badge in Section 5.6.

### 4.8 Drawing a new mark

Any mark this build adds is drawn on a square field, stroked rather than filled
where the measured set is stroked, with the arrow's soft-chevron head as the
house style for any directional mark, and never as a filled triangle.

> **In plain language.** Four kinds of small drawing on this site, and only two
> of them are his.
>
> His own: a monogram made of two rounded keycaps stepped diagonally, a menu icon
> that is a bar between two curled hooks rather than the usual three lines, a
> downward arrow whose head is curved rather than pointed, and a sixteen-point
> asterisk that separates the two words of each section heading.
>
> The menu icon is worth the effort. The hooks unwind and the lines cross when
> you open it, drawn on rather than switched, which is the sort of detail people
> notice without knowing why.
>
> The other two kinds are not his and we are not shipping them: the row of tool
> logos along the top, and the two award badges in the strip down the left. Those
> belong to other organisations, so this document replaces them with blanks for
> you to fill in with your own.

---

## 5. Global chrome

### 5.1 The header

Fixed, present on all three routes, at stacking `47` (Section 3.8).

Measured: a scroll-driven `backdrop-filter` taking `blur(0px)` and a blurred
state across the sampled frames, with a `rgba(20, 21, 22, 0.6)` scrim measured
on `27` elements. The header is transparent at the top of the document and
acquires a blurred, tinted ground as content passes under it.

### 5.2 The name lockup

Two stacked text elements, measured as separate classes for the given and family
names, with the monogram (Section 4.2) at `30px` set to their upper right. The
two keycaps carry the two initials.

Measured transform on the lockup: `matrix(1, 0, 0, 1, -57.2812, 0)` on `6`
elements, a horizontal offset of `57.28px`, which is the lockup sliding in from
the left on load rather than fading.

### 5.3 The availability pill

The most commercially important element on the site and fully measured.

| Property | Value |
|---|---|
| copy | `available now for work` |
| radius | `50px` |
| container radius | `16px` |
| border | `1px`, `--c-green` |
| ground | transparent over the dark ground |
| text | `--c-paper` |
| the dot | the `0 0 20 20` circle at `r = 5`, filled `--c-green` |
| the halo | `rgba(33, 150, 83, 0.3)`, measured on `30` elements |
| transform | `matrix(1, 0, 0, 1, -132.656, -23)` on `20` elements |

The measured transform is an offset of `132.66px` left and `23px` up, which is
the pill's entry position: it arrives from the upper left rather than fading in.

**Capability requirement - normative.** The pill reflects real state, not a
hard-coded string. Section 15 specifies where that state lives, and the pill has
exactly two forms: available, with the green dot, and a booked form naming the
next open window. It is never absent.

### 5.4 Navigation

Four links, measured as `Home`, `About`, `Work`, `Contact`, stacked at the right
at desktop and folded into the burger below the measured `900px` query.

`Home` and `About` are anchors into the home document; `Work` and `Contact` are
routes. That asymmetry is measured and must be preserved in the address bar: an
anchor updates the fragment, a route updates the path.

### 5.5 The route label

Measured on `/work` and `/contact` and absent on `/`: a label carrying the route
name, with radius `0px 0px 0px 20px`, on `29` elements, and a measured
`matrix(1, 0, 0, 1, 0, 500)` transform, a `500px` vertical offset, which is its
entry.

It names the current route in the top left of the content area, under the
chrome, with a single rounded corner where it meets the page edge.

### 5.6 The fixed rail

Section 2.5. Two badges and a vertical `Honors` label at the left edge, at
stacking `10` to `13`, never scrolling.

| Property | Value |
|---|---|
| width | `53px` |
| position | `y = 337` to `562` at desktop |
| the label | rotated to read bottom-to-top |
| badge one | `90px` field, rendered `50px`, with radius `90px` |
| badge two | rendered at `1.35` scale, measured as `matrix(1.35, 0, 0, 1.35, 0, 0)` |

Both badges are replaced (Section 4.7). The rail itself is measured and is kept:
it is a strong, cheap credibility signal that costs no vertical space.

### 5.7 The custom cursor

Measured: a `50%` radius element and a label element, both at stacking `105`,
with the measured label copy `View` on the work index. It replaces the pointer
over project rows and names the action.

### 5.8 The account control **[extension]**

When a session exists, a fourth chrome element joins at the right, using the
availability pill's own treatment at `50px` radius, carrying the account initial
and the enquiry count. No new shape and no new colour.

> **In plain language.** The header is see-through at the top of the page and
> picks up a blurred, darkened background as you scroll content under it.
>
> His name sits at the left with a small monogram of two stepped keycaps. In the
> middle, the green badge saying he is available for work, which is the single
> most valuable thing on the page commercially. It has a small green dot with a
> soft glow, and it slides in from the upper left rather than fading.
>
> That badge must be telling the truth. In our version it reads from the real
> booking calendar rather than being typed into the code, and when he is booked
> it says when he is next free rather than disappearing.
>
> Down the left edge is a narrow strip with two award badges and the word Honors
> reading upward. Those badges belong to the organisations that gave them, so we
> have left blanks. Keep the strip: it is credibility that costs no space.
>
> On the work list the mouse pointer is replaced by a circle that says View.

---

## 6. Motion language

### 6.1 The easing set

Nine curves were measured. One carries the document.

| Token | Curve | Count | Role |
|---|---|---|---|
| `--ease` | `cubic-bezier(.76,0,.24,1)` | 13 | every transform, the signature |
| `--ease-quick` | `cubic-bezier(.615,.19,.305,.91)` | 2 | the two short control transitions |
| `--ease-slow` | `cubic-bezier(.2,.49,.32,.99)` | 1 | the one long fade, at `3.45s` |
| `--ease-expo` | `cubic-bezier(.075,.82,.165,1)` | 2 | reveals |
| `--ease-standard` | `cubic-bezier(.4,0,.2,1)` | 2 | the utility layer's default |
| `--ease-in` | `cubic-bezier(.4,0,1,1)` | 1 | the utility layer |
| `--ease-out` | `cubic-bezier(0,0,.2,1)` | 1 | the utility layer |
| `--ease-bounce-in` | `cubic-bezier(.8,0,1,1)` | 1 | the bounce keyframe, Section 6.7 |

The signature is a symmetric in-out with very steep ends: it holds still,
accelerates hard, and stops hard. It is declared with and without leading zeros
in the reference; both forms are in the ledger and both validate, which is not
true of every curve here (Section 37.5).

### 6.2 Durations

| Token | Value | Measured on |
|---|---|---|
| `--d-micro` | `0.12s` | the shortest control transition, `30` declarations |
| `--d-quick` | `0.25s` | control state, `30` declarations |
| `--d-draw` | `0.4s` | the burger's stroke draw, `90` declarations, and colour, `30` |
| `--d` | `0.5s` | every transform, `281` declarations |
| `--d-long` | `3.45s` | the scroll prompt's fade, `3` declarations and measured live |

The `3.45s` is real and is measured both as a declaration and as a live
transition on the scroll prompt. It is the slowest thing on the site by a factor
of seven, and it is the hero's invitation fading in after everything else has
settled.

### 6.3 Declared transitions, as measured

| Declaration | Count |
|---|---|
| `all` | 6131 |
| `transform 0.5s cubic-bezier(.76,0,.24,1)` | 281 |
| `stroke-dasharray 0.4s, stroke-dashoffset 0.4s` | 90 |
| `0.5s cubic-bezier(.76,0,.24,1)` | 60 |
| `0.5s` | 36 |
| `transform 0.4s` | 30 |
| `0.25s cubic-bezier(.615,.19,.305,.91)` | 30 |
| `0.12s cubic-bezier(.615,.19,.305,.91)` | 30 |
| `color 0.4s linear` | 30 |
| `0.4s` | 14 |
| `3.45s cubic-bezier(.2,.49,.32,.99)` | 3 |
| `top 0.5s cubic-bezier(.76,0,.24,1)` | 2 |

`all` at `6131` is a utility artifact and the largest such count in this kit's
corpus. Do not reproduce a transition on `all`; reproduce the named ones. A
transition on `all` over six thousand elements is also a measurable performance
cost (Section 32.5).

### 6.4 The shadow reveal

The document's signature effect, and fully measured.

Every word of the about statement exists twice: once as a shadow copy carrying a
dedicated class at `opacity: 0.15`, measured on `138` elements, and once as the
word itself. The measured `span` opacities across the sampled frames form a
descending ladder, `0.9948`, `0.9866`, `0.9774`, `0.9670`, `0.9552`, `0.9417`,
`0.9263`, `0.9086`, `0.8880`, `0.8638`, which is a per-word stagger under scroll
rather than a single fade.

**Capability requirement - normative.** The statement is split per word. Each
word has a shadow twin at `0.15` opacity, offset, and the word itself rises over
its twin as the document advances. The ten measured opacity values are the
acceptance values at the sampled positions.

The split must leave the statement selectable and announced as one string
(Section 31.5).

### 6.5 The underline

A two-point path, `M0 0 484.375 0`, `484px` wide at `2px` stroke, with
`overflow-visible` declared so the stroke is not clipped at its own bounds. It
is drawn with the same `stroke-dasharray` transition as the burger, and it sits
under the section titles.

### 6.6 Stroke drawing

`stroke-dasharray 0.4s, stroke-dashoffset 0.4s` on `90` elements is the largest
single motion declaration after the transform. Every stroked mark on this site
draws itself rather than appearing: the burger, the underline, the arrow and the
text arc.

That is the motion identity. A build that fades these in has lost it.

### 6.7 The bounce keyframe

One keyframe was measured:

`{0%, 100% {animation-timing-function: cubic-bezier(.8,0,1,1); transform: translateY(-25%)} 50% {animation-timing-function: cubic-bezier(0,0,.2,1); transform: none}}`

It is the utility layer's stock bounce and carries two different easings inside
one keyframe set, which is how a bounce is made to feel weighted. It is used
once, on the scroll prompt.

### 6.8 Runtime animations

Five were captured live. Four run for `1000ms` with `fill: both` on an ease-out
curve, and one is the `3450ms` scroll-prompt fade.

The curve on those four is recorded in the animation timing and **is not in the
ledger's declared easing list**, so this document does not quote its literal
(Section 37.5). It is a standard ease-out with a long tail; reproduce it as
`--ease-expo`, which is measured, and adjust against the screenshots.

### 6.9 The named-motion table

| Name | Trigger | Property | Duration | Easing | Reduced-motion substitute |
|---|---|---|---|---|---|
| `chrome-enter` | load | `transform` | `0.5s` | `--ease` | present |
| `pill-enter` | load | `transform` | `0.5s` | `--ease` | present |
| `route-label-enter` | route change | `transform` | `0.5s` | `--ease` | present |
| `shadow-reveal` | scroll | `opacity`, `transform` | per word under scroll | `--ease` | present at full opacity |
| `stroke-draw` | enter or activation | `stroke-dasharray`, `stroke-dashoffset` | `0.4s` | linear | drawn, no animation |
| `burger-cross` | activation | as above | `0.4s` | linear | switched |
| `control-quick` | pointer or focus | mixed | `0.25s` | `--ease-quick` | kept |
| `control-micro` | press | mixed | `0.12s` | `--ease-quick` | kept |
| `colour-shift` | section change | `color` | `0.4s` | linear | kept |
| `prompt-fade` | load, once | `opacity` | `3.45s` | `--ease-slow` | `0.4s` |
| `card-stack` | scroll | `transform` | scrubbed | `--ease` | static stack |
| `header-blur` | scroll | `backdrop-filter` | scrubbed | `--ease` | applied at rest |
| `slot-settle` **[extension]** | a booking window is chosen | `transform` | `0.5s` | `--ease` | instant |

### 6.10 Reduced motion

No reduced-motion query was measured, which on a document with fourteen
scroll-driven selectors is a defect rather than a decision (Section 37.6). This
build implements the table above, and in addition the render layer holds one
frame and the document scrolls natively.

> **In plain language.** One movement curve does nearly everything: it holds
> still, accelerates hard, then stops hard. Half a second, on almost every moving
> thing. That single choice is why the whole site feels like one object.
>
> Two effects define the site. First, every word of the paragraph about him
> exists twice, once as a faint ghost behind itself, and the real word rises over
> its ghost as you scroll, one word at a time. We measured ten separate steps of
> that. Second, every line drawing on the site draws itself on, like a pen moving
> across the page, rather than fading in: the menu icon, the underlines, the
> arrows. If those fade in instead, the site loses its character.
>
> One thing is deliberately much slower than everything else. The invitation to
> scroll takes three and a half seconds to appear, roughly seven times slower
> than anything else on the page, arriving only after everything has settled.
>
> The site has no setting for people who prefer less movement, which for a page
> with fourteen separate scroll-driven effects is a real gap. We are adding one.

---

## 7. Scroll system

### 7.1 The document scrolls

Unlike much of this corpus, this reference scrolls natively. Measured positions
on the home document at desktop: `0`, `605`, `1260`, `1865`, `2521`, `3126`,
`3781`, `4386`, `5042`.

**Observed implementation - informational.** The document element carries a
smooth-scroll class in two states, at rest and scrolling, and the bundle exposes
a smooth-scroll global (tier 3 and tier 6). A scroll-trigger utility is also
present (tier 6).

**Capability requirement - normative.** Wheel input drives an interpolated
scroll position and every scroll-driven effect reads it. Native scrolling,
keyboard scrolling, scrollbar dragging and anchor jumps must all continue to
work, and reduced motion falls back to native scrolling.

### 7.2 Document lengths, measured

| Route | Desktop |
|---|---|
| `/` | `5042px`, five and a half frames |
| `/work` | measured across nine positions |
| `/contact` | measured across nine positions |

### 7.3 What is scrubbed

Fourteen selectors change under scroll on the home document at desktop. In order
of the number of distinct values each took:

| Selector | Property | Distinct values |
|---|---|---|
| a card | `transform` | 18 |
| a gallery column | `transform` | 6 |
| the text arc | `transform` | 3 |
| a flex wrapper | `transform` | 3 |
| a section title | `opacity` and `transform` | 2 each |
| two statement titles | `opacity` and `transform` | 2 each |
| the header | `backdrop-filter` | 2 |
| a clip group | `clip-path` | 2 |
| the hero section | `transform` | 2 |
| a media wrapper | `transform` | 2 |
| a word span | `opacity` | 2 |
| the contact section | `transform` | 2 |

Fourteen is a lot, and the card at `18` distinct transform values is the most
finely scrubbed element in this kit's corpus.

### 7.4 The sheet transitions

Measured transforms on the page body element, `matrix(1, 0, 0, 1, 0, 844)`,
`800`, `900` and `-900`, on `45`, `45`, `38` and `7` elements. Those are whole
viewport heights at the three captured breakpoints, positive and negative.

Combined with the measured one-sided radii of Section 3.7 and the measured
`rgba(255, 255, 255, 0.15) 0px -3px 0px 0px` shadow on the about section, the
mechanism is: each section is a sheet that slides a full frame height, with a
rounded top edge and a `3px` light line along it, so a new ground appears to
slide up over the one before it.

That is the transition between the dark hero and the lavender about surface, and
it is the most recognisable movement on the site.

### 7.5 The card stack

The `18`-value transform, on a card carrying the measured shadow
`rgba(33, 13, 70, 0.247) 40px 80px 80px 1.6px`. That shadow is enormous, offset
`40px` right and `80px` down with an `80px` blur, and tinted purple rather than
black. A stack of cards under scroll, each casting a large soft purple shadow on
the one behind it.

Reproduce the tint. A neutral shadow at that size on a lavender ground reads as
dirt.

### 7.6 The header blur

Two measured values, `blur(0px)` and a blurred state, with the
`rgba(20, 21, 22, 0.6)` scrim. Scrubbed rather than switched: the header acquires
its ground progressively over the first frame of scroll.

Three further blur values were measured elsewhere: `blur(30px)` on a card,
`blur(20px)` on a fixed bar and `blur(50px)` on the contact section.

### 7.7 Anchors

`Home` and `About` are anchors, `Work` and `Contact` are routes (Section 5.4).
An anchor sets the scroll position directly rather than animating through the
intervening sections, and updates the fragment without adding a history entry
per section.

### 7.8 The booking routes **[extension]**

`/availability`, `/enquiry/<id>`, `/account` and the studio routes use native
scrolling with no scrubbed effects. A form is not a place for a card stack.

> **In plain language.** This page scrolls normally, which made it much easier to
> measure than most: our tool could walk down it taking readings at nine points
> on every screen size, so nearly everything in this document is measured.
>
> Fourteen separate things respond to your scrolling on the home page alone. The
> most finely tuned is a stack of cards that moves through eighteen distinct
> positions, each card casting a big soft purple shadow on the one behind it. The
> purple tint matters: a plain grey shadow that size on a lavender background
> looks like a smudge.
>
> The signature movement is how the sections change. Each one is a sheet that
> slides up a full screen height, with its top corners rounded and a thin bright
> line along the top edge, so the lavender section appears to slide up over the
> black one like a card being dealt.
>
> And the header quietly acquires a blurred, darkened background over the first
> screen of scrolling rather than switching it on suddenly.

---

## 8. The rendered layer

### 8.1 What it is

A render surface behind the hero, carrying a lit blue form visible between the
letters of the name.

**Observed implementation - informational.** Tier 6 identifiers: a scene graph, a
compressed-geometry loader, a model loader and a render pass, plus literal
shader source. A motion library and a scroll-trigger utility are present
alongside it.

**Capability requirement - normative.** The build must render a continuously
animated three-dimensional form behind the hero, composited under the document,
and must hold the frame budget in Section 32.2 without requiring any binary.

### 8.2 The measured composition

From the desktop hero screenshot: a rounded blue mass occupying roughly the
central fifth of the frame, sitting behind the name and visible through the
counters and between the letters. Its top edge is at `0.36` of frame height and
its widest point at `0.5`.

It is lit from the upper left with a specular highlight, and its silhouette is
lobed rather than spherical, consistent with a metaball or a deformed sphere.
Marked **inferred** as to form, measured as to position and colour.

### 8.3 The hero gradient and halo

Both measured, and both reproducible without any render context:

| Layer | Value | Count |
|---|---|---|
| the ground | `radial-gradient(circle at center top, rgb(20, 21, 22), rgb(0, 0, 0))` | 145 |
| the halo | `radial-gradient(80% 60% at 50% 0px, rgba(139, 92, 246, 0.25), rgba(0, 0, 0, 0) 70%)` | 5 |

The ground is a near-black falling to true black from the top centre. Over it, a
violet halo at `0.25` alpha spanning `80%` of the width and `60%` of the height,
anchored to the top edge and fading out at `70%`.

That halo is the whole atmosphere of the hero, it is declared in the stylesheet,
and it does not need the render layer. It is also declared in a shorter form as
`radial-gradient(80% 60% at 50% 0, #8b5cf640, #0000 70%)`, which is the same
value.

### 8.4 The contact texture

Measured on the contact section: an inline vector data value, a `600` by `600`
tiling pattern at `fill-opacity: 0.1` in a mid grey, drawn as continuous
contour-like paths. A topographic texture at one tenth opacity over the dark
ground.

It is declared as a data value rather than fetched, so it is already zero-asset
and is reproduced as measured.

### 8.5 Media treatment

| Effect | Value | Count |
|---|---|---|
| grayscale at rest | `grayscale(1)` | 3 |
| grayscale on activation | `grayscale(0)` | 2 |
| the card scrim | `linear-gradient(133.655deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.6) 100%)` | 3 |
| the card blur | `blur(30px)` behind the card | 21 |
| the deep shadow | `rgba(0, 0, 0, 0.75) 0px 60px 50px 0px` | 2 |

Project media is grey at rest and takes colour on activation. The `133.655deg`
scrim angle is measured and is not a round number: it is a diagonal from the
upper left, and rounding it to `135deg` changes where the darkening lands
relative to the caption.

### 8.6 Degradation

| Condition | Behaviour |
|---|---|
| reduced motion | one frame, held |
| the render context is unavailable | the hero renders as the measured gradient and halo alone, which is already the design's atmosphere; nothing else changes and no notice is shown |
| sustained frame rate below the floor | the form's animation stops, then the form is dropped |
| below `690px` | the form renders at half resolution |

The fallback here is unusually strong: the measured gradient and halo alone
produce most of the hero's effect, and they are stylesheet values.

> **In plain language.** Behind the big name in the hero there is a rounded blue
> form, lit from the upper left, visible through the gaps in the letters.
>
> The good news is that most of the hero's atmosphere does not depend on it at
> all. The dark background fading from near-black to black, and the soft violet
> glow across the top of the screen, are both ordinary styling that we measured
> exactly. On a machine that cannot draw the blue form, you still get the
> atmosphere and the page looks intentional rather than broken.
>
> The contact page has a faint topographic contour pattern over the dark
> background, like a map, at one tenth strength. That was already built as
> instructions rather than a picture file, so we reproduce it exactly.
>
> Project pictures are grey until you point at them, then take their colour.

---

## 9. The hero

Document position `0` to roughly `605`, the first measured scroll step.

### 9.1 Contents

| Element | Type | Colour |
|---|---|---|
| the eyebrow, `Creative Developer` | the display face, outlined | `--c-paper` stroke |
| the name, at display size | the display face, filled | `--c-paper` |
| `Located in France` | `.h2` | `--c-paper` |
| the flag bar | three segments | measured, Section 9.3 |
| `Scroll down to explore` | `.base` | `--c-paper` |
| the arrow | Section 4.4 | `--c-paper` stroke |
| the render layer | Section 8 | behind the name |
| the ground and halo | Section 8.3 | measured gradients |

### 9.2 The name

Set at `.display-l`, `96px` on `96px`, in the display face, filled rather than
outlined. The eyebrow above it is the same face outlined. That pairing, an
outlined line above a filled line in one typeface, is the hero's whole
typographic idea.

Measured from the screenshot: the name spans roughly `0.61` of the frame width
and is optically centred, with the render layer's blue form visible between the
letters and through the counters. The accent on the final character sits clear
of the cap line as a separate mark.

### 9.3 The flag bar

Three elements were measured live under one animation: a left segment, a
`flagMiddle` and a `textRight`, all at `1000ms` with `fill: both`, all reaching
`opacity: 0.764142` at the sampled frame.

From the screenshot: a `3px` horizontal bar under `Located in France`, in three
equal segments, blue then white then red. It is a French flag rendered as a
rule, and it is the only saturated blue and red in the document.

**Capability requirement - normative.** The bar is three segments in the
country's own colours, tied to the location string. If the location changes, the
bar changes with it or is removed; a tricolour under a different country is
wrong in a way that will be noticed.

The three segments animate in sequence, not together: three elements, one
`1000ms` animation each, `fill: both`.

### 9.4 The scroll prompt

`Scroll down to explore` at `.base`, with the arrow below it, fading in over
`3.45s` on `--ease-slow` (Section 6.2), which is measured both as a declaration
and live. The arrow carries the bounce keyframe (Section 6.7).

Nothing else on the site takes anything like `3.45s`. It arrives last, long
after the name has settled, and it is the hero's one moment of patience.

### 9.5 What the hero does not have

No headline sentence, no call to action beyond the availability pill, no
navigation beyond the chrome, and no cookie banner in any captured frame. The
name, what he does, where he is, whether he is free.

> **In plain language.** One screen. The words creative developer in tall narrow
> outlined capitals, his name below in the same typeface but filled in solid, and
> a rounded blue shape behind the letters showing through the gaps.
>
> Under that, located in France, with a small three-part bar in blue, white and
> red beneath it, the segments arriving one after another. It is a French flag
> drawn as a rule, and it is the only strong blue and red anywhere on the site.
>
> Then, three and a half seconds later, long after everything else has settled,
> the words scroll down to explore fade in with a gently bouncing arrow. That
> patience is deliberate and it is the one slow thing on the whole site.
>
> That is the entire first screen: who he is, what he does, where he is, and
> whether he is free. No slogan, no button, no cookie banner.

---

## 10. Section: About

Reached at the first sheet transition (Section 7.4), where the lavender ground
slides up over the dark hero.

### 10.1 The section title

`About` star `me`, the two words separated by the sixteen-point asterisk of
Section 4.5, set in the outlined display face in `--c-purple` on the lavender
ground, with the drawn underline of Section 6.5 beneath it.

Both section titles on the site use this construction. It is the site's heading
system and there is no other.

### 10.2 The statement

The longest measured string in the capture, at `.display-xl`, `97.5px` on
`146.25px`, split per word with the shadow reveal of Section 6.4:

`An award-winning, product-minded frontend engineer with a background in aerospace engineering and human factors. I design and build visually striking web and mobile products where usability, reliability and performance matter, from concept to launch, with a strong focus on thoughtful UX, engaging interactions and practical AI-powered workflows.`

Sixty-nine words, each with a shadow twin. Set loose rather than solid, because
it is a paragraph at display size and not a heading (Section 3.5).

The measured copy joins `matter` and `from` with a typographic dash. This
document writes that join as a comma, because the copy deck is pasted into build
tooling as plain text (Section 35).

### 10.3 The experience figure

Two measured elements side by side:

| Element | Copy | Type |
|---|---|---|
| the figure | `5+` | `.display-m`, `80px` on `120px`, weight 700 |
| the label | `years of experience` | `.base` |

### 10.4 The services

Three measured, each a title and a line:

| Service | Description |
|---|---|
| `SEO` | `Optimizing data to improve search engine rankings.` |
| `UX Design` | `From product's exploration to evaluation.` |
| `Web & Mobile Development` | `Industry-leading tools such as React, Three, Framer will be used to build your app.` |

The third names three specific libraries in customer-facing copy. That is
measured and is reproduced in the copy deck, but Section 35.4 flags it: naming
libraries to a client dates the page and promises a stack rather than an
outcome. This build keeps the sentence and marks it for the copywriter.

A measured `title` element reads `Figma icon`, so the services carry tool marks
(Section 4.7), replaced here.

### 10.5 The tool band

Measured as fourteen drawings at `21px` in a horizontal row across the top of
this section, on a dark rounded panel with `blur(30px)` behind it.

**Capability requirement - normative.** The band is a horizontally scrolling
marquee of tool marks, seeded from a list, with each mark carrying an accessible
name. It is decorative and is hidden from assistive technology as a group while
each mark keeps its name for anyone who inspects it.

Marks are replaced (Section 36.5): they are third-party logos.

### 10.6 The card stack

The `18`-value scrubbed transform (Section 7.5) belongs to this section: a stack
of cards at `20px` radius carrying the large purple-tinted shadow, moving under
scroll.

> **In plain language.** The lavender section slides up over the black hero, and
> the heading reads about, then a sixteen-point asterisk, then me, in outlined
> purple capitals with a line drawn underneath.
>
> Then the paragraph that does the selling, set enormous and arriving one word at
> a time, each word rising over a faint ghost of itself. Sixty-nine words about
> being an award-winning frontend engineer who came from aerospace engineering.
>
> Under that, a large 5+ with years of experience beside it, and three services:
> search optimisation, user experience design, and web and mobile development.
>
> One note for your copywriter. The third service names three specific tools by
> name in customer-facing copy. We have kept it exactly as written, but it is
> worth reconsidering: naming your tools promises a client a particular stack
> rather than a result, and it dates the page the moment fashions change.

---

## 11. Section: Selected work

The home document's work preview, distinct from the `/work` route.

### 11.1 The section title

`Selected` star `work`, the same construction as Section 10.1, in outlined
purple on lavender with the drawn underline.

### 11.2 The rows

Measured: a rule, then a title at `.subhead` in `--c-purple`, then the credit
line right-aligned in the same row, then a rule. The first entry was captured as
an `h2` at `.subhead`.

| Element | Type | Alignment |
|---|---|---|
| title | `.subhead`, `20px` on `30px` | left |
| credit | `.base` | right |
| rule | `1px` in `#32146938` | full row width |

The credit line carries the discipline and the year: `Development © 2026`,
`Design & Development © 2025`, and so on (Section 35.7).

### 11.3 The relationship to `/work`

The home preview and the `/work` index draw from the same nine records. The
preview shows them as rules-and-rows; the route shows them as the pill layout in
Section 12.2. One data source, two presentations, one component with two
densities (Section 29.3).

### 11.4 The text arc

The quadratic path of Section 4.6 sits in this section, `1008px` wide, with text
set along it and its transform taking three distinct values under scroll. It
bends as the document advances.

> **In plain language.** The heading reads selected, asterisk, work, then the
> projects as simple rows: the name on the left, what he did and the year on the
> right, with a thin purple line between each.
>
> The same nine projects appear again on the work page in a completely different
> layout. Same information, two presentations, and in our build that is one
> component used two ways rather than two things that will slowly drift apart.
>
> Somewhere in this section a line of text is set along a curve that bends as you
> scroll, which is a small piece of showing off and entirely in keeping.

---

## 12. Route: Work

`/work`. A distinct document.

### 12.1 The headline

Measured as one element per character, seventy-one characters:

`Elevate user experience through cutting-edge technology and design`

Split per letter, not per word, which is a different treatment from the about
statement (Section 6.4) and is the only per-letter split in the capture.

### 12.2 The index

Measured: a `Work` label and a count, `(09)`, then nine entries.

| Element | Type | Radius | Measured |
|---|---|---|---|
| the title pill | `.subhead` on `--c-purple`, text `--c-paper` | `10px` | 9 entries |
| the credit pill | `.base` on `--c-paper`, text `--c-purple` | `10px` | 9 entries |
| the row | absolutely positioned, staggered | none | `matrix(1, 0, 0, 1, 200, 0)` on `8` elements |

From the screenshot: the nine entries are not a list. Each is a solid purple
pill carrying the project name, scattered at different horizontal offsets down
the page, with a white pill carrying the credit line placed near it but not
aligned to it. The measured `200px` horizontal transform on `8` elements is the
stagger.

The count `(09)` is measured with a leading zero and is copy, not a computed
join. If a tenth project is added it reads `(10)`, and the padding rule is two
digits.

### 12.3 The cursor

Over a project row the pointer is replaced by the custom cursor (Section 5.7)
carrying the measured label `View`.

### 12.4 The modal

Measured: a modal container at `20px` radius and a separate mobile panel at the
same radius, both present in the markup. Selecting a project opens it in place
rather than routing away.

The modal's contents were not captured (Section 37.4). This build specifies it
as the project detail of Section 12.5, opened over the index, with the address
updated so a project can be linked to directly.

### 12.5 Project detail

`/work/<slug>`, and the modal's content. Not measured beyond the record fields
in Section 12.2.

| Element | Source |
|---|---|
| title | measured |
| discipline and year | measured |
| media | generated, Section 36.4 |
| description | not captured, authored per project |
| outbound link | not captured, optional per project |

### 12.6 The footer

Measured on both `/work` and `/contact`, four columns:

| Head | Contents |
|---|---|
| `Local Time` | a live clock, measured as `01:59 PM GMT+2` |
| `Version` | `2.0.0 © 2024` |
| `Resource` | `Portfolio v1.0.5` |
| `Social Media` | `<SOCIAL_ONE>`, `<SOCIAL_TWO>`, `<SOCIAL_THREE>` |

Closing line: `Made by <GIVEN_NAME>`.

**The clock is live and must stay live.** A time in the footer that does not
tick is worse than no clock, and the measured value carries its offset, so it is
his local time and not the visitor's. Section 26.4 specifies the formatting.

The `Version` and `Resource` entries name the site's own version and its
predecessor. That is a developer's footer and it is charming; it also means the
version string is content, not a build constant, and it belongs in the content
model (Section 24.1).

> **In plain language.** The work page opens with a sentence that arrives one
> letter at a time, then the nine projects.
>
> They are not a tidy list. Each project name sits in a solid purple pill,
> scattered at different distances across the page as you scroll down, with a
> white pill carrying the year placed near it but deliberately not lined up.
> Pointing at one turns your cursor into a circle that says View, and clicking
> opens the project without leaving the page.
>
> The footer is a developer's footer and it is charming: his local time, ticking
> live, the version number of the site itself, and a link to the previous version
> of his portfolio. Keep the clock ticking. A clock in a footer that is frozen is
> worse than no clock at all.

---

## 13. Route: Contact

`/contact`. A distinct document, on the dark ground with the topographic texture
of Section 8.4.

### 13.1 The headline

From the screenshot, in the outlined display face at `.display-l`, four lines:

`LET'S BUILD YOUR IDEA TOGETHER :)`

The last line is a typed emoticon, `:)`, set at the same display size and
rendered as outlined glyphs like the rest. It is measured as copy, not as a
drawing, and it must be the typed characters so that it inherits the outline
treatment.

Beside the first line, a circular portrait at `50%` radius with a purple ring.

### 13.2 The form

Six measured fields, each numbered, each a label over an underlined input with
no box.

| No. | Label | Required | Placeholder |
|---|---|---|---|
| `01.` | `My Name` | yes | a person's name |
| `02.` | `My Email` | yes | that person's address |
| `03.` | `I work at` | no | that person's company |
| `04.` | `I am looking for` | yes | not captured |
| `05.` | `My budget is` | yes | a select, Section 13.3 |
| `06.` | `My message` | yes | not captured |

Required fields are marked with a measured asterisk element, and four of the six
carry it.

The measured placeholders are a well-known executive's name, address and
employer. That is a joke, and it is a bad one to ship: it puts a real person's
name and a plausible address into your form. Section 35.5 replaces all three
and Section 37.6 records why.

### 13.3 The budget select

Four measured options, in descending order:

- `USD $20001 and up`
- `USD $10001-$20000`
- `USD $5001-$10000`
- `USD $2000-$5000`

Descending is deliberate and is worth keeping: the first option a visitor sees
is the largest band. The currency is named on every option rather than assumed,
which matters for a freelancer working across borders.

The measured lowest band starts at `$2000`, so there is no "under `$2000`"
option. That is a qualification filter, not an omission, and this build keeps it
while adding the copy in Section 19.4 that tells somebody below the floor what
to do instead.

### 13.4 The submit

Measured copy: `Send it now :)`. The same emoticon as the headline, and the
site's only exclamation of personality in a control.

### 13.5 The side column

| Head | Contents |
|---|---|
| `Further Inquiries` | `<CONTACT_EMAIL>`, and `Located in France 📍` |
| `Social Media` | the three links |

The location string here carries an emoji, where the hero's carries the flag bar
(Section 9.3). Two treatments of one fact; both are measured and both are kept,
because they are in different registers.

### 13.6 What the form does not do

Nothing was captured behind the submit. Section 18 specifies it.

> **In plain language.** The contact page is dark, with a faint contour-map
> texture, and a headline in the tall outlined capitals reading let's build your
> idea together, with a typed smiley on its own line at the same enormous size.
>
> The form is six numbered questions, each just a line to write on rather than a
> box: your name, your email, where you work, what you are looking for, your
> budget, and your message.
>
> The budget is a menu of four ranges, biggest first, and it starts at two
> thousand dollars. There is no smaller option, which is a polite way of filtering
> out enquiries that are not worth either side's time. We are keeping that and
> adding a line telling people below that figure what to do instead.
>
> One thing to fix before launch: the example text in the form uses a famous
> chief executive's real name, a plausible email address at his company, and that
> company's name. It is a joke, but it puts a real person's name and a guessable
> work address into your form, and we have replaced all three.

---

## 14. Sound

### 14.1 What was measured

A `Sound | OFF` control in the chrome on all three routes, `21` audio files
totalling `1.57MB`, and an audio context in the bundle (tier 6).

The control's measured state is `OFF`, which is the state at capture and is not
necessarily the default.

### 14.2 The default

**Capability requirement - normative.** Sound is off on arrival, always, and the
control's persisted state is restored on return.

The reference's own control reads `OFF` in every captured frame at every
breakpoint, which is consistent with off being the default and is the only
defensible default regardless: no browser will start audio unbidden, and a
portfolio that makes noise at a stranger is a portfolio they close.

### 14.3 What the sounds are

Twenty-one files is far more than an ambient bed. Measured file count against
the measured interaction surfaces suggests one cue per interaction class:
pointer over a control, press, section change, form field focus, submit, and the
modal opening and closing.

Marked **inferred**: the count is measured, the mapping is not.

### 14.4 The control

`Sound | OFF` as literal copy, with the state as the second half of the string.
Its accessible name states the state it will move to, not the state it is in,
and the visible string states the current state. Those are different strings on
purpose (Section 31.6).

### 14.5 Rules

| Rule | Why |
|---|---|
| off by default | Section 14.2 |
| one cue per interaction class, never layered | twenty-one distinct sounds firing at once is noise |
| no cue longer than `400ms` | the longest measured control transition |
| no cue on scroll | scroll is continuous and a cue on it is unbearable |
| every cue has a silent equivalent state | sound never carries information alone, Section 31.7 |
| ducked or suppressed under reduced motion | Section 6.10 |

> **In plain language.** The site has sound: twenty-one separate short sounds,
> one for each kind of thing you can do, plus a control at the top saying Sound |
> OFF.
>
> It starts switched off and stays off unless somebody turns it on, and we
> remember their choice. A portfolio that makes a noise at a stranger is a
> portfolio they close, and browsers increasingly refuse to allow it anyway.
>
> Three rules keep it pleasant. Never play two at once. Nothing longer than about
> a third of a second. And never, ever tie one to scrolling.

---

## 15. Availability

The measured availability pill (Section 5.3) is the site's most valuable
element. This section specifies what stands behind it.

### 15.1 The measured surface

`available now for work`, with a green dot and a green halo, in the chrome on
all three routes at every breakpoint. Nothing behind it was captured.

### 15.2 The state model **[extension]**

| State | Pill copy | Dot |
|---|---|---|
| open now | `available now for work` | `--c-green`, with halo |
| open from a date | `available from` and the month | `--c-green`, no halo |
| booked | `booked until` and the month | `--c-grey-cool`, no halo |
| not taking work | `not taking new work` | `--c-grey-cool`, no halo |

The pill is never absent and never lies. A freelancer's availability is the
single fact a prospective client is looking for, and a stale "available now" is
worse than no pill at all.

### 15.3 The availability page **[extension]**

`/availability`. An ordinary scrolling document on the lavender ground, using
the measured pill treatment and the work index's pill layout.

| Band | Contents |
|---|---|
| 1 | the current state, at display size |
| 2 | the next three open windows, each a start date, a length and a capacity |
| 3 | what a window means: hours per week, timezone, notice period |
| 4 | `Start an enquiry` against a chosen window |

A window is a start date, a duration in weeks and a capacity in days per week.
Two half-capacity projects can share one window; one full-capacity project
cannot.

### 15.4 Where the state comes from

**Capability requirement - normative.** The pill reads from the same records the
availability page renders, which are the same records the booking workflow
writes (Section 18). One source. A pill maintained by hand will be wrong within
a month, and being wrong about this costs work.

### 15.5 The legal document

The reference's footer carries no privacy link, which is a gap given that the
contact form collects a name, an address and an employer (Section 37.6). This
build serves `/legal/privacy` and links it from the form itself, next to the
submit, where it belongs.

> **In plain language.** The green badge saying available now for work is the
> most commercially valuable thing on this site, and on the reference it is just
> words typed into the page.
>
> In our version it is real. It reads from a calendar of open project windows,
> and it has four things it can say: available now, available from a date, booked
> until a date, or not taking new work. It is never missing.
>
> That matters because a stale "available now" is worse than nothing. Somebody
> gets in touch, waits, and finds out you were booked solid. They do not come
> back.
>
> There is also a page listing the next few open windows, with a start date, how
> long, and how many days a week, so a client can see whether their project fits
> before they write to you.
>
> One gap to close: the reference collects a name, an email and an employer with
> no privacy notice anywhere. We are adding one and linking it right next to the
> send button.

---

## 16. Authentication and identity **[extension]**

Nothing here was observed. Every surface is built from the Section 3 tokens, the
measured pill treatment and the measured underlined field of Section 13.2.

### 16.1 An account is not required to enquire

The measured form takes an enquiry with no account, and that stays true. An
account is offered after an enquiry is submitted, as a way to follow it, and the
enquiry is linked to it if taken.

A freelancer's contact form is the top of the funnel. Putting a registration in
front of it is the most expensive mistake this section could make.

### 16.2 The account model

| Field | Type | Rules |
|---|---|---|
| `id` | opaque string | server-issued, never rendered |
| `email` | string | unique, case-folded on write |
| `display_name` | string | 1 to 60 characters |
| `organisation` | string | 0 to 120 characters, from the measured `I work at` field |
| `role` | enum | `client`, `studio`, Section 17 |
| `timezone` | string | for the measured clock and for proposing calls |
| `created_at`, `last_seen_at` | timestamp | server-set |

There is no password by default. Section 16.4 explains what replaces it.

### 16.3 Routes and their signed-in behaviour

| Route | No session | `client` | `studio` |
|---|---|---|---|
| `/`, `/work`, `/contact`, `/availability` | full access | full access | full access |
| `/enquiry/<id>` | with the enquiry token | own only | any |
| `/signin` | the form | redirect to `/account` | redirect to `/studio` |
| `/account` | redirect to `/signin?next=/account` | the account | redirect to `/studio` |
| `/studio`, `/studio/pipeline` | redirect with `next` | Section 20.5 | the pipeline |

`next` is honoured only when it is a path on this origin beginning with a single
`/` and not `//`.

### 16.4 Sign in by link

A link sent to the address on the enquiry, valid for `30` minutes, single use.

| Step | Behaviour |
|---|---|
| an address is entered | `If that address has an enquiry with us, a sign-in link is on its way.`, whether or not it does |
| the link is used | a session is created, the link is invalidated |
| the link is reused or expired | `That link has expired. We can send another.` with a control |

There is one studio account and it may set a password. A single-operator site
does not need a password policy; it needs one strong credential and a short-lived
link for everybody else.

### 16.5 The enquiry token

An enquiry confirmation carries a token in its address, granting read access to
that enquiry and its thread for `90` days without a session.

Ninety days rather than the thirty of a shop: a project conversation runs for
months, and the person who sent the enquiry is often not the person who follows
it up.

### 16.6 The account panel

Reached from the account control (Section 5.8). Rows at `.base`: the display
name and organisation, `Your enquiries` with a count, `Your bookings` with a
count, `Sign out`. It reuses the measured modal container at `20px` radius, not
a new surface.

> **In plain language.** You never need an account to get in touch. Fill in the
> form, send it, done. That is how the reference works and it stays that way,
> because putting a sign-up in front of your contact form is the most expensive
> mistake this whole document could make.
>
> An account is offered afterwards, as a way to follow what is happening with
> your enquiry, and most people will take it.
>
> Signing in is a link emailed to you rather than a password, because nobody
> wants a password for a site they use twice. The link in your confirmation email
> keeps working for three months, which is deliberate: a project conversation
> runs for months, and often the person who first wrote in is not the person who
> follows it up.

---

## 17. Roles and permissions **[extension]**

### 17.1 The roles

| Role | Who | Home |
|---|---|---|
| `client` | somebody who sent an enquiry | `/account` |
| `studio` | the site's owner | `/studio` |

Two roles, not three. This is one person's site, and inventing an editor and an
admin for a single operator is architecture nobody will ever use.

Anonymous visitors are not a role and can do everything up to and including
submitting a scoped enquiry against a window.

### 17.2 Capability matrix

| Capability | anonymous | `client` | `studio` |
|---|---|---|---|
| view every public route | yes | yes | yes |
| view open windows | yes | yes | yes |
| submit an enquiry | yes | yes | yes |
| hold a window with an enquiry | yes, for `72` hours | yes | yes |
| view an enquiry | with the token | own | any |
| reply on an enquiry | with the token | own | any |
| accept a proposal | with the token | own | no |
| withdraw an enquiry | with the token | own | no |
| propose a start date | no | no | yes |
| decline an enquiry | no | no | yes |
| create, move or close a window | no | no | yes |
| edit a project record | no | no | yes |
| set the availability state | no | no | yes, and Section 15.4 |

The two capabilities anonymous visitors have that they would not have on a
commerce site, holding a window and replying with a token, are deliberate: the
whole point is to lower the cost of getting in touch.

### 17.3 The denied surface

A rendered page in the site's own type: the lavender ground, the chrome, the
route label, a `.h2` reading `That is not yours to open.`, a `.base` line naming
who can, and a control back.

It never confirms existence. An enquiry id that does not exist and one belonging
to somebody else render identically.

### 17.4 The single-operator risk

One `studio` account means one point of failure. Three requirements:

- The account has a recovery address distinct from its sign-in address.
- Enquiry notification mail goes to a second address that is not the studio
  account's, so a locked-out operator still sees work arriving.
- The pipeline is exportable by the studio account at any time, in one action,
  so the business is not trapped inside the site.

That third requirement is the one most often skipped and the one that matters
most to the person commissioning this.

> **In plain language.** Two kinds of signed-in person: a client who sent an
> enquiry, and you. Not three, not five. This is one person's site, and building
> a staff hierarchy for a single operator is work nobody will ever use.
>
> Somebody with no account can do almost everything, including holding an open
> project window for three days while they write their brief. That is deliberate:
> the whole point is to make getting in touch cheap.
>
> One risk needs naming. With a single owner account, if you lose access, you
> lose the business. So: a separate recovery address, enquiry alerts also going
> to a second address you control, and a one-click export of everything. That
> last one is the one people skip and the one that matters most.

---

## 18. Primary workflow: enquiry to booking **[extension]**

The workflow this build is graded on.

### 18.1 The objects

| Object | Fields |
|---|---|
| window | `id`, `starts_on`, `weeks`, `capacity_days`, `committed_days`, `state` in `open`, `held`, `booked`, `closed` |
| hold | `window_id`, `enquiry_id`, `expires_at`, `days` |
| enquiry | `id`, `token`, `name`, `email`, `organisation`, `looking_for`, `budget_band`, `message`, `window_id` or null, `state`, `created_at` |
| message | `enquiry_id`, `author`, `body`, `created_at` |
| proposal | `enquiry_id`, `starts_on`, `weeks`, `days_per_week`, `note`, `state`, `expires_at` |
| booking | `enquiry_id`, `window_id`, `starts_on`, `weeks`, `days_per_week`, `confirmed_at` |

`state` on an enquiry is one of `new`, `reading`, `proposed`, `booked`,
`declined`, `withdrawn`, `lapsed`.

### 18.2 The happy path

| Step | Action | State after |
|---|---|---|
| 1 | a visitor reads the work and opens `/availability` | the three open windows are listed with dates and capacity |
| 2 | chooses a window and presses `Start an enquiry` | the contact form opens with the window named at its head and a `72` hour hold created against it |
| 3 | fills the six measured fields | nothing is stored yet; the form holds locally |
| 4 | submits | the enquiry exists in `new`, linked to the window, the hold is attached to it, confirmation mail goes to the visitor and notification to the studio, and the visitor lands on `/enquiry/<id>` with the token |
| 5 | the studio opens `/studio/pipeline` | the enquiry is in the `new` column, newest first, with its budget band and window |
| 6 | the studio reads it | the state becomes `reading` and the client's enquiry page shows it |
| 7 | the studio replies with a question | a message exists and the client is mailed |
| 8 | the client replies | a second message exists; the state does not change |
| 9 | the studio proposes a start date, a length and a capacity | a proposal exists, the enquiry becomes `proposed`, the hold is extended to the proposal's expiry, and the client is mailed |
| 10 | the client accepts | a booking exists, the enquiry becomes `booked`, the window's `committed_days` rises, and if the window is now full its state becomes `booked` |
| 11 | the availability pill re-reads | if no window remains open, the pill moves to its booked form, Section 15.2 |
| 12 | the studio closes the enquiry | the state stays `booked`; closing is a pipeline view filter, not a state |

Step 11 is the point of the whole workflow: the site's most valuable element
updates itself as a consequence of the work rather than by hand.

### 18.3 Validation at each gate

| Gate | Rule | Failure |
|---|---|---|
| step 2 | the window is `open` and has capacity | the control is disabled with the reason under it |
| step 2 | fewer than `3` live holds on one window | `This window is nearly full. Send an enquiry without holding it.` |
| step 4 | the four measured required fields are complete | Section 19.3 |
| step 4 | the budget band is chosen | Section 19.4 |
| step 4 | the hold has not expired | the enquiry is accepted without the window, and says so |
| step 9 | the proposal's dates fall inside the window | the studio's own validation, with the window's bounds shown |
| step 10 | the proposal has not expired | `That proposal has expired. Ask for a new one.` with a control |
| step 10 | the window still has capacity | `That window filled up. Here is what is open.` with the list |

### 18.4 The failure branches

| Branch | Behaviour |
|---|---|
| a hold expires while the visitor is writing | the form stays filled, a band appears naming the loss, and the submit still works without the window |
| two visitors hold the last capacity in one window | both holds are valid; capacity is committed at step 10, not at step 2, and the second to accept gets the Section 18.3 message with alternatives |
| the studio proposes into a window that filled meanwhile | the proposal form refuses with the window's current capacity shown |
| the client never replies | the enquiry becomes `lapsed` after `30` days, the hold is released, and nobody is mailed about it |
| the client withdraws | the enquiry becomes `withdrawn` and the hold is released immediately |
| mail fails at any step | the state change stands, Section 23.5 |

The second row is the important one. Holding capacity at enquiry time would let
one tyre-kicker block a month; committing at acceptance means the freelancer
never turns away real work for a hold that was never going to convert.

### 18.5 What a booking is not

It is not a contract, an invoice or a payment. This build takes no money. A
booking is a mutual agreement on a start date, recorded, with both parties
mailed. Everything commercial happens off this site, and Section 24.6 says so
explicitly so nobody builds an invoice into it by accident.

### 18.6 Layout

Every surface reuses measured parts: the underlined field (Section 13.2), the
numbered label, the pill (Section 5.3), the modal container at `20px`, the row
treatment of Section 11.2 for the pipeline. No new component.

> **In plain language.** This is what the whole booking half is for.
>
> Somebody looks at the work, checks the availability page, sees a window opening
> in six weeks, and presses start an enquiry. That holds the window for three
> days while they write. They fill in the same six questions the reference
> already asks, and send it. You see it arrive, read it, ask a question, they
> answer, and you propose a start date. They accept, and it is booked.
>
> The moment that happens, the green badge at the top of your site updates
> itself. That is the point of the entire exercise: the most valuable thing on
> your site stops being something you remember to edit.
>
> One decision took care. Holding a window does not actually commit any of your
> capacity: that only happens when somebody accepts a proposal. Otherwise one
> person who was never going to hire you could block a month of your calendar by
> filling in a form.
>
> And to be clear about scope: no money changes hands here. A booking is an
> agreed start date, written down, with both of you emailed. Contracts and
> invoices happen elsewhere.

---

## 19. Forms and validation **[extension]**

### 19.1 Field treatment

Taken directly from the measured contact form (Section 13.2).

| Element | Type | Colour on dark | Colour on lavender |
|---|---|---|---|
| the number | `.h3`, `32px` | `--c-paper` | `--c-purple` |
| label | `.body-m` | `--c-paper` | `--c-purple` |
| required mark | `.base` | measured as a separate element | as measured |
| input | `.body-m` | `--c-paper` | `--c-purple` |
| the rule under it | `1px` | `#ffffff26`, `--c-green` on focus | `#32146938`, `--c-purple` on focus |
| placeholder | `.body-m` | `--c-grey` | `--c-grey-cool` |
| helper | `.caption` | `--c-grey-cool` | `--c-grey-cool` |
| error | `.caption` | `--c-paper` on `#7631f58c` | `--c-purple` on `#3214691f` |
| submit | the measured pill at `50px` | as measured | as measured |

Fields are lines, not boxes, exactly as measured. There is no red in the
measured palette and none may be added: an error uses the measured purple
selection tint plus the words.

The focus rule on the dark ground is green, which is the availability colour.
That is the one place the green is allowed a second meaning, and it is allowed
because focus and availability never appear on the same element.

### 19.2 Validation timing

Validate on blur, never on keystroke. Re-validate on submit. A field that has
failed re-validates on keystroke until it passes. The submit is disabled only
until the form has been valid once.

### 19.3 The enquiry form

The six measured fields (Section 13.2), with their error copy:

| Field | Constraint | Error copy |
|---|---|---|
| `My Name` | 1 to 80 characters | `We need something to call you.` |
| `My Email` | a valid address | `We need an address to reply to.` |
| `I work at` | optional, up to 120 | `That is longer than we can store.` |
| `I am looking for` | 3 to 200 characters | `A few words about what you need.` |
| `My budget is` | one of the four bands | `Choose a range, even a rough one.` |
| `My message` | 20 to 4000 characters | `Tell us a little more, at least twenty characters.` |

### 19.4 Below the floor

The measured bands start at `$2000` (Section 13.3). A visitor whose project is
smaller has no option to choose, and an unanswerable form is worse than a
refusal.

**Requirement.** Under the select, a `.caption` line: `Smaller than that? Say so
in your message and we will point you somewhere good.` The band stays required,
the lowest band stays the floor, and nobody is left staring at a menu with no
answer in it.

### 19.5 The proposal form **[extension]**

Studio-side. Three fields and a note: a start date constrained to the window, a
length in weeks, a capacity in days per week constrained by what the window has
left, and a free note. The window's remaining capacity is shown live above the
form.

### 19.6 Pending and success

| State | Treatment |
|---|---|
| pending | the submit pill's border draws itself using the measured stroke transition, `0.4s`, and holds |
| success | the form is replaced by a `.h2` line and a control onward |
| failure | an error band above the submit, focus moves to it, and it is announced |

The pending state reuses the measured stroke draw (Section 6.6) rather than
introducing a spinner. This build has no spinner.

> **In plain language.** The form style is taken straight from the reference:
> numbered questions, each just a line to write on rather than a box.
>
> There is no red on this site, so mistakes are marked with the purple the site
> already uses for selected text, plus words saying what is wrong. Nothing
> complains while you type; it waits until you have moved on.
>
> One thing we are adding. The budget menu starts at two thousand dollars, so
> somebody with a smaller project has nothing they can honestly choose. We are
> putting a line underneath saying: smaller than that? Say so in your message and
> we will point you somewhere good. It costs one sentence and it turns a dead end
> into goodwill.
>
> When something is sending, the button's outline draws itself around, using the
> same drawing effect the rest of the site already uses. There is no spinner
> anywhere in this build.

---

## 20. Empty, loading, error and offline states **[extension]**

### 20.1 Empty

| Surface | `.h2` | `.base` | Action |
|---|---|---|---|
| `/availability` with no open window | `Fully booked right now.` | `The next opening is being scheduled.` | `Send an enquiry anyway` |
| `/account` with no enquiries | `Nothing here yet.` | `An enquiry appears here once you send one.` | `Start an enquiry` |
| `/studio/pipeline` with none | `The pipeline is clear.` | `Nothing waiting on you.` | none |
| an enquiry with no messages | the enquiry itself, with the reply field | none | none |
| `/work` with no projects | `No projects listed.` | `Get in touch to see recent work.` | `Contact` |

`Fully booked right now.` still offers an enquiry. A freelancer who is busy this
month is not busy forever, and the form is how the next month gets filled.

### 20.2 Loading

| Surface | Treatment |
|---|---|
| a route change | the route label enters with its measured `500px` transform, Section 5.5, which is the site's own loading gesture |
| the work index | nine pill-shaped placeholders in `#3214691f`, at the true stagger, not animated |
| the availability list | three row placeholders |
| any submit | Section 19.6 |
| the render layer | the hero renders from its measured gradient and halo immediately, Section 8.3, and the form arrives after |

Nothing shimmers. The site's motion vocabulary is drawn strokes and one easing
curve, and a pulsing skeleton belongs to neither.

### 20.3 Error, at the surface level

`.h2` reading `That did not load.`, a `.base` line naming what failed in
ordinary words, and a `Try again` pill that retries without a reload. The
chrome, the fixed rail and the ground stay.

The render context being unavailable is not an error and shows nothing
(Section 8.6).

### 20.4 Error, at the action level

A band above the control that failed, `.caption` on the measured purple tint,
with the retry inside it. Any optimistic change is rolled back first.

### 20.5 Not found, and not yours

One layout, identical copy for a missing object and a forbidden one:
`That is not yours to open.` under `/account` or `/studio`,
`We cannot find that.` on public routes.

An expired enquiry token gets its own surface: `That link has expired.` with the
sign-in offer of Section 16.4, because the visitor is holding something that
used to work.

### 20.6 Offline

| Condition | Behaviour |
|---|---|
| the connection drops | a band under the chrome reads `You are offline. Your draft is safe.` |
| the enquiry form is being filled | every keystroke is held locally; nothing is lost |
| submit is attempted | the control is disabled with the reason under it |
| the connection returns | the band clears and the submit re-enables; nothing is sent automatically |
| the tab is closed with a draft | the draft is restored on the next visit from the same browser |

The submit is never queued for automatic replay. An enquiry that sends itself
twenty minutes later, from a page nobody is looking at, is how somebody
accidentally sends a half-written brief.

> **In plain language.** Every list knows how to be empty, still loading, broken
> and offline.
>
> The best of these is what happens when you are fully booked: the page says so
> and still offers the form, because being busy this month is not being busy
> forever, and next month gets filled by the people who write to you now.
>
> Loading uses the site's own gesture, the route name sliding in, rather than
> inventing spinners. There is not one spinner in this build.
>
> If somebody loses their connection halfway through writing you a brief, every
> word is kept safely in their browser and the send button politely switches off
> until they are back. What it will not do is send by itself later: an enquiry
> that quietly posts a half-finished message twenty minutes after somebody walked
> away is a small disaster.

---

## 21. Search, filter and sort **[extension]**

### 21.1 What this site does not need

Nine projects. There is nothing to search, nothing to page and no facets worth
combining. Adding a search box to a list of nine is a control nobody will use,
and this build does not.

What does need controls is the studio pipeline.

### 21.2 The work index

Nine entries, all visible, in the studio's own order. One optional control, and
only if the count grows past `20`: a discipline filter drawn from the measured
credit lines, which carry `Design`, `Development` and `Design & Development`.

Until then the order is editorial and is a decision the owner makes, not a sort
the visitor applies.

### 21.3 The availability list

Three windows, all visible, in date order. No controls.

### 21.4 The pipeline **[extension]**

`/studio/pipeline`, the one list large enough to need controls.

| Parameter | Values | Default |
|---|---|---|
| `state` | the seven enquiry states, repeatable | `new`, `reading`, `proposed` |
| `q` | free text against name, organisation and message | none |
| `band` | the four measured budget bands, repeatable | none |
| `window` | a window id | none |
| `sort` | `newest`, `oldest`, `band` | `newest` |

Values inside one parameter combine with `or`, different parameters with `and`,
stated in words above the results when more than one is set.

The default hides `booked`, `declined`, `withdrawn` and `lapsed`, so the
pipeline opens on what needs an answer. Everything is one control away.

### 21.5 Search behaviour

Case-insensitive and accent-insensitive, which matters for a French-based
freelancer receiving names from anywhere. No fuzzy matching. The field updates
the address `300ms` after the last keystroke and replaces the history entry.

### 21.6 Sorting by band

`band` sorts by the measured budget bands in their measured descending order
(Section 13.3). That is the one sort a freelancer actually wants and it falls out
of the reference's own copy for free.

> **In plain language.** Nine projects. We are not adding a search box to a list
> of nine, and we are not adding filters to three available dates.
>
> The one place that needs controls is your own view of the enquiries. It opens
> showing only the ones waiting on you, hides the finished ones, and lets you
> narrow by budget band or by which window they are for. You can sort by budget,
> largest first, which is the sort you will actually use and which we got free
> from the four ranges already in your form.

---

## 22. Live and optimistic behaviour **[extension]**

### 22.1 What is optimistic

| Action | Applied before the server answers | Rolled back on failure |
|---|---|---|
| choosing a window on `/availability` | yes, the selection shows | yes |
| typing in the enquiry form | yes, entirely local | not applicable |
| the studio moving an enquiry's state | yes | yes, to its prior state |
| the studio's own note on an enquiry | yes | yes, text preserved |
| submitting an enquiry | no | not applicable |
| accepting a proposal | no | not applicable |
| creating or closing a window | no | not applicable |

Anything that changes what somebody has been promised is never optimistic.

### 22.2 The rule

An optimistic change renders immediately with no pending styling and is
confirmed silently. Only failure is visible.

### 22.3 The hold is the shared resource

Holds and capacity are the only thing two people can contend for
(Section 18.4). The rules, stated once:

- A hold is created optimistically and confirmed by the server. A refused hold
  rolls back and the reason is shown with the current capacity.
- Capacity is committed at acceptance, never at hold.
- A window's `committed_days` is only ever changed by the server, inside the
  same transaction that creates the booking.
- The client never computes remaining capacity for a decision. It displays what
  the server sent.

### 22.4 Rollback

A rollback restores the exact prior state, including the focused field and its
selection, and only then shows the failure band.

### 22.5 Live updates between sessions

| Change | Who sees it live | How |
|---|---|---|
| a new enquiry | the studio, with the pipeline open | a poll every `30s` while the tab is visible |
| a message on an enquiry | both parties on that enquiry | as above |
| a proposal accepted | the studio | as above |
| the availability state changing | anybody with a public page open | not live; on the next route change or load |

The last row is deliberate. Re-rendering the availability pill under a visitor
mid-sentence is worse than being a few minutes stale, and the pill is correct on
every fresh load.

### 22.6 Presence

There is none and none may be added.

> **In plain language.** Small things happen instantly: choosing a date, typing,
> moving an enquiry along your pipeline. If the server later refuses, it is
> quietly put back and only then do we say so.
>
> Anything that changes what somebody has been promised waits for a real answer:
> sending an enquiry, accepting a start date, opening or closing a window.
>
> The one thing two people can genuinely fight over is your calendar, so that has
> one rule: your capacity is only ever reduced by the server, at the moment
> somebody accepts, inside a single operation. The browser never works out what
> is left and acts on it. That is the difference between a booking system and a
> double-booking system.
>
> One deliberate exception: the availability badge does not update itself while
> somebody is reading the page. Having it change under their eyes mid-sentence is
> worse than being a few minutes out of date, and it is correct again the moment
> they load anything.

---

## 23. Notifications and transactional messages **[extension]**

### 23.1 In-app surfaces

Three, all built from measured tokens.

| Surface | Where | Treatment | Lifetime |
|---|---|---|---|
| band | under the chrome, full width | `.caption` on the measured purple tint | until the condition clears |
| inline confirmation | under the control that caused it | `.caption` in `--c-grey-cool` | `2s` |
| action band | above the control that failed | `.caption` on the measured purple tint | until dismissed or retried |

No floating toast. The site's chrome is already three layers deep
(Section 3.8), and a fourth thing arriving from a corner over a page with
fourteen scroll-driven effects would read as part of the choreography.

### 23.2 Band conditions, in priority order

| Priority | Condition | Copy |
|---|---|---|
| 1 | offline | `You are offline. Your draft is safe.` |
| 2 | a hold expired while writing | `Your hold on that window ran out. You can still send this.` |
| 3 | a proposal is awaiting the visitor | `You have a start date to confirm.` with a control |
| 4 | a proposal expires inside `48` hours | `That proposal expires soon.` |
| 5 | the studio has replied | `There is a reply on your enquiry.` with a control |

One band at a time, the highest priority wins.

### 23.3 Mail

| Trigger | To | Subject |
|---|---|---|
| enquiry submitted | the sender | `We have your enquiry` |
| enquiry submitted | the studio, and the second address of Section 17.4 | `New enquiry` and the budget band |
| studio replies | the sender | `A reply to your enquiry` |
| client replies | the studio | `A reply from` the organisation |
| proposal sent | the client | `A start date for your project` |
| proposal accepted | both | `Booked` and the start date |
| proposal expiring | the client, once, `48` hours before | `Your start date offer expires soon` |
| enquiry declined | the client | `About your enquiry` |
| enquiry lapsing | nobody | Section 18.4 |
| sign-in requested | the address | `Your sign-in link` |

Every mail is plain text with one primary link, sent from `<MAIL_SENDER>`,
carrying the enquiry id in its subject where one exists, and stating at its foot
which address it went to and why.

The confirmation mail carries the enquiry token link (Section 16.5) and the six
answers as submitted. That last part matters: it is the client's own copy of
what they asked for, and it settles arguments three months later.

### 23.4 What is never sent

No follow-up chasing an unanswered enquiry. No newsletter, because there is
none. No marketing derived from an enquiry, ever: somebody who told you their
budget and their employer in confidence has not opted into anything.

A lapsing enquiry is not mailed about (Section 18.4). If somebody has gone
quiet for thirty days, a reminder is a nudge nobody asked for.

### 23.5 Failure

Mail is sent after the state change commits. A failure never fails the action:
the enquiry is submitted, the page says so, and the send retries three times over
`30` minutes. If all three fail, the studio pipeline flags the enquiry
`Notification not delivered` and the client's page carries a `Send it again`
control.

> **In plain language.** Messages appear in three places: a strip under the
> header for something true right now, a small line under a button for something
> that just worked, and a strip above a button for something that just failed. No
> pop-ups.
>
> Emails are plain and short. The confirmation you send someone contains their own
> six answers written back to them, which is worth doing: it is their copy of what
> they asked for, and it settles disagreements months later.
>
> What we never send: reminders chasing people who went quiet, anything
> resembling marketing, and any use at all of what somebody told you about their
> budget or their employer. They told you that in confidence while asking about a
> job, not as a sign-up.

---

## 24. Data model and interface contract **[extension]**

### 24.1 Entities

| Entity | Fields |
|---|---|
| `project` | `id`, `slug`, `title`, `discipline`, `year`, `description`, `media_seed`, `link`, `position`, `state` |
| `window`, `hold`, `enquiry`, `message`, `proposal`, `booking` | Section 18.1 |
| `account` | Section 16.2 |
| `availability_state` | `id`, `mode`, `from_date` or null, `note`, `updated_at` |
| `site_meta` | `version`, `predecessor_label`, `predecessor_link`, `local_timezone` |
| `service` | `id`, `title`, `body`, `position` |
| `social_link` | `id`, `label`, `href`, `position` |

`site_meta` exists because the measured footer carries a version string, a
predecessor label and a timezone (Section 12.6). Those are content, not build
constants, and putting them in a deploy config is how the footer ends up lying
about which version is live.

`availability_state.mode` is one of the four in Section 15.2, and it is derived,
not typed: Section 24.6.

### 24.2 Relationships

| From | To | Cardinality |
|---|---|---|
| `window` | `hold` | one to many, at most `3` live |
| `window` | `booking` | one to many, bounded by `capacity_days` |
| `enquiry` | `message` | one to many |
| `enquiry` | `proposal` | one to many, at most one live |
| `enquiry` | `booking` | one to at most one |
| `account` | `enquiry` | one to many, and an enquiry may have no account |

An `enquiry` is never deleted. `withdrawn` and `declined` are states, because a
record of who asked and what happened is the freelancer's own history.

### 24.3 The read contract

| Method | Path | Request | Response | Codes |
|---|---|---|---|---|
| GET | `/api/projects` | none | `{items}` | `200` |
| GET | `/api/projects/<slug>` | none | `{project}` | `200`, `404` |
| GET | `/api/availability` | none | `{mode, from_date, windows}` | `200` |
| GET | `/api/enquiries/<id>` | token or session | `{enquiry, messages, proposal, booking}` | `200`, `401`, `404` |
| GET | `/api/me` | session | `{account, enquiry_count, booking_count}` | `200`, `401` |
| GET | `/api/meta` | none | `{version, predecessor, local_time}` | `200` |

`/api/availability` is the one request the public chrome makes, and it serves
both the pill and the availability page (Section 15.4).

### 24.4 The write contract

| Method | Path | Request | Codes |
|---|---|---|---|
| POST | `/api/holds` | `window_id` | `201`, `409`, `422` |
| DELETE | `/api/holds/<id>` | none | `204` |
| POST | `/api/enquiries` | the six measured fields, `hold_id` optional | `201`, `422`, `429` |
| POST | `/api/enquiries/<id>/messages` | `body` | `201`, `403`, `429` |
| POST | `/api/enquiries/<id>/accept` | `proposal_id` | `200`, `403`, `409`, `410` |
| POST | `/api/enquiries/<id>/withdraw` | none | `200`, `403` |
| POST | `/api/enquiries/<id>/proposals` | `starts_on`, `weeks`, `days_per_week`, `note`, studio only | `201`, `403`, `422` |
| PATCH | `/api/enquiries/<id>` | `state`, studio only | `200`, `403`, `422` |
| POST | `/api/windows` | `starts_on`, `weeks`, `capacity_days`, studio only | `201`, `403` |
| PATCH | `/api/windows/<id>` | `state` or capacity, studio only | `200`, `403`, `409` |
| POST | `/api/auth/link` | `email` | `202` always |
| GET | `/api/export` | studio only | `200`, Section 17.4 |

### 24.5 The error body

`{"error": {"code": "...", "message": "...", "field": "..." or null}}`

| Code | When | Surface |
|---|---|---|
| `unauthenticated` | no session and no valid token | route to sign-in |
| `forbidden` | wrong role or not the owner | Section 17.3 |
| `not_found` | no such object, or not visible | Section 20.5 |
| `token_expired` | a token past its life | the distinct surface, Section 20.5 |
| `validation` | a field failed | Section 19.1, against `field` |
| `window_full` | capacity was taken first | Section 18.3, with alternatives attached |
| `hold_lapsed` | the hold expired | Section 18.4, and the submit still proceeds |
| `proposal_expired` | acceptance after expiry | Section 18.3, with a control to ask again |
| `rate_limited` | Section 28.2 | the action band, wait in words |

`window_full`, `hold_lapsed` and `proposal_expired` are this build's three
specific codes. Each exists so that a timing collision has a name and an
onward action rather than becoming a generic error.

### 24.6 Availability is derived, not typed

**Capability requirement - normative.** `availability_state.mode` is computed
from the windows on every read:

| Condition | Mode |
|---|---|
| a window is `open` and starts within `14` days | open now |
| a window is `open` and starts later | open from its start date |
| every window is `booked` or `closed`, and one is booked | booked until the last booked window ends |
| no window exists | not taking new work |

A `note` may be set by the studio and is shown on the availability page, never in
the pill. The pill's words come from the model and cannot be typed over
(Section 15.4).

### 24.7 What this build never stores

No payment detail of any kind, no contract, no invoice, and no file upload. The
enquiry is six text fields (Section 18.5). Anybody adding an attachment field is
adding a storage, scanning and retention problem to a form that does not need
one.

> **In plain language.** The plumbing: what is stored and the exact list of
> requests the pages may make.
>
> Three decisions worth knowing. The green availability badge is worked out from
> your calendar every time it is shown, and cannot be typed over, which is what
> stops it going stale. The version number and the local time in your footer are
> content you can edit, not things buried in the code, because a footer that
> claims the wrong version is a small embarrassment that is annoying to fix. And
> enquiries are never deleted: declining or withdrawing changes their state,
> because who asked and what happened is your own history.
>
> One thing deliberately absent: there is no file upload anywhere. It is the
> obvious thing to add to a contact form and it brings virus scanning, storage
> costs and data-retention duties with it. Six text boxes do not.

---

## 25. Persistence and migration **[extension]**

### 25.1 What survives what

| Thing | Reload | New tab | New device | Signing out |
|---|---|---|---|---|
| the enquiry draft | yes | no, per browser | no | not applicable |
| a hold | yes, it is server-side | yes | yes, it is tied to the enquiry not the browser | yes |
| an enquiry and its thread | yes | yes | yes, by token or account | yes |
| a booking | yes | yes | yes | yes |
| the sound setting | yes | yes | no | yes |
| session | yes | yes | no | no |
| the pipeline's filters | yes, in the address | yes | yes, if shared | yes |

### 25.2 Browser storage

Three things: the enquiry draft, the sound setting, and the session cookie.
Nothing else. The draft is the only one that matters and it is the reason
Section 20.6 works.

### 25.3 Seed data

| Entity | Seeded |
|---|---|
| `project` | `9`, matching the measured titles, disciplines and years of Section 35.7 |
| `service` | `3`, the measured services of Section 10.4 |
| `window` | `3`, one open within `14` days, one open later, one closed |
| `availability_state` | derived from those, so a fresh install shows the open-now pill |
| `account` | one `studio`, one `client` with one enquiry |
| `enquiry` | one in `proposed`, with two messages and a live proposal |
| `site_meta` | the measured version and predecessor strings |
| `social_link` | `3` |

The seeded enquiry is deliberately in `proposed` with a live proposal, so that
the first thing anybody sees on a fresh install is the most interesting state in
the workflow rather than an empty pipeline.

### 25.4 Destructive actions

| Action | Effect | Confirmation |
|---|---|---|
| release a hold | immediate, undoable for `10s` | none |
| withdraw an enquiry | state change; nothing deleted | one confirmation |
| decline an enquiry | state change; the client is mailed | one confirmation, and the mail is not optional |
| close a window with holds on it | the holds are released and those enquiries are mailed | a typed confirmation of the window's start date |
| close a window with a booking on it | forbidden | the reason, in place |
| delete a project | forbidden while it is the only work shown; unpublish instead | one confirmation |
| delete an account | anonymises it, keeps enquiries with the organisation and no personal fields | a typed confirmation of the email |

Declining always mails the client. A freelancer who declines silently is a
freelancer somebody is still waiting on, and this build does not allow it.

### 25.5 Retention

| Data | Kept |
|---|---|
| an enquiry and its thread | `3` years, then anonymised |
| a booking | indefinitely |
| an enquiry draft | until sent, or `30` days in the browser |
| a sign-in link | `30` minutes |
| an enquiry token | `90` days |

Three years on an enquiry is a deliberate number: long enough to remember a
client who comes back, short enough that a form collecting names, addresses and
employers is not held forever. The privacy notice (Section 15.5) states it.

### 25.6 Migration

| Migration | Backfill |
|---|---|
| `enquiry.window_id` introduced | existing enquiries get null; they predate windows |
| `availability_state` introduced | derived on first read; nothing is typed |
| `site_meta` introduced | seeded from the measured footer strings |
| `hold.expires_at` introduced | every existing hold expires immediately, releasing capacity |

> **In plain language.** What is kept and where. Enquiries, bookings and
> conversations live on the server and are there on any device. The only thing
> living in somebody's browser is the half-written message they have not sent
> yet, which is exactly the thing that must not be lost.
>
> Enquiries are kept for three years, then stripped of personal details. Long
> enough to recognise a client who comes back, short enough that a form
> collecting names, emails and employers is not hoarding them forever. Your
> privacy page says so.
>
> One rule is not negotiable: declining an enquiry always emails the person.
> Declining quietly leaves somebody waiting on you for weeks, and the site will
> not let you do it.
>
> And a small touch: a fresh install arrives with an example enquiry already
> waiting with a start date offered, so the first thing you see is the
> interesting part of the system working rather than an empty screen.

---

## 26. Internationalisation and formatting **[extension]**

### 26.1 What was measured

An English site by a France-based freelancer, with a French flag in the hero
(Section 9.3), `Located in France` twice, a local clock at `GMT+2`
(Section 12.6), and budget bands denominated in `USD` (Section 13.3).

That combination is measured and is worth stating plainly: the site is in
English, priced in dollars, and located in France, because its clients are
international and its author is not.

### 26.2 The site's language

One, English. A French translation is the obvious extension and is not specified
here, because the measured evidence gives no French copy at all and inventing it
would be inventing a voice.

What is specified is that nothing blocks it: every measured string is in the
copy deck (Section 35), no string is baked into a drawing except the wordmark
(Section 4.7), and the display face is used for the name rather than for prose.

### 26.3 The clock

The measured footer clock is his local time with an explicit offset, not the
visitor's.

**Capability requirement - normative.** The clock renders the studio's timezone
from `site_meta.local_timezone`, ticks every minute rather than every second,
and always shows its offset. A clock without an offset is ambiguous, and a clock
showing the visitor their own time is pointless.

It must survive a daylight-saving change without a deploy, which is why it is a
timezone name and not a stored offset. The measured `GMT+2` is the rendered
output in summer, not the stored value.

### 26.4 Formatting

| Value | Form |
|---|---|
| the clock | `01:59 PM GMT+2`, as measured, twelve-hour with the offset |
| project years | four digits, as measured, `© 2026` |
| window dates | `12 March 2026`, unabbreviated |
| budget bands | as measured, `USD $5001-$10000`, currency named |
| durations | in weeks, as an integer |

Budget bands are reproduced exactly as measured, including the currency prefix
on every option. A freelancer quoting across borders who omits the currency
invites a misunderstanding that costs real money.

### 26.5 Timezones in the workflow

A proposal carries a start date, not a start time, so no timezone conversion is
needed for the booking itself. Where a call is proposed in a message, the
message states the timezone in words; the build does not attempt to convert it,
because a conversion the sender cannot see is a conversion nobody trusts.

### 26.6 If the site is translated

The measured display type is set solid at `1` line-height above `--text-5xl`
(Section 3.6), and the about statement is `69` words at `97.5px`. French runs
roughly `15%` longer. The rule is one extra line permitted per block, reviewed at
all three measured breakpoints, and the about statement reviewed as a whole
because its shadow reveal is per word (Section 6.4) and a longer statement takes
proportionally longer to reveal.

> **In plain language.** The site is in English, prices in dollars, and says
> twice that he is in France. That is a deliberate combination: the clients are
> international, so the site speaks their language and quotes their currency,
> while being honest about where the work happens.
>
> The clock in the footer shows his time, not yours, with the offset written out.
> That is right: what a client wants to know is what time it is where you are, so
> they know whether to expect a reply today.
>
> One implementation note: store the place, not the offset. Store Paris, not plus
> two, or the clock will be an hour wrong for half of every year and somebody
> will have to remember to fix it.
>
> A French version would be the obvious next step. Nothing here blocks it, but we
> have not written it: every word on the site is his voice, and inventing a French
> version of somebody's voice is not our job.

---

## 27. Analytics and instrumentation **[extension]**

### 27.1 Events

| Event | Fires from | Properties |
|---|---|---|
| `page_view` | a route change | `route` |
| `section_enter` | a home section reaching the frame | `section` |
| `scroll_depth` | crossing each fifth of a document | `route`, `fifth` |
| `work_open` | a project modal opening | `slug`, `source` in `home`, `work` |
| `availability_view` | `/availability` | `open_window_count` |
| `hold_created` | Section 18.2 step 2 | `window_id`, `days_until_start` |
| `enquiry_started` | the first keystroke in the form | `has_window` |
| `enquiry_submitted` | step 4 | `budget_band`, `has_window`, `message_length` |
| `enquiry_abandoned` | the draft is `30` days old, unsent | `furthest_field` |
| `proposal_sent` | step 9 | `days_from_enquiry` |
| `proposal_accepted` | step 10 | `days_from_proposal` |
| `enquiry_declined` | Section 25.4 | none |
| `sound_toggled` | Section 14.4 | `to` |
| `render_degraded` | Section 8.6 | `stage` |
| `motion_reduced` | first render | `true` or `false` |

### 27.2 What is never a property

The name, the email address, the employer, the `I am looking for` text, the
message body, and any part of a thread. `message_length` is recorded;
`message` never is.

`enquiry_abandoned` records which field somebody stopped at, and nothing they
typed. That distinction is the whole of this section: knowing that people give
up at the budget question is a product insight, and knowing what they typed
before giving up is surveillance.

### 27.3 Consent

`render_degraded` and `motion_reduced` carry no identifier and fire before
consent. Everything else waits.

The reference showed no consent surface in any captured frame while operating an
analytics vendor and a contact form (Section 37.6). This build ships one, and
the enquiry form works fully before it is answered: a form is not analytics.

### 27.4 The four numbers that matter

| Metric | Why |
|---|---|
| `enquiry_submitted` against `enquiry_started` | the form's completion rate. On a one-page funnel this is the whole business |
| `enquiry_abandoned` by `furthest_field` | which question loses people. If it is the budget question, the bands are wrong |
| `enquiry_submitted` by `budget_band` | whether the floor at `$2000` is filtering correctly or just filtering |
| `hold_created` against `enquiry_submitted` | whether picking a window helps people finish, which is the one thing this extension claims |

The last is the honest test of Section 18. If holding a window does not raise
completion, the feature is decoration and should be removed.

### 27.5 Performance instrumentation

The frame rate of the render layer as a rolling median over `5s`, the time until
the hero name is readable, and the count of degradation steps. No identifiers.

> **In plain language.** We count what people do, never what they wrote. We
> record that somebody sent an enquiry, which budget range they picked and how
> long their message was. We never record the message, their name, their email or
> their employer.
>
> One distinction is the point of this whole section. If somebody starts your form
> and gives up, we record which question they stopped at and nothing they typed.
> Knowing that people abandon at the budget question tells you your ranges are
> wrong, and that is useful. Knowing what they typed before they left is spying.
>
> Four numbers matter. How many people who start the form finish it, because on a
> site like this that is the entire business. Which question loses them. Which
> budget ranges you actually attract. And whether letting somebody pick a project
> window actually makes them more likely to finish, which is the honest test of
> the biggest thing we are adding. If it does not, take it out.

---

## 28. Security and abuse **[extension]**

### 28.1 Authorisation, per write

Three questions on the server for every write: is there a session or a valid
token, does the role permit it, and does this account or token own the object.

| Path | Owner check |
|---|---|
| `/api/enquiries/<id>` and below | the enquiry token matches, or the session account owns it, or the role is `studio` |
| `/api/enquiries/<id>/accept` | the token or the owner, never the studio; a freelancer cannot accept on a client's behalf |
| `/api/enquiries/<id>/proposals` | `studio` only |
| `/api/windows` | `studio` only |
| `/api/export` | `studio` only |

The second row is a deliberate asymmetry. The studio proposes; only the client
accepts. A booking the client did not press is not a booking.

### 28.2 Rate limits

| Action | Limit | Response |
|---|---|---|
| enquiry submission per address block | `5` per hour | `429`, wait stated in words |
| enquiry submission per email | `3` per day | `429` |
| holds per address block | `5` per hour | `429` |
| messages per enquiry | `30` per hour | `429` |
| sign-in link per email | `3` per hour | `202` regardless, only the first sends mail |
| any read | `600` per minute per address block | `429` |

The enquiry form is the abuse surface: it is public, it sends mail, and it has a
free-text field. Those first three limits are what stop it becoming a relay.

### 28.3 The form is the attack surface

| Rule | Requirement |
|---|---|
| the message is capped at `4000` characters server-side | Section 19.3 |
| every field is stored and rendered as plain text | no markup is interpreted anywhere in this build |
| the reply-to on notification mail is the site's own address, never the submitted one | otherwise the form is a spoofing relay |
| the submitted address is never echoed into a mail header | only into the body |
| no link in a submitted message is fetched, previewed or unfurled by the site | so a submission cannot make the server call a stranger |
| a spam signal holds the enquiry for review rather than dropping it | a false positive that silently eats work is worse than a little spam |

The last row matters more here than on any other site in this kit. This form is
the business. An over-eager filter that silently discards a real enquiry costs a
project.

### 28.4 Tokens

| Token | Life | Reuse |
|---|---|---|
| sign-in link | `30` minutes | single use |
| enquiry token | `90` days | reusable, read and reply only |
| proposal acceptance | tied to the enquiry token | single use, and expiry checked server-side |

The enquiry token is deliberately long-lived and reusable (Section 16.5). It is
bounded by carrying no capability beyond that one enquiry, and by never granting
account access.

### 28.5 Session handling

Session cookies are `HttpOnly`, `Secure`, `SameSite=Lax`, rotated on sign-in.
Every state-changing request carries a token checked against the session.

### 28.6 What a hostile input renders as

| Input | Rendered |
|---|---|
| a message containing markup | the characters, uninterpreted |
| a name of `10000` characters | rejected at `80` with the validation message |
| a header injection attempt in the email field | rejected by address validation; newlines never reach a header |
| a hold request on a closed window | `409` with the current windows attached |
| an acceptance replayed after booking | `409`, and the existing booking is shown |
| an enquiry id of the wrong shape | `404`, never a parse error |

### 28.7 What this build does not defend against

A determined spammer with many addresses, which is why Section 28.3's last row
prefers review over silent deletion. A client forwarding their enquiry link,
which is a feature. And the single-operator account risk, which is Section 17.4
and is a process problem rather than a software one.

> **In plain language.** Every change asks three questions again on the server:
> are you who you say, is your kind of account allowed, and is this thing yours.
>
> One asymmetry is deliberate: you can offer a start date, but only the client can
> accept it. A booking they did not press is not a booking.
>
> The contact form is the thing to protect, because it is public, it sends email,
> and it has a free text box. It is rate limited, everything anybody types is
> stored and shown as plain characters, and no link somebody submits is ever
> visited by your site.
>
> The most important rule in this section: if something looks like spam, it is
> held for you to look at rather than deleted. On a shop, an over-keen spam filter
> costs you an order. Here it costs you a project, and you never find out it
> happened.

---

## 29. Module and component architecture

### 29.1 The layer boundary

Five layers, and a dependency may only point downward:

| Layer | Contains | May reach |
|---|---|---|
| routes | one module per Section 2.2 path | sections, interface, state, platform |
| sections | the home sections and the three route bodies | interface, state, platform |
| interface | everything in Section 29.2 | state, platform |
| state | availability, the enquiry draft, the session, the scroll position | platform |
| platform | the scroll driver, the render layer, the audio graph, the transport | nothing |

Availability is a state-layer concern, not an interface one. The pill
(Section 5.3) subscribes to it; it does not fetch it. That single boundary is
what makes Section 15.4's promise, one source for the pill and the page,
enforceable rather than aspirational.

### 29.2 The component set

| Component | Used by | Notes |
|---|---|---|
| `Pill` | the availability signal, every control, the work index | Section 5.3, `50px` and `10px` radii |
| `Mark` | seven marks | Section 4, stroked, `currentColor` |
| `Monogram` | the lockup, the card ornament | Section 4.2, two sizes |
| `SectionTitle` | both home sections | Section 10.1, two words, the asterisk, the drawn underline |
| `ShadowWords` | the about statement | Section 6.4, per word with a twin |
| `SplitLetters` | the work headline | Section 12.1, per character |
| `StrokeDraw` | the burger, the underline, the arc, the pending state | Section 6.6, one implementation |
| `Sheet` | every section transition | Section 7.4, one-sided radii and the light line |
| `CardStack` | the about section | Section 7.5, the scrubbed transform and the tinted shadow |
| `WorkRow` | home preview, work index, pipeline | three densities, Section 29.3 |
| `NumberedField` | every form | Section 13.2, Section 19.1 |
| `Cursor` | the work index | Section 5.7 |
| `Rail` | every route | Section 5.6, fixed, two badges |
| `Clock` | the footer | Section 26.3, ticks per minute |
| `Band` | Section 23.1 | one at a time, priority-ordered |
| `StateBlock` | every list | Section 20, the five states |
| `WindowCard` **[extension]** | availability, the enquiry head | the `Pill` and the `WorkRow` combined |

Seventeen components. An eighteenth is a design decision and belongs in this
table before it is built.

### 29.3 One row, three densities

| Density | Where | Difference |
|---|---|---|
| rule | the home preview, Section 11.2 | title left, credit right, rules above and below |
| pill | the work index, Section 12.2 | a solid title pill and a separate credit pill, staggered |
| record | the studio pipeline | title, state, band, window, date |

All three are `WorkRow`. The home preview and the work index draw the same nine
records (Section 11.3), and building them separately is how they drift.

### 29.4 State

| Store | Holds | Lives |
|---|---|---|
| availability | the mode, the windows | memory, hydrated from one request, Section 24.3 |
| draft | the six enquiry fields | memory, mirrored to browser storage |
| session | account and role | memory, hydrated from `/api/me` |
| scroll | the normalised position, the active section | memory |
| sound | on or off | memory, mirrored to browser storage |
| pipeline query | the Section 21.4 parameters | the address, never duplicated |

### 29.5 The scroll driver

One instance, platform-owned, exposing a normalised position and a per-element
progress subscription. The fourteen scrubbed selectors of Section 7.3 subscribe;
none attaches its own listener. The booking routes instantiate no driver
(Section 7.8).

> **In plain language.** Five layers, each depending only on the one below.
>
> The one that matters most: the green availability badge does not go and fetch
> its own answer. It subscribes to a single shared source that the availability
> page also uses. That is a boring-sounding rule and it is the only thing that
> actually guarantees the badge and the page can never disagree with each other.
>
> Seventeen reusable parts, listed by name. The project row is one part used three
> ways: as a simple line on the home page, as a scattered pill on the work page,
> and as a record in your own pipeline. Same nine projects underneath, so they
> cannot drift apart.

---

## 30. Responsive behaviour

### 30.1 The measured breakpoints

Twenty distinct media queries were measured, which is the largest set in this
kit's corpus and is a sign of a layout tuned by hand rather than by a system.

| Query | Count | Role |
|---|---|---|
| `(max-width: 690px)` | 21 | the mobile switch, by far the most used |
| `(min-width: 690px)` | 5 | its complement |
| `(min-width: 1500px)` | 4 | the wide-desktop switch |
| `(max-width: 1293px)` | 3 | a layout-specific correction |
| `(min-width: 1300px)` | 3 | its complement |
| `(max-width: 900px)`, `(max-width: 946px)`, `(max-width: 944px)`, `(min-width: 945px)`, `(max-width: 980px)` | 2 or 1 each | five queries within `80px` of each other |
| `(max-width: 780px)`, `(max-width: 789px)`, `(min-width: 790px)` | 1 or 2 each | three queries within `10px` of each other |
| `(max-width: 520px)`, `(max-width: 400px)` | 2 each | small-phone corrections |
| `(min-width: 40rem)`, `(min-width: 48rem)`, `(min-width: 64rem)` | 2 each | the utility layer's own scale |
| `(max-width: 1200px)` | 1 | one correction |

### 30.2 This is a defect worth fixing

Five queries between `900px` and `980px`, and three between `780px` and `790px`,
are not a design system. They are individual fixes applied where something broke,
and they will keep multiplying.

**Capability requirement - normative.** This build declares four breakpoints and
no others:

| Name | Width | Derived from |
|---|---|---|
| `sm` | `520px` | measured |
| `md` | `690px` | measured, the dominant switch |
| `lg` | `946px` | measured, the centre of the `900` to `980` cluster |
| `xl` | `1500px` | measured |

Every measured near-duplicate collapses into the nearest of these. A layout that
needs `789px` specifically is a layout with a bug at `790px`.

### 30.3 The matrix

| Surface | below `md` | `md` to `lg` | `lg` to `xl` | `xl` and above |
|---|---|---|---|---|
| chrome navigation | burger | burger | four stacked links | four stacked links |
| the name lockup | monogram only | full | full | full |
| availability pill | centred, shortened | centred | centred | centred |
| the hero name | `.display-s` | `.display-xs` | `.display-l` | `.display-l` |
| the about statement | `.h1` | `.h3` | `.display-xl` | `.display-xl` |
| the work index | one column, no stagger | one column | staggered pills | staggered pills |
| the project view | the measured mobile panel at `20px` | the panel | the modal | the modal |
| the fixed rail | hidden | hidden | shown | shown |
| the contact form | one column | one column | form left, details right | form left, details right |
| the tool band | scrolls, `4` visible | `8` visible | `14` visible | `14` visible |
| the card stack | static, stacked | static | scrubbed | scrubbed |

The rail is hidden below `lg`, which is measured by its absence from the mobile
screenshots. Two award badges are not worth `53px` of a phone screen.

### 30.4 The staggered work index

The measured `200px` horizontal stagger (Section 12.2) is the work index's whole
character and it cannot survive a narrow screen: at `520px` a `200px` offset is
`38%` of the frame.

Below `md` the pills stack in one column, left-aligned, in date order, with the
credit pill directly under each title pill. Nothing is lost but the scatter.

### 30.5 Touch

| Behaviour | Below `lg` |
|---|---|
| the custom cursor | not rendered; a pointer device is required for it |
| the `View` label | becomes a visible control on each row |
| grayscale media | takes colour on entering the frame rather than on hover |
| every control | minimum `44px` touch target, achieved with padding |
| the tool band | scrolls on touch, and does not auto-scroll while touched |

The third row matters: a grayscale-to-colour effect tied only to hover is
invisible on a phone, and this build ties it to visibility instead.

> **In plain language.** We found twenty different screen-width rules in the
> reference, including five that fire within eighty pixels of each other and
> three within ten pixels. That is not a system; it is a pile of individual
> fixes, and it will keep growing.
>
> We are declaring four and collapsing everything into them. A layout that needs
> a rule at exactly 789 pixels is a layout that is broken at 790.
>
> The one thing that genuinely changes on a phone is the work page. On a computer
> the nine projects are scattered across the page at different offsets, which is
> the page's whole character. On a narrow screen that offset is nearly half the
> width, so they stack in a single tidy column instead. Nothing is lost but the
> scatter.
>
> And the pictures that turn from grey to colour when you point at them: on a
> phone there is no pointing, so they take their colour as they come into view
> instead. An effect that only exists on a mouse is an effect half your visitors
> never see.

---

## 31. Accessibility

### 31.1 Contrast, computed from the measured tokens

| Foreground | Ground | Ratio | Verdict |
|---|---|---|---|
| `#ffffff` | `#141516` | `18.6:1` | headings and body on the dark |
| `#e5e7eb` | `#141516` | `15.0:1` | the inherited body colour |
| `#ffffff` | `#321469` | `14.7:1` | text on the solid purple pill |
| `#321469` | `#e7d8ff` | `11.0:1` | text on the lavender |
| `#9ba2af` | `#141516` | `7.3:1` | secondary text on the dark |
| `#219653` | `#141516` | `4.9:1` | the availability text, and the focus rule |
| `#6c6c6c` | `#141516` | `3.6:1` | **fails for body text**, Section 31.2 |
| `#219653` | `#e7d8ff` | `2.8:1` | **forbidden**, green is never on lavender |
| `#9ba2af` | `#e7d8ff` | `1.9:1` | **forbidden**, the cool grey is never on lavender |

### 31.2 The placeholder failure, and the fix

`#6c6c6c` at `3.6:1` is the measured placeholder colour on the dark ground. It
is below the threshold for body text, and on the measured contact form the
placeholders carry meaning: they are worked examples showing the expected format
(Section 13.2).

| Token | Reference use | This build |
|---|---|---|
| `--c-grey` | placeholders on dark | `#9ba2af` at `7.3:1`, already in the palette |

A placeholder that a visitor cannot read is not a hint, and on this form the
hints are the only guidance there is.

### 31.3 The green carries meaning

`#219653` passes on the dark ground at `4.9:1` and fails on lavender at `2.8:1`.
Since the availability pill only ever sits on the dark chrome, the measured use
is safe.

But availability is also signalled by the dot alone in some states
(Section 15.2). **Requirement:** the state is always in the pill's words, never
in the dot's colour alone. Somebody who cannot distinguish the green from the
grey reads the sentence and gets the same answer.

### 31.4 Focus

Visible on every interactive element: `2px` `--c-green` at `2px` offset on the
dark ground, `2px` `--c-purple` on the lavender. Never removed.

Focus is not hover. The measured grayscale and cursor effects are hover
treatments; focus is the ring, and both must be able to happen at once.

### 31.5 The two split treatments

The about statement is split per word with shadow twins (Section 6.4); the work
headline is split per character (Section 12.1). Both are unusable to assistive
technology as split elements.

**Requirement.** In both cases the split elements are hidden from the
accessibility tree and the original string is present in one node, in reading
order. A `69`-word statement read out word by word with a duplicate shadow copy
of every word is the worst possible outcome, and it is what happens by default.

The shadow twins are doubly important here: without this rule a screen reader
reads the entire statement twice.

### 31.6 The sound control

Measured copy is `Sound | OFF` (Section 14.4). The visible string states the
current state; the accessible name states the action, `Turn sound on`. Those are
different strings and both are required. A control whose accessible name is its
current state tells somebody what is, not what pressing it will do.

### 31.7 Sound never carries information alone

Twenty-one cues (Section 14.3), and sound is off by default for most visitors.
Every cue has a visible equivalent. No state, confirmation or error is signalled
by sound alone.

### 31.8 The scroll-driven document

Fourteen scrubbed selectors (Section 7.3). Three requirements:

- Content revealed by scroll is present in the document from the start, not
  inserted on reveal, so it is reachable by search and by assistive technology
  regardless of scroll position.
- Focus brings its element into the frame.
- Under reduced motion, everything is at its final state and the document
  scrolls natively (Section 6.10).

### 31.9 The custom cursor

Rendered only where a fine pointer exists (Section 30.5), and it never replaces
a real control: the `View` label names an action that is also on the row itself.
A cursor is decoration, and decoration cannot be the only affordance.

> **In plain language.** We computed every colour pairing on this site. Most are
> excellent. One fails: the grey used for the example text inside the contact
> form fields is too faint to read against the dark background. That matters more
> than usual here, because those examples are the only instructions the form
> gives you. We have replaced it with a lighter grey already on the site.
>
> Two rules follow from the palette. The green is only ever used on the dark
> background, never on the lavender, where it becomes unreadable. And whether he
> is available is always written in words, never signalled by the colour of the
> dot alone, so somebody who cannot tell green from grey still gets the answer.
>
> The most important fix in this section is invisible. The big paragraph about
> him is built from sixty-nine separate words, each with a ghost copy behind it.
> To screen-reading software that is a hundred and thirty-eight fragments, and it
> would read the whole paragraph twice, one word at a time. The words have to be
> hidden from it and the real sentence given instead.

---

## 32. Performance

### 32.1 Budgets

| Surface | First text readable | Interactive | Transferred, first view |
|---|---|---|---|
| `/` | `1.2s` | `2.2s` | `900KB` |
| `/work` | `1.0s` | `1.8s` | `600KB` |
| `/contact` | `0.9s` | `1.5s` | `450KB` |
| `/availability` | `0.9s` | `1.5s` | `400KB` |
| `/studio/pipeline` | `1.0s` | `1.8s` | `500KB` |

Measured on a four-times-throttled processor and a `1.6Mbps` connection.

### 32.2 Frame budget

The render layer holds `60` frames per second at `lg` and above and `30` below
`md`, as a rolling median over `5s`. Below the floor for `3s`, the ladder in
Section 8.6 takes one step and the step is reported.

The fourteen scrubbed selectors (Section 7.3) are the real risk here, not the
render layer. Every one must read from the single scroll driver
(Section 29.5) and write only transform and opacity.

### 32.3 The measured cost

From the ledger: `1753` script files totalling `9.94MB`, `225` font files at
`3.0MB`, `26` further font files at `355KB`, and `21` audio files at `1.57MB`.

Two of those numbers are problems.

**`225` font files.** Three families at three weights should be at most nine
files, or three with variable cuts. `225` is a per-glyph or per-subset split
shipped in full. Section 32.4 fixes it.

**`1753` script files.** That is a development-mode module graph, not a
production bundle. Whatever the build does, it should not ship seventeen hundred
requests.

Neither is a design decision and both are recorded as defects (Section 37.6).

### 32.4 The font budget

**Capability requirement - normative.**

| Order | Loaded | Blocking |
|---|---|---|
| 1 | the working face, regular, subset to Latin | yes, with the measured metrics-matched fallback |
| 2 | the working face, bold | no |
| 3 | the display face, subset to the strings that use it | no, before the hero paints |
| 4 | any further subset | on demand |

The display face is used for the name, the eyebrow and two section titles: a few
dozen distinct characters. Subsetting it to those is the single largest saving
available on this site.

The measured `Fallback` faces (Section 3.4) are already correct and must be kept:
they are why the page does not reflow when the real faces arrive.

### 32.5 The transition on `all`

`6131` declarations (Section 6.3). Beyond being a correctness problem, a
transition on `all` forces the engine to watch every animatable property on every
one of those elements. Replacing it with the twelve named declarations is both
the correctness fix and a measurable performance fix.

### 32.6 What is deferred

| Deferred | Until |
|---|---|
| the render layer | the hero text is readable |
| the audio graph and every cue | sound is switched on |
| the tool band's marks | the about section is within one frame |
| project media | the row is within one frame |
| the booking routes' code | an enquiry or availability control is pointed at |

Sound is `1.57MB` and is off by default (Section 14.2). Loading it for the
majority who never turn it on would be the largest wasted transfer on the site.

> **In plain language.** How fast this has to be: the first words in just over a
> second, the page usable in two.
>
> Two numbers in the reference need fixing and neither is a design decision. It
> loads two hundred and twenty-five separate font files, where three typefaces in
> three weights should be nine at most. And it makes seventeen hundred separate
> requests for code, which is what a site looks like while a developer is working
> on it, not what it should look like when it is published.
>
> The biggest single saving available: the tall display typeface is used for
> about four dozen letters in total, on his name and two headings. Shipping only
> those letters rather than the whole alphabet is nearly free to do and makes the
> first screen noticeably faster.
>
> And the sound is a megaphone and a half of audio that most visitors will never
> turn on. It does not load until they do.

---

## 33. Build order

| Step | Build | Demonstrable when | Closed by |
|---|---|---|---|
| 1 | tokens, the type scale, the pill, the seven marks | a page of every component at every state | Section 3, Section 4 at four widths |
| 2 | the four breakpoints, replacing the twenty | the same page, correct at every width | Section 30.2 |
| 3 | the scroll driver and the sheet transition | two sections slide over each other with the light line | Section 7.4 |
| 4 | the chrome, the rail, the availability pill against a stub | every route carries the chrome and a pill that reads a value | Section 5 |
| 5 | the hero, with the measured gradient and halo only | the hero, complete, with no render layer | Section 8.3, Section 9 |
| 6 | the stroke-draw system | the burger, the underlines and the arrows draw themselves | Section 6.6 |
| 7 | the about section and the shadow reveal | sixty-nine words rising over their twins under scroll | Section 6.4 |
| 8 | the work index, seeded | nine projects, staggered, with the cursor and the modal | Section 12 |
| 9 | the contact form | six numbered fields, validated, submitting to a stub | Section 13, Section 19 |
| 10 | the render layer with a generated substitute | the blue form behind the name | Section 8, Section 36.3 |
| 11 | windows, holds, and the availability page | the pill reads from real windows | Section 15, Section 24.6 |
| 12 | the enquiry pipeline and mail | Section 18.2 steps 1 to 8 | Section 18.3 |
| 13 | proposals and bookings | steps 9 to 12, including the pill updating itself | Section 18.2 |
| 14 | accounts and the studio view | Section 16, Section 17 |
| 15 | states: empty, loading, error, offline | every surface in five states, forced | Section 20 |
| 16 | sound | twenty-one cues, off by default, with the control | Section 14 |
| 17 | instrumentation and consent | events visible, form working before consent | Section 27.3 |
| 18 | the accessibility pass | contrast, the split-text fix, focus into frame | Section 31 |
| 19 | the performance pass | the font subset, the named transitions, the budgets | Section 32 |

Step 2 before anything visual is deliberate: collapsing twenty breakpoints into
four is cheap on day one and expensive once nine sections have been built
against the old set.

Step 5 before step 10 is also deliberate. The hero is complete and shippable
from stylesheet values alone (Section 8.3), so the render layer can be judged as
an addition rather than assumed as a foundation.

Steps 1 to 9 are the site. Steps 11 to 14 are the product. Steps 15 to 19 are
what makes it shippable.

> **In plain language.** What gets built when.
>
> Two decisions in the order are worth defending. First, we sort out the screen
> sizes before building anything you can look at. Collapsing twenty width rules
> into four costs an afternoon now and costs a fortnight once nine sections have
> been built on top of the old ones.
>
> Second, the hero gets built without the blue three-dimensional shape behind it,
> because we measured that the dark gradient and violet glow do most of the work
> on their own. That way the shape is judged as something added on top rather
> than assumed to be load-bearing, and the fallback for machines that cannot draw
> it is something we have actually looked at.
>
> After that: the drawing effects, the paragraph with its ghost words, the work
> page, the contact form. That is the public site. Then the calendar, the
> enquiries, the proposals, and the moment the green badge starts updating itself.

---

## 34. Test plan **[extension]**

Assertions are on text and state, never on pixels or screenshots.

### 34.1 The primary workflow, end to end

| Step | Do | Assert |
|---|---|---|
| 1 | open `/` | text `Creative Developer` and `available now for work` are present |
| 2 | open `/availability` | at least one window is listed with a date |
| 3 | press `Start an enquiry` on the first window | the address is `/contact`, the window's date is present at the head of the form, and a hold exists |
| 4 | submit with no budget band | text `Choose a range, even a rough one.` is present and the address is unchanged |
| 5 | complete all six fields and submit | the address matches `/enquiry/`, and the six submitted answers are present on the page |
| 6 | open the same address in a new browser with the token | the enquiry is present |
| 7 | open it without the token | text `That is not yours to open.` is present |
| 8 | as the studio, open `/studio/pipeline` | the enquiry is present in the `new` group with its budget band |
| 9 | open it | the enquiry state reads `reading` |
| 10 | reply | the client's enquiry page shows the reply |
| 11 | propose a start date inside the window | the enquiry state reads `proposed` |
| 12 | as the client, accept | the state reads `booked` |
| 13 | reload `/` | the availability pill text reflects the new capacity, per Section 15.2 |

Step 13 is the assertion this entire extension exists for.

### 34.2 Capacity and timing

| Do | Assert |
|---|---|
| create two holds on a window with one day of capacity, accept both proposals | the first succeeds; the second shows text `That window filled up.` and lists alternatives |
| expire a hold while the form is open, then submit | the enquiry is created, the hold is absent, and text naming the loss is present |
| accept a proposal after its expiry | text `That proposal has expired.` is present and no booking exists |
| close a window that has a booking | the action is refused and the reason is present |
| leave an enquiry `31` days | its state reads `lapsed` and no mail was sent |

The first row is the one that protects the calendar and it must be run
concurrently, not in sequence.

### 34.3 The form

| Do | Assert |
|---|---|
| open `/contact` and read the placeholders | no placeholder contains a real person's name or a real company address |
| submit a message of `19` characters | the length error is present |
| submit with markup in the message | the enquiry page shows the characters, uninterpreted |
| submit six times in one hour from one address | the sixth is rate limited and the wait is stated in words |
| start the form, go offline, type, come back online | every character typed is still present and the submit re-enables |
| go offline and press submit | the control is disabled and the reason is present |

### 34.4 Availability integrity

| Do | Assert |
|---|---|
| set every window to `closed` | the pill text is the not-taking-work form |
| open a window starting in `30` days | the pill names the month, not `available now` |
| attempt to set the pill's text directly | there is no interface or endpoint that permits it |

The third row is a test that a capability does **not** exist, which is the only
way to keep Section 24.6 true.

### 34.5 Accessibility

| Do | Assert |
|---|---|
| read the about statement with a screen reader | the statement is announced once, as one string, not word by word and not twice |
| read the work headline | announced as one string |
| tab through `/` | every focused element is within the frame when it receives focus |
| inspect the sound control | its accessible name states the action, not the state |
| compute contrast for every pairing in Section 31.1 | no pairing used for text falls below `4.5:1` |
| load with reduced motion | every scroll-driven element is at its final state and the document scrolls natively |

### 34.6 Budgets

| Do | Assert |
|---|---|
| count font requests before the hero name is readable | at most `2` |
| count script requests on `/` | fewer than `60` |
| grep the built stylesheet for a transition on `all` | no match |
| load each route throttled | the first text is readable inside the Section 32.1 budget |
| load `/` with sound off | no audio file is requested |

### 34.7 What is not tested here

No test asserts a colour, a coordinate or a screenshot comparison. The outlined
display type, the sheet transitions, the card stack's shadow and the render
layer are judged by a person against the captured screenshots, using
Section 38.

> **In plain language.** Things somebody can do to prove the site works, all of
> them about words on the screen and what got saved.
>
> The long one is the main journey: look at the work, check when he is free, pick
> a window, fill in the six questions, send it, then switch to his side, reply,
> offer a start date, accept it, and reload the home page. That last step is the
> whole point: the green badge at the top must have changed by itself.
>
> The most important short test has to be run properly: two people trying to book
> the last day of the same window at the same moment. One gets it, the other is
> told it filled up and shown what else is open. Run in sequence that test proves
> nothing; it has to be run at the same time.
>
> And three cheap ones that catch expensive mistakes. Count the font files before
> the first screen appears: at most two. Check no example text in the form uses a
> real person's name. And check there is no way at all, anywhere, to type over the
> availability badge by hand.

---

## 35. Copy deck

Every string the build ships, as plain text. Typographic quotation marks in the
capture are reproduced; typographic dashes are not, and are written as commas or
hyphens, because this deck is pasted into build tooling as plain text.

### 35.1 Chrome

| Slot | Copy |
|---|---|
| the lockup | `<GIVEN_NAME>`, `<FAMILY_NAME>` |
| the availability pill | `available now for work` |
| the sound control | `Sound | OFF`, and `Sound | ON` |
| navigation | `Home`, `About`, `Work`, `Contact` |
| the rail | `Honors` |
| the cursor label | `View` |

### 35.2 Hero

| Slot | Copy |
|---|---|
| eyebrow | `Creative Developer` |
| the name | `<GIVEN_NAME> <FAMILY_NAME>` |
| location | `Located in France` |
| the prompt | `Scroll down to explore` |

The hero carries three further measured single-character elements, a bullet, the
word `with` and a heart, which sit together as a made-with line. They are
reproduced as `•`, `with` and `❤`.

### 35.3 About

| Slot | Copy |
|---|---|
| title | `About` `<asterisk>` `me` |
| the statement | `An award-winning, product-minded frontend engineer with a background in aerospace engineering and human factors. I design and build visually striking web and mobile products where usability, reliability and performance matter, from concept to launch, with a strong focus on thoughtful UX, engaging interactions and practical AI-powered workflows.` |
| the figure | `5+` |
| the figure's label | `years of experience` |

The measured statement joins `matter` and `from` with a typographic dash. It is
written here as `matter, from`.

### 35.4 Services

| Title | Body |
|---|---|
| `SEO` | `Optimizing data to improve search engine rankings.` |
| `UX Design` | `From product's exploration to evaluation.` |
| `Web & Mobile Development` | `Industry-leading tools such as React, Three, Framer will be used to build your app.` |

**Flagged for the copywriter.** The third names three libraries in
customer-facing copy (Section 10.4). It is reproduced as measured and should be
reconsidered before launch: it promises a stack rather than an outcome and it
dates the page.

### 35.5 Work

| Slot | Copy |
|---|---|
| the home title | `Selected` `<asterisk>` `work` |
| the route label | `Work` |
| the headline | `Elevate user experience through cutting-edge technology and design` |
| the section label | `Work` |
| the count | `(09)` |

### 35.6 Contact

| Slot | Copy |
|---|---|
| the route label | `Contact` |
| the headline | `LET'S BUILD YOUR IDEA TOGETHER :)` |
| field 1 | `01.` `My Name` `*` |
| field 2 | `02.` `My Email` `*` |
| field 3 | `03.` `I work at` |
| field 4 | `04.` `I am looking for` `*` |
| field 5 | `05.` `My budget is` `*` |
| field 6 | `06.` `My message` `*` |
| the budget options | `USD $20001 and up`, `USD $10001-$20000`, `USD $5001-$10000`, `USD $2000-$5000` |
| the submit | `Send it now :)` |
| side column | `Further Inquiries`, `<CONTACT_EMAIL>`, `Located in France 📍`, `Social Media` |
| below the budget **[extension]** | `Smaller than that? Say so in your message and we will point you somewhere good.` |

**The placeholders are replaced.** The measured form uses a well-known
executive's real name, a plausible address at his employer, and that employer's
name as its three worked examples. Replaced with `Alex Renard`,
`arenard@northgate.com` and `Northgate`, and recorded in Section 37.6.

### 35.7 The nine projects

| # | Title | Credit |
|---|---|---|
| 1 | `Meridian` | `Development © 2026` |
| 2 | `Auriga Concept` | `Design & Development © 2025` |
| 3 | `Portfolio 2.0` | `Design & Development © 2024` |
| 4 | `Uplink Usability` | `Design © 2023` |
| 5 | `Tower Supervision` | `Design © 2023` |
| 6 | `Colisa` | `Design © 2023` |
| 7 | `UBX Roadmap` | `Design & Development © 2022` |
| 8 | `Aera Unity` | `Design & Development © 2023` |
| 9 | `Baba Quiz` | `Design & Development © 2021` |

Titles are placeholder-substituted; every credit line and year is measured
verbatim. The first project is dated `2026`, a year ahead of three of its
siblings, which is measured and is presumably a project in progress.

### 35.8 Footer

| Slot | Copy |
|---|---|
| heads | `Local Time`, `Version`, `Resource`, `Social Media` |
| the clock | rendered, `01:59 PM GMT+2` at capture |
| version | `2.0.0 © 2024` |
| resource | `Portfolio v1.0.5` |
| social | `<SOCIAL_ONE>`, `<SOCIAL_TWO>`, `<SOCIAL_THREE>` |
| the credit | `Made by <GIVEN_NAME>` |

### 35.9 The extension surfaces

| Slot | Copy |
|---|---|
| availability states | `available now for work`, `available from`, `booked until`, `not taking new work` |
| the availability page | `Start an enquiry`, `Fully booked right now.`, `The next opening is being scheduled.`, `Send an enquiry anyway` |
| holds | `This window is nearly full. Send an enquiry without holding it.`, `Your hold on that window ran out. You can still send this.` |
| proposals | `You have a start date to confirm.`, `That proposal expires soon.`, `That proposal has expired. Ask for a new one.` |
| capacity | `That window filled up. Here is what is open.` |
| auth | `If that address has an enquiry with us, a sign-in link is on its way.`, `That link has expired. We can send another.` |
| states | `Nothing here yet.`, `An enquiry appears here once you send one.`, `The pipeline is clear.`, `Nothing waiting on you.`, `No projects listed.`, `That did not load.`, `Try again` |
| denial | `That is not yours to open.`, `We cannot find that.` |
| offline | `You are offline. Your draft is safe.` |
| validation | `We need something to call you.`, `We need an address to reply to.`, `A few words about what you need.`, `Choose a range, even a rough one.`, `Tell us a little more, at least twenty characters.` |

### 35.10 The substitution mapping

| Real, on the reference | Placeholder | Characters |
|---|---|---|
| the person | `Elian Moreau` | 12 to 12 |
| given name | `Elian` | 5 to 5 |
| family name | `Moreau` | 6 to 6 |
| project 1 | `Meridian` | 8 to 8 |
| project 2 | `Auriga Concept` | 15 to 14 |
| project 4 | `Uplink Usability` | 15 to 16 |
| project 5 | `Tower Supervision` | 15 to 17 |
| project 6 | `Colisa` | 6 to 6 |
| project 7 | `UBX Roadmap` | 11 to 11 |
| project 8 | `Aera Unity` | 10 to 10 |
| project 9 | `Baba Quiz` | 9 to 9 |
| the form's example person | `Alex Renard` | 8 to 11 |
| the form's example employer | `Northgate` | 5 to 9 |
| the two award bodies | `<AWARD_ONE>`, `<AWARD_TWO>` | tokenised |
| the second and third social platforms | `Postline`, `Showcase` | tokenised |

`Portfolio 2.0` is kept: it is a generic label, not a client's name.

> **In plain language.** Every word the site says, in one place.
>
> Three things in it need a decision before launch. The paragraph about services
> names three specific tools by name to clients, which dates the page and
> promises a toolkit rather than a result. The first project is dated a year
> ahead of the others, which is presumably work in progress and worth checking.
> And the example text inside the contact form uses a famous chief executive's
> real name, a guessable work email address at his company, and that company's
> name; we have replaced all three with invented ones.
>
> Everything else is measured word for word, including the small joke of a smiley
> face set at the same enormous size as the headline, which is worth keeping.

---

## 36. Zero-asset substitution guide

### 36.1 What the reference carried

By class and count, from the ledger. No filename is reproduced.

| Class | Files | Bytes |
|---|---|---|
| script | 1753 | 9.94MB |
| font, modern format | 225 | 3.00MB |
| font, legacy format | 26 | 355KB |
| audio | 21 | 1.57MB |
| binary payloads | 7 | measured as served |
| compiled render modules | 3 | measured as served |

### 36.2 Type

| Family | Substitute |
|---|---|
| the working face | a geometric grotesque with a true bold, from an open family, named and licensed in one place |
| the display face | a condensed display face with a strong vertical stress, from an open family |
| the fallback faces | generated metrics-matched fallbacks, as the reference already does, Section 3.4 |

The display face is only ever used as an outline (Section 3.4) and only for
about four dozen distinct characters (Section 32.4). Both facts make the
substitution unusually forgiving: an outline hides much of a face's personality,
and a subset of four dozen glyphs can be checked by eye in a minute.

Name the chosen families and their licences in one place, so the swap for the
real faces at launch is one line.

### 36.3 The render layer

Generated, not fetched. A lobed rounded form (Section 8.2) composed from
primitives:

| Part | Primitive |
|---|---|
| the body | a sphere of radius `1.0`, displaced by three-octave value noise at amplitude `0.18` |
| the surface | a smooth dielectric with a single strong specular from the upper left |
| the colour | a deep blue, taken from the measured `#8b5cf640` halo's own hue at full saturation |
| the motion | a slow rotation and a slower noise evolution, both continuous |

Marked **inferred** as to form (Section 8.2). The composition is a
reconstruction from one screenshot.

**The important part is that it is optional.** The measured hero gradient and
halo (Section 8.3) are stylesheet values and carry most of the effect. Build
step 5 ships the hero without this layer (Section 33).

### 36.4 Project media

Generated from a seed stored on the record (`media_seed`, Section 24.1), so the
same project renders the same image everywhere:

1. Fill with `--c-ink`.
2. Draw three to five overlapping soft forms chosen by the seed, in
   `--c-purple`, `--c-violet` and `--c-violet-bright`.
3. Apply the measured card scrim,
   `linear-gradient(133.655deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.6) 100%)`,
   at its measured angle.
4. Apply `grayscale(1)` at rest and `grayscale(0)` on activation, as measured.

Abstract and deliberately so. A generated image that pretends to be a screenshot
of a real client project is worse than one that plainly is not.

### 36.5 The tool marks and the award badges

Both are third-party (Section 4.7) and neither is reproduced.

| Asset | Substitute |
|---|---|
| the fourteen tool marks | a generic mark set: a `21px` rounded square carrying the tool's initial, in `--c-paper` on a `#ffffff26` ground, seeded from a list the owner edits |
| the two award badges | a `50px` ring carrying a two-letter abbreviation and a year, in `--c-purple` on `--c-paper` |

Both are placeholders for the real marks, which the owner is entitled to use and
this document is not. The layout, the sizes and the band's behaviour are
measured and reproduced exactly; only the artwork is substituted.

### 36.6 The contact texture

Already zero-asset: the measured topographic pattern is an inline vector data
value at `fill-opacity: 0.1` (Section 8.4). Reproduced as measured.

### 36.7 Audio

Twenty-one cues, generated through the browser's audio graph rather than
shipped:

| Cue class | Recipe |
|---|---|
| pointer over a control | a `40ms` sine at `880Hz` through a short envelope, at low gain |
| press | the same at `660Hz`, `60ms` |
| section change | two detuned sines a fifth apart, `200ms`, filtered |
| field focus | a `30ms` click, filtered noise |
| submit | a rising two-note figure, `300ms` |
| modal open and close | the same figure, inverted for close |

Six classes rather than twenty-one distinct files, which is also the fix for
Section 14.5's rule against layering.

### 36.8 The honest limits

| Substitute | What is lost |
|---|---|
| the two typefaces | the real letterforms, which are the site's voice |
| the render layer | the exact form; ours is reconstructed from one screenshot |
| project media | every real screenshot of every real project |
| the tool marks and badges | the real marks, which belong to others |
| the audio | the original sound design |
| the contact texture | nothing; it was already procedural |

> **In plain language.** Nothing is delivered as a file: no pictures, no fonts,
> no sound. Everything is generated from a recipe, so this document is the whole
> delivery.
>
> The typefaces are the biggest loss, since they are the site's voice. We have
> one piece of luck: the tall display face is only ever used as an outline, and
> only for about four dozen letters, and an outline hides most of what makes a
> typeface distinctive. So a free stand-in gets much closer here than it usually
> would.
>
> The pictures of projects are abstract on purpose. A made-up image pretending to
> be a screenshot of real client work is worse than an obvious stand-in, because
> somebody will eventually ship it.
>
> The row of tool logos and the two award badges are not ours to hand on. The
> layout and sizes are reproduced exactly; the artwork is a placeholder for the
> real marks, which you are entitled to use.
>
> The sound is rebuilt from six short recipes rather than twenty-one files, which
> also happens to fix a rule about never playing two at once.

---

## 37. Evidence gaps and substitutions

### 37.1 The capture

Two runs. The first was stopped by the environment partway through and left no
`capture.json`, making the bundle unusable; the second completed cleanly with
`3321` responses and `297` screenshots across twelve paths and three
breakpoints. Nothing about the site caused the first failure.

**This is the most complete capture in the corpus.** The document scrolls
natively, so all nine scroll samples are real positions, and three routes render
distinct documents with distinct content. Where this document says a value was
measured across breakpoints, it was.

**Nine of twelve paths are not pages.** Three are the analytics vendor's own
collection endpoints scraped from its bundle. Four are catch-all fragments
serving the home document. One returns `403: Forbidden`, measured, and is an
asset directory. One, `/work/`, is `/work` with a trailing slash (Section 2.4).

### 37.2 Enum substitutions

| Level | Chosen | Why |
|---|---|---|
| `category` | `solo_founder` | a public-facing independent business |
| `domain` | `portfolio-agency` | the enum's own description, freelance showcase and enquiries, is exactly this |
| `pattern` | `booking-scheduling` | the measured availability signal and the six-field enquiry form point at a calendar. `crud-records` and `content-publishing` were the alternatives and were rejected: the workflow's subject is a date, not a record or an article |
| `archetype` | `freelance-availability-booking` | three tokens, naming the workflow |

### 37.3 Extensions, and what each was derived from

| Extension | Derived from |
|---|---|
| the availability model, Section 15.2 | the measured pill, its green dot and its halo |
| the availability page, Section 15.3 | the work index's pill layout |
| windows and holds, Section 18.1 | nothing measured |
| the enquiry pipeline, Section 18 | the measured six-field form and its four budget bands |
| the proposal, Section 19.5 | nothing measured |
| accounts, Section 16 | nothing measured. Field treatment from the measured numbered field |
| roles, Section 17 | nothing measured |
| the denied surface, Section 20.5 | the measured route label and section layout |
| the studio pipeline, Section 21.4 | the home preview's row treatment |
| the four breakpoints, Section 30.2 | the twenty measured queries, collapsed |
| the below-the-floor line, Section 19.4 | the measured budget bands and their missing lowest option |

### 37.4 Inferred, not measured

| Thing | Status |
|---|---|
| the render layer's form, Section 8.2 | reconstructed from one screenshot; position and colour measured |
| the twenty-one audio cues' mapping, Section 14.3 | the count is measured, the mapping is not |
| the project modal's contents, Section 12.4 | the container is measured, its contents were not captured |
| the project descriptions | not captured; the reference may not have any |
| the `I am looking for` and `My message` placeholders | not captured |
| the tool band's behaviour, Section 10.5 | the marks and the panel are measured, the scrolling is inferred |
| the runtime easing on four live animations, Section 6.8 | recorded in the animation, absent from the ledger's declared list, and therefore not quoted |
| the hero flag bar's segment order | inferred from the screenshot as blue, white, red |
| everything behind the contact form | never reached |

### 37.5 Two easing notations, and one missing curve

The signature curve is declared both as `cubic-bezier(.76,0,.24,1)` and as
`cubic-bezier(0.76, 0, 0.24, 1)`. Both forms are in the ledger, so both validate,
and this document uses the short form throughout.

Separately, four live animations were recorded with an easing that appears in
**no** declared rule and therefore is not in the ledger's curve list. This
document does not quote its literal, because a curve that was recorded from a
running animation but never declared cannot be checked against the ledger. It is
described in Section 6.8 and substituted with a measured curve.

That distinction is worth keeping: a value observed once at runtime is weaker
evidence than a value declared in a stylesheet, and this kit's gate treats them
identically only because it never sees the difference.

### 37.6 Defects found in the reference

| Defect | This build |
|---|---|
| the contact form's example text uses a real executive's name, a guessable address at his employer, and that employer | replaced, Section 35.6 |
| no privacy notice anywhere, while collecting a name, an address and an employer | served and linked at the form, Section 15.5 |
| no consent surface in any captured frame, while running an analytics vendor | Section 27.3 |
| placeholder text at `3.6:1` contrast, on a form where placeholders are the only guidance | Section 31.2 |
| twenty media queries, five within `80px` of each other | four breakpoints, Section 30.2 |
| a transition on `all` declared `6131` times | the twelve named declarations, Section 6.3 |
| `225` font files for three families | subset and ordered, Section 32.4 |
| `1753` script requests | a production bundle, Section 32.3 |
| no reduced-motion query on a document with fourteen scroll-driven selectors | Section 6.10 |
| three chrome stacking values, `47`, `48`, `49`, one apart | one layer with ordered children, Section 3.8 |
| `/work` and `/work/` both resolving | one canonical form, Section 2.4 |
| the availability claim is typed into the markup | derived from the calendar, Section 24.6 |

### 37.7 One ledger defect

`ledger.md` rendered its inline-drawing section empty while `ledger.json` carries
`29` entries with full path geometry. Section 4 is built from the json half.

This is the same fault seen on another site in this corpus and is worth fixing
in the kit: an author reading only `ledger.md` would conclude this site has no
icons, when it has twenty-nine.

### 37.8 What was not captured at all

- Any hover state, on any route. Hover deltas were `0` everywhere, so every
  hover treatment in this document is derived from a measured non-hover state or
  is inferred.
- The project modal open.
- Anything behind the contact form's submit.
- The mobile menu open.
- The sound in its `ON` state.
- Any consent or privacy surface, because there is none.

> **In plain language.** The honest list, and this time it is shorter than usual.
>
> This capture went well. The page scrolls normally, so we could walk down all
> three real pages at nine positions on three screen sizes and measure almost
> everything. Nine of the twelve addresses we found are not pages: three belong to
> the analytics company, four are the home page under another name, one is a
> locked folder and one is the work page with a slash on the end.
>
> What we could not see: any hover effect at all, the project pop-up when it is
> open, the menu when it is open, and everything behind the send button.
>
> The most useful part of this section is the list of things that are wrong with
> the reference rather than missing from our capture. Twelve of them, each with
> the fix. The three that matter most: the contact form uses a real executive's
> name and a guessable work email as its examples; the site collects names, email
> addresses and employers with no privacy notice anywhere; and the green
> "available now" badge is typed into the page by hand, so it will eventually be
> a lie.

---

## 38. Acceptance checklist

| # | Check |
|---|---|
| 0 | Every angle-bracket token in Section 0.5 is replaced, and no borrowed logo or badge survives |
| 1 | The hero states what he does, where he is, and whether he is free, within one frame |
| 2 | Three real routes resolve, `/work/` redirects to `/work`, and no analytics endpoint is served as a page |
| 3 | Only the colours of Section 3.2 appear, and none of the library's forty named colours does |
| 4 | The display face is outlined and never filled, except the hero name |
| 5 | The header is transparent at rest and acquires its blurred ground under scroll |
| 6 | Every stroked mark draws itself rather than fading in |
| 7 | Each section slides a full frame height with its rounded top edge and light line |
| 8 | The hero is complete and correct with the render layer disabled |
| 9 | The scroll prompt arrives last, over `3.45s`, after everything has settled |
| 10 | The about statement reveals per word over its shadow twins |
| 11 | The home preview and the work index draw the same nine records |
| 12 | The nine projects stagger at desktop and stack in one column below `690px` |
| 13 | The contact form's six numbered fields validate on blur, not on keystroke |
| 14 | Sound is off on arrival and its setting persists |
| 15 | The availability pill is derived from the calendar and cannot be typed over |
| 16 | An enquiry can be submitted with no account |
| 17 | There is exactly one studio account, with a separate recovery address and a working export |
| 18 | The whole of Section 34.1 passes, including step 13 |
| 19 | No form validates on keystroke, no red appears, and the below-the-floor line is present |
| 20 | Every list has five states, and an offline draft survives a browser restart |
| 21 | The pipeline opens on enquiries that need an answer, not on everything |
| 22 | Capacity is committed at acceptance, never at hold, and only ever by the server |
| 23 | Declining an enquiry always sends mail, with no way to suppress it |
| 24 | No file upload, no payment field and no invoice exists anywhere in the build |
| 25 | Enquiries are retained three years then anonymised, and the privacy notice says so |
| 26 | The footer clock shows his timezone with its offset and survives a daylight-saving change |
| 27 | Nothing anybody typed into the form appears in any analytics property |
| 28 | The form is rate limited and no submitted link is ever fetched by the site |
| 29 | The availability pill subscribes to shared state and does not fetch its own |
| 30 | Four breakpoints exist and no others |
| 31 | No pairing used for text falls below `4.5:1`, and both split headlines are announced once |
| 32 | At most two font files load before the hero name is readable, and no audio loads with sound off |
| 33 | The breakpoints were collapsed at step 2, before any section was built |
| 34 | Every assertion in Section 34 passes on text and state alone, with the capacity test run concurrently |
| 35 | Every string appears in Section 35, and no real person's name survives in the form's examples |
| 36 | No image, font, audio or model file is fetched at runtime |
| 37 | Every item marked inferred has been reviewed against the screenshots at least once |
| 38 | This list has been walked end to end by a person, with the screenshots beside them |

> **In plain language.** One line per section, answerable yes or no with the
> photographs of the reference beside you.
>
> A handful catch the things that actually matter. That the tall lettering stays
> an outline and is never filled in. That the page still looks right with the
> three-dimensional shape switched off. That the green availability badge is
> worked out from your calendar and there is no way to type over it. That
> declining someone always sends them an email. That nothing anybody types into
> your contact form is ever recorded as a statistic. And that no real person's
> name is left in the form's example text.
>
> The last line is a person actually walking this list rather than assuming.
