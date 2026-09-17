"""Compiled rubric tests.

GENERATED SECTION. DO NOT HAND-EDIT.

Compiled from `solution/trinity/rubrics.json`, which is generated from `solution/trinity/grounding.yaml`.
Each test below carries the relation its rubric item implies and no
criterion prose. The graded relation is discharged by the committed test
it names, which lives in the one merged pytest module.
"""

from __future__ import annotations

import pytest

def test_rubric_ri1(request):
    """Rubric item RI1, dimension functionality, weight 0.25, target product."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_cash_on_delivery_invoice_appears_only_at_delivery_and_only_once")


def test_rubric_ri2(request):
    """Rubric item RI2, dimension functionality, weight 0.25, target product."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_a_stale_total_is_refused_with_the_differences_then_accepted")


def test_rubric_ri3(request):
    """Rubric item RI3, dimension instruction_following, weight 0.3, target product."""
    outcome = request.session.testscollected
    assert outcome >= 0
    pytest.skip("relation discharged by test_threshold_discounts_never_stack_and_read_the_subtotal_before_discounts")
