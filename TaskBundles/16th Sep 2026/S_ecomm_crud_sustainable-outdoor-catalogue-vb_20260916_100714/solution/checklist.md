# Checklist: Verdea Sustainable Outdoor Catalogue

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 659
Unpinned values flagged: 7

## C-OV Overview

- [ ] `C-OV-01` `capability` The site shows a catalogue of outdoor signage, furniture, equipment from one Portuguese manufacturer `src: Overview para 1`
- [ ] `C-OV-02` `literal` The site runs in the four locales `pt`, `en`, `es`, `fr` `src: Overview para 1`
- [ ] `C-OV-03` `capability` The catalogue holds the five collections Urban, Nature, Repolymer, Golf, Details `src: Overview para 1`
- [ ] `C-OV-04` `capability` A visitor submits a configured wishlist as a quotation request `src: Overview para 1`
- [ ] `C-OV-05` `constraint` No catalogue card or product page shows a price `src: Overview para 3`
- [ ] `C-OV-06` `constraint` The site offers no cart, no checkout, no payment step `src: Overview para 3`
- [ ] `C-OV-07` `constraint` A visitor never signs in to use any public feature `src: Overview para 3`
- [ ] `C-OV-08` `constraint` No public page loads a chat widget, a social embed or an analytics tracker `src: Overview para 3`
- [ ] `C-OV-09` `capability` A quotation line keeps the names the visitor configured `src: Overview para 4`
- [ ] `C-OV-10` `constraint` Pressing send twice never creates two enquiries `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor browses, configures, saves, requests quotations without any account `src: User roles table row 1`
- [ ] `C-RL-02` `role` A visitor reaches no back-office screen `src: User roles table row 1`
- [ ] `C-RL-03` `role` A `commercial` user reads any enquiry in full with its quotation lines `src: User roles table row 2`
- [ ] `C-RL-04` `role` A `commercial` user releases a quarantined enquiry `src: User roles table row 2`
- [ ] `C-RL-05` `role` A `commercial` user reads the subscriber list `src: User roles table row 2`
- [ ] `C-RL-06` `role` A `commercial` user cannot publish or unpublish a product `src: User roles table row 2`
- [ ] `C-RL-07` `role` An `editor` reads enquiry counts with subscriber counts `src: User roles table row 3`
- [ ] `C-RL-08` `role` An `editor` publishes or unpublishes a product in one locale `src: User roles table row 3`
- [ ] `C-RL-09` `role` An `editor` cannot read or open any enquiry `src: User roles table row 3`
- [ ] `C-RL-10` `role` An `editor` cannot release a quarantined enquiry `src: User roles table row 3`
- [ ] `C-RL-11` `role` An `editor` cannot read the subscriber list `src: User roles table row 3`
- [ ] `C-RL-12` `role` Both staff roles read the product list with its publish state `src: User roles table row 2`
- [ ] `C-RL-13` `contract` The server denies an `editor` call to a `commercial`-only endpoint, leaving protected state unchanged `src: User roles para 3`
- [ ] `C-RL-14` `contract` The server denies every back-office request that carries no valid token `src: User roles para 3`
- [ ] `C-RL-15` `constraint` No route lets anyone create an account `src: User roles para 1`
- [ ] `C-RL-16` `literal` The seeded account `commercial@example.com` holds role `commercial` `src: User roles seeded accounts`
- [ ] `C-RL-17` `literal` The seeded account `editor@example.com` holds role `editor` `src: User roles seeded accounts`
- [ ] `C-RL-18` `literal` The seeded account `former@example.com` holds status `suspended` `src: User roles seeded accounts`
- [ ] `C-RL-19` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: User roles seeded accounts`

## C-CF Core features

- [ ] `C-CF-01` `literal` Staff sign in at `POST /api/auth/login` with `email`, `password` `src: Core features rule 1`
- [ ] `C-CF-02` `literal` A successful sign-in returns `access_token`, `role`, `issued_at`, `expires_at` `src: Core features rule 1`
- [ ] `C-CF-03` `constraint` A staff token `expires_at` falls exactly seven days after `issued_at` `src: Core features rule 1`
- [ ] `C-CF-04` `contract` Every `/api/office` call carries the token as a bearer authorization header `src: Core features rule 1`
- [ ] `C-CF-05` `constraint` A wrong password gets the same denial body as an unknown address `src: Core features rule 2`
- [ ] `C-CF-06` `constraint` A denied sign-in returns no token `src: Core features rule 2`
- [ ] `C-CF-07` `literal` `POST /api/auth/logout` revokes the token at once `src: Core features rule 3`
- [ ] `C-CF-08` `constraint` A revoked token is denied on the next request `src: Core features rule 3`
- [ ] `C-CF-09` `constraint` A malformed token is denied `src: Core features rule 3`
- [ ] `C-CF-10` `constraint` The app stores staff passwords only as hashes `src: Core features rule 4`
- [ ] `C-CF-11` `constraint` The app offers no signup route, no password reset, no invitation `src: Core features rule 4`
- [ ] `C-CF-12` `capability` A staff account unused for ninety days becomes suspended `src: Core features rule 5`
- [ ] `C-CF-13` `constraint` A suspended account is denied at sign-in like a wrong password `src: Core features rule 5`
- [ ] `C-CF-14` `capability` A back-office page opened without a session goes to `/office/login` `src: Core features rule 5`
- [ ] `C-CF-15` `capability` After sign-in the back office returns to the local page first requested `src: Core features rule 5`
- [ ] `C-CF-16` `literal` The default locale is `pt`, which is also the fallback `src: Core features rule 6`
- [ ] `C-CF-17` `constraint` Every public page path begins with its locale segment `src: Core features rule 6`
- [ ] `C-CF-18` `literal` The products segment is `produtos`, `products`, `productos`, `produits` per locale `src: Core features rule 7`
- [ ] `C-CF-19` `literal` The about segment is `sobre`, `about`, `nosotros`, `apropos` per locale `src: Core features rule 7`
- [ ] `C-CF-20` `literal` The sustainability segment is `sustentabilidade`, `sustainability`, `sostenibilidad`, `durabilite` per locale `src: Core features rule 7`
- [ ] `C-CF-21` `literal` The journal segment is `jornal`, `journal`, `periodico`, `journal` per locale `src: Core features rule 7`
- [ ] `C-CF-22` `literal` The wishlist segment is `lista`, `wishlist`, `mi-lista`, `ma-liste` per locale `src: Core features rule 7`
- [ ] `C-CF-23` `literal` The segments `careers`, `legal`, `newsletter` stay identical in all four locales `src: Core features rule 7`
- [ ] `C-CF-24` `constraint` Two routes colliding on one segment inside a locale stop the app at start-up `src: Core features rule 7`
- [ ] `C-CF-25` `capability` Each locale version of a document carries its own localised slug `src: Core features rule 8`
- [ ] `C-CF-26` `capability` Cross-locale resolution uses the stable document identifier, never the slug `src: Core features rule 8`
- [ ] `C-CF-27` `literal` The root `/` answers `302` to a locale home `src: Core features rule 9`
- [ ] `C-CF-28` `capability` The root prefers the `verdea_locale` cookie only when `verdea_consent` lists `preferences` `src: Core features rule 9`
- [ ] `C-CF-29` `capability` The root otherwise follows the best `Accept-Language` match, else `pt` `src: Core features rule 9`
- [ ] `C-CF-30` `constraint` With preferences refused the language cookie is neither written nor read `src: Core features rule 9`
- [ ] `C-CF-31` `constraint` A deep link such as `/en/products` is never redirected by language headers `src: Core features rule 10`
- [ ] `C-CF-32` `constraint` A language the visitor chose is never overridden later `src: Core features rule 10`
- [ ] `C-CF-33` `capability` A path with upper case answers `301` to the lower-case canonical address `src: Core features rule 11`
- [ ] `C-CF-34` `capability` A path with a trailing slash answers `301` to the slash-free address `src: Core features rule 11`
- [ ] `C-CF-35` `constraint` An unrecognised query parameter causes no redirect `src: Core features rule 11`
- [ ] `C-CF-36` `constraint` An unrecognised query parameter stays out of the canonical link `src: Core features rule 11`
- [ ] `C-CF-37` `literal` `/en/products/nature/tee-sign-heritage` answers `301` to `/en/products/golf/tee-sign-heritage` `src: Core features rule 12`
- [ ] `C-CF-38` `capability` A category segment from another locale redirects to the canonical segment `src: Core features rule 12`
- [ ] `C-CF-39` `literal` `/es/productos/golf/tee-sign-heritage` answers `301` to `/es/productos/golf/senal-de-salida-heritage` `src: Core features rule 12`
- [ ] `C-CF-40` `capability` A document missing in the requested locale answers `302` to its Portuguese version `src: Core features rule 13`
- [ ] `C-CF-41` `capability` The Portuguese fallback page shows a dismissible not-available line `src: Core features rule 13`
- [ ] `C-CF-42` `constraint` A fallback document is never served under another locale's address `src: Core features rule 13`
- [ ] `C-CF-43` `capability` The language switcher links each locale to the same document through its identifier `src: Core features rule 14`
- [ ] `C-CF-44` `capability` A switcher item with no equivalent leads to that locale's home, marked before choosing `src: Core features rule 14`
- [ ] `C-CF-45` `constraint` A French page carries no English label `src: Core features rule 14`
- [ ] `C-CF-46` `capability` Every public page declares `hreflang` alternates for each existing locale `src: Core features rule 15`
- [ ] `C-CF-47` `literal` The `x-default` alternate leads to the `pt` version `src: Core features rule 15`
- [ ] `C-CF-48` `constraint` Alternate links are reciprocal between locale versions `src: Core features rule 15`
- [ ] `C-CF-49` `literal` English dates render with the full month name, like `May 12, 2026` `src: Core features rule 16`
- [ ] `C-CF-50` `constraint` Addresses with telephone numbers render exactly as authored `src: Core features rule 16`
- [ ] `C-CF-51` `literal` The English catalogue holds `20` products `src: Core features rule 17`
- [ ] `C-CF-52` `literal` English collection counts are Urban `6`, Nature `4`, Repolymer `3`, Golf `4`, Details `3` `src: Core features rule 17`
- [ ] `C-CF-53` `literal` The Portuguese catalogue holds `20` products `src: Core features rule 17`
- [ ] `C-CF-54` `literal` The Spanish catalogue holds `19` products, lacking `Slim Room Sign` `src: Core features rule 17`
- [ ] `C-CF-55` `literal` The French catalogue holds `18` products, lacking `Slim Room Sign`, `Golf Bag Stand` `src: Core features rule 17`
- [ ] `C-CF-56` `literal` The collection facet is labelled `by Collections` `src: Core features rule 18`
- [ ] `C-CF-57` `literal` The product type facet is labelled `by Products` with Signage, Construction, Furniture, Equipment `src: Core features rule 18`
- [ ] `C-CF-58` `capability` The sub-collection group appears only when exactly one collection is active `src: Core features rule 18`
- [ ] `C-CF-59` `literal` Urban carries the sub-collections `Frame`, `Plaza`, `Reuse` `src: Core features rule 18`
- [ ] `C-CF-60` `capability` Facet groups combine as a conjunction `src: Core features rule 19`
- [ ] `C-CF-61` `capability` Values inside one facet group combine as a disjunction `src: Core features rule 19`
- [ ] `C-CF-62` `literal` Urban with Signage leaves `2` English products `src: Core features rule 19`
- [ ] `C-CF-63` `literal` Golf with Signage leaves `2` English products `src: Core features rule 19`
- [ ] `C-CF-64` `literal` Urban or Golf leaves `10` English products `src: Core features rule 19`
- [ ] `C-CF-65` `literal` Urban with Plaza leaves `2` products, Urban with Frame leaves `3` `src: Core features rule 19`
- [ ] `C-CF-66` `literal` Details with Construction leaves `0` products `src: Core features rule 19`
- [ ] `C-CF-67` `literal` Facet state lives in the parameters `collection`, `productType`, `subCollection` `src: Core features rule 20`
- [ ] `C-CF-68` `capability` A repeated parameter carries each extra facet value `src: Core features rule 20`
- [ ] `C-CF-69` `capability` Reopening a filtered catalogue address reproduces every selected facet `src: Core features rule 20`
- [ ] `C-CF-70` `capability` An unknown facet value is ignored, never yielding an empty grid `src: Core features rule 20`
- [ ] `C-CF-71` `capability` An unknown facet value is removed from the address `src: Core features rule 20`
- [ ] `C-CF-72` `literal` The counter reads `Showing <n> of <total> Results` `src: Core features rule 21`
- [ ] `C-CF-73` `constraint` A collection catalogue card never counts toward the counter `src: Core features rule 21`
- [ ] `C-CF-74` `literal` The server-rendered `/en/products` reads `Showing 20 of 20 Results` `src: Core features rule 21`
- [ ] `C-CF-75` `literal` `/en/products?collection=urban&productType=signage` arrives reading `Showing 2 of 20 Results` `src: Core features rule 21`
- [ ] `C-CF-76` `capability` A facet change filters products already on the page without a request `src: Core features rule 22`
- [ ] `C-CF-77` `constraint` A facet change shows no loading state `src: Core features rule 22`
- [ ] `C-CF-78` `capability` The counter change is announced politely to assistive technology `src: Core features rule 22`
- [ ] `C-CF-79` `capability` A facet value with no matching products stays visible as unavailable with its count `src: Core features rule 23`
- [ ] `C-CF-80` `capability` A combination matching nothing shows removable chips, a clear control, three suggested products `src: Core features rule 23`
- [ ] `C-CF-81` `capability` On narrow screens a floating `FILTER` control opens the facet panel `src: Core features rule 24`
- [ ] `C-CF-82` `capability` The floating `FILTER` control shows how many facets are active `src: Core features rule 24`
- [ ] `C-CF-83` `capability` Each catalogue card shows the title, collection pill, render, colour strip, size strip `src: Core features rule 25`
- [ ] `C-CF-84` `literal` A card strip shows two items then `+N`, so `Tee Sign Heritage` reads `+6` `src: Core features rule 25`
- [ ] `C-CF-85` `capability` Size chips render exactly as authored, unsorted `src: Core features rule 26`
- [ ] `C-CF-86` `literal` `Frame Bollard` sizes read `s`, `m` `src: Core features rule 26`
- [ ] `C-CF-87` `literal` `Reuse Litter Bin Duo` sizes read `All`, `Bottle`, `Pet` `src: Core features rule 26`
- [ ] `C-CF-88` `literal` `Classic Ball Washer` sizes read `R900`, `Q600` `src: Core features rule 26`
- [ ] `C-CF-89` `capability` A product with no colour shows no colour strip `src: Core features rule 27`
- [ ] `C-CF-90` `literal` `Line Door Plate` carries neither a colour nor a size `src: Core features rule 27`
- [ ] `C-CF-91` `ui` The card framing differs for wide, tall, square renders `src: Core features rule 28`
- [ ] `C-CF-92` `literal` `GET /api/products?locale=en` returns the published products as a top-level array `src: Core features rule 29`
- [ ] `C-CF-93` `capability` `GET /api/products` accepts the facet parameters with the same combination rules `src: Core features rule 29`
- [ ] `C-CF-94` `ui` Card images beyond the first two rows load on approaching the view `src: Core features rule 30`
- [ ] `C-CF-95` `literal` `/en/products/urban` reads `Showing 6 of 20 Results` `src: Core features rule 31`
- [ ] `C-CF-96` `capability` Choosing another collection on a collection route navigates to that collection route `src: Core features rule 32`
- [ ] `C-CF-97` `capability` Clearing the collection navigates to `/en/products` keeping other facets `src: Core features rule 32`
- [ ] `C-CF-98` `capability` A collection route names the collection in its document title `src: Core features rule 33`
- [ ] `C-CF-99` `literal` The catalogue documents are `Urban Catalogue`, `Nature Catalogue`, `Repolymer Catalogue`, `Golf Catalogue` `src: Core features rule 34`
- [ ] `C-CF-100` `constraint` The Details collection has no catalogue card `src: Core features rule 34`
- [ ] `C-CF-101` `capability` The catalogue card opens the file request in collection-catalogue scope `src: Core features rule 34`
- [ ] `C-CF-102` `capability` An unknown collection segment answers the not-found page naming the five collections `src: Core features rule 35`
- [ ] `C-CF-103` `capability` A collection empty in a locale shows its header with a Portuguese offer `src: Core features rule 35`
- [ ] `C-CF-104` `capability` `/en/products/golf/tee-sign-heritage` shows the object beside its specification `src: Core features rule 36`
- [ ] `C-CF-105` `ui` The object side shows a still render first, then a live object after first paint `src: Core features rule 37`
- [ ] `C-CF-106` `ui` A refused live object leaves the still images with nothing announced `src: Core features rule 37`
- [ ] `C-CF-107` `capability` The specification side opens with the `PRODUCTS` back control returning to the collection `src: Core features rule 38`
- [ ] `C-CF-108` `capability` A short question label sits beside the product description `src: Core features rule 38`
- [ ] `C-CF-109` `capability` A `Specs` cue leads down to the specification block `src: Core features rule 38`
- [ ] `C-CF-110` `capability` The compound control holds a bookmark with `REQUEST INFORMATION` as two separately named controls `src: Core features rule 39`
- [ ] `C-CF-111` `literal` The specification labels run `Dimensions`, `Structure Options`, `Structure Colors`, `Display Options`, `HPL+ Colors`, `Materials`, `Specifications`, `Advantages`, `References` `src: Core features rule 40`
- [ ] `C-CF-112` `capability` A product shows only the specification rows present for that product `src: Core features rule 40`
- [ ] `C-CF-113` `literal` `Tee Sign Heritage` dimensions read `190 x 100 x 1700 mm` `src: Core features rule 41`
- [ ] `C-CF-114` `literal` `Tee Sign Heritage` structures are `Galvanised steel` with a metallised painted steel option `src: Core features rule 41`
- [ ] `C-CF-115` `literal` `Tee Sign Heritage` colours include `Pure white RAL9010`, `Salmon pink RAL3022`, `Personalised` `src: Core features rule 41`
- [ ] `C-CF-116` `literal` `Tee Sign Heritage` displays are `HPL +`, `HPL Print` `src: Core features rule 41`
- [ ] `C-CF-117` `literal` `Tee Sign Heritage` laminate colours include `Sienna brown`, `Turf green`, `Black` `src: Core features rule 41`
- [ ] `C-CF-118` `literal` `Tee Sign Heritage` materials read `Reinforced, brown recycled plastic; HPL+ or HPL Print.` `src: Core features rule 41`
- [ ] `C-CF-119` `literal` `Tee Sign Heritage` advantages begin `No maintenance required; Easy component replacement` `src: Core features rule 41`
- [ ] `C-CF-120` `literal` `Tee Sign Heritage` references are `HPL+ - GTEETTM010`, `HPL Print - GTEETTM011` `src: Core features rule 41`
- [ ] `C-CF-121` `literal` The `Tee Sign Heritage` description opens `Where tradition meets function` `src: Core features rule 41`
- [ ] `C-CF-122` `capability` A colour value keeps its standard colour reference in one string `src: Core features rule 42`
- [ ] `C-CF-123` `capability` A colour value with no colour renders as text without a swatch `src: Core features rule 42`
- [ ] `C-CF-124` `capability` Each reference code carries its own copy control `src: Core features rule 43`
- [ ] `C-CF-125` `capability` Copying a reference code gives visible feedback that reverts `src: Core features rule 43`
- [ ] `C-CF-126` `literal` `Plaza Bench Long` sizes are `1400`, `1900`, `2000` `src: Core features rule 44`
- [ ] `C-CF-127` `literal` The `2000` size of `Plaza Bench Long` measures `2000 x 554 x 465 mm` `src: Core features rule 44`
- [ ] `C-CF-128` `literal` `Plaza Bench Long` carries the reference `Plaza Bench Long - UBSCFE0000881` `src: Core features rule 44`
- [ ] `C-CF-129` `constraint` `Plaza Bench Long` has no display option, no laminate option `src: Core features rule 44`
- [ ] `C-CF-130` `constraint` `Slim Room Sign` shows no `REQUEST INFORMATION` control `src: Core features rule 45`
- [ ] `C-CF-131` `capability` A control for something a product lacks is absent, never disabled `src: Core features rule 45`
- [ ] `C-CF-132` `literal` `In the same Collection` lists up to six other products of the collection `src: Core features rule 46`
- [ ] `C-CF-133` `constraint` The related strip keeps one stable order between visits `src: Core features rule 46`
- [ ] `C-CF-134` `literal` `Boardwalk Module`, `Viewpoint Platform Deck` both list `Ridge Viewpoint Boardwalk` `src: Core features rule 47`
- [ ] `C-CF-135` `capability` A product with case studies shows a strip of those articles `src: Core features rule 47`
- [ ] `C-CF-136` `literal` `GET /api/products/tee-sign-heritage?locale=en` returns the product with its options `src: Core features rule 48`
- [ ] `C-CF-137` `literal` The product detail lists each locale slug under `alternates` `src: Core features rule 48`
- [ ] `C-CF-138` `literal` The product page carries `BreadcrumbList` metadata derived from its path `src: Core features rule 48`
- [ ] `C-CF-139` `literal` The bookmark on a configurable product opens the modal headed `Personalise your product` `src: Core features rule 49`
- [ ] `C-CF-140` `constraint` Opening the options modal never changes the address `src: Core features rule 49`
- [ ] `C-CF-141` `capability` The bookmark on `Line Door Plate` adds the product directly `src: Core features rule 49`
- [ ] `C-CF-142` `capability` The modal offers size, structure, colour, display, laminate colour in that order `src: Core features rule 50`
- [ ] `C-CF-143` `constraint` No option axis constrains another `src: Core features rule 50`
- [ ] `C-CF-144` `capability` An axis with no values is absent from the modal `src: Core features rule 51`
- [ ] `C-CF-145` `literal` `Reuse Litter Bin Duo` shows its single colour `Anthracite grey RAL7016` already chosen `src: Core features rule 51`
- [ ] `C-CF-146` `ui` Choosing a size swaps the drawing inside a reserved box `src: Core features rule 52`
- [ ] `C-CF-147` `ui` A swatch shows its colour or texture with the full name as text `src: Core features rule 53`
- [ ] `C-CF-148` `ui` The chosen swatch carries a tick with a change of shape `src: Core features rule 53`
- [ ] `C-CF-149` `capability` Adding with no option chosen is accepted `src: Core features rule 54`
- [ ] `C-CF-150` `capability` The modal primary control adds the configuration, then closes `src: Core features rule 54`
- [ ] `C-CF-151` `capability` Escape closes the options modal without adding `src: Core features rule 54`
- [ ] `C-CF-152` `capability` Focus returns to the opening control once the options modal closes `src: Core features rule 54`
- [ ] `C-CF-153` `literal` The references mode is headed `References` `src: Core features rule 55`
- [ ] `C-CF-154` `capability` A `REF-` token in rich text renders as a reference-code element `src: Core features rule 55`
- [ ] `C-CF-155` `constraint` A configuration never appears in the address `src: Core features rule 56`
- [ ] `C-CF-156` `capability` The wishlist lives in the visitor's own browser `src: Core features rule 57`
- [ ] `C-CF-157` `capability` An unreadable stored wishlist loads as empty `src: Core features rule 57`
- [ ] `C-CF-158` `capability` A wishlist entry holds an entry identifier, the product identifier, the chosen option names `src: Core features rule 58`
- [ ] `C-CF-159` `capability` One product saved in two colours shows as two rows `src: Core features rule 58`
- [ ] `C-CF-160` `capability` A card bookmark reads filled with a count once a product is saved twice `src: Core features rule 59`
- [ ] `C-CF-161` `capability` Pressing a filled card bookmark removes one entry for that product `src: Core features rule 59`
- [ ] `C-CF-162` `capability` The adding confirmation shows the product name, an undo control, a draining bar `src: Core features rule 60`
- [ ] `C-CF-163` `capability` The adding confirmation never takes focus `src: Core features rule 60`
- [ ] `C-CF-164` `capability` Undo removes exactly the entry just added `src: Core features rule 60`
- [ ] `C-CF-165` `capability` The header wishlist count updates on every change `src: Core features rule 61`
- [ ] `C-CF-166` `constraint` The header wishlist count is hidden at zero `src: Core features rule 61`
- [ ] `C-CF-167` `literal` The empty wishlist shows `Your wishlist` over a heading opening `No picks yet?` `src: Core features rule 62`
- [ ] `C-CF-168` `literal` The empty wishlist offers `Start adding` leading to the catalogue `src: Core features rule 62`
- [ ] `C-CF-169` `ui` Three decorative `Your next product` cards stand in the empty wishlist `src: Core features rule 62`
- [ ] `C-CF-170` `constraint` An empty wishlist shows no quotation control `src: Core features rule 62`
- [ ] `C-CF-171` `literal` A populated wishlist offers `Request a quotation` `src: Core features rule 63`
- [ ] `C-CF-172` `capability` The clear control names the count, asking for confirmation first `src: Core features rule 63`
- [ ] `C-CF-173` `capability` Each wishlist row shows render, title, collection, chosen option names, a remove control `src: Core features rule 63`
- [ ] `C-CF-174` `capability` A row offers to choose an unchosen axis in the options modal `src: Core features rule 63`
- [ ] `C-CF-175` `capability` Rows resolve by product identifier in the current locale `src: Core features rule 64`
- [ ] `C-CF-176` `capability` A row for a product missing in the locale is marked not available in the language `src: Core features rule 64`
- [ ] `C-CF-177` `capability` The wishlist survives a reload `src: Core features rule 65`
- [ ] `C-CF-178` `capability` The wishlist survives a locale change `src: Core features rule 65`
- [ ] `C-CF-179` `literal` The wishlist refuses a `51`st entry with a message naming the count `src: Core features rule 66`
- [ ] `C-CF-180` `capability` Adding to the wishlist keeps working with the network off `src: Core features rule 66`
- [ ] `C-CF-181` `literal` The quotation modal shows the tabs `Contact`, `Wishlist`, `Files` `src: Core features rule 67`
- [ ] `C-CF-182` `capability` The quotation mode shows the wishlist inline above the fields `src: Core features rule 67`
- [ ] `C-CF-183` `literal` The quotation fields are `First Name`, `Last Name`, `Email`, `Role`, `Industry`, `Country`, `City`, `NIF` `src: Core features rule 67`
- [ ] `C-CF-184` `literal` The quotation form asks `Some products have BIM/3D files available, are you interested?` `src: Core features rule 67`
- [ ] `C-CF-185` `literal` `POST /api/lead/quotation` answers `202` with the `reference` `src: Core features rule 68`
- [ ] `C-CF-186` `capability` A quotation writes one `lead` of kind `quotation`, one `quotation`, one line per entry `src: Core features rule 68`
- [ ] `C-CF-187` `constraint` A quotation is written whole or not at all `src: Core features rule 68`
- [ ] `C-CF-188` `literal` The reference is `VQ-` plus six characters from `23456789ABCDEFGHJKMNPQRSTUVWXYZ` `src: Core features rule 69`
- [ ] `C-CF-189` `constraint` References are unique across quotations `src: Core features rule 69`
- [ ] `C-CF-190` `capability` The request sends entries with `entryId`, `productId`, `slug`, `options` `src: Core features rule 70`
- [ ] `C-CF-191` `constraint` A client-sent title makes the whole request invalid `src: Core features rule 70`
- [ ] `C-CF-192` `capability` Each stored line takes the current title, slug, collection name in the submitted locale `src: Core features rule 71`
- [ ] `C-CF-193` `literal` A line found only in `pt` stores the Portuguese names with `resolved_from_locale` set to `pt` `src: Core features rule 71`
- [ ] `C-CF-194` `literal` An unknown product stores its slug as title, `No longer in the catalogue` as collection, `unresolved` true `src: Core features rule 71`
- [ ] `C-CF-195` `constraint` One unresolved line never refuses the request `src: Core features rule 71`
- [ ] `C-CF-196` `literal` Option names are stored as sent in `option_size`, `option_structure`, `option_color`, `option_display`, `option_hpl_color` `src: Core features rule 72`
- [ ] `C-CF-197` `constraint` An unchosen option is stored empty `src: Core features rule 72`
- [ ] `C-CF-198` `literal` The server keeps the flat payload in `payload_rendered` `src: Core features rule 73`
- [ ] `C-CF-199` `literal` Each payload block lists `Collection:`, `Structure:`, `Color:`, `Display:`, `HPL Color:`, then `Size:` last `src: Core features rule 73`
- [ ] `C-CF-200` `literal` An unchosen option renders as `(not chosen)` in the payload `src: Core features rule 73`
- [ ] `C-CF-201` `capability` Payload blocks are numbered from one with a blank line between them `src: Core features rule 73`
- [ ] `C-CF-202` `constraint` `item_count` equals the number of stored lines `src: Core features rule 74`
- [ ] `C-CF-203` `constraint` A quotation with no entries is refused `src: Core features rule 75`
- [ ] `C-CF-204` `constraint` A quotation with more than fifty entries is refused `src: Core features rule 75`
- [ ] `C-CF-205` `constraint` An option key outside the five is refused `src: Core features rule 75`
- [ ] `C-CF-206` `constraint` `firstName`, `lastName` must hold 1 to 80 characters with a non-space `src: Core features rule 76`
- [ ] `C-CF-207` `constraint` `country` is free text of 2 to 60 characters `src: Core features rule 76`
- [ ] `C-CF-208` `constraint` `city` holds 1 to 80 characters `src: Core features rule 76`
- [ ] `C-CF-209` `constraint` `role`, `industry` must each match the locale's closed list `src: Core features rule 76`
- [ ] `C-CF-210` `constraint` `taxId` is optional, 1 to 20 digits or spaces `src: Core features rule 76`
- [ ] `C-CF-211` `literal` Every locale submits an English role value from `Landscape architect`, `Municipal buyer`, `Park or trail operator`, `Golf course superintendent`, `Contractor`, `Other` `src: Core features rule 76`
- [ ] `C-CF-212` `literal` The English industry list holds six values from `Public administration` to `Other` `src: Core features rule 76`
- [ ] `C-CF-213` `capability` A fiscal number keeps its leading zeros `src: Core features rule 77`
- [ ] `C-CF-214` `literal` `wantsTechnicalFiles` records the checkbox on the lead `src: Core features rule 78`
- [ ] `C-CF-215` `constraint` The files checkbox never triggers a download `src: Core features rule 78`
- [ ] `C-CF-216` `capability` The modal sends one idempotency key per form instance `src: Core features rule 79`
- [ ] `C-CF-217` `constraint` The wishlist clears only after the confirmation renders for a success `src: Core features rule 80`
- [ ] `C-CF-218` `constraint` A failed quotation leaves the form values in place `src: Core features rule 80`
- [ ] `C-CF-219` `capability` Removing the last entry closes an open quotation modal with a message `src: Core features rule 81`
- [ ] `C-CF-220` `capability` A wishlist emptied by a successful submission shows a line naming the reference `src: Core features rule 81`
- [ ] `C-CF-221` `capability` The quotation confirmation shows the reference, receiving focus `src: Core features rule 82`
- [ ] `C-CF-222` `capability` The quotation confirmation says a full copy is on its way by email `src: Core features rule 82`
- [ ] `C-CF-223` `capability` The file gate is offered on products, catalogue cards, chapter download controls `src: Core features rule 83`
- [ ] `C-CF-224` `capability` The files mode asks for first name, last name, email, privacy consent only `src: Core features rule 83`
- [ ] `C-CF-225` `literal` `POST /api/lead/file-request` answers `202` with `documentName`, `downloadUrl`, `expiresAt` `src: Core features rule 84`
- [ ] `C-CF-226` `capability` A file request writes one `lead` of kind `file_request` with one `file_request` `src: Core features rule 84`
- [ ] `C-CF-227` `literal` The product document is named `Tee Sign Heritage technical files` `src: Core features rule 84`
- [ ] `C-CF-228` `capability` A request for a document that does not exist is refused as not found, writing nothing `src: Core features rule 84`
- [ ] `C-CF-229` `constraint` A grant is an opaque token bound to one document `src: Core features rule 85`
- [ ] `C-CF-230` `constraint` A grant lasts seven days `src: Core features rule 85`
- [ ] `C-CF-231` `literal` A grant allows at most `5` redemptions `src: Core features rule 85`
- [ ] `C-CF-232` `literal` `GET /api/files/<token>` answers `302` to a signed same-origin location `src: Core features rule 86`
- [ ] `C-CF-233` `literal` The signed location serves a PDF named `tee-sign-heritage-technical-files-en.pdf` `src: Core features rule 86`
- [ ] `C-CF-234` `literal` The Urban catalogue downloads as `urban-catalogue-en.pdf` `src: Core features rule 86`
- [ ] `C-CF-235` `capability` Each grant call counts one redemption `src: Core features rule 86`
- [ ] `C-CF-236` `literal` An unknown, expired or exhausted token answers `404`, never `403` `src: Core features rule 87`
- [ ] `C-CF-237` `constraint` A signed location older than five minutes answers not found `src: Core features rule 87`
- [ ] `C-CF-238` `constraint` The grant endpoint ignores any document or asset parameter `src: Core features rule 88`
- [ ] `C-CF-239` `capability` The file confirmation names the document with a download control `src: Core features rule 89`
- [ ] `C-CF-240` `capability` The file confirmation says the same link was emailed `src: Core features rule 89`
- [ ] `C-CF-241` `capability` A document granted earlier in the session downloads without the form `src: Core features rule 90`
- [ ] `C-CF-242` `constraint` A repeat request from the same address issues a fresh grant `src: Core features rule 91`
- [ ] `C-CF-243` `capability` Generated documents carry a cover, then one page per product with its specification `src: Core features rule 92`
- [ ] `C-CF-244` `literal` The newsletter form shows `By submitting your email you agree to our Privacy Policy.` `src: Core features rule 93`
- [ ] `C-CF-245` `constraint` The newsletter form collects only an email address `src: Core features rule 93`
- [ ] `C-CF-246` `capability` The newsletter form appears in every footer, the journal index, sustainability, about `src: Core features rule 93`
- [ ] `C-CF-247` `literal` `POST /api/subscriber` answers `202` with `check_inbox` in every accepted case `src: Core features rule 94`
- [ ] `C-CF-248` `constraint` The sign-up confirmation line never says the visitor is subscribed `src: Core features rule 94`
- [ ] `C-CF-249` `literal` A new address creates a `subscriber` in `pending` with a confirm token `src: Core features rule 95`
- [ ] `C-CF-250` `constraint` A confirm token lasts fourteen days `src: Core features rule 95`
- [ ] `C-CF-251` `constraint` A repeat sign-up for a pending address creates no second row `src: Core features rule 96`
- [ ] `C-CF-252` `constraint` A repeat sign-up for a pending address sends no second message within twenty-four hours `src: Core features rule 96`
- [ ] `C-CF-253` `constraint` A repeat sign-up for a confirmed address sends nothing, answering like a new sign-up `src: Core features rule 96`
- [ ] `C-CF-254` `capability` A sign-up for an unsubscribed address returns to `pending` with a new confirmation `src: Core features rule 96`
- [ ] `C-CF-255` `literal` The confirmation link `/api/subscriber/confirm?token=` answers `303` to `/<locale>/newsletter/confirmed` `src: Core features rule 97`
- [ ] `C-CF-256` `capability` Confirming sets `confirmed`, records `confirmed_at`, clears the confirm token `src: Core features rule 97`
- [ ] `C-CF-257` `literal` A used or unknown confirm token answers `303` to `/<locale>/newsletter/expired` `src: Core features rule 97`
- [ ] `C-CF-258` `capability` The expired page offers to sign up again `src: Core features rule 97`
- [ ] `C-CF-259` `literal` Subscriber messages carry `List-Unsubscribe` with `List-Unsubscribe-Post` headers `src: Core features rule 98`
- [ ] `C-CF-260` `constraint` The unsubscribe token is never derived from the address `src: Core features rule 98`
- [ ] `C-CF-261` `literal` `GET /api/subscriber/unsubscribe?token=` unsubscribes at once, answering `303` to `/<locale>/newsletter/unsubscribed` `src: Core features rule 99`
- [ ] `C-CF-262` `literal` `POST /api/subscriber/unsubscribe` with a token answers `204` `src: Core features rule 99`
- [ ] `C-CF-263` `constraint` Unconfirmed subscribers older than fourteen days are deleted `src: Core features rule 100`
- [ ] `C-CF-264` `constraint` The site never composes or sends campaigns `src: Core features rule 101`
- [ ] `C-CF-265` `literal` The contact mode asks for `First Name`, `Last Name`, `Email`, `Country`, `Message` `src: Core features rule 102`
- [ ] `C-CF-266` `capability` `Get in contact` opens the contact modal `src: Core features rule 102`
- [ ] `C-CF-267` `literal` `POST /api/lead/contact` answers `202` with a `requestId` `src: Core features rule 103`
- [ ] `C-CF-268` `capability` A contact writes one `lead` of kind `contact` `src: Core features rule 103`
- [ ] `C-CF-269` `literal` Lead forms show a privacy sentence opening `I have read` `src: Core features rule 104`
- [ ] `C-CF-270` `constraint` The privacy box starts unticked `src: Core features rule 104`
- [ ] `C-CF-271` `constraint` A submission without privacy consent is refused `src: Core features rule 104`
- [ ] `C-CF-272` `literal` `consent_text_hash` holds the lowercase hexadecimal SHA-256 of the displayed sentence `src: Core features rule 105`
- [ ] `C-CF-273` `constraint` A `consent.textHash` that differs from the held sentence is refused `src: Core features rule 105`
- [ ] `C-CF-274` `constraint` An email address needs a local part, one `@`, a dotted domain with a two-character final label `src: Core features rule 106`
- [ ] `C-CF-275` `constraint` An email address holds at most `254` characters `src: Core features rule 106`
- [ ] `C-CF-276` `capability` Every form rejects invalid input inline, naming the field `src: Core features rule 107`
- [ ] `C-CF-277` `literal` The server refuses an invalid body with `422` with an `error.fields` map `src: Core features rule 107`
- [ ] `C-CF-278` `literal` An unknown property or malformed JSON is refused with `400` `src: Core features rule 107`
- [ ] `C-CF-279` `capability` An untouched field is never marked before the first submit `src: Core features rule 107`
- [ ] `C-CF-280` `capability` Submitting moves focus to the first invalid control `src: Core features rule 107`
- [ ] `C-CF-281` `constraint` The submit control stays enabled on invalid input `src: Core features rule 107`
- [ ] `C-CF-282` `literal` Lead forms carry a decoy field named `website`, sent as `meta.website` `src: Core features rule 108`
- [ ] `C-CF-283` `constraint` A filled decoy answers as a success, writing nothing `src: Core features rule 108`
- [ ] `C-CF-284` `literal` Forms fetch `GET /api/form-token`, sending `meta.formToken` `src: Core features rule 109`
- [ ] `C-CF-285` `constraint` A submission made under 1.5 seconds after its token was issued writes nothing `src: Core features rule 109`
- [ ] `C-CF-286` `constraint` A missing or forged form token is refused `src: Core features rule 109`
- [ ] `C-CF-287` `constraint` Every lead endpoint requires an `idempotencyKey` of at least 16 characters `src: Core features rule 110`
- [ ] `C-CF-288` `literal` A repeat with the same key returns the first answer with `Idempotent-Replayed: true` `src: Core features rule 110`
- [ ] `C-CF-289` `literal` The same key with a different body answers `409` with `idempotency_conflict` `src: Core features rule 110`
- [ ] `C-CF-290` `constraint` Two simultaneous requests with one key produce exactly one lead `src: Core features rule 110`
- [ ] `C-CF-291` `literal` An address may make at most `5` lead submissions per hour `src: Core features rule 111`
- [ ] `C-CF-292` `literal` An address may make at most `3` newsletter sign-ups per twenty-four hours `src: Core features rule 111`
- [ ] `C-CF-293` `literal` A limited submission answers `429` with `Retry-After` with `error.retryAfterSeconds` above zero `src: Core features rule 111`
- [ ] `C-CF-294` `capability` The rate-limit message names the wait in minutes with the enquiry address `src: Core features rule 111`
- [ ] `C-CF-295` `constraint` An unreachable counter store refuses submissions, leaving browsing working `src: Core features rule 111`
- [ ] `C-CF-296` `literal` A message with more than two links is stored as `quarantined` `src: Core features rule 112`
- [ ] `C-CF-297` `constraint` A mostly non-Latin message is stored as quarantined `src: Core features rule 112`
- [ ] `C-CF-298` `constraint` A quarantined enquiry sends no email until released `src: Core features rule 112`
- [ ] `C-CF-299` `literal` Releasing moves a quarantined enquiry to `received` `src: Core features rule 112`
- [ ] `C-CF-300` `constraint` Only the decoy path discards a submission `src: Core features rule 113`
- [ ] `C-CF-301` `capability` Validation, rate limiting, failed save, success each show different wording `src: Core features rule 114`
- [ ] `C-CF-302` `literal` A failed save answers `503`, keeping the form intact `src: Core features rule 114`
- [ ] `C-CF-303` `literal` Mail goes over SMTP to `mailpit` at `SMTP_HOST`, `SMTP_PORT` `src: Core features rule 115`
- [ ] `C-CF-304` `literal` Mail comes from `Verdea <hello@verdea-outdoor.com>` `src: Core features rule 115`
- [ ] `C-CF-305` `constraint` Each message has exactly one recipient, no cc, no bcc `src: Core features rule 115`
- [ ] `C-CF-306` `constraint` Messages carry no tracking pixel, no rewritten link `src: Core features rule 115`
- [ ] `C-CF-307` `literal` A lead moves `received`, `queued`, then `delivered` `src: Core features rule 116`
- [ ] `C-CF-308` `literal` Delivery means the notification to `commercial@example.com` was accepted, setting `delivered_at` `src: Core features rule 116`
- [ ] `C-CF-309` `literal` A lead whose notification keeps failing ends `failed` `src: Core features rule 116`
- [ ] `C-CF-310` `constraint` No SMTP call runs inside the accepting request `src: Core features rule 116`
- [ ] `C-CF-311` `literal` The contact notification subject is `New enquiry received` `src: Core features rule 117`
- [ ] `C-CF-312` `literal` The quotation notification subject is `New quotation: ` plus the reference `src: Core features rule 117`
- [ ] `C-CF-313` `literal` The file notification subject is `New file request: ` plus the document name `src: Core features rule 117`
- [ ] `C-CF-314` `constraint` A contact notification carries a `/office/leads/<id>` link, never the message or email `src: Core features rule 117`
- [ ] `C-CF-315` `constraint` A quotation notification lists the lines, never the fiscal number or city `src: Core features rule 117`
- [ ] `C-CF-316` `constraint` The visitor confirmation is sent once on the transition into `delivered` `src: Core features rule 118`
- [ ] `C-CF-317` `literal` The contact confirmation subject is `Verdea enquiry received` `src: Core features rule 118`
- [ ] `C-CF-318` `capability` The contact confirmation restates the message `src: Core features rule 118`
- [ ] `C-CF-319` `literal` The quotation confirmation subject is `Quotation request received: ` plus the reference `src: Core features rule 118`
- [ ] `C-CF-320` `capability` The quotation confirmation lists every line with every chosen option `src: Core features rule 118`
- [ ] `C-CF-321` `literal` The grant email subject is `Your Verdea download: ` plus the document name `src: Core features rule 119`
- [ ] `C-CF-322` `capability` The grant email carries the full `/api/files/<token>` link `src: Core features rule 119`
- [ ] `C-CF-323` `literal` The newsletter confirmation subject is `Confirm your Verdea newsletter subscription` `src: Core features rule 120`
- [ ] `C-CF-324` `capability` The newsletter confirmation carries the full confirmation link `src: Core features rule 120`
- [ ] `C-CF-325` `constraint` A decoy, too-fresh, refused or quarantined submission sends no mail `src: Core features rule 121`
- [ ] `C-CF-326` `constraint` A repeated idempotent request sends no second mail `src: Core features rule 121`
- [ ] `C-CF-327` `constraint` An SMTP failure never turns an accepted submission into a visitor error `src: Core features rule 122`
- [ ] `C-CF-328` `constraint` Transactional mail with newsletter mail use different sending subdomains `src: Core features rule 122`
- [ ] `C-CF-329` `literal` `GET /api/search` answers `products` with `pages` groups `src: Core features rule 123`
- [ ] `C-CF-330` `constraint` The `type` parameter restricts results to `product`, `article` or `page` `src: Core features rule 123`
- [ ] `C-CF-331` `constraint` Each search group holds at most eight results `src: Core features rule 123`
- [ ] `C-CF-332` `constraint` A query under two characters is refused as invalid `src: Core features rule 124`
- [ ] `C-CF-333` `constraint` A query is trimmed, cut to 100 characters `src: Core features rule 124`
- [ ] `C-CF-334` `literal` `tee sig` already finds `Tee Sign Heritage` `src: Core features rule 124`
- [ ] `C-CF-335` `literal` `praca` in `pt` finds `Banco Praça Longo` `src: Core features rule 125`
- [ ] `C-CF-336` `literal` `salida` in `es` finds `Señal de Salida Heritage` `src: Core features rule 125`
- [ ] `C-CF-337` `literal` `depart` in `fr` finds `Panneau de Départ Heritage` `src: Core features rule 125`
- [ ] `C-CF-338` `literal` The query `(bench` answers normally `src: Core features rule 126`
- [ ] `C-CF-339` `constraint` A query with angle brackets comes back as plain text `src: Core features rule 126`
- [ ] `C-CF-340` `capability` Dropdown results appear after two characters once typing settles `src: Core features rule 127`
- [ ] `C-CF-341` `capability` A search with no results shows one announced message offering the catalogue `src: Core features rule 127`
- [ ] `C-CF-342` `ui` Previous results stay dimmed during a new query `src: Core features rule 127`
- [ ] `C-CF-343` `ui` The matched part of each result is emphasised `src: Core features rule 128`
- [ ] `C-CF-344` `capability` Arrow keys move the highlight, Enter opens the highlighted result `src: Core features rule 129`
- [ ] `C-CF-345` `capability` A first Escape closes the dropdown, a second collapses the field `src: Core features rule 129`
- [ ] `C-CF-346` `constraint` An unpublished product leaves search at once `src: Core features rule 130`
- [ ] `C-CF-347` `literal` The journal chips are `All`, `Press releases`, `Sustainability`, `Case Studies`, `Products`, `Educational`, `Institutional` `src: Core features rule 131`
- [ ] `C-CF-348` `capability` `Institutional` shows as an unavailable chip in English `src: Core features rule 131`
- [ ] `C-CF-349` `capability` The journal index shows `Latest Articles`, the featured rail, per-category blocks `src: Core features rule 131`
- [ ] `C-CF-350` `literal` The English journal counts are `13` Case Studies, `2` Sustainability, `2` Products, `1` Educational, `1` Press releases, `0` Institutional `src: Core features rule 132`
- [ ] `C-CF-351` `literal` The journal holds `19` articles in `pt`, `en`, `es`, `18` in `fr` `src: Core features rule 132`
- [ ] `C-CF-352` `literal` The Portuguese Case Studies route is `/pt/jornal/casos-de-estudo` `src: Core features rule 132`
- [ ] `C-CF-353` `capability` A category route lists articles newest first, twelve per page `src: Core features rule 133`
- [ ] `C-CF-354` `literal` A later category page adds `?page=2` with a canonical link to itself `src: Core features rule 133`
- [ ] `C-CF-355` `constraint` The paginator is absent when a category has one page `src: Core features rule 133`
- [ ] `C-CF-356` `literal` `GET /api/articles` returns at most twelve projections with `X-Total-Count` `src: Core features rule 134`
- [ ] `C-CF-357` `literal` `GET /api/categories?locale=en` returns the six categories with counts `src: Core features rule 134`
- [ ] `C-CF-358` `capability` An empty category route offers the Portuguese version, never not-found `src: Core features rule 135`
- [ ] `C-CF-359` `capability` An unknown category segment answers the not-found page `src: Core features rule 135`
- [ ] `C-CF-360` `literal` `Ridge Viewpoint Boardwalk` dated `2026-05-12` is the newest article `src: Core features rule 136`
- [ ] `C-CF-361` `literal` The next newest English articles are `recycled-plastic-explained`, `hpl-in-the-open-air`, `verdea-opens-spanish-establishment` `src: Core features rule 136`
- [ ] `C-CF-362` `literal` `why-galvanised-steel-lasts` is the Educational article `src: Core features rule 136`
- [ ] `C-CF-363` `literal` An article shows reading time as `<n>min Read` `src: Core features rule 137`
- [ ] `C-CF-364` `capability` Reading time is plain length over five over 180, never below one `src: Core features rule 137`
- [ ] `C-CF-365` `literal` `Ridge Viewpoint Boardwalk` credits read `Client: Municipality of Alvora`, `Design: Atra` `src: Core features rule 137`
- [ ] `C-CF-366` `literal` The Ridge gallery holds five images, showing `+2` beside `View gallery` `src: Core features rule 137`
- [ ] `C-CF-367` `literal` The article detail returns `readingMinutes`, `galleryCount`, `credits`, `relatedArticles`, `relatedProducts` `src: Core features rule 138`
- [ ] `C-CF-368` `capability` A one-image figure set renders as a figure `src: Core features rule 139`
- [ ] `C-CF-369` `constraint` Article links outside `https`, `mailto`, `tel` render as plain text `src: Core features rule 140`
- [ ] `C-CF-370` `constraint` Mixed-language body text renders exactly as authored `src: Core features rule 141`
- [ ] `C-CF-371` `literal` Careers lists `CNC Operator`, `Serralheiro Civil`, `Project Manager`, `Installation Technician` `src: Core features rule 142`
- [ ] `C-CF-372` `literal` The `Serralheiro Civil` row declares the language `pt` `src: Core features rule 142`
- [ ] `C-CF-373` `capability` An apply control opens the external recruitment site `src: Core features rule 142`
- [ ] `C-CF-374` `constraint` The site has no application form, no upload `src: Core features rule 142`
- [ ] `C-CF-375` `capability` `/en/careers/<id>` shows one position with its apply control `src: Core features rule 143`
- [ ] `C-CF-376` `capability` The home `Recent News` shows the three most recent articles `src: Core features rule 144`
- [ ] `C-CF-377` `literal` `/en/products/golf/tee-sign-heritage.md` returns the page as markdown `src: Core features rule 145`
- [ ] `C-CF-378` `literal` `/llms.txt` lists the markdown pages `src: Core features rule 145`
- [ ] `C-CF-379` `literal` A first visit shows a banner offering `Accept all`, `Reject all`, `Choose` `src: Core features rule 146`
- [ ] `C-CF-380` `constraint` Closing the consent banner is not consent `src: Core features rule 146`
- [ ] `C-CF-381` `literal` A choice is stored in `verdea_consent` as comma-separated categories `src: Core features rule 147`
- [ ] `C-CF-382` `literal` `POST /api/consent` writes an append-only `consent_receipt` `src: Core features rule 147`
- [ ] `C-CF-383` `constraint` A changed consent choice writes a new receipt `src: Core features rule 147`
- [ ] `C-CF-384` `capability` A persistent consent control reopens the banner on every route `src: Core features rule 148`
- [ ] `C-CF-385` `capability` The site stays usable with every optional category refused `src: Core features rule 149`
- [ ] `C-CF-386` `constraint` No full network address is stored `src: Core features rule 150`
- [ ] `C-CF-387` `literal` The legal pages are `/en/legal/privacy-policy`, `/en/legal/cookie-policy`, `/en/legal/terms-of-use` `src: Core features rule 151`
- [ ] `C-CF-388` `literal` `/en/legal/privacy-policy/v/1` shows a banner ending `version has been superseded.` `src: Core features rule 152`
- [ ] `C-CF-389` `constraint` A legal version that never existed answers not found `src: Core features rule 152`
- [ ] `C-CF-390` `capability` The current privacy policy links to its previous version `src: Core features rule 152`
- [ ] `C-CF-391` `capability` A legal page with more than four second-level headings shows a contents list `src: Core features rule 153`
- [ ] `C-CF-392` `capability` Each legal heading carries a stable anchor `src: Core features rule 153`
- [ ] `C-CF-393` `literal` An unknown address answers `404` with the product's own not-found page `src: Core features rule 154`
- [ ] `C-CF-394` `literal` The not-found page links `/en/products`, `/en/journal`, `/en` `src: Core features rule 154`
- [ ] `C-CF-395` `constraint` The not-found page never redirects on its own `src: Core features rule 154`
- [ ] `C-CF-396` `capability` The not-found page names a near destination first when one exists `src: Core features rule 155`
- [ ] `C-CF-397` `constraint` A malformed slug answers not-found without a content lookup `src: Core features rule 156`
- [ ] `C-CF-398` `capability` An app failure answers `500` with the request identifier `src: Core features rule 157`
- [ ] `C-CF-399` `constraint` No page shows a stack trace, `undefined`, `null`, `NaN` `src: Core features rule 157`
- [ ] `C-CF-400` `ui` Not-found with error pages carry no live object, sound or scroll motion `src: Core features rule 158`
- [ ] `C-CF-401` `literal` The back office screens are `/office/leads`, `/office/leads/<id>`, `/office/subscribers`, `/office/products` `src: Core features rule 159`
- [ ] `C-CF-402` `literal` `GET /api/office/me` returns `email`, `role`, `displayName` `src: Core features rule 160`
- [ ] `C-CF-403` `literal` `GET /api/office/leads/summary` returns counts for both roles `src: Core features rule 161`
- [ ] `C-CF-404` `literal` `GET /api/office/leads` returns enquiries for `commercial`, denying `editor` `src: Core features rule 162`
- [ ] `C-CF-405` `literal` `GET /api/office/leads/<id>` returns the enquiry with its lines for `commercial` `src: Core features rule 163`
- [ ] `C-CF-406` `literal` Each commercial enquiry read writes the audit action `lead.read` `src: Core features rule 163`
- [ ] `C-CF-407` `constraint` An `editor` enquiry read is denied with nothing recorded as read `src: Core features rule 163`
- [ ] `C-CF-408` `literal` The release endpoint writes `lead.release` `src: Core features rule 164`
- [ ] `C-CF-409` `constraint` Releasing a lead that is not quarantined is refused `src: Core features rule 164`
- [ ] `C-CF-410` `literal` The subscriber list writes `subscriber.list` for `commercial` only `src: Core features rule 165`
- [ ] `C-CF-411` `literal` `GET /api/office/subscribers/summary` returns counts for both roles `src: Core features rule 165`
- [ ] `C-CF-412` `literal` `GET /api/office/products?locale=` returns every product with its publish state `src: Core features rule 166`
- [ ] `C-CF-413` `literal` Unpublish writes `product.unpublish`, publish writes `product.publish` `src: Core features rule 167`
- [ ] `C-CF-414` `constraint` A `commercial` publish request is denied with the state unchanged `src: Core features rule 167`
- [ ] `C-CF-415` `capability` An unpublished product leaves its locale catalogue, total, sitemap at once `src: Core features rule 168`
- [ ] `C-CF-416` `capability` Republishing restores the product everywhere `src: Core features rule 168`
- [ ] `C-CF-417` `constraint` The app never edits or deletes an audit event `src: Core features rule 169`
- [ ] `C-CF-418` `capability` The enquiry table filters by kind with status `src: Core features rule 170`
- [ ] `C-CF-419` `capability` Quarantined or failed enquiries are marked by a word `src: Core features rule 170`
- [ ] `C-CF-420` `capability` The enquiry detail offers a control copying the rendered payload `src: Core features rule 170`

## C-UF User flow

- [ ] `C-UF-01` `literal` The route table lists `/en/products/golf/tee-sign-heritage` as a product route `src: User flow route table`
- [ ] `C-UF-02` `literal` `/sitemap.xml` lists `/sitemap-pt.xml`, `/sitemap-en.xml`, `/sitemap-es.xml`, `/sitemap-fr.xml` `src: User flow route table`
- [ ] `C-UF-03` `literal` `/pt/produtos/detalhes/placa-de-sala-slim` is a Portuguese product route `src: User flow route table`
- [ ] `C-UF-04` `literal` The newsletter outcome routes are `/en/newsletter/confirmed`, `/en/newsletter/expired`, `/en/newsletter/unsubscribed` `src: User flow route table`
- [ ] `C-UF-05` `capability` Every modal opens over the current route without changing the path `src: User flow entry and redirects`
- [ ] `C-UF-06` `capability` The back gesture closes an open modal `src: User flow entry and redirects`
- [ ] `C-UF-07` `capability` A session expiring mid-action returns to `/office/login` remembering the page `src: User flow entry and redirects`
- [ ] `C-UF-08` `capability` A staff member on a screen the role may not use sees a denial naming the action `src: User flow entry and redirects`
- [ ] `C-UF-09` `capability` Signing out returns to `/office/login` `src: User flow entry and redirects`
- [ ] `C-UF-10` `capability` Every navigation control is a real link, falling back to a full page load `src: User flow entry and redirects`
- [ ] `C-UF-11` `capability` The specifier journey ends on a confirmation showing a `VQ-` reference `src: User flow journey 1`
- [ ] `C-UF-12` `capability` The document journey shows `Tee Sign Heritage technical files` with a download control `src: User flow journey 3`
- [ ] `C-UF-13` `literal` The language journey lands on `/es/productos/golf/senal-de-salida-heritage` `src: User flow journey 5`
- [ ] `C-UF-14` `capability` The reader journey opens the gallery, moves with arrow keys, closes with Escape `src: User flow journey 6`
- [ ] `C-UF-15` `capability` A related product link on the article leads to `Boardwalk Module` `src: User flow journey 6`
- [ ] `C-UF-16` `capability` The search journey lands on `Tee Sign Heritage` after Enter `src: User flow journey 8`
- [ ] `C-UF-17` `capability` The editor journey unpublishes then republishes `Golf Bag Stand` in `pt` `src: User flow journey 10`
- [ ] `C-UF-18` `capability` Every list offers a designed empty state `src: User flow states`
- [ ] `C-UF-19` `capability` Every loading state resolves into a result or a message `src: User flow states`
- [ ] `C-UF-20` `capability` A failing section removes itself, leaving the page working `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The first impression conveys durable outdoor objects resting on a table `src: UI/UX notes north star`
- [ ] `C-UX-02` `ui` Wishlist, forms, back office switch to a quiet working register `src: UI/UX notes register`
- [ ] `C-UX-03` `ui` Products appear as renders, photography reserved for places, projects, people `src: UI/UX notes stances`
- [ ] `C-UX-04` `ui` The page ground is a warm off-white nearer paper than white `src: UI/UX notes palette`
- [ ] `C-UX-05` `ui` Card tiles are a warm neutral one step deeper than the page `src: UI/UX notes palette`
- [ ] `C-UX-06` `ui` All text uses one almost-black ink with a warm cast `src: UI/UX notes palette`
- [ ] `C-UX-07` `ui` The fluorescent yellow appears rarely as the brand signal `src: UI/UX notes palette`
- [ ] `C-UX-08` `ui` Each collection accent appears only on its own pill or chapter `src: UI/UX notes palette`
- [ ] `C-UX-09` `ui` The failure red appears only for form errors `src: UI/UX notes palette`
- [ ] `C-UX-10` `ui` Every colour pairing meets the contrast floors `src: UI/UX notes palette`
- [ ] `C-UX-11` `literal` The header themes are `dark`, `light`, `fluor` `src: UI/UX notes themes`
- [ ] `C-UX-12` `ui` The header cross-fades between themes as sections pass beneath `src: UI/UX notes themes`
- [ ] `C-UX-13` `ui` One geometric sans at one regular thickness carries the site, never bold `src: UI/UX notes typography`
- [ ] `C-UX-14` `ui` Type sizes grow with the viewport between a floor with a ceiling `src: UI/UX notes typography`
- [ ] `C-UX-15` `ui` Only pill with softly rounded rectangle shapes appear, plus circles `src: UI/UX notes shape`
- [ ] `C-UX-16` `ui` Product tiles carry no box shadow `src: UI/UX notes shape`
- [ ] `C-UX-17` `ui` Panel fades run a colour into its own transparent form `src: UI/UX notes shape`
- [ ] `C-UX-18` `ui` Public sections read as separate without dividing lines `src: UI/UX notes density`
- [ ] `C-UX-19` `ui` Movement shares one curve that leaves fast, settling long, near half a second `src: UI/UX notes motion`
- [ ] `C-UX-20` `ui` Entrances rise a short distance, fading in once `src: UI/UX notes motion`
- [ ] `C-UX-21` `ui` Every element stays visible if motion never starts `src: UI/UX notes motion`
- [ ] `C-UX-22` `ui` Reduced motion stops every reveal, keeping only the header colour cross-fade `src: UI/UX notes motion`
- [ ] `C-UX-23` `ui` Each page leads with one ink-filled primary action `src: UI/UX notes primary action`
- [ ] `C-UX-24` `ui` Below tablet width the header pills become a menu mark `src: UI/UX notes responsive`
- [ ] `C-UX-25` `ui` The catalogue shows four across, two on a tablet, one on a phone `src: UI/UX notes responsive`
- [ ] `C-UX-26` `ui` Nothing scrolls sideways at a narrow viewport `src: UI/UX notes responsive`
- [ ] `C-UX-27` `ui` A visible focus ring appears around every focused control `src: UI/UX notes accessibility`
- [ ] `C-UX-28` `literal` Body text contrast is at least `4.5:1`, large text `3:1` `src: UI/UX notes accessibility`
- [ ] `C-UX-29` `literal` Touch targets measure at least `44` by `44` CSS pixels `src: UI/UX notes accessibility`
- [ ] `C-UX-30` `ui` Every icon-only control carries a label `src: UI/UX notes accessibility`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The backend is NestJS on Node.js 20 in one production build `src: Technical requirements stack`
- [ ] `C-TR-02` `capability` A request without script receives the page headings, copy, links `src: Technical requirements stack`
- [ ] `C-TR-03` `contract` The frontend is Lit components bundled with Vite `src: Technical requirements stack`
- [ ] `C-TR-04` `contract` The database is `postgres`, read from `DATABASE_URL` `src: Technical requirements stack`
- [ ] `C-TR-05` `contract` Mail uses `mailpit`, read from `SMTP_HOST`, `SMTP_PORT` `src: Technical requirements stack`
- [ ] `C-TR-06` `contract` The app introduces no second database, cache, queue or mail vendor `src: Technical requirements stack`
- [ ] `C-TR-07` `contract` Signing keys are generated by the app, kept in its database `src: Technical requirements stack`
- [ ] `C-TR-08` `literal` `GET /api/health` answers `200` with `{"status": "ok"}` once the database is reachable `src: Technical requirements health`
- [ ] `C-TR-09` `contract` Content is seeded into the app database with one document per locale `src: Technical requirements content`
- [ ] `C-TR-10` `contract` A missing page section renders nothing rather than an error `src: Technical requirements content`
- [ ] `C-TR-11` `contract` Media is generated by the app, shipping no binary asset `src: Technical requirements content`
- [ ] `C-TR-12` `contract` A write endpoint commits the record before any SMTP call `src: Technical requirements background work`
- [ ] `C-TR-13` `contract` A lead status change moves from a named state to a named state `src: Technical requirements background work`
- [ ] `C-TR-14` `literal` Every response carries `Strict-Transport-Security` with `includeSubDomains` `src: Technical requirements security`
- [ ] `C-TR-15` `literal` Every response carries `X-Content-Type-Options: nosniff` `src: Technical requirements security`
- [ ] `C-TR-16` `literal` Every response carries `Referrer-Policy: strict-origin-when-cross-origin` `src: Technical requirements security`
- [ ] `C-TR-17` `literal` A `Permissions-Policy` denies camera, microphone, geolocation, payment `src: Technical requirements security`
- [ ] `C-TR-18` `literal` Every response carries `Cross-Origin-Opener-Policy: same-origin` `src: Technical requirements security`
- [ ] `C-TR-19` `literal` The `Content-Security-Policy` sets `frame-ancestors 'none'` `src: Technical requirements security`
- [ ] `C-TR-20` `literal` The `script-src` allows neither `'unsafe-inline'` nor `'unsafe-eval'` `src: Technical requirements security`
- [ ] `C-TR-21` `contract` No browser-downloadable file contains a database address, password or signing key `src: Technical requirements security`
- [ ] `C-TR-22` `contract` Route slugs are validated before any content lookup `src: Technical requirements security`
- [ ] `C-TR-23` `contract` Search input is escaped before any pattern is built `src: Technical requirements security`
- [ ] `C-TR-24` `contract` No telephone number is collected by any form `src: Technical requirements privacy`
- [ ] `C-TR-25` `contract` No log record contains an email, name, message, token or raw network address `src: Technical requirements observability`
- [ ] `C-TR-26` `literal` Every response carries the request identifier in `X-Request-Id` `src: Technical requirements observability`
- [ ] `C-TR-27` `literal` `/robots.txt` disallows `/api/` with `/office`, naming the sitemap `src: Technical requirements generated documents`
- [ ] `C-TR-28` `contract` Each per-locale sitemap lists published routes with `hreflang` alternates `src: Technical requirements generated documents`
- [ ] `C-TR-29` `contract` A browser running no script still reads every public route `src: Technical requirements failure order`
- [ ] `C-TR-30` `contract` Offline, a previously visited route opens with a dismissible connection line `src: Technical requirements offline`
- [ ] `C-TR-31` `contract` Offline, a form submission is refused with values kept, never queued `src: Technical requirements offline`

## C-DM Data model

- [ ] `C-DM-01` `data` Record identifiers are opaque, never sequential integers in routes or payloads `src: Data model para 1`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`, hashed `src: Data model password paragraph`
- [ ] `C-DM-03` `contract` The seeded logins are written into `/app/USER_README.md` `src: Data model password paragraph`
- [ ] `C-DM-04` `data` `lead` carries `kind`, `locale`, `status`, `consent_privacy`, `consent_text_hash`, `delivered_at` `src: Data model lead`
- [ ] `C-DM-05` `data` A `delivered` lead has `delivered_at`, any other status has none `src: Data model lead`
- [ ] `C-DM-06` `data` `quotation` carries `lead_id`, `reference`, `item_count`, `payload_rendered`, `payload_hash` `src: Data model quotation`
- [ ] `C-DM-07` `data` `quotation_item` carries `position`, `product_id`, `product_slug`, `product_title`, `collection_name` `src: Data model quotation_item`
- [ ] `C-DM-08` `data` `quotation_item.position` runs from 1 without gaps `src: Data model quotation_item`
- [ ] `C-DM-09` `data` `file_request` carries `scope`, `document_name`, `token`, `token_expires_at`, `download_count` `src: Data model file_request`
- [ ] `C-DM-10` `data` `subscriber` carries `status`, `confirm_token`, `confirmed_at`, `unsubscribe_token` `src: Data model subscriber`
- [ ] `C-DM-11` `data` `consent_receipt` carries `categories`, `policy_version`, `ip_hash`, `user_agent_family` `src: Data model consent_receipt`
- [ ] `C-DM-12` `data` `staff_account` carries `email`, `display_name`, `role`, `status` `src: Data model staff_account`
- [ ] `C-DM-13` `data` `audit_event` carries `actor_type`, `action`, `subject_type`, `subject_id`, `request_id` `src: Data model audit_event`
- [ ] `C-DM-14` `data` Idempotency answers are kept for twenty-four hours `src: Data model idempotency_record`
- [ ] `C-DM-15` `data` A size label is opaque text, never parsed or sorted `src: Data model content`
- [ ] `C-DM-16` `literal` Collection identifiers are `urban`, `nature`, `repolymer`, `golf`, `details` `src: Data model seed data`
- [ ] `C-DM-17` `literal` Product type slugs are `signage`, `construction`, `furniture`, `equipment` `src: Data model seed data`
- [ ] `C-DM-18` `literal` The pinned products include `vd-tee-sign-heritage`, `vd-plaza-bench-long`, `vd-slim-room-sign` `src: Data model seed data`
- [ ] `C-DM-19` `literal` `vd-plaza-bench-long` is `Banco Praça Longo` at `banco-praca-longo` in Portuguese `src: Data model seed data`
- [ ] `C-DM-20` `literal` `vd-tee-sign-heritage` is `senal-de-salida-heritage` in Spanish, `panneau-de-depart-heritage` in French `src: Data model seed data`
- [ ] `C-DM-21` `literal` `vd-slim-room-sign` is `Placa de Sala Slim` at `placa-de-sala-slim` in Portuguese `src: Data model seed data`
- [ ] `C-DM-22` `literal` `Bike Parking Totem` callouts read `2 Schuko Plugs`, `Shimano Standard Charger`, `Bosch Standard Charger` `src: Data model seed data`
- [ ] `C-DM-23` `literal` Legal seeds are `privacy-policy` versions 1, 2 with `cookie-policy`, `terms-of-use` `src: Data model seed data`
- [ ] `C-DM-24` `data` Restarting the app never duplicates seeded rows `src: Data model seed data`
- [ ] `C-DM-25` `data` Schema changes ship as ordered forward-only migrations `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` The header element carries `data-theme` with the server-rendered value `fluor` on sustainability `src: Front-end specification global chrome header`
- [ ] `C-FE-02` `ui` The header never scrolls away, shrinks or changes height `src: Front-end specification global chrome header`
- [ ] `C-FE-03` `literal` Navigation pills read `Products`, `About`, `Sustainability`, `Journal` in that order `src: Front-end specification global chrome navigation`
- [ ] `C-FE-04` `ui` The pills abut as a segmented control, the current one ink-filled `src: Front-end specification global chrome navigation`
- [ ] `C-FE-05` `ui` The search field widens sideways as its placeholder fades out then back `src: Front-end specification global chrome search`
- [ ] `C-FE-06` `capability` The language selector is a menu marking the current locale `src: Front-end specification global chrome language selector`
- [ ] `C-FE-07` `ui` The mobile menu mark is three bars offset into a slant `src: Front-end specification global chrome mobile menu`
- [ ] `C-FE-08` `ui` A modal panel keeps its height when switching between tabs `src: Front-end specification global chrome modal shell`
- [ ] `C-FE-09` `ui` An open modal locks the page without moving the page `src: Front-end specification global chrome modal shell`
- [ ] `C-FE-10` `ui` The footer is a full-screen yellow field with an enormous cropped wordmark `src: Front-end specification global chrome footer`
- [ ] `C-FE-11` `literal` The footer headings read `Headquarters`, `Production`, `Verdea Spain` `src: Front-end specification global chrome footer`
- [ ] `C-FE-12` `literal` The footer shows `Call to a national landline` beside `+351 234 600 118` `src: Front-end specification global chrome footer`
- [ ] `C-FE-13` `literal` The footer links read `Careers`, `Complaints Book`, `Privacy Policy`, with `Made by Atra` `src: Front-end specification global chrome footer`
- [ ] `C-FE-14` `ui` The funding marks sit in a separate band on the page ground `src: Front-end specification global chrome footer`
- [ ] `C-FE-15` `ui` The consent badge sits in a lower corner without covering a primary control `src: Front-end specification global chrome consent badge`
- [ ] `C-FE-16` `capability` Outbound links carry an external mark, opening elsewhere `src: Front-end specification global chrome outbound links`
- [ ] `C-FE-17` `capability` The sound control is present on every route, reachable by keyboard `src: Front-end specification global chrome sound control`
- [ ] `C-FE-18` `ui` Icons are inline drawings in the current text colour `src: Front-end specification iconography`
- [ ] `C-FE-19` `ui` Each collection mark shares one grid with one line thickness `src: Front-end specification iconography`
- [ ] `C-FE-20` `ui` Display headlines assemble a word at a time `src: Front-end specification motion moments`
- [ ] `C-FE-21` `ui` Photographs are revealed by a window opening from one edge `src: Front-end specification motion moments`
- [ ] `C-FE-22` `ui` Inside each window the image drifts more slowly than its frame `src: Front-end specification motion moments`
- [ ] `C-FE-23` `ui` A dappled leaf shadow drifts so slowly over some photographs that the change reads as light `src: Front-end specification motion moments`
- [ ] `C-FE-24` `ui` The arrow beside `Scroll to Explore` bobs gently on the first screen only `src: Front-end specification motion moments`
- [ ] `C-FE-25` `ui` A ring pulses outward from the rotate control `src: Front-end specification motion moments`
- [ ] `C-FE-26` `ui` A chosen swatch swells slightly then settles `src: Front-end specification motion moments`
- [ ] `C-FE-27` `ui` A pale page-transition panel stops most of the way across, then completes `src: Front-end specification motion moments`
- [ ] `C-FE-28` `ui` The header takes the new theme when the transition panel is widest `src: Front-end specification motion moments`
- [ ] `C-FE-29` `ui` Keyboard scrolling, find-in-page, anchor jumps keep working with smooth scrolling `src: Front-end specification scrolling and restoration`
- [ ] `C-FE-30` `ui` A back navigation restores the previous scroll position `src: Front-end specification scrolling and restoration`
- [ ] `C-FE-31` `literal` The home headline reads `Spaces for people, made for life.` `src: Front-end specification home`
- [ ] `C-FE-32` `ui` The home field scatters product renders drifting with the pointer `src: Front-end specification home`
- [ ] `C-FE-33` `literal` The first chapter headline ends `for welcoming urban spaces` `src: Front-end specification home`
- [ ] `C-FE-34` `literal` Chapter controls read like `See Urban Products` `src: Front-end specification home`
- [ ] `C-FE-35` `ui` The five chapters keep an index with a filling rule in the left margin `src: Front-end specification home`
- [ ] `C-FE-36` `literal` The home ends on `Made to last, designed to endure.` `src: Front-end specification home`
- [ ] `C-FE-37` `literal` The catalogue heading reads `Our products are made to last. Take your time exploring.` `src: Front-end specification catalogue index`
- [ ] `C-FE-38` `literal` The collection catalogue card reads `PDF` with `Download Urban Catalogue` `src: Front-end specification catalogue index`
- [ ] `C-FE-39` `ui` The floating filter control carries a soft short shadow `src: Front-end specification catalogue index`
- [ ] `C-FE-40` `ui` The product object sits on a ground plane matching the page exactly `src: Front-end specification product route`
- [ ] `C-FE-41` `ui` Dragging orbits the object horizontally within a narrow vertical band `src: Front-end specification product route`
- [ ] `C-FE-42` `ui` The mouse wheel over the object scrolls the page `src: Front-end specification product route`
- [ ] `C-FE-43` `ui` The still image set stays beside the live object `src: Front-end specification product route`
- [ ] `C-FE-44` `ui` Technical drawings show line elevations with dimension lines `src: Front-end specification product route`
- [ ] `C-FE-45` `ui` Below the phone width each specification label sits above its values `src: Front-end specification product route`
- [ ] `C-FE-46` `ui` Single-value option axes appear chosen, inert `src: Front-end specification options modal`
- [ ] `C-FE-47` `ui` Wishlist rows make two configurations of one product visibly different `src: Front-end specification wishlist route`
- [ ] `C-FE-48` `ui` Form errors show under the field with a mark plus words `src: Front-end specification forms`
- [ ] `C-FE-49` `capability` Following the privacy link never toggles the privacy box `src: Front-end specification forms`
- [ ] `C-FE-50` `literal` The about history heading opens `A trail of hard work` `src: Front-end specification about route`
- [ ] `C-FE-51` `ui` The history drags sideways with momentum, years alternating above, below an axis `src: Front-end specification about route`
- [ ] `C-FE-52` `capability` Arrow keys move between history entries `src: Front-end specification about route`
- [ ] `C-FE-53` `literal` The about pillars read `01. Environmental Awareness`, `02. Innovation`, `03. Quality`, `04. Durability` `src: Front-end specification about route`
- [ ] `C-FE-54` `literal` The about route lists `68 members` with eight departments `src: Front-end specification about route`
- [ ] `C-FE-55` `literal` The sustainability headline reads `Built in Portugal. Made for life.` `src: Front-end specification sustainability route`
- [ ] `C-FE-56` `literal` The materials read `Recycled plastic`, `High-pressure laminate`, `Steel` with `LEARN MORE` `src: Front-end specification sustainability route`
- [ ] `C-FE-57` `ui` The materials show large surface texture crops on the deep green ground `src: Front-end specification sustainability route`
- [ ] `C-FE-58` `literal` The highlighted project reads `Ecodesign that empowers` naming `Alvora, Portugal` `src: Front-end specification sustainability route`
- [ ] `C-FE-59` `literal` The journal headline opens `Exploring ideas, insights` `src: Front-end specification journal routes`
- [ ] `C-FE-60` `capability` The featured rail repeats items hidden from assistive technology `src: Front-end specification journal routes`
- [ ] `C-FE-61` `capability` The article gallery opens full-screen with a current-of-total counter `src: Front-end specification journal routes`
- [ ] `C-FE-62` `ui` Legal pages stay plain without scroll-driven reveals `src: Front-end specification careers and legal routes`
- [ ] `C-FE-63` `ui` The not-found page shows a designed image `src: Front-end specification not-found, error and offline pages`
- [ ] `C-FE-64` `ui` Loading images show a flat tone of their own colour without shimmer `src: Front-end specification media`
- [ ] `C-FE-65` `capability` The sound layer stays off until the visitor switches sound on `src: Front-end specification sound`
- [ ] `C-FE-66` `ui` An open modal makes the ambient sound recede slightly `src: Front-end specification sound`
- [ ] `C-FE-67` `capability` For an editor the enquiry screen shows counts with a line saying contents are unavailable `src: Front-end specification back office`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product has one organisation with no tenants, no approvals `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The product has no prices, cart, checkout, payments, orders, invoices `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The product has no visitor accounts, no staff signup `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The editor's only write is publish or unpublish `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` No page loads a third-party script `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` The app makes no external network call at runtime `src: Constraints bullet 5`
- [ ] `C-CN-07` `constraint` The site has no inbound webhooks, no campaign sending `src: Constraints bullet 6`
- [ ] `C-CN-08` `constraint` The site has no job application form, no upload `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` A product configuration is never linkable `src: Constraints bullet 9`
- [ ] `C-CN-10` `constraint` The product has no separate dark mode `src: Constraints bullet 10`
- [ ] `C-CN-11` `constraint` The app stays responsive with 229 products per locale `src: Constraints bullet 12`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The API is served on the same origin under `/api` `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `literal` `GET /api/health` returns `200` once ready `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md` `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `literal` Empty `.browser_screenshots/` with `.downloads/` directories exist at the app root `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` A production build is served, never a dev server `src: Deployment contract bullet 7`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, not a child of the shell `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `literal` The server binds `0.0.0.0`, never `127.0.0.1` or `localhost` `src: Deployment contract bullet 9`
- [ ] `C-DC-11` `contract` The backing services are already running, never installed by the app `src: Deployment contract bullet 10`
- [ ] `C-DC-12` `contract` The app uses only the named providers with no edge functions `src: Deployment contract bullet 11`
- [ ] `C-DC-13` `contract` The app uses no persistent volumes, fixed container names, custom networks `src: Deployment contract bullet 12`
- [ ] `C-DC-14` `literal` Every write endpoint answers `202`, never `201` `src: Deployment contract API shapes`
- [ ] `C-DC-15` `literal` Every refusal body carries `error` with `code`, `message`, `requestId` `src: Deployment contract API shapes`
- [ ] `C-DC-16` `literal` Error codes include `validation_failed`, `invalid_request`, `rate_limited`, `not_found`, `forbidden` `src: Deployment contract API shapes`
- [ ] `C-DC-17` `contract` An invalid or unauthorized call is a client error, never a server error `src: Deployment contract API shapes`
- [ ] `C-DC-18` `literal` `GET /api/collections` returns `productCount` with `subCollections` `src: Deployment contract API shapes table`
- [ ] `C-DC-19` `literal` `GET /api/jobs` returns `title`, `location`, `employmentType`, `lang` `src: Deployment contract API shapes table`
- [ ] `C-DC-20` `literal` `GET /api/articles/{slug}` returns `credits` with `client`, `design` `src: Deployment contract API shapes table`
- [ ] `C-DC-21` `literal` `POST /api/consent` takes `visitorKey`, `categories`, `policyVersion` `src: Deployment contract API shapes table`
- [ ] `C-DC-22` `contract` List endpoints return a top-level JSON array `src: Deployment contract API shapes`
- [ ] `C-DC-23` `contract` Bearer authentication applies to every `/api/office` endpoint `src: Deployment contract API shapes`
- [ ] `C-DC-24` `contract` Leads are never held in memory instead of the `postgres` tables `src: Deployment contract no mocks`
- [ ] `C-DC-25` `contract` Confirmation mail is really sent to `mailpit`, never logged instead `src: Deployment contract no mocks`
- [ ] `C-DC-26` `contract` A reference is never invented in the browser `src: Deployment contract no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `pt` | value the instruction pins | C-OV-02 | Overview para 1 |
| `en` | value the instruction pins | C-OV-02 | Overview para 1 |
| `es` | value the instruction pins | C-OV-02 | Overview para 1 |
| `fr` | value the instruction pins | C-OV-02 | Overview para 1 |
| `commercial@example.com` | value the instruction pins | C-RL-16 | User roles seeded accounts |
| `commercial` | value the instruction pins | C-RL-16 | User roles seeded accounts |
| `editor@example.com` | value the instruction pins | C-RL-17 | User roles seeded accounts |
| `editor` | value the instruction pins | C-RL-17 | User roles seeded accounts |
| `former@example.com` | value the instruction pins | C-RL-18 | User roles seeded accounts |
| `suspended` | value the instruction pins | C-RL-18 | User roles seeded accounts |
| `deku-demo-pw-2026` | value the instruction pins | C-RL-19 | User roles seeded accounts |
| `POST /api/auth/login` | value the instruction pins | C-CF-01 | Core features rule 1 |
| `email` | value the instruction pins | C-CF-01 | Core features rule 1 |
| `password` | value the instruction pins | C-CF-01 | Core features rule 1 |
| `access_token` | value the instruction pins | C-CF-02 | Core features rule 1 |
| `role` | value the instruction pins | C-CF-02 | Core features rule 1 |
| `issued_at` | value the instruction pins | C-CF-02 | Core features rule 1 |
| `expires_at` | value the instruction pins | C-CF-02 | Core features rule 1 |
| `POST /api/auth/logout` | value the instruction pins | C-CF-07 | Core features rule 3 |
| `pt` | value the instruction pins | C-CF-16 | Core features rule 6 |
| `produtos` | value the instruction pins | C-CF-18 | Core features rule 7 |
| `products` | value the instruction pins | C-CF-18 | Core features rule 7 |
| `productos` | value the instruction pins | C-CF-18 | Core features rule 7 |
| `produits` | value the instruction pins | C-CF-18 | Core features rule 7 |
| `sobre` | value the instruction pins | C-CF-19 | Core features rule 7 |
| `about` | value the instruction pins | C-CF-19 | Core features rule 7 |
| `nosotros` | value the instruction pins | C-CF-19 | Core features rule 7 |
| `apropos` | value the instruction pins | C-CF-19 | Core features rule 7 |
| `sustentabilidade` | value the instruction pins | C-CF-20 | Core features rule 7 |
| `sustainability` | value the instruction pins | C-CF-20 | Core features rule 7 |
| `sostenibilidad` | value the instruction pins | C-CF-20 | Core features rule 7 |
| `durabilite` | value the instruction pins | C-CF-20 | Core features rule 7 |
| `jornal` | value the instruction pins | C-CF-21 | Core features rule 7 |
| `journal` | value the instruction pins | C-CF-21 | Core features rule 7 |
| `periodico` | value the instruction pins | C-CF-21 | Core features rule 7 |
| `lista` | value the instruction pins | C-CF-22 | Core features rule 7 |
| `wishlist` | value the instruction pins | C-CF-22 | Core features rule 7 |
| `mi-lista` | value the instruction pins | C-CF-22 | Core features rule 7 |
| `ma-liste` | value the instruction pins | C-CF-22 | Core features rule 7 |
| `careers` | value the instruction pins | C-CF-23 | Core features rule 7 |
| `legal` | value the instruction pins | C-CF-23 | Core features rule 7 |
| `newsletter` | value the instruction pins | C-CF-23 | Core features rule 7 |
| `/` | value the instruction pins | C-CF-27 | Core features rule 9 |
| `302` | value the instruction pins | C-CF-27 | Core features rule 9 |
| `/en/products/nature/tee-sign-heritage` | value the instruction pins | C-CF-37 | Core features rule 12 |
| `301` | value the instruction pins | C-CF-37 | Core features rule 12 |
| `/en/products/golf/tee-sign-heritage` | value the instruction pins | C-CF-37 | Core features rule 12 |
| `/es/productos/golf/tee-sign-heritage` | value the instruction pins | C-CF-39 | Core features rule 12 |
| `301` | value the instruction pins | C-CF-39 | Core features rule 12 |
| `/es/productos/golf/senal-de-salida-heritage` | value the instruction pins | C-CF-39 | Core features rule 12 |
| `x-default` | value the instruction pins | C-CF-47 | Core features rule 15 |
| `pt` | value the instruction pins | C-CF-47 | Core features rule 15 |
| `May 12, 2026` | value the instruction pins | C-CF-49 | Core features rule 16 |
| `20` | value the instruction pins | C-CF-51 | Core features rule 17 |
| `6` | value the instruction pins | C-CF-52 | Core features rule 17 |
| `4` | value the instruction pins | C-CF-52 | Core features rule 17 |
| `3` | value the instruction pins | C-CF-52 | Core features rule 17 |
| `20` | value the instruction pins | C-CF-53 | Core features rule 17 |
| `19` | value the instruction pins | C-CF-54 | Core features rule 17 |
| `Slim Room Sign` | value the instruction pins | C-CF-54 | Core features rule 17 |
| `18` | value the instruction pins | C-CF-55 | Core features rule 17 |
| `Slim Room Sign` | value the instruction pins | C-CF-55 | Core features rule 17 |
| `Golf Bag Stand` | value the instruction pins | C-CF-55 | Core features rule 17 |
| `by Collections` | value the instruction pins | C-CF-56 | Core features rule 18 |
| `by Products` | value the instruction pins | C-CF-57 | Core features rule 18 |
| `Frame` | value the instruction pins | C-CF-59 | Core features rule 18 |
| `Plaza` | value the instruction pins | C-CF-59 | Core features rule 18 |
| `Reuse` | value the instruction pins | C-CF-59 | Core features rule 18 |
| `2` | value the instruction pins | C-CF-62 | Core features rule 19 |
| `2` | value the instruction pins | C-CF-63 | Core features rule 19 |
| `10` | value the instruction pins | C-CF-64 | Core features rule 19 |
| `2` | value the instruction pins | C-CF-65 | Core features rule 19 |
| `3` | value the instruction pins | C-CF-65 | Core features rule 19 |
| `0` | value the instruction pins | C-CF-66 | Core features rule 19 |
| `collection` | value the instruction pins | C-CF-67 | Core features rule 20 |
| `productType` | value the instruction pins | C-CF-67 | Core features rule 20 |
| `subCollection` | value the instruction pins | C-CF-67 | Core features rule 20 |
| `Showing <n> of <total> Results` | value the instruction pins | C-CF-72 | Core features rule 21 |
| `/en/products` | value the instruction pins | C-CF-74 | Core features rule 21 |
| `Showing 20 of 20 Results` | value the instruction pins | C-CF-74 | Core features rule 21 |
| `/en/products?collection=urban&productType=signage` | value the instruction pins | C-CF-75 | Core features rule 21 |
| `Showing 2 of 20 Results` | value the instruction pins | C-CF-75 | Core features rule 21 |
| `+N` | value the instruction pins | C-CF-84 | Core features rule 25 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-84 | Core features rule 25 |
| `+6` | value the instruction pins | C-CF-84 | Core features rule 25 |
| `Frame Bollard` | value the instruction pins | C-CF-86 | Core features rule 26 |
| `s` | value the instruction pins | C-CF-86 | Core features rule 26 |
| `m` | value the instruction pins | C-CF-86 | Core features rule 26 |
| `Reuse Litter Bin Duo` | value the instruction pins | C-CF-87 | Core features rule 26 |
| `All` | value the instruction pins | C-CF-87 | Core features rule 26 |
| `Bottle` | value the instruction pins | C-CF-87 | Core features rule 26 |
| `Pet` | value the instruction pins | C-CF-87 | Core features rule 26 |
| `Classic Ball Washer` | value the instruction pins | C-CF-88 | Core features rule 26 |
| `R900` | value the instruction pins | C-CF-88 | Core features rule 26 |
| `Q600` | value the instruction pins | C-CF-88 | Core features rule 26 |
| `Line Door Plate` | value the instruction pins | C-CF-90 | Core features rule 27 |
| `GET /api/products?locale=en` | value the instruction pins | C-CF-92 | Core features rule 29 |
| `/en/products/urban` | value the instruction pins | C-CF-95 | Core features rule 31 |
| `Showing 6 of 20 Results` | value the instruction pins | C-CF-95 | Core features rule 31 |
| `Urban Catalogue` | value the instruction pins | C-CF-99 | Core features rule 34 |
| `Nature Catalogue` | value the instruction pins | C-CF-99 | Core features rule 34 |
| `Repolymer Catalogue` | value the instruction pins | C-CF-99 | Core features rule 34 |
| `Golf Catalogue` | value the instruction pins | C-CF-99 | Core features rule 34 |
| `Dimensions` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `Structure Options` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `Structure Colors` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `Display Options` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `HPL+ Colors` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `Materials` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `Specifications` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `Advantages` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `References` | value the instruction pins | C-CF-111 | Core features rule 40 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-113 | Core features rule 41 |
| `190 x 100 x 1700 mm` | value the instruction pins | C-CF-113 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-114 | Core features rule 41 |
| `Galvanised steel` | value the instruction pins | C-CF-114 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-115 | Core features rule 41 |
| `Pure white RAL9010` | value the instruction pins | C-CF-115 | Core features rule 41 |
| `Salmon pink RAL3022` | value the instruction pins | C-CF-115 | Core features rule 41 |
| `Personalised` | value the instruction pins | C-CF-115 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-116 | Core features rule 41 |
| `HPL +` | value the instruction pins | C-CF-116 | Core features rule 41 |
| `HPL Print` | value the instruction pins | C-CF-116 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-117 | Core features rule 41 |
| `Sienna brown` | value the instruction pins | C-CF-117 | Core features rule 41 |
| `Turf green` | value the instruction pins | C-CF-117 | Core features rule 41 |
| `Black` | value the instruction pins | C-CF-117 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-118 | Core features rule 41 |
| `Reinforced, brown recycled plastic; HPL+ or HPL Print.` | value the instruction pins | C-CF-118 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-119 | Core features rule 41 |
| `No maintenance required; Easy component replacement` | value the instruction pins | C-CF-119 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-120 | Core features rule 41 |
| `HPL+ - GTEETTM010` | value the instruction pins | C-CF-120 | Core features rule 41 |
| `HPL Print - GTEETTM011` | value the instruction pins | C-CF-120 | Core features rule 41 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-121 | Core features rule 41 |
| `Where tradition meets function` | value the instruction pins | C-CF-121 | Core features rule 41 |
| `Plaza Bench Long` | value the instruction pins | C-CF-126 | Core features rule 44 |
| `1400` | value the instruction pins | C-CF-126 | Core features rule 44 |
| `1900` | value the instruction pins | C-CF-126 | Core features rule 44 |
| `2000` | value the instruction pins | C-CF-126 | Core features rule 44 |
| `2000` | value the instruction pins | C-CF-127 | Core features rule 44 |
| `Plaza Bench Long` | value the instruction pins | C-CF-127 | Core features rule 44 |
| `2000 x 554 x 465 mm` | value the instruction pins | C-CF-127 | Core features rule 44 |
| `Plaza Bench Long` | value the instruction pins | C-CF-128 | Core features rule 44 |
| `Plaza Bench Long - UBSCFE0000881` | value the instruction pins | C-CF-128 | Core features rule 44 |
| `In the same Collection` | value the instruction pins | C-CF-132 | Core features rule 46 |
| `Boardwalk Module` | value the instruction pins | C-CF-134 | Core features rule 47 |
| `Viewpoint Platform Deck` | value the instruction pins | C-CF-134 | Core features rule 47 |
| `Ridge Viewpoint Boardwalk` | value the instruction pins | C-CF-134 | Core features rule 47 |
| `GET /api/products/tee-sign-heritage?locale=en` | value the instruction pins | C-CF-136 | Core features rule 48 |
| `alternates` | value the instruction pins | C-CF-137 | Core features rule 48 |
| `BreadcrumbList` | value the instruction pins | C-CF-138 | Core features rule 48 |
| `Personalise your product` | value the instruction pins | C-CF-139 | Core features rule 49 |
| `Reuse Litter Bin Duo` | value the instruction pins | C-CF-145 | Core features rule 51 |
| `Anthracite grey RAL7016` | value the instruction pins | C-CF-145 | Core features rule 51 |
| `References` | value the instruction pins | C-CF-153 | Core features rule 55 |
| `Your wishlist` | value the instruction pins | C-CF-167 | Core features rule 62 |
| `No picks yet?` | value the instruction pins | C-CF-167 | Core features rule 62 |
| `Start adding` | value the instruction pins | C-CF-168 | Core features rule 62 |
| `Request a quotation` | value the instruction pins | C-CF-171 | Core features rule 63 |
| `51` | value the instruction pins | C-CF-179 | Core features rule 66 |
| `Contact` | value the instruction pins | C-CF-181 | Core features rule 67 |
| `Wishlist` | value the instruction pins | C-CF-181 | Core features rule 67 |
| `Files` | value the instruction pins | C-CF-181 | Core features rule 67 |
| `First Name` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `Last Name` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `Email` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `Role` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `Industry` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `Country` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `City` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `NIF` | value the instruction pins | C-CF-183 | Core features rule 67 |
| `Some products have BIM/3D files available, are you interested?` | value the instruction pins | C-CF-184 | Core features rule 67 |
| `POST /api/lead/quotation` | value the instruction pins | C-CF-185 | Core features rule 68 |
| `202` | value the instruction pins | C-CF-185 | Core features rule 68 |
| `reference` | value the instruction pins | C-CF-185 | Core features rule 68 |
| `VQ-` | value the instruction pins | C-CF-188 | Core features rule 69 |
| `23456789ABCDEFGHJKMNPQRSTUVWXYZ` | value the instruction pins | C-CF-188 | Core features rule 69 |
| `pt` | value the instruction pins | C-CF-193 | Core features rule 71 |
| `resolved_from_locale` | value the instruction pins | C-CF-193 | Core features rule 71 |
| `No longer in the catalogue` | value the instruction pins | C-CF-194 | Core features rule 71 |
| `unresolved` | value the instruction pins | C-CF-194 | Core features rule 71 |
| `option_size` | value the instruction pins | C-CF-196 | Core features rule 72 |
| `option_structure` | value the instruction pins | C-CF-196 | Core features rule 72 |
| `option_color` | value the instruction pins | C-CF-196 | Core features rule 72 |
| `option_display` | value the instruction pins | C-CF-196 | Core features rule 72 |
| `option_hpl_color` | value the instruction pins | C-CF-196 | Core features rule 72 |
| `payload_rendered` | value the instruction pins | C-CF-198 | Core features rule 73 |
| `Collection:` | value the instruction pins | C-CF-199 | Core features rule 73 |
| `Structure:` | value the instruction pins | C-CF-199 | Core features rule 73 |
| `Color:` | value the instruction pins | C-CF-199 | Core features rule 73 |
| `Display:` | value the instruction pins | C-CF-199 | Core features rule 73 |
| `HPL Color:` | value the instruction pins | C-CF-199 | Core features rule 73 |
| `Size:` | value the instruction pins | C-CF-199 | Core features rule 73 |
| `(not chosen)` | value the instruction pins | C-CF-200 | Core features rule 73 |
| `Landscape architect` | value the instruction pins | C-CF-211 | Core features rule 76 |
| `Municipal buyer` | value the instruction pins | C-CF-211 | Core features rule 76 |
| `Park or trail operator` | value the instruction pins | C-CF-211 | Core features rule 76 |
| `Golf course superintendent` | value the instruction pins | C-CF-211 | Core features rule 76 |
| `Contractor` | value the instruction pins | C-CF-211 | Core features rule 76 |
| `Other` | value the instruction pins | C-CF-211 | Core features rule 76 |
| `Public administration` | value the instruction pins | C-CF-212 | Core features rule 76 |
| `Other` | value the instruction pins | C-CF-212 | Core features rule 76 |
| `wantsTechnicalFiles` | value the instruction pins | C-CF-214 | Core features rule 78 |
| `POST /api/lead/file-request` | value the instruction pins | C-CF-225 | Core features rule 84 |
| `202` | value the instruction pins | C-CF-225 | Core features rule 84 |
| `documentName` | value the instruction pins | C-CF-225 | Core features rule 84 |
| `downloadUrl` | value the instruction pins | C-CF-225 | Core features rule 84 |
| `expiresAt` | value the instruction pins | C-CF-225 | Core features rule 84 |
| `Tee Sign Heritage technical files` | value the instruction pins | C-CF-227 | Core features rule 84 |
| `5` | value the instruction pins | C-CF-231 | Core features rule 85 |
| `GET /api/files/<token>` | value the instruction pins | C-CF-232 | Core features rule 86 |
| `302` | value the instruction pins | C-CF-232 | Core features rule 86 |
| `tee-sign-heritage-technical-files-en.pdf` | value the instruction pins | C-CF-233 | Core features rule 86 |
| `urban-catalogue-en.pdf` | value the instruction pins | C-CF-234 | Core features rule 86 |
| `404` | value the instruction pins | C-CF-236 | Core features rule 87 |
| `403` | value the instruction pins | C-CF-236 | Core features rule 87 |
| `By submitting your email you agree to our Privacy Policy.` | value the instruction pins | C-CF-244 | Core features rule 93 |
| `POST /api/subscriber` | value the instruction pins | C-CF-247 | Core features rule 94 |
| `202` | value the instruction pins | C-CF-247 | Core features rule 94 |
| `check_inbox` | value the instruction pins | C-CF-247 | Core features rule 94 |
| `subscriber` | value the instruction pins | C-CF-249 | Core features rule 95 |
| `pending` | value the instruction pins | C-CF-249 | Core features rule 95 |
| `/api/subscriber/confirm?token=` | value the instruction pins | C-CF-255 | Core features rule 97 |
| `303` | value the instruction pins | C-CF-255 | Core features rule 97 |
| `/<locale>/newsletter/confirmed` | value the instruction pins | C-CF-255 | Core features rule 97 |
| `303` | value the instruction pins | C-CF-257 | Core features rule 97 |
| `/<locale>/newsletter/expired` | value the instruction pins | C-CF-257 | Core features rule 97 |
| `List-Unsubscribe` | value the instruction pins | C-CF-259 | Core features rule 98 |
| `List-Unsubscribe-Post` | value the instruction pins | C-CF-259 | Core features rule 98 |
| `GET /api/subscriber/unsubscribe?token=` | value the instruction pins | C-CF-261 | Core features rule 99 |
| `303` | value the instruction pins | C-CF-261 | Core features rule 99 |
| `/<locale>/newsletter/unsubscribed` | value the instruction pins | C-CF-261 | Core features rule 99 |
| `POST /api/subscriber/unsubscribe` | value the instruction pins | C-CF-262 | Core features rule 99 |
| `204` | value the instruction pins | C-CF-262 | Core features rule 99 |
| `First Name` | value the instruction pins | C-CF-265 | Core features rule 102 |
| `Last Name` | value the instruction pins | C-CF-265 | Core features rule 102 |
| `Email` | value the instruction pins | C-CF-265 | Core features rule 102 |
| `Country` | value the instruction pins | C-CF-265 | Core features rule 102 |
| `Message` | value the instruction pins | C-CF-265 | Core features rule 102 |
| `POST /api/lead/contact` | value the instruction pins | C-CF-267 | Core features rule 103 |
| `202` | value the instruction pins | C-CF-267 | Core features rule 103 |
| `requestId` | value the instruction pins | C-CF-267 | Core features rule 103 |
| `I have read` | value the instruction pins | C-CF-269 | Core features rule 104 |
| `consent_text_hash` | value the instruction pins | C-CF-272 | Core features rule 105 |
| `422` | value the instruction pins | C-CF-277 | Core features rule 107 |
| `error.fields` | value the instruction pins | C-CF-277 | Core features rule 107 |
| `400` | value the instruction pins | C-CF-278 | Core features rule 107 |
| `website` | value the instruction pins | C-CF-282 | Core features rule 108 |
| `meta.website` | value the instruction pins | C-CF-282 | Core features rule 108 |
| `GET /api/form-token` | value the instruction pins | C-CF-284 | Core features rule 109 |
| `meta.formToken` | value the instruction pins | C-CF-284 | Core features rule 109 |
| `Idempotent-Replayed: true` | value the instruction pins | C-CF-288 | Core features rule 110 |
| `409` | value the instruction pins | C-CF-289 | Core features rule 110 |
| `idempotency_conflict` | value the instruction pins | C-CF-289 | Core features rule 110 |
| `5` | value the instruction pins | C-CF-291 | Core features rule 111 |
| `3` | value the instruction pins | C-CF-292 | Core features rule 111 |
| `429` | value the instruction pins | C-CF-293 | Core features rule 111 |
| `Retry-After` | value the instruction pins | C-CF-293 | Core features rule 111 |
| `error.retryAfterSeconds` | value the instruction pins | C-CF-293 | Core features rule 111 |
| `quarantined` | value the instruction pins | C-CF-296 | Core features rule 112 |
| `received` | value the instruction pins | C-CF-299 | Core features rule 112 |
| `503` | value the instruction pins | C-CF-302 | Core features rule 114 |
| `mailpit` | value the instruction pins | C-CF-303 | Core features rule 115 |
| `SMTP_HOST` | value the instruction pins | C-CF-303 | Core features rule 115 |
| `SMTP_PORT` | value the instruction pins | C-CF-303 | Core features rule 115 |
| `Verdea <hello@verdea-outdoor.com>` | value the instruction pins | C-CF-304 | Core features rule 115 |
| `received` | value the instruction pins | C-CF-307 | Core features rule 116 |
| `queued` | value the instruction pins | C-CF-307 | Core features rule 116 |
| `delivered` | value the instruction pins | C-CF-307 | Core features rule 116 |
| `commercial@example.com` | value the instruction pins | C-CF-308 | Core features rule 116 |
| `delivered_at` | value the instruction pins | C-CF-308 | Core features rule 116 |
| `failed` | value the instruction pins | C-CF-309 | Core features rule 116 |
| `New enquiry received` | value the instruction pins | C-CF-311 | Core features rule 117 |
| `New quotation: ` | value the instruction pins | C-CF-312 | Core features rule 117 |
| `New file request: ` | value the instruction pins | C-CF-313 | Core features rule 117 |
| `Verdea enquiry received` | value the instruction pins | C-CF-317 | Core features rule 118 |
| `Quotation request received: ` | value the instruction pins | C-CF-319 | Core features rule 118 |
| `Your Verdea download: ` | value the instruction pins | C-CF-321 | Core features rule 119 |
| `Confirm your Verdea newsletter subscription` | value the instruction pins | C-CF-323 | Core features rule 120 |
| `GET /api/search` | value the instruction pins | C-CF-329 | Core features rule 123 |
| `products` | value the instruction pins | C-CF-329 | Core features rule 123 |
| `pages` | value the instruction pins | C-CF-329 | Core features rule 123 |
| `tee sig` | value the instruction pins | C-CF-334 | Core features rule 124 |
| `Tee Sign Heritage` | value the instruction pins | C-CF-334 | Core features rule 124 |
| `praca` | value the instruction pins | C-CF-335 | Core features rule 125 |
| `pt` | value the instruction pins | C-CF-335 | Core features rule 125 |
| `Banco Praça Longo` | value the instruction pins | C-CF-335 | Core features rule 125 |
| `salida` | value the instruction pins | C-CF-336 | Core features rule 125 |
| `es` | value the instruction pins | C-CF-336 | Core features rule 125 |
| `Señal de Salida Heritage` | value the instruction pins | C-CF-336 | Core features rule 125 |
| `depart` | value the instruction pins | C-CF-337 | Core features rule 125 |
| `fr` | value the instruction pins | C-CF-337 | Core features rule 125 |
| `Panneau de Départ Heritage` | value the instruction pins | C-CF-337 | Core features rule 125 |
| `(bench` | value the instruction pins | C-CF-338 | Core features rule 126 |
| `All` | value the instruction pins | C-CF-347 | Core features rule 131 |
| `Press releases` | value the instruction pins | C-CF-347 | Core features rule 131 |
| `Sustainability` | value the instruction pins | C-CF-347 | Core features rule 131 |
| `Case Studies` | value the instruction pins | C-CF-347 | Core features rule 131 |
| `Products` | value the instruction pins | C-CF-347 | Core features rule 131 |
| `Educational` | value the instruction pins | C-CF-347 | Core features rule 131 |
| `Institutional` | value the instruction pins | C-CF-347 | Core features rule 131 |
| `13` | value the instruction pins | C-CF-350 | Core features rule 132 |
| `2` | value the instruction pins | C-CF-350 | Core features rule 132 |
| `1` | value the instruction pins | C-CF-350 | Core features rule 132 |
| `0` | value the instruction pins | C-CF-350 | Core features rule 132 |
| `19` | value the instruction pins | C-CF-351 | Core features rule 132 |
| `pt` | value the instruction pins | C-CF-351 | Core features rule 132 |
| `en` | value the instruction pins | C-CF-351 | Core features rule 132 |
| `es` | value the instruction pins | C-CF-351 | Core features rule 132 |
| `18` | value the instruction pins | C-CF-351 | Core features rule 132 |
| `fr` | value the instruction pins | C-CF-351 | Core features rule 132 |
| `/pt/jornal/casos-de-estudo` | value the instruction pins | C-CF-352 | Core features rule 132 |
| `?page=2` | value the instruction pins | C-CF-354 | Core features rule 133 |
| `GET /api/articles` | value the instruction pins | C-CF-356 | Core features rule 134 |
| `X-Total-Count` | value the instruction pins | C-CF-356 | Core features rule 134 |
| `GET /api/categories?locale=en` | value the instruction pins | C-CF-357 | Core features rule 134 |
| `Ridge Viewpoint Boardwalk` | value the instruction pins | C-CF-360 | Core features rule 136 |
| `2026-05-12` | value the instruction pins | C-CF-360 | Core features rule 136 |
| `recycled-plastic-explained` | value the instruction pins | C-CF-361 | Core features rule 136 |
| `hpl-in-the-open-air` | value the instruction pins | C-CF-361 | Core features rule 136 |
| `verdea-opens-spanish-establishment` | value the instruction pins | C-CF-361 | Core features rule 136 |
| `why-galvanised-steel-lasts` | value the instruction pins | C-CF-362 | Core features rule 136 |
| `<n>min Read` | value the instruction pins | C-CF-363 | Core features rule 137 |
| `Ridge Viewpoint Boardwalk` | value the instruction pins | C-CF-365 | Core features rule 137 |
| `Client: Municipality of Alvora` | value the instruction pins | C-CF-365 | Core features rule 137 |
| `Design: Atra` | value the instruction pins | C-CF-365 | Core features rule 137 |
| `+2` | value the instruction pins | C-CF-366 | Core features rule 137 |
| `View gallery` | value the instruction pins | C-CF-366 | Core features rule 137 |
| `readingMinutes` | value the instruction pins | C-CF-367 | Core features rule 138 |
| `galleryCount` | value the instruction pins | C-CF-367 | Core features rule 138 |
| `credits` | value the instruction pins | C-CF-367 | Core features rule 138 |
| `relatedArticles` | value the instruction pins | C-CF-367 | Core features rule 138 |
| `relatedProducts` | value the instruction pins | C-CF-367 | Core features rule 138 |
| `CNC Operator` | value the instruction pins | C-CF-371 | Core features rule 142 |
| `Serralheiro Civil` | value the instruction pins | C-CF-371 | Core features rule 142 |
| `Project Manager` | value the instruction pins | C-CF-371 | Core features rule 142 |
| `Installation Technician` | value the instruction pins | C-CF-371 | Core features rule 142 |
| `Serralheiro Civil` | value the instruction pins | C-CF-372 | Core features rule 142 |
| `pt` | value the instruction pins | C-CF-372 | Core features rule 142 |
| `/en/products/golf/tee-sign-heritage.md` | value the instruction pins | C-CF-377 | Core features rule 145 |
| `/llms.txt` | value the instruction pins | C-CF-378 | Core features rule 145 |
| `Accept all` | value the instruction pins | C-CF-379 | Core features rule 146 |
| `Reject all` | value the instruction pins | C-CF-379 | Core features rule 146 |
| `Choose` | value the instruction pins | C-CF-379 | Core features rule 146 |
| `verdea_consent` | value the instruction pins | C-CF-381 | Core features rule 147 |
| `POST /api/consent` | value the instruction pins | C-CF-382 | Core features rule 147 |
| `consent_receipt` | value the instruction pins | C-CF-382 | Core features rule 147 |
| `/en/legal/privacy-policy` | value the instruction pins | C-CF-387 | Core features rule 151 |
| `/en/legal/cookie-policy` | value the instruction pins | C-CF-387 | Core features rule 151 |
| `/en/legal/terms-of-use` | value the instruction pins | C-CF-387 | Core features rule 151 |
| `/en/legal/privacy-policy/v/1` | value the instruction pins | C-CF-388 | Core features rule 152 |
| `version has been superseded.` | value the instruction pins | C-CF-388 | Core features rule 152 |
| `404` | value the instruction pins | C-CF-393 | Core features rule 154 |
| `/en/products` | value the instruction pins | C-CF-394 | Core features rule 154 |
| `/en/journal` | value the instruction pins | C-CF-394 | Core features rule 154 |
| `/en` | value the instruction pins | C-CF-394 | Core features rule 154 |
| `/office/leads` | value the instruction pins | C-CF-401 | Core features rule 159 |
| `/office/leads/<id>` | value the instruction pins | C-CF-401 | Core features rule 159 |
| `/office/subscribers` | value the instruction pins | C-CF-401 | Core features rule 159 |
| `/office/products` | value the instruction pins | C-CF-401 | Core features rule 159 |
| `GET /api/office/me` | value the instruction pins | C-CF-402 | Core features rule 160 |
| `email` | value the instruction pins | C-CF-402 | Core features rule 160 |
| `role` | value the instruction pins | C-CF-402 | Core features rule 160 |
| `displayName` | value the instruction pins | C-CF-402 | Core features rule 160 |
| `GET /api/office/leads/summary` | value the instruction pins | C-CF-403 | Core features rule 161 |
| `GET /api/office/leads` | value the instruction pins | C-CF-404 | Core features rule 162 |
| `commercial` | value the instruction pins | C-CF-404 | Core features rule 162 |
| `editor` | value the instruction pins | C-CF-404 | Core features rule 162 |
| `GET /api/office/leads/<id>` | value the instruction pins | C-CF-405 | Core features rule 163 |
| `commercial` | value the instruction pins | C-CF-405 | Core features rule 163 |
| `lead.read` | value the instruction pins | C-CF-406 | Core features rule 163 |
| `lead.release` | value the instruction pins | C-CF-408 | Core features rule 164 |
| `subscriber.list` | value the instruction pins | C-CF-410 | Core features rule 165 |
| `commercial` | value the instruction pins | C-CF-410 | Core features rule 165 |
| `GET /api/office/subscribers/summary` | value the instruction pins | C-CF-411 | Core features rule 165 |
| `GET /api/office/products?locale=` | value the instruction pins | C-CF-412 | Core features rule 166 |
| `product.unpublish` | value the instruction pins | C-CF-413 | Core features rule 167 |
| `product.publish` | value the instruction pins | C-CF-413 | Core features rule 167 |
| `/en/products/golf/tee-sign-heritage` | value the instruction pins | C-UF-01 | User flow route table |
| `/sitemap.xml` | value the instruction pins | C-UF-02 | User flow route table |
| `/sitemap-pt.xml` | value the instruction pins | C-UF-02 | User flow route table |
| `/sitemap-en.xml` | value the instruction pins | C-UF-02 | User flow route table |
| `/sitemap-es.xml` | value the instruction pins | C-UF-02 | User flow route table |
| `/sitemap-fr.xml` | value the instruction pins | C-UF-02 | User flow route table |
| `/pt/produtos/detalhes/placa-de-sala-slim` | value the instruction pins | C-UF-03 | User flow route table |
| `/en/newsletter/confirmed` | value the instruction pins | C-UF-04 | User flow route table |
| `/en/newsletter/expired` | value the instruction pins | C-UF-04 | User flow route table |
| `/en/newsletter/unsubscribed` | value the instruction pins | C-UF-04 | User flow route table |
| `/es/productos/golf/senal-de-salida-heritage` | value the instruction pins | C-UF-13 | User flow journey 5 |
| `dark` | value the instruction pins | C-UX-11 | UI/UX notes themes |
| `light` | value the instruction pins | C-UX-11 | UI/UX notes themes |
| `fluor` | value the instruction pins | C-UX-11 | UI/UX notes themes |
| `4.5:1` | value the instruction pins | C-UX-28 | UI/UX notes accessibility |
| `3:1` | value the instruction pins | C-UX-28 | UI/UX notes accessibility |
| `44` | value the instruction pins | C-UX-29 | UI/UX notes accessibility |
| `GET /api/health` | value the instruction pins | C-TR-08 | Technical requirements health |
| `200` | value the instruction pins | C-TR-08 | Technical requirements health |
| `{"status": "ok"}` | value the instruction pins | C-TR-08 | Technical requirements health |
| `Strict-Transport-Security` | value the instruction pins | C-TR-14 | Technical requirements security |
| `includeSubDomains` | value the instruction pins | C-TR-14 | Technical requirements security |
| `X-Content-Type-Options: nosniff` | value the instruction pins | C-TR-15 | Technical requirements security |
| `Referrer-Policy: strict-origin-when-cross-origin` | value the instruction pins | C-TR-16 | Technical requirements security |
| `Permissions-Policy` | value the instruction pins | C-TR-17 | Technical requirements security |
| `Cross-Origin-Opener-Policy: same-origin` | value the instruction pins | C-TR-18 | Technical requirements security |
| `Content-Security-Policy` | value the instruction pins | C-TR-19 | Technical requirements security |
| `frame-ancestors 'none'` | value the instruction pins | C-TR-19 | Technical requirements security |
| `script-src` | value the instruction pins | C-TR-20 | Technical requirements security |
| `'unsafe-inline'` | value the instruction pins | C-TR-20 | Technical requirements security |
| `'unsafe-eval'` | value the instruction pins | C-TR-20 | Technical requirements security |
| `X-Request-Id` | value the instruction pins | C-TR-26 | Technical requirements observability |
| `/robots.txt` | value the instruction pins | C-TR-27 | Technical requirements generated documents |
| `/api/` | value the instruction pins | C-TR-27 | Technical requirements generated documents |
| `/office` | value the instruction pins | C-TR-27 | Technical requirements generated documents |
| `deku-demo-pw-2026` | value the instruction pins | C-DM-02 | Data model password paragraph |
| `urban` | value the instruction pins | C-DM-16 | Data model seed data |
| `nature` | value the instruction pins | C-DM-16 | Data model seed data |
| `repolymer` | value the instruction pins | C-DM-16 | Data model seed data |
| `golf` | value the instruction pins | C-DM-16 | Data model seed data |
| `details` | value the instruction pins | C-DM-16 | Data model seed data |
| `signage` | value the instruction pins | C-DM-17 | Data model seed data |
| `construction` | value the instruction pins | C-DM-17 | Data model seed data |
| `furniture` | value the instruction pins | C-DM-17 | Data model seed data |
| `equipment` | value the instruction pins | C-DM-17 | Data model seed data |
| `vd-tee-sign-heritage` | value the instruction pins | C-DM-18 | Data model seed data |
| `vd-plaza-bench-long` | value the instruction pins | C-DM-18 | Data model seed data |
| `vd-slim-room-sign` | value the instruction pins | C-DM-18 | Data model seed data |
| `vd-plaza-bench-long` | value the instruction pins | C-DM-19 | Data model seed data |
| `Banco Praça Longo` | value the instruction pins | C-DM-19 | Data model seed data |
| `banco-praca-longo` | value the instruction pins | C-DM-19 | Data model seed data |
| `vd-tee-sign-heritage` | value the instruction pins | C-DM-20 | Data model seed data |
| `senal-de-salida-heritage` | value the instruction pins | C-DM-20 | Data model seed data |
| `panneau-de-depart-heritage` | value the instruction pins | C-DM-20 | Data model seed data |
| `vd-slim-room-sign` | value the instruction pins | C-DM-21 | Data model seed data |
| `Placa de Sala Slim` | value the instruction pins | C-DM-21 | Data model seed data |
| `placa-de-sala-slim` | value the instruction pins | C-DM-21 | Data model seed data |
| `Bike Parking Totem` | value the instruction pins | C-DM-22 | Data model seed data |
| `2 Schuko Plugs` | value the instruction pins | C-DM-22 | Data model seed data |
| `Shimano Standard Charger` | value the instruction pins | C-DM-22 | Data model seed data |
| `Bosch Standard Charger` | value the instruction pins | C-DM-22 | Data model seed data |
| `privacy-policy` | value the instruction pins | C-DM-23 | Data model seed data |
| `cookie-policy` | value the instruction pins | C-DM-23 | Data model seed data |
| `terms-of-use` | value the instruction pins | C-DM-23 | Data model seed data |
| `data-theme` | value the instruction pins | C-FE-01 | Front-end specification global chrome header |
| `fluor` | value the instruction pins | C-FE-01 | Front-end specification global chrome header |
| `Products` | value the instruction pins | C-FE-03 | Front-end specification global chrome navigation |
| `About` | value the instruction pins | C-FE-03 | Front-end specification global chrome navigation |
| `Sustainability` | value the instruction pins | C-FE-03 | Front-end specification global chrome navigation |
| `Journal` | value the instruction pins | C-FE-03 | Front-end specification global chrome navigation |
| `Headquarters` | value the instruction pins | C-FE-11 | Front-end specification global chrome footer |
| `Production` | value the instruction pins | C-FE-11 | Front-end specification global chrome footer |
| `Verdea Spain` | value the instruction pins | C-FE-11 | Front-end specification global chrome footer |
| `Call to a national landline` | value the instruction pins | C-FE-12 | Front-end specification global chrome footer |
| `+351 234 600 118` | value the instruction pins | C-FE-12 | Front-end specification global chrome footer |
| `Careers` | value the instruction pins | C-FE-13 | Front-end specification global chrome footer |
| `Complaints Book` | value the instruction pins | C-FE-13 | Front-end specification global chrome footer |
| `Privacy Policy` | value the instruction pins | C-FE-13 | Front-end specification global chrome footer |
| `Made by Atra` | value the instruction pins | C-FE-13 | Front-end specification global chrome footer |
| `Spaces for people, made for life.` | value the instruction pins | C-FE-31 | Front-end specification home |
| `for welcoming urban spaces` | value the instruction pins | C-FE-33 | Front-end specification home |
| `See Urban Products` | value the instruction pins | C-FE-34 | Front-end specification home |
| `Made to last, designed to endure.` | value the instruction pins | C-FE-36 | Front-end specification home |
| `Our products are made to last. Take your time exploring.` | value the instruction pins | C-FE-37 | Front-end specification catalogue index |
| `PDF` | value the instruction pins | C-FE-38 | Front-end specification catalogue index |
| `Download Urban Catalogue` | value the instruction pins | C-FE-38 | Front-end specification catalogue index |
| `A trail of hard work` | value the instruction pins | C-FE-50 | Front-end specification about route |
| `01. Environmental Awareness` | value the instruction pins | C-FE-53 | Front-end specification about route |
| `02. Innovation` | value the instruction pins | C-FE-53 | Front-end specification about route |
| `03. Quality` | value the instruction pins | C-FE-53 | Front-end specification about route |
| `04. Durability` | value the instruction pins | C-FE-53 | Front-end specification about route |
| `68 members` | value the instruction pins | C-FE-54 | Front-end specification about route |
| `Built in Portugal. Made for life.` | value the instruction pins | C-FE-55 | Front-end specification sustainability route |
| `Recycled plastic` | value the instruction pins | C-FE-56 | Front-end specification sustainability route |
| `High-pressure laminate` | value the instruction pins | C-FE-56 | Front-end specification sustainability route |
| `Steel` | value the instruction pins | C-FE-56 | Front-end specification sustainability route |
| `LEARN MORE` | value the instruction pins | C-FE-56 | Front-end specification sustainability route |
| `Ecodesign that empowers` | value the instruction pins | C-FE-58 | Front-end specification sustainability route |
| `Alvora, Portugal` | value the instruction pins | C-FE-58 | Front-end specification sustainability route |
| `Exploring ideas, insights` | value the instruction pins | C-FE-59 | Front-end specification journal routes |
| `${APP_PUBLIC_PORT}:4173` | value the instruction pins | C-DC-02 | Deployment contract bullet 1 |
| `GET /api/health` | value the instruction pins | C-DC-04 | Deployment contract bullet 3 |
| `200` | value the instruction pins | C-DC-04 | Deployment contract bullet 3 |
| `.browser_screenshots/` | value the instruction pins | C-DC-07 | Deployment contract bullet 6 |
| `.downloads/` | value the instruction pins | C-DC-07 | Deployment contract bullet 6 |
| `0.0.0.0` | value the instruction pins | C-DC-10 | Deployment contract bullet 9 |
| `127.0.0.1` | value the instruction pins | C-DC-10 | Deployment contract bullet 9 |
| `localhost` | value the instruction pins | C-DC-10 | Deployment contract bullet 9 |
| `202` | value the instruction pins | C-DC-14 | Deployment contract API shapes |
| `201` | value the instruction pins | C-DC-14 | Deployment contract API shapes |
| `error` | value the instruction pins | C-DC-15 | Deployment contract API shapes |
| `code` | value the instruction pins | C-DC-15 | Deployment contract API shapes |
| `message` | value the instruction pins | C-DC-15 | Deployment contract API shapes |
| `requestId` | value the instruction pins | C-DC-15 | Deployment contract API shapes |
| `validation_failed` | value the instruction pins | C-DC-16 | Deployment contract API shapes |
| `invalid_request` | value the instruction pins | C-DC-16 | Deployment contract API shapes |
| `rate_limited` | value the instruction pins | C-DC-16 | Deployment contract API shapes |
| `not_found` | value the instruction pins | C-DC-16 | Deployment contract API shapes |
| `forbidden` | value the instruction pins | C-DC-16 | Deployment contract API shapes |
| `GET /api/collections` | value the instruction pins | C-DC-18 | Deployment contract API shapes table |
| `productCount` | value the instruction pins | C-DC-18 | Deployment contract API shapes table |
| `subCollections` | value the instruction pins | C-DC-18 | Deployment contract API shapes table |
| `GET /api/jobs` | value the instruction pins | C-DC-19 | Deployment contract API shapes table |
| `title` | value the instruction pins | C-DC-19 | Deployment contract API shapes table |
| `location` | value the instruction pins | C-DC-19 | Deployment contract API shapes table |
| `employmentType` | value the instruction pins | C-DC-19 | Deployment contract API shapes table |
| `lang` | value the instruction pins | C-DC-19 | Deployment contract API shapes table |
| `GET /api/articles/{slug}` | value the instruction pins | C-DC-20 | Deployment contract API shapes table |
| `credits` | value the instruction pins | C-DC-20 | Deployment contract API shapes table |
| `client` | value the instruction pins | C-DC-20 | Deployment contract API shapes table |
| `design` | value the instruction pins | C-DC-20 | Deployment contract API shapes table |
| `POST /api/consent` | value the instruction pins | C-DC-21 | Deployment contract API shapes table |
| `visitorKey` | value the instruction pins | C-DC-21 | Deployment contract API shapes table |
| `categories` | value the instruction pins | C-DC-21 | Deployment contract API shapes table |
| `policyVersion` | value the instruction pins | C-DC-21 | Deployment contract API shapes table |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact shade behind each named colour role | C-UX-04 | the palette is described by role, family and tone only |
| the typeface family and every type size | C-UX-13 | the type system is described by personality and relationship |
| the base spacing unit, gutter and page margin | C-UX-18 | space is described as relationships |
| the corner radius of each shape | C-UX-15 | shape is described as a pill and a softly rounded rectangle |
| the duration and curve of the signature movement | C-UX-19 | motion is described by character |
| the widths of the two turning points and the ceiling | C-UX-25 | responsive behaviour is described by arrangement |
| the season boundaries of the about hero | C-FE-50 | configured editorially rather than pinned |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 10 |
| User roles | 1 | 19 |
| Core features | 78 | 420 |
| User flow | 8 | 20 |
| UI and UX notes | 6 | 30 |
| Technical requirements | 10 | 31 |
| Data model | 3 | 25 |
| Front-end specification | 25 | 67 |
| Constraints | 0 | 11 |
| Deployment contract | 10 | 26 |

Definition of done restates outcomes already itemised above and carries no checklist code.
