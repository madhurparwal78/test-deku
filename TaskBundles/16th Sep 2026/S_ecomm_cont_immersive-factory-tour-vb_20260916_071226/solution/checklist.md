# Checklist: immersive-factory-tour

Items: 49
Sections present: C-CF, C-RL, C-DM, C-TR, C-UF, C-UX, C-OV, C-CN

## C-CF Core features

- [ ] `C-CF-01` `capability` The health endpoint returns a ready status. `src: Deployment contract`
- [ ] `C-CF-02` `capability` Signing in with a seeded account issues a bearer token. `src: Core features`
- [ ] `C-CF-03` `capability` Open signup creates a reader account. `src: Core features`
- [ ] `C-CF-04` `constraint` A sign-in with a wrong password is refused as a client error. `src: Core features`
- [ ] `C-CF-05` `capability` Creating a chapter writes its poster to the object store at the key scheme. `src: Core features`
- [ ] `C-CF-06` `capability` Publishing a chapter makes its poster publicly readable. `src: Core features`
- [ ] `C-CF-07` `constraint` A draft chapter poster is refused to a stranger. `src: Core features`
- [ ] `C-CF-08` `capability` Unpublishing a chapter returns the chapter to draft. `src: Core features`
- [ ] `C-CF-09` `capability` Publishing a prize writes its image to the object store. `src: Core features`
- [ ] `C-CF-10` `capability` A reader reads the tour of published chapters in station order. `src: Core features`
- [ ] `C-CF-11` `capability` Triggering a hotspot raises the reader running tally. `src: Core features`
- [ ] `C-CF-12` `capability` A reader submits a prize-draw entry that is stored. `src: Core features`
- [ ] `C-CF-13` `constraint` An entry without the terms consent is refused as invalid. `src: Core features`

## C-RL User roles

- [ ] `C-RL-01` `role` A reader publishing a chapter is denied by the server. `src: User roles`
- [ ] `C-RL-02` `role` A reader requesting the entry list is denied by the server. `src: User roles`
- [ ] `C-RL-03` `role` A reader requesting another reader's entry is denied by the server. `src: User roles`
- [ ] `C-RL-04` `role` A signed-out request to a reader route is refused by the server. `src: User roles`
- [ ] `C-RL-05` `role` A reader fetching a draft chapter poster is refused by the server. `src: User roles`

## C-DM Data model

- [ ] `C-DM-01` `data` The seeded author account is present. `src: Data model`
- [ ] `C-DM-02` `data` The two seeded reader accounts are present. `src: Data model`
- [ ] `C-DM-03` `data` Three published chapters, one per station, are present. `src: Data model`
- [ ] `C-DM-04` `data` A seeded draft chapter with a stored poster is present. `src: Data model`
- [ ] `C-DM-05` `data` Three published prizes are present. `src: Data model`
- [ ] `C-DM-06` `data` At most one prize-draw entry exists per reader. `src: Data model`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Two concurrent entry submissions by one reader resolve to exactly one stored entry. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The losing duplicate entry submission is refused as a conflict. `src: Technical requirements`
- [ ] `C-TR-03` `contract` Replaying an entry with the same client request id creates no second entry. `src: Technical requirements`
- [ ] `C-TR-04` `contract` A chapter poster lives in the object store, never on the app filesystem. `src: Technical requirements`
- [ ] `C-TR-05` `contract` No credential, key or token appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Every response carries a strict transport security header. `src: Technical requirements`
- [ ] `C-TR-07` `contract` Every response carries a nosniff content-type header. `src: Technical requirements`
- [ ] `C-TR-08` `contract` The document head declares a favicon the site serves. `src: Technical requirements`

## C-UF User flow

- [ ] `C-UF-01` `ui` A signed-out visit to a reader route lands on the login page. `src: User flow`
- [ ] `C-UF-02` `ui` A signed-in reader landing shows the tour. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The title screen reads as a living scene with a spinning backdrop. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The tour presents three tinted stations in a fixed order. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The primary action colour marks one action alone. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Body text holds a WCAG AA contrast ratio. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The layout holds at a narrow viewport with no sideways scroll. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Motion stays continuous, honouring a reduced-motion preference. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` The registration form rises from below on a deep soft shadow. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A refused submission rolls back the optimistic row with a message. `src: User flow`
- [ ] `C-UX-09` `ui` A published prize shows its stored image. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The persistent promo card offers the prize draw from the corner. `src: UI/UX notes`

## C-OV Overview

- [ ] `C-OV-01` `ui` The product opens onto the workshop title screen. `src: Overview`

## C-CN Constraints

- [ ] `C-CN-01` `ui` A first-time visitor is asked once about non-essential cookies. `src: Core features`
- [ ] `C-CN-02` `ui` A privacy page is reachable from the footer of every page. `src: Core features`
- [ ] `C-CN-03` `ui` A draft chapter is absent from the public tour. `src: Core features`
- [ ] `C-CN-04` `constraint` No image, font or media file is served by the product. `src: Constraints`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-CF-02` |
| `author@example.com` | the seeded maker account | `C-DM-01` |
| `reader@example.com` | a seeded reader account | `C-CF-12` |
| `knitting` | the first station | `C-DM-03` |
| `chapters/` | the poster object key scheme | `C-CF-05` |
| `Signature Green` | a seeded prize garment | `C-DM-05` |
| `consent_terms` | the required consent flag | `C-CF-13` |
| `4.5:1` | the WCAG AA contrast ratio | `C-UX-04` |
