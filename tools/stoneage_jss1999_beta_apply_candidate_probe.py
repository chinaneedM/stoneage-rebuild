#!/usr/bin/env python3
"""Test a tiny, explicitly hypothetical set of JSS beta-application URLs.

The Play Online scan proves the host and tail PO/sa_apply.html but leaves one
preceding character unresolved. This probe does NOT choose that character.
It checks only two evidence-motivated syntactic candidates through Wayback
Availability: old-style user-directory "~PO" (including URI-encoded %7E) and
plain "/PO". Negative results eliminate only these candidates.
"""

from __future__ import annotations

import concurrent.futures
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
AVAIL="https://archive.org/wayback/available"

CANDIDATES=(
    (
        "tilde-userdir",
        "http://www.dp.gamersdream.ne.jp/~PO/sa_apply.html",
    ),
    (
        "tilde-userdir-encoded",
        "http://www.dp.gamersdream.ne.jp/%7EPO/sa_apply.html",
    ),
    (
        "plain-po",
        "http://www.dp.gamersdream.ne.jp/PO/sa_apply.html",
    ),
    (
        "tilde-userdir-bare-host",
        "http://dp.gamersdream.ne.jp/~PO/sa_apply.html",
    ),
    (
        "plain-po-bare-host",
        "http://dp.gamersdream.ne.jp/PO/sa_apply.html",
    ),
)

KEY_DATES=(
    "19990801",
    "19990810",
    "19990820",
    "19990901",
    "19990915",
    "19990930",
)


def request_json(url,*,timeout=10):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Accept":"application/json"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8","replace"))


def parse_closest(payload):
    snapshots=payload.get("archived_snapshots")
    if not isinstance(snapshots,dict):
        return None
    closest=snapshots.get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return None
    return {
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def query_url(original,date):
    return AVAIL+"?"+urllib.parse.urlencode(
        {"url":original,"timestamp":date}
    )


def candidate_period_hit(closest):
    if closest is None:
        return False
    timestamp=str(closest.get("timestamp",""))
    status=str(closest.get("status",""))
    return timestamp.startswith("1999") and status=="200"


def clean(value,limit=900):
    value=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f").replace("|","%7C")[:limit]


def probe(job):
    label,original,date=job
    endpoint=query_url(original,date)
    try:
        closest=parse_closest(request_json(endpoint))
        return label,original,date,closest,None
    except Exception as exc:
        return label,original,date,None,(type(exc).__name__,str(exc))


def main():
    print("StoneAge JSS 1999 beta application candidate Availability probe — R1")
    print("SCOPE|explicit-hypotheses-only|availability-metadata|no-page-body")
    print("EVIDENCE_BOUNDARY|negative-result=absence-of-archive-capture-only|does-not-disprove-printed-url")
    print("KNOWN|host=www.dp.gamersdream.ne.jp|tail=PO/sa_apply.html|preceding-character=OPEN")
    print("DATES|"+",".join(KEY_DATES))

    jobs=[
        (label,original,date)
        for label,original in CANDIDATES
        for date in KEY_DATES
    ]
    rows=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for label,original,date,closest,error in pool.map(probe,jobs):
            if error:
                errors.append((label,original,date,error[0],error[1]))
            else:
                rows.append((label,original,date,closest))

    hits={}
    for label,original,date,closest in rows:
        if candidate_period_hit(closest):
            key=(label,original,closest["timestamp"],closest["url"])
            hits.setdefault(key,(label,original,closest))

    print(f"COUNT|queries|{len(jobs)}")
    print(f"COUNT|queries_succeeded|{len(rows)}")
    print(f"COUNT|queries_failed|{len(errors)}")
    print(f"COUNT|1999_candidate_capture_hits|{len(hits)}")

    for label,original,date,closest in rows:
        if closest is None:
            print(
                f"AVAIL|candidate={clean(label)}|requested={date}|"
                f"available=0|original={clean(original)}"
            )
            continue
        print(
            f"AVAIL|candidate={clean(label)}|requested={date}|available=1|"
            f"period_hit={int(candidate_period_hit(closest))}|"
            f"timestamp={clean(closest['timestamp'])}|status={clean(closest['status'])}|"
            f"original={clean(original)}|snapshot={clean(closest['url'])}"
        )

    for label,original,date,kind,message in errors:
        print(
            f"ERROR|candidate={clean(label)}|requested={date}|kind={clean(kind)}|"
            f"original={clean(original)}|message={clean(message)}"
        )

    for _,(label,original,closest) in sorted(hits.items()):
        print(
            f"HIT|candidate={clean(label)}|timestamp={clean(closest['timestamp'])}|"
            f"original={clean(original)}|snapshot={clean(closest['url'])}"
        )

    if hits:
        print("RESOLUTION|CANDIDATE_CAPTURE_FOUND|inspect literal archived original before promotion")
    elif rows and errors:
        print("RESOLUTION|PARTIAL_NO_CANDIDATE_CAPTURE|printed character remains OPEN")
    elif rows:
        print("RESOLUTION|BOUNDED_NO_CANDIDATE_CAPTURE|printed character remains OPEN")
    else:
        print("RESOLUTION|INCONCLUSIVE|all Availability queries failed")


if __name__=="__main__":
    main()
