"""Shared HTML chrome for the Service Profit public site."""

ORIGIN = "https://www.serviceprofit.com.au"
BOOK = "book.html"
MSBOOK = "https://outlook.office.com/book/booking@pinktax.com.au/s/g5puGFTA9kmn6ukDa4XssQ2"
GBP = "https://www.google.com/maps?cid=17544456102082616748"
ASSET = "rt18"


def head(title, description, canonical, og_image="/assets/og.png"):
    if not canonical.startswith("http"):
        canonical = ORIGIN + (canonical if canonical.startswith("/") else "/" + canonical)
    og = ORIGIN + og_image if og_image.startswith("/") else og_image
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
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self'; base-uri 'self'; form-action 'self' mailto:">
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
  <link rel="icon" href="assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ASSET}">
</head>
"""


def nav(current=""):
    def item(href, label, key):
        cur = ' aria-current="page"' if current == key else ""
        return f'        <a href="{href}"{cur}>{label}</a>'

    return f"""<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav" id="pinkNav">
    <div class="wrap">
      <a class="brand" href="index.html" aria-label="Service Profit, accounting firm">
        <img src="assets/logo.png" alt="">
        <span class="mark"><span class="offer">Service Profit</span><span class="firm">Accounting firm</span></span>
      </a>
      <nav class="links" aria-label="Primary">
{item("system.html", "The system", "system")}
{item("index.html#pricing", "Pricing", "pricing")}
{item("why.html", "Meet Pink", "why")}
{item("book.html", "Book a call", "book")}
{item("contact.html", "Contact", "contact")}
      </nav>
      <div class="navr">
        <a class="phone" href="tel:+61735446386">(07) 3544 6386</a>
        <a class="btn btn-primary" href="book.html" data-event="nav-book"><span class="full">Book a call</span><span class="short">Book</span></a>
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
          <img src="assets/logo-white.png" alt="Service Profit">
          <p class="blurb">Service Profit is an accounting firm for HVAC, electrical and construction service businesses. Brendale. Brisbane. Queensland. Registered Tax Agent 26284368.</p>
        </div>
        <div>
          <h4>Explore</h4>
          <a href="index.html">Home</a>
          <a href="system.html">The system</a>
          <a href="index.html#pricing">Pricing</a>
          <a href="hvac.html">HVAC</a>
          <a href="electrical.html">Electrical</a>
          <a href="construction.html">Construction services</a>
          <a href="why.html">Meet Pink</a>
          <a href="book.html">Book a call</a>
        </div>
        <div>
          <h4>Contact and legal</h4>
          <a href="tel:+61735446386">(07) 3544 6386</a>
          <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a>
          <a href="contact.html">Contact</a>
          <a href="rights.html">Your rights</a>
          <a href="privacy.html">Privacy</a>
          <a href="terms.html">Terms</a>
          <p class="addr" style="margin-top:12px;line-height:1.8">Shop 15A, 18-22 Kremzow Rd<br>Brendale QLD 4500</p>
        </div>
      </div>
      <p class="legal">© 2026 Pink Accounting &amp; Tax Solutions Pty Ltd. ABN 51 682 301 891. Business clients only. Queensland. Registered Tax Agent No. 26284368 · ASIC Registered Agent No. 52580 · <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB Register</a><br>Liability limited by a scheme approved under Professional Standards Legislation. Claims on this site last reviewed 10 September 2026.</p>
    </div>
  </footer>
  <script src="nav.js?v={ASSET}"></script>
</body>
</html>
"""


def sticky():
    return """  <div class="sticky-book" id="bookBar">
    <span>Fifteen minutes with the firm.</span>
    <a class="btn btn-primary" href="book.html" data-event="sticky-book">Book a call</a>
  </div>
"""
