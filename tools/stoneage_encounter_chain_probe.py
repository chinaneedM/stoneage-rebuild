#!/usr/bin/env python3
"""Probe recovered StoneAge group/encount server tables without retaining rows."""

import argparse,collections,hashlib
from pathlib import Path

GROUP_INT_NAMES=["GROUP_ID","APPEAR_ITEM","NOT_APPEAR_ITEM",
                 *[f"ENEMY_ID{i}" for i in range(1,11)],
                 *[f"CREATE_PROB{i}" for i in range(1,11)]]
ENCOUNT_BASE_NAMES=["INDEX","FLOOR","X1","Y1","X2","Y2","PROB_MIN","PROB_MAX","ENEMY_MAX","ZORDER",
                    *[f"GROUP_ID{i}" for i in range(1,11)],
                    *[f"GROUP_PROB{i}" for i in range(1,11)]]
ENCOUNT_EXT_NAMES=["EVENT_NOW","EVENT_END","EVENT_ENEMY_GROUP"]

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

def c_atoi(v):
    s=(v.decode("ascii","ignore") if isinstance(v,(bytes,bytearray)) else str(v)).lstrip()
    if not s:return 0
    sign=1
    if s[0] in "+-":
        if s[0]=="-":sign=-1
        s=s[1:]
    d=[]
    for ch in s:
        if not ch.isdigit():break
        d.append(ch)
    return sign*int("".join(d)) if d else 0

def setup_value(path,key):
    if not path or not path.exists():return None
    key=key.lower()
    for raw in path.read_bytes().splitlines():
        line=raw.split(b"#",1)[0].strip()
        if b"=" not in line:continue
        k,v=line.split(b"=",1)
        if k.decode("ascii","ignore").strip().lower()==key:
            return v.decode("utf-8","replace").strip()
    return None

def active_path(data_dir,configured,default):
    name=Path(configured.replace("\\","/")).name if configured else default
    return data_dir/name

def parse_enemy_ids(path):
    ids=set()
    if not path.exists():return ids
    for line in clean_lines(path):
        f=line.split(b",")
        # Active 2.5 schema is 3 strings + ints; fallback common schema is 2.
        if len(f)>=34:ids.add(c_atoi(f[3]))
        elif len(f)>=33:ids.add(c_atoi(f[2]))
    return ids

def parse_group_file(path,enemy_ids):
    rows=[];fc=collections.Counter();bad=0
    for line in clean_lines(path):
        f=line.split(b",");fc[len(f)]+=1
        if len(f)<1+len(GROUP_INT_NAMES):
            bad+=1;continue
        vals=[]
        for token in f[1:1+len(GROUP_INT_NAMES)]:
            vals.append(-1 if token.strip()==b"" else c_atoi(token))
        row=dict(zip(GROUP_INT_NAMES,vals))
        eids=[row[f"ENEMY_ID{i}"] for i in range(1,11) if row[f"ENEMY_ID{i}"]!=-1]
        row["_enemy_refs"]=eids
        row["_unresolved"]=sum(1 for v in eids if v not in enemy_ids)
        row["_duplicate_enemy_ids"]=len(eids)-len(set(eids))
        rows.append(row)
    return rows,fc,bad

def parse_encount_file(path,group_ids):
    rows=[];fc=collections.Counter();schema=collections.Counter();bad=0
    for line in clean_lines(path):
        f=line.split(b",");fc[len(f)]+=1
        if len(f)<30:
            bad+=1;continue
        vals=[]
        for i,name in enumerate(ENCOUNT_BASE_NAMES):
            token=f[i]
            if i>=10 and token.strip()==b"":
                vals.append(-1)
            else:
                vals.append(c_atoi(token))
        row=dict(zip(ENCOUNT_BASE_NAMES,vals))
        if len(f)>=33:
            row.update(dict(zip(ENCOUNT_EXT_NAMES,[c_atoi(x) for x in f[30:33]])))
            schema["extended_33"]+=1
        else:
            schema["base_30"]+=1
        gids=[row[f"GROUP_ID{i}"] for i in range(1,11) if row[f"GROUP_ID{i}"]!=-1]
        row["_group_refs"]=gids
        row["_unresolved"]=sum(1 for v in gids if v not in group_ids)
        row["_duplicate_group_ids"]=len(gids)-len(set(gids))
        row["_reversed_prob"]=row["PROB_MIN"]>row["PROB_MAX"]
        row["_rect_width"]=abs(row["X2"]-row["X1"])
        row["_rect_height"]=abs(row["Y2"]-row["Y1"])
        rows.append(row)
    return rows,fc,schema,bad

def stat(rows,name):
    vals=[r[name] for r in rows]
    return (min(vals),max(vals),len(set(vals))) if vals else (None,None,0)

def analyze(data_dir,setup=None):
    enemy_cfg=setup_value(setup,"enemyfile")
    group_cfg=setup_value(setup,"groupfile")
    enc_cfg=setup_value(setup,"encountfile")
    enemy_ids=parse_enemy_ids(active_path(data_dir,enemy_cfg,"enemy.txt"))

    groups=[]
    for p in sorted(data_dir.glob("group*.txt"),key=lambda p:p.name.lower()):
        rows,fc,bad=parse_group_file(p,enemy_ids)
        groups.append({"name":p.name,"rows":rows,"field_counts":fc,"bad":bad,
                       "sha":sha256(p),"bytes":p.stat().st_size,
                       "active":bool(group_cfg and Path(group_cfg.replace("\\","/")).name.lower()==p.name.lower())})
    active_group=next((g for g in groups if g["active"]),None)
    group_ids=set(r["GROUP_ID"] for r in active_group["rows"]) if active_group else set()

    ep=active_path(data_dir,enc_cfg,"encount.txt")
    enc=None
    if ep.exists():
        rows,fc,schemas,bad=parse_encount_file(ep,group_ids)
        enc={"name":ep.name,"rows":rows,"field_counts":fc,"schemas":schemas,"bad":bad,
             "sha":sha256(ep),"bytes":ep.stat().st_size}
    return enemy_cfg,group_cfg,enc_cfg,len(enemy_ids),groups,enc

def emit(data_dir,setup=None):
    enemy_cfg,group_cfg,enc_cfg,enemy_count,groups,enc=analyze(data_dir,setup)
    print("StoneAge recovered encounter-chain probe — R1")
    print("No group names, item IDs, enemy IDs, group IDs, or original rows are stored in this report.")
    print(f"ACTIVE_ENEMY_CONFIG|{enemy_cfg or 'UNKNOWN'}")
    print(f"ACTIVE_GROUP_CONFIG|{group_cfg or 'UNKNOWN'}")
    print(f"ACTIVE_ENCOUNT_CONFIG|{enc_cfg or 'UNKNOWN'}")
    print(f"ACTIVE_ENEMY_ID_COUNT|{enemy_count}")
    print(f"GROUP_FILE_COUNT|{len(groups)}")
    for g in groups:
        rows=g["rows"]
        print(f"GROUP_FILE|{g['name']}|bytes={g['bytes']}|sha256={g['sha']}|valid_rows={len(rows)}|malformed={g['bad']}|active={int(g['active'])}")
        for n,c in sorted(g["field_counts"].items()):print(f"GROUP_FIELD_COUNT|{g['name']}|{n}|{c}")
        lo,hi,uq=stat(rows,"GROUP_ID")
        if lo is not None:print(f"GROUP_ID_STAT|{g['name']}|min={lo}|max={hi}|unique={uq}")
        print(f"GROUP_UNRESOLVED_ENEMY_REFS|{g['name']}|{sum(r['_unresolved'] for r in rows)}")
        print(f"GROUP_DUPLICATE_ENEMY_REF_ROWS|{g['name']}|{sum(1 for r in rows if r['_duplicate_enemy_ids']>0)}")
        print(f"GROUP_WITH_APPEAR_ITEM_GATE|{g['name']}|{sum(1 for r in rows if r['APPEAR_ITEM']!=-1)}")
        print(f"GROUP_WITH_NOT_APPEAR_ITEM_GATE|{g['name']}|{sum(1 for r in rows if r['NOT_APPEAR_ITEM']!=-1)}")
        for i in range(1,11):
            print(f"GROUP_SLOT|{g['name']}|{i}|enemy_present={sum(1 for r in rows if r[f'ENEMY_ID{i}']!=-1)}|weight_present={sum(1 for r in rows if r[f'CREATE_PROB{i}']!=-1)}")
    if enc:
        rows=enc["rows"]
        print(f"ENCOUNT_FILE|{enc['name']}|bytes={enc['bytes']}|sha256={enc['sha']}|valid_rows={len(rows)}|malformed={enc['bad']}")
        for n,c in sorted(enc["field_counts"].items()):print(f"ENCOUNT_FIELD_COUNT|{n}|{c}")
        for n,c in sorted(enc["schemas"].items()):print(f"ENCOUNT_SCHEMA_ROWS|{n}|{c}")
        for name in ("INDEX","FLOOR","PROB_MIN","PROB_MAX","ENEMY_MAX","ZORDER"):
            lo,hi,uq=stat(rows,name)
            if lo is not None:print(f"ENCOUNT_STAT|{name}|min={lo}|max={hi}|unique={uq}")
        print(f"ENCOUNT_UNRESOLVED_GROUP_REFS|{sum(r['_unresolved'] for r in rows)}")
        print(f"ENCOUNT_DUPLICATE_GROUP_REF_ROWS|{sum(1 for r in rows if r['_duplicate_group_ids']>0)}")
        print(f"ENCOUNT_REVERSED_PROB_ROWS|{sum(1 for r in rows if r['_reversed_prob'])}")
        print(f"ENCOUNT_INVALID_ENEMY_MAX_ROWS|{sum(1 for r in rows if r['ENEMY_MAX']<1 or r['ENEMY_MAX']>10)}")
        print(f"ENCOUNT_NONPOSITIVE_ZORDER_ROWS|{sum(1 for r in rows if r['ZORDER']<=0)}")
        if rows:
            print(f"ENCOUNT_RECT_WIDTH|max={max(r['_rect_width'] for r in rows)}")
            print(f"ENCOUNT_RECT_HEIGHT|max={max(r['_rect_height'] for r in rows)}")
        for i in range(1,11):
            print(f"ENCOUNT_GROUP_SLOT|{i}|group_present={sum(1 for r in rows if r[f'GROUP_ID{i}']!=-1)}|weight_present={sum(1 for r in rows if r[f'GROUP_PROB{i}']!=-1)}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(a.data_dir,a.setup)
if __name__=="__main__":main()
