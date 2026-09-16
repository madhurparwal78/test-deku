from __future__ import annotations

import html
import re

import httpx
from conftest import (
    ADMIN, ANALYST, RECRUITER, AERO_BILLING, AERO_BRAND1, AERO_BRAND2, AERO_COLLAB, AERO_OWNER, AERO_PROCUREMENT,
    AERO_PROJECT, APPROVAL_SUBJECT, CLIENT_SECRET, CLOSED_VERDANE_TICKET, DB_PASSWORD,
    DESIGNER, DEV, DIRECTOR_FR, DIRECTOR_MT, EN_LEAD_SUBJECT, FINANCE_FR, FINANCE_MT,
    FR_LEAD_SUBJECT, FRANCE, FRANCE_NAME, FREELANCE, INSTITUT_CONTRACT, INSTITUT_OWNER, INSTITUT_PROJECT,
    MALTA, MALTA_NAME, NEVER_REVEALED, NOT_FOUND_DETAIL, OPEN_AEROLINE_TICKET, PM,
    SECRET_VALUES, SECURITY, VERDANE_OWNER, VERDANE_PROJECT, ZERO_HASH,
    access_log, access_request, admin_db, app_db, approve_request, asset_paths,
    contract_by_reference, decide, draft_invoice, expect, get_json, http,
    instant_in, invoice_by_number, issue, lead_body, lead_rows, link_tags,
    location_path, login_payload, messages_containing, messages_to, meta_robots,
    milestone_invoices, mutated_id, new_deliverable, new_milestone, number_parts, org_id,
    page, poll, post_lead, project_id, read_approval, read_invoice, refusal,
    probe_statement, replica_statement, reveal, run_together, seconds_until, secret_id, settle,
    share, shared_approval, stage, step_up, stepped_up, this_year, token_for, uid,
    upload_version, verify_log, wait_for_mail, wait_for_milestone_invoice,
)


def test_client_approval_releases_one_draft_invoice_issued():
    flow = shared_approval(AERO_PROJECT, 1500000)
    approval, version = flow["approval"], flow["version"]
    assert approval.get("state") == "pending" and approval.get("value_minor") == 1500000, approval
    brand1 = token_for(AERO_BRAND1)
    decided = expect(decide(brand1, approval["id"], version["id"]), 200)
    assert decided.get("state") == "approved", f"a single stage any_of approval did not complete: {decided}"
    pm = flow["pm"]
    deliverable = get_json(pm, f"/deliverables/{flow['deliverable']['id']}")
    assert deliverable.get("status") == "approved", deliverable
    finance = token_for(FINANCE_FR)
    milestone = wait_for_milestone_invoice(pm, flow["milestone"]["id"])
    assert milestone.get("status") == "approved" and milestone.get("approved_at"), milestone
    assert milestone.get("invoice_id"), f"no draft invoice within ten seconds: {milestone}"
    settle(2.0)
    drafts = milestone_invoices(finance, flow["milestone"]["id"])
    assert len(drafts) == 1, f"approval released {len(drafts)} invoices for one milestone: {drafts}"
    draft = drafts[0]
    assert draft["id"] == milestone["invoice_id"] and draft.get("status") == "draft", draft
    assert draft.get("number") is None and draft.get("agency_entity") == FRANCE, draft
    step_up(finance)
    issued = expect(issue(finance, draft["id"]), 200)
    assert issued.get("status") == "issued", issued
    number_parts(issued.get("number"), "PXF-")
    assert issued.get("subtotal_minor") == 1500000, issued


def test_login_returns_access_token_principal_kind():
    assert login_payload(FINANCE_FR).get("principal_kind") == "agency"
    assert login_payload(AERO_OWNER).get("principal_kind") == "client"
    assert login_payload(FREELANCE).get("principal_kind") == "external"


def test_concurrent_issues_take_contiguous_numbers_stored_once():
    finance = token_for(FINANCE_FR)
    verdane = org_id(finance, "verdane")
    drafts = [draft_invoice(finance, verdane, [(1, 10000 + i)])["id"] for i in range(6)]
    step_up(finance)
    responses = run_together([(finance, None, lambda c, d=d: c.post(f"/invoices/{d}/issue"))
                              for d in drafts])
    numbers = [expect(r, 200).get("number") for r in responses]
    parts = [number_parts(n, "PXF-") for n in numbers]
    counters = sorted(counter for _, counter in parts)
    assert len(set(numbers)) == 6, f"concurrent issues shared a number: {numbers}"
    assert counters == list(range(counters[0], counters[0] + 6)), (
        f"six simultaneous issues left a gap: {numbers}")
    assert {year for year, _ in parts} == {this_year()}, numbers


def test_refused_issue_consumes_no_number():
    finance = token_for(FINANCE_FR)
    verdane = org_id(finance, "verdane")
    institut = org_id(finance, "institut-lumiere")
    first = draft_invoice(finance, verdane, [(2, 45000)])
    unpaid_po = draft_invoice(finance, institut, [(1, 90000)])
    second = draft_invoice(finance, verdane, [(1, 12000)])
    step_up(finance)
    _, before = number_parts(expect(issue(finance, first["id"]), 200)["number"], "PXF-")
    refusal(issue(finance, unpaid_po["id"]), 422, "po_required")
    _, after = number_parts(expect(issue(finance, second["id"]), 200)["number"], "PXF-")
    assert after == before + 1, (
        f"a refused issue consumed a number: issued {before}, then {after} after the refusal")


def test_entity_sequences_independent_numbers():
    france = stepped_up(FINANCE_FR)
    malta = stepped_up(FINANCE_MT)
    verdane = org_id(france, "verdane")
    valletta = org_id(malta, "valletta-yachting")
    a = draft_invoice(france, verdane, [(1, 30000)])
    m = draft_invoice(malta, valletta, [(1, 30000)])
    b = draft_invoice(france, verdane, [(1, 30000)])
    _, first = number_parts(expect(issue(france, a["id"]), 200)["number"], "PXF-")
    malta_issued = expect(issue(malta, m["id"]), 200)
    assert malta_issued.get("agency_entity") == MALTA, malta_issued
    number_parts(malta_issued["number"], "PXM-")
    _, second = number_parts(expect(issue(france, b["id"]), 200)["number"], "PXF-")
    assert second == first + 1, (
        f"a Malta issue advanced the France sequence: {first} then {second}")


def test_issued_invoice_totals_from_lines_rounded_once():
    france = stepped_up(FINANCE_FR)
    verdane = org_id(france, "verdane")
    draft = draft_invoice(france, verdane, [(1, 3), (1, 3)], total_minor=1, subtotal_minor=1)
    issued = expect(issue(france, draft["id"]), 200)
    assert issued.get("tax_treatment") == "domestic_fr" and issued.get("tax_rate_bp") == 2000, issued
    assert (issued.get("subtotal_minor"), issued.get("tax_minor"), issued.get("total_minor")) == (6, 1, 7), (
        f"tax must be computed once on the subtotal: {issued}")
    malta = stepped_up(FINANCE_MT)
    valletta = org_id(malta, "valletta-yachting")
    small = expect(issue(malta, draft_invoice(malta, valletta, [(1, 25)])["id"]), 200)
    assert small.get("tax_treatment") == "domestic_mt" and small.get("tax_rate_bp") == 1800, small
    assert (small.get("subtotal_minor"), small.get("tax_minor"), small.get("total_minor")) == (25, 5, 30), (
        f"4.5 cents of tax rounds half away from zero to 5: {small}")


def test_invalid_vat_reverse_charge_issue_refused_draft_row_untouched():
    malta = stepped_up(FINANCE_MT)
    kessler = org_id(malta, "kessler")
    draft = draft_invoice(malta, kessler, [(4, 25000)])
    refusal(issue(malta, draft["id"]), 422, "vat_number_invalid")
    after = read_invoice(malta, draft["id"])
    assert after.get("status") == "draft" and after.get("number") is None, (
        f"a refused reverse charge changed the draft: {after}")


def test_stale_vies_validation_issue_refused():
    malta = stepped_up(FINANCE_MT)
    alpenrad = org_id(malta, "alpenrad")
    draft = draft_invoice(malta, alpenrad, [(1, 150000)])
    refusal(issue(malta, draft["id"]), 422, "vat_validation_stale")
    after = read_invoice(malta, draft["id"])
    assert after.get("status") == "draft" and after.get("number") is None, after


def test_recent_vies_validation_reverse_charge_note():
    malta = stepped_up(FINANCE_MT)
    vondel = org_id(malta, "vondel")
    issued = expect(issue(malta, draft_invoice(malta, vondel, [(2, 40000)])["id"]), 200)
    assert issued.get("tax_treatment") == "eu_reverse_charge", issued
    assert issued.get("tax_rate_bp") == 0 and issued.get("tax_minor") == 0, issued
    assert issued.get("tax_note") == "Reverse charge - Art. 196 VAT Directive", issued
    assert issued.get("total_minor") == 80000, issued


def test_same_country_valid_vat_domestic_treatment():
    france = stepped_up(FINANCE_FR)
    malta = stepped_up(FINANCE_MT)
    aeroline = expect(issue(france, draft_invoice(france, org_id(france, "aeroline"), [(1, 100000)])["id"]), 200)
    assert (aeroline.get("tax_treatment"), aeroline.get("tax_rate_bp"), aeroline.get("tax_note")) == (
        "domestic_fr", 2000, "Standard French TVA"), aeroline
    assert aeroline.get("tax_minor") == 20000, aeroline
    brugmann = expect(issue(malta, draft_invoice(malta, org_id(malta, "brugmann"), [(1, 100000)])["id"]), 200)
    assert (brugmann.get("tax_treatment"), brugmann.get("tax_note")) == (
        "eu_reverse_charge", "Reverse charge - Art. 196 VAT Directive"), brugmann
    lakeside = expect(issue(malta, draft_invoice(malta, org_id(malta, "lakeside"), [(1, 100000)])["id"]), 200)
    assert (lakeside.get("tax_treatment"), lakeside.get("tax_rate_bp"), lakeside.get("tax_note")) == (
        "export_outside_eu", 0, "Outside scope"), lakeside


def test_public_sector_without_po_issue_refused_no_number_stored():
    france = stepped_up(FINANCE_FR)
    institut = org_id(france, "institut-lumiere")
    draft = draft_invoice(france, institut, [(1, 300000)])
    refusal(issue(france, draft["id"]), 422, "po_required")
    after = read_invoice(france, draft["id"])
    assert after.get("status") == "draft" and after.get("number") is None, after


def test_einvoice_channel_by_client_profile():
    france = stepped_up(FINANCE_FR)
    malta = stepped_up(FINANCE_MT)
    public = expect(issue(france, draft_invoice(france, org_id(france, "institut-lumiere"),
                                                [(1, 300000)], po_number=uid("PO"))["id"]), 200)
    assert public.get("einvoice_channel") == "chorus_pro" and public.get("po_number"), public
    business = expect(issue(france, draft_invoice(france, org_id(france, "aeroline"), [(1, 50000)])["id"]), 200)
    assert business.get("einvoice_channel") == "pdp", business
    maltese = expect(issue(malta, draft_invoice(malta, org_id(malta, "valletta-yachting"), [(1, 50000)])["id"]), 200)
    assert maltese.get("einvoice_channel") == "none", maltese


def test_credit_note_own_sequence_voids_original_keeps_number():
    france = stepped_up(FINANCE_FR)
    verdane = org_id(france, "verdane")
    original = expect(issue(france, draft_invoice(france, verdane, [(3, 10000), (1, 5000)])["id"]), 200)
    with http(france) as c:
        note = expect(c.post(f"/invoices/{original['id']}/credit-note",
                             json={"reason": "Duplicate billing of the design phase"}), 201)
    assert note.get("doc_type") == "credit_note", note
    number_parts(note.get("number"), "PXFC-")
    assert note.get("credits_invoice_id") == original["id"], note
    assert note.get("total_minor") == -original["total_minor"], note
    assert note.get("tax_minor") == -original["tax_minor"], note
    assert sorted(line["amount_minor"] for line in note.get("lines", [])) == sorted(
        -line["amount_minor"] for line in original["lines"]), note
    assert note.get("tax_treatment") == original.get("tax_treatment"), note
    voided = read_invoice(france, original["id"])
    assert voided.get("status") == "void" and voided.get("number") == original["number"], voided
    _, before = number_parts(original["number"], "PXF-")
    _, after = number_parts(expect(issue(france, draft_invoice(france, verdane, [(1, 1000)])["id"]), 200)["number"], "PXF-")
    assert after == before + 1, f"the credit note consumed an invoice number: {before} then {after}"


def test_credit_note_on_draft_refused_not_issued():
    france = stepped_up(FINANCE_FR)
    draft = draft_invoice(france, org_id(france, "verdane"), [(1, 20000)])
    with http(france) as c:
        refusal(c.post(f"/invoices/{draft['id']}/credit-note", json={"reason": "Wrong client"}),
                409, "invoice_not_issued")
    assert read_invoice(france, draft["id"]).get("status") == "draft"


def test_project_manager_issue_denied_invoice_row_untouched():
    france = token_for(FINANCE_FR)
    draft = draft_invoice(france, org_id(france, "verdane"), [(1, 70000)])
    pm = stepped_up(PM)
    denied = issue(pm, draft["id"])
    assert denied.status_code in (403, 404), (
        f"a project manager issued an invoice: {denied.status_code} {denied.text[:300]}")
    after = read_invoice(france, draft["id"])
    assert after.get("status") == "draft" and after.get("number") is None, after


def test_login_alone_is_not_step_up_issue_forbidden():
    france = token_for(FINANCE_FR)
    draft = draft_invoice(france, org_id(france, "verdane"), [(1, 80000)])
    refusal(issue(france, draft["id"]), 403, "step_up_required")
    assert read_invoice(france, draft["id"]).get("number") is None
    step_up(france)
    assert expect(issue(france, draft["id"]), 200).get("status") == "issued"


def test_other_entity_finance_admin_issue_forbidden():
    france = token_for(FINANCE_FR)
    draft = draft_invoice(france, org_id(france, "verdane"), [(1, 90000)])
    malta = stepped_up(FINANCE_MT)
    denied = issue(malta, draft["id"])
    assert denied.status_code in (403, 404), (
        f"a Malta finance admin issued a France invoice: {denied.status_code} {denied.text[:300]}")
    after = read_invoice(france, draft["id"])
    assert after.get("status") == "draft" and after.get("number") is None, after


def test_unauthenticated_invoice_list_denied():
    with http() as c:
        refusal(c.get("/invoices"), 401, "unauthenticated")
        refusal(c.post("/invoices", json={"client_org_id": "x", "lines": []}), 401, "unauthenticated")


def test_signup_closed_and_wrong_password_denied():
    with http() as c:
        refusal(c.post("/auth/signup", json={"email": uid("new") + "@example.com",
                                             "password": "deku-demo-pw-2026"}), 404, "not_found")
        refusal(c.post("/auth/login", json={"email": FINANCE_FR, "password": "not-the-password"}),
                401, "invalid_credentials")


def test_role_table_never_cells_denied_at_api():
    pm = token_for(PM)
    aero = project_id(pm, AERO_PROJECT)
    verdane = org_id(pm, "verdane")
    with http(token_for(FINANCE_FR)) as c:
        listed = c.get("/vault/secrets", params={"client_org_id": verdane})
    assert listed.status_code in (403, 404) or (listed.status_code == 200 and listed.json() == []), (
        f"a finance admin opened the vault: {listed.status_code} {listed.text[:200]}")
    with http(token_for(RECRUITER)) as c:
        foreign = c.get(f"/projects/{aero}")
    assert foreign.status_code in (403, 404), f"a recruiter read client project data: {foreign.status_code}"
    with http(token_for(ANALYST)) as c:
        written = c.post(f"/projects/{aero}/milestones", json={"name": uid("Analyst"), "bill_amount_minor": 1000})
    assert written.status_code in (403, 404), f"an analyst wrote a milestone: {written.status_code} {written.text[:200]}"
    deliverable = new_deliverable(pm, aero, new_milestone(pm, aero, 90000)["id"])
    with http(token_for(AERO_BILLING)) as c:
        seen = c.get(f"/deliverables/{deliverable['id']}")
    assert seen.status_code in (403, 404), f"client finance read a deliverable: {seen.status_code}"
    designer = token_for(DESIGNER)
    aeroline = org_id(designer, "aeroline")
    proposal = next(p for p in get_json(designer, "/proposals", client_org_id=aeroline) if p.get("version") == 2)
    detail = get_json(designer, f"/proposals/{proposal['id']}")
    assert "margin_minor" not in detail, f"margin reached a producer: {detail}"
    assert all("cost_price_minor" not in line for line in detail.get("lines", [])), detail
    france = token_for(FINANCE_FR)
    draft = draft_invoice(france, org_id(france, "verdane"), [(1, 64000)])
    issued_by_director = issue(stepped_up(DIRECTOR_FR), draft["id"])
    assert issued_by_director.status_code in (403, 404), (
        f"an account director issued an invoice: {issued_by_director.status_code} {issued_by_director.text[:200]}")
    assert read_invoice(france, draft["id"]).get("number") is None
    secret = secret_id(token_for(DEV), verdane, "Hosting control panel")
    security = token_for(SECURITY)
    request = expect(access_request(security, secret, break_glass=True), 201)
    refusal(approve_request(security, request["id"]), 403, "self_approval_forbidden")


def test_uploader_decision_denied_separation_of_duties_row_unchanged():
    flow = shared_approval(VERDANE_PROJECT, 250000, uploader=DIRECTOR_FR)
    approval, version = flow["approval"], flow["version"]
    assert DIRECTOR_FR in stage(approval, 1).get("assignees", []), approval
    director = token_for(DIRECTOR_FR)
    refusal(decide(director, approval["id"], version["id"]), 403, "separation_of_duties")
    after = read_approval(director, approval["id"])
    assert after.get("state") == "pending", after
    assert stage(after, 1).get("decisions") == [], f"a refused decision was recorded: {after}"
    owner = token_for(VERDANE_OWNER)
    assert expect(decide(owner, approval["id"], version["id"]), 200).get("state") == "approved"


def test_rejection_without_comment_refused():
    flow = shared_approval(AERO_PROJECT, 400000)
    brand1 = token_for(AERO_BRAND1)
    refusal(decide(brand1, flow["approval"]["id"], flow["version"]["id"], "rejected", ""),
            422, "comment_required")
    after = read_approval(brand1, flow["approval"]["id"])
    assert after.get("state") == "pending" and stage(after, 1).get("decisions") == [], after


def test_rejection_ends_approval_changes_requested():
    flow = shared_approval(AERO_PROJECT, 450000)
    brand1 = token_for(AERO_BRAND1)
    rejected = expect(decide(brand1, flow["approval"]["id"], flow["version"]["id"], "rejected",
                             "The hero image contradicts the brand guide"), 200)
    assert rejected.get("state") == "rejected", rejected
    pm = flow["pm"]
    assert get_json(pm, f"/deliverables/{flow['deliverable']['id']}").get("status") == "changes_requested"
    settle(3.0)
    milestone = get_json(pm, f"/milestones/{flow['milestone']['id']}")
    assert milestone.get("status") != "approved" and not milestone.get("invoice_id"), milestone


def test_decision_on_superseded_version_refused_current_version():
    flow = shared_approval(AERO_PROJECT, 800000)
    first = flow["approval"]
    newer = upload_version(token_for(DESIGNER), flow["deliverable"]["id"])
    brand1 = token_for(AERO_BRAND1)
    refused = refusal(decide(brand1, first["id"], flow["version"]["id"]), 409, "approval_superseded")
    assert refused.get("current_version_id") == newer["id"], refused
    assert read_approval(brand1, first["id"]).get("state") == "cancelled"
    reshared = share(flow["pm"], flow["deliverable"]["id"])
    stale = refusal(decide(brand1, reshared["id"], flow["version"]["id"]), 409, "approval_superseded")
    assert stale.get("current_version_id") == newer["id"], stale
    assert read_approval(brand1, reshared["id"]).get("state") == "pending"


def test_new_version_cancels_pending_approval_state():
    flow = shared_approval(AERO_PROJECT, 600000)
    upload_version(token_for(DESIGNER), flow["deliverable"]["id"])
    after = read_approval(token_for(AERO_BRAND1), flow["approval"]["id"])
    assert after.get("state") == "cancelled", f"a new version left the old approval {after.get('state')}"
    deliverable = get_json(flow["pm"], f"/deliverables/{flow['deliverable']['id']}")
    assert deliverable.get("status") != "approved", deliverable


def test_share_without_version_refused():
    pm = token_for(PM)
    project = project_id(pm, AERO_PROJECT)
    milestone = new_milestone(pm, project, 300000)
    deliverable = new_deliverable(pm, project, milestone["id"])
    with http(pm) as c:
        refusal(c.post(f"/deliverables/{deliverable['id']}/share"), 422, "version_required")


def test_reshared_version_approves_milestone():
    flow = shared_approval(AERO_PROJECT, 700000)
    newer = upload_version(token_for(DESIGNER), flow["deliverable"]["id"])
    reshared = share(flow["pm"], flow["deliverable"]["id"])
    assert reshared.get("version_id") == newer["id"], reshared
    brand1 = token_for(AERO_BRAND1)
    assert expect(decide(brand1, reshared["id"], newer["id"]), 200).get("state") == "approved"
    milestone = wait_for_milestone_invoice(flow["pm"], flow["milestone"]["id"])
    assert milestone.get("status") == "approved" and milestone.get("invoice_id"), milestone


def test_high_value_approval_uses_two_stage_policy():
    high = shared_approval(AERO_PROJECT, 3000000)["approval"]
    assert high.get("value_minor") == 3000000 and high.get("current_stage") == 1, high
    assert len(high.get("stages", [])) == 2, high
    first, second = stage(high, 1), stage(high, 2)
    assert first.get("mode") == "any_of" and set(first.get("assignees", [])) == {AERO_BRAND1, AERO_BRAND2}, first
    assert second.get("mode") == "all_of" and set(second.get("assignees", [])) == {AERO_OWNER, AERO_PROCUREMENT}, second
    low = shared_approval(AERO_PROJECT, 2000000)["approval"]
    assert len(low.get("stages", [])) == 1, f"a value at the band edge took the high policy: {low}"


def test_all_of_stage_waits_for_every_assignee_counted_once():
    flow = shared_approval(AERO_PROJECT, 3200000)
    approval, version = flow["approval"], flow["version"]
    staged = expect(decide(token_for(AERO_BRAND1), approval["id"], version["id"]), 200)
    assert staged.get("state") == "pending" and staged.get("current_stage") == 2, staged
    owner = token_for(AERO_OWNER)
    once = expect(decide(owner, approval["id"], version["id"]), 200)
    assert once.get("state") == "pending", f"all_of completed on one of two approvers: {once}"
    twice = expect(decide(owner, approval["id"], version["id"]), 200)
    assert twice.get("state") == "pending", f"a repeated decision completed the stage: {twice}"
    owner_votes = [d for d in stage(twice, 2).get("decisions", []) if d.get("decided_by_email") == AERO_OWNER]
    assert len(owner_votes) == 1, f"a repeated decision was recorded twice: {owner_votes}"
    done = expect(decide(token_for(AERO_PROCUREMENT), approval["id"], version["id"]), 200)
    assert done.get("state") == "approved", done


def test_concurrent_all_of_final_decisions_one_draft_invoice_row():
    flow = shared_approval(AERO_PROJECT, 3400000)
    approval, version = flow["approval"], flow["version"]
    expect(decide(token_for(AERO_BRAND1), approval["id"], version["id"]), 200)
    owner, procurement = token_for(AERO_OWNER), token_for(AERO_PROCUREMENT)
    payload = {"decision": "approved", "comment": "Signed off", "version_id": version["id"]}
    responses = run_together([
        (tok, None, lambda c: c.post(f"/approvals/{approval['id']}/decisions", json=payload))
        for tok in (owner, procurement)])
    for r in responses:
        expect(r, 200)
    assert read_approval(owner, approval["id"]).get("state") == "approved"
    finance = token_for(FINANCE_FR)
    milestone = wait_for_milestone_invoice(flow["pm"], flow["milestone"]["id"])
    assert milestone.get("invoice_id"), f"no draft invoice within ten seconds: {milestone}"
    settle(3.0)
    drafts = milestone_invoices(finance, flow["milestone"]["id"])
    assert len(drafts) == 1, f"two simultaneous final decisions drafted {len(drafts)} invoices"


def test_stage_assignees_notified_by_email_only_current_stage():
    name = uid("Campaign landing")
    flow = shared_approval(AERO_PROJECT, 3100000, name=name)
    approval, version = flow["approval"], flow["version"]
    subject = APPROVAL_SUBJECT + name
    for assignee in (AERO_BRAND1, AERO_BRAND2):
        mail = wait_for_mail(assignee, subject)
        assert len(mail) == 1, f"{assignee} received {len(mail)} approval request emails"
        assert mail[0].body.strip().startswith(approval["id"]), mail[0].body[:120]
    for outsider in (AERO_OWNER, AERO_PROCUREMENT, DESIGNER):
        assert messages_to(outsider, subject) == [], f"{outsider} was emailed for stage 1"
    expect(decide(token_for(AERO_BRAND1), approval["id"], version["id"]), 200)
    for assignee in (AERO_OWNER, AERO_PROCUREMENT):
        mail = wait_for_mail(assignee, subject)
        assert len(mail) == 1, f"{assignee} received {len(mail)} stage 2 emails"
        assert mail[0].body.strip().startswith(approval["id"]), mail[0].body[:120]
    settle(3.0)
    assert len(messages_to(AERO_BRAND2, subject)) == 1, "a stage 1 assignee was emailed for stage 2"


def test_approver_below_value_threshold_denied_unchanged():
    flow = shared_approval(AERO_PROJECT, 3000000)
    brand2 = token_for(AERO_BRAND2)
    refusal(decide(brand2, flow["approval"]["id"], flow["version"]["id"]), 403, "approval_threshold_exceeded")
    after = read_approval(brand2, flow["approval"]["id"])
    assert after.get("state") == "pending" and after.get("current_stage") == 1, after
    assert stage(after, 1).get("decisions") == [], after


def test_later_stage_assignee_cannot_decide_current_stage():
    flow = shared_approval(AERO_PROJECT, 2500000)
    procurement = token_for(AERO_PROCUREMENT)
    refusal(decide(procurement, flow["approval"]["id"], flow["version"]["id"]), 403, "forbidden")
    after = read_approval(procurement, flow["approval"]["id"])
    assert after.get("current_stage") == 1 and stage(after, 1).get("decisions") == [], after


def test_client_collaborator_decision_forbidden():
    flow = shared_approval(AERO_PROJECT, 500000)
    collab = token_for(AERO_COLLAB)
    refusal(decide(collab, flow["approval"]["id"], flow["version"]["id"]), 403, "forbidden")
    assert read_approval(token_for(AERO_BRAND1), flow["approval"]["id"]).get("state") == "pending"


def test_other_tenant_project_denied_as_not_found():
    aero = project_id(token_for(PM), AERO_PROJECT)
    verdane_owner = token_for(VERDANE_OWNER)
    with http(verdane_owner) as c:
        foreign = c.get(f"/projects/{aero}")
        missing = c.get(f"/projects/{mutated_id(aero)}")
    refused = refusal(foreign, 404, "not_found")
    absent = refusal(missing, 404, "not_found")
    assert refused.get("detail") == NOT_FOUND_DETAIL, refused
    assert (refused.get("status"), refused.get("detail")) == (absent.get("status"), absent.get("detail")), (
        f"another tenant's project answers differently from a missing one: {refused} vs {absent}")


def test_other_tenant_invoice_and_approval_not_found():
    finance = token_for(FINANCE_FR)
    aeroline_invoice = invoice_by_number(finance, FRANCE, "PXF-2026-00002")
    flow = shared_approval(AERO_PROJECT, 350000)
    verdane_owner = token_for(VERDANE_OWNER)
    with http(verdane_owner) as c:
        refusal(c.get(f"/invoices/{aeroline_invoice['id']}"), 404, "not_found")
        refusal(c.get(f"/approvals/{flow['approval']['id']}"), 404, "not_found")
    refusal(decide(verdane_owner, flow["approval"]["id"], flow["version"]["id"]), 404, "not_found")
    assert read_approval(token_for(AERO_BRAND1), flow["approval"]["id"]).get("state") == "pending"


def test_org_and_project_lists_scoped_to_tenant():
    verdane_owner = token_for(VERDANE_OWNER)
    slugs = {org.get("slug") for org in get_json(verdane_owner, "/orgs")}
    assert slugs == {"verdane"}, f"a Verdane principal lists other organisations: {slugs}"
    assert get_json(verdane_owner, "/projects", code=AERO_PROJECT) == []
    numbers = {inv.get("number") for inv in get_json(verdane_owner, "/invoices")}
    assert "PXF-2026-00002" not in numbers and "PXM-2026-00001" not in numbers, numbers


def test_project_manager_proposal_margin_absent_denied():
    pm = token_for(PM)
    aeroline = org_id(pm, "aeroline")
    proposals = get_json(pm, "/proposals", client_org_id=aeroline)
    proposal = next(p for p in proposals if p.get("version") == 2)
    detail = get_json(pm, f"/proposals/{proposal['id']}")
    assert "margin_minor" not in detail, f"margin reached a project manager without visibility: {detail}"
    assert detail.get("lines"), detail
    for line in detail["lines"]:
        assert "cost_price_minor" not in line, f"cost price reached a project manager: {line}"


def test_client_owner_sees_sent_proposal_without_cost():
    owner = token_for(AERO_OWNER)
    aeroline = org_id(owner, "aeroline")
    proposals = get_json(owner, "/proposals", client_org_id=aeroline)
    proposal = next(p for p in proposals if p.get("version") == 2)
    detail = get_json(owner, f"/proposals/{proposal['id']}")
    assert detail.get("total_minor") == 3250000, detail
    assert "margin_minor" not in detail, detail
    assert all("cost_price_minor" not in line for line in detail.get("lines", [])), detail


def test_account_director_sees_margin_from_stored_lines():
    director = token_for(DIRECTOR_FR)
    aeroline = org_id(director, "aeroline")
    proposal = next(p for p in get_json(director, "/proposals", client_org_id=aeroline) if p.get("version") == 2)
    detail = get_json(director, f"/proposals/{proposal['id']}")
    assert detail.get("margin_minor") == 1405000, detail
    assert sorted(line.get("cost_price_minor") for line in detail.get("lines", [])) == [47000, 52000, 150000], detail
    assert detail.get("subtotal_minor") == 3250000 and detail.get("discount_minor") == 0, detail


def test_access_request_requires_open_ticket_same_org():
    dev = token_for(DEV)
    verdane = org_id(dev, "verdane")
    secret = secret_id(dev, verdane, "Production CMS admin")
    refusal(access_request(dev, secret, CLOSED_VERDANE_TICKET), 422, "open_ticket_required")
    refusal(access_request(dev, secret, OPEN_AEROLINE_TICKET), 422, "open_ticket_required")
    refusal(access_request(dev, secret, None), 422, "open_ticket_required")


def test_access_request_ttl_above_limit_refused():
    dev = token_for(DEV)
    secret = secret_id(dev, org_id(dev, "verdane"), "Production CMS admin")
    refusal(access_request(dev, secret, ttl=241), 422, "ttl_exceeds_limit")
    created = expect(access_request(dev, secret, ttl=240), 201)
    assert created.get("state") == "pending" and created.get("requested_ttl_minutes") == 240, created


def test_requester_self_approval_forbidden():
    dev = token_for(DEV)
    secret = secret_id(dev, org_id(dev, "verdane"), "Production CMS admin")
    request = expect(access_request(dev, secret), 201)
    refusal(approve_request(dev, request["id"]), 403, "self_approval_forbidden")
    step_up(dev)
    refusal(reveal(dev, secret, request["id"]), 409, "request_not_approved")


def test_reveal_needs_step_up_then_single_use_access():
    dev = token_for(DEV)
    secret = secret_id(dev, org_id(dev, "verdane"), "Production CMS admin")
    request = expect(access_request(dev, secret), 201)
    approved = expect(approve_request(token_for(SECURITY), request["id"]), 200)
    assert approved.get("state") == "approved", approved
    refusal(reveal(dev, secret, request["id"]), 403, "step_up_required")
    step_up(dev)
    shown = reveal(dev, secret, request["id"])
    payload = expect(shown, 200)
    assert payload.get("value") == SECRET_VALUES["Production CMS admin@verdane"], payload
    assert payload.get("revealed_until"), payload
    assert "no-store" in shown.headers.get("cache-control", "").lower(), shown.headers
    refusal(reveal(dev, secret, request["id"]), 409, "request_already_used")


def test_reveal_with_request_for_other_secret_denied():
    dev = token_for(DEV)
    verdane = org_id(dev, "verdane")
    cms = secret_id(dev, verdane, "Production CMS admin")
    dns = secret_id(dev, verdane, "DNS registrar")
    request = expect(access_request(dev, cms), 201)
    expect(approve_request(token_for(SECURITY), request["id"]), 200)
    step_up(dev)
    refusal(reveal(dev, dns, request["id"]), 403, "access_request_required")
    assert expect(reveal(dev, cms, request["id"]), 200).get("value") == SECRET_VALUES["Production CMS admin@verdane"]


def test_reveal_appends_read_log_entry_record():
    dev = token_for(DEV)
    secret = secret_id(dev, org_id(dev, "verdane"), "Production CMS admin")
    request = expect(access_request(dev, secret), 201)
    expect(approve_request(token_for(SECURITY), request["id"]), 200)
    step_up(dev)
    expect(reveal(dev, secret, request["id"]), 200)
    entries = access_log(token_for(SECURITY))
    reads = [e for e in entries if e.get("action") == "read" and e.get("request_id") == request["id"]]
    assert len(reads) == 1, f"one reveal left {len(reads)} read entries: {entries[-3:]}"
    assert reads[0].get("principal_email") == DEV and reads[0].get("secret_id") == secret, reads[0]


def test_break_glass_needs_two_different_approvers_access():
    dev = token_for(DEV)
    secret = secret_id(dev, org_id(dev, "verdane"), "Hosting control panel")
    request = expect(access_request(dev, secret, break_glass=True), 201)
    security, director = token_for(SECURITY), token_for(DIRECTOR_FR)
    first = expect(approve_request(security, request["id"]), 200)
    assert first.get("state") == "awaiting_second_approver", first
    assert first.get("approved_by") == [SECURITY], first
    refusal(approve_request(security, request["id"]), 409, "second_approver_must_differ")
    second = expect(approve_request(director, request["id"]), 200)
    assert second.get("state") == "approved", second
    assert set(second.get("approved_by", [])) == {SECURITY, DIRECTOR_FR}, second
    step_up(dev)
    assert expect(reveal(dev, secret, request["id"]), 200).get("value") == SECRET_VALUES[
        "Hosting control panel@verdane"]


def test_break_glass_awaiting_second_reveal_refused():
    dev = token_for(DEV)
    secret = secret_id(dev, org_id(dev, "verdane"), "Hosting control panel")
    request = expect(access_request(dev, secret, break_glass=True), 201)
    expect(approve_request(token_for(SECURITY), request["id"]), 200)
    step_up(dev)
    refusal(reveal(dev, secret, request["id"]), 409, "request_not_approved")


def test_ineligible_vault_approver_forbidden():
    dev = token_for(DEV)
    secret = secret_id(dev, org_id(dev, "verdane"), "Production CMS admin")
    request = expect(access_request(dev, secret), 201)
    outsider = approve_request(token_for(DIRECTOR_MT), request["id"])
    assert outsider.status_code in (403, 404), (
        f"another entity's director approved a Verdane request: {outsider.status_code} {outsider.text[:300]}")
    approved = expect(approve_request(token_for(SECURITY), request["id"]), 200)
    assert approved.get("state") == "approved" and approved.get("approved_by") == [SECURITY], approved


def test_bulk_export_denied_and_logged():
    dev = token_for(DEV)
    with http(dev) as c:
        refusal(c.post("/vault/secrets/export"), 403, "export_denied")
    with http(stepped_up(ADMIN)) as c:
        refusal(c.post("/vault/secrets/export"), 403, "export_denied")
    entries = access_log(token_for(SECURITY))
    denied = [e for e in entries if e.get("action") == "export_denied"]
    assert any(e.get("principal_email") == DEV for e in denied), entries[-3:]
    assert any(e.get("principal_email") == ADMIN for e in denied), entries[-3:]


def test_log_chain_links_from_zero_hash():
    with http(token_for(DEV)) as c:
        c.post("/vault/secrets/export")
        c.post("/vault/secrets/export")
    entries = access_log(token_for(SECURITY))
    assert len(entries) >= 2, entries
    sequences = [e.get("sequence") for e in entries]
    assert sequences == list(range(1, len(entries) + 1)), f"sequences are not 1..n in order: {sequences}"
    assert entries[0].get("prev_hash") == ZERO_HASH, entries[0]
    for earlier, later in zip(entries, entries[1:]):
        assert later.get("prev_hash") == earlier.get("entry_hash"), (earlier, later)
    assert all(re.fullmatch(r"[0-9a-f]{64}", e.get("entry_hash") or "") for e in entries), entries[-1]


def test_tampered_log_entry_verify_reports_broken_at():
    with http(token_for(DEV)) as c:
        c.post("/vault/secrets/export")
    security = token_for(SECURITY)
    clean = verify_log(security)
    assert clean.get("valid") is True and clean.get("broken_at") is None, clean
    entries = access_log(security)
    target = entries[len(entries) // 2]["sequence"]
    original = admin_db().query(
        "SELECT principal_email FROM vault_access_log WHERE sequence = %s", (target,))[0]["principal_email"]
    replica_statement(
        f"UPDATE vault_access_log SET principal_email = 'tampered-entry' WHERE sequence = {int(target)}")
    try:
        broken = verify_log(security)
        assert broken.get("valid") is False and broken.get("broken_at") == target, (
            f"rewriting entry {target} went undetected: {broken}")
    finally:
        replica_statement(
            "UPDATE vault_access_log SET principal_email = "
            f"'{original.replace(chr(39), chr(39) * 2)}' WHERE sequence = {int(target)}")
    assert verify_log(security).get("valid") is True


def test_app_credential_cannot_update_or_delete_log_row():
    with http(token_for(DEV)) as c:
        c.post("/vault/secrets/export")
    admin = admin_db()
    before = admin.query("SELECT * FROM vault_access_log ORDER BY sequence DESC LIMIT 1")[0]
    target = int(before["sequence"])
    admin.query("DROP TABLE IF EXISTS deku_verifier_log_copy")
    admin.query(f"CREATE TABLE deku_verifier_log_copy AS SELECT * FROM vault_access_log WHERE sequence = {target}")
    app = app_db()
    probe_statement(app, f"UPDATE vault_access_log SET principal_email = 'tampered-entry' WHERE sequence = {target}")
    after_update = admin.query("SELECT * FROM vault_access_log WHERE sequence = %s", (target,))
    probe_statement(app, f"DELETE FROM vault_access_log WHERE sequence = {target}")
    after_delete = admin.query("SELECT * FROM vault_access_log WHERE sequence = %s", (target,))
    replica_statement(
        "UPDATE vault_access_log v SET principal_email = c.principal_email FROM deku_verifier_log_copy c "
        f"WHERE v.sequence = c.sequence AND v.sequence = {target}")
    replica_statement(
        "INSERT INTO vault_access_log OVERRIDING SYSTEM VALUE SELECT * FROM deku_verifier_log_copy c "
        f"WHERE NOT EXISTS (SELECT 1 FROM vault_access_log v WHERE v.sequence = {target})")
    admin.query("DROP TABLE IF EXISTS deku_verifier_log_copy")
    assert after_update and after_update[0] == before, (
        "the application's own database credential rewrote a vault access log row")
    assert after_delete, "the application's own database credential deleted a vault access log row"


def test_database_holds_no_plaintext_secret_stored():
    admin = admin_db()
    tables = admin.query(
        "SELECT table_schema, table_name FROM information_schema.tables "
        "WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')")
    assert tables, "the database holds no tables"
    leaks = []
    for table in tables:
        qualified = '"{}"."{}"'.format(table["table_schema"].replace('"', '""'),
                                       table["table_name"].replace('"', '""'))
        for value in NEVER_REVEALED:
            hit = admin.query(f"SELECT count(*) AS n FROM {qualified} t WHERE row_to_json(t)::text LIKE %s",
                              (f"%{value}%",))
            if hit[0]["n"]:
                leaks.append(f"{qualified} holds {value}")
    assert not leaks, f"a vault secret is stored in plaintext: {leaks}"


def test_grant_without_expiry_refused():
    admin = stepped_up(ADMIN)
    project = project_id(token_for(PM), VERDANE_PROJECT)
    base = {"grantee_email": FREELANCE, "resource_type": "project", "resource_id": project,
            "capability": "project:read", "reason": "Storefront performance sprint"}
    with http(admin) as c:
        refusal(c.post("/grants", json=base), 422, "grant_requires_expiry")
        refusal(c.post("/grants", json={**base, "ends_at": instant_in(-3600)}), 422, "grant_ends_in_past")


def test_grant_needs_step_up_forbidden():
    admin = token_for(ADMIN)
    project = project_id(token_for(PM), VERDANE_PROJECT)
    with http(admin) as c:
        refusal(c.post("/grants", json={"grantee_email": FREELANCE, "resource_type": "project",
                                        "resource_id": project, "capability": "project:read",
                                        "reason": "Sprint", "ends_at": instant_in(3600)}),
                403, "step_up_required")


def test_expired_grant_denied_on_next_request():
    project = project_id(token_for(PM), INSTITUT_PROJECT)
    freelance = token_for(FREELANCE)
    with http(freelance) as c:
        refusal(c.get(f"/projects/{project}"), 404, "not_found")
    ends_at = instant_in(10)
    with http(stepped_up(ADMIN)) as c:
        grant = expect(c.post("/grants", json={"grantee_email": FREELANCE, "resource_type": "project",
                                               "resource_id": project, "capability": "project:read",
                                               "reason": "Research portal audit", "ends_at": ends_at}), 201)
    assert grant.get("ends_at"), grant
    with http(freelance) as c:
        assert expect(c.get(f"/projects/{project}"), 200).get("id") == project
    settle(max(seconds_until(ends_at), 0) + 3.0)
    with http(freelance) as c:
        refusal(c.get(f"/projects/{project}"), 404, "not_found")


def test_revoked_grant_denied_immediately():
    project = project_id(token_for(PM), VERDANE_PROJECT)
    freelance = token_for(FREELANCE)
    admin = stepped_up(ADMIN)
    with http(admin) as c:
        grant = expect(c.post("/grants", json={"grantee_email": FREELANCE, "resource_type": "project",
                                               "resource_id": project, "capability": "project:read",
                                               "reason": "Storefront sprint", "ends_at": instant_in(3600)}), 201)
    with http(freelance) as c:
        assert expect(c.get(f"/projects/{project}"), 200).get("code") == VERDANE_PROJECT
    with http(admin) as c:
        assert c.delete(f"/grants/{grant['id']}").status_code == 204
    with http(freelance) as c:
        refusal(c.get(f"/projects/{project}"), 404, "not_found")


def _institut_contract(token: str) -> dict:
    return contract_by_reference(token, org_id(token, "institut-lumiere"), INSTITUT_CONTRACT)


def _raise_change_order(pm: str, contract: str, delta: int, submit: bool = True) -> dict:
    with http(pm) as c:
        order = expect(c.post(f"/contracts/{contract}/change-orders",
                              json={"reason": uid("Scope change"), "delta_value_minor": delta}), 201)
        if submit:
            submitted = expect(c.post(f"/change-orders/{order['id']}/submit"), 200)
            assert submitted.get("status") == "client_review", submitted
    return order


def test_concurrent_change_order_approvals_value_stored_sum():
    pm = token_for(PM)
    contract = _institut_contract(pm)
    before = get_json(pm, f"/contracts/{contract['id']}")
    deltas = [50000, 70000, -20000, 10000]
    orders = [_raise_change_order(pm, contract["id"], d) for d in deltas]
    owner = token_for(INSTITUT_OWNER)
    responses = run_together([
        (owner, None, lambda c, o=o: c.post(f"/change-orders/{o['id']}/decision",
                                             json={"decision": "approved", "comment": "Agreed"}))
        for o in orders])
    assert all(expect(r, 200).get("status") == "approved" for r in responses)
    after = get_json(pm, f"/contracts/{contract['id']}")
    assert after.get("original_value_minor") == before.get("original_value_minor"), after
    assert after.get("value_minor") == before["value_minor"] + sum(deltas), (
        f"simultaneous approvals lost a delta: {before['value_minor']} + {sum(deltas)} became {after.get('value_minor')}")
    stored = admin_db().query("SELECT value_minor FROM contracts WHERE reference = %s", (INSTITUT_CONTRACT,))
    assert stored and stored[0]["value_minor"] == after["value_minor"], stored


def test_change_order_decision_outside_review_conflict():
    pm = token_for(PM)
    order = _raise_change_order(pm, _institut_contract(pm)["id"], 15000, submit=False)
    with http(token_for(INSTITUT_OWNER)) as c:
        refusal(c.post(f"/change-orders/{order['id']}/decision",
                       json={"decision": "approved", "comment": "Agreed"}), 409, "change_order_not_in_review")


def test_project_manager_cannot_decide_change_order():
    pm = token_for(PM)
    contract = _institut_contract(pm)
    before = get_json(pm, f"/contracts/{contract['id']}")["value_minor"]
    order = _raise_change_order(pm, contract["id"], 25000)
    with http(pm) as c:
        refusal(c.post(f"/change-orders/{order['id']}/decision",
                       json={"decision": "approved", "comment": "Self approval"}), 403, "forbidden")
    assert get_json(pm, f"/contracts/{contract['id']}")["value_minor"] == before


def test_rejected_change_order_leaves_value():
    pm = token_for(PM)
    contract = _institut_contract(pm)
    before = get_json(pm, f"/contracts/{contract['id']}")["value_minor"]
    order = _raise_change_order(pm, contract["id"], 90000)
    with http(token_for(INSTITUT_OWNER)) as c:
        decided = expect(c.post(f"/change-orders/{order['id']}/decision",
                                json={"decision": "rejected", "comment": "Out of budget"}), 200)
    assert decided.get("status") == "rejected", decided
    assert get_json(pm, f"/contracts/{contract['id']}")["value_minor"] == before


def test_concurrent_replayed_lead_one_row_one_confirmation_email():
    email = uid("replay") + "@example.com"
    payload = lead_body(email)
    key = uid("attempt")
    responses = run_together([(None, {"Idempotency-Key": key},
                               lambda c: c.post("/public/leads", json=payload)) for _ in range(3)])
    references = {expect(r, 202).get("reference") for r in responses}
    assert len(references) == 1 and None not in references, f"replays answered different leads: {references}"
    reference = references.pop()
    rows = lead_rows(email)
    assert len(rows) == 1 and rows[0]["reference"] == reference, f"replays stored {len(rows)} leads"
    subject = EN_LEAD_SUBJECT + reference
    assert len(wait_for_mail(email, subject)) >= 1, f"no confirmation email {subject!r}"
    settle(3.0)
    assert len(messages_to(email, subject)) == 1, "replays sent more than one confirmation"


def test_confirmation_email_from_routed_entity():
    french_company = uid("routed-fr") + "@example.com"
    reference = expect(post_lead(lead_body(french_company, site="en", country="FR"), uid("k")), 202)["reference"]
    rows = lead_rows(french_company)
    assert rows and rows[0]["entity"] == FRANCE, f"a French company on the English site routed to {rows}"
    mail = wait_for_mail(french_company, EN_LEAD_SUBJECT + reference)
    assert len(mail) == 1, f"expected one English confirmation for {reference}"
    assert mail[0].body.strip().startswith(FRANCE_NAME), mail[0].body[:120]
    german_company = uid("routed-de") + "@example.com"
    reference = expect(post_lead(lead_body(german_company, site="en", country="DE", phone="+4930123456"),
                                 uid("k")), 202)["reference"]
    assert lead_rows(german_company)[0]["entity"] == MALTA
    mail = wait_for_mail(german_company, EN_LEAD_SUBJECT + reference)
    assert len(mail) == 1 and mail[0].body.strip().startswith(MALTA_NAME), mail[:1]


def test_french_site_confirmation_subject():
    email = uid("devis") + "@example.com"
    reference = expect(post_lead(lead_body(email, site="fr", country="BE", phone="+3225551234"), uid("k")),
                       202)["reference"]
    assert lead_rows(email)[0]["entity"] == FRANCE
    mail = wait_for_mail(email, FR_LEAD_SUBJECT + reference)
    assert len(mail) == 1, [m.subject for m in messages_containing(email, reference)]
    assert mail[0].body.strip().startswith(FRANCE_NAME), mail[0].body[:120]


def test_idempotency_key_reuse_other_body_conflict():
    email = uid("reuse") + "@example.com"
    key = uid("attempt")
    expect(post_lead(lead_body(email), key), 202)
    refusal(post_lead(lead_body(email, message="A different brief entirely, sent again."), key),
            409, "idempotency_key_reused")
    refusal(post_lead(lead_body(uid("nokey") + "@example.com"), None), 422, "idempotency_key_required")
    assert len(lead_rows(email)) == 1


def test_honeypot_lead_stored_as_spam_no_email():
    email = uid("bot") + "@example.com"
    answered = expect(post_lead(lead_body(email, website="https://cheap-links.example.com"), uid("k")), 202)
    assert answered.get("reference"), answered
    rows = lead_rows(email)
    assert len(rows) == 1 and rows[0]["status"] == "spam", f"a filled decoy was stored as {rows}"
    settle(5.0)
    assert messages_containing(email, answered["reference"]) == [], "a spam lead was sent a confirmation"


def test_invalid_lead_fields_refused_nothing_stored():
    email = "not-an-email"
    payload = lead_body(email, consent=False, budget="band_huge")
    payload.pop("message")
    refused = expect(post_lead(payload, uid("k")), 422)
    errors = {(e.get("field"), e.get("code")) for e in refused.get("errors", [])}
    for expected in [("email", "invalid_email"), ("consent", "consent_required"),
                     ("budget", "invalid_choice"), ("message", "required")]:
        assert expected in errors, f"{expected} missing from {refused}"
    assert lead_rows(email) == []


def test_gclid_not_stored_without_marketing_consent_row():
    email = uid("noconsent") + "@example.com"
    expect(post_lead(lead_body(email, marketing_consent=False, gclid="Cj0KCQtest-declined"), uid("k")), 202)
    rows = lead_rows(email)
    assert len(rows) == 1 and rows[0]["gclid"] is None, f"a gclid was kept without marketing consent: {rows}"


def test_gclid_stored_with_marketing_consent():
    email = uid("consent") + "@example.com"
    expect(post_lead(lead_body(email, marketing_consent=True, gclid="Cj0KCQtest-granted"), uid("k")), 202)
    rows = lead_rows(email)
    assert len(rows) == 1 and rows[0]["gclid"] == "Cj0KCQtest-granted", rows


def _english_localisation(token: str, key: str) -> dict:
    entry = get_json(token, "/content/entries", key=key)
    for loc in entry.get("localisations", []):
        if loc.get("site") == "com":
            return loc
    raise AssertionError(f"entry {key} has no English localisation: {entry}")


def test_slug_change_old_path_permanent_redirect_stored_alias():
    pm = token_for(PM)
    loc = _english_localisation(pm, "case-study/office-forma")
    assert page("/work/office-forma/").status_code == 200
    new_slug = uid("office-forma-studio")
    with http(pm) as c:
        changed = expect(c.patch(f"/content/localisations/{loc['id']}",
                                 json={"slug": new_slug, "version": loc["version"]}), 200)
    assert changed.get("path") == f"/work/{new_slug}/", changed
    old = page("/work/office-forma/")
    assert old.status_code == 301 and location_path(old) == f"/work/{new_slug}/", (
        f"the old address answered {old.status_code} {old.headers.get('location')}")
    assert page(f"/work/{new_slug}/").status_code == 200


def test_stale_localisation_version_conflict():
    pm = token_for(PM)
    loc = _english_localisation(pm, "case-study/secora")
    with http(pm) as c:
        first = expect(c.patch(f"/content/localisations/{loc['id']}",
                               json={"slug": uid("secora"), "version": loc["version"]}), 200)
        stale = refusal(c.patch(f"/content/localisations/{loc['id']}",
                                json={"slug": uid("secora-other"), "version": loc["version"]}),
                        409, "version_conflict")
    assert stale.get("current_version") == first.get("version"), stale
    assert _english_localisation(pm, "case-study/secora").get("slug") == first.get("slug")


def test_legacy_addresses_redirect_permanently():
    expected = {"/project/verdane/": "/work/verdane/", "/projects/": "/work/",
                "/our-services/": "/services/", "/about-us/": "/about/", "/contact-us/": "/contact/",
                "/legal-mentions/": "/legal/", "/privacy-policy/": "/privacy/", "/work/verdane": "/work/verdane/"}
    for legacy, target in expected.items():
        answered = page(legacy)
        assert answered.status_code == 301 and location_path(answered) == target, (
            f"{legacy} answered {answered.status_code} to {answered.headers.get('location')}, expected 301 to {target}")


def test_hreflang_alternates_derived_from_siblings():
    shared = page("/work/bellamy-associes/")
    assert shared.status_code == 200, shared.status_code
    links = [l for l in link_tags(shared.text) if "alternate" in (l.get("rel") or "").lower() and l.get("hreflang")]
    hrefs = {l["hreflang"].lower(): l.get("href", "") for l in links}
    assert any(h.endswith("/fr/references/bellamy-associes/") for h in hrefs.values()), hrefs
    assert hrefs.get("x-default", "").endswith("/work/bellamy-associes/"), hrefs
    assert all(h.startswith("http") for h in hrefs.values()), f"alternate addresses must be absolute: {hrefs}"
    single = page("/work/verdane/")
    alternates = [l.get("href", "") for l in link_tags(single.text)
                  if "alternate" in (l.get("rel") or "").lower() and l.get("hreflang")]
    assert not any("/fr/" in h for h in alternates), f"a single-language case study claims a French sibling: {alternates}"
    assert any(h.endswith("/work/verdane/") for h in alternates), alternates


def _sitemap_locations() -> list[str]:
    root = page("/sitemap.xml")
    assert root.status_code == 200, root.status_code
    locations = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", root.text)
    if "<sitemapindex" in root.text:
        children = locations
        locations = []
        for child in children:
            answered = page(httpx.URL(child).path)
            assert answered.status_code == 200, child
            locations += re.findall(r"<loc>\s*([^<]+?)\s*</loc>", answered.text)
    return locations


def test_below_threshold_landing_noindex_excluded_from_sitemap():
    thin = {"/fr/agence-seo-paris/": True, "/fr/agence-ux-design-paris/": True,
            "/fr/agence-seo-lyon/": False, "/fr/agence-web-site-internet-lyon/": False}
    for path, noindex in thin.items():
        answered = page(path)
        assert answered.status_code == 200, f"{path} answered {answered.status_code}"
        flagged = any("noindex" in value for value in meta_robots(answered.text))
        assert flagged == noindex, f"{path} noindex={flagged}, expected {noindex}"
    paths = {httpx.URL(loc).path for loc in _sitemap_locations()}
    assert "/fr/agence-seo-lyon/" in paths and "/fr/agence-web-site-internet-lyon/" in paths, sorted(paths)[:20]
    assert "/fr/agence-seo-paris/" not in paths and "/fr/agence-ux-design-paris/" not in paths, "noindex pages in the sitemap"
    assert "/work/verdane/" in paths, sorted(paths)[:20]
    assert not any(p.startswith("/portal") or p.startswith("/api") for p in paths), sorted(paths)


def test_robots_disallows_portal_api_names_sitemap():
    answered = page("/robots.txt")
    assert answered.status_code == 200, answered.status_code
    lines = [line.strip().lower() for line in answered.text.splitlines()]
    assert any(re.fullmatch(r"disallow:\s*/portal/?", line) for line in lines), answered.text
    assert any(re.fullmatch(r"disallow:\s*/api/?", line) for line in lines), answered.text
    assert any(line.startswith("sitemap:") and "sitemap.xml" in line for line in lines), answered.text


def test_favicon_linked_and_served():
    for path in ("/", "/fr/", "/work/verdane/"):
        icons = [l for l in link_tags(page(path).text) if "icon" in (l.get("rel") or "").lower().split()]
        assert any(l.get("href", "").endswith("/favicon.ico") for l in icons), f"{path} links no /favicon.ico"
    icon = page("/favicon.ico")
    assert icon.status_code == 200 and icon.headers.get("content-type", "").startswith("image/"), (
        icon.status_code, icon.headers.get("content-type"))


def test_privacy_pages_linked_from_footers():
    pairs = {"/": "/privacy/", "/work/verdane/": "/privacy/", "/fr/": "/fr/confidentialite/"}
    for path, target in pairs.items():
        footers = re.findall(r"<footer\b.*?</footer>", page(path).text, flags=re.I | re.S)
        assert footers and any(re.search(rf'href\s*=\s*["\'](?:https?://[^"\']+)?{re.escape(target)}["\']', f)
                               for f in footers), f"{path} footer links no {target}"
    for path, heading in (("/privacy/", "Privacy policy"), ("/fr/confidentialite/", "Politique de confidentialité")):
        answered = page(path)
        assert answered.status_code == 200, path
        h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", answered.text, flags=re.I | re.S)
        assert [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in h1] == [heading], f"{path} h1 is {h1}"


def test_served_assets_hold_no_secret_access_values():
    forbidden = list(SECRET_VALUES.values()) + [CLIENT_SECRET, DB_PASSWORD]
    seen, leaks = set(), []
    for path in ("/", "/fr/", "/start-a-project/", "/portal/login", "/portal", "/portal/agency/vault"):
        answered = page(path)
        documents = [(path, answered.text)]
        for asset in asset_paths(answered.text)[:40]:
            if asset in seen:
                continue
            seen.add(asset)
            documents.append((asset, page(asset).text))
        for where, text in documents:
            leaks += [f"{where} carries {value}" for value in forbidden if value in text]
    assert not leaks, f"a served document exposes a secret: {leaks}"


def test_home_page_skip_links_first_images_carry_alt():
    home = page("/")
    assert home.status_code == 200, home.status_code
    text = home.text
    focusable = []
    for match in re.finditer(r"<(a|button|input|select|textarea)\b[^>]*>", text, flags=re.I):
        tag, raw = match.group(1).lower(), match.group(0)
        if tag == "a":
            closing = text.find("</a>", match.end())
            raw = raw + html.unescape(re.sub(r"<[^>]+>", "", text[match.end():closing]))
        if re.search(r'tabindex\s*=\s*["\']-1["\']', raw) or re.search(r'type\s*=\s*["\']hidden["\']', raw, flags=re.I):
            continue
        if tag == "a" and not re.search(r"\bhref\s*=", raw, flags=re.I):
            continue
        focusable.append((tag, raw))
    assert focusable, "the home page offers no focusable element"
    first_tag, first_raw = focusable[0]
    assert first_tag == "a" and re.search(r'href\s*=\s*["\']#', first_raw), (
        f"the first focusable element is {first_raw[:160]!r}, expected a skip to content link")
    assert re.search(r"skip", first_raw, flags=re.I) and "Skip visual gallery" not in first_raw, (
        f"the first focusable element is {first_raw[:160]!r}, expected a skip to content link")
    gallery_skip, gallery = text.find("Skip visual gallery"), text.find("Our projects")
    assert gallery >= 0, "the home page carries no Our projects gallery heading"
    assert 0 <= gallery_skip < gallery, "no skip link precedes the pinned project gallery"
    images = re.findall(r"<img\b[^>]*>", text, flags=re.I)
    assert images, "the home page serves no real img element"
    missing = [img[:120] for img in images if not re.search(r"\balt\s*=", img, flags=re.I)]
    assert not missing, f"images without alt text: {missing[:3]}"
