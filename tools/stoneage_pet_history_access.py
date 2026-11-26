"""Read-only chronology view over the exact accepted annual source receipts."""
import json
from collections import Counter
from stoneage_pet_source_lookup import ROOT, blob
from stoneage_pet_documentary_access import PINS as DOC_PINS, R as DOC_ROOT

MATRIX=("research/pets/PET-FINAL-REVIEW-MATRIX-R1.json","8a3694119db2c0b83dbe6b0c54fc7d912a8493c6")
QUEUE=("research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json","74cd977b39b8043b9c16ca57322b35542921ffc5")
REGIONS=("CN","TW","HK_MO","KR","JP","OTHER")
REGIONS_EARLY=set(REGIONS)-{"HK_MO"}
REGIONS_LATE=set(REGIONS)
LANE_KEYS=("operator","operators","operator_tracks","version_tracks","tracks","distinct_live_service_tracks","operator_product_version_lane","version_lane","lane","provenance_scope")
BOUNDARY_KEYS=("bounded_evidence","evidence","named_pet_evidence_grade","source_note","evidence_grade","verification_boundary","scope","prior_qualified_source_summary","open_source_gap","source_status","known","gap","grade","known_bounded_source_grade","source_boundary","original_native_and_issuance_gap","source_grade","pet_roster_missing","absence_1999_proven","next_attestation","release_date_attested","period_product_milestones","period_2005_pet_labels")
def read_pin(path,sha):
    raw=(ROOT/path).read_bytes()
    assert blob(raw)==sha,("changed historical source",path)
    return json.loads(raw)
def ref(path,sha,pointer):
    return dict(path=path,git_blob=sha,pointer=pointer)
def selected_fields(row,keys):
    return {k:row[k] for k in keys if k in row}
def build_history():
    m=read_pin(*MATRIX); q=read_pin(*QUEUE)
    assert m["official_species_count"] is None and not m["historically_complete"] and not m["source_bounded_closed"]
    assert q["active_module"]=="PET" and q["pc_only_scope_supersession"]["classic_pc_only_source_filter"]
    assert q["pc_only_scope_supersession"]["active_original_pc_release_event_count"]==9
    events=q["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]
    assert events==m["documentary_events_subset"] and len(events)==9
    event_records={}
    for ns,key,group,id_key in (("PET25","pet25_release","confirmed_official_release_records","record_id"),("PET26","pet26_release","new_japan_classic_official_release_events","id")):
        path,sha=DOC_PINS[key]; path=DOC_ROOT+path
        d=read_pin(path,sha)
        for i,x in enumerate(d[group]):
            event_records[(ns,x[id_key])]=(x,ref(path,sha,[group,i]))
    assert len(event_records)==9
    event_view=[]
    for e in events:
        x,p=event_records[(e["source_namespace"],e["source_id"])]
        assert x["region"]==e["region"] and x["product_line"]==e["product_line"]
        assert e["name"]==x.get("official_name_as_written",x.get("official_name_as_written_or_null"))
        assert not e["source_record_is_global_unique_species"]
        assert int(e["chronology_date"][:4])==e["year"]
        literal=x.get("official_release_version_or_event")
        # Only an explicit mainland version prefix identifies a version label here.
        # The WGS crossover product's 2.0 must NOT be assigned as a StoneAge version.
        version=None
        if literal and literal.startswith("大陆"):
            version=literal[2:5]
            assert version in ("3.0","4.0")
        event_view.append(dict(**e,source_record=p,identity_kind=x.get("record_identity_kind",x.get("identity_kind")),source_version_or_event_literal=literal,explicit_stoneage_version_label=version,record=x))
    years=[]; regional=[]
    assert [x["year"] for x in m["year_receipts"]]==list(range(1999,2027))
    assert [x["year"] for x in q["yearly_work_queue"]]==list(range(1999,2027))
    for e,work in zip(m["year_receipts"],q["yearly_work_queue"]):
        y=e["year"]; path=e["receipt"]; sha=e["git_blob"]
        d=read_pin(path,sha)
        assert d["year"]==y and e["official_species_count"] is None and not e["historically_complete"]
        assert e["status"]==work["research_gate"] and work["historical_species_count"] is None
        if y<2026:
            assert d.get("review_status",d.get("status"))=="SOURCE_BOUNDED_REVIEWED" and not d["historically_complete"]
        else:
            a=d["annual_review"]
            assert a["yearly_research_gate"]=="NOT_YEAR_AUDITED" and a["status"]=="IN_PROGRESS_YTD_SOURCE_BOUND_PRELIMINARY"
            assert not a["annual_closeout_allowed"] and a["official_original_pc_global_species_count"] is None
        key="region_source_reviews" if "region_source_reviews" in d else "region_reviews"
        regions=d[key]
        assert set(regions)==(REGIONS_EARLY if y<=2010 else REGIONS_LATE)
        ids=[x["source_id"] for x in event_view if x["year"]==y]
        assert sorted(ids)==sorted(work["documented_release_event_ids_from_existing_PET25_PET26"])
        assert len(ids)==work["pc_only_eligible_documentary_events"]
        year_reopen={k:v for k,v in d.items() if "reopen" in k and isinstance(v,(list,dict))}
        years.append(dict(year=y,year_review_status=e["status"],receipt=ref(path,sha,[]),regions_recorded=[r for r in REGIONS if r in regions],separate_region_receipt_not_recorded=[r for r in REGIONS if r not in regions],documented_release_event_subset_ids=ids,historical_global_species_count=None,historically_complete=False,year_reopen_conditions=year_reopen,as_of_date=d.get("as_of_date"),year_closeout_allowed=False))
        for region in REGIONS:
            if region not in regions: continue
            z=regions[region]
            assert not z.get("historically_complete",False)
            reopen=selected_fields(z,("reopen","reopen_trigger","reopen_condition","trigger"))
            regional.append(dict(year=y,region=region,year_review_status=e["status"],region_review_status_as_written=z.get("review_status"),source=ref(path,sha,[key,region]),operator_or_version_lane_as_written=selected_fields(z,LANE_KEYS),evidence_and_boundaries_as_written=selected_fields(z,BOUNDARY_KEYS),region_reopen_conditions=reopen,year_reopen_conditions_if_no_separate_region_trigger=year_reopen if not reopen else {},historical_species_count=None,historically_complete=False,record=z))
    milestones=[]
    byid={x["id"]:x for x in q["version_milestone_candidate_sources"]}
    assert len(byid)==6
    for i,x in enumerate(q["version_milestone_date_claims_not_pet_release_proofs"]):
        assert x["line"].startswith("STONEAGE_CLASSIC_PC")
        assert x["region"] in REGIONS and all(s in byid for s in x["sources"])
        milestones.append(dict(**x,year=int(x["date_claim"][:4]),source_record=ref(*QUEUE,["version_milestone_date_claims_not_pet_release_proofs",i]),source_details=[byid[s] for s in x["sources"]],qualification="VERSION_DATE_CLAIM_NOT_PET_RELEASE_PROOF"))
    return years,regional,milestones,event_view

def filter_history(years,regional,milestones,events,year=None,region=None,version=None,query=None,exact=False):
    def scope(x):
        return (year is None or x["year"]==year) and (region is None or x.get("region")==region)
    def text_match(values):
        return not query or any((query==s if exact else query in s) for s in values if isinstance(s,str))
    ms=[x for x in milestones if scope(x) and (version is None or x["claimed_version"]==version) and text_match([x["id"],x["claimed_version"],x["event_type"]])]
    ev=[x for x in events if scope(x) and (version is None or x["explicit_stoneage_version_label"]==version) and text_match([x["source_id"],x["name"],x["source_version_or_event_literal"]])]
    # When filtering explicit version/name claims, regional receipts are only context
    # for matching years and regions, never a version-specific or species-specific assignment.
    pairs={(x["year"],x["region"]) for x in ms+ev}
    rr=[x for x in regional if scope(x) and ((version is None and query is None) or (x["year"],x["region"]) in pairs)]
    yy=[x for x in years if (year is None or x["year"]==year) and ((version is None and query is None) or x["year"] in {p[0] for p in pairs})]
    return yy,rr,ms,ev

def verify(years,regional,milestones,events):
    assert len(years)==28 and len(regional)==156 and len(milestones)==12 and len(events)==9
    assert len({(x["year"],x["region"]) for x in regional})==156
    assert Counter(x["year_review_status"] for x in years)=={"SOURCE_BOUNDED_REVIEWED":27,"NOT_YEAR_AUDITED":1}
    assert Counter(x["region"] for x in regional)=={"CN":28,"TW":28,"HK_MO":16,"JP":28,"KR":28,"OTHER":28}
    assert Counter(x["region"] for x in events)=={"CN":5,"JP":4}
    assert sum(x["identity_kind"]=="NAMED_PET" for x in events)==5
    assert sum(x["name"] is None for x in events)==1
    assert sum(x["identity_kind"]=="FAMILY_OR_CARD_SERIES" for x in events)==3
    assert all(x["historical_species_count"] is None for x in regional)
    assert all(x["year_review_status"]=="NOT_YEAR_AUDITED" and x["region_review_status_as_written"]=="YTD_PARTIAL_OPEN" for x in regional if x["year"]==2026)
    a=filter_history(years,regional,milestones,events,year=2002,region="CN")
    assert len(a[0])==len(a[1])==1 and len(a[3])==4
    a=filter_history(years,regional,milestones,events,year=2001,region="HK_MO")
    assert len(a[0])==1 and "HK_MO" in a[0][0]["separate_region_receipt_not_recorded"] and not any(a[1:])
    a=filter_history(years,regional,milestones,events,version="3.0")
    assert [x["id"] for x in a[2]]==["TW-2002-3.0"] and {x["source_id"] for x in a[3]}=={"CN-PC-3-GP","CN-PC-3-YEAR"}
    a=filter_history(years,regional,milestones,events,version="2.0")
    assert {x["id"] for x in a[2]}=={"TW-2001-2.0","CN-2001-2.0"} and not a[3]
    a=filter_history(years,regional,milestones,events,query="ハクエン",exact=True)
    assert len(a[3])==1 and a[3][0]["source_id"]=="JP-2009-HAKUEN"
    a=filter_history(years,regional,milestones,events,version="99.0")
    assert not any(a)
    return dict(schema="stoneage.pet.chronology_access.r1",annual_receipts_verified=28,region_year_receipts=156,source_bounded_reviewed_years=27,open_years=[2026],separate_HK_MO_receipts_from=2011,version_date_claims_not_pet_release_proofs=12,documented_release_event_subset_not_species=9,named_pet_event_records=5,family_or_card_records=3,unnamed_pair_event_records=1,official_species_count=None,source_bounded_closed=False,active_module="PET")

def run(args):
    if args.source or args.variants: raise SystemExit("history uses year, region and explicit version/name filters; source IDs and variants belong to other modes")
    if args.exact and not args.query: raise SystemExit("--exact requires --query in history mode")
    years,regional,milestones,events=build_history(); report=verify(years,regional,milestones,events)
    if args.verify:
        print("PET_HISTORY_ACCESS_PASS "+json.dumps(report,ensure_ascii=False,sort_keys=True));return
    if args.summary or not any((args.year,args.region,args.version,args.query)):
        print(json.dumps(dict(**report,years=[{k:v for k,v in x.items() if k!="year_reopen_conditions"} for x in years]),ensure_ascii=False,indent=2));return
    yy,rr,ms,ev=filter_history(years,regional,milestones,events,args.year,args.region,args.version,args.query,args.exact)
    if not args.full:
        rr=[{k:v for k,v in x.items() if k!="record"} for x in rr]
        ev=[{k:v for k,v in x.items() if k!="record"} for x in ev]
    print(json.dumps(dict(filters=dict(year=args.year,region=args.region,version=args.version,query=args.query,exact=args.exact),years=yy,regional_receipt_context_not_version_assignment=rr,version_date_claims=ms,documented_release_event_subset=ev,official_species_count=None,notes=["No match does not prove no historical content.","Regional receipts are dated bounded source reviews, not version or pet identity masters.","Exact version filter covers only explicit indexed milestone labels and explicit release-version labels, not every historical version or narrative lane.","Nine release events are the retained PET25/PET26 subset, not all official release reports in annual evidence.","Original receipt text may preserve excluded-product context; excluded products are not active pet or release records."]),ensure_ascii=False,indent=2))
