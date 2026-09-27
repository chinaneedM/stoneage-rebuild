#!/usr/bin/env python3
"""Inspect the archived 302 for Waei fileid=133 without following it."""
from __future__ import annotations
import hashlib, urllib.request, urllib.error

UA="stoneage-rebuild-archaeology/1.0"
TS="20010605174213"
ORIG="http://www7.waei.net:80/download/download.asp?fileid=133"
URL=f"https://web.archive.org/web/{TS}id_/{ORIG}"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def main():
    print("StoneAge Waei fileid=133 archived 302 header probe — R1")
    print("SCOPE|single archived route capture|no redirect follow|no linked binary payload")
    opener=urllib.request.build_opener(NoRedirect())
    req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept-Encoding":"identity"})
    try:
        with opener.open(req,timeout=45) as r:
            b=r.read(65536)
            print(f"RESPONSE|status={r.status}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|location={clean(r.headers.get('Location'))}|content_type={clean(r.headers.get('Content-Type'))}|final={clean(r.geturl())}")
    except urllib.error.HTTPError as e:
        b=e.read(65536)
        print(f"RESPONSE|status={e.code}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|location={clean(e.headers.get('Location'))}|content_type={clean(e.headers.get('Content-Type'))}|final={clean(e.geturl())}")
        text=b.decode("latin1","replace")
        print(f"BODY|{clean(text,4000)}")
        loc=str(e.headers.get("Location") or "")
        if "spr_1.bin" in loc.lower():
            print("RESOLUTION|DIRECT_BINDING|fileid=133 -> spr_1.bin")
        elif loc:
            print("RESOLUTION|REDIRECT_TARGET_FOUND|classify exact target next")
        else:
            print("RESOLUTION|302_WITHOUT_LOCATION_IN_REPLAY|use archived response body/header metadata")
    print("EVIDENCE_BOUNDARY|Only the archived redirect response is inspected; the redirect target is not fetched.")
if __name__=="__main__":main()
