#!/usr/bin/env python3
"""Metadata-only preservation probe for Sina's 2001-11-02 StoneAge 2.0 client."""
from __future__ import annotations
import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
SOURCE="https://games.sina.com.cn/downgames/demo/1102970.shtml"
FILENAME="stoneage2.0setup.exe"
AID="41967"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"

def clean(v,limit=4000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=35,max_bytes=2*1024*1024):
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
    h=d[0]; return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cdx_url(u):
    p=[("url",u),("matchType","exact"),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),("from","2001"),("to","2005"),("limit","1000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def main():
    print("StoneAge 2001-11-02 2.0 client preservation probe — R1")
    print("SCOPE|Sina-source+exact-Wayback+IA+DiscMaster|metadata-only|no-payload")
    print(f"TARGET|date=2001-11-02|aid={AID}|filename={FILENAME}|size_kib=524377")
    errors=[]; hrefs=(); hits=0
    try:
        st,final,b=fetch(SOURCE)
        print(f"SOURCE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        hrefs=source_hrefs(b)
        for i,u in enumerate(hrefs,1):
            print(f"HREF|index={i}|url={clean(u)}")
            for k,v in urllib.parse.parse_qsl(urllib.parse.urlsplit(u).query,keep_blank_values=True):
                print(f"HREF_PARAM|index={i}|key={clean(k)}|value={clean(v)}")
    except Exception as e:
        errors.append(("source",type(e).__name__,str(e)))
    for i,u in enumerate(hrefs,1):
        try:
            st,final,b=fetch(cdx_url(u),timeout=45)
            rows=parse_cdx(b); hits+=len(rows)
            print(f"CDX|index={i}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rows[:100]:
                print(f"CDX_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
        except Exception as e:
            errors.append((f"cdx:{i}",type(e).__name__,str(e)))
        for date in ("20011102","20011127","20011231","20020101"):
            try:
                q=AVAIL+"?"+urllib.parse.urlencode({"url":u,"timestamp":date})
                st,final,b=fetch(q,timeout=25); d=json.loads(b.decode("utf-8")); c=(d.get("archived_snapshots") or {}).get("closest") or {}
                print(f"AVAIL|index={i}|date={date}|status={st}|hit={int(bool(c.get('available')))}|timestamp={clean(c.get('timestamp'))}|capture={clean(c.get('url'))}")
            except Exception as e:
                errors.append((f"avail:{i}:{date}",type(e).__name__,str(e)))
    ia_count=0
    for label,q in (("exact",f'"{FILENAME}"'),("stem",'"stoneage2.0setup"')):
        try:
            p=[("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("fl[]","description"),("rows","100"),("page","1"),("output","json")]
            st,final,b=fetch(IA+"?"+urllib.parse.urlencode(p),timeout=35)
            d=json.loads(b.decode("utf-8")); docs=((d.get("response") or {}).get("docs") or []); ia_count+=len(docs)
            print(f"IA|label={label}|status={st}|items={len(docs)}|bytes={len(b)}")
            for x in docs[:100]:
                print(f"IA_HIT|identifier={clean(x.get('identifier'))}|title={clean(x.get('title'))}|date={clean(x.get('date'))}|description={clean(x.get('description'))}")
        except Exception as e: errors.append((f"ia:{label}",type(e).__name__,str(e)))
    disc_count=0
    for q in (FILENAME,"stoneage2.0setup","stoneage2","stoneage~1.exe"):
        try:
            p=[("q",q),("qfields","name"),("mode","deep"),("limit","500"),("outputAs","json"),("showItemName","showItemName")]
            st,final,b=fetch(DISCM+"?"+urllib.parse.urlencode(p),timeout=35)
            d=json.loads(b.decode("utf-8"))
            rows=[]
            def walk(x):
                if isinstance(x,dict):
                    if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x): rows.append(x)
                    for v in x.values(): walk(v)
                elif isinstance(x,list):
                    for v in x: walk(v)
            walk(d); disc_count+=len(rows)
            print(f"DISCM|q={clean(q)}|status={st}|rows={len(rows)}|bytes={len(b)}")
            for r in rows[:100]:
                path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
                if "stoneage" in path.lower():
                    print(f"DISCM_HIT|itemid={clean(r.get('itemid'))}|itemName={clean(r.get('itemName'))}|path={clean(path)}|size={clean(r.get('size'))}|ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}")
        except Exception as e: errors.append((f"discm:{q}",type(e).__name__,str(e)))
    print(f"COUNT|source_hrefs|{len(hrefs)}")
    print(f"COUNT|cdx_rows|{hits}")
    print(f"COUNT|ia_docs|{ia_count}")
    print(f"COUNT|discm_rows|{disc_count}")
    for scope,kind,msg in errors: print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if hits or ia_count: print("RESOLUTION|CLIENT_CANDIDATE_FOUND|verify exact payload identity before recovery")
    else: print("RESOLUTION|NO_CLIENT_PAYLOAD_CARRIER_YET|exact 2001 client token established")
    print("EVIDENCE_BOUNDARY|Sina proves a 2001 download record and label; any preserved candidate must be byte-verified before clean-client classification.")

if __name__=="__main__": main()
