#!/usr/bin/env python3
"""Replay the only two preserved www9 Waei download.php pages in the trial window."""
from __future__ import annotations
import hashlib,html,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CAPTURES=(
 ("root","20001206135100","http://www9.waei.net:80/download.php"),
 ("dcat5","20001206142600","http://www9.waei.net:80/download.php?Dcat_ID=5"),
)
def fetch(url,timeout=40,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*;q=0.1","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b
def decode(b):
    for enc in ("big5","cp950","gb18030","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")
def plain(s):
    s=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",s)
    s=re.sub(r"(?is)<[^>]+>"," ",s)
    return re.sub(r"\s+"," ",html.unescape(s)).strip()
def links(s,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',s):
        href=html.unescape(m.group(1)).strip()
        if not href or href.lower().startswith(("javascript:","mailto:","#")):continue
        out.append((urllib.parse.urljoin(base,href),plain(m.group(2))))
    return out
def main():
    print("StoneAge Waei www9 preserved download pages replay — R1")
    print("SCOPE|two exact Dec-2000 HTML captures|no binary payload")
    for label,ts,orig in CAPTURES:
        url=f"https://web.archive.org/web/{ts}id_/{orig}"
        st,final,b=fetch(url);enc,text=decode(b);vis=plain(text);ls=links(text,orig)
        title=""
        m=re.search(r"(?is)<title[^>]*>(.*?)</title>",text)
        if m:title=plain(m.group(1))
        print(f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={title}|links={len(ls)}|final={final}")
        print(f"VISIBLE|label={label}|text={vis[:12000].replace('|','%7C')}")
        for href,anchor in ls:
            print(f"LINK|label={label}|anchor={anchor.replace('|','%7C')[:1000]}|href={href.replace('|','%7C')[:5000]}")
    print("EVIDENCE_BOUNDARY|HTML page content can identify categories/listings but does not authenticate unpreserved download bytes.")
if __name__=="__main__":main()
