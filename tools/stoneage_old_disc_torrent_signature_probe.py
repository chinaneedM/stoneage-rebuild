#!/usr/bin/env python3
"""Scan public old-disc torrent metadata for StoneAge-specific file/path signatures.

Metadata only: downloads allseeds.zip (torrent files) and never retrieves disc,
archive, client, or game payload bytes.
"""
from __future__ import annotations
import hashlib, io, urllib.request, zipfile
from tools.stoneage_sa25_old_disc_torrent_probe import (
    URL, UA, MAX_ZIP, MAX_TORRENT, bdecode, root_info_span, torrent_paths,
)

EXACT_BASENAMES=(
    "stoneage.exe","sa_3.exe","waei.bin",
    "real_1.bin","adrn_1.bin","spr_1.bin","spradrn_1.bin","battle_1.bin",
    "battletxt_1.txt","soundaddr_1.txt",
    "sa_2903.exe","real_15.bin","adrn_15.bin","spr_4.bin","spradrn_5.bin",
)
LEXICAL=(
    "stoneage","石器时代","石器時代","精灵王传说","精靈王傳說",
    "永远的石器时代","永遠的石器時代",
    "万方数据电子出版社","萬方數據電子出版社",
    "7-900096-07-8","7900096078","9787900096074",
)

def clean(v,n=3200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:n]

def basename(path):
    return path.replace("\\","/").rstrip("/").split("/")[-1].lower()

def classify(path):
    low=path.lower()
    base=basename(path)
    exact=tuple(x for x in EXACT_BASENAMES if base==x)
    lexical=tuple(x for x in LEXICAL if x.lower() in low)
    return exact,lexical

def fetch_zip():
    req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept":"application/zip,*/*"})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(MAX_ZIP+1)
        if len(b)>MAX_ZIP: raise ValueError("allseeds-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def main():
    print("StoneAge old-disc torrent signature probe — R1")
    print("SCOPE|public-allseeds.zip|torrent-path-metadata-only|no-disc-or-game-payload")
    st,final,h,zbytes=fetch_zip()
    print(f"ZIP|status={st}|bytes={len(zbytes)}|sha256={hashlib.sha256(zbytes).hexdigest()}|content_type={clean(h.get('Content-Type'))}|last_modified={clean(h.get('Last-Modified'))}|final={clean(final)}")
    totals={"torrent":0,"matching_torrents":0,"matching_paths":0,"exact_paths":0,"lexical_paths":0,"multi_exact":0,"errors":0}
    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        print(f"COUNT|zip_entries|{len(z.namelist())}")
        for entry in z.namelist():
            if not entry.lower().endswith(".torrent"): continue
            totals["torrent"]+=1
            try:
                zi=z.getinfo(entry)
                if zi.file_size>MAX_TORRENT:
                    print(f"SKIP|entry={clean(entry)}|reason=torrent-too-large|bytes={zi.file_size}")
                    continue
                raw=z.read(entry)
                meta,_=bdecode(raw,0)
                paths=torrent_paths(meta)
                hits=[]; exact_names=set(); lexical_names=set()
                for p in paths:
                    exact,lexical=classify(p)
                    if exact or lexical:
                        hits.append((p,exact,lexical))
                        exact_names.update(exact); lexical_names.update(lexical)
                if not hits: continue
                totals["matching_torrents"]+=1
                totals["matching_paths"]+=len(hits)
                totals["exact_paths"]+=sum(bool(e) for _,e,_ in hits)
                totals["lexical_paths"]+=sum(bool(l) for _,_,l in hits)
                if len(exact_names)>=2: totals["multi_exact"]+=1
                try:
                    s,e=root_info_span(raw); infohash=hashlib.sha1(raw[s:e]).hexdigest()
                except Exception: infohash=""
                cls="MULTI_EXACT_CLIENT_SIGNATURE" if len(exact_names)>=2 else ("EXACT_SIGNATURE" if exact_names else "LEXICAL_ONLY")
                print(f"TORRENT|entry={clean(entry)}|bytes={len(raw)}|sha256={hashlib.sha256(raw).hexdigest()}|infohash={infohash}|paths={len(paths)}|matching_paths={len(hits)}|exact_names={clean(','.join(sorted(exact_names)))}|lexical_names={clean(','.join(sorted(lexical_names)))}|classification={cls}")
                for p,exact,lexical in hits[:300]:
                    print(f"PATH|entry={clean(entry)}|exact={clean(','.join(exact))}|lexical={clean(','.join(lexical))}|value={clean(p)}")
            except Exception as e:
                totals["errors"]+=1
                print(f"ERROR|entry={clean(entry)}|kind={type(e).__name__}|message={clean(e)}")
    print(f"COUNT|torrent_entries|{totals['torrent']}")
    print(f"COUNT|matching_torrents|{totals['matching_torrents']}")
    print(f"COUNT|matching_paths|{totals['matching_paths']}")
    print(f"COUNT|exact_signature_paths|{totals['exact_paths']}")
    print(f"COUNT|lexical_paths|{totals['lexical_paths']}")
    print(f"COUNT|multi_exact_client_signature_torrents|{totals['multi_exact']}")
    print(f"COUNT|errors|{totals['errors']}")
    if totals["multi_exact"]:
        print("RESOLUTION|HIGH_VALUE_INSTALLED_TREE_OR_MEDIA_CANDIDATE|verify provenance and file-tree identity next")
    elif totals["exact_paths"]:
        print("RESOLUTION|EXACT_SIGNATURE_CANDIDATE|inspect co-located paths before any payload recovery")
    elif totals["lexical_paths"]:
        print("RESOLUTION|LEXICAL_CANDIDATES_ONLY|inspect names but do not infer client identity")
    elif totals["errors"]:
        print("RESOLUTION|PARTIAL_METADATA_FAILURE|retry only failed torrent metadata")
    else:
        print("RESOLUTION|NO_STONEAGE_SIGNATURE_PATHS|tested public torrent metadata surface contains no target path")
    print("EVIDENCE_BOUNDARY|torrent path metadata can identify preservation candidates only; it does not establish original-client provenance, cleanliness, or byte identity.")

if __name__=="__main__":
    main()
