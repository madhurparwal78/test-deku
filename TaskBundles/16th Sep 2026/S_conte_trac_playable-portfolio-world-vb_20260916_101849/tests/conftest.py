"""Fixtures, pinned literals and helpers for deku/playable-portfolio-world-vb.

Every literal here is pinned in instruction.md. Nothing here is a test.
"""

from __future__ import annotations

import datetime
import html
import json
import os
import re
import threading
import time
import unicodedata
from html.parser import HTMLParser

import httpx
import pytest

import appclient
import capabilities

PASSWORD = appclient.seeded_password("SEED_PASSWORD", "deku-demo-pw-2026")
OWNER_EMAIL = "owner@example.com"

GAMES = ("orchard", "lighthouse", "ski", "flight")
GAME_LABELS = {
    "orchard": "La Cueillette",
    "lighthouse": "La Veille du Phare",
    "ski": "La Descente",
    "flight": "Le Vol",
}
GAME_ZONES = {
    "orchard": "Le Verger",
    "lighthouse": "Le Phare",
    "ski": "Les Hautes Neiges",
    "flight": "La Grève",
}
KEEPERS = {
    "orchard": "La gardienne du verger",
    "lighthouse": "Le gardien du phare",
    "ski": "La monitrice des cimes",
    "flight": "Le portail du vent",
}
KEEPER_LINES = {
    "orchard": "Soixante secondes pour remplir le panier. Les fruits pourris vous coûtent une pomme.",
    "lighthouse": "Guidez les navires entre les récifs avant que la tempête ne tombe.",
    "ski": "Passez les portes, osez les sauts, cueillez les drapeaux jusqu’en bas.",
    "flight": "Le vent vous portera tant que votre coque tiendra.",
}
ITEMS = {
    "orchard": (("pommes", "Pommes", 10, 60), ("bananes", "Bananes", 25, 20),
                ("bonus", "Bonus", 50, 5)),
    "lighthouse": (("navires", "Navires guidés", 40, 30),
                   ("tempetes", "Tempêtes traversées", 100, 10)),
    "ski": (("portes", "Portes franchies", 30, 40), ("sauts", "Sauts réussis", 60, 15),
            ("drapeaux", "Drapeaux cueillis", 100, 5)),
    "flight": (("cibles", "Cibles touchées", 15, 100), ("canons", "Canons trouvés", 50, 6),
               ("anneaux", "Anneaux traversés", 20, 50)),
}
MAX_TOTALS = {"orchard": 1350, "lighthouse": 2200, "ski": 2600, "flight": 2800}
ORCHARD_SEEDS = (
    ("Mathilde", 1180, {"pommes": 58, "bananes": 20, "bonus": 2}),
    ("Yanis", 1040, {"pommes": 54, "bananes": 18, "bonus": 1}),
    ("Capucine", 990, {"pommes": 49, "bananes": 16, "bonus": 2}),
    ("Oscar", 870, {"pommes": 42, "bananes": 14, "bonus": 2}),
    ("Léa", 760, {"pommes": 36, "bananes": 12, "bonus": 2}),
    ("Nour", 640, {"pommes": 34, "bananes": 10, "bonus": 1}),
    ("Hugo", 640, {"pommes": 29, "bananes": 12, "bonus": 1}),
    ("Inès", 410, {"pommes": 21, "bananes": 6, "bonus": 1}),
    ("Basile", 300, {"pommes": 15, "bananes": 4, "bonus": 1}),
    ("Zoé", 180, {"pommes": 8, "bananes": 2, "bonus": 1}),
)
LIGHTHOUSE_SEEDS = (
    ("Admin Vireo", 2080, {"navires": 27, "tempetes": 10}),
    ("Margaux", 1640, {"navires": 21, "tempetes": 8}),
    ("Timothée", 960, {"navires": 14, "tempetes": 4}),
)
SKI_SEEDS = (
    ("Élodie", 1500, {"portes": 20, "sauts": 10, "drapeaux": 3}),
)
ANONYMOUS = "Voyageur anonyme"
RESERVED_NAMES = ("admin", "modérateur", "vireo", "voyageur anonyme")

SITE_TITLE = "Où sommeillent les Îles"
SUBTITLE = "Un voyage à travers les créations d’un Creative Developer"
PAGE_TITLE = "Where Worlds Take Shape - Interactive WebGL Portfolio"
PAGE_DESCRIPTION = ("A playable portfolio: walk a paper-craft world, meet its travellers "
                    "and post your best run to a public leaderboard.")
OG_IMAGE = "/og-image.png"
SITE_NAME = "Vireo"
LOCALE = "fr_FR"
LOCALE_ALTERNATE = "en_US"
CONTACT_LABEL = "Contact"
CONTACT_URL = "https://vireo.example/contact"
NEW_WINDOW_NOTE = "(Nouvelle fenêtre)"
LOADING_WORD = "LOADING"
VOYAGER = "Voyager"
WELCOME = "Bienvenue"
WELCOME_LINES = (
    "Ce site est une expérience interactive mêlant jeu et portfolio.",
    "À travers un univers jouable et évolutif, j’y explore des idées, des mécaniques "
    "et des techniques du web créatif.",
    "Activez vos haut-parleurs ou un casque, utilisez votre souris ou un gamepad, "
    "puis explorez à votre rythme.",
)
INPUT_CAPTION = "Souris / Clavier · Gamepad · Touch"
TIPS = (
    "Utilisez les flèches directionnelles, ainsi que la souris, pour jouer.",
    "Vous pouvez utiliser une manette de jeu pour jouer.",
    "N’hésitez pas à revenir sur vos pas : certains lieux révèlent de nouveaux chemins "
    "quand le monde a changé.",
    "Parlez aux voyageurs que vous croisez : leurs mots sont parfois des portes, et "
    "leurs silences des indices.",
    "Le Golem de Vigie peut grandement vous aider dans la quête : écoutez ce que la mer "
    "lui apprend.",
    "Certains passages sont bien cachés : n’hésitez pas à fouiller partout, observer "
    "les recoins et suivre les détails que le monde laisse derrière lui.",
)
HIDDEN_DESCRIPTION_SENTENCE = "Les flèches directionnelles déplacent le personnage."
ROTATE_PROMPT = "Veuillez tourner votre appareil"
NO_3D_NOTICE = "Le monde ne peut pas être dessiné sur cet appareil."
OPENING_ZONE = "Le Promontoire"
ARRIVAL_PREFIX = "Nouveau lieu, "
SENT_PREFIX = "Résultat envoyé, rang "
REFUSED_PREFIX = "Résultat refusé, "
MENU_NAME = "Menu"
NOTEBOOK_CONTROL = "Inventaire"
CLASSEMENTS = "Classements"
RESUME = "Reprendre"
END_RUN = "Terminer la course"
DEPART = "Partir"
CLOSE_BOARD = "Fermer"
TALK = "Parler"
START = "Commencer"
LATER = "Plus tard"
CONTINUE = "Continuer"
NAME_LABEL = "Votre nom"
SEND = "Envoyer"
SENT_NOTE = "Résultat envoyé."
EMPTY_BOARD = "Ce classement attend son premier nom."
TOTAL_ROW = "Total"
SETTING_GROUPS = {
    "Qualité": ("Basse", "Moyenne", "Haute"),
    "Volume de la musique": ("Bas", "Moyen", "Fort"),
    "Volume des effets": ("Bas", "Moyen", "Fort"),
    "Taille du texte": ("Normale", "Grande"),
    "Animations": ("Complètes", "Réduites"),
}
SETTING_SWITCHES = ("Couper la musique", "Couper les effets", "Inverser l’axe vertical")
NOTEBOOK_TITLE = "Carnet de voyage"
NOTEBOOK_PAGES = ("Récoltes", "Trouvailles", "Journal")
NEXT_PAGE = "Page suivante"
PREVIOUS_PAGE = "Page précédente"
EMPTY_PAGE = "Rien pour l’instant, mais la route est longue."
BRIDGE_ENTRY = "J’ai vu un pont apparaître entre le Promontoire et le Bois Murmurant."
TOUCH_BUTTONS = ("Interagir", "Courir")
NOT_FOUND_PATH = "/atelier-secret"
NOT_FOUND_TITLE = "Page introuvable - Vireo"
NOT_FOUND_DESCRIPTION = "Cette adresse ne mène nulle part dans le monde de Vireo."
NOT_FOUND_HEADING = "Page introuvable"
NOT_FOUND_LINK = "Retour au voyage"

ROOT_WIDE = "19px"
ROOT_NARROW = "12px"
ROOT_WIDE_LARGE = "23px"
ROOT_NARROW_LARGE = "15px"
TITLE_WIDE = "85.5px"
TITLE_NARROW = "48px"
WELCOME_WIDE = "114px"
WELCOME_NARROW = "60px"
SUBTITLE_SIZE = "22.8px"
BUTTON_LABEL_SIZE = "20.9px"
DISPLAY_FAMILY = "Playfair Display"
BODY_FAMILY = "Lato"
TOUCH_MIN = 44
FOCUS_RING_MIN = 2
SOCIAL_WIDTH = 1200
SOCIAL_HEIGHT = 630
RUNS_PER_WINDOW = 3
BOARD_ROWS = 10
IMMUTABLE_MAX_AGE = 31536000

APP_ROOT = "/app"
RESERVED_DIRS = (".browser_screenshots", ".downloads")

WIDE = (1440, 900)
NARROW = (1000, 700)
SHORT = (1440, 600)
PORTRAIT = (390, 844)
LANDSCAPE_PHONE = (844, 390)
TABLET_SIDEWAYS = (990, 700)

SETTLE_SECONDS = 0.25
UI_TIMEOUT_MS = 90000
WORLD_TIMEOUT = 150.0
CHROMIUM_ARGS = ("--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                 "--ignore-gpu-blocklist")
NO_3D_ARGS = ("--disable-3d-apis", "--disable-webgl", "--disable-webgl2")
MEDIA_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".svgz", ".mp3",
                  ".ogg", ".wav", ".m4a", ".aac", ".mp4", ".webm", ".glb", ".gltf",
                  ".ktx2", ".basis", ".hdr", ".exr", ".drc")
MEDIA_TYPES = ("image/", "audio/", "video/", "model/")
FONT_SUFFIXES = (".woff2", ".woff", ".ttf", ".otf", ".eot")

EFFECTIVE_OPACITY_JS = """(el) => {
  let o = 1;
  for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
    const s = getComputedStyle(n);
    if (s.display === 'none' || s.visibility === 'hidden') return 0;
    o *= parseFloat(s.opacity || '1');
  }
  return o;
}"""

FIND_TEXT_JS = """([text, wantVisible]) => {
  const norm = (s) => (s || '').replace(/[\\s\\u00a0\\u202f]+/g, ' ').trim();
  const squash = (s) => (s || '').replace(/[\\s\\u00a0\\u202f]+/g, '');
  const target = squash(text);
  const opacity = (el) => {
    let o = 1;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.display === 'none' || s.visibility === 'hidden') return 0;
      o *= parseFloat(s.opacity || '1');
    }
    return o;
  };
  const all = [...document.querySelectorAll('body *')].filter((el) => squash(el.textContent) === target);
  const hits = all.filter((el) => ![...el.children].some((c) => squash(c.textContent) === target));
  const out = [];
  for (const el of hits) {
    const r = el.getBoundingClientRect();
    const visible = r.width > 2 && r.height > 2 && opacity(el) > 0.05;
    if (wantVisible && !visible) continue;
    let leaf = el;
    while (leaf.firstElementChild && squash(leaf.firstElementChild.textContent)) leaf = leaf.firstElementChild;
    const ls = getComputedStyle(leaf);
    const cs = getComputedStyle(el);
    out.push({
      tag: el.tagName, x: r.x, y: r.y, width: r.width, height: r.height,
      opacity: opacity(el), fontSize: ls.fontSize, fontWeight: ls.fontWeight,
      fontFamily: ls.fontFamily, fontStyle: ls.fontStyle, color: ls.color,
      lineHeight: cs.lineHeight, numeric: ls.fontVariantNumeric,
      features: ls.fontFeatureSettings, lang: (el.closest('[lang]') || {}).lang || '',
      ariaHidden: !!el.closest('[aria-hidden="true"]'), text: norm(el.textContent),
    });
  }
  return out;
}"""


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep."""
    time.sleep(seconds)


def poll(predicate, what: str, timeout: float = 30.0):
    """Poll to a deadline and return the first truthy value."""
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    raise AssertionError(f"{what} did not happen within {timeout:.0f}s; last saw {last!r}")


def hold(seconds: float) -> None:
    """A bounded wait before asserting that something did NOT happen."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        settle()


def elapsed_since(start: float) -> float:
    return time.monotonic() - start


def now_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def days_until(moment) -> float:
    if isinstance(moment, str):
        moment = datetime.datetime.fromisoformat(moment.replace("Z", "+00:00"))
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=datetime.timezone.utc)
    return (moment - now_utc()).total_seconds() / 86400.0


def is_client_error(status: int) -> bool:
    return 400 <= status < 500


def is_success(status: int) -> bool:
    return 200 <= status < 300


def unique_suffix() -> str:
    return os.urandom(3).hex()


def new_player() -> str:
    return f"probe-{os.urandom(6).hex()}"


def unique_name(prefix: str) -> str:
    return f"{prefix} {unique_suffix()}"


def fold(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c)).lower()


def plain_spaces(text: str) -> str:
    return text.replace(" ", " ").replace(" ", " ")


def body_text(response: httpx.Response) -> str:
    return response.text[:400]


def total_for(game: str, counts: dict) -> int:
    worth = {key: value for key, _label, value, _max in ITEMS[game]}
    return sum(worth[key] * count for key, count in counts.items())


def api() -> httpx.Client:
    return appclient.client()


def owner_client() -> httpx.Client:
    return appclient.client(appclient.login(OWNER_EMAIL, PASSWORD))


def start_run(client: httpx.Client, game, player=None) -> httpx.Response:
    payload = {}
    if game is not None:
        payload["game"] = game
    if player is not None:
        payload["player_id"] = player
    return client.post("/runs", json=payload)


def run_token(client: httpx.Client, game: str, player=None) -> str:
    response = start_run(client, game, player or new_player())
    assert is_success(response.status_code), (
        f"POST /runs for {game!r} returned {response.status_code}: {body_text(response)}")
    token = response.json().get("run_token")
    assert isinstance(token, str) and token, f"run start returned no run_token: {response.text[:300]}"
    return token


def send_entry(client: httpx.Client, token, game, name, counts, total) -> httpx.Response:
    payload = {"run_token": token, "name": name, "counts": counts, "total": total}
    if game is not None:
        payload["game"] = game
    return client.post("/entries", json=payload)


def accepted_entry(client: httpx.Client, game: str, name: str, counts: dict) -> dict:
    token = run_token(client, game)
    response = send_entry(client, token, game, name, counts, total_for(game, counts))
    assert is_success(response.status_code), (
        f"a valid {game} entry for {name!r} was refused with {response.status_code}: "
        f"{body_text(response)}")
    entry = response.json()
    assert entry.get("entry_id") is not None, f"the accepted entry carries no entry_id: {entry}"
    return entry


def board(client: httpx.Client, game: str) -> list:
    response = client.get(f"/leaderboards/{game}")
    assert response.status_code == 200, (
        f"GET /leaderboards/{game} returned {response.status_code}: {body_text(response)}")
    rows = response.json()
    assert isinstance(rows, list), f"the {game} board is not a top-level array: {rows!r}"
    return rows


def row_for(rows: list, entry_id) -> dict | None:
    for row in rows:
        if str(row.get("entry_id")) == str(entry_id):
            return row
    return None


def counts_equal(game: str, stored, sent: dict) -> bool:
    if isinstance(stored, str):
        stored = json.loads(stored)
    keys = [key for key, _label, _worth, _max in ITEMS[game]]
    return all(int((stored or {}).get(k, 0)) == int(sent.get(k, 0)) for k in keys)


def game_entries(db, game: str) -> list:
    return db.rows("leaderboard_entry", limit=100000, game_id=game)


def expected_rank(entries: list, entry: dict) -> int:
    ahead = 0
    for other in entries:
        if other["id"] == entry["id"]:
            continue
        if other["total"] > entry["total"]:
            ahead += 1
        elif other["total"] == entry["total"] and (
                other["created_at"], other["id"]) < (entry["created_at"], entry["id"]):
            ahead += 1
    return ahead + 1


class DocumentScan(HTMLParser):
    """Collects the tags a served document declares."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.metas = []
        self.scripts = []
        self.links = []
        self.anchors = []
        self.title_attrs = None
        self.title_text = ""
        self.headings = []
        self.body_classes = ""
        self._in_title = False
        self._in_heading = False
        self._anchor = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "script":
            self.scripts.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "title":
            self.title_attrs = a
            self._in_title = True
        elif tag in ("h1", "h2"):
            self._in_heading = True
            self.headings.append("")
        elif tag == "a":
            self._anchor = {"href": a.get("href", ""), "text": ""}
            self.anchors.append(self._anchor)
        elif tag == "body":
            self.body_classes = a.get("class", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2"):
            self._in_heading = False
        elif tag == "a":
            self._anchor = None

    def handle_data(self, data):
        if self._in_title:
            self.title_text += data
        if self._in_heading and self.headings:
            self.headings[-1] += data
        if self._anchor is not None:
            self._anchor["text"] += data

    def meta(self, key: str) -> dict | None:
        for m in self.metas:
            if m.get("name") == key or m.get("property") == key:
                return m
        return None


def fetch(path: str, **kw) -> httpx.Response:
    return httpx.get(f"{appclient.app_url()}{path}", timeout=appclient.TIMEOUT, **kw)


def scan(text: str) -> DocumentScan:
    parser = DocumentScan()
    parser.feed(text)
    return parser


MARKUP_ASIDE = re.compile("<!" + "--" + ".*?" + "--" + ">", re.S)


def visible_words(text: str) -> str:
    without_comments = MARKUP_ASIDE.sub("", text)
    without_scripts = re.sub(r"<(script|style)\b.*?</\1>", " ", without_comments, flags=re.S | re.I)
    words = html.unescape(re.sub(r"<[^>]+>", " ", without_scripts))
    return re.sub(r"[ \t\r\n]+", " ", words)


def same_origin_assets(document: DocumentScan) -> list:
    out = []
    for s in document.scripts:
        src = s.get("src", "")
        if src and not src.startswith(("http:", "https:", "//", "data:")):
            out.append(src)
    for link in document.links:
        href = link.get("href", "")
        rel = link.get("rel", "")
        if href and ("stylesheet" in rel or "preload" in rel or "modulepreload" in rel) and \
                not href.startswith(("http:", "https:", "//", "data:")):
            out.append(href)
    return out


class BoardStream:
    """Reads one board's event stream on a background thread."""

    def __init__(self, game: str) -> None:
        self.game = game
        self.events = []
        self.stopping = threading.Event()
        self.thread = threading.Thread(target=self._read, daemon=True)

    def _read(self) -> None:
        url = f"{appclient.api_base()}/leaderboards/{self.game}/events"
        timeout = httpx.Timeout(20.0, connect=10.0)
        name, data = "message", []
        try:
            with httpx.stream("GET", url, timeout=timeout,
                              headers={"Accept": "text/event-stream"}) as response:
                self.events.append(("__status__", response.status_code,
                                    response.headers.get("content-type", "")))
                for line in response.iter_lines():
                    if self.stopping.is_set():
                        return
                    if line == "":
                        if data:
                            self.events.append((name, "\n".join(data), ""))
                        name, data = "message", []
                    elif line.startswith("event:"):
                        name = line[6:].strip()
                    elif line.startswith("data:"):
                        data.append(line[5:].lstrip())
        except (httpx.TransportError, httpx.StreamError):
            if not self.stopping.is_set():
                raise

    def start(self) -> "BoardStream":
        self.thread.start()
        return self

    def stop(self) -> None:
        self.stopping.set()

    def status(self):
        for event in list(self.events):
            if event[0] == "__status__":
                return event
        return None

    def named(self, name: str) -> list:
        out = []
        for event in list(self.events):
            if event[0] == name:
                out.append(json.loads(event[1]))
        return out


@pytest.fixture(scope="session")
def db():
    return capabilities.make_backend()


@pytest.fixture()
def anon():
    with api() as client:
        yield client


@pytest.fixture()
def owner():
    with owner_client() as client:
        yield client


@pytest.fixture()
def stream_factory():
    streams = []

    def make(game: str) -> BoardStream:
        stream = BoardStream(game).start()
        streams.append(stream)
        return stream

    yield make
    for stream in streams:
        stream.stop()


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=list(CHROMIUM_ARGS))
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def chromium_without_3d():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=list(NO_3D_ARGS))
        yield browser
        browser.close()


PAGE_ERRORS = {}


def errors_of(pg) -> list:
    return PAGE_ERRORS.get(id(pg), [])


def _context_factory(browser):
    contexts = []

    def make(width: int = WIDE[0], height: int = WIDE[1], **options):
        context = browser.new_context(viewport={"width": width, "height": height},
                                      locale="fr-FR", **options)
        contexts.append(context)
        pg = context.new_page()
        pg.set_default_timeout(UI_TIMEOUT_MS)
        PAGE_ERRORS[id(pg)] = []
        pg.on("pageerror", lambda error: PAGE_ERRORS[id(pg)].append(str(error)))
        return pg

    return make, contexts


@pytest.fixture()
def ui_page(chromium):
    make, contexts = _context_factory(chromium)
    yield make
    for context in contexts:
        context.close()


@pytest.fixture()
def browser_page(chromium_without_3d):
    make, contexts = _context_factory(chromium_without_3d)
    yield make
    for context in contexts:
        context.close()


@pytest.fixture()
def page(ui_page):
    return ui_page()


def find_text(pg, text: str, visible: bool = True) -> list:
    return pg.evaluate(FIND_TEXT_JS, [text, visible])


def wait_text(pg, text: str, timeout: float = 60.0) -> dict:
    found = poll(lambda: find_text(pg, text), f"the text {text!r} to become visible", timeout)
    return found[0]


def text_gone(pg, text: str) -> bool:
    return not find_text(pg, text)


def button(pg, label: str):
    return pg.get_by_role("button", name=re.compile(re.escape(label)))


def visible_button(pg, label: str, timeout: float = 60.0):
    def ready():
        loc = button(pg, label)
        for i in range(loc.count()):
            candidate = loc.nth(i)
            if candidate.is_visible() and candidate.evaluate(EFFECTIVE_OPACITY_JS) > 0.9:
                return candidate
        return None
    return poll(ready, f"the {label!r} button to be shown", timeout)


def corner_control(pg, label: str):
    return pg.get_by_role("button", name=re.compile(re.escape(label))).first


def root_font_size(pg) -> str:
    return pg.evaluate("() => getComputedStyle(document.documentElement).fontSize")


def box_center(box: dict) -> tuple:
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


def hit_is_world(pg, x: float, y: float) -> bool:
    return pg.evaluate(
        """([x, y]) => { const h = document.elementFromPoint(x, y);
        return !!h && (h.tagName === 'CANVAS' || !!h.querySelector('canvas')); }""", [x, y])


def hit_inside(pg, locator, x: float, y: float) -> bool:
    return locator.evaluate(
        """(el, [x, y]) => { const h = document.elementFromPoint(x, y);
        return !!h && (el === h || el.contains(h)); }""", [x, y])


def luminance(css_colour: str) -> float:
    parts = [float(p) for p in re.findall(r"[\d.]+", css_colour)[:3]]
    lin = [(c / 255) / 12.92 if c / 255 <= 0.04045 else ((c / 255 + 0.055) / 1.055) ** 2.4
           for c in parts]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def live_region_text(pg) -> str:
    return pg.evaluate(
        """() => [...document.querySelectorAll('[aria-live], [role=status], [role=log], [role=alert]')]
        .filter((el) => !el.closest('[role=application]'))
        .map((el) => el.textContent || '').join(' | ')""")


def open_site(pg):
    pg.goto(f"{appclient.app_url()}/", wait_until="domcontentloaded")


def wait_home(pg, timeout: float = WORLD_TIMEOUT):
    return visible_button(pg, VOYAGER, timeout)


def enter_world(pg):
    open_site(pg)
    wait_home(pg).click()
    wait_text(pg, WELCOME, 60.0)
    visible_button(pg, VOYAGER, 60.0).click()
    return visible_button(pg, NOTEBOOK_CONTROL, WORLD_TIMEOUT)


def open_menu(pg):
    corner_control(pg, MENU_NAME).click()
    wait_text(pg, CLASSEMENTS, 30.0)


def open_board(pg, game: str):
    open_menu(pg)
    visible_button(pg, GAME_LABELS[game], 30.0).click()
    visible_button(pg, DEPART, 30.0)


def depart(pg, game: str):
    open_board(pg, game)
    visible_button(pg, DEPART, 30.0).click()
    wait_text(pg, GAME_ZONES[game], 60.0)
    return visible_button(pg, TALK, 60.0)


def open_dialogue(pg, game: str, by_key: bool = False):
    prompt = depart(pg, game)
    if by_key:
        pg.keyboard.press("e")
    else:
        prompt.click()
    wait_text(pg, KEEPER_LINES[game], 30.0)
    return prompt


def begin_run(pg, game: str):
    open_dialogue(pg, game)
    visible_button(pg, START, 30.0).click()


def end_run_now(pg):
    open_menu(pg)
    visible_button(pg, END_RUN, 30.0).click()
    wait_text(pg, TOTAL_ROW, 30.0)


def reach_name_form(pg):
    visible_button(pg, CONTINUE, 30.0).click()
    return poll(lambda: pg.get_by_label(NAME_LABEL).first if pg.get_by_label(NAME_LABEL).count() else None,
                "the name form to arrive", 30.0)


def world_density(pg) -> float:
    return pg.evaluate(
        """() => { const region = document.querySelector('[role=application]');
        const canvas = region
          ? (region.matches('canvas') ? region : region.querySelector('canvas'))
          : document.querySelector('canvas');
        if (!canvas) return 0;
        const box = canvas.getBoundingClientRect();
        return box.width ? canvas.width / box.width : 0; }""")


def open_notebook_page(pg, text: str) -> bool:
    pg.keyboard.press("i")
    wait_text(pg, NOTEBOOK_TITLE, 30.0)
    for _ in range(6):
        if find_text(pg, text):
            return True
        visible_button(pg, NEXT_PAGE, 20.0).click()
        hold(1.0)
    raise AssertionError(f"turning the notebook pages never reached {text!r}")


def numeric_texts(pg) -> list:
    return pg.evaluate(
        """() => { const out = [];
        for (const el of document.querySelectorAll('body *')) {
          if (el.children.length) continue;
          const t = (el.textContent || '').trim();
          if (!/^\\d{1,3}$/.test(t)) continue;
          const r = el.getBoundingClientRect();
          if (r.width < 2 || r.height < 2) continue;
          const s = getComputedStyle(el);
          if (s.visibility === 'hidden' || s.display === 'none') continue;
          out.push({value: parseInt(t, 10), top: r.y, x: r.x + r.width / 2, y: r.y + r.height / 2,
                    size: parseFloat(s.fontSize), weight: parseInt(s.fontWeight, 10)});
        }
        return out; }""")


GAMEPAD_JS = """() => {
  const buttons = Array.from({length: 17}, () => ({pressed: false, touched: false, value: 0}));
  window.__deku_pad = {buttons, axes: [0, 0, 0, 0]};
  const pad = () => ({id: 'Deku pad (STANDARD GAMEPAD)', index: 0, connected: true,
    mapping: 'standard', timestamp: performance.now(), buttons: window.__deku_pad.buttons,
    axes: window.__deku_pad.axes, vibrationActuator: null});
  navigator.getGamepads = () => [pad(), null, null, null];
  window.addEventListener('load', () => {
    const ev = new Event('gamepadconnected');
    ev.gamepad = pad();
    window.dispatchEvent(ev);
  });
}"""


def press_pad(pg, index: int):
    pg.evaluate("(i) => { window.__deku_pad.buttons[i] = {pressed: true, touched: true, value: 1}; }", index)
    hold(0.5)
    pg.evaluate("(i) => { window.__deku_pad.buttons[i] = {pressed: false, touched: false, value: 0}; }", index)
    hold(0.5)
