# Service Profit

A **Pink Accounting** service for HVAC, electrical and construction service businesses in Queensland.

Public site: GitHub Pages from this repository (`www.serviceprofit.com.au`).

Entity: Pink Accounting & Tax Solutions Pty Ltd  
ABN 51 682 301 891 · Registered Tax Agent 26284368

Booking calendar is the Service Profit Bookings page (`ServiceProfit@pinktax.com.au`), not the hospitality diary. `book.html` also has a form to admin@pinktax.com.au if none of the times suit.

Pricing lives at `pricing.html` so the plans can be linked and indexed.

Rebuild pages after copy changes:

```
python tools/build_assets.py
python tools/build_pages.py
python tests/test_site.py
```
