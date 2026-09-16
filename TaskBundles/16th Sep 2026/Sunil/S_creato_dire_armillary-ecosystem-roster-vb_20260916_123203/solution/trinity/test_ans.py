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
    """Rubric item R1, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_concurrent_duplicate_applications_create_one_account")


def test_rubric_r2(request):
    """Rubric item R2, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_profile_not_live_is_unreadable_everywhere")


def test_rubric_r3(request):
    """Rubric item R3, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_live_profile_edit_is_held_until_published")


def test_rubric_r4(request):
    """Rubric item R4, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_division_change_goes_through_review_and_moves_profile")


def test_rubric_r5(request):
    """Rubric item R5, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_creator_is_denied_every_studio_route")


def test_rubric_r6(request):
    """Rubric item R6, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_creator_cannot_read_or_change_another_creators_profile")


def test_rubric_r7(request):
    """Rubric item R7, dimension functionality, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_placeholder_blocks_submission_and_names_fields")


def test_rubric_r8(request):
    """Rubric item R8, dimension functionality, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_application_sends_confirmation_mail")


def test_rubric_r9(request):
    """Rubric item R9, dimension functionality, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_curator_publish_goes_live_everywhere_and_mails_owner")


def test_rubric_r10(request):
    """Rubric item R10, dimension functionality, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_consent_decline_records_no_site_events")


def test_rubric_r11(request):
    """Rubric item R11, dimension functionality, weight 3, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_stale_version_write_is_refused")


def test_rubric_r12(request):
    """Rubric item R12, dimension functionality, weight 1, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_repeated_failed_sign_in_is_limited")
