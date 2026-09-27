#!/usr/bin/env python3
"""Deep lineage probe for archived Waei sa_40.exe and sa_42.exe.

Focuses on exact runtime/updater/login strings and embedded resource-path
evolution. Historical executable bytes are fetched transiently and discarded.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import re
import struct
import subprocess
import tempfile
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGETS=(
 ("sa40","20011031155747","http://stoneage.waei.net:80/saupdate/sa_40.exe"),
 ("sa42","20011206183120","http://stoneage.waei.net:80/saupdate/sa_42.exe"),
)
MAX=8*1024*1024
NEEDLES=(
 "CheckForUpdate","updated","StoneAge.exe","stoneage.exe","sa.exe","sa_3.exe",
 "ClientLogin","CharLogin","PPASSWORD","yStoneAge.exe","wgs@mail.hwaei.com.tw",
 "stoneage.waei.net","/saupdate/newest.txt","/saupdate/%s","SaUpdate","SaUpdate.EXE",
 "ttttttttt","20041215","HASH___________@@@@@@@@",
 "FileVersion","ProductVersion","ProductName","FileDescription","OriginalFilename",
 "InternalName","CompanyName","VS_VERSION_INFO",
)
RESOURCE_KEYS=("FileVersion","ProductVersion","ProductName","FileDescription","OriginalFilename","InternalName","CompanyName")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(ts,orig):
    url=f"https://web.archive.org/web/{ts}id_/{orig}"
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/octet-stream,*/*;q=0.1","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(MAX+1)
        if len(b)>MAX: raise ValueError("response-too-large")
        return b

def ascii_strings(data,minlen=4):
    return [m.group().decode("ascii","replace") for m in re.finditer(rb"[\x20-\x7e]{%d,}"%minlen,data)]

def utf16_strings(data,minlen=3):
    out=[]
    pat=rb"(?:[\x20-\x7e]\x00){%d,}"%minlen
    for m in re.finditer(pat,data):
        out.append((m.start(),m.group().decode("utf-16le","replace")))
    return out

def pe_timestamp(data):
    if len(data)<0x40 or data[:2]!=b"MZ": return None
    off=struct.unpack_from("<I",data,0x3c)[0]
    if off+12>len(data) or data[off:off+4]!=b"PE\0\0": return None
    return struct.unpack_from("<I",data,off+8)[0]

def imports(data):
    with tempfile.NamedTemporaryFile(suffix=".exe") as f:
        f.write(data); f.flush()
        p=subprocess.run(["objdump","-p",f.name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="replace",timeout=30)
    dll=""; rows=[]; inside=False
    for raw in p.stdout.splitlines():
        line=raw.strip()
        if "The Import Tables" in line:
            inside=True; continue
        if not inside: continue
        if line.startswith("The Export Tables") or line.startswith("PE File Base Relocations"): break
        if line.startswith("DLL Name:"):
            dll=line.split(":",1)[1].strip(); continue
        parts=line.split()
        if dll and len(parts)>=2 and re.fullmatch(r"[A-Za-z_?@][A-Za-z0-9_?@$.-]*",parts[-1]) and any(re.fullmatch(r"(?:0x)?[0-9A-Fa-f]+",x) for x in parts[:-1]):
            rows.append((dll,parts[-1]))
    return sorted(set(rows))

def path_sets(strings):
    paths=set()
    for s in strings:
        low=s.lower()
        if "data\\" in low or "data/" in low or "map\\" in low or "map/" in low:
            for m in re.finditer(r"(?i)(?:data|map)[\\/][A-Za-z0-9_ .%*()\-\\/]+\.[A-Za-z0-9]{2,5}",s):
                paths.add(m.group().replace("/","\\"))
    return paths

def battle_ids(paths):
    out=[]
    for p in paths:
        m=re.search(r"(?i)battlemap\\battle(\d+)\.sab$",p)
        if m: out.append(int(m.group(1)))
    return sorted(set(out))

def marker_presence(data):
    ascii_blob=data.lower()
    rows=[]
    for n in NEEDLES:
        a=n.encode("ascii","ignore")
        u=n.encode("utf-16le")
        ac=ascii_blob.count(a.lower()) if a else 0
        uc=data.count(u)
        rows.append((n,ac,uc))
    return rows

def resource_neighborhood(data):
    urows=utf16_strings(data)
    result=[]
    for key in RESOURCE_KEYS:
        hits=[off for off,s in urows if s==key]
        for off in hits:
            near=[s for o,s in urows if off-400<=o<=off+900]
            result.append((key,off,near[:40]))
    return result

def main():
    print("StoneAge Waei sa40/sa42 runtime-lineage probe — R1")
    print("CONTROL|accepted Taiwan-v1 runtime=sa_3.exe|size=425984|sha256=cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a")
    print("CONTROL|Taiwan-v1 sa_3.exe imports=DDRAW,DINPUT,DSOUND,GDI32,IMM32,KERNEL32,USER32,WINMM,WSOCK32")
    print("CONTROL|Taiwan-v1 runtime strings include ClientLogin,CharLogin,PPASSWORD,yStoneAge.exe,data resource generations and wgs@mail.hwaei.com.tw")
    blobs={}; pathmap={}; importmap={}; errors=[]
    for label,ts,orig in TARGETS:
        try:
            b=fetch(ts,orig); blobs[label]=b
            stamp=pe_timestamp(b)
            stamp_iso=dt.datetime.fromtimestamp(stamp,dt.timezone.utc).isoformat() if stamp else ""
            astr=ascii_strings(b)
            paths=path_sets(astr); pathmap[label]=paths
            bids=battle_ids(paths)
            imps=imports(b); importmap[label]=imps
            dlls=sorted({d for d,_ in imps}); funcs=sorted({f for _,f in imps})
            print(f"PAYLOAD|label={label}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|pe_timestamp={stamp}|pe_timestamp_utc={stamp_iso}|ascii_strings={len(astr)}|paths={len(paths)}|battle_ids={len(bids)}|battle_min={min(bids) if bids else ''}|battle_max={max(bids) if bids else ''}")
            print(f"IMPORTS|label={label}|dlls={len(dlls)}|functions={len(funcs)}|dll_values={','.join(dlls)}")
            for n,ac,uc in marker_presence(b):
                print(f"MARKER|label={label}|name={clean(n)}|ascii_count={ac}|utf16_count={uc}")
            for key,off,near in resource_neighborhood(b):
                print(f"VERSION_RESOURCE_NEAR|label={label}|key={key}|offset={off}|strings={clean(' || '.join(near),3500)}")
            for p in sorted(paths):
                if re.search(r"(?i)(AISetting|server|setting|config|battlemap\\battle2(?:1[8-9]|2\d)\.sab|real_\d+|adrn_\d+|spr_\d+|spradrn_\d+)",p):
                    print(f"PATH_SIGNAL|label={label}|path={clean(p)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
            print(f"ERROR|label={label}|kind={type(e).__name__}|message={clean(e)}")
    if "sa40" in pathmap and "sa42" in pathmap:
        a=pathmap["sa40"]; b=pathmap["sa42"]
        print(f"PATH_DIFF|common={len(a&b)}|only_sa40={len(a-b)}|only_sa42={len(b-a)}")
        for p in sorted(a-b): print(f"PATH_ONLY|label=sa40|path={clean(p)}")
        for p in sorted(b-a): print(f"PATH_ONLY|label=sa42|path={clean(p)}")
    if "sa40" in importmap and "sa42" in importmap:
        a=set(importmap["sa40"]); b=set(importmap["sa42"])
        print(f"IMPORT_DIFF|common={len(a&b)}|only_sa40={len(a-b)}|only_sa42={len(b-a)}")
        for d,f in sorted(a-b): print(f"IMPORT_ONLY|label=sa40|dll={clean(d)}|function={clean(f)}")
        for d,f in sorted(b-a): print(f"IMPORT_ONLY|label=sa42|dll={clean(d)}|function={clean(f)}")
    print(f"COUNT|errors|{len(errors)}")
    if len(blobs)==2 and not errors:
        print("RESOLUTION|RUNTIME_LINEAGE_SIGNALS_BOUND|interpret version-resource strings and TW10 continuity next")
    else:
        print("RESOLUTION|PARTIAL_RUNTIME_LINEAGE|retry failed exact artifact only")
    print("EVIDENCE_BOUNDARY|filename sa_40/sa_42 is not by itself a version proof; classification must agree with byte structure and contemporaneous chronology.")

if __name__=="__main__":
    main()
