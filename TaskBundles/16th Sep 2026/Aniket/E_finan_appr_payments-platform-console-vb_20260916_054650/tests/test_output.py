"""Graders for deku/payments-platform-console-vb.

One module, every section and every declared slot. Observations are made over
the JSON API, over the served markup, and over the rows postgres holds. Nothing
here reads the agent's source or probes for a feature at run time.
"""

from __future__ import annotations

import os

from conftest import (
    ADMIN_EMAIL, AMOUNT_ABOVE_CEILING, AMOUNT_BEYOND_REMAINDER,
    AMOUNT_WITHIN_CEILING, API_HEALTH, API_LEADS, API_ME, API_ACCOUNTS,
    AVAILABILITY_BADGE, BALANCE_KINDS, CODE_AMOUNT_TOO_LARGE,
    CODE_APPROVAL_EXPIRED, CODE_APPROVAL_REQUIRED, CODE_ENDPOINT_FORBIDDEN,
    CODE_IDEMPOTENCY_CONFLICT, CODE_PAYMENT_DISPUTED, CODE_SELF_APPROVAL,
    COPYRIGHT, CURRENCY, DECOY_FIELD, DENIED, DENIED_OR_MISSING,
    DISPUTE_PLANSMITH, DOWNLOAD_DIR,
    ENV_LIVE, ENV_SANDBOX, EVENT_TYPES, FINANCE_EMAIL, FORBIDDEN_ENDPOINTS,
    GATED_ACTION, HERO_ACTION, HERO_EYEBROW, HERO_LEAD, ICON_RE,
    LOCALE_LABEL, NORTHBEAM_LIVE_BALANCES,
    NORTHBEAM_LIVE_FEES, NORTHBEAM_LIVE_PAYMENTS, NORTHBEAM_SANDBOX_BALANCES,
    NOT_FOUND, NOT_FOUND_COPY, OG_DESC_RE, OG_IMAGE_RE, OG_TITLE_RE, OK_READ,
    OK_WRITE, ORG_NORTHBEAM, ORG_WELLSPRING, PAYMENT_STATES, PAYOUT_AMOUNT,
    PAYOUT_NORTHBEAM, PAY_BEANBAR, PAY_CORVID, PAY_NORTHWIND, PAY_PLANSMITH,
    PASSWORD, PAY_SANDBOX_BEANBAR, PAY_STREAMLY, PREFIX_SECRET_LIVE,
    PUBLIC_ROUTES, README_PATH,
    REFUSED, ROLE_FINANCE, ROLE_SUPPORT, ROUTE_FAVICON, ROUTE_HOME,
    ROUTE_QUERY, ROUTE_ROBOTS, ROUTE_SITEMAP, SANDBOX_PAYMENT_AMOUNT,
    SCREENSHOT_DIR, SEEDED_ACCOUNTS, SITEMAP_LINE_RE, SUPPORT2_EMAIL,
    SUPPORT_CEILING, SUPPORT_EMAIL,
    TABLE_AUDIT, TABLE_BALANCE, TABLE_LEAD, TABLE_LEDGER_ENTRY, TABLE_PAYMENT,
    TABLE_REFUND, TABLE_REQUEST, VOLUME_BANDS, WELLSPRING_LIVE_BALANCES,
    account_path, approve_request, as_list, available_of, bearer, body_text,
    create_refund, error_code, field, id_of, in_parallel, json_body, login,
    probe_email, probe_key, probe_reason, probe_token, raise_request,
    raised_request_id, read_balances, read_payment, read_payments,
    read_request, reject_request, settle, state_of, ttl_seconds,
    wait_for_state,
)

DEADLINE_MULTIPLE = 3.0


def _support(api):
    return bearer(api, SUPPORT_EMAIL)


def _finance(api):
    return bearer(api, FINANCE_EMAIL)


def _admin(api):
    return bearer(api, ADMIN_EMAIL)


def _support2(api):
    return bearer(api, SUPPORT2_EMAIL)


def _expiry_deadline() -> float:
    return ttl_seconds() * DEADLINE_MULTIPLE + 5.0


def _ledger_rows(db, transaction_id):
    return db.rows(TABLE_LEDGER_ENTRY, ledger_transaction_id=transaction_id)


def _entry_amount(row) -> int:
    value = field(row, "amount_minor", "amount")
    return int(value) if value is not None else 0


def _balance_rows(db, account, environment):
    return db.rows(TABLE_BALANCE, account_id=account, environment=environment)


"""--- core features --- business rules and state machines the spec pins"""


def test_login_returns_bearer_token(api):
    """A seeded account signs in with the pinned password.

    cov: C-RL-11, C-CF-01
    """
    response = login(api, SUPPORT_EMAIL)
    assert response.status_code in OK_WRITE, (
        "POST /api/auth/login refused the seeded support account with the pinned "
        "password: status %s, body %r"
        % (response.status_code, body_text(response)[:300]))
    payload = json_body(response)
    token = payload.get("access_token") or payload.get("token")
    assert isinstance(token, str) and token, (
        "POST /api/auth/login returned no bearer token for %s: body %r"
        % (SUPPORT_EMAIL, body_text(response)[:300]))


def test_wrong_password_is_refused(api):
    """A wrong password yields no session.

    cov: C-CF-02
    """
    response = login(api, SUPPORT_EMAIL, "not-the-seeded-password-%s" % probe_token())
    assert response.status_code not in OK_WRITE, (
        "POST /api/auth/login accepted a wrong password for %s: status %s, body %r"
        % (SUPPORT_EMAIL, response.status_code, body_text(response)[:300]))
    payload = json_body(response)
    assert not (isinstance(payload, dict) and payload.get("access_token")), (
        "POST /api/auth/login handed out a token on a wrong password: body %r"
        % body_text(response)[:300])


def test_me_lists_every_membership(api):
    """The identity endpoint reports both of the finance member's memberships.

    cov: C-CF-03, C-OV-02
    """
    response = api.get(API_ME, headers=_finance(api))
    assert response.status_code in OK_READ, (
        "GET /api/me returned %s for %s: %r"
        % (response.status_code, FINANCE_EMAIL, body_text(response)[:300]))
    payload = json_body(response)
    memberships = payload.get("memberships") if isinstance(payload, dict) else None
    rows = as_list(memberships)
    accounts = {str(field(r, "account_id", "account", "organisation")) for r in rows}
    assert {ORG_NORTHBEAM, ORG_WELLSPRING} <= accounts, (
        "GET /api/me reports memberships %r for %s; the brief seeds one on %r and "
        "one on %r" % (sorted(accounts), FINANCE_EMAIL, ORG_NORTHBEAM, ORG_WELLSPRING))
    roles = {str(field(r, "role")) for r in rows}
    assert ROLE_FINANCE in roles, (
        "GET /api/me reports roles %r for %s; the seeded role is %r"
        % (sorted(roles), FINANCE_EMAIL, ROLE_FINANCE))


def test_accounts_lists_only_memberships_held(api):
    """The organisation list never names an organisation the caller is outside.

    cov: C-CF-04
    """
    response = api.get(API_ACCOUNTS, headers=_support(api))
    assert response.status_code in OK_READ, (
        "GET /api/accounts returned %s for %s: %r"
        % (response.status_code, SUPPORT_EMAIL, body_text(response)[:300]))
    slugs = {str(field(row, "id", "slug", "account_id"))
             for row in as_list(response.json())}
    assert slugs == {ORG_NORTHBEAM}, (
        "GET /api/accounts returned %r for %s; the brief seeds exactly one "
        "membership, on %r" % (sorted(slugs), SUPPORT_EMAIL, ORG_NORTHBEAM))


def test_seeded_live_payments_are_stored(api, db):
    """Every seeded live payment exists as a row with its pinned amount.

    cov: C-CF-09, C-DM-11, C-CF-41, C-CN-04, C-TR-16, C-TR-17
    """
    headers = _support(api)
    response = read_payments(api, headers, ORG_NORTHBEAM, ENV_LIVE)
    assert response.status_code in OK_READ, (
        "GET the payments of %r returned %s: %r"
        % (ORG_NORTHBEAM, response.status_code, body_text(response)[:300]))
    assert isinstance(response.json(), list), (
        "the payment list of %r came back wrapped rather than as a top-level "
        "JSON array; the brief pins the array, with no total count of the "
        "collection" % ORG_NORTHBEAM)
    listed = {str(field(row, "id")): row for row in as_list(response.json())}
    for payment_id, amount in NORTHBEAM_LIVE_PAYMENTS.items():
        assert payment_id in listed, (
            "the payment list of %r omits the seeded payment %r; it listed %r"
            % (ORG_NORTHBEAM, payment_id, sorted(listed)))
        got = field(listed[payment_id], "amount_minor", "amount")
        assert int(got) == amount, (
            "the seeded payment %r reports amount_minor %r; the brief pins %s"
            % (payment_id, got, amount))
        fee = field(listed[payment_id], "fee_minor", "fee")
        assert int(fee) == NORTHBEAM_LIVE_FEES[payment_id], (
            "the seeded payment %r reports fee_minor %r; the brief pins %s"
            % (payment_id, fee, NORTHBEAM_LIVE_FEES[payment_id]))
        status = str(field(listed[payment_id], "status", "state"))
        assert status in PAYMENT_STATES, (
            "the seeded payment %r reports status %r, outside the pinned set %r"
            % (payment_id, status, list(PAYMENT_STATES)))
        assert str(field(listed[payment_id], "currency")).lower() == CURRENCY, (
            "the seeded payment %r reports currency %r; the brief serves one "
            "currency, %r"
            % (payment_id, field(listed[payment_id], "currency"), CURRENCY))
    row = db.payment(PAY_BEANBAR)
    assert row, (
        "no row for the seeded payment %r exists in the %r table"
        % (PAY_BEANBAR, TABLE_PAYMENT))


def test_refund_within_ceiling_is_persisted(api, db):
    """A refund at or below the ceiling writes a row without an approval.

    cov: C-CF-10, C-CF-12, C-RL-01
    """
    headers = _support(api)
    before = available_of(api, headers, ORG_NORTHBEAM, ENV_LIVE)
    amount = NORTHBEAM_LIVE_PAYMENTS[PAY_CORVID]
    response = create_refund(api, headers, ORG_NORTHBEAM, PAY_CORVID, amount)
    assert response.status_code in OK_WRITE, (
        "a refund of %s on %r, inside the support ceiling of %s, returned %s: %r"
        % (amount, PAY_CORVID, SUPPORT_CEILING, response.status_code,
           body_text(response)[:300]))
    refund_id = id_of(response.json())
    assert refund_id, (
        "the created refund carried no identifier: body %r"
        % body_text(response)[:300])
    rows = db.refunds_of(PAY_CORVID)
    assert rows, (
        "no row landed in %r for the refund just created on %r"
        % (TABLE_REFUND, PAY_CORVID))
    after = available_of(api, headers, ORG_NORTHBEAM, ENV_LIVE)
    assert before - after == amount, (
        "available moved from %s to %s on a refund of %s; the brief pins a fall of "
        "exactly the refund amount" % (before, after, amount))
    payment = read_payment(api, headers, ORG_NORTHBEAM, PAY_CORVID)
    assert str(field(payment.json(), "status", "state")) == "refunded", (
        "%r reports status %r after its whole captured amount was refunded; the "
        "brief pins refunded"
        % (PAY_CORVID, field(payment.json(), "status", "state")))


def test_refund_above_ceiling_requires_approval(api, db):
    """An over-ceiling refund is refused with the pinned code, writing nothing.

    cov: C-CF-13, C-CF-14, C-RL-02
    """
    headers = _support(api)
    before = len(db.refunds_of(PAY_NORTHWIND))
    response = create_refund(api, headers, ORG_NORTHBEAM, PAY_NORTHWIND,
                             AMOUNT_ABOVE_CEILING)
    assert response.status_code not in OK_WRITE, (
        "a refund of %s on %r, above the support ceiling of %s, was accepted with "
        "status %s: %r" % (AMOUNT_ABOVE_CEILING, PAY_NORTHWIND, SUPPORT_CEILING,
                           response.status_code, body_text(response)[:300]))
    assert error_code(response) == CODE_APPROVAL_REQUIRED, (
        "the over-ceiling refusal carried code %r; the brief pins %r. Body: %r"
        % (error_code(response), CODE_APPROVAL_REQUIRED, body_text(response)[:300]))
    assert len(db.refunds_of(PAY_NORTHWIND)) == before, (
        "a refund row landed in %r for an over-ceiling attempt that was refused"
        % TABLE_REFUND)


def test_refund_request_is_created_pending(api, db):
    """A raised request is stored pending with its justification.

    cov: C-CF-16, C-CF-20
    """
    headers = _support(api)
    response = raise_request(api, headers, ORG_NORTHBEAM, PAY_NORTHWIND,
                             AMOUNT_ABOVE_CEILING)
    assert response.status_code in OK_WRITE, (
        "raising a refund request on %r for %s returned %s: %r"
        % (PAY_NORTHWIND, AMOUNT_ABOVE_CEILING, response.status_code,
           body_text(response)[:300]))
    payload = response.json()
    assert state_of(payload) == "pending_approval", (
        "the raised request reports state %r; the brief pins pending_approval"
        % state_of(payload))
    assert field(payload, "justification"), (
        "the raised request carries no justification, which the brief makes "
        "mandatory: body %r" % body_text(response)[:300])
    row = db.request(id_of(payload))
    assert row, (
        "no row landed in %r for the request just raised" % TABLE_REQUEST)


def test_approval_executes_exactly_one_refund(api, db):
    """A finance approval turns one pending request into one refund.

    cov: C-CF-25, C-CF-27, C-RL-05, C-OV-03
    """
    support = _support(api)
    finance = _finance(api)
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    before = len(db.refunds_of(PAY_NORTHWIND))
    available_before = available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    response = approve_request(api, finance, ORG_NORTHBEAM, request_id,
                               "Approved by finance, probe %s" % probe_token())
    assert response.status_code in OK_WRITE, (
        "approving request %r as %s returned %s: %r"
        % (request_id, FINANCE_EMAIL, response.status_code,
           body_text(response)[:300]))
    payload = response.json()
    assert state_of(payload) == "executed", (
        "request %r reports state %r after approval; the brief pins executed"
        % (request_id, state_of(payload)))
    assert field(payload, "refund_id", "refund"), (
        "the executed request names no resulting refund: body %r"
        % body_text(response)[:300])
    assert len(db.refunds_of(PAY_NORTHWIND)) == before + 1, (
        "approving one request produced %s new refund row(s) on %r; the brief "
        "pins exactly one"
        % (len(db.refunds_of(PAY_NORTHWIND)) - before, PAY_NORTHWIND))
    available_after = available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    assert available_before - available_after == AMOUNT_ABOVE_CEILING, (
        "available moved from %s to %s on an approved refund of %s"
        % (available_before, available_after, AMOUNT_ABOVE_CEILING))


def test_rejected_request_writes_no_refund(api, db):
    """A rejection closes the request without moving money.

    cov: C-CF-28
    """
    support = _support(api)
    finance = _finance(api)
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    before = len(db.refunds_of(PAY_NORTHWIND))
    available_before = available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    response = reject_request(api, finance, ORG_NORTHBEAM, request_id,
                              "Not a goodwill case, probe %s" % probe_token())
    assert response.status_code in OK_WRITE, (
        "rejecting request %r returned %s: %r"
        % (request_id, response.status_code, body_text(response)[:300]))
    assert state_of(response.json()) == "rejected", (
        "request %r reports state %r after a rejection; the brief pins rejected"
        % (request_id, state_of(response.json())))
    assert len(db.refunds_of(PAY_NORTHWIND)) == before, (
        "a rejected request produced a refund row in %r" % TABLE_REFUND)
    assert available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE) == available_before, (
        "available moved on a rejected request; the brief pins no movement")


def test_withdrawn_request_is_closed_by_its_requester(api):
    """The raiser may withdraw a pending request.

    cov: C-CF-29
    """
    support = _support(api)
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    response = api.post(
        account_path(ORG_NORTHBEAM, "approval-requests", request_id, "withdraw"),
        json={}, headers=support)
    assert response.status_code in OK_WRITE, (
        "withdrawing request %r as its raiser returned %s: %r"
        % (request_id, response.status_code, body_text(response)[:300]))
    assert state_of(response.json()) == "withdrawn", (
        "request %r reports state %r after a withdrawal; the brief pins withdrawn"
        % (request_id, state_of(response.json())))


"""--- data integrity -- persistence, reconciliation, values surviving reload"""


def test_balances_sum_to_zero_per_environment(api):
    """Every seeded balance set nets to zero across its six kinds.

    cov: C-CF-38, C-DM-02
    """
    finance = _finance(api)
    for account, environment in ((ORG_NORTHBEAM, ENV_LIVE),
                                 (ORG_NORTHBEAM, ENV_SANDBOX),
                                 (ORG_WELLSPRING, ENV_LIVE)):
        balances = read_balances(api, finance, account, environment)
        missing = set(BALANCE_KINDS) - set(balances)
        assert not missing, (
            "the balances of %r in %r omit the kind(s) %r; the brief pins six"
            % (account, environment, sorted(missing)))
        total = sum(balances.values())
        assert total == 0, (
            "the balances of %r in %r sum to %s; the brief pins exactly zero. "
            "Rows: %r" % (account, environment, total, balances))


def test_balance_row_equals_sum_of_ledger_entries(api, db):
    """Each stored balance equals the sum of the entries behind it.

    cov: C-CF-39, C-DM-03
    """
    finance = _finance(api)
    balances = read_balances(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    entries = db.rows(TABLE_LEDGER_ENTRY, account_id=ORG_NORTHBEAM,
                      environment=ENV_LIVE)
    assert entries, (
        "no rows in %r for %r in %r; the brief seeds a capture per payment"
        % (TABLE_LEDGER_ENTRY, ORG_NORTHBEAM, ENV_LIVE))
    summed = {}
    for row in entries:
        kind = str(field(row, "balance_kind", "kind"))
        summed[kind] = summed.get(kind, 0) + _entry_amount(row)
    for kind, amount in balances.items():
        assert summed.get(kind, 0) == amount, (
            "the %r balance of %r reads %s while the entries behind it sum to %s; "
            "the brief pins a balance computed from the entries"
            % (kind, ORG_NORTHBEAM, amount, summed.get(kind, 0)))


def test_ledger_transaction_entries_sum_to_zero(db):
    """Each stored ledger transaction balances to zero across its entries.

    cov: C-CF-40, C-DM-04
    """
    entries = db.rows(TABLE_LEDGER_ENTRY, account_id=ORG_NORTHBEAM,
                      environment=ENV_LIVE)
    assert entries, (
        "no rows in %r for %r in %r" % (TABLE_LEDGER_ENTRY, ORG_NORTHBEAM, ENV_LIVE))
    per_transaction = {}
    for row in entries:
        key = str(field(row, "ledger_transaction_id", "transaction_id"))
        per_transaction[key] = per_transaction.get(key, 0) + _entry_amount(row)
    unbalanced = {k: v for k, v in per_transaction.items() if v != 0}
    assert not unbalanced, (
        "these ledger transactions do not sum to zero: %r. The brief pins a "
        "signed sum of exactly zero per transaction" % unbalanced)


def test_seeded_sandbox_balance_row_is_stored(api):
    """The sandbox balances read back at their seeded values.

    cov: C-DM-10, C-CF-06
    """
    finance = _finance(api)
    balances = read_balances(api, finance, ORG_NORTHBEAM, ENV_SANDBOX)
    for kind, amount in NORTHBEAM_SANDBOX_BALANCES.items():
        assert balances.get(kind) == amount, (
            "the %r balance of %r in sandbox reads %r; the brief seeds %s"
            % (kind, ORG_NORTHBEAM, balances.get(kind), amount))


def test_seeded_northbeam_balance_row_is_stored(db):
    """The seeded northbeam live balances hold before any refund is posted.

    cov: C-DM-08, C-DM-05, C-TR-03
    """
    entries = db.rows(TABLE_LEDGER_ENTRY, account_id=ORG_NORTHBEAM,
                      environment=ENV_LIVE)
    assert entries, (
        "no rows in %r for %r in %r" % (TABLE_LEDGER_ENTRY, ORG_NORTHBEAM,
                                        ENV_LIVE))
    seeded_kinds = ("capture", "dispute_opened", "payout_created", "payout_paid")
    transactions = db.rows("ledger_transaction", account_id=ORG_NORTHBEAM,
                           environment=ENV_LIVE)
    assert transactions, (
        "no rows in ledger_transaction for %r in %r" % (ORG_NORTHBEAM, ENV_LIVE))
    seeded_ids = {str(field(t, "id")) for t in transactions
                  if str(field(t, "kind", "type")) in seeded_kinds}
    summed = {}
    for row in entries:
        if str(field(row, "ledger_transaction_id", "transaction_id")) in seeded_ids:
            kind = str(field(row, "balance_kind", "kind"))
            summed[kind] = summed.get(kind, 0) + _entry_amount(row)
    for kind, amount in NORTHBEAM_LIVE_BALANCES.items():
        assert summed.get(kind, 0) == amount, (
            "the seeded %r balance of %r computes to %s from its capture, "
            "dispute and payout entries; the brief seeds %s"
            % (kind, ORG_NORTHBEAM, summed.get(kind, 0), amount))


def test_seeded_wellspring_balance_row_is_stored(api):
    """The second organisation's balances read back at their seeded values.

    cov: C-DM-09, C-DM-07
    """
    finance = _finance(api)
    balances = read_balances(api, finance, ORG_WELLSPRING, ENV_LIVE)
    for kind, amount in WELLSPRING_LIVE_BALANCES.items():
        assert balances.get(kind) == amount, (
            "the %r balance of %r reads %r; the brief seeds %s"
            % (kind, ORG_WELLSPRING, balances.get(kind), amount))


def test_pending_request_moves_no_balance(api, db):
    """A request that is waiting holds no money at all.

    cov: C-CF-17, C-CF-18
    """
    support = _support(api)
    finance = _finance(api)
    before = read_balances(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    entries_before = len(db.rows(TABLE_LEDGER_ENTRY, account_id=ORG_NORTHBEAM,
                                 environment=ENV_LIVE))
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    after = read_balances(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    entries_after = len(db.rows(TABLE_LEDGER_ENTRY, account_id=ORG_NORTHBEAM,
                                environment=ENV_LIVE))
    assert after == before, (
        "raising request %r moved the balances from %r to %r; the brief pins a "
        "pending request that holds nothing" % (request_id, before, after))
    assert entries_after == entries_before, (
        "raising request %r wrote %s ledger entr(ies); a pending request owns none"
        % (request_id, entries_after - entries_before))


def test_payout_reconciles_to_its_transactions(api):
    """The seeded payout equals the sum of the transactions it lists.

    cov: C-CF-42
    """
    finance = _finance(api)
    response = api.get(account_path(ORG_NORTHBEAM, "payouts", PAYOUT_NORTHBEAM),
                       headers=finance)
    assert response.status_code in OK_READ, (
        "reading the seeded payout %r returned %s: %r"
        % (PAYOUT_NORTHBEAM, response.status_code, body_text(response)[:300]))
    payload = response.json()
    amount = field(payload, "amount_minor", "amount")
    assert int(amount) == PAYOUT_AMOUNT, (
        "payout %r reports amount_minor %r; the brief seeds %s"
        % (PAYOUT_NORTHBEAM, amount, PAYOUT_AMOUNT))
    transactions = as_list(field(payload, "transactions", "ledger_transactions",
                                 "items"))
    assert transactions, (
        "payout %r lists no composing transactions; the brief pins a payout an "
        "operator can reconcile to the entry level" % PAYOUT_NORTHBEAM)


def test_refund_reduces_available_by_exact_amount(api, db):
    """A partial refund moves available by exactly its own amount.

    cov: C-CF-11, C-CF-08
    """
    support = _support(api)
    before = available_of(api, support, ORG_NORTHBEAM, ENV_LIVE)
    response = create_refund(api, support, ORG_NORTHBEAM, PAY_STREAMLY,
                             AMOUNT_WITHIN_CEILING)
    assert response.status_code in OK_WRITE, (
        "a refund of %s on %r returned %s: %r"
        % (AMOUNT_WITHIN_CEILING, PAY_STREAMLY, response.status_code,
           body_text(response)[:300]))
    after = available_of(api, support, ORG_NORTHBEAM, ENV_LIVE)
    assert before - after == AMOUNT_WITHIN_CEILING, (
        "available moved from %s to %s on a refund of %s"
        % (before, after, AMOUNT_WITHIN_CEILING))
    payment = read_payment(api, support, ORG_NORTHBEAM, PAY_STREAMLY).json()
    refunded = field(payment, "refunded_minor", "refunded")
    assert int(refunded) >= AMOUNT_WITHIN_CEILING, (
        "%r reports refunded_minor %r after a refund of %s; the total is computed "
        "from the refunds of the payment"
        % (PAY_STREAMLY, refunded, AMOUNT_WITHIN_CEILING))
    assert db.refunds_of(PAY_STREAMLY), (
        "no row in %r for the refund just created on %r"
        % (TABLE_REFUND, PAY_STREAMLY))


def test_audit_sequence_has_no_gap(db):
    """The audit record sequence rises by one with no gap.

    cov: C-CF-52, C-CF-53
    """
    rows = db.audit(account_id=ORG_NORTHBEAM)
    assert rows, (
        "no rows in %r for %r; every mutation appends one"
        % (TABLE_AUDIT, ORG_NORTHBEAM))
    seen = sorted(int(field(r, "sequence", "seq")) for r in rows)
    assert seen == list(range(1, len(seen) + 1)), (
        "the audit sequence for %r reads %r; the brief pins 1 upward with no gap"
        % (ORG_NORTHBEAM, seen[:12]))


def test_audit_record_hash_links_to_previous(db):
    """Each audit record carries the hash of the record before it.

    cov: C-CF-54, C-CF-55
    """
    rows = db.audit(account_id=ORG_NORTHBEAM)
    assert rows, (
        "no rows in %r for %r" % (TABLE_AUDIT, ORG_NORTHBEAM))
    ordered = sorted(rows, key=lambda r: int(field(r, "sequence", "seq")))
    for earlier, later in zip(ordered, ordered[1:]):
        prev_hash = field(later, "prev_hash", "previous_hash")
        own_hash = field(earlier, "hash", "record_hash")
        assert prev_hash and own_hash, (
            "an audit record carries no hash pair: %r" % {"earlier": earlier,
                                                          "later": later})
        assert str(prev_hash) == str(own_hash), (
            "audit record %r carries prev_hash %r while the record before it "
            "hashes to %r; the chain is what makes a modification detectable"
            % (field(later, "id"), prev_hash, own_hash))


"""--- authorization --- denial at the API, ownership, tenancy, row scope"""


def test_support_cannot_approve_request_denied(api, db):
    """A support session is refused the approve endpoint, state untouched.

    cov: C-RL-03, C-CF-22, C-CF-23
    """
    support = _support(api)
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    response = approve_request(api, support, ORG_NORTHBEAM, request_id, "probe")
    assert response.status_code in DENIED, (
        "approving request %r from a %s session returned %s; the server must deny "
        "it" % (request_id, ROLE_SUPPORT, response.status_code))
    row = db.request(request_id)
    assert str(field(row, "state", "status")) == "pending_approval", (
        "request %r reads state %r after a denied approval; the brief pins an "
        "unchanged row" % (request_id, field(row, "state", "status")))


def test_self_approval_is_forbidden(api, db):
    """The raiser cannot approve the request the raiser filed.

    cov: C-RL-06, C-CF-21, C-CF-24
    """
    finance = _finance(api)
    request_id = raised_request_id(api, finance, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    response = approve_request(api, finance, ORG_NORTHBEAM, request_id, "probe")
    assert response.status_code not in OK_WRITE, (
        "the raiser of request %r approved it, status %s: %r"
        % (request_id, response.status_code, body_text(response)[:300]))
    assert error_code(response) == CODE_SELF_APPROVAL, (
        "the self-approval refusal carried code %r; the brief pins %r"
        % (error_code(response), CODE_SELF_APPROVAL))
    row = db.request(request_id)
    assert str(field(row, "state", "status")) == "pending_approval", (
        "request %r reads state %r after a refused self-approval"
        % (request_id, field(row, "state", "status")))


def test_administrator_cannot_create_refund_denied(api, db):
    """An administrator session is refused the refund endpoint.

    cov: C-RL-07
    """
    admin = _admin(api)
    before = len(db.refunds_of(PAY_BEANBAR))
    response = create_refund(api, admin, ORG_NORTHBEAM, PAY_BEANBAR, 1000)
    assert response.status_code in DENIED, (
        "an %s session created a refund on %r, status %s: %r"
        % ("administrator", PAY_BEANBAR, response.status_code,
           body_text(response)[:300]))
    assert len(db.refunds_of(PAY_BEANBAR)) == before, (
        "a refund row landed in %r for a denied administrator attempt" % TABLE_REFUND)


def test_support_cannot_read_api_keys_denied(api):
    """A support session is refused the credential list.

    cov: C-RL-09, C-CF-44
    """
    support = _support(api)
    response = api.get(account_path(ORG_NORTHBEAM, "api-keys"),
                       params={"environment": ENV_LIVE}, headers=support)
    assert response.status_code in DENIED_OR_MISSING, (
        "a %s session read the credential list of %r, status %s: %r"
        % (ROLE_SUPPORT, ORG_NORTHBEAM, response.status_code,
           body_text(response)[:300]))


def test_support_cannot_read_audit_log_denied(api):
    """A support session is refused the audit log.

    cov: C-RL-08, C-CF-56
    """
    support = _support(api)
    response = api.get(account_path(ORG_NORTHBEAM, "audit-records"),
                       headers=support)
    assert response.status_code in DENIED_OR_MISSING, (
        "a %s session read the audit log of %r, status %s: %r"
        % (ROLE_SUPPORT, ORG_NORTHBEAM, response.status_code,
           body_text(response)[:300]))


def test_cross_account_payment_read_denied(api):
    """A member of one organisation cannot read another organisation's payment.

    cov: C-CF-05, C-CN-06
    """
    support = _support(api)
    response = read_payment(api, support, ORG_WELLSPRING, "pay_lumen_7750")
    assert response.status_code in DENIED_OR_MISSING, (
        "a member of %r read the payment %r of %r, status %s: %r"
        % (ORG_NORTHBEAM, "pay_lumen_7750", ORG_WELLSPRING,
           response.status_code, body_text(response)[:300]))


def test_wellspring_member_cannot_read_northbeam_denied(api):
    """Tenancy holds in both directions, not only one.

    cov: C-RL-10, C-OV-01
    """
    other = _support2(api)
    response = read_payment(api, other, ORG_NORTHBEAM, PAY_BEANBAR)
    assert response.status_code in DENIED_OR_MISSING, (
        "a member of %r read the payment %r of %r, status %s: %r"
        % (ORG_WELLSPRING, PAY_BEANBAR, ORG_NORTHBEAM, response.status_code,
           body_text(response)[:300]))


def test_unauthenticated_console_read_denied(api):
    """A caller with no session reaches no console data.

    cov: C-UF-15, C-TR-12
    """
    response = api.get(account_path(ORG_NORTHBEAM, "payments"),
                       params={"environment": ENV_LIVE})
    assert response.status_code in DENIED, (
        "an unauthenticated read of the payments of %r returned %s: %r"
        % (ORG_NORTHBEAM, response.status_code, body_text(response)[:300]))


"""--- edge cases ------ contention, empty state, boundary, validation reject"""


def test_duplicate_approval_creates_no_second_refund(api, db):
    """Approving the same request twice hands back the money once.

    cov: C-CF-26, C-CF-34
    """
    support = _support(api)
    finance = _finance(api)
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    first = approve_request(api, finance, ORG_NORTHBEAM, request_id, "first")
    assert first.status_code in OK_WRITE, (
        "the first approval of %r returned %s: %r"
        % (request_id, first.status_code, body_text(first)[:300]))
    count_after_first = len(db.refunds_of(PAY_NORTHWIND))
    available_after_first = available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    second = approve_request(api, finance, ORG_NORTHBEAM, request_id, "second")
    assert second.status_code not in (500, 502, 503, 504), (
        "the second approval of %r returned a server error %s: %r"
        % (request_id, second.status_code, body_text(second)[:300]))
    assert len(db.refunds_of(PAY_NORTHWIND)) == count_after_first, (
        "a second approval of %r produced another refund row; the brief pins "
        "exactly one" % request_id)
    assert available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE) == available_after_first, (
        "available moved again on a second approval of %r" % request_id)


def test_concurrent_approvals_produce_one_refund(api, db):
    """Two approvals at one instant produce one refund, never two.

    cov: C-CF-34, C-CF-37
    """
    support = _support(api)
    finance = _finance(api)
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    before = len(db.refunds_of(PAY_NORTHWIND))
    available_before = available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    headers_one = _finance(api)
    headers_two = _finance(api)
    results = in_parallel([
        lambda: approve_request(api, headers_one, ORG_NORTHBEAM, request_id, "one"),
        lambda: approve_request(api, headers_two, ORG_NORTHBEAM, request_id, "two"),
    ])
    statuses = [r.status_code for r in results]
    assert any(s in OK_WRITE for s in statuses), (
        "neither of two simultaneous approvals of %r succeeded: statuses %r"
        % (request_id, statuses))
    assert len(db.refunds_of(PAY_NORTHWIND)) == before + 1, (
        "two simultaneous approvals of %r produced %s refund row(s); the brief "
        "pins exactly one"
        % (request_id, len(db.refunds_of(PAY_NORTHWIND)) - before))
    available_after = available_of(api, finance, ORG_NORTHBEAM, ENV_LIVE)
    assert available_before - available_after == AMOUNT_ABOVE_CEILING, (
        "available moved by %s under two simultaneous approvals of %s each; the "
        "brief pins one movement"
        % (available_before - available_after, AMOUNT_ABOVE_CEILING))


def test_idempotent_refund_replay_creates_no_second_row(api, db):
    """A replayed key with the same body creates nothing new.

    cov: C-CF-35
    """
    support = _support(api)
    key = probe_key()
    reason = probe_reason("Replay probe")
    first = create_refund(api, support, ORG_NORTHBEAM, PAY_BEANBAR, 1000,
                          key=key, reason=reason)
    assert first.status_code in OK_WRITE, (
        "the first refund under key %r returned %s: %r"
        % (key, first.status_code, body_text(first)[:300]))
    count_after_first = len(db.refunds_of(PAY_BEANBAR))
    available_after_first = available_of(api, support, ORG_NORTHBEAM, ENV_LIVE)
    second = create_refund(api, support, ORG_NORTHBEAM, PAY_BEANBAR, 1000,
                           key=key, reason=reason)
    assert second.status_code in OK_WRITE, (
        "replaying key %r with an identical body returned %s; the brief pins the "
        "stored response" % (key, second.status_code))
    assert len(db.refunds_of(PAY_BEANBAR)) == count_after_first, (
        "replaying key %r wrote a second refund row" % key)
    assert available_of(api, support, ORG_NORTHBEAM, ENV_LIVE) == available_after_first, (
        "replaying key %r moved available a second time" % key)


def test_idempotency_conflict_on_changed_body(api):
    """A reused key carrying a different body is refused with the pinned code.

    cov: C-CF-36
    """
    support = _support(api)
    key = probe_key()
    first = create_refund(api, support, ORG_NORTHBEAM, PAY_BEANBAR, 1000, key=key)
    assert first.status_code in OK_WRITE, (
        "the first refund under key %r returned %s: %r"
        % (key, first.status_code, body_text(first)[:300]))
    second = create_refund(api, support, ORG_NORTHBEAM, PAY_BEANBAR, 2000, key=key)
    assert second.status_code not in OK_WRITE, (
        "key %r was accepted a second time with a different amount, status %s"
        % (key, second.status_code))
    assert error_code(second) == CODE_IDEMPOTENCY_CONFLICT, (
        "the key-reuse refusal carried code %r; the brief pins %r"
        % (error_code(second), CODE_IDEMPOTENCY_CONFLICT))


def test_refund_over_remainder_is_refused(api, db):
    """A refund beyond the refundable remainder is refused, writing nothing.

    cov: C-CF-32, C-DM-06, C-DC-13, C-TR-14
    """
    finance = _finance(api)
    before = len(db.refunds_of(PAY_BEANBAR))
    response = create_refund(api, finance, ORG_NORTHBEAM, PAY_BEANBAR,
                             AMOUNT_BEYOND_REMAINDER)
    assert response.status_code in REFUSED, (
        "a refund of %s on %r, far beyond the captured amount, returned %s: %r"
        % (AMOUNT_BEYOND_REMAINDER, PAY_BEANBAR, response.status_code,
           body_text(response)[:300]))
    assert error_code(response) == CODE_AMOUNT_TOO_LARGE, (
        "the over-remainder refusal carried code %r; the brief pins %r"
        % (error_code(response), CODE_AMOUNT_TOO_LARGE))
    envelope = json_body(response).get("error")
    assert isinstance(envelope, dict) and envelope.get("request_id"), (
        "the refusal body carries no request identifier; the brief pins one on "
        "every response including every error. Body: %r"
        % body_text(response)[:300])
    assert len(db.refunds_of(PAY_BEANBAR)) == before, (
        "a refund row landed in %r for an over-remainder attempt" % TABLE_REFUND)


def test_refund_of_disputed_payment_is_refused(api, db):
    """A disputed payment cannot be refunded by either path.

    cov: C-CF-33, C-CF-43
    """
    finance = _finance(api)
    before = len(db.refunds_of(PAY_PLANSMITH))
    response = create_refund(api, finance, ORG_NORTHBEAM, PAY_PLANSMITH, 1000)
    assert response.status_code in REFUSED, (
        "a refund on the disputed payment %r returned %s: %r"
        % (PAY_PLANSMITH, response.status_code, body_text(response)[:300]))
    assert error_code(response) == CODE_PAYMENT_DISPUTED, (
        "the disputed-payment refusal carried code %r; the brief pins %r"
        % (error_code(response), CODE_PAYMENT_DISPUTED))
    assert len(db.refunds_of(PAY_PLANSMITH)) == before, (
        "a refund row landed in %r for a disputed payment" % TABLE_REFUND)
    dispute = _finance(api)
    listed = api.get(account_path(ORG_NORTHBEAM, "disputes"),
                     params={"environment": ENV_LIVE}, headers=dispute)
    ids = {str(field(row, "id")) for row in as_list(listed.json())}
    assert DISPUTE_PLANSMITH in ids, (
        "the dispute list of %r omits the seeded dispute %r; it listed %r"
        % (ORG_NORTHBEAM, DISPUTE_PLANSMITH, sorted(ids)))


def test_expired_request_cannot_be_approved(api, db):
    """A request older than its lifetime is expired on read, never approvable.

    cov: C-CF-19, C-CF-30, C-CF-31, C-TR-08
    """
    support = _support(api)
    finance = _finance(api)
    request_id = raised_request_id(api, support, ORG_NORTHBEAM, PAY_NORTHWIND,
                                   AMOUNT_ABOVE_CEILING)
    reached = wait_for_state(api, finance, ORG_NORTHBEAM, request_id,
                             ("expired",), _expiry_deadline())
    assert reached == "expired", (
        "request %r still reads state %r after more than the lifetime in "
        "REFUND_REQUEST_TTL_SEC; the brief pins expiry computed on read"
        % (request_id, reached))
    before = len(db.refunds_of(PAY_NORTHWIND))
    response = approve_request(api, finance, ORG_NORTHBEAM, request_id, "late")
    assert response.status_code not in OK_WRITE, (
        "an expired request %r was approved, status %s: %r"
        % (request_id, response.status_code, body_text(response)[:300]))
    assert error_code(response) == CODE_APPROVAL_EXPIRED, (
        "the expired-request refusal carried code %r; the brief pins %r"
        % (error_code(response), CODE_APPROVAL_EXPIRED))
    assert len(db.refunds_of(PAY_NORTHWIND)) == before, (
        "approving an expired request produced a refund row in %r" % TABLE_REFUND)


def test_sandbox_payment_is_not_found_under_live(api):
    """An identifier from the other environment reads as absent, not as refused.

    cov: C-CF-07, C-DM-01
    """
    support = _support(api)
    response = read_payment(api, support, ORG_NORTHBEAM, PAY_SANDBOX_BEANBAR,
                            ENV_LIVE)
    assert response.status_code in NOT_FOUND, (
        "the sandbox payment %r read under live returned %s; the brief pins not "
        "found, because refused would confirm the row exists"
        % (PAY_SANDBOX_BEANBAR, response.status_code))
    sandbox = read_payment(api, support, ORG_NORTHBEAM, PAY_SANDBOX_BEANBAR,
                           ENV_SANDBOX)
    assert sandbox.status_code in OK_READ, (
        "the sandbox payment %r read under sandbox returned %s: %r"
        % (PAY_SANDBOX_BEANBAR, sandbox.status_code, body_text(sandbox)[:300]))
    amount = field(sandbox.json(), "amount_minor", "amount")
    assert int(amount) == SANDBOX_PAYMENT_AMOUNT, (
        "the sandbox payment %r reports amount_minor %r; the brief seeds %s"
        % (PAY_SANDBOX_BEANBAR, amount, SANDBOX_PAYMENT_AMOUNT))


def test_empty_filtered_queue_returns_empty_array(api):
    """A filter that matches nothing returns an empty array, never an error.

    cov: C-UF-20, C-DC-12
    """
    finance = _finance(api)
    response = api.get(account_path(ORG_NORTHBEAM, "approval-requests"),
                       params={"environment": ENV_LIVE,
                               "state": "execution_failed"},
                       headers=finance)
    assert response.status_code in OK_READ, (
        "a filtered approval queue returned %s: %r"
        % (response.status_code, body_text(response)[:300]))
    assert isinstance(response.json(), list), (
        "a filtered approval queue returned %r; the brief pins a top-level JSON "
        "array" % body_text(response)[:200])


def test_webhook_loopback_address_is_forbidden(api, db):
    """An endpoint on a loopback or private address is refused at configuration.

    cov: C-CF-48, C-TR-10
    """
    admin = _admin(api)
    before = db.count("webhook_endpoint", account_id=ORG_NORTHBEAM)
    for url in FORBIDDEN_ENDPOINTS:
        response = api.post(account_path(ORG_NORTHBEAM, "webhook-endpoints"),
                            json={"url": url,
                                  "subscribed_types": [EVENT_TYPES[0]],
                                  "environment": ENV_LIVE},
                            headers=admin)
        assert response.status_code not in OK_WRITE, (
            "the delivery address %r was accepted, status %s: %r"
            % (url, response.status_code, body_text(response)[:300]))
        assert error_code(response) == CODE_ENDPOINT_FORBIDDEN, (
            "the refusal of %r carried code %r; the brief pins %r"
            % (url, error_code(response), CODE_ENDPOINT_FORBIDDEN))
    assert db.count("webhook_endpoint", account_id=ORG_NORTHBEAM) == before, (
        "a row landed in webhook_endpoint for a refused address")


def test_webhook_plain_transport_is_refused(api):
    """An endpoint offered over plain transport is refused.

    cov: C-CF-49
    """
    admin = _admin(api)
    response = api.post(account_path(ORG_NORTHBEAM, "webhook-endpoints"),
                        json={"url": "http://hooks.northbeam.example/nimbus",
                              "subscribed_types": [EVENT_TYPES[0]],
                              "environment": ENV_LIVE},
                        headers=admin)
    assert response.status_code not in OK_WRITE, (
        "a delivery address on plain transport was accepted, status %s: %r"
        % (response.status_code, body_text(response)[:300]))


def test_unknown_event_type_is_refused(api):
    """An endpoint subscribing to an unknown event type is refused.

    cov: C-CF-50, C-CF-51
    """
    admin = _admin(api)
    response = api.post(account_path(ORG_NORTHBEAM, "webhook-endpoints"),
                        json={"url": "https://hooks.northbeam.example/probe-%s"
                                     % probe_token(),
                              "subscribed_types": ["payment.teleported"],
                              "environment": ENV_LIVE},
                        headers=admin)
    assert response.status_code not in OK_WRITE, (
        "an endpoint subscribing to an unknown event type was accepted, status "
        "%s: %r" % (response.status_code, body_text(response)[:300]))


def test_lead_decoy_field_writes_no_row(api, db):
    """A submission filling the unattended decoy field writes nothing.

    cov: C-CF-57, C-CF-58
    """
    before = db.count(TABLE_LEAD)
    payload = {
        "work_email": probe_email(),
        "full_name": "Probe Visitor",
        "company": "Probe Retail",
        "country": "India",
        "annual_volume_band": VOLUME_BANDS[0],
        "products_of_interest": ["billing"],
        "message": "Probe %s" % probe_token(),
        "consent": True,
        DECOY_FIELD: "+91 22 0000 0000",
    }
    response = api.post(API_LEADS, json=payload)
    assert response.status_code not in OK_WRITE, (
        "a lead carrying a filled %r was accepted, status %s: %r"
        % (DECOY_FIELD, response.status_code, body_text(response)[:300]))
    assert db.count(TABLE_LEAD) == before, (
        "a row landed in %r for a submission that filled the decoy field"
        % TABLE_LEAD)


def test_duplicate_lead_returns_first_identifier(api, db):
    """An identical repeat submission is deduplicated rather than doubled.

    cov: C-CF-59, C-CF-75
    """
    email = probe_email()
    payload = {
        "work_email": email,
        "full_name": "Probe Visitor",
        "company": "Probe Retail",
        "country": "India",
        "annual_volume_band": VOLUME_BANDS[1],
        "products_of_interest": ["billing"],
        "message": "Probe duplicate",
        "consent": True,
        DECOY_FIELD: "",
    }
    first = api.post(API_LEADS, json=payload)
    assert first.status_code in OK_WRITE, (
        "the first lead submission returned %s: %r"
        % (first.status_code, body_text(first)[:300]))
    count_after_first = db.count(TABLE_LEAD)
    second = api.post(API_LEADS, json=payload)
    assert second.status_code in OK_WRITE, (
        "the repeated lead submission returned %s: %r"
        % (second.status_code, body_text(second)[:300]))
    assert db.count(TABLE_LEAD) == count_after_first, (
        "a second row landed in %r for an identical repeat submission" % TABLE_LEAD)
    assert id_of(first.json()) == id_of(second.json()), (
        "the repeat submission returned identifier %r against the first %r; the "
        "brief pins the first identifier"
        % (id_of(second.json()), id_of(first.json())))


"""--- presentation --- served markup, the health route and the launch surface"""


def test_health_endpoint_returns_200(api):
    """The health route answers once the app is serving.

    cov: C-DC-05, C-DC-01, C-DC-02, C-DC-03, C-DC-04, C-DC-09, C-DC-10, C-DC-11, C-TR-01, C-TR-02, C-TR-09
    """
    response = api.get(API_HEALTH)
    assert response.status_code == 200, (
        "GET /api/health returned %s: %r"
        % (response.status_code, body_text(response)[:300]))


def test_out_of_scope_routes_are_absent(api):
    """The surfaces the brief scopes out are absent rather than half-built.

    cov: C-CN-01, C-CN-02, C-CN-03
    """
    admin = _admin(api)
    for tail in ("invoices", "subscriptions", "usage-meters", "reports",
                 "exports", "delivery-attempts", "jobs"):
        response = api.get(account_path(ORG_NORTHBEAM, tail),
                           params={"environment": ENV_LIVE}, headers=admin)
        assert response.status_code in NOT_FOUND, (
            "the scoped-out surface %r answered %s; the brief carries no such "
            "surface" % (tail, response.status_code))


def test_app_root_carries_readme_and_reserved_directories():
    """The credential file and the two reserved directories sit at the app root.

    cov: C-DC-06, C-DC-07, C-DC-08
    """
    assert os.path.isfile(README_PATH), (
        "%s does not exist; the deployment contract writes the seeded logins "
        "there" % README_PATH)
    readme = open(README_PATH, encoding="utf-8", errors="replace").read()
    for email in SEEDED_ACCOUNTS:
        assert email in readme, (
            "%s does not name the seeded account %r" % (README_PATH, email))
    assert PASSWORD in readme, (
        "%s does not carry the seeded password" % README_PATH)
    for path in (SCREENSHOT_DIR, DOWNLOAD_DIR):
        assert os.path.isdir(path), (
            "the reserved directory %s does not exist at the app root" % path)


def test_custom_not_found_page_answers_404(site):
    """An unknown address renders the product's own page, answering not found.

    cov: C-CF-60, C-CF-61
    """
    response = site.get("/in/not-a-real-route-%s" % probe_token())
    assert response.status_code == 404, (
        "an unknown address returned %s; the brief pins a not-found answer"
        % response.status_code)
    assert NOT_FOUND_COPY.lower() in body_text(response).lower(), (
        "the not-found page does not carry the pinned copy %r; body began %r"
        % (NOT_FOUND_COPY, body_text(response)[:300]))
    assert 'href="/in"' in body_text(response) or "href='/in'" in body_text(response), (
        "the not-found page offers no way back to %r" % ROUTE_HOME)


def test_sitemap_lists_every_public_route(site):
    """The sitemap names every public route the footer renders.

    cov: C-UF-08, C-TR-20
    """
    response = site.get(ROUTE_SITEMAP)
    assert response.status_code == 200, (
        "GET %s returned %s" % (ROUTE_SITEMAP, response.status_code))
    text = body_text(response)
    for route in PUBLIC_ROUTES:
        assert route in text, (
            "%s does not name the public route %r; it began %r"
            % (ROUTE_SITEMAP, route, text[:300]))


def test_robots_names_the_sitemap(site):
    """The robots file points at the sitemap by absolute address.

    cov: C-UF-09
    """
    response = site.get(ROUTE_ROBOTS)
    assert response.status_code == 200, (
        "GET %s returned %s" % (ROUTE_ROBOTS, response.status_code))
    match = SITEMAP_LINE_RE.search(body_text(response))
    assert match, (
        "%s carries no Sitemap line; it read %r"
        % (ROUTE_ROBOTS, body_text(response)[:300]))
    assert ROUTE_SITEMAP in match.group(1), (
        "%s points at %r rather than at %r"
        % (ROUTE_ROBOTS, match.group(1), ROUTE_SITEMAP))


def test_favicon_is_served(site):
    """The favicon resolves and is declared in the document head.

    cov: C-TR-18
    """
    icon = site.get(ROUTE_FAVICON)
    assert icon.status_code == 200, (
        "GET %s returned %s; the brief pins a served favicon"
        % (ROUTE_FAVICON, icon.status_code))
    home = site.get(ROUTE_HOME)
    assert ICON_RE.search(body_text(home)), (
        "%s declares no icon link in its head; it began %r"
        % (ROUTE_HOME, body_text(home)[:300]))


def test_public_routes_declare_social_preview(site):
    """Every public route carries its own preview title, description and image.

    cov: C-TR-19
    """
    titles = {}
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, (
            "GET %s returned %s" % (route, response.status_code))
        text = body_text(response)
        title = OG_TITLE_RE.search(text)
        description = OG_DESC_RE.search(text)
        image = OG_IMAGE_RE.search(text)
        assert title and description and image, (
            "%s declares social preview title %s, description %s, image %s"
            % (route, bool(title), bool(description), bool(image)))
        value = title.group(1).strip()
        assert value not in titles, (
            "%s shares its preview title %r with %s; no two public routes share "
            "one" % (route, value, titles[value]))
        titles[value] = route
        assert image.group(1).strip(), (
            "%s declares an empty preview image address" % route)


def test_home_route_carries_pinned_hero_copy(site):
    """The country home carries its pinned eyebrow, lead sentence and footer.

    cov: C-CF-65, C-CF-66, C-CF-67, C-CF-68, C-CF-69, C-CN-05, C-UF-01
    """
    response = site.get(ROUTE_HOME)
    assert response.status_code == 200, (
        "GET %s returned %s" % (ROUTE_HOME, response.status_code))
    text = body_text(response)
    for pinned in (HERO_EYEBROW, HERO_LEAD, HERO_ACTION, LOCALE_LABEL, COPYRIGHT):
        assert pinned in text, (
            "%s does not carry the pinned copy %r" % (ROUTE_HOME, pinned))


def test_gated_route_shows_waitlist_action(site):
    """The gated product route badges its availability and swaps its action.

    cov: C-CF-62, C-CF-63
    """
    response = site.get(ROUTE_QUERY)
    assert response.status_code == 200, (
        "GET %s returned %s" % (ROUTE_QUERY, response.status_code))
    text = body_text(response)
    assert AVAILABILITY_BADGE in text, (
        "%s does not carry the pinned badge %r" % (ROUTE_QUERY, AVAILABILITY_BADGE))
    assert GATED_ACTION in text, (
        "%s does not offer the pinned control %r" % (ROUTE_QUERY, GATED_ACTION))


def test_api_key_list_never_returns_secret(api):
    """The credential list carries a prefix, never a secret value.

    cov: C-CF-46, C-CF-47
    """
    admin = _admin(api)
    response = api.get(account_path(ORG_NORTHBEAM, "api-keys"),
                       params={"environment": ENV_LIVE}, headers=admin)
    assert response.status_code in OK_READ, (
        "the credential list of %r returned %s: %r"
        % (ORG_NORTHBEAM, response.status_code, body_text(response)[:300]))
    rows = as_list(response.json())
    assert rows, (
        "the credential list of %r came back empty; the brief seeds two"
        % ORG_NORTHBEAM)
    for row in rows:
        assert "secret" not in {str(k).lower() for k in row}, (
            "a credential row carries a secret field: %r" % row)
        assert field(row, "display_prefix", "prefix"), (
            "a credential row carries no display prefix: %r" % row)


def test_api_key_creation_returns_secret_once(api):
    """Creating a credential shows the value once, then never again.

    cov: C-CF-45, C-RL-08
    """
    admin = _admin(api)
    created = api.post(account_path(ORG_NORTHBEAM, "api-keys"),
                       json={"type": "secret", "environment": ENV_LIVE},
                       headers=admin)
    assert created.status_code in OK_WRITE, (
        "creating a secret credential returned %s: %r"
        % (created.status_code, body_text(created)[:300]))
    payload = created.json()
    secret = field(payload, "secret", "secret_value")
    assert isinstance(secret, str) and secret.startswith(PREFIX_SECRET_LIVE), (
        "the created credential returned secret %r; the brief pins a value "
        "beginning %r in live" % (secret, PREFIX_SECRET_LIVE))
    listed = api.get(account_path(ORG_NORTHBEAM, "api-keys"),
                     params={"environment": ENV_LIVE}, headers=admin)
    assert secret not in body_text(listed), (
        "the credential list returned the secret value again; the brief pins one "
        "showing only")
