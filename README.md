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

## Live Google reviews

The rating, review count and the three quotes on the homepage come from the
Google Business Profile, pulled at build time by `tools/fetch_reviews.py` into
`data/google_reviews.json`. The page renders from that file. If the file is
missing or malformed the site falls back to the figures committed in
`tools/build_pages.py`, so a Places API outage can never blank the homepage.

The fetch is build-time on purpose. This site is static GitHub Pages, so an API
key sent to the browser would be readable by anyone who opened devtools. The key
never leaves GitHub Actions.

Step-by-step setup, including what it costs and what to do when it fails, is
in `docs/GOOGLE_REVIEWS_SETUP.md`. In short, two settings on the repository:

| Where | Name | Value |
|---|---|---|
| Settings, Secrets, Actions | `GOOGLE_PLACES_API_KEY` | A Google Cloud key with the Places API (New) enabled, restricted to that API |
| Settings, Variables, Actions | `GOOGLE_PLACE_ID` | The Place ID. Leave unset for the first run and the workflow log prints it |

Then run the "Refresh Google reviews" workflow by hand once. After that it runs
Monday mornings Brisbane time. It opens a pull request rather than pushing to
`main`, because merging to `main` publishes the live site.

Reviews are shown with the author name and a link back to the review, which the
Places API terms require. There is deliberately no `aggregateRating` structured
data: the reviews are Google's, not ours, and marking up third-party reviews as
your own rating breaches Google's structured data policy.

## One business, one identity (HB 24 Sep 2026)

Pink Accounting is one business with two service lines. This site is the
trades line, "Service Profit, a Pink Accounting service". The hospitality line
is pinktax.com.au.

`identity.json` holds the name, address, phone, hours, Google profile and the
cross-link wording. It is generated from the firm's canonical file
(`Pink-Accounting-Automation/scripts/brand/pink-identity.json`) by
`Invoke-PinkIdentityGuard.py --sync`. Never edit it here, and never hardcode
those details in `tools/`.

- Tests fail if the schema, footer, hours or name drift from `identity.json`.
- `tools/identity_watch.py` runs every morning in GitHub Actions and checks both
  live sites and the Google profile. A red run means something changed outside
  the code: fix it at the source.
