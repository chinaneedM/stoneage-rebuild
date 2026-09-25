#!/usr/bin/env python3
"""Mine archived Sina download.pl rows for historical redirect/file-server topology.

This probe is metadata/small-response only. It enumerates archived download.pl
requests, isolates col=map rows, replays a bounded subset of small HTML/redirect
responses with redirects disabled, and records Location/body links. It never
downloads binary payloads.
"""
from __future__ import annotations
import collections, hashlib, json, re, urllib.error, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl"
TARGET_AID=23223
TARGET_FILENAME="samap_1220.zip"
WINDOWS=(("2000","20000101","20001231"),("2001","20010101","20011231"),("2002","20020101","20021231"),("2003","20030101","20031231"))

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fetch(url,timeout=50,max_bytes=2*1024*1024,no_redirect=False):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    opener=urllib.request.build_opener(NoRedirect) if no_redirect else None
    try:
        call=opener.open if opener is not None else urllib.request.urlopen
        with call(req,timeout=timeout) as r:
            return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)
    except urllib.error.HTTPError as e:
        return int(e.code),e.geturl(),dict(e.headers.items()),e.read(max_bytes)

def cdx_url(start,end):
    p=[
      ("url",PREFIX),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from",start),("to",end),("limit","10000")
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def params(url):
    try: return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query,keep_blank_values=True))
    except Exception: return {}

def map_row(row):
    p=params(str(row.get("original") or ""))
    if str(p.get("col") or "").lower()!="map": return None
    aid=str(p.get("aid") or "")
    return {
      "row":row,
      "aid":int(aid) if aid.isdigit() else None,
      "filename":str(p.get("filename") or ""),
      "size":str(p.get("size") or ""),
      "params":p,
    }

def location(headers):
    for k,v in headers.items():
        if str(k).lower()=="location": return str(v)
    return ""

def body_links(body,base):
    text=body.decode("gb18030","replace")
    vals=[]
    vals += re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    vals += re.findall(r'(?is)src\s*=\s*["\']([^"\']+)["\']',text)
    vals += re.findall(r'(?i)(?:https?|ftp)://[^\s"\'<>]+',text)
    out=[]
    for raw in vals:
        u=urllib.parse.urljoin(base,raw.replace("&amp;","&"))
        low=urllib.parse.unquote_plus(u).lower()
        if any(ext in low for ext in (".zip",".exe",".rar",".cab")) or "download" in low or "down." in low or "/down/" in low or low.startswith("ftp://"):
            out.append(u)
    return tuple(dict.fromkeys(out))

def directish(url):
    low=urllib.parse.unquote_plus(str(url)).lower()
    if not low: return False
    if any(host in low for host in ("login.games.sina.com.cn","macromedia.com","adobe.com")): return False
    return any(ext in low for ext in (".zip",".exe",".rar",".cab")) or low.startswith("ftp://")

def distance(item):
    aid=item.get("aid")
    return abs(aid-TARGET_AID) if isinstance(aid,int) else 10**12

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def main():
    print("StoneAge Sina download CGI topology census — R1")
    print("SCOPE|Wayback download.pl prefix census + bounded small-response replay|metadata/html-only|no-payload")
    print(f"TARGET|aid={TARGET_AID}|filename={TARGET_FILENAME}")
    errors=[];all_rows=[];maps=[]
    for label,start,end in WINDOWS:
        try:
            st,final,h,b=fetch(cdx_url(start,end),timeout=60,max_bytes=5*1024*1024)
            rows=parse_cdx(b);all_rows.extend(rows)
            yearmaps=[x for x in (map_row(r) for r in rows) if x]
            maps.extend(yearmaps)
            print(f"CDX_WINDOW|label={label}|status={st}|rows={len(rows)}|map_rows={len(yearmaps)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))
    print(f"COUNT|all_rows|{len(all_rows)}")
    col_counts=collections.Counter()
    for r in all_rows:
        p=params(str(r.get("original") or ""))
        col_counts[str(p.get("col") or "<none>").lower()]+=1
    for col,n in col_counts.most_common(30):
        print(f"COL_COUNT|col={clean(col)}|rows={n}")
    for i,r in enumerate(all_rows[:30],1):
        print(f"RAW_SAMPLE|index={i}|timestamp={clean(r.get('timestamp'))}|statuscode={clean(r.get('statuscode'))}|original={clean(r.get('original'))}")
    print(f"COUNT|map_rows|{len(maps)}")
    counts=collections.Counter(str(x["row"].get("statuscode") or "") for x in maps)
    for sc,n in sorted(counts.items()):
        print(f"STATUS_COUNT|statuscode={clean(sc)}|rows={n}")

    ordered=sorted(maps,key=lambda x:(distance(x),str(x["row"].get("timestamp") or ""),str(x["filename"])))
    for x in ordered[:40]:
        r=x["row"]
        print(f"NEAR_ROW|distance={distance(x)}|aid={clean(x['aid'])}|timestamp={clean(r.get('timestamp'))}|statuscode={clean(r.get('statuscode'))}|filename={clean(x['filename'])}|size={clean(x['size'])}|redirect={clean(r.get('redirect'))}|length={clean(r.get('length'))}")

    redirects=[x for x in maps if str(x["row"].get("statuscode") or "") in ("301","302","303","307","308")]
    candidates=[]
    sample=[]
    seen=set()
    for x in sorted(redirects,key=lambda z:(distance(z),str(z["row"].get("timestamp") or ""))):
        key=(str(x["row"].get("timestamp") or ""),str(x["row"].get("original") or ""))
        if key not in seen:
            seen.add(key);sample.append(x)
        if len(sample)>=30: break
    for x in ordered:
        r=x["row"]
        if str(r.get("statuscode") or "")=="200" and str(r.get("mimetype") or "").lower().startswith("text"):
            key=(str(r.get("timestamp") or ""),str(r.get("original") or ""))
            if key not in seen:
                seen.add(key);sample.append(x)
        if len(sample)>=45: break

    print(f"COUNT|replay_sample|{len(sample)}")
    for i,x in enumerate(sample,1):
        r=x["row"];ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        if not ts or not orig: continue
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=40,max_bytes=128*1024,no_redirect=True)
            loc=location(h);links=body_links(b,orig)
            print(f"REPLAY|index={i}|aid={clean(x['aid'])}|filename={clean(x['filename'])}|timestamp={clean(ts)}|status={st}|bytes={len(b)}|location={clean(loc)}|body_links={len(links)}")
            for u in ((loc,) if loc else ()) + links:
                kind="direct" if directish(u) else "gateway"
                print(f"TOPOLOGY_LINK|index={i}|kind={kind}|url={clean(u)}")
                if kind=="direct": candidates.append((x,u))
        except Exception as e:
            errors.append((f"replay:{i}",type(e).__name__,str(e)))

    uniq=[]
    seenurl=set()
    for x,u in candidates:
        if u not in seenurl:
            seenurl.add(u);uniq.append((x,u))
    print(f"COUNT|directish_unique|{len(uniq)}")
    for i,(x,u) in enumerate(uniq[:100],1):
        print(f"DIRECTISH|index={i}|aid={clean(x['aid'])}|filename={clean(x['filename'])}|url={clean(u)}")
    for s,k,m in errors[:200]:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if uniq:
        print("RESOLUTION|DIRECT_FILE_TOPOLOGY_FOUND|inspect host/path families and test target substitutions only as hypotheses")
    elif maps:
        print("RESOLUTION|CGI_CORPUS_BOUNDED_NO_DIRECT_FILE_URL|archived map CGI rows expose no direct binary topology in bounded replay sample")
    else:
        print("RESOLUTION|NO_MAP_CGI_CORPUS|no archived col=map rows recovered")
    print("EVIDENCE_BOUNDARY|recovered redirects/body links establish Sina CGI topology only; filename substitution never proves target payload identity.")

if __name__=="__main__":
    main()
