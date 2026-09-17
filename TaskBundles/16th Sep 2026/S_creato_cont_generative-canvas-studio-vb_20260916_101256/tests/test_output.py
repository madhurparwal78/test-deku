from __future__ import annotations

import re
import struct

import httpx
from playwright.sync_api import expect

import appclient
import conftest as fx
import _shapes


def test_health_route_answers_ready():
    """The health route answers once the app is ready."""
    response = httpx.get(f"{fx.api_base()}/health", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code} rather than 200: {response.text[:300]}"
    )


def test_app_serves_the_api_on_its_own_origin():
    """The app answers at its public address with the API on the same origin."""
    home = fx.page_response("/")
    assert home.status_code == 200, (
        f"GET / at {fx.app_url()} returned {home.status_code}: {home.text[:300]}"
    )
    models = httpx.get(f"{fx.api_base()}/v1/models", timeout=fx.TIMEOUT)
    assert models.status_code == 200, (
        f"GET /api/v1/models on the page origin returned {models.status_code}: {models.text[:300]}"
    )
    assert fx.api_base().startswith(fx.app_url()), (
        f"the API base {fx.api_base()} is not on the origin {fx.app_url()}"
    )


def test_seeded_accounts_sign_in_with_the_corpus_password():
    """Each seeded account signs in with the pinned password and reports its role."""
    expected = {fx.OWNER_EMAIL: "creator", fx.SECOND_STUDIO_EMAIL: "creator",
                fx.MEMBER_EMAIL: "creator", fx.CLIENT_EMAIL: "client"}
    for email, role in expected.items():
        name = fx.SEEDED_NAMES[email]
        response = httpx.post(f"{fx.api_base()}/auth/login",
                              json={"email": email, "password": fx.CORPUS_PASSWORD},
                              timeout=fx.TIMEOUT)
        assert response.status_code == 200, (
            f"login for {email} returned {response.status_code}: {response.text[:300]}"
        )
        body = response.json()
        assert body.get("access_token"), f"login for {email} returned no access_token"
        assert body.get("user", {}).get("role") == role, (
            f"login for {email} reports role {body.get('user', {}).get('role')!r}, not {role!r}"
        )
        assert body.get("user", {}).get("display_name") == name, (
            f"login for {email} reports display name {body.get('user', {}).get('display_name')!r}"
        )


def test_login_refusal_does_not_reveal_which_addresses_exist():
    """A wrong password and an unknown address are refused alike."""
    wrong = httpx.post(f"{fx.api_base()}/auth/login",
                       json={"email": fx.OWNER_EMAIL, "password": "not-the-password-11"},
                       timeout=fx.TIMEOUT)
    unknown = httpx.post(f"{fx.api_base()}/auth/login",
                         json={"email": fx.probe_email(), "password": "not-the-password-11"},
                         timeout=fx.TIMEOUT)
    assert fx.refused(wrong) and fx.refused(unknown), (
        f"login refusals returned {wrong.status_code} and {unknown.status_code}"
    )
    assert wrong.status_code == unknown.status_code, (
        f"a wrong password answered {wrong.status_code} while an unknown address answered "
        f"{unknown.status_code}, which reveals which addresses exist"
    )
    assert fx.error_code(wrong) == fx.error_code(unknown), (
        f"the two refusals carry different codes: {wrong.text[:200]} / {unknown.text[:200]}"
    )


def test_creator_signup_opens_a_free_studio_with_trial_credits():
    """A creator sign-up opens a named free studio holding the one trial grant."""
    email, token, body = fx.sign_up("creator", "Mina Park")
    assert body.get("user", {}).get("role") == "creator", (
        f"sign-up for {email} created role {body.get('user', {}).get('role')!r}"
    )
    with appclient.client(token) as client:
        studio = fx.workspace(client)
        assert studio.get("name") == "Mina Park's studio", (
            f"the new studio is named {studio.get('name')!r}"
        )
        assert studio.get("plan_code") == "free", (
            f"the new studio is on {studio.get('plan_code')!r}, not free"
        )
        credits = client.get("/v1/credits").json()
        assert credits.get("balance") == fx.TRIAL_CREDITS, (
            f"the new studio holds {credits.get('balance')} credits, not {fx.TRIAL_CREDITS}"
        )
        trials = [e for e in credits.get("entries", []) if e.get("kind") == "trial"]
        assert len(trials) == 1 and trials[0].get("amount") == fx.TRIAL_CREDITS, (
            f"the trial grant entries are {trials}"
        )


def test_client_signup_creates_a_client_without_a_studio():
    """A client sign-up creates a client, who has no studio and no canvases."""
    _, token, body = fx.sign_up("client", "Probe Client")
    assert body.get("user", {}).get("role") == "client", (
        f"a client sign-up created role {body.get('user', {}).get('role')!r}"
    )
    with appclient.client(token) as client:
        studio = client.get("/v1/workspace")
        assert fx.refused(studio), (
            f"GET /api/v1/workspace as a client returned {studio.status_code}: {studio.text[:200]}"
        )
        listing = client.get("/v1/deliveries")
        assert listing.status_code == 200 and _shapes.items(listing.json()) == [], (
            f"a new client's deliveries are {listing.status_code} {listing.text[:200]}"
        )


def test_signup_with_an_invalid_field_is_refused_and_names_it(backend):
    """A short password, a malformed address or an empty name is refused and writes nothing."""
    cases = (
        ({"password": "short"}, "password"),
        ({"email": "not-an-address"}, "email"),
        ({"display_name": ""}, "display_name"),
        ({"display_name": "n" * 61}, "display_name"),
    )
    for override, field in cases:
        email = fx.probe_email()
        payload = {"email": email, "password": fx.CORPUS_PASSWORD, "display_name": "Probe"}
        payload.update(override)
        response = httpx.post(f"{fx.api_base()}/auth/sign-up", json=payload, timeout=fx.TIMEOUT)
        assert fx.refused(response), (
            f"sign-up with a bad {field} returned {response.status_code}: {response.text[:200]}"
        )
        assert fx.error_code(response) == "invalid_request", (
            f"sign-up with a bad {field} carried code {fx.error_code(response)!r}"
        )
        assert field in response.text, (
            f"the refusal for a bad {field} does not name the field: {response.text[:300]}"
        )
        assert backend.count("app_user", email=payload["email"]) == 0, (
            f"a refused sign-up stored a user row for {payload['email']}"
        )


def test_duplicate_signup_is_refused_and_creates_nothing(backend):
    """A second sign-up with an address in use is a conflict and adds no account."""
    email, _, _ = fx.sign_up("creator")
    response = httpx.post(f"{fx.api_base()}/auth/sign-up", timeout=fx.TIMEOUT, json={
        "email": email, "password": fx.CORPUS_PASSWORD, "display_name": "Second Claim"})
    assert fx.refused(response) and fx.error_code(response) == "conflict", (
        f"a duplicate sign-up returned {response.status_code}: {response.text[:300]}"
    )
    assert backend.count("app_user", email=email) == 1, (
        f"a duplicate sign-up left {backend.count('app_user', email=email)} rows for {email}"
    )


def test_signup_with_an_unknown_account_type_is_refused(backend):
    """An account type other than creator or client is refused."""
    email = fx.probe_email()
    response = httpx.post(f"{fx.api_base()}/auth/sign-up", timeout=fx.TIMEOUT, json={
        "email": email, "password": fx.CORPUS_PASSWORD, "display_name": "Probe",
        "account_type": "admin"})
    assert fx.refused(response), (
        f"sign-up with account_type admin returned {response.status_code}: {response.text[:300]}"
    )
    assert backend.count("app_user", email=email) == 0, "a refused sign-up stored a user row"


def test_me_reports_role_and_studio_membership(owner, member, client_user):
    """The me route reports the role and, for creators, the studio membership."""
    mine = owner.get("/auth/me").json()
    assert mine.get("role") == "creator", f"/api/auth/me for the owner reports {mine}"
    assert fx.NORTHLIGHT in str(mine) and "owner" in str(mine), (
        f"/api/auth/me for the owner does not name the studio membership: {mine}"
    )
    theirs = member.get("/auth/me").json()
    assert fx.NORTHLIGHT in str(theirs) and "member" in str(theirs), (
        f"/api/auth/me for the member does not report member of {fx.NORTHLIGHT}: {theirs}"
    )
    client = client_user.get("/auth/me").json()
    assert client.get("role") == "client", f"/api/auth/me for the client reports {client}"


def test_workspace_reports_plan_balance_and_members(owner):
    """The studio route reports the plan, the balance and the members."""
    studio = fx.workspace(owner)
    assert studio.get("name") == fx.NORTHLIGHT, f"the owner's studio is {studio.get('name')!r}"
    assert studio.get("plan_code") == "professional", f"plan is {studio.get('plan_code')!r}"
    assert studio.get("billing_period") == "monthly", f"period is {studio.get('billing_period')!r}"
    assert studio.get("credit_option") == "110k", f"option is {studio.get('credit_option')!r}"
    assert studio.get("seat_limit") is None, f"seat_limit is {studio.get('seat_limit')!r}"
    assert studio.get("credit_balance") == fx.balance(owner), (
        "the studio route and the credits route disagree on the balance"
    )
    members = {m.get("email"): m.get("membership") for m in studio.get("members", [])}
    assert members.get(fx.OWNER_EMAIL) == "owner", f"members are {members}"
    assert members.get(fx.MEMBER_EMAIL) == "member", f"members are {members}"
    assert isinstance(studio.get("pending_invitations"), list), (
        f"pending_invitations is {studio.get('pending_invitations')!r}"
    )
    downgrade = fx.subscribe(owner, "growth", "monthly")
    assert fx.refused(downgrade) and fx.error_code(downgrade) == "limit_reached", (
        f"moving a two-member studio to a one-seat plan returned {downgrade.status_code}"
    )
    assert fx.workspace(owner).get("plan_code") == "professional", "a refused downgrade changed the plan"


def test_invitation_on_a_single_seat_plan_is_refused_with_limit_reached():
    """A studio on a one-seat plan cannot invite a teammate."""
    with fx.fresh_creator() as client:
        response = client.post("/v1/workspace/invitations", json={"email": fx.probe_email()})
        assert fx.refused(response) and fx.error_code(response) == "limit_reached", (
            f"inviting from a free studio returned {response.status_code}: {response.text[:300]}"
        )
        assert fx.workspace(client).get("pending_invitations") == [], (
            "a refused invitation was recorded"
        )


def test_invited_address_joins_the_studio_on_signup_without_trial_credits(owner):
    """An invited address signs up into the inviting studio as a member."""
    email = fx.probe_email()
    response = owner.post("/v1/workspace/invitations", json={"email": email})
    assert response.status_code in (200, 201), (
        f"inviting {email} returned {response.status_code}: {response.text[:300]}"
    )
    assert email in fx.workspace(owner).get("pending_invitations", []), (
        f"{email} is not listed among the pending invitations"
    )
    _, token, _ = fx.sign_up("creator", "Invited Maker", email=email)
    with appclient.client(token) as joined:
        studio = fx.workspace(joined)
        assert studio.get("name") == fx.NORTHLIGHT, (
            f"the invited address joined {studio.get('name')!r}, not {fx.NORTHLIGHT}"
        )
        mine = [m for m in studio.get("members", []) if m.get("email") == email]
        assert mine and mine[0].get("membership") == "member", f"membership rows are {mine}"
        entries = joined.get("/v1/credits").json().get("entries", [])
        assert not [e for e in entries if e.get("kind") == "trial"], (
            "joining an invited studio granted trial credits"
        )
    assert email not in fx.workspace(owner).get("pending_invitations", []), (
        f"{email} is still pending after signing up"
    )


def test_invitation_for_an_existing_account_is_refused_as_conflict(owner):
    """Inviting an address that already has an account, or inviting twice, is a conflict."""
    existing = owner.post("/v1/workspace/invitations", json={"email": fx.CLIENT_EMAIL})
    assert fx.refused(existing) and fx.error_code(existing) == "conflict", (
        f"inviting an existing account returned {existing.status_code}: {existing.text[:300]}"
    )
    email = fx.probe_email()
    first = owner.post("/v1/workspace/invitations", json={"email": email})
    assert first.status_code in (200, 201), f"first invitation returned {first.status_code}"
    again = owner.post("/v1/workspace/invitations", json={"email": email})
    assert fx.refused(again) and fx.error_code(again) == "conflict", (
        f"inviting {email} twice returned {again.status_code}: {again.text[:300]}"
    )



def test_subscription_records_the_amount_and_grants_the_allowance():
    """Choosing Creator monthly records 2000 and grants twenty thousand credits."""
    with fx.fresh_creator() as client:
        response = fx.subscribe(client, "creator", "monthly")
        assert response.status_code in (200, 201), (
            f"subscribing to creator returned {response.status_code}: {response.text[:300]}"
        )
        studio = fx.workspace(client)
        assert studio.get("plan_code") == "creator", f"plan is {studio.get('plan_code')!r}"
        events = fx.listed(client.get("/v1/billing-events"))
        assert [e.get("amount_minor") for e in events] == [2000], (
            f"billing events after one subscription are {events}"
        )
        assert events[0].get("currency") == "usd", f"currency is {events[0].get('currency')!r}"
        assert fx.balance(client) == fx.TRIAL_CREDITS + 20000, (
            f"balance after the grant is {fx.balance(client)}"
        )


def test_annual_subscription_records_twelve_times_the_monthly_equivalent():
    """Annual billing records twelve times the per-month annual price."""
    with fx.fresh_creator() as client:
        assert fx.subscribe(client, "creator", "annual").status_code in (200, 201)
        events = fx.listed(client.get("/v1/billing-events"))
        assert events and events[0].get("amount_minor") == 20400, (
            f"creator annual recorded {events}"
        )
    with fx.fresh_creator() as client:
        assert fx.subscribe(client, "professional", "annual", "110k").status_code in (200, 201)
        events = fx.listed(client.get("/v1/billing-events"))
        assert events and events[0].get("amount_minor") == 111600, (
            f"professional 110k annual recorded {events}"
        )


def test_professional_300k_subscription_grants_three_hundred_thousand():
    """The 300K option records 30000 monthly and grants 300,000 credits."""
    with fx.fresh_creator() as client:
        response = fx.subscribe(client, "professional", "monthly", "300k")
        assert response.status_code in (200, 201), response.text[:300]
        events = fx.listed(client.get("/v1/billing-events"))
        assert events and events[0].get("amount_minor") == 30000, f"events are {events}"
        assert fx.balance(client) == fx.TRIAL_CREDITS + 300000, (
            f"balance after a 300K grant is {fx.balance(client)}"
        )
        studio = fx.workspace(client)
        assert studio.get("credit_option") == "300k" and studio.get("seat_limit") is None, (
            f"the studio reads {studio}"
        )


def test_replayed_subscription_key_writes_no_second_billing_event(backend):
    """A repeated subscription with the same key writes one event and one grant."""
    with fx.fresh_creator() as client:
        key = fx.idem_key()
        first = fx.subscribe(client, "growth", "monthly", key=key)
        second = fx.subscribe(client, "growth", "monthly", key=key)
        assert first.status_code in (200, 201) and second.status_code in (200, 201), (
            f"the two identical subscriptions returned {first.status_code}, {second.status_code}"
        )
        events = fx.listed(client.get("/v1/billing-events"))
        assert len(events) == 1 and events[0].get("amount_minor") == 5000, (
            f"a replayed key produced billing events {events}"
        )
        grants = [e for e in client.get("/v1/credits").json()["entries"]
                  if e.get("kind") == "plan_grant"]
        assert len(grants) == 1 and grants[0].get("amount") == 50000, (
            f"a replayed key produced grants {grants}"
        )
        studio_id = fx.workspace(client)["id"]
        assert backend.count("billing_event", workspace_id=studio_id) == 1, (
            "the store holds more than one billing event for a replayed key"
        )


def test_subscription_to_enterprise_or_free_is_refused():
    """Enterprise, Free and an unsized Professional cannot be chosen through the subscription route."""
    with fx.fresh_creator() as client:
        for plan in ("enterprise", "free"):
            response = fx.subscribe(client, plan, "monthly")
            assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
                f"subscribing to {plan} returned {response.status_code}: {response.text[:200]}"
            )
        bare = fx.subscribe(client, "professional", "monthly")
        assert fx.refused(bare) and fx.error_code(bare) == "invalid_request", (
            f"professional with no credit option returned {bare.status_code}"
        )
        assert fx.workspace(client).get("plan_code") == "free", "a refused subscription changed the plan"
        assert fx.listed(client.get("/v1/billing-events")) == [], "a refused subscription was billed"



def test_credit_packs_on_free_are_refused_with_plan_required():
    """A studio on the free plan cannot buy credit packs."""
    with fx.fresh_creator() as client:
        response = fx.buy_packs(client, 2)
        assert fx.refused(response) and fx.error_code(response) == "plan_required", (
            f"buying packs on free returned {response.status_code}: {response.text[:300]}"
        )
        assert fx.balance(client) == fx.TRIAL_CREDITS, "a refused pack purchase changed the balance"


def test_credit_pack_purchase_adds_credits_and_records_the_charge():
    """Three packs add three thousand credits and record 3000, once per key."""
    with fx.fresh_creator() as client:
        assert fx.subscribe(client, "creator", "monthly").status_code in (200, 201)
        before = fx.balance(client)
        key = fx.idem_key()
        first = fx.buy_packs(client, 3, key)
        again = fx.buy_packs(client, 3, key)
        assert first.status_code in (200, 201) and again.status_code in (200, 201), (
            f"the pack purchase returned {first.status_code}, {again.status_code}"
        )
        assert fx.balance(client) == before + 3 * fx.PACK_CREDITS, (
            f"balance moved from {before} to {fx.balance(client)}"
        )
        packs = [e for e in fx.listed(client.get("/v1/billing-events"))
                 if e.get("kind") == "credit_pack"]
        assert len(packs) == 1 and packs[0].get("amount_minor") == 3 * fx.PACK_PRICE_MINOR, (
            f"pack billing events are {packs}"
        )
        altered = fx.buy_packs(client, 5, key)
        assert fx.refused(altered) and fx.error_code(altered) == "conflict", (
            f"reusing a key with a different body returned {altered.status_code}"
        )
        assert fx.balance(client) == before + 3 * fx.PACK_CREDITS, "a reused key with a new body wrote credits"
        too_many = fx.buy_packs(client, 21)
        assert fx.refused(too_many), f"buying 21 packs returned {too_many.status_code}"


def test_billing_events_are_newest_first_for_the_owner(owner, member):
    """The owner reads the billing ledger newest first; a member is denied it."""
    with fx.fresh_creator() as client:
        fx.subscribe(client, "creator", "monthly")
        fx.buy_packs(client, 1)
        events = fx.listed(client.get("/v1/billing-events"))
        assert [e.get("kind") for e in events] == ["credit_pack", "subscription"], (
            f"billing events are not newest first: {events}"
        )
    seeded = fx.listed(owner.get("/v1/billing-events"))
    assert any(e.get("amount_minor") == 11000 and e.get("plan_code") == "professional"
               for e in seeded), f"the seeded Northlight subscription is missing: {seeded}"
    denied = member.get("/v1/billing-events")
    assert fx.refused(denied), f"a member read the billing ledger with {denied.status_code}"


def test_canvas_creation_rejects_duplicates_and_bad_names(owner):
    """A canvas name is required, bounded and unique within the studio."""
    name = f"Probe unique {fx.unique_suffix()}"
    first = owner.post("/v1/canvases", json={"name": name})
    assert first.status_code in (200, 201), f"creating {name} returned {first.status_code}"
    dup = owner.post("/v1/canvases", json={"name": name})
    assert fx.refused(dup) and fx.error_code(dup) == "conflict", (
        f"a duplicate canvas name returned {dup.status_code}: {dup.text[:200]}"
    )
    for bad in ("", "x" * 81):
        response = owner.post("/v1/canvases", json={"name": bad})
        assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
            f"a canvas named with {len(bad)} characters returned {response.status_code}"
        )
    listing = fx.canvases(owner)
    assert sum(1 for c in listing if c.get("name") == name) == 1, "the duplicate was stored"
    assert {"id", "name", "node_count", "credits_spent", "last_run_at", "updated_at"} <= set(listing[0]), (
        f"a canvas row lacks the pinned fields: {listing[0]}"
    )


def test_canvas_detail_derives_node_ranks_from_edges(citrus):
    """Citrus Launch carries the advertising graph with ranks derived from its wires."""
    nodes = {n.get("node_key"): n for n in citrus.get("nodes", [])}
    assert set(nodes) == set(fx.ADVERTISING_NODES), f"Citrus Launch nodes are {sorted(nodes)}"
    for key, (title, _kind, model, aspect, rank, _inputs) in fx.ADVERTISING_NODES.items():
        node = nodes[key]
        assert node.get("title") == title and node.get("model_slug") == model, (
            f"node {key} reads {node.get('title')!r} on {node.get('model_slug')!r}"
        )
        assert node.get("rank") == rank, f"node {key} has rank {node.get('rank')}, not {rank}"
        assert node.get("aspect_ratio") == aspect, f"node {key} has aspect {node.get('aspect_ratio')!r}"
        assert node.get("is_stale") is False, f"seeded node {key} is stale"
        assert node.get("latest_output"), f"seeded node {key} has no output"
    by_id = {n["id"]: n["node_key"] for n in citrus["nodes"]}
    wires = {(by_id[e["from_node_id"]], by_id[e["to_node_id"]]) for e in citrus.get("edges", [])}
    expected = {(src, key) for key, spec in fx.ADVERTISING_NODES.items() for src in spec[5]}
    assert wires == expected, f"Citrus Launch wires are {sorted(wires)}"


def test_auto_model_resolves_to_the_fastest_available_model(owner):
    """A node created with auto stores the fastest available model of its kind."""
    canvas = fx.new_canvas(owner, "Probe auto")
    for kind, slug in fx.AUTO_RESOLUTION.items():
        aspect = fx.ASPECTS[kind][0] if fx.ASPECTS[kind] else None
        node = fx.add_node(owner, canvas["id"], title=f"Auto {kind}", model_slug="auto",
                           aspect_ratio=aspect, output_kind=kind)
        assert node.get("model_slug") == slug, (
            f"auto for {kind} resolved to {node.get('model_slug')!r}, not {slug!r}"
        )
        assert node.get("revision") == 1, f"a new node starts at revision {node.get('revision')}"
        assert node.get("is_stale") is False, f"a never-run {kind} node reads stale"
    twins = [fx.add_node(owner, canvas["id"], title="Probe Twin", model_slug="quill-3-mini",
                         aspect_ratio=None)["node_key"] for _ in range(2)]
    assert twins[0] == "probe-twin", f"the node key for Probe Twin is {twins[0]!r}"
    assert twins[1] != twins[0] and re.fullmatch(r"probe-twin-?\d+", twins[1]), (
        f"a second Probe Twin carries the key {twins[1]!r}"
    )


def test_node_aspect_ratio_outside_the_model_list_is_refused(owner):
    """An image node cannot take an aspect its model does not list."""
    canvas = fx.new_canvas(owner, "Probe aspect")
    response = owner.post(f"/v1/canvases/{canvas['id']}/nodes", json={
        "title": "Tall still", "prompt": "a tall still", "model_slug": "halcyon-2-1",
        "tier": "standard", "aspect_ratio": "9:16", "pos_x": 0, "pos_y": 0})
    assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
        f"a 9:16 image node returned {response.status_code}: {response.text[:200]}"
    )
    detail = owner.get(f"/v1/canvases/{canvas['id']}").json()
    assert detail.get("nodes") == [], "a refused node was stored"


def test_edge_that_closes_a_loop_is_refused(owner):
    """Self wires, loops and duplicate wires are refused and write nothing."""
    canvas = fx.new_canvas(owner, "Probe loop")
    first = fx.add_node(owner, canvas["id"], title="First", model_slug="quill-3-mini",
                        aspect_ratio=None)
    second = fx.add_node(owner, canvas["id"], title="Second", model_slug="quill-3-mini",
                         aspect_ratio=None)
    assert fx.wire(owner, canvas["id"], first["id"], second["id"]).status_code in (200, 201)
    for source, target, why in ((second["id"], first["id"], "a loop"),
                                (first["id"], first["id"], "a self wire"),
                                (first["id"], second["id"], "a duplicate")):
        response = fx.wire(owner, canvas["id"], source, target)
        assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
            f"{why} returned {response.status_code}: {response.text[:200]}"
        )
    detail = owner.get(f"/v1/canvases/{canvas['id']}").json()
    assert len(detail.get("edges", [])) == 1, f"edges after refusals: {detail.get('edges')}"


def test_wire_changes_mark_the_receiving_node_stale():
    """Adding or removing a wire marks the receiving node stale; a cross-canvas wire is refused."""
    with fx.fresh_creator() as client:
        canvas, nodes = fx.chain(client, 3, model_slug="quill-3-mini")
        fx.run_chain(client, canvas, nodes)
        detail = client.get(f"/v1/canvases/{canvas['id']}").json()
        edge = [e for e in detail["edges"] if e["to_node_id"] == nodes[1]["id"]][0]
        removed = client.delete(f"/v1/canvases/{canvas['id']}/edges/{edge['id']}")
        assert removed.status_code in (200, 204), f"deleting a wire returned {removed.status_code}"
        stale = {n["id"]: n["is_stale"] for n in client.get(f"/v1/canvases/{canvas['id']}").json()["nodes"]}
        assert stale[nodes[1]["id"]] and stale[nodes[2]["id"]] and not stale[nodes[0]["id"]], (
            f"after removing a wire the stale flags are {stale}"
        )
        fx.succeeded_run(client, canvas["id"], nodes[1]["id"])
        fx.succeeded_run(client, canvas["id"], nodes[2]["id"])
        added = fx.wire(client, canvas["id"], nodes[0]["id"], nodes[2]["id"])
        assert added.status_code in (200, 201), f"adding a wire returned {added.status_code}"
        stale = {n["id"]: n["is_stale"] for n in client.get(f"/v1/canvases/{canvas['id']}").json()["nodes"]}
        assert stale[nodes[2]["id"]] and not stale[nodes[0]["id"]], (
            f"after adding a wire the stale flags are {stale}"
        )
        other = fx.new_canvas(client, "Probe other")
        stranger = fx.add_node(client, other["id"], model_slug="quill-3-mini", aspect_ratio=None)
        crossing = fx.wire(client, canvas["id"], nodes[0]["id"], stranger["id"])
        assert fx.refused(crossing) and fx.error_code(crossing) == "invalid_request", (
            f"a wire between two canvases returned {crossing.status_code}"
        )


def test_prompt_edit_marks_the_node_and_downstream_stale():
    """Editing rank two's prompt marks ranks two to five stale and leaves rank one."""
    with fx.fresh_creator() as client:
        canvas, nodes = fx.chain(client, 5, model_slug="quill-3-mini")
        fx.run_chain(client, canvas, nodes)
        target = nodes[1]
        response = client.patch(f"/v1/canvases/{canvas['id']}/nodes/{target['id']}",
                                json={"prompt": "a sharper headline", "revision": target["revision"]})
        assert response.status_code == 200, f"editing the prompt returned {response.status_code}"
        detail = client.get(f"/v1/canvases/{canvas['id']}").json()
        stale = {n["id"]: n["is_stale"] for n in detail["nodes"]}
        assert stale[nodes[0]["id"]] is False, "rank one became stale"
        assert all(stale[n["id"]] for n in nodes[1:]), f"stale flags are {stale}"
        revisions = {n["id"]: n["revision"] for n in detail["nodes"]}
        assert all(revisions[n["id"]] == n["revision"] for n in nodes[2:]), (
            f"marking downstream nodes stale moved their revisions: {revisions}"
        )
        ranks = {n["id"]: n["rank"] for n in detail["nodes"]}
        assert [ranks[n["id"]] for n in nodes] == [1, 2, 3, 4, 5], f"ranks are {ranks}"


def test_position_only_edit_marks_nothing_stale():
    """Moving a node or renaming it marks nothing stale."""
    with fx.fresh_creator() as client:
        canvas, nodes = fx.chain(client, 2, model_slug="quill-3-mini")
        fx.run_chain(client, canvas, nodes)
        response = client.patch(f"/v1/canvases/{canvas['id']}/nodes/{nodes[0]['id']}",
                                json={"pos_x": 240, "pos_y": 120, "title": "Moved",
                                      "revision": nodes[0]["revision"]})
        assert response.status_code == 200, f"moving a node returned {response.status_code}"
        detail = client.get(f"/v1/canvases/{canvas['id']}").json()
        assert not any(n["is_stale"] for n in detail["nodes"]), (
            f"a position edit marked nodes stale: {detail['nodes']}"
        )


def test_node_edit_from_an_old_revision_is_refused_as_conflict(owner):
    """A write carrying an older revision is refused and changes nothing."""
    canvas = fx.new_canvas(owner, "Probe revision")
    node = fx.add_node(owner, canvas["id"], model_slug="quill-3-mini", aspect_ratio=None)
    path = f"/v1/canvases/{canvas['id']}/nodes/{node['id']}"
    accepted = owner.patch(path, json={"prompt": "first edit", "revision": 1})
    assert accepted.status_code == 200 and accepted.json().get("revision") == 2, (
        f"an edit at the current revision returned {accepted.status_code}: {accepted.text[:200]}"
    )
    stale_write = owner.patch(path, json={"prompt": "late edit", "revision": 1})
    assert fx.refused(stale_write) and fx.error_code(stale_write) == "conflict", (
        f"an edit from revision 1 returned {stale_write.status_code}: {stale_write.text[:200]}"
    )
    current = fx.node_by_title(owner.get(f"/v1/canvases/{canvas['id']}").json(), "Probe node")
    assert current.get("prompt") == "first edit" and current.get("revision") == 2, (
        f"the refused edit changed the node: {current}"
    )


def test_concurrent_node_edits_admit_exactly_one_winner(owner, member):
    """Two members saving one node from the same revision: exactly one is accepted."""
    canvas = fx.new_canvas(owner, "Probe contention")
    node = fx.add_node(owner, canvas["id"], model_slug="quill-3-mini", aspect_ratio=None)
    path = f"/v1/canvases/{canvas['id']}/nodes/{node['id']}"
    results = fx.at_the_same_moment(
        lambda: owner.patch(path, json={"prompt": "owner wording", "revision": 1}),
        lambda: member.patch(path, json={"prompt": "member wording", "revision": 1}),
    )
    statuses = sorted(r.status_code for r in results)
    winners = [r for r in results if r.status_code == 200]
    losers = [r for r in results if fx.refused(r)]
    assert len(winners) == 1 and len(losers) == 1, f"concurrent edits returned {statuses}"
    assert fx.error_code(losers[0]) == "conflict", f"the loser carried {losers[0].text[:200]}"
    current = fx.node_by_title(owner.get(f"/v1/canvases/{canvas['id']}").json(), "Probe node")
    assert current.get("revision") == 2, f"the node reached revision {current.get('revision')}"
    assert current.get("prompt") == winners[0].json().get("prompt"), (
        "the stored prompt is not the accepted one"
    )


def test_run_charges_the_current_rate_and_stores_the_output(store, backend):
    """A run charges the current rate once and stores the output at its scheme key."""
    with fx.fresh_creator() as client:
        canvas = fx.new_canvas(client)
        node = fx.add_node(client, canvas["id"], model_slug="vesper-3", tier="high",
                           aspect_ratio="1:1")
        run = fx.succeeded_run(client, canvas["id"], node["id"])
        assert run.get("credits_charged") == 144, f"a high image charged {run.get('credits_charged')}"
        assert fx.balance(client) == fx.TRIAL_CREDITS - 144, f"balance is {fx.balance(client)}"
        output = run.get("output") or {}
        match = fx.OBJECT_KEY_RE.match(output.get("object_key", ""))
        assert match, f"the object key {output.get('object_key')!r} breaks the pinned scheme"
        studio_id = fx.workspace(client)["id"]
        assert match.group(1) == str(studio_id) and match.group(2) == str(node["id"]), (
            f"the key {output['object_key']} does not carry studio {studio_id} and node {node['id']}"
        )
        assert match.group(4) == "png", f"an image output was stored as {match.group(4)}"
        assert store.exists(output["object_key"]), f"no object exists at {output['object_key']}"
        runs = [e for e in client.get("/v1/credits").json()["entries"] if e.get("kind") == "run"]
        assert len(runs) == 1 and runs[0].get("amount") == -144, f"run entries are {runs}"
        row = backend.one("asset", object_key=output["object_key"])
        assert row is not None and row.get("sha256") == match.group(3), (
            f"the asset row for {output['object_key']} is {row}"
        )
        detail = client.get(f"/v1/canvases/{canvas['id']}").json()
        assert detail["nodes"][0].get("latest_output", {}).get("object_key") == output["object_key"], (
            "the node does not point at its new output"
        )
        again = fx.succeeded_run(client, canvas["id"], node["id"])
        assert again.get("id") != run.get("id") and again.get("credits_charged") == 144, (
            f"running a current node again returned {again}"
        )
        assert fx.balance(client) == fx.TRIAL_CREDITS - 288, f"balance is {fx.balance(client)}"
        assert (again.get("output") or {}).get("object_key") == output["object_key"], (
            "identical bytes from a second run landed at a new key"
        )


def test_run_is_refused_while_an_upstream_node_is_stale():
    """A node runs only when everything wired into it has a current output."""
    with fx.fresh_creator() as client:
        canvas, nodes = fx.chain(client, 2, model_slug="quill-3-mini")
        early = fx.run_node(client, canvas["id"], nodes[1]["id"])
        assert fx.refused(early) and fx.error_code(early) == "conflict", (
            f"running a node with no upstream output returned {early.status_code}"
        )
        fx.run_chain(client, canvas, nodes)
        edit = client.patch(f"/v1/canvases/{canvas['id']}/nodes/{nodes[0]['id']}",
                            json={"prompt": "a new opening", "revision": nodes[0]["revision"]})
        assert edit.status_code == 200
        before = fx.balance(client)
        blocked = fx.run_node(client, canvas["id"], nodes[1]["id"])
        assert fx.refused(blocked) and fx.error_code(blocked) == "conflict", (
            f"running below a stale node returned {blocked.status_code}: {blocked.text[:200]}"
        )
        assert fx.balance(client) == before, "a refused run was charged"
        fx.succeeded_run(client, canvas["id"], nodes[0]["id"])
        cleared = {n["id"]: n["is_stale"] for n in client.get(f"/v1/canvases/{canvas['id']}").json()["nodes"]}
        assert cleared[nodes[0]["id"]] is False, "a successful run left the node stale"


def test_replayed_run_key_charges_once(backend):
    """Repeating a run with the same key returns the first run and charges once."""
    with fx.fresh_creator() as client:
        canvas = fx.new_canvas(client)
        node = fx.add_node(client, canvas["id"], model_slug="grain-4-turbo", aspect_ratio="16:9")
        key = fx.idem_key()
        first = fx.succeeded_run(client, canvas["id"], node["id"], key)
        second = fx.succeeded_run(client, canvas["id"], node["id"], key)
        assert first.get("id") == second.get("id"), "a replayed key produced a second run"
        assert fx.balance(client) == fx.TRIAL_CREDITS - 72, f"balance is {fx.balance(client)}"
        assert backend.count("generation_run", node_id=node["id"]) == 1, (
            "the store holds more than one run for a replayed key"
        )
        bare = client.post(f"/v1/canvases/{canvas['id']}/nodes/{node['id']}/runs")
        assert fx.refused(bare) and fx.error_code(bare) == "invalid_request", (
            f"a run without an Idempotency-Key returned {bare.status_code}"
        )
        assert fx.balance(client) == fx.TRIAL_CREDITS - 72, "a run without a key was charged"


def test_run_without_enough_credits_is_refused_and_writes_nothing(store, backend):
    """A run the balance cannot cover is refused and leaves no run or object."""
    with fx.fresh_creator() as client:
        canvas = fx.new_canvas(client)
        node = fx.add_node(client, canvas["id"], model_slug="reel-2-5", aspect_ratio="16:9")
        response = fx.run_node(client, canvas["id"], node["id"])
        assert fx.refused(response) and fx.error_code(response) == "insufficient_credits", (
            f"a 1000-credit run on 500 credits returned {response.status_code}: {response.text[:200]}"
        )
        assert fx.balance(client) == fx.TRIAL_CREDITS, "a refused run changed the balance"
        assert backend.count("generation_run", node_id=node["id"]) == 0, "a refused run was stored"
        studio_id = fx.workspace(client)["id"]
        assert store.list(f"outputs/{studio_id}/{node['id']}/") == [], "a refused run stored an object"


def test_concurrent_runs_for_the_last_credits_admit_exactly_one():
    """Two runs racing for credits that cover one: exactly one succeeds."""
    with fx.fresh_creator() as client:
        canvas = fx.new_canvas(client)
        for index in range(5):
            node = fx.add_node(client, canvas["id"], title=f"Drain {index}",
                               model_slug="grain-4-turbo", aspect_ratio="16:9")
            fx.succeeded_run(client, canvas["id"], node["id"])
        assert fx.balance(client) == 140, f"balance after five runs is {fx.balance(client)}"
        racer_a = fx.add_node(client, canvas["id"], title="Racer A",
                              model_slug="grain-4-turbo", aspect_ratio="16:9")
        racer_b = fx.add_node(client, canvas["id"], title="Racer B",
                              model_slug="grain-4-turbo", aspect_ratio="16:9")
        results = fx.at_the_same_moment(
            lambda: fx.run_node(client, canvas["id"], racer_a["id"]),
            lambda: fx.run_node(client, canvas["id"], racer_b["id"]),
        )
        wins = [r for r in results if r.status_code in (200, 201)
                and r.json().get("status") == "succeeded"]
        losses = [r for r in results if fx.refused(r)]
        assert len(wins) == 1 and len(losses) == 1, (
            f"racing runs returned {[r.status_code for r in results]}"
        )
        assert fx.error_code(losses[0]) == "insufficient_credits", losses[0].text[:200]
        assert fx.balance(client) == 68, f"balance after the race is {fx.balance(client)}"


def test_degraded_model_run_fails_and_charges_nothing():
    """A run on a degraded model fails at once without a charge or an output."""
    with fx.fresh_creator() as client:
        canvas = fx.new_canvas(client)
        node = fx.add_node(client, canvas["id"], model_slug="lumen-preview", aspect_ratio="4:5")
        response = fx.run_node(client, canvas["id"], node["id"])
        assert response.status_code in (200, 201), (
            f"a degraded run returned {response.status_code}: {response.text[:200]}"
        )
        run = response.json()
        assert run.get("status") == "failed" and run.get("credits_charged") == 0, f"run is {run}"
        assert not run.get("output"), f"a failed run carries an output: {run.get('output')}"
        assert fx.balance(client) == fx.TRIAL_CREDITS, "a failed run was charged"


def test_rerun_regenerates_stale_nodes_in_rank_order():
    """A rerun runs only the stale nodes, in rank order, and charges only for them."""
    with fx.fresh_creator() as client:
        canvas, nodes = fx.chain(client, 5, model_slug="quill-3-mini")
        runs = fx.run_chain(client, canvas, nodes)
        first_output = runs[0]["output"]["object_key"]
        client.patch(f"/v1/canvases/{canvas['id']}/nodes/{nodes[1]['id']}",
                     json={"prompt": "a different second line", "revision": nodes[1]["revision"]})
        before = fx.balance(client)
        response = client.post(f"/v1/canvases/{canvas['id']}/rerun",
                               headers=fx.with_headers(client, **{"Idempotency-Key": fx.idem_key()}))
        assert response.status_code in (200, 201), (
            f"the rerun returned {response.status_code}: {response.text[:300]}"
        )
        body = response.json()
        assert body.get("order") == [n["id"] for n in nodes[1:]], f"rerun order is {body.get('order')}"
        assert body.get("credits_charged") == 16, f"the rerun charged {body.get('credits_charged')}"
        assert fx.balance(client) == before - 16, f"balance moved to {fx.balance(client)}"
        detail = client.get(f"/v1/canvases/{canvas['id']}").json()
        assert not any(n["is_stale"] for n in detail["nodes"]), "nodes remain stale after the rerun"
        head = [n for n in detail["nodes"] if n["id"] == nodes[0]["id"]][0]
        assert head["latest_output"]["object_key"] == first_output, "rank one was run again"


def test_rerun_without_enough_credits_is_refused_before_any_node_runs():
    """A rerun the balance cannot cover is refused whole."""
    with fx.fresh_creator() as client:
        canvas = fx.new_canvas(client)
        nodes = []
        for index in range(5):
            node = fx.add_node(client, canvas["id"], title=f"Still {index}",
                               model_slug="grain-4-turbo", aspect_ratio="16:9")
            fx.succeeded_run(client, canvas["id"], node["id"])
            nodes.append(node)
        for node in nodes[:2]:
            edit = client.patch(f"/v1/canvases/{canvas['id']}/nodes/{node['id']}",
                                json={"prompt": f"a new still {fx.unique_suffix()}",
                                      "revision": node["revision"]})
            assert edit.status_code == 200, f"editing {node['title']} returned {edit.status_code}"
        before = fx.balance(client)
        assert before == 140, f"balance before the rerun is {before}"
        response = client.post(f"/v1/canvases/{canvas['id']}/rerun",
                               headers=fx.with_headers(client, **{"Idempotency-Key": fx.idem_key()}))
        assert fx.refused(response) and fx.error_code(response) == "insufficient_credits", (
            f"a 144-credit rerun on {before} credits returned {response.status_code}"
        )
        assert fx.balance(client) == before, "a refused rerun charged something"
        detail = client.get(f"/v1/canvases/{canvas['id']}").json()
        assert sum(1 for n in detail["nodes"] if n["is_stale"]) == 2, "a refused rerun cleared a stale node"


def test_generated_image_is_a_png_at_the_node_aspect(owner):
    """An image output is a PNG whose shape matches the node aspect."""
    canvas = fx.new_canvas(owner, "Probe aspects")
    for aspect in ("4:5", "16:9", "1:1"):
        node = fx.add_node(owner, canvas["id"], title=f"Still {aspect}", model_slug="folio-2",
                           aspect_ratio=aspect)
        run = fx.succeeded_run(owner, canvas["id"], node["id"])
        response = fx.fetch_output(owner, run["output"]["asset_id"])
        assert response.status_code == 200, f"streaming the {aspect} still returned {response.status_code}"
        assert response.headers.get("content-type", "").startswith("image/png"), (
            f"the {aspect} still streamed as {response.headers.get('content-type')}"
        )
        width, height = fx.png_size(response.content)
        assert abs(width / height - fx.ratio_of(aspect)) < 0.02, (
            f"a {aspect} still is {width} by {height}"
        )


def test_generated_outputs_are_deterministic_for_identical_inputs(owner):
    """Identical inputs give identical bytes and a changed prompt gives different bytes."""
    canvas = fx.new_canvas(owner, "Probe determinism")
    prompt = f"a lemon on marble {fx.unique_suffix()}"
    left = fx.add_node(owner, canvas["id"], title="Left", prompt=prompt, model_slug="atlas-image-1")
    right = fx.add_node(owner, canvas["id"], title="Right", prompt=prompt, model_slug="atlas-image-1")
    other = fx.add_node(owner, canvas["id"], title="Other", prompt=prompt + " at dusk",
                        model_slug="atlas-image-1")
    digests = [fx.succeeded_run(owner, canvas["id"], n["id"])["output"]["sha256"]
               for n in (left, right, other)]
    assert digests[0] == digests[1], f"identical inputs produced {digests[0]} and {digests[1]}"
    assert digests[0] != digests[2], "a changed prompt produced the same bytes"


def test_generated_video_audio_and_text_have_their_formats(owner):
    """Video is an animated SVG loop, audio a short WAV, text quotes its prompt."""
    canvas = fx.new_canvas(owner, "Probe formats")
    prompt = f"a wave of citrus {fx.unique_suffix()}"
    video = fx.add_node(owner, canvas["id"], title="Clip", prompt=prompt,
                        model_slug="strata-video-2", aspect_ratio="16:9")
    audio = fx.add_node(owner, canvas["id"], title="Sting", prompt=prompt,
                        model_slug="echo-voice-3", aspect_ratio=None)
    text = fx.add_node(owner, canvas["id"], title="Line", prompt=prompt,
                       model_slug="parley-2", aspect_ratio=None)
    clip = fx.fetch_output(owner, fx.succeeded_run(owner, canvas["id"], video["id"])["output"]["asset_id"])
    assert clip.headers.get("content-type", "").startswith("image/svg+xml"), (
        f"video streamed as {clip.headers.get('content-type')}"
    )
    assert "<svg" in clip.text and re.search(r"\b(4s|4000ms)\b", clip.text), (
        f"the video output is not a four-second SVG loop: {clip.text[:200]}"
    )
    sound = fx.fetch_output(owner, fx.succeeded_run(owner, canvas["id"], audio["id"])["output"]["asset_id"])
    assert sound.headers.get("content-type", "").startswith(("audio/wav", "audio/x-wav", "audio/wave")), (
        f"audio streamed as {sound.headers.get('content-type')}"
    )
    payload = sound.content
    assert payload[:4] == b"RIFF" and payload[8:12] == b"WAVE", "the audio output is not a WAV file"
    byte_rate = struct.unpack("<I", payload[28:32])[0]
    data_at = payload.find(b"data")
    data_size = struct.unpack("<I", payload[data_at + 4:data_at + 8])[0]
    assert 1.5 <= data_size / byte_rate <= 2.5, f"the audio lasts {data_size / byte_rate} seconds"
    words = fx.fetch_output(owner, fx.succeeded_run(owner, canvas["id"], text["id"])["output"]["asset_id"])
    assert words.headers.get("content-type", "").startswith("text/plain"), (
        f"text streamed as {words.headers.get('content-type')}"
    )
    assert prompt in words.text, f"the text output does not quote its prompt: {words.text[:200]}"


def test_output_bytes_are_stored_in_the_bucket_at_the_scheme_key(citrus, store, backend):
    """Every seeded Citrus Launch output exists in the bucket at its scheme key."""
    for node in citrus["nodes"]:
        output = node["latest_output"]
        match = fx.OBJECT_KEY_RE.match(output["object_key"])
        assert match and match.group(2) == str(node["id"]), (
            f"node {node['node_key']} has key {output['object_key']}"
        )
        assert store.exists(output["object_key"]), f"no object at {output['object_key']}"
        assert output["sha256"] == match.group(3), f"sha mismatch on {output['object_key']}"
        assert backend.count("asset", object_key=output["object_key"]) == 1, (
            f"the asset row for {output['object_key']} is missing or duplicated"
        )


def test_output_is_streamed_back_unchanged_with_its_content_type(citrus, owner):
    """The streamed bytes hash to the digest in the object key."""
    for key in ("pack-shot", "tagline", "jingle", "movie-cut-1"):
        output = fx.node_by_key(citrus, key)["latest_output"]
        response = fx.fetch_output(owner, output["asset_id"])
        assert response.status_code == 200, f"streaming {key} returned {response.status_code}"
        assert fx.digest(response.content) == output["sha256"], (
            f"the streamed bytes for {key} do not match {output['sha256']}"
        )
        assert response.headers.get("content-type", "").split(";")[0] == output["content_type"].split(";")[0], (
            f"{key} streamed as {response.headers.get('content-type')}, stored as {output['content_type']}"
        )
        assert len(response.content) == output["byte_size"], f"{key} byte size differs"


def test_identical_output_reuses_one_object_and_one_row(owner, store, backend):
    """Running one node twice with unchanged inputs reuses its single output."""
    canvas = fx.new_canvas(owner, "Probe reuse")
    node = fx.add_node(owner, canvas["id"], model_slug="tessera-0-9", aspect_ratio="1:1")
    first = fx.succeeded_run(owner, canvas["id"], node["id"])
    second = fx.succeeded_run(owner, canvas["id"], node["id"])
    assert first["output"]["asset_id"] == second["output"]["asset_id"], "a second output row was written"
    studio_id = fx.workspace(owner)["id"]
    keys = store.list(f"outputs/{studio_id}/{node['id']}/")
    assert keys == [first["output"]["object_key"]], f"objects under the node prefix are {keys}"
    assert backend.count("asset", object_key=first["output"]["object_key"]) == 1


def test_api_never_issues_a_link_into_the_bucket(citrus, owner, client_user):
    """No response hands out a storage address or a signed link."""
    bodies = [owner.get(f"/v1/canvases/{citrus['id']}").text,
              client_user.get("/v1/deliveries").text,
              owner.get("/v1/deliveries").text]
    storage_host = fx.storage_host()
    for body in bodies:
        assert "X-Amz-Signature" not in body and "X-Amz-Credential" not in body, (
            f"a response carries a signed storage link: {body[:300]}"
        )
        assert storage_host not in body, f"a response names the storage host: {body[:300]}"


def test_other_studio_creator_is_denied_the_output(citrus, second_studio, store):
    """A creator from another studio cannot stream an output or learn about it."""
    output = fx.node_by_key(citrus, "ooh-billboard")["latest_output"]
    response = fx.fetch_output(second_studio, output["asset_id"])
    assert response.status_code in (403, 404), (
        f"Saltmarsh Cut streamed a Northlight output with {response.status_code}"
    )
    assert fx.digest(response.content) != output["sha256"], "the refusal carried the bytes"
    assert store.exists(output["object_key"]), "the refusal disturbed the stored object"


def test_anonymous_caller_is_denied_the_output(citrus, guest):
    """A caller with no token cannot stream an output."""
    output = fx.node_by_key(citrus, "product-mockup")["latest_output"]
    response = fx.fetch_output(guest, output["asset_id"])
    assert response.status_code in (401, 403, 404), (
        f"an anonymous caller streamed an output with {response.status_code}"
    )
    assert fx.digest(response.content) != output["sha256"], "the refusal carried the bytes"


def test_client_is_denied_an_undelivered_output(citrus, client_user):
    """A client cannot stream an output that was never delivered to them."""
    output = fx.node_by_key(citrus, "studio-shot")["latest_output"]
    response = fx.fetch_output(client_user, output["asset_id"])
    assert response.status_code in (403, 404), (
        f"the client streamed an undelivered output with {response.status_code}"
    )


def test_client_reads_a_delivered_output(citrus, owner, client_user):
    """Delivering an output lets the addressed client stream it."""
    output = fx.node_by_key(citrus, "pack-shot")["latest_output"]
    delivery = fx.create_delivery(owner, output["asset_id"], fx.CLIENT_EMAIL)
    listed = fx.listed(client_user.get("/v1/deliveries"))
    assert any(d.get("id") == delivery["id"] for d in listed), "the client does not see the delivery"
    response = fx.fetch_output(client_user, output["asset_id"])
    assert response.status_code == 200 and fx.digest(response.content) == output["sha256"], (
        f"the client could not stream a delivered output: {response.status_code}"
    )
    owner.post(f"/v1/deliveries/{delivery['id']}/revoke")


def test_revoked_delivery_denies_the_client(owner, client_user, backend):
    """Revoking a delivery ends the client's access and hides the delivery."""
    canvas = fx.new_canvas(owner, "Probe revoke")
    node = fx.add_node(owner, canvas["id"], model_slug="halcyon-2-1")
    output = fx.succeeded_run(owner, canvas["id"], node["id"])["output"]
    delivery = fx.create_delivery(owner, output["asset_id"], fx.CLIENT_EMAIL)
    assert fx.fetch_output(client_user, output["asset_id"]).status_code == 200
    revoked = owner.post(f"/v1/deliveries/{delivery['id']}/revoke")
    assert revoked.status_code == 200 and revoked.json().get("state") == "revoked", (
        f"revoking returned {revoked.status_code}: {revoked.text[:200]}"
    )
    again = owner.post(f"/v1/deliveries/{delivery['id']}/revoke")
    assert again.status_code == 200 and again.json().get("state") == "revoked", "a second revoke changed state"
    response = fx.fetch_output(client_user, output["asset_id"])
    assert response.status_code in (403, 404), (
        f"the client streamed a revoked output with {response.status_code}"
    )
    ids = [d.get("id") for d in fx.listed(client_user.get("/v1/deliveries"))]
    assert delivery["id"] not in ids, "the revoked delivery is still listed for the client"
    row = backend.one("delivery", id=delivery["id"])
    assert row is not None and row.get("state") == "revoked" and row.get("revoked_at"), (
        f"the stored delivery reads {row}"
    )


def test_member_reads_the_studio_output(citrus, member):
    """A member of the studio streams its outputs."""
    output = fx.node_by_key(citrus, "lifestyle-scene")["latest_output"]
    response = fx.fetch_output(member, output["asset_id"])
    assert response.status_code == 200 and fx.digest(response.content) == output["sha256"], (
        f"the member could not stream the studio output: {response.status_code}"
    )


def test_client_is_denied_creator_endpoints(client_user, citrus, backend):
    """A client cannot create a canvas, run a node, run the bench, subscribe or buy credits."""
    before = backend.count("canvas")
    attempts = {
        "create a canvas": client_user.post("/v1/canvases", json={"name": "Client canvas"}),
        "claim a role": client_user.post("/v1/canvases", json={"name": "Role canvas",
                                                               "role": "creator"}),
        "run a node": fx.run_node(client_user, citrus["id"], citrus["nodes"][0]["id"]),
        "run the bench": fx.start_bench(client_user, ["halcyon-2-1", "vesper-3"]),
        "subscribe": fx.subscribe(client_user, "creator", "monthly"),
        "buy credits": fx.buy_packs(client_user, 1),
        "invite": client_user.post("/v1/workspace/invitations", json={"email": fx.probe_email()}),
    }
    for action, response in attempts.items():
        assert response.status_code in (401, 403, 404), (
            f"a client tried to {action} and received {response.status_code}: {response.text[:200]}"
        )
    assert backend.count("canvas") == before, "a client request created a canvas"


def test_member_cannot_subscribe_buy_packs_or_invite(member, owner):
    """A member is denied every owner-only write and nothing changes."""
    before = fx.workspace(owner)
    ledger = len(fx.listed(owner.get("/v1/billing-events")))
    for action, response in (
            ("subscribe", fx.subscribe(member, "growth", "monthly")),
            ("buy packs", fx.buy_packs(member, 1)),
            ("invite", member.post("/v1/workspace/invitations", json={"email": fx.probe_email()}))):
        assert response.status_code == 403 and fx.error_code(response) == "forbidden", (
            f"a member tried to {action} and received {response.status_code}: {response.text[:200]}"
        )
    after = fx.workspace(owner)
    assert after["plan_code"] == before["plan_code"] == "professional", "a member changed the plan"
    assert len(fx.listed(owner.get("/v1/billing-events"))) == ledger, "a member write was billed"


def test_other_studio_creator_cannot_open_or_edit_the_canvas(citrus, second_studio, owner):
    """A creator from another studio cannot read, edit, wire or run a canvas."""
    node = citrus["nodes"][0]
    base = f"/v1/canvases/{citrus['id']}"
    for action, response in (
            ("read", second_studio.get(base)),
            ("edit", second_studio.patch(f"{base}/nodes/{node['id']}",
                                         json={"prompt": "hijacked", "revision": node["revision"]})),
            ("wire", fx.wire(second_studio, citrus["id"], citrus["nodes"][0]["id"],
                             citrus["nodes"][1]["id"])),
            ("run", fx.run_node(second_studio, citrus["id"], node["id"]))):
        assert response.status_code in (403, 404), (
            f"Saltmarsh Cut tried to {action} Citrus Launch and received {response.status_code}"
        )
        assert fx.CITRUS_LAUNCH not in response.text, f"the {action} refusal discloses the canvas"
    after = fx.node_by_key(owner.get(base).json(), node["node_key"])
    assert after["prompt"] == node["prompt"] and after["revision"] == node["revision"], (
        "a refused edit changed the node"
    )
    names = [c.get("name") for c in fx.canvases(second_studio)]
    assert fx.CITRUS_LAUNCH not in names and fx.TRAILER_CUT in names, (
        f"Saltmarsh Cut lists canvases {names}"
    )


def test_other_studio_creator_cannot_deliver_or_revoke(citrus, second_studio, owner):
    """Another studio cannot deliver a Northlight output or revoke its delivery."""
    output = fx.node_by_key(citrus, "jingle")["latest_output"]
    response = second_studio.post("/v1/deliveries", json={
        "asset_id": output["asset_id"], "client_email": fx.probe_email(), "note": "stolen"})
    assert response.status_code in (403, 404) and fx.error_code(response) in ("not_found", "forbidden"), (
        f"Saltmarsh Cut delivered a Northlight output with {response.status_code}"
    )
    seeded = [d for d in fx.listed(owner.get("/v1/deliveries"))
              if d.get("note") == fx.SEEDED_DELIVERY_NOTE]
    assert seeded, "the seeded delivery is missing from the Northlight list"
    revoke = second_studio.post(f"/v1/deliveries/{seeded[0]['id']}/revoke")
    assert revoke.status_code in (403, 404), f"Saltmarsh Cut revoked with {revoke.status_code}"
    still = [d for d in fx.listed(owner.get("/v1/deliveries")) if d.get("id") == seeded[0]["id"]]
    assert still and still[0].get("state") == "delivered", "the refused revoke changed the delivery"
    theirs = [d.get("id") for d in fx.listed(second_studio.get("/v1/deliveries"))]
    assert seeded[0]["id"] not in theirs, "Saltmarsh Cut lists a Northlight delivery"


def test_membership_in_the_request_body_is_ignored(second_studio, owner):
    """A studio or membership named in a body grants nothing."""
    northlight_id = fx.workspace(owner)["id"]
    name = f"Smuggled {fx.unique_suffix()}"
    second_studio.post("/v1/canvases", json={
        "name": name, "workspace_id": northlight_id, "membership": "owner"})
    assert name not in [c.get("name") for c in fx.canvases(owner)], (
        "a workspace_id in the body placed a canvas in another studio"
    )
    invite = second_studio.post("/v1/workspace/invitations", json={
        "email": fx.probe_email(), "workspace_id": northlight_id})
    assert fx.refused(invite) and fx.error_code(invite) == "limit_reached", (
        f"a body naming Northlight let a one-seat studio invite: {invite.status_code}"
    )
    assert fx.workspace(owner)["plan_code"] == "professional"


def test_delivery_is_created_and_listed_for_the_studio(citrus, owner, member):
    """A delivery records its fields and every studio creator sees it."""
    output = fx.node_by_key(citrus, "tagline")["latest_output"]
    email = fx.probe_email()
    delivery = fx.create_delivery(member, output["asset_id"], email, note="Tagline for review")
    assert {"id", "asset_id", "client_email", "note", "state", "created_at"} <= set(delivery), (
        f"a delivery lacks the pinned fields: {delivery}"
    )
    assert delivery["client_email"] == email and delivery["note"] == "Tagline for review"
    listing = fx.listed(owner.get("/v1/deliveries"))
    assert any(d.get("id") == delivery["id"] for d in listing), "the owner does not see a member's delivery"
    bad = owner.post("/v1/deliveries", json={"asset_id": output["asset_id"],
                                             "client_email": "not-an-address", "note": "x"})
    assert fx.refused(bad) and fx.error_code(bad) == "invalid_request", (
        f"a malformed client address returned {bad.status_code}"
    )
    long_note = owner.post("/v1/deliveries", json={"asset_id": output["asset_id"],
                                                   "client_email": email, "note": "n" * 201})
    assert fx.refused(long_note), f"a 201-character note returned {long_note.status_code}"


def test_client_lists_only_their_own_live_deliveries(citrus, owner):
    """A client sees only the live deliveries addressed to them, with the studio name."""
    output = fx.node_by_key(citrus, "studio-shot")["latest_output"]
    email, token, _ = fx.sign_up("client", "Later Client")
    mine = fx.create_delivery(owner, output["asset_id"], email, note="For the later client")
    fx.create_delivery(owner, output["asset_id"], fx.probe_email(), note="For someone else")
    with appclient.client(token) as client:
        listing = fx.listed(client.get("/v1/deliveries"))
        assert [d.get("id") for d in listing] == [mine["id"]], f"the client lists {listing}"
        assert listing[0].get("studio_name") == fx.NORTHLIGHT, (
            f"the delivery names studio {listing[0].get('studio_name')!r}"
        )
        assert listing[0].get("client_email") == email


def test_seeded_delivery_is_readable_by_the_client(client_user, citrus):
    """The seeded billboard delivery is listed and streamable for the client."""
    listing = fx.listed(client_user.get("/v1/deliveries"))
    seeded = [d for d in listing if d.get("note") == fx.SEEDED_DELIVERY_NOTE]
    assert seeded, f"the client does not see the seeded delivery: {listing}"
    billboard = fx.node_by_key(citrus, "ooh-billboard")["latest_output"]
    assert seeded[0].get("asset_id") == billboard["asset_id"], "the seeded delivery is not the billboard"
    assert seeded[0].get("state") == "delivered" and seeded[0].get("studio_name") == fx.NORTHLIGHT
    response = fx.fetch_output(client_user, billboard["asset_id"])
    assert response.status_code == 200 and fx.digest(response.content) == billboard["sha256"]


def test_models_manifest_lists_the_twenty_two_models_in_order():
    """The manifest lists the pinned models in manifest order."""
    models = fx.listed(httpx.get(f"{fx.api_base()}/v1/models", timeout=fx.TIMEOUT))
    rows = [(m.get("slug"), m.get("display_name"), m.get("vendor"), m.get("output_kind"),
             m.get("latency_band"), m.get("availability")) for m in models]
    assert rows == list(fx.MODELS), f"the manifest reads {rows}"


def test_manifest_fields_and_credit_costs_follow_the_current_rates():
    """Every model carries its aspects, limits, gradient and current costs."""
    models = fx.listed(httpx.get(f"{fx.api_base()}/v1/models", timeout=fx.TIMEOUT))
    rates = fx.RATES[fx.CURRENT_RATE_VERSION]
    for model in models:
        kind = model["output_kind"]
        assert model.get("aspect_ratios") == fx.ASPECTS[kind], (
            f"{model['slug']} lists aspects {model.get('aspect_ratios')}"
        )
        cost = model.get("credit_cost") or {}
        assert cost.get("standard") == rates[(kind, "standard")], f"{model['slug']} cost is {cost}"
        assert cost.get("high") == rates[(kind, "high")], f"{model['slug']} cost is {cost}"
        assert len(model.get("gradient_stops") or []) in (6, 7), (
            f"{model['slug']} has {len(model.get('gradient_stops') or [])} gradient stops"
        )
        if kind == "image":
            assert model.get("max_dimensions") == fx.IMAGE_MAX_DIMENSIONS, model
            assert model.get("max_duration_seconds") is None, model
        if kind == "video":
            assert model.get("max_dimensions") == fx.VIDEO_MAX_DIMENSIONS, model
            assert model.get("max_duration_seconds") == 10, model
        if kind == "audio":
            assert model.get("max_duration_seconds") == 30, model
        if kind == "text":
            assert model.get("max_duration_seconds") is None, model


def test_every_model_page_answers_at_its_root_slug():
    """Each model has a page one segment deep at its slug."""
    failures = [(slug, fx.page_response(f"/{slug}").status_code) for slug in fx.MODEL_SLUGS
                if fx.page_response(f"/{slug}").status_code != 200]
    assert not failures, f"model pages that did not answer: {failures}"


def test_model_page_links_three_siblings_of_its_kind(page):
    """A model page names its kind and links at least three siblings of that kind."""
    for slug, kind, siblings in (("halcyon-2-1", "image", "image"),
                                 ("chorus-2", "audio", "audio")):
        page.goto(f"{fx.app_url()}/{slug}")
        expect(page.locator(f"[data-output-kind='{kind}']").first).to_be_attached()
        same_kind = {m[0] for m in fx.MODELS if m[3] == siblings and m[0] != slug}
        hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
        linked = {h.rstrip("/").rsplit("/", 1)[-1] for h in hrefs if h}
        assert len(linked & same_kind) >= 3, (
            f"/{slug} links only {sorted(linked & same_kind)} of its {kind} siblings"
        )
        expect(page.get_by_text("Try on the canvas").first).to_be_visible()
        expect(page.get_by_text("Compare on the bench").first).to_be_visible()
        assert page.locator("[data-sample]").count() >= 4, f"/{slug} shows fewer than four samples"
    for slug, runs in (("halcyon-2-1", 277), ("drift-1-6", 20), ("chorus-2", 500), ("lexicon-7", 5000)):
        page.goto(f"{fx.app_url()}/{slug}")
        expect(page.get_by_text(f"Creator buys {runs} standard runs a month").first).to_be_visible()
    page.goto(f"{fx.app_url()}/models")
    expect(page.get_by_text(fx.MODELS_HEADLINE).first).to_be_visible()
    roster = page.inner_text("body")
    for heading in ("Image", "Video", "Audio", "Text", "Let Ivo choose"):
        assert heading in roster, f"the roster does not show {heading!r}"


def test_plans_carry_prices_allowances_and_computed_yields():
    """The plan list carries the pinned prices, allowances, seats and yields."""
    plans = fx.listed(httpx.get(f"{fx.api_base()}/v1/plans", timeout=fx.TIMEOUT))
    assert [p.get("code") for p in plans] == list(fx.PLAN_CODES), f"plan order is {plans}"
    assert [p.get("display_name") for p in plans] == list(fx.PLAN_NAMES)
    assert [p.get("descriptor") for p in plans] == list(fx.PLAN_DESCRIPTORS)
    by_code = {p["code"]: p for p in plans}
    for code in ("free", "creator", "growth"):
        assert by_code[code].get("monthly_price_minor") == fx.MONTHLY_MINOR[code], by_code[code]
        assert by_code[code].get("annual_price_minor") == fx.ANNUAL_MINOR[code], by_code[code]
        assert by_code[code].get("credits") == fx.PLAN_CREDITS[code], by_code[code]
        assert by_code[code].get("seat_limit") == 1, by_code[code]
    for code, (images, videos) in fx.PLAN_YIELDS.items():
        assert (by_code[code].get("yield_images"), by_code[code].get("yield_videos")) == (images, videos), (
            f"{code} yields read {by_code[code]}"
        )
    options = {o.get("option"): o for o in by_code["professional"].get("credit_options", [])}
    for option, spec in fx.PROFESSIONAL_OPTIONS.items():
        got = options.get(option) or {}
        assert (got.get("credits"), got.get("monthly_price_minor"), got.get("annual_price_minor"),
                got.get("yield_images"), got.get("yield_videos")) == (
            spec["credits"], spec["monthly"], spec["annual"], spec["yield_images"], spec["yield_videos"]), (
            f"professional {option} reads {got}"
        )
    assert by_code["professional"].get("seat_limit") is None
    top = by_code["professional"]
    assert (top.get("credits"), top.get("monthly_price_minor"), top.get("annual_price_minor")) == (
        110000, 11000, 9300), f"professional top-level fields read {top}"
    assert by_code["enterprise"].get("seat_limit") is None
    for field in ("monthly_price_minor", "annual_price_minor", "credits", "yield_images", "yield_videos"):
        assert by_code["enterprise"].get(field) is None, f"enterprise {field} is {by_code['enterprise'].get(field)!r}"
    for field in ("yield_images", "yield_videos"):
        assert by_code["free"].get(field) is None, f"free {field} is {by_code['free'].get(field)!r}"


def test_rates_expose_the_current_and_the_retired_version():
    """The rate table is versioned with one current version."""
    for version, current in ((fx.CURRENT_RATE_VERSION, True), (fx.RETIRED_RATE_VERSION, False)):
        params = {} if current else {"version": version}
        body = httpx.get(f"{fx.api_base()}/v1/rates", params=params, timeout=fx.TIMEOUT).json()
        assert body.get("version") == version and body.get("current") is current, (
            f"the rate route for {version} reads {body}"
        )
        got = {(r["output_kind"], r["tier"]): r["credits"] for r in body.get("rates", [])}
        assert got == fx.RATES[version], f"rates for {version} are {got}"
    bad = httpx.get(f"{fx.api_base()}/v1/rates", params={"version": "1999-01"}, timeout=fx.TIMEOUT)
    assert fx.refused(bad), f"an unknown rate version returned {bad.status_code}"


def test_forecast_totals_and_recommendation_match_the_worked_examples():
    """The forecaster totals, recommends and prices the overflow as pinned."""
    cases = (
        ([("image", 400, "standard"), ("video", 30, "standard")], 58800,
         ("professional", "110k"), "growth", 9000),
        ([("image", 100, "standard")], 7200, ("creator", None), "free", 7000),
        ([("image", 3000, "high")], 432000, ("enterprise", None), "professional", 132000),
        ([("text", 10, "standard")], 40, ("free", None), None, 0),
    )
    for rows, total, (code, option), below, overflow in cases:
        response = fx.forecast(rows)
        assert response.status_code in (200, 201), f"forecasting {rows} returned {response.status_code}"
        body = response.json()
        assert body.get("total_credits") == total, f"{rows} totalled {body.get('total_credits')}"
        recommended = body.get("recommended_plan") or {}
        assert recommended.get("code") == code, f"{rows} recommended {recommended}"
        if option:
            assert recommended.get("credit_option") == option, f"{rows} recommended {recommended}"
        plan_below = body.get("plan_below")
        below_code = plan_below.get("code") if isinstance(plan_below, dict) else plan_below
        assert below_code == below, f"{rows} named {plan_below} below"
        assert body.get("overflow_cost_minor") == overflow, f"{rows} overflow {body.get('overflow_cost_minor')}"
        assert body.get("stale") is False, f"a current-version forecast is stale: {body}"
        again = httpx.get(f"{fx.api_base()}/v1/forecasts/{body['id']}", timeout=fx.TIMEOUT).json()
        assert again.get("total_credits") == total, "the stored forecast differs from the response"


def test_forecast_quantities_round_to_two_significant_figures():
    """Quantities round to two significant figures, half up."""
    for typed, rounded in ((437, 440), (1234, 1200), (1250, 1300), (5000, 5000), (10, 10)):
        body = fx.forecast([("text", typed, "standard")]).json()
        assert body["rows"][0]["monthly_quantity"] == rounded == fx.two_significant(typed), (
            f"{typed} rounded to {body['rows'][0]['monthly_quantity']}"
        )
        assert body["total_credits"] == rounded * 4, f"{typed} totalled {body['total_credits']}"


def test_forecast_with_invalid_rows_is_refused():
    """Seven rows, out-of-range quantities and unknown kinds are refused."""
    seven = [("image", 10, "standard")] * 7
    for rows in (seven, [("image", 9, "standard")], [("image", 5001, "standard")],
                 [("hologram", 10, "standard")], [("image", 10, "ultra")]):
        response = fx.forecast(rows)
        assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
            f"forecasting {rows[:1]} x{len(rows)} returned {response.status_code}"
        )
    bad_version = fx.forecast([("image", 10, "standard")], version="1999-01")
    assert fx.refused(bad_version), f"an unknown version returned {bad_version.status_code}"


def test_forecast_under_the_retired_version_is_stale_until_recomputed(page):
    """A forecast made under the retired rates stays stale until recomputed."""
    rows = [("image", 400, "standard"), ("video", 30, "standard")]
    body = fx.forecast(rows, version=fx.RETIRED_RATE_VERSION).json()
    assert body.get("stale") is True and body.get("total_credits") == 65000, f"retired forecast reads {body}"
    assert body.get("overflow_cost_minor") == 15000 and body.get("rate_version") == fx.RETIRED_RATE_VERSION
    stored = httpx.get(f"{fx.api_base()}/v1/forecasts/{body['id']}", timeout=fx.TIMEOUT).json()
    assert stored.get("stale") is True and stored.get("total_credits") == 65000, (
        f"reading the stale forecast recomputed it: {stored}"
    )
    page.goto(f"{fx.app_url()}/pricing?forecast={body['id']}")
    expect(page.get_by_role("button", name="Recompute").first).to_be_visible()
    glowing = page.eval_on_selector_all("[data-glow='on']", "els => els.map(e => e.getAttribute('data-plan'))")
    assert glowing == ["professional"], f"the stale forecast lights {glowing}"
    fresh = httpx.post(f"{fx.api_base()}/v1/forecasts/{body['id']}/recompute", timeout=fx.TIMEOUT)
    assert fresh.status_code in (200, 201), f"recompute returned {fresh.status_code}"
    fresh_body = fresh.json()
    assert fresh_body.get("stale") is False and fresh_body.get("total_credits") == 58800, fresh_body
    assert fresh_body.get("overflow_cost_minor") == 9000
    assert fresh_body.get("rate_version") == fx.CURRENT_RATE_VERSION


def test_pricing_page_carries_the_plan_hooks_and_one_glow(page):
    """The pricing route marks every plan card and exactly one glowing card."""
    page.goto(f"{fx.app_url()}/pricing")
    expect(page.locator("[data-plan]").first).to_be_attached()
    codes = page.eval_on_selector_all("[data-plan]", "els => els.map(e => e.getAttribute('data-plan'))")
    assert set(codes) >= set(fx.PLAN_CODES), f"plan cards declare {codes}"
    glowing = page.eval_on_selector_all("[data-glow='on']", "els => els.map(e => e.getAttribute('data-plan'))")
    assert glowing == ["professional"], f"cards glowing without a forecast: {glowing}"
    options = page.eval_on_selector_all("[data-credit-option]", "els => els.map(e => e.getAttribute('data-credit-option'))")
    assert options and set(options) <= {"110k", "300k"}, f"credit options declared: {options}"
    body = page.inner_text("body")
    for label in fx.PRICING_TEXT:
        assert label in body, f"the pricing route does not show {label!r}"


def test_billing_toggle_flips_the_billing_period(page):
    """The billing toggle moves the pricing root between monthly and annual."""
    page.goto(f"{fx.app_url()}/pricing")
    root = page.locator("[data-billing-period]").first
    expect(root).to_be_attached()
    expect(page.get_by_text(fx.SAVING_CHIP).first).to_be_visible()
    page.get_by_text("Annual", exact=True).first.click()
    expect(root).to_have_attribute("data-billing-period", "annual")
    assert "$17" in page.inner_text("body"), "annual mode does not show the Creator annual price"
    page.get_by_text("Monthly", exact=True).first.click()
    expect(root).to_have_attribute("data-billing-period", "monthly")


def test_replay_graphs_are_listed_with_the_advertising_shape():
    """The five graphs are listed in order and advertising has its pinned shape."""
    graphs = fx.replay_graphs()
    assert [g.get("key") for g in graphs] == list(fx.GRAPH_KEYS), f"graph order is {graphs}"
    assert [g.get("label") for g in graphs] == list(fx.GRAPH_LABELS)
    ad = graphs[0]
    assert ad.get("brief") == fx.ADVERTISING_BRIEF, f"the advertising brief reads {ad.get('brief')!r}"
    nodes = {n["key"]: n for n in ad["nodes"]}
    assert set(nodes) == set(fx.ADVERTISING_NODES)
    for key, (title, kind, model, aspect, rank, _inputs) in fx.ADVERTISING_NODES.items():
        got = nodes[key]
        assert (got.get("title"), got.get("output_kind"), got.get("model_slug"),
                got.get("aspect_ratio"), got.get("rank")) == (title, kind, model, aspect, rank), (
            f"advertising node {key} reads {got}"
        )
        assert got.get("default_prompt"), f"advertising node {key} has no default prompt"
    edges = {(e["from"], e["to"]) for e in ad["edges"]}
    assert edges == {(s, k) for k, spec in fx.ADVERTISING_NODES.items() for s in spec[5]}
    for key, titles in fx.OTHER_GRAPH_TITLES.items():
        got = [n.get("title") for n in fx.graph(key)["nodes"]]
        assert sorted(got) == sorted(titles), f"{key} titles are {got}"


def test_replay_graphs_are_acyclic_with_distinct_models():
    """Every graph is acyclic, at most twelve nodes, one model per node."""
    for g in fx.replay_graphs():
        nodes = g["nodes"]
        assert len(nodes) <= 12, f"{g['key']} has {len(nodes)} nodes"
        models = [n["model_slug"] for n in nodes]
        assert len(models) == len(set(models)), f"{g['key']} repeats a model: {models}"
        assert set(models) <= set(fx.MODEL_SLUGS), f"{g['key']} names unknown models"
        framed = [n.get("aspect_ratio") for n in nodes if n["output_kind"] in ("image", "video")]
        assert set(framed) <= {"4:5", "16:9"}, f"{g['key']} frames image or video nodes at {framed}"
        rank = {n["key"]: n["rank"] for n in nodes}
        for edge in g["edges"]:
            assert rank[edge["to"]] > rank[edge["from"]], f"{g['key']} edge {edge} is not forward"


def test_default_prompt_regeneration_is_served_from_the_cache():
    """The default prompt on the default model is a cache hit."""
    session = f"session-{fx.unique_suffix()}"
    node = [n for n in fx.graph("advertising")["nodes"] if n["key"] == "pack-shot"][0]
    response = fx.regenerate(session, "pack-shot", node["default_prompt"], 1)
    assert response.status_code == 200, f"regenerate returned {response.status_code}: {response.text[:200]}"
    body = response.json()
    assert body.get("source") == "cache" and body.get("nearby") is False, f"default regenerate reads {body}"
    assert body.get("rate_limited") is False and body.get("generation_token") == 1
    assert body.get("node_key") == "pack-shot" and body.get("preview_url"), body
    preview = httpx.get(fx.absolute(body["preview_url"]), timeout=fx.TIMEOUT)
    assert preview.status_code == 200, f"the preview address returned {preview.status_code}"


def test_edited_prompt_regeneration_falls_back_to_a_curated_variant():
    """An edited prompt is served from the curated set, deterministically."""
    prompt = f"a pack shot on wet slate {fx.unique_suffix()}"
    first = fx.regenerate(f"session-{fx.unique_suffix()}", "pack-shot", prompt, 1).json()
    second = fx.regenerate(f"session-{fx.unique_suffix()}", "pack-shot", prompt, 1).json()
    assert first.get("source") == "curated" and first.get("nearby") is True, f"edited regenerate reads {first}"
    assert first.get("preview_url") == second.get("preview_url"), (
        "the same prompt chose different curated variants"
    )


def test_lower_generation_token_is_refused_as_stale():
    """Tokens only move forward for a session and node."""
    session = f"session-{fx.unique_suffix()}"
    prompt = "a billboard at dusk"
    accepted = fx.regenerate(session, "ooh-billboard", prompt, 5)
    assert accepted.status_code == 200, accepted.text[:200]
    older = fx.regenerate(session, "ooh-billboard", prompt, 3)
    assert fx.refused(older) and fx.error_code(older) == "stale_generation", (
        f"an older token returned {older.status_code}: {older.text[:200]}"
    )
    assert "preview_url" not in older.json(), "a stale refusal returned a result"
    repeat = fx.regenerate(session, "ooh-billboard", prompt, 5)
    assert repeat.status_code == 200 and repeat.json().get("preview_url") == accepted.json().get("preview_url")
    other_node = fx.regenerate(session, "jingle", "a short citrus jingle", 1)
    assert other_node.status_code == 200, "a token on one node blocked another node"


def test_replay_rate_limit_degrades_instead_of_failing():
    """Past the per-session limit a rerun still succeeds, curated and marked."""
    session = f"session-{fx.unique_suffix()}"
    node = [n for n in fx.graph("advertising")["nodes"] if n["key"] == "tagline"][0]
    last = None
    for token in range(1, fx.REPLAY_SESSION_LIMIT + 2):
        last = fx.regenerate(session, "tagline", node["default_prompt"], token)
        assert last.status_code == 200, f"rerun {token} returned {last.status_code}"
    body = last.json()
    assert body.get("rate_limited") is True and body.get("source") == "curated", (
        f"rerun {fx.REPLAY_SESSION_LIMIT + 1} reads {body}"
    )


def test_regeneration_with_a_model_of_another_kind_is_refused():
    """A replay node cannot be rerouted to a model of another output kind."""
    response = fx.regenerate(f"session-{fx.unique_suffix()}", "pack-shot", "a pack shot", 1,
                             model_slug="chorus-2")
    assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
        f"rerouting an image node to audio returned {response.status_code}"
    )


def test_replay_session_claim_creates_the_first_canvas_once(backend):
    """Claiming a replay session creates My first canvas once, with the overrides."""
    with fx.fresh_creator() as client:
        session = f"session-{fx.unique_suffix()}"
        payload = {"session_id": session, "graph_key": "advertising",
                   "overrides": [{"node_key": "pack-shot", "prompt": "a pack shot on ice"}],
                   "stale_node_keys": ["pack-shot", "ooh-billboard", "movie-cut-1"]}
        first = client.post("/v1/replay/sessions/claim", json=payload)
        assert first.status_code in (200, 201), f"claim returned {first.status_code}: {first.text[:200]}"
        body = first.json()
        assert body.get("name") == fx.FIRST_CANVAS_NAME, f"the claimed canvas is {body}"
        second = client.post("/v1/replay/sessions/claim", json=payload)
        assert second.json().get("canvas_id") == body.get("canvas_id"), "a second claim made a new canvas"
        names = [c.get("name") for c in fx.canvases(client)]
        assert names.count(fx.FIRST_CANVAS_NAME) == 1, f"canvases after two claims: {names}"
        detail = client.get(f"/v1/canvases/{body['canvas_id']}").json()
        nodes = {n["node_key"]: n for n in detail["nodes"]}
        assert set(nodes) == set(fx.ADVERTISING_NODES) and len(detail["edges"]) == 8
        assert nodes["pack-shot"]["prompt"] == "a pack shot on ice"
        assert {k for k, n in nodes.items() if n["is_stale"]} == {"pack-shot", "ooh-billboard", "movie-cut-1"}
        assert nodes["movie-cut-1"]["model_slug"] == "kinetic-3-pro"
        assert all(n["tier"] == "standard" and n["revision"] == 1 for n in nodes.values()), (
            f"claimed nodes carry {[(n['tier'], n['revision']) for n in nodes.values()]}"
        )
        assert nodes["product-mockup"]["title"] == "Product Mockup"
        other = dict(payload, session_id=f"session-{fx.unique_suffix()}")
        third = client.post("/v1/replay/sessions/claim", json=other)
        assert third.status_code in (200, 201), f"a second session claim returned {third.status_code}"
        assert third.json().get("name") == f"{fx.FIRST_CANVAS_NAME} 2", (
            f"a second session was named {third.json().get('name')!r}"
        )


def test_replay_step_forward_reaches_the_last_rank(page):
    """Stepping the advertising graph reaches its fifth rank with eight nodes."""
    page.goto(f"{fx.app_url()}/")
    page.get_by_text("Advertising", exact=True).first.click()
    expect(page.locator("[data-graph-key='advertising']").first).to_be_attached()
    expect(page.get_by_text("Launch Fizzwell", exact=False).first).to_be_attached()
    for _ in range(6):
        page.get_by_role("button", name="Step forward").first.click()
    expect(page.get_by_text("Rank 5 of 5").first).to_be_visible()
    keys = page.eval_on_selector_all("[data-graph-key='advertising'] [data-node-key]",
                                     "els => els.map(e => e.getAttribute('data-node-key'))")
    assert set(keys) >= set(fx.ADVERTISING_NODES), f"the advertising graph renders {keys}"
    states = page.eval_on_selector_all("[data-graph-key='advertising'] [data-node-key]",
                                       "els => els.map(e => e.getAttribute('data-node-state'))")
    assert set(states) <= {"rest", "expanded", "stale", "regenerating"}, f"node states are {states}"
    for label in ("Play", "Step back"):
        expect(page.get_by_role("button", name=label).first).to_be_attached()


def test_bench_requires_a_creator_session(guest):
    """Starting a bench run needs a signed-in creator."""
    response = fx.start_bench(guest, ["halcyon-2-1", "vesper-3"])
    assert response.status_code == 401 and fx.error_code(response) == "unauthenticated", (
        f"an anonymous bench run returned {response.status_code}: {response.text[:200]}"
    )


def test_bench_run_rejects_a_fifth_or_duplicate_model():
    """Two to four distinct known models and a bounded brief are required."""
    with fx.fresh_creator() as client:
        for slugs, brief in ((["halcyon-2-1"], "a brief"),
                             (["halcyon-2-1", "vesper-3", "folio-2", "grain-4-turbo", "atlas-image-1"], "a brief"),
                             (["halcyon-2-1", "halcyon-2-1"], "a brief"),
                             (["halcyon-2-1", "not-a-model"], "a brief"),
                             (["halcyon-2-1", "vesper-3"], ""),
                             (["halcyon-2-1", "vesper-3"], "b" * 401)):
            response = fx.start_bench(client, slugs, brief=brief)
            assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
                f"a bench run with {len(slugs)} slugs and a {len(brief)}-character brief "
                f"returned {response.status_code}"
            )
        assert fx.balance(client) == fx.TRIAL_CREDITS, "a refused bench run was charged"
        costly = fx.start_bench(client, ["drift-1-6", "reel-2-5"])
        assert fx.refused(costly) and fx.error_code(costly) == "insufficient_credits", (
            f"a bench run costing more than the balance returned {costly.status_code}"
        )


def test_bench_frames_land_independently_and_charge_per_success():
    """Frames land on their own schedules and each success charges its rate."""
    with fx.fresh_creator() as client:
        response = fx.start_bench(client, ["prism-xl-1-5", "halcyon-2-1", "grain-4-turbo"])
        assert response.status_code in (200, 201), response.text[:300]
        run = response.json()
        assert run.get("status") == "running", f"a new run reads {run.get('status')}"
        assert [f.get("model_slug") for f in run.get("frames", [])] == [
            "prism-xl-1-5", "halcyon-2-1", "grain-4-turbo"], "frames are not in selection order"
        seen_split = False
        final = None
        deadline_polls = int(fx.SETTLE_LIMIT / fx.SETTLE_STEP)
        for _ in range(deadline_polls):
            current = client.get(f"/v1/bench/runs/{run['id']}").json()
            states = {f["model_slug"]: f["state"] for f in current["frames"]}
            if states["grain-4-turbo"] == "succeeded" and states["prism-xl-1-5"] == "running":
                seen_split = True
            if current.get("status") != "running":
                final = current
                break
            fx.settle()
        assert final is not None, "the bench run never finished"
        assert seen_split, "the fast frame was never reported before the slow frame finished"
        assert final.get("status") == "completed"
        assert all(f["state"] == "succeeded" and f["credits_charged"] == 72 for f in final["frames"])
        latency = {f["model_slug"]: f["latency_ms"] for f in final["frames"]}
        assert latency["grain-4-turbo"] < latency["prism-xl-1-5"], f"latencies are {latency}"
        assert all(f.get("preview_url") for f in final["frames"]), "a succeeded frame has no preview"
        assert fx.balance(client) == fx.TRIAL_CREDITS - 216, f"balance is {fx.balance(client)}"
        bench = [e for e in client.get("/v1/credits").json()["entries"] if e.get("kind") == "bench"]
        assert sum(e["amount"] for e in bench) == -216, f"bench entries are {bench}"


def test_bench_failed_frame_charges_nothing_and_run_completes():
    """One failed frame holds its place, says why and costs nothing."""
    with fx.fresh_creator() as client:
        run = fx.start_bench(client, ["halcyon-2-1", "vesper-3", "grain-4-turbo", "lumen-preview"]).json()
        final = fx.await_bench(client, run["id"])
        assert final.get("status") == "completed", f"the run reads {final.get('status')}"
        failed = fx.frame_for(final, "lumen-preview")
        assert failed.get("state") == "failed" and failed.get("credits_charged") == 0, failed
        assert failed.get("failure_reason") == fx.FAILING_ENGINE_REASON, failed
        assert [f["model_slug"] for f in final["frames"]][-1] == "lumen-preview", "the failed frame moved"
        assert fx.balance(client) == fx.TRIAL_CREDITS - 216, f"balance is {fx.balance(client)}"
        retry = client.post(f"/v1/bench/runs/{run['id']}/frames/lumen-preview/retry")
        assert retry.status_code in (200, 201), f"retrying the failed frame returned {retry.status_code}"
        assert fx.balance(client) == fx.TRIAL_CREDITS - 216, "a retry that failed again was charged"


def test_bench_two_failures_void_the_run_and_charge_nothing():
    """Two failed frames void the run and nothing is charged."""
    with fx.fresh_creator() as client:
        run = fx.start_bench(client, ["halcyon-2-1", "lumen-preview", "driftwood-beta"]).json()
        final = fx.await_bench(client, run["id"], limit=fx.BENCH_DEADLINE_LIMIT)
        assert final.get("status") == "voided", f"the run reads {final.get('status')}"
        assert fx.frame_for(final, "driftwood-beta").get("state") == "timed_out"
        assert all(f.get("credits_charged") == 0 for f in final["frames"]), final["frames"]
        assert fx.balance(client) == fx.TRIAL_CREDITS, "a voided run was charged"
        pick = client.post(f"/v1/bench/runs/{run['id']}/pick", json={"model_slug": "halcyon-2-1"})
        assert fx.refused(pick) and fx.error_code(pick) == "conflict", (
            f"picking on a voided run returned {pick.status_code}"
        )
        retry = client.post(f"/v1/bench/runs/{run['id']}/frames/lumen-preview/retry")
        assert fx.refused(retry) and fx.error_code(retry) == "conflict", (
            f"retrying a frame on a voided run returned {retry.status_code}"
        )


def test_bench_pick_requires_two_successes(second_studio):
    """A pick is recorded once on a completed run and only for a succeeded model."""
    with fx.fresh_creator() as client:
        run = fx.start_bench(client, ["grain-4-turbo", "vesper-3", "lumen-preview"]).json()
        fx.await_bench(client, run["id"])
        for response in (second_studio.get(f"/v1/bench/runs/{run['id']}"),
                         second_studio.post(f"/v1/bench/runs/{run['id']}/frames/lumen-preview/retry"),
                         second_studio.post(f"/v1/bench/runs/{run['id']}/pick",
                                            json={"model_slug": "vesper-3"})):
            assert response.status_code in (403, 404), (
                f"another studio reached this bench run with {response.status_code}"
            )
        wrong = client.post(f"/v1/bench/runs/{run['id']}/pick", json={"model_slug": "lumen-preview"})
        assert fx.refused(wrong) and fx.error_code(wrong) == "invalid_request", (
            f"picking the failed model returned {wrong.status_code}"
        )
        pick = client.post(f"/v1/bench/runs/{run['id']}/pick", json={"model_slug": "vesper-3"})
        assert pick.status_code in (200, 201), f"a valid pick returned {pick.status_code}"
        again = client.post(f"/v1/bench/runs/{run['id']}/pick", json={"model_slug": "grain-4-turbo"})
        assert fx.refused(again), f"a second pick returned {again.status_code}"


def test_bench_retry_of_a_succeeded_frame_is_refused():
    """Only a failed or timed-out frame may be retried."""
    with fx.fresh_creator() as client:
        run = fx.start_bench(client, ["grain-4-turbo", "folio-2"]).json()
        fx.await_bench(client, run["id"])
        before = fx.balance(client)
        retry = client.post(f"/v1/bench/runs/{run['id']}/frames/grain-4-turbo/retry")
        assert fx.refused(retry) and fx.error_code(retry) == "conflict", (
            f"retrying a succeeded frame returned {retry.status_code}"
        )
        assert fx.balance(client) == before, "a refused retry was charged"


def test_replayed_bench_key_starts_nothing_new(backend):
    """A replayed bench key returns the same run."""
    with fx.fresh_creator() as client:
        key = fx.idem_key()
        first = fx.start_bench(client, ["grain-4-turbo", "folio-2"], key=key).json()
        second = fx.start_bench(client, ["grain-4-turbo", "folio-2"], key=key).json()
        assert first.get("id") == second.get("id"), "a replayed key started a second run"
        fx.await_bench(client, first["id"])
        assert fx.balance(client) == fx.TRIAL_CREDITS - 144, f"balance is {fx.balance(client)}"
        assert backend.count("bench_run", idempotency_key=key) == 1


def test_bench_writes_nothing_to_the_bucket(store, backend):
    """A bench run keeps no output in the object store and names nobody."""
    with fx.fresh_creator() as client:
        studio_id = fx.workspace(client)["id"]
        before = store.list(f"outputs/{studio_id}/")
        run = fx.start_bench(client, ["grain-4-turbo", "halcyon-2-1"]).json()
        fx.await_bench(client, run["id"])
        assert store.list(f"outputs/{studio_id}/") == before, "a bench run wrote to the bucket"
        row = backend.one("bench_run", id=run["id"])
        assert row is not None, "the bench run record is missing"
        assert not any(k in row for k in ("user_id", "email", "display_name")), (
            f"the bench record names who ran it: {sorted(row)}"
        )


def test_bench_win_rates_hide_pairs_below_the_run_floor():
    """Win rates list only model pairs with at least two hundred runs."""
    rows = fx.listed(httpx.get(f"{fx.api_base()}/v1/bench/win-rates", timeout=fx.TIMEOUT))
    assert all(int(r.get("runs", 0)) >= 200 for r in rows), f"win rates list thin pairs: {rows}"


def test_posts_filter_and_sort_by_address_parameters():
    """The posts route filters and sorts by its query parameters."""
    comparisons = [p for p in fx.POSTS if p[2] == "comparisons"]
    body = fx.listed(httpx.get(f"{fx.api_base()}/v1/posts",
                               params={"category": "comparisons", "sort": "oldest"}, timeout=fx.TIMEOUT))
    assert [p.get("title") for p in body] == [p[1] for p in reversed(comparisons)], (
        f"oldest comparisons read {[p.get('title') for p in body]}"
    )
    guides = fx.listed(httpx.get(f"{fx.api_base()}/v1/posts",
                                 params={"category": "guides", "sort": "newest"}, timeout=fx.TIMEOUT))
    assert [p.get("slug") for p in guides] == [p[0] for p in fx.POSTS if p[2] == "guides"]
    bad = httpx.get(f"{fx.api_base()}/v1/posts", params={"category": "rumours"}, timeout=fx.TIMEOUT)
    assert fx.refused(bad), f"an unknown category returned {bad.status_code}"


def test_posts_paginate_at_twelve_with_an_opaque_cursor():
    """Posts come twelve at a time with a cursor header for the rest."""
    first = httpx.get(f"{fx.api_base()}/v1/posts", timeout=fx.TIMEOUT)
    page_one = fx.listed(first)
    assert [p.get("slug") for p in page_one] == [p[0] for p in fx.POSTS[:fx.BLOG_PAGE_SIZE]]
    cursor = first.headers.get("x-next-cursor")
    assert cursor, "the first page carries no X-Next-Cursor header"
    second = httpx.get(f"{fx.api_base()}/v1/posts", params={"cursor": cursor}, timeout=fx.TIMEOUT)
    assert [p.get("slug") for p in fx.listed(second)] == [p[0] for p in fx.POSTS[fx.BLOG_PAGE_SIZE:]]
    assert not second.headers.get("x-next-cursor"), "the last page still carries a cursor"
    for slug, title, *_ in fx.POSTS[:3]:
        assert fx.page_response(f"/blog/{slug}").status_code == 200, f"/blog/{slug} did not answer"
        one = httpx.get(f"{fx.api_base()}/v1/posts/{slug}", timeout=fx.TIMEOUT)
        assert one.status_code == 200 and one.json().get("title") == title and one.json().get("body"), (
            f"GET /api/v1/posts/{slug} returned {one.status_code}: {one.text[:200]}"
        )
    unknown = httpx.get(f"{fx.api_base()}/v1/posts/no-such-post", timeout=fx.TIMEOUT)
    assert unknown.status_code == 404, f"an unknown post returned {unknown.status_code}"


def test_blog_address_restores_the_filtered_view(page):
    """A cold load of a filtered blog address shows that view."""
    page.goto(f"{fx.app_url()}/blog?category=comparisons&sort=oldest")
    comparisons = [p[1] for p in fx.POSTS if p[2] == "comparisons"]
    expect(page.get_by_text(comparisons[-1]).first).to_be_visible()
    body = page.inner_text("body")
    positions = [body.find(t) for t in reversed(comparisons)]
    assert all(p >= 0 for p in positions) and positions == sorted(positions), (
        f"comparison titles appear at {positions}"
    )
    assert fx.POSTS[0][1] not in body, "a company news post shows under the comparisons filter"
    assert "Aug 27, 2026" in body and "9 min read" in body, "a card lacks its date or reading time"
    for label in ("All", "Company news", "Comparisons", "Guides", "Newest", "Oldest"):
        expect(page.get_by_text(label, exact=True).first).to_be_attached()


def test_lead_submission_stores_one_lead(backend):
    """An enterprise lead and a newsletter lead are each stored once."""
    email = fx.probe_email()
    response = httpx.post(f"{fx.api_base()}/v1/leads", timeout=fx.TIMEOUT, json={
        "source": "enterprise", "name": "Probe Buyer", "email": email,
        "company": "Field and Frame", "team_size": "11-50", "message": "A shared canvas"})
    assert response.status_code in (200, 201), f"an enterprise lead returned {response.status_code}"
    assert backend.count("lead", email=email) == 1, "the enterprise lead is not stored once"
    letter = fx.probe_email()
    response = httpx.post(f"{fx.api_base()}/v1/leads", timeout=fx.TIMEOUT,
                          json={"source": "newsletter", "email": letter})
    assert response.status_code in (200, 201), f"a newsletter lead returned {response.status_code}"
    assert backend.count("lead", email=letter, source="newsletter") == 1


def test_invalid_lead_is_refused_and_stores_nothing(backend):
    """A malformed address, a missing field or an unknown team size stores nothing."""
    email = fx.probe_email()
    for payload in ({"source": "enterprise", "name": "Probe", "email": "nope",
                     "company": "Co", "team_size": "1-10", "message": "m"},
                    {"source": "enterprise", "email": email, "company": "Co",
                     "team_size": "1-10", "message": "m"},
                    {"source": "enterprise", "name": "Probe", "email": email,
                     "company": "Co", "team_size": "9000", "message": "m"}):
        response = httpx.post(f"{fx.api_base()}/v1/leads", json=payload, timeout=fx.TIMEOUT)
        assert fx.refused(response) and fx.error_code(response) == "invalid_request", (
            f"an invalid lead returned {response.status_code}: {response.text[:200]}"
        )
    assert backend.count("lead", email=email) == 0, "an invalid lead was stored"


def test_desktop_releases_are_listed_at_the_pinned_version():
    """Four releases are listed at the pinned version."""
    releases = fx.listed(httpx.get(f"{fx.api_base()}/v1/desktop/releases", timeout=fx.TIMEOUT))
    got = {(r.get("platform"), r.get("arch")): r.get("label") for r in releases}
    assert got == fx.DESKTOP_RELEASES, f"releases are {got}"
    assert {r.get("version") for r in releases} == {fx.DESKTOP_VERSION}


def test_desktop_route_offers_the_detected_platform_first(browser_page):
    """A Windows visitor is offered the Windows download first."""
    page = browser_page(user_agent=fx.WINDOWS_USER_AGENT)
    page.goto(f"{fx.app_url()}/desktop-app")
    expect(page.locator("[data-primary-platform='windows']").first).to_be_attached()
    expect(page.get_by_text("Download for Windows").first).to_be_visible()
    body = page.inner_text("body")
    for heading in fx.NATIVE_CAPABILITIES:
        assert heading in body, f"the desktop route does not state {heading!r}"
    assert fx.DESKTOP_VERSION in body, "the desktop route does not show the version"


def test_announcement_dismissal_survives_a_reload(page):
    """A dismissed announcement stays dismissed after a reload."""
    page.goto(f"{fx.app_url()}/")
    expect(page.get_by_text(fx.ANNOUNCEMENT_TEXT).first).to_be_visible()
    expect(page.get_by_text("Try it on the canvas").first).to_be_visible()
    page.get_by_role("button", name="Dismiss announcement").first.click()
    expect(page.get_by_text(fx.ANNOUNCEMENT_TEXT)).to_have_count(0)
    page.reload()
    page.wait_for_load_state("networkidle")
    expect(page.get_by_text(fx.ANNOUNCEMENT_TEXT)).to_have_count(0)


def test_reduced_motion_selects_the_static_drawing_tier(browser_page):
    """A reduced-motion visitor gets the static tier and the reduced track."""
    page = browser_page(reduced_motion="reduce")
    page.goto(f"{fx.app_url()}/")
    root = page.locator("html")
    expect(root).to_have_attribute("data-motion", "reduced")
    expect(root).to_have_attribute("data-gl-tier", "static")


def test_sound_is_off_on_a_first_visit(page):
    """Sound starts off and the tier attribute is declared."""
    page.goto(f"{fx.app_url()}/")
    root = page.locator("html")
    expect(root).to_have_attribute("data-sound", "off")
    tier = root.get_attribute("data-gl-tier")
    assert tier in ("full", "reduced", "static"), f"data-gl-tier reads {tier!r}"
    motion = root.get_attribute("data-motion")
    assert motion in ("full", "reduced"), f"data-motion reads {motion!r}"


def test_about_route_carries_people_roles_and_investors(page):
    """The about route names the vignettes, people, roles and investors."""
    page.goto(f"{fx.app_url()}/about")
    expect(page.get_by_text(fx.TEAM_NAMES[0]).first).to_be_visible()
    body = page.inner_text("body")
    for text in fx.VIGNETTES + fx.TEAM_NAMES + fx.OPEN_ROLES + fx.INVESTOR_NAMES + ("Porto", "Bonfim"):
        assert text in body, f"the about route does not show {text!r}"
    expect(page.locator("a[href$='/about/roles']").first).to_be_attached()
    page.goto(f"{fx.app_url()}/about/roles")
    roles = page.inner_text("body")
    assert all(role in roles for role in fx.OPEN_ROLES), "the roles route misses a role"


def test_enterprise_route_offers_calls_not_trials(page):
    """The enterprise route carries its tabs, cards and booking calls."""
    page.goto(f"{fx.app_url()}/enterprise")
    expect(page.get_by_text("Your studio, one canvas.").first).to_be_visible()
    body = page.inner_text("body")
    for text in fx.ENTERPRISE_TABS + fx.ENTERPRISE_CARDS + ("Work email", "Team size"):
        assert text in body, f"the enterprise route does not show {text!r}"
    assert body.count(fx.ENTERPRISE_ACTION) >= len(fx.ENTERPRISE_CARDS), (
        "not every capability card ends in a booking call"
    )
    assert "Start free" not in body, "the enterprise route offers a trial"
    page.get_by_text("Controls", exact=True).first.click()
    after = page.inner_text("body")
    for chip in (fx.NORTHLIGHT, fx.SALTMARSH, "Field and Frame"):
        assert chip in after, f"the controls tab does not show {chip!r}"


def test_error_envelope_carries_a_code_and_a_correlation_id(guest):
    """Refusals use one envelope whose identifier matches the response header."""
    response = guest.post("/v1/canvases", json={"name": "Anonymous canvas"})
    assert response.status_code == 401, f"an anonymous write returned {response.status_code}"
    body = response.json()
    error = body.get("error") or {}
    assert error.get("code") == "unauthenticated" and error.get("message"), f"the envelope reads {body}"
    assert error.get("correlation_id"), "the envelope carries no correlation_id"
    assert response.headers.get("x-correlation-id") == error["correlation_id"], (
        "the correlation header and body disagree"
    )
    missing = httpx.get(f"{fx.api_base()}/v1/forecasts/999999999", timeout=fx.TIMEOUT)
    assert missing.status_code == 404 and fx.error_code(missing) == "not_found", (
        f"an unknown forecast returned {missing.status_code}: {missing.text[:200]}"
    )
    assert set(fx.ERROR_CODES) >= {error["code"], fx.error_code(missing)}


def test_privacy_page_is_linked_from_every_footer(page):
    """Every public page links the privacy page, which names the removal address."""
    for route in ("/", "/pricing", "/models", "/blog", "/about", "/halcyon-2-1"):
        page.goto(f"{fx.app_url()}{route}")
        expect(page.locator("footer a[href$='/privacy']").first).to_be_attached()
    footer = page.locator("footer").first
    for href in ("/terms", "/acceptable-use"):
        expect(footer.locator(f"a[href$='{href}']").first).to_be_attached()
    external = footer.eval_on_selector_all(
        "a[href^='http']", "els => els.map(e => [e.getAttribute('href'), e.getAttribute('target')])")
    outward = [pair for pair in external if not fx.is_internal(pair[0])]
    assert outward, "the footer carries no external link"
    assert all(target == "_blank" for _, target in outward), f"external footer links: {outward}"
    footer_text = footer.inner_text()
    for text in fx.FOOTER_TEXT:
        assert text in footer_text, f"the footer does not show {text!r}"
    page.goto(f"{fx.app_url()}{fx.PRIVACY_ROUTE}")
    expect(page.get_by_text(fx.PRIVACY_EMAIL).first).to_be_visible()
    for route in ("/terms", "/acceptable-use"):
        assert fx.page_response(route).status_code == 200, f"{route} did not answer"


def test_favicon_is_served_and_declared_in_the_head():
    """The head declares a favicon that resolves to an image."""
    head = fx.head_tags(fx.rendered_html("/"))
    assert head["icons"], "the home document declares no icon"
    icon = httpx.get(fx.absolute(head["icons"][0]), timeout=fx.TIMEOUT)
    assert icon.status_code == 200 and icon.headers.get("content-type", "").startswith("image/"), (
        f"the favicon returned {icon.status_code} {icon.headers.get('content-type')}"
    )


def test_every_public_route_declares_a_resolving_preview_image():
    """Each public route declares a preview title and a preview image that resolves."""
    for route in fx.PUBLIC_ROUTES + ("/halcyon-2-1", "/blog/vesper-3-lands"):
        head = fx.head_tags(fx.rendered_html(route))
        assert head["meta"].get("og:title"), f"{route} declares no preview title"
        image = head["meta"].get("og:image")
        assert image, f"{route} declares no preview image"
        response = httpx.get(fx.absolute(image), timeout=fx.TIMEOUT)
        assert response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"), (
            f"the preview image for {route} returned {response.status_code}"
        )


def test_public_routes_have_distinct_titles_and_descriptions():
    """No two public routes share a title or a description."""
    titles, descriptions = {}, {}
    for route in fx.PUBLIC_ROUTES + ("/halcyon-2-1", "/kinetic-3-pro"):
        head = fx.head_tags(fx.rendered_html(route))
        assert head["title"], f"{route} has no title"
        assert head["meta"].get("description"), f"{route} has no description"
        titles.setdefault(head["title"], []).append(route)
        descriptions.setdefault(head["meta"]["description"], []).append(route)
    shared = [r for r in list(titles.values()) + list(descriptions.values()) if len(r) > 1]
    assert not shared, f"routes sharing a title or description: {shared}"


def test_internal_links_on_public_routes_resolve(page):
    """Every internal link on the public routes answers."""
    targets = set()
    for route in ("/", "/pricing", "/models", "/halcyon-2-1", "/enterprise", "/about", "/blog"):
        page.goto(f"{fx.app_url()}{route}")
        page.wait_for_load_state("networkidle")
        hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
        targets.update(fx.absolute(h).split("#")[0] for h in hrefs if fx.is_internal(h))
        assert "seamless" not in page.inner_text("body").lower(), f"{route} uses the word seamless"
    broken = []
    for target in sorted(targets):
        response = httpx.get(target, timeout=fx.TIMEOUT, follow_redirects=True)
        if response.status_code >= 400:
            broken.append((target, response.status_code))
    assert targets, "no internal links were found"
    assert not broken, f"internal links that do not resolve: {broken[:10]}"


def test_unknown_address_answers_not_found_with_the_product_page(page):
    """An unknown address answers not found and shows the product's own page."""
    raw = fx.page_response("/no-such-canvas-page")
    assert raw.status_code == 404, f"an unknown address answered {raw.status_code}"
    response = page.goto(f"{fx.app_url()}/no-such-canvas-page")
    assert response.status == 404, f"the browser saw status {response.status}"
    expect(page.get_by_text(fx.NOT_FOUND_LINE).first).to_be_visible()
    expect(page.get_by_text(fx.NOT_FOUND_ACTION).first).to_be_visible()
    expect(page.locator("footer").first).to_be_attached()


def test_seeding_is_idempotent_and_balances_match_the_ledger(backend, owner):
    """Seeded rows exist exactly once and a balance is the sum of its entries."""
    for email in fx.SEEDED_EMAILS:
        assert backend.count("app_user", email=email) == 1, f"{email} is not seeded exactly once"
    assert backend.count("plan") == 5 and backend.count("model") == 22
    assert backend.count("blog_post") == 14 and backend.count("rate_version") == 2
    studio = fx.workspace(owner)
    assert backend.count("canvas", workspace_id=studio["id"], name=fx.CITRUS_LAUNCH) == 1
    grants = backend.rows("credit_entry", workspace_id=studio["id"], kind="plan_grant")
    assert len(grants) == 1 and grants[0]["amount"] == 110000, f"Northlight grants are {grants}"
    total = sum(int(r["amount"]) for r in backend.rows("credit_entry", workspace_id=studio["id"]))
    assert total == fx.balance(owner) >= 0, f"the ledger sums to {total}, the API says {fx.balance(owner)}"


def test_seeded_studio_balances_match_the_brief(owner, second_studio):
    """The seeded ledgers open at the pinned balances."""
    entries = owner.get("/v1/credits").json()["entries"]
    seeded = sorted(entries, key=lambda e: e["id"])[:9]
    assert sum(e["amount"] for e in seeded) == fx.NORTHLIGHT_BALANCE, (
        f"the nine seeded Northlight entries sum to {sum(e['amount'] for e in seeded)}"
    )
    assert sorted(e["kind"] for e in seeded) == ["plan_grant"] + ["run"] * 8
    assert [e["created_at"] for e in entries] == sorted([e["created_at"] for e in entries], reverse=True), (
        "credit entries are not newest first"
    )
    theirs = fx.workspace(second_studio)
    assert theirs.get("name") == fx.SALTMARSH and theirs.get("plan_code") == "creator"
    assert fx.balance(second_studio) == fx.SALTMARSH_BALANCE, (
        f"Saltmarsh Cut holds {fx.balance(second_studio)} credits"
    )
    trailer = fx.canvas_named(second_studio, fx.TRAILER_CUT)
    assert len(trailer["nodes"]) == 5 and not any(n.get("latest_output") for n in trailer["nodes"])
    lookbook = fx.canvas_named(owner, fx.AUTUMN_LOOKBOOK)
    assert len(lookbook["nodes"]) == 5 and not any(n.get("latest_output") for n in lookbook["nodes"])


def test_signed_in_routes_redirect_anonymous_visitors(browser_page):
    """An anonymous visitor to a signed-in route lands on sign-in."""
    page = browser_page()
    for route in fx.SIGNED_IN_ROUTES:
        page.goto(f"{fx.app_url()}{route}")
        page.wait_for_url(re.compile(r".*/sign-in.*"))
        assert "/sign-in" in page.url, f"{route} left an anonymous visitor on {page.url}"


def test_narrow_viewport_does_not_scroll_sideways(browser_page):
    """At a narrow viewport no public page overflows sideways."""
    page = browser_page(viewport=fx.NARROW_VIEWPORT, is_mobile=True, has_touch=True)
    for route in ("/", "/pricing", "/models", "/bench", "/blog", "/about"):
        page.goto(f"{fx.app_url()}{route}")
        page.wait_for_load_state("networkidle")
        overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 1, f"{route} overflows sideways by {overflow} at a narrow viewport"


def test_list_endpoints_return_top_level_arrays(owner, client_user):
    """Every list endpoint returns a top-level JSON array."""
    for client, path in ((owner, "/v1/canvases"), (owner, "/v1/deliveries"),
                         (owner, "/v1/billing-events"), (client_user, "/v1/deliveries")):
        body = client.get(path).json()
        assert isinstance(body, list), f"{path} returned {type(body).__name__}"
    for path in ("/v1/models", "/v1/plans", "/v1/replay/graphs", "/v1/posts",
                 "/v1/desktop/releases", "/v1/bench/win-rates"):
        body = httpx.get(f"{fx.api_base()}{path}", timeout=fx.TIMEOUT).json()
        assert isinstance(body, list), f"{path} returned {type(body).__name__}"


def test_canvases_page_shows_the_table_and_inline_row(browser_page):
    """Signing in as a creator lands on the canvases table with its inline row."""
    page = browser_page(viewport={"width": 1440, "height": 900})
    page.goto(f"{fx.app_url()}/sign-in")
    page.get_by_label("Email").fill(fx.OWNER_EMAIL)
    page.get_by_label("Password").fill(fx.CORPUS_PASSWORD)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url(re.compile(r".*/canvases.*"))
    for column in fx.CANVAS_TABLE_COLUMNS:
        expect(page.get_by_role("columnheader", name=column).first).to_be_visible()
    expect(page.get_by_placeholder(fx.CANVAS_INLINE_PLACEHOLDER).first).to_be_visible()
    expect(page.get_by_text(fx.CITRUS_LAUNCH).first).to_be_visible()
    body = page.inner_text("body")
    assert fx.NORTHLIGHT in body, "the top bar does not name the studio"
    page.get_by_text(fx.CITRUS_LAUNCH).first.click()
    page.wait_for_url(re.compile(r".*/canvases/.+"))
    expect(page.locator("[data-node-id]").first).to_be_attached()
    states = page.eval_on_selector_all("[data-node-id]", "els => els.map(e => e.getAttribute('data-node-state'))")
    assert len(states) >= 8 and set(states) <= {"rest", "expanded", "stale", "regenerating"}, (
        f"Citrus Launch node elements carry states {states}"
    )
    for label in ("Add node", "Rerun stale nodes"):
        expect(page.get_by_text(label).first).to_be_visible()
    page.goto(f"{fx.app_url()}/deliveries")
    expect(page.locator("[data-delivery-state]").first).to_be_attached()
    rows = page.eval_on_selector_all("[data-delivery-state]", "els => els.map(e => e.getAttribute('data-delivery-state'))")
    assert rows and set(rows) <= {"delivered", "revoked"}, f"delivery rows carry {rows}"
    for column in fx.DELIVERY_COLUMNS:
        expect(page.get_by_role("columnheader", name=column).first).to_be_visible()


def test_pages_meet_the_accessibility_floors(browser_page):
    """Images carry alternatives, controls carry names, body text contrasts, header targets are large."""
    page = browser_page(viewport=fx.NARROW_VIEWPORT, is_mobile=True, has_touch=True)
    for route in ("/", "/pricing", "/models"):
        page.goto(f"{fx.app_url()}{route}")
        page.wait_for_load_state("networkidle")
        missing_alt = page.eval_on_selector_all("img", "els => els.filter(e => !e.hasAttribute('alt')).length")
        assert missing_alt == 0, f"{route} has {missing_alt} images without alternative text"
        unnamed = page.eval_on_selector_all("button, [role='button']", fx.UNNAMED_PROBE)
        assert unnamed == 0, f"{route} has {unnamed} controls with no accessible name"
        pairs = page.evaluate(fx.CONTRAST_PROBE)
        weak = [(fg, bg) for fg, bg in pairs if fx.contrast(fx.parse_rgb(fg), fx.parse_rgb(bg)) < 4.5]
        assert pairs and not weak, f"{route} has paragraph text below 4.5 to 1: {weak[:3]}"
        small = page.eval_on_selector_all("header a, header button", fx.SMALL_TARGET_PROBE)
        assert small == 0, f"{route} has {small} header targets under 44 by 44 CSS pixels"


def test_sign_in_lands_each_role_on_its_surface(browser_page):
    """Each role lands on its own surface, remembered addresses return, sign-out goes home."""
    page = browser_page()
    page.goto(f"{fx.app_url()}/account/team")
    page.wait_for_url(re.compile(r".*/sign-in.*"))
    page.get_by_label("Email").fill(fx.OWNER_EMAIL)
    page.get_by_label("Password").fill(fx.CORPUS_PASSWORD)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url(re.compile(r".*/account/team.*"))
    page.get_by_role("button", name="Sign out").first.click()
    page.wait_for_url(re.compile("^" + re.escape(fx.app_url()) + "/?$"))
    visitor = browser_page()
    visitor.goto(f"{fx.app_url()}/sign-in")
    visitor.get_by_label("Email").fill(fx.CLIENT_EMAIL)
    visitor.get_by_label("Password").fill(fx.CORPUS_PASSWORD)
    visitor.get_by_role("button", name="Sign in").click()
    visitor.wait_for_url(re.compile(r".*/deliveries.*"))
    for route in ("/canvases", "/account/billing", "/account/team"):
        visitor.goto(f"{fx.app_url()}{route}")
        visitor.wait_for_url(re.compile(r".*/deliveries.*"))


def test_public_headlines_carry_the_pinned_copy(page):
    """Each public route shows its pinned headline and labels."""
    for route, texts in fx.ROUTE_COPY.items():
        page.goto(f"{fx.app_url()}{route}")
        expect(page.get_by_text(texts[0]).first).to_be_visible()
        body = page.inner_text("body")
        for text in texts:
            assert text in body, f"{route} does not show {text!r}"
    page.goto(f"{fx.app_url()}/")
    expect(page.get_by_placeholder("Describe what you want to make").first).to_be_visible()
    expect(page.get_by_role("button", name="Start the replay").first).to_be_attached()
