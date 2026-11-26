"""Replay source-pinned CN50 named SPR links against authenticated CN2012 original segments."""
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
P50 = "research/pets/PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json"
P85 = "research/pets/PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json"
PC = "research/pets/PET-CN50-CN85-NATIVE-NAME-CROSSWALK-R1.json"
REPORT = "research/pets/PET-CN50-CN85-SPR-INHERITANCE-R1.json"
def load(path, expected=None):
    raw = (ROOT / path).read_bytes()
    if expected:
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == expected
    return json.loads(raw)
def main():
    d = load(REPORT)
    assert d["input_git_blobs"] == dict(cn50="98fea71c051dfa887b91154a8a72d17c67b57744",cn85="a6ed895e5b6b18ebaa1c02e809da5a17937dd176",name_crosswalk="74c0c112fed4597ee8135228625b7c3fea81a245")
    a = load(P50,d["input_git_blobs"]["cn50"])
    b = load(P85,d["input_git_blobs"]["cn85"])
    c = load(PC,d["input_git_blobs"]["name_crosswalk"])
    assert b["original_client_verified"] and not b["analysis"]["adrn"]["actual_real_bytes_verified"]
    by = {}
    for i,x in enumerate(b["analysis"]["spr"]["group_rows"]):
        assert i == int(x["index"])
        by.setdefault(int(x["spr_no"]),[]).append((i,x))
    rows = []
    for i,p in enumerate(a["records"]):
        cr = c["rows"][p["ordinal"]]
        assert cr["cn50"]["name"] == p["compiled_name"]
        groups = []
        for g in p["spr_groups"]:
            candidates = by.get(g["spr_group"],[])
            groups.append(dict(number=g["spr_group"],sha256=g["sha256"],cn85_exact_positions=[j for j,x in candidates if x["segment_sha256"]==g["sha256"]],cn85_same_number_positions=[j for j,x in candidates]))
        rows.append(dict(cn50_record_index=i,cn50_ordinal=p["ordinal"],cn50_name=p["compiled_name"],cn85_same_ordinal=cr["cn85_same_ordinal"],cn85_same_name_candidates=cr["cn85_same_name_candidates"],groups=groups))
    assert rows == d["rows"]
    flat = [g for row in rows for g in row["groups"]]
    assert all(len(g["cn85_exact_positions"]) == len(g["cn85_same_number_positions"]) == 1 for g in flat)
    assert len({g["cn85_exact_positions"][0] for g in flat}) == 594
    duplicate = [dict(number=n,positions=[dict(index=i,sha256=x["segment_sha256"]) for i,x in v]) for n,v in by.items() if len(v)>1]
    assert duplicate == d["cn85_duplicate_numbers"]
    assert all(len({p["sha256"] for p in x["positions"]})==1 for x in duplicate)
    summary = dict(cn50_named_positions=len(rows),cn50_linked_groups=len(flat),cn85_same_number_exact_groups=sum(bool(g["cn85_exact_positions"]) for g in flat),cn50_named_positions_all_groups_exact=sum(all(g["cn85_exact_positions"] for g in row["groups"]) for row in rows),cn85_physical_groups=sum(map(len,by.values())),cn85_distinct_numbers=len(by),cn85_duplicate_numbers=len(duplicate),official_field_closures=0)
    assert summary == d["summary"] == dict(cn50_named_positions=305,cn50_linked_groups=594,cn85_same_number_exact_groups=594,cn50_named_positions_all_groups_exact=305,cn85_physical_groups=1837,cn85_distinct_numbers=1833,cn85_duplicate_numbers=3,official_field_closures=0)
    assert not any(d[k] for k in ("original_assets_published","official_identity_verified","cn85_native_selector_verified","cn85_rd_verified"))
    print("CN50_CN85_SPR_INHERITANCE_PASS",json.dumps(summary,sort_keys=True),flush=True)
if __name__ == "__main__":
    main()
