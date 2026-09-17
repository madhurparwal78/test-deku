# Checklist: issue-cycle-tracker

Items: 52
Sections present: C-CF, C-RL, C-DM, C-TR, C-UF, C-UX, C-OV, C-CN

## C-CF Core features

- [ ] `C-CF-01` `capability` The health endpoint returns a ready status. `src: Deployment contract`
- [ ] `C-CF-02` `capability` Signing in with a seeded member issues a bearer token. `src: Core features`
- [ ] `C-CF-03` `constraint` A sign-in with a wrong password is refused as a client error. `src: Core features`
- [ ] `C-CF-04` `capability` Filing an issue assigns the next per-team issue key. `src: Core features`
- [ ] `C-CF-05` `capability` A newly filed issue starts in the backlog state with no assignee. `src: Core features`
- [ ] `C-CF-06` `constraint` Filing an issue with a blank title is refused as invalid. `src: Core features`
- [ ] `C-CF-07` `capability` A lead reads the inbox of unassigned, uncycled issues. `src: Core features`
- [ ] `C-CF-08` `capability` A lead assigning an inbox issue to a member persists the new assignee. `src: Core features`
- [ ] `C-CF-09` `capability` Assigning an issue to a member delivers exactly one email to that member. `src: Core features`
- [ ] `C-CF-10` `constraint` The assignment email subject begins with the phrase Assigned to you. `src: Core features`
- [ ] `C-CF-11` `constraint` No email is sent for a change that touches only the label or the estimate. `src: Core features`
- [ ] `C-CF-12` `capability` Moving another member's assigned issue sends one update email to the assignee. `src: Core features`
- [ ] `C-CF-13` `capability` A member move of an owned issue to the next state survives a reload. `src: Core features`
- [ ] `C-CF-14` `capability` Closing a cycle returns every unfinished issue to the inbox. `src: Core features`
- [ ] `C-CF-15` `capability` Closing a cycle reports the count of issues moved. `src: Core features`
- [ ] `C-CF-16` `constraint` A closed cycle refuses any move of its issues. `src: Core features`
- [ ] `C-CF-17` `capability` A member comments on an issue with the author recorded. `src: Core features`
- [ ] `C-CF-18` `capability` An admin reads the team page-view log. `src: Core features`

## C-RL User roles

- [ ] `C-RL-01` `role` A member moving an issue owned by another member is denied by the server. `src: User roles`
- [ ] `C-RL-02` `role` A denied move leaves the issue state unchanged. `src: User roles`
- [ ] `C-RL-03` `role` A member requesting the inbox is denied by the server. `src: User roles`
- [ ] `C-RL-04` `role` A request for another team's issue is answered as not found. `src: User roles`
- [ ] `C-RL-05` `role` An admin removing its own admin role is denied by the server. `src: User roles`
- [ ] `C-RL-06` `role` A lead requesting the admin-only members endpoint is denied by the server. `src: User roles`

## C-DM Data model

- [ ] `C-DM-01` `data` The seeded team Orbit has four seeded members. `src: Data model`
- [ ] `C-DM-02` `data` The seeded active cycle Cycle 24 is present. `src: Data model`
- [ ] `C-DM-03` `data` The seeded closed cycle Cycle 23 is present. `src: Data model`
- [ ] `C-DM-04` `data` A state change writes one matching activity record for the issue. `src: Data model`
- [ ] `C-DM-05` `data` At most one cycle per team is active at any time. `src: Data model`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Two requests to activate a second cycle in one team resolve to exactly one active cycle. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The losing cycle-activation request is refused as a conflict. `src: Technical requirements`
- [ ] `C-TR-03` `contract` Replaying a create-issue request with the same client request id creates no second issue. `src: Technical requirements`
- [ ] `C-TR-04` `contract` Every issue key in a team is distinct, never reused. `src: Technical requirements`
- [ ] `C-TR-05` `contract` No credential, key or token appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Every response carries a strict transport security header. `src: Technical requirements`
- [ ] `C-TR-07` `contract` Every response carries a nosniff content-type header. `src: Technical requirements`

## C-UF User flow

- [ ] `C-UF-01` `ui` A signed-out visit to a protected route lands on the sign-in page. `src: User flow`
- [ ] `C-UF-02` `ui` A signed-in member landing shows the cycle board. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The layout is a fixed left sidebar beside the board surface. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The board shows the active cycle across five workflow-state columns. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Each workflow state shows a distinct glyph readable without colour. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The single accent colour marks the primary action alone. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Body text holds a WCAG AA contrast ratio against the dark surface. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The layout holds at a narrow viewport with no sideways scroll. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Motion stays restrained under an eased character. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A refused optimistic change is rolled back with a message. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The product commits to a dark surface with quiet layered panels. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Identifiers use a monospace family with aligned figures. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A board card shows the issue key beside the title. `src: UI/UX notes`

## C-OV Overview

- [ ] `C-OV-01` `ui` The product opens onto the cycle board as its main working surface. `src: Overview`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No font, image or video file is served by the product. `src: Constraints`
- [ ] `C-CN-02` `ui` Another team's data is never shown in the interface. `src: Constraints`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-CF-02` |
| `member@example.com` | a seeded member account | `C-CF-08` |
| `ORB` | the seeded team key | `C-CF-04` |
| `Assigned to you: ` | assignment email subject prefix | `C-CF-10` |
| `Issue updated: ` | state-change email subject prefix | `C-CF-12` |
| `Orbit` | the seeded team | `C-DM-01` |
| `Cycle 24` | the seeded active cycle | `C-DM-02` |
| `Cycle 23` | the seeded closed cycle | `C-DM-03` |
| `backlog` | the state a filed issue starts in | `C-CF-05` |
| `4.5:1` | the WCAG AA contrast ratio | `C-UX-05` |
