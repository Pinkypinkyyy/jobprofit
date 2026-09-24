"""Daily drift watch: is Pink Accounting still one business, everywhere?

HB 24 Sep 2026. identity.json is the single source of truth. This checks what is
actually LIVE against it, because drift happens outside our code: a directory
edit, a Google profile change, a second listing someone creates at Shop 15A.

Runs in GitHub Actions (.github/workflows/identity-watch.yml). Any finding fails
the run, and GitHub emails the repo owner. Stdlib only.
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))
# Home and the office page on each site.
PAGES = {
    "trades": (ID["service_lines"]["trades"]["site"], ("", "contact.html")),
    "hospitality": (ID["service_lines"]["hospitality"]["site"], ("", "contact/")),
}
TIMEOUT = 30


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PinkIdentityWatch/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def check_page(html, where):
    """Findings for one rendered page. Empty list means clean."""
    out = []
    org_id = ID["schema"]["organization_id"]
    nodes = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            nodes.append(json.loads(block))
        except ValueError:
            out.append(f"{where}: unreadable JSON-LD block")
    o = ID["office"]
    for n in nodes:
        if "address" not in n:
            continue
        if n.get("@id") != org_id:
            out.append(f"{where}: second business node {n.get('@id') or n.get('name')}")
            continue
        if n.get("name") != ID["public_name"]:
            out.append(f"{where}: schema name {n.get('name')!r}, want {ID['public_name']!r}")
        if n.get("telephone") != o["phone_e164"]:
            out.append(f"{where}: schema phone {n.get('telephone')!r}")
        if (n.get("address") or {}).get("streetAddress") != o["street"]:
            out.append(f"{where}: schema street {(n.get('address') or {}).get('streetAddress')!r}")
        if (n.get("openingHoursSpecification") or {}).get("dayOfWeek") != o["hours"]["days"]:
            out.append(f"{where}: schema hours differ from identity")
    if html.count('data-identity="cross-link"') != 1:
        out.append(f"{where}: cross-link line missing or doubled")
    text = html.replace("&amp;", "&")
    for banned in ID["banned_public_names"]:
        if banned in text:
            out.append(f"{where}: banned name {banned!r}")
    stem = ID["legal"]["entity"].replace(" Pty Ltd", "")
    for m in re.finditer(re.escape(stem), text):
        if text[m.end():m.end() + 8] != " Pty Ltd":
            out.append(f"{where}: full company name used as the business name")
            break
    return out


def check_sites():
    out = []
    for line, (base, pages) in PAGES.items():
        try:
            live = json.loads(fetch(base + "identity.json"))
            if live != ID:
                out.append(f"{line}: live identity.json differs from this repo (live version {live.get('version')})")
        except Exception as exc:  # noqa: BLE001 - any failure is a finding
            out.append(f"{line}: cannot read live identity.json ({exc})")
        for page in pages:
            url = base + page
            try:
                out += check_page(fetch(url), url)
            except Exception as exc:  # noqa: BLE001
                out.append(f"{url}: fetch failed ({exc})")
    return out


def _places(key, query):
    body = json.dumps({"textQuery": query, "maxResultCount": 10}).encode("utf-8")
    req = urllib.request.Request("https://places.googleapis.com/v1/places:searchText", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Goog-Api-Key", key)
    req.add_header("X-Goog-FieldMask",
                   "places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.googleMapsUri,places.types")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8")).get("places") or []


def check_google_profile(key):
    """One profile, right name and phone, and no second listing at Shop 15A."""
    out = []
    g, o = ID["google_profile"], ID["office"]
    seen = {}
    for q in (f"{g['name']} {o['locality']} {o['region']}",
              f"accountant {o['one_line']}",
              f"Service Profit {o['one_line']}"):
        for p in _places(key, q):
            seen[p.get("googleMapsUri", "")] = p
    ours = {uri: p for uri, p in seen.items() if f"cid={g['cid']}" in uri}
    if not ours:
        out.append("google: the Pink Accounting profile was not found by search")
    for p in ours.values():
        name = (p.get("displayName") or {}).get("text")
        if name != g["name"]:
            out.append(f"google: profile name is {name!r}, want {g['name']!r}")
        if (p.get("nationalPhoneNumber") or "").replace(" ", "") != o["phone_display"].replace(" ", ""):
            out.append(f"google: profile phone is {p.get('nationalPhoneNumber')!r}")
    for uri, p in seen.items():
        if uri in ours:
            continue
        addr = p.get("formattedAddress") or ""
        if "Kremzow" in addr and o["postcode"] in addr and "accounting" in (p.get("types") or []):
            out.append(f"google: second accounting profile at our address: "
                       f"{(p.get('displayName') or {}).get('text')!r} {uri}")
    return out


def main():
    findings = check_sites()
    key = os.environ.get("GOOGLE_PLACES_API_KEY", "").strip()
    if key:
        try:
            findings += check_google_profile(key)
        except Exception as exc:  # noqa: BLE001
            findings.append(f"google: Places lookup failed ({exc})")
    else:
        print("NOTE: GOOGLE_PLACES_API_KEY is not set, so the Google profile check did not run.")
    print(f"identity version {ID['version']}: {len(findings)} finding(s)")
    for f in findings:
        print("  DRIFT:", f)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
