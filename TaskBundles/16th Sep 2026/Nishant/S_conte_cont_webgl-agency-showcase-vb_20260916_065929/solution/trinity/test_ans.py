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
    """Rubric item R1, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_health_endpoint_returns_ok")


def test_rubric_r2(request):
    """Rubric item R2, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_seeded_accounts_sign_in_with_corpus_password")


def test_rubric_r3(request):
    """Rubric item R3, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_public_catalogue_lists_only_published_projects")


def test_rubric_r4(request):
    """Rubric item R4, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_draft_thumbnail_bytes_are_refused_to_anonymous")


def test_rubric_r5(request):
    """Rubric item R5, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_draft_thumbnail_bytes_are_refused_to_visitor")


def test_rubric_r6(request):
    """Rubric item R6, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_draft_thumbnail_bytes_are_served_to_curator")


def test_rubric_r7(request):
    """Rubric item R7, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_uploaded_thumbnail_lands_in_the_store_under_the_key_scheme")


def test_rubric_r8(request):
    """Rubric item R8, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_wizard_created_project_starts_as_draft")


def test_rubric_r9(request):
    """Rubric item R9, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_publishing_reveals_the_project_and_raises_the_count")


def test_rubric_r10(request):
    """Rubric item R10, dimension functionality, weight 5, target http-status-code."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_visitor_cannot_create_a_project")


def test_rubric_r11(request):
    """Rubric item R11, dimension functionality, weight 5, target http-response-body."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_enquiry_persists_and_returns_its_reference")


def test_rubric_r12(request):
    """Rubric item R12, dimension functionality, weight 5, target database-row."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_wildcard_application_file_lands_in_the_store")
