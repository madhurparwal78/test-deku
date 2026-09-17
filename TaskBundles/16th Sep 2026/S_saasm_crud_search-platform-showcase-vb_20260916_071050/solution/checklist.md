# Checklist: Kestrel

Items: 1002
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves a public marketing surface plus an operator console behind one sign-in. `src: Overview`
- [ ] `C-OV-02` `capability` The search box in the header runs the same engine the product sells. `src: Overview`
- [ ] `C-OV-03` `capability` The search covers documentation, support articles, blog posts, website pages, developer content, resources, academy courses, customer stories. `src: Overview`
- [ ] `C-OV-04` `capability` The conversational mode answers in prose, offering a route back to the plain results. `src: Overview`
- [ ] `C-OV-05` `constraint` The product carries no payment of any kind. `src: Overview`
- [ ] `C-OV-06` `constraint` The product sends no message of any kind. `src: Overview`
- [ ] `C-OV-07` `constraint` The product loads no third-party script. `src: Overview`
- [ ] `C-OV-08` `constraint` The product ships no binary asset. `src: Overview`
- [ ] `C-OV-09` `constraint` The ordering contract is lexicographic rather than arithmetic. `src: Overview`
- [ ] `C-OV-10` `constraint` The counting contract answers a different question from the one that produced the results on screen. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads the public routes. `src: User roles`
- [ ] `C-RL-02` `role` A signed-out visitor opens the search overlay, searching the public indices. `src: User roles`
- [ ] `C-RL-03` `role` A signed-out visitor answers the cookie question. `src: User roles`
- [ ] `C-RL-04` `role` A signed-out visitor submits the demo request form. `src: User roles`
- [ ] `C-RL-05` `role` A signed-out visitor subscribes to the newsletter. `src: User roles`
- [ ] `C-RL-06` `role` A signed-out visitor cannot reach any console route. `src: User roles`
- [ ] `C-RL-07` `role` An `analyst` browses records read only. `src: User roles`
- [ ] `C-RL-08` `role` An `analyst` runs the search preview. `src: User roles`
- [ ] `C-RL-09` `role` An `analyst` reads every analytics screen. `src: User roles`
- [ ] `C-RL-10` `role` An `analyst` cannot write a record. `src: User roles`
- [ ] `C-RL-11` `role` An `analyst` cannot edit index settings. `src: User roles`
- [ ] `C-RL-12` `role` An `analyst` cannot edit a rule. `src: User roles`
- [ ] `C-RL-13` `role` An `analyst` cannot edit a synonym. `src: User roles`
- [ ] `C-RL-14` `role` An `operator` writes records. `src: User roles`
- [ ] `C-RL-15` `role` An `operator` edits index settings, rules, synonyms. `src: User roles`
- [ ] `C-RL-16` `role` An `operator` cannot manage keys. `src: User roles`
- [ ] `C-RL-17` `role` An `operator` cannot manage members. `src: User roles`
- [ ] `C-RL-18` `role` An `admin` creates, lists, revokes keys. `src: User roles`
- [ ] `C-RL-19` `role` An `admin` cannot manage members. `src: User roles`
- [ ] `C-RL-20` `role` An `owner` manages members, the plan. `src: User roles`
- [ ] `C-RL-21` `role` An `owner` cannot reach another workspace's application by any route. `src: User roles`
- [ ] `C-RL-22` `capability` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-23` `capability` A hidden control never stands in for a server decision. `src: User roles`
- [ ] `C-RL-24` `capability` A direct call from a lower role to a higher-role endpoint is denied, leaving the protected state unchanged. `src: User roles`
- [ ] `C-RL-25` `ui` The role matrix is rendered on the members screen. `src: User roles`
- [ ] `C-RL-26` `capability` Signup is open, requiring no invitation. `src: User roles`
- [ ] `C-RL-27` `capability` A new signup creates its own workspace, its own application. `src: User roles`
- [ ] `C-RL-28` `capability` A new signup becomes the `owner` of the created workspace. `src: User roles`
- [ ] `C-RL-29` `literal` The seeded accounts are `owner@example.com`, `admin@example.com`, `operator@example.com`, `analyst@example.com`, `owner2@example.com`. `src: User roles`
- [ ] `C-RL-30` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-31` `literal` The seeded display names are `Amelia Ortega`, `Ravi Menon`, `Lena Fischer`, `Tomas Silva`, `Priya Raman`. `src: User roles`
- [ ] `C-RL-32` `literal` The two seeded workspaces are `Kestrel Demo`, `Northmoor Group`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` Sign-in accepts an email plus a password, returning a bearer token. `src: Core features, auth`
- [ ] `C-CF-02` `capability` A console bearer token expires after twelve hours. `src: Core features, auth`
- [ ] `C-CF-03` `capability` An expired console token is refused. `src: Core features, auth`
- [ ] `C-CF-04` `constraint` A password is stored hashed, never in clear text. `src: Core features, auth`
- [ ] `C-CF-05` `capability` Signup lowercases the submitted email before storing. `src: Core features, auth`
- [ ] `C-CF-06` `capability` Signup on an email already taken is rejected as invalid, naming the email field. `src: Core features, auth`
- [ ] `C-CF-07` `capability` A rejected signup leaves no second account row, no second workspace row, no second application row. `src: Core features, auth`
- [ ] `C-CF-08` `constraint` No password-reset flow exists. `src: Core features, auth`
- [ ] `C-CF-09` `capability` A successful signup creates exactly one workspace, one application, one `owner` membership. `src: Core features, auth`
- [ ] `C-CF-10` `capability` Every request resolves to exactly one workspace. `src: Core features, auth`
- [ ] `C-CF-11` `capability` A cross-workspace request reads nothing. `src: Core features, auth`
- [ ] `C-CF-12` `constraint` A refusal for an unreachable index is worded identically to a refusal for an absent index. `src: Core features, auth`
- [ ] `C-CF-13` `capability` Every form rejects invalid input inline, naming the wrong field. `src: Core features, auth`
- [ ] `C-CF-14` `capability` A rejected form writes nothing. `src: Core features, auth`
- [ ] `C-CF-15` `capability` The overlay opens from the header field on every route carrying chrome. `src: Core features, the site search overlay`
- [ ] `C-CF-16` `capability` The overlay opens from the body of the not-found route. `src: Core features, the site search overlay`
- [ ] `C-CF-17` `capability` The overlay searches the seeded `site_content` index. `src: Core features, the site search overlay`
- [ ] `C-CF-18` `capability` The overlay issues a query against the real index on every keystroke. `src: Core features, the site search overlay`
- [ ] `C-CF-19` `constraint` The overlay never filters a copy of data the page already holds. `src: Core features, the site search overlay`
- [ ] `C-CF-20` `ui` A hit row carries a title, a meta line, an action. `src: Core features, the site search overlay`
- [ ] `C-CF-21` `literal` The hit meta line takes the form `Website • products`. `src: Core features, the site search overlay`
- [ ] `C-CF-22` `literal` The hit action reads `Learn more →`. `src: Core features, the site search overlay`
- [ ] `C-CF-23` `literal` The results heading reads `Products & Resources`. `src: Core features, the site search overlay`
- [ ] `C-CF-24` `literal` The refinement heading reads `Filter by source`. `src: Core features, the site search overlay`
- [ ] `C-CF-25` `literal` The eight sources are `Documentation`, `Support`, `Blog`, `Website`, `Developers`, `Resources`, `Academy`, `Customer Stories`. `src: Core features, the site search overlay`
- [ ] `C-CF-26` `literal` The unfiltered source counts are `40`, `24`, `18`, `12`, `9`, `8`, `5`, `4`. `src: Core features, the site search overlay`
- [ ] `C-CF-27` `capability` Selecting one source leaves the other seven counts non-zero. `src: Core features, the site search overlay`
- [ ] `C-CF-28` `ui` Matched words are wrapped in the highlight tags inside the hit's own text. `src: Core features, the site search overlay`
- [ ] `C-CF-29` `capability` The number of results is announced once the list has settled. `src: Core features, the site search overlay`
- [ ] `C-CF-30` `constraint` The result count is never announced once per keystroke. `src: Core features, the site search overlay`
- [ ] `C-CF-31` `literal` The load-more control reads `Show more results`. `src: Core features, the site search overlay`
- [ ] `C-CF-32` `capability` Loading more results causes no navigation. `src: Core features, the site search overlay`
- [ ] `C-CF-33` `capability` A click on a hit records an interaction event carrying the query identity. `src: Core features, the site search overlay`
- [ ] `C-CF-34` `literal` The first suggested question asks how Kestrel improves a customer's search experience, conversions. `src: Core features, the site search overlay`
- [ ] `C-CF-35` `literal` The second suggested question reads `How do I integrate Kestrel search into my app?`. `src: Core features, the site search overlay`
- [ ] `C-CF-36` `literal` The third suggested question asks whether Kestrel helps shoppers find products faster, increasing sales. `src: Core features, the site search overlay`
- [ ] `C-CF-37` `literal` The fourth suggested question asks whether Kestrel scales with a customer's traffic, data size. `src: Core features, the site search overlay`
- [ ] `C-CF-38` `literal` The suggestions heading reads `Suggestions`. `src: Core features, the site search overlay`
- [ ] `C-CF-39` `literal` The four keyword buttons read `Kestrel API integration`, `Kestrel search benefits`, `Kestrel scalability`, `AI search for ecommerce`. `src: Core features, the site search overlay`
- [ ] `C-CF-40` `capability` The keyword buttons are built from the query rollups. `src: Core features, the site search overlay`
- [ ] `C-CF-41` `constraint` A query nobody has run is never offered as a suggestion. `src: Core features, the site search overlay`
- [ ] `C-CF-42` `literal` The mode toggle is labelled `AI mode`. `src: Core features, the site search overlay`
- [ ] `C-CF-43` `literal` The assistant title reads `Kestrel Assist`. `src: Core features, the site search overlay`
- [ ] `C-CF-44` `literal` The assistant actions read `New chat`, `Back to results`. `src: Core features, the site search overlay`
- [ ] `C-CF-45` `literal` The assistant attribution reads `AI powered by Kestrel`. `src: Core features, the site search overlay`
- [ ] `C-CF-46` `literal` The overlay filter controls read `Show All`, `Clear All Filters`. `src: Core features, the site search overlay`
- [ ] `C-CF-47` `constraint` The conversational answer never replaces the results. `src: Core features, the site search overlay`
- [ ] `C-CF-48` `ui` Down, Up move the active option, leaving focus in the input. `src: Core features, the site search overlay`
- [ ] `C-CF-49` `ui` Enter opens the active option, submitting the raw query when none is active. `src: Core features, the site search overlay`
- [ ] `C-CF-50` `ui` A first Escape clears the list, a second clears the input. `src: Core features, the site search overlay`
- [ ] `C-CF-51` `ui` Tab completes to the active option's text, opening nothing. `src: Core features, the site search overlay`
- [ ] `C-CF-52` `ui` Home, End move within the text, never within the list. `src: Core features, the site search overlay`
- [ ] `C-CF-53` `capability` The overlay closes on a route change. `src: Core features, the site search overlay`
- [ ] `C-CF-54` `literal` The eight ranking criteria are `typo`, `geo`, `words`, `filters`, `proximity`, `attribute`, `exact`, `custom`. `src: Core features, the ranking cascade`
- [ ] `C-CF-55` `capability` Each criterion is consulted only when the one before produced a tie. `src: Core features, the ranking cascade`
- [ ] `C-CF-56` `constraint` No weighted sum appears anywhere in the ordering. `src: Core features, the ranking cascade`
- [ ] `C-CF-57` `constraint` No relevance number is computed for the ordering. `src: Core features, the ranking cascade`
- [ ] `C-CF-58` `capability` A record carrying one typo ranks below every record carrying none. `src: Core features, the ranking cascade`
- [ ] `C-CF-59` `literal` The fixture query `blue running shoes` returns the order `r1`, `r3`, `r4`, `r2`. `src: Core features, the ranking cascade`
- [ ] `C-CF-60` `capability` Removing `customRanking` leaves the fixture order unchanged. `src: Core features, the ranking cascade`
- [ ] `C-CF-61` `capability` Disabling typo tolerance drops `r2`, leaving the other three in order. `src: Core features, the ranking cascade`
- [ ] `C-CF-62` `capability` The final tie-break is `objectID` ascending. `src: Core features, the ranking cascade`
- [ ] `C-CF-63` `capability` One query repeated fifty times returns a byte-identical ordering. `src: Core features, the ranking cascade`
- [ ] `C-CF-64` `capability` Collecting every page yields each `objectID` exactly once. `src: Core features, the ranking cascade`
- [ ] `C-CF-65` `capability` Proximity counts tokens between the closest matching positions of adjacent query words in one attribute, plus one. `src: Core features, the ranking cascade`
- [ ] `C-CF-66` `literal` Proximity is capped at `8`. `src: Core features, the ranking cascade`
- [ ] `C-CF-67` `capability` Adjacent words in order cost one; adjacent words reversed cost two. `src: Core features, the ranking cascade`
- [ ] `C-CF-68` `capability` Words matched in different attributes cost the proximity cap. `src: Core features, the ranking cascade`
- [ ] `C-CF-69` `capability` An unmatched optional word is skipped when pairs are formed. `src: Core features, the ranking cascade`
- [ ] `C-CF-70` `capability` A phrase requires proximity one for its pairs. `src: Core features, the ranking cascade`
- [ ] `C-CF-71` `literal` The query `blue shoes` returns `r4` before `r1`. `src: Core features, the ranking cascade`
- [ ] `C-CF-72` `capability` The attribute criterion compares the winning attribute's position in `searchableAttributes` first. `src: Core features, the ranking cascade`
- [ ] `C-CF-73` `capability` The attribute criterion then compares the match position inside that attribute. `src: Core features, the ranking cascade`
- [ ] `C-CF-74` `literal` The word-position component is capped at `63`. `src: Core features, the ranking cascade`
- [ ] `C-CF-75` `capability` Attributes wrapped `unordered(attr)` at one list position share an index. `src: Core features, the ranking cascade`
- [ ] `C-CF-76` `capability` An `unordered(attr)` attribute sets the word-position component to zero. `src: Core features, the ranking cascade`
- [ ] `C-CF-77` `constraint` Ordered attributes at different positions never tie. `src: Core features, the ranking cascade`
- [ ] `C-CF-78` `capability` The exact criterion counts query words matched with zero typos. `src: Core features, the ranking cascade`
- [ ] `C-CF-79` `constraint` A prefix expansion never counts toward the exact criterion. `src: Core features, the ranking cascade`
- [ ] `C-CF-80` `literal` `exactOnSingleWordQuery` takes `attribute`, `word`, `none`. `src: Core features, the ranking cascade`
- [ ] `C-CF-81` `literal` `alternativesAsExact` takes `ignorePlurals`, `singleWordSynonym`, `multiWordsSynonym`. `src: Core features, the ranking cascade`
- [ ] `C-CF-82` `capability` A one-word synonym counts as exact by default. `src: Core features, the ranking cascade`
- [ ] `C-CF-83` `constraint` A multi-word synonym does not count as exact by default. `src: Core features, the ranking cascade`
- [ ] `C-CF-84` `constraint` A decompounded part never counts as exact. `src: Core features, the ranking cascade`
- [ ] `C-CF-85` `literal` `customRanking` entries take the form `asc(attr)` or `desc(attr)`. `src: Core features, the ranking cascade`
- [ ] `C-CF-86` `capability` Each `customRanking` entry is its own tie-break level. `src: Core features, the ranking cascade`
- [ ] `C-CF-87` `capability` Numeric custom values compare at four significant decimal digits. `src: Core features, the ranking cascade`
- [ ] `C-CF-88` `capability` A record missing a custom attribute sorts last for ascending order, for descending order. `src: Core features, the ranking cascade`
- [ ] `C-CF-89` `capability` A boolean custom value compares as one, zero. `src: Core features, the ranking cascade`
- [ ] `C-CF-90` `capability` A string custom value compares by code point after folding. `src: Core features, the ranking cascade`
- [ ] `C-CF-91` `capability` A list custom value compares by its first element. `src: Core features, the ranking cascade`
- [ ] `C-CF-92` `capability` The geo criterion applies when `aroundLatLng` is set. `src: Core features, the ranking cascade`
- [ ] `C-CF-93` `literal` Geo distance is haversine metres on a sphere of radius `6371000` metres. `src: Core features, the ranking cascade`
- [ ] `C-CF-94` `literal` Geo distance is bucketed by `aroundPrecision`, default `10` metres. `src: Core features, the ranking cascade`
- [ ] `C-CF-95` `capability` The geo bucket rather than the raw distance is compared. `src: Core features, the ranking cascade`
- [ ] `C-CF-96` `literal` Searching around `48.8566,2.3522` returns the eight-metre record first, the five-metre record second, the sixty-metre record third. `src: Core features, the ranking cascade`
- [ ] `C-CF-97` `capability` `aroundRadius` filters before ranking. `src: Core features, the ranking cascade`
- [ ] `C-CF-98` `literal` `aroundRadius` set to `all` disables the geo filter, keeping the geo ranking. `src: Core features, the ranking cascade`
- [ ] `C-CF-99` `constraint` `insidePolygon`, `insideBoundingBox` filter only, never enabling the geo criterion. `src: Core features, the ranking cascade`
- [ ] `C-CF-100` `literal` `relevancyStrictness` runs `0` to `100`, defaulting to `100`. `src: Core features, the ranking cascade`
- [ ] `C-CF-101` `capability` At full strictness only the best `words` bucket is returned. `src: Core features, the ranking cascade`
- [ ] `C-CF-102` `capability` Below full strictness a hit under the cut is returned marked as not promoted. `src: Core features, the ranking cascade`
- [ ] `C-CF-103` `capability` The response reports the count of hits above the strictness cut. `src: Core features, the ranking cascade`
- [ ] `C-CF-104` `capability` The text pipeline applies Unicode normalization to `NFKC` first. `src: Core features, text pipeline`
- [ ] `C-CF-105` `capability` The text pipeline folds case fully, mapping the eszett to a double letter. `src: Core features, text pipeline`
- [ ] `C-CF-106` `capability` The Turkish tailoring applies only when `queryLanguages` carries `tr`. `src: Core features, text pipeline`
- [ ] `C-CF-107` `capability` The text pipeline folds diacritics after decomposition, recomposing afterwards. `src: Core features, text pipeline`
- [ ] `C-CF-108` `capability` Per-language exemptions keep a mark that is a letter rather than an accent. `src: Core features, text pipeline`
- [ ] `C-CF-109` `capability` Latin, Cyrillic, Greek split on anything that is neither letter nor digit. `src: Core features, text pipeline`
- [ ] `C-CF-110` `literal` `o'brien` yields one token. `src: Core features, text pipeline`
- [ ] `C-CF-111` `literal` `l'hotel` yields `l`, `hotel`. `src: Core features, text pipeline`
- [ ] `C-CF-112` `capability` A hyphenated word yields three tokens: the two parts, the joined form. `src: Core features, text pipeline`
- [ ] `C-CF-113` `capability` Han, Hiragana, Katakana take overlapping bigrams. `src: Core features, text pipeline`
- [ ] `C-CF-114` `constraint` Han, Hiragana, Katakana take neither unigrams nor dictionary segmentation. `src: Core features, text pipeline`
- [ ] `C-CF-115` `capability` Thai, Khmer, Lao take dictionary segmentation, falling back to whole-run tokens. `src: Core features, text pipeline`
- [ ] `C-CF-116` `capability` A dictionary-segmentation fallback is reported in the index build log. `src: Core features, text pipeline`
- [ ] `C-CF-117` `capability` A run of digits is one token. `src: Core features, text pipeline`
- [ ] `C-CF-118` `constraint` A decimal point inside digits does not split the token. `src: Core features, text pipeline`
- [ ] `C-CF-119` `literal` `a4` yields `a4`, `a`, `4`. `src: Core features, text pipeline`
- [ ] `C-CF-120` `capability` Stop words are removed at query time only. `src: Core features, text pipeline`
- [ ] `C-CF-121` `constraint` Stop words are never removed at index time. `src: Core features, text pipeline`
- [ ] `C-CF-122` `literal` With `ignorePlurals` on, `houses` maps to `house`. `src: Core features, text pipeline`
- [ ] `C-CF-123` `literal` With `ignorePlurals` on, `housing` does not map to `house`. `src: Core features, text pipeline`
- [ ] `C-CF-124` `capability` Decompounding applies to German, Dutch, Finnish, Swedish, Danish, Norwegian, Korean. `src: Core features, text pipeline`
- [ ] `C-CF-125` `capability` A decompounded part is marked as decompounded. `src: Core features, text pipeline`
- [ ] `C-CF-126` `capability` Every token keeps a byte offset range into the original un-normalized string. `src: Core features, text pipeline`
- [ ] `C-CF-127` `literal` Typo budgets are decided by `minWordSizefor1Typo`, default `4`, `minWordSizefor2Typos`, default `8`. `src: Core features, text pipeline`
- [ ] `C-CF-128` `capability` Word length is measured in Unicode scalars after folding. `src: Core features, text pipeline`
- [ ] `C-CF-129` `capability` A transposition of two adjacent characters costs one. `src: Core features, text pipeline`
- [ ] `C-CF-130` `literal` The query `hlelo` returns `t1` with a reported typo count of `1`. `src: Core features, text pipeline`
- [ ] `C-CF-131` `constraint` The first character may never be substituted, never deleted. `src: Core features, text pipeline`
- [ ] `C-CF-132` `literal` The query `xello` returns `t1` not at all. `src: Core features, text pipeline`
- [ ] `C-CF-133` `literal` The query `2024` returns `t4`, never `t5`. `src: Core features, text pipeline`
- [ ] `C-CF-134` `capability` A digit token gets no typo tolerance unless `allowTyposOnNumericTokens` is on. `src: Core features, text pipeline`
- [ ] `C-CF-135` `constraint` Typo tolerance is off inside a phrase. `src: Core features, text pipeline`
- [ ] `C-CF-136` `constraint` Typo tolerance is off for attributes named in `disableTypoToleranceOnAttributes`. `src: Core features, text pipeline`
- [ ] `C-CF-137` `literal` `typoTolerance` set to `min` returns typo matches only when the zero-typo set is empty. `src: Core features, text pipeline`
- [ ] `C-CF-138` `literal` `typoTolerance` set to `strict` drops two-typo matches whenever a one-typo match exists. `src: Core features, text pipeline`
- [ ] `C-CF-139` `literal` The default `queryType` is `prefixLast`. `src: Core features, text pipeline`
- [ ] `C-CF-140` `capability` Only the last query word is matched as a prefix by default. `src: Core features, text pipeline`
- [ ] `C-CF-141` `literal` `prefixAll` applies the prefix rule to every word; `prefixNone` applies the prefix rule to none. `src: Core features, text pipeline`
- [ ] `C-CF-142` `literal` The query `hel` returns `t1`, `t2`. `src: Core features, text pipeline`
- [ ] `C-CF-143` `literal` The query `hel world` returns `t1`, never `t2`. `src: Core features, text pipeline`
- [ ] `C-CF-144` `literal` Prefix expansion is bounded at `1000` term-dictionary entries. `src: Core features, text pipeline`
- [ ] `C-CF-145` `capability` On reaching the prefix bound the response reports `exhaustiveTypo` as `false`. `src: Core features, text pipeline`
- [ ] `C-CF-146` `capability` A record matches when every remaining required query word matches. `src: Core features, text pipeline`
- [ ] `C-CF-147` `capability` Matching is per word across the whole record, never per attribute. `src: Core features, text pipeline`
- [ ] `C-CF-148` `literal` The query `wor hello` returns `t1`. `src: Core features, text pipeline`
- [ ] `C-CF-149` `literal` The queries `creme`, `crème` both return `t3`. `src: Core features, text pipeline`
- [ ] `C-CF-150` `literal` The query `strasse` returns `t7`. `src: Core features, text pipeline`
- [ ] `C-CF-151` `literal` The query `東京` returns `t6`. `src: Core features, text pipeline`
- [ ] `C-CF-152` `capability` Words in `optionalWords` are optional. `src: Core features, text pipeline`
- [ ] `C-CF-153` `capability` Every query word past the tenth is optional. `src: Core features, text pipeline`
- [ ] `C-CF-154` `literal` `removeWordsIfNoResults` takes `none`, `lastWords`, `firstWords`, `allOptional`. `src: Core features, text pipeline`
- [ ] `C-CF-155` `capability` Each removal round is a complete ranking pass of its own. `src: Core features, text pipeline`
- [ ] `C-CF-156` `constraint` Results of two removal rounds never interleave. `src: Core features, text pipeline`
- [ ] `C-CF-157` `capability` An earlier removal round's results come first, in full. `src: Core features, text pipeline`
- [ ] `C-CF-158` `capability` A facet the caller filters on is counted with its own clause pruned from the filter tree. `src: Core features, filters`
- [ ] `C-CF-159` `capability` Every other facet uses the full filter tree. `src: Core features, filters`
- [ ] `C-CF-160` `literal` The seeded `catalog` holds `10` red Acme, `5` blue Acme, `20` red Zeta, `1` blue Zeta. `src: Core features, filters`
- [ ] `C-CF-161` `literal` With `brand:acme`, `colour:red` ticked, the disjunctive counts are `brand.acme` `10`, `brand.zeta` `20`, `colour.red` `10`, `colour.blue` `5`. `src: Core features, filters`
- [ ] `C-CF-162` `constraint` A single grouped pass over the result set is refused as the source of a disjunctive count. `src: Core features, filters`
- [ ] `C-CF-163` `capability` A selected disjunctive value matching nothing under the pruned tree is returned with a count of zero. `src: Core features, filters`
- [ ] `C-CF-164` `capability` `exhaustiveFacetsCount` is reported `false` whenever a grouping reached `maxValuesPerFacet`. `src: Core features, filters`
- [ ] `C-CF-165` `capability` `facets_stats` for a filtered range is computed with that range removed. `src: Core features, filters`
- [ ] `C-CF-166` `capability` An unfiltered facet is counted by one grouped pass over records matching the query, every filter. `src: Core features, filters`
- [ ] `C-CF-167` `literal` The filter grammar carries a facet atom `attr:value`. `src: Core features, filters`
- [ ] `C-CF-168` `literal` The filter grammar carries numeric comparisons `<`, `<=`, `=`, `!=`, `>=`, `>`. `src: Core features, filters`
- [ ] `C-CF-169` `literal` The filter grammar carries a range atom `attr:number TO number`, inclusive at both ends. `src: Core features, filters`
- [ ] `C-CF-170` `literal` The filter grammar carries a tag atom `_tags:value`. `src: Core features, filters`
- [ ] `C-CF-171` `literal` Filter precedence is `NOT`, then `AND`, then `OR`. `src: Core features, filters`
- [ ] `C-CF-172` `literal` A disjunction of a conjunction parses with the conjunction bound tighter, as the pinned example shows. `src: Core features, filters`
- [ ] `C-CF-173` `ui` The interface renders the parenthesization back rather than echoing the filter string. `src: Core features, filters`
- [ ] `C-CF-174` `capability` An attribute absent from `attributesForFaceting` is rejected as invalid. `src: Core features, filters`
- [ ] `C-CF-175` `literal` `price > "10"` is rejected as invalid. `src: Core features, filters`
- [ ] `C-CF-176` `constraint` A numeric comparison against a quoted value is never a lexical compare. `src: Core features, filters`
- [ ] `C-CF-177` `capability` A filter outside the grammar is rejected, naming the offending span. `src: Core features, filters`
- [ ] `C-CF-178` `literal` A flat two-entry array means a conjunction of the two entries, as the pinned example shows. `src: Core features, filters`
- [ ] `C-CF-179` `literal` `[["a:1", "a:2"]]` means `a:1 OR a:2`. `src: Core features, filters`
- [ ] `C-CF-180` `literal` A nested entry beside a flat entry means a disjunction conjoined with the flat entry, as the pinned example shows. `src: Core features, filters`
- [ ] `C-CF-181` `literal` `["-a:1"]` means `NOT a:1`. `src: Core features, filters`
- [ ] `C-CF-182` `capability` A doubly nested filter array is rejected as invalid. `src: Core features, filters`
- [ ] `C-CF-183` `literal` `optionalFilters` entries take the bracketed form pinned in the literals table. `src: Core features, filters`
- [ ] `C-CF-184` `capability` An optional filter feeds the `filters` criterion rather than filtering. `src: Core features, filters`
- [ ] `C-CF-185` `literal` A negative optional filter, pinned in the literals table, credits records that do not match. `src: Core features, filters`
- [ ] `C-CF-186` `capability` Filtering happens before ranking, before facet counting. `src: Core features, filters`
- [ ] `C-CF-187` `capability` A filtered-out record contributes to no count except a disjunctive count on its own facet. `src: Core features, filters`
- [ ] `C-CF-188` `capability` `attributeForDistinct` names the attribute deduplication groups by. `src: Core features, filters`
- [ ] `C-CF-189` `capability` Deduplication runs after ranking, before pagination. `src: Core features, filters`
- [ ] `C-CF-190` `capability` A record removed by deduplication occupies no slot on a page. `src: Core features, filters`
- [ ] `C-CF-191` `capability` `nbHits` counts groups whenever `distinct` is above zero. `src: Core features, filters`
- [ ] `C-CF-192` `literal` On `shirts` with `distinct` `1`, page zero reports `nbHits` `300`, `nbPages` `15`. `src: Core features, filters`
- [ ] `C-CF-193` `literal` On `shirts` with `distinct` `1`, page zero returns twenty distinct `shirt_id` values. `src: Core features, filters`
- [ ] `C-CF-194` `literal` On `shirts` the red colour count is `300` by default. `src: Core features, filters`
- [ ] `C-CF-195` `literal` On `shirts` with `facetingAfterDistinct` on, the red colour count is `75`. `src: Core features, filters`
- [ ] `C-CF-196` `capability` A record promoted by a rule is exempt from deduplication. `src: Core features, filters`
- [ ] `C-CF-197` `capability` A promoted record consumes none of its group's quota. `src: Core features, filters`
- [ ] `C-CF-198` `capability` Facet value search answers over the values of one facet rather than over records. `src: Core features, filters`
- [ ] `C-CF-199` `capability` Facet value search uses prefix matching, the index's own typo settings. `src: Core features, filters`
- [ ] `C-CF-200` `capability` Only an attribute declared `searchable(attr)` is eligible for facet value search. `src: Core features, filters`
- [ ] `C-CF-201` `literal` The read path runs fourteen stages in a fixed order. `src: Core features, filters`
- [ ] `C-CF-202` `capability` Highlighting is applied to the returned page only. `src: Core features, filters`
- [ ] `C-CF-203` `capability` Every hit carries a highlight result mirroring the record's shape. `src: Core features, highlighting`
- [ ] `C-CF-204` `capability` A snippet result accompanies every attribute named in `attributesToSnippet`. `src: Core features, highlighting`
- [ ] `C-CF-205` `capability` Highlight tags are inserted into the original attribute value at the recorded offsets. `src: Core features, highlighting`
- [ ] `C-CF-206` `constraint` The value returned is the original text, never the folded text. `src: Core features, highlighting`
- [ ] `C-CF-207` `literal` The default highlight tags are `<em>`, `</em>`. `src: Core features, highlighting`
- [ ] `C-CF-208` `literal` `highlightPreTag`, `highlightPostTag` configure the highlight tags. `src: Core features, highlighting`
- [ ] `C-CF-209` `literal` A match level of `none`, `partial`, `full` accompanies each highlighted attribute. `src: Core features, highlighting`
- [ ] `C-CF-210` `capability` A match level of `full` means every query word matched inside that attribute. `src: Core features, highlighting`
- [ ] `C-CF-211` `capability` Two adjacent matches with nothing between merge into one tag pair. `src: Core features, highlighting`
- [ ] `C-CF-212` `literal` `red red red` under the query `red` returns three separate tag pairs. `src: Core features, highlighting`
- [ ] `C-CF-213` `literal` `hel` against `Hello World` wraps only the first three letters. `src: Core features, highlighting`
- [ ] `C-CF-214` `capability` A snippet is centred on the first match. `src: Core features, highlighting`
- [ ] `C-CF-215` `literal` `snippetEllipsisText` defaults to `...`. `src: Core features, highlighting`
- [ ] `C-CF-216` `capability` A snippet whose value fits whole carries no ellipsis on either side. `src: Core features, highlighting`
- [ ] `C-CF-217` `constraint` The service returns raw text with tags, escaping nothing itself. `src: Core features, highlighting`
- [ ] `C-CF-218` `capability` `nbHits` is exact when `exhaustiveNbHits` is true. `src: Core features, highlighting`
- [ ] `C-CF-219` `capability` `nbPages` is the lesser of the pages implied by `nbHits`, the pages implied by `paginationLimitedTo`. `src: Core features, highlighting`
- [ ] `C-CF-220` `literal` `paginationLimitedTo` defaults to `1000`. `src: Core features, highlighting`
- [ ] `C-CF-221` `literal` `page` is zero based; `hitsPerPage` runs `1` to `1000`. `src: Core features, highlighting`
- [ ] `C-CF-222` `capability` Mixing `page` with `offset` in one request is rejected as invalid. `src: Core features, highlighting`
- [ ] `C-CF-223` `capability` A page past `nbPages` returns an empty hit list, answering success. `src: Core features, highlighting`
- [ ] `C-CF-224` `capability` An offset past `paginationLimitedTo` is rejected as invalid. `src: Core features, highlighting`
- [ ] `C-CF-225` `literal` A `queryID` is thirty-two hexadecimal characters. `src: Core features, highlighting`
- [ ] `C-CF-226` `capability` The three honesty flags are computed rather than constant. `src: Core features, highlighting`
- [ ] `C-CF-227` `capability` Ranking info is returned only when `getRankingInfo` is on. `src: Core features, highlighting`
- [ ] `C-CF-228` `capability` Ranking info is recorded by the ranker as comparisons happen. `src: Core features, highlighting`
- [ ] `C-CF-229` `literal` The customers route holds `24` seeded customer stories. `src: Core features, the customers index`
- [ ] `C-CF-230` `literal` The customers search placeholder reads `Search for a customer story`. `src: Core features, the customers index`
- [ ] `C-CF-231` `literal` The five facet groups are `Features`, `Use Case`, `Industry`, `Region`, `Integration`. `src: Core features, the customers index`
- [ ] `C-CF-232` `capability` All five facet groups accept more than one value at once. `src: Core features, the customers index`
- [ ] `C-CF-233` `literal` The unfiltered industry counts are `Ecommerce` `10`, `Media` `5`, `Marketplace` `4`, `B2B` `3`, `Travel` `2`. `src: Core features, the customers index`
- [ ] `C-CF-234` `literal` The unfiltered region counts are `North America` `10`, `Europe` `8`, `Asia Pacific` `4`, `Latin America` `2`. `src: Core features, the customers index`
- [ ] `C-CF-235` `capability` The facet controls emit the nested array form. `src: Core features, the customers index`
- [ ] `C-CF-236` `literal` A `Clear All Filters` link appears once any facet is active. `src: Core features, the customers index`
- [ ] `C-CF-237` `capability` The facet selection lives in the address bar. `src: Core features, the customers index`
- [ ] `C-CF-238` `capability` Opening a copied filtered address restores the same selection, the same cards. `src: Core features, the customers index`
- [ ] `C-CF-239` `capability` Further stories load in place rather than paginating. `src: Core features, the customers index`
- [ ] `C-CF-240` `capability` Loading more preserves the back button. `src: Core features, the customers index`
- [ ] `C-CF-241` `capability` Loading more preserves the scroll position on return. `src: Core features, the customers index`
- [ ] `C-CF-242` `capability` Loading more announces the number of new results. `src: Core features, the customers index`
- [ ] `C-CF-243` `literal` The four plans are `Elevate`, `Grow Plus`, `Grow`, `Free`. `src: Core features, pricing`
- [ ] `C-CF-244` `literal` The two plan groups are `Annual plan`, `Pay as you go`. `src: Core features, pricing`
- [ ] `C-CF-245` `literal` `Grow Plus` carries a `NEW` badge. `src: Core features, pricing`
- [ ] `C-CF-246` `literal` The four plan subtitles are pinned in the literals table. `src: Core features, pricing`
- [ ] `C-CF-247` `literal` The plan actions read `Start for free`, `Build for free`, `Request pricing`. `src: Core features, pricing`
- [ ] `C-CF-248` `literal` The `Grow` metering line reads `10K search requests /month included then $0.50 per additional 1K search requests`. `src: Core features, pricing`
- [ ] `C-CF-249` `literal` The `Grow` records line reads `100K records included then $0.40`. `src: Core features, pricing`
- [ ] `C-CF-250` `literal` The `Free` body reads `Get started building experiences ever with some of our features.`. `src: Core features, pricing`
- [ ] `C-CF-251` `literal` The `Free` note reads `No credit card required.`. `src: Core features, pricing`
- [ ] `C-CF-252` `literal` Money is held as integer minor units in `usd`: `$0.50` is `50`, `$0.40` is `40`. `src: Core features, pricing`
- [ ] `C-CF-253` `constraint` Nothing on the pricing route charges anything. `src: Core features, pricing`
- [ ] `C-CF-254` `literal` The jump link reads `See full features grid`. `src: Core features, pricing`
- [ ] `C-CF-255` `literal` The grid heading reads `Detailed feature comparison`. `src: Core features, pricing`
- [ ] `C-CF-256` `literal` The seven grid categories are `Search`, `Analytics`, `UI Components`, `Integrations & Data`, `Crawler`, `Infrastructure & Plan Limits`, `Support & Success`. `src: Core features, pricing`
- [ ] `C-CF-257` `ui` A grid cell holds a present marker, an absent marker, or a limit as text. `src: Core features, pricing`
- [ ] `C-CF-258` `literal` Two measured grid limits read `10 per index`, `10,000 per index`. `src: Core features, pricing`
- [ ] `C-CF-259` `ui` The plan header row stays visible as the grid body scrolls. `src: Core features, pricing`
- [ ] `C-CF-260` `literal` Six measured grid rows are `Rules`, `Visual Editor`, `Manual Synonyms`, `Virtual Replicas (Relevant Sort)`, `AI Synonyms`, `Query Categorization`. `src: Core features, pricing`
- [ ] `C-CF-261` `constraint` `AI Synonyms` shows absent in every plan column. `src: Core features, pricing`
- [ ] `C-CF-262` `constraint` `Query Categorization` shows absent in every plan column. `src: Core features, pricing`
- [ ] `C-CF-263` `literal` The questions accordion is headed `Pricing FAQs`. `src: Core features, pricing`
- [ ] `C-CF-264` `literal` The first pricing question reads `What is a search request?`. `src: Core features, pricing`
- [ ] `C-CF-265` `ui` The pricing accordion opens one question at a time. `src: Core features, pricing`
- [ ] `C-CF-266` `literal` The demo request fields are `First Name`, `Last Name`, `Business Email`, `Phone`, `Company`, `Country`. `src: Core features, the demo request`
- [ ] `C-CF-267` `capability` Every demo request field is required. `src: Core features, the demo request`
- [ ] `C-CF-268` `ui` Every demo request label is visible, persistent. `src: Core features, the demo request`
- [ ] `C-CF-269` `literal` The country list begins `Select...`, then `United States`, then every country alphabetically from `Afghanistan`. `src: Core features, the demo request`
- [ ] `C-CF-270` `literal` The demo request submit reads `Get In Touch`. `src: Core features, the demo request`
- [ ] `C-CF-271` `capability` A complete demo request stores exactly one row carrying the six values. `src: Core features, the demo request`
- [ ] `C-CF-272` `literal` A stored demo request carries a status of `received`. `src: Core features, the demo request`
- [ ] `C-CF-273` `ui` A successful submission replaces the form with a full-page confirmation naming the company. `src: Core features, the demo request`
- [ ] `C-CF-274` `data` A stored demo request returns the same six values after a restart. `src: Core features, the demo request`
- [ ] `C-CF-275` `capability` Demo request validation runs on blur, again on submit. `src: Core features, the demo request`
- [ ] `C-CF-276` `ui` An invalid field shows its error below itself in the failure colour. `src: Core features, the demo request`
- [ ] `C-CF-277` `ui` An invalid submit renders an error summary above the form linking to each failing field. `src: Core features, the demo request`
- [ ] `C-CF-278` `ui` An invalid submit moves focus to the error summary. `src: Core features, the demo request`
- [ ] `C-CF-279` `capability` An invalid submit writes nothing. `src: Core features, the demo request`
- [ ] `C-CF-280` `capability` A failed submission preserves the typed values. `src: Core features, the demo request`
- [ ] `C-CF-281` `ui` The submitting state disables the submit control, announcing progress. `src: Core features, the demo request`
- [ ] `C-CF-282` `capability` The newsletter takes one email address, storing one signup row. `src: Core features, the demo request`
- [ ] `C-CF-283` `capability` The newsletter rejects a malformed address inline, writing nothing. `src: Core features, the demo request`
- [ ] `C-CF-284` `ui` The newsletter states are shown inline rather than replacing the footer. `src: Core features, the demo request`
- [ ] `C-CF-285` `capability` A write batch is not a transaction. `src: Core features, ingestion`
- [ ] `C-CF-286` `capability` Batch operations are applied in array order. `src: Core features, ingestion`
- [ ] `C-CF-287` `capability` A rejected batch operation leaves a null at its position in the result list. `src: Core features, ingestion`
- [ ] `C-CF-288` `literal` A batch of `1000` records carrying one over-size record applies `999`. `src: Core features, ingestion`
- [ ] `C-CF-289` `literal` `addObject` creates a second object with a new server-assigned `objectID` when one exists. `src: Core features, ingestion`
- [ ] `C-CF-290` `literal` `updateObject` replaces every attribute. `src: Core features, ingestion`
- [ ] `C-CF-291` `literal` `updateObject` reports not found for an absent object, leaving the batch running. `src: Core features, ingestion`
- [ ] `C-CF-292` `literal` `partialUpdateObject` merges at the top level only. `src: Core features, ingestion`
- [ ] `C-CF-293` `literal` `partialUpdateObjectNoCreate` is a no-op for an absent object. `src: Core features, ingestion`
- [ ] `C-CF-294` `literal` `deleteObject` is a no-op for an absent object. `src: Core features, ingestion`
- [ ] `C-CF-295` `literal` `clear` empties the index, keeping settings, synonyms, rules. `src: Core features, ingestion`
- [ ] `C-CF-296` `constraint` An object value in a partial update replaces the whole nested object. `src: Core features, ingestion`
- [ ] `C-CF-297` `literal` The conditional operators are `Increment`, `Decrement`, `IncrementFrom`, `IncrementSet`, `Add`, `Remove`, `AddUnique`. `src: Core features, ingestion`
- [ ] `C-CF-298` `capability` `Increment` treats a missing attribute as zero. `src: Core features, ingestion`
- [ ] `C-CF-299` `capability` `Increment` rejects a non-numeric attribute. `src: Core features, ingestion`
- [ ] `C-CF-300` `literal` `IncrementFrom` `4` applied twice leaves `5`, rejecting the second attempt. `src: Core features, ingestion`
- [ ] `C-CF-301` `literal` `IncrementSet` `7` followed by `IncrementSet` `6` leaves `7`. `src: Core features, ingestion`
- [ ] `C-CF-302` `capability` `Add` appends; `AddUnique` appends unless already present; `Remove` removes every equal element. `src: Core features, ingestion`
- [ ] `C-CF-303` `capability` A `taskID` is monotonic per index. `src: Core features, ingestion`
- [ ] `C-CF-304` `constraint` A `taskID` carries no meaning across two indices. `src: Core features, ingestion`
- [ ] `C-CF-305` `capability` Tasks on one index are applied in `taskID` order. `src: Core features, ingestion`
- [ ] `C-CF-306` `capability` A task reports published once visible to every reader. `src: Core features, ingestion`
- [ ] `C-CF-307` `capability` A failed task carries its error on the task itself. `src: Core features, ingestion`
- [ ] `C-CF-308` `literal` Task polling backs off from `100` milliseconds, doubling, capped at `5` seconds, giving up at `300` seconds. `src: Core features, ingestion`
- [ ] `C-CF-309` `capability` A rebuild happens beside the live index, swapping in one motion. `src: Core features, ingestion`
- [ ] `C-CF-310` `constraint` A temporary index inherits nothing. `src: Core features, ingestion`
- [ ] `C-CF-311` `capability` Settings, synonyms, rules are copied onto a temporary index explicitly. `src: Core features, ingestion`
- [ ] `C-CF-312` `capability` A query in flight finishes against the generation on which the query began. `src: Core features, ingestion`
- [ ] `C-CF-313` `constraint` No query sees a mixture of two generations. `src: Core features, ingestion`
- [ ] `C-CF-314` `capability` A move destroys the destination index, its settings, its synonyms, its rules. `src: Core features, ingestion`
- [ ] `C-CF-315` `constraint` The source name does not exist after a move. `src: Core features, ingestion`
- [ ] `C-CF-316` `capability` Replicas survive a move, rebuilding from the new generation. `src: Core features, ingestion`
- [ ] `C-CF-317` `capability` Deleting an object marks the object dead in the current generation. `src: Core features, ingestion`
- [ ] `C-CF-318` `capability` Dead records are filtered after retrieval, before ranking. `src: Core features, ingestion`
- [ ] `C-CF-319` `literal` Compaction runs when dead records exceed a fifth of the generation. `src: Core features, ingestion`
- [ ] `C-CF-320` `capability` The record count excludes a deleted record from the moment the delete task publishes. `src: Core features, ingestion`
- [ ] `C-CF-321` `constraint` A delete by filter is never presented as a guarantee of an empty index. `src: Core features, ingestion`
- [ ] `C-CF-322` `literal` An idempotency key runs `16` to `128` characters. `src: Core features, ingestion`
- [ ] `C-CF-323` `literal` An idempotency record lives for `24` hours. `src: Core features, ingestion`
- [ ] `C-CF-324` `capability` A repeated idempotency key with the same body returns the stored response verbatim. `src: Core features, ingestion`
- [ ] `C-CF-325` `capability` A replayed idempotent request enqueues nothing. `src: Core features, ingestion`
- [ ] `C-CF-326` `capability` A repeated idempotency key with a different body is rejected as invalid. `src: Core features, ingestion`
- [ ] `C-CF-327` `constraint` A second body under a reused idempotency key is never applied. `src: Core features, ingestion`
- [ ] `C-CF-328` `capability` A key whose first request is in flight holds the second for up to five seconds, then reports a conflict. `src: Core features, ingestion`
- [ ] `C-CF-329` `literal` A record over `100` kilobytes serialized is rejected. `src: Core features, ingestion`
- [ ] `C-CF-330` `literal` A batch over `1000` operations is rejected. `src: Core features, ingestion`
- [ ] `C-CF-331` `literal` A batch over `10` megabytes is rejected. `src: Core features, ingestion`
- [ ] `C-CF-332` `literal` A query longer than `512` characters is truncated, reported as truncated. `src: Core features, ingestion`
- [ ] `C-CF-333` `literal` `maxValuesPerFacet` is itself capped at `1000`. `src: Core features, ingestion`
- [ ] `C-CF-334` `literal` Attribute nesting deeper than `6` is rejected as invalid. `src: Core features, ingestion`
- [ ] `C-CF-335` `literal` More than `100` distinct facet attributes per index is rejected as invalid. `src: Core features, ingestion`
- [ ] `C-CF-336` `capability` Every limit is enforced at the front door. `src: Core features, ingestion`
- [ ] `C-CF-337` `literal` The five synonym types are `multiWay`, `oneWay`, `altCorrection1`, `altCorrection2`, `placeholder`. `src: Core features, merchandising`
- [ ] `C-CF-338` `capability` A `multiWay` synonym expands any one of a list to all of the list. `src: Core features, merchandising`
- [ ] `C-CF-339` `capability` A `oneWay` synonym never matches in reverse. `src: Core features, merchandising`
- [ ] `C-CF-340` `capability` An `altCorrection1` synonym matches with one typo already spent. `src: Core features, merchandising`
- [ ] `C-CF-341` `capability` An `altCorrection2` synonym matches with two typos already spent. `src: Core features, merchandising`
- [ ] `C-CF-342` `capability` A `placeholder` synonym lets a record token stand for any value of a named placeholder. `src: Core features, merchandising`
- [ ] `C-CF-343` `literal` `bike` expanding to `mountain bike` matches only records carrying the two words adjacent. `src: Core features, merchandising`
- [ ] `C-CF-344` `capability` Synonym expansion happens after tokenization, before retrieval. `src: Core features, merchandising`
- [ ] `C-CF-345` `constraint` Synonyms are not carried by a move unless copied explicitly. `src: Core features, merchandising`
- [ ] `C-CF-346` `capability` A rule applies only when its validity window contains the request time. `src: Core features, merchandising`
- [ ] `C-CF-347` `capability` Rule conditions are evaluated against the parsed query. `src: Core features, merchandising`
- [ ] `C-CF-348` `literal` Rule anchoring takes `is`, `startsWith`, `endsWith`, `contains`. `src: Core features, merchandising`
- [ ] `C-CF-349` `capability` A facet-capture pattern captures a token that is a value of that facet. `src: Core features, merchandising`
- [ ] `C-CF-350` `capability` Matching rules sort by rank number ascending, then identifier ascending. `src: Core features, merchandising`
- [ ] `C-CF-351` `capability` A later rule overwrites an earlier rule on the same parameter. `src: Core features, merchandising`
- [ ] `C-CF-352` `capability` Promote lists concatenate, a repeated object keeping its first position. `src: Core features, merchandising`
- [ ] `C-CF-353` `capability` Hides are applied last. `src: Core features, merchandising`
- [ ] `C-CF-354` `capability` A hide removes an object a promote named. `src: Core features, merchandising`
- [ ] `C-CF-355` `capability` Two promotions to one position resolve by rule order, the loser taking the next free position. `src: Core features, merchandising`
- [ ] `C-CF-356` `capability` Promotion positions are zero based against the final list after deduplication. `src: Core features, merchandising`
- [ ] `C-CF-357` `capability` Promotions are honoured on the first page only. `src: Core features, merchandising`
- [ ] `C-CF-358` `capability` A promotion beyond the page size is dropped, reported as not applied. `src: Core features, merchandising`
- [ ] `C-CF-359` `capability` A filter removes a record no promotion can restore. `src: Core features, merchandising`
- [ ] `C-CF-360` `literal` Personalization event weights are view `1`, click `3`, conversion `10`. `src: Core features, merchandising`
- [ ] `C-CF-361` `literal` Personalization affinity decays by half every `30` days by default. `src: Core features, merchandising`
- [ ] `C-CF-362` `capability` The personalization boost enters the cascade as a term of the `filters` criterion. `src: Core features, merchandising`
- [ ] `C-CF-363` `constraint` The personalization boost never multiplies a final number. `src: Core features, merchandising`
- [ ] `C-CF-364` `constraint` The personalization boost never acts above `typo`, `words`, `proximity`. `src: Core features, merchandising`
- [ ] `C-CF-365` `capability` An exact match of a typed brand outranks a typo match of a preferred brand. `src: Core features, merchandising`
- [ ] `C-CF-366` `literal` `personalizationImpact` runs `0` to `100`, defaulting to `100`. `src: Core features, merchandising`
- [ ] `C-CF-367` `capability` At zero impact personalization is inert, logging still. `src: Core features, merchandising`
- [ ] `C-CF-368` `literal` A split run carries a control index, a challenger, a traffic split `1` to `99`, a window. `src: Core features, merchandising`
- [ ] `C-CF-369` `capability` Variant assignment is a stable hash of the run identifier plus the user token. `src: Core features, merchandising`
- [ ] `C-CF-370` `capability` One user token gets one variant for the whole run, across devices. `src: Core features, merchandising`
- [ ] `C-CF-371` `capability` A request carrying no user token runs the control. `src: Core features, merchandising`
- [ ] `C-CF-372` `constraint` A request carrying no user token is excluded from the analysis. `src: Core features, merchandising`
- [ ] `C-CF-373` `capability` The variant identifier is stamped on the query event. `src: Core features, merchandising`
- [ ] `C-CF-374` `capability` An interaction event inherits the variant identifier from the query identity. `src: Core features, merchandising`
- [ ] `C-CF-375` `constraint` A variant is never re-derived at analysis time. `src: Core features, merchandising`
- [ ] `C-CF-376` `capability` Stopping a split run freezes assignment, deleting no events. `src: Core features, merchandising`
- [ ] `C-CF-377` `literal` Control precedence runs rules, synonyms, filters, the cascade, personalization, promotions, hides, deduplication. `src: Core features, merchandising`
- [ ] `C-CF-378` `capability` A record in a vector-enabled index carries a vector computed from a template over the record's attributes. `src: Core features, hybrid retrieval`
- [ ] `C-CF-379` `literal` A vector dimension is fixed at index creation between `256`, `1536`. `src: Core features, hybrid retrieval`
- [ ] `C-CF-380` `constraint` A vector dimension is immutable after index creation. `src: Core features, hybrid retrieval`
- [ ] `C-CF-381` `capability` Vectors are stored normalized so similarity is a dot product. `src: Core features, hybrid retrieval`
- [ ] `C-CF-382` `capability` Each vector is stamped with the identity of the routine that produced the vector. `src: Core features, hybrid retrieval`
- [ ] `C-CF-383` `capability` A mixed-identity index reports the vector index as stale, falling back to keyword-only results. `src: Core features, hybrid retrieval`
- [ ] `C-CF-384` `capability` Changing the vector routine creates a new generation, re-embedding rather than rewriting in place. `src: Core features, hybrid retrieval`
- [ ] `C-CF-385` `literal` Graph parameters default to neighbours `16`, build-time breadth `200`, query breadth `64`. `src: Core features, hybrid retrieval`
- [ ] `C-CF-386` `literal` Query breadth is raisable per query up to `512`. `src: Core features, hybrid retrieval`
- [ ] `C-CF-387` `capability` A fixed seed per index makes a graph build reproducible. `src: Core features, hybrid retrieval`
- [ ] `C-CF-388` `capability` Filters are applied during the graph walk. `src: Core features, hybrid retrieval`
- [ ] `C-CF-389` `constraint` Filters are never applied after the graph walk has finished. `src: Core features, hybrid retrieval`
- [ ] `C-CF-390` `capability` The walk continues until enough surviving candidates are found, or the graph is exhausted. `src: Core features, hybrid retrieval`
- [ ] `C-CF-391` `literal` Fusion uses a constant of `60`, a keyword coefficient `1.0`, a vector coefficient `1.0`. `src: Core features, hybrid retrieval`
- [ ] `C-CF-392` `capability` Fusion combines the two lists by rank. `src: Core features, hybrid retrieval`
- [ ] `C-CF-393` `constraint` Fusion never normalizes the two lists onto a common range. `src: Core features, hybrid retrieval`
- [ ] `C-CF-394` `capability` A document absent from one list contributes nothing for that list. `src: Core features, hybrid retrieval`
- [ ] `C-CF-395` `capability` A record matching every query word exactly is never ranked below position ten by fusion. `src: Core features, hybrid retrieval`
- [ ] `C-CF-396` `capability` A lifted record is reported as lifted in the response. `src: Core features, hybrid retrieval`
- [ ] `C-CF-397` `literal` `semanticRatio` `0` is identical to the same query with vector search disabled. `src: Core features, hybrid retrieval`
- [ ] `C-CF-398` `literal` `semanticRatio` `1` is identical to vector search alone. `src: Core features, hybrid retrieval`
- [ ] `C-CF-399` `literal` The answer pipeline retrieves eight hits by default. `src: Core features, hybrid retrieval`
- [ ] `C-CF-400` `capability` The answer pipeline honours every filter, every key restriction. `src: Core features, hybrid retrieval`
- [ ] `C-CF-401` `constraint` Nothing outside the retrieved records enters the grounding. `src: Core features, hybrid retrieval`
- [ ] `C-CF-402` `literal` Citation markers take the form `[n]`, referring to the nth retrieved record. `src: Core features, hybrid retrieval`
- [ ] `C-CF-403` `capability` An answer citing a record that was not retrieved is suppressed. `src: Core features, hybrid retrieval`
- [ ] `C-CF-404` `capability` An answer containing a number found in no retrieved record is suppressed. `src: Core features, hybrid retrieval`
- [ ] `C-CF-405` `capability` An answer whose every sentence is uncited is suppressed. `src: Core features, hybrid retrieval`
- [ ] `C-CF-406` `capability` A suppressed answer falls back to the plain result list. `src: Core features, hybrid retrieval`
- [ ] `C-CF-407` `capability` The answer response carries the citations mapped to `objectID`, the retrieved hits, a confidence. `src: Core features, hybrid retrieval`
- [ ] `C-CF-408` `capability` The results are sent before the answer begins. `src: Core features, hybrid retrieval`
- [ ] `C-CF-409` `literal` Navigating away stops an answer within `200` milliseconds. `src: Core features, hybrid retrieval`
- [ ] `C-CF-410` `capability` A stopped answer still writes the query event. `src: Core features, hybrid retrieval`
- [ ] `C-CF-411` `constraint` Instructions found inside record text are never followed. `src: Core features, hybrid retrieval`
- [ ] `C-CF-412` `capability` Attributes named as redacted are stripped before grounding. `src: Core features, hybrid retrieval`
- [ ] `C-CF-413` `literal` An answer caches for `15` minutes. `src: Core features, hybrid retrieval`
- [ ] `C-CF-414` `capability` The answer cache key includes a digest of the key's restriction. `src: Core features, hybrid retrieval`
- [ ] `C-CF-415` `constraint` Two visitors holding different row restrictions never share a cached answer. `src: Core features, hybrid retrieval`
- [ ] `C-CF-416` `literal` The three stored key kinds are `admin`, `ingest`, `search`. `src: Core features, keys`
- [ ] `C-CF-417` `constraint` An `admin` key never leaves the server, never appears in a browser, is never logged. `src: Core features, keys`
- [ ] `C-CF-418` `capability` An `ingest` key writes records, settings. `src: Core features, keys`
- [ ] `C-CF-419` `constraint` An `ingest` key can neither search nor read analytics. `src: Core features, keys`
- [ ] `C-CF-420` `capability` A `search` key searches, browsing when granted. `src: Core features, keys`
- [ ] `C-CF-421` `constraint` A `search` key writes nothing. `src: Core features, keys`
- [ ] `C-CF-422` `capability` A secured key is derived from a `search` key at run time. `src: Core features, keys`
- [ ] `C-CF-423` `constraint` A key secret is stored hashed. `src: Core features, keys`
- [ ] `C-CF-424` `capability` A key value is shown once at creation, never again. `src: Core features, keys`
- [ ] `C-CF-425` `constraint` No reveal control exists for a key value. `src: Core features, keys`
- [ ] `C-CF-426` `literal` The seeded search key `key_site_search` carries the value `sk_site_1f6b2d8e4a`. `src: Core features, keys`
- [ ] `C-CF-427` `literal` `key_site_search` is scoped to `site_content`, `customer_stories`. `src: Core features, keys`
- [ ] `C-CF-428` `literal` The seeded search key `key_story_search` carries the value `sk_story_3c9a7e51b2`. `src: Core features, keys`
- [ ] `C-CF-429` `literal` `key_story_search` is scoped to `customer_stories` alone. `src: Core features, keys`
- [ ] `C-CF-430` `literal` The seeded ingest key `key_ingest_demo` carries the value `ik_demo_74d2c0a9f1`. `src: Core features, keys`
- [ ] `C-CF-431` `capability` `key_story_search` requesting `site_content` is refused. `src: Core features, keys`
- [ ] `C-CF-432` `capability` Secured key restrictions are url-encoded, sorted by name ascending, joined with `&`. `src: Core features, keys`
- [ ] `C-CF-433` `literal` A secured key restriction string looks like `filters=industry%3AEcommerce&userToken=u_1029&validUntil=1767225600`. `src: Core features, keys`
- [ ] `C-CF-434` `capability` The secured key signature is the hexadecimal HMAC-SHA256 of the encoded restriction string. `src: Core features, keys`
- [ ] `C-CF-435` `capability` The secured key is the base64 of the signature followed by the restriction string. `src: Core features, keys`
- [ ] `C-CF-436` `literal` The first `64` characters of a decoded secured key are the signature. `src: Core features, keys`
- [ ] `C-CF-437` `capability` The signature is recomputed against every active parent search key of the application. `src: Core features, keys`
- [ ] `C-CF-438` `capability` A rotated parent key leaves live secured keys working. `src: Core features, keys`
- [ ] `C-CF-439` `capability` A secured key whose `validUntil` has passed is refused. `src: Core features, keys`
- [ ] `C-CF-440` `capability` A key's `filters` restriction is combined with the request's filters by conjunction. `src: Core features, keys`
- [ ] `C-CF-441` `constraint` A request's filters never replace a key's filters. `src: Core features, keys`
- [ ] `C-CF-442` `constraint` A key's filters are never combined with a request's by disjunction. `src: Core features, keys`
- [ ] `C-CF-443` `capability` A key's index restriction is intersected with the requested index. `src: Core features, keys`
- [ ] `C-CF-444` `capability` A `userToken` carried by a key overrides any `userToken` in the request. `src: Core features, keys`
- [ ] `C-CF-445` `literal` A secured key restricted to `industry:Ecommerce` asked for `industry:Media` returns zero hits. `src: Core features, keys`
- [ ] `C-CF-446` `literal` The authorization order runs key present, signature valid, not expired, referer, action, index, rate, request limits. `src: Core features, keys`
- [ ] `C-CF-447` `constraint` A refusal for an out-of-scope index is indistinguishable from a refusal for an absent index. `src: Core features, keys`
- [ ] `C-CF-448` `literal` The rate bucket holds `100` requests, refilling at `10` per second. `src: Core features, keys`
- [ ] `C-CF-449` `literal` Rate costs are `1` for a search, `5` for a batch write, `20` for starting an answer. `src: Core features, keys`
- [ ] `C-CF-450` `capability` Rate refill is continuous, computed from elapsed time on each request. `src: Core features, keys`
- [ ] `C-CF-451` `constraint` A fixed window that resets on the second boundary is refused as a rate mechanism. `src: Core features, keys`
- [ ] `C-CF-452` `capability` The quota is per workspace per calendar month in UTC. `src: Core features, keys`
- [ ] `C-CF-453` `literal` One search unit is one search request, or one facet-value search. `src: Core features, keys`
- [ ] `C-CF-454` `literal` One record unit is one stored record, sampled hourly, billed on the maximum. `src: Core features, keys`
- [ ] `C-CF-455` `literal` One answer unit is one thousand generated tokens, rounded up per request. `src: Core features, keys`
- [ ] `C-CF-456` `literal` At `80` percent of quota a response carries a quota warning header. `src: Core features, keys`
- [ ] `C-CF-457` `capability` At full quota search continues, writes being refused. `src: Core features, keys`
- [ ] `C-CF-458` `capability` A rate refusal carries a retry hint in whole seconds. `src: Core features, keys`
- [ ] `C-CF-459` `data` Every write, key creation, settings change, rule change writes an audit record. `src: Core features, keys`
- [ ] `C-CF-460` `data` An audit record carries the acting key identifier, the action, the index, a before-after digest, the request identifier, the timestamp. `src: Core features, keys`
- [ ] `C-CF-461` `constraint` Audit records are append-only. `src: Core features, keys`
- [ ] `C-CF-462` `capability` Audit records are readable only with an `admin` key. `src: Core features, keys`
- [ ] `C-CF-463` `literal` Audit retention has a floor of `90` days on every plan. `src: Core features, keys`
- [ ] `C-CF-464` `literal` Event intake accepts `click`, `conversion`, `view`. `src: Core features, events`
- [ ] `C-CF-465` `capability` Event intake answers success even when individual events are dropped. `src: Core features, events`
- [ ] `C-CF-466` `capability` Event intake reports the count accepted. `src: Core features, events`
- [ ] `C-CF-467` `literal` An event older than `4` days is dropped as stale. `src: Core features, events`
- [ ] `C-CF-468` `capability` A click carrying a query identity without positions is dropped as malformed. `src: Core features, events`
- [ ] `C-CF-469` `literal` An event naming more than `20` objects is dropped. `src: Core features, events`
- [ ] `C-CF-470` `capability` An event carrying no user token is dropped. `src: Core features, events`
- [ ] `C-CF-471` `capability` An event naming an unknown index is dropped. `src: Core features, events`
- [ ] `C-CF-472` `capability` A timestamp more than one hour ahead is clamped to the receipt time. `src: Core features, events`
- [ ] `C-CF-473` `capability` A click carrying a query identity is attributed to that search. `src: Core features, events`
- [ ] `C-CF-474` `constraint` Attributed figures are never mixed with unattributed figures. `src: Core features, events`
- [ ] `C-CF-475` `literal` The attribution window is `24` hours from the query event. `src: Core features, events`
- [ ] `C-CF-476` `literal` The conversion attribution window extends to `30` days for an authenticated user token. `src: Core features, events`
- [ ] `C-CF-477` `capability` Two events sharing user token, type, object, query identity, whole minute are one event. `src: Core features, events`
- [ ] `C-CF-478` `capability` A late event triggers a recomputation of its hour. `src: Core features, events`
- [ ] `C-CF-479` `literal` A recomputation reaches back `4` days. `src: Core features, events`
- [ ] `C-CF-480` `constraint` A rollup is never an incremented counter. `src: Core features, events`
- [ ] `C-CF-481` `literal` The five rollup tables are searches, queries, hits, filters, variants, each per index per hour. `src: Core features, events`
- [ ] `C-CF-482` `capability` Hour boundaries are UTC, converted for display. `src: Core features, events`
- [ ] `C-CF-483` `literal` Click-through rate divides attributed clicks by searches that returned at least one hit. `src: Core features, events`
- [ ] `C-CF-484` `literal` Conversion rate uses the same denominator as click-through rate. `src: Core features, events`
- [ ] `C-CF-485` `literal` No-results rate divides searches returning zero hits by all searches. `src: Core features, events`
- [ ] `C-CF-486` `literal` Average click position is the mean of reported positions over attributed clicks, one based. `src: Core features, events`
- [ ] `C-CF-487` `constraint` A distinct user count is never the sum of the sub-period counts. `src: Core features, events`
- [ ] `C-CF-488` `capability` A wider-period distinct count is computed by merging sketches. `src: Core features, events`
- [ ] `C-CF-489` `ui` Every distinct count is marked approximate in the figure itself. `src: Core features, events`
- [ ] `C-CF-490` `capability` `/console` opens on an application picker. `src: Core features, the console`
- [ ] `C-CF-491` `capability` The application picker redirects through when the account holds exactly one application. `src: Core features, the console`
- [ ] `C-CF-492` `ui` A left rail carries the application switcher, eleven destinations. `src: Core features, the console`
- [ ] `C-CF-493` `ui` The top bar carries an index switcher that is a search over index names. `src: Core features, the console`
- [ ] `C-CF-494` `ui` Every console screen reading data shows the generation read, the age of that read. `src: Core features, the console`
- [ ] `C-CF-495` `capability` The record browser walks the index with a forward-only cursor. `src: Core features, the console`
- [ ] `C-CF-496` `ui` The record browser offers a visible way to start over. `src: Core features, the console`
- [ ] `C-CF-497` `data` Record browser columns are persisted per index per member. `src: Core features, the console`
- [ ] `C-CF-498` `capability` An inline edit writes a partial update, showing the returned `taskID`. `src: Core features, the console`
- [ ] `C-CF-499` `capability` An inline edit polls the returned task. `src: Core features, the console`
- [ ] `C-CF-500` `capability` A delete requires typing the `objectID`. `src: Core features, the console`
- [ ] `C-CF-501` `ui` A raw record view is read only, carrying a copy control. `src: Core features, the console`
- [ ] `C-CF-502` `data` A value edited inline is the value a fresh page load shows. `src: Core features, the console`
- [ ] `C-CF-503` `data` A value edited inline is the value a search returns. `src: Core features, the console`
- [ ] `C-CF-504` `literal` The record browser renders `200` rows without stalling. `src: Core features, the console`
- [ ] `C-CF-505` `capability` The record browser does not re-request a page already fetched. `src: Core features, the console`
- [ ] `C-CF-506` `ui` The search preview holds three panes. `src: Core features, the console`
- [ ] `C-CF-507` `ui` The preview filter builder emits the nested array form. `src: Core features, the console`
- [ ] `C-CF-508` `ui` The preview filter builder renders the filter back as prose. `src: Core features, the console`
- [ ] `C-CF-509` `ui` The preview centre pane shows the position number per hit. `src: Core features, the console`
- [ ] `C-CF-510` `ui` The preview right pane toggles each facet between conjunctive counting, disjunctive counting. `src: Core features, the console`
- [ ] `C-CF-511` `ui` A per-hit disclosure shows one row per ranking criterion. `src: Core features, the console`
- [ ] `C-CF-512` `ui` A per-hit disclosure shows the hit's own value beside the value of the hit above. `src: Core features, the console`
- [ ] `C-CF-513` `ui` A per-hit disclosure marks the criterion where the two first differed. `src: Core features, the console`
- [ ] `C-CF-514` `capability` `getRankingInfo` is on by default in the preview, off everywhere else. `src: Core features, the console`
- [ ] `C-CF-515` `ui` The preview renders degradation flags as a visible banner. `src: Core features, the console`
- [ ] `C-CF-516` `ui` The preview lists the rules applied to the query, each linking to an editor. `src: Core features, the console`
- [ ] `C-CF-517` `capability` The preview comparison mode runs one query against two settings sets side by side. `src: Core features, the console`
- [ ] `C-CF-518` `ui` The comparison mode highlights the ordering differences. `src: Core features, the console`
- [ ] `C-CF-519` `capability` Dragging a result to a position writes a rule. `src: Core features, the console`
- [ ] `C-CF-520` `constraint` Dragging a result never writes a separate pinning object. `src: Core features, the console`
- [ ] `C-CF-521` `capability` Hiding a hit writes a hide. `src: Core features, the console`
- [ ] `C-CF-522` `capability` Adding a banner writes user data on the consequence. `src: Core features, the console`
- [ ] `C-CF-523` `capability` Boosting a category for a query writes an optional filter. `src: Core features, the console`
- [ ] `C-CF-524` `ui` The merchandising editor shows the precedence list with the active steps marked. `src: Core features, the console`
- [ ] `C-CF-525` `capability` A rule carries a validity window, defaulting to starting now with no end. `src: Core features, the console`
- [ ] `C-CF-526` `capability` Analytics screens read only the rollup tables. `src: Core features, the console`
- [ ] `C-CF-527` `constraint` No analytics screen queries raw events. `src: Core features, the console`
- [ ] `C-CF-528` `ui` The analytics overview shows searches, users, click-through rate, no-results rate. `src: Core features, the console`
- [ ] `C-CF-529` `ui` The analytics overview states its denominators beside each figure. `src: Core features, the console`
- [ ] `C-CF-530` `ui` The top searches screen shows the normalized query, holding raw variants behind a disclosure. `src: Core features, the console`
- [ ] `C-CF-531` `ui` The no-results screen offers a control that opens the rule editor pre-filled. `src: Core features, the console`
- [ ] `C-CF-532` `ui` The results insight screen joins to the record browser. `src: Core features, the console`
- [ ] `C-CF-533` `ui` A date range is inclusive of both ends, labelled with the timezone. `src: Core features, the console`
- [ ] `C-CF-534` `ui` The keys screen carries a secured-key worked example generated live from the selected parent key. `src: Core features, the console`
- [ ] `C-CF-535` `ui` The members screen renders the role matrix. `src: Core features, the console`
- [ ] `C-CF-536` `ui` The tasks screen lists the write queue per index with identifier, kind, status, accept time, publish time. `src: Core features, the console`
- [ ] `C-CF-537` `ui` A failed task shows the error, the operation that caused the error. `src: Core features, the console`
- [ ] `C-CF-538` `constraint` The console never waits synchronously for a task inside a form submission. `src: Core features, the console`
- [ ] `C-CF-539` `constraint` The console never searches where a cursor walk is specified. `src: Core features, the console`
- [ ] `C-CF-540` `constraint` The console never stores an `admin` key in the browser. `src: Core features, the console`
- [ ] `C-CF-541` `constraint` The console session is not an application key. `src: Core features, the console`
- [ ] `C-CF-542` `constraint` The console never shows a sketch-derived figure without an approximation marker. `src: Core features, the console`
- [ ] `C-CF-543` `capability` A privacy page at `/privacy` is reachable from the footer of every route carrying one. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-544` `capability` The privacy page is reachable from the not-found route. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-545` `capability` The privacy page states what the product records about a visitor. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-546` `capability` The privacy page states how long each recorded thing is kept. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-547` `capability` A first-time visitor is asked once about non-essential cookies. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-548` `capability` The cookie answer survives a reload, every later route. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-549` `capability` The cookie band does not appear a second time for a visitor who answered. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-550` `ui` Refusing cookies is as easy to press as accepting. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-551` `constraint` The cookie answer is stored first-party, loading no consent vendor. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-552` `capability` Every public route carries its own title, its own description. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-553` `constraint` No two public routes share a title. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-554` `constraint` No two public routes share a description. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-555` `literal` The shed order runs answer generation, personalization, disjunctive facet counting, vector retrieval. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-556` `constraint` Keyword search is never shed. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-557` `capability` Every degradation is flagged in the response. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-558` `capability` An unmatched path renders the product's own not-found route. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-559` `capability` An unmatched path answers not found rather than success. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-560` `literal` The not-found numeral reads `404`, the brand mark standing in for the zero. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-561` `literal` The not-found heading reads `Page not found`. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-562` `literal` The not-found field is labelled `Search Kestrel`. `src: Core features, the site's remaining obligations`
- [ ] `C-CF-563` `literal` The three not-found links read `API Status`, `Home page`, `Support`. `src: Core features, the site's remaining obligations`

## C-UF User flow

- [ ] `C-UF-01` `literal` The public routes are `/`, `/pricing`, `/products`, `/customers`, `/demorequest`, `/privacy`, `/signup`, `/login`. `src: User flow`
- [ ] `C-UF-02` `literal` The console routes begin `/console`, `/console/<app>/indices`. `src: User flow`
- [ ] `C-UF-03` `literal` An index's console tabs are `configure`, `rules`, `synonyms`, `preview`. `src: User flow`
- [ ] `C-UF-04` `literal` The remaining console routes are `analytics`, `ab-tests`, `keys`, `tasks`, `members`. `src: User flow`
- [ ] `C-UF-05` `capability` A signed-out request for a console route lands on `/login`. `src: User flow`
- [ ] `C-UF-06` `capability` A successful sign-in returns to the route that was asked for. `src: User flow`
- [ ] `C-UF-07` `capability` A sign-in with no pending destination lands on `/console`. `src: User flow`
- [ ] `C-UF-08` `capability` Signing out returns to `/`. `src: User flow`
- [ ] `C-UF-09` `capability` A token expiring mid-action returns the operator to `/login` with the form contents preserved. `src: User flow`
- [ ] `C-UF-10` `capability` A token expiring mid-action writes nothing. `src: User flow`
- [ ] `C-UF-11` `capability` A member lacking a capability is refused by the server, naming the capability. `src: User flow`
- [ ] `C-UF-12` `constraint` A member lacking a capability is never quietly redirected into a read-only view. `src: User flow`
- [ ] `C-UF-13` `capability` An `analyst` may read the rule editor, being refused on save. `src: User flow`
- [ ] `C-UF-14` `capability` A request for another workspace's application renders the not-found route. `src: User flow`
- [ ] `C-UF-15` `ui` Every list carries an empty state naming what would appear there. `src: User flow`
- [ ] `C-UF-16` `ui` Every empty state offers the action that creates the missing thing. `src: User flow`
- [ ] `C-UF-17` `ui` Every route carries a loading state. `src: User flow`
- [ ] `C-UF-18` `ui` A route paints before the search overlay's code has loaded. `src: User flow`
- [ ] `C-UF-19` `ui` An error renders inside the page chrome with a plain sentence, a way onward. `src: User flow`
- [ ] `C-UF-20` `constraint` Nothing ever renders a blank screen, a raw error dump. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product alternates dark bands with light bands rather than gradating between the bands. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The boundary between two bands is a hard horizontal edge across the full width. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The dark ground is a near-black, muted blue carrying display type in a near-white neutral. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The light ground is a near-white neutral with a fractionally greyer second near-white neutral for the alternating band. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Body copy on light sits in a deep cool neutral. `src: UI/UX notes`
- [ ] `C-UX-06` `constraint` A band is one ground or the other, never half-committed. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` A mid, vivid blue carries the primary button fill, the link colour, the eyebrow label, every hover target. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A light, vivid blue carries the secondary fill, the start of every gradient. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A deeper mid, vivid blue carries the pressed state. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A near-white, muted blue carries the selected-row tint on light surfaces, appearing nowhere else. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A mid, muted blue carries the secondary text colour on light, the divider on dark. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` One mid, vivid green appears in exactly one gradient. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` The highlight yellow behind matched words is the only yellow in the product. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Three meaning-carrying colours cover failure, success, progress, appearing nowhere else. `src: UI/UX notes`
- [ ] `C-UX-15` `constraint` The light, vivid blue never carries body copy. `src: UI/UX notes`
- [ ] `C-UX-16` `constraint` The light cool neutral placeholder grey never carries text. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Two type families divide the work: `Sora` for display headings, `Inter` for everything else. `src: UI/UX notes`
- [ ] `C-UX-18` `literal` The `Sora` fallback stack is `"Sora", "Trebuchet MS", "Segoe UI", system-ui, sans-serif`. `src: UI/UX notes`
- [ ] `C-UX-19` `literal` The `Inter` fallback stack is `"Inter", "Helvetica Neue", Arial, system-ui, sans-serif`. `src: UI/UX notes`
- [ ] `C-UX-20` `literal` Body copy is `16px` over a `24px` line, set regular. `src: UI/UX notes`
- [ ] `C-UX-21` `literal` The display heading is `76px` over a `76px` line, set bold. `src: UI/UX notes`
- [ ] `C-UX-22` `literal` The not-found heading is `45px` rising to `56px` at a line-height factor of `1.2`. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Figures line up in a column wherever amounts stack. `src: UI/UX notes`
- [ ] `C-UX-24` `ui` Four shapes are fully rounded: the header search field, the plan chooser, the filter pills, the status markers. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` Density is comfortable on the marketing routes, compact in the console. `src: UI/UX notes`
- [ ] `C-UX-26` `constraint` The product carries no elevation ladder. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` The layering ladder is small, fixed, topping out below an embedded surface's range. `src: UI/UX notes`
- [ ] `C-UX-28` `constraint` The product carries no scroll-scrubbed motion. `src: UI/UX notes`
- [ ] `C-UX-29` `constraint` The product carries no scroll-triggered reveal. `src: UI/UX notes`
- [ ] `C-UX-30` `ui` Everything that changes on hover changes colour only, save two named exceptions. `src: UI/UX notes`
- [ ] `C-UX-31` `ui` The promotion bar rises into place from below, sits, rises out of the top. `src: UI/UX notes`
- [ ] `C-UX-32` `ui` The statistics column holds two copies of its content, translating by exactly half its own height. `src: UI/UX notes`
- [ ] `C-UX-33` `ui` The marquee rows drift in opposite directions, pausing on hover, pausing on focus within. `src: UI/UX notes`
- [ ] `C-UX-34` `constraint` A marquee row never traps a scroll gesture. `src: UI/UX notes`
- [ ] `C-UX-35` `ui` The hero carousel dot fills left to right as the timer runs. `src: UI/UX notes`
- [ ] `C-UX-36` `ui` The demo request submit grows slightly, swapping its flat fill for a translucent four-stop wash. `src: UI/UX notes`
- [ ] `C-UX-37` `ui` Everything that animates shares one character, one speed. `src: UI/UX notes`
- [ ] `C-UX-38` `constraint` No property that changes layout is animated. `src: UI/UX notes`
- [ ] `C-UX-39` `ui` A reduced-motion preference stops the promotion bar cycling. `src: UI/UX notes`
- [ ] `C-UX-40` `ui` A reduced-motion preference stops the statistics column, the marquee rows. `src: UI/UX notes`
- [ ] `C-UX-41` `ui` A reduced-motion preference stops the hero advancing, leaving the dots operable. `src: UI/UX notes`
- [ ] `C-UX-42` `ui` A reduced-motion preference removes hover transforms, keeping hover colour changes. `src: UI/UX notes`
- [ ] `C-UX-43` `constraint` Nothing that conveys information is removed under reduced motion. `src: UI/UX notes`
- [ ] `C-UX-44` `ui` Each route carries one banner, one navigation, one main, one contentinfo. `src: UI/UX notes`
- [ ] `C-UX-45` `ui` Each route carries exactly one first-level heading. `src: UI/UX notes`
- [ ] `C-UX-46` `ui` Heading levels descend without skipping. `src: UI/UX notes`
- [ ] `C-UX-47` `ui` A skip control is the first focusable element on every route. `src: UI/UX notes`
- [ ] `C-UX-48` `ui` The console skip control moves focus to the working pane rather than the left rail. `src: UI/UX notes`
- [ ] `C-UX-49` `contract` Body text meets a contrast ratio of 4.5 to 1 against its own background. `src: UI/UX notes`
- [ ] `C-UX-50` `contract` Large text meets a contrast ratio of 3 to 1. `src: UI/UX notes`
- [ ] `C-UX-51` `contract` An interface component boundary meets a contrast ratio of 3 to 1. `src: UI/UX notes`
- [ ] `C-UX-52` `contract` The contrast bar holds on the dark ground, the light ground alike. `src: UI/UX notes`
- [ ] `C-UX-53` `ui` Every interactive element is operable by keyboard navigation in visual order. `src: UI/UX notes`
- [ ] `C-UX-54` `ui` A visible focus ring is restyled rather than removed. `src: UI/UX notes`
- [ ] `C-UX-55` `ui` One focus ring works on both grounds. `src: UI/UX notes`
- [ ] `C-UX-56` `ui` A container scrolls a focused element into view. `src: UI/UX notes`
- [ ] `C-UX-57` `ui` A route change moves focus to the new route's first-level heading. `src: UI/UX notes`
- [ ] `C-UX-58` `ui` An icon-only control carries its purpose as a text label. `src: UI/UX notes`
- [ ] `C-UX-59` `contract` A touch target is no smaller than 44 by 44 pixels, padding counted. `src: UI/UX notes`
- [ ] `C-UX-60` `constraint` No information is carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-61` `ui` Every content image carries alternative text describing what the image shows. `src: UI/UX notes`
- [ ] `C-UX-62` `ui` A decorative image declares itself decorative. `src: UI/UX notes`
- [ ] `C-UX-63` `ui` A customer card's alternative text is the customer's name. `src: UI/UX notes`
- [ ] `C-UX-64` `ui` The arrangement holds at every width between the named tiers. `src: UI/UX notes`
- [ ] `C-UX-65` `ui` At a narrow viewport nothing overflows sideways. `src: UI/UX notes`
- [ ] `C-UX-66` `ui` At a narrow viewport every navigation target stays reachable. `src: UI/UX notes`
- [ ] `C-UX-67` `ui` The comparison grid becomes one plan at a time below the desktop threshold. `src: UI/UX notes`
- [ ] `C-UX-68` `ui` The selected plan is held in the address bar. `src: UI/UX notes`
- [ ] `C-UX-69` `ui` Every control carries resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes`
- [ ] `C-UX-70` `constraint` An unavailable state is never signalled by colour alone. `src: UI/UX notes`
- [ ] `C-UX-71` `ui` Escape closes the search overlay, the navigation panels, the drawer, the console slide-over. `src: UI/UX notes`
- [ ] `C-UX-72` `ui` Escape returns focus to the trigger. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` The page types are `marketing`, `commercial`, `index`, `capture`, `error`, `console`. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The customers route's header rests light on load. `src: Front-end specification`
- [ ] `C-FE-03` `constraint` The demo request route carries no promotion bar, no utility bar, no header, no footer. `src: Front-end specification`
- [ ] `C-FE-04` `constraint` The not-found route carries no promotion bar, no utility bar, no header, no footer. `src: Front-end specification`
- [ ] `C-FE-05` `literal` The first promotion slide reads `Join us:`, `Kestrel BuildCon 2026: Oct 1, 2026 - VIRTUAL`, `Register Now`. `src: Front-end specification`
- [ ] `C-FE-06` `literal` The second promotion slide reads `UPDATE:`, `Unlock the power of agentic AI with Agent Forge`, `See what's new`. `src: Front-end specification`
- [ ] `C-FE-07` `ui` The promotion bar scrolls away with the page. `src: Front-end specification`
- [ ] `C-FE-08` `literal` The utility bar carries `Company`, `Partners`, `Support`, `Login`, `Logout`. `src: Front-end specification`
- [ ] `C-FE-09` `literal` The language list carries `English`, `German`, `French`, `Brazilian Portuguese`, `Spanish`, `Italian`. `src: Front-end specification`
- [ ] `C-FE-10` `literal` The collapsed language selector shows `Eng`. `src: Front-end specification`
- [ ] `C-FE-11` `capability` The chosen language is held in a cookie, reflected in the route. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The header is sticky, the only sticky element outside the comparison grid. `src: Front-end specification`
- [ ] `C-FE-13` `literal` The five primary navigation items read `Products`, `Solutions`, `Pricing`, `Developers`, `Resources`. `src: Front-end specification`
- [ ] `C-FE-14` `literal` The header secondary button reads `Fix your search`. `src: Front-end specification`
- [ ] `C-FE-15` `literal` The header primary button reads `Get started`. `src: Front-end specification`
- [ ] `C-FE-16` `capability` Four primary items open a panel; only `Pricing` navigates. `src: Front-end specification`
- [ ] `C-FE-17` `ui` A panel opens on pointer entry, on keyboard activation. `src: Front-end specification`
- [ ] `C-FE-18` `literal` The header search placeholder reads `Search or Ask AI`. `src: Front-end specification`
- [ ] `C-FE-19` `literal` The customers route search placeholder reads `Search Kestrel`. `src: Front-end specification`
- [ ] `C-FE-20` `literal` The rotating field message reads `How can I help you?`. `src: Front-end specification`
- [ ] `C-FE-21` `ui` A caret blinks beside the rotating field message. `src: Front-end specification`
- [ ] `C-FE-22` `ui` Below the desktop threshold the header carries the mark, a menu glyph, a circular search control. `src: Front-end specification`
- [ ] `C-FE-23` `literal` The drawer group heading reads `Quick Access`. `src: Front-end specification`
- [ ] `C-FE-24` `literal` The drawer close control reads `Close`. `src: Front-end specification`
- [ ] `C-FE-25` `ui` Hovering a primary navigation item turns the item the mid, vivid blue on both grounds. `src: Front-end specification`
- [ ] `C-FE-26` `ui` Three button variants exist: primary, secondary, form submit. `src: Front-end specification`
- [ ] `C-FE-27` `literal` The footer link row carries `Careers`, `Contact Us`, `About Kestrel`, `Anti-Modern Slavery Statement`. `src: Front-end specification`
- [ ] `C-FE-28` `literal` The footer social heading reads `Social networks`. `src: Front-end specification`
- [ ] `C-FE-29` `literal` The footer newsletter line reads `Get the latest in AI search - straight to your inbox.`. `src: Front-end specification`
- [ ] `C-FE-30` `literal` The footer legal bar carries `Cookie settings`, `Trust Center`, `Privacy Policy`, `Terms of service`. `src: Front-end specification`
- [ ] `C-FE-31` `ui` The divider above the legal bar runs dark at both ends, lighter in the middle. `src: Front-end specification`
- [ ] `C-FE-32` `constraint` Every symbol is inline geometry rather than a file. `src: Front-end specification`
- [ ] `C-FE-33` `literal` The mark is square in a 501 by 501 box, rendered at 24 by 24. `src: Front-end specification`
- [ ] `C-FE-34` `literal` The wordmark sits in a 2197 by 501 box, rendered at 110 by 25. `src: Front-end specification`
- [ ] `C-FE-35` `literal` The wordmark is 4.386 times as wide as the wordmark is tall. `src: Front-end specification`
- [ ] `C-FE-36` `ui` The placeholder mark is a quarter-filled ring. `src: Front-end specification`
- [ ] `C-FE-37` `ui` The magnifier is a ring plus one diagonal handle line. `src: Front-end specification`
- [ ] `C-FE-38` `ui` The circle arrow grows slightly, changing fill, when pointed at. `src: Front-end specification`
- [ ] `C-FE-39` `ui` The globe is a ring, one equator line, one meridian ellipse drawn as two arcs. `src: Front-end specification`
- [ ] `C-FE-40` `constraint` The three chevrons are not interchangeable. `src: Front-end specification`
- [ ] `C-FE-41` `ui` The accordion caret sits at zero opacity at rest, rotating as its panel opens. `src: Front-end specification`
- [ ] `C-FE-42` `ui` The menu glyph is three lines; the close glyph is two crossing lines. `src: Front-end specification`
- [ ] `C-FE-43` `literal` Thirty-three inline vector elements exist across the routes. `src: Front-end specification`
- [ ] `C-FE-44` `ui` The overlay becomes a full modal below a narrow threshold. `src: Front-end specification`
- [ ] `C-FE-45` `capability` The overlay's default violet-leaning accent is overridden to the mid, vivid blue. `src: Front-end specification`
- [ ] `C-FE-46` `capability` The overlay's soft yellow highlight background is kept. `src: Front-end specification`
- [ ] `C-FE-47` `literal` The home route runs eight bands alternating dark, light. `src: Front-end specification`
- [ ] `C-FE-48` `literal` The hero heading reads `Agentic.`, `Generative.`, `Search`. `src: Front-end specification`
- [ ] `C-FE-49` `ui` The hero heading's third line ends with a terminal prompt glyph. `src: Front-end specification`
- [ ] `C-FE-50` `literal` The hero lead reads `One AI retrieval platform to power them all`. `src: Front-end specification`
- [ ] `C-FE-51` `literal` The hero button reads `Explore the platform`. `src: Front-end specification`
- [ ] `C-FE-52` `literal` The three hero panel eyebrows read `Generative`, `Search`, `Agentic`, each over `EXPERIENCES`. `src: Front-end specification`
- [ ] `C-FE-53` `constraint` A hero panel is a composition of live interface elements rather than a flat picture. `src: Front-end specification`
- [ ] `C-FE-54` `literal` The use-cases heading reads `Powering AI retrieval across use cases`. `src: Front-end specification`
- [ ] `C-FE-55` `literal` The use-cases lead is pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-56` `literal` The four accordion items read `AI mode search bar`, `Generative AI`, `Agentic commerce`, `Merchandising`. `src: Front-end specification`
- [ ] `C-FE-57` `literal` The first accordion body is pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-58` `ui` The first accordion item is open on load. `src: Front-end specification`
- [ ] `C-FE-59` `capability` Opening an accordion item changes the screenshot beside the accordion. `src: Front-end specification`
- [ ] `C-FE-60` `constraint` Only one capability accordion item is open at a time. `src: Front-end specification`
- [ ] `C-FE-61` `literal` The capability band button reads `See more capabilities`. `src: Front-end specification`
- [ ] `C-FE-62` `ui` The particle field is generated once from a fixed seed. `src: Front-end specification`
- [ ] `C-FE-63` `literal` The analyst eyebrow is pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-64` `literal` The analyst heading reads `A leader for the third consecutive year`. `src: Front-end specification`
- [ ] `C-FE-65` `literal` The analyst buttons read `Read the announcement`, `See Kestrel in action`. `src: Front-end specification`
- [ ] `C-FE-66` `literal` Five analyst panels rotate with five dots below. `src: Front-end specification`
- [ ] `C-FE-67` `literal` The solutions heading reads `Solutions that fulfill your business goals`. `src: Front-end specification`
- [ ] `C-FE-68` `literal` The solutions lead reads `Here are just some of the ways Kestrel technology provides value from day 1.`. `src: Front-end specification`
- [ ] `C-FE-69` `literal` The five solution card titles read `Quickly surface the right content`, `Understand user intent`, `Confidently launch agentic experiences`, `Personalize for more engagement`, `Create buying urgency`. `src: Front-end specification`
- [ ] `C-FE-70` `ui` The first solution card sits higher than the other four, carrying a two-colour bottom border. `src: Front-end specification`
- [ ] `C-FE-71` `literal` The customer band heading reads `See customer success in action`. `src: Front-end specification`
- [ ] `C-FE-72` `literal` The customer band lead reads `Discover how your peers have been succeeding with Kestrel`. `src: Front-end specification`
- [ ] `C-FE-73` `literal` The ten seeded customer wordmarks are `Northmoor`, `Culture Yard`, `Halcyon Sport`, `Fern & Co`, `Petsmith`, `Shoe Carousel`, `Club Meridian`, `DocMarket`, `Givewell Schools`, `Brightwell Group`. `src: Front-end specification`
- [ ] `C-FE-74` `literal` The customer band button reads `View all customer stories`. `src: Front-end specification`
- [ ] `C-FE-75` `literal` The closing heading reads `Harness the power of goal driven AI search with Kestrel`. `src: Front-end specification`
- [ ] `C-FE-76` `literal` The closing buttons read `Get Started`, `Get a demo`. `src: Front-end specification`
- [ ] `C-FE-77` `literal` The pricing heading reads `Scalable pricing for smarter search`. `src: Front-end specification`
- [ ] `C-FE-78` `literal` The pricing lead is pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-79` `literal` The plan chooser reads `Help me choose a plan`. `src: Front-end specification`
- [ ] `C-FE-80` `literal` The chooser caption reads `Answer 3 quick questions to see which plan fits best.`. `src: Front-end specification`
- [ ] `C-FE-81` `ui` The pricing hero ground sweeps violet-leaning at one edge to teal-leaning at the other. `src: Front-end specification`
- [ ] `C-FE-82` `ui` The `Grow Plus` card carries a lighter gradient ground, a border in the light, vivid blue. `src: Front-end specification`
- [ ] `C-FE-83` `literal` The grid plan actions read `Get started` for three plans, `Request pricing` for the fourth. `src: Front-end specification`
- [ ] `C-FE-84` `ui` Grid rows stripe between the plain light ground, the palest light ground. `src: Front-end specification`
- [ ] `C-FE-85` `ui` A grid feature name carrying a footnote wears the tooltip glyph. `src: Front-end specification`
- [ ] `C-FE-86` `literal` The products route runs nine bands. `src: Front-end specification`
- [ ] `C-FE-87` `literal` The products eyebrow reads `AI PRODUCT OVERVIEW`. `src: Front-end specification`
- [ ] `C-FE-88` `literal` The two-line products heading is pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-89` `literal` The products lead is pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-90` `literal` The products hero buttons read `Get a demo`, `Start building for free`. `src: Front-end specification`
- [ ] `C-FE-91` `constraint` The products hero carries no imagery. `src: Front-end specification`
- [ ] `C-FE-92` `literal` The products section heading reads `Make every interaction smarter with AI retrieval`. `src: Front-end specification`
- [ ] `C-FE-93` `literal` The first feature block is titled `Search experiences`. `src: Front-end specification`
- [ ] `C-FE-94` `literal` The first block's four terms are `Hybrid Search`, `AI Ranking`, `Query Categorization`, `Advanced Personalization`. `src: Front-end specification`
- [ ] `C-FE-95` `literal` The first block's button reads `Learn more about AI Search`. `src: Front-end specification`
- [ ] `C-FE-96` `literal` The video block question reads `Ready to build the next generation of search?`. `src: Front-end specification`
- [ ] `C-FE-97` `literal` The video block button reads `Book a live demo with our product experts`. `src: Front-end specification`
- [ ] `C-FE-98` `constraint` The media element is first-party, carrying native controls, no autoplay. `src: Front-end specification`
- [ ] `C-FE-99` `capability` The poster, the play affordance, the caption track render without a broken media element. `src: Front-end specification`
- [ ] `C-FE-100` `literal` The tools band heading reads `Tools for business users`. `src: Front-end specification`
- [ ] `C-FE-101` `ui` The tools band is a three-column grid carrying a line-drawn icon per column. `src: Front-end specification`
- [ ] `C-FE-102` `ui` The customers search field is roughly twice a text field's height. `src: Front-end specification`
- [ ] `C-FE-103` `ui` Story cards run three columns wide, two at tablet width, one on a phone. `src: Front-end specification`
- [ ] `C-FE-104` `ui` A story card title truncates to three lines with an ellipsis. `src: Front-end specification`
- [ ] `C-FE-105` `ui` A story card's control moves to the mid, vivid blue when the card is pointed at. `src: Front-end specification`
- [ ] `C-FE-106` `ui` The demo request ground sweeps violet to blue with a soft magenta bloom. `src: Front-end specification`
- [ ] `C-FE-107` `literal` The demo request heading reads `Fix your search experience`. `src: Front-end specification`
- [ ] `C-FE-108` `literal` The demo request lead is pinned in the literals table. `src: Front-end specification`
- [ ] `C-FE-109` `ui` A required marker is a red asterisk in its own element before the label text. `src: Front-end specification`
- [ ] `C-FE-110` `literal` The first demo request statistic reads `18,000+` beside `global brands served`. `src: Front-end specification`
- [ ] `C-FE-111` `literal` The second demo request statistic reads `9.3 Billion` beside `Single-day searches`. `src: Front-end specification`
- [ ] `C-FE-112` `ui` The statistics numerals are filled with a left-to-right blue wash clipped to the type. `src: Front-end specification`
- [ ] `C-FE-113` `literal` The first trust row reads `Trusted by 18,000+ businesses`. `src: Front-end specification`
- [ ] `C-FE-114` `literal` The second trust row reads `Enterprise-grade security & data privacy`. `src: Front-end specification`
- [ ] `C-FE-115` `literal` The five compliance badges read `CCPA`, `BSI C5`, `SOC 2 Type II`, `ISO 27001`, `GDPR`. `src: Front-end specification`
- [ ] `C-FE-116` `constraint` The compliance badges are text in bordered pills rather than pictures. `src: Front-end specification`
- [ ] `C-FE-117` `ui` The not-found type is filled with a radial wash, carrying two stacked drop-shadow layers. `src: Front-end specification`
- [ ] `C-FE-118` `ui` The not-found search affordance darkens a step when pointed at. `src: Front-end specification`
- [ ] `C-FE-119` `ui` A label sits above its field, always visible. `src: Front-end specification`
- [ ] `C-FE-120` `constraint` A placeholder is never a substitute for a label. `src: Front-end specification`
- [ ] `C-FE-121` `ui` A select opens on Enter, Space, Down. `src: Front-end specification`
- [ ] `C-FE-122` `ui` A select filters as the user types when holding more than twenty options. `src: Front-end specification`
- [ ] `C-FE-123` `ui` A select closes on Escape, returning focus to its trigger. `src: Front-end specification`
- [ ] `C-FE-124` `literal` The autofill tokens are given-name, family-name, email, tel, organization, country-name. `src: Front-end specification`
- [ ] `C-FE-125` `literal` The phone field carries the `tel` input type. `src: Front-end specification`
- [ ] `C-FE-126` `ui` Creating a record opens a slide-over panel from the right. `src: Front-end specification`
- [ ] `C-FE-127` `ui` Creating a rule opens a slide-over panel from the right. `src: Front-end specification`
- [ ] `C-FE-128` `ui` The search preview stacks to one column below desktop width, query pane first. `src: Front-end specification`
- [ ] `C-FE-129` `ui` A console status pill carries its word beside its fill. `src: Front-end specification`
- [ ] `C-FE-130` `literal` Eleven modules exist, a module depending only on modules above the module in the list. `src: Front-end specification`
- [ ] `C-FE-131` `constraint` The `client` module carries no interface dependency. `src: Front-end specification`
- [ ] `C-FE-132` `capability` The facet control is built once, appearing in the overlay, the customers route, the console preview. `src: Front-end specification`
- [ ] `C-FE-133` `literal` Accordion parameters are mode, an optional media binding, a chevron choice, an initial open item. `src: Front-end specification`
- [ ] `C-FE-134` `capability` An accordion body height is re-measured on a resize. `src: Front-end specification`
- [ ] `C-FE-135` `literal` Marquee parameters are axis, a constant pixel speed, direction, a mask fade distance. `src: Front-end specification`
- [ ] `C-FE-136` `capability` Marquee duration is derived from content length, the constant speed. `src: Front-end specification`
- [ ] `C-FE-137` `constraint` A marquee duration is never set per instance. `src: Front-end specification`
- [ ] `C-FE-138` `literal` Five pieces of state live outside any component. `src: Front-end specification`
- [ ] `C-FE-139` `data` Console table columns are held per member per index on the server. `src: Front-end specification`
- [ ] `C-FE-140` `constraint` No image file ships with the build. `src: Front-end specification`
- [ ] `C-FE-141` `constraint` No video file ships with the build. `src: Front-end specification`
- [ ] `C-FE-142` `constraint` No font file ships with the build. `src: Front-end specification`
- [ ] `C-FE-143` `capability` Only `Sora` at 700, `Inter` at 400 are preloaded. `src: Front-end specification`
- [ ] `C-FE-144` `capability` The fallback stacks carry the design if neither family arrives. `src: Front-end specification`
- [ ] `C-FE-145` `constraint` A generated panel ground never pretends to be a photograph. `src: Front-end specification`
- [ ] `C-FE-146` `ui` A customer wordmark is the customer's name set in `Inter` extra bold, knocked out in white. `src: Front-end specification`
- [ ] `C-FE-147` `constraint` Tracking pixels, the consent embed, the chat embed, the promotion embed are removed rather than replaced. `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is Astro rendering every public route on the server. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Islands hydrate the search overlay, the facet controls, the hero rotation, the accordion, the comparison grid, the console panes. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The backend is Fastify serving the HTTP API under the `/api` prefix on the same origin. `src: Technical requirements`
- [ ] `C-TR-04` `contract` The datastore is PostgreSQL read from `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Console sessions use the app's own email plus password with bearer tokens. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Search calls, ingest calls use the app's own API key system. `src: Technical requirements`
- [ ] `C-TR-07` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-08` `contract` One log line per request goes to standard output. `src: Technical requirements`
- [ ] `C-TR-09` `constraint` Every host, port, credential is read from the environment. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` PostgreSQL is already running; no copy is downloaded, installed, compiled, started. `src: Technical requirements`
- [ ] `C-TR-11` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` The engine is the application itself rather than a service the application calls. `src: Technical requirements`
- [ ] `C-TR-13` `contract` PostgreSQL holds the durable records, settings, synonyms, rules, keys, tasks, events. `src: Technical requirements`
- [ ] `C-TR-14` `capability` The index structures are rebuilt from PostgreSQL on start. `src: Technical requirements`
- [ ] `C-TR-15` `contract` A generation carries posting lists, a term dictionary, a forward view, per-facet document sets. `src: Technical requirements`
- [ ] `C-TR-16` `contract` The term dictionary supports exact lookup, a prefix range walk, edit-distance automaton traversal. `src: Technical requirements`
- [ ] `C-TR-17` `capability` The per-generation document identifier is reassigned on every rebuild. `src: Technical requirements`
- [ ] `C-TR-18` `constraint` Nothing outside a generation stores a per-generation document identifier. `src: Technical requirements`
- [ ] `C-TR-19` `capability` A read binds to one generation for the whole life of a query. `src: Technical requirements`
- [ ] `C-TR-20` `capability` A read carrying a minimum task identifier answers from a generation at or beyond that task. `src: Technical requirements`
- [ ] `C-TR-21` `capability` A read whose minimum task is unmet is refused with a retry hint of one second. `src: Technical requirements`
- [ ] `C-TR-22` `constraint` Older data is never served silently when a minimum task is unmet. `src: Technical requirements`
- [ ] `C-TR-23` `constraint` The console waits for a task nowhere in an interactive path. `src: Technical requirements`
- [ ] `C-TR-24` `constraint` No external model is called for a vector. `src: Technical requirements`
- [ ] `C-TR-25` `constraint` No external language model is called for an answer. `src: Technical requirements`
- [ ] `C-TR-26` `literal` The overlay shows its first result within a third of a second of opening. `src: Technical requirements`
- [ ] `C-TR-27` `literal` The overlay updates within a sixth of a second of a keystroke at the ninety-fifth percentile. `src: Technical requirements`
- [ ] `C-TR-28` `literal` A search over the seeded corpora answers in under twenty milliseconds at the median. `src: Technical requirements`
- [ ] `C-TR-29` `literal` Largest contentful paint stays under two seconds. `src: Technical requirements`
- [ ] `C-TR-30` `literal` Interaction to next paint stays under two hundred milliseconds. `src: Technical requirements`
- [ ] `C-TR-31` `literal` Cumulative layout shift stays under 0.05. `src: Technical requirements`
- [ ] `C-TR-32` `literal` First-party script stays under 120 kilobytes compressed per route. `src: Technical requirements`
- [ ] `C-TR-33` `literal` First-party style stays under 40 kilobytes compressed per route. `src: Technical requirements`
- [ ] `C-TR-34` `constraint` No third-party surface loads anywhere. `src: Technical requirements`
- [ ] `C-TR-35` `capability` Markup, style, the two preloaded faces arrive first. `src: Technical requirements`
- [ ] `C-TR-36` `capability` The overlay's code loads on the first focus of the search field. `src: Technical requirements`
- [ ] `C-TR-37` `constraint` The overlay's code never loads on page load. `src: Technical requirements`
- [ ] `C-TR-38` `capability` The marquee, the statistics loop, the remaining font weights load when the browser is idle. `src: Technical requirements`
- [ ] `C-TR-39` `capability` The consent band loads last of all. `src: Technical requirements`
- [ ] `C-TR-40` `data` Each request records the request identifier, workspace, index, key identifier, generation, stage timings. `src: Technical requirements`
- [ ] `C-TR-41` `data` Each request records candidate counts before, after each stage. `src: Technical requirements`
- [ ] `C-TR-42` `capability` A caller retries on a connection failure, a timeout, a server error. `src: Technical requirements`
- [ ] `C-TR-43` `constraint` A caller never retries a client error other than a rate refusal. `src: Technical requirements`
- [ ] `C-TR-44` `constraint` A caller never retries a mutating request lacking an idempotency key. `src: Technical requirements`
- [ ] `C-TR-45` `literal` Backoff runs exponential from two hundred milliseconds with full jitter, capped at ten seconds. `src: Technical requirements`
- [ ] `C-TR-46` `literal` Timeouts are two seconds connect, five seconds read for a search, thirty for a write. `src: Technical requirements`
- [ ] `C-TR-47` `constraint` No admin key, ingest key, database address, session secret appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-48` `capability` The only key the overlay carries is the seeded search-only key scoped to the two public indices. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Nineteen tables exist. `src: Data model`
- [ ] `C-DM-02` `data` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-04` `literal` The seeded password is written into `/app/USER_README.md` beside each account. `src: Data model`
- [ ] `C-DM-05` `data` `accounts` carries `id`, `email` unique lowercase, `password_hash`, `display_name`, `created_at`. `src: Data model`
- [ ] `C-DM-06` `data` `workspaces` carries `slug` unique, `name`, `plan`, `quota_search_units`, `quota_records`, `retention_days`. `src: Data model`
- [ ] `C-DM-07` `literal` A workspace plan is one of `free`, `growth`, `premium`, `elite`. `src: Data model`
- [ ] `C-DM-08` `literal` `retention_days` is one of `7`, `30`, `90`, `365`. `src: Data model`
- [ ] `C-DM-09` `data` `memberships` carries at most one row per account per workspace. `src: Data model`
- [ ] `C-DM-10` `literal` A membership role is one of `owner`, `admin`, `operator`, `analyst`. `src: Data model`
- [ ] `C-DM-11` `data` `applications` carries `slug` unique within its workspace, `name`, a non-empty ordered `regions` list. `src: Data model`
- [ ] `C-DM-12` `data` `indices` carries `name` unique within its application, case sensitive. `src: Data model`
- [ ] `C-DM-13` `data` `indices` carries `generation` monotonic, incremented on every publish. `src: Data model`
- [ ] `C-DM-14` `literal` `replica_kind` is one of `standard`, `virtual`. `src: Data model`
- [ ] `C-DM-15` `data` `index_settings` holds one row per index. `src: Data model`
- [ ] `C-DM-16` `data` `records` carries `object_id` unique within its index, `attributes`, `vector`, `vector_model_id`, `version`, `updated_at`. `src: Data model`
- [ ] `C-DM-17` `data` A record `version` increments on every accepted write. `src: Data model`
- [ ] `C-DM-18` `data` `synonyms` carries `type`, `synonyms`, `input`, `replacements`, `corrections`, `placeholder`. `src: Data model`
- [ ] `C-DM-19` `data` `rules` carries `enabled`, `conditions`, `consequence`, `validity`, `description`, a rank number. `src: Data model`
- [ ] `C-DM-20` `data` `api_keys` carries `kind`, `acl`, `indices` glob patterns, `valid_until`, `max_hits_per_query`, `referers`, `hashed_secret`. `src: Data model`
- [ ] `C-DM-21` `data` `tasks` carries `id` monotonic per index, `kind`, `status`, `accepted_at`, `published_at`, `error`. `src: Data model`
- [ ] `C-DM-22` `data` `query_events` carries `query_id`, `query`, `filters`, `nb_hits`, `processing_time_ms`, `variant_id`, `rule_ids`, `personalized`. `src: Data model`
- [ ] `C-DM-23` `data` `interaction_events` carries `type`, `subtype`, `user_token`, `object_ids`, `positions`, `query_id`, `value`, `currency`. `src: Data model`
- [ ] `C-DM-24` `data` `rollups_hourly` holds the five aggregate tables keyed by index, hour in UTC. `src: Data model`
- [ ] `C-DM-25` `data` `ab_tests` carries a control index, a challenger, a split `1` to `99`, a window, a status. `src: Data model`
- [ ] `C-DM-26` `data` `personalization_profiles` carries `user_token`, `facet_scores`, `event_count`, `last_seen_at`. `src: Data model`
- [ ] `C-DM-27` `data` `demo_requests` carries `first_name`, `last_name`, `email`, `phone`, `company`, `country`, `status`, `at`. `src: Data model`
- [ ] `C-DM-28` `constraint` No demo request value field may be stored empty. `src: Data model`
- [ ] `C-DM-29` `data` `newsletter_signups` carries `email` unique, `status`, `at`. `src: Data model`
- [ ] `C-DM-30` `data` `cookie_choices` carries `visitor_token` unique, `accepted`, `decided_at`. `src: Data model`
- [ ] `C-DM-31` `data` `idempotency_records` carries `key`, `path`, `body_digest`, the stored response, living twenty-four hours. `src: Data model`
- [ ] `C-DM-32` `contract` Two hits equal on all eight criteria are ordered by `object_id` ascending. `src: Data model`
- [ ] `C-DM-33` `contract` A key's `filters` restriction, the request's filters are both in force. `src: Data model`
- [ ] `C-DM-34` `contract` Two requests sharing key, path, body leave exactly one task. `src: Data model`
- [ ] `C-DM-35` `contract` An accepted demo request is readable afterwards with the six submitted values, unchanged by a restart. `src: Data model`
- [ ] `C-DM-36` `contract` A refused demo request left no row. `src: Data model`
- [ ] `C-DM-37` `contract` A record edited in the console carries its new value in the browser, in a fresh page load, in a search result. `src: Data model`
- [ ] `C-DM-38` `contract` An index record count excludes a deleted record from the moment its delete task publishes. `src: Data model`
- [ ] `C-DM-39` `contract` Seeding is idempotent, so restarting the app duplicates no rows. `src: Data model`
- [ ] `C-DM-40` `literal` The seeded workspaces are slugged `kestrel-demo`, `northmoor`. `src: Data model`
- [ ] `C-DM-41` `literal` The seeded applications are slugged `kestrel-web`, `northmoor-shop`. `src: Data model`
- [ ] `C-DM-42` `literal` The five seeded indices are `site_content`, `customer_stories`, `catalog`, `shirts`, `fixtures`. `src: Data model`
- [ ] `C-DM-43` `literal` `site_content` holds `120` records across the eight sources. `src: Data model`
- [ ] `C-DM-44` `literal` `site_content` uses `searchableAttributes` of `title`, then `unordered(body)`. `src: Data model`
- [ ] `C-DM-45` `literal` `customer_stories` holds `24` records. `src: Data model`
- [ ] `C-DM-46` `literal` Three story titles are pinned in the literals table. `src: Data model`
- [ ] `C-DM-47` `literal` `catalog` holds `36` records with `object_id` from `c_001` to `c_036`. `src: Data model`
- [ ] `C-DM-48` `literal` `shirts` holds `1200` records with `object_id` from `s_0001` to `s_1200`. `src: Data model`
- [ ] `C-DM-49` `literal` `shirts` groups into `300` distinct `shirt_id` values of four colours each. `src: Data model`
- [ ] `C-DM-50` `literal` `fixtures` holds `t1` `Hello World`, `t2` `Helo Word`, `t3` `Crème Brûlée`, `t4` `2024 Edition`, `t5` `2025 Edition`, `t6` `東京都庁`, `t7` `Straße`. `src: Data model`
- [ ] `C-DM-51` `literal` `fixtures` holds `r1` `Blue Running Shoes`, `r2` `Blue Runing Shoes`, `r3` `Shoes Running Blue`, `r4` `Blue Shoes`. `src: Data model`
- [ ] `C-DM-52` `literal` The `fixtures` popularities are `1`, `100`, `50`, `90`. `src: Data model`
- [ ] `C-DM-53` `literal` `fixtures` carries `customRanking` of `desc(popularity)`. `src: Data model`
- [ ] `C-DM-54` `literal` One seeded rule promotes `c_001` to position zero for the query `sofa`, disabled on load. `src: Data model`
- [ ] `C-DM-55` `literal` One seeded `multiWay` synonym joins `sofa`, `couch`, `settee`. `src: Data model`
- [ ] `C-DM-56` `literal` One seeded `oneWay` synonym maps `iphone` to `smartphone`. `src: Data model`
- [ ] `C-DM-57` `data` The demo request table starts empty. `src: Data model`
- [ ] `C-DM-58` `data` The newsletter table starts empty. `src: Data model`
- [ ] `C-DM-59` `data` The cookie choice table starts empty. `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The boundary is the workspace; an account reaches data only through a membership. `src: Constraints`
- [ ] `C-CN-02` `constraint` No request spans two workspaces. `src: Constraints`
- [ ] `C-CN-03` `constraint` No payment exists; the plans are displayed copy. `src: Constraints`
- [ ] `C-CN-04` `constraint` No invoice exists. `src: Constraints`
- [ ] `C-CN-05` `constraint` Every paid action leads to signup, or to `/demorequest`. `src: Constraints`
- [ ] `C-CN-06` `constraint` No email, no SMS, no push is sent. `src: Constraints`
- [ ] `C-CN-07` `constraint` No password reset exists. `src: Constraints`
- [ ] `C-CN-08` `constraint` No consent vendor, support chat, tag manager, analytics vendor, advertising panel, embedded video player is loaded. `src: Constraints`
- [ ] `C-CN-09` `constraint` No third-party search product, no managed search service is used. `src: Constraints`
- [ ] `C-CN-10` `constraint` No external language model, no external embedding provider is used. `src: Constraints`
- [ ] `C-CN-11` `constraint` No multi-region cluster, no physical replication, no second machine exists. `src: Constraints`
- [ ] `C-CN-12` `constraint` No automatically generated synonym feature exists. `src: Constraints`
- [ ] `C-CN-13` `constraint` No query categorization feature exists. `src: Constraints`
- [ ] `C-CN-14` `constraint` No crawler exists. `src: Constraints`
- [ ] `C-CN-15` `constraint` No native mobile application, no desktop application exists. `src: Constraints`
- [ ] `C-CN-16` `constraint` No external network call happens at run time. `src: Constraints`
- [ ] `C-CN-17` `constraint` The navigation panel link inventories are the build's to supply. `src: Constraints`
- [ ] `C-CN-18` `constraint` No marketing route hard-codes a value that should be live. `src: Constraints`
- [ ] `C-CN-19` `literal` The app stays responsive with `1500` records, `2000` query events, `5000` interaction events, `200` demo request rows. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `constraint` Neither port is hardcoded. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-06` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-07` `literal` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-09` `constraint` A dev server is never served. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` The server is not a child of the shell. `src: Deployment contract`
- [ ] `C-DC-12` `contract` The server binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` The server never binds `127.0.0.1`, never binds `localhost`. `src: Deployment contract`
- [ ] `C-DC-14` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-15` `constraint` No persistent volume, fixed container name, custom network is used. `src: Deployment contract`
- [ ] `C-DC-16` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-17` `contract` An invalid or unauthorized call is rejected as a client error rather than a server error. `src: Deployment contract`
- [ ] `C-DC-18` `constraint` An invalid call never answers a silent success. `src: Deployment contract`
- [ ] `C-DC-19` `contract` Every error body carries a `message`, a `code`, a `requestId`. `src: Deployment contract`
- [ ] `C-DC-20` `constraint` An error `message` never contains a key. `src: Deployment contract`
- [ ] `C-DC-21` `contract` A `details` object names the offending path, the offending value where one applies. `src: Deployment contract`
- [ ] `C-DC-22` `contract` Every search call, ingest call authenticates with an application key. `src: Deployment contract`
- [ ] `C-DC-23` `contract` Every console endpoint authenticates with a bearer token, save login, signup, health. `src: Deployment contract`
- [ ] `C-DC-24` `constraint` A search box that filters a list the page already holds is a violation. `src: Deployment contract`
- [ ] `C-DC-25` `constraint` Facet counts computed from the hits already on screen are a violation. `src: Deployment contract`
- [ ] `C-DC-26` `constraint` A hardcoded count beside a source name is a violation. `src: Deployment contract`
- [ ] `C-DC-27` `constraint` A ranking that computes one number per hit is a violation. `src: Deployment contract`
- [ ] `C-DC-28` `constraint` Highlight tags pasted around a folded copy of the text are a violation. `src: Deployment contract`
- [ ] `C-DC-29` `constraint` A demo request kept only in the page's memory is a violation. `src: Deployment contract`
- [ ] `C-DC-30` `constraint` A demo request written to a file on the app container is a violation. `src: Deployment contract`
- [ ] `C-DC-31` `constraint` An analytics figure read from raw events at display time is a violation. `src: Deployment contract`
- [ ] `C-DC-32` `constraint` An honesty flag returned as a constant is a violation. `src: Deployment contract`

## Pinned literals

| Value | What it is | Item |
|---|---|---|
| `owner@example.com` | a value the brief pins verbatim | `C-RL-29` |
| `admin@example.com` | a value the brief pins verbatim | `C-RL-29` |
| `operator@example.com` | a value the brief pins verbatim | `C-RL-29` |
| `analyst@example.com` | a value the brief pins verbatim | `C-RL-29` |
| `owner2@example.com` | a value the brief pins verbatim | `C-RL-29` |
| `deku-demo-pw-2026` | a value the brief pins verbatim | `C-RL-30` |
| `Amelia Ortega` | a value the brief pins verbatim | `C-RL-31` |
| `Ravi Menon` | a value the brief pins verbatim | `C-RL-31` |
| `Lena Fischer` | a value the brief pins verbatim | `C-RL-31` |
| `Tomas Silva` | a value the brief pins verbatim | `C-RL-31` |
| `Priya Raman` | a value the brief pins verbatim | `C-RL-31` |
| `Kestrel Demo` | a value the brief pins verbatim | `C-RL-32` |
| `Northmoor Group` | a value the brief pins verbatim | `C-RL-32` |
| `Website • products` | a value the brief pins verbatim | `C-CF-21` |
| `Learn more →` | a value the brief pins verbatim | `C-CF-22` |
| `Products & Resources` | a value the brief pins verbatim | `C-CF-23` |
| `Filter by source` | a value the brief pins verbatim | `C-CF-24` |
| `Documentation` | a value the brief pins verbatim | `C-CF-25` |
| `Support` | a value the brief pins verbatim | `C-CF-25` |
| `Blog` | a value the brief pins verbatim | `C-CF-25` |
| `Website` | a value the brief pins verbatim | `C-CF-25` |
| `Developers` | a value the brief pins verbatim | `C-CF-25` |
| `Resources` | a value the brief pins verbatim | `C-CF-25` |
| `Academy` | a value the brief pins verbatim | `C-CF-25` |
| `Customer Stories` | a value the brief pins verbatim | `C-CF-25` |
| `40` | a value the brief pins verbatim | `C-CF-26` |
| `24` | a value the brief pins verbatim | `C-CF-26` |
| `18` | a value the brief pins verbatim | `C-CF-26` |
| `12` | a value the brief pins verbatim | `C-CF-26` |
| `9` | a value the brief pins verbatim | `C-CF-26` |
| `8` | a value the brief pins verbatim | `C-CF-26` |
| `5` | a value the brief pins verbatim | `C-CF-26` |
| `4` | a value the brief pins verbatim | `C-CF-26` |
| `Show more results` | a value the brief pins verbatim | `C-CF-31` |
| `How do I integrate Kestrel search into my app?` | a value the brief pins verbatim | `C-CF-35` |
| `Suggestions` | a value the brief pins verbatim | `C-CF-38` |
| `Kestrel API integration` | a value the brief pins verbatim | `C-CF-39` |
| `Kestrel search benefits` | a value the brief pins verbatim | `C-CF-39` |
| `Kestrel scalability` | a value the brief pins verbatim | `C-CF-39` |
| `AI search for ecommerce` | a value the brief pins verbatim | `C-CF-39` |
| `AI mode` | a value the brief pins verbatim | `C-CF-42` |
| `Kestrel Assist` | a value the brief pins verbatim | `C-CF-43` |
| `New chat` | a value the brief pins verbatim | `C-CF-44` |
| `Back to results` | a value the brief pins verbatim | `C-CF-44` |
| `AI powered by Kestrel` | a value the brief pins verbatim | `C-CF-45` |
| `Show All` | a value the brief pins verbatim | `C-CF-46` |
| `Clear All Filters` | a value the brief pins verbatim | `C-CF-46` |
| `typo` | a value the brief pins verbatim | `C-CF-54` |
| `geo` | a value the brief pins verbatim | `C-CF-54` |
| `words` | a value the brief pins verbatim | `C-CF-54` |
| `filters` | a value the brief pins verbatim | `C-CF-54` |
| `proximity` | a value the brief pins verbatim | `C-CF-54` |
| `attribute` | a value the brief pins verbatim | `C-CF-54` |
| `exact` | a value the brief pins verbatim | `C-CF-54` |
| `custom` | a value the brief pins verbatim | `C-CF-54` |
| `blue running shoes` | a value the brief pins verbatim | `C-CF-59` |
| `r1` | a value the brief pins verbatim | `C-CF-59` |
| `r3` | a value the brief pins verbatim | `C-CF-59` |
| `r4` | a value the brief pins verbatim | `C-CF-59` |
| `r2` | a value the brief pins verbatim | `C-CF-59` |
| `blue shoes` | a value the brief pins verbatim | `C-CF-71` |
| `63` | a value the brief pins verbatim | `C-CF-74` |
| `exactOnSingleWordQuery` | a value the brief pins verbatim | `C-CF-80` |
| `word` | a value the brief pins verbatim | `C-CF-80` |
| `none` | a value the brief pins verbatim | `C-CF-80` |
| `alternativesAsExact` | a value the brief pins verbatim | `C-CF-81` |
| `ignorePlurals` | a value the brief pins verbatim | `C-CF-81` |
| `singleWordSynonym` | a value the brief pins verbatim | `C-CF-81` |
| `multiWordsSynonym` | a value the brief pins verbatim | `C-CF-81` |
| `customRanking` | a value the brief pins verbatim | `C-CF-85` |
| `asc(attr)` | a value the brief pins verbatim | `C-CF-85` |
| `desc(attr)` | a value the brief pins verbatim | `C-CF-85` |
| `6371000` | a value the brief pins verbatim | `C-CF-93` |
| `aroundPrecision` | a value the brief pins verbatim | `C-CF-94` |
| `10` | a value the brief pins verbatim | `C-CF-94` |
| `48.8566,2.3522` | a value the brief pins verbatim | `C-CF-96` |
| `aroundRadius` | a value the brief pins verbatim | `C-CF-98` |
| `all` | a value the brief pins verbatim | `C-CF-98` |
| `relevancyStrictness` | a value the brief pins verbatim | `C-CF-100` |
| `0` | a value the brief pins verbatim | `C-CF-100` |
| `100` | a value the brief pins verbatim | `C-CF-100` |
| `o'brien` | a value the brief pins verbatim | `C-CF-110` |
| `l'hotel` | a value the brief pins verbatim | `C-CF-111` |
| `l` | a value the brief pins verbatim | `C-CF-111` |
| `hotel` | a value the brief pins verbatim | `C-CF-111` |
| `a4` | a value the brief pins verbatim | `C-CF-119` |
| `a` | a value the brief pins verbatim | `C-CF-119` |
| `houses` | a value the brief pins verbatim | `C-CF-122` |
| `house` | a value the brief pins verbatim | `C-CF-122` |
| `housing` | a value the brief pins verbatim | `C-CF-123` |
| `minWordSizefor1Typo` | a value the brief pins verbatim | `C-CF-127` |
| `minWordSizefor2Typos` | a value the brief pins verbatim | `C-CF-127` |
| `hlelo` | a value the brief pins verbatim | `C-CF-130` |
| `t1` | a value the brief pins verbatim | `C-CF-130` |
| `1` | a value the brief pins verbatim | `C-CF-130` |
| `xello` | a value the brief pins verbatim | `C-CF-132` |
| `2024` | a value the brief pins verbatim | `C-CF-133` |
| `t4` | a value the brief pins verbatim | `C-CF-133` |
| `t5` | a value the brief pins verbatim | `C-CF-133` |
| `typoTolerance` | a value the brief pins verbatim | `C-CF-137` |
| `min` | a value the brief pins verbatim | `C-CF-137` |
| `strict` | a value the brief pins verbatim | `C-CF-138` |
| `queryType` | a value the brief pins verbatim | `C-CF-139` |
| `prefixLast` | a value the brief pins verbatim | `C-CF-139` |
| `prefixAll` | a value the brief pins verbatim | `C-CF-141` |
| `prefixNone` | a value the brief pins verbatim | `C-CF-141` |
| `hel` | a value the brief pins verbatim | `C-CF-142` |
| `t2` | a value the brief pins verbatim | `C-CF-142` |
| `hel world` | a value the brief pins verbatim | `C-CF-143` |
| `1000` | a value the brief pins verbatim | `C-CF-144` |
| `wor hello` | a value the brief pins verbatim | `C-CF-148` |
| `creme` | a value the brief pins verbatim | `C-CF-149` |
| `crème` | a value the brief pins verbatim | `C-CF-149` |
| `t3` | a value the brief pins verbatim | `C-CF-149` |
| `strasse` | a value the brief pins verbatim | `C-CF-150` |
| `t7` | a value the brief pins verbatim | `C-CF-150` |
| `東京` | a value the brief pins verbatim | `C-CF-151` |
| `t6` | a value the brief pins verbatim | `C-CF-151` |
| `removeWordsIfNoResults` | a value the brief pins verbatim | `C-CF-154` |
| `lastWords` | a value the brief pins verbatim | `C-CF-154` |
| `firstWords` | a value the brief pins verbatim | `C-CF-154` |
| `allOptional` | a value the brief pins verbatim | `C-CF-154` |
| `catalog` | a value the brief pins verbatim | `C-CF-160` |
| `20` | a value the brief pins verbatim | `C-CF-160` |
| `brand:acme` | a value the brief pins verbatim | `C-CF-161` |
| `colour:red` | a value the brief pins verbatim | `C-CF-161` |
| `brand.acme` | a value the brief pins verbatim | `C-CF-161` |
| `brand.zeta` | a value the brief pins verbatim | `C-CF-161` |
| `colour.red` | a value the brief pins verbatim | `C-CF-161` |
| `colour.blue` | a value the brief pins verbatim | `C-CF-161` |
| `attr:value` | a value the brief pins verbatim | `C-CF-167` |
| `<` | a value the brief pins verbatim | `C-CF-168` |
| `<=` | a value the brief pins verbatim | `C-CF-168` |
| `=` | a value the brief pins verbatim | `C-CF-168` |
| `!=` | a value the brief pins verbatim | `C-CF-168` |
| `>=` | a value the brief pins verbatim | `C-CF-168` |
| `>` | a value the brief pins verbatim | `C-CF-168` |
| `attr:number TO number` | a value the brief pins verbatim | `C-CF-169` |
| `_tags:value` | a value the brief pins verbatim | `C-CF-170` |
| `NOT` | a value the brief pins verbatim | `C-CF-171` |
| `AND` | a value the brief pins verbatim | `C-CF-171` |
| `OR` | a value the brief pins verbatim | `C-CF-171` |
| `price > "10"` | a value the brief pins verbatim | `C-CF-175` |
| `[["a:1", "a:2"]]` | a value the brief pins verbatim | `C-CF-179` |
| `a:1 OR a:2` | a value the brief pins verbatim | `C-CF-179` |
| `["-a:1"]` | a value the brief pins verbatim | `C-CF-181` |
| `NOT a:1` | a value the brief pins verbatim | `C-CF-181` |
| `optionalFilters` | a value the brief pins verbatim | `C-CF-183` |
| `shirts` | a value the brief pins verbatim | `C-CF-192` |
| `distinct` | a value the brief pins verbatim | `C-CF-192` |
| `nbHits` | a value the brief pins verbatim | `C-CF-192` |
| `300` | a value the brief pins verbatim | `C-CF-192` |
| `nbPages` | a value the brief pins verbatim | `C-CF-192` |
| `15` | a value the brief pins verbatim | `C-CF-192` |
| `shirt_id` | a value the brief pins verbatim | `C-CF-193` |
| `facetingAfterDistinct` | a value the brief pins verbatim | `C-CF-195` |
| `75` | a value the brief pins verbatim | `C-CF-195` |
| `<em>` | a value the brief pins verbatim | `C-CF-207` |
| `</em>` | a value the brief pins verbatim | `C-CF-207` |
| `highlightPreTag` | a value the brief pins verbatim | `C-CF-208` |
| `highlightPostTag` | a value the brief pins verbatim | `C-CF-208` |
| `partial` | a value the brief pins verbatim | `C-CF-209` |
| `full` | a value the brief pins verbatim | `C-CF-209` |
| `red red red` | a value the brief pins verbatim | `C-CF-212` |
| `red` | a value the brief pins verbatim | `C-CF-212` |
| `Hello World` | a value the brief pins verbatim | `C-CF-213` |
| `snippetEllipsisText` | a value the brief pins verbatim | `C-CF-215` |
| `...` | a value the brief pins verbatim | `C-CF-215` |
| `paginationLimitedTo` | a value the brief pins verbatim | `C-CF-220` |
| `page` | a value the brief pins verbatim | `C-CF-221` |
| `hitsPerPage` | a value the brief pins verbatim | `C-CF-221` |
| `queryID` | a value the brief pins verbatim | `C-CF-225` |
| `Search for a customer story` | a value the brief pins verbatim | `C-CF-230` |
| `Features` | a value the brief pins verbatim | `C-CF-231` |
| `Use Case` | a value the brief pins verbatim | `C-CF-231` |
| `Industry` | a value the brief pins verbatim | `C-CF-231` |
| `Region` | a value the brief pins verbatim | `C-CF-231` |
| `Integration` | a value the brief pins verbatim | `C-CF-231` |
| `Ecommerce` | a value the brief pins verbatim | `C-CF-233` |
| `Media` | a value the brief pins verbatim | `C-CF-233` |
| `Marketplace` | a value the brief pins verbatim | `C-CF-233` |
| `B2B` | a value the brief pins verbatim | `C-CF-233` |
| `3` | a value the brief pins verbatim | `C-CF-233` |
| `Travel` | a value the brief pins verbatim | `C-CF-233` |
| `2` | a value the brief pins verbatim | `C-CF-233` |
| `North America` | a value the brief pins verbatim | `C-CF-234` |
| `Europe` | a value the brief pins verbatim | `C-CF-234` |
| `Asia Pacific` | a value the brief pins verbatim | `C-CF-234` |
| `Latin America` | a value the brief pins verbatim | `C-CF-234` |
| `Elevate` | a value the brief pins verbatim | `C-CF-243` |
| `Grow Plus` | a value the brief pins verbatim | `C-CF-243` |
| `Grow` | a value the brief pins verbatim | `C-CF-243` |
| `Free` | a value the brief pins verbatim | `C-CF-243` |
| `Annual plan` | a value the brief pins verbatim | `C-CF-244` |
| `Pay as you go` | a value the brief pins verbatim | `C-CF-244` |
| `NEW` | a value the brief pins verbatim | `C-CF-245` |
| `Start for free` | a value the brief pins verbatim | `C-CF-247` |
| `Build for free` | a value the brief pins verbatim | `C-CF-247` |
| `Request pricing` | a value the brief pins verbatim | `C-CF-247` |
| `10K search requests /month included then $0.50 per additional 1K search requests` | a value the brief pins verbatim | `C-CF-248` |
| `100K records included then $0.40` | a value the brief pins verbatim | `C-CF-249` |
| `Get started building experiences ever with some of our features.` | a value the brief pins verbatim | `C-CF-250` |
| `No credit card required.` | a value the brief pins verbatim | `C-CF-251` |
| `usd` | a value the brief pins verbatim | `C-CF-252` |
| `$0.50` | a value the brief pins verbatim | `C-CF-252` |
| `50` | a value the brief pins verbatim | `C-CF-252` |
| `$0.40` | a value the brief pins verbatim | `C-CF-252` |
| `See full features grid` | a value the brief pins verbatim | `C-CF-254` |
| `Detailed feature comparison` | a value the brief pins verbatim | `C-CF-255` |
| `Search` | a value the brief pins verbatim | `C-CF-256` |
| `Analytics` | a value the brief pins verbatim | `C-CF-256` |
| `UI Components` | a value the brief pins verbatim | `C-CF-256` |
| `Integrations & Data` | a value the brief pins verbatim | `C-CF-256` |
| `Crawler` | a value the brief pins verbatim | `C-CF-256` |
| `Infrastructure & Plan Limits` | a value the brief pins verbatim | `C-CF-256` |
| `Support & Success` | a value the brief pins verbatim | `C-CF-256` |
| `10 per index` | a value the brief pins verbatim | `C-CF-258` |
| `10,000 per index` | a value the brief pins verbatim | `C-CF-258` |
| `Rules` | a value the brief pins verbatim | `C-CF-260` |
| `Visual Editor` | a value the brief pins verbatim | `C-CF-260` |
| `Manual Synonyms` | a value the brief pins verbatim | `C-CF-260` |
| `Virtual Replicas (Relevant Sort)` | a value the brief pins verbatim | `C-CF-260` |
| `AI Synonyms` | a value the brief pins verbatim | `C-CF-260` |
| `Query Categorization` | a value the brief pins verbatim | `C-CF-260` |
| `Pricing FAQs` | a value the brief pins verbatim | `C-CF-263` |
| `What is a search request?` | a value the brief pins verbatim | `C-CF-264` |
| `First Name` | a value the brief pins verbatim | `C-CF-266` |
| `Last Name` | a value the brief pins verbatim | `C-CF-266` |
| `Business Email` | a value the brief pins verbatim | `C-CF-266` |
| `Phone` | a value the brief pins verbatim | `C-CF-266` |
| `Company` | a value the brief pins verbatim | `C-CF-266` |
| `Country` | a value the brief pins verbatim | `C-CF-266` |
| `Select...` | a value the brief pins verbatim | `C-CF-269` |
| `United States` | a value the brief pins verbatim | `C-CF-269` |
| `Afghanistan` | a value the brief pins verbatim | `C-CF-269` |
| `Get In Touch` | a value the brief pins verbatim | `C-CF-270` |
| `received` | a value the brief pins verbatim | `C-CF-272` |
| `999` | a value the brief pins verbatim | `C-CF-288` |
| `addObject` | a value the brief pins verbatim | `C-CF-289` |
| `objectID` | a value the brief pins verbatim | `C-CF-289` |
| `updateObject` | a value the brief pins verbatim | `C-CF-290` |
| `partialUpdateObject` | a value the brief pins verbatim | `C-CF-292` |
| `partialUpdateObjectNoCreate` | a value the brief pins verbatim | `C-CF-293` |
| `deleteObject` | a value the brief pins verbatim | `C-CF-294` |
| `clear` | a value the brief pins verbatim | `C-CF-295` |
| `Increment` | a value the brief pins verbatim | `C-CF-297` |
| `Decrement` | a value the brief pins verbatim | `C-CF-297` |
| `IncrementFrom` | a value the brief pins verbatim | `C-CF-297` |
| `IncrementSet` | a value the brief pins verbatim | `C-CF-297` |
| `Add` | a value the brief pins verbatim | `C-CF-297` |
| `Remove` | a value the brief pins verbatim | `C-CF-297` |
| `AddUnique` | a value the brief pins verbatim | `C-CF-297` |
| `7` | a value the brief pins verbatim | `C-CF-301` |
| `6` | a value the brief pins verbatim | `C-CF-301` |
| `16` | a value the brief pins verbatim | `C-CF-322` |
| `128` | a value the brief pins verbatim | `C-CF-322` |
| `512` | a value the brief pins verbatim | `C-CF-332` |
| `maxValuesPerFacet` | a value the brief pins verbatim | `C-CF-333` |
| `multiWay` | a value the brief pins verbatim | `C-CF-337` |
| `oneWay` | a value the brief pins verbatim | `C-CF-337` |
| `altCorrection1` | a value the brief pins verbatim | `C-CF-337` |
| `altCorrection2` | a value the brief pins verbatim | `C-CF-337` |
| `placeholder` | a value the brief pins verbatim | `C-CF-337` |
| `bike` | a value the brief pins verbatim | `C-CF-343` |
| `mountain bike` | a value the brief pins verbatim | `C-CF-343` |
| `is` | a value the brief pins verbatim | `C-CF-348` |
| `startsWith` | a value the brief pins verbatim | `C-CF-348` |
| `endsWith` | a value the brief pins verbatim | `C-CF-348` |
| `contains` | a value the brief pins verbatim | `C-CF-348` |
| `30` | a value the brief pins verbatim | `C-CF-361` |
| `personalizationImpact` | a value the brief pins verbatim | `C-CF-366` |
| `99` | a value the brief pins verbatim | `C-CF-368` |
| `256` | a value the brief pins verbatim | `C-CF-379` |
| `1536` | a value the brief pins verbatim | `C-CF-379` |
| `200` | a value the brief pins verbatim | `C-CF-385` |
| `64` | a value the brief pins verbatim | `C-CF-385` |
| `60` | a value the brief pins verbatim | `C-CF-391` |
| `1.0` | a value the brief pins verbatim | `C-CF-391` |
| `semanticRatio` | a value the brief pins verbatim | `C-CF-397` |
| `[n]` | a value the brief pins verbatim | `C-CF-402` |
| `admin` | a value the brief pins verbatim | `C-CF-416` |
| `ingest` | a value the brief pins verbatim | `C-CF-416` |
| `search` | a value the brief pins verbatim | `C-CF-416` |
| `key_site_search` | a value the brief pins verbatim | `C-CF-426` |
| `sk_site_1f6b2d8e4a` | a value the brief pins verbatim | `C-CF-426` |
| `site_content` | a value the brief pins verbatim | `C-CF-427` |
| `customer_stories` | a value the brief pins verbatim | `C-CF-427` |
| `key_story_search` | a value the brief pins verbatim | `C-CF-428` |
| `sk_story_3c9a7e51b2` | a value the brief pins verbatim | `C-CF-428` |
| `key_ingest_demo` | a value the brief pins verbatim | `C-CF-430` |
| `ik_demo_74d2c0a9f1` | a value the brief pins verbatim | `C-CF-430` |
| `filters=industry%3AEcommerce&userToken=u_1029&validUntil=1767225600` | a value the brief pins verbatim | `C-CF-433` |
| `industry:Ecommerce` | a value the brief pins verbatim | `C-CF-445` |
| `industry:Media` | a value the brief pins verbatim | `C-CF-445` |
| `80` | a value the brief pins verbatim | `C-CF-456` |
| `90` | a value the brief pins verbatim | `C-CF-463` |
| `click` | a value the brief pins verbatim | `C-CF-464` |
| `conversion` | a value the brief pins verbatim | `C-CF-464` |
| `view` | a value the brief pins verbatim | `C-CF-464` |
| `404` | a value the brief pins verbatim | `C-CF-560` |
| `Page not found` | a value the brief pins verbatim | `C-CF-561` |
| `Search Kestrel` | a value the brief pins verbatim | `C-CF-562` |
| `API Status` | a value the brief pins verbatim | `C-CF-563` |
| `Home page` | a value the brief pins verbatim | `C-CF-563` |
| `/` | a value the brief pins verbatim | `C-UF-01` |
| `/pricing` | a value the brief pins verbatim | `C-UF-01` |
| `/products` | a value the brief pins verbatim | `C-UF-01` |
| `/customers` | a value the brief pins verbatim | `C-UF-01` |
| `/demorequest` | a value the brief pins verbatim | `C-UF-01` |
| `/privacy` | a value the brief pins verbatim | `C-UF-01` |
| `/signup` | a value the brief pins verbatim | `C-UF-01` |
| `/login` | a value the brief pins verbatim | `C-UF-01` |
| `/console` | a value the brief pins verbatim | `C-UF-02` |
| `/console/<app>/indices` | a value the brief pins verbatim | `C-UF-02` |
| `configure` | a value the brief pins verbatim | `C-UF-03` |
| `rules` | a value the brief pins verbatim | `C-UF-03` |
| `synonyms` | a value the brief pins verbatim | `C-UF-03` |
| `preview` | a value the brief pins verbatim | `C-UF-03` |
| `analytics` | a value the brief pins verbatim | `C-UF-04` |
| `ab-tests` | a value the brief pins verbatim | `C-UF-04` |
| `keys` | a value the brief pins verbatim | `C-UF-04` |
| `tasks` | a value the brief pins verbatim | `C-UF-04` |
| `members` | a value the brief pins verbatim | `C-UF-04` |
| `Sora` | a value the brief pins verbatim | `C-UX-18` |
| `"Sora", "Trebuchet MS", "Segoe UI", system-ui, sans-serif` | a value the brief pins verbatim | `C-UX-18` |
| `Inter` | a value the brief pins verbatim | `C-UX-19` |
| `"Inter", "Helvetica Neue", Arial, system-ui, sans-serif` | a value the brief pins verbatim | `C-UX-19` |
| `16px` | a value the brief pins verbatim | `C-UX-20` |
| `24px` | a value the brief pins verbatim | `C-UX-20` |
| `76px` | a value the brief pins verbatim | `C-UX-21` |
| `45px` | a value the brief pins verbatim | `C-UX-22` |
| `56px` | a value the brief pins verbatim | `C-UX-22` |
| `1.2` | a value the brief pins verbatim | `C-UX-22` |
| `marketing` | a value the brief pins verbatim | `C-FE-01` |
| `commercial` | a value the brief pins verbatim | `C-FE-01` |
| `index` | a value the brief pins verbatim | `C-FE-01` |
| `capture` | a value the brief pins verbatim | `C-FE-01` |
| `error` | a value the brief pins verbatim | `C-FE-01` |
| `console` | a value the brief pins verbatim | `C-FE-01` |
| `Join us:` | a value the brief pins verbatim | `C-FE-05` |
| `Kestrel BuildCon 2026: Oct 1, 2026 - VIRTUAL` | a value the brief pins verbatim | `C-FE-05` |
| `Register Now` | a value the brief pins verbatim | `C-FE-05` |
| `UPDATE:` | a value the brief pins verbatim | `C-FE-06` |
| `Unlock the power of agentic AI with Agent Forge` | a value the brief pins verbatim | `C-FE-06` |
| `See what's new` | a value the brief pins verbatim | `C-FE-06` |
| `Partners` | a value the brief pins verbatim | `C-FE-08` |
| `Login` | a value the brief pins verbatim | `C-FE-08` |
| `Logout` | a value the brief pins verbatim | `C-FE-08` |
| `English` | a value the brief pins verbatim | `C-FE-09` |
| `German` | a value the brief pins verbatim | `C-FE-09` |
| `French` | a value the brief pins verbatim | `C-FE-09` |
| `Brazilian Portuguese` | a value the brief pins verbatim | `C-FE-09` |
| `Spanish` | a value the brief pins verbatim | `C-FE-09` |
| `Italian` | a value the brief pins verbatim | `C-FE-09` |
| `Eng` | a value the brief pins verbatim | `C-FE-10` |
| `Products` | a value the brief pins verbatim | `C-FE-13` |
| `Solutions` | a value the brief pins verbatim | `C-FE-13` |
| `Pricing` | a value the brief pins verbatim | `C-FE-13` |
| `Fix your search` | a value the brief pins verbatim | `C-FE-14` |
| `Get started` | a value the brief pins verbatim | `C-FE-15` |
| `Search or Ask AI` | a value the brief pins verbatim | `C-FE-18` |
| `How can I help you?` | a value the brief pins verbatim | `C-FE-20` |
| `Quick Access` | a value the brief pins verbatim | `C-FE-23` |
| `Close` | a value the brief pins verbatim | `C-FE-24` |
| `Careers` | a value the brief pins verbatim | `C-FE-27` |
| `Contact Us` | a value the brief pins verbatim | `C-FE-27` |
| `About Kestrel` | a value the brief pins verbatim | `C-FE-27` |
| `Anti-Modern Slavery Statement` | a value the brief pins verbatim | `C-FE-27` |
| `Social networks` | a value the brief pins verbatim | `C-FE-28` |
| `Get the latest in AI search - straight to your inbox.` | a value the brief pins verbatim | `C-FE-29` |
| `Cookie settings` | a value the brief pins verbatim | `C-FE-30` |
| `Trust Center` | a value the brief pins verbatim | `C-FE-30` |
| `Privacy Policy` | a value the brief pins verbatim | `C-FE-30` |
| `Terms of service` | a value the brief pins verbatim | `C-FE-30` |
| `Agentic.` | a value the brief pins verbatim | `C-FE-48` |
| `Generative.` | a value the brief pins verbatim | `C-FE-48` |
| `One AI retrieval platform to power them all` | a value the brief pins verbatim | `C-FE-50` |
| `Explore the platform` | a value the brief pins verbatim | `C-FE-51` |
| `Generative` | a value the brief pins verbatim | `C-FE-52` |
| `Agentic` | a value the brief pins verbatim | `C-FE-52` |
| `EXPERIENCES` | a value the brief pins verbatim | `C-FE-52` |
| `Powering AI retrieval across use cases` | a value the brief pins verbatim | `C-FE-54` |
| `AI mode search bar` | a value the brief pins verbatim | `C-FE-56` |
| `Generative AI` | a value the brief pins verbatim | `C-FE-56` |
| `Agentic commerce` | a value the brief pins verbatim | `C-FE-56` |
| `Merchandising` | a value the brief pins verbatim | `C-FE-56` |
| `See more capabilities` | a value the brief pins verbatim | `C-FE-61` |
| `A leader for the third consecutive year` | a value the brief pins verbatim | `C-FE-64` |
| `Read the announcement` | a value the brief pins verbatim | `C-FE-65` |
| `See Kestrel in action` | a value the brief pins verbatim | `C-FE-65` |
| `Solutions that fulfill your business goals` | a value the brief pins verbatim | `C-FE-67` |
| `Here are just some of the ways Kestrel technology provides value from day 1.` | a value the brief pins verbatim | `C-FE-68` |
| `Quickly surface the right content` | a value the brief pins verbatim | `C-FE-69` |
| `Understand user intent` | a value the brief pins verbatim | `C-FE-69` |
| `Confidently launch agentic experiences` | a value the brief pins verbatim | `C-FE-69` |
| `Personalize for more engagement` | a value the brief pins verbatim | `C-FE-69` |
| `Create buying urgency` | a value the brief pins verbatim | `C-FE-69` |
| `See customer success in action` | a value the brief pins verbatim | `C-FE-71` |
| `Discover how your peers have been succeeding with Kestrel` | a value the brief pins verbatim | `C-FE-72` |
| `Northmoor` | a value the brief pins verbatim | `C-FE-73` |
| `Culture Yard` | a value the brief pins verbatim | `C-FE-73` |
| `Halcyon Sport` | a value the brief pins verbatim | `C-FE-73` |
| `Fern & Co` | a value the brief pins verbatim | `C-FE-73` |
| `Petsmith` | a value the brief pins verbatim | `C-FE-73` |
| `Shoe Carousel` | a value the brief pins verbatim | `C-FE-73` |
| `Club Meridian` | a value the brief pins verbatim | `C-FE-73` |
| `DocMarket` | a value the brief pins verbatim | `C-FE-73` |
| `Givewell Schools` | a value the brief pins verbatim | `C-FE-73` |
| `Brightwell Group` | a value the brief pins verbatim | `C-FE-73` |
| `View all customer stories` | a value the brief pins verbatim | `C-FE-74` |
| `Harness the power of goal driven AI search with Kestrel` | a value the brief pins verbatim | `C-FE-75` |
| `Get Started` | a value the brief pins verbatim | `C-FE-76` |
| `Get a demo` | a value the brief pins verbatim | `C-FE-76` |
| `Scalable pricing for smarter search` | a value the brief pins verbatim | `C-FE-77` |
| `Help me choose a plan` | a value the brief pins verbatim | `C-FE-79` |
| `Answer 3 quick questions to see which plan fits best.` | a value the brief pins verbatim | `C-FE-80` |
| `AI PRODUCT OVERVIEW` | a value the brief pins verbatim | `C-FE-87` |
| `Start building for free` | a value the brief pins verbatim | `C-FE-90` |
| `Make every interaction smarter with AI retrieval` | a value the brief pins verbatim | `C-FE-92` |
| `Search experiences` | a value the brief pins verbatim | `C-FE-93` |
| `Hybrid Search` | a value the brief pins verbatim | `C-FE-94` |
| `AI Ranking` | a value the brief pins verbatim | `C-FE-94` |
| `Advanced Personalization` | a value the brief pins verbatim | `C-FE-94` |
| `Learn more about AI Search` | a value the brief pins verbatim | `C-FE-95` |
| `Ready to build the next generation of search?` | a value the brief pins verbatim | `C-FE-96` |
| `Book a live demo with our product experts` | a value the brief pins verbatim | `C-FE-97` |
| `Tools for business users` | a value the brief pins verbatim | `C-FE-100` |
| `Fix your search experience` | a value the brief pins verbatim | `C-FE-107` |
| `18,000+` | a value the brief pins verbatim | `C-FE-110` |
| `global brands served` | a value the brief pins verbatim | `C-FE-110` |
| `9.3 Billion` | a value the brief pins verbatim | `C-FE-111` |
| `Single-day searches` | a value the brief pins verbatim | `C-FE-111` |
| `Trusted by 18,000+ businesses` | a value the brief pins verbatim | `C-FE-113` |
| `Enterprise-grade security & data privacy` | a value the brief pins verbatim | `C-FE-114` |
| `CCPA` | a value the brief pins verbatim | `C-FE-115` |
| `BSI C5` | a value the brief pins verbatim | `C-FE-115` |
| `SOC 2 Type II` | a value the brief pins verbatim | `C-FE-115` |
| `ISO 27001` | a value the brief pins verbatim | `C-FE-115` |
| `GDPR` | a value the brief pins verbatim | `C-FE-115` |
| `tel` | a value the brief pins verbatim | `C-FE-125` |
| `/app/USER_README.md` | a value the brief pins verbatim | `C-DM-04` |
| `free` | a value the brief pins verbatim | `C-DM-07` |
| `growth` | a value the brief pins verbatim | `C-DM-07` |
| `premium` | a value the brief pins verbatim | `C-DM-07` |
| `elite` | a value the brief pins verbatim | `C-DM-07` |
| `retention_days` | a value the brief pins verbatim | `C-DM-08` |
| `365` | a value the brief pins verbatim | `C-DM-08` |
| `owner` | a value the brief pins verbatim | `C-DM-10` |
| `operator` | a value the brief pins verbatim | `C-DM-10` |
| `analyst` | a value the brief pins verbatim | `C-DM-10` |
| `replica_kind` | a value the brief pins verbatim | `C-DM-14` |
| `standard` | a value the brief pins verbatim | `C-DM-14` |
| `virtual` | a value the brief pins verbatim | `C-DM-14` |
| `kestrel-demo` | a value the brief pins verbatim | `C-DM-40` |
| `northmoor` | a value the brief pins verbatim | `C-DM-40` |
| `kestrel-web` | a value the brief pins verbatim | `C-DM-41` |
| `northmoor-shop` | a value the brief pins verbatim | `C-DM-41` |
| `fixtures` | a value the brief pins verbatim | `C-DM-42` |
| `120` | a value the brief pins verbatim | `C-DM-43` |
| `searchableAttributes` | a value the brief pins verbatim | `C-DM-44` |
| `title` | a value the brief pins verbatim | `C-DM-44` |
| `unordered(body)` | a value the brief pins verbatim | `C-DM-44` |
| `36` | a value the brief pins verbatim | `C-DM-47` |
| `object_id` | a value the brief pins verbatim | `C-DM-47` |
| `c_001` | a value the brief pins verbatim | `C-DM-47` |
| `c_036` | a value the brief pins verbatim | `C-DM-47` |
| `1200` | a value the brief pins verbatim | `C-DM-48` |
| `s_0001` | a value the brief pins verbatim | `C-DM-48` |
| `s_1200` | a value the brief pins verbatim | `C-DM-48` |
| `Helo Word` | a value the brief pins verbatim | `C-DM-50` |
| `Crème Brûlée` | a value the brief pins verbatim | `C-DM-50` |
| `2024 Edition` | a value the brief pins verbatim | `C-DM-50` |
| `2025 Edition` | a value the brief pins verbatim | `C-DM-50` |
| `東京都庁` | a value the brief pins verbatim | `C-DM-50` |
| `Straße` | a value the brief pins verbatim | `C-DM-50` |
| `Blue Running Shoes` | a value the brief pins verbatim | `C-DM-51` |
| `Blue Runing Shoes` | a value the brief pins verbatim | `C-DM-51` |
| `Shoes Running Blue` | a value the brief pins verbatim | `C-DM-51` |
| `Blue Shoes` | a value the brief pins verbatim | `C-DM-51` |
| `desc(popularity)` | a value the brief pins verbatim | `C-DM-53` |
| `sofa` | a value the brief pins verbatim | `C-DM-54` |
| `couch` | a value the brief pins verbatim | `C-DM-55` |
| `settee` | a value the brief pins verbatim | `C-DM-55` |
| `iphone` | a value the brief pins verbatim | `C-DM-56` |
| `smartphone` | a value the brief pins verbatim | `C-DM-56` |
| `1500` | a value the brief pins verbatim | `C-CN-19` |
| `2000` | a value the brief pins verbatim | `C-CN-19` |
| `5000` | a value the brief pins verbatim | `C-CN-19` |
| `${APP_PUBLIC_PORT}:4173` | a value the brief pins verbatim | `C-DC-02` |
| `.browser_screenshots/` | a value the brief pins verbatim | `C-DC-07` |
| `.downloads/` | a value the brief pins verbatim | `C-DC-07` |
| `How will Kestrel improve our search experience and conversions?` | a value the brief pins verbatim | `C-CF-34` |
| `Can Kestrel help shoppers find products faster and increase sales?` | a value the brief pins verbatim | `C-CF-36` |
| `Will Kestrel scale with our traffic and data size?` | a value the brief pins verbatim | `C-CF-37` |
| `a:1 OR b:2 AND c:3` | a value the brief pins verbatim | `C-CF-172` |
| `a:1 OR (b:2 AND c:3)` | a value the brief pins verbatim | `C-CF-172` |
| `["a:1", "b:2"]` | a value the brief pins verbatim | `C-CF-178` |
| `a:1 AND b:2` | a value the brief pins verbatim | `C-CF-178` |
| `[["a:1","a:2"], "b:3"]` | a value the brief pins verbatim | `C-CF-180` |
| `(a:1 OR a:2) AND b:3` | a value the brief pins verbatim | `C-CF-180` |
| `["brand:acme<score=3>"]` | a value the brief pins verbatim | `C-CF-183` |
| `["-brand:zeta<score=2>"]` | a value the brief pins verbatim | `C-CF-185` |
| `Enterprise-scale AI Search` | a value the brief pins verbatim | `C-CF-246` |
| `Keyword search with AI` | a value the brief pins verbatim | `C-CF-246` |
| `Keyword search` | a value the brief pins verbatim | `C-CF-246` |
| `Search and recommendations` | a value the brief pins verbatim | `C-CF-246` |
| `More than 18,000 customers across 150+ countries use Kestrel to power agentic, generative, and search experiences across these use cases and more.` | a value the brief pins verbatim | `C-FE-55` |
| `Customers can use natural language in the search bar and AI recognizes intent to guide their discovery.` | a value the brief pins verbatim | `C-FE-57` |
| `NORTHGATE RESEARCH 2026 QUADRANT FOR SEARCH AND PRODUCT DISCOVERY` | a value the brief pins verbatim | `C-FE-63` |
| `Powering the world's best AI experiences - start for free, grow seamlessly and upgrade anytime` | a value the brief pins verbatim | `C-FE-78` |
| `AI search and retrieval` | a value the brief pins verbatim | `C-FE-88` |
| `that shows users what they need` | a value the brief pins verbatim | `C-FE-88` |
| `Enhance your users' journey with solutions powered by retrieval for searching, browsing, personalization, and recommendations.` | a value the brief pins verbatim | `C-FE-89` |
| `Struggling with relevance, slow results, or limited control? We'll show you how to improve search performance and conversions - fast.` | a value the brief pins verbatim | `C-FE-108` |
| `Northmoor Group leverages Kestrel to boost search performance` | a value the brief pins verbatim | `C-DM-46` |
| `Keeping it fast and cool. Culture Yard speeds up Search` | a value the brief pins verbatim | `C-DM-46` |
| `Halcyon Sport achieves +150% sales contribution from search` | a value the brief pins verbatim | `C-DM-46` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of every colour named by role | `C-UX-07` |
| the base spacing unit the density is built from | `C-UX-25` |
| the corner radius the softening steps are measured from | `C-UX-24` |
| the exact duration every animated thing shares | `C-UX-37` |
| where the responsive breakpoints sit | `C-UX-65` |
| the vector template over a record's attributes | `C-CF-315` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 0 | 10 |
| User roles | 1 | 32 |
| Core features | 80 | 563 |
| User flow | 8 | 20 |
| UI and UX notes | 7 | 72 |
| Front-end specification | 14 | 147 |
| Technical requirements | 10 | 48 |
| Data model | 5 | 59 |
| Constraints | 2 | 19 |
| Deployment contract | 9 | 32 |
