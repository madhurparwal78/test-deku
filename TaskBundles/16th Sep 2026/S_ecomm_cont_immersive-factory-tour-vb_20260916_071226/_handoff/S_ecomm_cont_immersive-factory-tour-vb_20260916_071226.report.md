# Build report: S_ecomm_cont_immersive-factory-tour-vb_20260916_071226

## Identity

- Task code: `S_ecomm_cont_immersive-factory-tour-vb_20260916_071226`
- Task id: `deku/immersive-factory-tour-vb`
- Cell: solo_founder / ecommerce-retail / content-publishing
- Service profile: P4-db-storage (slots: db, storage)
- Providers per slot: db -> postgres (postgres:16.4-bookworm); storage -> minio (minio/minio:RELEASE.2024-10-13T13-34-11Z)
- Variant: b; variant_axes: [critical_depth, spec_sections]
- Language: typescript; stack (drawn): Express + SvelteKit (ssr-islands)
- design_direction: companion (a full PRD was supplied)
- capability_flags: aesthetic, concurrency_hardening
- launch_surface (drawn): cookie_choice, favicon, no_frontend_secrets, privacy_page, security_headers
- spec_sections_given: overview, roles, features, flow, uiux, techrequirements, datamodel, buildplan, constraints, contract
- Shard 1 of 1

## Source resolution

The Task Order named `ecommerce-retail` / `content-publishing` /
`immersive-factory-tour`; the PRD (a captured 3D brand-workshop experience for an
apparel maker) records the same mapping in its own Section 23.3, and names the
prize-draw submission as the graded workflow. `content-publishing` is a live
solo_founder cell (P4-db-storage), so storage is genuine rather than reframed
away: the maker (the `author`) publishes tour chapters and prize garments as
content, and each poster and prize image is written as an object in MinIO. The
content-publishing critical focus, "object in the store; protected content not
publicly readable", is carried by the publish-to-object rule and the rule that a
draft chapter's poster is refused to anyone but the author. The prize-draw entry
is the lead-capture end state, one per reader, and carries the
`concurrency_hardening` obligation.

`design_direction = "companion"`, so the PRD's measured palette (carried by role
and by family/tone/shade words, never as hex or rgb), its type families and
scale, its physical continuous motion, and its accessibility floors reach
`## UI/UX notes`. G51 (`source_lint`) PASSES with every colour, heading and
enumerated item carried; the un-buildable, binary-heavy layers of the PRD (the
real-time 3D engine and its 193 models / 768 textures / 50 environment maps / 50
audio files, the vector-animation runtime, the device and second-screen modes,
the asset pipeline, the capture-methodology and evidence-gap sections, and the
acceptance checklist) are declared waivers: this build ships no binary and
substitutes every asset class procedurally, so those sections describe a product
this lean content build does not construct.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Publish a tour chapter with a stored poster object | INCLUDED | Core features, Data model | The storage substrate; object-in-store critical focus |
| Protected draft content (draft poster refused to non-authors) | INCLUDED | Core features, User roles | The content-publishing critical focus |
| Publish prize garments with stored images | INCLUDED | Core features | The three signature polos, each a stored object |
| The guided three-station tour with a running tally | INCLUDED | Core features, UI/UX notes | The idea's gamified spine, reframed onto published content |
| Prize-draw entry, one per reader, consent-gated | INCLUDED | Core features, Technical requirements | The graded workflow (PRD 19.2); concurrency_hardening |
| Idempotent / concurrent entry (exactly one, 409, no second write) | INCLUDED | Technical requirements | The one-entry-per-reader invariant |
| Server-side authorization (reader cannot publish; draft private) | INCLUDED | User roles, Core features | The permission boundary |
| Launch surface: cookie choice, privacy page, favicon, no secrets, security headers | INCLUDED | Core features, Technical requirements | reference/O draw, each graded |
| Real-time 3D scene, WebGL engine, models/textures/environments/audio | WAIVED | - | Zero-binary build; substituted procedurally (PRD Section 22) |
| Device / second-screen / signage / legacy modes, sync channel | WAIVED | - | Out of scope for the lean content build (G51 waivers) |
| Capture methodology, evidence gaps, acceptance checklist | WAIVED | - | PRD methodology, not product obligations |

## Gate log

All mechanical gates (batteries 1-2) PASS; rendered from
`S_ecomm_cont_immersive-factory-tour-vb_20260916_071226.gates.jsonl` (one row per
gate, each carrying the SHA-256 of the bytes it examined). G59/G60 return
NOT-APPLICABLE (no source-target code-quality rubric shipped). Battery 3 (G13,
G15, G18-G21, G25) and the adversarial-LLM gates (G23, G34, G35, G36, G37b, G53)
are declared, not proven here.

## Honest exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. `solution/` carries the checklist, the answer
key (trinity) and the loud-fail `solve.sh`; no reference app ships. The bundle is
not admissible until the app is generated downstream from `solution/checklist.md`
and `harbor run -a oracle` returns 1.0 twice.
