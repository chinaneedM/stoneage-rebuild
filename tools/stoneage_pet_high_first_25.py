"""Recompute 2011 attestation-to-preserved-index name references; no native identity assertion."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads((ROOT/path).read_bytes())
def blob(raw): return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def main():
    d=load("research/pets/PET-HIGH-FIRST-25-2011-NAMED-SOURCE-CROSSWALK-R1.json")
    for p,s in d["source_pins_git_blob"].items():
        assert blob((ROOT/p).read_bytes())==s
    p85,p86,m,g,n,c=[load(p) for p in d["source_pins_git_blob"]]
    def names(x):
        return list(dict.fromkeys([x,"".join(d["character_map"].get(ch,ch) for ch in x)]))
    def lookup(ns):
        return dict(
            claimed_tw75_templates=[dict(name=y["name"],template_id=y["template_id"],graphic=y["graphic"],physical_line=y["physical_line"],row_sha256=y["row_sha256"]) for y in m["pet_flag_1_field_projections"] if y["name"] in ns],
            tw85_album_slots=[dict(program=p,slot=y["slot"],name=y["original_name_cp950"],portrait_alias=y["source_portrait_alias"],row_sha256=y["original_row_sha256"]) for p,z in g["programs"].items() for y in z["source_records"] if y["original_name_cp950"] in ns],
            tw85_extra_spr=[dict(graphic=y["tw85_original_spr_number"],conflicting_names=y["graphic_has_conflicting_names_across_installer_programs"],program_names={p:z["original_name_cp950"] for p,z in y["program_routes"].items()},occurrences=y["source_spr_occurrences"]) for y in n["records"] if any(z["original_name_cp950"] in ns for z in y["program_routes"].values())],
            cn50_named_slots=[dict(name=y["compiled_name"],ordinal=y["ordinal"],portrait_rd_sha256=y["portrait_lookup_rd_sha256"],graphics=[z["spr_group"] for z in y["spr_groups"]]) for y in c["records"] if y["compiled_name"] in ns])
    rows=d["rows"]
    expect=[("PET85",i,y) for i,y in enumerate(p85["named_pet_claims"])]+[("PET86",i,y) for i,y in enumerate(p86["named_pet_attestations"])]
    assert len(rows)==len(expect)==41
    for x,(receipt,i,y) in zip(rows,expect):
        assert (x["receipt"],x["position"],x["name"],x["source_id"])==(receipt,i,y["name"],y["source_id"])
        assert x["source_class"]==y.get("evidence_class",y.get("claim_class"))
        assert x["region"]==y.get("region","CN")
        assert x["version_lane"]==y.get("version_lane","CN85_CONTEXT_NOT_NATIVE_VERIFIED")
        assert x["advertised_skill"]==y.get("advertised_skill")
        assert x["exact_name_spellings"]==names(x["name"])
        assert x["direct"]==lookup(names(x["name"]))
        stem=d["qualified_label_stems"].get(x["name"])
        assert x["qualified_label_stem"]==stem
        assert x["stem_candidates"]==(lookup(names(stem)) if stem else None)
        assert not x["actual_grant_verified"] and all(x[k] is None for k in ("native_2011_pet_id","original_2011_growth","original_2011_skill_ids","first_release_date"))
    hit=lambda x:any(x.values())
    assert d["summary"]["direct_name_matches"]==sum(hit(x["direct"]) for x in rows)
    assert d["summary"]["qualified_stem_only"]==sum(not hit(x["direct"]) and x["stem_candidates"] is not None and hit(x["stem_candidates"]) for x in rows)
    assert d["summary"]["unmatched"]==sum(not hit(x["direct"]) and not (x["stem_candidates"] and hit(x["stem_candidates"])) for x in rows)
    assert d["summary"]["distinct_source_labels"]==len({x["name"] for x in rows})
    assert d["summary"]["source_attestations"]==len(rows)
    for field,key in (("tw85_album_matches","tw85_album_slots"),("tw75_template_matches","claimed_tw75_templates"),("cn50_matches","cn50_named_slots")):
        assert d["summary"][field]==sum(bool(x["direct"][key]) for x in rows)
    assert d["official_species_count"] is None and not d["original_assets_published"] and d["summary"]["new_original_2011_client_bytes"]==0
    print("PET25: 41 original receipt positions and exact named crosswalks replayed; deployment unverified")
if __name__=="__main__": main()
