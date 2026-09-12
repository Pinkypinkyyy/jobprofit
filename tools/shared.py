"""Shared HTML chrome for the Service Profit public site."""

ORIGIN = "https://www.serviceprofit.com.au"
BOOK = "/book.html"
MSBOOK = "https://outlook.office.com/book/ServiceProfit@pinktax.com.au/"
GBP = "https://www.google.com/maps?cid=17544456102082616748"
FB = "https://www.facebook.com/profile.php?id=61594432044788"
LI = "https://www.linkedin.com/company/143802027/"
ASSET = "rt34"
GA4 = "G-8T6SXPNSCW"
GTAG = "GT-WVXQ29L2"
# Firm Meta pixel is not in any live source. Leave blank until Events Manager issues an ID.
META_PIXEL = ""

CSP = (
    "default-src 'self'; "
    "img-src 'self' data: https://www.google-analytics.com https://www.googletagmanager.com "
    "https://www.google.com https://www.google.com.au https://www.facebook.com https://www.facebook.com.au; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "script-src 'self' https://www.googletagmanager.com https://connect.facebook.net; "
    "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com "
    "https://region1.google-analytics.com https://www.facebook.com https://formsubmit.co; "
    "form-action 'self' mailto: https://formsubmit.co; "
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
  <link rel="icon" type="image/png" href="/assets/logo.png">
  <link rel="apple-touch-icon" href="/assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v={ASSET}">
{extra_block}</head>
"""


def jsonld(obj):
    import json
    payload = json.dumps(obj, ensure_ascii=True, separators=(",", ":"))
    return f'  <script type="application/ld+json">\n  {payload}\n  </script>\n'


def business_node():
    return {
        "@context": "https://schema.org",
        "@type": "AccountingService",
        "@id": f"{ORIGIN}/#business",
        "name": "Service Profit",
        "alternateName": "Pink Accounting",
        "url": f"{ORIGIN}/",
        "telephone": "+61735446386",
        "email": "admin@pinktax.com.au",
        "image": f"{ORIGIN}/assets/og.png",
        "logo": f"{ORIGIN}/assets/logo.png",
        "priceRange": "$$",
        "knowsAbout": [
            "HVAC accounting",
            "electrical contractors",
            "construction services",
            "job costing",
            "BAS",
            "GST",
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Shop 15A, 18-22 Kremzow Rd",
            "addressLocality": "Brendale",
            "addressRegion": "QLD",
            "postalCode": "4500",
            "addressCountry": "AU",
        },
        "areaServed": [
            {"@type": "Place", "name": "Brendale"},
            {"@type": "AdministrativeArea", "name": "Moreton Bay"},
            {"@type": "City", "name": "Brisbane"},
            {"@type": "State", "name": "Queensland"},
        ],
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00",
            "closes": "16:30",
        },
        "founder": {"@type": "Person", "name": "Huong Bui"},
        "taxID": "51682301891",
        "identifier": "26284368",
        "sameAs": [FB, LI],
    }


def service_node(name, url, description):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "url": url,
        "description": description,
        "provider": {"@id": f"{ORIGIN}/#business"},
        "areaServed": {"@type": "State", "name": "Queensland"},
        "serviceType": "Accounting",
    }


def faq_node(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }


def local_business_node():
    node = business_node()
    node["@type"] = "AccountingService"
    node["@id"] = f"{ORIGIN}/contact.html#local"
    return node


def nav(current=""):
    def item(href, label, key):
        cur = ' aria-current="page"' if current == key else ""
        return f'        <a href="{href}"{cur}>{label}</a>'

    return f"""<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav" id="pinkNav">
    <div class="wrap">
      <a class="brand" href="/index.html" aria-label="Pink Accounting, Service Profit">
        <img src="/assets/logo-white.png" alt="pink">
        <span class="mark"><span class="offer">Service Profit</span><span class="firm">Pink Accounting</span></span>
      </a>
      <nav class="links" aria-label="Primary">
{item("/pricing.html", "Pricing", "pricing")}
{item("/system.html", "The system", "system")}
{item("/why.html", "Meet Pink", "why")}
{item("/contact.html", "Contact", "contact")}
      </nav>
      <div class="navr">
        <a class="phone" href="tel:+61735446386">(07) 3544 6386</a>
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
          <h4>Explore</h4>
          <a href="/index.html">Home</a>
          <a href="/pricing.html">Pricing</a>
          <a href="/system.html">The system</a>
          <a href="/why.html">Meet Pink</a>
          <a href="/check.html">Hours check</a>
          <a href="/book.html">Book a call</a>
          <a href="/contact.html">Contact</a>
        </div>
        <div>
          <h4>Contact and legal</h4>
          <a href="tel:+61735446386">(07) 3544 6386</a>
          <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a>
          <a href="/contact.html">Contact</a>
          <a href="/rights.html">Your rights</a>
          <a href="/privacy.html">Privacy</a>
          <a href="/terms.html">Terms</a>
          <p class="addr" style="margin-top:12px;line-height:1.8">Shop 15A, 18-22 Kremzow Rd<br>Brendale QLD 4500</p>
        </div>
      </div>
      <p class="legal">© 2026 Pink Accounting &amp; Tax Solutions Pty Ltd. ABN 51 682 301 891. Business clients only. Queensland. Registered Tax Agent No. 26284368 · ASIC Registered Agent No. 52580 · <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB Register</a><br>Liability limited by a scheme approved under Professional Standards Legislation. Claims on this site last reviewed 12 September 2026.</p>
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
        <h3>Quoted 6 hours. Nine on the tools.</h3>
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
        <h3>The bank is not all yours.</h3>
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
    return """      <figure class="chart-fall">
        <p class="chart-kicker">One billed hour</p>
        <p class="chart-note">Worked example, not your rate.</p>
        <svg class="chart-svg light" viewBox="0 0 640 220" role="img" aria-label="Billed 165 dollars including GST. GST 15 dollars. 150 left. Labour 50 dollars. 100 left before parts and overhead.">
          <rect x="0" y="16" width="560" height="28" rx="8" fill="#0E0E12"/>
          <text x="12" y="35" fill="#fff" font-size="13">Billed</text>
          <text x="548" y="35" text-anchor="end" fill="#fff" font-size="16" font-weight="700">$165</text>
          <rect x="0" y="56" width="51" height="28" rx="8" fill="#ED1651"/>
          <text x="12" y="75" fill="#fff" font-size="13">GST</text>
          <text x="200" y="75" fill="#0E0E12" font-size="16" font-weight="700">−$15</text>
          <rect x="0" y="96" width="509" height="28" rx="8" fill="#0E0E12"/>
          <text x="12" y="115" fill="#fff" font-size="13">After GST</text>
          <text x="497" y="115" text-anchor="end" fill="#fff" font-size="16" font-weight="700">$150</text>
          <rect x="0" y="136" width="170" height="28" rx="8" fill="#B45309"/>
          <text x="12" y="155" fill="#fff" font-size="13">Labour, if $50 all-in</text>
          <text x="280" y="155" fill="#0E0E12" font-size="16" font-weight="700">−$50</text>
          <rect x="0" y="176" width="339" height="28" rx="8" fill="#0E0E12"/>
          <text x="12" y="195" fill="#fff" font-size="13">Left before parts and overhead</text>
          <text x="327" y="195" text-anchor="end" fill="#fff" font-size="16" font-weight="700">$100</text>
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
"""


def enquiry_form(prefix="book"):
    return f"""      <form class="enquiry" id="enquiryForm" action="https://formsubmit.co/admin@pinktax.com.au" method="POST" data-event="{prefix}-form">
        <input type="hidden" name="_subject" value="Service Profit intake">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="{ORIGIN}/book.html?sent=1">
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
          <label>What work
            <select name="trade" required>
              <option value="">Choose one</option>
              <option>Air con / refrigeration</option>
              <option>Electrical</option>
              <option>Construction services</option>
              <option>Mix of those</option>
            </select>
          </label>
          <label>People on the tools
            <select name="crew" required>
              <option value="">Choose one</option>
              <option>Just me</option>
              <option>2 to 5</option>
              <option>6 to 15</option>
              <option>16 or more</option>
            </select>
          </label>
          <label>Books now
            <select name="software" required>
              <option value="">Choose one</option>
              <option>Xero</option>
              <option>MYOB</option>
              <option>Excel or paper</option>
              <option>Something else</option>
              <option>Nothing yet</option>
            </select>
          </label>
          <label>What is hurting
            <select name="hurt" required>
              <option value="">Choose one</option>
              <option>Quoted hours vs hours on the job</option>
              <option>Bank looks full but tax is due</option>
              <option>BAS / ATO</option>
              <option>Hiring and not sure we can afford it</option>
              <option>Not sure. That is why I am calling</option>
            </select>
          </label>
        </div>
        <label>Anything else we should know
          <textarea name="message" rows="4" maxlength="2000" placeholder="How you quote. Whether jobs run long. What you want from the file."></textarea>
        </label>
        <button class="btn btn-primary" type="submit">Send this, then pick a time</button>
        <p class="form-note">Goes to admin@pinktax.com.au. We read it before the call. By sending you agree to our <a href="/terms.html">terms</a> and <a href="/privacy.html">privacy</a> pages.</p>
      </form>
      <p class="enquiry-ok" id="enquiryOk" hidden>Got it. Pick a time below with the same email so we are not chasing you.</p>
"""
