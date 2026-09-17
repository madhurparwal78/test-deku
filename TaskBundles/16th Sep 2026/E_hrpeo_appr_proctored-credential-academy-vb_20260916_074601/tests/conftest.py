"""Task fixtures for deku/proctored-credential-academy-vb.

Nothing here assumes the agent's framework, file layout, ORM or module names:
the only assumptions are the App Contract and what instruction.md pinned
literally. Nothing here reaches a provider SDK; the domain helpers are composed
from the generic primitives in capabilities.py, so swapping a slot's provider
replaces the adapter rather than this file.
"""

from __future__ import annotations

import time
import uuid

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, make_backend

LEARNER_EMAIL = "learner@example.com"
LEARNER2_EMAIL = "learner2@example.com"
LEARNER3_EMAIL = "learner3@example.com"
REVIEWER_EMAIL = "reviewer@example.com"
REGISTRAR_EMAIL = "registrar@example.com"
CORPUS_PASSWORD = "deku-demo-pw-2026"

PARTNER_NORTHGATE = "Northgate Institute"
PARTNER_HALCYON = "Halcyon Labs"
PROGRAM_NORTHGATE = "Northgate Cohort 2026"
PROGRAM_HALCYON = "Halcyon Cohort 2026"

NORTHGATE_TREASURY_REMAINING = 10000
NORTHGATE_TREASURY_TOTAL = 50000
NORTHGATE_SEATS_GRANTED = 2
NORTHGATE_SEAT_CAP = 3
HALCYON_TREASURY_REMAINING = 50000

COURSE_FREE = "solidity-beginner"
COURSE_RESTRICTED = "solidity-intermediate"
COURSE_PAID = "solana-intern"
COURSE_DEPRECATED = "intro-javascript"
COURSE_PAID_PRICE_MINOR = 10000

MODULE_BASICS = "solana-intern-basics"
MODULE_PROGRAMS = "solana-intern-programs"
MODULE_STORY = "solidity-beginner-story"

CHAIN_SOLIDITY = "solidity"
CHAIN_SOLANA = "solana"
CHAIN_JAVASCRIPT = "javascript"
SEEDED_CHAIN_COUNT = 7
SEEDED_COURSE_COUNT = 7

REWARD_TITLE = "Founding Artisan"
REWARD_QUOTA_TOTAL = 1
BOUNTY_TITLE = "Audit a Vault"

PASS_MARK = 70
EXAM_WINDOW_SECONDS = 1800
RETAKE_COOLDOWN_SECONDS = 300
REWARD_WINDOW_DAYS = 30
PROCTOR_SIGNAL_THRESHOLD = 3
PROCTOR_EVENT_RETENTION_DAYS = 90
ERASURE_GRACE_DAYS = 30
PAGE_SIZE = 25
CURSOR_HEADER = "X-Next-Cursor"
RATE_LIMIT_HEADER = "RateLimit-Limit"
RATE_LIMIT_REMAINING_HEADER = "RateLimit-Remaining"
RATE_LIMIT_RESET_HEADER = "RateLimit-Reset"
IDEMPOTENCY_HEADER = "Idempotency-Key"

ASSESSMENT_STATES = ("PreAssessment", "Exam", "ExamReview", "Project",
                     "ProjectReview", "Completed")
EXAM_STATES = ("InProgress", "Passed", "Suspicious", "Failed")
PROJECT_STATES = ("InProgress", "InReview", "Approved")
QUESTION_KINDS = ("MultipleChoice", "MultipleChoiceCode")
PROCTOR_KINDS = ("AnswerSubmitted", "OffFocus", "OnFocus", "NoFaceDetected",
                 "MultipleFaceDetected", "FaceResolved", "TestStarted",
                 "TestResumed", "TestSubmitted")
LEDGER_KINDS = ("issuance", "revocation")
CREDENTIAL_STATES = ("issued", "revoked")
PROCTORING_MODES = ("full", "degraded", "none")
REWARD_KINDS = ("nft", "coupon", "token", "fiat")
REWARD_EARN_STATES = ("in_progress", "redeemed", "expired")
BOUNTY_STATES = ("open", "work_started", "submissions", "concluded", "expired",
                 "canceled")
BOUNTY_APPLICATION_STATES = ("viewed", "bookmarked", "applied", "accepted",
                             "rejected", "work_started", "submitted", "canceled")
PROGRAM_STATES = ("active", "suspended", "terminated")
INVITE_STATES = ("Pending", "Sent", "Accepted")
ENTITLEMENT_SOURCES = ("free", "program")

OK = (200, 201)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
REFUSED = (400, 403, 409, 422)
NOT_FOUND = (404,)

SETTLE_SECONDS = 2.0
POLL_SECONDS = 20.0


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def unique_suffix() -> str:
    return uuid.uuid4().hex[:10]


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def poll_until(predicate, timeout: float = POLL_SECONDS):
    """Poll a predicate to a monotonic deadline. Returns the truthy value or None."""
    deadline = time.monotonic() + timeout
    while True:
        value = predicate()
        if value:
            return value
        if time.monotonic() >= deadline:
            return None
        settle()


class AcademyStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def account_by_email(self, email: str) -> dict | None:
        return self._b.one("account", email=email)

    def count_accounts(self, **where) -> int:
        return self._b.count("account", **where)

    def program_by_name(self, name: str) -> dict | None:
        return self._b.one("partner_program", name=name)

    def partner_by_name(self, name: str) -> dict | None:
        return self._b.one("partner", name=name)

    def course_by_identifier(self, identifier: str) -> dict | None:
        return self._b.one("course", identifier=identifier)

    def count_courses(self, **where) -> int:
        return self._b.count("course", **where)

    def count_chains(self, **where) -> int:
        return self._b.count("chain", **where)

    def module_by_slug(self, slug: str) -> dict | None:
        return self._b.one("module", slug=slug)

    def pages_for_module(self, module_id) -> list[dict]:
        lessons = self._b.rows("lesson", module_id=module_id)
        pages: list[dict] = []
        for lesson in lessons:
            pages.extend(self._b.rows("page", lesson_id=lesson["id"]))
        return pages

    def enrolment_for(self, account_id, course_id) -> dict | None:
        return self._b.one("enrolment", account_id=account_id, course_id=course_id)

    def count_enrolments(self, **where) -> int:
        return self._b.count("enrolment", **where)

    def enrolments_for_program(self, program_id) -> list[dict]:
        return self._b.rows("enrolment", program_id=program_id)

    def count_page_progress(self, **where) -> int:
        return self._b.count("page_progress", **where)

    def page_progress_for(self, account_id, page_id) -> dict | None:
        return self._b.one("page_progress", account_id=account_id, page_id=page_id)

    def assessment_for(self, account_id, module_id) -> dict | None:
        return self._b.one("assessment", account_id=account_id, module_id=module_id)

    def exams_for(self, assessment_id) -> list[dict]:
        return self._b.rows("exam", assessment_id=assessment_id)

    def questions_for(self, module_id) -> list[dict]:
        return self._b.rows("exam_question", module_id=module_id)

    def proctor_events_for(self, exam_id) -> list[dict]:
        return self._b.rows("proctor_event", exam_id=exam_id)

    def project_for(self, assessment_id) -> dict | None:
        return self._b.one("project", assessment_id=assessment_id)

    def count_projects(self, **where) -> int:
        return self._b.count("project", **where)

    def credentials_for(self, account_id) -> list[dict]:
        return self._b.rows("credential", account_id=account_id)

    def count_credentials(self, **where) -> int:
        return self._b.count("credential", **where)

    def ledger_entries_for(self, credential_id) -> list[dict]:
        return self._b.rows("ledger_entry", credential_id=credential_id)

    def count_ledger_entries(self, **where) -> int:
        return self._b.count("ledger_entry", **where)

    def reward_by_title(self, title: str) -> dict | None:
        return self._b.one("reward", title=title)

    def count_reward_earns(self, **where) -> int:
        return self._b.count("reward_earn", **where)

    def bounty_by_title(self, title: str) -> dict | None:
        return self._b.one("bounty", title=title)

    def count_bounty_applications(self, **where) -> int:
        return self._b.count("bounty_application", **where)

    def count_page_views(self, **where) -> int:
        return self._b.count("page_view", **where)

    def audit_entries(self, **where) -> list[dict]:
        return self._b.rows("audit_entry", **where)

    def count_audit_entries(self, **where) -> int:
        return self._b.count("audit_entry", **where)

    def count_erasure_requests(self, **where) -> int:
        return self._b.count("erasure_request", **where)


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def academy(backend: Backend) -> AcademyStore:
    return AcademyStore(backend)


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture()
def learner_client():
    token = login(LEARNER_EMAIL, seeded_password("SEED_LEARNER_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def learner2_client():
    token = login(LEARNER2_EMAIL, seeded_password("SEED_LEARNER2_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def learner3_client():
    token = login(LEARNER3_EMAIL, seeded_password("SEED_LEARNER3_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def reviewer_client():
    token = login(REVIEWER_EMAIL, seeded_password("SEED_REVIEWER_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def registrar_client():
    token = login(REGISTRAR_EMAIL, seeded_password("SEED_REGISTRAR_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


def api(path: str) -> str:
    """`client()` is already based at APP_PUBLIC_URL plus `/api`, so the route is
    written here in full and the shared prefix is trimmed before the call."""
    trimmed = path[len("/api"):] if path.startswith("/api") else path
    return trimmed.lstrip("/")


def body_of(response):
    return response.json()


def seed_course_id(academy: AcademyStore, identifier: str):
    row = academy.course_by_identifier(identifier)
    assert row is not None, (
        f"seed course {identifier!r} is missing from the course table"
    )
    return row["id"]


def seed_module_id(academy: AcademyStore, slug: str):
    row = academy.module_by_slug(slug)
    assert row is not None, (
        f"seed module {slug!r} is missing from the module table"
    )
    return row["id"]


def seed_account_id(academy: AcademyStore, email: str):
    row = academy.account_by_email(email)
    assert row is not None, (
        f"seed account {email!r} is missing from the account table"
    )
    return row["id"]


def seed_program_id(academy: AcademyStore, name: str):
    row = academy.program_by_name(name)
    assert row is not None, (
        f"seed program {name!r} is missing from the partner_program table"
    )
    return row["id"]
