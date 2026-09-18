#!/usr/bin/env python3
"""Analyze recovered StoneAge enemybase pet-template tables using the stable descendant prefix schema."""

import argparse,collections,hashlib\nfrom decimal import Decimal,InvalidOperation
from pathlib import Path

CHAR_FIELDS=6
INT_NAMES=[
"TEMPNO","INITNUM","LVUPPOINT","BASEVITAL","BASESTR","BASETGH","BASEDEX",
"MODAI","GET","EARTHAT","WATERAT","FIREAT","WINDAT","POISON","PARALYSIS",
"SLEEP","STONE","DRUNK","CONFUSION","PETSKILL1","PETSKILL2","PETSKILL3",
"PETSKILL4","PETSKILL5","PETSKILL6","PETSKILL7","RARE","CRITICAL","COUNTER",
"SLOT","IMGNUMBER","PETFLG","SIZE"
]
INDEX={name:CHAR_FIELDS+i for i,name in enumerate(INT_NAMES)}

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

def to_decimal(v):
    try:return Decimal(v.strip().decode("ascii"))
    except (InvalidOperation,UnicodeDecodeError):return None

def parse_file(path):
    rows=[]; field_counts=collections.Counter(); malformed=0; raw_rows=[]
    max_cols=0
    for line in clean_lines(path):
        fields=line.split(b","); raw_rows.append(fields)
        field_counts[len(fields)]+=1; max_cols=max(max_cols,len(fields))
        if len(fields)<CHAR_FIELDS+len(INT_NAMES):
            malformed+=1; continue
        vals={name:to_int(fields[idx]) for name,idx in INDEX.items()}
        vals["LVUPPOINT"]=to_decimal(fields[INDEX["LVUPPOINT"]])
        if any(v is None for v in vals.values()):
            malformed+=1; continue
        rows.append(vals)
    profiles=[]
    for idx in range(max_cols):
        integer=decimal=empty=text=missing=0
        for fields in raw_rows:
            if idx>=len(fields): missing+=1; continue
            v=fields[idx].strip()
            if not v: empty+=1
            elif to_int(v) is not None: integer+=1
            elif to_decimal(v) is not None: decimal+=1
            else: text+=1
        profiles.append((idx+1,integer,decimal,empty,text,missing))
    return rows,field_counts,malformed,raw_rows,profiles

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

def stat(rows,name):
    vals=[r[name] for r in rows]
    return (min(vals),max(vals),len(set(vals))) if vals else (None,None,0)

def analyze(data_dir,setup=None):
    active=setup_value(setup,"enemybasefile")
    files=sorted(data_dir.glob("enemybase*.txt"),key=lambda p:p.name.lower())
    out=[]
    for p in files:
        rows,fc,bad,raw_rows,profiles=parse_file(p)
        skills=collections.Counter()
        for r in rows:
            for n in ("PETSKILL1","PETSKILL2","PETSKILL3","PETSKILL4","PETSKILL5","PETSKILL6","PETSKILL7"):
                if r[n]>0:skills[r[n]]+=1
        elem_sums=collections.Counter(r["EARTHAT"]+r["WATERAT"]+r["FIREAT"]+r["WINDAT"] for r in rows)
        out.append({
            "name":p.name,"sha":sha256(p),"bytes":p.stat().st_size,"rows":rows,
            "field_counts":fc,"malformed":bad,"raw_row_count":len(raw_rows),"profiles":profiles,
            "skills":skills,"elem_sums":elem_sums,
            "active": bool(active and Path(active.replace("\\","/")).name.lower()==p.name.lower())
        })
    return active,out

def emit(data_dir,setup=None):
    active,files=analyze(data_dir,setup)
    print("StoneAge recovered pet-template probe — R1")
    print("No pet names or original table rows are stored in this report.")
    print("SCHEMA_SOURCE|descendant_ENEMYTEMP_prefix_6_char_fields_plus_33_int_fields")
    print(f"ACTIVE_ENEMYBASE_CONFIG|{active or 'UNKNOWN'}")
    print(f"ENEMYBASE_FILE_COUNT|{len(files)}")
    for f in files:
        rows=f["rows"]
        print(f"FILE|{f['name']}|bytes={f['bytes']}|sha256={f['sha']}|rows={f['raw_row_count']}|descendant_prefix_compatible={len(rows)}|active={int(f['active'])}")
        for n,c in sorted(f["field_counts"].items()):
            print(f"FIELD_COUNT|{f['name']}|{n}|{c}")
        numeric_cols=[]; text_cols=[]
        for col,integer,decimal,empty,text,missing in f["profiles"]:
            total=integer+decimal+empty+text+missing
            if total and integer+decimal==total: numeric_cols.append(col)
            if text: text_cols.append(col)
            print(f"COLUMN_PROFILE|{f['name']}|{col}|integer={integer}|decimal={decimal}|empty={empty}|text={text}|missing={missing}")
        print(f"ALL_INTEGER_COLUMNS|{f['name']}|"+",".join(map(str,numeric_cols)))
        print(f"TEXT_PRESENT_COLUMNS|{f['name']}|"+",".join(map(str,text_cols)))
        for name in ("TEMPNO","INITNUM","LVUPPOINT","BASEVITAL","BASESTR","BASETGH","BASEDEX","MODAI","GET","EARTHAT","WATERAT","FIREAT","WINDAT","RARE","CRITICAL","COUNTER","SLOT","IMGNUMBER","PETFLG","SIZE"):
            lo,hi,uniq=stat(rows,name)
            if lo is not None: print(f"STAT|{f['name']}|{name}|min={lo}|max={hi}|unique={uniq}")
        print(f"UNIQUE_PETSKILL_IDS|{f['name']}|{len(f['skills'])}")
        for v,n in f["skills"].most_common(15):
            print(f"PETSKILL_USAGE|{f['name']}|{v}|{n}")
        for total,n in sorted(f["elem_sums"].items()):
            print(f"ELEMENT_SUM|{f['name']}|{total}|{n}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args(); emit(a.data_dir,a.setup)
if __name__=="__main__":main()
