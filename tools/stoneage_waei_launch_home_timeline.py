#!/usr/bin/env python3
"""Recover Waei StoneAge homepage/news chronology around launch and Jan-2001 trial.

Uses only source-derived first-party page paths already recovered from the
2000-12-07 and 2001-02-26 StoneAge site. Replays archived HTML and emits
download/trial/fileid semantics and references. No binary payload is fetched.
"""
from __future__ import annotations
import hashlib, html, json, re, time, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001207"; TO="20010228"
LAUNCH_END="20010112"
MAX=2*1024*1024
TARGETS=(
 ("home","http://www7.waei.net/wgs/stoneage/default.asp"),
 ("home80","http://www7.waei.net:80/wgs/stoneage/default.asp"),
 ("news","http://www7.waei.net/wgs/stoneage/newsback.asp"),
 ("news80","http://www7.waei.net:80/wgs/stoneage/newsback.asp"),
 ("base","http://www7.waei.net/wgs/stoneage/"),
 ("base80","http://www7.waei.net:80/wgs/stoneage/"),
 ("index","http://www7.waei.net/wgs/stoneage/index.asp"),
 ("index80","http://www7.waei.net:80/wgs/stoneage/index.asp"),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=MAX,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*;q=0.2","Accept-Encoding":"identity"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b,i+1
        except Exception as e:
            last=e
            if i+1<attempts: time.sleep(2)
    raise last

def cdx(url):
    q=[("url",url),("matchType","exact"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from",FROM),("to",TO),("limit","5000")]
    return CDX+"?"+urllib.parse.urlencode(q)

def rows(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def decode(b):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def plain(t):
    p=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",t)
    p=html.unescape(re.sub(r"(?s)<[^>]+>"," ",p))
    return re.sub(r"\s+"," ",p)

def title(t):
    m=re.search(r"(?is)<title[^>]*>(.*?)</title>",t)
    return clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(1))) if m else "",500)

def refs(t,base):
    out=[]
    for kind,pat in (
      ("href",r'(?is)\bhref\s*=\s*["\']([^"\']+)["\']'),
      ("src",r'(?is)\bsrc\s*=\s*["\']([^"\']+)["\']'),
    ):
        for m in re.finditer(pat,t):
            u=html.unescape(m.group(1)).strip()
            if not u or u.lower().startswith(("javascript:","mailto:","#")):continue
            out.append((kind,urllib.parse.urljoin(base,u)))
    return out

def target_ref(kind,u):
    low=urllib.parse.unquote_plus(u).lower()
    return any(k in low for k in (
       "download","downloan","down_loan","fileid=","downloading.php",
       ".exe",".zip",".rar",".cab","stoneage","trial","demo","test"
    ))

def semantics(p):
    low=p.lower()
    stone=[x for x in ("石器時代","石器时代","stoneage","stone age") if x.lower() in low]
    trial=[x for x in ("試玩","试玩","測試","测试","trial","demo") if x.lower() in low]
    down=[x for x in ("下載","下载","download","客戶端","客户端","安裝","安装") if x.lower() in low]
    sizes=list(dict.fromkeys(m.group(0) for m in re.finditer(r"(?<!\d)(?:27[0-9](?:\.\d+)?)\s*(?:m|mb|兆|k|kb)",p,re.I)))
    return stone,trial,down,sizes

def snippets(p):
    needles=("石器時代","石器时代","試玩","试玩","測試","测试","下載","下载","download","274","273","275","客戶端","客户端")
    low=p.lower();out=[]
    for n in needles:
        s=0; nl=n.lower()
        while True:
            i=low.find(nl,s)
            if i<0:break
            v=clean(p[max(0,i-280):min(len(p),i+620)],1600)
            if v not in out:out.append(v)
            s=i+max(1,len(n))
    return out[:32]

def main():
    print("StoneAge Waei launch homepage/news timeline — R1")
    print(f"SCOPE|first-party source-derived exact paths|{FROM}..{TO}|launch-window-through={LAUNCH_END}|HTML only|no payload")
    caps={}; errors=[]
    for label,url in TARGETS:
        try:
            st,final,h,b,attempt=fetch(cdx(url),timeout=55,max_bytes=4*1024*1024)
            rr=rows(b)
            print(f"CDX|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|attempt={attempt}|final={clean(final)}")
            for r in rr:
                key=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                caps[key]=(label,r)
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))
    print(f"COUNT|unique_captures|{len(caps)}")
    launch=0;replayed=0;semantic=0;target_refs={}
    for (ts,orig,digest),(label,r) in sorted(caps.items()):
        in_launch=FROM<=ts[:8]<=LAUNCH_END
        launch+=int(in_launch)
        if str(r.get("statuscode") or "") not in ("","200"):continue
        try:
            st,final,h,b,attempt=fetch(f"https://web.archive.org/web/{ts}id_/{orig}",timeout=45,max_bytes=MAX)
            enc,t=decode(b);p=plain(t);replayed+=1
            stone,trial,down,sizes=semantics(p)
            sem=bool(stone and (trial or down or sizes)); semantic+=int(sem)
            rr=[(k,u) for k,u in refs(t,orig) if target_ref(k,u)]
            print(f"PAGE|label={label}|timestamp={ts}|launch_window={int(in_launch)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={title(t)}|stone={clean(','.join(stone))}|trial={clean(','.join(trial))}|download={clean(','.join(down))}|size_tokens={clean(','.join(sizes))}|target_refs={len(rr)}|original={clean(orig)}")
            for k,u in rr:
                target_refs[(ts,k,u)]=label
                print(f"REF|label={label}|timestamp={ts}|kind={k}|url={clean(u)}")
            if sem or in_launch:
                for s in snippets(p):
                    print(f"SNIPPET|label={label}|timestamp={ts}|text={s}")
        except Exception as e:
            errors.append((f"replay:{label}:{ts}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={kind}|message={clean(msg)}")
    print(f"COUNT|launch_window_captures|{launch}")
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|semantic_pages|{semantic}")
    print(f"COUNT|target_refs|{len(target_refs)}")
    print(f"COUNT|errors|{len(errors)}")
    if semantic:
        print("RESOLUTION|STONEAGE_LAUNCH_DOWNLOAD_SEMANTICS_FOUND|bind exact referenced route/fileid and capture chronology next")
    elif launch:
        print("RESOLUTION|STONEAGE_LAUNCH_PAGES_RECOVERED_NO_DIRECT_DOWNLOAD_TEXT|inspect target refs/news assets and neighboring capture dates")
    elif errors:
        print("RESOLUTION|STONEAGE_LAUNCH_TIMELINE_PARTIAL|retry failed exact surfaces only")
    else:
        print("RESOLUTION|STONEAGE_LAUNCH_EXACT_PATHS_UNPRESERVED|retain 2000-12-07 badlist as earliest current site anchor")
    print("EVIDENCE_BOUNDARY|Archived HTML/routes identify distribution topology only; no client binary is fetched or authenticated.")

if __name__=="__main__":main()
