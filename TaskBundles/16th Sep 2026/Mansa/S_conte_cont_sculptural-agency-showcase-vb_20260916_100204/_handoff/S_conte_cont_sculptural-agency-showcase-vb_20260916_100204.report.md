# Build report -- S_conte_cont_sculptural-agency-showcase-vb_20260916_100204

Rendered from `_handoff/S_conte_cont_sculptural-agency-showcase-vb_20260916_100204.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| | |
|---|---|
| task code | `S_conte_cont_sculptural-agency-showcase-vb_20260916_100204` |
| task id | `deku/sculptural-agency-showcase-vb` |
| cell | solo_founder / content-publishing / content-publishing |
| Task Order domain | `portfolio-agency`, outside the kit enum; mapped to `content-publishing` (G0), recorded in `_spec/.../00-decisions.md` |
| archetype | `sculptural-agency-showcase` |
| service profile | `P4-db-storage` |
| providers | `backend = postgres`, `storage = minio` |
| variant | `b`, axes `["critical_depth", "spec_sections"]` |
| language | `python` (draw: mpa-progressive, Django templates with HTMX) |
| design direction | `companion` (the draw was `editorial-serif` and does not govern) |
| launch surface | `meta_tags,sitemap_robots,social_preview,spam_protection,terms_page` |
| spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| authors | kaustubh.dalvi@ethara.ai, mansa.gupta@ethara.ai |
| shard | 1 of 1 (single-operator run) |
| kit revision | git HEAD `806eb0a`, 2026-09-16 |
| vendored grader | `0.22.0` |
| target schema | `1.4` |
| verifier mode | `separate` |
| rubric | `tests/rubric.json` generated from `grounding.yaml`; READ at runtime as of grader 0.21.0 |
| companion | `9.16_prds/prd6/bear_prd.md`, 4,575 lines |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Scroll-driven home page around the faceted mascot | INCLUDED | `## Core features` rules 32 to 35, `## Front-end specification` | the idea's centrepiece |
| Services page with the hive motif | INCLUDED | `## Core features` rule 43, `## Front-end specification` | the idea's services page |
| Case study index and long project pages | INCLUDED | `## Core features` rules 13 to 16 | the idea's case study index |
| Team and culture page, office switcher | INCLUDED | `## Core features` rule 41, `## Front-end specification` | the idea's team and culture page |
| Categorised article archive and article pages | INCLUDED | `## Core features` rules 17 to 21 | the idea's article archive |
| Project enquiry form with the app's own bot check | INCLUDED | `## Core features` rules 22 to 29, `## User flow` | the Task Order's end-to-end outcome |
| Editor studio with draft and published state, images in the bucket | INCLUDED | `## Core features` rules 1 to 12 | carries the pattern's critical focus and the declared backend and storage slots |
| Client account enquiry list | INCLUDED | `## Core features` rules 30 to 31, `## User flow` | the pattern's second role |
| The launch surface | INCLUDED | `## Core features` rules 44 to 49 | the reference/O draw |
| The companion's third-party captcha, analytics and chat widgets | DROPPED | `## Constraints` | external services outside the profile; declared to G51 with `--waive` |
| Grounds, header, drawer, footer and split headings | INCLUDED | `## Core features` rules 36 to 42 | companion chrome |
| Pixel, colour, duration and animation-name values | CARRIED AS DESCRIPTION | `## UI/UX notes`, `## Front-end specification` | tasker rule: intent register, no raw values |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_anonymous_enquiry_is_stored_with_state_new`, `test_seeding_is_idempotent_across_restarts` assert persisted rows |
| `storage` | `minio` | MET | `test_uploaded_image_is_stored_in_the_bucket_at_the_pinned_key` reads the bucket through the capability fixture |

## Grading layer

| | |
|---|---|
| workflows | 16 |
| browser substeps | 45 |
| pytest substeps | 104 |
| critical substeps | 14 |
| non-happy-path ids | 7: `draft_is_denied_to_other_visitors`, `other_roles_are_denied_studio_writes`, `unauthenticated_visitor_is_sent_to_sign_in`, `concurrent_publish_of_one_slug_has_one_winner`, `invalid_entry_or_upload_is_refused`, `invalid_enquiry_is_refused`, `expired_duplicate_or_repeated_enquiry_is_refused` |
| pytest module | `tests/test_output.py`, one module covering core, data integrity, authorization, edge cases and the page-driven surface |
| test functions | 104 |
| checklist items | 579 across 10 sections |

Checklist items per section: C-CF 227, C-CN 15, C-DC 47, C-DM 41, C-FE 73, C-OV 8, C-RL 35, C-TR 13, C-UF 43, C-UX 77.

## Rubric

26 judged criteria, 25 positive and 1 negative. Positive total 65.

| Dimension | Share | Target | Criteria |
|---|---|---|---|
| `instruction_following` | 0.354 | 0.3 | 7 |
| `functionality` | 0.231 | 0.25 | 5 |
| `ux_flow` | 0.123 | 0.15 | 4 |
| `ui_visual` | 0.154 | 0.15 | 6 |
| `motion` | 0.046 | 0.05 | 1 |
| `accessibility` | 0.046 | 0.05 | 1 |
| `responsiveness` | 0.046 | 0.05 | 1 |

Compiled answer key: 104 items in `solution/trinity/rubrics.json`, compiled-weight share 1.0.
Independent rubric review converged in three cycles (qc_rubric.md, RC-01 to RC-16).

## Grading window

| Section | Chars | Reference |
|---|---|---|
| `core_features` | 17057 | 2400 |
| `user_flow` | 5594 | 1900 |
| `ui_ux_notes` | 15711 | 1700 |
| `constraints` | 1221 | 800 |
| `user_roles` | 1918 | 1000 |
| `overview` | 2224 | 700 |
| joined | 43725 | 8,800 |

`window_lint.py` reports length and fails nothing. The tasker lifted the kit's size caps for this task. `## Core features` runs past the judge's 2,500-char slice; the critical-focus rules (publication state, slug contention, media privacy) are front-loaded, and the later rules are graded by pytest or by criteria that name their own surface.

## Literals ledger

358 pinned values.

| Class | Value | Carriers |
|---|---|---|
| `credential` | `deku-demo-pw-2026` | `instruction.md`, `conftest.py` |
| `account` | `editor@example.com` | `instruction.md`, `conftest.py` |
| `account` | `editor2@example.com` | `instruction.md`, `conftest.py` |
| `account` | `client@example.com` | `instruction.md`, `conftest.py`, `test_output.py` |
| `account` | `hello@example.com` | `instruction.md`, `conftest.py` |
| `account` | `hr@example.com` | `instruction.md`, `conftest.py` |
| `account` | `ada.quinn@example.com` | `instruction.md`, `conftest.py` |
| `env_var` | `DATABASE_URL` | `instruction.md` |
| `env_var` | `STORAGE_ENDPOINT` | `instruction.md`, `test_output.py` |
| `env_var` | `STORAGE_BUCKET` | `instruction.md`, `test_output.py` |
| `env_var` | `STORAGE_ACCESS_KEY` | `instruction.md` |
| `env_var` | `STORAGE_SECRET_KEY` | `instruction.md` |
| `env_var` | `APP_PUBLIC_URL` | `instruction.md` |
| `env_var` | `APP_PUBLIC_PORT` | `instruction.md` |
| `route` | `/services` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/works` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/works/{slug}` | `instruction.md`, `test_output.py` |
| `route` | `/about-us` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/blog` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/blog/{slug}` | `instruction.md` |
| `route` | `/blog-categories/{slug}` | `instruction.md`, `test_output.py` |
| `route` | `/contact` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/privacy-policy` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/terms` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/sign-in` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/sign-up` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/account/enquiries` | `instruction.md`, `conftest.py` |
| `route` | `/studio` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/studio/new/details` | `instruction.md`, `conftest.py` |
| `route` | `/studio/new/media` | `instruction.md`, `conftest.py` |
| `route` | `/studio/new/review` | `instruction.md`, `conftest.py` |
| `route` | `/studio/entries/{kind}/{id}` | `instruction.md` |
| `route` | `/studio/enquiries` | `instruction.md`, `conftest.py` |
| `route` | `/sitemap.xml` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/robots.txt` | `instruction.md`, `test_output.py` |
| `route` | `/social-preview/{page_key}` | `instruction.md` |
| `route` | `/app/USER_README.md` | `instruction.md`, `test_output.py` |
| `route` | `?page=2` | `instruction.md` |
| `endpoint` | `/api/auth/sign-up` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `/api/auth/login` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `/api/services` | `instruction.md`, `test_output.py` |
| `endpoint` | `/api/case-studies` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `/api/case-studies/{slug}` | `instruction.md` |
| `endpoint` | `/api/case-studies/{id}` | `instruction.md` |
| `endpoint` | `/api/case-studies/{id}/publish` | `instruction.md` |
| `endpoint` | `/api/case-studies/{id}/unpublish` | `instruction.md` |
| `endpoint` | `/api/case-studies/{id}/media` | `instruction.md` |
| `endpoint` | `/api/articles` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `/api/articles/{slug}` | `instruction.md` |
| `endpoint` | `/api/articles/{id}` | `instruction.md` |
| `endpoint` | `/api/articles/{id}/publish` | `instruction.md` |
| `endpoint` | `/api/articles/{id}/unpublish` | `instruction.md` |
| `endpoint` | `/api/articles/{id}/media` | `instruction.md` |
| `endpoint` | `/api/article-categories` | `instruction.md` |
| `endpoint` | `/api/media/{asset_id}/content` | `instruction.md` |
| `endpoint` | `/api/bot-check` | `instruction.md`, `conftest.py` |
| `endpoint` | `/api/enquiries` | `instruction.md`, `test_output.py` |
| `endpoint` | `/api/enquiries/{id}` | `instruction.md` |
| `endpoint` | `/api/health` | `instruction.md`, `test_output.py` |
| `endpoint` | `access_token` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `display_name` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `entry_count` | `instruction.md`, `test_output.py` |
| `endpoint` | `published_at` | `instruction.md`, `test_output.py` |
| `endpoint` | `alt_text` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `object_key` | `instruction.md`, `test_output.py` |
| `endpoint` | `content_type` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `byte_size` | `instruction.md`, `test_output.py` |
| `endpoint` | `website_url` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `read_minutes` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `bpGCap` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | ``Website`` | `instruction.md` |
| `endpoint` | ``Service`` | `instruction.md` |
| `endpoint` | ``Budget`` | `instruction.md` |
| `endpoint` | ``Message`` | `instruction.md` |
| `status` | ``draft`` | `instruction.md` |
| `status` | ``published`` | `instruction.md` |
| `status` | ``new`` | `instruction.md` |
| `status` | ``in_conversation`` | `instruction.md` |
| `status` | ``closed`` | `instruction.md` |
| `status` | ``editor`` | `instruction.md` |
| `status` | ``client`` | `instruction.md` |
| `status` | ``case-study`` | `instruction.md` |
| `status` | ``article`` | `instruction.md` |
| `status` | ``dark`` | `instruction.md` |
| `status` | ``light`` | `instruction.md` |
| `status` | ``tinted`` | `instruction.md` |
| `status` | ``right`` | `instruction.md` |
| `status` | ``left`` | `instruction.md` |
| `number` | `5 MB` | `instruction.md` |
| `number` | `ten minutes` | `instruction.md` |
| `number` | `sixty seconds` | `instruction.md` |
| `number` | `four to a page` | `instruction.md` |
| `number` | `image/png` | `instruction.md`, `conftest.py`, `test_output.py` |
| `number` | `image/jpeg` | `instruction.md` |
| `number` | `image/webp` | `instruction.md` |
| `number` | `404` | `instruction.md`, `conftest.py`, `test_output.py` |
| `scheme` | `media/{kind}/{entry_id}/{sha256_of_bytes}.{ext}` | `instruction.md` |
| `scheme` | `data-ground` | `instruction.md`, `test_output.py` |
| `scheme` | `data-scene` | `instruction.md`, `test_output.py` |
| `scheme` | `data-object` | `instruction.md`, `test_output.py` |
| `scheme` | `data-case-study-row` | `instruction.md`, `conftest.py`, `test_output.py` |
| `scheme` | `data-slug` | `instruction.md`, `conftest.py`, `test_output.py` |
| `scheme` | `data-image-side` | `instruction.md`, `test_output.py` |
| `scheme` | `data-article-row` | `instruction.md`, `conftest.py`, `test_output.py` |
| `scheme` | `data-pagination="next"` | `instruction.md` |
| `scheme` | `data-count` | `instruction.md`, `test_output.py` |
| `scheme` | `aria-current="page"` | `instruction.md` |
| `scheme` | `data-reading-progress` | `instruction.md`, `test_output.py` |
| `scheme` | `data-enquiry-form` | `instruction.md`, `test_output.py` |
| `scheme` | `data-form-result="success"` | `instruction.md` |
| `scheme` | `data-form-result="failure"` | `instruction.md` |
| `scheme` | `data-bot-check` | `instruction.md`, `test_output.py` |
| `scheme` | `data-enquiry-state` | `instruction.md` |
| `scheme` | `data-drawer` | `instruction.md`, `test_output.py` |
| `scheme` | `data-drawer-trigger` | `instruction.md`, `test_output.py` |
| `scheme` | `aria-expanded` | `instruction.md`, `test_output.py` |
| `scheme` | `data-office-switch` | `instruction.md`, `test_output.py` |
| `scheme` | `aria-pressed` | `instruction.md`, `test_output.py` |
| `scheme` | `data-office-image` | `instruction.md`, `test_output.py` |
| `scheme` | `data-active="true"` | `instruction.md` |
| `scheme` | `data-split-heading` | `instruction.md`, `test_output.py` |
| `scheme` | `aria-label` | `instruction.md`, `test_output.py` |
| `scheme` | `data-motif="hive"` | `instruction.md` |
| `scheme` | `data-motif-part="hive"` | `instruction.md` |
| `scheme` | `data-motif-part="orbit"` | `instruction.md` |
| `scheme` | `data-phase="reverse"` | `instruction.md` |
| `scheme` | `data-entry-state` | `instruction.md` |
| `scheme` | `data-wizard-step` | `instruction.md` |
| `scheme` | `og:title` | `instruction.md`, `test_output.py` |
| `scheme` | `og:image` | `instruction.md`, `test_output.py` |
| `scheme` | `Sitemap:` | `instruction.md`, `test_output.py` |
| `scheme` | `data-scene="mascot-hero"` | `instruction.md` |
| `scheme` | `data-scene="culture-object"` | `instruction.md` |
| `scheme` | `data-scene="works-field"` | `instruction.md` |
| `scheme` | `data-scene="works-preview"` | `instruction.md` |
| `seed_record` | `Nadia Brooks` | `instruction.md`, `conftest.py` |
| `seed_record` | `Owen Pike` | `instruction.md`, `conftest.py` |
| `seed_record` | `Leo Marsh` | `instruction.md`, `conftest.py` |
| `seed_record` | `Lumen Pay` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `lumen-pay` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Haven Health` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `haven-health` | `instruction.md`, `conftest.py` |
| `seed_record` | `Kitefolio` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Orchard Market` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `orchard-market` | `instruction.md`, `conftest.py` |
| `seed_record` | `Tidewater` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Northstar Learning` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `northstar-learning` | `instruction.md`, `conftest.py` |
| `seed_record` | `Quill and Ink` | `instruction.md`, `conftest.py` |
| `seed_record` | `quill-and-ink` | `instruction.md`, `conftest.py` |
| `seed_record` | `Parcelio` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Verde Energy` | `instruction.md`, `conftest.py` |
| `seed_record` | `verde-energy` | `instruction.md`, `conftest.py` |
| `seed_record` | `Atlas Freight` | `instruction.md`, `conftest.py` |
| `seed_record` | `atlas-freight` | `instruction.md`, `conftest.py` |
| `seed_record` | `A payments app that settles an invoice in one tap` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `A patient portal that makes a clinic visit feel shorter` | `instruction.md`, `conftest.py` |
| `seed_record` | `A portfolio builder for designers who hate building portfolios` | `instruction.md`, `conftest.py` |
| `seed_record` | `A grocery storefront that restocks before the shelf is empty` | `instruction.md`, `conftest.py` |
| `seed_record` | `A booking flow that fits a whole trip on one screen` | `instruction.md`, `conftest.py` |
| `seed_record` | `A course platform where every lesson ends with something built` | `instruction.md`, `conftest.py` |
| `seed_record` | `An editorial system for a newsroom that never sleeps` | `instruction.md`, `conftest.py` |
| `seed_record` | `A courier dashboard that shows every parcel at once` | `instruction.md`, `conftest.py` |
| `seed_record` | `A home energy app that turns a bill into a plan` | `instruction.md`, `conftest.py` |
| `seed_record` | `A freight marketplace that quotes in seconds` | `instruction.md`, `conftest.py` |
| `seed_record` | ``Fintech`` | `instruction.md` |
| `seed_record` | ``Healthcare`` | `instruction.md` |
| `seed_record` | ``SaaS`` | `instruction.md` |
| `seed_record` | ``E-commerce`` | `instruction.md` |
| `seed_record` | ``Travel`` | `instruction.md` |
| `seed_record` | ``Education`` | `instruction.md` |
| `seed_record` | ``Publishing`` | `instruction.md` |
| `seed_record` | ``Logistics`` | `instruction.md` |
| `seed_record` | ``Energy`` | `instruction.md` |
| `seed_record` | ``Supply chain`` | `instruction.md` |
| `seed_record` | `Nightjar` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | ``nightjar`` | `instruction.md` |
| `seed_record` | `Hiring a design partner in 2027` | `instruction.md`, `conftest.py` |
| `seed_record` | `hiring-a-design-partner` | `instruction.md`, `conftest.py` |
| `seed_record` | `Product design` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `product-design` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Engineering` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Studio life` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `studio-life` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Shipping an MVP in eight weeks` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `shipping-an-mvp-in-eight-weeks` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Field notes from a design thinking workshop` | `instruction.md`, `conftest.py` |
| `seed_record` | `design-thinking-workshop-field-notes` | `instruction.md`, `conftest.py` |
| `seed_record` | `Five questions to ask before you hire a studio` | `instruction.md`, `conftest.py` |
| `seed_record` | `five-questions-before-you-hire-a-studio` | `instruction.md`, `conftest.py` |
| `seed_record` | `When to bring in a fractional CTO` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `when-to-bring-in-a-fractional-cto` | `instruction.md`, `conftest.py` |
| `seed_record` | `Designing onboarding that converts` | `instruction.md`, `conftest.py` |
| `seed_record` | `designing-onboarding-that-converts` | `instruction.md`, `conftest.py` |
| `seed_record` | `A week inside the studio` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `a-week-inside-the-studio` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `7 min read` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `5 min read` | `instruction.md`, `conftest.py` |
| `seed_record` | `6 min read` | `instruction.md`, `conftest.py` |
| `seed_record` | `8 min read` | `instruction.md`, `conftest.py` |
| `seed_record` | `4 min read` | `instruction.md`, `conftest.py` |
| `seed_record` | `3 min read` | `instruction.md`, `conftest.py` |
| `seed_record` | `Sep 2, 2026` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Aug 26, 2026` | `instruction.md`, `conftest.py` |
| `seed_record` | `Aug 19, 2026` | `instruction.md`, `conftest.py` |
| `seed_record` | `Aug 5, 2026` | `instruction.md`, `conftest.py` |
| `seed_record` | `Jul 22, 2026` | `instruction.md`, `conftest.py` |
| `seed_record` | `Jul 8, 2026` | `instruction.md`, `conftest.py` |
| `seed_record` | `Design thinking workshop` | `instruction.md`, `conftest.py` |
| `seed_record` | `UX/UI design` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Fractional CTO` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Website development` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Dedicated team` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Software development` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Branding design` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Website design` | `instruction.md`, `conftest.py` |
| `seed_record` | `Under $10k` | `instruction.md`, `conftest.py` |
| `seed_record` | `$10k - $30k` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `$30k - $60k` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `$60k - $100k` | `instruction.md`, `conftest.py` |
| `seed_record` | `Over $100k` | `instruction.md`, `conftest.py` |
| `seed_record` | ``rocket`` | `instruction.md` |
| `seed_record` | ``wand`` | `instruction.md` |
| `seed_record` | ``arrow`` | `instruction.md` |
| `seed_record` | ``bomb`` | `instruction.md` |
| `seed_record` | ``thumb`` | `instruction.md` |
| `seed_record` | ``bond`` | `instruction.md` |
| `seed_record` | ``flame`` | `instruction.md` |
| `seed_record` | `Lift-off ready` | `instruction.md`, `conftest.py` |
| `seed_record` | `Technomagicians` | `instruction.md`, `conftest.py` |
| `seed_record` | `Aim for the point` | `instruction.md`, `conftest.py` |
| `seed_record` | `Go wow or go home` | `instruction.md`, `conftest.py` |
| `seed_record` | `Win-Win partnership` | `instruction.md`, `conftest.py` |
| `seed_record` | `Bonding together` | `instruction.md`, `conftest.py` |
| `seed_record` | `Keep the fire` | `instruction.md`, `conftest.py` |
| `seed_record` | `Empathize` | `instruction.md`, `conftest.py` |
| `seed_record` | `Define` | `instruction.md`, `conftest.py` |
| `seed_record` | `Ideate` | `instruction.md`, `conftest.py` |
| `seed_record` | `Prototype` | `instruction.md`, `conftest.py` |
| `seed_record` | `Repeat` | `instruction.md`, `conftest.py` |
| `seed_record` | `Mara Lindqvist` | `instruction.md`, `conftest.py` |
| `seed_record` | `Tomas Reyes` | `instruction.md`, `conftest.py` |
| `seed_record` | `Priya Anand` | `instruction.md`, `conftest.py` |
| `seed_record` | `The items were delivered on time and in great quality.` | `instruction.md`, `conftest.py` |
| `seed_record` | `They were a professional, experienced team with outstanding ideas.` | `instruction.md`, `conftest.py` |
| `seed_record` | `The team was always accommodating and supportive.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Pixel Guild Site of the Day` | `instruction.md`, `conftest.py` |
| `seed_record` | `Studio Honors Gold` | `instruction.md`, `conftest.py` |
| `seed_record` | `Product Craft Award` | `instruction.md`, `conftest.py` |
| `seed_record` | `Design Circle Pick` | `instruction.md`, `conftest.py` |
| `seed_record` | `Web Makers Top Studio` | `instruction.md`, `conftest.py` |
| `seed_record` | `Hana Ito` | `instruction.md`, `conftest.py` |
| `seed_record` | `Marco Silva` | `instruction.md`, `conftest.py` |
| `seed_record` | `Ruth Okafor` | `instruction.md`, `conftest.py` |
| `seed_record` | `Dev Patel` | `instruction.md`, `conftest.py` |
| `seed_record` | `Ingrid Moe` | `instruction.md`, `conftest.py` |
| `seed_record` | `Sam Carter` | `instruction.md`, `conftest.py` |
| `seed_record` | `First Office` | `instruction.md`, `conftest.py` |
| `seed_record` | `Second Office` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `85 Example St, District 4,` | `instruction.md`, `conftest.py` |
| `seed_record` | `60 Example Pl, Example NSW 2000` | `instruction.md`, `conftest.py` |
| `seed_record` | `Ada Quinn` | `instruction.md`, `test_output.py` |
| `seed_record` | `Ironwood` | `instruction.md`, `test_output.py` |
| `seed_record` | `Iron Wood` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Services.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Works.` | `instruction.md`, `conftest.py` |
| `seed_record` | `About.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Blog.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Home.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Hire us.` | `instruction.md`, `conftest.py` |
| `seed_record` | ``facebook`` | `instruction.md` |
| `seed_record` | ``behance`` | `instruction.md` |
| `seed_record` | ``instagram`` | `instruction.md` |
| `seed_record` | ``dribbble`` | `instruction.md` |
| `seed_record` | ``clutch`` | `instruction.md` |
| `seed_record` | ``linkedin`` | `instruction.md` |
| `seed_record` | ``awwwards`` | `instruction.md` |
| `seed_record` | `Have a product in mind?` | `instruction.md`, `conftest.py` |
| `seed_record` | `Let's build it` | `instruction.md`, `conftest.py` |
| `seed_record` | `© 2026 Iron Wood - UX UI Design Agency` | `instruction.md`, `conftest.py` |
| `seed_record` | `Privacy Policy` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Terms of Service` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `By creating an account you agree to the Terms of Service.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Sorry! The page you're looking for was not found` | `instruction.md`, `conftest.py` |
| `seed_record` | `Back to home` | `instruction.md`, `conftest.py` |
| `seed_record` | `Thank you. Your enquiry is with us.` | `instruction.md`, `conftest.py` |
| `seed_record` | `We read every message and reply within two working days.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Something went wrong and your enquiry was not sent. Everything you typed is still here.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Be our client. Get that buzz` | `instruction.md`, `conftest.py` |
| `seed_record` | `Send enquiry` | `instruction.md`, `test_output.py` |
| `seed_record` | `Follow us` | `instruction.md`, `test_output.py` |
| `seed_record` | `Visit site` | `instruction.md`, `test_output.py` |
| `seed_record` | `Industry` | `instruction.md`, `test_output.py` |
| `seed_record` | `Next project` | `instruction.md`, `test_output.py` |
| `seed_record` | `Contents` | `instruction.md`, `test_output.py` |
| `seed_record` | `Related articles` | `instruction.md`, `test_output.py` |
| `seed_record` | `Agency Services` | `instruction.md`, `test_output.py` |
| `seed_record` | `How we work with you` | `instruction.md`, `test_output.py` |
| `seed_record` | `A team that ships alongside yours` | `instruction.md`, `test_output.py` |
| `seed_record` | `Senior by default` | `instruction.md`, `test_output.py` |
| `seed_record` | `One channel, one owner` | `instruction.md`, `test_output.py` |
| `seed_record` | `Built to hand over` | `instruction.md`, `test_output.py` |
| `seed_record` | `Discover` | `instruction.md`, `test_output.py` |
| `seed_record` | `Deliver` | `instruction.md`, `test_output.py` |
| `seed_record` | `We build` | `instruction.md`, `conftest.py` |
| `seed_record` | `award-winning products` | `instruction.md`, `conftest.py` |
| `seed_record` | `that everyone loves.` | `instruction.md`, `conftest.py` |
| `seed_record` | `About Iron Wood` | `instruction.md`, `test_output.py` |
| `seed_record` | `Our journey` | `instruction.md`, `test_output.py` |
| `seed_record` | `Trusted by product teams at` | `instruction.md`, `test_output.py` |
| `seed_record` | `The people behind the work` | `instruction.md`, `test_output.py` |
| `seed_record` | `Two offices, one studio` | `instruction.md`, `test_output.py` |
| `seed_record` | `Insights from the studio` | `instruction.md` |
| `seed_record` | `Award-winning digital agency specializing in design and development` | `instruction.md`, `test_output.py` |
| `seed_record` | `See our services` | `instruction.md`, `test_output.py` |
| `seed_record` | `See our work` | `instruction.md`, `test_output.py` |
| `seed_record` | `Our culture, mantra, and beliefs` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `We've been doing brilliant work with brilliant brands` | `instruction.md`, `conftest.py` |
| `seed_record` | `We team up with great minds who think alike, regardless of business size.` | `instruction.md`, `test_output.py` |
| `seed_record` | `What our clients talk about us` | `instruction.md`, `conftest.py` |
| `seed_record` | `We rapidly transform ideas into problem-solving products, designed to adapt swiftly to the evolving market demands.` | `instruction.md`, `test_output.py` |
| `seed_record` | `We build business-savvy products from the hive of creativity blended with the latest technology trends.` | `instruction.md` |
| `seed_record` | ``More`` | `instruction.md` |
| `seed_record` | ``All`` | `instruction.md` |
| `seed_record` | `Entries` | `instruction.md` |
| `seed_record` | `New entry` | `instruction.md` |
| `seed_record` | `Enquiries` | `instruction.md` |
| `seed_record` | `Sign out` | `instruction.md` |
| `seed_record` | `+1 555 0100` | `instruction.md`, `test_output.py` |
| `seed_record` | `+61 2 5550 0100` | `instruction.md` |
| `seed_record` | `We want a faster marketing site with a case study library.` | `instruction.md`, `test_output.py` |
| `seed_record` | `Nightjar concept board` | `instruction.md`, `test_output.py` |
| `seed_record` | `https://lumen-pay.example.com` | `instruction.md`, `test_output.py` |
| `seed_record` | `Fintech product, designed and built by Iron Wood` | `instruction.md`, `test_output.py` |
| `seed_record` | `We need a redesign of our booking app before the spring launch.` | `instruction.md` |
| `seed_record` | ``works-{slug}`` | `instruction.md` |
| `seed_record` | ``sign-up`` | `instruction.md` |
| `motion_moment` | `one word at a time` | `instruction.md` |
| `motion_moment` | `sweeps out of its window` | `instruction.md` |
| `motion_moment` | `empties` | `instruction.md` |
| `motion_moment` | `trails behind the pointer` | `instruction.md` |
| `motion_moment` | `pushed outward` | `instruction.md` |
| `motion_moment` | `lifting a sheet` | `instruction.md` |
| `motion_moment` | `leaves upward` | `instruction.md` |
| `motion_moment` | `bobs` | `instruction.md` |
| `motion_moment` | `opposite phase` | `instruction.md` |
| `motion_moment` | `fills horizontally` | `instruction.md` |
| `design_phrase` | `watermark` | `instruction.md` |
| `design_phrase` | `drained` | `instruction.md` |
| `design_phrase` | `faceted` | `instruction.md` |
| `design_phrase` | `hard two-tone split` | `instruction.md` |
| `design_phrase` | `near-white neutral` | `instruction.md` |
| `design_phrase` | `near-black neutral` | `instruction.md` |
| `design_phrase` | `Space over dividers` | `instruction.md` |
| `design_phrase` | `three recurring vertical lines` | `instruction.md` |
| `design_phrase` | `pale soft red` | `instruction.md` |
| `design_phrase` | `neo-grotesque sans` | `instruction.md` |
| `env_var` | `DB_ADMIN_URL` (verifier-only) | `task.toml` |

## spec/ documents

Authored at `_spec/S_conte_cont_sculptural-agency-showcase-vb_20260916_100204/`, outside the bundle (CON-5).

| Document | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the draws, the companion carry table and the G51 waiver rationale |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not baseline and this variant does not request it |

## Kit gate log

Rendered from the receipts, one row per gate.

| Gate | Tool | Exit | Verdict | Findings |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 0 |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 0 |
| `G46` | `structure_lint.py` | 0 | PASS | 0 |
| `G50` | `docker_lint.py` | 0 | PASS | 0 |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 0 |
| `G63` | `secret_lint.py` | 0 | PASS | 0 |
| `G48` | `truth_lint.py` | 0 | PASS | 0 |
| `G51` | `source_lint.py` | 0 | PASS | 0 |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 0 |
| `G54` | `comment_lint.py` | 0 | PASS | 0 |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 0 |
| `G11` | `leak_scan.py` | 0 | PASS | 0 |
| `G33` | `window_lint.py` | 0 | PASS | 0 |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 0 |
| `G43` | `prescription_lint.py` | 0 | PASS | 0 |
| `G44` | `disclosure_lint.py` | 0 | PASS | 0 |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 0 |
| `G31` | `determinism_lint.py` | 0 | PASS | 0 |
| `G14` | `reward_path_lint.py` | 0 | PASS | 0 |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 0 |
| `G41` | `flag_lint.py` | 0 | PASS | 0 |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 0 |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 0 |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 0 |
| `G6` | `fixture_lint.py` | 0 | PASS | 0 |
| `G24` | `coverage_map.py` | 0 | PASS | 0 |
| `G37` | `checklist_qc.py` | 0 | PASS | 0 |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 0 |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 0 |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 0 |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 0 |
| `G47` | `output_qc.py` | 0 | PASS | 0 |

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks answered | Attestation |
|---|---|---|---|---|
| `qc_docker.md` | `G35` | PASS | 105 | independent-subagent |
| `QC_instruction.md` | `G34` | PASS | 24 | independent-subagent |
| `qc_rubric.md` | `G53` | PASS | 16 | independent-subagent |
| `qc_solution_checklist.md` | `G37` | PASS | 0 | independent-subagent |
| `QC_spec.md` | `G34` | PASS | 15 | independent-subagent |
| `qc_toml.md` | `G36` | PASS | 120 | independent-subagent |
| `task_code_verifier.md` | `G3` | VALID | 12 | independent-subagent |

The spec, instruction and rubric certifications were run by independent review subagents (three cycles each, every FAIL fixed and re-verified). The toml, docker, solution-checklist and task-code certifications were also answered by independent subagents. The generator prompts carry no certification and are advisory.

Open WARNs from QC_instruction.md: A1 and B3 (no `## Build plan`, not baseline for this variant), C3 (five endpoints named only in the API shapes table), C5 (slug uniqueness stated as an outcome only, the variant-b raise), C7 (sections past their size targets, lifted by the tasker). None needs a fix.

## Budget estimate

`turns_expected = 200`, `tokens_expected = 8000000`. Thirteen public routes, a live 3D mascot with two further scenes, scroll-bound motion throughout, a three-step editor wizard, a content pipeline with private media, and an enquiry flow with its own bot check put this at the top rung of the documented band. `difficulty` stays the mandated calibration placeholder.

## Blocking findings

None for the mechanical battery. Two things are unresolved and are the operator's:

- `[delivery]` is present but carries no `@sha256:` image digests for `python:3.12-slim-bookworm`, `postgres:16.4-bookworm` and `minio/minio:RELEASE.2024-10-13T13-34-11Z`; these cannot be resolved without a registry.
- No reference application exists. The bundle carries a brief, a checklist, an answer key and a grading layer, and `solution/solve.sh` exits non-zero saying so.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. Not admissible.
