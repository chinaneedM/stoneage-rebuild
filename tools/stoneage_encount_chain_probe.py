#!/usr/bin/env python3
"""Validate the recovered StoneAge encounter -> group -> enemy -> template/item chain."""

import argparse,collections,hashlib
from pathlib import Path
from tools.stoneage_enemybase_probe import analyze as analyze_enemybase
from tools.stoneage_itemset_schema_probe import SCHEMA as ITEM_SCHEMA, INDEX as ITEM_INDEX, to_int as item_to_int

ENCOUNT_COLS=33
GROUP_COLS=24
ENEMY_INT_COUNT=31

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def clean_rows(path):
    rows=[]
    for raw in path.read_bytes().splitlines():
        line=raw.strip()
        if not line or line.startswith(b"#"): continue
        rows.append([x.strip() for x in line.replace(b"\t",b" ").split(b",")])
    return rows

def atoi0(v):
    try:return int(v.strip() or b"0",10)
    except ValueError:return None

def optint(v):
    if not v.strip(): return -1
    try:return int(v.strip(),10)
    except ValueError:return None

def setup_values(path):
    out={}
    if not path or not path.exists(): return out
    for raw in path.read_bytes().splitlines():
        line=raw.split(b"#",1)[0].strip()
        if b"=" not in line: continue
        k,v=line.split(b"=",1)
        out[k.decode("ascii","ignore").strip().lower()]=v.decode("utf-8","replace").strip()
    return out

def configured_file(data_dir,config,key,patterns):
    val=config.get(key)
    if val:
        p=data_dir/Path(val.replace("\\","/")).name
        if p.exists(): return p
    found=[]
    for pat in patterns: found.extend(data_dir.glob(pat))
    return sorted(set(found),key=lambda p:p.name.lower())[0] if found else None

def parse_encount(path):
    rows=clean_rows(path); parsed=[]; bad=0; widths=collections.Counter(map(len,rows))
    for r in rows:
        if len(r)!=ENCOUNT_COLS:
            bad+=1; continue
        vals=[]
        ok=True
        for i,v in enumerate(r):
            n=optint(v) if 10<=i<30 else atoi0(v)
            if n is None: ok=False; break
            vals.append(n)
        if not ok:
            bad+=1; continue
        parsed.append({
            "index":vals[0],"floor":vals[1],"x1":vals[2],"y1":vals[3],"x2":vals[4],"y2":vals[5],
            "pmin":min(vals[6],vals[7]),"pmax":max(vals[6],vals[7]),
            "enemymax":vals[8],"zorder":vals[9],
            "groupids":vals[10:20],"groupprobs":vals[20:30],
            "event_now":vals[30],"event_end":vals[31],"enemy_group":vals[32],
        })
    return rows,parsed,bad,widths

def parse_group(path):
    rows=clean_rows(path); parsed=[]; bad=0; widths=collections.Counter(map(len,rows))
    for r in rows:
        if len(r)!=GROUP_COLS:
            bad+=1; continue
        nums=[];ok=True
        for v in r[1:]:
            n=optint(v)
            if n is None:ok=False;break
            nums.append(n)
        if not ok:
            bad+=1;continue
        parsed.append({
            "id":nums[0],"appear_item":nums[1],"notappear_item":nums[2],
            "enemyids":nums[3:13],"enemyprobs":nums[13:23],
        })
    return rows,parsed,bad,widths

def choose_enemy_prefix(rows):
    counts=collections.Counter(len(r) for r in rows)
    score2=counts[2+ENEMY_INT_COUNT]
    score3=counts[3+ENEMY_INT_COUNT]
    return 3 if score3>score2 else 2

def parse_enemy(path):
    rows=clean_rows(path); prefix=choose_enemy_prefix(rows); expected=prefix+ENEMY_INT_COUNT
    parsed=[];bad=0;widths=collections.Counter(map(len,rows))
    for r in rows:
        if len(r)!=expected:
            bad+=1;continue
        nums=[];ok=True
        for v in r[prefix:]:
            n=atoi0(v)
            if n is None:ok=False;break
            nums.append(n)
        if not ok:
            bad+=1;continue
        parsed.append({
            "id":nums[0],"tempno":nums[1],"lv_min":nums[2],"lv_max":nums[3],
            "create_max":nums[4],"create_min":nums[5],"tactics":nums[6],"exp":nums[7],
            "duelpoint":nums[8],"style":nums[9],"petflg":nums[10],
            "itemids":nums[11:21],"itemprobs":nums[21:31],
        })
    return rows,parsed,bad,widths,prefix

def active_enemybase_tempnos(data_dir,setup):
    active,files=analyze_enemybase(data_dir,setup)
    chosen=next((f for f in files if f["active"]),files[0] if files else None)
    return active,chosen["name"] if chosen else None,{r["TEMPNO"] for r in chosen["rows"]} if chosen else set()

def active_item_ids(data_dir,config):
    names=[]
    for key in ("itemset6file","itemset5file","itemset4file","itemset3file","itemfile"):
        val=config.get(key)
        if val:names.append(Path(val.replace("\\","/")).name)
    p=next((data_dir/n for n in names if (data_dir/n).exists()),None)
    if p is None:
        p=data_dir/"itemset.txt"
        if not p.exists():return None,set()
    ids=set()
    for r in clean_rows(p):
        if len(r)!=len(ITEM_SCHEMA):continue
        v=item_to_int(r[ITEM_INDEX["id"]])
        if v is not None:ids.add(v)
    return p.name,ids

def stats(vals):
    vals=list(vals)
    return (min(vals),max(vals),len(set(vals))) if vals else (None,None,0)

def analyze(data_dir,setup=None):
    config=setup_values(setup)
    ep=configured_file(data_dir,config,"encountfile",["encount*.txt"])
    gp=configured_file(data_dir,config,"groupfile",["group*.txt"])
    xp=configured_file(data_dir,config,"enemyfile",["enemy*.txt"])
    eb_cfg,eb_name,eb_tempnos=active_enemybase_tempnos(data_dir,setup)
    item_name,item_ids=active_item_ids(data_dir,config)
    if not ep or not gp or not xp:
        return {"config":config,"missing":[k for k,p in (("encount",ep),("group",gp),("enemy",xp)) if p is None]}

    eraw,enc,bad_e,w_e=parse_encount(ep)
    graw,groups,bad_g,w_g=parse_group(gp)
    xraw,enemies,bad_x,w_x,prefix=parse_enemy(xp)

    group_ids=[r["id"] for r in groups]
    group_set=set(group_ids)
    enc_group_refs=[v for r in enc for v in r["groupids"] if v>=0]
    enc_group_set=set(enc_group_refs)

    enemy_ids=[r["id"] for r in enemies]
    enemy_set=set(enemy_ids)
    group_enemy_refs=[v for r in groups for v in r["enemyids"] if v>=0]
    group_enemy_set=set(group_enemy_refs)

    temp_refs=[r["tempno"] for r in enemies if r["tempno"]>=0]
    temp_set=set(temp_refs)

    drop_refs=[v for r in enemies for v in r["itemids"] if v>0]
    drop_set=set(drop_refs)
    cond_refs=[v for r in groups for v in (r["appear_item"],r["notappear_item"]) if v>0]
    cond_set=set(cond_refs)

    floors=[r["floor"] for r in enc]
    pmins=[r["pmin"] for r in enc];pmaxs=[r["pmax"] for r in enc]
    z=[r["zorder"] for r in enc];enemymax=[r["enemymax"] for r in enc]
    group_prob_sums=[sum(max(0,v) for v in r["groupprobs"]) for r in enc]
    enemy_prob_sums=[sum(max(0,v) for v in r["enemyprobs"]) for r in groups]

    return {
        "config":config,"missing":[],
        "enc_path":ep,"group_path":gp,"enemy_path":xp,"enemybase_cfg":eb_cfg,"enemybase_name":eb_name,
        "item_name":item_name,
        "enc_raw":len(eraw),"enc":enc,"enc_bad":bad_e,"enc_widths":w_e,
        "group_raw":len(graw),"groups":groups,"group_bad":bad_g,"group_widths":w_g,
        "enemy_raw":len(xraw),"enemies":enemies,"enemy_bad":bad_x,"enemy_widths":w_x,"enemy_prefix":prefix,
        "group_id_dup":len(group_ids)-len(group_set),
        "enemy_id_dup":len(enemy_ids)-len(enemy_set),
        "enc_group_refs":enc_group_refs,"enc_group_set":enc_group_set,
        "enc_group_missing":sorted(enc_group_set-group_set),"unused_groups":sorted(group_set-enc_group_set),
        "group_enemy_refs":group_enemy_refs,"group_enemy_set":group_enemy_set,
        "group_enemy_missing":sorted(group_enemy_set-enemy_set),"unused_enemies":sorted(enemy_set-group_enemy_set),
        "temp_set":temp_set,"temp_missing":sorted(temp_set-eb_tempnos),"enemybase_tempnos":eb_tempnos,
        "drop_set":drop_set,"drop_missing":sorted(drop_set-item_ids),
        "cond_set":cond_set,"cond_missing":sorted(cond_set-item_ids),
        "item_ids":item_ids,
        "floors":floors,"pmins":pmins,"pmaxs":pmaxs,"zorder":z,"enemymax":enemymax,
        "group_prob_sums":group_prob_sums,"enemy_prob_sums":enemy_prob_sums,
    }

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered encounter-chain probe — R1")
    print("No original encounter/group/enemy/item names or table rows are stored in this report.")
    print("SCHEMA_SOURCE|descendant_ENCOUNT_initEncount_GROUP_initGroup_enemy_callback")
    print("CHAIN|encount.groupid -> group.id -> group.enemyid -> enemy.id -> enemy.tempno -> enemybase.tempno")
    print("DROP_CHAIN|enemy.itemid -> active_itemset.id")
    print("ENCOUNT_SCHEMA|33 columns")
    print("GROUP_SCHEMA|1 text + 23 integer/optional-integer columns")
    print("ENEMY_SCHEMA|2_or_3_text_prefix + 31 integer columns")
    if r["missing"]:
        print("MISSING_REQUIRED_FILES|"+",".join(r["missing"]));return
    print(f"ACTIVE_FILE|encount|{r['enc_path'].name}|sha256={sha256(r['enc_path'])}")
    print(f"ACTIVE_FILE|group|{r['group_path'].name}|sha256={sha256(r['group_path'])}")
    print(f"ACTIVE_FILE|enemy|{r['enemy_path'].name}|sha256={sha256(r['enemy_path'])}")
    print(f"ACTIVE_FILE|enemybase|{r['enemybase_name'] or 'NONE'}")
    print(f"ACTIVE_FILE|itemset|{r['item_name'] or 'NONE'}")
    print(f"ENCOUNT_ROWS|raw={r['enc_raw']}|parsed={len(r['enc'])}|malformed={r['enc_bad']}")
    for n,c in sorted(r["enc_widths"].items()):print(f"ENCOUNT_FIELD_COUNT|{n}|{c}")
    print(f"GROUP_ROWS|raw={r['group_raw']}|parsed={len(r['groups'])}|malformed={r['group_bad']}|duplicate_ids={r['group_id_dup']}")
    for n,c in sorted(r["group_widths"].items()):print(f"GROUP_FIELD_COUNT|{n}|{c}")
    print(f"ENEMY_ROWS|raw={r['enemy_raw']}|parsed={len(r['enemies'])}|malformed={r['enemy_bad']}|duplicate_ids={r['enemy_id_dup']}|text_prefix={r['enemy_prefix']}")
    for n,c in sorted(r["enemy_widths"].items()):print(f"ENEMY_FIELD_COUNT|{n}|{c}")

    for name,vals in (("FLOOR",r["floors"]),("ENCOUNT_MIN",r["pmins"]),("ENCOUNT_MAX",r["pmaxs"]),("ZORDER",r["zorder"]),("ENEMYMAX",r["enemymax"]),("ENCOUNT_GROUP_PROB_SUM",r["group_prob_sums"]),("GROUP_ENEMY_PROB_SUM",r["enemy_prob_sums"])):
        lo,hi,uniq=stats(vals);print(f"STAT|{name}|min={lo}|max={hi}|unique={uniq}")

    print(f"ENCOUNT_GROUP_REF|rows={len(r['enc_group_refs'])}|unique={len(r['enc_group_set'])}|matched={len(r['enc_group_set'])-len(r['enc_group_missing'])}|missing={len(r['enc_group_missing'])}")
    if r["enc_group_missing"]:print("ENCOUNT_GROUP_MISSING_SAMPLE|"+",".join(map(str,r["enc_group_missing"][:40])))
    print(f"GROUP_UNUSED_BY_ENCOUNT|{len(r['unused_groups'])}")

    print(f"GROUP_ENEMY_REF|rows={len(r['group_enemy_refs'])}|unique={len(r['group_enemy_set'])}|matched={len(r['group_enemy_set'])-len(r['group_enemy_missing'])}|missing={len(r['group_enemy_missing'])}")
    if r["group_enemy_missing"]:print("GROUP_ENEMY_MISSING_SAMPLE|"+",".join(map(str,r["group_enemy_missing"][:40])))
    print(f"ENEMY_UNUSED_BY_GROUP|{len(r['unused_enemies'])}")

    print(f"ENEMY_TEMPNO_REF|unique={len(r['temp_set'])}|enemybase_templates={len(r['enemybase_tempnos'])}|matched={len(r['temp_set'])-len(r['temp_missing'])}|missing={len(r['temp_missing'])}")
    if r["temp_missing"]:print("ENEMY_TEMPNO_MISSING_SAMPLE|"+",".join(map(str,r["temp_missing"][:40])))

    print(f"ENEMY_DROP_ITEM_REF|unique={len(r['drop_set'])}|itemset_ids={len(r['item_ids'])}|matched={len(r['drop_set'])-len(r['drop_missing'])}|missing={len(r['drop_missing'])}")
    if r["drop_missing"]:print("ENEMY_DROP_ITEM_MISSING_SAMPLE|"+",".join(map(str,r["drop_missing"][:40])))
    print(f"GROUP_CONDITION_ITEM_REF|unique={len(r['cond_set'])}|matched={len(r['cond_set'])-len(r['cond_missing'])}|missing={len(r['cond_missing'])}")
    if r["cond_missing"]:print("GROUP_CONDITION_ITEM_MISSING_SAMPLE|"+",".join(map(str,r["cond_missing"][:40])))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(a.data_dir,a.setup)

if __name__=="__main__":main()
