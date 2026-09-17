from __future__ import annotations

import httpx

import appclient
import conftest as fixtures


def test_signup_creates_an_account_and_returns_a_token(fresh_account):
    response = fresh_account.get("/console/projects")
    assert response.status_code in (200, 403), (
        f"a freshly signed-up account reached GET /api/console/projects with "
        f"{response.status_code}, expected either the list or a refusal rather "
        f"than an unauthenticated denial: {fixtures.body_excerpt(response)}"
    )


def test_signup_refuses_a_duplicate_address(anon):
    response = anon.post("/auth/signup",
                         json={"email": fixtures.EDITOR_EMAIL,
                               "password": fixtures.PASSWORD})
    assert response.status_code in fixtures.REFUSED, (
        f"POST /api/auth/signup reusing {fixtures.EDITOR_EMAIL} returned "
        f"{response.status_code}, expected a client error: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_login_with_a_wrong_password_is_denied(anon):
    response = anon.post("/auth/login",
                         json={"email": fixtures.EDITOR_EMAIL,
                               "password": "not-the-corpus-password"})
    assert response.status_code in (400, 401, 403, 422), (
        f"POST /api/auth/login with a wrong password returned "
        f"{response.status_code}, expected a refusal: "
        f"{fixtures.body_excerpt(response)}"
    )
    assert "access_token" not in (response.text or ""), (
        f"a denied login still returned a token: {fixtures.body_excerpt(response)}"
    )


def test_console_endpoint_without_a_token_is_denied(anon):
    response = anon.get("/console/projects")
    assert response.status_code in fixtures.DENIED, (
        f"GET /api/console/projects with no bearer token returned "
        f"{response.status_code}, expected a denial: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_french_catalogue_is_served_without_a_prefix():
    response = fixtures.page("/projets/")
    assert response.status_code == 200, (
        f"GET /projets/ returned {response.status_code}; French is the default "
        f"locale and is served with no prefix"
    )


def test_english_catalogue_is_served_under_the_prefix():
    response = fixtures.page("/en/projects/")
    assert response.status_code == 200, (
        f"GET /en/projects/ returned {response.status_code}; English is served "
        f"under its own prefix at its own slug"
    )


def test_path_without_a_trailing_slash_redirects_to_the_canonical_form():
    response = fixtures.page("/projets", follow=False)
    assert response.status_code in fixtures.REDIRECTED, (
        f"GET /projets returned {response.status_code}, expected a permanent "
        f"redirect to /projets/ rather than a second address rendering one page"
    )
    target = response.headers.get("location", "")
    assert target.rstrip("/").endswith("/projets"), (
        f"the redirect from /projets points at {target!r} rather than the "
        f"canonical trailing-slash form"
    )


def test_uppercase_path_redirects_to_the_canonical_form():
    response = fixtures.page("/Projets/", follow=False)
    assert response.status_code in fixtures.REDIRECTED, (
        f"GET /Projets/ returned {response.status_code}, expected a permanent "
        f"redirect to the lowercase canonical form"
    )


def test_language_header_never_redirects():
    response = fixtures.page("/", headers={"Accept-Language": "en-GB,en;q=0.9"},
                             follow=False)
    assert response.status_code == 200, (
        f"GET / with an English language header returned {response.status_code}; "
        f"the site never redirects on the browser's language header, because a "
        f"shared link must resolve the same way for everybody"
    )


def test_project_published_in_french_only_is_absent_from_the_english_catalogue(anon):
    english = fixtures.slugs_of(fixtures.catalogue(anon, fixtures.EN))
    assert fixtures.QUAI_DOUZE not in english, (
        f"{fixtures.QUAI_DOUZE} is published in French alone yet appears in the "
        f"English catalogue: {english!r}"
    )
    french = fixtures.slugs_of(fixtures.catalogue(anon, fixtures.FR))
    assert fixtures.QUAI_DOUZE in french, (
        f"{fixtures.QUAI_DOUZE} is missing from the French catalogue: {french!r}"
    )


def test_language_switch_explains_a_missing_translation():
    response = fixtures.page(f"/projets/{fixtures.QUAI_DOUZE}/")
    assert response.status_code == 200, (
        f"GET /projets/{fixtures.QUAI_DOUZE}/ returned {response.status_code}"
    )
    assert fixtures.SWITCH_UNAVAILABLE_FR in response.text, (
        f"the case study with no English translation renders no explanation; "
        f"the pinned line is {fixtures.SWITCH_UNAVAILABLE_FR!r}"
    )


def test_catalogue_carries_total_facets_and_results(anon):
    payload = fixtures.catalogue(anon, fixtures.FR)
    assert "total" in payload, f"the catalogue payload carries no total: {payload!r}"
    counts = fixtures.facet_counts(payload)
    assert set(counts) == set(fixtures.DISCIPLINES), (
        f"the facets are {sorted(counts)!r}, expected exactly the four "
        f"disciplines {sorted(fixtures.DISCIPLINES)!r}"
    )
    assert fixtures.results_of(payload), (
        f"the unfiltered French catalogue returned no result: {payload!r}"
    )


def test_seeded_french_total_matches_the_published_rows(anon):
    payload = fixtures.catalogue(anon, fixtures.FR)
    assert int(payload["total"]) == fixtures.FRENCH_TOTAL, (
        f"the French catalogue total is {payload['total']!r}, expected "
        f"{fixtures.FRENCH_TOTAL} published French projects"
    )
    assert len(fixtures.results_of(payload)) == fixtures.FRENCH_TOTAL, (
        f"the total says {payload['total']!r} while the unfiltered result set "
        f"holds {len(fixtures.results_of(payload))} cards; the count above the "
        f"mosaic and the mosaic beneath are one read"
    )


def test_facet_counts_sum_above_the_total(anon):
    payload = fixtures.catalogue(anon, fixtures.FR)
    counts = fixtures.facet_counts(payload)
    total = int(payload["total"])
    assert sum(counts.values()) == fixtures.FRENCH_FACET_SUM, (
        f"the four French facet counts sum to {sum(counts.values())}, expected "
        f"{fixtures.FRENCH_FACET_SUM}: {counts!r}"
    )
    assert sum(counts.values()) > total, (
        f"the facet counts sum to {sum(counts.values())} against a total of "
        f"{total}; a project carries more than one discipline, so the sum is "
        f"above the total by construction"
    )


def test_filtering_moves_the_total_and_the_results_together(anon):
    payload = fixtures.catalogue(anon, fixtures.FR,
                                 discipline=fixtures.DIGITAL_EXPERIENCE)
    total = int(payload["total"])
    rows = fixtures.results_of(payload)
    assert total == len(rows), (
        f"a catalogue narrowed to {fixtures.DIGITAL_EXPERIENCE} reports a total "
        f"of {total} over {len(rows)} cards; the number above the mosaic cannot "
        f"disagree with the mosaic"
    )
    assert fixtures.LUNE_BASSE in [row.get("slug") for row in rows], (
        f"{fixtures.LUNE_BASSE} carries {fixtures.DIGITAL_EXPERIENCE} yet is "
        f"absent from the narrowed set: {[row.get('slug') for row in rows]!r}"
    )


def test_all_mode_is_stricter_than_any_mode(anon):
    pair = f"{fixtures.ART_DIRECTION},{fixtures.COMMERCE}"
    loose = fixtures.catalogue(anon, fixtures.FR, discipline=pair,
                               mode=fixtures.MODE_ANY)
    strict = fixtures.catalogue(anon, fixtures.FR, discipline=pair,
                                mode=fixtures.MODE_ALL)
    assert int(strict["total"]) <= int(loose["total"]), (
        f"the strict mode returned {strict['total']!r} against the permissive "
        f"mode's {loose['total']!r}; every project matching all of a set matches "
        f"any of it"
    )
    assert fixtures.SERRE_VERTE in fixtures.slugs_of(strict), (
        f"{fixtures.SERRE_VERTE} carries both {fixtures.ART_DIRECTION} and "
        f"{fixtures.COMMERCE} yet is absent under {fixtures.MODE_ALL}: "
        f"{fixtures.slugs_of(strict)!r}"
    )


def test_filter_state_round_trips_through_the_address(anon):
    first = fixtures.catalogue(anon, fixtures.FR,
                               discipline=fixtures.SHOWCASE_SITE,
                               mode=fixtures.MODE_ANY)
    second = fixtures.catalogue(anon, fixtures.FR,
                                discipline=fixtures.SHOWCASE_SITE,
                                mode=fixtures.MODE_ANY)
    assert fixtures.slugs_of(first) == fixtures.slugs_of(second), (
        f"one address produced two different result orders: "
        f"{fixtures.slugs_of(first)!r} then {fixtures.slugs_of(second)!r}"
    )
    rendered = fixtures.page(
        f"/projets/?discipline={fixtures.SHOWCASE_SITE}&mode={fixtures.MODE_ANY}")
    assert rendered.status_code == 200, (
        f"the narrowed catalogue address returned {rendered.status_code} when "
        f"requested directly; a filter state that lives only in the page loses "
        f"the shared link"
    )


def test_a_filter_combination_with_no_match_renders_the_empty_panel(anon):
    payload = fixtures.catalogue(
        anon, fixtures.FR,
        discipline=f"{fixtures.DIGITAL_EXPERIENCE},{fixtures.COMMERCE}",
        mode=fixtures.MODE_ALL)
    assert int(payload["total"]) == 0, (
        f"no seeded project carries both {fixtures.DIGITAL_EXPERIENCE} and "
        f"{fixtures.COMMERCE}, yet the total is {payload['total']!r}"
    )
    rendered = fixtures.page(
        f"/projets/?discipline={fixtures.DIGITAL_EXPERIENCE},"
        f"{fixtures.COMMERCE}&mode={fixtures.MODE_ALL}")
    assert fixtures.EMPTY_FILTER_TITLE in rendered.text, (
        f"an over-narrow filter renders no empty panel; the pinned title is "
        f"{fixtures.EMPTY_FILTER_TITLE!r}"
    )


def test_every_catalogue_card_carries_its_declared_fields(anon):
    for row in fixtures.results_of(fixtures.catalogue(anon, fixtures.FR)):
        for field in ("slug", "title", "client", "year", "tier",
                      "disciplines", "ground"):
            assert row.get(field) is not None, (
                f"a catalogue card carries no {field}: {row!r}"
            )


def test_project_detail_returns_its_blocks_in_order(anon):
    detail = fixtures.project_detail(anon, fixtures.ATELIER_BRUNE)
    rows = fixtures.blocks_of(detail)
    positions = [row.get("position") for row in rows]
    assert positions == sorted(positions), (
        f"the blocks of {fixtures.ATELIER_BRUNE} arrived out of order: "
        f"{positions!r}"
    )


def test_the_feature_project_carries_every_block_kind(anon):
    detail = fixtures.project_detail(anon, fixtures.ATELIER_BRUNE)
    kinds = {row.get("kind") for row in fixtures.blocks_of(detail)}
    assert len(kinds) >= 11, (
        f"{fixtures.ATELIER_BRUNE} carries {len(kinds)} block kinds "
        f"({sorted(kinds)!r}); the seeded feature project carries one of every "
        f"one of the eleven"
    )


def test_a_full_bleed_image_block_carries_both_crops(anon):
    detail = fixtures.project_detail(anon, fixtures.ATELIER_BRUNE)
    full = [row for row in fixtures.blocks_of(detail)
            if "full" in str(row.get("kind", "")) and "image" in str(row.get("kind", ""))]
    assert full, (
        f"{fixtures.ATELIER_BRUNE} carries no full-bleed image block: "
        f"{[row.get('kind') for row in fixtures.blocks_of(detail)]!r}"
    )
    for row in full:
        rendered = str(row)
        assert "narrow" in rendered and "wide" in rendered, (
            f"a published full-bleed image block carries one crop rather than "
            f"two: {row!r}"
        )


def test_an_autoplaying_video_block_carries_a_description(anon):
    detail = fixtures.project_detail(anon, fixtures.ATELIER_BRUNE)
    videos = [row for row in fixtures.blocks_of(detail)
              if "video" in str(row.get("kind", ""))]
    assert videos, (
        f"{fixtures.ATELIER_BRUNE} carries no video block: "
        f"{[row.get('kind') for row in fixtures.blocks_of(detail)]!r}"
    )
    backgrounds = [row for row in videos if "full" in str(row.get("kind", ""))]
    for row in backgrounds:
        assert row.get("description") or row.get("alt"), (
            f"an autoplaying background video block reached the published state "
            f"with no description: {row!r}"
        )


def test_an_unpublished_project_is_not_readable_anonymously(anon):
    response = anon.get(f"/projects/{fixtures.LUNE_BASSE}",
                        params={"locale": fixtures.FR})
    assert response.status_code in fixtures.MISSING, (
        f"{fixtures.LUNE_BASSE} sits in {fixtures.STATE_DRAFT} yet "
        f"GET /api/projects/{fixtures.LUNE_BASSE} answered "
        f"{response.status_code}: {fixtures.body_excerpt(response)}"
    )


def test_the_preflight_names_every_unmet_obligation(editor):
    ident = fixtures.console_project_id(editor, fixtures.LUNE_BASSE)
    response = editor.post(f"/console/projects/{ident}/preflight",
                           json={"locale": fixtures.FR})
    assert response.status_code in fixtures.OK, (
        f"POST /api/console/projects/{ident}/preflight returned "
        f"{response.status_code}: {fixtures.body_excerpt(response)}"
    )
    findings = fixtures.as_list(response.json())
    assert len(findings) >= 2, (
        f"the preflight on {fixtures.LUNE_BASSE} returned {len(findings)} "
        f"finding(s); the seeded draft is missing a narrow crop and an "
        f"alternative text, so a preflight that names one stopped at the first: "
        f"{findings!r}"
    )


def test_publish_is_refused_while_the_preflight_is_unclean(editor):
    ident = fixtures.console_project_id(editor, fixtures.LUNE_BASSE)
    response = editor.post(f"/console/projects/{ident}/publish",
                           json={"locale": fixtures.FR})
    assert response.status_code in fixtures.REFUSED, (
        f"publishing {fixtures.LUNE_BASSE} with two unmet obligations returned "
        f"{response.status_code}, expected a refusal: "
        f"{fixtures.body_excerpt(response)}"
    )
    after = editor.get("/console/projects")
    rows = [row for row in fixtures.as_list(after.json())
            if row.get("slug") == fixtures.LUNE_BASSE]
    assert rows and rows[0].get("state") == fixtures.STATE_DRAFT, (
        f"a refused publish left {fixtures.LUNE_BASSE} in "
        f"{rows[0].get('state') if rows else None!r} rather than "
        f"{fixtures.STATE_DRAFT}"
    )


def test_a_commercial_account_cannot_publish(commercial, editor):
    ident = fixtures.console_project_id(editor, fixtures.MAISON_CARRE)
    response = commercial.post(f"/console/projects/{ident}/publish",
                               json={"locale": fixtures.FR})
    assert response.status_code in fixtures.MISSING, (
        f"a commercial account publishing {fixtures.MAISON_CARRE} returned "
        f"{response.status_code}, expected the status an absent record carries: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_an_editor_cannot_read_the_lead_inbox(editor):
    response = editor.get("/console/leads")
    assert response.status_code in fixtures.MISSING, (
        f"an editor reading GET /api/console/leads returned "
        f"{response.status_code}, expected the status an absent record carries "
        f"so the console enumerates nothing: {fixtures.body_excerpt(response)}"
    )


def test_an_editor_cannot_read_the_activity_log(editor):
    response = editor.get("/console/activity")
    assert response.status_code in fixtures.MISSING, (
        f"an editor reading GET /api/console/activity returned "
        f"{response.status_code}, expected a refusal: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_publishing_a_new_project_moves_the_catalogue_by_one(editor, anon):
    before = int(fixtures.catalogue(anon, fixtures.FR)["total"])
    slug = fixtures.unique_slug()
    created = editor.post("/console/projects", json={
        "locale": fixtures.FR, "slug": slug, "title": "Projet Probe",
        "client": "Probe", "year": 2026, "tier": "list",
        "disciplines": [fixtures.SHOWCASE_SITE],
    })
    assert created.status_code in fixtures.OK, (
        f"POST /api/console/projects returned {created.status_code}: "
        f"{fixtures.body_excerpt(created)}"
    )
    ident = created.json().get("project_id", created.json().get("id"))
    assert ident is not None, (
        f"the created project carries no identifier: {created.json()!r}"
    )
    block = editor.post(f"/console/projects/{ident}/blocks", json={
        "kind": "text", "position": 1,
        "content": {"body": "Un projet de demonstration."},
    })
    assert block.status_code in fixtures.OK, (
        f"POST /api/console/projects/{ident}/blocks returned "
        f"{block.status_code}: {fixtures.body_excerpt(block)}"
    )
    published = editor.post(f"/console/projects/{ident}/publish",
                            json={"locale": fixtures.FR})
    assert published.status_code in fixtures.OK, (
        f"publishing a complete project returned {published.status_code}: "
        f"{fixtures.body_excerpt(published)}"
    )
    after = fixtures.catalogue(anon, fixtures.FR)
    assert int(after["total"]) == before + 1, (
        f"the catalogue total moved from {before} to {after['total']!r} after "
        f"one publish; publishing one project moves the total by exactly one"
    )
    counts = fixtures.facet_counts(after)
    assert counts[fixtures.SHOWCASE_SITE] >= 1, (
        f"the published project carries {fixtures.SHOWCASE_SITE} yet that facet "
        f"count did not rise: {counts!r}"
    )


def test_a_publish_writes_a_revision(editor):
    ident = fixtures.console_project_id(editor, fixtures.MAISON_CARRE)
    response = editor.get(f"/console/projects/{ident}")
    assert response.status_code in fixtures.OK, (
        f"GET /api/console/projects/{ident} returned {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )
    detail = response.json()
    revisions = detail.get("revisions")
    assert isinstance(revisions, list) and revisions, (
        f"the published {fixtures.MAISON_CARRE} carries no revision history: "
        f"{detail!r}"
    )


def test_renaming_a_published_slug_writes_a_redirect_automatically(editor):
    ident = fixtures.console_project_id(editor, fixtures.PORT_NEUF)
    fresh = fixtures.unique_slug()
    response = editor.patch(f"/console/projects/{ident}",
                            json={"locale": fixtures.FR, "slug": fresh})
    assert response.status_code in fixtures.OK, (
        f"renaming the French slug of {fixtures.PORT_NEUF} returned "
        f"{response.status_code}: {fixtures.body_excerpt(response)}"
    )
    sources = [row.get("source") for row in fixtures.redirect_rows(editor)]
    assert any(fixtures.PORT_NEUF in str(source) for source in sources), (
        f"renaming a published slug wrote no redirect from the old path; the "
        f"studio is not asked to remember, so a redirect nobody creates does "
        f"not exist: {sources!r}"
    )
    landing = fixtures.page(f"/projets/{fixtures.PORT_NEUF}/", follow=False)
    assert landing.status_code in fixtures.REDIRECTED, (
        f"the superseded path /projets/{fixtures.PORT_NEUF}/ returned "
        f"{landing.status_code} rather than a permanent redirect"
    )
    assert fresh in landing.headers.get("location", ""), (
        f"the superseded path redirects to "
        f"{landing.headers.get('location')!r} rather than in one hop to the "
        f"address the record occupies now"
    )


def test_renaming_the_french_slug_leaves_the_english_path_untouched():
    response = fixtures.page(f"/en/projects/{fixtures.NEW_HARBOUR}/",
                             follow=False)
    assert response.status_code == 200, (
        f"GET /en/projects/{fixtures.NEW_HARBOUR}/ returned "
        f"{response.status_code}; slug history is per locale, so a French "
        f"rename touches no English address"
    )


def test_a_redirect_target_off_the_allow_list_is_rejected(editor):
    response = editor.post("/console/redirects", json={
        "source": f"/projets/{fixtures.unique_slug()}/",
        "target": "https://not-an-allow-listed-host.example.com/landing/",
        "status": 301,
    })
    assert response.status_code in fixtures.REFUSED, (
        f"writing a redirect to an address off the allow-list returned "
        f"{response.status_code}, expected a rejection at write time: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_withdrawing_without_an_outcome_is_refused(editor):
    ident = fixtures.console_project_id(editor, fixtures.SERRE_VERTE)
    response = editor.post(f"/console/projects/{ident}/unpublish",
                           json={"locale": fixtures.FR})
    assert response.status_code in fixtures.REFUSED, (
        f"withdrawing {fixtures.SERRE_VERTE} with no choice between gone and "
        f"redirected returned {response.status_code}, expected a refusal: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_an_enquiry_creates_one_lead_and_returns_a_reference(anon, commercial):
    payload = fixtures.enquiry_payload()
    reference = fixtures.reference_of(fixtures.submitted(anon, payload))
    assert fixtures.REFERENCE_PATTERN.match(str(reference)), (
        f"the reference {reference!r} does not match the pinned shape "
        f"{fixtures.REFERENCE_PREFIX} followed by six uppercase letters or digits"
    )
    row = fixtures.poll_until(
        lambda: fixtures.lead_by_reference(commercial, reference), 30.0)
    assert row is not None, (
        f"the enquiry answered with {reference!r} yet no lead carrying it "
        f"reached the inbox"
    )
    assert row.get("state") == fixtures.LEAD_NEW, (
        f"a freshly filed lead is in state {row.get('state')!r} rather than "
        f"{fixtures.LEAD_NEW}"
    )


def test_a_repeat_submission_under_one_key_produces_one_lead(anon, commercial):
    payload = fixtures.enquiry_payload()
    key = fixtures.unique_key()
    first = fixtures.reference_of(fixtures.submitted(anon, payload, key=key))
    second = fixtures.reference_of(fixtures.submitted(anon, payload, key=key))
    assert first == second, (
        f"two submissions under one idempotency key returned {first!r} then "
        f"{second!r}; a retry after a timeout returns the first reference "
        f"rather than filing a second enquiry"
    )
    rows = [row for row in fixtures.lead_rows(commercial)
            if row.get("reference") == first]
    assert len(rows) == 1, (
        f"{len(rows)} leads carry the reference {first!r} after two submissions "
        f"under one key"
    )


def test_simultaneous_submissions_under_one_key_produce_one_lead(commercial):
    payload = fixtures.enquiry_payload()
    key = fixtures.unique_key()

    def send():
        with httpx.Client(base_url=appclient.api_base(), timeout=30.0) as client:
            return fixtures.submit_enquiry(client, payload, key=key)

    responses = fixtures.race([send] * fixtures.CONTENDERS)
    accepted = [r for r in responses if r.status_code in fixtures.OK]
    assert accepted, (
        f"every one of {fixtures.CONTENDERS} simultaneous submissions was "
        f"refused: {[r.status_code for r in responses]!r}"
    )
    references = {fixtures.reference_of(r.json()) for r in accepted}
    assert len(references) == 1, (
        f"{fixtures.CONTENDERS} simultaneous submissions under one idempotency "
        f"key produced {len(references)} references {references!r}; the "
        f"uniqueness of the key is the store's to enforce rather than a check "
        f"the application makes before writing"
    )
    reference = references.pop()
    rows = [row for row in fixtures.lead_rows(commercial)
            if row.get("reference") == reference]
    assert len(rows) == 1, (
        f"{len(rows)} leads carry {reference!r} after {fixtures.CONTENDERS} "
        f"simultaneous submissions"
    )


def test_an_enquiry_without_consent_is_refused(anon):
    payload = fixtures.enquiry_payload(consent=False)
    response = fixtures.submit_enquiry(anon, payload)
    assert response.status_code in fixtures.REFUSED, (
        f"an enquiry carrying no consent returned {response.status_code}, "
        f"expected a refusal: {fixtures.body_excerpt(response)}"
    )


def test_the_acknowledgement_reaches_the_mail_server(anon, inbox):
    email = fixtures.unique_email()
    payload = fixtures.enquiry_payload(email=email)
    fixtures.submitted(anon, payload)
    message = fixtures.poll_until(
        lambda: inbox.find(email, fixtures.PROJECT_SUBJECT), 60.0)
    assert message is not None, (
        f"no acknowledgement carrying the subject "
        f"{fixtures.PROJECT_SUBJECT!r} reached {email}; the acknowledgement is "
        f"committed in the same transaction as the lead"
    )
    assert message.subject.startswith(fixtures.PROJECT_SUBJECT), (
        f"the acknowledgement subject is {message.subject!r}, expected it to "
        f"begin with {fixtures.PROJECT_SUBJECT!r}"
    )


def test_an_application_acknowledgement_carries_its_own_subject(anon, inbox):
    email = fixtures.unique_email()
    payload = fixtures.enquiry_payload(branch=fixtures.BRANCH_APPLICATION,
                                       email=email)
    fixtures.submitted(anon, payload)
    message = fixtures.poll_until(
        lambda: inbox.find(email, fixtures.APPLICATION_SUBJECT), 60.0)
    assert message is not None, (
        f"an application to {email} produced no acknowledgement carrying "
        f"{fixtures.APPLICATION_SUBJECT!r}"
    )


def test_the_acknowledgement_is_addressed_to_the_enquirer_alone(anon, inbox):
    email = fixtures.unique_email()
    fixtures.submitted(anon, fixtures.enquiry_payload(email=email))
    message = fixtures.poll_until(
        lambda: inbox.find(email, fixtures.PROJECT_SUBJECT), 60.0)
    assert message is not None, (
        f"no acknowledgement reached {email}"
    )
    assert len(message.to) == 1, (
        f"the acknowledgement was addressed to {message.to!r}; it goes to the "
        f"one typed address with no carbon copy and no blind carbon copy"
    )


def test_the_acknowledgement_never_quotes_the_payload_back(anon, inbox):
    email = fixtures.unique_email()
    payload = fixtures.enquiry_payload(email=email)
    fixtures.submitted(anon, payload)
    message = fixtures.poll_until(
        lambda: inbox.find(email, fixtures.PROJECT_SUBJECT), 60.0)
    assert message is not None, f"no acknowledgement reached {email}"
    answer = payload["answers"][0]["answer"]
    assert answer not in message.body, (
        f"the acknowledgement quotes the submitted answer back at the sender; "
        f"a mailbox is not a place to put somebody's answers"
    )


def test_a_lead_stores_the_question_wording_used_at_submission(anon, commercial):
    payload = fixtures.enquiry_payload()
    reference = fixtures.reference_of(fixtures.submitted(anon, payload))
    row = fixtures.poll_until(
        lambda: fixtures.lead_by_reference(commercial, reference), 30.0)
    assert row is not None, f"no lead carries {reference!r}"
    ident = row.get("lead_id", row.get("id"))
    detail = commercial.get(f"/console/leads/{ident}")
    assert detail.status_code in fixtures.OK, (
        f"GET /api/console/leads/{ident} returned {detail.status_code}: "
        f"{fixtures.body_excerpt(detail)}"
    )
    stored = str(detail.json())
    for entry in payload["answers"]:
        assert entry["question"] in stored, (
            f"the lead detail does not carry the question {entry['question']!r} "
            f"as it was worded at submission"
        )


def test_a_consent_record_is_written_with_the_lead(anon, commercial):
    reference = fixtures.reference_of(
        fixtures.submitted(anon, fixtures.enquiry_payload()))
    row = fixtures.poll_until(
        lambda: fixtures.lead_by_reference(commercial, reference), 30.0)
    assert row is not None, f"no lead carries {reference!r}"
    ident = row.get("lead_id", row.get("id"))
    detail = commercial.get(f"/console/leads/{ident}")
    assert detail.status_code in fixtures.OK, (
        f"GET /api/console/leads/{ident} returned {detail.status_code}"
    )
    assert "consent" in str(detail.json()).lower(), (
        f"the lead carries no consent record: {fixtures.body_excerpt(detail)}"
    )


def test_closing_a_lead_without_a_reason_is_refused(anon, commercial):
    reference = fixtures.reference_of(
        fixtures.submitted(anon, fixtures.enquiry_payload()))
    row = fixtures.poll_until(
        lambda: fixtures.lead_by_reference(commercial, reference), 30.0)
    assert row is not None, f"no lead carries {reference!r}"
    ident = row.get("lead_id", row.get("id"))
    response = commercial.post(f"/console/leads/{ident}/close", json={})
    assert response.status_code in fixtures.REFUSED, (
        f"closing a lead with no reason returned {response.status_code}, "
        f"expected a refusal: {fixtures.body_excerpt(response)}"
    )
    after = fixtures.lead_by_reference(commercial, reference)
    assert after and after.get("state") != fixtures.LEAD_CLOSED, (
        f"a refused close still moved the lead to {fixtures.LEAD_CLOSED}"
    )


def test_a_lead_is_routed_or_visibly_unrouted(anon, commercial):
    reference = fixtures.reference_of(
        fixtures.submitted(anon, fixtures.enquiry_payload()))
    row = fixtures.poll_until(
        lambda: fixtures.lead_by_reference(commercial, reference), 30.0)
    assert row is not None, f"no lead carries {reference!r}"
    assert "owner" in row, (
        f"a lead carries no owner field, so a lead that is neither assigned nor "
        f"visibly unassigned has nowhere to be seen: {row!r}"
    )


def test_a_document_is_unreachable_while_its_scan_is_pending(commercial):
    rows = fixtures.lead_rows(commercial, branch=fixtures.BRANCH_APPLICATION)
    assert rows, (
        f"no seeded application lead exists, so the document boundary has no "
        f"case on the first page load"
    )
    pending = None
    for row in rows:
        ident = row.get("lead_id", row.get("id"))
        detail = commercial.get(f"/console/leads/{ident}")
        if detail.status_code not in fixtures.OK:
            continue
        for document in fixtures.as_list(detail.json().get("documents", [])):
            if document.get("scan_state") == fixtures.PENDING_SCAN:
                pending = document
                break
        if pending:
            break
    assert pending is not None, (
        f"no seeded application carries a document in {fixtures.PENDING_SCAN}"
    )
    ident = pending.get("document_id", pending.get("id"))
    response = commercial.get(f"/console/documents/{ident}/download",
                              params={"assertion": fixtures.PASSWORD})
    assert response.status_code in fixtures.REFUSED + fixtures.MISSING, (
        f"a document still in {fixtures.PENDING_SCAN} was released with "
        f"{response.status_code}; the check is made where the bytes are read, "
        f"not by hiding the control: {fixtures.body_excerpt(response)}"
    )


def test_a_document_download_is_refused_to_an_editor(editor):
    response = editor.get("/console/documents/1/download",
                          params={"assertion": fixtures.PASSWORD})
    assert response.status_code in fixtures.MISSING, (
        f"an editor reaching a candidate document returned "
        f"{response.status_code}, expected the status an absent record carries: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_a_document_download_is_refused_without_a_token(anon):
    response = anon.get("/console/documents/1/download")
    assert response.status_code in fixtures.DENIED, (
        f"an unauthenticated caller reaching a candidate document returned "
        f"{response.status_code}, expected a denial"
    )


def test_a_withdrawal_removes_the_lead_and_returns_a_certificate(anon, commercial):
    payload = fixtures.enquiry_payload()
    created = fixtures.submitted(anon, payload)
    reference = fixtures.reference_of(created)
    token = created.get("withdrawal_token") or created.get("token")
    assert token, (
        f"the enquiry response carries no withdrawal token, so the one-action "
        f"link in the acknowledgement has nothing to carry: {created!r}"
    )
    response = anon.post(f"/enquiries/{reference}/withdraw",
                         json={"token": token})
    assert response.status_code in fixtures.OK, (
        f"POST /api/enquiries/{reference}/withdraw returned "
        f"{response.status_code}: {fixtures.body_excerpt(response)}"
    )
    certificate = str(response.json())
    assert "store" in certificate.lower() or "lead" in certificate.lower(), (
        f"the withdrawal returned no certificate naming the stores the record "
        f"was removed from: {certificate[:400]}"
    )
    gone = fixtures.poll_until(
        lambda: fixtures.lead_by_reference(commercial, reference) is None, 30.0)
    assert gone, (
        f"the lead carrying {reference!r} is still in the inbox after a "
        f"withdrawal"
    )


def test_a_withdrawn_reference_no_longer_resolves(anon):
    created = fixtures.submitted(anon, fixtures.enquiry_payload())
    reference = fixtures.reference_of(created)
    token = created.get("withdrawal_token") or created.get("token")
    assert token, f"the enquiry response carries no withdrawal token: {created!r}"
    withdraw = anon.post(f"/enquiries/{reference}/withdraw",
                         json={"token": token})
    assert withdraw.status_code in fixtures.OK, (
        f"the withdrawal returned {withdraw.status_code}: "
        f"{fixtures.body_excerpt(withdraw)}"
    )
    fixtures.settle()
    response = anon.get(f"/enquiries/{reference}")
    assert response.status_code in fixtures.MISSING, (
        f"the withdrawn reference {reference!r} still resolves with "
        f"{response.status_code}: {fixtures.body_excerpt(response)}"
    )


def test_a_privileged_read_writes_an_activity_entry(anon, commercial):
    reference = fixtures.reference_of(
        fixtures.submitted(anon, fixtures.enquiry_payload()))
    row = fixtures.poll_until(
        lambda: fixtures.lead_by_reference(commercial, reference), 30.0)
    assert row is not None, f"no lead carries {reference!r}"
    ident = row.get("lead_id", row.get("id"))
    before = len(fixtures.activity_rows(commercial))
    detail = commercial.get(f"/console/leads/{ident}")
    assert detail.status_code in fixtures.OK, (
        f"GET /api/console/leads/{ident} returned {detail.status_code}"
    )
    after = fixtures.poll_until(
        lambda: len(fixtures.activity_rows(commercial)) > before, 30.0)
    assert after, (
        f"opening a lead wrote no activity entry; every privileged read is "
        f"recorded with who, what, which record and when"
    )


def test_activity_entries_cannot_be_updated_or_deleted(commercial):
    rows = fixtures.activity_rows(commercial)
    assert rows, (
        f"the activity log is empty, so its append-only property cannot be "
        f"observed"
    )
    ident = rows[0].get("entry_id", rows[0].get("id"))
    patched = commercial.patch(f"/console/activity/{ident}",
                               json={"actor": "somebody-else"})
    assert patched.status_code in fixtures.REFUSED + fixtures.MISSING + (405,), (
        f"an activity entry accepted an update with {patched.status_code}; the "
        f"log is append-only at the database grant, so no handler anybody "
        f"writes later can weaken it: {fixtures.body_excerpt(patched)}"
    )
    deleted = commercial.delete(f"/console/activity/{ident}")
    assert deleted.status_code in fixtures.REFUSED + fixtures.MISSING + (405,), (
        f"an activity entry accepted a delete with {deleted.status_code}"
    )


def test_every_public_route_carries_a_distinct_title_and_description():
    seen_titles = {}
    seen_descriptions = {}
    for path in fixtures.FRENCH_ROUTES + fixtures.ENGLISH_ROUTES:
        response = fixtures.page(path)
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}"
        )
        body = response.text
        start = body.lower().find("<title>")
        end = body.lower().find("</title>")
        assert start != -1 and end > start, f"{path} carries no title element"
        title = body[start + 7:end].strip()
        assert title, f"{path} carries an empty title"
        assert title not in seen_titles, (
            f"{path} shares its title {title!r} with {seen_titles[title]!r}; a "
            f"site where two pages share one title is two pages a search engine "
            f"treats as one"
        )
        seen_titles[title] = path
        marker = 'name="description"'
        index = body.lower().find(marker)
        assert index != -1, f"{path} declares no description"
        window = body[index:index + 400]
        content = window.lower().find('content="')
        assert content != -1, f"{path} declares a description with no content"
        value = window[content + 9:].split('"')[0].strip()
        assert value, f"{path} declares an empty description"
        assert value not in seen_descriptions, (
            f"{path} shares its description with {seen_descriptions[value]!r}"
        )
        seen_descriptions[value] = path


def test_every_response_carries_the_security_headers():
    response = fixtures.page("/")
    lowered = {key.lower() for key in response.headers}
    for header in fixtures.SECURITY_HEADERS:
        assert header in lowered, (
            f"the home route carries no {header} header; the set present is "
            f"{sorted(lowered)!r}"
        )
    policy = response.headers.get("content-security-policy", "")
    assert "unsafe-inline" not in policy or "script" not in policy.split("unsafe-inline")[0][-80:], (
        f"the content security policy allows unsafe-inline for scripts, which "
        f"removes most of the value of the policy: {policy!r}"
    )


def test_no_credential_reaches_the_browser():
    for path in fixtures.FRENCH_ROUTES:
        body = fixtures.page(path).text
        assert fixtures.PASSWORD not in body, (
            f"{path} ships the corpus password in what the browser downloads"
        )
        assert "postgres://" not in body, (
            f"{path} ships a database address in what the browser downloads"
        )


def test_the_privacy_page_is_reachable_from_every_public_route():
    for path in fixtures.FRENCH_ROUTES:
        body = fixtures.page(path).text
        assert "/confidentialite/" in body, (
            f"{path} carries no link to the personal-data page, which is "
            f"reachable from the footer of every page"
        )


def test_every_internal_link_on_the_catalogue_resolves():
    body = fixtures.page("/projets/").text
    targets = set()
    cursor = 0
    while True:
        index = body.find('href="/', cursor)
        if index == -1:
            break
        end = body.find('"', index + 6)
        if end == -1:
            break
        targets.add(body[index + 6:end])
        cursor = end
    assert targets, "the catalogue route carries no internal link at all"
    for target in sorted(targets):
        if target.startswith("//") or "#" in target:
            continue
        response = fixtures.page(target)
        assert response.status_code == 200, (
            f"the internal link {target!r} on /projets/ answered "
            f"{response.status_code}"
        )


def test_an_unknown_address_answers_not_found_with_the_product_page():
    response = fixtures.page("/projets/pas-un-projet-du-tout/", follow=False)
    assert response.status_code == 404, (
        f"an unknown address answered {response.status_code}; a not-found page "
        f"answering with a success status tells a search engine the page exists"
    )
    assert fixtures.NOT_FOUND_COPY in response.text, (
        f"the not-found route renders no product copy; the pinned body is "
        f"{fixtures.NOT_FOUND_COPY!r}"
    )


def test_a_not_found_on_an_english_path_answers_in_english():
    response = fixtures.page("/en/projects/not-a-project-at-all/", follow=False)
    assert response.status_code == 404, (
        f"an unknown English address answered {response.status_code}"
    )
    assert fixtures.NOT_FOUND_COPY not in response.text, (
        f"a not-found on an English path rendered the French copy; the error "
        f"route inherits the locale of the address that produced it"
    )


def test_the_health_route_answers(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_seeding_is_idempotent(backend):
    rows = backend.count("account")
    assert rows >= 4, (
        f"the datastore holds {rows} account rows; four accounts are seeded"
    )
    assert rows < 40, (
        f"the datastore holds {rows} account rows, which is what repeated "
        f"non-idempotent seeding looks like"
    )
