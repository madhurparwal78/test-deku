# Doudou Fever

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, pick a chapter of the Doudou Fever
comic from the record rack, read it panel by panel inside one full-window drawn scene, and, once a
tip of theirs has been verified, read the next chapter before its release moment, without hitting an
error page. A different stranger who has not tipped must NOT be able to read that unreleased chapter
by any means, including a direct request for its manifest or for any of its images with a valid
reader session of their own. The early access must come from a Tipbox notification whose signature
the app has checked over the exact bytes it received; a thank-you page the app shows to itself is
not a tip. Every panel image must live in the object store at its key; a copy on the app's own disk
does not count.

## Overview

Doudou Fever is a serialised interactive comic and the studio system that publishes it. It is made
by a two-person studio: Camille Rouyer draws it and Damien Lorca animates it. The comic follows
Doudou, a megalomaniac sheep who wants to become a DJ and make the world dance, with his flatmates
Jean-Loic, a wild barman, and Milan, a future cooking star on socials. It is free, it ships in two
languages (English and French), and it is paid for by tips on Tipbox, a hosted creator-tipping service run by a third party.

The product has three surfaces. The **reading surface** is a small public site: a title screen, a
chapter rack dressed as a shelf of records where chapters are called tracks, a chapter reader, an
about page and a legal page, all sharing one persistent drawn canvas that fills the window and never
unmounts. A reader does not scroll a column of images: they travel along a chapter panel by panel,
by arrow keys, the mouse wheel, dragging, small arrow controls or a timeline slider. The **studio
console** is a private document application where the two authors create volumes and chapters,
import layered panel artwork, tune each layer's depth, translate every string, schedule chapter
drops, and watch tips and reading numbers arrive. The **delivery layer** is the service and object
store behind both: it decides who may read what, streams panel images, and records tips.

The comic is organised in four levels. A **volume** (the first is `Vol. I`) holds chapters. A
**chapter** is one reading session, reached at its own address. A **board** is a contiguous strip
inside a chapter. A **panel** is one camera stop and holds between one and several separately drawn
**layers** stacked at different depths, so the near layers slide faster than the far ones as the
view moves and a flat drawing behaves like a shallow stage set. Every layer has an identifier built
from its chapter, board and panel numbers and a role name, for example `c1b1p1-back`.

At launch the first volume holds six chapters: three published and readable, two scheduled and
locked with their release moments shown, and one draft still being drawn. A reader who tips at or
above the early-access threshold reads a scheduled chapter up to a week before everyone else.

The genuinely hard part is the lock: whether a chapter is readable is decided by the server on every
request, from the chapter's state, its release moment, its early-access window and the caller's
current entitlements, and a tip only counts once its signed notification has been verified,
deduplicated and not refunded.

Its non-goals are deliberate. There are no comments, no social graph, no user-generated
content, no store or checkout inside the product, no native app, no animation authoring tool, no
advertising and no audio. The product sends no mail of any kind. There is no second factor, no
studio invitation flow and no team management. Nothing is measured about a visitor until they
accept measurement, and no measurement ever leaves the app's own origin.

## User roles

The permission matrix, by role:

| Role | Can do |
|---|---|
| Visitor (signed out) | Read every published chapter, see the rack with its locked sleeves and their release moments, read the about and legal pages, switch language, accept or decline measurement, keep reading progress in their own browser, open the Tipbox page from `support us`, create a reader account. **Cannot** read a scheduled or draft chapter, sync progress, hold an entitlement, or reach any `/api/me` or `/api/studio` endpoint. |
| Reader (signed in) | Everything a visitor can do, plus sync reading progress between devices, hold early-access and credits entitlements granted by tips, read a scheduled chapter inside its early-access window while holding an active early access, set a notification preference, export their data and delete their account. **Cannot** read a draft chapter, read a scheduled chapter outside its window or without an active early access, read another reader's progress or data, or reach any studio endpoint. |
| Author (studio member) | Everything in the studio console: create volumes and chapters, import and replace layers, edit panels and layers, store covers, edit translations for any locale, run preflight, mark ready, schedule, cancel, publish immediately, unpublish, read supporter records including a supporter's address, record a manual tip, confirm an address match, read insights, change studio settings, rotate the Tipbox signing secret, raise the asset version, preview any chapter including drafts. **Cannot** sign in on the reader surface with a studio account, read an individual reader's progress, sessions or account, or use a reader token on the studio surface. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a reader session to any author-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

Isolation holds on two axes: studio content belongs to the studio and is changed only by authors, and a reader's progress, entitlements and account belong to that reader alone. This is enforcement by the server, not a convention of the interface. Readers and authors are two separate identity systems. A reader signs in at `POST /api/auth/login`
and an author at `POST /api/studio/auth/login`; a reader token grants nothing on `/api/studio/*` and
an author token grants nothing on `/api/me*`. Reader signup is **open** to anyone at
`POST /api/auth/register`. Author accounts exist only as seeded; there is no author signup.

Seeded accounts, every one using the password `deku-demo-pw-2026`:

- `author@example.com`, author, Camille Rouyer
- `author2@example.com`, author, Damien Lorca
- `reader@example.com`, reader, holding an active early access granted by the seeded tip `tbx_seed_001`
- `reader2@example.com`, reader, holding no entitlement, with progress on chapter 1 of `Vol. I`

## Core features

### Authentication and account lifecycle

1. `POST /api/auth/register` with `email`, `password`, optional `locale` (`en` or `fr`) and
   `website` creates a reader and returns an `access_token`. A new reader's `notifications` starts
   at `drops`.
2. The reader signup form carries a decoy field named `website` that a person never sees or fills.
   A registration whose `website` is not empty is refused as a bot and creates no account.
3. A password shorter than 12 characters is rejected as invalid naming the `password` field, and a
   malformed address is rejected naming the `email` field; nothing is created.
4. Registering, or changing a reader's address to, an address already in use is rejected with the
   message `That address cannot be used.` and never says the other account exists. Addresses compare
   case-insensitively.
5. `POST /api/auth/login` returns an `access_token` for the right password. A wrong password and an
   unknown address get the same status, the same error `code` and the same `message`.
6. Authentication back-off: after 10 consecutive failed sign-ins for one address within an hour, sign-in for that address
   keeps failing for 15 minutes even with the right password, with the same response as a wrong
   password. An address that repeatedly fails sign-in is held back this way, and the same rule applies to author
   sign-in.
7. `POST /api/auth/logout` ends that session: the token no longer works on any endpoint. A reader session
   ends 90 days after its most recent authenticated request. An author session ends 2 hours after its most
   recent authenticated request and never later than 12 hours after sign-in. While a session is live, the
   session row's `expires_at` holds the moment the session ends. After that moment an endpoint that needs
   a session denies the token, and an endpoint open to visitors answers the request as a visitor's.
8. Passwords are stored hashed, never as the typed text, and a session token is never stored as
   issued.
9. An author signs in at `POST /api/studio/auth/login`; reader and author tokens are refused on each
   other's surface, and an anonymous call to any `/api/me` or `/api/studio` endpoint is denied.
10. There is no password reset, no passwordless link and no second factor.
11. The reader sign-in dialog is named `sign in`. It has an `email` field, a `password` field, a `sign in`
    button, and a `create an account` control that turns the dialog into the signup form with the same two
    fields and a `create account` button. The studio sign-in page at `/studio/sign-in` has the same two fields and a `sign in` button.

### The reading surface

1. The public routes are `/`, `/chapters`, `/chapter/:id`, `/about`, `/legal`, `/support/return` and
   `/account`, repeated for French under `/fr` with the same untranslated path segments
   (`/fr/chapters`, never a translated segment). Chapters of the first volume are addressed
   `/chapter/:id`; chapters of a later volume are addressed `/volumes/:volume/chapter/:id`, where
   `:volume` is the volume's order.
2. Every route renders inside one persistent shell: the header, the footer link, the language
   selector, the fullscreen control, the consent strip and one `canvas` that fills the window. The
   canvas is created once for the life of the page and survives every in-app navigation; moving
   between routes never reloads the document.
3. The first HTML response of every public route already carries that route's own `<title>`, its own
   `<meta name="description">` and an `<html lang>` naming its locale (`en` or `fr`). No two routes
   in one locale share a title or a description. The English titles and descriptions are:

   - `/` has the title `Doudou Fever - Interactive Comic` and the description `Doudou Fever is an interactive comic. Follow the adventure of a megalomaniac sheep who wants to make the world dance. Created by Camille Rouyer & Damien Lorca.`
   - `/chapters` has the title `Chapters | Doudou Fever - Interactive Comic` and the description
     `Pick a track from the Doudou Fever record rack and start reading.`
   - `/chapter/1` has the title `Chapter #1: Welcome To Varny - Doudou Fever - Interactive Comic` and
     the description `Read chapter 1, welcome to Varny, of the Doudou Fever interactive comic.`
   - `/about` has the title `About | Doudou Fever - Interactive Comic` and the description `Meet Doudou, the sheep who wants to make the world dance, and the two people who draw and animate him.`
   - `/legal` has the title `Legal Notice and Terms of Use | Doudou Fever - Interactive Comic` and the
     description `Publisher, hosting, rights, terms, personal data and cookies for the Doudou Fever website.`
   - `/support/return` has the title `Thank You | Doudou Fever - Interactive Comic` and the description
     `Thanks for tipping Doudou Fever.`
   - `/account` has the title `Your Account | Doudou Fever - Interactive Comic` and the description
     `Your Doudou Fever reading account.`
   - The not-found page has the title `Page Not Found | Doudou Fever - Interactive Comic` and the
     description `This page of Doudou Fever does not exist.`

   Every chapter page follows the chapter pattern: `Chapter #<n>: <Title With Each Word Capitalised> - Doudou Fever - Interactive Comic` and `Read chapter <n>, <title>, of the Doudou Fever interactive comic.` The French titles and descriptions are:

   - `/fr` has the title `Doudou Fever - BD interactive` and the description `Doudou Fever est une BD interactive. Suis l'aventure d'un mouton megalomane qui veut faire danser le monde. Creee par Camille Rouyer & Damien Lorca.`
   - `/fr/chapters` has the title `Chapitres | Doudou Fever - BD interactive` and the description `Choisis une piste dans le bac a disques de Doudou Fever et commence a lire.`
   - `/fr/chapter/1` has the title `Chapitre #1 : Bonjour Varny - Doudou Fever - BD interactive` and the description `Lis le chapitre 1, bonjour Varny, de la BD interactive Doudou Fever.`
   - `/fr/about` has the title `A propos | Doudou Fever - BD interactive` and the description `Rencontre Doudou, le mouton qui veut faire danser le monde, et les deux personnes qui le dessinent et l'animent.`
   - `/fr/legal` has the title `Mentions legales et conditions d'utilisation | Doudou Fever - BD interactive` and the description `Editeur, hebergement, droits, conditions, donnees personnelles et cookies du site Doudou Fever.`
   - `/fr/support/return` has the title `Merci | Doudou Fever - BD interactive` and the description `Merci d'avoir soutenu Doudou Fever.`
   - `/fr/account` has the title `Ton compte | Doudou Fever - BD interactive` and the description `Ton compte de lecture Doudou Fever.`
   - The French not-found page has the title `Page introuvable | Doudou Fever - BD interactive` and the description `Cette page de Doudou Fever n'existe pas.`

   Every French chapter page follows `Chapitre #<n> : <Titre Avec Chaque Mot En Capitale> - Doudou Fever - BD interactive` and `Lis le chapitre <n>, <titre>, de la BD interactive Doudou Fever.`
4. The title screen at `/` shows one entry button, `read now`, which opens `/chapters`. Its heading
   `Doudou Fever` and its credit line `By Damien Lorca & Camille Rouyer` are present for assistive
   technology and search engines while the visible title is drawn in the scene. A slowly spinning
   record sits above the centre of the screen; clicking it starts the surprise.
5. The chapter rack at `/chapters` carries the heading `select a chapter` and one sleeve per chapter
   of every volume that is published, scheduled or unpublished. A draft chapter has no sleeve. Each
   open sleeve shows its title as the two-digit number, a full stop and the title with no space
   (`01.welcome to Varny`), a subtitle joining the brand and the volume label with no space
   (`Doudou FeverVol. I`), and a timecode of the two-digit chapter number and the two-digit count of
   chapters in its volume (`01:06`). The count includes every chapter that exists, drafts included.
6. A sleeve that is not readable by the caller is a locked sleeve: a padlock replaces the play symbol,
   neither the icon nor the text is a link, and its accessible name states its title, that it is
   locked and, when it has a release moment, when it opens, for example
   `scratch that !, locked, opens 19 September 2026`; an unpublished chapter's sleeve is named
   `<title>, locked`. An open
   sleeve's timecode is announced as `chapter 1 of 6`.
7. The rack is a keyboard listbox: arrow keys move the selection, Enter opens the selected chapter,
   Home and End jump to the ends. Wheel, drag and the two small arrows on a sleeve move it too, and it
   settles on the nearest sleeve. The chapter last opened is remembered in local storage and the rack
   opens with that sleeve selected.
8. A chapter the caller may read opens the reader. While it loads, a caption `Next track is loading...` sits over a slow charcoal gradient with the name line `01. welcome to Varny` (two-digit
   number, full stop, space, title).
9. The reader draws the chapter's panels in the canvas, each from its layers at their depths. The
   canvas carries `role="img"` and an accessible name naming the chapter. A layer's base opacity is part of its properties. The view moves forward one
   panel on the right or up arrow key, back one panel on the left or down arrow key, and moves along
   the chapter with the wheel, where scrolling the wheel down means forward, or by dragging.
10. A timeline capsule at the bottom shows the chapter's cover, its title, the subtitle
    `Doudou FeverVol. I`, a progress track and a timecode of the two-digit chapter number and the
    two-digit number of the current panel counted across the whole chapter (`01:01`, announced as
    `panel 1`). The progress track is a slider named `chapter progress` whose value runs from 0 to
    100; pressing a point on it or using its arrow and page keys moves the view there.
11. Two controls named `previous panel` and `next panel` step the view. On the first panel `previous panel` is disabled.
12. Reaching the last panel slides a second face across the capsule: the label `next track` and the
    next chapter's title repeated four times, each copy followed by ` _ `, as a scrolling marquee.
    The face is a link to the next chapter, and following it changes chapter without reloading the
    document. On the last chapter of a volume there is no next-track face; one line, `last track of the volume, back to chapters`, links to the rack.
13. A control `read as text` switches the reader to text mode: the chapter as an ordered list of its
    panels' descriptions in reading order, in the current language. Text mode is the complete
    accessible equivalent of the drawn chapter.
14. Reading progress is kept in local storage under `dd-last-chapter` (the volume order and chapter
    number, for example `1/2`) and `dd-progress-<volume>-<chapter>` (a fraction from `0` to `1` with at
    most three decimals, for example `dd-progress-1-1` holding `0.400`), written at most once per
    second while reading.
15. A chapter that exists but the caller may not read renders the locked state at a normal `200`
    status: the name line (`04. scratch that !`), one line `This chapter opens <date>.` with the
    release moment as day, month name and year in the page's language and the reader's time zone
    (`This chapter opens 19 September 2026.`), a `notify me` control, a `support us` control with the
    line `Supporters read it as soon as it is finished.`, and the previous chapter's sleeve as a way
    back. A draft chapter shows `This chapter is still being drawn.` in place of the opening line.
16. `notify me` opens the reader sign-in dialog (with a way to create an account) and, once signed in,
    records the reader's wish to hear of drops through `POST /api/me/notify`, leaving `notifications`
    at `drops` or `all`. If the signed-in reader may now read the chapter, the reader opens in place.
17. The route parameter ladder for chapter pages: a value that is not a positive integer, or an
    integer above the number of chapters in that volume, or a volume order that does not exist,
    renders the not-found page with a `404` status; otherwise an unpublished chapter's page answers a
    temporary redirect to `/chapters` (`/fr/chapters` in French); otherwise a chapter that exists but is
    not readable renders the locked state with `200`; otherwise the reader renders with `200`.
18. Any other path renders the not-found page with a `404` status: the line `Oopsy, page not found`
    and a control `Go back to home` leading to `/`. The not-found page requests no chapter manifest
    and no panel image and draws no scene.
19. If one layer image of a panel fails to load, the panel renders without that layer and reading
    continues. If a whole chapter fails to load, the page shows `Something went missing. Try again?`
    with `try again`, which retries without reloading the document, and `back to chapters`.
20. If the browser cannot give the app a drawing context for the canvas, every route still works as a
    plain readable site: the title screen shows its heading and credit line, the rack lists every
    readable chapter as an ordinary link and every locked chapter as plain text, a chapter opens in text
    mode, and the about and legal pages show
    their text.
21. The persistent tip control `support us` sits on the rack and in the reader. It is a link to the
    Tipbox page `https://tipbox.example/doudou-fever` carrying a `return_token` query parameter
    issued for this visit, and it opens in a new tab with `target="_blank"` and a `rel` holding both
    `noopener` and `noreferrer`.
22. An `/account` page lets a signed-in reader see their address, language and notification
    preference, change them, download their data and delete their account. A signed-out visitor who
    opens `/account` gets the reader sign-in dialog over the rack.

### Who may read a chapter

1. A chapter is readable by a caller when it is `published`; or when it is `scheduled`, the current
   moment is at or after its release moment minus its `early_access_days`, and the caller is a
   signed-in reader holding an early access that is active (granted, not expired, not revoked). No
   other state or caller makes it readable on the public surface.
2. This is evaluated on the server on every request that could reveal a chapter, from the current
   state of the chapter and the caller's entitlements. A revoked or expired early access takes effect
   on the reader's very next request.
3. `GET /api/volumes/{order}/chapters/{number}` returns the manifest of a readable chapter. For a
   chapter the caller may not read, and for one that does not exist, it answers `404`, never `403`:
   the manifest endpoint confirms nothing about an unreleased chapter beyond what its sleeve shows.
4. In a manifest, `total` is the number of chapters in the volume and each panel's `index` is its
   1-based position across the whole chapter, the right-hand number of the reader timecode. A `sprite`
   layer also carries `frame_table_url`, the address of its frame table,
   `/api/textures/v<asset_version>/<volume order>/<chapter number>/<file identifier>.json?tag=<content tag>`,
   under the same rules as its image; every other layer carries `frame_table_url` as null. The manifest of a published chapter points at each layer image with
   `/api/textures/v<asset_version>/<volume order>/<chapter number>/<file identifier>.png?tag=<content tag>`. For a readable chapter that is not published, each address also carries `expires` and
   `sig` query parameters: a signature over that address, valid for 15 minutes.
5. An image of a chapter that is not published answers `404` when requested without its `sig`, with a
   `sig` that does not match, or after `expires`. An image of a published chapter needs no signature.
6. `GET /api/volumes` lists every volume with its chapters for the caller, marking each `locked` or
   open from the same evaluation; a draft chapter is never listed. A chapter's title in the list and
   its release moment are public.
7. Covers at `/api/covers/<volume order>/<chapter number>.png` are public for published and scheduled
   chapters and answer `404` for a draft.
8. The sitemaps `/sitemap.xml` (English addresses) and `/fr/sitemap.xml` (French addresses) list the
   static public routes and every published chapter's address, and never a scheduled, draft or
   unpublished chapter.
9. Every image object in the bucket is private: a request to the object store for any key without
   credentials is refused. Readers only ever receive images through the app.

### Tips and early access

1. `POST /api/tips/return-tokens` issues a return token, valid for 24 hours, that the tip control puts
   on its Tipbox link as `return_token`. Tipbox passes the token back in its notification and sends
   the tipper back to `/support/return?token=<token>`.
2. The return page calls `POST /api/tips/return` with the token. Without a reader session the answer
   is `{"status": "sign_in_required"}` and the page shows `Thank you. Sign in and we will attach it to your account.` with the sign-in dialog. With a reader session the token is claimed by that reader
   (a token is claimed by one reader only; another reader's claim is rejected) and the status is
   `granted` if a tip carrying the token has arrived and granted early access (`Thank you. Your early access is active.`), `below_threshold` if one has arrived below the threshold (`Thank you. Every tip helps, and this one goes straight into the next chapter.`), or `pending` if none has arrived
   yet (`Thank you. Your tip is on its way to us.`). An unknown or expired token is rejected and the
   page shows `This thank-you link has expired.` The return token never grants anything by itself.
3. Tipbox delivers inbound notifications to `POST /api/webhooks/tipbox`. The studio's Tipbox signing secret
   is `tbx_whsec_5f3a9c2e81d7`. Each request carries the header `Tipbox-Signature: t=<unix seconds>,v1=<signature>`, where the signature is the lowercase hexadecimal HMAC-SHA256,
   keyed with the signing secret, of the timestamp, a full stop, and the raw request body bytes
   exactly as received.
4. A notification whose signature does not match those exact bytes, or whose timestamp is more than
   300 seconds away from the server's clock in either direction, is answered `401`, is recorded with
   `signature_verified` false, and changes nothing else. A body that changed by a single space after
   signing does not verify.
5. A verified notification is recorded and answered `200`. A notification whose event `id` was
   already verified is answered `200` and does nothing a second time. Its effects appear within 30
   seconds of the `200`.
6. The notification body is `{"id": "evt_...", "type": "tip.received" | "tip.refunded" | "tip.disputed", "created": <unix seconds>, "data": {...}}`. For `tip.received`, `data` carries
   `tip_id`, `amount` (original minor units), `currency` (lowercase, for example `eur`),
   `settled_amount` (minor units in the studio currency `usd`, already converted by Tipbox), `rate`
   (the conversion rate as decimal text, for example `1.087500`), `supporter_email`, `message` and
   `return_token`. For `tip.refunded` and `tip.disputed`, `data` carries `tip_id`. A verified notification of any other
   `type` is answered `200` and changes nothing.
7. Each tip is stored once per Tipbox `tip_id`, however many times or however concurrently it
   arrives, with its original amount and currency, its settled amount and its rate exactly as
   received. The settled amount is never recomputed.
8. A tip is matched to a reader in this order: to the reader who claimed its `return_token` (method
   `token`, exact, whether the claim came before or after the tip); otherwise to a reader whose
   address equals `supporter_email` ignoring case (method `address`, probable, which grants nothing
   until an author confirms it); otherwise to nobody (method `none`).
9. A tip matched by token, or matched by address and confirmed by an author, whose settled amount is
   at or above the early-access threshold (`500`, that is `$5.00`) grants an `early_access`
   entitlement that expires 12 calendar months after the grant (granted on 16 September 2026, it
   expires on 16 September 2027). At or above the credit threshold (`2000`, that is `$20.00`) it
   also grants a `credits` entitlement with no expiry. Below `500` it grants nothing.
10. `tip.refunded` sets the tip's state to `refunded` and `tip.disputed` sets it to `disputed`. Either
    revokes the entitlements that tip granted, unless the same reader holds another tip still
    `received` whose settled amount is at or above the early-access threshold, in which case the early
    access stands. Revocation never removes what was
    already read; it only closes early access from the next request on. Each revocation appears on
    the studio overview.
11. Ordering is never assumed: notifications may arrive out of order. A refund or dispute for a `tip_id` that has not arrived yet
    creates that tip in its refunded or disputed state; when the tip itself arrives it fills in the
    amounts and grants nothing.
12. Every seeded and received tip appears in the studio supporter list, and `reader@example.com`'s
    seeded tip `tbx_seed_001` (settled `800`) is the one granting their early access.

### Reading progress synchronisation across devices

1. A signed-in reader's progress is `GET /api/me/progress` and `PUT /api/me/progress`, one whole
   document: `last_chapter` (`{"volume", "chapter"}` or null), `last_chapter_at`, and `chapters`, a
   list of `{"volume", "chapter", "fraction", "last_panel"}`.
2. A `PUT` merges with what is stored and returns the merged document: for each chapter the greater
   `fraction` wins; where fractions are equal the greater `last_panel` wins; `last_chapter` is taken
   from whichever document has the later `last_chapter_at`; a chapter that does not exist is dropped.
3. The merge is commutative and idempotent: two devices syncing in either order end with the same
   document, and sending the same document twice changes nothing. A reader never loses a position by
   syncing.
4. A `fraction` outside `0` to `1`, or with more than three decimals, rejects the whole request as
   invalid and writes nothing.
5. When a signed-out visitor signs in, the progress in their browser is uploaded and merged, never
   discarded. Signing out keeps the browser's progress.
6. No studio endpoint returns an individual reader's progress or sessions, and a reader's address reaches
   the studio only on a tip that reader is matched to, as that tip row's `matched_reader_email`; the studio
   sees reading progress as counts only.

### Reader data rights

1. `GET /api/me/export` returns the reader's own data as a JSON attachment: `reader`, `progress`,
   `entitlements` and `tips` matched to them.
2. `DELETE /api/me` with the reader's `password` deletes the reader, their sessions, their progress
   and their entitlements. Tips they sent are kept for the studio's records with the matched reader
   and the `supporter_email` cleared. A wrong password deletes nothing.
3. `PATCH /api/me` changes `locale` (`en` or `fr`), `notifications` (`all`, `drops` or `none`) and
   `email`, validated as at signup.

### Languages and localisation

1. Two locales exist: `en` (English, the default, served without a prefix) and `fr` (French, under
   `/fr`). Path segments are never translated; a translated segment such as `/fr/chapitres` is a
   `404` not-found page.
2. The language selector shows `EN` and `FR` with a `|` between them. Pressing the inactive language
   switches without reloading the document: a coloured curtain sweeps over the window, the address
   gains or loses `/fr` on the same path, every string and every lettered layer image changes to the
   new language, `<html lang>` changes, and the curtain lifts. The choice is remembered in local
   storage under `dd-language` as `en` or `fr`.
3. The locales table drives the route table, the language selector and the sitemaps, so adding a third
   locale is data plus translations, not a code change.
4. `GET /api/catalogue/<locale>` returns every interface string for a locale as a flat object of
   dotted keys. A key whose translation is `untranslated` in that locale serves the default-locale
   value instead. A reader never sees a key path.
5. The catalogue holds at least these keys, each in both languages. Every other interface string this
   brief shows or announces is also a catalogue key in both languages, in its page's namespace, with its
   English text as stated in this brief: the about page's long paragraphs, the team card bodies, the
   legal bodies, the sleeve and timecode announcements, the dialog names, and each page's title and
   description, held as `index.meta_title`, `chapters.meta_title`, `reader.meta_title` (chapter pages, with the
   placeholders `{number}` and `{title}`), `about.meta_title`, `legal.meta_title`, `support.meta_title`,
   `account.meta_title` and `not-found.meta_title`, each with a matching `meta_description` key, holding the
   values in The reading surface rule 3.

   | Key | `en` | `fr` |
   |---|---|---|
   | `chrome.chapters` | `chapters` | `chapitres` |
   | `chrome.about` | `about` | `a propos` |
   | `chrome.legal` | `legal notice & terms of use` | `mentions legales & conditions d'utilisation` |
   | `chrome.byline` | `by Camille Rouyer and Damien Lorca` | `par Camille Rouyer et Damien Lorca` |
   | `chrome.fullscreen_enter` | `enter fullscreen` | `plein ecran` |
   | `chrome.fullscreen_exit` | `exit fullscreen` | `quitter le plein ecran` |
   | `index.button` | `read now` | `lire maintenant` |
   | `index.credit` | `By Damien Lorca & Camille Rouyer` | `Par Damien Lorca & Camille Rouyer` |
   | `chapters.heading` | `select a chapter` | `choisis un chapitre` |
   | `chapters.tip` | `support us` | `soutiens-nous` |
   | `chapters.next_track` | `next track` | `piste suivante` |
   | `reader.loading` | `Next track is loading...` | `La piste suivante arrive...` |
   | `reader.text_mode` | `read as text` | `lire en texte` |
   | `reader.previous_panel` | `previous panel` | `case precedente` |
   | `reader.next_panel` | `next panel` | `case suivante` |
   | `reader.progress` | `chapter progress` | `progression du chapitre` |
   | `reader.load_failed` | `Something went missing. Try again?` | `Il manque quelque chose. On reessaie ?` |
   | `reader.retry` | `try again` | `reessayer` |
   | `reader.back` | `back to chapters` | `retour aux chapitres` |
   | `locked.timing` | `This chapter opens {date}.` | `Ce chapitre sort le {date}.` |
   | `locked.drawing` | `This chapter is still being drawn.` | `Ce chapitre est encore en dessin.` |
   | `locked.notify` | `notify me` | `previens-moi` |
   | `locked.support` | `Supporters read it as soon as it is finished.` | `Les soutiens le lisent des qu'il est fini.` |
   | `consent.message` | `Hey you ✨ This site uses cookies to measure the traffic.` | `Coucou ✨ Ce site utilise des cookies pour mesurer la frequentation.` |
   | `consent.accept` | `Accept` | `Accepter` |
   | `consent.decline` | `Decline` | `Refuser` |
   | `support.granted` | `Thank you. Your early access is active.` | `Merci. Ton acces anticipe est actif.` |
   | `support.sign_in` | `Thank you. Sign in and we will attach it to your account.` | `Merci. Connecte-toi et nous l'ajouterons a ton compte.` |
   | `support.below_threshold` | `Thank you. Every tip helps, and this one goes straight into the next chapter.` | `Merci. Chaque pourboire aide, et celui-ci part droit dans le prochain chapitre.` |
   | `support.pending` | `Thank you. Your tip is on its way to us.` | `Merci. Ton pourboire est en route.` |
   | `support.expired` | `This thank-you link has expired.` | `Ce lien de remerciement a expire.` |
   | `support.chip_tip` | `♥ give a tip ♥` | `♥ laisse un pourboire ♥` |
   | `support.entitlement` | `Tips of {amount} or more read new chapters up to {days} days early.` | `Les pourboires de {amount} ou plus lisent les nouveaux chapitres jusqu'a {days} jours plus tot.` |
   | `about.nav_intro` | `intro` | `intro` |
   | `about.nav_legend` | `the legend` | `la legende` |
   | `about.nav_team` | `the team` | `l'equipe` |
   | `about.nav_support` | `support us` | `soutiens-nous` |
   | `about.scroll` | `Scroll down` | `Descends` |
   | `about.intro_title` | `the interactive adventure of a megalomaniac sheep who wants to make the world dance.` | `l'aventure interactive d'un mouton megalomane qui veut faire danser le monde.` |
   | `about.legend_title_1` | `yes the legend,` | `oui la legende,` |
   | `about.legend_title_2` | `is {hero}!` | `c'est {hero} !` |
   | `about.team_title_1` | `behind` | `derriere` |
   | `about.team_title_2` | `the legend` | `la legende` |
   | `about.support_title_1` | `i love you too` | `moi aussi je t'aime` |
   | `about.support_title_2` | `my friend!` | `mon ami !` |
   | `about.chip_contact` | `email us` | `ecris-nous` |
   | `legal.title` | `Legal Notice & Terms of Use` | `Mentions legales & conditions d'utilisation` |
   | `legal.publisher` | `Website Publisher` | `Editeur du site` |
   | `legal.hosting` | `Hosting` | `Hebergement` |
   | `legal.domains` | `Domains` | `Domaines` |
   | `legal.property` | `Intellectual Property` | `Propriete intellectuelle` |
   | `legal.terms` | `Terms of Use` | `Conditions d'utilisation` |
   | `legal.data` | `Personal Data & Privacy` | `Donnees personnelles & vie privee` |
   | `legal.cookies` | `Cookies & Trackers` | `Cookies & traceurs` |
   | `legal.law` | `Applicable Law & Jurisdiction` | `Droit applicable & juridiction` |
   | `not-found.text` | `Oopsy, page not found` | `Oups, page introuvable` |
   | `not-found.cta` | `Go back to home` | `Retour a l'accueil` |
   | `account.heading` | `Your account` | `Ton compte` |
   | `account.export` | `download my data` | `telecharger mes donnees` |
   | `account.delete` | `delete my account` | `supprimer mon compte` |
   | `account.sign_in` | `sign in` | `se connecter` |
   | `account.create` | `create an account` | `creer un compte` |
   | `account.email` | `email` | `e-mail` |
   | `account.password` | `password` | `mot de passe` |
   | `chrome.surprise` | `surprise` | `surprise` |
   | `chapters.locked_name` | `{title}, locked, opens {date}` | `{title}, verrouille, sort le {date}` |
   | `chapters.locked_plain` | `{title}, locked` | `{title}, verrouille` |
   | `chapters.timecode_label` | `chapter {number} of {count}` | `chapitre {number} sur {count}` |
   | `reader.timecode_label` | `panel {number}` | `case {number}` |
   | `reader.announce_loading` | `Chapter {number} is loading.` | `Le chapitre {number} arrive.` |
   | `reader.announce_ready` | `Chapter {number} is ready.` | `Le chapitre {number} est pret.` |
   | `reader.announce_failed` | `Chapter {number} could not be loaded.` | `Le chapitre {number} n'a pas pu etre charge.` |
   | `reader.end_of_volume` | `last track of the volume, back to chapters` | `derniere piste du volume, retour aux chapitres` |
   | `chrome.announce_locale` | `The page is now in English.` | `La page est maintenant en francais.` |
   | `about.legend_body` | `Doudou is a megalomaniac sheep, tender and dead set on becoming a DJ. With Jean-Loic, a wild barman, and Milan, a future cooking star on socials, he mixes chaos and big dreams in a flat full of laughs and late-night noise. It's cool, it's fun, it's Doudou Fever.` | `Doudou est un mouton megalomane, tendre et bien decide a devenir DJ. Avec Jean-Loic, un barman dechaine, et Milan, future star de la cuisine sur les reseaux, il melange chaos et grands reves dans un appart plein de rires et de bruit tard le soir. C'est cool, c'est drole, c'est Doudou Fever.` |
   | `about.team_dam_title` | `Dam` | `Dam` |
   | `about.team_dam_body` | `Creative developer and animator, half-coder half-wizard. He animates images, makes pixels move, and transforms lines of code into cool and magical experiences.` | `Developpeur creatif et animateur, moitie codeur moitie sorcier. Il anime les images, fait bouger les pixels et transforme des lignes de code en experiences cool et magiques.` |
   | `about.team_ca_title` | `Ca` | `Ca` |
   | `about.team_ca_body` | `Art director, illustrator and digital brush master. She draws faster than her shadow and gives life to each character with style, emotion...` | `Directrice artistique, illustratrice et maitresse du pinceau numerique. Elle dessine plus vite que son ombre et donne vie a chaque personnage avec style, emotion...` |
   | `about.support_body` | `Support Doudou on his way to glory and help him become a legend. One day, maybe : a printed edition, sweet merch, and Doudou stealing the spotlight!` | `Soutiens Doudou sur le chemin de la gloire et aide-le a devenir une legende. Un jour, peut-etre : une edition imprimee, du merch trop mignon, et Doudou sous les projecteurs !` |
   | `about.support_hidden` | `Be part of the adventure, or live with this question forever "What if I had helped Doudou become a legend?"` | `Fais partie de l'aventure, ou vis pour toujours avec cette question "Et si j'avais aide Doudou a devenir une legende ?"` |
   | `about.chip_photogram` | `photogram` | `photogram` |
   | `about.chip_clipclop` | `clipclop` | `clipclop` |
   | `legal.publisher_body` | `The Doudou Fever website is created and published by Damien Lorca and Camille Rouyer.` | `Le site Doudou Fever est cree et publie par Damien Lorca et Camille Rouyer.` |
   | `legal.contact_label` | `Contact email` | `E-mail de contact` |
   | `legal.hosting_body` | `Hosted by Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.` | `Heberge par Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.` |
   | `legal.domains_body` | `The domains doudoufever.example, www.doudoufever.example, doudou-fever.example and doudoufever-comic.example are registered with Registre Clair SARL, 4 quai du Port, 13002 Marseille, France.` | `Les domaines doudoufever.example, www.doudoufever.example, doudou-fever.example et doudoufever-comic.example sont enregistres aupres de Registre Clair SARL, 4 quai du Port, 13002 Marseille, France.` |
   | `legal.property_body` | `All content of this website is protected. No licence is granted, and any reproduction, distribution, modification or exploitation without prior authorisation is prohibited.` | `Tout le contenu de ce site est protege. Aucune licence n'est accordee, et toute reproduction, diffusion, modification ou exploitation sans autorisation prealable est interdite.` |
   | `legal.terms_body` | `Use of this website is personal. Users agree not to disrupt the site. External links such as Tipbox are outside the publisher's responsibility, including for payment incidents. The site may be modified or suspended without notice.` | `L'utilisation de ce site est personnelle. Les utilisateurs s'engagent a ne pas perturber le site. Les liens externes comme Tipbox ne relevent pas de la responsabilite de l'editeur, y compris pour les incidents de paiement. Le site peut etre modifie ou suspendu sans preavis.` |
   | `legal.data_body` | `A reader's address, progress and matched tips are collected only to run the reader account. They are never resold, and can be exported, corrected or deleted from the account page.` | `L'adresse, la progression et les pourboires rattaches d'un lecteur sont collectes uniquement pour faire fonctionner le compte lecteur. Ils ne sont jamais revendus et peuvent etre exportes, corriges ou supprimes depuis la page du compte.` |
   | `legal.cookies_body` | `The functional keys dd-consent, dd-language, dd-last-chapter, the dd-progress- keys, dd-session and dd-studio-session are set whatever the consent decision because they only remember the reader's place, language and session. Measurement runs only after Accept.` | `Les cles fonctionnelles dd-consent, dd-language, dd-last-chapter, les cles dd-progress-, dd-session et dd-studio-session sont posees quel que soit le choix de consentement car elles retiennent seulement la place, la langue et la session du lecteur. La mesure ne demarre qu'apres Accepter.` |
   | `legal.law_body` | `These terms are governed by French law. Any dispute falls under the courts of Paris.` | `Ces conditions sont regies par le droit francais. Tout litige releve des tribunaux de Paris.` |

6. Chapter titles are transcreated per locale, not translated: `welcome to Varny` is `bonjour Varny`,
   `under pressure` is `sous pression`, `sheep don't sleep` is `moutons insomniaques`, `scratch that !`
   is `on efface tout !`, `wow ...` is `ouf ...`, and `the big mix` is `le grand mix`.
7. Every date and number shown is formatted for the page's language rather than built from fragments;
   money follows the two written forms pinned in About and legal rule 5.

### Consent, measurement and page views

1. On a first visit a consent strip slides up along the bottom with `Hey you ✨ This site uses cookies to measure the traffic.`, `Accept` and `Decline`. When it appears it takes keyboard focus and keeps
   focus inside it until answered.
2. Pressing either button writes `dd-consent` in local storage as `accepted` or `declined`, slides the
   strip away, and releases the four corner controls (footer, language selector, fullscreen control,
   tip control) into place. A reload with an answer stored shows no strip.
3. The legal page's cookies section names the functional keys `dd-consent`, `dd-language`,
   `dd-last-chapter`, the `dd-progress-` keys, `dd-session` and `dd-studio-session`, and states that they are set
   whatever the
   consent decision because they only remember the reader's place, language and session.
4. After a visitor declines, their cookies, local storage and session storage hold no key other than
   `dd-consent`, `dd-language`, `dd-last-chapter` and keys beginning `dd-progress-`, however much they
   read, and the app sends no request to `/api/events`. The session keys are the only further keys: `dd-session` while a reader is signed in and
   `dd-studio-session` while an author is signed in to the studio.
5. After a visitor accepts, the app records reading events through `POST /api/events` with a `name`
   and `params` from this closed set, and nothing else: `chapter_opened` (`volume`, `chapter`,
   `locale`), `panel_reached` (`volume`, `chapter`, `panel`, `elapsed_seconds`), `chapter_completed`
   (`volume`, `chapter`, `elapsed_seconds`), `chapter_abandoned` (`volume`, `chapter`, `last_panel`,
   `elapsed_seconds`), `tip_control_pressed` (`route`), `chapter_load_failed` (`volume`, `chapter`,
   `failure`), `language_switched` (`locale`) and `fullscreen_toggled` (`state`). An event with any
   other name or any other parameter key, such as an address or a free-text field, is rejected as
   invalid and stored nowhere. `panel_reached` is sent at most once per panel per visit.
6. Every public page view, including a view reached by in-app navigation and whatever the consent
   decision, is recorded with its route name (`index`, `chapters`, `chapter-id` for both chapter address forms,
   `about`, `legal`, `support-return`, `account`, `not-found`) and the moment, through `POST /api/page-views` with `{"route": ...}`, and with no
   visitor, reader, address or query value. A route name outside that list is rejected.
7. Every manifest the service returns counts one chapter open for that chapter in that hour, again
   with no identifier.
8. Authors read page views newest first at `GET /api/studio/page-views` (optionally filtered by
   `route`) and read both sources at `GET /api/studio/insights`, which keeps the server counts
   (`page_views` and `chapter_opens` by hour) and the measured `events` (count by name) side by side
   and never adds one to the other.

### About and legal

1. `/about` is the only public page that scrolls, and it has four sections whose accessible names are
   `intro`, `the legend`, `the team` and `support us`, matching a small navigation rail of four dots
   on the right edge that names each section on hover and jumps to it. The rail disappears at the
   same width step where the language selector moves to the bottom left.
2. The intro section's heading reads `the interactive adventure of a megalomaniac sheep who wants to make the world dance.` above a prompt `Scroll down`. Behind it, characters fall into the frame
   under gravity, pile up along the bottom, and can be picked up and thrown with the pointer.
3. The legend section's heading reads `yes the legend,` and `is Doudou!`, and its body reads
   `Doudou is a megalomaniac sheep, tender and dead set on becoming a DJ. With Jean-Loic, a wild barman, and Milan, a future cooking star on socials, he mixes chaos and big dreams in a flat full of laughs and late-night noise. It's cool, it's fun, it's Doudou Fever.`, arriving word by word
   as the section scrolls into view.
4. The team section's heading reads `behind` and `the legend`, with two cards that begin tilted away
   and swing round to face the reader as the section scrolls: `Dam`, on a near-black card, reads
   `Creative developer and animator, half-coder half-wizard. He animates images, makes pixels move, and transforms lines of code into cool and magical experiences.`; `Ca`, on a cream card, reads
   `Art director, illustrator and digital brush master. She draws faster than her shadow and gives life to each character with style, emotion...`. Pressing a card flips it.
5. The support section's heading reads `i love you too` and `my friend!`, its body reads `Support Doudou on his way to glory and help him become a legend. One day, maybe : a printed edition, sweet merch, and Doudou stealing the spotlight!`, a second paragraph `Be part of the adventure, or live with this question forever "What if I had helped Doudou become a legend?"` is present but hidden,
   and four chips follow: `♥ give a tip ♥` (the Tipbox link), `photogram`, `clipclop` and `email us`.
   Under the chips one line states what a tip buys, with `{amount}` filled from the early-access threshold
   as money and `{days}` from the default `early_access_days`. Money is written with a leading `$` and a full
   stop before two decimals in English (`$5.00`), and with a comma before two decimals, one space and a
   trailing `$` in French (`5,00 $`); with the seeded
   settings the English line reads `Tips of $5.00 or more read new chapters up to 7 days early.` and the French
   line reads `Les pourboires de 5,00 $ ou plus lisent les nouveaux chapitres jusqu'a 7 jours plus tot.`
6. In either language, the fragment `#doudou` opens the about page at the legend section, `#team` or
   `#equipe` at the team section, and `#support` at the support section (`/about#team`,
   `/fr/about#equipe`); any other fragment opens at the intro.
7. `/legal` is plain prose the reader can select in one sweep, headed `Legal Notice & Terms of Use`,
   with eight sections headed `Website Publisher`, `Hosting`, `Domains`, `Intellectual Property`,
   `Terms of Use`, `Personal Data & Privacy`, `Cookies & Trackers` and `Applicable Law & Jurisdiction`.
8. Website Publisher reads `The Doudou Fever website is created and published by Damien Lorca and Camille Rouyer.` with `Contact email` `hello@example.com`. Hosting names `Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France`. Domains lists `doudoufever.example`,
   `www.doudoufever.example`, `doudou-fever.example` and `doudoufever-comic.example`, registered with
   `Registre Clair SARL, 4 quai du Port, 13002 Marseille, France`.
9. Intellectual Property states that all content is protected, no licence is granted, and reproduction,
   distribution, modification and exploitation without prior authorisation are prohibited. Terms of Use
   states that use is personal, that users agree not to disrupt the site, that external links such as
   Tipbox are outside the publisher's responsibility including for payment incidents, and that the
   site may be modified or suspended without notice. Personal Data & Privacy states that a reader's
   address, progress and matched tips are collected only to run the reader account, are never resold,
   and can be exported, corrected or deleted from the account page. Cookies & Trackers carries the
   functional-keys statement above and says measurement runs only after `Accept`. Applicable Law &
   Jurisdiction names French law and the courts of Paris.

### Delight surfaces: the surprise easter egg

1. Typing the key sequence up, up, down, down, left, right, left, right, `b`, `a` on any public page,
   or clicking the record on the title screen, opens the surprise: a dialog named `surprise` over a
   half-black overlay, fifty-five spinning copies of Doudou's head scattered across the window, and a
   wobbling centre frame playing a looping animation. A wrong key resets the sequence.
2. The surprise never plays sound. Escape or pressing the overlay closes it and returns focus to where
   it was; navigating away closes it. Focus stays inside it while open.
3. When the reader's system asks for reduced motion, neither the key sequence nor the record opens the
   surprise.

### Studio content: volumes, chapters, boards, panels and layers

1. Authors list volumes at `GET /api/studio/volumes` and create one with a `label` of 1 to 40
   characters at `POST /api/studio/volumes`; a new volume takes the next `order`. `Vol. I` is order `1`.
   A label outside that range is rejected naming the field and creates nothing.
2. `POST /api/studio/volumes/{id}/chapters` creates the next chapter number of that volume as a
   `draft`, with `titles` and `descriptions` per locale (title 1 to 60 characters, description up to
   200). Chapter numbers are contiguous from 1 within each volume. A title or description outside its
   range is rejected naming the field and creates nothing.
3. The chapter list (`GET /api/studio/volumes/{id}/chapters`) returns one row per chapter ordered by
   number, with `titles`, `state`, `release_at`, `published_at`, `boards_ready` over `boards_total`, and
   `image_bytes` (the stored bytes of all its images). A board is ready when it has at least one panel,
   every panel has at least one layer and a description in every active locale, and every layer image
   exists in the bucket.
4. `POST /api/studio/chapters/{id}/boards` adds the next board number. `PUT /api/studio/chapters/{id}/cover` stores the cover image.
5. Panel creation from an upload: `POST /api/studio/boards/{id}/imports` takes one multipart request of `files` and imports them as
   one transaction: either every file is imported or none is, and a rejection names the failing
   `file`. A rejected import leaves no new panel, no new layer and no new object in the bucket.
6. Each filename is parsed against the layer identifier grammar, a layer identifier plus an extension: `c<chapter>b<board>p<panel>-<role>` where
   the chapter number has 1 to 3 digits, the board number 1 to 3 digits, the panel number 1 to 2
   digits, none with a leading zero, and the role is one or more segments of 1 to 24 lowercase letters
   or digits joined by single hyphens, for example `c1b1p1-back.png`. The chapter and board numbers
   must be the importing board's own. Uppercase letters, spaces, underscores and every other character
   are rejected, and the rejection names the offending character; a name is never tidied.
7. A file naming a panel that does not exist creates that panel. A file naming a role that already
   exists in that panel replaces that layer's image and keeps its depth, offset, scale, opacity and
   draw order. Two files naming the same role in one import are rejected.
8. Trailing role segments with a meaning: `depth` or `map` (for example `c1b1p1-stage-depth.png`)
   adds a greyscale map layer, used as a distortion field that makes a surface ripple, attached as the displacement source of the layer it names, which must exist in the
   panel or in the same import; `sprite` must arrive with the matching `sprite-data` JSON frame table
   (`c1b1p2-crowd-sprite.png` with `c1b1p2-crowd-sprite-data.json`) and neither is accepted alone; a
   locale code (`en`, `fr`) marks a localised layer, and every active locale needs its own file for
   that role in the same import (`c1b1p1-sign-en.png` with `c1b1p1-sign-fr.png`).
9. A frame table carries `width`, `height`, `fps`, `frames` (each `x`, `y`, `w`, `h`, `pivot_x`,
   `pivot_y`, `duration_ms`) and `clips` (each `name`, `first`, `last`, `loop` of `once`, `loop` or
   `ping-pong`). A frame table missing any of these is rejected.
10. Image content is recognised from its bytes, never from the file name: PNG, WebP and JPEG are
    accepted, anything else is rejected even when named `.png`. At most 200 files and 40 megabytes per
    file are accepted per import.
11. Every accepted image is re-encoded as PNG with every metadata chunk removed before it is stored,
    and is stored in the bucket at `chapters/{volume_order}/{chapter_number}/{file_identifier}/{sha256_of_bytes}.png`,
    where the hash is the lowercase hexadecimal SHA-256 of the stored bytes and the file identifier keeps
    any locale segment, for example
    `chapters/1/1/c1b1p1-back/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae.png`. A
    frame table is stored at the same scheme ending `.json`, and a cover at
    `covers/{volume_order}/{chapter_number}/{sha256_of_bytes}.png`. Nothing is written to the app's own
    disk.
12. Adding or replacing any image of a chapter changes that chapter's `content_tag`; nothing else does.
13. `PATCH /api/studio/layers/{id}` edits a layer: `depth` from -10 to 10, `offset_x` and `offset_y`
    from -10 to 10, `scale` from 0.1 to 4, `opacity` from 0 to 1, `blend` of `normal` or `additive`,
    `draw_order` from 0 to 63 and unique within the panel, `displacement_source` naming a map layer in
    the same panel, `displacement_strength` from 0 to 1, `clip` naming a clip of its frame table,
    `loop_mode` of `once`, `loop` or `ping-pong`, and `retain`. A value outside its range is rejected
    naming the field and changes nothing.
14. `PATCH /api/studio/panels/{id}` edits a panel: `descriptions` per locale (1 to 300 characters),
    `selectable`, `hold`, `wide`, `entry_duration` from 0.1 to 3.0 seconds, `camera_x` and `camera_y`
    from -10 to 10. A value outside its range is rejected naming the field and changes nothing.
15. Editing in the console is optimistic: a change shows at once and is then saved. Every chapter, board, panel and layer carries a `version`. Every edit sends the `version` it last
    read. When a save is rejected as invalid, the console puts back the last saved value and states why
    beneath the field. On a `version_conflict` the console shows the author's value beside the `current`
    value and asks which to keep, so no work is silently lost. An edit carrying a stale version answers `409` with the error code `version_conflict` and the
    current row under `current`, and changes nothing. A successful edit returns the new version.
16. Any edit to a `ready` chapter's titles, descriptions, boards, panels or layers returns it to
    `draft`. An edit to a `scheduled` chapter's content is refused until its release is cancelled.
17. `GET /api/studio/search?q=` searches chapter titles, panel identifiers, layer identifiers and
    translation keys, in that priority, each result carrying a `type` of `chapter`, `panel`, `layer` or `translation`; a
    query that is a full layer identifier returns that layer's panel composer address first.
18. `GET /api/studio/chapters/{id}/manifest` previews any chapter, drafts included, with signed image
    addresses.

### Release scheduling

1. A chapter's `state` is one of `draft`, `ready`, `scheduled`, `published` and `unpublished`. The only
   transitions are: `draft` to `ready` (`POST .../ready`), `ready` back to `draft` (any content edit),
   `ready` to `scheduled` (`POST .../schedule`), `scheduled` to `ready` (`POST .../cancel`),
   `scheduled` to `published` (at the release moment), `scheduled` to `ready` (at the release moment
   when preflight fails), `ready` to `published` (`POST .../publish`), `published` to `unpublished`
   (`POST .../unpublish`) and `unpublished` to `ready` (`POST .../ready`). Any other request is rejected
   and leaves the state unchanged.
2. `POST /api/studio/chapters/{id}/preflight` runs ten rules and returns `{"passed": ..., "failures": [{"rule": <number>, "message": ...}]}` listing every failing rule:
   rule 1, the chapter has at least one board, every board at least one panel and every panel at
   least one layer; rule 2, every layer's image object exists in the bucket at its key; rule 3, every
   localised layer has an image for every active locale; rule 4, the chapter has a title in every
   active locale and every panel a description in every active locale, unless that locale has a live
   waiver; rule 5, the chapter's stored image bytes stay within its byte budget of `24000000`; rule 6, its first board's
   stored image bytes stay within `3000000`; rule 7, chapter numbers 1 up to this one all exist in
   its volume; rule 8, the chapter has a cover; rule 9, the previous chapter of the volume is published,
   or, for a chapter being scheduled or already scheduled, scheduled for an earlier release moment
   (chapter 1 has no previous chapter);
   rule 10, the first layer image of the first board can actually be read back from the bucket.
3. Marking `ready` requires rules 1, 2, 3, 4, 5, 6 and 8 to pass. Scheduling requires all ten, and a
   `release_at` in the future and at most 5 years ahead. Publishing immediately requires all ten, with
   the previous chapter published. A `release_at` without a UTC offset, in the past, or more than 5 years
   ahead is rejected naming the `release_at` field. A ready, schedule or publish request whose required
   rules fail is rejected with the error code `preflight_failed` and the failing rules under `failures`.
   Either rejection changes nothing.
4. `release_at` is accepted with any UTC offset, stored as an instant and returned in UTC with a `Z`.
   A chapter scheduled for `2027-03-28T20:00:00+02:00` reads back as `2027-03-28T18:00:00Z`. The
   studio sees moments in the studio time zone `Europe/Paris`; readers see them in their own.
5. A scheduled chapter becomes `published` no more than 60 seconds after its release moment, whether or
   not anyone asks for it. The app re-runs preflight at that moment; if it fails, the chapter returns
   to `ready` and the overview shows an alert of kind `preflight_failed_at_release`.
6. Publishing stamps `published_at` once. Publishing a chapter that is already published succeeds and
   changes nothing: the same `published_at` and no second audit record.
7. Unpublishing sets `unpublished`, removes the chapter from the sitemaps and from readers, and makes
   its page answer a temporary redirect to `/chapters`.
8. A chapter's `early_access_days` is set per chapter from 0 to 30 and defaults to `7`; a value outside
   that range is rejected naming the field and changes nothing.
9. A chapter's per-locale waiver is set through `waivers` with a required `reason` of 1 to 200
   characters, lasts 30 days, and lets rule 4 skip that locale. A waiver without a reason is rejected.
10. Every studio mutation writes one audit record carrying the author's address, the action, the
    subject and the `request_id` of that request. Publication writes the action `chapter.published`,
    scheduling `chapter.scheduled`, unpublishing `chapter.unpublished`, an import `layer.imported`.
    Audit records are only ever added, never changed or removed.
11. Scheduling, publishing, unpublishing and raising the asset version each end in the console on a
    full-page confirmation naming what changed.

### Translations

1. Every interface string exists per locale with a state of `untranslated`, `translated` or
   `reviewed`, in the namespaces `chrome`, `index`, `chapters`, `reader`, `locked`, `about`, `legal`,
   `consent`, `not-found`, `support` and `account`.
2. `GET /api/studio/translations/coverage` returns, per namespace and locale, `total`, `translated`,
   `reviewed` and `percent` (0 to 100). In the `legal` namespace only `reviewed` strings count; in every
   other namespace `translated` and `reviewed` both count.
3. `GET /api/studio/translations/{locale}?namespace=` lists each `key` with its `source` (the English
   value), `value`, `state` and `note`; `PUT /api/studio/translations/{locale}/{key}` saves `value`,
   `state` and `note`.
4. Rule 4 of preflight is the shipping gate for a chapter's strings, and every catalogue save is validated. Every named placeholder in the source, written `{name}`, must appear in the translated value exactly
   once; a value missing one or repeating one is rejected. A value containing markup (`<` or `>`) is
   rejected. Nothing is saved on a rejection.
5. The console's translation screen is a grid with namespaces down the side, locales across the top and
   coverage in each cell; a cell below 100 percent opens its missing keys. Chapter titles are edited as
   transcreations, with the previous chapters' titles in both languages shown beside them.

### Supporters, insights and settings

1. `GET /api/studio/tips` lists tips newest first, 50 per page by default and never more than 200,
   paged by `next_cursor`. Each row carries `id`, `tip_id` (the Tipbox `tip_id`, null for a manual tip), `received_at`,
   `source` (`tipbox` or `manual`),
   `amount`, `currency`, `settled_amount`, `rate`, `message`, `supporter_email`,
   `matched_reader_email`, `match_method`, `entitlement` (`granted`, `below_threshold`, `unmatched`,
   `awaiting_confirmation` or `revoked`) and `state` (`received`, `refunded` or `disputed`).
2. `POST /api/studio/tips/{id}/confirm-match` confirms an `address` match and applies the entitlement
   rule to it; it is rejected for any other match method.
3. `POST /api/studio/tips` records a manual tip with `amount` in `usd`, `received_at` and `reason`. It
   has `source` `manual`, counts in totals and grants nothing. An `amount` that is not a whole number
   above 0, a missing or malformed `received_at`, or a missing `reason` is rejected naming the field and
   records nothing.
4. `GET /api/studio/tips/totals` returns the sum of `settled_amount` and the count of `received` tips
   by calendar month (`YYYY-MM`, in UTC) and by source; refunded and disputed tips are excluded.
5. `GET /api/studio/overview` returns four cards: `next_drop` (the next scheduled chapter, its release
   moment and whether its preflight passes), `unready` (failing preflight rules of every draft, ready
   and scheduled chapter), `support` (count and total of received tips in the last 30 days against
   the 30 days before, and entitlements granted), and `reading` (chapter opens from the server counts
   beside completions and abandonments from measured events, never summed), plus `alerts` and
   `revocations`.
6. `GET /api/studio/settings` and `PATCH /api/studio/settings` read and change `name`, `contact_email`,
   `time_zone`, `early_access_threshold` and `credit_threshold`, and show `currency` (`usd`),
   `default_locale` (`en`) and `asset_version`. A threshold that is not a whole number of at least 0,
   a credit threshold below the early-access threshold, or a time zone that is not a real zone name is
   rejected and changes nothing.
7. `GET /api/studio/integrations/tipbox` returns `page_url`, `secret_last_four` (the last four
   characters of the signing secret, `81d7` for the seeded one), `secret_created_at` and
   `secret_last_used_at`, and never the secret itself. `PUT /api/studio/integrations/tipbox/secret`
   rotates it to a new `secret` of at least 16 characters, after which a notification signed with the
   previous secret is answered `401`; a shorter secret is rejected naming the field. The full secret is
   never read back by any endpoint.
8. `POST /api/studio/asset-version` raises the global asset version by one (the seeded version is
   `66`). Every manifest then points at the new version's image addresses, and the old version's image
   addresses answer `404`.

## User flow

### Routes

The information architecture and routing, public and studio:

| Route | Purpose | Auth |
|---|---|---|
| `/` | Title screen with `read now` | none |
| `/chapters` | Record rack of chapter sleeves | none |
| `/chapter/:id` | Reader, or locked state, for a chapter of `Vol. I` | none; a reader session unlocks early access |
| `/volumes/:volume/chapter/:id` | Reader, or locked state, for a chapter of a later volume | as above |
| `/about` | The four-section story of the comic and its makers | none |
| `/legal` | Legal notice and terms of use | none |
| `/support/return` | Thank-you page after tipping, reads `token` | none; a reader session attaches the tip |
| `/account` | Reader address, language, notifications, export, deletion | reader |
| `/fr`, `/fr/chapters`, `/fr/chapter/:id`, `/fr/volumes/:volume/chapter/:id`, `/fr/about`, `/fr/legal`, `/fr/support/return`, `/fr/account` | French versions | as above |
| `/sitemap.xml`, `/fr/sitemap.xml` | Published addresses per language | none |
| `/studio/sign-in` | Author sign-in | none |
| `/studio` | Overview with `Next drop`, `Unready work`, `Support` and `Reading` cards | author |
| `/studio/volumes` | Volume cards and `New volume` | author |
| `/studio/volumes/:volumeId` | Chapter table and `New chapter` | author |
| `/studio/chapters/:chapterId` | Chapter editor: titles, descriptions, cover, boards, waivers, release state | author |
| `/studio/chapters/:chapterId/boards/:boardId` | Board editor: panel filmstrip and file drop | author |
| `/studio/chapters/:chapterId/panels/:panelId` | Panel composer | author |
| `/studio/translations` | Coverage grid | author |
| `/studio/translations/:locale` | One locale's editor | author |
| `/studio/releases` | Release calendar and preflight | author |
| `/studio/supporters` | Tip list and totals | author |
| `/studio/insights` | Server counts beside measured events | author |
| `/studio/settings` | Studio settings and the asset version | author |
| `/studio/settings/integrations` | Tipbox page and signing secret | author |

### Entry and redirects

- `/` and `/fr` are the title screens; the root never redirects by browser language.
- A signed-out visitor opening any `/studio` route other than `/studio/sign-in` is sent to
  `/studio/sign-in` and returned to that route after signing in; signing out returns to
  `/studio/sign-in`.
- A signed-out visitor opening `/account` gets the reader sign-in dialog over `/chapters`, and the
  account page after signing in.
- Apart from `/account` and an expired session, the reader sign-in dialog is offered in exactly three
  places: `notify me` on a locked chapter, the end of the last readable chapter, and the tip return page. There is no sign-in link in the header.
  Signing in returns the reader to the page they were on.
- A session that has expired or been revoked mid-action: the next request is denied, the app forgets
  the session and offers sign-in again without losing the page.
- A reader whose early access lapsed while reading sees the locked state on their next chapter request.
- An unpublished chapter's address redirects temporarily to `/chapters`.
- A locked chapter never reveals a manifest or an image; the rack still shows its sleeve.

### Journeys

1. **First visit.** Open `/`; the consent strip takes focus; press `Decline`; press `read now`; the
   rack at `/chapters` shows open sleeves `01.welcome to Varny`, `02.under pressure`,
   `03.sheep don't sleep` and locked sleeves for chapters 4 and 5; press `01.welcome to Varny`;
   `Next track is loading...` gives way to the reader at `01:01`; press the right arrow key four times
   to reach `01:05`; the next-track face shows `under pressure`; press it; the reader opens
   `/chapter/2` at `02:01` without a reload.
2. **Return visit.** Having opened chapter 2, open `/chapters` again; the rack opens with the chapter 2
   sleeve selected.
3. **Locked chapter.** Signed out, open `/chapter/4`; see `04. scratch that !`, `This chapter opens <date>.`, `notify me`, `support us` with `Supporters read it as soon as it is finished.`, and the
   chapter 3 sleeve.
4. **Early access.** On `/chapter/4` press `notify me`, sign in as `reader@example.com` with
   `deku-demo-pw-2026`; the reader opens chapter 4 at `04:01` in place.
5. **Tip.** On `/chapters` press `support us`; the Tipbox page opens in a new tab with a
   `return_token`; Tipbox later sends the reader to `/support/return?token=<token>`; sign in there;
   the page states whether early access is active, pending or not granted.
6. **Text mode.** In any readable chapter press `read as text`; the panels' descriptions appear as an
   ordered list; for chapter 1 the first reads `Doudou steps off the night bus into Varny.`
7. **Language.** On `/about` press `FR`; the curtain sweeps; the address is `/fr/about`, the header
   reads `chapitres` and `a propos`, and the page never reloaded.
8. **Drawing to panel.** Sign in at `/studio/sign-in` as `author@example.com`; open Volumes; press
   `New volume`, name it `Vol. II` in the modal; press `New chapter`, enter the titles `the night shift` and
   `le service de nuit`; press `New board`; drop
   files named `c1b1p1-back.png` and `c1b1p1-stage.png`; the filmstrip shows panel 1 with two layers;
   open the panel composer; set the `stage` layer's depth to `3`; its mark moves on the depth ruler.
9. **Chapter to published.** In that chapter add both panel descriptions and a cover; press
   `Mark ready`; press `Run preflight` and see every rule pass; press `Publish now`; a full-page
   confirmation names the published chapter.
10. **Tip to insight.** Open `/studio/supporters`; the newest tip is first with its amount, source,
    message, match and entitlement, beside totals by month and by source; open `/studio/insights`;
    `Server counts` and `Measured events` sit side by side.
11. **Translation.** Open `/studio/translations`; open the `fr` column's `consent` cell; change
    `consent.accept`; save; the cell still reads 100 percent.

### States

- Every public route has a loading state: the first-load screen on the first visit, a thin bar along
  the bottom afterwards. Nothing else appears over the scene before it has arrived.
- A rack whose volume list comes back empty shows the recoverable error with a retry.
- The supporter list with no tips, the page-view list with no views and a studio
  volume with no chapters each show an empty state saying so.
- A failed request shows a named, recoverable state with a retry; no route ever shows a raw error, a
  stack trace or a key path.
- The studio shows skeleton rows while loading, never a spinner that reflows the layout, and an empty
  studio offers the guided path: create a volume, then a chapter, then a board, then import panels.

## UI/UX notes

**North star.** The first moment should feel like stepping inside a drawn night-time world, with the
interface almost out of the way. **Register:** consumer and editorial for the public site, where the
scene is seen first and the chrome is quiet; operational for the studio console, which is a plain,
fast document application with no scene, no physics and no heavy motion.

**Palette by role.** The language divider and the inactive language buttons are deep neutrals. Two families do nearly all the work: a near-black neutral, used for text on light
ground, the header, the footer, the wordmark and the entry button, and a near-white warm neutral with
a faint pink tint, used for text on dark ground, the entry button's label, every icon and the page
ground. The chrome follows the ground under it rather than the route: on the title screen, while a
chapter loads, and on the about page's dark support section the header, footer and fullscreen control
turn cream; the language selector turns cream too, except on the title screen, where it alone stays a
deep neutral. Chapter sleeves and the reader's timeline capsule are near-black
capsules with white text, and a locked sleeve is one step lighter, a deep neutral. There is exactly one
saturated colour in the product, a mid, vivid amber, and it is spent only on the thin loading bar;
the first-load screen's progress line is a light, soft orange on a near-white warm neutral paper
ground. The language curtain is a near-white, muted red over a paper-coloured curtain. A near-white
soft orange appears only as a chip tint. There is no dark mode and no theme switch, so light is the
committed mode for chrome over a scene that is mostly night. Meaning is never carried by colour alone:
a locked sleeve also shows a padlock and says `locked`. The studio console alone carries three meaning-carrying colours, each always paired with an icon
and a word: failure and danger in a deep, muted red, warning in a deep, muted amber, success in a deep,
muted green; the public site wears none of them, so the loading bar's amber stays its only saturated
colour. The exact shades are yours, so long as these roles and that single public amber hold.

**Typeface and type.** One family, `Inter`, variable from weight 100 to 900. The scale is deliberately flat, with no
ladder of ever larger headings: the reader timecode at 9.5px weight 700, the language buttons at 10px
weight 600, the sleeve timecode at 12px weight 700, the sleeve subtitle at 14px, the header links and
footer at 15px, the tip label at 15px weight 700, about body copy at 16px, the sleeve title at 17px
weight 800 on one line, team card bodies at 18px, the reader loading caption and legal paragraphs at
20px, the entry button label at 35px weight 600, the legal page heading at 60px with section headings
at 30px. The four about headings are sized against the window width so they fill the same share of
any screen, in weight 900. Figures line up in every studio table.

**Shape, spacing and density.** Spacing is placed by feel against the scene, with no grid of spacing constants. Corners are very round and the border radius is its own scale: small pills for the
language switch, big soft capsules for sleeves and the timeline, fully round chips, a fully round entry
button. The public site is spacious and almost empty around the scene; the studio is comfortable and
dense enough that a chapter table fits one screen.

**Motion character: eased and playful.** Chrome moves with the browser's own simple transitions so it
works before the scene has loaded: the consent strip slides up and slides away; the four corner
controls wait just off screen until consent is answered and then rise together; hovering a header link
tips it a few degrees, the two links in opposite directions, and draws a rounded outline around it;
hovering the consent buttons tips them in opposite directions, the decline button further than the
accept button. Text arrives word by word, rising from
behind an invisible edge; buttons and sleeves pop in from nothing; leaving the rack shrinks every
sleeve before the next page appears; leaving a chapter tips the timeline back and away; leaving the legal page fades it to transparent on a linear curve, and leaving the title screen or the about page fades to transparent on an ease-out curve. The chrome recolouring between grounds is a short colour transition, and the reader's animated backdrop is a slow, eased charcoal gradient drifting forever. Nothing
animates on hover on a touch device. Reduced-motion handling applies anywhere motion appears: when the system asks for reduced motion the camera jumps between
panels instead of flying, the record stops spinning, reveals become instant, the physics pile lies
still but can still be dragged, the team cards face front, the marquee stops, the surprise is suppressed entirely with its trigger, and the consent strip simply appears.

**Components and states.** Every control has a resting, pointed-at, pressed, focused and unavailable
state; an unavailable control, such as `previous panel` on the first panel, is dimmed and inert, never
signalled by colour alone. Every form field has a visible label above it and its error directly beneath it, naming the problem.
Modal dialogs close on Escape. Destructive studio actions (unpublish,
raising the asset version, rotating the secret) confirm first and say what will happen.
The primary action on each page is the one visually loudest thing: `read now` on the title screen, the selected
sleeve on the rack, the next-track face at the end of a chapter; everything else on that page is
quieter.

**Accessibility.** WCAG 2.2 AA contrast for all text, including white on the near-black sleeves and
any text drawn over the scene, which carries a thin outline or a solid ground. Full keyboard navigation
with a visible focus ring of at least 3:1 contrast on both light and dark grounds. Every icon-only
control has a label. Touch targets are at least 44 by 44 pixels of hit area even where the icon is
smaller. Text that exists only for assistive technology is hidden by clipping, never by zero opacity
and never by `display: none`. Every route has one level-one heading. Announcements: a polite live region announces a
chapter loading, a chapter ready, a reached panel's description and a completed language switch; an
assertive one announces a failed load and a rejected studio save. The product stays usable at 200
percent text size, where the sleeve and timeline titles truncate with an ellipsis and keep the full
title as their accessible name. Public pages stay usable with no sideways scrolling at a 320 pixel wide
viewport.

**Responsive.** The responsive layout holds at every viewport width from the narrowest supported width, a small phone, to a wide desktop. On a
wide desktop the header links sit either side of the centred wordmark and both arrow pairs show. These are three separate steps, never one mobile
layout. At a tablet width the arrow pairs disappear and reading becomes drag, keys and the slider.
Slightly narrower, the corner controls rearrange: the fullscreen control lifts, the language selector
moves to the bottom left and the about rail disappears. Narrower still, at a phone width, the header
links move to the two edges with a smaller wordmark between them, the tip control moves to the top
centre, the rack and the timeline scale down, and nothing overflows sideways. Full-height surfaces use the window's real
visible height, so a phone's retracting browser bar never pushes the `Scroll down` prompt out of view. In portrait orientation the about headings grow to fill more of the width.

## Technical requirements

- **Rendering model:** a single-page application over a JSON API. The Litestar server answers every
  page route with a small HTML document that already carries that route's title, description, `lang`
  and HTTP status, and the Preact application renders the page in the browser from the JSON API on
  the same origin under `/api`.
- **Backend:** Litestar on Python 3.12, one server process serving the API, the built front end, the
  sitemaps and the page documents.
- **Frontend:** Preact with Vite and TypeScript, served as a production build by the same process.
- **Database:** PostgreSQL at `DATABASE_URL`.
- **Object storage:** MinIO, an S3-compatible store, at `STORAGE_ENDPOINT` in the bucket named by
  `STORAGE_BUCKET`, with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The bucket already exists and
  is private.
- **Auth:** app-implemented email and password with bearer tokens sent as `Authorization: Bearer <token>`, in two separate systems for readers and authors. The console keeps a signed-in author's token in local storage under `dd-studio-session`.
- **Health:** `GET /api/health` returns `200` with `{"status": "ok"}` once the database and the bucket
  answer.
- **Observability:** structured logging, one JSON line per request on stdout carrying the `request_id`, method, route, status and
  duration, and never an address, password, token or signature.
- **Environment:** read `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DATABASE_URL`, `STORAGE_ENDPOINT`,
  `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY` from the environment; hardcode no
  host, port or credential.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database,
cache, queue, object store, identity provider or mail vendor; the only backing services available in
this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation.

- Every `/api` response carries an `X-Request-Id` header, and every error body repeats it as
  `request_id`, so a reader reporting a problem can quote it.
- Every rejection answers a client error with the body `{"error": {"code": ..., "message": ..., "field": ..., "request_id": ...}}`; a version conflict adds `current`, a preflight rejection adds `failures`, and an import
  rejection adds `file`. Business-rule and validation rejections are never a server error and never a silent success.
- Every identifier the API returns is a 26-character opaque, sortable string. Chapter, board and panel
  numbers are small integers used in addresses and layer identifiers; they are not identifiers.
- Security and compliance: every response, page or API, carries `Strict-Transport-Security`, a `Content-Security-Policy` whose
  directives include `frame-ancestors 'none'`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and a `Permissions-Policy` that allows
  `fullscreen` and denies everything else the product does not use.
- An image of a published chapter answers `Cache-Control: public, max-age=31536000, immutable`. A
  published chapter's manifest answers `public` with a one-hour `max-age`. A manifest of a chapter that
  is not published, every signed image, every response that depends on a reader token, and every
  `/api/me` response answers `Cache-Control` containing both `private` and `no-store`.
- The scheduler works on absolute instants, never on wall-clock comparisons. A scheduled chapter is published by the app itself, within 60 seconds after its release moment, with
  nothing outside the app prompting it.
- A `sig` on an image address is the lowercase hexadecimal HMAC-SHA256 of that address and its `expires`,
  keyed with the studio's `image_signing_key`, which only the server holds; a signature for one image does
  not open another.
- Zero-asset substitution: no binary asset ships with the build. Seeded panel layers, covers and every placeholder picture are
  drawn by the app: a flat colour from the palette chosen by the layer's role, a simple silhouette by
  role, and the layer identifier stamped in a corner.
- The `Inter` font files are bundled into the build and served from the app's own origin, with the
  fallback stack `"Helvetica Neue", Helvetica, Arial, "Liberation Sans", system-ui, sans-serif`.
- The app makes no outbound network call at runtime: no analytics host, no font service, no video
  embed and no call to Tipbox.
- Seeding runs on first start and again on every start without duplicating anything.

## Data model

Twenty-eight tables. All timestamps are UTC instants. Money is integer minor units.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**studios** (one row): `id`, `name` `Doudou Fever`, `contact_email` `hello@example.com`,
`time_zone` `Europe/Paris`, `currency` `usd`, `default_locale` `en`, `early_access_threshold` `500`,
`credit_threshold` `2000`, `asset_version` `66`, `image_signing_key` (32 random bytes generated on
first start and kept across restarts, never returned by any endpoint), `created_at`.

**locales:** `code` (`en`, `fr`), `language_tag` (`en-GB`, `fr-FR`), `display_name` (`English`,
`Francais`), `is_default`, `active`, `position`.

**volumes:** `id`, `label`, `position` (the API's `order`, unique, 1 upward), `created_at`.

**chapters:** `id`, `volume_id`, `number` (unique within the volume), `state`, `release_at`,
`published_at`, `early_access_days`, `content_tag`, `cover_object_key`, `version`, `created_at`,
`updated_at`. **chapter_texts:** `chapter_id`, `locale`, `title`, `description`, one row per chapter
and locale. **chapter_waivers:** `chapter_id`, `locale`, `reason`, `expires_at`.

**boards:** `id`, `chapter_id`, `number` (unique within the chapter), `name`, `version`.
**panels:** `id`, `board_id`, `number` (unique within the board), `camera_x`, `camera_y`,
`entry_duration`, `selectable`, `hold`, `wide`, `version`. **panel_descriptions:** `panel_id`,
`locale`, `text`, one row per panel and locale.

**layers:** `id`, `panel_id`, `role` (unique within the panel), `kind` (`image`, `map`, `sprite`),
`draw_order` (unique within the panel), `depth`, `offset_x`, `offset_y`, `scale`, `opacity`, `blend`,
`displacement_source_id`, `displacement_strength`, `clip`, `loop_mode`, `localised`, `retain`,
`version`. **layer_images:** `id`, `layer_id`, `locale` (`all`, or the locale code of a localised
image), `object_key`, `byte_length`, `content_hash`, `stored_at`, one row per layer and locale.
**frame_tables:** `layer_id`, `object_key`, `frame_count`, `clips`, `byte_length`.

**messages:** `namespace`, `key`, `locale`, `value`, `state`, `note`, `updated_at`, one row per key and
locale.

**members** (authors): `id`, `email`, `name`, `password_hash`, `created_at`, `last_seen_at`.
**studio_sessions:** `token_hash`, `member_id`, `created_at`, `expires_at`, `revoked_at`.

**readers:** `id`, `email` (unique ignoring case), `password_hash`, `locale`, `notifications`,
`last_chapter_id`, `last_chapter_at`, `created_at`. **reader_sessions:** `token_hash`, `reader_id`,
`created_at`, `expires_at`, `revoked_at`. **progress:** `reader_id`, `chapter_id`, `fraction` (three
decimal places), `last_panel`, `updated_at`, one row per reader and chapter.

**entitlements:** `id`, `reader_id`, `kind` (`early_access`, `credits`), `tip_id`, `granted_at`,
`expires_at`, `revoked_at`, `revoked_reason` (`refunded`, `disputed`).

**tips:** `id`, `source` (`tipbox`, `manual`), `external_id` (the Tipbox `tip_id`), `amount`,
`currency`, `settled_amount`, `rate`, `message`, `supporter_email`, `matched_reader_id`, `match_method`
(`token`, `address`, `none`), `match_confirmed_at`, `state` (`received`, `refunded`, `disputed`),
`received_at`, `state_changed_at`, `reason`. **return_tokens:** `token_hash`, `issued_at`,
`expires_at`, `claimed_by_reader_id`, `claimed_at`. **webhook_events:** `id`, `source`, `external_id`
(the event `id`), `event_type`, `signature_verified`, `payload`, `received_at`, `processed_at`.

**page_views:** `id`, `route`, `viewed_at`. **chapter_opens:** `id`, `chapter_id`, `opened_at`, one row
per manifest served. **measured_events:** `id`, `name`, `params`, `received_at`.

**audit_records:** `id`, `actor_email`, `action`, `subject_type`, `subject_id`, `request_id`,
`created_at`. **integrations:** `provider` (`tipbox`), `signing_secret`, `page_url`,
`secret_created_at`, `secret_last_used_at`. **alerts:** `id`, `kind`, `subject_id`, `message`,
`created_at`.

**Derived, never stored:** a chapter's count in its volume (the right-hand side of a sleeve timecode);
whether a chapter is locked for a caller; chapter-open counts by hour; byte totals; coverage percentages; a tip's `entitlement`
column; a panel's position across its chapter.

**Invariants, as they must hold under concurrent requests:**

- Two deliveries of the same Tipbox `tip_id`, sent at the same moment, leave exactly one tip row and
  at most one grant.
- Two deliveries of the same verified event `id` record it once and apply it once.
- A reader has at most one progress row per chapter; two simultaneous progress writes from two devices
  end in one row holding the merge of both.
- A chapter is published once: `published_at` never changes after it is first written, and two
  simultaneous publish requests leave exactly one `chapter.published` audit record.
- Within a volume two chapters never share a number; within a panel two layers never share a role or
  a draw order.
- Two edits to one row carrying the same `version`, sent at the same moment: exactly one is accepted and
  the other answers `409`.
- Two readers claiming one return token at the same moment: exactly one claim succeeds.
- A tip grants each entitlement kind at most once.

**Seed data.** Studio, locales, the Tipbox integration (`tbx_whsec_5f3a9c2e81d7`,
`https://tipbox.example/doudou-fever`) and the four accounts as above. Volume `Vol. I` (order `1`)
holds six chapters, where S is the moment of first start:

| Number | `en` title | `fr` title | State | Release moment |
|---|---|---|---|---|
| 1 | `welcome to Varny` | `bonjour Varny` | `published` | 60 days before S, at 18:00 UTC |
| 2 | `under pressure` | `sous pression` | `published` | 40 days before S, at 18:00 UTC |
| 3 | `sheep don't sleep` | `moutons insomniaques` | `published` | 20 days before S, at 18:00 UTC |
| 4 | `scratch that !` | `on efface tout !` | `scheduled` | 3 days after S, at 18:00 UTC |
| 5 | `wow ...` | `ouf ...` | `scheduled` | 20 days after S, at 18:00 UTC |
| 6 | `the big mix` | `le grand mix` | `draft` | none |

Every chapter's `early_access_days` is `7`, so chapter 4 is inside its early-access window from the
start and chapter 5 is outside it. Chapters 1 to 5 each have a cover, descriptions in both languages
and pass all ten preflight rules; chapter 6 has one board, one panel with one layer and descriptions,
and no cover. Chapter 1 has board 1 with panels 1, 2 and 3 and board 2 with panels 1 and 2; chapters 2
to 5 each have board 1 with panels 1, 2 and 3. Every panel of chapters 1 to 5 has three layers: `back`
at depth `-4` with draw order `0`, `stage` at depth `0` with draw order `1` and `characters` at depth `2`
with draw order `2`; chapter 6's single panel has one layer, `back` at depth `-4` with draw order `0`.
Panel 1 of board 1 of chapter 1 also has a localised layer `sign` at depth `1` with draw order `3` and an
English and a French image. Every seeded layer has kind `image`, `offset_x` and `offset_y` `0`, `scale`
`1`, `opacity` `1` and `blend` `normal`, and only `sign` is localised. Every seeded panel is `selectable`,
with `hold` and `wide` false, `entry_duration` `0.6`, and `camera_x` and `camera_y` `0`. Every image is
stored in the bucket at its key.

Chapter descriptions:

| Chapter | `en` description | `fr` description |
|---|---|---|
| 1 | `Doudou arrives in Varny with a suitcase full of records.` | `Doudou arrive a Varny avec une valise pleine de disques.` |
| 2 | `The first gig goes wrong in every possible way.` | `Le premier concert tourne mal de toutes les facons.` |
| 3 | `A night without sleep before the big audition.` | `Une nuit blanche avant la grande audition.` |
| 4 | `Doudou erases the whole set and starts again.` | `Doudou efface tout le set et recommence.` |
| 5 | `The crowd finally dances.` | `La foule danse enfin.` |
| 6 | `Jean-Loic and Milan plan the biggest party in Varny.` | `Jean-Loic et Milan preparent la plus grande fete de Varny.` |

Panel descriptions, by chapter, board and panel:

| Chapter | Board | Panel | `en` description | `fr` description |
|---|---|---|---|---|
| 1 | 1 | 1 | `Doudou steps off the night bus into Varny.` | `Doudou descend du bus de nuit a Varny.` |
| 1 | 1 | 2 | `The flat above the bar is small and loud.` | `L'appartement au-dessus du bar est petit et bruyant.` |
| 1 | 1 | 3 | `Jean-Loic hands Doudou a key and a warning.` | `Jean-Loic donne a Doudou une cle et un avertissement.` |
| 1 | 2 | 1 | `Milan films dinner for her followers.` | `Milan filme le diner pour ses abonnes.` |
| 1 | 2 | 2 | `Doudou unpacks the turntables on the kitchen table.` | `Doudou deballe les platines sur la table de la cuisine.` |
| 2 | 1 | 1 | `The speakers crackle before the first song.` | `Les enceintes gresillent avant le premier morceau.` |
| 2 | 1 | 2 | `Nobody on the dance floor moves.` | `Personne ne bouge sur la piste.` |
| 2 | 1 | 3 | `Doudou pulls the plug in a panic.` | `Doudou debranche tout en panique.` |
| 3 | 1 | 1 | `Doudou counts beats instead of sheep.` | `Doudou compte des temps au lieu des moutons.` |
| 3 | 1 | 2 | `Milan brings midnight pancakes.` | `Milan apporte des crepes de minuit.` |
| 3 | 1 | 3 | `The sun rises over an unfinished mix.` | `Le soleil se leve sur un mix inacheve.` |
| 4 | 1 | 1 | `Doudou deletes every track on the laptop.` | `Doudou efface chaque morceau de l'ordinateur.` |
| 4 | 1 | 2 | `Jean-Loic hums a tune from the bar.` | `Jean-Loic fredonne un air du bar.` |
| 4 | 1 | 3 | `A new beat starts with that tune.` | `Un nouveau rythme nait de cet air.` |
| 5 | 1 | 1 | `The whole town queues outside the bar.` | `Toute la ville fait la queue devant le bar.` |
| 5 | 1 | 2 | `Doudou drops the first beat.` | `Doudou lance le premier rythme.` |
| 5 | 1 | 3 | `Varny dances until morning.` | `Varny danse jusqu'au matin.` |
| 6 | 1 | 1 | `Posters for the big mix cover the flat.` | `Les affiches du grand mix couvrent l'appartement.` |

Tip `tbx_seed_001`, received 2 days before S: from `reader@example.com`, amount `800` `usd`, settled `800`, rate `1.000000`, message
`go doudou go`, matched by token to `reader@example.com`, `received`, granting early access when it was received. Tip `tbx_seed_002`, received 1 day before S: from `friend@example.com`, amount `300` `usd`, settled `300`, rate `1.000000`, message
`for the bus scene`, match `none`, `received`, granting nothing. `reader2@example.com` has progress on
chapter 1 of `Vol. I` at `0.400` with last panel `2`, and that chapter as their last chapter, 1 day
before S. Every catalogue string exists in both languages
as `reviewed`. Seeding must be idempotent - restarting the app must not duplicate rows or objects.

## Front-end specification

**Header.** Fixed along the top: the wordmark `Doudou Fever` as two lines of heavy lowercase
lettering, centred, with the byline `by Camille Rouyer and Damien Lorca` beneath it for machines and
selection; the link `chapters` to its left and `about` to its right, the active one heavier. The
wordmark links to `/` except on the title screen, where it does not navigate. At phone width the two
links move to the two edges.

**Footer.** One link, `legal notice & terms of use`, in the bottom right corner, with an underline that
grows from its centre on hover.

**Corner controls.** The language selector (`EN`, `|`, `FR`, uppercase), a fullscreen control named
`enter fullscreen` or `exit fullscreen` drawn as four arrowheads pointing into or out of the corners,
the footer and the tip control. All four wait off screen until the consent strip is answered. The
fullscreen control is absent where the browser offers no fullscreen.

**Edge strips.** Two invisible strips down the left and right edges prevent edge gesture theft: they swallow a drag that starts right
at the edge, so a sideways drag through a chapter is never taken by the browser as back or forward.

**Iconography.** Every icon is drawn inline and takes the current colour: a play triangle with its back edge
pinched inward for the sleeve and, squeezed into a small square, the next-panel icon on the next-track face, a double chevron with a leading bar (a
fast-forward mark) for the arrows, mirrored for previous, a padlock with a round shackle for locked
sleeves, four corner arrowheads for fullscreen, a rounded down arrow for the about scroll prompt, and a
thin rule with one small step in it for the loading line.

**First-load screen.** The loader drives a progressive boot. On the paper ground: a ghost of the wordmark barely visible behind, the hero's
head in the middle pulling a sequence of faces as the drawings arrive, and the stepped rule filling
from the left in soft orange. After the first load, the quieter in-page loader shows only a thin amber bar along the
bottom edge.

**Title screen composition.** The record spins slowly above the centre (hidden on narrow screens); `read now` is a
large near-black capsule button with a cream label near the bottom. Behind them the night scene: a
looping sky, a moon, a city silhouette, a vegetable field, a stage platform with speakers, fireflies,
Doudou and his two flatmates.

**Rack composition.** A curved carousel of sleeves under a gentle perspective, the centred one facing the reader
and the others turned slightly away. Each sleeve is a near-black capsule: the play icon on the left, a
text column of title, subtitle and timecode, and on wide screens a pair of small arrows on the right,
the first disabled on the first sleeve and the second on the last. A locked sleeve is the lighter
capsule with the padlock and a not-allowed cursor. The tip control is a pill with a thin cream border that brightens toward white on hover, whose label
rolls up on hover to reveal a second copy, one step larger and cream, like a departure board; the roll
never happens on touch.

**Reader.** Wheel input on both axes is continuous and mapped to the single horizontal position. Settling on a sleeve in the rack snaps it into place. The capsule looks like a music player: the cover, the title, the subtitle and the white
progress line; it pulses gently while the chapter is still streaming; the two arrow controls sit just to
its right on wide screens. Clicking a panel flies the camera to frame it; Escape flies back out;
selecting a panel is refused during the chapter's first and last tenth, while it is arriving or
leaving. A second input within a moment of a selection is swallowed, so mashing an arrow key never
skips panels. Near layers slide past faster than far layers, continuously, with no jump when a panel
becomes selected.

**About.** The headings carry a thin cream outline so black lettering stays readable over the drawings.
The team cards are rotated rounded title pills over their body text with two social icons; the second
card mirrors the first. The support section is dark, and everything in the chrome turns cream while it
is in view. Each chip is a pill with the same rolling label as the tip control.

**Not-found composition.** A dark gradient from near-black to deep neutral, one drawing behind the text, the line
`Oopsy, page not found` in cream, and `Go back to home` as a cream pill that turns inside out on hover.

**Studio console.** A left rail of seven destinations: `overview`, `volumes`, `translations`,
`releases`, `supporters`, `insights` and `settings`; a header bar with the studio name `Doudou Fever`, a
search field and the signed-in author's initials. The chapter table's columns are `Number`, `Title`,
`State`, `Release`, `Readiness` and `Image bytes`. The board editor is a filmstrip of panel thumbnails,
each showing its layer count and a warning mark for any failing preflight rule. The panel composer puts
a live preview of the real panel in two thirds of the width, the layer list back to front on the right
(role, thumbnail, depth, visibility, solo and lock toggles), the selected layer's properties below it, a
depth ruler under the preview showing every layer as a draggable mark at its depth, and a parallax
scrubber that sweeps the camera across the panel. The releases screen is a month calendar with a list
beneath it. The insights screen shows `Server counts` and `Measured events` in two columns. Creating a
volume, chapter or board, recording a manual tip and adding a waiver each open a modal dialog.

## Constraints

- One studio. Two languages, `en` and `fr`, with a third addable as data.
- No outbound mail of any kind: no sign-in links, no invitations, no drop notifications, no alerts by
  mail. `notify me` only records the preference.
- No second factor, recovery codes, studio invitations or team management; authors are seeded.
- No comments, social graph, user-generated content, in-product store or checkout, native app,
  animation authoring tool, advertising or audio.
- No payment processing inside the app; money arrives only as Tipbox notifications and manual entries.
- No outbound call to Tipbox, no reconciliation pull and no outbound studio webhook.
- No deletion of chapters, boards or panels, and no renumbering of chapters.
- No debug query parameters.
- No rate limiting or quotas beyond the sign-in lockout; abuse control is the signup decoy field and that lockout.
- No third-party analytics, font service or video embed; no network call at runtime.
- No texture compression formats, reduced variants or hardware classes; images are stored PNGs.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never a server error and never a silent
success. Bearer auth is required on every `/api/me` and `/api/studio` endpoint except the two sign-in
endpoints; the webhook authenticates by its signature, never by a token. Pagination is by opaque cursor: a paged list returns
`{"items": [...], "next_cursor": ...}`, and passing `cursor` fetches the next page. Response shapes are stable: a field is never renamed or removed.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | | `{"status": "ok"}` |
| `GET /api/volumes` | `locale`; optional reader bearer | array of `{"id", "label", "order", "chapter_count", "chapters": [{"number", "title", "locked", "release_at", "cover_url"}]}` |
| `GET /api/volumes/{order}/chapters/{number}` | `locale`; optional reader bearer | `{"volume", "number", "title", "description", "total", "content_tag", "boards": [{"number", "panels": [{"number", "index", "description", "selectable", "layers": [{"role", "identifier", "kind", "depth", "offset_x", "offset_y", "scale", "opacity", "blend", "draw_order", "image_url", "frame_table_url"}]}]}]}`, or `404` |
| `GET /api/textures/v{asset_version}/{order}/{number}/{file_identifier}.png` | `tag`; `expires` and `sig` when not published | PNG bytes, or `404` |
| `GET /api/textures/v{asset_version}/{order}/{number}/{file_identifier}.json` | `tag`; `expires` and `sig` when not published | frame table JSON, or `404` |
| `GET /api/covers/{order}/{number}.png` | | PNG bytes, or `404` |
| `GET /api/catalogue/{locale}` | | flat object of dotted keys to strings |
| `POST /api/page-views` | `{"route"}` | created |
| `POST /api/events` | `{"name", "params"}` | created |
| `POST /api/tips/return-tokens` | | `{"token", "expires_at"}` |
| `POST /api/tips/return` | `{"token"}`; optional reader bearer | `{"status"}` |
| `POST /api/webhooks/tipbox` | raw body; `Tipbox-Signature` header | `200`, or `401` |
| `POST /api/auth/register` | `{"email", "password", "locale", "website"}` | `{"access_token"}` |
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token"}` |
| `POST /api/auth/logout` | | no content |
| `GET /api/me` | | `{"email", "locale", "notifications", "created_at"}` |
| `PATCH /api/me` | `{"email", "locale", "notifications"}`, any subset | the reader |
| `GET /api/me/progress` | | `{"last_chapter", "last_chapter_at", "chapters": [{"volume", "chapter", "fraction", "last_panel", "updated_at"}]}` |
| `PUT /api/me/progress` | the progress document | the merged document |
| `GET /api/me/entitlements` | | array of `{"kind", "granted_at", "expires_at", "revoked_at", "active"}` |
| `POST /api/me/notify` | `{"volume", "chapter"}` | the reader |
| `GET /api/me/export` | | attachment `{"reader", "progress", "entitlements", "tips"}` |
| `DELETE /api/me` | `{"password"}` | no content |
| `POST /api/studio/auth/login` | `{"email", "password"}` | `{"access_token", "member": {"email", "name"}}` |
| `POST /api/studio/auth/logout` | | no content |
| `GET /api/studio/overview` | | `{"next_drop", "unready", "support", "reading", "alerts", "revocations"}` |
| `GET /api/studio/search` | `q` | array of `{"type", "label", "href"}` |
| `GET /api/studio/volumes` | | array of `{"id", "label", "order", "chapter_count"}` |
| `POST /api/studio/volumes` | `{"label"}` | the volume |
| `GET /api/studio/volumes/{id}/chapters` | | array of `{"id", "number", "titles", "state", "release_at", "published_at", "boards_ready", "boards_total", "image_bytes", "version"}` |
| `POST /api/studio/volumes/{id}/chapters` | `{"titles": {"en", "fr"}, "descriptions": {"en", "fr"}}` | the chapter |
| `GET /api/studio/chapters/{id}` | | the chapter with `boards`, `waivers`, `early_access_days`, `content_tag`, `has_cover` |
| `PATCH /api/studio/chapters/{id}` | `{"version", "titles", "descriptions", "early_access_days", "waivers"}`, `version` plus any subset | the chapter, or `409` |
| `PUT /api/studio/chapters/{id}/cover` | multipart `file` | the chapter |
| `POST /api/studio/chapters/{id}/boards` | `{"name"}` | `{"id", "number"}` |
| `GET /api/studio/boards/{id}` | | the board with `panels` and their `layers` |
| `POST /api/studio/boards/{id}/imports` | multipart `files` | `{"panels_created", "layers"}` |
| `PATCH /api/studio/panels/{id}` | `version` plus any panel field | the panel, or `409` |
| `PATCH /api/studio/layers/{id}` | `version` plus any layer field | the layer, or `409` |
| `GET /api/studio/chapters/{id}/manifest` | `locale` | the manifest, drafts included |
| `POST /api/studio/chapters/{id}/preflight` | | `{"passed", "failures": [{"rule", "message"}]}` |
| `POST /api/studio/chapters/{id}/ready` | | the chapter |
| `POST /api/studio/chapters/{id}/schedule` | `{"release_at"}` | the chapter |
| `POST /api/studio/chapters/{id}/cancel` | | the chapter |
| `POST /api/studio/chapters/{id}/publish` | | the chapter |
| `POST /api/studio/chapters/{id}/unpublish` | | the chapter |
| `GET /api/studio/translations/coverage` | | array of `{"namespace", "locale", "total", "translated", "reviewed", "percent"}` |
| `GET /api/studio/translations/{locale}` | `namespace` | array of `{"key", "source", "value", "state", "note"}` |
| `PUT /api/studio/translations/{locale}/{key}` | `{"value", "state", "note"}` | the entry |
| `GET /api/studio/tips` | `limit`, `cursor` | `{"items": [{"id", "tip_id", "received_at", "source", "amount", "currency", "settled_amount", "rate", "message", "supporter_email", "matched_reader_email", "match_method", "entitlement", "state"}], "next_cursor"}` |
| `POST /api/studio/tips` | `{"amount", "received_at", "reason"}` | the tip |
| `POST /api/studio/tips/{id}/confirm-match` | | the tip |
| `GET /api/studio/tips/totals` | | `{"by_month": [{"month", "count", "total"}], "by_source": [{"source", "count", "total"}]}` |
| `GET /api/studio/insights` | | `{"server": {"page_views": [{"route", "hour", "count"}], "chapter_opens": [{"volume", "chapter", "hour", "count"}]}, "measured": {"events": [{"name", "count"}]}}` |
| `GET /api/studio/page-views` | `route`, `limit`, `cursor` | `{"items": [{"route", "viewed_at"}], "next_cursor"}` |
| `GET /api/studio/settings` | | `{"name", "contact_email", "time_zone", "currency", "default_locale", "early_access_threshold", "credit_threshold", "asset_version"}` |
| `PATCH /api/studio/settings` | any subset of the changeable fields | the settings |
| `GET /api/studio/integrations/tipbox` | | `{"page_url", "secret_last_four", "secret_created_at", "secret_last_used_at"}` |
| `PUT /api/studio/integrations/tipbox/secret` | `{"secret"}` | the integration, without the secret |
| `POST /api/studio/asset-version` | | `{"asset_version"}` |

**No mocks.** PostgreSQL and MinIO are the facts. Panel images kept on the app container's filesystem
or in database blobs, a manifest that serves every chapter and hides the locked ones only in the page,
an image address that works for anyone who guesses it, an early access granted because a return page
was visited, a tip recorded from a body whose signature was never checked, a signature checked against
re-serialised JSON rather than the bytes received, a second tip row for a replayed notification, and a
publication that only flips a flag in the page are all violations. The object store and the database
hold what happened; the app's UI and its own responses can only reflect what lives there, never
substitute for it.

## Definition of done

A visitor can open the rack, read a published chapter panel by panel and switch language without a
reload, while a scheduled chapter's manifest and images stay unreachable to them. A reader whose
verified tip settles at `$5.00` or more reads that chapter early, and loses the access on the next
request after a refund. An author can import layered panels into the object store, run preflight and
publish or schedule a chapter that goes live on time.
