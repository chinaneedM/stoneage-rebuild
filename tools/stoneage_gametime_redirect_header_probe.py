#!/usr/bin/env python3
"""Recover Location headers from archived GameTime download 302 responses.

The normal URL opener follows redirects and loses the historical attachment
target. This probe disables redirect following and records response headers only.
No client payload bytes are requested.
"""

from __future__ import annotations

import concurrent.futures
import urllib.error
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CASES=[
    ("gw9-20010614","20010614215330","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("gw9-20010806","20010806022454","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("gw9-20011215","20011215020725","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("gw9-20020208","20020208034143","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("gw76-20010706","20010706060327","http://www.gametime.co.kr/data/download.asp?GW_IDX=76&GW_Name=Online"),
    ("gw76-20010805","20010805231219","http://www.gametime.co.kr/data/download.asp?GW_IDX=76&GW_Name=Online"),
    ("gw76-20011106","20011106115109","http://www.gametime.co.kr/data/download.asp?GW_IDX=76&GW_Name=Online"),
    ("gw76-20011215","20011215000332","http://www.gametime.co.kr/data/download.asp?GW_IDX=76&GW_Name=Online"),
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def clean(v,limit=1600):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def replay_urls(ts,url):
    return [
        f"https://web.archive.org/web/{ts}id_/{url}",
        f"https://web.archive.org/web/{ts}/{url}",
    ]


def one(case):
    label,ts,url=case
    opener=urllib.request.build_opener(NoRedirect)
    errors=[]
    for replay in replay_urls(ts,url):
        req=urllib.request.Request(replay,headers={"User-Agent":UA,"Accept":"*/*"})
        try:
            with opener.open(req,timeout=15) as r:
                body=r.read(2048)
                return {
                    "label":label,"timestamp":ts,"url":url,"replay":replay,
                    "status":getattr(r,"status",200),
                    "location":r.headers.get("Location",""),
                    "content_location":r.headers.get("Content-Location",""),
                    "body":body.decode("latin-1","replace"),
                    "error":"",
                }
        except urllib.error.HTTPError as exc:
            if exc.code in (301,302,303,307,308):
                body=exc.read(2048)
                return {
                    "label":label,"timestamp":ts,"url":url,"replay":replay,
                    "status":exc.code,
                    "location":exc.headers.get("Location",""),
                    "content_location":exc.headers.get("Content-Location",""),
                    "body":body.decode("latin-1","replace"),
                    "error":"",
                }
            errors.append(f"{type(exc).__name__}:{exc}")
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
    return {
        "label":label,"timestamp":ts,"url":url,"replay":"",
        "status":"","location":"","content_location":"","body":"",
        "error":"; ".join(errors),
    }


def main():
    print("StoneAge GameTime archived 302 Location probe — R1")
    print("SCOPE|archived-response-headers-only|redirect-following-disabled|no-payload-download")
    print(f"COUNT|cases|{len(CASES)}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results=list(ex.map(one,CASES))

    print(f"COUNT|errors|{sum(bool(r['error']) for r in results)}")
    print(f"COUNT|responses|{sum(not r['error'] for r in results)}")
    print(f"COUNT|locations|{sum(bool(r['location']) for r in results)}")

    for r in results:
        if r["error"]:
            print(
                f"ERROR|label={clean(r['label'])}|timestamp={r['timestamp']}|"
                f"url={clean(r['url'])}|message={clean(r['error'])}"
            )
            continue
        print(
            f"RESPONSE|label={clean(r['label'])}|timestamp={r['timestamp']}|"
            f"status={r['status']}|url={clean(r['url'])}|replay={clean(r['replay'])}|"
            f"location={clean(r['location'])}|content_location={clean(r['content_location'])}|"
            f"body={clean(r['body'],1800)}"
        )


if __name__=="__main__":
    main()
