# Checklist: deku/consumer-device-catalogue-vb

Items: 234
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Unpinned values flagged: 6

## C-OV Overview

- [ ] `C-OV-01` `capability` The catalogue is organised on one axis, the product family. `src: Overview`
- [ ] `C-OV-02` `capability` A variant is the unit carrying media, availability, the buy route. `src: Overview`
- [ ] `C-OV-03` `constraint` Two colourways of one phone are two separate stored rows. `src: Overview`
- [ ] `C-OV-04` `constraint` The application ships no photograph file, no video file, no font binary. `src: Overview`
- [ ] `C-OV-05` `capability` A product belongs to exactly one family. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor cannot register a device. `src: User roles`
- [ ] `C-RL-02` `contract` A direct call from an anonymous session to an owner-only endpoint is denied. `src: User roles`
- [ ] `C-RL-03` `contract` A denied call leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-04` `role` An owner cannot open a request against a registration owned by anybody else. `src: User roles`
- [ ] `C-RL-05` `role` An owner cannot read another account's registrations. `src: User roles`
- [ ] `C-RL-06` `role` An owner cannot read another account's support requests. `src: User roles`
- [ ] `C-RL-07` `role` An owner cannot register a serial already registered to another account. `src: User roles`
- [ ] `C-RL-08` `literal` The seeded owner accounts are `owner@example.com`, `owner2@example.com`. `src: User roles`
- [ ] `C-RL-09` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-10` `contract` Authorization is enforced on the server for every mutating endpoint. `src: User roles`
- [ ] `C-RL-11` `contract` The account a row belongs to is read from the session rather than from the request body. `src: User roles`
- [ ] `C-RL-12` `role` No refusal reveals which account holds a serial. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `literal` The closed family slug set is `phones`, `audio`, `wearables`, `arc`. `src: Core features`
- [ ] `C-CF-02` `contract` The families endpoint returns the four families in catalogue order. `src: Core features`
- [ ] `C-CF-03` `contract` A colourway with a capacity resolves to exactly one variant. `src: Core features`
- [ ] `C-CF-04` `contract` The variant endpoint returns one variant carrying colourway, capacity, buy route, availability, media, price. `src: Core features`
- [ ] `C-CF-05` `literal` A worked variant identifier is `phone-5a-pro--midnight--12-256`. `src: Core features`
- [ ] `C-CF-06` `contract` An impossible colourway with capacity pair requested directly is refused as invalid. `src: Core features`
- [ ] `C-CF-07` `data` The colourway `Midnight` crossed with the smaller capacity has no seeded row on the flagship phone. `src: Core features`
- [ ] `C-CF-08` `literal` The buy route values are `direct`, `handoff`, `unavailable`. `src: Core features`
- [ ] `C-CF-09` `contract` A cart line posted for a variant whose buy route is not direct is refused as invalid. `src: Core features`
- [ ] `C-CF-10` `literal` The handed off variants are `phone-5a-pro--chalk--12-256`, `phone-5a-pro--slate--8-128`, `phone-5a--chalk--8-128`, `phone-5a--slate--8-128`, `headphone-2--white`, `arc-buds-1--orange`, `arc-buds-1--grey`. `src: Core features`
- [ ] `C-CF-11` `capability` A direct action adds the resolved variant to the cart. `src: Core features`
- [ ] `C-CF-12` `literal` The direct variants are `phone-5a-pro--chalk--8-128`, `phone-5a-pro--midnight--12-256`, `headphone-2--black`, `earbud-3a--white`, `arc-watch-2--grey`. `src: Core features`
- [ ] `C-CF-13` `literal` The seeded direct prices are `79900`, `99900`, `29900`, `14900`, `6900`. `src: Core features`
- [ ] `C-CF-14` `capability` A family listing shows one card per variant rather than one per product. `src: Core features`
- [ ] `C-CF-15` `data` The phones listing shows seven entries. `src: Core features`
- [ ] `C-CF-16` `data` The audio listing shows four entries. `src: Core features`
- [ ] `C-CF-17` `capability` Two chosen values on one facet axis widen the result set. `src: Core features`
- [ ] `C-CF-18` `capability` Values chosen on two different facet axes narrow the result set. `src: Core features`
- [ ] `C-CF-19` `data` Choosing the colourway `Chalk` with the capacity `12 GB / 256 GB` on the phones listing leaves exactly one entry. `src: Core features`
- [ ] `C-CF-20` `constraint` The capacity facet is offered on a phone family only. `src: Core features`
- [ ] `C-CF-21` `literal` The sort orders are `Featured`, `Newest`, `Name`. `src: Core features`
- [ ] `C-CF-22` `data` The newest order is by release date descending. `src: Core features`
- [ ] `C-CF-23` `literal` The seeded release dates are `2026-08-12`, `2026-06-03`, `2026-04-21`, `2026-02-17`, `2025-11-05`, `2025-09-30`. `src: Core features`
- [ ] `C-CF-24` `constraint` No price sort is offered. `src: Core features`
- [ ] `C-CF-25` `capability` A family route holding no products renders the empty listing surface. `src: Core features`
- [ ] `C-CF-26` `constraint` A family route holding no products does not render the not found surface. `src: Core features`
- [ ] `C-CF-27` `literal` The family `wearables` is seeded holding no products. `src: Core features`
- [ ] `C-CF-28` `contract` A family slug outside the closed set renders the not found surface. `src: Core features`
- [ ] `C-CF-29` `capability` A product holding no variants renders the empty listing surface. `src: Core features`
- [ ] `C-CF-30` `contract` An address matching no route answers not found. `src: Core features`
- [ ] `C-CF-31` `constraint` An unmatched address never renders an empty application shell. `src: Core features`
- [ ] `C-CF-32` `contract` Reloading a product route at a resolved address shows the same variant, media, availability, buy route, price. `src: Core features`
- [ ] `C-CF-33` `contract` A resolved variant is read from the stored row rather than rebuilt in the browser. `src: Core features`
- [ ] `C-CF-34` `data` Only a variant whose buy route is direct carries a stored price. `src: Core features`
- [ ] `C-CF-35` `constraint` A listing entry carries no price. `src: Core features`
- [ ] `C-CF-36` `capability` An owner registers a device by serial number against their own account. `src: Core features`
- [ ] `C-CF-37` `literal` The serial `HLC-3M08XT55` is seeded unregistered, resolving to `headphone-2`. `src: Core features`
- [ ] `C-CF-38` `constraint` A followed handoff writes no order row. `src: Core features`
- [ ] `C-CF-39` `constraint` A followed handoff writes no revenue row. `src: Core features`
- [ ] `C-CF-40` `contract` The cart survives a page reload. `src: Core features`
- [ ] `C-CF-41` `contract` The cart survives a browser restart. `src: Core features`
- [ ] `C-CF-42` `contract` A request naming a registration belonging to another account is refused on the server. `src: Core features`
- [ ] `C-CF-43` `constraint` A refused cross-account request writes no request row. `src: Core features`
- [ ] `C-CF-44` `contract` The registrations endpoint returns only the signed in account's rows. `src: Core features`
- [ ] `C-CF-45` `contract` The support requests endpoint returns only the signed in account's rows. `src: Core features`
- [ ] `C-CF-46` `contract` A serial is registered to at most one account. `src: Core features`
- [ ] `C-CF-47` `constraint` The refusal for an already registered serial names neither the holding account nor the address of that account. `src: Core features`
- [ ] `C-CF-48` `literal` The serial `HLC-9P61BW73` is seeded against the second owner account. `src: Core features`
- [ ] `C-CF-49` `literal` A serial is `HLC-` followed by eight upper case letters or digits. `src: Core features`
- [ ] `C-CF-50` `contract` A serial not matching the shape is refused as invalid with the field named. `src: Core features`
- [ ] `C-CF-51` `contract` A refused serial writes no registration row. `src: Core features`
- [ ] `C-CF-52` `contract` A well formed serial naming no product in the catalogue is refused as invalid. `src: Core features`
- [ ] `C-CF-53` `literal` The serial `HLC-0000ZZZZ` is seeded well formed, naming no product. `src: Core features`
- [ ] `C-CF-54` `contract` A request with an empty body is refused as invalid with the field named. `src: Core features`
- [ ] `C-CF-55` `contract` A request whose category falls outside the closed set is refused as invalid. `src: Core features`
- [ ] `C-CF-56` `literal` The support categories are `Setup`, `Battery`, `Connectivity`, `Software`, `Physical damage`. `src: Core features`
- [ ] `C-CF-57` `contract` One vote exists per article per anonymous identifier. `src: Core features`
- [ ] `C-CF-58` `contract` A second vote from the same identifier updates the stored answer rather than inserting a row. `src: Core features`
- [ ] `C-CF-59` `literal` A failed login answers with the wording `Incorrect email or password`. `src: Core features`
- [ ] `C-CF-60` `contract` A wrong password is indistinguishable from an unknown address at the boundary of the application. `src: Core features`
- [ ] `C-CF-61` `contract` Passwords are stored hashed rather than in clear. `src: Core features`
- [ ] `C-CF-62` `contract` The acknowledgement is a real message delivered over the configured mail service. `src: Core features`
- [ ] `C-CF-63` `contract` The acknowledgement is addressed to the signed in owner's own address. `src: Core features`
- [ ] `C-CF-64` `literal` The acknowledgement subject begins with `Support request ` followed by the reference. `src: Core features`
- [ ] `C-CF-65` `literal` A reference is `SR-` followed by eight digits. `src: Core features`
- [ ] `C-CF-66` `contract` A second submission carrying the same idempotency key returns the original reference. `src: Core features`
- [ ] `C-CF-67` `contract` A second submission carrying the same idempotency key writes no second request row. `src: Core features`
- [ ] `C-CF-68` `contract` A second submission carrying the same idempotency key sends no second acknowledgement. `src: Core features`
- [ ] `C-CF-69` `constraint` Registering a device sends no mail. `src: Core features`
- [ ] `C-CF-70` `constraint` A refused request sends no mail. `src: Core features`
- [ ] `C-CF-71` `literal` The first three home actions read `DISCOVER`, leading to a product route. `src: Core features`
- [ ] `C-CF-72` `capability` A capacity that exists in no variant of the chosen colourway renders unselectable. `src: Core features`
- [ ] `C-CF-73` `constraint` An impossible capacity is offered rather than removed from the selector. `src: Core features`
- [ ] `C-CF-74` `contract` Changing a selector rewrites the address to carry the resolved variant. `src: Core features`
- [ ] `C-CF-75` `capability` Changing a selector swaps the thumbnail to the resolved variant media. `src: Core features`
- [ ] `C-CF-76` `literal` A handed off variant renders the action label `SHOP ON Bazaario`. `src: Core features`
- [ ] `C-CF-77` `contract` A handed off action is a real anchor carrying a real address. `src: Core features`
- [ ] `C-CF-78` `contract` A handed off anchor carries the resolved variant identifier. `src: Core features`
- [ ] `C-CF-79` `literal` A direct variant renders the action label `ADD TO CART`. `src: Core features`
- [ ] `C-CF-80` `capability` A direct action opens the cart drawer. `src: Core features`
- [ ] `C-CF-81` `literal` The empty cart renders one full width action reading `CONTINUE SHOPPING`. `src: Core features`
- [ ] `C-CF-82` `contract` The checkout action is a real anchor to the separate payment origin. `src: Core features`
- [ ] `C-CF-83` `contract` Facet state lives in the query string. `src: Core features`
- [ ] `C-CF-84` `contract` Sort state lives in the query string. `src: Core features`
- [ ] `C-CF-85` `capability` The browser back button steps back through facet changes one at a time. `src: Core features`
- [ ] `C-CF-86` `literal` The not found surface carries the numeral `404` centred at display size. `src: Core features`
- [ ] `C-CF-87` `literal` The not found card heading reads `Page Not Found`. `src: Core features`
- [ ] `C-CF-88` `literal` The not found card action reads `BACK TO HOME`, returning to the home route. `src: Core features`
- [ ] `C-CF-89` `ui` The registration panel names the product a serial resolves to before confirmation. `src: Core features`
- [ ] `C-CF-90` `capability` A support request carries a body written by the owner. `src: Core features`
- [ ] `C-CF-91` `contract` A successful request returns a reference. `src: Core features`
- [ ] `C-CF-92` `capability` The request form carries an idempotency key issued when the form is opened. `src: Core features`
- [ ] `C-CF-93` `literal` Every article ends with the pinned helpfulness question. `src: Core features`
- [ ] `C-CF-94` `ui` Choosing a feedback control replaces both controls with an acknowledgement in place. `src: Core features`
- [ ] `C-CF-95` `literal` The seven support categories are `Product guide`, `Troubleshooting`, `FAQs`, `Software download`, `Service centres`, `Product status`, `Accessibility`. `src: Core features`
- [ ] `C-CF-96` `ui` The support centre bar carries the four product families, the community forum, support itself. `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `literal` The home route is `/`. `src: User flow`
- [ ] `C-UF-02` `literal` The family listings are `/collections/phones`, `/collections/audio`, `/collections/wearables`, `/collections/arc`. `src: User flow`
- [ ] `C-UF-03` `ui` An empty listing names the family, offering a control clearing every facet. `src: User flow`
- [ ] `C-UF-04` `ui` A loading listing renders card shaped placeholders at the card width. `src: User flow`
- [ ] `C-UF-05` `literal` The account route is `/account`. `src: User flow`
- [ ] `C-UF-06` `literal` The support centre route is `/pages/support-centre`. `src: User flow`
- [ ] `C-UF-07` `literal` The support request route is `/pages/contact-support`, open to an owner only. `src: User flow`
- [ ] `C-UF-08` `literal` The owner device route is `/pages/my-devices`, open to an owner only. `src: User flow`
- [ ] `C-UF-09` `capability` A form showing an error keeps everything else the visitor had typed. `src: User flow`
- [ ] `C-UF-10` `contract` An anonymous visitor reaching an owner-only route is sent to the account route. `src: User flow`
- [ ] `C-UF-11` `contract` A visitor sent to the account route is returned to the route asked for once signed in. `src: User flow`
- [ ] `C-UF-12` `ui` The registration panel shows an error beside the field causing the error. `src: User flow`
- [ ] `C-UF-13` `ui` The request form shows an error beside the field causing the error. `src: User flow`
- [ ] `C-UF-14` `constraint` An error is stated in words rather than by a change of border colour alone. `src: User flow`
- [ ] `C-UF-15` `literal` The launch surface routes are `/sitemap.xml`, `/robots.txt`, `/favicon.ico`. `src: User flow`
- [ ] `C-UF-16` `literal` The standing page routes are `/pages/privacy-policy`, `/pages/warranty-policy`, `/pages/user-agreement`, `/pages/acceptable-use`, `/pages/terms-of-sale`. `src: User flow`
- [ ] `C-UF-17` `literal` The reading routes are `/about`, `/halcyonos-4-1`, `/lower-ground`. `src: User flow`
- [ ] `C-UF-18` `literal` The cart route is `/cart`. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `constraint` The four type roles are held apart rather than consolidated onto one face. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The page ground is a near-white neutral rather than white. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` A card sits one ramp step apart from the ground, carrying no shadow. `src: UI/UX notes`
- [ ] `C-UX-04` `constraint` A default page carries greyscale alone. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Two hover states exist across the catalogue, both making the element slightly lighter. `src: UI/UX notes`
- [ ] `C-UX-06` `constraint` A hover leaves position, size, colour untouched. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Every icon carries an accessible name. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` The menu toggle is the first focusable element on the page. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A link leaving the site announces the departure. `src: UI/UX notes`
- [ ] `C-UX-10` `constraint` Every route holds its content inside the viewport width at a phone size. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` One statement per screen governs the catalogue routes. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The sense of movement comes from the inertia of the scrolling rather than from anything performing. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` A handed off anchor announces an external destination to assistive technology. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The home route is four full viewport panels stacked above the footer. `src: Front-end specification`
- [ ] `C-FE-03` `constraint` Home panels are separated by no rule, no gap, no parallax offset. `src: Front-end specification`
- [ ] `C-FE-04` `ui` A panel image occupies roughly the upper two thirds of the panel with the card overlapping the lower edge. `src: Front-end specification`
- [ ] `C-FE-05` `ui` A full viewport field of small dots sits fixed behind the content. `src: Front-end specification`
- [ ] `C-FE-06` `constraint` The dot field does not scroll, so content moves under a stationary grid. `src: Front-end specification`
- [ ] `C-FE-07` `ui` The dot field is drawn at low opacity. `src: Front-end specification`
- [ ] `C-FE-08` `ui` The dot field is blended so one layer resolves on a pale ground, a dark ground, a saturated ground. `src: Front-end specification`
- [ ] `C-FE-09` `constraint` Every global component works on a coloured route with a single definition of that component. `src: Front-end specification`
- [ ] `C-FE-10` `ui` The software release route ships the dark theme, every other route shipping light. `src: Front-end specification`
- [ ] `C-FE-11` `ui` Every icon is a field of identical circles on a square grid. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The menu toggle is two rows of six dots with an empty band between the rows. `src: Front-end specification`
- [ ] `C-FE-13` `ui` An icon takes its colour from the text around the icon. `src: Front-end specification`
- [ ] `C-FE-14` `ui` One floating bar is pinned to the top centre of every catalogue route. `src: Front-end specification`
- [ ] `C-FE-15` `constraint` The floating bar holds no cart count, no search field, no account link. `src: Front-end specification`
- [ ] `C-FE-16` `constraint` The floating bar holds its size, its position, its fill at every scroll position. `src: Front-end specification`
- [ ] `C-FE-17` `ui` The drawer occupies the full viewport, carrying every destination in two groups. `src: Front-end specification`
- [ ] `C-FE-18` `ui` A readout row sets the label, the colon, the value as three separate elements. `src: Front-end specification`
- [ ] `C-FE-19` `ui` The footer carries the utility rows plus account, contact, careers, legal, four social destinations. `src: Front-end specification`
- [ ] `C-FE-20` `ui` The support centre header is a full width bar rather than a floating bar. `src: Front-end specification`
- [ ] `C-FE-21` `constraint` The support centre renders without the dot field behind the content. `src: Front-end specification`
- [ ] `C-FE-22` `ui` The support centre landing carries a search field as a primary control. `src: Front-end specification`
- [ ] `C-FE-23` `ui` Headlines with body copy are set in a serif face. `src: Front-end specification`
- [ ] `C-FE-24` `ui` The wordmark, every label, every section numeral, every button is set in a dot matrix face. `src: Front-end specification`
- [ ] `C-FE-25` `ui` Figure captions, pull quotes, small print are set in a monospace face. `src: Front-end specification`
- [ ] `C-FE-26` `ui` The greyscale ramp holds thirteen roles, each with one job. `src: Front-end specification`
- [ ] `C-FE-27` `ui` The brand statement square is the only coloured element above the fold. `src: Front-end specification`
- [ ] `C-FE-28` `ui` A single amber dot at the top right of an editorial image card is the only amber on the site. `src: Front-end specification`
- [ ] `C-FE-29` `ui` A small square on the brand story route pulses continuously. `src: Front-end specification`
- [ ] `C-FE-30` `ui` The dot field is hidden from assistive technology, taking no focus. `src: Front-end specification`
- [ ] `C-FE-31` `ui` Below the constellation width the authored positions give way to a single stacked column of feature cards. `src: Front-end specification`
- [ ] `C-FE-32` `ui` The family listing goes from as many fixed width columns as fit, to two, to one. `src: Front-end specification`
- [ ] `C-FE-33` `ui` Feature cards are positioned around the central image rather than stacked beneath. `src: Front-end specification`
- [ ] `C-FE-34` `ui` The product route image is bled to the top of the viewport behind the floating bar. `src: Front-end specification`
- [ ] `C-FE-35` `ui` A buy panel is anchored over the product image carrying the selectors with one action. `src: Front-end specification`
- [ ] `C-FE-36` `ui` The community route sets running body copy in the dot matrix face. `src: Front-end specification`
- [ ] `C-FE-37` `ui` The community route ground is a saturated pink set as a route level override. `src: Front-end specification`
- [ ] `C-FE-38` `constraint` A listing card carries no price. `src: Front-end specification`
- [ ] `C-FE-39` `ui` One button style exists: a near-black fill, dot matrix capitals, the full width of the card. `src: Front-end specification`
- [ ] `C-FE-40` `ui` A card over a photograph takes a heavy backdrop blur with white at partial transparency. `src: Front-end specification`
- [ ] `C-FE-41` `ui` Where a backdrop blur is unavailable the fallback is a flat fill at the average colour of the region behind the card. `src: Front-end specification`
- [ ] `C-FE-42` `constraint` A semi transparent white is refused as a frosted fallback. `src: Front-end specification`
- [ ] `C-FE-43` `capability` Every catalogue route replaces the native scroll response with an inertial one. `src: Front-end specification`
- [ ] `C-FE-44` `ui` The inertial scroll response is disabled outright under reduced motion. `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` A sitemap lists every public route. `src: Technical requirements`
- [ ] `C-TR-02` `contract` A robots file names the sitemap. `src: Technical requirements`
- [ ] `C-TR-03` `contract` A favicon is served at its own address. `src: Technical requirements`
- [ ] `C-TR-04` `contract` The favicon is declared in the document head. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Every public route carries a title of its own. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Every public route carries a description of its own. `src: Technical requirements`
- [ ] `C-TR-07` `constraint` No two public routes share a title. `src: Technical requirements`
- [ ] `C-TR-08` `contract` Every public route declares a social preview title. `src: Technical requirements`
- [ ] `C-TR-09` `contract` Every public route declares a social preview image that resolves. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-11` `constraint` No database address appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` No administrative token appears in anything the browser downloads. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The variants table holds fourteen rows. `src: Data model`
- [ ] `C-DM-02` `data` The products table holds six rows. `src: Data model`
- [ ] `C-DM-03` `data` The families table holds four rows. `src: Data model`
- [ ] `C-DM-04` `contract` Seeding is idempotent, so restarting the application duplicates no row. `src: Data model`
- [ ] `C-DM-05` `data` A variant row carries a unique variant identifier, a product slug, a colourway, a nullable capacity, a buy route, an availability flag, a nullable price, a media seed. `src: Data model`
- [ ] `C-DM-06` `data` The stored price is null on every variant whose buy route is not direct. `src: Data model`
- [ ] `C-DM-07` `data` A registration row carries an identifier, an account identifier, a product slug, a serial, a registration timestamp. `src: Data model`
- [ ] `C-DM-08` `contract` A registration row survives a restart of the application. `src: Data model`
- [ ] `C-DM-09` `data` An outbound click row carries a variant identifier, a destination, an anonymous identifier, a creation timestamp. `src: Data model`
- [ ] `C-DM-10` `constraint` Nothing other than a followed handoff writes an outbound click row. `src: Data model`
- [ ] `C-DM-11` `data` A cart line row carries a cart identifier, a variant identifier, a quantity, a unit price, a line total, an exclusion flag. `src: Data model`
- [ ] `C-DM-12` `data` An article vote row carries an article slug, an anonymous identifier, a helpfulness answer, an update timestamp. `src: Data model`
- [ ] `C-DM-13` `contract` An idempotency key appears at most once in the support requests table. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One brand owns every product, so no seller account exists. `src: Constraints`
- [ ] `C-CN-02` `constraint` No conversion reporting of any kind exists. `src: Constraints`
- [ ] `C-CN-03` `constraint` No persistent cart badge appears in the catalogue chrome. `src: Constraints`
- [ ] `C-CN-04` `constraint` No search field appears in the catalogue chrome. `src: Constraints`
- [ ] `C-CN-05` `constraint` No sale banner, countdown, promotional ticker appears on the home route. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The health endpoint answers ready once the application has started. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The HTTP API is served on the same origin under the api prefix. `src: Deployment contract`
- [ ] `C-DC-03` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The application is reachable at the public address read from the environment. `src: Deployment contract`
- [ ] `C-DC-05` `constraint` Neither the public address nor the public port is hardcoded. `src: Deployment contract`
- [ ] `C-DC-06` `contract` An unauthorized call is rejected as a client error rather than as a server error. `src: Deployment contract`
- [ ] `C-DC-07` `contract` Bearer auth is required on everything except login, signup, health, the webhook receiver. `src: Deployment contract`
- [ ] `C-DC-08` `contract` The acknowledgement exists as a real message delivered over SMTP. `src: Deployment contract`
- [ ] `C-DC-09` `constraint` A log line standing in for a message is a contract violation. `src: Deployment contract`
- [ ] `C-DC-10` `constraint` A stubbed mail client returning success without connecting is a contract violation. `src: Deployment contract`
- [ ] `C-DC-11` `contract` The registration exists as a real row in the datastore. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` An in-memory list of registrations is a contract violation. `src: Deployment contract`
- [ ] `C-DC-13` `contract` The support request exists as a real row in the datastore. `src: Deployment contract`
- [ ] `C-DC-14` `constraint` A JSON file of support requests is a contract violation. `src: Deployment contract`
- [ ] `C-DC-15` `contract` The application starts from the environment image with no manual step. `src: Deployment contract`
- [ ] `C-DC-16` `contract` Login credentials are written to the credential file at the application root. `src: Deployment contract`
- [ ] `C-DC-17` `contract` A production build is served rather than a development server. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `owner@example.com` | User roles | `C-RL-08` |
| `owner2@example.com` | User roles | `C-RL-08` |
| `deku-demo-pw-2026` | User roles | `C-RL-09` |
| `phones` | Core features | `C-CF-01` |
| `audio` | Core features | `C-CF-01` |
| `wearables` | Core features | `C-CF-01` |
| `arc` | Core features | `C-CF-01` |
| `phone-5a-pro--midnight--12-256` | Core features | `C-CF-05` |
| `direct` | Core features | `C-CF-08` |
| `handoff` | Core features | `C-CF-08` |
| `unavailable` | Core features | `C-CF-08` |
| `phone-5a-pro--chalk--12-256` | Core features | `C-CF-10` |
| `phone-5a-pro--slate--8-128` | Core features | `C-CF-10` |
| `phone-5a--chalk--8-128` | Core features | `C-CF-10` |
| `phone-5a--slate--8-128` | Core features | `C-CF-10` |
| `headphone-2--white` | Core features | `C-CF-10` |
| `arc-buds-1--orange` | Core features | `C-CF-10` |
| `arc-buds-1--grey` | Core features | `C-CF-10` |
| `phone-5a-pro--chalk--8-128` | Core features | `C-CF-12` |
| `headphone-2--black` | Core features | `C-CF-12` |
| `earbud-3a--white` | Core features | `C-CF-12` |
| `arc-watch-2--grey` | Core features | `C-CF-12` |
| `79900` | Core features | `C-CF-13` |
| `99900` | Core features | `C-CF-13` |
| `29900` | Core features | `C-CF-13` |
| `14900` | Core features | `C-CF-13` |
| `6900` | Core features | `C-CF-13` |
| `Featured` | Core features | `C-CF-21` |
| `Newest` | Core features | `C-CF-21` |
| `Name` | Core features | `C-CF-21` |
| `2026-08-12` | Core features | `C-CF-23` |
| `2026-06-03` | Core features | `C-CF-23` |
| `2026-04-21` | Core features | `C-CF-23` |
| `2026-02-17` | Core features | `C-CF-23` |
| `2025-11-05` | Core features | `C-CF-23` |
| `2025-09-30` | Core features | `C-CF-23` |
| `HLC-3M08XT55` | Core features | `C-CF-37` |
| `headphone-2` | Core features | `C-CF-37` |
| `HLC-9P61BW73` | Core features | `C-CF-48` |
| `HLC-` | Core features | `C-CF-49` |
| `HLC-0000ZZZZ` | Core features | `C-CF-53` |
| `Setup` | Core features | `C-CF-56` |
| `Battery` | Core features | `C-CF-56` |
| `Connectivity` | Core features | `C-CF-56` |
| `Software` | Core features | `C-CF-56` |
| `Physical damage` | Core features | `C-CF-56` |
| `Incorrect email or password` | Core features | `C-CF-59` |
| `Support request ` | Core features | `C-CF-64` |
| `SR-` | Core features | `C-CF-65` |
| `DISCOVER` | Core features | `C-CF-71` |
| `SHOP ON Bazaario` | Core features | `C-CF-76` |
| `ADD TO CART` | Core features | `C-CF-79` |
| `CONTINUE SHOPPING` | Core features | `C-CF-81` |
| `404` | Core features | `C-CF-86` |
| `Page Not Found` | Core features | `C-CF-87` |
| `BACK TO HOME` | Core features | `C-CF-88` |
| `Product guide` | Core features | `C-CF-95` |
| `Troubleshooting` | Core features | `C-CF-95` |
| `FAQs` | Core features | `C-CF-95` |
| `Software download` | Core features | `C-CF-95` |
| `Service centres` | Core features | `C-CF-95` |
| `Product status` | Core features | `C-CF-95` |
| `Accessibility` | Core features | `C-CF-95` |
| `/` | User flow | `C-UF-01` |
| `/collections/phones` | User flow | `C-UF-02` |
| `/collections/audio` | User flow | `C-UF-02` |
| `/collections/wearables` | User flow | `C-UF-02` |
| `/collections/arc` | User flow | `C-UF-02` |
| `/account` | User flow | `C-UF-05` |
| `/pages/support-centre` | User flow | `C-UF-06` |
| `/pages/contact-support` | User flow | `C-UF-07` |
| `/pages/my-devices` | User flow | `C-UF-08` |
| `/sitemap.xml` | User flow | `C-UF-15` |
| `/robots.txt` | User flow | `C-UF-15` |
| `/favicon.ico` | User flow | `C-UF-15` |
| `/pages/privacy-policy` | User flow | `C-UF-16` |
| `/pages/warranty-policy` | User flow | `C-UF-16` |
| `/pages/user-agreement` | User flow | `C-UF-16` |
| `/pages/acceptable-use` | User flow | `C-UF-16` |
| `/pages/terms-of-sale` | User flow | `C-UF-16` |
| `/about` | User flow | `C-UF-17` |
| `/halcyonos-4-1` | User flow | `C-UF-17` |
| `/lower-ground` | User flow | `C-UF-17` |
| `/cart` | User flow | `C-UF-18` |
| `Was this page helpful?` | Core features | `C-CF-93` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact colour value of every palette role | `C-UX-01` |
| the exact size of every type scale row | `C-FE-13` |
| the exact softness of a card, a button, a dot | `C-FE-16` |
| the exact duration of every transition | `C-UX-05` |
| the exact viewport width of each structural change | `C-FE-28` |
| the address of the retailer, the payment origin, the forum, the careers site, the experiments site | `C-CF-40` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 4 | 5 |
| User roles | 1 | 12 |
| Core features | 37 | 96 |
| User flow | 7 | 18 |
| UI/UX notes | 8 | 12 |
| Technical requirements | 5 | 12 |
| Data model | 7 | 13 |
| Front-end specification | 30 | 44 |
| Constraints | 3 | 5 |
| Deployment contract | 13 | 17 |

