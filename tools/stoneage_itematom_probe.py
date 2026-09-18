#!/usr/bin/env python3
"""Validate recovered StoneAge item-atom references from itemset and enemybase snapshots."""

import argparse,collections,hashlib
from pathlib import Path
from tools.stoneage_encount_chain_probe import clean_rows,setup_values
from tools.stoneage_itemset_schema_probe import SCHEMA as ITEM_SCHEMA,INDEX as ITEM_INDEX,to_int

ATOM_COLS=2
ING_NAMES=[f"ingname{i}" for i in range(5)]
ING_VALUES=[f"ingvalue{i}" for i in range(5)]

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def parse_atoms(path):
    rows=clean_rows(path);names=[];flags=[];bad=0;widths=collections.Counter(map(len,rows))
    for r in rows:
        if len(r)!=2:
            bad+=1;continue
        name=r[0].strip()
        try:flag=int(r[1].strip() or b"0",10)
        except ValueError:
            bad+=1;continue
        if flag not in (0,1):
            bad+=1;continue
        names.append(name);flags.append(flag)
    return rows,names,flags,bad,widths

def parse_itemset_atoms(path,atomset):
    rows=clean_rows(path)
    total_refs=0;refs=set();missing=set();recipe_items=0;values=[]
    bad_width=0;missing_value=0
    for r in rows:
        if len(r)!=len(ITEM_SCHEMA):
            bad_width+=1;continue
        used=False
        for n,vn in zip(ING_NAMES,ING_VALUES):
            name=r[ITEM_INDEX[n]].strip()
            val=r[ITEM_INDEX[vn]].strip()
            if not name:continue
            used=True;total_refs+=1;refs.add(name)
            if name not in atomset:missing.add(name)
            iv=to_int(val)
            if iv is None:missing_value+=1
            else:values.append(iv)
        if used:recipe_items+=1
    return {
        "rows":len(rows),"bad_width":bad_width,"recipe_items":recipe_items,
        "total_refs":total_refs,"refs":refs,"missing":missing,
        "values":values,"missing_value":missing_value,
    }

def parse_enemybase_atoms(path,atomset):
    rows=clean_rows(path)
    refs=set();total_refs=0;missing=set();templates=0;bad=0
    for r in rows:
        if len(r)<6:
            bad+=1;continue
        used=False
        for v in r[1:6]:
            name=v.strip()
            if not name:continue
            used=True;total_refs+=1;refs.add(name)
            if name not in atomset:missing.add(name)
        if used:templates+=1
    return {
        "rows":len(rows),"bad":bad,"templates":templates,"total_refs":total_refs,
        "refs":refs,"missing":missing,
    }

def active_name(config,keys):
    for k in keys:
        if config.get(k):return Path(config[k].replace("\\","/")).name.lower()
    return None

def analyze(data_dir,setup=None):
    config=setup_values(setup)
    atom_cfg=config.get("itematomfile")
    atom_path=data_dir/Path(atom_cfg.replace("\\","/")).name if atom_cfg else data_dir/"itematom.txt"
    if not atom_path.exists():
        return {"exists":False,"config":config}
    raw,names,flags,bad,widths=parse_atoms(atom_path)
    atomset=set(names)
    active_item=active_name(config,("itemset6file","itemset5file","itemset4file","itemset3file","itemfile"))
    active_base=active_name(config,("enemybasefile",))
    itemsets={}
    for p in sorted(data_dir.glob("itemset*.txt"),key=lambda p:p.name.lower()):
        itemsets[p.name]=parse_itemset_atoms(p,atomset)
        itemsets[p.name]["active"]=p.name.lower()==active_item
    bases={}
    for p in sorted(data_dir.glob("enemybase*.txt"),key=lambda p:p.name.lower()):
        bases[p.name]=parse_enemybase_atoms(p,atomset)
        bases[p.name]["active"]=p.name.lower()==active_base
    flag_counts=collections.Counter(flags)
    return {
        "exists":True,"config":config,"atom_path":atom_path,"raw_count":len(raw),
        "names":names,"atomset":atomset,"flags":flags,"flag_counts":flag_counts,
        "bad":bad,"widths":widths,"duplicate_names":len(names)-len(atomset),
        "itemsets":itemsets,"bases":bases,
    }

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered item-atom probe — R1")
    print("No original atom/item/pet names or source rows are stored in this report.")
    print("SCHEMA_SOURCE|descendant_ITEM_initItemAtom_ITEM_initItemIngCache_ITEM_merge_getPetFix")
    print("ATOM_SCHEMA|name + magicflg")
    print("ITEMSET_LINK|itemset.ingname0..4 -> itematom.name")
    print("ENEMYBASE_LINK|enemybase.atomfixname1..5 -> itematom.name")
    if not r["exists"]:
        print("ITEMATOM_FILE_EXISTS|0");return
    print("ITEMATOM_FILE_EXISTS|1")
    print(f"FILE|{r['atom_path'].name}|bytes={r['atom_path'].stat().st_size}|sha256={sha256(r['atom_path'])}|rows={r['raw_count']}|malformed={r['bad']}|unique_names={len(r['atomset'])}|duplicate_names={r['duplicate_names']}")
    for n,c in sorted(r["widths"].items()):print(f"FIELD_COUNT|{n}|{c}")
    for v,n in sorted(r["flag_counts"].items()):print(f"MAGICFLG_VALUE|{v}|{n}")
    for name,x in sorted(r["itemsets"].items()):
        vals=x["values"]
        print(f"ITEMSET_ATOM_COVERAGE|{name}|active={int(x['active'])}|rows={x['rows']}|bad_width={x['bad_width']}|recipe_items={x['recipe_items']}|slot_refs={x['total_refs']}|unique_refs={len(x['refs'])}|matched={len(x['refs'])-len(x['missing'])}|missing={len(x['missing'])}|missing_values={x['missing_value']}")
        if vals:print(f"ITEMSET_INGVALUE_STAT|{name}|min={min(vals)}|max={max(vals)}|unique={len(set(vals))}")
    for name,x in sorted(r["bases"].items()):
        print(f"ENEMYBASE_ATOM_COVERAGE|{name}|active={int(x['active'])}|rows={x['rows']}|malformed={x['bad']}|templates_with_atoms={x['templates']}|slot_refs={x['total_refs']}|unique_refs={len(x['refs'])}|matched={len(x['refs'])-len(x['missing'])}|missing={len(x['missing'])}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(a.data_dir,a.setup)

if __name__=="__main__":main()
