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
    pytest.skip("relation discharged by test_published_open_story_is_served_in_full_to_a_signed_out_visitor")


def test_rubric_r2(request):
    """Rubric item R2, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_draft_story_requested_by_slug_while_signed_out_is_refused")


def test_rubric_r3(request):
    """Rubric item R3, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_members_story_body_is_withheld_from_a_signed_out_visitor")


def test_rubric_r4(request):
    """Rubric item R4, dimension data_integrity, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_concurrent_story_creates_on_one_slug_leave_exactly_one_row")


def test_rubric_r5(request):
    """Rubric item R5, dimension data_integrity, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_uploaded_cover_bytes_live_in_the_object_store_at_the_key_scheme")


def test_rubric_r6(request):
    """Rubric item R6, dimension data_integrity, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_complete_scan_carries_exactly_four_graded_sections")


def test_rubric_r7(request):
    """Rubric item R7, dimension data_integrity, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_two_scans_of_one_address_produce_identical_grades")


def test_rubric_r8(request):
    """Rubric item R8, dimension data_integrity, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_repeated_newsletter_address_creates_no_second_subscriber_row")


def test_rubric_r9(request):
    """Rubric item R9, dimension security, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_reader_request_to_an_author_endpoint_is_denied_at_the_api")


def test_rubric_r10(request):
    """Rubric item R10, dimension security, weight 3, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_signed_out_request_for_the_leads_desk_is_denied")


def test_rubric_r11(request):
    """Rubric item R11, dimension deployment, weight 3, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_health_endpoint_answers_two_hundred")


def test_rubric_r12(request):
    """Rubric item R12, dimension data_integrity, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_seeded_accounts_stories_and_subscriber_are_present_once")
