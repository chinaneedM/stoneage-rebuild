#!/usr/bin/env python3
"""Score cross-file referential coherence among recovered StoneAge gameplay snapshots."""

import argparse,itertools
from pathlib import Path
from tools.stoneage_encount_chain_probe import (
    clean_rows,parse_encount,parse_group,parse_enemy,setup_values
)
from tools.stoneage_enemybase_probe import parse_file as parse_enemybase_file
from tools.stoneage_itemset_schema_probe import SCHEMA as ITEM_SCHEMA,INDEX as ITEM_INDEX,to_int

def base_name(v):
    return Path(v.replace("\\","/")).name.lower() if v else None

def itemset_ids(path):
    ids=set()
    for r in clean_rows(path):
        if len(r)!=len(ITEM_SCHEMA):continue
        v=to_int(r[ITEM_INDEX["id"]])
        if v is not None:ids.add(v)
    return ids

def load(data_dir,setup=None):
    config=setup_values(setup)
    enc_path=next(iter(sorted(data_dir.glob("encount*.txt"),key=lambda p:p.name.lower())),None)
    enc_refs=set()
    if enc_path:
        _,enc,bad,_=parse_encount(enc_path)
        if bad==0:enc_refs={v for r in enc for v in r["groupids"] if v>=0}

    groups={}
    for p in sorted(data_dir.glob("group*.txt"),key=lambda p:p.name.lower()):
        _,rows,bad,_=parse_group(p)
        if bad:continue
        groups[p.name]={
            "ids":{r["id"] for r in rows},
            "enemy_refs":{v for r in rows for v in r["enemyids"] if v>=0},
            "condition_items":{v for r in rows for v in (r["appear_item"],r["notappear_item"]) if v>0},
        }

    enemies={}
    for p in sorted(data_dir.glob("enemy*.txt"),key=lambda p:p.name.lower()):
        if p.name.lower().startswith("enemybase"):continue
        _,rows,bad,_,prefix=parse_enemy(p)
        if bad:continue
        enemies[p.name]={
            "ids":{r["id"] for r in rows},
            "tempnos":{r["tempno"] for r in rows if r["tempno"]>=0},
            "drops":{v for r in rows for v in r["itemids"] if v>0},
            "prefix":prefix,
        }

    bases={}
    for p in sorted(data_dir.glob("enemybase*.txt"),key=lambda p:p.name.lower()):
        rows,_,bad,_,_=parse_enemybase_file(p)
        if bad:continue
        bases[p.name]={"tempnos":{r["TEMPNO"] for r in rows}}

    items={}
    for p in sorted(data_dir.glob("itemset*.txt"),key=lambda p:p.name.lower()):
        ids=itemset_ids(p)
        if ids:items[p.name]={"ids":ids}

    active={
        "group":base_name(config.get("groupfile")),
        "enemy":base_name(config.get("enemyfile")),
        "enemybase":base_name(config.get("enemybasefile")),
        "itemset":next((base_name(config.get(k)) for k in ("itemset6file","itemset5file","itemset4file","itemset3file","itemfile") if config.get(k)),None),
    }
    return config,enc_path,enc_refs,groups,enemies,bases,items,active

def miss(refs,targets):
    return len(refs-targets)

def analyze(data_dir,setup=None):
    config,enc_path,enc_refs,groups,enemies,bases,items,active=load(data_dir,setup)
    group_enc={g:miss(enc_refs,x["ids"]) for g,x in groups.items()}
    group_enemy={(g,e):miss(gx["enemy_refs"],ex["ids"]) for g,gx in groups.items() for e,ex in enemies.items()}
    enemy_base={(e,b):miss(ex["tempnos"],bx["tempnos"]) for e,ex in enemies.items() for b,bx in bases.items()}
    enemy_item={(e,i):miss(ex["drops"],ix["ids"]) for e,ex in enemies.items() for i,ix in items.items()}
    group_item={(g,i):miss(gx["condition_items"],ix["ids"]) for g,gx in groups.items() for i,ix in items.items()}

    tuples=[]
    for g,e,b,i in itertools.product(groups,enemies,bases,items):
        links={
            "enc_group":group_enc[g],
            "group_enemy":group_enemy[(g,e)],
            "enemy_base":enemy_base[(e,b)],
            "enemy_item":enemy_item[(e,i)],
            "group_item":group_item[(g,i)],
        }
        flags=sum([
            int(g.lower()==active["group"]),
            int(e.lower()==active["enemy"]),
            int(b.lower()==active["enemybase"]),
            int(i.lower()==active["itemset"]),
        ])
        tuples.append({
            "group":g,"enemy":e,"enemybase":b,"itemset":i,
            "links":links,"total":sum(links.values()),"active_flags":flags,
        })
    tuples.sort(key=lambda x:(x["total"],-x["active_flags"],x["group"],x["enemy"],x["enemybase"],x["itemset"]))
    return {
        "config":config,"enc_path":enc_path,"enc_refs":enc_refs,"groups":groups,"enemies":enemies,
        "bases":bases,"items":items,"active":active,
        "group_enc":group_enc,"group_enemy":group_enemy,"enemy_base":enemy_base,
        "enemy_item":enemy_item,"group_item":group_item,"tuples":tuples,
    }

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered gameplay snapshot coherence probe — R1")
    print("No original names/descriptions or table rows are stored in this report.")
    print("SCORING|sum of unique foreign-key IDs missing across five links; lower means fewer unresolved references")
    print(f"ENCOUNT_FILE|{r['enc_path'].name if r['enc_path'] else 'NONE'}|group_refs={len(r['enc_refs'])}")
    for k,v in r["active"].items():print(f"ACTIVE_CONFIG|{k}|{v or 'UNKNOWN'}")
    for g,x in sorted(r["groups"].items()):
        print(f"GROUP_SNAPSHOT|{g}|ids={len(x['ids'])}|enemy_refs={len(x['enemy_refs'])}|condition_items={len(x['condition_items'])}|encount_missing={r['group_enc'][g]}")
    for e,x in sorted(r["enemies"].items()):
        print(f"ENEMY_SNAPSHOT|{e}|ids={len(x['ids'])}|tempnos={len(x['tempnos'])}|drops={len(x['drops'])}|text_prefix={x['prefix']}")
    for b,x in sorted(r["bases"].items()):print(f"ENEMYBASE_SNAPSHOT|{b}|tempnos={len(x['tempnos'])}")
    for i,x in sorted(r["items"].items()):print(f"ITEMSET_SNAPSHOT|{i}|ids={len(x['ids'])}")

    for (g,e),n in sorted(r["group_enemy"].items()):print(f"LINK|group_enemy|{g}|{e}|missing={n}")
    for (e,b),n in sorted(r["enemy_base"].items()):print(f"LINK|enemy_enemybase|{e}|{b}|missing={n}")
    for (e,i),n in sorted(r["enemy_item"].items()):print(f"LINK|enemy_itemset|{e}|{i}|missing={n}")
    for (g,i),n in sorted(r["group_item"].items()):print(f"LINK|group_itemset|{g}|{i}|missing={n}")

    for rank,t in enumerate(r["tuples"],1):
        l=t["links"]
        print(f"TUPLE|{rank}|group={t['group']}|enemy={t['enemy']}|enemybase={t['enemybase']}|itemset={t['itemset']}|total_missing={t['total']}|active_flags={t['active_flags']}|enc_group={l['enc_group']}|group_enemy={l['group_enemy']}|enemy_base={l['enemy_base']}|enemy_item={l['enemy_item']}|group_item={l['group_item']}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(a.data_dir,a.setup)

if __name__=="__main__":main()
