#!/usr/bin/env python3
"""Analyze recovered StoneAge skillcode.txt and cross-link it to enemybase/petskill."""

import argparse,collections,hashlib
from pathlib import Path
from tools.stoneage_enemybase_probe import analyze as analyze_enemybase

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

def parse_skillcode(path):
    rows=[]; malformed=0
    for line in clean_lines(path):
        fields=line.split()
        if len(fields)<4:
            malformed+=1; continue
        try:
            tempno=int(fields[1],10); petid=int(fields[2],10)
        except ValueError:
            malformed+=1; continue
        rows.append({"tempno":tempno,"petid":petid,"code":fields[3]})
    return rows,malformed

def parse_petskill_kindcodes(path):
    rows=[]; malformed=0
    if not path.exists(): return rows,malformed
    for line in clean_lines(path):
        fields=[x.strip() for x in line.replace(b"\t",b" ").split(b",")]
        # Recovered active table has a descendant-compatible prefix:
        # col6 KINDCODE, col7 ID. Trailing columns are deliberately ignored.
        if len(fields)<7:
            malformed+=1; continue
        try: skillid=int(fields[6],10)
        except ValueError:
            malformed+=1; continue
        rows.append({"id":skillid,"kindcode":fields[5]})
    return rows,malformed

def active_enemy(data_dir,setup):
    active,files=analyze_enemybase(data_dir,setup)
    selected=None
    for f in files:
        if f["active"]:
            selected=f;break
    if selected is None and files:selected=files[0]
    tempnos=set(r["TEMPNO"] for r in selected["rows"]) if selected else set()
    return active,selected["name"] if selected else None,tempnos

def analyze(data_dir,setup=None):
    skillcode=data_dir/"skillcode.txt"
    petskill=data_dir/"petskill.txt"
    enemy_active,enemy_file,enemy_tempnos=active_enemy(data_dir,setup)
    if not skillcode.exists():
        return {"exists":False,"enemy_active":enemy_active,"enemy_file":enemy_file}
    rows,bad=parse_skillcode(skillcode)
    ps,psbad=parse_petskill_kindcodes(petskill)
    petids=[r["petid"] for r in rows]; tempnos=[r["tempno"] for r in rows]
    petid_counter=collections.Counter(petids)
    duplicate_petids=sum(1 for _,n in petid_counter.items() if n>1)
    matched_rows=sum(1 for r in rows if r["petid"] in enemy_tempnos)
    unique_petids=set(petids)
    matched_petids=unique_petids & enemy_tempnos
    unmatched_petids=sorted(unique_petids-enemy_tempnos)
    enemy_without_code=sorted(enemy_tempnos-unique_petids)

    nonempty=[r for r in ps if r["kindcode"]]
    empty=[r for r in ps if not r["kindcode"]]
    kind_match=0; kind_nomatch=[]
    capability_counts=[]
    for s in nonempty:
        matching={r["petid"] for r in rows if s["kindcode"] in r["code"]}
        if matching:
            kind_match+=1
            capability_counts.append(len(matching))
        else:
            kind_nomatch.append(s["id"])

    code_lengths=collections.Counter(len(r["code"]) for r in rows)
    return {
        "exists":True,"path":skillcode,"bytes":skillcode.stat().st_size,"sha":sha256(skillcode),
        "rows":rows,"malformed":bad,"petid_min":min(petids) if petids else None,
        "petid_max":max(petids) if petids else None,"petid_unique":len(unique_petids),
        "duplicate_petids":duplicate_petids,"tempno_min":min(tempnos) if tempnos else None,
        "tempno_max":max(tempnos) if tempnos else None,"tempno_unique":len(set(tempnos)),
        "enemy_active":enemy_active,"enemy_file":enemy_file,"enemy_count":len(enemy_tempnos),
        "matched_rows":matched_rows,"matched_petids":len(matched_petids),
        "unmatched_petids":unmatched_petids,"enemy_without_code":enemy_without_code,
        "petskill_rows":len(ps),"petskill_malformed":psbad,
        "kind_nonempty":len(nonempty),"kind_empty":len(empty),"kind_match":kind_match,
        "kind_nomatch":sorted(kind_nomatch),"capability_counts":capability_counts,
        "code_lengths":code_lengths,
    }

def emit(data_dir,setup=None):
    r=analyze(data_dir,setup)
    print("StoneAge recovered skill-code crosslink probe — R1")
    print("No original pet/skill names or code strings are stored in this report.")
    print("SCHEMA_SOURCE|descendant_Load_PetSkillCodes_and_NPC_CHECKFREEPETSKILL")
    print("FOREIGN_KEY_SOURCE|CHAR_PETID_equals_enemybase_TEMPNO")
    if not r["exists"]:
        print("SKILLCODE_FILE_EXISTS|0");return
    print("SKILLCODE_FILE_EXISTS|1")
    print(f"FILE|skillcode.txt|bytes={r['bytes']}|sha256={r['sha']}|rows={len(r['rows'])}|malformed={r['malformed']}")
    print(f"PETID_STAT|min={r['petid_min']}|max={r['petid_max']}|unique={r['petid_unique']}|duplicate_keys={r['duplicate_petids']}")
    print(f"TEMPNO_FIELD_STAT|min={r['tempno_min']}|max={r['tempno_max']}|unique={r['tempno_unique']}")
    print(f"ENEMYBASE_SELECTED|{r['enemy_file'] or 'NONE'}|templates={r['enemy_count']}")
    print(f"PETID_ENEMYBASE_COVERAGE|matched_unique={r['matched_petids']}|skillcode_unique={r['petid_unique']}|matched_rows={r['matched_rows']}")
    print(f"PETID_NOT_IN_ENEMYBASE_COUNT|{len(r['unmatched_petids'])}")
    if r["unmatched_petids"]:print("PETID_NOT_IN_ENEMYBASE_SAMPLE|"+",".join(map(str,r["unmatched_petids"][:40])))
    print(f"ENEMYBASE_WITHOUT_SKILLCODE_COUNT|{len(r['enemy_without_code'])}")
    if r["enemy_without_code"]:print("ENEMYBASE_WITHOUT_SKILLCODE_SAMPLE|"+",".join(map(str,r["enemy_without_code"][:40])))
    print(f"PETSKILL_PREFIX_ROWS|{r['petskill_rows']}|malformed={r['petskill_malformed']}")
    print(f"PETSKILL_KINDCODE_EMPTY|{r['kind_empty']}")
    print(f"PETSKILL_KINDCODE_NONEMPTY|{r['kind_nonempty']}")
    print(f"PETSKILL_KINDCODE_MATCHED_BY_ANY_CODE|{r['kind_match']}")
    print(f"PETSKILL_KINDCODE_UNMATCHED_COUNT|{len(r['kind_nomatch'])}")
    if r["kind_nomatch"]:print("PETSKILL_KINDCODE_UNMATCHED_SKILL_IDS|"+",".join(map(str,r["kind_nomatch"][:40])))
    if r["capability_counts"]:
        print(f"KINDCODE_CAPABILITY_PET_COUNT|min={min(r['capability_counts'])}|max={max(r['capability_counts'])}|unique={len(set(r['capability_counts']))}")
    for n,c in sorted(r["code_lengths"].items()):
        print(f"CODE_LENGTH|{n}|{c}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(a.data_dir,a.setup)

if __name__=="__main__":main()
