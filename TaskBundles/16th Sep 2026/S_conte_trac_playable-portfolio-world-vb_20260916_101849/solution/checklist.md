# Checklist: Vireo

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, techrequirements, datamodel, frontend, constraints, contract
Sections absent: buildplan
Items: 608
Unpinned values flagged: 5

## C-OV Overview

- [ ] `C-OV-01` `capability` The product is the portfolio of a solo creative developer, built as a game. `src: Overview para 1`
- [ ] `C-OV-02` `constraint` The product has no project index, no case study template, no about page. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The product is one page holding a continuous 3D world made of folded paper, card. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The visitor is handed a small character on a hill with a cottage. `src: Overview para 1`
- [ ] `C-OV-05` `capability` The maker's work sits in the landscape as an orchard, a lighthouse, a ski run, a flight through a wind portal. `src: Overview para 1`
- [ ] `C-OV-06` `capability` Walking through the landscape is the menu of the product. `src: Overview para 1`
- [ ] `C-OV-07` `ui` The home screen is a lit, live diorama with the title set over the scene. `src: Overview para 2`
- [ ] `C-OV-08` `capability` The `Bienvenue` screen tells a recruiter what the product is. `src: Overview para 2`
- [ ] `C-OV-09` `constraint` The interface copy is French. `src: Overview para 3`
- [ ] `C-OV-10` `constraint` The document title plus the metadata are English. `src: Overview para 3`
- [ ] `C-OV-11` `capability` Exactly one action leaves the browser, putting a name on a minigame public leaderboard. `src: Overview para 3`
- [ ] `C-OV-12` `capability` A board updates in front of anyone holding the board open. `src: Overview para 3`
- [ ] `C-OV-13` `constraint` Walking, talking, collecting, exploring stay in the visitor's own browser. `src: Overview para 3`
- [ ] `C-OV-14` `literal` The only outbound link is `Contact`. `src: Overview para 3`
- [ ] `C-OV-15` `capability` The world is built entirely from generated geometry, generated sound. `src: Overview para 4`
- [ ] `C-OV-16` `constraint` The product has no visitor accounts, no sign-in for visitors. `src: Overview para 5`
- [ ] `C-OV-17` `constraint` The product carries no comments, likes, chat, messaging. `src: Overview para 5`
- [ ] `C-OV-18` `constraint` The product carries no contact form. `src: Overview para 5`
- [ ] `C-OV-19` `constraint` The product shows no cookie banner. `src: Overview para 5`
- [ ] `C-OV-20` `constraint` The product takes no payments, accepts no uploads, lists no projects. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` Two roles exist, `visitor` plus `owner`. `src: User roles table`
- [ ] `C-RL-02` `role` A `visitor` plays the whole world with no account, no sign-in. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A `visitor` starts a run in any of the four minigames. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A `visitor` sends one entry per finished run. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A `visitor` reads any board. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A `visitor` follows the live updates of a board. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A `visitor` keeps progress in the visitor's own browser. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A `visitor` cannot remove or change any name or total. `src: User roles table row 1`
- [ ] `C-RL-09` `role` A `visitor` cannot list the entries behind a board. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A `visitor` cannot send a second entry for one run. `src: User roles table row 1`
- [ ] `C-RL-11` `role` The `owner` signs in with the seeded account. `src: User roles table row 2`
- [ ] `C-RL-12` `role` The `owner` lists every entry of a game with the stored name. `src: User roles table row 2`
- [ ] `C-RL-13` `role` The `owner` removes the name from an entry, keeping the entry's total, rank. `src: User roles table row 2`
- [ ] `C-RL-14` `role` The `owner` cannot change a total. `src: User roles table row 2`
- [ ] `C-RL-15` `role` The `owner` cannot delete an entry. `src: User roles table row 2`
- [ ] `C-RL-16` `role` The `owner` cannot create a second account. `src: User roles table row 2, User roles signup paragraph`
- [ ] `C-RL-17` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles authorization paragraph`
- [ ] `C-RL-18` `contract` A direct API call from a `visitor` to an `owner`-only endpoint is denied by the server. `src: User roles authorization paragraph`
- [ ] `C-RL-19` `contract` A denied call leaves the protected state unchanged. `src: User roles authorization paragraph`
- [ ] `C-RL-20` `contract` A request to an `owner`-only endpoint with no bearer token is denied. `src: User roles authorization paragraph`
- [ ] `C-RL-21` `contract` A request to an `owner`-only endpoint with a token the app did not issue is denied. `src: User roles authorization paragraph`
- [ ] `C-RL-22` `capability` Anyone plays, signs a board with no invitation, no account, no sign-in. `src: User roles signup paragraph`
- [ ] `C-RL-23` `literal` One account is seeded, `owner@example.com` with role `owner`. `src: User roles seeded account table`
- [ ] `C-RL-24` `literal` The seeded account uses the password `deku-demo-pw-2026`. `src: User roles seeded account line, Data model password paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` Each of the four minigames has a board of its own. `src: Core features, The leaderboard service para 1`
- [ ] `C-CF-02` `capability` A visitor browser keeps an opaque `player_id` in the browser's own storage, reusing the same `player_id` after a reload. `src: Core features, The leaderboard service para 1`
- [ ] `C-CF-03` `literal` A `player_id` is `8` to `64` characters drawn from letters, digits, hyphens. `src: Core features, The leaderboard service para 1`
- [ ] `C-CF-04` `capability` The browser starts a run when a minigame begins. `src: Core features, The leaderboard service para 1`
- [ ] `C-CF-05` `capability` The browser sends one entry when a run ends. `src: Core features, The leaderboard service para 1`
- [ ] `C-CF-06` `capability` Starting a run returns a `run_token` bound to the run's game. `src: Core features, The leaderboard service rule 1`
- [ ] `C-CF-07` `capability` An entry sent with a `run_token` is accepted once. `src: Core features, The leaderboard service rule 1`
- [ ] `C-CF-08` `constraint` A second send carrying the same `run_token` is refused with a reason. `src: Core features, The leaderboard service rule 1, Overview para 5`
- [ ] `C-CF-09` `constraint` A refused second send writes nothing. `src: Core features, The leaderboard service rule 1`
- [ ] `C-CF-10` `constraint` Two simultaneous sends with one `run_token` leave exactly one entry, the other refused. `src: Core features, The leaderboard service rule 1, A1 framing`
- [ ] `C-CF-11` `constraint` An entry naming no `game` is refused as invalid. `src: Core features, The leaderboard service rule 2`
- [ ] `C-CF-12` `constraint` An entry naming an unknown game is refused. `src: Core features, The leaderboard service rule 2`
- [ ] `C-CF-13` `constraint` An entry naming a game other than the `run_token` game is refused. `src: Core features, The leaderboard service rule 2`
- [ ] `C-CF-14` `constraint` A refused entry of any kind writes nothing. `src: Core features, The leaderboard service rules 2 to 3`
- [ ] `C-CF-15` `constraint` Starting a run for an unknown or missing game is refused, creating no run. `src: Core features, The leaderboard service rule 2`
- [ ] `C-CF-16` `capability` An entry carries `counts`, one whole number per item key, plus a `total`. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-17` `literal` Each count is a whole number from `0` up to the item maximum. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-18` `constraint` An item key the game lacks is refused. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-19` `constraint` A negative count is refused. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-20` `constraint` A fractional count is refused. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-21` `constraint` A count above the item maximum is refused. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-22` `capability` A missing item key counts as zero. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-23` `constraint` The `total` equals the sum of each count times the item worth. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-24` `constraint` A total differing from that sum is refused. `src: Core features, The leaderboard service rule 3, A1 framing`
- [ ] `C-CF-25` `constraint` A total above the game maximum is refused. `src: Core features, The leaderboard service rule 3`
- [ ] `C-CF-26` `literal` Orchard counts `pommes 12`, `bananes 3`, `bonus 1` sent with total `245` are accepted. `src: Core features, The leaderboard service rule 3 table row 1`
- [ ] `C-CF-27` `literal` The same orchard counts sent with total `250` are refused. `src: Core features, The leaderboard service rule 3 table row 2`
- [ ] `C-CF-28` `literal` Orchard count `pommes 61` sent with total `610` is refused. `src: Core features, The leaderboard service rule 3 table row 3`
- [ ] `C-CF-29` `literal` Orchard counts `pommes 60`, `bananes 20`, `bonus 5` sent with total `1350` are accepted. `src: Core features, The leaderboard service rule 3 table row 4`
- [ ] `C-CF-30` `literal` Orchard count `cerises 2` sent with total `20` is refused. `src: Core features, The leaderboard service rule 3 table row 5`
- [ ] `C-CF-31` `literal` One `player_id` starts at most `3` runs in any `60` seconds. `src: Core features, The leaderboard service rule 4`
- [ ] `C-CF-32` `constraint` A fourth run start inside the window is refused with a reason, creating no run. `src: Core features, The leaderboard service rule 4`
- [ ] `C-CF-33` `constraint` A run start with a missing `player_id` is refused. `src: Core features, The leaderboard service rule 4`
- [ ] `C-CF-34` `constraint` A run start with a `player_id` outside the character rule is refused. `src: Core features, The leaderboard service rule 4`
- [ ] `C-CF-35` `literal` A board lists at most `10` rows. `src: Core features, The leaderboard service rule 5`
- [ ] `C-CF-36` `capability` A board orders rows by highest total first. `src: Core features, The leaderboard service rule 5`
- [ ] `C-CF-37` `capability` Equal totals are ordered by the earlier entry first. `src: Core features, The leaderboard service rule 5`
- [ ] `C-CF-38` `capability` Ranks run upward from one with no gaps, no shared rank. `src: Core features, The leaderboard service rule 5`
- [ ] `C-CF-39` `capability` An accepted entry response carries the entry rank on the whole board of the game. `src: Core features, The leaderboard service rule 5`
- [ ] `C-CF-40` `capability` An entry outside the top ten is still stored, still ranked. `src: Core features, The leaderboard service rule 5`
- [ ] `C-CF-41` `capability` A viewer holding a board open sees a newly accepted entry take a place without reloading. `src: Core features, The leaderboard service rule 6`
- [ ] `C-CF-42` `constraint` An open board never asks the server again on a timer. `src: Core features, The leaderboard service rule 6`
- [ ] `C-CF-43` `capability` The event stream for a game opens with the current board. `src: Core features, The leaderboard service rule 6`
- [ ] `C-CF-44` `capability` The event stream pushes the new board whenever the game top ten changes. `src: Core features, The leaderboard service rule 6`
- [ ] `C-CF-45` `constraint` An entry below the top ten pushes nothing on the event stream. `src: Core features, The leaderboard service rule 6`
- [ ] `C-CF-46` `constraint` An entry on another game board pushes nothing on the event stream. `src: Core features, The leaderboard service rule 6`
- [ ] `C-CF-47` `capability` A name is checked before being stored. `src: Core features, The leaderboard service rule 7`
- [ ] `C-CF-48` `capability` A name is checked again before being served. `src: Core features, The leaderboard service rule 7`
- [ ] `C-CF-49` `literal` A stored name failing the reserved-word rule is served as `Voyageur anonyme`. `src: Core features, The leaderboard service rule 7`
- [ ] `C-CF-50` `literal` A name the owner removed is served everywhere as `Voyageur anonyme`. `src: Core features, The leaderboard service rules 7 to 8`
- [ ] `C-CF-51` `capability` The owner removes the name from any entry. `src: Core features, The leaderboard service rule 8`
- [ ] `C-CF-52` `capability` An entry with a removed name keeps the same total, the same rank on the board. `src: Core features, The leaderboard service rule 8`
- [ ] `C-CF-53` `capability` Removing an already removed name succeeds, changing nothing. `src: Core features, The leaderboard service rule 8`
- [ ] `C-CF-54` `constraint` A removal call with no bearer token is denied. `src: Core features, The leaderboard service rule 8`
- [ ] `C-CF-55` `constraint` A removal call with a token the app did not issue is denied. `src: Core features, The leaderboard service rule 8`
- [ ] `C-CF-56` `constraint` A denied removal leaves the stored name unchanged. `src: Core features, The leaderboard service rule 8`
- [ ] `C-CF-57` `constraint` The listing of every entry behind a board is denied without the owner bearer token. `src: Core features, The leaderboard service rule 9`
- [ ] `C-CF-58` `capability` The owner signs in with email plus password against the app itself, with no external identity provider. `src: Core features, Auth`
- [ ] `C-CF-59` `literal` A successful sign-in returns a bearer token as `access_token`. `src: Core features, Auth`
- [ ] `C-CF-60` `capability` The bearer token is sent on every owner request. `src: Core features, Auth`
- [ ] `C-CF-61` `capability` The bearer token expires thirty days after issue. `src: Core features, Auth`
- [ ] `C-CF-62` `constraint` Passwords are stored hashed. `src: Core features, Auth`
- [ ] `C-CF-63` `constraint` A wrong password is denied. `src: Core features, Auth`
- [ ] `C-CF-64` `capability` Every minigame has an id, a French label, a zone, a keeper, an item table. `src: Core features, The four minigames and their boards para 1`
- [ ] `C-CF-65` `capability` A game maximum total is the sum of every item worth times the item maximum count. `src: Core features, The four minigames and their boards para 1`
- [ ] `C-CF-66` `literal` Game `orchard` carries label `La Cueillette`, zone `Le Verger`. `src: Core features, The four minigames and their boards table rows 1 to 3`
- [ ] `C-CF-67` `literal` Orchard items are `pommes` `Pommes` worth `10` max `60`, `bananes` `Bananes` worth `25` max `20`, `bonus` `Bonus` worth `50` max `5`. `src: Core features, The four minigames and their boards table rows 1 to 3`
- [ ] `C-CF-68` `literal` Game `lighthouse` carries label `La Veille du Phare`, zone `Le Phare`. `src: Core features, The four minigames and their boards table rows 4 to 5`
- [ ] `C-CF-69` `literal` Lighthouse items are `navires` `Navires guidés` worth `40` max `30`, `tempetes` `Tempêtes traversées` worth `100` max `10`. `src: Core features, The four minigames and their boards table rows 4 to 5`
- [ ] `C-CF-70` `literal` Game `ski` carries label `La Descente`, zone `Les Hautes Neiges`. `src: Core features, The four minigames and their boards table rows 6 to 8`
- [ ] `C-CF-71` `literal` Ski items are `portes` `Portes franchies` worth `30` max `40`, `sauts` `Sauts réussis` worth `60` max `15`, `drapeaux` `Drapeaux cueillis` worth `100` max `5`. `src: Core features, The four minigames and their boards table rows 6 to 8`
- [ ] `C-CF-72` `literal` Game `flight` carries label `Le Vol`, zone `La Grève`. `src: Core features, The four minigames and their boards table rows 9 to 11`
- [ ] `C-CF-73` `literal` Flight items are `cibles` `Cibles touchées` worth `15` max `100`, `canons` `Canons trouvés` worth `50` max `6`, `anneaux` `Anneaux traversés` worth `20` max `50`. `src: Core features, The four minigames and their boards table rows 9 to 11`
- [ ] `C-CF-74` `literal` Maximum totals are `1350` for `orchard`, `2200` for `lighthouse`, `2600` for `ski`, `2800` for `flight`. `src: Core features, The four minigames and their boards para 2`
- [ ] `C-CF-75` `capability` The games are always listed in the order orchard, lighthouse, ski, flight. `src: Core features, The four minigames and their boards para 2`
- [ ] `C-CF-76` `literal` The keepers are `La gardienne du verger`, `Le gardien du phare`, `La monitrice des cimes`, `Le portail du vent`. `src: Core features, The four minigames and their boards table keeper column`
- [ ] `C-CF-77` `capability` In La Cueillette walking into a fruit picks the fruit. `src: Core features, The four minigames and their boards rule 1`
- [ ] `C-CF-78` `capability` An apple counts as `Pommes`, a banana as `Bananes`, a golden fruit as `Bonus`. `src: Core features, The four minigames and their boards rule 1`
- [ ] `C-CF-79` `capability` Touching a rotten fruit costs one apple, never below zero. `src: Core features, The four minigames and their boards rule 1`
- [ ] `C-CF-80` `literal` The orchard clock starts at `60` seconds. `src: Core features, The four minigames and their boards rule 1`
- [ ] `C-CF-81` `capability` An orchard run ends when the clock reaches zero. `src: Core features, The four minigames and their boards rule 1`
- [ ] `C-CF-82` `capability` In La Veille du Phare the visitor turns the lighthouse beam to guide ships between reefs. `src: Core features, The four minigames and their boards rule 2`
- [ ] `C-CF-83` `capability` A ship brought through counts as `Navires guidés`; a storm wave ridden out counts as `Tempêtes traversées`. `src: Core features, The four minigames and their boards rule 2`
- [ ] `C-CF-84` `literal` The lighthouse clock starts at `90` seconds. `src: Core features, The four minigames and their boards rule 2`
- [ ] `C-CF-85` `capability` In La Descente a gate passed counts as `Portes franchies`, a landed jump as `Sauts réussis`, a flag taken as `Drapeaux cueillis`. `src: Core features, The four minigames and their boards rule 3`
- [ ] `C-CF-86` `literal` A ski run ends at the finish line or after `120` seconds. `src: Core features, The four minigames and their boards rule 3`
- [ ] `C-CF-87` `capability` In Le Vol a target hit counts as `Cibles touchées`, a cannon as `Canons trouvés`, a ring as `Anneaux traversés`. `src: Core features, The four minigames and their boards rule 4`
- [ ] `C-CF-88` `capability` The flight craft carries five cells of life. `src: Core features, The four minigames and their boards rule 4`
- [ ] `C-CF-89` `capability` A flight run ends when the last life cell is lost or after 120 seconds. `src: Core features, The four minigames and their boards rule 4`
- [ ] `C-CF-90` `literal` Two weapons, `Canon`, `Super canon`, can be picked up in Le Vol, each announced by a banner. `src: Core features, The four minigames and their boards rule 4`
- [ ] `C-CF-91` `literal` Standing at a keeper brings up the prompt `Parler` with the key `E`. `src: Core features, The four minigames and their boards rule 5`
- [ ] `C-CF-92` `literal` Acting on the prompt opens the keeper dialogue with the choices `Commencer`, `Plus tard`. `src: Core features, The four minigames and their boards rule 5`
- [ ] `C-CF-93` `capability` The choice `Commencer` starts the run with the game display. `src: Core features, The four minigames and their boards rule 5`
- [ ] `C-CF-94` `capability` The choice `Plus tard` closes the dialogue, starting nothing. `src: Core features, The four minigames and their boards rule 5`
- [ ] `C-CF-95` `literal` The orchard keeper says `Soixante secondes pour remplir le panier. Les fruits pourris vous coûtent une pomme.` `src: Core features, The four minigames and their boards rule 5 table row 1`
- [ ] `C-CF-96` `literal` The lighthouse keeper says `Guidez les navires entre les récifs avant que la tempête ne tombe.` `src: Core features, The four minigames and their boards rule 5 table row 2`
- [ ] `C-CF-97` `literal` The ski keeper says `Passez les portes, osez les sauts, cueillez les drapeaux jusqu’en bas.` `src: Core features, The four minigames and their boards rule 5 table row 3`
- [ ] `C-CF-98` `literal` The wind portal says `Le vent vous portera tant que votre coque tiendra.` `src: Core features, The four minigames and their boards rule 5 table row 4`
- [ ] `C-CF-99` `literal` During a run the Menu offers `Terminer la course`. `src: Core features, The four minigames and their boards rule 6`
- [ ] `C-CF-100` `capability` The choice `Terminer la course` ends the run at once with the tally so far. `src: Core features, The four minigames and their boards rule 6`
- [ ] `C-CF-101` `capability` The run clock stops when the Menu is open. `src: Core features, The four minigames and their boards rule 6`
- [ ] `C-CF-102` `capability` The first finished orchard run raises a rope bridge between Le Promontoire, Le Bois Murmurant. `src: Core features, The four minigames and their boards rule 7`
- [ ] `C-CF-103` `literal` The first finished orchard run adds the `Journal` entry `J’ai vu un pont apparaître entre le Promontoire et le Bois Murmurant.` `src: Core features, The four minigames and their boards rule 7`
- [ ] `C-CF-104` `capability` The bridge, the journal entry remain after a reload. `src: Core features, The four minigames and their boards rule 7`
- [ ] `C-CF-105` `capability` A name is trimmed at both ends, inner runs of spaces collapsed to one, before being checked or stored. `src: Core features, The name rule`
- [ ] `C-CF-106` `literal` A name is `2` to `16` characters long after trimming. `src: Core features, The name rule`
- [ ] `C-CF-107` `constraint` A name contains only letters, accented Latin letters, digits, spaces, hyphens, apostrophes. `src: Core features, The name rule`
- [ ] `C-CF-108` `constraint` A name contains at least one letter. `src: Core features, The name rule`
- [ ] `C-CF-109` `literal` A name containing `admin`, `modérateur`, `vireo` or `voyageur anonyme` is refused as reserved. `src: Core features, The name rule`
- [ ] `C-CF-110` `capability` The reserved-word comparison ignores letter case, accents. `src: Core features, The name rule`
- [ ] `C-CF-111` `constraint` An invalid or reserved name is refused with a reason, writing nothing. `src: Core features, The name rule`
- [ ] `C-CF-112` `capability` A loading screen, the preloader, appears on arrival. `src: Core features, The loading screen rule 1`
- [ ] `C-CF-113` `capability` A loading screen appears again after the second `Voyager`. `src: Core features, The loading screen rule 1`
- [ ] `C-CF-114` `ui` The loading screen is never blank, never static in either phase. `src: Core features, The loading screen rule 1`
- [ ] `C-CF-115` `ui` The loading screen shows a small paper figure in a wide hat walking on the spot in a pool of warm light. `src: Core features, The loading screen rule 2`
- [ ] `C-CF-116` `literal` The word `LOADING` sits beneath the loading figure. `src: Core features, The loading screen rule 2`
- [ ] `C-CF-117` `capability` One tip at the bottom of the loading screen changes every few seconds. `src: Core features, The loading screen rule 2`
- [ ] `C-CF-118` `capability` The loading figure is rendered live by the app, never a downloaded animation. `src: Core features, The loading screen rule 2`
- [ ] `C-CF-119` `constraint` The loading screen shows no progress bar, no percentage, no count. `src: Core features, The loading screen rule 3`
- [ ] `C-CF-120` `constraint` The word LOADING never changes during loading. `src: Core features, The loading screen rule 3`
- [ ] `C-CF-121` `capability` Exactly one of the six tips shows at a time. `src: Core features, The loading screen rule 4`
- [ ] `C-CF-122` `ui` The tips crossfade in place with no movement of the layout. `src: Core features, The loading screen rule 4`
- [ ] `C-CF-123` `ui` The first two tips show a drawn keyboard, a drawn controller beside the text. `src: Core features, The loading screen rule 4`
- [ ] `C-CF-124` `literal` Tip 1 reads `Utilisez les flèches directionnelles, ainsi que la souris, pour jouer.` `src: Core features, The loading screen table row 1`
- [ ] `C-CF-125` `literal` Tip 2 reads `Vous pouvez utiliser une manette de jeu pour jouer.` `src: Core features, The loading screen table row 2`
- [ ] `C-CF-126` `literal` Tip 3 reads `N’hésitez pas à revenir sur vos pas : certains lieux révèlent de nouveaux chemins quand le monde a changé.` `src: Core features, The loading screen table row 3`
- [ ] `C-CF-127` `literal` Tip 4 reads `Parlez aux voyageurs que vous croisez : leurs mots sont parfois des portes, et leurs silences des indices.` `src: Core features, The loading screen table row 4`
- [ ] `C-CF-128` `literal` Tip 5 reads `Le Golem de Vigie peut grandement vous aider dans la quête : écoutez ce que la mer lui apprend.` `src: Core features, The loading screen table row 5`
- [ ] `C-CF-129` `literal` Tip 6 reads `Certains passages sont bien cachés : n’hésitez pas à fouiller partout, observer les recoins et suivre les détails que le monde laisse derrière lui.` `src: Core features, The loading screen table row 6`
- [ ] `C-CF-130` `capability` The document the server sends already carries the loading layer, `LOADING`, all six tips. `src: Core features, The loading screen rule 5`
- [ ] `C-CF-131` `constraint` Any new tip describes the world, never an interface element. `src: Core features, The loading screen rule 5`
- [ ] `C-CF-132` `ui` The home screen shows a live diorama of a small wooden cottage on a dark grassy hill at dusk. `src: Core features, The home screen rule 1`
- [ ] `C-CF-133` `ui` A tree leans in from the left out of focus beside a row of trees along a flat sea under a deep blue sky. `src: Core features, The home screen rule 1`
- [ ] `C-CF-134` `ui` Spots of warm light drift over the grass like fireflies. `src: Core features, The home screen rule 1`
- [ ] `C-CF-135` `ui` Only the cottage, the tiny figure in front of the porch are sharp. `src: Core features, The home screen rule 1`
- [ ] `C-CF-136` `capability` The home scene is running, not a picture, part of the same world the visitor later walks. `src: Core features, The home screen rule 1`
- [ ] `C-CF-137` `literal` The display title reads `Où sommeillent les Îles`. `src: Core features, The home screen rule 2`
- [ ] `C-CF-138` `literal` The subtitle reads `Un voyage à travers les créations d’un Creative Developer`. `src: Core features, The home screen rule 2`
- [ ] `C-CF-139` `ui` Title letters write out one at a time, each letter settling from slightly right, slightly large. `src: Core features, The home screen rule 2`
- [ ] `C-CF-140` `capability` Title, subtitle lines break only between words. `src: Core features, The home screen rule 2`
- [ ] `C-CF-141` `capability` The primary action `Voyager` appears four seconds after the title starts, never before. `src: Core features, The home screen rule 3`
- [ ] `C-CF-142` `ui` Voyager fades up from slightly below, then settles. `src: Core features, The home screen rule 3`
- [ ] `C-CF-143` `ui` Voyager carries a drawn return-key mark. `src: Core features, The home screen rule 3`
- [ ] `C-CF-144` `capability` The Enter key activates `Voyager`. `src: Core features, The home screen rule 3`
- [ ] `C-CF-145` `literal` The link `Contact` opens `https://vireo.example/contact` in a new window. `src: Core features, The home screen rule 4`
- [ ] `C-CF-146` `literal` A visually hidden `(Nouvelle fenêtre)` follows the `Contact` label. `src: Core features, The home screen rule 4`
- [ ] `C-CF-147` `capability` Text on the home screen never intercepts the pointer. `src: Core features, The home screen rule 5`
- [ ] `C-CF-148` `capability` Dragging anywhere on the home composition swings the camera around the cottage. `src: Core features, The home screen rule 5`
- [ ] `C-CF-149` `capability` Only `Voyager`, `Contact` take the pointer on the home screen. `src: Core features, The home screen rule 5`
- [ ] `C-CF-150` `ui` The band between the subtitle, Voyager carries no text, no control. `src: Core features, The home screen rule 6`
- [ ] `C-CF-151` `capability` Pressing `Voyager` shows the instruction screen instead of entering the world. `src: Core features, The instruction screen and the second load rule 1`
- [ ] `C-CF-152` `ui` The camera lifts off the hill into a bright sky as the instruction screen appears. `src: Core features, The instruction screen and the second load rule 1`
- [ ] `C-CF-153` `literal` The word `Bienvenue` replaces the title. `src: Core features, The instruction screen and the second load rule 1`
- [ ] `C-CF-154` `literal` Instruction line 1 reads `Ce site est une expérience interactive mêlant jeu et portfolio.` `src: Core features, The instruction screen and the second load table row 1`
- [ ] `C-CF-155` `literal` Instruction line 2 reads `À travers un univers jouable et évolutif, j’y explore des idées, des mécaniques et des techniques du web créatif.` `src: Core features, The instruction screen and the second load table row 2`
- [ ] `C-CF-156` `literal` Instruction line 3 reads `Activez vos haut-parleurs ou un casque, utilisez votre souris ou un gamepad, puis explorez à votre rythme.` `src: Core features, The instruction screen and the second load table row 3`
- [ ] `C-CF-157` `literal` The italic caption `Souris / Clavier · Gamepad · Touch` names the four ways to play. `src: Core features, The instruction screen and the second load rule 2`
- [ ] `C-CF-158` `ui` The instruction paragraph holds a reading measure of about half the screen width. `src: Core features, The instruction screen and the second load rule 2`
- [ ] `C-CF-159` `capability` Voyager drifts up again two seconds after the instruction screen appears. `src: Core features, The instruction screen and the second load rule 3`
- [ ] `C-CF-160` `capability` Pressing the second Voyager starts the second load. `src: Core features, The instruction screen and the second load rule 4`
- [ ] `C-CF-161` `capability` The first zone begins streaming during the home screen. `src: Core features, The instruction screen and the second load rule 4`
- [ ] `C-CF-162` `capability` Only the first zone is required before the visitor can move. `src: Core features, The instruction screen and the second load rule 4`
- [ ] `C-CF-163` `ui` The world stays rendered behind the second wait. `src: Core features, The instruction screen and the second load rule 4`
- [ ] `C-CF-164` `capability` A reload from any state returns to the loading screen, then the home screen, with no error. `src: Core features, The instruction screen and the second load rule 5, User flow entry paragraph`
- [ ] `C-CF-165` `capability` The world holds nine named zones. `src: Core features, The world rule 1`
- [ ] `C-CF-166` `capability` Arriving in a zone names the zone. `src: Core features, The world rule 1`
- [ ] `C-CF-167` `literal` The opening zone is `Le Promontoire`. `src: Core features, The world rule 1`
- [ ] `C-CF-168` `literal` The four minigame zones are `Le Verger`, `Le Phare`, `Les Hautes Neiges`, `La Grève`. `src: Core features, The world rule 1`
- [ ] `C-CF-169` `literal` The other four zones are `Le Bois Murmurant`, `La Lande du Golem`, `Les Neiges`, `Le Dernier Seuil`. `src: Core features, The world rule 1`
- [ ] `C-CF-170` `capability` Fifteen travellers, objects live in the zones. `src: Core features, The world rule 2`
- [ ] `C-CF-171` `capability` Talking to travellers is how the world explains itself. `src: Core features, The world rule 2`
- [ ] `C-CF-172` `ui` The character is folded card in a wide conical hat with a satchel at the hip, facets visible. `src: Core features, The world rule 3`
- [ ] `C-CF-173` `ui` The cottage is paper planks, paper shingles in the warm sand colour. `src: Core features, The world rule 3`
- [ ] `C-CF-174` `ui` Trees have crumpled paper trunks with many separately made leaves. `src: Core features, The world rule 3`
- [ ] `C-CF-175` `ui` The grass is real blades, bright at the tip, dark at the root, leaning together in a slow wave. `src: Core features, The world rule 3`
- [ ] `C-CF-176` `ui` Two grey rocks with chalk drawings lie in the grass at the arrival point on Le Promontoire. `src: Core features, The world rule 4`
- [ ] `C-CF-177` `constraint` No overlay teaches the controls once the world is showing. `src: Core features, The world rule 4`
- [ ] `C-CF-178` `capability` The character is pushed by the ground, the slopes, never teleported. `src: Core features, The world rule 5`
- [ ] `C-CF-179` `capability` Talk ranges, pickup ranges belong to the same physical world as the ground. `src: Core features, The world rule 5`
- [ ] `C-CF-180` `capability` The camera never sinks below the height the camera looks at. `src: Core features, The world rule 6`
- [ ] `C-CF-181` `capability` The camera glides toward position at a pace independent of machine speed. `src: Core features, The world rule 6`
- [ ] `C-CF-182` `capability` Pulling the camera back lifts the camera gaze a little. `src: Core features, The world rule 6`
- [ ] `C-CF-183` `capability` Pointer drag swings the camera freely when the character stands still. `src: Core features, The world rule 6`
- [ ] `C-CF-184` `capability` Pointer drag becomes about a hundred times weaker when the character walks. `src: Core features, The world rule 6`
- [ ] `C-CF-185` `capability` The mouse wheel pulls the camera in, out. `src: Core features, The world rule 6`
- [ ] `C-CF-186` `capability` Some routes are hidden, rewarding a look in corners. `src: Core features, The world rule 7`
- [ ] `C-CF-187` `literal` A browser unable to draw 3D keeps every interface layer with the notice `Le monde ne peut pas être dessiné sur cet appareil.` `src: Core features, The world rule 8, User flow states`
- [ ] `C-CF-188` `capability` Walking near something usable slides one outlined button up from the bottom, naming the action, the key. `src: Core features, Interaction, dialogue and arrival rule 1`
- [ ] `C-CF-189` `capability` The dialogue shows the speaker name above the line. `src: Core features, Interaction, dialogue and arrival rule 2`
- [ ] `C-CF-190` `ui` The dialogue sits over a shadow fading from almost black at the bottom to nothing, keeping the landscape visible. `src: Core features, Interaction, dialogue and arrival rule 2`
- [ ] `C-CF-191` `capability` The prompt turns dark in the four bright places, among them the lighthouse keeper, the ski keeper. `src: Core features, Interaction, dialogue and arrival rule 3`
- [ ] `C-CF-192` `ui` The prompt key mark darkens at the same moment as the prompt. `src: Core features, Interaction, dialogue and arrival rule 3`
- [ ] `C-CF-193` `ui` Arriving in a zone shows the zone name centred in thin letters between two hairlines as wide as the name. `src: Core features, Interaction, dialogue and arrival rule 4`
- [ ] `C-CF-194` `ui` A found object stops the world under a soft dark wash with two star-bursts turning in opposite tints. `src: Core features, Interaction, dialogue and arrival rule 5`
- [ ] `C-CF-195` `ui` A found object turns in front of the visitor as a rendered model, not an icon. `src: Core features, Interaction, dialogue and arrival rule 5`
- [ ] `C-CF-196` `capability` Found objects are recorded in the notebook. `src: Core features, Interaction, dialogue and arrival rule 5`
- [ ] `C-CF-197` `capability` Each minigame display never takes the pointer. `src: Core features, The minigame displays rule 1`
- [ ] `C-CF-198` `ui` The orchard display sets the clock top centre, the Pommes tally bottom centre, the clock larger. `src: Core features, The minigame displays rule 2`
- [ ] `C-CF-199` `ui` The tally swells on gain, shuddering back to place on loss. `src: Core features, The minigame displays rule 2`
- [ ] `C-CF-200` `ui` The clock pulses gently once 10 seconds or fewer remain. `src: Core features, The minigame displays rule 2`
- [ ] `C-CF-201` `ui` The lighthouse display, the ski display are one row along the top edge with time left, item tallies. `src: Core features, The minigame displays rule 3`
- [ ] `C-CF-202` `ui` The flight display uses a deep slate, a pale ice blue, white, half see-through, none of the site colours. `src: Core features, The minigame displays rule 4`
- [ ] `C-CF-203` `ui` The flight tallies sit in the bottom corners with five life cells down the right edge. `src: Core features, The minigame displays rule 4`
- [ ] `C-CF-204` `ui` The flight display is tilted in space rather than flat. `src: Core features, The minigame displays rule 4`
- [ ] `C-CF-205` `ui` A banner crosses the screen, holds, leaves when Canon or Super canon is picked up. `src: Core features, The minigame displays rule 4`
- [ ] `C-CF-206` `capability` A finished run shows a receipt breakdown, one row per item with label, count, worth. `src: Core features, The run loop: receipt, board and name form rule 1`
- [ ] `C-CF-207` `literal` The receipt ends with a `Total` row set apart, half again as large. `src: Core features, The run loop: receipt, board and name form rule 1`
- [ ] `C-CF-208` `ui` Receipt silhouettes are the game pictures crushed to black. `src: Core features, The run loop: receipt, board and name form rule 1`
- [ ] `C-CF-209` `literal` The button `Continuer` with key Enter opens the board. `src: Core features, The run loop: receipt, board and name form rule 1`
- [ ] `C-CF-210` `capability` The board title is the game label. `src: Core features, The run loop: receipt, board and name form rule 2`
- [ ] `C-CF-211` `ui` The board deals itself out one row at a time, a quarter of a second apart. `src: Core features, The run loop: receipt, board and name form rule 2`
- [ ] `C-CF-212` `ui` The name form slides in from the opposite side only after the last row lands. `src: Core features, The run loop: receipt, board and name form rule 2`
- [ ] `C-CF-213` `capability` Each board row shows the rank, the name in italics, the total. `src: Core features, The run loop: receipt, board and name form rule 3`
- [ ] `C-CF-214` `capability` Board totals line up on the digits down the right edge. `src: Core features, The run loop: receipt, board and name form rule 3, UI/UX notes type paragraph`
- [ ] `C-CF-215` `capability` The first board row is noticeably larger than the rest. `src: Core features, The run loop: receipt, board and name form rule 3, Front-end specification board paragraph`
- [ ] `C-CF-216` `ui` The first three rows carry star marks of three, two, one stars over the rank. `src: Core features, The run loop: receipt, board and name form rule 3`
- [ ] `C-CF-217` `capability` The visitor's own entry shows above the board with the rank, even outside the top ten. `src: Core features, The run loop: receipt, board and name form rule 4`
- [ ] `C-CF-218` `ui` The own entry is tinted, glowing gently on, off. `src: Core features, The run loop: receipt, board and name form rule 4`
- [ ] `C-CF-219` `literal` The name form is one row with the bold label `Votre nom`, an italic underlined field, the button `Envoyer`. `src: Core features, The run loop: receipt, board and name form rule 5`
- [ ] `C-CF-220` `capability` The Envoyer button is unavailable during sending. `src: Core features, The run loop: receipt, board and name form rule 5`
- [ ] `C-CF-221` `literal` An accepted send replaces the form with the note `Résultat envoyé.` `src: Core features, The run loop: receipt, board and name form rule 5`
- [ ] `C-CF-222` `capability` The name form is never offered again for a run once sent. `src: Core features, The run loop: receipt, board and name form rule 5`
- [ ] `C-CF-223` `capability` An invalid or reserved name is refused inline, keeping the form with the typed text. `src: Core features, The run loop: receipt, board and name form rule 6`
- [ ] `C-CF-224` `literal` The inline refusal message names the `Votre nom` field. `src: Core features, The run loop: receipt, board and name form rule 6`
- [ ] `C-CF-225` `constraint` An inline refusal writes nothing. `src: Core features, The run loop: receipt, board and name form rule 6`
- [ ] `C-CF-226` `capability` A board opened from the Menu is read-only, with no name form. `src: Core features, The run loop: receipt, board and name form rule 7`
- [ ] `C-CF-227` `literal` A board opened from the Menu offers `Partir`, `Fermer`. `src: Core features, The run loop: receipt, board and name form rule 7`
- [ ] `C-CF-228` `capability` The button `Partir` places the character at the minigame keeper, naming the zone on arrival. `src: Core features, The run loop: receipt, board and name form rule 7`
- [ ] `C-CF-229` `literal` A board with no entries shows `Ce classement attend son premier nom.` `src: Core features, The run loop: receipt, board and name form rule 8`
- [ ] `C-CF-230` `literal` The top-left Menu control is named `Menu`, showing the key `M`. `src: Core features, The Menu and its settings rule 1`
- [ ] `C-CF-231` `capability` The Menu control reports whether the panel is open. `src: Core features, The Menu and its settings rule 1`
- [ ] `C-CF-232` `capability` A click, the M key, the controller start button each open the Menu panel. `src: Core features, The Menu and its settings rule 1`
- [ ] `C-CF-233` `capability` Escape closes the Menu panel, returning focus to the Menu control. `src: Core features, The Menu and its settings rule 1`
- [ ] `C-CF-234` `literal` The Menu panel carries `Reprendre`. `src: Core features, The Menu and its settings rule 2`
- [ ] `C-CF-235` `literal` The `Classements` section lists `La Cueillette`, `La Veille du Phare`, `La Descente`, `Le Vol`. `src: Core features, The Menu and its settings rule 2`
- [ ] `C-CF-236` `capability` The panel shows `Terminer la course` only during a run. `src: Core features, The Menu and its settings rule 2`
- [ ] `C-CF-237` `capability` The settings are real radio groups with a legend each, operable by keyboard. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-238` `literal` Group `Qualité` offers `Basse`, `Moyenne`, `Haute`, defaulting to `Moyenne`. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-239` `literal` Group `Volume de la musique` offers `Bas`, `Moyen`, `Fort`. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-240` `literal` Group `Volume des effets` offers `Bas`, `Moyen`, `Fort`. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-241` `literal` Group `Taille du texte` offers `Normale`, `Grande`. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-242` `literal` Group `Animations` offers `Complètes`, `Réduites`. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-243` `literal` Switches `Couper la musique`, `Couper les effets` each mute a group, keeping the level. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-244` `literal` Switch `Inverser l’axe vertical` inverts the camera vertical control. `src: Core features, The Menu and its settings rule 3`
- [ ] `C-CF-245` `capability` The chosen option in a group lifts, grows, turns bold. `src: Core features, The Menu and its settings rule 4`
- [ ] `C-CF-246` `capability` Every setting takes effect at once with no reload. `src: Core features, The Menu and its settings rule 5`
- [ ] `C-CF-247` `capability` Every setting is still chosen after a reload. `src: Core features, The Menu and its settings rule 5`
- [ ] `C-CF-248` `capability` Quality Basse draws the world at no more than one device pixel per interface pixel. `src: Core features, The Menu and its settings rule 6`
- [ ] `C-CF-249` `capability` Quality Haute uses the full screen density up to twice the interface pixel. `src: Core features, The Menu and its settings rule 6`
- [ ] `C-CF-250` `capability` Quality Basse turns off the depth blur, the glow; quality Haute keeps both. `src: Core features, The Menu and its settings rule 6`
- [ ] `C-CF-251` `capability` The quality choice sets the grass draw distance, the shadow sharpness. `src: Core features, The Menu and its settings rule 6`
- [ ] `C-CF-252` `literal` Text size `Normale` keeps the root at `19px`, `12px` on narrow screens. `src: Core features, The Menu and its settings rule 7`
- [ ] `C-CF-253` `literal` Text size `Grande` sets the root to `23px`, `15px` on narrow screens. `src: Core features, The Menu and its settings rule 7`
- [ ] `C-CF-254` `capability` Group `Animations` defaults to `Réduites` when the system asks to reduce motion, otherwise `Complètes`. `src: Core features, The Menu and its settings rule 8`
- [ ] `C-CF-255` `literal` The notebook, the product inventory, is a ring binder titled `Carnet de voyage`. `src: Core features, The notebook para 1, rule 1`
- [ ] `C-CF-256` `literal` The bottom-right control is named `Inventaire`, showing the key `I`. `src: Core features, The notebook rule 1`
- [ ] `C-CF-257` `capability` A click, the I key, the controller north face button each open the notebook. `src: Core features, The notebook rule 1`
- [ ] `C-CF-258` `capability` Escape closes the notebook. `src: Core features, The notebook rule 1`
- [ ] `C-CF-259` `ui` The notebook rises from the bottom into the middle as two facing pages with metal rings floating in front. `src: Core features, The notebook rule 2`
- [ ] `C-CF-260` `capability` The notebook stays landscape, never taller than four fifths of the screen, never wider than three quarters. `src: Core features, The notebook rule 2`
- [ ] `C-CF-261` `capability` Notebook text uses the handwriting face. `src: Core features, The notebook rule 2`
- [ ] `C-CF-262` `ui` Notebook entries read in the first person. `src: Core features, The notebook rule 2`
- [ ] `C-CF-263` `literal` The notebook pages after the cover are `Récoltes`, `Trouvailles`, `Journal`, then a closing page. `src: Core features, The notebook rule 3`
- [ ] `C-CF-264` `capability` Page `Récoltes` lists the tallies `Pommes`, `Bananes`, `Bonus` across every orchard run. `src: Core features, The notebook rule 3`
- [ ] `C-CF-265` `capability` Page `Trouvailles` lists found objects. `src: Core features, The notebook rule 3`
- [ ] `C-CF-266` `capability` Page `Journal` lists changes seen in the world. `src: Core features, The notebook rule 3`
- [ ] `C-CF-267` `literal` An empty notebook page reads `Rien pour l’instant, mais la route est longue.` `src: Core features, The notebook rule 3`
- [ ] `C-CF-268` `literal` The notebook corners carry `Page suivante`, `Page précédente`. `src: Core features, The notebook rule 4`
- [ ] `C-CF-269` `ui` Unopened notebook entries carry a dotted underline until opened. `src: Core features, The notebook rule 4`
- [ ] `C-CF-270` `capability` Tallies, found objects, journal entries persist in the browser across reloads. `src: Core features, The notebook rule 5`
- [ ] `C-CF-271` `constraint` Notebook contents are never sent to the server. `src: Core features, The notebook rule 5`
- [ ] `C-CF-272` `constraint` Character position, current zone, a run in progress are never kept across a reload. `src: Core features, The notebook rule 5`
- [ ] `C-CF-273` `capability` Mouse, keyboard, controller, touch are peers, each reaching every action. `src: Core features, Input rule 1`
- [ ] `C-CF-274` `capability` The visitor never declares an input method. `src: Core features, Input rule 1`
- [ ] `C-CF-275` `capability` The arrow keys walk, turn the character. `src: Core features, Input rule 2`
- [ ] `C-CF-276` `capability` Keys A, D swing the camera; keypad 5, 2 zoom; holding Shift runs. `src: Core features, Input rule 2`
- [ ] `C-CF-277` `capability` The E key acts on the prompt. `src: Core features, Input rule 2`
- [ ] `C-CF-278` `capability` Enter commits; Escape closes. `src: Core features, Input rule 2`
- [ ] `C-CF-279` `ui` Every control shows the control key in a drawn ring beside the label. `src: Core features, Input rule 2`
- [ ] `C-CF-280` `capability` The left stick, the directional pad walk; the right stick swings, zooms the camera. `src: Core features, Input rule 3`
- [ ] `C-CF-281` `capability` The south face button commits like Enter. `src: Core features, Input rule 3`
- [ ] `C-CF-282` `capability` The east face button closes like Escape. `src: Core features, Input rule 3`
- [ ] `C-CF-283` `capability` The west face button acts on the prompt. `src: Core features, Input rule 3`
- [ ] `C-CF-284` `capability` A controller with a different axis order or direction is read through a per-device mapping table. `src: Core features, Input rule 3`
- [ ] `C-CF-285` `literal` A sideways touch screen shows an on-screen stick at the lower left, buttons `Interagir`, `Courir` at the lower right. `src: Core features, Input rule 4`
- [ ] `C-CF-286` `literal` Each touch control is at least `44` CSS pixels across, never scaling with the interface. `src: Core features, Input rule 4`
- [ ] `C-CF-287` `capability` The touch pad lets touches through except on the pad controls. `src: Core features, Input rule 4`
- [ ] `C-CF-288` `capability` A touch on the glyph inside a touch button counts for the button. `src: Core features, Input rule 4`
- [ ] `C-CF-289` `capability` Every sound is synthesised in the browser. `src: Core features, Audio rule 1`
- [ ] `C-CF-290` `capability` The sound set is a music bed, the sea, the wind, one click, two footsteps. `src: Core features, Audio rule 1`
- [ ] `C-CF-291` `capability` The footstep follows the ground under the character, varying in pitch on every step. `src: Core features, Audio rule 2`
- [ ] `C-CF-292` `capability` The sea swells toward the shore; the wind rises on high open ground. `src: Core features, Audio rule 3`
- [ ] `C-CF-293` `constraint` No sound starts before the first press. `src: Core features, Audio rule 4`
- [ ] `C-CF-294` `capability` The product still plays in silence. `src: Core features, Audio rule 4`
- [ ] `C-CF-295` `capability` The animated title, subtitle each keep the whole sentence in a visually hidden element. `src: Core features, Accessibility rule 1`
- [ ] `C-CF-296` `capability` The per-letter run is hidden from assistive technology. `src: Core features, Accessibility rule 1`
- [ ] `C-CF-297` `literal` A visually hidden heading reads `Où sommeillent les Îles`. `src: Core features, Accessibility rule 2`
- [ ] `C-CF-298` `literal` A visually hidden description includes `Les flèches directionnelles déplacent le personnage.` `src: Core features, Accessibility rule 2`
- [ ] `C-CF-299` `capability` The world surface is a focusable application region. `src: Core features, Accessibility rule 3`
- [ ] `C-CF-300` `capability` A live region outside the application region announces in French. `src: Core features, Accessibility rule 4`
- [ ] `C-CF-301` `literal` A zone arrival is announced as `Nouveau lieu, Le Promontoire` for the opening zone. `src: Core features, Accessibility rule 4`
- [ ] `C-CF-302` `capability` Every dialogue line is announced in the live region. `src: Core features, Accessibility rule 4`
- [ ] `C-CF-303` `literal` A found object is announced with `Objet trouvé, ` before the object name. `src: Core features, Accessibility rule 4`
- [ ] `C-CF-304` `literal` A tally change is announced as the label, a comma, the count, such as `Pommes, 3`. `src: Core features, Accessibility rule 4`
- [ ] `C-CF-305` `literal` A send is announced with `Résultat envoyé, rang ` before the rank. `src: Core features, Accessibility rule 4`
- [ ] `C-CF-306` `literal` A refused send is announced with `Résultat refusé, ` before the reason. `src: Core features, Accessibility rule 4`
- [ ] `C-CF-307` `literal` Every focusable control shows a focus ring at least `2` CSS pixels thick. `src: Core features, Accessibility rule 5`
- [ ] `C-CF-308` `capability` The focus ring stays legible over bright, dark parts of the world without relying on colour. `src: Core features, Accessibility rule 5`
- [ ] `C-CF-309` `capability` Every pointer-hover state has an identical focus state. `src: Core features, Accessibility rule 5`
- [ ] `C-CF-310` `capability` Under reduced motion split text appears at once. `src: Core features, Accessibility rule 6`
- [ ] `C-CF-311` `capability` Under reduced motion the clock warning, the own-row glow are static, the star-burst stops, layers cross-fade without travel. `src: Core features, Accessibility rule 6`
- [ ] `C-CF-312` `capability` Under reduced motion the camera, the character still move. `src: Core features, Accessibility rule 6`
- [ ] `C-CF-313` `literal` The picture controls are named `Menu`, `Inventaire`, keeping the keys in the accessibility tree. `src: Core features, Accessibility rule 7`
- [ ] `C-CF-314` `constraint` The document declares French. `src: Core features, Language and copy rule 1`
- [ ] `C-CF-315` `constraint` The document title, the description each declare English on the element. `src: Core features, Language and copy rule 1`
- [ ] `C-CF-316` `literal` The word `LOADING` declares English. `src: Core features, Language and copy rule 1`
- [ ] `C-CF-317` `constraint` French copy uses the typographic apostrophe, never the straight quote. `src: Core features, Language and copy rule 2`
- [ ] `C-CF-318` `constraint` A no-break space precedes every colon, semicolon, question mark, exclamation mark in French copy. `src: Core features, Language and copy rule 3`
- [ ] `C-CF-319` `literal` `Creative Developer` stays English inside the French subtitle. `src: Core features, Language and copy rule 4`
- [ ] `C-CF-320` `capability` Keyboard shortcut letters live in the copy. `src: Core features, Language and copy rule 4`
- [ ] `C-CF-321` `constraint` No dialogue says press a button; no zone title says level. `src: Core features, Language and copy rule 5`
- [ ] `C-CF-322` `literal` The page title is `Where Worlds Take Shape - Interactive WebGL Portfolio`. `src: Core features, The published surface rule 1`
- [ ] `C-CF-323` `literal` The page description opens `A playable portfolio: walk a paper-craft world, meet its travellers`. `src: Core features, The published surface rule 1`
- [ ] `C-CF-324` `literal` The page description ends `post your best run to a public leaderboard.` `src: Core features, The published surface rule 1`
- [ ] `C-CF-325` `capability` The page declares a social preview title equal to the page title. `src: Core features, The published surface rule 2`
- [ ] `C-CF-326` `literal` The social preview image is `/og-image.png`. `src: Core features, The published surface rule 2`
- [ ] `C-CF-327` `literal` The page declares the site name `Vireo`, locale `fr_FR`, alternate `en_US`, a large summary card. `src: Core features, The published surface rule 2`
- [ ] `C-CF-328` `literal` The preview image resolves as a `1200` by `630` PNG. `src: Core features, The published surface rule 2`
- [ ] `C-CF-329` `capability` The preview image is rendered from the home camera at build time. `src: Core features, The published surface rule 2`
- [ ] `C-CF-330` `capability` An unknown address answers not-found. `src: Core features, The published surface rule 3, User flow route table row 2`
- [ ] `C-CF-331` `literal` The not-found page is titled `Page introuvable - Vireo`. `src: Core features, The published surface rule 3`
- [ ] `C-CF-332` `literal` The not-found page is described as `Cette adresse ne mène nulle part dans le monde de Vireo.` `src: Core features, The published surface rule 3`
- [ ] `C-CF-333` `literal` The not-found page is headed `Page introuvable` with the link `Retour au voyage` back to `/`. `src: Core features, The published surface rule 3, User flow entry paragraph`
- [ ] `C-CF-334` `constraint` The not-found page loads no script. `src: Core features, The published surface rule 3`
- [ ] `C-CF-335` `constraint` No path under the static files answers with a directory listing. `src: Core features, The published surface rule 4`

## C-UF User flow

- [ ] `C-UF-01` `literal` Route `/` serves the whole product to the public. `src: User flow route table row 1`
- [ ] `C-UF-02` `capability` The address never changes as the visitor moves between screens. `src: User flow para 1`
- [ ] `C-UF-03` `capability` Screen state, character position, collection live as layers over one running world. `src: User flow para 1`
- [ ] `C-UF-04` `constraint` No visitor sign-in, no protected page exists. `src: User flow entry paragraph`
- [ ] `C-UF-05` `constraint` An expired owner token is denied, leaving the entry untouched. `src: User flow entry paragraph`
- [ ] `C-UF-06` `capability` Escape closes the open layer, returning focus to the opener. `src: User flow entry paragraph`
- [ ] `C-UF-07` `capability` Journey one reaches the world through the loading screen, the home title, Voyager, the welcome screen, the second Voyager, arriving at the opening zone. `src: User flow journey 1`
- [ ] `C-UF-08` `capability` Journey one ends with the Menu control, the notebook control in their corners. `src: User flow journey 1`
- [ ] `C-UF-09` `capability` Journey two runs from the Menu boards to the orchard board, the keeper, the run start, the early run end. `src: User flow journey 2`
- [ ] `C-UF-10` `capability` Journey two shows the receipt rows for apples, bananas, bonus, total before the board opens. `src: User flow journey 2`
- [ ] `C-UF-11` `capability` Journey two ends with the sent note replacing the form, the own entry above the board. `src: User flow journey 2`
- [ ] `C-UF-12` `capability` Journey three sends the name A, keeping the form with a message naming the name field, writing no entry. `src: User flow journey 3`
- [ ] `C-UF-13` `capability` Journey four opens the flight board from the Menu, showing the empty board line. `src: User flow journey 4`
- [ ] `C-UF-14` `capability` Journey five keeps the Grande text size, the reduced animations chosen after a reload. `src: User flow journey 5`
- [ ] `C-UF-15` `capability` Journey six opens the notebook with the I key, turning a page to the tallies. `src: User flow journey 6`
- [ ] `C-UF-16` `capability` Journey seven removes a name through the API, the board showing the anonymous name at the same total, rank. `src: User flow journey 7`
- [ ] `C-UF-17` `constraint` No error crashes the app or leaves a blank page. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface is a small quiet frame around a paper world, letting the world be seen first. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The register is playful, atmospheric, with the subject seen first. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The palette holds five colours with one transparency. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` Almost all interface text is a near-white neutral over the rendered world. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` The document ground before the first frame is a near-black neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` The loading ground is one step lighter than the document near-black. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` Paper is a mid, soft orange reserved for paper things. `src: UI/UX notes para 2`
- [ ] `C-UX-08` `ui` Two blues, a mid vivid blue, a deep muted blue, complete the token set. `src: UI/UX notes para 2`
- [ ] `C-UX-09` `ui` Washes over the world are black at partial opacity. `src: UI/UX notes para 2`
- [ ] `C-UX-10` `constraint` The interface has no colour scale, no elevation scale, no grid. `src: UI/UX notes para 2`
- [ ] `C-UX-11` `literal` `Playfair Display` carries the home title at `85.5px`, `Bienvenue` at `114px`. `src: UI/UX notes para 3`
- [ ] `C-UX-12` `literal` `Lato` carries body at `19px` in thickness `400`, the subtitle at `22.8px` in thickness `100`, the button label at `20.9px`. `src: UI/UX notes para 3`
- [ ] `C-UX-13` `literal` The word `LOADING` is `Lato` at `19px`, bold. `src: UI/UX notes para 3`
- [ ] `C-UX-14` `capability` One handwriting face is used in the notebook, nowhere else. `src: UI/UX notes para 3`
- [ ] `C-UX-15` `ui` Every letter of the home title, subtitle carries a soft shadow, supplemented where the shadow alone falls short. `src: UI/UX notes para 3`
- [ ] `C-UX-16` `capability` A name is always italic, typed or displayed. `src: UI/UX notes para 3`
- [ ] `C-UX-17` `constraint` No other font family is loaded. `src: UI/UX notes para 3`
- [ ] `C-UX-18` `ui` Every button is a pill; every key mark sits in a thin drawn circle. `src: UI/UX notes para 4`
- [ ] `C-UX-19` `ui` Panels are softly rounded; hairlines stay one line thick at every size. `src: UI/UX notes para 4`
- [ ] `C-UX-20` `ui` Density is sparse, comfortable. `src: UI/UX notes para 4`
- [ ] `C-UX-21` `constraint` The layout has no menu bar, no header, no footer. `src: UI/UX notes para 4`
- [ ] `C-UX-22` `capability` At most three layers are live at once. `src: UI/UX notes para 4`
- [ ] `C-UX-23` `ui` Every panel sits dead centre, bottom centre, top centre, or in a corner. `src: UI/UX notes para 4`
- [ ] `C-UX-24` `capability` The Menu sits in the top-left corner; the notebook control sits in the bottom-right corner. `src: UI/UX notes para 4`
- [ ] `C-UX-25` `constraint` The product has one scheme with no light theme, no dark theme. `src: UI/UX notes para 4`
- [ ] `C-UX-26` `ui` The pill fills from the bottom edge to the top on pointer rest or keyboard focus, the label flipping colour. `src: UI/UX notes para 5`
- [ ] `C-UX-27` `capability` An unavailable button is dimmed, ignoring the pointer. `src: UI/UX notes para 5`
- [ ] `C-UX-28` `ui` Each screen leads with one primary action visually distinct from every secondary one. `src: UI/UX notes para 5`
- [ ] `C-UX-29` `ui` On the home screen Voyager is the pill; Contact is a quiet underlined word. `src: UI/UX notes para 5`
- [ ] `C-UX-30` `ui` The motion character is eased with four speeds, the home Voyager arriving slowly, late on purpose. `src: UI/UX notes para 6`
- [ ] `C-UX-31` `constraint` No custom-shaped motion curve appears in the interface. `src: UI/UX notes para 6`
- [ ] `C-UX-32` `ui` A layer fade, a layer rise follow one number; an entrance interrupted halfway reverses smoothly. `src: UI/UX notes para 6`
- [ ] `C-UX-33` `ui` The board rises a little; the notebook rises a whole page height. `src: UI/UX notes para 6`
- [ ] `C-UX-34` `ui` Bottom-docked things park twice their height below the screen, sliding up. `src: UI/UX notes para 6`
- [ ] `C-UX-35` `ui` The Contact hairline grows outward from the middle. `src: UI/UX notes para 6`
- [ ] `C-UX-36` `literal` Interface text over the world meets WCAG AA, at least `4.5:1` against the brightest pixel. `src: UI/UX notes para 7`
- [ ] `C-UX-37` `capability` Keyboard navigation reaches everything from the first frame to a moving character. `src: UI/UX notes para 7`
- [ ] `C-UX-38` `capability` Meaning never rides on colour alone. `src: UI/UX notes para 7`
- [ ] `C-UX-39` `capability` Changing the single root text size grows every gap, padding, button, panel together. `src: UI/UX notes para 8, Front-end specification scaling paragraph`
- [ ] `C-UX-40` `literal` One breakpoint sits at `64em` wide, also applying under `40.625em` tall. `src: UI/UX notes para 8, Front-end specification scaling paragraph`
- [ ] `C-UX-41` `literal` Below the breakpoint the root drops from `19px` to `12px`. `src: UI/UX notes para 8, Front-end specification scaling paragraph`
- [ ] `C-UX-42` `literal` Below the breakpoint the home title becomes `48px`, `Bienvenue` becomes `60px`. `src: UI/UX notes para 8`
- [ ] `C-UX-43` `capability` Below the breakpoint dialogue text grows relative to the root. `src: UI/UX notes para 8`
- [ ] `C-UX-44` `capability` Below the breakpoint the Contact link moves to the lower right corner. `src: UI/UX notes para 8`
- [ ] `C-UX-45` `capability` Below the breakpoint the lighthouse, ski, flight displays shrink further than the rest. `src: UI/UX notes para 8, Front-end specification displays paragraph`
- [ ] `C-UX-46` `capability` The design holds at every width between phone, tablet, desktop. `src: UI/UX notes para 8`
- [ ] `C-UX-47` `capability` At a narrow viewport held sideways nothing overflows sideways, every control staying reachable. `src: UI/UX notes para 8`
- [ ] `C-UX-48` `ui` A phone held upright is asked to rotate rather than given a cramped layout. `src: UI/UX notes para 8`
- [ ] `C-UX-49` `constraint` The interface never reads as a website pasted over a game, with a navigation bar, cards, a footer. `src: UI/UX notes para 9`
- [ ] `C-UX-50` `constraint` A frozen photograph never stands where a running scene belongs. `src: UI/UX notes para 9`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The rendering model is server-rendered HTML with hydrated islands. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The first document carries the hidden title, the hidden description rather than an empty shell. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The page is built with SolidStart in TypeScript. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The HTTP API is built with Express on the same origin under `/api`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The world is drawn with WebGL through three. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` Persistence is PostgreSQL. `src: Technical requirements para 1`
- [ ] `C-TR-07` `literal` The database is reached at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-08` `literal` The app address, port are read from `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. `src: Technical requirements para 1`
- [ ] `C-TR-09` `constraint` No host or port is hardcoded. `src: Technical requirements para 1`
- [ ] `C-TR-10` `constraint` PostgreSQL is already running, never installed by the app. `src: Technical requirements para 1`
- [ ] `C-TR-11` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements para 2`
- [ ] `C-TR-12` `capability` The live board is served by the app on the app's own origin. `src: Technical requirements para 2`
- [ ] `C-TR-13` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements para 3, Deployment contract bullet 3`
- [ ] `C-TR-14` `contract` Request logs go to standard output, one line per request with method, path, outcome. `src: Technical requirements para 3`
- [ ] `C-TR-15` `contract` Every script, stylesheet, font file carries a content hash in the file name. `src: Technical requirements para 5`
- [ ] `C-TR-16` `literal` Those files carry `Cache-Control` containing `immutable` with a max-age of at least `31536000` seconds. `src: Technical requirements para 5`
- [ ] `C-TR-17` `constraint` Fonts are served in WOFF2 only, subset to Latin, French characters. `src: Technical requirements para 5`
- [ ] `C-TR-18` `literal` Any shipped WebAssembly is served as `application/wasm`. `src: Technical requirements para 5`
- [ ] `C-TR-19` `constraint` Nothing the page needs is fetched from another host. `src: Technical requirements para 5`
- [ ] `C-TR-20` `constraint` The page sets no cookie. `src: Technical requirements para 5`
- [ ] `C-TR-21` `constraint` No photograph, raster sprite, animated image, audio file, video, model file, texture file is downloaded. `src: Technical requirements para 6`
- [ ] `C-TR-22` `capability` Every model, texture, mark, diagram, sound is generated in the browser, the loading figure included. `src: Technical requirements para 6`
- [ ] `C-TR-23` `constraint` The only binary files served are WOFF2 fonts plus the social preview image. `src: Technical requirements para 6, Constraints bullet 6`
- [ ] `C-TR-24` `capability` A panel reads game state, never driving the world. `src: Technical requirements para 7`
- [ ] `C-TR-25` `capability` Closing a panel leaves nothing running behind the panel. `src: Technical requirements para 7`
- [ ] `C-TR-26` `capability` The site keeps pace after a long session of opening, closing layers. `src: Technical requirements para 7`
- [ ] `C-TR-27` `constraint` Development tooling, tuning panels, debug markers stay out of the production build. `src: Technical requirements para 7`
- [ ] `C-TR-28` `literal` The document body never carries a `debug` class. `src: Technical requirements para 7`

## C-DM Data model

- [ ] `C-DM-01` `data` Six tables exist; all timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-02` `contract` The seeded password is written into `/app/USER_README.md` beside each account. `src: Data model password paragraph`
- [ ] `C-DM-03` `data` Table `account` holds `id`, unique `email`, `password_hash`, `role` of `owner`, `created_at`. `src: Data model account`
- [ ] `C-DM-04` `data` Table `session` holds `id`, `account_id`, unique `token`, `expires_at` thirty days from issue. `src: Data model session`
- [ ] `C-DM-05` `data` Table `game` holds `id`, `label`, `zone`, `max_total`, `position`. `src: Data model game`
- [ ] `C-DM-06` `data` Table `game_item` holds `id`, `game_id`, `key`, `label`, `worth`, `max_count`, `position`, one row per item. `src: Data model game_item`
- [ ] `C-DM-07` `data` Table `run` holds `id`, unique opaque `run_token`, `game_id`, `player_id`, `started_at`, `used_at`. `src: Data model run`
- [ ] `C-DM-08` `constraint` A `run_token` is never derived from the `player_id`. `src: Data model run`
- [ ] `C-DM-09` `data` Column `used_at` stays empty until an entry for the run is accepted. `src: Data model run`
- [ ] `C-DM-10` `data` Table `leaderboard_entry` holds integer `id` served as `entry_id`, `game_id`, unique `run_id`, `name`, `name_removed`, `total`, `counts`, `created_at`. `src: Data model leaderboard_entry`
- [ ] `C-DM-11` `data` Column `counts` is a JSON object mapping each item key to a count. `src: Data model leaderboard_entry`
- [ ] `C-DM-12` `constraint` An entry `game_id` always equals the run `game_id`. `src: Data model invariants paragraph`
- [ ] `C-DM-13` `constraint` An entry `total` always equals the sum of counts times worths, never above `max_total`. `src: Data model invariants paragraph`
- [ ] `C-DM-14` `constraint` Removing a name sets `name_removed`, never deleting the row, never changing `total`. `src: Data model invariants paragraph`
- [ ] `C-DM-15` `capability` Rank, served name, top ten are derived rather than stored. `src: Data model derived line`
- [ ] `C-DM-16` `literal` Seed data holds the owner account `owner@example.com` with role `owner`. `src: Data model seed paragraph`
- [ ] `C-DM-17` `capability` Seed data holds the four games, eleven items exactly as tabled. `src: Data model seed paragraph`
- [ ] `C-DM-18` `literal` Orchard seeds `Mathilde` `1180`, `Yanis` `1040`, `Capucine` `990`, `Oscar` `870`, `Léa` `760`. `src: Data model seed table rows 1 to 5`
- [ ] `C-DM-19` `literal` Orchard seeds `Nour` `640`, `Hugo` `640`, `Inès` `410`, `Basile` `300`, `Zoé` `180`. `src: Data model seed table rows 6 to 10`
- [ ] `C-DM-20` `capability` Every seeded entry stores the tabled counts. `src: Data model seed table counts column`
- [ ] `C-DM-21` `literal` Lighthouse seeds `Admin Vireo` `2080`, `Margaux` `1640`, `Timothée` `960`. `src: Data model seed table rows 11 to 13`
- [ ] `C-DM-22` `literal` Ski seeds `Élodie` `1500` with `portes 20`, `sauts 10`, `drapeaux 3`. `src: Data model seed table row 14`
- [ ] `C-DM-23` `capability` Every seeded entry has a run of its own, already used. `src: Data model seed paragraph`
- [ ] `C-DM-24` `capability` Seeded entries are created in the listed order. `src: Data model seed paragraph`
- [ ] `C-DM-25` `literal` On the orchard board `Nour` ranks `6`, `Hugo` ranks `7`. `src: Data model seed closing paragraph`
- [ ] `C-DM-26` `literal` The lighthouse board serves `Admin Vireo` at rank `1` as `Voyageur anonyme`. `src: Data model seed closing paragraph`
- [ ] `C-DM-27` `capability` The flight board has no entries. `src: Data model seed closing paragraph`
- [ ] `C-DM-28` `constraint` Seeding is idempotent, a restart never duplicating rows. `src: Data model closing line`

## C-FE Front-end specification

- [ ] `C-FE-01` `capability` Nothing in the interface is sized apart from the root except hairlines, the touch pad. `src: Front-end specification, The scaling model and the stack of layers`
- [ ] `C-FE-02` `capability` Layers follow one ordered list of named places with gaps between the places. `src: Front-end specification, The scaling model and the stack of layers`
- [ ] `C-FE-03` `capability` A dialogue never covers the Menu control. `src: Front-end specification, The scaling model and the stack of layers`
- [ ] `C-FE-04` `capability` The rotate prompt sits above every other layer, the loading screen included. `src: Front-end specification, The scaling model and the stack of layers`
- [ ] `C-FE-05` `capability` The touch pad sits above every other layer. `src: Front-end specification, The scaling model and the stack of layers`
- [ ] `C-FE-06` `ui` The world layer never fades; every layer fades over the world. `src: Front-end specification, The scaling model and the stack of layers`
- [ ] `C-FE-07` `ui` The change-over wipe is near-black, taking the pointer when showing. `src: Front-end specification, The scaling model and the stack of layers`
- [ ] `C-FE-08` `ui` The key ring sits after the pill label, the gap growing with screen height. `src: Front-end specification, The pill button and the key ring`
- [ ] `C-FE-09` `ui` On the receipt, board panels the pill fills dark with a light label. `src: Front-end specification, The pill button and the key ring`
- [ ] `C-FE-10` `ui` The key ring is a thin circle on the edge of a box one-and-a-half times the label size, the letter a centred capital. `src: Front-end specification, The pill button and the key ring`
- [ ] `C-FE-11` `ui` A key ring turns dark when a pill fills light behind the ring. `src: Front-end specification, The pill button and the key ring`
- [ ] `C-FE-12` `ui` Dialogue choice buttons drop the outline. `src: Front-end specification, The pill button and the key ring`
- [ ] `C-FE-13` `ui` The Menu control is two interlocking paper gears turning slowly, lit by the world sun. `src: Front-end specification, The two corner controls`
- [ ] `C-FE-14` `capability` The Menu control, the notebook control each render in a canvas of their own. `src: Front-end specification, The two corner controls`
- [ ] `C-FE-15` `capability` The notebook control appears only in the world, not on the home screen. `src: Front-end specification, The two corner controls`
- [ ] `C-FE-16` `ui` The notebook control is a paper satchel with a handle, twice the size of the gears. `src: Front-end specification, The two corner controls`
- [ ] `C-FE-17` `capability` Both corner controls keep a name, a key in the accessibility tree, showing neither on screen. `src: Front-end specification, The two corner controls`
- [ ] `C-FE-18` `capability` Interface 3D surfaces redraw only on change, stopping when hidden. `src: Front-end specification, The two corner controls`
- [ ] `C-FE-19` `ui` The loading figure stays centred at three tenths of the screen height on laptop, phone. `src: Front-end specification, The loading screen`
- [ ] `C-FE-20` `ui` The tips sit stacked in one place at the bottom of the loading screen. `src: Front-end specification, The loading screen`
- [ ] `C-FE-21` `ui` A paper-coloured ellipse with LOADING stands before the figure renders, the figure fading in over the ellipse. `src: Front-end specification, The loading screen`
- [ ] `C-FE-22` `ui` On a wide screen the title sits near a ninth of the height, Voyager in the lower third, Contact at the bottom edge. `src: Front-end specification, The home composition`
- [ ] `C-FE-23` `ui` On a narrow screen the title sits a tenth of the way down. `src: Front-end specification, The home composition`
- [ ] `C-FE-24` `capability` The whole title fits on one line at a tablet width held sideways. `src: Front-end specification, The home composition`
- [ ] `C-FE-25` `ui` Bienvenue sits in a softly rounded centred panel about half the screen width, nine tenths on narrow screens. `src: Front-end specification, The instruction panel`
- [ ] `C-FE-26` `capability` The instruction caption is italic at three quarters of the text size. `src: Front-end specification, The instruction panel`
- [ ] `C-FE-27` `capability` The instruction panel carries one line of title. `src: Front-end specification, The instruction panel`
- [ ] `C-FE-28` `capability` The dialogue spans the full width at the bottom with text held to four fifths of the width. `src: Front-end specification, Dialogue, prompt, title card and collect ceremony`
- [ ] `C-FE-29` `ui` The dialogue shadow is a gradient from almost black to transparent with a plain black fallback. `src: Front-end specification, Dialogue, prompt, title card and collect ceremony`
- [ ] `C-FE-30` `ui` Each dialogue line, dialogue button carries a soft drop shadow. `src: Front-end specification, Dialogue, prompt, title card and collect ceremony`
- [ ] `C-FE-31` `capability` The zone title card is `Lato` at thickness `200`, centred between hairlines, never wider than half the screen. `src: Front-end specification, Dialogue, prompt, title card and collect ceremony`
- [ ] `C-FE-32` `ui` The zone title card has five times as much side space as top space. `src: Front-end specification, Dialogue, prompt, title card and collect ceremony`
- [ ] `C-FE-33` `ui` The collect ceremony wash is translucent black, taking the pointer, with two bursts from one image, the second inverted, a second behind. `src: Front-end specification, Dialogue, prompt, title card and collect ceremony`
- [ ] `C-FE-34` `capability` The orchard clock is `Lato` bold at three root units; the tally is bold at two root units. `src: Front-end specification, The minigame displays`
- [ ] `C-FE-35` `ui` Swelling scales up then settles; shuddering ends where shuddering started; the warning pulse is smaller, slower, repeating. `src: Front-end specification, The minigame displays`
- [ ] `C-FE-36` `ui` Lighthouse, ski rows are spaced in their own units, drawing in toward the edge on narrow screens. `src: Front-end specification, The minigame displays`
- [ ] `C-FE-37` `ui` The flight display declares an own colour block, changing no site colour, filled, empty life cells swapping colours. `src: Front-end specification, The minigame displays`
- [ ] `C-FE-38` `ui` Flight tallies sit two units in from the bottom corners; the life strip sits one unit in from the right edge. `src: Front-end specification, The minigame displays`
- [ ] `C-FE-39` `capability` The receipt is a centred paper panel, the only scrolling region, scrolling when taller than nine tenths of the screen. `src: Front-end specification, The receipt and the board`
- [ ] `C-FE-40` `ui` Each receipt row is silhouette, italic label over count, bold worth; Total sits three row-gaps below with a number half again as large. `src: Front-end specification, The receipt and the board`
- [ ] `C-FE-41` `ui` The board is a paper panel with the title between two rules running to the panel edges. `src: Front-end specification, The receipt and the board`
- [ ] `C-FE-42` `capability` A long name shrinks in the name column rather than pushing the total off the panel. `src: Front-end specification, The receipt and the board`
- [ ] `C-FE-43` `ui` Rows arrive alternately from one side, the form from the other, each fading in over half a second. `src: Front-end specification, The receipt and the board`
- [ ] `C-FE-44` `ui` The name form sits on a translucent light pill with a rule beneath, the field underlined rather than boxed. `src: Front-end specification, The receipt and the board`
- [ ] `C-FE-45` `capability` The notebook spread is one-and-a-half times as wide as tall. `src: Front-end specification, The notebook`
- [ ] `C-FE-46` `capability` The notebook height is the smaller of four fifths of the screen height, half the screen width. `src: Front-end specification, The notebook`
- [ ] `C-FE-47` `ui` Notebook pages turn in three dimensions around the spine with binder rings floating in front. `src: Front-end specification, The notebook`
- [ ] `C-FE-48` `capability` The space around the notebook lets the pointer through; the pages do not. `src: Front-end specification, The notebook`
- [ ] `C-FE-49` `ui` The forward page control tilts, grows the label, slides the arrow; the back control tilts the other way, growing the arrow. `src: Front-end specification, The notebook`
- [ ] `C-FE-50` `ui` Openable page items swell slightly, drawing a hairline from the middle outward. `src: Front-end specification, The notebook`
- [ ] `C-FE-51` `ui` Touch buttons are translucent white circles with a thin white edge, glyphs at half size, the stick twice a button. `src: Front-end specification, The touch pad and the settings panel`
- [ ] `C-FE-52` `ui` The settings panel is a paper-coloured column with bold legends, an icon leading each label. `src: Front-end specification, The touch pad and the settings panel`
- [ ] `C-FE-53` `ui` Models are simple shapes with faceted surfaces in one flat paper material. `src: Front-end specification, The generated world`
- [ ] `C-FE-54` `ui` The character hat brim lags a moment behind the head. `src: Front-end specification, The generated world`
- [ ] `C-FE-55` `ui` Walking swings the legs with counter-swinging arms; running widens the arc, pitching the torso forward. `src: Front-end specification, The generated world`
- [ ] `C-FE-56` `ui` The sky is a generated gradient, deep blue above, warm pale at the horizon, with a softened sun. `src: Front-end specification, The generated world`
- [ ] `C-FE-57` `ui` Trees are faceted trunks with leaf cards in three greens, a deep muted lime for the darkest foliage. `src: Front-end specification, The generated world`
- [ ] `C-FE-58` `ui` Water ripples between a deep, a mid blue-green by depth with a sun highlight. `src: Front-end specification, The generated world`
- [ ] `C-FE-59` `ui` A warm key light from one side, a cool fill light from the other light the world. `src: Front-end specification, The generated world`
- [ ] `C-FE-60` `ui` The world uses depth of field, a soft glow on bright spots, a colour grade held as data. `src: Front-end specification, The generated world`
- [ ] `C-FE-61` `capability` Keyboard, controller, rotating-phone drawings, the return-key mark, star marks, bursts are drawn by code. `src: Front-end specification, The generated world`
- [ ] `C-FE-62` `capability` Counter silhouettes are collected models rendered once, crushed to black. `src: Front-end specification, The generated world`
- [ ] `C-FE-63` `capability` The music bed is detuned tones under a moving filter; the sea rises, falls about every twelve seconds. `src: Front-end specification, The generated sound`
- [ ] `C-FE-64` `capability` The wind level follows how exposed the character is. `src: Front-end specification, The generated sound`
- [ ] `C-FE-65` `capability` The click is a short high tone; the snow footstep is brighter, longer than the grass footstep. `src: Front-end specification, The generated sound`
- [ ] `C-FE-66` `capability` Repeated sounds are pooled so fast footsteps never stall. `src: Front-end specification, The generated sound`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product is one page, one maker, one world with no multi-tenancy. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The product has no project index, no case study pages, no about page. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The contact destination is one outbound link, never a form. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` The product has no follows beside the absent comments, likes, chat, messaging. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The leaderboard is the only shared surface. `src: Constraints bullet 3`
- [ ] `C-CN-06` `constraint` The product has no analytics, tracking, fingerprinting, consent banner, cookie. `src: Constraints bullet 4`
- [ ] `C-CN-07` `constraint` The app makes no external network calls at run time, no third-party request. `src: Constraints bullet 4`
- [ ] `C-CN-08` `constraint` The product has no payments, no uploads, no email. `src: Constraints bullet 5`
- [ ] `C-CN-09` `constraint` The build succeeds with an empty asset directory. `src: Constraints bullet 6`
- [ ] `C-CN-10` `constraint` The measured site's own world, maker name, hosts appear nowhere. `src: Constraints bullet 6`
- [ ] `C-CN-11` `constraint` The product has no native application, no offline play, no second language build. `src: Constraints bullet 7`
- [ ] `C-CN-12` `constraint` The owner removes names through the API with no moderation page. `src: Constraints bullet 8`
- [ ] `C-CN-13` `capability` The app stays responsive at tens of thousands of entries per board. `src: Constraints bullet 10`
- [ ] `C-CN-14` `capability` The app stays responsive with a few hundred viewers holding boards open. `src: Constraints bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `contract` A production build is served, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session, never a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0`, never `127.0.0.1` or `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `contract` Backing services are already running; no copy is downloaded, installed, started. `src: Deployment contract bullet 10`
- [ ] `C-DC-11` `contract` Only the named providers are used, with no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-12` `contract` No persistent volumes, fixed container names, custom networks are used. `src: Deployment contract bullet 12`
- [ ] `C-DC-13` `contract` API field names are exact; a list endpoint returns a top-level JSON array. `src: Deployment contract API shapes paragraph`
- [ ] `C-DC-14` `contract` An invalid or unauthorized call is a client error with a reason, never a server error, never a silent success. `src: Deployment contract API shapes paragraph`
- [ ] `C-DC-15` `contract` An unknown game in a path answers not-found. `src: Deployment contract API shapes paragraph`
- [ ] `C-DC-16` `contract` Bearer auth is required on the two owner endpoints, on nothing else. `src: Deployment contract API shapes paragraph`
- [ ] `C-DC-17` `contract` `POST /api/auth/login` takes `{ email, password }`, returning `{ access_token }`. `src: Deployment contract API shapes row 2`
- [ ] `C-DC-18` `contract` `GET /api/games` returns rows of `{ id, label, zone, max_total, items }` with items of `{ key, label, worth, max }`. `src: Deployment contract API shapes row 3`
- [ ] `C-DC-19` `contract` `POST /api/runs` takes `{ game, player_id }`, returning `{ run_token, game, started_at }`. `src: Deployment contract API shapes row 4`
- [ ] `C-DC-20` `contract` `POST /api/entries` takes `{ run_token, game, name, counts, total }`, returning `{ entry_id, game, name, total, rank }`. `src: Deployment contract API shapes row 5`
- [ ] `C-DC-21` `contract` `GET /api/leaderboards/{game}` returns at most ten `{ rank, entry_id, name, total }` rows, best first. `src: Deployment contract API shapes row 6`
- [ ] `C-DC-22` `contract` `GET /api/leaderboards/{game}/events` is a `text/event-stream` with events `leaderboard`, `leaderboardUpdated` carrying the board array. `src: Deployment contract API shapes row 7`
- [ ] `C-DC-23` `contract` `GET /api/moderation/entries` with `?game=` returns `{ entry_id, name, name_removed, total, created_at }` rows, newest first, for the owner only. `src: Deployment contract API shapes row 8`
- [ ] `C-DC-24` `contract` `DELETE /api/entries/{entry_id}/name` returns `{ entry_id, name, name_removed, total }` for the owner only. `src: Deployment contract API shapes row 9`
- [ ] `C-DC-25` `constraint` A board in page memory, a module-variable entry list, a timer re-read, a replayed stream, an unrecomputed total, a button-only one-send rule are violations. `src: Deployment contract No mocks`
- [ ] `C-DC-26` `contract` PostgreSQL is the fact; the interface, the app tables only reflect the provider. `src: Deployment contract No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Contact` | The only outbound link is the value. | C-OV-14 | Overview para 3 |
| `owner@example.com` | One account is seeded, the value with role the value. | C-RL-23 | User roles seeded account table |
| `owner` | One account is seeded, the value with role the value. | C-RL-23 | User roles seeded account table |
| `deku-demo-pw-2026` | The seeded account uses the password the value. | C-RL-24 | User roles seeded account line, Data model password paragraph |
| `player_id` | A the value is the value to the value characters drawn from letters, digits, hyphens. | C-CF-03 | Core features, The leaderboard service para 1 |
| `8` | A the value is the value to the value characters drawn from letters, digits, hyphens. | C-CF-03 | Core features, The leaderboard service para 1 |
| `64` | A the value is the value to the value characters drawn from letters, digits, hyphens. | C-CF-03 | Core features, The leaderboard service para 1 |
| `0` | Each count is a whole number from the value up to the item maximum. | C-CF-17 | Core features, The leaderboard service rule 3 |
| `pommes 12` | Orchard counts the value, the value, the value sent with total the value are ... | C-CF-26 | Core features, The leaderboard service rule 3 table row 1 |
| `bananes 3` | Orchard counts the value, the value, the value sent with total the value are ... | C-CF-26 | Core features, The leaderboard service rule 3 table row 1 |
| `bonus 1` | Orchard counts the value, the value, the value sent with total the value are ... | C-CF-26 | Core features, The leaderboard service rule 3 table row 1 |
| `245` | Orchard counts the value, the value, the value sent with total the value are ... | C-CF-26 | Core features, The leaderboard service rule 3 table row 1 |
| `250` | The same orchard counts sent with total the value are refused. | C-CF-27 | Core features, The leaderboard service rule 3 table row 2 |
| `pommes 61` | Orchard count the value sent with total the value is refused. | C-CF-28 | Core features, The leaderboard service rule 3 table row 3 |
| `610` | Orchard count the value sent with total the value is refused. | C-CF-28 | Core features, The leaderboard service rule 3 table row 3 |
| `pommes 60` | Orchard counts the value, the value, the value sent with total the value ar... | C-CF-29 | Core features, The leaderboard service rule 3 table row 4 |
| `bananes 20` | Orchard counts the value, the value, the value sent with total the value ar... | C-CF-29 | Core features, The leaderboard service rule 3 table row 4 |
| `bonus 5` | Orchard counts the value, the value, the value sent with total the value ar... | C-CF-29 | Core features, The leaderboard service rule 3 table row 4 |
| `1350` | Orchard counts the value, the value, the value sent with total the value ar... | C-CF-29 | Core features, The leaderboard service rule 3 table row 4 |
| `cerises 2` | Orchard count the value sent with total the value is refused. | C-CF-30 | Core features, The leaderboard service rule 3 table row 5 |
| `20` | Orchard count the value sent with total the value is refused. | C-CF-30 | Core features, The leaderboard service rule 3 table row 5 |
| `3` | One the value starts at most the value runs in any the value seconds. | C-CF-31 | Core features, The leaderboard service rule 4 |
| `60` | One the value starts at most the value runs in any the value seconds. | C-CF-31 | Core features, The leaderboard service rule 4 |
| `10` | A board lists at most the value rows. | C-CF-35 | Core features, The leaderboard service rule 5 |
| `Voyageur anonyme` | A stored name failing the reserved-word rule is served as the value. | C-CF-49 | Core features, The leaderboard service rule 7 |
| `access_token` | A successful sign-in returns a bearer token as the value. | C-CF-59 | Core features, Auth |
| `orchard` | Game the value carries label the value, zone the value. | C-CF-66 | Core features, The four minigames and their boards table rows 1 to 3 |
| `La Cueillette` | Game the value carries label the value, zone the value. | C-CF-66 | Core features, The four minigames and their boards table rows 1 to 3 |
| `Le Verger` | Game the value carries label the value, zone the value. | C-CF-66 | Core features, The four minigames and their boards table rows 1 to 3 |
| `pommes` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `Pommes` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `bananes` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `Bananes` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `25` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `bonus` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `Bonus` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `50` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `5` | Orchard items are the value the value worth the value max the value, the value the value ... | C-CF-67 | Core features, The four minigames and their boards table rows 1 to 3 |
| `lighthouse` | Game the value carries label the value, zone the value. | C-CF-68 | Core features, The four minigames and their boards table rows 4 to 5 |
| `La Veille du Phare` | Game the value carries label the value, zone the value. | C-CF-68 | Core features, The four minigames and their boards table rows 4 to 5 |
| `Le Phare` | Game the value carries label the value, zone the value. | C-CF-68 | Core features, The four minigames and their boards table rows 4 to 5 |
| `navires` | Lighthouse items are the value the value worth the value max the value, `tempete... | C-CF-69 | Core features, The four minigames and their boards table rows 4 to 5 |
| `Navires guidés` | Lighthouse items are the value the value worth the value max the value, `tempete... | C-CF-69 | Core features, The four minigames and their boards table rows 4 to 5 |
| `40` | Lighthouse items are the value the value worth the value max the value, `tempete... | C-CF-69 | Core features, The four minigames and their boards table rows 4 to 5 |
| `30` | Lighthouse items are the value the value worth the value max the value, `tempete... | C-CF-69 | Core features, The four minigames and their boards table rows 4 to 5 |
| `tempetes` | Lighthouse items are the value the value worth the value max the value, `tempete... | C-CF-69 | Core features, The four minigames and their boards table rows 4 to 5 |
| `Tempêtes traversées` | Lighthouse items are the value the value worth the value max the value, `tempete... | C-CF-69 | Core features, The four minigames and their boards table rows 4 to 5 |
| `100` | Lighthouse items are the value the value worth the value max the value, `tempete... | C-CF-69 | Core features, The four minigames and their boards table rows 4 to 5 |
| `ski` | Game the value carries label the value, zone the value. | C-CF-70 | Core features, The four minigames and their boards table rows 6 to 8 |
| `La Descente` | Game the value carries label the value, zone the value. | C-CF-70 | Core features, The four minigames and their boards table rows 6 to 8 |
| `Les Hautes Neiges` | Game the value carries label the value, zone the value. | C-CF-70 | Core features, The four minigames and their boards table rows 6 to 8 |
| `portes` | Ski items are the value the value worth the value max the value, the value `Sauts... | C-CF-71 | Core features, The four minigames and their boards table rows 6 to 8 |
| `Portes franchies` | Ski items are the value the value worth the value max the value, the value `Sauts... | C-CF-71 | Core features, The four minigames and their boards table rows 6 to 8 |
| `sauts` | Ski items are the value the value worth the value max the value, the value `Sauts... | C-CF-71 | Core features, The four minigames and their boards table rows 6 to 8 |
| `Sauts réussis` | Ski items are the value the value worth the value max the value, the value `Sauts... | C-CF-71 | Core features, The four minigames and their boards table rows 6 to 8 |
| `15` | Ski items are the value the value worth the value max the value, the value `Sauts... | C-CF-71 | Core features, The four minigames and their boards table rows 6 to 8 |
| `drapeaux` | Ski items are the value the value worth the value max the value, the value `Sauts... | C-CF-71 | Core features, The four minigames and their boards table rows 6 to 8 |
| `Drapeaux cueillis` | Ski items are the value the value worth the value max the value, the value `Sauts... | C-CF-71 | Core features, The four minigames and their boards table rows 6 to 8 |
| `flight` | Game the value carries label the value, zone the value. | C-CF-72 | Core features, The four minigames and their boards table rows 9 to 11 |
| `Le Vol` | Game the value carries label the value, zone the value. | C-CF-72 | Core features, The four minigames and their boards table rows 9 to 11 |
| `La Grève` | Game the value carries label the value, zone the value. | C-CF-72 | Core features, The four minigames and their boards table rows 9 to 11 |
| `cibles` | Flight items are the value the value worth the value max the value, the value `C... | C-CF-73 | Core features, The four minigames and their boards table rows 9 to 11 |
| `Cibles touchées` | Flight items are the value the value worth the value max the value, the value `C... | C-CF-73 | Core features, The four minigames and their boards table rows 9 to 11 |
| `canons` | Flight items are the value the value worth the value max the value, the value `C... | C-CF-73 | Core features, The four minigames and their boards table rows 9 to 11 |
| `Canons trouvés` | Flight items are the value the value worth the value max the value, the value `C... | C-CF-73 | Core features, The four minigames and their boards table rows 9 to 11 |
| `6` | Flight items are the value the value worth the value max the value, the value `C... | C-CF-73 | Core features, The four minigames and their boards table rows 9 to 11 |
| `anneaux` | Flight items are the value the value worth the value max the value, the value `C... | C-CF-73 | Core features, The four minigames and their boards table rows 9 to 11 |
| `Anneaux traversés` | Flight items are the value the value worth the value max the value, the value `C... | C-CF-73 | Core features, The four minigames and their boards table rows 9 to 11 |
| `2200` | Maximum totals are the value for the value, the value for the value, the value for ... | C-CF-74 | Core features, The four minigames and their boards para 2 |
| `2600` | Maximum totals are the value for the value, the value for the value, the value for ... | C-CF-74 | Core features, The four minigames and their boards para 2 |
| `2800` | Maximum totals are the value for the value, the value for the value, the value for ... | C-CF-74 | Core features, The four minigames and their boards para 2 |
| `La gardienne du verger` | The keepers are the value, the value, `La monitric... | C-CF-76 | Core features, The four minigames and their boards table keeper column |
| `Le gardien du phare` | The keepers are the value, the value, `La monitric... | C-CF-76 | Core features, The four minigames and their boards table keeper column |
| `La monitrice des cimes` | The keepers are the value, the value, `La monitric... | C-CF-76 | Core features, The four minigames and their boards table keeper column |
| `Le portail du vent` | The keepers are the value, the value, `La monitric... | C-CF-76 | Core features, The four minigames and their boards table keeper column |
| `90` | The lighthouse clock starts at the value seconds. | C-CF-84 | Core features, The four minigames and their boards rule 2 |
| `120` | A ski run ends at the finish line or after the value seconds. | C-CF-86 | Core features, The four minigames and their boards rule 3 |
| `Canon` | Two weapons, the value, the value, can be picked up in Le Vol, each announc... | C-CF-90 | Core features, The four minigames and their boards rule 4 |
| `Super canon` | Two weapons, the value, the value, can be picked up in Le Vol, each announc... | C-CF-90 | Core features, The four minigames and their boards rule 4 |
| `Parler` | Standing at a keeper brings up the prompt the value with the key the value. | C-CF-91 | Core features, The four minigames and their boards rule 5 |
| `E` | Standing at a keeper brings up the prompt the value with the key the value. | C-CF-91 | Core features, The four minigames and their boards rule 5 |
| `Commencer` | Acting on the prompt opens the keeper dialogue with the choices the value, ... | C-CF-92 | Core features, The four minigames and their boards rule 5 |
| `Plus tard` | Acting on the prompt opens the keeper dialogue with the choices the value, ... | C-CF-92 | Core features, The four minigames and their boards rule 5 |
| `Soixante secondes pour remplir le panier. Les fruits pourris vous coûtent une pomme.` | The orchard keeper says `Soixante secondes pour remplir le panier. Les fruits... | C-CF-95 | Core features, The four minigames and their boards rule 5 table row 1 |
| `Guidez les navires entre les récifs avant que la tempête ne tombe.` | The lighthouse keeper says `Guidez les navires entre les récifs avant que la ... | C-CF-96 | Core features, The four minigames and their boards rule 5 table row 2 |
| `Passez les portes, osez les sauts, cueillez les drapeaux jusqu’en bas.` | The ski keeper says `Passez les portes, osez les sauts, cueillez les drapeaux... | C-CF-97 | Core features, The four minigames and their boards rule 5 table row 3 |
| `Le vent vous portera tant que votre coque tiendra.` | The wind portal says the value | C-CF-98 | Core features, The four minigames and their boards rule 5 table row 4 |
| `Terminer la course` | During a run the Menu offers the value. | C-CF-99 | Core features, The four minigames and their boards rule 6 |
| `Journal` | The first finished orchard run adds the the value entry `J’ai vu un pont appa... | C-CF-103 | Core features, The four minigames and their boards rule 7 |
| `J’ai vu un pont apparaître entre le Promontoire et le Bois Murmurant.` | The first finished orchard run adds the the value entry `J’ai vu un pont appa... | C-CF-103 | Core features, The four minigames and their boards rule 7 |
| `2` | A name is the value to the value characters long after trimming. | C-CF-106 | Core features, The name rule |
| `16` | A name is the value to the value characters long after trimming. | C-CF-106 | Core features, The name rule |
| `admin` | A name containing the value, the value, the value or the value is ref... | C-CF-109 | Core features, The name rule |
| `modérateur` | A name containing the value, the value, the value or the value is ref... | C-CF-109 | Core features, The name rule |
| `vireo` | A name containing the value, the value, the value or the value is ref... | C-CF-109 | Core features, The name rule |
| `voyageur anonyme` | A name containing the value, the value, the value or the value is ref... | C-CF-109 | Core features, The name rule |
| `LOADING` | The word the value sits beneath the loading figure. | C-CF-116 | Core features, The loading screen rule 2 |
| `Utilisez les flèches directionnelles, ainsi que la souris, pour jouer.` | Tip 1 reads `Utilisez les flèches directionnelles, ainsi que la souris, pour ... | C-CF-124 | Core features, The loading screen table row 1 |
| `Vous pouvez utiliser une manette de jeu pour jouer.` | Tip 2 reads the value | C-CF-125 | Core features, The loading screen table row 2 |
| `N’hésitez pas à revenir sur vos pas : certains lieux révèlent de nouveaux chemins quand le monde a changé.` | Tip 3 reads `N’hésitez pas à revenir sur vos pas : certains lieux révèlent de... | C-CF-126 | Core features, The loading screen table row 3 |
| `Parlez aux voyageurs que vous croisez : leurs mots sont parfois des portes, et leurs silences des indices.` | Tip 4 reads `Parlez aux voyageurs que vous croisez : leurs mots sont parfois ... | C-CF-127 | Core features, The loading screen table row 4 |
| `Le Golem de Vigie peut grandement vous aider dans la quête : écoutez ce que la mer lui apprend.` | Tip 5 reads `Le Golem de Vigie peut grandement vous aider dans la quête : éco... | C-CF-128 | Core features, The loading screen table row 5 |
| `Certains passages sont bien cachés : n’hésitez pas à fouiller partout, observer les recoins et suivre les détails que le monde laisse derrière lui.` | Tip 6 reads `Certains passages sont bien cachés : n’hésitez pas à fouiller pa... | C-CF-129 | Core features, The loading screen table row 6 |
| `Où sommeillent les Îles` | The display title reads the value. | C-CF-137 | Core features, The home screen rule 2 |
| `Un voyage à travers les créations d’un Creative Developer` | The subtitle reads the value. | C-CF-138 | Core features, The home screen rule 2 |
| `https://vireo.example/contact` | The link the value opens the value in a new window. | C-CF-145 | Core features, The home screen rule 4 |
| `(Nouvelle fenêtre)` | A visually hidden the value follows the the value label. | C-CF-146 | Core features, The home screen rule 4 |
| `Bienvenue` | The word the value replaces the title. | C-CF-153 | Core features, The instruction screen and the second load rule 1 |
| `Ce site est une expérience interactive mêlant jeu et portfolio.` | Instruction line 1 reads `Ce site est une expérience interactive mêlant jeu e... | C-CF-154 | Core features, The instruction screen and the second load table row 1 |
| `À travers un univers jouable et évolutif, j’y explore des idées, des mécaniques et des techniques du web créatif.` | Instruction line 2 reads `À travers un univers jouable et évolutif, j’y explo... | C-CF-155 | Core features, The instruction screen and the second load table row 2 |
| `Activez vos haut-parleurs ou un casque, utilisez votre souris ou un gamepad, puis explorez à votre rythme.` | Instruction line 3 reads `Activez vos haut-parleurs ou un casque, utilisez vo... | C-CF-156 | Core features, The instruction screen and the second load table row 3 |
| `Souris / Clavier · Gamepad · Touch` | The italic caption the value names the four ways t... | C-CF-157 | Core features, The instruction screen and the second load rule 2 |
| `Le Promontoire` | The opening zone is the value. | C-CF-167 | Core features, The world rule 1 |
| `Le Bois Murmurant` | The other four zones are the value, the value, `Les Neige... | C-CF-169 | Core features, The world rule 1 |
| `La Lande du Golem` | The other four zones are the value, the value, `Les Neige... | C-CF-169 | Core features, The world rule 1 |
| `Les Neiges` | The other four zones are the value, the value, `Les Neige... | C-CF-169 | Core features, The world rule 1 |
| `Le Dernier Seuil` | The other four zones are the value, the value, `Les Neige... | C-CF-169 | Core features, The world rule 1 |
| `Le monde ne peut pas être dessiné sur cet appareil.` | A browser unable to draw 3D keeps every interface layer with the notice `Le m... | C-CF-187 | Core features, The world rule 8, User flow states |
| `Total` | The receipt ends with a the value row set apart, half again as large. | C-CF-207 | Core features, The run loop: receipt, board and name form rule 1 |
| `Continuer` | The button the value with key Enter opens the board. | C-CF-209 | Core features, The run loop: receipt, board and name form rule 1 |
| `Votre nom` | The name form is one row with the bold label the value, an italic underline... | C-CF-219 | Core features, The run loop: receipt, board and name form rule 5 |
| `Envoyer` | The name form is one row with the bold label the value, an italic underline... | C-CF-219 | Core features, The run loop: receipt, board and name form rule 5 |
| `Résultat envoyé.` | An accepted send replaces the form with the note the value | C-CF-221 | Core features, The run loop: receipt, board and name form rule 5 |
| `Partir` | A board opened from the Menu offers the value, the value. | C-CF-227 | Core features, The run loop: receipt, board and name form rule 7 |
| `Fermer` | A board opened from the Menu offers the value, the value. | C-CF-227 | Core features, The run loop: receipt, board and name form rule 7 |
| `Ce classement attend son premier nom.` | A board with no entries shows the value | C-CF-229 | Core features, The run loop: receipt, board and name form rule 8 |
| `Menu` | The top-left Menu control is named the value, showing the key the value. | C-CF-230 | Core features, The Menu and its settings rule 1 |
| `M` | The top-left Menu control is named the value, showing the key the value. | C-CF-230 | Core features, The Menu and its settings rule 1 |
| `Reprendre` | The Menu panel carries the value. | C-CF-234 | Core features, The Menu and its settings rule 2 |
| `Classements` | The the value section lists the value, the value, `La De... | C-CF-235 | Core features, The Menu and its settings rule 2 |
| `Qualité` | Group the value offers the value, the value, the value, defaulting to the value. | C-CF-238 | Core features, The Menu and its settings rule 3 |
| `Basse` | Group the value offers the value, the value, the value, defaulting to the value. | C-CF-238 | Core features, The Menu and its settings rule 3 |
| `Moyenne` | Group the value offers the value, the value, the value, defaulting to the value. | C-CF-238 | Core features, The Menu and its settings rule 3 |
| `Haute` | Group the value offers the value, the value, the value, defaulting to the value. | C-CF-238 | Core features, The Menu and its settings rule 3 |
| `Volume de la musique` | Group the value offers the value, the value, the value. | C-CF-239 | Core features, The Menu and its settings rule 3 |
| `Bas` | Group the value offers the value, the value, the value. | C-CF-239 | Core features, The Menu and its settings rule 3 |
| `Moyen` | Group the value offers the value, the value, the value. | C-CF-239 | Core features, The Menu and its settings rule 3 |
| `Fort` | Group the value offers the value, the value, the value. | C-CF-239 | Core features, The Menu and its settings rule 3 |
| `Volume des effets` | Group the value offers the value, the value, the value. | C-CF-240 | Core features, The Menu and its settings rule 3 |
| `Taille du texte` | Group the value offers the value, the value. | C-CF-241 | Core features, The Menu and its settings rule 3 |
| `Normale` | Group the value offers the value, the value. | C-CF-241 | Core features, The Menu and its settings rule 3 |
| `Grande` | Group the value offers the value, the value. | C-CF-241 | Core features, The Menu and its settings rule 3 |
| `Animations` | Group the value offers the value, the value. | C-CF-242 | Core features, The Menu and its settings rule 3 |
| `Complètes` | Group the value offers the value, the value. | C-CF-242 | Core features, The Menu and its settings rule 3 |
| `Réduites` | Group the value offers the value, the value. | C-CF-242 | Core features, The Menu and its settings rule 3 |
| `Couper la musique` | Switches the value, the value each mute a group, keeping ... | C-CF-243 | Core features, The Menu and its settings rule 3 |
| `Couper les effets` | Switches the value, the value each mute a group, keeping ... | C-CF-243 | Core features, The Menu and its settings rule 3 |
| `Inverser l’axe vertical` | Switch the value inverts the camera vertical control. | C-CF-244 | Core features, The Menu and its settings rule 3 |
| `19px` | Text size the value keeps the root at the value, the value on narrow screens. | C-CF-252 | Core features, The Menu and its settings rule 7 |
| `12px` | Text size the value keeps the root at the value, the value on narrow screens. | C-CF-252 | Core features, The Menu and its settings rule 7 |
| `23px` | Text size the value sets the root to the value, the value on narrow screens. | C-CF-253 | Core features, The Menu and its settings rule 7 |
| `15px` | Text size the value sets the root to the value, the value on narrow screens. | C-CF-253 | Core features, The Menu and its settings rule 7 |
| `Carnet de voyage` | The notebook, the product inventory, is a ring binder titled `Carnet de voyag... | C-CF-255 | Core features, The notebook para 1, rule 1 |
| `Inventaire` | The bottom-right control is named the value, showing the key the value. | C-CF-256 | Core features, The notebook rule 1 |
| `I` | The bottom-right control is named the value, showing the key the value. | C-CF-256 | Core features, The notebook rule 1 |
| `Récoltes` | The notebook pages after the cover are the value, the value, the value, ... | C-CF-263 | Core features, The notebook rule 3 |
| `Trouvailles` | The notebook pages after the cover are the value, the value, the value, ... | C-CF-263 | Core features, The notebook rule 3 |
| `Rien pour l’instant, mais la route est longue.` | An empty notebook page reads the value | C-CF-267 | Core features, The notebook rule 3 |
| `Page suivante` | The notebook corners carry the value, the value. | C-CF-268 | Core features, The notebook rule 4 |
| `Page précédente` | The notebook corners carry the value, the value. | C-CF-268 | Core features, The notebook rule 4 |
| `Interagir` | A sideways touch screen shows an on-screen stick at the lower left, buttons `... | C-CF-285 | Core features, Input rule 4 |
| `Courir` | A sideways touch screen shows an on-screen stick at the lower left, buttons `... | C-CF-285 | Core features, Input rule 4 |
| `44` | Each touch control is at least the value CSS pixels across, never scaling with the... | C-CF-286 | Core features, Input rule 4 |
| `Les flèches directionnelles déplacent le personnage.` | A visually hidden description includes `Les flèches directionnelles déplacent... | C-CF-298 | Core features, Accessibility rule 2 |
| `Nouveau lieu, Le Promontoire` | A zone arrival is announced as the value for the opening... | C-CF-301 | Core features, Accessibility rule 4 |
| `Objet trouvé, ` | A found object is announced with the value before the object name. | C-CF-303 | Core features, Accessibility rule 4 |
| `Pommes, 3` | A tally change is announced as the label, a comma, the count, such as `Pommes... | C-CF-304 | Core features, Accessibility rule 4 |
| `Résultat envoyé, rang ` | A send is announced with the value before the rank. | C-CF-305 | Core features, Accessibility rule 4 |
| `Résultat refusé, ` | A refused send is announced with the value before the reason. | C-CF-306 | Core features, Accessibility rule 4 |
| `Creative Developer` | the value stays English inside the French subtitle. | C-CF-319 | Core features, Language and copy rule 4 |
| `Where Worlds Take Shape - Interactive WebGL Portfolio` | The page title is the value. | C-CF-322 | Core features, The published surface rule 1 |
| `A playable portfolio: walk a paper-craft world, meet its travellers` | The page description opens `A playable portfolio: walk a paper-craft world, m... | C-CF-323 | Core features, The published surface rule 1 |
| `post your best run to a public leaderboard.` | The page description ends the value | C-CF-324 | Core features, The published surface rule 1 |
| `/og-image.png` | The social preview image is the value. | C-CF-326 | Core features, The published surface rule 2 |
| `Vireo` | The page declares the site name the value, locale the value, alternate the value, a... | C-CF-327 | Core features, The published surface rule 2 |
| `fr_FR` | The page declares the site name the value, locale the value, alternate the value, a... | C-CF-327 | Core features, The published surface rule 2 |
| `en_US` | The page declares the site name the value, locale the value, alternate the value, a... | C-CF-327 | Core features, The published surface rule 2 |
| `1200` | The preview image resolves as a the value by the value PNG. | C-CF-328 | Core features, The published surface rule 2 |
| `630` | The preview image resolves as a the value by the value PNG. | C-CF-328 | Core features, The published surface rule 2 |
| `Page introuvable - Vireo` | The not-found page is titled the value. | C-CF-331 | Core features, The published surface rule 3 |
| `Cette adresse ne mène nulle part dans le monde de Vireo.` | The not-found page is described as `Cette adresse ne mène nulle part dans le ... | C-CF-332 | Core features, The published surface rule 3 |
| `Page introuvable` | The not-found page is headed the value with the link `Retour au voya... | C-CF-333 | Core features, The published surface rule 3, User flow entry paragraph |
| `Retour au voyage` | The not-found page is headed the value with the link `Retour au voya... | C-CF-333 | Core features, The published surface rule 3, User flow entry paragraph |
| `/` | The not-found page is headed the value with the link `Retour au voya... | C-CF-333 | Core features, The published surface rule 3, User flow entry paragraph |
| `Playfair Display` | the value carries the home title at the value, the value at the value. | C-UX-11 | UI/UX notes para 3 |
| `85.5px` | the value carries the home title at the value, the value at the value. | C-UX-11 | UI/UX notes para 3 |
| `114px` | the value carries the home title at the value, the value at the value. | C-UX-11 | UI/UX notes para 3 |
| `Lato` | the value carries body at the value in thickness the value, the subtitle at the value in... | C-UX-12 | UI/UX notes para 3 |
| `400` | the value carries body at the value in thickness the value, the subtitle at the value in... | C-UX-12 | UI/UX notes para 3 |
| `22.8px` | the value carries body at the value in thickness the value, the subtitle at the value in... | C-UX-12 | UI/UX notes para 3 |
| `20.9px` | the value carries body at the value in thickness the value, the subtitle at the value in... | C-UX-12 | UI/UX notes para 3 |
| `4.5:1` | Interface text over the world meets WCAG AA, at least the value against the bri... | C-UX-36 | UI/UX notes para 7 |
| `64em` | One breakpoint sits at the value wide, also applying under the value tall. | C-UX-40 | UI/UX notes para 8, Front-end specification scaling paragraph |
| `40.625em` | One breakpoint sits at the value wide, also applying under the value tall. | C-UX-40 | UI/UX notes para 8, Front-end specification scaling paragraph |
| `48px` | Below the breakpoint the home title becomes the value, the value becomes the value. | C-UX-42 | UI/UX notes para 8 |
| `60px` | Below the breakpoint the home title becomes the value, the value becomes the value. | C-UX-42 | UI/UX notes para 8 |
| `DATABASE_URL` | The database is reached at the value. | C-TR-07 | Technical requirements para 1 |
| `APP_PUBLIC_URL` | The app address, port are read from the value, the value. | C-TR-08 | Technical requirements para 1 |
| `APP_PUBLIC_PORT` | The app address, port are read from the value, the value. | C-TR-08 | Technical requirements para 1 |
| `Cache-Control` | Those files carry the value containing the value with a max-age of at... | C-TR-16 | Technical requirements para 5 |
| `immutable` | Those files carry the value containing the value with a max-age of at... | C-TR-16 | Technical requirements para 5 |
| `31536000` | Those files carry the value containing the value with a max-age of at... | C-TR-16 | Technical requirements para 5 |
| `application/wasm` | Any shipped WebAssembly is served as the value. | C-TR-18 | Technical requirements para 5 |
| `debug` | The document body never carries a the value class. | C-TR-28 | Technical requirements para 7 |
| `Mathilde` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `1180` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `Yanis` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `1040` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `Capucine` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `990` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `Oscar` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `870` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `Léa` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `760` | Orchard seeds the value the value, the value the value, the value the value, the value `8... | C-DM-18 | Data model seed table rows 1 to 5 |
| `Nour` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `640` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `Hugo` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `Inès` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `410` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `Basile` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `300` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `Zoé` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `180` | Orchard seeds the value the value, the value the value, the value the value, the value the value, the value... | C-DM-19 | Data model seed table rows 6 to 10 |
| `Admin Vireo` | Lighthouse seeds the value the value, the value the value, the value the value. | C-DM-21 | Data model seed table rows 11 to 13 |
| `2080` | Lighthouse seeds the value the value, the value the value, the value the value. | C-DM-21 | Data model seed table rows 11 to 13 |
| `Margaux` | Lighthouse seeds the value the value, the value the value, the value the value. | C-DM-21 | Data model seed table rows 11 to 13 |
| `1640` | Lighthouse seeds the value the value, the value the value, the value the value. | C-DM-21 | Data model seed table rows 11 to 13 |
| `Timothée` | Lighthouse seeds the value the value, the value the value, the value the value. | C-DM-21 | Data model seed table rows 11 to 13 |
| `960` | Lighthouse seeds the value the value, the value the value, the value the value. | C-DM-21 | Data model seed table rows 11 to 13 |
| `Élodie` | Ski seeds the value the value with the value, the value, the value. | C-DM-22 | Data model seed table row 14 |
| `1500` | Ski seeds the value the value with the value, the value, the value. | C-DM-22 | Data model seed table row 14 |
| `portes 20` | Ski seeds the value the value with the value, the value, the value. | C-DM-22 | Data model seed table row 14 |
| `sauts 10` | Ski seeds the value the value with the value, the value, the value. | C-DM-22 | Data model seed table row 14 |
| `drapeaux 3` | Ski seeds the value the value with the value, the value, the value. | C-DM-22 | Data model seed table row 14 |
| `7` | On the orchard board the value ranks the value, the value ranks the value. | C-DM-25 | Data model seed closing paragraph |
| `1` | The lighthouse board serves the value at rank the value as the value. | C-DM-26 | Data model seed closing paragraph |
| `${APP_PUBLIC_PORT}:4173` | The port mapping is the value. | C-DC-02 | Deployment contract bullet 1 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact colour value behind each named family, tone, shade | C-UX-03 | the palette is carried as words by design |
| the exact easing curve behind the eased motion character | C-UX-30 | motion is carried as words by design |
| the handwriting face used in the notebook | C-UX-14 | any open handwriting family is left to the builder |
| the dialogue of the fifteen travellers beyond the four keeper lines | C-CF-171 | the brief names the travellers and leaves their lines to the builder |
| the per-letter delay of the title animation | C-CF-139 | the brief pins the four-second wait, not the stagger |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 4 | 20 |
| User roles | 3 | 24 |
| Core features | 34 | 335 |
| User flow | 10 | 17 |
| UI and UX notes | 4 | 50 |
| Technical requirements | 4 | 28 |
| Data model | 6 | 28 |
| Front-end specification | 4 | 66 |
| Constraints | 2 | 14 |
| Deployment contract | 11 | 26 |
