#!/usr/bin/env python3
"""Replay a bounded set of Dec-2000/Jan-2001 Waei StoneAge-adjacent pages.

Targets come directly from the already recovered early-Waei CDX census:
- forum classid=sasp
- forum Brd_172 / Brd_173
- www7 /wgs/stoneage/ bad-list page
- gamedetail P_ID=131, the product-detail capture adjacent in time
No linked payloads are downloaded.
"""
from __future__ import annotations
import hashlib,html,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGETS=(
 ("brd172","20001213182500","http://www6.waei.net:80/forum.php?classid=Brd_172&GCAction=display"),
 ("sasp","20001213211300","http://www6.waei.net:80/forum.php?classid=sasp%26GCAction=display"),
 ("brd173","20010107210200","http://www6.waei.net:80/forum.php?classid=Brd_173%26GCAction=display"),
 ("stoneage-badlist","20001207211100","http://www7.waei.net:80/wgs/stoneage/content/bad_list/badlist-3.htm"),
 ("pid131","20001207033400","http://www9.waei.net:80/gamedetail.php?P_ID=131"),
)
TOKENS=("石器","石器時代","stoneage","stone age","下載","試玩","遊戲","討論","論壇","WGS","華義","P_ID","gamedetail","download")
MAX=2*1024*1024

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(ts,orig):
    url=f"https://web.archive.org/web/{ts}id_/{orig}"
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(MAX+1)
        if len(b)>MAX: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def decode(b):
    for enc in ("big5","cp950","gb18030","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def title(t):
    m=re.search(r"(?is)<title\b[^>]*>(.*?)</title>",t)
    return clean(html.unescape(re.sub(r"(?is)<[^>]+>"," ",m.group(1)))) if m else ""

def visible(t):
    v=re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>"," ",t)
    v=re.sub(r"(?is)<[^>]+>"," ",v)
    return clean(html.unescape(v),60000)

def links(t,base):
    out=[];seen=set()
    for m in re.finditer(r"(?is)<a\b[^>]*href\s*=\s*([\"'])(.*?)\1[^>]*>(.*?)</a>",t):
        raw=html.unescape(m.group(2)).strip()
        if not raw or raw.lower().startswith(("javascript:","mailto:","#")):continue
        u=urllib.parse.urljoin(base,raw)
        a=clean(html.unescape(re.sub(r"(?is)<[^>]+>"," ",m.group(3))),1500)
        k=(u,a)
        if k not in seen:seen.add(k);out.append(k)
    return out

def token_hits(v):
    lo=v.lower()
    return [x for x in TOKENS if x.lower() in lo]

def snippets(v,hits,radius=320):
    lo=v.lower();out=[];seen=set()
    for h in hits:
        i=lo.find(h.lower())
        if i<0:continue
        s=clean(v[max(0,i-radius):min(len(v),i+len(h)+radius)],1200)
        if s and s not in seen:seen.add(s);out.append((h,s))
    return out

def score_link(u,a):
    s=(urllib.parse.unquote_plus(u)+" "+a).lower()
    return sum(1 for x in ("stone","石器","sasp","brd_17","game","gamedetail","download","trial","試玩","wgs") if x in s)

def main():
    print("StoneAge Waei early product/forum identity replay — R1")
    print("SCOPE|5 source-grounded exact archived HTML pages|2000-12..2001-01|no linked payload")
    errors=[];targets=[]
    for label,ts,orig in TARGETS:
        try:
            st,final,b=fetch(ts,orig);enc,t=decode(b);v=visible(t);hits=token_hits(v);ls=links(t,orig)
            print(f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={clean(title(t))}|hits={clean(','.join(hits))}|links={len(ls)}|final={clean(final)}")
            print(f"VISIBLE|label={label}|text={clean(v,9000)}")
            for h,s in snippets(v,hits):
                print(f"SNIPPET|label={label}|token={clean(h)}|text={clean(s,1400)}")
            for u,a in ls:
                sc=score_link(u,a)
                if sc:
                    targets.append((sc,label,u,a))
                    print(f"LINK|label={label}|score={sc}|anchor={clean(a)}|url={clean(u)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
            print(f"ERROR|label={label}|kind={type(e).__name__}|message={clean(e)}")
    for sc,label,u,a in sorted(targets,key=lambda x:(-x[0],x[1],x[2]))[:120]:
        print(f"RANKED|score={sc}|from={label}|anchor={clean(a)}|url={clean(u)}")
    print(f"COUNT|ranked_links|{len(targets)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|EARLY_IDENTITY_REPLAY_COMPLETE|use only directly named StoneAge product/forum identifiers as next targets")
    print("EVIDENCE_BOUNDARY|forum/product HTML identifies historical routing and names only; no linked client payload is fetched.")

if __name__=="__main__":main()
