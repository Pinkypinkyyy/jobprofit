"""Audience and resource pages. Same offer. Different jobs. Not three products."""

import re

from shared import ORIGIN, faq_node, footer, head, jsonld, nav, service_node

STEM_SIZE = {
    "tech-hvac": (838, 1059),
    "tech-electrical": (838, 1059),
    "construction": (838, 1036),
}


def picture(stem, alt, extra="", lazy=True, sizes="(max-width:940px) 100vw, 55vw"):
    loading = ' loading="lazy"' if lazy else ""
    w, h = STEM_SIZE[stem]
    return (
        f'          <picture>\n'
        f'            <source type="image/webp" srcset="/assets/{stem}-480.webp?v=real1 480w, /assets/{stem}-864.webp?v=real1 864w, /assets/{stem}-1200.webp?v=real1 1200w" sizes="{sizes}">\n'
        f'            <img{extra} src="/assets/{stem}.jpg?v=real1" width="{w}" height="{h}" alt="{alt}"{loading}>\n'
        f'          </picture>'
    )


def same_offer():
    return """        <div class="same-offer">
          <p>Same plans as the rest of Service Profit. Not a separate HVAC product, not a separate electrical product. Job Profit is $1,650 + GST a month for most files. The letter is the quote.</p>
          <p><a href="/pricing.html">See the plans</a> · <a href="/system.html#weekly">See what lands on Monday</a> · <a href="/book.html">Book 15 minutes</a></p>
        </div>"""


def trade_more(current):
    links = [
        ("/air-conditioning-accountant-brisbane/", "Air con"),
        ("/electrician-accountant-brisbane/", "Electrical"),
        ("/construction-services-accountant-brisbane/", "Construction services"),
        ("/quoted-hours-vs-actual-hours/", "Quoted vs actual hours"),
        ("/cash-that-is-yours/", "Cash that is yours"),
        ("/can-i-afford-another-technician/", "Another technician"),
    ]
    items = "\n".join(
        f'          <a href="{href}">{label}</a>'
        for href, label in links
        if not href.rstrip("/").endswith(current.rstrip("/"))
    )
    return f'        <p class="trade-more">Also on this site\n{items}\n        </p>'


def breadcrumbs(slug, name):
    """Home > this page. Google needs it to show the path instead of the raw URL."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{ORIGIN}/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": f"{ORIGIN}/{slug}/"},
        ],
    }


def write_pretty(root, slug, html):
    # Added here rather than in each builder so every page on PAGES gets one.
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    name = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else slug
    html = html.replace("</head>", jsonld(breadcrumbs(slug, name)) + "</head>", 1)
    (root / slug).mkdir(exist_ok=True)
    (root / f"{slug}.html").write_text(html, encoding="utf-8")
    (root / slug / "index.html").write_text(html, encoding="utf-8")
    print("wrote", slug)


def air_con():
    slug = "air-conditioning-accountant-brisbane"
    faqs = [
        (
            "Do you only work with air con businesses?",
            "No. Service Profit is one offer for air con and refrigeration, electrical, and construction services. The job language changes. The plans do not.",
        ),
        (
            "What about maintenance contracts versus installs?",
            "They are different jobs. A maintenance round that runs long is not the same leak as a rooftop changeover that forgot the crane. We read both in the file. We do not invent a savings figure from either.",
        ),
        (
            "How do I start?",
            "Book 15 minutes or run the hours check. A booked call is a conversation to see whether we can take the file. It is not an engagement until the letter is issued.",
        ),
    ]
    extra = jsonld(service_node(
        "Air conditioning accountant, Brisbane and Queensland",
        f"{ORIGIN}/{slug}/",
        "Accounting for air con and refrigeration businesses in Queensland. Quoted hours versus hours on the tools, cash that is yours, tax and BAS held.",
    )) + jsonld(faq_node(faqs))
    h = head(
        "Air con accountant Brisbane | Service Profit",
        "Accounting for air con and refrigeration in Queensland. Quoted hours versus hours on the roof. Cash, tax and BAS held. Book 15 minutes.",
        f"/{slug}",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Air con and refrigeration</span>
      <h1>Quoted six hours on the roof. Nine on the tools.</h1>
      <p class="lead">Call-outs, changeovers, maintenance rounds. The quote is one number. The day is another. We keep billed hours, cash and tax in the file so you can stay on the roof. Queensland.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="hvac-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/check.html" data-event="hvac-check">Free hours check</a>
      </div>
      <div class="photo-frame" style="margin:28px 0">
{picture("tech-hvac", "HVAC technician on a rooftop unit")}
      </div>
      <div class="prose">
        <h2>The leak is usually the next quote</h2>
        <p>A rooftop changeover quoted at six hours that took nine does not only cost three hours. It trains the next quote to stay at six. Crane time, access, recovery of old gas, a second tech for the lift: if those are not in the template, they will not be in the price.</p>
        <p>That is a worked pattern, not a client result. Your jobs will be different. The file still has to show quoted hours against hours on the tools, job by job, before you price the next one.</p>
        <h2>Call-outs and maintenance are not the same job as an install</h2>
        <p>A summer of call-outs can fill the bank and still leave you short once GST, PAYG, super and wages come out. A maintenance contract that looks fat on paper can lose money if the round runs long and nobody counts the extra hours. An install that bills parts at cost needs the labour to land, or the margin is the parts handling and nothing else.</p>
        <p>We do not run your diary. We hold the numbers so you can see which of those jobs actually paid.</p>
        <h2>Vans, utes and FBT sit in the same file</h2>
        <p>Air con work moves in vans and on roofs. FBT on utes and phones is not a June surprise if it is watched in the file. Tax and BAS are held with the hours and the cash. You stay on the tools.</p>
        <h2>Who this page is for</h2>
        <p>Air con and refrigeration businesses in Queensland, with people on the tools or about to put someone on, who quote work and could not say today which of last month's jobs made money. One trading entity unless the letter says otherwise.</p>
        <p>Not a fit if you only want the annual return lodged. That is Compliance at $550 + GST a month, and we will say so on the call.</p>
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


def electrical():
    slug = "electrician-accountant-brisbane"
    faqs = [
        (
            "Do you only work with electricians?",
            "No. Service Profit is one offer for electrical, air con and refrigeration, and construction services. Same plans. The examples on this page are electrical because that is the search.",
        ),
        (
            "What about subcontractors on a board upgrade?",
            "A contractor invoice is visible on the job. That is useful. It is not automatically cheaper than staff once you count how they actually work. We show the cost in the file. We do not write the contract.",
        ),
        (
            "How do I start?",
            "Book 15 minutes or run the hours check. You have not signed anything by booking.",
        ),
    ]
    extra = jsonld(service_node(
        "Electrician accountant, Brisbane and Queensland",
        f"{ORIGIN}/{slug}/",
        "Accounting for electrical contractors in Queensland. Quoted hours versus hours on the tools, unfinished work, cash, tax and BAS held.",
    )) + jsonld(faq_node(faqs))
    h = head(
        "Electrician accountant Brisbane | Service Profit",
        "Accounting for electrical contractors in Queensland. Quoted hours versus hours on the tools. Cash, tax and BAS held. Book 15 minutes.",
        f"/{slug}",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Electrical</span>
      <h1>The switchboard ran long. The quote did not.</h1>
      <p class="lead">Quoted jobs versus hours on the tools. Variations that never made an invoice. Cash that looks like yours until GST, PAYG, super and wages come out. Queensland.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="elec-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/check.html" data-event="elec-check">Free hours check</a>
      </div>
      <div class="photo-frame" style="margin:28px 0">
{picture("tech-electrical", "Electrician testing a switchboard")}
      </div>
      <div class="prose">
        <h2>Unfinished work hides in a busy week</h2>
        <p>A board upgrade quoted at six hours that took nine is the obvious leak. The quieter one is the job that is still open, materials on the van, labour already spent, nothing invoiced. The bank can look full while that work is sitting in the week unpaid.</p>
        <p>Worked pattern, not a client result. The file still has to show which jobs closed, which are open, and whether the quote covered the hours that actually landed.</p>
        <h2>Staff, apprentices and contractors</h2>
        <p>An apprentice is not a billed hour until the work they do is on an invoice. A contractor invoice is easy to see. Staff cost is not the wage: super, leave, workers compensation, PAYG and often a ute sit on top. Before you hire, the diary has to show the billed hours that person needs this week. If it cannot, the hire is hope.</p>
        <h2>Variations</h2>
        <p>Extra points, extra circuits, a return visit because the board was not as drawn. If the variation never becomes a line on the invoice, the hours still happened. We do not chase your customers. We keep the hours and the bills in the same picture so you can see it.</p>
        <h2>Who this page is for</h2>
        <p>Electrical contractors in Queensland, with people on the tools or about to put someone on, who quote work and could not say today which of last month's jobs made money. One trading entity unless the letter says otherwise.</p>
        <p>Not a fit if you are a builder. We do construction services, not head contracting.</p>
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


def construction():
    slug = "construction-services-accountant-brisbane"
    faqs = [
        (
            "Do you take builders?",
            "No. Construction services here means fit-out, maintenance and installation. Not head contracting. If you are a builder, we will say so on the call and we will not take the file.",
        ),
        (
            "Is this a different plan to HVAC and electrical?",
            "No. Same plans. Job Profit is $1,650 + GST a month for most files. The letter is the quote.",
        ),
        (
            "How do I start?",
            "Book 15 minutes. You have not signed anything by booking.",
        ),
    ]
    extra = jsonld(service_node(
        "Construction services accountant, Brisbane and Queensland",
        f"{ORIGIN}/{slug}/",
        "Accounting for fit-out, maintenance and installation businesses in Queensland. Not head contracting. Quoted hours, cash, tax and BAS held.",
    )) + jsonld(faq_node(faqs))
    h = head(
        "Construction services accountant | Brisbane",
        "Fit-out, maintenance and installation in Queensland. Not head contracting. Quoted hours, cash, tax and BAS held. Book 15 minutes.",
        f"/{slug}",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Construction services</span>
      <h1>Fit-out, maintenance, installation. Not a builder.</h1>
      <p class="lead">Quoted hours versus hours on site. Materials and subcontractors in the same picture as the bank. Tax and BAS held. Queensland.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="con-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/check.html" data-event="con-check">Free hours check</a>
      </div>
      <div class="photo-frame" style="margin:28px 0">
{picture("construction", "Construction services fit-out")}
      </div>
      <div class="prose">
        <h2>The job, not the building</h2>
        <p>Fit-out, maintenance and installation run on quotes and hours, the same way air con and electrical do. Head contracting does not. Progress claims, retentions and a QBCC licence for a builder are a different file. We do not take that file.</p>
        <p>If your work is installing, maintaining or fitting out, and you quote hours, this page is for you. If you are the builder, it is not.</p>
        <h2>Site hours that never made the quote</h2>
        <p>Access delayed. The room was not ready. A return visit because the first measure was wrong. Six hours quoted, nine on site. If that overrun does not change the next quote, you donate the three hours again. Worked pattern, not a client result.</p>
        <h2>Materials and subcontractors</h2>
        <p>A subcontractor invoice is easy to see. Materials sitting for a job that has not billed yet are not. The bank can look full while both are waiting. We pull GST, PAYG, super and wages out of that balance so you know what is actually yours to spend.</p>
        <h2>Who this page is for</h2>
        <p>Construction services in Queensland: fit-out, maintenance, installation. People on the tools, or about to put someone on. One trading entity unless the letter says otherwise.</p>
        <p>Not a fit if you are a builder, or if you only want the annual return lodged. That is Compliance at $550 + GST a month.</p>
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


def quoted_hours():
    slug = "quoted-hours-vs-actual-hours"
    faqs = [
        (
            "Is this a calculator or tax advice?",
            "Neither as a promise. The hours check is a sketch from numbers you type. Tax advice sits in the letter, on a file we hold.",
        ),
        (
            "What do you do with the leak once you see it?",
            "The next quote should not repeat it. That is your decision. We keep the hours in the file so the leak is visible while you can still change the template.",
        ),
    ]
    extra = jsonld(faq_node(faqs))
    h = head(
        "Quoted hours vs hours on the tools",
        "How a job quoted at six hours and done in nine trains the next quote. Sketch the last job. Queensland.",
        f"/{slug}",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Job profitability</span>
      <h1>Quoted hours versus hours on the tools</h1>
      <p class="lead">Six on the quote. Nine on the job. Those three hours do not only cost this week. They teach the next quote to stay at six.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/check.html" data-event="qh-check">Sketch the last job</a>
        <a class="btn btn-outline" href="/book.html" data-event="qh-book">Book 15 minutes</a>
      </div>
      <div class="prose">
        <h2>The simple sum</h2>
        <p>Hours on the tools, minus hours you quoted, times the rate you billed excluding GST. That is the labour that never made the invoice. Parts, travel and a second pair of hands sit on top of that. The hours check on this site does the first sum from numbers you type. It is a sketch. Not your file.</p>
        <p>Worked example, not a client result: quoted 6, on the tools 9, billed at $150 an hour excluding GST. Three hours. About $450 that did not make the next quote.</p>
        <h2>Why the next quote matters more than this one</h2>
        <p>One overrun is a bad day. Repeating the same quote is a method. If crane time, recovery, access or a second tech is missing from the template, it will be missing every time that job comes around.</p>
        <h2>What Job Profit holds</h2>
        <p>Quoted hours versus hours on the tools, each week, across the jobs that closed. If two jobs did most of the overrun, those two are the ones to fix in the template. See a labelled sample of that Monday read on <a href="/system.html#weekly">the system page</a>.</p>
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


def cash_yours():
    slug = "cash-that-is-yours"
    faqs = [
        (
            "Is the bank split tax advice?",
            "No. It is a picture of what is already in the file: GST, PAYG, super, wages, and what is left. Tax advice sits in the letter.",
        ),
        (
            "Do you hold the money?",
            "No. We hold the file. The money stays in your bank. The split is so you do not spend the ATO's week.",
        ),
    ]
    extra = jsonld(faq_node(faqs))
    h = head(
        "Cash that is yours | Service Profit",
        "The bank looks full. GST, PAYG, super and wages sit in there. What is actually yours to spend. Queensland.",
        f"/{slug}",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Cash</span>
      <h1>The bank looks full. It is not all yours.</h1>
      <p class="lead">GST, PAYG, super and wages sit in the same balance as the money you can spend. Pull them apart each week or you find out on BAS day.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="cash-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/system.html#weekly" data-event="cash-sample">See the Monday sample</a>
      </div>
      <div class="prose">
        <h2>Four holds, then yours</h2>
        <p>GST collected is not yours. PAYG and super for the people on the tools are not yours. Wages still to go out this week are not yours. What is left after those holds is the number that can move. Unfinished work makes the picture worse: labour already spent, nothing in yet.</p>
        <p>The Monday sample on the system page uses invented figures and says so. Bank $84,200. GST $11,400. PAYG and super $9,860. Wages $18,300. Yours $44,640. Your first week uses your jobs and your bank.</p>
        <h2>A profitable week can still be tight</h2>
        <p>Quoted hours can land and the bank can still be the ATO's. That is not a reason to skip jobs. It is a reason to stop reading the bank app as profit.</p>
        <h2>Tax sits in the same file</h2>
        <p>Income tax, FBT, financial statements, BAS and GST are held with the cash split. You stay on the tools. We do not need a standing meeting in your diary for that read to exist.</p>
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


def another_tech():
    slug = "can-i-afford-another-technician"
    faqs = [
        (
            "Will you tell me to hire?",
            "No. We show the cost of staff and of a contractor in the file. The employment decision is yours. If someone works like staff, that is a compliance issue as well as a cost issue.",
        ),
        (
            "What number should I look at?",
            "Weekly cost of the person, divided by the billed rate after GST. That is the hours that must land on invoices this week, before materials and overhead. If the diary cannot show those hours as billed, do not hire on a feeling.",
        ),
    ]
    extra = jsonld(faq_node(faqs))
    h = head(
        "Can I afford another technician?",
        "Wage is not the full cost. Super, leave, workers compensation, PAYG and a ute sit on top. Count billed hours before you hire.",
        f"/{slug}",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">People</span>
      <h1>Can I afford another technician?</h1>
      <p class="lead">Wage is not the cost. Super, leave, workers compensation, PAYG and often a ute sit on top. The diary has to show the billed hours that person needs this week.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/check.html" data-event="hire-check">Hours check</a>
        <a class="btn btn-outline" href="/book.html" data-event="hire-book">Book 15 minutes</a>
      </div>
      <div class="prose">
        <h2>The hours that must land</h2>
        <p>Take the weekly cost of the person, all-in. Divide by the billed rate after GST. That is the hours that must actually be invoiced this week, before materials and overhead, before your own time, before any profit. If labour costs $50 all-in for an hour and you bill $150 + GST, one billed hour does not buy you a spare hour of profit.</p>
        <p>Worked method, not a client result, not a recommendation to hire.</p>
        <h2>Staff is not automatically worse than a contractor</h2>
        <p>A contractor invoice is visible on the job. Staff cost is hidden until you add the on-costs. If the contractor works like staff, the cost and the compliance both change. We read the numbers. We do not write the contract.</p>
        <h2>The crew check</h2>
        <p>If four people each lose three hours a week at $145 billed, that is $1,740 a week, about $90,480 a year, that never made a quote. That sum is a sketch from numbers you type on the <a href="/check.html">hours check</a>. Real weeks are not all billable. Fifty-two is the year on paper.</p>
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


PAGES = (air_con, electrical, construction, quoted_hours, cash_yours, another_tech)
