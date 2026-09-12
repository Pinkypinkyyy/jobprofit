from pathlib import Path
from shared import (
    GBP,
    MSBOOK,
    ORIGIN,
    cash_chart,
    enquiry_form,
    faq_node,
    footer,
    head,
    hour_waterfall,
    hours_chart,
    jsonld,
    business_node,
    local_business_node,
    nav,
    service_node,
    sticky,
)

ROOT = Path(__file__).resolve().parents[1]


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
        "A monthly meeting, unlimited access, catch-up of earlier periods, a published savings figure, and extra entities unless the letter says so. Xero subscription is yours.",
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
        "Are the fees plus GST?",
        "Yes. Published fees are monthly, exclusive of GST, for one trading entity unless the letter says otherwise.",
    ),
    (
        "How do I start?",
        "Send the enquiry on the book page or call. A booked call is a conversation to see whether there is a fit. It is not an engagement until the letter is issued.",
    ),
]


def picture(stem, alt, extra="", lazy=False, sizes="(max-width:940px) 100vw, 55vw"):
    loading = ' loading="lazy"' if lazy else ""
    return (
        f'          <picture>\n'
        f'            <source type="image/webp" srcset="/assets/{stem}-480.webp?v=real1 480w, /assets/{stem}-864.webp?v=real1 864w, /assets/{stem}-1200.webp?v=real1 1200w" sizes="{sizes}">\n'
        f'            <img{extra} src="/assets/{stem}.jpg?v=real1" width="838" height="1059" alt="{alt}"{loading}>\n'
        f'          </picture>'
    )


def index():
    h = head(
        "Service Profit | HVAC, electrical and construction accounting in Brendale, Brisbane and Queensland",
        "Pink Accounting in Brendale for HVAC, electrical and construction service businesses across Brisbane and Queensland. Job Profit $1,650 + GST a month. Book a 15-minute call.",
        "/",
        extra=jsonld(business_node()),
    )
    body = f"""{nav("home")}
  <main id="main">
    <section class="hero-bleed">
      <div class="hero-media" id="stage">
{picture("tech-hvac", "HVAC technician on a rooftop unit", ' class="is-on" data-trade="hvac"', False, "100vw")}
{picture("electrical", "Electrical switchboard", ' data-trade="electrical" aria-hidden="true" inert', True, "100vw")}
{picture("construction", "Construction services fit-out", ' data-trade="construction" aria-hidden="true" inert', True, "100vw")}
        <div class="hero-scrim"></div>
        <div class="cap" id="stageCap">HVAC</div>
      </div>
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="kicker">Pink Accounting · HVAC, electrical, construction · Queensland</p>
          <h1>See job profit while you can still change the next quote.</h1>
          <p class="lead">You stay on the jobs. We hold billed hours, cash, income tax, FBT, financial statements and BAS, from Brendale.</p>
          <div class="cta">
            <a class="btn btn-primary" href="/book.html" data-event="hero-book">Book a 15-minute call</a>
            <a class="btn btn-ghost" href="/pricing.html">See the plans</a>
          </div>
          <div class="trades" aria-label="Same work, three kinds of job">
            <button class="trade is-on" type="button" data-trade="hvac" aria-pressed="true">HVAC</button>
            <button class="trade" type="button" data-trade="electrical" aria-pressed="false">Electrical</button>
            <button class="trade" type="button" data-trade="construction" aria-pressed="false">Construction services</button>
          </div>
          <p class="live" id="liveLine">HVAC: labour against quoted hours, materials on the job, and whether the call-out covered the next tax bill.</p>
          <div class="trust">
            <a class="stars" href="{GBP}" rel="noopener">
              <span class="star-value">5.0</span>
              <span class="star-icons" aria-hidden="true">★★★★★</span>
              <span>25 Google reviews</span>
            </a>
            <span class="sep"></span><span>Registered Tax Agent 26284368</span>
          </div>
        </div>
{hours_chart()}
      </div>
    </section>

    <section class="band band-photo">
      <div class="wrap split-visual">
        <div class="photo-frame">
          <img src="/assets/tech-electrical-864.webp?v=real1" width="864" height="1092" alt="Electrician testing a switchboard" loading="lazy">
        </div>
        <div class="split-copy">
          <h2>You stay on the jobs. We hold the file.</h2>
          <p>Income tax, FBT, financial statements, BAS and GST. Billed hours versus quoted hours, each week. Cash that is yours versus GST, PAYG, super and wages. Registered Tax Agent 26284368.</p>
{cash_chart()}
          <a class="btn btn-primary" href="/book.html" data-event="split-book">Book a 15-minute call</a>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
      <figure class="watch">
        <div class="watch-frame">
          <video controls playsinline preload="metadata" poster="/assets/video/callback-cost-poster.jpg" width="1080" height="1920">
            <source src="/assets/video/callback-cost.mp4" type="video/mp4">
          </video>
        </div>
        <figcaption>
          <h2>What a callback really costs</h2>
          <p>Two technicians. Labour on the clock. A $600 job given away because the callback was never counted. Worked example, not a client result. Same story for HVAC, electrical and construction services.</p>
        </figcaption>
      </figure>
      </div>
    </section>

    <section class="band" id="who">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">Who this is for</span>
          <h2>One line. HVAC, electrical, construction services.</h2>
          <p>Same plans. Same file. Quoted hours versus hours on the tools. Cash that is yours versus GST, PAYG, super and wages. Not house builders. Not hospitality.</p>
        </div>
      </div>
    </section>

    <section class="band" id="pricing">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">Our fees</span>
          <h2>Job Profit $1,650 + GST a month.</h2>
          <p>Monthly. Books, billed hours and cash in the file, tax and BAS held. Not unlimited work. The letter is the quote.</p>
        </div>
        <div class="feat" id="job-profit">
          <div>
            <span class="badge">Typical ongoing plan</span>
            <h3>Job Profit</h3>
            <div class="fprice">$1,650<small> + GST / month</small></div>

            <p class="fdesc">The number you care about is billed hours versus quoted hours, and how much of the bank balance is actually yours. GST, PAYG, super and wages sit in that account. They are not drawings.</p>
            <div class="fcta"><a class="btn btn-primary" href="/book.html" data-event="pricing-book">Book a 15-minute call</a></div>
            <div class="fnote">If you only need the return, that is Compliance. Bookkeeping is an add-on when you need it, not a plan.</div>
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
      </div>
    </section>

    <section class="band" id="reviews">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow">Google reviews</span>
          <h2>5.0 on Google.</h2>
        </div>
        <div class="quotes">
          <blockquote>
            <p>I’ve had a fantastic experience working with Pinky. She is professional, knowledgeable, and always takes the time to explain things clearly. As a small business owner, I really appreciate her patience, attention to detail, and prompt responses.</p>
            <footer>T D · Google</footer>
          </blockquote>
          <blockquote>
            <p>Huong is super knowledgeable and keeps your books tidy and taxes up to date. She explains things clearly so you actually understand your tax, not just the numbers.</p>
            <footer>N T · Google</footer>
          </blockquote>
          <blockquote>
            <p>Pink is amazing — super quick, really knows her stuff, and an absolute gem for any business. She makes everything easy.</p>
            <footer>N M · Google</footer>
          </blockquote>
        </div>
        <p class="creds"><a href="{GBP}" rel="noopener">Read all 25 Google reviews</a></p>
      </div>
    </section>

    <section class="band">
      <div class="wrap meet">
        <div class="shot photo-frame">
          <picture>
            <source type="image/webp" srcset="/assets/pink-home.webp?v=real1">
            <img src="/assets/pink-home.jpg?v=real1" width="1200" height="1800" alt="Huong Bui, principal of Service Profit" loading="lazy">
          </picture>
        </div>
        <div>
          <span class="eyebrow">Meet Pink</span>
          <h2>Hello, I am Pink.</h2>
          <p>Huong Bui. Master of Professional Accounting (Griffith). MIPA AFA. Registered Tax Agent 26284368. More than ten years in the books. I founded the firm in 2020.</p>
          <p>We hold income tax, FBT, financial statements, BAS, GST and payroll. You stay on the jobs.</p>
          <div class="creds"><a href="/why.html">Read more about Pink</a></div>
          <a class="btn btn-primary" href="/book.html" data-event="meet-book">Book a 15-minute call</a>
        </div>
      </div>
    </section>

    <section class="final">
      <div class="wrap">
        <h2>Fifteen minutes. Then we look at the file.</h2>
        <p>You stay on the jobs. We hold billed hours, cash, tax and BAS. Brendale, Brisbane and Queensland.</p>
        <a class="btn btn-white" href="/book.html" data-event="final-book">Book a 15-minute call</a>
        <div class="micro">Registered Tax Agent 26284368 · Business clients only · Queensland · <a href="/rights.html">Your rights</a> · <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></div>
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
        <p class="lead">That is a billed hour. It is not profit. GST comes off. Then the person on the tools — staff or contractor — then parts, then the business. We hold that picture, and we hold tax and BAS, so you can stay on the jobs.</p>
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
        "Pricing | Service Profit HVAC, electrical and construction accounting",
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
        <h1>Four plans. The letter is the quote.</h1>
        <p class="lead">Monthly, exclusive of GST, for one trading entity unless the letter says otherwise. Same plans for HVAC, electrical and construction services. Not unlimited work.</p>
        <div class="cta">
          <a class="btn btn-primary" href="/book.html" data-event="pricing-page-book">Book a 15-minute call</a>
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <div class="feat" id="job-profit">
          <div>
            <span class="badge">Typical ongoing plan</span>
            <h2>Job Profit</h2>
            <div class="fprice">$1,650<small> + GST / month</small></div>

            <p class="fdesc">Billed hours versus quoted hours, and how much of the bank balance is actually yours.</p>
            <div class="fcta"><a class="btn btn-primary" href="/book.html" data-event="pricing-job">Book a 15-minute call</a></div>
          </div>
          <ul>
            <li><b>In:</b> billed hours vs quoted hours each week; cash that is yours vs GST, PAYG, super, wages; FBT watched in the file; income tax, FBT, financial statements, BAS and GST held for one trading entity</li>
            <li><b>Out:</b> a monthly meeting, unlimited access, catch-up, a published savings figure</li>
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
                <td>A monthly meeting. Unlimited access. Catch-up. A published savings figure.</td>
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
                <td>A guaranteed result. Unlimited access.</td>
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
          <article class="scope-card"><h2>Ready to Scale</h2><div class="price">from $3,500 + GST / month</div><p><b>In:</b> Weekly Visibility, plus a written forecast: hire, draw, hold. Application only.</p><p><b>Out:</b> a guaranteed result. Unlimited access.</p></article>
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
        "Meet Pink | Service Profit",
        "Huong Bui, Master of Professional Accounting (Griffith), Registered Tax Agent 26284368. More than ten years in the books. Income tax, FBT, financial statements, BAS.",
        "/why.html",
    )
    body = f"""{nav("why")}
  <main id="main">
    <section class="page" style="padding-bottom:0">
      <div class="wrap meet">
        <div class="shot">
          <picture>
            <source type="image/webp" srcset="/assets/pink-meet.webp?v=real1">
            <img src="/assets/pink-meet.jpg?v=real1" width="1080" height="1350" alt="Huong Bui in a client meeting">
          </picture>
        </div>
        <div>
          <span class="eyebrow">Meet Pink</span>
          <h1 style="margin-top:12px">Hello, I am Pink.</h1>
          <p class="lead">Huong Bui. I am a registered tax agent. I have spent more than ten years in the books. Service Profit is this accounting work with HVAC, electrical and construction services in Queensland.</p>
          <p>I take the call when I am free. If I am already booked, a team member takes it and I read the notes the same working day.</p>
          <a class="btn btn-primary" href="/book.html" data-event="why-book" style="margin-top:22px">Book a 15-minute call</a>
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <h2>Qualification</h2>
        <p class="lead" style="margin-top:12px">Master of Professional Accounting, Griffith University. Member of the Institute of Public Accountants (MIPA AFA). Registered Tax Agent 26284368. ASIC Registered Agent 52580.</p>
        <h2>Years in the books</h2>
        <p class="lead" style="margin-top:12px">More than ten years. I founded the firm in 2020. The work is in the file, not in a once-a-year pack. You stay on the jobs. I stay in the numbers.</p>
        <h2>What we hold</h2>
        <p class="lead" style="margin-top:12px">The return. FBT on utes, phones and other benefits. Financial statements. BAS and GST. Payroll, super and PAYG where you have staff. Tax compliance so you are not paying on missing invoices.</p>
        <h2>On the public register</h2>
        <p class="lead" style="margin-top:12px">Search 26284368 on the <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB public register</a>. Our obligations are written on <a href="/rights.html">Your rights</a>. ABN 51 682 301 891.</p>
      </div>
    </section>
  </main>
{footer()}"""
    return h + body


def book():
    h = head(
        "Book a 15-minute call | Service Profit | Pink Accounting",
        "Book a 15-minute Service Profit call for Queensland HVAC, electrical and construction services. Calendar confirmation to you and to admin@pinktax.com.au.",
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
    <div class="wrap">
      <span class="eyebrow">Service Profit</span>
      <h1>Book a 15-minute call</h1>
      <p class="lead">This call is for HVAC, electrical and construction service businesses in Queensland. It is not a hospitality or venue call. Bring how the business runs, the software you use, and what you want from the file. You do not need a street address for a discovery call.</p>
      <div class="cta">
        <a class="btn btn-primary" href="{MSBOOK}" rel="noopener" data-event="book-calendar">Open the Service Profit calendar</a>
        <a class="btn btn-outline" href="mailto:admin@pinktax.com.au?subject=Service%20Profit%20enquiry" data-event="book-email">Email admin@pinktax.com.au</a>
        <a class="btn btn-outline" href="tel:+61735446386" data-event="book-call">Call 07 3544 6386</a>
      </div>
      <div class="prose">
        <h2>Who you will speak with</h2>
        <p>The booking is with Service Profit. Huong (Pink) takes the call when she is free. If a team member takes it, Pink reads the notes the same working day.</p>
        <h2>What happens after you book</h2>
        <p>Microsoft Bookings sends a confirmation to you. A copy goes to admin@pinktax.com.au. A click is not a completed enquiry until the appointment is booked.</p>
      </div>
      <h2>Or send this</h2>
      <p class="lead" style="margin-top:10px">If none of the times suit, use the form. We reply within one business day.</p>
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
          <li><b>Tax agent registration 26284368</b> — <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB public register</a></li>
          <li><b>ABN 51 682 301 891</b> — <a href="https://abr.business.gov.au/ABN/View?abn=51682301891" rel="noopener">ABN Lookup</a></li>
          <li><b>Company and business names</b> — ASIC, including Pink Accounting and Pink Strategic Accounting</li>
          <li><b>Professional membership</b> — Member, Institute of Public Accountants (MIPA AFA)</li>
        </ul>
        <p>If anything on this page disagrees with those registers, the register wins. Tell us: admin@pinktax.com.au.</p>
        <h2>Smart technology, real expertise</h2>
        <p>Pink pairs experienced people with business-grade tools for research, data and drafting. We do the thinking, the judgment and the advice. Every output is reviewed and signed off by a qualified member of the team. No automated tool makes decisions about your tax affairs. We do not allow confidential information to train public models. Personal information is handled under the Privacy Act 1988. If you would prefer we did not use those tools on your file, tell us.</p>
        <h2>Disclosure statements</h2>
        <p>No prescribed events under section 45 of the Tax Agent Services (Code of Professional Conduct) Determination 2024 have occurred in the last 5 years. Owner: Huong Bui. Review date: 11 September 2026.</p>
        <p>Our registration is not subject to any conditions limiting the scope of services we can provide. Owner: Huong Bui. Review date: 11 September 2026.</p>
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


def redirect_home(title):
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <title>{title} | Service Profit</title>
  <link rel="canonical" href="{ORIGIN}/">
  <meta http-equiv="refresh" content="0;url=/index.html">
  <script>location.replace("/index.html");</script>
</head>
<body>
  <p>Service Profit is one offer for HVAC, electrical and construction service businesses. <a href="/index.html">Continue to Service Profit</a>.</p>
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
    return h + body


SITEMAP = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{ORIGIN}/</loc></url>
  <url><loc>{ORIGIN}/system.html</loc></url>
  <url><loc>{ORIGIN}/pricing.html</loc></url>
  <url><loc>{ORIGIN}/why.html</loc></url>
  <url><loc>{ORIGIN}/book.html</loc></url>
  <url><loc>{ORIGIN}/contact.html</loc></url>
  <url><loc>{ORIGIN}/rights.html</loc></url>
  <url><loc>{ORIGIN}/privacy.html</loc></url>
  <url><loc>{ORIGIN}/terms.html</loc></url>
</urlset>
"""


def main():
    write("index.html", index())
    write("system.html", system())
    write("pricing.html", pricing())
    write("why.html", why())
    write("book.html", book())
    write("contact.html", contact())
    write("privacy.html", privacy())
    write("rights.html", rights())
    write("terms.html", terms())
    write("hvac.html", redirect_home("HVAC"))
    write("electrical.html", redirect_home("Electrical"))
    write("construction.html", redirect_home("Construction"))
    write("404.html", not_found())
    (ROOT / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
