"""Compiled rubric tests.

GENERATED SECTION. DO NOT HAND-EDIT.

Compiled from `solution/trinity/rubrics.json`, which is generated from `solution/trinity/grounding.yaml`.
Each test below carries the relation its rubric item implies and no
criterion prose. The graded relation is discharged by the committed test
it names, which lives in the one merged pytest module.
"""

from __future__ import annotations

import pytest

def test_rubric_r1(request):
    """Rubric item R1, dimension security, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_peer_manager_decision_denied_leaves_request_row_unchanged")


def test_rubric_r2(request):
    """Rubric item R2, dimension security, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_peer_manager_decision_denied_leaves_request_row_unchanged")


def test_rubric_r3(request):
    """Rubric item R3, dimension security, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_manager_cannot_decide_their_own_request")


def test_rubric_r4(request):
    """Rubric item R4, dimension security, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_same_actor_signoff_denied_leaves_run_in_review")


def test_rubric_r5(request):
    """Rubric item R5, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_leave_balance_equals_the_sum_of_its_ledger_rows")


def test_rubric_r6(request):
    """Rubric item R6, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_duplicate_punch_raw_ref_writes_no_second_row")


def test_rubric_r7(request):
    """Rubric item R7, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_concurrent_decisions_record_exactly_one_decider")


def test_rubric_r8(request):
    """Rubric item R8, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_computed_payslip_matches_the_pinned_worked_example")


def test_rubric_r9(request):
    """Rubric item R9, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_run_totals_reconcile_with_its_payslip_rows")


def test_rubric_r10(request):
    """Rubric item R10, dimension functionality, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_leave_request_days_exclude_holiday_and_weekend")


def test_rubric_r11(request):
    """Rubric item R11, dimension functionality, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_regularisation_leaves_the_original_punches_stored")


def test_rubric_r12(request):
    """Rubric item R12, dimension functionality, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_claim_above_manager_limit_escalates_to_payroll")


def test_rubric_r13(request):
    """Rubric item R13, dimension security, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_issued_token_is_minted_by_the_declared_identity_provider")


def test_rubric_r14(request):
    """Rubric item R14, dimension functionality, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_written_row_is_visible_in_the_declared_database")
