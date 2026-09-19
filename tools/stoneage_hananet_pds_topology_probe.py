#!/usr/bin/env python3
"""Recover sparse topology metadata from the archived Hananet PDS frameset."""

from __future__ import annotations

import hashlib
import html.parser
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
PAGES=[
    ("root","20001018214759","http://pds.hananet.net:80/"),
    ("index2","20001018214759","http://pds.hananet.net:80/index2.html"),
    ("topfrm","20001018214759","http://pds.hananet.net:80/topfrm.html"),
    ("nav","20001018214759","http://pds.hananet.net:80/nav.html"),
    ("top","20001018214759","http://pds.hananet.net:80/top.asp"),
    ("content","20001018214759","http://pds.hananet.net:80/content.html"),
    ("sub_c","20001018214759","http://pds.hananet.net:80/sub_c.html"),
    ("sub_c0","20001018214759","http://pds.hananet.net:80/sub_c0.asp"),
    ("sub_c1","20001018214759","http://pds.hananet.net:80/sub_c1.html"),
]
PATH_RE=re.compile(r"""(?ix)(?:https?://[a-z0-9._:/?&=%#~-]{4,}|[a-z0-9_./?-]{2,}\.(?:html?|asp|cgi|php|js)(?:\?[a-z0-9_=&%.-]+)?)""")
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs=[]
        self.inputs=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower(); a=dict(attrs)
        for attr in ("href","src","action"):
            if a.get(attr): self.refs.append((tag,attr,a[attr]))
        if tag=="input":
            self.inputs.append((a.get("type",""),a.get("name",""),a.get("value","")))


def request(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()


def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"


def normalize(base,target):
    target=target.strip()
    if not target or target.startswith(("javascript:","mailto:","#")):return ""
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def safe(v,limit=700):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def main():
    print("StoneAge Hananet PDS topology probe — R1")
    print("SCOPE|transient-html|hash-refs-form-fields-path-tokens-only|no-client-binary-download")
    for label,ts,original in PAGES:
        try:data=request(replay(ts,original))
        except Exception as exc:
            print(f"ERROR|page={label}|kind={type(exc).__name__}|message={safe(exc)}")
            continue
        text=data.decode("latin-1","replace")
        p=Parser(); p.feed(text)
        refs=sorted({(tag,attr,safe(normalize(original,target))) for tag,attr,target in p.refs if normalize(original,target)})
        toks=sorted({safe(x) for x in PATH_RE.findall(text)})
        print(f"PAGE|page={label}|timestamp={ts}|bytes={len(data)}|sha256={hashlib.sha256(data).hexdigest()}|url={safe(original)}")
        for tag,attr,target in refs:
            print(f"REF|page={label}|tag={tag}|attr={attr}|target={target}")
        for typ,name,value in p.inputs:
            print(f"INPUT|page={label}|type={safe(typ)}|name={safe(name)}|value={safe(value)}")
        for token in toks:
            print(f"TOKEN|page={label}|value={token}")

if __name__=="__main__":main()
