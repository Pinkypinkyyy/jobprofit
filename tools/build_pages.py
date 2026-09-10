from pathlib import Path
from shared import BOOK, GBP, MSBOOK, ORIGIN, footer, head, nav, sticky

ROOT = Path(__file__).resolve().parents[1]


def write(name, html):
    path = ROOT / name
    path.write_text(html, encoding="utf-8")
    print("wrote", name, path.stat().st_size)


JSONLD = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"AccountingService","@id":"https://www.serviceprofit.com.au/#business","name":"Service Profit","alternateName":"Pink Accounting","url":"https://www.serviceprofit.com.au/","telephone":"+61735446386","email":"admin@pinktax.com.au","image":"https://www.serviceprofit.com.au/assets/og.png","priceRange":"$$","knowsAbout":["HVAC accounting","electrical contractors","construction services","job costing","BAS","GST"],"address":{"@type":"PostalAddress","streetAddress":"Shop 15A, 18-22 Kremzow Rd","addressLocality":"Brendale","addressRegion":"QLD","postalCode":"4500","addressCountry":"AU"},"areaServed":[{"@type":"Place","name":"Brendale"},{"@type":"AdministrativeArea","name":"Moreton Bay"},{"@type":"City","name":"Brisbane"},{"@type":"State","name":"Queensland"}],"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"16:30"},"founder":{"@type":"Person","name":"Huong Bui"},"taxID":"51682301891","identifier":"26284368"}
  </script>
"""


def index():
    h = head(
        "Service Profit | HVAC, electrical and construction accounting in Brendale, Brisbane and Queensland",
        "Pink Accounting in Brendale for HVAC, electrical and construction service businesses across Brisbane and Queensland. Job Profit $1,650 + GST a month. Book a 15-minute call.",
        "/",
    ).replace("</head>", JSONLD + "</head>")
    body = f"""{nav("home")}
  <main id="main">
    <section class="hero">
      <div class="wrap">
        <div>
          <p class="kicker">Brendale · Brisbane · Queensland</p>
          <h1>See job profit while you can still change the next quote.</h1>
          <p class="lead">You stay on the jobs. We hold billed hours, cash, tax, BAS and GST from our Brendale office.</p>
          <div class="cta">
            <a class="btn btn-primary" href="book.html" data-event="hero-book">Book a 15-minute call</a>
            <a class="btn btn-outline" href="index.html#pricing">See the plans</a>
          </div>
          <p class="kicker" style="margin-top:28px">Same plans for every trade.</p>
          <div class="trades" aria-label="Trade examples">
            <button class="trade is-on" type="button" data-trade="hvac" aria-pressed="true">HVAC</button>
            <button class="trade" type="button" data-trade="electrical" aria-pressed="false">Electrical</button>
            <button class="trade" type="button" data-trade="construction" aria-pressed="false">Construction services</button>
          </div>
          <p class="live" id="liveLine">HVAC: labour against quoted hours, materials on the job, and whether the call-out covered the next tax bill.</p>
          <div class="trust">
            <span><a href="{GBP}" rel="noopener">Google reviews</a></span>
            <span class="sep"></span><span>Registered Tax Agent 26284368</span>
          </div>
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

    <section class="band">
      <div class="wrap">
        <span class="eyebrow">The work</span>
        <h2 style="margin-top:12px">HVAC. Electrical. Construction services.</h2>
        <div class="mosaic">
          <a class="tile" href="hvac.html"><img src="assets/hvac-864.webp" alt="HVAC plant, Brendale and Brisbane jobs" width="864" height="1152"><span>HVAC</span></a>
          <a class="tile" href="electrical.html"><img src="assets/electrical-864.webp" alt="Electrical services" width="864" height="1152"><span>Electrical</span></a>
          <a class="tile" href="construction.html"><img src="assets/construction-864.webp" alt="Construction services fit-out" width="864" height="1152"><span>Construction services</span></a>
        </div>
        <div class="stack" style="margin-top:var(--gutter)">
    <article class="split">
      <img src="assets/tech-hvac.jpg" width="864" height="1152" alt="HVAC technician reading a job docket on a commercial roof">
      <div class="split-copy">
        <span class="eyebrow">Billed hours</span>
        <h2>Quoted 6 hours. Nine on the tools.</h2>
        <p>Those 3 hours never went into the next quote. Worked example, not a client result.</p>
        <div class="docket">
          <div class="docket-row"><span>Quoted</span><b>6 h</b></div>
          <div class="docket-row"><span>On the tools</span><b>9 h</b></div>
          <div class="docket-row is-miss"><span>Unbilled</span><b>3 h</b></div>
        </div>
      </div>
    </article>

    <article class="split reverse">
      <div class="split-copy">
        <span class="eyebrow">On the tools</span>
        <h2>You stay on the jobs. We hold the file.</h2>
        <p>Billed time, materials, unfinished work, tax, BAS and GST. Registered Tax Agent 26284368. Brendale, Brisbane and Queensland.</p>
        <a class="btn btn-primary" href="book.html" data-event="split-book" style="margin-top:22px">Book a 15-minute call</a>
      </div>
      <img src="assets/tech-electrical.jpg" width="864" height="1152" alt="Electrician at a commercial switchboard">
    </article>

    <article class="split">
      <img src="assets/desk.jpg" width="1280" height="720" alt="Tax papers and a calculator on a desk">
      <div class="split-copy">
        <span class="eyebrow">Cash and tax</span>
        <h2>The bank mix is not all yours.</h2>
        <p>$100k–$500k through the account is turnover, not profit. GST, PAYG, super and wages sit in it. We pull that apart during the year so June is not a reconstruction.</p>
      </div>
    </article>
        </div>
      </div>
    </section>

    <section class="band" id="pricing">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">The plans</span>
          <h2>Can you relax on $150 + GST an hour?</h2>
          <p>That is a billed hour, not profit. GST comes off first. Then labour — staff or contractor — then materials, then the ute and the insurance. What is left is yours. If nothing is left, the hour was not enough.</p>
        </div>
        <div class="hour-board">
          <div class="cell"><b>$150 + GST</b><span>Billed to the client. Worked example, not your rate.</span></div>
          <div class="cell"><b>$15 GST</b><span>Not yours. It sits in the bank for the ATO.</span></div>
          <div class="cell"><b>$150 left</b><span>On paper. Labour, parts and overhead still come out.</span></div>
          <div class="cell is-miss"><b>Profit?</b><span>Only after staff or contractor, materials, and the business.</span></div>
        </div>
        <p class="note-ex">If a staff hour costs you $50 all-in, you need more than one billed hour to cover one hour of their time, before your own wage and any profit. Count the billed hours in the week before you hire.</p>
        <div class="feat" id="job-profit">
          <div>
            <span class="badge">Typical ongoing plan</span>
            <h3>Job Profit</h3>
            <div class="fprice">$1,650<small> + GST / month</small></div>
            <div class="fyear">$19,800 + GST a year</div>
            <p class="fdesc">The number you care about is billed hours versus quoted hours, and how much of the bank balance is actually yours. GST, PAYG, super and wages sit in that account. They are not drawings.</p>
            <div class="fcta"><a class="btn btn-primary" href="book.html" data-event="pricing-book">Book a 15-minute call</a></div>
            <div class="fnote">We do not publish a savings figure for your firm. One unbilled day of labour is usually more than a month of this fee. That is a comparison, not a client result.</div>
          </div>
          <ul>
            <li><b>Billed time</b> quoted hours versus hours on the tools, each week. If a job ran long, the next quote should not repeat it</li>
            <li><b>Cash that is yours</b> unfinished work, GST, PAYG, super and wages pulled apart so you know what you can spend</li>
            <li><b>Utes, phones, FBT</b> watched in the file. Not left as a June surprise</li>
            <li><b>Tax, BAS and GST held</b> for one trading entity, as written in the letter. Prepared from current records, so you are not paying tax on missing invoices</li>
          </ul>
        </div>
        <div class="tiers">
          <a class="tier" href="#level-weekly">
            <div class="tname">Weekly Visibility</div>
            <div class="tprice">$2,650<small> + GST/mo, from</small></div>
            <div class="fyear">from $31,800 + GST a year</div>
            <p>Job Profit, plus a snapshot while the job is still on site. You see billed time before the job is closed.</p>
          </a>
          <a class="tier" href="#level-scale">
            <div class="tname">Ready to Scale</div>
            <div class="tprice">$3,500<small> + GST/mo, from</small></div>
            <div class="fyear">from $42,000 + GST a year</div>
            <p>Plus a written forecast: hire, draw, hold. Application only. Not a guaranteed result.</p>
          </a>
          <a class="tier" href="#level-compliance">
            <div class="tname">Compliance</div>
            <div class="tprice">$550<small> + GST/mo</small></div>
            <div class="fyear">$6,600 + GST a year</div>
            <p>Tax and BAS. Return and GST from a file that is already in order, so compliance is not a June scramble.</p>
          </a>
        </div>
        <div class="addon" id="level-bookkeeping">
          <h3>Bookkeeping add-on · from $500 + GST / month · from $6,000 + GST a year</h3>
          <p>Not a plan. Quoted when it is actually needed: tax time, a catch-up, or while Job Profit is more than the business can take yet. It does not include the weekly job-and-cash look.</p>
        </div>
        <details class="scope-fold">
          <summary>Full comparison — fees, included, not included</summary>
        <div class="table-scroll" tabindex="0" aria-label="Plan comparison. Scroll sideways on a small screen to read every column.">
          <table class="scope">
            <thead>
              <tr><th>Level</th><th>Fee</th><th>Included</th><th>Not included</th></tr>
            </thead>
            <tbody>
              <tr class="pop" id="level-job">
                <td><strong>Job Profit</strong></td>
                <td class="price">$1,650 / mo<br>$19,800 / yr</td>
                <td>Billed hours vs quoted hours. Cash that is yours vs GST, PAYG, super, wages. FBT watched in the file. Books and BAS sit under that.</td>
                <td>A monthly meeting. Unlimited access. Catch-up. A published savings figure.</td>
              </tr>
              <tr id="level-weekly">
                <td><strong>Weekly Visibility</strong></td>
                <td class="price">from $2,650 / mo<br>from $31,800 / yr</td>
                <td>Includes Job Profit. Snapshot while the job is still on site.</td>
                <td>Open-ended project work unless scoped.</td>
              </tr>
              <tr id="level-scale">
                <td><strong>Ready to Scale</strong></td>
                <td class="price">from $3,500 / mo<br>from $42,000 / yr</td>
                <td>Includes Weekly Visibility. Written forecast: hire, draw, hold. Application only.</td>
                <td>A guaranteed result. Unlimited access.</td>
              </tr>
              <tr id="level-compliance">
                <td><strong>Compliance</strong></td>
                <td class="price">$550 / mo<br>$6,600 / yr</td>
                <td>Tax and BAS. Return and GST from records already in order. We are the registered tax agent for the file.</td>
                <td>Job-and-cash look. WhatsApp. Catch-up. Unlimited advisory.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="table-hint">Swipe sideways for every column.</p>
        </details>
        <div class="scope-cards">
          <article class="scope-card"><h3>Job Profit</h3><div class="price">$1,650 / month · $19,800 / year</div><p><b>You care about:</b> billed hours vs quoted hours, and how much of the bank balance is yours.</p><p><b>Not included:</b> a monthly meeting, a published savings figure.</p></article>
          <article class="scope-card"><h3>Weekly Visibility</h3><div class="price">from $2,650 / month · from $31,800 / year</div><p><b>You care about:</b> seeing billed time while the job is still on site.</p></article>
          <article class="scope-card"><h3>Ready to Scale</h3><div class="price">from $3,500 / month · from $42,000 / year</div><p><b>You care about:</b> a written forecast before you hire or draw. Application only.</p></article>
          <article class="scope-card" id="card-compliance"><h3>Compliance</h3><div class="price">$550 / month · $6,600 / year</div><p>Tax and BAS. Return and GST from a file already in order. We hold this so you can stay on the jobs.</p></article>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap meet">
        <div class="shot">
          <img src="assets/pink-portrait.jpg" width="800" height="1000" alt="Huong Bui, principal of Pink Accounting">
        </div>
        <div>
          <span class="eyebrow">Meet Pink</span>
          <h2 style="margin-top:12px">Hello, I am Pink.</h2>
          <p>Huong Bui. I founded Pink Accounting in 2020. We are your tax agent. We take care of the file so you can do the jobs.</p>
          <p>I take the call when I am free. If I am already booked, a team member takes it and I read the notes the same working day.</p>
          <div class="creds">Registered Tax Agent 26284368 · MIPA / AFA · Brendale QLD</div>
          <a class="btn btn-primary" href="book.html" data-event="meet-book" style="margin-top:22px">Book a 15-minute call</a>
        </div>
      </div>
    </section>

    <section class="final final-photo">
      <div class="wrap">
        <h2>Fifteen minutes. Then we look at the file.</h2>
        <p>You stay on the jobs. We hold tax, BAS, billed hours and cash from Brendale, across Brisbane and Queensland.</p>
        <a class="btn btn-white" href="book.html" data-event="final-book">Book a 15-minute call</a>
        <div class="micro">Registered Tax Agent 26284368 · Business clients only · Queensland · <a href="rights.html" style="color:#fff;text-decoration:underline">Your rights</a> · <a href="privacy.html" style="color:#fff;text-decoration:underline">Privacy</a> · <a href="terms.html" style="color:#fff;text-decoration:underline">Terms</a></div>
      </div>
    </section>
  </main>
{sticky()}
{footer()}"""
    return h + body


def system():
    h = head(
        "The system | Service Profit",
        "Billed hours, staff versus contractors, cash that is yours, tax and BAS held. Service Profit for HVAC, electrical and construction services in Queensland.",
        "/system.html",
    )
    body = f"""{nav("system")}
  <main id="main">
    <section class="page" style="padding-bottom:0">
      <div class="wrap">
        <span class="eyebrow">The system</span>
        <h1>Is $150 + GST an hour enough to relax?</h1>
        <p class="lead">That is a billed hour. It is not profit. GST comes off. Then the person on the tools — staff or contractor — then parts, then the business. We hold that picture, and we hold tax and BAS, so you can stay on the jobs.</p>
        <div class="cta">
          <a class="btn btn-primary" href="book.html" data-event="system-book">Book a 15-minute call</a>
          <a class="btn btn-outline" href="index.html#pricing">See the plans</a>
        </div>
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
      <div class="wrap stack">
    <article class="split">
      <img src="assets/tech-electrical.jpg" width="864" height="1152" alt="Electrician on the tools">
      <div class="split-copy">
        <span class="eyebrow">Hours you can afford</span>
        <h2>How many billed hours does that person need?</h2>
        <p>Take the weekly cost of the person. Divide by the billed rate after GST. That is the hours that must land on invoices this week, before materials and overhead. If that number is not in the diary, do not hire on a feeling.</p>
      </div>
    </article>
    <article class="split reverse">
      <div class="split-copy">
        <span class="eyebrow">Compliance</span>
        <h2>Tax and BAS stay in the file.</h2>
        <p>We are the tax agent. Super, PAYG, GST, FBT on utes and phones, and the return, sit here so you are not paying tax on a mess. You stay on the jobs.</p>
        <a class="btn btn-primary" href="book.html" data-event="system-comp" style="margin-top:22px">Book a 15-minute call</a>
      </div>
      <img src="assets/desk.jpg" width="1280" height="720" alt="Tax papers on a desk">
    </article>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <div class="faq">
          <details><summary>What happens in the first month?</summary><p>You give Xero, bank and payroll access, or send the source documents. We confirm the start date in the letter. Catch-up of earlier periods is a separate fee, quoted first.</p></details>
          <details><summary>Do you tell me whether to hire staff or a contractor?</summary><p>We show the cost of each in the file. The employment decision is yours. If someone works like staff, that is a compliance issue as well as a cost issue.</p></details>
          <details><summary>How do I cancel?</summary><p>The letter of engagement sets the term and how to end it.</p></details>
        </div>
      </div>
    </section>
  </main>
{footer()}"""
    return h + body


def why():
    h = head(
        "Meet Pink | Service Profit",
        "Huong Bui. Service Profit for HVAC, electrical and construction service businesses in Queensland.",
        "/why.html",
    )
    body = f"""{nav("why")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Service Profit</span>
      <h1>You stay on the jobs. We hold the file.</h1>
      <div class="prose">
        <p>Service Profit is the brand for HVAC, electrical and construction service businesses in Queensland. It is not hospitality, and it is not for builders putting up houses or commercial buildings.</p>
        <h2>A system, not a once-a-year pack</h2>
        <p>We are a registered tax agent. Your file runs on documented coding rules, GST logic and review gates. Job and cash numbers sit in the year so the return is prepared from a file that is already in order. You stay on the tools.</p>
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
        <a class="btn btn-primary" href="book.html" data-event="why-book">Book a 15-minute call</a>
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
        <a class="btn btn-primary" href="{MSBOOK}" rel="noopener" data-event="book-calendar">Open the Service Profit calendar</a>
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
        "Contact | Service Profit Brendale | Pink Accounting",
        "Talk to Pink Accounting at Shop 15A, 18-22 Kremzow Rd, Brendale QLD. HVAC, electrical and construction accounting across Brisbane and Queensland. 07 3544 6386.",
        "/contact.html",
    )
    body = f"""{nav("contact")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Contact Pink Accounting</span>
      <h1>Talk to the accountant. Not a ticket queue.</h1>
      <p class="lead">Brendale office. HVAC, electrical and construction service businesses across Brisbane and Queensland.</p>
      <div class="cta">
        <a class="btn btn-primary" href="book.html" data-event="contact-book">Book a 15-minute call</a>
        <a class="btn btn-outline" href="tel:+61735446386">Call 07 3544 6386</a>
      </div>
      <div class="grid3">
        <section class="card"><span class="eyebrow">Phone</span><h2><a href="tel:+61735446386">07 3544 6386</a></h2><p>Mon-Fri, 9:00am-4:30pm. Saturday by appointment.</p></section>
        <section class="card"><span class="eyebrow">Email</span><h2><a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a></h2><p>The firm mailbox. A person reads it.</p></section>
        <section class="card"><span class="eyebrow">Visit</span><h2>Brendale QLD 4500</h2><p>Shop 15A, 18-22 Kremzow Rd. Moreton Bay, north of Brisbane. Service Profit is Queensland. Hospitality clients of the same firm sit on pinktax.com.au.</p></section>
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
        f"{title} accounting in Queensland | Service Profit, Brendale",
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
        <a class="btn btn-primary" href="book.html" data-event="trade-book-{slug}">Book a 15-minute call</a>
        <a class="btn btn-outline" href="index.html#pricing">See the plans</a>
      </div>
      <div class="grid3">
{cards}
      </div>
      <div class="prose" style="margin-top:48px">
        <h2>What we need from the file</h2>
        <p>Xero for the books. Labour and materials on the job, or a job report you already keep. If those are missing, we can still keep the books current. We will not dress that up as job profit.</p>
        <p>This page is for {title.lower()} work from our Brendale office, across Brisbane and Queensland. It does not change the fee table. Builders of houses or commercial buildings are outside this line.</p>
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
      <p class="lead">Go back to Service Profit. HVAC, electrical and construction service businesses in Queensland.</p>
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
            "Quoted hours versus hours on the job.",
            "HVAC accounting from Brendale for air conditioning and refrigeration firms across Brisbane and Queensland. Labour against the quote, materials on the job, tax and BAS held.",
            [
                ("Labour", "Call-out versus quoted hours", "A diary full of call-outs can still hide jobs that ran long and were never repriced."),
                ("Materials", "Parts on the job", "Parts billed at cost, or not billed at all, do not show up in a year-end pack in time to change the next quote."),
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
            "Electrical contracting accounting from Brendale, for firms across Brisbane and Queensland. Quoted work, subcontractors, unfinished jobs, tax and BAS held.",
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
            "Construction services accounting from Brendale: fit-out, maintenance and installation across Brisbane and Queensland. Not house builders.",
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
