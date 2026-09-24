#!/usr/bin/env python3
"""Search public old-disc torrent metadata for the StoneAge 2.5 cross-promo carrier.

This downloads torrent METADATA only (allseeds.zip), never disc/game payload bytes.
"""
from __future__ import annotations
import hashlib, io, urllib.request, zipfile

URL="https://www.nuduseng.com/laoguangpan/allseeds.zip"
UA="stoneage-rebuild-archaeology/1.0"
MAX_ZIP=100_000_000
MAX_TORRENT=25_000_000
TOKENS=(
    "2001C226",
    "哇靠轰炸鸡",
    "2001 NEW GAME 093",
    "NEW GAME 093",
    "藏经阁280",
)
CONTEXTUAL=(("总第280期","NEW GAME"),("总第280期","藏经阁"),("总第280期","2001C226"))
WEAK=("NEW GAME","藏经阁")

def clean(v,n=2200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:n]

class BencodeError(ValueError): pass

def bdecode(data:bytes, i:int=0):
    if i>=len(data): raise BencodeError("eof")
    c=data[i:i+1]
    if c==b"i":
        j=data.find(b"e",i+1)
        if j<0: raise BencodeError("bad-int")
        return int(data[i+1:j]),j+1
    if c==b"l":
        out=[]; i+=1
        while data[i:i+1]!=b"e":
            v,i=bdecode(data,i); out.append(v)
        return out,i+1
    if c==b"d":
        out={}; i+=1
        while data[i:i+1]!=b"e":
            k,i=bdecode(data,i)
            if not isinstance(k,bytes): raise BencodeError("dict-key")
            v,i=bdecode(data,i); out[k]=v
        return out,i+1
    if c.isdigit():
        j=data.find(b":",i)
        if j<0: raise BencodeError("bad-str")
        n=int(data[i:j]); j+=1
        e=j+n
        if e>len(data): raise BencodeError("short-str")
        return data[j:e],e
    raise BencodeError(f"bad-token-{c!r}")

def root_info_span(data:bytes):
    if not data.startswith(b"d"): raise BencodeError("root-not-dict")
    i=1
    while data[i:i+1]!=b"e":
        k,i=bdecode(data,i)
        start=i
        _,i=bdecode(data,i)
        if k==b"info": return start,i
    raise BencodeError("no-info")

def text(b):
    if isinstance(b,str): return b
    if not isinstance(b,(bytes,bytearray)): return str(b)
    for enc in ("utf-8","gb18030","big5","latin1"):
        try:
            s=bytes(b).decode(enc)
            if s: return s
        except Exception:
            pass
    return bytes(b).decode("utf-8","replace")

def torrent_paths(meta):
    info=meta.get(b"info",{}) if isinstance(meta,dict) else {}
    out=[]
    name=info.get(b"name.utf-8",info.get(b"name",b"")) if isinstance(info,dict) else b""
    if name: out.append(text(name))
    files=info.get(b"files",[]) if isinstance(info,dict) else []
    for row in files:
        if not isinstance(row,dict): continue
        p=row.get(b"path.utf-8",row.get(b"path",[]))
        if isinstance(p,list): out.append("/".join(text(x) for x in p))
    return tuple(out)

def interesting(paths, raw):
    joined="\n".join(paths)
    low=joined.lower()
    strong=[t for t in TOKENS if t.lower() in low]
    # “总第280期” is generic (e.g. magazines); require a catalog-specific co-token.
    for a,b in CONTEXTUAL:
        if a.lower() in low and b.lower() in low:
            strong.append(a+"+"+b)
    weak=[]
    if not strong:
        for t in WEAK:
            if t.lower() in low: weak.append(t)
    return tuple(dict.fromkeys(strong)),tuple(dict.fromkeys(weak))

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept":"application/zip,*/*"})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(MAX_ZIP+1)
        if len(b)>MAX_ZIP: raise ValueError("allseeds-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def main():
    print("StoneAge 2.5 old-disc torrent metadata probe — R2")
    print("SCOPE|public-allseeds.zip|torrent-metadata-only|no-disc-payload")
    st,final,h,b=fetch()
    print(f"ZIP|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|content_type={clean(h.get('Content-Type'))}|last_modified={clean(h.get('Last-Modified'))}|final={clean(final)}")
    strong_hits=0; weak_hits=0; errors=0; torrents=0
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist()
        print(f"COUNT|zip_entries|{len(names)}")
        for zn in names:
            if not zn.lower().endswith(".torrent"): continue
            torrents+=1
            try:
                zi=z.getinfo(zn)
                if zi.file_size>MAX_TORRENT:
                    print(f"SKIP|entry={clean(zn)}|reason=torrent-too-large|bytes={zi.file_size}")
                    continue
                raw=z.read(zn)
                meta,end=bdecode(raw,0)
                paths=torrent_paths(meta)
                strong,weak=interesting(paths,raw)
                if not strong and not weak: continue
                try:
                    s,e=root_info_span(raw)
                    infohash=hashlib.sha1(raw[s:e]).hexdigest()
                except Exception:
                    infohash=""
                kind="STRONG" if strong else "WEAK"
                if strong: strong_hits+=1
                else: weak_hits+=1
                print(f"TORRENT_{kind}|entry={clean(zn)}|bytes={len(raw)}|sha256={hashlib.sha256(raw).hexdigest()}|infohash={infohash}|strong={clean(','.join(strong))}|weak={clean(','.join(weak))}|paths={len(paths)}")
                for p in relevant_paths(paths,strong,weak)[:100]:
                    print(f"PATH|entry={clean(zn)}|value={clean(p,3000)}")
            except Exception as e:
                errors+=1
                print(f"ERROR|entry={clean(zn)}|kind={type(e).__name__}|message={clean(e)}")
    print(f"COUNT|torrent_entries|{torrents}")
    print(f"COUNT|strong_hits|{strong_hits}")
    print(f"COUNT|weak_hits|{weak_hits}")
    print(f"COUNT|errors|{errors}")
    if strong_hits:
        print("RESOLUTION|EXACT_TARGET_TORRENT_METADATA_FOUND|inspect exact image/path identity before any payload recovery")
    elif weak_hits:
        print("RESOLUTION|WEAK_CATALOG_NEIGHBORHOOD_ONLY|generic issue/catalog tokens only; do not promote as target media")
    else:
        print("RESOLUTION|NO_TARGET_TORRENT_METADATA|public allseeds metadata has no tested target tokens")
    print("EVIDENCE_BOUNDARY|torrent metadata proves a preserved file-tree/index reference only; it does not prove StoneAge carriage or Waei provenance until exact media contents are verified.")

if __name__=="__main__":
    main()
