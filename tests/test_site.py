from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = list(ROOT.glob("*.html"))
HOSP = "PinkAccountingTaxSolutionsClientBookings"
FIELD = "g5puGFTA9kmn6ukDa4XssQ2"


def test_no_hospitality_booking():
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        assert HOSP not in text, p.name


def test_book_uses_field_service_calendar():
    text = (ROOT / "book.html").read_text(encoding="utf-8")
    assert FIELD in text
    assert 'href="book.html"' in (ROOT / "index.html").read_text(encoding="utf-8")


def test_privacy_and_terms_on_every_page():
    for p in HTML:
        text = p.read_text(encoding="utf-8")
        assert "privacy.html" in text, p.name
        assert "terms.html" in text, p.name
        assert "og.png" in text, p.name
        assert "Service Profit" in text, p.name


def test_queensland_not_australia_wide_claim():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Australia-wide" not in home
    assert "Queensland" in home
    assert "Brendale" in home
    assert "Brisbane" in home
    assert "areaServed" in home and "Queensland" in home
    assert "Brendale" in (ROOT / "contact.html").read_text(encoding="utf-8")


def test_404_uses_service_profit_name():
    text = (ROOT / "404.html").read_text(encoding="utf-8")
    assert "Service Profit" in text
    assert "Go back to Job Profit" not in text


def test_mobile_pricing_and_a11y_hooks():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "nav.js").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert ".table-scroll" in css
    assert ".scope-cards" in css
    assert "Escape" in js
    assert "aria-pressed" in home
    assert "role=\"tablist\"" not in home
    assert "hvac.html" in home
    assert "assets/hvac.jpg" in home


def test_sitemap_has_trade_pages():
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for slug in ("hvac.html", "electrical.html", "construction.html", "terms.html"):
        assert slug in sm


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS", name)
    print("all site tests passed")
