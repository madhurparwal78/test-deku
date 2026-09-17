"""Task fixtures for deku/birthday-keyed-arcade-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The only assumptions are the App Contract (the app answers at
APP_PUBLIC_URL with its HTTP API under /api) and the literals instruction.md
pinned explicitly: routes, response fields, accessible names, copy, the link
format and the store file format.

Provider agnostic: the datastore is reached through the generic primitives in
capabilities.py, never through a provider SDK. The rendered product is reached
through Chromium, which the verifier image already carries.
"""

from __future__ import annotations

import base64
import json
import re
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from appclient import app_url
from capabilities import Backend, make_backend
from playwright.sync_api import expect, sync_playwright

CYCLE_DAYS = 366
SERIES_COUNT = 16
COLLECTION_TOTAL = 5856
LEAP_DAY_ORDINAL = 60
LAST_ORDINAL = 366
SERIES_LABELS = [366, 732, 1098, 1464, 1830, 2196, 2562, 2928,
                 3294, 3660, 4026, 4392, 4758, 5124, 5490, 5856]

HUB_ORDER = ["Shaking", "Memory", "Rocket", "Puzzle", "Challenge",
             "Wheel", "Wiggle", "Picks", "Gotcha", "Love"]

GAME_ROUTES = ["/whack-a-mole", "/memory", "/rocket", "/puzzle", "/challenge",
               "/wheel", "/wiggle", "/picks", "/gotcha", "/love"]

PUBLIC_ROUTES = ["/", "/games", "/universe", "/roadmap"] + GAME_ROUTES

WHEEL_CATEGORY_COUNT = 16
ORACLE_DECK_COUNT = 6
PRIZE_TIERS = {"COMMON": 10, "RARE": 100, "LEGENDARY": 250}
PHASES = ["Wood", "Fire", "Earth", "Metal", "Water"]
BACKGROUNDS = ["plain", "confetti", "stripes", "clouds"]
MAX_PAGE_SIZE = 500
WELCOME_GRANT = 300
DAILY_GRANT = 50
BRAND = "Daykin"
STORE_FORMAT = "daykin-store"
STORE_VERSION = 2
LINK_VERSION = 2

DATE_REFUSAL = "Oops! This date doesn't exist."
KEPT_COPY = "Kept. It's in your collection."
EMPTY_COLLECTION = "No characters kept yet. Find one from your birthday."
NO_STORAGE = ("This device won't let the page save anything, so nothing will be "
              "kept after you leave.")
EVERYTHING_DELETED = "Everything this page had kept has been deleted."
PROMPT_AGAIN = "Today's challenge, again. A new one arrives at midnight."
SHARED_BOARD = "Everyone gets this same board today."
CLOCK_BACKWARDS = ("Your device's date went backwards. Nothing you've earned has "
                   "been touched.")
SHARE_WARNING = "The link will contain your birthday. Anyone you send it to will see it."
LINK_NOT_DESCRIBED = "That link doesn't describe anything this page can show."
LINK_TOO_OLD = "That link was made by an older version of this page."
PURSE_CONFLICT = "Both devices spent shards. Choose which purse to keep."
MERGED = "Merged. Undo is available until you leave."
UNREADABLE_FILE = "That file isn't readable, so nothing was changed."

KIRITIMATI = timezone(timedelta(hours=14))
HONOLULU = timezone(timedelta(hours=-10))

REFUSE_STORAGE = """
(() => {
  const refuse = () => {
    throw new DOMException("This page may not store anything here.", "SecurityError");
  };
  for (const name of ["localStorage", "sessionStorage", "indexedDB", "caches"]) {
    Object.defineProperty(window, name, { configurable: true, get: refuse });
  }
})();
"""


@pytest.fixture(scope="session")
def anon_client():
    with httpx.Client(base_url=app_url(), timeout=30.0) as c:
        yield c


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def chromium():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def devices(chromium):
    opened = []

    def open_device(timezone_id: str = "UTC", at: datetime | None = None):
        context = chromium.new_context(
            base_url=app_url(), timezone_id=timezone_id,
            viewport={"width": 1280, "height": 800})
        context.set_default_timeout(20000)
        if at is not None:
            context.clock.install(time=at)
        opened.append(context)
        return context

    yield open_device
    for context in opened:
        context.close()


@pytest.fixture
def page(devices):
    return devices().new_page()


def resolve(c, day: int, month: int):
    return c.get("/api/resolve", params={"day": day, "month": month})


def items_of(payload):
    if isinstance(payload, dict) and "items" in payload:
        return payload["items"]
    return payload


def member_label(number: int) -> str:
    return f"{BRAND} #{number}"


def member_pattern(number: int) -> re.Pattern:
    return re.compile(rf"{BRAND} #{number}(?!\d)")


def member_number(series: int, ordinal: int) -> int:
    return (series - 1) * CYCLE_DAYS + ordinal


def encode_link(payload) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_link(token: str) -> dict:
    padded = token + "=" * (-len(token) % 4)
    return json.loads(base64.urlsafe_b64decode(padded.encode("ascii")))


def kept(series: int, day: int, month: int, background: str, colour: str,
         kept_at: str) -> dict:
    return {"series": series, "day": day, "month": month,
            "background": background, "colour": colour, "keptAt": kept_at}


def credit(entry_id: str, amount: int, at: str) -> dict:
    return {"id": entry_id, "kind": "credit", "amount": amount,
            "reason": entry_id, "at": at}


def debit(entry_id: str, amount: int, at: str) -> dict:
    return {"id": entry_id, "kind": "debit", "amount": amount,
            "reason": entry_id, "at": at}


def store_file(tmp_path, name: str, **kinds) -> str:
    doc = {"format": STORE_FORMAT, "version": STORE_VERSION}
    doc.update(kinds)
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return str(path)


def raw_file(tmp_path, name: str, text: str) -> str:
    path = tmp_path / f"{name}.json"
    path.write_text(text, encoding="utf-8")
    return str(path)


def find_birthday(page, day: int, month: int) -> None:
    group = page.get_by_role("group", name="Birthday")
    group.get_by_role("textbox", name="Day").fill(f"{day:02d}")
    group.get_by_role("textbox", name="Month").fill(f"{month:02d}")
    group.get_by_role("button", name="Find").click()


def sixteen(page):
    return page.get_by_role("list", name="Your sixteen").get_by_role("listitem")


def choose(page, group: str, option: str) -> None:
    page.get_by_role("radiogroup", name=group).get_by_role("radio", name=option).check()


def collection_entries(page):
    return page.get_by_role("list", name="Collection").get_by_role("listitem")


def import_store(page, path: str) -> None:
    page.goto("/import")
    page.get_by_label("Store file").set_input_files(path)
    expect(page.get_by_role("region", name="Import preview")).to_be_visible()
    page.get_by_role("button", name="Apply import").click()
    expect(page.get_by_text(MERGED, exact=True)).to_be_visible()


def enter_machine(page) -> None:
    page.goto("/gotcha")
    page.get_by_role("button", name="ENTER").click()


def expect_balance(page, amount: int) -> None:
    expect(page.get_by_text(f"Balance: {amount} SOUL SHARDS", exact=True)).to_be_visible()


def exchange(page, tier: str) -> None:
    page.get_by_role("button", name=f"Exchange {tier}").click()
    expect(page.get_by_role("region", name="Reward")).to_be_visible()
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_role("region", name="Reward")).to_have_count(0)


def read_board(page) -> list[list[int]]:
    grid = page.get_by_role("grid", name="Puzzle board")
    expect(grid.get_by_role("row")).to_have_count(4)
    board = []
    for row in grid.get_by_role("row").all():
        cells = row.get_by_role("gridcell")
        expect(cells).to_have_count(4)
        board.append([int(text) if text.strip() else 0
                      for text in cells.all_inner_texts()])
    return board


def board_is_solvable(board: list[list[int]]) -> bool:
    flat = [n for row in board for n in row]
    tiles = [n for n in flat if n]
    inversions = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles))
                     if tiles[i] > tiles[j])
    blank_row_from_bottom = 4 - flat.index(0) // 4
    return (inversions + blank_row_from_bottom) % 2 == 1


def blank_of(board: list[list[int]]) -> tuple[int, int]:
    for r, row in enumerate(board):
        for c, n in enumerate(row):
            if n == 0:
                return r, c
    raise AssertionError(f"the board carries no empty cell: {board}")


def move_blank(board: list[list[int]], key: str) -> list[list[int]]:
    dr, dc = {"ArrowUp": (-1, 0), "ArrowDown": (1, 0),
              "ArrowLeft": (0, -1), "ArrowRight": (0, 1)}[key]
    r, c = blank_of(board)
    nr, nc = r + dr, c + dc
    moved = [row[:] for row in board]
    moved[r][c], moved[nr][nc] = moved[nr][nc], 0
    return moved


def prompt_shown(region_text: str, prompts: dict[str, str]) -> str:
    hits = [key for key, text in prompts.items() if text in region_text]
    assert hits, f"no published prompt appears in {region_text[:200]!r}"
    return max(hits, key=lambda key: len(prompts[key]))


def at_local(tz: timezone, year: int, month: int, day: int, hour: int,
             minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=tz)
