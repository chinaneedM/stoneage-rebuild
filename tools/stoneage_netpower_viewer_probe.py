#!/usr/bin/env python3
"""Extract public GameMeca magazine viewer asset/path metadata.

Stores no magazine image bytes or article text; only URL/attribute/path tokens
needed to locate historically relevant scan pages.
"""

import html
import re
import urllib.parse
import urllib.request

URL="https://www.gamemeca.com/magazine/index.php?mgz=netpower&ym=2000_9"
UA="Mozilla/5.0 StoneAgeArchaeology/1.0"

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept-Language":"ko,en;q=0.8"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read().decode("utf-8","replace")

def clean(s):
    s=html.unescape(s)
    s="".join(c for c in s if c >= " " and c != "\x7f")
    return s[:1000]

def main():
    body=fetch(URL)
    print("StoneAge NetPower 2000-09 viewer metadata probe — R1")
    print("SOURCE|"+URL)
    print("SCOPE|url-and-viewer-metadata-only|no-magazine-image-bytes")
    print("HTML_BYTES|"+str(len(body.encode("utf-8"))))

    # Preserve script/image/anchor/form targets and interesting literal path tokens.
    attrs=set()
    for m in re.finditer(r'''(?is)\b(?:src|href|action|data-[\w-]+)\s*=\s*["']([^"']+)["']''',body):
        v=clean(m.group(1))
        if v:
            attrs.add(urllib.parse.urljoin(URL,v))

    literals=set()
    patterns=[
        r'''(?i)[^"'\s<>]{0,120}(?:magazine|netpower|2000_9|page|scan|jpg|jpeg|png|gif)[^"'\s<>]{0,180}''',
        r'''(?i)(?:https?:)?//[^"'\s<>]+''',
    ]
    for pat in patterns:
        for m in re.finditer(pat,body):
            v=clean(m.group(0))
            if v:
                literals.add(v)

    print("COUNT|attribute_urls|"+str(len(attrs)))
    for v in sorted(attrs):
        print("ATTR|"+v)
    print("COUNT|interesting_literals|"+str(len(literals)))
    for v in sorted(literals):
        print("LITERAL|"+v)

if __name__=="__main__":
    main()
