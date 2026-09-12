"""Split hospitality and Service Profit Microsoft Bookings. No secrets logged."""
from __future__ import annotations

import json
import subprocess
import urllib.error
import urllib.request

GRAPH = "https://graph.microsoft.com/v1.0"
HOSP = "booking@pinktax.com.au"
SP = "ServiceProfit@pinktax.com.au"
LEAKED = "186e9a83-c054-49f6-a7ea-e9036b85ecb1"
HOSP_DISCOVERY = "7927082f-f5f4-4722-894a-ce4d2146209f"
SP_CALL = "622b3116-d18c-4dee-a65a-8561e37712a3"
HOSP_STAFF = "bcb02096-f46a-4fcb-a1d8-66401aa06276"


def token() -> str:
    return subprocess.check_output(
        ["python", r"C:\src\Pink-Accounting-Automation\scripts\quality-gate\Get-PinkAmeliaGraphToken.py"],
        text=True,
    ).strip()


def call(tok: str, path: str, method: str = "GET", body=None):
    url = GRAPH + path
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def add_question(tok: str, biz: str, name: str, kind: str, options=None):
    body = {
        "displayName": name,
        "answerInputType": kind,
        "answerOptions": options or [],
    }
    st, d = call(tok, f"/solutions/bookingBusinesses/{biz}/customQuestions", "POST", body)
    qid = d.get("id") if isinstance(d, dict) else None
    print("question", st, name, qid)
    if not qid:
        print("  body", str(d)[:500])
    return qid


def main():
    tok = token()
    print("token_len", len(tok))

    st, existing = call(tok, f"/solutions/bookingBusinesses/{HOSP}/customQuestions")
    names = {q.get("displayName"): q.get("id") for q in (existing.get("value") or [])} if isinstance(existing, dict) else {}
    print("hosp existing questions", list(names))

    staff_id = names.get("How many staff?") or add_question(
        tok,
        HOSP,
        "How many staff?",
        "radioButton",
        ["Just me", "1-5", "6-15", "16-30", "30+"],
    )
    pos_id = names.get("Where is the business now?") or add_question(
        tok,
        HOSP,
        "Where is the business now?",
        "text",
    )
    vis_id = names.get("Where do you want it in 12 months?") or add_question(
        tok,
        HOSP,
        "Where do you want it in 12 months?",
        "text",
    )

    st, svc = call(tok, f"/solutions/bookingBusinesses/{HOSP}/services/{HOSP_DISCOVERY}")
    current = svc.get("customQuestions") or []
    have = {q.get("questionId") for q in current}
    extra = []
    for qid in (staff_id, pos_id, vis_id):
        if qid and qid not in have:
            extra.append({"questionId": qid, "isRequired": True})
    patch = {
        "staffMemberIds": [HOSP_STAFF],
        "isHiddenFromCustomers": False,
    }
    if extra:
        patch["customQuestions"] = current + extra
    st, out = call(
        tok,
        f"/solutions/bookingBusinesses/{HOSP}/services/{HOSP_DISCOVERY}",
        "PATCH",
        patch,
    )
    print("patch hosp discovery", st, str(out)[:300])

    st, gone = call(
        tok,
        f"/solutions/bookingBusinesses/{HOSP}/services/{LEAKED}",
        "DELETE",
    )
    print("delete leaked SP service", st, str(gone)[:300])

    st, spq = call(tok, f"/solutions/bookingBusinesses/{SP}/customQuestions")
    sp_names = {q.get("displayName"): q.get("id") for q in (spq.get("value") or [])} if isinstance(spq, dict) else {}
    print("sp existing questions", list(sp_names))

    wanted = [
        ("What work?", "radioButton", ["Air con / refrigeration", "Electrical", "Construction services", "Mix of those"]),
        ("Annual revenue", "radioButton", ["Under $1M", "$1M-$3M", "$3M-$5M", "$5M+"]),
        ("Staff", "radioButton", ["Just me", "2 to 5", "6 to 15", "16 or more"]),
        ("What is hurting?", "text", None),
        ("Where is the business now?", "text", None),
        ("Where do you want it in 12 months?", "text", None),
    ]
    sp_ids = []
    for name, kind, opts in wanted:
        qid = sp_names.get(name) or add_question(tok, SP, name, kind, opts)
        if qid:
            sp_ids.append({"questionId": qid, "isRequired": True})

    st, out = call(
        tok,
        f"/solutions/bookingBusinesses/{SP}/services/{SP_CALL}",
        "PATCH",
        {"customQuestions": sp_ids, "isHiddenFromCustomers": False},
    )
    print("patch SP service questions", st, str(out)[:300])

    print("--- prove ---")
    for bid in (HOSP, SP):
        st, svcs = call(tok, f"/solutions/bookingBusinesses/{bid}/services")
        names = [
            (s.get("displayName"), s.get("staffMemberIds"), len(s.get("customQuestions") or []))
            for s in (svcs.get("value") or [])
        ]
        print(bid, names)


if __name__ == "__main__":
    main()
