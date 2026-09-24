import json
from pathlib import Path
from shared import (
    GBP,
    IMG_VERSION,
    MSBOOK,
    ORIGIN,
    cash_chart,
    enquiry_form,
    hours_check,
    faq_node,
    footer,
    head,
    hour_waterfall,
    hours_chart,
    jsonld,
    business_node,
    ID,
    trust_line,
    local_business_node,
    nav,
    person_node,
    service_node,
    sticky,
    webp_srcset,
    website_node,
)
import seo_pages

ROOT = Path(__file__).resolve().parents[1]

# Fallback figures, used only when data/google_reviews.json is absent, which is
# the case before the first scheduled fetch runs or if the Places API is down.
# tools/fetch_reviews.py is what normally supplies these.
FALLBACK_RATING = "5.0"
FALLBACK_COUNT = 32
FALLBACK_AS_AT = "September 2026"
FALLBACK_QUOTES = [
    ("I\u2019ve had a fantastic experience working with Pinky. She is professional, knowledgeable, "
     "and always takes the time to explain things clearly. As a small business owner, I really "
     "appreciate her patience, attention to detail, and prompt responses.", "T D", ""),
    ("Huong is super knowledgeable and keeps your books tidy and taxes up to date. She explains "
     "things clearly so you actually understand your tax, not just the numbers.", "N T", ""),
    ("Pink is amazing \u2014 super quick, really knows her stuff, and an absolute gem for any "
     "business. She makes everything easy.", "N M", ""),
]

MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def load_reviews(path=None):
    """Live Google data if the scheduled fetch has written it, else the
    committed fallback. Never let a bad file take the site down."""
    path = path or ROOT / "data" / "google_reviews.json"
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        rating = d["rating"]
        count = int(d["count"])
        y, m, _ = (d.get("fetched") or "").split("-")
        as_at = f"{MONTHS[int(m) - 1]} {y}"
        quotes = [
            (r["text"], r.get("author") or "Google reviewer", r.get("uri") or d.get("maps_uri", ""))
            for r in d.get("reviews", [])
            if r.get("text") and (r.get("rating") or 0) >= 4
        ][:3]
        if not quotes:
            quotes = FALLBACK_QUOTES
        rating = f"{float(rating):.1f}"
        return rating, count, as_at, quotes, d.get("maps_uri") or GBP
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return FALLBACK_RATING, FALLBACK_COUNT, FALLBACK_AS_AT, FALLBACK_QUOTES, GBP


REVIEWS_RATING, REVIEWS_COUNT, REVIEWS_AS_AT, REVIEWS_QUOTES, REVIEWS_URL = load_reviews()


def write(name, html):
    path = ROOT / name
    path.write_text(html, encoding="utf-8")
    print("wrote", name, path.stat().st_size)


SYSTEM_FAQ = [
    (
        "What happens in the first month?",
        "You give Xero, bank and payroll access, or send the source documents. We confirm the start date in the letter. Catch-up of earlier periods is a separate fee, quoted first.",
    ),
    (
        "Do you tell me whether to hire staff or a contractor?",
        "We show the cost of each in the file. The employment decision is yours. If someone works like staff, that is a compliance issue as well as a cost issue.",
    ),
    (
        "How do I cancel?",
        "The letter of engagement sets the term and how to end it.",
    ),
]

PRICING_FAQ = [
    (
        "What is in Job Profit?",
        "Billed hours versus quoted hours each week, cash that is yours versus GST, PAYG, super and wages, FBT watched in the file, and income tax, FBT, financial statements, BAS and GST held for one trading entity as written in the letter.",
    ),
    (
        "What is not included?",
        "A monthly meeting, unlimited work (ask us anything; bigger jobs are quoted first), catch-up of earlier periods, a published savings figure, and extra entities unless the letter says so. Xero subscription is yours.",
    ),
    (
        "Do the higher plans include Job Profit?",
        "Weekly Visibility includes Job Profit. Ready to Scale includes Weekly Visibility. Compliance does not include the job-and-cash look.",
    ),
    (
        "Is bookkeeping a plan?",
        "No. It is an add-on from $500 + GST a month, quoted when it is actually needed. It does not include the weekly job-and-cash look.",
    ),
    (
        "My bookkeeper charges $300 a month. Why is this five times that?",
        "Because it is not the same job. A bookkeeper records what already happened. This tells you, each week, whether the hours you quoted matched the hours you paid for, and how much of the bank is actually yours once GST, PAYG, super and wages come out. It also carries the tax agent work: income tax, FBT, financial statements, BAS and GST. If what you need is the recording, keep your bookkeeper. Bookkeeping is an add-on here from $500 + GST a month and we will say so.",
    ),
    (
        "What happens if it does not pay for itself?",
        "Then it is the wrong plan and you should not be on it. The fee is worth it if a job that ran long gets caught before the next quote repeats it. If your jobs already land on quote and you know what is yours in the bank, you do not need Job Profit. Compliance at $550 + GST a month does the returns and the BAS, and that is an honest answer on the call.",
    ),
    (
        "Are the fees plus GST?",
        "Yes. Published fees are monthly, exclusive of GST, for one trading entity unless the letter says otherwise.",
    ),
    (
        "How do I start?",
        "Send the enquiry on the book page or call. A booked call is a conversation to see whether there is a fit. It is not an engagement until the letter is issued.",
    ),
]


# Real pixel sizes of assets/<stem>.jpg. A wrong height here reserves the wrong
# box and the page shifts when the image lands.
STEM_SIZE = {
    "hvac": (838, 1059),
    "electrical": (838, 1059),
    "construction": (838, 1036),
    "tech-hvac": (838, 1059),
    "tech-electrical": (838, 1059),
    "pink-home": (1200, 1800),
    "pink-meet": (1080, 1350),
}


# The weekly output sample. A permanent worked example, not a placeholder
# waiting on real data: it stays invented even once there are clients, and the
# page says so. Do not put a real client's figures, job numbers or trading name
# in here, anonymised or otherwise. The figures must still reconcile, because
# an accountant showing numbers that do not add up is worse than showing none,
# and the arithmetic test reads from this block to enforce that.
WEEKLY_SAMPLE = {
    "week_ending": "5 September",
    "jobs_closed": 14,
    "hours_quoted": 96,
    "hours_actual": 112,
    "jobs": [
        ("Rooftop changeover", 8, 15),
        ("Switchboard upgrade", 6, 9),
    ],
    "bank": 84200,
    "holdbacks": [
        ("GST held", 11400),
        ("PAYG and super", 9860),
        ("Wages to Thursday", 18300),
    ],
    "decision": (
        "Third rooftop changeover this quarter to run over. The quote template "
        "does not carry crane time. Worth a ten-minute fix before the next one "
        "goes out."
    ),
}


def weekly_yours():
    return WEEKLY_SAMPLE["bank"] - sum(v for _, v in WEEKLY_SAMPLE["holdbacks"])


def weekly_sample():
    """What actually lands in the inbox. The site sold the idea of the weekly
    look without ever showing the thing, which is the one artefact a buyer at
    this fee wants to see. Every figure comes from WEEKLY_SAMPLE."""
    w = WEEKLY_SAMPLE
    over = w["hours_actual"] - w["hours_quoted"]
    jobs = "\n".join(
        f'              <li><span>{name}</span><b>quoted {q}, took {a}</b></li>'
        for name, q, a in w["jobs"]
    )
    holds = "\n".join(
        f'              <li><span>{name}</span><b>${amount:,}</b></li>'
        for name, amount in w["holdbacks"]
    )
    return f"""        <div class="wsample">
          <div class="wsample-head">
            <span class="label">Monday 9:00 &middot; week ending {w["week_ending"]}</span>
            <span class="label">Job Profit &middot; weekly</span>
          </div>
          <div class="wsample-body">
            <h3>Quoted {w["hours_quoted"]} hours. On the tools {w["hours_actual"]}.</h3>
            <p class="wsample-sub">{w["jobs_closed"]} jobs closed. {over} hours over. Two jobs did most of it.</p>
            <ul class="wsample-list">
{jobs}
              <li><span>Everything else</span><b>within an hour of quote</b></li>
            </ul>
            <h3>In the bank ${w["bank"]:,}. Yours ${weekly_yours():,}.</h3>
            <ul class="wsample-list">
{holds}
              <li class="is-you"><span>Yours to spend</span><b>${weekly_yours():,}</b></li>
            </ul>
            <h3>One thing needs you</h3>
            <p class="wsample-sub">{w["decision"]}</p>
          </div>
        </div>
        <p class="note-ex">Illustration of the weekly output. Invented figures, not a client file. Your first one uses your jobs and your bank.</p>"""


def review_quotes():
    """Google requires the author and a link back to the review. Both are
    carried here whenever the live fetch supplied them."""
    import html as _html
    out = ['        <div class="quotes">']
    for text, author, uri in REVIEWS_QUOTES:
        cite = _html.escape(author)
        if uri:
            cite = f'<a href="{_html.escape(uri)}" rel="noopener nofollow">{cite}</a>'
        out.append("          <blockquote>")
        out.append(f"            <p>{_html.escape(text)}</p>")
        out.append(f"            <footer>{cite} \u00b7 Google</footer>")
        out.append("          </blockquote>")
    out.append("        </div>")
    return "\n".join(out)


# Section 45 of the Tax Agent Services (Code of Professional Conduct)
# Determination 2024. Both rights.html and /disclosure render these, so the
# two pages cannot drift apart. Owner and review date travel with each
# statement because the Code expects them to be maintained, not just posted.
DISCLOSURE_OWNER = "Huong Bui"
DISCLOSURE_REVIEWED = "11 September 2026"
DISCLOSURE_STATEMENTS = (
    "No prescribed events under section 45 of the Tax Agent Services (Code of "
    "Professional Conduct) Determination 2024 have occurred in the last 5 years.",
    "Our registration is not subject to any conditions limiting the scope of "
    "services we can provide.",
)


def disclosure_paragraphs(indent="        "):
    return "\n".join(
        f"{indent}<p>{text} Owner: {DISCLOSURE_OWNER}. Review date: {DISCLOSURE_REVIEWED}.</p>"
        for text in DISCLOSURE_STATEMENTS
    )


def picture(stem, alt, extra="", lazy=False, sizes="(max-width:940px) 100vw, 55vw"):
    loading = ' loading="lazy"' if lazy else ""
    w, h = STEM_SIZE[stem]
    return (
        f'          <picture>\n'
        f'            <source type="image/webp" srcset="{webp_srcset(stem)}" sizes="{sizes}">\n'
        f'            <img{extra} src="/assets/{stem}.jpg?v={IMG_VERSION}" width="{w}" height="{h}" alt="{alt}"{loading}>\n'
        f'          </picture>'
    )


def index():
    h = head(
        "Accountants Brendale | Tax, BAS and bookkeeping for trades",
        "Accountants and registered tax agents in Brendale for air con, electrical and construction businesses. Tax, BAS, bookkeeping and payroll. Queensland.",
        "/",
        extra=jsonld(business_node()) + jsonld(website_node()),
    )
    body = f"""{nav("home")}
  <main id="main">
    <section class="hero-bleed">
      <div class="hero-media" id="stage">
{picture("tech-hvac", "HVAC technician on a rooftop unit", ' class="is-on" data-trade="hvac" fetchpriority="high"', False, "100vw")}
{picture("electrical", "Electrical switchboard", ' data-trade="electrical" aria-hidden="true" inert', True, "100vw")}
{picture("construction", "Construction services fit-out", ' data-trade="construction" aria-hidden="true" inert', True, "100vw")}
        <div class="hero-scrim"></div>
        <div class="cap" id="stageCap">HVAC</div>
      </div>
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="kicker">Pink Accounting. Brendale.</p>
          <h1>Accountants, bookkeepers and tax agents in Brendale</h1>
          <p class="hook">For air con, electrical and construction businesses.</p>
          <p class="lead">You quoted 6 hours. You did 9. Every Monday we show you the hours quoted against the hours worked, and how much of the bank is really yours. Then we do the tax, BAS, books and payroll.</p>
          <div class="cta">
            <a class="btn btn-primary" href="/book.html" data-event="hero-book">Book 15 minutes</a>
            <a class="btn btn-ghost" href="/check.html" data-event="hero-check">Free 60-second hours check</a>
          </div>
    {trust_line()}
          <p class="why-call">The call is to see if we can take the file. You have not signed anything.</p>
          <div class="trades" aria-label="The same work on three kinds of job">
            <button class="trade is-on" type="button" data-trade="hvac" aria-pressed="true">Air con</button>
            <button class="trade" type="button" data-trade="electrical" aria-pressed="false">Electrical</button>
            <button class="trade" type="button" data-trade="construction" aria-pressed="false">Construction services</button>
          </div>
          <p class="live" id="liveLine">Air con and refrigeration. Quoted hours versus hours on the job.</p>
          <p class="trade-links">Same offer. Different jobs. <a href="/air-conditioning-accountant-brisbane/">Air con</a> · <a href="/electrician-accountant-brisbane/">Electrical</a> · <a href="/construction-services-accountant-brisbane/">Construction services</a></p>
          <div class="trust">
            <a class="stars" href="{REVIEWS_URL}" rel="noopener">
              <span class="star-value">{REVIEWS_RATING}</span>
              <span class="star-icons" aria-hidden="true">★★★★★</span>
              <span>{REVIEWS_COUNT} Google reviews as at {REVIEWS_AS_AT}</span>
            </a>
            <span class="trust-reg">Registered Tax Agent 26284368</span>
          </div>
        </div>
{hours_chart()}
      </div>
    </section>

    <section class="band band-bone">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">Before you read on</span>
          <h2>Is this you?</h2>
          <p class="sec-note">We would rather you worked that out now than on a call.</p>
        </div>
        <div class="hire">
          <article>
            <span class="eyebrow">A fit</span>
            <h3>Yes, if</h3>
            <ul class="ticks">
              <li><a href="/air-conditioning-accountant-brisbane/">Air con and refrigeration</a>, <a href="/electrician-accountant-brisbane/">electrical</a>, or <a href="/construction-services-accountant-brisbane/">construction services</a> meaning fit-out, maintenance and installation</li>
              <li>Queensland, and one trading entity</li>
              <li>You have people on the tools, staff or subcontractors, or you are about to put someone on</li>
              <li>You quote work and you could not say, today, which of last month's jobs actually made money</li>
            </ul>
          </article>
          <article>
            <span class="eyebrow">Not a fit</span>
            <h3>No, if</h3>
            <ul class="ticks is-no">
              <li>You are a builder. We do construction services, not head contracting</li>
              <li>You are hospitality or retail. Same firm, different site: <a href="https://www.pinktax.com.au" rel="noopener">pinktax.com.au</a></li>
              <li>You only want the annual return lodged. That is Compliance at $550 + GST a month and we will say so on the call</li>
              <li>You want a monthly meeting and unlimited work for one fee. That is not what this is</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
        <span class="eyebrow">The first question</span>
        <h2>You already have job software.</h2>
        <p class="sec-lead">Then you already know what a job should have cost, based on the hours that got entered. We answer the other half: what actually landed in the bank, how much of it is yours once GST, PAYG, super and wages come out, and what that says about the next quote.</p>
        <p class="sec-lead">simPRO, ServiceM8, AroFlo and the rest all feed Xero. Xero is where we work. We are not your software people and we will not pretend to be.</p>
        <p><a href="/job-software-and-your-accountant/">Why an accountant as well as the job system</a></p>
      </div>
    </section>

    <section class="band band-photo">
      <div class="wrap split-visual">
        <div class="photo-frame">
{picture("tech-electrical", "Electrician testing a switchboard", "", True, "(max-width:940px) 100vw, 45vw")}
        </div>
        <div class="split-copy">
          <h2>The bank looks full. It is not all yours.</h2>
          <p>GST, PAYG, super and wages sit in there. We pull that apart each week. We also hold tax and BAS. You stay on the tools.</p>
{cash_chart()}
          <a class="btn btn-primary" href="/book.html" data-event="split-book">Book a 15-minute call</a>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
      <figure class="watch">
        <div class="watch-frame">
          <video controls playsinline preload="metadata" poster="/assets/video/callback-cost-poster.jpg" width="720" height="1280">
            <source src="/assets/video/callback-cost.mp4" type="video/mp4">
          </video>
        </div>
        <figcaption>
          <h2>What a callback really costs</h2>
          <p>Two technicians. Labour on the clock. A $600 job given away because nobody counted the callback. Worked example, not a client result.</p>
        </figcaption>
      </figure>
      </div>
    </section>

    <section class="band" id="pricing">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">Fees</span>
          <h2>$1,650 + GST a month for most files.</h2>
          <p>That is Job Profit. Billed hours, cash, tax and BAS. Not unlimited work. The letter is the quote.</p>
          <p class="sec-note">The names, once: <b>Pink Accounting</b> is the firm and the registered tax agent. <b>Service Profit</b> is what we do for trade and service businesses. <b>Job Profit</b> is the plan most files sit on.</p>
        </div>
        <div class="feat" id="job-profit">
          <div>
            <span class="badge">Most files</span>
            <h3>Job Profit</h3>
            <div class="fprice">$1,650<small> + GST / month</small></div>

            <p class="fdesc">Billed hours versus quoted hours. How much of the bank is actually yours. Tax and BAS held. If you only need the return, that is Compliance at $550 + GST a month.</p>
            <div class="fcta"><a class="btn btn-primary" href="/book.html" data-event="pricing-book">Book a 15-minute call</a></div>
            <div class="fnote">Bookkeeping is extra, quoted when you need it. Not a plan.</div>
          </div>
          <ul>
            <li><b>Billed time</b> quoted hours versus hours on the tools, each week. If a job ran long, the next quote should not repeat it</li>
            <li><b>Cash that is yours</b> unfinished work, GST, PAYG, super and wages pulled apart so you know what you can spend</li>
            <li><b>Utes, phones, FBT</b> watched in the file. Not left as a June surprise</li>
            <li><b>Income tax, FBT, financial statements, BAS and GST held</b> for one trading entity, as written in the letter</li>
          </ul>
        </div>
        <div class="tiers">
          <a class="tier" href="/pricing.html#level-weekly">
            <div class="tname">Weekly Visibility</div>
            <div class="tprice">$2,650<small> + GST/mo, from</small></div>
            <p>Job Profit, plus a snapshot while the job is still on site. You see billed time before the job is closed.</p>
          </a>
          <a class="tier" href="/pricing.html#level-scale">
            <div class="tname">Ready to Scale</div>
            <div class="tprice">$3,500<small> + GST/mo, from</small></div>
            <p>Plus a written forecast: hire, draw, hold. Application only. Not a guaranteed result.</p>
          </a>
          <a class="tier" href="/pricing.html#level-compliance">
            <div class="tname">Compliance</div>
            <div class="tprice">$550<small> + GST/mo</small></div>
            <p>Income tax, FBT, financial statements, BAS and GST from a file that is already in order.</p>
          </a>
        </div>
        <p class="pricing-more"><a href="/pricing.html">Full plans, what is in, what is out, and the FAQ</a></p>
        <p class="pricing-more"><a href="/system.html#weekly">See what lands in your inbox on Monday</a></p>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">What happens</span>
          <h2>From the call to the first Monday.</h2>
          <p class="sec-note">Three steps. No black box in the middle.</p>
        </div>
        <div class="grid3">
          <section class="card">
            <span class="eyebrow">Step one</span>
            <h3>A 15-minute call</h3>
            <p>We look at whether we can take the file, and whether it is worth your money. If it is not, we say so and tell you what would be. You have not signed anything.</p>
          </section>
          <section class="card">
            <span class="eyebrow">Step two</span>
            <h3>A letter, then you decide</h3>
            <p>If it is a fit you get a letter of engagement setting out the scope, what is not included, and the monthly fee. The letter is the quote. Nothing starts until you sign it.</p>
          </section>
          <section class="card">
            <span class="eyebrow">Step three</span>
            <h3>The first month</h3>
            <p>You give Xero, bank and payroll access, or send the source documents. The start date is in the letter. Catch-up of earlier periods is a separate fee, quoted before we touch it.</p>
          </section>
        </div>
        <p class="note-ex">You stay on the tools throughout. We do not need a standing meeting in your diary.</p>
      </div>
    </section>

    <section class="band" id="reviews">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">Google reviews</span>
          <h2>{REVIEWS_RATING} on Google.</h2>
          <p class="sec-note">Reviews of Pink Accounting, the firm behind Service Profit. {REVIEWS_COUNT} reviews as at {REVIEWS_AS_AT}. They are not job-costing results.</p>
        </div>
{review_quotes()}
        <p class="creds"><a href="{REVIEWS_URL}" rel="noopener">Read all {REVIEWS_COUNT} Google reviews</a></p>
      </div>
    </section>

    <section class="band">
      <div class="wrap meet">
        <div class="shot photo-frame">
{picture("pink-home", "Huong Bui, principal of Service Profit", "", True, "(max-width:940px) 100vw, 40vw")}
        </div>
        <div>
          <span class="eyebrow">Pink</span>
          <h2>I am the accountant.</h2>
          <p>Huong Bui. Registered Tax Agent 26284368. More than ten years in the books. I started the firm in 2020.</p>
          <p>You call because the quotes and the bank no longer match, and you do not have time to sit in Xero. We take the file. You stay on the jobs.</p>
          <p>Master of Professional Accounting, Griffith. Member of the Institute of Public Accountants. Our registration carries no conditions limiting what we can do for you, and you can check that yourself on the <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB public register</a> against 26284368. What else we must tell you is on <a href="/disclosure">our disclosures page</a>.</p>
          <div class="creds"><a href="/why.html">Read more about Pink</a></div>
          <a class="btn btn-primary" href="/book.html" data-event="meet-book">Book a 15-minute call</a>
        </div>
      </div>
    </section>

    <section class="final">
      <div class="wrap">
        <h2>Book 15 minutes if this is your week.</h2>
        <p>If it is a fit, you get a letter and a monthly fee. If it is not, you have not signed anything. Brendale, Queensland.</p>
        <a class="btn btn-white" href="/book.html" data-event="final-book">Book 15 minutes</a>
        <div class="micro">Registered Tax Agent 26284368 · Business clients only · Queensland · <a href="/rights.html">Your rights</a> · <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></div>
      </div>
    </section>
  </main>
{sticky()}
{footer()}"""
    return h + body


def system():
    h = head(
        "Job costing for trades | Service Profit",
        "Billed hours, staff versus contractors, cash that is yours, tax and BAS held. Service Profit for HVAC, electrical and construction services in Queensland.",
        "/system.html",
        extra=jsonld(faq_node(SYSTEM_FAQ)),
    )
    faqs = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in SYSTEM_FAQ
    )
    body = f"""{nav("system")}
  <main id="main">
    <section class="page" style="padding-bottom:0">
      <div class="wrap">
        <span class="eyebrow">The system</span>
        <h1>Is $150 + GST an hour enough to relax?</h1>
        <p class="lead">That is a billed hour. It is not profit. GST comes off. Then the person on the tools, staff or contractor. Then parts. Then the business. We hold that picture, and we hold tax and BAS, so you can stay on the jobs.</p>
        <div class="cta">
          <a class="btn btn-primary" href="/book.html" data-event="system-book">Book a 15-minute call</a>
          <a class="btn btn-outline" href="/pricing.html">See the plans</a>
        </div>
{hour_waterfall()}
        <div class="hour-board">
          <div class="cell"><b>$150 + GST</b><span>Billed. Worked example, not your rate.</span></div>
          <div class="cell"><b>$15</b><span>GST. Not yours.</span></div>
          <div class="cell"><b>$150</b><span>Left on paper before labour and parts.</span></div>
          <div class="cell is-miss"><b>Then profit</b><span>Only if billed hours cover the real cost.</span></div>
        </div>
        <p class="note-ex">If labour costs you $50 all-in for an hour, one billed hour does not buy you a spare hour of profit. Count billed hours in the week before you hire.</p>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <span class="eyebrow">People</span>
        <h2 style="margin-top:12px">Staff or contractor. The file should show the true cost before you hire.</h2>
        <div class="hire">
          <article>
            <span class="eyebrow">Staff</span>
            <h3>Wage is not the full cost</h3>
            <p>Super, leave, workers compensation, PAYG and often a ute sit on top of the wage. How many $150 hours must actually be billed this week to cover that person, before your own time and any profit? If the diary cannot show those hours as billed, the hire is hope.</p>
          </article>
          <article>
            <span class="eyebrow">Contractor</span>
            <h3>The invoice is not automatically cheaper</h3>
            <p>A contractor invoice is visible on the job. That is useful. It is not automatically better. If they work like staff, the cost and the compliance both change. We read the numbers. We do not write the contract.</p>
          </article>
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap hire">
        <article>
          <span class="eyebrow">Hours you can afford</span>
          <h3>How many billed hours does that person need?</h3>
          <p>Take the weekly cost of the person. Divide by the billed rate after GST. That is the hours that must land on invoices this week, before materials and overhead. If that number is not in the diary, do not hire on a feeling.</p>
        </article>
        <article>
          <span class="eyebrow">Compliance</span>
          <h3>Income tax, FBT, financial statements</h3>
          <p>We are the tax agent. The return, FBT, BAS, GST, super and PAYG sit in the file so you are not paying tax on a mess. You stay on the jobs.</p>
          <a class="btn btn-primary" href="/book.html" data-event="system-comp" style="margin-top:18px">Book a 15-minute call</a>
        </article>
      </div>
    </section>
    <section class="band band-bone" id="weekly">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">What you actually get</span>
          <h2>This lands Monday morning.</h2>
          <p class="sec-note">Not a pack in October. Not a meeting you have to attend. One read on the phone between jobs.</p>
        </div>
{weekly_sample()}
        <div class="cta" style="margin-top:28px">
          <a class="btn btn-primary" href="/book.html" data-event="system-sample">Book a 15-minute call</a>
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <div class="faq">
{faqs}
        </div>
      </div>
    </section>
  </main>
{footer()}"""
    return h + body


def pricing():
    h = head(
        "Pricing | Trade accounting plans and fees | Service Profit",
        "Job Profit $1,650 + GST a month. Weekly Visibility from $2,650. Ready to Scale from $3,500. Compliance $550. What is in, what is out, and the FAQ. Queensland.",
        "/pricing.html",
        extra=jsonld(faq_node(PRICING_FAQ)),
    )
    faqs = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in PRICING_FAQ
    )
    body = f"""{nav("pricing")}
  <main id="main">
    <section class="page" style="padding-bottom:0">
      <div class="wrap">
        <span class="eyebrow">Pricing</span>
        <h1>Plans from $550 + GST a month</h1>
        <p class="lead">Most trade files are $1,650 + GST a month. A fixed monthly fee, set out in writing before anything starts.</p>
        <div class="cta">
          <a class="btn btn-primary" href="/book.html" data-event="pricing-page-book">Book a 15-minute call</a>
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <div class="feat" id="job-profit">
          <div>
            <span class="badge">Most files</span>
            <h2>Job Profit</h2>
            <div class="fprice">$1,650<small> + GST / month</small></div>

            <p class="fdesc">Billed hours versus quoted hours, and how much of the bank balance is actually yours.</p>
            <div class="fcta"><a class="btn btn-primary" href="/book.html" data-event="pricing-job">Book a 15-minute call</a></div>
          </div>
          <ul>
            <li><b>In:</b> billed hours vs quoted hours each week; cash that is yours vs GST, PAYG, super, wages; FBT watched in the file; income tax, FBT, financial statements, BAS and GST held for one trading entity</li>
            <li><b>Out:</b> a monthly meeting, unlimited work (ask anything; bigger jobs are quoted first), catch-up, a published savings figure</li>
          </ul>
        </div>
        <div class="table-scroll" tabindex="0" aria-label="Plan comparison. Scroll sideways on a small screen to read every column.">
          <table class="scope">
            <thead>
              <tr><th>Level</th><th>Fee</th><th>Included</th><th>Not included</th></tr>
            </thead>
            <tbody>
              <tr class="pop" id="level-job">
                <td><strong>Job Profit</strong></td>
                <td class="price">$1,650 + GST / month</td>
                <td>Billed hours vs quoted hours. Cash that is yours vs GST, PAYG, super, wages. FBT watched in the file. Books and BAS sit under that.</td>
                <td>A monthly meeting. Unlimited work: ask anything, bigger jobs are quoted first. Catch-up. A published savings figure.</td>
              </tr>
              <tr id="level-weekly">
                <td><strong>Weekly Visibility</strong></td>
                <td class="price">from $2,650 + GST / month</td>
                <td>Includes Job Profit. Snapshot while the job is still on site.</td>
                <td>Open-ended project work unless scoped.</td>
              </tr>
              <tr id="level-scale">
                <td><strong>Ready to Scale</strong></td>
                <td class="price">from $3,500 + GST / month</td>
                <td>Includes Weekly Visibility. Written forecast: hire, draw, hold. Application only.</td>
                <td>A guaranteed result. Unlimited work.</td>
              </tr>
              <tr id="level-compliance">
                <td><strong>Compliance</strong></td>
                <td class="price">$550 + GST / month</td>
                <td>Income tax, FBT, financial statements, BAS and GST from records already in order. We are the registered tax agent.</td>
                <td>Job-and-cash look. WhatsApp. Catch-up. Unlimited advisory.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="table-hint">Swipe sideways for every column.</p>
        <div class="scope-cards">
          <article class="scope-card" id="card-job"><h2>Job Profit</h2><div class="price">$1,650 + GST / month</div><p><b>In:</b> billed hours vs quoted hours, cash that is yours, FBT watched, tax and BAS held.</p><p><b>Out:</b> a monthly meeting, a published savings figure, catch-up.</p></article>
          <article class="scope-card"><h2>Weekly Visibility</h2><div class="price">from $2,650 + GST / month</div><p><b>In:</b> Job Profit, plus a snapshot while the job is still on site.</p><p><b>Out:</b> open-ended project work unless scoped.</p></article>
          <article class="scope-card"><h2>Ready to Scale</h2><div class="price">from $3,500 + GST / month</div><p><b>In:</b> Weekly Visibility, plus a written forecast: hire, draw, hold. Application only.</p><p><b>Out:</b> a guaranteed result. Unlimited work.</p></article>
          <article class="scope-card" id="card-compliance"><h2>Compliance</h2><div class="price">$550 + GST / month</div><p><b>In:</b> income tax, FBT, financial statements, BAS and GST from a file already in order.</p><p><b>Out:</b> job-and-cash look, WhatsApp, catch-up, unlimited advisory.</p></article>
        </div>
        <div class="addon" id="level-bookkeeping">
          <h2>Bookkeeping add-on · from $500 + GST / month</h2>
          <p>Not a plan. Quoted when it is actually needed: tax time, a catch-up, or while Job Profit is more than the business can take yet. It does not include the weekly job-and-cash look.</p>
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <h2>Questions about the fees</h2>
        <div class="faq">
{faqs}
        </div>
        <div class="cta">
          <a class="btn btn-primary" href="/book.html" data-event="pricing-faq-book">Book a 15-minute call</a>
        </div>
      </div>
    </section>
  </main>
{footer()}"""
    return h + body


def why():
    h = head(
        "Meet Huong Bui, registered tax agent | Service Profit",
        "Huong Bui, Master of Professional Accounting (Griffith), Registered Tax Agent 26284368. More than ten years in the books. Income tax, FBT, financial statements, BAS.",
        "/why.html",
        extra=jsonld(person_node()),
    )
    body = f"""{nav("why")}
  <main id="main">
    <section class="page" style="padding-bottom:0">
      <div class="wrap meet">
        <div class="shot">
{picture("pink-meet", "Huong Bui in a client meeting", "", False, "(max-width:940px) 100vw, 40vw")}
        </div>
        <div class="meet-copy">
          <span class="eyebrow">Meet Pink</span>
          <h1>Hello, I am Pink.</h1>
          <p class="lead">Huong Bui. Registered tax agent. More than ten years in the books. Air con, electrical and construction services in Queensland.</p>
          <p>I take the call when I am free. If I am already booked, a team member takes it and I read the notes the same working day. The file is held by the firm, not by one diary.</p>
          <a class="btn btn-primary" href="/book.html" data-event="why-book">Book 15 minutes</a>
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap prose">
        <h2>Qualification</h2>
        <p>Master of Professional Accounting, Griffith University. Member of the Institute of Public Accountants (MIPA AFA). Registered Tax Agent 26284368. ASIC Registered Agent 52580.</p>
        <h2>Years in the books</h2>
        <p>More than ten years. I started the firm in 2020. The work is in the file, not in a once-a-year pack.</p>
        <h2>What we hold</h2>
        <p>The return. FBT on utes, phones and other benefits. Financial statements. BAS and GST. Payroll, super and PAYG where you have staff. Tax so you are not paying on missing invoices.</p>
        <h2>On the public register</h2>
        <p>Search 26284368 on the <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB public register</a>. Our obligations are written on <a href="/rights.html">Your rights</a>. ABN 51 682 301 891.</p>
      </div>
    </section>
  </main>
{footer()}"""
    return h + body


def check():
    h = head(
        "Free hours check for trade jobs | Service Profit",
        "Type the last job. Hours quoted versus hours on the tools. Then book 15 minutes if you want the file held.",
        "/check.html",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap book-wide">
      <span class="eyebrow">Hours check</span>
      <h1>Where did the last job leak?</h1>
      <p class="lead">Hours you quoted. Hours on the tools. The rate you billed. Sixty seconds. Then we will tell you if the call is worth it.</p>
{hours_check()}
      <div class="prose">
        <p>This is a sketch from the numbers you type. Not your file. Not tax advice. On the call we look at the real jobs, the bank, and tax.</p>
        <p>Job Profit is $1,650 + GST a month for most files. The letter is the quote. You have not signed anything by booking.</p>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def book():
    h = head(
        "Book a 15-minute call | Service Profit | Pink Accounting",
        "Book a 15-minute call with Pink. Air con, electrical and construction services in Queensland.",
        "/book.html",
        extra=jsonld(
            {
                "@context": "https://schema.org",
                "@type": "ContactPage",
                "name": "Book a 15-minute call",
                "url": f"{ORIGIN}/book.html",
                "about": {"@id": f"{ORIGIN}/#business"},
            }
        ),
    )
    body = f"""{nav("book")}
  <main id="main" class="page">
    <div class="wrap book-wide">
      <span class="eyebrow">Book</span>
      <h1>Book a 15‑minute call</h1>
      <p class="lead">Talk to an accountant and registered tax agent. Pick a time first; the questions can wait.</p>
      <section class="pick-time" id="pick-time">
        <div class="cta">
          <a class="btn btn-primary" href="{MSBOOK}" rel="noopener" data-event="book-calendar">Open full-screen booking</a>
          <a class="btn btn-outline btn-call" href="tel:{ID["office"]["phone_e164"]}" data-event="book-call">Or call {ID["office"]["phone_display"]}</a>
        </div>
{trust_line()}
      </section>
      <h2>After you book: tell us a bit more</h2>
      <p>Optional. Revenue, staff, what is hurting, where you want the business in 12 months. Use the same email as your booking and we read it before the call.</p>
{enquiry_form("book")}
      <p class="creds">Pink Accounting &amp; Tax Solutions Pty Ltd · Shop 15A, 18-22 Kremzow Rd, Brendale QLD 4500 · Registered Tax Agent 26284368</p>
    </div>
  </main>
{footer()}"""
    return h + body


def contact():
    h = head(
        "Contact | Service Profit Brendale | Pink Accounting",
        "Talk to Pink Accounting at Shop 15A, 18-22 Kremzow Rd, Brendale QLD. HVAC, electrical and construction accounting across Brisbane and Queensland. 07 3544 6386.",
        "/contact.html",
        extra=jsonld(local_business_node()),
    )
    body = f"""{nav("contact")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Contact Pink Accounting</span>
      <h1>Talk to the accountant. Not a ticket queue.</h1>
      <p class="lead">Brendale office. HVAC, electrical and construction service businesses across Brisbane and Queensland.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="contact-book">Book a 15-minute call</a>
        <a class="btn btn-outline btn-call" href="tel:+61735446386">Call 07 3544 6386</a>
      </div>
      <div class="grid3">
        <section class="card"><span class="eyebrow">Phone</span><h2><a href="tel:+61735446386">07 3544 6386</a></h2><p>Office hours {ID["office"]["hours"]["display"]}. 15-minute calls run Monday to Thursday.</p></section>
        <section class="card"><span class="eyebrow">Email</span><h2><a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a></h2><p>The firm mailbox. A person reads it.</p></section>
        <section class="card"><span class="eyebrow">Visit</span><h2>Brendale QLD 4500</h2><p>Shop 15A, 18-22 Kremzow Rd. Moreton Bay, north of Brisbane. Service Profit is Queensland. Hospitality clients of the same firm sit on pinktax.com.au.</p></section>
      </div>
      <div class="sec-head">
        <span class="eyebrow">Or write to us</span>
        <h2>Send a short message instead.</h2>
        <p class="sec-note">Not everyone wants to ring. Six fields. It goes to the same mailbox.</p>
      </div>
{enquiry_form("contact", short=True, next_page="/contact.html")}
    </div>
  </main>
{footer()}"""
    return h + body


def privacy():
    h = head(
        "Privacy | Service Profit | Pink Accounting",
        "Privacy policy for Pink Accounting & Tax Solutions Pty Ltd, including the Service Profit service.",
        "/privacy.html",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Pink Accounting</span>
      <h1>Privacy</h1>
      <div class="prose">
        <p>Pink Accounting &amp; Tax Solutions Pty Ltd (ABN 51 682 301 891) handles personal information under the Privacy Act 1988. Service Profit is a service of this firm. This page applies to the whole practice. Last reviewed 11 September 2026.</p>
        <h2>What we collect</h2>
        <p>Name, contact details, business details, and the financial and tax information needed to provide accounting and tax services. If you send the enquiry form, book a call or email us, we keep that correspondence. Microsoft Bookings also holds the appointment details you enter there, when that calendar is open.</p>
        <h2>Why we collect it</h2>
        <p>To provide the service you asked for, meet our tax-agent and legal obligations, and run the practice. We do not sell lists.</p>
        <h2>How we hold it</h2>
        <p>Client files live in the firm’s Microsoft 365, Xero and related practice systems. Access is limited to people doing the work. We keep records for as long as tax and professional rules require, then destroy or de-identify them in the ordinary course.</p>
        <h2>Who we share it with</h2>
        <p>Only where the job requires it: the ATO, ASIC, your bank or software provider with your authority, professional indemnity insurers, and regulators when the law requires it. Microsoft, Xero, Google Analytics, Meta (when the advertising pixel is active) and similar suppliers process information to run those tools. Some of those suppliers store or support data outside Australia. We use them because the practice cannot run without them. Tell us if you do not want a named tool used on your file.</p>
        <h2>This website</h2>
        <p>This site runs Google Analytics 4 so we can see which pages are used and whether an enquiry was sent. If a Meta pixel ID is configured, Meta also receives a page view and a lead event after a successful enquiry. We do not treat a click on Book a call as a completed enquiry. The enquiry form is sent through Formsubmit to admin@pinktax.com.au. You can ask us not to use analytics on a future visit by writing to admin@pinktax.com.au.</p>
        <h2>Access and correction</h2>
        <p>You can ask to see the personal information we hold about you, and ask us to correct it. Write to admin@pinktax.com.au. We will respond within 30 days. If we refuse, we will say why and how to complain.</p>
        <h2>Complaints</h2>
        <p>Privacy complaints go first to admin@pinktax.com.au or 07 3544 6386. The principal reviews them. If we cannot resolve it, you can contact the Office of the Australian Information Commissioner at oaic.gov.au.</p>
        <h2>How to contact us</h2>
        <p>admin@pinktax.com.au or 07 3544 6386. Shop 15A, 18–22 Kremzow Rd, Brendale QLD 4500.</p>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def rights():
    h = head(
        "Your rights and our obligations | Service Profit",
        "Pink Accounting is a registered tax practitioner. TPB register, complaints, ABN, AI disclosure and professional obligations.",
        "/rights.html",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Pink Accounting</span>
      <h1>Your rights and our obligations</h1>
      <div class="prose">
        <p>We are a registered tax practitioner. Service Profit is a service of Pink Accounting &amp; Tax Solutions Pty Ltd, not a separate firm. Owner of these statements: Huong Bui. Last reviewed 11 September 2026.</p>
        <h2>The TPB public register</h2>
        <p>The Tax Practitioners Board maintains a public register of all registered tax and BAS agents. Search it at <a href="https://www.tpb.gov.au/public-register" rel="noopener">tpb.gov.au/public-register</a>. Our registration number is <b>26284368</b>.</p>
        <h2>How to make a complaint</h2>
        <p>If something is wrong, tell us first: <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a> or 07 3544 6386. The principal reviews every complaint. You can also complain to the TPB via <a href="https://www.tpb.gov.au/complaints" rel="noopener">tpb.gov.au/complaints</a>.</p>
        <h2>Rights, responsibilities and obligations</h2>
        <p>As a registered tax practitioner we must act honestly and with integrity, comply with the taxation laws in our own affairs, act lawfully in your best interests, manage conflicts of interest, take reasonable care to ascertain your state of affairs and apply the tax laws correctly, keep your information confidential unless we have a legal duty or your permission to disclose it, maintain professional indemnity insurance, and not knowingly obstruct the administration of the tax laws.</p>
        <p>You have obligations too: providing complete and accurate information, keeping the records the law requires, lodging and paying on time once advised, and telling us when your circumstances change. Our letter of engagement sets out both sides before work starts.</p>
        <h2>Verify us</h2>
        <p>Practising as Pink since 2020; incorporated as Pink Accounting &amp; Tax Solutions Pty Ltd in November 2024, which is why our current ABN shows a 2024 start date.</p>
        <ul>
          <li><b>Tax agent registration 26284368</b>. <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB public register</a></li>
          <li><b>ABN 51 682 301 891</b>. <a href="https://abr.business.gov.au/ABN/View?abn=51682301891" rel="noopener">ABN Lookup</a></li>
          <li><b>Company and business names</b>. ASIC, including Pink Accounting, Pink Strategic Accounting and Service Profit Accounting, the name this site trades under, registered 24 August 2026</li>
          <li><b>Professional membership</b>. Member, Institute of Public Accountants (MIPA AFA)</li>
        </ul>
        <p>If anything on this page disagrees with those registers, the register wins. Tell us: admin@pinktax.com.au.</p>
        <h2>Smart technology, real expertise</h2>
        <p>Pink pairs experienced people with business-grade tools for research, data and drafting. We do the thinking, the judgment and the advice. Every output is reviewed and signed off by a qualified member of the team. No automated tool makes decisions about your tax affairs. We do not allow confidential information to train public models. Personal information is handled under the Privacy Act 1988. If you would prefer we did not use those tools on your file, tell us.</p>
        <h2 id="disclosure">Disclosure statements</h2>
{disclosure_paragraphs()}
        <p>These also sit on their own page at <a href="/disclosure">serviceprofit.com.au/disclosure</a>, which is the address to give a client who asks for them.</p>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def disclosure():
    h = head(
        "Disclosures | Service Profit | Pink Accounting",
        "Section 45 Code Determination disclosures for Pink Accounting & Tax Solutions Pty Ltd, Registered Tax Agent 26284368, with the TPB register and the complaints process.",
        "/disclosure",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Pink Accounting</span>
      <h1>Disclosures</h1>
      <div class="prose">
        <p>Pink Accounting &amp; Tax Solutions Pty Ltd, ABN 51 682 301 891, Registered Tax Agent 26284368. Service Profit is a service of this firm, not a separate practice. These are the disclosures required of a registered tax practitioner. Owner: {DISCLOSURE_OWNER}. Last reviewed {DISCLOSURE_REVIEWED}.</p>
        <h2>Matters we must disclose</h2>
{disclosure_paragraphs()}
        <h2>Check the register yourself</h2>
        <p>The Tax Practitioners Board keeps a public register of every registered tax and BAS agent, including any conditions or sanctions. Search <b>26284368</b> at <a href="https://www.tpb.gov.au/public-register" rel="noopener">tpb.gov.au/public-register</a>. If anything here disagrees with the register, the register is correct and we want to know: <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a>.</p>
        <h2>If you need to complain</h2>
        <p>Tell us first. Email <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a> or call 07 3544 6386. The principal reviews every complaint. If we have not resolved it, you can take it to the TPB at <a href="https://www.tpb.gov.au/complaints" rel="noopener">tpb.gov.au/complaints</a>. Complaining to the TPB does not cost you anything and does not affect your file with us.</p>
        <h2>The rest of your rights</h2>
        <p>Our full obligations to you, your obligations to us, how we use technology on your file and how to verify the firm are on <a href="/rights.html">Your rights and our obligations</a>. How we handle personal information is on <a href="/privacy.html">Privacy</a>.</p>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def terms():
    h = head(
        "Terms | Service Profit | Pink Accounting",
        "Website and enquiry terms for Pink Accounting Service Profit. The letter of engagement is the contract for paid work.",
        "/terms.html",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Pink Accounting</span>
      <h1>Terms</h1>
      <div class="prose">
        <p>These terms cover this website and an enquiry or discovery call. Paid work is governed by the letter of engagement, not this page. Last reviewed 11 September 2026.</p>
        <h2>Who we are</h2>
        <p>Pink Accounting &amp; Tax Solutions Pty Ltd, ABN 51 682 301 891, Registered Tax Agent 26284368. Service Profit is a Queensland service line of that firm.</p>
        <h2>The call</h2>
        <p>A booked call is a conversation to see whether there is a fit. It is not tax advice, not an engagement, and not a quote until the letter is issued. The enquiry form on this site emails admin@pinktax.com.au. Booking software is Microsoft Bookings when that calendar is open. Confirmation then goes to you and to admin@pinktax.com.au.</p>
        <h2>Fees on this site</h2>
        <p>Published fees are monthly, exclusive of GST, for one trading entity unless the letter says otherwise. Starting prices can rise with volume, payroll, extra entities or catch-up. The letter is the quote.</p>
        <h2>No unlimited work</h2>
        <p>Scope is defined. Extra work is quoted before we start it.</p>
        <h2>Liability</h2>
        <p>Liability limited by a scheme approved under Professional Standards Legislation.</p>
        <h2>Contact</h2>
        <p>admin@pinktax.com.au · 07 3544 6386 · Shop 15A, 18-22 Kremzow Rd, Brendale QLD 4500.</p>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def redirect_to(title, dest, label):
    """GitHub Pages cannot send a 301. Canonical plus refresh plus JS is the
    strongest consolidation this host allows. Old trade stubs now point at the
    matching audience page, not the homepage, so the HVAC URL does not keep
    telling Google the homepage is the HVAC document."""
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Service Profit</title>
  <link rel="canonical" href="{ORIGIN}{dest}">
  <meta http-equiv="refresh" content="0;url={dest}">
  <script>location.replace("{dest}");</script>
</head>
<body>
  <p>Service Profit is one offer. The {label} page is <a href="{dest}">{label}</a>.</p>
</body>
</html>
"""


def not_found():
    h = head(
        "Page not found | Service Profit | Pink Accounting",
        "That page is not on the Service Profit site.",
        "/404.html",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Service Profit</span>
      <h1>That page is not here.</h1>
      <p class="lead">Go back to Service Profit. HVAC, electrical and construction service businesses in Queensland.</p>
      <div class="cta"><a class="btn btn-primary" href="/index.html">Home</a></div>
    </div>
  </main>
{footer()}"""
    # A direct hit on /404.html returns 200. Keep it out of the index.
    return (h + body).replace('content="index,follow"', 'content="noindex,follow"', 1)


SITEMAP = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{ORIGIN}/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/system.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/pricing.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/why.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/book.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/check.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/contact.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/rights.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/disclosure</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/privacy.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/terms.html</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/air-conditioning-accountant-brisbane/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/electrician-accountant-brisbane/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/construction-services-accountant-brisbane/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/quoted-hours-vs-actual-hours/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/cash-that-is-yours/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/can-i-afford-another-technician/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/job-software-and-your-accountant/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/services/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/tax-agent-for-trades/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/bas-and-gst-for-trades/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/payroll-for-trades/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/bookkeeping-and-xero-for-trades/</loc><lastmod>2026-09-24</lastmod></url>
  <url><loc>{ORIGIN}/accountant-brendale/</loc><lastmod>2026-09-24</lastmod></url>
</urlset>
"""

LLMS_TXT = """# Service Profit

> Accounting for air con, electrical and construction services in Queensland. A line of Pink Accounting. Registered Tax Agent 26284368.

Pink Accounting & Tax Solutions Pty Ltd is the firm. Service Profit is what we do for those trades. Not a separate company. Not hospitality. Hospitality sits on https://pinktax.com.au/.

Job Profit is $1,650 + GST a month for most files. The letter is the quote. Book 15 minutes: https://www.serviceprofit.com.au/book.html

## Offer

- [Home](https://www.serviceprofit.com.au/): quoted hours versus hours on the tools
- [Pricing](https://www.serviceprofit.com.au/pricing.html): four plans, in and out
- [The system](https://www.serviceprofit.com.au/system.html): billed hours, cash that is yours, tax and BAS
- [Hours check](https://www.serviceprofit.com.au/check.html): last job, or the crew for a year
- [Book](https://www.serviceprofit.com.au/book.html): 15 minutes
- [Contact](https://www.serviceprofit.com.au/contact.html): Brendale QLD 4500, 07 3544 6386

## Who it is for

- [Air con accountant, Brisbane](https://www.serviceprofit.com.au/air-conditioning-accountant-brisbane/)
- [Electrician accountant, Brisbane](https://www.serviceprofit.com.au/electrician-accountant-brisbane/)
- [Construction services accountant, Brisbane](https://www.serviceprofit.com.au/construction-services-accountant-brisbane/)

Construction services means fit-out, maintenance and installation. Not head contracting. Not house builders.

## Services

- [All services](https://www.serviceprofit.com.au/services/): accountant, tax agent, BAS, bookkeeping, payroll, Xero setup, advisory
- [Tax agent for trades](https://www.serviceprofit.com.au/tax-agent-for-trades/): income tax, tax planning, FBT, TPAR
- [BAS and GST for trades](https://www.serviceprofit.com.au/bas-and-gst-for-trades/): BAS services under the tax agent registration
- [Bookkeeping and Xero setup](https://www.serviceprofit.com.au/bookkeeping-and-xero-for-trades/)
- [Payroll and super](https://www.serviceprofit.com.au/payroll-for-trades/): Single Touch Payroll, Payday Super
- [Accountant in Brendale](https://www.serviceprofit.com.au/accountant-brendale/)

## Job numbers

- [Quoted hours vs hours on the tools](https://www.serviceprofit.com.au/quoted-hours-vs-actual-hours/)
- [Cash that is yours](https://www.serviceprofit.com.au/cash-that-is-yours/)
- [Can I afford another technician?](https://www.serviceprofit.com.au/can-i-afford-another-technician/)

## Firm

- [Meet Pink](https://www.serviceprofit.com.au/why.html): Huong Bui, Registered Tax Agent 26284368
- [Disclosures](https://www.serviceprofit.com.au/disclosure)
- [Your rights](https://www.serviceprofit.com.au/rights.html)
- [Privacy](https://www.serviceprofit.com.au/privacy.html)
- [Terms](https://www.serviceprofit.com.au/terms.html)
- [Machine-readable fees](https://www.serviceprofit.com.au/pricing.md)

ABN 51 682 301 891. Shop 15A, 18-22 Kremzow Rd, Brendale QLD 4500. Business clients only. Queensland.
"""

PRICING_MD = """# Service Profit fees

Monthly, exclusive of GST, for one trading entity unless the letter says otherwise. Same plans for air con, electrical and construction services. The letter is the quote.

Human page: https://www.serviceprofit.com.au/pricing.html

## Job Profit

- Fee: $1,650 + GST / month
- Most files
- In: billed hours vs quoted hours each week; cash that is yours vs GST, PAYG, super, wages; FBT watched in the file; income tax, FBT, financial statements, BAS and GST held for one trading entity
- Out: a monthly meeting, unlimited work (ask anything; bigger jobs are quoted first), catch-up, a published savings figure

## Weekly Visibility

- Fee: from $2,650 + GST / month
- In: Job Profit, plus a snapshot while the job is still on site
- Out: open-ended project work unless scoped

## Ready to Scale

- Fee: from $3,500 + GST / month
- In: Weekly Visibility, plus a written forecast: hire, draw, hold. Application only
- Out: a guaranteed result. Unlimited work

## Compliance

- Fee: $550 + GST / month
- In: income tax, FBT, financial statements, BAS and GST from a file already in order
- Out: job-and-cash look, WhatsApp, catch-up, unlimited advisory

Bookkeeping is an add-on from $500 + GST a month, quoted when it is actually needed. It is not a plan.

A booked call is not an engagement. https://www.serviceprofit.com.au/book.html
"""


def main():
    write("index.html", index())
    write("system.html", system())
    write("pricing.html", pricing())
    write("why.html", why())
    write("book.html", book())
    write("check.html", check())
    write("contact.html", contact())
    write("privacy.html", privacy())
    write("rights.html", rights())
    write("terms.html", terms())
    write("hvac.html", redirect_to("HVAC", "/air-conditioning-accountant-brisbane/", "air con accountant"))
    write("electrical.html", redirect_to("Electrical", "/electrician-accountant-brisbane/", "electrician accountant"))
    write("construction.html", redirect_to("Construction", "/construction-services-accountant-brisbane/", "construction services accountant"))
    for builder in seo_pages.PAGES:
        slug, html = builder()
        seo_pages.write_pretty(ROOT, slug, html)
    write("disclosure.html", disclosure())
    (ROOT / "disclosure").mkdir(exist_ok=True)
    write("disclosure/index.html", disclosure())
    write("404.html", not_found())
    (ROOT / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    print("wrote sitemap.xml")
    (ROOT / "llms.txt").write_text(LLMS_TXT, encoding="utf-8")
    print("wrote llms.txt")
    (ROOT / "pricing.md").write_text(PRICING_MD, encoding="utf-8")
    print("wrote pricing.md")


if __name__ == "__main__":
    main()
