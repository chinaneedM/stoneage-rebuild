#!/usr/bin/env python3
"""Replay the preserved Waei StoneAge /saupdate/ directory index from 2001-05-30.

This is a metadata/navigation recovery probe. It parses the archived directory
listing for filenames, hrefs and surrounding row text, but downloads no linked
payloads.
"""
from __future__ import annotations

import hashlib
import html
from html.parser import HTMLParser
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TIMESTAMP="20010530234248"
ORIGINAL="http://stoneage.waei.net:80/saupdate/?M=D"
REPLAY=f"https://web.archive.org/web/{TIMESTAMP}id_/{ORIGINAL}"
MAX=2*1024*1024

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch():
    req=urllib.request.Request(REPLAY,headers={
      "User-Agent":UA,
      "Accept":"text/html,text/plain,*/*;q=0.2",
      "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(MAX+1)
        if len(b)>MAX: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def decode(body):
    for enc in ("big5","cp950","gb18030","utf-8","latin1"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",body.decode("latin1","replace")

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.text=[]
        self._a=None
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            d=dict(attrs)
            self._a={"href":d.get("href",""),"parts":[]}
    def handle_data(self,data):
        self.text.append(data)
        if self._a is not None:self._a["parts"].append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._a is not None:
            self.links.append((self._a["href"],"".join(self._a["parts"])))
            self._a=None

def likely_payload(url,text):
    low=urllib.parse.unquote_plus((url+" "+text)).lower()
    return any(x in low for x in (
      "sa_",".exe",".bin",".txt",".dat",".zip",".cab",".rar",
      "real_","adrn_","spr_","spradrn_","battle_","sound_","soundaddr","battletxt","newest"
    ))

def generations(value):
    s=urllib.parse.unquote_plus(value)
    found=[]
    for m in re.finditer(r"(?i)(sa|real|adrn|spr|spradrn|battle|sound|soundaddr|battletxt)_([0-9]+)",s):
        found.append((m.group(1).lower(),int(m.group(2))))
    return found

def main():
    print("StoneAge Waei /saupdate/ archived directory replay — R1")
    print(f"SCOPE|exact archived directory index|timestamp={TIMESTAMP}|navigation/text only|no linked payload")
    st,final,h,b=fetch()
    enc,text=decode(b)
    p=P();p.feed(text)
    visible=clean(html.unescape(" ".join(p.text)),50000)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|links={len(p.links)}|content_type={clean(h.get('Content-Type'))}|final={clean(final)}")
    print(f"VISIBLE|text={clean(visible,12000)}")
    uniq=[];seen=set()
    gen={}
    for href,anchor in p.links:
        absolute=urllib.parse.urljoin(ORIGINAL,html.unescape(href).strip())
        key=absolute
        if not absolute or key in seen: continue
        seen.add(key)
        decoded=urllib.parse.unquote_plus(absolute)
        relevant=likely_payload(absolute,anchor)
        print(f"LINK|relevant={int(relevant)}|anchor={clean(html.unescape(anchor),1200)}|url={clean(absolute)}|decoded={clean(decoded,1800)}")
        if relevant: uniq.append((absolute,anchor))
        for kind,n in generations(decoded+" "+anchor):
            gen.setdefault(kind,set()).add(n)
    for kind in sorted(gen):
        vals=sorted(gen[kind])
        print(f"GENERATION_SET|kind={kind}|count={len(vals)}|min={min(vals)}|max={max(vals)}|values={','.join(str(x) for x in vals)}")
    print(f"COUNT|links|{len(seen)}")
    print(f"COUNT|relevant_links|{len(uniq)}")
    if uniq:
        print("RESOLUTION|SAUPDATE_DIRECTORY_INDEX_RECOVERED|probe earliest/highest-information listed runtime/resource paths next")
    else:
        print("RESOLUTION|SAUPDATE_DIRECTORY_INDEX_NO_PAYLOAD_LINKS|treat capture as weak directory-state evidence")
    print("EVIDENCE_BOUNDARY|directory listing proves paths visible in the archived page only; linked files are not downloaded by this probe.")

if __name__=="__main__":
    main()
