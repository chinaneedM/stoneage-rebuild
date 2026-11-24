"""Verify bounded JP/KR named dossier projections and cross-year masks."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-22-JP-KR-NAMED-INDEX-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s
    ev={x["id"]:x for x in d["events"]}; rows=d["rows"]
    assert len(ev)==10 and len(rows)==len({(x["region"],x["name"]) for x in rows})==29
    expected={(e["region"],n) for e in ev.values() for n in e["names"]}
    assert expected=={(x["region"],x["name"]) for x in rows}
    for x in rows:
        assert x["attestations"]==[dict(event=e["id"],date=e["date"],kind=e["kind"]) for e in ev.values() if e["region"]==x["region"] and x["name"] in e["names"]]
        assert not x["actual_grant_verified"] and all(x[k] is None for k in ("historical_native_id","original_sprite","original_animation","birth_stats","growth","skills","first_release_date"))
        for i in x["images"]:assert i["name"]==x["name"] and x["name"] in ev[i["event"]]["names"] and i["raw_sha256"] is None and i["original_sprite_id"] is None
    imgs=[i for x in rows for i in x["images"]];assert len(imgs)==13 and sum(i["status"]=="WEB_RENDERED_MANUALLY_OBSERVED" for i in imgs)==4
    p78=read("research/recovered/STONEAGE-PET78-2008-JP-NAMED-PET-POOL-AND-SOURCE-GATES-R1.json");p79=read("research/recovered/STONEAGE-PET79-YEAR2008-FIVE-REGION-SOURCE-BOUNDED-AUDIT-R1.json");evo=read("research/recovered/STONEAGE-JP2008-PET-EVOLUTION-SOURCE-R1.json")
    assert ev["JP080922"]["names"]==p78["japan_2008_random_pool_names_ordered"] and ev["JP091013"]["names"]==p78["japan_2009_later_evolved_pet_names_ordered"]
    assert ev["KR081117"]["names"]==p79["korean_2008_newly_named_obtainable_pet"]
    assert ev["JP081111"]["names"]==evo["inputs"][0]["extracted"]["facts"]["eligible_pet_labels"]
    masks=evo["inputs"][1]["extracted"]["facts"]["eligibility_name_masks"]
    for x,y in zip(d["evolution_mask_candidates"],masks):
        assert x["input"]==y["before"] and x["mask"]==y["evolved_mask"]
        assert x["compatible_2009_names"]==[n for n in ev["JP091013"]["names"] if re.fullmatch(x["mask"].replace("？","."),n)] and len(x["compatible_2009_names"])==1 and not x["pairing_verified"]
    assert len(d["evolution_mask_candidates"])==4 and d["official_species_count"] is None and not d["original_assets_published"]
    print("PET22: 29 regional named dossiers, 13 labelled image references, four unverified mask matches")
if __name__=="__main__":main()
