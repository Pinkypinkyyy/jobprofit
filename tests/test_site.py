from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = list(ROOT.glob("*.html"))
HOSP = "PinkAccountingTaxSolutionsClientBookings"
FIELD = "ServiceProfit@pinktax.com.au"
CACHE = "rt30"


def test_no_hospitality_booking():
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        assert HOSP not in text, p.name


def test_book_uses_service_profit_calendar():
    text = (ROOT / "book.html").read_text(encoding="utf-8")
    assert FIELD in text
    assert HOSP not in text
    assert "Open the Service Profit calendar" in text
    assert "not taking new times" not in text
    assert 'id="enquiryForm"' in text
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
    assert 'href="/hvac.html"' in home
    nav_home = home
    assert 'href="/hvac.html">HVAC</a>' in nav_home
    assert 'href="/electrical.html">Electrical</a>' in nav_home
    assert 'href="/construction.html">Construction</a>' in nav_home


def test_google_reviews_visible():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "5.0" in home
    assert "25 Google reviews" in home
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
    assert '"@type":"Service"' in (ROOT / "hvac.html").read_text(encoding="utf-8")
    assert '"@type":"Service"' in (ROOT / "electrical.html").read_text(encoding="utf-8")
    assert '"@type":"Service"' in (ROOT / "construction.html").read_text(encoding="utf-8")
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
    assert (ROOT / "assets" / "pink-home.webp").exists()
    assert (ROOT / "assets" / "tech-hvac-480.webp").exists()
    assert (ROOT / "favicon.ico").exists()


def test_cache_buster_consistent():
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        assert f"styles.css?v={CACHE}" in text, p.name
        assert "rt15" not in text and "rt20" not in text and "rt23" not in text, p.name


def test_privacy_and_terms_on_every_page():
    for p in HTML:
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


def test_hvac_has_callback_video():
    text = (ROOT / "hvac.html").read_text(encoding="utf-8")
    assert 'callback-cost.mp4' in text
    assert "<video" in text
    assert (ROOT / "assets" / "video" / "callback-cost.mp4").exists()
    assert (ROOT / "assets" / "video" / "callback-cost-poster.jpg").exists()
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "callback-cost.mp4" in home


def test_fees_are_monthly_only():
    banned = ("$19,800", "$31,800", "$42,000", "$6,600", "/ yr", "/ year", "+ GST a year")
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        for token in banned:
            assert token not in text, (p.name, token)


def test_trade_pages_cross_link():
    hvac = (ROOT / "hvac.html").read_text(encoding="utf-8")
    electrical = (ROOT / "electrical.html").read_text(encoding="utf-8")
    construction = (ROOT / "construction.html").read_text(encoding="utf-8")
    assert "Electrician instead?" in hvac
    assert "/electrical.html" in hvac
    assert "/construction.html" in hvac
    assert "HVAC instead?" in electrical
    assert "/hvac.html" in electrical
    assert "Electrician instead?" in construction


def test_mobile_pricing_and_a11y_hooks():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert ".table-scroll" in css
    assert ".scope-cards" in css
    assert "Escape" in js
    assert 'href="/hvac.html" data-trade="hvac"' in home
    assert 'role="tablist"' not in home
    assert "hvac.html" in home


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


def test_sitemap_has_trade_pages():
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for slug in ("hvac.html", "electrical.html", "construction.html", "terms.html", "pricing.html"):
        assert slug in sm


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS", name)
    print("all site tests passed")
