# Iron Wood

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, scroll the home page past the sculpted honey badger, read what the studio does, open a case study from the index, and send a project enquiry that is stored and confirmed in place, without hitting an error page. A different stranger must NOT be able to read an unpublished case study or article, the record behind it, or any image an editor stored for it, by any means. The image bytes must live in the object store at their scheme's key; a copy on the app's own disk does not count, and neither does a database row that only says an upload happened.

## Overview

Iron Wood is a product design and development studio with two offices. This product is the studio's public website, its new-business front door, together with the small signed-in studio its editors use to keep the work current. The site is built for founders, product leads and marketing leads who are commissioning a digital product and comparing three or four studios at once. They arrive from a referral, a directory listing or an award profile, and they want, in this order: proof the studio has shipped work at their scale, a sense of its taste, a clear list of what it actually does, and a way to start a conversation. The site is ordered exactly that way, and the award badges sit directly under the first paragraph of self-description, before any case study, any service and any word about the team.

The public site carries ten content routes, a terms page and an error page: a home page built around a sculpted three-dimensional mascot, a services page, a case study index whose entries open into long project pages, an about page for the team and the offices, a categorised article archive with article pages, a privacy policy, and a contact page that ends in the project enquiry form. Everything above that form is persuasion; submitting it is the one conversion.

It deliberately is not: a store, a payment surface, a mail sender, a search engine, a job application system, a comment system or a client portal beyond a list of one's own enquiries. The case studies describe products the studio built for its clients; none of those products is built here.

Four things make it expensive, in the order they cost time: a live, faceted sculpture of the mascot that carries the home page; a second pair of live scenes on the case study index, one of which replaces a row's picture; seven small live objects floating in the home page culture section; and a per-word reveal applied to every heading on the site. The genuinely hard part underneath all of that is that a draft is private in three places at once: its public page, the record behind that page, and every image stored for it must refuse everyone except the editor who owns it, and a draft must never leak into a listing, a category count or the sitemap.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `editor` | Sign in to the studio. Create case studies and articles as drafts. Edit, publish and unpublish the case studies and articles they own. Upload images to an entry they own. Read their own drafts and their own draft images. Read every enquiry. Move an enquiry forward through its states. | **Cannot read, edit, publish or unpublish another editor's entry while it is a draft.** **Cannot read another editor's draft image.** **Cannot edit or withdraw another editor's published entry.** |
| `client` | Sign up without an invitation. Read every published page. Send an enquiry while signed in, which attaches it to their account. Read the enquiries attached to their own account and see each one's state. | **Cannot read any draft, any draft record or any draft image, including one they were linked to directly.** **Cannot create, edit, publish or upload anything.** **Cannot read another person's enquiries.** **Cannot change an enquiry's state.** |

A visitor with no account can read every published page and can send an enquiry; an anonymous enquiry is stored with no account attached.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `client` session to any `editor`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create a `client` account from `/sign-up` with no invitation and no approval step. `editor` accounts exist only as seeded data and cannot be created through the site.

Seeded accounts, every one with the password `deku-demo-pw-2026`:

| Email | Role | Display name |
|---|---|---|
| `editor@example.com` | `editor` | `Nadia Brooks` |
| `editor2@example.com` | `editor` | `Owen Pike` |
| `client@example.com` | `client` | `Leo Marsh` |

## Core features

### Auth

Email and password, implemented in this application. Passwords are hashed and the exact literal `deku-demo-pw-2026` must work at login for every seeded account. A successful call to `POST /api/auth/login` returns a bearer token in the field `access_token`; API clients send it as a bearer token on every request except login, sign-up, the health route and the public read endpoints, and the pages may carry the same session in a cookie. A session that expires mid-action leaves the page in place, shows an inline banner saying the session ended, and offers to sign in again without discarding the form the person was filling.

`POST /api/auth/sign-up` takes `email`, `password` and `display_name` and creates a `client`. A second signup with an address already in use is refused as invalid and creates nothing. There is no password reset flow and no email is sent anywhere by this product.

### Studio entries and the publication rules

Editors keep two kinds of entry: case studies and articles. Each carries a `state` of `draft` or `published`. A slug is lowercase letters, digits and hyphens, and always starts with a letter.

1. An editor creates an entry as a `draft`, and it is visible to nobody but that editor. Requesting a draft's public page, its record through the API, or any image stored for it, as an anonymous visitor, as a `client`, or as a different `editor`, is refused, and the refusal does not disclose that the entry exists.
2. A draft never appears in a public listing, in the case study index, in the article archive, in a category's entry count, in the related articles on an article page, in the next-project section of a case study, or in the sitemap.
3. Publishing an entry makes it readable at its public route, stamps `published_at` in UTC, adds it to its listings and adds its address to the sitemap, all in the same operation. Unpublishing reverses every one of those: the page, the record and its images stop being served to anyone but the owner, and it leaves every listing, every count and the sitemap.
4. **Exactly one published case study holds a given slug, and exactly one published article holds a given slug.** A draft may hold a slug that is already taken; publishing it is refused as a conflict and it stays a draft. Two simultaneous publishes claiming the same slug must not both succeed: exactly one wins and the other is rejected as a conflict. The loser leaves nothing behind: no half-published entry, no stray listing position, no sitemap address, no entry stranded between states.
5. A case study references its services by relation, never as free text: every service it names must be one of the eight services, and naming any other value is refused as invalid with nothing written. The same list renders on the case study index row and on the case study page, so the two can never disagree.
6. An article references exactly one category. Creating an article with no category, or with a category that does not exist, is refused as invalid with nothing written.
7. An editor can change or withdraw only the entries they own. A write from another editor, or from a `client`, is refused and the entry does not change.

### Images live in the object store

Every image an editor uploads is stored in the MinIO bucket named by `STORAGE_BUCKET`, reached at `STORAGE_ENDPOINT` with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, and nowhere else.

8. The object key is `media/{kind}/{entry_id}/{sha256_of_bytes}.{ext}`, where `kind` is `case-study` or `article`. For example `media/case-study/42/9f2a1c7d3b0e5a86c41f29d7e0b3a5c8d9f1e2a4b6c8d0e2f4a6b8c0d2e4f6a8.png`. An upload writes the bytes to that key and records the key, the content type, the byte size and the alternative text. Bytes on the app container's filesystem are a contract violation, as is a database column holding the image itself, however correct the page looks.
9. Only images are accepted: `image/png`, `image/jpeg` and `image/webp`, up to 5 MB. Anything else is refused as invalid, and nothing reaches the bucket or the database.
10. Bytes are served only through `GET /api/media/{asset_id}/content`, which streams them from the bucket after checking who is asking: anyone for an image of a published entry, and only the owning editor for an image of a draft. The bucket is never made publicly readable and no time-limited link to an object is ever issued.
11. Sending the same bytes to the same entry twice does not create a second object and does not create a second asset record. The second attempt is a no-op that returns the existing asset.
12. Every uploaded image carries alternative text written by the editor, and an upload without it is refused as invalid. Uploaded images appear on the entry's page in upload order with that text.

### The case study index and the project pages

13. The index at `/works` lists every published case study as a full-width row, in index order: the ten seeded case studies first in the order listed under `## Data model`, then any case study published later, appended after the last in the order it was first published.
14. Rows alternate which side carries the picture: the first row carries it on the right, the second on the left, and so on down the page. Each row carries `data-case-study-row`, `data-slug` set to the case study's slug, and `data-image-side` set to `right` or `left`.
15. A row carries the case study's label, its title, the list of its services and an arrow link, and the whole row opens the case study page at `/works/{slug}`; no row opens any other address.
16. A case study page carries, in order: the client name set in the display face, a subtitle, a fact sheet (the client name, a `Visit site` link to the client's own site, the `Industry` label with the case study's label, and the `Year` label with its year), the services list, the body with its uploaded images, and a closing next-project section headed `Next project` that shows the title of the case study after it in index order and links to it. The last case study's next project is the first.

### The article archive

17. The archive at `/blog` lists published articles newest first by `published_at`, four to a page. Each entry row carries `data-article-row` and `data-slug`, and shows the category, the title, the publication date and the reading time in the form `7 min read`.
18. Pagination appends rather than replaces: a single control labelled `More` carries `data-pagination="next"` and links to the next page as `?page=2`, `?page=3` and so on; pressing it adds the next four rows beneath the ones already shown without reloading the document. The control is absent on the last page. `/blog?page=2` also renders on its own.
19. Above the rows sits a row of category tabs: `All`, then the three categories in the order `Product design`, `Engineering`, `Studio life`. Each category tab links to `/blog-categories/{slug}` and shows the number of published articles in that category, carried as `data-count`. The tab for the page being viewed carries `aria-current="page"`.
20. A category route lists only the published articles of that category, newest first, four to a page, with the same pagination, in the same template as the archive.
21. An article page carries the title, the category, the date and reading time, a hero picture, the body, a sidebar with a contents list and share links, a reading progress bar carrying `data-reading-progress`, and a closing set of at most two related articles drawn from the same category (the newest published ones other than the article itself). No other route carries `data-reading-progress`.

### The project enquiry

22. The contact page carries one form, marked `data-enquiry-form`, with five visible fields named exactly `Service`, `Budget`, `Name`, `Email` and `Message`, a hidden field named `bpGCap` carrying the bot-check token, and a decoy field named `Website` that a person never sees and never fills.
23. `Service` and `Budget` are chosen from fixed options, not typed. `Service` offers the eight services. `Budget` offers `Under $10k`, `$10k - $30k`, `$30k - $60k`, `$60k - $100k` and `Over $100k`. A submission carrying any other value in either field is refused as invalid and stores nothing.
24. `Name`, `Email` and `Message` are required; an address that is not a valid email address is refused as invalid. Every refusal names the field at fault, beside that field, and stores nothing.
25. The bot-check token comes from `GET /api/bot-check`, which returns `token`. The contact page renders with a fresh one in `bpGCap`. A token is valid for ten minutes and for one submission. A submission with a missing, unknown, expired or already used token is refused and stores nothing.
26. A submission whose decoy field `Website` arrives filled is refused and stores nothing. The same email address sending enquiries repeatedly in quick succession is refused after the second: a third enquiry from one address within sixty seconds of the first of them is refused and stores nothing. Each refusal is reported in the failure panel with a plain reason.
27. An accepted enquiry is stored with the state `new`, and with the sender's account attached when the sender is signed in. The page then replaces the form, in place and without navigating, with the success panel, which carries `data-form-result="success"`, the heading `Thank you. Your enquiry is with us.` and the line `We read every message and reply within two working days.`
28. Any refusal or failure shows the failure panel, which carries `data-form-result="failure"` and the line `Something went wrong and your enquiry was not sent. Everything you typed is still here.`, and leaves every value the person typed in its field. Both panels are in the page from the start and are hidden until needed.
29. The bot check loads on the contact route and on no other route: the contact page carries one element marked `data-bot-check`, and no other route carries one.
30. An enquiry moves forward only: from `new` to `in_conversation`, and from `new` or `in_conversation` to `closed`. `closed` is final. Only an editor may move one, through `PATCH /api/enquiries/{id}`; a backward move is refused and changes nothing.
31. `GET /api/enquiries` returns every enquiry to an editor, only the caller's own enquiries to a `client`, and is refused to a visitor with no session. A signed-in client sees their enquiries, newest first, at `/account/enquiries`, each row carrying `data-enquiry-state` set to its state.

### Where the sculptures are drawn

32. Live scenes exist on two routes only. The home page carries one element marked `data-scene="mascot-hero"` and seven marked `data-scene="culture-object"`; the case study index carries one marked `data-scene="works-field"` and one marked `data-scene="works-preview"`. No other route carries any `data-scene` element, and a route that carries none never starts a renderer.
33. The seven culture objects carry `data-object`, in page order: `rocket`, `wand`, `arrow`, `bomb`, `thumb`, `bond`, `flame`. Each is its own scene, never seven objects in one scene.
34. The home page sculpture is drawn live only at desktop widths. Below that, the same element draws nothing and a still of the same sculpture stands in its place. The culture objects and both case study index scenes are live at every width, and both index scenes draw the same faceted honey badger: the full-height field shows the sculpture moving against scroll behind the rows, and the preview shows it inside a row's picture box.
35. Everywhere outside the home page and the case study index the mascot appears, it is a still rendered from the same sculpture rather than an image file fetched from the server: standing in the footer of every route that has one, standing beside the contact page's hero, and seated in a chair on the about page. The error page carries a still of a low, faceted rock form.

### The page grounds

36. Every public content route is a stack of full-width bands, and each band carries `data-ground` set to `dark`, `light` or `tinted`. No two neighbouring bands share a ground, on any route.
37. Every public content route's first band is `dark`, except the case study index, whose first band is `light`. The sequences are: home `dark`, `light`, `dark`, `tinted` (the hero and the process section share the first dark band, because the sculpture stays pinned across their boundary); services `dark`, `light`, `dark`, `tinted`; the case study index `light`, `dark`; a case study page `dark`, `light`, `dark`; about `dark`, `light`, `dark`, `tinted`; the article archive and every category route `dark`, `tinted`; an article page `dark`, `light`, `tinted`; contact `dark`, `light`; the privacy policy and the terms page `dark`, `light`; the sign-in page, the sign-up page, the account page and every studio page one `dark` band; the error page one `light` band whose lower part is painted dark behind the rock still, which makes it the second route that does not open dark. The footer is not a band and carries no `data-ground`.

### The chrome every route shares

38. The header carries the logo, the four links `Services.`, `Works.`, `About.` and `Blog.`, and a button reading `Contact` that opens `/contact`. The drawer carries `Home.` (opening `/`), `Services.`, `Works.`, `About.`, `Blog.` and `Hire us.` (opening `/contact`), the seven social labels `facebook`, `behance`, `instagram`, `dribbble`, `clutch`, `linkedin` and `awwwards`, the contact block `Contact` with `hello@example.com` and `Careers` with `hr@example.com`, and both office addresses. The full stop is part of each navigation label. The three link sets are deliberately not identical.
39. The drawer is marked `data-drawer`, and the control that opens it is a button marked `data-drawer-trigger` carrying `aria-expanded`, which reads `false` while the drawer is closed.
40. Every public route except the contact page and the error page ends with the footer. The footer carries a lead-in line `Have a product in mind?`, one oversized link reading `Let's build it` that opens `/contact`, both office addresses, the copyright line `© 2026 Iron Wood - UX UI Design Agency`, a `Privacy Policy` link to `/privacy-policy`, a `Terms` link to `/terms`, and six social labels, which are the drawer's seven without `behance`.
41. The about page's office section is a switcher built from two real buttons marked `data-office-switch`, each carrying `aria-pressed`, beside two office images marked `data-office-image`, exactly one of which carries `data-active="true"` at any time. Pressing a button makes its office active.
42. Every heading that arrives one word at a time carries `data-split-heading` and carries its complete text as its `aria-label`, so it is announced once, as one sentence.
43. The services page motif is marked `data-motif="hive"` and contains one part marked `data-motif-part="hive"` and three marked `data-motif-part="orbit"`, of which exactly one carries `data-phase="reverse"`.

### The launch surface

44. Every public HTML route carries its own `<title>` and its own meta description in the document head, and no two routes share either. That includes each case study page, each article page, each category route, `/sign-in` and `/sign-up`; the sitemap, the robots file and the preview images are not HTML routes.
45. A sitemap at `/sitemap.xml` lists `/`, `/services`, `/works`, `/about-us`, `/blog`, `/contact`, `/privacy-policy`, `/terms`, every published case study, every published article and every category route, and never a draft. A robots file at `/robots.txt` points at the sitemap with a `Sitemap:` line carrying the sitemap's full address.
46. Every public HTML route declares a social preview title and a social preview image in its head, as `og:title` and `og:image`. The preview image address is `/social-preview/{page_key}` on this app's own origin, with no file extension, where `page_key` is `home`, `services`, `works`, `works-{slug}`, `about-us`, `blog`, `blog-{slug}`, `blog-categories-{slug}`, `contact`, `privacy-policy`, `terms`, `sign-in` or `sign-up`, and it answers with an image generated when it is requested from the brand's own geometry; nothing is stored.
47. A terms page at `/terms` states the terms under which the site and the enquiry form may be used. It is linked from the footer of every route that has a footer and from the sign-up form, which reads `By creating an account you agree to the Terms of Service.` with the last three words linking to `/terms`.
48. The privacy policy at `/privacy-policy` states what the site stores about a person who sends an enquiry or creates an account, how long it is kept, and how to ask for it to be removed by writing to `hello@example.com`.
49. An unknown address renders the site's own error page and answers not-found. The page reads `Sorry! The page you're looking for was not found`, shows `404` very large beneath it, and offers a `Back to home` link to `/`. It keeps the header, the drawer and the pointer ring, carries no footer, and is exactly one viewport tall with nothing to scroll.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: the sculpture, the intro and awards, the process words, the culture scatter, the client strip, the testimonials | public |
| `/services` | what the studio does: the hive motif, the service list, how it works, the team promise | public |
| `/works` | the case study index: ten alternating rows over a full-height scene | public |
| `/works/{slug}` | one case study, as a long project document | public |
| `/about-us` | the seated sculpture, the journey, the team grid, the office switcher | public |
| `/blog` | the article archive, four rows to a page, with category tabs | public |
| `/blog/{slug}` | one article, with its progress bar and sticky sidebar | public |
| `/blog-categories/{slug}` | the archive filtered to one category | public |
| `/contact` | the offices, the studio addresses and the enquiry form | public |
| `/privacy-policy` | the privacy policy | public |
| `/terms` | the terms of service | public |
| `/sign-in` | sign in | public |
| `/sign-up` | open signup, creating a `client` | public |
| `/account/enquiries` | a client's own enquiries and their states | `client` |
| `/studio` | the editor's card grid of every case study and article they own | `editor` |
| `/studio/new/details` | step one of creating an entry: kind, name or title, slug, and the kind's fields | `editor` |
| `/studio/new/media` | step two: images and their alternative text | `editor` |
| `/studio/new/review` | step three: review, save as draft, or publish | `editor` |
| `/studio/entries/{kind}/{id}` | one owned entry, where `kind` is `case-study` or `article`: edit, upload, publish, unpublish | `editor` |
| `/studio/enquiries` | every enquiry, with its state control | `editor` |
| `/sitemap.xml` | the sitemap | public |
| `/robots.txt` | the robots file | public |
| `/social-preview/{page_key}` | the generated social preview image for one route | public |

The about route is `/about-us` although every label for it reads `About.`, and category routes are `/blog-categories/{slug}`, plural and hyphenated, while articles are `/blog/{slug}`. Both irregularities are deliberate and are kept.

### Entry and redirects

A visitor with no session reaching `/account/enquiries` or any `/studio` route is sent to `/sign-in` with the intended address remembered, and lands there after signing in. Signing in sends an `editor` to `/studio` and a `client` to `/account/enquiries`. A `client` reaching a `/studio` route is refused and shown their own enquiries instead. Signing out returns to `/`. A session that expires mid-action leaves the page in place with an inline banner and the form intact. Moving between any two public routes swaps the page without reloading the document, resets the scroll position to the top of the new route, and leaves the drawer trigger, the pointer ring and the scrolling behaviour running rather than rebuilding them.

### Journeys

**A founder decides and writes in.** Open `/`. Watch the loader count up and leave upward. Scroll past the sculpture as the ground turns dark beneath it, through the process words and the culture scatter to the testimonials. Open the drawer and choose `Services.`; read the service list while the hive sways. Choose `Works.`, watch the ground invert at the edge of the first band, and open the `Lumen Pay` row. Scroll the project to `Next project`. Press the header's `Contact` button, choose `UX/UI design` and `$30k - $60k`, fill name, email and message, and press send. The form is replaced in place by the success panel.

**A founder with an account follows up.** Open `/sign-up`, read the terms sentence, create an account, send an enquiry while signed in, open `/account/enquiries`, and see it listed as `new`.

**An editor publishes a case study with an image.** Sign in as `editor@example.com`. The studio opens on a card grid of every entry that editor owns, each card showing a state chip and carrying `data-entry-state`. Press `New entry`. The wizard opens at `/studio/new/details`, marked `data-wizard-step="details"`: choose case study, fill name, slug, label, title, subtitle, summary, year, site address and body, and pick services. Continue to `/studio/new/media` (`data-wizard-step="media"`) and attach an image with its alternative text. Continue to `/studio/new/review` (`data-wizard-step="review"`), save as a draft, and see an inline banner confirm it. Open the entry and press `Publish`; an inline banner confirms it in place, the card's state reads `published`, the row appears at the end of `/works`, and its address appears in `/sitemap.xml`.

**An editor answers an enquiry.** Sign in as an editor, open `/studio/enquiries`, and move the enquiry from `client@example.com` from `new` to `in_conversation`. An inline banner confirms it, and the client sees the new state at `/account/enquiries`.

**A reader walks the archive.** Open `/blog`, press `Engineering`, return to `All`, press `More` to append the next rows, open an article, and watch the bar beneath the hero fill as the body scrolls past.

### States

Every list has an empty state and every page a loading state. An editor with no entries sees a studio grid with one sentence and the `New entry` action. A client with no enquiries sees one sentence and a link to `/contact`. Appending the next page of articles shows a quiet loading indicator in the place of the `More` control until the rows arrive. A category with no published article shows one sentence under its tabs. A failed request leaves an inline banner and the page still usable; errors never crash the app.

## UI/UX notes

Somebody arriving here should understand within the first screen that this studio makes digital products with real craft and has shipped them for companies like theirs, and should feel invited to start a conversation rather than sold to. The register is a portfolio and persuasion site: atmosphere and a point of view are allowed and expected on the public routes, the sculpture and the work are seen first, and every page leads toward one enquiry. The editor studio and the account page are the opposite register: quiet, operational working tools with no atmosphere at all.

The public site has to convey craft and confidence, so each band gives one subject the whole width and surrounds it with space; it has to guide, so every route leads with one clear primary action (the header's `Contact` button, the footer's oversized link, the form's send control) and everything else is quieter; and it has to support exploring, so the case study rows and the article rows repeat one scannable shape all the way down.

**Scale over pixels.** The whole design is measured against one base unit, and every type size, line height, gutter and container padding is a clean whole or half multiple of it. The base unit is not the browser's default text size: it is slightly smaller on a wide laptop, marginally smaller again on a tablet, and slightly larger on a phone, and any smooth change that lands on those three reference widths is acceptable. Get the base right first; a build that converts a fixed pixel scale by hand will be subtly wrong at two widths out of three and at every width between. The exact unit is yours, so long as every size is a clean multiple of it.

**Type.** One neo-grotesque sans carries every word of body and heading text on the site, at five weights from light to bold and never thinner or heavier. One heavy display face at a single bold weight appears in exactly three places: the loader wordmark, the two-line wordmark on the home page, and the client name at the top of a case study. No monospace face is loaded, and no other face renders. The heading scale runs from a vast display step down through a large headline step, a medium headline step, a small headline step and a subhead step to three body steps, named large body, body and small body, and a tiny label step. Headings shrink as the screen narrows, and body copy does the opposite: the body step grows two steps on a phone while the large body and small body steps hold their desktop size there, and no body step ever shrinks, so a phone build that scales all type down uniformly is wrong on every paragraph. Only the two largest heading steps change at tablet width; everything else holds its desktop size there. The small headline step keeps its generous line height on a phone while its size drops, so its leading doubles, and that doubling is the rhythm of the phone drawer and the phone case study titles. The display step is so large that the wordmark `Ironwood` fills the full content width on a laptop, and the second line `Agency` sits under it. The exact families and sizes are yours, so long as those relationships hold.

**Colour by role.** Nine colours make the design, and they are named here by what they do. The dark ground is a near-black neutral and is the ground of the page itself and of every dark band. The light ground is plain white. The tinted ground is a near-white neutral, the third ground, also used to fill the header button. Body ink on light grounds is a deep neutral and is the most frequent colour on the site by a wide margin. Strong ink, for headings and links on light grounds, is the same near-black neutral as the dark ground. Muted ink, for secondary copy on light grounds, is a deep neutral a step lighter than body ink. All copy on dark grounds is white, and muted copy on dark grounds, including the header links at rest, is white at half strength. The border colour, used for the rule beneath each form field and the track of the send control's ring, is a near-white neutral clearly darker than the tinted ground. Four quieter structural values sit alongside: a faint near-black hairline between stacked rows on light grounds, a faint white track and rule on dark grounds, a still quieter white divider on dark grounds, and muted ink at half strength for tertiary copy. The small labels above the contact page's details are a mid neutral grey. The failure panel is the only pink surface on the whole site, a pale soft red, and pink appears nowhere else. The pointer ring is drawn in a mid neutral grey that belongs to it alone. The success panel sits on the tinted ground in strong ink. There is no warning surface. State chips in the studio and the account page differ by ground and weight within these roles, a `published` chip on the dark ground in white and a `draft` chip on the tinted ground in body ink, and every chip always carries its word. There is no brand hue: the identity is black, white, one pale grey and the lit sculpture, and a build that introduces an accent colour has invented one. The exact shades are yours, so long as those roles and exclusivity rules hold.

**Mode.** One designed theme, in which light and dark are properties of each band rather than a visitor preference; there is no visitor-selected mode and no dark-mode toggle.

**Grounds as structure.** Three grounds, and the order they appear in is the design: bands flip between them as a visitor scrolls, and no two neighbours ever match. Every public content route opens dark except the case study index, which opens white and then drops, with no transition band at all, into the darkest and longest band on the site (the error page, a single light band over a painted dark lower part, is the only other light opening); that hard edge is the loudest moment on the site and it is meant to be. Ground changes over dividers: sections separate by changing ground, never by a drawn line, and stacked rows inside a band separate by the faint hairline only. Where a band needs to fade into the next, it fades through a soft vertical gradient between its own ground and the transparent, never through a shadow.

**Depth without shadow.** Nothing on this site casts a soft drop shadow. Elevation comes only from ground changes and from the real sculptures, which light their own subjects and cast their own soft contact shadows. There is exactly one diagonal in the design: a hard two-tone split with no blend between the halves, behind the services hero. There is no grain, no speckle and no noise overlay anywhere; every surface is flat colour or a rendered object.

**The column lines.** On a wide screen the content column has three recurring vertical lines: an indent line, a centre line and a right edge. Headings, body copy, rows and footer blocks snap to those three lines on the home page, the contact page, the article archive and the footer, and that repetition is the closest thing this design has to a grid. The about page's journey section is the only text block that starts at the container edge instead of the indent line. The container keeps generous side padding that halves on a tablet and halves again on a phone.

**Shape.** Corners are nearly square throughout. Case study gallery images are softly rounded, and a softer modifier rounds a few of them further, including the first case study video block. The tablet mockup inside a case study is the only nested shape: a frame holding a screen with its own rounder corners and an even bezel on every side. The share buttons on an article, the social marks and the tiny dot separators are the only circles.

**Imagery.** Client marks, partner marks and award badges are drained of all colour and set at low strength. Team portraits are drained of saturation. The sculpture, the culture objects and the rock form are faceted and dark, lit so each flat face catches the light separately with a hard edge between faces and no smoothing across them; a smooth, soft-looking animal is as wrong as a crude one.

**Links and controls.** Every text link carries a painted rule of its own full width, drawn from the bottom of the link's box rather than as a border or a text decoration, and squashed to no width at rest. Pointing at the link grows the rule out to full width while the text brightens from half strength to full, and the two animate together. The header `Contact` button does something different: it empties rather than changing colour, its pale fill draining away completely to leave the label floating on the dark page, and the label brightens in about half the time the fill takes to go. Every arrow on a row or link has an invisible twin parked one diagonal step behind it; on pointing, and as the row scrolls in, the arrow leaves along its own diagonal and its twin arrives from behind, and the pair moves together. The drawer trigger's two short rules each have a twin parked outside a window that hides it; on pointing, each rule sweeps out of its window while its twin slides in from the opposite side, the top pair moving right and the bottom pair moving left, and neither rule ever stretches or fades. Every control has resting, pointed-at, pressed, focused and unavailable states, and unavailable is never shown by colour alone.

**Motion character.** Movement here reads as the page responding to the reader's hand, not as a show playing on its own. Scroll is interpolated rather than native, so a position between two input events still produces a frame, and almost every reveal is driven directly by scroll position, which means scrolling back up runs every reveal backward exactly. Headings arrive one word at a time: each word starts a short distance below its place and invisible, and rises into place while fading in as its section comes up, and the words of one heading never all arrive together, so it reads as writing appearing rather than a block fading in. Larger blocks travel further than words and the largest blocks travel furthest, three distances in all. Case study pictures sit inside a window smaller than the picture, with the picture enlarged inside it; as the row comes into view the window opens outward while the picture settles back to its true size, both driven by the same progress, so the picture seems pushed outward by the opening frame rather than dragged along behind it. The system pointer is replaced by a custom cursor, a thin ring that trails behind the pointer rather than tracking it exactly, and turns slowly and continuously whether or not the pointer moves, so slowly that it reads as drift rather than spin. The footer is already sitting underneath each page; as the page's last band scrolls away it is uncovered, like lifting a sheet off a table, rather than sliding up from below. The CSS layer is reserved for small discrete changes on specific properties of specific components, a link brightening or a button emptying; no blanket transition applies to every element, and nothing animates a property that changes the page's layout while scrolling. Every hover treatment is limited to pointers that can hover, so nothing sticks highlighted after a tap. The exact speeds and curves are yours, so long as those characters hold.

**Where motion is absent, deliberately.** The about page has no scroll-driven movement at any width, and neither do the privacy policy, the terms page or the error page. That stillness is a decision; adding motion there is new scope, not restoration. The editor studio and the account page carry no scroll-driven motion and no sculpture.

**Responsive behaviour.** The layout is designed for three reference widths, a wide laptop, a tablet and a phone, and must hold at every viewport width between them without horizontal scrolling. Motion is cut back by width in a fixed pattern. The case study index's four-stage row reveal happens on a laptop only; on a tablet and a phone the rows simply sit there, and only the arrow slide survives. Case study pictures move and fade on a laptop, fade without moving on a tablet, and neither move nor fade on a phone. The home page loses its live sculpture below laptop width and shows the still instead, and its scattered culture objects become a plain two-column grid of equal squares, the first bleeding slightly off the left edge on a phone. The hive motif on the services page is the one piece of movement that is never switched off at any width. Below the phone breakpoint the header's four links give way and the drawer is the only navigation; the logo there inverts against whatever passes behind it, exactly like the drawer trigger.

**Accessibility floors.** The whole site meets WCAG 2.2 AA. Text contrast is at least 4.5 to 1 against whatever is actually behind it. Navigation text must hold that bar on every route, including the case study index where the header sits over a white band; the half-strength white rest colour does not, so the header there must take a ground of its own, invert against the band like the trigger does, or change its rest colour for that route. Every heading split into words is exposed as one accessible name, its word fragments and the separator elements between service tags are hidden from assistive technology, and under a reduced-motion preference the split is skipped and the heading renders as plain text at full strength. Full keyboard navigation reaches and operates everything a pointer can, with a visible focus ring that meets contrast on all three grounds and a focus order that follows reading order. Where a row carries a decorative arrow, the whole row is the target and the arrow is not separately focusable. Every interactive target meets the WCAG 2.2 minimum target size. Icon-only controls carry labels. Every content image carries alternative text and decorative images declare themselves decorative. The custom pointer ring is suppressed when the device has no fine pointer and when the visitor prefers reduced motion; under that preference the scroll driver also switches off in favour of native scrolling, which must never break keyboard scrolling, in-page anchors or focus, and every scroll-driven effect renders in its final state rather than its resting state. Nothing is hidden and no meaning is lost when motion is reduced. Meaning is never carried by colour alone: an enquiry's state, an entry's state and an active tab each carry a word as well as a colour.

**The studio and the account page.** A quiet, dense working register: a fixed left sidebar reading `Entries`, `New entry`, `Enquiries` and `Sign out`, a card grid of entries at compact density with the title, kind, slug and a state chip on each card, the three-step wizard with its step names always visible, and outcomes reported by inline banners in place, never by a corner message that disappears on a timer. Every panel that covers the page closes on Escape. Unpublishing asks once before it runs, and the confirming control names the entry it will withdraw.

**What it must not look like.** No page dominated by a single hue family with no second signal: the site is monochrome plus the lit sculptures, and the third-party accents its reference build loaded, a vivid blue, a light cyan, a vivid teal, a soft teal, a vivid red, a vivid violet, a vivid amber and a vivid indigo, never render anywhere. No soft drop shadow, no glass blur, no grain. No decoration standing in for content: the sculptures are the only ornament. No marketing composition inside the studio or the account page. No flattening of the faceted sculpture into a smooth or cartoon form. **Space over dividers** on the public routes, where a reader is being led down a page; **hairlines over space** only between stacked rows of the same kind, where a reader is comparing one row with the next.

## Technical requirements

The backend is Django with its template engine on Python 3.12, and every public route is complete in the HTML the server sends: a visitor with scripting unavailable reads the whole site, and client code only enhances it. The frontend is HTMX over those server templates: navigation between routes is boosted so the server's page body is swapped in without reloading the document, and appended pages and in-place panels arrive the same way. The browser code that drives the scroll behaviour, the per-word reveal and the live scenes is bundled when the image is built; Node 20 is available in the image for that bundling only, and nothing Node-based serves traffic. The HTTP API is served under the `/api` prefix on the same origin. The datastore is PostgreSQL, reached through `DATABASE_URL`. The object store is MinIO, reached through `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Authentication is email and password implemented in this application, with bearer tokens. `GET /api/health` returns `200` once the app is ready. Requests are logged as structured records to standard output.

The libraries for the scroll driver, the per-word reveal and the 3D scenes, and the bundler, are your choice, and are permitted alongside the libraries named here. Use only the libraries named here, those, and their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation. Both are already running and reachable at the variables above; do not download, install, compile or start a copy of either.

**What the scroll layer must be capable of.** A scroll position interpolated between input events and exposed to every effect on every frame; timelines scrubbed against that position rather than played on a clock; a per-frame callback the scenes can read; and survival across a page swap without being rebuilt. The drawer trigger, the pointer ring and the scroll driver persist across route changes; the scenes do not.

**What the scene layer must be capable of.** Real-time rendering in the browser's own 3D graphics context of a lit, flat-shaded polygonal object with a single dominant key light and no texture map, over a page-length scroll, without dropping frames. Each scene mounts into a box the page layout already sized and lays nothing out itself, and the scene layer mounts per route rather than once per application, so a route with no scene never creates a renderer. The full-height scene on the case study index must never allocate a drawing surface as tall as its band: it renders at the height of the viewport and is moved against scroll, because a surface the height of six screens on a high-density display is larger than most machines will hold. A scene outside the visible region stops drawing.

**The three layers stay separable.** Page structure (bands, containers, rows), behaviour (hover, reveal, loops) and scenes are kept apart: a behaviour attaches to an element the structure produced without that element being authored differently, and a scene fills a box without laying anything out. Per-instance spacing between case study blocks is expressed as one spacing scale applied by a single modifier, never as a separate named rule per value.

**No binary asset ships.** No video file, no 3D model file, no photograph, no raster image, no icon file and no icon font is shipped with the build or referenced by any page. The mascot, the seven culture objects, the rock form, the hive and the three bees are composed from simple solids at build or render time and given flat faces: the badger from a capsule body, a rounded box head, four tapered limbs and two small cone ears; the rocket from a cone nose on a cylinder body with three flattened fins; the wand as a tapered cylinder with a star at the tip; the arrow as the arrow mark given depth; the bomb as a sphere with a collar and a coiled tube fuse; the thumb as a rounded glove with four capsule fingers, one raised thumb and a cuff; the bond as two spheres of unequal size joined by a short capsule with a third sphere alongside; the flame as a flame profile turned and twisted about its upright axis; the hive as a stack of rings narrowing toward the bottom hung from a tapered branch with short forks; each bee as a capsule body with two flattened wings and two short antennae; the sculpture reads correctly only in a middle band of detail, coarse enough that each face catches the light and fine enough that the silhouette holds. Every still of a sculpture is rendered once from the same geometry, at the same light, rather than shipped as an image. The looping bees are small drawn objects animated by their loop rather than video playback. Client marks and award badges are generated placeholders: settings of their names, never photographic. Team portraits and case study imagery are generated from a seed, using only the site's own grounds, at the box each block calls for. Every icon and the logo mark are inline vector geometry that takes its colour from the surrounding text, and the arrow's stroke thickness scales with the text beside it, so the same arrow reads correctly small in an article row and large in the footer. Images an editor uploads are content, not shipped assets, and live in the bucket.

**Performance.** The site spends its rendering budget only where a scene is on screen. The home page carries eight live scenes and no video; the services page carries no scene and only its four drawn loops; every other route carries neither. Scrolling holds the display's own refresh rate on a mid-range laptop with both case study index scenes visible.

The site must also stay smooth and responsive with both scenes on screen on the case study index, with the full article archive, and with a case study document many screens long.

**Fonts.** Exactly two typefaces are downloaded, the sans and the display face, both open-licence families of your choosing, from files installed at image build time; those two font files are the one permitted exception to the no-binary rule; no monospace face, no icon font and no typeface that would sit loaded but unused on every route loads. Every face declares a swap behaviour so text is readable before the face arrives, and the fallback stack is the chosen family, then a system grotesque, then the generic sans.

**Third-party code.** None. No analytics, no tag manager, no captcha service, no font service and no outbound call of any kind at run time. The bot check is the application's own.

## Data model

Fifteen tables. All timestamps are UTC. Ids are integers, slugs are kebab-case and start with a letter.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

### `app_user`

`id`, `email` unique across the product, `password_digest`, `role` in `editor` or `client`, `display_name`, `created_at`.

### `service`

`id`, `name` unique, `sort_order`. Exactly eight rows: `Design thinking workshop`, `UX/UI design`, `Fractional CTO`, `Website development`, `Dedicated team`, `Software development`, `Branding design`, `Website design`.

### `case_study` and `case_study_service`

`case_study` carries `id`, `slug`, `name`, `label`, `title`, `subtitle`, `summary`, `body`, `year`, `website_url`, `owner_id` referencing `app_user`, `state` in `draft` or `published`, `published_at` which is null until publication, `sort_order`, `created_at`, `updated_at`. At most one case study in state `published` holds any given slug. `case_study_service` carries `case_study_id` and `service_id`; the pair is the key and both must exist.

### `article_category` and `article`

`article_category` carries `id`, `slug` unique, `name`, `sort_order`. `article` carries `id`, `slug`, `title`, `summary`, `body`, `category_id` referencing exactly one `article_category`, `read_minutes`, `owner_id`, `state` in `draft` or `published`, `published_at`, `created_at`, `updated_at`. At most one article in state `published` holds any given slug.

### `media_asset`

`id`, `entry_kind` in `case-study` or `article`, `entry_id`, `object_key` unique across the product, `content_type`, `byte_size`, `alt_text`, `created_at`. `object_key` always matches `media/{kind}/{entry_id}/{sha256_of_bytes}.{ext}`. The bytes are in the bucket and in no other place.

### `enquiry` and `bot_check_token`

`enquiry` carries `id`, `service`, `budget`, `name`, `email`, `message`, `state` in `new`, `in_conversation` or `closed`, `client_id` which is null for an anonymous enquiry, `created_at`, `updated_at`. `service` is always one of the eight service names and `budget` one of the five budget options. `bot_check_token` carries `id`, `token` unique, `issued_at` and `used_at`, which is null until the token is spent.

### The content tables

`culture_value` (`id`, `title`, `body`, `object_name`, `sort_order`), `testimonial` (`id`, `name`, `role`, `quote`, `body`, `sort_order`), `award_badge` (`id`, `name`, `link_url`, `sort_order`), `client_logo` (`id`, `name`, `placement` in `home` or `partner`, `sort_order`), `team_member` (`id`, `name`, `role`, `profile_url`, `sort_order`) and `office` (`id`, `label`, `street`, `city`, `phone`, `sort_order`). The pages read these tables; none of their content is typed into a template.

### Derived rather than stored

Whether an entry is readable by a caller is derived from its `state` and its `owner_id` together with the caller, and is never a column. A category's entry count is computed on read from its published articles. The next project on a case study page is computed on read from index order. The case study index order is computed from `sort_order` among published case studies. The sitemap is computed on read from the published rows. No count that can be computed from rows is kept in a column of its own.

### Seed data

Three accounts as named in `## User roles`. Eight services. Three categories: `Product design` with slug `product-design`, `Engineering` with slug `engineering`, `Studio life` with slug `studio-life`.

Ten published case studies owned by `editor@example.com`, in index order:

| Name | Slug | Label | Title | Year | Services |
|---|---|---|---|---|---|
| `Lumen Pay` | `lumen-pay` | `Fintech` | `A payments app that settles an invoice in one tap` | `2026` | UX/UI design, Software development, Branding design |
| `Haven Health` | `haven-health` | `Healthcare` | `A patient portal that makes a clinic visit feel shorter` | `2025` | UX/UI design, Website development |
| `Kitefolio` | `kitefolio` | `SaaS` | `A portfolio builder for designers who hate building portfolios` | `2025` | Design thinking workshop, Software development |
| `Orchard Market` | `orchard-market` | `E-commerce` | `A grocery storefront that restocks before the shelf is empty` | `2025` | Website design, Website development |
| `Tidewater` | `tidewater` | `Travel` | `A booking flow that fits a whole trip on one screen` | `2024` | UX/UI design, Dedicated team |
| `Northstar Learning` | `northstar-learning` | `Education` | `A course platform where every lesson ends with something built` | `2024` | Software development, Dedicated team |
| `Quill and Ink` | `quill-and-ink` | `Publishing` | `An editorial system for a newsroom that never sleeps` | `2024` | Fractional CTO, Software development |
| `Parcelio` | `parcelio` | `Logistics` | `A courier dashboard that shows every parcel at once` | `2023` | UX/UI design, Software development |
| `Verde Energy` | `verde-energy` | `Energy` | `A home energy app that turns a bill into a plan` | `2023` | Branding design, UX/UI design |
| `Atlas Freight` | `atlas-freight` | `Supply chain` | `A freight marketplace that quotes in seconds` | `2023` | Fractional CTO, Website development |

Every seeded case study's subtitle reads its label followed by ` product, designed and built by Iron Wood` (for example `Fintech product, designed and built by Iron Wood`), its summary repeats its title, and its site address is `https://` followed by its slug and `.example.com` (for example `https://lumen-pay.example.com`). The body of each is two or more paragraphs written for that product.

One draft case study named `Nightjar` with slug `nightjar`, owned by `editor@example.com`, with one stored PNG image whose alternative text is `Nightjar concept board`.

Six published articles, owned by `editor@example.com`, newest first:

| Title | Slug | Category | Reading time | Published |
|---|---|---|---|---|
| `Shipping an MVP in eight weeks` | `shipping-an-mvp-in-eight-weeks` | Engineering | `7 min read` | `Sep 2, 2026` |
| `Field notes from a design thinking workshop` | `design-thinking-workshop-field-notes` | Product design | `5 min read` | `Aug 26, 2026` |
| `Five questions to ask before you hire a studio` | `five-questions-before-you-hire-a-studio` | Studio life | `6 min read` | `Aug 19, 2026` |
| `When to bring in a fractional CTO` | `when-to-bring-in-a-fractional-cto` | Engineering | `8 min read` | `Aug 5, 2026` |
| `Designing onboarding that converts` | `designing-onboarding-that-converts` | Product design | `4 min read` | `Jul 22, 2026` |
| `A week inside the studio` | `a-week-inside-the-studio` | Studio life | `3 min read` | `Jul 8, 2026` |

One draft article titled `Hiring a design partner in 2027` with slug `hiring-a-design-partner`, category Studio life, owned by `editor2@example.com`.

Seven culture values, in page order, each paired with its object: `Lift-off ready` with `rocket`, `We plan for launch day from the first sketch, so nothing important is left for the last week.`; `Technomagicians` with `wand`, `Tech and design - that's where we shine. We have the knowledge and tools to bring all of your ideas to life, even the craziest ones. Let the magic begin!`; `Aim for the point` with `arrow`, `Every screen we design answers one question for one person. Anything that does not is cut.`; `Go wow or go home` with `bomb`, `We're not that average team with mediocre attitude. Our working ethos is to create "WOW!" - worthy products which stay both in the now and the future.`; `Win-Win partnership` with `thumb`, `Truly great things are never accomplished alone. We work as your companion, your best buddy, and your silent backbone to thrive further together.`; `Bonding together` with `bond`, `We work in one room with your team, share the same board, and celebrate the same releases.`; `Keep the fire` with `flame`, `Curiosity is the job. We keep learning, keep prototyping, and keep the work warm between projects.`

Three testimonials: `Mara Lindqvist`, `Head of Product, Lumen Pay`, quote `The items were delivered on time and in great quality.`, body `Iron Wood delivered the project on time with excellent quality, actively listening to feedback and making appropriate changes. Their attention to detail and storytelling approach were impressive. Customer service was commendable, ensuring a positive experience.`; `Tomas Reyes`, `Founder, Orchard Market`, quote `They were a professional, experienced team with outstanding ideas.`, body `Iron Wood delivered a successful project tailored to the client's needs, leaving the client satisfied with the engagement. Their excellent design and development skills and timeliness brought visual advancement to the brand. Communication was efficient through regular meetings and emails.`; `Priya Anand`, `Marketing Lead, Haven Health`, quote `The team was always accommodating and supportive.`, body `The client was pleased with the visual appeal and flow of the website. Iron Wood was highly communicative with the project's outlines, and internal stakeholders were particularly impressed with the vendor's design prowess.`

Five award badges: `Pixel Guild Site of the Day`, `Studio Honors Gold`, `Product Craft Award`, `Design Circle Pick`, `Web Makers Top Studio`. Five home client marks: Lumen Pay, Haven Health, Kitefolio, Orchard Market, Tidewater. Seven partner marks: those five plus Northstar Learning and Parcelio. Six team members: `Hana Ito`, Design Director; `Marco Silva`, Engineering Lead; `Ruth Okafor`, Product Strategist; `Dev Patel`, Senior Product Designer; `Ingrid Moe`, Frontend Engineer; `Sam Carter`, Project Manager. Two offices: `First Office` at `85 Example St, District 4,` and `Example City, Country`; `Second Office` at `60 Example Pl, Example NSW 2000`. The first office telephone is `+1 555 0100` and the second is `+61 2 5550 0100`. Each award badge links to `https://awards.example.com/` followed by its name in kebab-case, and each team member's profile link is `https://example.com/team/` followed by the lowercase first name.

Two enquiries: one from `client@example.com` attached to that account, name `Leo Marsh`, service `UX/UI design`, budget `$30k - $60k`, message `We need a redesign of our booking app before the spring launch.`, state `new`; and one anonymous from `ada.quinn@example.com`, name `Ada Quinn`, service `Website development`, budget `$10k - $30k`, message `We want a faster marketing site with a case study library.`, state `in_conversation`.

Seeding is idempotent. Restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual composition of every route and the global chrome. Nothing here restates a rule from `## Core features` or `## UI/UX notes`; where a value is not given, it is a design preference and yours to choose within the relationships stated.

### The loader

On first load a full-viewport panel on the dark ground covers the page, carrying the brand mark centred, a thin progress track beneath it on the faint white track colour with a white fill, and a numeric counter beneath the track followed by `%`. The counter counts up to `100` against real loading progress, the fill reaches the full width of the track at the same moment, and then the panel leaves upward, off the top of the viewport. It is the topmost layer on the site. It returns briefly as part of a route change, so it belongs to the page swap rather than being a first-load splash only. Under a reduced-motion preference it appears already complete and leaves without travelling.

### The header

A transparent strip across the top of every route that scrolls away with the page rather than sticking. Left to right: the logo mark on the indent side, then the four links on the indent line, evenly spaced by a constant gap rather than placed in equal cells, then, at the right edge, the `Contact` button filled with the tinted ground and dark label. The links sit at half-strength white at rest.

### The drawer and its trigger

The trigger is a small white square fixed near the top right corner, above everything except the loader, holding two short dark horizontal rules a small distance apart. It inverts against whatever passes behind it, so it reads as a white square with dark rules over dark bands and as a dark square with light rules over light bands, with no flicker at a band boundary and without the page measuring what is behind it. It is the only element that holds its place through a page swap.

The drawer is fixed, inert to the pointer while closed, and parked fully off the right edge. Opening it slides a panel in from the right. The panel is two columns: a wide navigation column holding the six links in a single column at the small headline step, one per line on an even pitch, and a narrower detail column holding the social labels in two short columns, the two mailboxes under their labels, and beneath both columns the two office addresses. The links move and fade in one after another rather than arriving as a block. Escape and a press outside the panel close it, and focus returns to the trigger.

### The pointer ring

A thin circle drawn in its own mid grey with a stroke that is a small fraction of its size, following the pointer as described in `## UI/UX notes`.

### The footer

A tall white block. On the indent line: the lead-in line, then beneath it the oversized link at the large headline step, underlined by the painted rule, with the large arrow at its end; this is the largest interactive target on the site. Beneath: the two office labels on the indent and centre lines, with the first office on two lines and the second on one. Beneath: the copyright line on the indent line, the `Privacy Policy` and `Terms` links under it, and the six social labels in two rows starting at the centre line. On the right, the standing still of the sculpture fills a tall box that reaches almost the full height of the footer.

### Iconography

Every mark is inline geometry that inherits its colour. The logo mark is the studio's own faceted animal silhouette in two exports: a small one for the header, the drawer and the loader, and a very large one used as a ghosted watermark behind the culture section. The arrow is a corner pointing up and to the right with a shaft meeting it on the same diagonal as the corner. The pagination mark is a single chevron. The close mark is two crossed rules in a box slightly wider than it is tall. The social marks are small filled glyphs. The bordered mark on a team card carries its own hairline frame drawn so the stroke sits exactly on the edge of its box. The send control's ring is two concentric circles in the same place: a fixed track in the border colour and, exactly on top of it, a ring in the inherited ink that fills around the circle while the enquiry is sending.

### Route: home

Four bands: dark (hero and process), light (culture), dark (clients), tinted (testimonials), then the footer.

The hero. The two-line wordmark `Ironwood` / `Agency` fills the content width in the display face, painted only marginally lighter than the dark ground, so it reads as a watermark the sculpture stands in front of rather than as a headline. The live sculpture of the standing honey badger sits in a large square stage in front of the wordmark, overlapping its first letters and hanging off the left edge of the viewport. The sculpture faces three-quarters left at rest and fills the left half of the frame; as the page scrolls it grows and shifts right, then leaves the frame. Its stage stays pinned for a distance longer than the hero itself, so the ground beneath it has already turned to the process section's dark while the sculpture is still standing there; only then does it release. A soft fade joins the hero to the block below it.

The intro block sits on the right column beneath the hero: the heading `Award-winning digital agency specializing in design and development`, then two paragraphs, `We support worldwide businesses and startups by turning their visions into digital products that drive substantial results.` and `Our goal is to craft remarkable digital experiences that spark conversation, adding strategic value to brands through our expertise in design and development, whether it be in finance, e-commerce, tech or arts.`, then the link `See our services`, then the award strip: five badges in a row, each a small drained square linking to its award.

The process section. Centred on the viewport, a tall well holds the six process words stacked one per line, `Empathize`, `Define`, `Ideate`, `Prototype`, `Test`, `Repeat`, each arriving on scroll into its own line. Beneath them, centred, the two-line paragraph `We rapidly transform ideas into problem-solving products, designed to adapt swiftly to the evolving market demands.` and the single link `See our work` to `/works`.

The culture section. The heading `Our culture, mantra, and beliefs`, centred, over the very large ghosted watermark of the logo, which is already on screen while the process section is still finishing. The seven culture objects float in a composed scatter down the section in alternating columns, not on a grid: the third sits higher than the second and the fifth higher than the fourth. Each object is rendered into a frame noticeably larger than the space it occupies, so it can move without being clipped. Each rotates slowly about its vertical axis and bobs gently, each out of step with the others so no two move together. Each casts a soft contact shadow onto the white ground and is drawn in the same dark faceted material as the mascot. Beside each object sits its culture value: the title in the large body step at a semibold weight over the body in the small body step, in a deliberately narrow column of roughly a short phrase per line.

The client strip. The heading `We've been doing brilliant work with brilliant brands`, centred over two lines, the line `We team up with great minds who think alike, regardless of business size.` beneath it, then five equal tiles across the container, each holding a drained client mark at low strength. The tiles arrive one after another.

The testimonials. The heading `What our clients talk about us` on the indent line, then three entries separated by the faint hairline, each a two-column entry: a narrow attribution column (name in semibold, role, a small generated avatar) and a wide quote column carrying the quote at the subhead step over its body at the large body step. Each entry arrives on its own.

### Route: services

Four bands: dark (hero), light (service list), dark (how the studio works), tinted (the team promise), then the footer.

The hero carries, on the indent line, the four-line sentence `We build business-savvy products from the hive of creativity blended with the latest technology trends.` set a step smaller than every other page's hero because it is the longest, and the right half of the band is given to the motif. The word `hive` is the first of the site's two mascot metaphors; the contact hero's `buzz` is the second, and both sit in the largest type on their routes. The hard two-tone diagonal split sits behind the hero.

The hive motif spans the whole service band and is mirrored horizontally. A dark branch reaches in from above the band's top edge and a hanging hive hangs from it across the boundary between the dark and light grounds, reading correctly against both. Three bees, small flying creatures orbiting the hive, circle it. The hive sways continuously on a slow loop; each bee bobs continuously on a loop half as long, one of the three moving in the opposite phase, so the group never looks synchronised. Scrolling also moves the whole group down the band, and the two motions add together rather than one replacing the other, so the motif never freezes while scrolling and never jumps when scrolling stops. The loops never restart on scroll. The swaying hive and the three bobbing bees are the four continuous animation loops on the services page; the pointer ring's slow endless turn is the site's fifth continuous animation, and the seven culture objects rotate and bob continuously in their own scenes; apart from these and the generated looping sequence on each case study page, nothing on the site loops.

The service list carries the label `Agency Services` and seven wide offering rows on the indent line. These offering rows are fixed page copy, separate from the eight services the `service` table holds, and each row's narrow tag column lists services drawn from those eight. Each row carries a name, its body, and that tag column on the centre line, whose tags fade in one by one. The rows are `MVP`, with `We offer a comprehensive package encompassing both design and development to quickly bring your MVP to life. Our goal is to encapsulate your product's core features and value proposition into a streamlined version that can be launched swiftly.` and `This approach allows for rapid market testing, user feedback collection, and further product refinement.`; `UX/UI design`, with `We provide a variety of design services for websites, SaaS (Software as a Service) applications, and mobile applications. More than just making visually pleasing interfaces, our team focuses on the user-centric design approach to provide you with high-converting solutions.` and `We make "technology meets aesthetic" happen while achieving your business goals.`; `Website development`, with `We build fast, accessible marketing sites and web apps that your team can keep editing long after launch.`; `Software development`, with `From the first interface to the hundredth release, we write the product code and the pipeline that ships it.`; `Branding design`, with `We shape the name, the mark and the voice so the product looks like one company everywhere it appears.`; `Dedicated team`, with `A standing squad of designers and engineers who join your planning, your stand-ups and your release train.`; and `Fractional CTO`, with `A senior technical lead for the months when you need architecture decisions and hiring judgement more than another pair of hands.`

How the studio works. The heading `How we work with you` in a narrow column on the centre line, followed by three items, each a subhead over a two-line body: `Discover`, `We start with your users, your numbers and your deadline, and agree what success looks like.`; `Design`, `We prototype early and put real screens in front of real people before a line of production code.`; `Deliver`, `We ship in small releases with your team in the room, and stay until the product runs without us.` On the left, a tall generated picture bleeds off the left edge of the viewport, with a soft fade at its foot that stops it against the band boundary.

The team promise. The heading `A team that ships alongside yours` over four lines on the indent line, then rows pairing a short label on the indent line with a paragraph on the centre line: `Senior by default`, `Every project is led by people who have shipped products of your size before.`; `One channel, one owner`, `You always know who is responsible and where the conversation lives.`; `Built to hand over`, `We document as we go, so your team can own the product the day we step back.`

### Route: case study index

Two bands: light (hero), dark (the list), then the footer.

The hero carries a three-line heading on the indent side, `We build` / `award-winning products` / `that everyone loves.`, and leaves the right half of the band empty so the inversion below has nothing to compete with.

The list band carries the full-height background scene behind every row: the faceted honey badger, lit, on a slow field of the same dark faceted material, moving as the page scrolls. The ten rows run down the band on an even pitch, each as tall as its picture, with a generous gap between rows. A row's picture well is a little over half the container width and a little under two-thirds as tall as it is wide; the text column takes the other side. Each row reveals in four ordered stages against its own scroll progress: the label, then the title word by word, then the service tags, then the arrow, each rising while fading in, while the picture well opens from its inset window with the picture settling back from enlarged. The service tags are set inline at the body step with a small separator between each pair. The second row's picture is replaced, when the pointer enters that row, by the live preview scene in exactly the same box, and the swap never changes the row's size or position; the preview follows the pointer from row to row, showing a live rendering in place of each row's picture while the pointer is over it.

### Route: case study

Three bands: dark (hero), light (the document), dark (next project), then the footer. It is the longest template on the site by a wide margin and reads as a document rather than a page.

The hero centres the client name in the display face at the display step, with the subtitle centred beneath it at the subhead step.

The fact sheet puts the facts hard against the far left and the services list hard against the far right, with the whole middle empty. The facts are the client name at the small headline step, the `Visit site` link carrying both the painted underline and the arrow substitution (the only link on the site carrying both), then the `Industry` label with its value and the `Year` label with its value, each label in the body step over its value.

The document is a long sequence of media blocks at three recurring widths: a standard width, a wider width, and one block that bleeds off both edges of the viewport. A wide video-like block holds a generated looping sequence inset by a hairline so the frame shows around it, and a second, softer-cornered block further down holds another generated looping sequence of the product in use. A gallery pairs images of different sizes. A tablet mockup nests a rounded screen inside its frame. The document closes on a fixed wide landscape picture. Vertical spacing between blocks follows one spacing scale. The ground of the document changes partway down: bands of the other ground are painted behind the blocks rather than by the band itself, so a picture can sit exactly across the line where white becomes dark, and the picture's position and the colour boundary are placed independently. A soft fade at the foot of the document joins it to the next band. Images drift against scroll at slightly different rates from each other on a laptop, a parallax that gives the page depth; the softer-cornered gallery images drift at a different rate from the others. The editor's uploaded images appear within this sequence, in upload order, each with its alternative text.

The next-project section fills exactly one viewport: the next case study's generated picture full-bleed, darkened toward its foot so the words stay readable, with `Next project` centred at the subhead step and the next case study's title centred beneath it.

### Route: about

Four bands: dark (hero), light (journey), dark (team), tinted (offices), then the footer. Nothing moves on scroll.

The hero is the only opening on the site with no headline over it: the still of the honey badger seated in a chair, centred. The page still carries a heading for assistive technology, `About Iron Wood`, visually hidden.

The journey section starts at the container edge rather than the indent line: the heading `Our journey`, the paragraph `Iron Wood started as two designers and an engineer who wanted to build products the way they wished studios had built theirs. Today the studio works across two offices with founders and product teams in finance, e-commerce, health and the arts.`, a tall generated picture on the right, and beneath both a band carrying the label `Trusted by product teams at` over seven drained partner marks in one row.

The team section is a three-column grid on the indent line with an even gutter: six cards, each a drained portrait taller than it is wide, then the name at the subhead step and the role beneath, with the bordered mark aligned to the card's right edge on the name's baseline, resting at low strength and brightening on pointing. The section heading reads `The people behind the work`.

The office section pairs the office image box on the indent line with the heading `Two offices, one studio` and the office list on the centre line: each office's label, street and city, and telephone number, with its switch button.

### Route: article archive and category

Two bands: dark (hero), tinted (the list), then the footer. The archive and a category route share one template and one height.

The hero is the shortest on the site, with more space above its heading than below: the heading `Insights from the studio` on the indent line.

The tabs sit at the top of the list band on the indent line: `All` alone, then the three category tabs as a group at the subhead step, each with its small count. The current tab's painted underline grows in as the page scrolls rather than simply being present.

Each row spans the content width on the indent line: the category in the small label step, a generous title well at the small headline step, then a meta line with the date and reading time separated by a tiny round dot, and at the far right the small arrow with its twin. The dot on this light ground is white at low strength, barely visible, which is the measured design. Rows are separated by the faint hairline. The `More` control is a single centred square button holding its label and the chevron.

### Route: article

Three bands: dark (hero), light (body), tinted (related), then the footer.

The title block sits on the indent line at the large headline step over two lines, then a meta line carrying the date and reading time separated by the light-ground variant of the dot. Below it the hero picture sits in a full-width window, enlarged inside that window so it overhangs equally left and right and overhangs mostly downward; as the page scrolls the window and the picture move at two different rates, the window fading while the picture does not. A soft fade darkens the foot of the window. Directly beneath the window, full-bleed and pinned below the hero rather than to the top of the viewport, runs the thin reading progress bar, which fills horizontally in proportion to progress through the body.

The body pairs a narrow sidebar at the container edge with a wide reading column. The sidebar holds `Contents`, listing the body's headings as in-page links, and the share links as small circular buttons, and it stays with the reader for the whole length of the body. The related section is headed `Related articles` and carries up to two cards side by side, each the archive row at half width; a category holding only one other published article shows a single card.

### Route: contact

Two bands: dark (hero), light (main). There is no footer; the page ends on the form.

The hero has three columns: the heading `Be our client. Get that buzz` in white on the indent line over three lines, then the two offices on the centre line and the right, each an office label in half-strength white over the address in white at a slightly brighter strength than the labels (the only body copy on the site at that strength), with the telephone number beneath. The standing still of the sculpture fills the right side of the page beside the hero.

The main band has the information column on the indent line and the form on the centre line. The information column stacks three items on an even pitch, each a tiny label in the mid grey over a link at the subhead step: `Email` with `hello@example.com`, `Careers` with `hr@example.com`, and `Follow us` with the six social labels set inline. This is the only place the tiny label step appears.

The form. No field is a box: each has no border except a rule beneath it in the border colour, a transparent ground, and its label sitting above the value. The layout is three rows: `Service` wide beside `Budget` narrow, then `Name` and `Email` as an equal pair, then `Message` across the full width. The two splits differ and both are deliberate. The send control sits at the bottom right, flush with the message field's right edge: a large square target holding the two-ring mark with the arrow centred in it, with the accessible name `Send enquiry`. While an enquiry is sending, the inner ring fills around the circle. The success panel and the failure panel sit in the form's place, hidden; the failure panel is the pale soft red surface with a small inner padding.

### Routes: privacy policy and terms

One dark hero band with the heading `Privacy Policy` or `Terms of Service`, then one light band holding a single centred text column at the large body step, a little wider than a comfortable measure, which is the measured design. Nothing moves.

### Route: error page

Exactly one viewport tall. The composition is centred: the heading `Sorry! The page you're looking for was not found` at the small headline step over two lines, then `404` at the display step set in the sans rather than the display face, then the `Back to home` link. The upper part of the viewport is the light ground and the lower part the dark ground, and the still of the rock form straddles that seam. The header, the drawer, the trigger and the pointer ring are present; the footer is not.

### Motion authored by eye

Some of this site's motion is authored by eye rather than from measurements: how the sculptures move between their three known poses, the speed and path of each loop, the drawer's opening movement, the loader's exit, and the trailing distance of the pointer ring. Those are design decisions for the builder within the characters stated above, not gaps to leave empty. The band between tablet and phone was never measured, and nothing is specified for it beyond the scale model and the rule that nothing scrolls sideways.

### Sign-in, sign-up and the account page

One dark band holding a centred form column in white ink, with no card around it: labels above fields, the error for a field directly beneath it, and one primary action. The sign-up form carries the terms sentence above its action. The account page lists the client's enquiries as rows with the service, the budget, the date and a state chip carrying a word.

## Constraints

Single tenancy: one studio, one site, one set of editors.

Not built, and not to be built: payments of any kind, email sending of any kind, a newsletter, site search, sorting, filtering beyond the category tabs, a language switch, a dark-mode toggle (light and dark here are per band, never a visitor preference), comments, reactions, a careers application flow (the careers mailbox is only an address), a client portal beyond the list of one's own enquiries, file attachments on enquiries, a native application, and any of the client products the case studies describe. Pagination state beyond the `page` query is not kept.

No email is sent by this product and no mail service is available. No payments provider, no cache, no queue, no search service and no realtime service is available; the only backing services are PostgreSQL and MinIO. No third-party script, font service, analytics or captcha service, and no outbound network call at run time.

No binary asset of any kind ships with the build. Every client, partner and award mark is a generated setting of a name the site invents and resembles no real trademark. Every person named on the site is invented. No real studio, client or person is named anywhere.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/sign-up` | `email`, `password`, `display_name` | `access_token`, `user` with `id`, `email`, `role`, `display_name` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `user` |
| `GET /api/services` | none | a top-level JSON array of services, each with `name` |
| `GET /api/case-studies` | `state` (optional; `draft` returns only the caller's own drafts) | a top-level JSON array of case studies in index order |
| `GET /api/case-studies/{slug}` | none | the published case study holding the slug, or else the caller's own draft holding it |
| `POST /api/case-studies` | `slug`, `name`, `label`, `title`, `subtitle`, `summary`, `body`, `year`, `website_url`, `services` (array of service names) | the created case study in state `draft` |
| `PATCH /api/case-studies/{id}` | any writable field | the updated case study |
| `POST /api/case-studies/{id}/publish` | none | the case study in state `published` with `published_at` set |
| `POST /api/case-studies/{id}/unpublish` | none | the case study in state `draft` |
| `POST /api/case-studies/{id}/media` | the file bytes as `file`, `alt_text` | `id`, `object_key`, `content_type`, `byte_size`, `alt_text` |
| `GET /api/articles` | `category` (a category slug), `page` (from `1`), `state` (optional; `draft` returns only the caller's own drafts) | a top-level JSON array of up to four articles, newest first |
| `GET /api/articles/{slug}` | none | the published article holding the slug, or else the caller's own draft holding it |
| `POST /api/articles` | `slug`, `title`, `summary`, `body`, `category` (a category slug), `read_minutes` | the created article in state `draft` |
| `PATCH /api/articles/{id}` | any writable field | the updated article |
| `POST /api/articles/{id}/publish` | none | the article in state `published` with `published_at` set |
| `POST /api/articles/{id}/unpublish` | none | the article in state `draft` |
| `POST /api/articles/{id}/media` | the file bytes as `file`, `alt_text` | `id`, `object_key`, `content_type`, `byte_size`, `alt_text` |
| `GET /api/article-categories` | none | a top-level JSON array of categories, each with `slug`, `name`, `entry_count` |
| `GET /api/media/{asset_id}/content` | none | the image bytes, streamed from the bucket |
| `GET /api/bot-check` | none | `token` |
| `POST /api/enquiries` | `Service`, `Budget`, `Name`, `Email`, `Message`, `bpGCap`, `Website` | the stored enquiry with `id` and `state` |
| `GET /api/enquiries` | none | a top-level JSON array of enquiries |
| `PATCH /api/enquiries/{id}` | `state` | the updated enquiry |
| `GET /api/health` | none | `200` |

A case study record carries `id`, `slug`, `name`, `label`, `title`, `subtitle`, `summary`, `body`, `year`, `website_url`, `services` as an array of service names, `state`, `published_at` and `media` as an array of asset records. An article record carries `id`, `slug`, `title`, `summary`, `body`, `category` with `slug` and `name`, `read_minutes`, `state`, `published_at` and `media`. An enquiry record carries `id`, `service`, `budget`, `name`, `email`, `message`, `state` and `created_at`.

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success. Bearer auth is required on every write and on `GET /api/enquiries`; the public read endpoints, `POST /api/enquiries`, `GET /api/bot-check`, login, sign-up and health are open.

### No mocks

The named provider is the fact. Any of the following is a contract violation: an in-memory list standing in for the case study or article tables, an uploaded image written to the app container's filesystem, a database column holding image bytes instead of an object key, a media endpoint that reports success without an object existing in the bucket, a case study list or the eight-service list typed into a template instead of read from the tables, a category count kept by hand, a sitemap written by hand, or an enquiry acknowledged on screen without a row being stored. The app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A founder can scroll the home page past the live honey badger, open a case study from the index and send an enquiry that is stored and confirmed in place. An editor can publish a case study with an image and see it join the index and the sitemap, while an unpublished entry and its images stay unreadable to everyone but its own editor.
