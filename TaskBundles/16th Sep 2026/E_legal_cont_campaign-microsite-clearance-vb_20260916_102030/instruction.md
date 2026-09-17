# Halden Drops

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser, land on
a limited-drop page in their own language, pick a product colourway, and follow a link that
carries that colourway and the campaign's attribution to their own market's storefront,
while staff sign in, translate a market, clear it legally and publish it, without hitting
an error page.

A staff member must NOT be able to change a market they hold no grant for, keep writing after
their grant has expired, or publish a market whose legal and owner approvals do not match the
content currently in it, by any means: not through the studio, and not by calling the API
directly with their own token. An image uploaded for a market that is not live must live in the
object store at its key and must not be readable by the public, neither through the app nor from
the bucket. Every refusal must say why, and every write and every refusal must land in an audit
log that the database itself will not let the app rewrite.

## Overview

Halden Drops is the publishing platform Halden Sport, a sporting-goods retailer, uses to put
each limited-drop collection online in seven locales and hand every visitor to one of six
national storefronts. The public side is one long scrolling narrative per campaign market: a
hero, a tagline, a collage, the collection, the artist, the story of one shoe, a lookbook, a
numbered footer list and a legal footer. The site sells nothing. Every commercial action is a
hand-off to the storefront, so the product is judged by whether that hand-off is complete,
correctly targeted and correctly counted.

Two campaigns are seeded. `Afterglow` is a capsule with the artist Tove Ardenne, live in France
and the United Kingdom and at every other stage of review elsewhere. `Dusk Parade` is a
one-product drop with every market still in draft.

The staff side is the studio, where five roles share one set of records and hold different
rights over them. Products and colourways are stored once and globally; a storefront link is
never typed by anyone and is derived from the market it is rendered for. Each market moves
through its own review on its own: a French approval never publishes Germany. An approval binds
to the exact content it approved, so an edit afterwards withdraws it. Publishing writes a
numbered artifact to the object store, and the live page is served from it.

The genuinely hard part is that authorization and evidence are the product: a grant is checked
at the moment of every request, including its expiry; an approval is only worth the content hash
it was given against; and the audit log is chained so that a rewritten row is detectable. What
this platform deliberately is not: no visitor accounts, no checkout, no cart, no stock, no
notifications, no analytics, no consent banner, no newsletter and no external calls at runtime.

## User roles

Staff hold accounts; visitors do not. Every staff right comes from a **grant**: a role, the
market it covers (or every market), whether it permits or denies, and an optional expiry. The table
below is the permission matrix; a cell's rights apply only inside that role's grants.

| Role | Read | Write |
|---|---|---|
| visitor (no account) | live market pages, legal pages, the privacy page, live media | **nothing** |
| `owner` | every campaign, market, product, translation, grant and the whole audit log | campaigns, strings, translations, market fields, shared and market images, submit, the owner approval, publish, unpublish, rollback, and grants for `editor` and `translator`. **Cannot record a legal approval or change a price.** |
| `editor` | the markets its grants cover | strings, translations, market fields, images and availability in those markets, submit. **Cannot approve, publish, change a price, or touch a market outside its grants.** |
| `translator` | the markets its grants cover | translations in those markets, submit. **Cannot write a product identifier, a model code, a swatch, a slot, a price, availability or any market field.** |
| `legal` | the markets its grants cover and their audit events | the legal approval and unpublish in those markets. **Cannot publish, record the owner approval, or edit content.** |
| `merchandiser` | every campaign and market | products, colourways, availability and prices. **Cannot edit copy, submit, approve or publish.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from an `editor`, `translator` or `merchandiser` session
to any `owner`-only or `legal`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is closed. There is no registration page and no registration endpoint; every account is
seeded. Every seeded account uses the password `deku-demo-pw-2026`:

| Email | Name | Grants |
|---|---|---|
| `owner@example.com` | Maren Holt | `owner`, every market |
| `editor@example.com` | Jonas Weber | `editor` on `fr`, `be-nl` and `be-fr`, plus a deny on `be-fr` |
| `editor2@example.com` | Priya Anand | `editor` on `de`, from Parallel Studio, expired one day before the app first started |
| `editor3@example.com` | Luca Moretti | none |
| `translator@example.com` | Sofia Brandt | `translator` on `de`, `it` and `es` |
| `legal@example.com` | Camille Roux | `legal` on `fr`, `en` and `be-nl` |
| `legal2@example.com` | Anke de Vries | `legal` on `de`, `it`, `es` and `be-fr` |
| `merchandiser@example.com` | Tomás Ibarra | `merchandiser`, every market |

## Core features

### Auth

Staff sign in with email and password, implemented by the app. `POST /api/v1/auth/login`
takes `email` and `password` and returns a bearer `token` plus the signed-in `principal` with
its `grants`. Every later call carries `Authorization: Bearer <token>`. A token expires 12 hours
after it is issued. `POST /api/v1/auth/logout` retires the token at once.

1. A wrong password and an unknown email are refused with the same message, `Sign-in failed`,
   so neither reveals whether the account exists.
2. Passwords are stored hashed. The literal `deku-demo-pw-2026` works at login for every seeded
   account and appears in no stored record.
3. A missing, unknown, retired or expired token is refused as unauthenticated and changes
   nothing.
4. There is no signup: a request to create an account is refused and creates no account.
5. The staff directory at `GET /api/v1/principals` answers only a signed-in `owner`; an
   anonymous request is refused as unauthenticated and lists nobody.
6. Signing in does not settle what a person may do. A grant is evaluated at the moment of each
   request, so a grant that expires while a token is still valid stops working on the very next
   request, and the token still authenticates.

### 1. The public drop page

`/afterglow/fr/` is the Afterglow page for France. A market's page exists only while that market
is **live** (it has a current published artifact); for a market that is not live the page
answers as not found.

1. The page is one document in the market's language: the root element's `lang` is the market's
   `hreflang`, there is exactly one `h1` and it carries the `hero.title` string, and the
   landmarks are a banner, a navigation, a main region and a content footer.
2. Sections appear in the campaign's order. For Afterglow: hero, tagline, collage, collection,
   artist, story, lookbook, the footer list and the legal footer. Four sections carry anchors,
   `collection`, `ardenne`, `rx2k` and `lookbook`, each a section element whose accessible name
   is its heading.
3. A fixed bar, the page's `header` element and its banner, holds three zones: the menu button at the left, the Halden Sport wordmark in the
   centre, and the language switcher followed by the shop action at the right. The bar never
   hides, shrinks or inverts on scroll.
4. The menu button opens a full-viewport overlay listing the four anchors by their headings.
   The button carries `aria-expanded` reflecting its state and `aria-controls` naming the
   overlay. Opening moves focus to the first item; `Escape` closes it and returns focus to the
   button; while it is open the page behind it cannot be
   reached: the content behind it is inert, or the overlay is a native modal dialog. Choosing an item closes the overlay
   and then moves to that section, and focus lands on the section. The button's label is the
   market's `menu.label` while closed and `menu.close` while open. The section in view is marked
   `aria-current="location"` in the menu list.
5. Every decorative sticker (the bolts, arcs, discs, stars and triangle) is marked
   `data-sticker`, `aria-hidden="true"` and `focusable="false"`, and is never announced.
6. The footer list repeats the market's products as full-width rows numbered `[01]`, `[02]` and
   onward with each price at the right.
7. The legal footer links the market's legal notice, the privacy page and the design credit to
   Parallel Studio.
8. With scripting turned off the page is still whole: every heading, every paragraph, every
   product link, every price and the language switcher are in the served document, and no
   content depends on an animation to become visible.
9. With reduced motion requested, no piece of content is left invisible or off to one side: every
   scroll-driven reveal is already at its end state.
10. `/afterglow/fr/mentions-legales/` is the French legal notice, carrying `legal.title` as its
    heading and `legal.body` as its text. Each market's legal notice lives under that market's own
    slug, and any other slug under that market answers as not found.
11. `/` lists every campaign with at least one live market, linking to `/{campaign}/`. With both
    seeded campaigns as they are at first start, it lists Afterglow only.

### 2. Locales, the language switcher and discovery

Seven markets exist, and a market is data, not code: adding one is a row, not a deploy. This locale
matrix drives every route, link and price, which is also what search engines see (the SEO and
discovery rules below).

| Market | `hreflang` | Name in its own language | Currency | Storefront host | Locale segment | Legal slug |
|---|---|---|---|---|---|---|
| `fr` | `fr-FR` | Français | `EUR` | `shop-fr.example.com` | none | `mentions-legales` |
| `en` | `en` | English | `GBP` | `shop-uk.example.com` | none | `legal-notice` |
| `it` | `it` | Italiano | `EUR` | `shop-it.example.com` | none | `note-legali` |
| `es` | `es` | Español | `EUR` | `shop-es.example.com` | `/es` | `aviso-legal` |
| `de` | `de` | Deutsch | `EUR` | `shop-de.example.com` | none | `impressum` |
| `be-nl` | `nl` | Nederlands (België) | `EUR` | `shop-be.example.com` | `/nl` | `wettelijke-vermeldingen` |
| `be-fr` | `fr-BE` | Français (Belgique) | `EUR` | `shop-be.example.com` | `/fr` | `mentions-legales` |

1. `/afterglow/` never renders a page. It redirects temporarily (never permanently) to one live
   market, chosen in this order: the market named by the `drop_lang` cookie when that market is
   live; a live market whose `hreflang` equals a tag in `Accept-Language`; a live market whose
   `hreflang` shares the primary language of a tag, in the table's order; the campaign's default
   locale when live; the first live market in the table's order. A campaign with no live market
   answers as not found.
2. The language switcher is a native select with a `label` element tied to it, reading the market's
   `lang.label`. It lists only live markets, each option written as the market's name
   in its own language with a `lang` attribute equal to that market's `hreflang`, and each option
   leads to **the same document** in that market, its value being `/lang?to=` followed by that
   document's path: from `/afterglow/fr/mentions-legales/` the
   English option leads to `/afterglow/en/legal-notice/`, not to the English home page.
3. Choosing a language goes through `/lang?to=<path>`, which sets the cookie `drop_lang` to the
   chosen market (path `/`, kept for 365 days, which is a max age of `31536000` seconds, same-site
   lax) and redirects to that path. The
   switcher works with scripting off. A `to` that is not a path to a live document on this site,
   including any address on another host, is refused and sets no cookie.
4. Every live market page and legal page declares an alternate link for every live market of the
   campaign, including itself, plus `x-default` pointing at `/afterglow/`, and a canonical link
   to itself. Alternates are reciprocal: if France lists England, England lists France.
5. Every public route has its own title and its own meta description, and no two routes share
   either. A drop page takes `meta.title` and `meta.description`; its legal notice takes
   `legal.title` joined with the campaign name, and a description drawn from `legal.body`.
6. `/sitemap.xml` lists `/`, `/privacy/`, and every live market page and its legal notice, and
   nothing that is not live. `/robots.txt` names the sitemap and disallows `/studio/` and `/api/`.

### 3. Product cards, link derivation and the storefront hand-off

The collection section holds one card per product that is **available** in the market, three
across on the wide layout and two across below it. A card is marked `data-product` with the
commerce product id, and shows a swipeable slide per colourway, the product's name, the price,
and one swatch per colourway.

1. **A storefront link is derived, never stored**, replacing the hand-typed behaviour that let
   links drift. For a product, a colourway and a market it is
   `https://` then the market's host, then its locale segment, then `/p/*/_/R-p-` and the commerce
   product id, then the query `mc` = the model code, `hscamp` = the attribution value, and
   `type` = `hscamp`, with query values percent-encoded and the asterisk in the path literal.
   The attribution value is the campaign's prefix, then its attribution slug, then `_` and the
   colourway's slot. Worked examples for the Afterglow graphic tee in pink (product `482913`,
   model `7310042`, slot `p1`), shown decoded:

   | Market | Link |
   |---|---|
   | `fr` | `https://shop-fr.example.com/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` |
   | `es` | `https://shop-es.example.com/es/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` |
   | `be-nl` | `https://shop-be.example.com/nl/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` |

2. Every market carries attribution, or none does: there is no market whose links lack the
   `hscamp` and `type` parameters.
3. The shop action in the bar leads to the market's collection page for the campaign:
   `https://` then host, segment, `/c/` and the campaign slug, with `hscamp` =
   `hscamp:__drop-afterglow` and `type` = `hscamp`. It is labelled with the market's `shop.cta`.
4. Each colourway's own link is marked `data-colourway` with its model code; the card title
   links to the selected colourway too, so clicking the photograph and clicking the name go to
   the same place.
5. Every link that opens in a new tab, including the shop action, the wordmark and the design
   credit, carries `rel="noopener noreferrer"`. Every storefront link, the shop action and the design
   credit also carry the market's `newtab.suffix` as text read by assistive technology only; the
   wordmark instead carries the `aria-label` `Halden Sport`.
6. Swatches are buttons, each marked `data-swatch` with its model code, carrying `aria-pressed`,
   and named by the colour's name in the market's language (`Blanc` in France, `White` in the
   United Kingdom). Activating one by click, `Enter` or `Space` selects that colourway, and the
   arrow keys move between a card's swatches. Exactly one swatch per card is pressed. Each
   swatch looks small but offers a hit area of at least 44 by 44 CSS pixels around its centre.
7. A product that is not available in the market has no card and no footer row: it is absent,
   not greyed out and not a dead link. Track pants are not available in `en`.
8. A price is the market's own, in the market's currency, formatted from integer minor units at
   render: `2000` `EUR` reads `20,00 €` in `fr`, `it`, `es`, `de` and `be-fr` and `€ 20,00` in
   `be-nl`; `1700` `GBP` reads `£17.00` in `en`. The price element is marked `data-price`. A
   product with no price for the market renders its card with no price rather than another
   market's price.
9. The platform stores no product photography. Each colourway's slide is a panel painted in
   that colourway's swatch colour at a fixed portrait proportion, marked `data-slide` with its model
   code, with the colour carried as data on the element rather than as a class, so a new colourway needs no stylesheet change. The grid
   never shifts while the page settles.

### 4. Products, prices and attribution slots

A product belongs to one campaign and carries a global, merchandiser-owned `commerce_product_id`;
each colourway carries a global `model_code`, a `swatch_hex` and an attribution slot. Availability and price
belong to a product in one market. Afterglow's products:

| Order | Product | Name (`fr` / `en`) | Colourways: model code, slot, name (`fr` / `en`) |
|---|---|---|---|
| 1 | `482913` | T-shirt graphique / Graphic tee | `7310042` `p1` Rose / Pink; `7310043` `p2` Blanc / White |
| 2 | `482927` | Veste de survêtement / Track jacket | `7310118` `p3` Pervenche / Periwinkle; `7310119` `p4` Blanc cassé / Off white |
| 3 | `482940` | Pantalon de survêtement / Track pants | `7310205` `p5` Pervenche / Periwinkle |
| 4 | `482956` | RX2K / RX2K | `7310377` `p6` Sarcelle profonde / Deep teal; `7310378` `p7` Blanc / White |

In every euro market all four are available at `2000`, `4500`, `3500` and `9000` `EUR`. In `en`
the graphic tee is `1700` `GBP`, the track jacket `3900` `GBP` and the RX2K `7900` `GBP`; the
track pants are not available there and have no price. Dusk Parade has one product, `483101`,
with one colourway `7311550` in slot `p1`, available in `be-nl` and `de` at `6500` `EUR` and
nowhere else.

1. The validation rules: a `commerce_product_id` is 4 to 10 digits and unique within its campaign; a `model_code` is 6
   to 10 digits and unique within its product; a `swatch_hex` is `#` followed by six hexadecimal
   digits. Anything else is rejected as invalid, naming the field, and nothing is stored. A
   repeated identifier is refused with `duplicate`.
2. **Slots are assigned by the server, never typed.** A new colourway takes `p` followed by one
   more than the highest slot number already used in its campaign, so a new Afterglow colourway
   takes `p8`. A slot is unique within its campaign and stable for the life of the campaign:
   reassigning one would silently merge two colourways' historical conversion data. A request that sends a
   slot is refused with `field_not_permitted`.
3. Creating a product also creates its `product.<id>.name` string and one
   `colour.<model_code>.name` string per colourway, with no translations yet.
4. `price_minor` is a whole number greater than zero and below `100000000`, in minor units.
   `20.00`, `"2000"` and `0` are rejected as invalid.
5. **A price's currency always equals its market's currency.** Setting the graphic tee's `en`
   price to `1700` `EUR` is refused with `currency_mismatch` and the stored price stays `1700`
   `GBP`. A price sent without a currency is rejected as invalid.
6. Product identity, colourways and prices are `merchandiser` fields. Anyone else writing one is
   refused with `field_not_permitted`. An `owner`, or an `editor` in a market its grants cover, may
   change `available` alone.
7. No storefront address is accepted or stored anywhere: a body carrying a `url` field is refused
   with `field_not_permitted`.

### 5. Grants and refusals

Every refusal answers with a JSON body carrying `title`, a stable `reason` and the `request_id`,
plus `fields` naming each bad field when the body itself was invalid. A request is authenticated
first, then its body is validated, then it is authorized, and only then applied. The reasons are
a closed set. Silent denial is a defect, because a refusal with no reason is indistinguishable
from a bug to the person it happens to, so every deny is logged with its reason:

| `reason` | When |
|---|---|
| `not_authenticated` | no valid token |
| `role_not_permitted` | none of the principal's roles may take this action |
| `market_out_of_scope` | a role allows it, but no grant covers this market |
| `grant_expired` | the only covering grant has passed its expiry |
| `explicit_deny` | a deny grant covers this market; a deny always wins over a permit |
| `field_not_permitted` | the body writes a field outside the role's writable set |
| `role_not_grantable` | a grant was requested for `owner`, `legal` or `merchandiser` |
| `invalid` | the body or the request is malformed |
| `duplicate` | the identifier, key or slug already exists |
| `currency_mismatch` | a price's currency differs from its market's |
| `translations_incomplete` | a submit found a key not `reviewed` or `approved` |
| `price_missing` | a submit found an available product with no price |
| `untranslated_copy` | a translation repeats the default locale's text in another language |
| `machine_legal_text` | legal text was sent with the status `machine` |
| `approvals_incomplete` | a publish lacked a current legal or owner approval |
| `embargo_pending` | a publish came before the campaign's embargo time |
| `not_live` | an unpublish targeted a market that is not live |
| `nothing_to_roll_back` | a rollback found no earlier artifact |
| `stale_version` | `If-Match` no longer matches the market |
| `precondition_required` | a market change came without `If-Match` |
| `unsupported_media` | an upload is not a PNG, JPEG or WebP image |

1. **Market scope.** `editor@example.com` writing a translation in `de` is refused with
   `market_out_of_scope` and the translation is unchanged.
2. **Expiry is checked at decision time.** `editor2@example.com` signs in successfully and every
   write in `de` is refused with `grant_expired`.
3. **A deny wins.** `editor@example.com` holds a permit and a deny on `be-fr`; every write there
   is refused with `explicit_deny`.
4. **Fields.** `translator@example.com` writing a price, a model code, a swatch or availability is
   refused with `field_not_permitted`.
5. **Roles.** `merchandiser@example.com` submitting, approving or publishing a market is refused
   with `role_not_permitted`.
6. **Reads.** A market page, market record, translation list, render or preview for a market the
   principal holds no grant for answers as not found, so a stranger cannot learn its state.
7. **Owner-issued grants.** `POST /api/v1/grants` takes `email`, `role` (`editor` or
   `translator`), `market_code`, `expires_at` and `reason`. An expiry is required, must be in the
   future and no more than 90 days away, and a reason is required; otherwise the grant is rejected
   as invalid. A grant for another role is refused with `role_not_grantable`. A new grant works on
   the grantee's very next request without signing in again. `DELETE /api/v1/grants/{id}`
   revokes one, and the grantee's next request in that market is refused.
8. A grant that expires between two requests on the same token: the first write succeeds, the
   second is refused with `grant_expired`, and `GET /api/v1/me` still answers for that token.

### 6. Translations

Every piece of copy is a keyed string of a campaign with a translation per market. Afterglow has
thirty strings: `meta.title`, `meta.description`, `hero.title`, `tagline.one`,
`collage.headline`, `collection.heading`, `artist.heading`, `artist.bio`, `story.heading`,
`story.body`, `lookbook.heading`, `lookbook.alt`, `menu.label`, `menu.close`, `shop.cta`,
`lang.label`, `newtab.suffix`, `legal.title`, `legal.body`, four product names and seven colour
names. Dusk Parade has thirteen. A translation's status is one of `machine`, `draft`, `reviewed`
and `approved`; a string with no translation in a market is missing there.

1. A translation's value is required and no longer than the string's `max_length` when one is
   set; a longer value is rejected as invalid, naming `value`.
2. **No untranslated copy.** In a market whose language differs from the campaign default
   locale's language, a value that contains the default locale's value for that key word for
   word, where that default value is 20 characters or longer, is refused with `untranslated_copy`.
   Short labels such as `Menu` are exempt, and so is `be-fr`, whose language is the default's own.
3. **Legal text is never machine translated.** `legal.body` or `legal.title` sent with the status
   `machine` is refused with `machine_legal_text`.
4. **A source edit re-queues every other market.** Changing a key's value in the campaign's
   default locale moves that key's translation in every other market from `reviewed` or
   `approved` to `draft`, and returns every other market that was `in_review`, `approved`,
   `published` or `unpublished` to `draft` with its approvals superseded. A live market stays live
   on its current artifact.
5. A translation status change alone never changes a market's content.
6. A new campaign starts with eleven strings: `meta.title`, `meta.description`, `hero.title`,
   `collection.heading`, `menu.label`, `menu.close`, `shop.cta`, `lang.label`, `newtab.suffix`,
   `legal.title` and `legal.body`, none of them with a length budget, its seven markets as `draft`,
   and the sections `hero`, `collection` (anchor `collection`), `footer_list` and `legal_footer`.
7. The studio preview of a market shows a missing string in the default locale's value and marks
   the element `data-untranslated` with the key, and carries `<meta name="robots" content="noindex">`.
   A live page never falls back to another language.

### 7. Review, approval and publication, one market at a time

A campaign market's `status` is one of `draft`, `in_review`, `approved`, `published` and
`unpublished`. Separately, a market is **live** while it has a current artifact. Afterglow at first
start:

| Market | Status | Live | Current approvals | Translations |
|---|---|---|---|---|
| `fr` | `published` | version 1 | legal and owner | all `approved` |
| `en` | `published` | version 1 | legal and owner | all `approved` |
| `it` | `approved` | no | legal and owner | all `reviewed` |
| `de` | `in_review` | no | legal only | all `reviewed` |
| `es` | `draft` | no | none | `legal.body` and `story.body` missing, `artist.bio` `machine`, the rest `draft` |
| `be-nl` | `draft` | no | none | all `reviewed` |
| `be-fr` | `unpublished` | no, version 1 exists | legal and owner | all `approved` |

Every Dusk Parade market is `draft` with no approvals; its translations are complete and
`reviewed` in `be-nl` and `de` and missing elsewhere.

1. **Content hash.** A market's `content_hash` is 64 lowercase hexadecimal characters computed
   over that market's translation values, that market's availability and prices, the campaign's
   products, colourways, slots and swatches, the campaign's attribution prefix and slug, the page
   sections, and the market's hero image and product order. It changes when any of those change and
   for no other reason; a change in another market never changes it.
2. **Submit.** `POST .../submit` moves a `draft` market to `in_review`, for the `owner`, or an
   `editor` or `translator` whose grant covers the market. It is refused with
   `translations_incomplete` (and a `keys` list) while any string is missing or not `reviewed` or
   `approved` there, and with `price_missing` (and a `products` list) while an available product
   has no price there. Afterglow `es` cannot be submitted; Afterglow `be-nl` can. A market that is
   not `draft` cannot be submitted and the attempt is rejected as invalid.
3. **Approvals bind to content.** `POST .../approvals` takes `kind` (`legal` or `owner`),
   `decision` (`approved` or `rejected`) and an optional `comment`, only while the market is
   `in_review`. A `legal` approval needs a legal grant covering the market; `legal@example.com`
   approving `de` is refused with `market_out_of_scope`. An `owner` approval needs the owner, and
   recording the approval kind of another role is refused with `role_not_permitted`. Each approval records the market's `content_hash` at that moment. When a current legal approval and
   a current owner approval both exist for the present hash, the market becomes `approved`. A
   rejection returns it to `draft`.
4. **An edit withdraws approval.** Any write that changes a market's content hash while it is
   `in_review`, `approved`, `published` or `unpublished` returns it to `draft` and marks every one
   of its approvals `superseded`.
5. **Markets are independent.** Submitting, approving, publishing, unpublishing or editing one
   market leaves every other market's status, approvals, content hash and live artifact exactly as
   they were. Approving France never publishes Germany.
6. **Publish.** `POST .../publish` is the owner's. It requires the market to be `approved`, or
   `unpublished` with both approvals still current for its hash; otherwise it is refused with
   `approvals_incomplete`. Before a campaign's `embargo_at` it is refused with `embargo_pending`.
   It writes the next artifact version, sets the market `published` and makes that version live.
7. **Publishing once.** A publish that carries an `Idempotency-Key` header already used by the same
   principal on the same market within 24 hours returns the first response again, writes no second
   version and records no second publish.
8. **Unpublish is always easy.** `POST .../unpublish` by the owner, or a legal reviewer whose grant
   covers the market, needs no approval and takes effect at once: the market becomes
   `unpublished`, stops being live, and its page answers as not found on the next request. A market
   that is not live is refused with `not_live`.
9. **Rollback**, the resilience control that bounds what a bad publish costs. `POST .../rollback`
   by the owner makes the highest earlier artifact version live
   and leaves the status as it is; with no earlier version it is refused with
   `nothing_to_roll_back`.
10. **The live page is the artifact.** Once published, a market's public page shows what that
    artifact holds. An edit made afterwards does not reach the public page until the market is
    approved and published again.
11. **No lost update.** Reading a market returns an `ETag`. `PATCH` of a market (its
    `hero_asset_id`, and its `product_order`, an array of the campaign's `commerce_product_id`
    strings; a partial list puts those products first and the rest follow in their own order, and an
    empty list restores the campaign order, which is the products' `sort_order`) must carry `If-Match`: without it the change is refused
    with `precondition_required`, and with a value that no longer matches it is refused with
    `stale_version`. Either way nothing is written. Two editors saving from the same read: the
    first save lands, the second is refused.

### 8. Images and artifacts in the object store

1. `POST /api/v1/campaigns/{slug}/assets` takes a multipart `file` and an optional `market_code`
   (absent means shared). The type is decided by the bytes, not the file name: only PNG, JPEG and
   WebP are accepted, anything else is refused with `unsupported_media`, and a file over 5 MB is
   rejected as invalid. A market image needs the owner or an editor whose grant covers the market;
   a shared image needs the owner.
2. **The bytes live in the object store and nowhere else.** An image is stored at
   `assets/{campaign_slug}/{market_code or shared}/{sha256 of the bytes}.{png, jpg or webp}`, for
   example `assets/afterglow/fr/9c1d...4e.png`. The response carries `id`, `object_key`,
   `checksum` (that sha256 in lowercase hex), `byte_size`, `content_type` and `market_code`. The
   same bytes uploaded again for the same market return the same asset and store no second object.
3. **The bucket is private.** An object requested from the store without its credentials is
   refused.
4. **An image of a market that is not live is not public.** `/media/{id}` serves a market image
   only while that market is live and a shared image only while the campaign has a live market,
   with the stored bytes unchanged and the stored content type. Otherwise it answers as not found,
   and it answers as not found again the moment the market is unpublished.
5. A market's `hero_asset_id` must name an image of the same campaign that is shared or belongs to
   that market; anything else is rejected as invalid.
6. **Artifacts.** Each publish stores the market's render payload, in the shape given under the API
   shapes, as JSON at
   `artifacts/{campaign_slug}/{market_code}/{version}.json`, for example
   `artifacts/afterglow/fr/1.json`, and the market's artifact list names each version with its
   `object_key`, `content_hash`, `published_by`, `published_at` and whether it is live.

### 9. The audit log

1. **Everything lands.** Every successful write records exactly one event with `decision`
   `permit`, and every refused write by a signed-in principal records exactly one event with
   `decision` `deny` and its `reason`. An event carries `id`, `occurred_at`, `actor_email`,
   `action`, `resource_type`, `resource_id`, `campaign_slug`, `market_code`, `decision`,
   `reason`, `request_id`, `before`, `after`, `prev_hash` and `hash`.
2. The actions are `campaign.create`, `campaign.update`, `string.create`, `translation.write`,
   `product.create`, `product.update`, `colourway.create`, `price.write`, `market.update`,
   `asset.upload`, `market.submit`, `approval.record`, `market.publish`, `market.unpublish`,
   `market.rollback`, `grant.create`, `grant.revoke` and `audit.export`.
3. Every response carries an `X-Request-Id` header, and every event a request produced carries
   that same value as its `request_id`.
4. **The chain.** The first event's `prev_hash` is sixty-four zeros. Every later event's
   `prev_hash` equals the previous event's `hash`. An event's `hash` is the lowercase hex sha256 of
   its `prev_hash` followed by the event's own fields as JSON with sorted keys and no whitespace.
5. **Append-only at the database.** An update or a delete of an audit row issued with the app's
   own database credentials is refused by the database itself, whatever code sends it.
6. `GET /api/v1/audit` returns events newest first, narrowed by `market`, `actor`, `action`,
   `decision` and `limit`. The owner reads every event; a legal reviewer reads only events in the
   markets its grants cover; anyone else is refused with `role_not_permitted`.
7. `GET /api/v1/audit/verify`, for the owner, walks the whole chain and returns `intact`,
   `events`, `head` (the last hash) and `first_broken_id`. When a row has been altered outside the
   app, `intact` is false and `first_broken_id` names the earliest event whose hash no longer
   holds.
8. `POST /api/v1/audit/exports`, for the owner, returns the log as CSV with a header row, and the
   export itself is recorded as `audit.export`.
9. No event carries a password, a token or a password hash.

### 10. The site's own pages

1. **Privacy.** `/privacy/` is linked from the footer of every public page and carries the personal
   data inventory, which is where the site's compliance and data governance are stated in plain
   words: what the site records about a visitor and for how long, and why. The address a request came
   from is kept in server logs for security and abuse prevention, on legitimate interest, for 30 days; the `drop_lang` language preference cookie, for 365 days; and staff audit records,
   for 7 years. It states that there is no visitor account, no analytics, no advertising and no
   third parties receiving anything, so an erasure request has nothing about a visitor to erase, and
   it names each market's data residency region: `eu-west`, `uk-south` and `eu-central`.
2. **Studio forms.** Every studio form rejects invalid input inline: the offending field is marked
   `aria-invalid="true"` with a message beside it naming the field, the refusal also appears as a
   toast, and nothing is written.
3. **Narrow viewport.** At a phone's narrow viewport no public or studio page scrolls sideways, and
   every navigation target stays reachable: the menu button, the language switcher and the shop
   action on a drop page, and every top navigation link in the studio, each visible
   without opening anything first.
4. **One primary action per page.** A drop page leads with its shop action; a studio market page
   leads with the next step its status allows (submit, approve or publish); every other action on
   those pages is visibly secondary.
5. **No third-party requests.** A public page loads nothing from any other host: its typeface,
   styles, scripts and images all come from this site.

## User flow

The information architecture is small and deep rather than wide: a public page is one very long
document plus its legal notice, and the studio is a handful of screens.

| Route | Purpose | Auth |
|---|---|---|
| `/` | campaigns with a live market | none |
| `/{campaign}/` | redirects to the chosen live market | none |
| `/{campaign}/{market}/` | the drop page of a live market | none |
| `/{campaign}/{market}/{legal_slug}/` | that market's legal notice | none |
| `/privacy/` | the privacy page | none |
| `/lang` | sets the language preference, then redirects to `to` | none |
| `/media/{id}` | a live image | none |
| `/sitemap.xml` | the sitemap | none |
| `/robots.txt` | the robots file | none |
| `/studio/login` | staff sign-in | none |
| `/studio/` | the campaign list beside the selected campaign's markets | staff |
| `/studio/campaigns/{campaign}/` | the same, with that campaign selected | staff |
| `/studio/campaigns/{campaign}/markets/{market}/` | one market: status, approvals, the primary next step, translations, availability and prices | staff with a grant covering the market |
| `/studio/campaigns/{campaign}/markets/{market}/preview/` | the market rendered from its current content | staff with a grant covering the market |
| `/studio/campaigns/{campaign}/products/` | products and colourways | staff |
| `/studio/audit/` | the audit log, its filters and the chain's state | `owner`, `legal` |
| `/studio/grants/` | grants, with issue and revoke | `owner` |

### Entry and redirects

Every page route above ends in a slash; the same address without it answers with a permanent
redirect to the slash form. `/lang`, `/media/{id}`, `/sitemap.xml`, `/robots.txt` and
`/studio/login` take no slash.

A visitor needs no account for anything public, and a visitor who asks for a campaign root is
sent to a live market by the order in core feature 2. A market that is not live, an unknown
campaign and a legal slug that is not the market's own answer as not found.

Anyone not signed in who asks for a studio page is sent to `/studio/login?next=<that path>` and,
after signing in, lands on that path. Signing out retires the token and lands on the sign-in page.
A token that expires mid-action sends the next studio request to the sign-in page with `next` set
to where the person was. A staff member asking for a market page their grants do not cover gets
the not-found page rather than a redirect, so the market's state is not disclosed.

### Journeys

1. **Arrive in English.** With an English browser, open `/afterglow/`. Arrive at
   `/afterglow/en/`, whose heading reads `Afterglow, the Halden Sport x Tove Ardenne capsule
   collection`. Open the menu; the button reports it is expanded. Choose `The collection`; the menu
   closes and the collection section is in view. The track pants are absent. The graphic tee card
   offers `Pink` and `White`; choose `White`, and the card's link now carries `mc=7310043` and the
   attribution value `hscamp:__drop-afterglow_p2`. The prices read `£17.00`, `£39.00` and
   `£79.00`.
2. **Keep your place.** Open `/afterglow/fr/mentions-legales/` and choose `English` in the
   switcher. Arrive at `/afterglow/en/legal-notice/`. Open `/afterglow/` again, this time with a
   French browser, and arrive at `/afterglow/en/` because the choice was remembered.
3. **Clear and publish one market.** Sign in as `editor@example.com`, open Dusk Parade `be-nl` and
   submit it; a toast confirms and the status reads `in_review`. Sign in as `legal@example.com` and
   approve it as legal. Sign in as `owner@example.com`, approve it as owner (the status reads
   `approved`) and publish it; the status reads `published` and version 1 is live.
   `/dusk-parade/be-nl/` now shows `Dusk Parade, lopen na zonsondergang`, while `/dusk-parade/de/`
   still answers as not found. The owner unpublishes it and `/dusk-parade/be-nl/` answers as not
   found again.
4. **Meet a deny.** Signed in as `editor@example.com`, open Afterglow `be-fr` and change a
   translation. A toast names `explicit_deny` and the row keeps its value.
5. **Let the agency in.** Signed in as `owner@example.com`, open `/studio/grants/` and add a row:
   `editor3@example.com`, `editor`, market `it`, expiring seven days from now, reason `Lookbook
   retouch`. The row appears in place with its expiry. Leaving the reason empty instead marks the
   reason field invalid and adds nothing.
6. **A pound is not a euro.** Signed in as `merchandiser@example.com`, open the Afterglow products
   and set the graphic tee's `en` price to `1700` with the currency `EUR`. The row marks the
   currency invalid, a toast names `currency_mismatch`, and the stored price is still `1700` `GBP`.
7. **Read the log.** Signed in as `owner@example.com`, open `/studio/audit/`, narrow it to market
   `be-nl`, and read the Dusk Parade submit, both approvals, the publish and the unpublish, each
   with its actor, time and hash. The chain reads intact.

### States

Every studio list has an empty state that says what would appear there. Every studio action shows
a busy state on its own trigger while it runs and ends in a toast: a success toast naming what
changed, or a refusal toast naming the `reason`. A refusal never leaves a half-changed row on
screen, and no error shows a stack trace. The public page never waits behind a loading screen for
more than three seconds and shows none at all with scripting off. A campaign index with no live
campaign says so. A preview with missing strings marks each one rather than showing a key or an
empty space.

## UI/UX notes

The public page is a consumer, editorial surface for a youth-nostalgia capsule and may carry
atmosphere; the studio is an operational tool and reads quiet, dense and built for repeated work.
They share one palette and one typography and nothing else. North star for the page: the collection
reads as a loud revival of the late nineties, and the product and its price are never harder to
find than the stickers around them. North star for the studio: at a glance, what state is this
market in and what is the one thing to do next.

**Colour.** The page is a Memphis-revival scheme: loud on purpose, with black outlines holding it
together. The default ground is a near-white neutral with a faint green cast; the collection
section sits on a near-white neutral with a pink cast; the tagline and collage passage and the story
sit on a light, muted magenta; the hero itself sits on the default ground. Type, outlines and sticker keylines are near-black neutral; the
product ground and one swatch are near-white neutral. The brand acid is a light, vivid amber and
is the colour of the primary action, the wordmark fill and some sticker fills; nothing else that
a visitor can press wears it. A deep, vivid teal is the accent; a light, vivid orange and a light,
soft cyan are sticker fills only and never carry text; a light, muted red is a second accent; a
deep neutral carries studio text; the overlay menu alone sits on a light, muted teal. A swatch's
colour is data, and the page paints it exactly as stored. In the studio, failure is the muted red
with a near-black keyline, success is the deep teal, in progress is the acid amber, and every
status chip also spells its status word, so colour is never the only signal. The exact shades are
yours within those relationships.

**Type.** One family, `Roboto Flex`, as a single variable font served by the app, with a
metric-matched fallback so a late font never moves a line. Display product names in the footer
list run full-bleed in a heavy condensed cut at about a quarter of the viewport height. The page
heading is `48px` on a `52px` line on the wide layout and `32px` on `36px` below it; section
headings are `64px` on `64px` wide and `36px` on `40px` below; card titles `20px` on `24px`; body
`16px` on `24px`; uppercase labels `12px` on `16px`; studio tables `14px` on `20px`. Headings
balance their lines. Prices align on their figures wherever they stack.

**Shape and density.** Hard black keylines and flat fills rather than shadows on the page; stickers
and cards may tilt, text never does. The studio is compact: rows sit tight so a whole market's
translations fit a screen, and position never shifts between visits.

**Motion.** Movement is attached to the reader's scroll, not to a clock. The page arrives at a
scroll position a beat after the input, so it feels carried rather than snapped. The hero image
starts as a small portrait window in the middle of a coloured field and opens outward exactly as far
as the reader has scrolled. Stickers fly up from well below the fold, some spinning a quarter turn
as they land. The tagline is stored as a sentence and only split into letters once the page runs,
then revealed letter by letter. In the collage two photographs travel across a giant headline on
opposite diagonals, hiding and revealing it. Cards arrive in a short cascade on the wide layout and
all at once on a narrow one, because a cascade reads as lag when several cards are visible. The
footer list replays row by row. Interface feedback is quick; content reveals take longer. Every movement draws from one small
easing catalogue of eased-in, eased-out and eased-both-ways curves, so nothing moves with a character
of its own. Only
position, opacity and clipping animate, never layout. In the studio a toast slides in from the top
right and fades out; nothing else moves. With reduced motion requested, the carried scroll is off,
every reveal sits at its end state, sliders never advance on their own, and only short fades
remain, so no content is ever hidden by switching motion off.

**Accessibility.** Every text and ground pairing meets WCAG 2.2 AA contrast for its size, and the
pairings to watch are any non-black text on the orange or the cyan fills, which is why those fills
never carry text. Keyboard navigation reaches every control in order with a visible focus ring
distinct from hover, on every ground including the menu's teal. Every swatch, the menu button and
every icon-only control has a name. Nothing flashes more than three times a second. Focus is never
left on something the scroll has carried off screen.

**Responsive.** Below the wide layout the collection goes two across, the menu button keeps its
icon and drops its word, the shop action leaves the bar and floats near the bottom of the viewport
where a thumb rests, swatches become small circles beside the product name, and the menu list
becomes a single column. The layout holds at every width from a small phone to a very wide screen,
and in landscape on a phone it is not a squeezed desktop layout. There is no horizontal overflow at
any width: every decorative sticker is clipped by its own section. The studio's list pane stacks
above the detail pane on a narrow viewport. Every breakpoint is a rearrangement and none removes a
control. Hover-only effects apply only where the pointer can hover, and every hover effect has a
focus equivalent.

**Mode.** Light only. There is no dark scheme.

## Front-end specification

### The drop page, section by section

| Section | Ground | Content | Motion |
|---|---|---|---|
| Hero | default ground | the hero image in its opening window; four stickers at the corners (a pink arc, an orange speckled disc, an amber bolt, a cyan arc) and a teal triangle bleeding off the top right | the window opens with scroll; stickers drift |
| Tagline | default ground passing into the muted magenta | `tagline.one` | letter-by-letter reveal |
| Collage | muted magenta | `collage.headline` behind two travelling photographs | the cross-traverse |
| Lines | muted magenta | a full-bleed band of decorative lines overlapping the next section | a held stage |
| Collection, `#collection` | pink-cast neutral | `collection.heading`, then the cards | per-card reveal in a cascade |
| Artist, `#ardenne` | default ground with an orange sun form | `artist.heading`, `artist.bio`, a portrait | stickers enter; the sun grows |
| Story, `#rx2k` | muted magenta | `story.heading`, `story.body`, line drawings of the shoe | paired parallax |
| Lookbook, `#lookbook` | mixed | `lookbook.heading` and the shared lookbook image with `lookbook.alt` as its alternative text | reveal on scroll |
| Footer list | default ground | every available product full-bleed, `[01]` onward at the left, price at the right | each row replays |
| Legal footer | default ground | the legal notice link, the privacy link, the design credit | none |

A campaign with fewer sections, like Dusk Parade, renders only its own.

### The fixed bar

The bar spans the full width but only its controls take the pointer, so the page behind it can be
scrolled and dragged anywhere else. At the left, the menu button: an icon with its word on the wide
layout, the icon alone below it. In the centre, the Halden Sport wordmark, filled with the acid amber
over a black outline shape, linking to `https://halden.example.com/` in a new tab with the
accessible name `Halden Sport`. At the right, the language switcher and then the shop action. Two
copies of the shop action exist in the document, one in the bar and one floating, each hidden at the
other's width. The bar stays legible over every ground; a section whose ground would fail against it
insets its own content rather than making the bar adapt.

### The product card

The card's structure: a card is a slider of colourway slides above a meta row. The meta row holds the title link across
two thirds, the price, and the swatch row aligned to the end. On the wide layout swatches are small
squares at the end of the row; below it they are small circles beside the title. States: resting
shows the first colourway with its swatch pressed; pointing at a swatch grows it; activating a swatch
moves the slider to that colourway; pointing at the card engages an overlay and draws an underline
under the title, and keyboard focus on the card's link does the same; focus rings are visible on the
link and on each swatch; swiping advances the slider on touch. A long name wraps to two lines on the
wide layout and three below it, never breaking mid-word, and the grid is laid out against the longest
language rather than the shortest.

### The overlay menu

A full-viewport overlay on the light, muted teal holding the four anchors as a grid, four across on
the wide layout and one column below it, each item carrying a strip of tape as decoration.

### The studio

A top navigation reading `Campaigns`, `Audit` and, for the owner only, `Grants`, with the signed-in
email and `Sign out` at the right. `/studio/` is a split view: the campaign list in a narrow pane at
the left, and the selected campaign's seven markets at the right, each with its status chip, whether
it is live, and its approvals. A market page leads with its status, its current approvals and the one
primary next step, then a translations table (key, value, status) whose rows are edited in place,
then an availability and price table, then the artifact list with rollback. New strings, products,
colourways and grants are added as a new row inside their own table, not in a dialog or on another
page, started by a button labelled `Add` and kept with a button labelled `Save`. Every outcome is a
toast at the top right. The sign-in form's fields are labelled `Email` and
`Password`, and its button reads `Sign in`; a studio form always submits and the server's refusal marks the
field, rather than the browser's own validation bubble standing in for it; a grant row's fields are labelled `Email`, `Role`, `Market`, `Expires` and `Reason`; a
price row's fields are labelled `Price` and `Currency`.

## Technical requirements

Build this as a **multi-page application rendered on the server with progressive enhancement**.
The backend is **Django 5** with Django templates and the Django ORM, served in production by
**gunicorn** with static files served by **WhiteNoise**. The frontend is **HTMX with server
templates**: every route answers with a complete HTML document produced on the server, and the
studio swaps server-rendered fragments into the page for inline rows, the detail pane and toasts.
The first paint a browser receives is the whole document; no page is an empty shell that fills
itself from a second request. The drop page's motion is a plain script layered on top of a
document that already reads correctly without it. The JSON API is served by the same Django
process under `/api`, on the same origin and port as the pages.

The database is **PostgreSQL**, read from `DATABASE_URL`, which the environment also exports as
`DB_URL` with the same value. Images and artifacts live in **MinIO**, an S3-compatible object
store, read from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`, and reached with **boto3**. The app's own address and port come from
`APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port. Both backing services are
**already running** at those variables and must not be downloaded, installed, compiled or started;
the bucket already exists and is private.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing services
available in this environment are PostgreSQL and MinIO, and reaching for anything else is a
contract violation.

**Authentication** is the app's own email and password with opaque bearer tokens, as described
under `### Auth`. Passwords are hashed with a slow, salted password hash. A token is stored only as
a hash of itself, so a copy of the database yields no usable token. The studio's pages use the
same sign-in and keep the token in a cookie that scripts cannot read; a studio page requested with
the bearer token in the `Authorization` header is served exactly as it is to that signed-in cookie.

**Authorization** is one decision point that every write passes through, not checks scattered
across views, and it returns permit or deny with a reason from the closed set in core feature 5.
The studio hides what a person may not do as a courtesy only.

`GET /api/health` returns `200` once the app can reach both PostgreSQL and the bucket.

**Observability.** Each request writes one JSON line to standard output carrying `request_id`, `method`,
`path` (without its query string), `status`, `elapsed_ms`, `principal_email` and `market_code`. No
log line carries a price, a token, a password or a query string.

**Request identity.** Every response carries an `X-Request-Id` header, generated when the request
did not bring one, and the same value appears on every audit event the request produced and in
every refusal body.

**Security headers on every response.** `X-Content-Type-Options: nosniff`, `Referrer-Policy:
strict-origin-when-cross-origin`, a `Permissions-Policy` that denies camera, microphone,
geolocation and payment, and a `Content-Security-Policy` whose script source list carries no
`unsafe-inline` and which sets `frame-ancestors 'none'`, `base-uri 'self'` and
`form-action 'self'`.

**Caching headers.** A live drop page and a legal notice answer with `Cache-Control: public,
max-age=60, stale-while-revalidate=86400, stale-if-error=604800` and `Vary: Accept-Encoding`, and
never vary on `Cookie`: nothing on them depends on the visitor. A campaign root answers its
temporary redirect with `Cache-Control: private, no-store` and `Vary: Accept-Language, Cookie`,
because it is a per-visitor decision and must never be stored.

**Nothing leaves the site at runtime.** No page and no server call reaches another host. The
typeface is served by the app itself: self-hosting the variable font removes the only third-party
runtime dependency, which is the compliance fix and the faster page at once, with one less DNS
lookup and connection on the critical path.

**Performance and scalability.** Every public response is a function of published content and the
market, never of the visitor, which is why the caching headers below can let a shared cache absorb a
launch-day spike.

**Idempotency.** Every `POST` accepts an `Idempotency-Key` header. A repeat of a key already used by
the same principal on the same endpoint within 24 hours returns the first response and does nothing
again.

**Money** is integer minor units plus an uppercase ISO 4217 code everywhere it is stored, returned
or compared; a displayed price is formatted from the minor units at render time.

**Time** is UTC everywhere, written as ISO 8601 with a `Z`.

**No secret reaches the browser.** No document, script, stylesheet or JSON the browser can fetch
carries the database address, the object store's keys or another person's token; the bucket is
only ever reached by the server.

**Seeding** runs when the app starts and is idempotent.

## Data model

Seventeen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not
a credential to protect. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

- **`markets`** - `code` (primary key), `hreflang`, `display_name`, `currency`, `locale_tag`,
  `commerce_host`, `commerce_locale_segment`, `legal_page_slug`, `data_region`, `sort_order`,
  `active`. Seven rows, exactly the table in core feature 2, with `locale_tag` `fr-FR`, `en-GB`,
  `it-IT`, `es-ES`, `de-DE`, `nl-BE` and `fr-BE` and `data_region` `eu-west`, `uk-south`,
  `eu-west`, `eu-west`, `eu-central`, `eu-west` and `eu-west` in that order. There is no URL
  column in this table or any other.
- **`principals`** - `id`, `email` (unique, lowercase), `display_name`, `password_hash`,
  `status` (`active` or `suspended`), `created_at`.
- **`sessions`** - `id`, `principal_id`, `token_hash` (unique), `issued_at`, `expires_at`,
  `revoked_at`.
- **`grants`** - `id`, `principal_id`, `role`, `market_code` (empty means every market),
  `effect` (`permit` or `deny`), `expires_at`, `granted_by`, `reason`, `created_at`,
  `revoked_at`.
- **`campaigns`** - `id`, `slug` (unique), `name`, `default_locale`, `attribution_prefix`,
  `attribution_slug`, `embargo_at`, `created_by`, `created_at`.
- **`campaign_markets`** - one row per campaign and market: `campaign_id`, `market_code`,
  `status`, `content_hash`, `live_version`, `hero_asset_id`, `product_order`, `published_at`,
  `published_by`, `updated_at`. Creating a campaign creates all seven rows as `draft`.
- **`page_sections`** - `id`, `campaign_id`, `kind` (`hero`, `tagline`, `collage`,
  `collection`, `artist`, `story`, `lookbook`, `footer_list` or `legal_footer`), `anchor`
  (unique within the campaign, lowercase letters, digits and hyphens), `sort_order`.
- **`products`** - `id`, `campaign_id`, `commerce_product_id` (unique within the campaign),
  `sort_order`, `created_at`.
- **`colourways`** - `id`, `product_id`, `model_code` (unique within the product), `swatch_hex`,
  `attribution_slot` (unique within the campaign), `sort_order`.
- **`product_markets`** - one row per product and market: `product_id`, `market_code`,
  `available`, `price_minor`, `price_currency`. A stored currency always equals the market's
  currency, and a price never exists without its currency.
- **`translatable_strings`** - `id`, `campaign_id`, `key` (unique within the campaign),
  `context`, `max_length`.
- **`translations`** - one row per string and market: `string_id`, `market_code`, `value`,
  `status`, `translated_by`, `updated_at`. No row means missing.
- **`assets`** - `id`, `campaign_id`, `kind` (`image`), `object_key` (unique), `content_type`,
  `byte_size`, `checksum`, `market_code` (empty means shared), `created_by`, `created_at`.
- **`approvals`** - `id`, `campaign_id`, `market_code`, `kind`, `decision`, `decided_by`,
  `decided_at`, `content_hash`, `superseded`, `comment`. There is never more than one current
  approval of a kind for a market and a content hash.
- **`published_artifacts`** - `id`, `campaign_id`, `market_code`, `version`, `object_key`,
  `content_hash`, `published_by`, `published_at`. Versions of a market count 1, 2, 3 and never
  repeat.
- **`audit_events`** - the fields in core feature 9. `id` is an integer that increases with every
  event, and the chain runs in `id` order. The database refuses an update or delete of
  this table issued with the application's own credentials.
- **`idempotency_keys`** - `key`, `principal_id`, `endpoint`, `status_code`, `response_body`,
  `created_at`; one row per key, principal and endpoint.

The governance entities are `principals`, `sessions`, `grants`, `approvals`, `published_artifacts`
and `audit_events`; `markets.data_region` records each market's residency. Derived rather than
stored: every storefront link, every displayed price, translation completeness
and the submit check. `content_hash` is stored for reading but always recomputed from the content on
write, never accepted from a caller.

### Seed data

Markets, accounts and grants are as tabled under core features 2 and `## User roles`.
`editor2@example.com`'s grant carries the reason `Parallel Studio design pass`.

**Afterglow** has the slug `afterglow`, the default locale `fr`, the attribution prefix
`hscamp:__drop-`, the attribution slug `afterglow` and no embargo. Its sections in order are
`hero`, `tagline`, `collage`, `collection` (anchor `collection`), `artist` (anchor `ardenne`),
`story` (anchor `rx2k`), `lookbook` (anchor `lookbook`), `footer_list` and `legal_footer`. Its
products, availability, prices and market states are tabled under core features 4 and 7. Its
swatches are a pale pink for `7310042`, white for `7310043` and `7310378`, a muted periwinkle blue
for `7310118` and `7310205`, an off white for `7310119` and a soft deep teal for `7310377`. Its
media inventory is PNG images: a hero image for each of the seven markets and four shared images (the lookbook
image and the two collage photographs and the artist portrait), all stored under their keys. The
`fr` and `en` markets each have artifact version 1 live, and `be-fr` has artifact version 1 stored
and not live.

**Afterglow copy, `fr` and `en`:**

| Key | `fr` | `en` |
|---|---|---|
| `meta.title` | Afterglow, la capsule Halden Sport x Tove Ardenne | Afterglow, the Halden Sport x Tove Ardenne capsule |
| `meta.description` | Quatre pièces rétro dessinées avec Tove Ardenne, en édition limitée. | Four retro pieces designed with Tove Ardenne, in a limited drop. |
| `hero.title` | Afterglow, la collection capsule Halden Sport x Tove Ardenne | Afterglow, the Halden Sport x Tove Ardenne capsule collection |
| `tagline.one` | À vos côtés depuis 1976 | Right beside you since 1976 |
| `collage.headline` | Plongez au cœur de la décennie la plus vibrante qui soit | Dive into the most vibrant decade there ever was |
| `collection.heading` | La collection | The collection |
| `artist.heading` | Salut, je suis Tove Ardenne | Hi, I am Tove Ardenne |
| `artist.bio` | Illustratrice née à Lyon, je dessine le sport comme un souvenir de cour de récréation. | An illustrator born in Lyon, I draw sport the way you remember a school playground. |
| `story.heading` | L'histoire de la RX2K | The RX2K story |
| `story.body` | Une chaussure de course de 1999, redessinée trait pour trait à partir de ses plans d'origine. | A 1999 running shoe, redrawn line for line from its original plans. |
| `lookbook.heading` | Lookbook | Lookbook |
| `lookbook.alt` | Deux coureurs en veste pervenche sur une piste au coucher du soleil | Two runners in periwinkle jackets on a track at sunset |
| `menu.label` | Menu | Menu |
| `menu.close` | Fermer | Close |
| `shop.cta` | Boutique | Shop |
| `lang.label` | Choisir la langue | Choose language |
| `newtab.suffix` | ouvre la boutique dans un nouvel onglet | opens the shop in a new tab |
| `legal.title` | Mentions légales | Legal notice |
| `legal.body` | Ce site est édité par Halden Sport SA, 12 rue des Tanneurs, 59000 Lille. Conception : Parallel Studio. | This site is published by Halden Sport SA, 12 rue des Tanneurs, 59000 Lille. Design: Parallel Studio. |

Product and colour names are tabled under core feature 4. `max_length` is `70` for `meta.title`,
`160` for `meta.description`, `90` for `hero.title`, `12` for `menu.label` and `menu.close`, `16`
for `shop.cta`, `32` for `lang.label` and `600` for `artist.bio` and `story.body`; the other keys
have none.

**Afterglow copy, the other markets:**

| Key | `it` | `es` | `de` | `be-nl` | `be-fr` |
|---|---|---|---|---|---|
| `lang.label` | Scegli la lingua | Elegir idioma | Sprache wählen | Kies je taal | Choisir la langue |
| `shop.cta` | Negozio | Tienda | Shop | Winkel | Boutique |
| `menu.label` | Menu | Menú | Menü | Menu | Menu |
| `menu.close` | Chiudi | Cerrar | Schließen | Sluiten | Fermer |
| `newtab.suffix` | apre il negozio in una nuova scheda | abre la tienda en una pestaña nueva | öffnet den Shop in einem neuen Tab | opent de winkel in een nieuw tabblad | ouvre la boutique dans un nouvel onglet |
| `legal.title` | Note legali | Aviso legal | Impressum | Wettelijke vermeldingen | Mentions légales |
| `hero.title` | Afterglow, la collezione capsule Halden Sport x Tove Ardenne | Afterglow, la colección cápsula Halden Sport x Tove Ardenne | Afterglow, die Capsule-Kollektion von Halden Sport x Tove Ardenne | Afterglow, de capsulecollectie Halden Sport x Tove Ardenne | Afterglow, la collection capsule Halden Sport x Tove Ardenne |

Every other present translation in those markets is a faithful rendering in the market's own
language, and `be-fr` carries the French values.

**Dusk Parade** has the slug `dusk-parade`, the default locale `be-nl`, the attribution slug
`dusk-parade` and no embargo. Its sections are `hero`, `collection` (anchor `collection`),
`footer_list` and `legal_footer`. Its product is tabled under core feature 4 with a near-black
swatch.

| Key | `be-nl` | `de` |
|---|---|---|
| `meta.title` | Dusk Parade, de avondcollectie van Halden Sport | Dusk Parade, die Abendkollektion von Halden Sport |
| `meta.description` | Een windjack voor wie na zonsondergang loopt. | Eine Windjacke für alle, die nach Sonnenuntergang laufen. |
| `hero.title` | Dusk Parade, lopen na zonsondergang | Dusk Parade, Laufen nach Sonnenuntergang |
| `collection.heading` | De collectie | Die Kollektion |
| `menu.label` | Menu | Menü |
| `menu.close` | Sluiten | Schließen |
| `shop.cta` | Winkel | Shop |
| `lang.label` | Kies je taal | Sprache wählen |
| `newtab.suffix` | opent de winkel in een nieuw tabblad | öffnet den Shop in einem neuen Tab |
| `legal.title` | Wettelijke vermeldingen | Impressum |
| `legal.body` | Deze site wordt uitgegeven door Halden Sport SA, 12 rue des Tanneurs, 59000 Lille. | Diese Website wird von Halden Sport SA, 12 rue des Tanneurs, 59000 Lille herausgegeben. |
| `product.483101.name` | Nachtloper windjack | Nachtläufer Windjacke |
| `colour.7311550.name` | Diepgrijs | Tiefgrau |

The seeded audit log begins with the events that built the seed and verifies intact.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One retailer, no tenancy: every staff member works in the same set of campaigns, bounded by
  grants.
- No visitor accounts, no cart, no checkout, no stock and no order: the storefront owns every sale
  and every stock level, and the page never claims availability beyond the market's own flag.
- No federated sign-in, no provisioning feed, no second factor and no emergency override account:
  staff sign in with the app's own email and password.
- No platform administrator role and no change freeze windows.
- No mail, no in-app notification feed, no digests and no webhooks in either direction.
- No link checking against the storefronts, no catalogue reconciliation, no search-engine
  notification and no translation vendor exchange: each needs a call to another host.
- No hero film, no draggable family track, no per-market colourway availability, no reduced or
  struck-through prices and no product photography.
- No measurement layer, no consent management platform, no newsletter and no analytics of any
  kind.
- No image variants, no licence expiry tracking and no automatic campaign retirement.
- No tracing, no metrics endpoint and no content delivery network in front of the app.
- One colour mode, light.
- No external network call at runtime and no native app.
- The app stays responsive with two campaigns, seven markets, five products, forty-three strings
  translated into seven markets and an audit log of several thousand events.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment;
  never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not be
  running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy of
  any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Every list endpoint returns a top-level JSON array. Bearer auth is carried on everything under
`/api/v1` except `POST /api/v1/auth/login` and the `/api/v1/public` reads; `GET /api/health`
needs none. A successful call returns the named resource or shape; an invalid or unauthorized call
is rejected as a client error with the refusal body of core feature 5, never with a `5xx` and never
with a silent success. In the paths below `{slug}` is a campaign slug and `{market}` a market code.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/v1/auth/login` | `email`, `password` | `token`, `principal` with `email`, `display_name`, `grants` (each `id`, `role`, `market_code`, `effect`, `expires_at`) |
| `POST /api/v1/auth/logout` | none | `{}`; the token is retired |
| `GET /api/v1/me` | none | the `principal` |
| `GET /api/v1/principals` | none | array of `email`, `display_name`; owner only |
| `GET /api/v1/campaigns` | none | array of `slug`, `name`, `default_locale`, `embargo_at` |
| `POST /api/v1/campaigns` | `slug`, `name`, `default_locale`, `attribution_slug`, optional `embargo_at` | the campaign |
| `PATCH /api/v1/campaigns/{slug}` | `name`, `embargo_at` | the campaign |
| `GET /api/v1/campaigns/{slug}/markets` | none | array of `market_code`, `status`, `live_version`, `content_hash` for the markets the caller holds |
| `GET /api/v1/campaigns/{slug}/markets/{market}` | none | `market_code`, `status`, `content_hash`, `live_version`, `hero_asset_id`, `product_order`, `approvals` (each `kind`, `decision`, `decided_by`, `decided_at`, `content_hash`, `superseded`); header `ETag` |
| `PATCH /api/v1/campaigns/{slug}/markets/{market}` | header `If-Match`; `hero_asset_id`, `product_order` | the market, with a new `ETag` |
| `POST /api/v1/campaigns/{slug}/markets/{market}/submit` | none | the market |
| `POST /api/v1/campaigns/{slug}/markets/{market}/approvals` | `kind`, `decision`, `comment` | the market |
| `POST /api/v1/campaigns/{slug}/markets/{market}/publish` | optional header `Idempotency-Key` | the market, with `live_version` |
| `POST /api/v1/campaigns/{slug}/markets/{market}/unpublish` | none | the market |
| `POST /api/v1/campaigns/{slug}/markets/{market}/rollback` | none | the market |
| `GET /api/v1/campaigns/{slug}/markets/{market}/artifacts` | none | array of `version`, `object_key`, `content_hash`, `published_by`, `published_at`, `live` |
| `GET /api/v1/campaigns/{slug}/markets/{market}/render` | none | the render payload of the current content |
| `GET /api/v1/campaigns/{slug}/strings` | none | array of `key`, `context`, `max_length` |
| `POST /api/v1/campaigns/{slug}/strings` | `key`, `context`, `max_length` | the string |
| `GET /api/v1/campaigns/{slug}/translations` | `market` | array of `key`, `market_code`, `value`, `status`, `updated_at`, one row per stored translation; a missing string has no row |
| `PUT /api/v1/campaigns/{slug}/translations/{market}/{key}` | `value`, `status` | the translation |
| `GET /api/v1/campaigns/{slug}/products` | none | array of `id`, `commerce_product_id`, `sort_order`, `colourways` (each `id`, `model_code`, `swatch_hex`, `attribution_slot`), `markets` (each `market_code`, `available`, `price_minor`, `price_currency`) |
| `POST /api/v1/campaigns/{slug}/products` | `commerce_product_id`, `colourways` (each `model_code`, `swatch_hex`) | the product |
| `PATCH /api/v1/products/{id}` | `commerce_product_id`, `sort_order` | the product |
| `POST /api/v1/products/{id}/colourways` | `model_code`, `swatch_hex` | the colourway |
| `PUT /api/v1/products/{id}/markets/{market}` | any of `available`, or `price_minor` together with `price_currency`; a field left out keeps its value | the product market row |
| `POST /api/v1/campaigns/{slug}/assets` | multipart `file`, optional `market_code` | `id`, `object_key`, `checksum`, `byte_size`, `content_type`, `market_code` |
| `GET /api/v1/grants` | none | array of `id`, `email`, `role`, `market_code`, `effect`, `expires_at`, `reason`, `revoked_at` |
| `POST /api/v1/grants` | `email`, `role`, `market_code`, `expires_at`, `reason` | the grant |
| `DELETE /api/v1/grants/{id}` | none | `{}`; the grant is revoked |
| `GET /api/v1/audit` | `market`, `actor`, `action`, `decision`, `limit` | array of events, newest first |
| `GET /api/v1/audit/verify` | none | `intact`, `events`, `head`, `first_broken_id` |
| `POST /api/v1/audit/exports` | none | CSV with a header row |
| `GET /api/v1/public/campaigns/{slug}/markets` | none | array of `market_code`, `hreflang`, `path` for live markets |
| `GET /api/v1/public/campaigns/{slug}/markets/{market}` | none | the render payload of the live artifact, with `version`; not found when not live |

The **render payload** is `campaign` (`slug`, `name`), `market` (`code`, `hreflang`, `currency`,
`legal_page_slug`), `content_hash`, `version` (empty for the current-content render), `strings`
(key to value), `sections` (each `kind`, `anchor`), `shop_url`, `hero_image` (a `/media/{id}`
path or empty), and `products` in the market's order, available ones only, each with
`commerce_product_id`, `name`, `price_minor`, `price_currency`, `price_display` and `colourways`
(each `model_code`, `name`, `swatch_hex`, `attribution_slot`, `url`).

### No mocks

PostgreSQL and MinIO are the facts. Image bytes written to the app container's disk, image bytes in a
database column, an artifact kept in memory, a storefront address stored in a product row, an audit
log the app could quietly rewrite, a content hash accepted from the caller, a grant checked once at
sign-in and cached in the token, or an approval that stays current after an edit: each of these is a
contract violation however good the studio looks. The named provider is the fact - the app's UI and
its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor lands on a live drop page in their own language, picks a colourway, and follows a link that
carries that colourway and the campaign's attribution to their own market's storefront at their own
market's price. Staff translate, clear and publish one market without touching any other, and an edit
after approval withdraws that approval. A write outside a grant, after a grant expires or under a deny
is refused with its reason and recorded, and an image of a market that is not live is never public.
