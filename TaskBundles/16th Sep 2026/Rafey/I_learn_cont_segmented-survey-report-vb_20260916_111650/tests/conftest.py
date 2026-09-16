"""Fixtures, pinned literals, the seeded dataset and a reference resolver for Studio Signals.

Black-box only: HTTP against the running app, the rendered page through Playwright,
PostgreSQL through the shared backend adapter and MinIO through the shared storage
adapter. The resolver below restates the brief's arithmetic so every expected figure is
computed from the pinned seed, never read back from the app under test.
"""

from __future__ import annotations

import json
import math
import os
import re
import time
import uuid

import httpx
import pytest

import capabilities

TIMEOUT = 40.0
SETTLE_SECONDS = 0.5
PASSWORD = "deku-demo-pw-2026"
READER_EMAIL = "reader@example.com"
READER2_EMAIL = "reader2@example.com"
READER_NAME = "Ines Park"
READER2_NAME = "Tomas Reyes"
OK = (200, 201, 202, 204)
REFUSED = tuple(range(400, 500))
CHAPTER_SLUGS = ("tools", "craft", "teams")
PUBLISHED_CASES = ("harbour-type", "kestrel-health", "fieldwork-studio")
ANNOUNCED_CASES = ("lumen-transit", "oakline-bank", "parcel-and-post", "quarry-games")
CAVEAT_SHORT = "Directional, not a benchmark. See methodology."
UNKNOWN_SEGMENT = "That link asks for a group this report doesn't have. Showing everyone."
EXPORT_KEY_RE = re.compile(r"^exports/(?P<account>[^/]+)/(?P<export>[^/]+)\.md$")

SIZES = [("startup", "Startups (1 to 50)"), ("growth", "Growth (51 to 500)"),
         ("scale-up", "Scale-up (501 to 2K)"), ("enterprise", "Enterprise (2,000+)")]
ENVS = [("in-house", "In-house"), ("agency", "Agency"), ("freelance", "Freelance")]
EXPS = [("under-10", "Under 10 years"), ("10-plus", "10 years or more")]
WAVES = [2025, 2026]
R = {
 ("startup","in-house","under-10"):(52,60), ("startup","in-house","10-plus"):(21,25),
 ("startup","agency","under-10"):(41,48), ("startup","agency","10-plus"):(17,20),
 ("startup","freelance","under-10"):(30,40), ("startup","freelance","10-plus"):(26,30),
 ("growth","in-house","under-10"):(74,90), ("growth","in-house","10-plus"):(36,45),
 ("growth","agency","under-10"):(31,38), ("growth","agency","10-plus"):(18,22),
 ("growth","freelance","under-10"):(9,12), ("growth","freelance","10-plus"):(7,8),
 ("scale-up","in-house","under-10"):(66,85), ("scale-up","in-house","10-plus"):(49,60),
 ("scale-up","agency","under-10"):(16,20), ("scale-up","agency","10-plus"):(12,15),
 ("scale-up","freelance","under-10"):(4,5), ("scale-up","freelance","10-plus"):(3,4),
 ("enterprise","in-house","under-10"):(88,110), ("enterprise","in-house","10-plus"):(79,95),
 ("enterprise","agency","under-10"):(15,18), ("enterprise","agency","10-plus"):(11,14),
 ("enterprise","freelance","under-10"):(2,3), ("enterprise","freelance","10-plus"):(2,2),
}
CELLS = [(s, e, x) for s, _ in SIZES for e, _ in ENVS for x, _ in EXPS]
Q = {
 "usage-frequency": ("single", "How often do you use AI tools in your design work?", True, [
   ("daily", "Every day", 310, 470, (90, 20, -30, -70)),
   ("weekly", "Every week", 280, 250, (-10, 10, 20, -10)),
   ("monthly", "Every month", 170, 120, (-30, 0, 20, 20)),
   ("rarely", "Rarely", 140, 100, (-30, -20, 0, 40)),
   ("never", "Never", None, None, None)]),
 "stack-tools": ("multi", "Which of these tools are part of your working stack?", True, [
   ("canvas-assistant", "Canvas assistant", 420, 610, (60, 20, -20, -60)),
   ("image-generator", "Image generator", 520, 548, (40, 10, -10, -40)),
   ("code-copilot", "Code copilot", 300, 300, (-20, 0, 20, 30)),
   ("research-summariser", "Research summariser", 380, 280, (-30, 0, 10, 30)),
   ("prototype-builder", "Prototype builder", None, 330, (80, 20, -30, -70))]),
 "tool-count": ("numeric", "How many AI tools do you use in a typical week?", True, [
   ("tools", "Tools per week", 41, 58, (14, 4, -6, -12))]),
 "confidence": ("single", "How confident are you judging the quality of AI-assisted work?", True, [
   ("very", "Very confident", 180, 240, (60, 20, -20, -60)),
   ("fairly", "Fairly confident", 410, 430, (0, 10, 0, -10)),
   ("slightly", "Slightly confident", 250, 220, (-30, -10, 10, 30)),
   ("not", "Not confident", None, None, None)]),
 "stick-reasons": ("multi", "What makes a tool stick in your workflow?", True, [
   ("speed", "Speed", 610, 640, (40, 0, -20, -30)),
   ("quality", "Quality", 450, 520, (0, 10, 0, -10)),
   ("team-standard", "Team standard", 300, 500, (-120, 0, 60, 110)),
   ("integration", "Integration", 400, 440, (-10, 10, 0, 0)),
   ("cost", "Cost", 350, 330, (70, 10, -30, -60))]),
 "craft-shift": ("single", "Has your core craft changed in the last year?", True, [
   ("substantially", "Substantially", 240, 300, (30, 0, -10, -20)),
   ("somewhat", "Somewhat", 450, 440, (0, 0, 0, 0)),
   ("barely", "Barely", None, None, None)]),
 "team-policy": ("single", "Does your team have a written policy on AI tools?", False, [
   ("written", "Yes, written down", 220, 380, (-150, -20, 60, 140)),
   ("drafting", "It is being drafted", 260, 240, (-40, 10, 20, 10)),
   ("none", "No policy", None, None, None)]),
 "hiring-outlook": ("single", "Do you expect your design team to grow next year?", True, [
   ("grow", "Grow", 380, 350, (60, 10, -20, -40)),
   ("hold", "Hold steady", 420, 440, (-20, 0, 10, 10)),
   ("shrink", "Shrink", None, None, None)]),
}

Z = 1.96; THRESHOLD = 30; WIDE_BASE = 200
PUB = "Studio Signals"
SIZE_L = dict(SIZES); ENV_L = dict(ENVS); EXP_L = dict(EXPS)
CHAPTERS = [
 ("tools", "01", "Tools", [
   ("usage-frequency", "How often designers use AI", "usage-frequency", "part-to-whole", "daily"),
   ("stack-ranked", "What is in the stack", "stack-tools", "ranked-bars", None),
   ("stack-movement", "How the stack moved", "stack-tools", "movement-list", None)]),
 ("craft", "02", "Craft", [
   ("tool-count", "How many tools", "tool-count", "segment-breakdown", "tools"),
   ("confidence-by-size", "Confidence by company size", "confidence", "segment-breakdown", "very"),
   ("stick-reasons", "What makes a tool stick", "stick-reasons", "ordered-ranking", None)]),
 ("teams", "03", "Teams", [
   ("craft-shift", "How the craft shifted", "craft-shift", "two-wave", "substantially"),
   ("team-policy", "Written team policies", "team-policy", "two-wave", "written"),
   ("hiring-outlook", "Hiring outlook", "hiring-outlook", "part-to-whole", "grow")]),
]
def half_up(x): return int(math.floor(x + 0.5)) if x >= 0 else -int(math.floor(-x + 0.5))
def match(c, seg): return all(seg.get(k) in (None, v) for k, v in zip(("size","env","exp"), c))
def respondents(w, seg): wi = WAVES.index(w); return sum(R[c][wi] for c in CELLS if match(c, seg))
def cell_count(w, q, oi, c):
    typ, _, _, opts = Q[q]; wi = WAVES.index(w); n = R[c][wi]; si = [s for s,_ in SIZES].index(c[0])
    o = opts[oi]
    if typ == "numeric": return n * (o[2+wi] + o[4][si])
    if o[2+wi] is None and typ == "single":
        return n - sum(cell_count(w, q, j, c) for j in range(len(opts)-1))
    if o[2+wi] is None: return None
    return n * min(1000, max(0, o[2+wi] + o[4][si])) // 1000
def val(w, q, oi, seg):
    n = respondents(w, seg); cs = [cell_count(w, q, oi, c) for c in CELLS if match(c, seg)]
    if n == 0 or any(x is None for x in cs): return None, n
    return (sum(cs)/10/n if Q[q][0] == "numeric" else sum(cs)/n), n
def margin(p, n): return Z*math.sqrt(p*(1-p)/n)
def supported(p1, n1, p2, n2): return abs(p1-p2) > Z*math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
def pct(p): return f"{half_up(p*100)}%"
def mean(v): return f"{half_up(v*10)/10:.1f}"
def label(seg):
    parts = [L[seg[k]] for k, L in (("size",SIZE_L),("env",ENV_L),("exp",EXP_L)) if seg.get(k)]
    return ", ".join(parts)
def movement(q, oi, seg):
    typ, _, comp, opts = Q[q]
    if not comp: return {"state": "not-comparable", "points": None}
    p26, n26 = val(2026, q, oi, seg); p25, n25 = val(2025, q, oi, seg)
    if p25 is None and n25 > 0 or opts[oi][2] is None and opts[oi][3] is not None: return {"state": "not-asked", "points": None}
    if n25 < THRESHOLD: return {"state": "suppressed", "points": None}
    pts = half_up((p26-p25)*100)
    if supported(p26, n26, p25, n25) and pts != 0: return {"state": "rise" if pts > 0 else "fall", "points": pts}
    return {"state": "no-change" if pts == 0 else "not-detectable", "points": pts}
PHRASE = {"rise": "up {n} points since 2025", "fall": "down {n} points since 2025", "no-change": "no change since 2025",
          "not-detectable": "no detectable change since 2025", "not-asked": "not asked in 2025",
          "not-comparable": "asked differently in 2025", "suppressed": "too few 2025 answers to compare"}
CELL = {"no-change": "No change since 2025.", "not-detectable": "No detectable change since 2025.",
        "not-asked": "Not asked in 2025", "not-comparable": "Asked differently in 2025, so the two are not compared.",
        "suppressed": "Too few 2025 answers to compare."}
def phrase(m): return PHRASE[m["state"]].format(n=abs(m["points"] or 0))
def cell_text(m):
    if m["state"] == "rise": return f"+{m['points']}pts"
    if m["state"] == "fall": return f"{m['points']}pts"
    return CELL[m["state"]]
def opt_index(q, slug): return [o[0] for o in Q[q][3]].index(slug)
def ranked(q, seg):
    opts = Q[q][3]; rows = []
    for i, o in enumerate(opts):
        p, n = val(2026, q, i, seg); rows.append((i, o, p, n))
    rows.sort(key=lambda r: (-r[2], r[0]))
    tied = []
    for k in range(len(rows)):
        t = k+1 < len(rows) and not supported(rows[k][2], rows[k][3], rows[k+1][2], rows[k+1][3])
        tied.append(t)
    return rows, tied
def finding(chapter, f, seg):
    fid, short, q, form, focus = f
    typ, wording, comp, opts = Q[q]
    n = respondents(2026, seg)
    out = {"id": fid, "short_title": short, "question": q, "type": typ, "form": form, "base": n, "suppressed": n < THRESHOLD}
    if out["suppressed"]:
        out["heading"] = f"{short}: not reported for this group."
        out["message"] = f"Too few respondents in this group to report. {n} answered."
        out["rows"] = []; return out
    rows = []
    if form in ("part-to-whole", "movement-list"):
        for i, o in enumerate(opts):
            p, _ = val(2026, q, i, seg)
            m = movement(q, i, seg); p25, _ = val(2025, q, i, seg)
            rows.append({"option": o[0], "label": o[1], "value": p, "display": pct(p), "base": n,
                         "previous": None if m["state"] in ("not-comparable","not-asked","suppressed") else pct(p25),
                         "margin_points": half_up(margin(p, n)*100), "movement": m})
    elif form == "two-wave":
        i = opt_index(q, focus); p, _ = val(2026, q, i, seg); p25, n25 = val(2025, q, i, seg)
        m = movement(q, i, seg)
        rows.append({"option": opts[i][0], "label": opts[i][1], "value": p, "display": pct(p), "base": n,
                     "previous": None if m["state"] in ("not-comparable","not-asked","suppressed") else pct(p25),
                     "margin_points": half_up(margin(p, n)*100), "movement": m})
    elif form in ("ranked-bars", "ordered-ranking"):
        rs, tied = ranked(q, seg)
        for (i, o, p, nn), t in zip(rs, tied):
            rows.append({"option": o[0], "label": o[1], "value": p, "display": pct(p), "base": n,
                         "margin_points": half_up(margin(p, n)*100), "tied_with_next": t})
    elif form == "segment-breakdown":
        i = opt_index(q, focus)
        for s, sl in SIZES:
            sub = dict(seg, size=s) if not seg.get("size") or seg.get("size") == s else None
            nb = respondents(2026, sub) if sub else 0
            if nb < THRESHOLD:
                rows.append({"option": s, "label": sl, "value": None, "display": "not reported, base too small", "base": nb, "suppressed": True}); continue
            p, _ = val(2026, q, i, sub)
            rows.append({"option": s, "label": sl, "value": p, "display": mean(p) if typ == "numeric" else pct(p), "base": nb, "suppressed": False})
    out["rows"] = rows
    out["heading"] = heading(fid, q, seg, rows)
    out["source"] = f"Source: {PUB} survey, 2026 wave, {label(seg) or 'all respondents'}, base {n}."
    return out
def heading(fid, q, seg, rows):
    if fid == "usage-frequency":
        i = opt_index(q, "daily"); p,_ = val(2026,q,i,seg); return f"{pct(p)} use AI tools every day, {phrase(movement(q,i,seg))}."
    if fid in ("stack-ranked", "stick-reasons"):
        a, b = rows[0], rows[1]
        noun = "the most common tool in the stack" if fid == "stack-ranked" else "the first reason a tool sticks"
        nouns = "the most common tools in the stack" if fid == "stack-ranked" else "the first reasons a tool sticks"
        if a["tied_with_next"]: return f"{a['label']} and {b['label']} are {nouns}, too close to separate."
        return f"{a['label']} is {noun}, used by {a['display']}." if fid == "stack-ranked" else f"{a['label']} is {noun}."
    if fid == "stack-movement":
        rises = [r for r in rows if r["movement"]["state"] == "rise"]
        if not rises: return "No tool in the stack rose detectably since 2025."
        top = sorted(rises, key=lambda r: -r["movement"]["points"])[0]
        return f"{top['label']} rose the most, {phrase(top['movement'])}."
    if fid == "tool-count":
        p,_ = val(2026,q,0,seg); return f"Designers use {mean(p)} AI tools in a typical week."
    if fid == "confidence-by-size":
        i = opt_index(q,"very"); p,_ = val(2026,q,i,seg); return f"{pct(p)} are very confident judging AI-assisted work."
    if fid == "craft-shift":
        i = opt_index(q,"substantially"); p,_ = val(2026,q,i,seg); return f"{pct(p)} say their core craft changed substantially, {phrase(movement(q,i,seg))}."
    if fid == "team-policy":
        i = opt_index(q,"written"); p,_ = val(2026,q,i,seg); return f"{pct(p)} work in a team with a written AI policy."
    if fid == "hiring-outlook":
        i = opt_index(q,"grow"); p,_ = val(2026,q,i,seg); return f"{pct(p)} expect their design team to grow next year."
def chapter(slug, seg):
    for s, num, title, fs in CHAPTERS:
        if s == slug: return {"slug": s, "number": num, "title": title, "findings": [finding(s, f, seg) for f in fs]}


def segment_params(seg: dict, prefix: str = "") -> dict:
    return {prefix + k: v for k, v in seg.items() if v}


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause, for a side effect the app applies asynchronously."""
    time.sleep(seconds)


def base_url() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}: {response.text[:400]}")


def unique(prefix: str = "probe") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def norm(text: str) -> str:
    return (text or "").replace("\u2019", "'").replace("\u2018", "'")


def body(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return {}
    text = response.text.strip()
    return json.loads(text) if text else {}


def ok(response: httpx.Response, what: str):
    assert response.status_code in OK, f"{what} failed: {describe(response)}"
    return body(response)


def refused(response: httpx.Response, what: str) -> None:
    assert response.status_code in REFUSED, f"{what} was not refused: {describe(response)}"


def missing(response: httpx.Response, what: str) -> None:
    assert response.status_code == 404, f"{what} did not answer as missing: {describe(response)}"


def client(token: str | None = None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=base_url(), timeout=TIMEOUT, headers=headers, follow_redirects=False)


def token_for(email: str, password: str = PASSWORD) -> str:
    with client() as anon:
        payload = ok(anon.post("/api/auth/sign-in", json={"email": email, "password": password}),
                     f"sign in for {email}")
    value = str(payload.get("token") or "")
    assert value, f"sign in for {email} returned no token: {payload}"
    return value


def sign_up(display_name: str = "Probe Reader") -> tuple[httpx.Client, str]:
    address = f"{unique('reader')}@example.com"
    with client() as anon:
        payload = ok(anon.post("/api/auth/sign-up", json={
            "display_name": display_name, "email": address, "password": PASSWORD, "website": ""}), "sign up")
    return client(str(payload["token"])), address


def cookie_session(email: str, password: str = PASSWORD) -> httpx.Client:
    session = httpx.Client(base_url=base_url(), timeout=TIMEOUT, follow_redirects=False)
    ok(session.post("/api/auth/sign-in", json={"email": email, "password": password}), f"sign in {email}")
    return session


def resolved(session: httpx.Client, slug: str, seg: dict | None = None, vs: dict | None = None) -> dict:
    params = segment_params(seg or {})
    params.update(segment_params(vs or {}, "vs_"))
    return ok(session.get(f"/api/chapters/{slug}", params=params), f"chapter {slug} {params}")


def by_id(chapter_payload: dict) -> dict:
    return {f["id"]: f for f in chapter_payload["findings"]}


def export_text(session: httpx.Client, seg: dict | None = None) -> str:
    response = session.get("/api/export.md", params=segment_params(seg or {}))
    assert response.status_code == 200, describe(response)
    return response.text


def html_text(markup: str) -> str:
    import html as html_lib
    markup = re.sub(r"<(script|style|template)\b.*?</\1>", " ", markup, flags=re.S | re.I)
    return re.sub(r"\s+", " ", norm(html_lib.unescape(re.sub(r"<[^>]+>", " ", markup)))).strip()


def links_to(markup: str, path: str) -> bool:
    return re.search(rf"href=[\"'](?:https?://[^\"'/]+)?{re.escape(path)}/?(?:[?#][^\"']*)?[\"']", markup, re.I) is not None


def contrast(front: tuple, back: tuple) -> float:
    def channel(value):
        value = value / 255.0
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    def luminance(colour):
        r, g, b = (channel(c) for c in colour[:3])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    light, dark = sorted((luminance(front), luminance(back)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def goto(tab, path: str) -> None:
    tab.goto(base_url() + path, wait_until="load")
    settle(1.5)


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def anon() -> httpx.Client:
    with client() as session:
        yield session


@pytest.fixture()
def reader() -> httpx.Client:
    with client(token_for(READER_EMAIL)) as session:
        yield session


@pytest.fixture()
def fresh():
    session, address = sign_up()
    with session:
        yield session


@pytest.fixture()
def fresh2():
    session, address = sign_up("Second Probe")
    with session:
        yield session


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        chromium = pw.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def phone_page(browser):
    context = browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def reduced_page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    tab = context.new_page()
    yield tab
    context.close()
