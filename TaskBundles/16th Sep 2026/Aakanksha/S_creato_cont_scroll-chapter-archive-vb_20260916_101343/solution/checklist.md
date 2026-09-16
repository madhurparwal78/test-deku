# Checklist: scroll-chapter-archive

Items: 37
Unpinned values flagged: 0
Sections present: C-CF, C-RL, C-TR, C-DM, C-OV, C-UF, C-UX, C-CN

## C-CF Core features

- [ ] `C-CF-01` `capability` The health endpoint returns a ready status. `src: Deployment contract`
- [ ] `C-CF-02` `capability` The chapter list read returns the published chapters in story order. `src: Core features`
- [ ] `C-CF-03` `capability` A published chapter poster image streams from the stored object under the key scheme posters/{chapter_id}/{sha256_of_bytes}.{ext}. `src: Core features`
- [ ] `C-CF-04` `capability` A curator publishes a draft chapter to the public story. `src: Core features`
- [ ] `C-CF-05` `capability` A signed-in member captures a frame into the archive. `src: Core features`
- [ ] `C-CF-06` `capability` A member archive alongside the reading position reads back on a fresh session. `src: Core features`
- [ ] `C-CF-07` `capability` A member sets the order of the captures in a route the member owns. `src: Core features`
- [ ] `C-CF-08` `capability` A member publishes a route holding at least two captures to the public index. `src: Core features`
- [ ] `C-CF-09` `capability` A curator features a published route. `src: Core features`
- [ ] `C-CF-10` `capability` A first-visit cookie choice survives a reload. `src: Core features`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out request for a member endpoint is refused as not-signed-in. `src: User roles`
- [ ] `C-RL-02` `role` A member request for a curator endpoint is refused as not-allowed-for-you. `src: User roles`
- [ ] `C-RL-03` `role` A member write against a route the caller does not own is refused as not-allowed-for-you. `src: User roles`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` A capture missing its title is refused as something-missing-or-wrong. `src: Technical requirements`
- [ ] `C-TR-02` `constraint` A public read of a draft chapter is refused as no-such-thing. `src: Technical requirements`
- [ ] `C-TR-03` `constraint` A public read of a draft chapter poster is refused as no-such-thing. `src: Technical requirements`
- [ ] `C-TR-04` `constraint` A route published with fewer than two captures is refused as the-rules-dont-allow-that. `src: Technical requirements`
- [ ] `C-TR-05` `constraint` A public read of a draft route is refused as no-such-thing. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Each public route returns a document title distinct from every other public route. `src: Technical requirements`
- [ ] `C-TR-07` `contract` Every response carries the standard security headers. `src: Technical requirements`
- [ ] `C-TR-08` `contract` No credential appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-09` `contract` Each public route declares a social preview whose image resolves. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The public story reconciles with the published chapter rows. `src: Data model`

## C-OV Overview

- [ ] `C-OV-01` `ui` The site presents a public story, a member archive, a curator queue. `src: Overview`

## C-UF User flow

- [ ] `C-UF-01` `ui` Publishing a chapter moves the chapter onto the public story in place. `src: User flow`
- [ ] `C-UF-02` `ui` A member finds the same archive on a fresh session. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The chapters dissolve through the scene as the visitor scrolls. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The act marks glide rather than jump. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` A reduced-motion preference collapses every animation to a still state. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A reorder in the archive is its own feedback with no toast. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Body text holds WCAG AA contrast against the dark ground. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The archive grid reflows to a single readable column at a narrow phone width. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Each chapter poster carries descriptive alternative text naming the scene. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Each page leads with one primary action set apart from the secondary controls. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The one red accent is spent on the featured route mark alone. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The act headings dissolve edge-lit rather than fading. `src: UI/UX notes`

## C-CN Constraints

- [ ] `C-CN-01` `ui` Interface icons alongside the studio mark are drawn in code rather than shipped as image files. `src: Constraints`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `posters/{chapter_id}/{sha256_of_bytes}.{ext}` | chapter poster object key scheme | `C-CF-03` |
| `deku-demo-pw-2026` | seeded account password | `C-CF-05` |
| `not-signed-in` | unauthorized failure kind | `C-RL-01` |
| `not-allowed-for-you` | forbidden failure kind | `C-RL-02` |
| `something-missing-or-wrong` | validation failure kind | `C-TR-01` |
| `no-such-thing` | missing failure kind | `C-TR-02` |
| `the-rules-dont-allow-that` | business-rule failure kind | `C-TR-04` |
| `cookie_choice` | cookie preference name | `C-CF-10` |
| `solar` | the opening published chapter | `C-CF-02` |
| `bone` | a draft chapter | `C-TR-02` |
