"""Replay a later-PC static reference chain from immutable public comparison bytes.
No original server is launched. No raw source payload is retained.
"""
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/pets/PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json"
CLAIMED = ROOT / "research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json"

def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def load(report, path, width):
    url = "https://raw.githubusercontent.com/" + report["comparison_repo"] + "/" + report["comparison_commit"] + "/" + path
    with urllib.request.urlopen(url, timeout=45) as response:
        raw = response.read(2_000_001)
    assert len(raw) <= 2_000_000
    assert blob(raw) == report["comparison_input_blobs"][path], path
    if width is None:
        return raw
    rows = [line.strip().split(b",") for line in raw.splitlines()
            if line.strip() and not line.lstrip().startswith(b"#")]
    assert all(len(row) == width for row in rows), path
    return [[x.strip() for x in row] for row in rows]

def n(x):
    return int(x) if x else -1

def index(rows, col):
    out = defaultdict(list)
    for row in rows:
        out[n(row[col])].append(row)
    return out

def level(row):
    lo, hi = n(row[5]), n(row[6])
    if lo == 0:
        lo = hi
    return [min(lo,hi),max(lo,hi)]

def is1(x):
    return x[0] <= 1 <= x[1]

def summary(rows):
    return dict(templates=len(rows),
        with_instances=sum(x["comparison_instance_count"] > 0 for x in rows),
        with_instance_petflag1=sum(x["instance_petflag1_count"] > 0 for x in rows),
        with_instance_petflag1_lv1=sum(x["instance_petflag1_lv1_count"] > 0 for x in rows),
        with_positive_routes=sum(x["positive_reference_count"] > 0 for x in rows),
        with_positive_lv1_routes=sum(x["lv1_positive_reference_count"] > 0 for x in rows),
        route_refs=sum(x["positive_reference_count"] for x in rows),
        distinct_floors=len({f for x in rows for f in x["comparison_floor_ids"]}))

def verify():
    r = json.loads(REPORT.read_bytes())
    assert r["scope"] == "LATER_COMMUNITY_PC_SAME_COMMIT_REFERENCE_CHAIN_NOT_OFFICIAL_TW75"
    assert r["comparison_repo"] == "gavinlinasd/StoneAge" and r["comparison_commit"] == "1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56"
    for k in ("official_deployment_verified","official_capture_verified","official_birth_skills_verified","runtime_executed"):
        assert r[k] is False
    assert r["official_species_count"] is None
    raw = CLAIMED.read_bytes()
    assert blob(raw) == r["claimed_catalog_blob"]
    claimed = json.loads(raw)["pet_flag_1_field_projections"]
    assert len(claimed) == 467 and all(x["pet_flag"] == 1 and not x["official_live_pet_release_verified"] for x in claimed)
    e,g,c,s1,s2,base,setup = [load(r,p,w) for p,w in [["gmsv/data/enemy1.txt",34],["gmsv/data/group1.txt",24],["gmsv/data/encount.txt",33],["gmsv/data/petskill.txt",9],["gmsv/data/petskill2.txt",12],["gmsv/data/enemybase1.txt",56],["gmsv/setup.cf",None]]]
    for key,val in ((b"enemyfile",b"enemy1.txt"),(b"enemybasefile",b"enemybase1.txt"),(b"groupfile",b"group1.txt"),(b"encountfile",b"encount.txt"),(b"petskillfile1",b"petskill.txt"),(b"petskillfile2",b"petskill2.txt")):
        assert any(line.strip().startswith(key+b"=") and line.strip().endswith(val) for line in setup.splitlines())
    ei,gi,bi,by_t = index(e,3),index(g,1),index(base,6),index(e,4)
    si1,si2 = index(s1,4),index(s2,6)
    assert all(len(v)==1 for tab in (ei,gi,si1,si2) for v in tab.values())
    routes = defaultdict(list)
    unresolved = rejected = 0
    for ordinal,x in enumerate(c,1):
        for gid,gw in zip(map(n,x[10:20]),map(n,x[20:30])):
            if gid < 0 or gw <= 0:
                continue
            if gid not in gi:
                unresolved += 1
                continue
            gr = gi[gid][0]
            resolved = [eid for eid in map(n,gr[4:14]) if eid >= 0 and eid in ei]
            if not resolved or len(resolved)!=len(set(resolved)):
                rejected += 1
                continue
            for eid,ew in zip(map(n,gr[4:14]),map(n,gr[14:24])):
                if eid not in ei or ew <= 0:
                    continue
                inst = ei[eid][0]
                tid = n(inst[4])
                if len(bi.get(tid,[]))!=1 or n(inst[13])!=1:
                    continue
                routes[tid].append(dict(floor=n(x[1]),rect=list(map(n,x[2:6])),
                    encounter_index=n(x[0]),encounter_row_ordinal=ordinal,group_id=gid,
                    enemy_id=eid,level=level(inst),group_item_gates=list(map(n,gr[2:4])),
                    event_fields=list(map(n,x[30:33])),weights=[gw,ew],
                    encounter_rate_fields=list(map(n,x[6:8]))))
    out=[]
    for x in claimed:
        tid=x["template_id"]
        ins=by_t.get(tid,[])
        fl=[v for v in ins if n(v[13])==1]
        rr=routes[tid]
        one=[y for y in rr if is1(y["level"])]
        out.append(dict(template_id=tid,comparison_status=x["comparison_status"],
            comparison_instance_count=len(ins),instance_petflag1_count=len(fl),
            instance_petflag1_lv1_count=sum(is1(level(v)) for v in fl),
            positive_reference_count=len(rr),comparison_floor_ids=sorted({y["floor"] for y in rr}),
            lv1_positive_reference_count=len(one),first_route=rr[0] if rr else None,
            first_lv1_route=one[0] if one else None))
    assert out == r["rows"]
    assert summary(out)==r["all_same_id"]
    assert summary([x for x in out if x["comparison_status"]=="EXACT_NONNAME_50_FIELD_TAIL"])==r["exact_50_field_tail_subset"]
    assert r["counts"] == dict(base_rows=len(base),enemy_rows=len(e),group_rows=len(g),
        encounter_rows=len(c),legacy_skill_rows=len(s1),extended_skill_rows=len(s2),
        enemy_flag1_rows=sum(n(x[13])==1 for x in e),
        duplicate_encounter_indices=sum(len(v)>1 for v in index(c,0).values()),
        positive_unresolved_group_slots=unresolved,positive_slots_rejected_group=rejected)
    def val(table,k,col):
        return table[k][0][col].decode("gb18030") if k in table else None
    skills=sorted({v for x in claimed for v in x["skill_slots"] if v is not None and v>=0})
    assert r["skill_ids"]==[dict(id=k,legacy_name=val(si1,k,0),extended_name=val(si2,k,0),
        legacy_function=val(si1,k,2),extended_function=val(si2,k,2)) for k in skills]
    assert r["negative_skill_sentinel_template_ids"]==[x["template_id"] for x in claimed if -1 in x["skill_slots"]]
    assert r["special_skill_witnesses"]==[dict(id=k,extended_name=val(si2,k,0),extended_function=val(si2,k,2),
        claimed_template_ids=[x["template_id"] for x in claimed if k in x["skill_slots"]]) for k in (612,639)]
    print(json.dumps(r["exact_50_field_tail_subset"],sort_keys=True))
    print("467 rows replayed; seven comparison source blobs verified; no official capture or skill promotion.")

if __name__ == "__main__":
    verify()
