import urllib.request

req = urllib.request.Request(
    "https://www.serviceprofit.com.au/",
    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
)
with urllib.request.urlopen(req) as r:
    h = r.read().decode("utf-8", "replace")
    print("last-modified", r.headers.get("Last-Modified"))
    print("age", r.headers.get("Age"))
    print("rt3", "v=rt3" in h)
    print("arw", 'class="arw"' in h)
    print("len", len(h))
