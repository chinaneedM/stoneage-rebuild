#!/usr/bin/env python3
"""Analyze recovered StoneAge magic.txt using the descendant server loader schema."""

import argparse,collections,hashlib
from pathlib import Path

CHAR_FIELDS=4
INT_NAMES=["ID","FIELD","TARGET","TARGET_DEADFLG"]

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def clean_lines(path):
    for raw in path.read_bytes().splitlines():
        line=raw.strip()
        if not line or line.startswith(b"#"): continue
        yield line

def to_int(v):
    try:return int(v.strip() or b"-1",10)
    except ValueError:return None

def setup_value(path,key):
    if not path or not path.exists(): return None
    key=key.lower()
    for raw in path.read_bytes().splitlines():
        line=raw.split(b"#",1)[0].strip()
        if b"=" not in line: continue
        k,v=line.split(b"=",1)
        if k.decode("ascii","ignore").strip().lower()==key:
            return v.decode("utf-8","replace").strip()
    return None

def parse(path):
    raw_rows=[]; parsed=[]; malformed=0; counts=collections.Counter(); max_cols=0
    for line in clean_lines(path):
        fields=[x.strip() for x in line.replace(b"\t",b" ").split(b",")]
        raw_rows.append(fields); counts[len(fields)]+=1; max_cols=max(max_cols,len(fields))
        if len(fields)<8:
            malformed+=1; continue
        vals={}; ok=True
        for i,name in enumerate(INT_NAMES):
            v=to_int(fields[CHAR_FIELDS+i])
            if v is None:
                ok=False; break
            vals[name]=v
        if not ok:
            malformed+=1; continue
        vals["IDX"]=None
        if len(fields)>=9 and fields[8]:
            vals["IDX"]=to_int(fields[8])
            if vals["IDX"] is None:
                malformed+=1; continue
        parsed.append((fields,vals))
    profiles=[]
    for idx in range(max_cols):
        integer=empty=text=missing=0
        for fields in raw_rows:
            if idx>=len(fields): missing+=1; continue
            v=fields[idx].strip()
            if not v: empty+=1
            elif to_int(v) is not None: integer+=1
            else: text+=1
        profiles.append((idx+1,integer,empty,text,missing))
    return raw_rows,parsed,malformed,counts,profiles

def analyze(data_dir,setup=None):
    path=data_dir/"magic.txt"
    active=setup_value(setup,"magicfile")
    if not path.exists():
        return {"active":active,"exists":False}
    raw,parsed,bad,field_counts,profiles=parse(path)
    ids=[v["ID"] for _,v in parsed]
    idset=set(ids)
    counters={k:collections.Counter() for k in ("FIELD","TARGET","TARGET_DEADFLG","IDX","EFFECTIVE_TARGET")}
    funcs=collections.Counter()
    for fields,v in parsed:
        if len(fields)>=3 and fields[2]: funcs[fields[2]]+=1
        counters["FIELD"][v["FIELD"]]+=1
        counters["TARGET"][v["TARGET"]]+=1
        counters["TARGET_DEADFLG"][v["TARGET_DEADFLG"]]+=1
        if v["IDX"] is not None: counters["IDX"][v["IDX"]]+=1
        effective=v["TARGET"]+100 if v["TARGET_DEADFLG"]==1 else v["TARGET"]
        counters["EFFECTIVE_TARGET"][effective]+=1
    return {
        "active":active,"exists":True,"bytes":path.stat().st_size,"sha":sha256(path),
        "raw_rows":len(raw),"parsed_rows":len(parsed),"malformed":bad,
        "field_counts":field_counts,"profiles":profiles,
        "id_min":min(ids) if ids else None,"id_max":max(ids) if ids else None,
        "id_unique":len(idset),"id_duplicates":len(ids)-len(idset),
        "func_count":len(funcs),"counters":counters,
        "active_match":bool(active and Path(active.replace("\\","/")).name.lower()=="magic.txt")
    }

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered magic-table probe — R1")
    print("No original magic names/comments/options are stored in this report.")
    print("SCHEMA_SOURCE|descendant_MAGIC_initMagic")
    print("SCHEMA|4 char fields + ID,FIELD,TARGET,TARGET_DEADFLG + optional attack-magic IDX")
    print(f"MAGIC_CONFIG|{r.get('active') or 'UNKNOWN'}")
    if not r["exists"]:
        print("MAGIC_FILE_EXISTS|0"); return
    print("MAGIC_FILE_EXISTS|1")
    print(f"FILE|magic.txt|bytes={r['bytes']}|sha256={r['sha']}|rows={r['raw_rows']}|parsed={r['parsed_rows']}|malformed={r['malformed']}|active={int(r['active_match'])}")
    for n,c in sorted(r["field_counts"].items()):
        print(f"FIELD_COUNT|magic.txt|{n}|{c}")
    for col,integer,empty,text,missing in r["profiles"]:
        print(f"COLUMN_PROFILE|magic.txt|{col}|integer={integer}|empty={empty}|text={text}|missing={missing}")
    print(f"ID_STAT|magic.txt|min={r['id_min']}|max={r['id_max']}|unique={r['id_unique']}|duplicates={r['id_duplicates']}")
    print(f"UNIQUE_FUNCTION_TOKENS|magic.txt|{r['func_count']}")
    for key in ("FIELD","TARGET","TARGET_DEADFLG","EFFECTIVE_TARGET"):
        for v,n in sorted(r["counters"][key].items()):
            print(f"{key}_VALUE|magic.txt|{v}|{n}")
    print(f"IDX_PRESENT_ROWS|magic.txt|{sum(r['counters']['IDX'].values())}")
    for v,n in r["counters"]["IDX"].most_common(20):
        print(f"IDX_TOP|magic.txt|{v}|{n}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args(); emit(a.data_dir,a.setup)

if __name__=="__main__": main()
