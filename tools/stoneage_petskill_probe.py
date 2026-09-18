#!/usr/bin/env python3
"""Analyze recovered StoneAge pet-skill tables and cross-link them to enemybase skill IDs."""

import argparse,collections,hashlib
from pathlib import Path
from tools.stoneage_enemybase_probe import analyze as analyze_enemybase

SCHEMAS={
    "legacy4":{
        "char_fields":4,
        "int_names":["ID","FIELD","TARGET","COST","ILLEGAL"],
    },
    "cfree6":{
        "char_fields":6,
        "int_names":["ID","FIELD","TARGET","COST","ILLEGAL"],
    },
    "cfree6_usetype":{
        "char_fields":6,
        "int_names":["ID","FIELD","TARGET","USETYPE","COST","ILLEGAL"],
    },
}

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

def setup_values(path):
    out={}
    if not path or not path.exists(): return out
    for raw in path.read_bytes().splitlines():
        line=raw.split(b"#",1)[0].strip()
        if b"=" not in line: continue
        k,v=line.split(b"=",1)
        key=k.decode("ascii","ignore").strip().lower()
        if key in ("petskillfile1","petskillfile2"):
            out[key]=v.decode("utf-8","replace").strip()
    return out

def rows_for(path):
    rows=[]
    counts=collections.Counter()
    max_cols=0
    for line in clean_lines(path):
        fields=[x.strip() for x in line.replace(b"\t",b" ").split(b",")]
        rows.append(fields)
        counts[len(fields)]+=1
        max_cols=max(max_cols,len(fields))
    profiles=[]; text_stats=[]
    for idx in range(max_cols):
        integer=empty=text=missing=0; text_values=[]
        for fields in rows:
            if idx>=len(fields):
                missing+=1; continue
            v=fields[idx].strip()
            if not v:
                empty+=1
            elif to_int(v) is not None:
                integer+=1
            else:
                text+=1; text_values.append(v)
        profiles.append((idx+1,integer,empty,text,missing))
        lens=collections.Counter(len(v) for v in text_values)
        text_stats.append({
            "col":idx+1,"count":len(text_values),"unique":len(set(text_values)),
            "minlen":min(lens) if lens else 0,"maxlen":max(lens) if lens else 0,
            "lengths":lens,
        })
    return rows,counts,max_cols,profiles,text_stats

def parse_schema(rows,schema):
    chars=schema["char_fields"]; ints=schema["int_names"]
    needed=chars+len(ints)
    parsed=[]; malformed=0; exact=0
    for fields in rows:
        if len(fields)<needed:
            malformed+=1; continue
        vals={}
        ok=True
        for i,name in enumerate(ints):
            v=to_int(fields[chars+i])
            if v is None:
                ok=False; break
            vals[name]=v
        if not ok:
            malformed+=1; continue
        exact += int(len(fields)==needed)
        parsed.append(vals)
    return {"rows":parsed,"malformed":malformed,"exact":exact,"needed":needed}

def enemy_skill_ids(data_dir,setup):
    active,files=analyze_enemybase(data_dir,setup)
    selected=None
    for f in files:
        if f["active"]:
            selected=f; break
    if selected is None and files:
        selected=files[0]
    skills=set(selected["skills"]) if selected else set()
    return active, selected["name"] if selected else None, skills

def analyze(data_dir,setup=None):
    config=setup_values(setup)
    enemy_active,enemy_file,enemy_ids=enemy_skill_ids(data_dir,setup)
    files=[]
    for p in sorted(data_dir.glob("petskill*.txt"),key=lambda x:x.name.lower()):
        rows,field_counts,max_cols,profiles,text_stats=rows_for(p)
        candidates={}
        for name,schema in SCHEMAS.items():
            parsed=parse_schema(rows,schema)
            ids=[r["ID"] for r in parsed["rows"] if r["ID"]>=0]
            idset=set(ids)
            coverage=len(enemy_ids & idset)
            dup=len(ids)-len(idset)
            candidates[name]={
                **parsed,
                "idset":idset,
                "coverage":coverage,
                "duplicate_ids":dup,
                "id_min":min(ids) if ids else None,
                "id_max":max(ids) if ids else None,
            }
        selected_name=max(
            candidates,
            key=lambda n:(
                candidates[n]["coverage"],
                candidates[n]["exact"],
                len(candidates[n]["rows"]),
                -candidates[n]["malformed"],
                candidates[n]["needed"],
            )
        )
        if len(candidates[selected_name]["rows"])==0:
            selected_name="unknown"
            selected={"rows":[],"malformed":len(rows),"exact":0,"needed":0,
                      "idset":set(),"coverage":0,"duplicate_ids":0,
                      "id_min":None,"id_max":None}
        else:
            selected=candidates[selected_name]
        counters={k:collections.Counter() for k in ("FIELD","TARGET","USETYPE","COST","ILLEGAL")}
        funcs=collections.Counter()
        if selected_name!="unknown":
            compatible_fields=[r for r in rows if len(r)>=selected["needed"]]
            for fields,vals in zip(compatible_fields,selected["rows"]):
                # Function name is the third string field in all descendant layouts.
                if len(fields)>=3 and fields[2]:
                    funcs[fields[2]]+=1
                for k in counters:
                    if k in vals:counters[k][vals[k]]+=1
        active_paths={Path(v.replace("\\","/")).name.lower() for v in config.values()}
        last_vs_func=None
        if rows and max_cols>3 and all(len(x)==max_cols for x in rows):
            func=[x[2].strip() for x in rows if x[2].strip()]
            tail=[x[-1].strip() for x in rows if x[-1].strip()]
            fs=set(func); ts=set(tail)
            last_vs_func={
                "func_unique":len(fs),"tail_unique":len(ts),
                "unique_overlap":len(fs&ts),
                "tail_rows_in_func_domain":sum(1 for v in tail if v in fs),
                "same_row":sum(1 for x in rows if x[2].strip() and x[-1].strip() and x[2].strip()==x[-1].strip()),
                "rows":len(rows),
            }
        missing=sorted(enemy_ids-selected["idset"])
        unreferenced=sorted(selected["idset"]-enemy_ids)
        files.append({
            "name":p.name,"bytes":p.stat().st_size,"sha":sha256(p),
            "rows":len(rows),"field_counts":field_counts,"max_cols":max_cols,"profiles":profiles,"text_stats":text_stats,
            "candidates":candidates,"selected":selected_name,
            "trailing_cols":(max_cols-selected["needed"]) if selected_name!="unknown" else None,
            "counters":counters,"func_count":len(funcs),"last_vs_func":last_vs_func,
            "active":p.name.lower() in active_paths,
            "enemy_missing":missing,"unreferenced":unreferenced,
        })
    return {
        "config":config,"enemy_active":enemy_active,"enemy_file":enemy_file,
        "enemy_ids":enemy_ids,"files":files
    }

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered pet-skill probe — R1")
    print("No original skill names/comments/options are stored in this report.")
    print("SCHEMA_SOURCE|descendant_pet_skill_h_and_pet_skill_c")
    print("SCHEMA_LEGACY4|4 char fields + ID,FIELD,TARGET,COST,ILLEGAL")
    print("SCHEMA_CFREE6|6 char fields + ID,FIELD,TARGET,COST,ILLEGAL")
    print("SCHEMA_CFREE6_USETYPE|6 char fields + ID,FIELD,TARGET,USETYPE,COST,ILLEGAL")
    print(f"ENEMYBASE_ACTIVE_CONFIG|{r['enemy_active'] or 'UNKNOWN'}")
    print(f"ENEMYBASE_SELECTED_FILE|{r['enemy_file'] or 'NONE'}")
    print(f"ENEMYBASE_UNIQUE_SKILL_IDS|{len(r['enemy_ids'])}")
    for k,v in sorted(r["config"].items()):
        print(f"PETSKILL_CONFIG|{k}|{v}")
    print(f"PETSKILL_FILE_COUNT|{len(r['files'])}")
    for f in r["files"]:
        print(f"FILE|{f['name']}|bytes={f['bytes']}|sha256={f['sha']}|rows={f['rows']}|active={int(f['active'])}|selected_prefix_schema={f['selected']}|trailing_cols={f['trailing_cols']}")
        for n,c in sorted(f["field_counts"].items()):
            print(f"FIELD_COUNT|{f['name']}|{n}|{c}")
        for col,integer,empty,textc,missing in f["profiles"]:
            print(f"COLUMN_PROFILE|{f['name']}|{col}|integer={integer}|empty={empty}|text={textc}|missing={missing}")
        for s in f["text_stats"]:
            if not s["count"]: continue
            print(f"TEXT_COLUMN_STAT|{f['name']}|{s['col']}|count={s['count']}|unique={s['unique']}|minlen={s['minlen']}|maxlen={s['maxlen']}")
            for n,c in sorted(s["lengths"].items()):
                print(f"TEXT_LENGTH|{f['name']}|{s['col']}|{n}|{c}")
        for name in SCHEMAS:
            c=f["candidates"][name]
            print(f"SCHEMA_SCORE|{f['name']}|{name}|compatible={len(c['rows'])}|malformed={c['malformed']}|exact={c['exact']}|enemy_coverage={c['coverage']}|duplicate_ids={c['duplicate_ids']}|id_min={c['id_min']}|id_max={c['id_max']}")
        if f["selected"]=="unknown":
            sel={"idset":set(),"coverage":0}
        else:
            sel=f["candidates"][f["selected"]]
        print(f"SELECTED_ID_COUNT|{f['name']}|{len(sel['idset'])}")
        if f["selected"]!="unknown" and f["trailing_cols"]:
            print(f"PREFIX_SCHEMA_TRAILING_COLUMNS|{f['name']}|{f['selected']}|{f['trailing_cols']}")
        print(f"ENEMYBASE_SKILL_COVERAGE|{f['name']}|covered={sel['coverage']}|total={len(r['enemy_ids'])}|missing={len(f['enemy_missing'])}")
        if f["enemy_missing"]:
            print(f"ENEMYBASE_SKILL_MISSING_SAMPLE|{f['name']}|"+",".join(map(str,f["enemy_missing"][:40])))
        print(f"UNREFERENCED_SKILL_ID_COUNT|{f['name']}|{len(f['unreferenced'])}")
        if f["unreferenced"]:
            print(f"UNREFERENCED_SKILL_ID_SAMPLE|{f['name']}|"+",".join(map(str,f["unreferenced"][:40])))
        print(f"UNIQUE_FUNCTION_TOKENS|{f['name']}|{f['func_count']}")
        rel=f.get("last_vs_func")
        if rel:
            print(f"LAST_COLUMN_VS_FUNC3|{f['name']}|rows={rel['rows']}|func_unique={rel['func_unique']}|tail_unique={rel['tail_unique']}|unique_overlap={rel['unique_overlap']}|tail_rows_in_func_domain={rel['tail_rows_in_func_domain']}|same_row={rel['same_row']}")
        for key in ("FIELD","TARGET","USETYPE","ILLEGAL"):
            for v,n in sorted(f["counters"][key].items()):
                print(f"{key}_VALUE|{f['name']}|{v}|{n}")
        for v,n in f["counters"]["COST"].most_common(20):
            print(f"COST_TOP|{f['name']}|{v}|{n}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args()
    emit(a.data_dir,a.setup)

if __name__=="__main__":main()
