#!/usr/bin/env python3
"""Locate Inium's trial-client menu/page from archived sitemap/main menu pages."""

from __future__ import annotations
import concurrent.futures, html.parser, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
AVAIL="https://archive.org/wayback/available"
DATES=["20010413","20010614","20010801"]
PAGES=["sitemap.htm","main_1.htm","main_2.htm","main_3.htm","main_3_2.htm","main_3_3.htm",
       "main_4.htm","main_4_2.htm","main_4_3.htm","main_5.htm","main_6.htm","main_7.htm",
       "main_8.htm","main_9.htm","main_hot.htm"]
ROOT="http://stoneage.enium.co.kr/"
KEY=re.compile(r"(?i)(체험|trial|demo|다운로드|download|sa_demo|\.exe|\.zip)")

class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.links=[];self.text=[];self._href=None;self._a=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);tag=tag.lower()
        if tag=="a" and a.get("href"):self._href=a["href"];self._a=[]
        for k in ("src","action","onclick"):
            if a.get(k):self.links.append((tag,k,a[k],""))
    def handle_data(self,d):
        if d.strip():self.text.append(d)
        if self._href is not None:self._a.append(d)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.links.append(("a","href",self._href," ".join(self._a).strip()));self._href=None;self._a=[]

def get(url,timeout=12):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()

def availability(url,date):
    q=urllib.parse.urlencode({"url":url,"timestamp":date})
    o=json.loads(get(AVAIL+"?"+q,8).decode("utf-8","replace"))
    c=o.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):return None
    return str(c.get("timestamp",""))

def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"

def decode(b):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return b.decode(enc)
        except UnicodeDecodeError:pass
    return b.decode("latin-1","replace")

def safe(v,n=700):
    v=" ".join(str(v).split())
    return "".join(c for c in v if c>=" " and c!="\x7f").replace("|","%7C")[:n]

def analyze(url,ts):
    text=decode(get(replay(ts,url),15));p=P();p.feed(text)
    hits=[]
    for tag,attr,target,label in p.links:
        absolute=urllib.parse.urljoin(url,target) if not target.lower().startswith("javascript:") else target
        if KEY.search(absolute+" "+label):hits.append(("LINK",tag,attr,absolute,label))
    for t in p.text:
        line=safe(t,300)
        if KEY.search(line):hits.append(("TEXT","","",line,""))
    return hits

def main():
    print("StoneAge Inium trial-menu locator — R1")
    print("SCOPE|archived-menu-metadata-only|no-client-binary-download")
    jobs=[(page,date,ROOT+page) for page in PAGES for date in DATES]
    av=[];errors=[]
    def one(x):
        page,date,url=x
        try:return page,date,url,availability(url,date),None
        except Exception as e:return page,date,url,None,(type(e).__name__,str(e))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for page,date,url,ts,err in ex.map(one,jobs):
            if err:errors.append(("availability",page,date,err[0],err[1]))
            elif ts:av.append((page,date,url,ts))
    unique={(page,url,ts) for page,date,url,ts in av}
    found=[]
    for page,url,ts in sorted(unique):
        try:hits=analyze(url,ts)
        except Exception as e:
            errors.append(("replay",page,ts,type(e).__name__,str(e)));continue
        for h in hits:found.append((page,ts)+h)
    print(f"COUNT|availability_queries|{len(jobs)}")
    print(f"COUNT|available_page_snapshots|{len(unique)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|trial_download_hits|{len(found)}")
    for phase,page,marker,kind,msg in errors:
        print(f"ERROR|phase={phase}|page={safe(page)}|marker={safe(marker)}|kind={safe(kind)}|message={safe(msg)}")
    for page,ts,kind,tag,attr,value,label in sorted(found):
        print(f"HIT|page={page}|timestamp={ts}|kind={kind}|tag={tag}|attr={attr}|value={safe(value)}|label={safe(label,250)}")

if __name__=="__main__":main()
