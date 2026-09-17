from __future__ import annotations

import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import httpx
from _shapes import flatten, items
from appclient import client
from conftest import (
    ACCEPTED,
    ARTICLE_TOTALS,
    AUTHORED_SIZES,
    CATALOGUE_DOCUMENTS,
    CATEGORY_COUNTS,
    COMMERCIAL_EMAIL,
    CONSENT_COOKIE,
    CONTACT_SUBJECT,
    DENIED,
    EDITOR_EMAIL,
    EDUCATIONAL_SLUG,
    ENGLISH_COLLECTION_COUNTS,
    FORBIDDEN_IN_BUNDLES,
    FOURTEEN_DAYS_SECONDS,
    FRAME_BOLLARD_ID,
    FRAME_BOLLARD_SLUG,
    GOLF_BAG_STAND_ID,
    GRANT_REDEMPTIONS,
    GRANT_SUBJECT_PREFIX,
    INVALID,
    JOB_TITLES,
    LEAD_LIMIT_PER_HOUR,
    LINE_DOOR_PLATE_SLUG,
    LOCALE_COOKIE,
    LOCALE_TOTALS,
    NEWSLETTER_SUBJECT,
    NOT_CHOSEN,
    PLAZA_BENCH_2000_DIMENSIONS,
    PLAZA_BENCH_COLORS,
    PLAZA_BENCH_ID,
    PLAZA_BENCH_PT_SLUG,
    PLAZA_BENCH_PT_TITLE,
    PLAZA_BENCH_REFERENCE_CODE,
    PLAZA_BENCH_SIZES,
    PLAZA_BENCH_SLUG,
    PLAZA_BENCH_STRUCTURES,
    PLAZA_BENCH_TITLE,
    PRIVACY_SENTENCE,
    QUOTATION_SUBJECT_PREFIX,
    RECENT_SLUGS,
    REFERENCE_RE,
    REUSE_BIN_SLUG,
    RIDGE_SLUG,
    ROLE_VALUE,
    ROOM_SIGN_ID,
    ROOM_SIGN_PT_SLUG,
    ROOM_SIGN_PT_TITLE,
    ROOM_SIGN_SLUG,
    SEEDED_PASSWORD_DEFAULT,
    SENDER_ADDRESS,
    SEVEN_DAYS_SECONDS,
    SIGNUP_LIMIT_PER_DAY,
    SINGLE_COLOR,
    SPEC_LABEL_ORDER,
    STAFF_CONTACT_SUBJECT,
    STAFF_FILE_PREFIX,
    STAFF_QUOTATION_PREFIX,
    SUSPENDED_EMAIL,
    TEE_SIGN_ADVANTAGES,
    TEE_SIGN_COLORS,
    TEE_SIGN_DESCRIPTION_START,
    TEE_SIGN_DIMENSIONS,
    TEE_SIGN_DISPLAYS,
    TEE_SIGN_DOCUMENT,
    TEE_SIGN_ES_SLUG,
    TEE_SIGN_ES_TITLE,
    TEE_SIGN_FR_SLUG,
    TEE_SIGN_HPL_COLORS,
    TEE_SIGN_ID,
    TEE_SIGN_MATERIALS,
    TEE_SIGN_PDF,
    TEE_SIGN_PT_SLUG,
    TEE_SIGN_REFERENCES,
    TEE_SIGN_ROUTE,
    TEE_SIGN_SIZES,
    TEE_SIGN_SLUG,
    TEE_SIGN_STRUCTURES,
    TEE_SIGN_TITLE,
    TERRA_PLANTER_ID,
    UNRESOLVED_COLLECTION,
    URBAN_DOCUMENT,
    URBAN_PDF,
    WITHDRAWN_ID,
    WITHDRAWN_SLUG,
    absolute,
    api,
    api_get,
    api_post,
    as_json,
    blank,
    consent,
    contact_body,
    entry,
    error_code,
    error_fields,
    get,
    idem_key,
    labels,
    link_tags,
    location_path,
    mail_detail,
    mail_headers,
    mail_text,
    mails_to,
    names,
    page,
    plaza_bench_entry,
    poll_until,
    probe_email,
    probe_suffix,
    product_detail,
    product_ids,
    products,
    quotation_body,
    recipients,
    settle,
    sha256_hex,
    sign_up,
    staff_mail_mentioning,
    submit_contact,
    submit_file_request,
    submit_quotation,
    tee_sign_entry,
    token_for,
    visible_text,
    wait_for_mail,
    wait_for_status,
)


def _quotation_lead(db, form_token, **kwargs):
    email = probe_email()
    response = submit_quotation(email, form_token, **kwargs)
    assert response.status_code == ACCEPTED, (
        f"POST /api/lead/quotation for {email} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    lead = db.lead(email)
    assert lead is not None, f"no lead row exists for {email} after an accepted quotation"
    return email, response.json(), lead


def _quarantined_lead(db, form_token):
    email = probe_email()
    message = ("See https://a.example.com/x and https://b.example.com/y "
               "and https://c.example.com/z")
    response = submit_contact(email, form_token, message=message)
    assert response.status_code == ACCEPTED, (
        f"a link-heavy contact for {email} returned {response.status_code}: {response.text[:300]}"
    )
    lead = db.lead(email)
    assert lead is not None, f"no lead row exists for the link-heavy contact {email}"
    return email, lead


def _pdf_redemption(url: str) -> httpx.Response:
    first = httpx.get(absolute(url), timeout=60.0, follow_redirects=False)
    assert first.status_code == 302, (
        f"GET {url} returned {first.status_code}, expected a 302 to the signed location"
    )
    target = first.headers.get("location", "")
    assert target.startswith("/") or target.startswith(page("")), (
        f"the grant redirected off the app's own origin: {target!r}"
    )
    return httpx.get(absolute(target), timeout=60.0, follow_redirects=False)


def _grant_token(url: str) -> str:
    match = re.search(r"/api/files/([^/?#\s]+)", url)
    assert match, f"downloadUrl {url!r} does not carry a /api/files/<token> path"
    return match.group(1)


def test_health_endpoint_reports_ready():
    response = httpx.get(api("/health"), timeout=60.0)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:300]}"
    )
    assert response.json().get("status") == "ok", (
        f"GET /api/health did not answer status ok: {response.text[:300]}"
    )


def test_catalogue_counts_per_locale():
    for locale, total in LOCALE_TOTALS.items():
        ids = product_ids(locale)
        assert len(ids) == total, (
            f"the {locale} catalogue lists {len(ids)} products, expected {total}"
        )
    assert TEE_SIGN_ID in product_ids("en"), "the English catalogue lacks Tee Sign Heritage"
    assert ROOM_SIGN_ID not in product_ids("es"), "Spanish lists Slim Room Sign, which it lacks"
    french = product_ids("fr")
    assert ROOM_SIGN_ID not in french and GOLF_BAG_STAND_ID not in french, (
        f"French lists a product it lacks: {sorted(french)[:25]}"
    )


def test_catalogue_collection_counts_in_english():
    response = api_get("/collections", params={"locale": "en"})
    assert response.status_code == 200, (
        f"GET /api/collections returned {response.status_code}: {response.text[:300]}"
    )
    rows = {str(c.get("id")): c for c in items(response.json())}
    assert set(rows) == set(ENGLISH_COLLECTION_COUNTS), (
        f"collection identifiers are {sorted(rows)}, expected {sorted(ENGLISH_COLLECTION_COUNTS)}"
    )
    for cid, count in ENGLISH_COLLECTION_COUNTS.items():
        assert int(rows[cid].get("productCount")) == count, (
            f"collection {cid} reports productCount {rows[cid].get('productCount')}, expected {count}"
        )
        assert len(product_ids("en", collection=[cid])) == count, (
            f"filtering by {cid} does not leave {count} products"
        )
    for cid, document in CATALOGUE_DOCUMENTS.items():
        catalogue = rows[cid].get("catalogue") or {}
        assert catalogue.get("documentName") == document, (
            f"collection {cid} catalogue is {catalogue!r}, expected {document!r}"
        )
    assert not rows["details"].get("catalogue"), (
        f"Details reports a catalogue document: {rows['details'].get('catalogue')!r}"
    )
    urban_subs = {str(s.get("slug")) for s in rows["urban"].get("subCollections") or []}
    assert urban_subs == {"frame", "plaza", "reuse"}, (
        f"Urban sub-collections are {sorted(urban_subs)}"
    )


def test_facet_groups_combine_as_intersection():
    urban_signage = product_ids("en", collection=["urban"], productType=["signage"])
    assert urban_signage == {"vd-frame-wayfinding-totem", "vd-bike-parking-totem"}, (
        f"Urban with Signage left {sorted(urban_signage)}"
    )
    golf_signage = product_ids("en", collection=["golf"], productType=["signage"])
    assert golf_signage == {TEE_SIGN_ID, "vd-course-distance-marker"}, (
        f"Golf with Signage left {sorted(golf_signage)}"
    )
    none_left = product_ids("en", collection=["details"], productType=["construction"])
    assert none_left == set(), f"Details with Construction left {sorted(none_left)}"


def test_facet_values_within_a_group_combine_as_union():
    either = product_ids("en", collection=["urban", "golf"])
    assert len(either) == 10, f"Urban or Golf left {len(either)} products, expected 10"
    types = product_ids("en", productType=["signage", "construction"])
    assert len(types) == 11, f"Signage or Construction left {len(types)} products, expected 11"


def test_sub_collection_filter_narrows_urban():
    plaza = product_ids("en", collection=["urban"], subCollection=["plaza"])
    assert plaza == {PLAZA_BENCH_ID, "vd-plaza-bike-rack-arc"}, f"Urban with Plaza left {sorted(plaza)}"
    frame = product_ids("en", collection=["urban"], subCollection=["frame"])
    assert len(frame) == 3, f"Urban with Frame left {sorted(frame)}"
    reuse = product_ids("en", collection=["urban"], subCollection=["reuse"])
    assert reuse == {"vd-reuse-litter-bin-duo"}, f"Urban with Reuse left {sorted(reuse)}"


def test_unknown_facet_value_is_ignored():
    ids = product_ids("en", collection=["mars"])
    assert len(ids) == 20, f"an unknown collection value left {len(ids)} products instead of 20"


def test_server_rendered_counter_reflects_address():
    cases = [
        ("/en/products", "Showing 20 of 20 Results"),
        ("/en/products?collection=urban&productType=signage", "Showing 2 of 20 Results"),
        ("/en/products?collection=urban&collection=golf", "Showing 10 of 20 Results"),
        ("/en/products/urban", "Showing 6 of 20 Results"),
    ]
    for path, counter in cases:
        response = get(path)
        assert response.status_code == 200, f"GET {path} returned {response.status_code}"
        text = visible_text(response.text)
        assert counter in text, (
            f"GET {path} did not arrive reading {counter!r}: {text[:300]}"
        )
    urban = get("/en/products/urban").text
    title = re.search(r"(?is)<title[^>]*>(.*?)</title>", urban)
    assert title and "Urban" in title.group(1), (
        f"the Urban collection route's document title does not name Urban: {title.group(1) if title else None!r}"
    )


def test_catalogue_document_renders_product_titles_without_script():
    response = get("/en/products")
    assert response.status_code == 200, f"GET /en/products returned {response.status_code}"
    text = visible_text(response.text)
    for title in (TEE_SIGN_TITLE, PLAZA_BENCH_TITLE):
        assert title in text, f"the server-rendered catalogue lacks {title!r}"
    assert TEE_SIGN_ROUTE in response.text, (
        f"the server-rendered catalogue carries no real link to {TEE_SIGN_ROUTE}"
    )


def test_size_labels_are_returned_as_authored():
    by_slug = {str(p.get("slug")): p for p in products("en")}
    for slug, sizes in AUTHORED_SIZES.items():
        assert slug in by_slug, f"{slug} is missing from the English catalogue"
        assert labels(by_slug[slug].get("sizes")) == sizes, (
            f"{slug} sizes are {by_slug[slug].get('sizes')!r}, expected {sizes!r} as authored"
        )


def test_product_without_options_reports_none():
    by_slug = {str(p.get("slug")): p for p in products("en")}
    plate = by_slug[LINE_DOOR_PLATE_SLUG]
    assert plate.get("hasOptions") is False, f"Line Door Plate reports hasOptions {plate.get('hasOptions')!r}"
    assert not plate.get("colors") and not plate.get("sizes"), (
        f"Line Door Plate reports colours {plate.get('colors')!r} and sizes {plate.get('sizes')!r}"
    )
    options = product_detail(LINE_DOOR_PLATE_SLUG).get("options") or {}
    assert not any(options.get(axis) for axis in ("sizes", "structures", "colors", "displays", "hplColors")), (
        f"Line Door Plate detail carries option values: {options!r}"
    )


def test_tee_sign_detail_carries_every_option():
    detail = product_detail(TEE_SIGN_SLUG)
    assert detail.get("id") == TEE_SIGN_ID, f"tee sign detail id is {detail.get('id')!r}"
    assert str((detail.get("collection") or {}).get("slug")) == "golf", (
        f"tee sign collection is {detail.get('collection')!r}"
    )
    assert str(detail.get("description", "")).startswith(TEE_SIGN_DESCRIPTION_START), (
        f"tee sign description is {detail.get('description')!r}"
    )
    options = detail.get("options") or {}
    assert labels(options.get("sizes")) == TEE_SIGN_SIZES, f"tee sign sizes are {options.get('sizes')!r}"
    assert names(options.get("structures")) == TEE_SIGN_STRUCTURES, (
        f"tee sign structures are {options.get('structures')!r}"
    )
    assert names(options.get("colors")) == TEE_SIGN_COLORS, f"tee sign colours are {options.get('colors')!r}"
    assert names(options.get("displays")) == TEE_SIGN_DISPLAYS, f"tee sign displays are {options.get('displays')!r}"
    assert names(options.get("hplColors")) == TEE_SIGN_HPL_COLORS, (
        f"tee sign laminate colours are {options.get('hplColors')!r}"
    )


def test_colour_values_keep_their_reference_codes():
    colours = names((product_detail(TEE_SIGN_SLUG).get("options") or {}).get("colors"))
    assert "Anthracite grey RAL7016" in colours, f"colour values lost their reference codes: {colours!r}"
    assert "RAL7016" not in colours and "Anthracite grey" not in colours, (
        f"a colour value was split from its reference code: {colours!r}"
    )
    assert "Personalised" in colours, f"Personalised is missing from the colour values: {colours!r}"


def test_plaza_bench_detail_matches_seed():
    detail = product_detail(PLAZA_BENCH_SLUG)
    options = detail.get("options") or {}
    assert labels(options.get("sizes")) == PLAZA_BENCH_SIZES, f"bench sizes are {options.get('sizes')!r}"
    by_label = {str(s.get("label")): s for s in options.get("sizes") or [] if isinstance(s, dict)}
    assert str(by_label.get("2000", {}).get("dimensions")) == PLAZA_BENCH_2000_DIMENSIONS, (
        f"the 2000 size carries dimensions {by_label.get('2000')!r}"
    )
    assert names(options.get("structures")) == PLAZA_BENCH_STRUCTURES, (
        f"bench structures are {options.get('structures')!r}"
    )
    assert names(options.get("colors")) == PLAZA_BENCH_COLORS, f"bench colours are {options.get('colors')!r}"
    assert not options.get("displays") and not options.get("hplColors"), (
        f"the bench carries display or laminate options: {options!r}"
    )
    assert PLAZA_BENCH_REFERENCE_CODE in flatten(detail.get("references")).upper(), (
        f"bench references are {detail.get('references')!r}"
    )
    spec_labels = [str(r.get("label")) for r in detail.get("specifications") or []]
    assert "Display Options" not in spec_labels and "HPL+ Colors" not in spec_labels, (
        f"the bench shows specification rows for options it lacks: {spec_labels!r}"
    )


def test_single_value_colour_axis_on_reuse_bin():
    colours = names((product_detail(REUSE_BIN_SLUG).get("options") or {}).get("colors"))
    assert colours == [SINGLE_COLOR], f"the bin colour axis is {colours!r}, expected [{SINGLE_COLOR!r}]"


def test_specification_rows_for_tee_sign():
    detail = product_detail(TEE_SIGN_SLUG)
    rows = detail.get("specifications") or []
    seen = [str(r.get("label")) for r in rows]
    order = [label for label in seen if label in SPEC_LABEL_ORDER]
    assert order == [label for label in SPEC_LABEL_ORDER if label in seen], (
        f"specification labels are out of order: {seen!r}"
    )
    for required in ("Dimensions", "Materials", "Advantages", "References"):
        assert required in seen, f"the tee sign lacks the {required} row: {seen!r}"
    values = {str(r.get("label")): " ".join(str(v) for v in r.get("values") or []) for r in rows}
    assert TEE_SIGN_DIMENSIONS in values["Dimensions"], f"Dimensions reads {values['Dimensions']!r}"
    assert TEE_SIGN_MATERIALS in values["Materials"], f"Materials reads {values['Materials']!r}"
    assert TEE_SIGN_ADVANTAGES in values["Advantages"], f"Advantages reads {values['Advantages']!r}"
    for reference in TEE_SIGN_REFERENCES:
        assert reference in values["References"], f"References reads {values['References']!r}"


def test_product_without_documents_reports_none():
    assert product_detail(ROOM_SIGN_SLUG).get("hasDocuments") is False, (
        "Slim Room Sign reports technical documents it does not have"
    )
    assert product_detail(TEE_SIGN_SLUG).get("hasDocuments") is True, (
        "Tee Sign Heritage reports no technical documents"
    )
    room = get("/en/products/details/slim-room-sign")
    assert room.status_code == 200, f"the Slim Room Sign route returned {room.status_code}"
    assert "request information" not in visible_text(room.text).lower(), (
        "the Slim Room Sign page renders a REQUEST INFORMATION control for documents it lacks"
    )


def test_related_products_exclude_current_and_stay_in_collection():
    first = product_detail(TEE_SIGN_SLUG).get("related") or []
    second = product_detail(TEE_SIGN_SLUG).get("related") or []
    assert 1 <= len(first) <= 6, f"the related strip holds {len(first)} products"
    assert all(str(r.get("id")) != TEE_SIGN_ID for r in first), "the related strip lists the product itself"
    assert all(str((r.get("collection") or {}).get("slug")) == "golf" for r in first), (
        f"the related strip leaves the Golf collection: {first!r}"
    )
    assert [r.get("id") for r in first] == [r.get("id") for r in second], (
        "the related strip reshuffled between two reads"
    )


def test_case_study_lists_featured_products():
    response = api_get(f"/articles/{RIDGE_SLUG}", params={"locale": "en"})
    assert response.status_code == 200, f"GET /api/articles/{RIDGE_SLUG} returned {response.status_code}"
    article = response.json()
    slugs = {str(p.get("slug")) for p in article.get("relatedProducts") or []}
    assert {"boardwalk-module", "viewpoint-platform-deck"} <= slugs, f"related products are {sorted(slugs)}"
    assert int(article.get("galleryCount")) == 5, f"galleryCount is {article.get('galleryCount')!r}"
    credits = article.get("credits") or {}
    assert credits.get("client") == "Municipality of Alvora" and credits.get("design") == "Atra", (
        f"credits are {credits!r}"
    )
    assert int(article.get("readingMinutes")) >= 1, f"readingMinutes is {article.get('readingMinutes')!r}"
    assert str(article.get("date")).startswith("2026-05-12"), f"the article date is {article.get('date')!r}"


def test_product_page_carries_breadcrumb_metadata():
    response = get(TEE_SIGN_ROUTE)
    assert response.status_code == 200, f"GET {TEE_SIGN_ROUTE} returned {response.status_code}"
    assert "BreadcrumbList" in response.text, "the product page carries no BreadcrumbList metadata"


def test_root_redirect_follows_accept_language():
    spanish = get("/", headers={"Accept-Language": "es-ES,es;q=0.9"})
    assert spanish.status_code == 302, f"GET / returned {spanish.status_code}, expected 302"
    assert location_path(spanish).rstrip("/") == "/es", f"Spanish browser went to {location_path(spanish)!r}"
    german = get("/", headers={"Accept-Language": "de-DE,de;q=0.9"})
    assert german.status_code == 302 and location_path(german).rstrip("/") == "/pt", (
        f"an unmatched language went to {german.status_code} {location_path(german)!r}"
    )


def test_root_redirect_honours_stored_locale_only_with_consent():
    headers = {"Accept-Language": "es-ES,es;q=0.9"}
    granted = get("/", headers={**headers, "Cookie": f"{LOCALE_COOKIE}=fr; {CONSENT_COOKIE}=necessary,preferences"})
    assert granted.status_code == 302 and location_path(granted).rstrip("/") == "/fr", (
        f"a consented stored locale went to {granted.status_code} {location_path(granted)!r}"
    )
    refused = get("/", headers={**headers, "Cookie": f"{LOCALE_COOKIE}=fr; {CONSENT_COOKIE}=necessary"})
    assert refused.status_code == 302 and location_path(refused).rstrip("/") == "/es", (
        f"a stored locale without preferences consent went to {location_path(refused)!r}"
    )


def test_deep_link_is_never_redirected_by_language():
    response = get("/en/products", headers={"Accept-Language": "fr-FR,fr;q=0.9"})
    assert response.status_code == 200, (
        f"a French browser on /en/products got {response.status_code} {location_path(response)!r}"
    )


def test_localised_segments_serve_the_catalogue():
    paths = ["/pt/produtos", "/en/products", "/es/productos", "/fr/produits",
             "/pt/sobre", "/en/about", "/es/nosotros", "/fr/apropos",
             "/pt/sustentabilidade", "/en/sustainability", "/es/sostenibilidad", "/fr/durabilite",
             "/pt/jornal", "/en/journal", "/es/periodico", "/fr/journal",
             "/pt/lista", "/en/wishlist", "/es/mi-lista", "/fr/ma-liste",
             "/pt", "/en", "/es", "/fr"]
    for path in paths:
        response = get(path)
        assert response.status_code == 200, f"GET {path} returned {response.status_code}"
    assert get("/products").status_code != 200, "an unprefixed catalogue path answered 200"


def test_uppercase_and_trailing_slash_redirect_permanently():
    upper = get("/EN/Products")
    assert upper.status_code == 301 and location_path(upper) == "/en/products", (
        f"/EN/Products answered {upper.status_code} {location_path(upper)!r}"
    )
    slash = get("/en/products/")
    assert slash.status_code == 301 and location_path(slash) == "/en/products", (
        f"/en/products/ answered {slash.status_code} {location_path(slash)!r}"
    )
    campaign = get("/en/products?utm_source=newsletter")
    assert campaign.status_code == 200, f"a campaign parameter caused {campaign.status_code}"


def test_wrong_collection_segment_redirects_to_canonical():
    wrong = get("/en/products/nature/tee-sign-heritage")
    assert wrong.status_code == 301, f"the wrong collection segment answered {wrong.status_code}"
    assert location_path(wrong) == TEE_SIGN_ROUTE, f"it redirected to {location_path(wrong)!r}"
    foreign = get("/es/productos/golf/tee-sign-heritage")
    assert foreign.status_code == 301, f"an English slug under /es answered {foreign.status_code}"
    assert location_path(foreign) == f"/es/productos/golf/{TEE_SIGN_ES_SLUG}", (
        f"it redirected to {location_path(foreign)!r}"
    )


def test_missing_translation_redirects_to_portuguese():
    response = get("/fr/produits/details/slim-room-sign")
    assert response.status_code == 302, f"a product missing in French answered {response.status_code}"
    target = f"/pt/produtos/detalhes/{ROOM_SIGN_PT_SLUG}"
    assert location_path(response) == target, f"it redirected to {location_path(response)!r}"
    landed = get(target)
    assert landed.status_code == 200, f"GET {target} returned {landed.status_code}"
    assert ROOM_SIGN_PT_TITLE in visible_text(landed.text), f"{target} does not show {ROOM_SIGN_PT_TITLE!r}"


def test_product_alternates_resolve_by_identifier():
    alternates = product_detail(TEE_SIGN_SLUG).get("alternates") or {}
    expected = {"pt": TEE_SIGN_PT_SLUG, "en": TEE_SIGN_SLUG, "es": TEE_SIGN_ES_SLUG, "fr": TEE_SIGN_FR_SLUG}
    for locale, slug in expected.items():
        assert str((alternates.get(locale) or {}).get("slug")) == slug, (
            f"tee sign alternate for {locale} is {alternates.get(locale)!r}, expected {slug!r}"
        )
    room = product_detail(ROOM_SIGN_SLUG).get("alternates") or {}
    assert set(k for k, v in room.items() if v) == {"pt", "en"}, f"room sign alternates are {room!r}"
    bench = product_detail(PLAZA_BENCH_SLUG).get("alternates") or {}
    assert str((bench.get("pt") or {}).get("slug")) == PLAZA_BENCH_PT_SLUG, f"bench pt alternate is {bench.get('pt')!r}"
    spanish = product_detail(TEE_SIGN_ES_SLUG, "es")
    assert spanish.get("id") == TEE_SIGN_ID and spanish.get("title") == TEE_SIGN_ES_TITLE, (
        f"the Spanish slug resolved to {spanish.get('id')!r} {spanish.get('title')!r}"
    )
    portuguese = product_detail(PLAZA_BENCH_PT_SLUG, "pt")
    assert portuguese.get("title") == PLAZA_BENCH_PT_TITLE, f"the Portuguese bench title is {portuguese.get('title')!r}"


def test_product_page_declares_reciprocal_alternates():
    english = link_tags(get(TEE_SIGN_ROUTE).text)
    langs = {t.get("hreflang"): t.get("href", "") for t in english if t.get("rel", "").lower() == "alternate"}
    for locale in ("pt", "en", "es", "fr", "x-default"):
        assert locale in langs, f"the English product page lacks an hreflang {locale} alternate: {sorted(langs)}"
    assert f"/pt/produtos/golfe/{TEE_SIGN_PT_SLUG}" in langs["pt"], f"pt alternate is {langs['pt']!r}"
    assert f"/pt/produtos/golfe/{TEE_SIGN_PT_SLUG}" in langs["x-default"], f"x-default is {langs['x-default']!r}"
    spanish = link_tags(get(f"/es/productos/golf/{TEE_SIGN_ES_SLUG}").text)
    back = {t.get("hreflang"): t.get("href", "") for t in spanish if t.get("rel", "").lower() == "alternate"}
    assert TEE_SIGN_ROUTE in back.get("en", ""), f"the Spanish page does not point back to English: {back!r}"
    campaign = link_tags(get(f"{TEE_SIGN_ROUTE}?utm_source=newsletter").text)
    canonical = [t.get("href", "") for t in campaign if t.get("rel", "").lower() == "canonical"]
    assert canonical and canonical[0].endswith(TEE_SIGN_ROUTE), (
        f"the canonical link keeps a campaign parameter or is missing: {canonical!r}"
    )


def test_search_folds_diacritics_per_locale():
    cases = [("praca", "pt", PLAZA_BENCH_PT_SLUG), ("salida", "es", TEE_SIGN_ES_SLUG),
             ("depart", "fr", TEE_SIGN_FR_SLUG)]
    for query, locale, slug in cases:
        response = api_get("/search", params={"q": query, "locale": locale})
        assert response.status_code == 200, f"search {query!r} returned {response.status_code}"
        found = {str(p.get("slug")) for p in response.json().get("products") or []}
        assert slug in found, f"search {query!r} in {locale} found {sorted(found)}, expected {slug}"


def test_search_matches_prefix_of_last_word():
    response = api_get("/search", params={"q": "tee sig", "locale": "en"})
    assert response.status_code == 200, f"search 'tee sig' returned {response.status_code}"
    found = {str(p.get("slug")) for p in response.json().get("products") or []}
    assert TEE_SIGN_SLUG in found, f"search 'tee sig' found {sorted(found)}"


def test_search_treats_query_as_text():
    for query in ("(bench", "[plaza", "<b>plaza</b>", "bench.*", "\\d+"):
        response = api_get("/search", params={"q": query, "locale": "en"})
        assert response.status_code == 200, f"search {query!r} returned {response.status_code}: {response.text[:200]}"
        assert "json" in response.headers.get("content-type", ""), f"search {query!r} did not answer JSON"
        body = response.json()
        assert isinstance(body.get("products"), list), f"search {query!r} answered {body!r}"


def test_search_refuses_single_character_query():
    short = api_get("/search", params={"q": "a", "locale": "en"})
    assert short.status_code in INVALID, f"a one-character search returned {short.status_code}"
    assert error_code(short) == "invalid_request", f"the refusal code is {error_code(short)!r}"
    long = api_get("/search", params={"q": "plaza " + "x" * 150, "locale": "en"})
    assert long.status_code == 200, f"a long search was refused with {long.status_code}"


def test_search_groups_and_caps_results():
    response = api_get("/search", params={"q": "sign", "locale": "en"})
    assert response.status_code == 200, f"search 'sign' returned {response.status_code}"
    body = response.json()
    assert isinstance(body.get("products"), list) and isinstance(body.get("pages"), list), (
        f"search did not answer the two groups: {body!r}"
    )
    assert len(body["products"]) <= 8 and len(body["pages"]) <= 8, "a search group holds more than eight"
    only = api_get("/search", params={"q": "sign", "locale": "en", "type": "product"}).json()
    assert not only.get("pages"), f"type=product still returned pages: {only.get('pages')!r}"


def test_quotation_request_returns_quotable_reference(form_token):
    first = submit_quotation(probe_email(), form_token)
    assert first.status_code == ACCEPTED, f"quotation returned {first.status_code}: {first.text[:300]}"
    body = first.json()
    assert REFERENCE_RE.match(str(body.get("reference", ""))), f"the reference {body.get('reference')!r} is malformed"
    assert int(body.get("itemCount")) == 2, f"itemCount is {body.get('itemCount')!r}"
    second = submit_quotation(probe_email(), form_token)
    assert second.status_code == ACCEPTED, f"a second quotation returned {second.status_code}"
    assert second.json().get("reference") != body.get("reference"), "two quotations share one reference"


def test_quotation_items_persist_the_configured_options(db, form_token):
    email, body, lead = _quotation_lead(db, form_token)
    assert lead["kind"] == "quotation" and lead["locale"] == "en", f"lead is {lead['kind']!r} {lead['locale']!r}"
    assert lead["wants_technical_files"] is True, f"wants_technical_files is {lead['wants_technical_files']!r}"
    assert lead["role"] == ROLE_VALUE, f"the stored role is {lead['role']!r}"
    quotation = db.quotation(lead["id"])
    assert quotation is not None, f"no quotation row belongs to lead {lead['id']}"
    assert quotation["reference"] == body["reference"], "the stored reference differs from the answered one"
    lines = db.lines(quotation["id"])
    assert len(lines) == 2 and int(quotation["item_count"]) == 2, f"stored {len(lines)} lines"
    first, second = lines
    assert (first["product_id"], first["product_slug"], first["product_title"], first["collection_name"]) == (
        TEE_SIGN_ID, TEE_SIGN_SLUG, TEE_SIGN_TITLE, "Golf"), f"line 1 is {first!r}"
    assert (first["option_size"], first["option_structure"], first["option_color"],
            first["option_display"], first["option_hpl_color"]) == (
        "M", "Galvanised steel", "Anthracite grey RAL7016", "HPL +", "Dark green"), (
        f"line 1 options are {first!r}"
    )
    assert (second["product_title"], second["collection_name"], second["option_size"]) == (
        PLAZA_BENCH_TITLE, "Urban", "2000"), f"line 2 is {second!r}"
    for column in ("option_structure", "option_color", "option_display", "option_hpl_color"):
        assert blank(second[column]), f"line 2 stored {column} {second[column]!r} for an unchosen option"


def test_quotation_payload_is_rendered_on_the_server(db, form_token):
    email, body, lead = _quotation_lead(db, form_token)
    quotation = db.quotation(lead["id"])
    expected = [
        "1. Tee Sign Heritage (tee-sign-heritage)", "Collection: Golf", "Structure: Galvanised steel",
        "Color: Anthracite grey RAL7016", "Display: HPL +", "HPL Color: Dark green", "Size: M", "",
        "2. Plaza Bench Long (plaza-bench-long)", "Collection: Urban", f"Structure: {NOT_CHOSEN}",
        f"Color: {NOT_CHOSEN}", f"Display: {NOT_CHOSEN}", f"HPL Color: {NOT_CHOSEN}", "Size: 2000",
    ]
    lines = [line.strip() for line in str(quotation["payload_rendered"]).strip().splitlines()]
    assert lines == expected, f"payload_rendered is:\n{quotation['payload_rendered']}"
    assert quotation["payload_hash"], "payload_hash is empty"


def test_quotation_confirmation_email_lists_every_item(db, form_token):
    email, body, lead = _quotation_lead(db, form_token)
    subject = f"{QUOTATION_SUBJECT_PREFIX}{body['reference']}"
    message = wait_for_mail(email, subject)[0]
    assert str(message.get("Subject")) == subject, f"the confirmation subject is {message.get('Subject')!r}"
    assert recipients(message) == [email] and not recipients(message, "Cc") and not recipients(message, "Bcc"), (
        f"the confirmation is addressed to {recipients(message)} cc {recipients(message, 'Cc')}"
    )
    text = mail_text(message["ID"])
    for needle in (TEE_SIGN_TITLE, PLAZA_BENCH_TITLE, "Anthracite grey RAL7016", "Dark green", "2000", body["reference"]):
        assert needle in text, f"the quotation confirmation lacks {needle!r}"
    assert not re.search(r"""(?i)<img[^>]+(width|height)\s*=\s*["']?1["'\s>]""", text), (
        "the quotation confirmation carries a tracking pixel"
    )


def test_quotation_lead_reaches_delivered(db, form_token):
    email, body, lead = _quotation_lead(db, form_token)
    delivered = wait_for_status(db, email, "delivered")
    assert delivered["delivered_at"] is not None, "a delivered lead has no delivered_at"
    staff_mail_mentioning(STAFF_QUOTATION_PREFIX, body["reference"])


def test_quotation_staff_notification_omits_fiscal_number(db, form_token):
    email, body, lead = _quotation_lead(db, form_token, taxId="0071 9933", city="Mirandela")
    message, text = staff_mail_mentioning(f"{STAFF_QUOTATION_PREFIX}{body['reference']}", body["reference"])
    assert TEE_SIGN_TITLE in text, "the staff quotation notification does not list the lines"
    assert "0071 9933" not in text and "Mirandela" not in text, (
        "the staff quotation notification carries the fiscal number or the city"
    )


def test_quotation_confirmation_is_sent_exactly_once(db, form_token):
    email = probe_email()
    payload = quotation_body(email, form_token)
    first = api_post("/lead/quotation", payload)
    assert first.status_code == ACCEPTED, f"quotation returned {first.status_code}"
    wait_for_status(db, email, "delivered")
    wait_for_mail(email, QUOTATION_SUBJECT_PREFIX)
    replay = api_post("/lead/quotation", payload)
    assert replay.status_code in (200, ACCEPTED), f"a replay returned {replay.status_code}"
    settle()
    settle()
    assert len(mails_to(email, QUOTATION_SUBJECT_PREFIX)) == 1, (
        f"{len(mails_to(email, QUOTATION_SUBJECT_PREFIX))} confirmations reached {email}"
    )


def test_quotation_line_positions_are_contiguous(db, form_token):
    entries = [tee_sign_entry(), plaza_bench_entry(), entry(FRAME_BOLLARD_ID, FRAME_BOLLARD_SLUG, size="s")]
    email, body, lead = _quotation_lead(db, form_token, entries=entries)
    quotation = db.quotation(lead["id"])
    lines = db.lines(quotation["id"])
    assert [int(l["position"]) for l in lines] == [1, 2, 3], f"positions are {[l['position'] for l in lines]}"
    assert int(quotation["item_count"]) == 3, f"item_count is {quotation['item_count']}"
    assert all(l["product_title"] and l["product_slug"] and l["collection_name"] for l in lines), (
        f"a stored line has an empty name: {lines!r}"
    )


def test_consent_hash_matches_the_displayed_sentence(db, form_token):
    email, body, lead = _quotation_lead(db, form_token)
    assert lead["consent_privacy"] is True, f"consent_privacy is {lead['consent_privacy']!r}"
    assert lead["consent_text_hash"] == sha256_hex(PRIVACY_SENTENCE), (
        f"consent_text_hash is {lead['consent_text_hash']!r}"
    )
    assert lead["consent_recorded_at"] is not None, "consent_recorded_at is empty"


def test_unresolved_product_line_is_kept_and_flagged(db, form_token):
    entries = [entry(WITHDRAWN_ID, WITHDRAWN_SLUG, color="Black")]
    email, body, lead = _quotation_lead(db, form_token, entries=entries)
    quotation = db.quotation(lead["id"])
    line = db.lines(quotation["id"])[0]
    assert line["unresolved"] is True, f"unresolved is {line['unresolved']!r}"
    assert line["product_title"] == WITHDRAWN_SLUG and line["collection_name"] == UNRESOLVED_COLLECTION, (
        f"the unresolved line stored {line['product_title']!r} {line['collection_name']!r}"
    )
    assert WITHDRAWN_SLUG in quotation["payload_rendered"], "the unresolved line is missing from the payload"


def test_line_missing_in_locale_resolves_from_portuguese(db, form_token):
    entries = [entry(ROOM_SIGN_ID, ROOM_SIGN_SLUG, size="M")]
    email, body, lead = _quotation_lead(db, form_token, entries=entries, locale="fr")
    line = db.lines(db.quotation(lead["id"])["id"])[0]
    assert line["resolved_from_locale"] == "pt", f"resolved_from_locale is {line['resolved_from_locale']!r}"
    assert (line["product_title"], line["product_slug"]) == (ROOM_SIGN_PT_TITLE, ROOM_SIGN_PT_SLUG), (
        f"the fallback line stored {line['product_title']!r} {line['product_slug']!r}"
    )
    assert line["unresolved"] is False, "a line resolved from pt was flagged unresolved"


def test_duplicate_idempotent_submission_creates_one_quotation(db, form_token):
    email = probe_email()
    payload = quotation_body(email, form_token)
    first = api_post("/lead/quotation", payload)
    second = api_post("/lead/quotation", payload)
    assert first.status_code == ACCEPTED, f"the first submission returned {first.status_code}"
    assert second.status_code in (200, ACCEPTED), f"the replay returned {second.status_code}"
    assert second.json().get("reference") == first.json().get("reference"), "the replay minted a new reference"
    assert second.headers.get("idempotent-replayed", "").lower() == "true", (
        f"the replay carries Idempotent-Replayed {second.headers.get('idempotent-replayed')!r}"
    )
    assert len(db.leads(email)) == 1, f"{len(db.leads(email))} leads exist for one idempotency key"


def test_concurrent_identical_submissions_create_one_lead(db, form_token):
    email = probe_email()
    payload = quotation_body(email, form_token)
    gate = threading.Barrier(2)

    def fire(_):
        gate.wait()
        return api_post("/lead/quotation", payload).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(fire, range(2)))
    assert all(s in (200, ACCEPTED, 409) for s in statuses), f"simultaneous submissions returned {statuses}"
    assert ACCEPTED in statuses, f"neither simultaneous submission was accepted: {statuses}"
    assert len(db.leads(email)) == 1, f"{len(db.leads(email))} leads exist after two simultaneous submissions"


def test_reused_key_with_different_body_conflicts(db, form_token):
    email = probe_email()
    key = idem_key()
    first = api_post("/lead/quotation", quotation_body(email, form_token, key=key))
    assert first.status_code == ACCEPTED, f"the first submission returned {first.status_code}"
    changed = api_post("/lead/quotation", quotation_body(email, form_token, key=key, city="Braga"))
    assert changed.status_code == 409, f"a reused key with a new body returned {changed.status_code}"
    assert error_code(changed) == "idempotency_conflict", f"the conflict code is {error_code(changed)!r}"
    assert len(db.leads(email)) == 1, "a conflicting reuse wrote a second lead"


def test_missing_idempotency_key_is_refused(db, form_token):
    email = probe_email()
    payload = quotation_body(email, form_token)
    payload.pop("idempotencyKey")
    missing = api_post("/lead/quotation", payload)
    assert missing.status_code in INVALID, f"a missing key returned {missing.status_code}"
    short = api_post("/lead/quotation", quotation_body(email, form_token, key="short"))
    assert short.status_code in INVALID, f"a five-character key returned {short.status_code}"
    assert not db.leads(email), "a refused submission wrote a lead"


def test_quotation_contact_fields_are_validated(db, form_token):
    cases = [({"role": "Astronaut"}, "role"), ({"industry": "Mining"}, "industry"),
             ({"taxId": "12AB"}, "taxId"), ({"lastName": "   "}, "lastName"),
             ({"city": ""}, "city"), ({"country": "P"}, "country"), ({"firstName": "A" * 81}, "firstName")]
    for override, field in cases:
        email = probe_email()
        response = submit_quotation(email, form_token, **override)
        assert response.status_code == 422, f"{override} returned {response.status_code}"
        assert field in error_fields(response), f"{override} did not name {field}: {response.text[:300]}"
        assert not db.leads(email), f"{override} wrote a lead"
    valid = submit_quotation(probe_email(), form_token, role="Golf course superintendent", industry="Golf and leisure")
    assert valid.status_code == ACCEPTED, f"a listed role and industry were refused: {valid.status_code}"


def test_invalid_email_is_refused_with_field_error(db, form_token):
    for bad in ("not-an-email", "someone@nodot", "two words @example.com", ("x" * 250) + "@example.com"):
        response = submit_contact(bad, form_token)
        assert response.status_code == 422, f"email {bad[:30]!r} returned {response.status_code}"
        assert "email" in error_fields(response), f"email {bad[:30]!r} was not named: {response.text[:200]}"


def test_unknown_property_is_refused(db, form_token):
    email = probe_email()
    payload = contact_body(email, form_token)
    payload["contact"]["phone"] = "+351 900 000 000"
    extra = api_post("/lead/contact", payload)
    assert extra.status_code == 400, f"an unknown property returned {extra.status_code}"
    assert error_code(extra) == "invalid_request", f"the code is {error_code(extra)!r}"
    option = quotation_body(email, form_token, entries=[entry(TEE_SIGN_ID, TEE_SIGN_SLUG, finish="Matte")])
    assert api_post("/lead/quotation", option).status_code in INVALID, "an unknown option key was accepted"
    broken = httpx.post(api("/lead/contact"), content=b"{not json", timeout=60.0,
                        headers={"Content-Type": "application/json"})
    assert broken.status_code == 400, f"malformed JSON returned {broken.status_code}"
    assert not db.leads(email), "a refused body wrote a lead"


def test_client_supplied_title_is_refused(db, form_token):
    email = probe_email()
    carried = tee_sign_entry()
    carried["title"] = "Free Bench"
    response = api_post("/lead/quotation", quotation_body(email, form_token, entries=[carried]))
    assert response.status_code == 400, f"a client-sent title returned {response.status_code}"
    assert not db.leads(email), "a client-sent title wrote a lead"


def test_quotation_with_no_entries_is_refused(db, form_token):
    email = probe_email()
    response = submit_quotation(email, form_token, entries=[])
    assert response.status_code in INVALID, f"an empty wishlist returned {response.status_code}"
    assert not db.leads(email), "an empty quotation wrote a lead"


def test_quotation_over_fifty_entries_is_refused(db, form_token):
    email = probe_email()
    many = [entry(TEE_SIGN_ID, TEE_SIGN_SLUG, size="S") for _ in range(51)]
    response = submit_quotation(email, form_token, entries=many)
    assert response.status_code in INVALID, f"51 entries returned {response.status_code}"
    assert not db.leads(email), "a 51-entry quotation wrote a lead"


def test_missing_privacy_consent_is_refused(db, form_token):
    email = probe_email()
    payload = quotation_body(email, form_token)
    payload["consent"] = consent(privacy=False)
    response = api_post("/lead/quotation", payload)
    assert response.status_code == 422, f"missing consent returned {response.status_code}"
    assert "consent" in error_fields(response), f"consent was not named: {response.text[:200]}"
    assert not db.leads(email), "a submission without consent wrote a lead"


def test_mismatched_consent_hash_is_refused(db, form_token):
    email = probe_email()
    payload = contact_body(email, form_token)
    payload["consent"] = {"privacy": True, "textHash": sha256_hex("A different sentence.")}
    response = api_post("/lead/contact", payload)
    assert response.status_code in INVALID, f"a mismatched hash returned {response.status_code}"
    assert not db.leads(email), "a mismatched consent hash wrote a lead"


def test_tax_id_keeps_leading_zeros(db, form_token):
    email, body, lead = _quotation_lead(db, form_token, taxId="0012 345")
    assert lead["tax_id"] == "0012 345", f"tax_id is {lead['tax_id']!r}"


def test_error_body_uses_the_single_shape(form_token):
    payload = contact_body("not-an-email", form_token)
    response = httpx.post(api("/lead/contact"), json=payload, timeout=60.0,
                          headers={"X-Request-Id": "probe-request-4471"})
    assert response.status_code == 422, f"the invalid body returned {response.status_code}"
    error = response.json().get("error") or {}
    for key in ("code", "message", "requestId"):
        assert error.get(key), f"the error body lacks {key}: {response.text[:300]}"
    assert error.get("code") == "validation_failed", f"the code is {error.get('code')!r}"
    assert response.headers.get("x-request-id") == "probe-request-4471", (
        f"X-Request-Id was not echoed: {response.headers.get('x-request-id')!r}"
    )
    lowered = response.text.lower()
    for leak in ("traceback", "postgres", "undefined"):
        assert leak not in lowered, f"the error body leaks {leak!r}: {response.text[:300]}"
    for leak in ("SELECT ", "NaN"):
        assert leak not in response.text, f"the error body leaks {leak!r}: {response.text[:300]}"
    assert api_get("/health").headers.get("x-request-id"), "a success carries no X-Request-Id"


def test_contact_enquiry_is_stored_and_answered_with_request_id(db, form_token):
    email = probe_email()
    response = submit_contact(email, form_token, message="Quote for six benches, please.")
    assert response.status_code == ACCEPTED, f"contact returned {response.status_code}, expected 202"
    assert response.json().get("requestId"), f"no requestId in {response.text[:200]}"
    lead = db.lead(email)
    assert lead and lead["kind"] == "contact", f"the contact lead is {lead!r}"
    assert lead["message"] == "Quote for six benches, please.", f"the message stored is {lead['message']!r}"
    assert lead["status"] in ("received", "queued", "delivered"), f"status is {lead['status']!r}"


def test_contact_confirmation_email_restates_the_message(db, form_token):
    email = probe_email()
    marker = f"marker-{probe_suffix()}"
    assert submit_contact(email, form_token, message=f"Benches for the park {marker}").status_code == ACCEPTED
    message = wait_for_mail(email, CONTACT_SUBJECT)[0]
    assert str(message.get("Subject")) == CONTACT_SUBJECT, f"the subject is {message.get('Subject')!r}"
    assert marker in mail_text(message["ID"]), "the enquiry confirmation does not restate the message"
    sender = (mail_detail(message["ID"]).get("From") or {}).get("Address", "")
    assert str(sender).lower() == SENDER_ADDRESS, f"the confirmation comes from {sender!r}"


def test_contact_staff_notification_carries_no_message(db, form_token):
    email = probe_email()
    marker = f"secret-note-{probe_suffix()}"
    assert submit_contact(email, form_token, message=f"Private detail {marker}").status_code == ACCEPTED
    lead = db.lead(email)
    message, text = staff_mail_mentioning(STAFF_CONTACT_SUBJECT, f"/office/leads/{lead['id']}")
    assert marker not in text, "the staff enquiry notification carries the message"
    assert email not in text.lower(), "the staff enquiry notification carries the visitor's email"


def test_filled_decoy_field_writes_nothing(db, form_token):
    email = probe_email()
    response = api_post("/lead/contact", contact_body(email, form_token, website="https://spam.example.com"))
    assert response.status_code == ACCEPTED, f"a filled decoy returned {response.status_code}"
    settle()
    assert not db.leads(email), "a filled decoy wrote a lead"
    assert not mails_to(email), "a filled decoy sent mail"


def test_too_fresh_form_token_writes_nothing(db):
    fresh = api_get("/form-token").json().get("formToken")
    email = probe_email()
    response = submit_contact(email, fresh)
    assert response.status_code == ACCEPTED, f"a too-fresh token returned {response.status_code}"
    settle()
    assert not db.leads(email), "a submission made at once with a new token wrote a lead"
    assert not mails_to(email), "a too-fresh submission sent mail"


def test_missing_form_token_is_refused(db):
    email = probe_email()
    missing = submit_contact(email, None)
    assert missing.status_code in INVALID, f"a missing form token returned {missing.status_code}"
    forged = submit_contact(email, "forged-token-value")
    assert forged.status_code in INVALID, f"a forged form token returned {forged.status_code}"
    assert not db.leads(email), "a refused token wrote a lead"


def test_repeated_submissions_from_one_address_are_limited(db, form_token):
    email = probe_email()
    for n in range(LEAD_LIMIT_PER_HOUR):
        response = submit_contact(email, form_token, message=f"Enquiry number {n}")
        assert response.status_code == ACCEPTED, f"submission {n + 1} returned {response.status_code}"
    limited = submit_contact(email, form_token, message="One more enquiry")
    assert limited.status_code == 429, f"submission six returned {limited.status_code}"
    assert int(limited.headers.get("retry-after", "0")) > 0, "the limit carries no Retry-After"
    assert error_code(limited) == "rate_limited", f"the code is {error_code(limited)!r}"
    assert int((limited.json().get("error") or {}).get("retryAfterSeconds", 0)) > 0, "retryAfterSeconds is not positive"
    assert len(db.leads(email)) == LEAD_LIMIT_PER_HOUR, f"{len(db.leads(email))} leads exist after the limit"


def test_link_heavy_message_is_quarantined(db, form_token):
    email, lead = _quarantined_lead(db, form_token)
    assert lead["status"] == "quarantined", f"a three-link message is {lead['status']!r}"
    settle()
    settle()
    assert not mails_to(email), "a quarantined enquiry sent mail"


def test_file_request_issues_a_grant_for_one_document(db, form_token):
    email = probe_email()
    response = submit_file_request(email, form_token)
    assert response.status_code == ACCEPTED, f"file request returned {response.status_code}"
    body = response.json()
    assert body.get("documentName") == TEE_SIGN_DOCUMENT, f"documentName is {body.get('documentName')!r}"
    assert "/api/files/" in str(body.get("downloadUrl")), f"downloadUrl is {body.get('downloadUrl')!r}"
    assert body.get("expiresAt"), "the grant answer carries no expiresAt"
    lead = db.lead(email)
    assert lead and lead["kind"] == "file_request", f"the lead is {lead!r}"
    grants = db.file_requests(lead["id"])
    assert len(grants) == 1, f"{len(grants)} file_request rows exist"
    assert (grants[0]["scope"], grants[0]["product_id"], grants[0]["document_name"]) == (
        "product", TEE_SIGN_ID, TEE_SIGN_DOCUMENT), f"the grant row is {grants[0]!r}"


def test_file_grant_redirects_to_a_signed_pdf(db, form_token):
    email = probe_email()
    body = submit_file_request(email, form_token).json()
    document = _pdf_redemption(body["downloadUrl"])
    assert document.status_code == 200, f"the signed location returned {document.status_code}"
    assert "application/pdf" in document.headers.get("content-type", ""), (
        f"the document type is {document.headers.get('content-type')!r}"
    )
    assert TEE_SIGN_PDF in document.headers.get("content-disposition", ""), (
        f"content-disposition is {document.headers.get('content-disposition')!r}"
    )
    assert document.content.startswith(b"%PDF"), "the served document is not a PDF"
    grant = db.file_requests(db.lead(email)["id"])[0]
    assert int(grant["download_count"]) == 1, f"download_count is {grant['download_count']}"


def test_collection_catalogue_request_is_granted(db, form_token):
    email = probe_email()
    document = {"scope": "collection_catalogue", "collectionId": "urban"}
    first = submit_file_request(email, form_token, document=document)
    assert first.status_code == ACCEPTED, f"a catalogue request returned {first.status_code}"
    assert first.json().get("documentName") == URBAN_DOCUMENT, f"documentName is {first.json().get('documentName')!r}"
    served = _pdf_redemption(first.json()["downloadUrl"])
    assert URBAN_PDF in served.headers.get("content-disposition", ""), (
        f"content-disposition is {served.headers.get('content-disposition')!r}"
    )
    again = submit_file_request(email, form_token, document=document)
    assert again.status_code == ACCEPTED, f"a repeat catalogue request returned {again.status_code}"
    assert _grant_token(again.json()["downloadUrl"]) != _grant_token(first.json()["downloadUrl"]), (
        "a repeat request reused the first grant"
    )


def test_file_grant_email_carries_the_download_link(db, form_token):
    email = probe_email()
    body = submit_file_request(email, form_token).json()
    token = _grant_token(body["downloadUrl"])
    message = wait_for_mail(email, f"{GRANT_SUBJECT_PREFIX}{TEE_SIGN_DOCUMENT}")[0]
    assert f"/api/files/{token}" in mail_text(message["ID"]), "the grant email lacks the download link"
    staff_mail_mentioning(f"{STAFF_FILE_PREFIX}{TEE_SIGN_DOCUMENT}", TEE_SIGN_DOCUMENT)


def test_file_grant_expires_seven_days_after_creation(db, form_token):
    email = probe_email()
    assert submit_file_request(email, form_token).status_code == ACCEPTED
    grant = db.file_requests(db.lead(email)["id"])[0]
    span = (grant["token_expires_at"] - grant["created_at"]).total_seconds()
    assert abs(span - SEVEN_DAYS_SECONDS) <= 300, f"the grant lasts {span} seconds, expected seven days"


def test_unknown_file_token_answers_not_found():
    response = httpx.get(api(f"/files/unknown-{probe_suffix()}"), timeout=60.0, follow_redirects=False)
    assert response.status_code == 404, f"an unknown token returned {response.status_code}, expected 404"


def test_file_grant_is_exhausted_after_five_redemptions(db, form_token):
    url = submit_file_request(probe_email(), form_token).json()["downloadUrl"]
    for n in range(GRANT_REDEMPTIONS):
        response = httpx.get(absolute(url), timeout=60.0, follow_redirects=False)
        assert response.status_code == 302, f"redemption {n + 1} returned {response.status_code}"
    exhausted = httpx.get(absolute(url), timeout=60.0, follow_redirects=False)
    assert exhausted.status_code == 404, f"the sixth redemption returned {exhausted.status_code}, expected 404"


def test_file_grant_ignores_a_supplied_asset_parameter(db, form_token):
    url = submit_file_request(probe_email(), form_token).json()["downloadUrl"]
    joiner = "&" if "?" in url else "?"
    tampered = f"{url}{joiner}assetKey=urban-catalogue&productId={PLAZA_BENCH_ID}&document=urban"
    served = _pdf_redemption(tampered)
    assert TEE_SIGN_PDF in served.headers.get("content-disposition", ""), (
        f"a supplied parameter changed the document: {served.headers.get('content-disposition')!r}"
    )


def test_file_request_for_missing_documents_is_refused(db, form_token):
    email = probe_email()
    room = submit_file_request(email, form_token, document={"scope": "product", "productId": ROOM_SIGN_ID})
    assert room.status_code == 404, f"technical files for Slim Room Sign returned {room.status_code}"
    details = submit_file_request(email, form_token, document={"scope": "collection_catalogue", "collectionId": "details"})
    assert details.status_code == 404, f"a Details catalogue returned {details.status_code}"
    assert not db.leads(email), "a request for a missing document wrote a lead"


def test_newsletter_signup_creates_pending_subscriber(db, form_token):
    email = probe_email()
    response = sign_up(email, form_token)
    assert response.status_code == ACCEPTED, f"sign-up returned {response.status_code}"
    assert response.json() == {"status": "check_inbox"}, f"sign-up answered {response.text[:200]}"
    row = db.subscriber(email)
    assert row and row["status"] == "pending", f"the subscriber row is {row!r}"
    assert row["confirm_token"], "a pending subscriber has no confirm token"
    span = (row["confirm_token_expires_at"] - row["created_at"]).total_seconds()
    assert abs(span - FOURTEEN_DAYS_SECONDS) <= 300, f"the confirm token lasts {span} seconds"
    token = str(row["unsubscribe_token"] or "")
    assert token and email not in token and token != sha256_hex(email), (
        "the unsubscribe token is missing or derived from the address"
    )


def test_newsletter_confirmation_email_is_sent_once(db, form_token):
    email = probe_email()
    assert sign_up(email, form_token).status_code == ACCEPTED
    message = wait_for_mail(email, NEWSLETTER_SUBJECT)[0]
    assert str(message.get("Subject")) == NEWSLETTER_SUBJECT, f"the subject is {message.get('Subject')!r}"
    repeat = sign_up(email, form_token)
    assert repeat.status_code == ACCEPTED and repeat.json() == {"status": "check_inbox"}, (
        f"a repeat sign-up answered {repeat.status_code} {repeat.text[:200]}"
    )
    settle()
    settle()
    assert len(mails_to(email)) == 1, f"{len(mails_to(email))} messages reached a pending address"
    assert db.count_subscribers(email) == 1, "a repeat sign-up created a second row"


def test_newsletter_confirmation_link_confirms_subscriber(db, form_token):
    email = probe_email()
    assert sign_up(email, form_token).status_code == ACCEPTED
    message = wait_for_mail(email, NEWSLETTER_SUBJECT)[0]
    match = re.search(r"/api/subscriber/confirm\?token=([A-Za-z0-9_\-.~%]+)", mail_text(message["ID"]))
    assert match, "the confirmation message carries no confirmation link"
    link = api(f"/subscriber/confirm?token={match.group(1)}")
    confirmed = httpx.get(link, timeout=60.0, follow_redirects=False)
    assert confirmed.status_code == 303, f"confirming returned {confirmed.status_code}"
    assert location_path(confirmed) == "/en/newsletter/confirmed", f"it went to {location_path(confirmed)!r}"
    row = db.subscriber(email)
    assert row["status"] == "confirmed" and row["confirmed_at"] is not None, f"the row is {row!r}"
    assert blank(row["confirm_token"]), "the confirm token survived confirmation"
    reused = httpx.get(link, timeout=60.0, follow_redirects=False)
    assert reused.status_code == 303 and location_path(reused) == "/en/newsletter/expired", (
        f"a used link returned {reused.status_code} {location_path(reused)!r}"
    )


def test_confirmed_address_signup_discloses_nothing(db, form_token):
    email = probe_email()
    assert sign_up(email, form_token).status_code == ACCEPTED
    wait_for_mail(email, NEWSLETTER_SUBJECT)
    token = db.subscriber(email)["confirm_token"]
    confirmed = api_get(f"/subscriber/confirm", params={"token": token})
    assert confirmed.status_code == 303, f"confirming returned {confirmed.status_code}"
    again = sign_up(email, form_token)
    assert again.status_code == ACCEPTED and again.json() == {"status": "check_inbox"}, (
        f"a confirmed address sign-up answered {again.status_code} {again.text[:200]}"
    )
    settle()
    settle()
    assert len(mails_to(email)) == 1, "a sign-up for a confirmed address sent another message"


def test_newsletter_message_carries_unsubscribe_headers(db, form_token):
    email = probe_email()
    assert sign_up(email, form_token).status_code == ACCEPTED
    message = wait_for_mail(email, NEWSLETTER_SUBJECT)[0]
    headers = mail_headers(message["ID"])
    assert headers.get("list-unsubscribe"), f"no List-Unsubscribe header: {sorted(headers)}"
    assert "one-click" in json.dumps(headers.get("list-unsubscribe-post", "")).lower(), (
        f"List-Unsubscribe-Post is {headers.get('list-unsubscribe-post')!r}"
    )


def test_unsubscribe_link_takes_effect_at_once(db, form_token):
    email = probe_email()
    assert sign_up(email, form_token).status_code == ACCEPTED
    token = db.subscriber(email)["unsubscribe_token"]
    response = api_get("/subscriber/unsubscribe", params={"token": token})
    assert response.status_code == 303, f"unsubscribing returned {response.status_code}"
    assert location_path(response) == "/en/newsletter/unsubscribed", f"it went to {location_path(response)!r}"
    row = db.subscriber(email)
    assert row["status"] == "unsubscribed" and row["unsubscribed_at"] is not None, f"the row is {row!r}"
    for path in ("/en/newsletter/unsubscribed", "/en/newsletter/confirmed", "/en/newsletter/expired"):
        assert get(path).status_code == 200, f"GET {path} did not answer 200"


def test_resubscribe_returns_to_pending_with_new_confirmation(db, form_token):
    email = probe_email()
    assert sign_up(email, form_token).status_code == ACCEPTED
    wait_for_mail(email, NEWSLETTER_SUBJECT)
    token = db.subscriber(email)["unsubscribe_token"]
    assert api_get("/subscriber/unsubscribe", params={"token": token}).status_code == 303
    assert sign_up(email, form_token).status_code == ACCEPTED
    assert db.subscriber(email)["status"] == "pending", f"the row is {db.subscriber(email)!r}"
    found = poll_until(lambda: len(mails_to(email, NEWSLETTER_SUBJECT)) >= 2)
    assert found, "a returning address received no new confirmation"


def test_one_click_unsubscribe_post_answers_no_content(db, form_token):
    email = probe_email()
    assert sign_up(email, form_token).status_code == ACCEPTED
    token = db.subscriber(email)["unsubscribe_token"]
    response = api_post("/subscriber/unsubscribe", {"token": token})
    assert response.status_code == 204, f"the one-click unsubscribe returned {response.status_code}"
    assert db.subscriber(email)["status"] == "unsubscribed", "the one-click unsubscribe changed nothing"


def test_newsletter_rate_limit_applies_per_address(form_token):
    email = probe_email()
    for n in range(SIGNUP_LIMIT_PER_DAY):
        response = sign_up(email, form_token)
        assert response.status_code == ACCEPTED, f"sign-up {n + 1} returned {response.status_code}"
    limited = sign_up(email, form_token)
    assert limited.status_code == 429, f"sign-up four returned {limited.status_code}"


def test_journal_categories_and_counts():
    response = api_get("/categories", params={"locale": "en"})
    assert response.status_code == 200, f"GET /api/categories returned {response.status_code}"
    rows = [(str(c.get("slug")), int(c.get("articleCount"))) for c in items(response.json())]
    assert rows == CATEGORY_COUNTS, f"categories are {rows}"
    educational = api_get("/articles", params={"locale": "en", "category": "educational"})
    assert [a.get("slug") for a in items(educational.json())] == [EDUCATIONAL_SLUG], (
        f"the Educational category holds {educational.text[:200]}"
    )


def test_journal_counts_per_locale():
    for locale, total in ARTICLE_TOTALS.items():
        response = api_get("/articles", params={"locale": locale})
        assert response.status_code == 200, f"GET /api/articles?locale={locale} returned {response.status_code}"
        assert int(response.headers.get("x-total-count", "-1")) == total, (
            f"{locale} reports X-Total-Count {response.headers.get('x-total-count')!r}, expected {total}"
        )


def test_case_study_pages_hold_twelve_then_one():
    first = api_get("/articles", params={"locale": "en", "category": "case-studies"})
    second = api_get("/articles", params={"locale": "en", "category": "case-studies", "page": 2})
    page_one, page_two = items(first.json()), items(second.json())
    assert len(page_one) == 12 and len(page_two) == 1, f"pages hold {len(page_one)} then {len(page_two)}"
    assert int(first.headers.get("x-total-count", "-1")) == 13, "Case Studies does not total 13"
    assert page_one[0].get("slug") == RIDGE_SLUG, f"page one opens with {page_one[0].get('slug')!r}"
    dates = [str(a.get("date")) for a in page_one]
    assert dates == sorted(dates, reverse=True), f"page one is not newest first: {dates}"


def test_recent_articles_are_newest_first():
    listed = items(api_get("/articles", params={"locale": "en"}).json())
    assert [a.get("slug") for a in listed[:4]] == RECENT_SLUGS, (
        f"the newest English articles are {[a.get('slug') for a in listed[:4]]}"
    )


def test_category_page_links_its_later_pages():
    later = get("/en/journal/case-studies?page=2")
    assert later.status_code == 200, f"page two returned {later.status_code}"
    tags = link_tags(later.text)
    canonical = [t.get("href", "") for t in tags if t.get("rel", "").lower() == "canonical"]
    assert canonical and canonical[0].endswith("/en/journal/case-studies?page=2"), f"canonical is {canonical!r}"
    assert any(t.get("rel", "").lower() == "prev" for t in tags), "page two has no previous relation"
    first = [t.get("href", "") for t in link_tags(get("/en/journal/case-studies").text)
             if t.get("rel", "").lower() == "canonical"]
    assert first and first[0].endswith("/en/journal/case-studies"), f"page one canonical is {first!r}"
    assert get("/pt/jornal/casos-de-estudo").status_code == 200, "the Portuguese Case Studies route failed"
    foreign = get("/en/journal/casos-de-estudo")
    assert foreign.status_code == 301 and location_path(foreign) == "/en/journal/case-studies", (
        f"a Portuguese category segment under /en answered {foreign.status_code} {location_path(foreign)!r}"
    )


def test_unknown_category_is_not_found():
    response = get("/en/journal/no-such-category")
    assert response.status_code == 404, f"an unknown category returned {response.status_code}"


def test_open_positions_are_listed():
    response = api_get("/jobs", params={"locale": "en"})
    assert response.status_code == 200, f"GET /api/jobs returned {response.status_code}"
    jobs = items(response.json())
    assert {str(j.get("title")) for j in jobs} == JOB_TITLES, f"positions are {[j.get('title') for j in jobs]}"
    portuguese = [j for j in jobs if j.get("title") == "Serralheiro Civil"][0]
    assert portuguese.get("lang") == "pt", f"Serralheiro Civil declares {portuguese.get('lang')!r}"
    for path in ("/en/careers", "/es/careers", "/pt/careers", "/fr/newsletter/confirmed", "/es/legal/privacy-policy"):
        assert get(path).status_code in (200, 302), f"GET {path} returned {get(path).status_code}"


def test_legal_versions_are_retained():
    current = get("/en/legal/privacy-policy")
    assert current.status_code == 200, f"the privacy policy returned {current.status_code}"
    assert "/en/legal/privacy-policy/v/1" in current.text, "the privacy policy does not link to version 1"
    old = get("/en/legal/privacy-policy/v/1")
    assert old.status_code == 200, f"version 1 returned {old.status_code}"
    assert "This version has been superseded." in visible_text(old.text), "version 1 carries no superseded banner"
    assert re.search(r"""href=["'](?:https?://[^"']+)?/en/legal/privacy-policy["']""", old.text), (
        "version 1 does not link to the current policy"
    )
    assert get("/en/legal/privacy-policy/v/9").status_code == 404, "a version that never existed did not answer 404"
    for path in ("/en/legal/cookie-policy", "/en/legal/terms-of-use"):
        assert get(path).status_code == 200, f"GET {path} did not answer 200"


def test_markdown_page_carries_product_substance():
    response = get(f"{TEE_SIGN_ROUTE}.md")
    assert response.status_code == 200, f"the markdown page returned {response.status_code}"
    assert "markdown" in response.headers.get("content-type", ""), (
        f"the markdown page is served as {response.headers.get('content-type')!r}"
    )
    assert TEE_SIGN_TITLE in response.text and "GTEETTM010" in response.text, "the markdown lacks the product substance"
    assert "<nav" not in response.text.lower(), "the markdown carries navigation chrome"
    index = get("/llms.txt")
    assert index.status_code == 200 and f"{TEE_SIGN_ROUTE}.md" in index.text, "llms.txt does not list the product page"


def test_sitemap_and_robots_describe_public_routes():
    sitemap = get("/sitemap.xml")
    assert sitemap.status_code == 200, f"sitemap.xml returned {sitemap.status_code}"
    for locale in ("pt", "en", "es", "fr"):
        assert f"sitemap-{locale}.xml" in sitemap.text, f"sitemap.xml does not list sitemap-{locale}.xml"
    english = get("/sitemap-en.xml")
    assert english.status_code == 200 and TEE_SIGN_ROUTE in english.text, "sitemap-en.xml lacks the tee sign"
    assert "hreflang" in english.text, "sitemap-en.xml carries no hreflang alternates"
    robots = get("/robots.txt")
    assert robots.status_code == 200, f"robots.txt returned {robots.status_code}"
    for needle in ("Disallow: /api/", "Disallow: /office", "Sitemap:"):
        assert needle in robots.text, f"robots.txt lacks {needle!r}"


def test_header_theme_is_rendered_on_the_server():
    sustainability = get("/en/sustainability").text
    assert re.search(r"""data-theme=["']fluor["']""", sustainability), "the sustainability header is not fluor"
    about = get("/en/about").text
    assert re.search(r"""data-theme=["']dark["']""", about), "the about header is not dark"


def test_not_found_page_offers_three_destinations():
    response = get("/en/nowhere-at-all")
    assert response.status_code == 404, f"an unknown address returned {response.status_code}"
    for target in ("/en/products", "/en/journal"):
        assert re.search(rf"""href=["'](?:https?://[^"']+)?{re.escape(target)}["']""", response.text), (
            f"the not-found page does not link {target}"
        )
    assert re.search(r"""href=["'](?:https?://[^"']+)?/en/?["']""", response.text), "the not-found page does not link home"
    assert "http-equiv" not in response.text.lower() or "refresh" not in response.text.lower(), (
        "the not-found page redirects on its own"
    )


def test_consent_choice_is_recorded_as_receipt(db):
    visitor = f"visitor-{probe_suffix()}"
    first = api_post("/consent", {"visitorKey": visitor, "policyVersion": "2",
                                   "categories": {"necessary": True, "preferences": True,
                                                  "statistics": False, "marketing": False}})
    assert first.status_code == ACCEPTED, f"POST /api/consent returned {first.status_code}"
    rows = db.receipts(visitor)
    assert len(rows) == 1, f"{len(rows)} receipts exist after one choice"
    categories = as_json(rows[0]["categories"])
    assert categories.get("preferences") is True and categories.get("marketing") is False, f"categories are {categories!r}"
    assert str(rows[0]["policy_version"]) == "2", f"policy_version is {rows[0]['policy_version']!r}"
    assert not re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", str(rows[0]["ip_hash"])), "a raw network address was stored"
    second = api_post("/consent", {"visitorKey": visitor, "policyVersion": "2",
                                    "categories": {"necessary": True, "preferences": False,
                                                   "statistics": False, "marketing": False}})
    assert second.status_code == ACCEPTED, f"a changed choice returned {second.status_code}"
    rows = db.receipts(visitor)
    assert len(rows) == 2, f"{len(rows)} receipts exist after a changed choice"
    assert any(as_json(r["categories"]).get("preferences") is True for r in rows), "the first receipt was rewritten"


def test_unknown_product_slug_is_not_found():
    api_miss = api_get("/products/no-such-product", params={"locale": "en"})
    assert api_miss.status_code == 404 and error_code(api_miss) == "not_found", (
        f"an unknown product answered {api_miss.status_code} {error_code(api_miss)!r}"
    )
    assert get("/en/products/golf/no-such-product").status_code == 404, "an unknown product route did not answer 404"
    unknown = get("/en/products/mars")
    assert unknown.status_code == 404, f"an unknown collection returned {unknown.status_code}"
    text = visible_text(unknown.text)
    assert all(name in text for name in ("Urban", "Nature", "Repolymer", "Golf", "Details")), (
        "the not-found page for a collection does not name the five collections"
    )


def test_malformed_slug_is_not_found():
    for slug in ("Bad%27Slug", "%27%20OR%201%3D1", "a--b", "x" * 121):
        response = httpx.get(page(f"/en/products/golf/{slug}"), timeout=60.0, follow_redirects=False)
        assert response.status_code == 404, f"the malformed slug {slug[:20]!r} returned {response.status_code}"
        api_miss = httpx.get(api(f"/products/{slug}?locale=en"), timeout=60.0, follow_redirects=False)
        assert api_miss.status_code == 404, f"the malformed API slug {slug[:20]!r} returned {api_miss.status_code}"


def test_security_headers_on_documents_and_api():
    for path in ("/en/products", "/api/health"):
        headers = get(path).headers
        hsts = headers.get("strict-transport-security", "")
        age = re.search(r"max-age=(\d+)", hsts)
        assert age and int(age.group(1)) >= 31536000 and "includesubdomains" in hsts.lower(), (
            f"{path} carries Strict-Transport-Security {hsts!r}"
        )
        assert headers.get("x-content-type-options", "").lower() == "nosniff", f"{path} lacks nosniff"
        assert headers.get("referrer-policy", "").lower() == "strict-origin-when-cross-origin", (
            f"{path} carries Referrer-Policy {headers.get('referrer-policy')!r}"
        )
        permissions = headers.get("permissions-policy", "").lower()
        for feature in ("camera", "microphone", "geolocation", "payment"):
            assert feature in permissions, f"{path} Permissions-Policy does not name {feature}"
        assert headers.get("cross-origin-opener-policy", "").lower() == "same-origin", (
            f"{path} carries Cross-Origin-Opener-Policy {headers.get('cross-origin-opener-policy')!r}"
        )


def test_content_policy_forbids_inline_script():
    response = get("/en/products")
    policy = response.headers.get("content-security-policy", "")
    directives = {}
    for part in policy.split(";"):
        bits = part.strip().split()
        if bits:
            directives[bits[0].lower()] = " ".join(bits[1:])
    assert "'none'" in directives.get("frame-ancestors", ""), f"frame-ancestors is {directives.get('frame-ancestors')!r}"
    assert "'none'" in directives.get("object-src", ""), f"object-src is {directives.get('object-src')!r}"
    script = directives.get("script-src", "")
    assert script, f"the policy has no script-src: {policy!r}"
    assert "'unsafe-inline'" not in script and "'unsafe-eval'" not in script, f"script-src is {script!r}"
    assert directives.get("connect-src", "").strip() == "'self'", f"connect-src is {directives.get('connect-src')!r}"
    for src in re.findall(r"""(?is)<script\b[^>]*\bsrc=["']([^"']+)["']""", response.text):
        assert src.startswith("/") or src.startswith(page("")), f"a page script loads from another origin: {src}"


def test_browser_bundles_carry_no_secret():
    documents = [get(path).text for path in ("/en/products", TEE_SIGN_ROUTE, "/en/wishlist")]
    assets = set()
    for markup in documents:
        assets.update(re.findall(r"""(?is)<script\b[^>]*\bsrc=["']([^"']+)["']""", markup))
        assets.update(re.findall(r"""(?is)<link\b[^>]*\bhref=["']([^"']+\.(?:js|mjs|css))["']""", markup))
    bodies = list(documents)
    for asset in sorted(assets):
        if asset.startswith("/") or asset.startswith(page("")):
            fetched = httpx.get(absolute(asset), timeout=60.0)
            assert fetched.status_code == 200, f"GET {asset} returned {fetched.status_code}"
            bodies.append(fetched.text)
    assert len(bodies) > len(documents), "the pages reference no script or style file"
    for body in bodies:
        for secret in FORBIDDEN_IN_BUNDLES:
            assert secret not in body, f"a browser-delivered file contains {secret!r}"


def test_staff_login_returns_access_token(db):
    response = httpx.post(api("/auth/login"), json={"email": COMMERCIAL_EMAIL, "password": SEEDED_PASSWORD_DEFAULT},
                          timeout=60.0)
    assert response.status_code == 200, f"login returned {response.status_code}: {response.text[:200]}"
    body = response.json()
    assert body.get("access_token") and body.get("role") == "commercial", f"login answered {body!r}"
    issued = datetime.fromisoformat(str(body["issued_at"]).replace("Z", "+00:00"))
    expires = datetime.fromisoformat(str(body["expires_at"]).replace("Z", "+00:00"))
    assert abs((expires - issued).total_seconds() - SEVEN_DAYS_SECONDS) <= 1, (
        f"the token spans {expires - issued}, expected seven days"
    )
    with client(body["access_token"]) as staff:
        me = staff.get("/office/me")
    assert me.status_code == 200, f"GET /api/office/me returned {me.status_code}"
    assert me.json() == {**me.json(), "email": COMMERCIAL_EMAIL, "role": "commercial", "displayName": "Carla Mendes"}, (
        f"GET /api/office/me answered {me.text[:200]}"
    )
    row = db.staff(COMMERCIAL_EMAIL)
    assert row is not None and row["role"] == "commercial", f"the staff row is {row!r}"
    assert SEEDED_PASSWORD_DEFAULT not in flatten(row), "the staff row stores the password in the clear"


def test_wrong_password_and_unknown_address_are_denied_alike():
    wrong = httpx.post(api("/auth/login"), json={"email": COMMERCIAL_EMAIL, "password": "not-the-password-1"},
                       timeout=60.0)
    unknown = httpx.post(api("/auth/login"), json={"email": probe_email(), "password": "not-the-password-1"},
                         timeout=60.0)
    assert wrong.status_code == 401 and unknown.status_code == 401, (
        f"denied sign-ins returned {wrong.status_code} and {unknown.status_code}"
    )
    assert error_code(wrong) == error_code(unknown), "the two denials differ"
    assert "access_token" not in wrong.text and "access_token" not in unknown.text, "a denied sign-in returned a token"


def test_office_requires_a_valid_token():
    for path in ("/office/leads/summary", "/office/leads", "/office/me", "/office/subscribers"):
        anonymous = api_get(path)
        assert anonymous.status_code in DENIED, f"GET /api{path} without a token returned {anonymous.status_code}"
        with client("not-a-real-token") as bad:
            malformed = bad.get(path)
        assert malformed.status_code in DENIED, f"GET /api{path} with a malformed token returned {malformed.status_code}"


def test_editor_is_denied_lead_contents(db, form_token, editor_client):
    email, body, lead = _quotation_lead(db, form_token)
    before = db.audit_count("lead.read", lead["id"])
    listing = editor_client.get("/office/leads")
    assert listing.status_code in DENIED, f"an editor listing enquiries got {listing.status_code}"
    detail = editor_client.get(f"/office/leads/{lead['id']}")
    assert detail.status_code in DENIED, f"an editor reading an enquiry got {detail.status_code}"
    assert email not in detail.text and email not in listing.text, "an editor denial leaked the enquirer's email"
    assert db.audit_count("lead.read", lead["id"]) == before, "an editor denial was recorded as a read"
    assert db.lead_by_id(lead["id"]) is not None, "the lead disappeared under a denial"


def test_editor_sees_lead_counts(editor_client):
    me = editor_client.get("/office/me")
    assert me.status_code == 200 and me.json().get("role") == "editor" and me.json().get("email") == EDITOR_EMAIL, (
        f"the editor identity is {me.text[:200]}"
    )
    summary = editor_client.get("/office/leads/summary")
    assert summary.status_code == 200 and "total" in summary.json(), f"lead summary answered {summary.text[:200]}"
    subscribers = editor_client.get("/office/subscribers/summary")
    assert subscribers.status_code == 200, f"subscriber summary returned {subscribers.status_code}"
    assert {"pending", "confirmed", "unsubscribed"} <= set(subscribers.json()), f"it answered {subscribers.text[:200]}"


def test_editor_cannot_release_or_list_subscribers(db, form_token, editor_client, commercial_client):
    email, lead = _quarantined_lead(db, form_token)
    release = editor_client.post(f"/office/leads/{lead['id']}/release", json={})
    assert release.status_code in DENIED, f"an editor release returned {release.status_code}"
    assert db.lead(email)["status"] == "quarantined", "an editor release changed the lead"
    assert editor_client.get("/office/subscribers").status_code in DENIED, "an editor read the subscriber list"
    listed = commercial_client.get("/office/subscribers")
    assert listed.status_code == 200 and isinstance(items(listed.json()), list), (
        f"the commercial subscriber list returned {listed.status_code}"
    )


def test_commercial_is_denied_product_publishing(editor_client, commercial_client):
    for staff in (commercial_client, editor_client):
        listing = staff.get("/office/products", params={"locale": "en"})
        assert listing.status_code == 200, f"the product list returned {listing.status_code}"
        rows = items(listing.json())
        assert len(rows) == 20 and all("published" in r for r in rows), f"the product list is {listing.text[:200]}"
    denied = commercial_client.post(f"/office/products/{TERRA_PLANTER_ID}/unpublish", json={"locale": "en"})
    assert denied.status_code in DENIED, f"a commercial unpublish returned {denied.status_code}"
    assert TERRA_PLANTER_ID in product_ids("en"), "a denied unpublish removed the product"


def test_editor_unpublish_hides_product_until_republished(db, editor_client):
    rows = {str(r.get("id")): r for r in items(editor_client.get("/office/products", params={"locale": "pt"}).json())}
    slug = str(rows[GOLF_BAG_STAND_ID].get("slug"))
    title_word = str(rows[GOLF_BAG_STAND_ID].get("title")).split()[0]
    before = db.audit_count("product.unpublish", GOLF_BAG_STAND_ID)
    try:
        hidden = editor_client.post(f"/office/products/{GOLF_BAG_STAND_ID}/unpublish", json={"locale": "pt"})
        assert hidden.status_code == 200 and hidden.json().get("published") is False, (
            f"unpublishing returned {hidden.status_code} {hidden.text[:200]}"
        )
        assert len(product_ids("pt")) == 19, "the Portuguese catalogue still counts the unpublished product"
        assert get(f"/pt/produtos/golfe/{slug}").status_code == 404, "the unpublished product route still answers"
        found = api_get("/search", params={"q": title_word, "locale": "pt"}).json().get("products") or []
        assert GOLF_BAG_STAND_ID not in {str(p.get("id")) for p in found}, "search still finds the unpublished product"
        assert slug not in get("/sitemap-pt.xml").text, "the Portuguese sitemap still lists the unpublished product"
        assert db.audit_count("product.unpublish", GOLF_BAG_STAND_ID) == before + 1, "unpublishing wrote no audit event"
    finally:
        restored = editor_client.post(f"/office/products/{GOLF_BAG_STAND_ID}/publish", json={"locale": "pt"})
    assert restored.status_code == 200 and restored.json().get("published") is True, (
        f"republishing returned {restored.status_code} {restored.text[:200]}"
    )
    assert len(product_ids("pt")) == 20, "republishing did not restore the Portuguese catalogue"
    assert db.audit_count("product.publish", GOLF_BAG_STAND_ID) >= 1, "republishing wrote no audit event"


def test_commercial_reads_quotation_with_its_lines(db, form_token, commercial_client):
    email, body, lead = _quotation_lead(db, form_token)
    listing = commercial_client.get("/office/leads", params={"kind": "quotation"})
    assert listing.status_code == 200, f"the commercial listing returned {listing.status_code}"
    assert any(str(r.get("id")) == str(lead["id"]) for r in items(listing.json())), "the new quotation is not listed"
    detail = commercial_client.get(f"/office/leads/{lead['id']}")
    assert detail.status_code == 200, f"the commercial detail returned {detail.status_code}"
    quotation = detail.json().get("quotation") or {}
    assert quotation.get("reference") == body["reference"] and int(quotation.get("itemCount")) == 2, (
        f"the detail quotation is {quotation!r}"
    )
    first = (quotation.get("items") or [{}])[0]
    assert first.get("productTitle") == TEE_SIGN_TITLE and (first.get("options") or {}).get("size") == "M", (
        f"the first line is {first!r}"
    )
    assert "Size: M" in str(quotation.get("payloadRendered")), "the detail lacks the rendered payload"
    assert detail.json().get("taxId") == "0012 345", f"the detail taxId is {detail.json().get('taxId')!r}"
    assert db.audit_count("lead.read", lead["id"]) >= 1, "a commercial read wrote no audit event"


def test_commercial_releases_quarantined_enquiry(db, form_token, commercial_client):
    email, lead = _quarantined_lead(db, form_token)
    released = commercial_client.post(f"/office/leads/{lead['id']}/release", json={})
    assert released.status_code == 200, f"releasing returned {released.status_code}: {released.text[:200]}"
    assert db.lead(email)["status"] in ("received", "queued", "delivered"), "the released lead did not move on"
    assert db.audit_count("lead.release", lead["id"]) == 1, "releasing wrote no audit event"
    wait_for_mail(email, CONTACT_SUBJECT)


def test_releasing_a_non_quarantined_enquiry_is_refused(db, form_token, commercial_client):
    email = probe_email()
    assert submit_contact(email, form_token).status_code == ACCEPTED
    lead = db.lead(email)
    response = commercial_client.post(f"/office/leads/{lead['id']}/release", json={})
    assert 400 <= response.status_code < 500, f"releasing a normal lead returned {response.status_code}"
    assert error_code(response) == "invalid_state", f"the code is {error_code(response)!r}"
    assert db.lead(email)["status"] != "quarantined", "releasing a normal lead quarantined it"


def test_logout_revokes_the_token():
    token = token_for(COMMERCIAL_EMAIL)
    with client(token) as staff:
        out = staff.post("/auth/logout", json={})
        assert out.status_code == 204, f"logout returned {out.status_code}"
        after = staff.get("/office/me")
    assert after.status_code in DENIED, f"a revoked token still reached /api/office/me: {after.status_code}"


def test_suspended_account_is_denied(db):
    response = httpx.post(api("/auth/login"), json={"email": SUSPENDED_EMAIL, "password": SEEDED_PASSWORD_DEFAULT},
                          timeout=60.0)
    assert response.status_code == 401, f"a suspended account sign-in returned {response.status_code}"
    assert "access_token" not in response.text, "a suspended account received a token"
    wrong = httpx.post(api("/auth/login"), json={"email": COMMERCIAL_EMAIL, "password": "not-the-password-1"},
                       timeout=60.0)
    assert error_code(response) == error_code(wrong), "the suspended denial differs from a wrong password"
    row = db.staff(SUSPENDED_EMAIL)
    assert row is not None and row["status"] == "suspended", f"the suspended staff row is {row!r}"


def test_seeded_staff_accounts_are_not_duplicated(db):
    for email, role in ((COMMERCIAL_EMAIL, "commercial"), (EDITOR_EMAIL, "editor"), (SUSPENDED_EMAIL, "commercial")):
        assert db.count_staff(email) == 1, f"{db.count_staff(email)} staff rows exist for {email}"
        assert db.staff(email)["role"] == role, f"{email} holds role {db.staff(email)['role']!r}"
        assert db.staff(email)["display_name"], f"{email} has no display name"


def test_signup_route_does_not_exist():
    for path in ("/auth/signup", "/auth/register", "/office/staff"):
        response = api_post(path, {"email": probe_email(), "password": "Pass-word-12345"})
        assert not 200 <= response.status_code < 300, f"POST /api{path} returned {response.status_code}"
