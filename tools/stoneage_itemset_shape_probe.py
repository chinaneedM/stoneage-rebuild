#!/usr/bin/env python3
"""Profile recovered StoneAge itemset text files before assigning a versioned schema."""

import argparse,collections,hashlib
from pathlib import Path

ID_CANDIDATE_COLS=(15,17)

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def clean_lines(path):
    for raw in path.read_bytes().splitlines():
        line=raw.strip()
        if not line or line.startswith(b"#"):continue
        yield line

def to_int(v):
    try:return int(v.strip(),10)
    except ValueError:return None

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
        if base.startswith("itemset") and base.endswith(".txt"):
            out[key]=val
    return out

def column_stats(rows,col1):
    idx=col1-1
    vals=[];missing=0;empty=0;integer=0;text=0;ints=[]
    for r in rows:
        if idx>=len(r):
            missing+=1;continue
        v=r[idx].strip();vals.append(v)
        if not v:empty+=1
        else:
            n=to_int(v)
            if n is None:text+=1
            else:integer+=1;ints.append(n)
    counter=collections.Counter(ints)
    return {
        "col":col1,"missing":missing,"empty":empty,"integer":integer,"text":text,
        "unique_int":len(counter),"duplicates":sum(n-1 for n in counter.values() if n>1),
        "min":min(ints) if ints else None,"max":max(ints) if ints else None,
        "zero":counter.get(0,0),"negative":sum(n for v,n in counter.items() if v<0),
    }

def analyze_file(path,active_names):
    rows=[];field_counts=collections.Counter();max_cols=0
    for line in clean_lines(path):
        fields=[x.strip() for x in line.replace(b"\t",b" ").split(b",")]
        rows.append(fields);field_counts[len(fields)]+=1;max_cols=max(max_cols,len(fields))
    profiles=[]
    for col in range(1,max_cols+1):
        s=column_stats(rows,col)
        profiles.append(s)
    candidates={c:column_stats(rows,c) for c in ID_CANDIDATE_COLS}
    selected=max(
        ID_CANDIDATE_COLS,
        key=lambda c:(
            candidates[c]["integer"],
            candidates[c]["unique_int"],
            -candidates[c]["duplicates"],
            -candidates[c]["empty"],
            -c,
        )
    )
    ids=[]
    idx=selected-1
    for r in rows:
        if idx<len(r):
            v=to_int(r[idx])
            if v is not None:ids.append(v)
    return {
        "name":path.name,"bytes":path.stat().st_size,"sha":sha256(path),
        "rows":rows,"row_count":len(rows),"field_counts":field_counts,"max_cols":max_cols,
        "profiles":profiles,"candidates":candidates,"selected_id_col":selected,
        "ids":ids,"idset":set(ids),
        "active":path.name.lower() in active_names,
    }

def analyze(data_dir,setup=None):
    config=setup_itemsets(setup)
    active_names={Path(v.replace("\\","/")).name.lower() for v in config.values()}
    files=[analyze_file(p,active_names) for p in sorted(data_dir.glob("itemset*.txt"),key=lambda p:p.name.lower())]
    comparisons=[]
    for i in range(len(files)):
        for j in range(i+1,len(files)):
            a,b=files[i],files[j]
            comparisons.append({
                "a":a["name"],"b":b["name"],
                "a_ids":len(a["idset"]),"b_ids":len(b["idset"]),
                "intersection":len(a["idset"]&b["idset"]),
                "a_only":len(a["idset"]-b["idset"]),
                "b_only":len(b["idset"]-a["idset"]),
                "same_field_shape":a["field_counts"]==b["field_counts"],
            })
    return {"config":config,"files":files,"comparisons":comparisons}

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered itemset structural probe — R1")
    print("No original item names/descriptions/function strings are stored in this report.")
    print("SOURCE_VERSION_HINT|descendant item ID token is column 15 for itemset1 and column 17 for itemset2+")
    for k,v in sorted(r["config"].items()):
        print(f"ITEMSET_CONFIG|{k}|{v}")
    print(f"ITEMSET_FILE_COUNT|{len(r['files'])}")
    for f in r["files"]:
        print(f"FILE|{f['name']}|bytes={f['bytes']}|sha256={f['sha']}|rows={f['row_count']}|max_cols={f['max_cols']}|active={int(f['active'])}|selected_id_col={f['selected_id_col']}")
        for n,c in sorted(f["field_counts"].items()):
            print(f"FIELD_COUNT|{f['name']}|{n}|{c}")
        for c in ID_CANDIDATE_COLS:
            s=f["candidates"][c]
            print(f"ID_CANDIDATE|{f['name']}|col={c}|integer={s['integer']}|text={s['text']}|empty={s['empty']}|missing={s['missing']}|unique={s['unique_int']}|duplicates={s['duplicates']}|min={s['min']}|max={s['max']}|zero={s['zero']}|negative={s['negative']}")
        for s in f["profiles"]:
            print(f"COLUMN_PROFILE|{f['name']}|{s['col']}|integer={s['integer']}|text={s['text']}|empty={s['empty']}|missing={s['missing']}|unique_int={s['unique_int']}")
    for c in r["comparisons"]:
        print(f"FILE_ID_COMPARE|{c['a']}|{c['b']}|a_ids={c['a_ids']}|b_ids={c['b_ids']}|intersection={c['intersection']}|a_only={c['a_only']}|b_only={c['b_only']}|same_field_shape={int(c['same_field_shape'])}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(a.data_dir,a.setup)

if __name__=="__main__":main()
