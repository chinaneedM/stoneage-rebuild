#!/usr/bin/env python3
"""Recover preservation metadata for the 2001-11-27 StoneAge full-map package.

Target is sourced from the surviving Sina page:
  aid=43172, col=map, filename=Estoneage2.0map_1127.exe, size=1911K.
The probe uses metadata/index surfaces only and never downloads the package body.
"""
from __future__ import annotations
import hashlib, html, json, re, urllib.parse, urllib.request, urllib.error

UA="stoneage-rebuild-archaeology/1.0"
SOURCE="https://games.sina.com.cn/downgames/map/11271899.shtml"
FILENAME="Estoneage2.0map_1127.exe"
STEM="Estoneage2.0map_1127"
AID="43172"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"

def clean(v,limit=5000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=40,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def parse_cdx(body):
    data=json.loads(body.decode("utf-8"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list): return ()
    hdr=data[0]
    return tuple(dict(zip(hdr,row)) for row in data[1:] if isinstance(row,list))

def source_hrefs(body):
    text=body.decode("gb18030","replace")
    hrefs=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    out=[]
    for href in hrefs:
        u=urllib.parse.urljoin(SOURCE,html.unescape(href))
        low=urllib.parse.unquote_plus(u).lower()
        if f"aid={AID}" in low or FILENAME.lower() in low:
            out.append(u)
    return tuple(dict.fromkeys(out))

def cdx_url(target,match="exact"):
    q=[
      ("url",target),("matchType",match),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from","2001"),("to","2005"),("limit","5000")
    ]
    return CDX+"?"+urllib.parse.urlencode(q)

def avail(target,date):
    u=AVAIL+"?"+urllib.parse.urlencode({"url":target,"timestamp":date})
    st,final,h,b=fetch(u,timeout=25)
    obj=json.loads(b.decode("utf-8"))
    c=(obj.get("archived_snapshots") or {}).get("closest") or {}
    return st,final,c if c.get("available") else None

def ia_url(q):
    p=[("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("fl[]","description"),("rows","100"),("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(q):
    p=[("q",q),("qfields","name"),("mode","deep"),("limit","500"),("outputAs","json"),("showItemName","showItemName")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def walk_rows(node):
    rows=[]
    def walk(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x):
                rows.append(x)
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(node)
    seen={}
    for r in rows:
        k=(str(r.get("itemid","")),str(r.get("fileid","")),str(r.get("filename",r.get("name",""))))
        seen[k]=r
    return tuple(seen.values())

def row_path(r):
    return str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")

def main():
    print("StoneAge 2001 full-map preservation probe — R1")
    print("SCOPE|Sina-source+Wayback+IA+DiscMaster|metadata-only|no-payload")
    print(f"TARGET|date=2001-11-27|aid={AID}|filename={FILENAME}|size_kib=1911|compatibility=1.X,2.0")
    errors=[]
    hrefs=()
    try:
        st,final,h,b=fetch(SOURCE,timeout=30)
        print(f"SOURCE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        hrefs=source_hrefs(b)
        print(f"COUNT|source_hrefs|{len(hrefs)}")
        for i,u in enumerate(hrefs,1):
            print(f"HREF|index={i}|url={clean(u)}")
            for k,v in urllib.parse.parse_qsl(urllib.parse.urlsplit(u).query,keep_blank_values=True):
                print(f"HREF_PARAM|index={i}|key={clean(k)}|value={clean(v)}")
    except Exception as e:
        errors.append(("source",type(e).__name__,str(e)))

    targets=list(hrefs)
    # Route-derived direct-file candidates only; kept separate from confirmed hrefs.
    for host in ("games1.sina.com.cn","games.sina.com.cn"):
        for path in (
          f"/downgames/map/{FILENAME}",
          f"/games/downgames/map/{FILENAME}",
          f"/downgames/{FILENAME}",
        ):
            targets.append("http://"+host+path)
    targets=tuple(dict.fromkeys(targets))
    print(f"COUNT|wayback_targets|{len(targets)}")

    seen_rows=[]
    for i,u in enumerate(targets,1):
        for match in ("exact","prefix"):
            try:
                st,final,h,b=fetch(cdx_url(u,match),timeout=45)
                rows=parse_cdx(b); seen_rows.extend(rows)
                print(f"CDX|index={i}|match={match}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|target={clean(u)}")
                for row in rows[:100]:
                    print(f"CDX_ROW|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|length={clean(row.get('length'))}|redirect={clean(row.get('redirect'))}")
            except Exception as e:
                errors.append((f"cdx:{i}:{match}",type(e).__name__,str(e)))

    # Host-wide wildcard filename query.
    for wild in (f"*.sina.com.cn/*{FILENAME}",f"*.sina.com.cn/*{STEM}*"):
        try:
            st,final,h,b=fetch(cdx_url(wild,"prefix"),timeout=50)
            rows=parse_cdx(b); seen_rows.extend(rows)
            print(f"CDX_WILDCARD|target={clean(wild)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for row in rows[:100]:
                print(f"CDX_WILDCARD_ROW|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|length={clean(row.get('length'))}|redirect={clean(row.get('redirect'))}")
        except Exception as e:
            errors.append((f"cdx-wild:{wild}",type(e).__name__,str(e)))

    for i,u in enumerate(hrefs,1):
        for date in ("20011127","20011201","20011231","20020101","20021108","20030403"):
            try:
                st,final,c=avail(u,date)
                print(f"AVAIL|index={i}|date={date}|status={st}|hit={int(c is not None)}|timestamp={clean(c.get('timestamp') if c else '')}|capture={clean(c.get('url') if c else '')}|http_status={clean(c.get('status') if c else '')}")
            except Exception as e:
                errors.append((f"avail:{i}:{date}",type(e).__name__,str(e)))

    ia_docs=0
    for label,q in (
      ("exact",f'"{FILENAME}"'),
      ("stem",f'"{STEM}"'),
      ("estoneage",'"Estoneage2.0map"'),
      ("stoneage-map",'stoneage AND "1127" AND map'),
    ):
        try:
            st,final,h,b=fetch(ia_url(q),timeout=40)
            obj=json.loads(b.decode("utf-8")); docs=((obj.get("response") or {}).get("docs") or [])
            ia_docs+=len(docs)
            print(f"IA|label={label}|status={st}|items={len(docs)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for d in docs[:100]:
                print(f"IA_HIT|label={label}|identifier={clean(d.get('identifier'))}|title={clean(d.get('title'))}|date={clean(d.get('date'))}|description={clean(d.get('description'))}")
        except Exception as e:
            errors.append((f"ia:{label}",type(e).__name__,str(e)))

    disc_rows=[]
    for q in (FILENAME,STEM,"Estoneage2.0map","estoneage","1127.exe","estone~1.exe"):
        try:
            st,final,h,b=fetch(discm_url(q),timeout=40)
            obj=json.loads(b.decode("utf-8")); rows=walk_rows(obj); disc_rows.extend(rows)
            print(f"DISCM|q={clean(q)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rows[:100]:
                path=row_path(r)
                low=path.lower()
                if ("estoneage" in low or "1127" in low or FILENAME.lower()==path.rsplit("/",1)[-1].lower()):
                    print(f"DISCM_HIT|q={clean(q)}|itemid={clean(r.get('itemid'))}|itemName={clean(r.get('itemName'))}|path={clean(path)}|size={clean(r.get('size'))}|ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}")
        except Exception as e:
            errors.append((f"discm:{q}",type(e).__name__,str(e)))

    uniq_cdx={(str(r.get("timestamp","")),str(r.get("original","")),str(r.get("digest",""))) for r in seen_rows}
    uniq_disc={(str(r.get("itemid","")),row_path(r)) for r in disc_rows}
    print(f"COUNT|cdx_unique_rows|{len(uniq_cdx)}")
    print(f"COUNT|ia_docs|{ia_docs}")
    print(f"COUNT|discm_unique_rows|{len(uniq_disc)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if uniq_cdx:
        print("RESOLUTION|WAYBACK_CANDIDATE_FOUND|inspect candidate response before payload recovery")
    elif ia_docs or uniq_disc:
        print("RESOLUTION|PRESERVATION_CANDIDATE_FOUND|verify exact filename/size identity before payload recovery")
    else:
        print("RESOLUTION|NO_PAYLOAD_CARRIER_YET|exact 2001 recovery token established; expand independent archive/mirror search")
    print("EVIDENCE_BOUNDARY|the surviving Sina page proves the 2001 package record and compatibility claim; archive/index hits must be byte-verified separately before being promoted to the package itself.")

if __name__=="__main__":
    main()
