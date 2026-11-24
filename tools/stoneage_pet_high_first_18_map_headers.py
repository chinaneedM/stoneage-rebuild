"""Extract only source-bounded map header metadata for PET17 encounter floors."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56"
SOURCE_TREE = "33f71a5f804480cec28edee4bd6a6d1851ba2dab"
INPUT = ROOT / "research/pets/PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json"
REPORT = ROOT / "research/pets/PET-HIGH-FIRST-18-COMPARISON-MAP-HEADERS-R1.json"

def git(root, *args):
    return subprocess.check_output(["git","-C",str(root),*args])

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def read(root):
    assert git(root,"rev-parse","HEAD").decode().strip()==SOURCE_COMMIT
    assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==SOURCE_TREE
    raw_input=INPUT.read_bytes()
    pet=json.loads(raw_input)
    floors=sorted({f for x in pet["rows"] for f in x["comparison_floor_ids"]})
    wanted=set(floors)
    assert len(floors)==349
    found=defaultdict(list)
    counts=dict(source_map_tree_blobs=0,source_map_bytes=0,valid_map_headers=0,
                nonmap_files=0,invalid_size_maps=0,header_filename_id_disagreements=0)
    for record in git(root,"ls-tree","-rz","HEAD","--","gmsv/data/map").split(b"\0"):
        if not record:
            continue
        meta,path=record.split(b"\t",1)
        mode,kind,sha=meta.decode("ascii").split()
        assert kind=="blob"
        path=path.decode("utf-8")
        raw=(root/path).read_bytes()
        assert blob(raw)==sha, path
        counts["source_map_tree_blobs"]+=1
        counts["source_map_bytes"]+=len(raw)
        if len(raw)<44 or raw[:6]!=b"LS2MAP":
            counts["nonmap_files"]+=1
            continue
        fid=struct.unpack_from(">H",raw,6)[0]
        w,h=struct.unpack_from(">HH",raw,40)
        if not w or not h or len(raw)!=44+4*w*h:
            counts["invalid_size_maps"]+=1
            continue
        counts["valid_map_headers"]+=1
        basename=Path(path).name
        if basename.isdecimal() and int(basename)!=fid:
            counts["header_filename_id_disagreements"]+=1
        if fid not in wanted:
            continue
        # Native loader forces the last byte of the 32-byte name buffer to zero.
        name_raw=raw[8:39].split(b"\0",1)[0]
        names={}
        for codec in ("gb18030","cp950"):
            try:
                names[codec]=name_raw.decode(codec)
            except UnicodeDecodeError:
                names[codec]=None
        found[fid].append(dict(path=path,blob=sha,bytes=len(raw),width=w,height=h,
             name_raw_sha256=hashlib.sha256(name_raw).hexdigest(),
             header_sha256=hashlib.sha256(raw[:44]).hexdigest(),names=names))
    assert counts["source_map_tree_blobs"]==1284
    assert counts["source_map_bytes"]==49808963
    rows=[]
    for fid in floors:
        candidates=found[fid]
        fingerprints={(x["width"],x["height"],x["name_raw_sha256"]) for x in candidates}
        status=("MISSING" if not candidates else
                "UNIQUE_HEADER" if len(candidates)==1 else
                "MULTIPLE_FILES_SAME_HEADER_FIELDS" if len(fingerprints)==1 else
                "CONFLICTING_HEADER_FIELDS")
        rows.append(dict(floor=fid,status=status,candidates=candidates))
    return dict(scope="LATER_PC_COMPARISON_SAME_COMMIT_MAP_HEADERS_NOT_OFFICIAL",
        comparison_commit=SOURCE_COMMIT,comparison_tree=SOURCE_TREE,pet17_blob=blob(raw_input),
        counts=counts,rows=rows,official_map_or_capture_verified=False,runtime_executed=False)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path)
    args=p.parse_args()
    report=read(args.source)
    if REPORT.exists():
        assert json.loads(REPORT.read_bytes())==report
    from collections import Counter
    print("SUMMARY",json.dumps({"counts":report["counts"],"status":Counter(x["status"] for x in report["rows"])},ensure_ascii=False,sort_keys=True))
    # Separate bounded lines avoid truncation of a single large CI log line.
    print("META",json.dumps({k:v for k,v in report.items() if k!="rows"},ensure_ascii=False,separators=(",",":")))
    for row in report["rows"]:
        print("MAP_ROW",json.dumps(row,ensure_ascii=False,separators=(",",":")))
    print("END_MAP_ROWS",len(report["rows"]))

if __name__=="__main__":
    main()
