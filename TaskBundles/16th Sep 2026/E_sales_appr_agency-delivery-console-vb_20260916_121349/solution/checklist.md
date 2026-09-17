# Checklist: Parallax

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Items: 418
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` Approvals release invoices `src: Overview, approvals release invoices`
- [ ] `C-OV-02` `constraint` Invoice numbers stay gapless `src: Overview, numbers must stay gapless`
- [ ] `C-OV-03` `constraint` No principal holds standing access to a client secret `src: Overview, no one holds standing access to a client secret`
- [ ] `C-OV-04` `capability` The client portal opens under the portal address `src: Overview, the client portal under /portal`
- [ ] `C-OV-05` `capability` The agency back office opens under the portal agency address `src: Overview, the agency back office under /portal/agency`
- [ ] `C-OV-06` `constraint` Self-serve signup is absent `src: Overview, has no self-serve signup`

## C-RL User roles

- [ ] `C-RL-01` `role` A project manager session calling a finance admin endpoint is rejected by the server `src: User roles, a direct API call from a project manager session to any finance admin-only endpoint must be rejected by the server`
- [ ] `C-RL-02` `constraint` A denied call leaves the protected state unchanged `src: User roles, leaving the protected state unchanged`
- [ ] `C-RL-03` `role` A role counts only in the scope held `src: User roles, A role counts only in the scope it is held in`
- [ ] `C-RL-04` `role` A finance admin issues invoices for its own entity only `src: User roles, invoices, credit notes, payments for its entity`
- [ ] `C-RL-05` `role` An account director reads margin on a portfolio proposal `src: User roles, its portfolio, rates, margin, approvals`
- [ ] `C-RL-06` `role` A project manager holding no grant reads no cost or margin `src: User roles, cost or margin without a grant`
- [ ] `C-RL-07` `role` A client approver is refused approvals above the approver threshold `src: User roles, anything above its threshold`
- [ ] `C-RL-08` `role` A client collaborator is refused an approval decision `src: User roles, comments, annotations, tickets`
- [ ] `C-RL-09` `role` A client owner reads no other organisation `src: User roles, its whole organisation, final approver`
- [ ] `C-RL-10` `role` A contractor reads exactly what an expiring grant names `src: User roles, exactly what an expiring grant names`
- [ ] `C-RL-11` `role` A security officer gives the second approval of a break-glass request `src: User roles, vault policy, second approvals, audit export`
- [ ] `C-RL-12` `role` Invoices of the client organisation are listed for a client finance principal `src: User roles, invoices and billing documents`
- [ ] `C-RL-13` `role` A producer holds no standing credential `src: User roles, financial fields, standing credentials`
- [ ] `C-RL-14` `role` A producer reads no financial fields `src: User roles, financial fields, standing credentials`
- [ ] `C-RL-15` `role` A finance admin is refused the vault secret list `src: User roles, approves deliverables, opens the vault`
- [ ] `C-RL-16` `role` An account director is refused invoice issue `src: User roles, issues invoices`
- [ ] `C-RL-17` `role` An analyst is refused a milestone write `src: User roles, writes outside reports`
- [ ] `C-RL-18` `role` A recruiter is refused client project data `src: User roles, applicants | client data`
- [ ] `C-RL-19` `role` A client finance principal is refused a deliverable read `src: User roles, invoices and billing documents | deliverables`
- [ ] `C-RL-20` `role` A security officer is refused approving the officer's own break-glass request `src: User roles, approves its own break-glass`

## C-CF Core features

- [ ] `C-CF-01` `constraint` Issued invoice numbers per entity per document type per year form a contiguous run `src: Core features, form a contiguous run with no gap and no repeat`
- [ ] `C-CF-02` `constraint` Simultaneous issues never share a number `src: Core features, however many issues arrive at once`
- [ ] `C-CF-03` `constraint` A refused issue takes no number `src: Core features, an issue refused for any reason takes no number`
- [ ] `C-CF-04` `constraint` A reverse charge needs a validated VAT number `src: Core features, Reverse charge needs a validated VAT number`
- [ ] `C-CF-05` `constraint` A validation older than ninety days with the register unreachable refuses the issue `src: Core features, a validation older than ninety days while the register is unreachable`
- [ ] `C-CF-06` `constraint` A refused reverse charge leaves the draft untouched `src: Core features, leaves the draft untouched`
- [ ] `C-CF-07` `constraint` The uploader of the version under review is refused a decision `src: Core features, Whoever uploaded the version under review is refused a decision on it`
- [ ] `C-CF-08` `constraint` A refused uploader decision leaves the approval unchanged `src: Core features, the approval is unchanged`
- [ ] `C-CF-09` `capability` Uploading a new version cancels the pending approval `src: Core features, Uploading while an approval is pending cancels it`
- [ ] `C-CF-10` `constraint` A decision on the old version is refused naming the new version `src: Core features, a decision on the old version is refused naming the new one`
- [ ] `C-CF-11` `constraint` A milestone is approved only once every stage is complete `src: Core features, A milestone is approved only when every stage is complete`
- [ ] `C-CF-12` `constraint` Stage completion creates exactly one draft invoice `src: Core features, completion creates exactly one draft invoice`
- [ ] `C-CF-13` `constraint` An approver whose threshold is below the value is refused `src: Core features, An approver whose threshold is below the value is refused`
- [ ] `C-CF-14` `constraint` A contract value equals the original value plus every approved change order `src: Core features, A contract is always its original value plus every approved change order`
- [ ] `C-CF-15` `constraint` Change orders approved at once all reach the contract value `src: Core features, however many are approved at once`
- [ ] `C-CF-16` `constraint` Another organisation's record answers as a missing record `src: Core features, Another organisation's record answers exactly as a record that does not exist`
- [ ] `C-CF-17` `constraint` Cost fields are absent for a caller lacking commercial visibility `src: Core features, cost and margin are absent, not empty`
- [ ] `C-CF-18` `constraint` A reveal needs an approved request bound to an open ticket `src: Core features, A reveal needs an approved request bound to an open ticket`
- [ ] `C-CF-19` `constraint` A reveal needs a recent step-up `src: Core features, a recent step-up`
- [ ] `C-CF-20` `constraint` A reveal request is single use `src: Core features, is single use`
- [ ] `C-CF-21` `constraint` Break-glass needs two different approvers `src: Core features, break-glass needs two different approvers`
- [ ] `C-CF-22` `constraint` No access log entry is ever rewritten `src: Core features, every access is logged in a chain nothing rewrites`
- [ ] `C-CF-23` `constraint` A grant lacking an end is refused `src: Core features, A grant without an end is refused`
- [ ] `C-CF-24` `constraint` An expired grant is denied on the very next request `src: Core features, an expired or revoked grant is denied on the very next request`
- [ ] `C-CF-25` `constraint` A revoked grant is denied on the very next request `src: Core features, an expired or revoked grant is denied on the very next request`
- [ ] `C-CF-26` `constraint` A replayed submission creates one lead `src: Core features, A replayed submission creates one lead`
- [ ] `C-CF-27` `capability` A lead confirmation email comes from the handling entity `src: Core features, one confirmation email from the entity that will handle it`
- [ ] `C-CF-28` `constraint` A bot trap submission is stored silently as spam `src: Core features, a bot trap is stored silently as spam`
- [ ] `C-CF-29` `constraint` Invalid lead fields are refused by name `src: Core features, invalid fields are refused by name`
- [ ] `C-CF-30` `constraint` No gclid is kept without marketing consent `src: Core features, no gclid is kept without marketing consent`
- [ ] `C-CF-31` `constraint` A changed public address redirects permanently `src: Core features, A changed or legacy address redirects permanently`
- [ ] `C-CF-32` `constraint` A legacy public address redirects permanently `src: Core features, A changed or legacy address redirects permanently`
- [ ] `C-CF-33` `capability` Language alternates are derived `src: Core features, language alternates are derived`
- [ ] `C-CF-34` `constraint` Thin landing pages stay out of the sitemap `src: Core features, thin landing pages stay out of the sitemap`
- [ ] `C-CF-35` `capability` A privacy page is served `src: Core features, a privacy page and favicon are served`
- [ ] `C-CF-36` `capability` A favicon is served `src: Core features, a privacy page and favicon are served`
- [ ] `C-CF-37` `constraint` No secret reaches the browser `src: Core features, no secret reaches the browser`

## C-UF User flow

- [ ] `C-UF-01` `capability` The English public site is served at the root address `src: User flow, the rest of the English site`
- [ ] `C-UF-02` `capability` The French public site is served under the fr address `src: User flow, the rest of the French site`
- [ ] `C-UF-03` `capability` Every principal signs in at the portal login page `src: User flow, sign in for every principal`
- [ ] `C-UF-04` `ui` The portal home opens on the Needs you block `src: User flow, the Needs you queue`
- [ ] `C-UF-05` `ui` The deliverable page holds viewer, comment rail, approval bar in one split pane `src: User flow, viewer, comment rail and approval bar in one split pane`
- [ ] `C-UF-06` `ui` The sidebar offers Approvals with Invoices, opening the client work lists `src: User flow, client work lists`
- [ ] `C-UF-07` `ui` Finance opens invoicing in the back office `src: User flow, finance and custody`
- [ ] `C-UF-08` `constraint` An unauthenticated portal visit renders the sign in panel in place `src: User flow, an unauthenticated visit renders the sign in panel in place`
- [ ] `C-UF-09` `constraint` An unauthenticated portal visit shows no invoice number `src: User flow, never serves data`
- [ ] `C-UF-10` `ui` A sidebar of sections sits beside the agency day view `src: User flow, A sidebar holds every section`
- [ ] `C-UF-11` `capability` A client approver approves the current version of a shared deliverable `src: User flow, opens a shared deliverable, annotates a point`
- [ ] `C-UF-12` `capability` Finance issues a draft after stepping up `src: User flow, steps up, issues a draft`
- [ ] `C-UF-13` `capability` A requested secret is revealed once after approval with step-up `src: User flow, after approval and step-up it is revealed once`
- [ ] `C-UF-14` `ui` A request for vault access opens in a slide-over `src: User flow, requests a secret from the vault in a slide-over`
- [ ] `C-UF-15` `ui` An empty approvals view shows the reason `src: User flow, empty with the reason`
- [ ] `C-UF-16` `ui` Loading states are shaped like the content `src: User flow, loading shaped like its content`
- [ ] `C-UF-17` `ui` Error states carry the request identifier `src: User flow, error with the request identifier`
- [ ] `C-UF-18` `ui` An approver annotates a point on a shared deliverable `src: User flow, annotates a point`
- [ ] `C-UF-19` `ui` A visitor completing the six step brief sees the reference with the expected response time `src: User flow, sees the reference and expected response time`
- [ ] `C-UF-20` `ui` A denied page says Not found, or you do not have access `src: User flow, permission denied as not found`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Grounds are near-black neutrals under near-white type `src: UI/UX notes, near-black neutral grounds`
- [ ] `C-UX-02` `ui` Parallax offers no light theme `src: UI/UX notes, There is no light theme`
- [ ] `C-UX-03` `ui` Aligned figures use tabular digits `src: UI/UX notes, aligned figures use tabular digits`
- [ ] `C-UX-04` `ui` Reduced motion turns entrances into a short fade `src: UI/UX notes, a reduced motion preference turns entrances into a short fade`
- [ ] `C-UX-05` `ui` Text meets WCAG 2.2 AA contrast `src: UI/UX notes, Text meets WCAG 2.2 AA contrast`
- [ ] `C-UX-06` `ui` Targets are comfortable to touch `src: UI/UX notes, targets are comfortable to touch`
- [ ] `C-UX-07` `ui` Icon-only controls carry labels `src: UI/UX notes, icon-only controls carry labels`
- [ ] `C-UX-08` `ui` Overlays return focus when closed `src: UI/UX notes, overlays close on Escape and return focus`
- [ ] `C-UX-09` `ui` One mid vivid red accent marks primary actions, focus, danger `src: UI/UX notes, one mid, vivid red accent spent on primary actions, focus and danger`
- [ ] `C-UX-10` `ui` A light muted orange serves only as an editorial secondary `src: UI/UX notes, A light, muted orange is an editorial secondary only`
- [ ] `C-UX-11` `ui` Portal statuses pair teal, orange or blue with a word plus a shape `src: UI/UX notes, each always with a word and a shape`
- [ ] `C-UX-12` `ui` Display headings use MargoBeuys from 40px to 112px `src: UI/UX notes, MargoBeuys for display headings, from 40px to 112px`
- [ ] `C-UX-13` `ui` Body text uses Poppins from 15px to 18px `src: UI/UX notes, body from 15px to 18px`
- [ ] `C-UX-14` `ui` The public site is spacious, scroll-driven, motion-rich `src: UI/UX notes, The public site is spacious, scroll-driven and motion-rich`
- [ ] `C-UX-15` `ui` The portal is dense with legible type `src: UI/UX notes, the portal is dense and legible`
- [ ] `C-UX-16` `ui` All motion shares one curve that leaves fast, settling long `src: UI/UX notes, All motion shares one curve that leaves fast and settles long`
- [ ] `C-UX-17` `ui` A reduced motion preference removes smooth scrolling `src: UI/UX notes, removes smooth scrolling entirely`
- [ ] `C-UX-18` `ui` Creation opens in a slide-over `src: UI/UX notes, creation opens in a slide-over`
- [ ] `C-UX-19` `ui` A toast confirms a completed write `src: UI/UX notes, a toast confirms a completed write`
- [ ] `C-UX-20` `ui` Input errors appear beneath the field in the measured words `src: UI/UX notes, Inputs show errors beneath them in the measured words`
- [ ] `C-UX-21` `ui` Every control has a visible focus ring `src: UI/UX notes, every control has a visible focus ring`
- [ ] `C-UX-22` `ui` Overlays close on Escape `src: UI/UX notes, overlays close on Escape`
- [ ] `C-UX-23` `ui` Colour never carries meaning alone `src: UI/UX notes, colour never carries meaning alone`
- [ ] `C-UX-24` `ui` Each breakpoint changes structure rather than size `src: UI/UX notes, each breakpoint changes structure, never size`
- [ ] `C-UX-25` `ui` Money-moving actions ask for typed confirmation naming the object `src: UI/UX notes, money-moving or destructive actions ask for typed confirmation naming the object`
- [ ] `C-UX-26` `ui` The portal is a sidebar beside a split detail pane `src: UI/UX notes, The portal is a sidebar beside a split detail pane`
- [ ] `C-UX-27` `ui` Cards with sheets are flat raised surfaces edged by hairlines `src: UI/UX notes, Cards and sheets are flat raised surfaces edged by hairlines`
- [ ] `C-UX-28` `ui` Primary buttons answer hover with a masked label swap `src: UI/UX notes, primary buttons answer hover with a masked label swap`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Login answers a principal kind of agency, client or external `src: Technical requirements, where principal_kind is agency, client or external`
- [ ] `C-TR-02` `contract` A wrong login pair answers 401 invalid_credentials `src: Technical requirements, a wrong pair is 401 invalid_credentials`
- [ ] `C-TR-03` `contract` Step-up re-proves the session principal with the password `src: Technical requirements, re-proves the session's principal`
- [ ] `C-TR-04` `constraint` Signing in counts as no step-up `src: Technical requirements, Signing in is not a step-up`
- [ ] `C-TR-05` `contract` An action needing step-up without one answers 403 step_up_required `src: Technical requirements, is refused with 403 and code step_up_required`
- [ ] `C-TR-06` `contract` Signup answers 404 not_found `src: Technical requirements, POST /api/auth/signup answers 404 with code not_found`
- [ ] `C-TR-07` `contract` A call lacking a principal answers 401 unauthenticated `src: Technical requirements, refused with 401 and code unauthenticated`
- [ ] `C-TR-08` `contract` A denied read answers as a missing resource `src: Technical requirements, A denied read answers exactly as a missing resource`
- [ ] `C-TR-09` `contract` A denied read carries the detail Not found, or you do not have access `src: Technical requirements, Not found, or you do not have access`
- [ ] `C-TR-10` `contract` A principal lacking the grant for a visible resource answers 403 forbidden `src: Technical requirements, is refused with 403 and code forbidden`
- [ ] `C-TR-11` `contract` A lead lacking an Idempotency-Key answers 422 idempotency_key_required `src: Technical requirements, refused with 422 and code idempotency_key_required`
- [ ] `C-TR-12` `contract` A reused key with a different body answers 409 idempotency_key_reused `src: Technical requirements, the same key with a different body is refused with 409 and code idempotency_key_reused`
- [ ] `C-TR-13` `contract` A replay with the same body returns the original answer `src: Technical requirements, a replay with the same body returns the original status and body`
- [ ] `C-TR-14` `contract` An accepted lead answers 202 with a reference `src: Technical requirements, It answers 202 with`
- [ ] `C-TR-15` `contract` A failing lead body answers 422 with errors naming each field `src: Technical requirements, refused with 422 and errors naming each field`
- [ ] `C-TR-16` `data` A failing lead body stores nothing `src: Technical requirements, and stores nothing`
- [ ] `C-TR-17` `data` A filled decoy lead is stored with status spam `src: Technical requirements, stores the lead with status spam and sends nothing`
- [ ] `C-TR-18` `capability` A filled decoy answers 202 with a reference like an accepted lead `src: Technical requirements, answers 202 with a reference exactly like an accepted lead`
- [ ] `C-TR-19` `data` Every lead is a row of the leads table `src: Technical requirements, Every lead is a row of the leads table`
- [ ] `C-TR-20` `data` A lead gclid is NULL unless marketing consent is true `src: Technical requirements, which is NULL unless marketing_consent is true`
- [ ] `C-TR-21` `data` A lead with marketing consent keeps the gclid `src: Technical requirements, which is NULL unless marketing_consent is true`
- [ ] `C-TR-22` `capability` Each lead that is not spam sends exactly one confirmation email `src: Technical requirements, Each lead that is not spam sends exactly one confirmation email`
- [ ] `C-TR-23` `contract` An English site confirmation subject is the brief subject followed by the reference `src: Technical requirements, Parallax: we received your brief followed by the reference`
- [ ] `C-TR-24` `contract` A French site confirmation subject is the demande subject followed by the reference `src: Technical requirements, Parallax : demande reçue followed by the reference`
- [ ] `C-TR-25` `contract` The first confirmation body line is the handling entity name `src: Technical requirements, The first line of the body is the handling entity's name`
- [ ] `C-TR-26` `capability` A French site submission or a French company routes to parallax-france `src: Technical requirements, entity is parallax-france when the submission came from the French site or the company country is`
- [ ] `C-TR-27` `capability` Any other submission routes to parallax-malta `src: Technical requirements, otherwise parallax-malta`
- [ ] `C-TR-28` `constraint` A spam outcome answers the submitter as an accepted one does `src: Technical requirements, A spam outcome answers the submitter exactly as an accepted one does`
- [ ] `C-TR-29` `constraint` Address-based limits exempt private or loopback addresses `src: Technical requirements, exempts private and loopback addresses`
- [ ] `C-TR-30` `contract` Organisations are listed by slug `src: Technical requirements, GET /api/orgs | slug`
- [ ] `C-TR-31` `contract` The organisation list holds only organisations the caller may see `src: Technical requirements, the caller may see`
- [ ] `C-TR-32` `contract` Projects are listed by code `src: Technical requirements, GET /api/projects | code`
- [ ] `C-TR-33` `contract` A milestone is created with status not_started `src: Technical requirements, with status not_started and trigger on_approval`
- [ ] `C-TR-34` `contract` A deliverable is created with status draft `src: Technical requirements, with status draft`
- [ ] `C-TR-35` `role` Milestones are created by the project manager of the project `src: Technical requirements, Milestones and deliverables are created by the project's project manager or account director`
- [ ] `C-TR-36` `contract` A version upload answers the uploader email `src: Technical requirements, 201 {"id", "version", "uploaded_by_email"}`
- [ ] `C-TR-37` `capability` An uploaded version becomes current `src: Technical requirements, the version becomes current`
- [ ] `C-TR-38` `contract` Sharing a deliverable lacking a version answers 422 version_required `src: Technical requirements, 422 version_required when the deliverable has no version`
- [ ] `C-TR-39` `contract` The approval value is the linked milestone bill amount `src: Technical requirements, value_minor is the linked milestone's bill amount`
- [ ] `C-TR-40` `contract` The current stage number counts from 1 `src: Technical requirements, current_stage is the number of the stage now open counting from 1`
- [ ] `C-TR-41` `contract` Each stage lists the email of every assignee `src: Technical requirements, assignees lists the email of every principal who may decide that stage`
- [ ] `C-TR-42` `contract` A recorded decision names the deciding email `src: Technical requirements, {"decided_by_email", "decision", "comment", "on_behalf_of_email"}`
- [ ] `C-TR-43` `contract` A decision on a cancelled approval answers 409 approval_superseded with current_version_id `src: Technical requirements, 409 approval_superseded with {"current_version_id"}`
- [ ] `C-TR-44` `contract` A version_id other than the approval version answers approval_superseded `src: Technical requirements, or version_id is not the approval's version`
- [ ] `C-TR-45` `contract` A caller outside the current stage assignees answers 403 forbidden `src: Technical requirements, the caller is an assignee of the current stage`
- [ ] `C-TR-46` `contract` An uploader decision answers 403 separation_of_duties `src: Technical requirements, 403 separation_of_duties`
- [ ] `C-TR-47` `contract` A threshold below the value answers 403 approval_threshold_exceeded `src: Technical requirements, 403 approval_threshold_exceeded`
- [ ] `C-TR-48` `contract` A rejection lacking a comment answers 422 comment_required `src: Technical requirements, 422 comment_required`
- [ ] `C-TR-49` `constraint` A refused decision records nothing `src: Technical requirements, A refused decision records nothing and changes nothing`
- [ ] `C-TR-50` `constraint` A repeated decision answers 200 with the approval unchanged `src: Technical requirements, gets 200 with the approval unchanged`
- [ ] `C-TR-51` `capability` The last stage completing approves the deliverable `src: Technical requirements, the approval is approved, the deliverable approved`
- [ ] `C-TR-52` `capability` The milestone becomes approved with approved_at `src: Technical requirements, the milestone approved with approved_at`
- [ ] `C-TR-53` `capability` A draft invoice exists within ten seconds of completion `src: Technical requirements, within ten seconds exactly one draft invoice exists for the milestone`
- [ ] `C-TR-54` `contract` The milestone invoice_id names the draft `src: Technical requirements, its id on the milestone's invoice_id`
- [ ] `C-TR-55` `capability` A rejection at any stage ends the approval as rejected `src: Technical requirements, A rejection at any stage ends the whole approval as rejected`
- [ ] `C-TR-56` `capability` A rejection moves the deliverable to changes_requested `src: Technical requirements, moves the deliverable to changes_requested`
- [ ] `C-TR-57` `capability` An any_of stage completes on one approval `src: Technical requirements, any_of completes when any one assignee approves`
- [ ] `C-TR-58` `constraint` An all_of stage completes only when every assignee approves `src: Technical requirements, all_of when every assignee approves`
- [ ] `C-TR-59` `capability` Sharing selects the policy band containing the bill amount `src: Technical requirements, whose value band contains the milestone's bill amount`
- [ ] `C-TR-60` `capability` A new version cancels the pending approval rather than carrying the approval over `src: Technical requirements, that approval is cancelled, not carried over`
- [ ] `C-TR-61` `constraint` The draft invoice is created once per milestone however often the event arrives `src: Technical requirements, the draft is created once per milestone however many times the event is delivered`
- [ ] `C-TR-62` `capability` An approval request email goes to each assignee of the current stage `src: Technical requirements, one message to each assignee of the now current stage and to no one else`
- [ ] `C-TR-63` `contract` The approval email subject is the request subject followed by the deliverable name `src: Technical requirements, subject Parallax: approval requested for followed by the deliverable's name`
- [ ] `C-TR-64` `contract` The approval email body opens with the approval id `src: Technical requirements, with the approval id as the first line of the body`
- [ ] `C-TR-65` `constraint` Assignees of later stages receive nothing for the current stage `src: Technical requirements, the assignees of later stages`
- [ ] `C-TR-66` `constraint` The uploader receives no approval request email `src: Technical requirements, The uploader, the assignees of later stages`
- [ ] `C-TR-67` `data` An Aeroline value above 2000000 adds an all_of stage of owner with procurement `src: Technical requirements, stage 2 all_of owner@aeroline.example.com and procurement@aeroline.example.com`
- [ ] `C-TR-68` `data` Aeroline stage 1 is any_of every active Brand client approver `src: Technical requirements, stage 1 any_of every active client_approver of Digital > Brand`
- [ ] `C-TR-69` `data` Verdane approvals name the Verdane owner with the account director `src: Technical requirements, stage 1 any_of owner@verdane.example.com and the account's director`
- [ ] `C-TR-70` `data` The second Aeroline brand approver holds a threshold of 1000000 `src: Technical requirements, | brand2@aeroline.example.com | Aeroline | client_approver | Digital > Brand | 1000000 |`
- [ ] `C-TR-71` `data` The seeded proposal margin is 1405000 `src: Technical requirements, is 1405000`
- [ ] `C-TR-72` `data` Issued invoice PXF-2026-00002 belongs to Aeroline `src: Technical requirements, PXF-2026-00002 to Aeroline`
- [ ] `C-TR-73` `data` Kessler holds an invalid VAT validation state `src: Technical requirements, kessler | Kessler Werkzeug GmbH | DE | DE500000005 | invalid`
- [ ] `C-TR-74` `data` Vondel last validated 40 days before seeding with the register unavailable `src: Technical requirements, service_unavailable | 40 days before seeding`
- [ ] `C-TR-75` `data` Alpenrad last validated 120 days before seeding `src: Technical requirements, service_unavailable | 120 days before seeding`
- [ ] `C-TR-76` `data` Ticket PX-2026-000143 is closed `src: Technical requirements, PX-2026-000143 | Verdane | p3 | closed`
- [ ] `C-TR-77` `data` Each ticket references the managed site of the organisation `src: Technical requirements, Each ticket references its organisation's managed site`
- [ ] `C-TR-78` `data` The on-call producer works on the 24x7 calendar `src: Technical requirements, so its working window is the 24x7 calendar`
- [ ] `C-TR-79` `data` A request is break-glass only when break_glass is true `src: Technical requirements, break-glass only when its break_glass is true, whatever the hour it is made`
- [ ] `C-TR-80` `data` The vault access log starts empty `src: Technical requirements, The vault access log starts empty`
- [ ] `C-TR-81` `data` Contract PXF-CT-2026-003 is worth 3000000 `src: Technical requirements, PXF-CT-2026-003 | 3000000`
- [ ] `C-TR-82` `data` Institut Lumiere is a public_sector client `src: Technical requirements, public_sector`
- [ ] `C-TR-83` `contract` Margin is absent from the body for a caller lacking commercial visibility `src: Technical requirements, are absent from the body, not null`
- [ ] `C-TR-84` `capability` Client principals see only sent proposals `src: Technical requirements, client principals see only proposals that were sent`
- [ ] `C-TR-85` `contract` Submitting a change order moves the order to client_review `src: Technical requirements, 200 with status client_review`
- [ ] `C-TR-86` `contract` A decision outside review answers 409 change_order_not_in_review `src: Technical requirements, 409 change_order_not_in_review when not in review`
- [ ] `C-TR-87` `role` A project manager deciding a change order answers 403 forbidden `src: Technical requirements, others are refused with 403 forbidden`
- [ ] `C-TR-88` `capability` The client owner decides change orders `src: Technical requirements, decided by the client's owner`
- [ ] `C-TR-89` `constraint` A rejected change order leaves the contract value `src: Technical requirements, the deltas of all its approved change orders`
- [ ] `C-TR-90` `contract` A created invoice is a draft with a null number `src: Technical requirements, status draft, number null`
- [ ] `C-TR-91` `constraint` Any total sent on invoice creation is ignored `src: Technical requirements, any total sent is ignored`
- [ ] `C-TR-92` `role` Drafts are issued by a finance admin of the client billing entity `src: Technical requirements, Drafts are created and issued by a finance_admin of the client's billing entity or a group_admin`
- [ ] `C-TR-93` `contract` Issuing first confirms the caller may issue for the entity `src: Technical requirements, the caller may issue for that entity (403 forbidden)`
- [ ] `C-TR-94` `contract` Issuing needs a step-up no older than 15 minutes `src: Technical requirements, a step-up no older than 15 minutes (403 step_up_required)`
- [ ] `C-TR-95` `contract` An invalid VAT number answers 422 vat_number_invalid `src: Technical requirements, 422 vat_number_invalid`
- [ ] `C-TR-96` `contract` A stale validation answers 422 vat_validation_stale `src: Technical requirements, 422 vat_validation_stale`
- [ ] `C-TR-97` `contract` A public_sector client lacking a PO answers 422 po_required `src: Technical requirements, a PO number for a public_sector client (422 po_required)`
- [ ] `C-TR-98` `contract` A credit note on an unissued invoice answers 409 invoice_not_issued `src: Technical requirements, (409 invoice_not_issued otherwise)`
- [ ] `C-TR-99` `contract` A credit note takes the next number of the credit-note sequence `src: Technical requirements, the next number of the entity's credit-note sequence`
- [ ] `C-TR-100` `contract` A credit note names the original in credits_invoice_id `src: Technical requirements, credits_invoice_id naming the original`
- [ ] `C-TR-101` `contract` A credit note negates the original lines `src: Technical requirements, the original's lines negated`
- [ ] `C-TR-102` `contract` A credit note negates the original totals `src: Technical requirements, the original's treatment, rate and totals negated`
- [ ] `C-TR-103` `capability` The credited original becomes void keeping the number `src: Technical requirements, the original becomes void and keeps its number`
- [ ] `C-TR-104` `capability` Issuing re-runs tax determination `src: Technical requirements, re-run tax determination and refuse on any unresolved condition`
- [ ] `C-TR-105` `constraint` A refused issue consumes no sequence value `src: Technical requirements, no sequence value is consumed`
- [ ] `C-TR-106` `constraint` Two issues never read the same next value `src: Technical requirements, so two issues never read the same next value`
- [ ] `C-TR-107` `contract` A Parallax France invoice number reads PXF- with year plus five digits `src: Technical requirements, invoices of Parallax France read PXF-2026-00001`
- [ ] `C-TR-108` `contract` A Parallax Malta invoice number reads PXM- with year plus five digits `src: Technical requirements, of Parallax Malta PXM-2026-00001`
- [ ] `C-TR-109` `contract` A France credit note number reads PXFC- with year plus five digits `src: Technical requirements, credit notes PXFC-2026-00001`
- [ ] `C-TR-110` `capability` Each entity, document type, year keeps a separate counter `src: Technical requirements, a five digit counter starting at 00001 for each entity, document type and year`
- [ ] `C-TR-111` `capability` Tax is rounded once, half away from zero, to a whole minor unit `src: Technical requirements, rounded once, half away from zero, to a whole minor unit`
- [ ] `C-TR-112` `capability` A line amount is the quantity times the unit price `src: Technical requirements, A line's amount is its quantity times its unit price in minor units`
- [ ] `C-TR-113` `capability` The France entity billing a French client applies domestic_fr at the 2000 basis-point rate `src: Technical requirements, domestic_fr | French standard, 2000 basis points | Standard French TVA`
- [ ] `C-TR-114` `capability` The Malta entity billing a Maltese client applies domestic_mt at the 1800 basis-point rate `src: Technical requirements, domestic_mt | Malta standard, 1800 basis points | Standard Maltese VAT`
- [ ] `C-TR-115` `capability` The Malta entity billing a valid EU business prints the Art. 196 reverse charge note `src: Technical requirements, Reverse charge - Art. 196 VAT Directive`
- [ ] `C-TR-116` `capability` A business outside the EU is billed export_outside_eu noted Outside scope `src: Technical requirements, export_outside_eu | 0 | Outside scope`
- [ ] `C-TR-117` `capability` A validation under 90 days old is used with the register unavailable `src: Technical requirements, the last successful validation is used if it is under 90 days old at the issue instant`
- [ ] `C-TR-118` `capability` A public_sector client uses the chorus_pro channel `src: Technical requirements, chorus_pro for a public_sector client`
- [ ] `C-TR-119` `capability` Another French business client of Parallax France uses pdp `src: Technical requirements, for any other French business client of Parallax France`
- [ ] `C-TR-120` `capability` Every other client uses the channel none `src: Technical requirements, none otherwise`
- [ ] `C-TR-121` `contract` A grant lacking ends_at answers 422 grant_requires_expiry `src: Technical requirements, no ends_at is 422 grant_requires_expiry`
- [ ] `C-TR-122` `contract` An ends_at in the past answers 422 grant_ends_in_past `src: Technical requirements, an ends_at not in the future is 422 grant_ends_in_past`
- [ ] `C-TR-123` `contract` Revoking a grant answers 204 `src: Technical requirements, DELETE /api/grants/{id} | none | 204`
- [ ] `C-TR-124` `role` Grants are created by a group admin with step-up `src: Technical requirements, Grants are created by a group_admin, or by an account director over its own portfolio, with step-up`
- [ ] `C-TR-125` `capability` A contractor holding an unexpired project:read grant reads the project `src: Technical requirements, reads GET /api/projects/{id} for that project`
- [ ] `C-TR-126` `constraint` Once the grant ends the next contractor read answers 404 `src: Technical requirements, once the grant ends or is revoked, the very next read answers 404`
- [ ] `C-TR-127` `contract` The secret list returns metadata with no value `src: Technical requirements, never a value`
- [ ] `C-TR-128` `contract` A requested ttl above 240 answers 422 ttl_exceeds_limit `src: Technical requirements, 422 ttl_exceeds_limit above 240`
- [ ] `C-TR-129` `contract` A missing, closed or foreign ticket answers 422 open_ticket_required `src: Technical requirements, 422 open_ticket_required when the ticket is missing, not open, or belongs to another organisation than the secret`
- [ ] `C-TR-130` `contract` A requester approving the request answers 403 self_approval_forbidden `src: Technical requirements, 403 self_approval_forbidden for the requester`
- [ ] `C-TR-131` `contract` The same approver approving twice answers 409 second_approver_must_differ `src: Technical requirements, 409 second_approver_must_differ`
- [ ] `C-TR-132` `contract` An ineligible approver is refused `src: Technical requirements, 403 forbidden for an ineligible approver`
- [ ] `C-TR-133` `contract` A reveal answers the value with Cache-Control no-store `src: Technical requirements, with Cache-Control: no-store`
- [ ] `C-TR-134` `contract` A reveal naming a request for another secret answers 403 access_request_required `src: Technical requirements, (403 access_request_required)`
- [ ] `C-TR-135` `contract` A reveal on an unapproved request answers 409 request_not_approved `src: Technical requirements, it is approved (409 request_not_approved)`
- [ ] `C-TR-136` `contract` A used request answers 409 request_already_used `src: Technical requirements, (409 request_already_used)`
- [ ] `C-TR-137` `constraint` A refused reveal leaves the request unused `src: Technical requirements, A refused reveal leaves the request unused`
- [ ] `C-TR-138` `capability` A reveal appends a read entry before the value returns `src: Technical requirements, appends a read entry to the access log before the value is returned`
- [ ] `C-TR-139` `contract` Export answers 403 export_denied recorded in the access log `src: Technical requirements, 403 export_denied, recorded in the access log`
- [ ] `C-TR-140` `contract` The log verification call answers valid with broken_at `src: Technical requirements, 200 {"valid", "broken_at"}`
- [ ] `C-TR-141` `capability` broken_at names the first sequence whose stored hash no longer matches `src: Technical requirements, the first sequence whose stored hash no longer matches`
- [ ] `C-TR-142` `capability` Log sequences start at 1 in one chain for the vault `src: Technical requirements, starting at 1, one chain for the whole vault`
- [ ] `C-TR-143` `capability` The first prev_hash is sixty four zeros `src: Technical requirements, sixty four zeros for the first`
- [ ] `C-TR-144` `capability` Each entry_hash is a SHA-256 hex digest `src: Technical requirements, the SHA-256 hex digest of`
- [ ] `C-TR-145` `constraint` No application connection updates a log row `src: Technical requirements, No connection the application holds can update or delete a log row`
- [ ] `C-TR-146` `constraint` No application connection deletes a log row `src: Technical requirements, No connection the application holds can update or delete a log row`
- [ ] `C-TR-147` `constraint` The vault tables hold no plaintext `src: Technical requirements, the vault tables hold no plaintext and no unwrapped key`
- [ ] `C-TR-148` `role` A vault request is approved by the security officer or the organisation account director `src: Technical requirements, approved by the security_officer or by the account director of the secret's client organisation`
- [ ] `C-TR-149` `capability` A break-glass request awaits a second approver after the first approval `src: Technical requirements, awaiting_second_approver after its first approval`
- [ ] `C-TR-150` `capability` A normal request is approved after one approval `src: Technical requirements, A normal request is approved after one approval`
- [ ] `C-TR-151` `constraint` No call returns more than one secret `src: Technical requirements, No call returns more than one secret`
- [ ] `C-TR-152` `contract` A content entry lists localisations with slug, path, version `src: Technical requirements, with each localisation {"id", "site", "locale", "slug", "path", "version", "status"}`
- [ ] `C-TR-153` `contract` A stale localisation version answers 409 version_conflict with current_version `src: Technical requirements, 409 version_conflict with {"current_version"} when version is stale`
- [ ] `C-TR-154` `contract` An English case study path is the work path of the slug `src: Technical requirements, /work/{slug}/ on the English`
- [ ] `C-TR-155` `capability` A path that stops being a localisation path answers 301 to the new path `src: Technical requirements, answers 301 to the new path from then on`
- [ ] `C-TR-156` `contract` Every public page links an alternate for each sibling localisation `src: Technical requirements, for each sibling localisation of the same entry`
- [ ] `C-TR-157` `contract` The x-default alternate targets the English localisation `src: Technical requirements, pointing at the English one`
- [ ] `C-TR-158` `contract` Alternate addresses are absolute `src: Technical requirements, each href an absolute address on APP_PUBLIC_URL`
- [ ] `C-TR-159` `contract` A thin landing page carries meta robots noindex `src: Technical requirements, content="noindex">`
- [ ] `C-TR-160` `contract` An indexable page carries no noindex `src: Technical requirements, an indexable page carries no noindex`
- [ ] `C-TR-161` `contract` The sitemap lists every published indexable public page `src: Technical requirements, every published and indexable public page of both sites`
- [ ] `C-TR-162` `constraint` The sitemap lists nothing under the portal or api paths `src: Technical requirements, nothing under /portal or /api`
- [ ] `C-TR-163` `contract` robots.txt disallows the portal path `src: Technical requirements, disallows /portal and /api`
- [ ] `C-TR-164` `contract` robots.txt disallows the api path `src: Technical requirements, disallows /portal and /api`
- [ ] `C-TR-165` `contract` robots.txt names the sitemap in a Sitemap line `src: Technical requirements, names the sitemap in a Sitemap: line`
- [ ] `C-TR-166` `contract` Every public page links the favicon.ico icon `src: Technical requirements, <link rel="icon" href="/favicon.ico">`
- [ ] `C-TR-167` `contract` favicon.ico answers 200 with an image content type `src: Technical requirements, answers 200 with an image content type`
- [ ] `C-TR-168` `contract` Every English page footer links the privacy page `src: Technical requirements, Every English page's footer links /privacy/`
- [ ] `C-TR-169` `contract` Every French page footer links the confidentialite page `src: Technical requirements, every French page's footer links /fr/confidentialite/`
- [ ] `C-TR-170` `contract` The English privacy page heading is Privacy policy `src: Technical requirements, the English privacy page's h1 is Privacy policy`
- [ ] `C-TR-171` `contract` The French privacy page heading is Politique de confidentialité `src: Technical requirements, the French one's is Politique de confidentialité`
- [ ] `C-TR-172` `ui` The French privacy page reached from the footer is headed Politique de confidentialité `src: Technical requirements, the French one's is Politique de confidentialité`
- [ ] `C-TR-173` `capability` The privacy page says how long lead records are kept `src: Technical requirements, states what Parallax records about visitors, leads and applicants and how long it keeps each`
- [ ] `C-TR-174` `contract` A legacy project address answers 301 to the work address `src: Technical requirements, /project/{slug}/ to /work/{slug}/`
- [ ] `C-TR-175` `contract` The legacy projects index answers 301 to the work index `src: Technical requirements, /projects/ to /work/`
- [ ] `C-TR-176` `contract` The legacy services address answers 301 to the services address `src: Technical requirements, /our-services/ to /services/`
- [ ] `C-TR-177` `contract` The legacy about address answers 301 to the about address `src: Technical requirements, /about-us/ to /about/`
- [ ] `C-TR-178` `contract` The legacy contact address answers 301 to the contact address `src: Technical requirements, /contact-us/ to /contact/`
- [ ] `C-TR-179` `contract` The legacy legal address answers 301 to the legal address `src: Technical requirements, /legal-mentions/ to /legal/`
- [ ] `C-TR-180` `contract` The legacy privacy address answers 301 to the privacy address `src: Technical requirements, /privacy-policy/ to /privacy/`
- [ ] `C-TR-181` `constraint` No served script carries a vault secret value `src: Technical requirements, No served document, script or style anywhere carries a vault secret's value`
- [ ] `C-TR-182` `constraint` No served document carries the identity provider client secret `src: Technical requirements, the identity provider client secret`
- [ ] `C-TR-183` `constraint` No served document carries a database credential `src: Technical requirements, a database credential`
- [ ] `C-TR-184` `capability` A spam lead receives no confirmation `src: Technical requirements, and sends nothing`
- [ ] `C-TR-185` `contract` Errors are problem documents carrying a machine code `src: Technical requirements, application/problem+json with type, title, status, detail, code`
- [ ] `C-TR-186` `contract` Field names are snake_case `src: Technical requirements, snake_case in every request, response, row and event`
- [ ] `C-TR-187` `contract` List calls answer a top-level JSON array `src: Technical requirements, Every list call below answers a top-level JSON array`
- [ ] `C-TR-188` `contract` Money fields are integer euro cents `src: Technical requirements, integer amount_minor fields in euro cents`
- [ ] `C-TR-189` `capability` Keycloak holds every principal credential in the parallax realm `src: Technical requirements, the identity provider holding every principal's credentials, realm parallax`
- [ ] `C-TR-190` `capability` Every message Parallax sends goes to Mailpit `src: Technical requirements, every message Parallax sends goes here`
- [ ] `C-TR-191` `literal` Seeded principals sign in to the Keycloak realm `parallax` `src: Technical requirements, realm parallax`
- [ ] `C-TR-192` `capability` Every public route renders as a complete HTML document on the server `src: Technical requirements, rendered on the server as a complete HTML document, readable without any script`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded principal uses the password `deku-demo-pw-2026` `src: Data model, uses the password deku-demo-pw-2026`
- [ ] `C-DM-02` `data` The vault_access_log table carries sequence with principal_email `src: Data model, one row per access: sequence, secret_id`
- [ ] `C-DM-03` `constraint` Invariant CO-1 holds at every instant `src: Data model, Invariant CO-1. A contract's value_minor always equals its original_value_minor plus the sum of its`
- [ ] `C-DM-04` `data` Contracts carry value_minor beside original_value_minor `src: Data model, value_minor (the current value including approved change orders), original_value_minor`
- [ ] `C-DM-05` `constraint` Invariant FIN-1 keeps issued numbers gapless `src: Data model, Invariant FIN-1, gapless numbering.`
- [ ] `C-DM-06` `constraint` An assigned number is immutable with corrections made by credit notes `src: Data model, once assigned it is immutable and corrections are credit notes`
- [ ] `C-DM-07` `constraint` Invariant FIN-2 refuses a second invoice for one milestone `src: Data model, Invariant FIN-2, no double billing.`
- [ ] `C-DM-08` `constraint` A number is unique per entity per document type among issued rows `src: Data model, A number is unique per entity and document type among issued rows`
- [ ] `C-DM-09` `data` An invoice number stays empty until issued `src: Data model, empty until issued, assigned once and never reused`
- [ ] `C-DM-10` `data` Each issued number is assigned once, never reused `src: Data model, empty until issued, assigned once and never reused`
- [ ] `C-DM-11` `data` Every sequence is unique per entity, document type, year `src: Data model, unique per entity, document type and year`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Near-black neutral is the page ground `src: Front-end specification, the page ground, the most declared value`
- [ ] `C-FE-02` `ui` The muted foreground stays off portal body text `src: Front-end specification, must never be used for portal body text`
- [ ] `C-FE-03` `ui` The mid vivid red is the single high-chroma accent `src: Front-end specification, the single high-chroma accent`
- [ ] `C-FE-04` `ui` Semantic success, warning, information colours appear in the portal `src: Front-end specification, The semantic colours`
- [ ] `C-FE-05` `ui` display-xl scales from 40px to 112px in MargoBeuys `src: Front-end specification, | display-xl | 40px | 112px | 0.95 | display, MargoBeuys |`
- [ ] `C-FE-06` `ui` body-m scales from 15px to 16px in Poppins `src: Front-end specification, | body-m | 15px | 16px | 1.6 | body, Poppins |`
- [ ] `C-FE-07` `ui` body-l scales from 16px to 18px in Poppins `src: Front-end specification, | body-l | 16px | 18px | 1.6 | body, Poppins |`
- [ ] `C-FE-08` `ui` Aligned figures in tables use tabular digits `src: Front-end specification, Aligned figures in tables, counters and totals use tabular digits`
- [ ] `C-FE-09` `ui` Every animation uses the one curve with a duration band `src: Front-end specification, Every animation uses that curve and one of the four duration bands`
- [ ] `C-FE-10` `ui` reveal-up rises a short distance with a fade `src: Front-end specification, fades in while rising a short distance`
- [ ] `C-FE-11` `ui` A reduced motion preference disables the smooth-scroll layer `src: Front-end specification, a reduced motion preference disables the smooth-scroll layer entirely`
- [ ] `C-FE-12` `ui` Only transform with opacity animate `src: Front-end specification, only transform and opacity animate`
- [ ] `C-FE-13` `ui` The pinned gallery uses no pin below 768px `src: Front-end specification, uses no pin below 768px`
- [ ] `C-FE-14` `constraint` A skip link precedes the pinned project gallery `src: Front-end specification, Skip visual gallery - view all projects as a list link`
- [ ] `C-FE-15` `constraint` WebGL imagery also exists as real images carrying alt text `src: Front-end specification, also exists as a real <img> with alt`
- [ ] `C-FE-16` `ui` The home page heading reads the measured intro line `src: Front-end specification, The agency that covers your digital needs in a creative and efficient way`
- [ ] `C-FE-17` `ui` The project gallery sections carry the heading Our projects `src: Front-end specification, h2 Our projects, seventeen case studies`
- [ ] `C-FE-18` `ui` The partner logo sections carry the trust heading `src: Front-end specification, h2 They trust us, sixteen client logos`
- [ ] `C-FE-19` `ui` The Verdane case study shows the client description `src: Front-end specification, a one-line client description`
- [ ] `C-FE-20` `ui` The case study shows a list of service tags `src: Front-end specification, a service tag list`
- [ ] `C-FE-21` `ui` The case study carries a See live link `src: Front-end specification, a See live outbound link`
- [ ] `C-FE-22` `ui` The Verdane case study carries a next project link to Hello Marlo `src: Front-end specification, measured as Hello Marlo`
- [ ] `C-FE-23` `ui` The language switcher lands on the equivalent page `src: Front-end specification, a language switcher that maps to the equivalent page on the`
- [ ] `C-FE-24` `ui` The brief wizard on start-a-project displays Step 1 of 6 `src: Front-end specification, a visible Step n of m`
- [ ] `C-FE-25` `ui` The start-a-project page carries a heading `src: Front-end specification, get an h1 and a heading per step`
- [ ] `C-FE-26` `ui` The email error reads Oops, e-mail is not valid. `src: Front-end specification, the email error copy Oops, e-mail is not valid.`
- [ ] `C-FE-27` `ui` The budget choices carry the corrected labels `src: Front-end specification, labels 10K-20K, 20K-30K, 30K-60K, +60K`
- [ ] `C-FE-28` `ui` The portal overview first block is titled Needs you `src: Front-end specification, Its first block is Needs you`
- [ ] `C-FE-29` `ui` Each listed invoice shows a due date `src: Front-end specification, show status, due date`
- [ ] `C-FE-30` `ui` The invoice page states the tax treatment in words `src: Front-end specification, the tax treatment in plain language`
- [ ] `C-FE-31` `ui` The invoice page offers a Dispute action `src: Front-end specification, a Dispute action opens a ticket`
- [ ] `C-FE-32` `ui` A client invoice list shows each listed invoice with its status `src: Front-end specification, Invoices show status`
- [ ] `C-FE-33` `ui` The sites page has only the organisation managed sites listed `src: Front-end specification, show, per managed site`
- [ ] `C-FE-34` `ui` The sites page shows an uptime strip with a TLS expiry countdown `src: Front-end specification, a TLS expiry countdown`
- [ ] `C-FE-35` `ui` Only the organisation tickets are listed on the tickets page `src: Front-end specification, list, create, thread, with SLA state visible`
- [ ] `C-FE-36` `ui` Organisation settings list the users for the client owner `src: Front-end specification, users, roles, approval routing, SSO and SCIM configuration, for the client_owner only`
- [ ] `C-FE-37` `ui` Organisation settings for a client approver say Not found, or you do not have access `src: Front-end specification, the interface says Not found, or you do not have access`
- [ ] `C-FE-38` `ui` The documents page lists the organisation contract `src: Front-end specification, contracts, change orders, signed PDFs, DPA, sub-processor register`
- [ ] `C-FE-39` `ui` Only the organisation projects are listed on the projects page `src: Front-end specification, list with a card and table toggle, filtered by status`
- [ ] `C-FE-40` `ui` The agency day view renders in the back office `src: Front-end specification, today: my tasks, my approvals, leads awaiting first response`
- [ ] `C-FE-41` `ui` The invoicing screen shows the queue of draft invoices `src: Front-end specification, the draft queue, issue runs, dunning, payment allocation`
- [ ] `C-FE-42` `ui` The vault screen lists secrets by label with no value shown `src: Front-end specification, The vault screen never shows a secret in a list.`
- [ ] `C-FE-43` `ui` The vault screen shows each secret type with a rotation status `src: Front-end specification, It lists labels, types, rotation status and last access`
- [ ] `C-FE-44` `ui` The vault screen states that access to secrets is recorded `src: Front-end specification, the screen states permanently that access is recorded`
- [ ] `C-FE-45` `ui` Every vault opening starts as a request `src: Front-end specification, every opening is a request flow`
- [ ] `C-FE-46` `ui` The vault screen offers no export of every secret at once `src: Front-end specification, no bulk export path`
- [ ] `C-FE-47` `ui` Approval confirmation states the invoice released with the amount `src: Front-end specification, Approving this releases invoice for`
- [ ] `C-FE-48` `ui` The approval bar shows who else must approve with the order `src: Front-end specification, an approval bar showing who else must approve and in what order`
- [ ] `C-FE-49` `ui` Data grids keep sticky headers `src: Front-end specification, sticky headers`
- [ ] `C-FE-50` `ui` Grids scroll horizontally inside their own container `src: Front-end specification, horizontal scroll inside their own container`
- [ ] `C-FE-51` `ui` Loading skeletons match the final layout dimensions `src: Front-end specification, skeletons matching the final layout's dimensions`
- [ ] `C-FE-52` `ui` Empty states distinguish nothing yet from nothing matches `src: Front-end specification, distinguishes nothing yet from nothing matches`
- [ ] `C-FE-53` `ui` Error states carry the request_id `src: Front-end specification, carries the request_id so support can find it`
- [ ] `C-FE-54` `ui` Focus rings reach 3:1 against the background `src: Front-end specification, at least 3:1 against its background, never removed`
- [ ] `C-FE-55` `constraint` Skip-to-content is the first focusable element on every route `src: Front-end specification, skip-to-content as the first focusable element on every route`
- [ ] `C-FE-56` `ui` A modal closes on Escape `src: Front-end specification, a focus trap, Escape closes, focus returns to the trigger`
- [ ] `C-FE-57` `ui` Below 768px the portal stacks cards with the primary action in a sticky bottom bar `src: Front-end specification, the primary action in a sticky bottom bar`
- [ ] `C-FE-58` `ui` Counters render final values under reduced motion `src: Front-end specification, render their final values immediately under reduced motion`
- [ ] `C-FE-59` `ui` A consent banner offers a reject all choice on the first screen `src: Front-end specification, declining is one click from the first screen`
- [ ] `C-FE-60` `ui` A footer link reopens consent preferences after the banner closes `src: Front-end specification, a persistent footer link on both sites`
- [ ] `C-FE-61` `constraint` The budget choices carry labels matching the submitted bands `src: Front-end specification, so the submitted identifier never disagrees with the label`
- [ ] `C-FE-62` `constraint` Concurrent issues across entities produce contiguous numbers `src: Front-end specification, concurrent issues across both entities produce 50 contiguous numbers`
- [ ] `C-FE-63` `constraint` A reverse charge cannot be applied on an invalid VAT number `src: Front-end specification, a reverse charge cannot be applied on an invalid VAT number`
- [ ] `C-FE-64` `constraint` A VIES timeout blocks issue unless a validation under 90 days old exists `src: Front-end specification, a VIES timeout blocks issue unless a validation under 90 days old exists`
- [ ] `C-FE-65` `constraint` The uploader of a version cannot approve the version `src: Front-end specification, the uploader of a version cannot approve it`
- [ ] `C-FE-66` `capability` A pending approval is cancelled when a new version lands `src: Front-end specification, is cancelled with a stated reason when a new version lands`
- [ ] `C-FE-67` `constraint` Changing a slug creates a 301 never a 404 `src: Front-end specification, changing a slug creates a 301 and never a 404`
- [ ] `C-FE-68` `constraint` Concurrent content edits conflict rather than overwrite `src: Front-end specification, concurrent edits conflict rather than overwrite`
- [ ] `C-FE-69` `constraint` A page below the uniqueness threshold is noindex `src: Front-end specification, below the uniqueness threshold is noindex`
- [ ] `C-FE-70` `constraint` The sitemap never contains a noindex page `src: Front-end specification, the sitemap never contains a noindex page`
- [ ] `C-FE-71` `constraint` A full database dump yields no plaintext secret `src: Front-end specification, yields no plaintext`
- [ ] `C-FE-72` `constraint` A break-glass request lacking a second approver is refused a reveal `src: Front-end specification, a break-glass request with no available second approver is denied and recorded`
- [ ] `C-FE-73` `constraint` A contractor whose grant expires mid-session is denied at the next decision `src: Front-end specification, a contractor whose grant expires mid-session is denied at the next decision`
- [ ] `C-FE-74` `constraint` A public-sector invoice cannot be issued lacking a PO `src: Front-end specification, a public-sector invoice cannot be issued without a PO`
- [ ] `C-FE-75` `constraint` Invoice numbers per entity, document type, year form a contiguous set `src: Front-end specification, invoice numbers per entity, document type and year form a contiguous set with no duplicates`
- [ ] `C-FE-76` `constraint` Every contract value equals the original value plus approved change orders `src: Front-end specification, every contract's value equals its original value plus its approved change orders`
- [ ] `C-FE-77` `constraint` No grant is active past the expiry `src: Front-end specification, no grant is active past its expiry`
- [ ] `C-FE-78` `constraint` Modifying a historical access log row is detected `src: Front-end specification, modifying any historical row is detected by J-16`
- [ ] `C-FE-79` `constraint` Every published localisation has a consistent hreflang sibling set `src: Front-end specification, has an hreflang sibling set consistent with its entry`
- [ ] `C-FE-80` `constraint` Every historical published path resolves with 200 or 301 `src: Front-end specification, every historical published path resolves with 200 or 301`
- [ ] `C-FE-81` `constraint` Legacy addresses are seeded as aliases with permanent redirects `src: Front-end specification, seeded as an alias with a permanent redirect to its new home`
- [ ] `C-FE-82` `constraint` A public address lacking the trailing slash answers 301 to the slashed form `src: Front-end specification, without its trailing slash answers 301 to the slashed form`
- [ ] `C-FE-83` `capability` No gclid is stored with marketing consent declined `src: Front-end specification, with marketing consent declined, no gclid is stored`
- [ ] `C-FE-84` `capability` Organisation A receives 404 for every organisation B resource `src: Front-end specification, organisation A receives 404`
- [ ] `C-FE-85` `constraint` A revoked grant is denied on the next request despite the cache `src: Front-end specification, a revoked grant is denied on the next request despite the cache`
- [ ] `C-FE-86` `capability` Replaying milestone approval produces one draft unique on milestone_id `src: Front-end specification, produces one draft, unique on milestone_id`
- [ ] `C-FE-87` `constraint` No code path returns more than one secret per request `src: Front-end specification, no code path returns more than one secret per request`
- [ ] `C-FE-88` `constraint` A vault reveal lacking a recent step-up is refused `src: Front-end specification, minutes is refused for vault and finance actions`
- [ ] `C-FE-89` `ui` The public site reads spacious beside a visibly denser portal `src: Front-end specification, the public site's job is motion and impression, the portal's job is density and legibility`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No row of a client organisation is readable by another client organisation `src: Constraints, no row of a client organisation is ever readable by another client`
- [ ] `C-CN-02` `constraint` A contractor reads only what an unexpired grant names `src: Constraints, a contractor reads only what an unexpired grant names`
- [ ] `C-CN-03` `ui` A contractor holding no grant sees no project listed `src: Constraints, a contractor reads only`
- [ ] `C-CN-04` `constraint` Signup is closed `src: Constraints, Signup is closed`
- [ ] `C-CN-05` `constraint` Issued invoices only ever grow `src: Constraints, Issued invoices, the vault access log and the audit log only ever grow`
- [ ] `C-CN-06` `constraint` The vault access log only ever grows `src: Constraints, Issued invoices, the vault access log and the audit log only ever grow`
- [ ] `C-CN-07` `constraint` Money is integer minor units in `EUR` `src: Constraints, Money is integer minor units in EUR`

## C-DC Deployment contract

- [ ] `C-DC-01` `capability` The app is reachable at APP_PUBLIC_URL `src: Deployment contract, The app must be reachable at APP_PUBLIC_URL`
- [ ] `C-DC-02` `capability` The HTTP API is served on the same origin under the api prefix `src: Deployment contract, The HTTP API is served on that same origin under the /api prefix`
- [ ] `C-DC-03` `capability` Every seeded principal shares one password `src: Deployment contract, they all share one password`
- [ ] `C-DC-04` `capability` Keycloak holds every principal credential `src: Deployment contract, Keycloak holds every principal's credentials`
- [ ] `C-DC-05` `capability` Mailpit receives every message `src: Deployment contract, Mailpit receives every message`
- [ ] `C-DC-06` `constraint` An email kept out of SMTP delivery counts as unsent `src: Deployment contract, instead of sent over SMTP does not count`
- [ ] `C-DC-07` `constraint` The listener is reachable from outside the container `src: Deployment contract, A loopback-only listener is unreachable from outside the container`
- [ ] `C-DC-08` `capability` The server keeps running after the session ends `src: Deployment contract, The server must keep running after this session ends`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `parallax` | the Keycloak realm | C-TR-191 | Technical requirements, the stack |
| `deku-demo-pw-2026` | the password of every seeded principal | C-DM-01 | Data model, opening paragraph |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 6 |
| User roles | 1 | 20 |
| Core features | 3 | 37 |
| User flow | 2 | 20 |
| UI and UX notes | 2 | 28 |
| Technical requirements | 111 | 192 |
| Data model | 11 | 11 |
| Front-end specification | 67 | 89 |
| Constraints | 1 | 7 |
| Deployment contract | 6 | 8 |

The obligation-bearing sentence counts above are the machine recount of each instruction section. Every
section yields at least as many items as that recount, and every item is paired to a grading channel.
`## Definition of done` restates the core outcome and the hardest guarantee already itemised above, so it
carries no separate items.

- Declared but ungraded: `/app/USER_README.md` carrying every seeded address, the reserved
  `.browser_screenshots/` and `.downloads/` directories, the production build behind a static or preview
  server, `GET /api/health`, no edge functions, and no persistent volumes, fixed container names or
  custom networks are Deployment contract obligations no separately running grader can observe.
- Declared but ungraded, window sections: the product being no marketplace and hosting no client
  websites; the group admin row and the client viewer row, which no seeded principal or pinned call
  exercises; the second journey's queue behaviour after issue, since no draft exists when the browser
  walk runs; the offline state, which needs a network failure no outside request can induce; and the
  Constraints lines on checkout, marketplace, hosting, design tool, payroll, partner portal, public API,
  native application, backing services, outbound hosts, instant zones, opaque identifiers and the
  responsiveness volume, none of which has a pinned observable.
- Declared but ungraded, unbudgeted sections: the reference architecture, integrations, background jobs,
  observability, compliance programme, delivery phases, assumptions and evidence log are carried from the
  companion in full so the build is specified completely; the items above are their observable subset.
