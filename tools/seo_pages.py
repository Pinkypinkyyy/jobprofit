"""Audience and resource pages. Same offer. Different jobs. Not three products."""

import re

from shared import ID, IMG_VERSION, trust_line, ORIGIN, faq_node, footer, head, jsonld, nav, service_node, webp_srcset

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
        f'            <source type="image/webp" srcset="{webp_srcset(stem)}" sizes="{sizes}">\n'
        f'            <img{extra} src="/assets/{stem}.jpg?v={IMG_VERSION}" width="{w}" height="{h}" alt="{alt}"{loading}>\n'
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
        ("/job-software-and-your-accountant/", "You already have job software"),
        ("/services/", "All services"),
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
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    name = title.group(1).split(" | ")[0].strip() if title else slug
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
        "Air conditioning accountant Brisbane | Tax, BAS, payroll",
        "Accounting for air con and refrigeration in Queensland. Quoted hours versus hours on the roof. Cash, tax and BAS held. Book 15 minutes.",
        f"/{slug}/",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Air con and refrigeration</span>
      <h1>Air conditioning accountant in Brisbane</h1>
      <p class="hook">Quoted six hours on the roof. Nine on the tools.</p>
      <p class="lead">Call-outs, changeovers, maintenance rounds: the quote is one number, the day is another. We show you which jobs paid, and do the tax, BAS, books and payroll.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="hvac-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/check.html" data-event="hvac-check">Free hours check</a>
      </div>
{trust_line()}
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
        "Electrician accountant Brisbane | Tax, BAS, payroll",
        "Accounting for electrical contractors in Queensland. Quoted hours versus hours on the tools. Cash, tax and BAS held. Book 15 minutes.",
        f"/{slug}/",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Electrical</span>
      <h1>Accountant for electricians in Brisbane</h1>
      <p class="hook">The switchboard ran long. The quote did not.</p>
      <p class="lead">Quoted jobs against hours on the tools, and variations that never made an invoice. We show you which jobs paid, and do the tax, BAS, books and payroll.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="elec-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/check.html" data-event="elec-check">Free hours check</a>
      </div>
{trust_line()}
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
        "Construction services accountant Brisbane | Tax and BAS",
        "Fit-out, maintenance and installation in Queensland. Not head contracting. Quoted hours, cash, tax and BAS held. Book 15 minutes.",
        f"/{slug}/",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Construction services</span>
      <h1>Construction services accountant in Brisbane</h1>
      <p class="hook">For fit-out, maintenance and installation businesses.</p>
      <p class="lead">Quoted hours against hours on site, with materials and subcontractors in the same picture as the bank. We do the tax, BAS, books and payroll.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="con-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/check.html" data-event="con-check">Free hours check</a>
      </div>
{trust_line()}
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
        f"/{slug}/",
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
        f"/{slug}/",
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
        f"/{slug}/",
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



def job_software():
    slug = "job-software-and-your-accountant"
    faqs = [
        (
            "Do you work inside my job management software?",
            "No. We work in Xero. Your job software already sends its invoices there, so we do not need a seat in it to read what happened. If you want someone to set up or run that system, you want an implementer, and we will tell you so.",
        ),
        (
            "So what do you do that it does not?",
            "We reconcile to the bank. Your job software knows the hours somebody entered. We see the money that actually arrived and the money that actually left, and we tell you how much of it is yours once GST, PAYG, super and wages come out.",
        ),
        (
            "What if my job software says the job made money?",
            "Then that is a good start. It is working from the hours that got entered. If an hour never got entered, the job looks better on the screen than it was in the week. That gap is what we read.",
        ),
    ]
    extra = jsonld(service_node(
        "Accounting for trade businesses running job management software",
        f"{ORIGIN}/{slug}/",
        "Your job software prices the job. We reconcile the bank, split out what is actually yours after GST, PAYG, super and wages, and hold tax and BAS.",
    )) + jsonld(faq_node(faqs))
    h = head(
        "You already have job software | Service Profit",
        "Your job software prices the job from the hours entered. We reconcile the bank and tell you what is actually yours after GST, PAYG, super and wages. Queensland.",
        f"/{slug}/",
        extra=extra,
    )
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Before you ask</span>
      <h1>You already have job software. So why an accountant?</h1>
      <p class="lead">Fair question, and it is usually the first one. The short answer is that your job software and your accountant are answering two different questions, and only one of them is the bank.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="software-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/check.html" data-event="software-check">Free hours check</a>
      </div>
      <div class="prose">
        <h2>Two different questions</h2>
        <p>Your job software answers this one: what should this job have cost, based on what was entered against it? That is a useful question and a good system answers it well.</p>
        <p>We answer a different one: what actually landed in the bank, how much of it is yours, and what does that say about the next quote? Those are not the same number, and the gap between them is the whole point of this page.</p>
        <h2>It only knows what somebody typed</h2>
        <p>A job costing screen is built from entered hours. If a second tech went back on the Friday and nobody logged it, the job reads as profitable. Nothing is wrong with the software. It simply was not told.</p>
        <p>We work from the bank and the file, so the hours that never got entered still show up as a gap between what you invoiced and what the week actually cost you.</p>
        <h2>We are not your software people</h2>
        <p>simPRO, ServiceM8, AroFlo and the rest all feed Xero. Xero is where we work. We are not your software people and we will not pretend to be. If you need that system set up, tuned or migrated, that is an implementer's job, not ours, and we will say so on the call rather than take the work.</p>
        <p>What we hold is the accounting: the bank reconciled, GST, PAYG, super and wages separated out so you know what you can actually spend, FBT watched in the file, and income tax and BAS held for one trading entity as written in the letter.</p>
        <h2>Who this page is for</h2>
        <p>Air con and refrigeration, electrical, or construction services businesses in Queensland who already run a job system and still could not say, today, which of last month's jobs made money once the bank had its say.</p>
        <p>Not a fit if what you actually want is someone to run the job software itself. That is a different trade to ours.</p>
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


HOOKS = {
    "services": "For air con, electrical and construction businesses.",
    "tax-agent-for-trades": "For air con, electrical and construction owners. Tax planned before 30 June.",
    "bas-and-gst-for-trades": "The GST is still in the bank when the BAS is due.",
    "payroll-for-trades": "Super now goes out with every pay. We run it.",
    "bookkeeping-and-xero-for-trades": "Xero that shows which jobs paid.",
    "accountant-brendale": "For air con, electrical and construction businesses across Queensland.",
}


def service_page(slug, title, desc, eyebrow, h1, lead, prose, faqs, service_name):
    """One service, same offer. Leanne's keyword list, said in trade language."""
    extra = jsonld(service_node(service_name, f"{ORIGIN}/{slug}/", desc)) + jsonld(faq_node(faqs))
    h = head(title, desc, f"/{slug}/", extra=extra)
    faq_html = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    body = f"""{nav("services" if slug == "services" else "")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="hook">{HOOKS[slug]}</p>
      <p class="lead">{lead}</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book.html" data-event="{slug}-book">Book 15 minutes</a>
        <a class="btn btn-outline" href="/pricing.html" data-event="{slug}-pricing">See the plans</a>
      </div>
{trust_line()}
      <div class="prose">
{prose}
      </div>
{same_offer()}
      <div class="faq">{faq_html}</div>
{trade_more(slug)}
    </div>
  </main>
{footer()}"""
    return slug, h + body


NOT_PERSONAL = (
    "Do you do personal tax returns?",
    "Service Profit is for businesses. If all you need is a personal return, we are not the right fit and we will say so on the call.",
)
CATCH_UP = (
    "What if I am behind?",
    "Catch-up work is quoted on its own, after we have seen the file. It is not inside the monthly plans.",
)


def services():
    return service_page(
        "services",
        "Accounting services for trades | Tax, BAS, payroll, Xero",
        "Accountant, tax agent, BAS, bookkeeping, payroll and Xero setup for air con, electrical and construction businesses. Pink Accounting, Brendale, Queensland.",
        "Services",
        "Accounting, tax and bookkeeping services for trades",
        "Tax, BAS, bookkeeping, payroll and the numbers that show which jobs paid. One firm, one file, a registered tax agent.",
        """        <h2>Business accounting and job profit</h2>
        <p>The core of Service Profit. Every Monday: hours quoted against hours on the tools, and how much of the bank is yours once GST, PAYG, super and wages come out. <a href="/system.html">See what lands on Monday</a>.</p>
        <h2>Tax agent and income tax returns</h2>
        <p>The business return, the financial statements behind it and the FBT return, prepared and lodged by a registered tax agent. <a href="/tax-agent-for-trades/">Tax agent for trades</a>.</p>
        <h2>Tax planning</h2>
        <p>We look at the year in May, while there is still time to act, not in August when the bill is already set. <a href="/tax-agent-for-trades/#planning">How tax planning works here</a>.</p>
        <h2>BAS and GST</h2>
        <p>Activity statements prepared and lodged, with GST and PAYG kept apart from your cash all quarter. <a href="/bas-and-gst-for-trades/">BAS and GST for trades</a>.</p>
        <h2>Bookkeeping</h2>
        <p>The bank reconciled in Xero, supplier bills matched, receipts attached. <a href="/bookkeeping-and-xero-for-trades/">Bookkeeping for trades</a>.</p>
        <h2>Xero setup</h2>
        <p>Accounts that split labour, materials and subcontractors, bank feeds on, job software feeding in once. <a href="/bookkeeping-and-xero-for-trades/#xero">Xero setup for trades</a>.</p>
        <h2>Payroll and super</h2>
        <p>Pay runs, Single Touch Payroll and Payday Super, with apprentices and subcontractors counted at their true cost. <a href="/payroll-for-trades/">Payroll for trades</a>.</p>
        <h2>Business advisory</h2>
        <p>Advice here means the numbers behind a real decision: can you afford another technician, can you draw more, should you hold cash for the tax. <a href="/can-i-afford-another-technician/">Can I afford another technician?</a> A written forecast sits in the Ready to Scale plan.</p>
        <h2>Where we are</h2>
        <p>Shop 15A, 18-22 Kremzow Rd, Brendale. For trade businesses across Queensland. <a href="/accountant-brendale/">Accountant in Brendale</a>.</p>""",
        [
            (
                "Do I have to take all of these?",
                "No. Compliance at $550 + GST a month covers income tax, FBT, financial statements, BAS and GST from a file already in order. Job Profit adds the job and cash look. Bookkeeping is an add-on from $500 + GST a month.",
            ),
            NOT_PERSONAL,
        ],
        "Accounting, tax, BAS, bookkeeping and payroll for trade businesses",
    )


def tax_agent():
    return service_page(
        "tax-agent-for-trades",
        "Tax agent Brendale and Brisbane | Tax returns, tax planning",
        "Registered tax agent for air con, electrical and construction businesses in Queensland. Income tax, tax planning, FBT, TPAR and financial statements.",
        "Tax agent",
        "Tax agent in Brendale for tax returns and tax planning",
        "We prepare and lodge the business return, the financial statements and the FBT return. Registered tax agent 26284368, on the TPB register.",
        """        <h2>Income tax returns for the business</h2>
        <p>Whatever structure the business trades through, the return is built from a reconciled file, not a box of receipts in July. One trading entity is included unless the letter says otherwise.</p>
        <h2 id="planning">Tax planning before 30 June</h2>
        <p>A good year on the tools can turn into a hard August. We look at the year to date in May, while there is still time to act: what the tax is likely to be, what has already been set aside, and what a purchase would or would not change. A ute bought in June to save tax is still a ute you have to pay for. The letter says whether planning sits inside your plan.</p>
        <h2>Utes, vans and FBT</h2>
        <p>Work vehicles, phones and tools sit across income tax and FBT. Some utes are exempt from FBT when private use is limited to travel between home and work and other minor, infrequent and irregular trips. Some are not. We read the log and the use, not the badge.</p>
        <h2>TPAR, if you pay subcontractors</h2>
        <p>If building and construction services make up 10% or more of your GST turnover and you pay contractors for that work, the ATO expects a taxable payments annual report by 28 August. Electrical, air con and fit-out businesses often fall in. We check whether yours does, and the letter says whether lodging it is inside your plan.</p>
        <h2>Who this page is for</h2>
        <p>Trade businesses in Queensland that want the return lodged by the same people who hold the books. If you only need the annual return, that is Compliance at $550 + GST a month, and we will say so on the call.</p>""",
        [
            (
                "Are you a registered tax agent?",
                "Yes. Pink Accounting &amp; Tax Solutions Pty Ltd, Registered Tax Agent 26284368. You can check the TPB public register yourself.",
            ),
            CATCH_UP,
            NOT_PERSONAL,
        ],
        "Tax agent for trade businesses, Queensland",
    )


def bas_gst():
    return service_page(
        "bas-and-gst-for-trades",
        "BAS and GST services Brendale | Registered tax agent",
        "BAS, GST and PAYG for air con, electrical and construction businesses in Queensland, lodged by a registered tax agent. GST held before the due date.",
        "BAS and GST",
        "BAS and GST services in Brendale",
        "We prepare and lodge the BAS. GST, PAYG and super stay apart from the cash that is yours, all quarter.",
        """        <h2>BAS services come with the tax agent registration</h2>
        <p>Pink Accounting is a registered tax agent. Under the Tax Practitioners Board rules that registration covers BAS services, so we prepare and lodge activity statements ourselves. You will not find us listed as a separate BAS agent because we do not need to be.</p>
        <h2>GST on deposits, progress claims and materials</h2>
        <p>Trade work bills in pieces: a deposit, a progress claim, a variation, the final invoice. Materials go on the card before the customer pays. If the business reports GST on an accruals basis, GST can be owed before the money arrives. We check which basis you report on and match the BAS to it.</p>
        <h2>PAYG withholding and instalments</h2>
        <p>If you have staff, the PAYG withheld from their pay goes on the BAS. If the business pays PAYG instalments, those sit there too. None of it is yours, even while it sits in your account. <a href="/cash-that-is-yours/">Cash that is yours</a>.</p>
        <h2>Who this page is for</h2>
        <p>Air con, electrical and construction services businesses in Queensland that lodge a BAS and want the cash for it held, not found. BAS and GST are inside every plan, from Compliance at $550 + GST a month.</p>""",
        [
            (
                "Are you a BAS agent?",
                "We are a registered tax agent, number 26284368. That registration covers BAS services, so we prepare and lodge your BAS without a separate BAS agent listing.",
            ),
            (
                "Can you do a monthly BAS?",
                "Yes, if the business reports monthly. Most small businesses report quarterly. We lodge on the cycle the ATO has you on.",
            ),
            CATCH_UP,
        ],
        "BAS and GST for trade businesses, Queensland",
    )


def payroll():
    return service_page(
        "payroll-for-trades",
        "Payroll services Brendale and Brisbane | STP and super",
        "Payroll, Single Touch Payroll and Payday Super for air con, electrical and construction businesses in Queensland. Apprentices and contractors costed properly.",
        "Payroll",
        "Payroll services in Brendale: pay runs, STP and super",
        "Pay runs, Single Touch Payroll and super, done in Xero by a registered tax agent. Since 1 July 2026 super is paid with every pay.",
        """        <h2>Payday Super changed the rhythm</h2>
        <p>From 1 July 2026 employers pay super guarantee with each pay, at 12% of qualifying earnings, and the fund has to receive it within seven business days. Quarterly super payments are gone, and so is the Small Business Superannuation Clearing House, which closed on 1 July 2026. We run super on the pay cycle so it lands on time.</p>
        <h2>Single Touch Payroll</h2>
        <p>Every pay run is reported to the ATO through Single Touch Payroll from Xero. End of year finalisation is part of the job, so your people's income statements are ready when they need them.</p>
        <h2>Apprentices, staff and subcontractors</h2>
        <p>An apprentice costs more than the hourly rate, and a subcontractor who works like staff can bring super and payroll obligations with them. We show the true cost in the file. Award rates and contracts come from Fair Work, not from us. The Fair Work Ombudsman's pay calculator is the place to check a rate. <a href="/can-i-afford-another-technician/">Can I afford another technician?</a></p>
        <h2>How payroll is priced</h2>
        <p>Payroll is not inside the monthly plans. Like bookkeeping, it is quoted in the letter when you actually need it.</p>""",
        [
            (
                "Do you use Xero Payroll?",
                "Yes. We work in Xero, so pay runs, Single Touch Payroll and super all sit in the same file as the bank and the BAS.",
            ),
            (
                "What about WorkCover?",
                "In Queensland, workers compensation is through WorkCover Queensland. We keep the wages figures it asks for in the file. The policy stays yours.",
            ),
            CATCH_UP,
        ],
        "Payroll and super for trade businesses, Queensland",
    )


def bookkeeping_xero():
    return service_page(
        "bookkeeping-and-xero-for-trades",
        "Bookkeeper Brendale | Bookkeeping and Xero setup",
        "Bookkeeping and Xero setup for air con, electrical and construction businesses in Queensland. Bank reconciled, job software feeding Xero. Brendale.",
        "Bookkeeping and Xero",
        "Bookkeeper in Brendale: bookkeeping and Xero setup",
        "The bank reconciled in Xero, supplier bills matched and your job software feeding in cleanly. So you can see which jobs paid.",
        """        <h2>Bookkeeping that ends in a reconciled bank</h2>
        <p>Every bank line matched to an invoice, a bill or a pay run. Supplier statements checked against the bills. Card receipts attached. The test is simple: the bank in Xero agrees with the bank.</p>
        <h2 id="checked">How the books are checked before a BAS is lodged</h2>
        <p>Our method is a two-person check. One person works through the period. A second person, who did not do that work, reviews it in live Xero before it is signed off. Anything they disagree on goes back and is fixed in Xero, not explained away.</p>
        <ul><li>The bank in Xero is agreed to your bank statement</li><li>Wholesaler and subcontractor accounts are agreed to their own statements, or the difference is named</li><li>Pay runs are traced through STP, the bank and the super fund</li><li>The BAS figures are agreed to the file and to what was lodged before</li><li>Opening balances are checked against last year's finished figures</li></ul>
        <p>The principal reviews the BAS or tax return before it is lodged.</p>
        <h2 id="xero">Xero setup for a trade business</h2>
        <p>A chart of accounts that splits labour, materials and subcontractors. Bank feeds on. Tracking by trade or crew where it helps. Your job software connected so invoices land once, not twice. If you are moving from another accounting system, the opening balances are mapped before anything is switched off.</p>
        <h2>Your job software feeds Xero. We work in Xero.</h2>
        <p>We set up Xero. We do not set up or run your job software; that is an implementer's job, and we will say so. <a href="/job-software-and-your-accountant/">You already have job software</a>.</p>
        <h2>How bookkeeping is priced</h2>
        <p>Bookkeeping is an add-on from $500 + GST a month, quoted in the letter when it is actually needed. Xero setup is quoted once, after we have seen what you have.</p>""",
        [
            (
                "Are you a bookkeeper or an accountant?",
                "Both, under one roof. Pink Accounting is a registered tax agent, and the bookkeeping and the tax sit in the same file with the same firm.",
            ),
            (
                "Can I keep doing my own bookkeeping?",
                "Yes. If the file is in order each month, Compliance or Job Profit runs without the bookkeeping add-on. We will tell you on the call which it is.",
            ),
            CATCH_UP,
        ],
        "Bookkeeping and Xero setup for trade businesses, Queensland",
    )


def brendale():
    return service_page(
        "accountant-brendale",
        "Accountant Brendale QLD 4500 | Pink Accounting",
        "Accountant and registered tax agent at Shop 15A, 18-22 Kremzow Rd, Brendale, for air con, electrical and construction businesses across Queensland.",
        "Brendale",
        "Accountant in Brendale",
        'Shop 15A, 18-22 Kremzow Rd, Brendale QLD 4500. Call <a href="tel:+61735446386">(07) 3544 6386</a> or book 15 minutes.',
        f"""        <h2>Come in, or stay on the job</h2>
        <p>Office hours are {ID["office"]["hours"]["display"]}. 15-minute calls run Monday to Thursday. Most of the work does not need you to leave site: the file is in Xero, the first call is 15 minutes, and the Monday numbers come to you.</p>
        <h2>Moreton Bay, north Brisbane and the rest of Queensland</h2>
        <p>Strathpine, Lawnton, Bray Park, Albany Creek, Warner, Petrie, Kallangur and North Lakes are close enough to meet at the office. Further out, the work runs the same way by phone and Xero. Service Profit takes trade businesses anywhere in Queensland.</p>
        <h2>What we do from Brendale</h2>
        <p><a href="/tax-agent-for-trades/">Tax returns and tax planning</a> · <a href="/bas-and-gst-for-trades/">BAS and GST</a> · <a href="/bookkeeping-and-xero-for-trades/">Bookkeeping and Xero setup</a> · <a href="/payroll-for-trades/">Payroll and super</a> · <a href="/system.html">Job profit every Monday</a> · <a href="/services/">All services</a></p>
        <h2>Who this page is for</h2>
        <p>Air con and refrigeration, electrical, and construction services businesses with people on the tools, who want their accountant close by and their numbers weekly.</p>""",
        [
            (
                "Do I have to be in Brendale?",
                "No. Service Profit is for air con, electrical and construction services businesses anywhere in Queensland. Brendale is where the office is.",
            ),
            (
                "Can I meet you at the office?",
                "Yes. Book the 15-minute call first. If it makes sense to meet, we set a time at Kremzow Rd.",
            ),
        ],
        "Accountant in Brendale for trade businesses",
    )


PAGES = (
    air_con, electrical, construction, quoted_hours, cash_yours, another_tech, job_software,
    services, tax_agent, bas_gst, payroll, bookkeeping_xero, brendale,
)
