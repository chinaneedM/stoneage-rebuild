#!/usr/bin/env python3
"""Probe Arquivo.pt for mirrors/reposts of the exact StoneAge 4.0 map patch.

Independent of Wayback. Uses full-text search, URL version-history search and
CDX metadata only. No candidate payload is downloaded.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TEXT="https://arquivo.pt/textsearch"
CDX="https://arquivo.pt/wayback/cdx"
SOURCE="http://games.sina.com.cn/downgames/updatex/11084599.shtml"
CGI="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=updatex&aid=61620&title=%A1%B6%CA%AF%C6%F7%CA%B1%B4%FA4.0%A1%B7%D7%EE%D0%C2%B5%D8%CD%BC%B2%B9%B6%A1&author=%D3%CE%C3%F1%B2%BF%C2%E4%CD%F8xinhaonanhai&filename=shiqi4updatex_02_11_08.zip&size=3440"
QUERIES=(
  "shiqi4updatex_02_11_08.zip",
  "shiqi4updatex",
  '"石器时代4.0" "地图补丁"',
  '"xinhaonanhai" "石器时代"',
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(8*1024*1024)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def parse_json(b):
    try:return json.loads(b.decode("utf-8"))
    except Exception:return None

def items(obj):
    if isinstance(obj,dict):
        for key in ("response_items","items","results","documents","captures"):
            v=obj.get(key)
            if isinstance(v,list):return v
    if isinstance(obj,list):return obj
    return []

def field(row,*names):
    if not isinstance(row,dict):return ""
    low={str(k).lower():v for k,v in row.items()}
    for n in names:
        if n.lower() in low:return low[n.lower()]
    return ""

def emit_items(label,obj):
    rr=items(obj)
    print(f"RESULT_COUNT|label={clean(label)}|count={len(rr)}")
    for i,row in enumerate(rr[:500],1):
        print(
          f"RESULT|label={clean(label)}|index={i}|"
          f"url={clean(field(row,'originalURL','url','original','uri'))}|"
          f"title={clean(field(row,'title'))}|"
          f"timestamp={clean(field(row,'tstamp','timestamp','date'))}|"
          f"status={clean(field(row,'statusCode','status','statuscode'))}|"
          f"mime={clean(field(row,'mimeType','mime','mimetype'))}|"
          f"digest={clean(field(row,'digest'))}|"
          f"length={clean(field(row,'contentLength','length'))}|"
          f"archive={clean(field(row,'linkToArchive','archiveURL','link'))}|"
          f"original_file={clean(field(row,'linkToOriginalFile'))}"
        )
    return len(rr)

def text_url(q):
    return TEXT+"?"+urllib.parse.urlencode({
      "q":q,"maxItems":"500","from":"20020101000000","to":"20151231235959"
    })

def version_url(u):
    return TEXT+"?"+urllib.parse.urlencode({"versionHistory":u,"maxItems":"500"})

def cdx_url(u):
    return CDX+"?"+urllib.parse.urlencode({"url":u,"output":"json","limit":"5000"})

def main():
    print("StoneAge 4.0 Arquivo.pt independent archive probe — R1")
    print("SCOPE|full-text+versionHistory+CDX|exact-filename+source+full-CGI|metadata-only|no-payload")
    errors=[];hits=0
    for q in QUERIES:
        try:
            u=text_url(q);st,final,h,b=fetch(u);obj=parse_json(b)
            print(f"TEXTSEARCH|q={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|json={int(obj is not None)}|final={clean(final)}")
            if obj is not None:hits+=emit_items("text:"+q,obj)
            else:print(f"BODY|label={clean('text:'+q)}|value={clean(b[:3000].decode('utf-8','replace'))}")
        except Exception as exc:errors.append(("text:"+q,type(exc).__name__,str(exc)))
    for label,u0 in (("source",SOURCE),("cgi",CGI)):
        try:
            u=version_url(u0);st,final,h,b=fetch(u);obj=parse_json(b)
            print(f"VERSION|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|json={int(obj is not None)}|final={clean(final)}")
            if obj is not None:hits+=emit_items("version:"+label,obj)
            else:print(f"BODY|label=version:{label}|value={clean(b[:3000].decode('utf-8','replace'))}")
        except Exception as exc:errors.append(("version:"+label,type(exc).__name__,str(exc)))
        try:
            u=cdx_url(u0);st,final,h,b=fetch(u);obj=parse_json(b)
            print(f"CDX|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|json={int(obj is not None)}|final={clean(final)}")
            if obj is not None:hits+=emit_items("cdx:"+label,obj)
            else:print(f"BODY|label=cdx:{label}|value={clean(b[:3000].decode('utf-8','replace'))}")
        except Exception as exc:errors.append(("cdx:"+label,type(exc).__name__,str(exc)))
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|reported_rows|{hits}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|"+("ARQUIVO_ROWS_FOUND|inspect URLs for independent mirror/repost evidence" if hits else "NO_ARQUIVO_ROW|independent archive exposed no indexed row on tested surfaces"))
    print("EVIDENCE_BOUNDARY|Arquivo.pt search/version/CDX rows are archive discovery metadata; no returned original-file payload is fetched by this probe.")
if __name__=="__main__":main()
