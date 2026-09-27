#!/usr/bin/env python3
"""Recover Sina 2002 download-category -> file-server directory mappings.

The StoneAge 4.0 target is a Sina download.pl record with col=updatex and
aid=61620. Earlier body inspection proved that archived download.pl pages can
contain direct file-server URLs (for example, bizhi rows -> 202.106.185.224).
This probe queries the same Q4-2002 CGI archive, samples categories with
filename-bearing rows, replays only small HTML bodies, and extracts the direct
URL that contains each row's own filename. No linked payload is fetched.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
CGI="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl"
TARGET_COL="updatex"
TARGET_AID=61620
TARGET_FILE="shiqi4updatex_02_11_08.zip"
CATEGORIES=("updatex","demo","tools","littlegame","map","bizhi")
MAX_PER_CATEGORY=5
URLISH=re.compile(
    r'''(?is)(?:href|src|action)\s*=\s*["']([^"']+)["']'''
    r'''|(?:window\.open|location(?:\.href)?\s*=|window\.location\s*=)\s*\(?\s*["']([^"']+)["']'''
)
ABS=re.compile(r'''(?i)(?:https?|ftp)://[^\s"'<>]+''')


def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=35,max_bytes=4*1024*1024):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.4","Accept-Encoding":"identity"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b


def cdx_url():
    p=[
      ("url",CGI),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length"),
      ("from","20021001"),("to","20021231"),("limit","20000"),
      ("filter","statuscode:200"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,row)) for row in obj[1:] if isinstance(row,list))


def qparams(url):
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query,keep_blank_values=True))


def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode(body):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try:return body.decode(enc)
        except UnicodeDecodeError:pass
    return body.decode("latin1","replace")


def extract_refs(text,base):
    out=[]
    for m in URLISH.finditer(text):
        raw=(m.group(1) or m.group(2) or "").strip()
        if raw and not raw.startswith(("javascript:","mailto:","#")):
            out.append(urllib.parse.urljoin(base,html.unescape(raw)))
    for m in ABS.finditer(text):
        out.append(html.unescape(m.group(0)).rstrip("),.;"))
    return tuple(dict.fromkeys(out))


def filename_urls(text,base,filename):
    if not filename:return ()
    fn=filename.lower()
    return tuple(
        u for u in extract_refs(text,base)
        if fn in urllib.parse.unquote_plus(u).lower()
    )


def direct_shape(url):
    p=urllib.parse.urlsplit(url)
    leaf=p.path.rsplit("/",1)[-1]
    directory=p.path.rsplit("/",1)[0]+"/" if "/" in p.path else "/"
    return p.scheme,p.hostname or "",directory,leaf


def main():
    print("StoneAge Sina 2002 download-category routing probe — R1")
    print("SCOPE|Q4-2002 download.pl rows|category sampling|small archived HTML bodies|no-linked-payload")
    print(f"TARGET|col={TARGET_COL}|aid={TARGET_AID}|filename={TARGET_FILE}")
    errors=[]
    try:
        st,final,h,b=fetch(cdx_url(),timeout=60,max_bytes=8*1024*1024)
        rows=parse_cdx(b)
        print(f"CDX|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
    except Exception as e:
        rows=()
        errors.append(("cdx",type(e).__name__,str(e)))

    bycat={c:[] for c in CATEGORIES}
    target_rows=[]
    for row in rows:
        orig=str(row.get("original") or "")
        qp=qparams(orig)
        col=str(qp.get("col") or "").lower()
        fn=str(qp.get("filename") or "")
        aid=str(qp.get("aid") or "")
        if col==TARGET_COL:
            target_rows.append((aid,fn,row))
        if col in bycat and fn:
            bycat[col].append((aid,fn,row))

    for cat in CATEGORIES:
        vals=bycat.get(cat,[])
        print(f"CATEGORY|col={cat}|rows_with_filename={len(vals)}")
    print(f"COUNT|target_col_rows|{len(target_rows)}")
    exact=[x for x in target_rows if x[0]==str(TARGET_AID) or x[1].lower()==TARGET_FILE.lower()]
    print(f"COUNT|exact_target_rows|{len(exact)}")
    for aid,fn,row in exact[:20]:
        print(f"TARGET_ROW|aid={clean(aid)}|filename={clean(fn)}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}")

    mappings=[]
    seen_orig=set()
    for cat in CATEGORIES:
        vals=bycat.get(cat,[])
        # Prefer rows nearest the target aid when numeric, then earliest timestamp.
        def key(x):
            aid=x[0]
            dist=abs(int(aid)-TARGET_AID) if aid.isdigit() else 10**9
            return (dist,str(x[2].get("timestamp") or ""))
        vals=sorted(vals,key=key)
        used=0
        for aid,fn,row in vals:
            orig=str(row.get("original") or "")
            if orig in seen_orig:continue
            seen_orig.add(orig)
            ts=str(row.get("timestamp") or "")
            if not ts:continue
            if used>=MAX_PER_CATEGORY:break
            used+=1
            try:
                st,final,h,b=fetch(replay(ts,orig),timeout=22,max_bytes=96*1024)
                text=decode(b)
                refs=filename_urls(text,orig,fn)
                print(
                  f"REPLAY|col={cat}|aid={clean(aid)}|filename={clean(fn)}|timestamp={ts}|"
                  f"status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|filename_refs={len(refs)}"
                )
                for u in refs:
                    scheme,host,directory,leaf=direct_shape(u)
                    mappings.append((cat,scheme,host,directory,leaf,u))
                    print(
                      f"DIRECT_FILE|col={cat}|aid={clean(aid)}|filename={clean(fn)}|"
                      f"scheme={clean(scheme)}|host={clean(host)}|dir={clean(directory)}|url={clean(u)}"
                    )
            except Exception as e:
                errors.append((f"replay:{cat}:{aid}:{fn}",type(e).__name__,str(e)))

    agg={}
    for cat,scheme,host,directory,leaf,u in mappings:
        k=(cat,scheme,host,directory)
        agg[k]=agg.get(k,0)+1
    for (cat,scheme,host,directory),n in sorted(agg.items(),key=lambda kv:(kv[0][0],-kv[1],kv[0][2],kv[0][3])):
        print(f"MAPPING|col={cat}|count={n}|base={clean(f'{scheme}://{host}{directory}')}")
    target_mapping=[m for m in mappings if m[0]==TARGET_COL]
    print(f"COUNT|direct_file_mappings|{len(mappings)}")
    print(f"COUNT|target_col_mappings|{len(target_mapping)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:
        print("RESOLUTION|EXACT_TARGET_CGI_CAPTURE_FOUND|inspect exact archived body before any payload recovery")
    elif target_mapping:
        print("RESOLUTION|UPDATE_COL_DIRECTORY_TEMPLATE_FOUND|synthesize target basename only within repeated updatex base")
    elif target_rows:
        print("RESOLUTION|UPDATE_COL_ROWS_FOUND_NO_DIRECT_TEMPLATE|retain updatex CGI rows as new exact replay tokens")
    elif mappings:
        print("RESOLUTION|OTHER_CATEGORY_TEMPLATES_ONLY|do not infer updatex directory from unrelated categories")
    elif errors:
        print("RESOLUTION|CATEGORY_ROUTING_INCOMPLETE|retry failed bounded samples only")
    else:
        print("RESOLUTION|NO_CATEGORY_FILE_SERVER_MAPPING|close archived-body category route")
    print("EVIDENCE_BOUNDARY|Neighbor-category URL templates are routing evidence only; different col values must not be treated as sharing a directory without direct updatex evidence.")


if __name__=="__main__":
    main()
