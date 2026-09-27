#!/usr/bin/env python3
"""Recover the source-linked Waei StoneAge early download page.

The target path is directly linked from a preserved Dec-2000 first-party
StoneAge page:
  /wgs/stoneage/content/down_loan.htm

This probe inventories all Wayback captures in the launch/trial window and
replays distinct HTTP-200 HTML bodies, extracting only text/navigation/download
targets. Linked client payloads are not downloaded.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
TARGETS=(
 "http://www7.waei.net/wgs/stoneage/content/down_loan.htm",
 "http://www7.waei.net:80/wgs/stoneage/content/down_loan.htm",
)
FROM="20001201"; TO="20010228"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"
TOKENS=("石器","石器時代","stoneage","下載","download","試玩","更新","版本","完整","安裝","容量","大小","MB","M","exe","zip","rar","ftp","http")

def clean(v,n=9000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=60,max_bytes=3*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(u):
    p=[("url",u),("matchType","exact"),("output","json"),("fl",FIELDS),
       ("from",FROM),("to",TO),("limit","5000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def decode(b):
    for enc in ("big5","cp950","gb18030","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def visible(t):
    v=re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>"," ",t)
    v=re.sub(r"(?is)<[^>]+>"," ",v)
    return clean(html.unescape(v),80000)

def title(t):
    m=re.search(r"(?is)<title\b[^>]*>(.*?)</title>",t)
    return clean(html.unescape(re.sub(r"(?is)<[^>]+>"," ",m.group(1)))) if m else ""

def refs(t,base):
    out=[];seen=set()
    for attr in ("href","src","action"):
        pat=rf"(?is)\b{attr}\s*=\s*([\"'])(.*?)\1"
        for m in re.finditer(pat,t):
            raw=html.unescape(m.group(2)).strip()
            if not raw or raw.lower().startswith(("javascript:","mailto:","#","data:")):continue
            u=urllib.parse.urljoin(base,raw)
            k=(attr,u)
            if k not in seen:seen.add(k);out.append(k)
    # Also recover naked FTP/HTTP URLs in page text/scripts.
    for m in re.finditer(r"(?i)(?:https?|ftp)://[^\s\"'<>]+",t):
        u=html.unescape(m.group(0)).rstrip(");,.")
        k=("naked",u)
        if k not in seen:seen.add(k);out.append(k)
    return out

def score(u):
    low=urllib.parse.unquote_plus(u).lower()
    score=0
    if any(low.endswith(x) for x in (".exe",".zip",".rar",".cab",".bin",".iso")):score+=5
    if low.startswith("ftp:"):score+=4
    if any(x in low for x in ("stone","sa_","setup","install","client","trial","demo","download")):score+=3
    if "waei" in low or "wayi" in low:score+=1
    return score

def snippets(v):
    lo=v.lower();out=[];seen=set()
    for token in TOKENS:
        start=0
        while True:
            i=lo.find(token.lower(),start)
            if i<0:break
            s=clean(v[max(0,i-400):min(len(v),i+len(token)+500)],1800)
            if s and s not in seen:seen.add(s);out.append((token,s))
            start=i+max(1,len(token))
            if len(out)>=24:return out
    return out

def main():
    print("StoneAge Waei early first-party down_loan recovery — R1")
    print(f"SOURCE|preserved StoneAge page link|path=/wgs/stoneage/content/down_loan.htm")
    print(f"SCOPE|Wayback exact captures + bounded HTML replay|{FROM}..{TO}|no linked client payload")
    rows={};errors=[]
    for u in TARGETS:
        try:
            st,final,b=fetch(cdx_url(u));rr=parse(b)
            print(f"QUERY|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|url={clean(u)}|final={clean(final)}")
            for r in rr:
                k=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""),str(r.get("statuscode") or ""))
                rows[k]=r
        except Exception as e:
            errors.append(("cdx:"+u,type(e).__name__,str(e)))
    ordered=sorted(rows.values(),key=lambda r:str(r.get("timestamp") or ""))
    for r in ordered:
        print("ROW|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
            clean(r.get("timestamp")),clean(r.get("statuscode")),clean(r.get("mimetype")),clean(r.get("length")),
            clean(r.get("digest")),clean(r.get("redirect")),clean(r.get("original"))
        ))
    seen_digest=set();download_targets=[]
    for r in ordered:
        if str(r.get("statuscode") or "")!="200":continue
        if "html" not in str(r.get("mimetype") or "").lower():continue
        dig=str(r.get("digest") or "")
        if dig and dig in seen_digest:continue
        seen_digest.add(dig)
        ts=str(r.get("timestamp") or ""); orig=str(r.get("original") or "")
        try:
            st,final,b=fetch(f"https://web.archive.org/web/{ts}id_/{orig}")
            enc,t=decode(b);v=visible(t);rr=refs(t,orig)
            print(f"PAGE|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={clean(title(t))}|refs={len(rr)}|final={clean(final)}")
            print(f"VISIBLE|timestamp={ts}|text={clean(v,14000)}")
            for tok,s in snippets(v):
                print(f"SNIPPET|timestamp={ts}|token={clean(tok)}|text={clean(s,2000)}")
            for kind,u in rr:
                sc=score(u)
                if sc:
                    download_targets.append((sc,ts,kind,u))
                    print(f"TARGET|timestamp={ts}|score={sc}|kind={kind}|url={clean(u)}")
        except Exception as e:
            errors.append(("replay:"+ts,type(e).__name__,str(e)))
    for sc,ts,kind,u in sorted(set(download_targets),key=lambda x:(-x[0],x[1],x[3])):
        print(f"RANKED_TARGET|score={sc}|timestamp={ts}|kind={kind}|url={clean(u)}")
    print(f"COUNT|cdx_rows|{len(ordered)}")
    print(f"COUNT|distinct_html_digests|{len(seen_digest)}")
    print(f"COUNT|download_targets|{len(set(download_targets))}")
    for scope,k,m in errors:print(f"ERROR|scope={clean(scope)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if download_targets:
        print("RESOLUTION|EARLY_STONEAGE_DOWNLOAD_TARGET_RECOVERED|probe exact highest-score target metadata next")
    elif seen_digest:
        print("RESOLUTION|EARLY_STONEAGE_DOWNLOAD_PAGE_RECOVERED_NO_DIRECT_PAYLOAD|use page wording/adjacent first-party routes next")
    elif errors:
        print("RESOLUTION|PARTIAL_DOWN_LOAN_RECOVERY|retry failed exact archive surface only")
    else:
        print("RESOLUTION|DOWN_LOAN_ARCHIVE_NOT_INDEXED|retain source-linked route as historical topology")
    print("EVIDENCE_BOUNDARY|page/link recovery does not authenticate any unpreserved client bytes; linked payloads are not fetched.")

if __name__=="__main__":main()
