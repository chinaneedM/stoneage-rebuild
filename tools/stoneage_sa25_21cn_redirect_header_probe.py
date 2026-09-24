#!/usr/bin/env python3
"""Recover archived 21CN downit redirect headers for StoneAge 2.5 record 20165.

Redirect following is disabled. At most a tiny response body is read from the archived
downit wrapper; the historical ZIP target is never requested or downloaded.
"""
from __future__ import annotations

import concurrent.futures
import re
import urllib.error
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CASES=(
    ("num0-20021017","20021017194106","http://download.21cn.com:80/downit.php?id=20165&num=0"),
    ("num0-20030318","20030318074019","http://download.21cn.com:80/downit.php?id=20165&num=0"),
    ("num0-20030422","20030422235035","http://download.21cn.com:80/downit.php?id=20165&num=0"),
    ("plain-20040824","20040824222843","http://download.21cn.com:80/downit.php?id=20165"),
    ("plain-20041026","20041026191344","http://download.21cn.com:80/downit.php?id=20165"),
)
URL_RE=re.compile(r"""(?i)(https?://[^"'\s<>]+|(?:location|url)\s*[=:]\s*["']?([^"'\s<>]+))""")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def clean(v,limit=2200):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def replay_urls(ts,url):
    return (
        f"https://web.archive.org/web/{ts}id_/{url}",
        f"https://web.archive.org/web/{ts}/{url}",
    )


def body_targets(body):
    out=[]
    seen=set()
    for m in URL_RE.finditer(body or ""):
        value=(m.group(2) or m.group(1) or "").strip()
        if not value:
            continue
        low=value.lower()
        if "sa25" in low or "file" in low or "game" in low or "download.21cn" in low:
            if value not in seen:
                seen.add(value); out.append(value)
    return tuple(out)


def one(case):
    label,ts,url=case
    opener=urllib.request.build_opener(NoRedirect)
    errors=[]
    for replay in replay_urls(ts,url):
        req=urllib.request.Request(replay,headers={"User-Agent":UA,"Accept":"*/*"})
        try:
            with opener.open(req,timeout=18) as r:
                body=r.read(4096).decode("latin-1","replace")
                return {
                    "label":label,"timestamp":ts,"url":url,"replay":replay,
                    "status":getattr(r,"status",200),
                    "location":r.headers.get("Location",""),
                    "content_location":r.headers.get("Content-Location",""),
                    "body":body,"targets":body_targets(body),"error":"",
                }
        except urllib.error.HTTPError as exc:
            if exc.code in (301,302,303,307,308):
                body=exc.read(4096).decode("latin-1","replace")
                return {
                    "label":label,"timestamp":ts,"url":url,"replay":replay,
                    "status":exc.code,
                    "location":exc.headers.get("Location",""),
                    "content_location":exc.headers.get("Content-Location",""),
                    "body":body,"targets":body_targets(body),"error":"",
                }
            errors.append(f"{type(exc).__name__}:{exc}")
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
    return {
        "label":label,"timestamp":ts,"url":url,"replay":"",
        "status":"","location":"","content_location":"","body":"","targets":(),
        "error":"; ".join(errors),
    }


def main():
    print("StoneAge 2.5 21CN record 20165 archived redirect-header probe — R1")
    print("SCOPE|archived-downit-wrapper-only|redirect-following-disabled|no-zip-payload-download")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        results=list(ex.map(one,CASES))

    print(f"COUNT|cases|{len(CASES)}")
    print(f"COUNT|responses|{sum(not r['error'] for r in results)}")
    print(f"COUNT|locations|{sum(bool(r['location']) for r in results)}")
    print(f"COUNT|body_targets|{sum(len(r['targets']) for r in results)}")
    print(f"COUNT|errors|{sum(bool(r['error']) for r in results)}")

    for r in results:
        if r["error"]:
            print(
                f"ERROR|label={clean(r['label'])}|timestamp={r['timestamp']}|"
                f"url={clean(r['url'])}|message={clean(r['error'])}"
            )
            continue
        print(
            f"RESPONSE|label={clean(r['label'])}|timestamp={r['timestamp']}|status={r['status']}|"
            f"url={clean(r['url'])}|replay={clean(r['replay'])}|"
            f"location={clean(r['location'])}|content_location={clean(r['content_location'])}|"
            f"body={clean(r['body'],2600)}"
        )
        for n,target in enumerate(r["targets"],1):
            print(f"BODY_TARGET|label={clean(r['label'])}|order={n}|value={clean(target,2200)}")

    print("EVIDENCE_BOUNDARY|a recovered Location/body target establishes 21CN mirror routing only; it does not recover or authenticate the target ZIP bytes.")


if __name__=="__main__":
    main()
