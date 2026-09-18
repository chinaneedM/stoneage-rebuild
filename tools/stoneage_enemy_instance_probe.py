#!/usr/bin/env python3
"""Probe recovered StoneAge enemy-instance tables without retaining payload rows."""

import argparse, collections, hashlib
from pathlib import Path

INT_NAMES = [
    "ID","TEMPNO","LV_MIN","LV_MAX","CREATE_MAX","CREATE_MIN","TACTICS","EXP",
    "DUELPOINT","STYLE","PETFLG",
    *[f"ITEM{i}" for i in range(1,11)],
    *[f"ITEMPROB{i}" for i in range(1,11)],
]

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def clean_lines(path):
    for raw in path.read_bytes().splitlines():
        line=raw.strip()
        if not line or line.startswith(b"#"):
            continue
        yield line

def setup_value(path,key):
    if not path or not path.exists():
        return None
    key=key.lower()
    for raw in path.read_bytes().splitlines():
        line=raw.split(b"#",1)[0].strip()
        if b"=" not in line:
            continue
        k,v=line.split(b"=",1)
        if k.decode("ascii","ignore").strip().lower()==key:
            return v.decode("utf-8","replace").strip()
    return None

def to_int(v):
    try:
        return int(v.strip(),10)
    except (ValueError, TypeError):
        return None

def parse_enemy_row(line):
    """Support the common 2-string schema and active 3-string warp-condition extension."""
    fields=line.split(b",")
    candidates=[]
    for string_fields,label in ((2,"common_2char"),(3,"warp_3char")):
        need=string_fields+len(INT_NAMES)
        if len(fields) < need:
            continue
        vals=[to_int(x) for x in fields[string_fields:need]]
        if all(v is not None for v in vals):
            exact=(len(fields)==need)
            candidates.append((exact,string_fields,label,vals))
    if not candidates:
        return None,len(fields),None
    candidates.sort(key=lambda x:(x[0],x[1]), reverse=True)
    _,string_fields,label,vals=candidates[0]
    return dict(zip(INT_NAMES,vals)),len(fields),label

def enemybase_tempnos(path):
    vals=set()
    if not path or not path.exists():
        return vals
    for line in clean_lines(path):
        f=line.split(b",")
        if len(f) < 7:
            continue
        v=to_int(f[6])
        if v is not None:
            vals.add(v)
    return vals

def normalize_levels(lo,hi):
    if lo==0:
        lo=hi
    return min(lo,hi),max(lo,hi)

def parse_file(path,template_tempnos=frozenset()):
    rows=[]; field_counts=collections.Counter(); schema=collections.Counter()
    malformed=0
    for line in clean_lines(path):
        row,n,label=parse_enemy_row(line)
        field_counts[n]+=1
        if row is None:
            malformed+=1
            continue
        schema[label]+=1
        rows.append(row)

    ids=[r["ID"] for r in rows]
    id_counts=collections.Counter(ids)
    missing_temp=sum(1 for r in rows if template_tempnos and r["TEMPNO"] not in template_tempnos)
    zero_min=0; reversed_levels=0; normalized=[]
    for r in rows:
        if r["LV_MIN"]==0:
            zero_min+=1
        if r["LV_MIN"]!=0 and r["LV_MIN"]>r["LV_MAX"]:
            reversed_levels+=1
        normalized.append(normalize_levels(r["LV_MIN"],r["LV_MAX"]))

    return {
        "rows":rows,
        "field_counts":field_counts,
        "schema_counts":schema,
        "malformed":malformed,
        "duplicate_id_values":sum(1 for _,n in id_counts.items() if n>1),
        "duplicate_id_rows":sum(n-1 for n in id_counts.values() if n>1),
        "missing_temp":missing_temp,
        "zero_min":zero_min,
        "reversed_levels":reversed_levels,
        "normalized":normalized,
    }

def stat(rows,name):
    vals=[r[name] for r in rows]
    if not vals:
        return None,None,0
    return min(vals),max(vals),len(set(vals))

def dist(rows,name):
    return collections.Counter(r[name] for r in rows)

def analyze(data_dir,setup=None):
    active_enemy=setup_value(setup,"enemyfile")
    active_base=setup_value(setup,"enemybasefile")
    base_name=Path(active_base.replace("\\","/")).name if active_base else "enemybase.txt"
    base_path=data_dir/base_name
    tempnos=enemybase_tempnos(base_path)
    files=sorted(data_dir.glob("enemy*.txt"),key=lambda p:p.name.lower())
    files=[p for p in files if not p.name.lower().startswith("enemybase")]
    out=[]
    for p in files:
        d=parse_file(p,tempnos)
        d.update({
            "name":p.name,
            "bytes":p.stat().st_size,
            "sha":sha256(p),
            "active":bool(active_enemy and Path(active_enemy.replace("\\","/")).name.lower()==p.name.lower()),
        })
        out.append(d)
    return active_enemy,active_base,len(tempnos),out

def emit(data_dir,setup=None):
    active_enemy,active_base,temp_count,files=analyze(data_dir,setup)
    print("StoneAge recovered enemy-instance probe — R1")
    print("No enemy names, tactics strings, item IDs, or original table rows are stored in this report.")
    print("SCHEMA_SOURCE|descendant_ENEMY_2_or_3_char_fields_plus_31_int_fields")
    print(f"ACTIVE_ENEMY_CONFIG|{active_enemy or 'UNKNOWN'}")
    print(f"ACTIVE_ENEMYBASE_CONFIG|{active_base or 'UNKNOWN'}")
    print(f"ACTIVE_TEMPLATE_TEMPNO_COUNT|{temp_count}")
    print(f"ENEMY_FILE_COUNT|{len(files)}")
    for f in files:
        rows=f["rows"]
        print(f"FILE|{f['name']}|bytes={f['bytes']}|sha256={f['sha']}|valid_rows={len(rows)}|malformed={f['malformed']}|active={int(f['active'])}")
        for n,c in sorted(f["field_counts"].items()):
            print(f"FIELD_COUNT|{f['name']}|{n}|{c}")
        for name,c in sorted(f["schema_counts"].items()):
            print(f"SCHEMA_ROWS|{f['name']}|{name}|{c}")
        for name in ("ID","TEMPNO","LV_MIN","LV_MAX","CREATE_MAX","CREATE_MIN","TACTICS","EXP","DUELPOINT","STYLE","PETFLG"):
            lo,hi,uniq=stat(rows,name)
            if lo is not None:
                print(f"STAT|{f['name']}|{name}|min={lo}|max={hi}|unique={uniq}")
        print(f"DUPLICATE_ID_VALUES|{f['name']}|{f['duplicate_id_values']}")
        print(f"DUPLICATE_ID_EXTRA_ROWS|{f['name']}|{f['duplicate_id_rows']}")
        print(f"UNRESOLVED_TEMPNO|{f['name']}|{f['missing_temp']}")
        print(f"LEVEL_ZERO_MIN_ROWS|{f['name']}|{f['zero_min']}")
        print(f"LEVEL_REVERSED_NONZERO_ROWS|{f['name']}|{f['reversed_levels']}")
        if f["normalized"]:
            print(f"NORMALIZED_LEVEL_RANGE|{f['name']}|min={min(x[0] for x in f['normalized'])}|max={max(x[1] for x in f['normalized'])}")
        for name in ("PETFLG","STYLE","TACTICS"):
            for value,count in sorted(dist(rows,name).items()):
                print(f"DIST|{f['name']}|{name}|{value}|{count}")
        exp=dist(rows,"EXP")
        print(f"EXP_SENTINEL_MINUS1|{f['name']}|{exp.get(-1,0)}")
        print(f"EXP_ZERO|{f['name']}|{exp.get(0,0)}")
        print(f"EXP_POSITIVE|{f['name']}|{sum(n for v,n in exp.items() if v>0)}")
        for i in range(1,11):
            item=f"ITEM{i}"; prob=f"ITEMPROB{i}"
            populated=sum(1 for r in rows if r[item]>0)
            prob_nonzero=sum(1 for r in rows if r[prob]!=0)
            prob_outside_0_1000=sum(1 for r in rows if r[prob]<0 or r[prob]>1000)
            print(f"DROP_SLOT|{f['name']}|{i}|item_positive={populated}|prob_nonzero={prob_nonzero}|prob_outside_0_1000={prob_outside_0_1000}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args()
    emit(a.data_dir,a.setup)

if __name__=="__main__":
    main()
