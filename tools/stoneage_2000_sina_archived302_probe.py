#!/usr/bin/env python3
"""Recover raw Wayback 302 Location headers from late-2000 Sina map CGI controls.

The 2000-12-28 south-island control (aid=23681) has a 2005 Wayback CDX row with
HTTP 302 but an empty CDX redirect field. This probe fetches only the small
archived CGI response with redirects disabled, records Location, and tests any
filename-substituted target URL in Wayback metadata. It never downloads map ZIPs.
"""
from __future__ import annotations
import hashlib,json,urllib.error,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
TARGET_FILENAME="samap_1220.zip"
CONTROLS=(
 ("north","http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=23680&title=%CA%AF%C6%F7%CA%B1%B4%FA%A1%AA%B1%B1%B5%BA%CF%EA%CF%B8%B5%D8%CD%BC%D6%B8%C4%CF&author=%D3%CE%C3%F1%B2%BF%C2%E4&filename=northisland_1228.zip&size=134"),
 ("south","http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=23681&title=%CA%AF%C6%F7%CA%B1%B4%FA%A1%AA%C4%CF%B5%BA%CF%EA%CF%B8%B5%D8%CD%BC%D6%B8%C4%CF&author=%D3%CE%C3%F1%B2%BF%C2%E4&filename=southisland_1228.zip&size=202"),
)

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fetch(url,timeout=40,max_bytes=512*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)
    except urllib.error.HTTPError as e:
        b=e.read(max_bytes)
        return int(e.code),e.geturl(),dict(e.headers.items()),b

def fetch_no_redirect(url,timeout=40,max_bytes=128*1024):
    op=urllib.request.build_opener(NoRedirect)
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    try:
        with op.open(req,timeout=timeout) as r:
            return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)
    except urllib.error.HTTPError as e:
        return int(e.code),e.geturl(),dict(e.headers.items()),e.read(max_bytes)

def cdx_url(u):
    return CDX+"?"+urllib.parse.urlencode({
      "url":u,"matchType":"exact","output":"json",
      "fl":"timestamp,original,statuscode,mimetype,digest,length,redirect",
      "from":"2000","to":"2008","limit":"500"
    })

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def replay_url(ts,orig,mode="id_"):
    return f"https://web.archive.org/web/{ts}{mode}/{orig}"

def location(headers):
    for k,v in headers.items():
        if str(k).lower()=="location":return str(v)
    return ""

def substitute_filename(url,source_filename,target_filename=TARGET_FILENAME):
    if not url:return ""
    low=url.lower();src=source_filename.lower()
    i=low.find(src)
    if i<0:return ""
    return url[:i]+target_filename+url[i+len(source_filename):]

def main():
    print("StoneAge 2000 Sina archived-302 topology probe — R1")
    print("SCOPE|exact control CGI CDX + no-follow Wayback replay headers + target filename substitution|small-response-only|no-payload")
    errors=[];locations=[];synth=[]
    for label,orig in CONTROLS:
        p=dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(orig).query,keep_blank_values=True))
        fn=str(p.get("filename") or "")
        try:
            st,final,h,b=fetch(cdx_url(orig),timeout=50)
            rows=parse_cdx(b)
            print(f"CDX|label={label}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        except Exception as e:
            rows=();errors.append((f"cdx:{label}",type(e).__name__,str(e)))
        for r in rows:
            ts=str(r.get("timestamp") or "")
            sc=str(r.get("statuscode") or "")
            print(f"ROW|label={label}|timestamp={clean(ts)}|statuscode={clean(sc)}|redirect={clean(r.get('redirect'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
            if not ts or sc not in ("301","302","303","307","308"):continue
            for mode in ("id_","if_"):
                u=replay_url(ts,orig,mode)
                try:
                    rst,rfinal,rh,rb=fetch_no_redirect(u,timeout=40,max_bytes=128*1024)
                    loc=location(rh)
                    print(f"REPLAY|label={label}|timestamp={ts}|mode={mode}|status={rst}|bytes={len(rb)}|sha256={hashlib.sha256(rb).hexdigest()}|location={clean(loc)}|final={clean(rfinal)}")
                    if loc:
                        locations.append((label,fn,loc))
                        su=substitute_filename(loc,fn)
                        if su:synth.append(su)
                except Exception as e:errors.append((f"replay:{label}:{ts}:{mode}",type(e).__name__,str(e)))
    synth=tuple(dict.fromkeys(synth))
    print(f"COUNT|locations|{len(locations)}")
    print(f"COUNT|synthesized_target_urls|{len(synth)}")
    for i,u in enumerate(synth,1):
        print(f"SYNTH|index={i}|url={clean(u)}")
        try:
            st,final,h,b=fetch(cdx_url(u),timeout=50)
            rr=parse_cdx(b)
            print(f"SYNTH_CDX|index={i}|status={st}|rows={len(rr)}|bytes={len(b)}")
            for r in rr:
                print(f"TARGET_ROW|index={i}|timestamp={clean(r.get('timestamp'))}|statuscode={clean(r.get('statuscode'))}|original={clean(r.get('original'))}|redirect={clean(r.get('redirect'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
        except Exception as e:errors.append((f"synth:{i}",type(e).__name__,str(e)))
    for s,k,m in errors[:200]:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if synth:print("RESOLUTION|ARCHIVED_302_LOCATION_RECOVERED|evaluate synthesized target CDX rows; location establishes control topology only")
    elif locations:print("RESOLUTION|ARCHIVED_302_LOCATION_NO_FILENAME_TEMPLATE|inspect recovered locations manually")
    else:print("RESOLUTION|NO_ARCHIVED_302_LOCATION|CDX control capture exists but replay headers expose no usable Location on tested modes")
    print("EVIDENCE_BOUNDARY|a recovered control Location proves only historical Sina download topology; substituted target URLs remain hypotheses until independently archived.")
if __name__=="__main__":main()
