"""R11 joint conditional panel growth, exact rational pre-truncation projection."""
import argparse,json,hashlib
from pathlib import Path
from functools import lru_cache
from tools.stoneage_pet_growth_model import pet_level_increments,pet_rank_from_template_base,RANK_ROLL_RANGES
from tools.stoneage_pet_high_first_tw75_conditional_ranges import ALLOCATIONS,rolls
ROOT=Path(__file__).resolve().parents[1]
DEN=2000
WEIGHTS=((80,20,20,20),(2,20,2,1),(2,2,20,1),(0,0,0,20),(4,22,22,22))
NAMES=('hp','attack','defense','agility','attack_defense_agility_sum')
PINS={
"research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json":"fec03646d7c7e4e287f9347c306119cc626d6abf",
"research/pets/PET-HIGH-FIRST-16-TW75-CONDITIONAL-BIRTH-GROWTH-R1.json":"8cb864a78f1ff2b3c89ae1739ac485968d104c10",
"research/pets/PET-HIGH-FIRST-76-SELECTED-MASTER-FIELDS-R1.json":"0005e7d7943907c01024f5dd24132b126e4bb3f3",
"tools/stoneage_pet_growth_model.py":"29910ff8b5e59fcd1a7ee306dd624ac467769853",
"tools/stoneage_pet_detail30_base_panel.py":"364005a85983a93a286873bcd2f94b71a14da06b",
"tools/stoneage_pet_high_first_tw75_conditional_ranges.py":"5b9338878786d20e0c25664b77a513f0191d0245"}
def stable(d):return (json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
@lru_cache(None)
def model(base):
    assert len(base)==4 and all(type(b)==int and 2<=b<=253 for b in base)
    r=pet_rank_from_template_base(*base);lo,hi=RANK_ROLL_RANGES[r]
    bounds=[[None,None] for _ in WEIGHTS];witnesses=[[None,None] for _ in WEIGHTS];internal=[[None,None] for _ in base]
    # Every coefficient and increment is nonnegative/monotone in base
    # offsets and common rank roll, including binary32 rounding/truncation.
    # Extremes at all-low/all-high corners are attainable. Enumerate all
    # shared ten-draw compositions there, not independent marginal maxima.
    for j,(off,roll) in enumerate(((-2,lo),(2,hi))):
        for counts in ALLOCATIONS:
            inc=pet_level_increments(tuple(b+off for b in base),r,rolls(counts),roll)
            for i,value in enumerate(inc):
                before=internal[i][j]
                if before is None or (value<before if j==0 else value>before):internal[i][j]=value
            for i,w in enumerate(WEIGHTS):
                value=sum(x*y for x,y in zip(inc,w));before=bounds[i][j]
                if before is None or (value<before if j==0 else value>before):
                    bounds[i][j]=value;witnesses[i][j]=dict(offsets=[off]*4,allocation_counts=list(counts),rank_roll=roll,internal_increment=list(inc))
    return dict(base=list(base),rank=r,rank_roll_range=[lo,hi],internal_increment_marginals=internal,denominator=DEN,panel_linear_growth_numerators=dict(zip(NAMES,bounds)),extremum_witnesses=dict(zip(NAMES,witnesses)))
def derive():
    vals={}
    for p,h in PINS.items():
        raw=(ROOT/p).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==h,p
        if p.endswith(".json"):vals[p]=json.loads(raw)
    a,b,c=list(vals.values());rows=[]
    assert len(a["pet_flag_1_field_projections"])==len(b["rows"])==len(c["rows"])==467 and len(ALLOCATIONS)==286
    for i,(x,y,z) in enumerate(zip(a["pet_flag_1_field_projections"],b["rows"],c["rows"],strict=True)):
        assert x["template_id"]==y["template_id"]==z["template_id"] and x["row_sha256"]==y["source_row_sha256"]==z["row_sha256"] and z["position"]==i
        g=model(tuple(x["base"]));assert g["rank"]==y["rank"] and g["internal_increment_marginals"]==y["per_level_internal_increment_marginal_ranges"]
        item=dict(template_id=x["template_id"],source_row_sha256=x["row_sha256"],claimed=g,official_growth_verified=False)
        v=(z["selected_fields_differing_from_claim"] or {}).get("base")
        if v is not None:
            assert v!=x["base"] and z["selected_row_sha256"]!=x["row_sha256"]
            item["saved_variant"]=dict(source_row_sha256=z["selected_row_sha256"],**model(tuple(v)))
        rows.append(item)
    assert len({r["template_id"] for r in rows})==467
    assert {r["template_id"] for r in rows if "saved_variant" in r}=={755,777,901,902,903,904}
    return dict(schema='stoneage.pet.r11.conditional_linear_panel_growth.r1',scope='CLAIMED_TW75_AND_SIX_SAVED_VARIANTS_X_LATER_PC_MODEL_NOT_OFFICIAL',allocation_compositions=len(ALLOCATIONS),offset_range=[-2,2],official_growth_verified=False,official_species_count=None,total_definition='attack + defense + agility, excluding HP; exact rational linear projection before panel integer truncation',rows=rows)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args()
    raw=stable(derive());digest=hashlib.sha256(raw).hexdigest()
    assert digest=="c1360cbbdca9e70387f85a33645ef1c37831f0697e72fbb745cdd6c6fac7fc35",digest
    if a.output:a.output.write_bytes(raw)
    print("R11_GROWTH_PASS 467 templates, 6 saved variants, exact independent local projection match SHA256 "+digest,flush=True)
if __name__=="__main__":main()
