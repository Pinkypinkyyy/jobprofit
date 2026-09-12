from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = list(ROOT.glob("*.html"))
REDIRECTS = {ROOT / "hvac.html", ROOT / "electrical.html", ROOT / "construction.html"}
PAGES = [p for p in HTML if p not in REDIRECTS]
HOSP = "PinkAccountingTaxSolutionsClientBookings"
FIELD = "ServiceProfit@pinktax.com.au"
CACHE = "rt36"


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
    assert text.find('id="enquiryForm"') < text.find('id="pick-time"')
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
    assert (ROOT / "assets" / "pink-home.webp").exists()
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
    assert 'rel="canonical" href="https://www.serviceprofit.com.au/"' in hvac


def test_fees_are_monthly_only():
    banned = ("$19,800", "$31,800", "$42,000", "$6,600", "/ yr", "/ year", "+ GST a year")
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        for token in banned:
            assert token not in text, (p.name, token)


def test_old_trade_urls_redirect_home():
    for slug in ("hvac", "electrical", "construction"):
        text = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
        assert 'url=/index.html' in text
        assert "location.replace" in text
        assert "one offer" in text.lower() or "Continue to Service Profit" in text


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
    assert "hvac.html" not in sm
    assert "electrical.html" not in sm
    assert "construction.html" not in sm


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS", name)
    print("all site tests passed")
