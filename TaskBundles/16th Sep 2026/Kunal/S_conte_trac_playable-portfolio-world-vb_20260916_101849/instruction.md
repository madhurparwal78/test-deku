# Vireo

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, cross from the loading
screen into a small paper world, finish a timed run in the orchard and put a name on that
minigame's public leaderboard, without hitting an error page.

A run's result must be counted once. Two sends carrying the same run must leave exactly one entry
on the board, and a total the minigame could not have produced must be refused. Every accepted
entry must exist as a real row in PostgreSQL; a board the page keeps to itself does not count,
and neither does a total the browser simply asserts.

## Overview

Vireo is the portfolio of a solo creative developer, built as a game. There is no project index,
no case study template and no about page. There is one page, and behind it a continuous 3D world
made of folded paper and card. The visitor is handed a small character on a hill with a cottage,
and everything the maker wants to show is somewhere in the landscape: an orchard with a clock on
it, a lighthouse, a snowfield with a ski run, a flight through a wind portal. Walking is the menu.
The argument the product makes is the argument about its maker: whether the things this person
builds feel good under the hand can only be judged by moving through one.

Three readers use it. A studio or agency lead gives it thirty seconds and judges the first frame
after loading, which is why the home screen is a lit, live diorama with the title set over it. A
peer developer looks for the seams, tries a controller, resizes the window and reads the markup,
which is why the accessibility layer below is real. A recruiter or client will not play past a
minute and needs to be told what this is, which is why the `Bienvenue` screen exists.

The interface is French. The document title and the metadata are English, because they speak to
search engines and to someone scanning browser tabs. Exactly one action leaves the browser: at the
end of a timed run the visitor may put a name on that minigame's public leaderboard, and the board
updates in front of anyone who has it open. Walking, talking, collecting and exploring all stay in
the visitor's own browser. The only outbound link is `Contact`.

Part of the frame around the world was measured from a real site and is exact: the text, the
buttons, the loading screen, the leaderboard and the way the whole interface scales from one
number. The world inside the frame is described rather than measured, so treat it as something
to art-direct from the descriptions below: where the evidence about the measured world ran out,
its substitution is built entirely from generated geometry and sound. Several things the measured
site got wrong are corrected here rather than copied, and several accessibility behaviours it
lacked are added; every one of them is stated below as a requirement of acceptance.

What it deliberately is not: there are no visitor accounts and no sign-in for visitors, no
comments, likes, chat or messaging, no contact form, no cookie banner, no analytics or tracking of
any kind, no payments, no uploads and no project list. The genuinely hard part is the leaderboard:
a total arrives from somebody else's browser, so it is a number they could have chosen, and the
service must count each run once, refuse what the minigame could not produce, and keep the board
live without letting a bored visitor put something unpleasant at the top of it.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Play the whole world with no account and no sign-in; start a run in any of the four minigames; send one entry per finished run; read any board and follow its live updates; keep progress in their own browser | **Cannot remove or change any name or total**, **cannot list the entries behind a board**, **cannot send a second entry for one run** |
| `owner` | Sign in with the seeded account; list every entry of a game with its stored name; remove the name from an entry while its total and rank stay | **Cannot change a total**, **cannot delete an entry**, **cannot create a second account** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `visitor` session to any `owner`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged. A visitor carries no session at all, so any request to an `owner`-only endpoint
that arrives with no bearer token, or with a token the app did not issue, is denied in the same
way.

Signup is open in the only sense this product has: anyone may play and sign a board with no
invitation, no account and no sign-in. There is no visitor account to create. The one account is
seeded, and there is no signup for a second owner.

Seeded account, using the password `deku-demo-pw-2026`:

| Email | Role | Notes |
|---|---|---|
| `owner@example.com` | `owner` | the maker; removes names from boards through the API |

## Core features

### The leaderboard service

Each of the four minigames has its own board. A visitor's browser keeps an opaque `player_id` of
its own (8 to 64 characters drawn from letters, digits and hyphens) in its own storage, starts a
run when a minigame begins, and sends one entry when the run ends.

1. **One entry per run.** Starting a run returns a `run_token` bound to that run's game. An entry
   sent with that token is accepted once. A second send carrying the same `run_token` is refused
   with a reason and writes nothing; this holds when the two sends arrive at the same moment, so
   two simultaneous sends with one `run_token` leave exactly one entry and the other is refused.
2. **The minigame is named, and must match.** An entry that names no `game`, names an unknown
   game, or names a game other than the one its `run_token` was started for is refused as invalid
   and writes nothing. Starting a run for an unknown or missing game is refused and creates no
   run.
3. **The total must be possible.** An entry carries `counts`, one whole number per item key of
   its game, and a `total`. Each count is a whole number from `0` up to that item's maximum; an
   item key the game does not have, a negative count, a fractional count or a count above its
   maximum is refused. A missing key counts as zero. The `total` must equal the sum of each count
   times that item's worth; any other total is refused, and so is any total above the game's
   maximum. Worked examples for the orchard:

   | `counts` | `total` sent | Outcome |
   |---|---|---|
   | `pommes 12`, `bananes 3`, `bonus 1` | `245` | accepted: 120 + 75 + 50 |
   | `pommes 12`, `bananes 3`, `bonus 1` | `250` | refused: the sum is 245 |
   | `pommes 61` | `610` | refused: `pommes` stops at 60 |
   | `pommes 60`, `bananes 20`, `bonus 5` | `1350` | accepted: the orchard maximum |
   | `cerises 2` | `20` | refused: the orchard has no `cerises` |

4. **A limit on starting runs.** One `player_id` may start at most `3` runs in any `60` seconds; a
   fourth start inside that window is refused with a reason and creates no run. A missing
   `player_id`, or one outside the character rule above, is refused.
5. **Ranking.** A board lists at most `10` rows, highest total first. Equal totals are ordered by
   the earlier entry first, and ranks run `1`, `2`, `3` and on with no gaps and no shared rank. An
   accepted entry's response carries its `rank` on the whole board of its game, which may be
   greater than `10`; an entry outside the top ten is still stored and still ranked.
6. **The board is live.** A viewer holding a board open sees a newly accepted entry take its
   place without reloading and without the page asking again on a timer. The event stream for a
   game opens with the current board and pushes the new board whenever that game's top ten
   changes. An entry that does not reach the top ten, or an entry on another game's board, pushes
   nothing.
7. **Names are filtered twice.** A name is checked before it is stored (see the name rule below)
   and again before it is served. A stored name that fails the reserved-word rule, and any name the
   owner has removed, is served everywhere as `Voyageur anonyme`.
8. **Removing a name keeps the result.** The owner may remove the name from any entry. The entry
   stays on its board with the same total and the same rank, and is served as
   `Voyageur anonyme`. Removing an already removed name succeeds and changes nothing. A visitor
   calling the removal endpoint, with no bearer token or with a token the app did not issue, is
   denied, and the entry's stored name is unchanged.
9. **Only the owner lists entries.** The listing of every entry behind a board, with stored names,
   is denied to anyone without the owner's bearer token.

### Auth

The owner signs in with email and password against the app itself; there is no external identity
provider. A successful sign-in returns a bearer token as `access_token`, which is sent on every
owner request and expires thirty days after it is issued. Passwords are stored hashed. A wrong
password is denied. Visitors never sign in.

### The four minigames and their boards

Every minigame has an id, a French label, the zone it lives in, a keeper who introduces it, and an
item table. The maximum total is the sum of every item's worth times its maximum count.

| `game` | Label | Zone | Keeper | Item key | Item label | Worth | Maximum count |
|---|---|---|---|---|---|---|---|
| `orchard` | `La Cueillette` | `Le Verger` | `La gardienne du verger` | `pommes` | `Pommes` | `10` | `60` |
| `orchard` | | | | `bananes` | `Bananes` | `25` | `20` |
| `orchard` | | | | `bonus` | `Bonus` | `50` | `5` |
| `lighthouse` | `La Veille du Phare` | `Le Phare` | `Le gardien du phare` | `navires` | `Navires guidés` | `40` | `30` |
| `lighthouse` | | | | `tempetes` | `Tempêtes traversées` | `100` | `10` |
| `ski` | `La Descente` | `Les Hautes Neiges` | `La monitrice des cimes` | `portes` | `Portes franchies` | `30` | `40` |
| `ski` | | | | `sauts` | `Sauts réussis` | `60` | `15` |
| `ski` | | | | `drapeaux` | `Drapeaux cueillis` | `100` | `5` |
| `flight` | `Le Vol` | `La Grève` | `Le portail du vent` | `cibles` | `Cibles touchées` | `15` | `100` |
| `flight` | | | | `canons` | `Canons trouvés` | `50` | `6` |
| `flight` | | | | `anneaux` | `Anneaux traversés` | `20` | `50` |

The maximum totals are `1350` for `orchard`, `2200` for `lighthouse`, `2600` for `ski` and `2800`
for `flight`. The games are always listed in that order.

1. **La Cueillette.** Fruit hangs in the orchard trees and falls to the grass. Walking into a piece
   picks it: an apple is a `Pommes`, a banana is a `Bananes`, a golden fruit is a `Bonus`. Touching a
   rotten fruit costs one apple, never taking the tally below zero. The clock starts at `60`
   seconds and the run ends when it reaches zero.
2. **La Veille du Phare.** The visitor turns the lighthouse beam left and right to guide ships
   between the reefs; each ship brought through is a `Navires guidés`, and each storm wave the
   lighthouse rides out with its beam held steady is a `Tempêtes traversées`. The clock starts at
   `90` seconds.
3. **La Descente.** The visitor skis down the high snowfield; each gate passed between its poles
   is a `Portes franchies`, each landed jump a `Sauts réussis`, each flag taken on the way a
   `Drapeaux cueillis`. The run ends at the finish line or after `120` seconds.
4. **Le Vol.** The visitor flies through the wind portal on a set course; each target hit is a
   `Cibles touchées`, each cannon picked up a `Canons trouvés`, each ring flown through an
   `Anneaux traversés`. The craft carries five cells of life; the run ends when the last cell is
   lost or after `120` seconds. Two weapons can be picked up, `Canon` and `Super canon`, each
   announced by a banner.
5. **A run starts at its keeper.** Standing in front of a keeper brings up the prompt `Parler`
   with the key `E`. Acting on it opens the keeper's dialogue with the choices `Commencer` and
   `Plus tard`. `Commencer` starts the run and its display; `Plus tard` closes the dialogue and
   starts nothing. The keepers' opening lines are:

   | Keeper | Line |
   |---|---|
   | `La gardienne du verger` | `Soixante secondes pour remplir le panier. Les fruits pourris vous coûtent une pomme.` |
   | `Le gardien du phare` | `Guidez les navires entre les récifs avant que la tempête ne tombe.` |
   | `La monitrice des cimes` | `Passez les portes, osez les sauts, cueillez les drapeaux jusqu’en bas.` |
   | `Le portail du vent` | `Le vent vous portera tant que votre coque tiendra.` |

6. **A run can be ended early.** While a run is in progress the Menu offers `Terminer la course`,
   which ends the run at once with the tally so far, exactly as if its clock had run out. The run
   clock stops while the Menu is open.
7. **Finishing a run changes the world.** The first time any orchard run ends, a rope bridge
   appears between `Le Promontoire` and `Le Bois Murmurant`, and the notebook's `Journal` page gains
   the entry `J’ai vu un pont apparaître entre le Promontoire et le Bois Murmurant.` The bridge and
   the entry are still there after a reload.

### The name rule

A name is trimmed at both ends and every run of inner spaces is collapsed to one before it is
checked and stored. After that it must be `2` to `16` characters long; may contain only letters
(accented Latin letters included), digits, spaces, hyphens and apostrophes; and must contain at
least one letter. A name containing any of `admin`, `modérateur`, `vireo` or `voyageur anonyme`,
compared without regard to letter case or accents, is refused as reserved. An invalid or reserved
name is refused with a reason and nothing is written.

### The loading screen

The loading screen is the preloader for the whole product.

1. A loading screen appears on arrival and again after the second `Voyager`, because that is when
   the world itself is fetched. It is never blank and never static at any point in either phase.
2. It shows a small paper figure in a wide hat walking on the spot in a pool of warm light, the
   word `LOADING` beneath it, and one piece of advice at the bottom of the screen that changes
   every few seconds. The figure is rendered live by the app, not a downloaded animation.
3. There is no progress bar, no percentage and no count of anything. The word `LOADING` never
   changes.
4. Six tips rotate, crossfading in place with no movement of the layout; exactly one is showing
   at a time. The first two show a drawn keyboard and a drawn controller beside their text; the
   other four are text alone, written as advice from someone who has been there:

   | Tip | Text |
   |---|---|
   | 1 | `Utilisez les flèches directionnelles, ainsi que la souris, pour jouer.` |
   | 2 | `Vous pouvez utiliser une manette de jeu pour jouer.` |
   | 3 | `N’hésitez pas à revenir sur vos pas : certains lieux révèlent de nouveaux chemins quand le monde a changé.` |
   | 4 | `Parlez aux voyageurs que vous croisez : leurs mots sont parfois des portes, et leurs silences des indices.` |
   | 5 | `Le Golem de Vigie peut grandement vous aider dans la quête : écoutez ce que la mer lui apprend.` |
   | 6 | `Certains passages sont bien cachés : n’hésitez pas à fouiller partout, observer les recoins et suivre les détails que le monde laisse derrière lui.` |

5. The document the server sends already carries the loading layer, the word `LOADING` and all six
   tips, so the first paint is never an empty page. Any new tip describes the world, never an
   interface element.

### The home screen

1. After the first load the visitor sees a live diorama: a small wooden cottage on a dark grassy
   hill at dusk, a tree leaning in from the left out of focus, a row of trees along a flat sea
   under a deep blue sky, also out of focus, points of warm light drifting over the grass like
   fireflies, and a tiny figure in front of the porch. Only the cottage and the figure are sharp.
   The scene is running, not a picture, and it is the same world the visitor later walks.
2. The display title `Où sommeillent les Îles` is set large over the scene and the subtitle
   `Un voyage à travers les créations d’un Creative Developer` sits directly under it. Both write
   themselves out one letter at a time; each letter starts slightly to the right and slightly too
   large, then settles, and lines break only between words.
3. Four seconds after the title starts, and not before, the one primary action `Voyager` fades up
   from slightly below and settles. It carries a drawn return-key mark, and the Enter key activates
   it.
4. At the bottom edge sits the link `Contact`, which opens `https://vireo.example/contact` in a new
   window. A visually hidden `(Nouvelle fenêtre)` follows its label so a screen reader announces
   that it opens a new window.
5. None of the text on this screen intercepts the pointer. Pressing and dragging anywhere on the
   composition, straight through the title, swings the camera around the cottage; only `Voyager`
   and `Contact` take the pointer.
6. The middle of the screen, the band between the subtitle and `Voyager`, carries no text and no
   control. The cottage and the figure live there.

### The instruction screen and the second load

1. Pressing `Voyager` does not enter the world. The camera lifts off the hill and climbs into a
   bright sky while the title is replaced by the word `Bienvenue` over three lines:

   | Line | Text |
   |---|---|
   | 1 | `Ce site est une expérience interactive mêlant jeu et portfolio.` |
   | 2 | `À travers un univers jouable et évolutif, j’y explore des idées, des mécaniques et des techniques du web créatif.` |
   | 3 | `Activez vos haut-parleurs ou un casque, utilisez votre souris ou un gamepad, puis explorez à votre rythme.` |

2. Under the three lines, in small italics, the caption `Souris / Clavier · Gamepad · Touch` names
   the four ways to play. The paragraph is held to a comfortable reading measure of about half the
   screen's width.
3. `Voyager` drifts up again two seconds after this screen appears, more slowly than on the home
   screen.
4. Pressing it starts the second load. The first zone begins streaming while the visitor is still
   on the home screen, only the first zone is required before the visitor can move, and the world
   stays rendered behind the second wait rather than being replaced by a blank page.
5. A reload from any state returns to the loading screen and then the home screen, with no error.

### The world

1. The world is nine named zones, and arriving in each one names it: `Le Promontoire` (the opening
   hilltop and the cottage), `La Grève` (the shore below it), `Le Bois Murmurant` (a wood where a
   sword waits), `Le Verger` (the orchard), `La Lande du Golem` (the ground where the Golem de
   Vigie stands), `Le Phare` (the lighthouse), `Les Neiges` (a snowfield entered through a snow
   portal), `Les Hautes Neiges` (the upper snowfield where the ski run begins) and
   `Le Dernier Seuil` (the final encounter, with two boss forms).
2. Fifteen travellers and objects live in the zones: the Golem de Vigie, a magician, a cook and
   the fire the cook asks to have lit, a named traveller, an artefact to find, the orchard tree and
   a small orchard tree, the sword waiting to be taken in the wood, the snow portal, the wind
   portal, a wind that can be shown, a yeti who stands against the visitor in the snow, and the two
   boss forms. Talking to travellers is how the world explains itself.
3. Everything is made of paper and card. The character is folded card in a wide conical hat with
   a satchel at the hip, facets visible. The cottage is paper planks and paper shingles in the warm
   sand colour. Trees have crumpled paper trunks and many separately made leaves. The grass is the
   one thing that is not paper: real blades, thousands of them, bright at the tip, dark at the
   root, all leaning together in a slow wave.
4. The control lessons are not a panel. Two grey rocks lie in the grass at the arrival point on
   `Le Promontoire`, one with a controller drawn on it in chalk and one with arrows and a hand. No
   overlay teaches the controls once the world is showing.
5. The character has weight: it is pushed by the ground and the slopes, never teleported, and the
   areas that decide when the visitor is close enough to talk or to pick something up are part of
   the same physical world as the ground.
6. The camera floats behind and above the character. It never sinks below the height it is
   looking at, so walking downhill never buries it in the hillside. It glides toward where it
   should be rather than snapping, at the same pace however fast the machine is. Pulling it back
   also lifts its gaze a little so more of the landscape shows. Dragging the pointer swings it
   freely while the character stands still, and becomes about a hundred times weaker while the
   character walks. The mouse wheel pulls the camera in and out.
7. Places change. Besides the orchard bridge above, some routes are hidden and reward looking in
   corners; the loading tips hint at both.
8. A browser that cannot draw 3D still gets every interface layer, the Menu and the boards, and
   the notice `Le monde ne peut pas être dessiné sur cet appareil.` where the world would be.

### Interaction, dialogue and arrival

1. Walking near something usable slides one outlined button up from the bottom of the screen,
   naming the action and its key.
2. Acting on it replaces the button with a dialogue: the speaker's name, a line of text beneath it
   and a row of choices over a shadow that fades from almost black at the very bottom of the screen to nothing a little way up,
   so the landscape stays visible above the words.
3. The prompt is light by default. In four bright places it turns dark instead, with its key mark
   darkened at the same moment: at the snow portal, at the lighthouse keeper in `Le Phare`, at the
   yeti and at the ski keeper in `Les Hautes Neiges`.
4. Arriving in a zone puts its name in the middle of the screen in thin letters between two
   hairlines exactly as wide as the name, then lets it go.
5. Picking up a found object stops the world under a soft dark wash; behind the object two copies
   of one star-burst turn slowly in opposite tints, one a second behind the other, and the object
   itself turns in front of the visitor as a rendered model, not an icon. Found objects are
   recorded in the notebook.

### The minigame displays

1. Each minigame has its own display, and no display ever takes the pointer.
2. The orchard display puts the clock at the top centre and the `Pommes` tally at the bottom
   centre, with the clock the larger of the two. The tally swells and settles when fruit is
   picked, shudders and returns to exactly where it was when an apple is lost, and the clock
   pulses gently without stopping once `10` seconds or fewer remain.
3. The lighthouse and ski displays are one row along the top edge: the time left and the run's
   item tallies.
4. The flight display is the odd one out. It uses its own colours, a deep slate, a pale ice blue
   and white, all half see-through, and none of the site's. The tallies sit in the two bottom
   corners, a strip of five cells runs down the right edge showing the life left, the whole
   display is tilted in space rather than flat, and a banner slides across the screen, holds and
   slides off when `Canon` or `Super canon` is picked up.

### The run loop: receipt, board and name form

1. When a run ends the visitor first gets a receipt, the run's breakdown: one row per item of that game showing a black
   silhouette of the item, its label in italics, how many were collected and what they were worth,
   then a `Total` row set well apart and half again as large. The silhouettes are the game's own
   pictures with every colour crushed to black. The button `Continuer` (key Enter) opens the board.
2. The board's title is the game's label. Its assembly is staggered: it deals itself out one row at
   a time, a quarter of a
   second apart, and only after the last row has landed does the name form slide in from the
   opposite side.
3. Each row shows the rank, the name in italics and the total, with the totals lined up on their
   digits down the right edge. The first row is noticeably larger than the rest, and the first
   three each carry a small star mark over the rank: three stars, two stars, one star.
4. The visitor's own entry shows above the board with its rank even when it is outside the top
   ten, and wherever it appears it is tinted and glows gently on and off.
5. The name form is one row: the bold label `Votre nom`, a name field written in italics on a single
   underline, and the button `Envoyer`. While sending, the button is unavailable. After an accepted
   send the form is replaced by the note `Résultat envoyé.` and never offered again for that run.
6. An invalid or reserved name is refused inline: the form stays, keeps what was typed, names the
   `Votre nom` field in its message and writes nothing.
7. A board opened from the Menu is read-only: it shows the same rows, the button `Partir` and the
   button `Fermer`, and no name form. `Partir` places the character at that minigame's keeper and
   names the zone on arrival.
8. A board with no entries shows `Ce classement attend son premier nom.`

### The Menu and its settings

1. The Menu control in the top-left corner is named `Menu`, shows the key `M`, reports whether the
   panel is open, and opens the panel from a click, the `M` key or the controller's start button.
   Escape closes the panel and returns focus to the Menu control.
2. The panel carries `Reprendre`, the `Classements` section listing `La Cueillette`,
   `La Veille du Phare`, `La Descente` and `Le Vol`, and, during a run only,
   `Terminer la course`.
3. The settings are real radio groups with a legend each, reachable and operable by keyboard: the
   group `Qualité` with `Basse`, `Moyenne` and `Haute` (default `Moyenne`); the group
   `Volume de la musique` with `Bas`, `Moyen` and `Fort`; the group `Volume des effets` with `Bas`,
   `Moyen` and `Fort`; the group `Taille du texte` with `Normale` and `Grande`; and the group
   `Animations` with `Complètes` and `Réduites`. Two switches sit beside them: `Couper la musique`
   and `Couper les effets`, each muting its group while keeping its level. One more switch,
   `Inverser l’axe vertical`, inverts the camera's vertical control.
4. The chosen option in a group lifts slightly, grows slightly and turns bold, so the choice reads
   without colour.
5. Every setting takes effect at once, with no reload, and is still chosen after a reload.
6. `Qualité` controls how finely the world is drawn: `Basse` draws it at no more than one device
   pixel per interface pixel and turns off the depth blur and the glow, while `Haute` uses the
   screen's full density up to twice the interface pixel and keeps both. It also sets how far the
   grass is drawn and how sharp the shadows are.
7. `Taille du texte` changes the whole interface at once: `Normale` keeps the root text size at
   `19px` (`12px` on narrow screens) and `Grande` sets it to `23px` (`15px` on narrow screens).
8. `Animations` defaults to `Réduites` when the visitor's system asks to reduce motion, and to
   `Complètes` otherwise.

### The notebook

The notebook is the product's inventory.

1. Everything the visitor collects goes into a ring-binder notebook titled `Carnet de voyage`. The
   control in the bottom-right corner is named `Inventaire`, shows the key `I`, and opens it from a
   click, the `I` key or the controller's north face button. Escape closes it.
2. The notebook rises from the bottom of the screen into the middle as two facing pages with metal
   rings down the spine floating slightly in front of the paper, always landscape, never taller
   than four fifths of the screen or wider than three quarters of it. Everything in it is written in
   the handwriting face, in the first person.
3. It has four pages after the cover: `Récoltes`, listing the tallies `Pommes`, `Bananes` and
   `Bonus` collected across every orchard run; `Trouvailles`, listing found objects; `Journal`,
   listing the changes the visitor has seen in the world; and a closing page. A page with nothing
   on it yet reads `Rien pour l’instant, mais la route est longue.`
4. The corners carry `Page suivante` and `Page précédente`. Anything not yet looked at carries a
   dotted underline until it is opened.
5. Tallies, found objects and journal entries persist in the visitor's own browser across
   reloads and sessions and are never sent to the server. Where the character stands, the current
   zone and any run in progress are not kept.

### Input

1. Mouse, keyboard, controller and touch are peers. Every action can be reached from each of them,
   and the visitor never has to say which one they are using.
2. Keyboard: the arrow keys walk and turn; `A` and `D` also swing the camera left and right; the
   numeric keypad `5` and `2` zoom in and out; holding Shift runs; `E` acts on the prompt; Enter
   commits; Escape closes; `M` opens the Menu; `I` opens the notebook. Every control shows its key
   in a drawn ring beside its label.
3. Controller: the left stick and the directional pad walk, the right stick swings and zooms the
   camera, the south face
   button commits like Enter, the east face button closes like Escape, the west face button acts
   on the prompt, the north face button opens the notebook and the start button opens the Menu. A
   controller whose axes report in another order or direction is read through a per-device mapping
   table.
4. Touch: on a touch screen held sideways a translucent on-screen stick sits at the lower left and
   round buttons named `Interagir` and `Courir` sit at the lower right. Each is at least `44` CSS
   pixels across and does not scale with the interface. The pad lets touches through everywhere
   except on its own controls, so the world can still be dragged beside them, and a touch landing
   on the glyph inside a button still counts for the button.

### Audio

1. Every sound is synthesised in the browser: a quiet music bed, the sea, the wind, one interface
   click and two footsteps, one for grass and earth and one for snow.
2. The footstep is chosen by the ground under the character at that instant, and its pitch varies
   slightly on every step so no two consecutive footsteps sound the same.
3. The sea swells as the character walks toward the shore and the wind rises on high open ground.
4. No sound starts before the visitor's first press; the first `Voyager` is when sound may begin.
   The product still plays in silence.

### Accessibility

1. The animated title and subtitle each keep their whole sentence in a visually hidden element,
   and the per-letter run is hidden from assistive technology, so a screen reader hears one
   sentence rather than single letters.
2. The document carries a visually hidden heading reading `Où sommeillent les Îles` and a visually
   hidden description that includes the sentence `Les flèches directionnelles déplacent le personnage.`
3. The world surface is a focusable application region, so arrow keys reach the character rather
   than the screen reader.
4. A live region outside that region announces, in French: each zone arrival as `Nouveau lieu, `
   followed by the zone name (for example `Nouveau lieu, Le Promontoire`); every dialogue line;
   each found object as `Objet trouvé, ` followed by its name; each tally change during a run as the
   item label followed by a comma and the new count (for example `Pommes, 3`); and each send as
   `Résultat envoyé, rang ` followed by the rank, or `Résultat refusé, ` followed by the reason.
5. Every focusable control shows a visible focus ring at least `2` CSS pixels thick that does not
   rely on colour alone and stays legible over both bright and dark parts of the world. Every
   pointer-hover state has an identical focus state.
6. When motion is reduced, by the visitor's system or by `Animations`, split text appears at once,
   the clock warning and the own-row glow are static, the star-burst stops turning and layers
   cross-fade with no travel. The camera and the character still move, because that is the
   product.
7. The two picture controls are named in French, `Menu` and `Inventaire`, with their keys kept in
   the accessibility tree while hidden from view.

### Language and copy

1. The document declares French. The document title and the description are English and each
   declares English on its own element; the word `LOADING` also declares English.
2. Apostrophes in French copy are the typographic apostrophe (U+2019), never the straight quote.
3. In French copy a no-break space (U+00A0, or the narrow U+202F) precedes every colon, semicolon,
   question mark and exclamation mark; an ordinary space never does.
4. `Creative Developer` stays English inside the French subtitle. `Voyager` is a verb inviting the
   visitor to travel. Keyboard shortcut letters are part of the copy, not fixed in code.
5. Nothing inside the world names the interface: no dialogue says press a button and no zone title
   says level.

### The published surface

1. The page has its own English title, `Where Worlds Take Shape - Interactive WebGL Portfolio`, and
   its own English description,
   `A playable portfolio: walk a paper-craft world, meet its travellers and post your best run to a public leaderboard.`
2. The page declares a social preview title (the same English title), a social preview image at
   `/og-image.png`, the site name `Vireo`, the locale `fr_FR` with the alternate `en_US`, and a large
   summary card. The preview image resolves: it is a `1200` by `630` PNG rendered from the home
   camera when the app is built.
3. An unknown address answers not-found with a small French page titled
   `Page introuvable - Vireo`, described as `Cette adresse ne mène nulle part dans le monde de Vireo.`,
   headed `Page introuvable`, and carrying the link `Retour au voyage` back to `/`. The not-found
   page loads no script at all, so it never starts the application.
4. No path under the app's static files answers with a directory listing.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the whole product: loading, home, instruction, world, Menu, boards, notebook | public |
| any unknown address | the not-found page | public |

The information architecture is one page. The address never changes as the visitor moves
between screens. What a conventional site keeps in
the address is kept as a stack of layers over one running world: which screen is showing, where
the character stands, and what has been collected.

**Entry and redirects.** There is no visitor sign-in and no protected page. A request to an
`owner`-only endpoint without a valid bearer token is denied, and an expired token is denied the
same way while leaving the entry untouched. An unknown address is the not-found page, and
`Retour au voyage` leads back to `/`. A reload from any state returns to the loading screen and
then the home screen. Escape closes whatever layer is open and returns focus to what opened it.

**Journeys.**

1. *A stranger arrives.* Open `/`. The loading screen shows `LOADING` and a tip, then the home
   screen writes out `Où sommeillent les Îles`. After four seconds `Voyager` appears. Press it:
   `Bienvenue` and its three lines appear. Press `Voyager` again: the loading screen returns, then
   the world, with the name `Le Promontoire` in the middle of the screen and the `Menu` and
   `Inventaire` controls in their corners.
2. *A stranger signs the orchard board.* Open the Menu, open `Classements`, choose `La Cueillette`,
   read its ten rows, press `Partir`. The zone name `Le Verger` appears and the prompt `Parler`
   slides up. Act on it, read the keeper's line, choose `Commencer`. The clock shows `60`. Open the
   Menu and choose `Terminer la course`. Read the receipt with its `Pommes`, `Bananes`, `Bonus` and
   `Total` rows, press `Continuer`, watch the board deal itself out, type a name into `Votre nom`,
   press `Envoyer`. The note `Résultat envoyé.` replaces the form and the visitor's own entry shows
   above the board with its rank.
3. *A name is refused.* At the name form, send `A`. The form stays with a message naming
   `Votre nom`, and no entry is written.
4. *An empty board.* Open the Menu, open `Classements`, choose `Le Vol`. The board reads
   `Ce classement attend son premier nom.`
5. *Settings survive a reload.* Press `M`, choose `Grande` under `Taille du texte` and `Réduites`
   under `Animations`; the interface grows at once. Reload, cross to the world, press `M`: both are
   still chosen.
6. *The notebook.* In the world press `I`. `Carnet de voyage` opens; turn with `Page suivante` to
   `Récoltes` and read the `Pommes`, `Bananes` and `Bonus` tallies. Press Escape.
7. *The owner removes a name.* Sign in as `owner@example.com` through the API, remove the name from
   an entry, and read the board: the entry now reads `Voyageur anonyme` with the same total and
   rank.

**States.** Every board has an empty state. Both loading phases show continuous motion and a
rotating tip and never a blank frame. A refused send keeps the form and what was typed, with the
reason beside the name field. A device that cannot draw 3D keeps every interface layer with the
notice `Le monde ne peut pas être dessiné sur cet appareil.` No error crashes the app or leaves a
blank page.

## UI/UX notes

The direction comes from the product itself: the interface is a small, quiet frame around a world
made of paper, and it exists so the world can be seen first. The north star is that within four
seconds of the home screen a visitor understands this is a place to move through, made by someone
whose things feel good under the hand. The register is playful and atmospheric, with the subject
seen first: the interface never competes with the landscape behind it. The stances, each of which
another product could rationally invert: world over interface, words over icons, restraint over
decoration, and one scaling number over many layout rules.

The palette is five colours and one transparency, and nothing else. Almost all interface text is a
near-white neutral set over the rendered world, so the colour a visitor actually experiences is
the render rather than the stylesheet. The document ground before the first frame is a near-black
neutral, so the moment before the world appears is black rather than white; the loading screen's
ground is one step lighter than that near-black neutral, so its arrival reads as a curtain lifting.
Paper is a mid, soft orange, the warm sand of folded card, and it is reserved for paper things:
the loading figure, the cottage, the satchel, the Menu gears and the paper panels of the receipt,
the board and the notebook. Two blues, a mid, vivid blue and a deep, muted blue, complete the
token set. Washes over the world, behind the notebook, the collect ceremony and alerts, are black
at partial opacity. There is no colour scale, no tints and shades, no elevation scale and no grid.
The exact shades are yours, so long as these roles and exclusions hold.

Type is three families with exact jobs and exact sizes. `Playfair Display`, an elegant serif,
carries the two large titles: the home title at `85.5px` and `Bienvenue` at `114px`, each with a
line box tighter than its size. `Lato` carries everything read: body at `19px` and weight `400`,
the home subtitle at `22.8px` and weight `100` (the only place the thinnest weight appears, and
half of the composition), the button label at `20.9px`, and `LOADING` at `19px` bold. One open
handwriting face is used in the notebook and nowhere else. Every letter of the home title and
subtitle carries a soft shadow so white type stays readable over a bright sky, and that shadow is
supplemented wherever it alone would fall short. Totals on a board use equal-width digits so they
align like a table, and a name is always italic, typed or displayed. No other family is loaded.

There is no icon set: the iconography is drawn key rings, two rendered corner controls and chalk
on rocks in the world. Shape carries meaning: every button is a pill, every key mark sits in a true circle drawn by a
thin line, panels are softly rounded, and hairlines stay one line thick at every size because a
hairline that scales stops being one. Density is sparse and comfortable. The layout archetype is
no chrome at all: no menu bar, no header and no footer, just full-screen layers stacked over the
world, at most three live at once, and every panel sits in one of four places, dead centre,
centred on the bottom edge, centred on the top edge, or tucked into a corner. The Menu sits in the
top-left corner and the notebook control in the bottom-right corner. The product commits to one
scheme, white type over a rendered world, and has no light and dark themes.

Components have their states and behave consistently. The pill button rests as an outline, and on
pointer rest or keyboard focus it fills from its bottom edge to its top like rising liquid while
its label flips to the opposite colour, in one quarter-second transition. Every hover state has an
identical focus state. Pressing gives immediate feedback; an unavailable button is dimmed and
ignores the pointer, and unavailable is never signalled by colour alone. Escape closes every
layer. The home screen and every other screen lead with one primary action, visually distinct from
every secondary one: on the home screen `Voyager` is the filled-on-focus pill and `Contact` is a
quiet underlined word.

The motion character is eased, and there are only four speeds in the interface: a quarter of a
second for anything touched, a third of a second for each letter of text appearing, half a second
for a layer changing over, and a slow second and a half for the home `Voyager`, which arrives late
on purpose. There is no custom-shaped motion curve anywhere in the interface; the expressive motion
lives in the world. Every layer's fade and its rise are driven by one number counting from nothing
to everything, so the two cannot fall out of step and an entrance interrupted halfway reverses smoothly, with no
cancel and no jump;
each layer picks its own travel, the board rising a little and the notebook rising a whole page
height. Anything docked on the bottom edge parks twice its own height below the screen and slides
up. Named moments: letters that settle from slightly right and slightly large; the pill that fills
from the bottom; the hairline under `Contact` that grows outward from its middle; the tally that
swells on gain, shudders and returns on loss; the clock that pulses when time runs short; the board
that deals itself out and the form that slides in last from the other side; the own row that glows
on and off; the two star-bursts that turn out of step; the weapon banner that crosses, holds and
leaves. When motion is reduced every decorative animation stops or becomes a plain cross-fade, and
the world keeps moving.

The accessibility floors are contract, not taste. All interface text over the world meets WCAG AA
contrast, at least `4.5:1` against the brightest pixel the world can put behind it, by scrim, by
shadow or by the dark variant of the prompt. Keyboard navigation reaches everything from the first
frame to a moving character, with a visible focus ring that survives both bright and dark
backgrounds. Touch targets are at least `44` CSS pixels. The two picture controls carry French
names, and meaning never rides on colour alone.

The responsive design is one number. The whole interface is sized from a single root text size, so
changing that one value grows or shrinks every gap, padding, button and panel together. There is
one breakpoint, at `64em` wide, and the same rule applies to a window shorter than `40.625em`:
below it the root drops from `19px` to `12px`. Display titles shrink harder than everything else
(the home title becomes `48px` and `Bienvenue` becomes `60px`), dialogue text grows slightly
relative to the root because it is the one thing that must be read, the `Contact` link moves from
the middle of the bottom edge into the lower right corner so it is not under a thumb, and the
lighthouse, ski and flight displays shrink further than the rest because they are glanced at. The design holds at
every width between phone, tablet and desktop, and at a narrow viewport held sideways nothing
overflows sideways and every control stays reachable. A phone held upright is asked to rotate
rather than given a cramped layout, and the ask reads `Veuillez tourner votre appareil`.

What it must not look like: a website pasted over a game, with a navigation bar, cards and a
footer; a frozen photograph where a running scene belongs; an interface loud enough to compete
with the landscape; or a monochrome page dominated by one hue family. The exact values behind
these words are yours, so long as the roles, relationships and exclusions above hold.

## Technical requirements

The rendering model is server-rendered HTML with hydrated islands. The page at `/` is produced on
the server, so the first document the browser receives already carries the loading layer, its six
tips, the visually hidden title and the visually hidden description rather than an empty shell;
the world, the Menu, the boards and the notebook are hydrated in the browser. Build the page with
**SolidStart** in TypeScript, and the HTTP API with **Express**, on the same origin under the `/api`
prefix. Draw the world with WebGL through **three**. Persist to **PostgreSQL**, reached at
`DATABASE_URL`. The app's own address and port come from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`.
Never hardcode a host or a port; read every one of them from the environment. PostgreSQL is
**already running** and reachable at that variable and must not be downloaded, installed, compiled
or started.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing service
available in this environment is PostgreSQL, and reaching for anything else is a contract
violation. The live board is served by the app itself on its own origin.

Authentication is app-implemented email and password for the one owner account, with bearer
tokens that expire after thirty days. Passwords are hashed. `GET /api/health` returns `200` once
the app is ready. Request logs go to standard output, one line per request, carrying the method,
the path and the outcome.

The page carries its own title and description in the document head, as stated above, and a
social preview image with its title. The description and the preview image are part of the
published surface and are served by the app itself.

Delivery is the product's whole performance problem, because the page is almost entirely
download. Every script,
stylesheet and font file carries a content hash in its file name and is served with a
`Cache-Control` header containing `immutable` and a max-age of at least `31536000` seconds. Fonts
are served in WOFF2 only, subset to the Latin and French characters the copy needs, and only the
families named above are served. Any WebAssembly the build ships is served with the content type
`application/wasm`. Nothing the page needs is fetched from another host, and the page sets no
cookie.

No binary asset is downloaded to draw the product: no photograph, no raster sprite, no animated
image, no audio file, no video, no model file and no texture file. Every model, texture, mark,
diagram and sound is generated in the browser from code, the loading figure included. The only
binary files the app serves are its WOFF2 fonts and the social preview image.

The interface follows the world and never drives it: a panel reads the game's state and draws it,
and closing a panel leaves nothing running behind it, so the site does not slow down after a long
session of opening and closing layers. Development tooling, tuning panels and debug markers do not
reach the production build, and the document body never carries a `debug` class.

The world's worst moment is the second wait. The first zone starts streaming while the visitor is
still on the home screen, only the first zone is needed before the visitor can move, and the
rendered scene stays on screen through the wait.

## Data model

Six tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`account`** - `id`, `email` (unique), `password_hash`, `role` (`owner`), `created_at`.

**`session`** - `id`, `account_id`, `token` (unique), `expires_at` (thirty days from issue).

**`game`** - `id` (the game id, one of `orchard`, `lighthouse`, `ski`, `flight`), `label`, `zone`,
`max_total`, `position`.

**`game_item`** - `id`, `game_id`, `key`, `label`, `worth`, `max_count`, `position`. One row per
item in the table under `### The four minigames and their boards`.

**`run`** - `id`, `run_token` (unique, opaque and unguessable, never derived from the
`player_id`), `game_id`, `player_id`, `started_at`, `used_at` (empty until an entry for the run is
accepted).

**`leaderboard_entry`** - `id` (an integer, served as `entry_id`), `game_id`, `run_id` (unique),
`name` (the name as normalised and stored), `name_removed` (true once the owner removes the name),
`total` (an integer), `counts` (a JSON object mapping each item key to its count), `created_at`.

A run carries at most one entry: two simultaneous sends for the same run store exactly one row,
and the other send is refused. An entry's `game_id` always equals its run's `game_id`. An entry's
`total` always equals the sum of its counts times their worths, and never exceeds its game's
`max_total`. Removing a name sets `name_removed` and never deletes the row or changes its `total`.

Derived rather than stored: an entry's rank, the name a board serves, and a board's top ten.

**Seed data.** The owner account `owner@example.com` with role `owner`. The four games and eleven
items exactly as tabled above. Entries, each with its own already used run, created in the order
listed:

| `game` | `name` | `total` | `counts` |
|---|---|---|---|
| `orchard` | `Mathilde` | `1180` | `pommes 58`, `bananes 20`, `bonus 2` |
| `orchard` | `Yanis` | `1040` | `pommes 54`, `bananes 18`, `bonus 1` |
| `orchard` | `Capucine` | `990` | `pommes 49`, `bananes 16`, `bonus 2` |
| `orchard` | `Oscar` | `870` | `pommes 42`, `bananes 14`, `bonus 2` |
| `orchard` | `Léa` | `760` | `pommes 36`, `bananes 12`, `bonus 2` |
| `orchard` | `Nour` | `640` | `pommes 34`, `bananes 10`, `bonus 1` |
| `orchard` | `Hugo` | `640` | `pommes 29`, `bananes 12`, `bonus 1` |
| `orchard` | `Inès` | `410` | `pommes 21`, `bananes 6`, `bonus 1` |
| `orchard` | `Basile` | `300` | `pommes 15`, `bananes 4`, `bonus 1` |
| `orchard` | `Zoé` | `180` | `pommes 8`, `bananes 2`, `bonus 1` |
| `lighthouse` | `Admin Vireo` | `2080` | `navires 27`, `tempetes 10` |
| `lighthouse` | `Margaux` | `1640` | `navires 21`, `tempetes 8` |
| `lighthouse` | `Timothée` | `960` | `navires 14`, `tempetes 4` |
| `ski` | `Élodie` | `1500` | `portes 20`, `sauts 10`, `drapeaux 3` |

The orchard board is therefore full, with `Nour` ranked `6` and `Hugo` ranked `7` on equal totals.
`Admin Vireo` is a legacy row whose stored name now fails the reserved-word rule, so the lighthouse
board serves it at rank `1` as `Voyageur anonyme`. The `flight` board has no entries.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual specification in full. Nothing here overrides a rule stated
above; it makes the look exact.

### The scaling model and the stack of layers

Typography and spacing both come from the root: every size and every gap is a multiple of it.
The root text size is `19px` on wide screens and `12px` at or below `64em` wide (or under
`40.625em` tall), and nothing in the interface is sized apart from it except the one-line
hairlines and the touch pad. Layers are ordered from one list of named places rather than per
component, with gaps between them so a new layer can be slid in later: the world at the bottom,
then the main interface, the interaction prompt, the zone title card, alerts, the notebook, the
notebook control, the Menu control, the cutscene skip control, the collect ceremony and tutorial
layers; above those, the loading screen and the change-over wipe; above the loading screen, the
rotate prompt; and above absolutely everything, the touch pad. A dialogue can never cover the Menu
control, and a loading screen always does. The world layer never fades; everything fades over it.
The change-over wipe that covers the screen while a zone changes is near-black and takes the
pointer while it shows.

### The pill button and the key ring

The pill's label and key ring sit side by side with the ring after the label, and the gap between
them grows slightly with the screen's height. The fill is a hard edge that rises from the bottom
to the top in a quarter of a second while the label turns to the opposite colour; on the paper
panels of the receipt and the board the pill fills dark instead of light and its label turns
light. The key ring is a square box one and a half times the label's size with a thin circle drawn
exactly on its edge, the letter centred inside and always shown as a capital. When a pill fills
light behind it, the ring turns dark so it stays visible. The dialogue's choice buttons drop the
outline and read from their label and ring alone.

### The two corner controls

The Menu control is two interlocking paper gears turning slowly, rendered by the same 3D system as
the world in their own small square surface in the top-left corner, so they are lit by the same
sun and look warmer at dusk than at dawn. The notebook control is a paper satchel with a handle
rendered the same way at twice that size in the bottom-right corner, present only in the world.
Both keep their names and keys in the accessibility tree while showing neither. These interface
surfaces redraw only when something changes and stop entirely while hidden.

### The loading screen

The figure is centred and always three tenths of the screen's height, so the screen reads the same
on a laptop and a phone. `LOADING` sits directly beneath it. The tips sit at the bottom of the
screen, all stacked in one place; the two with a drawing carry it beside the text. Before the
figure can be rendered, a plain ellipse in the paper colour stands where its feet will be, with
`LOADING` beneath it, and the rendered figure fades in over it, so no frame is ever empty.

### The home composition

On a wide screen the title's top edge sits at about a ninth of the height, the subtitle at about a
fifth, `Voyager` in the lower third about a sixth of the height above the bottom, and `Contact` at
the very bottom edge. The band between subtitle and `Voyager`, about three fifths of the height, is
the cottage's. On a narrow screen the title sits a tenth of the way down. The whole title fits on
one line at a tablet width held sideways.

### The instruction panel

`Bienvenue` and its lines sit in a softly rounded panel centred on the screen, about half the
screen's width on wide screens and nine tenths on narrow ones. The caption is italic at three
quarters of the text size, set as a caption under the three lines. Only one line of title ever sits
in this panel, because its line box is tighter than its size.

### Dialogue, prompt, title card and collect ceremony

The prompt sits two root units above the bottom edge and, in the four bright places, turns its
text, its ring and its key mark dark together from a single switch. The dialogue spans the full
width at the bottom with its text held to four fifths of the width; its shadow is a gradient from
almost black at the bottom edge to transparent, with a plain black fallback where the gradient
cannot be drawn, and each line and button carries its own soft drop shadow. The zone title card is
centred, thin (`Lato` at weight `200`), between hairlines above and below, with five times as much
space at its sides as above and below, and never wider than half the screen. The collect ceremony
covers the world with a translucent black wash that takes the pointer; the two star-bursts are one
generated image drawn twice at half strength, the second inverted and a second behind, each turning
once every six seconds; the found object turns in front of them at the size of the screen.

### The minigame displays

The orchard clock is `Lato` bold at three root units and the tally bold at two, the tally's
silhouette above its number. Swelling means scaling up and settling; shuddering means small quick
displacements that end exactly where they started; the warning pulse is smaller and slower than
the swell and repeats until the run ends. The lighthouse and ski rows are spaced in units of their
own size, so on a narrow screen the whole row, margins included, draws in toward the edge. The
flight display declares its own colour block on its own root and changes no site colour: a deep
cool neutral, a near-white muted cyan and a near-white neutral, each at partial opacity, with the
filled and empty life cells swapping those two colours. Its tallies sit two units in from the
bottom corners and its life strip one unit in from the right edge, vertically centred. On narrow
screens the lighthouse, ski and flight displays drop to seven tenths of the root size.

### The receipt and the board

The receipt is a paper panel centred on the screen that scrolls inside itself when it is taller
than nine tenths of the screen; it is the only scrolling region in the product. Each row is the
silhouette, then the italic label over the count, then the worth in bold; the `Total` row sits
three row-gaps below the rest with its number half again as large. The board is a paper panel on a
translucent light ground with its title between two rules that run from the title to the panel's
edges at any title length. Each row is a three-column grid: a narrow rank column, a name column that
shrinks rather than pushing the total off the panel, and a wide total column aligned to the right.
The first row is two fifths larger than the others. The own row is tinted light and glows on a slow
loop. The rows arrive alternately from one side and the form from the other, each fading in over
half a second, with each row invisible until its turn. The form sits on a translucent light pill
with a rule beneath it, and its field is underlined rather than boxed.

### The notebook

The notebook is a landscape spread one and a half times as wide as it is tall, its height the
smaller of four fifths of the screen's height and half its width, so it needs no separate phone
layout. Each page is half the spread, hinged at the spine, and pages turn in three dimensions with a
shallow perspective. The binder rings are a fifth of the spread wide and four fifths tall and float
in front of the pages. The space around the book lets the pointer through; the pages do not. The
cover shows the title; the section pages open with an underlined title. The forward corner control's
label tilts one way and grows while its arrow slides outward; the back control's label tilts the
other way without growing while its arrow slides and grows. Anything that can be opened on a page
swells very slightly and draws a hairline under itself from the middle outward.

### The touch pad and the settings panel

The touch pad's buttons are translucent white circles with a thin white edge, placed by their
centres, with glyphs at half their size; the stick is twice a button's size. The settings panel is a
paper-coloured column of rows: in each group the legend is bold, the radio inputs are visually
hidden but still focusable, and the chosen label lifts, grows and turns bold. Inside this panel an
icon leads its label.

### The generated world

Models are composed from simple shapes with faceted, unsmoothed surfaces in one flat paper
material, which is what makes them read as folded card rather than plastic: the character is a
capsule body with rounded limbs, a cone hat with a flattened brim and a box satchel, and its hat
brim lags a moment behind the head as it moves; the cottage is two boxes, a triangular roof, a
small porch, inset windows and a chimney; the gears are two toothed cylinders; the satchel is a
rounded box with a flap and a handle. The character idles, walks and runs: walking swings the
legs through an arc with the arms counter-swinging at half that amplitude, and running widens the
arc and pitches the torso forward. The sky is a generated
gradient, deep blue above and warm pale at the horizon with a softened sun, and it also lights the
world. The grass is instanced blades, each a tapered strip with a tip, randomly turned and sized,
coloured along a ramp of deep, muted greens from a lit tip to a dark root, with a deep, muted lime
for the darkest foliage, and displaced together by a slow
field so it moves as one. Trees are tapered faceted trunks with many small leaf cards in three
greens. Water is a plane whose surface ripples with two moving noise layers and is coloured between
a deep and a mid blue-green by depth, with a highlight from the sun. The light is a warm key from one
side and a cool fill from the other. The world uses depth of field, a soft glow on bright points and
a colour grade held as data, and the grade can change without rebuilding. Paper panels, the notebook
cover and the rings are generated textures. The keyboard, controller and rotating-phone drawings,
the return-key mark, the star marks, the star-burst and the counter silhouettes are drawn by code;
the silhouettes are the collected models rendered once and crushed to black.

### The generated sound

The music bed is a few slightly detuned tones drifting under a slowly moving filter. The sea is
filtered noise that rises and falls about every twelve seconds. The wind is band-limited noise
whose level follows how exposed the character is. The click is a very short high tone. The grass
footstep is a short, soft burst of noise; the snow footstep is brighter and a little longer. Music
and effects are two groups, each with its own level and mute, and repeated sounds are pooled so a
fast run of footsteps never stalls.

## Constraints

- One page, one maker, one world. There is no multi-tenancy and no visitor account.
- No project index, no case study pages, no about page, no contact form. The contact destination is
  one outbound link.
- No comments, likes, follows, chat or messaging. The leaderboard is the only shared surface.
- No analytics, tracking, fingerprinting, consent banner or cookie. No external network calls at
  run time and no third-party request of any kind.
- No payments, no uploads and no email.
- The build is zero-asset: no binary asset ships except the WOFF2 files of the named open font
  families and the generated social preview image. The build must succeed with an empty asset
  directory. The measured site's own world, its maker's name and its hosts appear nowhere.
- No native application and no offline play. No second language build of the interface.
- The owner removes names through the API; there is no moderation page.
- Several things the measured site does are deliberately not reproduced: it has no reduced-motion
  behaviour, no visible focus ring, no live region, no declared language, a title shadow that fails
  over a bright sky, an English name on a French control, ordinary spaces before French colons, two
  unused font families, uncompressed fonts, a downloaded loading animation, a blank screen during
  the second wait, and development tooling in production. Each is corrected by a requirement above.
- The data volume the app must stay responsive at: tens of thousands of entries per board and a few
  hundred viewers holding boards open at once.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | - | `200` |
| `POST /api/auth/login` | `{ email, password }` | `{ access_token }` |
| `GET /api/games` | - | a top-level JSON array of `{ id, label, zone, max_total, items }`, each item `{ key, label, worth, max }`, in the order `orchard`, `lighthouse`, `ski`, `flight` |
| `POST /api/runs` | `{ game, player_id }` | `{ run_token, game, started_at }` |
| `POST /api/entries` | `{ run_token, game, name, counts, total }` | `{ entry_id, game, name, total, rank }` |
| `GET /api/leaderboards/{game}` | - | a top-level JSON array of at most ten `{ rank, entry_id, name, total }`, best first |
| `GET /api/leaderboards/{game}/events` | - | a `text/event-stream`: an event named `leaderboard` at once, then an event named `leaderboardUpdated` each time the top ten changes, each carrying the board array as JSON data |
| `GET /api/moderation/entries` | `?game=` | a top-level JSON array of `{ entry_id, name, name_removed, total, created_at }`, newest first, `owner` only |
| `DELETE /api/entries/{entry_id}/name` | - | `{ entry_id, name, name_removed, total }`, `owner` only |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns
the named resource or shape; an invalid or unauthorized call is rejected as a client error, never
as a server error and never as a silent success, and a refusal carries a reason. An unknown game in
a path answers not-found. Bearer auth is required on the two `owner` endpoints and on nothing else.

### No mocks

PostgreSQL is the fact. A board held in the page's own memory, entries kept in a module variable, a
live update the page fakes by re-reading on a timer, an event stream that replays a fixed board, a
total the server stores without recomputing it from the counts, or a one-send rule enforced only by
hiding the button: each of these is a contract violation however good the interface looks. **The
named provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.**

## Definition of done

A visitor can cross from the loading screen into the paper world, run the orchard clock down and put
a name on its board, and anyone holding that board open sees the entry arrive. One run is one entry,
even when it is sent twice at once, and a total the minigame could not produce never reaches a
board. The owner can take a name down while its result keeps its place.
