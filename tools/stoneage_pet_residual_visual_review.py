"""Independently replay all residual visual references; do not certify original selection."""
import json
from pathlib import Path
from collections import Counter
from stoneage_pet_source_lookup import load,blob
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/pets"
def run():
    m,d=load()
    raw=(P/"PET-WHOLE-REVIEW-RESIDUAL-VISUAL-R1.json").read_bytes()
    assert blob(raw)=="320dbf690fc184434659debe7c60408a62135454"
    report=json.loads(raw)
    sources={"cn85":"cn85_original","tw85":"hf74","rd":"hf73","map":"hf30_31","cn50":"cn50","inherit":"cn50_cn85_spr_inheritance"}
    pins={k:m["sources"][v]["git_blob"] for k,v in sources.items()}
    x,v,rd,mapping,n,c=(d[k] for k in sources.values())
    def pinned(name,key):
        raw=(P/name).read_bytes()
        pins[key]=blob(raw)
        return json.loads(raw)
    z=pinned("PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json","spr")
    p=pinned("PET-WHOLE-REVIEW-TW75-TW85-PORTRAIT-REFERENCE-R1.json","tw75ref")
    assert pins==report["source_pins"]
    add={"华":"華","温":"溫","杰":"傑","库":"庫","达":"達","莱":"萊","变":"變"}
    assert report["bounded_character_additions"]==add
    cmap=mapping["character_map"]
    assert all(k not in cmap or cmap[k]==v for k,v in add.items())
    def norm(s):
        return "".join(add.get(ch,cmap.get(ch,ch)) for ch in s)
    def rd_rows(y,q):
        hashes={a["rd_sha256"] for a in y["face_map_number_candidates"]}
        return [i for i in q["portrait_rows"] if rd["observations"][str(i)]["rd_sha256"] in hashes]
    def rd_match(y,q):
        return q["portrait_alias"]==y["face"] and bool(rd_rows(y,q))
    spr=z["analysis"]["spr"]["group_rows"]
    def matches(q):
        out=[]
        for g in q["group_ids"]:
            t=v["groups"][g]
            for s in spr:
                if int(s["spr_no"])==t["graphic"] and s["segment_sha256"]==t["spr_sha256"]:
                    out.append(dict(tw_group=int(g),cn_group=int(s["index"]),number=int(s["spr_no"]),sha256=s["segment_sha256"]))
        return out
    cnrows=[]
    for y in x["analysis"]["resource_links"]["rows"]:
        if y["ordinal_spr_group_indices"] or y["slot_spr_group_indices"]:continue
        hashes={a["rd_sha256"] for a in y["face_map_number_candidates"]}
        cn=[]
        for q in n["records"]:
            if (q["compiled_name"],q["portrait_alias"])!=(y["compiled_label"],y["face"]) or q["portrait_lookup_rd_sha256"] not in hashes:continue
            groups=[g for s in c["rows"] if s["cn50_ordinal"]==q["ordinal"] for g in s["groups"] if g["cn85_exact_positions"]]
            if groups:
                for g in groups:
                    assert all(any(int(s["index"])==i and int(s["spr_no"])==g["number"] and s["segment_sha256"]==g["sha256"] for s in spr) for i in g["cn85_exact_positions"])
                cn.append(dict(ordinal=q["ordinal"],rd_sha256=q["portrait_lookup_rd_sha256"],groups=groups))
        tw=[]
        for k,q in sorted(v["positions"].items()):
            if norm(q["name"])!=norm(y["compiled_label"]) or not rd_match(y,q):continue
            groups=matches(q)
            if groups:tw.append(dict(position=k,name=q["name"],portrait_rows=rd_rows(y,q),groups=groups))
        grade="CN50_EXACT_NAME_FACE_RD_SPR" if cn else "TW85_NAME_VARIANT_EXACT_FACE_RD_SPR" if tw else "OPEN"
        cnrows.append(dict(ordinal=y["ordinal"],name=y["compiled_label"],face=y["face"],grade=grade,cn50=cn,tw85=tw))
    twrows=[]
    for y in p["rows"]:
        if y["grade"]=="EXACT_NAME_GRAPHIC_UNIQUE_ALIAS":continue
        tw=[(k,q) for k,q in v["positions"].items() if norm(q["name"])==norm(y["name"])]
        assert all(y["graphic"] not in q["graphics"] for k,q in tw)
        cn=[q["ordinal"] for q in x["analysis"]["resource_links"]["rows"] if norm(q["compiled_label"])==norm(y["name"]) and any(rd_match(q,t) for k,t in tw)]
        grade=("NAME_ONLY_GRAPHIC_CONFLICT_CROSS_CARRIER_RD_EXACT" if cn else "NAME_ONLY_GRAPHIC_CONFLICT") if tw else "NO_QUALIFIED_NAME"
        twrows.append(dict(index=y["index"],name=y["name"],graphic=y["graphic"],grade=grade,tw85_positions=sorted(k for k,q in tw),tw85_aliases=sorted({q["portrait_alias"] for k,q in tw}),tw85_graphics=sorted({g for k,q in tw for g in q["graphics"]}),cn85_exact_name_face_rd_ordinals=cn))
    assert cnrows==report["cn85_rows"]
    assert twrows==report["tw75_rows"]
    metrics={k:dict(Counter(x["grade"] for x in rows)) for k,rows in (("cn85",cnrows),("tw75",twrows))}
    assert metrics==report["metrics"]
    assert metrics["cn85"]=={"CN50_EXACT_NAME_FACE_RD_SPR":61,"TW85_NAME_VARIANT_EXACT_FACE_RD_SPR":70}
    assert metrics["tw75"]=={"NO_QUALIFIED_NAME":28,"NAME_ONLY_GRAPHIC_CONFLICT":1,"NAME_ONLY_GRAPHIC_CONFLICT_CROSS_CARRIER_RD_EXACT":14}
    assert not any(report["limits"].values())
    print("PET_RESIDUAL_VISUAL_PASS "+json.dumps(metrics,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":
    run()
