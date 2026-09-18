#!/usr/bin/env python3
"""Validate the recovered 94-column StoneAge itemset schema without storing item text."""

import argparse,collections,hashlib
from pathlib import Path

def col(name,kind): return (name,kind)
SCHEMA=[
    col("name","text"),col("secretname","text"),col("effectstring","text"),col("argument","text"),
    col("acode","text"),col("inlaycode","text"),
    col("initfunc","text"),col("preoverfunc","text"),col("postoverfunc","text"),col("watchfunc","text"),
    col("usefunc","text"),col("attachfunc","text"),col("detachfunc","text"),col("dropfunc","text"),
    col("pickupfunc","text"),col("relifefunc","text"),
    col("id","int"),col("imagenumber","int"),col("cost","int"),col("type","int"),
    col("fieldtype","int"),col("target","int"),col("level","int"),col("dambreak","int"),
    col("upinums","int"),col("campile","int"),col("nestr","int"),col("nedex","int"),
    col("netra","int"),col("neprof","int"),col("damcrushe","int"),col("maxdmce","int"),
    col("otdmags","int"),col("otdefcs","int"),col("nsuit","int"),
    col("attacknum_min","int"),col("attacknum_max","int"),
]
for n in ("attack","defence","quick","hp","mp","luck","charm","avoid"):
    SCHEMA.extend([col(n+"_raw_a","int"),col(n+"_raw_b","int")])
SCHEMA.extend([
    col("attrib","int"),col("attribvalue","int"),col("magicid","int"),col("magicprob","int"),
    col("magicusemp","int"),col("arr","int"),col("seqce","int"),col("iapi","int"),
    col("hirt","int"),col("neguard","int"),
])
for n in ("poison","paralysis","sleep","stone","drunk","confusion","critical"):
    SCHEMA.extend([col(n+"_raw_a","int"),col(n+"_raw_b","int")])
SCHEMA.extend([
    col("useaction","int"),col("dropatlogout","bool"),col("vanishatdrop","bool"),
    col("isovered","bool"),col("canpetmail","bool"),col("canmergefrom","bool"),col("canmergeto","bool"),
    col("ingname0","text"),col("ingvalue0","int"),col("ingname1","text"),col("ingvalue1","int"),
    col("ingname2","text"),col("ingvalue2","int"),col("ingname3","text"),col("ingvalue3","int"),
    col("ingname4","text"),col("ingvalue4","int"),
])
assert len(SCHEMA)==94
INDEX={name:i for i,(name,_) in enumerate(SCHEMA)}

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def to_int(v):
    try:return int(v.strip(),10)
    except ValueError:return None

def clean_rows(path):
    rows=[]
    for raw in path.read_bytes().splitlines():
        line=raw.strip()
        if not line or line.startswith(b"#"): continue
        rows.append([x.strip() for x in line.replace(b"\t",b" ").split(b",")])
    return rows

def setup_itemsets(path):
    out={}
    if not path or not path.exists():return out
    for raw in path.read_bytes().splitlines():
        line=raw.split(b"#",1)[0].strip()
        if b"=" not in line:continue
        k,v=line.split(b"=",1)
        key=k.decode("ascii","ignore").strip().lower()
        val=v.decode("utf-8","replace").strip()
        base=Path(val.replace("\\","/")).name.lower()
        if base.startswith("itemset") and base.endswith(".txt"):out[key]=val
    return out

def parse_magic_ids(path):
    ids=set()
    if not path.exists():return ids
    for raw in path.read_bytes().splitlines():
        line=raw.strip()
        if not line or line.startswith(b"#"):continue
        fields=[x.strip() for x in line.replace(b"\t",b" ").split(b",")]
        if len(fields)>=5:
            v=to_int(fields[4])
            if v is not None:ids.add(v)
    return ids

def validate_file(path,active_names,magic_ids):
    rows=clean_rows(path)
    wrong_width=sum(1 for r in rows if len(r)!=len(SCHEMA))
    stats=[]
    invalid_cells=[]
    ids=[]; magic_refs=[]
    parsed_by_id={}
    for ci,(name,kind) in enumerate(SCHEMA):
        empty=integer=text=invalid=0
        values=[]
        for ri,r in enumerate(rows):
            if ci>=len(r):
                invalid+=1;continue
            v=r[ci].strip()
            if not v:
                empty+=1;continue
            n=to_int(v)
            if n is not None:integer+=1
            else:text+=1
            ok=True
            if kind=="int":ok=n is not None
            elif kind=="bool":ok=n in (0,1)
            if not ok:
                invalid+=1
                if len(invalid_cells)<40:invalid_cells.append((ri+1,ci+1,name))
            if n is not None:values.append(n)
        stats.append({
            "col":ci+1,"name":name,"kind":kind,"empty":empty,"integer":integer,
            "text":text,"invalid":invalid,"unique_int":len(set(values)),
            "min":min(values) if values else None,"max":max(values) if values else None,
        })
    if not wrong_width:
        ididx=INDEX["id"]; midx=INDEX["magicid"]
        for r in rows:
            iid=to_int(r[ididx]); mid=to_int(r[midx])
            if iid is not None:
                ids.append(iid);parsed_by_id[iid]=r
            if mid is not None and mid>=0:magic_refs.append(mid)
    idset=set(ids)
    mset=set(magic_refs)
    return {
        "name":path.name,"bytes":path.stat().st_size,"sha":sha256(path),
        "rows":rows,"row_count":len(rows),"wrong_width":wrong_width,"stats":stats,
        "invalid_cells":invalid_cells,"ids":ids,"idset":idset,"by_id":parsed_by_id,
        "id_duplicates":len(ids)-len(idset),
        "magic_refs":magic_refs,"magic_unique":mset,
        "magic_matched":mset&magic_ids,"magic_missing":sorted(mset-magic_ids),
        "active":path.name.lower() in active_names,
    }

def diff_files(a,b):
    shared=sorted(a["idset"]&b["idset"])
    changed_rows=0; changed_cells=collections.Counter()
    for iid in shared:
        ra=a["by_id"][iid]; rb=b["by_id"][iid]
        changed=False
        for i,(name,_) in enumerate(SCHEMA):
            if ra[i]!=rb[i]:
                changed=True;changed_cells[name]+=1
        if changed:changed_rows+=1
    return {
        "a":a["name"],"b":b["name"],"shared":len(shared),
        "a_only":len(a["idset"]-b["idset"]),"b_only":len(b["idset"]-a["idset"]),
        "changed_rows":changed_rows,"unchanged_rows":len(shared)-changed_rows,
        "changed_cells":changed_cells,
        "b_only_ids":sorted(b["idset"]-a["idset"]),
    }

def analyze(data_dir,setup=None):
    config=setup_itemsets(setup)
    active_names={Path(v.replace("\\","/")).name.lower() for v in config.values()}
    magic_ids=parse_magic_ids(data_dir/"magic.txt")
    files=[validate_file(p,active_names,magic_ids) for p in sorted(data_dir.glob("itemset*.txt"),key=lambda p:p.name.lower())]
    diffs=[]
    for i in range(len(files)):
        for j in range(i+1,len(files)):diffs.append(diff_files(files[i],files[j]))
    return {"config":config,"magic_ids":magic_ids,"files":files,"diffs":diffs}

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered itemset schema probe — R1")
    print("No original item names/descriptions/function strings are stored in this report.")
    print("SCHEMA_SOURCE|descendant_ITEM_itemDescriptors_pre_reserved10_layout")
    print("SCHEMA_COLUMNS|94")
    print("ID_COLUMN|17")
    print("MAGICID_COLUMN|56")
    for i,(name,kind) in enumerate(SCHEMA,1):
        print(f"SCHEMA_COLUMN|{i}|{name}|{kind}")
    for k,v in sorted(r["config"].items()):print(f"ITEMSET_CONFIG|{k}|{v}")
    print(f"MAGIC_ID_REFERENCE_SET|{len(r['magic_ids'])}")
    for f in r["files"]:
        print(f"FILE|{f['name']}|bytes={f['bytes']}|sha256={f['sha']}|rows={f['row_count']}|active={int(f['active'])}|wrong_width={f['wrong_width']}|id_duplicates={f['id_duplicates']}")
        invalid_total=sum(s["invalid"] for s in f["stats"])
        print(f"SCHEMA_INVALID_CELL_COUNT|{f['name']}|{invalid_total}")
        for s in f["stats"]:
            print(f"COLUMN_STAT|{f['name']}|{s['col']}|{s['name']}|{s['kind']}|empty={s['empty']}|integer={s['integer']}|text={s['text']}|invalid={s['invalid']}|unique_int={s['unique_int']}|min={s['min']}|max={s['max']}")
        print(f"MAGIC_REF|{f['name']}|rows={len(f['magic_refs'])}|unique={len(f['magic_unique'])}|matched={len(f['magic_matched'])}|missing={len(f['magic_missing'])}")
        if f["magic_missing"]:print(f"MAGIC_REF_MISSING_SAMPLE|{f['name']}|"+",".join(map(str,f["magic_missing"][:40])))
    for d in r["diffs"]:
        print(f"FILE_DIFF|{d['a']}|{d['b']}|shared={d['shared']}|a_only={d['a_only']}|b_only={d['b_only']}|changed_rows={d['changed_rows']}|unchanged_rows={d['unchanged_rows']}")
        if d["b_only_ids"]:
            print(f"B_ONLY_ID_RANGE|{d['a']}|{d['b']}|min={min(d['b_only_ids'])}|max={max(d['b_only_ids'])}")
            print(f"B_ONLY_ID_SAMPLE|{d['a']}|{d['b']}|"+",".join(map(str,d["b_only_ids"][:40])))
        for name,n in d["changed_cells"].most_common():
            print(f"DIFF_COLUMN|{d['a']}|{d['b']}|{name}|{n}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(a.data_dir,a.setup)

if __name__=="__main__":main()
