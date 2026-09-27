#!/usr/bin/env python3
"""Retry only the preserved Waei www9 download root capture from 2000-12-06.

Prior R1 located the capture but replay timed out. This bounded retry extracts
category/download routing and StoneAge/trial/size semantics from HTML only.
No linked payload is fetched.
"""
from __future__ import annotations
import hashlib, html, re, time, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20001206135100"
ORIG="http://www9.waei.net:80/download.php"
REPLAYS=(
    f"https://web.archive.org/web/{TS}id_/{ORIG}",
    f"https://web.archive.org/web/{TS}if_/{ORIG}",
    f"https://web.archive.org/web/{TS}/{ORIG}",
)
MAX=2*1024*1024

def clean(v,n=4000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,attempts=3,timeout=45):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*;q=0.2","Accept-Encoding":"identity"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(MAX+1)
                if len(b)>MAX: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b,i+1
        except Exception as e:
            last=e
            if i+1<attempts: time.sleep(2*(i+1))
    raise last

def decode(b):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def plain(t):
    p=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",t)
    p=html.unescape(re.sub(r"(?s)<[^>]+>"," ",p))
    return re.sub(r"\s+"," ",p)

def links(t,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',t):
        h=html.unescape(m.group(1)).strip()
        a=clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2))),1200)
        if not h or h.lower().startswith(("javascript:","mailto:","#")):continue
        out.append((urllib.parse.urljoin(base,h),a))
    return out

def snippets(p):
    needles=("石器時代","石器时代","石器","試玩","试玩","測試","测试","download","下載","下载","274","MB")
    low=p.lower(); out=[]
    for n in needles:
        start=0; nl=n.lower()
        while True:
            i=low.find(nl,start)
            if i<0:break
            s=clean(p[max(0,i-260):min(len(p),i+520)],1400)
            if s not in out:out.append(s)
            start=i+max(1,len(n))
    return out[:30]

def relevant(u,a):
    s=(u+" "+a).lower()
    return any(x in s for x in ("download.php","downloading.php","dcat_id","石器","stoneage","試玩","试玩","測試","测试"))

def main():
    print("StoneAge Waei www9 2000-12-06 download-root replay residual — R2")
    print("SCOPE|known preserved root capture only|HTML routing+semantics|no linked payload")
    errors=[]
    for idx,url in enumerate(REPLAYS,1):
        try:
            st,final,h,b,attempt=fetch(url)
            enc,t=decode(b); p=plain(t); ls=links(t,ORIG)
            rel=[x for x in ls if relevant(*x)]
            stone=tuple(x for x in ("石器時代","石器时代","StoneAge","stoneage") if x.lower() in p.lower())
            trial=tuple(x for x in ("試玩","试玩","測試","测试","trial","demo") if x.lower() in p.lower())
            sizes=tuple(dict.fromkeys(m.group(0) for m in re.finditer(r"(?<!\d)(?:27[0-9](?:\.\d+)?)\s*(?:m|mb|兆)",p,re.I)))
            print(f"PAGE|variant={idx}|attempt={attempt}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|stone={clean(','.join(stone))}|trial={clean(','.join(trial))}|size_tokens={clean(','.join(sizes))}|links={len(ls)}|relevant_links={len(rel)}|final={clean(final)}")
            print(f"VISIBLE|text={clean(p,12000)}")
            for u,a in rel:
                q=urllib.parse.parse_qs(urllib.parse.urlsplit(u).query.replace("%26","&"))
                dcat=(q.get("Dcat_ID") or q.get("dcat_id") or [""])[0]
                did=(q.get("ID") or q.get("id") or [""])[0]
                print(f"LINK|dcat={clean(dcat)}|id={clean(did)}|anchor={clean(a)}|url={clean(u)}")
            for s in snippets(p):
                print(f"SNIPPET|text={s}")
            print("RESOLUTION|ROOT_CAPTURE_REPLAYED|classify any StoneAge/trial category or downloading-ID route next")
            print("EVIDENCE_BOUNDARY|HTML proves historical listing/routing only; linked executables/archives are not fetched.")
            return
        except Exception as e:
            errors.append((idx,type(e).__name__,str(e)))
            print(f"ERROR|variant={idx}|kind={type(e).__name__}|message={clean(e)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|ROOT_CAPTURE_REPLAY_STILL_FAILED|retain known CDX capture and pursue alternate mirrors/captures only")

if __name__=="__main__":
    main()
