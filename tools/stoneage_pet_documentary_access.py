"""Search retained classic PC documentary pet evidence, not additional species."""
from collections import Counter,defaultdict
import json
from stoneage_pet_source_lookup import ROOT,blob,load,build
from stoneage_pet_legacy_access import load_legacy,index

R="research/recovered/"
PINS={
 "cn20_commission":("STONEAGE-CN20-PET-COMMISSION-HABITATS-SOURCE-R1.json","6fb6bd8ea700c2a761b503eb414851bbe6090af5"),
 "cn20_catalogue":("STONEAGE-CN20-PET-COMMISSION-HABITATS-CATALOG-R1.json","56545290e9c1412666b7a2001619c53c187aab6a"),
 "cn30_special":("STONEAGE-CN30-SPECIAL-PET-SKILLS-SOURCE-R1.json","8909ba6aed8fa5f754b0628cf0f2303f41ae7651"),
 "cn2004_trainers":("STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json","b6f42811c23cadc8b80fabb0a53b98a6aa9e8b2f"),
 "o92_early":("STONEAGE-O92-EARLY-PET-ACQUISITION-CENSUS-R1.json","81eb64c6b5681e71017be352a59e480fdc39a266"),
 "pet25_release":("STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json","168e3fd24000ac02e2c2d02cdbb6a03850570df5"),
 "pet26_release":("STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json","15394100aae36f114f52d009b2c3ac4dc685fd50"),
}
def resolve(data,key,pointer):
    x=data[key]
    for p in pointer: x=x[p]
    return x
def materials():
    out={}
    for key,(path,sha) in PINS.items():
        raw=(ROOT/(R+path)).read_bytes()
        assert blob(raw)==sha,path
        out[key]=json.loads(raw)
    return out
def make_rows(d):
    rows=[]
    def add(key,pointer,id,kind,grade,pet=(),terms=(),context=None):
        names=list(dict.fromkeys(x for x in pet if isinstance(x,str) and x))
        labels=list(dict.fromkeys([id]+names+[x for x in terms if isinstance(x,str) and x]))
        path,sha=PINS[key]
        rows.append(dict(id=id,source=key,source_path=R+path,git_blob=sha,pointer=pointer,kind=kind,evidence_grade=grade,pet_labels=names,query_labels=labels,record=resolve(d,key,pointer),context=context,same_deployment_identity_verified=False,native_runtime_verified=False,global_unique_species_counted=False))
    cn=d["cn20_commission"]
    catalog=d["cn20_catalogue"]
    byid={x["record_id"]:x for x in catalog["records"]}
    assert len(byid)==len(catalog["records"])==27
    assert catalog["source_contract_path"]==R+PINS["cn20_commission"][0]
    assert catalog["authenticated_game_master_count"]==0 and cn["extracted"]["publication_date_verified"] is None
    seen=set()
    for i,q in enumerate(cn["extracted"]["commissions"]):
        id="cn20-sina-10236724:marinas-pet-"+q["id"]
        names=[x["species_label"] for x in q["targets"]]; targets={x["species_label"]:x["quantity_each"] for x in q["targets"]}
        assert byid[id]["source_relation"]["target_labels"]==names and byid[id]["source_refs"]==[q["source_page"]]
        assert len(targets)==len(names) and not q["actual_handover_or_payment_verified"]
        assert q["deposit_refund"] is None and q["net_profit_S"] is None
        seen.add(id)
        context=dict(source_page=q["source_page"],purchase=cn["extracted"]["purchase"],handin=cn["extracted"]["handin"],date=None,exact_build=None,catalogue_id=id)
        add("cn20_commission",["extracted","commissions",i],id,"commission","PORTAL_DESCRIPTION_NOT_AUTHENTICATED_QUEST",names,context=context)
        for j,h in enumerate(q["habitats_in_source_order"]):
            hid=id+":habitat-"+str(j+1); n=h["species_label"]
            assert n in targets and byid[hid]["source_relation"]==dict(quest_record=id,species_label=n,source_habitat_ordinal=j+1)
            assert byid[hid]["source_refs"]==[q["source_page"]]
            assert all(h[k] is None for k in ("spawn_level","spawn_weight","map_id","species_id"))
            seen.add(hid)
            add("cn20_commission",["extracted","commissions",i,"habitats_in_source_order",j],hid,"habitat","DOCUMENTARY_LOCATION_NOT_SPAWN_MASTER",[n],context=dict(commission_id=id,quantity=targets[n],source_page=q["source_page"],listed_cost_S=q["listed_cost_S"],listed_reward_S=q["listed_reward_S"],date=None,exact_build=None))
    assert seen==set(byid)
    assert cn["extracted"]["commissions"][-1]["listed_reward_S"] is None
    for i,x in enumerate(d["cn30_special"]["catalog_records"]):
        c=x["content"]; pet=c.get("eligible_pet_label_as_reported")
        add("cn30_special",["catalog_records",i],x["record_id"],"special_skill_claim",x["verification_status"],[pet],[c.get("name_as_written"),c.get("skill_label"),c.get("actor_category")])
    trainers=d["cn2004_trainers"]
    for group in ("first_guide_trainer_rows","second_guide_selected_rows"):
        for i,x in enumerate(trainers[group]):
            assert x["original_skill_id"] is None
            add("cn2004_trainers",[group,i],"CN-TRAINER-"+x["source_id"]+"-"+str(i+1),"trainer_skill_claim","GUIDE_NOT_NATIVE_SKILL_DEFINITION",terms=[x["name_as_page"]],context=dict(source=next(s for s in trainers["sources"] if s["id"]==x["source_id"])))
    for i,x in enumerate(trainers["crosssource_tensions"]):
        assert x["do_not_merge"] and not x["same_build_proven"]
        add("cn2004_trainers",["crosssource_tensions",i],"CN-TRAINER-CONFLICT-"+x["topic"],"trainer_conflict","CONFLICT_RETAINED_NOT_MERGED",terms=[x["topic"],x["s1_claim"].get("name"),x["s2_claim"].get("name")])
    early=d["o92_early"]
    for group,kind in (("four_starter_claims","starter_claim"),("nine_JSS_award_claims","award_claim")):
        for i,x in enumerate(early["categories"][group]):
            add("o92_early",["categories",group,i],"O92-"+kind+"-"+str(x["source_id"]),kind,"2001_DATED_PLAYER_GUIDE_NOT_OFFICIAL_GRANT",[x["name"]],context=early["source"])
    for i,x in enumerate(early["census"]["family_ranges"]):
        add("o92_early",["census","family_ranges",i],"O92-FAMILY-"+str(i+1),"guide_family_range","PLAYER_GUIDE_FAMILY_NOT_PET_MASTER",terms=[x["name"]])
    add("o92_early",["census"],"O92-CENSUS","guide_census","PLAYER_GUIDE_ORDINALS_NOT_GLOBAL_SPECIES",context=dict(source=early["source"],categories=early["categories"],limits=early["limits"]))
    for i,x in enumerate(d["pet25_release"]["confirmed_official_release_records"]):
        assert x["counts_as_operator_release_record"] and not x["counts_as_unique_global_species"] and not x["source_is_user_private_server_only"]
        name=x["official_name_as_written"]
        add("pet25_release",["confirmed_official_release_records",i],x["record_id"],"documented_release",x["status"],[name] if x["record_identity_kind"]=="NAMED_PET" else [],[name])
    for i,x in enumerate(d["pet26_release"]["new_japan_classic_official_release_events"]):
        assert not x["private_server_provenance"] and x["global_species_count_contribution"] is None
        name=x["official_name_as_written_or_null"]
        add("pet26_release",["new_japan_classic_official_release_events",i],x["id"],"documented_release",x["status"],[name] if x["identity_kind"]=="NAMED_PET" else [],[name])
    for i,x in enumerate(d["pet26_release"]["japan_2008_existing_base_evolution_records"]):
        assert not x["is_four_new_named_species"] and x["evolved_new_form_name_or_null"] is None
        add("pet26_release",["japan_2008_existing_base_evolution_records",i],x["id"],"evolution_base","EXISTING_BASE_NOT_NEW_NAMED_SPECIES",[x["name"]])
    for i,x in enumerate(d["pet26_release"]["japan_official_version_species_count_snapshots"]):
        assert x["not_a_global_cross_region_species_total"]
        add("pet26_release",["japan_official_version_species_count_snapshots",i],"JP-REPORTED-COUNT-"+x["date"],"regional_count_snapshot","PUBLISHER_REPORTED_REGIONAL_COUNT_NOT_GLOBAL",terms=[x["date"]])
    for key,group in (("pet25_release","remaining_unconfirmed_official_leads"),("pet26_release","japan_taiwan_prelaunch_or_mechanic_leads")):
        for i,x in enumerate(d[key][group]):
            assert not x.get("counts_in_release_records",x.get("counts_as_official_released_pet"))
            id=x.get("lead_id",x.get("id")); name=x.get("name_as_source",x.get("official_name_as_written_or_null"))
            add(key,[group,i],id,"unconfirmed_release_lead",x["status"],terms=[name])
    return rows
def attach_names(rows):
    m,d=load(); current=build(d)
    legacy=index(load_legacy())
    assert len(current)==5924 and len(legacy)==2792
    labels=defaultdict(list)
    for x in current:
        for name in set(x["labels"]):
            s=m["sources"][x["source"]]
            labels[name].append(dict(directory="current",source=x["source"],path=s["path"],git_blob=s["git_blob"],pointer=x["pointer"],label=name,qualification="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY"))
    for x in legacy:
        if x["name"]:
            labels[x["name"]].append(dict(directory="PET16",source=x["namespace"],path="research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json",git_blob="fdb7d9aade2df62d1a1e06b2d2f9e383693ed980",pointer=x["pointer"],label=x["name"],qualification="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY"))
    for row in rows:
        row["candidate_refs"]={name:labels[name] for name in row["pet_labels"]}
    return dict(current_occurrences=len(current),pet16_rows=len(legacy))
def search(rows,q,source=None,exact=False):
    return [r for r in rows if (source is None or r["source"]==source) and any((q==n if exact else q in n) for n in r["query_labels"])]
def verify(rows,counts):
    byid={r["id"]:r for r in rows}
    kinds=Counter(r["kind"] for r in rows)
    assert len(rows)==len(byid)==140
    assert kinds=={"commission":6,"habitat":21,"special_skill_claim":15,"trainer_skill_claim":30,"trainer_conflict":5,"starter_claim":4,"award_claim":9,"guide_family_range":28,"guide_census":1,"documented_release":9,"evolution_base":4,"regional_count_snapshot":2,"unconfirmed_release_lead":6}
    assert len({r["pet_labels"][0] for r in rows if r["kind"]=="habitat"})==19
    assert all(not r[k] for r in rows for k in ("same_deployment_identity_verified","native_runtime_verified","global_unique_species_counted"))
    assert all(l["label"]==n and l["qualification"]=="EXACT_LITERAL_LABEL_ONLY_NOT_IDENTITY" for r in rows for n,ls in r["candidate_refs"].items() for l in ls)
    poison=[x for x in search(rows,"猛毒攻击","cn2004_trainers",True) if x["kind"]=="trainer_skill_claim"]
    assert sorted(x["record"]["listed_price"] for x in poison)==[4000,4400]
    assert len(search(rows,"乌力","cn20_commission",True))==2
    assert byid["cn20-sina-10236724:marinas-pet-F"]["record"]["listed_reward_S"] is None
    assert len(search(rows,"帖拉所伊朵","cn30_special",True))==12
    assert not any(r["candidate_refs"] for r in rows if r["kind"] in ("trainer_skill_claim","trainer_conflict","guide_family_range","regional_count_snapshot","unconfirmed_release_lead"))
    assert not search(rows,"not-a-real-pet-name",exact=True)
    names={n for r in rows for n in r["pet_labels"]}
    matched={n for r in rows for n,ls in r["candidate_refs"].items() if ls}
    return dict(schema="stoneage.pet.documentary_lookup.r1",source_pins=len(PINS),documentary_records=len(rows),by_kind=dict(kinds),exact_pet_label_candidates=len(names),labels_with_exact_directory_candidate=len(matched),labels_without_exact_directory_candidate=sorted(names-matched),records_with_any_candidate=sum(any(r["candidate_refs"].values()) for r in rows),candidate_references_not_identity=sum(len(ls) for r in rows for ls in r["candidate_refs"].values()),official_release_events_previously_documented=9,new_release_certifications=0,official_species_count=None,source_bounded_closed=False,**counts)
def run(args):
    if args.variants: raise SystemExit("documentary mode uses literal labels only; variant identity is not established")
    if args.source and args.source not in PINS: raise SystemExit("unknown documentary source")
    rows=make_rows(materials()); counts=attach_names(rows); report=verify(rows,counts)
    if args.verify:
        print("PET_DOCUMENTARY_LOOKUP_PASS "+json.dumps(report,ensure_ascii=False,sort_keys=True)); return
    if args.summary or not args.query:
        print(json.dumps(report,ensure_ascii=False,indent=2)); return
    hits=search(rows,args.query,args.source,args.exact)
    if not args.full: hits=[{k:v for k,v in x.items() if k not in ("record","context")} for x in hits]
    print(json.dumps(dict(query=args.query,source_occurrences=len(hits),official_species_count=None,results=hits),ensure_ascii=False,indent=2))
