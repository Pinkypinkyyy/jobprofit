You are a new Grok session. Own this job end-to-end. Do not re-ask for permission. Do not use MCP/sandbox Chrome.

# Job

Finish Service Profit public channels: Facebook, Instagram, LinkedIn, Google Business Profile. Best quality. Red-team before claiming done. Hospitality (pinktax.com.au) stays off these surfaces.

# Chrome (hard)

- Only Chrome **Profile 18** (Huong / Pink — Primary Workspace, hbpinkacc@gmail.com). Pink toolbar.
- Drive it with pywinauto UIA + PrintWindow. Helper: `_PinkOps\Workspaces\serviceprofit-channels-20260911\chrome_drive.py`
- Do not restart Chrome (Xero tab must stay). Do not CDP-kill the profile.
- Do not Ctrl+L on the Xero tab. Do not SetCursorPos on the left monitor (negative X).
- Facebook password already failed once for hb@pinktax.com.au. **Do not retry passwords.**

# Brand lock (exact)

Read: `_PinkOps\Workspaces\serviceprofit-channels-20260911\BRAND_LOCK.md`

- Public brand: **Service Profit**. Legal entity in about/footer only: Pink Accounting & Tax Solutions Pty Ltd
- Website: https://www.serviceprofit.com.au/  (never pinktax.com.au)
- Book: https://outlook.office.com/book/ServiceProfit@pinktax.com.au/
- Email: admin@pinktax.com.au
- Phone: 07 3544 6386
- Address: Shop 15A, 18-22 Kremzow Rd, Brendale QLD 4500
- Hours: Mon–Fri 9:00 am – 4:30 pm
- Category: Accountant / Accounting. Not Chartered accountant.
- TPB 26284368. ABN 51 682 301 891. Queensland / Brendale / Brisbane.
- Assets: `...\serviceprofit-channels-20260911\assets\` (profile-1080.png, cover-facebook.png, cover-linkedin.png, cover-google.png)

# Live state already proved (do not recreate)

## Google Business Profile — created, NOT public

- Name Service Profit. Category Accountant.
- Address Shop 15A / 18-22 Kremzow Rd, Brendale QLD 4500. Phone (07) 3544 6386. Website serviceprofit.com.au
- Duplicate-address screen showed **PINK ACCOUNTING** — chose **None of these**. Do not select Pink Accounting. Do not edit Pink hospitality GBP (CID 17544456102082616748).
- Listing `l/05228865027849822793` lid `563462930842102603`
- Search shows **NOT PUBLICLY VISIBLE**. Verify = shop video only. Verify Later already used so edits could continue.
- Hours: Open with main hours. Mon/Tue/Fri 09:00–17:00 (lock is 16:30). Sat/Sun closed. Wed/Thu may still be closed — fix.
- Hold: shop-front verification video at Shop 15A. Do not claim Google is public until Search no longer says not visible.

## Facebook Page — exists, dressed

- https://www.facebook.com/profile.php?id=61594432044788
- Name: Service Profit Accounting. Category: Accounting service. 0 followers (real).
- Cover + profile uploaded. Bio rewritten (QBCC / 30 June stub gone):
  `Accounting firm for HVAC, electrical and construction service businesses in Queensland. You stay on the jobs. We hold the file.`
- Phone +61 7 3544 6386. Email admin@pinktax.com.au. Website https://www.serviceprofit.com.au/
- Still to do: claim username (serviceprofit / serviceprofitau / serviceprofitaccounting), action button Book or Website, add Bookings URL as a link, About long copy, hours.

## Instagram — not created

Facebook → Connect Instagram only links an **existing** professional account. Do **not** connect a personal Instagram. Create a new professional IG for Service Profit, then connect it to this Page.

## LinkedIn company page — not created

Signed out. Must be its **own company page**, not a showcase under Pink hospitality. Use locked LinkedIn about. No password spam.

# Red-team fail (stop if any)

- Hospitality / Margin Check / venue / Australia-wide copy
- Website pinktax.com.au on any Service Profit channel
- Hijack or rename Pink Accounting GBP
- Copy Pink 5.0 Google reviews onto the new listing
- Empty shell (no logo/about/hours/CTA)
- Personal Instagram
- LinkedIn showcase of the hospitality company
- Invented followers or reviews
- Claiming done without live URL read-back

# Do next, in this order

1. Re-attach Profile 18 Chrome. Screenshot. Stay off Xero.
2. Facebook: username + Book action + Bookings link + hours. Read-back the public page.
3. Instagram: new professional account (not personal), then connect to the Facebook Page. Upload profile + bio.
4. LinkedIn: only if already signed in. Own company page. Cover + about + logo.
5. Google: fix Wed/Thu hours to 09:00–16:30. Do not claim public until verified.
6. Independent red-team. Write CHANNEL_STATUS. Push sanitised record to `Pinkypinkyyy/jobprofit` `main`. State SHA.

Site already live: https://www.serviceprofit.com.au/ — Bookings calendar already Service Profit. Do not mix Pink hospitality into this brand.

Workspace: `C:\Users\HuongBui\OneDrive - Pink Accounting & Tax Solutions Pty Ltd\_PinkOps\Workspaces\serviceprofit-channels-20260911\`
Site repo: `C:\src\jobprofit` (never the OneDrive git clone)
Prior push: `9410dd5` on `Pinkypinkyyy/jobprofit` `main`
