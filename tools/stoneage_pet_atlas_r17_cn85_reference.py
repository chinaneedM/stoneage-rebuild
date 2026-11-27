"""R17: verify exact pre-existing TW85 references for the 70 CN85 residual positions.
Cross-version original SPR and portrait evidence, not a native CN85 selector.
"""
import collections,hashlib,json
from pathlib import Path
from tools.stoneage_pet_atlas_r13_cn85_original import plan
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/pets"
def stable(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
def main():
    raw=(P/"PET-WHOLE-REVIEW-RESIDUAL-VISUAL-R1.json").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="320dbf690fc184434659debe7c60408a62135454"
    d=json.loads(raw)
    _,_,named,_,selected,_,_,_,groups=plan()
    by={x["ordinal"]:x for x in named}
    rows=[x for x in d["cn85_rows"] if x["grade"]=="TW85_NAME_VARIANT_EXACT_FACE_RD_SPR"]
    assert hashlib.sha256(stable(rows)).hexdigest()=="41c0b6eb555a5f771ae258d30f4402cc964f9fc9a3b7d785fe46253ca4624685"
    assert len(rows)==70 and len({x["ordinal"] for x in rows})==70
    assert len(selected)==740
    ids=set();count=0
    for x in rows:
        q=by[x["ordinal"]]
        assert (q["compiled_label"],q["face"])==(x["name"],x["face"])
        assert not q["ordinal_spr_group_indices"] and not q["slot_spr_group_indices"] and not x["cn50"]
        assert len(x["tw85"])==4
        assert {t["position"] for t in x["tw85"]}=={f"{p}.exe:{x['ordinal']}" for p in ("sa","sb","sc","sd")}
        ref=x["tw85"][0]["groups"]
        assert ref and all(t["groups"]==ref for t in x["tw85"])
        for t in x["tw85"]:
            assert t["portrait_rows"]
            for g in t["groups"]:
                i=g["cn_group"]
                assert i==g["tw_group"] and i not in selected
                assert int(groups[i]["spr_no"])==g["number"] and groups[i]["segment_sha256"]==g["sha256"]
                ids.add(i);count+=1
    assert len(ids)==263 and count==1052 and len(ids|set(selected))==1003
    print("R17_SOURCE_REFERENCE_PASS "+stable(dict(positions=70,groups=263,program_route_occurrences=count,independent_R13_groups=740,disjoint_union=1003,native_selector_verified=False,cn85_frame_pixels_verified=False,official_closures=0)).decode())
if __name__=="__main__":main()
