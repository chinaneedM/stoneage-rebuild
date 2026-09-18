#!/usr/bin/env python3
"""Analyze recovered StoneAge attmagic.bin and cross-link magic.txt IDX values."""

import argparse,collections,hashlib,struct
from pathlib import Path
from tools.stoneage_magic_probe import parse as parse_magic

RECORD_WORDS=33
RECORD_SIZE=RECORD_WORDS*4
FIELD_NAMES=[
    "SPRITE_NUM","ATTACK_TYPE","SLICE_TIME","SHOW_TYPE","SX","SY",
    "SHOW_BEHIND_CHAR","SHAKE_SCREEN","SHAKE_FROM","SHAKE_TO",
    "PREV_MAGIC_NUM","PREV_MAGIC_SX","PREV_MAGIC_SY","PREV_MAGIC_ON_CHAR",
    "POST_MAGIC_NUM","POST_MAGIC_SX","POST_MAGIC_SY","POST_MAGIC_ON_CHAR",
]
SIGNED={4,5,11,12,13,15,16,17}
UNSIGNED=set(range(18))-SIGNED

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def s32(v):
    return v-0x100000000 if v&0x80000000 else v

def parse_attmagic(path):
    data=path.read_bytes()
    if len(data)%RECORD_SIZE:
        raise ValueError(f"size_not_multiple:{len(data)}:{RECORD_SIZE}")
    records=[]
    for off in range(0,len(data),RECORD_SIZE):
        records.append(struct.unpack_from("<33I",data,off))
    return records

def analyze(data_dir):
    path=data_dir/"attmagic.bin"
    magic_path=data_dir/"magic.txt"
    if not path.exists():
        return {"exists":False}
    records=parse_attmagic(path)
    raw_count=len(records)
    source_even=(raw_count%2==0)
    effective_count=(raw_count//2) if source_even else None
    pair_exact=0
    pair_diff=0
    if effective_count is not None:
        for i in range(effective_count):
            if records[i]==records[i+effective_count]:pair_exact+=1
            else:pair_diff+=1

    idxs=[]; magic_bad=None
    if magic_path.exists():
        _,parsed,magic_bad,_,_=parse_magic(magic_path)
        idxs=[v["IDX"] for _,v in parsed if v["IDX"] is not None]
    idxset=set(idxs)
    valid_idx=set()
    invalid_idx=set()
    if effective_count is not None:
        valid_idx={v for v in idxset if 0<=v<effective_count}
        invalid_idx=idxset-valid_idx
    else:
        invalid_idx=idxset

    field_stats=[]
    effective=records[:effective_count] if effective_count is not None else records
    for i,name in enumerate(FIELD_NAMES):
        vals=[r[i] if i in UNSIGNED else s32(r[i]) for r in effective]
        field_stats.append((name,min(vals) if vals else None,max(vals) if vals else None,len(set(vals))))

    attack=collections.Counter(r[1] for r in effective)
    show=collections.Counter(r[3] for r in effective)
    behind=collections.Counter(r[6] for r in effective)
    shake=collections.Counter(r[7] for r in effective)
    prev_sentinel=sum(1 for r in effective if r[10]==0xffffffff)
    post_sentinel=sum(1 for r in effective if r[14]==0xffffffff)

    matrix=[]
    for r in effective:
        matrix.extend(s32(v) for v in r[18:33])

    return {
        "exists":True,"bytes":path.stat().st_size,"sha":sha256(path),
        "raw_count":raw_count,"source_even":source_even,"effective_count":effective_count,
        "pair_exact":pair_exact,"pair_diff":pair_diff,
        "idxs":idxs,"idx_unique":idxset,"valid_idx":valid_idx,"invalid_idx":invalid_idx,
        "magic_bad":magic_bad,
        "unreferenced":sorted(set(range(effective_count or 0))-valid_idx),
        "field_stats":field_stats,"attack":attack,"show":show,"behind":behind,"shake":shake,
        "prev_sentinel":prev_sentinel,"post_sentinel":post_sentinel,
        "matrix_min":min(matrix) if matrix else None,"matrix_max":max(matrix) if matrix else None,
        "matrix_unique":len(set(matrix)),"matrix_zero":sum(1 for v in matrix if v==0),
    }

def emit(data_dir):
    r=analyze(data_dir)
    print("StoneAge recovered attack-magic binary probe — R1")
    print("No proprietary attack-magic payload bytes are stored in this report.")
    print("SCHEMA_SOURCE|descendant_tagAttMagic_and_ATTMAGIC_initMagic")
    print(f"RECORD_SIZE|{RECORD_SIZE}")
    if not r["exists"]:
        print("ATTMAGIC_FILE_EXISTS|0");return
    print("ATTMAGIC_FILE_EXISTS|1")
    print(f"FILE|attmagic.bin|bytes={r['bytes']}|sha256={r['sha']}")
    print(f"RAW_RECORD_COUNT|{r['raw_count']}")
    print(f"SOURCE_EVEN_RECORD_REQUIREMENT|{int(r['source_even'])}")
    print(f"SOURCE_EFFECTIVE_RECORD_COUNT|{r['effective_count'] if r['effective_count'] is not None else -1}")
    print(f"HALF_PAIR_EXACT|{r['pair_exact']}")
    print(f"HALF_PAIR_DIFFERENT|{r['pair_diff']}")
    print(f"MAGIC_IDX_PRESENT_ROWS|{len(r['idxs'])}")
    print(f"MAGIC_IDX_UNIQUE|{len(r['idx_unique'])}")
    if r["idxs"]:
        print(f"MAGIC_IDX_RANGE|min={min(r['idxs'])}|max={max(r['idxs'])}")
    print(f"MAGIC_IDX_VALID_UNIQUE|{len(r['valid_idx'])}")
    print(f"MAGIC_IDX_INVALID_UNIQUE|{len(r['invalid_idx'])}")
    if r["invalid_idx"]:print("MAGIC_IDX_INVALID_VALUES|"+",".join(map(str,sorted(r["invalid_idx"]))))
    print(f"EFFECTIVE_RECORDS_UNREFERENCED_BY_MAGIC_IDX|{len(r['unreferenced'])}")
    if r["unreferenced"]:print("EFFECTIVE_UNREFERENCED_INDEX_SAMPLE|"+",".join(map(str,r["unreferenced"][:40])))
    for name,lo,hi,uniq in r["field_stats"]:
        print(f"FIELD_STAT|{name}|min={lo}|max={hi}|unique={uniq}")
    for key,counter in (("ATTACK_TYPE",r["attack"]),("SHOW_TYPE",r["show"]),("SHOW_BEHIND_CHAR",r["behind"]),("SHAKE_SCREEN",r["shake"])):
        for v,n in sorted(counter.items()):print(f"{key}_VALUE|{v}|{n}")
    print(f"PREV_MAGIC_SENTINEL_FFFFFFFF|{r['prev_sentinel']}")
    print(f"POST_MAGIC_SENTINEL_FFFFFFFF|{r['post_sentinel']}")
    print(f"FIELD_MATRIX_STAT|min={r['matrix_min']}|max={r['matrix_max']}|unique={r['matrix_unique']}|zero={r['matrix_zero']}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    a=ap.parse_args();emit(a.data_dir)

if __name__=="__main__":main()
