"""R12: inspectable source-qualified skill, reward and acquisition records per TW75 template."""
import argparse,collections,hashlib,json
from pathlib import Path
from tools import stoneage_pet_source_lookup as lookup
MANIFEST_PIN="4a667f7354466bd61b020cb92998c6b64c2a9690"
HIST={"hf19c","hf47","hf48","hf49","hf81","hf82","hf83","hf84","hf85","hf86","hf87","hf53","hf54","hf56","hf58","hf63","fusion2003"}
OTHER={"hf46","hf50","hf51_petabi","hf52","hf62"}
SKILL={"hf61","hf89","hf90","hf91"}
def stable(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
def derive():
    assert lookup.blob((lookup.ROOT/lookup.MANIFEST).read_bytes())==MANIFEST_PIN
    manifest,d=lookup.load()
    records=lookup.build(d)
    rows=[x for x in records if x["source"]=="tw75"]
    master=d["hf76"];native=d["tw75"]["pet_flag_1_field_projections"]
    definitions={v["skill_id"]:v for v in master["configured_skill_definitions"]}
    shops=d["hf88_skillshop"]["original_skillshop_CREATE_to_parameter_rows"]
    rewards={x["tw75_row_index"]:x for x in d["hf42_cross"]["rows"]}
    floor={v["floor_id"]:v for v in d["hf45_floor"]["rows"]}
    out=[];counts=collections.Counter();pins={}
    def pin(source):
        pins[source]={k:manifest["sources"][source][k] for k in ("path","git_blob")}
    for k in ("tw75","hf76","hf88_skillshop","hf45_floor","hf42_cross","hf42","hf42_raw","hf43","hf44"):pin(k)
    for entry in rows:
        i=entry["pointer"][-1];raw=native[i];sel=master["rows"][i];tid=raw["template_id"]
        assert (sel["position"],sel["template_id"],sel["row_sha256"],sel["graphic"])==(i,tid,raw["row_sha256"],raw["graphic"])
        assert entry["labels"][0]==raw["name"]
        assert not entry["official_same_deployment_identity_verified"]
        exact=sel["selected_table_grade"]=="EXACT_SHARED_TEMPLATE_ROW"
        configured=[]
        for s in sel["configured_skill_slots"]:
            assert exact and raw["skill_slots"][s["slot_index"]]==s["skill_id"]
            df=definitions[s["skill_id"]]
            assert (s["definition_line"],s["definition_row_sha256"])==(df["line"],df["row_sha256"])
            availability=[]
            for j,shop in enumerate(shops):
                if s["skill_id"] not in shop["source_pet_skill_ids_ordered"]:continue
                f=floor.get(shop["source_floorid"]);name=f.get("later_recovered_name") if f else None
                availability.append(dict(shop_index=j,floor_id=shop["source_floorid"],map_name_candidate=name["display_name_candidate"] if name else None,parameter_path=shop["parameter_path"],rate_literal=shop["source_skill_rate_literal"],parameter_sha256=shop["source_original_sha256"],create_block_sha256=shop["create_block_sha256"],skill_list_index=[k for k,v in enumerate(shop["source_pet_skill_ids_ordered"]) if v==s["skill_id"]]))
            configured.append(dict(slot_index=s["slot_index"],definition=df,shop_configurations=availability,official_birth_skill_verified=False,official_species_learnability_verified=False))
            counts["configured_slots"]+=1
            counts["slot_shop_references"]+=len(availability)
        counts["templates_with_configured_slots"]+=bool(configured)
        counts["templates_with_configured_shop_refs"]+=any(x["shop_configurations"] for x in configured)
        reward=None
        if i in rewards:
            x=rewards[i];j=x["reward_row_index"];a=x["award_instance_id"];y=d["hf42"]["rows"][j];z=d["hf42_raw"]["rows"][j]
            assert exact and (x["template_id"],x["graphic"],x["shared_template_row_sha256"])==(tid,raw["graphic"],raw["row_sha256"])
            assert a==sel["saved_reward_instance_id"]==y["award_instance_id"]==z["award_instance_id"] and z["template_id"]==tid
            commands=[];exchanges=[];windows=[]
            for s in d["hf42_raw"]["scripts"]:
                for c in s["commands"]:
                    if a in c["numeric_literals"]:commands.append(dict(path=s["path"],command=c,token_count=c["numeric_literals"].count(a)))
            for s in d["hf43"]["projection"]["scripts"]:
                for c in s["commands"]:
                    if a in c["numeric_literals"]:exchanges.append(dict(path=s["path"],script_sha256=s["script_sha256"],command=c))
            for s in d["hf44"]["rows"]:
                if a in s["pet_slots"]:windows.append(s)
            assert commands
            reward=dict(instance=z,source_script_refs=y["script_refs"],commands=commands,exchange_controls=exchanges,window_controls=windows,official_delivery_verified=False,official_probability_verified=False)
            counts["exact_reward_templates"]+=1;counts["reward_command_references"]+=len(commands);counts["exchange_templates"]+=bool(exchanges);counts["window_templates"]+=bool(windows)
        hist=[];other=[];skill_context=[]
        for l in entry["linked_records"]:
            source=l["source"]
            if source not in HIST|OTHER|SKILL:continue
            pin(source)
            v=lookup.resolve(d,source,l["pointer"])
            # Keep literal record and its pre-existing qualification, never promote a contextual link.
            record=dict(source=source,pointer=l["pointer"],qualification=l["qualification"],record=v)
            (hist if source in HIST else other if source in OTHER else skill_context).append(record)
        counts["historical_link_occurrences"]+=len(hist);counts["templates_with_historical_links"]+=bool(hist)
        counts["other_link_occurrences"]+=len(other);counts["skill_context_occurrences"]+=len(skill_context)
        out.append(dict(template_id=tid,position=i,name=raw["name"],graphic=raw["graphic"],row_sha256=raw["row_sha256"],selected_row_sha256=sel["selected_row_sha256"],selected_grade=sel["selected_table_grade"],configured_skills=configured,reward=reward,historical_references=hist,other_acquisition_references=other,skill_context=skill_context,official_birth_skills=None,official_learnable_skills=None,official_capture=None,official_other_acquisition=None))
    assert len(out)==len({v["template_id"] for v in out})==467
    assert counts["configured_slots"]==941 and counts["exact_reward_templates"]==36
    assert len(definitions)==38 and len(shops)==21
    counts["templates"]=len(out);counts["skill_definitions"]=len(definitions);counts["shop_records"]=len(shops)
    return dict(schema="stoneage.pet.atlas_r12.skill_acquisition.r1",scope="SOURCE_QUALIFIED_CONFIG_AND_DOCUMENTARY_REFERENCES_NOT_OFFICIAL_DEPLOYMENT",source_pins=pins,summary=dict(counts),rows=out,official_field_closures=0,official_species_count=None)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();d=derive();raw=stable(d);a.output.write_bytes(raw);print("R12_SUMMARY="+json.dumps(d["summary"],sort_keys=True),flush=True);print("R12_SHA256="+hashlib.sha256(raw).hexdigest(),flush=True)
if __name__=="__main__":main()
