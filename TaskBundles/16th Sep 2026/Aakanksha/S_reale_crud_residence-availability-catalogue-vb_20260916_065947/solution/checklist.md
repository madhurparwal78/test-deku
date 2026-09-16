# Checklist: residence-availability-catalogue

Items: 30
Unpinned values flagged: 0
Sections present: C-CF, C-RL, C-TR, C-DM, C-OV, C-UF, C-UX

## C-CF Core features

- [ ] `C-CF-01` `capability` The health endpoint returns a ready status. `src: Deployment contract`
- [ ] `C-CF-02` `capability` The apartment list read returns the released apartments. `src: Core features`
- [ ] `C-CF-03` `capability` The apartment list narrows by typology combined with bedroom count. `src: Core features`
- [ ] `C-CF-04` `capability` A released apartment reads in full at its own address. `src: Core features`
- [ ] `C-CF-05` `capability` A released apartment floor plan streams from the stored object under the key scheme plans/{unit_id}/{index}/{sha256_of_bytes}.{ext}. `src: Core features`
- [ ] `C-CF-06` `capability` A callback request records the chosen apartment reference alongside the contact details. `src: Core features`
- [ ] `C-CF-07` `capability` A sales user reads the callback requests. `src: Core features`
- [ ] `C-CF-08` `capability` A sales user releases a coming-soon apartment to the public index. `src: Core features`
- [ ] `C-CF-09` `capability` A first-visit cookie choice survives a reload. `src: Core features`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out request for a sales endpoint is refused as not-signed-in. `src: User roles`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` A callback request missing a required field is refused as something-missing-or-wrong. `src: Technical requirements`
- [ ] `C-TR-02` `constraint` A public read of a coming-soon apartment is refused as no-such-thing. `src: Technical requirements`
- [ ] `C-TR-03` `constraint` A public read of a coming-soon apartment floor plan is refused as no-such-thing. `src: Technical requirements`
- [ ] `C-TR-04` `constraint` An illegal availability step is refused as the-rules-dont-allow-that. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Each public route returns a document title distinct from every other public route. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The public apartment index reconciles with the released rows. `src: Data model`
- [ ] `C-DM-02` `data` Sorting by area orders the apartments by interior area alone. `src: Data model`

## C-OV Overview

- [ ] `C-OV-01` `ui` The site presents the public apartment catalogue alongside a sales console. `src: Overview`

## C-UF User flow

- [ ] `C-UF-01` `ui` Releasing an apartment moves the apartment onto the public index in place. `src: User flow`
- [ ] `C-UF-02` `ui` The callback form prefills the apartment when opened from a detail page. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The live count on the index equals the number of apartments shown. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The apartment index narrows through a quiet row of filter controls. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Opening an apartment on the index reaches its floor plans. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Photography is uncovered rather than faded on arrival. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Reveals on the index ease at one shared speed rather than snapping. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` A reduced-motion preference collapses every reveal to a still state. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Each floor plan image carries descriptive alternative text naming the plan. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` The apartment index leads with one primary action set apart from the filter controls. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Body text holds WCAG AA contrast against the warm neutral ground. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The apartment grid reflows to a single readable column at a narrow phone width. `src: UI/UX notes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `plans/{unit_id}/{index}/{sha256_of_bytes}.{ext}` | floor plan object key scheme | `C-CF-05` |
| `deku-demo-pw-2026` | seeded sales password | `C-CF-07` |
| `not-signed-in` | unauthorized failure kind | `C-RL-01` |
| `something-missing-or-wrong` | validation failure kind | `C-TR-01` |
| `no-such-thing` | missing failure kind | `C-TR-02` |
| `the-rules-dont-allow-that` | business-rule failure kind | `C-TR-04` |
