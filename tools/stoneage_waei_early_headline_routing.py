#!/usr/bin/env python3
"""Extract raw HTML routing around retained early StoneAge headlines.

The known 2001-02-06 first-party homepage retains a Dec-1-2000 free-test
headline and Jan-4-2001 mainland-related headlines. This probe replays that one
known HTML capture and emits bounded raw/decoded contexts plus URL/action/query
tokens around those exact headlines. No linked page or payload is fetched.
"""
from __future__ import annotations
import hashlib, html, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010206195220"
PAGE="http://www7.waei.net:80/wgs/stoneage/"
MAX=1024*1024
NEEDLES=(
    "免費測試",
    "石器時代在大陸的熱鬧情形",
    "來自石器時代玩家的幽默",
)

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=45) as r:
        b=r.read(MAX+1)
        if len(b)>MAX:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def decode(b):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def raw_tokens(chunk):
    vals=[]
    patterns=(
      ("href",r'(?is)href\s*=\s*["\']([^"\']+)["\']'),
      ("src",r'(?is)src\s*=\s*["\']([^"\']+)["\']'),
      ("action",r'(?is)action\s*=\s*["\']([^"\']+)["\']'),
      ("onclick",r'(?is)onclick\s*=\s*["\']([^"\']+)["\']'),
      ("url",r'(?i)https?://[^\s\"\'<>]+'),
      ("query",r'(?i)\b(?:id|newsid|news_id|nid|no|sn|articleid|xnewsid)\s*=\s*[0-9]+'),
    )
    for kind,pat in patterns:
        for m in re.finditer(pat,chunk):
            val=m.group(1) if m.lastindex else m.group(0)
            row=(kind,html.unescape(val))
            if row not in vals: vals.append(row)
    return vals

def visible(chunk):
    x=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",chunk)
    return clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",x)),5000)

def main():
    print("StoneAge Waei retained early-headline HTML routing — R1")
    print("SCOPE|single known first-party 2001-02-06 homepage capture|bounded raw context|no linked fetch")
    try:
        st,final,h,b=fetch(f"https://web.archive.org/web/{TS}id_/{PAGE}")
    except Exception as e:
        print(f"ERROR|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|HOMEPAGE_REPLAY_FAILED|retain prior visible headline evidence")
        return
    enc,t=decode(b)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|final={clean(final)}")
    hits=0; route_tokens=0
    for needle in NEEDLES:
        start=0
        while True:
            i=t.find(needle,start)
            if i<0:break
            hits+=1
            chunk=t[max(0,i-1800):min(len(t),i+2200)]
            print(f"HIT|needle={clean(needle)}|offset={i}|visible={visible(chunk)}")
            print(f"RAW|needle={clean(needle)}|html={clean(chunk,12000)}")
            toks=raw_tokens(chunk);route_tokens+=len(toks)
            for kind,val in toks:
                print(f"TOKEN|needle={clean(needle)}|kind={kind}|value={clean(val)}")
            start=i+len(needle)
    print(f"COUNT|hits|{hits}")
    print(f"COUNT|route_tokens|{route_tokens}")
    if hits and route_tokens:
        print("RESOLUTION|EARLY_HEADLINE_ROUTING_CONTEXT_RECOVERED|classify article/detail token nearest Dec-1 headline")
    elif hits:
        print("RESOLUTION|HEADLINES_ARE_RETAINED_WITHOUT_ROUTE_TOKEN|use month archive or external mirror for body")
    else:
        print("RESOLUTION|EXPECTED_HEADLINE_NOT_FOUND|do not override prior decoded-page evidence")
    print("EVIDENCE_BOUNDARY|Proximity in raw HTML can recover routing structure, but only direct target replay can authenticate article content.")

if __name__=="__main__":main()
