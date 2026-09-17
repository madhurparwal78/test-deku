# Checklist: Travel Luggage Storefront

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 943
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `constraint` The catalogue holds no listing from a second seller. `src: Overview, para 1; Constraints, bullet 1`
- [ ] `C-OV-02` `literal` The wordmark reads `valisette` in lower case on every page. `src: Overview, para 1`
- [ ] `C-OV-03` `capability` The catalogue organises products along a size axis. `src: Overview, para 2`
- [ ] `C-OV-04` `capability` The catalogue organises products along a collection axis of six named lines. `src: Overview, para 2`
- [ ] `C-OV-05` `capability` Every product exists in one or more colourways. `src: Overview, para 2`
- [ ] `C-OV-06` `capability` The running sale `Road Week` prices colourways below their list price. `src: Overview, para 3`
- [ ] `C-OV-07` `capability` A completed checkout opens a billing account at the payments provider. `src: Overview, para 3`
- [ ] `C-OV-08` `constraint` Stock never goes negative. `src: Overview, para 3`
- [ ] `C-OV-09` `constraint` The product offers no auction. `src: Overview, para 4; Constraints, bullet 1`
- [ ] `C-OV-10` `constraint` The product offers no customer reviews. `src: Overview, para 4; Constraints, bullet 2`
- [ ] `C-OV-11` `constraint` The product offers no live chat. `src: Overview, para 4; Constraints, bullet 2`
- [ ] `C-OV-12` `constraint` The product offers no subscription plan. `src: Overview, para 4; Constraints, bullet 2`
- [ ] `C-OV-13` `constraint` The product runs no loyalty scheme. `src: Overview, para 4; Constraints, bullet 2`
- [ ] `C-OV-14` `constraint` The price charged is the price in force at checkout. `src: Overview, para 4`
- [ ] `C-OV-15` `constraint` A repeated submission of one checkout produces one order. `src: Overview, para 4`
- [ ] `C-OV-16` `constraint` The last unit of a colourway is sold exactly once. `src: Overview, para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads products, collections, search without an account. `src: User roles, table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor keeps a cart. `src: User roles, table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor checks out as a guest. `src: User roles, table row 1`
- [ ] `C-RL-04` `role` A signed-out visitor subscribes to the newsletter. `src: User roles, table row 1`
- [ ] `C-RL-05` `role` A signed-out visitor checks a gift card balance. `src: User roles, table row 1`
- [ ] `C-RL-06` `role` A signed-out visitor opens no signed-in `/account` page. `src: User roles, table row 1`
- [ ] `C-RL-07` `role` A signed-out visitor reads no order. `src: User roles, table row 1`
- [ ] `C-RL-08` `role` A signed-out visitor calls no owner endpoint. `src: User roles, table row 1`
- [ ] `C-RL-09` `role` A customer keeps a cart attached to the account. `src: User roles, table row 2`
- [ ] `C-RL-10` `role` A customer saves delivery addresses. `src: User roles, table row 2`
- [ ] `C-RL-11` `role` A customer reads the account's own orders. `src: User roles, table row 2`
- [ ] `C-RL-12` `role` A customer reads no order of another account. `src: User roles, table row 2`
- [ ] `C-RL-13` `role` A customer reads no address of another account. `src: User roles, table row 2`
- [ ] `C-RL-14` `role` A customer calls no owner endpoint. `src: User roles, table row 2`
- [ ] `C-RL-15` `role` The owner renames products. `src: User roles, table row 3`
- [ ] `C-RL-16` `role` The owner reprices colourways. `src: User roles, table row 3`
- [ ] `C-RL-17` `role` The owner delists products. `src: User roles, table row 3`
- [ ] `C-RL-18` `role` The owner records stock movements. `src: User roles, table row 3`
- [ ] `C-RL-19` `role` The owner moves the end of the running sale. `src: User roles, table row 3`
- [ ] `C-RL-20` `role` The owner lists every order. `src: User roles, table row 3`
- [ ] `C-RL-21` `role` The owner fulfils a paid order. `src: User roles, table row 3`
- [ ] `C-RL-22` `role` The owner cancels a paid order. `src: User roles, table row 3`
- [ ] `C-RL-23` `role` The owner edits no stock movement once written. `src: User roles, table row 3`
- [ ] `C-RL-24` `role` The owner moves no order out of `cancelled`. `src: User roles, table row 3`
- [ ] `C-RL-25` `role` The owner moves no order out of `fulfilled`. `src: User roles, table row 3`
- [ ] `C-RL-26` `role` The server rejects a direct owner endpoint call from a customer session. `src: User roles, authorization paragraph`
- [ ] `C-RL-27` `role` A rejected owner call leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-28` `role` A signed-out caller is denied on every guarded endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-29` `role` One customer reaching for another customer's orders or addresses is denied. `src: User roles, authorization paragraph`
- [ ] `C-RL-30` `role` Every account created at `/account/register` is a `customer`. `src: User roles, signup paragraph`
- [ ] `C-RL-31` `role` No request body, form field or header chooses the role of a new account. `src: User roles, signup paragraph`
- [ ] `C-RL-32` `role` The seeded `owner@example.com` is the only `owner`. `src: User roles, signup paragraph`
- [ ] `C-RL-33` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-34` `literal` `owner@example.com` is the seeded owner Kiran Rao. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-35` `literal` `customer@example.com` is the seeded customer Aarav Mehta. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-36` `literal` `customer2@example.com` is the seeded customer Noor Haddad. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-37` `data` `customer@example.com` holds the orders `VS-100001` plus `VS-100002`. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-38` `data` `customer2@example.com` holds the order `VS-100003`. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-39` `data` `customer2@example.com` holds no saved address. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-40` `data` `owner@example.com` holds no orders, no addresses. `src: User roles, seeded accounts table row 1`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app runs an own email-with-password sign-in. `src: Core features, Accounts intro`
- [ ] `C-CF-02` `constraint` The app keeps only a slow salted hash of each password. `src: Core features, Accounts intro`
- [ ] `C-CF-03` `constraint` No response carries a password or a password hash. `src: Core features, Accounts intro`
- [ ] `C-CF-04` `capability` Signed-in API calls carry the bearer token handed back by sign-in. `src: Core features, Accounts intro`
- [ ] `C-CF-05` `literal` `POST /api/auth/signup` with `name`, `email`, `password` creates a `customer`. `src: Core features, Accounts rule 1`
- [ ] `C-CF-06` `literal` A signup returns `access_token`, `email`, `role`. `src: Core features, Accounts rule 1`
- [ ] `C-CF-07` `constraint` The app stores emails lowercased. `src: Core features, Accounts rule 1`
- [ ] `C-CF-08` `constraint` A second signup with an address in use, in any letter case, is rejected as invalid. `src: Core features, Accounts rule 1`
- [ ] `C-CF-09` `constraint` A rejected signup creates no account. `src: Core features, Accounts rule 1`
- [ ] `C-CF-10` `constraint` A signup password shorter than ten characters is rejected as invalid. `src: Core features, Accounts rule 1`
- [ ] `C-CF-11` `literal` `POST /api/auth/login` takes `email`, `password`, an optional `remember` flag. `src: Core features, Accounts rule 2`
- [ ] `C-CF-12` `literal` A sign-in returns `access_token`, `role`, `expires_at`. `src: Core features, Accounts rule 2`
- [ ] `C-CF-13` `constraint` A token issued without `remember` expires twelve hours after sign-in. `src: Core features, Accounts rule 2`
- [ ] `C-CF-14` `constraint` A token issued with `remember` set to true expires thirty days after sign-in. `src: Core features, Accounts rule 2`
- [ ] `C-CF-15` `constraint` A wrong password gets the same status, the same body, as an unknown email. `src: Core features, Accounts rule 3`
- [ ] `C-CF-16` `capability` A failed sign-in answers with the pinned email-or-password mismatch message. `src: Core features, Accounts rule 3`
- [ ] `C-CF-17` `capability` `POST /api/auth/logout` ends the session. `src: Core features, Accounts rule 4`
- [ ] `C-CF-18` `constraint` A logged-out token is turned away by every guarded endpoint. `src: Core features, Accounts rule 4`
- [ ] `C-CF-19` `constraint` A guarded endpoint turns away a call without a token. `src: Core features, Accounts rule 5`
- [ ] `C-CF-20` `constraint` A guarded endpoint turns away a token the app never issued. `src: Core features, Accounts rule 5`
- [ ] `C-CF-21` `constraint` A turned-away call changes nothing. `src: Core features, Accounts rule 5`
- [ ] `C-CF-22` `constraint` A signup body naming a `role` still creates a `customer`. `src: Core features, Accounts rule 6`
- [ ] `C-CF-23` `literal` `POST /api/auth/recover` answers `If we know that address, a reset link is on its way.` `src: Core features, Accounts rule 7`
- [ ] `C-CF-24` `constraint` A recovery answers with the same status for a known address as for an unknown one. `src: Core features, Accounts rule 7`
- [ ] `C-CF-25` `literal` A recovery for a known address sends one email with the subject `Reset your valisette password`. `src: Core features, Accounts rule 7`
- [ ] `C-CF-26` `literal` The reset email body opens with the link `<APP_PUBLIC_URL>/account/reset/<token>`. `src: Core features, Accounts rule 7`
- [ ] `C-CF-27` `constraint` A recovery for an unknown address sends no email. `src: Core features, Accounts rule 7`
- [ ] `C-CF-28` `capability` `POST /api/auth/reset` with the emailed token replaces the password. `src: Core features, Accounts rule 8`
- [ ] `C-CF-29` `constraint` A new password from a reset holds ten characters or more. `src: Core features, Accounts rule 8`
- [ ] `C-CF-30` `capability` After a reset the new password signs in. `src: Core features, Accounts rule 8`
- [ ] `C-CF-31` `constraint` After a reset the old password no longer signs in. `src: Core features, Accounts rule 8`
- [ ] `C-CF-32` `constraint` A reset token works once. `src: Core features, Accounts rule 8`
- [ ] `C-CF-33` `constraint` A used or unknown reset token is rejected as invalid, changing nothing. `src: Core features, Accounts rule 8`
- [ ] `C-CF-34` `literal` `GET /api/me` returns `name`, `email`, `role`. `src: Core features, Accounts rule 9`
- [ ] `C-CF-35` `constraint` Every product belongs to exactly one category. `src: Core features, Catalogue intro`
- [ ] `C-CF-36` `constraint` A product belongs to at most one of the six lines. `src: Core features, Catalogue intro`
- [ ] `C-CF-37` `constraint` A luggage product carries exactly one size class. `src: Core features, Catalogue intro`
- [ ] `C-CF-38` `constraint` A bag carries exactly one bag type. `src: Core features, Catalogue intro`
- [ ] `C-CF-39` `capability` A colourway is a variant of one product, identified by its `sku`. `src: Core features, Catalogue intro`
- [ ] `C-CF-40` `capability` Each colourway carries its own stock figure. `src: Core features, Catalogue intro`
- [ ] `C-CF-41` `capability` Each colourway carries its own price with its own list price. `src: Core features, Catalogue intro`
- [ ] `C-CF-42` `data` The thirteen colourways carry the codes, families of the colourway table. `src: Core features, Catalogue colourway table`
- [ ] `C-CF-43` `data` Each swatch colour is stored as a `#RRGGBB` string. `src: Core features, Catalogue para after the colourway table`
- [ ] `C-CF-44` `ui` Each swatch colour reads as the family of its colourway. `src: Core features, Catalogue para after the colourway table`
- [ ] `C-CF-45` `literal` A colourway `sku` joins the product SKU prefix, a hyphen, the colourway code, as in `PSG-CAB-OLV`. `src: Core features, Catalogue para before the product table`
- [ ] `C-CF-46` `literal` Prices are integer cents in `usd`, so `17900` is `$179`. `src: Core features, Catalogue para before the product table`
- [ ] `C-CF-47` `data` The thirty-nine products carry the handles, titles, categories, lines of the product table. `src: Core features, Catalogue product table`
- [ ] `C-CF-48` `data` Each product carries the size class or bag type, uses, tags, badge of the product table. `src: Core features, Catalogue product table`
- [ ] `C-CF-49` `data` Each product carries the price, list price, units sold, launch date of the product table. `src: Core features, Catalogue product table`
- [ ] `C-CF-50` `data` Each product lists the colourways of the product table in order. `src: Core features, Catalogue product table`
- [ ] `C-CF-51` `literal` Each colourway holds 20 units unless the table names an exception. `src: Core features, Catalogue para before the product table`
- [ ] `C-CF-52` `literal` `MRD-CAB-STB` is priced `19900` over `29900`. `src: Core features, Catalogue exceptions`
- [ ] `C-CF-53` `literal` `PSG-CAB-CSP` holds 0 units. `src: Core features, Catalogue exceptions`
- [ ] `C-CF-54` `literal` `VLT-CSE-NSH` holds 0 units. `src: Core features, Catalogue exceptions`
- [ ] `C-CF-55` `literal` `CTR-CAB-CSP` holds 2 units. `src: Core features, Catalogue exceptions`
- [ ] `C-CF-56` `literal` `RDG-TRL-SFL` holds exactly 1 unit. `src: Core features, Catalogue exceptions`
- [ ] `C-CF-57` `literal` Size classes are `cabin`, `check-in`, `check-in-large`, `trunk`, `kids`, `set`. `src: Core features, Catalogue para after the exceptions`
- [ ] `C-CF-58` `literal` Bag types are `backpack`, `briefcase`, `duffle`, `diaper-bag`, `kids-backpack`. `src: Core features, Catalogue para after the exceptions`
- [ ] `C-CF-59` `literal` Uses are `work`, `travel`, `diaper-and-kids`. `src: Core features, Catalogue para after the exceptions`
- [ ] `C-CF-60` `literal` Tags are `tech`, `clearance`. `src: Core features, Catalogue para after the exceptions`
- [ ] `C-CF-61` `literal` Product badges are `hot`, `must-have`. `src: Core features, Catalogue para after the exceptions`
- [ ] `C-CF-62` `literal` `GET /api/products/{handle}` returns `handle`, `title`, `category`, `line`, `size_class`, `bag_type`, `badge`. `src: Core features, Catalogue rule 1`
- [ ] `C-CF-63` `literal` The product read carries `personalisable`, `units_sold`, `weight_kg`, `capacity_litres`, `dimensions`, `description`. `src: Core features, Catalogue rule 1`
- [ ] `C-CF-64` `literal` Each variant carries `sku`, `colourway`, `colour_family`, `swatch`, `price`, `list_price`. `src: Core features, Catalogue rule 1`
- [ ] `C-CF-65` `literal` Each variant carries `discount_percent`, `on_sale`, `stock`, `in_stock`, `badge`, `media`. `src: Core features, Catalogue rule 1`
- [ ] `C-CF-66` `capability` The product read lists the other same-line products whose size class is cabin, check-in, check-in-large or set. `src: Core features, Catalogue rule 1`
- [ ] `C-CF-67` `literal` Each sibling carries `handle`, `title`, `size_class`. `src: Core features, Catalogue rule 1`
- [ ] `C-CF-68` `capability` `price` in every response is the live price. `src: Core features, Catalogue rule 2`
- [ ] `C-CF-69` `constraint` `discount_percent` is derived from the two prices, rounded to the nearest whole number with halves up. `src: Core features, Catalogue rule 2`
- [ ] `C-CF-70` `literal` `17900` over `29900` gives a `discount_percent` of `40`. `src: Core features, Catalogue rule 2`
- [ ] `C-CF-71` `literal` `19900` over `29900` gives `33`. `src: Core features, Catalogue rule 2`
- [ ] `C-CF-72` `literal` `59900` over `109900` gives `45`. `src: Core features, Catalogue rule 2`
- [ ] `C-CF-73` `literal` A colourway sold at its list price gives `0`. `src: Core features, Catalogue rule 2`
- [ ] `C-CF-74` `constraint` A colourway with no stock reads the badge `sold-out`. `src: Core features, Catalogue rule 3`
- [ ] `C-CF-75` `constraint` A colourway in stock reads the badge of its product. `src: Core features, Catalogue rule 3`
- [ ] `C-CF-76` `constraint` Only one badge ever applies to a colourway. `src: Core features, Catalogue rule 3`
- [ ] `C-CF-77` `literal` `Passage Luggage - Cabin` reads `sold-out` in `Corner Shop Pink`, `hot` in every other colourway. `src: Core features, Catalogue rule 3`
- [ ] `C-CF-78` `literal` `Vault Card Case` reads `sold-out` in `Night Shift`. `src: Core features, Catalogue rule 3`
- [ ] `C-CF-79` `capability` `units_sold` adds the units of every paid or fulfilled order placed since first start to the table figure. `src: Core features, Catalogue rule 4`
- [ ] `C-CF-80` `constraint` A cancelled order stops counting toward `units_sold`. `src: Core features, Catalogue rule 4`
- [ ] `C-CF-81` `capability` Products in the `luggage` category are `personalisable`. `src: Core features, Catalogue rule 5`
- [ ] `C-CF-82` `constraint` No product outside `luggage` is personalisable. `src: Core features, Catalogue rule 5`
- [ ] `C-CF-83` `literal` A `cabin` piece reads `3.23`, `40`, `54 x 37.5 x 23.5 cm`. `src: Core features, Catalogue rule 6 table row 1`
- [ ] `C-CF-84` `literal` A `check-in` piece reads `3.95`, `68`, `66 x 44 x 27 cm`. `src: Core features, Catalogue rule 6 table row 2`
- [ ] `C-CF-85` `literal` A `check-in-large` piece reads `4.70`, `98`, `76 x 50 x 30 cm`. `src: Core features, Catalogue rule 6 table row 3`
- [ ] `C-CF-86` `literal` A `trunk` piece reads `5.10`, `90`, `70 x 45 x 34 cm`. `src: Core features, Catalogue rule 6 table row 4`
- [ ] `C-CF-87` `literal` A `kids` piece reads `2.10`, `22`, `45 x 32 x 20 cm`. `src: Core features, Catalogue rule 6 table row 5`
- [ ] `C-CF-88` `literal` A set of 3 reads `11.88`, `206`, the three piece dimensions comma separated. `src: Core features, Catalogue rule 6 table row 6`
- [ ] `C-CF-89` `literal` A set of 2 reads `4.20`, `44`, `45 x 32 x 20 cm, 45 x 32 x 20 cm`. `src: Core features, Catalogue rule 6 table row 7`
- [ ] `C-CF-90` `capability` `media` lists four `image` shots per colourway at positions 1 to 4. `src: Core features, Catalogue rule 7`
- [ ] `C-CF-91` `literal` Each shot carries `alt` text such as `Passage Luggage - Cabin in Field Olive, front view`. `src: Core features, Catalogue rule 7`
- [ ] `C-CF-92` `constraint` A delisted product answers not found on its product page. `src: Core features, Catalogue rule 8`
- [ ] `C-CF-93` `constraint` A delisted product answers not found on its product API. `src: Core features, Catalogue rule 8`
- [ ] `C-CF-94` `constraint` A delisted product leaves every collection. `src: Core features, Catalogue rule 8`
- [ ] `C-CF-95` `constraint` A delisted product leaves the search. `src: Core features, Catalogue rule 8`
- [ ] `C-CF-96` `constraint` A delisted product leaves the home page bestsellers. `src: Core features, Catalogue rule 8`
- [ ] `C-CF-97` `constraint` A delisted product cannot join a cart. `src: Core features, Catalogue rule 8`
- [ ] `C-CF-98` `constraint` Every browsing destination is a collection. `src: Core features, Collections intro`
- [ ] `C-CF-99` `capability` A collection carries `handle`, `name`, `kind`, `position`, `strapline`. `src: Core features, Collections intro`
- [ ] `C-CF-100` `constraint` A collection holds exactly the products its rule selects. `src: Core features, Collections intro`
- [ ] `C-CF-101` `data` The thirty-one collections carry the handles, names, kinds, rules of the collection table. `src: Core features, Collections table`
- [ ] `C-CF-102` `literal` Each collection holds the product count of the collection table. `src: Core features, Collections table`
- [ ] `C-CF-103` `literal` Each collection carries the strapline of the collection table. `src: Core features, Collections table`
- [ ] `C-CF-104` `literal` `GET /api/collections` lists collections in table order with `handle`, `name`, `kind`, `product_count`. `src: Core features, Collections rule 1`
- [ ] `C-CF-105` `literal` `GET /api/collections/{handle}` returns `strapline`, `banner_title`, `siblings`. `src: Core features, Collections rule 2`
- [ ] `C-CF-106` `capability` Collection siblings are the other same-kind collections in table order, then the kind's parent. `src: Core features, Collections rule 2`
- [ ] `C-CF-107` `literal` The parent is `luggage` for `line` or `size`, `backpacks-and-briefcases` for `type` or `use`, `all` for `category` or `highlight`. `src: Core features, Collections rule 2`
- [ ] `C-CF-108` `literal` The siblings of `all` are the six categories. `src: Core features, Collections rule 2`
- [ ] `C-CF-109` `literal` A line `banner_title` reads `The <name> Series`, as in `The Meridian Series`. `src: Core features, Collections rule 2`
- [ ] `C-CF-110` `constraint` Every other collection uses its name as the `banner_title`. `src: Core features, Collections rule 2`
- [ ] `C-CF-111` `constraint` An unknown collection handle answers not found. `src: Core features, Collections rule 2`
- [ ] `C-CF-112` `literal` The collection products endpoint returns `products`, `total`, `page`, `page_size`. `src: Core features, Collections rule 3`
- [ ] `C-CF-113` `literal` `page_size` is `24`, with `page` counting from 1. `src: Core features, Collections rule 3`
- [ ] `C-CF-114` `constraint` `total` counts every product surviving the filters. `src: Core features, Collections rule 3`
- [ ] `C-CF-115` `literal` A card carries `handle`, `title`, `lowest_price`, `colourways`, `more_colourways`. `src: Core features, Collections rule 3`
- [ ] `C-CF-116` `capability` A card lists the first four colourways with `sku`, `colourway`, `swatch`, `price`, `list_price`, `in_stock`, `badge`. `src: Core features, Collections rule 3`
- [ ] `C-CF-117` `capability` `more_colourways` counts the colourways beyond the first four. `src: Core features, Collections rule 3`
- [ ] `C-CF-118` `literal` `sort` takes `featured`, `best-selling`, `price-asc`, `price-desc`, `newest`. `src: Core features, Collections rule 4`
- [ ] `C-CF-119` `capability` `featured` orders by `position` as the default. `src: Core features, Collections rule 4`
- [ ] `C-CF-120` `capability` `best-selling` orders by `units_sold`, most first. `src: Core features, Collections rule 4`
- [ ] `C-CF-121` `capability` The two price sorts order by the lowest live price of each product. `src: Core features, Collections rule 4`
- [ ] `C-CF-122` `capability` `newest` orders by launch date, latest first. `src: Core features, Collections rule 4`
- [ ] `C-CF-123` `constraint` Sort ties fall back to `position`. `src: Core features, Collections rule 4`
- [ ] `C-CF-124` `constraint` Any other `sort` value is rejected as invalid. `src: Core features, Collections rule 4`
- [ ] `C-CF-125` `capability` The repeatable `size` filter takes size classes. `src: Core features, Collections rule 5`
- [ ] `C-CF-126` `capability` The repeatable `colour` filter keeps products with any colourway in a chosen family. `src: Core features, Collections rule 5`
- [ ] `C-CF-127` `capability` `price_min` with `price_max` compare cents against the lowest live price, both ends included. `src: Core features, Collections rule 5`
- [ ] `C-CF-128` `capability` `in_stock` set to `true` keeps only products with a colourway in stock. `src: Core features, Collections rule 5`
- [ ] `C-CF-129` `constraint` A product must satisfy every filter group given. `src: Core features, Collections rule 5`
- [ ] `C-CF-130` `constraint` A product needs any one value within a filter group. `src: Core features, Collections rule 5`
- [ ] `C-CF-131` `constraint` The server sorts, filters over the whole collection before paging. `src: Core features, Collections rule 6`
- [ ] `C-CF-132` `constraint` Page 2 of a sorted, filtered collection continues where page 1 stopped. `src: Core features, Collections rule 6`
- [ ] `C-CF-133` `literal` `/api/collections/luggage/products` has `total` `20`. `src: Core features, Collections rule 7`
- [ ] `C-CF-134` `literal` `/api/collections/on-sale/products?page=2` returns 10 cards with `total` `34`. `src: Core features, Collections rule 7`
- [ ] `C-CF-135` `literal` Cabin luggage in pink returns `Passage Luggage - Cabin`, then `Contour Luggage - Cabin`. `src: Core features, Collections rule 7`
- [ ] `C-CF-136` `literal` Luggage sorted by `price-desc` starts with `Passage Luggage - Set of 3`. `src: Core features, Collections rule 7`
- [ ] `C-CF-137` `literal` All products sorted by `best-selling` start with `Passage Luggage - Cabin`, then `Passage Backpack - 30L`. `src: Core features, Collections rule 7`
- [ ] `C-CF-138` `literal` Wallets priced from `4000` to `5000` return only `Vault Card Case`. `src: Core features, Collections rule 7`
- [ ] `C-CF-139` `literal` `Meridian Luggage - Cabin` shows `more_colourways` `3`. `src: Core features, Collections rule 7`
- [ ] `C-CF-140` `literal` `Passage Luggage - Cabin` shows `more_colourways` `2`. `src: Core features, Collections rule 7`
- [ ] `C-CF-141` `capability` `best-sellers` holds the twenty products with the most `units_sold`, most first. `src: Core features, Collections rule 8`
- [ ] `C-CF-142` `capability` The home page shows the same twenty bestsellers in the same order. `src: Core features, Collections rule 8`
- [ ] `C-CF-143` `capability` `/collections/all` stacks the six categories in table order, each under a banner above its products. `src: Core features, Collections rule 9`
- [ ] `C-CF-144` `literal` The running sale is named `Road Week`. `src: Core features, Sale rule 1`
- [ ] `C-CF-145` `literal` `GET /api/sale` returns `name`, `ends_at`, `active`, `server_time`. `src: Core features, Sale rule 1`
- [ ] `C-CF-146` `constraint` The seeded sale ends at 00:00 UTC on the seventh day after the first start date. `src: Core features, Sale rule 1`
- [ ] `C-CF-147` `capability` During the sale every colourway sells at its stored sale price. `src: Core features, Sale rule 2`
- [ ] `C-CF-148` `constraint` After `ends_at`, every read uses the list price as `price`. `src: Core features, Sale rule 2`
- [ ] `C-CF-149` `constraint` After `ends_at`, every checkout charges the list price. `src: Core features, Sale rule 2`
- [ ] `C-CF-150` `constraint` After `ends_at`, `discount_percent` is `0`. `src: Core features, Sale rule 2`
- [ ] `C-CF-151` `constraint` After `ends_at`, `on_sale` is false. `src: Core features, Sale rule 2`
- [ ] `C-CF-152` `constraint` After `ends_at`, the `on-sale` collection is empty. `src: Core features, Sale rule 2`
- [ ] `C-CF-153` `constraint` After `ends_at`, the served collection page shows each list price as the live price. `src: Core features, Sale rule 2`
- [ ] `C-CF-154` `capability` Moving `ends_at` into the future brings the sale prices back. `src: Core features, Sale rule 2`
- [ ] `C-CF-155` `literal` `PATCH /api/owner/sale` with `ends_at` moves the end of the sale. `src: Core features, Sale rule 3`
- [ ] `C-CF-156` `role` Only the owner moves the end of the sale. `src: Core features, Sale rule 3`
- [ ] `C-CF-157` `capability` The countdown works from `ends_at` with the page's `server_time`, never the visitor clock. `src: Core features, Sale rule 4`
- [ ] `C-CF-158` `capability` At zero the offer strip disappears from the product page. `src: Core features, Sale rule 4`
- [ ] `C-CF-159` `capability` At zero the product page reads the prices again. `src: Core features, Sale rule 4`
- [ ] `C-CF-160` `constraint` A sale price never shows after the sale has ended. `src: Core features, Sale rule 4`
- [ ] `C-CF-161` `literal` `POST /api/carts` creates an empty cart with a `token`. `src: Core features, Cart rule 1`
- [ ] `C-CF-162` `constraint` A cart token holds at least 24 random letters or digits. `src: Core features, Cart rule 1`
- [ ] `C-CF-163` `constraint` The token is the only key to a cart. `src: Core features, Cart rule 1`
- [ ] `C-CF-164` `capability` A cart created with a bearer token is attached to that account. `src: Core features, Cart rule 1`
- [ ] `C-CF-165` `literal` `POST /api/carts/{token}/claim` attaches a signed-out cart to the caller. `src: Core features, Cart rule 1`
- [ ] `C-CF-166` `constraint` Claiming a cart attached to another account is denied. `src: Core features, Cart rule 1`
- [ ] `C-CF-167` `literal` `GET /api/me/cart` returns the most recently changed cart that has lines. `src: Core features, Cart rule 1`
- [ ] `C-CF-168` `constraint` `GET /api/me/cart` answers not found without such a cart. `src: Core features, Cart rule 1`
- [ ] `C-CF-169` `literal` `GET /api/carts/{token}` returns `token`, `lines`, `item_count`, `subtotal`, `discount`, `delivery`, `total`, `currency`. `src: Core features, Cart rule 2`
- [ ] `C-CF-170` `constraint` An unknown cart token answers not found. `src: Core features, Cart rule 2`
- [ ] `C-CF-171` `literal` `POST /api/carts/{token}/lines` takes `sku`, `quantity`, optional `properties`. `src: Core features, Cart rule 3`
- [ ] `C-CF-172` `constraint` A line quantity below 1 is rejected as invalid. `src: Core features, Cart rule 3; Core features, Cart rule 7`
- [ ] `C-CF-173` `constraint` Adding a `sku` already in the cart with the same properties raises that line's quantity. `src: Core features, Cart rule 3`
- [ ] `C-CF-174` `constraint` Different properties make a separate line. `src: Core features, Cart rule 3`
- [ ] `C-CF-175` `constraint` An unknown `sku` is rejected as invalid. `src: Core features, Cart rule 3`
- [ ] `C-CF-176` `literal` A line carries `id`, `sku`, `product_title`, `colourway`, `size_class`, `quantity`. `src: Core features, Cart rule 4`
- [ ] `C-CF-177` `literal` A line carries `unit_price`, `list_price`, `line_total`, `line_saving`, `properties`, `sold_out`. `src: Core features, Cart rule 4`
- [ ] `C-CF-178` `capability` `line_total` is `unit_price x quantity`. `src: Core features, Cart rule 4`
- [ ] `C-CF-179` `capability` `line_saving` is `(list_price - unit_price) x quantity`. `src: Core features, Cart rule 4`
- [ ] `C-CF-180` `constraint` A line's colourway never changes. `src: Core features, Cart rule 4`
- [ ] `C-CF-181` `capability` `subtotal` sums `list_price x quantity` over the lines. `src: Core features, Cart rule 5`
- [ ] `C-CF-182` `capability` `discount` sums every `line_saving`. `src: Core features, Cart rule 5`
- [ ] `C-CF-183` `literal` `delivery` is `0` in the cart. `src: Core features, Cart rule 5`
- [ ] `C-CF-184` `capability` `total` is `subtotal - discount + delivery`. `src: Core features, Cart rule 5`
- [ ] `C-CF-185` `constraint` A cart line never holds more units than its colourway has in stock. `src: Core features, Cart rule 6`
- [ ] `C-CF-186` `constraint` Every add or change reads the stock from the store at that moment. `src: Core features, Cart rule 6`
- [ ] `C-CF-187` `literal` An over-stock add or change is refused with `error` `insufficient_stock` plus `available`. `src: Core features, Cart rule 6`
- [ ] `C-CF-188` `literal` The refusal message follows `Only <available> left in stock.`, as in `Only 2 left in stock.` `src: Core features, Cart rule 6`
- [ ] `C-CF-189` `constraint` A refused change leaves the line at the quantity the line had. `src: Core features, Cart rule 6`
- [ ] `C-CF-190` `literal` A colourway with no stock is refused with `Sorry, the last one just sold out.` `src: Core features, Cart rule 6`
- [ ] `C-CF-191` `literal` `PATCH /api/carts/{token}/lines/{id}` with `quantity` changes a line. `src: Core features, Cart rule 7`
- [ ] `C-CF-192` `literal` `DELETE /api/carts/{token}/lines/{id}` removes a line. `src: Core features, Cart rule 7`
- [ ] `C-CF-193` `constraint` Adding to a cart holds no stock. `src: Core features, Cart rule 8`
- [ ] `C-CF-194` `constraint` A cart with its lines persists across reloads, browser restarts, sign-ins. `src: Core features, Cart rule 9`
- [ ] `C-CF-195` `constraint` Only a completed checkout or removing lines empties a cart. `src: Core features, Cart rule 9`
- [ ] `C-CF-196` `literal` A personalisable line may carry `properties` with `initials` plus `placement`. `src: Core features, Personalisation rule 1`
- [ ] `C-CF-197` `constraint` `initials` holds 1 to 7 letters, digits or spaces, stored in capitals. `src: Core features, Personalisation rule 1`
- [ ] `C-CF-198` `literal` `placement` is `front` or `top`. `src: Core features, Personalisation rule 1`
- [ ] `C-CF-199` `constraint` Any other placement is rejected as invalid. `src: Core features, Personalisation rule 1`
- [ ] `C-CF-200` `constraint` Empty or longer initials are rejected as invalid. `src: Core features, Personalisation rule 1`
- [ ] `C-CF-201` `constraint` Initials with other characters are rejected as invalid. `src: Core features, Personalisation rule 1`
- [ ] `C-CF-202` `constraint` Properties on a product that is not personalisable are rejected as invalid. `src: Core features, Personalisation rule 1`
- [ ] `C-CF-203` `capability` The properties travel unchanged from the cart line to the order line. `src: Core features, Personalisation rule 2`
- [ ] `C-CF-204` `literal` Personalisation shows as `Initials: <initials>, <placement>`, as in `Initials: AM, front`. `src: Core features, Personalisation rule 2`
- [ ] `C-CF-205` `constraint` Personalisation renders no preview, generating no artwork. `src: Core features, Personalisation rule 3; Constraints, bullet 5`
- [ ] `C-CF-206` `literal` The empty personalise panel reads `Design not created yet. Start customising`. `src: Core features, Personalisation rule 3`
- [ ] `C-CF-207` `literal` `POST /api/checkout` takes `cart_token`, `checkout_key`, `email`, `address`, `delivery_method`, optional `corporate_account`. `src: Core features, Checkout rule 1`
- [ ] `C-CF-208` `constraint` `checkout_key` holds 8 to 64 characters. `src: Core features, Checkout rule 1`
- [ ] `C-CF-209` `literal` The checkout address takes `name`, `line1`, optional `line2`, `city`, `region`, `postcode`, `country`, `phone`. `src: Core features, Checkout rule 1`
- [ ] `C-CF-210` `capability` A signed-in checkout links the order to the account. `src: Core features, Checkout rule 1`
- [ ] `C-CF-211` `capability` A signed-out checkout creates a guest order. `src: Core features, Checkout rule 1`
- [ ] `C-CF-212` `constraint` Checkout validation happens before anything is written. `src: Core features, Checkout rule 2`
- [ ] `C-CF-213` `literal` An empty cart is refused with `error` `cart_empty`. `src: Core features, Checkout rule 2`
- [ ] `C-CF-214` `constraint` A missing required address field is rejected as invalid, with `field` naming the first bad field. `src: Core features, Checkout rule 2`
- [ ] `C-CF-215` `constraint` A `postcode` that is not five digits is rejected as invalid. `src: Core features, Checkout rule 2`
- [ ] `C-CF-216` `constraint` A `country` other than `US` is rejected as invalid. `src: Core features, Checkout rule 2; Constraints, bullet 4`
- [ ] `C-CF-217` `constraint` A checkout `email` that is not an address is rejected as invalid. `src: Core features, Checkout rule 2`
- [ ] `C-CF-218` `constraint` A `delivery_method` outside `standard` or `express` is rejected as invalid. `src: Core features, Checkout rule 2`
- [ ] `C-CF-219` `literal` `standard` delivery costs `0`, arriving 3 to 5 days after the order date. `src: Core features, Checkout rule 3`
- [ ] `C-CF-220` `literal` `express` delivery costs `1500`, arriving 1 to 2 days after the order date. `src: Core features, Checkout rule 3`
- [ ] `C-CF-221` `literal` `GET /api/delivery-estimate?method=standard` returns `method`, `cost`, `from`, `to`. `src: Core features, Checkout rule 3`
- [ ] `C-CF-222` `constraint` The estimate dates are UTC dates counted from today. `src: Core features, Checkout rule 3`
- [ ] `C-CF-223` `literal` A live price differing from the cart `unit_price` refuses the checkout with `error` `price_changed`. `src: Core features, Checkout rule 4`
- [ ] `C-CF-224` `capability` A price-change refusal carries the pinned price-change message. `src: Core features, Checkout rule 4`
- [ ] `C-CF-225` `capability` A price-change refusal moves the cart lines to the live prices. `src: Core features, Checkout rule 4`
- [ ] `C-CF-226` `constraint` A price-change refusal writes nothing else. `src: Core features, Checkout rule 4`
- [ ] `C-CF-227` `capability` A second submission after a price change proceeds at the live prices. `src: Core features, Checkout rule 4`
- [ ] `C-CF-228` `constraint` The amount charged is always the price in force at checkout. `src: Core features, Checkout rule 4`
- [ ] `C-CF-229` `literal` A line asking for more units than the stock is refused with `error` `out_of_stock` plus the `sku`. `src: Core features, Checkout rule 5`
- [ ] `C-CF-230` `constraint` An out-of-stock refusal marks the line `sold_out` when none are left. `src: Core features, Checkout rule 5`
- [ ] `C-CF-231` `constraint` An out-of-stock refusal writes no order, no movement, no billing account. `src: Core features, Checkout rule 5`
- [ ] `C-CF-232` `literal` Order numbers read `VS-` followed by six digits, counting up from `VS-100004`. `src: Core features, Checkout rule 6`
- [ ] `C-CF-233` `capability` An accepted checkout opens the billing account in `killbill` with `POST /1.0/kb/accounts`. `src: Core features, Checkout rule 6`
- [ ] `C-CF-234` `literal` The billing account `externalKey` is `valisette-<number>`, as in `valisette-VS-100004`. `src: Core features, Checkout rule 6`
- [ ] `C-CF-235` `capability` The billing account carries the address `name`, the checkout `email`, `currency` `USD`, the address `country`. `src: Core features, Checkout rule 6`
- [ ] `C-CF-236` `constraint` An order becomes `paid` only once the provider answers with the account for its `externalKey`. `src: Core features, Checkout rule 6`
- [ ] `C-CF-237` `literal` The order `billing_account` is the account `externalKey`. `src: Core features, Checkout rule 6`
- [ ] `C-CF-238` `constraint` The app never marks an order paid on the strength of an own request alone. `src: Core features, Checkout rule 6`
- [ ] `C-CF-239` `capability` A corporate checkout opens no new billing account. `src: Core features, Checkout rule 7`
- [ ] `C-CF-240` `capability` A corporate checkout reads the account by `externalKey` at the provider. `src: Core features, Checkout rule 7`
- [ ] `C-CF-241` `literal` An unknown corporate account is refused with `error` `billing_account_unknown`. `src: Core features, Checkout rule 7`
- [ ] `C-CF-242` `literal` The unknown corporate refusal reads `We could not find that corporate account.` `src: Core features, Checkout rule 7`
- [ ] `C-CF-243` `literal` A corporate account not billed in `USD` is refused with `error` `billing_account_currency`. `src: Core features, Checkout rule 7`
- [ ] `C-CF-244` `literal` The currency refusal follows `That corporate account is billed in <currency>. Corporate orders are billed in USD.` `src: Core features, Checkout rule 7`
- [ ] `C-CF-245` `literal` `orbit-acme` is refused with `That corporate account is billed in EUR. Corporate orders are billed in USD.` `src: Core features, Checkout rule 7`
- [ ] `C-CF-246` `capability` A `USD` corporate account takes the order, whose `billing_account` is the key given. `src: Core features, Checkout rule 7`
- [ ] `C-CF-247` `literal` The provider holds `orbit-northwind`, Northwind Trading, in `USD`. `src: Core features, Checkout rule 7`
- [ ] `C-CF-248` `literal` The provider holds `orbit-acme`, Acme Partner Ltd, in `EUR`. `src: Core features, Checkout rule 7`
- [ ] `C-CF-249` `literal` The provider holds `orbit-amelia`, Amelia Ortega, in `EUR`. `src: Core features, Checkout rule 7`
- [ ] `C-CF-250` `constraint` A refused corporate checkout writes no order. `src: Core features, Checkout rule 7`
- [ ] `C-CF-251` `constraint` A refused corporate checkout moves no stock. `src: Core features, Checkout rule 7`
- [ ] `C-CF-252` `constraint` Paying, writing lines, taking stock, emptying the cart all happen together or not at all. `src: Core features, Checkout rule 8`
- [ ] `C-CF-253` `capability` Order lines keep the prices captured at payment. `src: Core features, Checkout rule 8`
- [ ] `C-CF-254` `capability` A paid order writes one `sale` movement per line. `src: Core features, Checkout rule 8`
- [ ] `C-CF-255` `capability` A completed checkout empties the cart. `src: Core features, Checkout rule 8`
- [ ] `C-CF-256` `constraint` A failed checkout leaves no order without its lines. `src: Core features, Checkout rule 8`
- [ ] `C-CF-257` `constraint` A failed checkout leaves no movement without its order. `src: Core features, Checkout rule 8`
- [ ] `C-CF-258` `constraint` A checkout repeated with the same `checkout_key` returns the first order with the same number. `src: Core features, Checkout rule 9`
- [ ] `C-CF-259` `constraint` A repeated checkout creates no second order. `src: Core features, Checkout rule 9`
- [ ] `C-CF-260` `constraint` A repeated checkout writes no second movement. `src: Core features, Checkout rule 9`
- [ ] `C-CF-261` `constraint` A repeated checkout opens no second billing account. `src: Core features, Checkout rule 9`
- [ ] `C-CF-262` `constraint` A repeated checkout sends no second email. `src: Core features, Checkout rule 9; Core features, Confirmation rule 3`
- [ ] `C-CF-263` `constraint` Two simultaneous submissions of one `checkout_key` still make one order. `src: Core features, Checkout rule 9`
- [ ] `C-CF-264` `capability` The provider refuses a second account whose `externalKey` is already in use. `src: Core features, Checkout rule 9`
- [ ] `C-CF-265` `constraint` Two checkouts for the last unit make exactly one paid order plus one `out_of_stock` refusal. `src: Core features, Checkout rule 10`
- [ ] `C-CF-266` `constraint` The contested colourway's stock ends at `0`, never below. `src: Core features, Checkout rule 10`
- [ ] `C-CF-267` `literal` An accepted checkout answers with `number`, `state`, `email`, `lines`, `address`, `delivery_method`, `delivery_from`, `delivery_to`. `src: Core features, Checkout rule 11`
- [ ] `C-CF-268` `literal` The order answer carries `subtotal`, `discount`, `delivery`, `total`, `currency` `usd`, `billing_account`, `placed_at`. `src: Core features, Checkout rule 11`
- [ ] `C-CF-269` `capability` Order totals follow the cart arithmetic with the chosen delivery cost added. `src: Core features, Checkout rule 11`
- [ ] `C-CF-270` `literal` One `PSG-CAB-OLV` with two `MNI-SLG-NSH` on `standard` totals `27700` from `45700` less `18000`. `src: Core features, Checkout rule 12 table row 1`
- [ ] `C-CF-271` `literal` The same cart on `express` totals `29200` with `1500` delivery. `src: Core features, Checkout rule 12 table row 2`
- [ ] `C-CF-272` `literal` One `MRD-CAB-STB` with one `PCK-CUB-HTG` on `standard` totals `22800` from `32800` less `10000`. `src: Core features, Checkout rule 12 table row 3`
- [ ] `C-CF-273` `literal` One `PSG-SET-NSH` after the sale ends totals `109900` with no discount. `src: Core features, Checkout rule 12 table row 4`
- [ ] `C-CF-274` `literal` Amounts show in dollars with a thousands separator, dropping zero cents, as `$277`, `$1,099`, `$44.75`. `src: Core features, Checkout rule 12`
- [ ] `C-CF-275` `capability` An order becoming `paid` sends one email over SMTP to the checkout `email`. `src: Core features, Confirmation rule 1`
- [ ] `C-CF-276` `constraint` The confirmation carries no cc, no bcc. `src: Core features, Confirmation rule 1`
- [ ] `C-CF-277` `literal` The confirmation comes from `orders@valisette.example.com`. `src: Core features, Confirmation rule 1`
- [ ] `C-CF-278` `literal` The subject reads exactly `Your valisette order <number> is confirmed`. `src: Core features, Confirmation rule 1`
- [ ] `C-CF-279` `literal` The body opens with `Order <number>, total charged <amount>.`, as in `Order VS-100004, total charged $277.` `src: Core features, Confirmation rule 2`
- [ ] `C-CF-280` `capability` The body lists every line with title, colourway, size class, quantity, personalisation. `src: Core features, Confirmation rule 2`
- [ ] `C-CF-281` `capability` The body names the delivery address with the arrival window. `src: Core features, Confirmation rule 2`
- [ ] `C-CF-282` `constraint` A refused checkout sends no email. `src: Core features, Confirmation rule 3`
- [ ] `C-CF-283` `constraint` A cart change, a signup, a sign-in, a newsletter subscription send no email. `src: Core features, Confirmation rule 3`
- [ ] `C-CF-284` `literal` `GET /api/me/orders` lists own orders newest first with `number`, `placed_at`, `total`, `currency`, `state`. `src: Core features, Orders rule 1`
- [ ] `C-CF-285` `capability` `GET /api/orders/{number}` returns an order to the account that placed the order. `src: Core features, Orders rule 2`
- [ ] `C-CF-286` `literal` The order read carries lines, address, state, delivery window, totals, `billing_account`. `src: Core features, Orders rule 2`
- [ ] `C-CF-287` `constraint` Another signed-in caller gets the same refusal as a number that does not exist. `src: Core features, Orders rule 2`
- [ ] `C-CF-288` `constraint` The refusal status with body is identical for an existing order as for a missing one. `src: Core features, Orders rule 2`
- [ ] `C-CF-289` `constraint` A guest order is read only through the owner endpoints. `src: Core features, Orders rule 2`
- [ ] `C-CF-290` `constraint` An order line keeps the captured `product_title`, `colourway`, `size_class`, `unit_price`, `list_price`. `src: Core features, Orders rule 3`
- [ ] `C-CF-291` `constraint` A later rename, reprice or delisting never changes what a past order says. `src: Core features, Orders rule 3`
- [ ] `C-CF-292` `literal` An order `state` is one of `pending`, `paid`, `fulfilled`, `cancelled`. `src: Core features, Orders rule 4`
- [ ] `C-CF-293` `constraint` The order number is unique. `src: Core features, Orders rule 4`
- [ ] `C-CF-294` `constraint` The order number is the only order identifier in any web address. `src: Core features, Orders rule 4`
- [ ] `C-CF-295` `literal` `GET /api/owner/orders` lists every order, newest first. `src: Core features, Orders rule 5`
- [ ] `C-CF-296` `literal` `POST /api/owner/orders/{number}/fulfil` moves a `paid` order to `fulfilled`. `src: Core features, Orders rule 5`
- [ ] `C-CF-297` `literal` `POST /api/owner/orders/{number}/cancel` moves a `paid` order to `cancelled`. `src: Core features, Orders rule 5`
- [ ] `C-CF-298` `capability` A cancel writes one `cancellation` movement per line with a positive delta. `src: Core features, Orders rule 5`
- [ ] `C-CF-299` `constraint` A cancel keeps the original `sale` movements. `src: Core features, Orders rule 5`
- [ ] `C-CF-300` `constraint` Any other order transition is rejected as invalid, changing nothing. `src: Core features, Orders rule 5`
- [ ] `C-CF-301` `constraint` Cancelling moves no money at the provider, leaving the billing account in place. `src: Core features, Orders rule 5`
- [ ] `C-CF-302` `literal` `GET /api/me/addresses` lists the caller's delivery addresses. `src: Core features, Orders rule 6`
- [ ] `C-CF-303` `literal` `POST /api/me/addresses` saves a delivery address. `src: Core features, Orders rule 6`
- [ ] `C-CF-304` `literal` `PATCH /api/me/addresses/{id}` changes a saved address. `src: Core features, Orders rule 6`
- [ ] `C-CF-305` `literal` `DELETE /api/me/addresses/{id}` removes a saved address. `src: Core features, Orders rule 6`
- [ ] `C-CF-306` `constraint` A saved address is validated like a checkout address. `src: Core features, Orders rule 6`
- [ ] `C-CF-307` `capability` The first address saved becomes the default. `src: Core features, Orders rule 6`
- [ ] `C-CF-308` `capability` `is_default` true makes that address the only default. `src: Core features, Orders rule 6`
- [ ] `C-CF-309` `capability` Deleting the default makes the oldest remaining address the default. `src: Core features, Orders rule 6`
- [ ] `C-CF-310` `constraint` Another account's address id answers not found, changing nothing. `src: Core features, Orders rule 6`
- [ ] `C-CF-311` `constraint` Every stock change is a stock movement. `src: Core features, Stock rule 1`
- [ ] `C-CF-312` `literal` A movement carries `sku`, `delta`, `kind`, `order_number`, `note`, `created_at`. `src: Core features, Stock rule 1`
- [ ] `C-CF-313` `literal` Movement kinds are `sale`, `restock`, `cancellation`, `adjustment`. `src: Core features, Stock rule 1`
- [ ] `C-CF-314` `constraint` A `sale` or `cancellation` movement names an `order_number`. `src: Core features, Stock rule 1`
- [ ] `C-CF-315` `constraint` A colourway's `stock` equals the sum of its movements' deltas. `src: Core features, Stock rule 1`
- [ ] `C-CF-316` `constraint` A movement is never updated. `src: Core features, Stock rule 1`
- [ ] `C-CF-317` `constraint` A movement is never deleted. `src: Core features, Stock rule 1`
- [ ] `C-CF-318` `literal` `POST /api/owner/stock-movements` takes `sku`, `delta`, `kind`, `note`. `src: Core features, Stock rule 2`
- [ ] `C-CF-319` `constraint` A movement `delta` is a whole number other than zero. `src: Core features, Stock rule 2`
- [ ] `C-CF-320` `constraint` A hand-written movement is `restock` or `adjustment`. `src: Core features, Stock rule 2`
- [ ] `C-CF-321` `constraint` A movement taking stock below zero is rejected, writing nothing. `src: Core features, Stock rule 2`
- [ ] `C-CF-322` `constraint` `sale` or `cancellation` movements cannot be written by hand. `src: Core features, Stock rule 2`
- [ ] `C-CF-323` `literal` `GET /api/owner/stock-movements?sku=<sku>` lists a colourway's movements, oldest first. `src: Core features, Stock rule 3`
- [ ] `C-CF-324` `constraint` Stock never reads below zero under any interleaving of checkouts, cancellations, owner movements. `src: Core features, Stock rule 4`
- [ ] `C-CF-325` `literal` `PATCH /api/owner/products/{handle}` changes `title`, `published`. `src: Core features, Owner edits rule 1`
- [ ] `C-CF-326` `capability` The owner endpoints reach a delisted product. `src: Core features, Owner edits rule 1`
- [ ] `C-CF-327` `literal` `PATCH /api/owner/variants/{sku}` changes `colourway`, `price`, `list_price`. `src: Core features, Owner edits rule 2`
- [ ] `C-CF-328` `constraint` A `price` above the `list_price` is rejected as invalid, changing nothing. `src: Core features, Owner edits rule 2`
- [ ] `C-CF-329` `constraint` A price at or below zero is rejected as invalid. `src: Core features, Owner edits rule 2`
- [ ] `C-CF-330` `role` Every owner endpoint denies a `customer`. `src: Core features, Owner edits rule 3`
- [ ] `C-CF-331` `role` Every owner endpoint denies a signed-out caller. `src: Core features, Owner edits rule 3`
- [ ] `C-CF-332` `constraint` A denied owner call leaves the catalogue unchanged. `src: Core features, Owner edits rule 3`
- [ ] `C-CF-333` `literal` `GET /api/search?q=<text>` returns `query`, `count`, `products` as collection cards. `src: Core features, Search rule 1`
- [ ] `C-CF-334` `constraint` Search matching ignores letter case. `src: Core features, Search rule 1`
- [ ] `C-CF-335` `capability` Search matches the product title. `src: Core features, Search rule 1`
- [ ] `C-CF-336` `capability` Search matches the colourway names. `src: Core features, Search rule 1`
- [ ] `C-CF-337` `capability` Search matches the name of the product's line. `src: Core features, Search rule 1`
- [ ] `C-CF-338` `literal` `olive` returns the 8 products that come in `Field Olive`. `src: Core features, Search rule 1`
- [ ] `C-CF-339` `capability` Title matches rank first, then colourway matches, then line-name matches. `src: Core features, Search rule 2`
- [ ] `C-CF-340` `constraint` Each search match group keeps `position` order. `src: Core features, Search rule 2`
- [ ] `C-CF-341` `literal` `coastal` returns the four `Coastal` titles, then `Ridge Trunk - Medium`, then `Ridge Cabin Pro`. `src: Core features, Search rule 2`
- [ ] `C-CF-342` `literal` `meridian` ends with `Overnight Backpack - 23L`. `src: Core features, Search rule 2`
- [ ] `C-CF-343` `capability` A search `sort` value reorders the results. `src: Core features, Search rule 3`
- [ ] `C-CF-344` `constraint` Filters do not apply to search. `src: Core features, Search rule 3`
- [ ] `C-CF-345` `literal` A query with no match returns `count` `0`. `src: Core features, Search rule 4`
- [ ] `C-CF-346` `capability` The empty search page quotes the query back. `src: Core features, Search rule 4`
- [ ] `C-CF-347` `capability` The empty search page offers the `best-sellers`, `on-sale`, `luggage` collections. `src: Core features, Search rule 4`
- [ ] `C-CF-348` `constraint` Recent searches stay in the visitor's own browser, never sent to the server. `src: Core features, Search rule 5; Core features, Standing pages rule 2`
- [ ] `C-CF-349` `capability` Recently viewed products stay in the visitor's own browser. `src: Core features, Search rule 5`
- [ ] `C-CF-350` `capability` A single control clears the recent searches. `src: Core features, Search rule 5`
- [ ] `C-CF-351` `literal` `GET /api/stores` returns `name`, `city`, `region`, `address`, `postcode`, `phone`, `hours`. `src: Core features, Store directory rule 1`
- [ ] `C-CF-352` `capability` Stores are ordered by `city`, then by `name`. `src: Core features, Store directory rule 1`
- [ ] `C-CF-353` `capability` `q` narrows stores to a city or name containing the text, ignoring letter case. `src: Core features, Store directory rule 1`
- [ ] `C-CF-354` `literal` `port` returns the two Portland stores. `src: Core features, Store directory rule 1`
- [ ] `C-CF-355` `literal` `new` returns `Newbury Street`, `Hudson Yards`, `SoHo`. `src: Core features, Store directory rule 1`
- [ ] `C-CF-356` `data` The fourteen stores carry the names, cities, regions, addresses, postcodes, phones, hours of the store table. `src: Core features, Store directory rule 2`
- [ ] `C-CF-357` `capability` An empty store filter lists every store. `src: Core features, Store directory rule 3`
- [ ] `C-CF-358` `constraint` The store directory shows no map. `src: Core features, Store directory rule 3; Constraints, bullet 6`
- [ ] `C-CF-359` `constraint` The store directory asks for no geolocation. `src: Core features, Store directory rule 3; Constraints, bullet 6`
- [ ] `C-CF-360` `constraint` The store directory offers no distance sort. `src: Core features, Store directory rule 3; Constraints, bullet 6`
- [ ] `C-CF-361` `capability` `POST /api/newsletter` stores the address lowercased. `src: Core features, Newsletter rule 1`
- [ ] `C-CF-362` `literal` A subscription answers `Thank you for subscribing!`. `src: Core features, Newsletter rule 1`
- [ ] `C-CF-363` `constraint` A repeat subscription answers the same, storing nothing new. `src: Core features, Newsletter rule 1`
- [ ] `C-CF-364` `constraint` A newsletter value that is not an email address is rejected as invalid. `src: Core features, Newsletter rule 1`
- [ ] `C-CF-365` `literal` `POST /api/gift-cards/balance` answers `balance` in cents with `currency` for an active card. `src: Core features, Newsletter rule 2`
- [ ] `C-CF-366` `literal` `VSGC-2026-AMBER` holds `5000`. `src: Core features, Newsletter rule 2`
- [ ] `C-CF-367` `constraint` Every other gift card code gets the same status, the same body. `src: Core features, Newsletter rule 2`
- [ ] `C-CF-368` `literal` The gift card refusal reads `That code is not recognised.` `src: Core features, Newsletter rule 2`
- [ ] `C-CF-369` `constraint` The expired `VSGC-2025-LAPSED` answers like an unknown code. `src: Core features, Newsletter rule 2`
- [ ] `C-CF-370` `literal` Ten standing pages live at `/pages/<handle>`. `src: Core features, Standing pages rule 1`
- [ ] `C-CF-371` `literal` `GET /api/pages/{handle}` returns `handle`, `title`, `body`. `src: Core features, Standing pages rule 1`
- [ ] `C-CF-372` `data` The standing pages carry the handles, titles of the page table. `src: Core features, Standing pages rule 1 table`
- [ ] `C-CF-373` `literal` The footer link texts of the page table lead to their pages. `src: Core features, Standing pages rule 1 table`
- [ ] `C-CF-374` `capability` The privacy page names the account details, saved addresses, orders, carts, newsletter address kept. `src: Core features, Standing pages rule 2`
- [ ] `C-CF-375` `literal` The privacy page keeps orders seven years. `src: Core features, Standing pages rule 2`
- [ ] `C-CF-376` `literal` The privacy page keeps carts ninety days after their last change. `src: Core features, Standing pages rule 2`
- [ ] `C-CF-377` `capability` The privacy page keeps accounts, newsletter addresses until removal is asked for. `src: Core features, Standing pages rule 2`
- [ ] `C-CF-378` `capability` The privacy page states that no card details are ever collected. `src: Core features, Standing pages rule 2`
- [ ] `C-CF-379` `capability` The privacy page states that search history never leaves the visitor's browser. `src: Core features, Standing pages rule 2`
- [ ] `C-CF-380` `capability` The footer of every page links the privacy page. `src: Core features, Standing pages rule 2`
- [ ] `C-CF-381` `capability` An unknown address renders the own not-found page inside the full chrome. `src: Core features, Standing pages rule 3`
- [ ] `C-CF-382` `literal` The not-found heading reads `That page has moved on without us.` `src: Core features, Standing pages rule 3`
- [ ] `C-CF-383` `capability` The not-found page carries one line of apology. `src: Core features, Standing pages rule 3`
- [ ] `C-CF-384` `literal` The not-found page links `/`, `/collections/all`, `/pages/stores`. `src: Core features, Standing pages rule 3`
- [ ] `C-CF-385` `constraint` The not-found page answers with a not-found status, never a success status. `src: Core features, Standing pages rule 3`
- [ ] `C-CF-386` `constraint` An unknown product, collection or page handle renders the not-found page. `src: Core features, Standing pages rule 3; User flow, Entry para`
- [ ] `C-CF-387` `literal` An unknown `/api` address answers JSON `error` `not_found` with a not-found status. `src: Core features, Standing pages rule 4`
- [ ] `C-CF-388` `capability` Every internal link on every page resolves to a page that exists. `src: Core features, Standing pages rule 5`
- [ ] `C-CF-389` `capability` Every document declares a favicon in its head. `src: Core features, Standing pages rule 6`
- [ ] `C-CF-390` `capability` The declared favicon answers as an image, the suitcase glyph drawn as vector markup. `src: Core features, Standing pages rule 6; Technical requirements, bullet 9`
- [ ] `C-CF-391` `capability` `item_count` is the sum of the line quantities, the number the rail with the drawer heading show. `src: Core features, Cart rule 5`

## C-UF User flow

- [ ] `C-UF-01` `capability` `/` serves the home page. `src: User flow, route table row 1`
- [ ] `C-UF-02` `capability` `/collections/<handle>` serves one collection. `src: User flow, route table row 2`
- [ ] `C-UF-03` `capability` `/collections/all` serves every product stacked by category under banners. `src: User flow, route table row 3`
- [ ] `C-UF-04` `capability` `/products/<handle>` serves one product. `src: User flow, route table row 4`
- [ ] `C-UF-05` `capability` `/search?q=<text>` serves search results with the query in the address. `src: User flow, route table row 5`
- [ ] `C-UF-06` `capability` `/cart` serves the cart with its summary. `src: User flow, route table row 6`
- [ ] `C-UF-07` `capability` `/checkout` serves the three checkout sections, then the confirmation. `src: User flow, route table row 7`
- [ ] `C-UF-08` `capability` `/pages/stores` serves the store directory. `src: User flow, route table row 8`
- [ ] `C-UF-09` `capability` `/pages/<handle>` serves the standing pages. `src: User flow, route table row 9`
- [ ] `C-UF-10` `capability` `/account/login`, `/account/register`, `/account/recover` serve the public account pages. `src: User flow, route table rows 10 to 12`
- [ ] `C-UF-11` `capability` `/account/reset/<token>` serves the new-password page. `src: User flow, route table row 13`
- [ ] `C-UF-12` `role` `/account`, `/account/orders`, `/account/orders/<number>`, `/account/addresses` need a signed-in visitor. `src: User flow, route table rows 14 to 17`
- [ ] `C-UF-13` `capability` A signed-out request for an account page lands on `/account/login?next=<path>`. `src: User flow, Entry para`
- [ ] `C-UF-14` `capability` Signing in returns to the `next` path. `src: User flow, Entry para`
- [ ] `C-UF-15` `capability` Signing in without a `next` lands on `/account`. `src: User flow, Entry para`
- [ ] `C-UF-16` `capability` Signing out returns to `/`. `src: User flow, Entry para`
- [ ] `C-UF-17` `constraint` A signed-out token stops working. `src: User flow, Entry para`
- [ ] `C-UF-18` `capability` A signed-in visitor opening `/account/login` lands on `/account`. `src: User flow, Entry para`
- [ ] `C-UF-19` `capability` `/checkout` with an empty cart redirects to `/cart`. `src: User flow, Entry para`
- [ ] `C-UF-20` `constraint` Another account's order number shows the same not-found page as a missing number. `src: User flow, Entry para`
- [ ] `C-UF-21` `capability` The `Luggage` rail panel's `Cabin` entry leads to `/collections/cabin`. `src: User flow, Journey 1`
- [ ] `C-UF-22` `capability` The `Sets` chip in the chip strip leads to `/collections/sets`. `src: User flow, Journey 1`
- [ ] `C-UF-23` `capability` The panel's `Meridian` entry leads to `/collections/meridian` under `The Meridian Series`. `src: User flow, Journey 1`
- [ ] `C-UF-24` `capability` Choosing a colourway thumbnail on a product page shows `Color:` with that colourway name. `src: User flow, Journey 2`
- [ ] `C-UF-25` `capability` `ADD TO CART` opens the cart drawer holding the new line. `src: User flow, Journey 2`
- [ ] `C-UF-26` `capability` A guest places an order from the drawer through `/checkout` to the confirmation. `src: User flow, Journey 2`
- [ ] `C-UF-27` `literal` The confirmation reads `Thank you. Your order is confirmed.` with a `VS-` number. `src: User flow, Journey 2`
- [ ] `C-UF-28` `capability` A collection filter choice shows the filter count beside `FILTER BY`. `src: User flow, Journey 4`
- [ ] `C-UF-29` `capability` A reload keeps the filtered collection view. `src: User flow, Journey 4`
- [ ] `C-UF-30` `capability` `Clear all` restores the unfiltered collection. `src: User flow, Journey 4`
- [ ] `C-UF-31` `capability` `Load more` appends cards, showing `page=2` in the address. `src: User flow, Journey 5`
- [ ] `C-UF-32` `capability` Returning from a product keeps the loaded collection depth. `src: User flow, Journey 5`
- [ ] `C-UF-33` `capability` A stepper raise past the stock shows the refusal line beside the alert mark. `src: User flow, Journey 6`
- [ ] `C-UF-34` `capability` The store filter `port` shows `2 stores`. `src: User flow, Journey 7`
- [ ] `C-UF-35` `capability` An opened store row shows opening hours, a phone number, a directions link. `src: User flow, Journey 7`
- [ ] `C-UF-36` `capability` The search overlay submit lands on `/search?q=olive` reading `8 results for "olive"`. `src: User flow, Journey 8`
- [ ] `C-UF-37` `capability` A later overlay lists `olive` under `Recent Searches`. `src: User flow, Journey 8`
- [ ] `C-UF-38` `capability` `Order History` from the rail lists `VS-100002` above `VS-100001`. `src: User flow, Journey 9`
- [ ] `C-UF-39` `capability` The `VS-100001` page shows `Passage Luggage - Cabin` in `Field Olive` at `$179`, state `Fulfilled`. `src: User flow, Journey 9`
- [ ] `C-UF-40` `capability` The gift card page shows `Balance: $50` for `VSGC-2026-AMBER`. `src: User flow, Journey 12`
- [ ] `C-UF-41` `capability` The gift card page shows `That code is not recognised.` for `VSGC-2025-LAPSED`. `src: User flow, Journey 12`
- [ ] `C-UF-42` `capability` A newsletter submit replaces the field with `Thank you for subscribing!` on the same page. `src: User flow, Journey 13`
- [ ] `C-UF-43` `capability` The recover page answers in place with the recovery message. `src: User flow, Journey 14`
- [ ] `C-UF-44` `ui` Every grid shows loading cells at the final size before cards arrive. `src: User flow, States para`
- [ ] `C-UF-45` `capability` A collection with no match shows `Nothing here matches that yet.` over `Clear the filters, or browse the whole range.` `src: User flow, States para`
- [ ] `C-UF-46` `capability` A search with no match shows `Nothing matched that.` over `Try a colour, a size, or one of these.` `src: User flow, States para`
- [ ] `C-UF-47` `capability` An empty cart shows `Your cart is empty` with `CONTINUE SHOPPING`. `src: User flow, States para`
- [ ] `C-UF-48` `capability` An account with no orders shows `No orders yet.` `src: User flow, States para`
- [ ] `C-UF-49` `capability` An account with no addresses shows `No saved addresses yet.` `src: User flow, States para`
- [ ] `C-UF-50` `capability` A grid failing to load more keeps its cards, adding a row with the alert mark plus `Try again`. `src: User flow, States para`
- [ ] `C-UF-51` `constraint` Errors never show a stack trace, never taking a page down. `src: User flow, States para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product itself is the first thing seen on every page. `src: UI/UX notes, North star para`
- [ ] `C-UX-02` `ui` The wall of products, the buy panel, the cart read dense, ruled, scannable. `src: UI/UX notes, North star para`
- [ ] `C-UX-03` `ui` Atmosphere lives in the drawn imagery rather than in decoration around the imagery. `src: UI/UX notes, North star para`
- [ ] `C-UX-04` `ui` The grid reads as one continuous ruled sheet, not floating cards. `src: UI/UX notes, North star para`
- [ ] `C-UX-05` `capability` Sorting with filtering sit in the left column beside the product wall. `src: UI/UX notes, North star para`
- [ ] `C-UX-06` `ui` The product is designed light, a white page with a black navigation column. `src: UI/UX notes, Mode para`
- [ ] `C-UX-07` `ui` Product pictures sit on a near-white neutral tile, with a slightly deeper tile where two tiles meet. `src: UI/UX notes, Palette para`
- [ ] `C-UX-08` `ui` The rail with every panel from the rail is pure black with white ink. `src: UI/UX notes, Palette para`
- [ ] `C-UX-09` `ui` Secondary ink is a mid cool neutral grey, black ink carrying the rest of the page. `src: UI/UX notes, Palette para`
- [ ] `C-UX-10` `ui` A light cool neutral hairline is the most used colour, separating the grid cells. `src: UI/UX notes, Palette para`
- [ ] `C-UX-11` `ui` The vivid amber accent grounds only the promotional ticker at full strength. `src: UI/UX notes, Palette para`
- [ ] `C-UX-12` `ui` A lighter amber marks the coverage term, a pale amber wash marks the active panel label, rail underline, product page rule. `src: UI/UX notes, Palette para`
- [ ] `C-UX-13` `ui` Nothing in the interface outside a promotion borrows the amber. `src: UI/UX notes, Palette para`
- [ ] `C-UX-14` `ui` A vivid red grounds only the fast-selling badge. `src: UI/UX notes, Palette para`
- [ ] `C-UX-15` `ui` The sold-out badge is grounded in black. `src: UI/UX notes, Palette para`
- [ ] `C-UX-16` `ui` A vivid orange marks only the warning mark beside a form or cart error. `src: UI/UX notes, Palette para`
- [ ] `C-UX-17` `ui` The single green in the product belongs to the size tile leading to a set. `src: UI/UX notes, Palette para`
- [ ] `C-UX-18` `ui` The dialog veil sits on translucent black. `src: UI/UX notes, Palette para`
- [ ] `C-UX-19` `ui` Panel column headings are white at reduced strength rather than a separate grey. `src: UI/UX notes, Palette para`
- [ ] `C-UX-20` `ui` A very pale swatch disc carries a hairline edge. `src: UI/UX notes, Palette para`
- [ ] `C-UX-21` `ui` One sans-serif family from the reader's own system carries the whole product. `src: UI/UX notes, Type para`
- [ ] `C-UX-22` `constraint` No font file is ever downloaded. `src: UI/UX notes, Type para`
- [ ] `C-UX-23` `ui` Titles, prices, rail links, running text share one body size, smaller steps carrying secondary text. `src: UI/UX notes, Type para`
- [ ] `C-UX-24` `ui` The ticker is set in the smallest capitals. `src: UI/UX notes, Type para`
- [ ] `C-UX-25` `ui` A section heading is the largest text on a page, about half again the body size. `src: UI/UX notes, Type para`
- [ ] `C-UX-26` `ui` The largest words in the product are drawn into pictures, never set as text. `src: UI/UX notes, Type para`
- [ ] `C-UX-27` `ui` Medium, semibold, boldest weights mark the active rail entry, size captions, panel card titles. `src: UI/UX notes, Type para`
- [ ] `C-UX-28` `ui` Figures line up in a column wherever prices, totals, quantities stack. `src: UI/UX notes, Type para`
- [ ] `C-UX-29` `ui` Corners are square on cells, tiles, banners, fields, buttons. `src: UI/UX notes, Shape para`
- [ ] `C-UX-30` `ui` Colourway swatches are full discs. `src: UI/UX notes, Shape para`
- [ ] `C-UX-31` `ui` The card badge sits flush to the cell edge, rounded only on the side leaving the edge. `src: UI/UX notes, Shape para`
- [ ] `C-UX-32` `ui` Only the swatch label with the search panel cast shadows. `src: UI/UX notes, Shape para`
- [ ] `C-UX-33` `ui` The phone header with the search veil blur what lies behind. `src: UI/UX notes, Shape para`
- [ ] `C-UX-34` `ui` Grid cells abut with no gap, text inset by one even margin beneath an edge-to-edge picture. `src: UI/UX notes, Shape para`
- [ ] `C-UX-35` `ui` A full wall of products fits a laptop screen. `src: UI/UX notes, Shape para`
- [ ] `C-UX-36` `literal` The layout archetype is `sidebar-nav`, a fixed left column beside the working surface. `src: UI/UX notes, Shape para`
- [ ] `C-UX-37` `constraint` Nothing slides in as the page scrolls. `src: UI/UX notes, Motion para`
- [ ] `C-UX-38` `constraint` Nothing follows the pointer. `src: UI/UX notes, Motion para`
- [ ] `C-UX-39` `ui` One symmetric curve eases every hover, open, close, colour change. `src: UI/UX notes, Motion para`
- [ ] `C-UX-40` `ui` The overshoot curve appears only on the cart count confirmation. `src: UI/UX notes, Motion para`
- [ ] `C-UX-41` `ui` Durations follow one ladder, control colour changes quickest, area-covering surfaces about a third of a second. `src: UI/UX notes, Motion para`
- [ ] `C-UX-42` `ui` The ticker glides left seamlessly, a lap taking about a minute, driven by time rather than scrolling. `src: UI/UX notes, Motion para`
- [ ] `C-UX-43` `ui` A panel lifts into place with a fade, its inner group growing slightly. `src: UI/UX notes, Motion para`
- [ ] `C-UX-44` `ui` A small aeroplane crosses the coverage strip, starting again. `src: UI/UX notes, Motion para`
- [ ] `C-UX-45` `ui` Drawers grow to their height, never blinking into place. `src: UI/UX notes, Motion para`
- [ ] `C-UX-46` `ui` A drawer plus mark never rotates. `src: UI/UX notes, Motion para`
- [ ] `C-UX-47` `ui` An open drawer row takes a bolder face with its hairline turning black. `src: UI/UX notes, Motion para`
- [ ] `C-UX-48` `ui` The phone header is the only element animating its width. `src: UI/UX notes, Motion para`
- [ ] `C-UX-49` `ui` Under reduced motion the ticker holds still on its first pair. `src: UI/UX notes, Motion para`
- [ ] `C-UX-50` `ui` Under reduced motion the aeroplane stops. `src: UI/UX notes, Motion para`
- [ ] `C-UX-51` `ui` Under reduced motion the cart count changes without the overshoot. `src: UI/UX notes, Motion para`
- [ ] `C-UX-52` `ui` Under reduced motion every drawer, panel, overlay still opens. `src: UI/UX notes, Motion para`
- [ ] `C-UX-53` `ui` A pointed-at rail link gains a pale amber underline. `src: UI/UX notes, Hover para`
- [ ] `C-UX-54` `ui` A pointed-at product card crossfades to the second view of the same colourway. `src: UI/UX notes, Hover para`
- [ ] `C-UX-55` `ui` A pointed-at swatch gains a black ring set off the disc, showing its label. `src: UI/UX notes, Hover para`
- [ ] `C-UX-56` `ui` A pointed-at main action keeps its black ground, turning its label pale amber. `src: UI/UX notes, Hover para`
- [ ] `C-UX-57` `ui` A pointed-at footer link gains an underline. `src: UI/UX notes, Hover para`
- [ ] `C-UX-58` `ui` Every hover state has a focus state at least as visible. `src: UI/UX notes, Hover para`
- [ ] `C-UX-59` `constraint` No information exists only on hover. `src: UI/UX notes, Hover para`
- [ ] `C-UX-60` `ui` Every control has resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, Components para`
- [ ] `C-UX-61` `ui` Unavailable is never signalled by colour alone. `src: UI/UX notes, Components para`
- [ ] `C-UX-62` `ui` The main action is a black ground with a white capitalised label. `src: UI/UX notes, Components para`
- [ ] `C-UX-63` `ui` The quieter action is a black outline with a black label on the page ground. `src: UI/UX notes, Components para`
- [ ] `C-UX-64` `ui` Each page leads with one primary action, visibly distinct from every secondary one. `src: UI/UX notes, Components para`
- [ ] `C-UX-65` `capability` Escape closes a drawer, panel, overlay or dialog, returning focus to the opener. `src: UI/UX notes, Components para`
- [ ] `C-UX-66` `capability` Removing an address asks once before acting, in place. `src: UI/UX notes, Components para`
- [ ] `C-UX-67` `literal` The product meets WCAG 2.2 level AA. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-68` `literal` Body text reaches a contrast of at least `4.5:1`. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-69` `literal` Large text, components, the focus indicator reach at least `3:1`. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-70` `ui` White text in the black column meets the same contrast bars. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-71` `ui` The live price is full-strength ink, the struck list price secondary grey, both passing. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-72` `ui` Touch targets meet the WCAG 2.2 minimum target size. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-73` `capability` Keyboard navigation reaches every control. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-74` `capability` Every panel, drawer, overlay, dialog works by keyboard alone. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-75` `constraint` Focus is held inside a dialog with the phone drawer, nowhere else. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-76` `ui` Tab order follows the visual order at every width. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-77` `capability` Each swatch control has the colourway name as its accessible name. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-78` `capability` Each group of swatches is labelled with the product name. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-79` `capability` The chosen swatch is marked pressed. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-80` `capability` Icon-only controls carry a text label. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-81` `ui` Meaning is never carried by colour alone. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-82` `capability` Every drawn product picture carries alternative text naming the product with the colourway. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-83` `capability` Every drawn editorial tile carries alternative text describing its scene. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-84` `ui` The layout holds at every viewport width from a phone to a wide desktop. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-85` `ui` A wide screen shows four cards across. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-86` `ui` A middle-width screen narrows the rail with three cards across. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-87` `ui` A phone swaps the rail for a floating translucent pill header, two cards across. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-88` `constraint` A phone keeps every product, filter, policy link reachable. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-89` `constraint` Nothing scrolls sideways except a strip meant to. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-90` `ui` No page is washed in yellow. `src: UI/UX notes, What it must not look like para`
- [ ] `C-UX-91` `ui` No gapped card grid with shadows stands where the ruled sheet belongs. `src: UI/UX notes, What it must not look like para`
- [ ] `C-UX-92` `ui` No marketing banner stack stands in place of the wall of products. `src: UI/UX notes, What it must not look like para`
- [ ] `C-UX-93` `ui` No product picture is a grey placeholder box. `src: UI/UX notes, What it must not look like para`
- [ ] `C-UX-94` `ui` No price saving has to be read from colour alone. `src: UI/UX notes, What it must not look like para`
- [ ] `C-UX-95` `ui` Every gap is a multiple of one base unit. `src: UI/UX notes, Shape para`
- [ ] `C-UX-96` `ui` Loading bars hold still under a reduced-motion request. `src: UI/UX notes, Motion para; Front-end specification, Product card para`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The front end is Svelte with Vite in TypeScript, built for production. `src: Technical requirements, bullet 1`
- [ ] `C-TR-02` `capability` The browser runs a single-page application on the same-origin JSON API. `src: Technical requirements, bullet 1`
- [ ] `C-TR-03` `capability` The served `/collections/<handle>` document already carries the first page of product titles with live prices. `src: Technical requirements, bullet 1; Front-end specification, Loading para`
- [ ] `C-TR-04` `capability` The served `/collections/all` document carries product titles before any script runs. `src: Technical requirements, bullet 1`
- [ ] `C-TR-05` `contract` The back end is Express on Node.js 20 in TypeScript, serving `/api` with the built front end. `src: Technical requirements, bullet 2`
- [ ] `C-TR-06` `capability` The back end answers the not-found status for an unknown address or handle, still serving the chrome. `src: Technical requirements, bullet 2`
- [ ] `C-TR-07` `contract` PostgreSQL is reached at `DATABASE_URL`, also exported as `DB_URL`, through the `pg` driver. `src: Technical requirements, bullet 3`
- [ ] `C-TR-08` `contract` `killbill` is reached at `PAYMENTS_API_URL`. `src: Technical requirements, bullet 4`
- [ ] `C-TR-09` `contract` Every `/1.0/kb/*` call carries Basic credentials from `PAYMENTS_API_USER` with `PAYMENTS_API_PASSWORD`. `src: Technical requirements, bullet 4`
- [ ] `C-TR-10` `contract` Every `/1.0/kb/*` call carries `X-Killbill-ApiKey` from `PAYMENTS_API_KEY` plus `X-Killbill-ApiSecret` from `PAYMENTS_API_SECRET`. `src: Technical requirements, bullet 4`
- [ ] `C-TR-11` `contract` A write to `killbill` carries `X-Killbill-CreatedBy`. `src: Technical requirements, bullet 4`
- [ ] `C-TR-12` `contract` `GET /1.0/healthcheck` answers without credentials. `src: Technical requirements, bullet 4`
- [ ] `C-TR-13` `literal` The billing account body is `{"name", "externalKey", "email", "currency", "country"}`. `src: Technical requirements, bullet 4`
- [ ] `C-TR-14` `contract` The account write answers `201` on create, `409` for a held key; the lookup answers `200` or `404`. `src: Technical requirements, bullet 4`
- [ ] `C-TR-15` `constraint` The product takes no card, card token or decline. `src: Technical requirements, bullet 4; Constraints, bullet 3`
- [ ] `C-TR-16` `contract` Mail goes to Mailpit over SMTP at `SMTP_HOST`, `SMTP_PORT`, with `SMTP_USER`, `SMTP_PASS` when set, through `nodemailer`. `src: Technical requirements, bullet 5`
- [ ] `C-TR-17` `contract` Auth is app-implemented email with password, using bearer tokens. `src: Technical requirements, bullet 6`
- [ ] `C-TR-18` `literal` `GET /api/health` returns `200` with `{"status": "ok"}` once PostgreSQL with `killbill` answer. `src: Technical requirements, bullet 7`
- [ ] `C-TR-19` `constraint` The app adds no second database, cache, queue, object store, identity provider or mail vendor. `src: Technical requirements, library para`
- [ ] `C-TR-20` `contract` Every host, port, credential is read from the environment. `src: Technical requirements, running services para`
- [ ] `C-TR-21` `capability` The app opens the billing accounts of `VS-100001` with `VS-100002` in `killbill` at first start. `src: Technical requirements, running services para`
- [ ] `C-TR-22` `capability` The app retries at start until the payments service answers. `src: Technical requirements, running services para`
- [ ] `C-TR-23` `literal` The scripts a page references directly stay within 180 KB once gzip compressed. `src: Technical requirements, bullet 8`
- [ ] `C-TR-24` `constraint` No page requests a raster image, a video, a font file or an icon sprite. `src: Technical requirements, bullet 9; Constraints, bullet 9`
- [ ] `C-TR-25` `constraint` Nothing the browser downloads carries a database credential, a payments credential, another shopper's token. `src: Technical requirements, bullet 10`
- [ ] `C-TR-26` `literal` Timestamps are UTC ISO 8601 strings ending in `Z`, dates written `YYYY-MM-DD`. `src: Technical requirements, bullet 11`
- [ ] `C-TR-27` `literal` List endpoints return a top-level JSON array, the collection with search endpoints excepted. `src: Technical requirements, bullet 12`
- [ ] `C-TR-28` `capability` Moving the end of the sale takes effect on the very next read. `src: Technical requirements, bullet 13`
- [ ] `C-TR-29` `constraint` The app uses only the named libraries plus their direct dependencies. `src: Technical requirements, library para`

## C-DM Data model

- [ ] `C-DM-01` `contract` `/app/USER_README.md` lists each seeded account with `deku-demo-pw-2026`. `src: Data model, password para; Deployment contract, bullet 5`
- [ ] `C-DM-02` `data` `account` carries `email` unique lowercased, `password_hash`, `name`, `role`, `created_at`. `src: Data model, account`
- [ ] `C-DM-03` `data` `session_token` carries `account_id`, `token_hash`, `expires_at`, `revoked_at`, `created_at`. `src: Data model, session_token`
- [ ] `C-DM-04` `data` `password_reset` carries `account_id`, `token_hash`, `used_at`, `created_at`. `src: Data model, password_reset`
- [ ] `C-DM-05` `data` `address` carries `name`, `line1`, `line2`, `city`, `region`, `postcode`, `country`, `phone`, `is_default`. `src: Data model, address`
- [ ] `C-DM-06` `constraint` An account holds at most one default address. `src: Data model, address`
- [ ] `C-DM-07` `data` `category` carries `handle` unique, `name`, `position`. `src: Data model, category`
- [ ] `C-DM-08` `data` `collection` carries `handle`, `name`, `kind`, `rule`, `strapline`, `position`. `src: Data model, collection`
- [ ] `C-DM-09` `literal` A collection `kind` is `line`, `size`, `category`, `type`, `use`, `highlight` or `all`. `src: Data model, collection`
- [ ] `C-DM-10` `data` `product` carries the table fields with `seed_units_sold`, `launched_on`, `position`, `published`. `src: Data model, product`
- [ ] `C-DM-11` `data` `variant` carries `sku` unique, `colourway`, `colour_family`, `swatch`, `price`, `list_price`, `position`. `src: Data model, variant`
- [ ] `C-DM-12` `constraint` A variant `price` never exceeds its `list_price`, both above zero. `src: Data model, variant`
- [ ] `C-DM-13` `data` `media` carries `variant_id`, `kind`, `position`, `alt`. `src: Data model, media`
- [ ] `C-DM-14` `literal` A media `kind` is `image` or `video`. `src: Data model, media`
- [ ] `C-DM-15` `data` `stock_movement` carries `variant_id`, `delta`, `kind`, `order_id`, `note`, `created_at`. `src: Data model, stock_movement`
- [ ] `C-DM-16` `constraint` `stock_movement` rows are only ever added. `src: Data model, stock_movement; Data model, Invariants bullet 2`
- [ ] `C-DM-17` `data` `store` carries `name`, `city`, `region`, `address`, `postcode`, `phone`, `hours`. `src: Data model, store`
- [ ] `C-DM-18` `data` `cart` carries `token` unique, `account_id`, `created_at`, `updated_at`. `src: Data model, cart`
- [ ] `C-DM-19` `data` `cart_line` carries `cart_id`, `variant_id`, `quantity`, `properties`, `unit_price_captured`, `added_at`. `src: Data model, cart_line`
- [ ] `C-DM-20` `data` `orders` carries `number` unique, `account_id`, `email`, `address_snapshot`, `delivery_method`. `src: Data model, orders`
- [ ] `C-DM-21` `data` `orders` carries `subtotal`, `discount`, `delivery`, `total`, `currency`, `state`, `checkout_key` unique, `billing_account`, `placed_at`. `src: Data model, orders`
- [ ] `C-DM-22` `constraint` One order exists per `checkout_key`, however often submitted. `src: Data model, orders`
- [ ] `C-DM-23` `data` `order_line` carries `order_id`, `variant_id`, `sku`, `product_title`, `colourway`, `size_class`, `quantity`, `unit_price`, `list_price`, `properties`. `src: Data model, order_line`
- [ ] `C-DM-24` `data` `subscriber` carries `email` unique lowercased, `created_at`. `src: Data model, subscriber`
- [ ] `C-DM-25` `data` `gift_card` carries `code` unique, `balance`, `currency`, `expires_on`. `src: Data model, gift_card`
- [ ] `C-DM-26` `data` `sale` carries `name`, `ends_at`. `src: Data model, sale`
- [ ] `C-DM-27` `data` `page` carries `handle` unique, `title`, `body`. `src: Data model, page`
- [ ] `C-DM-28` `constraint` Stock, discount, badge, units sold, members, cart sums, delivery windows are derived, never stored columns. `src: Data model, derived para`
- [ ] `C-DM-29` `constraint` An order in `paid`, `fulfilled` or `cancelled` has its `billing_account` set. `src: Data model, Invariants bullet 4`
- [ ] `C-DM-30` `constraint` An order in `paid`, `fulfilled` or `cancelled` has one `sale` movement per line. `src: Data model, Invariants bullet 4`
- [ ] `C-DM-31` `constraint` A failed action leaves no partial row. `src: Data model, Invariants bullet 5`
- [ ] `C-DM-32` `literal` Seeding writes one `restock` movement per colourway for the table quantity plus the seeded order units. `src: Data model, Seed data bullet 1`
- [ ] `C-DM-33` `literal` Seeding writes one `sale` movement per seeded order line. `src: Data model, Seed data bullet 1`
- [ ] `C-DM-34` `data` `customer@example.com` holds the default address `Aarav Mehta`, `42 Alder Lane`, `Apt 3`, `Portland`, `OR`, `97205`, `US`, `+1 503 555 0177`. `src: Data model, Seed data bullet 2`
- [ ] `C-DM-35` `data` `VS-100001` is `fulfilled`, placed 20 days before first start, one `PSG-CAB-OLV` at 17900 over 29900, `standard`, subtotal 29900, discount 12000, delivery 0, total 17900, billed to `valisette-VS-100001`. `src: Data model, Seed data orders table row 1`
- [ ] `C-DM-36` `data` `VS-100002` is `paid`, placed 2 days before first start, one `MNI-SLG-NSH` plus one `PCK-CUB-HTG`, `express`, subtotal 10800, discount 3000, delivery 1500, total 9300, billed to `valisette-VS-100002`. `src: Data model, Seed data orders table row 2`
- [ ] `C-DM-37` `data` `VS-100003` is `paid`, placed 1 day before first start, two `VLT-SLV-OLV`, `standard`, subtotal 11800, discount 4000, delivery 0, total 7800, billed to `orbit-northwind`. `src: Data model, Seed data orders table row 3`
- [ ] `C-DM-38` `data` `VS-100003` ships to `Noor Haddad`, `9 Birch Court`, `Seattle`, `WA`, `98101`, `US`, `+1 206 555 0188`. `src: Data model, Seed data orders para`
- [ ] `C-DM-39` `data` The seed carries the fourteen stores, the ten standing pages, the `Road Week` sale. `src: Data model, Seed data bullet 4`
- [ ] `C-DM-40` `literal` `VSGC-2026-AMBER` holds `5000` in `usd` with no expiry. `src: Data model, Seed data bullet 4`
- [ ] `C-DM-41` `literal` `VSGC-2025-LAPSED` holds `2500`, expired on `2025-12-31`. `src: Data model, Seed data bullet 4`
- [ ] `C-DM-42` `constraint` Restarting the app duplicates no row. `src: Data model, closing para`
- [ ] `C-DM-43` `constraint` Restarting writes no second set of seed movements. `src: Data model, closing para`
- [ ] `C-DM-44` `constraint` Restarting opens no second billing account. `src: Data model, closing para`
- [ ] `C-DM-45` `data` `VS-100001` with `VS-100002` ship to the default address of `customer@example.com`. `src: Data model, Seed data orders para`

## C-FE Front-end specification

- [ ] `C-FE-01` `capability` The first control on every page is a `Skip to content` link, hidden until focused. `src: Front-end specification, Chrome para`
- [ ] `C-FE-02` `capability` Every page has one `banner`, one `main`, one `contentinfo` landmark. `src: Front-end specification, Chrome para; Front-end specification, Machine-readable hooks para`
- [ ] `C-FE-03` `ui` The ticker is a thin full-width band on the vivid amber ground above everything, the rail included. `src: Front-end specification, Ticker para`
- [ ] `C-FE-04` `literal` The ticker alternates `Road Week - Up to 50% off` with `LIVE NOW`. `src: Front-end specification, Ticker para`
- [ ] `C-FE-05` `ui` A small upright pale amber bar separates each ticker pair. `src: Front-end specification, Ticker para`
- [ ] `C-FE-06` `constraint` The ticker never shifts page layout when wrapping, the page never scrolling with the ticker. `src: Front-end specification, Ticker para`
- [ ] `C-FE-07` `capability` Every ticker item links to `/collections/on-sale`. `src: Front-end specification, Ticker para`
- [ ] `C-FE-08` `ui` The ticker looks identical on every screen size. `src: Front-end specification, Ticker para`
- [ ] `C-FE-09` `capability` The ticker is hidden once the sale has ended. `src: Front-end specification, Ticker para`
- [ ] `C-FE-10` `ui` On wide or middle screens the rail is a fixed full-height black column that never scrolls. `src: Front-end specification, Rail para`
- [ ] `C-FE-11` `ui` The rail holds three blocks separated by a sliver of page ground, reading as three cards. `src: Front-end specification, Rail para`
- [ ] `C-FE-12` `literal` The category block lists `Luggage`, `Backpacks & Briefcases`, `Totes`, `Slings & Crossbodies`, `Accessories`, `Wallets`, `Gift Card`, `Clearance Sale`. `src: Front-end specification, Rail para`
- [ ] `C-FE-13` `capability` The first two rail categories open a panel. `src: Front-end specification, Rail para`
- [ ] `C-FE-14` `capability` The other rail categories lead straight to their collections or the gift card page. `src: Front-end specification, Rail para`
- [ ] `C-FE-15` `ui` The actions block sits on white, `SEARCH` in the boldest type above `ACCOUNT` with `CART`, glyphs aligned right. `src: Front-end specification, Rail para`
- [ ] `C-FE-16` `capability` The rail cart row shows the item count beside `CART`. `src: Front-end specification, Rail para`
- [ ] `C-FE-17` `capability` The rail cart row disappears whenever the cart is empty rather than showing a zero. `src: Front-end specification, Rail para`
- [ ] `C-FE-18` `capability` Signed in, the rail account row shows `Order History` with `Logout` beneath. `src: Front-end specification, Rail para`
- [ ] `C-FE-19` `capability` The fourth rail block appears on collection pages with `SORT BY` above `FILTER BY`, on the search page with `SORT BY` alone, on no other page. `src: Front-end specification, Rail para`
- [ ] `C-FE-20` `capability` On a product page the rail collapses to the wordmark block alone. `src: Front-end specification, Rail para`
- [ ] `C-FE-21` `ui` The collapsed product page rail carries a pale amber rule along its lower edge. `src: Front-end specification, Rail para`
- [ ] `C-FE-22` `ui` A panel's left edge meets the rail with no seam, the panel floating above the content. `src: Front-end specification, Panels para`
- [ ] `C-FE-23` `literal` The luggage panel carries the `By Size`, `By Collection`, `Highlights` columns. `src: Front-end specification, Panels para`
- [ ] `C-FE-24` `literal` The luggage panel image cards read `Passage Collection`, `Meridian Collection`. `src: Front-end specification, Panels para`
- [ ] `C-FE-25` `literal` The bags panel carries the `Collection`, `By Use`, `Highlights` columns. `src: Front-end specification, Panels para`
- [ ] `C-FE-26` `capability` Every panel entry leads to the collection of the same name. `src: Front-end specification, Panels para`
- [ ] `C-FE-27` `capability` A panel's `View All` leads to the panel's category. `src: Front-end specification, Panels para`
- [ ] `C-FE-28` `ui` Panel headings are capitalised, entries solid white, one per line. `src: Front-end specification, Panels para`
- [ ] `C-FE-29` `ui` The entry for the viewed collection carries the pale amber wash. `src: Front-end specification, Panels para`
- [ ] `C-FE-30` `ui` Panel image cards are rounded with a bold white title over a drawn picture. `src: Front-end specification, Panels para`
- [ ] `C-FE-31` `ui` A panel opens on pointer entry, closing once the pointer has left with a short grace. `src: Front-end specification, Panels para`
- [ ] `C-FE-32` `capability` The rail entry toggles its panel from the keyboard, moving focus into the panel. `src: Front-end specification, Panels para`
- [ ] `C-FE-33` `capability` Escape closes the panel, returning focus to the rail entry. `src: Front-end specification, Panels para`
- [ ] `C-FE-34` `capability` `SEARCH` opens a full-page overlay rather than a new page. `src: Front-end specification, Search overlay para`
- [ ] `C-FE-35` `ui` The overlay veil is translucent black, softly blurring the whole page. `src: Front-end specification, Search overlay para`
- [ ] `C-FE-36` `ui` The overlay panel covers most of the window, all of the window on a phone, with the one deep shadow. `src: Front-end specification, Search overlay para`
- [ ] `C-FE-37` `literal` The overlay shows `Recent Searches` with a `Clear` control above `Recently Viewed Products`. `src: Front-end specification, Search overlay para`
- [ ] `C-FE-38` `capability` Escape closes the overlay, returning focus to `SEARCH`. `src: Front-end specification, Search overlay para`
- [ ] `C-FE-39` `literal` The newsletter block reads `Warm Hugs, valisette.` above the pinned two-line body. `src: Front-end specification, Footer para`
- [ ] `C-FE-40` `literal` The newsletter field placeholder reads `Enter Email Address`. `src: Front-end specification, Footer para`
- [ ] `C-FE-41` `ui` The newsletter submit is a square button carrying an up-and-right arrow. `src: Front-end specification, Footer para`
- [ ] `C-FE-42` `capability` A newsletter success never navigates away. `src: Front-end specification, Footer para`
- [ ] `C-FE-43` `ui` The footer is black with a low-contrast drawn landscape behind readable white text. `src: Front-end specification, Footer para`
- [ ] `C-FE-44` `capability` The footer holds the wordmark, the contact block, two link columns, the brand essay. `src: Front-end specification, Footer para`
- [ ] `C-FE-45` `literal` The contact block reads `Need assistance?` above the pinned contact sentence, the support address plus phone as links. `src: Front-end specification, Footer para`
- [ ] `C-FE-46` `literal` The gifting block reads `For Gifting & Corporate orders` above `Message us at +1 503 555 0199 or email gifting@valisette.example.com`. `src: Front-end specification, Footer para`
- [ ] `C-FE-47` `literal` The first footer link column lists `FAQ`, `Claim My Warranty`, `Terms & Conditions`, `Airline Damage Policy`, `Blogs`. `src: Front-end specification, Footer para`
- [ ] `C-FE-48` `literal` The second footer link column lists `Claim 30 Day Trial`, `Return & Refund Policy`, `Privacy Policy`, the careers link, `Check Gift Card Balance`. `src: Front-end specification, Footer para`
- [ ] `C-FE-49` `literal` The footer essay is headed `#KeepMoving` above the pinned essay body. `src: Front-end specification, Footer para`
- [ ] `C-FE-50` `ui` On a phone the two footer link columns become drawers with a down chevron. `src: Front-end specification, Footer para`
- [ ] `C-FE-51` `constraint` Every icon is drawn by the page from geometry, never loaded as a file. `src: Front-end specification, Iconography para`
- [ ] `C-FE-52` `ui` The icon set covers search, account, cart, close, chevrons, wedge, home, plus, filter, tick, pin, card, warning, play, arrow glyphs. `src: Front-end specification, Iconography para`
- [ ] `C-FE-53` `ui` The size tile suitcase is amber-yellow with black wheels, a telescopic handle, a label plate, seven grooves. `src: Front-end specification, Iconography para`
- [ ] `C-FE-54` `ui` Larger sizes draw a taller suitcase, a set tile two or three smaller suitcases. `src: Front-end specification, Iconography para`
- [ ] `C-FE-55` `constraint` The product ships no photograph. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-56` `ui` Drawn product pictures float in generous margin on the near-white tile ground. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-57` `ui` The same colourway always draws the same picture across reloads. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-58` `ui` Hard-shell luggage shows a shaded body, vertical grooves, a darker plate, four wheels, a handle, an amber stripe on half the colourways. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-59` `ui` Soft bags show a narrowing body, a flap with a shadow line, straps, pockets. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-60` `ui` Totes show a gently convex body with two long handle arcs. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-61` `ui` Wallets show a wide rounded rectangle with an amber stripe near the bottom. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-62` `ui` Every drawn object sits over one soft elliptical shadow wider than the object. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-63` `ui` The four shots of a colourway are front, side, back, interior views of one object. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-64` `ui` Editorial tiles are drawn duotone compositions with a silhouette, soft shapes, words drawn in white. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-65` `ui` The video tile shows a drawn still frame with the play triangle, playing a drawn pan when pressed. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-66` `constraint` No video file is ever fetched. `src: Front-end specification, Zero-asset para`
- [ ] `C-FE-67` `ui` The product card is identical on the home page, collections, search, recently viewed, cross-sell. `src: Front-end specification, Product card para`
- [ ] `C-FE-68` `ui` A card is a ruled cell with square corners with no shadow. `src: Front-end specification, Product card para`
- [ ] `C-FE-69` `literal` A card title links to `/products/<handle>?sku=<sku>` for the chosen colourway. `src: Front-end specification, Product card para`
- [ ] `C-FE-70` `ui` The card price row shows the live price, then the struck list price smaller in grey. `src: Front-end specification, Product card para`
- [ ] `C-FE-71` `ui` A card shows no struck price when the two prices are equal. `src: Front-end specification, Product card para`
- [ ] `C-FE-72` `capability` The card swatch row shows up to four discs, then `+<n>`. `src: Front-end specification, Product card para`
- [ ] `C-FE-73` `ui` The overflow count is not a control, never expanding the row. `src: Front-end specification, Product card para`
- [ ] `C-FE-74` `capability` Choosing a disc switches the card picture, prices, link in place without reloading or moving. `src: Front-end specification, Product card para`
- [ ] `C-FE-75` `ui` The chosen disc carries a black ring with a gap, the disc keeping its size. `src: Front-end specification, Product card para`
- [ ] `C-FE-76` `capability` A card shows at most one badge: `SOLD OUT`, `HOT` or `MUST HAVE`. `src: Front-end specification, Product card para`
- [ ] `C-FE-77` `ui` Badge labels are small white capitals, `MUST HAVE` set on two lines, `HOT` on the vivid red. `src: Front-end specification, Product card para`
- [ ] `C-FE-78` `ui` A sold-out colourway shows a faded picture. `src: Front-end specification, Product card para`
- [ ] `C-FE-79` `ui` Pointing at a swatch shows a small black label centred above the disc whatever the name length. `src: Front-end specification, Product card para`
- [ ] `C-FE-80` `ui` Loading cells hold the final size with gently pulsing bars. `src: Front-end specification, Product card para`
- [ ] `C-FE-81` `ui` The home page runs several screens tall, meant to be scrolled. `src: Front-end specification, Home para`
- [ ] `C-FE-82` `capability` The hero carousel shows three drawn slides leading to `/collections/passage`, `/collections/meridian`, `/collections/on-sale`. `src: Front-end specification, Home para`
- [ ] `C-FE-83` `ui` Hero slides carry no text or button over the picture. `src: Front-end specification, Home para`
- [ ] `C-FE-84` `capability` Indicators, dragging, arrow keys change the hero slide, never a timer. `src: Front-end specification, Home para`
- [ ] `C-FE-85` `ui` Thin indicator bars sit beneath the slides, the active one solid white. `src: Front-end specification, Home para`
- [ ] `C-FE-86` `literal` The collections strip reads `Luggage Collections` with `Passage Collection`, `Coastal Collection`, `Meridian Collection`. `src: Front-end specification, Home para`
- [ ] `C-FE-87` `literal` The categories strip reads `Categories` with `Luggage`, `Bags & Backpacks`, `Totes & Handbags`, `Travel Accessories`, `Wallets`. `src: Front-end specification, Home para`
- [ ] `C-FE-88` `capability` The home collection tiles with category tiles lead to their collections. `src: Front-end specification, Home para`
- [ ] `C-FE-89` `ui` Strip tiles carry a white caption in the bottom corner over a translucent black scrim. `src: Front-end specification, Home para`
- [ ] `C-FE-90` `ui` The categories strip scrolls sideways on middle screens with phones. `src: Front-end specification, Home para`
- [ ] `C-FE-91` `literal` The grid heading reads `Bestsellers` with `View All` leading to `/collections/best-sellers`. `src: Front-end specification, Home para`
- [ ] `C-FE-92` `literal` An editorial tile after the first grid row reads `ELEVATE` over `your daily carry`. `src: Front-end specification, Home para`
- [ ] `C-FE-93` `literal` An editorial tile after the third grid row reads `THE CRAFTSMANSHIP OF A` over `tuxedo` over `TAILORED FOR YOUR POCKET.` `src: Front-end specification, Home para`
- [ ] `C-FE-94` `capability` Editorial tiles lead to collections, never to a product. `src: Front-end specification, Home para`
- [ ] `C-FE-95` `capability` The home bestseller grid is not paged. `src: Front-end specification, Home para`
- [ ] `C-FE-96` `capability` The home page closes with the video tile, the newsletter block, the footer. `src: Front-end specification, Home para`
- [ ] `C-FE-97` `ui` The collection trail is a slim pale grey band with the home glyph, the wedge, the collection name. `src: Front-end specification, Collection page para`
- [ ] `C-FE-98` `capability` The trail wedge beside the collection name opens a list of sibling collections. `src: Front-end specification, Collection page para`
- [ ] `C-FE-99` `capability` The chip strip shows one chip per sibling collection with the collection name. `src: Front-end specification, Collection page para`
- [ ] `C-FE-100` `ui` The chip of the viewed collection carries a thin black border, the rest none. `src: Front-end specification, Collection page para`
- [ ] `C-FE-101` `literal` The last chip reads `View all`, leading to the parent collection. `src: Front-end specification, Collection page para`
- [ ] `C-FE-102` `ui` The collection banner is full bleed with the title drawn in white above a one-line strapline. `src: Front-end specification, Collection page para`
- [ ] `C-FE-103` `literal` The sort list reads `Featured`, `Best selling`, `Price, low to high`, `Price, high to low`, `Newest`. `src: Front-end specification, Sort para`
- [ ] `C-FE-104` `ui` The chosen sort sits on a black row with a small white tick. `src: Front-end specification, Sort para`
- [ ] `C-FE-105` `capability` Choosing a sort reorders the grid in place without a page change. `src: Front-end specification, Sort para`
- [ ] `C-FE-106` `literal` The filter groups read `Size`, `Colour`, `Price`, `Availability` with `In stock only`, `Clear all`, `Apply`. `src: Front-end specification, Sort para`
- [ ] `C-FE-107` `ui` The price filter is a two-handle range across the collection's price span, rounded out to whole dollars. `src: Front-end specification, Sort para`
- [ ] `C-FE-108` `capability` Each chosen filter value clears on its own. `src: Front-end specification, Sort para`
- [ ] `C-FE-109` `literal` The collection address carries the API parameters, as in `/collections/luggage?size=cabin&colour=pink&sort=price-asc&page=2`. `src: Front-end specification, Sort para`
- [ ] `C-FE-110` `ui` The product page places the media stack left of the buy panel. `src: Front-end specification, Product page para`
- [ ] `C-FE-111` `capability` Choosing a colourway replaces the whole media stack. `src: Front-end specification, Product page para`
- [ ] `C-FE-112` `literal` The feature carousel holds eight panels counted like `1/8`, headed `Aviation-grade telescope handle` first. `src: Front-end specification, Product page para`
- [ ] `C-FE-113` `ui` The buy panel stays in view past the media, releasing at the accordions. `src: Front-end specification, Product page para`
- [ ] `C-FE-114` `literal` The buy panel tabs read `Colors`, `Personalise`, `Compare`. `src: Front-end specification, Product page para`
- [ ] `C-FE-115` `ui` The active tab is full ink with a thick underline, the others faded. `src: Front-end specification, Product page para`
- [ ] `C-FE-116` `ui` The colourway row shows square thumbnails, the chosen one with a thin black border. `src: Front-end specification, Product page para`
- [ ] `C-FE-117` `literal` The line `Color:` precedes the chosen colourway name. `src: Front-end specification, Product page para`
- [ ] `C-FE-118` `capability` Size tiles show the viewed product, marked chosen, beside each sibling. `src: Front-end specification, Product page para`
- [ ] `C-FE-119` `literal` Size tile captions read `Cabin`, `Medium`, `Large`, `Save on Sets`. `src: Front-end specification, Product page para`
- [ ] `C-FE-120` `literal` The price row shows `MRP:` before the struck list price. `src: Front-end specification, Product page para`
- [ ] `C-FE-121` `literal` `Incl of all taxes` sits beneath the price row. `src: Front-end specification, Product page para`
- [ ] `C-FE-122` `literal` The instalment line reads `or pay in 4 - <first instalment> today - 0% interest`. `src: Front-end specification, Product page para`
- [ ] `C-FE-123` `capability` The first instalment is the live price over four, rounded up to the cent, as `$44.75` at `$179`. `src: Front-end specification, Product page para`
- [ ] `C-FE-124` `literal` The buy panel buttons read `PERSONALISE` above `ADD TO CART`. `src: Front-end specification, Product page para`
- [ ] `C-FE-125` `capability` Choosing a colourway writes its `sku` into the product page address. `src: Front-end specification, Product page para`
- [ ] `C-FE-126` `capability` A sold-out colourway shows an unavailable `SOLD OUT` button in place of `ADD TO CART`. `src: Front-end specification, Product page para`
- [ ] `C-FE-127` `ui` Adding runs the single overshoot on the cart drawer's item count. `src: Front-end specification, Product page para`
- [ ] `C-FE-128` `literal` The cross-sell block under the pinned pairing heading offers `Packing Cubes (Set of 6)` over `The End of Digging.`, `Travel Pillow` over `Your Window Seat Upgrade.` `src: Front-end specification, Product page para`
- [ ] `C-FE-129` `capability` A cross-sell `ADD` adds the first colourway of that item to the cart. `src: Front-end specification, Product page para`
- [ ] `C-FE-130` `literal` The delivery estimate reads `Expected Delivery in <from> - <to>`, as in `Expected Delivery in 21 Sep - 23 Sep`. `src: Front-end specification, Product page para`
- [ ] `C-FE-131` `literal` The trust chips read `Durable, Lightweight shell`, `30 Day Return Policy`, `3 Years Warranty`. `src: Front-end specification, Product page para`
- [ ] `C-FE-132` `literal` The luggage coverage strip shows `1-Year`, `AIRLINE DAMAGE COVER`, a struck `$49`, a `Details` link. `src: Front-end specification, Coverage para`
- [ ] `C-FE-133` `capability` `Details` opens a dialog rather than a page. `src: Front-end specification, Coverage para`
- [ ] `C-FE-134` `capability` The coverage dialog holds focus, closing with Escape or the drawn cross. `src: Front-end specification, Coverage para`
- [ ] `C-FE-135` `literal` The coverage dialog carries the pinned eyebrow, headline, promise, then `Plan value` over `FREE`, `Validity` over `1 Year`. `src: Front-end specification, Coverage para`
- [ ] `C-FE-136` `literal` The coverage dialog carries a three-step list: `Spot damage at the belt?`, `Tell us within 7 days`, `We repair or replace`. `src: Front-end specification, Coverage para`
- [ ] `C-FE-137` `literal` The coverage dialog carries `Also covered under warranty` with `Shell`, `Wheels & trolley`, `Hardware`. `src: Front-end specification, Coverage para`
- [ ] `C-FE-138` `literal` The coverage dialog lists `Not covered` with `Theft & loss`, `Overpacking`, `Wear & tear`, `Scratches & scuffs`, `Heat, fire & chemicals`, `Commercial use`. `src: Front-end specification, Coverage para`
- [ ] `C-FE-139` `capability` The coverage dialog's `Know More` link leads to `/pages/airline-damage-policy`. `src: Front-end specification, Coverage para`
- [ ] `C-FE-140` `literal` The offer strip reads `The Road Week Sale` over `Up to 50% off` beside `Pay in 4` over `Interest-free on every order`. `src: Front-end specification, Offer strip para`
- [ ] `C-FE-141` `literal` The countdown reads `Sale Extended! Ends in` with days, hours, minutes, seconds separated by colons, labelled `D`, `H`, `M`, `S`. `src: Front-end specification, Offer strip para`
- [ ] `C-FE-142` `capability` The offer strip disappears with the sale. `src: Front-end specification, Offer strip para`
- [ ] `C-FE-143` `capability` The personalise form shows the characters remaining with `front` or `top` placements. `src: Front-end specification, Personalise para`
- [ ] `C-FE-144` `capability` The `PERSONALISE` button opens the personalise tab. `src: Front-end specification, Personalise para`
- [ ] `C-FE-145` `capability` Compare shows `Your Pick` beside a chosen same-category product with `weight_kg`, `capacity_litres`, `dimensions` aligned. `src: Front-end specification, Personalise para`
- [ ] `C-FE-146` `literal` The product accordions read `Dimension`, `Description`, `Warranty & Return`, `More Information`, in that order. `src: Front-end specification, Accordions para`
- [ ] `C-FE-147` `capability` `Dimension` is open on arrival, showing the pinned mass label, `Capacity`, `External dimensions` with values such as `3.23 Kg`, `40L`, `54 x 37.5 x 23.5 cm`. `src: Front-end specification, Accordions para`
- [ ] `C-FE-148` `capability` The `Warranty & Return` drawer names the support address `care@valisette.example.com`. `src: Front-end specification, Accordions para`
- [ ] `C-FE-149` `literal` `More Information` carries `Valisette Travelware Co.`, `Unit 4, Coastline Works`, `118 Canal Street`, `Portland, OR 97209, USA`, `Country of Origin:`, `Vietnam, Mexico`. `src: Front-end specification, Accordions para`
- [ ] `C-FE-150` `literal` The trial banner reads `30` over `days trial`. `src: Front-end specification, Accordions para`
- [ ] `C-FE-151` `literal` The compare module reads `COMPARE` with `Wish to Compare your bag?`, `Your Pick`. `src: Front-end specification, Accordions para`
- [ ] `C-FE-152` `literal` A `Recently Viewed` strip closes the product page. `src: Front-end specification, Accordions para`
- [ ] `C-FE-153` `capability` The cart drawer shows the same lines with the same summary as `/cart`. `src: Front-end specification, Cart para`
- [ ] `C-FE-154` `capability` A cart line shows the picture, title, colourway, size class, personalisation, stepper, line total, remove control. `src: Front-end specification, Cart para`
- [ ] `C-FE-155` `literal` The cart summary reads `Subtotal`, `Discount`, `Delivery` as `Free`, `Total`, then `Checkout`. `src: Front-end specification, Cart para`
- [ ] `C-FE-156` `ui` The cart summary sits right of the lines on a wide screen, below on a phone with a sticky checkout button. `src: Front-end specification, Cart para`
- [ ] `C-FE-157` `capability` A line sold out during checkout shows `SOLD OUT` with unavailable quantity controls. `src: Front-end specification, Cart para`
- [ ] `C-FE-158` `capability` `CONTINUE SHOPPING` leads to `/collections/all`. `src: Front-end specification, Cart para`
- [ ] `C-FE-159` `ui` The empty cart shows a centred heading above the drawn trolley, drawn large. `src: Front-end specification, Cart para`
- [ ] `C-FE-160` `capability` Checkout opens its three sections in turn, the order summary beside them on a wide screen. `src: Front-end specification, Checkout para`
- [ ] `C-FE-161` `literal` The checkout sections read `Contact & delivery`, `Delivery method`, `Payment`. `src: Front-end specification, Checkout para`
- [ ] `C-FE-162` `capability` A signed-in checkout fills in the email with the default address. `src: Front-end specification, Checkout para`
- [ ] `C-FE-163` `literal` Delivery choices read `Standard` with `Free, 3 to 5 days`, `Express` with `$15, 1 to 2 days`. `src: Front-end specification, Checkout para`
- [ ] `C-FE-164` `capability` The checkout total updates as the delivery choice changes. `src: Front-end specification, Checkout para`
- [ ] `C-FE-165` `literal` Payment offers `Pay now` by default or `Bill a corporate account` with a `Corporate account reference` field. `src: Front-end specification, Checkout para`
- [ ] `C-FE-166` `ui` `Place order` shows a busy state, refusing a second press during placement. `src: Front-end specification, Checkout para`
- [ ] `C-FE-167` `capability` Checkout fields reject invalid input next to the field named, keeping what was typed. `src: Front-end specification, Checkout para`
- [ ] `C-FE-168` `capability` A price change, sold-out line or refused corporate account is explained above the button, the cart intact. `src: Front-end specification, Checkout para`
- [ ] `C-FE-169` `ui` The checkout page stays still with plain wording during placement. `src: Front-end specification, Checkout para`
- [ ] `C-FE-170` `literal` The confirmation shows the number, the lines, the address, `Arriving <from> - <to>`. `src: Front-end specification, Checkout para`
- [ ] `C-FE-171` `literal` The store filter placeholder reads `Find a store by city or name`. `src: Front-end specification, Store directory para`
- [ ] `C-FE-172` `capability` The store count reads `14 stores` or `1 store`. `src: Front-end specification, Store directory para`
- [ ] `C-FE-173` `ui` Store rows show the name at heading size, the address in black, the plus mark at the right. `src: Front-end specification, Store directory para`
- [ ] `C-FE-174` `literal` An opened store reads `Opening hours`, `Call the store`, `Directions` with the map pin. `src: Front-end specification, Store directory para`
- [ ] `C-FE-175` `literal` A store filter with no match reads `No store matches that yet.` `src: Front-end specification, Store directory para`
- [ ] `C-FE-176` `capability` The search page offers `SORT BY` without `FILTER BY`. `src: Front-end specification, Search page para`
- [ ] `C-FE-177` `literal` The search header reads `<count> results for "<query>"`. `src: Front-end specification, Search page para`
- [ ] `C-FE-178` `ui` Standing pages share one reading column at a paperback measure with bold headings, no pictures. `src: Front-end specification, Standing pages para`
- [ ] `C-FE-179` `literal` The gift card page shows `Check Gift Card Balance`, `Gift card code`, `CHECK BALANCE`. `src: Front-end specification, Standing pages para`
- [ ] `C-FE-180` `literal` The not-found page shows `The page you asked for is not here any more.` with `Home`, `Shop all`, `Find a store`. `src: Front-end specification, Not-found para`
- [ ] `C-FE-181` `literal` Sign in shows `Login`, `Email` with `Enter your email`, `Password` with `Enter your password`. `src: Front-end specification, Account pages para`
- [ ] `C-FE-182` `literal` Sign in shows `Remember me` with `Forgot password?` on one line above `LOGIN`. `src: Front-end specification, Account pages para`
- [ ] `C-FE-183` `capability` A failed sign-in shows the mismatch message above the button. `src: Front-end specification, Account pages para`
- [ ] `C-FE-184` `literal` Register shows `Create an account`, `Name`, `Email`, `Password`, `Confirm password`, `CREATE ACCOUNT`. `src: Front-end specification, Account pages para`
- [ ] `C-FE-185` `literal` Differing passwords show `The two passwords do not match.`, sending nothing. `src: Front-end specification, Account pages para`
- [ ] `C-FE-186` `literal` Recover shows `Reset your password` with `SEND RESET LINK`. `src: Front-end specification, Account pages para`
- [ ] `C-FE-187` `literal` The reset page shows `Choose a new password`, `SAVE PASSWORD`, then `Your password has been changed.` `src: Front-end specification, Account pages para`
- [ ] `C-FE-188` `literal` `/account` greets the shopper as `Hello, <first name>`, as in `Hello, Aarav`. `src: Front-end specification, Account pages para`
- [ ] `C-FE-189` `capability` `/account` shows the default address above the three latest orders with `Order History`, `Addresses` links. `src: Front-end specification, Account pages para`
- [ ] `C-FE-190` `literal` Order states read `Pending`, `Paid`, `Fulfilled`, `Cancelled`. `src: Front-end specification, Account pages para`
- [ ] `C-FE-191` `literal` The addresses page shows a `Default` marker on one address. `src: Front-end specification, Account pages para`
- [ ] `C-FE-192` `ui` On a phone the rail becomes a floating translucent pill with a menu control, the wordmark, search, cart. `src: Front-end specification, Phone para`
- [ ] `C-FE-193` `ui` On a phone the menu opens a full-height left drawer with a `Back` control, holding focus. `src: Front-end specification, Phone para`
- [ ] `C-FE-194` `ui` On a phone sort with filter move into a dialog opened from a sticky bar. `src: Front-end specification, Phone para`
- [ ] `C-FE-195` `ui` On a phone the product media stacks above a buy panel that no longer stays in view. `src: Front-end specification, Phone para`
- [ ] `C-FE-196` `literal` Each swatch disc is a button with `aria-label` as the colourway name, `aria-pressed` `true` on the chosen disc. `src: Front-end specification, Machine-readable hooks para`
- [ ] `C-FE-197` `literal` Each disc row is a `role="group"` whose `aria-label` is the product title. `src: Front-end specification, Machine-readable hooks para`
- [ ] `C-FE-198` `literal` Each drawn picture has `role="img"` with its alternative text as `aria-label`. `src: Front-end specification, Machine-readable hooks para`
- [ ] `C-FE-199` `literal` The countdown carries `data-ends-at`, each figure in a `data-unit` element valued `d`, `h`, `m`, `s`. `src: Front-end specification, Machine-readable hooks para`
- [ ] `C-FE-200` `ui` Pictures below the first screen are drawn as the pictures approach the window, the hero drawn at once. `src: Front-end specification, Loading para`
- [ ] `C-FE-201` `ui` Every drawn picture reserves its size, so nothing moves when pictures appear. `src: Front-end specification, Loading para`
- [ ] `C-FE-202` `ui` A card title sits on one line, cut with an ellipsis when too long. `src: Front-end specification, Product card para`
- [ ] `C-FE-203` `capability` The whole card cell is one link except the swatch discs. `src: Front-end specification, Product card para`
- [ ] `C-FE-204` `ui` The home editorial tiles sit in the bestseller grid as ordinary cells, the `ELEVATE` tile two cells wide, the tuxedo tile one cell, every rule unbroken. `src: Front-end specification, Home para`
- [ ] `C-FE-205` `ui` Collection grids carry editorial tiles cut in as on the home page. `src: Front-end specification, Collection page para`
- [ ] `C-FE-206` `ui` The `Luggage Collections` strip never scrolls sideways. `src: Front-end specification, Home para`
- [ ] `C-FE-207` `literal` The feature carousel headings continue `Silent wheels`, `Water resistant`, `Thoughtful details`, `3 years warranty`, `30 day trial`, with the pinned personalisation heading. `src: Front-end specification, Product page para`
- [ ] `C-FE-208` `literal` The luggage panel `By Size` column lists `Tech Range`, `Cabin`, `Check-in`, `Check-in Large`, `Trunk`, `Kids Luggage`, `Sets`, `View All`. `src: Front-end specification, Panels para`
- [ ] `C-FE-209` `literal` The luggage panel `By Collection` column lists `Passage`, `Contour`, `Meridian`, `Ridge`, `Coastal`, `Solstice`, `Kids Luggage`. `src: Front-end specification, Panels para`
- [ ] `C-FE-210` `literal` The luggage panel `Highlights` column lists `Best Sellers`, `On Sale`. `src: Front-end specification, Panels para`
- [ ] `C-FE-211` `literal` The bags panel `Collection` column lists `Backpacks`, `Briefcases`, `Duffles`, `Diaper Bags`, `Kids Backpacks`, `View All`. `src: Front-end specification, Panels para`
- [ ] `C-FE-212` `literal` The bags panel `By Use` column lists `Work`, `Travel`, `Diaper & Kids`. `src: Front-end specification, Panels para`
- [ ] `C-FE-213` `literal` The coverage dialog steps carry the three pinned step bodies. `src: Front-end specification, Coverage para`
- [ ] `C-FE-214` `literal` The coverage warranty cards carry `Cracks, dents & colour fades`, `Wobbles, stiff handles, buttons`, `Zippers, handles, feet & logo plate`. `src: Front-end specification, Coverage para`
- [ ] `C-FE-215` `literal` The coverage dialog closes with `Part of valisette Shield, valisette's damage protection programme.` `src: Front-end specification, Coverage para`
- [ ] `C-FE-216` `literal` The coverage dialog carries the pinned promise sentence. `src: Front-end specification, Coverage para`
- [ ] `C-FE-217` `literal` The `Warranty & Return` drawer carries `Not 100% Sure?`, `No strings attached.`, `3 Years worry-free warranty.` beside the pinned refund paragraph. `src: Front-end specification, Accordions para`
- [ ] `C-FE-218` `literal` The trial banner body is the pinned trial sentence. `src: Front-end specification, Accordions para`
- [ ] `C-FE-219` `capability` The cart summary shows `Discount` as a negative amount. `src: Front-end specification, Cart para`
- [ ] `C-FE-220` `capability` The checkout country is fixed to the United States. `src: Front-end specification, Checkout para`
- [ ] `C-FE-221` `capability` `/account/orders` is a table of number, date, total, state columns. `src: Front-end specification, Account pages para`
- [ ] `C-FE-222` `capability` `/account/addresses` lets an address be edited. `src: Front-end specification, Account pages para`
- [ ] `C-FE-223` `capability` `/account/addresses` lets an address be made default. `src: Front-end specification, Account pages para`
- [ ] `C-FE-224` `capability` The cart drawer heading carries the item count. `src: Front-end specification, Cart para; Front-end specification, Product page para`
- [ ] `C-FE-225` `ui` The ticker band keeps a slim inset at its ends. `src: Front-end specification, Ticker para`
- [ ] `C-FE-226` `ui` A hairline separates the rows of the rail actions block. `src: Front-end specification, Rail para`
- [ ] `C-FE-227` `ui` A hairline separates the cart lines. `src: Front-end specification, Cart para`
- [ ] `C-FE-228` `ui` The search overlay input carries a larger, lighter search glyph. `src: Front-end specification, Search overlay para`
- [ ] `C-FE-229` `ui` Every icon is drawn with round joins, round caps. `src: Front-end specification, Iconography para`
- [ ] `C-FE-230` `ui` The buy panel title with the live price sit at section heading size. `src: Front-end specification, Product page para`
- [ ] `C-FE-231` `ui` Each offer strip term is bold over an italic qualifier. `src: Front-end specification, Offer strip para`
- [ ] `C-FE-232` `ui` The `Description` drawer carries four or five bold lead-ins, each followed by a sentence. `src: Front-end specification, Accordions para`
- [ ] `C-FE-233` `ui` Sign in is a centred form on the page ground. `src: Front-end specification, Account pages para`
- [ ] `C-FE-234` `ui` On a phone the recently viewed strip scrolls sideways. `src: Front-end specification, Phone para`
- [ ] `C-FE-235` `ui` On a phone the search page's sort moves into the sticky-bar dialog. `src: Front-end specification, Phone para`
- [ ] `C-FE-236` `capability` An order page shows the lines as bought with colourway, size class, quantity, personalisation, captured prices. `src: Front-end specification, Account pages para`
- [ ] `C-FE-237` `capability` An order page shows the delivery address, the state, the arrival window, the amount charged. `src: Front-end specification, Account pages para`
- [ ] `C-FE-238` `capability` Sign in carries a link to create an account below the `LOGIN` button. `src: Front-end specification, Account pages para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product runs no marketplace. `src: Constraints, bullet 1`
- [ ] `C-CN-02` `constraint` The product offers no wish list. `src: Constraints, bullet 2`
- [ ] `C-CN-03` `constraint` The product offers no conversational assistant. `src: Constraints, bullet 2`
- [ ] `C-CN-04` `constraint` The product collects no card. `src: Constraints, bullet 3`
- [ ] `C-CN-05` `constraint` The product issues no refunds at the provider. `src: Constraints, bullet 3`
- [ ] `C-CN-06` `constraint` The product has one currency, US dollars. `src: Constraints, bullet 4`
- [ ] `C-CN-07` `constraint` The product has one language, English, with no locale switching. `src: Constraints, bullet 4`
- [ ] `C-CN-08` `constraint` The product offers no multi currency pricing. `src: Constraints, bullet 4`
- [ ] `C-CN-09` `constraint` No owner console exists in the browser. `src: Constraints, bullet 7`
- [ ] `C-CN-10` `constraint` No third-party analytics, tag manager, identity drawer, instalment widget, affiliate tracker, font host, content delivery network loads. `src: Constraints, bullet 8`
- [ ] `C-CN-11` `constraint` No page makes a runtime network call to another origin. `src: Constraints, bullet 8`
- [ ] `C-CN-12` `constraint` The product offers no native app, no offline mode. `src: Constraints, bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `contract` `4173` is the container-internal port, both ports read from the environment. `src: Deployment contract, bullet 1`
- [ ] `C-DC-04` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract, bullet 2`
- [ ] `C-DC-05` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract, bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, bullet 4`
- [ ] `C-DC-07` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract, bullet 5`
- [ ] `C-DC-08` `contract` Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root, empty. `src: Deployment contract, bullet 6`
- [ ] `C-DC-09` `contract` The app serves a production build, never a dev server. `src: Deployment contract, bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends, never a child of the shell. `src: Deployment contract, bullet 8`
- [ ] `C-DC-11` `literal` The server binds `0.0.0.0`, never `127.0.0.1` or `localhost`. `src: Deployment contract, bullet 9`
- [ ] `C-DC-12` `contract` The backing services are already running; the app downloads, installs, starts no copy. `src: Deployment contract, bullet 10; Technical requirements, running services para`
- [ ] `C-DC-13` `contract` The app uses only the named providers, with no edge functions. `src: Deployment contract, bullet 11`
- [ ] `C-DC-14` `contract` The app relies on no persistent volumes, fixed container names, custom networks. `src: Deployment contract, bullet 12`
- [ ] `C-DC-15` `contract` API field names are exact. `src: Deployment contract, API shapes para`
- [ ] `C-DC-16` `contract` An invalid or unauthorized call is a client error carrying `error` with a `message`. `src: Deployment contract, API shapes para`
- [ ] `C-DC-17` `contract` A refused call is never a server error, never a silent success. `src: Deployment contract, API shapes para`
- [ ] `C-DC-18` `role` Bearer auth guards `/api/me`, `/api/orders`, `/api/owner`, logout, the cart claim. `src: Deployment contract, auth para`
- [ ] `C-DC-19` `role` The owner endpoints additionally require the `owner` role. `src: Deployment contract, auth para`
- [ ] `C-DC-20` `capability` Every other endpoint answers without a session, a cart endpoint reached by its token. `src: Deployment contract, auth para`
- [ ] `C-DC-21` `constraint` `killbill` is the only place a billing account exists. `src: Deployment contract, No mocks para`
- [ ] `C-DC-22` `constraint` Mailpit is the only place a confirmation email is delivered. `src: Deployment contract, No mocks para`
- [ ] `C-DC-23` `constraint` PostgreSQL is the only place the app's records exist. `src: Deployment contract, No mocks para`
- [ ] `C-DC-24` `constraint` No pretend billing account, self-answered paid status, in-memory order list or stock figure stands in for a provider. `src: Deployment contract, No mocks para`
- [ ] `C-DC-25` `literal` `POST /api/owner/stock-movements` answers with the movement plus the colourway's new `stock`. `src: Deployment contract, API shapes table`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `valisette` | pinned in wordmark | C-OV-02 | Overview, para 1 |
| `deku-demo-pw-2026` | pinned in password | C-RL-33 | User roles, seeded accounts paragraph |
| `owner@example.com` | pinned in seed owner | C-RL-34 | User roles, seeded accounts table row 1 |
| `customer@example.com` | pinned in seed customer | C-RL-35 | User roles, seeded accounts table row 2 |
| `customer2@example.com` | pinned in seed customer2 | C-RL-36 | User roles, seeded accounts table row 3 |
| `POST /api/auth/signup` | pinned in signup fields | C-CF-05 | Core features, Accounts rule 1 |
| `name` | pinned in signup fields | C-CF-05 | Core features, Accounts rule 1 |
| `email` | pinned in signup fields | C-CF-05 | Core features, Accounts rule 1 |
| `password` | pinned in signup fields | C-CF-05 | Core features, Accounts rule 1 |
| `customer` | pinned in signup fields | C-CF-05 | Core features, Accounts rule 1 |
| `access_token` | pinned in signup token | C-CF-06 | Core features, Accounts rule 1 |
| `POST /api/auth/login` | pinned in login fields | C-CF-11 | Core features, Accounts rule 2 |
| `remember` | pinned in login fields | C-CF-11 | Core features, Accounts rule 2 |
| `role` | pinned in login returns | C-CF-12 | Core features, Accounts rule 2 |
| `expires_at` | pinned in login returns | C-CF-12 | Core features, Accounts rule 2 |
| `POST /api/auth/recover` | pinned in recover message | C-CF-23 | Core features, Accounts rule 7 |
| `If we know that address, a reset link is on its way.` | pinned in recover message | C-CF-23 | Core features, Accounts rule 7 |
| `Reset your valisette password` | pinned in recover email | C-CF-25 | Core features, Accounts rule 7 |
| `<APP_PUBLIC_URL>/account/reset/<token>` | pinned in recover link | C-CF-26 | Core features, Accounts rule 7 |
| `GET /api/me` | pinned in me | C-CF-34 | Core features, Accounts rule 9 |
| `sku` | pinned in sku scheme | C-CF-45 | Core features, Catalogue para before the product table |
| `PSG-CAB-OLV` | pinned in sku scheme | C-CF-45 | Core features, Catalogue para before the product table |
| `usd` | pinned in cents | C-CF-46 | Core features, Catalogue para before the product table |
| `17900` | pinned in cents | C-CF-46 | Core features, Catalogue para before the product table |
| `$179` | pinned in cents | C-CF-46 | Core features, Catalogue para before the product table |
| `MRD-CAB-STB` | pinned in stb price | C-CF-52 | Core features, Catalogue exceptions |
| `19900` | pinned in stb price | C-CF-52 | Core features, Catalogue exceptions |
| `29900` | pinned in stb price | C-CF-52 | Core features, Catalogue exceptions |
| `PSG-CAB-CSP` | pinned in stock psg csp | C-CF-53 | Core features, Catalogue exceptions |
| `VLT-CSE-NSH` | pinned in stock vlt nsh | C-CF-54 | Core features, Catalogue exceptions |
| `CTR-CAB-CSP` | pinned in stock ctr csp | C-CF-55 | Core features, Catalogue exceptions |
| `RDG-TRL-SFL` | pinned in stock rdg sfl | C-CF-56 | Core features, Catalogue exceptions |
| `cabin` | pinned in size values | C-CF-57 | Core features, Catalogue para after the exceptions |
| `check-in` | pinned in size values | C-CF-57 | Core features, Catalogue para after the exceptions |
| `check-in-large` | pinned in size values | C-CF-57 | Core features, Catalogue para after the exceptions |
| `trunk` | pinned in size values | C-CF-57 | Core features, Catalogue para after the exceptions |
| `kids` | pinned in size values | C-CF-57 | Core features, Catalogue para after the exceptions |
| `set` | pinned in size values | C-CF-57 | Core features, Catalogue para after the exceptions |
| `backpack` | pinned in type values | C-CF-58 | Core features, Catalogue para after the exceptions |
| `briefcase` | pinned in type values | C-CF-58 | Core features, Catalogue para after the exceptions |
| `duffle` | pinned in type values | C-CF-58 | Core features, Catalogue para after the exceptions |
| `diaper-bag` | pinned in type values | C-CF-58 | Core features, Catalogue para after the exceptions |
| `kids-backpack` | pinned in type values | C-CF-58 | Core features, Catalogue para after the exceptions |
| `work` | pinned in use values | C-CF-59 | Core features, Catalogue para after the exceptions |
| `travel` | pinned in use values | C-CF-59 | Core features, Catalogue para after the exceptions |
| `diaper-and-kids` | pinned in use values | C-CF-59 | Core features, Catalogue para after the exceptions |
| `tech` | pinned in tag values | C-CF-60 | Core features, Catalogue para after the exceptions |
| `clearance` | pinned in tag values | C-CF-60 | Core features, Catalogue para after the exceptions |
| `hot` | pinned in badge values | C-CF-61 | Core features, Catalogue para after the exceptions |
| `must-have` | pinned in badge values | C-CF-61 | Core features, Catalogue para after the exceptions |
| `GET /api/products/{handle}` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `handle` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `title` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `category` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `line` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `size_class` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `bag_type` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `badge` | pinned in product fields | C-CF-62 | Core features, Catalogue rule 1 |
| `personalisable` | pinned in product fields2 | C-CF-63 | Core features, Catalogue rule 1 |
| `units_sold` | pinned in product fields2 | C-CF-63 | Core features, Catalogue rule 1 |
| `weight_kg` | pinned in product fields2 | C-CF-63 | Core features, Catalogue rule 1 |
| `capacity_litres` | pinned in product fields2 | C-CF-63 | Core features, Catalogue rule 1 |
| `dimensions` | pinned in product fields2 | C-CF-63 | Core features, Catalogue rule 1 |
| `description` | pinned in product fields2 | C-CF-63 | Core features, Catalogue rule 1 |
| `colourway` | pinned in variant fields | C-CF-64 | Core features, Catalogue rule 1 |
| `colour_family` | pinned in variant fields | C-CF-64 | Core features, Catalogue rule 1 |
| `swatch` | pinned in variant fields | C-CF-64 | Core features, Catalogue rule 1 |
| `price` | pinned in variant fields | C-CF-64 | Core features, Catalogue rule 1 |
| `list_price` | pinned in variant fields | C-CF-64 | Core features, Catalogue rule 1 |
| `discount_percent` | pinned in variant fields2 | C-CF-65 | Core features, Catalogue rule 1 |
| `on_sale` | pinned in variant fields2 | C-CF-65 | Core features, Catalogue rule 1 |
| `stock` | pinned in variant fields2 | C-CF-65 | Core features, Catalogue rule 1 |
| `in_stock` | pinned in variant fields2 | C-CF-65 | Core features, Catalogue rule 1 |
| `media` | pinned in variant fields2 | C-CF-65 | Core features, Catalogue rule 1 |
| `40` | pinned in discount 40 | C-CF-70 | Core features, Catalogue rule 2 |
| `33` | pinned in discount 33 | C-CF-71 | Core features, Catalogue rule 2 |
| `59900` | pinned in discount 45 | C-CF-72 | Core features, Catalogue rule 2 |
| `109900` | pinned in discount 45 | C-CF-72 | Core features, Catalogue rule 2 |
| `45` | pinned in discount 45 | C-CF-72 | Core features, Catalogue rule 2 |
| `0` | pinned in discount 0 | C-CF-73 | Core features, Catalogue rule 2 |
| `Passage Luggage - Cabin` | pinned in badge psg | C-CF-77 | Core features, Catalogue rule 3 |
| `sold-out` | pinned in badge psg | C-CF-77 | Core features, Catalogue rule 3 |
| `Corner Shop Pink` | pinned in badge psg | C-CF-77 | Core features, Catalogue rule 3 |
| `Vault Card Case` | pinned in badge vlt | C-CF-78 | Core features, Catalogue rule 3 |
| `Night Shift` | pinned in badge vlt | C-CF-78 | Core features, Catalogue rule 3 |
| `3.23` | pinned in dims cabin | C-CF-83 | Core features, Catalogue rule 6 table row 1 |
| `54 x 37.5 x 23.5 cm` | pinned in dims cabin | C-CF-83 | Core features, Catalogue rule 6 table row 1 |
| `3.95` | pinned in dims checkin | C-CF-84 | Core features, Catalogue rule 6 table row 2 |
| `68` | pinned in dims checkin | C-CF-84 | Core features, Catalogue rule 6 table row 2 |
| `66 x 44 x 27 cm` | pinned in dims checkin | C-CF-84 | Core features, Catalogue rule 6 table row 2 |
| `4.70` | pinned in dims large | C-CF-85 | Core features, Catalogue rule 6 table row 3 |
| `98` | pinned in dims large | C-CF-85 | Core features, Catalogue rule 6 table row 3 |
| `76 x 50 x 30 cm` | pinned in dims large | C-CF-85 | Core features, Catalogue rule 6 table row 3 |
| `5.10` | pinned in dims trunk | C-CF-86 | Core features, Catalogue rule 6 table row 4 |
| `90` | pinned in dims trunk | C-CF-86 | Core features, Catalogue rule 6 table row 4 |
| `70 x 45 x 34 cm` | pinned in dims trunk | C-CF-86 | Core features, Catalogue rule 6 table row 4 |
| `2.10` | pinned in dims kids | C-CF-87 | Core features, Catalogue rule 6 table row 5 |
| `22` | pinned in dims kids | C-CF-87 | Core features, Catalogue rule 6 table row 5 |
| `45 x 32 x 20 cm` | pinned in dims kids | C-CF-87 | Core features, Catalogue rule 6 table row 5 |
| `11.88` | pinned in dims set3 | C-CF-88 | Core features, Catalogue rule 6 table row 6 |
| `206` | pinned in dims set3 | C-CF-88 | Core features, Catalogue rule 6 table row 6 |
| `4.20` | pinned in dims set2 | C-CF-89 | Core features, Catalogue rule 6 table row 7 |
| `44` | pinned in dims set2 | C-CF-89 | Core features, Catalogue rule 6 table row 7 |
| `45 x 32 x 20 cm, 45 x 32 x 20 cm` | pinned in dims set2 | C-CF-89 | Core features, Catalogue rule 6 table row 7 |
| `alt` | pinned in media alt | C-CF-91 | Core features, Catalogue rule 7 |
| `Passage Luggage - Cabin in Field Olive, front view` | pinned in media alt | C-CF-91 | Core features, Catalogue rule 7 |
| `GET /api/collections` | pinned in coll list | C-CF-104 | Core features, Collections rule 1 |
| `kind` | pinned in coll list | C-CF-104 | Core features, Collections rule 1 |
| `product_count` | pinned in coll list | C-CF-104 | Core features, Collections rule 1 |
| `GET /api/collections/{handle}` | pinned in coll detail | C-CF-105 | Core features, Collections rule 2 |
| `strapline` | pinned in coll detail | C-CF-105 | Core features, Collections rule 2 |
| `banner_title` | pinned in coll detail | C-CF-105 | Core features, Collections rule 2 |
| `siblings` | pinned in coll detail | C-CF-105 | Core features, Collections rule 2 |
| `luggage` | pinned in coll parent | C-CF-107 | Core features, Collections rule 2 |
| `size` | pinned in coll parent | C-CF-107 | Core features, Collections rule 2 |
| `backpacks-and-briefcases` | pinned in coll parent | C-CF-107 | Core features, Collections rule 2 |
| `type` | pinned in coll parent | C-CF-107 | Core features, Collections rule 2 |
| `use` | pinned in coll parent | C-CF-107 | Core features, Collections rule 2 |
| `all` | pinned in coll parent | C-CF-107 | Core features, Collections rule 2 |
| `highlight` | pinned in coll parent | C-CF-107 | Core features, Collections rule 2 |
| `The <name> Series` | pinned in banner line | C-CF-109 | Core features, Collections rule 2 |
| `The Meridian Series` | pinned in banner line | C-CF-109 | Core features, Collections rule 2 |
| `products` | pinned in coll products fields | C-CF-112 | Core features, Collections rule 3 |
| `total` | pinned in coll products fields | C-CF-112 | Core features, Collections rule 3 |
| `page` | pinned in coll products fields | C-CF-112 | Core features, Collections rule 3 |
| `page_size` | pinned in coll products fields | C-CF-112 | Core features, Collections rule 3 |
| `24` | pinned in page size | C-CF-113 | Core features, Collections rule 3 |
| `lowest_price` | pinned in card fields | C-CF-115 | Core features, Collections rule 3 |
| `colourways` | pinned in card fields | C-CF-115 | Core features, Collections rule 3 |
| `more_colourways` | pinned in card fields | C-CF-115 | Core features, Collections rule 3 |
| `sort` | pinned in sort values | C-CF-118 | Core features, Collections rule 4 |
| `featured` | pinned in sort values | C-CF-118 | Core features, Collections rule 4 |
| `best-selling` | pinned in sort values | C-CF-118 | Core features, Collections rule 4 |
| `price-asc` | pinned in sort values | C-CF-118 | Core features, Collections rule 4 |
| `price-desc` | pinned in sort values | C-CF-118 | Core features, Collections rule 4 |
| `newest` | pinned in sort values | C-CF-118 | Core features, Collections rule 4 |
| `/api/collections/luggage/products` | pinned in ex luggage total | C-CF-133 | Core features, Collections rule 7 |
| `20` | pinned in ex luggage total | C-CF-133 | Core features, Collections rule 7 |
| `/api/collections/on-sale/products?page=2` | pinned in ex on sale page2 | C-CF-134 | Core features, Collections rule 7 |
| `34` | pinned in ex on sale page2 | C-CF-134 | Core features, Collections rule 7 |
| `Contour Luggage - Cabin` | pinned in ex cabin pink | C-CF-135 | Core features, Collections rule 7 |
| `Passage Luggage - Set of 3` | pinned in ex price desc | C-CF-136 | Core features, Collections rule 7 |
| `Passage Backpack - 30L` | pinned in ex best selling | C-CF-137 | Core features, Collections rule 7 |
| `4000` | pinned in ex wallets range | C-CF-138 | Core features, Collections rule 7 |
| `5000` | pinned in ex wallets range | C-CF-138 | Core features, Collections rule 7 |
| `Meridian Luggage - Cabin` | pinned in ex more meridian | C-CF-139 | Core features, Collections rule 7 |
| `3` | pinned in ex more meridian | C-CF-139 | Core features, Collections rule 7 |
| `2` | pinned in ex more passage | C-CF-140 | Core features, Collections rule 7 |
| `Road Week` | pinned in sale name | C-CF-144 | Core features, Sale rule 1 |
| `GET /api/sale` | pinned in sale fields | C-CF-145 | Core features, Sale rule 1 |
| `ends_at` | pinned in sale fields | C-CF-145 | Core features, Sale rule 1 |
| `active` | pinned in sale fields | C-CF-145 | Core features, Sale rule 1 |
| `server_time` | pinned in sale fields | C-CF-145 | Core features, Sale rule 1 |
| `PATCH /api/owner/sale` | pinned in sale patch | C-CF-155 | Core features, Sale rule 3 |
| `POST /api/carts` | pinned in cart create | C-CF-161 | Core features, Cart rule 1 |
| `token` | pinned in cart create | C-CF-161 | Core features, Cart rule 1 |
| `POST /api/carts/{token}/claim` | pinned in cart claim | C-CF-165 | Core features, Cart rule 1 |
| `GET /api/me/cart` | pinned in me cart | C-CF-167 | Core features, Cart rule 1 |
| `GET /api/carts/{token}` | pinned in cart fields | C-CF-169 | Core features, Cart rule 2 |
| `lines` | pinned in cart fields | C-CF-169 | Core features, Cart rule 2 |
| `item_count` | pinned in cart fields | C-CF-169 | Core features, Cart rule 2 |
| `subtotal` | pinned in cart fields | C-CF-169 | Core features, Cart rule 2 |
| `discount` | pinned in cart fields | C-CF-169 | Core features, Cart rule 2 |
| `delivery` | pinned in cart fields | C-CF-169 | Core features, Cart rule 2 |
| `currency` | pinned in cart fields | C-CF-169 | Core features, Cart rule 2 |
| `POST /api/carts/{token}/lines` | pinned in line add | C-CF-171 | Core features, Cart rule 3 |
| `quantity` | pinned in line add | C-CF-171 | Core features, Cart rule 3 |
| `properties` | pinned in line add | C-CF-171 | Core features, Cart rule 3 |
| `id` | pinned in line fields | C-CF-176 | Core features, Cart rule 4 |
| `product_title` | pinned in line fields | C-CF-176 | Core features, Cart rule 4 |
| `unit_price` | pinned in line fields2 | C-CF-177 | Core features, Cart rule 4 |
| `line_total` | pinned in line fields2 | C-CF-177 | Core features, Cart rule 4 |
| `line_saving` | pinned in line fields2 | C-CF-177 | Core features, Cart rule 4 |
| `sold_out` | pinned in line fields2 | C-CF-177 | Core features, Cart rule 4 |
| `error` | pinned in insufficient | C-CF-187 | Core features, Cart rule 6 |
| `insufficient_stock` | pinned in insufficient | C-CF-187 | Core features, Cart rule 6 |
| `available` | pinned in insufficient | C-CF-187 | Core features, Cart rule 6 |
| `Only <available> left in stock.` | pinned in insufficient msg | C-CF-188 | Core features, Cart rule 6 |
| `Only 2 left in stock.` | pinned in insufficient msg | C-CF-188 | Core features, Cart rule 6 |
| `Sorry, the last one just sold out.` | pinned in sold out msg | C-CF-190 | Core features, Cart rule 6 |
| `PATCH /api/carts/{token}/lines/{id}` | pinned in line patch | C-CF-191 | Core features, Cart rule 7 |
| `DELETE /api/carts/{token}/lines/{id}` | pinned in line delete | C-CF-192 | Core features, Cart rule 7 |
| `initials` | pinned in pers props | C-CF-196 | Core features, Personalisation rule 1 |
| `placement` | pinned in pers props | C-CF-196 | Core features, Personalisation rule 1 |
| `front` | pinned in pers placement | C-CF-198 | Core features, Personalisation rule 1 |
| `top` | pinned in pers placement | C-CF-198 | Core features, Personalisation rule 1 |
| `Initials: <initials>, <placement>` | pinned in pers display | C-CF-204 | Core features, Personalisation rule 2 |
| `Initials: AM, front` | pinned in pers display | C-CF-204 | Core features, Personalisation rule 2 |
| `Design not created yet. Start customising` | pinned in pers empty | C-CF-206 | Core features, Personalisation rule 3 |
| `POST /api/checkout` | pinned in co fields | C-CF-207 | Core features, Checkout rule 1 |
| `cart_token` | pinned in co fields | C-CF-207 | Core features, Checkout rule 1 |
| `checkout_key` | pinned in co fields | C-CF-207 | Core features, Checkout rule 1 |
| `address` | pinned in co fields | C-CF-207 | Core features, Checkout rule 1 |
| `delivery_method` | pinned in co fields | C-CF-207 | Core features, Checkout rule 1 |
| `corporate_account` | pinned in co fields | C-CF-207 | Core features, Checkout rule 1 |
| `line1` | pinned in co address | C-CF-209 | Core features, Checkout rule 1 |
| `line2` | pinned in co address | C-CF-209 | Core features, Checkout rule 1 |
| `city` | pinned in co address | C-CF-209 | Core features, Checkout rule 1 |
| `region` | pinned in co address | C-CF-209 | Core features, Checkout rule 1 |
| `postcode` | pinned in co address | C-CF-209 | Core features, Checkout rule 1 |
| `country` | pinned in co address | C-CF-209 | Core features, Checkout rule 1 |
| `phone` | pinned in co address | C-CF-209 | Core features, Checkout rule 1 |
| `cart_empty` | pinned in co empty | C-CF-213 | Core features, Checkout rule 2 |
| `standard` | pinned in del standard | C-CF-219 | Core features, Checkout rule 3 |
| `express` | pinned in del express | C-CF-220 | Core features, Checkout rule 3 |
| `1500` | pinned in del express | C-CF-220 | Core features, Checkout rule 3 |
| `GET /api/delivery-estimate?method=standard` | pinned in del endpoint | C-CF-221 | Core features, Checkout rule 3 |
| `method` | pinned in del endpoint | C-CF-221 | Core features, Checkout rule 3 |
| `cost` | pinned in del endpoint | C-CF-221 | Core features, Checkout rule 3 |
| `from` | pinned in del endpoint | C-CF-221 | Core features, Checkout rule 3 |
| `to` | pinned in del endpoint | C-CF-221 | Core features, Checkout rule 3 |
| `price_changed` | pinned in price changed | C-CF-223 | Core features, Checkout rule 4 |
| `out_of_stock` | pinned in out of stock | C-CF-229 | Core features, Checkout rule 5 |
| `VS-` | pinned in order number | C-CF-232 | Core features, Checkout rule 6 |
| `VS-100004` | pinned in order number | C-CF-232 | Core features, Checkout rule 6 |
| `externalKey` | pinned in kb key | C-CF-234 | Core features, Checkout rule 6 |
| `valisette-<number>` | pinned in kb key | C-CF-234 | Core features, Checkout rule 6 |
| `valisette-VS-100004` | pinned in kb key | C-CF-234 | Core features, Checkout rule 6 |
| `billing_account` | pinned in kb billing field | C-CF-237 | Core features, Checkout rule 6 |
| `billing_account_unknown` | pinned in corp unknown | C-CF-241 | Core features, Checkout rule 7 |
| `We could not find that corporate account.` | pinned in corp unknown msg | C-CF-242 | Core features, Checkout rule 7 |
| `USD` | pinned in corp currency | C-CF-243 | Core features, Checkout rule 7 |
| `billing_account_currency` | pinned in corp currency | C-CF-243 | Core features, Checkout rule 7 |
| `That corporate account is billed in <currency>. Corporate orders are billed in USD.` | pinned in corp currency msg | C-CF-244 | Core features, Checkout rule 7 |
| `orbit-acme` | pinned in corp acme msg | C-CF-245 | Core features, Checkout rule 7 |
| `That corporate account is billed in EUR. Corporate orders are billed in USD.` | pinned in corp acme msg | C-CF-245 | Core features, Checkout rule 7 |
| `orbit-northwind` | pinned in corp northwind | C-CF-247 | Core features, Checkout rule 7 |
| `EUR` | pinned in corp acme | C-CF-248 | Core features, Checkout rule 7 |
| `orbit-amelia` | pinned in corp amelia | C-CF-249 | Core features, Checkout rule 7 |
| `number` | pinned in order answer | C-CF-267 | Core features, Checkout rule 11 |
| `state` | pinned in order answer | C-CF-267 | Core features, Checkout rule 11 |
| `delivery_from` | pinned in order answer | C-CF-267 | Core features, Checkout rule 11 |
| `delivery_to` | pinned in order answer | C-CF-267 | Core features, Checkout rule 11 |
| `placed_at` | pinned in order answer2 | C-CF-268 | Core features, Checkout rule 11 |
| `MNI-SLG-NSH` | pinned in ex row1 | C-CF-270 | Core features, Checkout rule 12 table row 1 |
| `27700` | pinned in ex row1 | C-CF-270 | Core features, Checkout rule 12 table row 1 |
| `45700` | pinned in ex row1 | C-CF-270 | Core features, Checkout rule 12 table row 1 |
| `18000` | pinned in ex row1 | C-CF-270 | Core features, Checkout rule 12 table row 1 |
| `29200` | pinned in ex row2 | C-CF-271 | Core features, Checkout rule 12 table row 2 |
| `PCK-CUB-HTG` | pinned in ex row3 | C-CF-272 | Core features, Checkout rule 12 table row 3 |
| `22800` | pinned in ex row3 | C-CF-272 | Core features, Checkout rule 12 table row 3 |
| `32800` | pinned in ex row3 | C-CF-272 | Core features, Checkout rule 12 table row 3 |
| `10000` | pinned in ex row3 | C-CF-272 | Core features, Checkout rule 12 table row 3 |
| `PSG-SET-NSH` | pinned in ex row4 | C-CF-273 | Core features, Checkout rule 12 table row 4 |
| `$277` | pinned in money format | C-CF-274 | Core features, Checkout rule 12 |
| `$1,099` | pinned in money format | C-CF-274 | Core features, Checkout rule 12 |
| `$44.75` | pinned in money format | C-CF-274 | Core features, Checkout rule 12 |
| `orders@valisette.example.com` | pinned in mail from | C-CF-277 | Core features, Confirmation rule 1 |
| `Your valisette order <number> is confirmed` | pinned in mail subject | C-CF-278 | Core features, Confirmation rule 1 |
| `Order <number>, total charged <amount>.` | pinned in mail opening | C-CF-279 | Core features, Confirmation rule 2 |
| `Order VS-100004, total charged $277.` | pinned in mail opening | C-CF-279 | Core features, Confirmation rule 2 |
| `GET /api/me/orders` | pinned in my orders | C-CF-284 | Core features, Orders rule 1 |
| `pending` | pinned in order states | C-CF-292 | Core features, Orders rule 4 |
| `paid` | pinned in order states | C-CF-292 | Core features, Orders rule 4 |
| `fulfilled` | pinned in order states | C-CF-292 | Core features, Orders rule 4 |
| `cancelled` | pinned in order states | C-CF-292 | Core features, Orders rule 4 |
| `GET /api/owner/orders` | pinned in owner orders | C-CF-295 | Core features, Orders rule 5 |
| `POST /api/owner/orders/{number}/fulfil` | pinned in fulfil | C-CF-296 | Core features, Orders rule 5 |
| `POST /api/owner/orders/{number}/cancel` | pinned in cancel | C-CF-297 | Core features, Orders rule 5 |
| `GET /api/me/addresses` | pinned in addr list | C-CF-302 | Core features, Orders rule 6 |
| `POST /api/me/addresses` | pinned in addr save | C-CF-303 | Core features, Orders rule 6 |
| `PATCH /api/me/addresses/{id}` | pinned in addr patch | C-CF-304 | Core features, Orders rule 6 |
| `DELETE /api/me/addresses/{id}` | pinned in addr delete | C-CF-305 | Core features, Orders rule 6 |
| `delta` | pinned in mv fields | C-CF-312 | Core features, Stock rule 1 |
| `order_number` | pinned in mv fields | C-CF-312 | Core features, Stock rule 1 |
| `note` | pinned in mv fields | C-CF-312 | Core features, Stock rule 1 |
| `created_at` | pinned in mv fields | C-CF-312 | Core features, Stock rule 1 |
| `sale` | pinned in mv kinds | C-CF-313 | Core features, Stock rule 1 |
| `restock` | pinned in mv kinds | C-CF-313 | Core features, Stock rule 1 |
| `cancellation` | pinned in mv kinds | C-CF-313 | Core features, Stock rule 1 |
| `adjustment` | pinned in mv kinds | C-CF-313 | Core features, Stock rule 1 |
| `POST /api/owner/stock-movements` | pinned in mv post | C-CF-318 | Core features, Stock rule 2 |
| `GET /api/owner/stock-movements?sku=<sku>` | pinned in mv list | C-CF-323 | Core features, Stock rule 3 |
| `PATCH /api/owner/products/{handle}` | pinned in owner product patch | C-CF-325 | Core features, Owner edits rule 1 |
| `published` | pinned in owner product patch | C-CF-325 | Core features, Owner edits rule 1 |
| `PATCH /api/owner/variants/{sku}` | pinned in owner variant patch | C-CF-327 | Core features, Owner edits rule 2 |
| `GET /api/search?q=<text>` | pinned in search fields | C-CF-333 | Core features, Search rule 1 |
| `query` | pinned in search fields | C-CF-333 | Core features, Search rule 1 |
| `count` | pinned in search fields | C-CF-333 | Core features, Search rule 1 |
| `olive` | pinned in search olive | C-CF-338 | Core features, Search rule 1 |
| `Field Olive` | pinned in search olive | C-CF-338 | Core features, Search rule 1 |
| `coastal` | pinned in search coastal | C-CF-341 | Core features, Search rule 2 |
| `Coastal` | pinned in search coastal | C-CF-341 | Core features, Search rule 2 |
| `Ridge Trunk - Medium` | pinned in search coastal | C-CF-341 | Core features, Search rule 2 |
| `Ridge Cabin Pro` | pinned in search coastal | C-CF-341 | Core features, Search rule 2 |
| `meridian` | pinned in search meridian | C-CF-342 | Core features, Search rule 2 |
| `Overnight Backpack - 23L` | pinned in search meridian | C-CF-342 | Core features, Search rule 2 |
| `GET /api/stores` | pinned in stores fields | C-CF-351 | Core features, Store directory rule 1 |
| `hours` | pinned in stores fields | C-CF-351 | Core features, Store directory rule 1 |
| `port` | pinned in stores port | C-CF-354 | Core features, Store directory rule 1 |
| `new` | pinned in stores new | C-CF-355 | Core features, Store directory rule 1 |
| `Newbury Street` | pinned in stores new | C-CF-355 | Core features, Store directory rule 1 |
| `Hudson Yards` | pinned in stores new | C-CF-355 | Core features, Store directory rule 1 |
| `SoHo` | pinned in stores new | C-CF-355 | Core features, Store directory rule 1 |
| `Thank you for subscribing!` | pinned in news msg | C-CF-362 | Core features, Newsletter rule 1 |
| `POST /api/gift-cards/balance` | pinned in gift answer | C-CF-365 | Core features, Newsletter rule 2 |
| `balance` | pinned in gift answer | C-CF-365 | Core features, Newsletter rule 2 |
| `VSGC-2026-AMBER` | pinned in gift amber | C-CF-366 | Core features, Newsletter rule 2 |
| `That code is not recognised.` | pinned in gift msg | C-CF-368 | Core features, Newsletter rule 2 |
| `/pages/<handle>` | pinned in pages ten | C-CF-370 | Core features, Standing pages rule 1 |
| `GET /api/pages/{handle}` | pinned in pages api | C-CF-371 | Core features, Standing pages rule 1 |
| `body` | pinned in pages api | C-CF-371 | Core features, Standing pages rule 1 |
| `That page has moved on without us.` | pinned in nf heading | C-CF-382 | Core features, Standing pages rule 3 |
| `/` | pinned in nf links | C-CF-384 | Core features, Standing pages rule 3 |
| `/collections/all` | pinned in nf links | C-CF-384 | Core features, Standing pages rule 3 |
| `/pages/stores` | pinned in nf links | C-CF-384 | Core features, Standing pages rule 3 |
| `/api` | pinned in nf api | C-CF-387 | Core features, Standing pages rule 4 |
| `not_found` | pinned in nf api | C-CF-387 | Core features, Standing pages rule 4 |
| `Thank you. Your order is confirmed.` | pinned in confirmation | C-UF-27 | User flow, Journey 2 |
| `sidebar-nav` | pinned in sidebar | C-UX-36 | UI/UX notes, Shape para |
| `4.5:1` | pinned in contrast body | C-UX-68 | UI/UX notes, Accessibility para |
| `3:1` | pinned in contrast large | C-UX-69 | UI/UX notes, Accessibility para |
| `{"name", "externalKey", "email", "currency", "country"}` | pinned in kb body | C-TR-13 | Technical requirements, bullet 4 |
| `GET /api/health` | pinned in health | C-TR-18 | Technical requirements, bullet 7 |
| `200` | pinned in health | C-TR-18 | Technical requirements, bullet 7 |
| `{"status": "ok"}` | pinned in health | C-TR-18 | Technical requirements, bullet 7 |
| `killbill` | pinned in health | C-TR-18 | Technical requirements, bullet 7 |
| `Z` | pinned in utc | C-TR-26 | Technical requirements, bullet 11 |
| `YYYY-MM-DD` | pinned in utc | C-TR-26 | Technical requirements, bullet 11 |
| `image` | pinned in media kind | C-DM-14 | Data model, media |
| `video` | pinned in media kind | C-DM-14 | Data model, media |
| `VSGC-2025-LAPSED` | pinned in gift lapsed | C-DM-41 | Data model, Seed data bullet 4 |
| `2500` | pinned in gift lapsed | C-DM-41 | Data model, Seed data bullet 4 |
| `2025-12-31` | pinned in gift lapsed | C-DM-41 | Data model, Seed data bullet 4 |
| `Road Week - Up to 50% off` | pinned in ticker items | C-FE-04 | Front-end specification, Ticker para |
| `LIVE NOW` | pinned in ticker items | C-FE-04 | Front-end specification, Ticker para |
| `Luggage` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `Backpacks & Briefcases` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `Totes` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `Slings & Crossbodies` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `Accessories` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `Wallets` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `Gift Card` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `Clearance Sale` | pinned in rail categories | C-FE-12 | Front-end specification, Rail para |
| `By Size` | pinned in panel luggage | C-FE-23 | Front-end specification, Panels para |
| `By Collection` | pinned in panel luggage | C-FE-23 | Front-end specification, Panels para |
| `Highlights` | pinned in panel luggage | C-FE-23 | Front-end specification, Panels para |
| `Passage Collection` | pinned in panel luggage cards | C-FE-24 | Front-end specification, Panels para |
| `Meridian Collection` | pinned in panel luggage cards | C-FE-24 | Front-end specification, Panels para |
| `Collection` | pinned in panel bags | C-FE-25 | Front-end specification, Panels para |
| `By Use` | pinned in panel bags | C-FE-25 | Front-end specification, Panels para |
| `Recent Searches` | pinned in overlay blocks | C-FE-37 | Front-end specification, Search overlay para |
| `Clear` | pinned in overlay blocks | C-FE-37 | Front-end specification, Search overlay para |
| `Recently Viewed Products` | pinned in overlay blocks | C-FE-37 | Front-end specification, Search overlay para |
| `Warm Hugs, valisette.` | pinned in newsletter heading | C-FE-39 | Front-end specification, Footer para |
| `Enter Email Address` | pinned in newsletter field | C-FE-40 | Front-end specification, Footer para |
| `Need assistance?` | pinned in footer contact | C-FE-45 | Front-end specification, Footer para |
| `For Gifting & Corporate orders` | pinned in footer gifting | C-FE-46 | Front-end specification, Footer para |
| `FAQ` | pinned in footer col1 | C-FE-47 | Front-end specification, Footer para |
| `Claim My Warranty` | pinned in footer col1 | C-FE-47 | Front-end specification, Footer para |
| `Terms & Conditions` | pinned in footer col1 | C-FE-47 | Front-end specification, Footer para |
| `Airline Damage Policy` | pinned in footer col1 | C-FE-47 | Front-end specification, Footer para |
| `Blogs` | pinned in footer col1 | C-FE-47 | Front-end specification, Footer para |
| `Claim 30 Day Trial` | pinned in footer col2 | C-FE-48 | Front-end specification, Footer para |
| `Return & Refund Policy` | pinned in footer col2 | C-FE-48 | Front-end specification, Footer para |
| `Privacy Policy` | pinned in footer col2 | C-FE-48 | Front-end specification, Footer para |
| `Check Gift Card Balance` | pinned in footer col2 | C-FE-48 | Front-end specification, Footer para |
| `#KeepMoving` | pinned in footer essay | C-FE-49 | Front-end specification, Footer para |
| `/products/<handle>?sku=<sku>` | pinned in card link | C-FE-69 | Front-end specification, Product card para |
| `Luggage Collections` | pinned in home collections | C-FE-86 | Front-end specification, Home para |
| `Coastal Collection` | pinned in home collections | C-FE-86 | Front-end specification, Home para |
| `Categories` | pinned in home categories | C-FE-87 | Front-end specification, Home para |
| `Bags & Backpacks` | pinned in home categories | C-FE-87 | Front-end specification, Home para |
| `Totes & Handbags` | pinned in home categories | C-FE-87 | Front-end specification, Home para |
| `Travel Accessories` | pinned in home categories | C-FE-87 | Front-end specification, Home para |
| `Bestsellers` | pinned in home grid heading | C-FE-91 | Front-end specification, Home para |
| `View All` | pinned in home grid heading | C-FE-91 | Front-end specification, Home para |
| `/collections/best-sellers` | pinned in home grid heading | C-FE-91 | Front-end specification, Home para |
| `ELEVATE` | pinned in editorial one | C-FE-92 | Front-end specification, Home para |
| `your daily carry` | pinned in editorial one | C-FE-92 | Front-end specification, Home para |
| `THE CRAFTSMANSHIP OF A` | pinned in editorial two | C-FE-93 | Front-end specification, Home para |
| `tuxedo` | pinned in editorial two | C-FE-93 | Front-end specification, Home para |
| `TAILORED FOR YOUR POCKET.` | pinned in editorial two | C-FE-93 | Front-end specification, Home para |
| `View all` | pinned in chip view all | C-FE-101 | Front-end specification, Collection page para |
| `Featured` | pinned in sort options | C-FE-103 | Front-end specification, Sort para |
| `Best selling` | pinned in sort options | C-FE-103 | Front-end specification, Sort para |
| `Price, low to high` | pinned in sort options | C-FE-103 | Front-end specification, Sort para |
| `Price, high to low` | pinned in sort options | C-FE-103 | Front-end specification, Sort para |
| `Newest` | pinned in sort options | C-FE-103 | Front-end specification, Sort para |
| `Size` | pinned in filter groups | C-FE-106 | Front-end specification, Sort para |
| `Colour` | pinned in filter groups | C-FE-106 | Front-end specification, Sort para |
| `Price` | pinned in filter groups | C-FE-106 | Front-end specification, Sort para |
| `Availability` | pinned in filter groups | C-FE-106 | Front-end specification, Sort para |
| `In stock only` | pinned in filter groups | C-FE-106 | Front-end specification, Sort para |
| `Clear all` | pinned in filter groups | C-FE-106 | Front-end specification, Sort para |
| `Apply` | pinned in filter groups | C-FE-106 | Front-end specification, Sort para |
| `/collections/luggage?size=cabin&colour=pink&sort=price-asc&page=2` | pinned in filter address | C-FE-109 | Front-end specification, Sort para |
| `1/8` | pinned in feature carousel | C-FE-112 | Front-end specification, Product page para |
| `Aviation-grade telescope handle` | pinned in feature carousel | C-FE-112 | Front-end specification, Product page para |
| `Colors` | pinned in tabs | C-FE-114 | Front-end specification, Product page para |
| `Personalise` | pinned in tabs | C-FE-114 | Front-end specification, Product page para |
| `Compare` | pinned in tabs | C-FE-114 | Front-end specification, Product page para |
| `Color:` | pinned in color line | C-FE-117 | Front-end specification, Product page para |
| `Cabin` | pinned in size captions | C-FE-119 | Front-end specification, Product page para |
| `Medium` | pinned in size captions | C-FE-119 | Front-end specification, Product page para |
| `Large` | pinned in size captions | C-FE-119 | Front-end specification, Product page para |
| `Save on Sets` | pinned in size captions | C-FE-119 | Front-end specification, Product page para |
| `MRP:` | pinned in mrp | C-FE-120 | Front-end specification, Product page para |
| `Incl of all taxes` | pinned in taxes | C-FE-121 | Front-end specification, Product page para |
| `or pay in 4 - <first instalment> today - 0% interest` | pinned in instalment | C-FE-122 | Front-end specification, Product page para |
| `PERSONALISE` | pinned in buttons | C-FE-124 | Front-end specification, Product page para |
| `ADD TO CART` | pinned in buttons | C-FE-124 | Front-end specification, Product page para |
| `Packing Cubes (Set of 6)` | pinned in cross sell | C-FE-128 | Front-end specification, Product page para |
| `Travel Pillow` | pinned in cross sell | C-FE-128 | Front-end specification, Product page para |
| `Expected Delivery in <from> - <to>` | pinned in delivery estimate | C-FE-130 | Front-end specification, Product page para |
| `Expected Delivery in 21 Sep - 23 Sep` | pinned in delivery estimate | C-FE-130 | Front-end specification, Product page para |
| `Durable, Lightweight shell` | pinned in trust chips | C-FE-131 | Front-end specification, Product page para |
| `30 Day Return Policy` | pinned in trust chips | C-FE-131 | Front-end specification, Product page para |
| `3 Years Warranty` | pinned in trust chips | C-FE-131 | Front-end specification, Product page para |
| `1-Year` | pinned in coverage strip | C-FE-132 | Front-end specification, Coverage para |
| `AIRLINE DAMAGE COVER` | pinned in coverage strip | C-FE-132 | Front-end specification, Coverage para |
| `$49` | pinned in coverage strip | C-FE-132 | Front-end specification, Coverage para |
| `Details` | pinned in coverage strip | C-FE-132 | Front-end specification, Coverage para |
| `Plan value` | pinned in coverage head | C-FE-135 | Front-end specification, Coverage para |
| `FREE` | pinned in coverage head | C-FE-135 | Front-end specification, Coverage para |
| `Validity` | pinned in coverage head | C-FE-135 | Front-end specification, Coverage para |
| `1 Year` | pinned in coverage head | C-FE-135 | Front-end specification, Coverage para |
| `Spot damage at the belt?` | pinned in coverage steps | C-FE-136 | Front-end specification, Coverage para |
| `Tell us within 7 days` | pinned in coverage steps | C-FE-136 | Front-end specification, Coverage para |
| `We repair or replace` | pinned in coverage steps | C-FE-136 | Front-end specification, Coverage para |
| `Also covered under warranty` | pinned in coverage cards | C-FE-137 | Front-end specification, Coverage para |
| `Shell` | pinned in coverage cards | C-FE-137 | Front-end specification, Coverage para |
| `Wheels & trolley` | pinned in coverage cards | C-FE-137 | Front-end specification, Coverage para |
| `Hardware` | pinned in coverage cards | C-FE-137 | Front-end specification, Coverage para |
| `Not covered` | pinned in coverage exclusions | C-FE-138 | Front-end specification, Coverage para |
| `Theft & loss` | pinned in coverage exclusions | C-FE-138 | Front-end specification, Coverage para |
| `Overpacking` | pinned in coverage exclusions | C-FE-138 | Front-end specification, Coverage para |
| `Wear & tear` | pinned in coverage exclusions | C-FE-138 | Front-end specification, Coverage para |
| `Scratches & scuffs` | pinned in coverage exclusions | C-FE-138 | Front-end specification, Coverage para |
| `Commercial use` | pinned in coverage exclusions | C-FE-138 | Front-end specification, Coverage para |
| `The Road Week Sale` | pinned in offer strip | C-FE-140 | Front-end specification, Offer strip para |
| `Up to 50% off` | pinned in offer strip | C-FE-140 | Front-end specification, Offer strip para |
| `Pay in 4` | pinned in offer strip | C-FE-140 | Front-end specification, Offer strip para |
| `Interest-free on every order` | pinned in offer strip | C-FE-140 | Front-end specification, Offer strip para |
| `Sale Extended! Ends in` | pinned in countdown | C-FE-141 | Front-end specification, Offer strip para |
| `D` | pinned in countdown | C-FE-141 | Front-end specification, Offer strip para |
| `H` | pinned in countdown | C-FE-141 | Front-end specification, Offer strip para |
| `M` | pinned in countdown | C-FE-141 | Front-end specification, Offer strip para |
| `S` | pinned in countdown | C-FE-141 | Front-end specification, Offer strip para |
| `Dimension` | pinned in accordions | C-FE-146 | Front-end specification, Accordions para |
| `Description` | pinned in accordions | C-FE-146 | Front-end specification, Accordions para |
| `Warranty & Return` | pinned in accordions | C-FE-146 | Front-end specification, Accordions para |
| `More Information` | pinned in accordions | C-FE-146 | Front-end specification, Accordions para |
| `Valisette Travelware Co.` | pinned in legal block | C-FE-149 | Front-end specification, Accordions para |
| `Unit 4, Coastline Works` | pinned in legal block | C-FE-149 | Front-end specification, Accordions para |
| `Vietnam, Mexico` | pinned in legal block | C-FE-149 | Front-end specification, Accordions para |
| `30` | pinned in trial banner | C-FE-150 | Front-end specification, Accordions para |
| `days trial` | pinned in trial banner | C-FE-150 | Front-end specification, Accordions para |
| `COMPARE` | pinned in compare module | C-FE-151 | Front-end specification, Accordions para |
| `Wish to Compare your bag?` | pinned in compare module | C-FE-151 | Front-end specification, Accordions para |
| `Your Pick` | pinned in compare module | C-FE-151 | Front-end specification, Accordions para |
| `Recently Viewed` | pinned in recently viewed | C-FE-152 | Front-end specification, Accordions para |
| `Subtotal` | pinned in summary labels | C-FE-155 | Front-end specification, Cart para |
| `Discount` | pinned in summary labels | C-FE-155 | Front-end specification, Cart para |
| `Delivery` | pinned in summary labels | C-FE-155 | Front-end specification, Cart para |
| `Free` | pinned in summary labels | C-FE-155 | Front-end specification, Cart para |
| `Total` | pinned in summary labels | C-FE-155 | Front-end specification, Cart para |
| `Checkout` | pinned in summary labels | C-FE-155 | Front-end specification, Cart para |
| `Contact & delivery` | pinned in checkout labels | C-FE-161 | Front-end specification, Checkout para |
| `Delivery method` | pinned in checkout labels | C-FE-161 | Front-end specification, Checkout para |
| `Payment` | pinned in checkout labels | C-FE-161 | Front-end specification, Checkout para |
| `Standard` | pinned in delivery choices | C-FE-163 | Front-end specification, Checkout para |
| `Free, 3 to 5 days` | pinned in delivery choices | C-FE-163 | Front-end specification, Checkout para |
| `Express` | pinned in delivery choices | C-FE-163 | Front-end specification, Checkout para |
| `$15, 1 to 2 days` | pinned in delivery choices | C-FE-163 | Front-end specification, Checkout para |
| `Pay now` | pinned in payment choices | C-FE-165 | Front-end specification, Checkout para |
| `Bill a corporate account` | pinned in payment choices | C-FE-165 | Front-end specification, Checkout para |
| `Corporate account reference` | pinned in payment choices | C-FE-165 | Front-end specification, Checkout para |
| `Arriving <from> - <to>` | pinned in confirmation parts | C-FE-170 | Front-end specification, Checkout para |
| `Find a store by city or name` | pinned in store placeholder | C-FE-171 | Front-end specification, Store directory para |
| `Opening hours` | pinned in store disclosure | C-FE-174 | Front-end specification, Store directory para |
| `Call the store` | pinned in store disclosure | C-FE-174 | Front-end specification, Store directory para |
| `Directions` | pinned in store disclosure | C-FE-174 | Front-end specification, Store directory para |
| `No store matches that yet.` | pinned in store empty | C-FE-175 | Front-end specification, Store directory para |
| `<count> results for "<query>"` | pinned in search header | C-FE-177 | Front-end specification, Search page para |
| `Gift card code` | pinned in gift form | C-FE-179 | Front-end specification, Standing pages para |
| `CHECK BALANCE` | pinned in gift form | C-FE-179 | Front-end specification, Standing pages para |
| `The page you asked for is not here any more.` | pinned in nf copy | C-FE-180 | Front-end specification, Not-found para |
| `Home` | pinned in nf copy | C-FE-180 | Front-end specification, Not-found para |
| `Shop all` | pinned in nf copy | C-FE-180 | Front-end specification, Not-found para |
| `Find a store` | pinned in nf copy | C-FE-180 | Front-end specification, Not-found para |
| `Login` | pinned in login form | C-FE-181 | Front-end specification, Account pages para |
| `Email` | pinned in login form | C-FE-181 | Front-end specification, Account pages para |
| `Enter your email` | pinned in login form | C-FE-181 | Front-end specification, Account pages para |
| `Password` | pinned in login form | C-FE-181 | Front-end specification, Account pages para |
| `Enter your password` | pinned in login form | C-FE-181 | Front-end specification, Account pages para |
| `Remember me` | pinned in login options | C-FE-182 | Front-end specification, Account pages para |
| `Forgot password?` | pinned in login options | C-FE-182 | Front-end specification, Account pages para |
| `LOGIN` | pinned in login options | C-FE-182 | Front-end specification, Account pages para |
| `Create an account` | pinned in register form | C-FE-184 | Front-end specification, Account pages para |
| `Name` | pinned in register form | C-FE-184 | Front-end specification, Account pages para |
| `Confirm password` | pinned in register form | C-FE-184 | Front-end specification, Account pages para |
| `CREATE ACCOUNT` | pinned in register form | C-FE-184 | Front-end specification, Account pages para |
| `The two passwords do not match.` | pinned in register mismatch | C-FE-185 | Front-end specification, Account pages para |
| `Reset your password` | pinned in recover form | C-FE-186 | Front-end specification, Account pages para |
| `SEND RESET LINK` | pinned in recover form | C-FE-186 | Front-end specification, Account pages para |
| `Choose a new password` | pinned in reset form | C-FE-187 | Front-end specification, Account pages para |
| `SAVE PASSWORD` | pinned in reset form | C-FE-187 | Front-end specification, Account pages para |
| `Your password has been changed.` | pinned in reset form | C-FE-187 | Front-end specification, Account pages para |
| `/account` | pinned in greeting | C-FE-188 | Front-end specification, Account pages para |
| `Hello, <first name>` | pinned in greeting | C-FE-188 | Front-end specification, Account pages para |
| `Hello, Aarav` | pinned in greeting | C-FE-188 | Front-end specification, Account pages para |
| `Pending` | pinned in state words | C-FE-190 | Front-end specification, Account pages para |
| `Paid` | pinned in state words | C-FE-190 | Front-end specification, Account pages para |
| `Fulfilled` | pinned in state words | C-FE-190 | Front-end specification, Account pages para |
| `Cancelled` | pinned in state words | C-FE-190 | Front-end specification, Account pages para |
| `Default` | pinned in default marker | C-FE-191 | Front-end specification, Account pages para |
| `aria-label` | pinned in hooks swatch | C-FE-196 | Front-end specification, Machine-readable hooks para |
| `aria-pressed` | pinned in hooks swatch | C-FE-196 | Front-end specification, Machine-readable hooks para |
| `true` | pinned in hooks swatch | C-FE-196 | Front-end specification, Machine-readable hooks para |
| `role="group"` | pinned in hooks group | C-FE-197 | Front-end specification, Machine-readable hooks para |
| `role="img"` | pinned in hooks img | C-FE-198 | Front-end specification, Machine-readable hooks para |
| `data-ends-at` | pinned in hooks countdown | C-FE-199 | Front-end specification, Machine-readable hooks para |
| `data-unit` | pinned in hooks countdown | C-FE-199 | Front-end specification, Machine-readable hooks para |
| `d` | pinned in hooks countdown | C-FE-199 | Front-end specification, Machine-readable hooks para |
| `h` | pinned in hooks countdown | C-FE-199 | Front-end specification, Machine-readable hooks para |
| `m` | pinned in hooks countdown | C-FE-199 | Front-end specification, Machine-readable hooks para |
| `s` | pinned in hooks countdown | C-FE-199 | Front-end specification, Machine-readable hooks para |
| `${APP_PUBLIC_PORT}:4173` | pinned in port map | C-DC-02 | Deployment contract, bullet 1 |
| `0.0.0.0` | pinned in bind | C-DC-11 | Deployment contract, bullet 9 |
| `127.0.0.1` | pinned in bind | C-DC-11 | Deployment contract, bullet 9 |
| `localhost` | pinned in bind | C-DC-11 | Deployment contract, bullet 9 |
| `Pair It With` | cross-sell heading | C-FE-128 | Front-end specification, Product page para |
| `How it works` | coverage steps heading | C-FE-136 | Front-end specification, Coverage para |
| `That email and password do not match.` | the failed sign-in message | C-CF-16 | Core features, Accounts rule 3 |
| `The price of one item changed while you were shopping. Review before paying.` | the price-change refusal message | C-CF-224 | Core features, Checkout rule 4 |
| `Included with this luggage` | coverage dialog eyebrow | C-FE-135 | Front-end specification, Coverage para |
| `1 year of airline damage cover. Free.` | coverage dialog headline | C-FE-135 | Front-end specification, Coverage para |
| `Free with this luggage` | coverage strip qualifier | C-FE-132 | Front-end specification, Coverage para |
| `Your order is billed through our payments partner when you place it.` | payment step line | C-FE-165 | Front-end specification, Checkout para |
| `Order and try valisette for 30 days.` | returns drawer line | C-FE-148 | Front-end specification, Accordions para |
| `Manufactured, Imported and Marketed by:` | legal block opener | C-FE-149 | Front-end specification, Accordions para |
| `Weight` | Dimension drawer mass label | C-FE-147 | Front-end specification, Accordions para |
| `Indestructible and lightweight` | feature carousel heading | C-FE-112 | Front-end specification, Product page para |
| `care@valisette.example.com` | support address | C-FE-148 | Front-end specification, Accordions para |
| `+1 503 555 0142` | support phone | C-FE-45 | Front-end specification, Footer para |
| `+1 503 555 0199` | gifting phone | C-FE-46 | Front-end specification, Footer para |
| `gifting@valisette.example.com` | gifting address | C-FE-46 | Front-end specification, Footer para |
| `Message us at +1 503 555 0199 or email gifting@valisette.example.com` | pinned in C-FE-46 | C-FE-46 | Front-end specification, Footer para |
| `The End of Digging.` | pinned in C-FE-128 | C-FE-128 | Front-end specification, Product page para |
| `Your Window Seat Upgrade.` | pinned in C-FE-128 | C-FE-128 | Front-end specification, Product page para |
| `Heat, fire & chemicals` | pinned in C-FE-138 | C-FE-138 | Front-end specification, Coverage para |
| `118 Canal Street` | pinned in C-FE-149 | C-FE-149 | Front-end specification, Accordions para |
| `Portland, OR 97209, USA` | pinned in C-FE-149 | C-FE-149 | Front-end specification, Accordions para |
| `Country of Origin:` | pinned in C-FE-149 | C-FE-149 | Front-end specification, Accordions para |
| `Silent wheels` | pinned in C-FE-207 | C-FE-207 | Front-end specification, Product page para |
| `Water resistant` | pinned in C-FE-207 | C-FE-207 | Front-end specification, Product page para |
| `Thoughtful details` | pinned in C-FE-207 | C-FE-207 | Front-end specification, Product page para |
| `3 years warranty` | pinned in C-FE-207 | C-FE-207 | Front-end specification, Product page para |
| `30 day trial` | pinned in C-FE-207 | C-FE-207 | Front-end specification, Product page para |
| `Tech Range` | pinned in C-FE-208 | C-FE-208 | Front-end specification, Panels para |
| `Check-in` | pinned in C-FE-208 | C-FE-208 | Front-end specification, Panels para |
| `Check-in Large` | pinned in C-FE-208 | C-FE-208 | Front-end specification, Panels para |
| `Trunk` | pinned in C-FE-208 | C-FE-208 | Front-end specification, Panels para |
| `Kids Luggage` | pinned in C-FE-208 | C-FE-208 | Front-end specification, Panels para |
| `Sets` | pinned in C-FE-208 | C-FE-208 | Front-end specification, Panels para |
| `Passage` | pinned in C-FE-209 | C-FE-209 | Front-end specification, Panels para |
| `Contour` | pinned in C-FE-209 | C-FE-209 | Front-end specification, Panels para |
| `Meridian` | pinned in C-FE-209 | C-FE-209 | Front-end specification, Panels para |
| `Ridge` | pinned in C-FE-209 | C-FE-209 | Front-end specification, Panels para |
| `Solstice` | pinned in C-FE-209 | C-FE-209 | Front-end specification, Panels para |
| `Best Sellers` | pinned in C-FE-210 | C-FE-210 | Front-end specification, Panels para |
| `On Sale` | pinned in C-FE-210 | C-FE-210 | Front-end specification, Panels para |
| `Backpacks` | pinned in C-FE-211 | C-FE-211 | Front-end specification, Panels para |
| `Briefcases` | pinned in C-FE-211 | C-FE-211 | Front-end specification, Panels para |
| `Duffles` | pinned in C-FE-211 | C-FE-211 | Front-end specification, Panels para |
| `Diaper Bags` | pinned in C-FE-211 | C-FE-211 | Front-end specification, Panels para |
| `Kids Backpacks` | pinned in C-FE-211 | C-FE-211 | Front-end specification, Panels para |
| `Work` | pinned in C-FE-212 | C-FE-212 | Front-end specification, Panels para |
| `Travel` | pinned in C-FE-212 | C-FE-212 | Front-end specification, Panels para |
| `Diaper & Kids` | pinned in C-FE-212 | C-FE-212 | Front-end specification, Panels para |
| `Cracks, dents & colour fades` | pinned in C-FE-214 | C-FE-214 | Front-end specification, Coverage para |
| `Wobbles, stiff handles, buttons` | pinned in C-FE-214 | C-FE-214 | Front-end specification, Coverage para |
| `Zippers, handles, feet & logo plate` | pinned in C-FE-214 | C-FE-214 | Front-end specification, Coverage para |
| `Part of valisette Shield, valisette's damage protection programme.` | pinned in C-FE-215 | C-FE-215 | Front-end specification, Coverage para |
| `Not 100% Sure?` | pinned in C-FE-217 | C-FE-217 | Front-end specification, Accordions para |
| `No strings attached.` | pinned in C-FE-217 | C-FE-217 | Front-end specification, Accordions para |
| `3 Years worry-free warranty.` | pinned in C-FE-217 | C-FE-217 | Front-end specification, Accordions para |
| `We'll email you important updates, new launch info and the occasional silly picture.` | newsletter body | C-FE-39 | Front-end specification, Footer para |
| `Write to us at care@valisette.example.com or call us at +1 503 555 0142. We're available on weekdays from 10:00 AM to 7:00 PM and on Saturdays from 10:00 AM to 6:00 PM.` | contact sentence | C-FE-45 | Front-end specification, Footer para |
| `We believe people have to keep moving to thrive. To grow. To feel alive. As long as there is a destination in mind, whether it's a life goal, a career aim or a trip, there is a purpose. We're on a mission to help folks travel with ease and arrive looking sharp. Every trip starts the minute you have a destination in mind, not when you get there.` | footer essay body | C-FE-49 | Front-end specification, Footer para |
| `Make it truly yours` | personalisation carousel heading | C-FE-207 | Front-end specification, Product page para |
| `Get a damage report from the airline desk before you leave the airport.` | coverage step body | C-FE-213 | Front-end specification, Coverage para |
| `Share the report and photographs of the damage.` | coverage step body | C-FE-213 | Front-end specification, Coverage para |
| `Your luggage. Free.` | coverage step body | C-FE-213 | Front-end specification, Coverage para |
| `If an airline damages your bag in transit, we repair or replace it. No extra cost, no fine print gymnastics.` | coverage promise | C-FE-216 | Front-end specification, Coverage para |
| `We know you'll love it, but if you don't, just send it back. We'll give you a full refund. We offer a 30 day risk free return on all our luggage. To start a return, email us at care@valisette.example.com.` | refund paragraph | C-FE-217 | Front-end specification, Accordions para |
| `We love our products. If anything breaks we fix or replace it for you.` | warranty line | C-FE-217 | Front-end specification, Accordions para |
| `Try out your valisette for 30 days. If you still feel it's not the one for you, return it for a full refund.` | trial banner body | C-FE-218 | Front-end specification, Accordions para |
| `Capacity` | Dimension drawer volume label | C-FE-147 | Front-end specification, Accordions para |
| `External dimensions` | Dimension drawer size label | C-FE-147 | Front-end specification, Accordions para |
| `Addresses` | account overview link | C-FE-189 | Front-end specification, Account pages para |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the weight, capacity and dimensions of bags, totes, slings, accessories and wallets | C-CF-63 | the brief leaves these figures to the builder |
| the swatch colour values | C-CF-43 | each is a `#RRGGBB` string reading as its family, with no value pinned |
| the description blocks of each product | C-CF-63 | the brief pins the field, not its text |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 16 |
| User roles | 2 | 40 |
| Core features | 49 | 391 |
| User flow | 16 | 51 |
| UI and UX notes | 8 | 96 |
| Technical requirements | 7 | 29 |
| Data model | 7 | 45 |
| Front-end specification | 40 | 238 |
| Constraints | 1 | 12 |
| Deployment contract | 10 | 25 |
