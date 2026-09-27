#!/usr/bin/env python3
"""Probe Waei's pre-www7 download system on www9.waei.net around the StoneAge trial.

Metadata/HTML only. Candidate game binaries are never fetched.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"; TO="20010112"
TARGETS=(
 ("download-prefix","http://www9.waei.net/download.php","prefix"),
 ("www9-prefix","http://www9.waei.net/","prefix"),
)
BINARY_EXTS=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z",".bin",".iso",".cue")
STONE=("stoneage","stone age","石器時代","石器时代","石器")
TRIAL=("trial","demo","test","試玩","试玩","測試","测试")
SIZE=("274","273","275")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url(url,match):
    params=[
      ("url",url),("matchType",match),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from",FROM),("to",TO),("filter","statuscode:200"),("limit","15000")
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))

def low(v): return urllib.parse.unquote_plus(str(v or "")).lower()
def is_binary(url): return urllib.parse.urlsplit(low(url)).path.endswith(BINARY_EXTS)
def replay(ts,orig): return f"https://web.archive.org/web/{ts}id_/{orig}"

def decode(body):
    for enc in ("big5","cp950","gb18030","utf-8","latin1"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",body.decode("latin1","replace")

def plain(text):
    p=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",text)
    p=re.sub(r"(?is)<[^>]+>"," ",p)
    return re.sub(r"\s+"," ",html.unescape(p))

def links(text,base):
    out=[]
    for m in re.finditer(r'(?is)(?:href|src)\s*=\s*["\']([^"\']+)["\']',text):
        raw=html.unescape(m.group(1)).strip()
        if not raw or raw.lower().startswith(("javascript:","mailto:","#")):continue
        out.append(urllib.parse.urljoin(base,raw))
    return tuple(dict.fromkeys(out))

def score_row(r):
    u=low(r.get("original"))
    s=0
    if "download.php" in u:s+=15
    if any(t in u for t in STONE):s+=30
    if any(t in u for t in TRIAL):s+=20
    if is_binary(u):s+=25
    if str(r.get("timestamp") or "").startswith(("200012","200101")):s+=5
    return s

def semantic(text):
    p=plain(text);l=p.lower()
    stone=[t for t in STONE if t.lower() in l]
    trial=[t for t in TRIAL if t.lower() in l]
    size=[t for t in SIZE if re.search(rf"(?<!\d){t}(?:\s*(?:m|mb|兆))?(?!\d)",l)]
    return p,stone,trial,size

def main():
    print("StoneAge Waei www9 pre-release download-system probe — R1")
    print(f"SCOPE|Wayback CDX+bounded HTML|window={FROM}..{TO}|www9 old download system|no binary payload")
    allrows={};errors=[]
    for label,url,match in TARGETS:
        try:
            st,final,h,b=fetch(cdx_url(url,match),timeout=60)
            rr=parse(b)
            print(f"CDX|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                key=(str(r.get("original") or ""),str(r.get("timestamp") or ""),str(r.get("digest") or ""))
                allrows[key]=r
        except Exception as exc:
            errors.append((f"cdx:{label}",type(exc).__name__,str(exc)))

    rows=sorted(allrows.values(),key=lambda r:(str(r.get("timestamp") or ""),str(r.get("original") or "")))
    binaries=[r for r in rows if is_binary(str(r.get("original") or ""))]
    print(f"COUNT|unique_rows|{len(rows)}")
    print(f"COUNT|binary_rows|{len(binaries)}")
    for r in binaries[:300]:
        print(f"BINARY_ROW|timestamp={clean(r.get('timestamp'))}|length={clean(r.get('length'))}|mime={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|original={clean(r.get('original'))}")

    # Replay one best/newest capture per URL, capped.
    byurl={}
    for r in rows:
        orig=str(r.get("original") or "")
        mt=str(r.get("mimetype") or "").lower()
        path=urllib.parse.urlsplit(orig).path.lower()
        if "html" not in mt and not path.endswith((".php",".asp",".htm",".html","/")):continue
        old=byurl.get(orig)
        if old is None or score_row(r)>score_row(old) or (score_row(r)==score_row(old) and str(r.get("timestamp"))>str(old.get("timestamp"))):
            byurl[orig]=r
    selected=sorted(byurl.values(),key=lambda r:(score_row(r),str(r.get("timestamp") or "")),reverse=True)[:30]
    print(f"COUNT|html_urls|{len(byurl)}")
    print(f"COUNT|selected_pages|{len(selected)}")
    semantic_pages=0;target_links={}
    for i,r in enumerate(selected,1):
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay(ts,orig),timeout=30,max_bytes=1024*1024)
            enc,text=decode(b);vis,stone,trial,size=semantic(text)
            ls=links(text,orig)
            hits=[]
            for u in ls:
                lu=low(u)
                if is_binary(u) or any(t in lu for t in STONE+TRIAL) or "download" in lu:
                    hits.append(u);target_links[u]=orig
            interesting=bool(stone or trial or size or hits or "download.php" in low(orig))
            if interesting:
                semantic_pages+=1
                title=""
                m=re.search(r"(?is)<title[^>]*>(.*?)</title>",text)
                if m:title=plain(m.group(1))
                print(f"PAGE|index={i}|timestamp={ts}|status={st}|bytes={len(b)}|encoding={enc}|stone={clean(','.join(stone),300)}|trial={clean(','.join(trial),300)}|size_tokens={clean(','.join(size),100)}|links={len(ls)}|target_links={len(hits)}|title={clean(title,1000)}|original={clean(orig)}")
                # Compact snippets only around source-derived terms.
                lvis=vis.lower()
                positions=[]
                for term in ("stoneage","stone age","石器時代","石器时代","試玩","试玩","測試","测试","274"):
                    start=0
                    while True:
                        p=lvis.find(term.lower(),start)
                        if p<0:break
                        positions.append(p);start=p+len(term)
                for p in sorted(set(positions))[:20]:
                    print(f"SNIPPET|page={i}|text={clean(vis[max(0,p-180):p+320],700)}")
            for u in hits[:100]:
                print(f"LINK|page={i}|binary={int(is_binary(u))}|href={clean(u)}")
        except Exception as exc:
            errors.append((f"page:{i}:{orig}",type(exc).__name__,str(exc)))
    print(f"COUNT|semantic_pages|{semantic_pages}")
    print(f"COUNT|unique_target_links|{len(target_links)}")
    print(f"COUNT|binary_target_links|{sum(is_binary(u) for u in target_links)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if binaries or any(is_binary(u) for u in target_links):
        print("RESOLUTION|WWW9_BINARY_ROUTE_FOUND|classify filenames and candidate size next")
    elif semantic_pages:
        print("RESOLUTION|WWW9_HTML_ROUTE_FOUND|follow exact category/query topology next")
    elif errors:
        print("RESOLUTION|PARTIAL_WWW9_PROBE|retry failed surfaces only")
    else:
        print("RESOLUTION|WWW9_ROUTE_BOUNDED|no source-specific trial token exposed in current archive")
    print("EVIDENCE_BOUNDARY|Archived page/link evidence proves distribution topology only; no candidate client binary is downloaded or authenticated.")

if __name__=="__main__":main()
