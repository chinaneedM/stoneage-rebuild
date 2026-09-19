#!/usr/bin/env python3
"""Extract public GameMeca magazine viewer asset/path metadata.

Stores no magazine image bytes or article text; only URL/attribute/path tokens
needed to locate historically relevant scan pages.
"""

import hashlib
import html
import re
import urllib.parse
import urllib.request

URL="https://www.gamemeca.com/magazine/index.php?mgz=netpower&ym=2000_9"
MOBILE="https://m.gamemeca.com/magazine.php?mgz=netpower&ym=2000_9"
JS="https://www.gamemeca.com/magazine/common.1.js"
UA="Mozilla/5.0 StoneAgeArchaeology/1.0"

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept-Language":"ko,en;q=0.8"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read().decode("utf-8","replace")

def page_meta(page):
    url=f"https://m.gamemeca.com/mgz_img.php?m=b&title=netpower&ym=2000_9&p={page}"
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"image/*"})
    with urllib.request.urlopen(req,timeout=30) as resp:
        data=resp.read()
        return {
            "page": page,
            "request": url,
            "final": resp.geturl(),
            "status": getattr(resp,"status",200),
            "type": resp.headers.get("Content-Type",""),
            "length": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }

def clean(s):
    s=html.unescape(s)
    s="".join(c for c in s if c >= " " and c != "\x7f")
    return s[:1000]

def main():
    body=fetch(URL)
    mobile=fetch(MOBILE)
    js=fetch(JS)
    print("StoneAge NetPower 2000-09 viewer metadata probe — R2")
    print("SOURCE|"+URL)
    print("SCOPE|url-and-viewer-metadata-only|no-magazine-image-bytes")
    print("HTML_BYTES|"+str(len(body.encode("utf-8"))))
    print("MOBILE_HTML_BYTES|"+str(len(mobile.encode("utf-8"))))
    print("VIEWER_JS_BYTES|"+str(len(js.encode("utf-8"))))

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

    def emit_context(label, text):
        keys=("2000_9","page_list","magazine_list","magazine_netpower","jpg","image","page","mgz","ym")
        seen=set()
        for line in text.splitlines():
            compact=line.strip()
            if not compact or not any(k.lower() in compact.lower() for k in keys):
                continue
            compact=clean(compact)
            if compact in seen:
                continue
            seen.add(compact)
            print(f"{label}|{compact}")

    emit_context("DESKTOP_CONTEXT",body)
    emit_context("MOBILE_CONTEXT",mobile)
    emit_context("JS_CONTEXT",js)

    for page in range(87,97):
        try:
            meta=page_meta(page)
            print(
                "PAGE_META|"
                + "|".join(
                    [
                        f"page={meta['page']}",
                        f"status={meta['status']}",
                        f"type={clean(meta['type'])}",
                        f"bytes={meta['length']}",
                        f"sha256={meta['sha256']}",
                        f"final={clean(meta['final'])}",
                    ]
                )
            )
        except Exception as exc:
            print(f"PAGE_ERROR|page={page}|{type(exc).__name__}|{clean(str(exc))}")

if __name__=="__main__":
    main()
