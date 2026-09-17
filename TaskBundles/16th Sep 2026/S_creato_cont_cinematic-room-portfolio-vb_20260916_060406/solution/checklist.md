# Checklist: cinematic-room-portfolio

Items: 37
Unpinned values flagged: 0
Sections present: C-CF, C-RL, C-TR, C-DM, C-OV, C-UF, C-UX, C-CN

## C-CF Core features

- [ ] `C-CF-01` `capability` The health endpoint returns a ready status. `src: Deployment contract`
- [ ] `C-CF-02` `capability` The published site read returns the rooms in their published order. `src: Core features`
- [ ] `C-CF-03` `capability` A published room scene image streams from the stored object under the key scheme scenes/{site_id}/{room_id}/{sha256_of_bytes}.{ext}. `src: Core features`
- [ ] `C-CF-04` `capability` The header player lists the published releases in their position order. `src: Core features`
- [ ] `C-CF-05` `capability` A signed-in visitor signs one standing guest-book note. `src: Core features`
- [ ] `C-CF-06` `capability` A creator upload writes a room scene image to the object store. `src: Core features`
- [ ] `C-CF-07` `capability` Publishing copies the working copy into the published snapshot. `src: Core features`
- [ ] `C-CF-08` `capability` A creator hides a standing note off the public guest book. `src: Core features`
- [ ] `C-CF-09` `capability` A creator restores a hidden note to the public guest book. `src: Core features`
- [ ] `C-CF-10` `capability` A creator reorders the rooms on the owned site. `src: Core features`
- [ ] `C-CF-11` `capability` A privacy page reachable from the footer states what the site stores about a visitor. `src: Core features`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out request for a studio endpoint is refused as not-signed-in. `src: User roles`
- [ ] `C-RL-02` `role` A visitor request for a studio endpoint is refused as not-allowed-for-you. `src: User roles`
- [ ] `C-RL-03` `role` A creator write against a site the caller does not own is refused as not-allowed-for-you. `src: User roles`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` A guest-book sign missing the note text is refused as something-missing-or-wrong. `src: Technical requirements`
- [ ] `C-TR-02` `constraint` A second standing note by one visitor on one site is refused as that-clashes. `src: Technical requirements`
- [ ] `C-TR-03` `constraint` A public read of a draft site is refused as no-such-thing. `src: Technical requirements`
- [ ] `C-TR-04` `constraint` A public read of a draft room scene is refused as no-such-thing. `src: Technical requirements`
- [ ] `C-TR-05` `constraint` A signed-out guest-book sign is refused as not-signed-in. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Each public route returns a document title distinct from every other public route. `src: Technical requirements`
- [ ] `C-TR-07` `contract` The sitemap lists every public route. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The public site read reconciles with the latest published snapshot rows. `src: Data model`
- [ ] `C-DM-02` `data` A room edit after publishing stays off the public read until the next publish. `src: Data model`

## C-OV Overview

- [ ] `C-OV-01` `ui` The site presents the public rooms alongside an owner studio. `src: Overview`

## C-UF User flow

- [ ] `C-UF-01` `ui` Publishing a room moves the room onto the public site in place. `src: User flow`
- [ ] `C-UF-02` `ui` An owner reading the owned site sees the working copy rather than the published snapshot. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` A visitor moves through the rooms a whole room at a time. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` A glass button brightens the border on hover rather than filling. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Room reveals ease at one shared speed rather than snapping. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A reduced-motion preference collapses every room reveal to a still state. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Body text holds WCAG AA contrast against the near-black ground in both themes. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The rooms stack to a single readable column at a narrow phone width. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Each scene image carries descriptive alternative text naming the scene. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Each page leads with one primary action set apart from the secondary actions. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The record player sits in the page header rather than inside a room. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The guest book of standing notes appears beneath the last room. `src: UI/UX notes`

## C-CN Constraints

- [ ] `C-CN-01` `ui` Interface icons alongside the rail markers are drawn in code rather than shipped as image files. `src: Constraints`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `scenes/{site_id}/{room_id}/{sha256_of_bytes}.{ext}` | room scene object key scheme | `C-CF-03` |
| `deku-demo-pw-2026` | seeded account password | `C-CF-05` |
| `not-signed-in` | unauthorized failure kind | `C-RL-01` |
| `not-allowed-for-you` | forbidden failure kind | `C-RL-02` |
| `something-missing-or-wrong` | validation failure kind | `C-TR-01` |
| `that-clashes` | duplicate failure kind | `C-TR-02` |
| `no-such-thing` | missing failure kind | `C-TR-03` |
| `the-rules-dont-allow-that` | business-rule failure kind | `C-CF-07` |
| `atrium` | the published site handle | `C-CF-02` |
| `nightshift` | the draft site handle | `C-TR-03` |
