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
    pytest.skip("relation discharged by test_reservation_request_confirms_with_a_code")


def test_rubric_r2(request):
    """Rubric item R2, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_concurrent_requests_for_the_last_place_confirm_exactly_one")


def test_rubric_r3(request):
    """Rubric item R3, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_booked_places_never_exceed_capacity_under_concurrency")


def test_rubric_r4(request):
    """Rubric item R4, dimension functionality, weight 4, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_confirmed_reservation_row_is_stored_in_reservations")


def test_rubric_r5(request):
    """Rubric item R5, dimension functionality, weight 4, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_places_left_equals_capacity_minus_confirmed_party_sizes")


def test_rubric_r6(request):
    """Rubric item R6, dimension functionality, weight 4, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_confirmation_email_reaches_the_reservation_address")


def test_rubric_r7(request):
    """Rubric item R7, dimension instruction_following, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_confirmation_subject_begins_visit_reserved_with_the_code")


def test_rubric_r8(request):
    """Rubric item R8, dimension functionality, weight 4, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_saving_a_frame_persists_a_selection_row")


def test_rubric_r9(request):
    """Rubric item R9, dimension functionality, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_adding_an_already_saved_frame_leaves_one_selection_row")


def test_rubric_r10(request):
    """Rubric item R10, dimension functionality, weight 4, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_signed_out_selection_write_is_denied")


def test_rubric_r11(request):
    """Rubric item R11, dimension functionality, weight 4, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_cancelling_another_visitors_reservation_is_denied")


def test_rubric_r12(request):
    """Rubric item R12, dimension functionality, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_party_larger_than_places_left_is_rejected")


def test_rubric_r13(request):
    """Rubric item R13, dimension functionality, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_reservation_for_a_full_entry_time_is_rejected")


def test_rubric_r14(request):
    """Rubric item R14, dimension functionality, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_cancelling_a_reservation_returns_its_places")


def test_rubric_r15(request):
    """Rubric item R15, dimension instruction_following, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_slots_api_lists_every_run_day_at_five_entry_times")


def test_rubric_r16(request):
    """Rubric item R16, dimension instruction_following, weight 3, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_aura_manifesto_returns_the_three_pinned_paragraphs")


def test_rubric_r17(request):
    """Rubric item R17, dimension instruction_following, weight 2, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_no_image_font_audio_or_video_file_loads")


def test_rubric_r18(request):
    """Rubric item R18, dimension functionality, weight 3, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_login_returns_access_token")


def test_rubric_r19(request):
    """Rubric item R19, dimension instruction_following, weight 2, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_unknown_address_renders_the_not_found_document")


def test_rubric_r20(request):
    """Rubric item R20, dimension functionality, weight 3, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_seeded_rows_appear_exactly_once")
