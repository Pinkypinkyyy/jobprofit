# Red team: three trade pages were fake products

HVAC, electrical and construction services are **who the work is for**, not three products.

Same plans. Same letter. Same billed-hours and cash look. Splitting them into `/hvac.html`, `/electrical.html` and `/construction.html` made a nav a tradie (and the owner) could not read, and hid the callback film on a page nobody opened.

Fix: one homepage, one pricing page, one system page. Nav is Pricing · The system · Meet Pink · Contact.

Audience pages (18 September 2026) are a different thing. `/air-conditioning-accountant-brisbane/`, `/electrician-accountant-brisbane/` and `/construction-services-accountant-brisbane/` explain the same Job Profit offer in that trade's job language. They are not three products, they are not in the primary nav, and they all carry the same fee. Old `/hvac.html`, `/electrical.html` and `/construction.html` stubs now canonicalise to those audience pages.
