"""Fixtures, domain helpers and the pinned literals for Travel Luggage Storefront.

No test_* function lives here. Every value test_output.py asserts about the SEEDED
world is pinned in this file and appears verbatim in instruction.md. Per-run probe
values are generated here and are only ever compared against themselves.

The shared grader (appclient, capabilities, _shapes) is supplied by the deku-verifier-base
image on PYTHONPATH=/tests. Nothing here imports a provider SDK.
"""

from __future__ import annotations

import concurrent.futures
import datetime
import gzip
import math
import os
import re
import time

import httpx
import pytest
from playwright.sync_api import sync_playwright

import _shapes
import appclient
import capabilities

OWNER_EMAIL = "owner@example.com"
CUSTOMER_EMAIL = "customer@example.com"
CUSTOMER2_EMAIL = "customer2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"
SEEDED_ACCOUNTS = (
    (OWNER_EMAIL, "owner", "Kiran Rao"),
    (CUSTOMER_EMAIL, "customer", "Aarav Mehta"),
    (CUSTOMER2_EMAIL, "customer", "Noor Haddad"),
)
ROLE_OWNER = "owner"
ROLE_CUSTOMER = "customer"
FIRST_NAME = "Aarav"
GREETING = "Hello, Aarav"

SALE_NAME = "Road Week"
CURRENCY = "usd"
PAGE_SIZE = 24
DEFAULT_STOCK = 20
SORTS = ("featured", "best-selling", "price-asc", "price-desc", "newest")
SIZE_CLASSES = ("cabin", "check-in", "check-in-large", "trunk", "kids", "set")
BAG_TYPES = ("backpack", "briefcase", "duffle", "diaper-bag", "kids-backpack")
USES = ("work", "travel", "diaper-and-kids")
TAGS = ("tech", "clearance")
BADGES = ("hot", "must-have")
BADGE_SOLD_OUT = "sold-out"
SIBLING_SIZES = ("cabin", "check-in", "check-in-large", "set")
COLLECTION_KINDS = ("line", "size", "category", "type", "use", "highlight", "all")
KIND_PARENT = {"line": "luggage", "size": "luggage", "type": "backpacks-and-briefcases",
               "use": "backpacks-and-briefcases", "category": "all", "highlight": "all"}
PANEL_ENTRIES = ("Tech Range", "Cabin", "Check-in", "Check-in Large", "Trunk", "Kids Luggage",
                 "Sets", "Passage", "Contour", "Meridian", "Ridge", "Coastal", "Solstice",
                 "Best Sellers", "On Sale", "Backpacks", "Briefcases", "Duffles", "Diaper Bags",
                 "Kids Backpacks", "Work", "Travel", "Diaper & Kids")
CATEGORY_HANDLES = ("luggage", "backpacks-and-briefcases", "totes", "slings-and-crossbodies",
                    "accessories", "wallets")
SIZE_FIGURES = {
    "cabin": ("3.23", "40", "54 x 37.5 x 23.5 cm"),
    "check-in": ("3.95", "68", "66 x 44 x 27 cm"),
    "check-in-large": ("4.70", "98", "76 x 50 x 30 cm"),
    "trunk": ("5.10", "90", "70 x 45 x 34 cm"),
    "kids": ("2.10", "22", "45 x 32 x 20 cm"),
}
SET_OF_3_FIGURES = ("11.88", "206", "54 x 37.5 x 23.5 cm, 66 x 44 x 27 cm, 76 x 50 x 30 cm")
SET_OF_2_FIGURES = ("4.20", "44", "45 x 32 x 20 cm, 45 x 32 x 20 cm")
SET_HANDLES_OF_3 = ("passage-luggage-set-of-3", "meridian-luggage-set-of-3")
SET_HANDLE_OF_2 = "solstice-luggage-set-of-2"
MEDIA_KIND_IMAGE = "image"
MEDIA_KINDS = ("image", "video")
ALT_EXAMPLE = "Passage Luggage - Cabin in Field Olive, front view"
DISCOUNT_EXAMPLES = ((17900, 29900, 40), (19900, 29900, 33), (59900, 109900, 45))

MSG_LOGIN = "That email and password do not match."
MSG_RECOVER = "If we know that address, a reset link is on its way."
RESET_SUBJECT = "Reset your valisette password"
RESET_PATH = "/account/reset/"
RESET_HEADING = "Choose a new password"
RESET_BUTTON = "SAVE PASSWORD"
RESET_DONE = "Your password has been changed."
MSG_TWO_LEFT = "Only 2 left in stock."
MSG_SOLD_OUT = "Sorry, the last one just sold out."
MSG_PRICE_CHANGED = "The price of one item changed while you were shopping. Review before paying."
MSG_CORPORATE_UNKNOWN = "We could not find that corporate account."
MSG_CORPORATE_EUR = "That corporate account is billed in EUR. Corporate orders are billed in USD."
MSG_NEWSLETTER = "Thank you for subscribing!"
MSG_GIFT_UNKNOWN = "That code is not recognised."
NOT_FOUND_HEADING = "That page has moved on without us."
NOT_FOUND_LINE = "The page you asked for is not here any more."
NOT_FOUND_LINKS = ("/", "/collections/all", "/pages/stores")
NOT_FOUND_LABELS = ("Home", "Shop all", "Find a store")

ERR_INSUFFICIENT = "insufficient_stock"
ERR_OUT_OF_STOCK = "out_of_stock"
ERR_PRICE_CHANGED = "price_changed"
ERR_CART_EMPTY = "cart_empty"
ERR_CORPORATE_UNKNOWN = "billing_account_unknown"
ERR_CORPORATE_CURRENCY = "billing_account_currency"
ERR_NOT_FOUND = "not_found"

MAIL_FROM = "orders@valisette.example.com"
SUBJECT_EXAMPLE = "Your valisette order VS-100004 is confirmed"
OPENING_EXAMPLE = "Order VS-100004, total charged $277."
FIRST_NEW_ORDER = "VS-100004"
ORDER_PREFIX = "VS-"
EXTERNAL_KEY_PREFIX = "valisette-"
KB_USD = "USD"
KB_EUR = "EUR"
CORPORATE_ACCOUNTS = (
    ("orbit-northwind", "Northwind Trading", "USD"),
    ("orbit-acme", "Acme Partner Ltd", "EUR"),
    ("orbit-amelia", "Amelia Ortega", "EUR"),
)
NORTHWIND = "orbit-northwind"
ACME = "orbit-acme"
AMELIA = "orbit-amelia"
KB_ACCOUNTS_PATH = "/1.0/kb/accounts"
KB_HEALTH_PATH = "/1.0/healthcheck"

STATE_PENDING = "pending"
STATE_PAID = "paid"
STATE_FULFILLED = "fulfilled"
STATE_CANCELLED = "cancelled"
ORDER_STATES = (STATE_PENDING, STATE_PAID, STATE_FULFILLED, STATE_CANCELLED)
MOVE_SALE = "sale"
MOVE_RESTOCK = "restock"
MOVE_CANCELLATION = "cancellation"
MOVE_ADJUSTMENT = "adjustment"
MOVEMENT_KINDS = (MOVE_SALE, MOVE_RESTOCK, MOVE_CANCELLATION, MOVE_ADJUSTMENT)
STANDARD = "standard"
EXPRESS = "express"
EXPRESS_COST = 1500
PLACEMENTS = ("front", "top")
COUNTRY = "US"

SEED_ORDERS = (
    ("VS-100001", CUSTOMER_EMAIL, STATE_FULFILLED, (("PSG-CAB-OLV", 1, 17900, 29900),),
     STANDARD, 29900, 12000, 0, 17900, "valisette-VS-100001"),
    ("VS-100002", CUSTOMER_EMAIL, STATE_PAID,
     (("MNI-SLG-NSH", 1, 4900, 7900), ("PCK-CUB-HTG", 1, 2900, 2900)),
     EXPRESS, 10800, 3000, 1500, 9300, "valisette-VS-100002"),
    ("VS-100003", CUSTOMER2_EMAIL, STATE_PAID, (("VLT-SLV-OLV", 2, 3900, 5900),),
     STANDARD, 11800, 4000, 0, 7800, "orbit-northwind"),
)
SEED_NUMBERS = ("VS-100001", "VS-100002", "VS-100003")
SELF_BILLED_KEYS = ("valisette-VS-100001", "valisette-VS-100002")
SEED_ADDRESS = ("Aarav Mehta", "42 Alder Lane", "Apt 3", "Portland", "OR", "97205", "US",
                "+1 503 555 0177")
SEED_PLACED_DAYS_BEFORE_START = {"VS-100001": 20, "VS-100002": 2, "VS-100003": 1}
ORDER3_ADDRESS = ("Noor Haddad", "9 Birch Court", "Seattle", "WA", "98101", "US",
                  "+1 206 555 0188")

GIFT_ACTIVE = "VSGC-2026-AMBER"
GIFT_ACTIVE_BALANCE = 5000
GIFT_LAPSED = "VSGC-2025-LAPSED"
GIFT_LAPSED_BALANCE = 2500
GIFT_LAPSED_EXPIRY = "2025-12-31"

PAGES = (
    ("faq", "FAQ", "FAQ"),
    ("warranty", "Warranty", "Claim My Warranty"),
    ("terms", "Terms & Conditions", "Terms & Conditions"),
    ("airline-damage-policy", "Airline Damage Policy", "Airline Damage Policy"),
    ("journal", "Journal", "Blogs"),
    ("trial", "30 Day Trial", "Claim 30 Day Trial"),
    ("returns", "Return & Refund Policy", "Return & Refund Policy"),
    ("privacy", "Privacy Policy", "Privacy Policy"),
    ("careers", "Careers", "Join our team! - careers@valisette.example.com"),
    ("gift-cards", "Gift Cards", "Check Gift Card Balance"),
)
PRIVACY_PATH = "/pages/privacy"
STORES_PATH = "/pages/stores"
PUBLIC_ROUTES = ("/", "/collections/luggage", "/collections/all",
                 "/products/passage-luggage-cabin", "/search?q=olive", "/cart", "/pages/stores",
                 "/pages/faq", "/account/login", "/account/register", "/account/recover")
SIGNED_IN_ROUTES = ("/account", "/account/orders", "/account/orders/VS-100001",
                    "/account/addresses")
LOGIN_PATH = "/account/login"
SEARCH_EXAMPLE = "olive"
SEARCH_OLIVE_COUNT = 8
OLIVE = "Field Olive"
SEARCH_COASTAL = ("Coastal Luggage - Cabin", "Coastal Luggage - Medium", "Coastal Luggage - Large",
                  "Coastal Weekender", "Ridge Trunk - Medium", "Ridge Cabin Pro")
SEARCH_MERIDIAN_LAST = "Overnight Backpack - 23L"
STORES_PORT = ("Lloyd Center", "Pearl District")
STORES_NEW = ("Newbury Street", "Hudson Yards", "SoHo")
CABIN_PINK = ("Passage Luggage - Cabin", "Contour Luggage - Cabin")
PRICE_DESC_FIRST = "Passage Luggage - Set of 3"
BEST_SELLING_FIRST = ("Passage Luggage - Cabin", "Passage Backpack - 30L")
WALLETS_RANGE = "Vault Card Case"
LUGGAGE_TOTAL = 20
ON_SALE_TOTAL = 34
ON_SALE_PAGE_TWO = 10
MORE_MERIDIAN = 3
MORE_PASSAGE = 2
BEST_SELLER_COUNT = 20
CROSS_SELL = ("Packing Cubes (Set of 6)", "Travel Pillow")
INSTALMENT_EXAMPLE = "or pay in 4 - $44.75 today - 0% interest"
SCRIPT_BUDGET_BYTES = 180 * 1024
ALLOWED_ASSET_TYPES = ("document", "script", "stylesheet", "xhr", "fetch", "websocket",
                       "manifest", "other")
WORKED_EXAMPLES = (
    ((("PSG-CAB-OLV", 1), ("MNI-SLG-NSH", 2)), STANDARD, 45700, 18000, 0, 27700, "$277"),
    ((("PSG-CAB-OLV", 1), ("MNI-SLG-NSH", 2)), EXPRESS, 45700, 18000, 1500, 29200, "$292"),
    ((("MRD-CAB-STB", 1), ("PCK-CUB-HTG", 1)), STANDARD, 32800, 10000, 0, 22800, "$228"),
)
ENDED_SALE_EXAMPLE = ("PSG-SET-NSH", 109900, 0, 109900, "$1,099")
MONEY_EXAMPLES = ((27700, "$277"), (109900, "$1,099"), (4475, "$44.75"))

TABLES = ("account", "session_token", "password_reset", "address", "category", "collection",
          "product", "variant", "media", "stock_movement", "store", "cart", "cart_line",
          "orders", "order_line", "subscriber", "gift_card", "sale", "page")
DERIVED_COLUMNS = (("variant", "stock"), ("variant", "in_stock"), ("variant", "discount_percent"),
                   ("variant", "on_sale"), ("variant", "badge"), ("product", "units_sold"),
                   ("cart", "subtotal"), ("cart", "total"), ("cart_line", "line_total"),
                   ("cart_line", "line_saving"), ("sale", "active"),
                   ("collection", "product_count"), ("orders", "delivery_from"))

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 20.0
SALE_WAIT_SECONDS = 45.0
PAGE_TIMEOUT_MS = 20000

COLOURWAYS = (
    ('Field Olive', 'OLV', 'green'),
    ('Night Shift', 'NSH', 'black'),
    ('Deep End Blue', 'DEB', 'blue'),
    ('Salt Flat', 'SFL', 'white'),
    ('Slow Sunday', 'SSU', 'beige'),
    ('Corner Shop Pink', 'CSP', 'pink'),
    ('Hold The Grey', 'HTG', 'grey'),
    ('Static Blue', 'STB', 'blue'),
    ('Cloud Cover', 'CCV', 'grey'),
    ('Fast Lane Amber', 'FLA', 'yellow'),
    ('Home Turf Amber', 'HTA', 'yellow'),
    ('Long Way Round', 'LWR', 'beige'),
    ('Coastal Mist', 'CMI', 'grey'),
)

PRODUCTS = (
    ('passage-luggage-cabin', 'Passage Luggage - Cabin', 'luggage', 'Passage', 'cabin', None, ('travel',), (), 'hot', 17900, 29900, 940, '2026-03-02', 'PSG-CAB', ('OLV', 'NSH', 'DEB', 'SFL', 'SSU', 'CSP')),
    ('passage-luggage-medium', 'Passage Luggage - Medium', 'luggage', 'Passage', 'check-in', None, ('travel',), (), None, 22900, 37900, 610, '2026-03-02', 'PSG-MED', ('OLV', 'NSH', 'DEB')),
    ('passage-luggage-large', 'Passage Luggage - Large', 'luggage', 'Passage', 'check-in-large', None, ('travel',), (), None, 25900, 42900, 380, '2026-03-02', 'PSG-LRG', ('OLV', 'NSH')),
    ('passage-luggage-set-of-3', 'Passage Luggage - Set of 3', 'luggage', 'Passage', 'set', None, ('travel',), (), 'must-have', 59900, 109900, 520, '2026-03-09', 'PSG-SET', ('NSH', 'OLV')),
    ('meridian-luggage-cabin', 'Meridian Luggage - Cabin', 'luggage', 'Meridian', 'cabin', None, ('travel',), (), None, 17900, 29900, 870, '2026-05-18', 'MRD-CAB', ('HTG', 'STB', 'CCV', 'FLA', 'HTA', 'LWR', 'NSH')),
    ('meridian-luggage-medium', 'Meridian Luggage - Medium', 'luggage', 'Meridian', 'check-in', None, ('travel',), (), None, 22900, 37900, 450, '2026-05-18', 'MRD-MED', ('HTG', 'STB', 'CCV')),
    ('meridian-luggage-large', 'Meridian Luggage - Large', 'luggage', 'Meridian', 'check-in-large', None, ('travel',), (), None, 25900, 42900, 300, '2026-05-18', 'MRD-LRG', ('HTG', 'CCV')),
    ('meridian-luggage-set-of-3', 'Meridian Luggage - Set of 3', 'luggage', 'Meridian', 'set', None, ('travel',), (), None, 59900, 109900, 260, '2026-05-25', 'MRD-SET', ('HTG', 'STB')),
    ('coastal-luggage-cabin', 'Coastal Luggage - Cabin', 'luggage', 'Coastal', 'cabin', None, ('travel',), (), 'hot', 17900, 29900, 790, '2026-01-12', 'CST-CAB', ('DEB', 'SFL', 'NSH')),
    ('coastal-luggage-medium', 'Coastal Luggage - Medium', 'luggage', 'Coastal', 'check-in', None, ('travel',), (), None, 22900, 37900, 330, '2026-01-12', 'CST-MED', ('DEB', 'SFL')),
    ('coastal-luggage-large', 'Coastal Luggage - Large', 'luggage', 'Coastal', 'check-in-large', None, ('travel',), (), None, 25900, 42900, 210, '2026-01-12', 'CST-LRG', ('DEB', 'NSH')),
    ('contour-luggage-cabin', 'Contour Luggage - Cabin', 'luggage', 'Contour', 'cabin', None, ('travel',), ('clearance',), None, 17900, 29900, 240, '2025-09-01', 'CTR-CAB', ('FLA', 'CSP', 'NSH')),
    ('contour-luggage-medium', 'Contour Luggage - Medium', 'luggage', 'Contour', 'check-in', None, ('travel',), ('clearance',), None, 22900, 37900, 150, '2025-09-01', 'CTR-MED', ('FLA', 'NSH')),
    ('contour-luggage-large', 'Contour Luggage - Large', 'luggage', 'Contour', 'check-in-large', None, ('travel',), ('clearance',), None, 25900, 42900, 90, '2025-09-01', 'CTR-LRG', ('FLA', 'NSH')),
    ('ridge-trunk-medium', 'Ridge Trunk - Medium', 'luggage', 'Ridge', 'trunk', None, ('travel',), (), None, 28900, 45900, 420, '2026-06-22', 'RDG-TRM', ('NSH', 'CMI', 'SFL')),
    ('ridge-trunk-large', 'Ridge Trunk - Large', 'luggage', 'Ridge', 'trunk', None, ('travel',), (), None, 31900, 49900, 180, '2026-06-22', 'RDG-TRL', ('NSH', 'SFL')),
    ('ridge-cabin-pro', 'Ridge Cabin Pro', 'luggage', 'Ridge', 'cabin', None, ('work', 'travel'), ('tech',), 'must-have', 19900, 32900, 560, '2026-07-06', 'RDG-CPR', ('NSH', 'CMI')),
    ('solstice-kids-cabin', 'Solstice Kids Cabin', 'luggage', 'Solstice', 'kids', None, ('travel', 'diaper-and-kids'), (), None, 9900, 15900, 270, '2026-04-06', 'SLS-KCB', ('CSP', 'FLA', 'DEB')),
    ('solstice-kids-trolley', 'Solstice Kids Trolley', 'luggage', 'Solstice', 'kids', None, ('travel', 'diaper-and-kids'), (), None, 11900, 18900, 140, '2026-04-06', 'SLS-KTR', ('CSP', 'DEB')),
    ('solstice-luggage-set-of-2', 'Solstice Luggage - Set of 2', 'luggage', 'Solstice', 'set', None, ('travel',), (), None, 18900, 31900, 120, '2026-04-13', 'SLS-SET', ('SSU', 'LWR')),
    ('passage-backpack-30l', 'Passage Backpack - 30L', 'backpacks-and-briefcases', 'Passage', None, 'backpack', ('work', 'travel'), ('tech',), 'hot', 8900, 14900, 900, '2026-02-16', 'PSG-B30', ('NSH', 'OLV', 'HTG')),
    ('overnight-backpack-23l', 'Overnight Backpack - 23L', 'backpacks-and-briefcases', 'Meridian', None, 'backpack', ('travel',), ('tech',), None, 7900, 12900, 480, '2026-02-23', 'OVN-B23', ('NSH', 'DEB')),
    ('kettle-backpack', 'Kettle Backpack', 'backpacks-and-briefcases', None, None, 'backpack', ('work',), (), None, 6900, 10900, 350, '2025-11-03', 'KTL-BPK', ('HTG', 'SSU', 'CSP')),
    ('swerve-backpack', 'Swerve Backpack', 'backpacks-and-briefcases', None, None, 'backpack', ('travel',), ('clearance',), None, 5900, 9900, 160, '2025-08-11', 'SWV-BPK', ('NSH', 'FLA')),
    ('passage-briefcase', 'Passage Briefcase', 'backpacks-and-briefcases', 'Passage', None, 'briefcase', ('work',), ('tech',), None, 11900, 19900, 230, '2026-02-16', 'PSG-BRF', ('NSH', 'HTG')),
    ('transit-duffle', 'Transit Duffle', 'backpacks-and-briefcases', None, None, 'duffle', ('travel',), (), None, 9900, 16900, 310, '2026-07-20', 'TRN-DUF', ('NSH', 'OLV')),
    ('nest-diaper-backpack', 'Nest Diaper Backpack', 'backpacks-and-briefcases', None, None, 'diaper-bag', ('diaper-and-kids',), (), None, 7900, 12900, 200, '2026-08-03', 'NST-DBP', ('SSU', 'HTG')),
    ('solstice-kids-backpack', 'Solstice Kids Backpack', 'backpacks-and-briefcases', 'Solstice', None, 'kids-backpack', ('diaper-and-kids',), (), None, 4900, 7900, 170, '2026-04-06', 'SLS-KBP', ('CSP', 'FLA')),
    ('marigold-tote', 'Marigold Tote', 'totes', None, None, None, ('work',), (), None, 6900, 11900, 640, '2026-03-30', 'MRG-TOT', ('FLA', 'SSU')),
    ('ripple-tote', 'Ripple Tote', 'totes', None, None, None, ('work',), (), 'must-have', 6900, 11900, 590, '2026-06-08', 'RPL-TOT', ('DEB', 'SFL', 'NSH')),
    ('coastal-weekender', 'Coastal Weekender', 'totes', 'Coastal', None, None, ('travel',), (), None, 7900, 12900, 280, '2026-01-19', 'CST-WKD', ('DEB', 'SSU')),
    ('mini-sling', 'Mini Sling', 'slings-and-crossbodies', None, None, None, ('travel',), (), 'hot', 4900, 7900, 820, '2026-05-04', 'MNI-SLG', ('NSH', 'CSP', 'OLV')),
    ('passage-crossbody', 'Passage Crossbody', 'slings-and-crossbodies', 'Passage', None, None, ('travel',), (), None, 5900, 9900, 250, '2026-02-16', 'PSG-XBD', ('NSH', 'HTG')),
    ('packing-cubes-set-of-6', 'Packing Cubes (Set of 6)', 'accessories', None, None, None, ('travel',), (), None, 2900, 2900, 700, '2025-10-06', 'PCK-CUB', ('HTG', 'SSU')),
    ('travel-pillow', 'Travel Pillow', 'accessories', None, None, None, ('travel',), (), None, 3500, 3500, 440, '2025-10-06', 'TRV-PLW', ('HTG', 'DEB')),
    ('stretch-luggage-cover', 'Stretch Luggage Cover', 'accessories', None, None, None, ('travel',), (), None, 2400, 2400, 100, '2025-10-20', 'STR-CVR', ('NSH',)),
    ('vault-card-sleeve', 'Vault Card Sleeve', 'wallets', None, None, None, ('work',), (), None, 3900, 5900, 660, '2026-08-17', 'VLT-SLV', ('NSH', 'OLV')),
    ('vault-bifold-wallet', 'Vault Bifold Wallet', 'wallets', None, None, None, ('work',), (), None, 5900, 5900, 390, '2026-08-17', 'VLT-BIF', ('NSH', 'HTG')),
    ('vault-card-case', 'Vault Card Case', 'wallets', None, None, None, ('work',), (), None, 4900, 4900, 130, '2026-08-24', 'VLT-CSE', ('NSH', 'SFL')),
)

PRICE_EXCEPTIONS = {'MRD-CAB-STB': (19900, 29900)}

STOCK_EXCEPTIONS = {'PSG-CAB-CSP': 0, 'CTR-CAB-CSP': 2, 'RDG-TRL-SFL': 1, 'VLT-CSE-NSH': 0}

COLLECTIONS = (
    ('passage', 'Passage', 'line', 'The everyday classic, refined', 7),
    ('meridian', 'Meridian', 'line', 'The new face of movement', 5),
    ('coastal', 'Coastal', 'line', 'Salt air, sure footing', 4),
    ('contour', 'Contour', 'line', 'Lines that hold their shape', 3),
    ('ridge', 'Ridge', 'line', 'Trunks for the long haul', 3),
    ('solstice', 'Solstice', 'line', 'Small cases for small travellers', 4),
    ('tech-range', 'Tech Range', 'size', 'Room for the laptop, too', 4),
    ('cabin', 'Cabin', 'size', 'Made for the overhead bin', 5),
    ('check-in', 'Check-in', 'size', 'A week away, sorted', 4),
    ('check-in-large', 'Check-in Large', 'size', 'For the long trip', 4),
    ('trunk', 'Trunk', 'size', 'Deep enough for everything', 2),
    ('kids-luggage', 'Kids Luggage', 'size', 'Their own suitcase at last', 2),
    ('sets', 'Sets', 'size', 'More pieces, less to pay', 3),
    ('luggage', 'Luggage', 'category', 'Every suitcase we make', 20),
    ('backpacks-and-briefcases', 'Backpacks & Briefcases', 'category', 'Carry for the commute and beyond', 8),
    ('totes', 'Totes', 'category', 'Open, easy, everyday', 3),
    ('slings-and-crossbodies', 'Slings & Crossbodies', 'category', 'Hands free, essentials close', 2),
    ('accessories', 'Accessories', 'category', 'Small things that make a trip', 3),
    ('wallets', 'Wallets', 'category', 'Slim by design', 3),
    ('backpacks', 'Backpacks', 'type', 'Two straps, every day', 4),
    ('briefcases', 'Briefcases', 'type', 'Sharp for the office', 1),
    ('duffles', 'Duffles', 'type', 'Throw it all in', 1),
    ('diaper-bags', 'Diaper Bags', 'type', 'Ready for small emergencies', 1),
    ('kids-backpacks', 'Kids Backpacks', 'type', 'Sized for school days', 1),
    ('work', 'Work', 'use', 'Built for the working week', 9),
    ('travel', 'Travel', 'use', 'Pack once, go anywhere', 30),
    ('diaper-and-kids', 'Diaper & Kids', 'use', 'For the smallest travellers', 4),
    ('best-sellers', 'Best Sellers', 'highlight', 'What everyone is packing', 20),
    ('on-sale', 'On Sale', 'highlight', 'Road Week prices', 34),
    ('clearance-sale', 'Clearance Sale', 'highlight', 'Last call on these', 4),
    ('all', 'All Products', 'all', 'The whole range', 39),
)

RULE_MEMBERS = (
    ('passage', ('Passage Luggage - Cabin', 'Passage Luggage - Medium', 'Passage Luggage - Large', 'Passage Luggage - Set of 3', 'Passage Backpack - 30L', 'Passage Briefcase', 'Passage Crossbody')),
    ('meridian', ('Meridian Luggage - Cabin', 'Meridian Luggage - Medium', 'Meridian Luggage - Large', 'Meridian Luggage - Set of 3', 'Overnight Backpack - 23L')),
    ('coastal', ('Coastal Luggage - Cabin', 'Coastal Luggage - Medium', 'Coastal Luggage - Large', 'Coastal Weekender')),
    ('contour', ('Contour Luggage - Cabin', 'Contour Luggage - Medium', 'Contour Luggage - Large')),
    ('ridge', ('Ridge Trunk - Medium', 'Ridge Trunk - Large', 'Ridge Cabin Pro')),
    ('solstice', ('Solstice Kids Cabin', 'Solstice Kids Trolley', 'Solstice Luggage - Set of 2', 'Solstice Kids Backpack')),
    ('tech-range', ('Ridge Cabin Pro', 'Passage Backpack - 30L', 'Overnight Backpack - 23L', 'Passage Briefcase')),
    ('cabin', ('Passage Luggage - Cabin', 'Meridian Luggage - Cabin', 'Coastal Luggage - Cabin', 'Contour Luggage - Cabin', 'Ridge Cabin Pro')),
    ('check-in', ('Passage Luggage - Medium', 'Meridian Luggage - Medium', 'Coastal Luggage - Medium', 'Contour Luggage - Medium')),
    ('check-in-large', ('Passage Luggage - Large', 'Meridian Luggage - Large', 'Coastal Luggage - Large', 'Contour Luggage - Large')),
    ('trunk', ('Ridge Trunk - Medium', 'Ridge Trunk - Large')),
    ('kids-luggage', ('Solstice Kids Cabin', 'Solstice Kids Trolley')),
    ('sets', ('Passage Luggage - Set of 3', 'Meridian Luggage - Set of 3', 'Solstice Luggage - Set of 2')),
    ('luggage', ('Passage Luggage - Cabin', 'Passage Luggage - Medium', 'Passage Luggage - Large', 'Passage Luggage - Set of 3', 'Meridian Luggage - Cabin', 'Meridian Luggage - Medium', 'Meridian Luggage - Large', 'Meridian Luggage - Set of 3', 'Coastal Luggage - Cabin', 'Coastal Luggage - Medium', 'Coastal Luggage - Large', 'Contour Luggage - Cabin', 'Contour Luggage - Medium', 'Contour Luggage - Large', 'Ridge Trunk - Medium', 'Ridge Trunk - Large', 'Ridge Cabin Pro', 'Solstice Kids Cabin', 'Solstice Kids Trolley', 'Solstice Luggage - Set of 2')),
    ('backpacks-and-briefcases', ('Passage Backpack - 30L', 'Overnight Backpack - 23L', 'Kettle Backpack', 'Swerve Backpack', 'Passage Briefcase', 'Transit Duffle', 'Nest Diaper Backpack', 'Solstice Kids Backpack')),
    ('totes', ('Marigold Tote', 'Ripple Tote', 'Coastal Weekender')),
    ('slings-and-crossbodies', ('Mini Sling', 'Passage Crossbody')),
    ('accessories', ('Packing Cubes (Set of 6)', 'Travel Pillow', 'Stretch Luggage Cover')),
    ('wallets', ('Vault Card Sleeve', 'Vault Bifold Wallet', 'Vault Card Case')),
    ('backpacks', ('Passage Backpack - 30L', 'Overnight Backpack - 23L', 'Kettle Backpack', 'Swerve Backpack')),
    ('briefcases', ('Passage Briefcase',)),
    ('duffles', ('Transit Duffle',)),
    ('diaper-bags', ('Nest Diaper Backpack',)),
    ('kids-backpacks', ('Solstice Kids Backpack',)),
    ('work', ('Ridge Cabin Pro', 'Passage Backpack - 30L', 'Kettle Backpack', 'Passage Briefcase', 'Marigold Tote', 'Ripple Tote', 'Vault Card Sleeve', 'Vault Bifold Wallet', 'Vault Card Case')),
    ('travel', ('Passage Luggage - Cabin', 'Passage Luggage - Medium', 'Passage Luggage - Large', 'Passage Luggage - Set of 3', 'Meridian Luggage - Cabin', 'Meridian Luggage - Medium', 'Meridian Luggage - Large', 'Meridian Luggage - Set of 3', 'Coastal Luggage - Cabin', 'Coastal Luggage - Medium', 'Coastal Luggage - Large', 'Contour Luggage - Cabin', 'Contour Luggage - Medium', 'Contour Luggage - Large', 'Ridge Trunk - Medium', 'Ridge Trunk - Large', 'Ridge Cabin Pro', 'Solstice Kids Cabin', 'Solstice Kids Trolley', 'Solstice Luggage - Set of 2', 'Passage Backpack - 30L', 'Overnight Backpack - 23L', 'Swerve Backpack', 'Transit Duffle', 'Coastal Weekender', 'Mini Sling', 'Passage Crossbody', 'Packing Cubes (Set of 6)', 'Travel Pillow', 'Stretch Luggage Cover')),
    ('diaper-and-kids', ('Solstice Kids Cabin', 'Solstice Kids Trolley', 'Nest Diaper Backpack', 'Solstice Kids Backpack')),
    ('clearance-sale', ('Contour Luggage - Cabin', 'Contour Luggage - Medium', 'Contour Luggage - Large', 'Swerve Backpack')),
)

STORES = (
    ('South Congress', 'Austin', 'TX', '1400 South Congress Avenue', '78704', '+1 512 555 0131', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Newbury Street', 'Boston', 'MA', '234 Newbury Street', '02116', '+1 617 555 0142', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Fulton Market', 'Chicago', 'IL', '900 West Randolph Street', '60607', '+1 312 555 0153', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Magnificent Mile', 'Chicago', 'IL', '540 North Michigan Avenue', '60611', '+1 312 555 0164', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('LoDo', 'Denver', 'CO', '1650 Wazee Street', '80202', '+1 303 555 0175', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Abbot Kinney', 'Los Angeles', 'CA', '1305 Abbot Kinney Boulevard', '90291', '+1 310 555 0186', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Wynwood', 'Miami', 'FL', '2520 NW 2nd Avenue', '33127', '+1 305 555 0197', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Hudson Yards', 'New York', 'NY', '20 Hudson Yards', '10001', '+1 212 555 0108', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('SoHo', 'New York', 'NY', '118 Greene Street', '10012', '+1 212 555 0119', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Lloyd Center', 'Portland', 'OR', '2201 Lloyd Center', '97232', '+1 503 555 0120', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Pearl District', 'Portland', 'OR', '1120 NW Couch Street', '97209', '+1 503 555 0110', 'Mon to Sun 10:00 to 21:00'),
    ('Hayes Valley', 'San Francisco', 'CA', '432 Hayes Street', '94102', '+1 415 555 0121', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Union Square', 'San Francisco', 'CA', "170 O'Farrell Street", '94102', '+1 415 555 0132', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
    ('Pike Place', 'Seattle', 'WA', '1501 Pike Place', '98101', '+1 206 555 0143', 'Mon to Sat 10:00 to 20:00, Sun 11:00 to 18:00'),
)


VARIANT_COUNT = sum(len(row[14]) for row in PRODUCTS)


def settle() -> None:
    """Yield briefly so an asynchronous side effect can land."""
    time.sleep(SETTLE_SECONDS)


def poll_until(predicate, timeout: float = POLL_TIMEOUT_SECONDS):
    """Bounded poll on a monotonic clock; returns the last value the predicate saw."""
    deadline = time.monotonic() + timeout
    value = None
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        settle()
    return value


def run_together(*calls):
    """Start every call at once and return their results in order."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(call) for call in calls]
        return [f.result() for f in futures]


def unique_suffix() -> str:
    return os.urandom(5).hex()


def probe_address(suffix: str) -> str:
    """A per-run address, only ever compared against itself."""
    return "probe-" + suffix + "@" + "example.com"


def probe_password(suffix: str) -> str:
    return "probe-pass-" + suffix


def checkout_key() -> str:
    return "probe-key-" + os.urandom(8).hex()


def now_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def today_utc() -> datetime.date:
    return now_utc().date()


def iso_from_now(seconds: float) -> str:
    stamp = now_utc() + datetime.timedelta(seconds=seconds)
    return stamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def parse_stamp(value: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def date_of(value: str) -> datetime.date:
    return datetime.date.fromisoformat(str(value)[:10])


def describe(response: httpx.Response, what: str) -> str:
    """Anchor, request, status and body for a failure message."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def api(token: str | None = None) -> httpx.Client:
    return appclient.client(token)


def login(email: str, password: str = SEEDED_PASSWORD) -> str:
    return appclient.login(email, password)


def login_response(email: str, password: str, **extra) -> httpx.Response:
    with api() as client:
        return client.post("/auth/login", json={"email": email, "password": password, **extra})


def body_of(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return {}
    return response.json()


def message_of(response: httpx.Response) -> str:
    payload = body_of(response)
    return payload.get("message", "") if isinstance(payload, dict) else ""


def error_of(response: httpx.Response) -> str:
    payload = body_of(response)
    return payload.get("error", "") if isinstance(payload, dict) else ""


def listing(response: httpx.Response) -> list:
    assert response.status_code == 200, describe(response, "a list endpoint must answer 200")
    return _shapes.items(response.json())


def top_level_array(response: httpx.Response) -> list:
    assert response.status_code == 200, describe(response, "a list endpoint must answer 200")
    payload = response.json()
    assert isinstance(payload, list), describe(response, "a list endpoint returns a top-level array")
    return payload


def is_client_error(response: httpx.Response) -> bool:
    return 400 <= response.status_code < 500


def accepted(response: httpx.Response) -> bool:
    return 200 <= response.status_code <= 204


def denied(response: httpx.Response) -> bool:
    return response.status_code in (401, 403, 404)


def backend() -> capabilities.Backend:
    return capabilities.make_backend()


def sql(query: str, *params) -> list[dict]:
    return backend().query(query, tuple(params))


def scalar(query: str, *params):
    rows = sql(query, *params)
    if not rows:
        return None
    return next(iter(rows[0].values()))


def table_columns(table: str) -> set[str]:
    rows = sql("SELECT column_name FROM information_schema.columns WHERE table_name = %s", table)
    return {r["column_name"] for r in rows}


def money(cents: int) -> str:
    whole, rest = divmod(int(cents), 100)
    text = f"${whole:,}"
    return text if rest == 0 else f"{text}.{rest:02d}"


def first_instalment(cents: int) -> int:
    return math.ceil(int(cents) / 4)


def discount_percent(price: int, list_price: int) -> int:
    whole, rest = divmod((list_price - price) * 100, list_price)
    return whole + (1 if rest * 2 >= list_price else 0)


def subject_for(number: str) -> str:
    return f"Your valisette order {number} is confirmed"


def opening_for(number: str, total: int) -> str:
    return f"Order {number}, total charged {money(total)}."


def only_left(available: int) -> str:
    return f"Only {available} left in stock."


def currency_refusal(currency: str) -> str:
    return (f"That corporate account is billed in {currency}. "
            f"Corporate orders are billed in USD.")


def external_key(number: str) -> str:
    return EXTERNAL_KEY_PREFIX + number


def product_row(handle: str) -> tuple:
    found = [p for p in PRODUCTS if p[0] == handle]
    assert found, f"{handle} is not a pinned product"
    return found[0]


def handle_of_sku(sku: str) -> str:
    prefix = sku.rsplit("-", 1)[0]
    found = [p[0] for p in PRODUCTS if p[13] == prefix]
    assert found, f"{sku} has no pinned product prefix"
    return found[0]


def pinned_variants():
    """(handle, sku, colourway, family, price, list_price, table stock) in table order."""
    names = {code: (name, family) for name, code, family in COLOURWAYS}
    for row in PRODUCTS:
        for code in row[14]:
            sku = f"{row[13]}-{code}"
            price, list_price = PRICE_EXCEPTIONS.get(sku, (row[9], row[10]))
            yield (row[0], sku, names[code][0], names[code][1], price, list_price,
                   STOCK_EXCEPTIONS.get(sku, DEFAULT_STOCK))


def product(handle: str, token: str | None = None) -> dict:
    with api(token) as client:
        response = client.get(f"/products/{handle}")
    assert response.status_code == 200, describe(response, f"product {handle} must be readable")
    return response.json()


def variant(sku: str) -> dict:
    found = [v for v in product(handle_of_sku(sku)).get("variants", []) if v.get("sku") == sku]
    assert found, f"{sku} is missing from its product read"
    return found[0]


def stock_of(sku: str) -> int:
    return int(variant(sku)["stock"])


def collection(handle: str) -> dict:
    with api() as client:
        response = client.get(f"/collections/{handle}")
    assert response.status_code == 200, describe(response, f"collection {handle} must be readable")
    return response.json()


def collection_page(handle: str, **params) -> dict:
    with api() as client:
        response = client.get(f"/collections/{handle}/products", params=params)
    assert response.status_code == 200, describe(response, f"collection {handle} products")
    return response.json()


def collection_titles(handle: str, **params) -> list[str]:
    """Every card title of a collection, following the pages to the end."""
    titles, page_no = [], 1
    while True:
        payload = collection_page(handle, page=page_no, **params)
        titles += [card["title"] for card in payload["products"]]
        if len(titles) >= payload["total"] or not payload["products"]:
            return titles
        page_no += 1


def search(query: str, **params) -> dict:
    with api() as client:
        response = client.get("/search", params={"q": query, **params})
    assert response.status_code == 200, describe(response, f"search {query}")
    return response.json()


def sale(token: str | None = None) -> dict:
    with api(token) as client:
        response = client.get("/sale")
    assert response.status_code == 200, describe(response, "the sale must be readable")
    return response.json()


def move_sale_end(owner_token: str, ends_at: str) -> httpx.Response:
    with api(owner_token) as client:
        return client.patch("/owner/sale", json={"ends_at": ends_at})


def new_cart(token: str | None = None) -> str:
    with api(token) as client:
        response = client.post("/carts")
    assert accepted(response), describe(response, "a cart must be created")
    cart_token = response.json().get("token")
    assert cart_token, describe(response, "a new cart carries its token")
    return cart_token


def cart(cart_token: str) -> dict:
    with api() as client:
        response = client.get(f"/carts/{cart_token}")
    assert response.status_code == 200, describe(response, "a cart must be readable")
    return response.json()


def add_line(cart_token: str, sku: str, quantity: int = 1, properties: dict | None = None,
             token: str | None = None) -> httpx.Response:
    body = {"sku": sku, "quantity": quantity}
    if properties is not None:
        body["properties"] = properties
    with api(token) as client:
        return client.post(f"/carts/{cart_token}/lines", json=body)


def change_line(cart_token: str, line_id, quantity: int) -> httpx.Response:
    with api() as client:
        return client.patch(f"/carts/{cart_token}/lines/{line_id}", json={"quantity": quantity})


def remove_line(cart_token: str, line_id) -> httpx.Response:
    with api() as client:
        return client.delete(f"/carts/{cart_token}/lines/{line_id}")


def filled_cart(lines, token: str | None = None) -> str:
    cart_token = new_cart(token)
    for sku, quantity in lines:
        response = add_line(cart_token, sku, quantity)
        assert accepted(response), describe(response, f"{quantity} x {sku} must join the cart")
    return cart_token


def delivery_address(**overrides) -> dict:
    body = {"name": "Probe Shopper", "line1": "1 Probe Way", "line2": "",
            "city": "Portland", "region": "OR", "postcode": "97205", "country": COUNTRY,
            "phone": "+1 503 555 0100"}
    body.update(overrides)
    return body


def checkout(cart_token: str, email: str | None = None, method: str = STANDARD,
             key: str | None = None, token: str | None = None, corporate: str | None = None,
             address: dict | None = None) -> httpx.Response:
    body = {"cart_token": cart_token, "checkout_key": key or checkout_key(),
            "email": email or probe_address(unique_suffix()),
            "address": address or delivery_address(), "delivery_method": method}
    if corporate is not None:
        body["corporate_account"] = corporate
    with api(token) as client:
        return client.post("/checkout", json=body)


def place_order(lines, method: str = STANDARD, token: str | None = None,
                email: str | None = None) -> dict:
    ensure_stock([sku for sku, _ in lines])
    cart_token = filled_cart(lines, token)
    response = checkout(cart_token, email=email, method=method, token=token)
    assert response.status_code in (200, 201), describe(response, "an in-stock checkout must pass")
    order = response.json()
    order["cart_token"] = cart_token
    return order


def owner_token() -> str:
    return login(OWNER_EMAIL)


def movements(sku: str, token: str | None = None) -> list:
    with api(token or owner_token()) as client:
        return top_level_array(client.get("/owner/stock-movements", params={"sku": sku}))


def record_movement(sku: str, delta: int, kind: str, token: str | None = None,
                    note: str = "probe movement") -> httpx.Response:
    with api(token or owner_token()) as client:
        return client.post("/owner/stock-movements",
                           json={"sku": sku, "delta": delta, "kind": kind, "note": note})


def set_stock(sku: str, target: int) -> None:
    current = stock_of(sku)
    if current == target:
        return
    kind = MOVE_RESTOCK if target > current else MOVE_ADJUSTMENT
    response = record_movement(sku, target - current, kind)
    assert accepted(response), describe(response, f"the owner must move {sku} to {target}")


def ensure_stock(skus, minimum: int = 10) -> None:
    for sku in skus:
        current = stock_of(sku)
        if current < minimum:
            response = record_movement(sku, minimum - current, MOVE_RESTOCK)
            assert accepted(response), describe(response, f"the owner must restock {sku}")


def owner_orders(token: str | None = None) -> list:
    with api(token or owner_token()) as client:
        return top_level_array(client.get("/owner/orders"))


def owner_order(number: str, token: str | None = None) -> dict:
    found = [o for o in owner_orders(token) if o.get("number") == number]
    assert found, f"{number} is missing from the owner order list"
    return found[0]


def order_row(number: str) -> dict | None:
    rows = sql("SELECT * FROM orders WHERE number = %s", number)
    return rows[0] if rows else None


def orders_for_key(key: str) -> int:
    return int(scalar("SELECT count(*) FROM orders WHERE checkout_key = %s", key))


def order_count() -> int:
    return int(scalar("SELECT count(*) FROM orders"))


def movement_count() -> int:
    return int(scalar("SELECT count(*) FROM stock_movement"))


def movement_sum(sku: str) -> int:
    return int(scalar(
        "SELECT coalesce(sum(m.delta), 0) FROM stock_movement m "
        "JOIN variant v ON v.id = m.variant_id WHERE v.sku = %s", sku))


def units_since_start(handle: str) -> int:
    return int(scalar(
        "SELECT coalesce(sum(l.quantity), 0) FROM order_line l "
        "JOIN orders o ON o.id = l.order_id JOIN variant v ON v.id = l.variant_id "
        "JOIN product p ON p.id = v.product_id "
        "WHERE p.handle = %s AND o.state IN ('paid', 'fulfilled') "
        "AND o.number NOT IN ('VS-100001', 'VS-100002', 'VS-100003')", handle))


def signup(suffix: str, **extra) -> dict:
    body = {"name": "Probe " + suffix, "email": probe_address(suffix),
            "password": probe_password(suffix)}
    body.update(extra)
    with api() as client:
        response = client.post("/auth/signup", json=body)
    assert accepted(response), describe(response, "an open signup must succeed")
    payload = response.json()
    assert payload.get("access_token"), describe(response, "a signup returns an access_token")
    return {"token": payload["access_token"], "email": body["email"],
            "password": body["password"], "payload": payload}


def me(token: str) -> httpx.Response:
    with api(token) as client:
        return client.get("/me")


def save_address(token: str, **fields) -> httpx.Response:
    with api(token) as client:
        return client.post("/me/addresses", json=delivery_address(**fields))


def addresses(token: str) -> list:
    with api(token) as client:
        return top_level_array(client.get("/me/addresses"))


def kb_client() -> httpx.Client:
    capabilities.selected("payments")
    return httpx.Client(
        base_url=os.environ["PAYMENTS_API_URL"].rstrip("/"), timeout=appclient.TIMEOUT,
        auth=(os.environ["PAYMENTS_ADMIN_USER"], os.environ["PAYMENTS_ADMIN_PASSWORD"]),
        headers={"X-Killbill-ApiKey": os.environ["PAYMENTS_API_KEY"],
                 "X-Killbill-ApiSecret": os.environ["PAYMENTS_API_SECRET"],
                 "X-Killbill-CreatedBy": "deku-verifier", "Accept": "application/json"})


def kb_account(key: str) -> httpx.Response:
    with kb_client() as client:
        return client.get(KB_ACCOUNTS_PATH, params={"externalKey": key})


def kb_open_account(key: str, name: str, email: str) -> httpx.Response:
    body = {"name": name, "externalKey": key, "email": email, "currency": KB_USD,
            "country": COUNTRY}
    with kb_client() as client:
        return client.post(KB_ACCOUNTS_PATH, json=body)


def inbox() -> capabilities.Inbox:
    return capabilities.make_inbox()


def mail_client() -> httpx.Client:
    capabilities.selected("email")
    base = os.environ["EMAIL_INBOX_API_URL"].rstrip("/") + "/api" + "/v1"
    return httpx.Client(base_url=base, timeout=appclient.TIMEOUT)


def mail_to(address: str) -> list[dict]:
    """Every Mailpit summary addressed to one recipient."""
    with mail_client() as client:
        response = client.get("/search", params={"query": f"to:\"{address}\"",
                                                       "limit": 200})
    assert response.status_code == 200, describe(response, "the Mailpit search must answer")
    rows = response.json().get("messages", [])
    return [m for m in rows
            if any(address.lower() == (a.get("Address") or "").lower() for a in m.get("To", []))]


def mail_text(summary: dict) -> str:
    with mail_client() as client:
        response = client.get(f"/message/{summary['ID']}")
    assert response.status_code == 200, describe(response, "a Mailpit message must be readable")
    payload = response.json()
    return payload.get("Text") or payload.get("HTML") or ""


def wait_for_mail(address: str, count: int = 1) -> list[dict]:
    def enough():
        rows = mail_to(address)
        return rows if len(rows) >= count else None
    return poll_until(enough) or mail_to(address)


def app_url() -> str:
    return appclient.app_url()


def api_base() -> str:
    return appclient.api_base()


def fetch_asset(src: str) -> httpx.Response:
    if src.startswith("http"):
        return fetch_document(app_path(src))
    return fetch_document(src if src.startswith("/") else "/" + src)


def fetch_document(path: str, token: str | None = None, follow: bool = True) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.get(appclient.app_url() + path, timeout=appclient.TIMEOUT,
                     follow_redirects=follow, headers=headers)


def unescape(text: str) -> str:
    return (text.replace("&amp;", "&").replace("&#39;", "'").replace("&#x27;", "'")
            .replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">"))


def head_tags(markup: str, tag: str) -> list[str]:
    lower = markup.lower()
    end = lower.find("</head>")
    head = markup[:end] if end > 0 else markup
    return re.findall(r"<" + tag + r"\b[^>]*>", head, flags=re.IGNORECASE)


def attribute(tag: str, name: str) -> str:
    match = re.search(r"\b" + re.escape(name) + r"\s*=\s*([\"'])(.*?)\1", tag,
                      flags=re.IGNORECASE | re.DOTALL)
    return match.group(2) if match else ""


def favicon_href(markup: str) -> str:
    for tag in head_tags(markup, "link"):
        if "icon" in attribute(tag, "rel").lower().split():
            return attribute(tag, "href")
    return ""


def script_sources(markup: str) -> list[str]:
    return [attribute(tag, "src") for tag in re.findall(r"<script\b[^>]*>", markup,
                                                        flags=re.IGNORECASE)
            if attribute(tag, "src")]


def app_path(url: str) -> str:
    base = appclient.app_url()
    return url[len(base):] if url.startswith(base) else url


def open_page(page, path: str):
    page.goto(appclient.app_url() + path, wait_until="networkidle")
    return page


def page_text(page) -> str:
    return page.evaluate("() => document.body ? document.body.innerText : ''") or ""


def collect_requests(page) -> list:
    seen = []
    page.on("request", lambda request: seen.append((request.url, request.resource_type)))
    return seen


def cart_token_in_page(page, sku: str) -> str:
    """The cart token the page holds, found in its storage or cookies and confirmed by the API."""
    values = page.evaluate(
        "() => [...Object.values(localStorage), ...Object.values(sessionStorage)]") or []
    values += [cookie["value"] for cookie in page.context.cookies()]
    candidates = []
    for value in values:
        for found in re.findall(r"[A-Za-z0-9]{24,}", str(value)):
            if found not in candidates:
                candidates.append(found)
    with api() as client:
        for found in candidates:
            response = client.get(f"/carts/{found}")
            if response.status_code == 200 and any(
                    line.get("sku") == sku for line in response.json().get("lines", [])):
                return found
    return ""


def product_handles_shown(page) -> list[str]:
    hrefs = page.evaluate(
        "() => Array.from(document.querySelectorAll('main a[href*=\"/products/\"]'))"
        ".map(a => a.getAttribute('href'))") or []
    seen = []
    for href in hrefs:
        handle = href.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
        if handle not in seen:
            seen.append(handle)
    return seen


def unnamed_controls(page) -> list[str]:
    return page.evaluate(
        "() => Array.from(document.querySelectorAll('button, a[href]'))"
        ".filter(e => e.offsetParent !== null && !(e.innerText || '').trim())"
        ".filter(e => !(e.getAttribute('aria-label') || e.getAttribute('title') || "
        "e.getAttribute('aria-labelledby') || e.querySelector('[aria-label], [alt]')))"
        ".map(e => e.outerHTML.slice(0, 120))") or []


def internal_hrefs(page) -> list[str]:
    hrefs = page.evaluate(
        "() => Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))")
    out = []
    for href in hrefs or []:
        if href.startswith("/") and not href.startswith("//"):
            out.append(href.split("#")[0] or "/")
        elif href.startswith(appclient.app_url()):
            out.append(app_path(href).split("#")[0] or "/")
    return sorted(set(out))


def countdown_seconds(page) -> int:
    values = page.evaluate(
        "() => Object.fromEntries(Array.from(document.querySelectorAll('[data-unit]'))"
        ".map(e => [e.getAttribute('data-unit'), e.textContent.trim()]))")
    digits = {unit: int(re.sub(r"\D", "", values.get(unit, "0")) or 0) for unit in "dhms"}
    return digits["d"] * 86400 + digits["h"] * 3600 + digits["m"] * 60 + digits["s"]


def seconds_until(ends_at: str, server_time: str) -> float:
    return (parse_stamp(ends_at) - parse_stamp(server_time)).total_seconds()


def clock_offset_time(days: int) -> datetime.datetime:
    return now_utc() + datetime.timedelta(days=days)


def gzip_size(data: bytes) -> int:
    return len(gzip.compress(data))


@pytest.fixture()
def suffix() -> str:
    return unique_suffix()


@pytest.fixture()
def owner() -> str:
    return login(OWNER_EMAIL)


@pytest.fixture()
def customer() -> str:
    return login(CUSTOMER_EMAIL)


@pytest.fixture()
def customer2() -> str:
    return login(CUSTOMER2_EMAIL)


@pytest.fixture()
def shopper(suffix) -> dict:
    return signup(suffix)


@pytest.fixture()
def page():
    with sync_playwright() as runner:
        browser = runner.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        tab = context.new_page()
        tab.set_default_timeout(PAGE_TIMEOUT_MS)
        yield tab
        context.close()
        browser.close()
