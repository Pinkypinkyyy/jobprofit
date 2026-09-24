"""Pull the live Google rating, review count and reviews into data/google_reviews.json.

This runs at BUILD time, never in the browser. serviceprofit.com.au is static
GitHub Pages, so any key shipped to the page would be readable by anyone who
opened devtools. The key lives in a GitHub Actions secret and never reaches
the site; the pages are rebuilt with whatever this wrote.

Usage:
    GOOGLE_PLACES_API_KEY=... GOOGLE_PLACE_ID=ChIJ... python3 tools/fetch_reviews.py

If GOOGLE_PLACE_ID is not set, the script resolves it from the business name
and address and prints it so it can be pinned as a repository variable. Place
IDs are the one Places response Google permits you to store indefinitely.
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "google_reviews.json"

_ID = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))
BUSINESS = _ID["public_name"]
ADDRESS = _ID["office"]["one_line"]
CID = _ID["google_profile"]["cid"]
DETAIL_FIELDS = "rating,userRatingCount,googleMapsUri,reviews"
TIMEOUT = 30


def _post(url, payload, key, field_mask):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Goog-Api-Key", key)
    req.add_header("X-Goog-FieldMask", field_mask)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(url, key, field_mask):
    req = urllib.request.Request(url)
    req.add_header("X-Goog-Api-Key", key)
    req.add_header("X-Goog-FieldMask", field_mask)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def resolve_place_id(key):
    data = _post(
        "https://places.googleapis.com/v1/places:searchText",
        {"textQuery": f"{BUSINESS} {ADDRESS}", "maxResultCount": 1},
        key,
        "places.id,places.displayName,places.formattedAddress",
    )
    places = data.get("places") or []
    if not places:
        raise SystemExit("No place matched. Check BUSINESS and ADDRESS.")
    p = places[0]
    print(f"Resolved place: {p.get('displayName', {}).get('text')} | {p.get('formattedAddress')}")
    print("=" * 60)
    print(f"GOOGLE_PLACE_ID={p['id']}")
    print("Save that as a repository variable so the lookup is not repeated.")
    print("=" * 60)
    return p["id"]


def normalise(detail):
    """Keep only what the page renders. Author name and the review link are
    required attribution under the Places API terms, so both are retained."""
    reviews = []
    for r in detail.get("reviews", []):
        text = (r.get("originalText") or r.get("text") or {}).get("text", "").strip()
        author = r.get("authorAttribution", {}) or {}
        if not text:
            continue
        reviews.append(
            {
                "text": text,
                "rating": r.get("rating"),
                "author": author.get("displayName", "").strip(),
                "author_uri": author.get("uri", ""),
                "photo_uri": author.get("photoUri", ""),
                "relative_time": r.get("relativePublishTimeDescription", ""),
                "publish_time": r.get("publishTime", ""),
                "uri": r.get("googleMapsUri", ""),
            }
        )
    return {
        "fetched": datetime.date.today().isoformat(),
        "rating": detail.get("rating"),
        "count": detail.get("userRatingCount"),
        "maps_uri": detail.get("googleMapsUri", ""),
        "reviews": reviews,
    }


def main():
    key = os.environ.get("GOOGLE_PLACES_API_KEY", "").strip()
    if not key:
        # Not an error. Until the secret exists the site renders the committed
        # figures, and the weekly workflow should stay green and quiet rather
        # than mailing a red build every Monday.
        print("GOOGLE_PLACES_API_KEY is not set, so there is nothing to fetch.")
        print("The site keeps using the figures committed in tools/build_pages.py.")
        print("See docs/GOOGLE_REVIEWS_SETUP.md to turn this on.")
        return 0
    place_id = os.environ.get("GOOGLE_PLACE_ID", "").strip() or resolve_place_id(key)
    url = f"https://places.googleapis.com/v1/places/{urllib.parse.quote(place_id)}"
    try:
        detail = _get(url, key, DETAIL_FIELDS)
    except urllib.error.HTTPError as e:
        print(f"Places API returned {e.code}: {e.read().decode('utf-8')[:400]}", file=sys.stderr)
        return 1

    # Fail closed: only the one Pink Accounting profile may feed this site.
    if f"cid={CID}" not in (detail.get("googleMapsUri") or ""):
        print(f"Place {place_id} is not the Pink Accounting profile (cid {CID}). Refusing.", file=sys.stderr)
        return 1

    data = normalise(detail)
    if not data["rating"] or not data["count"]:
        print("Response carried no rating or count. Leaving the committed file alone.", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}: {data['rating']} from {data['count']} reviews, "
          f"{len(data['reviews'])} quotes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
