"""Final review evidence matrix, with explicit source and runtime boundaries."""
import json
from collections import Counter
from pathlib import Path
from stoneage_pet_source_lookup import load,build,verify,blob,search
from stoneage_pet_whole_module_review import review
ROOT=Path(__file__).resolve().parents[1]
R="research/recovered/"
P="research/pets/"
# This inventory reconciles named material carrier groups; it is not a proof that
# every potentially extant physical disc or online file has been discovered.
CARRIERS=[
("TW1_ORIGINAL","VERIFIED_SOURCE",R+"STONEAGE-PET126C-TW10-ORIGINAL-SOURCE-REACCESS-R1.json","18c288f3b836a67f8a784d31999937e9899cac11","Authenticated retail archive; previous full CRC/hash replay; album, resources and local static fields processed.","Original matching service master or original game observation."),
("TW1_PRIVATE_VISUAL","VERIFIED_SOURCE",R+"STONEAGE-PET126F-SOURCE-CUSTODY-SEVEN-DIMENSION-RESIDUAL-R1.json","c92bd2928ed1caaf155947a7e8245a28848b2fdc","Private derived observer, not another client; prior 32155 PNG/hash replay; not public assets.","Legal private reaccess or native runtime evidence."),
("CN50_PRESERVED","VERIFIED_SOURCE",P+"PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json","98fea71c051dfa887b91154a8a72d17c67b57744","Preserved CAB-derived named table and SPR/RD; not independently certified official pressing.","Official pressing or same-deployment server identity/runtime."),
("TW85_PRESERVED","VERIFIED_SOURCE",P+"PET-HIGH-FIRST-74-UNIFIED-VISUAL-R1.json","8c69875806d9dff353c60bc3834ec98197d1059d","Preserved programs and sprite/portrait evidence; 6 partial motion positions, original deployment not independently authenticated.","Exact original build/renderer or missing pixel/sequence source."),
("CN2012","VERIFIED_SOURCE",P+"PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json","a6ed895e5b6b18ebaa1c02e809da5a17937dd176","Full client transfer and resource analysis; PET124/125 and residual review processed; no native selector proof.","Same-build native selector/render observations, exact server fields."),
("TW75_CLAIMED_MASTER","CROSS_CARRIER_CANDIDATE",P+"PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json","fec03646d7c7e4e287f9347c306119cc626d6abf","467 flagged candidate template positions; claimed deployment not authenticated.","Authentic original server master, client and deployment evidence."),
("MIXED25_COMMUNITY","CROSS_CARRIER_CANDIDATE",R+"STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json","f4ac9b805724bcd847c9632cad3c35bc4309a526","Preserved mixed server file index and technical evidence, no official roster promotion.","Exact official source with independent version and operator identity."),
("JP_PERIOD_VISUAL","VERIFIED_SOURCE",R+"STONEAGE-JP-PET-VISUAL-R25-CUSTODY-R1.json","a2851606a2210e41eafd7f4c467c523ae2bb9de4","Limited private source-derived web visuals; no original client identity.","Qualified original client and same-version issuance evidence."),
("CN20_PERIOD_VISUAL","VERIFIED_SOURCE",R+"STONEAGE-CN20-NAMED-PET-VISUAL-CUSTODY-R104.json","8a6d4fe628744694547b9a21ef4b78c8b83d573b","Historical named web-visual source receipt, not complete client or native species roster.","Original client or operator primary same-build identity."),
("EARLY_JSS_KR_CN","MISSING_SOURCE",R+"STONEAGE-PET38-CLIENT-FIRST-AVAILABLE-SOURCE-INVENTORY-R1.json","47589bc59341a3ed83ecc7a7f360b8792a18a00e","JSS1999, KR2000, CN early original client missing from earlier inventory.","Lawful readable authenticated original discs/packages."),
("CN70","MISSING_SOURCE",P+"PET-HIGH-FIRST-105-CN70-ARCHIVE-REPLAY-PREFLIGHT-R1.json","802a6200640abb4721c07959118c01fffaf42eb0","Archive RAR prefix only; PET107 torrent metadata not payload.","Complete lawful original RAR with source identity and member hashes."),
("CN75","MISSING_SOURCE",P+"PET-HIGH-FIRST-113-CN75-TORRENT-IDENTITY-REVIEW-R1.json","bec4bf24c737ac0e2510a010ac50e5c65a83f015","Two exact replayed torrent metadata variants, no payload; no peer/tracker contacted.","Complete lawful original payload with verified provenance."),
("KR_NETMARBLE120","MISSING_SOURCE",R+"STONEAGE-KR-NETMARBLE120-R27-ACTUAL-SOURCE-R1.json","8e414fe8db04a3ecdd1be31335d35cee9d575049","Public thread response denied body/package; no original bytes.","Lawfully accessible original download or carrier."),
("TW2014_198","MISSING_SOURCE",R+"STONEAGE-PET97-TW2014-TAOZHU-PC198-DOWNLOAD-AND-BYTE-CUSTODY-GATES-R1.json","785928fa141c0375ed2c9cfa730cdc5ddde52ccb","Recorded installer/patch paths not obtained; environment DNS failure is not universal unavailability.","Accessible original official installer/patch with provenance."),
("TW85_SERVER_MASTER","MISSING_SOURCE",P+"PET-HIGH-FIRST-102-TW85-EMBEDDED-MASTER-SCREEN-R1.json","1535249fa4b2450a8522fba914e2aae06d28fedc","18-file limited signature screen; no hit, not proof of absence.","Original server master and matching build."),
]
def pinned(path,sha):
    raw=(ROOT/path).read_bytes()
    assert blob(raw)==sha,path
    return json.loads(raw)
def final_review():
    m,d=load(); es=build(d);verify(m,d,es)
    coverage=review()
    assert len(es)==5924 and coverage["queue_positions"]==3563 and len(m["sources"])==98
    assert coverage["official_full_fields_certified"]==0
    carriers=[]
    for name,grade,path,sha,observed,reopen in CARRIERS:
        pinned(path,sha)
        carriers.append(dict(id=name,grade=grade,source_path=path,git_blob=sha,observed=observed,reopen=reopen,original_bytes_reaccessed_this_run=False))
    chronology=pinned(R+"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json","74cd977b39b8043b9c16ca57322b35542921ffc5")
    years=[]
    for y in chronology["yearly_work_queue"]:
        path=y.get("source_bounded_review_receipt") or R+"STONEAGE-PET126-YEAR2026-YTD-CLASSIC-PC-SOURCE-AND-MODULE-GAPS-R1.json"
        raw=(ROOT/path).read_bytes()
        data=json.loads(raw)
        years.append(dict(year=y["year"],status=y["research_gate"],receipt=path,git_blob=blob(raw),historically_complete=False,official_species_count=None))
    assert [x["year"] for x in years]==list(range(1999,2027))
    assert Counter(x["status"] for x in years)=={"SOURCE_BOUNDED_REVIEWED":27,"NOT_YEAR_AUDITED":1}
    cn=pinned(R+"STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json","168e3fd24000ac02e2c2d02cdbb6a03850570df5")
    jp=pinned(R+"STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json","15394100aae36f114f52d009b2c3ac4dc685fd50")
    events=chronology["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]
    assert len(events)==len(cn["confirmed_official_release_records"])+len(jp["new_japan_classic_official_release_events"])==9
    assert all(e["region"] in ("CN","JP") and not e.get("source_record_is_global_unique_species",False) for e in events)
    # These nine retained records are a historical event subset, not the entire later literature.
    old=pinned(R+"STONEAGE-PET126T-PC-MODULE-SOURCE-COVERAGE-AND-STOP-GATE-R1.json","c8d103807d43bf9dd9cf34de9890184604bdbb60")
    v=d["review_residual_visual"]["metrics"]
    dimensions=[
      ("PROVENANCE_CARRIERS","VERIFIED_SOURCE + MISSING_SOURCE","98 pinned derivative sources, 15 carrier groups reviewed, original bytes not reaccessed; additional provenance ledger reconciliation required."),
      ("IDENTITY_NAMES_ATLAS","VERIFIED_SOURCE + CROSS_CARRIER_CANDIDATE","5924 occurrences, 3563 queue positions; nine retained documentary release events separate; no global deduplicated official roster."),
      ("2D_PIXELS_ACTIONS","VERIFIED_SOURCE + CROSS_CARRIER_CANDIDATE + UNVERIFIED_RUNTIME","TW1 120 original portraits and four pose fallbacks; CN50 305 portrait/motion positions; TW85 1889 portraits and 6 partial motion positions; TW75 424 strict references and 43 conflicts; CN2012 417 arithmetic and 131 cross-carrier motion references."),
      ("STATS_GROWTH","CROSS_CARRIER_CANDIDATE + MISSING_SOURCE","467 conditional models, 440 exact shared template rows, 26 same-ID differences, one no match; native formula/deployment not proven."),
      ("SKILLS_RULES","CROSS_CARRIER_CANDIDATE + UNVERIFIED_RUNTIME","38 configured definitions, 941 slots; historical own-table missing-skill residues retained; matching official runtime rules open."),
      ("PET_ACQUISITION_ACTIONS","CROSS_CARRIER_CANDIDATE + MISSING_SOURCE + UNVERIFIED_RUNTIME","118 double-flag routes, 13 static task reward configurations, 67 strict residual positions; conditional routes not actual official grants."),
      ("RIGHTS_PRIVATE_SOURCE_ACCESS","VERIFIED_SOURCE + MISSING_SOURCE","Private custody receipts and derived hashes retained, current legal byte access not retested, publication/use rights open.")
    ]
    assert len(old["seven_dimensions"])==len(dimensions)==7
    result=[]
    for (id,grade,observed),before in zip(dimensions,old["seven_dimensions"]):
        assert before["id"].endswith(id)
        result.append(dict(id=id,grade=grade,observed=observed,remaining=before["remaining"],reopen=before["reopen_with"],closed=False))
    return dict(schema="stoneage.pet.final_review.matrix.r1",scope="CLASSIC_PC_ONLY_SOURCE_BOUNDED_REVIEW_NOT_CLOSURE",
        manifest_sources=len(m["sources"]),lookup_occurrences=len(es),queue_positions=coverage["queue_positions"],coverage=coverage,carrier_review=carriers,
        carrier_groups_reviewed=len(carriers),year_receipts=years,documentary_events_subset=events,documentary_event_count_not_species=len(events),seven_dimensions=result,
        visual_residual_metrics=v,official_species_count=None,official_full_fields_certified=0,source_bounded_closed=False,historically_complete=False,native_runtime_verified=False,
        remaining_acceptance=["Complete material source-ledger reconciliation including obtainable but not yet integrated records.","Verify source-separated catalogue delivery and explicit user acceptance of bounded stop."],
        user_authorized_switch_to_npc=False,original_assets_published=False)
if __name__=="__main__":
    a=final_review()
    print("PET_FINAL_MATRIX_PASS "+json.dumps({k:a[k] for k in ("manifest_sources","lookup_occurrences","queue_positions","carrier_groups_reviewed","documentary_event_count_not_species","visual_residual_metrics")},ensure_ascii=False,sort_keys=True))
    print("PET_FINAL_CARRIER_GRADES="+json.dumps(dict(Counter(x["grade"] for x in a["carrier_review"])),sort_keys=True))
    Path("pet-final-review-matrix.json").write_text(json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
