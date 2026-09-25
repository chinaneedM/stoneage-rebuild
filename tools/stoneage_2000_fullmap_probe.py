#!/usr/bin/env python3
"""Metadata-only recovery probe for Sina's 2000-12-20 StoneAge full-map ZIP."""
from __future__ import annotations
import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
SOURCE="https://games.sina.com.cn/downgames/map/1220492.shtml"
FILENAME="samap_1220.zip"
STEM="samap_1220"
AID="23223"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"

def clean(v,limit=5000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=40,max_bytes=3*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),r.read(max_bytes)

def source_hrefs(body):
    text=body.decode("gb18030","replace")
    out=[]
    for href in re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text):
        u=urllib.parse.urljoin(SOURCE,html.unescape(href))
        low=urllib.parse.unquote_plus(u).lower()
        if f"aid={AID}" in low or FILENAME.lower() in low: out.append(u)
    return tuple(dict.fromkeys(out))

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0];return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cdx_url(u,match="exact"):
    p=[("url",u),("matchType",match),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),("from","2000"),("to","2005"),("limit","5000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def ia_url(q):
    p=[("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("fl[]","description"),("rows","100"),("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(q):
    p=[("q",q),("qfields","name"),("mode","deep"),("limit","500"),("outputAs","json"),("showItemName","showItemName")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def strict_disc_candidate(path):
    leaf=str(path).replace("\\","/").rsplit("/",1)[-1].lower()
    return leaf==FILENAME.lower()

def rows_walk(d):
    out=[]
    def w(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x): out.append(x)
            for v in x.values(): w(v)
        elif isinstance(x,list):
            for v in x:w(v)
    w(d);return out

def main():
    print("StoneAge 2000-12-20 full-map preservation probe — R1")
    print("SCOPE|Sina-source+Wayback+IA+DiscMaster|metadata-only|no-payload")
    print(f"TARGET|date=2000-12-20|aid={AID}|filename={FILENAME}|size_kib=1410")
    errors=[];hrefs=();cdx_rows=[];ia_docs=0;ia_candidate_docs=0;disc_hits=[]
    try:
        st,final,b=fetch(SOURCE)
        print(f"SOURCE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        hrefs=source_hrefs(b)
        print(f"COUNT|source_hrefs|{len(hrefs)}")
        for i,u in enumerate(hrefs,1):
            print(f"HREF|index={i}|url={clean(u)}")
            for k,v in urllib.parse.parse_qsl(urllib.parse.urlsplit(u).query,keep_blank_values=True):
                print(f"HREF_PARAM|index={i}|key={clean(k)}|value={clean(v)}")
    except Exception as e: errors.append(("source",type(e).__name__,str(e)))

    targets=list(hrefs)
    for host in ("games1.sina.com.cn","games.sina.com.cn"):
        for path in (f"/downgames/map/{FILENAME}",f"/games/downgames/map/{FILENAME}",f"/downgames/{FILENAME}"):
            targets.append("http://"+host+path)
    targets=tuple(dict.fromkeys(targets))
    for i,u in enumerate(targets,1):
        for match in ("exact","prefix"):
            try:
                st,final,b=fetch(cdx_url(u,match),timeout=45)
                rr=parse_cdx(b);cdx_rows.extend(rr)
                print(f"CDX|index={i}|match={match}|status={st}|rows={len(rr)}|bytes={len(b)}|target={clean(u)}")
                for r in rr[:100]:
                    print(f"CDX_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
            except Exception as e: errors.append((f"cdx:{i}:{match}",type(e).__name__,str(e)))
    for i,u in enumerate(hrefs,1):
        for date in ("20001220","20010101","20010201","20011127","20020101"):
            try:
                q=AVAIL+"?"+urllib.parse.urlencode({"url":u,"timestamp":date})
                st,final,b=fetch(q,timeout=25);d=json.loads(b.decode("utf-8"));c=(d.get("archived_snapshots") or {}).get("closest") or {}
                print(f"AVAIL|index={i}|date={date}|status={st}|hit={int(bool(c.get('available')))}|timestamp={clean(c.get('timestamp'))}|capture={clean(c.get('url'))}|http_status={clean(c.get('status'))}")
            except Exception as e: errors.append((f"avail:{i}:{date}",type(e).__name__,str(e)))
    for label,q in (("exact",f'"{FILENAME}"'),("stem",f'"{STEM}"'),("samap",'"samap" AND stoneage')):
        try:
            st,final,b=fetch(ia_url(q),timeout=35);d=json.loads(b.decode("utf-8"));docs=((d.get("response") or {}).get("docs") or []);ia_docs+=len(docs);ia_candidate_docs+=len(docs) if label in ("exact","stem") else 0
            print(f"IA|label={label}|status={st}|items={len(docs)}|bytes={len(b)}")
            for x in docs[:100]:
                print(f"IA_HIT|identifier={clean(x.get('identifier'))}|title={clean(x.get('title'))}|date={clean(x.get('date'))}|description={clean(x.get('description'))}")
        except Exception as e: errors.append((f"ia:{label}",type(e).__name__,str(e)))
    for q in (FILENAME,STEM,"samap","samap_1220","samap~1.zip","1220.zip"):
        try:
            st,final,b=fetch(discm_url(q),timeout=40);d=json.loads(b.decode("utf-8"));rr=rows_walk(d)
            print(f"DISCM|q={clean(q)}|status={st}|rows={len(rr)}|bytes={len(b)}")
            for r in rr:
                path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
                leaf=path.replace("\\","/").rsplit("/",1)[-1].lower()
                low=path.lower()
                if strict_disc_candidate(path):
                    disc_hits.append(r)
                    print(f"DISCM_HIT|q={clean(q)}|itemid={clean(r.get('itemid'))}|itemName={clean(r.get('itemName'))}|path={clean(path)}|size={clean(r.get('size'))}|ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}")
        except Exception as e: errors.append((f"discm:{q}",type(e).__name__,str(e)))
    print(f"COUNT|cdx_rows|{len(cdx_rows)}")
    print(f"COUNT|ia_docs|{ia_docs}")
    print(f"COUNT|ia_candidate_docs|{ia_candidate_docs}")
    print(f"COUNT|discm_strict_candidate_rows|{len(disc_hits)}")
    for scope,kind,msg in errors: print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if cdx_rows: print("RESOLUTION|WAYBACK_CANDIDATE_FOUND|verify exact package response before payload recovery")
    elif ia_candidate_docs or disc_hits: print("RESOLUTION|PRESERVATION_CANDIDATE_FOUND|strict filename/stem carrier found; verify filename/size before payload recovery")
    else: print("RESOLUTION|NO_PAYLOAD_CARRIER_YET|exact 2000 recovery token established")
    print("EVIDENCE_BOUNDARY|the surviving Sina page proves the named 2000 distribution record; exact package bytes remain unverified until a carrier is recovered.")

if __name__=="__main__": main()
