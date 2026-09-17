# Checklist: Sounding

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, deployment
Sections absent: buildplan
Items: 266
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` A signed-in visitor keeps a logbook of saved dive moments. `src: Overview, Overview para 3`
- [ ] `C-OV-02` `data` A saved moment records the scene, the depth the dive had travelled. `src: Overview, Overview para 3`
- [ ] `C-OV-03` `constraint` A draft logbook is readable by the owning diver alone. `src: Overview, Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A `diver` saves a moment to their own logbook. `src: User roles, User roles table row 1`
- [ ] `C-RL-02` `role` A `diver` is denied the dock queue. `src: User roles, User roles table row 1`
- [ ] `C-RL-03` `role` A `diver` is denied annotating an entry belonging to another diver. `src: User roles, User roles table row 1`
- [ ] `C-RL-04` `role` A `diver` is denied deleting an entry belonging to another diver. `src: User roles, User roles table row 1`
- [ ] `C-RL-05` `role` An unauthenticated write to any logbook path is refused. `src: User roles, User roles authorization para`
- [ ] `C-RL-06` `role` A `diver` is denied marking a logbook answered. `src: User roles, User roles table row 1`
- [ ] `C-RL-07` `role` A `host` reads the queue of published logbooks. `src: User roles, User roles table row 2`
- [ ] `C-RL-08` `role` A `host` opens any published logbook from the queue. `src: User roles, User roles table row 2`
- [ ] `C-RL-09` `role` A `host` reads the page view record. `src: User roles, User roles table row 2`
- [ ] `C-RL-10` `role` A `host` is denied every logbook still in `draft`. `src: User roles, User roles table row 2`
- [ ] `C-RL-11` `role` A `host` is denied editing another diver's entry. `src: User roles, User roles table row 2`
- [ ] `C-RL-12` `role` A `host` is denied publishing another diver's logbook. `src: User roles, User roles table row 2`
- [ ] `C-RL-13` `capability` The dive route is served to a visitor holding no session. `src: User roles, User roles visitor para`
- [ ] `C-RL-14` `capability` A visitor with no account reads any published logbook. `src: User roles, User roles visitor para`
- [ ] `C-RL-15` `constraint` No diver-facing path carries a logbook identifier. `src: User roles, User roles session para`
- [ ] `C-RL-16` `role` A `host` asking for a draft logbook is answered as a missing record. `src: User roles, User roles host para`
- [ ] `C-RL-17` `role` A real draft identifier, an invented identifier answer the portfolio owner identically. `src: User roles, User roles host para`
- [ ] `C-RL-18` `role` The dock queue carries no row from a logbook still in draft. `src: User roles, User roles host para`
- [ ] `C-RL-19` `capability` Signup is open, so anyone creates an account from `/sign-in?mode=create`. `src: User roles, User roles signup para`
- [ ] `C-RL-20` `capability` An account created from the sign-in surface is usable at once. `src: User roles, User roles signup para`

## C-CF Core features

- [ ] `C-CF-01` `data` Every account has exactly one logbook, created with the account. `src: Core features, the logbook para 1`
- [ ] `C-CF-02` `literal` A new logbook starts in state `empty` with nothing saved. `src: Core features, the logbook state table row 1`
- [ ] `C-CF-03` `literal` A logbook in `empty` becomes `draft` on the first save. `src: Core features, the logbook state table row 1`
- [ ] `C-CF-04` `literal` A logbook in `published` is readable by anybody holding the address. `src: Core features, the logbook state table row 3`
- [ ] `C-CF-05` `literal` A logbook in `published` appears in the dock queue. `src: Core features, the logbook state table row 3`
- [ ] `C-CF-06` `constraint` A logbook title is between `1`, `80` characters after trimming. `src: Core features, the logbook para 2`
- [ ] `C-CF-07` `constraint` A logbook title is trimmed before the length bounds are applied. `src: Core features, the logbook para 2`
- [ ] `C-CF-08` `constraint` A cleared title is kept on a draft, refused when the logbook is published. `src: Core features, the logbook para 2`
- [ ] `C-CF-09` `constraint` A depth is a number from `0` to `1`. `src: Core features, the logbook para 2`
- [ ] `C-CF-10` `constraint` Twelve entries is the ceiling, so the thirteenth save is refused. `src: Core features, the logbook para 2`
- [ ] `C-CF-11` `constraint` Only a logbook in `draft` accepts a write. `src: Core features, the logbook para 3`
- [ ] `C-CF-12` `contract` A mutating request against a logbook outside `draft` is rejected as a conflict. `src: Core features, the logbook para 3`
- [ ] `C-CF-13` `ui` A surface receiving a conflict reconciles to read-only rather than retrying. `src: Core features, the logbook para 3`
- [ ] `C-CF-14` `capability` Unpublishing removes a logbook from the dock queue. `src: Core features, the logbook para 4`
- [ ] `C-CF-15` `contract` The public address of an unpublished logbook answers not found. `src: Core features, the logbook para 4`
- [ ] `C-CF-16` `constraint` Unpublishing a logbook already in `draft` is refused as a conflict. `src: Core features, the logbook para 4`
- [ ] `C-CF-17` `constraint` Unpublishing an answered logbook does not undo the answer. `src: Core features, the logbook para 4`
- [ ] `C-CF-18` `ui` A save control sits at the bottom left of the dive. `src: Core features, saving a moment para 1`
- [ ] `C-CF-19` `literal` The save control at rest names logging a moment inside square brackets. `src: Core features, saving a moment para 1`
- [ ] `C-CF-20` `data` A save captures the scene index the dive is in. `src: Core features, saving a moment para 1`
- [ ] `C-CF-21` `data` A save captures the instant the moment was logged. `src: Core features, saving a moment para 1`
- [ ] `C-CF-22` `literal` After a successful save the control reads `[Logged]` for two seconds. `src: Core features, saving a moment para 2`
- [ ] `C-CF-23` `data` A newly saved row is appended at the end of the order. `src: Core features, saving a moment para 2`
- [ ] `C-CF-24` `literal` Saving at the ceiling puts `[Logbook full]` in the message strip. `src: Core features, saving a moment para 2`
- [ ] `C-CF-25` `contract` The sign-in opened from the save control carries `next` with the current depth. `src: Core features, saving a moment para 3`
- [ ] `C-CF-26` `capability` The dive resumes at the depth `next` named after signing in. `src: Core features, saving a moment para 3`
- [ ] `C-CF-27` `ui` A row is reorderable by dragging the index cell with a pointer. `src: Core features, ordering entries para 1`
- [ ] `C-CF-28` `ui` A row is reorderable by focusing the index cell, pressing an arrow. `src: Core features, ordering entries para 1`
- [ ] `C-CF-29` `contract` The order write carries one complete ordered list of entry identifiers. `src: Core features, ordering entries para 2`
- [ ] `C-CF-30` `data` The service rewrites each entry position from the ordered list index. `src: Core features, ordering entries para 2`
- [ ] `C-CF-31` `constraint` An order write omitting an entry is refused, leaving the stored order untouched. `src: Core features, ordering entries para 2`
- [ ] `C-CF-32` `data` Two tabs racing an order write resolve as one winner on the whole list. `src: Core features, ordering entries para 2`
- [ ] `C-CF-33` `data` Positions are contiguous, unique within a logbook. `src: Core features, ordering entries para 3`
- [ ] `C-CF-34` `data` Removing an entry closes the gap in the remaining positions. `src: Core features, ordering entries para 3`
- [ ] `C-CF-35` `capability` A note autosaves when the field loses focus. `src: Core features, notes and renaming para 1`
- [ ] `C-CF-36` `data` A written note is returned by the next read of the entry. `src: Core features, notes and renaming para 1`
- [ ] `C-CF-37` `constraint` A note longer than the ceiling is refused, so nothing is written. `src: Core features, notes and renaming para 1`
- [ ] `C-CF-38` `data` A note travels with the row carrying the note through a reorder. `src: Core features, notes and renaming para 1`
- [ ] `C-CF-39` `data` A patch carrying no note leaves the stored note untouched. `src: Core features, notes and renaming para 1`
- [ ] `C-CF-40` `constraint` Publishing runs the validation rules in order, stopping at the first failure. `src: Core features, publishing para 1`
- [ ] `C-CF-41` `data` A failed publish leaves the logbook in `draft` with no public address minted. `src: Core features, publishing para 1`
- [ ] `C-CF-42` `literal` Publishing an empty logbook answers `Log at least one moment`. `src: Core features, publishing rule 1`
- [ ] `C-CF-43` `literal` Publishing without a title answers `Give the logbook a name`. `src: Core features, publishing rule 3`
- [ ] `C-CF-44` `literal` Publishing an entry naming a missing scene answers `One of your moments is no longer in the dive`. `src: Core features, publishing rule 5`
- [ ] `C-CF-45` `literal` Publishing twice answers copy ending `logbook is already published`. `src: Core features, publishing rule 6`
- [ ] `C-CF-46` `data` A passing publish moves the logbook to `published`. `src: Core features, publishing para 2`
- [ ] `C-CF-47` `data` A passing publish writes the publish instant. `src: Core features, publishing para 2`
- [ ] `C-CF-48` `capability` A passing publish mints a public address, shown with a `copy` control. `src: Core features, publishing para 2`
- [ ] `C-CF-49` `constraint` The public identifier carries at least `128` bits of entropy. `src: Core features, publishing para 2`
- [ ] `C-CF-50` `constraint` The public identifier is unrelated to the logbook identifier. `src: Core features, publishing para 2`
- [ ] `C-CF-51` `constraint` The public identifier is unrelated to the diver, to the publish time. `src: Core features, publishing para 2`
- [ ] `C-CF-52` `data` The public identifier is minted once, stable across unpublish, republish. `src: Core features, publishing para 3`
- [ ] `C-CF-53` `ui` A published logbook renders identically for visitor, diver, host. `src: Core features, publishing para 5`
- [ ] `C-CF-54` `ui` A published logbook shows every row, every note, the title, the display name. `src: Core features, publishing para 5`
- [ ] `C-CF-55` `data` The later order write wins because the write is one whole list. `src: Core features, real-time behaviour para 4`
- [ ] `C-CF-56` `contract` A publish against an already published logbook is a conflict. `src: Core features, real-time behaviour para 4`
- [ ] `C-CF-57` `data` The dock queue is ordered by publish time, newest first. `src: Core features, sorting and filtering para 2`
- [ ] `C-CF-58` `capability` The dock filters to one state, never to both at once. `src: Core features, sorting and filtering para 2`
- [ ] `C-CF-59` `capability` Replay places the dive at the entry scene, the entry depth. `src: Core features, replay para 1`
- [ ] `C-CF-60` `constraint` Replay does not animate the journey to the saved depth. `src: Core features, replay para 1`
- [ ] `C-CF-61` `constraint` Replay from a shared logbook skips the introduction. `src: Core features, replay para 2`
- [ ] `C-CF-62` `capability` The portfolio owner reads a queue of published logbooks at `/dock`. `src: Core features, the dock para 1`
- [ ] `C-CF-63` `ui` The dock shows the queue beside the logbook currently open. `src: Core features, the dock para 1`
- [ ] `C-CF-64` `contract` The dock queue filters to `published` or to `answered`. `src: Core features, the dock para 1`
- [ ] `C-CF-65` `contract` The dock queue pages by cursor rather than by offset. `src: Core features, the dock para 1`
- [ ] `C-CF-66` `data` Marking answered sets the state to `answered`, writes the instant. `src: Core features, the dock para 2`
- [ ] `C-CF-67` `literal` An answered logbook shows a persistent `[Received]` notice above the entries. `src: Core features, the dock para 2`
- [ ] `C-CF-68` `capability` An account is created with an email address, a display name, a password. `src: Core features, identity para 1`
- [ ] `C-CF-69` `constraint` Switching sign-in mode rewrites the query without navigating. `src: Core features, identity para 1`
- [ ] `C-CF-70` `capability` A reset request always shows the same success surface. `src: Core features, identity para 2`
- [ ] `C-CF-71` `constraint` A reset message goes out only for a registered address. `src: Core features, identity para 2`
- [ ] `C-CF-72` `constraint` An unregistered address receives no reset message at all. `src: Core features, identity para 2`
- [ ] `C-CF-73` `constraint` A reset link is single use. `src: Core features, identity para 2`
- [ ] `C-CF-74` `literal` Creating an account sends the new diver a message subject `Sounding: your logbook`. `src: Core features, messages table row 1`
- [ ] `C-CF-75` `literal` The welcome message subject line is exactly `Sounding: your logbook`. `src: Core features, messages table row 1`
- [ ] `C-CF-76` `literal` A reset request for a registered address sends subject `Sounding: reset your password`. `src: Core features, messages table row 2`
- [ ] `C-CF-77` `literal` Publishing sends the diver a message subject `Sounding: your logbook is live`. `src: Core features, messages table row 3`
- [ ] `C-CF-78` `literal` Publishing sends `host@example.com` a subject beginning `New logbook from `. `src: Core features, messages table row 4`
- [ ] `C-CF-79` `contract` The waiting message subject ends with the publishing diver display name. `src: Core features, messages table row 4`
- [ ] `C-CF-80` `constraint` Marking answered sends no message. `src: Core features, messages para 2`
- [ ] `C-CF-81` `constraint` No message ever carries the text of a note. `src: Core features, messages para 2`
- [ ] `C-CF-82` `constraint` Gesturing up at the surface leaves the dive at the surface. `src: Core features, the dive para 4`
- [ ] `C-CF-83` `constraint` Gesturing down at the last scene leaves the dive at the last scene. `src: Core features, the dive para 4`
- [ ] `C-CF-84` `capability` The three header words jump the dive to works, message, contact depths. `src: Core features, the dive para 5`
- [ ] `C-CF-85` `contract` A parameter named `at` places the dive at a depth on first paint. `src: Core features, the dive para 5`
- [ ] `C-CF-86` `contract` The dive route accepts a depth parameter from `0` to `1`. `src: Core features, the dive para 5`
- [ ] `C-CF-87` `constraint` An out of range `at` value is clamped rather than refused. `src: Core features, the dive para 5`
- [ ] `C-CF-88` `constraint` The depth reaches the address only on a save or a replay. `src: Core features, the dive para 6`
- [ ] `C-CF-89` `literal` The gate offers a control reading `Dive into the experience`. `src: Core features, the entry gate para`
- [ ] `C-CF-90` `literal` The gate offers a control reading `Enter without audio`. `src: Core features, the entry gate para`
- [ ] `C-CF-91` `constraint` Both gate controls enter the dive. `src: Core features, the entry gate para`
- [ ] `C-CF-92` `data` Four projects live in the works scene. `src: Core features, works para 1`
- [ ] `C-CF-93` `data` A project carries a title, a description, a skills line, an outbound link. `src: Core features, works para 1`
- [ ] `C-CF-94` `constraint` The gesture steps rather than glides with the works layer open. `src: Core features, works para 1`
- [ ] `C-CF-95` `constraint` One ordinary gesture moves exactly one project. `src: Core features, works para 1`
- [ ] `C-CF-96` `contract` `/works` enters the dive at the works depth with the works layer open. `src: Core features, works para 3`
- [ ] `C-CF-97` `contract` An unknown address answers as not found. `src: Core features, errors para 1`
- [ ] `C-CF-98` `constraint` The consent question does not return once the answer has been recorded. `src: Core features, errors para 2`
- [ ] `C-CF-99` `constraint` Refusing consent leaves the dive, the logbook, the dock working identically. `src: Core features, errors para 2`
- [ ] `C-CF-100` `ui` The consent question is asked in the message strip rather than in a dialog. `src: Core features, errors para 2`
- [ ] `C-CF-101` `data` Every page view is recorded with the route, the instant served. `src: Core features, the page view record para`
- [ ] `C-CF-102` `constraint` The page view record is readable by the host alone. `src: Core features, the page view record para`
- [ ] `C-CF-103` `constraint` The page view record is never keyed to a person. `src: Core features, the page view record para`
- [ ] `C-CF-104` `constraint` A public logbook address never appears in the page view record. `src: Core features, the page view record para`
- [ ] `C-CF-105` `ui` One strip along the bottom edge carries every transient message. `src: Core features, the message strip para`
- [ ] `C-CF-106` `constraint` The strip shows one message at a time for five seconds. `src: Core features, the message strip para`
- [ ] `C-CF-107` `constraint` A second strip message replaces the first rather than stacking. `src: Core features, the message strip para`
- [ ] `C-CF-108` `literal` The strip message `[Offline]` persists rather than dwelling. `src: Core features, the message strip para`

## C-UF User flow

- [ ] `C-UF-01` `contract` The route `/works` serves the dive at the works depth. `src: User flow, Routes table row 2`
- [ ] `C-UF-02` `contract` The route `/logbook` serves the signed-in diver's own logbook. `src: User flow, Routes table row 4`
- [ ] `C-UF-03` `contract` The route `/dock` serves the host queue beside the open logbook. `src: User flow, Routes table row 6`
- [ ] `C-UF-04` `literal` The parameter `next` takes a path beginning with a single slash. `src: User flow, Parameters table row 2`
- [ ] `C-UF-05` `literal` The parameter `token` carries a single-use reset token. `src: User flow, Parameters table row 3`
- [ ] `C-UF-06` `ui` The three header words are the only navigation the dive has. `src: User flow, Routes para`
- [ ] `C-UF-07` `ui` A signed-in diver reaching `/sign-in` is redirected to `/logbook`. `src: User flow, Entry table row 2`
- [ ] `C-UF-08` `ui` A signed-in host reaching `/sign-in` is redirected to `/dock`. `src: User flow, Entry table row 2`
- [ ] `C-UF-09` `contract` A visitor holding no session asking for a draft address is sent to sign in. `src: User flow, Entry table row 5`
- [ ] `C-UF-10` `constraint` A forbidden route renders with the address unchanged. `src: User flow, Entry para 1`
- [ ] `C-UF-11` `constraint` A `next` value beginning with two slashes becomes `/`. `src: User flow, Entry para 2`
- [ ] `C-UF-12` `constraint` A `next` value pointing at another origin falls back to the dive. `src: User flow, Entry para 2`
- [ ] `C-UF-13` `ui` The gate offers two ways in after the loader fills. `src: User flow, Journeys para 1`
- [ ] `C-UF-14` `ui` The surface scene carries the name across the top. `src: User flow, Journeys para 1`
- [ ] `C-UF-15` `ui` Three saved moments appear as three rows in save order. `src: User flow, Journeys para 3`
- [ ] `C-UF-16` `capability` Pressing the up arrow twice moves the third row to the top. `src: User flow, Journeys para 3`
- [ ] `C-UF-17` `data` A reload returns the order the diver left. `src: User flow, Journeys para 3`
- [ ] `C-UF-18` `ui` A passing publish shows a public address with a `copy` control. `src: User flow, Journeys para 3`
- [ ] `C-UF-19` `ui` A stranger with no cookies reads the title, the display name, every row. `src: User flow, Journeys para 4`
- [ ] `C-UF-20` `literal` Unpublishing puts `[Unpublished. The link is dead]` in the strip. `src: User flow, Journeys para 5`
- [ ] `C-UF-21` `literal` A refused diver reads copy ending `logbook belongs to someone else`. `src: User flow, Journeys para 6`
- [ ] `C-UF-22` `literal` An empty logbook shows `[Empty log]`, `Nothing logged yet`, `back to the dive`. `src: User flow, States table row 2`
- [ ] `C-UF-23` `literal` A signed-out logbook shows `[No log]`, `Sign in to keep a logbook`, `sign in`. `src: User flow, States table row 3`
- [ ] `C-UF-24` `constraint` A surface never shows two states at once. `src: User flow, States para 1`
- [ ] `C-UF-25` `ui` A machine with no usable graphics gets a still frame, the whole text. `src: User flow, States para 2`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The signal is a mid, vivid orange spent exactly once on the whole site. `src: UI/UX notes, palette para 1`
- [ ] `C-UX-02` `ui` The water's own hue is a deep, soft teal. `src: UI/UX notes, scene palette para`
- [ ] `C-UX-03` `ui` The distortion surges hardest halfway through a transition. `src: UI/UX notes, motion para`
- [ ] `C-UX-04` `constraint` Reduced motion removes the drawn pointer, restores the system pointer. `src: UI/UX notes, reduced motion para`
- [ ] `C-UX-05` `ui` The drawn pointer shows two states, over water, over something activatable. `src: UI/UX notes, pointer para`
- [ ] `C-UX-06` `literal` The ink against the ground is about `18:1`. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-07` `ui` A disabled control keeps the mark colour for the label text. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-08` `ui` A disabled control signals state by the spinner replacing the label. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-09` `constraint` Body text meets the WCAG AA contrast bar on every surface. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-10` `ui` Every focusable element has a visible focus treatment. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-11` `constraint` A focus treatment is distinguishable from the hover treatment. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-12` `capability` Page down, down arrow descend one scene per press. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-13` `capability` Escape closes an open panel. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-14` `constraint` Every scene's own text is present in the document for assistive technology. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-15` `constraint` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes, responsive para`
- [ ] `C-UX-16` `ui` Two arrow controls become permanently visible below the breakpoint. `src: UI/UX notes, responsive para`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The chrome fades in once the introduction completes. `src: Front-end specification, global chrome para`
- [ ] `C-FE-02` `literal` The three header words are `Works`, `Message`, `Contact`. `src: Front-end specification, chrome table row 2`
- [ ] `C-FE-03` `ui` The three audio bars are driven from the sound itself. `src: Front-end specification, chrome table row 3`
- [ ] `C-FE-04` `ui` The save control sits bottom left in the header control treatment. `src: Front-end specification, chrome table row 4`
- [ ] `C-FE-05` `ui` The depth mark travels the right edge as the dive moves. `src: Front-end specification, chrome table row 5`
- [ ] `C-FE-06` `ui` The depth mark fades when the dive stops. `src: Front-end specification, chrome table row 5`
- [ ] `C-FE-07` `literal` The loader carries a status label reading `[Please wait]`. `src: Front-end specification, loader para 1`
- [ ] `C-FE-08` `literal` The loader carries a status line reading `Loading 3D experience`. `src: Front-end specification, loader para 1`
- [ ] `C-FE-09` `ui` The loader meter is two runs of slash characters. `src: Front-end specification, loader para 2`
- [ ] `C-FE-10` `ui` The loader dissolves rather than cutting when loading finishes. `src: Front-end specification, loader para 3`
- [ ] `C-FE-11` `literal` The gate salutation reads `[Welcome aboard]`. `src: Front-end specification, gate para`
- [ ] `C-FE-12` `ui` The gate secondary control is pinned to the bottom of the screen. `src: Front-end specification, gate para 2`
- [ ] `C-FE-13` `literal` The surface scene carries the name `Ines Marlow` across the top. `src: Front-end specification, surface para`
- [ ] `C-FE-14` `literal` The introduction sentence reads `Ines Marlow is a Software Engineer`. `src: Front-end specification, introduction para`
- [ ] `C-FE-15` `ui` The introduction sentence is drawn in a difference blend. `src: Front-end specification, introduction para`
- [ ] `C-FE-16` `literal` The about location line reads `based in Portugal`. `src: Front-end specification, about table row 2`
- [ ] `C-FE-17` `literal` The about affiliation reads `/// Creative Developer at [Kelp Studio]`. `src: Front-end specification, about table row 3`
- [ ] `C-FE-18` `literal` The works close control reads `Close`. `src: Front-end specification, works para`
- [ ] `C-FE-19` `ui` The works close control sits near the middle of the top edge. `src: Front-end specification, works para`
- [ ] `C-FE-20` `ui` The works title is given exactly one line, clipped rather than wrapped. `src: Front-end specification, works para`
- [ ] `C-FE-21` `literal` The works link reads `Visit Project`. `src: Front-end specification, works para`
- [ ] `C-FE-22` `constraint` Eight contact destinations are listed as words, never as icons. `src: Front-end specification, contact para`
- [ ] `C-FE-23` `literal` The footer sign-off reads `Thanks for visiting`. `src: Front-end specification, footer para`
- [ ] `C-FE-24` `ui` The rights block grows on a small screen rather than shrinking. `src: Front-end specification, footer para`
- [ ] `C-FE-25` `ui` The project detail panel is a full surface over the dive. `src: Front-end specification, detail panel para`
- [ ] `C-FE-26` `constraint` The project detail panel is the only scrolling region in the product. `src: Front-end specification, detail panel para`
- [ ] `C-FE-27` `capability` Escape closes the detail panel, returning focus to the opening control. `src: Front-end specification, detail panel para 3`
- [ ] `C-FE-28` `literal` The not-found surface shows `[No such depth]`, `That address does not exist`. `src: Front-end specification, refusal table row 1`
- [ ] `C-FE-29` `constraint` The password field holds `8` to `200` characters. `src: Front-end specification, forms table row 2`
- [ ] `C-FE-30` `constraint` A submit control is disabled only during a request in flight. `src: Front-end specification, forms rule 1`
- [ ] `C-FE-31` `constraint` An empty required field produces a message on submit, never a dead control. `src: Front-end specification, forms rule 1`
- [ ] `C-FE-32` `ui` The error slot is reserved under every form whether or not a message shows. `src: Front-end specification, forms rule 2`
- [ ] `C-FE-33` `literal` The sign-in primary controls read `Sign in`, `Start a logbook`. `src: Front-end specification, forms controls para`
- [ ] `C-FE-34` `literal` The sign-in secondary controls read `Forgot password`, `Show`, `Sign out`. `src: Front-end specification, forms controls para`
- [ ] `C-FE-35` `literal` A wrong password answers copy ending `password do not match`. `src: Front-end specification, forms message table row 1`
- [ ] `C-FE-36` `literal` A taken address answers `That email is already registered`. `src: Front-end specification, forms message table row 2`
- [ ] `C-FE-37` `ui` An entry row carries the scene name, the depth as a percentage with no decimal. `src: Front-end specification, logbook surfaces para`
- [ ] `C-FE-38` `ui` The title field sits above the rows. `src: Front-end specification, logbook surfaces para 3`
- [ ] `C-FE-39` `ui` A published logbook shows the public address with a `copy` control. `src: Front-end specification, logbook surfaces para 3`
- [ ] `C-FE-40` `literal` Copying the public address puts `[Link copied]` in the strip. `src: Front-end specification, logbook surfaces para 3`
- [ ] `C-FE-41` `ui` A published logbook at the public address shows only the replay control per row. `src: Front-end specification, logbook surfaces para 4`
- [ ] `C-FE-42` `ui` The water is a shader over geometry needing no texture. `src: Front-end specification, zero-asset water para`
- [ ] `C-FE-43` `constraint` The same moment always generates the same thumbnail. `src: Front-end specification, thumbnail para 2`
- [ ] `C-FE-44` `constraint` Audio never starts without a gesture. `src: Front-end specification, audio para`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` Every route is served as its own document. `src: Technical requirements, stack para 1`
- [ ] `C-TR-02` `constraint` The browser receives finished HTML on first paint for every route. `src: Technical requirements, stack para 3`
- [ ] `C-TR-03` `constraint` The session cookie is HTTP-only, secure, same-site-strict. `src: Technical requirements, identity para`
- [ ] `C-TR-04` `contract` The public logbook route declares a no-referrer policy on its own responses. `src: Technical requirements, secret para`
- [ ] `C-TR-05` `contract` Every response carries a strict transport policy of one year with subdomains. `src: Technical requirements, headers para`
- [ ] `C-TR-06` `contract` Every response carries a nosniff content-type policy. `src: Technical requirements, headers para`
- [ ] `C-TR-07` `constraint` A note renders as a text node, never as markup. `src: Technical requirements, input para`
- [ ] `C-TR-08` `constraint` A hostile note returns the literal characters, running nothing. `src: Technical requirements, input para`
- [ ] `C-TR-09` `constraint` A hostile note is never silently stripped or rewritten. `src: Technical requirements, input para`
- [ ] `C-TR-10` `constraint` A hostile note is returned unchanged by the read of the logbook. `src: Technical requirements, input para`
- [ ] `C-TR-11` `constraint` A scene index is range-checked against the six scenes. `src: Technical requirements, input para`
- [ ] `C-TR-12` `literal` The dive title is `Ines Marlow // Creative Software Engineer & UI/UX Designer`. `src: Technical requirements, titles para`
- [ ] `C-TR-13` `literal` An unknown address carries the title `Not found - Ines Marlow`. `src: Technical requirements, titles para`
- [ ] `C-TR-14` `constraint` Every public route carries its own title, its own description. `src: Technical requirements, titles para`
- [ ] `C-TR-15` `constraint` No two routes share a title or a description. `src: Technical requirements, titles para`
- [ ] `C-TR-16` `capability` The site serves a favicon at its own address. `src: Technical requirements, titles para`
- [ ] `C-TR-17` `contract` Every document head declares the favicon. `src: Technical requirements, titles para`
- [ ] `C-TR-18` `constraint` The health route answers once six scenes, four projects are loaded. `src: Technical requirements, health para`
- [ ] `C-TR-19` `data` A page view row names the route served, the instant of service. `src: Technical requirements, health para`

## C-DM Data model

- [ ] `C-DM-01` `data` A scene carries an index, a slug, a name, a field of view, a layer identifier. `src: Data model, built in para`
- [ ] `C-DM-02` `data` A project carries an id, a slug, a title, a description, a skills list. `src: Data model, built in para`
- [ ] `C-DM-03` `literal` Four projects exist, every one at scene `3`. `src: Data model, built in para`
- [ ] `C-DM-04` `data` A diver carries an id, an email, a display name, a password hash, a role. `src: Data model, account state para`
- [ ] `C-DM-05` `data` An entry carries an id, a logbook id, a scene index, a progress, a position. `src: Data model, account state para`
- [ ] `C-DM-06` `data` A page view carries an id, a route, the instant served. `src: Data model, account state para`
- [ ] `C-DM-07` `constraint` A display name holds `1` to `60` characters after trimming. `src: Data model, field rules table row 4`
- [ ] `C-DM-08` `constraint` A progress value is a number from `0` to `1` inclusive. `src: Data model, field rules table row 7`
- [ ] `C-DM-09` `data` A saved progress value round trips through the store without losing precision. `src: Data model, field rules table row 7`
- [ ] `C-DM-10` `data` A diver owns exactly one logbook created with the account in state `empty`. `src: Data model, relationships para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Only `/`, `/works` load the three-dimensional layer. `src: Constraints, constraints bullet 3`
- [ ] `C-CN-02` `constraint` A logbook follows a diver to another machine. `src: Constraints, constraints bullet 5`
- [ ] `C-CN-03` `constraint` A moment cannot be saved without an account. `src: Constraints, constraints bullet 5`
- [ ] `C-CN-04` `constraint` Nothing a diver typed is discarded by a failure. `src: Constraints, constraints bullet 7`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` `GET /api/scenes` returns the six scenes in index order. `src: Deployment contract, API table row 2`
- [ ] `C-DC-02` `contract` `GET /api/projects` returns the four projects in position order. `src: Deployment contract, API table row 3`
- [ ] `C-DC-03` `contract` `POST /api/auth/sign-out` revokes every session for the account. `src: Deployment contract, API table row 6`
- [ ] `C-DC-04` `contract` `PUT /api/logbook/order` takes `order`, the complete array of entry identifiers. `src: Deployment contract, API table row 15`
- [ ] `C-DC-05` `contract` `POST /api/logbook/unpublish` returns the logbook with `publicId` unchanged. `src: Deployment contract, API table row 17`
- [ ] `C-DC-06` `contract` `GET /api/logbook/public/<publicId>` returns the diver `displayName` alone. `src: Deployment contract, API table row 18`
- [ ] `C-DC-07` `contract` `GET /api/dock/<logbookId>` returns the logbook, entries, diver. `src: Deployment contract, API table row 20`
- [ ] `C-DC-08` `contract` `POST /api/dock/<logbookId>/answer` returns the logbook in `answered`. `src: Deployment contract, API table row 21`
- [ ] `C-DC-09` `constraint` Field names are exact across every response. `src: Deployment contract, API para`
- [ ] `C-DC-10` `literal` The code `unauthenticated` answers `401`. `src: Deployment contract, error code table row 1`
- [ ] `C-DC-11` `literal` The code `forbidden` answers `403`. `src: Deployment contract, error code table row 2`
- [ ] `C-DC-12` `literal` The code `not_found` answers `404`. `src: Deployment contract, error code table row 3`
- [ ] `C-DC-13` `literal` The code `already_published` answers `409`. `src: Deployment contract, error code table row 5`
- [ ] `C-DC-14` `literal` The code `scene_missing` answers `422`. `src: Deployment contract, error code table row 7`
- [ ] `C-DC-15` `literal` The code `invalid` answers `422` with `field` naming the field. `src: Deployment contract, error code table row 8`
- [ ] `C-DC-16` `ui` The `error` field renders straight into the form error slot. `src: Deployment contract, error table`
- [ ] `C-DC-17` `contract` The public logbook read, sign-up, sign-in, reset need no session. `src: Deployment contract, auth para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `empty` | pinned value | C-CF-02 | Core features, the logbook state table row 1 |
| `draft` | pinned value | C-CF-03 | Core features, the logbook state table row 1 |
| `published` | pinned value | C-CF-04 | Core features, the logbook state table row 3 |
| `[Logged]` | bracketed status copy | C-CF-22 | Core features, saving a moment para 2 |
| `[Logbook full]` | bracketed status copy | C-CF-24 | Core features, saving a moment para 2 |
| `Log at least one moment` | pinned value | C-CF-42 | Core features, publishing rule 1 |
| `Give the logbook a name` | pinned value | C-CF-43 | Core features, publishing rule 3 |
| `One of your moments is no longer in the dive` | pinned value | C-CF-44 | Core features, publishing rule 5 |
| `logbook is already published` | pinned value | C-CF-45 | Core features, publishing rule 6 |
| `[Received]` | bracketed status copy | C-CF-67 | Core features, the dock para 2 |
| `Sounding: your logbook` | pinned value | C-CF-74 | Core features, messages table row 1 |
| `Sounding: reset your password` | pinned value | C-CF-76 | Core features, messages table row 2 |
| `Sounding: your logbook is live` | pinned value | C-CF-77 | Core features, messages table row 3 |
| `host@example.com` | seeded account email | C-CF-78 | Core features, messages table row 4 |
| `New logbook from ` | pinned value | C-CF-78 | Core features, messages table row 4 |
| `Dive into the experience` | pinned value | C-CF-89 | Core features, the entry gate para |
| `Enter without audio` | pinned value | C-CF-90 | Core features, the entry gate para |
| `[Offline]` | bracketed status copy | C-CF-108 | Core features, the message strip para |
| `next` | pinned value | C-UF-04 | User flow, Parameters table row 2 |
| `token` | pinned value | C-UF-05 | User flow, Parameters table row 3 |
| `[Unpublished. The link is dead]` | bracketed status copy | C-UF-20 | User flow, Journeys para 5 |
| `logbook belongs to someone else` | pinned value | C-UF-21 | User flow, Journeys para 6 |
| `[Empty log]` | bracketed status copy | C-UF-22 | User flow, States table row 2 |
| `Nothing logged yet` | pinned value | C-UF-22 | User flow, States table row 2 |
| `back to the dive` | pinned value | C-UF-22 | User flow, States table row 2 |
| `[No log]` | bracketed status copy | C-UF-23 | User flow, States table row 3 |
| `Sign in to keep a logbook` | pinned value | C-UF-23 | User flow, States table row 3 |
| `sign in` | pinned value | C-UF-23 | User flow, States table row 3 |
| `18:1` | pinned measure | C-UX-06 | UI/UX notes, accessibility para 1 |
| `Works` | pinned value | C-FE-02 | Front-end specification, chrome table row 2 |
| `Message` | pinned value | C-FE-02 | Front-end specification, chrome table row 2 |
| `Contact` | pinned value | C-FE-02 | Front-end specification, chrome table row 2 |
| `[Please wait]` | bracketed status copy | C-FE-07 | Front-end specification, loader para 1 |
| `Loading 3D experience` | pinned value | C-FE-08 | Front-end specification, loader para 1 |
| `[Welcome aboard]` | bracketed status copy | C-FE-11 | Front-end specification, gate para |
| `Ines Marlow` | pinned value | C-FE-13 | Front-end specification, surface para |
| `Ines Marlow is a Software Engineer` | pinned value | C-FE-14 | Front-end specification, introduction para |
| `based in Portugal` | pinned value | C-FE-16 | Front-end specification, about table row 2 |
| `/// Creative Developer at [Kelp Studio]` | route | C-FE-17 | Front-end specification, about table row 3 |
| `Close` | pinned value | C-FE-18 | Front-end specification, works para |
| `Visit Project` | pinned value | C-FE-21 | Front-end specification, works para |
| `Thanks for visiting` | pinned value | C-FE-23 | Front-end specification, footer para |
| `[No such depth]` | bracketed status copy | C-FE-28 | Front-end specification, refusal table row 1 |
| `That address does not exist` | pinned value | C-FE-28 | Front-end specification, refusal table row 1 |
| `Sign in` | pinned value | C-FE-33 | Front-end specification, forms controls para |
| `Start a logbook` | pinned value | C-FE-33 | Front-end specification, forms controls para |
| `Forgot password` | pinned value | C-FE-34 | Front-end specification, forms controls para |
| `Show` | pinned value | C-FE-34 | Front-end specification, forms controls para |
| `Sign out` | pinned value | C-FE-34 | Front-end specification, forms controls para |
| `password do not match` | pinned value | C-FE-35 | Front-end specification, forms message table row 1 |
| `That email is already registered` | pinned value | C-FE-36 | Front-end specification, forms message table row 2 |
| `[Link copied]` | bracketed status copy | C-FE-40 | Front-end specification, logbook surfaces para 3 |
| `Ines Marlow // Creative Software Engineer & UI/UX Designer` | pinned value | C-TR-12 | Technical requirements, titles para |
| `Not found - Ines Marlow` | pinned value | C-TR-13 | Technical requirements, titles para |
| `3` | pinned measure | C-DM-03 | Data model, built in para |
| `unauthenticated` | pinned value | C-DC-10 | Deployment contract, error code table row 1 |
| `401` | pinned measure | C-DC-10 | Deployment contract, error code table row 1 |
| `forbidden` | pinned value | C-DC-11 | Deployment contract, error code table row 2 |
| `403` | pinned measure | C-DC-11 | Deployment contract, error code table row 2 |
| `not_found` | pinned value | C-DC-12 | Deployment contract, error code table row 3 |
| `404` | pinned measure | C-DC-12 | Deployment contract, error code table row 3 |
| `already_published` | pinned value | C-DC-13 | Deployment contract, error code table row 5 |
| `409` | pinned measure | C-DC-13 | Deployment contract, error code table row 5 |
| `scene_missing` | pinned value | C-DC-14 | Deployment contract, error code table row 7 |
| `422` | pinned measure | C-DC-14 | Deployment contract, error code table row 7 |
| `invalid` | pinned value | C-DC-15 | Deployment contract, error code table row 8 |
| `field` | pinned value | C-DC-15 | Deployment contract, error code table row 8 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the salted one-way password hash | C-DM-04 | named as the stored form with no literal given |
| the reset token the message carries | C-UF-05 | named as single use with no literal given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 3 |
| User roles | 2 | 20 |
| Core features | 19 | 108 |
| User flow | 9 | 25 |
| UI and UX notes | 4 | 16 |
| Front-end specification | 23 | 44 |
| Technical requirements | 11 | 19 |
| Data model | 5 | 10 |
| Constraints | 3 | 4 |
| Deployment contract | 10 | 17 |

