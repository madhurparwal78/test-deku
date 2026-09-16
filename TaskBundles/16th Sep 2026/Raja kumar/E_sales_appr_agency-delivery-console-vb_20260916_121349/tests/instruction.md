# Parallax

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a client approver at Aeroline can open a shared
deliverable in the portal, annotate its current version and approve it, and that
approval closes the milestone and releases exactly one draft invoice, which
finance issues under the next gapless number of the right legal entity; the
person who uploaded the version can never be the one who approves it.

That sentence is the product. An approval the app shows itself does not count: a
milestone is approved only when every stage of its client's policy has been
decided by someone entitled at that moment, and an invoice number exists only
once it is issued and never goes missing or repeats.

## Overview

Parallax is an operating system for a creative digital agency with offices in
Malta, Lyon and Paris, two legal entities under two VAT regimes, and around four
hundred client businesses whose production credentials it holds. Parallax OS
runs the whole lifecycle: anonymous visitor, lead, proposal, signed contract,
project, approved deliverable, issued invoice and retained monitoring.

You are building three surfaces on one origin: the public site in English and
French, the client portal under `/portal`, and the agency back office under
`/portal/agency`. The hard part is money and access: approvals release invoices,
numbers must stay gapless, and no one holds standing access to a client secret.
Parallax is not a marketplace, has no self-serve signup, and does not host client
websites.

## User roles

Sixteen roles in three families, each held through a membership or a grant.

| Role | Holds | Never |
|---|---|---|
| group admin | every action across both entities | reads a secret without a second approver |
| finance admin | invoices, credit notes, payments for its entity | approves deliverables, opens the vault |
| account director | its portfolio, rates, margin, approvals | issues invoices |
| project manager | projects, milestones, deliverables, content | cost or margin without a grant |
| producer | tasks, time, deliverable versions | financial fields, standing credentials |
| analyst | reads delivery and performance data | writes outside reports |
| recruiter | applicants | client data |
| security officer | vault policy, second approvals, audit export | approves its own break-glass |
| client owner | its whole organisation, final approver | another organisation |
| client approver | approvals within its threshold | anything above its threshold |
| client collaborator | comments, annotations, tickets | approving |
| client finance | invoices and billing documents | deliverables |
| client viewer | a named project subset | writes |
| contractor, partner PM, auditor | exactly what an expiring grant names | anything unexpired grants do not name |

A role counts only in the scope it is held in. Authorization is enforced **server-side on every
mutating endpoint**. Hiding a button in the UI is not authorization: a direct
API call from a project manager session to any finance admin-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving
the protected state unchanged.

## Core features

1. **Invoice numbers are gapless per entity.** Numbers for one entity, document
   type and year form a contiguous run with no gap and no repeat, however many
   issues arrive at once; an issue refused for any reason takes no number.
2. **Reverse charge needs a validated VAT number.** An invalid number, or a
   validation older than ninety days while the register is unreachable, refuses
   the issue with the reason and leaves the draft untouched.
3. **The uploader never approves.** Whoever uploaded the version under review is
   refused a decision on it, and the approval is unchanged.
4. **A new version supersedes.** Uploading while an approval is pending cancels
   it, and a decision on the old version is refused naming the new one.
5. **Stages complete by their rule.** A milestone is approved only when every
   stage is complete, and completion creates exactly one draft invoice.
6. **Thresholds bind.** An approver whose threshold is below the value is refused.
7. **Contract value stays reconciled.** A contract is always its original value
   plus every approved change order, however many are approved at once.
8. **Denied reads look missing.** Another organisation's record answers exactly as
   a record that does not exist, and cost and margin are absent, not empty, for
   anyone without commercial visibility.
9. **No standing access to secrets.** A reveal needs an approved request bound to
   an open ticket, a recent step-up, and is single use; break-glass needs two
   different approvers, and every access is logged in a chain nothing rewrites.
10. **Grants expire when they say.** A grant without an end is refused, and an
    expired or revoked grant is denied on the very next request.
11. **Leads arrive once.** A replayed submission creates one lead and one
    confirmation email from the entity that will handle it; a bot trap is stored
    silently as spam, invalid fields are refused by name, and no gclid is kept
    without marketing consent.
12. **The public site keeps its addresses.** A changed or legacy address redirects
    permanently, language alternates are derived, thin landing pages stay out of
    the sitemap, a privacy page and favicon are served, and no secret reaches the
    browser.

## User flow

| Route | Purpose |
|---|---|
| `/`, `/work/`, `/services/`, `/start-a-project/`, `/privacy/` and the rest of the English site | public, English |
| `/fr/`, `/fr/references/`, `/fr/devis/`, `/fr/confidentialite/` and the rest of the French site | public, French |
| `/portal/login` | sign in for every principal |
| `/portal` | the Needs you queue |
| `/portal/deliverables/{id}` | viewer, comment rail and approval bar in one split pane |
| `/portal/approvals`, `/portal/invoices`, `/portal/tickets` | client work lists |
| `/portal/agency` | the agency day view |
| `/portal/agency/invoicing`, `/portal/agency/vault` | finance and custody |

**Entry.** Every portal route needs a session; an unauthenticated visit renders
the sign in panel in place and never serves data. A sidebar holds every section.

**Journeys.**
1. `brand1@aeroline.example.com` opens a shared deliverable, annotates a point,
   approves the version; a toast confirms and the approval bar shows who is next.
2. `finance.fr@parallax.example.com` opens invoicing, steps up, issues a draft;
   the number appears and the draft leaves the queue.
3. `dev.fr@parallax.example.com` requests a secret from the vault in a slide-over
   bound to an open ticket; after approval and step-up it is revealed once.
4. A visitor completes the six step brief on `/start-a-project/` and sees the
   reference and expected response time.

**States.** Every view has loading shaped like its content, empty with the reason,
error with the request identifier, offline with staleness, and permission denied
as not found.

## UI/UX notes

Dark-first and editorial: near-black neutral grounds with a one step darker
recess and a near-black raised surface, near-white neutral type, deep neutral
hairlines and muted type, a mid neutral tertiary, and one mid, vivid red accent
spent on primary actions, focus and danger. A light, muted orange is an
editorial secondary only. The portal adds a mid, vivid teal for success, a mid,
vivid orange for warning and a light, vivid blue for information, each always
with a word and a shape. There is no light theme.

Type is `MargoBeuys` for display headings, from `40px` to `112px`, and `Poppins`
for everything else, body from `15px` to `18px`; aligned figures use tabular
digits. The public site is spacious, scroll-driven and motion-rich; the portal is
dense and legible. All motion shares one curve that leaves fast and settles long,
and only moves and fades; a reduced motion preference turns entrances into a
short fade, removes smooth scrolling entirely, and keeps hover and focus feedback.
The portal is a sidebar beside a split detail pane; creation opens in a
slide-over and a toast confirms a completed write. Cards and sheets are flat raised surfaces
edged by hairlines, and primary buttons answer hover with a masked label swap.

Inputs show errors beneath them in the measured words, overlays close on Escape
and return focus, and money-moving or destructive actions ask for typed
confirmation naming the object. Text meets WCAG 2.2 AA contrast, every control
has a visible focus ring, targets are comfortable to touch, icon-only controls
carry labels, colour never carries meaning alone, and each breakpoint changes
structure, never size.

## Technical requirements

### The stack, and what is already running

Build Parallax with **server-rendered pages and islands**. The server is **Express** on Node.js 20,
running beside the image's Python 3.12. The browser half is **SolidStart**: every public route of both
language sites is rendered on the server as a complete HTML document, readable without any script, and
only interactive parts hydrate as islands; the portal and back office are SolidStart routes behind a
session. One process serves the production build of the pages, the documents the server owes on its
own (redirects, the sitemap, `robots.txt`, the favicon), and the HTTP API on the same origin under the
`/api` prefix.

Three backing services are **already running** and reachable at their environment variables. Do not
download, install, compile or start a copy of any of them.

| Service | Read from | What it is for |
|---|---|---|
| PostgreSQL | `DATABASE_URL` (the same value is also in `DB_URL`) | every durable row in this brief, the vault included |
| Keycloak | `AUTH_URL` and `AUTH_ISSUER_URL`, which carry the same issuer, with `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET` | the identity provider holding every principal's credentials, realm `parallax` |
| Mailpit | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`, the last two empty because the server takes no authentication | real SMTP; every message Parallax sends goes here |

`APP_PUBLIC_URL` and `APP_PUBLIC_PORT` are read from the environment and never hardcoded; every absolute
address Parallax emits (canonicals, language alternates, sitemap entries, links in email) is built on
`APP_PUBLIC_URL`. Do not introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are PostgreSQL, Keycloak and
Mailpit. Anything this brief calls a cache, a queue, an event bus, an outbox, a search index, a time
series store, a vault cluster or an object store is PostgreSQL tables here, and anything it calls a
payment rail, an e-signature provider, an e-invoicing platform, a VAT register, an analytics connector,
a probe network, a chat workspace or a consent platform is represented by its records, its inbound
webhook endpoints and its stated states, never by a network call: Parallax makes no outbound call to
any host other than the three services above.

### Placeholder identity

The reference measured a real agency. Every name below replaces one, and the replacement is the name
you use everywhere, in copy, seeds, addresses and email.

| Stands for | Use |
|---|---|
| the agency and its wordmark | `Parallax`, and the system `Parallax OS` |
| the group entity in Malta, issuing for the English site | `Parallax Malta Ltd`, slug `parallax-malta`, country `MT` |
| the entity in France, issuing for the French site | `Parallax France SAS`, slug `parallax-france`, country `FR` |
| the English and French public domains | the English site at `/` and the French site under `/fr/` on this one origin |
| the portal and API hosts | `/portal` and `/api` on this one origin |
| the published contact addresses | `contact@parallax.example.com` for Malta, `contact@parallax-france.example.com` for France |
| the theme folder name | `parallax` |
| the listed and large clients | `Aeroline`, `Banque Horizon`, `Pharmalis`, `Enerva`, `Verrier Group` |
| the public and para-public buyers | `Institut Lumiere`, `Laboratoire Nova`, `Centre Lumen` |
| the logo wall under `They trust us`, in order | `Caffe Moreno`, `Slice House`, `Toolyard`, `Autonav`, `Eventia`, `Aeroline`, `Pharmalis`, `Railbite`, `Olympique Rhone`, `Verrier Group`, `Banque Horizon`, `Kinfolk Print`, `Institut Lumiere`, `Laboratoire Nova`, `Enerva`, `Verdane` |
| the award-recognised work | `Lyon Junior Conseil`, `Maison Interieur`, `Squadron Toulouse`, `Lead Digital`, `Petit Atelier`, `Centre Lumen`, `Arcwood` |
| the outdoor furniture client of the sampled case study | `Verdane`, described as `Verdane, a French brand of outdoor and indoor furniture with a trendy, colourful and sustainable design.` |
| the case study that exists on both sites | `Bellamy Associes` |
| the next project named after Verdane | `Hello Marlo` |

The design awards site, the regulators and the third-party tools keep their public names where this
brief states them as standards or integration kinds (VIES, Factur-X, Chorus Pro, SEPA, OpenID Connect,
SAML 2.0, SCIM 2.0, CNIL, GA4, Search Console, Google Ads, Meta, Consent Mode v2, Turnstile, Stripe,
Slack or Teams, GSAP, ScrollTrigger, OGL, Splitting.js), and none of them is called.

### What Parallax is, measured

Parallax is a creative digital agency founded in 2012, operating from three offices.

| Office | Phone | Address | Contact |
|---|---|---|---|
| Malta, headquarters and group entity | `+356 2200 0100` | Harbour Centre, Triq il-Wied Street, St Julian's, STJ 3154, Malta | `contact@parallax.example.com` |
| Lyon | `+33 4 72 00 01 00` | 24 avenue du Rhone 69009 Lyon, France | `contact@parallax-france.example.com` |
| Paris | `+33 1 89 00 01 00` | 207 rue de la Gare 75012 Paris, France | `contact@parallax-france.example.com` |

Self-reported scale on the About page counters: 20 awards won, 10 years of experience, 400 companies
that trust us, 20 employees worldwide, 5 languages spoken, 400+ digital projects, in business since 2012.
The service catalogue, verbatim and in order:

- `Tailor-made website`
- `Digital strategy`
- `UX & UI design`
- `Search Engine Advertising - SEA`
- `Social Media Ads & Management`
- `E-commerce website`
- `Art direction & brand identity`
- `Search Engine Optimisation - SEO`
- `CRM & Marketing Automation`

The French site adds two commercial lines absent from the English catalogue: replatforming and
migration engagements (`accompagnement-refonte-site-internet`) and GEO, generative engine optimisation,
alongside SEO in its blog and page titles.

### The commercial reality that drives the system

Six evidenced facts dictate the architecture.

- **The agency is a privileged-access holder for hundreds of other businesses.** For each client it
  designs, develops and manages, it holds CMS admin accounts, hosting and DNS control, ads accounts
  spending client money, GA4 and Search Console properties, CDN and registrar logins and deploy keys. A
  single compromise of the agency is a supply-chain compromise of 400 businesses, so credential custody
  is the highest-risk subsystem, not a feature.
- **Two legal entities, two tax regimes, one pipeline.** The English site bills from Malta and the
  French site bills from France, with one delivery team: per-entity gapless invoice sequences, Maltese
  VAT against French TVA, intra-EU B2B reverse charge with VIES validation, the French e-invoicing
  mandate (Factur-X structured invoices through a registered platform) and Chorus Pro for public-sector
  clients, who cannot receive a PDF by email and pay it.
- **The buyers are enterprise procurement, not founders.** Large clients route a homepage design through
  a named approver chain, demand their own SSO, send security questionnaires, require a DPA with a
  sub-processor register, and expect an audit trail of what was approved and when. Deliverable approval
  is a contractual event that releases a payment milestone, so it needs a workflow engine, not a boolean.
- **The public surface is two disconnected installs that duplicate each other.** Both sites ran one
  theme with different, partly overlapping case-study collections; `Bellamy Associes` exists on both at
  `/project/bellamy-associes/` and `/references/bellamy-associes/` with no `hreflang` annotation on either
  domain. The French site also runs a programmatic service by city landing matrix
  (`agence-{seo|sea|ux-design|content-marketing|webmarketing|digitale|web|web-site-internet}-{lyon|paris}`).
  For an agency whose product is SEO, cross-domain near-duplicate content with no canonical or hreflang
  signal is a credibility problem and the argument for one governed content model behind two sites.
- **Money and delivery are decoupled, and it hurts.** The six step `start-a-project` form collects a
  budget band and a project kind before a human reads the brief. The bands are `10K-20K`, `20K-30K`,
  `30K-60K` and a fourth whose submitted value was `+50K` while its label read `+60K`, a live defect
  mis-classifying the top of the funnel. Qualification data is typed domain values with one source of
  truth.
- **The agency is a GDPR processor and was non-compliant on its own site.** Both properties loaded tag
  infrastructure (`googletagmanager`, `gtag`) on first paint with no consent management platform, a
  breach of ePrivacy as transposed in France (CNIL) and Malta, and the easiest finding for a client's
  security reviewer. Beyond its own site, the agency processes client customer data through its CRM and
  marketing automation line, which makes it a processor with Article 28 obligations, a sub-processor
  register and data subject request duties that fan out across client systems.

### Product goal and success metrics

Run the agency's entire commercial and delivery lifecycle, anonymous visitor to signed contract to
approved deliverable to paid invoice to retained monitoring, on one governed system, where every access
to a client's production credentials is authorised and recorded, every approval that moves money is
attributable to a named principal, every invoice is jurisdiction-correct at the moment it is issued, and
every page on both public sites comes from one content model that cannot contradict itself across
languages.

| Metric | Target | Instrumented by |
|---|---|---|
| Qualified-lead rate, brief to sales-accepted | at least 40 per cent | the lead state machine |
| Brief to proposal sent, median | at most 3 business days | proposal timestamps |
| Proposal to signed contract | at least 25 per cent | the e-signature webhook |
| Deliverable approval cycle time, median | at most 4 business days | the approval engine |
| Milestone invoice drafted within 24 hours of approval | at least 98 per cent | the billing job J-11 |
| Invoice sequence gaps or duplicates | zero, a hard requirement | the numbering invariant |
| VAT treatment corrections after issue | at most 0.5 per cent of invoices | the credit-note ratio |
| Credential accesses without a linked authorisation record | zero, a hard requirement | the vault audit |
| Ex-staff or ex-contractor retaining any grant 24 hours after offboarding | zero, a hard requirement | access reconciliation J-04 |
| Cross-tenant data exposure incidents | zero, a hard requirement | row-level security and query-guard checks |
| Tags fired before consent, sampled weekly | zero, a hard requirement | the consent proof job J-17 |
| Retained-client SLA breach rate | at most 2 per cent of tickets | SLA timers |
| Client-site downtime detected before the client reports it | at least 95 per cent | the monitoring ingest |
| p75 LCP on public marketing routes over 4G | at most 2.5 seconds | real-user monitoring |
| Public site keyboard-operable end to end | 100 per cent, a hard requirement | axe and manual audit |
| DSR fulfilled within the statutory window | 100 per cent within 30 days | the DSR tracker |

Metrics six, eight, nine, ten, eleven and fifteen are hard requirements: a build failing any one of them
fails regardless of feature completeness.

### Tier classification

Parallax is an enterprise system: org-scale, distributed in responsibility and governed.

**Why not a browser-only tool.** The artefacts under management (contracts, invoices, credentials,
approvals) are legally consequential records that multiple principals in multiple organisations read and
write and that regulators and auditors read afterwards; no state lives in browser storage. The public
marketing surface alone would be a strong browser exercise (a WebGL-augmented, scroll-driven page with a
pinned project gallery and a six step form wizard), and that work is kept, folded into requirements that
also carry consent enforcement, content governance and accessibility, so no capability is pure rendering.

**Why not a single-tenant workspace with a payment rail.** Six things push past that line:

| Workspace assumption | Why it breaks here |
|---|---|
| One identity provider, users sign up | enterprise clients require their staff to reach the portal through their own IdP (Okta, Entra ID, Ping, Google Workspace) simultaneously, with domain ownership resolved and group claims honoured: multi-tenant federated identity, not a social login |
| Users belong to a workspace | the principals are agency staff across two entities, client stakeholders inside client org hierarchies, freelancers and subcontractors with time-bounded project-scoped grants, partner agencies on white-label work, and machine principals such as client sites posting monitoring beacons; delegation is routine |
| A row-level tenant filter is enough | authorisation is attribute-based: whether a principal may see the day rate on a line depends on org, role, the engagement's commercial model, white-label status and whether the viewer is the paying entity; scattered role checks leak margin data to the client |
| Stripe is the billing system | two issuing entities in two jurisdictions, gapless per-entity sequences, reverse-charge determination with VIES lookups, French structured e-invoicing through a mandated platform, public-sector routing via Chorus Pro, and credit notes that cannot renumber history; Stripe is a payment rail, not the ledger |
| An audit log is nice to have | the approval releasing a forty thousand euro milestone and the moment someone opened a client's production DNS credentials decide disputes; they are append-only, tamper-evident and queryable by actor, resource and time under a retention policy that differs by jurisdiction |
| The blast radius is one tenant's data | the blast radius is the production infrastructure of 400 client businesses, several of them listed multinationals |

**What the classification obliges**, as first-class subsystems:

- a real authorisation layer with a policy decision point, decision logs and deny by default;
- federated identity with SCIM lifecycle and just-in-time provisioning;
- immutable, hash-chained audit logging with WORM retention;
- approval workflows with delegation, parallel branches and timeout escalation;
- multi-jurisdiction tax and e-invoicing with per-entity sequence integrity;
- data governance: RoPA, sub-processor register, DSR fan-out, consent enforcement;
- distributed-system hygiene: outbox, idempotency keys, sagas across the billing and e-signature boundary,
  backpressure on the monitoring ingest path;
- per-org rate limits and quotas, including on the client-facing API.

**What is deliberately not escalated:**

- **Multi-region active-active.** All data stays in the EU; one primary region with a warm standby suits
  a 20-person agency, and a multi-region write topology would be architecture theatre.
- **Event sourcing of the whole domain.** Only credential access, approvals and the invoice lifecycle are
  event-sourced, because those have legal replay value.
- **A metadata-driven custom-field engine.** Clients do not extend the agency's schema: a fixed schema
  with a narrow, schema-validated extension point on four structures only.
- **Break-glass without a human.** Emergency credential access always requires a second named principal;
  there is no automated override path.

### Scope

**In scope:**

| Capability area | One-line definition |
|---|---|
| Public web presence | both sites rendered from one governed content model: home, services, case studies, editorial, the service by city landing matrix and legal pages, in English and French |
| Lead capture and qualification | the three measured forms rebuilt as one typed intake engine with anti-abuse, routing and a first-response SLA |
| CRM and pipeline | organisations, contacts, opportunities, activities, attribution to campaign and channel |
| Scoping and proposals | estimate builder, rate cards per entity and role, proposal document generation, versioning, e-signature |
| Contracts and change orders | the signed scope of record, the change-order workflow, the three-way reconciliation of contract, delivery and billing |
| Project delivery | projects, phases, milestones, tasks, assignments, capacity, time tracking, cost and margin |
| Deliverable review and approval | versioned deliverables, pin-anchored annotation, multi-stage client approval that releases milestones |
| Client portal | the client-facing surface for status, deliverables, approvals, documents, invoices, reports and tickets |
| Retained services | maintenance, SEO and SEA retainers, ticketing with SLA timers, monthly report generation |
| Client asset custody | encrypted credential vault, access authorisation, break-glass, session records, exit and handover |
| Finance | multi-entity invoicing, VAT determination, e-invoicing, payments, dunning, revenue recognition |
| Recruitment | the application funnel as a real applicant pipeline with retention limits |
| Identity and access | multi-IdP SSO, SCIM, the RBAC and ABAC policy layer, delegation, time-bounded grants |
| Governance | audit log, RoPA, DPAs, sub-processor register, consent enforcement, DSR handling, retention |
| Observability and reliability | tracing, metrics, SLOs, alerting, incident workflow |

**Out of scope:**

| Excluded | Why |
|---|---|
| Hosting the clients' websites | the agency manages sites on third-party hosting; Parallax holds credentials and monitors, it serves no client traffic |
| A design tool | Figma is the design surface; Parallax links to and versions exports and renders no editable design file |
| A general-purpose project management product | delivery modelling serves billing, approval and capacity; it is not sold and needs no swimlane Gantt tooling |
| Payroll and HR | recruitment stops at offer extended; employment records are out |
| A public marketplace or self-serve signup | every client relationship starts with a human sales conversation; there is no self-serve tier |
| Native mobile apps | responsive web only; the portal is used at a desk |
| Multi-region write topology | stated above |

**Explicitly deferred**, designed for but not built:

- a partner white-label portal for the reseller relationships implied by `Partnership` in the application
  form's type of job options;
- a client-facing public API, which the rate-limit design already anticipates;
- automated GEO and AI-visibility tracking as a product line, beyond content provenance;
- programmatic expansion of the service by city matrix beyond Lyon and Paris.

### System shape

Parallax is a modular monolith with three isolated responsibilities, chosen by isolation requirement:
the content renderer, the vault and the job runners.

- **The core** is one deployable with enforced module boundaries, because the hard problems are
  transactional consistency between contract, delivery and billing, which separate services make harder.
- **The vault** is isolated in responsibility: a bug in invoice rendering can never read a client's DNS
  password. Here it is a separate module with its own tables, its own authorisation check inside the
  module that does not trust the caller's assertion of identity, and no path from any other module's code
  to its ciphertext or its keys.
- **The content renderer** serves both public sites and survives core-API trouble: if the portal's
  business logic fails, a published page still renders.
- **Job runners** carry monitoring ingest and report generation, whose bursty profiles never contend with
  a request serving an approval.

| Module | Owns | Publishes |
|---|---|---|
| `identity` | principals, orgs, memberships, grants, sessions, IdP configs | `principal.*`, `grant.*` |
| `authz` | the policy bundle, the decision cache, the decision log | `authz.decision`, sampled |
| `crm` | leads, contacts, opportunities, activities, attribution | `lead.*`, `opportunity.*` |
| `commerce` | proposals, contracts, change orders, rate cards | `proposal.*`, `contract.*` |
| `delivery` | projects, phases, milestones, tasks, assignments, time | `project.*`, `milestone.*`, `time.*` |
| `review` | deliverables, versions, annotations, approvals | `deliverable.*`, `approval.*` |
| `retainers` | retainer contracts, tickets, SLA policies and timers | `ticket.*`, `sla.*` |
| `finance` | invoices, lines, tax determination, payments, credit notes, dunning | `invoice.*`, `payment.*` |
| `content` | editorial workflow state for both sites | `content.*` |
| `insights` | connectors, metric snapshots, report definitions and runs | `report.*` |
| `governance` | audit chain, RoPA, DSRs, consent records, retention jobs | `audit.*`, `dsr.*` |
| `notify` | notification preferences, channels, delivery attempts | `notification.*` |

A module reads another module's data only through that module's interface and never writes it; a
cross-module table reference is a defect, because this is the cheapest substitute for network boundaries
and survives the day `finance` needs extracting.

**Stores, as the reference designed them and as they live here:**

| Designed store | Contents | Here |
|---|---|---|
| PostgreSQL 16, primary and read replica | all transactional domain data, row-level security on every tenant-scoped table | PostgreSQL at `DATABASE_URL` |
| A separate PostgreSQL cluster | vault ciphertext and vault audit, no shared credentials with the core | vault tables in the same PostgreSQL, reachable only through the vault module |
| Redis | sessions, the policy decision cache with a short TTL, rate-limit counters, queue backing, idempotency keys | PostgreSQL tables with expiry columns |
| An S3-compatible object store in the EU | deliverable files, brief attachments, CVs, generated PDFs, report exports, versioned with object-lock on invoices | file metadata and bytes in PostgreSQL, invoice documents never rewritten |
| ClickHouse | site-monitoring beacons, uptime samples, Core Web Vitals, 400-day retention | PostgreSQL tables with the same shapes and retention |
| An event bus | domain events published through the outbox, durable and replayable | the outbox table and its relay |
| OpenSearch | cross-entity search over orgs, projects, deliverables, tickets and content, permission-filtered at query time, not after | PostgreSQL queries that apply the permission filter inside the query |

**The outbox.** Nothing publishes an event inside a business write by calling a broker:

- the business write records its domain rows and an `outbox_events` row in the same PostgreSQL
  transaction;
- a relay reads `outbox_events` in order, dispatches, and marks dispatched;
- consumers are idempotent by event id and tolerate at-least-once delivery;
- every event carries `event_id`, `occurred_at`, `aggregate_type`, `aggregate_id`, `version`,
  `actor_principal_id`, `correlation_id`, `causation_id`, `tenant_id`, `payload` and `schema_version`.

Event schemas are versioned and additive-only; a breaking change publishes a new event name, the registry lives in
`contracts/events/`, and CI verifies that every published event matches a registered schema (T-ARCH-03).

**Environments and the client-asset boundary.** The reference runs four environments, `local`, `preview`
(per change, synthetic data only), `staging` (anonymised production shape) and `production`, with one
rule with teeth: production client data never appears outside `production`, and staging replaces every
vault secret with an unusable sentinel, because a staging database that can authenticate to a client's
real CMS ends the agency. This environment is seeded fixture data throughout.

### Principals, not users

Parallax has principals: anything that can be the subject of an authorisation decision and the actor on
an audit record. There are five kinds, and conflating any two is a privilege-escalation defect.

| Kind | Examples | Authenticates via | Lives in |
|---|---|---|---|
| Agency principal | an employee of Parallax Malta or Parallax France | the agency IdP with mandatory MFA; here, password sign in against Keycloak | `principals` with `agency_memberships` |
| Client principal | a marketing manager at Verdane, procurement at Aeroline | the client's own IdP by SAML or OIDC when federated, else magic link with MFA; here, password sign in against Keycloak | `principals` with `org_memberships` |
| External principal | a freelance developer, a partner agency, an auditor | the agency IdP as a guest, MFA required, always time-bounded; here, password sign in against Keycloak | `principals` with `grants` only |
| Service principal | the report generator, the monitoring ingester, the billing job | mTLS or a signed, scoped service token | `service_principals` |
| Device principal | a monitored client site posting a beacon | a rotatable per-site HMAC key | `site_keys` |

Every row that records an action stores `actor_principal_id`, `actor_kind`, `on_behalf_of_id` (for
delegation), `request_id`, a hashed address and `auth_context`, which says how the principal proved
identity, including whether MFA and step-up were satisfied. There are no exceptions, jobs included.

### Organisations

Three organisation kinds share one table with a discriminator, because they share relationships (a
partner can be a client, a client can be a supplier):

- **agency entity**: exactly two, `Parallax Malta Ltd` (`MT`, issuing for English-site engagements) and
  `Parallax France SAS` (`FR`, issuing for French-site engagements), each with its own invoice sequences,
  bank account, rate card and legal footer;
- **client organisation**: the client businesses, carrying country, VAT number and VIES validation
  state, billing entity, industry and a governance profile;
- **partner organisation**: subcontractors, freelance collectives, white-label partners.

Client organisations have internal structure: org units form a self-referential tree (Aeroline, then
Digital, then Brand) and org memberships bind a principal to an organisation, optionally to a unit, with
a role, an optional approval threshold and an optional expiry. Approval chains reference units, not only
individuals, so a departure never orphans a workflow.

### Role catalogue

**Agency roles**, scoped to an agency entity and inheritable across both entities only for group admin:

| Role | Core rights | Notably cannot |
|---|---|---|
| `group_admin` | everything across both entities, including policy and role administration | read a vault secret without a second approver; edit an audit record |
| `finance_admin` | rate cards, invoices, credit notes, VAT configuration, payment reconciliation, revenue recognition, for its own entity | approve a deliverable; access the vault |
| `account_director` | owns client relationships; sees margin, cost and rates; approves proposals and change orders up to a threshold; is an approver where a client's policy names the account's director | issue an invoice; grant vault access outside its portfolio |
| `project_manager` | runs projects, milestones, tasks, capacity, client communication, content; submits proposals | see blended cost or margin unless a `commercial_visibility` grant is attached |
| `producer` | designer, developer, SEO or SEA specialist; executes tasks, logs time, uploads deliverable versions | see any financial field; access production credentials without a just-in-time request |
| `analyst` | read-only across delivery and marketing performance data, builds reports | write anything outside report definitions |
| `recruiter` | the applicant pipeline only | see any client data |
| `security_officer` | vault policy, break-glass second approval, access reviews, audit export | approve its own break-glass request |

**Client roles**, scoped to one client organisation:

| Role | Core rights |
|---|---|
| `client_owner` | full visibility of its organisation: contracts, invoices, deliverables, reports, tickets; manages its users and IdP binding; final approver by default |
| `client_approver` | approves deliverables and change orders within the threshold on its membership |
| `client_collaborator` | comments and annotates deliverables, opens tickets, uploads assets; cannot approve |
| `client_finance` | invoices, payment status and billing documents only; no deliverables |
| `client_viewer` | read-only on a named project subset |

**External roles:** `contractor` (project-scoped, always expiring), `partner_pm` (a partner's project
manager on white-labelled work, who sees the project and never the end client's commercial terms) and
`auditor` (read-only, time-bounded, and its reads are themselves audited).

### The authorisation model

Roles alone cannot express the rules this business has. Three worked examples, each an attribute and
relationship decision rather than a role check:

- a `project_manager` may see a line's day rate only for projects in its own entity, and never for
  white-labelled work where the partner's rate is embedded;
- a `client_approver` at Aeroline may approve a deliverable only if its value is at or below the
  approver's threshold, the approver did not upload the version, and the preceding stage is complete;
- a `producer` may read the production CMS credential for `verdane.example.com` only while an open ticket
  or task assigned to it references that site, only within its working window, and only after a step-up
  in the last 15 minutes.

Parallax therefore ships a policy decision point with these properties:

- **deny by default**: the absence of a matching permit is a denial;
- **explicit deny wins** over any permit, always, `group_admin` included;
- **decisions are data**: every permit and deny is recorded with the policy id, a hash of the input
  attributes and the latency, at 100 per cent for vault and finance resources and 1 per cent for reads;
- **one policy bundle for API and UI**: the UI asks for a decision set to render affordances and never
  re-implements a rule; a UI hiding a button the API would permit is a defect, and showing one the API
  would deny is a worse one.

### Delegation and time-bounded grants

Grants are a first-class table, not a column: grantee, resource type and id, capability, granted by,
reason, start, end, revocation instant and actor, whether step-up is required, maximum uses, uses so far.

- **Every external principal's access is a grant, and every grant has an end.** A grant without an end
  cannot be created: the API refuses it with `422` and code `grant_requires_expiry`.
- **Delegation** (an account director delegating approval authority for a date range) creates grants
  carrying `on_behalf_of`, and every action taken under one records both principals. Delegation is not
  transitive: a delegate cannot re-delegate.
- **Expiry is enforced at decision time, not by a cleanup job.** An expired or revoked grant is denied on
  the next request that relies on it; the reconciliation job exists to detect drift, never to enforce.
- Grants over vault resources additionally require step-up and carry a maximum number of uses.

### Governance profiles

Applying the strictest controls to every client makes the system unusable for the many who do not need
them, so each client organisation carries a profile:

| Profile | Applies to | Effects |
|---|---|---|
| `standard` | SMB clients, the majority | magic-link auth with MFA, single approver, 12-month audit retention, PDF invoices |
| `enterprise` | listed and large clients: Aeroline, Banque Horizon, Pharmalis, Enerva, Verrier Group | mandatory federated SSO, SCIM, approval chains with at least two stages, 7-year audit retention, quarterly access review, DPA and sub-processor register exposed in the portal |
| `public_sector` | Institut Lumiere, Laboratoire Nova, Centre Lumen and similar | everything in `enterprise`, plus Chorus Pro invoice routing, purchase-order enforcement (no invoice issues without a PO reference) and public-procurement document retention |

The profile is an input to policy, not a set of feature flags in code: raising a client from `standard`
to `enterprise` changes behaviour with no deployment.

### Permission matrix

`R` read, `W` write, `A` approve, a dash for no access, `G` only through an explicit grant.

| Resource | group admin | finance admin | account director | project manager | producer | client owner | client approver | client collaborator | contractor |
|---|---|---|---|---|---|---|---|---|---|
| Client org profile | RW | R | RW | R | - | RW own | R own | R own | - |
| Opportunity and pipeline | RW | R | RW | RW | - | - | - | - | - |
| Proposal draft | RW | R | RWA | RW | - | - | - | - | - |
| Proposal sent | R | R | R | R | - | R own | R own | - | - |
| Contract and change order | RW | R | RWA | RW | - | RA own | A own within threshold | R own | - |
| Rate card and cost | RW | RW | R | G | - | - | - | - | - |
| Margin on a project | R | R | R | G | - | - | - | - | - |
| Project and tasks | RW | R | RW | RW | RW assigned | R own | R own | R own | RW granted |
| Time entries | RW | R | R | RW | RW own | - | - | - | RW own |
| Deliverable version | RW | - | RW | RW | RW | R own | RA own | RW comments | RW granted |
| Approval decision | R | - | A | - | - | A own | A own within threshold | - | - |
| Invoice | RW | RW | R | R | - | R own | - | - | - |
| Vault secret | G two-person | - | G | G | G just-in-time | - | - | - | - |
| Audit log | R | R finance scope | R own portfolio | - | - | R own org actions | - | - | - |
| Content and CMS | RW | - | R | RW | RW own drafts | - | - | - | - |
| Applicant records | R | - | - | - | - | - | - | - | - |

The machine-readable matrix lives with the policy bundle and this human summary is generated from it, so
the two cannot drift.

### The decision point in practice

One policy decision point is consulted by everything: an embedded policy engine in the Cedar or OPA
style, with its bundle versioned with the code and never edited in production.

A request carries the principal (id, kind, roles, org ids, entity, MFA and step-up instant), the action
(such as `deliverable:approve`), the resource (type, id, client org, project, value, uploader, white-label
flag) and context (now, country, request id). The response is a decision of permit or deny, the policy id,
obligations and a reason.

**Obligations** make field-level redaction central: a permit may carry an obligation to redact
`cost_price_minor` and `margin_minor`, and serialisation applies it in one place. A field redacted by
obligation is **absent from the response body**: not `null`, not zero, so its existence cannot be
inferred.

Six rules:

- deny by default; no matching permit is a deny;
- an explicit deny is final and no permit overrides it, `group_admin` included;
- decisions may be cached for at most 30 seconds, keyed by the full input, and the cache is bypassed
  entirely for vault, finance-issue and grant-creation actions, because a stale permit on a revoked grant
  is exactly the defect a cache must never cause;
- every deny on a write and every decision on a vault or finance resource is logged, read denies sampled
  at 1 per cent plus always for auditor principals;
- the UI consumes the same engine through a batch decision endpoint, so affordances and enforcement cannot
  diverge;
- row-level security is the second layer: every tenant-scoped table is filtered by the session's
  organisation set, so a bypassed policy layer still reads nothing across tenants.

### Authentication and sessions

In the reference, agency principals sign in through the agency IdP with mandatory MFA and WebAuthn
preferred and no local passwords; client principals are federated where their organisation has an IdP,
otherwise use a single-use magic link (10-minute expiry, invalidated on use, bound to the requesting user
agent) plus TOTP for `enterprise` and `public_sector` organisations; if passwords are ever offered they
use Argon2id, breach-list checking and no composition rules beyond length.

In this environment every seeded principal signs in with email and password through Parallax, which
exchanges them with Keycloak. Seeded principals hold no MFA enrolment: the password sign in completes the
session, and the step-up below is the only second proof this build asks for.

- **Sessions**: the browser holds an httpOnly, `Secure`, `SameSite=Lax` session cookie with a
  double-submit CSRF token on state changes, and API clients present `Authorization: Bearer <access_token>`
  from `POST /api/auth/login`. Absolute lifetime 12 hours; idle timeout 30 minutes for agency principals
  with vault capability and 8 hours otherwise; rotation on privilege change; full session listing and
  revocation in profile settings.
- **Refresh tokens** rotate on use with reuse detection: a replayed refresh token revokes the whole
  session family and alerts.
- **Step-up** is required, no older than 15 minutes, for any vault reveal, invoice issue, credit note,
  grant creation, role change, IdP configuration and audit export. `POST /api/auth/step-up` with
  `{"password"}` re-proves the session's principal and answers `200` with `{"step_up_at"}`; a wrong
  password answers `401` with code `invalid_credentials`. Signing in is not a step-up: a session has none
  until that call succeeds. An action needing step-up without a recent one is refused with `403` and code
  `step_up_required`.
- **No secret is ever logged, returned in an error, or placed in a URL.**
- **Signup is closed** in every space: `POST /api/auth/signup` answers `404` with code `not_found`, and no
  call creates an account for its own caller.

### Lifecycles, the system's spine

Five state machines carry the business. Each is states, permitted transitions, the guard on each, and the
side effects that happen exactly once. A transition not listed is refused with `409` and code
`illegal_transition`, and the attempt is audited.

**Lead lifecycle.** States `new`, `triaged`, `qualified`, `converted`, `spam`, `duplicate`,
`disqualified`.

| Transition | Guard | Side effects, exactly once |
|---|---|---|
| to `new` | the submission passes anti-abuse, consent is true, required fields are valid | persist the lead and its attribution; notify the routing target; set the first-response due instant; publish `lead.created` |
| `new` to `spam` | a spam score of at least 0.85, or manual | no notification to a human; retained 30 days, then purged |
| `new` to `triaged` | the actor holds `crm:triage` | assign an owner by the routing rules; publish `lead.triaged` |
| `triaged` to `duplicate` | a matching org domain and email within 90 days | merge activity onto the surviving lead, keep both rows, link them |
| `triaged` to `qualified` | budget band and project kind present, the actor holds `crm:qualify` | create or attach the organisation; create an opportunity at `scoping`; publish `lead.qualified` |
| any to `disqualified` | a reason from an enumerated list, never free text | publish `lead.disqualified`; suppress from remarketing exports |
| `qualified` to `converted` | the opportunity exists | link the opportunity; freeze the lead, immutable thereafter |

**First-response SLA.** The due instant is created plus 4 business hours, or 2 for high priority, on the
calendar of the entity the lead routed to, because Malta and France have different holidays. Breach at
100 per cent of budget notifies the account director; at 150 per cent it escalates to `group_admin`.

**Opportunity to contract.** `discovery`, `scoping`, `proposal_sent`, `negotiation`, `verbal_yes`,
`won`, with `lost` or `dormant` reachable from any open stage.

- `scoping` to `proposal_sent` requires a proposal in `sent` whose entity matches the opportunity's,
  whose valid-until date is in the future, and whose tax treatment resolved without error; a proposal
  cannot be sent while the buyer's VAT number is invalid and the treatment would be reverse charge: it
  goes to `finance_admin` for a decision instead of silently issuing untaxed.
- `verbal_yes` to `won` requires an `active` contract, which requires a signature instant set only by a
  verified e-signature webhook, never by a human clicking mark as signed; a human override exists
  (`finance_admin`, an uploaded countersigned PDF and a reason) as a distinct, separately audited action.
- `won` is terminal; further commercial change happens through change orders.

**Deliverable approval, the transition that moves money.** A deliverable moves `draft`, `internal_review`,
`shared`, then `approved` or `changes_requested`, and a new version returns it to `shared` at the next
version. An approval on a milestone-linked deliverable moves the milestone to `approved`, which releases
its draft invoice.

- **Stage evaluation.** Sharing creates an approval from the client organisation's deliverable policy
  whose value band contains the milestone's bill amount. Stages run in order; within a stage the mode
  decides completion: `any_of` completes when any one assignee approves, `all_of` when every assignee
  approves, `quorum` when the stated number approve, ignoring abstentions. A rejection at any stage ends
  the whole approval as `rejected` and moves the deliverable to `changes_requested`; there is no partial
  approval, and approved with comments is a rejection with a comment.
- **Guards.** The approver's threshold must be at least the approval's value, or the decision is refused
  and the approval unchanged. The principal who uploaded the version under review can never decide on it,
  even where its role permits approval generally. The version at decision time is recorded on the step,
  and if a new version is uploaded while an approval is pending, that approval is **cancelled**, not
  carried over, and the client is told why.
- **Timeouts and escalation.** A policy's timeout runs on the client's business calendar; on expiry it
  notifies, escalates to the parent unit's approver, or auto-rejects. There is no auto-approve option:
  silence is never consent for something that releases an invoice.
- **Assignee resolution and departures.** A stage names a principal, a role or an org unit. Resolution
  order: the named principal while its membership is active, then any active member of the named unit
  with the required role, then the client's `client_owner`, then the account director, with a banner
  telling the client its routing is broken.
- **Side effects on approval**, in one transaction: approval `approved`, deliverable `approved`, milestone
  `approved` with its instant, an audit entry, and an outbox event `milestone.approved`. Drafting the
  invoice consumes that event, so a rendering failure never rolls back a client's approval, and the draft
  is created once per milestone however many times the event is delivered.

**Invoice lifecycle.** `draft`, `issued`, `sent`, then `partially_paid` and `paid`, or `overdue` through
dunning to `written_off`, or `disputed` until resolved to `paid` or credited; an issued, sent or paid
invoice becomes `void` only through a credit note.

- `draft` to `issued` assigns the number, freezes the lines, computes tax, renders the PDF and, where
  required, the Factur-X hybrid for the e-invoicing channel; after this an invoice is immutable.
- An invoice is never deleted and never renumbered; an error is corrected by a credit note that references
  the original and takes the next number in the credit-note sequence.
- `sent` to `overdue` is computed daily from the due date, never set by hand.
- `disputed` pauses dunning and notifies the account director; a dispute raised in the portal requires a
  reason and opens a ticket.
- Payments allocate to invoices explicitly; a payment is never matched to an invoice by amount, because
  transfers arrive with wrong references and two invoices can share a total.

**Ticket and SLA lifecycle.** `new`, `triaged`, `in_progress`, then `waiting_on_client` or
`waiting_on_third_party` and back, `resolved`, `closed`, and `reopened` from `resolved`.

- Entering a paused state writes a pause clock event and leaving it writes resume; the respond target stops
  permanently at the first agency response, and the resolve target accumulates only unpaused business time.
- `resolved` to `reopened` within 72 hours restarts the resolve clock with the budget remaining at
  resolution, never a fresh budget, so closing and reopening cannot launder an SLA.
- Tickets opened from site alerts inherit priority from the alert severity and skip `new`, because a
  confirmed outage does not wait for triage.

**Contract exit, the lifecycle everyone forgets.** When a client leaves, five things happen and Parallax
proves each:

- the final invoice is issued and reconciled, and unbilled approved milestones are flagged;
- credential handover: each managed site moves `held`, `handover_requested`, `handed_over`, which requires
  the client to confirm receipt in the portal, and on `handed_over` the agency's copies are crypto-shredded
  by destroying the organisation's key, and the fact is recorded;
- connectors are revoked at the provider, not merely marked revoked locally;
- portal access ends: every client principal's membership is end-dated and every agency grant over that
  organisation's resources is revoked;
- a machine-readable portability export of contracts, invoices, deliverable files, ticket history and the
  report archive is generated, retained for the statutory period, then deleted on schedule.

### Business logic

**Lead routing** is deterministic, ordered and auditable, and the decision is stored on the lead:

- **entity** is `parallax-france` when the submission came from the French site or the company country is
  `FR`, otherwise `parallax-malta`; a tie resolves to the form's own site;
- **owner** is the account director already owning an organisation matching the email domain; otherwise a
  round-robin among the entity's account directors, weighted by open opportunities and skipping anyone on
  declared leave;
- **priority** is `high` when the budget band is `band_30_60k` or `band_60k_plus` or the email domain is
  on the named account list, otherwise `normal`;
- **SLA** is 4 business hours on the entity's calendar for `normal` and 2 for `high`.

**Anti-abuse scoring** for public submissions is a composite score between 0 and 1, evaluated on the
server, because any single signal is weak.

| Signal | Weight |
|---|---|
| The hidden `website` field is filled | 1.00, immediate `spam` |
| Time to submit under 4 seconds across a six step wizard | 0.45 |
| A disposable-domain email | 0.25 |
| A message with 3 or more links, or a known SEO-spam n-gram | 0.30 |
| A company country inconsistent with the phone's country code | 0.10 |
| An address belonging to a hosting provider, not an ISP | 0.20 |
| The same /24 submitting 5 or more times in 24 hours | 0.35 |

A score of 0.85 or more stores the lead as `spam` with no human notification and purges it after 30 days;
0.55 to 0.85 escalates to a Turnstile challenge, and passing subtracts 0.4 and re-evaluates; below 0.55 is
accepted. **A spam outcome answers the submitter exactly as an accepted one does**, with a reference, so a
bot learns nothing. Rate limits are layered: 5 submissions per address per hour, 3 per email per day, 30 per
/24 per hour, and a global circuit breaker switching every form to a mandatory challenge when the site-wide
rate exceeds ten times the trailing 7-day median. Every per-address limit and every address-based signal in
Parallax counts the client address a request arrives from and exempts private and loopback addresses, which are
the edge and internal proxies in front of the app. The time-to-submit signal is measured only for a submission
the wizard page made with its own start instant; a submission without one adds nothing for that signal.

**Upload safety**: every uploaded byte follows one path, with no shortcut for internal uploads:

- the client requests a single-object upload slot scoped to one key, one content-length range and a
  5-minute expiry;
- the bytes land in quarantine, which no application path reads;
- the client confirms and a scan is enqueued;
- the scanner compares declared and detected type from magic bytes (a `.pdf` that is a PHP file is
  rejected), size, PDF page count, an antivirus pass, and embedded JavaScript or launch actions in PDFs;
- clean files move to durable storage under a normalised name; infected files are deleted, recorded and
  alerted;
- only a `clean` file can be linked to a lead, deliverable or application, and only then can a download be
  minted.

Downloads are short-lived (5 minutes), single-use, minted after an authorisation decision, served with
`Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`, never from a path a user controls.

**The approval engine** is a durable workflow, because it must survive a deploy in the middle of a
three-week approval:

- state transitions are events, not mutations, and an approval's state is a fold over its decisions,
  escalations, reminders and timeouts, which is what makes what was approved and when answerable years
  later;
- timers are durable and calendar-aware: a reminder for 48 business hours survives restarts and never fires
  on 15 August in France;
- every decision is idempotent on approval, step and principal, so a double-click, a retried webhook and a
  mobile retry produce one decision;
- escalation cannot create authority: escalating finds a principal whose threshold covers the value, and if
  none exists the approval blocks and alerts.

**Tax determination** runs at proposal issue and again, authoritatively, at invoice issue, from the supplier
entity's country, the buyer's country, the buyer's VAT number and its validation state, whether the buyer is
a business, the place-of-supply rules for electronically supplied services, and the issue date.

| Case | Treatment | Rate | Note printed on the invoice |
|---|---|---|---|
| Malta entity to a Maltese client | `domestic_mt` | Malta standard, `1800` basis points | `Standard Maltese VAT` |
| France entity to a French client | `domestic_fr` | French standard, `2000` basis points | `Standard French TVA` |
| France entity to an EU business with a valid VAT number | `eu_reverse_charge` | `0` | `Autoliquidation - Article 283-2 du CGI` |
| Malta entity to an EU business with a valid VAT number | `eu_reverse_charge` | `0` | `Reverse charge - Art. 196 VAT Directive` |
| Either entity to an EU consumer | `eu_b2c` | the supplier's domestic rate | no note |
| Either entity to a business outside the EU | `export_outside_eu` | `0` | `Outside scope` |

A business buyer is one with a VAT number on its organisation; the EU is the twenty seven member states.
Hard rules:

- **A zero-rate reverse charge is never applied on an unvalidated VAT number.** When the buyer's validation
  state is `invalid`, the issue is refused with `422` and code `vat_number_invalid` and blocks for
  `finance_admin`.
- **When the register is unreachable Parallax does not guess.** VIES is not reachable from this environment,
  so each organisation's stored state is what a lookup returned: `valid`, `invalid` or `service_unavailable`,
  with `vat_validated_at` the instant of the last successful validation. When the state is
  `service_unavailable`, the last successful validation is used if it is under 90 days old at the issue
  instant; otherwise the issue is refused with `422` and code `vat_validation_stale`. Applying a zero rate on
  the basis of a timeout is a tax exposure with the agency's name on it.
- **Rates are dated, not constants**: a rate table with valid-from and valid-to dates, where the issue date
  selects the row, so re-issuing a 2025 credit note in 2026 uses the 2025 rate.
- **The treatment and rate are snapshotted onto the invoice** and never recomputed on read.

**Invoice issue** is one transaction, in this order:

- re-run tax determination and refuse on any unresolved condition;
- verify a PO number is present when the client's profile is `public_sector`, refusing with `422` and code
  `po_required` otherwise;
- take the next value of the entity's sequence for that document type and year, serialised per sequence
  so two issues never read the same next value, assign the number, and advance the sequence;
- freeze the lines and compute every total from the lines, never from a client-supplied total;
- write the audit event and the outbox event `invoice.issued`.

A refused issue changes nothing: the invoice stays `draft` with no number and **no sequence value is
consumed**, because a consumed and abandoned value is a gap. After the transaction, idempotently on the
invoice, Parallax renders the PDF, renders Factur-X where the buyer is French, records the submission to the
e-invoicing channel and sends the notification; a failure there leaves the invoice `issued` with its
e-invoice state `failed` and an alert, and never rolls back the number.

**Numbers and totals.** A number is the entity's prefix, the issue year in UTC, a hyphen and a five digit
counter starting at `00001` for each entity, document type and year: invoices of Parallax France read
`PXF-2026-00001`, of Parallax Malta `PXM-2026-00001`, and credit notes `PXFC-2026-00001` and
`PXMC-2026-00001`. A line's amount is its quantity times its unit price in minor units; the subtotal is the
sum of lines; tax is the subtotal times the rate in basis points divided by ten thousand, rounded once, half
away from zero, to a whole minor unit; the total is subtotal plus tax. Every amount is an integer number of
euro cents.

**E-invoicing channel**: `chorus_pro` for a `public_sector` client, `pdp` (a registered platform) for any
other French business client of Parallax France, `none` otherwise.

**Billing triggers:**

| Trigger | Rule |
|---|---|
| `on_approval` | `milestone.approved` drafts an invoice for the milestone's bill amount, or its bill percent of contract value |
| `on_date` | a nightly job on the milestone's due date |
| Retainer | monthly on the retainer's billing day, in advance, with overage from the previous period computed from approved time above included hours, honouring the rollover policy |
| Time and materials | monthly, from approved and unlocked time entries only; a time entry approved after its period is locked moves to the next period rather than mutating a closed one |

Drafts queue for `finance_admin` review and nothing auto-issues: the system generates, a human issues, so
the moment a legal document comes into existence has a person's name on it.

**Content publishing and SEO derivation:**

- publishing is a transition on a localisation, guarded by an editorial approval for `landing` and
  `article` types, and scheduled publishing runs on a durable timer;
- **hreflang is derived, never authored**: each published localisation emits alternate links for every
  sibling localisation of the same entry key plus `x-default` pointing at the English version;
- cross-domain canonicals are emitted where two localisations share a language, and every published path is
  recorded as an alias so changing a slug creates a `301` automatically rather than a `404`;
- sitemaps are generated from what is published and indexable, with last-modified from the published
  version;
- **the landing matrix is gated**: generation produces a draft from the shared template plus city-specific
  evidence (local case studies, local client names, the office address), a similarity check computes the
  unique body ratio against sibling pages, and below the threshold the page stays `noindex` and is queued
  for a writer. No page enters the index because a loop generated it.

### Managed sites and the credential vault

This is the subsystem where a mistake ends the business. Managed sites carry a label, primary URL,
environment (`production`, `staging`, `development`), platform, hosting provider, registrar, whether
monitoring is on, a beacon key, the date under management began, and a handover state of `held`,
`handover_requested`, `handed_over` or `revoked`. Vault secrets carry a label, a type (`cms_admin`,
`hosting`, `dns`, `registrar`, `ftp_sftp`, `database`, `api_key`, `ads_account`, `analytics`, `ssl`,
`other`), the encrypted value, its wrapped data key and key id, a version, rotation due and last rotated
instants, and a destroyed instant for crypto-shredding.

Six rules govern the vault, and all six hold here:

- **No standing access.** No role can read a secret. A read requires an approved access request with a
  time to live of at most 240 minutes, bound to an open ticket or task.
- **Step-up within 15 minutes** of the read, always, for every principal.
- **Two-person rule for break-glass.** Out-of-hours emergency access requires a second named approver who
  is neither the requester nor the approver of record.
- **Per-organisation keys.** Each client organisation's secrets are wrapped under a distinct key, so
  deleting a client's data is achievable by destroying one key, and a leaked data key compromises one
  organisation rather than four hundred.
- **Reads are logged before the value is returned**, in the same write as the usage count; if the log write
  fails, the read fails.
- **No bulk export path exists.** No call returns more than one secret; an attempt is recorded as
  `export_denied` and pages the `security_officer`.

Beyond those rules:

- **Envelope encryption**: a data key per secret, wrapped by the organisation's key; the vault never exports
  a key. In this environment Parallax generates its key material inside its own container at first start,
  outside the database and never served, so **the vault tables hold no plaintext and no unwrapped key**: a
  full dump of the database without the key material yields nothing.
- **Isolation**: only the vault module reaches the vault tables, and it re-checks authorisation itself.
- **Reveal responses are single-use and never cached**, marked `Cache-Control: no-store`, and the browser
  clears the value on blur or when the countdown ends.
- **Rotation tracking**: every secret has a rotation due date, overdue secrets appear on the account
  director's dashboard, and any secret revealed by a principal who later leaves is flagged for rotation
  automatically.
- **Quarterly access review**: the `security_officer` and each account director attest to the grant list for
  their portfolio, and unattested grants expire.

**Who approves.** A vault access request is approved by the `security_officer` or by the account director
of the secret's client organisation, never by its requester. A normal request is `approved` after one
approval. A break-glass request is `awaiting_second_approver` after its first approval and `approved` only
when a different eligible principal approves it; the same approver approving twice is refused with `409`
and code `second_approver_must_differ`.

**The access log** is append-only and hash-chained. Every create, read, rotate, destroy and
`export_denied` appends an entry carrying its `sequence` (starting at `1`, one chain for the whole vault),
`action`, `principal_email`, the access request id where there is one, `occurred_at`, the previous entry's
hash as `prev_hash` (sixty four zeros for the first) and its own `entry_hash`, the SHA-256 hex digest of
`prev_hash` followed by its sequence, secret id, action, principal email, request id and occurrence instant.
Recomputing the chain in order reproduces every hash, and a changed entry breaks its own hash first. No
connection the application holds can update or delete a log row, because that guarantee cannot rest on the
application's own good behaviour.

### Integrations

Ten external systems, each with the failure mode that matters, because that is the part routinely got wrong.
In this environment each is its records, its inbound endpoint and its stated states.

**Identity providers, OIDC and SAML 2.0.** Per-client IdP registration: OIDC with authorisation code and
PKCE, `nonce` and `state` validated, `iss`, `aud`, `exp`, `iat` checked, JWKS cached with rotation; SAML
assertions validated for signature against the registered certificates with clock skew of at most 2
minutes, `NotBefore` and `NotOnOrAfter`, `Destination`, `InResponseTo`, and replay through an assertion id
cache. The two failures that matter: **domain confusion**, where an assertion may only mint or match a
principal whose email domain is verified for that IdP by a DNS TXT record, domains being globally unique so
a second claim escalates to the `security_officer` rather than resolving first come first served; and
**ignored group claims**, where group-to-role mapping applies on every login, so a user removed from the
`dc-approvers` group at Aeroline loses approval authority at the next login and within 24 hours regardless.

**SCIM 2.0.** `Users` and `Groups` with PATCH semantics, per-IdP bearer tokens held in the vault and
rotatable, filtered reads. `active=false` immediately end-dates every membership and revokes every session
and grant, not at next login; deletions are deactivations. Where SCIM is unavailable, the reconciliation job
compares against the IdP's directory nightly, and drift older than 24 hours is an alert, not a log line.

**Email.** A transactional sender authenticated for both entities' domains (SPF, DKIM, DMARC at reject after
monitoring), per-recipient locale, a plain-text alternative on every message, one-click unsubscribe for
anything marketing-shaped, bounce and complaint handling that marks contacts undeliverable, and suppression
honoured across both entities: a person who unsubscribed from the French entity never receives an English
campaign. Deliverability incidents are visible in the back office. Here every message goes through Mailpit.

**E-signature.** Envelopes from the generated contract PDF, ordered signer routing, completion driven by
webhook only: signature verification against the provider's public key, tolerance of event order
(`completed` may arrive before `delivered`), idempotent processing on the envelope id, and storage of the
signed artefact and certificate of completion as immutable files. A contract is `active` only when the signed
artefact is stored, not when the webhook arrives.

**Payments and e-invoicing.**

- **Stripe** for cards and SEPA Direct Debit on retainers, with webhook signature verification and replay
  protection by event id; the ledger is PostgreSQL, not Stripe, so Stripe events create payment rows that are
  then explicitly allocated. Failed direct-debit retries follow the scheme's rules, move the retainer to
  `payment_failed` and start dunning, and after 3 failures suspend service with notice.
- **A bank feed** for SEPA credit transfers (CAMT.053 import or an open-banking connector) creates payments
  with a suggested allocation that a human confirms.
- **E-invoicing**: Factur-X (PDF/A-3 with embedded CII XML) for French buyers, submitted through a registered
  platform for businesses and through **Chorus Pro** for public buyers, which requires the buyer's SIRET,
  service code and engagement (PO) number. Rejections arrive asynchronously and typed: the invoice stays
  issued, its e-invoice state becomes `rejected` with the reason shown to `finance_admin`, and the correction
  is a credit note plus a re-issue, never an edit.

**Analytics and search connectors (GA4, Search Console, Google Ads, Meta).** OAuth with offline access per
client. Tokens live in the vault and are referenced, never stored in plaintext in application tables. Refresh
happens before expiry on a jittered schedule, and `invalid_grant` marks the connector `revoked` and raises a
task for the account manager rather than retrying forever. Quota discipline is a token bucket per provider per
client with exponential backoff and jitter on `429` or `RESOURCE_EXHAUSTED` and a global concurrency cap, so one
client's backfill never starves the nightly sync for the other 399. Sampling metadata and Search Console's
roughly three-day finality are recorded per snapshot and surfaced in reports. Offline conversion export to
Google Ads uploads a conversion when a lead with a `gclid` becomes qualified or won, so Ads optimises on revenue
rather than form fills, and it is gated on consent: **no `gclid` is captured or exported without marketing
consent**.

**VIES VAT validation.** A lookup cached 24 hours by VAT number, storing the consultation number as evidence,
treating unavailability explicitly, and never caching a negative result longer than 1 hour.

**Site monitoring probes.** Synthetic checks from at least 3 regions every 60 seconds for `p1` sites and every
5 minutes otherwise: HTTP status, response time, TLS expiry, the content hash of a declared selector
(defacement and parking-page detection) and a scripted login check where permitted; plus real-user vitals
posted by a beacon on managed sites, signed with the site's HMAC key.

**Slack or Teams.** Outbound only, routed per channel for lead alerts, approval reminders, SLA breaches and
site alerts, carrying only a title and a link that requires portal authentication, with a per-workspace token
in the vault and email as the fallback, because chat is a convenience and email is the record.

**Consent management.** Server-side consent state is authoritative: the banner is the interface, enforcement
lives in the tag loader and the API, Consent Mode v2 signals are set from the stored state, and every decision
is kept as proof.

### Webhooks

**Outbound**, to clients and partners that want project and invoice events in their own systems:

- signed with `X-PX-Signature: t=...,v1=HMAC-SHA256(t + "." + body)` using a per-endpoint secret, with
  `X-PX-Event-Id` for the receiver's idempotency;
- at-least-once, retried with backoff after 1 minute, 5 minutes, 30 minutes, 2 hours, 6 hours and 24 hours,
  then the endpoint is disabled and the client notified;
- replayable from the back office for 30 days;
- ordered per aggregate on a best-effort basis, with a monotonically increasing aggregate version so a
  receiver can discard stale deliveries;
- no personal data beyond identifiers by default, with payload scope configured per endpoint and shown to
  the client.

**Inbound:**

| Source | Verification | Idempotency |
|---|---|---|
| Stripe | signature and a timestamp tolerance of 5 minutes | the event id |
| E-signature provider | the provider's public-key signature | envelope id plus event type |
| Email provider bounces | a signed webhook or mTLS | message id plus event |
| E-invoicing platform | mTLS and a signed payload | submission id plus status |
| Monitoring probes | mTLS from the probe network | the check id |
| Site beacons | per-site HMAC, a 5-minute timestamp window and a replay cache | the beacon id |

Every inbound webhook writes the raw receipt first, answers `200` fast and processes asynchronously; a
processing failure never makes the sender retry a stored payload, and raw payloads are kept 30 days for replay
and dispute.

### Background jobs

| Job | Work | Schedule | Idempotency and notes |
|---|---|---|---|
| J-01 | outbox relay | continuous | ordered per aggregate, at least once |
| J-02 | lead SLA sweep | every 5 minutes | notifies at 100 and 150 per cent of budget, keyed by lead and threshold |
| J-03 | approval reminders, escalation and expiry timers | durable timers | keyed by approval, stage and kind |
| J-04 | access reconciliation of IdP directory, memberships and grants | hourly | reports drift and revokes on confirmed departure |
| J-05 | grant expiry sweep | every 5 minutes | detection only; enforcement happens at decision time |
| J-06 | connector token refresh | every 15 minutes | jittered, one lock per connector |
| J-07 | metric sync for GA4, Search Console and Ads | hourly and a nightly full run | upsert on connector, date and dimension; re-fetches the last 3 days |
| J-08 | synthetic probe scheduler | 60-second and 5-minute tiers | a lock per site; confirmation rules below |
| J-09 | vitals rollup into daily aggregates | hourly | idempotent by site and day |
| J-10 | TLS expiry check | daily | a ticket at 14 days, `p1` at 3 |
| J-11 | milestone to draft invoice | on `milestone.approved` | unique on the milestone, safe to retry |
| J-12 | contract value reconciliation | nightly | alerts on any drift |
| J-13 | invoice sequence integrity | nightly | pages `finance_admin` on a gap or duplicate |
| J-14 | dunning ladder | daily | a per-invoice state machine that pauses on dispute |
| J-15 | retainer billing run | daily, acting on the billing day | unique on retainer and period |
| J-16 | audit chain verification and daily anchor | hourly and daily | pages the `security_officer` on a mismatch |
| J-17 | consent enforcement proof: a headless crawl for tags fired before consent | weekly and on deploy | fails the deploy gate on any violation |
| J-18 | retention sweep over files, leads, applicants and logs | nightly | per retention class, with a dry-run report before the first live run |
| J-19 | DSR due-date watch | daily | escalates at 20 days |
| J-20 | report generation | monthly and on demand | unique on definition and period, records completeness |
| J-21 | secret rotation due-date sweep | daily | creates tasks and never rotates by itself |
| J-22 | search index sync | continuous | from outbox events, permission-filtered at query time |
| J-23 | landing-matrix uniqueness evaluation | weekly | sets indexable to false on regression |
| J-24 | sitemap and hreflang regeneration | on publish and nightly | idempotent |
| J-25 | staging refresh with pseudonymisation | weekly | asserts vault sentinels |

Every job holds a lock so two runners never double-execute, a maximum runtime after which it is stopped and
alerted, structured logs with a job run id, and a dead-letter view in the back office. No job silently
swallows an exception, and a job failing twice in a row raises an alert.

### Caching

| Layer | Contents | Invalidation |
|---|---|---|
| Edge | public HTML, images, fonts, scripts and styles | on publish by content entry, with immutable hashed asset names |
| Application | policy decisions (at most 30 seconds, bypassed for vault, finance issue and grant creation), VIES results (24 hours), connector metadata, rate-limit counters | a TTL plus an explicit bust on the underlying write |
| Query | expensive aggregates: the pipeline forecast, project burn, uptime rollups | refreshed on a schedule, with the computed instant shown in the UI |
| Client | stale-while-revalidate with ETags; the portal shows staleness rather than hiding it | per key on mutation |

Two rules prevent the classic cross-tenant cache leak: every cache key includes the principal's organisation
scope and the policy bundle version, and no warming job runs with elevated privileges, so a warmed entry never
holds data the requesting principal could not have read.

### Notifications

Six channels: in-app, email, Slack or Teams, SMS for `p1` site alerts only, webhook and digest.

- Preferences are per principal, per event class, per channel, with sane defaults and an organisation-level
  policy that can require some notifications (an enterprise client can force approval notifications on).
- Digests collapse low-urgency events into a daily or weekly summary in the principal's timezone and locale.
- Quiet hours per principal are overridden only by `p1` alerts.
- Deduplication turns an event firing many times in a window into one notification with a count.
- Every notification links to the exact object, which requires authentication to view, and carries no client
  data beyond names the recipient already knows.

**Approval requests** are emailed when an approval is shared and whenever a stage becomes current: one message
to each assignee of the now current stage and to no one else, subject `Parallax: approval requested for `
followed by the deliverable's name, with the approval id as the first line of the body. The uploader, the
assignees of later stages and anyone who has already decided receive nothing for that stage.

### Validation

| Layer | Job |
|---|---|
| Client | immediate feedback and formatting, never trusted |
| API schema | shape, types, enums, lengths and formats, refused with field-level errors before business code runs |
| Domain | invariants needing context: transitions, thresholds, tax rules, cross-entity consistency |
| Database | constraints, foreign keys, uniqueness among live rows, check constraints, exclusion rules, row-level security |

Normalisations on write: emails lowercased and compared case-insensitively; phones parsed to E.164 with the
country from the form's country field; VAT numbers uppercased with spaces removed; URLs normalised and required
to be absolute `https`; filenames sanitised and never used as storage keys; free text length-bounded and stored
as given, escaped at render per context, so the same string is safe in HTML, in a PDF and in an email.

### End-to-end workflows

Six journeys, traced through every layer.

**Anonymous visitor to qualified opportunity.**

- A visitor lands on `/fr/agence-seo-lyon/` from a paid search click carrying a `gclid`.
- The consent banner appears before any tag loads; the visitor accepts analytics and marketing, the decision
  is recorded, Consent Mode signals are set, and only then do GA4 and the Ads tag start. Had they declined,
  the `gclid` would not be stored at all.
- They browse three case studies; first-touch and last-touch attribution accumulate in a first-party cookie
  holding a signed, opaque session id, never raw UTM values.
- They open `/fr/devis/` and complete the six step wizard, whose state survives an accidental refresh.
- On submit the lead is written once under its idempotency key with the typed budget band and project kind,
  the attribution, the consent version and a hashed address, and anti-abuse scores it low.
- The PDF specification uploads to quarantine, scans clean and is linked.
- Routing picks the France entity and the account director with the lightest pipeline; priority is `high`
  because the band is `band_30_60k`, so the first response is due in 2 business hours on the French calendar.
- The owner gets an in-app notification, `#leads-fr` gets a chat message, and the prospect gets an email
  confirmation from `contact@parallax-france.example.com` in French naming the response window and reference.
- The account director triages and qualifies; an organisation and an opportunity at `scoping` are created,
  and the `gclid` conversion is exported with the qualified-lead value.

Failure paths: an infected upload still lands the lead, flagged, with the file rejected and the prospect told;
an ambiguous score raises a Turnstile challenge and a re-score; a mail outage stores the lead, queues the
confirmation and still confirms success on screen, because the lead is what matters, not the receipt.

**Proposal to signed contract to project.**

- The account director builds an estimate of phases and roles times days from the French rate card, with
  margin visible and computed per line.
- Sending runs tax determination: a French SAS gets `domestic_fr`; a Belgian company would be checked against
  VIES for `eu_reverse_charge`, and the send would block on an invalid number.
- The client opens a link and the first view is recorded by an authenticated or tokenised view, never a
  tracking pixel.
- The client accepts; a contract is created `pending_signature` and an envelope is routed in the order defined
  for the client organisation.
- Both parties sign; the verified webhook is processed once, the signed artefact and completion certificate are
  stored, and only then does the contract become `active` and the opportunity `won`.
- A project is created from the proposal's phases: phases become milestones billed on approval, and tasks are
  seeded from the template for the service lines sold.
- Client principals are invited; for an `enterprise` client the invite starts the SSO setup flow with the
  `client_owner` instead.

**Deliverable to approval to invoice to payment.**

- A designer uploads version 3 of the homepage design to a milestone-linked deliverable.
- The project manager reviews it internally and shares it.
- An approval is created from the client's policy: stage one any of the brand team unit, stage two all of the
  head of digital and procurement, because the milestone value of forty thousand euros is above the
  single-approver threshold.
- The client's brand manager annotates three points and requests changes; the deliverable moves to
  `changes_requested` and the approval ends `rejected`.
- Version 4 is uploaded; annotations are remapped, one cannot be located and appears in the orphaned tray, and
  a fresh approval starts.
- Stage one approves; stage two's procurement approver is on leave and has delegated, and the decision records
  both principals.
- On completion the milestone is `approved`, the audit entry written and `milestone.approved` published.
- The billing job drafts the invoice; `finance_admin` reviews and issues it under the next France number, with
  tax `domestic_fr`, a PO number present because the client is `public_sector`, and Factur-X submitted to
  Chorus Pro.
- Chorus Pro rejects it because the service code is wrong; the e-invoice state becomes `rejected` and an alert
  is raised, and the fix is a credit note plus a corrected re-issue: the original number is never reused.
- A SEPA transfer arrives with a mangled reference; the bank feed creates a payment, a human allocates it, and
  the invoice becomes `paid`.

**Retained client: alert to ticket to fix to report.**

- Probes in two regions see `verdane.example.com` return 502 on three consecutive checks and a third region
  agrees; the alert is confirmed and opens a `p1` ticket, skipping triage.
- SLA timers start; because `p1` targets are around the clock for this retainer, the `24x7` calendar applies
  instead of the French office calendar.
- The on-call developer needs the hosting credential and opens a vault access request bound to the ticket with
  a justification; out of hours this is break-glass, a second approver is paged and approves, step-up is
  performed, the secret is revealed for 30 minutes, and the read is logged before the value is returned.
- The fix is applied, the ticket moves to `resolved` and the timer stops.
- The client sees the incident on the sites page with its duration, and the next monthly report shows uptime
  including it, plus an honest gap marker for the minutes when the agency's own probe network was degraded.

**Enterprise onboarding: SSO, SCIM, approval routing.**

- A `client_owner` starts SSO setup with the IdP metadata URL.
- They prove domain ownership with a DNS TXT record; verification is polled, and until it is confirmed no
  assertion from that IdP is accepted for the domain.
- Group mappings are configured: `dc-approvers` to `client_approver`, `dc-finance` to `client_finance`.
- SCIM is enabled with a token stored in the vault; the IdP pushes 40 users, and roles derive from groups on
  every push and login.
- Approval routing is configured against org units rather than named individuals.
- Months later a user leaves; SCIM propagates within seconds, every session, membership and grant is revoked,
  and the next reconciliation confirms zero drift.

**Client exit.**

- The client gives 60 days' notice; the contract moves toward `terminated` on the notice date and the exit
  checklist is scheduled.
- Final invoices issue, and unbilled approved milestones are surfaced so nothing is written off by accident.
- Handover transfers credentials through a one-time secure channel, the client confirms receipt in the portal,
  and the agency's copies are crypto-shredded by destroying the organisation's key, recorded on the exit
  certificate.
- Connectors are revoked at Google and Meta, not merely locally, and the revocation responses are stored.
- A portability export is generated and available for 30 days.
- Portal access ends; audit records stay under the retention policy, which outlives the relationship, and the
  client is told exactly what is retained and for how long.

### Critical edge cases

Each states the situation and the required behaviour; where a naive behaviour is tempting, it is named.

| ID | Situation | Required behaviour |
|---|---|---|
| EC-01 | two finance admins issue the same draft invoice at the same moment | the issues are serialised: one assigns the number, the other sees the invoice already issued and is refused with `409` and code `invoice_not_draft`; wrong would be two numbers, or one number twice |
| EC-02 | a client approves a deliverable at the exact moment a new version is uploaded | the upload cancels the pending approval, and the approval attempt is refused with `409` and code `approval_superseded` naming the new version; wrong would be approving a version the approver never saw |
| EC-03 | an approver's membership is revoked while an approval is pending on them | the step re-resolves by the assignee order and the client is told routing changed; wrong would be a permanently blocked workflow, or auto-approval |
| EC-04 | two client orgs claim the same email domain for SSO | the domain is globally unique; the second claim fails and escalates to the `security_officer`; wrong would be last writer wins, a cross-tenant takeover |
| EC-05 | a user belongs to two client orgs, such as a group and its subsidiary | one principal, two memberships; every request is scoped by the active org and the audit records the org context; wrong would be duplicate principals, or org A's data in org B's view |
| EC-06 | VIES is down when an invoice must be issued for an EU business | use a validation under 90 days old, otherwise refuse with a clear reason; wrong would be defaulting to a zero rate because the check timed out |
| EC-07 | a payment arrives for more than the invoice total | allocate up to the invoice and hold the remainder as unallocated credit on the organisation, visible in the portal; wrong would be marking the invoice overpaid, or silently absorbing it |
| EC-08 | a time entry is approved after its period was locked and invoiced | it rolls into the next billing period with a link to the closed one; wrong would be mutating a closed period behind an issued invoice |
| EC-09 | a contractor's grant expires mid-task with an unsaved comment | the decision point denies at expiry; the UI says access to the project ended, keeps the draft locally and offers an extension request; wrong would be a server error or lost work |
| EC-10 | a client's GA4 property is disconnected by their own admin | the connector goes `revoked`, reports for affected periods show an explicit data gap, and a task is raised; wrong would be reporting zeros as if traffic collapsed |
| EC-11 | a single monitoring region has a network fault | no alert until 2 of 3 regions agree across 3 checks; wrong would be paging a client at 03:00 for a probe blip |
| EC-12 | a monitored client site is defaced and its content hash changes | a `critical` `defacement_suspect` alert, the diff captured as evidence, a ticket opened, and the agency told before the client |
| EC-13 | a DSR erasure request comes from someone who is also a contract signatory | erase marketing and behavioural data, retain contractual and accounting records under legal obligation, and state exactly what was retained and why; wrong would be deleting invoice records, or refusing the whole request |
| EC-14 | the same person applies for a job and is also a client contact | two distinct records with different retention classes and no cross-linking; recruitment cannot see client data and the reverse |
| EC-15 | a lead is submitted twice within seconds by a double click or retry | the idempotency key returns the original result; a genuine second submission an hour later becomes a linked duplicate, not a merged record |
| EC-16 | an approval policy is edited while approvals are in flight | in-flight approvals continue under their pinned policy version; wrong would be retroactive rule changes |
| EC-17 | a client requests deletion of a deliverable containing a third party's IP | soft-delete keeping the audit trail, crypto-shred the file only after the contractual retention window, and record the request |
| EC-18 | a slug changes on a published case study | the old path becomes a permanent `301` automatically, the sitemap regenerates and alternates update; wrong would be a `404` on an address with inbound links and rankings |
| EC-19 | a generated service by city landing page is too similar to its siblings | it stays `noindex` and is queued for a writer; wrong would be publishing a doorway grid from an agency that sells SEO |
| EC-20 | a visitor withdraws consent after accepting | tags unload without a reload where possible, the consent record updates, `gclid` and attribution collected under the prior consent are deleted, and nothing further is collected |
| EC-21 | the e-signature provider sends `completed` before `delivered` | events are processed by envelope state, not arrival order, and reconciled rather than rejected |
| EC-22 | two people edit the same content localisation | the stale write is refused with `409` and code `version_conflict` carrying the current version; no silent overwrite |
| EC-23 | an agency employee leaves on a Friday evening | deprovisioning revokes sessions and grants at once, and every secret they revealed in the last 30 days is flagged with rotation tasks created |
| EC-24 | a break-glass request is made by the only available approver | it cannot self-approve; escalation reaches the `security_officer` and then `group_admin`, and with no second principal reachable access is denied and the incident recorded, never overridden automatically |
| EC-25 | clock skew or a DST transition during an SLA window | timers compute in UTC against calendars with explicit zones, and DST transitions for France and Malta both hold |
| EC-26 | a client uploads a 40 megabyte PSD to a PDF-only field | the client-side rejection is a hint, the upload slot enforces the content-length range, the server re-validates, and the error names the limit `Max. file size : 8MB` |
| EC-27 | the WebGL context is lost on the public site mid-scroll | the DOM layer is revealed, the page stays fully navigable, and there is no restore loop |
| EC-28 | a search query would match a resource the principal cannot read | permission filtering happens inside the query, and result counts never reveal inaccessible records |

### Security

**Threat model**, assets ranked by what their loss costs:

| Rank | Asset | Loss scenario | Blast radius |
|---|---|---|---|
| 1 | client production credentials | vault compromise | 400 businesses; existential for the agency |
| 2 | authorisation integrity | privilege escalation | cross-tenant data exposure; contractual breach |
| 3 | audit trail integrity | tampering | every dispute unwinnable; a regulatory finding |
| 4 | financial records | manipulation | fraud, tax exposure, unreconcilable books |
| 5 | client personal data | breach | Article 33 and 34 notification, client contract termination |
| 6 | public site integrity | defacement or injected script | reputational, and supply-chain risk to visitors |

Principal adversaries: an external attacker seeking the vault through the public site or a phished employee; a
departed contractor with lingering access; a malicious or careless insider; a client principal reaching for
another client's data; an automated credential-stuffing or form-spam operation.

**Application security baseline:**

| Control | Requirement |
|---|---|
| Transport | TLS 1.3, HSTS with preload on all hosts, no mixed content |
| CSP | strict and nonce-based: `default-src 'self'`, no `unsafe-inline`, no `unsafe-eval`, an explicit allow-list for the tag manager gated by consent, `frame-ancestors 'none'` except the deliverable preview frame, which uses a sandboxed dedicated origin |
| Headers | `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, a `Permissions-Policy` denying camera, microphone and geolocation, `Cross-Origin-Opener-Policy: same-origin` |
| CSRF | a double-submit token on every cookie-authenticated state change, and no state change on a `GET`, ever |
| Injection | parameterised queries only, no string-built SQL, raw query escapes reviewed |
| XSS | context-aware escaping at render; raw HTML only through a sanitised rich-text renderer with an allow-list |
| SSRF | the build URL preview and any client-supplied URL fetch go through an allow-listed proxy with DNS-rebinding protection and no access to link-local or private ranges |
| Deserialisation | JSON only; no native object deserialisation from untrusted input |
| Dependencies | composition analysis, pinned lockfiles, an SBOM per release, automated patch proposals, a documented 7-day SLA on critical advisories |
| Secrets in delivery | federated deploy credentials, no long-lived cloud keys, secret scanning on every push and on history |
| Uploads | the upload safety path above, in full |
| Admin surface | `/portal/agency/admin` routes require step-up and are restricted to the offices' egress ranges plus the VPN |

The old public WordPress attack surface is retired: no `xmlrpc.php`, no `wp-json`, no plugin-authored endpoints.
The public site is a renderer with no writable surface except the three rate-limited, anti-abused form endpoints.

**Multi-tenancy enforcement, three ways:** the decision point denies; row-level security filters by the
session's organisation scope; and an enumeration of every route authenticates as a principal from organisation
A and requests every resource id from organisation B, expecting `404` with no timing difference, so a new route
without a case is an incomplete route.

**Existence disclosure.** Denied and non-existent are indistinguishable: same status, same body, same headers,
and a latency envelope that does not leak. This applies to resource reads, search, the SSO email resolver (rate
limited, returning a generic path for unknown domains) and magic-link requests, which always report that a link
was sent if the address exists.

**Rate limits and quotas:**

| Scope | Limit |
|---|---|
| Public form endpoints | as stated for anti-abuse |
| Auth endpoints | 10 per minute per address, 5 per minute per email, exponential lockout with alerting on distributed patterns |
| Authenticated API, per principal | 600 per minute sustained, burst 100 |
| Per client org | 3 000 per minute aggregate, so one org's integration cannot starve others |
| Vault reveal | 10 per principal per hour; exceeding it alerts rather than only refusing |
| Export endpoints for CSV, audit and portability | 5 per hour per principal, always audited |
| Outbound webhook delivery | 20 per second per endpoint with backpressure |
| Beacon ingest | 100 per second per site, then sampled |

Limits are token buckets in PostgreSQL-backed counters; a limiter failure fails closed for auth and vault and
open for read paths, chosen per endpoint rather than globally. Per-address limits exempt private and loopback
source addresses, as stated for anti-abuse.

**Incident response.** Detection feeds from audit anomalies (a principal reading 20 secrets in an hour),
failed-auth spikes, chain-verification failure, CSP violation reports, dependency advisories and client-site
monitoring alerts. SEV-1 is a suspected vault compromise, confirmed cross-tenant exposure, or a client site
compromised through agency-held access; SEV-2 is portal unavailability or one client's data exposed to one wrong
party; SEV-3 is degraded function. A SEV-1 involving client credentials triggers a standing playbook: revoke all
sessions, freeze vault reveals, rotate every secret that principal could reach, notify affected clients within
the contractual window, and preserve the audit chain segment as evidence. Breach notification obligations under
Article 33 (the supervisory authority within 72 hours) and Article 34 (data subjects without undue delay) are
tracked with a clock in the DSR and incident module; as a processor for client data, the agency notifies the
controller without undue delay and the contract's timeline governs.

### Compliance and data governance

**The agency's two hats:**

| Hat | When | Obligations |
|---|---|---|
| Controller | its own leads, applicants, contacts, staff and site analytics | lawful basis, transparency, DSRs, retention, security |
| Processor | client customer data reached through CRM and marketing automation work, client analytics, client site databases | an Article 28 contract, acting only on instructions, sub-processor consent and notification, assisting with DSRs, breach notification to the controller, deletion or return at the end of service |

The distinction is recorded per processing activity and per DSR, because the response differs: as controller
the agency answers the data subject; as processor it routes the request to the client and assists.

**Data minimisation, applied:**

- raw addresses are never stored; leads and consent records keep a salted hash plus a country code, with the
  salt rotating monthly so the hash is not a durable identifier;
- no behavioural tracking in the portal; product analytics, if any, are aggregated event counts, never per
  named user;
- personal data never enters logs; a redaction layer strips known-sensitive keys before emission, and a request
  carrying a synthetic canary email produces no log line containing it;
- personal data in error tracking is scrubbed at the source, with allow-listed fields only.

**Consent, done properly** rather than as a banner on the page:

- no non-essential tag loads before a decision, and the tag manager container itself is not loaded until
  consent state is known; essential functional storage (session, consent record, CSRF) is exempt and
  documented;
- server-side state is authoritative: the banner records the decision on the server, which sets a signed,
  httpOnly consent cookie that the tag loader reads, never a local flag a user could not audit;
- granular purposes, functional, analytics, marketing and personalisation, each accepted or rejected
  independently, with reject-all as prominent as accept-all, as CNIL requires;
- re-prompting at most every 13 months, and immediately on a material policy change;
- withdrawal as easy as granting, through a persistent preference-centre link in the footer of both sites at
  `/cookies/` and `/fr/cookies/`;
- proof: consent records keep purposes, policy version, method and timestamp, and the weekly crawl with consent
  denied fails the deploy if any non-essential request fires;
- **consent gates the data model, not just the tags**: without marketing consent no `gclid` is captured,
  attribution keeps only a channel bucket, and no offline conversion export happens.

**Data subject requests:**

- intake from a form on both sites, from the contact addresses and from the portal;
- identity verification proportionate to the request: a link to the verified email for access, stronger for
  erasure of a portal account;
- fan-out search across leads, contacts, principals, tickets, annotations, time entries, audit, attachments,
  CVs, deliverables, hashed session data, the search index, the email provider and the backup catalogue, with
  each system searched recorded, and an unrecorded system treated as unsearched;
- erasure distinguishes what must go from what must stay: contractual and accounting records are retained under
  legal obligation, marketing and behavioural data erased, and the response itemises both;
- denormalised copies are covered: cached, indexed, exported and backed-up copies are enumerated; backups age out
  rather than being rewritten, the erasure record states when the last backup copy expires, and a suppression
  list prevents restoring erased subjects;
- a 30-day clock with escalation at 20 days and a documented extension path.

**Tax, invoicing and accounting compliance:**

| Requirement | Implementation |
|---|---|
| Gapless, immutable numbering per entity and year | the numbering invariant, verified nightly |
| Inalterability of issued documents | no update path; corrections are credit notes; stored PDFs are never rewritten |
| Audit trail of accounting entries | the audit chain covers every finance change with actor, time and before and after |
| French e-invoicing | Factur-X (PDF/A-3 with CII XML) through a registered platform; Chorus Pro for public buyers with SIRET, service code and engagement number |
| Maltese requirements | local numbering, the VAT number on the face, statutory content per the Maltese VAT Act |
| Intra-EU reverse charge | the treatment matrix, with VIES evidence retained including the consultation number |
| Retention | accounting records kept for the longer of the two jurisdictions' requirements, 10 years, enforced by retention class |

**Data residency and sub-processors:**

- all primary data stays in the EU, stated in the DPA and verifiable from the infrastructure code;
- every sub-processor is registered with purpose and location, and the register is exposed in the portal and on
  a public page;
- adding a sub-processor notifies affected clients with a defined objection window under Article 28(2), and a new
  data-handling vendor without a register entry is an incomplete change;
- any transfer outside the EU requires SCCs and a documented transfer impact assessment, and the default is an
  EU-region alternative.

**Retention schedule:**

| Class | Data | Retention | Basis |
|---|---|---|---|
| `lead_unconverted` | leads never converted | 24 months from last contact | legitimate interest |
| `lead_spam` | spam-scored submissions | 30 days | security |
| `applicant` | CVs, cover letters, application data | 24 months from application, longer only with explicit talent-pool consent | consent or legitimate interest, CNIL guidance |
| `client_commercial` | contracts, proposals, change orders | 10 years after contract end | legal obligation |
| `accounting` | invoices, credit notes, payments | 10 years | legal obligation |
| `delivery` | deliverables, annotations, project data | contract end plus 3 years, then client-directed | contract |
| `credentials` | vault secrets | destroyed at handover by crypto-shredding | security |
| `audit_standard` | audit events for `standard` orgs | 12 months | accountability |
| `audit_enterprise` | audit events for `enterprise` and `public_sector` orgs | 7 years | contract and accountability |
| `telemetry` | site checks and vitals | 400 days | service |
| `consent` | consent records | 3 years after withdrawal or expiry | proof of compliance |
| `webhook_raw` | raw inbound payloads | 30 days | operations |

The retention sweep enforces the schedule, and its first live run follows a dry-run report a human signs off,
because an over-eager retention job is itself a data-loss incident.

### Performance, scalability, availability

**Load model**, derived from the measured scale of 400 clients, 20 employees and 3 offices, stated as assumptions
because no analytics access was available:

| Dimension | Assumption |
|---|---|
| Public site sessions | 30 000 per month across both sites, peaking five times during campaigns |
| Form submissions | 150 to 400 per month, bursty around campaigns |
| Portal principals | about 1 200 client principals, about 150 monthly actives |
| Agency principals | 20, near-continuous in business hours |
| Managed sites monitored | 400 at 60 or 300 second intervals, about 4.5 million checks a day |
| Vitals beacons | about 2 million a day at 10 per cent sampling across managed sites |
| Connector API calls | about 5 000 a day across 400 clients, concentrated at night |
| Deliverable storage | about 2 TB, growing about 40 GB a month |
| Invoices | about 250 a month across both entities |

The system is not high-throughput on the transactional path; it is high-throughput on one path, monitoring
ingest, isolated behind its own runners so its bursts never degrade an approval.

**Public site budgets:** p75 LCP on 4G mid-tier mobile at most 2.5 seconds; p75 INP at most 200 milliseconds; CLS
at most 0.05; TTFB from the edge at most 200 milliseconds; first-load JavaScript on the home route at most 180
KB compressed excluding WebGL; the WebGL bundle lazy, at most 120 KB compressed, loaded after LCP and never on
mobile; hero image payload at most 250 KB at 1x desktop; at most 2 font families and 4 files with
`font-display: swap`, subset and preloaded.

**Portal and back office budgets:** p95 API read at most 300 milliseconds; p95 write at most 600; p95
authorisation decision at most 15 cached and 60 cold; overview interactive within 1.5 seconds warm; a 50-row
filtered grid within 400 milliseconds of server time; the first page of a 20 MB PDF within 2 seconds
progressively; one client's monthly report within 90 seconds.

**Database discipline:** every listing query has a supporting index and a verified plan for the twelve
highest-traffic queries; no N+1 in any list endpoint, a request issuing more than 15 queries being a defect;
keyset pagination everywhere; statement timeouts per role, lower for interactive sessions than for jobs.

**Scalability posture:** the core API is stateless and horizontally scalable, with sessions and rate limits
outside the process; job runners scale by queue class, `interactive` (approval timers, notifications), `batch`
(reports, syncs) and `ingest` (monitoring), so a report backlog never delays an SLA timer; PostgreSQL scales
vertically first with a replica for reporting and grids, partitioning only where volume justifies it (audit
events by month, webhook receipts by week); telemetry is partitioned monthly with a 400-day TTL and daily rollups,
so the uptime strip reads a rollup; large objects live outside the relational rows.

**Availability and failure handling:**

| Component | Target | Degradation |
|---|---|---|
| Public sites | 99.95 per cent | cached HTML serves even when the origin and core API are down; a stale page beats an error page |
| Portal and API | 99.9 per cent in business hours | read-only mode on primary failover: reads from the replica, writes refused with a clear banner and retry, never silently queued |
| Vault | 99.9 per cent, failing closed | if the vault is unavailable, secrets cannot be read, and there is no fallback |
| Monitoring ingest | best effort | backpressure and sampling; a dropped beacon is acceptable, a dropped alert is not, so alert evaluation runs on the check path |
| E-invoicing | asynchronous | queued with retries; invoices stay valid and issued while transmission is pending |
| Email | 99.9 per cent | queued and retried; the in-app notification is written first so the record exists even if the email never arrives |

Backups: continuous archiving with point-in-time recovery over 35 days, versioned object storage, daily telemetry
snapshots, and a restore rehearsed quarterly against a scratch environment with the RTO of 4 hours and RPO of 5
minutes recorded from the rehearsal; an untested backup is a hypothesis. Every outbound integration sits behind a
circuit breaker with a per-provider budget, so an open breaker degrades one feature (an unreachable VIES blocks
issues with an explanatory error) and never cascades, and every network call has an explicit timeout: 5 seconds
on interactive paths, 30 for jobs, none unbounded.

### Observability

**Structured logging**: JSON to stdout, one event per line, with `timestamp`, `level`, `service`, `version`,
`request_id`, `trace_id`, `principal_id`, `principal_kind`, `client_org_id`, `route`, `duration_ms` and
`outcome`; personal data redacted at emission by a reviewed allow-list, not an ad hoc pattern.

**Tracing and metrics**: OpenTelemetry throughout, with spans on handlers, authorisation decisions, query
groups, external calls, jobs and policy evaluations, and trace context carried into jobs through the outbox, so an
approval and the invoice drafted twenty minutes later share a correlation id and read as one causal chain. RED
metrics on every endpoint and job, USE metrics on every resource, and business metrics emitted as telemetry
(leads by source and entity, SLA breaches, approval cycle time, invoice issue latency, e-invoice rejection rate,
vault reveals by principal, connector health, and the sixteen success metrics). `client_org_id` is a metric label
only where per-tenant visibility is required (SLA, connector health, ingest volume), never on generic HTTP
metrics.

**Real-user monitoring** on both public sites and the portal, sampled and consent-gated, reporting Core Web
Vitals by route, device class and country: the same vitals pipeline that reports on client sites reports on the
agency's own, side by side on the internal dashboard.

**Alerting and SLOs:**

| SLO | Target | Alert |
|---|---|---|
| Portal API availability | 99.9 per cent over 30 days | multi-window burn rate, 2 per cent in 1 hour and 5 per cent in 6 hours |
| Public site availability | 99.95 per cent | synthetic checks from 3 regions |
| p95 API latency | at most 500 milliseconds | sustained 15 minutes |
| Interactive job queue age | at most 60 seconds | page at 5 minutes |
| Outbox lag | at most 30 seconds | page at 5 minutes |
| Audit chain verification | 100 per cent pass | an immediate page, SEV-1 |
| Invoice sequence integrity | 100 per cent pass | an immediate page to finance and engineering |
| Consent violations | zero | blocks deploy and alerts |
| Connector failure rate | at most 5 per cent | a ticket, not a page |
| Vault reveal anomaly | statistical | pages the `security_officer` |

Every alert names an owner and links to a runbook; an alert without one is deleted at the next review, because an
alert nobody knows how to action trains a team to ignore alerts.

**Audit as an observability surface**: the audit log is queryable by actor, resource, organisation and time in the
back office, with saved investigations and a signed export for a client or regulator, and client principals see
the audit trail of their own organisation's actions in the portal: who approved what, when and from where.

### API conventions

JSON over HTTPS under `/api` on the app's own origin; the reference's `/v1/` prefix is `/api` here.

| Concern | Rule |
|---|---|
| Versioning | the prefix is the version; breaking changes ship a new prefix, additive changes do not |
| Auth | `Authorization: Bearer <access_token>` for API clients; the browser uses the httpOnly session cookie plus a double-submit CSRF token on state changes |
| Idempotency | required on every `POST` that creates a durable side effect where this contract says so, through the `Idempotency-Key` header, stored 24 hours with the response and keyed by principal or form, endpoint and key; a replay with the same body returns the original status and body, and the same key with a different body is refused with `409` and code `idempotency_key_reused` |
| Concurrency | every mutable resource carries a monotonic `version`, which an update names; a stale write is refused with `409` and code `version_conflict` carrying `current_version`, never last write wins |
| Pagination | keyset only, `limit` and `cursor`, with the next cursor returned alongside the page; no total count on unbounded collections |
| Filtering | explicit allow-listed query parameters only, no query language from the client |
| Errors | `application/problem+json` with `type`, `title`, `status`, `detail`, `code` (the machine string named throughout this brief), `request_id`, and for validation `errors`, a list of `{"field", "code"}` |
| Rate limits | `RateLimit-Limit`, `RateLimit-Remaining` and `RateLimit-Reset` on every response; `429` with `Retry-After` and code `rate_limited` |
| Tracing | `traceparent` accepted and propagated; `request_id` on every response including errors |
| Time | RFC 3339 UTC instants everywhere; no local time crosses the wire |
| Money | integer `amount_minor` fields in euro cents, never a decimal string or a float |
| Field names | snake_case in every request, response, row and event: `version_id`, never `versionId`; the event envelope's `event_id`, `occurred_at`, `aggregate_type` and `aggregate_id` are never `eventId`, `occurredAt`, `aggregateType` or `aggregateId` |

**A denied read answers exactly as a missing resource**: `404` with code `not_found`, the same `detail`
(`Not found, or you do not have access`), the same headers and the same latency envelope. A call needing a
principal without one is refused with `401` and code `unauthenticated`. A principal whose grants do not permit a
call on a resource it can see is refused with `403` and code `forbidden`, and the protected state is unchanged.
An unknown path under `/api` answers `404` with code `not_found`.

### The endpoint catalogue

The reference's load-bearing endpoints, with the method and path each takes here:

| Area | Calls |
|---|---|
| Public, unauthenticated | `POST /api/public/leads` for the three intake forms, idempotent, anti-abused, consent recorded, `202` with a reference; `POST /api/public/uploads` a two-step single-object upload slot then confirm, never a direct multipart post; `POST /api/public/applications` for the application funnel with its own retention class; `GET /api/public/content/{site}/{locale}/{path}` read-only content for the renderer, cached with ETags; `POST /api/public/consent` records a consent decision and returns the signed consent state; `POST /api/public/vitals` a web-vitals beacon signed with the site key |
| Identity | `POST /api/auth/login`; `POST /api/auth/step-up`; `POST /api/auth/refresh` rotating refresh with reuse detection; `DELETE /api/auth/session`, with `all=true` revoking every session of the principal; `GET /api/auth/idp/resolve` returning which IdP handles a verified domain or the generic path, hard rate limited as an enumeration surface; the OIDC callback and SAML assertion consumer; SCIM 2.0 `Users` and `Groups` under `/api/scim/v2` with a per-IdP bearer token |
| Organisations and members | `GET /api/orgs`, `GET /api/orgs/{id}`, `PATCH /api/orgs/{id}`, `GET /api/orgs/{id}/members`, `POST /api/orgs/{id}/members`, `DELETE /api/orgs/{id}/members/{principal_id}` |
| CRM and commerce | `GET /api/leads`, `POST /api/leads/{id}/transition`, `GET /api/opportunities`, `POST /api/opportunities/{id}/stage`, `GET /api/proposals`, `GET /api/proposals/{id}`, `POST /api/proposals/{id}/send`, `POST /api/proposals/{id}/duplicate`, `POST /api/proposals/{id}/decision`, `GET /api/contracts`, `GET /api/contracts/{id}`, `POST /api/contracts/{id}/sign-request`, `POST /api/contracts/{id}/change-orders`, `POST /api/change-orders/{id}/submit`, `POST /api/change-orders/{id}/decision` |
| Delivery and review | `GET /api/projects`, `GET /api/projects/{id}`, `GET /api/projects/{id}/burn`, `POST /api/projects/{id}/milestones`, `GET /api/milestones/{id}`, `POST /api/milestones/{id}/submit`, `POST /api/projects/{id}/deliverables`, `GET /api/deliverables/{id}`, `POST /api/deliverables/{id}/versions`, `POST /api/deliverables/{id}/share`, `GET /api/deliverables/{id}/annotations`, `POST /api/annotations`, `PATCH /api/annotations/{id}`, `GET /api/approvals`, `GET /api/approvals/{id}`, `POST /api/approvals/{id}/decisions`, `POST /api/approvals/{id}/delegate`, `POST /api/approvals/{id}/cancel` |
| Time, tickets, finance | `GET /api/time-entries`, `POST /api/time-entries/bulk`, `POST /api/time-entries/{id}/submit`, `POST /api/time-periods/{id}/lock`, `GET /api/tickets/{id}`, `POST /api/tickets/{id}/transition`, `GET /api/invoices`, `POST /api/invoices`, `GET /api/invoices/{id}`, `POST /api/invoices/{id}/issue`, `POST /api/invoices/{id}/credit-note`, `POST /api/invoices/{id}/dispute`, `GET /api/payments`, `POST /api/payments/{id}/allocate` |
| Sites, reports, governance | `GET /api/sites/{id}/health`, `POST /api/sites/{id}/handover`, `GET /api/reports/{id}`, `POST /api/report-definitions/{id}/run`, `GET /api/audit-events`, `POST /api/audit-events/export`, `GET /api/dsrs`, `POST /api/dsrs/{id}/fulfil`, `POST /api/grants`, `DELETE /api/grants/{id}`, `POST /api/authz/decisions` |
| Content | `GET /api/content/entries`, `PATCH /api/content/localisations/{id}` |
| Vault | `GET /api/vault/secrets` metadata only, never ciphertext or a value; `POST /api/vault/access-requests`; `POST /api/vault/access-requests/{id}/approve`; `POST /api/vault/secrets/{id}/reveal`, which needs an approved request and step-up and is single use; `POST /api/vault/secrets/{id}/rotate`; `DELETE /api/vault/secrets/{id}`, crypto-shredding, irreversible, two-person; `POST /api/vault/secrets/export`, which exists only to refuse; `GET /api/vault/access-log`; `POST /api/vault/access-log/verify` |

There is deliberately no call returning a secret's plaintext outside the single-use reveal, and no list returning
more than metadata.

### The contract, call by call

Shapes a client may rely on. Anything unlisted is yours to design, and every refusal carries the `code` named.
Every list call below answers a top-level JSON array of at most `limit` rows, `limit` defaulting to `500`; when
more rows match, the keyset cursor for the next page is in the `Next-Cursor` response header.

**Sessions**

| Call | Body | Answer |
|---|---|---|
| `POST /api/auth/login` | `{"email", "password"}` | `200` `{"access_token", "expires_at", "principal_kind"}` where `principal_kind` is `agency`, `client` or `external`; a wrong pair is `401` `invalid_credentials` |
| `POST /api/auth/step-up` | `{"password"}` | `200` `{"step_up_at"}`; a wrong password is `401` `invalid_credentials` |
| `GET /api/health` | none | `200` |

**Intake**

`POST /api/public/leads` needs no session and requires an `Idempotency-Key` header; without one it is refused
with `422` and code `idempotency_key_required`.

| Field | Rule |
|---|---|
| `form` | `start_a_project` or `say_hello` |
| `site` | `en` or `fr`, the site the form was submitted on |
| `first_name`, `last_name`, `email`, `phone` | required |
| `company_name` | optional |
| `company_country` | required, ISO 3166 alpha-2 |
| `budget` | required for `start_a_project`: `band_10_20k`, `band_20_30k`, `band_30_60k` or `band_60k_plus` |
| `kind` | required for `start_a_project`: `website`, `website_with_seo_sea`, `digital_campaign`, `seo`, `ux_webdesign`, `branding` or `full_project` |
| `message` | required |
| `consent` | must be `true` |
| `marketing_consent` | `true` or `false` |
| `gclid` | optional |
| `website` | the hidden decoy field a person never fills, sent empty |

It answers `202` with `{"reference"}`. A body failing validation is refused with `422` and `errors` naming each
field with code `required`, `invalid_email`, `invalid_choice` or `consent_required`, and stores nothing. A filled
`website` field answers `202` with a reference exactly like an accepted lead, stores the lead with status `spam`
and sends nothing. Every lead is a row of the `leads` table with its `reference`, `email`, `status`, `budget`,
`kind`, `entity` (`parallax-france` or `parallax-malta`) and `gclid`, which is `NULL` unless `marketing_consent`
is `true`.

Each lead that is not spam sends exactly one confirmation email to its `email`, from the handling entity's
contact address, in the language of the site it was submitted on. An English-site confirmation has the subject
`Parallax: we received your brief ` followed by the reference; a French-site confirmation has the subject
`Parallax : demande reçue ` followed by the reference. The first line of the body is the handling entity's name,
`Parallax Malta Ltd` or `Parallax France SAS`, on its own, then the reference and the expected response time.

**Organisations and projects**

| Call | Query or body | Answer |
|---|---|---|
| `GET /api/orgs` | `slug` | an array of `{"id", "slug", "legal_name", "kind", "country", "governance", "billing_entity"}` the caller may see |
| `GET /api/projects` | `code` | an array of `{"id", "code", "name", "status", "client_org_id"}` the caller may see |
| `GET /api/projects/{id}` | none | `200` `{"id", "code", "name", "status", "client_org_id"}` |
| `POST /api/projects/{id}/milestones` | `{"name", "bill_amount_minor"}` | `201` `{"id", "name", "status", "bill_amount_minor", "billing_trigger", "approved_at", "invoice_id"}` with status `not_started` and trigger `on_approval` |
| `GET /api/milestones/{id}` | none | `200`, the milestone in that shape |
| `POST /api/projects/{id}/deliverables` | `{"name", "kind", "milestone_id"}` | `201` `{"id", "name", "kind", "status", "current_version_id", "milestone_id", "client_org_id"}` with status `draft` |
| `GET /api/deliverables/{id}` | none | `200`, the deliverable in that shape |

Milestones and deliverables are created by the project's project manager or account director, or a group admin.

**Review and approval**

| Call | Body | Answer |
|---|---|---|
| `POST /api/deliverables/{id}/versions` | `{"notes"}` | `201` `{"id", "version", "uploaded_by_email"}`; the version becomes current, and a pending approval on the deliverable becomes `cancelled` |
| `POST /api/deliverables/{id}/share` | none | `201`, the approval; `422` `version_required` when the deliverable has no version |
| `GET /api/approvals/{id}` | none | `200`, the approval |
| `GET /api/approvals` | `assignee=me` | an array of the pending approvals whose current stage names the caller |
| `POST /api/approvals/{id}/decisions` | `{"decision", "comment", "version_id"}` with `decision` `approved` or `rejected` | `200`, the approval after the decision |

An approval is `{"id", "state", "current_stage", "value_minor", "version_id", "subject_id", "stages"}`, where
`value_minor` is the linked milestone's bill amount, `current_stage` is the number of the stage now open counting
from `1`, and `state` is `pending`, `approved`, `rejected` or `cancelled`. Each stage is `{"stage", "mode",
"state", "assignees", "decisions"}`, where `stage` is its number, `assignees` lists the email of every principal who may decide that stage and each decision is
`{"decided_by_email", "decision", "comment", "on_behalf_of_email"}`. The version uploaded by project staff,
producers and account directors may be shared by the project manager or account director.

A decision is checked in this order, and the first failing check answers:

| Check | Refusal |
|---|---|
| the approval exists and the caller may see it | `404` `not_found` |
| the approval was cancelled by a newer version, or `version_id` is not the approval's version | `409` `approval_superseded` with `{"current_version_id"}` |
| the approval is still `pending` | `409` `approval_not_pending` |
| the caller is an assignee of the current stage | `403` `forbidden` |
| the caller did not upload the version under review | `403` `separation_of_duties` |
| the caller's approval threshold is at least the approval's value | `403` `approval_threshold_exceeded` |
| a rejection carries a comment | `422` `comment_required` |

A refused decision records nothing and changes nothing. A principal repeating a decision already recorded for the
current stage gets `200` with the approval unchanged, so a double submit is one decision. When the last stage
completes, the approval is `approved`, the deliverable `approved`, the milestone `approved` with `approved_at`,
and within ten seconds exactly one draft invoice exists for the milestone, its id on the milestone's `invoice_id`.

**Commerce**

| Call | Body or query | Answer |
|---|---|---|
| `GET /api/proposals` | `client_org_id` | an array of `{"id", "version", "status"}`; client principals see only proposals that were sent |
| `GET /api/proposals/{id}` | none | `200` `{"id", "version", "status", "subtotal_minor", "discount_minor", "total_minor", "margin_minor", "lines"}` with each line `{"position", "kind", "description", "role", "quantity", "unit", "unit_price_minor", "cost_price_minor", "amount_minor"}` |
| `GET /api/contracts` | `client_org_id` | an array of contracts |
| `GET /api/contracts/{id}` | none | `200` `{"id", "reference", "status", "client_org_id", "value_minor", "original_value_minor", "currency"}` |
| `POST /api/contracts/{id}/change-orders` | `{"reason", "delta_value_minor"}` | `201` `{"id", "sequence", "status", "delta_value_minor"}` with status `draft` |
| `POST /api/change-orders/{id}/submit` | none | `200` with status `client_review` |
| `POST /api/change-orders/{id}/decision` | `{"decision", "comment"}` | `200` with status `approved` or `rejected`; `409` `change_order_not_in_review` when not in review |

`margin_minor` and every line's `cost_price_minor` are **absent from the body**, not `null`, for every caller
without commercial visibility: client principals, and project managers and producers holding no
`commercial_visibility` grant. Change orders are raised by the account director or project manager and decided by
the client's owner, or by a client approver whose threshold covers the absolute delta; others are refused with
`403` `forbidden`. At every instant a contract's `value_minor` equals its `original_value_minor` plus the deltas of
all its approved change orders, however many are approved at the same moment.

**Finance**

| Call | Body or query | Answer |
|---|---|---|
| `POST /api/invoices` | `{"client_org_id", "lines", "po_number"}`, each line `{"description", "quantity", "unit_price_minor"}`; any total sent is ignored | `201`, the invoice, status `draft`, number `null` |
| `GET /api/invoices/{id}` | none | `200`, the invoice |
| `GET /api/invoices` | `agency_entity`, `doc_type`, `milestone_id` | an array of invoices the caller may see |
| `POST /api/invoices/{id}/issue` | none | `200`, the issued invoice |
| `POST /api/invoices/{id}/credit-note` | `{"reason"}` | `201`, the credit note |

An invoice is `{"id", "doc_type", "status", "number", "agency_entity", "client_org_id", "milestone_id",
"issue_date", "tax_treatment", "tax_rate_bp", "tax_note", "subtotal_minor", "tax_minor", "total_minor",
"po_number", "einvoice_channel", "credits_invoice_id", "lines"}`, where `doc_type` is `invoice` or `credit_note`,
`agency_entity` is the entity slug, and each line is `{"position", "description", "quantity", "unit_price_minor",
"amount_minor"}`. Drafts are created and issued by a `finance_admin` of the client's billing entity or a
`group_admin`; a draft for a milestone is created by the billing job.

Issuing is checked in this order: the caller may issue for that entity (`403` `forbidden`); a step-up no older
than 15 minutes (`403` `step_up_required`); the invoice is a `draft` (`409` `invoice_not_draft`); tax
determination (`422` `vat_number_invalid` or `422` `vat_validation_stale`); a PO number for a `public_sector`
client (`422` `po_required`). A credit note, from a `finance_admin` with step-up, is allowed on an invoice that
is issued, sent or paid (`409` `invoice_not_issued` otherwise); it has `doc_type` `credit_note`, the next number
of the entity's credit-note sequence, `credits_invoice_id` naming the original, the original's lines negated and
the original's treatment, rate and totals negated; the original becomes `void` and keeps its number.

**Grants**

| Call | Body | Answer |
|---|---|---|
| `POST /api/grants` | `{"grantee_email", "resource_type", "resource_id", "capability", "reason", "ends_at"}` | `201` `{"id", "grantee_email", "resource_type", "resource_id", "capability", "ends_at"}`; no `ends_at` is `422` `grant_requires_expiry`; an `ends_at` not in the future is `422` `grant_ends_in_past` |
| `DELETE /api/grants/{id}` | none | `204` |

Grants are created by a `group_admin`, or by an account director over its own portfolio, with step-up. A contractor
holding a grant with resource type `project`, capability `project:read` and an unexpired end reads
`GET /api/projects/{id}` for that project; once the grant ends or is revoked, the very next read answers `404`
`not_found`.

**Vault**

| Call | Body or query | Answer |
|---|---|---|
| `GET /api/vault/secrets` | `client_org_id` | an array of `{"id", "label", "secret_type", "site_url", "client_org_id", "rotation_due_at", "last_accessed_at"}`, never a value |
| `POST /api/vault/access-requests` | `{"secret_id", "justification", "ticket_reference", "requested_ttl_minutes", "break_glass"}` | `201` `{"id", "state", "break_glass", "requested_ttl_minutes", "approved_by", "expires_at"}` with state `pending`; `422` `ttl_exceeds_limit` above 240; `422` `open_ticket_required` when the ticket is missing, not open, or belongs to another organisation than the secret |
| `POST /api/vault/access-requests/{id}/approve` | none | `200`, the request with state `approved` or `awaiting_second_approver` and `approved_by` listing approver emails; `403` `self_approval_forbidden` for the requester; `409` `second_approver_must_differ`; `403` `forbidden` for an ineligible approver |
| `POST /api/vault/secrets/{id}/reveal` | `{"request_id"}` | `200` `{"value", "revealed_until"}` with `Cache-Control: no-store` |
| `POST /api/vault/secrets/export` | none | `403` `export_denied`, recorded in the access log |
| `GET /api/vault/access-log` | none | for the `security_officer`, an array of `{"sequence", "action", "secret_id", "principal_email", "request_id", "occurred_at", "prev_hash", "entry_hash"}` in sequence order |
| `POST /api/vault/access-log/verify` | none | for the `security_officer`, `200` `{"valid", "broken_at"}`, `broken_at` being `null` or the first sequence whose stored hash no longer matches |

A ticket is open unless it is `resolved` or `closed`. A reveal is checked in this order: the request exists, is the
caller's own and names this secret (`403` `access_request_required`); it is `approved` (`409`
`request_not_approved`); it has not expired (`409` `request_expired`); it has not been used (`409`
`request_already_used`); the caller stepped up within 15 minutes (`403` `step_up_required`). A refused reveal
leaves the request unused. A successful reveal appends a `read` entry to the access log before the value is
returned and uses the request up.

**Content**

| Call | Body or query | Answer |
|---|---|---|
| `GET /api/content/entries` | `key` | `200` `{"id", "key", "type", "status", "localisations"}` with each localisation `{"id", "site", "locale", "slug", "path", "version", "status"}` |
| `PATCH /api/content/localisations/{id}` | `{"slug", "version"}` | `200`, the localisation; `409` `version_conflict` with `{"current_version"}` when `version` is stale |

Content is edited by a project manager or group admin. A case study's `path` is `/work/{slug}/` on the English
site (`site` `com`) and `/fr/references/{slug}/` on the French site (`site` `fr`). A published path that stops being
a localisation's path answers `301` to the new path from then on.

**Documents the server answers**

- Every public route of both sites answers as a complete HTML document with one `h1`, its title, its canonical
  link, and a `<link rel="alternate" hreflang="...">` for each sibling localisation of the same entry plus
  `hreflang="x-default"` pointing at the English one, each `href` an absolute address on `APP_PUBLIC_URL`.
- A landing page below its uniqueness threshold carries `<meta name="robots" content="noindex">`; an indexable page
  carries no `noindex`.
- `GET /sitemap.xml` answers `200` with a sitemap listing, as `<loc>` absolute addresses, every published and
  indexable public page of both sites, and nothing else: no `noindex` page and nothing under `/portal` or `/api`.
- `GET /robots.txt` answers `200`, disallows `/portal` and `/api`, and names the sitemap in a `Sitemap:` line.
- Every public page links a favicon in its head with `<link rel="icon" href="/favicon.ico">`, and `GET /favicon.ico`
  answers `200` with an image content type.
- Every English page's footer links `/privacy/` and every French page's footer links `/fr/confidentialite/`; the
  English privacy page's `h1` is `Privacy policy`, the French one's is `Politique de confidentialité`, and each
  states what Parallax records about visitors, leads and applicants and how long it keeps each.
- The legacy addresses answer `301`: `/project/{slug}/` to `/work/{slug}/`, `/projects/` to `/work/`,
  `/our-services/` to `/services/`, `/about-us/` to `/about/`, `/contact-us/` to `/contact/`, `/legal-mentions/`
  to `/legal/` and `/privacy-policy/` to `/privacy/`.
- No served document, script or style anywhere carries a vault secret's value, a database credential or the
  identity provider client secret; the browser receives only what a signed-out visitor or the signed-in principal
  may see.

### Seeded fixtures

Seeding runs on first start and is idempotent: restarting never creates a second copy of any seeded row.
Every seeded principal uses the password `deku-demo-pw-2026` and also exists in the Keycloak realm
`parallax` with the same address and password. Seeded principals hold no MFA enrolment, and the password
sign in completes their session. Instants below written relative to seeding are computed from the instant
seeding runs.

**Agency entities.**

| Slug | Legal name | Country | VAT number | Invoice prefix | Credit-note prefix | Sender | Calendar |
|---|---|---|---|---|---|---|---|
| `parallax-malta` | `Parallax Malta Ltd` | `MT` | `MT20000001` | `PXM-` | `PXMC-` | `contact@parallax.example.com` | `MT office hours`, Europe/Malta, Monday to Friday 09:00 to 18:00, Maltese public holidays |
| `parallax-france` | `Parallax France SAS` | `FR` | `FR40900000001` | `PXF-` | `PXFC-` | `contact@parallax-france.example.com` | `FR office hours`, Europe/Paris, Monday to Friday 09:00 to 18:00, French public holidays |

A third calendar, `24x7`, covers every hour of every day.

**Agency and external principals.**

| Email | Role | Scope | Approval threshold |
|---|---|---|---|
| `admin@parallax.example.com` | `group_admin` | both entities | none |
| `finance.fr@parallax.example.com` | `finance_admin` | Parallax France | none |
| `finance2.fr@parallax.example.com` | `finance_admin` | Parallax France | none |
| `finance.mt@parallax.example.com` | `finance_admin` | Parallax Malta | none |
| `director.fr@parallax.example.com` | `account_director` | Parallax France, portfolio Aeroline, Verdane and Institut Lumiere | `5000000` |
| `director.mt@parallax.example.com` | `account_director` | Parallax Malta, portfolio Brugmann Logistics, Kessler Werkzeug, Vondel Media, Alpenrad, Valletta Yachting and Lakeside Systems | `5000000` |
| `pm.fr@parallax.example.com` | `project_manager` | Parallax France, projects `AERO-2026-01`, `VERD-2026-01`, `INST-2026-01`, no commercial visibility | none |
| `designer.fr@parallax.example.com` | `producer` | Parallax France, the same three projects | none |
| `dev.fr@parallax.example.com` | `producer` | Parallax France, the same three projects, on call, so its working window is the `24x7` calendar | none |
| `security@parallax.example.com` | `security_officer` | both entities | none |
| `analyst@parallax.example.com` | `analyst` | both entities | none |
| `recruiter@parallax.example.com` | `recruiter` | both entities | none |
| `freelance@kite-studio.example.com` | `contractor`, external | no grant | none |

**Client organisations.** Every one is a `client_org` in `EUR`.

| Slug | Legal name | Country | VAT number | Validation state | Last successful validation | Billing entity | Profile |
|---|---|---|---|---|---|---|---|
| `aeroline` | `Aeroline SA` | `FR` | `FR11400000001` | `valid` | 10 days before seeding | `parallax-france` | `enterprise` |
| `verdane` | `Verdane SAS` | `FR` | `FR22500000002` | `valid` | 10 days before seeding | `parallax-france` | `standard` |
| `institut-lumiere` | `Institut Lumiere` | `FR` | `FR33600000003` | `valid` | 10 days before seeding | `parallax-france` | `public_sector` |
| `brugmann` | `Brugmann Logistics NV` | `BE` | `BE0400000004` | `valid` | 10 days before seeding | `parallax-malta` | `standard` |
| `kessler` | `Kessler Werkzeug GmbH` | `DE` | `DE500000005` | `invalid` | none | `parallax-malta` | `standard` |
| `vondel` | `Vondel Media BV` | `NL` | `NL600000006B01` | `service_unavailable` | 40 days before seeding | `parallax-malta` | `standard` |
| `alpenrad` | `Alpenrad GmbH` | `AT` | `ATU70000007` | `service_unavailable` | 120 days before seeding | `parallax-malta` | `standard` |
| `valletta-yachting` | `Valletta Yachting Ltd` | `MT` | `MT80000008` | `valid` | 10 days before seeding | `parallax-malta` | `standard` |
| `lakeside` | `Lakeside Systems AG` | `CH` | `CHE900000009` | `valid` | 10 days before seeding | `parallax-malta` | `standard` |

Aeroline's org units are `Digital`, `Digital > Brand` beneath it, and `Procurement`.

**Client principals.**

| Email | Organisation | Role | Unit | Approval threshold |
|---|---|---|---|---|
| `owner@aeroline.example.com` | Aeroline | `client_owner` | `Digital` | `20000000` |
| `brand1@aeroline.example.com` | Aeroline | `client_approver` | `Digital > Brand` | `5000000` |
| `brand2@aeroline.example.com` | Aeroline | `client_approver` | `Digital > Brand` | `1000000` |
| `procurement@aeroline.example.com` | Aeroline | `client_approver` | `Procurement` | `20000000` |
| `collab@aeroline.example.com` | Aeroline | `client_collaborator` | `Digital > Brand` | none |
| `billing@aeroline.example.com` | Aeroline | `client_finance` | none | none |
| `owner@verdane.example.com` | Verdane | `client_owner` | none | `10000000` |
| `owner@institut-lumiere.example.com` | Institut Lumiere | `client_owner` | none | `10000000` |

**Deliverable approval policies.**

| Organisation | Value band, minor units | Stages |
|---|---|---|
| Aeroline | up to and including `2000000` | stage 1 `any_of` every active `client_approver` of `Digital > Brand` |
| Aeroline | above `2000000` | stage 1 `any_of` every active `client_approver` of `Digital > Brand`; stage 2 `all_of` `owner@aeroline.example.com` and `procurement@aeroline.example.com` |
| Verdane | any value | stage 1 `any_of` `owner@verdane.example.com` and the account's director `director.fr@parallax.example.com` |
| Institut Lumiere | any value | stage 1 `any_of` `owner@institut-lumiere.example.com` |

**Projects and contracts.**

| Project code | Name | Organisation | Contract reference | Contract original value | Contract status |
|---|---|---|---|---|---|
| `AERO-2026-01` | Aeroline brand site | Aeroline | `PXF-CT-2026-001` | `12000000` | `active` |
| `VERD-2026-01` | Verdane storefront | Verdane | `PXF-CT-2026-002` | `4500000` | `active` |
| `INST-2026-01` | Institut Lumiere research portal | Institut Lumiere | `PXF-CT-2026-003` | `3000000` | `active`, PO required |

Each project's lead project manager is `pm.fr@parallax.example.com` and its account director is
`director.fr@parallax.example.com`; each contract's value equals its original value, with no change orders.

**Proposal.** Aeroline's proposal version `2`, status `sent`, fixed price, Parallax France, lines:

| Position | Kind | Description | Role | Quantity | Unit | Unit price | Cost price | Amount |
|---|---|---|---|---|---|---|---|---|
| 1 | `role_days` | UX design phase | `ux_designer` | 10 | day | `90000` | `52000` | `900000` |
| 2 | `role_days` | Front-end build | `frontend_dev` | 25 | day | `80000` | `47000` | `2000000` |
| 3 | `fixed_item` | Analytics setup | none | 1 | item | `350000` | `150000` | `350000` |

Its subtotal and total are `3250000`, its discount `0`, and its `margin_minor`, the sum of each line's amount less
its quantity times its cost price, is `1405000`.

**Issued invoices**, all dated in 2026: `PXF-2026-00001` to Verdane and `PXF-2026-00002` to Aeroline from Parallax
France, and `PXM-2026-00001` to Valletta Yachting from Parallax Malta. No credit note is seeded.

**Tickets.**

| Reference | Organisation | Priority | Status | Subject | Assignee |
|---|---|---|---|---|---|
| `PX-2026-000142` | Verdane | `p1` | `in_progress` | Storefront returns 502 | `dev.fr@parallax.example.com` |
| `PX-2026-000143` | Verdane | `p3` | `closed` | Update footer links | `dev.fr@parallax.example.com` |
| `PX-2026-000150` | Aeroline | `p2` | `in_progress` | Newsletter form timeout | `dev.fr@parallax.example.com` |

Each ticket references its organisation's managed site.

**Managed sites and vault secrets.**

| Organisation | Site | Label | Type | Value |
|---|---|---|---|---|
| Verdane | `https://verdane.example.com` | Production CMS admin | `cms_admin` | `vlt-verdane-cms-4471-QZ` |
| Verdane | `https://verdane.example.com` | Hosting control panel | `hosting` | `vlt-verdane-host-9022-KP` |
| Verdane | `https://verdane.example.com` | DNS registrar | `dns` | `vlt-verdane-dns-3318-LM` |
| Aeroline | `https://aeroline.example.com` | Production CMS admin | `cms_admin` | `vlt-aeroline-cms-7710-RT` |

Both sites are `production`, held, and monitored. The vault access log starts empty. An access request is
break-glass only when its `break_glass` is `true`, whatever the hour it is made.

**Public content.** Both sites are seeded and published:

- the nine English services at `/services/{slug}/`, and on the French site the same services plus
  `accompagnement-refonte-site-internet` at `/fr/services/{slug}/`;
- seventeen English case studies at `/work/{slug}/`: `anvil`, `arcwood-design`, `bellamy-associes`, `benno`,
  `centre-lumen`, `playcraft`, `durand-fils`, `lyon-junior-conseil`, `squadron`, `verdane`, `hello-marlo`,
  `petit-atelier`, `ossature-nord`, `maison-interieur`, `office-forma`, `secora`, `sequoia-habitat`;
- nine French references at `/fr/references/{slug}/`: `3bis`, `altera`, `bellamy-associes`, `bloomy`,
  `kopter`, `site-internet-groupe-m`, `site-internet-jacquard`, `site-internet-rail-immobilier`,
  `site-internet-xenon`;
- a case study's entry key is `case-study/` followed by its English slug, or its French slug where it has no
  English localisation; `case-study/bellamy-associes` is one entry with both localisations, and every other case
  study has one;
- the sixteen French landing pages, each human-reviewed, with these unique body ratios against a threshold of
  `0.400`: `agence-seo-lyon` `0.620`, `agence-seo-paris` `0.310`, `agence-sea-lyon` `0.540`, `agence-sea-paris`
  `0.280`, `agence-ux-design-lyon` `0.470`, `agence-ux-design-paris` `0.390`, `agence-content-marketing-lyon`
  `0.350`, `agence-content-marketing-paris` `0.410`, `agence-webmarketing-lyon` `0.300`, `agence-webmarketing-paris`
  `0.450`, `agence-digitale-lyon` `0.580`, `agence-digitale-paris` `0.360`, `agence-web-lyon` `0.500`,
  `agence-web-site-internet-lyon` `0.420`, `agence-web-site-internet-paris` `0.330`, `agence-web-digitale` `0.600`;
  each lives at `/fr/{key}/`, and a page is indexable only at or above the threshold;
- the legal pages, the home pages, the about, journal, contact, careers and form pages of both sites.

## Data model

Roughly sixty two tables, grouped by module, all in PostgreSQL at `DATABASE_URL`. **Every seeded principal
uses the password `deku-demo-pw-2026`.** It is fixture data, not a secret. Keycloak holds it for every seeded
principal; the exact literal must work at `POST /api/auth/login`, and it must be written into
`/app/USER_README.md` beside each seeded address so anyone opening the app can sign in.

### Conventions

| Convention | Rule |
|---|---|
| identifiers | UUIDv7, time-ordered so they index well and leak no count |
| timestamps | `created_at` and `updated_at` are timezone-aware instants in UTC |
| money | never a float: every amount is an integer `amount_minor` plus a three letter `currency` |
| enumerations | stored as enumerated types, so a typo fails at write time |
| tenancy | every tenant-scoped table carries `client_org_id` and a row-level security policy |
| soft deletes | `deleted_at`, and every uniqueness rule applies among rows where `deleted_at` is empty |
| extension points | only `content_localisations.blocks`, `report_definitions.sections`, `approval_policies.stages` and `site_alerts.evidence` hold open-ended JSON, each validated on write against a registered JSON Schema with its schema version stored alongside; there is no general metadata column, because tenant-specific behaviour would start living in it where the authorisation layer cannot reason about it |

### Identity and organisation

- **organisations** - kind (`agency_entity`, `client_org`, `partner_org`), legal name, display name, slug unique
  case-insensitively, country (ISO 3166-1 alpha-2), VAT number, `vat_validated_at` (the last successful
  validation), `vat_validation_state` (`unchecked`, `valid`, `invalid`, `service_unavailable`), billing entity
  (an agency entity organisation), governance profile (`standard`, `enterprise`, `public_sector`, default
  `standard`), industry, primary locale (`en` or `fr`), data region (default `EU`), onboarded and offboarded
  instants.
- **org_units** - organisation, parent unit, name, and a materialised path for subtree queries, unique per
  organisation.
- **principals** - kind (`agency`, `client`, `external`, `service`, `device`), email unique case-insensitively
  among live rows (empty for service and device principals), full name, locale (default `en`), timezone
  (default `Europe/Paris`), status (`invited`, `active`, `suspended`, `offboarded`), MFA enrolment and last seen
  instants.
- **agency_memberships** - principal, agency entity, role, approval threshold, start and end.
- **org_memberships** - principal, organisation, optional unit, role validated against the policy bundle,
  `approval_threshold_minor` (empty means no approval authority), source (`manual`, `scim`, `jit`, `invite`),
  start, end and revocation instants, unique per principal, organisation and role.
- **grants** - grantee, resource type and id, capability, granted by, `on_behalf_of_id` for delegation, a
  mandatory reason shown in access reviews, whether step-up is required, `starts_at`, a mandatory `ends_at`
  after `starts_at` (no perpetual grants), maximum uses, uses so far, revocation instant and actor; active
  grants are found quickly by grantee and resource among unrevoked rows.
- **identity_providers** - organisation, protocol (`oidc`, `saml2`), issuer unique across the table, metadata
  URL, signing certificates (several valid at once for rotation), client id, a vault reference for the client
  secret and never the secret, just-in-time provisioning (default on), default role (default `client_viewer`),
  group claim (such as `groups`), SCIM enabled and its token reference, status (`pending`, `active`,
  `disabled`).
- **idp_domains** - IdP, domain unique across the whole table case-insensitively, verified instant, the DNS
  TXT verification token and method (default `dns_txt`). An IdP asserts identities only in a domain it has
  verified; because the domain is globally unique, two organisations can never both claim it, and a conflicting
  claim escalates to the `security_officer`.
- **idp_group_mappings** - IdP, group value, role, unique per IdP and group value.
- **service_principals** and **site_keys** - scoped service tokens and rotatable per-site HMAC keys.
- **sessions** - principal, session family, `step_up_at`, absolute and idle expiry, revocation, device summary.

### CRM

- **leads** - `reference` unique, `source` (`start_a_project`, `say_hello`, `devis_fr`, `apply`, `referral`,
  `inbound_call`, `partner`, `event`, `outbound`, `unknown`), `source_locale` (`en` or `fr`), `entity` (the
  routed agency entity slug), first and last name, `email` compared case-insensitively, phone in E.164 and its
  country, company name and country, `budget` (`band_10_20k`, `band_20_30k`, `band_30_60k`, `band_60k_plus`),
  `kind` (`website`, `website_with_seo_sea`, `digital_campaign`, `seo`, `ux_webdesign`, `branding`, `ecommerce`,
  `crm_marketing_automation`, `replatform`, `full_project`), message, attachment, `status` (`new`, `triaged`,
  `qualified`, `disqualified`, `converted`, `spam`, `duplicate`, default `new`), disqualify reason, spam score
  between 0.000 and 1.000, assigned owner and instant, priority, first-response due and first-responded
  instants, converted organisation and opportunity, attribution, `gclid` (empty unless marketing consent was
  given), consent version and instant, hashed address and user agent, the idempotency key it arrived under.
  Triage reads by status and newest first among live rows, and leads are also found by email.
- **attributions** - first touch and last touch (source, medium, campaign, term, content, landing URL, referrer,
  instant, and the click id only under marketing consent), touch count, hashed session id, and the consent state
  under which attribution was captured.
- **contacts** - organisation, optional principal once they have portal access, first and last name, email
  unique per organisation among live rows, phone, job title, unit, primary flag, marketing consent instant.
- **opportunities** - organisation, billing entity, name, stage (`discovery`, `scoping`, `proposal_sent`,
  `negotiation`, `verbal_yes`, `won`, `lost`, `dormant`, default `discovery`), owner, expected value and currency
  (default `EUR`), probability between 0 and 100, expected close, lost reason, source lead.
- **opportunity_stage_history** - append-only: opportunity, from and to stage, actor, instant, note.

**The budget band.** The legacy `+50K` value behind a `+60K` label is resolved by an identifier,
`band_60k_plus`, independent of both the label and any legacy string; historic `+50K` and `+60K` map to it, and
the displayed label lives in the content model, not in code.

### Files

- **files** - one table for every upload, because a brief, a CV and a deliverable behave alike and differ only in
  policy: client organisation (empty for pre-conversion leads and applicants), storage bucket and object key
  unique together, a sanitised filename never used as a path, declared and detected type, size, SHA-256, scan
  state (`pending`, `clean`, `infected`, `failed`, `skipped`), scan result, visibility (`private`, `org`,
  `public`), uploader, retention class, expiry. The object key is organisation, a UUIDv7 and a hash prefix, so
  neither filename nor sequence is inferable, and every download goes through a signed, short-lived, single-use
  address minted after an authorisation decision.

### Commerce

- **rate_cards** - agency entity, name, currency (default `EUR`), effective from and to; two cards of one entity
  and name never have overlapping effective date ranges.
- **rate_card_lines** - rate card, role (`ux_designer`, `frontend_dev`, `seo_consultant` and so on), seniority,
  day rate, and an internal cost rate visible only to margin-visible principals, unique per card, role and
  seniority.
- **proposals** - opportunity, client organisation, agency entity, version unique per opportunity, status
  (`draft`, `internal_review`, `sent`, `viewed`, `accepted`, `rejected`, `expired`, `superseded`), locale, rate
  card, commercial model (`fixed_price`, `time_and_materials`, `retainer`, `hybrid`), subtotal, discount, tax
  treatment computed at issue, total, currency, valid until, document file, sent, first viewed and decided
  instants, creator.
- **proposal_lines** - proposal, position unique per proposal, kind (`phase`, `role_days`, `fixed_item`,
  `expense`, `discount`, `retainer_month`), description, role, seniority, quantity, unit (`day`, `item`, `month`),
  unit price, cost price (redacted by policy for client principals), amount.
- **contracts** - client organisation, agency entity, origin proposal, `reference` unique per entity, status
  (`pending_signature`, `active`, `suspended`, `completed`, `terminated`, `void`), commercial model, currency,
  `value_minor` (the current value including approved change orders), `original_value_minor`, start and end
  dates, PO number and whether one is required (for `public_sector`), approval policy, the e-signature envelope
  reference, signature instant and signed document, termination instant and reason.
- **change_orders** - contract, sequence unique per contract, reason, delta value (possibly negative), schedule
  impact in days, status (`draft`, `submitted`, `client_review`, `approved`, `rejected`, `withdrawn`),
  requester, approval, approval instant.

**Invariant CO-1.** A contract's `value_minor` always equals its `original_value_minor` plus the sum of its
approved change orders' deltas: enforced where change orders are approved, reconciled nightly, and the
foundation of the three-way reconciliation of contract, delivery and billing.

### Delivery

- **projects** - client organisation, contract, agency entity, `code` unique (such as `VERD-2026-01`), name,
  status (`planned`, `active`, `on_hold`, `in_review`, `delivered`, `closed`, `cancelled`), white-label flag and
  partner organisation, lead project manager, account director, planned and actual start and end, budget days,
  health (`green`, `amber`, `red`).
- **milestones** - project, contract, position unique per project, name, status (`not_started`, `in_progress`,
  `submitted`, `approved`, `rejected`, `invoiced`, `paid`), billing trigger (`on_approval`, `on_date`,
  `on_completion`, `none`, default `on_approval`), bill amount or bill percent, due date, approval instant and
  approval, invoice.
- **tasks** - project, milestone, parent task, title, description, status (`todo`, `in_progress`, `blocked`,
  `in_review`, `done`, `cancelled`), assignee, role, estimate, due date, whether it requires site access (which
  gates just-in-time vault requests) and the managed site.
- **time_entries** - principal, project, task, client organisation, work date, minutes above 0 and at most 1440,
  billable flag, role, rate and cost snapshotted at approval rather than joined at read, note, status (`draft`,
  `submitted`, `approved`, `rejected`, `locked`), approver, lock instant set when the period is invoiced; read by
  organisation, work date and status. Rates are snapshotted because a March rate-card change must never silently
  reprice February's approved and invoiced time.

### Review

- **deliverables** - project, client organisation, milestone, name, kind (`design`, `prototype`, `copy`,
  `build_url`, `document`, `report`, `asset_bundle`), current version, status (`draft`, `internal_review`,
  `shared`, `changes_requested`, `approved`, `superseded`, `withdrawn`).
- **deliverable_versions** - deliverable, version number unique per deliverable, file, external URL for the
  `build_url` kind, checksum of the file or a rendered snapshot, notes, uploader, shared instant.
- **annotations** - deliverable, version, anchor (point, region, text range or time, with x and y normalised
  between 0 and 1, page, selector and milliseconds), anchor confidence (`exact`, `remapped`, `orphaned`), body,
  author, parent annotation, status (`open`, `resolved`, `wont_fix`), resolver and instant. Anchors are
  normalised rather than pixel coordinates; on a new version annotations are carried forward with a remap
  attempt, and anything that cannot be located becomes `orphaned` and appears in a tray of comments from a
  previous version, never silently dropped and never pinned to the wrong place.
- **agency_notes** - a structurally separate channel for agency-internal notes on a deliverable, which no API
  response to a client principal ever includes.
- **approval_policies** - organisation (empty for the agency's default template), name, applies to
  (`deliverable`, `change_order`, `contract`, `invoice_credit`), stages as an ordered list of stage definitions,
  timeout hours, escalation (to a role or unit after hours, then escalate or auto-reject), minimum and maximum
  value, version, active flag.
- **approvals** - policy and the pinned `policy_version` (a policy edit never rewrites a live approval), subject
  type and id, client organisation, value, the version under review, state (`pending`, `approved`, `rejected`,
  `expired`, `cancelled`), current stage, due, decided and cancellation instants and the superseding version.
- **approval_steps** - approval, stage, mode (`any_of`, `all_of`, `quorum`), quorum, assignee principal, unit or
  role, decision (`approved`, `rejected`, `abstained`), decider, `on_behalf_of_id`, comment, decision instant,
  notified instant, reminder count.

### Retainers, tickets and SLA

- **retainers** - contract, client organisation, service lines (`maintenance`, `seo`, `sea`, `content`,
  `hosting_mgmt`), monthly fee, included hours, overage rate, rollover policy (`none`, `one_month`, `quarter`),
  SLA policy, billing day (default 1), start and end, notice days (default 60), auto-renew.
- **sla_policies** - name, business calendar, targets per priority in business minutes (for example `p1`
  respond 60 and resolve 240), states that pause the clock (default `waiting_on_client`), breach action (default
  notify the account director).
- **business_calendars** - name (`FR office hours`, `MT office hours`, `24x7`), timezone, ISO workdays, open and
  close times, holidays, which differ between France and Malta.
- **tickets** - client organisation, retainer, managed site, `reference` unique (such as `PX-2026-014392`),
  subject, body, priority (`p1` to `p4`, default `p3`), category, status (`new`, `triaged`, `in_progress`,
  `waiting_on_client`, `waiting_on_third_party`, `resolved`, `closed`, `reopened`), reporter, assignee, channel
  (`portal`, `email`, `monitor`, `phone`), source alert, respond and resolve due instants, first response and
  resolution instants, breach flags.
- **sla_clock_events** - append-only: ticket, kind (`start`, `pause`, `resume`, `stop`, `target_changed`), target
  (`respond`, `resolve`), instant, reason. **SLA time is computed, never counted down in a column**: remaining
  budget is a pure function of these events, the policy targets and the business calendar, evaluated on read,
  because a stored countdown is wrong after a restart, a clock skew, or a pause across a French holiday a Maltese
  calendar lacks.

### Managed sites and the vault

- **managed_sites** - client organisation, label, primary URL, environment, platform (`wordpress`, `shopify`,
  `custom`, `headless`), hosting provider, registrar, monitoring enabled, beacon key, under management since,
  handover state (`held`, `handover_requested`, `handed_over`, `revoked`).
- **vault_secrets** - client organisation and site validated by the vault module, label, secret type, the value
  encrypted with AES-256-GCM as ciphertext and nonce, the data key wrapped under the organisation's key and that
  key's id, version, rotation due and last rotated instants, creator, destroyed instant (the key destroyed, the
  row kept), unique per organisation, site, label and version. No column of `vault_secrets` ever holds a secret's
  plaintext.
- **vault_access_requests** - secret, requester, justification, linked task or ticket, requested time to live in
  minutes, at most 240, state (`pending`, `awaiting_second_approver`, `approved`, `denied`, `expired`, `used`,
  `revoked`), approvers and approval instants, break-glass flag, second approver (mandatory for break-glass),
  expiry.
- **vault_access_log** - append-only and hash-chained, one row per access: `sequence`, `secret_id`,
  `request_id`, `principal_email` and principal id, `action` (`create`, `read`, `update`, `rotate`, `destroy`,
  `export_denied`), hashed address, user agent, authentication context (MFA, step-up instant, IdP, session),
  `occurred_at`, `prev_hash` and `entry_hash`.

### Content, both public sites

- **content_entries** - type (`page`, `case_study`, `service`, `landing`, `article`, `legal`, `person`,
  `job_posting`), a locale-independent key such as `case-study/verdane`, status (`draft`, `in_review`,
  `scheduled`, `published`, `unpublished`, `archived`), owner, unique per type and key.
- **content_localisations** - entry, locale (`en`, `fr`), site (`com`, `fr`), slug unique per site and locale,
  title, SEO fields (title, description, canonical override, robots, social), ordered blocks validated per block
  type, translation state (`source`, `translated`, `stale`, `machine_draft`), source localisation and the source
  version it was translated from, version, published, scheduled and unpublished instants, last editor.
- **content_versions** - a full snapshot per save for diff and rollback, with provenance: author, whether AI
  assisted and which model, and the human reviewer.
- **url_aliases** - every path ever published, forever: site, path unique per site, target entry or path, and a
  status of `301`, `302` or `410`.
- **landing_matrix** - the governed service by city grid: entry, service key (`seo`, `sea`, `ux-design`,
  `content-marketing` and so on), city key (`lyon`, `paris`), unique body ratio, minimum ratio (default 0.400),
  indexable (default false), last evaluated instant, human review, unique per service and city.

Two decisions carried by this model: the key is locale-independent and the site explicit, so
`case-study/bellamy-associes` is one entry with an English localisation at `/work/bellamy-associes/` and a French
one at `/fr/references/bellamy-associes/`, from which language alternates and cross-site canonicals are derived
and cannot be forgotten; and a landing page is not indexable until earned, `noindex` until its unique body ratio
reaches the minimum and a human has reviewed it.

### Finance

- **invoice_sequences** - agency entity, document type (`invoice`, `credit_note`, `proforma`), fiscal year,
  prefix, next value (default 1), unique per entity, document type and year.
- **invoices** - agency entity, client organisation, contract, project, retainer, milestone, document type
  (default `invoice`), `number` (empty until issued, assigned once and never reused), status (`draft`, `issued`,
  `sent`, `partially_paid`, `paid`, `overdue`, `disputed`, `void`, `written_off`), issue and due dates, payment
  terms (default 30 days), currency, subtotal, tax, total and paid amounts, tax treatment (`domestic_mt`,
  `domestic_fr`, `eu_reverse_charge`, `eu_b2c`, `export_outside_eu`, `exempt`), tax rate in basis points, tax
  note, buyer VAT number and its validation instant, PO number, whether e-invoicing is required, e-invoice channel
  (`none`, `pdp`, `chorus_pro`) and state (`not_applicable`, `queued`, `submitted`, `accepted`, `rejected`,
  `failed`), e-invoice reference, PDF and Factur-X files, issuer and instant, the credit note that voided it, and
  the invoice a credit note credits. A number is unique per entity and document type among issued rows.
- **invoice_lines** - invoice, position unique per invoice, source type (`milestone`, `time`, `retainer`,
  `expense`, `overage`, `adjustment`, `discount`) and id, description, quantity (default 1), unit, unit price,
  amount, tax rate; an item appears at most once on an invoice, and a milestone, time entry or overage appears on
  at most one invoice line across all invoices.
- **payments** - agency entity, client organisation, method (`sepa_transfer`, `sepa_direct_debit`, `card`,
  `cheque`, `other`), provider and reference, amount, currency, received instant, bank reference, state
  (`received`, `allocated`, `partially_allocated`, `refunded`, `failed`, `chargeback`), idempotency key unique.
- **payment_allocations** - payment, invoice, a positive amount, allocator and instant, unique per payment and
  invoice.
- **revenue_recognition** - contract, period (the first day of a month) unique per contract, method (`milestone`,
  `percent_complete`, `straight_line`), recognised, deferred and accrued amounts, computed instant.

**Invariant FIN-1, gapless numbering.** A number is assigned inside the issuing transaction from the entity's
sequence row, serialised per sequence, never from a database sequence that skips values on rollback, and never
guessed; once assigned it is immutable and corrections are credit notes. Each entity, document type and year's
issued numbers form a contiguous range with no gap and no duplicate, verified nightly with a page to
`finance_admin` on any deviation.

**Invariant FIN-2, no double billing.** The database itself refuses a second invoice line for the same milestone,
time entry or overage, rather than application code promising not to create one.

### Governance

- **audit_events** - a strictly increasing sequence, instant, actor and kind, `on_behalf_of_id`, action (such as
  `invoice.issued` or `vault.secret.read`), resource type and id, client organisation and agency entity, outcome
  (`success`, `failure`, `denied`), request and correlation ids, hashed address, authentication context,
  field-level before and after state with personal data redacted by policy, previous hash and entry hash (a
  SHA-256 over the previous hash and the entry's canonical JSON), retention date; read by actor, by resource and by
  organisation, each newest first.
- **audit_anchors** - periodic notarisation of the chain head: as-of instant, head sequence and hash, a signature
  from an offline key, and where it was exported with object lock.
- **consent_records** - a hashed visitor key, site, purposes (`analytics`, `marketing`, `functional`), policy
  version, method (`banner_accept_all`, `banner_reject_all`, `banner_custom`, `preference_centre`, `withdrawn`),
  country, instant, and an expiry at most 13 months later.
- **data_subject_requests** - kind (`access`, `erasure`, `rectification`, `portability`, `restriction`,
  `objection`), the agency's role (`controller` or `processor`), the organisation it acts for when processor,
  subject email and verification instant, received and due instants (received plus 30 days), state (`received`,
  `verifying`, `searching`, `awaiting_client`, `fulfilled`, `refused`, `extended`), systems searched, result file,
  refusal reason, closure.
- **processing_activities** - the Article 30 record, versioned: name, role (`controller`, `processor`, `joint`),
  purposes, lawful basis, categories, subjects, recipients, transfers, retention, security, effective date.
- **subprocessors** - name, purpose, location, DPA URL, whether SCCs are in place, added and removed dates, and
  when clients were notified under Article 28(2).
- **outbox_events**, **webhook_receipts**, **idempotency_keys**, **rate_limit_buckets**,
  **authorization_decisions** and **notifications** - the operational tables the technical requirements name.

The chain is verified, not merely written: the last 24 hours of audit events are recomputed hourly, a mismatch
pages the `security_officer` as SEV-1, and daily anchors go to storage under compliance-mode object lock, so even a
compromised database administrator cannot rewrite history without the discrepancy being provable.

### Insights and monitoring

- **connectors** - client organisation, provider (`ga4`, `search_console`, `google_ads`, `meta_ads`,
  `linkedin_ads`, `matomo`, `crux`), external account reference, a vault reference for the OAuth token and never a
  plaintext token, scopes, status (`connected`, `expired`, `revoked`, `error`, `rate_limited`), last sync, last
  error, the client contact who authorised it and when, unique per organisation, provider and account.
- **metric_snapshots** - organisation, connector, metric date, dimension key (`total`, `page:/fr/services`,
  `query:agence seo lyon`), metrics, a finality flag because GA4 and Search Console backfill for up to three
  days, fetch instant, unique per connector, date and dimension.
- **report_definitions** - organisation, name, locale (default `fr`), sections, schedule, recipients, active flag.
- **report_runs** - definition, period start and end unique per definition, state (`queued`, `running`,
  `succeeded`, `partial`, `failed`), data completeness per source shown on the report's face, file, an input digest
  that makes a run reproducible, start and finish, error. A report generated on the first of the month from
  unfinalised data will not match the same report on the eighth, so the report states its completeness or the
  agency spends a support cycle explaining moved numbers.
- **site_checks** and **web_vitals** - time series partitioned by month with a 400-day retention: site, instant,
  check type, region, status code, response time, success flag, error class, TLS days left, content hash; and
  site, instant, URL, device, LCP, INP, CLS times 1000, TTFB, hashed session, consent flag.
- **site_alerts** - site, kind (`down`, `slow`, `tls_expiring`, `content_changed`, `vitals_regression`,
  `cert_invalid`, `defacement_suspect`), severity (`info`, `warning`, `critical`), opened and confirmed instants
  (confirmed only after consecutive failures from several regions), closed instant, ticket, evidence. An alert
  requires confirmation from at least 2 of 3 probe regions across 3 consecutive checks before opening a ticket.

## Front-end specification

Everything below was measured from the live properties of the agency Parallax replaces, or designed on top of
that evidence, and says which. Literals in `monospace` were measured and are not to be invented around; where
evidence is missing this section says not captured rather than guessing.

### Three surfaces, one system

| Surface | Where | Rendering | Audience |
|---|---|---|---|
| Public marketing | the English site at `/` and the French site at `/fr/` | server-rendered HTML with islands, cached at the edge, WebGL-enhanced, no auth | anonymous prospects, search engines, AI crawlers |
| Client portal | `/portal` | behind a session, with a server-rendered shell for first paint | client principals and external principals |
| Back office | `/portal/agency` | the same application with a different route tree and policy set | agency principals |

The portal and back office are one application with one design system and one policy client, not two
applications; they differ only by the decision set the policy engine returns, which is the only way to
guarantee a client never sees an agency-only affordance because someone forgot to duplicate a guard. The public
site and the portal share design tokens but not components: the public site's job is motion and impression, the
portal's job is density and legibility.

### Design tokens, measured

The measured theme stylesheet (191 379 bytes) declares its colours with this frequency:

| Colour | Occurrences | Role inferred from usage |
|---|---|---|
| near-black neutral, the page ground | 51 | primary surface |
| near-white neutral | 41 | primary foreground and inverted surface |
| near-black neutral, one step darker | 20 | secondary surface, recessed |
| deep neutral, the lighter of two | 10 | muted foreground and rules |
| mid, vivid red | 5 | the brand accent, a crimson |
| mid neutral | 1 | tertiary foreground |
| deep neutral, the darker of two | 1 | border and divider |
| near-black neutral, raised | 1 | elevated surface |
| light, muted orange | 1 | secondary accent, a warm sand |
| true black | 1 | isolated use |

The palette is dark-first with a single high-chroma accent, and there is no declared light theme.

**Tokens for the rebuild:**

| Token | Colour | Use |
|---|---|---|
| `--surface-0` | near-black neutral | the page ground, the most declared value |
| `--surface-1` | near-black neutral, one step darker | recessed areas |
| `--surface-2` | near-black neutral, raised | cards and sheets |
| `--surface-3` | deep neutral, the darker | borders and dividers |
| `--fg-strong` | near-white neutral | primary text |
| `--fg-muted` | deep neutral, the lighter | decorative muted text on the marketing site only |
| `--fg-subtle` | mid neutral | tertiary text |
| `--accent` | mid, vivid red | the single high-chroma accent |
| `--accent-warm` | light, muted orange | secondary, editorial use only |
| `--ok` | mid, vivid teal | success, new for the portal |
| `--warn` | mid, vivid orange | warning, new for the portal |
| `--danger` | mid, vivid red, deliberately the brand accent | destructive, which is on-brand |
| `--info` | light, vivid blue | information, new for the portal |
| `--ease` | the one measured curve, easeOutQuint | every animation |
| `--dur-instant`, `--dur-fast`, `--dur-base`, `--dur-slow` | four duration bands, slow being the site's dominant one | every animation |
| `--font-display` | `MargoBeuys`, then `Poppins`, then `Arial`, then sans-serif | display |
| `--font-body` | `Poppins`, then `Arial`, then sans-serif | body and interface |
| `--bp-xs` to `--bp-3xl` | `320px`, `480px`, `768px`, `1024px`, `1200px`, `1400px`, `1600px` | the measured breakpoints |

**The semantic colours** for success, warning and information do not exist in the measured stylesheet: the live
site is a brochure without status states. They are introduced for the portal, flagged as new, and contrast-audited
against the page ground and the raised surface before use. Danger reuses the measured accent deliberately, because
a destructive action in a portal whose whole identity is one crimson should not import a second red.

**Contrast is a build gate, not a review comment.** The muted foreground on the page ground yields roughly 2.0:1,
a decorative value on the marketing site that must never be used for portal body text. The token file ships a
machine-readable map of allowed pairings, and any text and background pair below 4.5:1 (3:1 for text at least
24px, or 19px bold) fails the build, which removes the most common accessibility regression in dark-first systems.

### Type scale

A fluid scale on the body face, with the display face reserved for `h1`, `h2` and the pinned-gallery captions,
implemented as a clamp between the two anchor widths `320px` and `1600px`:

| Role | At 320px | At 1600px | Line height | Face |
|---|---|---|---|---|
| `display-xl` | `40px` | `112px` | 0.95 | display, `MargoBeuys` |
| `display-l` | `32px` | `72px` | 1.0 | display, `MargoBeuys` |
| `heading-l` | `26px` | `40px` | 1.15 | display, `MargoBeuys` |
| `heading-m` | `20px` | `28px` | 1.25 | body, `Poppins` |
| `heading-s` | `17px` | `20px` | 1.35 | body, `Poppins` |
| `body-l` | `16px` | `18px` | 1.6 | body, `Poppins` |
| `body-m` | `15px` | `16px` | 1.6 | body, `Poppins` |
| `caption` | `12px` | `13px` | 1.45 | body, `Poppins` |

The measured families were `MargoBeuys` for display, `Poppins` for body and interface and `Arial` in the fallback
stack; weights, sizes and the exact fallback stack were not captured, so this scale is specified rather than
measured. `MargoBeuys` web licensing is an open question, and the build degrades to `Poppins` for display roles
without layout breakage if it cannot ship. Aligned figures in tables, counters and totals use tabular digits.

### Motion

Exactly one easing curve is used across the measured stylesheet, easeOutQuint, 512 times, and no other curve is
declared: the brand's motion identity is one curve that leaves fast and settles long, applied everywhere.
Transition durations by frequency favour the slowest band (272 declarations), then the instant band (36), with a
tail through the fast and base bands. Every animation uses that curve and one of the four duration bands.

Eight named primitives, each with a mandatory reduced-motion collapse:

| Primitive | Behaviour | Reduced-motion collapse |
|---|---|---|
| `reveal-up` | fades in while rising a short distance, in the slow band | a fade only, in the fast band |
| `split-line` | per-line masked reveal of split text with a short stagger | full text, no stagger |
| `magnetic` | pointer-following translate of a few pixels, only where hover exists | not instantiated |
| `hover-swap` | the masked label swap of the hover button: the outgoing label leaves left while the incoming arrives from the right | an instant colour change |
| `pinned-scrub` | a pinned section whose scroll scrubs a timeline over the section's scroll budget | the section unpins and its contents stack vertically |
| `webgl-plane` | a WebGL plane with scroll-driven scale and rotate | a static image, WebGL never started |
| `marquee` | an infinite horizontal scroll of partner logos | a static wrapped grid |
| `page-transition` | a cover wipe on route change, in the base band | instant navigation |

Rules that are acceptance criteria, not suggestions:

- only `transform` and `opacity` animate; anything animating `width`, `top`, `filter` or `box-shadow` fails review;
- `will-change` is applied on approach and removed on completion, because a page holding 40 permanent layers is
  why mid-range Android devices stutter;
- every scroll trigger is destroyed on route change, because leaked triggers are the top cause of memory growth in
  single-page replacements of WordPress sites;
- scroll positions are recomputed after fonts are ready and after any image without intrinsic dimensions loads,
  otherwise every pin is computed against the wrong layout;
- **a reduced motion preference disables the smooth-scroll layer entirely**, not merely the decorative tweens,
  because hijacked scrolling is itself a vestibular trigger.

### The WebGL layer and its mandatory fallback

The measured home page starts a WebGL renderer and marks sections `data-webgl-section="1"`, `data-scale="1.044"`,
`data-rotate="0.1"` and `data-webgl-offset="0, 80%"`. The rebuild keeps that behaviour under four hard constraints:

- **the DOM is the source of truth**: every WebGL-rendered image also exists as a real `<img>` with `alt`, `srcset`
  and intrinsic dimensions; WebGL replaces its appearance, never its existence, so a crawler, a screen reader and a
  browser with WebGL disabled all get the page;
- **feature detection, then capability detection**: no WebGL context, a reduced motion preference, four or fewer
  logical cores, or under 4 GB of device memory means the layer never starts;
- **a frame-time budget**: if the rolling mean frame time exceeds 20 milliseconds for 2 seconds, the layer tears
  itself down and reveals the DOM images, because degrading beats shipping 12 frames per second;
- **context loss is handled**: losing the context reveals the DOM layer without an infinite restore loop.

### The pinned project gallery

The measured home page gives the project gallery a scroll budget of fifteen viewport heights with a companion
fixed layer. The rebuild:

- **derives the budget** from the published project count, one viewport height per project, so adding an
  eighteenth case study needs no stylesheet edit; seventeen case studies plus an intro and outro beat come close to
  what the live site allocated, which validates the model;
- gives each project one viewport-height beat, whose timeline runs image scale, the `split-line` caption reveal and
  an index counter;
- **makes keyboard and assistive access a parallel affordance, not a translation of the scroll**: the gallery is
  also a list, Tab moves through project links in document order, focusing one scrolls its beat into view
  respecting reduced motion, and a visually hidden `Skip visual gallery - view all projects as a list` link
  precedes the section and jumps past it, because pinned sections that trap keyboard users are the most common
  accessibility failure in awarded agency sites;
- **uses no pin below `768px`**: the gallery renders as a vertical stack of cards, because fifteen viewport heights
  of scroll-jacking on a phone is a bounce, not an experience.

### Interaction vocabulary, measured

Runtime libraries fingerprinted in the measured theme script (228 122 bytes):

| Library | Signal | Use |
|---|---|---|
| GSAP | 30 identifier hits | the tween engine |
| GSAP ScrollTrigger | 9 hits | scroll-linked animation |
| OGL | 14 hits | the WebGL renderer, a lightweight alternative to three.js |
| Splitting.js | 3 hits | per-character and per-word text splitting for stagger reveals |
| jQuery 3.7.1 with migrate 3.4.1 | WordPress include script tags | legacy WordPress, unused by the theme's own bundle |

Scroll orchestration was attribute-driven on the home page's sections: `data-scroll-section`, `data-scroll`,
`data-scroll-repeat`, `data-scroll-call` with `content-button`, `b-video`, `b-sentence` or `project-gallery`,
`data-scroll-offset` with `0, 125%` or `100%, 100%`, plus the WebGL attributes above. The project gallery was the
pinned section `b-project-gallery b-project-gallery--block` with a paired `b-project-gallery-fixed` holding the fixed
layer.

The measured component naming convention, with prefixes carrying meaning:

| Prefix | Meaning | Examples measured |
|---|---|---|
| `c-` | component | `c-intro`, `c-field__input`, `c-field__label-i`, `c-form-page`, `c-field--consent__label` |
| `b-` | block or section | `b-content-button`, `b-video`, `b-sentence`, `b-project-gallery`, `b-partners`, `b-skf`, `b-cover`, `b-services`, `b-kf__pager-stroke` |
| `e-` | element or atom | `e-button`, `e-button--hover`, `e-button--magnetic`, `e-button__text`, `e-button__icon`, `e-button__hover` |
| `u-` | utility | `u-margin`, `u-pe-n` for pointer events none |

Two button behaviours were declared: `e-button--hover`, a masked text swap whose hover span translates horizontally
inside a centred wrapper, and `e-button--magnetic`, cursor-following with a thin near-white border state, both gated
behind a hover-capable pointer.

The breakpoints were mobile-first with eight minimum widths, by frequency: `768px` (182), `1200px` (121), `1024px`
(88), `1600px` (58), `480px` (55), `1400px` (54), `320px` (54) and `0` (53), plus a hover-capability query (23), one
maximum-width query just below `768px` and one maximum-height query at `667px`; hover-dependent behaviour was correctly
gated behind hover capability.

### The measured public surface

The English property, owned by the Malta entity:

| Route | Purpose | Notes |
|---|---|---|
| `/` | home | eight sections, a WebGL intro, the pinned project gallery |
| `/our-services/` | service catalogue | `h1` `We make creative and innovative website that do convert` |
| `/about-us/` | agency story and counters | `h1` `We're driven by creating the most beautiful websites with the best rankings and conversion rates` |
| `/projects/` | portfolio index | seventeen case studies, heading `Discover our projects and rewards` |
| `/project/{slug}/` | case study | seventeen slugs |
| `/contact/` | contact hub | three routes, `Start a project`, `Say hello` and `Apply`, under the heading `What are you searching for ?` |
| `/contact-us/` | contact hub duplicate | the same content, linked from navigation as `Join the team` |
| `/start-a-project/` | six step brief wizard | form `form_2` |
| `/say-hello/` | two step general enquiry | form `form_3` |
| `/apply/` | six step job application | form `form_1` |
| `/legal-mentions/` | legal notice | linked in the footer as `Web terms and conditions` |
| `/privacy-policy/` | privacy policy | footer |

The French property was a separate WordPress installation running the same theme with a different information
architecture:

| Route family | Members measured |
|---|---|
| Service by city landing matrix | `agence-seo-lyon`, `agence-seo-paris`, `agence-sea-lyon`, `agence-sea-paris`, `agence-ux-design-lyon`, `agence-ux-design-paris`, `agence-content-marketing-lyon`, `agence-content-marketing-paris`, `agence-webmarketing-lyon`, `agence-webmarketing-paris`, `agence-digitale-lyon`, `agence-digitale-paris`, `agence-web-lyon`, `agence-web-site-internet-lyon`, `agence-web-site-internet-paris`, `agence-web-digitale` |
| Service detail pages | `creation-de-site-internet`, `referencement-naturel-seo`, `agence-referencement-payant`, `conseil-strategie-digitale`, `accompagnement-refonte-site-internet` under `services` |
| Case studies | the `references` index plus the nine references seeded for Parallax |
| Editorial | the `actualites-web` blog, with articles including `comment-choisir-une-agence-geo` and `e-e-a-t-le-guide-complet-pour-gagner-en-credibilite` |
| Commercial | `devis` for a quote request, `carriere` for careers, `contact`, `mentions-legales` |

The French home title was `Agence web Lyon & Paris : Création de Site internet, SEO, GEO, SEA`; the English home
title was `Digital Creative Agency in Malta, Paris & Lyon : Parallax`, with the meta description `We build and manage
efficient, creative and innovative websites optimised using SEO and conversion strategies.`

### Public site routes and composition

Routes are generated from the content model's localisations, so this table is the expected output of the content
model rather than a hard-coded router:

| English site | French site | Content type |
|---|---|---|
| `/` | `/fr/` | `page:home` |
| `/services/` | `/fr/services/` | `page:services` with `service` children |
| `/services/{slug}/` | `/fr/services/{slug}/` | `service` |
| `/work/` | `/fr/references/` | `page:work_index` |
| `/work/{slug}/` | `/fr/references/{slug}/` | `case_study` |
| `/about/` | `/fr/agence/` | `page:about` |
| `/journal/` | `/fr/actualites-web/` | `page:blog_index` with `article` |
| `/journal/{slug}/` | `/fr/actualites-web/{slug}/` | `article` |
| none | `/fr/agence-{service}-{city}/` | `landing`, the governed matrix |
| `/contact/` | `/fr/contact/` | `page:contact_hub` |
| `/start-a-project/` | `/fr/devis/` | `page:brief_form` |
| `/say-hello/` | `/fr/contact/message/` | `page:enquiry_form` |
| `/careers/` | `/fr/carriere/` | `page:careers` with `job_posting` |
| `/apply/` | `/fr/carriere/candidature/` | `page:application_form` |
| `/legal/` | `/fr/mentions-legales/` | `legal` |
| `/privacy/` | `/fr/confidentialite/` | `legal` |
| `/cookies/` | `/fr/cookies/` | `legal` with the preference centre |

**Legacy URL preservation is mandatory.** Every previously live path, every `/project/{slug}/` address, the
`/our-services/`, `/about-us/`, `/projects/`, `/contact-us/`, `/legal-mentions/` and `/privacy-policy/` addresses, is
seeded as an alias with a permanent redirect to its new home. Both contact hubs resolve, `/contact-us/` redirecting,
which also fixes the mislabelled `Join the team` navigation entry by pointing it at `/careers/`. A public address
without its trailing slash answers `301` to the slashed form.

**Home composition**, from the measured eight sections, with the measured copy as seed content:

| Section | Measured class | Content | Motion |
|---|---|---|---|
| Intro | `c-intro` | `h1` `The agency that covers your digital needs in a creative and efficient way` | `webgl-plane` with `split-line` |
| Positioning | `b-content-button` | `We design, develop and manage innovative websites optimised using SEO and conversion strategies` with the call to action `Discover our projects` | `reveal-up`, a `magnetic` call to action |
| Showreel | `b-video` | autoplay muted, poster first, controls exposed | plays on intersection, never with sound |
| Challenge statement | `b-sentence` | `Whatever business you do, we take the challenge to bring your digital identity to the next level. Here's what we've done:` | `split-line` |
| Project gallery | `b-project-gallery` | `h2` `Our projects`, seventeen case studies | `pinned-scrub` |
| Trust wall | `b-partners` | `h2` `They trust us`, sixteen client logos | `marquee` |
| Counters | new | 20 awards, 10 years, 400 companies, 20 employees | count up on intersection, static under reduced motion |
| Closing call to action | `b-content-button` | `We'd love to be challenged by you! Feel free to share your brief with us.` with a call to action to the brief form | `reveal-up` |

**Heading semantics are fixed.** Exactly one `h1` per page; the marketing sentences that were `h2` become display
paragraphs where they are not section headings; every landmark section gets a real heading, visually hidden where the
design shows none; and the form pages `/start-a-project/` and `/apply/`, which shipped with no headings at all, get an
`h1` and a heading per step.

**Video**: metadata-only preload, the poster image as the LCP candidate, muted inline autoplay only when reduced
motion is not requested and the connection is not in save-data mode, native controls available at all times, and a
captions track for any showreel carrying speech.

**Case study template**, from the measured Verdane page: title; a one-line client description, `Verdane, a French brand
of outdoor and indoor furniture with a trendy, colourful and sustainable design.`; a service tag list, measured as
`Digital Strategy`, `E-commerce`, `UI Design`, `UX design`, `Webdesign`, `Website`; a `See live` outbound link marked as
leaving the site with `rel="noopener"`; a media sequence of images and muted looping videos; and a next-project link,
measured as `Hello Marlo`. Year, awards, team credits and results metrics were absent from the live page but are
modelled as optional fields, because a case study without a result is a mood board and the agency's own pitch is
conversion.

### The intake forms, measured

All three measured forms used `class="dc_form"` with `autocomplete="off"` and were multi-step: each step a
`c-form-page`, inactive steps carrying `u-pe-n`.

**`/start-a-project/`, form `form_2`, six steps, nine field controls:**

| Order | Name | Type | Required | Label, verbatim |
|---|---|---|---|---|
| 1 | `input_4` | text | yes | `First name` |
| 2 | `input_3` | text | yes | `Last name` |
| 3 | `input_5` | text | no | `Company name` |
| 4 | `input_6` | text | yes | `Company country` |
| 5 | `input_23` | text | yes | `Phone` |
| 6 | `input_26` | email | yes | `Email` |
| 7 | `input_10` | four radios | yes | `Your budget range` |
| 8 | `input_25` | seven radios | yes | `Kind of project` |
| 9 | `input_8` | textarea of four rows | yes | `More about your project` |
| 10 | `input_18` | a PDF file | no | `Specifications` |
| 11 | `input_12.1` | checkbox | yes | `I agree with terms conditions and privacy policy` |

Budget values as submitted were `10K-20K`, `20K-30K`, `30K-60K`, `+50K`; as displayed, `10K-20K`, `20K-30K`,
`30K-60K`, `+60K`. Project kinds: `Website`, `Website with SEO and/or SEA`, `Digital Campaign`, `Search Engine
Optimization`, `UX & Webdesign`, `Branding`, `Full Project`.

**`/say-hello/`, form `form_3`, two steps, seven controls:** `input_1` last name, `input_3` first name, `input_4`
e-mail, `input_7` phone, `input_12` country, `input_9` the textarea `Your message`, and `input_11.1` the consent
checkbox, all required.

**`/apply/`, form `form_1`, six steps, six text and file controls plus three radio groups:** `input_3` last name,
`input_4` first name, `input_16` e-mail, all required; `input_5` `Job you apply for` with values `project manager`,
`development`, `design`, `SEA`, `SEO`, `Other` displayed as `Project management`, `Development`, `Design`,
`SEM / SEA`, `SEO`, `Other`; `input_7` `Type of job` with `Permanent contract`, `Internship`, `Partnership`;
`input_9` `Location` with `Malta`, `France`, `Remote`; `input_11` the required PDF `Curriculum vitae`; `input_12` the
optional PDF `Cover letter`; `input_14` the optional `Portfolio URL`.

**Shared micro-copy, verbatim:**

| String | Context |
|---|---|
| `Oops, e-mail is not valid.` | email field error |
| `Attach or drop it here` | file dropzone idle |
| `File type : .pdf` | file constraint hint |
| `Max. file size : 8MB` | file constraint hint |
| `Wrong file type` | file type error |
| `Max file size exceeded` | file size error |
| `I agree with terms conditions and privacy policy` | consent checkbox |

The measured submit endpoint, method, nonce, success copy and server-side validation were not captured: no form
action appeared in the served HTML and submission lived inside the script bundle.

### The intake forms, rebuilt

One wizard engine over a declarative step schema drives all three, so the six step brief, the two step enquiry
and the six step application are three configurations, not three implementations.

**Brief wizard, `/start-a-project/` and `/fr/devis/`:**

| Step | Fields | Notes |
|---|---|---|
| 1 | first name and last name, required | given-name and family-name autocomplete, reversing the old autocomplete suppression |
| 2 | company name, and company country, required | the country is a searchable combobox over ISO 3166 rather than free text, and drives entity routing and VAT expectations |
| 3 | phone and email, required | an international phone input with the country from step 2; the email error copy `Oops, e-mail is not valid.` |
| 4 | budget, required, four radios | labels `10K-20K`, `20K-30K`, `30K-60K`, `+60K`, mapped to `band_10_20k` through `band_60k_plus`, so the submitted identifier never disagrees with the label |
| 5 | kind, required, seven radios | `Website`, `Website with SEO and/or SEA`, `Digital Campaign`, `Search Engine Optimization`, `UX & Webdesign`, `Branding`, `Full Project` |
| 6 | message, required; specification, a PDF up to 8 MB; consent, required | the measured copy retained: `Attach or drop it here`, `File type : .pdf`, `Max. file size : 8MB`, `Wrong file type`, `Max file size exceeded`, `I agree with terms conditions and privacy policy` |

**Enquiry, `/say-hello/` and `/fr/contact/message/`:** two steps, last name, first name, email, phone and country,
then message and consent, all required.

**Application, `/apply/` and `/fr/carriere/candidature/`:** six steps, identity; `Job you apply for`; `Type of job`;
`Location`; the CV (required, PDF, 8 MB) and cover letter (optional); `Portfolio URL` and consent. The applicant
consent copy differs from the commercial one and states the retention period: applicant data is deleted after 24
months in France, following CNIL guidance, unless the candidate consents to a longer talent-pool retention.

**Wizard behaviour:**

- one step is one `<fieldset>` with a `<legend>`, the step container is the labelled region, and progress is a
  progressbar with its current value plus a visible `Step n of m`;
- validation on blur, never on keystroke; an error summary at the top of the step links to each invalid field; each
  message is wired to its input and the input marked invalid; advancing with an invalid step moves focus to the
  summary and announces it through a polite live region;
- back never loses data: state is held in memory and mirrored to session storage under a key namespaced by form and
  schema version, so a refresh mid-wizard resumes, cleared on success; consent is never persisted and must be given in
  the session that submits;
- the old unfocusable-field defect is not reproduced: inactive steps are hidden from the accessibility tree entirely
  rather than made unclickable while still focusable, focus moves to the new step's heading on change, the whole form
  completes by keyboard, and with JavaScript disabled it falls back to a single server-rendered page that posts;
- file upload is a real file input with a drag-and-drop overlay, never a styled container pretending; client checks of
  extension, type and size are hints and the server re-validates; progress, cancel, retry and remove are present, and a
  failed upload never loses the rest of the form;
- anti-abuse is invisible to people: the hidden decoy, a minimum time to submit, and a challenge only when the score is
  ambiguous, never on the happy path;
- submission is idempotent: the page generates a key per attempt and sends it as `Idempotency-Key`, so a double submit
  or a retry after a timeout returns the original result;
- offline, when the browser reports no network or the post fails with a network error, the payload is queued and
  replayed on reconnect, and the page says so plainly rather than spinning;
- success replaces the form with a confirmation naming the expected response time from the first-response SLA, the
  reference and what happens next, and the email confirmation comes from the entity that will handle the lead.

### Client portal

The portal answers four questions without a phone call: where is my project, what do you need from me, what have
I been billed, and is my site healthy. Every route is scoped by an organisation switcher, because a principal can
belong to more than one client organisation, a group with subsidiaries or an agency-of-record relationship.

| Route | Content |
|---|---|
| `/portal` | Needs you queue, project health, next milestone, open tickets |
| `/portal/projects` | list with a card and table toggle, filtered by status |
| `/portal/projects/{id}` | timeline, milestones, team, documents, activity feed |
| `/portal/projects/{id}/deliverables` | the project's deliverables |
| `/portal/deliverables/{id}` | viewer, annotation and the approval action |
| `/portal/approvals` | everything awaiting this principal, with due dates |
| `/portal/documents` | contracts, change orders, signed PDFs, DPA, sub-processor register |
| `/portal/invoices` | list, status, PDF and Factur-X download, dispute action |
| `/portal/tickets` | list, create, thread, with SLA state visible |
| `/portal/reports` | monthly SEO and SEA reports, archive, data-completeness note |
| `/portal/sites` | managed sites: uptime, vitals, TLS expiry, handover state |
| `/portal/settings/organisation` | users, roles, approval routing, SSO and SCIM configuration, for the `client_owner` only |
| `/portal/settings/profile` | locale, timezone, notification preferences, sessions |

A sidebar lists every section the principal may reach, and a new ticket, a request for access or a delegation opens
in a slide-over without leaving the list behind it.

**The overview is a queue, not a dashboard.** Its first block is `Needs you`: pending approvals, unanswered questions
on deliverables, overdue invoices, tickets waiting on the client, ordered by due date, each one click from action,
with charts below the fold. Approval cycle time is dominated by the client not knowing it was waiting on them.

**The deliverable viewer** is a split detail pane, the viewer beside a comment rail and an approval bar, handling four
kinds:

| Kind | Viewer | Annotation anchor |
|---|---|---|
| `design`, an image | zoom and pan canvas, fit to width by default | a normalised point or region |
| `document`, a PDF | paged renderer with a real text layer for search and selection | page plus normalised point, or a text range |
| `build_url` | a sandboxed responsive frame at three device widths, plus open in a new tab | a CSS selector plus a normalised offset within the element |
| `prototype` or video | a player with frame-accurate scrubbing | a timestamp in milliseconds |

It offers side-by-side version comparison with a diff affordance; the tray of comments from a previous version for
orphaned annotations; comment threads with mentions that respect visibility, where **an agency-internal note is never
visible to the client** because internal notes live in a separate channel the API never returns to client principals,
not a flag the interface filters; and an approval bar showing who else must approve and in what order, so nobody
approves believing they are the last gate when they are the second of three.

**Approvals are explicit and feel irreversible.** Approving asks for typed confirmation when the linked milestone's
value exceeds the organisation's confirmation threshold, states plainly `Approving this releases invoice for` and the
amount, and records the decision against the version hash. Rejecting requires a comment. Neither action is offered
to the principal who uploaded the version under review.

**Invoices** show status, due date, the tax treatment in plain language (`Reverse charge - VAT to be accounted for by
the recipient (Art. 196 VAT Directive)`), the PO reference where required, and downloads of the PDF and, where issued,
the Factur-X file; a `Dispute` action opens a ticket with the invoice attached and pauses dunning.

**Sites** show, per managed site, current status with the last 90 days as a compact uptime strip, p75 LCP, INP and
CLS trends, a TLS expiry countdown and handover state. This screen is the retainer's renewal argument, so it is
honest: a gap in the agency's own monitoring renders as a gap, never as uptime.

### Back office

The same shell with the agency route tree:

| Route | Content |
|---|---|
| `/portal/agency` | today: my tasks, my approvals, leads awaiting first response |
| `/portal/agency/leads` | triage queue with spam score, source and SLA countdown |
| `/portal/agency/pipeline` | opportunities board by stage, weighted forecast per entity |
| `/portal/agency/proposals/{id}` | the estimate builder: phases, roles, days, rate card, margin |
| `/portal/agency/contracts` | contracts, change orders, signature state |
| `/portal/agency/projects/{id}` | delivery board, capacity, burn against budget, margin |
| `/portal/agency/time` | a week timesheet grid, approvals, lock state |
| `/portal/agency/tickets` | a queue across all clients, SLA at risk first |
| `/portal/agency/invoicing` | the draft queue, issue runs, dunning, payment allocation |
| `/portal/agency/vault` | secrets by client and site, where every opening is a request flow |
| `/portal/agency/content` | editorial: entries, locales, translation state, publishing schedule |
| `/portal/agency/insights` | connector health, report runs, failures |
| `/portal/agency/recruitment` | the applicant pipeline |
| `/portal/agency/admin` | policies, roles, rate cards, calendars, IdPs, audit, DSRs, RoPA |

**Data grids** are the workhorse, one implementation everywhere: server-side keyset pagination (page 400 of the
leads table never scans 400 pages), column selection, saved views per principal, multi-select bulk actions that
traverse the same authorisation path as single actions and report partial failures per row, CSV export that is
audited and rate limited because bulk export of client data is an exfiltration path, sticky headers, horizontal
scroll inside their own container, and full keyboard operation with a roving focus inside the grid.

**The estimate builder** is where margin lives: it composes proposal lines from rate-card role times days, showing
cost, price and margin per line and in total. The margin column renders only when the policy engine grants
`commerce:read_cost`; it is not hidden with styling, and the API does not send the numbers.

**The vault screen never shows a secret in a list.** It lists labels, types, rotation status and last access.
Revealing one is request, approval, step-up and a time-boxed reveal with a visible countdown, clipboard-only copy
and automatic re-masking, and the screen states permanently that access is recorded.

### Accessibility

WCAG 2.2 AA on all three surfaces, verified rather than asserted:

| Area | Requirement |
|---|---|
| Landmarks | `header`, `nav`, `main` and `footer` on every page, exactly one `main`, and skip-to-content as the first focusable element on every route |
| Headings | one `h1`, no skipped levels, every landmark labelled |
| Focus | a visible ring on every interactive element, at least 3:1 against its background, never removed; focus is never lost on route change and moves to the new page's `h1` |
| Modals and sheets | a focus trap, Escape closes, focus returns to the trigger, the background is inert |
| Motion | the reduced motion preference is honoured by every primitive, including the smooth-scroll layer itself |
| Colour | never the sole carrier of meaning: status chips carry a label and a shape, uptime strips carry a pattern, required fields carry text |
| Live regions | one polite region for status and one assertive region for errors; a form error announces once, not per keystroke |
| Tables | real tables with header scope, sortable headers exposing their sort state, grids exposing row counts |
| Targets | at least 24 by 24 CSS pixels, and at least 44 pixels on touch surfaces |
| Zoom | usable at 400 per cent zoom, the equivalent of `320px`, with no horizontal page scroll |
| Media | captions for any speech, no autoplay with sound, and the pinned gallery's list alternative |
| Language | `lang` correct per document, language alternates present, and mixed-language runs such as `See live` or French client names inside English copy marked inline |

Keyboard-only traversal covers the six end-to-end journeys, and one screen-reader pass per release covers the brief
wizard, the deliverable viewer and the approval flow. An agency selling digital delivery to French public buyers is
measured against RGAA on the work it ships, and failing on its own site is a commercial liability as well as an
ethical one.

### Responsiveness

Eight measured breakpoints, mobile-first:

| Surface | Below `768px` | `768px` to `1199px` | `1200px` and wider |
|---|---|---|---|
| Public | a single column; the gallery unpinned; navigation as a full-screen overlay with a focus trap and scroll lock; WebGL never starts | two-column grids; the gallery pinned; fewer planes | the full experience, content capped at `1600px` with fluid gutters |
| Portal | stacked cards; grids become card lists; the primary action in a sticky bottom bar | master and detail collapse to stacked; the side navigation becomes a drawer | persistent side navigation, master and detail, the comment rail beside the deliverable |
| Back office | read-mostly; grids scroll horizontally inside their own container, never the page | compact grids | dense grids and multiple panes |

Container queries govern the components that appear at three intrinsic widths, the project card (gallery, related
rail, back-office grid), the invoice row and the ticket row, so each is correct at its own width rather than the
viewport's. A hover-capability query gates every hover-dependent affordance, and on touch `magnetic` and `hover-swap`
are not instantiated at all, so no phantom hover state can stick.

### States: loading, empty, error, offline, permission

Every data-bearing view specifies five states; a view with only a happy path is incomplete.

| State | Rule |
|---|---|
| Loading | skeletons matching the final layout's dimensions, keeping layout shift at most 0.05; never a full-page spinner on a route with a cached shell; actions show inline progress on their own button, disabled and marked busy, never removed |
| Empty | distinguishes nothing yet from nothing matches: `No invoices yet`, with the reason that no milestone is approved yet, is not `No results for status: overdue`, with a clear-filter action |
| Error | states what failed, whether it is retryable and what to do next, and carries the `request_id` so support can find it; never a raw stack trace and never a bare something went wrong where the failure is known |
| Offline | reads served from cache with a visible staleness marker and timestamp; writes queued where safe (comments, time entries, wizard steps) and refused with an explanation where not |
| Permission | a resource the principal may not see returns exactly what a non-existent one returns, and the interface says `Not found, or you do not have access`, offering a request-access action where a grant path exists |

Two rules with teeth:

- **nothing that moves money or grants access looks done before the server confirms it**: comments and annotations may appear at once,
  but approvals, invoice issue, grant creation and vault reveals show a real pending state and wait for the server,
  because an approval that appears to succeed and silently fails is the worst defect this system can ship;
- **every destructive action is either reversible or confirmed, and says which**: deleting a draft is undoable for
  10 seconds from its toast; voiding an invoice is not undoable and requires typed confirmation naming the document
  number.

### Defects found in the measured surface

Recorded because the replacement must not reproduce them.

| ID | Defect | Evidence | Severity |
|---|---|---|---|
| D-01 | every form input in the served HTML carried a negative tab index, so no field was in the natural tab order, and keyboard access to the forms depended on scripts or did not exist, failing WCAG 2.1 success criterion 2.1.1 in the served document | all three forms, every input and textarea | critical, accessibility |
| D-02 | no consent management on an EU property: `googletagmanager` and `gtag` loaded on the home page with no consent platform of any vendor | home HTML | critical, legal |
| D-03 | budget band value and label mismatch: the radio submitted `+50K` while its label read `+60K`, recording every top-band lead against the wrong band | `/start-a-project/` | high, data |
| D-04 | no `hreflang` on either domain: two properties in two languages with overlapping content and zero language annotation | both home pages, zero alternates | high, SEO |
| D-05 | a duplicate case study across domains with divergent URLs: `Bellamy Associes` under `/project/` and `/references/` with no canonical relationship | both sites | high, SEO |
| D-06 | two contact hubs with identical content: `/contact/` and `/contact-us/` both render the same three-action page, and navigation labelled one `Join the team`, which does not describe it | the English site | medium, information architecture |
| D-07 | `xmlrpc.php` and `wp-json` reachable on the French property: standard WordPress attack surface left open by an agency selling security-adjacent management | the French site | medium, security |
| D-08 | autocomplete turned off on all three forms, including name, email and phone, suppressing browser autofill exactly where it helps most, an accessibility and conversion cost with no stated benefit | all three forms | medium, accessibility and UX |
| D-09 | heading semantics were decorative: one `h1` followed by four `h2` marketing sentences on the home page, and no headings at all on the two form-bearing pages, leaving a screen-reader user no outline | the English site | high, accessibility |

### Evidence gaps

Each is resolved by a capture during delivery or is a deliberate decision point:

- the form submission contract: endpoint, method, nonce, rate limiting, success and error responses, handled inside
  the minified bundle and not extracted;
- the typography scale: exact sizes, line heights and letter spacing per role, and the complete fallback stack, of
  which only family names were captured;
- `MargoBeuys` licensing for web use, which must be confirmed before reuse;
- WebGL shader behaviour: the renderer was present, but the shaders, uniforms and the meaning of the scale and rotate
  attributes were not extracted;
- the case-study page schema: the sampled page showed a description, a service tag list, a `See live` link and a
  next-project link, and whether year, awards, team credits and metrics are modelled per project is unknown;
- the existing back office: whether the agency runs a CRM, a PSA, a time tracker or a billing tool today, and what
  must be migrated, is unknown from the public surface;
- real traffic and lead volume, with no analytics access, so capacity figures are derived from the stated scale and
  marked as assumptions;
- whether the two properties shared a database: the theme was shared and the content was not, making two installs the
  strong inference, though not proven.

### Quality engineering the product carries

Parallax is a system where most correctness is invisible in a demo, so its own engineering pipeline is part of the
product. The pyramid is weighted for this system:

| Layer | Coverage focus |
|---|---|
| Unit | tax determination, SLA arithmetic across calendars and DST, money arithmetic, state-machine guards, anchor remapping, spam scoring |
| Integration | every API endpoint against a real PostgreSQL with row-level security enabled, including the authorisation matrix |
| Contract | every inbound webhook against recorded real payloads; every outbound webhook against a schema |
| End-to-end | the six end-to-end workflows, in Playwright, at three viewports |
| Accessibility | axe-core on every route; keyboard traces on the six journeys; one manual screen-reader pass per release |
| Security | the cross-tenant enumeration suite, authorisation regression, upload safety, injection fuzzing |
| Performance | k6 against the API; Lighthouse CI against the public routes with the budgets as gates |
| Chaos | quarterly: kill the primary database, saturate the ingest queue, break VIES, make the e-signature provider return 500s, expire every token |

**Data correctness gates run nightly against production.** They check state, not code, and catch the failures that
only appear after months of real use:

| Gate | Property that holds |
|---|---|
| G-01 | invoice numbers per entity, document type and year form a contiguous set with no duplicates |
| G-02 | every contract's value equals its original value plus its approved change orders (CO-1) |
| G-03 | no milestone, time entry or overage appears on more than one invoice line (FIN-2) |
| G-04 | every payment allocation sums to no more than the payment amount and no more than the invoice total |
| G-05 | no active grant lacks an expiry, and no grant is active past its expiry |
| G-06 | every vault read in the last 24 hours has a matching approved request within its TTL |
| G-07 | the audit hash chain verifies from the last anchor to head |
| G-08 | no principal has an active membership in an organisation they were deprovisioned from |
| G-09 | every published content localisation has an `hreflang` sibling set consistent with its entry |
| G-10 | every historical published path resolves with 200 or 301, and none returns 404 |
| G-11 | no file referenced by a deliverable is in a scan state other than `clean` |
| G-12 | every `enterprise` organisation has a verified IdP domain or an explicit exception record |

**The six acceptance journeys** are the six end-to-end workflows, automated end to end, holding not only the happy
path but the named failure path in each: an infected upload, a blocked reverse charge, a superseded approval, a
break-glass denial with no second approver, SCIM deprovisioning within 60 seconds, and crypto-shred confirmation at
exit.

**Authorisation assurance** has four parts:

- **matrix generation**: the permission matrix is generated from the policy bundle, and a divergence between the
  document and the bundle fails CI (T-AUTH-09);
- **property-based checking**: for randomly generated principal and resource pairs, the API result matches the
  policy engine's decision, so the interface, the API and the engine can never disagree;
- **negative-space enumeration**: the cross-tenant enumeration suite described under security;
- **a regression corpus**: every authorisation bug ever found becomes a permanent case.

**A requirement is done** when the happy path works; all five interface states exist; the authorisation decision is
enforced in the API and reflected in the interface; the audit event is written; the failure path is handled and
exercised; the accessibility gate passes; telemetry is emitted; and the relevant nightly data gate covers it. Seven
of those eight are invisible in a demo, which is precisely why they are written down.

**The launch gate blocks, not merely flags**, on any of: a failing hard requirement from the success metrics; an open
critical or high accessibility defect on a public or portal route; any cross-tenant failure; J-17 reporting a consent
violation; an unrehearsed restore; or any of D-01, D-02, D-03 or D-04 persisting from the legacy surface.

### Work breakdown by difficulty

Difficulty here is not effort, size or line count. It is what kind of reasoning the work demands, and therefore
what a failure on it diagnoses.

| Tier | Definition | A failure becomes visible | Diagnoses |
|---|---|---|---|
| Medium | one surface, a bounded contract, correctness checkable by exercising it; demands completeness in states, validation, accessibility and edge inputs, not architecture | immediately, by using it | thoroughness: does the builder finish a thing, or ship the happy path? |
| Hard | cross-cutting: concurrency, money, third-party contracts, cache and authorisation interaction, or a data model that must hold under contention; correct-looking code is routinely wrong | under load, on retry, or at a boundary, often in production | systems judgment: does the builder know where correctness actually lives? |
| Expert | two or more legitimate constraints genuinely conflict and the reconciliation must be designed; there is no library call; the failure is legal, financial or organisational and surfaces months later | when a regulator, an auditor, a lawyer or an attacker looks | architectural reasoning under real-world constraint |

There are no easy items by construction: every candidate, such as rendering the trust wall, has been folded into a
requirement that carries state, authorisation, accessibility or data correctness with it. The distribution is 24
Medium, 22 Hard and 12 Expert, 58 in all. Each entry gives its area, its scope, the properties that hold when it is
complete, and for the harder ones why it sits in its tier.

#### Medium

- **M-01, Design token system and contrast gate**, frontend. The ten measured colours as semantic tokens, the single
  measured easing easeOutQuint, the four durations, the eight measured breakpoints and the fluid type scale as a
  clamp. Holds when every token resolves at all eight breakpoints; a contrast script proves every text and background
  pairing in `allowed_pairings` meets 4.5:1, or 3:1 at 24px and above, and fails the build otherwise; no hard-coded
  colour literal exists outside the token file; and `--fg-muted`, the lighter deep neutral, is structurally prevented
  from being used as portal body text. Why this tier: the naive implementation copies the measured palette into
  variables and ships a dark theme whose muted foreground is 2:1 on the page ground; the gate is the requirement.
- **M-02, Motion primitive library**, frontend. The eight primitives as declarative, reusable components on one easing
  and four durations. Holds when only `transform` and `opacity` animate; `will-change` is added on approach and removed
  on completion; every primitive has a reduced-motion collapse; 60 fps is sustained on a 2021 mid-tier Android on the
  home route; and every ScrollTrigger is destroyed on route change with no leak across 20 navigations. Why this tier:
  completeness under constraint; any one primitive is easy, and eight that share a lifecycle and all degrade
  correctly is not.
- **M-03, Scroll system and reduced-motion integration**, frontend. The smooth-scroll layer plus ScrollTrigger
  orchestration, anchor handling with hash updates and header offset, a refresh after fonts are ready, and complete
  teardown on navigation. Holds when in-page anchors land correctly; browser find-in-page can scroll to a match;
  toggling the operating system's reduced motion setting and reloading yields a fully static, fully navigable page
  with no scroll hijacking at all; and no layout shift follows font load. Why this tier: find-in-page and reduced
  motion are the two things smooth-scroll implementations routinely break, and both are invisible until someone
  specifically checks.
- **M-04, Public application shell and navigation**, frontend. A header with a scroll-state transition, a mobile
  full-screen overlay with focus trap and scroll lock, a language switcher that maps to the equivalent page on the
  other site rather than its homepage, a skip link, and a footer with the measured office data. Holds when opening the
  overlay shifts no layout; Escape closes it and restores focus; the language switcher resolves through
  `content_entries.key` and falls back to the other site's homepage only when no sibling exists, saying so; and
  keyboard traversal reaches every link.
- **M-05, Home page composition**, frontend. The eight measured home sections with the measured copy as seed content,
  corrected heading semantics (D-09), and the counter block. Holds when there is exactly one `h1`; no level is skipped;
  axe-core is clean at 360, 768 and 1440 pixels; counters animate on intersect and render their final values
  immediately under reduced motion; and the marquee pauses on hover and on focus.
- **M-06, Case study template and index**, frontend. The measured `Verdane` structure: description, service tags, the
  `See live` outbound link, a media sequence and the next-project link, plus the optional year, awards and results
  fields. Holds when it renders correctly with every optional field absent, which is the live site's actual state;
  outbound links carry `rel="noopener"` and an accessible opens-in-a-new-tab affordance; and video is muted,
  `playsinline`, poster-first, and never autoplays under reduced motion or `save-data`.
- **M-07, Service catalogue pages**, frontend and content. The nine measured service entries plus the French-only
  replatforming line, as content-driven pages with a shared template. Holds when adding a tenth service requires no
  code change; each page emits valid `Service` structured data; and the English and French variants are linked by
  `hreflang` derived from the content model.
- **M-08, Multi-step form engine**, frontend. One wizard engine driving all three measured forms, of 6, 2 and 6 steps,
  from a declarative schema. Holds when the entire flow is completable by keyboard only; inactive steps are `hidden`,
  not merely pointer-events none, so D-01 is not reproduced; focus moves to the new step's heading on advance; a
  refresh mid-wizard restores state; and with JavaScript disabled the form degrades to a server-rendered single page
  that posts and works. Why this tier: the live site's own implementation fails the first property on every field;
  this is where looking the same and working diverge most sharply.
- **M-09, Form validation and error presentation**, frontend. Per-field validation on blur, an error summary with
  in-page links, `aria-invalid` and `aria-describedby` wiring, live-region announcements, and the measured error copy
  verbatim. Holds when an error announces once, not per keystroke; the summary receives focus on a failed advance; and
  every message names the constraint, as in `Max. file size : 8MB`, never invalid input.
- **M-10, File upload component and client-side pre-checks**, frontend. A real file input with a drag-and-drop
  overlay, progress, cancel, retry and remove, and the measured constraint copy. Holds when dropping a `.docx` shows
  `Wrong file type` without clearing the rest of the form; a cancelled upload aborts the request rather than orphaning
  it; the component is operable by keyboard alone; and a failed upload never loses the wizard's other answers.
- **M-11, Consent banner and preference centre**, frontend. Granular purposes, reject-all as prominent as accept-all,
  a persistent footer link on both sites, and a re-prompt on a policy version change. Holds when no non-essential
  request fires before a decision, as the J-17 consent crawl proves; the banner is keyboard-operable and focus-trapped;
  declining is one click from the first screen; and withdrawal unloads what can be unloaded and takes effect
  immediately for everything else.
- **M-12, Accessibility remediation pass on the public surface**, frontend. Landmarks, heading order, focus
  management, target sizes, `lang` attributes including inline marking of French names in English copy, and the
  pinned gallery's list alternative. Holds when axe-core is clean on all public routes at three viewports as a
  blocking CI gate; a manual keyboard traversal of the home page reaches every interactive element including inside
  the pinned gallery; and 400 per cent zoom produces no horizontal page scroll.
- **M-13, Portal application shell**, frontend. The portal route tree, the organisation switcher, the notification
  centre, the command palette, responsive navigation, and affordances rendered from the decision set. Holds when
  switching organisation re-scopes every open view and clears cached data for the previous organisation; no
  affordance renders that the API would deny; and the shell renders a usable skeleton before data arrives.
- **M-14, Deliverable viewer**, frontend. The four deliverable kinds with zoom and pan, a paged PDF with a text layer,
  a sandboxed responsive iframe, and frame-accurate video scrubbing. Holds when pin placement is accurate at every zoom
  level and after a window resize; a 20 MB PDF shows its first page within 2 seconds; the iframe cannot script the
  parent; and the viewer is usable with the keyboard alone, including pin placement and navigation between pins.
- **M-15, Notification centre and preferences**, full-stack. An in-app centre, preferences per principal, per event
  class and per channel, quiet hours, and digest scheduling in the principal's timezone and locale. Holds when an
  organisation-level required notification cannot be disabled by the principal but is shown as enforced with the
  reason; digests respect timezone across a DST boundary; and marking read syncs across open tabs.
- **M-16, Data grid component**, frontend. One grid: keyset pagination, column selection, saved views, bulk actions,
  CSV export, sticky headers and horizontal scroll containment. Holds when page 400 of a 20 000-row table is as fast as
  page 1; bulk actions traverse the same authorisation path as single actions and report partial failures per row;
  the grid is fully keyboard-operable with a roving tabindex; and exports are audited and rate limited.
- **M-17, Time tracking**, full-stack. Week-grid entry, a running timer, submission, approval and period locking.
  Holds when a running timer survives a refresh and a laptop sleep; entries cannot be edited once locked; the sum of a
  day's entries cannot exceed 24 hours; and rate and cost are snapshotted at approval, so a later rate-card change
  does not alter approved entries.
- **M-18, Invoice document rendering**, backend. A deterministic PDF for both entities with correct statutory content,
  both locales, the tax note, the PO reference and payment instructions. Holds when the same invoice renders
  byte-identically twice; long line descriptions and 40-line invoices paginate correctly with totals on the final
  page; the French template carries the `Autoliquidation` mention when applicable and omits it otherwise; and PDF/A-3
  conformance validates for the Factur-X variant.
- **M-19, Global search**, full-stack. A command palette over organisations, projects, deliverables, tickets, invoices
  and content. Holds when permission filtering is applied inside the query; result counts never reveal inaccessible
  records (EC-28); names tolerate typos; and p95 stays under 200 milliseconds at 100 000 documents.
- **M-20, Transactional email templating**, backend. Localised templates for both entities with a plain-text
  alternative, the correct sender identity per entity, and one-click unsubscribe on anything marketing-shaped. Holds
  when every template renders in `en` and `fr` with no untranslated key; suppression is honoured across both entities;
  and a template referencing a missing variable fails at build, not at send.
- **M-21, Media pipeline**, backend and frontend. An AVIF, WebP and JPEG chain, responsive `srcset` with accurate
  `sizes`, LQIP, explicit dimensions, and an eager LCP hero with `fetchpriority`. Holds when CLS is at most 0.05 on
  every public route; the hero payload is at most 250 KB at desktop 1x; slow image loads shift no layout; and every
  image has meaningful `alt` or is explicitly marked decorative.
- **M-22, Managed-site health widget**, frontend. The uptime strip, vitals trends, the TLS countdown, handover state and
  honest gap rendering. Holds when a monitoring gap renders as a distinct visual state, never as uptime; the strip is
  readable without colour, with a pattern plus a label; and the widget renders correctly for a site with no data yet,
  and says why.
- **M-23, Audit log viewer**, frontend. Filters by actor, resource, action, outcome and time; a permalink to an event;
  signed export. Holds when a client principal sees only their own organisation's events; the before and after diff
  renders redacted fields as absent rather than as `null`; and exporting is step-up gated, audited and rate limited.
- **M-24, Client onboarding wizard**, full-stack. Create the organisation, set its governance profile, invite
  principals, configure approval routing, attach a rate card and billing entity, and generate the DPA. Holds when
  selecting `public_sector` makes the PO field mandatory on contracts and switches the e-invoicing channel to Chorus
  Pro with no code change; an incomplete onboarding is resumable; and the DPA and sub-processor register are attached
  and visible in the client portal immediately.

#### Hard

- **H-01, Authorisation layer**, backend. The policy decision point: bundle, decision API, obligations, decision log,
  a 30-second cache with mandatory bypasses, and a batch decision endpoint for the interface. Holds when the permission
  matrix is generated from the bundle and CI fails on divergence; property-based checks confirm the interface, API and
  engine never disagree; a revoked grant is denied on the next request despite the cache; and an explicit deny defeats
  every permit, including `group_admin`. Why Hard: the failure is silent and total; scattering role checks produces
  code that passes every feature check and leaks margin data to a client six weeks later.
- **H-02, Multi-IdP federated SSO**, backend. OIDC and SAML per client organisation, domain verification by DNS TXT,
  JIT provisioning, group-to-role mapping applied on every login, and certificate rotation. Holds when an assertion for
  an unverified domain is rejected; a domain claimed by two organisations escalates rather than resolving (EC-04);
  replayed SAML assertions are rejected; removing a user from a mapped group removes the role at next login; and clock
  skew of 2 minutes either way is tolerated and anything beyond it rejected.
- **H-03, SCIM provisioning and deprovisioning reconciliation**, backend. SCIM 2.0 `Users` and `Groups` with PATCH
  semantics, plus the hourly directory reconciliation job. Holds when `active=false` revokes every session, membership
  and grant within 60 seconds, verified end to end; reconciliation detects and reports drift and revokes on confirmed
  departure; deletion is treated as deactivation; and the reconciliation is idempotent and safe to run concurrently
  with live SCIM traffic.
- **H-04, Session and token lifecycle**, backend. Cookie sessions, rotating refresh tokens with reuse detection,
  step-up assertions, session listing and revocation, and absolute and idle timeouts differentiated by capability.
  Holds when a replayed refresh token revokes the whole family and alerts; a step-up older than 15 minutes is refused
  for vault and finance actions; revoking a session ends its open live connections at once; and no token
  appears in a URL, a log or an error body.
- **H-05, Tenant isolation, row-level security plus the enumeration suite**, backend. Row-level security on every
  tenant-scoped table, a session-scoped organisation context, and the automated cross-tenant enumeration suite. Holds
  when every route is covered and a new route without a case fails CI; organisation A receives `404` and a
  statistically indistinguishable latency for every organisation B resource; and disabling the policy layer in a
  build still yields zero cross-tenant reads, because row-level security holds independently.
- **H-06, Public intake anti-abuse**, backend. The composite spam scorer, layered rate limits, the global circuit
  breaker, and Turnstile escalation only in the ambiguous band. Holds when a scripted submission at 100 per minute is
  blocked without affecting a genuine concurrent submission from another IP; no CAPTCHA appears on the happy path;
  scores and their contributing signals are stored and reviewable; and false positives are recoverable: a human can
  reclassify, and the lead re-enters the funnel with its SLA recomputed.
- **H-07, Upload safety pipeline**, backend. A presigned two-step upload, a quarantine bucket, magic-byte MIME
  detection, antivirus, PDF active-content checks, promotion, and signed single-use download URLs. Holds when a PHP
  file renamed `.pdf` is rejected at the server despite passing client checks; a quarantined file is unreachable by
  every application path; a download URL cannot be replayed; and the `8MB` limit is enforced by the presigned policy,
  not only by the client.
- **H-08, Attribution and offline conversion export**, backend. First-touch and last-touch capture, consent-gated
  `gclid` storage, lead-to-conversion mapping, and export to Google Ads. Holds when, with marketing consent declined,
  no `gclid` is stored and no export occurs, as the consent crawl proves; a lead converting 60 days after first touch
  still exports with the correct conversion time; duplicate exports are idempotent; and attribution survives a session
  that crosses both sites.
- **H-09, Proposal to contract with e-signature**, backend. Envelope creation, ordered routing, webhook verification,
  tolerance of out-of-order events, artefact storage and the human-override path. Holds when `completed` arriving
  before `delivered` is reconciled, not rejected (EC-21); a replayed webhook produces one state change; a contract
  becomes `active` only when the signed artefact and completion certificate are stored; and the manual override is a
  distinct, step-up-gated, separately audited action.
- **H-10, Milestone billing engine**, backend. `milestone.approved` becomes a draft invoice; retainer runs; time and
  materials runs from approved unlocked time; overage with a rollover policy. Holds when replaying `milestone.approved`
  ten times produces one draft, unique on `milestone_id`; FIN-2 makes double billing structurally impossible; a time
  entry approved after a period lock rolls forward (EC-08); and a retainer's overage calculation is reproducible from
  stored inputs months later.
- **H-11, Multi-entity invoice numbering and issue**, backend. The invoice issue order with per-entity, per-year,
  per-document-type gapless sequences. Holds when 50 concurrent issues across both entities produce 50 contiguous
  numbers with no duplicates and no gaps (EC-01); a failure in PDF rendering leaves the number assigned and the invoice
  issued, never rolled back; and J-13, run over a database holding a deliberately introduced gap, reports that gap
  rather than hiding it.
- **H-12, VAT determination engine**, backend. The tax treatment matrix, dated rate tables, VIES integration with
  caching, negative-result handling and explicit unavailability behaviour. Holds when a reverse charge cannot be
  applied on an `invalid` VAT number; a VIES timeout blocks issue unless a validation under 90 days old exists (EC-06);
  re-issuing a document dated in a prior rate period uses that period's rate; and the treatment and rate are
  snapshotted and never recomputed on read.
- **H-13, Approval workflow engine**, backend. Durable multi-stage workflows with `any_of`, `all_of` and `quorum`,
  delegation, calendar-aware timers, escalation, separation of duties and pinned policy versions. Holds when a deploy
  mid-approval does not lose a timer; a reminder scheduled for 48 business hours does not fire on a French public
  holiday; the uploader of a version cannot approve it; escalation never grants authority beyond a principal's
  threshold; and editing a policy does not alter in-flight approvals (EC-16).
- **H-14, Deliverable versioning and annotation remapping**, backend and frontend. Normalised anchors, version
  supersession, remapping on a new version, the orphan tray, and approval cancellation on upload. Holds when, across a
  version change that moves content, an anchor is either remapped correctly or marked `orphaned`, never silently
  repositioned; no annotation is ever lost; and a pending approval is cancelled with a stated reason when a new version
  lands (EC-02).
- **H-15, SLA timers across business calendars**, backend. Event-sourced clocks, per-calendar business time, pause and
  resume, reopen semantics and breach detection. Holds when the remaining budget is a pure function of the event log
  and is identical after a process restart; French and Maltese holiday sets produce different deadlines for identical
  tickets; a resolve-then-reopen restores the remaining budget, not a fresh one; and DST transitions in both timezones
  are covered (EC-25).
- **H-16, Monitoring ingest and alert confirmation**, backend. Probe scheduling across regions, telemetry ingest into
  the monitoring tables, beacon HMAC verification, multi-region confirmation and rollups. Holds when a single-region
  fault produces no alert (EC-11); 4.5 million checks a day sustain without affecting p95 API latency; a replayed beacon
  is rejected; and a confirmed outage opens a `p1` ticket within 90 seconds of the third failed check.
- **H-17, Analytics connector framework**, backend. OAuth with vault-stored tokens, pre-emptive refresh, per-provider
  quota buckets, backoff, sampling and finality metadata, and revocation handling. Holds when a revoked connector
  raises a task and stops retrying; a 429 storm from one client does not delay the other 399, shown under a synthetic
  burst; the last three days are re-fetched and snapshots flip to `is_final` correctly; and no token exists in
  plaintext anywhere in the application database.
- **H-18, Report generation pipeline**, backend. Scheduled and on-demand runs, deterministic composition, completeness
  reporting, PDF and portal rendering, and an archive. Holds when the same period regenerated later produces the same
  numbers or an explicit revised marker with a diff; a missing data source yields a partial report that names the gap
  rather than zeros (EC-10); a run is unique per definition and period and safe to retry; and 400 clients' monthly runs
  complete inside the batch window.
- **H-19, Outbox, event bus and outbound webhooks**, backend. A transactional outbox, an ordered relay, consumer
  idempotency, signed outbound delivery with a retry ladder, replay, and endpoint auto-disable. Holds when killing the
  relay mid-batch loses no event and duplicates none after restart; a receiver returning 500 for 24 hours is disabled
  and the client notified; signature verification is demonstrated against a reference implementation; and
  per-aggregate ordering holds under concurrent producers.
- **H-20, Multi-locale, multi-site content publishing**, backend and frontend. The content model rendering both sites,
  scheduled publishing, preview, derived hreflang and canonicals, automatic alias creation and sitemap generation.
  Holds when D-04 and D-05 are structurally impossible, because a published localisation without a correct alternate
  set fails G-09; changing a slug creates a 301 and never a 404 (EC-18); every legacy URL enumerated in the measured
  surface inventory resolves after launch; and concurrent edits conflict rather than overwrite (EC-22).
- **H-21, Landing matrix generation and governance**, backend. Generation of the service by city grid from templates
  plus city-specific evidence, similarity scoring, the `indexable` gate and weekly re-evaluation. Holds when a page
  below the uniqueness threshold is `noindex` and queued (EC-19); the threshold is configurable and its effect is
  demonstrable; expanding to a third city requires no code change; and the sitemap never contains a `noindex` page.
- **H-22, Caching and invalidation**, backend and edge. Incremental regeneration with surrogate keys, the cache layers,
  materialised aggregates, and client-side stale-while-revalidate with ETags. Holds when publishing a case study
  invalidates exactly the pages that embed it, in under 30 seconds, and nothing else; every cache key includes the
  organisation scope and the policy bundle version; a cache-warming job cannot warm an entry the requesting principal
  could not read; and a stale-served page carries a visible timestamp in the portal.

#### Expert

These are the places where the system either holds or does not, and where no library call resolves the conflict.
Each names the two constraints that genuinely oppose each other.

- **E-01, Credential vault and privileged access management.** In conflict: an on-call developer must fix a client's
  production site at 03:00 in under ten minutes, and no principal may ever hold standing access to 400 businesses'
  production credentials. Scope: envelope encryption with per-organisation KEKs in the key service; the request,
  approve, step-up and time-boxed reveal flow; the two-person break-glass rule; log before plaintext; no bulk export
  path; rotation tracking; automatic rotation flagging when a principal who revealed a secret departs; and quarterly
  access attestation. Holds when a full dump of the vault database plus the application database yields no plaintext
  and no usable key; no code path returns more than one secret per request, shown by an enumeration over the whole
  route table; a break-glass request with no available second approver is denied and recorded, not escalated into an
  automatic override (EC-24); every reveal in a 30-day window reconciles one to one with an approved request inside its
  TTL (G-06); and revoking a departed principal's access automatically creates rotation tasks for every secret they
  touched (EC-23). Why Expert: every individual control is implementable; the design problem is making the emergency
  path fast enough that nobody builds a shadow credentials spreadsheet, while keeping it strong enough that a phished
  account cannot drain the vault; get the balance wrong in either direction and the control fails silently, in the
  direction of the humans' convenience.
- **E-02, GDPR processor programme and DSR fan-out.** In conflict: a data subject's erasure right is near-absolute, and
  accounting, contractual and audit records must survive erasure for up to ten years. Scope: the controller and
  processor split applied per activity; the RoPA; the sub-processor register with change notification; DSR intake,
  verification, fan-out across nine storage systems and an itemised response; the retention schedule with automated
  enforcement; and backup-aware erasure with a suppression list. Holds when an erasure request from a person who is
  both a marketing contact and a contract signatory erases the former and retains the latter, and the response says
  exactly which and why (EC-13); every system searched is recorded, and an unrecorded system fails the completeness
  check; a restored backup cannot resurrect an erased subject; and the sub-processor register is provably complete
  against the deployed infrastructure (T-GOV-03). Why Expert: the naive implementation deletes rows and creates an
  accounting hole, the paranoid one refuses erasure and creates a regulatory finding, and the correct answer is a
  per-field legal basis map that no framework provides.
- **E-03, Consent enforcement architecture.** In conflict: the agency's own business model depends on attribution and
  conversion measurement, and an EU visitor must be able to decline all of it with one click and have that decision
  provably honoured. Scope: server-authoritative consent state; the tag loader gated on a signed cookie; Consent Mode
  v2 signalling; consent as an input to the data model, so no `gclid` capture, no attribution detail and no offline
  export without consent; the J-17 crawl as a deploy gate; and withdrawal semantics including deletion of data
  collected under prior consent (EC-20). Holds when, with consent denied, a headless crawl of every public route fires
  zero non-essential requests and a failure blocks deployment (metric 11); with consent granted then withdrawn,
  previously stored `gclid` and attribution detail are deleted within 24 hours; and the stored proof for any visitor
  reconstructs exactly what they were shown and what they chose. Why Expert: the live site's current state (D-02) is
  what happens when this is treated as an interface task; doing it properly means accepting a measurable
  revenue-attribution loss and designing the funnel to work without the data, a product decision expressed in
  architecture.
- **E-04, Multi-jurisdiction invoicing and French e-invoicing.** In conflict: two legal entities in two jurisdictions
  must share one delivery pipeline and one client base, and each jurisdiction's invoice must be independently valid,
  sequenced and transmissible under its own rules. Scope: per-entity gapless sequences; the treatment matrix; dated
  rates; Factur-X generation with PDF/A-3 conformance; transmission through a registered platform; Chorus Pro routing
  with SIRET, service code and engagement number; typed asynchronous rejection handling; and correction by credit note
  only. Holds when a public-sector invoice cannot be issued without a PO; a rejection from Chorus Pro leaves the invoice
  issued and valid with a typed reason and a correction path that never reuses the number; Factur-X output validates
  against the standard's schema and the PDF/A-3 profile; and G-01 holds across both entities after a chaos run that
  kills the process mid-issue. Why Expert: the conflict is between engineering's instinct to roll back on failure and
  tax law's requirement that an issued number never disappears; the correct design commits the number and tolerates
  a broken downstream, which feels wrong until you understand why.
- **E-05, Data residency, sub-processor topology and the EU-only guarantee.** In conflict: enterprise clients demand a
  contractual EU-only guarantee, and the best tools for monitoring, error tracking, email and AI assistance are
  predominantly US-operated. Scope: EU-region primaries for every store including backups and logs; a vendor decision
  record per sub-processor with a transfer impact assessment where relevant; CI enforcement that a new outbound
  data-handling destination cannot ship without a register entry; per-region log isolation; and an architecture that
  keeps client PII out of the tools that cannot be pinned to the EU. Holds when an infrastructure audit enumerates
  every data-handling destination and each maps to a register entry; a deliberately introduced call to a non-registered
  vendor fails CI; and the DPA's residency claim is verifiable from the deployment manifests rather than asserted in
  prose. Why Expert: this constrains tooling choices for the whole build and must be enforced mechanically, because a
  single well-meaning error-tracker call carrying a user object breaks the contractual guarantee for 400 clients at
  once.
- **E-06, Access lifecycle across five principal kinds.** In conflict: delivery needs freelancers onboarded in hours
  and client staff self-serving their own teams, and the system must guarantee that nobody retains access one day
  past their entitlement. Scope: grants with mandatory expiry; delegation without transitivity; the SCIM-driven client
  lifecycle; agency offboarding; contractor project scoping; partner white-label boundaries; quarterly attestation; and
  the reconciliation job as detection, with enforcement at decision time. Holds when metric 9 holds, zero principals
  retaining any grant 24 hours after offboarding, as G-05 and G-08 show against seeded departures across all five
  principal kinds; a delegated approver cannot re-delegate; a contractor whose grant expires mid-session is denied at
  the next decision, not at the next login (EC-09); and attestation gaps expire grants automatically. Why Expert: the
  failure is invisible by construction, since nothing breaks when access lingers, which is why it lingers; detecting it
  requires modelling entitlement as a first-class, expiring relationship rather than as a row someone remembers to
  delete.
- **E-07, Client asset custody and exit.** In conflict: the agency must retain enough to defend a dispute and meet its
  own retention duties, and a departing client is entitled to full portability and to know that the agency no longer
  holds the keys to their business. Scope: the exit checklist; handover with client confirmation; crypto-shredding by
  KEK destruction; provider-side connector revocation with stored evidence; the portability export; the exit
  certificate; and the retention carve-outs that survive. Holds when, after exit, no code path can decrypt that
  organisation's secrets, shown by attempting a reveal and receiving a cryptographic failure rather than an
  authorisation failure; connector revocation is confirmed at the provider, not merely locally; the export is complete
  and machine-readable; and the certificate itemises what was destroyed, what was retained, on what basis, and until
  when. Why Expert: most systems have no exit path at all, so the data quietly stays forever; designing destruction
  that is provable, partial and legally survivable is architecture, not cleanup.
- **E-08, Audit integrity and evidential value.** In conflict: the audit log must be append-only and tamper-evident
  even against a compromised administrator, and it must be queryable at interactive speed, retained for seven years,
  and free of PII that the retention schedule requires erasing. Scope: hash chaining; periodic signed anchors exported
  to object-lock storage; monthly partitioning; per-jurisdiction retention; PII-redacted diffs whose redaction does not
  break the chain; the verification job; signed export for a client or a regulator; and client-facing audit
  visibility. Holds when modifying any historical row is detected by J-16 within the hour and pages as SEV-1 (G-07); a
  signed export verifies independently of the system that produced it; erasing a data subject does not invalidate the
  chain; and querying a specific resource's 7-year history returns in under a second. Why Expert: hash chaining is
  easy; hash chaining while satisfying erasure requests, redacting PII, partitioning for performance and remaining
  independently verifiable is a set of requirements that pull against each other, and the reconciliation is the
  deliverable.
- **E-09, Contract, delivery and billing three-way reconciliation.** In conflict: the signed contract is the legal
  source of truth, delivery reality diverges from it constantly, and billing must follow both without the three ever
  silently disagreeing. Scope: invariant CO-1; change orders as the only path to commercial change; milestone-to-line
  traceability; scope-drift detection for delivered work with no contractual basis; unbilled-approved detection; and
  the nightly reconciliation with its exception queue. Holds when G-02 and G-03 hold under concurrent change-order
  approval and invoicing; work logged against a milestone whose contractual basis was removed by a negative change
  order is surfaced as an exception rather than absorbed; and every invoice line traces to a contractual authority,
  with the trace renderable for a client dispute. Why Expert: this is the reconciliation agencies lose money on and
  that no off-the-shelf tool models, because it requires holding three inconsistent truths simultaneously and making
  the inconsistency visible rather than resolving it prematurely.
- **E-10, Supply-chain incident response.** In conflict: a compromise of agency-held access is simultaneously the
  agency's incident and an incident inside 400 other companies, with the agency as processor owing notification to
  each affected controller on a clock. Scope: detection signals; the SEV-1 playbook of revoke, freeze, rotate, notify
  and preserve; blast-radius computation from the vault access log, meaning which principal could reach which secrets
  over which window; per-client notification with contractual timelines tracked; evidence preservation of the audit
  chain segment; and post-incident rotation verification. Holds when, given a compromised principal id and a time
  window, the system produces the exact list of affected clients, sites and secrets in under five minutes;
  notification clocks start automatically and are tracked per controller; a tabletop exercise executes the playbook
  end to end; and rotation completeness is verifiable afterwards rather than assumed. Why Expert: the blast radius must
  be computable, which forces decisions about access-log completeness and secret-to-site mapping months before any
  incident; a system that cannot answer what they reached turns a contained incident into a total one.
- **E-11, Revenue recognition across entities and commercial models.** In conflict: cash timing, meaning deposits,
  milestone invoices and monthly retainers billed in advance, bears no relationship to when revenue is earned, and two
  entities in two jurisdictions must each produce defensible periodic accounts from the same delivery data. Scope: a
  recognition method per commercial model (milestone, percent-complete from approved time, straight-line for
  retainers); deferred and accrued balances per period; intercompany allocation when a French project is delivered
  partly by Maltese staff; period close with immutability; and restatement by explicit adjustment only. Holds when,
  for every contract and period, recognised plus deferred plus accrued reconciles to invoiced and to delivered; a
  closed period cannot be mutated by a late time entry (EC-08), only adjusted forward with a visible link; the same
  delivery data produces consistent results under both entities' reporting; and a percent-complete contract whose
  estimate is revised restates prospectively, not retrospectively. Why Expert: correctness here is defined by
  accounting standards rather than by checks an engineer would naturally write, and the wrong model goes undetected
  until an accountant looks at year-end.
- **E-12, AI-assisted content governance and GEO.** In conflict: the French site already competes on GEO and E-E-A-T,
  measured through articles at `comment-choisir-une-agence-geo` and
  `e-e-a-t-le-guide-complet-pour-gagner-en-credibilite` and `GEO` in the site title, so AI-assisted production at
  scale is commercially necessary, and the agency's entire credibility rests on the claim that its content
  demonstrates genuine experience and expertise. Scope: provenance on every content version (`ai_assisted`, the model
  and the human reviewer); a review gate so no AI-assisted content publishes without a named human reviewer;
  factual-claim tracking with a source for every statistic, client name and result figure published; the uniqueness
  gate of H-21 extended to AI-generated drafts; a disclosure policy; and structured data plus authorship signals that
  are true rather than decorative. Holds when every published article carries a provenance record naming a human
  reviewer; a claim published without a source fails the pre-publish check; AI-generated drafts cannot reach
  `published` through any path that skips review; the landing matrix cannot be filled by generation alone, because
  H-21's gate holds against AI-authored bodies; and a content audit can reconstruct, for any paragraph, who wrote it,
  what assisted, who checked it and against what source. Why Expert: the conflict is commercial; every control here
  reduces output volume, and the argument for them is a reputational risk that has not happened yet, so the actual
  engineering problem is making the safe path the fast path rather than a checklist people route around under
  deadline.

**What the distribution diagnoses:**

| Tier | Count | Concentrated in |
|---|---|---|
| Medium | 24 | frontend completeness, component correctness, state coverage, accessibility |
| Hard | 22 | authorisation, identity, money, third-party contracts, concurrency, caching, content integrity |
| Expert | 12 | credential custody, compliance, multi-jurisdiction finance, access lifecycle, incident blast radius, content governance |

A builder that completes all 24 Medium items and no Hard ones is a component builder, trusted with the public site
under review. Adding the Hard tier makes a product engineer, trusted with the portal while anything touching money
or access is still reviewed. Only the Expert tier distinguishes a systems architect, and those twelve are
deliberately the ones where a plausible-looking implementation is wrong in a way that surfaces months later, in
front of an auditor, a regulator, a client's security team, or an attacker.

### Delivery phases

Sequenced so that each phase is independently useful and nothing later invalidates something earlier; the order is
driven by dependency, not visibility.

| Phase | Duration | Contents | Exit criteria |
|---|---|---|---|
| 0, Foundations | 3 weeks | repository, environments, CI, module boundaries and their lint rules, PostgreSQL with row-level security scaffolding, the observability baseline, design tokens (M-01), the motion library (M-02, M-03) | a trivial endpoint deployed with tracing, structured logs and row-level security active, and a failing contrast gate proven to block a merge |
| 1, Identity and authorisation | 4 weeks | H-01, H-02, H-04, H-05, the principals, organisations and grants schema, the enumeration suite | the permission matrix generates from the bundle; the cross-tenant suite is green; SSO works against a test IdP |
| 2, Public presence | 5 weeks | H-20, M-04 to M-07, M-12, M-21, H-22, plus H-21 and M-11 | both sites render from the content model; every legacy URL resolves; axe gates are green; J-17 passes with consent denied; G-09 and G-10 are green |
| 3, Intake | 3 weeks | M-08, M-09, M-10, H-06, H-07, H-08, the lead schema and routing, M-20 | the three measured forms are rebuilt, keyboard-complete and spam-resistant, with D-01 and D-03 verifiably fixed; the first-response SLA is instrumented |
| 4, Commercial core | 5 weeks | rate cards, M-16, the estimate builder, H-09, contracts and change orders, the opportunity pipeline | a lead becomes a signed contract end to end, including a webhook-driven signature with out-of-order events |
| 5, Delivery and review | 5 weeks | projects, milestones, tasks, M-17, M-14, H-14, H-13, M-13 | the deliverable to invoice journey completes to milestone approval, including EC-02 and separation of duties |
| 6, Finance | 5 weeks | H-10, H-11, H-12, M-18, payments, allocation, dunning, E-04 | G-01 through G-04 are green under a chaos run; a Factur-X invoice validates; a Chorus Pro rejection is handled |
| 7, Custody | 4 weeks | E-01, the vault service, M-23, E-08 | a full database dump yields no plaintext; G-06 and G-07 are green; the break-glass tabletop is executed |
| 8, Retained services | 4 weeks | H-15, H-16, tickets, M-22, H-17, H-18, connectors | an outage in a trial site opens a `p1` ticket within 90 seconds; a monthly report generates with an honest data gap |
| 9, Governance | 4 weeks | E-02, E-03 completion, E-05, E-06, retention jobs, the DSR module, the RoPA | a seeded DSR fans out across all nine systems; the retention dry-run is signed off; the residency audit passes |
| 10, Enterprise readiness | 3 weeks | H-03, approval routing by unit, governance profiles, E-09, E-11, the E-10 playbook | the enterprise onboarding journey completes including 60-second deprovisioning; the blast-radius query returns in under 5 minutes |
| 11, Hardening and launch | 3 weeks | E-07, E-12, chaos, a penetration exercise, restore rehearsal, migration of legacy content and URLs | the launch gate is satisfied with no exceptions |

Roughly 48 weeks for a small team, with phases 2 and 3 and phases 5 and 6 parallelisable across a frontend and a
backend track. Phases 0 and 1 are not parallelisable with anything: an authorisation layer retrofitted after five
phases of features is the single most expensive mistake available on this project.

### Assumptions, decisions and open questions

**Assumptions:**

| # | Assumption | Impact if wrong |
|---|---|---|
| A-1 | the two properties are separate WordPress installs sharing a theme, the eighth evidence gap | if they share a database, migration is simpler; the target model is unaffected |
| A-2 | the agency has about 400 active client relationships, not 400 lifetime projects | vault, monitoring and connector capacity are sized on this; a lifetime figure would reduce load about fourfold |
| A-3 | the traffic and lead volumes of the load model | budgets and infrastructure sizing; the architecture holds at ten times without redesign |
| A-4 | both entities invoice in EUR only | a GBP or CHF client would require multi-currency on invoices and revenue recognition, which the schema supports but no logic implements |
| A-5 | retainer clients grant credential access rather than delegating through their own IAM | where a client offers scoped access instead, that is strictly better and the vault holds fewer secrets |
| A-6 | award-recognised work implies design-led delivery where visual approval is contractual | drives the weight given to the review module |
| A-7 | the `Partnership` option in the measured application form indicates real subcontractor relationships | justifies `partner_org` and white-label boundaries |
| A-8 | French e-invoicing obligations apply to the French entity on the timetable currently legislated | the timing of E-04, not its design |

**Decisions taken in this document:**

| # | Decision | Rationale | Alternative rejected |
|---|---|---|---|
| DEC-1 | Tier 3, not Tier 2 | the tier classification | Tier 2 would omit the vault, federated identity and audit integrity, which are the actual risks |
| DEC-2 | a modular monolith with three extractions | the system shape | microservices: 20 employees, and the hard problems are transactional |
| DEC-3 | a policy engine, not role checks | the policy decision point | scattered conditionals cannot express the real rules and cannot be audited |
| DEC-4 | PostgreSQL as the finance ledger, Stripe as a rail | payments and e-invoicing | Stripe as ledger cannot produce jurisdiction-correct gapless documents |
| DEC-5 | a content model with derived hreflang | the content model | two CMSs, which is the current state and the cause of D-04 and D-05 |
| DEC-6 | the vault as a separate service and database | the system shape | same-database storage makes any application bug a credential-disclosure bug |
| DEC-7 | ClickHouse for telemetry in the reference design, realised as PostgreSQL tables here | the stores mapping | PostgreSQL alone would work at launch volume and fail by month six in the reference deployment |
| DEC-8 | no auto-approval on timeout, ever | the approval engine | convenient, and indefensible the first time it is disputed |
| DEC-9 | consent gates the data model, not just tags | consent | tag-only gating still collects `gclid` server-side and is a violation with extra steps |
| DEC-10 | WebGL as an enhancement over a real DOM | the WebGL layer | canvas-only would be inaccessible and invisible to search and AI crawlers |
| DEC-11 | a human issues invoices; the system only drafts | billing triggers | auto-issue removes the last human check before a legal document exists |
| DEC-12 | semantic colours introduced and flagged, not invented silently | the design tokens | pretending they were measured would corrupt the evidence base |

**Open questions**, recorded with their owners and not blocking this build:

| # | Question | Blocks | Owner |
|---|---|---|---|
| OQ-1 | what CRM, PSA, time-tracking and accounting tools are in use today, and what must be migrated, the sixth evidence gap | phases 4 and 6, and migration scope | agency operations |
| OQ-2 | which clients are contractually `enterprise` or `public_sector`, and what their existing DPAs and security schedules already commit to | governance profiles, phase 10 | legal and account directors |
| OQ-3 | whether `MargoBeuys` is licensed for web use at the required volume, the third evidence gap | M-01, phase 0 | design |
| OQ-4 | whether the agency currently holds client production credentials, and where | E-01 migration, and the size of the immediate risk | security officer |
| OQ-5 | which e-invoicing platform the French entity will register with, and whether any clients already receive through Chorus Pro | E-04 | finance |
| OQ-6 | whether the English site becomes a global English site with the French site as a French market site, or both carry both languages | the H-20 URL strategy and the redirect map | marketing |
| OQ-7 | what the actual form submission endpoint and volume are today, the first evidence gap | migration of historical leads, and anti-abuse tuning | agency operations |
| OQ-8 | whether the 400 companies that trust us are active relationships or a lifetime count (A-2) | capacity sizing | agency operations |
| OQ-9 | whether the agency wants the client-facing API in v1 for its enterprise clients | rate-limit design is already in place; the endpoints are not | product |

**What would change the tier.** If the agency dropped retained services and credential custody, stopped serving
public-sector and listed clients, and consolidated to a single legal entity, this would become a Tier 2 product: a
proposal-to-invoice tool with a client portal. Three of the twelve Expert items would disappear entirely (E-01, E-04,
E-10) and four more would collapse to Hard. That counterfactual is the clearest statement of what makes this system
Tier 3: it is not the size of the agency, it is the concentration of other organisations' risk inside it.

### Evidence log

All observations were captured on 2026-09-01 from the live properties by direct HTTP fetch of the served HTML, the
theme stylesheet and the theme JavaScript bundle, with a desktop Chrome user agent, followed by static extraction. No
JavaScript was executed, which is why runtime behaviour such as form submission and WebGL shader detail appears as an
evidence gap rather than as a measurement.

**Artefacts fetched** (the legacy English property's paths, the legacy French property's home, and the theme files
under `wp-content/themes/`):

| Artefact | Path | Size |
|---|---|---|
| English home | `/` on the English property | 123 461 bytes |
| English services | `/our-services/` | fetched |
| English about | `/about-us/` | fetched |
| English projects index | `/projects/` | fetched |
| English case study sample | `/project/verdane/` | fetched |
| English contact hub | `/contact/` | fetched |
| English brief form | `/start-a-project/` | 48 985 bytes |
| English enquiry form | `/say-hello/` | 41 263 bytes |
| English application form | `/apply/` | 48 779 bytes |
| French home | `/` on the French property | fetched |
| Theme stylesheet | the theme's `dist/styles/main.css` | 191 379 bytes |
| Theme script | the theme's `dist/scripts/main.js` | 228 122 bytes |

**Extraction results by claim:**

| Claim | Source | Method |
|---|---|---|
| the colour frequency table | `main.css` | a regex over six-digit and three-digit colour literals, counted |
| the single easing easeOutQuint, 512 occurrences | `main.css` | a regex over easing declarations, deduplicated by value |
| duration frequencies | `main.css` | a regex over `transition:` shorthands, seconds captured |
| eight breakpoints with counts | `main.css` | a regex over screen minimum-width media queries |
| the hover-capability query, 23 occurrences | `main.css` | a direct count |
| font families `MargoBeuys`, `Poppins` and `Arial` | `main.css` | a regex over `font-family` declarations |
| libraries: GSAP (30), ScrollTrigger (9), OGL (14), Splitting (3) | `main.js` | identifier fingerprint counts |
| jQuery 3.7.1 with migrate 3.4.1 | English home | `wp-includes` script tags with a `ver=` query |
| the theme name | all pages | `wp-content/themes/` path extraction |
| the home section list and `data-scroll-*` attributes | English home | `<section>` tag extraction with attributes |
| a height of fifteen viewport heights on the project gallery | English home | the inline `style` attribute on `b-project-gallery` |
| `data-scale="1.044"`, `data-rotate="0.1"`, `data-webgl-offset="0, 80%"` | English home | attributes on `c-intro` |
| the class prefix convention (`c-`, `b-`, `e-`, `u-`) | English home, form pages | a class attribute survey |
| all form fields, types, `required` and radio values | the three form pages | input, textarea and label extraction inside each form |
| form micro-copy strings | the three form pages | the tag-stripped inner text of each form |
| step counts of 6, 2 and 6 | the three form pages | a count of `.c-form-page`, with `u-pe-n` marking inactive steps |
| a negative tab index on every input (D-01) | the three form pages | present on all 22 field controls surveyed |
| the budget value and label mismatch (D-03) | `/start-a-project/` | the radio value `+50K` against the displayed label `+60K` |
| no consent platform, analytics present (D-02) | English home | a fingerprint scan for 12 known consent-platform vendors returned zero; `gtag` twice, `googletagmanager` three times |
| no `hreflang` (D-04) | English home, French home | zero language-alternate link elements on either |
| 17 English case-study slugs | `/projects/` | `href` extraction on `/project/` links |
| 9 French case-study slugs, 16 matrix paths, 5 service pages | French home | `href` extraction, deduplicated |
| the duplicate `bellamy-associes` case study (D-05) | both indexes | the slug appears under `/project/` and `/references/` |
| `xmlrpc.php` and `wp-json/` exposed (D-07) | French home | link and RSD references present |
| office data, phone numbers, addresses | `/contact/`, `/about-us/` | transcribed verbatim, then re-cast to placeholder identity |
| counters of 20, 10, 400 and 20, since 2012 | `/about-us/` | transcribed |
| the service list of 9 entries | `/our-services/` | transcribed |
| client logo names (16) | English home | transcribed from the `They trust us` section, then re-cast |
| the award-recognised project list (7) | `/about-us/` | transcribed, then re-cast |
| headings quoted in the surface inventory and the home composition | the respective pages | `h1` to `h4` extraction in document order |
| the `Verdane` case-study structure and service tags | `/project/verdane/` | page content transcription |
| the French `<title>` including `GEO` | French home | `<title>` extraction |
| French blog articles on GEO and E-E-A-T | French home | `href` extraction under `/actualites-web/` and the root |

**What was deliberately not done:**

- no JavaScript execution and no browser automation: everything above is from served bytes, which keeps the evidence
  base falsifiable, since any reader can re-fetch the same paths and check, at the cost of the runtime evidence gaps;
- no authenticated or private surfaces were probed, and no form was submitted, so the submission contract, the first
  evidence gap, remains open for that reason;
- no load or security probing was performed against the live properties: the measured defects are observations of
  publicly served markup, not the results of probing.

**Reproduction.** Every extraction claim is reproducible with a fetch of the listed artefact plus the stated
extraction. Where this specification states a value in `monospace` it came from that extraction; where it states a
value that was not measured, namely the type scale, the semantic colours and the load model, it says so at the point
of use, and those points are the boundary between what was measured and what was designed.

## Constraints

- Tenancy is the client organisation: no row of a client organisation is ever readable by another client
  organisation, a client principal reads only its own organisation's records, and a contractor reads only
  what an unexpired grant names.
- Signup is closed; principals arrive through seeding, an invitation or the directory.
- No self-serve checkout, no marketplace, no hosting of client websites, no design tool, no payroll or HR
  records, and no partner white-label portal or client-facing public API in this build.
- No native application.
- No backing service beyond PostgreSQL, Keycloak and Mailpit, and no call to any other host.
- Money is integer minor units in `EUR`, instants carry their zone, and identifiers handed out are opaque.
- Issued invoices, the vault access log and the audit log only ever grow.
- The portal stays responsive with four hundred client organisations, twenty thousand leads and a year of
  invoices, tickets and time entries.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is
  the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
  Parallax has twelve seeded agency principals, one seeded contractor and eight seeded client principals,
  twenty one in all, and they all share one password; list every address, whether it signs in to the back office or the portal,
  and that password there.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary
  background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the
  container.
- The backing services named in this brief are already running and reachable at their environment variables.
  Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**No mocks.** Keycloak holds every principal's credentials and Mailpit receives every message: a user list
in the app's own memory or tables that accepts a password Keycloak does not hold, a sign-in that skips
Keycloak, or an email written to a log, a file or a table instead of sent over SMTP does not count. The
named provider is the fact: the app's UI and its own tables can only reflect what lives in the provider,
never substitute for it.

## Definition of done

Parallax is done when it is deployed and healthy, a client approver can approve the current version of a
shared deliverable so that its milestone releases exactly one draft invoice, and finance can issue that
draft under the next gapless number of the right entity with the right tax treatment. Nobody approves a
version they uploaded, and nobody reads a client secret without an approved, logged, single use request.
