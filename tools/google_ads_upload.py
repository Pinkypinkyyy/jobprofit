"""Service Profit Google Search campaign -> Google Ads bulk-upload CSV (Editor columns).
Source spec: jobprofit/docs/ADS_AND_SEO_SETUP_20260912.md, red-teamed 2 Oct 2026."""
import csv, sys

C = "Search | Service Profit | QLD trades | 2026-10"
SITE = "https://www.serviceprofit.com.au"

GROUPS = {
    "SP-01 HVAC": dict(
        url=f"{SITE}/air-conditioning-accountant-brisbane/", p1="HVAC", p2="Queensland",
        phrase=["hvac accountant", "air conditioning accountant", "refrigeration accountant",
                "hvac bookkeeping", "air conditioning bookkeeping", "accountant for hvac business",
                "hvac tax agent"],
        exact=["hvac accountant", "hvac accountant brisbane", "air conditioning accountant brisbane"],
        h=["HVAC accounting, Brendale", "See job profit in time", "Quoted 6 hours. Nine used",
           "Tax agent for HVAC QLD", "Pink Accounting for trades", "Books, BAS and billed hours",
           "Stay on the jobs", "HVAC bookkeeping, Queensland", "FBT on work utes covered",
           "Book a 15-minute call", "Service Profit HVAC", "From Shop 15A, Brendale",
           "Income tax and BAS lodged", "Air con and refrigeration", "Change the next quote"],
        d=["HVAC in Queensland. Billed hours, cash, tax and BAS from Brendale. Book a 15-minute call.",
           "Quoted hours versus hours on the tools. Pink Accounting. Registered Tax Agent 26284368.",
           "You stay on the jobs. We hold the file. Job Profit is $1,650 + GST a month.",
           "Air conditioning and refrigeration books from Brendale, for firms across Queensland."]),
    "SP-02 Electrical": dict(
        url=f"{SITE}/electrician-accountant-brisbane/", p1="Electrical", p2="Queensland",
        phrase=["electrician accountant", "electrical contractor accountant", "accountant for electricians",
                "electrician bookkeeping", "electrical contractor bookkeeping", "electrician tax agent"],
        exact=["electrician accountant brisbane", "accountant for electricians"],
        h=["Electrical accounting QLD", "Quote versus hours on tools", "Electrician bookkeeping",
           "Tax agent, Brendale", "Pink Accounting for trades", "Subcontractors in the file",
           "Stay on the jobs", "BAS and billed hours", "Book a 15-minute call",
           "Service Profit electrical", "Unfinished work, visible", "From Brendale, Queensland",
           "Income tax and FBT lodged", "Electrical contractors, QLD", "Change the next quote"],
        d=["Electrical contractors in Queensland. Quoted jobs, subcontractors, tax and BAS.",
           "Hours on the tools against the quote, while the next tender can still change.",
           "Pink Accounting. Registered Tax Agent 26284368. You stay on the jobs.",
           "Job Profit is $1,650 + GST a month. The letter is the quote."]),
    "SP-03 Construction services": dict(
        url=f"{SITE}/construction-services-accountant-brisbane/", p1="Construction", p2="Queensland",
        phrase=["construction services accountant", "fit out accountant", "shopfitting accountant",
                "maintenance contractor accountant", "construction services bookkeeping",
                "fitout bookkeeping"],
        exact=["construction services accountant", "fit out accountant brisbane"],
        neg=["residential builder", "volume builder"],
        h=["Construction services books", "The job, not the building", "Fit-out accounting, QLD",
           "Tax agent in Brendale", "Pink Accounting for trades", "Labour and materials",
           "Stay on the jobs", "Book a 15-minute call", "Service Profit",
           "Not house builders", "BAS and cash in the file", "From Brendale, Queensland",
           "Change the next quote", "Income tax and FBT lodged", "Job Profit $1,650 + GST/mo"],
        d=["Fit-out, maintenance and installation. Not house builders. Tax and BAS from Brendale.",
           "Read labour, subcontractors and materials while you can still change the next quote.",
           "Pink Accounting. Registered Tax Agent 26284368. Queensland construction services.",
           "Job Profit is $1,650 + GST a month. Book a 15-minute call."]),
    "SP-04 Trades general": dict(
        url=f"{SITE}/", p1="Trades", p2="Queensland",
        phrase=["accountant for tradies", "tradie accountant", "trade business accountant",
                "accountant for trade business", "tradie bookkeeping", "bookkeeper for tradies"],
        exact=["tradie accountant brisbane", "accountant for tradies brisbane"],
        h=["Accountant for trades, QLD", "Air con, electrical, fit-out", "Quote versus hours on tools",
           "Tax agent in Brendale", "Pink Accounting for trades", "Books, BAS and billed hours",
           "Stay on the jobs", "Book a 15-minute call", "Service Profit",
           "Income tax and BAS lodged", "Change the next quote", "From Brendale, Queensland",
           "Job Profit $1,650 + GST/mo", "Payroll, super and STP", "Cash that is yours, weekly"],
        d=["Air con, electrical and construction service firms in Queensland. Book a 15-minute call.",
           "Hours on the tools against the quote each week, while the next quote can still change.",
           "Pink Accounting. Registered Tax Agent 26284368. Income tax, BAS, payroll and Xero.",
           "Job Profit is $1,650 + GST a month. The letter sets the fee before anything starts."]),
}

CAMPAIGN_NEG = ["hospitality", "restaurant", "cafe", "venue", "margin check", "cheap", "free", "diy",
                "template", "course", "jobs", "careers", "vacancy", "salary", "hiring",
                "individual tax return", "mygov", "ato login", "house builder", "home builder",
                "commercial builder", "chartered accountant"]

# Limits: headline 30, description 90, path 15. Fail closed on any breach or duplicate.
errs = []
for g, s in GROUPS.items():
    if len(s["h"]) != 15 or len(set(s["h"])) != 15: errs.append(f"{g}: need 15 unique headlines")
    if len(s["d"]) != 4: errs.append(f"{g}: need 4 descriptions")
    errs += [f"{g} H {len(x)}: {x}" for x in s["h"] if len(x) > 30]
    errs += [f"{g} D {len(x)}: {x}" for x in s["d"] if len(x) > 90]
    errs += [f"{g} path: {p}" for p in (s["p1"], s["p2"]) if len(p) > 15]
    errs += [f"{g} '!' not allowed in headline: {x}" for x in s["h"] if "!" in x]
if errs:
    print("\n".join(errs)); sys.exit(1)

H = ["Campaign", "Campaign type", "Campaign status", "Budget", "Budget type", "Bid strategy type",
     "Networks", "Languages", "EU political ads", "Final URL suffix", "Ad group", "Ad group status", "Keyword",
     "Criterion type", "Ad type", "Status", "Final URL", "Path 1", "Path 2"] + \
    [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)]
rows = []
def row(**k): r = dict.fromkeys(H, ""); r.update(k); rows.append(r)

row(**{"Campaign": C, "Campaign type": "Search", "Campaign status": "Paused", "Budget": "14.29",
       "Budget type": "Daily", "Bid strategy type": "Maximize clicks", "Networks": "Google search",
       "Languages": "en", "EU political ads": "No",
       "Final URL suffix": "utm_source=google&utm_medium=cpc&utm_campaign=sp-qld-trades&utm_content={creative}"})
for k in CAMPAIGN_NEG:
    # No ad group on the row makes it a campaign-level negative.
    row(**{"Campaign": C, "Keyword": k, "Criterion type": "Negative broad"})
for g, s in GROUPS.items():
    row(**{"Campaign": C, "Ad group": g, "Ad group status": "Enabled"})
    for k in s["phrase"]: row(**{"Campaign": C, "Ad group": g, "Keyword": k, "Criterion type": "Phrase"})
    for k in s["exact"]: row(**{"Campaign": C, "Ad group": g, "Keyword": k, "Criterion type": "Exact"})
    for k in s.get("neg", []): row(**{"Campaign": C, "Ad group": g, "Keyword": k, "Criterion type": "Negative broad"})
    ad = {"Campaign": C, "Ad group": g, "Ad type": "Responsive search ad", "Status": "Enabled",
          "Final URL": s["url"], "Path 1": s["p1"], "Path 2": s["p2"]}
    ad.update({f"Headline {i+1}": x for i, x in enumerate(s["h"])})
    ad.update({f"Description {i+1}": x for i, x in enumerate(s["d"])})
    row(**ad)

out = sys.argv[1] if len(sys.argv) > 1 else "google_ads_upload.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, H); w.writeheader(); w.writerows(rows)
kw = sum(len(s["phrase"]) + len(s["exact"]) for s in GROUPS.values())
print(f"OK {out}: {len(rows)} rows, {len(GROUPS)} ad groups, {kw} keywords, {len(CAMPAIGN_NEG)} campaign negatives")
