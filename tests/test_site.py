import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_pages import REVIEWS_AS_AT, REVIEWS_COUNT  # noqa: E402
from shared import ASSET, GBP  # noqa: E402
HTML = list(ROOT.glob("*.html"))
REDIRECTS = {ROOT / "hvac.html", ROOT / "electrical.html", ROOT / "construction.html"}
PAGES = [p for p in HTML if p not in REDIRECTS]
HOSP = "PinkAccountingTaxSolutionsClientBookings"
FIELD = "ServiceProfit@pinktax.com.au"
CACHE = ASSET  # read from tools/shared.py so a bump cannot desync the test


def _contrast(a, b):
    """WCAG relative-contrast ratio between two #rrggbb colours."""
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    def lum(h):
        h = h.lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def test_no_hospitality_booking():
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        assert HOSP not in text, p.name


def test_book_uses_service_profit_calendar():
    text = (ROOT / "book.html").read_text(encoding="utf-8")
    assert FIELD in text
    assert HOSP not in text
    assert "Open full-screen booking" in text
    assert "not taking new times" not in text
    assert 'id="enquiryForm"' in text
    assert 'name="business"' in text
    assert 'name="trade"' in text
    assert 'name="revenue"' in text
    assert 'name="staff"' in text
    assert 'name="hurt"' in text
    assert 'name="position"' in text
    assert 'name="vision"' in text
    assert "Annual revenue" in text
    assert "Where is the business now" in text
    assert "Where do you want it in 12 months" in text
    # HB 24 Sep 2026: pick a time first; the questions come after and are optional.
    assert text.find('id="pick-time"') < text.find('id="enquiryForm"')
    assert "sell-grid" not in text
    assert "book-steps" not in text
    assert "You quoted 6 hours. You did 9." not in text
    assert "hoursCheck" not in text
    assert 'href="/check.html"' in (ROOT / "index.html").read_text(encoding="utf-8")
    check = (ROOT / "check.html").read_text(encoding="utf-8")
    assert "hoursCheck" in check
    assert "Where did the last job leak?" in check
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'href="/book.html"' in home


def test_pricing_page_exists():
    text = (ROOT / "pricing.html").read_text(encoding="utf-8")
    for plan in ("Job Profit", "Weekly Visibility", "Ready to Scale", "Compliance"):
        assert plan in text
    assert "What is in Job Profit?" in text
    assert "FAQPage" in text
    nav_home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'href="/pricing.html"' in nav_home
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "pricing.html" in sm


def test_hero_is_not_plenum():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "tech-hvac" in home
    assert 'data-trade="hvac"' in home
    assert "assets/hvac.jpg" not in home
    assert "HVAC technician on a rooftop unit" in home


def test_homepage_does_not_repeat_trade_photos():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'class="tile"' not in home
    assert home.count('alt="HVAC technician on a rooftop unit"') == 1
    assert home.count('alt="Electrician testing a switchboard"') == 1
    assert home.count('alt="Electrical switchboard"') == 1
    assert home.count('alt="Construction services fit-out"') == 1
    assert 'href="/hvac.html">HVAC</a>' not in home
    assert "You quoted 6 hours. You did 9." in home
    assert "The call is to see if we can take the file." in home
    assert "One line." not in home


def test_google_reviews_visible():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "5.0" in home
    # Count and date come from build_pages so the page and the test cannot drift.
    assert f"{REVIEWS_COUNT} Google reviews as at {REVIEWS_AS_AT}" in home
    assert f"Read all {REVIEWS_COUNT} Google reviews" in home
    assert "Reviews of Pink Accounting, the firm behind Service Profit" in home
    assert "T D · Google" in home
    assert "N T · Google" in home
    assert "N M · Google" in home
    assert "Worked example, not a client result" in home
    assert "chart-hours" in home
    assert "Quoted 6 hours. Nine on the tools." in home
    assert "chart-cash" in home
    assert "chart-fall" in (ROOT / "system.html").read_text(encoding="utf-8")
    assert "Real clients, not a worked example" not in home
    assert "not labelled as HVAC" not in home
    assert "aggregateRating" not in home


def test_analytics_tags():
    track = (ROOT / "track.js").read_text(encoding="utf-8")
    assert "G-8T6SXPNSCW" in track
    assert "GT-WVXQ29L2" in track
    assert "generate_lead" in track
    assert "connect.facebook.net" in track
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "track.js" in home
    privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")
    assert "Google Analytics 4" in privacy


def test_structured_data_on_inner_pages():
    assert "AccountingService" in (ROOT / "index.html").read_text(encoding="utf-8")
    assert "FAQPage" in (ROOT / "system.html").read_text(encoding="utf-8")
    contact = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert "AccountingService" in contact
    assert "sameAs" in (ROOT / "index.html").read_text(encoding="utf-8")
    assert "facebook.com/profile.php?id=61594432044788" in (ROOT / "index.html").read_text(encoding="utf-8")
    assert "linkedin.com/company/143802027" in (ROOT / "index.html").read_text(encoding="utf-8")
    assert "facebook.com/pinkaccountingtax" not in (ROOT / "index.html").read_text(encoding="utf-8")
    assert "linkedin.com/company/pinkaccountingtax" not in (ROOT / "index.html").read_text(encoding="utf-8")


def test_lazy_load_and_webp():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert home.count("loading=\"lazy\"") >= 3
    assert "tech-hvac-480.webp" in home
    # pink-home now ships responsive variants rather than one full-size webp.
    for w in (480, 864, 1200):
        assert (ROOT / "assets" / f"pink-home-{w}.webp").exists()
    assert (ROOT / "assets" / "tech-hvac-480.webp").exists()
    assert (ROOT / "favicon.ico").exists()


def test_cache_buster_consistent():
    for p in PAGES:
        text = p.read_text(encoding="utf-8")
        assert f"styles.css?v={CACHE}" in text, p.name
        assert "rt15" not in text and "rt20" not in text and "rt23" not in text, p.name


def test_privacy_and_terms_on_every_page():
    for p in PAGES:
        text = p.read_text(encoding="utf-8")
        assert "privacy.html" in text, p.name
        assert "terms.html" in text, p.name
        assert "og.png" in text, p.name
        assert "Service Profit" in text, p.name
        assert 'href="/favicon.ico"' in text, p.name


def test_queensland_not_australia_wide_claim():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Australia-wide" not in home
    assert "Queensland" in home
    assert "Brendale" in home
    assert "Brisbane" in home
    assert "areaServed" in home and "Queensland" in home
    assert "Brendale" in (ROOT / "contact.html").read_text(encoding="utf-8")


def test_404_uses_service_profit_name_and_root_paths():
    text = (ROOT / "404.html").read_text(encoding="utf-8")
    assert "Service Profit" in text
    assert "Go back to Job Profit" not in text
    assert 'href="/styles.css' in text
    assert 'href="/index.html"' in text


def test_why_has_subheadings():
    text = (ROOT / "why.html").read_text(encoding="utf-8")
    assert text.lower().count("<h2") >= 4
    assert "Qualification" in text
    assert "Years in the books" in text
    assert "What we hold" in text
    assert "On the public register" in text


def test_callback_video_on_homepage_not_fake_trade_pages():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "callback-cost.mp4" in home
    assert "<video" in home
    assert (ROOT / "assets" / "video" / "callback-cost.mp4").exists()
    assert (ROOT / "assets" / "video" / "callback-cost-poster.jpg").exists()
    hvac = (ROOT / "hvac.html").read_text(encoding="utf-8")
    assert "callback-cost.mp4" not in hvac
    assert 'rel="canonical" href="https://www.serviceprofit.com.au/air-conditioning-accountant-brisbane/"' in hvac


def test_fees_are_monthly_only():
    banned = ("$19,800", "$31,800", "$42,000", "$6,600", "/ yr", "/ year", "+ GST a year")
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        for token in banned:
            assert token not in text, (p.name, token)


def test_old_trade_urls_redirect_to_audience_pages():
    mapping = {
        "hvac": "/air-conditioning-accountant-brisbane/",
        "electrical": "/electrician-accountant-brisbane/",
        "construction": "/construction-services-accountant-brisbane/",
    }
    for slug, dest in mapping.items():
        text = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
        assert f"url={dest}" in text
        assert f'location.replace("{dest}")' in text
        assert "one offer" in text.lower()
        assert dest in (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_mobile_pricing_and_a11y_hooks():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert ".table-scroll" in css
    assert ".scope-cards" in css
    assert "Escape" in js
    assert "aria-pressed" in home
    assert 'role="tablist"' not in home
    assert 'href="/pricing.html"' in home


def test_pink_brand_not_a_second_identity():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Montserrat" in css
    assert "IBM Plex" not in css
    assert "#ED1651" in css
    assert "#1E6BD6" not in css
    assert "logo-white.png" in home
    assert "Pink Accounting" in home
    assert 'alt="pink"' in home
    og = ROOT / "assets" / "og.png"
    assert og.exists()


def test_sitemap_has_real_pages_not_fake_trades():
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for slug in ("terms.html", "pricing.html", "system.html", "check.html"):
        assert slug in sm
    for slug in (
        "air-conditioning-accountant-brisbane/",
        "electrician-accountant-brisbane/",
        "construction-services-accountant-brisbane/",
        "quoted-hours-vs-actual-hours/",
        "cash-that-is-yours/",
        "can-i-afford-another-technician/",
    ):
        assert slug in sm
        assert "<lastmod>" in sm
    assert "hvac.html" not in sm
    assert "electrical.html" not in sm
    assert "construction.html" not in sm



def test_forms_have_captcha_and_honeypot():
    for page in ("book.html", "contact.html"):
        html = (ROOT / page).read_text(encoding="utf-8")
        assert 'name="_captcha" value="true"' in html, page
        assert 'name="_captcha" value="false"' not in html, page
        assert 'name="_gotcha"' in html, page


def test_contact_has_a_form_not_just_phone_and_email():
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert 'action="https://formsubmit.co/admin@pinktax.com.au"' in html
    assert 'name="message"' in html
    # The short form, not the full book.html intake.
    assert 'name="revenue"' not in html
    assert "contact.html?sent=1" in html


def test_hero_keeps_its_side_gutter_on_mobile():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    # A padding shorthand here zeroes the inline padding .wrap sets, which put
    # the hero CTAs at x=0 on a phone. Only the block axis may be set.
    assert ".hero-grid{display:block;min-height:0;padding-block:28px 40px}" in css
    for bad in ("padding:28px 0 40px", "padding:calc(var(--nav-h) + 28px) 0 36px"):
        assert bad not in css, bad


def test_hero_primary_cta_is_readable_on_the_dark_photo():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert ".hero-copy .btn-primary{background:#fff" in css


def test_rights_lists_the_trading_business_name():
    html = (ROOT / "rights.html").read_text(encoding="utf-8")
    assert "Service Profit Accounting" in html


def test_callback_video_is_phone_sized():
    mp4 = ROOT / "assets" / "video" / "callback-cost.mp4"
    assert mp4.exists()
    mb = mp4.stat().st_size / 1_000_000
    # It was 20.7 MB. Anyone tapping play on a phone plan pays for this.
    assert mb < 5, f"callback-cost.mp4 is {mb:.1f} MB"


def test_titles_fit_a_search_result():
    import re
    for page in ROOT.glob("*.html"):
        html = page.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if not m:
            continue
        assert len(m.group(1)) <= 62, f"{page.name} title is {len(m.group(1))} chars"


def test_schema_points_at_the_google_business_profile():
    # The strongest entity signal a local firm has. It was missing from sameAs.
    for page in ("index.html", "contact.html"):
        html = (ROOT / page).read_text(encoding="utf-8")
        assert GBP in html, page


def test_no_em_dashes_in_our_own_copy():
    # House style. The one Google review quote is verbatim and is exempt.
    quote = "Pink is amazing"
    for page in ROOT.glob("*.html"):
        for line in page.read_text(encoding="utf-8").splitlines():
            if "\u2014" in line:
                assert quote in line, f"{page.name}: {line.strip()[:90]}"


def test_booking_form_does_not_demand_three_essays():
    import re
    html = (ROOT / "book.html").read_text(encoding="utf-8")
    required = re.findall(r"<(?:input|select|textarea)[^>]*\brequired\b", html)
    assert len(required) <= 8, f"{len(required)} required fields on the booking form"
    req_textareas = re.findall(r"<textarea[^>]*\brequired\b", html)
    assert len(req_textareas) <= 1, f"{len(req_textareas)} required essay boxes"


def test_live_reviews_are_parsed_filtered_and_escaped():
    from build_pages import load_reviews

    fixture = ROOT / "tests" / "fixtures" / "google_reviews_sample.json"
    rating, count, as_at, quotes, url = load_reviews(fixture)
    assert rating == "4.9"
    assert count == 34
    assert as_at == "November 2026"
    # The 2-star review must not reach the page.
    assert all("Too slow" not in q[0] for q in quotes)
    assert len(quotes) == 3
    # Every quote carries an author and a link back, as Places terms require.
    assert all(q[1] and q[2] for q in quotes)


def test_review_text_from_google_is_escaped():
    import html as _html
    from build_pages import load_reviews

    fixture = ROOT / "tests" / "fixtures" / "google_reviews_sample.json"
    _, _, _, quotes, _ = load_reviews(fixture)
    injected = [q for q in quotes if "script" in q[0]]
    assert injected, "fixture should carry the injection case"
    assert "&lt;script&gt;" in _html.escape(injected[0][0])


def test_site_falls_back_when_there_is_no_live_review_file():
    from build_pages import load_reviews

    rating, count, as_at, quotes, url = load_reviews(ROOT / "tests" / "fixtures" / "nope.json")
    assert rating == "5.0"
    assert count == 32
    assert len(quotes) == 3


def test_no_api_key_is_shipped_to_the_browser():
    # The Places fetch is build-time only. A key in a page would be public.
    for page in ROOT.glob("*.html"):
        html = page.read_text(encoding="utf-8")
        assert "GOOGLE_PLACES_API_KEY" not in html, page.name
        assert "places.googleapis.com" not in html, page.name
        assert "AIza" not in html, page.name


def test_js_does_not_override_the_forms_captcha_setting():
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    # The ajax path is the one visitors use. It used to hardcode _captcha
    # back to "false", so the hidden field in the HTML did nothing.
    assert '_captcha = "false"' not in js
    assert '_captcha="false"' not in js
    assert "formShownAt" in js, "time trap missing"


def test_mailto_fallback_carries_every_field_the_visitor_filled():
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    # Built from the submitted data, not a hand-listed set that silently
    # dropped contact.html's message field.
    assert "Object.keys(data)" in js
    assert "message:" in js


def test_every_shipped_asset_is_actually_referenced():
    import re
    referenced = set()
    for page in list(ROOT.glob("*.html")) + [ROOT / "styles.css"]:
        for m in re.findall(r"/assets/([A-Za-z0-9._-]+)", page.read_text(encoding="utf-8")):
            referenced.add(m)
    orphans = []
    for f in (ROOT / "assets").glob("*"):
        if f.is_file() and f.name not in referenced:
            orphans.append(f.name)
    assert not orphans, f"unreferenced assets still deploying: {sorted(orphans)}"


def test_the_weekly_output_sample_is_on_the_system_page():
    html = (ROOT / "system.html").read_text(encoding="utf-8")
    assert 'id="weekly"' in html
    assert "wsample" in html
    # It is invented data and must say so.
    assert "not a client file" in html.lower()
    # And the homepage must point at it.
    assert "/system.html#weekly" in (ROOT / "index.html").read_text(encoding="utf-8")


def test_pricing_answers_the_cheap_bookkeeper_objection():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    assert "bookkeeper charges" in html
    assert "does not pay for itself" in html


def test_form_endpoint_is_defined_in_one_place():
    from shared import FORM_AJAX_ENDPOINT, FORM_ENDPOINT, FORM_ORIGIN

    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    # nav.js must not carry its own copy of the endpoint.
    assert "formsubmit.co" not in js
    assert "data-ajax" in js
    for page in ("book.html", "contact.html"):
        html = (ROOT / page).read_text(encoding="utf-8")
        assert f'action="{FORM_ENDPOINT}"' in html
        assert f'data-ajax="{FORM_AJAX_ENDPOINT}"' in html
        # CSP must allow wherever the form actually posts.
        csp = [l for l in html.splitlines() if "Content-Security-Policy" in l][0]
        assert FORM_ORIGIN in csp


def test_colours_on_dark_panels_meet_aa():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    ratio = _contrast

    import re
    tokens = dict(re.findall(r"--(accent-on-dark|gold-on-dark):(#[0-9A-Fa-f]{6})", css))
    assert set(tokens) == {"accent-on-dark", "gold-on-dark"}, tokens
    for name, hex_ in tokens.items():
        # Darkest panel the tokens are used on.
        assert ratio(hex_, "#121A1C") >= 4.5, f"{name} {hex_} fails AA on dark"
    # The raw brand colours must not be used for text on those panels.
    assert ".docket-row.is-miss b{color:var(--gold-on-dark)}" in css
    assert ".wsample-list li.is-you b{color:var(--accent-on-dark)}" in css


def test_no_internal_link_or_asset_404s():
    """Every internal href, src and srcset must resolve to a file that ships.
    A broken one sends a visitor to the 404 page, which is exactly what a
    deleted asset or a renamed page looks like from the outside."""
    import os
    import re

    broken = []
    for page in sorted(ROOT.glob("*.html")):
        html = page.read_text(encoding="utf-8")
        refs = (
            re.findall(r'href="([^"]+)"', html)
            + re.findall(r'src="([^"]+)"', html)
            + re.findall(r'srcset="([^"]+)"', html)
        )
        for ref in refs:
            for part in ref.split(","):
                url = part.strip().split()[0] if part.strip() else ""
                if not url or url.startswith(("http", "mailto:", "tel:", "#", "data:")):
                    continue
                rel = url.split("?")[0].split("#")[0].lstrip("/") or "index.html"
                target = ROOT / rel
                # An extensionless URL only serves if there is a real file
                # behind it: dir/index.html, or name.html alongside it.
                served = (
                    target.is_file()
                    or (target / "index.html").is_file()
                    or target.with_name(target.name + ".html").is_file()
                )
                if not served:
                    broken.append(f"{page.name} -> {url}")
    assert not broken, "internal references that would 404: " + ", ".join(sorted(set(broken)))


def test_the_disclosure_url_resolves_three_ways():
    """Clients are given serviceprofit.com.au/disclosure. It must not depend
    on one host's pretty-URL behaviour, so all three spellings ship."""
    for path in ("disclosure.html", "disclosure/index.html"):
        assert (ROOT / path).is_file(), path
    both = {(ROOT / p).read_text(encoding="utf-8") for p in ("disclosure.html", "disclosure/index.html")}
    assert len(both) == 1, "the two disclosure files have drifted apart"
    html = (ROOT / "disclosure.html").read_text(encoding="utf-8")
    assert 'rel="canonical" href="https://www.serviceprofit.com.au/disclosure"' in html
    assert "tpb.gov.au/public-register" in html
    assert "tpb.gov.au/complaints" in html
    assert "/disclosure" in (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_the_section_45_wording_cannot_drift_between_pages():
    from build_pages import DISCLOSURE_STATEMENTS

    rights = (ROOT / "rights.html").read_text(encoding="utf-8")
    disclosure = (ROOT / "disclosure.html").read_text(encoding="utf-8")
    for statement in DISCLOSURE_STATEMENTS:
        assert statement in rights, statement[:50]
        assert statement in disclosure, statement[:50]


def test_homepage_lets_a_visitor_rule_themselves_out():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Is this you?" in html
    # Willingness to exclude is the trust signal. It must survive edits.
    assert "You are a builder" in html
    assert "pinktax.com.au" in html
    assert "Compliance at $550" in html


def test_homepage_says_what_happens_after_the_call():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for step in ("A 15-minute call", "A letter, then you decide", "The first month"):
        assert step in html, step
    assert "Nothing starts until you sign it." in html


def test_homepage_explains_the_name_ladder_once():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    # Six names in one visit. The relationship has to be stated somewhere
    # other than the footer.
    assert "The names, once:" in html
    for name in ("Pink Accounting", "Service Profit", "Job Profit"):
        assert name in html


def test_homepage_carries_the_no_conditions_statement():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "no conditions limiting" in html
    assert "/disclosure" in html


def test_office_hours_come_from_identity_and_bookings_stay_mon_thu():
    """HB 24 Sep 2026: office hours are Mon-Fri for the whole firm. The trades
    booking calendar is Mon-Thu; that is when calls book, not office hours."""
    import json
    ident = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert ident["office"]["hours"]["display"] in html
    assert "15-minute calls run Monday to Thursday" in html
    days = json.dumps(ident["office"]["hours"]["days"], separators=(",", ":"))
    assert f'"dayOfWeek":{days}' in html


def test_the_weekly_sample_figures_actually_add_up():
    """An accountant's site showing numbers that do not reconcile is worse
    than showing none. The sample is a permanent worked example, so this
    guards whoever edits the figures next."""
    from build_pages import WEEKLY_SAMPLE, weekly_yours

    w = WEEKLY_SAMPLE
    held = sum(amount for _, amount in w["holdbacks"])
    assert weekly_yours() == w["bank"] - held
    assert weekly_yours() > 0, "holdbacks exceed the bank balance"

    over = w["hours_actual"] - w["hours_quoted"]
    assert over > 0, "the sample only makes its point if the job ran over"
    named_overrun = sum(a - q for _, q, a in w["jobs"])
    assert named_overrun <= over, (
        "the named jobs overrun by more than the week's total, which cannot happen"
    )

    html = (ROOT / "system.html").read_text(encoding="utf-8")
    assert f"${w['bank']:,}" in html
    assert f"${weekly_yours():,}" in html
    assert str(over) in html


def test_the_weekly_sample_carries_no_client_identifiers():
    from build_pages import WEEKLY_SAMPLE

    blob = repr(WEEKLY_SAMPLE).lower()
    # The sample is deliberately invented and stays that way. No ABN, no TFN,
    # no trading name, no job number, not even an anonymised real one.
    import re
    assert not re.search(r"\b\d{11}\b", blob), "an 11-digit number looks like an ABN"
    assert not re.search(r"\b\d{8,9}\b", blob), "an 8-9 digit number looks like a TFN"
    assert "pty" not in blob and "ltd" not in blob


def test_no_claim_implies_existing_service_profit_clients():
    """There is no Service Profit client with real figures yet. Nothing on the
    site may imply otherwise, and every number shown must be labelled as an
    example. This is the ACCC exposure, not a style preference."""
    import re

    banned = (
        r"our clients",
        r"clients see",
        r"clients save",
        r"we have helped",
        r"typical client",
        r"results speak",
        r"on average,? (?:our|clients)",
    )
    for page in sorted(ROOT.glob("*.html")):
        text = page.read_text(encoding="utf-8").lower()
        for pattern in banned:
            assert not re.search(pattern, text), f"{page.name} matches {pattern!r}"

    # Every figure-bearing illustration keeps its label.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert home.count("Worked example, not a client result.") >= 2
    assert "illustration, not a client file" in home
    system = (ROOT / "system.html").read_text(encoding="utf-8")
    assert "Invented figures, not a client file" in system
    assert system.count("Worked example, not your rate.") >= 2


def test_industry_pages_are_audience_not_products():
    """Same offer. Unique job language. Not three products in the nav."""
    pages = {
        "air-conditioning-accountant-brisbane": (
            "Quoted six hours on the roof. Nine on the tools.",
            "rooftop changeover",
        ),
        "electrician-accountant-brisbane": (
            "The switchboard ran long. The quote did not.",
            "board upgrade",
        ),
        "construction-services-accountant-brisbane": (
            "For fit-out, maintenance and installation businesses.",
            "head contracting",
        ),
    }
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    nav = home.split("<nav class=\"links\"")[1].split("</nav>")[0]
    import re
    for slug, (h1, unique) in pages.items():
        html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        heading = re.search(r"<h1>(.*?)</h1>", html, re.S).group(1)
        # HB 24 Sep 2026: the H1 is the search words, big. The hook stays, right under it.
        assert "accountant" in heading.lower() and "brisbane" in heading.lower(), slug
        assert f'<p class="hook">{h1}</p>' in html, slug
        assert unique in html.lower(), slug
        assert "Job Profit is $1,650 + GST a month" in html
        assert "Same plans as the rest of Service Profit" in html
        assert f'href="/{slug}/"' not in nav
        assert (ROOT / f"{slug}.html").read_text(encoding="utf-8") == html
    assert "Pricing" in nav and "The system" in nav
    assert "HVAC</a>" not in nav


def test_hours_check_has_a_crew_calculator():
    check = (ROOT / "check.html").read_text(encoding="utf-8")
    assert 'id="hoursCheck"' in check
    assert 'id="crewCheck"' in check
    assert 'name="techs"' in check
    assert 'name="leak"' in check
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    assert "hours-check-crew" in js
    assert "52" in js


def test_cornerstone_pages_exist():
    pages = {
        "quoted-hours-vs-actual-hours": "Quoted hours versus hours on the tools",
        "cash-that-is-yours": "The bank looks full. It is not all yours.",
        "can-i-afford-another-technician": "Can I afford another technician?",
    }
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    for slug, h1 in pages.items():
        html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        assert f"<h1>{h1}</h1>" in html, slug
        assert "Job Profit is $1,650 + GST a month" in html
        assert f'href="/{slug}/"' in home


def test_why_has_person_schema_and_firm_continuity():
    html = (ROOT / "why.html").read_text(encoding="utf-8")
    assert '"@type":"Person"' in html
    assert "Huong Bui" in html
    assert "The file is held by the firm, not by one diary." in html


def test_llms_and_pricing_md_are_on_the_origin():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    fees = (ROOT / "pricing.md").read_text(encoding="utf-8")
    assert "Registered Tax Agent 26284368" in llms
    assert "air-conditioning-accountant-brisbane" in llms
    assert "pinktax.com.au" in llms
    assert "Australia-wide" not in llms
    assert "hospitality" in llms.lower()  # the split sentence, not a hospitality offer
    assert "Job Profit" in fees
    assert "$1,650" in fees
    assert "$550" in fees
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "Disallow: /" not in robots or "Allow: /" in robots
    assert "GPTBot" not in robots  # do not block AI citation crawlers


def test_homepage_has_website_schema_and_offer_catalog():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert '"@type":"WebSite"' in html
    assert "hasOfferCatalog" in html
    assert "1650.00" in html




def test_no_competitor_attack_copy():
    # HB, 18 Sep 2026, firm-wide and absolute, every surface: never attack
    # another firm or another accountant. An owner who chose their last
    # accountant hears it as an insult to their own judgement.
    #
    # The sell here is structural and needs no comparison: a job quoted at six
    # hours that took nine trains the next quote. That point stands alone.
    #
    # Same list as Pinkypinkyyy/pinktax so the two sites cannot drift apart.
    banned = (
        "autopsy",
        "old accountant",
        "files and forgets",
        "most accountants",
        "other accountants",
        "typical accountant",
        "traditional accounting",
        "traditional accountant",
        "unlike other",
        "unlike most",
        "your accountant never",
        "cheap accountant",
        "bad accountant",
        "wrong accountant",
    )
    for p in PAGES:
        text = p.read_text(encoding="utf-8").lower()
        for word in banned:
            assert word not in text, f"{p}: {word}"


def test_our_own_csp_does_not_block_analytics():
    # GA4 does not post to www.google-analytics.com. It picks analytics.google.com,
    # stats.g.doubleclick.net and www.google.com/g/collect at runtime. Leaving those
    # out of connect-src silently dropped every page_view and every generate_lead
    # conversion while the tag itself looked installed. Ads bidding starves on that.
    from shared import CSP
    connect = [d for d in CSP.split(";") if d.strip().startswith("connect-src")][0]
    for host in (
        "https://*.google-analytics.com",
        "https://analytics.google.com",
        "https://stats.g.doubleclick.net",
        "https://www.google.com",
    ):
        assert host in connect, f"{host} missing from connect-src"
    for p in PAGES:
        assert "https://stats.g.doubleclick.net" in p.read_text(encoding="utf-8"), p.name


def test_headings_do_not_skip_a_level():
    import re
    for p in PAGES:
        levels = [int(m) for m in re.findall(r"<h([1-6])[ >]", p.read_text(encoding="utf-8"))]
        assert levels and levels[0] == 1, f"{p.name}: first heading is h{levels[0] if levels else None}"
        for before, after in zip(levels, levels[1:]):
            assert after <= before + 1, f"{p.name}: h{before} jumps to h{after}"


def test_brand_link_accessible_name_leads_with_visible_text():
    # WCAG 2.5.3. The link reads "Service Profit" then "Pink Accounting" on screen,
    # so the accessible name has to start the same way or voice control misses it.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'aria-label="Service Profit Pink Accounting"' in home
    assert "Pink Accounting" in home


def test_cash_bar_pink_meets_aa():
    # White on raw --accent (#ED1651) is 4.34:1 at .68rem, under the 4.5 floor.
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert ".cash-bar .yours{background:var(--accent-deep);color:#fff}" in css
    assert ".cash-bar .yours{background:#ED1651" not in css
    assert _contrast("#D8124B", "#FFFFFF") >= 4.5
    assert _contrast("#B50E3E", "#FFFFFF") >= 4.5


def test_audience_pages_carry_breadcrumbs():
    import json, re
    slugs = [
        "air-conditioning-accountant-brisbane",
        "electrician-accountant-brisbane",
        "construction-services-accountant-brisbane",
        "quoted-hours-vs-actual-hours",
        "cash-that-is-yours",
        "can-i-afford-another-technician",
    ]
    for slug in slugs:
        text = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
        crumbs = [json.loads(b) for b in blocks]
        crumbs = [c for c in crumbs if c.get("@type") == "BreadcrumbList"]
        assert len(crumbs) == 1, f"{slug}: {len(crumbs)} BreadcrumbList blocks"
        items = crumbs[0]["itemListElement"]
        assert [i["position"] for i in items] == [1, 2]
        assert items[1]["item"].endswith(f"/{slug}/")
        assert items[1]["name"]


def test_no_photo_variant_is_wider_than_its_source():
    # The trade photos are 838px wide. The build used to emit 864 and 1200
    # variants from them, so a phone downloaded a third more bytes for pixels
    # the resampler had guessed. It looked soft on exactly the retina screens
    # this audience reads the site on. Never ship a variant above its source.
    from PIL import Image
    assets = ROOT / "assets"
    for src in assets.glob("*.jpg"):
        with Image.open(src) as im:
            source_width = im.width
        for variant in assets.glob(f"{src.stem}-*.webp"):
            width = int(variant.stem.rsplit("-", 1)[1])
            assert width <= source_width, (
                f"{variant.name} is {width}px from a {source_width}px source"
            )


def test_every_srcset_width_matches_a_file_that_exists():
    import re
    for p in PAGES:
        for entry in re.findall(r"/assets/([A-Za-z0-9._-]+\.webp)\?[^ ]* (\d+)w", p.read_text(encoding="utf-8")):
            name, width = entry
            assert (ROOT / "assets" / name).exists(), f"{p.name}: {name} missing"
            assert name.endswith(f"-{width}.webp"), f"{p.name}: {name} declared as {width}w"


def test_the_job_software_objection_is_answered():
    # The buyer runs simPRO, ServiceM8, AroFlo or similar and thinks the job
    # costing screen already answers this. If the site does not meet that on
    # the homepage, the rest of the page is arguing with someone who has left.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "You already have job software." in home
    assert "/job-software-and-your-accountant/" in home
    page = (ROOT / "job-software-and-your-accountant.html").read_text(encoding="utf-8")
    assert "So why an accountant?" in page
    for name in ("simPRO", "ServiceM8", "AroFlo"):
        assert name in page, name


def test_we_never_claim_to_work_inside_the_job_software():
    # HB, 18 Sep 2026: Pink has not used these platforms. The page positions
    # from the accountant's side on purpose. A future edit must not quietly
    # turn that into a capability claim that falls over on the first call.
    banned = (
        "we work in simpro",
        "we work in servicem8",
        "we work in aroflo",
        "simpro specialist",
        "servicem8 specialist",
        "certified partner",
        "we set up simpro",
        "we implement simpro",
    )
    for p in PAGES:
        text = p.read_text(encoding="utf-8").lower()
        for phrase in banned:
            assert phrase not in text, f"{p.name}: {phrase}"
    page = (ROOT / "job-software-and-your-accountant.html").read_text(encoding="utf-8")
    assert "We are not your software people" in page


def test_the_crew_check_puts_the_fee_next_to_the_leak():
    # The comparison is the persuasion. His numbers, our fee, he does the
    # arithmetic himself, so nothing here is a savings claim.
    import re
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    m = re.search(r"Job Profit is \$([0-9,]+) \+ GST a year", js)
    assert m, "crew result must state the annual fee"
    annual = int(m.group(1).replace(",", ""))
    pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
    monthly = re.search(r"\$([0-9,]+) \+ GST", pricing)
    assert monthly, "pricing page must state the monthly fee"
    assert annual == int(monthly.group(1).replace(",", "")) * 12, (
        f"nav.js says {annual} a year, pricing says {monthly.group(1)} a month"
    )


def test_the_trade_photos_keep_an_ungraded_original():
    # The grade is applied on build from assets/_source. If the originals go
    # missing, a rebuild would grade an already-graded file and the set would
    # drift darker every time anyone ran it.
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from build_assets import TRADE_STEMS
    for stem in TRADE_STEMS:
        assert (ROOT / "assets" / "_source" / f"{stem}.jpg").exists(), stem
        assert (ROOT / "assets" / f"{stem}.jpg").exists(), stem


def test_service_pages_carry_the_keyword_in_the_h1():
    import re
    pages = {
        "services": "accounting",
        "tax-agent-for-trades": "tax agent",
        "bas-and-gst-for-trades": "bas and gst",
        "payroll-for-trades": "payroll",
        "bookkeeping-and-xero-for-trades": "xero setup",
        "accountant-brendale": "accountant in brendale",
    }
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    nav = (ROOT / "index.html").read_text(encoding="utf-8").split('<nav class="links"')[1].split("</nav>")[0]
    assert 'href="/services/"' in nav
    for slug, keyword in pages.items():
        html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        assert (ROOT / f"{slug}.html").read_text(encoding="utf-8") == html
        heading = re.search(r"<h1>(.*?)</h1>", html, re.S).group(1)
        assert keyword in heading.lower(), slug
        assert f'rel="canonical" href="https://www.serviceprofit.com.au/{slug}/"' in html, slug
        assert f"/{slug}/</loc>" in sm, slug
        assert '"@type":"Service"' in html and "BreadcrumbList" in html, slug
        assert "Same plans as the rest of Service Profit" in html, slug


def test_home_h1_says_accountant_and_brendale():
    import re
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    heading = re.search(r"<h1>(.*?)</h1>", home, re.S).group(1).lower()
    # HB 24 Sep 2026: who we are first (accountants, bookkeepers, tax agents),
    # then who it is for, then the hook.
    for word in ("accountants", "bookkeepers", "tax agents", "brendale"):
        assert word in heading, word
    assert '<p class="hook">For air con, electrical and construction businesses.</p>' in home
    assert "You quoted 6 hours. You did 9." in home
    assert 'class="trust-line"' in home and 'class="call-icon"' in home


def test_pretty_page_canonicals_match_the_sitemap():
    # Canonical, sitemap, breadcrumbs and links must name one URL, not two.
    import re
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for loc in re.findall(r"<loc>(.*?)</loc>", sm):
        if not loc.endswith("/") or loc.count("/") < 4:
            continue
        slug = loc.rstrip("/").rsplit("/", 1)[1]
        html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        assert f'rel="canonical" href="{loc}"' in html, slug


def test_we_never_call_ourselves_a_bas_agent():
    # Tax agent registration covers BAS services (TPB). "BAS agent" is a
    # separate registration we do not hold, so we never claim the title.
    import re
    for p in PAGES:
        text = re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8")).lower()
        assert "registered bas agent" not in text, p.name
        for m in re.finditer(r"bas agent", text):
            before = text[max(0, m.start() - 40):m.start()]
            assert before.endswith(("separate ", "are you a ", "every registered tax and ", "all registered tax and ")), f"{p.name}: {before}"


def test_no_implied_existing_trade_clients():
    for p in PAGES:
        assert "working with trade businesses" not in p.read_text(encoding="utf-8").lower(), p.name


def test_404_is_not_indexed():
    assert 'content="noindex,follow"' in (ROOT / "404.html").read_text(encoding="utf-8")


def _identity():
    import json
    return json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))


def _ld_blocks(html):
    import json, re
    return [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


def test_identity_file_is_the_firm_canon():
    ident = _identity()
    assert ident["public_name"] == "Pink Accounting"
    assert ident["google_profile"]["count_allowed"] == 1


def test_schema_is_one_business_with_service_profit_as_a_department():
    """One @id for the firm on both sites. Service Profit never carries its own
    address or phone, or Google reads a second business at Shop 15A."""
    ident = _identity()
    org_id = ident["schema"]["organization_id"]
    for p in PAGES:
        for node in _ld_blocks(p.read_text(encoding="utf-8")):
            if node.get("@id") == org_id and "address" in node:
                assert node["name"] == ident["public_name"], p.name
                assert node["telephone"] == ident["office"]["phone_e164"], p.name
                assert node["address"]["streetAddress"] == ident["office"]["street"], p.name
                assert node["openingHoursSpecification"]["dayOfWeek"] == ident["office"]["hours"]["days"], p.name
                assert ident["google_profile"]["maps_url"] in node["sameAs"], p.name
                dept = node["department"][0]
                assert dept["name"] == "Service Profit"
                assert "address" not in dept and "telephone" not in dept
            # No node other than the firm may claim an address.
            if "address" in node and node.get("@type") != "PostalAddress":
                assert node.get("@id") == org_id, f"{p.name}: second business node {node.get('@id')}"
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert f'"@id":"{org_id}"' in home


def test_public_name_is_pink_accounting_only():
    import html as h, re
    ident = _identity()
    legal = ident["legal"]["entity"]            # "... Pty Ltd"
    stem = legal.replace(" Pty Ltd", "")
    for p in PAGES + [ROOT / "llms.txt"]:
        text = h.unescape(p.read_text(encoding="utf-8"))
        for banned in ident["banned_public_names"]:
            assert banned not in text, f"{p.name}: {banned}"
        for m in re.finditer(re.escape(stem), text):
            assert text[m.end():m.end() + 8] == " Pty Ltd", f"{p.name}: full name used as a business name"


def test_every_page_links_to_the_other_service_line_once():
    ident = _identity()["cross_links"]["on_trades_site"]
    for p in PAGES:
        html = p.read_text(encoding="utf-8")
        assert html.count('data-identity="cross-link"') == 1, p.name
        assert f'href="{ident["href"]}"' in html, p.name


def test_nap_on_pages_matches_identity():
    o = _identity()["office"]
    for p in PAGES:
        html = p.read_text(encoding="utf-8")
        assert o["street"] in html and o["postcode"] in html, p.name
        assert "tel:" + o["phone_e164"] in html, p.name


def test_review_fetcher_only_accepts_the_pink_accounting_profile():
    src = (ROOT / "tools" / "fetch_reviews.py").read_text(encoding="utf-8")
    assert 'CID = _ID["google_profile"]["cid"]' in src
    assert "is not the Pink Accounting profile" in src


def test_identity_watch_passes_our_pages_and_catches_drift():
    sys.path.insert(0, str(ROOT / "tools"))
    import identity_watch as w
    for page in ("index.html", "contact.html"):
        html = (ROOT / page).read_text(encoding="utf-8")
        assert w.check_page(html, page) == [], page
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert w.check_page(html.replace('"name":"Pink Accounting"', '"name":"Pink Tax Solutions"'), "x")
    assert w.check_page(html.replace('data-identity="cross-link"', 'data-x="y"'), "x")


def test_no_template_code_leaks_onto_a_page():
    # 24 Sep 2026: the Brendale page shipped a raw {ID[...]} placeholder.
    import re
    for p in PAGES:
        text = p.read_text(encoding="utf-8")
        assert not re.search(r"\{ID\[|\{[A-Za-z_]+\(\)\}", text), p.name


def test_services_dropdown_on_every_page():
    # HB 24 Sep 2026: every service one click away from any page.
    from shared import SERVICE_MENU
    for p in PAGES:
        html = p.read_text(encoding="utf-8")
        nav = html.split('<nav class="links"')[1].split("</nav>")[0]
        assert 'class="navdrop"' in nav and 'aria-controls="svcMenu"' in nav, p.name
        for href, label, _ in SERVICE_MENU:
            assert f'href="{href}"' in nav, f"{p.name}: {href}"
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    assert "navdrop-toggle" in js and "aria-expanded" in js


# Must stay at the very bottom: CI runs this file as a script, and any test
# defined below this block would silently never run.
if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS", name)
    print("all site tests passed")
