from pathlib import Path
from shared import BOOK, GBP, MSBOOK, ORIGIN, footer, head, nav, sticky

ROOT = Path(__file__).resolve().parents[1]


def write(name, html):
    path = ROOT / name
    path.write_text(html, encoding="utf-8")
    print("wrote", name, path.stat().st_size)


JSONLD = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"AccountingService","name":"Pink Accounting","alternateName":"Service Profit","url":"https://www.serviceprofit.com.au/","telephone":"+61735446386","email":"admin@pinktax.com.au","knowsAbout":["HVAC accounting","electrical contractors","construction services"],"address":{"@type":"PostalAddress","streetAddress":"Shop 15A, 18-22 Kremzow Rd","addressLocality":"Brendale","addressRegion":"QLD","postalCode":"4500","addressCountry":"AU"},"areaServed":{"@type":"AdministrativeArea","name":"Queensland"},"founder":{"@type":"Person","name":"Huong Bui"},"taxID":"51682301891"}
  </script>
"""


def index():
    h = head(
        "Service Profit | Pink Accounting for HVAC, electrical and construction services",
        "Pink Accounting for HVAC, electrical and construction service businesses in Queensland. Job Profit $1,650 + GST a month. Book a 15-minute call.",
        "/",
    ).replace("</head>", JSONLD + "</head>")
    body = f"""{nav("home")}
  <main id="main">
    <section class="hero">
      <div class="wrap">
        <div>
          <p class="kicker">A Pink Accounting service · Queensland</p>
          <h1>See job profit while you can still change the next quote.</h1>
          <p class="lead">We keep the books current for HVAC, electrical and construction service businesses, then read labour, materials and cash against the job. A year-end P&amp;L cannot fix a quote you already sent.</p>
          <div class="cta">
            <a class="btn btn-primary" href="book.html" data-event="hero-book">Book a 15-minute call <span class="arw">→</span></a>
            <a class="btn btn-outline" href="system.html">How the system works</a>
          </div>
          <p class="kicker" style="margin-top:28px">Choose a trade for a one-line example. Pricing and booking stay the same.</p>
          <div class="trades" aria-label="Trade examples">
            <button class="trade is-on" type="button" data-trade="hvac" aria-pressed="true">HVAC</button>
            <button class="trade" type="button" data-trade="electrical" aria-pressed="false">Electrical</button>
            <button class="trade" type="button" data-trade="construction" aria-pressed="false">Construction services</button>
          </div>
          <p class="live" id="liveLine">For HVAC firms we watch labour against the quoted hours, materials on the van, and whether a call-out actually covered the next tax bill.</p>
          <p class="trade-links">Read more: <a href="hvac.html">HVAC</a><a href="electrical.html">Electrical</a><a href="construction.html">Construction services</a></p>
          <div class="trust">
            <span><a href="{GBP}" rel="noopener">Google reviews</a> for Pink Accounting</span>
            <span class="sep"></span><span>Registered Tax Agent 26284368</span>
          </div>
          <div class="under">Pink Accounting &amp; Tax Solutions Pty Ltd · Queensland</div>
        </div>
        <div class="stage" id="stage">
          <picture>
            <source type="image/webp" srcset="assets/hvac-480.webp 480w, assets/hvac-864.webp 864w, assets/hvac-1200.webp 1200w" sizes="(max-width:940px) 100vw, 55vw">
            <img class="is-on" data-trade="hvac" src="assets/hvac.jpg" width="864" height="1152" alt="Commercial HVAC plant">
          </picture>
          <picture>
            <source type="image/webp" srcset="assets/electrical-480.webp 480w, assets/electrical-864.webp 864w, assets/electrical-1200.webp 1200w" sizes="(max-width:940px) 100vw, 55vw">
            <img data-trade="electrical" src="assets/electrical.jpg" width="864" height="1152" alt="Commercial electrical services" loading="lazy" aria-hidden="true" inert>
          </picture>
          <picture>
            <source type="image/webp" srcset="assets/construction-480.webp 480w, assets/construction-864.webp 864w, assets/construction-1200.webp 1200w" sizes="(max-width:940px) 100vw, 55vw">
            <img data-trade="construction" src="assets/construction.jpg" width="864" height="1152" alt="Construction services fit-out" loading="lazy" aria-hidden="true" inert>
          </picture>
          <div class="cap" id="stageCap">HVAC</div>
        </div>
      </div>
    </section>

    <section class="problem">
      <div class="wrap">
        <span class="eyebrow">Why this exists</span>
        <h2 style="margin-top:14px">Tax is the end result of decisions made months earlier.</h2>
        <p class="lead">If the first close look at a job is when the return is prepared, the file can still be right. The chance to price the next one better has often already passed. That gap shows up in quotes, labour, subcontractors and cash.</p>
        <div class="pcols">
          <div class="pcol"><div class="n">01</div><h3>The return is last</h3><p>It tells you what happened after the job was quoted, the van was on site, and the subcontractor was paid.</p></div>
          <div class="pcol"><div class="n">02</div><h3>Busy is not the same as profitable</h3><p>A full diary can still hide a job that did not cover labour, materials or the next tax bill.</p></div>
          <div class="pcol"><div class="n">03</div><h3>Somebody should be in the file during the year</h3><p>We keep the books current, so when a job or cash question comes up we can talk while there is still time.</p></div>
        </div>
      </div>
    </section>

    <section class="band" id="pricing">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">The plans</span>
          <h2>Same firm. A defined monthly scope.</h2>
          <p>Monthly, ex GST, for technical service businesses in Queensland. Each higher plan includes the plan below it. The fee is not unlimited work. Extra work is quoted before we start it.</p>
        </div>
        <div class="feat" id="job-profit">
          <div>
            <span class="badge">Typical ongoing plan</span>
            <h3>Job Profit</h3>
            <div class="fprice">$1,650<small> + GST / month</small></div>
            <p class="fdesc">Books and compliance stay current. Each week we look at jobs and cash inside the file. If something is off, we raise it. You get a note when a decision is needed. There is no standing monthly meeting.</p>
            <div class="fcta"><a class="btn btn-primary" href="book.html" data-event="pricing-book">Book a 15-minute call <span class="arw">→</span></a></div>
            <div class="fnote">If a lighter tier is enough, we will say so on the call.</div>
          </div>
          <ul>
            <li><b>Includes Compliance and Bookkeeping</b> for one trading entity, as written in the letter</li>
            <li><b>Weekly internal look</b> at jobs, labour, materials, subcontractors and cash. The firm raises exceptions. You do not have to chase us to start that look</li>
            <li><b>What you receive</b> a WhatsApp or email when something needs a decision, plus the current books and BAS oversight</li>
            <li><b>What we need from you</b> Xero access, bank feeds, invoices, and labour or materials against jobs. If costs are not on jobs, job profit is an estimate until they are</li>
          </ul>
        </div>
        <div class="tiers">
          <a class="tier" href="#level-compliance">
            <div class="tname">Compliance</div>
            <div class="tprice">$550<small> + GST/mo</small></div>
            <p>Tax, BAS oversight and the return for one entity, while you keep more of the day-to-day.</p>
          </a>
          <a class="tier" href="#level-bookkeeping">
            <div class="tname">Bookkeeping</div>
            <div class="tprice">+$500<small> + GST/mo, from</small></div>
            <p>Add-on to Compliance. We keep the books current. Starts from $500 + GST.</p>
          </a>
          <a class="tier" href="#level-weekly">
            <div class="tname">Weekly Visibility</div>
            <div class="tprice">$2,650<small> + GST/mo, from</small></div>
            <p>Includes Job Profit, plus a weekly snapshot while the job is still running.</p>
          </a>
          <a class="tier" href="#level-scale">
            <div class="tname">Ready to Scale</div>
            <div class="tprice">$3,500<small> + GST/mo, from</small></div>
            <p>Includes Weekly Visibility, plus forecasting written into the letter. Application only.</p>
          </a>
        </div>
        <p class="psub">Compliance plus the minimum Bookkeeping add-on is $1,050 + GST. Job Profit is $1,650 + GST. The extra $600 is the weekly internal look, the firm raising job and cash exceptions, and WhatsApp. Bookkeeping volume, payroll headcount and catch-up of old periods can change the fee. The letter is the quote.</p>
        <div class="table-scroll" tabindex="0" aria-label="Plan comparison. Scroll sideways on a small screen to read every column.">
          <table class="scope">
            <thead>
              <tr><th>Level</th><th>Fee</th><th>Included</th><th>Not included</th></tr>
            </thead>
            <tbody>
              <tr id="level-compliance">
                <td><strong>Compliance</strong></td>
                <td class="price">$550 + GST</td>
                <td>Tax planning, BAS oversight and the annual return for one trading entity. Email to admin@pinktax.com.au. Ordinary hours reply: next working day.</td>
                <td>Full bookkeeping. WhatsApp. Weekly job reads. Catch-up of prior periods. Xero subscription unless the letter says we bill it. Unlimited advisory.</td>
              </tr>
              <tr id="level-bookkeeping">
                <td><strong>Bookkeeping</strong></td>
                <td class="price">from +$500 + GST</td>
                <td>Adds current books to Compliance. Bank, suppliers, payroll and GST coded in Xero. Starting price; volume can lift it.</td>
                <td>Job-and-cash exception review as a standing service. WhatsApp. Unlimited advisory.</td>
              </tr>
              <tr class="pop" id="level-job">
                <td><strong>Job Profit</strong></td>
                <td class="price">$1,650 + GST</td>
                <td>Includes Compliance and Bookkeeping. Weekly internal look. We raise job and cash exceptions. WhatsApp. One entity. Payroll where you have staff, as written.</td>
                <td>A monthly meeting. Unlimited access. Catch-up. Software setup projects. Work outside the letter.</td>
              </tr>
              <tr id="level-weekly">
                <td><strong>Weekly Visibility</strong></td>
                <td class="price">from $2,650 + GST</td>
                <td>Includes Job Profit. A weekly snapshot you can read while the job is still running.</td>
                <td>Open-ended project work unless scoped. Application of extra entities unless written in.</td>
              </tr>
              <tr id="level-scale">
                <td><strong>Ready to Scale</strong></td>
                <td class="price">from $3,500 + GST</td>
                <td>Includes Weekly Visibility. Forecasting and decision support as written in the letter first. Application only.</td>
                <td>A guaranteed result. Unlimited access.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="table-hint">On a phone, swipe the table sideways, or use the stacked cards below on the narrow layout.</p>
        <div class="scope-cards">
          <article class="scope-card" id="card-compliance"><h3>Compliance</h3><div class="price">$550 + GST / month</div><p><b>Included:</b> tax planning, BAS oversight and the annual return for one entity. Email only.</p><p><b>Not included:</b> full bookkeeping, WhatsApp, weekly job reads, catch-up, Xero subscription unless billed in the letter.</p></article>
          <article class="scope-card"><h3>Bookkeeping</h3><div class="price">from +$500 + GST / month</div><p><b>Included:</b> current books added to Compliance.</p><p><b>Not included:</b> standing job-and-cash review, WhatsApp.</p></article>
          <article class="scope-card"><h3>Job Profit</h3><div class="price">$1,650 + GST / month</div><p><b>Included:</b> Compliance and Bookkeeping, weekly internal look, exceptions raised by us, WhatsApp.</p><p><b>Not included:</b> a monthly meeting, unlimited access, catch-up, software setup projects.</p></article>
          <article class="scope-card"><h3>Weekly Visibility</h3><div class="price">from $2,650 + GST / month</div><p><b>Included:</b> Job Profit plus a weekly snapshot while the job is running.</p><p><b>Not included:</b> unscoped project work.</p></article>
          <article class="scope-card"><h3>Ready to Scale</h3><div class="price">from $3,500 + GST / month</div><p><b>Included:</b> Weekly Visibility plus forecasting written into the letter. Application only.</p><p><b>Not included:</b> a guaranteed result.</p></article>
        </div>
      </div>
    </section>

    <section class="band band-bone">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">How it works</span>
          <h2>We agree the start date and the boundary before you sign.</h2>
          <p>Pink Accounting is the firm. Service Profit is how we work with technical service businesses in Queensland. We do not manufacture tax savings. We look early enough to name something worth discussing.</p>
        </div>
        <div class="steps">
          <div class="stepc"><div class="n">01</div><h3>Fifteen minutes</h3><p>A direct conversation about how the business runs. If we are not the right firm, we say so.</p></div>
          <div class="stepc"><div class="n">02</div><h3>The right level, written down</h3><p>Exact fee in the letter of engagement before work begins. Once scope is agreed we usually issue the letter the same working day.</p></div>
          <div class="stepc"><div class="n">03</div><h3>The system goes live</h3><p>Books stay current from the start date in the letter. We look at the file each week on Job Profit and above, and we raise what needs a decision.</p></div>
        </div>
        <div class="funnel">
          <a class="card" href="book.html" data-event="funnel-book"><span class="eyebrow">Book</span><h2>15-minute call</h2><p>Use the booking page. The calendar is the Service Profit service, not the hospitality diary.</p></a>
          <a class="card" href="mailto:admin@pinktax.com.au?subject=Service%20Profit%20enquiry" data-event="funnel-email"><span class="eyebrow">Email</span><h2>admin@pinktax.com.au</h2><p>The firm mailbox. A person reads it.</p></a>
          <a class="card" href="tel:+61735446386" data-event="funnel-call"><span class="eyebrow">Call</span><h2>07 3544 6386</h2><p>Mon-Fri 9:00am-4:30pm. Saturday by appointment. Brendale QLD.</p></a>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap meet">
        <div class="shot">
          <div class="frame" role="img" aria-label="Huong Bui, principal of Pink Accounting"></div>
        </div>
        <div>
          <span class="eyebrow">Meet Pink</span>
          <h2 style="margin-top:12px">Hello, I am Pink.</h2>
          <p>I am Huong Bui. I founded Pink Accounting in 2020. Service Profit is our work with HVAC, electrical and construction service businesses in Queensland: full diaries, tight cash, and a year-end pack that arrives too late to change a job already quoted.</p>
          <p>You deal with the principal on the discovery call where the diary allows. The firm is small on purpose. If I am already in a client meeting, another member of the team takes the call and I read the notes the same working day.</p>
          <div class="creds">Registered Tax Agent 26284368 · MIPA / AFA · Master of Professional Accounting (Griffith)</div>
          <a class="btn btn-primary" href="why.html">Why Pink Accounting</a>
        </div>
      </div>
    </section>

    <section class="final">
      <div class="wrap">
        <h2>Have a look first. Then we can look properly at the file.</h2>
        <p>Compare us with other firms if you need to. The useful test is whether the scope, fee and what you must send us are a fit.</p>
        <a class="btn btn-white" href="book.html" data-event="final-book">Book a 15-minute call <span class="arw">→</span></a>
        <div class="micro">Registered Tax Agent 26284368 · Business clients only · Queensland</div>
      </div>
    </section>
  </main>
{sticky()}
{footer()}"""
    return h + body


def system():
    h = head(
        "The system | Service Profit | Pink Accounting",
        "How Pink Accounting works with HVAC, electrical and construction service businesses in Queensland: current books, jobs, cash, tax and BAS.",
        "/system.html",
    )
    body = f"""{nav("system")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">The system</span>
      <h1>Numbers read in time to act.</h1>
      <p class="lead">Clean bookkeeping and compliance, with job and cash raised when the file shows a problem. Built for HVAC, electrical and construction services in Queensland.</p>
      <div class="cta">
        <a class="btn btn-primary" href="book.html" data-event="system-book">Book a 15-minute call <span class="arw">→</span></a>
        <a class="btn btn-outline" href="index.html#pricing">See the service levels</a>
      </div>
      <div class="grid3">
        <section class="card"><span class="eyebrow">01 · Books</span><h2>Clean source numbers</h2><p>Bank, suppliers, jobs, materials and subcontractor payments coded so the file is ready for decisions, not reconstructed at year end.</p></section>
        <section class="card"><span class="eyebrow">02 · People</span><h2>Labour and subcontractors seen clearly</h2><p>Payroll and super where you have staff. Subcontractors left visible, not mixed into a lump that only makes sense in June.</p></section>
        <section class="card"><span class="eyebrow">03 · Jobs</span><h2>Quote versus actual, when it matters</h2><p>On Job Profit and above we look at the file each week. If labour, materials or cash is off, we raise it. You get a note. There is no monthly performance.</p></section>
      </div>
      <div class="prose" style="margin-top:48px">
        <h2>Who this is for</h2>
        <p>Technical service businesses in Queensland: air conditioning and refrigeration, electrical contracting, and construction services. Construction services means contracted fit-out, maintenance, installation and similar job work. It does not mean building houses or commercial buildings as a builder. It is not the hospitality service line.</p>
        <h2>What job profit actually needs</h2>
        <p>Ordinary bookkeeping does not, by itself, produce a reliable profit per job. Job profit needs labour, materials and subcontractors on the job, plus a view of unfinished work. We work in Xero. If your job list lives in another system, we use an export or a job report you already keep. We do not claim a live integration with every field app. If costs are not assigned to jobs, we will say the figure is an estimate and quote any setup as a separate piece of work.</p>
        <h2>What the monthly fee covers</h2>
        <p>Each level has a defined scope. Higher plans include the plans below them. WhatsApp is for Job Profit and above. We aim to reply the next working day, Monday to Friday 9:00am to 4:30pm. That is not a 24-hour promise and not several working days.</p>
        <div class="example">
          <div class="label">Illustrative example · not a client result</div>
          <p>A quoted 6-hour call-out runs 9 hours. Materials go out at cost. The extra labour never goes back into the next quote. The books can still be right. The next job stays underpriced until someone reads labour against the quote during the month.</p>
        </div>
        <h2>Questions we hear before people sign</h2>
      </div>
      <div class="faq">
        <details><summary>What happens in the first month?</summary><p>You give Xero, bank and payroll access, or send the source documents. We confirm the start date in the letter. From that date the books are kept current. Catch-up of earlier periods is a separate fee, quoted first.</p></details>
        <details><summary>Can you take over from another accountant?</summary><p>Yes. We start from the agreed date. We do not silently rebuild last year unless catch-up is in the letter.</p></details>
        <details><summary>What do I still have to do?</summary><p>Send invoices, bills, timesheets or job costs, or give us access to the systems that already hold them. We cannot invent missing source data.</p></details>
        <details><summary>How do I cancel?</summary><p>The letter of engagement sets the term and how to end it. We will not hide that in marketing copy. Ask for it on the call if you want the wording before you book.</p></details>
        <details><summary>Do you work outside Queensland?</summary><p>Service Profit is a Queensland service line. Hospitality work on pinktax.com.au stays Australia-wide. The two are not mixed.</p></details>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def why():
    h = head(
        "Meet Pink | Service Profit | Pink Accounting",
        "Huong Bui founded Pink Accounting in 2020. Service Profit is the Pink Accounting work with HVAC, electrical and construction service businesses in Queensland.",
        "/why.html",
    )
    body = f"""{nav("why")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Pink Accounting</span>
      <h1>One firm. Service Profit is how we work with you.</h1>
      <div class="prose">
        <p>Service Profit is not a separate company. It is Pink Accounting for HVAC, electrical and construction service businesses in Queensland. It is not hospitality, and it is not for builders putting up houses or commercial buildings.</p>
        <h2>A system, not a once-a-year pack</h2>
        <p>Your file runs on documented coding rules, GST logic and review gates. The work is checked against the source. Tax still happens. It is not the only conversation.</p>
        <h2>Honest tiering</h2>
        <p>If compliance at $550 is all you need, that is what we will recommend. Each level has a boundary. That is so the fee matches the work.</p>
        <h2>Who is a fit</h2>
        <p>Owners who want current books and someone in the file during the year. People who will send job costs, or already keep them. A comparison of fees is reasonable. We will also say if the work you want is outside the letter.</p>
        <h2>Registered and accountable</h2>
        <p>Registered Tax Agent 26284368. Our obligations to you are public. See <a href="rights.html">Your rights and our obligations</a>.</p>
        <h2>How Pink started</h2>
        <p>Pink Accounting was founded in 2020 by Huong (Pinky) Bui. The practice incorporated as Pink Accounting &amp; Tax Solutions Pty Ltd in November 2024, which is why the current ABN shows a 2024 start date. The work began in 2020.</p>
        <p>Huong holds a Master of Professional Accounting (Griffith), is MIPA AFA, and is Registered Tax Agent 26284368. Discovery calls are with the principal where the diary allows. If she is already booked, a team member takes the call and she reads the notes the same working day.</p>
      </div>
      <div class="cta" style="margin-top:32px">
        <a class="btn btn-primary" href="book.html" data-event="why-book">Book a 15-minute call <span class="arw">→</span></a>
      </div>
      <p class="creds">ABN 51 682 301 891 · Registered Tax Agent 26284368 · ASIC Registered Agent 52580</p>
    </div>
  </main>
{footer()}"""
    return h + body


def book():
    h = head(
        "Book a 15-minute call | Service Profit | Pink Accounting",
        "Book a 15-minute Service Profit call with Pink Accounting. Queensland HVAC, electrical and construction services. Confirmation to you and to admin@pinktax.com.au.",
        "/book.html",
    )
    body = f"""{nav("book")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Service Profit</span>
      <h1>Book a 15-minute call</h1>
      <p class="lead">This call is for HVAC, electrical and construction service businesses in Queensland. It is not a hospitality or venue call. Bring how the business runs, the software you use, and what you want from the file. You do not need a street address for a discovery call.</p>
      <div class="prose">
        <h2>Who you will speak with</h2>
        <p>The booking is with Pink Accounting. Huong (Pink) takes the call when she is free. The calendar may show Anyone because the firm covers the slot. If a team member takes it, Pink reads the notes the same working day. That is team-led delivery with principal review, not a promise that every slot is only her.</p>
        <h2>When the first slot appears</h2>
        <p>The first open time is often a few working days out. That is ordinary diary lead time, not a permanent delay. If none of the times suit, email or call and we will find another slot.</p>
        <h2>What happens after you book</h2>
        <p>Microsoft Bookings sends a confirmation to you. A copy goes to admin@pinktax.com.au. That is the firm mailbox. We have not treated a click on this page as a completed enquiry.</p>
      </div>
      <div class="cta">
        <a class="btn btn-primary" href="{MSBOOK}" rel="noopener" data-event="book-calendar">Open the Service Profit calendar <span class="arw">→</span></a>
        <a class="btn btn-outline" href="mailto:admin@pinktax.com.au?subject=Service%20Profit%20enquiry" data-event="book-email">Email admin@pinktax.com.au</a>
        <a class="btn btn-outline" href="tel:+61735446386" data-event="book-call">Call 07 3544 6386</a>
      </div>
      <p class="creds">By booking you agree to our <a href="terms.html">terms</a> and <a href="privacy.html">privacy</a> pages. Pink Accounting &amp; Tax Solutions Pty Ltd · Shop 15A, 18-22 Kremzow Rd, Brendale QLD 4500 · Registered Tax Agent 26284368</p>
    </div>
  </main>
{footer()}"""
    return h + body


def contact():
    h = head(
        "Contact | Service Profit | Pink Accounting",
        "Talk to Pink Accounting. Brendale office. 07 3544 6386. admin@pinktax.com.au. Book a 15-minute Service Profit call.",
        "/contact.html",
    )
    body = f"""{nav("contact")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Contact Pink Accounting</span>
      <h1>Talk to the accountant. Not a ticket queue.</h1>
      <p class="lead">Bring the question, the messy numbers, or the decision you are about to make.</p>
      <div class="cta">
        <a class="btn btn-primary" href="book.html" data-event="contact-book">Book a 15-minute call <span class="arw">→</span></a>
        <a class="btn btn-outline" href="tel:+61735446386">Call 07 3544 6386</a>
      </div>
      <div class="grid3">
        <section class="card"><span class="eyebrow">Phone</span><h2><a href="tel:+61735446386">07 3544 6386</a></h2><p>Mon-Fri, 9:00am-4:30pm. Saturday by appointment.</p></section>
        <section class="card"><span class="eyebrow">Email</span><h2><a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a></h2><p>The firm mailbox. A person reads it.</p></section>
        <section class="card"><span class="eyebrow">Visit</span><h2>Brendale</h2><p>Shop 15A, 18-22 Kremzow Rd, Brendale QLD 4500. Service Profit is Queensland. Hospitality clients of the same firm may sit elsewhere.</p></section>
      </div>
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
        <p>Pink Accounting &amp; Tax Solutions Pty Ltd (ABN 51 682 301 891) handles personal information under the Privacy Act 1988. Service Profit is a service of this firm. This page applies to the whole practice. Last reviewed 10 September 2026.</p>
        <h2>What we collect</h2>
        <p>Name, contact details, business details, and the financial and tax information needed to provide accounting and tax services. If you book a call or email us, we keep that correspondence. Microsoft Bookings also holds the appointment details you enter there.</p>
        <h2>Why we collect it</h2>
        <p>To provide the service you asked for, meet our tax-agent and legal obligations, and run the practice. We do not sell lists.</p>
        <h2>How we hold it</h2>
        <p>Client files live in the firm’s Microsoft 365, Xero and related practice systems. Access is limited to people doing the work. We keep records for as long as tax and professional rules require, then destroy or de-identify them in the ordinary course.</p>
        <h2>Who we share it with</h2>
        <p>Only where the job requires it: the ATO, ASIC, your bank or software provider with your authority, professional indemnity insurers, and regulators when the law requires it. Microsoft, Xero and similar suppliers process information to run those tools. Some of those suppliers store or support data outside Australia. We use them because the practice cannot run without them. Tell us if you do not want a named tool used on your file.</p>
        <h2>This website</h2>
        <p>This site does not currently run advertising or audience analytics tags. Clicks on book, email and call links may be stored in your own browser session so we can test the pages. That does not leave your device. Search engines may still crawl public pages.</p>
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
        "Your rights and our obligations | Service Profit | Pink Accounting",
        "Pink Accounting is a registered tax practitioner. TPB register, complaints, ABN, AI disclosure and professional obligations.",
        "/rights.html",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Pink Accounting</span>
      <h1>Your rights and our obligations</h1>
      <div class="prose">
        <p>We are a registered tax practitioner. Service Profit is a service of Pink Accounting &amp; Tax Solutions Pty Ltd, not a separate firm. Owner of these statements: Huong Bui. Last reviewed 10 September 2026.</p>
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
          <li><b>Tax agent registration 26284368</b> — <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB public register</a></li>
          <li><b>ABN 51 682 301 891</b> — <a href="https://abr.business.gov.au/ABN/View?abn=51682301891" rel="noopener">ABN Lookup</a></li>
          <li><b>Company and business names</b> — ASIC, including Pink Accounting and Pink Strategic Accounting</li>
          <li><b>Professional membership</b> — Member, Institute of Public Accountants (MIPA AFA)</li>
        </ul>
        <p>If anything on this page disagrees with those registers, the register wins. Tell us: admin@pinktax.com.au.</p>
        <h2>Smart technology, real expertise</h2>
        <p>Pink pairs experienced people with business-grade tools for research, data and drafting. We do the thinking, the judgment and the advice. Every output is reviewed and signed off by a qualified member of the team. No automated tool makes decisions about your tax affairs. We do not allow confidential information to train public models. Personal information is handled under the Privacy Act 1988. If you would prefer we did not use those tools on your file, tell us.</p>
        <h2>Disclosure statements</h2>
        <p>No prescribed events under section 45 of the Tax Agent Services (Code of Professional Conduct) Determination 2024 have occurred in the last 5 years. Owner: Huong Bui. Review date: 10 September 2026.</p>
        <p>Our registration is not subject to any conditions limiting the scope of services we can provide. Owner: Huong Bui. Review date: 10 September 2026.</p>
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
        <p>These terms cover this website and an enquiry or discovery call. Paid work is governed by the letter of engagement, not this page. Last reviewed 10 September 2026.</p>
        <h2>Who we are</h2>
        <p>Pink Accounting &amp; Tax Solutions Pty Ltd, ABN 51 682 301 891, Registered Tax Agent 26284368. Service Profit is a Queensland service line of that firm.</p>
        <h2>The call</h2>
        <p>A booked call is a conversation to see whether there is a fit. It is not tax advice, not an engagement, and not a quote until the letter is issued. Booking software is Microsoft Bookings. Confirmation goes to you and to admin@pinktax.com.au.</p>
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


def trade_page(slug, title, h1, lead, blocks):
    h = head(
        f"{title} | Service Profit | Pink Accounting",
        lead,
        f"/{slug}.html",
    )
    cards = "\n".join(
        f'        <section class="card"><span class="eyebrow">{k}</span><h2>{t}</h2><p>{p}</p></section>'
        for k, t, p in blocks
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Service Profit · Queensland</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="cta">
        <a class="btn btn-primary" href="book.html" data-event="trade-book-{slug}">Book a 15-minute call <span class="arw">→</span></a>
        <a class="btn btn-outline" href="index.html#pricing">See the plans</a>
      </div>
      <div class="grid3">
{cards}
      </div>
      <div class="prose" style="margin-top:48px">
        <h2>What we need from the file</h2>
        <p>Xero for the books. Labour and materials on the job, or a job report you already keep. If those are missing, we can still keep the books current. We will not dress that up as job profit.</p>
        <p>This page is for {title.lower()} work. It does not change the fee table. Builders of houses or commercial buildings are outside this line.</p>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


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
      <p class="lead">Go back to Service Profit, a Pink Accounting service for HVAC, electrical and construction service businesses in Queensland.</p>
      <div class="cta"><a class="btn btn-primary" href="index.html">Home</a></div>
    </div>
  </main>
{footer()}"""
    return h + body


SITEMAP = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{ORIGIN}/</loc></url>
  <url><loc>{ORIGIN}/system.html</loc></url>
  <url><loc>{ORIGIN}/why.html</loc></url>
  <url><loc>{ORIGIN}/book.html</loc></url>
  <url><loc>{ORIGIN}/contact.html</loc></url>
  <url><loc>{ORIGIN}/hvac.html</loc></url>
  <url><loc>{ORIGIN}/electrical.html</loc></url>
  <url><loc>{ORIGIN}/construction.html</loc></url>
  <url><loc>{ORIGIN}/rights.html</loc></url>
  <url><loc>{ORIGIN}/privacy.html</loc></url>
  <url><loc>{ORIGIN}/terms.html</loc></url>
</urlset>
"""


def main():
    write("index.html", index())
    write("system.html", system())
    write("why.html", why())
    write("book.html", book())
    write("contact.html", contact())
    write("privacy.html", privacy())
    write("rights.html", rights())
    write("terms.html", terms())
    write(
        "hvac.html",
        trade_page(
            "hvac",
            "HVAC",
            "Quoted hours versus hours on the van.",
            "For air conditioning and refrigeration firms in Queensland. Labour against the quote, materials on the van, and whether a call-out covered the next tax bill.",
            [
                ("Labour", "Call-out versus quoted hours", "A diary full of call-outs can still hide jobs that ran long and were never repriced."),
                ("Materials", "What left the van", "Parts billed at cost, or not billed at all, do not show up in a year-end pack in time to change the next quote."),
                ("Cash", "The next tax bill", "We keep the books current so a busy week is not mistaken for a funded BAS."),
            ],
        ),
    )
    write(
        "electrical.html",
        trade_page(
            "electrical",
            "Electrical",
            "Quoted jobs versus hours on the tools.",
            "For electrical contracting businesses in Queensland. Quoted work, subcontractors, and cash sitting in unfinished jobs.",
            [
                ("Jobs", "Quote versus actual", "Hours on the tools against the quote, while the next tender can still change."),
                ("People", "Subcontractors in plain sight", "Subcontractors left visible, not mixed into a lump that only makes sense in June."),
                ("Cash", "Unfinished work", "Cash can sit in work not yet billed. The books should show that before you hire the next pair of hands."),
            ],
        ),
    )
    write(
        "construction.html",
        trade_page(
            "construction",
            "Construction services",
            "The job, not the building.",
            "For contracted fit-out, maintenance and installation in Queensland. Not house builders. Not commercial builders.",
            [
                ("Scope", "What construction services means here", "Fit-out, maintenance, installation and similar contracted job work. Not building houses or commercial buildings as a builder."),
                ("Jobs", "Labour, subcontractors, materials", "Read while you can still change the next quote, not after 30 June."),
                ("Boundary", "Who we do not take on this line", "Hospitality sits on pinktax.com.au. Builders of houses or commercial buildings are outside Service Profit."),
            ],
        ),
    )
    write("404.html", not_found())
    (ROOT / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
