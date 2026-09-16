# Checklist: Halden Drops

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 604
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` A browser preferring English lands on the English Afterglow address, whose heading reads the capsule collection title `src: Overview`
- [ ] `C-OV-02` `capability` A visitor presses a swatch on a card, so the card link carries the pressed colourway plus the hscamp attribution in the query `src: Overview`
- [ ] `C-OV-03` `constraint` Every storefront link is derived from the market template, never typed by anyone `src: Overview`
- [ ] `C-OV-04` `capability` Staff sign in, clear one market legally, then publish that market, with the page going live `src: Overview`
- [ ] `C-OV-05` `constraint` A staff member cannot change a market outside the staff member's grants, by the studio or by a direct call with the staff member's own token `src: Overview`
- [ ] `C-OV-06` `constraint` A staff member cannot keep writing after a grant has expired; the expired grant is refused, yet the token still authenticates `src: Overview`
- [ ] `C-OV-07` `constraint` A market publish is refused without both current approvals, legal plus owner, matching the market content `src: Overview`
- [ ] `C-OV-08` `constraint` An image uploaded for a market that is not live lives in the object store at the digest key `src: Overview`
- [ ] `C-OV-09` `constraint` An image of a market that is not live is not public through the app `src: Overview`
- [ ] `C-OV-10` `constraint` An image of a market that is not live is not readable from the bucket by an anonymous read `src: Overview`
- [ ] `C-OV-11` `constraint` Every write plus every refusal lands as an audit event, with the refusal reason recorded `src: Overview`
- [ ] `C-OV-12` `constraint` The audit log is one the database refuses to let the app role rewrite `src: Overview`
- [ ] `C-OV-13` `capability` The public side is one long narrative per campaign market, with the anchored sections collection, artist, story, lookbook following the campaign order `src: Overview`
- [ ] `C-OV-14` `constraint` The site sells nothing; every commercial action is a hand-off to the market storefront link `src: Overview`
- [ ] `C-OV-15` `literal` Two campaigns are seeded: `Afterglow` listed in the campaign index, with `Dusk Parade` absent from the campaign index `src: Overview`
- [ ] `C-OV-16` `literal` `Afterglow` is the capsule with the artist Tove Ardenne, whose English heading reads Hi, I am Tove Ardenne in the overlay menu `src: Overview`
- [ ] `C-OV-17` `data` Dusk Parade is a one-product drop, not live at first start, so the Dusk Parade campaign root answers not found `src: Overview`
- [ ] `C-OV-18` `constraint` Each market moves through review on the market's own: approving France leaves Germany untouched `src: Overview`
- [ ] `C-OV-19` `constraint` An approval binds to the content hash approved, so an edit afterwards supersedes the approval `src: Overview`
- [ ] `C-OV-20` `capability` Publishing writes a numbered artifact to the object store, with the live page served from the artifact `src: Overview`
- [ ] `C-OV-21` `constraint` A grant is evaluated at the moment of every request, expiry included, so an issued grant works at once, then stops at expiry mid session `src: Overview`
- [ ] `C-OV-22` `constraint` The audit log is chained, so an altered row breaks verification at the first altered event `src: Overview`
- [ ] `C-OV-23` `constraint` No visitor accounts exist: signup answers as refused, with the staff directory answering the owner only `src: Overview`
- [ ] `C-OV-24` `constraint` No external call at runtime: a public page requests nothing from another host `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` Staff hold accounts; visitors hold none, so signup answers refused, the staff directory answers the owner only `src: User roles`
- [ ] `C-RL-02` `role` Every staff right comes from a grant: a role, the market covered or every market, permit or deny, an optional expiry `src: User roles`
- [ ] `C-RL-03` `role` A visitor reads live market pages, legal notices, the privacy page, live images; a market that is not live answers not found `src: User roles`
- [ ] `C-RL-04` `role` A visitor writes nothing: an anonymous request to a staff surface is sent to sign in `src: User roles`
- [ ] `C-RL-05` `role` The `owner` reads every campaign, market, product, translation, grant, plus the whole audit log with filters `src: User roles`
- [ ] `C-RL-06` `role` The owner issues grants for `editor` plus `translator`, which work on the grantee's very next request once issued `src: User roles`
- [ ] `C-RL-07` `role` The owner cannot record a legal approval, since a legal approval needs a legal grant covering the market `src: User roles`
- [ ] `C-RL-08` `role` The owner cannot change a price: product identity plus prices are merchandiser writes only `src: User roles`
- [ ] `C-RL-09` `role` The owner records the owner approval on a market, making Publish the primary action `src: User roles`
- [ ] `C-RL-10` `role` The `editor` reads the markets the editor's grants cover; a market outside the grants reads as not found `src: User roles`
- [ ] `C-RL-11` `role` The editor writes strings, translations, market fields, images, availability inside the editor's grants only `src: User roles`
- [ ] `C-RL-12` `role` The editor cannot write prices or product identity, which only the merchandiser writes `src: User roles`
- [ ] `C-RL-13` `role` The `translator` writes translations in covered markets; a translator write to a price, product or market field is refused `src: User roles`
- [ ] `C-RL-14` `role` The `legal` role records the legal approval plus unpublish in covered markets, with a grant covering the market `src: User roles`
- [ ] `C-RL-15` `role` The legal role reads the audit events of the markets its grants cover only, a scoped audit reader `src: User roles`
- [ ] `C-RL-16` `role` The `merchandiser` writes products, colourways, availability, prices `src: User roles`
- [ ] `C-RL-17` `role` The merchandiser cannot submit, approve or publish a market `src: User roles`
- [ ] `C-RL-18` `role` The editor cannot approve, publish or roll back a market: each role outside the writable set is refused by role `src: User roles`
- [ ] `C-RL-19` `role` The legal role cannot publish or edit copy: a legal publish or copy write is refused by role `src: User roles`
- [ ] `C-RL-20` `role` The merchandiser cannot edit copy: a merchandiser copy write is refused by role `src: User roles`
- [ ] `C-RL-21` `contract` Authorization is enforced server side on every mutating endpoint; an editor, translator or merchandiser call to an owner-only or legal-only endpoint is refused by role `src: User roles`
- [ ] `C-RL-22` `literal` Every seeded account uses the password `deku-demo-pw-2026`, which signs in; a wrong password is refused alike `src: User roles`
- [ ] `C-RL-23` `literal` `owner@example.com` is Maren Holt, `owner` over every market, as the seeded staff directory shows `src: User roles`
- [ ] `C-RL-24` `literal` `editor@example.com` is Jonas Weber, `editor` on `fr`, `be-nl`, `be-fr` in the seeded grants `src: User roles`
- [ ] `C-RL-25` `literal` `editor@example.com` also holds a deny on `be-fr`, where the deny grant wins over the permit `src: User roles`
- [ ] `C-RL-26` `literal` `editor2@example.com` is Priya Anand, whose seeded `editor` grant on `de` from Parallel Studio carries the reason `Parallel Studio design pass` plus an expiry `src: User roles`
- [ ] `C-RL-27` `literal` `editor3@example.com` is Luca Moretti with no grants in the seed, as the seeded staff directory shows `src: User roles`
- [ ] `C-RL-28` `literal` The seeded grants match the seed: `translator@example.com` on `de`, `es` plus Italy, `legal@example.com` on `fr`, `en`, `be-nl`, `editor@example.com` on `fr`, `be-nl`, `be-fr`, owner plus merchandiser over every market `src: User roles`
- [ ] `C-RL-29` `literal` `translator@example.com` is Sofia Brandt, `translator` on `de`, `es` plus the Italian market in the seeded grants `src: User roles`
- [ ] `C-RL-30` `literal` `legal@example.com` is Camille Roux, `legal` on `fr`, `en`, `be-nl` in the seeded grants `src: User roles`
- [ ] `C-RL-31` `literal` `legal2@example.com` is Anke de Vries, `legal` on `de`, `es`, `be-fr` plus the Italian market, named in the seeded staff directory `src: User roles`
- [ ] `C-RL-32` `literal` `merchandiser@example.com` is Tomás Ibarra, `merchandiser` over every market in the seeded grants `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` `POST /api/v1/auth/login` takes `email` plus `password`, returning a bearer `token` with the signed-in `principal`, so a wrong password signs in nobody `src: Core features`
- [ ] `C-CF-02` `contract` Sign in returns the `principal` with `email`, `display_name` plus `grants`, each grant with `id`, `role`, `market_code`, `effect`, `expires_at` `src: Core features`
- [ ] `C-CF-03` `contract` Every later call carries `Authorization: Bearer <token>`; a studio preview page requested with the bearer token renders the product preview for the signed-in owner `src: Core features`
- [ ] `C-CF-04` `constraint` A token expires 12 hours after issue, stored hashed, never as the token itself `src: Core features`
- [ ] `C-CF-05` `contract` `POST /api/v1/auth/logout` retires the token at once, so the next call with the retired token is refused `src: Core features`
- [ ] `C-CF-06` `literal` A wrong password plus an unknown email are refused with the same message, `Sign-in failed`, alike `src: Core features`
- [ ] `C-CF-07` `literal` The studio sign-in page answers a wrong password with `Sign-in failed`, staying on sign-in `src: Core features`
- [ ] `C-CF-08` `constraint` Passwords are stored hashed; the literal password appears in no stored record `src: Core features`
- [ ] `C-CF-09` `constraint` The literal `deku-demo-pw-2026` works at login for every seeded account, with a wrong password refused alike `src: Core features`
- [ ] `C-CF-10` `constraint` A missing, unknown, retired or expired token is refused as unauthenticated, changing nothing, so logout retires a token for good `src: Core features`
- [ ] `C-CF-11` `constraint` There is no signup: a signup request to create a staff account is refused, creating no account `src: Core features`
- [ ] `C-CF-12` `contract` The staff directory at `GET /api/v1/principals` answers only a signed-in owner; an anonymous directory request is refused `src: Core features`
- [ ] `C-CF-13` `constraint` Signing in settles nothing about rights: a grant expiring mid session stops the grantee on the very next request `src: Core features`
- [ ] `C-CF-14` `constraint` An expired grant is refused on the next request, yet the same token still authenticates `src: Core features`
- [ ] `C-CF-15` `literal` `/afterglow/fr/` is the Afterglow page for France, a live market `src: Core features`
- [ ] `C-CF-16` `constraint` A market page exists only as long as the market is live, holding a current published artifact `src: Core features`
- [ ] `C-CF-17` `constraint` For a market that is not live the page answers as not found `src: Core features`
- [ ] `C-CF-18` `constraint` A market address that is not live shows the not-found page, as the Afterglow es plus be-fr market addresses do `src: Core features`
- [ ] `C-CF-19` `constraint` The drop page is one document in the market's language: the root element declares the market hreflang as the page language `src: Core features`
- [ ] `C-CF-20` `constraint` A live market page carries exactly one `h1`, the heading holding the `hero.title` string `src: Core features`
- [ ] `C-CF-21` `constraint` The live market page declares four landmarks: a banner, a navigation, a main region, a content footer `src: Core features`
- [ ] `C-CF-22` `constraint` Sections follow the campaign order: for Afterglow the collection, the artist section, the story, the lookbook come in that order, each named by the heading `src: Core features`
- [ ] `C-CF-23` `literal` Four sections carry anchors `collection`, `ardenne`, `rx2k`, `lookbook`, each a section element named by the section heading `src: Core features`
- [ ] `C-CF-24` `ui` A fixed bar holds three zones: the menu button at the left, the Halden Sport wordmark in the centre, the language switcher then the shop action at the right `src: Core features`
- [ ] `C-CF-25` `constraint` The menu button opens a full-viewport overlay listing the four anchors by heading `src: Core features`
- [ ] `C-CF-26` `contract` The menu button carries `aria-expanded` reflecting state plus `aria-controls` naming the overlay, opening a modal overlay `src: Core features`
- [ ] `C-CF-27` `constraint` Opening the menu moves focus to the first menu item; the page behind the open overlay menu cannot be reached, being inert or behind a native modal dialog `src: Core features`
- [ ] `C-CF-28` `constraint` `Escape` closes the overlay menu, returning keyboard focus to the menu button `src: Core features`
- [ ] `C-CF-29` `constraint` Choosing a menu item moves focus to the chosen section, which the menu marks current with `aria-current="location"`, as the menu button opens the overlay again `src: Core features`
- [ ] `C-CF-30` `constraint` Choosing a menu item closes the overlay, then the chosen section is in view `src: Core features`
- [ ] `C-CF-31` `literal` The menu button label is the market's `menu.label` when closed, `menu.close` when open, so the English button reads Close once the overlay opens `src: Core features`
- [ ] `C-CF-32` `contract` Every decorative sticker is marked `data-sticker`, `aria-hidden="true"`, `focusable="false"`, hidden from assistive technology `src: Core features`
- [ ] `C-CF-33` `constraint` Decorative stickers include the bolts, arcs, discs, stars plus the triangle, with each sticker never announced by assistive technology `src: Core features`
- [ ] `C-CF-34` `literal` The footer list repeats the market's products as full-width rows numbered `[01]`, `[02]` onward, each price at the right `src: Core features`
- [ ] `C-CF-35` `constraint` The legal footer links the market's legal notice, the privacy page, the design credit to Parallel Studio `src: Core features`
- [ ] `C-CF-36` `constraint` With scripting off every heading, paragraph, product link, price plus the language switcher are in the served document `src: Core features`
- [ ] `C-CF-37` `constraint` No content depends on an animation to become visible, since the served document carries copy without scripts `src: Core features`
- [ ] `C-CF-38` `constraint` With reduced motion requested, no content is left invisible: headings, cards, prices stay opaque `src: Core features`
- [ ] `C-CF-39` `constraint` With reduced motion every scroll reveal sits at the end state, leaving no content invisible off to one side `src: Core features`
- [ ] `C-CF-40` `constraint` Scrolling the drop page slowly from top to bottom, every section heading, product card plus footer list row becomes visible by the time the row is in view `src: Core features`
- [ ] `C-CF-41` `literal` `/afterglow/fr/mentions-legales/` is the French legal notice, with `legal.title` as the heading plus `legal.body` as the text `src: Core features`
- [ ] `C-CF-42` `constraint` Each market's legal notice lives under that market's own legal slug; any other slug under the market answers not found `src: Core features`
- [ ] `C-CF-43` `constraint` `/` lists every campaign with at least one live market, linking to the campaign root `src: Core features`
- [ ] `C-CF-44` `constraint` At first start the campaign index lists Afterglow only, with Dusk Parade absent `src: Core features`
- [ ] `C-CF-45` `data` Seven markets exist as data, not code: adding a market is a row, so the render of every market carries attribution from the market row `src: Core features`
- [ ] `C-CF-46` `literal` `fr` has hreflang `fr-FR`, the name `Français`, currency `EUR`, host `shop-fr.example.com`, no locale segment, legal slug `mentions-legales`, seeded in the locale matrix `src: Core features`
- [ ] `C-CF-47` `literal` `en` has hreflang `en`, the name `English`, currency `GBP`, host `shop-uk.example.com`, no segment, legal slug `legal-notice`, seeded in the locale matrix `src: Core features`
- [ ] `C-CF-48` `literal` The seeded Italian market row holds the Italian hreflang code, the name `Italiano`, currency `EUR`, the Italian shop host, no locale segment, legal slug `note-legali` in the locale matrix `src: Core features`
- [ ] `C-CF-49` `literal` `es` has hreflang `es`, the name `Español`, host `shop-es.example.com`, the locale segment `/es`, legal slug `aviso-legal`, seeded in the locale matrix `src: Core features`
- [ ] `C-CF-50` `literal` `de` has hreflang `de`, the name `Deutsch`, host `shop-de.example.com`, no segment, legal slug `impressum`, seeded in the locale matrix `src: Core features`
- [ ] `C-CF-51` `literal` `be-nl` has hreflang `nl`, the name `Nederlands (België)`, host `shop-be.example.com`, segment `/nl`, legal slug `wettelijke-vermeldingen`, seeded in the locale matrix `src: Core features`
- [ ] `C-CF-52` `literal` `be-fr` has hreflang `fr-BE`, the name `Français (Belgique)`, host `shop-be.example.com`, segment `/fr`, legal slug `mentions-legales`, seeded in the locale matrix `src: Core features`
- [ ] `C-CF-53` `constraint` `/afterglow/` never renders a page; the campaign root redirect is temporary, never permanent `src: Core features`
- [ ] `C-CF-54` `constraint` The campaign root prefers the `drop_lang` cookie market when that market is live `src: Core features`
- [ ] `C-CF-55` `constraint` Next the campaign root prefers a live market whose hreflang equals an `Accept-Language` tag `src: Core features`
- [ ] `C-CF-56` `constraint` Next the campaign root matches the primary language of a tag, in market table order, before the default `src: Core features`
- [ ] `C-CF-57` `constraint` Then the campaign root takes the default locale when live, then the first live market in table order `src: Core features`
- [ ] `C-CF-58` `constraint` A campaign with no live market answers not found at the campaign root `src: Core features`
- [ ] `C-CF-59` `contract` The language switcher is a native select whose label reads the market's `lang.label`, listing live markets `src: Core features`
- [ ] `C-CF-60` `constraint` The switcher lists only live markets, each option written as the market name in the market's own language `src: Core features`
- [ ] `C-CF-61` `contract` Each switcher option carries a `lang` attribute equal to that market's hreflang, listing live markets only `src: Core features`
- [ ] `C-CF-62` `constraint` Each switcher option keeps the same document: from the French legal notice the English option leads to `/afterglow/en/legal-notice/`, not the English home `src: Core features`
- [ ] `C-CF-63` `literal` Choosing a language goes through `/lang?to=<path>`, which sets the preference cookie `drop_lang` to the chosen market `src: Core features`
- [ ] `C-CF-64` `constraint` Choosing a language sets the preference cookie on path `/`, kept for 365 days, same-site lax, then redirects to the chosen path `src: Core features`
- [ ] `C-CF-65` `constraint` The language switcher works with scripting off, since the served document carries the switcher without scripts `src: Core features`
- [ ] `C-CF-66` `constraint` A language target that is not a path to a live document on the site, a foreign host included, is refused, setting no cookie `src: Core features`
- [ ] `C-CF-67` `contract` Every live page declares an alternate link for every live market, itself included, forming reciprocal links `src: Core features`
- [ ] `C-CF-68` `contract` Alternate links add `x-default` pointing at `/afterglow/` plus a self canonical link `src: Core features`
- [ ] `C-CF-69` `constraint` Alternates are reciprocal: if France links England as alternate, England links France `src: Core features`
- [ ] `C-CF-70` `constraint` Every public route has its own title plus its own meta description, with no two routes sharing either `src: Core features`
- [ ] `C-CF-71` `constraint` A drop page takes `meta.title` plus `meta.description` as the route title plus description `src: Core features`
- [ ] `C-CF-72` `constraint` A legal notice takes `legal.title` joined with the campaign name as the route title, plus a description drawn from `legal.body` `src: Core features`
- [ ] `C-CF-73` `contract` `/sitemap.xml` lists `/`, `/privacy/`, every live market page plus the legal notice, only live documents `src: Core features`
- [ ] `C-CF-74` `constraint` The sitemap lists nothing that is not live: Afterglow Italy, be-fr, Dusk Parade be-nl stay out of the sitemap `src: Core features`
- [ ] `C-CF-75` `contract` `/robots.txt` names the sitemap, disallowing `/studio/` plus `/api/` for robots `src: Core features`
- [ ] `C-CF-76` `constraint` The collection section holds one card per product available in the market, so an unavailable product has no card `src: Core features`
- [ ] `C-CF-77` `contract` A card is marked `data-product` with the commerce product id, holding a swipeable slide per colourway, the product name, the price, one swatch per colourway `src: Core features`
- [ ] `C-CF-78` `constraint` A storefront link is derived, never stored, from the market template, replacing the hand-typed links that drifted `src: Core features`
- [ ] `C-CF-79` `constraint` A derived storefront link is `https://`, then the market host, then the locale segment, then `/p/*/_/R-p-` with the commerce product id `src: Core features`
- [ ] `C-CF-80` `constraint` The derived link query carries `mc` as the model code, `hscamp` as the attribution value, `type` as `hscamp`, with the market link parameters percent-encoded `src: Core features`
- [ ] `C-CF-81` `constraint` The asterisk in the derived storefront link path stays literal in the market template `src: Core features`
- [ ] `C-CF-82` `constraint` The attribution value is the campaign prefix, the attribution slug, `_`, then the colourway slot, carried by every market link `src: Core features`
- [ ] `C-CF-83` `literal` The graphic tee in pink is product `482913`, model `7310042`, slot `p1`, whose French card link leads to `shop-fr.example.com` with `mc=7310042` in the query `src: Core features`
- [ ] `C-CF-84` `literal` The derived `fr` link is `https://shop-fr.example.com/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` from the market template `src: Core features`
- [ ] `C-CF-85` `literal` The derived `es` link is `https://shop-es.example.com/es/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` from the market template `src: Core features`
- [ ] `C-CF-86` `literal` The derived `be-nl` link is `https://shop-be.example.com/nl/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` from the market template `src: Core features`
- [ ] `C-CF-87` `constraint` Every market carries attribution or none does: no market link lacks the `hscamp` plus `type` parameters `src: Core features`
- [ ] `C-CF-88` `constraint` The shop action in the bar leads to the market collection page for the campaign, with attribution `src: Core features`
- [ ] `C-CF-89` `literal` The shop action collection link is `https://`, host, segment, `/c/` plus the campaign slug, with `hscamp` = `hscamp:__drop-afterglow` plus `type` = `hscamp` as attribution `src: Core features`
- [ ] `C-CF-90` `constraint` The shop action is labelled with the market's `shop.cta`, leading to the market collection `src: Core features`
- [ ] `C-CF-91` `contract` Each colourway's own link is marked `data-colourway` with the model code, carrying the link served in the document `src: Core features`
- [ ] `C-CF-92` `constraint` The card title links to the selected colourway too, so the pressed White swatch makes the card link carry mc=7310043 `src: Core features`
- [ ] `C-CF-93` `contract` Every link opening a new tab, the shop action, wordmark plus design credit included, carries `rel="noopener noreferrer"`, isolated `src: Core features`
- [ ] `C-CF-94` `constraint` Every storefront link, the shop action plus the design credit carry the market's `newtab.suffix` as text announced to assistive technology only `src: Core features`
- [ ] `C-CF-95` `contract` Swatches are buttons marked `data-swatch` with the model code, carrying `aria-pressed`, named swatches `src: Core features`
- [ ] `C-CF-96` `literal` A swatch is named by the colour name in the market language: `Blanc` in France, `White` in the United Kingdom, so the White swatch reads as pressed once pressed `src: Core features`
- [ ] `C-CF-97` `constraint` Activating a swatch by click, `Enter` or `Space` selects the colourway; the arrow keys move between a card's swatches, operated by keyboard `src: Core features`
- [ ] `C-CF-98` `constraint` Exactly one swatch per card is pressed, so pressing White leaves Pink unpressed `src: Core features`
- [ ] `C-CF-99` `constraint` Each swatch looks small yet offers a hit area of at least 44 by 44 CSS pixels around the swatch centre, as named pressed buttons `src: Core features`
- [ ] `C-CF-100` `constraint` A product unavailable in the market has no card plus no footer row: absent, not greyed out, not a dead link `src: Core features`
- [ ] `C-CF-101` `literal` Track pants are not available in `en`, so the English collection shows no Track pants card `src: Core features`
- [ ] `C-CF-102` `constraint` A price is the market's own, in the market currency, formatted from integer minor units at render `src: Core features`
- [ ] `C-CF-103` `literal` `2000` `EUR` reads `20,00 €` in `fr`, `es`, `de`, `be-fr` plus the Italian market, formatted in the market currency from minor units `src: Core features`
- [ ] `C-CF-104` `literal` `2000` `EUR` reads `€ 20,00` in `be-nl`, formatted from minor units in the market currency `src: Core features`
- [ ] `C-CF-105` `literal` `1700` `GBP` reads `£17.00` in `en`, so the English prices read £17.00, £39.00, £79.00, formatted from minor units in the market currency `src: Core features`
- [ ] `C-CF-106` `contract` The price element is marked `data-price`, carrying the prices served in the document `src: Core features`
- [ ] `C-CF-107` `constraint` A product with no price for the market renders the card with no price, never another market's price, in the preview `src: Core features`
- [ ] `C-CF-108` `constraint` The platform stores no product photography; each colourway slide is a panel painted in the stored swatch colour `src: Core features`
- [ ] `C-CF-109` `contract` Each slide is marked `data-slide` with the model code, painted in the colourway swatch at a fixed portrait proportion `src: Core features`
- [ ] `C-CF-110` `data` A product belongs to one campaign with a global, merchandiser-owned `commerce_product_id`, written only by the merchandiser `src: Core features`
- [ ] `C-CF-111` `data` Each colourway carries a global `model_code`, a `swatch_hex`, an attribution slot, validated as product identifiers `src: Core features`
- [ ] `C-CF-112` `data` Availability plus price belong to a product in one market, formatted in that market currency `src: Core features`
- [ ] `C-CF-113` `literal` Afterglow product 1 is `482913` T-shirt graphique / Graphic tee with `7310042` `p1` Rose / Pink plus `7310043` `p2` Blanc / White, the seeded copy deck of every market naming each `src: Core features`
- [ ] `C-CF-114` `literal` Afterglow product 2 is `482927` Veste de survêtement / Track jacket with `7310118` `p3` Pervenche / Periwinkle plus `7310119` `p4` Blanc cassé / Off white, matching the seeded copy deck `src: Core features`
- [ ] `C-CF-115` `literal` Afterglow product 3 is `482940` Pantalon de survêtement / Track pants with `7310205` `p5` Pervenche / Periwinkle, the product unavailable in en with no card `src: Core features`
- [ ] `C-CF-116` `literal` Afterglow product 4 is `482956` RX2K with `7310377` `p6` Sarcelle profonde / Deep teal plus `7310378` `p7` Blanc / White, matching the seeded copy deck `src: Core features`
- [ ] `C-CF-117` `literal` In every euro market the four products are available at `2000`, `4500`, `3500`, `9000` `EUR`, so the French footer list reads 20,00 €, 45,00 €, 35,00 €, 90,00 € `src: Core features`
- [ ] `C-CF-118` `literal` In `en` the graphic tee is `1700` `GBP`, the track jacket `3900` `GBP`, the RX2K `7900` `GBP`, prices formatted in the market currency `src: Core features`
- [ ] `C-CF-119` `constraint` A `commerce_product_id` is 4 to 10 digits, unique within the campaign; anything else is rejected as invalid, validated `src: Core features`
- [ ] `C-CF-120` `constraint` A `model_code` is 6 to 10 digits, unique within the product, validated with the product identifiers `src: Core features`
- [ ] `C-CF-121` `constraint` A `swatch_hex` is `#` followed by six hexadecimal digits, validated with the product swatches `src: Core features`
- [ ] `C-CF-122` `constraint` An invalid product identifier is rejected naming the field, storing nothing; a repeated identifier is refused as `duplicate`, validated `src: Core features`
- [ ] `C-CF-123` `constraint` Slots are assigned by the server, never typed: a new colourway takes `p` plus one more than the highest slot in the campaign `src: Core features`
- [ ] `C-CF-124` `literal` A new Afterglow colourway would take `p8`, since the server assigned slots `p1` through `p7` `src: Core features`
- [ ] `C-CF-125` `constraint` A slot is unique within the campaign, stable for the life of the campaign, since reassigning slots would merge conversion data `src: Core features`
- [ ] `C-CF-126` `constraint` A request that sends a slot is refused with `field_not_permitted`, the sent slot refused by the server `src: Core features`
- [ ] `C-CF-127` `constraint` Creating a product creates the product name string plus one colour name string per colourway `src: Core features`
- [ ] `C-CF-128` `literal` The created strings are `product.<id>.name` plus `colour.<model_code>.name`, with no translations yet after creating the product `src: Core features`
- [ ] `C-CF-129` `constraint` `price_minor` is a whole number of minor units greater than zero, below `100000000`, inside the range `src: Core features`
- [ ] `C-CF-130` `literal` `20.00`, `"2000"`, `0` are each rejected as invalid price minor units `src: Core features`
- [ ] `C-CF-131` `constraint` A price's currency always equals the market currency; a price in another currency is refused, nothing changes `src: Core features`
- [ ] `C-CF-132` `literal` Setting the graphic tee `en` price to `1700` `EUR` is refused with `currency_mismatch`, the stored price unchanged at `1700` `GBP` `src: Core features`
- [ ] `C-CF-133` `constraint` A price sent without a currency is rejected as invalid, whole minor units needing a currency `src: Core features`
- [ ] `C-CF-134` `constraint` Product identity, colourways plus prices are merchandiser fields; anyone else writing one is refused with `field_not_permitted` `src: Core features`
- [ ] `C-CF-135` `constraint` The owner, or an editor inside the editor's grants, may change `available` alone, never the product prices `src: Core features`
- [ ] `C-CF-136` `constraint` No storefront address is accepted or stored: a body carrying a `url` field is refused with `field_not_permitted` `src: Core features`
- [ ] `C-CF-137` `contract` Every refusal answers with JSON carrying `title`, a stable `reason`, the `request_id` `src: Core features`
- [ ] `C-CF-138` `contract` A refusal of an invalid body also carries `fields` naming each bad field, beside the reason plus request id `src: Core features`
- [ ] `C-CF-139` `constraint` A request is authenticated first, then validated, then authorized: an anonymous invalid write carries `not_authenticated`, an out-of-scope invalid body carries `invalid`, so every refusal carries its reason `src: Core features`
- [ ] `C-CF-140` `constraint` Silent denial is a defect, so every deny is logged with the reason as a refusal audit event `src: Core features`
- [ ] `C-CF-141` `literal` `not_authenticated`: no valid token, so an anonymous staff directory request is refused `src: Core features`
- [ ] `C-CF-142` `literal` `role_not_permitted`: no role held may take the action, so the merchandiser cannot submit, approve or publish `src: Core features`
- [ ] `C-CF-143` `literal` `market_out_of_scope`: a role allows the write, yet no grant covers the market, so an editor write outside the grants is refused `src: Core features`
- [ ] `C-CF-144` `literal` `grant_expired`: the only covering grant has passed expiry, so the expired grant is refused `src: Core features`
- [ ] `C-CF-145` `literal` `explicit_deny`: a deny grant covers the market; a deny grant always wins over a permit `src: Core features`
- [ ] `C-CF-146` `literal` `field_not_permitted`: the body writes a field outside the role's set, so the translator cannot write product, price or market fields `src: Core features`
- [ ] `C-CF-147` `literal` `role_not_grantable`: a grant requested for `owner`, `legal` or `merchandiser`, a role the grant cannot carry `src: Core features`
- [ ] `C-CF-148` `literal` `invalid`: the body or the request is malformed, so a price outside the whole minor units range is refused `src: Core features`
- [ ] `C-CF-149` `literal` `duplicate`: the identifier, key or slug already exists, so a repeated product identifier is refused `src: Core features`
- [ ] `C-CF-150` `literal` `currency_mismatch`: a price currency differs from the market currency, refused with nothing changed `src: Core features`
- [ ] `C-CF-151` `literal` `translations_incomplete`: a submit found a key missing or not reviewed, so submit is refused on incomplete translations `src: Core features`
- [ ] `C-CF-152` `literal` `price_missing`: a submit found an available product with no price, so submit is refused on incomplete prices `src: Core features`
- [ ] `C-CF-153` `literal` `untranslated_copy`: a translation repeats the default language copy in another language, refused `src: Core features`
- [ ] `C-CF-154` `literal` `machine_legal_text`: legal text sent as `machine`, never accepted as machine translation `src: Core features`
- [ ] `C-CF-155` `literal` `approvals_incomplete`: a publish lacked a current legal or owner approval, refused without both approvals `src: Core features`
- [ ] `C-CF-156` `literal` `embargo_pending`: a publish came before the campaign embargo time, refused `src: Core features`
- [ ] `C-CF-157` `literal` `not_live`: an unpublish targeted a market that is not live, refused once the page is down `src: Core features`
- [ ] `C-CF-158` `literal` `nothing_to_roll_back`: a rollback found no earlier artifact to make live `src: Core features`
- [ ] `C-CF-159` `literal` `stale_version`: `If-Match` no longer matches the market, so a market change needs a current match `src: Core features`
- [ ] `C-CF-160` `literal` `precondition_required`: a market change came without `If-Match`, needing a current match `src: Core features`
- [ ] `C-CF-161` `literal` `unsupported_media`: an upload is not a PNG, JPEG or WebP image, uploads typed by bytes `src: Core features`
- [ ] `C-CF-162` `constraint` Market scope: `editor@example.com` writing a translation in `de` is refused with `market_out_of_scope`, the write outside the grants unchanged `src: Core features`
- [ ] `C-CF-163` `constraint` Expiry is checked at decision time: `editor2@example.com` signs in, yet every write in `de` is refused with `grant_expired` `src: Core features`
- [ ] `C-CF-164` `constraint` A deny wins: `editor@example.com` holds a permit plus a deny on `be-fr`; every write there is refused with `explicit_deny` `src: Core features`
- [ ] `C-CF-165` `constraint` Fields: `translator@example.com` writing a price, a model code, a swatch or availability is refused with `field_not_permitted` `src: Core features`
- [ ] `C-CF-166` `constraint` Roles: `merchandiser@example.com` submitting, approving or publishing a market is refused with `role_not_permitted` `src: Core features`
- [ ] `C-CF-167` `constraint` Reads: a market page, record, translation list, render or preview outside the reader's grants answers not found `src: Core features`
- [ ] `C-CF-168` `constraint` Reading a market outside the grants reads as not found, so a stranger cannot learn the market state `src: Core features`
- [ ] `C-CF-169` `contract` `POST /api/v1/grants` takes `email`, `role` (`editor` or `translator`), `market_code`, `expires_at`, `reason`, a grant the owner issues `src: Core features`
- [ ] `C-CF-170` `constraint` A grant needs an expiry, in the future, no more than 90 days away, plus a reason; otherwise the grant is rejected as invalid `src: Core features`
- [ ] `C-CF-171` `constraint` A grant for another role is refused with `role_not_grantable`, since a grant needs a grantable role `src: Core features`
- [ ] `C-CF-172` `constraint` A new grant works on the grantee's very next request without signing in again, an owner-issued grant working at once `src: Core features`
- [ ] `C-CF-173` `contract` `DELETE /api/v1/grants/{id}` revokes a grant; the grantee's next request in that market is refused, the revoked grant stopping requests `src: Core features`
- [ ] `C-CF-174` `constraint` A grant expiring between two requests on one token: the first write succeeds, the second is refused with `grant_expired`, mid session `src: Core features`
- [ ] `C-CF-175` `constraint` After a grant expires mid session, `GET /api/v1/me` still answers for the same token, so the expired grant token authenticates `src: Core features`
- [ ] `C-CF-176` `data` Every piece of copy is a keyed string of a campaign with a translation per market, so a new campaign starts with eleven strings `src: Core features`
- [ ] `C-CF-177` `literal` Afterglow has thirty strings, Dusk Parade thirteen, matching the seeded copy deck of every market `src: Core features`
- [ ] `C-CF-178` `literal` A translation status is one of `machine`, `draft`, `reviewed`, `approved`; a string with no translation is missing, so submit is refused on incomplete translations `src: Core features`
- [ ] `C-CF-179` `constraint` A translation value is required, no longer than the string budget `max_length` when set; a longer translation is rejected naming `value` `src: Core features`
- [ ] `C-CF-180` `constraint` In a market whose language differs from the default language, a value containing the default copy word for word is refused as untranslated copy `src: Core features`
- [ ] `C-CF-181` `constraint` The untranslated copy rule applies only where the default copy is 20 characters or longer, so short labels such as `Menu` in another language pass `src: Core features`
- [ ] `C-CF-182` `constraint` `be-fr` is exempt from the untranslated copy rule, sharing the default language `src: Core features`
- [ ] `C-CF-183` `constraint` Legal text is never machine translated: `legal.body` or `legal.title` sent as `machine` is never accepted, refused with `machine_legal_text` `src: Core features`
- [ ] `C-CF-184` `constraint` A source edit in the default locale moves that key's translation in every other market from reviewed or approved to draft, requeueing every other market `src: Core features`
- [ ] `C-CF-185` `constraint` A source edit returns every other market that was in review, approved, published or unpublished to draft, its approvals superseded `src: Core features`
- [ ] `C-CF-186` `constraint` After a source edit a live market stays live on the current artifact, with the live page showing the artifact rather than later edits `src: Core features`
- [ ] `C-CF-187` `constraint` A translation status change alone never changes a market's content hash `src: Core features`
- [ ] `C-CF-188` `literal` A new campaign starts with eleven strings: `meta.title`, `meta.description`, `hero.title`, `collection.heading`, `menu.label`, `menu.close`, `shop.cta`, `lang.label`, `newtab.suffix`, `legal.title`, `legal.body` `src: Core features`
- [ ] `C-CF-189` `constraint` A new campaign's eleven strings carry no length budget, with seven draft markets `src: Core features`
- [ ] `C-CF-190` `literal` A new campaign starts with the sections `hero`, `collection` (anchor `collection`), `footer_list`, `legal_footer`, its seven markets as draft `src: Core features`
- [ ] `C-CF-191` `contract` The studio preview shows a missing string in the default value, marking the element `data-untranslated` with the key, preview strings untranslated `src: Core features`
- [ ] `C-CF-192` `constraint` A live page never falls back to another language: the live French page carries no untranslated marks, only the preview marks strings `src: Core features`
- [ ] `C-CF-193` `literal` A campaign market status is one of `draft`, `in_review`, `approved`, `published`, `unpublished`, matching the seeded market states `src: Core features`
- [ ] `C-CF-194` `constraint` Separately, a market is live as long as the market holds a current artifact, so the seeded market states pair status with a live version `src: Core features`
- [ ] `C-CF-195` `literal` Afterglow `fr` is `published`, version 1 live, current legal plus owner approvals, translations `approved`, matching the seeded market states `src: Core features`
- [ ] `C-CF-196` `literal` Afterglow `en` is `published`, version 1 live, current legal plus owner approvals, matching the seeded market states `src: Core features`
- [ ] `C-CF-197` `literal` The Afterglow Italian market is `approved`, not live, legal plus owner approvals current, translations `reviewed`, with Publish as the primary action `src: Core features`
- [ ] `C-CF-198` `literal` Afterglow `de` is `in_review`, not live, with the legal approval only, matching the seeded approvals `src: Core features`
- [ ] `C-CF-199` `literal` Afterglow `es` is `draft` with `legal.body` plus `story.body` missing, `artist.bio` `machine`, the rest `draft`, so submit is refused on incomplete translations `src: Core features`
- [ ] `C-CF-200` `literal` Afterglow `be-nl` is `draft` with no approvals, every translation `reviewed`, matching the seeded market states `src: Core features`
- [ ] `C-CF-201` `literal` Afterglow `be-fr` is `unpublished`, not live, version 1 stored, approvals current, matching the seeded market states `src: Core features`
- [ ] `C-CF-202` `literal` The editor submits Dusk Parade `be-nl` from `draft`, the market status reading `in_review` `src: Core features`
- [ ] `C-CF-203` `constraint` A market `content_hash` is 64 lowercase hexadecimal characters, the content hash that approvals bind `src: Core features`
- [ ] `C-CF-204` `constraint` The content hash covers the market translations, availability, prices, the campaign products, colourways, slots, swatches, attribution, sections, hero image, product order `src: Core features`
- [ ] `C-CF-205` `constraint` The content hash changes when a hashed input such as a translation value changes; a status change alone or another market's edit never changes the content hash `src: Core features`
- [ ] `C-CF-206` `contract` `POST .../submit` moves a draft market to `in_review`, for the owner or an editor or translator inside the grants `src: Core features`
- [ ] `C-CF-207` `constraint` Submit is refused with `translations_incomplete`, plus a `keys` list, as long as translations are incomplete `src: Core features`
- [ ] `C-CF-208` `constraint` Submit is refused with `price_missing`, plus a `products` list, when an available product has incomplete prices `src: Core features`
- [ ] `C-CF-209` `constraint` Afterglow `es` cannot be submitted, refused on incomplete translations, the market staying draft `src: Core features`
- [ ] `C-CF-210` `constraint` A market that is not draft cannot be submitted; submit on an approved market is refused as invalid `src: Core features`
- [ ] `C-CF-211` `contract` `POST .../approvals` takes `kind` (`legal` or `owner`), `decision` (`approved` or `rejected`), an optional `comment`, recording an approval in the approvals list `src: Core features`
- [ ] `C-CF-212` `constraint` An approval is recorded only when the market is in review, a legal approval needing a legal grant covering the market `src: Core features`
- [ ] `C-CF-213` `literal` `legal@example.com` approving `de` is refused with `market_out_of_scope`, the legal approval needing a grant covering the market `src: Core features`
- [ ] `C-CF-214` `constraint` An owner approval needs the owner; legal recording the owner kind is refused, each approval kind needing a grant `src: Core features`
- [ ] `C-CF-215` `constraint` Each approval records the market content hash at that moment, so approvals bind to the content hash `src: Core features`
- [ ] `C-CF-216` `constraint` A current legal approval plus a current owner approval for the present hash make the market status read approved `src: Core features`
- [ ] `C-CF-217` `constraint` A rejection returns the market to draft, so publish is refused without both current approvals `src: Core features`
- [ ] `C-CF-218` `constraint` An edit changing the content hash of a market in review, approved, published or unpublished returns the market to draft, the edit superseding every approval `src: Core features`
- [ ] `C-CF-219` `constraint` Markets are independent: approving or publishing one market leaves every other market's status, approvals, hash, artifact untouched `src: Core features`
- [ ] `C-CF-220` `constraint` Approving France never publishes Germany: after approving plus publishing fr, the de market is untouched `src: Core features`
- [ ] `C-CF-221` `constraint` Publishing Dusk Parade be-nl leaves the Dusk Parade de address showing the not-found page `src: Core features`
- [ ] `C-CF-222` `contract` `POST .../publish` is the owner's, requiring the market approved, or unpublished with both approvals current; otherwise publish is refused without both current approvals `src: Core features`
- [ ] `C-CF-223` `constraint` Publish before the campaign `embargo_at` is refused with `embargo_pending`, then allowed once the embargo passes `src: Core features`
- [ ] `C-CF-224` `constraint` Publishing writes the next artifact version, sets the market published, making that version live in the artifact list `src: Core features`
- [ ] `C-CF-225` `constraint` A publish repeating an `Idempotency-Key` already used by the same principal on the same market within 24 hours returns the first response, publishing once `src: Core features`
- [ ] `C-CF-226` `constraint` A repeated idempotency key writes no second version, records no second publish, so the key publishes once `src: Core features`
- [ ] `C-CF-227` `constraint` Unpublish is always easy: the owner or a legal reviewer inside the grants takes the page down at once, without approval `src: Core features`
- [ ] `C-CF-228` `constraint` After unpublish the market is `unpublished`, no longer live, its page not found on the next request, taken down at once `src: Core features`
- [ ] `C-CF-229` `constraint` Once unpublish takes the page down, a second unpublish is refused with `not_live` `src: Core features`
- [ ] `C-CF-230` `constraint` A legal reviewer unpublishing a market records `market.unpublish` with the reviewer as actor, taking the page down at once `src: Core features`
- [ ] `C-CF-231` `constraint` Unpublishing Dusk Parade be-nl makes the be-nl address show the not-found page again, the market reading unpublished `src: Core features`
- [ ] `C-CF-232` `contract` `POST .../rollback` by the owner makes the highest earlier artifact version live, leaving the market status unchanged `src: Core features`
- [ ] `C-CF-233` `constraint` A rollback with no earlier version is refused with `nothing_to_roll_back` `src: Core features`
- [ ] `C-CF-234` `constraint` Rollback is the resilience control bounding what a bad publish costs: the previous artifact becomes live again `src: Core features`
- [ ] `C-CF-235` `constraint` The live page is the artifact: once published, the public page shows what the artifact holds rather than later edits `src: Core features`
- [ ] `C-CF-236` `constraint` An edit made after publishing does not reach the live page until the market is approved plus published again, the artifact live rather than edits `src: Core features`
- [ ] `C-CF-237` `contract` Reading a market returns an `ETag`, so a market change needs a current match `src: Core features`
- [ ] `C-CF-238` `contract` `PATCH` of a market (`hero_asset_id`, `product_order`) must carry `If-Match`; a market change without the match is refused with `precondition_required` `src: Core features`
- [ ] `C-CF-239` `constraint` A market change with an `If-Match` no longer current is refused with `stale_version`, writing nothing `src: Core features`
- [ ] `C-CF-240` `constraint` Two editors saving from the same read: the first save lands, the second market change is refused, needing a current match `src: Core features`
- [ ] `C-CF-241` `contract` `POST /api/v1/campaigns/{slug}/assets` takes a multipart `file` plus an optional `market_code`, absent meaning shared, an upload stored at the digest key `src: Core features`
- [ ] `C-CF-242` `constraint` Uploads are typed by bytes, not the file name: only PNG, JPEG, WebP bytes are accepted `src: Core features`
- [ ] `C-CF-243` `constraint` Uploads typed by bytes refuse anything else with `unsupported_media`, a file over 5 MB rejected as invalid `src: Core features`
- [ ] `C-CF-244` `constraint` A market image upload needs the owner or an editor inside the grants; a shared image upload needs the owner, so uploads by an editor for another market are refused `src: Core features`
- [ ] `C-CF-245` `constraint` The image bytes live in the object store at the digest key, nowhere else, never as database bytes `src: Core features`
- [ ] `C-CF-246` `literal` An image is stored at `assets/{campaign_slug}/{market_code or shared}/{sha256 of the bytes}.{png, jpg or webp}`, the digest key in the object store `src: Core features`
- [ ] `C-CF-247` `literal` A worked example object key is `assets/afterglow/fr/9c1d...4e.png`, a digest key in the object store `src: Core features`
- [ ] `C-CF-248` `contract` The upload response carries `id`, `object_key`, `checksum` (lowercase hex sha256), `byte_size`, `content_type`, `market_code`, the digest key stored `src: Core features`
- [ ] `C-CF-249` `constraint` The same bytes uploaded again for the same market return the same asset, storing no second object at the digest key `src: Core features`
- [ ] `C-CF-250` `constraint` The bucket is private: an object requested from the store without credentials is refused, an anonymous read of the bucket refused `src: Core features`
- [ ] `C-CF-251` `constraint` `/media/{id}` serves a market image only when that market is live, so an image of a market that is not live is not public `src: Core features`
- [ ] `C-CF-252` `constraint` A shared image is public only when the campaign has a live market, a shared image of no live market staying not public `src: Core features`
- [ ] `C-CF-253` `constraint` A live image is served with the stored bytes unchanged plus the stored content type, public once the market is live `src: Core features`
- [ ] `C-CF-254` `constraint` An image answers not found again the moment the market is unpublished, an image no longer public `src: Core features`
- [ ] `C-CF-255` `constraint` A market `hero_asset_id` names an image of the same campaign, shared or of that market; anything else is rejected as invalid, a market change refused `src: Core features`
- [ ] `C-CF-256` `constraint` Each publish stores the market content as a JSON artifact in the object store, versioned per publish `src: Core features`
- [ ] `C-CF-257` `literal` An artifact is stored at `artifacts/{campaign_slug}/{market_code}/{version}.json`, e.g. `artifacts/afterglow/fr/1.json`, a versioned artifact in the object store `src: Core features`
- [ ] `C-CF-258` `contract` The market artifact list names each version with `object_key`, `content_hash`, `published_by`, `published_at`, whether live, the versioned artifact the publish stores `src: Core features`
- [ ] `C-CF-259` `constraint` The Afterglow fr artifact list shows version 1 marked live with the market status reading published `src: Core features`
- [ ] `C-CF-260` `constraint` Every successful write records exactly one audit event with `decision` `permit` `src: Core features`
- [ ] `C-CF-261` `constraint` Every refused write by a signed-in principal records exactly one audit event with `decision` `deny` plus the refusal reason `src: Core features`
- [ ] `C-CF-262` `contract` An audit event carries `id`, `occurred_at`, `actor_email`, `action`, `resource_type`, `resource_id`, `campaign_slug`, `market_code`, `decision`, `reason`, `request_id`, `before`, `after`, `prev_hash`, `hash`, recorded per write `src: Core features`
- [ ] `C-CF-263` `literal` A translation write records one audit event with the action `translation.write`, the refusal event action drawn from the closed audit action set `src: Core features`
- [ ] `C-CF-264` `literal` Publishing then rolling back records the actions `market.submit`, `approval.record`, `market.publish`, `market.rollback` for the market, rollback making the previous artifact live `src: Core features`
- [ ] `C-CF-265` `literal` Issuing then revoking a grant records `grant.create` plus `grant.revoke` against the revoked grant, which stops the next request `src: Core features`
- [ ] `C-CF-266` `literal` Creating a product records `product.create`, a new colourway `colourway.create`, as slots are assigned by the server `src: Core features`
- [ ] `C-CF-267` `literal` Writing a price records `price.write`, a whole minor units price inside the range `src: Core features`
- [ ] `C-CF-268` `literal` Creating a string records `string.create` for a budget string whose longer translation is rejected `src: Core features`
- [ ] `C-CF-269` `literal` Creating a campaign records `campaign.create`, changing the embargo `campaign.update`, before publish is refused on the embargo `src: Core features`
- [ ] `C-CF-270` `literal` A market change records `market.update` as a permitted audit write once the If-Match save lands `src: Core features`
- [ ] `C-CF-271` `constraint` A market change to `product_order` listing some products puts those first, the rest following in the campaign order; an empty `product_order` restores the campaign order, the products' `sort_order` `src: Core features`
- [ ] `C-CF-272` `literal` A product change records `product.update`, as a merchandiser setting the `sort_order` of a product needs a current market If-Match only for the market order `src: Core features`
- [ ] `C-CF-273` `literal` An upload records `asset.upload`, the stored object sitting at the digest key `src: Core features`
- [ ] `C-CF-274` `contract` Every response carries an `X-Request-Id` header, so a refusal carries the request id `src: Core features`
- [ ] `C-CF-275` `constraint` Every audit event a request produced carries the same `X-Request-Id` value as the event `request_id`, recorded per write `src: Core features`
- [ ] `C-CF-276` `constraint` The first audit event `prev_hash` is sixty-four zeros, starting the audit chain `src: Core features`
- [ ] `C-CF-277` `constraint` Every later audit event `prev_hash` equals the previous event `hash`, so the chain links every event to the predecessor `src: Core features`
- [ ] `C-CF-278` `constraint` An update or delete of an audit row issued with the app's own database credentials is refused by the database itself, the audit rows never rewritten `src: Core features`
- [ ] `C-CF-279` `contract` `GET /api/v1/audit` returns audit events newest first, filtered by `market`, `actor`, `action`, `decision`, `limit` `src: Core features`
- [ ] `C-CF-280` `constraint` The owner reads every audit event; a legal reviewer reads only events in the markets the reader's grants cover, scoped reads `src: Core features`
- [ ] `C-CF-281` `constraint` Anyone else reading the audit log is refused with `role_not_permitted`, the audit reads scoped `src: Core features`
- [ ] `C-CF-282` `contract` The chain verification endpoint under the audit path, for the owner, walks the whole chain, returning `intact`, `events`, `head`, `first_broken_id`, reported by verification `src: Core features`
- [ ] `C-CF-283` `constraint` When a row is altered outside the app, `intact` is false with `first_broken_id` naming the first altered audit event `src: Core features`
- [ ] `C-CF-284` `contract` `POST /api/v1/audit/exports`, for the owner, returns the audit log as CSV with a header row, the export itself audited `src: Core features`
- [ ] `C-CF-285` `constraint` The audit export itself is recorded as `audit.export`, an audited export `src: Core features`
- [ ] `C-CF-286` `constraint` No audit event carries a password, a token or a password hash, recorded per write without credentials `src: Core features`
- [ ] `C-CF-287` `constraint` The studio audit page reports the audit chain as intact `src: Core features`
- [ ] `C-CF-288` `constraint` The studio audit log narrowed to decision deny shows the be-fr refusal to the editor with the reason `explicit_deny` `src: Core features`
- [ ] `C-CF-289` `contract` `/privacy/` is linked from the footer of every public page, the privacy page linking inventory `src: Core features`
- [ ] `C-CF-290` `constraint` The privacy page carries the personal data inventory, stating what the site records about a visitor, for how long `src: Core features`
- [ ] `C-CF-291` `constraint` The privacy page states no visitor account, no analytics, no advertising, no third parties receiving anything, so an erasure request has nothing to erase, request addresses kept on legitimate interest, among the public inventory states `src: Core features`
- [ ] `C-CF-292` `literal` The privacy page states request addresses kept in server logs for `30 days`, for security plus abuse prevention `src: Core features`
- [ ] `C-CF-293` `literal` The privacy page states the `drop_lang` language preference cookie is kept for `365 days` `src: Core features`
- [ ] `C-CF-294` `literal` The privacy page states staff audit records are kept for `7 years` `src: Core features`
- [ ] `C-CF-295` `constraint` The privacy page names each market residency region `eu-west`, `uk-south`, `eu-central` in the privacy inventory `src: Core features`
- [ ] `C-CF-296` `constraint` Every studio form rejects invalid input inline, writing nothing `src: Core features`
- [ ] `C-CF-297` `contract` The offending field is marked `aria-invalid="true"` with a message beside the field naming the field, invalid studio form fields marked inline `src: Core features`
- [ ] `C-CF-298` `constraint` An invalid studio form writes nothing: leaving the grant Reason empty marks the Reason field invalid with no grant row added `src: Core features`
- [ ] `C-CF-299` `constraint` At a phone's narrow viewport no public or studio page scrolls sideways `src: Core features`
- [ ] `C-CF-300` `constraint` At a narrow viewport every navigation target stays reachable: the menu button, the language switcher, the shop action on a drop page, never scrolling sideways `src: Core features`
- [ ] `C-CF-301` `constraint` At a narrow viewport the studio never scrolls sideways, every top navigation link staying reachable `src: Core features`
- [ ] `C-CF-302` `constraint` At a narrow viewport product cards sit two across, swatches become circles, keeping navigation reachable without scrolling sideways `src: Core features`
- [ ] `C-CF-303` `ui` A drop page leads with the shop action as the one primary action, with every other control visibly secondary `src: Core features`
- [ ] `C-CF-304` `ui` Pointing at a product card engages an overlay on the card plus an underline under the product title `src: Core features`
- [ ] `C-CF-305` `ui` Keyboard focus on the card's title link produces the same overlay plus underline as pointing at the card `src: Core features`
- [ ] `C-CF-306` `constraint` A studio market page leads with the next step the status allows, so the approved market's primary action reads Publish once both approvals are recorded `src: Core features`
- [ ] `C-CF-307` `constraint` A public page requests nothing from another host: typeface, styles, scripts plus images all come from the site `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `capability` The information architecture is small plus deep: a public drop page, the legal notice, a handful of studio screens behind sign in `src: User flow`
- [ ] `C-UF-02` `literal` `/` shows campaigns with a live market, the campaign index listing live campaigns `src: User flow`
- [ ] `C-UF-03` `literal` `/{campaign}/` redirects to the chosen live market, a temporary campaign root redirect `src: User flow`
- [ ] `C-UF-04` `literal` `/{campaign}/{market}/` is the drop page of a live market, declaring language, heading, landmarks `src: User flow`
- [ ] `C-UF-05` `literal` `/{campaign}/{market}/{legal_slug}/` is that market's legal notice, living under the market slug `src: User flow`
- [ ] `C-UF-06` `literal` `/privacy/` is the privacy page, linked from public pages, stating the inventory `src: User flow`
- [ ] `C-UF-07` `literal` `/lang` sets the language preference, then redirects to `to`, choosing a language cookie `src: User flow`
- [ ] `C-UF-08` `literal` `/media/{id}` serves a live image, so an image of a market not live is not public `src: User flow`
- [ ] `C-UF-09` `literal` `/sitemap.xml` is the sitemap, listing only live documents, with `/robots.txt` naming the sitemap for robots `src: User flow`
- [ ] `C-UF-10` `literal` `/studio/login` is staff sign-in, where an anonymous studio request is sent with next `src: User flow`
- [ ] `C-UF-11` `ui` `/studio/` shows the campaign list beside the selected campaign's markets, the studio campaign view `src: User flow`
- [ ] `C-UF-12` `literal` `/studio/campaigns/{campaign}/` is the same view with that campaign selected, listing the seven markets once signed in `src: User flow`
- [ ] `C-UF-13` `literal` `/studio/campaigns/{campaign}/markets/{market}/` is one market page for staff with a grant covering the market; outside the grants the studio market page reads as not found `src: User flow`
- [ ] `C-UF-14` `literal` `/studio/campaigns/{campaign}/markets/{market}/preview/` renders the market from current content for staff with a grant covering the market, the preview carrying noindex `src: User flow`
- [ ] `C-UF-15` `literal` `/studio/campaigns/{campaign}/products/` is products plus colourways, where the merchandiser sets a price row `src: User flow`
- [ ] `C-UF-16` `literal` `/studio/audit/` is the audit log with filters plus the chain state, for `owner` plus `legal`, narrowing the log by market `src: User flow`
- [ ] `C-UF-17` `literal` `/studio/grants/` is grants with issue plus revoke, for the `owner`, where a grant row is revoked `src: User flow`
- [ ] `C-UF-18` `constraint` Every page route ends in a slash; the same address without the slash answers a permanent redirect to the slash form, as an anonymous request to a slashless address is sent on `src: User flow`
- [ ] `C-UF-19` `constraint` `/sitemap.xml` plus `/robots.txt` take no trailing slash `src: User flow`
- [ ] `C-UF-20` `constraint` A visitor needs no account for anything public, so a public page answers without sign in, the campaign index listing live campaigns `src: User flow`
- [ ] `C-UF-21` `constraint` A visitor asking for a campaign root is sent to a live market by the language order: cookie, accept language, default `src: User flow`
- [ ] `C-UF-22` `constraint` A market not live, an unknown campaign, a legal slug not the market's own each answer not found `src: User flow`
- [ ] `C-UF-23` `constraint` Anyone not signed in asking for a studio page is sent to `/studio/login?next=<that path>`, the anonymous studio request carrying next `src: User flow`
- [ ] `C-UF-24` `constraint` After signing in the staff member lands on the next path, the Afterglow campaign view opening `src: User flow`
- [ ] `C-UF-25` `constraint` Signing out retires the token, landing on the sign-in page, so logout retires the token for any later call `src: User flow`
- [ ] `C-UF-26` `constraint` A staff member asking for a market page outside the grants gets the not-found page rather than a redirect `src: User flow`
- [ ] `C-UF-27` `constraint` A staff member with only an expired grant sees the not-found page for the de market, once the studio opens `src: User flow`
- [ ] `C-UF-28` `capability` Arrive in English: a browser preferring English opens `/afterglow/`, the address becomes `/afterglow/en/` with the capsule collection heading `src: User flow`
- [ ] `C-UF-29` `literal` The English heading reads `Afterglow, the Halden Sport x Tove Ardenne capsule collection`, the address becoming /afterglow/en/ `src: User flow`
- [ ] `C-UF-30` `capability` Opening the menu, the menu button reports expanded; the overlay lists The collection, Hi, I am Tove Ardenne, The RX2K story, Lookbook `src: User flow`
- [ ] `C-UF-31` `literal` Choosing `The collection` closes the menu with the collection section in view, the Graphic tee, Track jacket, RX2K cards showing `src: User flow`
- [ ] `C-UF-32` `capability` The graphic tee card offers `Pink` plus `White`; choosing White makes the card link carry `mc=7310043` with `hscamp:__drop-afterglow_p2` in the query `src: User flow`
- [ ] `C-UF-33` `literal` The English prices read `£17.00`, `£39.00`, `£79.00`, formatted in the market currency from minor units `src: User flow`
- [ ] `C-UF-34` `capability` Keep your place: from `/afterglow/fr/mentions-legales/` choosing `English` in the switcher lands on `/afterglow/en/legal-notice/` with the Legal notice heading `src: User flow`
- [ ] `C-UF-35` `capability` Opening `/afterglow/` again after choosing a language lands on the remembered market, although the browser prefers another language `src: User flow`
- [ ] `C-UF-36` `capability` Clear plus publish one market: `editor@example.com` opens Dusk Parade `be-nl`, submits, a toast confirms, the status reads `in_review` `src: User flow`
- [ ] `C-UF-37` `capability` `legal@example.com` approves Dusk Parade be-nl as legal, the approvals list showing a current legal approval `src: User flow`
- [ ] `C-UF-38` `capability` `owner@example.com` approves as owner, the status reads `approved`, then publishes; the status reads `published`, version 1 live `src: User flow`
- [ ] `C-UF-39` `literal` `/dusk-parade/be-nl/` then shows `Dusk Parade, lopen na zonsondergang`, with `/dusk-parade/de/` still answering as not found `src: User flow`
- [ ] `C-UF-40` `capability` The owner unpublishes Dusk Parade be-nl, so `/dusk-parade/be-nl/` answers as not found again `src: User flow`
- [ ] `C-UF-41` `capability` Meet a deny: `editor@example.com` changes an Afterglow `be-fr` translation; a toast names `explicit_deny`, the row keeping the value `src: User flow`
- [ ] `C-UF-42` `capability` Let the agency in: the owner adds a grant row on `/studio/grants/` for `editor3@example.com` as `editor`, expiring seven days from now, reason `Lookbook retouch`, the row appearing with the expiry `src: User flow`
- [ ] `C-UF-43` `capability` Leaving the grant reason empty marks the Reason field invalid, adding no grant row `src: User flow`
- [ ] `C-UF-44` `capability` `editor3@example.com` then opens the Afterglow Italian market page with the translations table `src: User flow`
- [ ] `C-UF-45` `capability` A pound is not a euro: `merchandiser@example.com` sets the graphic tee `en` price to `1700` with the currency `EUR`; the currency field is marked invalid, a toast names `currency_mismatch` `src: User flow`
- [ ] `C-UF-46` `constraint` After the refused currency the stored price is still `1700` `GBP`, the currency refused with nothing changed `src: User flow`
- [ ] `C-UF-47` `capability` Read the log: the owner narrows `/studio/audit/` to market `be-nl`, reading the Dusk Parade submit, both approvals, the publish, the unpublish, each with actor, time, hash `src: User flow`
- [ ] `C-UF-48` `capability` The translator opens Afterglow de with translations editing offered, no price control, no availability control, no publish control `src: User flow`
- [ ] `C-UF-49` `constraint` Every studio action shows a busy state on the pressed trigger, then ends in a toast `src: User flow`
- [ ] `C-UF-50` `constraint` A refusal toast names the `reason`, as the be-fr deny toast names explicit_deny `src: User flow`
- [ ] `C-UF-51` `constraint` An invalid grant row refusal appears as a toast, the Reason field marked invalid with no grant row added `src: User flow`
- [ ] `C-UF-52` `constraint` A success toast names what changed, as the saved grant row toast names the new editor3 grant `src: User flow`
- [ ] `C-UF-53` `constraint` A refusal never leaves a half-changed row on screen: the refused price row still shows 1700 GBP after the currency mismatch `src: User flow`
- [ ] `C-UF-54` `constraint` A preview with missing strings marks each one visibly as untranslated rather than showing a key `src: User flow`
- [ ] `C-UF-55` `constraint` The public page never waits behind a loading screen longer than three seconds, showing none at all with scripting off, the served document carrying copy without scripts `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The studio is an operational tool reading quiet, with flat plain panels free of the public page decoration `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The public page is a consumer editorial surface carrying atmosphere through stickers over flat grounds `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The studio north star: at a glance each market status is spelled as a word inside a status chip `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The page is a Memphis-revival scheme, loud on purpose, with black outlines around every sticker fill `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The default ground is a near-white neutral with a faint green cast, the hero sitting on the near-white ground `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The collection section sits on a near-white neutral with a pink cast, the collection cards on the pale pink-cast ground `src: UI/UX notes`
- [ ] `C-UX-07` `ui` The tagline plus collage passage plus the story section sit on a light muted magenta ground, the hero on the near-white ground `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Type, outlines, sticker keylines are near-black; each sticker wears a flat fill inside a black keyline `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The brand acid is a light vivid amber, the colour of the primary action, the wordmark fill, some sticker fills `src: UI/UX notes`
- [ ] `C-UX-10` `ui` On the drop page the Shop action is the only button-shaped control wearing the acid amber, the amber wordmark being a logo in the fixed bar `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A light vivid orange plus a light soft cyan are sticker fills only, never carrying copy: no heading or paragraph printed on an orange or cyan fill `src: UI/UX notes`
- [ ] `C-UX-12` `ui` A deep vivid teal is the accent; the overlay menu alone sits on a light muted teal ground where each focused menu item shows a ring `src: UI/UX notes`
- [ ] `C-UX-13` `constraint` A swatch colour is data, with the page painting the colourway slide in the stored swatch colour `src: UI/UX notes`
- [ ] `C-UX-14` `ui` In the studio every status also spells the status word, so a status is never shown by colour alone `src: UI/UX notes`
- [ ] `C-UX-15` `ui` In the studio a status in progress wears the acid amber, a finished status the deep teal, every status chip also spelling the word `src: UI/UX notes`
- [ ] `C-UX-16` `constraint` The drop page headings plus body set `Roboto Flex` as the first family, the pinned typeface `src: UI/UX notes`
- [ ] `C-UX-17` `literal` The page heading is `48px` on a `52px` line on the wide layout, the pinned heading sizes of the Roboto Flex typeface `src: UI/UX notes`
- [ ] `C-UX-18` `literal` Section headings are `64px` on `64px` wide, the pinned heading sizes `src: UI/UX notes`
- [ ] `C-UX-19` `literal` Body copy is `16px` on `24px`, alongside the pinned heading sizes of the typeface `src: UI/UX notes`
- [ ] `C-UX-20` `literal` Below the wide layout the page heading is `32px` on `36px`, section headings `36px` on `40px`, the pinned heading sizes `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Hard black keylines with flat fills rather than shadows; a sticker is never shaded with a gradient or a shadow `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Movement on the drop page follows scrolling, not a clock: the hero window opens in step with scrolling `src: UI/UX notes`
- [ ] `C-UX-23` `ui` The hero image starts as a small portrait window in the middle of the ground, opening outward as far as the reader has scrolled `src: UI/UX notes`
- [ ] `C-UX-24` `ui` Stickers fly up from below, some turning a quarter turn as the stickers land `src: UI/UX notes`
- [ ] `C-UX-25` `ui` The tagline is stored as a sentence, revealed letter by letter once the page runs `src: UI/UX notes`
- [ ] `C-UX-26` `ui` In the collage two photographs travel across the giant headline on opposite diagonals, partly covering the words `src: UI/UX notes`
- [ ] `C-UX-27` `ui` The footer list replays row by row, each numbered row animating into place in turn as the rows reach the viewport `src: UI/UX notes`
- [ ] `C-UX-28` `ui` In the studio a toast slides in from the top right, then fades away by itself `src: UI/UX notes`
- [ ] `C-UX-29` `ui` Cards arrive in a short cascade on the wide layout, the four product cards arriving one after another `src: UI/UX notes`
- [ ] `C-UX-30` `ui` Display product names in the footer list run full-bleed in a heavy condensed display type on the near-white ground `src: UI/UX notes`
- [ ] `C-UX-31` `constraint` The fixed bar keeps its place plus size as the page scrolls, never hiding, shrinking or inverting on scroll `src: UI/UX notes`
- [ ] `C-UX-32` `constraint` One colour mode, light: a dark preference changes nothing on the drop page `src: UI/UX notes`
- [ ] `C-UX-33` `constraint` With reduced motion requested every reveal sits at the end state, so reduced motion leaves no content invisible `src: UI/UX notes`
- [ ] `C-UX-34` `constraint` Every text plus ground pairing meets WCAG 2.2 AA contrast for the text size, the contrast bar against the ground `src: UI/UX notes`
- [ ] `C-UX-35` `ui` Keyboard navigation reaches every control with a visible focus ring drawn differently from hover, on every ground, the teal menu ground included `src: UI/UX notes`
- [ ] `C-UX-36` `constraint` Every swatch, the menu button, every icon-only control has a name: swatches are named buttons the keyboard operates `src: UI/UX notes`
- [ ] `C-UX-37` `ui` Focus on a swatch shows a ring around the swatch, drawn differently from the hover look `src: UI/UX notes`
- [ ] `C-UX-38` `ui` Below the wide layout the menu button keeps the icon, dropping the word Menu `src: UI/UX notes`
- [ ] `C-UX-39` `ui` The studio list pane stacks above the detail pane on a narrow viewport, the campaign list above the market rows `src: UI/UX notes`
- [ ] `C-UX-40` `constraint` Below the wide layout the shop action floats near the bottom of the narrow viewport, keeping navigation reachable `src: UI/UX notes`
- [ ] `C-UX-41` `constraint` The layout holds at every width with no horizontal overflow: a narrow viewport never scrolls sideways `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `constraint` Two copies of the shop action exist in the document, the bar copy shown on the wide layout, the floating copy shown at a narrow viewport, each hidden at the other width `src: Front-end specification`
- [ ] `C-FE-02` `constraint` The overlay menu becomes a single column at a narrow viewport, the four anchors stacked one below another `src: Front-end specification`
- [ ] `C-FE-03` `ui` Hero: the hero image starts in a small portrait window, the window opening outward with scroll `src: Front-end specification`
- [ ] `C-FE-04` `ui` Tagline: `tagline.one` with a letter-by-letter reveal `src: Front-end specification`
- [ ] `C-FE-05` `ui` Collage: `collage.headline` behind two travelling photographs crossing the headline on opposite diagonals `src: Front-end specification`
- [ ] `C-FE-06` `ui` Collection `#collection`: the pale pink-cast ground holding `collection.heading` above the cards `src: Front-end specification`
- [ ] `C-FE-07` `ui` Artist `#ardenne`: the near-white ground with an orange sun form, the artist heading plus bio `src: Front-end specification`
- [ ] `C-FE-08` `ui` Story `#rx2k`: the muted magenta ground again, the story heading plus body `src: Front-end specification`
- [ ] `C-FE-09` `contract` Lookbook `#lookbook`: `lookbook.heading` plus the shared lookbook image carrying `lookbook.alt` as alternative text in the served document `src: Front-end specification`
- [ ] `C-FE-10` `literal` Footer list: every available product full-bleed, `[01]` onward at the left, the price at the right, rows naming T-shirt graphique through RX2K `src: Front-end specification`
- [ ] `C-FE-11` `ui` Legal footer on the near-white ground ends the scroll after the footer list `src: Front-end specification`
- [ ] `C-FE-12` `constraint` A campaign with fewer sections renders only its own, so the published Dusk Parade be-nl drop page shows the Dusk Parade heading `src: Front-end specification`
- [ ] `C-FE-13` `contract` The Halden Sport wordmark in the centre links to `https://halden.example.com/` in a new tab with the `aria-label` `Halden Sport`, isolated with noopener noreferrer `src: Front-end specification`
- [ ] `C-FE-14` `ui` The wordmark is filled with the acid amber over a black outline shape in the fixed bar `src: Front-end specification`
- [ ] `C-FE-15` `ui` The bar stays legible over every ground as the page scrolls under the fixed bar `src: Front-end specification`
- [ ] `C-FE-16` `ui` Pointing at a swatch grows the swatch on the card `src: Front-end specification`
- [ ] `C-FE-17` `constraint` Resting shows the first colourway with the swatch pressed; activating a swatch moves the slider, pressed swatches the keyboard operates `src: Front-end specification`
- [ ] `C-FE-18` `ui` The overlay menu is a full-viewport overlay on the light muted teal ground `src: Front-end specification`
- [ ] `C-FE-19` `ui` On the wide layout the overlay menu lays the four section names out four across as a grid `src: Front-end specification`
- [ ] `C-FE-20` `ui` Each overlay menu item carries a strip of tape as decoration `src: Front-end specification`
- [ ] `C-FE-21` `ui` The studio top navigation reads Campaigns, Audit plus, for the owner only, Grants, with the signed-in email plus Sign out `src: Front-end specification`
- [ ] `C-FE-22` `ui` `/studio/` is a split view: the campaign list in a narrow pane at the left, the seven markets of the selected campaign at the right `src: Front-end specification`
- [ ] `C-FE-23` `ui` Each market row carries the status word, a live mark, the current approvals `src: Front-end specification`
- [ ] `C-FE-24` `ui` A market page stacks the status plus current approvals above every table `src: Front-end specification`
- [ ] `C-FE-25` `ui` Below the top block come the translations table, then the availability plus price table, then the artifact list with rollback `src: Front-end specification`
- [ ] `C-FE-26` `ui` A new string is added as a new editable row inside the translations table, not in a dialog or on another page `src: Front-end specification`
- [ ] `C-FE-27` `ui` A new row is started by a button labelled `Add` inside the table, the page address staying the same `src: Front-end specification`
- [ ] `C-FE-28` `constraint` A new grant row is kept with a button labelled `Save`; the grant row fields `Email`, `Expires`, `Reason` are labelled, the invalid Reason field marked inline `src: Front-end specification`
- [ ] `C-FE-29` `constraint` The sign-in form fields are labelled `Email` plus `Password`, a studio form marking an invalid field inline `src: Front-end specification`
- [ ] `C-FE-30` `constraint` The sign-in form button reads `Sign in`; the grant row carries labelled `Role` plus `Market` fields, a studio form marking an invalid field inline `src: Front-end specification`
- [ ] `C-FE-31` `literal` A price row's fields are labelled `Price` plus `Currency`, where a EUR currency on en is marked invalid `src: Front-end specification`
- [ ] `C-FE-32` `ui` Every studio outcome is a toast sliding in at the top right, fading away by itself `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` Every route answers with a complete document rendered on the server, so the served document carries copy, links, prices plus the switcher without scripts `src: Technical requirements`
- [ ] `C-TR-02` `constraint` No page is an empty shell filling itself from a second request; the first paint is the whole served document with copy, links, prices `src: Technical requirements`
- [ ] `C-TR-03` `constraint` The drop page motion is a plain script over a document reading correctly without the script, so reduced motion leaves no content invisible `src: Technical requirements`
- [ ] `C-TR-04` `contract` The JSON API is served under `/api` on the same origin as the pages, so `GET /api/health` answers once the app is ready `src: Technical requirements`
- [ ] `C-TR-05` `constraint` Images plus artifacts live in MinIO from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, an upload stored at the digest key in the object store `src: Technical requirements`
- [ ] `C-TR-06` `constraint` The bucket already exists, private, so an anonymous read of the bucket is refused `src: Technical requirements`
- [ ] `C-TR-07` `constraint` Studio pages keep the token in a cookie scripts cannot read; an anonymous studio request is sent to sign in with next `src: Technical requirements`
- [ ] `C-TR-08` `constraint` A studio page requested with the bearer token in the `Authorization` header is served as for the signed-in cookie, so the preview renders for the product owner `src: Technical requirements`
- [ ] `C-TR-09` `contract` `GET /api/health` returns `200` once the app reaches PostgreSQL plus the bucket, the health route answering once ready `src: Technical requirements`
- [ ] `C-TR-10` `contract` Every response carries an `X-Request-Id` header, generated when absent, the same value in every refusal body `src: Technical requirements`
- [ ] `C-TR-11` `literal` Every response carries `X-Content-Type-Options: nosniff` among the security headers `src: Technical requirements`
- [ ] `C-TR-12` `literal` Every response carries `Referrer-Policy: strict-origin-when-cross-origin` among the security headers `src: Technical requirements`
- [ ] `C-TR-13` `constraint` Every response carries a `Permissions-Policy` denying camera, microphone, geolocation, payment, among the security headers riding on every response `src: Technical requirements`
- [ ] `C-TR-14` `constraint` The `Content-Security-Policy` script source list carries no `unsafe-inline`, a security header riding on every response `src: Technical requirements`
- [ ] `C-TR-15` `literal` The content security policy sets `frame-ancestors 'none'`, `base-uri 'self'`, `form-action 'self'` on every response header `src: Technical requirements`
- [ ] `C-TR-16` `literal` A live drop page plus a legal notice carry `Cache-Control: public, max-age=60, stale-while-revalidate=86400, stale-if-error=604800`, the shared cache headers of live pages `src: Technical requirements`
- [ ] `C-TR-17` `constraint` Live pages carry `Vary: Accept-Encoding`, never varying on `Cookie`, since nothing on the live pages depends on the visitor `src: Technical requirements`
- [ ] `C-TR-18` `literal` A campaign root answers the temporary redirect with `Cache-Control: private, no-store` plus `Vary: Accept-Language, Cookie`, a private root redirect varying by language `src: Technical requirements`
- [ ] `C-TR-19` `constraint` The typeface is served by the app itself, so the public page requests no font from another host `src: Technical requirements`
- [ ] `C-TR-20` `contract` Every `POST` accepts an `Idempotency-Key` header; a repeated key from the same principal within 24 hours returns the first response, so a repeated idempotency key publishes once `src: Technical requirements`
- [ ] `C-TR-21` `constraint` Money is integer minor units plus an uppercase ISO 4217 code, stored, returned, compared in those pinned forms `src: Technical requirements`
- [ ] `C-TR-22` `constraint` A displayed price is formatted from the minor units at render time, in the market currency `src: Technical requirements`
- [ ] `C-TR-23` `constraint` Time is UTC everywhere, returned as ISO 8601 with a `Z`, the pinned time form `src: Technical requirements`
- [ ] `C-TR-24` `constraint` No document, script, stylesheet or JSON the browser downloads carries the database address, the object store keys or another token: no secret reaches the browser `src: Technical requirements`
- [ ] `C-TR-25` `constraint` Seeding is idempotent: the seeded markets hold the locale matrix once, with no duplicate campaign, product or string rows `src: Technical requirements`
- [ ] `C-TR-26` `literal` The seeded Dusk Parade campaign holds default locale `be-nl`, no embargo, one product `483101` with colourway `7311550` in slot `p1`, available in `be-nl` plus `de` at `6500` `EUR`, sections `hero`, `collection`, `footer_list`, `legal_footer`, matching the seeded locale matrix `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026`, which signs in; a wrong password refused alike `src: Data model`
- [ ] `C-DM-02` `constraint` The seeded password is hashed as normal, the stored password hashes never holding the literal `src: Data model`
- [ ] `C-DM-03` `data` `markets` holds `code`, `hreflang`, `display_name`, `currency`, `locale_tag`, `commerce_host`, `commerce_locale_segment`, `legal_page_slug`, `data_region`, `sort_order`, `active`, the source of every market link template `src: Data model`
- [ ] `C-DM-04` `literal` The seeded markets hold the locale matrix with the seven `locale_tag` values `fr-FR`, `en-GB`, `es-ES`, `de-DE`, `nl-BE`, `fr-BE` plus the Italian tag for Italy `src: Data model`
- [ ] `C-DM-05` `literal` The seeded markets hold the locale matrix `data_region` values `eu-west`, `uk-south`, `eu-west`, `eu-west`, `eu-central`, `eu-west`, `eu-west` in market order `src: Data model`
- [ ] `C-DM-06` `constraint` There is no URL column in `markets` or any other table, so no storefront url is stored `src: Data model`
- [ ] `C-DM-07` `data` `principals` holds `id`, `email` (unique, lowercase), `display_name`, `password_hash`, `status`, `created_at`, passwords stored hashed `src: Data model`
- [ ] `C-DM-08` `data` `sessions` holds `id`, `principal_id`, `token_hash` (unique), `issued_at`, `expires_at`, `revoked_at`, so logout retires the token `src: Data model`
- [ ] `C-DM-09` `data` `grants` holds `id`, `principal_id`, `role`, `market_code`, `effect`, `expires_at`, `granted_by`, `reason`, `created_at`, `revoked_at`, so a revoked grant stops the next request `src: Data model`
- [ ] `C-DM-10` `data` `campaigns` holds `id`, `slug`, `name`, `default_locale`, `attribution_prefix`, `attribution_slug`, `embargo_at`, `created_by`, `created_at`, the embargo refusing an early publish `src: Data model`
- [ ] `C-DM-11` `data` `campaign_markets` holds one row per campaign plus market with `status`, `content_hash`, `live_version`, `hero_asset_id`, `product_order`, `published_at`, `published_by`, matching the seeded market states `src: Data model`
- [ ] `C-DM-12` `constraint` Creating a campaign creates all seven campaign market rows as draft, so a new campaign starts with seven draft markets `src: Data model`
- [ ] `C-DM-13` `data` `page_sections` holds `id`, `campaign_id`, `kind`, `anchor`, `sort_order`; the anchor is unique within the campaign, so sections follow the campaign order with named anchors `src: Data model`
- [ ] `C-DM-14` `data` `products` holds `id`, `campaign_id`, `commerce_product_id` unique within the campaign, `sort_order`, `created_at`, product identifiers validated `src: Data model`
- [ ] `C-DM-15` `data` `colourways` holds `id`, `product_id`, `model_code`, `swatch_hex`, `attribution_slot` unique within the campaign, `sort_order`, slots assigned by the server `src: Data model`
- [ ] `C-DM-16` `data` `product_markets` holds `product_id`, `market_code`, `available`, `price_minor`, `price_currency`, prices refused in another currency `src: Data model`
- [ ] `C-DM-17` `constraint` A stored price currency always equals the market currency, a price never existing without currency, so another currency is refused with nothing changed `src: Data model`
- [ ] `C-DM-18` `data` `translatable_strings` holds `id`, `campaign_id`, `key` unique within the campaign, `context`, `max_length`, so a translation longer than the budget is rejected `src: Data model`
- [ ] `C-DM-19` `data` `translations` holds one row per string plus market with `string_id`, `market_code`, `value`, `status`, `translated_by`, `updated_at`; no row means missing, marked untranslated in the preview `src: Data model`
- [ ] `C-DM-20` `data` `assets` holds `id`, `campaign_id`, `kind`, `object_key` unique, `content_type`, `byte_size`, `checksum`, `market_code`, `created_by`, `created_at`, never the image bytes, the object stored at the digest key `src: Data model`
- [ ] `C-DM-21` `data` `approvals` holds `id`, `campaign_id`, `market_code`, `kind`, `decision`, `decided_by`, `decided_at`, `content_hash`, `superseded`, `comment`, approvals binding the content hash `src: Data model`
- [ ] `C-DM-22` `constraint` There is never more than one current approval of a kind for a market plus content hash, so an edit supersedes approvals bound to the hash `src: Data model`
- [ ] `C-DM-23` `data` `published_artifacts` holds `id`, `campaign_id`, `market_code`, `version`, `object_key`, `content_hash`, `published_by`, `published_at`; versions count 1, 2, 3, never repeating, each publish storing a versioned artifact `src: Data model`
- [ ] `C-DM-24` `constraint` The database refuses an update or delete of `audit_events` issued with the application's own credentials, the app role unable to rewrite audit rows `src: Data model`
- [ ] `C-DM-25` `data` `idempotency_keys` holds `key`, `principal_id`, `endpoint`, `status_code`, `response_body`, `created_at`, one row per key, principal, endpoint, so a repeated idempotency key publishes once `src: Data model`
- [ ] `C-DM-26` `constraint` Every storefront link is derived rather than stored from the market template `src: Data model`
- [ ] `C-DM-27` `constraint` `content_hash` is stored for reading yet always recomputed on write, never accepted from a caller, ignoring status changes plus other markets `src: Data model`
- [ ] `C-DM-28` `literal` Afterglow has the slug `afterglow`, the default locale `fr`, the attribution prefix `hscamp:__drop-`, the attribution slug `afterglow`, no embargo, carried by every market link as attribution `src: Data model`
- [ ] `C-DM-29` `literal` Afterglow sections follow the campaign order with the anchored sections `collection`, `artist` (anchor `ardenne`), `story` (anchor `rx2k`), `lookbook` in that order, each named by the heading `src: Data model`
- [ ] `C-DM-30` `data` The Afterglow media inventory is PNG images: a hero image for each of the seven markets plus four shared images, the lookbook image carrying alternative text in the served document `src: Data model`
- [ ] `C-DM-31` `data` The seeded media holds a hero image object for each of the seven markets plus four shared image objects, each at a digest key, matching the seed `src: Data model`
- [ ] `C-DM-32` `literal` The seeded deny grant is the `editor@example.com` deny on `be-fr`, matching the seeded grants `src: Data model`
- [ ] `C-DM-33` `data` The `fr` plus `en` markets each have artifact version 1 live; `be-fr` has version 1 stored, not live, matching the seeded market states `src: Data model`
- [ ] `C-DM-34` `literal` Afterglow `fr` copy: `hero.title` Afterglow, la collection capsule Halden Sport x Tove Ardenne; `meta.title` Afterglow, la capsule Halden Sport x Tove Ardenne, matching the seeded copy deck of every market `src: Data model`
- [ ] `C-DM-35` `literal` Afterglow `meta.description` reads Quatre pièces rétro dessinées avec Tove Ardenne, en édition limitée. in `fr`, Four retro pieces designed with Tove Ardenne, in a limited drop. in `en`, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-36` `literal` Afterglow `en` copy: `tagline.one` Right beside you since 1976; `collage.headline` Dive into the most vibrant decade there ever was, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-37` `literal` Afterglow `en` copy: `artist.bio` An illustrator born in Lyon, I draw sport the way you remember a school playground; `story.body` A 1999 running shoe, redrawn line for line from its original plans, the seeded copy deck `src: Data model`
- [ ] `C-DM-38` `literal` Afterglow `fr` copy: `tagline.one` À vos côtés depuis 1976; `collage.headline` Plongez au cœur de la décennie la plus vibrante qui soit, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-39` `literal` Afterglow `fr` copy: `menu.label` Menu, `menu.close` Fermer, `shop.cta` Boutique, `lang.label` Choisir la langue, `newtab.suffix` ouvre la boutique dans un nouvel onglet, `legal.title` Mentions légales, the seeded copy deck of every market `src: Data model`
- [ ] `C-DM-40` `literal` Afterglow `en` copy: `menu.label` Menu, `menu.close` Close, `shop.cta` Shop, `lang.label` Choose language, `newtab.suffix` opens the shop in a new tab, `legal.title` Legal notice, the seeded copy deck of every market `src: Data model`
- [ ] `C-DM-41` `literal` Afterglow `fr` plus `en` `lookbook.alt`: Deux coureurs en veste pervenche sur une piste au coucher du soleil / Two runners in periwinkle jackets on a track at sunset, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-42` `literal` Afterglow `legal.body` names Halden Sport SA at `12 rue des Tanneurs, 59000 Lille` with the design credit Parallel Studio, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-43` `constraint` The seeded markets hold the string budgets: `max_length` is 70 for `meta.title`, 160 for `meta.description`, 90 for `hero.title`, 12 for `menu.label` plus `menu.close`, 16 for `shop.cta`, 32 for `lang.label`, 600 for `artist.bio` plus `story.body` `src: Data model`
- [ ] `C-DM-44` `literal` Afterglow `lang.label` in the other markets: Elegir idioma (`es`), Sprache wählen (`de`), Kies je taal (`be-nl`), Choisir la langue (`be-fr`), plus Scegli la lingua for the Italian market, matching the seeded copy deck of every market `src: Data model`
- [ ] `C-DM-45` `literal` Afterglow `shop.cta` in the other markets: Tienda, Shop, Winkel, Boutique, plus Negozio for the Italian market, matching the seeded copy deck of every market `src: Data model`
- [ ] `C-DM-46` `literal` Afterglow `menu.label` plus `menu.close` in the other markets: Menú / Cerrar, Menü / Schließen, Menu / Sluiten, Menu / Fermer, plus Menu / Chiudi for Italy, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-47` `literal` Afterglow `newtab.suffix` in the other markets: abre la tienda en una pestaña nueva, öffnet den Shop in einem neuen Tab, opent de winkel in een nieuw tabblad, plus apre il negozio in una nuova scheda for Italy, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-48` `literal` Afterglow `legal.title` in the other markets: Aviso legal, Impressum, Wettelijke vermeldingen, Mentions légales, plus Note legali for Italy, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-49` `literal` Afterglow `hero.title` in `de` is Afterglow, die Capsule-Kollektion von Halden Sport x Tove Ardenne, in `be-nl` Afterglow, de capsulecollectie Halden Sport x Tove Ardenne, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-50` `literal` Afterglow `hero.title` in `es` is Afterglow, la colección cápsula Halden Sport x Tove Ardenne, with the Italian market holding Afterglow, la collezione capsule Halden Sport x Tove Ardenne, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-51` `constraint` `be-fr` carries the French values, so the be-fr `shop.cta` Boutique survives the editor write refused because the deny grant wins over the permit `src: Data model`
- [ ] `C-DM-52` `literal` Dusk Parade `be-nl` copy: `meta.title` Dusk Parade, de avondcollectie van Halden Sport; `hero.title` Dusk Parade, lopen na zonsondergang; `product.483101.name` Nachtloper windjack; `colour.7311550.name` Diepgrijs, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-53` `literal` Dusk Parade `de` copy: `meta.title` Dusk Parade, die Abendkollektion von Halden Sport; `hero.title` Dusk Parade, Laufen nach Sonnenuntergang; `product.483101.name` Nachtläufer Windjacke; `colour.7311550.name` Tiefgrau, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-54` `literal` Dusk Parade `be-nl` plus `de` copy: `collection.heading` De collectie / Die Kollektion; `shop.cta` Winkel / Shop; `lang.label` Kies je taal / Sprache wählen; `legal.title` Wettelijke vermeldingen / Impressum, matching the seeded copy deck `src: Data model`
- [ ] `C-DM-55` `constraint` The seeded audit log begins with the events that built the seed, the audit chain linking every event to the predecessor `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One retailer with no tenancy: every staff member works in the same campaigns, bounded by grants, a write outside the editor grants refused `src: Constraints`
- [ ] `C-CN-02` `constraint` No visitor accounts: signup does not exist, the staff directory answering the owner only `src: Constraints`
- [ ] `C-CN-03` `constraint` The page never claims availability beyond the market's own flag, so an unavailable product has no card `src: Constraints`
- [ ] `C-CN-04` `constraint` No product photography: a colourway slide is painted in the stored swatch `src: Constraints`
- [ ] `C-CN-05` `constraint` No external network call at runtime: a public page requests nothing from another host `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The translations list carries one row per stored translation, a missing string having no row, as the seeded copy deck of every market shows `src: Deployment contract`
- [ ] `C-DC-02` `contract` A product market write accepts any of `available`, or `price_minor` with `price_currency`, so an available product can have no price in the preview `src: Deployment contract`
- [ ] `C-DC-03` `contract` A product market write leaving a field out keeps the stored value, so writing `available` alone keeps the market price before the If-Match market change `src: Deployment contract`
- [ ] `C-DC-04` `contract` `audit_events.id` is an integer increasing with every event, the audit chain linking every event to the predecessor in id order `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app is reachable at `APP_PUBLIC_URL`, the health route answering once ready `src: Deployment contract`
- [ ] `C-DC-06` `contract` The HTTP API is served on the same origin under the `/api` prefix, so `GET /api/health` answers once ready `src: Deployment contract`
- [ ] `C-DC-07` `contract` Every list endpoint returns a top-level JSON array; bearer auth rides on everything under `/api/v1` except login plus the public reads, an anonymous refusal carrying the reason plus request id `src: Deployment contract`
- [ ] `C-DC-08` `contract` An invalid or unauthorized call is rejected as a client error with the refusal body, never a `5xx`, carrying the reason plus request id `src: Deployment contract`
- [ ] `C-DC-09` `contract` `GET /api/v1/campaigns/{slug}/markets/{market}` returns `market_code`, `status`, `content_hash`, `live_version`, `hero_asset_id`, `product_order`, `approvals`, matching the seeded market states plus approvals `src: Deployment contract`
- [ ] `C-DC-10` `contract` `GET /api/v1/campaigns/{slug}/markets/{market}/render` returns the render payload of current content, every storefront link derived from the market template `src: Deployment contract`
- [ ] `C-DC-11` `contract` `GET /api/v1/public/campaigns/{slug}/markets/{market}` returns the live artifact payload with `version`, not found when the market is not live `src: Deployment contract`
- [ ] `C-DC-12` `contract` `GET /api/v1/public/campaigns/{slug}/markets` returns live markets with `market_code`, `hreflang`, `path`, so approving plus publishing one market lists only that market `src: Deployment contract`
- [ ] `C-DC-13` `contract` The render payload carries `campaign`, `market`, `content_hash`, `version`, `strings`, `sections`, `shop_url`, `hero_image`, `products` with `price_display` plus `colourways` each with `url`, the shop action leading to the market collection `src: Deployment contract`
- [ ] `C-DC-14` `contract` `GET /api/v1/campaigns/{slug}/products` returns products with `colourways` plus `markets` holding `price_minor`, `price_currency`, prices refused in another currency `src: Deployment contract`
- [ ] `C-DC-15` `contract` `PUT /api/v1/campaigns/{slug}/translations/{market}/{key}` takes `value` plus `status`, a translation longer than the budget rejected `src: Deployment contract`
- [ ] `C-DC-16` `contract` `POST /api/v1/campaigns` takes `slug`, `name`, `default_locale`, `attribution_slug`, optional `embargo_at`, a new campaign starting with eleven strings plus seven draft markets `src: Deployment contract`
- [ ] `C-DC-17` `contract` `PATCH /api/v1/campaigns/{slug}` takes `name` plus `embargo_at`, so publish is refused before the embargo `src: Deployment contract`
- [ ] `C-DC-18` `contract` `GET /api/v1/campaigns/{slug}/markets/{market}/artifacts` lists each `version`, `object_key`, `content_hash`, `published_by`, `published_at`, `live`, each publish storing a versioned artifact `src: Deployment contract`
- [ ] `C-DC-19` `contract` `GET /api/v1/campaigns/{slug}/strings` lists `key`, `context`, `max_length`, a created product adding the product name strings `src: Deployment contract`
- [ ] `C-DC-20` `contract` `POST /api/v1/products/{id}/colourways` takes `model_code` plus `swatch_hex`, the slot assigned by the server `src: Deployment contract`
- [ ] `C-DC-21` `contract` `GET /api/v1/grants` lists `id`, `email`, `role`, `market_code`, `effect`, `expires_at`, `reason`, `revoked_at`, so a revoked grant shows `revoked_at` once the grant stops the next request `src: Deployment contract`
- [ ] `C-DC-22` `constraint` PostgreSQL plus MinIO are the facts: image bytes on the app container disk or in a database column violate the contract, the upload stored only at the digest key in the object store `src: Deployment contract`
- [ ] `C-DC-23` `constraint` A storefront address stored in a product row violates the contract, so no storefront url is accepted or stored `src: Deployment contract`
- [ ] `C-DC-24` `constraint` An audit log the app could quietly rewrite violates the contract: the database refuses the app role rewriting audit rows `src: Deployment contract`
- [ ] `C-DC-25` `constraint` A grant checked once at sign-in plus cached in the token violates the contract, since an expired grant is refused, yet the token authenticates `src: Deployment contract`
- [ ] `C-DC-26` `constraint` An approval staying current after an edit violates the contract: an edit supersedes approvals bound to the content hash `src: Deployment contract`
- [ ] `C-DC-27` `constraint` An artifact kept in memory violates the contract: each publish stores a versioned artifact object in the store `src: Deployment contract`

## Pinned literals

| Value | Meaning | Item | Where |
|---|---|---|---|
| `Afterglow` | value pinned by C-OV-15 | C-OV-15 | Overview |
| `Dusk Parade` | value pinned by C-OV-15 | C-OV-15 | Overview |
| `deku-demo-pw-2026` | value pinned by C-RL-22 | C-RL-22 | User roles |
| `owner@example.com` | value pinned by C-RL-23 | C-RL-23 | User roles |
| `owner` | value pinned by C-RL-23 | C-RL-23 | User roles |
| `editor@example.com` | value pinned by C-RL-24 | C-RL-24 | User roles |
| `editor` | value pinned by C-RL-24 | C-RL-24 | User roles |
| `fr` | value pinned by C-RL-24 | C-RL-24 | User roles |
| `be-nl` | value pinned by C-RL-24 | C-RL-24 | User roles |
| `be-fr` | value pinned by C-RL-24 | C-RL-24 | User roles |
| `editor2@example.com` | value pinned by C-RL-26 | C-RL-26 | User roles |
| `de` | value pinned by C-RL-26 | C-RL-26 | User roles |
| `Parallel Studio design pass` | value pinned by C-RL-26 | C-RL-26 | User roles |
| `editor3@example.com` | value pinned by C-RL-27 | C-RL-27 | User roles |
| `translator@example.com` | value pinned by C-RL-28 | C-RL-28 | User roles |
| `es` | value pinned by C-RL-28 | C-RL-28 | User roles |
| `legal@example.com` | value pinned by C-RL-28 | C-RL-28 | User roles |
| `en` | value pinned by C-RL-28 | C-RL-28 | User roles |
| `translator` | value pinned by C-RL-29 | C-RL-29 | User roles |
| `legal` | value pinned by C-RL-30 | C-RL-30 | User roles |
| `legal2@example.com` | value pinned by C-RL-31 | C-RL-31 | User roles |
| `merchandiser@example.com` | value pinned by C-RL-32 | C-RL-32 | User roles |
| `merchandiser` | value pinned by C-RL-32 | C-RL-32 | User roles |
| `Sign-in failed` | value pinned by C-CF-06 | C-CF-06 | Core features |
| `/afterglow/fr/` | value pinned by C-CF-15 | C-CF-15 | Core features |
| `collection` | value pinned by C-CF-23 | C-CF-23 | Core features |
| `ardenne` | value pinned by C-CF-23 | C-CF-23 | Core features |
| `rx2k` | value pinned by C-CF-23 | C-CF-23 | Core features |
| `lookbook` | value pinned by C-CF-23 | C-CF-23 | Core features |
| `menu.label` | value pinned by C-CF-31 | C-CF-31 | Core features |
| `menu.close` | value pinned by C-CF-31 | C-CF-31 | Core features |
| `[01]` | value pinned by C-CF-34 | C-CF-34 | Core features |
| `[02]` | value pinned by C-CF-34 | C-CF-34 | Core features |
| `/afterglow/fr/mentions-legales/` | value pinned by C-CF-41 | C-CF-41 | Core features |
| `legal.title` | value pinned by C-CF-41 | C-CF-41 | Core features |
| `legal.body` | value pinned by C-CF-41 | C-CF-41 | Core features |
| `fr-FR` | value pinned by C-CF-46 | C-CF-46 | Core features |
| `Français` | value pinned by C-CF-46 | C-CF-46 | Core features |
| `EUR` | value pinned by C-CF-46 | C-CF-46 | Core features |
| `shop-fr.example.com` | value pinned by C-CF-46 | C-CF-46 | Core features |
| `mentions-legales` | value pinned by C-CF-46 | C-CF-46 | Core features |
| `English` | value pinned by C-CF-47 | C-CF-47 | Core features |
| `GBP` | value pinned by C-CF-47 | C-CF-47 | Core features |
| `shop-uk.example.com` | value pinned by C-CF-47 | C-CF-47 | Core features |
| `legal-notice` | value pinned by C-CF-47 | C-CF-47 | Core features |
| `Italiano` | value pinned by C-CF-48 | C-CF-48 | Core features |
| `note-legali` | value pinned by C-CF-48 | C-CF-48 | Core features |
| `Español` | value pinned by C-CF-49 | C-CF-49 | Core features |
| `shop-es.example.com` | value pinned by C-CF-49 | C-CF-49 | Core features |
| `/es` | value pinned by C-CF-49 | C-CF-49 | Core features |
| `aviso-legal` | value pinned by C-CF-49 | C-CF-49 | Core features |
| `Deutsch` | value pinned by C-CF-50 | C-CF-50 | Core features |
| `shop-de.example.com` | value pinned by C-CF-50 | C-CF-50 | Core features |
| `impressum` | value pinned by C-CF-50 | C-CF-50 | Core features |
| `nl` | value pinned by C-CF-51 | C-CF-51 | Core features |
| `Nederlands (België)` | value pinned by C-CF-51 | C-CF-51 | Core features |
| `shop-be.example.com` | value pinned by C-CF-51 | C-CF-51 | Core features |
| `/nl` | value pinned by C-CF-51 | C-CF-51 | Core features |
| `wettelijke-vermeldingen` | value pinned by C-CF-51 | C-CF-51 | Core features |
| `fr-BE` | value pinned by C-CF-52 | C-CF-52 | Core features |
| `Français (Belgique)` | value pinned by C-CF-52 | C-CF-52 | Core features |
| `/fr` | value pinned by C-CF-52 | C-CF-52 | Core features |
| `/lang?to=<path>` | value pinned by C-CF-63 | C-CF-63 | Core features |
| `drop_lang` | value pinned by C-CF-63 | C-CF-63 | Core features |
| `482913` | value pinned by C-CF-83 | C-CF-83 | Core features |
| `7310042` | value pinned by C-CF-83 | C-CF-83 | Core features |
| `p1` | value pinned by C-CF-83 | C-CF-83 | Core features |
| `mc=7310042` | value pinned by C-CF-83 | C-CF-83 | Core features |
| `https://shop-fr.example.com/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` | value pinned by C-CF-84 | C-CF-84 | Core features |
| `https://shop-es.example.com/es/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` | value pinned by C-CF-85 | C-CF-85 | Core features |
| `https://shop-be.example.com/nl/p/*/_/R-p-482913?mc=7310042&hscamp=hscamp:__drop-afterglow_p1&type=hscamp` | value pinned by C-CF-86 | C-CF-86 | Core features |
| `https://` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `/c/` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `hscamp` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `hscamp:__drop-afterglow` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `type` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `Blanc` | value pinned by C-CF-96 | C-CF-96 | Core features |
| `White` | value pinned by C-CF-96 | C-CF-96 | Core features |
| `2000` | value pinned by C-CF-103 | C-CF-103 | Core features |
| `20,00 €` | value pinned by C-CF-103 | C-CF-103 | Core features |
| `€ 20,00` | value pinned by C-CF-104 | C-CF-104 | Core features |
| `1700` | value pinned by C-CF-105 | C-CF-105 | Core features |
| `£17.00` | value pinned by C-CF-105 | C-CF-105 | Core features |
| `7310043` | value pinned by C-CF-113 | C-CF-113 | Core features |
| `p2` | value pinned by C-CF-113 | C-CF-113 | Core features |
| `482927` | value pinned by C-CF-114 | C-CF-114 | Core features |
| `7310118` | value pinned by C-CF-114 | C-CF-114 | Core features |
| `p3` | value pinned by C-CF-114 | C-CF-114 | Core features |
| `7310119` | value pinned by C-CF-114 | C-CF-114 | Core features |
| `p4` | value pinned by C-CF-114 | C-CF-114 | Core features |
| `482940` | value pinned by C-CF-115 | C-CF-115 | Core features |
| `7310205` | value pinned by C-CF-115 | C-CF-115 | Core features |
| `p5` | value pinned by C-CF-115 | C-CF-115 | Core features |
| `482956` | value pinned by C-CF-116 | C-CF-116 | Core features |
| `7310377` | value pinned by C-CF-116 | C-CF-116 | Core features |
| `p6` | value pinned by C-CF-116 | C-CF-116 | Core features |
| `7310378` | value pinned by C-CF-116 | C-CF-116 | Core features |
| `p7` | value pinned by C-CF-116 | C-CF-116 | Core features |
| `4500` | value pinned by C-CF-117 | C-CF-117 | Core features |
| `3500` | value pinned by C-CF-117 | C-CF-117 | Core features |
| `9000` | value pinned by C-CF-117 | C-CF-117 | Core features |
| `3900` | value pinned by C-CF-118 | C-CF-118 | Core features |
| `7900` | value pinned by C-CF-118 | C-CF-118 | Core features |
| `p8` | value pinned by C-CF-124 | C-CF-124 | Core features |
| `product.<id>.name` | value pinned by C-CF-128 | C-CF-128 | Core features |
| `colour.<model_code>.name` | value pinned by C-CF-128 | C-CF-128 | Core features |
| `20.00` | value pinned by C-CF-130 | C-CF-130 | Core features |
| `"2000"` | value pinned by C-CF-130 | C-CF-130 | Core features |
| `0` | value pinned by C-CF-130 | C-CF-130 | Core features |
| `currency_mismatch` | value pinned by C-CF-132 | C-CF-132 | Core features |
| `not_authenticated` | value pinned by C-CF-141 | C-CF-141 | Core features |
| `role_not_permitted` | value pinned by C-CF-142 | C-CF-142 | Core features |
| `market_out_of_scope` | value pinned by C-CF-143 | C-CF-143 | Core features |
| `grant_expired` | value pinned by C-CF-144 | C-CF-144 | Core features |
| `explicit_deny` | value pinned by C-CF-145 | C-CF-145 | Core features |
| `field_not_permitted` | value pinned by C-CF-146 | C-CF-146 | Core features |
| `role_not_grantable` | value pinned by C-CF-147 | C-CF-147 | Core features |
| `invalid` | value pinned by C-CF-148 | C-CF-148 | Core features |
| `duplicate` | value pinned by C-CF-149 | C-CF-149 | Core features |
| `translations_incomplete` | value pinned by C-CF-151 | C-CF-151 | Core features |
| `price_missing` | value pinned by C-CF-152 | C-CF-152 | Core features |
| `untranslated_copy` | value pinned by C-CF-153 | C-CF-153 | Core features |
| `machine_legal_text` | value pinned by C-CF-154 | C-CF-154 | Core features |
| `machine` | value pinned by C-CF-154 | C-CF-154 | Core features |
| `approvals_incomplete` | value pinned by C-CF-155 | C-CF-155 | Core features |
| `embargo_pending` | value pinned by C-CF-156 | C-CF-156 | Core features |
| `not_live` | value pinned by C-CF-157 | C-CF-157 | Core features |
| `nothing_to_roll_back` | value pinned by C-CF-158 | C-CF-158 | Core features |
| `stale_version` | value pinned by C-CF-159 | C-CF-159 | Core features |
| `If-Match` | value pinned by C-CF-159 | C-CF-159 | Core features |
| `precondition_required` | value pinned by C-CF-160 | C-CF-160 | Core features |
| `unsupported_media` | value pinned by C-CF-161 | C-CF-161 | Core features |
| `draft` | value pinned by C-CF-178 | C-CF-178 | Core features |
| `reviewed` | value pinned by C-CF-178 | C-CF-178 | Core features |
| `approved` | value pinned by C-CF-178 | C-CF-178 | Core features |
| `meta.title` | value pinned by C-CF-188 | C-CF-188 | Core features |
| `meta.description` | value pinned by C-CF-188 | C-CF-188 | Core features |
| `hero.title` | value pinned by C-CF-188 | C-CF-188 | Core features |
| `collection.heading` | value pinned by C-CF-188 | C-CF-188 | Core features |
| `shop.cta` | value pinned by C-CF-188 | C-CF-188 | Core features |
| `lang.label` | value pinned by C-CF-188 | C-CF-188 | Core features |
| `newtab.suffix` | value pinned by C-CF-188 | C-CF-188 | Core features |
| `hero` | value pinned by C-CF-190 | C-CF-190 | Core features |
| `footer_list` | value pinned by C-CF-190 | C-CF-190 | Core features |
| `legal_footer` | value pinned by C-CF-190 | C-CF-190 | Core features |
| `in_review` | value pinned by C-CF-193 | C-CF-193 | Core features |
| `published` | value pinned by C-CF-193 | C-CF-193 | Core features |
| `unpublished` | value pinned by C-CF-193 | C-CF-193 | Core features |
| `story.body` | value pinned by C-CF-199 | C-CF-199 | Core features |
| `artist.bio` | value pinned by C-CF-199 | C-CF-199 | Core features |
| `assets/{campaign_slug}/{market_code or shared}/{sha256 of the bytes}.{png, jpg or webp}` | value pinned by C-CF-246 | C-CF-246 | Core features |
| `assets/afterglow/fr/9c1d...4e.png` | value pinned by C-CF-247 | C-CF-247 | Core features |
| `artifacts/{campaign_slug}/{market_code}/{version}.json` | value pinned by C-CF-257 | C-CF-257 | Core features |
| `artifacts/afterglow/fr/1.json` | value pinned by C-CF-257 | C-CF-257 | Core features |
| `translation.write` | value pinned by C-CF-263 | C-CF-263 | Core features |
| `market.submit` | value pinned by C-CF-264 | C-CF-264 | Core features |
| `approval.record` | value pinned by C-CF-264 | C-CF-264 | Core features |
| `market.publish` | value pinned by C-CF-264 | C-CF-264 | Core features |
| `market.rollback` | value pinned by C-CF-264 | C-CF-264 | Core features |
| `grant.create` | value pinned by C-CF-265 | C-CF-265 | Core features |
| `grant.revoke` | value pinned by C-CF-265 | C-CF-265 | Core features |
| `product.create` | value pinned by C-CF-266 | C-CF-266 | Core features |
| `colourway.create` | value pinned by C-CF-266 | C-CF-266 | Core features |
| `price.write` | value pinned by C-CF-267 | C-CF-267 | Core features |
| `string.create` | value pinned by C-CF-268 | C-CF-268 | Core features |
| `campaign.create` | value pinned by C-CF-269 | C-CF-269 | Core features |
| `campaign.update` | value pinned by C-CF-269 | C-CF-269 | Core features |
| `market.update` | value pinned by C-CF-270 | C-CF-270 | Core features |
| `product.update` | value pinned by C-CF-272 | C-CF-272 | Core features |
| `sort_order` | value pinned by C-CF-272 | C-CF-272 | Core features |
| `asset.upload` | value pinned by C-CF-273 | C-CF-273 | Core features |
| `30 days` | value pinned by C-CF-292 | C-CF-292 | Core features |
| `365 days` | value pinned by C-CF-293 | C-CF-293 | Core features |
| `7 years` | value pinned by C-CF-294 | C-CF-294 | Core features |
| `/` | value pinned by C-UF-02 | C-UF-02 | User flow |
| `/{campaign}/` | value pinned by C-UF-03 | C-UF-03 | User flow |
| `/{campaign}/{market}/` | value pinned by C-UF-04 | C-UF-04 | User flow |
| `/{campaign}/{market}/{legal_slug}/` | value pinned by C-UF-05 | C-UF-05 | User flow |
| `/privacy/` | value pinned by C-UF-06 | C-UF-06 | User flow |
| `/lang` | value pinned by C-UF-07 | C-UF-07 | User flow |
| `to` | value pinned by C-UF-07 | C-UF-07 | User flow |
| `/media/{id}` | value pinned by C-UF-08 | C-UF-08 | User flow |
| `/sitemap.xml` | value pinned by C-UF-09 | C-UF-09 | User flow |
| `/robots.txt` | value pinned by C-UF-09 | C-UF-09 | User flow |
| `/studio/login` | value pinned by C-UF-10 | C-UF-10 | User flow |
| `/studio/campaigns/{campaign}/` | value pinned by C-UF-12 | C-UF-12 | User flow |
| `/studio/campaigns/{campaign}/markets/{market}/` | value pinned by C-UF-13 | C-UF-13 | User flow |
| `/studio/campaigns/{campaign}/markets/{market}/preview/` | value pinned by C-UF-14 | C-UF-14 | User flow |
| `/studio/campaigns/{campaign}/products/` | value pinned by C-UF-15 | C-UF-15 | User flow |
| `/studio/audit/` | value pinned by C-UF-16 | C-UF-16 | User flow |
| `/studio/grants/` | value pinned by C-UF-17 | C-UF-17 | User flow |
| `Afterglow, the Halden Sport x Tove Ardenne capsule collection` | value pinned by C-UF-29 | C-UF-29 | User flow |
| `The collection` | value pinned by C-UF-31 | C-UF-31 | User flow |
| `£39.00` | value pinned by C-UF-33 | C-UF-33 | User flow |
| `£79.00` | value pinned by C-UF-33 | C-UF-33 | User flow |
| `/dusk-parade/be-nl/` | value pinned by C-UF-39 | C-UF-39 | User flow |
| `Dusk Parade, lopen na zonsondergang` | value pinned by C-UF-39 | C-UF-39 | User flow |
| `/dusk-parade/de/` | value pinned by C-UF-39 | C-UF-39 | User flow |
| `48px` | value pinned by C-UX-17 | C-UX-17 | UI/UX notes |
| `52px` | value pinned by C-UX-17 | C-UX-17 | UI/UX notes |
| `64px` | value pinned by C-UX-18 | C-UX-18 | UI/UX notes |
| `16px` | value pinned by C-UX-19 | C-UX-19 | UI/UX notes |
| `24px` | value pinned by C-UX-19 | C-UX-19 | UI/UX notes |
| `32px` | value pinned by C-UX-20 | C-UX-20 | UI/UX notes |
| `36px` | value pinned by C-UX-20 | C-UX-20 | UI/UX notes |
| `40px` | value pinned by C-UX-20 | C-UX-20 | UI/UX notes |
| `Price` | value pinned by C-FE-31 | C-FE-31 | Front-end specification |
| `Currency` | value pinned by C-FE-31 | C-FE-31 | Front-end specification |
| `X-Content-Type-Options: nosniff` | value pinned by C-TR-11 | C-TR-11 | Technical requirements |
| `Referrer-Policy: strict-origin-when-cross-origin` | value pinned by C-TR-12 | C-TR-12 | Technical requirements |
| `frame-ancestors 'none'` | value pinned by C-TR-15 | C-TR-15 | Technical requirements |
| `base-uri 'self'` | value pinned by C-TR-15 | C-TR-15 | Technical requirements |
| `form-action 'self'` | value pinned by C-TR-15 | C-TR-15 | Technical requirements |
| `Cache-Control: public, max-age=60, stale-while-revalidate=86400, stale-if-error=604800` | value pinned by C-TR-16 | C-TR-16 | Technical requirements |
| `Cache-Control: private, no-store` | value pinned by C-TR-18 | C-TR-18 | Technical requirements |
| `Vary: Accept-Language, Cookie` | value pinned by C-TR-18 | C-TR-18 | Technical requirements |
| `483101` | value pinned by C-TR-26 | C-TR-26 | Technical requirements |
| `7311550` | value pinned by C-TR-26 | C-TR-26 | Technical requirements |
| `6500` | value pinned by C-TR-26 | C-TR-26 | Technical requirements |
| `locale_tag` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `en-GB` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `es-ES` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `de-DE` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `nl-BE` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `data_region` | value pinned by C-DM-05 | C-DM-05 | Data model |
| `eu-west` | value pinned by C-DM-05 | C-DM-05 | Data model |
| `uk-south` | value pinned by C-DM-05 | C-DM-05 | Data model |
| `eu-central` | value pinned by C-DM-05 | C-DM-05 | Data model |
| `afterglow` | value pinned by C-DM-28 | C-DM-28 | Data model |
| `hscamp:__drop-` | value pinned by C-DM-28 | C-DM-28 | Data model |
| `artist` | value pinned by C-DM-29 | C-DM-29 | Data model |
| `story` | value pinned by C-DM-29 | C-DM-29 | Data model |
| `tagline.one` | value pinned by C-DM-36 | C-DM-36 | Data model |
| `collage.headline` | value pinned by C-DM-36 | C-DM-36 | Data model |
| `lookbook.alt` | value pinned by C-DM-41 | C-DM-41 | Data model |
| `12 rue des Tanneurs, 59000 Lille` | value pinned by C-DM-42 | C-DM-42 | Data model |
| `product.483101.name` | value pinned by C-DM-52 | C-DM-52 | Data model |
| `colour.7311550.name` | value pinned by C-DM-52 | C-DM-52 | Data model |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 24 |
| User roles | 2 | 32 |
| Core features | 33 | 307 |
| User flow | 9 | 55 |
| UI/UX notes | 0 | 41 |
| Front-end specification | 1 | 32 |
| Technical requirements | 10 | 26 |
| Data model | 2 | 55 |
| Constraints | 0 | 5 |
| Deployment contract | 10 | 27 |
