"""Shared HTML chrome for the Service Profit public site."""

import json
import pathlib

# HB 24 Sep 2026: every business fact comes from identity.json, generated from
# the firm's canonical file. Never hardcode the name, address, phone or hours.
ID = json.loads((pathlib.Path(__file__).resolve().parents[1] / "identity.json").read_text(encoding="utf-8"))

ORIGIN = "https://www.serviceprofit.com.au"
BOOK = "/book.html"
MSBOOK = "https://outlook.office.com/book/ServiceProfit@pinktax.com.au/"
GBP = ID["google_profile"]["maps_url"]
FB = "https://www.facebook.com/profile.php?id=61594432044788"
LI = "https://www.linkedin.com/company/143802027/"
ASSET = "rt47"
IMG_VERSION = "real2"


def image_widths(stem):
    """Widths we actually hold for this photo, smallest first.

    The source photos top out at 838px wide. The build used to emit 864 and
    1200 variants from them, so the browser downloaded a third more bytes for
    pixels that had been invented by the resampler. Read what is on disk
    instead of asserting a ladder that may not exist.
    """
    import pathlib as _p
    import re as _re
    assets = _p.Path(__file__).resolve().parents[1] / "assets"
    found = []
    for f in assets.glob(f"{stem}-*.webp"):
        m = _re.fullmatch(rf"{_re.escape(stem)}-(\d+)\.webp", f.name)
        if m:
            found.append(int(m.group(1)))
    return sorted(found)


def webp_srcset(stem):
    return ", ".join(
        f"/assets/{stem}-{w}.webp?v={IMG_VERSION} {w}w" for w in image_widths(stem)
    )
GA4 = "G-8T6SXPNSCW"
GTAG = "GT-WVXQ29L2"
# Firm Meta pixel is not in any live source. Leave blank until Events Manager issues an ID.
META_PIXEL = ""

# Where the enquiry forms post. Changing these three lines is the whole job of
# moving off the third-party US relay onto a first-party endpoint (a Power
# Automate "when an HTTP request is received" flow inside the Pink tenant, for
# example). The CSP, both form actions and the ajax path in nav.js all derive
# from here, so nothing is left pointing at the old host.
FORM_ORIGIN = "https://formsubmit.co"
FORM_ENDPOINT = f"{FORM_ORIGIN}/admin@pinktax.com.au"
FORM_AJAX_ENDPOINT = f"{FORM_ORIGIN}/ajax/admin@pinktax.com.au"

CSP = (
    "default-src 'self'; "
    "img-src 'self' data: https://*.google-analytics.com https://analytics.google.com "
    "https://www.googletagmanager.com https://stats.g.doubleclick.net "
    "https://www.google.com https://www.google.com.au https://www.facebook.com https://www.facebook.com.au; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "script-src 'self' https://www.googletagmanager.com https://connect.facebook.net; "
    "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
    "https://analytics.google.com https://www.googletagmanager.com "
    "https://stats.g.doubleclick.net https://www.google.com https://www.google.com.au "
    "https://www.facebook.com " + FORM_ORIGIN + "; "
    "form-action 'self' mailto: " + FORM_ORIGIN + "; "
    "media-src 'self'; "
    "base-uri 'self'"
)


def head(title, description, canonical, og_image="/assets/og.png", extra=""):
    if not canonical.startswith("http"):
        canonical = ORIGIN + (canonical if canonical.startswith("/") else "/" + canonical)
    og = ORIGIN + og_image if og_image.startswith("/") else og_image
    extra_block = extra if extra else ""
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:site_name" content="Service Profit">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_AU">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{og}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400..800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v={ASSET}">
{extra_block}</head>
"""


def jsonld(obj):
    import json
    payload = json.dumps(obj, ensure_ascii=True, separators=(",", ":"))
    return f'  <script type="application/ld+json">\n  {payload}\n  </script>\n'


def business_node():
    """The one firm. Same @id as pinktax.com.au, so Google sees one business
    with two service lines, not two businesses at Shop 15A."""
    o = ID["office"]
    return {
        "@context": "https://schema.org",
        "@type": ID["schema"]["type"],
        "@id": ID["schema"]["organization_id"],
        "name": ID["public_name"],
        "legalName": ID["legal"]["entity"],
        "url": ID["service_lines"]["hospitality"]["site"],
        "telephone": o["phone_e164"],
        "email": o["email"],
        "logo": f"{ORIGIN}/assets/logo.png",
        "image": f"{ORIGIN}/assets/og.png",
        "address": postal_address(),
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": o["hours"]["days"],
            "opens": o["hours"]["opens"],
            "closes": o["hours"]["closes"],
        },
        "founder": {"@type": "Person", "name": "Huong Bui"},
        "taxID": ID["legal"]["abn"].replace(" ", ""),
        "identifier": ID["legal"]["tax_agent_number"],
        "sameAs": [GBP],
        "department": [service_profit_node()],
    }


def postal_address():
    o = ID["office"]
    return {
        "@type": "PostalAddress",
        "streetAddress": o["street"],
        "addressLocality": o["locality"],
        "addressRegion": o["region"],
        "postalCode": o["postcode"],
        "addressCountry": o["country"],
    }


def service_profit_node():
    """The trades service line. Deliberately no address or phone of its own:
    it is a department of the firm, not a second business."""
    return {
        "@type": "AccountingService",
        "@id": f"{ORIGIN}/#service-profit",
        "name": ID["service_lines"]["trades"]["service_name"],
        "url": f"{ORIGIN}/",
        "parentOrganization": {"@id": ID["schema"]["organization_id"]},
        "priceRange": "$$",
        "sameAs": [FB, LI],
        "knowsAbout": [
            "HVAC accounting",
            "air conditioning accountant",
            "electrical contractors",
            "electrician accountant",
            "construction services",
            "job costing",
            "quoted hours versus actual hours",
            "BAS",
            "GST",
            "tax agent services",
            "tax planning",
            "bookkeeping",
            "Xero setup",
            "payroll",
            "Single Touch Payroll",
            "business advisory",
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Service Profit plans",
            "itemListElement": [
                {"@type": "Offer", "name": "Job Profit", "price": "1650.00", "priceCurrency": "AUD", "url": f"{ORIGIN}/pricing.html#level-job"},
                {"@type": "Offer", "name": "Weekly Visibility", "price": "2650.00", "priceCurrency": "AUD", "url": f"{ORIGIN}/pricing.html#level-weekly"},
                {"@type": "Offer", "name": "Ready to Scale", "price": "3500.00", "priceCurrency": "AUD", "url": f"{ORIGIN}/pricing.html#level-scale"},
                {"@type": "Offer", "name": "Compliance", "price": "550.00", "priceCurrency": "AUD", "url": f"{ORIGIN}/pricing.html#level-compliance"},
            ],
        },
        "areaServed": [
            {"@type": "Place", "name": "Brendale"},
            {"@type": "AdministrativeArea", "name": "Moreton Bay"},
            {"@type": "City", "name": "Brisbane"},
            {"@type": "State", "name": "Queensland"},
        ],
    }


def service_node(name, url, description):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "url": url,
        "description": description,
        # Named inline: the #business node is only on the home page.
        "provider": {"@type": "AccountingService", "@id": ID["schema"]["organization_id"], "name": ID["public_name"], "telephone": ID["office"]["phone_e164"], "address": postal_address()},
        "areaServed": {"@type": "State", "name": "Queensland"},
        "serviceType": "Accounting",
    }


def faq_node(pairs):
    import html
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)},
            }
            for q, a in pairs
        ],
    }


def local_business_node():
    # One business, one @id. A second id here read as a second business.
    return business_node()


def website_node():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Service Profit",
        "url": f"{ORIGIN}/",
        "publisher": {"@id": ID["schema"]["organization_id"]},
        "inLanguage": "en-AU",
    }


def person_node():
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Huong Bui",
        "alternateName": "Pink",
        "jobTitle": "Registered Tax Agent",
        "worksFor": {"@id": ID["schema"]["organization_id"]},
        "alumniOf": "Griffith University",
        "identifier": "26284368",
        "url": f"{ORIGIN}/why.html",
    }


# HB 24 Sep 2026: every service one click away from any page.
SERVICE_MENU = (
    ("/services/", "All services", "Everything we do for trade businesses"),
    ("/tax-agent-for-trades/", "Tax agent and tax planning", "Returns, planning before 30 June, FBT, TPAR"),
    ("/bas-and-gst-for-trades/", "BAS and GST", "Lodged by a registered tax agent"),
    ("/bookkeeping-and-xero-for-trades/", "Bookkeeping and Xero setup", "Bank reconciled, job software feeding Xero"),
    ("/payroll-for-trades/", "Payroll and super", "Pay runs, Single Touch Payroll, Payday Super"),
    ("/system.html", "Job profit and advisory", "Quoted hours against hours on the tools, every Monday"),
)


def trust_line():
    """HB 24 Sep 2026: who we are, the price and the registration, under every hero button."""
    return (
        '      <p class="trust-line">Accountants, bookkeepers and tax agents. From $550 + GST a month; '
        f'most trade files $1,650. Registered tax agent {ID["legal"]["tax_agent_number"]}, Brendale.</p>'
    )


def services_dropdown(current=""):
    cur = ' aria-current="page"' if current == "services" else ""
    items = "\n".join(
        f'            <a href="{href}"><b>{label}</b><span>{note}</span></a>' for href, label, note in SERVICE_MENU
    )
    return f"""        <div class="navdrop">
          <a class="navdrop-top" href="/services/"{cur}>Services</a>
          <button class="navdrop-toggle" type="button" aria-expanded="false" aria-controls="svcMenu" aria-label="Show all services"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
          <div class="navdrop-menu" id="svcMenu">
{items}
          </div>
        </div>"""


def nav(current=""):
    def item(href, label, key):
        cur = ' aria-current="page"' if current == key else ""
        return f'        <a href="{href}"{cur}>{label}</a>'

    return f"""<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav" id="pinkNav">
    <div class="wrap">
      <a class="brand" href="/index.html" aria-label="Service Profit Pink Accounting">
        <img src="/assets/logo-white.png" alt="">
        <span class="mark"><span class="offer">Service Profit</span><span class="firm">Pink Accounting</span></span>
      </a>
      <nav class="links" aria-label="Primary">
{services_dropdown(current)}
{item("/pricing.html", "Pricing", "pricing")}
{item("/system.html", "The system", "system")}
{item("/why.html", "Meet Pink", "why")}
{item("/contact.html", "Contact", "contact")}
      </nav>
      <div class="navr">
        <a class="phone" href="tel:{ID["office"]["phone_e164"]}">{ID["office"]["phone_display"]}</a>
        <a class="call-icon" href="tel:{ID["office"]["phone_e164"]}" aria-label="Call {ID["office"]["phone_display"]}" data-event="nav-call"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z" fill="currentColor"/></svg></a>
        <a class="btn btn-primary" href="/book.html" data-event="nav-book"><span class="full">Book a call</span><span class="short">Book</span></a>
        <button class="burger" id="pinkBurger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="pinkNav"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>
"""


def footer():
    return f"""  <footer class="foot">
    <div class="wrap">
      <div class="grid">
        <div>
          <img src="/assets/logo-white.png" alt="pink">
          <p class="blurb">Service Profit is Pink Accounting’s line for HVAC, electrical and construction service businesses. Brendale. Brisbane. Queensland. Registered Tax Agent 26284368.</p>
        </div>
        <div>
          <h2>Explore</h2>
          <a href="/index.html">Home</a>
          <a href="/services/">Services</a>
          <a href="/pricing.html">Pricing</a>
          <a href="/system.html">The system</a>
          <a href="/why.html">Meet Pink</a>
          <a href="/check.html">Hours check</a>
          <a href="/accountant-brendale/">Accountant in Brendale</a>
          <a href="/air-conditioning-accountant-brisbane/">Air con accountant</a>
          <a href="/electrician-accountant-brisbane/">Electrician accountant</a>
          <a href="/construction-services-accountant-brisbane/">Construction services</a>
          <a href="/quoted-hours-vs-actual-hours/">Quoted vs actual hours</a>
          <a href="/cash-that-is-yours/">Cash that is yours</a>
          <a href="/can-i-afford-another-technician/">Another technician</a>
          <a href="/book.html">Book a call</a>
          <a href="/contact.html">Contact</a>
        </div>
        <div>
          <h2>Contact and legal</h2>
          <a href="tel:+61735446386">(07) 3544 6386</a>
          <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a>
          <a href="/contact.html">Contact</a>
          <a href="/rights.html">Your rights</a>
          <a href="/privacy.html">Privacy</a>
          <a href="/terms.html">Terms</a>
          <p class="addr" style="margin-top:12px;line-height:1.8">{ID["office"]["street"]}<br>{ID["office"]["locality"]} {ID["office"]["region"]} {ID["office"]["postcode"]}</p>
        </div>
      </div>
      <p class="sister-line" data-identity="cross-link">{ID["cross_links"]["on_trades_site"]["text"]} <a href="{ID["cross_links"]["on_trades_site"]["href"]}">{ID["cross_links"]["on_trades_site"]["link_text"]}</a>.</p>
      <p class="legal">© 2026 Pink Accounting &amp; Tax Solutions Pty Ltd. ABN 51 682 301 891. Business clients only. Queensland. Registered Tax Agent No. 26284368 · ASIC Registered Agent No. 52580 · <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB Register</a><br>Liability limited by a scheme approved under Professional Standards Legislation. Claims on this site last reviewed 13 September 2026.</p>
    </div>
  </footer>
  <script src="/track.js?v={ASSET}"></script>
  <script src="/nav.js?v={ASSET}"></script>
</body>
</html>
"""


def hours_chart():
    return """      <figure class="chart-hours">
        <p class="chart-kicker">One job</p>
        <h2>Quoted 6 hours. Nine on the tools.</h2>
        <p class="chart-note">Worked example, not a client result.</p>
        <svg class="chart-svg" viewBox="0 0 560 176" role="img" aria-label="Quoted 6 hours. Nine hours on the tools. Three hours unbilled.">
          <text x="0" y="18" fill="currentColor" font-size="12">Quoted</text>
          <text x="560" y="18" text-anchor="end" fill="currentColor" font-size="18" font-weight="700">6 h</text>
          <rect x="0" y="26" width="560" height="12" rx="6" fill="rgba(255,255,255,.12)"/>
          <rect x="0" y="26" width="373" height="12" rx="6" fill="#fff"/>
          <text x="0" y="70" fill="currentColor" font-size="12">On the tools</text>
          <text x="560" y="70" text-anchor="end" fill="currentColor" font-size="18" font-weight="700">9 h</text>
          <rect x="0" y="78" width="560" height="12" rx="6" fill="#fff"/>
          <text x="0" y="122" fill="currentColor" font-size="12">Unbilled</text>
          <text x="560" y="122" text-anchor="end" fill="#ED1651" font-size="18" font-weight="700">3 h</text>
          <rect x="0" y="130" width="560" height="12" rx="6" fill="rgba(255,255,255,.12)"/>
          <rect x="0" y="130" width="187" height="12" rx="6" fill="#ED1651"/>
        </svg>
        <p class="chart-foot">Those 3 hours never went into the next quote.</p>
      </figure>
"""


def cash_chart():
    return """      <figure class="chart-cash">
        <p class="chart-kicker">Cash</p>
        <h2>The bank is not all yours.</h2>
        <p class="chart-note">GST, PAYG, super and wages sit in there. You cannot spend that. This bar is an illustration, not a client file.</p>
        <div class="cash-bar" role="img" aria-label="Illustration. GST, PAYG, super, wages and what is yours sit in the same bank balance.">
          <span class="seg">GST</span>
          <span class="seg">PAYG</span>
          <span class="seg">Super</span>
          <span class="seg">Wages</span>
          <span class="seg yours">Yours</span>
        </div>
      </figure>
"""


def hour_waterfall():
    # 360 wide so the labels stay readable on a phone (the old 640 wide chart
    # shrank its text to about 6px). Labels sit above each bar.
    rows = (
        ("Billed", "$165", 330, "#0E0E12", True),
        ("GST", "−$15", 30, "#ED1651", False),
        ("After GST", "$150", 300, "#0E0E12", True),
        ("Labour, if $50 all-in", "−$50", 100, "#5A5A60", False),
        ("Left before parts and overhead", "$100", 200, "#0E0E12", True),
    )
    parts = []
    for i, (label, value, width, colour, inside) in enumerate(rows):
        y = i * 48
        parts.append(f'          <text x="0" y="{y + 14}" fill="#0E0E12" font-size="14">{label}</text>')
        parts.append(f'          <rect x="0" y="{y + 20}" width="{width}" height="22" rx="6" fill="{colour}"/>')
        if inside:
            parts.append(f'          <text x="{width - 8}" y="{y + 36}" text-anchor="end" fill="#fff" font-size="15" font-weight="700">{value}</text>')
        else:
            parts.append(f'          <text x="{width + 8}" y="{y + 36}" fill="#0E0E12" font-size="15" font-weight="700">{value}</text>')
    bars = "\n".join(parts)
    return f"""      <figure class="chart-fall">
        <p class="chart-kicker">One billed hour</p>
        <p class="chart-note">Worked example, not your rate.</p>
        <svg class="chart-svg light" viewBox="0 0 360 240" role="img" aria-label="Billed 165 dollars including GST. GST 15 dollars. 150 left. Labour 50 dollars. 100 left before parts and overhead.">
{bars}
        </svg>
        <p class="chart-foot">Then parts. Then overhead. Then profit, if the billed hours actually landed.</p>
      </figure>
"""


def sticky():
    return """  <div class="sticky-book" id="bookBar">
    <span>Book 15 minutes. See if we can take the file.</span>
    <a class="btn btn-primary" href="/book.html" data-event="sticky-book">Book a call</a>
  </div>
"""


def hours_check():
    return """      <form class="hours-check" id="hoursCheck">
        <div class="fields">
          <label>Hours you quoted
            <input type="number" name="quoted" min="0.5" step="0.5" required inputmode="decimal">
          </label>
          <label>Hours on the tools
            <input type="number" name="tools" min="0.5" step="0.5" required inputmode="decimal">
          </label>
          <label>Rate you billed, ex GST
            <input type="number" name="rate" min="1" step="1" value="150" required inputmode="decimal">
          </label>
        </div>
        <button class="btn btn-primary" type="submit">Show the gap</button>
      </form>
      <div class="hours-result" id="hoursResult" hidden>
        <p id="hoursResultLine"></p>
        <p class="chart-note">Sketch from the numbers you typed. Not your file. Not a promise.</p>
        <a class="btn btn-primary" href="/book.html" data-event="check-book">Book 15 minutes</a>
      </div>
      <form class="hours-check" id="crewCheck">
        <p class="crew-kicker">Or the whole crew, for a week</p>
        <div class="fields">
          <label>People on the tools
            <input type="number" name="techs" min="1" step="1" value="4" required inputmode="numeric">
          </label>
          <label>Unbilled hours each, a week
            <input type="number" name="leak" min="0" step="0.5" value="3" required inputmode="decimal">
          </label>
          <label>Rate billed, ex GST
            <input type="number" name="rate" min="1" step="1" value="145" required inputmode="decimal">
          </label>
        </div>
        <button class="btn btn-primary" type="submit">Show the year</button>
      </form>
      <div class="hours-result" id="crewResult" hidden>
        <p id="crewResultLine"></p>
        <p class="chart-note">Sketch from the numbers you typed. Not your file. Not a promise. Fifty-two weeks is the year. Real weeks are not all billable.</p>
        <a class="btn btn-primary" href="/book.html" data-event="crew-book">Book 15 minutes</a>
      </div>
"""


def short_enquiry_form(prefix="contact", next_page="/contact.html"):
    return f"""      <form class="enquiry" id="enquiryForm" action="{FORM_ENDPOINT}" method="POST" data-ajax="{FORM_AJAX_ENDPOINT}" data-event="{prefix}-form">
        <input type="hidden" name="_subject" value="Service Profit enquiry">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="true">
        <input type="hidden" name="_next" value="{ORIGIN}{next_page}?sent=1">
        <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="fields">
          <label>Your name
            <input type="text" name="name" required autocomplete="name">
          </label>
          <label>Business name
            <input type="text" name="business" required autocomplete="organization">
          </label>
          <label>Email
            <input type="email" name="email" required autocomplete="email">
          </label>
          <label>Phone
            <input type="tel" name="phone" required autocomplete="tel">
          </label>
        </div>
        <label>What work
          <select name="trade" required>
            <option value="">Choose one</option>
            <option>Air con / refrigeration</option>
            <option>Electrical</option>
            <option>Construction services</option>
            <option>Mix of those</option>
          </select>
        </label>
        <label>What do you need
          <textarea class="short" name="message" rows="4" maxlength="1000" required placeholder="What is going on with the books, the BAS or the job costs. A sentence or two is enough."></textarea>
        </label>
        <button class="btn btn-primary" type="submit">Send this</button>
        <p class="form-note">Goes to admin@pinktax.com.au. A person reads it. Please do not send your TFN or bank details through this form. By sending you agree to our <a href="/terms.html">terms</a> and <a href="/privacy.html">privacy</a> pages.</p>
      </form>
      <p class="enquiry-ok" id="enquiryOk" hidden>Got it. We will come back to you the same working day.</p>
"""


def enquiry_form(prefix="book", short=False, next_page="/book.html"):
    if short:
        return short_enquiry_form(prefix, next_page)
    return f"""      <form class="enquiry" id="enquiryForm" action="{FORM_ENDPOINT}" method="POST" data-ajax="{FORM_AJAX_ENDPOINT}" data-event="{prefix}-form">
        <input type="hidden" name="_subject" value="Service Profit intake">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="true">
        <input type="hidden" name="_next" value="{ORIGIN}{next_page}?sent=1">
        <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="fields">
          <label>Your name
            <input type="text" name="name" required autocomplete="name">
          </label>
          <label>Business name <span class="opt">optional</span>
            <input type="text" name="business" autocomplete="organization">
          </label>
          <label>Email
            <input type="email" name="email" required autocomplete="email">
          </label>
          <label>Phone <span class="opt">optional</span>
            <input type="tel" name="phone" autocomplete="tel">
          </label>
          <label>What work <span class="opt">optional</span>
            <select name="trade">
              <option value="">Choose one</option>
              <option>Air con / refrigeration</option>
              <option>Electrical</option>
              <option>Construction services</option>
              <option>Mix of those</option>
            </select>
          </label>
          <label>Annual revenue <span class="opt">optional</span>
            <select name="revenue">
              <option value="">Choose one</option>
              <option>Under $1M</option>
              <option>$1M-$3M</option>
              <option>$3M-$5M</option>
              <option>$5M+</option>
            </select>
          </label>
          <label>Staff <span class="opt">optional</span>
            <select name="staff">
              <option value="">Choose one</option>
              <option>Just me</option>
              <option>2 to 5</option>
              <option>6 to 15</option>
              <option>16 or more</option>
            </select>
          </label>
        </div>
        <label>What is hurting <span class="opt">optional</span>
          <textarea class="short" name="hurt" rows="4" maxlength="1000" placeholder="Jobs running long. Bank looks full but tax is due. BAS. Hiring and not sure you can afford it."></textarea>
        </label>
        <label>Where is the business now <span class="opt">optional</span>
          <textarea class="short" name="position" rows="3" maxlength="1000" placeholder="Quoted hours vs real hours. Bank. BAS. Who does the books. What the file looks like today."></textarea>
        </label>
        <label>Where do you want it in 12 months <span class="opt">optional</span>
          <textarea class="short" name="vision" rows="3" maxlength="1000" placeholder="More billed hours. A crew you can afford. Cash that is yours after tax. Off the tools, or still on them."></textarea>
        </label>
        <button class="btn btn-primary" type="submit">Send this before the call</button>
        <p class="form-note">Goes to admin@pinktax.com.au. We read it before the call. By sending you agree to our <a href="/terms.html">terms</a> and <a href="/privacy.html">privacy</a> pages.</p>
      </form>
      <p class="enquiry-ok" id="enquiryOk" hidden>Got it. We read this before your call.</p>
"""
