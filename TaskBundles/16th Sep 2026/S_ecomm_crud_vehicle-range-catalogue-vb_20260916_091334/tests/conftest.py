"""Fixtures, pinned literals and helpers for the Valdris vehicle range catalogue.

No test functions live here. Every literal below appears verbatim in
instruction.md, so a grader never asserts a value the brief left the agent to
invent.
"""

from __future__ import annotations

import os
import re
import time

import httpx

import appclient
import capabilities

TIMEOUT = 30.0
SETTLE_SECONDS = 3.0

PASSWORD = appclient.seeded_password("SEEDED_PASSWORD", "deku-demo-pw-2026")
OWNER_ONE = "owner@example.com"
OWNER_TWO = "owner2@example.com"
SEEDED_ACCOUNTS = (OWNER_ONE, OWNER_TWO)

DEFAULT_LOCALE = "international-en"

FAMILY_HOME_ORDER = ("900", "700", "Volten", "Cardinal", "Terra", "Sierran")
FAMILY_FACET_ORDER = ("700", "900", "Volten", "Cardinal", "Terra", "Sierran")
SERIES_COUNTS = {
    "All": 92,
    "700": 10,
    "900": 22,
    "Volten": 22,
    "Cardinal": 9,
    "Terra": 5,
    "Sierran": 24,
}
TOTAL_VARIANTS = 92
FAMILY_COUNT = 6

UNAVAILABLE_FAMILY = "700"
UNAVAILABLE_CHIP = "Model currently unavailable for order."

FACET_NAMES = ("Model series", "Body Design", "Seats", "Drive")
GROUP_HEADINGS = ("900 Corsa Model variants", "900 Corsa Cabriolet Model variants")

MODEL_YEAR = "2027"
COMPARISON_CAP = 4

ACCELERATION_LABEL_PLAIN = "Acceleration 0 - 100 km/h"
ACCELERATION_LABEL_PACKAGE = "Acceleration 0 - 100 km/h with Sport Chrono Package"
POWER_LABEL_PLAIN = "Power (kW) / Power (PS)"
POWER_LABEL_COMBINED = "Power combined (kW) / Power combined (PS)"
TOP_SPEED_LABEL = "Top speed"

CONSUMPTION_PREFIX = "Fuel consumption combined (model range):"
EMISSIONS_CLAUSE = "CO2-emissions combined (model range):"

SEEDED_VARIANTS = {
    "Corsa": {
        "acceleration": "3.9 s", "power": "290 kW / 394 PS", "top_speed": "294 km/h",
        "acceleration_label": ACCELERATION_LABEL_PACKAGE,
        "power_label": POWER_LABEL_PLAIN,
        "consumption": "10.4 - 9.9 l/100 km", "emissions": "237 - 227 g/km",
        "chips": ("Gasoline", "Rear-Wheel Drive", "Automatic"),
    },
    "Corsa T": {
        "acceleration": "4.5 s", "power": "290 kW / 394 PS", "top_speed": "295 km/h",
        "acceleration_label": ACCELERATION_LABEL_PLAIN,
        "power_label": POWER_LABEL_PLAIN,
        "consumption": "10.9 - 10.4 l/100 km", "emissions": "248 - 237 g/km",
        "chips": ("Gasoline", "Rear-Wheel Drive", "Manual"),
    },
    "Corsa S": {
        "acceleration": "3.3 s", "power": "353 kW / 480 PS", "top_speed": "308 km/h",
        "acceleration_label": ACCELERATION_LABEL_PACKAGE,
        "power_label": POWER_LABEL_PLAIN,
        "consumption": "10.6 - 10.1 l/100 km", "emissions": "242 - 230 g/km",
        "chips": ("Gasoline", "Rear-Wheel Drive", "Automatic"),
    },
    "Corsa 4S": {
        "acceleration": "3.3 s", "power": "353 kW / 480 PS", "top_speed": "308 km/h",
        "acceleration_label": ACCELERATION_LABEL_PACKAGE,
        "power_label": POWER_LABEL_PLAIN,
        "consumption": "11.0 - 10.4 l/100 km", "emissions": "249 - 237 g/km",
        "chips": ("Gasoline", "All-Wheel Drive", "Automatic"),
    },
    "Corsa GTS": {
        "acceleration": "3.0 s", "power": "398 kW / 541 PS", "top_speed": "312 km/h",
        "acceleration_label": ACCELERATION_LABEL_PACKAGE,
        "power_label": POWER_LABEL_COMBINED,
        "consumption": "10.6 - 10.1 l/100 km", "emissions": "242 - 230 g/km",
        "chips": ("Gasoline", "Rear-Wheel Drive", "Automatic"),
    },
    "Corsa 4 GTS": {
        "acceleration": "3.0 s", "power": "398 kW / 541 PS", "top_speed": "312 km/h",
        "acceleration_label": ACCELERATION_LABEL_PACKAGE,
        "power_label": POWER_LABEL_COMBINED,
        "consumption": "10.8 - 10.3 l/100 km", "emissions": "246 - 234 g/km",
        "chips": ("Gasoline", "All-Wheel Drive", "Automatic"),
    },
}

TILE_DESCRIPTIONS = {
    "900": "Iconic sports car with rear engine: 2 doors, 2+2 seats.",
    "700": "Precise mid-engine sports car: 2 doors, 2 seats.",
    "Volten": "Electric sports car: 4 doors, 4/5 seats.",
    "Cardinal": "Luxury sedan with a high level of comfort: 4 doors, 4/5 seats.",
    "Terra": "Sporty compact SUV: 4 doors, 5 seats.",
    "Sierran": "Versatile SUV: 4 doors, up to 5 seats.",
}

REGIONS = ("Africa", "Asia", "Australia/Oceania", "Europe", "Latin America",
           "Middle East", "North America")

OVERVIEW_HEADING = "Model overview"
RANGE_HEADLINE = "Your Valdris journey starts now."
HERO_ACTION = "Discover more"
RESET_CONTROL = "Reset Filter"
COMPARE_CONTROL = "Compare"
STORAGE_ACCEPT = "Accept all"
STORAGE_MINIMAL = "Only necessary cookies"
SELECTOR_HEADING = "Select your market or region"

SEEDED_COMPARISON_NAME = "Weekend coupes"

PUBLIC_ROUTES = (
    f"/{DEFAULT_LOCALE}",
    f"/{DEFAULT_LOCALE}/models/900",
    "/countries",
    f"/{DEFAULT_LOCALE}/legal-notice",
    f"/{DEFAULT_LOCALE}/privacy",
    f"/{DEFAULT_LOCALE}/cookie-policy",
)

SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options")

SEEDED_TABLES = ("families", "variants", "markets", "promotions", "owners",
                 "saved_comparisons", "saved_comparison_variants", "consent_choices")

CONTRAST_FLOOR = 4.5

SORT_WORDS = ("sort by", "sort:", "order by", "newest first", "price low", "price high")

_TAG_RE = re.compile(r"<[^>]+>")
_ASSET_RE = re.compile(r'(?:src|href)="([^"]+)"', re.I)


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def unique(stem: str) -> str:
    return f"{stem}-{os.urandom(4).hex()}"


def session(email: str) -> httpx.Client:
    """A fresh bearer token per call, so no fixture caches one across a run."""
    return appclient.client(appclient.login(email, PASSWORD))


def anonymous() -> httpx.Client:
    return appclient.client(None)


def backend():
    return capabilities.make_backend()


def backend_count(table: str) -> int:
    return backend().count(table)


def visible_text(html: str) -> str:
    return " ".join(_TAG_RE.sub(" ", html).split())


def asset_refs(html: str) -> list:
    return sorted(set(_ASSET_RE.findall(html)))


def variants_payload(client: httpx.Client, **facets):
    """GET /api/variants with a facet selection, returned as parsed JSON."""
    response = client.get("/variants", params={k: v for k, v in facets.items() if v})
    assert response.status_code == 200, (
        f"GET /api/variants{facets} returned {response.status_code}: {response.text[:300]}"
    )
    return response.json()


def series_counts(payload) -> dict:
    """The count shown beside every row of the Model series facet."""
    counts = payload.get("counts") or payload.get("facet_counts") or {}
    series = counts.get("series") or counts.get("Model series") or {}
    out = {}
    for key, value in series.items():
        if isinstance(value, dict):
            value = value.get("count")
        out[str(key)] = int(value)
    return out


def grouped_variants(payload) -> dict:
    """Result groups as {heading: [variant name, ...]}."""
    groups = payload.get("groups") or payload.get("result_groups") or []
    out = {}
    for group in groups:
        heading = group.get("heading") or group.get("title") or group.get("body_style")
        names = [v.get("display_name") or v.get("name") for v in group.get("variants", [])]
        out[str(heading)] = names
    return out


def flat_variants(payload) -> list:
    out = []
    for names in grouped_variants(payload).values():
        out.extend(names)
    return out


def relative_contrast(first, second) -> float:
    """WCAG relative-contrast ratio between two (r, g, b) triples in 0-255."""
    def luminance(rgb):
        channels = []
        for raw in rgb[:3]:
            value = raw / 255.0
            channels.append(value / 12.92 if value <= 0.04045
                            else ((value + 0.055) / 1.055) ** 2.4)
        red, green, blue = channels
        return 0.2126 * red + 0.7152 * green + 0.0722 * blue
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)
