# Service Profit

A **Pink Accounting** service for HVAC, electrical and construction service businesses in Queensland.

Public site: GitHub Pages from this repository (`www.serviceprofit.com.au`).

Entity: Pink Accounting & Tax Solutions Pty Ltd  
ABN 51 682 301 891 · Registered Tax Agent 26284368

Booking calendar for this site is the field-service Bookings service, not the hospitality diary. When that calendar is closed, `book.html` captures the lead with a form to admin@pinktax.com.au.

Pricing lives at `pricing.html` so the plans can be linked and indexed.

Rebuild pages after copy changes:

```
python tools/build_assets.py
python tools/build_pages.py
python tests/test_site.py
```
