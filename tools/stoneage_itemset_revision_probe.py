#!/usr/bin/env python3
"""Classify revision differences between recovered StoneAge itemset snapshots."""

import argparse,collections
from pathlib import Path
from tools.stoneage_itemset_schema_probe import SCHEMA,INDEX,clean_rows,to_int

NUMERIC_DIFF_FIELDS=("damcrushe","maxdmce","magicusemp","imagenumber","type","magicid")
TEXT_DIFF_FIELDS=("effectstring","argument")

TYPE_LABELS={
  0:"fist",1:"axe",2:"club",3:"spear",4:"bow",5:"shield",6:"helm",7:"armour",
  8:"bracelet",9:"music",10:"necklace",11:"ring",12:"belt",13:"earring",14:"nosering",15:"amulet",
  16:"other",17:"boomerang",18:"boundthrow",19:"breakthrow",20:"dish",21:"metal",22:"jewel",
  23:"wares",24:"wbelt",25:"wshield",26:"wshoes",27:"wglove",30:"alchemist",
  31:"pet_head",32:"pet_tooth",33:"pet_claw",34:"pet_breast",35:"pet_back",36:"pet_wing",37:"pet_feet",
}

def load(path):
    rows=clean_rows(path)
    by={}
    for r in rows:
        if len(r)!=94:continue
        iid=to_int(r[INDEX["id"]])
        if iid is not None:by[iid]=r
    return rows,by

def classify(a,b):
    if not a and not b:return "empty_same"
    if not a and b:return "empty_to_value"
    if a and not b:return "value_to_empty"
    na,nb=to_int(a),to_int(b)
    if na is not None and nb is not None:
        if na==nb:return "same_numeric"
        return "numeric_changed"
    if a==b:return "same_text"
    return "text_changed"

def analyze(data_dir):
    a_path=data_dir/"itemset.txt"; b_path=data_dir/"itemset0710.txt"
    a_rows,a=load(a_path);b_rows,b=load(b_path)
    shared=sorted(set(a)&set(b));bonly=sorted(set(b)-set(a))
    transitions={name:collections.Counter() for name in NUMERIC_DIFF_FIELDS+TEXT_DIFF_FIELDS}
    delta_sign={name:collections.Counter() for name in NUMERIC_DIFF_FIELDS}
    delta_range={name:[] for name in NUMERIC_DIFF_FIELDS}
    durability_pair={"a_both_empty":0,"a_equal":0,"a_different":0,"b_both_empty":0,"b_equal":0,"b_different":0}
    for iid in shared:
        ra,rb=a[iid],b[iid]
        for name in transitions:
            va,vb=ra[INDEX[name]].strip(),rb[INDEX[name]].strip()
            transitions[name][classify(va,vb)]+=1
            if name in NUMERIC_DIFF_FIELDS:
                na,nb=to_int(va),to_int(vb)
                if na is not None and nb is not None and na!=nb:
                    d=nb-na
                    delta_sign[name]["positive" if d>0 else "negative"]+=1
                    delta_range[name].append(d)
        for prefix,row in (("a",ra),("b",rb)):
            x=row[INDEX["damcrushe"]].strip();y=row[INDEX["maxdmce"]].strip()
            if not x and not y:durability_pair[prefix+"_both_empty"]+=1
            elif x==y:durability_pair[prefix+"_equal"]+=1
            else:durability_pair[prefix+"_different"]+=1

    type_counts={}
    for label,by in (("itemset.txt",a),("itemset0710.txt",b)):
        c=collections.Counter()
        for r in by.values():
            v=to_int(r[INDEX["type"]])
            if v is not None:c[v]+=1
        type_counts[label]=c
    new_type_counts=collections.Counter()
    for iid in bonly:
        v=to_int(b[iid][INDEX["type"]])
        if v is not None:new_type_counts[v]+=1

    magic_a={to_int(r[INDEX["magicid"]]) for r in a.values() if r[INDEX["magicid"]].strip()}
    magic_b={to_int(r[INDEX["magicid"]]) for r in b.values() if r[INDEX["magicid"]].strip()}
    magic_a.discard(None);magic_b.discard(None)

    return {
      "a_rows":len(a_rows),"b_rows":len(b_rows),"shared":len(shared),"b_only":len(bonly),
      "transitions":transitions,"delta_sign":delta_sign,"delta_range":delta_range,
      "durability_pair":durability_pair,"type_counts":type_counts,"new_type_counts":new_type_counts,
      "magic_added":sorted(magic_b-magic_a),"magic_removed":sorted(magic_a-magic_b),
    }

def emit(data_dir):
    r=analyze(data_dir)
    print("StoneAge recovered itemset revision probe — R1")
    print("No original item names/descriptions/function strings are stored in this report.")
    print(f"ROWS|itemset.txt|{r['a_rows']}")
    print(f"ROWS|itemset0710.txt|{r['b_rows']}")
    print(f"SHARED_IDS|{r['shared']}")
    print(f"ITEMSET0710_ONLY_IDS|{r['b_only']}")
    for fname,c in r["type_counts"].items():
        for v,n in sorted(c.items()):
            print(f"TYPE_VALUE|{fname}|{v}|{TYPE_LABELS.get(v,'unknown')}|{n}")
    for v,n in sorted(r["new_type_counts"].items()):
        print(f"NEW_ID_TYPE_VALUE|{v}|{TYPE_LABELS.get(v,'unknown')}|{n}")
    for name,c in r["transitions"].items():
        for k,n in sorted(c.items()):
            print(f"TRANSITION|{name}|{k}|{n}")
        ds=r["delta_sign"].get(name)
        if ds:
            print(f"DELTA_SIGN|{name}|positive={ds['positive']}|negative={ds['negative']}")
            vals=r["delta_range"][name]
            if vals: print(f"DELTA_RANGE|{name}|min={min(vals)}|max={max(vals)}")
    for k,v in r["durability_pair"].items():print(f"DURABILITY_PAIR|{k}|{v}")
    print(f"MAGIC_ID_ADDED_COUNT|{len(r['magic_added'])}")
    if r["magic_added"]:print("MAGIC_ID_ADDED|"+",".join(map(str,r["magic_added"][:80])))
    print(f"MAGIC_ID_REMOVED_COUNT|{len(r['magic_removed'])}")
    if r["magic_removed"]:print("MAGIC_ID_REMOVED|"+",".join(map(str,r["magic_removed"][:80])))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--data-dir",type=Path,required=True)
    a=ap.parse_args();emit(a.data_dir)

if __name__=="__main__":main()
