#!/usr/bin/env python3
"""Recover archived 21CN download-router topology for StoneAge 2.5 record 20165.

Metadata/HTML only. Redirects are deliberately NOT followed, so this probe never
downloads the historical game payload.
"""
from __future__ import annotations
import hashlib, html, re, time, urllib.error, urllib.request
from tools.stoneage_sa25_21cn_record20165_probe import ID, cdx_url, clean, parse, replay
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible

UA="stoneage-rebuild-archaeology/1.0"
TARGET=f"http://download.21cn.com/downit.php?id={ID}"
ATTR_RE=re.compile(r"""(?is)(?:href|src|content)\s*=\s*["']?([^"'<>]+)""")
URL_RE=re.compile(r"""(?i)https?://[^\s"'<>]+""")
JS_RE=re.compile(r"""(?is)(?:location(?:\.href)?|window\.location)\s*=\s*["']([^"']+)["']""")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fetch_no_redirect(url,timeout=25,max_bytes=1_000_000,attempts=3):
    opener=urllib.request.build_opener(NoRedirect)
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*"})
            try:
                r=opener.open(req,timeout=timeout)
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
            except urllib.error.HTTPError as e:
                b=e.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(e.code),e.geturl(),dict(e.headers.items()),b
        except Exception as e:
            last=e
            if n+1<attempts: time.sleep(1.0*(n+1))
    raise last

def candidate_refs(text):
    out=[]; seen=set()
    vals=[]
    vals.extend(ATTR_RE.findall(text))
    vals.extend(URL_RE.findall(text))
    vals.extend(JS_RE.findall(text))
    for raw in vals:
        v=html.unescape(str(raw)).strip()
        low=v.lower()
        if any(k in low for k in ("sa25up","download.21cn","202.104.32.168","/file/","/file1","downit.php")):
            if v not in seen:
                seen.add(v); out.append(v)
    return tuple(out)

def main():
    print("StoneAge 2.5 21CN record 20165 download-router topology — R1")
    print("SCOPE|wayback-cdx+non-following-router-replay|metadata/html-only|no-game-payload")
    errors=[]
    try:
        st,final,hdr,b=fetch_no_redirect(cdx_url(TARGET,"prefix",1000),30,2_000_000,3)
        rows=parse(b)
        print(f"CDX_QUERY|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|final={clean(final)}")
    except Exception as e:
        rows=()
        errors.append(("cdx",type(e).__name__,str(e)))
    for r in rows:
        print(
            f"CDX_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|"
            f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
            f"digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
        )
        try:
            st,final,hdr,b=fetch_no_redirect(replay(r),22,1_000_000,2)
            enc,text=decode(b,declared_charset(b))
            loc=hdr.get("Location") or hdr.get("location") or ""
            refs=candidate_refs(text)
            print(
                f"REPLAY|timestamp={clean(r.get('timestamp'))}|status={st}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|"
                f"location={clean(loc,5000)}|final={clean(final,5000)}|refs={len(refs)}"
            )
            if b:
                print(f"BODY|timestamp={clean(r.get('timestamp'))}|value={clean(visible(text),7000)}")
            for n,v in enumerate(refs,1):
                print(f"REF|timestamp={clean(r.get('timestamp'))}|order={n}|value={clean(v,5000)}")
        except Exception as e:
            errors.append((f"replay:{r.get('timestamp')}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|rows|{len(rows)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|ROUTER_TOPOLOGY_CAPTURED|inspect Location/body refs for alternate historical mirrors")
    print("EVIDENCE_BOUNDARY|router metadata can identify historical delivery paths; it does not recover or authenticate payload bytes.")

if __name__=="__main__":
    main()
